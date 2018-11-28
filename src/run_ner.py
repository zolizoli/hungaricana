import subprocess
from os import listdir
from os.path import isfile, join

in_path = 'data/txt'
out_path = 'data/ner'

txts = [f for f in listdir(in_path) if isfile(join(in_path, f))]

command = 'java -Xmx3G -jar etc/ner.jar -mode predicate -input %s -output %s'
for txt in txts:
    outname = txt.split('.')[0] + '.out'
    local_command = command % (join(in_path, txt), join(out_path, outname))
    local_command = local_command.split()
    try:
        subprocess.run(local_command)
    except Exception as e:
        print(e)
        continue
