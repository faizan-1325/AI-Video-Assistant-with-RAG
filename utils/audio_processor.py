import yt_dlp
from pydub import AudioSegment
import os

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

#this method downloads the audio from youtube and saves it as a wav file in the downloads folder
def download_yt_audio(url: str)-> str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "noplaylist": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192",
        }],
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
    return filename


#this method converts any audio or video file to wav format using pydub
def convert_to_wav(input_path: str)-> str:
    """Convert any audio or video file to WAV format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000) #16 khz
    audio.export(output_path, format="wav")
    return output_path



def chunk_audio(wav_path: str, chunk_length: int = 1)-> list:
    """Chunk a WAV audio file into smaller segments of specified length (in seconds)."""
    audio = AudioSegment.from_wav(wav_path)
    chunk_size = chunk_length * 60 * 1000  # Convert seconds to milliseconds
    chunks = []
    for i, start in enumerate(range(0, len(audio), chunk_size)):
        chunk = audio[start:start + chunk_size]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)
    return chunks

def process_audio(src: str)-> list:
    if src.startswith("http://") or src.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_yt_audio(src)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(src)
    print(f"Processing audio file: {wav_path}")
    chunks = chunk_audio(wav_path)
    print(f"Audio file has been chunked into {len(chunks)} segments.")
    return chunks

