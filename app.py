import pickle

import pyxel
import socket


class Piece:
    def __init__(self):
        self.x = 30
        self.y = 30
        self.state = 0
        self.f_count = 0

    def update(self):
        if pyxel.frame_count - self.f_count == 30:
            self.state += 8
            if self.state > 32:
                self.state = 0
            self.f_count = pyxel.frame_count


    def draw(self):
        pyxel.blt(self.x, self.y, 0, 48 + self.state, 200, 8, 8)


class Client:
    def __init__(self, pseudo):
        self.pseudo = pseudo
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect(("127.0.0.1", 3489))
        self.send_text(f"/handshake f{self.pseudo}")
        print(self.recv_text())

    def send_object(self, data):
        self.sock.send(pickle.dumps(data))

    def send_text(self, text: str):
        self.sock.send(text.encode('utf-8'))

    def recv_object(self):
        data = self.sock.recv(1024)
        if not data:
            return None
        return pickle.loads(data)

    def recv_text(self):
        return self.sock.recv(1024).decode('utf-8')

class Ecran:
    def __init__(self, question):
        self.question = question
        self.ask = False
        self.keys = {pyxel.KEY_A: "a", pyxel.KEY_B: "b", pyxel.KEY_C: "c", pyxel.KEY_D: "d", pyxel.KEY_E: "e", pyxel.KEY_F: "f", pyxel.KEY_G: "g", pyxel.KEY_H: "h", pyxel.KEY_I: "i", pyxel.KEY_J: "j", pyxel.KEY_K: "k", pyxel.KEY_L: "l", pyxel.KEY_M: "m", pyxel.KEY_N: "n", pyxel.KEY_O: "o", pyxel.KEY_P: "p", pyxel.KEY_Q: "q", pyxel.KEY_R: "r", pyxel.KEY_S:" s", pyxel.KEY_T: "t", pyxel.KEY_U: "u", pyxel.KEY_V: "v", pyxel.KEY_W:" w", pyxel.KEY_X: "x", pyxel.KEY_Y: "y", pyxel.KEY_Z: "z"}
        self.answer = ""

    def update(self):
        if not self.ask:
            return None
        for key, value in self.keys.items():
            if pyxel.btnp(key):
                self.answer += value

        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.ask = False


    def draw(self):
        if not self.ask:
            return None
        pyxel.text(0, 0, self.question, 2)
        pyxel.text(0, 20, self.answer, 2)

class App:
    def __init__(self):
        pyxel.init(128, 128, title="Pong", fps=60)
        pyxel.load("2.pyxres")
        self.pseudo = Ecran("pseudo")
        self.client = Client("timtonix")
        self.client.connect()
        self.piece = Piece()
        pyxel.run(self.update, self.draw)

    def update(self):
        self.pseudo.update()
        self.piece.update()

    def draw(self):
        self.pseudo.draw()
        self.piece.draw()


App()