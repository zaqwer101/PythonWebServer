###
# На сервере висят 20 воркеров, каждый из которых ждет подключения в отдельном
# Если воркеров стало <20, создаются новые
# Воркеру передается строка, содержащая данные о клиенте, которые он парсит
# В дальнейшем он обрабатывает все запросы клиента, а при ошибке закрывает сокет и умирает
###

import threading
import socket

import time


class Worker(threading.Thread):

    def die(self):
        self.conn.close()
        workers.remove(self)
        print("Worker убит: " + str(self.id))
        # print("-----------------------------------------------------------------------------------------------")

    def work(self):
        try:
            self.conn, self.addr = self.s.accept()
            self.conn.send(b"HTTP/1.1 200 OK\r\nServer: zaqwer101\r\nContent-Type: text/html\r\n\r\n")
            # self.conn.send("Content-Type: text/html".encode())
            print("Worker принял подключение: " + str(self.id))
            self.conn.send(html.encode())
            self.i = self.i + 1

            self.die()
        except Exception as e:
            print(e)
            self.die()

    def __init__(self, s, _id, html):
        self.html = html
        self.id = _id
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.i = 0
        self.s = s

    def run(self):
        print("Worker ожидает подключения: " + str(self.id))
        self.work()


# --------------------------------------------------------------------------------------------------------------------


workers = []
port = 8556
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
i = 0
sock.bind(("", port))
sock.listen(1000)

work_file = open('index.html')

html = work_file.read()

while True :
    if len(workers) < 3:
        worker = Worker(sock, i, html)
        worker.start()
        workers.append(worker)
        i = i + 1
        # print("Worker начал работу!:" + str(worker.id))

