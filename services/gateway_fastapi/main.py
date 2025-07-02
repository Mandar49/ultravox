import base64
import json
import os
import uuid
from typing import Dict, List

from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

from ultravox.data import data_sample
from ultravox.inference import base as infer_base
from ultravox.tools import infer_api
from ultravox.tools.ds_tool import tts

app = FastAPI()
_sessions: Dict[str, List[Dict[str, str]]] = {}


class StreamRequest(BaseModel):
    audio_b64: str
    lang: str
    session_id: str


def _event(data: Dict[str, str]) -> str:
    return f"data: {json.dumps(data)}\n\n"


@app.post("/stream")
async def stream(req: StreamRequest):
    history = _sessions.get(req.session_id, [])[-10:]

    sample = data_sample.VoiceSample(
        messages=history + [{"role": "user", "content": "<|audio|>"}],
        audio=base64.b64decode(req.audio_b64),
    )
    inf = infer_api.create_inference(
        os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        "gpt-4o-mini",
        os.environ.get("OPENAI_API_KEY"),
    )

    async def gen():
        text = "Hello"
        for chunk in inf.infer_stream(sample, lang=req.lang):
            if isinstance(chunk, infer_base.InferenceChunk):
                text += chunk.text
                yield _event({"role": "assistant", "text": chunk.text})
        audio_bytes = tts.speak(text, req.lang)
        fname = f"{uuid.uuid4()}.wav"
        path = f"/tmp/{fname}"
        with open(path, "wb") as f:
            f.write(audio_bytes)
        yield _event(
            {"role": "assistant", "text": text, "audio_url": f"/audio/{fname}"}
        )
        _sessions[req.session_id] = history + [{"role": "user", "content": text}]

    return StreamingResponse(gen(), media_type="text/event-stream")


@app.get("/audio/{fname}")
async def audio(fname: str):
    return FileResponse(f"/tmp/{fname}", media_type="audio/wav")
