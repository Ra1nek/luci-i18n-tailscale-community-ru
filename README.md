<p align="center">
  <img src="docs/assets/mark.svg" width="80" height="80" alt="Tailscale LuCI RU">
</p>

<h1 align="center">Tailscale LuCI RU</h1>

<p align="center">
  <strong>Tailscale в LuCI — по-русски.</strong><br>
  Перевод настроек, понятные пояснения и аккуратное отображение на узком экране.
</p>

<p align="center">
  <a href="https://github.com/Ra1nek/tailscale-luci-ru/actions/workflows/build.yml"><img src="https://github.com/Ra1nek/tailscale-luci-ru/actions/workflows/build.yml/badge.svg?branch=main" alt="Статус сборки OpenWrt"></a>
  <a href="#совместимость"><img src="https://img.shields.io/badge/OpenWrt-25.12-2563eb?style=flat-square" alt="OpenWrt 25.12"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache--2.0-64748b?style=flat-square" alt="Лицензия Apache-2.0"></a>
</p>

<p align="center">
  <a href="#установка">Установка</a> ·
  <a href="#возможности">Возможности</a> ·
  <a href="#совместимость">Совместимость</a> ·
  <a href="#разработка">Разработка</a> ·
  <a href="https://github.com/Ra1nek/tailscale-luci-ru/issues">Сообщить об ошибке</a>
</p>

---

Дополнение для Tailscale Community в OpenWrt. Русский перевод и оформление страницы устанавливаются одним пакетом `luci-app-tailscale-community-ru`.

## Возможности

| Возможность | Что меняется |
| --- | --- |
| **Настройки на русском** | Названия и пояснения помогают выбрать, как подключаться к Tailscale и пользоваться домашней сетью. |
| **Понятные сообщения** | Известные уведомления о состоянии службы получают русский перевод. |
| **Удобнее на узком экране** | Исправлены переносы, подписи, кнопки и заголовки таблицы устройств. |

Оформление и дополнительные переводы применяются к русской странице Tailscale. Страница использует штатный интерфейс Tailscale Community.

## Установка

### 1. Скачайте пакет

Откройте последнюю успешную сборку ветки `main`. В разделе **Artifacts** скачайте архив **luci-app-tailscale-community-ru-openwrt-25.12.6** и распакуйте его.

**[Открыть сборки и скачать APK →](https://github.com/Ra1nek/tailscale-luci-ru/actions/workflows/build.yml)**

В архиве находятся APK, файл `SHA256SUMS` для проверки загрузки и сведения о сборке.

> [!NOTE]
> Для скачивания артефактов GitHub нужен вход в аккаунт.

### 2. Передайте файлы на роутер

Скопируйте APK и `SHA256SUMS` в `/tmp` на роутере. Например, из папки с распакованным архивом можно выполнить команду ниже. Замените `192.168.1.1` на адрес своего роутера.

```sh
scp -O luci-app-tailscale-community-ru-1.1.0-r1.apk SHA256SUMS root@192.168.1.1:/tmp/
```

### 3. Установите дополнение

Подключитесь к роутеру по SSH и выполните команды для версии **1.1.0-r1**.

```sh
cd /tmp &&
sha256sum -c SHA256SUMS &&
apk update &&
apk add luci-app-tailscale-community tailscale &&
apk add --allow-untrusted ./luci-app-tailscale-community-ru-1.1.0-r1.apk &&
rm -f /tmp/luci-indexcache.*
```

Продолжайте установку после успешной проверки SHA-256. Параметр `--allow-untrusted` разрешает установить локальный APK без подписи доверенного репозитория.

Выберите русский язык в LuCI и заново откройте **VPN → Tailscale**.

## Совместимость

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

## Вопросы

<details>
<summary><strong>Почему часть сообщений может остаться на английском?</strong></summary>

Дополнение переводит настройки страницы и известные сообщения состояния. Новые сообщения, которые пришли от службы Tailscale, сохраняются в исходном виде до добавления перевода. Приложите такой текст к сообщению об ошибке, скрыв личные данные.

</details>

<details>
<summary><strong>Как удалить дополнение?</strong></summary>

Выполните команды на роутере, затем обновите страницу LuCI.

```sh
apk del luci-app-tailscale-community-ru
rm -f /tmp/luci-indexcache.*
```

</details>

## Разработка

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

## Участие в проекте

Нашли неточный перевод или проблему с отображением? Укажите версию OpenWrt, версию Tailscale Community и шаги воспроизведения. Для ошибки оформления приложите снимок экрана и ширину окна. Скройте адреса устройств, ключи и другие личные данные.

**[Создать issue](https://github.com/Ra1nek/tailscale-luci-ru/issues/new)** · **[Предложить правку](CONTRIBUTING.md)**

## Авторы и лицензия

Проект использует интерфейс Tailscale Community и русский перевод nagual2. Перевод дополнен и вычитан, оформление и сообщения состояния объединены в отдельный пакет.

- [Tailscale Community](https://github.com/Tokisaki-Galaxy/luci-app-tailscale-community) — исходное приложение для LuCI.
- [nagual2](https://github.com/nagual2/luci-i18n-tailscale-community-ru) — основа русского перевода.
- [OpenWrt и LuCI](https://github.com/openwrt/luci) — платформа и средства сборки.

Проект распространяется по **Apache-2.0**. Авторство и сведения об изменениях приведены в [NOTICE](NOTICE), полный текст лицензии — в [LICENSE](LICENSE).
