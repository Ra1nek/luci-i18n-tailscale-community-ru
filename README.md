# Tailscale LuCI RU

Русский перевод и оформление Tailscale Community для OpenWrt. Одно дополнение объединяет перевод страницы, сообщения состояния и исправления отображения на узком экране.

## Возможности

- Русские названия настроек и пояснения к ним.
- Перевод известных сообщений состояния Tailscale.
- Читаемые кнопки, подписи и заголовки таблицы на телефоне и компьютере.
- Общий пакет перевода и оформления.

Дополнение использует штатную страницу Tailscale Community. Стили и обработка сообщений ограничены русской страницей Tailscale.

## Совместимость

Нужны OpenWrt 25.12, LuCI и `luci-app-tailscale-community`. Пакет зависит от `tailscale`, `luci-base` и `ucode-mod-fs`. SDK и официальные feeds для сборки закреплены на OpenWrt 25.12.6.

Перевод и оформление проверены с Tailscale Community 4.5.1-r1. Обновление исходного приложения может изменить тексты и разметку, поэтому совместимость с новой версией нужно проверять отдельно. Пакет `luci-app-tailscale` из других проектов использует другой интерфейс.

Каталог также проверяется по исходной странице из официального feed OpenWrt 25.12, закреплённого в сборке. Эта проверка охватывает тексты и параметры сообщений. Проверка отображения в браузере относится к версии 4.5.1-r1.

## Установка

Соберите пакет через SDK или скачайте архив пакета со страницы завершённой сборки GitHub Actions. Готовый пакет имеет архитектуру `all`. Совместимость определяется выпуском OpenWrt и версией приложения.

На роутере выполните команды, подставив имя скачанного APK.

```sh
apk update
apk add luci-app-tailscale-community tailscale
apk add --allow-untrusted /tmp/luci-app-tailscale-community-ru-1.1.0-r1.apk
rm -f /tmp/luci-indexcache.*
```

`--allow-untrusted` нужен для локального APK, пока пакет распространяется без подписи репозитория. Сверьте SHA-256 с файлом `SHA256SUMS` из той же сборки.

В LuCI выберите русский язык и заново откройте страницу Tailscale. Для удаления дополнения выполните `apk del luci-app-tailscale-community-ru`, очистите кэш LuCI указанной выше командой и обновите страницу браузера.

## Сборка

Нужен Linux x86-64 и зависимости OpenWrt SDK. Путь к рабочей копии должен быть без пробелов. Сценарий скачивает официальный SDK, проверяет SHA-256, подключает этот репозиторий как локальный feed и собирает пакет штатными средствами OpenWrt.

```sh
python3 scripts/check.py
bash scripts/ci-build.sh
```

APK, контрольные суммы, сведения о сборке и журнал появятся в `artifacts/`. Для проверки исходников нужен Python 3 и Node.js. Сборка выполняется от обычного пользователя.

Для подключения к уже подготовленному SDK добавьте feed и соберите пакет.

```sh
printf '\nsrc-link tailscale_ru /path/to/tailscale-luci-ru\n' >> feeds.conf
./scripts/feeds update tailscale_ru
./scripts/feeds install -p tailscale_ru luci-app-tailscale-community-ru
make menuconfig
make package/luci-base/host/compile V=s
make package/luci-app-tailscale-community-ru/compile V=s NO_DEPS=1
```

Официальный feed LuCI должен быть подключён. В `menuconfig` выберите пакет в разделе LuCI → Applications.

## Структура

```text
package/luci-app-tailscale-community-ru/
├── Makefile
├── LICENSE
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

`htdocs` устанавливается в `/www`, `root` содержит шаблон и дополнение меню LuCI. Каталог PO компилируется штатным `po2lmo` из SDK в `tailscale.ru.lmo`. Домен `tailscale` соответствует исходной странице. Один Makefile собирает единый пакет. Правила для правок описаны в [CONTRIBUTING.md](CONTRIBUTING.md).

## Источники и лицензия

Основа перевода — проект nagual2, Apache-2.0. Перевод дополнен и вычитан, оформление выделено в отдельные ресурсы страницы. Авторство и сведения об изменениях сохранены в `NOTICE`.

- [Tailscale Community](https://github.com/Tokisaki-Galaxy/luci-app-tailscale-community)
- [Исходный русский перевод](https://github.com/nagual2/luci-i18n-tailscale-community-ru)
- [Официальный LuCI](https://github.com/openwrt/luci)
- [Сборка пакетов через OpenWrt SDK](https://openwrt.org/docs/guide-developer/toolchain/using_the_sdk)
- [Лицензия Apache-2.0](LICENSE)
