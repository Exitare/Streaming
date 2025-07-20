import subprocess
import threading
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

server_process = None

def start_server():
    global server_process
    server_process = subprocess.Popen(["hypercorn", "app:app", "--bind", "0.0.0.0:8000"])

def restart_server():
    global server_process
    if server_process:
        server_process.terminate()
        server_process.wait()
    start_server()

class ReloadHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.src_path.endswith(('.html', '.css', '.js', '.py')):
            print(f"Change detected in {event.src_path}, restarting server...")
            restart_server()

if __name__ == "__main__":
    print("Starting reload watcher...")
    observer = Observer()
    handler = ReloadHandler()
    observer.schedule(handler, path=".", recursive=True)
    observer.start()

    start_server()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if server_process:
            server_process.terminate()
            server_process.wait()
    observer.join()