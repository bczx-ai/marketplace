"""pytest conftest — 屏蔽重型三方库，确保零依赖测试可运行。"""
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


# === 屏蔽重型三方库（确保零依赖测试不引入 pip 包）===
class HeavyLibBlocker:
    BLOCKED = (
        "numpy", "pandas", "sklearn", "scipy", "arch", "statsmodels",
        "lightgbm", "matplotlib", "empyrical", "openpyxl", "docx",
        "requests", "ollama", "mootdx", "mcp", "langchain", "langgraph",
    )

    def find_module(self, name, path=None):
        for b in self.BLOCKED:
            if name == b or name.startswith(b + ".") or name.startswith(b + "_"):
                return self
        return None

    def load_module(self, name):
        raise ImportError("blocked " + name)


sys.meta_path.insert(0, HeavyLibBlocker())


# === stub crawl_utils 防止 fund_analyzer/market 因 requests 被屏蔽而导入失败 ===
_crawl_stub = types.ModuleType("crawl_utils")
_crawl_stub.safe_request = lambda *a, **k: None
_crawl_stub.fetch_json = lambda *a, **k: None
_crawl_stub.today_str = lambda fmt="%Y-%m-%d": "2026-07-26"
_crawl_stub.read_json = lambda p, d=None: d
_crawl_stub.write_json = lambda p, d, indent=2: True
_crawl_stub.detect_encoding = lambda r, d="utf-8": d
sys.modules["crawl_utils"] = _crawl_stub
