
## Hybrid LKM (KernelSU-Next + SUSFS Guard) Injection
home="${home:-${AKHOME:-$PWD}}"
if [ -d "$home/modules" ] && [ -f "$home/tools/ksud" ]; then
    ui_print " "
    ui_print "=========================================="
    ui_print "[+] Injecting KernelSU-Next & SUSFS LKM..."
    ui_print "=========================================="
    chmod 755 "$home/tools/ksud" "$home/tools/magiskboot" 2>/dev/null || true

    find_target_dev() {
        local part="$1"
        for p in "${part}${SLOT}" "$part" "${part}_a" "${part}_b"; do
            for dir in /dev/block/by-name /dev/block/bootdevice/by-name /dev/block/mapper /dev/block/platform/*/by-name /dev/block/platform/*/*/by-name; do
                if [ -e "$dir/$p" ]; then
                    echo "$dir/$p"
                    return 0
                fi
            done
            if [ -e "/dev/$p" ]; then
                echo "/dev/$p"
                return 0
            fi
        done
        return 1
    }

    target_part=""
    target_dev=""

    # Prefer init_boot for GKI 2.0 (Android 13+), fall back to boot
    dev=$(find_target_dev init_boot 2>/dev/null)
    if [ -n "$dev" ] && [ -e "$dev" ]; then
        target_part="init_boot${SLOT}"
        target_dev="$dev"
    else
        dev=$(find_target_dev boot 2>/dev/null)
        if [ -n "$dev" ] && [ -e "$dev" ]; then
            target_part="boot${SLOT}"
            target_dev="$dev"
        fi
    fi

    if [ -n "$target_dev" ]; then
        ui_print " - Target partition: $target_part ($target_dev)"
        cd "$home"
        rm -f target_image.img patched_image.img kernelsu_next_patched_*.img ksud_patched_*.img 2>/dev/null

        # Dump target partition image
        if [ -f "$home/tools/magiskboot" ]; then
            $home/tools/magiskboot dump "$target_dev" target_image.img 2>/dev/null || dd if="$target_dev" of=target_image.img 2>/dev/null
        else
            dd if="$target_dev" of=target_image.img 2>/dev/null
        fi

        if [ -f target_image.img ] && [ -s target_image.img ]; then
            ui_print " - Patching ramdisk with kernelsu.ko..."
            $home/tools/ksud boot-patch -b target_image.img -m "$home/modules/kernelsu.ko" --magiskboot "$home/tools/magiskboot" --out-name patched_image.img 2>&1

            patched_file=""
            if [ -f "$home/patched_image.img" ]; then
                patched_file="$home/patched_image.img"
            else
                patched_file=$(ls kernelsu_next_patched_*.img ksud_patched_*.img 2>/dev/null | head -n 1)
            fi

            if [ -n "$patched_file" ] && [ -f "$patched_file" ]; then
                ui_print " - Flashing patched $target_part..."
                dd if="$patched_file" of="$target_dev" 2>/dev/null
                rm -f "$patched_file" target_image.img 2>/dev/null
                ui_print "✅ KSUN LKM injected successfully into $target_part!"
            else
                ui_print "⚠️ Failed to patch ramdisk with ksud."
            fi
        else
            ui_print "⚠️ Failed to dump $target_part image."
        fi

        if [ -f "$home/modules/susfs_guard_lkm.ko" ]; then
            ui_print " - Staging SUSFS Guard LKM module..."
            mkdir -p /data/adb/modules/susfs_guard 2>/dev/null || true
            cp "$home/modules/susfs_guard_lkm.ko" /data/adb/modules/susfs_guard/ 2>/dev/null || true
            mkdir -p /tmp/modules 2>/dev/null || true
            cp "$home/modules/susfs_guard_lkm.ko" /tmp/modules/ 2>/dev/null || true
            ui_print "✅ SUSFS Guard LKM staged!"
        fi
    else
        ui_print "⚠️ Target boot/init_boot partition could not be detected."
    fi
fi

ui_print " "
ui_print "----------------------------------------------"
ui_print "OnePlus Kernels by SakFi"
ui_print "Telegram: https://t.me/SakFi"
ui_print "GitHub:   https://github.com/sakfi/OP_KSUN_FS"
ui_print "----------------------------------------------"
ui_print " "
ui_print "✅ Installation complete! Enjoy your kernel!"
ui_print " "

