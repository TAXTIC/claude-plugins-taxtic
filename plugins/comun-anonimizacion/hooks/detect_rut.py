"""Detect Chilean RUT in stdin. Exit non-zero with a warning if found.

Used by Claude Code hooks to flag possible PII in prompts or edited files.
"""

import json
import re
import sys

RUT_PATTERN = re.compile(
    r"\b\d{1,2}\.?\d{3}\.?\d{3}-?[\dkK]\b|\b\d{7,8}-?[\dkK]\b"
)


def validate_rut(rut: str) -> bool:
    """Validate Chilean RUT check digit (módulo 11)."""
    rut = rut.replace(".", "").replace("-", "").upper()
    if len(rut) < 2:
        return False
    body, dv = rut[:-1], rut[-1]
    if not body.isdigit():
        return False
    multipliers = [2, 3, 4, 5, 6, 7]
    total = 0
    for i, digit in enumerate(reversed(body)):
        total += int(digit) * multipliers[i % len(multipliers)]
    remainder = total % 11
    expected = 11 - remainder
    if expected == 11:
        expected_dv = "0"
    elif expected == 10:
        expected_dv = "K"
    else:
        expected_dv = str(expected)
    return dv == expected_dv


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw)
        text = payload.get("prompt") or payload.get("content") or raw
    except json.JSONDecodeError:
        text = raw

    matches = RUT_PATTERN.findall(text)
    real_ruts = [m for m in matches if validate_rut(m) and m not in {"11111111-1", "22222222-2", "33333333-3"}]

    if real_ruts:
        sys.stderr.write(
            f"\n[comun-anonimizacion] Detected {len(real_ruts)} possible real Chilean RUT(s) "
            f"in this input. Consider running /anonimizar first.\n"
            f"Sample: {real_ruts[0]}\n"
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
