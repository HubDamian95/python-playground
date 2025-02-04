import pygetwindow as gw
import keyboard
import time
import random
import ctypes
from ctypes import wintypes

# Windows API setup
user32 = ctypes.WinDLL('user32')
SendMessage = user32.SendMessageW
GetWindowRect = user32.GetWindowRect
ClientToScreen = user32.ClientToScreen

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

# Configuration
GAME_WINDOW_TITLE = "Leaf Blower Revolution"
SWEEP_DURATION = 0.8    # Time to move across the screen (in seconds)
STEP_INTERVAL = 0.02    # Time between position updates (controls smoothness)
EXIT_KEY = 'q'

def send_mouse_event(hwnd, x, y):
    """Send mouse move event directly to window"""
    pt = POINT()
    pt.x = x
    pt.y = y
    ClientToScreen(hwnd, ctypes.byref(pt))
    l_param = pt.x | (pt.y << 16)
    SendMessage(hwnd, 0x0200, 0x0001, l_param)  

def smooth_move(hwnd, start_x, start_y, end_x, end_y, duration):
    """Smoothly move between points using linear interpolation"""
    steps = int(duration / STEP_INTERVAL)
    x_step = (end_x - start_x) / steps
    y_step = (end_y - start_y) / steps
    
    for i in range(steps):
        if exit_flag:
            return
        x = int(start_x + x_step * i)
        y = int(start_y + y_step * i)
        send_mouse_event(hwnd, x, y)
        time.sleep(STEP_INTERVAL)
    
    send_mouse_event(hwnd, end_x, end_y)

def main():
    global exit_flag
    exit_flag = False
    keyboard.on_press(lambda e: set_exit() if e.name == EXIT_KEY else None)

    try:
        game_window = gw.getWindowsWithTitle(GAME_WINDOW_TITLE)[0]
    except IndexError:
        print(f"Window '{GAME_WINDOW_TITLE}' not found!")
        return

    hwnd = game_window._hWnd
    game_window.activate()
    time.sleep(0.5)

    rect = wintypes.RECT()
    user32.GetClientRect(hwnd, ctypes.byref(rect))
    width = rect.right - rect.left
    height = rect.bottom - rect.top

    try:
        while not exit_flag:
            step_size = random.randint(150, 250)
            y = height 
            direction = 1

            while y >= 0 and not exit_flag:
                if direction == 1:
                    # Left to right sweep
                    smooth_move(hwnd, 0, y, width, y, SWEEP_DURATION)
                else:
                    # Right to left sweep
                    smooth_move(hwnd, width, y, 0, y, SWEEP_DURATION)
                
                y -= step_size
                direction *= -1
                time.sleep(0.05)

    except Exception as e:
        print(f"Error: {str(e)}")

def set_exit():
    global exit_flag
    exit_flag = True
    print("\nExit requested...")

if __name__ == "__main__":
    try:
        import keyboard
    except ImportError:
        print("Installing required keyboard module...")
        import subprocess
        subprocess.check_call(["pip", "install", "keyboard"])
        import keyboard

    main()
