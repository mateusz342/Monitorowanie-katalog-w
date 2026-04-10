import time
import sys
from pathlib import Path
from datetime import datetime
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

class MyEventHandler(FileSystemEventHandler):
	def on_any_event(self, event: FileSystemEvent) -> None:
		now = datetime.now().strftime("%H:%M:%S")
		print(f"[{now}] {event.src_path} - {event.event_type}")

def main():
    if len(sys.argv) != 2:
        sys.exit("usage: 5-1.py <path>")
    path = Path(sys.argv[1])
    if not path.exists():
        sys.exit(f"Ścieżka nie istnieje: {path}")
    if not path.is_dir():
        sys.exit(f"Podana ścieżka nie jest katalogiem: {path}")

    print(f"Obserwuję katalog: {path.resolve()}")
    event_handler = MyEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
    	while True:
        	time.sleep(1)
    except KeyboardInterrupt:
    	print("\nZatrzymano.")
    finally:
    	observer.stop()
    	observer.join()

if __name__ == "__main__":
    main()