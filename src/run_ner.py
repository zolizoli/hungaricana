import subprocess
from os import listdir
from os.path import isfile, join
from concurrent.futures import ThreadPoolExecutor

in_path = 'data/txt'
out_path = 'data/ner'

txts = [f for f in listdir(in_path) if isfile(join(in_path, f))]
c = len(txts)
command = 'java -Xmx3G -jar etc/ner.jar -mode predicate -input %s -output %s'


def run_ner(txt):
    outname = txt.split('.')[0] + '.out'
    local_command = command % (join(in_path, txt), join(out_path, outname))
    local_command = local_command.split()
    try:
        subprocess.run(local_command)
    except Exception as e:
        print(e)
        pass


with ThreadPoolExecutor(max_workers=3) as executor:
    executor.map(run_ner, txts)
