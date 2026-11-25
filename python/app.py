import os
import signal
import sys
import time
from datetime import datetime
from pathlib import Path

# Caminho externo ao checkout; o volume é fornecido pela plataforma.
VOLUME_PATH = Path(os.environ.get("VOLUME_PATH", "/mnt/hexon-data"))

running = True


def handle_stop(signum, frame):
    global running
    running = False


signal.signal(signal.SIGTERM, handle_stop)
signal.signal(signal.SIGINT, handle_stop)


def create_startup_file():
    now = datetime.now().astimezone()

    # Cria estrutura: /mnt/hexon-data/YYYY-MM-DD/HH/worker-YYYYMMDD-HHMMSS.txt
    target_dir = VOLUME_PATH / now.strftime("%Y-%m-%d") / now.strftime("%H")
    target_dir.mkdir(parents=True, exist_ok=True)

    filename = f"worker-{now.strftime('%Y%m%d-%H%M%S')}.txt"
    file_path = target_dir / filename

    file_path.write_text(
        f"Worker iniciado em: {now.isoformat()}\n",
        encoding="utf-8",
    )
    print(f"[worker] Arquivo criado: {file_path}", flush=True)


if __name__ == "__main__":
    try:
        create_startup_file()
    except OSError as error:
        print(f"[worker] Erro ao acessar volume {VOLUME_PATH}: {error}", flush=True)
        sys.exit(1)

    print("[worker] Em execução...", flush=True)
    while running:
        time.sleep(5)

    print("[worker] Encerrado.", flush=True)
