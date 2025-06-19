# ─── FONTS ──────────────────────────────────────────────────────────
ENTRY_FONT    = ("Inter", 16, "normal")
FONT_HEADER   = ("Inter", 15, "bold")
FONT_STREAK   = ("Inter", 20, "bold")
FONT_WORD     = ("Inter", 45)
FONT_WEIGHT   = ("Inter", 12)
FONT_FEEDBACK = ("Inter", 20)

# ─── COLOURS ────────────────────────────────────────────────────────
COLOR_CARD     = "#ffffff"
COLOR_LEFT_BG  = "#e0bae3"
COLOR_RIGHT_BG = "#f9eeff"

# ─── CTkSegmentedButton STYLE ───────────────────────────────────────
SEGMENTED_BUTTON_STYLE = {
    "font": ENTRY_FONT, "width": 240, "height": 34, "corner_radius": 4,
    "border_width": 1, "fg_color": "#eedaf0",
    "unselected_color": "#FFFFFF", "unselected_hover_color": "#F5F5F5",
    "selected_color": "#eedaf0", "selected_hover_color": "#F5F5F5",
    "text_color": "#1C1C1E", "text_color_disabled": "#A1A1A1",
}

# ─── BUTTON STYLES ──────────────────────────────────────────────────
BUTTON_GRAY = {
    "width": 200, "height": 30, "corner_radius": 4, "font": ENTRY_FONT,
    "fg_color": "#FFFFFF", "hover_color": "#F5F5F5", "text_color": "#000000",
    "border_color": "#9b9b9b", "border_width": 1, "state": "normal",
}
BUTTON_STYLE_ANSWERS = {
    "width": 180, "height": 40, "corner_radius": 20, "font": ENTRY_FONT,
    "fg_color": "#FFFFFF", "hover_color": "#eedaf0", "text_color": "#000000",
    "border_color": "#ababab", "border_width": 2, "state": "normal",
}
