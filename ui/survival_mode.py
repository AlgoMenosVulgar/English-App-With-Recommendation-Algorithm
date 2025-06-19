"""Survival-Mode screen: builds the quiz UI and runs the loop."""
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime
import tkinter as tk
import customtkinter as ctk
from PIL import Image
import pygame
from tkinter import filedialog

import ui.screens_utils as utils
from ui.styles import (
    BUTTON_STYLE_ANSWERS, BUTTON_GRAY, SEGMENTED_BUTTON_STYLE,
    FONT_HEADER, FONT_STREAK, FONT_WORD, FONT_WEIGHT, FONT_FEEDBACK,
    COLOR_CARD, COLOR_LEFT_BG, COLOR_RIGHT_BG,
)
from utils.file_io  import guardar_resultado_json, save_data_to_json, load_vocabulary
from utils.feedback import vibrate_window, reproducir_sonido
from utils.recommendation_algorithm import seleccionar_siguiente

PROJECT_ROOT_PATH   = Path(__file__).parent.parent
FEEDBACK_DELAY_MS   = 2000
SOUND_FILE_CORRECT  = "Correct.mp3"
SOUND_FILE_INCORRECT= "Incorrect.mp3"
IMAGE_DISPLAY_SIZE  = (180, 180)

current_vocab_path: Path | None = None
streak_counter: int = 0

# ─── HELPERS ────────────────────────────────────────────────────────
def import_vocabulary_json() -> None:
    """Pick a JSON list and reload the screen."""
    global current_vocab_path
    sel = filedialog.askopenfilename(
        title="Select Vocabulary JSON", filetypes=[("JSON", "*.json")]
    )
    if sel:
        current_vocab_path = Path(sel)
        utils.clear_screen()
        survival_mode(current_vocab_path)

def load_ctk_image(path: Path, *, size: tuple[int, int]) -> ctk.CTkImage:
    img = Image.open(path)
    return ctk.CTkImage(light_image=img, dark_image=img, size=size)

# ─── IMAGE ASSETS ───────────────────────────────────────────────────
ctk_image_happy  = load_ctk_image(PROJECT_ROOT_PATH / "assets/images/snoopy_happy.png",
                                  size=IMAGE_DISPLAY_SIZE)
ctk_image_sad    = load_ctk_image(PROJECT_ROOT_PATH / "assets/images/snoopy_sad.png",
                                  size=IMAGE_DISPLAY_SIZE)
ctk_image_empty  = ctk.CTkImage(light_image=Image.new("RGBA", (1, 1), (0, 0, 0, 0)),
                                dark_image =Image.new("RGBA", (1, 1), (0, 0, 0, 0)),
                                size=(1, 1))

# ─── UI BUILDERS (panels, buttons) ──────────────────────────────────
def make_resume_button(parent: ctk.CTkFrame, text: str) -> ctk.CTkButton:
    return ctk.CTkButton(parent, text=text, **BUTTON_GRAY)

def make_answer_button(parent: ctk.CTkFrame, text: str, cmd) -> ctk.CTkButton:
    return ctk.CTkButton(parent, text=text, command=cmd, **BUTTON_STYLE_ANSWERS)

def build_config_panel(parent: ctk.CTkFrame) -> ctk.CTkSegmentedButton:
    ctk.CTkLabel(parent, text="Configuration Panel", font=FONT_HEADER
                 ).pack(pady=(20, 10), padx=20)
    ctk.CTkButton(parent, text="Import List", command=import_vocabulary_json,
                  **BUTTON_GRAY).pack(pady=10, padx=20, fill="x")
    ctk.CTkLabel(parent, text="Difficulty Mode:", font=FONT_HEADER
                 ).pack(pady=(5, 0), padx=20, anchor="w")
    selector = ctk.CTkSegmentedButton(parent,
                                      values=["Random", "AI Mode", "Hard"],
                                      **SEGMENTED_BUTTON_STYLE)
    selector.set("AI Mode")
    selector.pack(pady=0, padx=20, fill="x")
    return selector

def build_quiz_area(parent: ctk.CTkFrame) -> dict[str, ctk.CTkBaseClass]:
    card = ctk.CTkFrame(parent, fg_color=COLOR_CARD, corner_radius=20,
                        width=900, height=600)
    card.pack(pady=20, padx=20)
    card.pack_propagate(False)

    lbl_streak   = ctk.CTkLabel(card, text="Streak: 0", font=FONT_STREAK)
    lbl_wordbox  = ctk.CTkFrame(card, fg_color="transparent")
    lbl_word     = ctk.CTkLabel(lbl_wordbox, text="", font=FONT_WORD)
    lbl_weight   = ctk.CTkLabel(lbl_wordbox, text="", font=FONT_WEIGHT,
                                text_color="gray")
    feed_box     = ctk.CTkFrame(card, fg_color="transparent")
    lbl_feedback = ctk.CTkLabel(feed_box, text="", font=FONT_FEEDBACK)
    btn_frame    = ctk.CTkFrame(card, fg_color="transparent")
    lbl_image    = ctk.CTkLabel(card, image=ctk_image_empty, text="")
    resume_btn   = make_resume_button(card, "Resume Game")

    lbl_streak.pack(pady=(10, 0))
    lbl_wordbox.pack(pady=(0, 5))
    lbl_word.pack(side=tk.LEFT); lbl_weight.pack(side=tk.LEFT, padx=(5, 0))
    feed_box.pack(pady=10); lbl_feedback.pack(side=tk.LEFT, padx=5)
    btn_frame.pack(pady=10)
    lbl_image.pack(pady=(5, 5))
    resume_btn.pack(pady=(0, 10)); resume_btn.pack_forget()

    return {
        "label_streak": lbl_streak, "label_word": lbl_word,
        "label_weight": lbl_weight, "label_feedback": lbl_feedback,
        "button_frame": btn_frame, "label_image": lbl_image,
        "resume_button": resume_btn,
    }

# ─── GAMEPLAY LOGIC ─────────────────────────────────────────────────
def verificar_respuesta(selected: str, correct: str, word: str,
                        weights: dict[str, float],
                        wdg: dict[str, ctk.CTkBaseClass],
                        list_name: str, *, auto_hide: bool = True) -> None:
    global streak_counter
    is_correct = selected == correct
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    weights[word] = max(0.1, min(1.0, weights[word] + (0.2 if is_correct else -0.3)))

    if is_correct:
        wdg["label_feedback"].configure(text="✔️ Correct!", text_color="green")
        reproducir_sonido(SOUND_FILE_CORRECT)
        streak_counter += 1
        wdg["label_image"].configure(image=ctk_image_happy)
    else:
        wdg["label_feedback"].configure(text=f"❌ Incorrect. Correct: {correct}",
                                        text_color="red")
        reproducir_sonido(SOUND_FILE_INCORRECT)
        streak_counter = 0
        wdg["label_image"].configure(image=ctk_image_sad)
        vibrate_window()

    if auto_hide:
        wdg["label_feedback"].after(FEEDBACK_DELAY_MS,
                                    lambda: wdg["label_feedback"].configure(text=""))
        wdg["label_image"].after(FEEDBACK_DELAY_MS,
                                 lambda: wdg["label_image"].configure(image=ctk_image_empty))

    wdg["label_streak"].configure(text=f"Streak: {streak_counter}")
    wdg["label_word"].configure(text_color=utils.weight_to_color(weights[word]))
    wdg["label_weight"].configure(text=f"{weights[word]:.2f}")

    guardar_resultado_json(session_id, list_name, word, correct, selected,
                           is_correct, weights[word])

def ask_next_question(vocab: list[dict], weights: dict[str, float],
                      weight_file: Path,
                      mode_selector: ctk.CTkSegmentedButton,
                      wdg: dict[str, ctk.CTkBaseClass]) -> None:
    wdg["resume_button"].pack_forget()
    wdg["resume_button"].configure(command=lambda: None)

    word, correct, options = seleccionar_siguiente(
        vocab, weights, mode_selector.get(), wdg["label_image"]
    )

    wdg["label_word"].configure(text=word,
                                text_color=utils.weight_to_color(weights[word]))
    wdg["label_weight"].configure(text=f"{weights[word]:.2f}")

    for child in wdg["button_frame"].winfo_children():
        child.destroy()

    def handle_answer(opt: str) -> None:
        for btn in wdg["button_frame"].winfo_children():
            btn.configure(state=tk.DISABLED)

        if opt == correct:
            verificar_respuesta(opt, correct, word, weights, wdg,
                                weight_file.stem, auto_hide=True)
            wdg["label_feedback"].after(
                FEEDBACK_DELAY_MS,
                lambda: ask_next_question(vocab, weights, weight_file,
                                          mode_selector, wdg),
            )
        else:
            verificar_respuesta(opt, correct, word, weights, wdg,
                                weight_file.stem, auto_hide=False)
            wdg["resume_button"].pack(pady=(0, 10))
            wdg["resume_button"].configure(
                command=lambda: (
                    wdg["label_feedback"].configure(text=""),
                    wdg["label_image"].configure(image=ctk_image_empty),
                    ask_next_question(vocab, weights, weight_file,
                                      mode_selector, wdg),
                ),
                state=tk.NORMAL,
            )

    for option in options:
        make_answer_button(
            wdg["button_frame"], option, cmd=lambda opt=option: handle_answer(opt)
        ).pack(side=tk.LEFT, padx=5)

    save_data_to_json(weights, weight_file)

# ─── PUBLIC ENTRY POINT ─────────────────────────────────────────────
def survival_mode(vocab_path: Path | str | None = None) -> None:
    pygame.mixer.init()
    utils.clear_screen()
    global streak_counter, current_vocab_path
    streak_counter = 0

    current_vocab_path = Path(vocab_path) if vocab_path else (
        current_vocab_path or PROJECT_ROOT_PATH / "data" / "Verbs.JSON"
    )

    vocab         = load_vocabulary(current_vocab_path)
    list_name     = current_vocab_path.stem
    weight_path   = PROJECT_ROOT_PATH / "stats" / f"{list_name}_weights.json"

    try:
        weights = json.loads(weight_path.read_text("utf-8"))
    except FileNotFoundError:
        weights = {}
    for entry in vocab:
        weights.setdefault(entry["texto"], 0.5)
    save_data_to_json(weights, weight_path)

    root = ctk.CTkFrame(utils.app, fg_color="transparent")
    left = ctk.CTkFrame(root, fg_color=COLOR_LEFT_BG,
                        corner_radius=20, width=900, height=500)
    right= ctk.CTkFrame(root, fg_color=COLOR_RIGHT_BG)

    root.pack(expand=True, fill="both", padx=10, pady=20)
    left.pack(side=tk.LEFT, padx=(0, 20), fill="both", expand=True)
    right.pack(side=tk.RIGHT, fill="y")
    left.pack_propagate(False)

    selector = build_config_panel(right)
    widgets  = build_quiz_area(left)
    ask_next_question(vocab, weights, weight_path, selector, widgets)
