from threading import Thread
from queue import Queue
import time


class KafkaMsgReader(Thread):
    def __init__(self, name=None, server=None, topic=None, queue=None):
        Thread.__init__(self)
        self.server = server
        self.topic = topic
        self.queue = queue

    def run(self):
        i = 0
        while True:
            time.sleep(1)
            self.queue.put((self.name, i))
            i += 1


if __name__ == "__main__":
    msg_queue = Queue(2)
    reader1 = KafkaMsgReader(name="global", queue=msg_queue)
    reader2 = KafkaMsgReader(name="local", queue=msg_queue)
    reader1.start()
    reader2.start()

    while True:
        msg = msg_queue.get()
        print(msg)
