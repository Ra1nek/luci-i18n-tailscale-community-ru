'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const packageRoot = path.join(root, 'package/luci-app-tailscale-community-ru');
const resources = path.join(packageRoot, 'htdocs/luci-static/resources/tailscale-ru');
const catalog = new Map();
let key;
for (const line of fs.readFileSync(path.join(packageRoot, 'po/ru/tailscale.po'), 'utf8').split('\n')) {
    if (line.startsWith('msgid ')) key = JSON.parse(line.slice(6));
    if (line.startsWith('msgstr ')) catalog.set(key, JSON.parse(line.slice(7)));
}

function createPage(language = 'ru', page = 'admin-vpn-tailscale') {
    let onMutation;
    const textNode = { nodeValue: 'Tailscale is stopped.' };
    const context = {
        document: {
            documentElement: { lang: language },
            body: { dataset: { page } },
            getElementById: id => id === 'tailscale_health_notification' ? {} : null,
            createTreeWalker: () => {
                let visited = false;
                return { nextNode: () => visited ? null : (visited = true, textNode) };
            }
        },
        NodeFilter: { SHOW_TEXT: 4 },
        Node: { ELEMENT_NODE: 1 },
        MutationObserver: class {
            constructor(callback) { onMutation = callback; }
            observe() {}
        },
        window: { TR: {} },
        sfh: value => value,
        _: value => {
            assert.ok(catalog.has(value), `Missing catalog entry ${value}`);
            return catalog.get(value);
        }
    };
    vm.createContext(context);
    return { context, textNode, mutation: () => onMutation };
}

const units = fs.readFileSync(path.join(resources, 'units.js'), 'utf8');
const health = fs.readFileSync(path.join(resources, 'health.js'), 'utf8');
const page = createPage();
vm.runInContext(units, page.context);
assert.equal(page.context.window.TR.minute, 'мин');
assert.equal(page.context.window.TR.RX, 'Приём');
vm.runInContext(health, page.context);
assert.equal(page.textNode.nodeValue, 'Tailscale остановлен.');
const element = { nodeType: 1, closest: () => true };
for (const match of health.matchAll(/_\(("(?:\\.|[^"])*")\)/g)) {
    const message = JSON.parse(match[1]);
    page.textNode.nodeValue = message;
    page.mutation()([{ target: element }]);
    assert.equal(page.textNode.nodeValue, catalog.get(message));
}
page.textNode.nodeValue = 'A new unknown diagnostic message';
page.mutation()([{ target: element }]);
assert.equal(page.textNode.nodeValue, 'A new unknown diagnostic message');
page.textNode.nodeValue = 'Tailscale is stopped.';
page.mutation()([{ target: element }]);
page.mutation()([{ target: element }]);
assert.equal(page.textNode.nodeValue, 'Tailscale остановлен.');
for (const other of [createPage('en'), createPage('ru', 'admin-status-overview')]) {
    vm.runInContext(units, other.context);
    vm.runInContext(health, other.context);
    assert.deepEqual(other.context.window.TR, {});
    assert.equal(other.mutation(), undefined);
}
console.log('Translation runtime checks passed.');
