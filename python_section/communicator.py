import argparse
import time
import json
import os


def listener(rootdir, max_time=60):
    for iter in range(1, (max_time * 2)): # (max * 2) daje okolo 60 sekund, bo sleep trwa 0.5 sekundy
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                filepath = os.path.join(subdir, file)
                ID, file_extension = os.path.splitext(file)
                if (ID == args.ID) and filepath.endswith(".jpeg"):
                    return
        time.sleep(0.5)
        print('Listening folder ' + rootdir + '...')

parser = argparse.ArgumentParser(description='Generate image.')
parser.add_argument('--ID', action='store', type=str, help='User\'s ID.')
parser.add_argument('--cat', action='store', type=str, help='Dataset category.')
parser.add_argument('--lang', action='store', type=str, help='Input language.')
parser.add_argument('--desc', action='store', type=str, help='Description.')
args = parser.parse_args()

data =  '{ "category":"' + args.cat + '", "language":"' + args.lang + '", "description":"' + args.desc + '"}'
data = json.loads(data)

with open(os.path.join('python_section', 'clients_request', args.ID + '.json'), 'w') as f:
    json.dump(data, f, indent=4)

listener(os.path.join('public', 'clients_images'))