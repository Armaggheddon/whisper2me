import ffmpeg
import numpy as np

def load_audio_from_bytes(audio_bytes, sr: int = 16000):
    """
    Custom implementation of load_audio in whisper library
    to avoid having to write the audio file to disk

    See https://github.com/openai/whisper/discussions/380#discussioncomment-3928648
    """
    
    try:
        # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
        # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.    
        out, _ = (
            ffmpeg.input("pipe:", threads=0)
            .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=sr)
            .run(cmd="ffmpeg", capture_stdout=True, capture_stderr=True, input=audio_bytes)
        )
    except ffmpeg.Error as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0