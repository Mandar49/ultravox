import io

import numpy as np
import soundfile as sf


def speak(text: str, lang: str, sample_rate: int = 16000) -> bytes:
    """Placeholder Coqui TTS implementation returning silence."""
    duration = 1.0
    samples = np.zeros(int(sample_rate * duration), dtype=np.float32)
    buf = io.BytesIO()
    sf.write(buf, samples, sample_rate, format="wav")
    return buf.getvalue()
