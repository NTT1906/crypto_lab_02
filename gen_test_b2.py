import random
import subprocess
from pathlib import Path
from sympy import randprime  # pip install sympy

PROJECT_DIR = Path(__file__).parent
EXE = PROJECT_DIR / "b2.exe"

def to_rev_hex(x: int) -> str:
    # hex without 0x, lowercase, no leading zeros unless value is 0
    h = format(x, "x")
    # if length is odd, pad to full bytes so reversing is byte-wise if you want
    if len(h) % 2 == 1:
        h = "0" + h
    return h[::-1]  # reverse string

def from_rev_hex(s: str) -> int:
    s = s.strip()
    if not s:
        return 0
    # reverse back then parse as hex
    return int(s[::-1], 16)

def run_b2(p, g, a, b):
    """Run b2.exe with reversed-hex input and parse three reversed-hex outputs."""
    inp = "\n".join([
        to_rev_hex(p),
        to_rev_hex(g),
        to_rev_hex(a),
        to_rev_hex(b),
    ]) + "\n"

    in_path = PROJECT_DIR / "_prop.inp"
    out_path = PROJECT_DIR / "_prop.out"
    in_path.write_text(inp, encoding="utf-8")

    r = subprocess.run(
        [str(EXE), str(in_path), str(out_path)],
        text=True,
        capture_output=True,
        timeout=5,
    )
    if r.returncode != 0 or not out_path.exists():
        raise RuntimeError(f"b2.exe failed: {r.stderr}")

    lines = out_path.read_text(encoding="utf-8").strip().splitlines()
    in_path.unlink(missing_ok=True)
    out_path.unlink(missing_ok=True)

    if len(lines) != 3:
        raise ValueError(f"Expected 3 output lines, got {len(lines)}")

    A = from_rev_hex(lines[0])
    B = from_rev_hex(lines[1])
    K = from_rev_hex(lines[2])
    return A, B, K

def random_prime(bits: int = 32) -> int:
    low = 1 << (bits - 1)
    high = 1 << bits
    return randprime(low, high)

def random_case():
    p = random_prime(32)
    g = random.randint(2, p - 2)
    a = random.randint(1, p - 2)
    b = random.randint(1, p - 2)
    return p, g, a, b

def main():
    trials = 100
    for t in range(1, trials + 1):
        p, g, a, b = random_case()

        # Expected values in integer form.
        A_exp = pow(g, a, p)
        B_exp = pow(g, b, p)
        K_exp = pow(g, a * b, p)

        try:
            A_exe, B_exe, K_exe = run_b2(p, g, a, b)
        except Exception as e:
            print(f"[FAIL] trial {t}: crash: {e}")
            print("  input (int):", p, g, a, b)
            return

        if (A_exe, B_exe, K_exe) != (A_exp, B_exp, K_exp):
            print(f"[FAIL] trial {t}: wrong answer")
            print("  input (int):", p, g, a, b)
            print("  input (hex):", to_rev_hex(p), to_rev_hex(g), to_rev_hex(a), to_rev_hex(b))
            print("  expected:", to_rev_hex(A_exp), to_rev_hex(B_exp), to_rev_hex(K_exp))
            print("  got     :", to_rev_hex(A_exe), to_rev_hex(B_exe), to_rev_hex(K_exe))
            return

        if t % 10 == 0:
            print(f"[OK] up to trial {t}")

    print("All b2 random tests passed")

if __name__ == "__main__":
    main()
