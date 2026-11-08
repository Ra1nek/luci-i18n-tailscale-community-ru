"""Check a built APK against Makefile, installer and release checksums."""
import argparse
import hashlib
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = 'luci-app-tailscale-community-ru'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path, help='Directory containing APK and SHA256SUMS')
    args = parser.parse_args()
    makefile = (ROOT / 'package' / PACKAGE / 'Makefile').read_text(encoding='utf-8')
    version = re.search(r'^PKG_VERSION:=(\S+)$', makefile, re.M)[1]
    release = re.search(r'^PKG_RELEASE:=(\S+)$', makefile, re.M)[1]
    expected_version = version + '-r' + release
    installer = (ROOT / 'install.sh').read_text(encoding='utf-8')
    assert re.search(r"^VERSION='([^']+)'", installer, re.M)[1] == expected_version, 'Installer and Makefile versions differ'
    expected_name = PACKAGE + '-' + expected_version + '.apk'
    checksum_lines = (args.directory / 'SHA256SUMS').read_text().splitlines()
    checksums = {}
    for line in checksum_lines:
        digest, name = line.split(None, 1)
        name = name.strip().removeprefix('*')
        assert Path(name).name == name, 'Unexpected checksum path'
        assert re.fullmatch('[a-f0-9]{64}', digest), 'Invalid SHA-256'
        assert name not in checksums, 'Duplicate checksum entry'
        checksums[name] = digest
    assert expected_name in checksums, 'Expected APK missing from SHA256SUMS'
    actual = hashlib.sha256((args.directory / expected_name).read_bytes()).hexdigest()
    assert actual == checksums[expected_name], 'APK checksum mismatch'
    pinned = re.search(r"^SHA256='([a-f0-9]{64})'", installer, re.M)[1]
    assert actual == pinned, 'Installer checksum differs from built APK'
    print('Release version, filename and SHA-256 match.')


if __name__ == '__main__':
    main()
