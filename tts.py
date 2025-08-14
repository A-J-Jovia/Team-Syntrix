from __future__ import annotations
import os
import io
import json
import tempfile
from pathlib import Path
from typing import Optional
import requests
from pydub import AudioSegment, effects
from dotenv import load_dotenv
from num2words import num2words
from transformers import VitsModel, AutoTokenizer
import torch
import scipy
import re

try:
    import pyttsx3
    _HAS_PYTTXS3 = True
except Exception:
    _HAS_PYTTXS3 = False

# -------- Global Caches for Hugging Face model --------
HF_TOKENIZER = None
HF_MODEL = None
HF_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# -------- Config & helpers --------
_TARGET_SR = 16000
_MAX_CHARS = 6000

HF_VOICE_MAP = {
    "VoiceA": "eng"
}

def _normalize_to_mp3(seg: AudioSegment, out_path: Path) -> Path:
    """Normalize, convert to mono + target SR, export to MP3."""
    seg = seg.set_channels(1).set_frame_rate(_TARGET_SR)
    seg = effects.normalize(seg)
    out_path = out_path.with_suffix(".mp3")
    seg.export(out_path.as_posix(), format="mp3")
    return out_path

# -------- Text Pre-processing --------
def preprocess_text(text: str) -> str:
    """
    Cleans and normalizes text, including numbers, for better TTS pronunciation.
    """
    text = re.sub(r'(\d+)', lambda x: num2words(int(x.group(1))), text)
    text = text.replace('St.', 'Street')
    text = text.replace('Mr.', 'Mister')
    text = text.replace('Dr.', 'Doctor')
    text = text.replace('&', ' and ')
    text = ' '.join(text.split())
    return text

# -------- Hugging Face TTS --------
def synthesize_hf(text: str) -> Optional[Path]:
    global HF_TOKENIZER, HF_MODEL
    
    try:
        if HF_TOKENIZER is None:
            print("Loading Hugging Face VITS model for the first time. This may take a moment...")
            HF_MODEL = VitsModel.from_pretrained("facebook/mms-tts-eng").to(HF_DEVICE)
            HF_TOKENIZER = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")

        inputs = HF_TOKENIZER(text=text, return_tensors="pt")
        inputs = inputs.to(HF_DEVICE)
        
        with torch.no_grad():
            outputs = HF_MODEL(**inputs).waveform
        
        wav_path = Path(tempfile.gettempdir()) / f"mms_speech_{os.getpid()}.wav"
        scipy.io.wavfile.write(wav_path, rate=HF_MODEL.config.sampling_rate, data=outputs.cpu().numpy().squeeze())

        return wav_path

    except Exception as e:
        print(f"Hugging Face TTS failed: {e}")
        return None

# -------- Fallback (pyttsx3 offline) --------
def _fallback_pyttsx3_to_mp3(text: str, voice_label: str, rate_factor: float = 1.0) -> Optional[Path]:
    if not _HAS_PYTTXS3:
        return None

    try:
        engine = pyttsx3.init()
        
        voices = engine.getProperty('voices')
        if "VoiceA" in voice_label and len(voices) > 0:
            engine.setProperty('voice', voices[0].id)
        elif "VoiceB" in voice_label and len(voices) > 1:
            engine.setProperty('voice', voices[1].id)
        
        base_rate = engine.getProperty("rate") or 180
        engine.setProperty("rate", int(base_rate * max(0.6, min(rate_factor, 1.6))))

        with tempfile.TemporaryDirectory() as tmpd:
            wav_path = Path(tmpd) / "speech.wav"
            engine.save_to_file(text, wav_path.as_posix())
            engine.runAndWait()

            seg = AudioSegment.from_wav(wav_path.as_posix())
            out_path = Path(tmpd) / "speech.mp3"
            out_mp3 = _normalize_to_mp3(seg, out_path)

            outputs = Path("outputs")
            outputs.mkdir(parents=True, exist_ok=True)
            final = outputs / "echoverse_tts.mp3"
            AudioSegment.from_file(out_mp3.as_posix()).export(final.as_posix(), format="mp3")
            return final
    except Exception as e:
        print(f"pyttsx3 fallback failed: {e}")
        return None

# -------- Public API --------
def synthesize(
    text: str,
    voice_label: str = "VoiceA",
    rate_factor: float = 1.0,
) -> str:
    """
    Main entry point used by the app.
    Prioritizes Hugging Face, then falls back to offline TTS.
    """
    text = (text or "").strip()
    if not text:
        raise ValueError("No text provided for TTS.")
    if len(text) > _MAX_CHARS:
        text = text[:_MAX_CHARS] + " …"
    
    preprocessed_text = preprocess_text(text)
    
    outputs = Path("outputs")
    outputs.mkdir(parents=True, exist_ok=True)
    final_path = outputs / "echoverse_tts.mp3"

    hf_path = synthesize_hf(preprocessed_text)
    if hf_path and hf_path.is_file():
        try:
            seg = AudioSegment.from_wav(hf_path.as_posix())
            _normalize_to_mp3(seg, final_path)
            os.remove(hf_path)
            return final_path.as_posix()
        except Exception:
            pass
            
    print("Hugging Face failed or was not available, using offline fallback.")
    mp3_path = _fallback_pyttsx3_to_mp3(preprocessed_text, voice_label=voice_label, rate_factor=rate_factor)
    if mp3_path:
        return mp3_path.as_posix()

    try:
        silence = AudioSegment.silent(duration=1500)
        _normalize_to_mp3(silence, final_path)
        return final_path.as_posix()
    except Exception as e:
        raise RuntimeError(f"TTS failed, and silent fallback failed: {e}")