import os


pathDir='input'
onlyfiles = [os.path.join(pathDir, f) for f in os.listdir(pathDir) if os.path.isfile(os.path.join(pathDir, f))]
for x in onlyfiles:
    print(x)