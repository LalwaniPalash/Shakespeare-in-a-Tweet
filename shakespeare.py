# Shakespeare-in-a-Tweet (lossless-only)
# Modes:
#   - demo (default): compressed excerpt embedded here
#   - lossless-full : stream words from a local complete_works file (path via $SHAKES_PATH)

import os, lzma
from typing import Iterable, Iterator

# -------- Base-2048 emoji codec (11 bits/symbol) --------
BASE = 0x1F300
def _alpha(i: int) -> str: return chr(BASE + i)

def b2048_encode(data: bytes) -> str:
    out=[]; acc=0; bits=0
    for b in data:
        acc=(acc<<8)|b; bits+=8
        while bits>=11:
            out.append(_alpha((acc>>(bits-11))&2047)); bits-=11
    if bits: out.append(_alpha((acc<<(11-bits))&2047))
    return "".join(out)

def b2048_decode_stream(s: str, chunk_bytes: int = 4096) -> Iterator[bytes]:
    acc=0; bits=0; buf=bytearray()
    for ch in s:
        acc=(acc<<11)|(ord(ch)-BASE); bits+=11
        while bits>=8:
            buf.append((acc>>(bits-8))&255); bits-=8
            if len(buf)>=chunk_bytes: yield bytes(buf); buf.clear()
    if bits: buf.append((acc<<(8-bits))&255)
    if buf: yield bytes(buf)

# -------- Word splitting from streamed bytes (LZMA) --------
def _words_from_bytes(byte_chunks: Iterable[bytes]) -> Iterator[str]:
    dec = lzma.LZMADecompressor()
    tail = ""
    for chunk in byte_chunks:
        if not chunk: continue
        out = dec.decompress(chunk)
        if not out: continue
        txt = out.decode("utf-8", "replace")
        if tail: txt = tail + txt
        parts = txt.split()
        if txt and not txt[-1].isspace():
            tail = parts.pop() if parts else txt
        else:
            tail = ""
        for w in parts: yield w
    if tail:
        for w in tail.split(): yield w

# -------- Demo mode: small excerpt embedded & looped --------
_DEMO_TEXT = (
    "Shall I compare thee to a summer's day? Thou art more lovely and more temperate; "
    "Rough winds do shake the darling buds of May, and summer's lease hath all too short a date. "
    "So long lives this, and this gives life to thee. "
) * 20
_DEMO_PAYLOAD = b2048_encode(lzma.compress(_DEMO_TEXT.encode("utf-8"), preset=9))

def _demo_words() -> Iterator[str]:
    while True:
        yield from _words_from_bytes(b2048_decode_stream(_DEMO_PAYLOAD))

# -------- Lossless-full mode: stream from local file --------
def _lossless_words() -> Iterator[str]:
    path = os.getenv("SHAKES_PATH", "/usr/share/dict/shakespeare")
    while True:
        try:
            with open(path, "rb") as f:
                tail = ""
                while True:
                    b = f.read(4096)
                    if not b: break
                    txt = b.decode("utf-8", "replace")
                    if tail: txt = tail + txt
                    parts = txt.split()
                    if txt and not txt[-1].isspace():
                        tail = parts.pop() if parts else txt
                    else:
                        tail = ""
                    for w in parts: yield w
                if tail:
                    for w in tail.split(): yield w
        except FileNotFoundError:
            msg = "Set $SHAKES_PATH to a local complete_works.txt for lossless-full mode."
            for w in msg.split(): yield w

# -------- Public API --------
def stream(mode: str = "demo") -> Iterator[str]:
    m = (mode or "demo").lower()
    if m.startswith("lossless"): return _lossless_words()
    return _demo_words()