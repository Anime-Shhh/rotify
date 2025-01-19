import assemblyai as aai
import pysrt
from apiKeys import AssemblyAIKey
from PyPDF2 import PdfReader
from gtts import gTTS
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
from moviepy.video.fx import Crop

aai.settings.api_key = AssemblyAIKey

# get text from File

pdf_file = "files/random.pdf"
unedited_audio_file = "files/audio.mp3"
sped_up_audio = "files/final.mp3"
original_video = "files/minecraftParkour.mp4"
srt_file = "files/subtitle.srt"
video_and_audio = "files/video_and_audio.mp4"
final_video = "files/superFinal.mp4"
font_path = "files/mont/Mont-HeavyDEMO.otf"


def extractText(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text.strip()


# generate text to speech with gtts
def generate_audio(text, output_file):
    tts = gTTS(text)
    tts.save(output_file)  # returns an mp3
    return output_file


def generate_transcript(audio_file):
    transcript = aai.Transcriber().transcribe(audio_file)
    subtitles = transcript.export_subtitles_srt(chars_per_caption=15)

    f = open("files/subtitle.srt", "w")
    f.write(subtitles)
    f.close()


def combine_audio_and_shorten(audio_file, video_file, final_video_file):
    video = VideoFileClip(video_file)
    audio = AudioFileClip(audio_file)

    final = video.subclipped(start_time=0, end_time=audio.duration)
    final = final.with_audio(audio)
    final.write_videofile(final_video_file, codec="libx264", fps=30)


def time_to_seconds(time_obj):
    return time_obj.hours * 3600 + time_obj.minutes * 60 + time_obj.seconds + time_obj.milliseconds/1000


def make_subtitles(srt_file, video_file):
    srt_subtitles = pysrt.open(srt_file)
    subtitle_clips = []

    for subtitle in srt_subtitles:
        print(subtitle.text)
        start_time = time_to_seconds(subtitle.start)
        end_time = time_to_seconds(subtitle.end)
        duration = end_time - start_time

        video = VideoFileClip(video_file)
        video_width, video_height = video.size

        print("TextClip reached")
        subtitle_clip = (
            TextClip(text=subtitle.text,
                     font_size=24,
                     font=font_path,
                     color='white', stroke_color='black',
                     stroke_width=1,
                     size=(int(video_width*3/4), None),
                     method='caption').with_start(start_time).with_duration(duration))
        text_position = ('center', 'center')
        subtitle_clips.append(subtitle_clip.with_position(text_position))

    return subtitle_clips


# MAKE A FINAL VIDEO PARAMETER IF IT DOESNT WORK TO COMBINE THE VIDEO ON ITSELF
def add_subtitles_to_video(subtitle_clips, video_file, final_video_file):
    video = VideoFileClip(video_file)
    video = CompositeVideoClip([video] + subtitle_clips)
    video.write_videofile(final_video_file)


def main():
    print("extracting text")
    text = extractText(pdf_file)

    print("generating audio")
    generate_audio(text, unedited_audio_file)

    print("generating transcript with AssemblyAI")
    generate_transcript(unedited_audio_file)

    print("shortening video and adding audio")
    combine_audio_and_shorten(
        unedited_audio_file, original_video, video_and_audio)

    print("generating subtitles from the transcript")
    try:
        subtitle_clips = make_subtitles(srt_file, video_and_audio)
    except Exception as e:
        print(f"Error is in make Subtitles: {e}")

    print("Adding subtitles on top of the video")
    add_subtitles_to_video(subtitle_clips, video_and_audio, final_video)

    print("Done")


main()
