#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
set -eu
umask 077

VERSION='1.1.0-r2'
PACKAGE="luci-app-tailscale-community-ru-${VERSION}.apk"
SHA256='cbf31bb32a6a8f1ebfd8a05c5974da79d0bca7e1f9307a896dd3adb962067505'
URL='https://api.github.com/repos/Ra1nek/luci-i18n-tailscale-community-ru/releases/assets/723574867?download=1'

fail() {
    printf '%s\n' "$*" >&2
    exit 1
}

[ "$#" -eq 0 ] || fail 'Запустите установщик без дополнительных параметров.'
[ "$(id -u)" -eq 0 ] || fail 'Подключитесь к роутеру под пользователем root.'
[ -r /etc/openwrt_release ] || fail 'Установщик предназначен для OpenWrt 25.12.'
# shellcheck source=/dev/null
. /etc/openwrt_release
case "${DISTRIB_RELEASE:-}" in
    25.12|25.12.*) ;;
    *) fail 'Для этой версии дополнения нужен OpenWrt 25.12.' ;;
esac
command -v apk >/dev/null 2>&1 || fail 'На роутере не найден пакетный менеджер APK.'
command -v sha256sum >/dev/null 2>&1 || fail 'На роутере не найдена команда sha256sum.'

command -v wget >/dev/null 2>&1 || fail 'На роутере не найдена команда wget.'

work_dir=$(mktemp -d /tmp/tailscale-luci-ru.XXXXXX) || fail 'Не удалось создать временную папку.'
cleanup() {
    rm -f "$work_dir/$PACKAGE"
    rmdir "$work_dir" 2>/dev/null || true
}
trap cleanup EXIT
trap 'exit 1' HUP INT TERM

printf 'Скачиваем Tailscale LuCI RU %s…\n' "$VERSION"
wget -T 60 --header='Accept: application/octet-stream' -O "$work_dir/$PACKAGE" "$URL" || \
    fail 'Не удалось скачать пакет. Проверьте подключение к GitHub.'

actual_sha256=$(sha256sum "$work_dir/$PACKAGE")
actual_sha256=${actual_sha256%% *}
[ "$actual_sha256" = "$SHA256" ] || fail 'Скачанный файл не прошёл проверку целостности. Повторите загрузку.'

printf '%s\n' 'Устанавливаем необходимые пакеты…'
apk update || fail 'Не удалось обновить список пакетов OpenWrt.'
apk add luci-app-tailscale-community tailscale luci-base ucode-mod-fs || \
    fail 'Не удалось установить необходимые пакеты OpenWrt.'

printf '%s\n' 'Устанавливаем русский перевод и оформление…'
apk add --allow-untrusted --no-network "$work_dir/$PACKAGE" || \
    fail 'Не удалось установить дополнение. Подробности приведены выше.'

rm -f /tmp/luci-indexcache.*
printf '%s\n' 'Готово. Выберите русский язык в LuCI и откройте VPN → Tailscale.'
