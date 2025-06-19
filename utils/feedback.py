import time
import random
from pathlib import Path
import pygame

import ui.screens_utils as utils

PROJECT_ROOT = Path(__file__).parent.parent

def vibrate_window(duration=300, interval=20, intensity=8):
    if not (hasattr(utils, "app") and utils.app.winfo_exists() and utils.app.winfo_ismapped()):
        return
    x0, y0 = utils.app.winfo_x(), utils.app.winfo_y()
    end = time.time() + duration / 1000
    while time.time() < end and utils.app.winfo_exists():
        dx, dy = (random.randint(-intensity, intensity) for _ in range(2))
        utils.app.geometry(f"+{x0+dx}+{y0+dy}")
        utils.app.update_idletasks()
        time.sleep(interval / 1000)
    if utils.app.winfo_exists():
        utils.app.geometry(f"+{x0}+{y0}")

def reproducir_sonido(fn: str):
    path = PROJECT_ROOT / "assets" / "sounds" / fn
    if not pygame.mixer.get_init() or not path.exists():
        return
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Sound error: {e}")
