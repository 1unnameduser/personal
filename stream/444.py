from instagrapi import Client # type: ignore
import os, random, subprocess, datetime, var # type: ignore
#import youtube_upload

os.chdir(os.path.dirname(os.path.realpath(__file__)))

dir                             = var.dir
fps                             = var.fps
text                            = var.text
key                             = var.twitchkey

instUSERNAME, instPASSWORD      = var.instUSERNAME, var.instPASSWORD
caption                         = var.caption

dlina, vysota                   = var.dlina, var.vysota
text_size                       = var.text_size
margin_bottom                   = var.margin_bottom
line_spacing                    = var.line_spacing
font                            = var.font
text_border                     = var.text_border
shag                            = var.shag
fade_dur                        = var.fade_dur
uploadfilename                  = var.uploadfilename

while True:
    ifile, dur  = None, None
    ifile       = random.choice(os.listdir(dir))

    print('=== START on ' + str(datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")))
    print(f'{ifile}')

    dur = int(subprocess.check_output(f'ffprobe -i "{dir}/{ifile}" -show_entries format=duration -v quiet -of csv="p=0"', shell=True).decode('utf-8').split(".")[0])

    start = random.randint(0, dur - shag)

    print('Стрим на твич')
    subprocess.run(f'ffmpeg -thread_queue_size 1M -hide_banner -loglevel error -nostats -re -i "{dir}/{ifile}" -r {fps} -c:v libx264 '
    f'-x264-params "keyint={fps*2}:scenecut=0" -preset superfast ' 
    f'-filter_complex "[0:v]scale=-2:480:flags=lanczos[v0];[v0]drawtext=text={text}:fontcolor=white:fontsize=15:x=10:y=10:bordercolor=black:borderw=3[video];'
    f'[0:a]volume=1.0[audio]" -map [video] -map [audio] -b:v 3M -minrate 3M -maxrate 3M -bufsize 512k -threads 3 '
    f'-f flv rtmp://hel03.contribute.live-video.net/app/{key}', shell = True) #TWITCH

    print('Генерю файл')
    subprocess.run(f'ffmpeg -hide_banner -loglevel error -nostats -re -ss {start} -t {shag} -i "{dir}/{ifile}" -c:v libx264 -preset superfast -profile:v baseline ' + 
    f'-filter_complex "[0:v]scale=-1:{vysota},crop={dlina}:{vysota},gblur=sigma=10[bg];[0:v]scale={dlina}:-1[ov];[0:a]volume=1.0[audio];[bg][ov]overlay=(W-w)/2:(H-h)/2,'+
    f'drawtext=text=\'twitch s1rmtrpr\':fontfile={font}:fontcolor=white:fontsize={text_size}:x=w/2-text_w/2:y=h-{margin_bottom}-{line_spacing}:bordercolor=black:borderw={text_border},'+
    f'fade=type=in:duration={fade_dur},fade=type=out:start_time={shag - fade_dur}:duration={fade_dur}[mix];" -map "[mix]" -map "[audio]" '+
    f'-r 60 {uploadfilename} -y', shell=True)
    
    print('Рилс в инсту')
    try:
        cl = Client()
        cl.set_proxy("socks5://127.0.0.1:1080")
        print(f"🔑 Logging into {instUSERNAME}...")
        cl.load_settings("instagram_session.json")
        cl.login (instUSERNAME, instPASSWORD) # this doesn't actually login using username/password but uses the session
        cl.get_timeline_feed() # check session
        print(f"✅ Successfully logged in to {instUSERNAME}")

        # Uploading the video
        print(f"📤 Uploading video for {instUSERNAME}")
        cl.video_upload(uploadfilename, caption)
        print(f"🎬 Video uploaded successfully to {instUSERNAME}")

        #cl.logout()
        #print(f"🚪 Logged out from {instUSERNAME}.")

    except Exception as e:
        print(f"❌ Error uploading video to {instUSERNAME}: {e}")

    print('Шортс в ютюб')
    subprocess.run(["python", "youtube_upload.py"])

    print('=== END on ' + str(datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")))
