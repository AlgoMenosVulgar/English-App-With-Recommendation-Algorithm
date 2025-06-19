## English-App-With-Recommendation-Algorithm


This app utilizes **CustomTkinter** for its user interface. It features a **backend recommendation algorithm** that presents words and phrases in a multiple-choice format. The system maintains a "**Memory**" by calculating an "**Ease**" weight for each word or phrase, indicating its difficulty for the user based on interactions. Three game modes are available: **Random**, where words are selected with equal probability; **AI Mode**, which is slated for future enhancements with machine learning; and **Hard**, which focuses on words in a higher percentile of difficulty (those the user frequently answers incorrectly).

[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)]()

## Features
- **Survival Mode** – Keeps going until you miss; then you must resume.
- **AI Difficulty** – Weight‑based algorithm surfaces weaker words more often.
- **Streak Counter** – Reset‑on‑mistake motivator front‑and‑center.
- **Per‑word Stats** – Weights and results stored in `/stats/` as JSON.
- **Audio & Vibration** – Immediate feedback with `pygame` and window shake.
- **Import Any JSON** – One‑click loader; supports any properly‑formatted list.

## Folder Structure
```text
Survival-Mode-App/
├── assets/         # images / sounds
├── data/           # sample vocabulary JSONs
├── stats/          # auto-generated weights & session logs
├── ui/             # GUI code
├── utils/          # I/O, algorithm, feedback helpers
├── main.py         # entry point
├── requirements.txt
└── README.md
```

## Quick Start
```bash
# 1. Clone this repository
git clone https://github.com/AlgoMenosVulgar/English-App-With-Recommendation-Algorithm.git
cd English-App-With-Recommendation-Algorithm

# 2. Install required packages
pip install -r requirements.txt

# 3. Run the application
python -m main
```

### Requirements
* Python 3.9+
* See `requirements.txt` for full dependency list (`customtkinter`, `Pillow`, `pygame`, …).

## Vocabulary JSON Format
```jsonc
[
  {
    "texto": "go",                 // Prompt shown
    "traduccion": "ir",            // Correct answer
    "categoria": "verb",           // Your grouping
    "opciones": ["ir", "empezar", "correr"]  // ≥3 Options incluging the correct one (the first slot of "opciones" has to be the correct option)
  }
]
```
Place the sample vocabulary JSONs anywhere; **Import List** dialog remembers last path used.

[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)]()

This is my very first repository, a humble starting point I hope to look back on proudly five or ten years from now.  
Let's hope it marks the beginning of a consistent journey through learning and open-source.

