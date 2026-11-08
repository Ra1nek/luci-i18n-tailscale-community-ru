"""Run source, installer and workflow checks without compiling an APK."""
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def tool(name):
    value = os.environ.get(name.upper()) or shutil.which(name)
    if not value:
        raise SystemExit('Install ' + name + ' or set ' + name.upper() + ' to its executable path.')
    return value


def main():
    shellcheck = tool('shellcheck')
    actionlint = tool('actionlint')
    commands = [
        [sys.executable, 'scripts/check.py'],
        [sys.executable, 'tests/installer.py'],
        [shellcheck, 'install.sh', 'scripts/ci-build.sh'],
        [actionlint, '-shellcheck=', '-pyflakes=', '.github/workflows/build.yml'],
    ]
    for command in commands:
        subprocess.run(command, cwd=ROOT, check=True)
    print('Code checks passed.')


if __name__ == '__main__':
    main()
