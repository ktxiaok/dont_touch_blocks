import json
import os
from typing import Any, Dict
import xor_encrypt
from decimal import Decimal

DEFAULT_SAVE = {
    "is_fullscreen" : False
}

SAVE_FILENAME = "save.json"

ENCRYPT_KEY = "2023.12.15 Don't touch blocks. You can't cheat!"

_save: Dict[str, Any] = {}

def load():
    global _save

    _save = DEFAULT_SAVE.copy()
    if os.path.exists(SAVE_FILENAME):
        obj = None
        with open(SAVE_FILENAME, "r", encoding = "utf-8") as file:
            content = file.read()
            try:
                obj = json.loads(content)
            except:
                pass
        if obj != None:
            if "is_fullscreen" in obj:
                val = obj["is_fullscreen"]
                if isinstance(val, bool):
                    _save["is_fullscreen"] = val
            if "best_score" in obj and "best_score_md5" in obj:
                val1 = obj["best_score"]
                val2 = obj["best_score_md5"]
                if isinstance(val1, str) and isinstance(val2, str):
                    best_score = xor_encrypt.decrypt(val1, ENCRYPT_KEY, val2)
                    if best_score != None:
                        try:
                            _save["best_score"] = Decimal(best_score)
                        except:
                            pass
    save()

def save():
    global _save

    json_obj = {}
    json_obj["is_fullscreen"] = _save["is_fullscreen"]
    if "best_score" in _save:
        best_score = str(_save["best_score"])
        best_score, best_score_md5 = xor_encrypt.encrypt(
            best_score, ENCRYPT_KEY
        )
        json_obj["best_score"] = best_score
        json_obj["best_score_md5"] = best_score_md5
    with open(SAVE_FILENAME, "w", encoding = "utf-8") as file:
        json.dump(json_obj, file)

def is_fullscreen() -> bool:
    global _save

    return _save["is_fullscreen"]

def set_fullscreen(val: bool):
    global _save

    _save["is_fullscreen"] = val
    save()

def get_best_score() -> Decimal:
    global _save

    if "best_score" in _save:
        return _save["best_score"]
    else:
        return Decimal(0)
    
def set_best_score(val: Decimal):
    global _save

    _save["best_score"] = val
    save()