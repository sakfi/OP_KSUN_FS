
## Hybrid LKM (KernelSU-Next + SUSFS Guard) Injection
if [ -d "$home/modules" ] && [ -f "$home/tools/ksud" ]; then
    ui_print " "
    ui_print "=========================================="
    ui_print "[+] Injecting KernelSU-Next & SUSFS LKM..."
    ui_print "=========================================="
    chmod 755 "$home/tools/ksud" "$home/tools/magiskboot" 2>/dev/null || true

    target_part=""
    target_dev=""
    for p in init_boot init_boot_a init_boot_b boot boot_a boot_b; do
        dev=$(find_block $p 2>/dev/null)
        if [ -n "$dev" ] && [ -e "$dev" ]; then
            target_part="$p"
            target_dev="$dev"
            break
        fi
    done

    init_boot_dev=$(find_block init_boot 2>/dev/null)
    if [ -n "$init_boot_dev" ] && [ -e "$init_boot_dev" ]; then
        target_dev="$init_boot_dev"
        target_part="init_boot"
    fi

    if [ -n "$target_dev" ]; then
        ui_print " - Target partition: $target_part ($target_dev)"
        cd "$home"
        rm -f target_image.img ksud_patched_*.img 2>/dev/null
        $home/tools/magiskboot dump "$target_dev" target_image.img 2>/dev/null || dd if="$target_dev" of=target_image.img 2>/dev/null

        if [ -f target_image.img ]; then
            ui_print " - Patching ramdisk with kernelsu.ko..."
            $home/tools/ksud boot-patch -b target_image.img -m "$home/modules/kernelsu.ko" --magiskboot "$home/tools/magiskboot"
            patched_file=$(ls ksud_patched_*.img 2>/dev/null | head -n 1)
            if [ -n "$patched_file" ] && [ -f "$patched_file" ]; then
                ui_print " - Flashing patched $target_part..."
                dd if="$patched_file" of="$target_dev" 2>/dev/null
                ui_print "✅ KSUN LKM injected successfully!"
            else
                ui_print "⚠️ Failed to patch ramdisk with ksud."
            fi
        fi

        if [ -f "$home/modules/susfs_guard_lkm.ko" ]; then
            ui_print " - Staging SUSFS Guard LKM module..."
            mkdir -p /data/adb/modules/susfs_guard 2>/dev/null || true
            cp "$home/modules/susfs_guard_lkm.ko" /data/adb/modules/susfs_guard/ 2>/dev/null || true
            mkdir -p /tmp/modules 2>/dev/null || true
            cp "$home/modules/susfs_guard_lkm.ko" /tmp/modules/ 2>/dev/null || true
            ui_print "✅ SUSFS Guard LKM staged!"
        fi
    fi
fi
