import random
import subprocess
from pathlib import Path
from sympy import randprime, factorint  # pip install sympy
import requests
import gmpy2
def get_factors_numbers_only(number):
    url = f"http://factordb.com/api?query={number}"
    response = requests.get(url)
    data = response.json()
    status = data.get('status')
    if status in ['CF', 'FF']:
        # Extract only the factor[0], ignoring exponent
        return [int(factor[0]) for factor in data.get('factors', [])]
    return []

def small_factors(n, limit=2000000):
    n = gmpy2.mpz(n)
    factors = []
    i = 2
    while i <= limit and n > 1:
        if n % i == 0:
            factors.append(i)
            n //= i
        else:
            i += 1
    return factors, n

PROJECT_DIR = Path(__file__).parent
EXE = PROJECT_DIR / "b1.exe"

def to_rev_hex(x: int) -> str:
    h = format(x, "x")
    if len(h) % 2 == 1:
        h = "0" + h
    return h[::-1]

def run_b1(p, qs, g) -> int:
    """
    Run b1.exe with:
        p
        n = len(qs)
        line of qs
        g
    all in reversed-hex format.
    Returns int 0/1 from the program.
    """
    n = len(qs)
    line_q = " ".join(to_rev_hex(q) for q in qs)
    inp = "\n".join([
        to_rev_hex(p),
        to_rev_hex(n),
        line_q,
        to_rev_hex(g),
    ]) + "\n"

    in_path = PROJECT_DIR / "_prop_b1.inp"
    out_path = PROJECT_DIR / "_prop_b1.out"
    in_path.write_text(inp, encoding="utf-8")

    r = subprocess.run(
        [str(EXE), str(in_path), str(out_path)],
        text=True,
        capture_output=True,
        timeout=5,
    )
    if r.returncode != 0 or not out_path.exists():
        raise RuntimeError(f"b1.exe failed: {r.stderr}")

    out = out_path.read_text(encoding="utf-8").strip()
    in_path.unlink(missing_ok=True)
    out_path.unlink(missing_ok=True)

    if out not in ("0", "1"):
        raise ValueError(f"Unexpected output: {out!r}")
    return int(out)

def random_prime_for_b1(bits: int = 512) -> int:
    # Keep p small enough that factorint(p-1) is cheap.
    low = 1 << (bits - 1)
    high = 1 << bits
    return randprime(low, high)

def is_primitive_root_py(p: int, g: int, qs) -> bool:
    """
    Check in Python whether g is a primitive root modulo p,
    given the distinct prime factors qs of p-1.
    """
    phi = p - 1
    for q in qs:
        e = phi // q
        if pow(g, e, p) == 1:
            return False
    return True

def random_case():
    p = random_prime_for_b1(512)
    print(p)
    fac, remaining = small_factors(p - 1)

    # fac = factordb_factors(p - 1)
    # factorint returns {prime: exponent}
    # fac = factorint(p - 1)
    qs = sorted(fac)  # distinct prime factors
    print(qs)
    # Choose random g in [2, p-2]
    g = random.randint(2, p - 2)
    # x = random.randint(2, p - 2)
    # print(x)
    # g = pow(x, 2, p)
    # g = guaranteed_non_primitive(p)
    return p, qs, g

def main():
    trials = 100
    for t in range(1, trials + 1):
        p, qs, g = random_case()
        expected = 1 if is_primitive_root_py(p, g, qs) else 0
        print(expected)

        try:
            got = run_b1(p, qs, g)
        except Exception as e:
            print(f"[FAIL] trial {t}: crash: {e}")
            print("  p     :", p)
            print("  qs    :", qs)
            print("  g     :", g)
            return

        if got != expected:
            print(f"[FAIL] trial {t}: wrong answer")
            print("  p     :", p)
            print("  qs    :", qs)
            print("  g     :", g)
            print("  p(hex):", to_rev_hex(p))
            print("  n(hex):", to_rev_hex(len(qs)))
            print("  qs(hex):", [to_rev_hex(q) for q in qs])
            print("  g(hex):", to_rev_hex(g))
            print("  expected:", expected)
            print("  got     :", got)
            return

        # if t % 10 == 0:
        print(f"[OK] up to trial {t}")

    print("All b1 random tests passed")

if __name__ == "__main__":
    main()
