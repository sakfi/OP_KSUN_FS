# oplus-sukisu_kernel

OnePlus GKI kernels built in CI with [SukiSU-Ultra](https://github.com/SukiSU-Ultra/SukiSU-Ultra) (SUSFS integrated) instead of KernelSU-Next. Fork of [sakfi/OP_KSUN_FS](https://github.com/sakfi/OP_KSUN_FS), kept in sync with upstream.

No local toolchain needed: pick your device in GitHub Actions, and the kernel is compiled, patched and packaged as a flashable AnyKernel3 zip.

---

### Table of Contents

- [Building the kernel](#building-the-kernel)
- [What's inside](#whats-inside)
- [Supported devices](#supported-devices)
- [Flashing](#flashing)
- [Notes](#notes)
- [Credits](#credits)

---

## Building the kernel

1. Open the [Actions tab](https://github.com/Unnidentified/oplus-sukisu_kernel/actions) and run the **Build Kernel** workflow.
2. Pick your device. For a OnePlus 15: `op_model: OP15`, `android_version_filter: A16`, `kernel_version_filter: android16-6.12`.
3. Leave the root options at their defaults unless you know what you are doing:

| Input | Default | Meaning |
|---|---|---|
| `ksu_options` | `[{"type":"ksun","hash":"builtin"}]` | SukiSU-Ultra `builtin` branch (the only line with in-kernel `KSU_SUSFS`; `main`/`dev` ship SUSFS as a userspace extension shim only) |
| `ksu_mode` | `builtin` | `builtin` compiles SukiSU into the kernel (recommended, full SUSFS support); `lkm` downloads a prebuilt `kernelsu.ko` and injects it into the ramdisk at flash time |

4. When the run finishes, grab the `SKF_*.zip` from [Releases](https://github.com/Unnidentified/oplus-sukisu_kernel/releases) or the run's artifacts.

Zip names follow `SKF_{MODEL}_{OS}_{KERNEL}_{KSU_TYPE}_{VERSION}_SuSFS[_LKM].zip`, e.g. `SKF_OP15_A16_6.12.x_KSUN_41140_SuSFS_v2.3.0.zip` for builtin builds.

---

## What's inside

| Area | Feature | Notes |
|---|---|---|
| Root | **SukiSU-Ultra** (`builtin` branch) | KernelSU-Next fork with SUSFS hooks already integrated — no extra KSU patching needed. Manager APK from [SukiSU-Ultra releases](https://github.com/SukiSU-Ultra/SukiSU-Ultra/releases). The build carries small compat patches (6.7+ `struct lsm_id` LSM registration, SUSFS priority-filter guards) under `.github/actions/build-kernel/patches/` |
| Stealth | **SUSFS** | Magic mount, `SUS_PATH` / `SUS_MOUNT` / `SUS_KSTAT` / `SUS_MAP`, uname & cmdline spoofing, open redirect. Branch auto-synced from [susfs4ksu](https://gitlab.com/simonpunk/susfs4ksu) |
| Gaming | **NTSync** | NT synchronization primitives for Windows emulators (Winlator, Box64) |
| Network | **BBR**, **WireGuard**, TTL / IP Set | Congestion control, in-kernel VPN, packet tools |
| Power | **Battery suite** | Wakelock hard caps, schedutil tuning, MGLRU, log silencing |
| Containers | **Droidspaces** | SYSVIPC support for portable Linux containers |
| Misc | HMBIRD SCX, LTO, TMPFS xattr, Unicode bypass fix | Toggled per device in `configs/` |

The OnePlus 15 profile (`configs/a16/OP15.json`) is `android16` / `6.12` (`canoe`) with SUSFS and HMBIRD on, and BBG off — this fork keeps Baseband Guard disabled on the OP15 so the EFS/bootloader mod keeps working.

---

## Supported devices

Per-device configs live in [`configs/`](configs), kernel source manifests in [`manifests/`](manifests):

| OxygenOS | Kernel | Devices |
|---|---|---|
| OOS 14 | 5.10 / 5.15 / 6.1 | OnePlus 10 Pro, 10T, 11, 11R, 12, 12R, Pad, Ace series |
| OOS 15 | 5.15 / 6.1 / 6.6 | OnePlus 12, 12R, 13, 13S, Open, Ace 3/5, Nord 4/5 |
| OOS 16 | 6.1 / 6.6 / 6.12 | OnePlus 13, 13S, 15, 15R, 15T, Ace 6, Turbo 6, Pad 2/3/4 |

Everything is built from [OnePlus's official kernel sources](https://github.com/OnePlusOSS/), so the zips target stock ROMs. Don't flash a zip across a major OTA (e.g. A15 to A16) without checking — the KMI has to match.

---

## Flashing

1. Unlock the bootloader and back up your stock `boot` / `init_boot` image.
2. Flash the `SKF_*.zip` with [Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher), [Horizon Kernel Flasher](https://github.com/libxzr/HorizonKernelFlasher), or a custom recovery. In `lkm` mode the installer patches the ramdisk on-device via `ksud boot-patch`.
3. Reboot, then install the SukiSU-Ultra manager APK.

---

## Notes

> [!WARNING]
> Flashing a custom kernel can brick your device or wipe data. Match the zip to your exact model and OxygenOS build, and keep a stock boot image around for recovery. The maintainers are not responsible for any damage.

On non-OnePlus devices, pick the config whose `androidXX-YY.ZZ` KMI matches yours (see the [KernelSU KMI guide](https://kernelsu.org/guide/installation.html#kmi)) and disable dm-verity first.

---

## Credits

| Project | Author | Link |
|---|---|---|
| Upstream pipeline (OP_KSUN_FS) | sakfi | [github.com/sakfi/OP_KSUN_FS](https://github.com/sakfi/OP_KSUN_FS) |
| Original OnePlus kernel CI | fatalcoder524 | [github.com/fatalcoder524](https://github.com/fatalcoder524) |
| SukiSU-Ultra (KernelSU-Next fork) | SukiSU-Ultra | [github.com/SukiSU-Ultra/SukiSU-Ultra](https://github.com/SukiSU-Ultra/SukiSU-Ultra) |
| KernelSU-Next | rifsxd | [github.com/KernelSU-Next/KernelSU-Next](https://github.com/KernelSU-Next/KernelSU-Next) |
| SUSFS | simonpunk | [gitlab.com/simonpunk/susfs4ksu](https://gitlab.com/simonpunk/susfs4ksu) |
| SUSFS module | sidex15 | [github.com/sidex15/ksu_module_susfs](https://github.com/sidex15/ksu_module_susfs) |
| AnyKernel3 | osm0sis | [github.com/osm0sis/AnyKernel3](https://github.com/osm0sis/AnyKernel3) |
