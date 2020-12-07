from torch.utils.data import Dataset, DataLoader
from models.gan_factory import gan_factory
from corpus_loader import CorpusLoader
from torch.autograd import Variable
from urllib import request, error
from PIL import Image, ImageDraw
from googletrans import Translator

import numpy as np

# NEW ###########
import requests #
import json     #
#################

import torch
import os

class Maker(object):

    def __init__(self, datasetFile, textDir, checking_folder, lang, client_txt, pre_trained_gen, pre_trained_disc, ID, batch_size=1):

        self.generator = torch.nn.DataParallel(gan_factory.generator_factory('gan').cuda())
        self.generator.load_state_dict(torch.load(pre_trained_gen))

        self.discriminator = torch.nn.DataParallel(gan_factory.discriminator_factory('gan').cuda())
        self.discriminator.load_state_dict(torch.load(pre_trained_disc))

        self.checking_folder = checking_folder
        self.lang = lang
        self.client_txt = client_txt
        self.filename = ID
        self.batch_size = batch_size

        cl = CorpusLoader(datasetFile=datasetFile, textDir=textDir)
        self.vectorizer = cl.TrainVocab()

    def generate(self):

        # translator = Translate_GoogleTrans(txt=self.client_txt) # For googletrans
        translator = Translate_MyMemory(txt=self.client_txt)

        if self.network_connection():
            try:
                status, translated = translator.translation()
            except:
                self.generate_error_image('Translator\nerror', self.checking_folder, self.filename)
                return  # Translator error
            if ((self.lang == 'en') and (status != 200)) or ((self.lang != 'en') and (status != 200)):
                txt = translator.parse_only()
            else:
                txt = translated
        else:
            self.generate_error_image('Connection\nerror', self.checking_folder, self.filename)
            return  # No network connection

        captions = []
        captions.append(txt)

        vector = self.vectorizer.transform(captions)
        raw_vector = vector.toarray()
        embed = torch.FloatTensor(np.array(raw_vector[0]))
        embed = Variable(embed.float()).cuda()

        noise = Variable(torch.randn(self.batch_size, 100)).cuda()
        noise = noise.view(noise.size(0), 100, 1, 1)
        opds = OnePieceDataset(embed=embed)
        data_loader = DataLoader(opds, batch_size=self.batch_size, shuffle=False, num_workers=0)

        single_el = next(iter(data_loader))

        self.generator.eval()
        fake_image = self.generator(single_el, noise)

        self.discriminator.eval()
        outputs, _ = self.discriminator(fake_image, single_el)

        dir_path = os.path.dirname(os.path.realpath(__file__))

        for fimage in fake_image:
            img = Image.fromarray(fimage.data.mul_(127.5).add_(127.5).byte().permute(1, 2, 0).cpu().numpy())
            img.save(os.path.join(self.checking_folder, self.filename + '.jpeg'))

        return

    @staticmethod
    def network_connection():
        try:
            request.urlopen('http://216.58.192.142', timeout=1) # Google Default Server
            return True
        except error.URLError as err:
            return False

    @staticmethod
    def generate_error_image(error_txt, checking_folder, filename):
        W, H = (64, 64)
        img = Image.new('RGB', (W, H), color = (0, 0, 0))
        d = ImageDraw.Draw(img)
        w, h = d.textsize(error_txt)
        d.text(((W-w)/2,(H-h)/2), error_txt, fill=(255, 255 ,255))
        img.save(os.path.join(checking_folder, filename + '.jpeg'))
        
class Translate_GoogleTrans():

    def __init__(self, txt):
        self.txt = txt

    def translation(self):
        translator = Translator()
        tr = translator.translate(self.txt, dest='en')

        translated = tr.text.lower()
        if translated[-1] != '.':
            translated += '.'

        return translated

    def check_lang(self):
        translator = Translator()
        detector = translator.detect(self.txt)
        return detector.lang


class Translate_MyMemory():

    def __init__(self, txt):
        self.txt = txt
        method = 'get'
        extended_requests = '282560@stud.umk.pl'
        source_lang = 'autodetect'
        target_lang = 'en'
        self.url = 'https://api.mymemory.translated.net/' + method + '?q=' + txt + '&de=' + extended_requests + '&langpair=' + source_lang + '|' + target_lang

    def translation(self):
        res = requests.get(self.url)
        json_res = json.loads(res.text)
        tr = json_res['responseData']['translatedText']
        status = json_res['responseStatus']


        translated = tr.lower()
        if translated[-1] != '.':
            translated += '.'

        return status, translated

    def parse_only(self):
        parsed = self.txt.lower()
        if parsed[-1] != '.':
            parsed += '.'

        return parsed

class OnePieceDataset(Dataset):

    def __init__(self, embed):
        self.embed = embed

    def __len__(self):
        return 1

    def __getitem__(self, item):
        return self.embed
