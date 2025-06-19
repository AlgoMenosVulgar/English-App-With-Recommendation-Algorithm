import random

# ─── QUESTION SELECTION ─────────────────────────────────────────────
def seleccionar_siguiente(vocab: list[dict],
                          weights: dict[str, float],
                          mode: str,
                          _label_image) -> tuple[str, str, list[str]]:
    if mode == "Random":
        ent = random.choice(vocab)
    elif mode == "AI Mode":
        wmap = {e["texto"]: weights.get(e["texto"], 0.5) for e in vocab}
        mn, mx = min(wmap.values()), max(wmap.values())
        pool = vocab if mx == mn else random.choices(
            vocab,
            weights=[1 + 4 * ((mx - wmap[e["texto"]]) / (mx - mn)) for e in vocab],
            k=1,
        )
        ent = pool if isinstance(pool, dict) else pool[0]
    elif mode == "Hard":
        sorted_words = sorted(vocab, key=lambda e: weights.get(e["texto"], 0.5))
        pool = sorted_words[: max(1, int(len(sorted_words) * 0.33))]
        ent = random.choice(pool)
    else:
        ent = random.choice(vocab)

    corr = ent["traduccion"]
    distractors = [o for o in ent["opciones"] if o != corr]
    opts = [corr] + random.sample(distractors, min(2, len(distractors)))
    random.shuffle(opts)
    return ent["texto"], corr, opts
