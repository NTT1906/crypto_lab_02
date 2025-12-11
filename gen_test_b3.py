import random
import subprocess
from pathlib import Path
from sympy import randprime  # pip install sympy

PROJECT_DIR = Path(__file__).parent
EXE = PROJECT_DIR / "b3.exe"

def to_rev_hex(x: int) -> str:
    h = format(x, "x")
    if len(h) % 2 == 1:
        h = "0" + h
    return h[::-1]

def from_rev_hex(s: str) -> int:
    s = s.strip()
    if not s:
        return 0
    return int(s[::-1], 16)

def run_b3(p, g, x, c1, c2):
    """Run b3.exe with reversed-hex input and parse its two outputs."""
    inp = "\n".join([
        to_rev_hex(p),
        to_rev_hex(g),
        to_rev_hex(x),
        to_rev_hex(c1),
        to_rev_hex(c2),
    ]) + "\n"

    in_path = PROJECT_DIR / "_prop_b3.inp"
    out_path = PROJECT_DIR / "_prop_b3.out"
    in_path.write_text(inp, encoding="utf-8")

    r = subprocess.run(
        [str(EXE), str(in_path), str(out_path)],
        text=True,
        capture_output=True,
        timeout=5,
    )
    if r.returncode != 0 or not out_path.exists():
        raise RuntimeError(f"b3.exe failed: {r.stderr}")

    lines = out_path.read_text(encoding="utf-8").strip().splitlines()
    in_path.unlink(missing_ok=True)
    out_path.unlink(missing_ok=True)

    if len(lines) != 2:
        raise ValueError(f"Expected 2 output lines, got {len(lines)}")

    h_exe = from_rev_hex(lines[0])
    m_exe = from_rev_hex(lines[1])
    return h_exe, m_exe

def random_prime(bits: int = 32) -> int:
    low = 1 << (bits - 1)
    high = 1 << bits
    return randprime(low, high)

def random_case():
    p = random_prime(32)
    g = random.randint(2, p - 2)
    x = random.randint(1, p - 2)
    k = random.randint(1, p - 2)      # ephemeral key
    m = random.randint(1, p - 2)      # plaintext

    h = pow(g, x, p)
    c1 = pow(g, k, p)
    c2 = (m * pow(h, k, p)) % p
    return p, g, x, m, h, c1, c2

def main():
    trials = 100
    for t in range(1, trials + 1):
        p, g, x, m, h, c1, c2 = random_case()

        # Expected results
        h_exp = h
        m_exp = m

        try:
            h_exe, m_exe = run_b3(p, g, x, c1, c2)
        except Exception as e:
            print(f"[FAIL] trial {t}: crash: {e}")
            print("  p,g,x,m,c1,c2:", p, g, x, m, c1, c2)
            return

        if h_exe != h_exp or m_exe != m_exp:
            print(f"[FAIL] trial {t}: wrong answer")
            print("  p,g,x,m,c1,c2 (int):", p, g, x, m, c1, c2)
            print("  p,g,x,m,c1,c2 (hex):",
                  to_rev_hex(p), to_rev_hex(g), to_rev_hex(x),
                  to_rev_hex(m), to_rev_hex(c1), to_rev_hex(c2))
            print("  expected h,m (int):", h_exp, m_exp)
            print("  got      h,m (int):", h_exe, m_exe)
            print("  expected h,m (hex):", to_rev_hex(h_exp), to_rev_hex(m_exp))
            print("  got      h,m (hex):", to_rev_hex(h_exe), to_rev_hex(m_exe))
            return

        if t % 10 == 0:
            print(f"[OK] up to trial {t}")

    print("All b3 random tests passed")

if __name__ == "__main__":
    main()
