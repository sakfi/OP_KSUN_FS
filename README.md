# OP_KSUN_FS

> A GitHub Actions build toolkit for **KernelSU-Next + SUSFS** on OnePlus GKI devices.  
> Maintained by **[sakfi](https://github.com/sakfi)** · Forked from [WildKernels/OnePlus_KernelSU_SUSFS](https://github.com/WildKernels/OnePlus_KernelSU_SUSFS)

---

## ⚠️ Disclaimer

### Your warranty is no longer valid!

I am **not responsible** for bricked devices, damaged hardware, or any issues that arise from using this kernel.

**Please** do thorough research and fully understand the features included before flashing!

By flashing this kernel, **YOU** are choosing to make these modifications. If something goes wrong, **do not blame me**!

<table>
  <tr>
    <th> :warning: </th>
    <th> Verify compatibility of your device and OxygenOS version before flashing. </th>
  </tr>
</table>

**Proceed at your own risk!**

---

## 🚀 What This Does

This repository provides a fully automated GitHub Actions workflow that:

- Clones the OnePlus GKI kernel source via `repo sync`
- Integrates **KernelSU-Next (KSUN)** or **KernelSU (KSU)**
- Applies **SUSFS** patches for advanced root hiding
- Applies a curated set of performance & optimization patches
- Builds and packages a flashable **AnyKernel3 ZIP**
- Supports all major OnePlus OxygenOS versions (OOS14, OOS15, OOS16)

---

## 📦 Features

- **KernelSU-Next** — Next-generation kernel-level root solution
- **SUSFS v2.0.0** — Advanced root hiding with Magic Mount support
- **Manual Hooks** — `scope_min_manual_hooks_v1.4` for better app compatibility
- **BBR** — Improved TCP congestion control
- **BBG** — LSM-based Baseband Guard security
- **TTL Target Support** — Network packet manipulation
- **IP Set Support** — Advanced firewall capabilities
- **HMBIRD SCX** — Scheduler extensions for SM8750 devices
- **LTO** — Link Time Optimization (thin/full/none configurable)
- **TMPFS XATTR / POSIX ACL** — Extended attributes for Mountify support
- **Optimization patches** — Memory, I/O, CPU scheduler, network tuning

### SUSFS Hide Capabilities
- ✅ SUS_PATH · SUS_MOUNT · SUS_KSTAT · SUS_MAP
- ✅ SPOOF_UNAME · SPOOF_CMDLINE · OPEN_REDIRECT · AVC_SPOOF

---

## 📱 Supported Devices

Device configs are located in [`configs/`](./configs/). Devices are grouped by OxygenOS version:

| OOS Version | Kernel | Example Devices |
|-------------|--------|-----------------|
| OOS14 | android12 (5.10) / android13 (5.15) / android14 (6.1) | OP10 Pro, OP11, OP12, OP-ACE series |
| OOS15 | android13 (5.15) / android14 (6.1) / android15 (6.6) | OP12, OP13, OP13S, OP-ACE-5, OP-NORD series, OP-PAD series |
| OOS16 | android14 (6.1) / android15 (6.6) / android16 (6.12) | OP13, OP-ACE-5 series, OP-PAD series |

> Full device list: browse the [`configs/`](./configs/) folder.

---

## 📥 Installation

### Prerequisites
- Unlocked bootloader
- A backup of your current boot image
- Any root solution already installed (Magisk / KernelSU / APatch)

### Steps
1. Download the AnyKernel3 ZIP for your device from the [Releases](../../releases) page
2. Flash using [Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher) or [Horizon Kernel Flasher](https://github.com/libxzr/HorizonKernelFlasher)
3. Reboot
4. Install **KernelSU-Next Manager** → [Releases](https://github.com/KernelSU-Next/KernelSU-Next/releases)
5. Install **SUSFS Module** from within the manager → [sidex15/ksu_module_susfs](https://github.com/sidex15/ksu_module_susfs/releases)

> For GKI installation details: [kernelsu.org/guide/installation](https://kernelsu.org/guide/installation.html)

---

## 🙏 Credits

- **KernelSU**: Developed by [tiann](https://github.com/tiann/KernelSU).
- **KernelSU-Next**: Developed by [rifsxd](https://github.com/KernelSU-Next/KernelSU-Next).
- **Magic-KSU**: Developed by [5ec1cff](https://github.com/5ec1cff/KernelSU).
- **SUSFS**: Developed by [simonpunk](https://gitlab.com/simonpunk/susfs4ksu.git).
- **SUSFS Module**: Developed by [sidex15](https://github.com/sidex15).
- **Sultan Kernels**: Developed by [kerneltoast](https://github.com/kerneltoast).

Special thanks to the open-source community for their contributions!

---

## 🌟 Special thanks to the following people for their contributions!

This helps me alot! <3

[fatalcoder524](https://github.com/fatalcoder524) - Created Original Repository!  
[simonpunk](https://gitlab.com/simonpunk/susfs4ksu.git) - Created SUSFS!  
[sidex15](https://github.com/sidex15) - Created module!  
[backslashxx](https://github.com/backslashxx) - Helped with patches!  
[Teemo](https://github.com/liqideqq) - Helped with patches!  

If you have contributed and are not here please remind me!

---

## 🐛 Support & Issues

If you encounter any issues, feel free to [open an issue](../../issues) in this repository.

---

