<div align="center">

# 🔥 OP_KSUN_FS 🔥
### *High-Performance Built-in KernelSU-Next & SUSFS LKM Kernels for OnePlus Devices*

[![Build Kernel](https://img.shields.io/github/actions/workflow/status/sakfi/OP_KSUN_FS/build-kernel-release.yml?label=Release%20Builds&style=flat-square&logo=githubactions&logoColor=white)](https://github.com/sakfi/OP_KSUN_FS/actions/workflows/build-kernel-release.yml)
[![GitHub Release](https://flat.badgen.net/github/tag/sakfi/OP_KSUN_FS?label=Latest%20Release&color=00FF99&icon=github)](https://github.com/sakfi/OP_KSUN_FS/releases/latest)
[![AnyKernel3.1](https://img.shields.io/badge/AnyKernel3.1-Custom-blue?style=flat-square&logo=git)](https://github.com/sakfi/AnyKernel3.1)
[![Forks](https://badgen.net/github/forks/sakfi/OP_KSUN_FS?color=orange&style=flat-square)](https://github.com/sakfi/OP_KSUN_FS/network/members)
[![Stars](https://badgen.net/github/stars/sakfi/OP_KSUN_FS?color=yellow&style=flat-square)](https://github.com/sakfi/OP_KSUN_FS/stargazers)

<a href="https://github.com/sakfi/OP_KSUN_FS">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=20&duration=3000&pause=1000&color=00FF99&center=true&vCenter=true&width=620&lines=OnePlus+Kernels+by+SakFi;Built-in+KernelSU-Next+%2B+SUSFS+LKM;Clean+Unpatched+GKI+Core+%28Zero+.rej%29;Battery+Optimization+%2B+Gaming+NTSync;OxygenOS+14+%2F+15+%2F+16+Ready" alt="Typing SVG" />
</a>

<br>

[![KernelSU-Next](https://img.shields.io/badge/KernelSU--Next-Built--in%20GKI-00c853?style=for-the-badge&logo=android)](https://kernelsu-next.github.io/webpage/)
[![SUSFS](https://img.shields.io/badge/SUSFS-LKM%20Via%20Manager-ff6d00?style=for-the-badge&logo=gitlab)](https://github.com/KernelSU-Next/KernelSU-Next)
[![Brand](https://img.shields.io/badge/Branding-SakFi--OP-00b0ff?style=for-the-badge&logo=oneplus)](https://github.com/sakfi/OP_KSUN_FS)
[![Downloads](https://img.shields.io/github/downloads/sakfi/OP_KSUN_FS/total?style=for-the-badge&logo=github&label=Downloads&color=aa00ff)](https://github.com/sakfi/OP_KSUN_FS/releases)

</div>

<div align="center">
  <img src=".github/workflows/split.gif" alt="Divider" width="100%" height="4px" />
</div>

## 📖 Overview

**OP_KSUN_FS** is a modern, enterprise-grade automated CI/CD pipeline engineered to compile, optimize, and package customized Android kernels for **OnePlus devices** running **OxygenOS 14, 15, and 16** (Kernels `5.10`, `5.15`, `6.1`, `6.6`, and `6.12`).

Built around an **In-Tree KernelSU-Next (`CONFIG_KSU=y`) + Modular SUSFS LKM (`susfs_guard_lkm.ko`)** architecture, OP_KSUN_FS delivers out-of-the-box root privileges upon flashing—with zero `init_boot` or `boot` ramdisk patching required—while offloading SUSFS root hiding to KernelSU-Next's native LKM loader. This keeps the core GKI `fs/` and `mm/` trees 100% free of fragile in-tree SUSFS source patches, while packing all custom performance, networking, battery, and gaming features directly into the kernel.

---

## ⚡ What Makes OP_KSUN_FS Different?

```
┌────────────────────────────────────────────────────────────────────────┐
│                        OP_KSUN_FS ARCHITECTURE                         │
├────────────────────────────────┬───────────────────────────────────────┤
│ 1. Core Kernel (Image)         │ Clean GKI with Built-in KSUN, BBRv3,  │
│                                │ HMBird, NTSync, BBG & Battery suite.  │
├────────────────────────────────┼───────────────────────────────────────┤
│ 2. Built-in KernelSU-Next      │ Compiled in-tree (CONFIG_KSU=y) —     │
│                                │ works immediately after flashing ZIP. │
├────────────────────────────────┼───────────────────────────────────────┤
│ 3. SUSFS Guard LKM             │ Enabled directly in KSUN Manager      │
│                                │ settings (susfs_guard_lkm.ko).        │
├────────────────────────────────┼───────────────────────────────────────┤
│ 4. SakFi AnyKernel3.1          │ Custom recovery & flasher installer   │
│                                │ with native SakFi ASCII branding.     │
└────────────────────────────────┴───────────────────────────────────────┘
```

1. **🚀 Built-in KernelSU-Next + Clean GKI Core**:
   - **KernelSU-Next** is compiled directly into the kernel image (`CONFIG_KSU=y`), so root works immediately after flashing the AnyKernel3 ZIP without needing to patch `init_boot` or `boot`.
   - In-tree `simonpunk/susfs4ksu` source patches are intentionally skipped (`"susfs": false`), ensuring the kernel source is never destabilized by upstream sub-level rebase mismatches (such as `6.12.23/38` vs `6.12.92`) and eliminating `.rej` build failures and GitLab 403 rate limits.

2. **🛡️ Native SUSFS LKM Support (One-Click in KSUN Manager)**:
   - Compiled with full GKI loadable module and Kprobes symbol support (`CONFIG_MODULES=y`, `CONFIG_MODVERSIONS=y`, `CONFIG_KALLSYMS_ALL=y`, `CONFIG_KPROBES=y`) and whitelisted against vendor module debloating.
   - After flashing the kernel and rebooting, simply open the **KernelSU-Next Manager** app, go to **Settings**, and toggle **SUSFS** on—`ksud` automatically loads `<kmi>_susfs_guard_lkm.ko` at boot!

3. **🎨 Customized AnyKernel3.1 Packaging**:
   - Powered by our dedicated fork: [**sakfi/AnyKernel3.1**](https://github.com/sakfi/AnyKernel3.1).
   - Custom SakFi ASCII banner displayed natively in recovery consoles (TWRP, OrangeFox) and kernel flashing tools.
   - Real-time cinematic flash logging and `SakFi-OP` kernel `uname` branding.

4. **🔋 Battery Optimization & Performance Suite**:
   - **Wakelock Caps**: 10-second hard safety timeout for noisy background driver wakelocks (`wlan`, `IPA`).
   - **Schedutil & EAS Tuning**: Little-core scheduling preference (80% utilization bias) for cool, efficient daily use.
   - **MGLRU & Memory Reclamation**: Multi-Gen LRU enablement and kswapd dampening to eliminate micro-stutters.
   - **Compile-Level Log Silencing**: Eliminates debug spam, reducing CPU and flash I/O churn.

5. **🎮 Gaming & Networking Enhancements**:
   - **NTSync**: Backported universal NT synchronization driver for zero-overhead Windows gaming emulation via Winlator, Mobox, and Box64.
   - **BBRv3**: Google's BBRv3 TCP congestion control for minimum latency and maximum networking throughput.
   - **WireGuard**: Fast, modern, kernel-space VPN for private and efficient mobile connectivity.

---

<div align="center">
  <img src=".github/workflows/split.gif" alt="Divider" width="100%" height="4px" />
</div>

## ✨ Key Features Matrix

| Category | Feature | Status | Description |
|:---|:---|:---:|:---|
| **Root Solution** | **KernelSU-Next (KSUN)** | ✅ Built-in | In-tree kernel-level root (`CONFIG_KSU=y`) ready right after flash |
| **Stealth** | **SUSFS Guard LKM** | ✅ LKM Ready | Enabled via KSUN Manager settings (`susfs_guard_lkm.ko`) |
| **Core Stability** | **Zero In-Tree SUSFS Patches** | ✅ Clean GKI | Untouched `fs/` & `mm/` core for 100% KMI compatibility across all kernels |
| **Installer** | **SakFi AnyKernel3.1** | ✅ Active | Custom recovery installer with ASCII branding (`SakFi-OP`) |
| **Scheduler** | **HMBIRD SCX** | ✅ Active | OnePlus scheduler extensions for supported Snapdragon/Dimensity devices |
| **Emulation** | **NTSync** | ✅ Active | High-performance fast sync primitives for Windows game emulators |
| **Networking** | **BBRv3** | ✅ Active | Latest TCP congestion control for low-latency network traffic |
| **Networking** | **WireGuard** | ✅ Active | In-kernel encrypted VPN subsystem |
| **Networking** | **TTL / IP Set** | ✅ Active | Packet mangling and advanced firewall capabilities |
| **Power** | **Battery Optimization** | ✅ Active | Schedutil tuning, wakelock hard-caps, and MGLRU dynamic memory |
| **Hardening** | **BBG Security** | ✅ Active | LSM-based Baseband Guard security whitelist |
| **Hardening** | **Unicode Bypass Fix** | ✅ Active | Prevents path traversal via non-printable Unicode codepoints |
| **Containers** | **Droidspaces** | ✅ Active | Kernel support (`SYSVIPC`, `USER_NS`, `MACVLAN`) for Linux containers |

<br>

<details>
<summary><b>🔍 Expand SUSFS LKM Stealth Capabilities</b></summary>

- `SUS_PATH` - Hide files, directories, and sensitive system artifacts
- `SUS_MOUNT` - Mask overlayfs, tmpfs, and root injection mounts
- `SUS_KSTAT` - Spoof file attributes, modification timestamps, and stat info
- `SUS_MAP` - Hide loaded library maps and executable memory regions
- `SPOOF_UNAME` - Custom branded uname identification (`SakFi-OP`)
- `SPOOF_CMDLINE` - Conceal boot parameters and root indicators
- `OPEN_REDIRECT` - Intercept and redirect file descriptor access
- `AVC_SPOOF` - Suppress SELinux audit vector logs
</details>

---

<div align="center">
  <img src=".github/workflows/split.gif" alt="Divider" width="100%" height="4px" />
</div>

## 📱 Supported Devices & OxygenOS Versions

Configurations are maintained under [`configs/`](./configs/). Build manifests support all modern OnePlus devices:

| OxygenOS Version | Linux Kernel | Supported Platforms / Devices |
|:---:|:---:|:---|
| **OOS 14** | `5.10` / `5.15` / `6.1` | OnePlus 10 Pro, 10R, 10T, 11, 11R, 12, 12R, Pad, Ace Series |
| **OOS 15** | `5.10` / `5.15` / `6.1` / `6.6` | OnePlus 11, 12, 12R, 13, 13R, 13T, Open, Ace 2/3/5 Series, Nord 3/4/5 |
| **OOS 16** | `5.15` / `6.1` / `6.6` / `6.12` | OnePlus 11, 12, 13, 13R, 13S, 13T, 15, 15R, 15T, N6, N6X, Nord CE6, Turbo 6 Series, Ace 5/6 Series, Pad 2/3/4 Pro |

---

<div align="center">
  <img src=".github/workflows/split.gif" alt="Divider" width="100%" height="4px" />
</div>

## 📥 Installation Instructions

### 🛠️ Prerequisites
- Unlocked bootloader on your OnePlus device.
- Recommended flashing utility: [**Kernel Flasher**](https://github.com/fatalcoder524/KernelFlasher), [**Horizon Kernel Flasher**](https://github.com/libxzr/HorizonKernelFlasher), or the built-in flasher in **KernelSU-Next Manager**.
- A backup of your stock `boot.img` stored safely.

---

### 📲 Flashing Procedure

1. **Download the Flashable ZIP**:
   Grab the appropriate zip for your device model and OS version from [**GitHub Releases**](https://github.com/sakfi/OP_KSUN_FS/releases).
   ```
   Package Naming Convention:
   SKF_{MODEL}_{OS_VER}_{KERNEL_VER}_{KSU_TYPE}_{KSU_VER}.zip
   ```

2. **Flash via Kernel Flasher or Custom Recovery**:
   - Open **Kernel Flasher** (or boot into **TWRP / OrangeFox**).
   - Select the downloaded `SKF_*.zip` file and flash it.

3. **Reboot**:
   - Reboot your device normally. Built-in **KernelSU-Next** will be active immediately on boot.

4. **Enable SUSFS LKM in Manager**:
   - Install or open the **KernelSU-Next Manager** APK from [KernelSU-Next Releases](https://github.com/KernelSU-Next/KernelSU-Next/releases).
   - Navigate to **Settings** inside the Manager app and **enable SUSFS** (LKM).
   - Enjoy built-in KernelSU-Next root with modular SUSFS stealth protection!

---

<div align="center">
  <img src=".github/workflows/split.gif" alt="Divider" width="100%" height="4px" />
</div>

## ⚠️ Disclaimer

```
Your warranty is now void. You are proceeding entirely at your own risk.
```
- Modifying your Android kernel can cause bootloops, device bricks, or loss of data if flashed onto incompatible firmware.
- Always ensure that your active OxygenOS version and kernel sub-version match the release package you download.
- The authors and maintainers of this repository take **no responsibility** for damaged hardware, bootloops, or lost data.

---

<div align="center">
  <img src=".github/workflows/split.gif" alt="Divider" width="100%" height="4px" />
</div>

## 🌟 Special Thanks & Credits

Heartfelt gratitude to the outstanding developers and projects whose open-source work made this kernel possible:

<div align="center">

| Project / Component | Author / Maintainer | Upstream Link |
|:---|:---|:---:|
| **AnyKernel3 & Recovery Tools** | **osm0sis** | [![XDA](https://img.shields.io/badge/XDA-osm0sis-orange?style=flat-square)](https://xdaforums.com/m/osm0sis.4544860/) |
| **Original OnePlus Pipeline** | **fatalcoder524** | [![GitHub](https://img.shields.io/badge/GitHub-fatalcoder524-blue?style=flat-square&logo=github)](https://github.com/fatalcoder524) |
| **KernelSU-Next** | **rifsxd** | [![GitHub](https://img.shields.io/badge/GitHub-rifsxd-blue?style=flat-square&logo=github)](https://github.com/KernelSU-Next/KernelSU-Next) |
| **SUSFS (Root Hiding)** | **simonpunk** | [![GitLab](https://img.shields.io/badge/GitLab-simonpunk-orange?style=flat-square&logo=gitlab)](https://gitlab.com/simonpunk/susfs4ksu) |
| **SUSFS KSU Module** | **sidex15** | [![GitHub](https://img.shields.io/badge/GitHub-sidex15-blue?style=flat-square&logo=github)](https://github.com/sidex15) |
| **Droidspaces** | **ravindu644** | [![GitHub](https://img.shields.io/badge/GitHub-ravindu644-blue?style=flat-square&logo=github)](https://github.com/ravindu644/Droidspaces-OSS) |

</div>

---

<div align="center">
  <img src=".github/workflows/split.gif" alt="Divider" width="100%" height="4px" />
</div>

## 💬 Community & Support

Have questions, suggestions, or encountered a bug?
- 🐛 **Issue Tracker**: Open an issue on [GitHub Issues](https://github.com/sakfi/OP_KSUN_FS/issues)
- 💬 **Telegram Channel**: Join the discussion on [t.me/SakFi](https://t.me/SakFi)

<div align="center">

[![Telegram](https://img.shields.io/badge/Telegram-SakFi-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/SakFi)
[![GitHub](https://img.shields.io/badge/GitHub-SakFi-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sakfi)

<br>

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=sakfi&label=Profile%20Views&color=00FF99&style=for-the-badge" alt="sakfi profile views" />
</p>

</div>
