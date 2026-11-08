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
  <a href="#что-меняется">Возможности</a> ·
  <a href="#совместимость">Совместимость</a> ·
  <a href="#структура-проекта">Структура проекта</a> ·
  <a href="https://github.com/Ra1nek/tailscale-luci-ru/issues">Сообщить об ошибке</a>
</p>

---

## Что меняется

| Компонент интерфейса | Что меняется для пользователя |
| :--- | :--- |
| 🌐 **Настройки сети и устройств** | Русские названия и пояснения помогают настроить подключение, доступ к домашней сети и выход в интернет через Tailscale. |
| 📱 **Оформление LuCI** | Исправлены переносы текста, расположение статусов, размеры кнопок и заголовки таблицы устройств. |
| 💬 **Уведомления** | Известные сообщения о состоянии службы и подключении переведены на русский. |
| 📦 **Установка** | Перевод и оформление устанавливаются одним пакетом. |

Дополнение применяется к русской странице Tailscale и использует исходное приложение Tailscale Community.

## Совместимость

Нужны **OpenWrt 25.12** с пакетным менеджером APK и приложение **Tailscale Community** (`luci-app-tailscale-community`). Пакет подходит для разных процессоров.

## Установка

### 1. Скачайте пакет

Скачайте APK из выпуска **1.1.0-r1** и сохраните его в отдельную папку.

**[Скачать APK →](https://github.com/Ra1nek/tailscale-luci-ru/releases/download/v1.1.0-r1/luci-app-tailscale-community-ru-1.1.0-r1.apk)** · [Все выпуски](https://github.com/Ra1nek/tailscale-luci-ru/releases)

### 2. Передайте пакет на роутер

Откройте терминал в папке со скачанным APK и выполните команду. Замените `192.168.1.1` на адрес своего роутера.

```sh
scp -O luci-app-tailscale-community-ru-1.1.0-r1.apk root@192.168.1.1:/tmp/
```

### 3. Установите дополнение

Подключитесь к роутеру по SSH.

```sh
ssh root@192.168.1.1
```

Выполните команду установки.

```sh
apk update && apk add luci-app-tailscale-community tailscale && apk add --allow-untrusted /tmp/luci-app-tailscale-community-ru-1.1.0-r1.apk && rm -f /tmp/luci-indexcache.*
```

После установки выберите **русский язык в LuCI** и откройте **VPN → Tailscale**.

<details>
<summary><strong>Удаление дополнения</strong></summary>

Выполните на роутере и обновите страницу браузера.

```sh
apk del luci-app-tailscale-community-ru && rm -f /tmp/luci-indexcache.*
```

</details>

## Структура проекта

Перевод и оформление объединены в одном пакете. Репозиторий организован как feed для стандартной сборки OpenWrt.

```text
tailscale-luci-ru/
├── package/
│   └── luci-app-tailscale-community-ru/
│       ├── Makefile             Сборка пакета
│       ├── htdocs/              Оформление и уведомления
│       ├── po/ru/               Русский перевод
│       └── root/                Подключение к LuCI
├── .github/workflows/           Автоматическая сборка
├── scripts/                     Сценарии сборки
├── tests/                       Проверка перевода
├── NOTICE                       Авторы и источники
└── LICENSE                      Лицензия Apache-2.0
```

## Часто задаваемые вопросы

### Зачем нужен `--allow-untrusted`?

APK собирается в GitHub Actions и распространяется отдельным файлом. Пакетный менеджер роутера не может подтвердить его через доверенный репозиторий и требует явно разрешить установку.

Скачивайте пакет со страницы выпуска этого проекта. Рядом с APK доступен файл `SHA256SUMS` для проверки целостности загрузки.

### Дополнение изменяет исходное приложение?

Оно добавляет собственный перевод, стили и шаблон страницы, который открывает штатный интерфейс Tailscale Community. Исходные файлы приложения сохраняются.

После обновления Tailscale Community оформление и перевод могут потребовать доработки, если автор изменит страницу.

### Что делать, если интерфейс сразу не обновился?

Обновите страницу с очисткой кэша браузера. Убедитесь, что в LuCI выбран русский язык.

Если прежнее оформление осталось, выполните на роутере и откройте страницу заново.

```sh
rm -f /tmp/luci-indexcache.*
```

### Почему сообщение осталось на английском?

Перевод охватывает известные уведомления. Новое сообщение службы Tailscale может появиться раньше его перевода. Пришлите его текст через Issues, скрыв личные данные.

## Помощь и участие

Нашли неточный перевод или проблему с отображением? Создайте issue и приложите необходимую информацию.

- Версия OpenWrt и Tailscale Community.
- Что вы делали и какой результат ожидали.
- Снимок экрана для проблемы оформления.
- Устройство и браузер, на которых возникла ошибка.

Перед публикацией скройте адреса устройств, ключи и другие личные данные.

**[Сообщить об ошибке →](https://github.com/Ra1nek/tailscale-luci-ru/issues/new)** · **[Предложить улучшение →](https://github.com/Ra1nek/tailscale-luci-ru/issues/new)**

## Авторы и благодарности

Проект создан благодаря работе авторов открытых компонентов.

| Проект | Вклад |
| :--- | :--- |
| [Tailscale Community](https://github.com/Tokisaki-Galaxy/luci-app-tailscale-community) | Исходное приложение управления Tailscale в LuCI |
| [Русский перевод nagual2](https://github.com/nagual2/luci-i18n-tailscale-community-ru) | Основа русского перевода |
| [OpenWrt LuCI](https://github.com/openwrt/luci) | Веб-интерфейс OpenWrt и средства разработки |
| [Ra1nek](https://github.com/Ra1nek) | Доработка перевода, оформление и объединение компонентов |

Спасибо всем, кто сообщает об ошибках, предлагает формулировки и помогает улучшать интерфейс.

## Лицензия

Проект распространяется по **Apache-2.0**. Сведения об авторах и происхождении компонентов сохранены в [NOTICE](NOTICE). Полный текст условий доступен в [LICENSE](LICENSE).
