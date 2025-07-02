# Asha Ultravox Notes

## Repository Map
- **README.md** – project overview, installation, and training instructions.
- **LICENSE** – MIT license.
- **pyproject.toml** – Poetry configuration with Python dependencies.
- **Justfile** – helper commands for formatting, tests, training, etc.
- **docs/** – architecture diagrams and marketing assets.
- **scripts/** – shell scripts for dataset creation and development utilities.
- **ultravox/** – Python package containing all source code:
  - `assets/` – tokenizers and model files.
  - `data/` – dataset definitions, loaders, and text processing utilities.
  - `evaluation/` – evaluation harness and GPT-based scoring.
  - `inference/` – local/remote inference classes and helpers.
  - `model/` – Ultravox model definition and configuration.
  - `tools/` – demos, dataset tooling, and TTS helpers.
  - `training/` – training loop and config files.
  - `utils/` – device helpers and monkey patches.

Primary language is **Python**. The project uses **Poetry** for dependency
management and includes `mcloud_*` YAML files for running jobs on MosaicML.

## Feature & Architecture Digest
- **Audio-to-text LLM** – Ultravox converts audio directly into LLM embeddings,
  bypassing a separate ASR step. It currently outputs streaming text only
  (`README` lines 24‑31).
- **Dataset registry** – numerous language datasets (e.g., English and Hindi)
  are defined under `ultravox/data/configs` and registered via
  `data/registry.py` (English example lines 10‑15 in
  `commonvoice.py`; Hindi example lines 134‑146).
- **Training pipeline** – `ultravox/training/train.py` orchestrates adapter
  training with configs like `training/configs/release_config.yaml`.
- **Inference stack** – `UltravoxInference` (in
  `inference/ultravox_infer.py`) wraps the model and processor for streaming
  inference and supports conversation history.
- **Interactive demos** – `tools/gradio_voice.py` provides a microphone-based
  demo, while `ds_tool/tts.py` includes Azure and ElevenLabs TTS clients.
- **External services** – uses Hugging Face Hub, Weights & Biases, GCP
  streaming datasets (`datasets.py` lines 16‑23), optional OpenAI inference,
  and Twilio TURN credentials for WebRTC.

## Gap / Fit Analysis for "Asha"
| Requirement | Current Status | Needed Changes (files) |
|-------------|----------------|------------------------|
| GPT‑4o‑mini dialog model | Inference defaults to open Llama models; `tools/infer_api.py` supports OpenAI endpoints but not used by demos. | Configure `UltravoxInference` or API wrapper to call GPT‑4o‑mini via `infer_api.py`. |
| ElevenLabs "Prem" voice with Coqui fallback | `tools/ds_tool/tts.py` implements ElevenLabs and Azure clients but no Coqui support. | Extend `tts.py` with Coqui client and specify "Prem" voice in config. |
| Hinglish + hi / en‑IN / gu / ta / te / mr datasets | Only Hindi and general English configs exist (`commonvoice.py`). | Create new dataset configs and register them in `data/registry.py`. |
| Web-only SSE streaming | Current demos use Gradio WebRTC; no SSE server implementation. | Add FastAPI/Starlette SSE endpoint and integrate with web UI. |
| Session memory & React dashboard | Conversation mode exists in `inference` and Gradio demo, but no React dashboard. | Build React frontend and connect via API for session state. |
| ≤200 ms TTFB | Not explicitly optimized; depends on model size and server setup. | Profiling and runtime tuning required (e.g., smaller model, caching). |

Estimated times and owners should be assigned based on team capacity.

