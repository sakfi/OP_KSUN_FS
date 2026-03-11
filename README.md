<div align="center">

# 🔥 OP_KSUN_FS 🔥
[![Build Kernel](https://github.com/sakfi/OP_KSUN_FS/actions/workflows/build-kernel-release.yml/badge.svg)](https://github.com/sakfi/OP_KSUN_FS/actions/workflows/build-kernel-release.yml)
[![GitHub Release](https://img.shields.io/github/v/release/sakfi/OP_KSUN_FS?style=flat-square&color=blue)](https://github.com/sakfi/OP_KSUN_FS/releases/latest)
[![Forks](https://img.shields.io/github/forks/sakfi/OP_KSUN_FS?style=flat-square&color=orange)](https://github.com/sakfi/OP_KSUN_FS/network/members)
[![Stars](https://img.shields.io/github/stars/sakfi/OP_KSUN_FS?style=flat-square&color=yellow)](https://github.com/sakfi/OP_KSUN_FS/stargazers)

<a href="https://github.com/sakfi/OP_KSUN_FS">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&size=20&duration=3000&pause=1000&color=00FF99&center=true&vCenter=true&width=600&lines=An+Open+Source+Kernel;Integrated+With+KernelSU-Next+%2B+SUSFS;For+OnePlus+Devices;Maintained+by+SakFi" alt="Typing SVG" />
</a>

[![KernelSU](https://img.shields.io/badge/KernelSU-Supported-green)](https://kernelsu.org/)
[![KernelSU-Next](https://img.shields.io/badge/KernelSU_Next-Supported-green)](https://kernelsu-next.github.io/webpage/)
[![Wild KSU](https://img.shields.io/badge/Wild_KSU-Supported-green)](https://github.com/WildKernels/Wild_KSU/)
[![SUSFS](https://img.shields.io/badge/SUSFS-Integrated-orange)](https://gitlab.com/simonpunk/susfs4ksu)

> **Forked from [WildKernels/OnePlus_KernelSU_SUSFS](https://github.com/WildKernels/OnePlus_KernelSU_SUSFS)**

</div>

---

## ⚠️ Disclaimer

### **🚨 Your warranty is no longer valid!**

Flashing this kernel will not void your warranty, but there is always a risk of bricking your device. Please make sure to:
- 💾 **Back up your data**
- 🧠 **Understand the risks before proceeding**

- I am **not responsible** for bricked devices, damaged hardware, or any issues that arise from using this kernel.
- **Please** do thorough research and fully understand the features added in this kernel before flashing it!
- By flashing this kernel, **YOU** are choosing to make these modifications. If something goes wrong, **do not blame me**!

<br>

> **⚠️ Verify compatibility of your device and OxygenOS version before flashing.**


<div align="center">

**Proceed at your own risk!**

</div>

---

## 🚀 What This Does

This repository provides a fully automated GitHub Actions workflow that:
- 📥 Clones the OnePlus GKI kernel source via `repo sync`
- 🛡️ Integrates **KernelSU-Next (KSUN)** or **KernelSU (KSU)**
- 🥷 Applies **SUSFS** patches for advanced root hiding
- 🚀 Applies a curated set of performance & optimization patches
- 📦 Builds and packages a flashable **AnyKernel3 ZIP**
- 📱 Supports all major OnePlus OxygenOS versions (OOS14, OOS15, OOS16)

---

## ✨ Features

| 🏷️ Feature | 📝 Description |
|:---|:---|
| 🔐 **KernelSU-Next** | Next-generation kernel-level root solution |
| 🥷 **SUSFS v2.0.0** | Advanced root hiding with Magic Mount support |
| 🛠️ **Manual Hooks** | `scope_min_manual_hooks_v1.4` for better app compatibility |
| 🖧 **BBR** | Improved TCP congestion control |
| 🛡️ **BBG** | LSM-based Baseband Guard security |
| 🌐 **TTL Target Support** | Network packet manipulation |
| 🧱 **IP Set Support** | Advanced firewall capabilities |
| 🏗️ **HMBIRD SCX** | Scheduler extensions for SM8750 devices |
| ✅ **LTO** | Link Time Optimization (thin/full/none configurable) |
| ⚡️ **TMPFS XATTR / POSIX ACL** | Extended attributes for Mountify support |
| 🚀 **Optimization patches** | Memory, I/O, CPU scheduler, network tuning |

<details>
<summary><b>👀 View SUSFS Hide Capabilities</b></summary>

- ✅ SUS_PATH · SUS_MOUNT · SUS_KSTAT · SUS_MAP
- ✅ SPOOF_UNAME · SPOOF_CMDLINE · OPEN_REDIRECT · AVC_SPOOF
</details>

---

## 📱 Supported Devices

Device configs are located in [`configs/`](./configs/). Devices are grouped by OxygenOS version:

| OOS Version | Kernel | Example Devices |
|-------------|--------|-----------------|
| **OOS14** | `android12` (5.10) <br> `android13` (5.15) <br> `android14` (6.1) | OP10 Pro, OP11, OP12, OP-ACE series |
| **OOS15** | `android13` (5.15) <br> `android14` (6.1) <br> `android15` (6.6) | OP12, OP13, OP13S, OP-ACE-5, OP-NORD series, OP-PAD series |
| **OOS16** | `android14` (6.1) <br> `android15` (6.6) <br> `android16` (6.12) | OP13, OP-ACE-5 series, OP-PAD series |

> 📁 **Full device list**: Browse the [`configs/`](./configs/) folder.

---

## 📋 Installation Instructions

<details>
<summary><b>🛠️ View Prerequisites</b></summary>

- Unlocked bootloader
- A backup of your current boot image
- Any root solution already installed (Magisk / KernelSU / APatch)
</details>

### Steps

1. 📥 Download the AnyKernel3 ZIP for your device from the [Releases](../../releases) page
2. ⚡ Flash using [Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher) or [Horizon Kernel Flasher](https://github.com/libxzr/HorizonKernelFlasher)
3. 🔄 Reboot
4. 📱 Install **KernelSU-Next Manager** → [Releases](https://github.com/KernelSU-Next/KernelSU-Next/releases)
5. 🧩 Install **SUSFS Module** from within the manager → [sidex15/ksu_module_susfs](https://github.com/sidex15/ksu_module_susfs/releases)

> 📖 **For GKI installation details:** [kernelsu.org/guide/installation](https://kernelsu.org/guide/installation.html)

---

## 🌟 Special Thanks

These amazing people help make this project possible! ❤️

<div align="center">

| 🔧 Project/Role | 👨‍💻 Developer | 🔗 Link |
|:---:|:---:|:---:|
| **Original Repository** | fatalcoder524 | [![GitHub](https://img.shields.io/badge/GitHub-fatalcoder524-blue?style=flat-square&logo=github)](https://github.com/fatalcoder524) |
| **KernelSU** | tiann | [![GitHub](https://img.shields.io/badge/GitHub-tiann-blue?style=flat-square&logo=github)](https://github.com/tiann/KernelSU) |
| **KernelSU-Next** | rifsxd | [![GitHub](https://img.shields.io/badge/GitHub-rifsxd-blue?style=flat-square&logo=github)](https://github.com/KernelSU-Next/KernelSU-Next) |
| **Magic-KSU** | 5ec1cff | [![GitHub](https://img.shields.io/badge/GitHub-5ec1cff-blue?style=flat-square&logo=github)](https://github.com/5ec1cff/KernelSU) |
| **SUSFS** | simonpunk | [![GitLab](https://img.shields.io/badge/GitLab-simonpunk-orange?style=flat-square&logo=gitlab)](https://gitlab.com/simonpunk/susfs4ksu.git) |
| **SUSFS Module** | sidex15 | [![GitHub](https://img.shields.io/badge/GitHub-sidex15-blue?style=flat-square&logo=github)](https://github.com/sidex15) |
| **Sultan Kernels** | kerneltoast | [![GitHub](https://img.shields.io/badge/GitHub-kerneltoast-blue?style=flat-square&logo=github)](https://github.com/kerneltoast) |
| **Helped with patches** | backslashxx | [![GitHub](https://img.shields.io/badge/GitHub-backslashxx-blue?style=flat-square&logo=github)](https://github.com/backslashxx) |
| **Helped with patches** | liqideqq (Teemo) | [![GitHub](https://img.shields.io/badge/GitHub-liqideqq-blue?style=flat-square&logo=github)](https://github.com/liqideqq) |

</div>

*If you have contributed and are not listed here, please remind me!* 🙏

---

## 💬 Support

If you encounter any issues or need help, feel free to:

<br>

- 🐛 Open an issue in this repository
- 💬 Reach out to me directly

---

## 📱 Connect With Me

<div align="center">

[![Telegram](https://img.shields.io/badge/Telegram-SakFi-blue?logo=telegram)](http://t.me/SakFi)
[![GitHub](https://img.shields.io/badge/GitHub-SakFi-blue?logo=github)](https://github.com/sakfi)

</div>

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=sakfi&label=Profile%20Views&color=ff007f&style=for-the-badge" alt="sakfi" />
</p>

