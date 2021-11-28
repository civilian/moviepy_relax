import sys

from numpy.core.fromnumeric import clip
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip

from os import listdir
from os.path import isfile, join

from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

# print ("Script name: %s" % str(sys.argv[0]))
# print ("First argument: %s" % str(sys.argv[1]))
#print ("Second argument: %s" % str(sys.argv[2]))
total = len(sys.argv)
if total < 6:
    print("usage python moviepy.py FILE_BACKGROUND  FILE_SOUND  FILE_INIT  DIR_IN  FILE_OUT [AUDIO]")
else:
    path = sys.argv[4]
    files = [sys.argv[3]] # I add the presentation
    files.extend([join(path, f) for f in listdir(path) if isfile(join(path, f))])
    print(files)
    start = 0
    clips = []
    clips_with_sound = []

    background = VideoFileClip(sys.argv[1], audio=False)

    audio_boolean = total > 6

    for f in files:
        video_clip = VideoFileClip(f, audio=audio_boolean).set_start(start).set_position("center")
        video_clip = video_clip.resize(height=background.h)
        start = video_clip.end
        clips.append(video_clip)
    
    end = clips[-1].end
    background = background.subclip(0, end)
    clips.insert(0, background) # I add the background
    # while clip[-1].end < end:
    print(clips)
    video = CompositeVideoClip(clips)
    if not audio_boolean:
        audio = AudioFileClip(sys.argv[2]).subclip(0, clips[-1].end)
        video = video.set_audio(audio)
    video.write_videofile(sys.argv[5],
                    # audio_codec='aac', 
                    # temp_audiofile='temp-audio.m4a', 
                    # remove_temp=True
                    )