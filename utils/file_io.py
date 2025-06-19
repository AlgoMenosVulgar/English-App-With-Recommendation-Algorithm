"""
Lectura y escritura robusta de JSON + utilidades de E/S.
Siempre escribe en UTF-8 y lee con tolerancia a ficheros mal codificados.
"""
from __future__ import annotations
import json
from pathlib import Path

# ─── RUTAS GLOBALES ────────────────────────────────────────────────────────────
PROJECT_ROOT    = Path(__file__).parent.parent
RESULTADOS_PATH = PROJECT_ROOT / "stats" / "resultados_sesiones.json"

# ─── HELPERS PRIVADOS ──────────────────────────────────────────────────────────
def _read_json_safe(path: Path, default: list | dict | None = None):
    """Carga un JSON con reintentos de decodificación; devuelve default si falla."""
    if default is None:
        default = []
    if not path.exists():
        return default

    raw = path.read_bytes()
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return json.loads(raw.decode(enc))
        except UnicodeDecodeError:
            continue
        except json.JSONDecodeError:
            break   # contenido no es JSON
    # Si llega aquí => irreparable → se sobre-escribe la próxima vez
    return default


def _write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


# ─── API PÚBLICA ───────────────────────────────────────────────────────────────
def guardar_resultado_json(session_id: str, list_name: str, word: str,
                            correct_answer: str, selected_answer: str,
                            correct: bool, current_weight: float) -> None:
    """Anexa el resultado de la pregunta a `stats/resultados_sesiones.json`."""
    nuevo = {
        "session_id":     session_id,
        "list_name":      list_name,
        "word":           word,
        "correct_answer": correct_answer,
        "selected_answer": selected_answer,
        "correct":        correct,
        "current_weight": round(current_weight, 2),
    }

    data = _read_json_safe(RESULTADOS_PATH, default=[])
    data.append(nuevo)
    _write_json(RESULTADOS_PATH, data)


def save_data_to_json(data: dict, out: Path) -> None:
    """Guarda cualquier diccionario en JSON (UTF-8)."""
    _write_json(out, data)


def load_vocabulary(fp: Path) -> list[dict]:
    """Carga un vocabulario JSON (UTF-8 con tolerancia a BOM)."""
    return _read_json_safe(fp, default=[])
