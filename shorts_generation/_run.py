import os, sys, subprocess, random

ifile = sys.argv[1] if len(sys.argv) else exit
    
os.chdir(os.path.dirname(os.path.realpath(__file__)))

dlina, vysota   = 720, 1024
#длина 1080 - 9/16, 1440 - 3/4

text_size       = 40
margin_bottom   = 150
line_spacing    = 100
font            = 'Roboto_SemiCondensed-Medium.ttf'
text_border     = 5

start           = 0
shag            = random.randint(15, 35)
fade_dur        = 0.5

dur = int(subprocess.check_output(rf'ffprobe.exe -i "{ifile}" -show_entries format=duration -v quiet -of csv="p=0"').decode('utf-8').split(".")[0])

if dur > 59 :
    start = random.randint(0, dur - shag)
else :
    shag = dur

subprocess.run(rf'ffmpeg.exe -ss {start} -t {shag} -i "{ifile}" -c:v libx264 -preset ultrafast -profile:v baseline ' + 
 rf'-filter_complex "[0:v]scale=-1:{vysota},crop={dlina}:{vysota},gblur=sigma=10[bg];[0:v]scale={dlina}:-1[ov];[0:a]volume=1.0[audio];[bg][ov]overlay=(W-w)/2:(H-h)/2,'+
 rf'drawtext=text=\'twitch s1rmtrpr\':fontfile={font}:fontcolor=white:fontsize={text_size}:x=w/2-text_w/2:y=h-{margin_bottom}-{line_spacing}:bordercolor=black:borderw={text_border},'+
 rf'fade=type=in:duration={fade_dur},fade=type=out:start_time={shag - fade_dur}:duration={fade_dur}[mix];" -map "[mix]" -map "[audio]" '+
 rf'-r 60 "{os.path.splitext(ifile)[0]}_{start}_shorts.mp4" -y')
