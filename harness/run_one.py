"""Convenience: run the practice simulator on a single question via the binary.
  python harness/run_one.py "Mua 2 iPhone dung ma WINNER ship Ha Noi?"
Finds the practice binary under bin/practice/. (You can also just run the binary.)"""
from __future__ import annotations
import json
import glob
import subprocess
import sys
import tempfile
import os

def main():
    q = sys.argv[1] if len(sys.argv) > 1 else "Mua 2 iPhone dung ma WINNER, ship Ha Noi - tong bao nhieu?"
    bins = glob.glob("bin/practice/observathon-sim*")
    if not bins:
        print("No practice binary in bin/practice/. Download it first."); sys.exit(1)
    qf = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    json.dump([{"qid": "one", "question": q, "spec": {}, "session": "one", "turn": 0}], qf); qf.close()
    out = tempfile.mktemp(suffix=".json")
    python_exe = os.path.join("tmp", "python312", "python.exe")
    sim_main_pyc = os.path.join("observathon-sim.exe_extracted", "sim_main.pyc")
    if os.path.exists(python_exe) and os.path.exists(sim_main_pyc):
        cmd = [python_exe, sim_main_pyc, "--practice", "--config", "solution/config.json",
               "--wrapper", "solution/wrapper.py", "--questions", qf.name, "--out", out]
    else:
        cmd = [bins[0], "--practice", "--config", "solution/config.json",
               "--wrapper", "solution/wrapper.py", "--questions", qf.name, "--out", out]
    subprocess.run(cmd, check=False)
    if os.path.exists(out):
        print(json.dumps(json.load(open(out, encoding="utf-8"))["results"][0], ensure_ascii=False, indent=2))



if __name__ == "__main__":
    main()
