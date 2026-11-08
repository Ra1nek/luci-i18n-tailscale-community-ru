"""Validate catalogs, source coverage and the scoped JavaScript entry points."""
import ast
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'package/luci-app-tailscale-community-ru'


def read_po(path):
    catalog = {}
    key = None
    value = ''
    field = None
    for line in path.read_text(encoding='utf-8').splitlines() + ['']:
        if line.startswith('msgid '):
            key = ast.literal_eval(line[6:])
            value = ''
            field = 'key'
        elif line.startswith('msgstr '):
            value = ast.literal_eval(line[7:])
            field = 'value'
        elif line.startswith('"'):
            if field == 'key':
                key += ast.literal_eval(line)
            elif field == 'value':
                value += ast.literal_eval(line)
        elif not line.strip() and key is not None:
            if key in catalog:
                raise ValueError('Duplicate translation key ' + key)
            catalog[key] = value
            key = None
    return catalog


def translation_keys(source):
    expression = r'''\b_\(\s*('(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*")'''
    return {ast.literal_eval(match[1]) for match in re.finditer(expression, source)}


def main():
    catalog = read_po(PACKAGE / 'po/ru/tailscale.po')
    view = '\n'.join(path.read_text(encoding='utf-8') for path in (ROOT / 'tests/fixtures').glob('tailscale-*.js'))
    required = translation_keys(view)
    for match in re.finditer(r"fmt\([^,]+,\s*'([^']+)',\s*'([^']+)'\)", view):
        required.update(match.groups())
    for match in re.finditer(r"_\(\s*('(?:\\.|[^'\\])*')\.format\(\s*('(?:\\.|[^'\\])*')\s*\)\s*\)", view):
        required.add(ast.literal_eval(match[1]).replace('%s', ast.literal_eval(match[2])))
    javascript = list((PACKAGE / 'htdocs').rglob('*.js'))
    for path in javascript:
        source = path.read_text(encoding='utf-8')
        required.update(translation_keys(source))
        assert 'admin-vpn-tailscale' in source and "lang !== 'ru'" in source, path
        assert '__HEALTH_MESSAGES__' not in source
        subprocess.run(['node', '--check', str(path)], check=True)
    for path in (PACKAGE / 'root').rglob('*.ut'):
        required.update(translation_keys(path.read_text(encoding='utf-8')))
    missing = sorted(key for key in required if not catalog.get(key))
    assert not missing, missing
    placeholders = re.compile(r'%(?:\d+\$)?[-+ #0]*(?:\d+|\*)?(?:\.(?:\d+|\*))?[a-zA-Z%]')
    for key, value in catalog.items():
        if key:
            assert sorted(placeholders.findall(key)) == sorted(placeholders.findall(value)), key
    for path in (PACKAGE / 'root').rglob('*.json'):
        json.loads(path.read_text(encoding='utf-8'))
    subprocess.run(['node', str(ROOT / 'tests/translation-runtime.cjs')], check=True)
    print(f'Catalog and source checks passed. {len(catalog) - 1} translated keys.')


if __name__ == '__main__':
    main()
