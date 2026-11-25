#!/usr/bin/env python3
"""Universal, KMI-safe battery & power optimization patcher for Android GKI 5.10 - 6.12.

Applies deterministic, idempotent source-level power optimizations without relying on
brittle line-number unified diffs (zero .rej failures across 5.10, 5.15, 6.1, 6.6, 6.12).
Never alters exported ABI/KMI struct layouts.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path


def patch_file(path: Path, desc: str, transform) -> bool:
    if not path.is_file():
        print(f"  [SKIP] {desc}: {path} not found")
        return False
    original = path.read_text(encoding="utf-8", errors="surrogateescape")
    updated, status = transform(original)
    if updated != original:
        path.write_text(updated, encoding="utf-8", errors="surrogateescape")
        print(f"  [OK]   {desc} ({status})")
        return True
    print(f"  [SKIP] {desc} ({status})")
    return False


def patch_mglru_force_enabled(text: str) -> tuple[str, str]:
    """Force MGLRU fully enabled (0x7) even when Android init.rc writes 0 at boot."""
    marker = "/* Force MGLRU on: request all caps, kernel caps to what's supported */"
    if marker in text:
        return text, "already applied"

    pattern = re.compile(
        r"(static ssize_t store_enabled\([^\)]*\)\s*\{.*?kstrtouint\(buf,\s*0,\s*&caps\)\)\s*return -EINVAL;\s*)"
        r"(for\s*\(i\s*=\s*0;\s*i\s*<\s*NR_LRU_GEN_CAPS;\s*i\+\+\)\s*\{.*?"
        r"if\s*\(i\s*==\s*LRU_GEN_CORE\)\s*)lru_gen_change_state\(enabled\);",
        re.DOTALL,
    )

    def repl(m: re.Match[str]) -> str:
        return (
            f"{m.group(1)}\n"
            f"\t{marker}\n"
            f"\tcaps |= BIT(LRU_GEN_CORE) | BIT(LRU_GEN_MM_WALK) | BIT(LRU_GEN_NONLEAF_YOUNG);\n\n"
            f"\t{m.group(2)}lru_gen_change_state(true); /* always enable core */"
        )

    new_text, count = pattern.subn(repl, text, count=1)
    if count == 0:
        return text, "MGLRU store_enabled() not present on this kernel"
    return new_text, "forced MGLRU 0x7 in mm/vmscan.c"


def patch_vmstat_interval(text: str) -> tuple[str, str]:
    """Double sysctl_stat_interval (1*HZ -> 2*HZ) to halve per-CPU vmstat timer wakeups."""
    if "sysctl_stat_interval __read_mostly = 2 * HZ;" in text or "sysctl_stat_interval = 2 * HZ;" in text:
        return text, "already applied"

    pattern = re.compile(r"(int\s+sysctl_stat_interval(?:\s+__read_mostly)?\s*=\s*)HZ(\s*;)")
    new_text, count = pattern.subn(r"\g<1>2 * HZ\g<2>", text, count=1)
    if count == 0:
        return text, "pattern not found"
    return new_text, "sysctl_stat_interval: HZ -> 2 * HZ"


def patch_dirty_writeback_interval(text: str) -> tuple[str, str]:
    """Increase dirty_writeback_interval (5s -> 15s) to cut periodic UFS writeback wakeups 3x."""
    if "dirty_writeback_interval = 15 * 100;" in text:
        return text, "already applied"

    pattern = re.compile(r"(unsigned int\s+dirty_writeback_interval\s*=\s*)5 \* 100(\s*;)")
    new_text, count = pattern.subn(r"\g<1>15 * 100\g<2>", text, count=1)
    if count == 0:
        return text, "pattern not found"
    return new_text, "dirty_writeback_interval: 5s -> 15s"


def patch_timer_slack(text: str) -> tuple[str, str]:
    """Increase default background timer_slack_ns (50us -> 100us) for better C-state residency."""
    if "timer_slack_ns\t= 100000" in text or "timer_slack_ns = 100000" in text or "#define TIMER_SLACK_NS_DEFAULT 100000" in text:
        return text, "already applied"

    pattern = re.compile(r"(\.timer_slack_ns\s*=\s*)50000(\s*,)")
    new_text, count = pattern.subn(r"\g<1>100000\g<2>", text, count=1)
    if count > 0:
        return new_text, "init_task.timer_slack_ns: 50000 -> 100000 ns"

    pattern2 = re.compile(r"(->timer_slack_ns\s*=\s*)50000(\s*;)")
    new_text, count = pattern2.subn(r"\g<1>100000\g<2>", text, count=1)
    if count > 0:
        return new_text, "default timer_slack_ns: 50000 -> 100000 ns"

    return text, "pattern not found"


def patch_wq_power_efficient_default(text: str) -> tuple[str, str]:
    """Ensure wq_power_efficient defaults to true in kernel/workqueue.c."""
    if "static bool wq_power_efficient = true;" in text:
        return text, "already applied"

    pattern = re.compile(
        r"static bool wq_power_efficient\s*=\s*IS_ENABLED\(CONFIG_WQ_POWER_EFFICIENT_DEFAULT\);"
    )
    new_text, count = pattern.subn("static bool wq_power_efficient = true;", text, count=1)
    if count == 0:
        return text, "pattern not found"
    return new_text, "wq_power_efficient forced true by default"


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply universal GKI battery optimizations.")
    parser.add_argument("--root", required=True, help="Path to common kernel source root")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"ERROR: kernel root not found: {root}", file=sys.stderr)
        return 1

    print(f"🔋 Applying Universal GKI Battery Optimizations to {root} ...")
    applied = 0
    applied += int(patch_file(root / "mm/vmscan.c", "Force full MGLRU (0x7)", patch_mglru_force_enabled))
    applied += int(patch_file(root / "mm/vmstat.c", "Halve per-CPU vmstat wakeups", patch_vmstat_interval))
    applied += int(patch_file(root / "mm/page-writeback.c", "3x fewer dirty writeback wakeups", patch_dirty_writeback_interval))
    applied += int(patch_file(root / "init/init_task.c", "Coalesce default background timers", patch_timer_slack))
    applied += int(patch_file(root / "kernel/workqueue.c", "Default power-efficient workqueues", patch_wq_power_efficient_default))

    print(f"✅ Universal battery optimization pass complete ({applied}/5 rules applied).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
