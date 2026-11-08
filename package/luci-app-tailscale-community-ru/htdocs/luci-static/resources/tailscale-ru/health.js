(function () {
    'use strict';
    if (document.documentElement.lang !== 'ru' ||
        document.body.dataset.page !== 'admin-vpn-tailscale' || typeof _ !== 'function')
        return;

    const messages = {
    "Unable to connect to the Tailscale coordination server to synchronize the state of your tailnet. Peer reachability might degrade over time.": _("Unable to connect to the Tailscale coordination server to synchronize the state of your tailnet. Peer reachability might degrade over time."),
    "Unable to connect to the Tailscale coordination server to synchronize the state of the tailnet. Peer reachability might degrade over time.": _("Unable to connect to the Tailscale coordination server to synchronize the state of the tailnet. Peer reachability might degrade over time."),
    "Tailscale is stopped.": _("Tailscale is stopped."),
    "Tailscale is starting. Please wait.": _("Tailscale is starting. Please wait."),
    "You are logged out.": _("You are logged out."),
    "Tailscale cannot connect because the network is down. Check your Internet connection.": _("Tailscale cannot connect because the network is down. Check your Internet connection."),
    "Tailscale could not connect to any relay server. Check your Internet connection.": _("Tailscale could not connect to any relay server. Check your Internet connection."),
    "Tailscale couldn't listen for incoming UDP connections.": _("Tailscale couldn't listen for incoming UDP connections."),
    "Subnet routing is enabled, but IP forwarding is disabled. Check that IP forwarding is enabled on your machine.": _("Subnet routing is enabled, but IP forwarding is disabled. Check that IP forwarding is enabled on your machine.")
};
    function translateHealth() {
        const notification = document.getElementById('tailscale_health_notification');
        if (!notification)
            return;
        const walker = document.createTreeWalker(notification, NodeFilter.SHOW_TEXT);
        let node;
        while ((node = walker.nextNode())) {
            let text = node.nodeValue;
            for (const source of Object.keys(messages))
                text = text.split(source).join(messages[source]);
            if (text !== node.nodeValue)
                node.nodeValue = text;
        }
    }

    const observer = new MutationObserver(function (changes) {
        if (changes.some(function (change) {
            const element = change.target.nodeType === Node.ELEMENT_NODE ? change.target : change.target.parentElement;
            return element && (element.closest('#tailscale_health_notification') ||
                Array.from(change.addedNodes).some(function (node) {
                    return node.nodeType === Node.ELEMENT_NODE &&
                        (node.id === 'tailscale_health_notification' || node.querySelector('#tailscale_health_notification'));
                }));
        }))
            translateHealth();
    });
    observer.observe(document.body, { childList: true, characterData: true, subtree: true });
    translateHealth();
})();
