import subprocess
import time
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed

class ServerError(Exception):
    pass

class Server(object):
    """ class to control mpg123 player """
    def __init__(self, url=None):
        if url is None:
            self.url = 'http://nashe2.hostingradio.ru/ultra-128.mp3'
        else:
            self.url = url
        self.p = None
        self.isStoped = False
        self.history = []

    def read_info(self):
        """ read meta-info """
        for line in iter(self.p.stdout.readline, b''):
            # парсер сначала
            print(line.decode())

    def add_history(self, track):
        """
        store tracks history

        :param track: track name

        :return:
        """
        if len(self.history) > 5:
            self.history.pop(0)
        else:
            self.history.append(track)

    def run(self):
        while True:
            if not self.isStoped:
                self.p = subprocess.Popen(['mpg123', '-@', self.url], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                out, err = self.p.communicate()
                time.sleep(5)
            else:
                print('Stop command received')
                break

    @property
    def stop(self):
        """
        Stop radio

        :return: True or False

        """
        if self.p is not None:
            try:
                print('Stop command send')
                self.isStoped = True
                self.p.kill()
            except Exception as err:
                raise ServerError('Cant stop radio server. {error}'.format(error=err))
            else:
                return True
        else:
            return False

    @property
    def start(self):
        th1 = Thread(target=self.run, args=())
        th1.start()
        # with ThreadPoolExecutor(max_workers=2) as pool:
        #     futures = [pool.submit(self.run(),)

if __name__ == '__main__':
    x = Server(url='http://nashe2.hostingradio.ru/ultra-128.mp3')

    x.start
    time.sleep(25)
    x.stop
