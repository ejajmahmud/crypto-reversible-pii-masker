"""Core Crypto Reversible PII Masker implementation."""
import re
from typing import Dict, List, Tuple, Optional


class MaskResult:
    def __init__(self, masked_text: str, detected_entities_count: int):
        self.masked_text = masked_text
        self.detected_entities_count = detected_entities_count


class PIIMasker:
    PATTERNS = {
        "EMAIL": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
        "PHONE": re.compile(r"\b(?:\+?1[-.]?)?\(?[2-9]\d{2}\)?[-.]?\d{3}[-.]?\d{4}\b"),
        "SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
    }

    def __init__(self):
        self.forward_map: Dict[str, str] = {}  # original -> placeholder
        self.reverse_map: Dict[str, str] = {}  # placeholder -> original
        self.counters: Dict[str, int] = {"EMAIL": 0, "PHONE": 0, "SSN": 0}

    def mask(self, text: str) -> MaskResult:
        detected_count = 0
        masked_text = text

        for pii_type, regex in self.PATTERNS.items():
            matches = list(regex.finditer(masked_text))
            for m in reversed(matches):
                orig_val = m.group(0)
                if orig_val not in self.forward_map:
                    self.counters[pii_type] += 1
                    placeholder = f"<{pii_type}_{self.counters[pii_type]}>"
                    self.forward_map[orig_val] = placeholder
                    self.reverse_map[placeholder] = orig_val
                else:
                    placeholder = self.forward_map[orig_val]

                masked_text = masked_text[:m.start()] + placeholder + masked_text[m.end():]
                detected_count += 1

        return MaskResult(masked_text, detected_count)

    def unmask(self, model_output: str) -> str:
        restored = model_output
        for placeholder, original in self.reverse_map.items():
            restored = restored.replace(placeholder, original)
        return restored
