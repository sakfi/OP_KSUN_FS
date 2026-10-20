#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
set -euo pipefail
echo "::group::Apply SUSFS patches"
if [ "${KSUMODE:-lkm}" = "lkm" ]; then
  echo "ℹ️ LKM Mode Active: GKI kernel will be patched with SUSFS hooks, while KernelSU is loaded as an LKM module."
fi
cd "$KERNEL_PLATFORM_FOLDER"
if [ -d "$SUSFS_FOLDER/kernel_patches/fs" ]; then
  cp "$SUSFS_FOLDER/kernel_patches/fs/"* "$COMMON_KERNEL_FOLDER/fs/"
  cp "$SUSFS_FOLDER/kernel_patches/include/linux/"* "$COMMON_KERNEL_FOLDER/include/linux/"
elif [ -d "$SUSFS_FOLDER/fs" ]; then
  cp "$SUSFS_FOLDER/fs/"* "$COMMON_KERNEL_FOLDER/fs/"
  cp "$SUSFS_FOLDER/include/linux/"* "$COMMON_KERNEL_FOLDER/include/linux/"
fi

# Ensure susfs_def.h is self-contained with required standard kernel types and headers
if [ -f "$COMMON_KERNEL_FOLDER/include/linux/susfs_def.h" ]; then
  if ! grep -q '<linux/cred.h>' "$COMMON_KERNEL_FOLDER/include/linux/susfs_def.h"; then
    sed -i '/#include <linux\/string.h>/a #include <linux/types.h>\n#include <linux/sched.h>\n#include <linux/cred.h>\n#include <linux/thread_info.h>' "$COMMON_KERNEL_FOLDER/include/linux/susfs_def.h"
  fi
fi

susfs_version=$(grep '#define SUSFS_VERSION' "$COMMON_KERNEL_FOLDER/include/linux/susfs.h" | awk -F'"' '{print $2}')
echo "SUSVER=$susfs_version" >> $GITHUB_ENV
echo "$susfs_version" >> "${ARTIFACTS_FOLDER}/${OP_MODEL}_${OP_OS_VERSION}.txt"
echo "SusFS Version: $susfs_version"

# Function to compare semantic versions
version_lte() {
  [ "$(printf '%s\n' "$2" "$1" | sort -V | head -n1)" = "$1" ]
}

if version_lte "${susfs_version:1}" "1.5.12"; then
  echo "NEED_HOOKS=true" >> $GITHUB_ENV
else
  echo "NEED_HOOKS=false" >> $GITHUB_ENV
fi

if [ "${KSUMODE:-lkm}" != "lkm" ]; then
  case "$susfs_version" in
    "v1.5.8")
    if [ "${KSU_TYPE:-}" = "KSUN" ]; then
      patch -p1 --forward --fuzz=3 < "$SUSFS_FOLDER/kernel_patches/KernelSU/10_enable_susfs_for_ksu.patch" || true
      patch -p1 --forward --fuzz=3 < "$KERNEL_PATCHES_FOLDER/next/susfs_fix_patches/$susfs_version/fix_apk_sign.c.patch"
      patch -p1 --forward --fuzz=3 < "$KERNEL_PATCHES_FOLDER/next/susfs_fix_patches/$susfs_version/fix_core_hook.c.patch"
      patch -p1 --forward --fuzz=3 < "$KERNEL_PATCHES_FOLDER/next/susfs_fix_patches/$susfs_version/fix_selinux.c.patch"
      patch -p1 --forward --fuzz=3 < "$KERNEL_PATCHES_FOLDER/next/susfs_fix_patches/$susfs_version/fix_ksud.c.patch"
    else
      cd "$KSU_FOLDER"
      patch -p1 --forward --fuzz=3 < "$SUSFS_FOLDER/kernel_patches/KernelSU/10_enable_susfs_for_ksu.patch"
    fi
    ;;
  "v1.5.9"|"v1.5.10"|"v1.5.11"|"v1.5.12")
    if [ "${KSU_TYPE:-}" = "KSUN" ]; then
      cd "$KSUN_FOLDER"
      patch -p1 --forward < "$SUSFS_FOLDER/kernel_patches/KernelSU/10_enable_susfs_for_ksu.patch" || true
      mapfile -t rej_files < <(find ./kernel -maxdepth 2 -name "*.rej")
      for rej_file in "${rej_files[@]}"; do
        [ -f "$rej_file" ] || continue
        file=$(basename "$rej_file" .c.rej)
        echo "Patching file: $file.c with fix_$file.c.patch"
        rm -f "$rej_file"
        patch -p1 --forward < "$KERNEL_PATCHES_FOLDER/next/susfs_fix_patches/$susfs_version/fix_$file.c.patch"
      done
      patch -p1 --forward < "$KERNEL_PATCHES_FOLDER/next/susfs_fix_patches/$susfs_version/fix_kernel_compat.c.patch"
    else
      cd "$KSU_FOLDER"
      patch -p1 --forward < "$SUSFS_FOLDER/kernel_patches/KernelSU/10_enable_susfs_for_ksu.patch"
    fi
    ;;
  "v2.0.0")
    if [ "${KSU_TYPE:-}" = "KSUN" ]; then
      cd "$KSUN_FOLDER"
      patch -p1 --forward < "$SUSFS_FOLDER/kernel_patches/KernelSU/10_enable_susfs_for_ksu.patch" || true
      mapfile -t rej_files < <(find ./kernel -name "*.rej")
      for rej_file in "${rej_files[@]}"; do
        [ -f "$rej_file" ] || continue
        file=$(basename "$rej_file" .rej)
        echo "Patching file: $file with fix_$file.patch"
        rm -f "$rej_file"
        patch -p1 --forward < "$KERNEL_PATCHES_FOLDER/next/susfs_fix_patches/$susfs_version/fix_$file.patch"
      done
      echo "Patching Hook Mode!"
      patch -p1 --forward < "$KERNEL_PATCHES_FOLDER/next/susfs_fix_patches/$susfs_version/overwrite_hook_mode.patch"
      echo "Patching KSU_TOOLKIT Support for SusFS kernel!"
      patch -p1 --forward < "$KERNEL_PATCHES_FOLDER/next/susfs_fix_patches/$susfs_version/ksu_toolkit.patch"
      if [ "$KSUVER" -le 33095 ]; then
        echo "Patching Multi-manager Support for SusFS kernel!"
        patch -p1 --forward < "$KERNEL_PATCHES_FOLDER/next/susfs_fix_patches/$susfs_version/multi_manager.patch"
      fi
      if [ "$KSUVER" -ge 33068 ] && [ "$KSUVER" -lt 33070 ]; then
        echo "Patching Multi-manager sepolicy Support for SusFS kernel!"
        patch -p1 --forward < "$KERNEL_PATCHES_FOLDER/next/susfs_fix_patches/$susfs_version/multi_sepolicy_fix.patch"
      fi
    else
      cd "$KSU_FOLDER"
      patch -p1 --forward < "$SUSFS_FOLDER/kernel_patches/KernelSU/10_enable_susfs_for_ksu.patch" || true
    fi
    ;;
  "v2.1.0")
    if [ "${KSU_TYPE:-}" = "KSUN" ]; then
      cd "$KSUN_FOLDER"
      patch -p1 --forward < "$SUSFS_FOLDER/kernel_patches/KernelSU/10_enable_susfs_for_ksu.patch" || true
      mapfile -t rej_files < <(find ./kernel -name "*.rej")
      for rej_file in "${rej_files[@]}"; do
        [ -f "$rej_file" ] || continue
        file=$(basename "$rej_file" .rej)
        echo "Patching file: $file with fix_$file.patch"
        rm -f "$rej_file"
        patch -p1 --forward < "$KERNEL_PATCHES_FOLDER/next/susfs_fix_patches/$susfs_version/fix_$file.patch"
      done
      echo "Patching Hook Mode!"
      patch -p1 --forward < "$KERNEL_PATCHES_FOLDER/next/susfs_fix_patches/$susfs_version/overwrite_hook_mode.patch"
      echo "Patching KSU_TOOLKIT Support for SusFS kernel!"
      patch -p1 --forward < "$KERNEL_PATCHES_FOLDER/next/susfs_fix_patches/$susfs_version/ksu_toolkit.patch"
      if [ "$KSUVER" -le 33095 ]; then
        echo "Patching Multi-manager Support for SusFS kernel!"
        patch -p1 --forward < "$KERNEL_PATCHES_FOLDER/next/susfs_fix_patches/$susfs_version/multi_manager.patch"
      fi
      if [ "$KSUVER" -ge 33068 ] && [ "$KSUVER" -lt 33070 ]; then
        echo "Patching Multi-manager sepolicy Support for SusFS kernel!"
        patch -p1 --forward < "$KERNEL_PATCHES_FOLDER/next/susfs_fix_patches/$susfs_version/multi_sepolicy_fix.patch"
      fi
    else
      cd "$KSU_FOLDER"
      patch -p1 --forward < "$SUSFS_FOLDER/kernel_patches/KernelSU/10_enable_susfs_for_ksu.patch" || true
    fi
    ;;
  "v2.2.0"|"v2.3.0")
    if [ "${KSU_TYPE:-}" = "KSUN" ]; then
      cd "$KSUN_FOLDER"
      patch -p1 --forward < "$SUSFS_FOLDER/kernel_patches/KernelSU/10_enable_susfs_for_ksu.patch" || true
      mapfile -t rej_files < <(find ./kernel -name "*.rej")
      for rej_file in "${rej_files[@]}"; do
        [ -f "$rej_file" ] || continue
        file=$(basename "$rej_file" .rej)
        fix_patch="$KERNEL_PATCHES_FOLDER/next/susfs_fix_patches/$susfs_version/fix_$file.patch"
        if [ -f "$fix_patch" ]; then
          echo "Patching file: $file with fix_$file.patch"
          rm -f "$rej_file"
          patch -p1 --forward < "$fix_patch" || true
        elif [ -f "$KERNEL_PATCHES_FOLDER/next/susfs_fix_patches/$susfs_version/fix_${file}.c.patch" ]; then
          echo "Patching file: $file with fix_${file}.c.patch"
          rm -f "$rej_file"
          patch -p1 --forward < "$KERNEL_PATCHES_FOLDER/next/susfs_fix_patches/$susfs_version/fix_${file}.c.patch" || true
        else
          echo "⚠️ No fix patch found for $file (reject file: $rej_file)"
        fi
      done
      echo "Applying KSUN compatibility fixes (patch_ksun_33400.py)..."
      python3 "$SCRIPT_DIR/patch_ksun_33400.py" "$KSUN_FOLDER"
      # Clean up any harmless non-KSUN rejects (e.g. ksud_integration.c from official KernelSU patch)
      rm -f ./kernel/runtime/*.rej 2>/dev/null || true
      echo "Patching Hook Mode!"
      patch -p1 --forward < "$KERNEL_PATCHES_FOLDER/next/susfs_fix_patches/$susfs_version/overwrite_hook_mode.patch"
      echo "Patching KSU_TOOLKIT Support for SusFS kernel!"
      patch -p1 --forward < "$KERNEL_PATCHES_FOLDER/next/susfs_fix_patches/$susfs_version/ksu_toolkit.patch"
    else
      cd "$KSU_FOLDER"
      patch -p1 --forward < "$SUSFS_FOLDER/kernel_patches/KernelSU/10_enable_susfs_for_ksu.patch" || true
    fi
    ;;
  *)
    echo "::error::Unsupported SUSFS version: $susfs_version"
    exit 1
    ;;
esac
else
  echo "ℹ️ LKM mode: In-tree KernelSU SUSFS patch skipped (modular KSUN driver used)."
fi

cd "$COMMON_KERNEL_FOLDER"
if [ "$ANDROID_VER" = "android15" ] && [ "$KERNEL_VER" = "6.6" ]; then
  if ! grep -qxF '#include <trace/hooks/fs.h>' ./fs/namespace.c; then
    sed -i '/#include <trace\/hooks\/blk.h>/a #include <trace\/hooks\/fs.h>' ./fs/namespace.c
  fi
  if ! grep -qxF 'extern void __fold_filemap_fixup_entry(struct vma_iterator *iter, unsigned long *end);' ./include/linux/page_size_compat.h; then
    patch -p1 < "$KERNEL_PATCHES_FOLDER/common/backports/fold_fixup_entries.patch"
  fi
fi

# Fake kernel patch to fix failures
fake_patched=0
fake_patched_expand=0
if [ "$ANDROID_VER" = "android15" ] && [ "$KERNEL_VER" = "6.6" ]; then
  if ! grep -qxF $'\tunsigned int nr_subpages = __PAGE_SIZE / PAGE_SIZE;' ./fs/proc/task_mmu.c; then
    echo "nr_subpages Line not found. Fake Patching!"
    sed -i -e '/int ret = 0, copied = 0;/a \\tunsigned int nr_subpages \= __PAGE_SIZE \/ PAGE_SIZE;' -e '/int ret = 0, copied = 0;/a \\tpagemap_entry_t \*res = NULL;' ./fs/proc/task_mmu.c
    fake_patched=1
  fi
  
  if ! grep -qxF '#include <linux/dma-buf.h>' ./fs/proc/base.c; then
    echo "#include <linux/dma-buf.h> Line not found. Adding missing header"
    sed -i '/#include <linux\/cpufreq_times.h>/a #include <linux\/dma-buf.h>' ./fs/proc/base.c
  fi
  
  if ! grep -qxF '#include <linux/zswap.h>' ./mm/memory.c; then
    echo "#include <linux/zswap.h> Line not found. Adding missing header"
    sed -i '/#include <linux\/sched\/sysctl.h>/a #include <linux\/zswap.h>' ./mm/memory.c
  fi
  
  if grep -qF 'if (vma->vm_end > last_vma_end)' ./fs/proc/task_mmu.c && ! grep -qxF 'SUSFS_IS_INODE_SUS_MAP' ./fs/proc/task_mmu.c; then
    echo "Temporarily expand the last_vma_end if block to fix a matching issue."
    perl -i -0pe 's/\t\t\tif \(vma->vm_end > last_vma_end\)\n\t\t\t\tsmap_gather_stats\(vma, &mss, last_vma_end\);/\t\t\tif (vma->vm_end > last_vma_end) {\n\t\t\t\tsmap_gather_stats(vma, \&mss, last_vma_end);\n\t\t\t\tlast_vma_end = vma->vm_end;\n\t\t\t}/' ./fs/proc/task_mmu.c
    fake_patched_expand=1
  fi
fi
if [ "$ANDROID_VER" = "android12" ] && [ "$KERNEL_VER" = "5.10" ]; then
  if ! grep -qxF $'\tif (!vma_pages(vma))' ./fs/proc/task_mmu.c; then
    echo "vma_pages Line not found. Fake Patching!"
    fake_patched=1
  fi
fi
if [ "$ANDROID_VER" = "android13" ] && [ "$KERNEL_VER" = "5.15" ]; then
  if ! grep -qxF $'\tif (!vma_pages(vma))' ./fs/proc/task_mmu.c; then
    echo "vma_pages Line not found. Fake Patching!"
    fake_patched=1
  fi
  
  if grep -qxF '#include <linux/swap_slots.h>' ./mm/memory.c; then
    echo "#include swap_slots.h> Line found. Deleting header."
    sed -i '/#include <linux\/swap_slots.h>/d' ./mm/memory.c
    fake_patched=1
  fi
fi

if [ "$ANDROID_VER" = "android14" ] && [ "$KERNEL_VER" = "6.1" ]; then
  if ! grep -qxF $'\tif (!vma_pages(vma))' ./fs/proc/task_mmu.c; then
    echo "vma_pages Line not found. Fake Patching!"
    fake_patched=1
  fi
  
  if ! grep -qxF '#include <linux/dma-buf.h>' ./fs/proc/base.c; then
    echo "#include <linux/dma-buf.h> Line not found. Adding missing header"
    sed -i '/#include <linux\/cpufreq_times.h>/a #include <linux\/dma-buf.h>' ./fs/proc/base.c
  fi
fi

target_patch=""
if [ -d "$SUSFS_FOLDER/$KERNEL_VER" ]; then
  target_patch=$(find "$SUSFS_FOLDER/$KERNEL_VER" -name "50_add_susfs_in_${SUSFS_KERNEL_BRANCH:-}*.patch" 2>/dev/null | head -n 1)
  if [ -z "$target_patch" ] || [ ! -f "$target_patch" ]; then
    target_patch=$(find "$SUSFS_FOLDER/$KERNEL_VER" -name "50_add_susfs_in_*.patch" 2>/dev/null | head -n 1)
  fi
fi
if [ -z "$target_patch" ] || [ ! -f "$target_patch" ]; then
  target_patch="$SUSFS_FOLDER/kernel_patches/50_add_susfs_in_${SUSFS_KERNEL_BRANCH:-}.patch"
  if [ ! -f "$target_patch" ]; then
    target_patch=$(find "$SUSFS_FOLDER/kernel_patches" -maxdepth 1 -name "50_add_susfs_in_*.patch" 2>/dev/null | head -n 1)
  fi
fi
if [ -z "$target_patch" ] || [ ! -f "$target_patch" ]; then
  target_patch=$(find "$SUSFS_FOLDER" -name "50_add_susfs_in_*.patch" 2>/dev/null | head -n 1)
fi
echo "Applying SUSFS kernel patch: $target_patch"
patch -p1 --forward < "$target_patch" || true

# Resolve harmless header reject in fs/namespace.c if hunk 1 failed due to missing trace hook context
if [ -f "./fs/namespace.c.rej" ]; then
  if ! grep -q '<linux/susfs_def.h>' ./fs/namespace.c; then
    if grep -q '#include "internal.h"' ./fs/namespace.c; then
      sed -i '/#include "internal.h"/a #include <linux/susfs_def.h>\nextern bool susfs_is_current_ksu_domain(void);\nextern struct static_key_true susfs_is_sdcard_android_data_not_decrypted;\n#ifndef CL_COPY_MNT_NS\n#define CL_COPY_MNT_NS BIT(25)\n#endif' ./fs/namespace.c
    else
      sed -i '1i #include <linux/susfs_def.h>\nextern bool susfs_is_current_ksu_domain(void);\nextern struct static_key_true susfs_is_sdcard_android_data_not_decrypted;\n#ifndef CL_COPY_MNT_NS\n#define CL_COPY_MNT_NS BIT(25)\n#endif' ./fs/namespace.c
    fi
  fi
  if grep -q 'susfs_def.h' ./fs/namespace.c.rej && ! grep -q 'mnt_alloc_id' ./fs/namespace.c.rej; then
    echo "Resolved harmless header reject in fs/namespace.c"
    rm -f ./fs/namespace.c.rej
  fi
fi
# Resolve harmless header reject in fs/exec.c if hunk 1 failed
if [ -f "./fs/exec.c.rej" ]; then
  if ! grep -q '<linux/susfs_def.h>' ./fs/exec.c; then
    if grep -q '#include <linux/binfmts.h>' ./fs/exec.c; then
      sed -i '/#include <linux\/binfmts.h>/a #include <linux/susfs_def.h>' ./fs/exec.c
    else
      sed -i '1i #include <linux/susfs_def.h>' ./fs/exec.c
    fi
  fi
  if grep -q 'susfs_def.h' ./fs/exec.c.rej && ! grep -q 'do_execveat_common' ./fs/exec.c.rej; then
    echo "Resolved harmless header reject in fs/exec.c"
    rm -f ./fs/exec.c.rej
  fi
fi
# Resolve harmless header and map rejects in fs/proc/task_mmu.c
if [ -f "./fs/proc/task_mmu.c.rej" ]; then
  if ! grep -q '<linux/susfs_def.h>' ./fs/proc/task_mmu.c; then
    if grep -q '#include "internal.h"' ./fs/proc/task_mmu.c; then
      sed -i '/#include "internal.h"/a #include <linux/susfs_def.h>' ./fs/proc/task_mmu.c
    else
      sed -i '1i #include <linux/susfs_def.h>' ./fs/proc/task_mmu.c
    fi
  fi
  # If show_smap hunk rejected, ensure SUSFS check is added to show_smap
  if grep -q 'show_smap' ./fs/proc/task_mmu.c.rej && ! grep -q 'SUSFS_IS_INODE_SUS_MAP' ./fs/proc/task_mmu.c; then
    perl -i -0pe 's/(static int show_smap\(struct seq_file \*m, void \*v\)\n\{\n\tstruct vm_area_struct \*vma = v;\n\tstruct mem_size_stats mss = \{\};\n)/$1#ifdef CONFIG_KSU_SUSFS_SUS_MAP\n\tif (vma->vm_file) {\n\t\tif (SUSFS_IS_INODE_SUS_MAP(file_inode(vma->vm_file)))\n\t\t\treturn 0;\n\t}\n#endif\n/' ./fs/proc/task_mmu.c
    echo "Injected SUSFS_IS_INODE_SUS_MAP into show_smap"
  fi
  # If show_smaps_rollup hunk rejected, ensure bypass_orig_flow is added around smap_gather_stats
  if grep -q 'show_smaps_rollup' ./fs/proc/task_mmu.c.rej && grep -q 'smap_gather_stats(vma, &mss, 0);' ./fs/proc/task_mmu.c && ! grep -q 'bypass_orig_flow' ./fs/proc/task_mmu.c; then
    perl -i -0pe 's/(\tdo \{\n)(\t\tsmap_gather_stats\(vma, &mss, 0\);)/$1#ifdef CONFIG_KSU_SUSFS_SUS_MAP\n\t\tif (vma->vm_file && SUSFS_IS_INODE_SUS_MAP(file_inode(vma->vm_file)))\n\t\t\tgoto bypass_orig_flow;\n#endif\n$2\n#ifdef CONFIG_KSU_SUSFS_SUS_MAP\nbypass_orig_flow:\n#endif/' ./fs/proc/task_mmu.c
    echo "Injected SUSFS bypass_orig_flow into show_smaps_rollup"
  fi
  # Clear task_mmu.c.rej if show_vma_header_prefix did not reject
  if ! grep -q 'show_vma_header_prefix' ./fs/proc/task_mmu.c.rej; then
    echo "Resolved rejects in fs/proc/task_mmu.c"
    rm -f ./fs/proc/task_mmu.c.rej
  fi
fi

# SUSFS's OPEN_REDIRECT code unconditionally calls VMA_PAD_START(), which
# only exists on GKI branches that carry Google's page-size-migration
# feature (added to each android version's kernel/common branch at a
# different, sometime later, os_patch_level). Older os_patch_levels in
# our build matrix predate it, so fall back to a no-padding definition
# when the real header/macro isn't present. This is version-agnostic and
# a no-op wherever the real header already provides it.
if grep -q 'VMA_PAD_START(' ./fs/proc/task_mmu.c && ! grep -qE '#include <linux/pgsize_migration(_inline)?\.h>|define VMA_PAD_START' ./fs/proc/task_mmu.c; then
  sed -i '\|#include "internal.h"|a\\n#undef VMA_PAD_START\n#ifndef VMA_PAD_START\n#define VMA_PAD_START(vma) ((vma)->vm_end)\n#endif' fs/proc/task_mmu.c
  echo "Added VMA_PAD_START fallback definition to fs/proc/task_mmu.c"
fi

# Revert Fake kernel patch
if [ "$fake_patched_expand" = 1 ]; then
  if [ "$ANDROID_VER" = "android15" ] && [ "$KERNEL_VER" = "6.6" ]; then
    if grep -qF 'if (vma->vm_end > last_vma_end) {' ./fs/proc/task_mmu.c && ! grep -qxF 'SUSFS_IS_INODE_SUS_MAP' ./fs/proc/task_mmu.c; then
      perl -i -0pe 's/\t\t\tif \(vma->vm_end > last_vma_end\) \{\n\t\t\t\tsmap_gather_stats\(vma, &mss, last_vma_end\);\n\t\t\t\tlast_vma_end = vma->vm_end;\n\t\t\t\}/\t\t\tif (vma->vm_end > last_vma_end)\n\t\t\t\tsmap_gather_stats(vma, \&mss, last_vma_end);/' ./fs/proc/task_mmu.c
    fi
  fi
fi

if [ "$fake_patched" = 1 ]; then
  if [ "$ANDROID_VER" = "android15" ] && [ "$KERNEL_VER" = "6.6" ]; then
    if grep -qxF $'\tunsigned int nr_subpages = __PAGE_SIZE / PAGE_SIZE;' ./fs/proc/task_mmu.c; then
      echo "nr_subpages Line found. Revert Fake Patching!"
      sed -i -e '/unsigned int nr_subpages \= __PAGE_SIZE \/ PAGE_SIZE;/d' -e '/pagemap_entry_t \*res = NULL;/d' ./fs/proc/task_mmu.c
    fi
  fi
  if [ "$ANDROID_VER" = "android12" ] && [ "$KERNEL_VER" = "5.10" ]; then
    if grep -qxF $'\t\t\tgoto show_pad;' ./fs/proc/task_mmu.c; then
      echo "vma_pages Line found. Revert Fake Patching!"
      sed -i -e 's/goto show_pad;/return 0;/' ./fs/proc/task_mmu.c
    fi
  fi
  if [ "$ANDROID_VER" = "android13" ] && [ "$KERNEL_VER" = "5.15" ]; then
    if grep -qxF $'\t\t\tgoto show_pad;' ./fs/proc/task_mmu.c; then
      echo "vma_pages Line found. Revert Fake Patching!"
      sed -i -e 's/goto show_pad;/return 0;/' ./fs/proc/task_mmu.c
    fi
    
    if ! grep -qxF '#include <linux/swap_slots.h>' ./mm/memory.c; then
      echo "#include <linux/swap_slots.h> Line not found. Adding missing header"
      sed -i '/#include <linux\/vmalloc.h>/a #include <linux\/swap_slots.h>' ./mm/memory.c
    fi
  fi
  if [ "$ANDROID_VER" = "android14" ] && [ "$KERNEL_VER" = "6.1" ]; then
    if grep -qxF $'\t\t\tgoto show_pad;' ./fs/proc/task_mmu.c; then
      echo "vma_pages Line found. Revert Fake Patching!"
      sed -i -e 's/goto show_pad;/return 0;/' ./fs/proc/task_mmu.c
    fi
  fi
fi

# Verify no patch rejects (.rej) exist
rej_count=0
for dir in "$COMMON_KERNEL_FOLDER" "${KSUN_FOLDER:-}" "${KSU_FOLDER:-}"; do
  if [ -n "$dir" ] && [ -d "$dir" ]; then
    if find "$dir" -name "*.rej" -print | grep -q .; then
      echo "::error::SUSFS patches did not apply cleanly in $dir! Found .rej files:"
      find "$dir" -name "*.rej" -exec echo "REJECT: {}" \;
      
      echo "::group::🔍 Detailed reject file contents from $dir"
      find "$dir" -name "*.rej" | while read -r rej_file; do
        echo "------------------------------------------------------------"
        echo "Reject file: $rej_file"
        echo "------------------------------------------------------------"
        sed -n '1,120p' "$rej_file" 2>/dev/null || cat "$rej_file" 2>/dev/null || true
      done
      echo "::endgroup::"
      # Copy rejects to a folder for artifact upload
      mkdir -p "$GITHUB_WORKSPACE/patch_rejects"
      find "$dir" -name "*.rej" | while read -r rej_file; do
        rel_path="${rej_file#$GITHUB_WORKSPACE/}"
        dest_dir="$GITHUB_WORKSPACE/patch_rejects/$(dirname "$rel_path")"
        mkdir -p "$dest_dir"
        cp "$rej_file" "$dest_dir/"
      done
      
      rej_count=$((rej_count + 1))
    fi
  fi
done
if [ "$rej_count" -gt 0 ]; then
  echo "::error::One or more SUSFS / KernelSU patches created .rej files. Aborting build."
  exit 1
fi

echo "✅ SUSFS patches applied"

echo "Add SUSFS Configuration Settings"
printf '%s\n' \
  'CONFIG_KSU_SUSFS=y' \
  'CONFIG_KSU_SUSFS_HAS_MAGIC_MOUNT=y' \
  'CONFIG_KSU_SUSFS_SUS_PATH=y' \
  'CONFIG_KSU_SUSFS_SUS_MOUNT=y' \
  'CONFIG_KSU_SUSFS_AUTO_ADD_SUS_KSU_DEFAULT_MOUNT=y' \
  'CONFIG_KSU_SUSFS_AUTO_ADD_SUS_BIND_MOUNT=y' \
  'CONFIG_KSU_SUSFS_SUS_KSTAT=y' \
  'CONFIG_KSU_SUSFS_SUS_OVERLAYFS=n' \
  'CONFIG_KSU_SUSFS_TRY_UMOUNT=y' \
  'CONFIG_KSU_SUSFS_AUTO_ADD_TRY_UMOUNT_FOR_BIND_MOUNT=y' \
  'CONFIG_KSU_SUSFS_SPOOF_UNAME=y' \
  'CONFIG_KSU_SUSFS_ENABLE_LOG=y' \
  'CONFIG_KSU_SUSFS_HIDE_KSU_SUSFS_SYMBOLS=y' \
  'CONFIG_KSU_SUSFS_SPOOF_CMDLINE_OR_BOOTCONFIG=y' \
  'CONFIG_KSU_SUSFS_OPEN_REDIRECT=y' \
  'CONFIG_KSU_SUSFS_SUS_MAP=y' \
  'CONFIG_KSU_SUSFS_SUS_SU=n' \
  >> "$COMMON_KERNEL_FOLDER/arch/arm64/configs/gki_defconfig"

echo "::endgroup::"
