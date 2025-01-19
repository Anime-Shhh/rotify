# Rotify

##Disclaimer: This project is not aimed to automate the creation of short video formats such as those of tiktok or youtube shorts for a profit. It is simply a tool to create attention grabbing videos for those who struggle to read without getting distracted. 

##Please do not use this code in order to create something similar for money-making purposes. Other than that, you are free to utilize this code, all I ask is that you give credits to me in the read me or in any other form in your project. 

This project is a Python-based tool that aims to convert text extracted from a PDF file into a video with accompanying audio narration and subtitles. It is designed to provide a seamless way to turn static PDF content into engaging, multimedia-rich output.

---

## Features
- **Text Extraction from PDF**: Reads text from a PDF file using `PyPDF2`.
- **Text-to-Speech (TTS)**: Converts the extracted text into speech using `gTTS`.
- **Subtitles Generation**: Automatically generates subtitles from the audio transcript using `AssemblyAI`'s transcription API.
- **Audio and Video Integration**: Synchronizes the generated audio with the video.
- **Subtitle Overlay**: Adds timed subtitles to the video, ensuring clear and readable captions.

---

## Requirements
Ensure you have the following installed:
- Python 3.10+
- Required Python libraries:
  - `PyPDF2`
  - `gTTS`
  - `moviepy`
  - `pysrt`
  - `assemblyai`
- AssemblyAI API Key (sign up at [AssemblyAI](https://www.assemblyai.com/) to get your key).

---

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/pdf-to-video-converter.git
   cd pdf-to-video-converter
   ```
2. Set up a Python virtual environment (optional but recommended):
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # Linux/Mac
   myenv\Scripts\activate    # Windows
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Place your input files (PDF, video, and font) in the `files/` directory, matching the formats and names of mine(for the easiest setup)

---

## Usage
1. **Prepare the Input Files**:
   - PDF File: Place your source PDF in `files/random.pdf`.
   - Video File: Add your base video (e.g., a background video) as `files/minecraftParkour.mp4`.
   - Font File: Include your desired font file (e.g., Montserrat) as `files/mont/Mont-HeavyDEMO.otf`.

2. **Set Your API Key**:
   Open the `apiKeys.py` file and update the `AssemblyAIKey` variable with your API key:
   ```python
   AssemblyAIKey = "your_api_key_here"
   ```

3. **Run the Script**:
   Execute the script with:
   ```bash
   python3 main.py
   ```

4. **Output**:
   The final video will be generated in `files/superFinal.mp4`, complete with synced audio and subtitles.

---

## My File Structure
```
project/
├── files/
│   ├── random.pdf            # Input PDF file
│   ├── minecraftParkour.mp4  # Input video file
│   ├── audio.mp3             # Generated audio
│   ├── subtitle.srt          # Generated subtitles
│   ├── video_and_audio.mp4   # Video with synced audio
│   ├── superFinal.mp4        # Final video with subtitles
│   └── mont/
│       └── Mont-HeavyDEMO.otf  # Custom font
├── main.py                   # Main script
├── apiKeys.py                # API key configuration
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## Future Enhancements
- Add support for multiple font styles and sizes.
- Allow customization of subtitle positioning.
- Add error handling for missing or unsupported files.
- Implement a GUI for easier user interaction.

---

## Acknowledgments
- **AssemblyAI**: For their transcription API.
- **MoviePy**: For seamless video editing capabilities.
- **PyPDF2**: For efficient PDF text extraction.
- **gTTS**: For converting text to speech.

---

Feel free to contribute by submitting issues or pull requests!
