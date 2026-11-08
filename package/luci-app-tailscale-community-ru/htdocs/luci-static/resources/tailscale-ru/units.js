(function () {
    'use strict';
    if (document.documentElement.lang !== 'ru' ||
        document.body.dataset.page !== 'admin-vpn-tailscale' ||
        !window.TR || typeof sfh !== 'function' || typeof _ !== 'function')
        return;
    const translations = {
    "minute": _("Tailscale minute"),
    "minutes": _("Tailscale minutes"),
    "hour": _("Tailscale hour"),
    "hours": _("Tailscale hours"),
    "day": _("Tailscale day"),
    "days": _("Tailscale days"),
    "RX": _("Tailscale received data"),
    "TX": _("Tailscale sent data"),
    "Tailscale IP": _("Tailscale device address")
};
    for (const key of Object.keys(translations))
        window.TR[sfh(key)] = translations[key];
})();
