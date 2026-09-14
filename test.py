from utils.audio_processor import process_audio
from core.transcriber import transcribe_all

source = "https://www.youtube.com/watch?v=v1t4MTqdfyI&list=RDv1t4MTqdfyI&start_radio=1"

chunks = process_audio(source)

transcriptions = transcribe_all(chunks)

print(transcriptions)