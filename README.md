# Shakespeare-in-a-Tweet

A tiny Python program that streams Shakespeare forever from a single "tweet-sized" script — no temp files, no network (in demo), and tiny RAM.

> ⚖️ **Honesty note:** Squeezing the *complete works* (≈ 5.4 MB) into ≈ 2.5 kB losslessly is physically impossible for general English text (lower bound ≈ 2.3 bits/char → ≈ 1.5 MB).
> This repo is truthful and ships two modes:
> 	•	demo — runs out of the box (small excerpt, embedded)
> 	•	lossless-full — streams from a local complete_works.txt you provide (no network while running)

## Repo

`https://github.com/LalwaniPalash/Shakespeare-in-a-Tweet`

| File | Size | Purpose |
|------|------|----------|
| tweet.py | ≤ 280 chars | One-liner runner (streams words at a fixed WPM) |
| shakespeare.py | ~2–3 KB | Demo payload, base-2048 emoji codec, lossless streamer |
| demo.py | ≤ 20 lines | Optional CLI wrapper with MODE/WPM args |

## Quick start

```bash
git clone https://github.com/LalwaniPalash/Shakespeare-in-a-Tweet.git
cd Shakespeare-in-a-Tweet

# Run the out-of-the-box demo mode
python3 tweet.py
```

You'll see lines of Shakespeare (excerpt) scroll by at ~60 wpm, forever.

## Modes

Switch modes with the MODE env var or pass a mode to demo.py.

### 1) demo (default)

Small excerpt, compressed and embedded so it runs immediately.

```bash
python3 tweet.py
# or
MODE=demo python3 tweet.py
```

### 2) lossless-full (local complete works, no network)

Streams your local plain-text corpus in small chunks (never loads it all into RAM).

```bash
# Get the text (Project Gutenberg "Complete Works")
curl -L https://www.gutenberg.org/ebooks/100.txt.utf-8 -o complete_works.txt

# Optional: strip Gutenberg header/footer
sed -n '/^\*\*\* START OF/,/^\*\*\* END OF/p' complete_works.txt > clean_works.txt

# Stream it
export MODE=lossless-full
export SHAKES_PATH="$PWD/clean_works.txt"   # or complete_works.txt
python3 tweet.py
```

#### Windows (PowerShell)

```powershell
iwr https://www.gutenberg.org/ebooks/100.txt.utf-8 -OutFile complete_works.txt
$in = Get-Content .\complete_works.txt
$start = ($in | Select-String '^\*\*\* START OF').LineNumber
$end   = ($in | Select-String '^\*\*\* END OF').LineNumber
if ($start -and $end) { $in[($start-1)..($end-1)] | Set-Content clean_works.txt }
$env:MODE="lossless-full"; $env:SHAKES_PATH="$PWD\clean_works.txt"
python3 tweet.py
```

## Control the speed (WPM)

tweet.py is tweet-sized and supports WPM via env var; demo.py also accepts CLI args.

```bash
# Env var (any platform)
WPM=120 python3 tweet.py

# Windows PowerShell
$env:WPM=150; python3 tweet.py

# CLI with demo.py (mode, WPM)
python3 demo.py lossless-full 200
```

## Piping & fun stuff

• **Color:**

```bash
python3 tweet.py | lolcat
```

• **Spoken Bard:**

```bash
python3 tweet.py | espeak-ng
```

• **Make a GIF of your terminal output:**
gifski can't read raw text from stdin. Record first, then render:

```bash
# macOS/Homebrew
brew install asciinema agg
asciinema rec -c 'WPM=200 python3 tweet.py' cast.cast
agg cast.cast shakespeare.gif
```

## Clean exits (no tracebacks)

If you press Ctrl-C or close the pipe (e.g., | head), the included tweet.py variant exits quietly:

```python
import sys,os,time as t;from shakespeare import stream
w=sys.stdout.write;f=sys.stdout.flush;g=stream(os.getenv("MODE","demo"));d=60/float(os.getenv("WPM",60))
try:
 while 1:w(next(g)+" ");f();t.sleep(d)
except(KeyboardInterrupt,BrokenPipeError):pass
```

## How it works

• **Streaming only:** emits one word at a time; never holds the full corpus.
• **Demo compression:** lzma packs a short excerpt; a base-2048 emoji codec embeds/decodes it.
• **Lossless-full:** reads your local file in small byte chunks, splits to words, and loops forever.

## Development

• Python 3.7+
• No external Python deps.
• Optional tools:
  • espeak-ng, lolcat
  • asciinema, agg (record terminal → GIF)

Run locally:

```bash
python3 -m pip install --upgrade pip
python3 tweet.py
```

## License

MIT — copy the tweet, share the Bard.

