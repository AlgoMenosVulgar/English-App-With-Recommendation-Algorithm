"""Shared state & helper utilities for every screen."""
from __future__ import annotations
import customtkinter as ctk

# ─── RUNTIME-SINGLETONS ─────────────────────────────────────────────
app: ctk.CTk | None = None               # set in ui/screens.py
menu_window: ctk.CTkToplevel | None = None

# per-user globals
current_user: str = ""
VOCAB_FILES: dict[str, str] = {}

# ─── BASIC HELPERS ──────────────────────────────────────────────────
def clear_screen() -> None:
    """Destroy all widgets in the root window and close any burger-menu."""
    global menu_window
    if menu_window and menu_window.winfo_exists():
        menu_window.destroy()
        menu_window = None
    if app is None:
        return
    for child in app.winfo_children():
        child.destroy()
    app.bind("<Button-1>", lambda _e: None)

# ─── COLOUR UTILITIES ───────────────────────────────────────────────
_GRADIENT_RED  = "#dc3545"
_GRADIENT_GREEN = "#28a745"

def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def _rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def weight_to_color(weight: float) -> str:
    """0.1 → red, 1.0 → green."""
    weight = max(0.1, min(1.0, weight))
    t      = (weight - 0.1) / 0.9
    r0, g0, b0 = _hex_to_rgb(_GRADIENT_RED)
    r1, g1, b1 = _hex_to_rgb(_GRADIENT_GREEN)
    r = int(r0 * (1 - t) + r1 * t)
    g = int(g0 * (1 - t) + g1 * t)
    b = int(b0 * (1 - t) + b1 * t)
    return _rgb_to_hex((r, g, b))
