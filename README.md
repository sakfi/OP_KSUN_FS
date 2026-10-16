<div align="center">

# 🔥 OP_KSUN_FS 🔥
### *High-Performance Hybrid LKM & SUSFS Kernels for OnePlus Devices*

[![Build Kernel](https://img.shields.io/github/actions/workflow/status/sakfi/OP_KSUN_FS/build-kernel-release.yml?label=Release%20Builds&style=flat-square&logo=githubactions&logoColor=white)](https://github.com/sakfi/OP_KSUN_FS/actions/workflows/build-kernel-release.yml)
[![GitHub Release](https://img.shields.io/github/v/release/sakfi/OP_KSUN_FS?label=Latest%20Release&color=00FF99&style=flat-square&logo=github)](https://github.com/sakfi/OP_KSUN_FS/releases/latest)
[![AnyKernel3.1](https://img.shields.io/badge/AnyKernel3.1-SakFi%20Custom-blue?style=flat-square&logo=git)](https://github.com/sakfi/AnyKernel3.1)
[![Forks](https://badgen.net/github/forks/sakfi/OP_KSUN_FS?color=orange&style=flat-square)](https://github.com/sakfi/OP_KSUN_FS/network/members)
[![Stars](https://badgen.net/github/stars/sakfi/OP_KSUN_FS?color=yellow&style=flat-square)](https://github.com/sakfi/OP_KSUN_FS/stargazers)

<a href="https://github.com/sakfi/OP_KSUN_FS">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=20&duration=3000&pause=1000&color=00FF99&center=true&vCenter=true&width=620&lines=OnePlus+Kernels+by+SakFi;Hybrid+LKM+%2B+SUSFS+v2.2.0%2B;Automated+On-Device+Ramdisk+Patching;Battery+Optimization+%2B+Gaming+NTSync;OxygenOS+14+%2F+15+%2F+16+Ready" alt="Typing SVG" />
</a>

<br>

[![KernelSU-Next](https://img.shields.io/badge/KernelSU--Next-Hybrid%20LKM%20%7C%20Built--in-00c853?style=for-the-badge&logo=android)](https://kernelsu-next.github.io/webpage/)
[![SUSFS](https://img.shields.io/badge/SUSFS-v2.2.0%2B%20Patched-ff6d00?style=for-the-badge&logo=gitlab)](https://gitlab.com/simonpunk/susfs4ksu)
[![Brand](https://img.shields.io/badge/Branding-SakFi--OP-00b0ff?style=for-the-badge&logo=oneplus)](https://github.com/sakfi/OP_KSUN_FS)

</div>

<div align="center">
  <img src=".github/workflows/split.gif" alt="Divider" width="100%" height="4px" />
</div>

## 📖 Overview

**OP_KSUN_FS** is a modern, enterprise-grade automated CI/CD pipeline engineered to compile, optimize, and package customized Android kernels for **OnePlus devices** running **OxygenOS 14, 15, and 16** (Kernels `5.10`, `5.15`, `6.1`, `6.6`, and `6.12`).

Built with a **Hybrid LKM (Loadable Kernel Module)** architecture, OP_KSUN_FS seamlessly combines non-intrusive modular root injection with deep kernel-level stealth root hiding (**SUSFS**), cutting-edge battery life tunables, and Windows game emulation synchronization primitives (**NTSync**).

---

## ⚡ What Makes OP_KSUN_FS Different?

```
┌────────────────────────────────────────────────────────────────────────┐
│                        OP_KSUN_FS ARCHITECTURE                         │
├────────────────────────────────┬───────────────────────────────────────┤
│ 1. Core Kernel (Image)         │ Clean, hardened GKI with SUSFS hooks, │
│                                │ BBRv3, NTSync, and Battery suite.     │
├────────────────────────────────┼───────────────────────────────────────┤
│ 2. Hybrid LKM (kernelsu.ko)    │ Root logic compiled as standalone     │
│                                │ module, completely out-of-tree.       │
├────────────────────────────────┼───────────────────────────────────────┤
│ 3. SUSFS Guard Module          │ Runtime root mount and trace shield   │
│                                │ protection (susfs_guard_lkm.ko).      │
├────────────────────────────────┼───────────────────────────────────────┤
│ 4. SakFi AnyKernel3.1          │ Recovery installer with built-in      │
│                                │ 'ksud boot-patch' ramdisk injection.  │
└────────────────────────────────┴───────────────────────────────────────┘
```

1. **🚀 Modular Hybrid LKM Architecture**:
   - Rather than forcing in-tree modifications that can destabilize vendor drivers, KernelSU-Next is compiled as a dedicated kernel module (`kernelsu.ko`).
   - The installer automatically patches the device ramdisk (`init_boot` or `boot`) on-the-fly during flash via an integrated `ksud boot-patch` routine.
   - Dual-mode support: Choose between **Modular LKM** (`ksu_mode: lkm`, default) or traditional **In-Tree Builtin** (`ksu_mode: builtin`).

2. **🛡️ Advanced Stealth with SUSFS v2.2.0+**:
   - Fully patched with Simonpunk's SUSFS for deep hide capabilities: `SUS_PATH`, `SUS_MOUNT`, `SUS_KSTAT`, `SUS_MAP`, `SPOOF_UNAME`, `SPOOF_CMDLINE`, `OPEN_REDIRECT`, and `AVC_SPOOF`.
   - Bundled with a specialized **SUSFS Guard** module to prevent detection across banking apps, enterprise apps, and Google Play Protect.
   - Multi-tier resilient GitLab API fetching ensures CI builds never fail due to network blips.

3. **🎨 Customized AnyKernel3.1 Packaging**:
   - Powered by our dedicated fork: [**sakfi/AnyKernel3.1**](https://github.com/sakfi/AnyKernel3.1).
   - Custom SakFi ASCII banner displayed natively in recovery consoles (TWRP, OrangeFox) and kernel flashing tools.
   - Real-time cinematic flash logging with module verification indicators and upstream credits.

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
| **Root Solution** | **KernelSU-Next (KSUN)** | ✅ Active | Next-generation kernel-level root with manual hook support |
| **Root Solution** | **Hybrid LKM Mode** | ✅ Active | Out-of-tree modular loading with automated ramdisk injection |
| **Stealth** | **SUSFS v2.2.0+** | ✅ Active | Magic Mount hiding, open redirection, and inode/kstat spoofing |
| **Stealth** | **SUSFS Guard LKM** | ✅ Active | Staged mount shield preventing root footprint leaks |
| **Installer** | **SakFi AnyKernel3.1** | ✅ Active | Custom recovery installer with ASCII branding & boot patcher |
| **Emulation** | **NTSync** | ✅ Active | High-performance fast sync primitives for Windows game emulators |
| **Networking** | **BBRv3** | ✅ Active | Latest TCP congestion control for low-latency network traffic |
| **Networking** | **WireGuard** | ✅ Active | In-kernel encrypted VPN subsystem |
| **Networking** | **TTL / IP Set** | ✅ Active | Packet mangling and advanced firewall capabilities |
| **Power** | **Battery Optimization** | ✅ Active | Schedutil tuning, wakelock hard-caps, and MGLRU dynamic memory |
| **Hardening** | **BBG Security** | ✅ Active | LSM-based Baseband Guard security whitelist |
| **Hardening** | **Unicode Bypass Fix** | ✅ Active | Prevents path traversal via non-printable Unicode codepoints |
| **Containers** | **Droidspaces** | ✅ Active | Kernel support for portable Linux containers and chroots |

<br>

<details>
<summary><b>🔍 Expand SUSFS Stealth Capabilities</b></summary>

- `SUS_PATH` - Hide files, directories, and sensitive system artifacts
- `SUS_MOUNT` - Mask overlayfs, tempfs, and root injection mounts
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
| **OOS 14** | `5.10` / `5.15` / `6.1` | OnePlus 10 Pro, 10T, 11, 11R, 12, 12R, Pad, Ace Series |
| **OOS 15** | `5.15` / `6.1` / `6.6` | OnePlus 12, 12R, 13, 13S, Open, Ace 3/5 Series, Nord 4/5 |
| **OOS 16** | `6.1` / `6.6` / `6.12` | OnePlus 13, 13S, Turbo 6 Series, Ace 6 Series, Pad 2/3/4 Pro |

---

<div align="center">
  <img src=".github/workflows/split.gif" alt="Divider" width="100%" height="4px" />
</div>

## 📥 Installation Instructions

### 🛠️ Prerequisites
- Unlocked bootloader on your OnePlus device.
- Recommended flashing utility: [**Kernel Flasher**](https://github.com/fatalcoder524/KernelFlasher) or [**Horizon Kernel Flasher**](https://github.com/libxzr/HorizonKernelFlasher).
- A backup of your stock `boot.img` and `init_boot.img` stored in external storage.

---

### 📲 Flashing Procedure

1. **Download the Flashable ZIP**:
   Grab the appropriate zip for your device model and OS version from [**GitHub Releases**](https://github.com/sakfi/OP_KSUN_FS/releases).
   ```
   Package Naming Convention:
   SKF_{MODEL}_{OS_VER}_{KERNEL_VER}_{KSU_TYPE}_{KSU_VER}_SuSFS_LKM.zip
   ```

2. **Flash via Kernel Flasher or Custom Recovery**:
   - Open **Kernel Flasher** or boot into **TWRP / OrangeFox**.
   - Select the downloaded `SKF_*.zip` file and begin flashing.
   - **Automatic Ramdisk Patching**: The installer automatically unpacks the target image, patches `kernelsu.ko` via `ksud`, stages `susfs_guard_lkm.ko`, and flashes the patched partition.

3. **Reboot**:
   - Reboot your system normally.

4. **Install Management Apps**:
   - Install the **KernelSU-Next Manager** APK from [KernelSU-Next Releases](https://github.com/KernelSU-Next/KernelSU-Next/releases).
   - In the Manager, install the **SUSFS Module** from [sidex15/ksu_module_susfs Releases](https://github.com/sidex15/ksu_module_susfs/releases).
   - Enjoy root privileges with stealth protections!

---

<div align="center">
  <img src=".github/workflows/split.gif" alt="Divider" width="100%" height="4px" />
</div>

## ⚠️ Disclaimer

```
Your warranty is now void. You are proceeding entirely at your own risk.
```
- Modifying your Android kernel can cause bootloops, device bricks, or loss of data if flashed onto incompatible firmware.
- Always ensure that your active OxygenOS version matches the release package you download.
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
