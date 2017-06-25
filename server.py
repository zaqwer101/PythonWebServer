###
# На сервере висят 20 воркеров, каждый из которых ждет подключения в отдельном
# Если воркеров стало <20, создаются новые
# Воркеру передается строка, содержащая данные о клиенте, которые он парсит
# В дальнейшем он обрабатывает все запросы клиента, а при ошибке закрывает сокет и умирает
###

import threading
import socket
import time

header = b"HTTP/1.1 200 OK\r\nServer: zaqwer101\r\nContent-Type: text/html\r\n\r\n"


class Worker(threading.Thread):
    def die(self):
        self.conn.close()
        workers.remove(self)
        print("Worker погиб:" + str(self.id))

    def work(self):
        try:
            print("Worker ожидает подключения:" + str(self.id))
            self.conn, self.addr = self.s.accept()
            print("Worker принял подключение:" + str(self.id))
            self.conn.send(header + html.encode())
            time.sleep(1)
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
        self.work()


# --------------------------------------------------------------------------------------------------------------------


workers = []    # Массив обработчиков
port = 8556     # Порт сервера
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Создание сокета
i = 0   # Счетчик количества рабочих
sock.bind(("", port))   # Бинд сокета к IP и порту
sock.listen(1000)       # Указать сокету слушать до 1000 подключений одновременно

work_file = open('index.html') # Открыть и обработать
html = work_file.read()        # файл с сайтом

##
# Бесконечный цикл работы сервера. Если рабочих < 20 - создает новых
# Все рабочие хранятся в списке workers
##
while True:
    if len(workers) < 20:
        worker = Worker(sock, i, html) # Рабочему передается сокет, порядковый номер и контент, который он отдает
                                       # клиентам
        worker.start()
        workers.append(worker)
        i = i + 1
