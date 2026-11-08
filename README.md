<h1 align="center">Tailscale LuCI RU</h1>

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="docs/assets/overview-dark-mobile.svg">
  <source media="(max-width: 600px)" srcset="docs/assets/overview-light-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/overview-dark.svg">
  <img src="docs/assets/overview-light.svg" alt="Tailscale по-русски. Настройки, понятные уведомления и удобная страница на телефоне и компьютере." width="1280">
</picture>

<p align="center">
  Русский перевод и оформление Tailscale Community для OpenWrt.<br>
  Всё в одном дополнении.
</p>

<p align="center">
  <strong><a href="https://github.com/Ra1nek/tailscale-luci-ru/actions/workflows/build.yml">Получить пакет →</a></strong> ·
  <a href="docs/INSTALL.md">Как установить</a> ·
  <a href="https://github.com/Ra1nek/tailscale-luci-ru/issues">Помощь</a>
</p>

## Три шага до русской страницы

```mermaid
flowchart LR
    A["Скачайте дополнение"] --> B["Установите на роутер"]
    B --> C["Откройте Tailscale на русском"]
    classDef step fill:#edf4ff,stroke:#5185e7,color:#142b50,rx:12,ry:12
    class A,B,C step
```

1. **Получите пакет.** Откройте последнюю успешную сборку ветки `main` и скачайте архив в разделе **Artifacts**. Для скачивания нужен вход в GitHub.
2. **Установите дополнение.** Передайте файл на роутер и выполните команды из [пошаговой инструкции](docs/INSTALL.md).
3. **Откройте страницу.** Выберите русский язык в LuCI и перейдите в **VPN → Tailscale**.

## Подойдёт ли моему роутеру?

Дополнение рассчитано на **OpenWrt 25.12** и приложение **Tailscale Community**. Перевод и оформление устанавливаются вместе. Пакет подходит для разных процессоров.

<details>
<summary><strong>Совместимость и текущая проверка</strong></summary>

Нужно приложение `luci-app-tailscale-community`. Единый пакет прошёл сборку SDK и автоматические проверки. Оформление проверялось со страницей Tailscale Community **4.5.1-r1** при разработке исходных дополнений. Отдельная проверка объединённой установки в браузере ещё предстоит.

[Подробности совместимости и проверки](docs/DEVELOPMENT.md#проверенные-версии)

</details>

## Нужна помощь?

Нашли неточный перевод или заметили, что страница отображается неправильно? Приложите снимок экрана и укажите версии OpenWrt и Tailscale Community. Скройте адреса устройств и ключи.

**[Сообщить об ошибке →](https://github.com/Ra1nek/tailscale-luci-ru/issues/new)**

<details>
<summary><strong>Почему уведомление осталось на английском?</strong></summary>

Дополнение переводит известные сообщения состояния. Новое сообщение от Tailscale может появиться раньше его перевода. Пришлите текст — его можно будет добавить в следующую версию.

</details>

---

<p align="center">
  <strong>Создано на основе открытых проектов</strong><br>
  <a href="https://github.com/Tokisaki-Galaxy/luci-app-tailscale-community">Tailscale Community</a> ·
  <a href="https://github.com/nagual2/luci-i18n-tailscale-community-ru">Русский перевод nagual2</a> ·
  <a href="https://github.com/openwrt/luci">OpenWrt LuCI</a>
</p>

<p align="center">
  <a href="CONTRIBUTING.md">Предложить улучшение</a> ·
  <a href="docs/DEVELOPMENT.md">Для разработчиков</a> ·
  <a href="NOTICE">Авторство</a> ·
  <a href="LICENSE">Apache-2.0</a>
</p>

<p align="center">
  <a href="https://github.com/Ra1nek/tailscale-luci-ru/actions/workflows/build.yml"><img src="https://github.com/Ra1nek/tailscale-luci-ru/actions/workflows/build.yml/badge.svg?branch=main" alt="Статус сборки"></a>
</p>
