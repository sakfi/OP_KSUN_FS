#!/usr/bin/env python3
import os
import sys

def patch_ksun(ksun_folder):
    print(f"Applying KSUN 33400+ SUSFS fixes to {ksun_folder}...")
    
    # 1. Fix dispatch.c
    dispatch_path = os.path.join(ksun_folder, "kernel", "supercall", "dispatch.c")
    if os.path.isfile(dispatch_path):
        with open(dispatch_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Remove MODULE and late_loaded in do_get_info
        old_do_get_info = """static int do_get_info(void __user *arg)
{
    struct ksu_get_info_cmd cmd = { .version = KERNEL_SU_VERSION, .flags = 0 };

#ifdef MODULE
    cmd.flags |= KSU_GET_INFO_FLAG_LKM;
    if (ksu_bundled) {
        cmd.flags |= KSU_GET_INFO_FLAG_BUNDLED;
    }
#endif

    if (ksuver_override)
        cmd.version = ksuver_override;

    if (is_manager()) {
        cmd.flags |= KSU_GET_INFO_FLAG_MANAGER;
    }
    if (ksu_late_loaded) {
        cmd.flags |= KSU_GET_INFO_FLAG_LATE_LOAD;
    }
    // A late load never sees PID 1's selinux_setup, so preinit cannot run.
    if (ksu_preinit_enabled_param() && !ksu_late_loaded) {
        cmd.flags |= KSU_GET_INFO_FLAG_PREINIT;
    }
    cmd.features = KSU_FEATURE_MAX;
    cmd.uapi_version = KERNEL_SU_UAPI_VERSION;"""

        new_do_get_info = """static int do_get_info(void __user *arg)
{
    struct ksu_get_info_cmd cmd = { .version = KERNEL_SU_VERSION, .flags = 0 };

    if (ksuver_override)
        cmd.version = ksuver_override;

    if (is_manager()) {
        cmd.flags |= KSU_GET_INFO_FLAG_MANAGER;
    }
    // A late load never sees PID 1's selinux_setup, so preinit cannot run.
    if (ksu_preinit_enabled_param()) {
        cmd.flags |= KSU_GET_INFO_FLAG_PREINIT;
    }
    cmd.features = KSU_FEATURE_MAX;
    cmd.uapi_version = KERNEL_SU_UAPI_VERSION;"""

        old_do_get_info_legacy = """static int do_get_info_legacy(void __user *arg)
{
    struct ksu_get_info_legacy_cmd cmd = { .version = KERNEL_SU_VERSION, .flags = 0 };

#ifdef MODULE
    cmd.flags |= KSU_GET_INFO_FLAG_LKM;
    if (ksu_bundled) {
        cmd.flags |= KSU_GET_INFO_FLAG_BUNDLED;
    }
#endif

    if (is_manager()) {
        cmd.flags |= KSU_GET_INFO_FLAG_MANAGER;
    }
    if (ksu_late_loaded) {
        cmd.flags |= KSU_GET_INFO_FLAG_LATE_LOAD;
    }
    cmd.features = KSU_FEATURE_MAX;"""

        new_do_get_info_legacy = """static int do_get_info_legacy(void __user *arg)
{
    struct ksu_get_info_legacy_cmd cmd = { .version = KERNEL_SU_VERSION, .flags = 0 };

    if (is_manager()) {
        cmd.flags |= KSU_GET_INFO_FLAG_MANAGER;
    }
    cmd.features = KSU_FEATURE_MAX;"""

        if old_do_get_info in content:
            content = content.replace(old_do_get_info, new_do_get_info)
            print("  [OK] Fixed do_get_info in dispatch.c")
        if old_do_get_info_legacy in content:
            content = content.replace(old_do_get_info_legacy, new_do_get_info_legacy)
            print("  [OK] Fixed do_get_info_legacy in dispatch.c")

        with open(dispatch_path, "w", encoding="utf-8") as f:
            f.write(content)

        # Remove reject file
        rej = os.path.join(ksun_folder, "kernel", "supercall", "dispatch.c.rej")
        if os.path.isfile(rej):
            os.remove(rej)
            print("  [OK] Removed dispatch.c.rej")

    # 2. Fix init.c
    init_path = os.path.join(ksun_folder, "kernel", "core", "init.c")
    if os.path.isfile(init_path):
        with open(init_path, "r", encoding="utf-8") as f:
            content = f.read()

        if "#include <linux/susfs.h>" not in content:
            content = content.replace(
                '#include <linux/workqueue.h>\n',
                '#include <linux/workqueue.h>\n#include <linux/susfs.h>\n'
            )

        old_includes = """#include "selinux/selinux.h"
#include "hook/syscall_hook.h"
#include "feature/adb_root.h"
#include "feature/selinux_hide.h"
#include "feature/module_blacklist.h"
#include "feature/shell_su_adb_only.h"
#include "feature/sulog.h"
#include "infra/symbol_resolver.h"
#include "preinit/preinit.h"

#if defined(__x86_64__) && !defined(CONFIG_KSU_X86_PATCH_SYSCALL_DISPATCHER)
#include <asm/cpufeature.h>
#include <linux/version.h>
#ifndef X86_FEATURE_INDIRECT_SAFE
#error "FATAL: Your kernel is missing the indirect syscall bypass patches!"
#endif
#endif"""

        new_includes = """#include "selinux/selinux.h"
#include "feature/adb_root.h"
#include "feature/selinux_hide.h"
#include "feature/module_blacklist.h"
#include "feature/shell_su_adb_only.h"
#include "feature/sulog.h"
#include "preinit/preinit.h"
#include "hook/setuid_hook.h"
#include "feature/sucompat.h\""""

        if old_includes in content:
            content = content.replace(old_includes, new_includes)
            print("  [OK] Replaced hook includes in init.c")

        old_bundled = """#ifdef MODULE
bool ksu_bundled = false;
module_param_named(bundled, ksu_bundled, bool, 0);
#endif"""
        if old_bundled in content:
            content = content.replace(old_bundled, "")

        old_late_loaded = """#ifdef MODULE
\tksu_late_loaded = (current->pid != 1);
#else
\tksu_late_loaded = false;
#endif"""
        if old_late_loaded in content:
            content = content.replace(old_late_loaded, "")

        old_init_body = """\tksu_cred = prepare_creds();
\tif (!ksu_cred) {
\t\tpr_err("prepare cred failed!\\n");
\t\treturn -ENOSYS;
\t}

\tksu_init_symbol_resolver();
\tksu_syscall_hook_init();

\t// Block modules early, before vendor modules are loaded in second stage.
\tksu_module_blacklist_init();

\tksu_feature_init();
\tksu_sulog_init();
\tksu_adb_root_init();
\tksu_lsm_hook_init();
\tksu_selinux_hide_init();
\tksu_shell_su_adb_only_init();

\tksu_supercalls_init();
\tksu_app_profile_init();

\tif (ksu_late_loaded) {
\t\tpr_info("late load mode, skipping kprobe hooks\\n");

\t\tapply_kernelsu_rules();
\t\tcache_sid();
\t\tsetup_ksu_cred();

\t\t// Grant current process (ksud late-load) root
\t\t// with KSU SELinux domain before enforcing SELinux, so it
\t\t// can continue to access /data/app etc. after enforcement.
\t\tescape_to_root_for_init();

\t\tksu_allowlist_init();
\t\tksu_load_allow_list();

\t\tksu_syscall_hook_manager_init();

\t\tksu_throne_tracker_init();
\t\tksu_observer_init();
\t\tksu_file_wrapper_init();

\t\tksu_boot_completed = true;
\t\ttrack_throne(false);

\t\tksu_feature_apply_forced();

\t\tif (!getenforce()) {
\t\t\tpr_info("Permissive SELinux, enforcing\\n");
\t\t\tsetenforce(true);
\t\t}

\t} else {
\t\tksu_syscall_hook_manager_init();

\t\tksu_allowlist_init();

\t\tksu_throne_tracker_init();

\t\tksu_ksud_init();

\t\tksu_preinit_init();

\t\tksu_file_wrapper_init();
\t}

#ifdef MODULE
#ifndef CONFIG_KSU_DEBUG
\tkobject_del(&THIS_MODULE->mkobj.kobj);
#endif
#endif
\treturn 0;
}

void __exit kernelsu_exit(void)
{
\t// Phase 1: Stop all hooks first to prevent new callbacks
\tksu_syscall_hook_manager_exit();

\tksu_supercalls_exit();

\tif (!ksu_late_loaded) {
\t\tksu_ksud_exit();
\t\tksu_preinit_exit();
\t}"""

        new_init_body = """\tksu_cred = prepare_creds();
\tif (!ksu_cred) {
\t\tpr_err("prepare cred failed!\\n");
\t\treturn -ENOSYS;
\t}

#ifdef CONFIG_KSU_SUSFS
    susfs_init();
#endif // #ifdef CONFIG_KSU_SUSFS

\t// Block modules early, before vendor modules are loaded in second stage.
\tksu_module_blacklist_init();

\tksu_feature_init();

\tksu_supercalls_init();
    ksu_sucompat_init();

    ksu_setuid_hook_init();

    ksu_sulog_init();

    ksu_adb_root_init();

    ksu_selinux_hide_init();

    ksu_shell_su_adb_only_init();

\tksu_allowlist_init();

\tksu_throne_tracker_init();

\tksu_ksud_init();

\tksu_preinit_init();

\tksu_file_wrapper_init();

\treturn 0;
}

void __exit kernelsu_exit(void)
{
\tksu_supercalls_exit();

\tksu_ksud_exit();
\tksu_preinit_exit();"""

        if old_init_body in content:
            content = content.replace(old_init_body, new_init_body)
            print("  [OK] Updated kernelsu_init and kernelsu_exit in init.c")

        content = content.replace('\tksu_lsm_hook_exit();\n', '')

        with open(init_path, "w", encoding="utf-8") as f:
            f.write(content)

        rej = os.path.join(ksun_folder, "kernel", "core", "init.c.rej")
        if os.path.isfile(rej):
            os.remove(rej)
            print("  [OK] Removed init.c.rej")

    # 3. Fix sucompat.c
    sucompat_path = os.path.join(ksun_folder, "kernel", "feature", "sucompat.c")
    if os.path.isfile(sucompat_path):
        with open(sucompat_path, "r", encoding="utf-8") as f:
            content = f.read()

        changed = False
        # Ensure util.h is included for userspace_stack_buffer
        if '#include "util.h"' not in content:
            if '#include "runtime/ksud.h"' in content:
                content = content.replace('#include "runtime/ksud.h"', '#include "runtime/ksud.h"\n#include "util.h"')
                changed = True
            elif '#include "feature/sucompat.h"' in content:
                content = content.replace('#include "feature/sucompat.h"', '#include "feature/sucompat.h"\n#include "util.h"')
                changed = True

        # Remove duplicate get_user_arg_ptr since runtime/ksud.h already defines it inline
        import re
        pattern = r'static const char __user \*get_user_arg_ptr\(struct user_arg_ptr argv, int nr\)\s*\{.*?\n\}\n'
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, '', content, flags=re.DOTALL)
            changed = True
            print("  [OK] Removed duplicate get_user_arg_ptr from sucompat.c")

        if changed:
            with open(sucompat_path, "w", encoding="utf-8") as f:
                f.write(content)
            print("  [OK] Patched sucompat.c with util.h and removed redefinition")

        rej = os.path.join(ksun_folder, "kernel", "feature", "sucompat.c.rej")
        if os.path.isfile(rej):
            os.remove(rej)
            print("  [OK] Removed sucompat.c.rej")

    # 4. Fix rules.c
    rules_path = os.path.join(ksun_folder, "kernel", "selinux", "rules.c")
    if os.path.isfile(rules_path):
        with open(rules_path, "r", encoding="utf-8") as f:
            content = f.read()

        changed = False
        if "susfs_set_batch_sid();" not in content and "void apply_kernelsu_rules()" in content:
            if "out_unlock:" in content:
                content = content.replace("out_unlock:", "    susfs_set_batch_sid();\nout_unlock:", 1)
                changed = True
                print("  [OK] Injected susfs_set_batch_sid() into rules.c")

        if changed:
            with open(rules_path, "w", encoding="utf-8") as f:
                f.write(content)

        rej = os.path.join(ksun_folder, "kernel", "selinux", "rules.c.rej")
        if os.path.isfile(rej):
            os.remove(rej)
            print("  [OK] Removed rules.c.rej")

if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "."
    patch_ksun(folder)

