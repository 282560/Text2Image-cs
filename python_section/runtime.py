from maker import Maker

import argparse
import easydict
import torch
import time
import json
import os


parser = argparse.ArgumentParser(description='Generate image.')
parser.add_argument('--CUDACARD', action='store', type=str, help='Set the number of the GPU card that will not be masked.')
args = parser.parse_args()

os.system("set CUDA_VISIBLE_DEVICES=" + args.CUDACARD)
torch.empty(0).cuda() # Zainicjowanie cuda() na pustym tensorze

rootdir = 'clients_request'
# rootdir = os.path.join('clients_request')
while True:
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            filepath = os.path.join(subdir, file)
            if filepath.endswith(".json"):
                with open(filepath) as f:
                    data = json.load(f)
                    ID, file_extension = os.path.splitext(file)
                    cat = data["category"]
                    lang = data["language"]
                    desc = data["description"]

                    checking_folder = os.path.join('..', 'public', 'clients_images')
                    dirs_suffix = ''

                    ds_name = cat
                    paths = easydict.EasyDict({})

                    if ds_name == 'flowers':
                        paths = easydict.EasyDict({
                            'datasetFile': os.path.join(dirs_suffix, 'datasets', '102flowers'),
                            'textDir': 'text_c10',
                            'maxEpochs': '1000'
                        })
                    elif ds_name == 'birds':
                        paths = easydict.EasyDict({
                            'datasetFile': os.path.join(dirs_suffix, 'datasets', 'caltech_ucsd_birds'),
                            'textDir': 'text_c10',
                            'maxEpochs': '1000'
                        })
                    elif ds_name == 'three_flowers':
                        paths = easydict.EasyDict({
                            'datasetFile': os.path.join(dirs_suffix, 'datasets', 'three_flowers'),
                            'textDir': 'text_c10',
                            'maxEpochs': '1000'
                        })
                    elif ds_name == 'three_birds':
                        paths = easydict.EasyDict({
                            'datasetFile': os.path.join(dirs_suffix, 'datasets', 'three_birds'),
                            'textDir': 'text_c10',
                            'maxEpochs': '2000'
                        })
                    elif ds_name == 'three_fruits':
                        paths = easydict.EasyDict({
                            'datasetFile': os.path.join(dirs_suffix, 'datasets', 'three_fruits'),
                            'textDir': 'text_c10',
                            'maxEpochs': '1000'
                        })

                    maker = Maker(
                        datasetFile=paths.datasetFile,
                        textDir=paths.textDir,
                        checking_folder=checking_folder,
                        lang=lang,
                        client_txt=desc,
                        pre_trained_gen=os.path.join(dirs_suffix, 'checkpoints', ds_name + '_cls_test', 'gen_' + paths.maxEpochs + '.pth'),
                        pre_trained_disc=os.path.join(dirs_suffix, 'checkpoints', ds_name + '_cls_test', 'disc_' + paths.maxEpochs + '.pth'),
                        ID=ID )

                    maker.generate()
                os.remove(filepath)
    time.sleep(0.5)
    print('Listening folder ' + rootdir + '...')