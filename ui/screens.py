"""Entry point: build main window and launch Survival mode."""
from pathlib import Path
import customtkinter as ctk

import ui.screens_utils as utils
from ui.survival_mode import survival_mode

def start_app() -> None:
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    utils.app = ctk.CTk()
    utils.app.title("Modern App UI")
    utils.app.geometry("1250x550")
    utils.app.configure(fg_color="#eedaf0")

    vocab_path = Path(__file__).parent.parent / "data" / "Verbs.JSON"
    survival_mode(vocab_path)

    utils.app.mainloop()

if __name__ == "__main__":
    start_app()
