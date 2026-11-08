# Разработка и совместимость

[← На главную](../README.md) · [Правила участия](../CONTRIBUTING.md)

## Сборка и исходники


Исходники перевода, оформления и упаковки находятся в одном репозитории. Правки проходят проверку каталога и сборку APK в GitHub Actions.

<details>
<summary><strong>Проверить исходники и собрать пакет</strong></summary>

Для проверки нужны Python 3 и Node.js. Для SDK нужен Linux x86-64 с [зависимостями OpenWrt](https://openwrt.org/docs/guide-developer/toolchain/using_the_sdk). Используйте обычного пользователя и путь к рабочей копии без пробелов.

```sh
git clone https://github.com/Ra1nek/tailscale-luci-ru.git
cd tailscale-luci-ru
python3 scripts/check.py
bash scripts/ci-build.sh
```

Сценарий загружает SDK **25.12.6**, проверяет его SHA-256, подключает закреплённые официальные feeds и этот проект как локальный feed. Затем собирает `po2lmo` и единый пакет. APK, контрольные суммы, сведения о сборке и журнал сохраняются в `artifacts/`.

Для уже подготовленного SDK с официальным feed LuCI добавьте локальный feed проекта.

```sh
printf '\nsrc-link tailscale_ru /path/to/tailscale-luci-ru\n' >> feeds.conf
./scripts/feeds update tailscale_ru
./scripts/feeds install -p tailscale_ru luci-app-tailscale-community-ru
make menuconfig
make package/luci-base/host/compile V=s
make package/luci-app-tailscale-community-ru/compile V=s NO_DEPS=1
```

В `menuconfig` выберите пакет в разделе **LuCI → Applications**.

</details>

<details>
<summary><strong>Структура проекта</strong></summary>

```text
package/luci-app-tailscale-community-ru/
├── Makefile
├── LICENSE
├── NOTICE
├── htdocs/luci-static/resources/tailscale-ru/
│   ├── health.js
│   ├── layout.css
│   └── units.js
├── po/ru/tailscale.po
└── root/usr/share/
    ├── luci/menu.d/zz-tailscale-ru-layout.json
    └── ucode/luci/template/tailscale-ru.ut
.github/workflows/build.yml
scripts/
tests/
```

`htdocs` устанавливается в `/www`, `root` содержит шаблон и запись меню LuCI. Штатный `po2lmo` из SDK компилирует каталог в `tailscale.ru.lmo`. Домен `tailscale` соответствует исходной странице приложения.

</details>


## Проверенные версии


| Компонент | Требование |
| --- | --- |
| OpenWrt | Ветка **25.12**, пакетный менеджер APK. |
| Интерфейс | **luci-app-tailscale-community**. |
| Служба | **tailscale**. |
| LuCI | **luci-base** и **ucode-mod-fs**. |
| Процессор | Пакет содержит перевод, стили и JavaScript, его архитектура — **noarch**. |

Нужные зависимости указаны в пакете. Используйте репозитории своего выпуска OpenWrt.

**Что проверено**

- Сборка единого APK через официальный SDK **OpenWrt 25.12.6**.
- Полнота перевода по странице **Tailscale Community 4.5.1-r1** и закреплённой версии из официального feed **OpenWrt 25.12**.
- Параметры сообщений, JavaScript и обработка известных уведомлений о состоянии службы.
- Оформление страницы **4.5.1-r1** при разработке исходных дополнений.

> [!IMPORTANT]
> Единый пакет прошёл сборку SDK и автоматические проверки. Отдельная проверка объединённого пакета в браузере ещё предстоит. При обновлении Tailscale Community нужно повторно сверять тексты и разметку страницы.

