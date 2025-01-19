import assemblyai as aai
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
    subtitles = transcript.export_subtitles_srt(chars_per_caption=30)

    f = open("files/subtitle.srt", "a")
    f.write(subtitles)
    f.close()


# format the transcript
def format_subtitles(srt_file):
    subtitles = []
    # break srt into chunks about each subtitle
    chunks = srt_file.strip().split("\n\n")
    for chunk in chunks:
        # break chunk down into parts (sub no., time, subtitle)
        lines = chunk.split("\n")
        if len(lines) >= 3:  # ensure its valid 3 piece
            timing = [lines[1].split("-->")]
            start = timing_helper(timing[0])
            end = timing_helper(timing[1])
            subtitle = " ".join(lines[2:])
            subtitles.append(start, end, subtitle)
    return subtitles


def timing_helper(timing):
    hr, min, sec = timing.split(":")
    secs, millis = sec.split(",")
    timestamp = int(hr) * 3600 + int(min) * 60 + int(secs) + int(millis)/1000
    return timestamp


def add_text_to_vid(video_file, audio_file, subtitles, output_file):
    video = VideoFileClip(video_file)
    audio = AudioFileClip(audio_file)

    video = video.subclipped(0, audio.duration)

    video = video.with_audio(audio)

    subtitle_clips = []

    for start, end, subtitle in subtitles:
        subtitle_clip = ((TextClip(text=subtitle, font_size=24, color='white',
                                   stroke_color='black', stroke_width=1,
                                   font='Ariel-Bold'))
                         .set_position('center')
                         .set_duration(end - start)
                         .set_start(start))
        subtitle_clips.append(subtitle_clip)

    # combine clips
    #
    final_vid = CompositeVideoClip([video] + subtitle_clips)
    # write the File
    final_vid.write_videofile(output_file, codec="libx264", fps=30)


def main():
    print("extracting text")
    text = extractText(pdf_file)

    print("generating audio")
    generate_audio(text, unedited_audio_file)

    print("generating transcript with AssemblyAI")
    generate_transcript(unedited_audio_file)

    print("generating subtitles from the transcript")
    subtitles = format_subtitles(srt_file)

    print("making video")
    (add_text_to_vid(original_video, unedited_audio_file, subtitles,
                     "files/final.mp4"))

    print("Done")


main()
