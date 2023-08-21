import os
import liveget as lg
import initial


def main():
    initial.initial()
    x = lg.LiveInfoGet(rid=34162)
    os.startfile('reader.py')
    x.living_on()


if __name__ == '__main__':
    main()
