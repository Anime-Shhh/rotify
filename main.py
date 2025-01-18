import assemblyai as aai
from apiKeys import AssemblyAIKey
from PyPDF2 import PdfReader
from gtts import gTTS
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip

aai.settings.api_key = AssemblyAIKey

# get text from File

pdf_file = "files/random.pdf"
audio_file = "files/audio.mp3"


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
    subtitles = transcript.export_subtitles_srt(chars_per_caption=100)

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
            start = timing[0]
            end = timing[1]
            subtitle = " ".join(lines[2:])
            subtitles.append(start, end, subtitle)
    return subtitles


def main():
    print("extracting text")
    text = extractText(pdf_file)

    print("generating audio")
    generate_audio(text, audio_file)

    print("generating transcript with AssemblyAI")
    generate_transcript(audio_file)

    print("Done")


main()
