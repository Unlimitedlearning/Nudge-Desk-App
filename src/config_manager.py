# src/config_manager.py
import json
import os

CONFIG_PATH = "data/calibration.json"

def load_calibration():
    """读取本地保存的阈值，如果不存在返回 None"""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("threshold")
        except Exception:
            return None
    return None

def save_calibration(threshold):
    """保存阈值到本地"""
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump({"threshold": threshold}, f, ensure_ascii=False, indent=4)