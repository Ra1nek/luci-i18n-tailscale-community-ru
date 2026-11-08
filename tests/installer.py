from pathlib import Path
import os
import hashlib
import shlex
import subprocess
import tempfile
import re

repo = Path(__file__).resolve().parents[1]
shell = 'C:/Program Files/Git/bin/sh.exe' if os.name == 'nt' else '/bin/sh'
original = (repo / 'install.sh').read_text(encoding='utf-8')
fixture_bytes = b'test package payload\n'
scenarios = ['success', 'download-failure', 'corrupt', 'update-failure', 'dependencies-failure', 'install-failure', 'wrong-version', 'not-root']

for scenario in scenarios:
    with tempfile.TemporaryDirectory(prefix='tailscale-installer-') as directory:
        root = Path(directory)
        mock = root / 'bin'
        mock.mkdir()
        release = root / 'openwrt_release'
        release.write_text("DISTRIB_RELEASE='" + ('24.10.8' if scenario == 'wrong-version' else '25.12.6') + "'\n")
        fixture = root / 'fixture.apk'
        fixture.write_bytes(fixture_bytes)
        log = root / 'apk.log'
        def command(name, source):
            (mock / name).write_bytes(('#!/bin/sh\n' + source).encode())
            (mock / name).chmod(0o755)
        command('id', 'echo ' + ('1000' if scenario == 'not-root' else '0') + '\n')
        command('wget', '''while [ "$#" -gt 0 ]; do
 if [ "$1" = -O ]; then destination=$2; shift 2; else shift; fi
done
case "$SCENARIO" in
 download-failure) printf partial > "$destination"; exit 1 ;;
 corrupt) printf corrupted > "$destination" ;;
 *) cp "$FIXTURE" "$destination" ;;
esac
''')
        command('apk', '''printf '%s\\n' "$*" >> "$APK_LOG"
case "$SCENARIO:$*" in
 update-failure:update|dependencies-failure:"add luci-app"*|install-failure:"add --allow-untrusted"*) exit 1 ;;
esac
''')
        source = re.sub(r"SHA256='[a-f0-9]{64}'", "SHA256='" + hashlib.sha256(fixture_bytes).hexdigest() + "'", original)
        source = source.replace('/tmp/', root.as_posix() + '/')
        source = source.replace('/etc/openwrt_release', release.as_posix())
        script = root / 'install.sh'
        script.write_bytes(source.encode('utf-8'))
        environment = os.environ.copy()
        environment.update(SCENARIO=scenario, FIXTURE=fixture.as_posix(), APK_LOG=log.as_posix())
        mock_path = mock.as_posix()
        if os.name == 'nt':
            mock_path = subprocess.check_output([shell, '-c', 'cygpath -u ' + shlex.quote(mock_path)], text=True).strip()
        invocation = 'PATH=' + shlex.quote(mock_path) + ':$PATH; export PATH; sh ' + shlex.quote(script.as_posix())
        result = subprocess.run([shell, '-c', invocation], env=environment, capture_output=True)
        assert (result.returncode == 0) == (scenario == 'success'), (scenario, result.stdout, result.stderr)
        calls = log.read_text() if log.exists() else ''
        if scenario in ['download-failure', 'corrupt', 'wrong-version', 'not-root']:
            assert not calls, (scenario, calls)
        if scenario in ['update-failure', 'dependencies-failure']:
            assert '--allow-untrusted' not in calls
        if scenario == 'success':
            assert 'add --allow-untrusted --no-network ' in calls
        assert not list(root.glob('tailscale-luci-ru.*')), scenario

print('Installer scenarios PASS', len(scenarios), '(network and apk mocked)')
