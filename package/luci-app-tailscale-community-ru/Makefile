# SPDX-License-Identifier: Apache-2.0

include $(TOPDIR)/rules.mk

PKG_NAME:=luci-app-tailscale-community-ru
PKG_VERSION:=1.1.0
PKG_RELEASE:=1
PKG_LICENSE:=Apache-2.0
PKG_LICENSE_FILES:=LICENSE
PKG_MAINTAINER:=Ra1nek
PKG_BUILD_DEPENDS:=luci-base/host
PKG_BUILD_PARALLEL:=1

LUCI_TITLE:=Russian language and layout for Tailscale Community
LUCI_DEPENDS:=+luci-app-tailscale-community +tailscale +luci-base +ucode-mod-fs
LUCI_PKGARCH:=all

include $(INCLUDE_DIR)/package.mk

define Package/$(PKG_NAME)
  SECTION:=luci
  CATEGORY:=LuCI
  SUBMENU:=3. Applications
  TITLE:=$(LUCI_TITLE)
  DEPENDS:=$(LUCI_DEPENDS)
  PKGARCH:=$(LUCI_PKGARCH)
endef

define Package/$(PKG_NAME)/description
 Russian translations and scoped layout adjustments for the Tailscale
 Community LuCI application, including known service status messages.
endef

define Build/Prepare
	$(INSTALL_DIR) $(PKG_BUILD_DIR)/po/ru
	$(CP) ./po/ru/tailscale.po $(PKG_BUILD_DIR)/po/ru/
	$(CP) ./LICENSE $(PKG_BUILD_DIR)/LICENSE
endef

define Build/Configure
endef

define Build/Compile
	$(STAGING_DIR_HOSTPKG)/bin/po2lmo \
		$(PKG_BUILD_DIR)/po/ru/tailscale.po \
		$(PKG_BUILD_DIR)/tailscale.ru.lmo
endef

define Package/$(PKG_NAME)/install
	$(INSTALL_DIR) $(1)/www $(1)/usr/lib/lua/luci/i18n
	$(CP) ./htdocs/. $(1)/www/
	$(CP) ./root/. $(1)/
	$(INSTALL_DATA) $(PKG_BUILD_DIR)/tailscale.ru.lmo \
		$(1)/usr/lib/lua/luci/i18n/tailscale.ru.lmo
endef

$(eval $(call BuildPackage,$(PKG_NAME)))
