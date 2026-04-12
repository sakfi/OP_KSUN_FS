# WireGuard Kernel Patches for OnePlus (SM8650/SM8750)

This directory contains patches to enable and optimize WireGuard support across all kernel versions.

## Patches included:
1. `0001-Add-WireGuard-source.patch`: Ensures `drivers/net/wireguard` is present and integrated into the Kconfig/Makefile if missing from the vendor tree.
2. `0002-Optimize-NEON-ARM64.patch`: Hardware acceleration for Curve25519 and ChaCha20Poly1305.
3. `0003-Fix-GKI-compatibility.patch`: Exports and internal headers fixes for GKI compliance.

> [!NOTE]
> These patches are applied automatically by the GitHub Actions workflow during the build process.
