# Установить Tailscale LuCI RU

[← На главную](../README.md)

Нужны OpenWrt **25.12** и приложение **Tailscale Community**. Инструкция рассчитана на пакет **1.1.0-r1**.


## 1. Скачайте пакет

Откройте последнюю успешную сборку ветки `main`. В разделе **Artifacts** скачайте архив **luci-app-tailscale-community-ru-openwrt-25.12.6** и распакуйте его.

**[Открыть сборки и скачать APK →](https://github.com/Ra1nek/tailscale-luci-ru/actions/workflows/build.yml)**

В архиве находятся APK, файл `SHA256SUMS` для проверки загрузки и сведения о сборке.

> [!NOTE]
> Для скачивания артефактов GitHub нужен вход в аккаунт.

## 2. Передайте файлы на роутер

Скопируйте APK и `SHA256SUMS` в `/tmp` на роутере. Например, из папки с распакованным архивом можно выполнить команду ниже. Замените `192.168.1.1` на адрес своего роутера.

```sh
scp -O luci-app-tailscale-community-ru-1.1.0-r1.apk SHA256SUMS root@192.168.1.1:/tmp/
```

## 3. Установите дополнение

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


## Если нужна помощь

Приложите текст ошибки и укажите версию OpenWrt. Перед отправкой скройте адреса устройств и ключи.

[Сообщить об ошибке](https://github.com/Ra1nek/tailscale-luci-ru/issues/new)
