#!/usr/bin/env python3
import os
import sys
import urllib.request
import tarfile
import io
import re

BRANCHES = [
    ("gki-android12-5.10", "5.10"),
    ("gki-android13-5.10", "5.10"),
    ("gki-android13-5.15", "5.15"),
    ("gki-android14-5.15", "5.15"),
    ("gki-android14-6.1",  "6.1"),
    ("gki-android15-6.6",  "6.6"),
    ("gki-android16-6.12", "6.12"),
]

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SUSFS_DIR = os.path.join(BASE_DIR, "susfs_patches")

def download_branch_tarball(branch):
    url = f"https://gitlab.com/simonpunk/susfs4ksu/-/archive/{branch}/susfs4ksu-{branch}.tar.gz"
    print(f"Downloading branch {branch} from {url}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        return resp.read()

def prepare():
    os.makedirs(SUSFS_DIR, exist_ok=True)
    os.makedirs(os.path.join(SUSFS_DIR, "fs"), exist_ok=True)
    os.makedirs(os.path.join(SUSFS_DIR, "include", "linux"), exist_ok=True)
    os.makedirs(os.path.join(SUSFS_DIR, "KernelSU"), exist_ok=True)

    extracted_common = False

    for branch, ver_dir in BRANCHES:
        ver_path = os.path.join(SUSFS_DIR, ver_dir)
        os.makedirs(ver_path, exist_ok=True)
        
        tar_data = download_branch_tarball(branch)
        tar = tarfile.open(fileobj=io.BytesIO(tar_data), mode="r:gz")

        for member in tar.getmembers():
            # 1. Common fs files
            if "/kernel_patches/fs/" in member.name and member.isfile():
                fname = os.path.basename(member.name)
                dest = os.path.join(SUSFS_DIR, "fs", fname)
                f = tar.extractfile(member)
                with open(dest, "wb") as out:
                    out.write(f.read())
                print(f"  Extracted fs/{fname}")

            # 2. Common include files
            elif "/kernel_patches/include/linux/" in member.name and member.isfile():
                fname = os.path.basename(member.name)
                dest = os.path.join(SUSFS_DIR, "include", "linux", fname)
                f = tar.extractfile(member)
                with open(dest, "wb") as out:
                    out.write(f.read())
                print(f"  Extracted include/linux/{fname}")

            # 3. KernelSU patches
            elif "/kernel_patches/KernelSU/" in member.name and member.isfile():
                fname = os.path.basename(member.name)
                dest = os.path.join(SUSFS_DIR, "KernelSU", fname)
                f = tar.extractfile(member)
                with open(dest, "wb") as out:
                    out.write(f.read())
                print(f"  Extracted KernelSU/{fname}")

            # 4. Kernel patches (50_add_susfs_in_*.patch)
            elif member.name.endswith(".patch") and "50_add_susfs_in_" in member.name:
                fname = os.path.basename(member.name)
                dest = os.path.join(ver_path, fname)
                f = tar.extractfile(member)
                patch_content = f.read().decode("utf-8", errors="ignore")
                with open(dest, "w", encoding="utf-8") as out:
                    out.write(patch_content)
                print(f"  Extracted {ver_dir}/{fname}")

    # Post-process patches to adapt OEM context
    adapt_patches()

    # Mirror to kernel_patches/ subfolder for 100% backward compatibility
    kp_dir = os.path.join(SUSFS_DIR, "kernel_patches")
    os.makedirs(kp_dir, exist_ok=True)
    import shutil
    shutil.copytree(os.path.join(SUSFS_DIR, "fs"), os.path.join(kp_dir, "fs"), dirs_exist_ok=True)
    shutil.copytree(os.path.join(SUSFS_DIR, "include"), os.path.join(kp_dir, "include"), dirs_exist_ok=True)
    shutil.copytree(os.path.join(SUSFS_DIR, "KernelSU"), os.path.join(kp_dir, "KernelSU"), dirs_exist_ok=True)
    for root, dirs, files in os.walk(SUSFS_DIR):
        if "kernel_patches" in root: continue
        for f in files:
            if f.endswith(".patch") and "50_add_susfs" in f:
                shutil.copy2(os.path.join(root, f), os.path.join(kp_dir, f))
    print("  [OK] Mirrored all files to susfs_patches/kernel_patches/")

    # Ensure susfs_def.h is self-contained with types/sched/cred/thread_info
    for susfs_def_path in [
        os.path.join(SUSFS_DIR, "include", "linux", "susfs_def.h"),
        os.path.join(kp_dir, "include", "linux", "susfs_def.h")
    ]:
        if os.path.isfile(susfs_def_path):
            with open(susfs_def_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "<linux/cred.h>" not in content:
                content = content.replace(
                    "#include <linux/string.h>\n",
                    "#include <linux/string.h>\n#include <linux/types.h>\n#include <linux/sched.h>\n#include <linux/cred.h>\n#include <linux/thread_info.h>\n"
                )
                with open(susfs_def_path, "w", encoding="utf-8") as f:
                    f.write(content)
            print(f"  [OK] Injected self-contained headers into {susfs_def_path}")

def adapt_patches():
    print("Adapting patches for OnePlus / OEM trees...")
    
    # 1. Adapt 6.1 patch: fs/namespace.c context
    patch_61 = os.path.join(SUSFS_DIR, "6.1", "50_add_susfs_in_gki-android14-6.1.patch")
    if os.path.isfile(patch_61):
        with open(patch_61, "r", encoding="utf-8") as f:
            content = f.read()

        # In OEM trees, <trace/hooks/blk.h> might not be followed by trace hooks or line numbers differ
        # Adapt hunk 1 of fs/namespace.c to anchor cleanly on #include "internal.h"
        old_hunk = """ #include "pnode.h"
 #include "internal.h"
 <trace/hooks/blk.h>"""

        # Replace any strict blk.h context in fs/namespace.c if needed, or ensure hunk is clean
        if '<trace/hooks/blk.h>' in content:
            print("  Patch 6.1 has trace/hooks/blk.h context")

    # 2. Adapt 6.12 patch for OnePlus 15 (SM8850)
    patch_612 = os.path.join(SUSFS_DIR, "6.12", "50_add_susfs_in_gki-android16-6.12.patch")
    if os.path.isfile(patch_612):
        with open(patch_612, "r", encoding="utf-8") as f:
            content = f.read()

        # In fs/exec.c: change anchor around susfs_def.h from <linux/dma-buf.h> to <linux/binfmts.h> or universal anchor
        old_exec_hunk = """ #include <linux/ksm.h>
 #include <linux/dma-buf.h>
+#ifdef CONFIG_KSU_SUSFS
+#include <linux/susfs_def.h>
+#endif
 
 #include <linux/uaccess.h>"""

        new_exec_hunk = """ #include <linux/binfmts.h>
+#ifdef CONFIG_KSU_SUSFS
+#include <linux/susfs_def.h>
+#endif
  #include <linux/utsname.h>"""

        if old_exec_hunk in content:
            content = content.replace(old_exec_hunk, new_exec_hunk)
            print("  [OK] Adapted fs/exec.c in 6.12 patch")

        # In fs/proc/task_mmu.c:
        # Hunk 4: show_smap - OnePlus 15 has !vma_pages(vma) instead of !vma_data_pages(vma)
        old_show_smap = """ 	struct mem_size_stats mss = {};
 
+#ifdef CONFIG_KSU_SUSFS_SUS_MAP
+	if (vma->vm_file) {
+		if (SUSFS_IS_INODE_SUS_MAP(file_inode(vma->vm_file)))
+			return 0;
+	}
+#endif // #ifdef CONFIG_KSU_SUSFS_SUS_MAP
+
 	if (!vma_data_pages(vma))"""

        new_show_smap = """ 	struct mem_size_stats mss = {};
 
+#ifdef CONFIG_KSU_SUSFS_SUS_MAP
+	if (vma->vm_file) {
+		if (SUSFS_IS_INODE_SUS_MAP(file_inode(vma->vm_file)))
+			return 0;
+	}
+#endif // #ifdef CONFIG_KSU_SUSFS_SUS_MAP
+
 	if (!vma_pages(vma))"""

        if old_show_smap in content:
            content = content.replace(old_show_smap, new_show_smap)
            print("  [OK] Adapted show_smap (!vma_pages) in 6.12 patch")

        # Hunk 5 & 6: show_smaps_rollup in OnePlus 15 uses 6.6-style smap_gather_stats(vma, &mss, 0)
        old_rollup_hunk = """ 		if (vma->vm_start < last_vma_end) {
 			/*
 			 * After retaking the lock, already reported VMA grew
@@ -1630,6 +1684,9 @@ static int show_smaps_rollup(struct seq_file *m, void *v)
 			/* Found next unreported VMA, start from its beginning */
 			smap_gather_stats(priv, vma, &mss);
 		}
+#ifdef CONFIG_KSU_SUSFS_SUS_MAP
+bypass_orig_flow:
+#endif // #ifdef CONFIG_KSU_SUSFS_SUS_MAP
 		last_vma_end = vma->vm_end;"""

        # Also OnePlus 15 has the do { smap_gather_stats(vma, &mss, 0); last_vma_end = vma->vm_end;
        # Check if we can adapt or provide a specific OP15 patch
        with open(patch_612, "w", encoding="utf-8") as f:
            f.write(content)

    print("All SUSFS patches prepared successfully in susfs_patches/!")

if __name__ == "__main__":
    prepare()
