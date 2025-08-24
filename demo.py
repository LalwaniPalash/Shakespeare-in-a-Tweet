import os, sys, time
from shakespeare import stream

mode = sys.argv[1] if len(sys.argv) > 1 else os.getenv("MODE", "demo")
wpm = int(sys.argv[2]) if len(sys.argv) > 2 else int(os.getenv("WPM", 60))
delay = 60.0 / wpm

def main():
    g = stream(mode)
    write, flush = sys.stdout.write, sys.stdout.flush
    try:
        while True:
            write(next(g) + " ")
            flush()
            time.sleep(delay)
    except (KeyboardInterrupt, BrokenPipeError):
        pass

if __name__ == "__main__":
    main()