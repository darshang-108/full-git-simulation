"""
Helper script to install the pre-commit hook into .git/hooks/.

Run:  python setup_hooks.py
"""

import shutil
import os
import stat

HOOK_SRC = os.path.join("hooks", "pre-commit")
HOOK_DST = os.path.join(".git", "hooks", "pre-commit")


def main():
    if not os.path.isdir(".git"):
        print("Error: This must be run from the repository root (no .git/ found).")
        return

    os.makedirs(os.path.dirname(HOOK_DST), exist_ok=True)
    shutil.copy2(HOOK_SRC, HOOK_DST)

    # Make executable (required on Linux / macOS / Git Bash)
    st = os.stat(HOOK_DST)
    os.chmod(HOOK_DST, st.st_mode | stat.S_IEXEC)

    print(f"✅ Pre-commit hook installed → {HOOK_DST}")


if __name__ == "__main__":
    main()
