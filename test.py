import subprocess
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
ASSET_DIR = PROJECT_DIR / "asset"
EXECUTABLES = ["b1.exe", "b2.exe", "b3.exe", "b4.exe"]
PROJECT_TESTS = [
    "project_02_01",
    "project_02_02",
    "project_02_03",
    "project_02_04",
]

def run_once(exe, inp, out_tmp):
    if out_tmp.exists():
        out_tmp.unlink()
    r = subprocess.run(
        [str(exe), str(inp), str(out_tmp)],
        text=True,
        capture_output=True,
        timeout=5,
    )
    return r.returncode == 0 and out_tmp.exists()

def files_equal(a: Path, b: Path) -> bool:
    ta = a.read_text(encoding="utf-8").replace("\r\n", "\n").rstrip("\n")
    tb = b.read_text(encoding="utf-8").replace("\r\n", "\n").rstrip("\n")
    return ta == tb

def test_exe(exe_name: str, tests: Path):
    exe = PROJECT_DIR / exe_name
    if not exe.exists():
        print(f"{exe_name}: not found, skipped.")
        return

    print(f"{exe_name}:")
    out_tmp = PROJECT_DIR / "_tmp.out"
    total = passed = 0

    for inp in sorted(tests.glob("*.inp")):
        ref = inp.with_suffix(".out")
        if not ref.exists():
            continue
        total += 1

        ok_run = run_once(exe, inp, out_tmp)
        ok_cmp = ok_run and files_equal(out_tmp, ref)

        if ok_cmp:
            passed += 1
        else:
            print(f"  FAIL {inp.relative_to(ASSET_DIR)}")

    print(f"  => {passed}/{total} passed")


if __name__ == "__main__":
    for i in range(len(EXECUTABLES)):
        test_exe(EXECUTABLES[i], ASSET_DIR / PROJECT_TESTS[i])
    tmp = PROJECT_DIR / "_tmp.out"
    if tmp.exists():
        tmp.unlink()