import subprocess
import socket
import json
import os
import time

SOCKET_PATH = os.path.join(
        os.environ.get("XDG_RUNTIME_DIR", "/tmp"),
        "scc-mpv.sock"
        )

class Player:
    def __init__(self):
        self.mp_proc = None

    def play(self, stream_url):
        if self.is_playing():
            self.stop()

        self.mp_proc = subprocess.Popen(["mpv", f"--input-ipc-server={SOCKET_PATH}", stream_url, "--no-video", "--terminal=no"])
        self.wait_for_socket()

    def wait_for_socket(self,timeout=5):
        start = time.time()
        while True:
            if time.time() - start > timeout:
                raise TimeoutError("mpv socket connection request timedout")
            try:
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                sock.connect(SOCKET_PATH)
                sock.close()
                return
            except:
                time.sleep(0.1)

    def stop(self):
        if self.mp_proc:
            self.mp_proc.terminate()
            try:
                self.mp_proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.mp_proc.kill()

    def is_playing(self):
        if self.mp_proc is None:
            return False
        return self.mp_proc.poll() is None

    #SOCKET COMMUNICATION
    def send_command(self, command_list):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(SOCKET_PATH)

        command = json.dumps({"command": command_list}) + "\n"
        sock.sendall(command.encode())
        response = json.loads(sock.recv(4096))
        return response

    #HELPER FUNCTIONS
    def pause(self):
        self.send_command(["set_rpoperty", "pause", True])

    def resume(self):
        self.send_command(["set_property", "pause", True])

    def get_position(self):
        response = self.send_command(["get_property", "time-pos"])
        return response.get("data", 0)

    def seek(self, position):
        #POSITION -> IN SECONDS
        try:
            response = self.send_command(["seek", position, "absolute"])
            return response.get("data", 0)
        except Exception:
            pass

    def set_volume(self, level):
        self.send_command(["set_property", "volume", level])
