import random
import socketserver
from Crypto.Util import number
import os

flag = os.environ.get('flag', 'flag{test_flag}')
class EncryptHandler(socketserver.BaseRequestHandler):

    p = 1543
    iv = 792

    def encrypt(self, m: list):
        self.r1.seed(self.r1_key)
        self.r2.seed(self.r2_key)
        res = []
        w = self.iv
        for i in m:
            w = ((i + w + self.r1.randrange(0, self.p)) % self.p) * self.r2.randrange(0, self.p) % self.p
            res.append(w)
            w ^= self.random_key
        return res

    def setup(self):
        self.random_key = random.randrange(0, self.p)
        self.r1_key = random.randrange(0, self.p)
        self.r2_key = random.randrange(0, self.p)
        self.r1 = random.Random()
        self.r2 = random.Random()
        self.enc_flag = self.encrypt(list(flag.encode()))

    def handle(self):
        hello_msg = ('Hello, here gives you the encrypted Flag:\n'
        '{}\n'
        'You can type any msg, and I will give you the encrypted message\n'
        ).format(self.enc_flag)
        self.request.sendall(hello_msg.encode())
        while True:
            msg = self.request.recv(1024)[:-1]
            self.request.sendall((str(self.encrypt(msg)) + '\n').encode())


if __name__ == '__main__':
    HOST, PORT = '0.0.0.0', 12001
    with socketserver.ThreadingTCPServer((HOST, PORT), EncryptHandler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()
