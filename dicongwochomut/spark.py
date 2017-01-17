import os
import subprocess

try:
    with open("life", "r") as f:
        pass
except:
    import sys
    sys.exit(1)

incarnation = '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
# Hardcoded because muh bug
mac = 84440840607841L
pid = os.getpid()

newstr = ""
i = 1
for c in str(incarnation):
    n = str(mac)[i%len(str(mac))]
    p = str(pid)[i%len(str(pid))]
    newstr += str(int(c)*int(n)*int(p)+i)[-1]
    i+=1

with open("corpus", "r") as f:
    corpus = int(f.read()[:-1])
os.utime("manifestation.py", None) # Same as "touch" command. Metaphysical reasons.

try:
    with open("draw_corpus", "r") as f:
        draw_corpus = int(f.read()[:-1])
except:
    pass

with open("dicongwochomut/spark.py", "r") as f:
    core = f.readlines()

core[10] = "incarnation = '"+newstr+"'\n"

with open("dicongwochomut/egg.py", "w") as f:
    f.write("".join(core))

subprocess.call("./dicongwochomut/samsara.sh")
