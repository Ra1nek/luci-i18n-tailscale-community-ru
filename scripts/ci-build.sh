#!/usr/bin/env bash
set -euo pipefail

readonly package_name=luci-app-tailscale-community-ru
readonly sdk_version=25.12.6
readonly sdk_archive=openwrt-sdk-25.12.6-x86-64_gcc-14.3.0_musl.Linux-x86_64.tar.zst
readonly sdk_sha256=1864152619092e781fa36a401960c8e9ae42d6a364c44ee5f0b197ca5f3c0fcc
readonly sdk_url="https://downloads.openwrt.org/releases/${sdk_version}/targets/x86/64/${sdk_archive}"
readonly source_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
readonly work_dir="${SDK_WORKDIR:-$(mktemp -d -t tailscale-ru-sdk.XXXXXXXX)}"
readonly artifacts_dir="${ARTIFACTS_DIR:-${source_dir}/artifacts}"

if [[ ${EUID} -eq 0 ]]; then
	printf '%s\n' 'Run the OpenWrt SDK as a regular user.' >&2
	exit 1
fi

if [[ "${source_dir}" == *' '* ]]; then
	printf '%s\n' 'The OpenWrt feed path must not contain spaces. Copy this repository to a path without spaces.' >&2
	exit 1
fi

mkdir -p "${work_dir}" "${artifacts_dir}"
exec > >(tee "${artifacts_dir}/sdk-build.log") 2>&1

curl --fail --location --retry 3 --connect-timeout 20 \
	--output "${work_dir}/${sdk_archive}" "${sdk_url}"
printf '%s  %s\n' "${sdk_sha256}" "${work_dir}/${sdk_archive}" | sha256sum --check -
mkdir -p "${work_dir}/sdk"
tar --zstd --extract --file "${work_dir}/${sdk_archive}" \
	--directory "${work_dir}/sdk" --strip-components=1
cd "${work_dir}/sdk"

# Match the feeds used for the official 25.12.6 release.
cat > feeds.conf <<EOF
src-git packages https://github.com/openwrt/packages.git^093d551675b1119a06ef224d419905e8d6b2af1a
src-git luci https://github.com/openwrt/luci.git^75a306df84a020c57a631ef5b4c02ace56d93387
src-link tailscale_ru ${source_dir}
EOF

./scripts/feeds update -a
./scripts/feeds install -p tailscale_ru "${package_name}"

cat > .config <<EOF
CONFIG_ALL_NONSHARED=n
CONFIG_ALL_KMODS=n
CONFIG_ALL=n
CONFIG_PACKAGE_${package_name}=m
EOF
make defconfig
grep --fixed-strings --line-regexp "CONFIG_PACKAGE_${package_name}=m" .config
# Only po2lmo is needed to build this architecture-independent add-on.
# Runtime dependencies stay in APK metadata and come from OpenWrt feeds.
make --jobs "$(nproc)" package/luci-base/host/compile V=s
test -x staging_dir/hostpkg/bin/po2lmo
make --jobs "$(nproc)" "package/${package_name}/compile" V=s NO_DEPS=1

mapfile -d '' built_packages < <(find bin/packages -type f -name "${package_name}-*.apk" -print0)
if [[ ${#built_packages[@]} -ne 1 ]]; then
	printf 'Expected one %s APK, found %s.\n' "${package_name}" "${#built_packages[@]}" >&2
	exit 1
fi
cp -- "${built_packages[0]}" "${artifacts_dir}/"
(
	cd "${artifacts_dir}"
	sha256sum -- "$(basename -- "${built_packages[0]}")" > SHA256SUMS
)

{
	printf 'OpenWrt SDK %s\nSDK SHA256 %s\n' "${sdk_version}" "${sdk_sha256}"
	printf 'Source commit %s\n' "$(git -C "${source_dir}" rev-parse HEAD)"
	printf 'packages feed %s\n' "$(git -C feeds/packages rev-parse HEAD)"
	printf 'luci feed %s\n' "$(git -C feeds/luci rev-parse HEAD)"
} > "${artifacts_dir}/build-info.txt"
