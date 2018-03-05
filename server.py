import json
from threading import Thread
from player import mpg123Player, mpg123PlayerError


class ServerError(Exception):
    pass


class Server(object):
    """ class to control mpg123 player """
    def __init__(self, station=None):
        if station is None:
            self.url = 'http://nashe2.hostingradio.ru/ultra-128.mp3'
        else:
            self.url = json.load(open('urls', 'r'))[station]
        self.player = None
        self.isEnabled = False
        self.history = []
        self.isRunning = False
        self.current_radio_station = station


    def store_history(self, track):
        """
        store tracks history

        :param track: track name

        :return:
        """
        if len(self.history) > 4:
            self.history.pop(0)
            self.history.append(self.player.get_current_track)
        else:
            self.history.append(self.player.get_current_track)

    @property
    def get_history(self):
        return self.history

    @property
    def get_current_radio_station(self):
        return self.current_radio_station

    def run(self):
        while True:
            if not self.isEnabled and not self.isRunning:
                self.player = mpg123Player(self.history)
                self.isRunning = True
                self.player.run()
                self.player.play(self.url)
                self.history = []
            else:
                for track in self.player._read:
                    self.store_history(track)
                    continue

    @property
    def stop(self):
        """
        Stop radio

        :return: True or False

        """
        if self.player is not None:
            try:
                print('Stop command send')
                self.isEnabled = True
                self.player.stop()
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
        #self.run()

if __name__ == '__main__':
    x = Server(url='http://nashe2.hostingradio.ru/ultra-128.mp3')

    x.start
