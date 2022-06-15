import tika
from tika import parser
from os import listdir
from os.path import join, isfile
from concurrent.futures import ThreadPoolExecutor

# mielőtt a szkriptet indítod, el kell indítani a Tika-t
# java -jar tika-app-1.18.jar -s
tika.initVM()
in_path = 'data/raw'
out_path = 'data/txt'
raw_texts = [f for f in listdir(in_path) if isfile(join(in_path, f))]


def process_pdf(raw_text):
    parsed = parser.from_file(join(in_path, raw_text))
    plain_text = parsed['content'].strip()
    fname = raw_text.split('.')[0] + '.txt'
    with open(join(out_path, fname), 'w') as f:
        f.write(plain_text)


with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(process_pdf, raw_texts)
