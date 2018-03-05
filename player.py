import re
import subprocess
import time


class mpg123PlayerError(Exception):
    pass


class mpg123Player(object):
    """ Class to control player

    remote command help: https://github.com/georgi/mpg123/blob/master/doc/README.remote

    """

    def __init__(self, history):
        self.history = history
        self.current_track = None

    @property
    def get_current_track(self):
        return self.current_track

    def store_history(self, track):
        """
        store tracks history

        :param track: track name

        :return:
        """
        if len(self.history) > 4:
            self.history.pop(0)
            self.history.append(track)
        else:
            self.history.append(track)

    @property
    def _read(self):
        """ read from stdout """
        pattern = r"StreamTitle='(?P<artist>[\w\s]+) - (?P<song>[\w\s]+)'"
        if self.p:
            for line in iter(self.p.stdout.readline, b''):
                match = re.search(pattern, line.decode('UTF-8').strip())
                if match:
                    artist, song = match.groups()
                    # self.add_history('{artist} - {song}'.format(artist=artist, song=song))
                    self.current_track = '{artist} - {song}'.format(artist=artist, song=song)
                    yield self.current_track

    def __write(self, cmd):
        """
        Send message to console

        :param cmd: sending command
        :return:
        """
        cmd = cmd + '\n'
        try:
            self.p.stdin.write(cmd.encode())
            self.p.stdin.flush()
        except Exception as err:
            raise mpg123PlayerError("{0}: {1}".format(type(err).__name__, err))

    def run(self):
        self.p = subprocess.Popen(['mpg123', '-R'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
        print('start player')
        # time.sleep(1)

    def play(self, trackname):
        """ LOAD and start playing """
        print('play: ', trackname)
        if self.p is not None:
            self.__write('LOAD {trackname}'.format(trackname= trackname))
            return True
        else:
            return False

    def pause(self):
        """ PAUSE """
        if self.p is not None:
            self.__write('PAUSE')

    def stop(self):
        """ PAUSE """
        if self.p is not None:
            self.__write('STOP')

    def quit(self):
        """ QUIT """
        if self.p is not None:
            self.__write('QUIT')