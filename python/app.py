import os
import signal
import sys
import time
from datetime import datetime
from pathlib import Path

VOLUME_PATH = Path(os.environ.get("VOLUME_PATH", "/mnt/hexon-data"))
running = True

def handle_stop(signum, frame):
    global running
    running = False

signal.signal(signal.SIGTERM, handle_stop)
signal.signal(signal.SIGINT, handle_stop)

def create_startup_file():
    now = datetime.now().astimezone()
    filename = f"worker-{now.strftime('%Y%m%d-%H%M%S')}.txt"
    file_path = VOLUME_PATH / filename
    VOLUME_PATH.mkdir(parents=True, exist_ok=True)
    file_path.write_text(f"Worker iniciado em: {now.isoformat()}\n", encoding="utf-8")
    print(f"[worker] Arquivo criado: {file_path}", flush=True)

if __name__ == "__main__":
    create_startup_file()
    while running:
        time.sleep(5)
