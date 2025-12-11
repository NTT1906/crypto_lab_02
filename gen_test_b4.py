import math
import random
import subprocess
from pathlib import Path
from sympy import randprime  # pip install sympy

PROJECT_DIR = Path(__file__).parent
EXE = PROJECT_DIR / "b4.exe"

def to_rev_hex(x: int) -> str:
    h = format(x, "x")
    if len(h) % 2 == 1:
        h = "0" + h
    return h[::-1]

def run_b4(p, g, y, m, r, h_sig) -> int:
    inp = "\n".join([
        to_rev_hex(p),
        to_rev_hex(g),
        to_rev_hex(y),
        to_rev_hex(m),
        to_rev_hex(r),
        to_rev_hex(h_sig),
    ]) + "\n"

    in_path = PROJECT_DIR / "_prop_b4.inp"
    out_path = PROJECT_DIR / "_prop_b4.out"
    in_path.write_text(inp, encoding="utf-8")

    r_proc = subprocess.run(
        [str(EXE), str(in_path), str(out_path)],
        text=True,
        capture_output=True,
        timeout=5,
    )
    if r_proc.returncode != 0 or not out_path.exists():
        raise RuntimeError(f"b4.exe failed: {r_proc.stderr}")

    out = out_path.read_text(encoding="utf-8").strip()
    in_path.unlink(missing_ok=True)
    out_path.unlink(missing_ok=True)

    if out not in ("0", "1"):
        raise ValueError(f"Unexpected output: {out!r}")
    return int(out)

def random_prime(bits: int = 32) -> int:
    low = 1 << (bits - 1)
    high = 1 << bits
    return randprime(low, high)

def sample_coprime(mod: int) -> int:
    """Return random k with gcd(k, mod) == 1."""
    while True:
        k = random.randint(1, mod - 1)
        if math.gcd(k, mod) == 1:
            return k

def gen_valid_signature():
    """
    Generate p, g, y, m and a valid (r, h) for ElGamal signature over Z_p.
    Scheme:
      y = g^x mod p
      choose k with gcd(k, p-1) = 1
      r = g^k mod p
      h = (m - x*r) * k^{-1} mod (p-1)
    """
    p = random_prime(32)
    g = random.randint(2, p - 2)
    x = random.randint(1, p - 2)
    y = pow(g, x, p)
    m = random.randint(1, p - 2)

    k = sample_coprime(p - 1)
    r = pow(g, k, p)
    kinv = pow(k, -1, p - 1)
    h_sig = ((m - x * r) * kinv) % (p - 1)
    return p, g, y, m, r, h_sig

def main():
    trials = 100

    # Valid signatures
    for t in range(1, trials + 1):
        p, g, y, m, r, h_sig = gen_valid_signature()
        got = run_b4(p, g, y, m, r, h_sig)
        if got != 1:
            print(f"[FAIL] valid trial {t}: signature rejected")
            print("  p,g,y,m,r,h (int):", p, g, y, m, r, h_sig)
            return
        if t % 10 == 0:
            print(f"[OK] valid up to trial {t}")

    # Invalid signatures
    for t in range(1, trials + 1):
        p, g, y, m, r, h_sig = gen_valid_signature()
        m_bad = (m + 1) % (p - 1) or 1
        got = run_b4(p, g, y, m_bad, r, h_sig)
        if got != 0:
            print(f"[FAIL] invalid trial {t}: bad signature accepted")
            print("  p,g,y,m_bad,r,h (int):", p, g, y, m_bad, r, h_sig)
            return
        if t % 10 == 0:
            print(f"[OK] invalid up to trial {t}")

    print("All b4 random tests passed")

if __name__ == "__main__":
    main()
