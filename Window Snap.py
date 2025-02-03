import sys as system_MODULE
import threading as threading_MODULE
import keyboard as keyboard_MODULE
import pyautogui as pyAutoGui_MODULE
import tkinter as tk
from pystray import Icon, Menu, MenuItem
from PIL import Image
from screeninfo import get_monitors
from pathlib import Path

percentage_INT = 85

def exit_FUNC(icon_CON):
    keyboard_MODULE.clear_all_hotkeys()
    icon_CON.stop()
    system_MODULE.exit()

def window_FUNC(action_STRING):
    active_MONITOR = None
    mouseX_INT, mouseY_INT = pyAutoGui_MODULE.position()

    for iterating_MONITOR in get_monitors():
        if iterating_MONITOR.x <= mouseX_INT < iterating_MONITOR.x + iterating_MONITOR.width and iterating_MONITOR.y <= mouseY_INT < iterating_MONITOR.y + iterating_MONITOR.height:
            active_MONITOR = iterating_MONITOR
            break

    if active_MONITOR:
        active_WINDOW = pyAutoGui_MODULE.getActiveWindow()
        active_WINDOW.restore()

        screenX_INT, screenY_INT = active_MONITOR.width, active_MONITOR.height
        difference_INT = int(screenY_INT - (percentage_INT / 100 * screenY_INT))
        newWidth_INT, newHeight_INT = screenX_INT - difference_INT, screenY_INT - difference_INT
        windowX_INT, windowY_INT = active_MONITOR.x + (screenX_INT - newWidth_INT) // 2, active_MONITOR.y + (screenY_INT - newHeight_INT) // 2

        difference_INT = int(difference_INT / 4)

        if action_STRING == 'fullscreen':
            active_WINDOW.resizeTo(newWidth_INT, newHeight_INT)

            screenX_INT, screenY_INT = active_MONITOR.width, active_MONITOR.height
            windowX_INT, windowY_INT = active_WINDOW.width, active_WINDOW.height
            windowX_INT, windowY_INT = active_MONITOR.x + ((screenX_INT - windowX_INT) // 2), active_MONITOR.y + ((screenY_INT - windowY_INT) // 2)

            active_WINDOW.moveTo(windowX_INT, windowY_INT)
        elif action_STRING == 'left':
            active_WINDOW.resizeTo(int((newWidth_INT / 2) - difference_INT), newHeight_INT)
            active_WINDOW.moveTo(windowX_INT, windowY_INT)
        elif action_STRING == 'right':
            active_WINDOW.resizeTo(int((newWidth_INT / 2) - difference_INT), newHeight_INT)
            active_WINDOW.moveTo(windowX_INT + int((newWidth_INT / 2) + difference_INT), windowY_INT)
        elif action_STRING == 'fullscreenTwice':
            active_WINDOW.resizeTo(int(newWidth_INT / 3) - int(difference_INT / 2), newHeight_INT)
            active_WINDOW.moveTo(windowX_INT + int((newWidth_INT / 3)) + int(difference_INT / 4), windowY_INT)
        elif action_STRING == 'leftTwice':
            active_WINDOW.resizeTo(int((newWidth_INT / 3) - int(difference_INT / 2)), newHeight_INT)
            active_WINDOW.moveTo(windowX_INT, windowY_INT)
        elif action_STRING == 'rightTwice':
            active_WINDOW.resizeTo(int((newWidth_INT / 3) - int(difference_INT / 2)), newHeight_INT)
            active_WINDOW.moveTo(windowX_INT + int((newWidth_INT / 3 * 2)) + int(difference_INT / 2), windowY_INT)
        elif action_STRING == 'up':
            active_WINDOW.resizeTo(newWidth_INT, int((newHeight_INT / 2) - difference_INT))
            active_WINDOW.moveTo(windowX_INT, windowY_INT)
        elif action_STRING == 'down':
            active_WINDOW.resizeTo(newWidth_INT, int((newHeight_INT / 2) - difference_INT))
            active_WINDOW.moveTo(windowX_INT, windowY_INT + int((newHeight_INT / 2) + difference_INT))

def background_FUNC():
    def fullscreen_FUNC():
        window_FUNC('fullscreen')
        window_FUNC('fullscreen')

    def left_FUNC():
        window_FUNC('left')

    def right_FUNC():
        window_FUNC('right')

    def fullscreenTwice_FUNC():
        window_FUNC('fullscreenTwice')

    def leftTwice_FUNC():
        window_FUNC('leftTwice')

    def rightTwice_FUNC():
        window_FUNC('rightTwice')

    def up_FUNC():
        window_FUNC('up')
    
    def down_FUNC():
        window_FUNC('down')

    keyboard_MODULE.add_hotkey('windows+f', fullscreen_FUNC)
    keyboard_MODULE.add_hotkey('alt+left', left_FUNC)
    keyboard_MODULE.add_hotkey('alt+right', right_FUNC)
    keyboard_MODULE.add_hotkey('ctrl+alt+f', fullscreenTwice_FUNC)
    keyboard_MODULE.add_hotkey('ctrl+alt+left', leftTwice_FUNC)
    keyboard_MODULE.add_hotkey('ctrl+alt+right', rightTwice_FUNC)
    keyboard_MODULE.add_hotkey('alt+up', up_FUNC)
    keyboard_MODULE.add_hotkey('alt+down', down_FUNC)

def open_slider_window():
    slider_window = tk.Tk()
    slider_window.title("Adjust Percentage")

    def update_percentage_from_slider(val):
        global percentage_INT
        percentage_INT = int(float(val))
        entry_value.set(percentage_INT)

    def update_percentage_from_entry(event=None):
        global percentage_INT
        try:
            value = int(entry_value.get())
            clamped_value = max(0, min(100, value))  # Clamp the value between 0 and 100
            percentage_INT = clamped_value
            slider.set(clamped_value)  # Update the slider to match the clamped value
            entry_value.set(clamped_value)  # Ensure the entry box displays the clamped value
        except ValueError:
            entry_value.set(percentage_INT)  # Reset entry to the current percentage if input is invalid

    slider = tk.Scale(slider_window, from_=0, to=100, orient='horizontal', command=update_percentage_from_slider)
    slider.set(percentage_INT)  # Set initial value to current percentage
    slider.pack(padx=20, pady=10)

    entry_value = tk.StringVar(value=str(percentage_INT))
    entry = tk.Entry(slider_window, textvariable=entry_value)
    entry.pack(padx=20, pady=10)
    entry.bind("<Return>", update_percentage_from_entry)  # Update percentage when Enter key is pressed
    entry.bind("<FocusOut>", update_percentage_from_entry)  # Update percentage when the entry box loses focus

    slider_window.mainloop()

def icon_FUNC():
    menu_MENU = Menu(
        MenuItem("Adjust Percentage", lambda: threading_MODULE.Thread(target=open_slider_window).start()),
        MenuItem("Exit", exit_FUNC)
    )

    script_DIRECTORY = Path(system_MODULE.argv[0] if __name__ == '__main__' else __file__).resolve().parent
    icon_IMAGE = Image.open(script_DIRECTORY / "icon.ico")
    icon_ICON = Icon("Windows Snap", icon_IMAGE, "Windows Snap", menu_MENU)
    icon_ICON.run()

if __name__ == "__main__":
    threading_MODULE.Thread(target=background_FUNC, daemon=True).start()
    icon_FUNC()
