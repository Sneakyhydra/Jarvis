from pynput import keyboard
import pystray
from PIL import Image
from pystray import Menu, MenuItem
import os
import Jarvis
import speech_recognition as sr
import win32.win32gui as win32gui
import win32.lib.win32con as win32con

global r
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Please wait. Calibrating microphone...")
    # listen for 5 seconds and calculate the ambient noise energy level
    r.adjust_for_ambient_noise(source, duration=5)
    print("Calibrated")

# Hide the window
window = win32gui.GetForegroundWindow()
win32gui.ShowWindow(window, win32con.SW_HIDE)

# Paths
common_path = os.path.dirname(os.path.abspath(__file__))
startingAssistant_icon_path = common_path + "\\StartingAssistant.jpg"
jarvis_path = common_path + "\\Jarvis.py"


def exit_action(icon):
    icon.visible = False
    os._exit(0)


# System tray icon
startingAssistant_image = Image.open(startingAssistant_icon_path)
startingAssistant_icon = pystray.Icon("Listening")
startingAssistant_icon.menu = Menu(
    MenuItem("Exit", lambda: exit_action(startingAssistant_icon)),)
startingAssistant_icon.icon = startingAssistant_image
startingAssistant_icon.title = "Starting Assistant"


global vkeyboard
vkeyboard = keyboard.Controller()


def execute():
    vkeyboard.release(keyboard.Key.ctrl)
    vkeyboard.release(keyboard.Key.alt)
    vkeyboard.release(keyboard.Key.shift)

    Jarvis.main(r.energy_threshold)


def setup(icon):
    icon.visible = True

    def for_canonical(f):
        return lambda k: f(l.canonical(k))

    hotkey = keyboard.HotKey(
        keyboard.HotKey.parse('<ctrl>+<alt>+<shift>'),
        execute)

    with keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release)
    ) as l:
        l.join()


startingAssistant_icon.run(setup)
