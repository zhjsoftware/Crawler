__author__ = 'jing'

import threading
import time


class MyThread(threading.Thread):

    def run(self):
        global num
        time.sleep(1)

        if mutex.acquire(1):
            num += 1
            msg = self.name + ' set num to: ' + str(num)
            print msg
            mutex.release()


num = 0
mutex = threading.Lock()


def test():
    for i in range(0, 5):
        thread = MyThread()
        thread.start()

if __name__ == '__main__':
    test()
    print threading.activeCount()