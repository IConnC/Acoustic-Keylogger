import os
import keyboard
import datetime

keys_down = []

cases = ['Rctrl', 'p', 'esc', 'g', 'slash', 'down', '7', 'Lalt', 'equal', 'w', 'a', 'dash', 'caps', 'l', 'd', 'backspace', 'bracketclose', 'z', '1', 'end', 'Rshift', 'comma', 'c', 'fn', 'tab', 'b', 'j', 'cmd', 'right', 'Lctrl', 'n', 't', 'f', 'm', 'Ralt', 'o', 'apostrophe', 'y', '8', 'space', 'backslash', 's', '9', 'i', 'r', 'asterisk', 'bracketopen', 'semicolon', 'q', '5', 'k', '3', 'x', '4', '6', '2', 'Lshift', 'left', 'backtick', 'enter', 'fullstop', 'e', '0', 'h', 'v', 'up', 'u', 'altL', 'altR', 'lcmd', 'delete']

def on_event(key):
    if key.event_type == "down" and key.name not in keys_down:
        print('{0} pressed'.format(key))
        keys_down.append(key.name)
        # print(datetime.datetime.fromtimestamp(key.time))
    if key.event_type == "up":
        keys_down.remove(key.name)

keyboard.hook(on_event)

if not os.path.exists("./output"):
    os.mkdir("./output")

while True:
    pass