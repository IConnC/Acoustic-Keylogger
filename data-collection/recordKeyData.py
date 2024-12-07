import os
import keyboard
import datetime
import time

keys_down = []

recorded_data = []

cases = ['Rctrl', 'p', 'esc', 'g', 'slash', 'down', '7', 'equal', 'w', 'a', 'dash', 'caps', 'l', 'd', 'backspace', 'bracketclose', 'z', '1', 'Rshift', 'comma', 'c', 'tab', 'b', 'j', 'right', 'Lctrl', 'n', 't', 'f', 'm', 'o', 'apostrophe', 'y', '8', 'space', 'backslash', 's', '9', 'i', 'r', 'bracketopen', 'semicolon', 'q', '5', 'k', '3', 'x', '4', '6', '2', 'Lshift', 'left', 'backtick', 'enter', 'fullstop', 'e', '0', 'h', 'v', 'up', 'u', 'delete']
mapped_cases = ['right ctrl', 'p', 'esc', 'g', '/', 'down', '7', '=', 'w', 'a', '-', 'caps lock', 'l', 'd', 'backspace', ']', 'z', '1', 'right shift', ',', 'c', 'tab', 'b', 'j', 'right', 'ctrl', 'n', 't', 'f', 'm', 'o', '\'', 'y', '8', 'space', '\\', 's', '9', 'i', 'r', '[', ';', 'q', '5', 'k', '3', 'x', '4', '6', '2', 'shift', 'left', '`', 'enter', '.', 'e', '0', 'h', 'v', 'up', 'u', 'delete']

def on_event(key):
    actual_key = key.name.lower()
    if key.event_type == "down" and actual_key not in keys_down:
        if actual_key in mapped_cases:
            print(actual_key)
            print(datetime.datetime.fromtimestamp(key.time))
            keys_down.append(actual_key)
            recorded_data.append({"keypress": cases[mapped_cases.index(actual_key)], "time": key.time})
            
    if key.event_type == "up" and actual_key in mapped_cases:
        try:
            keys_down.remove(actual_key)
        except:
            print("Key cannot be removed from keys down: ", actual_key)

keyboard.hook(on_event)

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/output-meta/"

if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

try:
    while True:
        time.sleep(5)
        # print(recorded_data)
        # print(len(recorded_data))
except KeyboardInterrupt:
    keyboard.unhook(on_event)
    dt = datetime.datetime.now()
    filename = f"{OUTPUT_DIR}{dt.date()}-{dt.timestamp()}.txt"
    with open(filename, "w") as file:
        for entry in recorded_data:
            file.write(f"{entry["keypress"]},{entry["time"]}\n")
    print(f"Wrote to file: {filename}")