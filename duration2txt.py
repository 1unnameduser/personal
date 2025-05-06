import sys, subprocess

print(sys.argv[1])
file    = sys.argv[1] if sys.argv[1] else exit
durfile = rf'{file}.txt'
dur     = str(subprocess.check_output(rf'ffprobe.exe -i "{file}" -show_entries format=duration -sexagesimal -v quiet -of csv="p=0"').decode('utf-8').split(".")[0])
open(durfile, 'w').write(dur)
