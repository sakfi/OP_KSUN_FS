# OP_KSUN_FS Repository Knowledge Base (Normalized)

This document is the authoritative technical reference for the `OP_KSUN_FS` project, synchronized with the "Source of Truth" found in the active workspace workflows and configuration files.

## 🛠 Project Scope & Matrix
This repository provides a multi-device build infrastructure for OnePlus kernels across OxygenOS versions.

- **OS Coverage**: OxygenOS 14 (Android 12/13/14), OxygenOS 15 (Android 13/14/15), and OxygenOS 16 (Android 14/15/16).
- **Device Matrix**: 
  - **OP Series**: 10 Pro/R/T, 11/11R, 12/12R, 13/13r/PJZ/PJZ, 15/15r/T.
  - **Ace Series**: Ace/Pro/Race variants across generations 2 through 6.
  - **Nord Series**: Nord 3, 4, 5 and CE variants.
  - **Pad Series**: OnePlus Pad 2, Pad 3, Pad Pro, and Pad Go (MTK and Qualcomm variants).
- **Kernel Versions**: GKI 2.0 (5.10, 5.15, 6.1, 6.6, 6.12).

## 🩹 Critical Technical Implementations

### 1. Release Workflow & Security Gate
- **Source**: `build-kernel-release.yml`
- **Manual Gate**: All production releases are gated by the `environment: Production-Release` setting. This requires manual approval within the GitHub Actions UI before the release script proceeds.
- **Branding**: The build system defaults to **SakFi-OP** branding for the kernel local version and `uname` string across all configurations.

### 2. BBG (Baseband Guard) Setup
- **Source**: `action.yml` (Line 1113)
- **Implementation**: The BBG set-up script is fetched via `curl` with targeted robustness flags:
  ```bash
  curl --fail --location --proto '=https' --retry 3 --retry-all-errors -LSs "https://setup-url"
  ```
- **Note**: This corrected configuration replaces older references to legacy retry counts.

### 3. SUS_MOUNT Panic Fix (OP-15)
- **Status**: Live in `action.yml`.
- **Implementation**: Safety checks added to `fs/statfs.c` and `fs/proc/fd.c` to prevent null-pointer dereferences in the mount tree during Recovery mode on newer OxygenOS versions (OOS16).

## 🏗 Patching Strategy
- **SUSFS**: Broadly utilizes `patch -p1` to accommodate multi-file upstream changes (v2.1.0+).
- **Adaptive Routing**: The build system dynamically handles missing `Kbuild` files by fallback-routing patch injections to `Makefile`.

## 📁 Repository Health & Outdated Docs
- **Source of Truth**: Always rely on `.github/actions/action.yml` and `.github/workflows/build-kernel-release.yml` for the current build logic.
- **Lagging Artifacts**: Be aware that `README.md` may occasionally lag behind active workflow updates (e.g., still referencing legacy branding or older SUSFS versions). The `KNOWLEDGE_BASE.md` is the primary record for current technical logic.
