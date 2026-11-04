#!/usr/bin/env python3
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

def inject_banner(banner_path, ak3_dir):
    if not os.path.isfile(banner_path):
        print(f"Warning: Banner file not found: {banner_path}")
        return False
    
    anykernel_path = os.path.join(ak3_dir, "anykernel.sh")
    if not os.path.isfile(anykernel_path):
        print(f"Warning: anykernel.sh not found in {ak3_dir}")
        return False

    # 1. Silence default AnyKernel3 banner in tools/ak3-core.sh
    ak3_core_path = os.path.join(ak3_dir, "tools", "ak3-core.sh")
    if os.path.isfile(ak3_core_path):
        with open(ak3_core_path, "r", encoding="utf-8", errors="ignore") as f:
            core_content = f.readlines()
        with open(ak3_core_path, "w", encoding="utf-8", newline="\n") as f:
            for line in core_content:
                if 'ui_print "$kernel_string"' in line or 'ui_print "AnyKernel3 by osm0sis' in line:
                    continue
                f.write(line)

    # 2. Parse custom_banner.txt
    with open(banner_path, "r", encoding="utf-8", errors="ignore") as f:
        banner_raw = f.readlines()

    banner_commands = []
    mode = None
    for line in banner_raw:
        line = line.strip("\r\n")
        if "[ASCII_BANNER_START]" in line:
            mode = "ASCII"
            continue
        elif "[ASCII_BANNER_END]" in line:
            mode = None
            continue
        elif "[UI_PRINT_START]" in line:
            mode = "UI"
            continue
        elif "[UI_PRINT_END]" in line:
            mode = None
            continue

        if mode == "ASCII":
            if not line:
                continue
            if line.startswith("sleep") or line.startswith("ui_print"):
                banner_commands.append(line)
            else:
                escaped = line.replace('"', '\\"')
                banner_commands.append(f'ui_print "{escaped}"')
        elif mode == "UI":
            if line.startswith("#"):
                continue
            banner_commands.append(line)

    banner_str = "\n".join(banner_commands)

    # 3. Read & inject into anykernel.sh
    with open(anykernel_path, "r", encoding="utf-8", errors="ignore") as f:
        ak3_raw = f.readlines()

    ak3_new = []
    for line in ak3_raw:
        stripped = line.strip()
        # Remove original ui_print lines
        if stripped.startswith("ui_print"):
            continue
        # Brand kernel.string
        if line.startswith("kernel.string="):
            ak3_new.append("kernel.string=OnePlus Kernels by SakFi\n")
            continue
        
        ak3_new.append(line)
        # Inject right after . tools/ak3-core.sh
        if stripped.startswith(". tools/ak3-core.sh"):
            ak3_new.append("\n" + banner_str + "\n")

    with open(anykernel_path, "w", encoding="utf-8", newline="\n") as f:
        f.writelines(ak3_new)

    # 4. Remove default static banner if present
    static_banner = os.path.join(ak3_dir, "banner")
    if os.path.exists(static_banner):
        try:
            os.remove(static_banner)
        except OSError:
            pass

    print("[+] Custom SakFi cinematic banner injected successfully into anykernel.sh!")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: inject_banner.py <banner_file> <ak3_folder>")
        sys.exit(1)
    banner_file = sys.argv[1]
    ak3_folder = sys.argv[2]
    success = inject_banner(banner_file, ak3_folder)
    sys.exit(0 if success else 1)
