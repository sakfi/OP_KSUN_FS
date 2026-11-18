#!/usr/bin/env python3
"""
Telegram release notification sender for OnePlus Kernels.
Supports release events and manual workflow_dispatch triggers.
Ensures HTML entity safety and includes an automatic plain-text fallback.
"""

import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request


def fetch_release_data(repo, rel_tag, gh_token):
    """Fetch release details from GitHub API if triggering manually."""
    url = f"https://api.github.com/repos/{repo}/releases/tags/{rel_tag}"
    headers = {"User-Agent": "GitHub-Action"}
    if gh_token:
        headers["Authorization"] = f"token {gh_token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return {
            "name": data.get("name", ""),
            "body": data.get("body", ""),
            "url": data.get("html_url", ""),
        }


def extract_features(rel_body):
    """Extract and group features from release body table."""
    fallback = (
        "Features:\n"
        "- Integrated: KernelSU-Next & SUSFS\n"
        "- Optimized for performance and battery life (LTO, Optimization, Battery)\n"
        "- Network features (BBRv3, TTL Target Support, WireGuard)\n"
        "- Advanced features (Droidspaces, NTSync, HMBIRD SCX, TMPFS XATTR)\n"
        "- Enhanced security (BBG)"
    )
    if not rel_body:
        return fallback

    lines = rel_body.splitlines()
    in_features = False
    feature_items = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## ✨ Features"):
            in_features = True
            continue
        if in_features:
            if (
                stripped.startswith("---")
                or stripped.startswith("<")
                or (stripped.startswith("## ") and not stripped.startswith("## ✨ Features"))
            ):
                break
            if (
                stripped.startswith("|")
                and stripped.endswith("|")
                and not stripped.startswith("|:---")
                and not stripped.startswith("| Feature")
            ):
                parts = [p.strip() for p in stripped.strip("|").split("|")]
                if len(parts) >= 2:
                    name = parts[0].replace("**", "").replace("`", "").strip()
                    name_clean = re.sub(r"^[^\w\s]+\s*", "", name)
                    desc = parts[1].strip()
                    feature_items.append((name_clean, desc))

    if not feature_items:
        return fallback

    variants, network, advanced, security, optimization = [], [], [], [], []
    for name, desc in feature_items:
        lower = name.lower()
        if "kernelsu" in lower or "susfs" in lower:
            variants.append(name)
        elif any(k in lower for k in ["bbr", "wireguard", "ttl", "ip.set", "ipset"]):
            network.append(name)
        elif any(k in lower for k in ["droidspaces", "ntsync", "hmbird", "tmpfs", "sdp", "charging"]):
            advanced.append(name)
        elif any(k in lower for k in ["bbg", "manual.hooks", "unicode", "socket"]):
            security.append(name)
        elif any(k in lower for k in ["lto", "optimization", "battery", "mlgo"]):
            optimization.append(name)

    opt_str = ", ".join(optimization) if optimization else "LTO, Optimization, Battery"
    net_str = ", ".join(network) if network else "BBRv3, TTL Target Support, WireGuard"
    adv_str = ", ".join(advanced) if advanced else "Droidspaces, NTSync, HMBIRD SCX, TMPFS XATTR"
    sec_str = ", ".join(security) if security else "BBG"

    return (
        "Features:\n"
        "- Integrated: KernelSU-Next & SUSFS\n"
        f"- Optimized for performance and battery life ({opt_str})\n"
        f"- Network features ({net_str})\n"
        f"- Advanced features ({adv_str})\n"
        f"- Enhanced security ({sec_str})"
    )


def extract_changelog(rel_body):
    """Read changelog from changelog.txt or release body fallback."""
    if os.path.exists("changelog.txt") and os.path.getsize("changelog.txt") > 0:
        try:
            with open("changelog.txt", "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    return content
        except Exception as e:
            print(f"Warning reading changelog.txt: {e}")

    if rel_body:
        lines = rel_body.splitlines()
        in_release = False
        changelog_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("### This Release"):
                in_release = True
                continue
            if in_release:
                if (
                    stripped.startswith("### Previous Releases")
                    or stripped.startswith("---")
                    or stripped.startswith("## ")
                ):
                    break
                if stripped.startswith("- ") or stripped.startswith("• "):
                    changelog_lines.append(stripped)
        if changelog_lines:
            return "\n".join(changelog_lines)

    return "- Minor updates and under the hood improvements"


def send_telegram(bot_token, chat_id, message_html):
    """Send message to Telegram with HTML formatting, retrying with plain text on error."""
    if not chat_id:
        print("Warning: chat_id is empty, skipping.")
        return True

    print(f"Sending message to {chat_id}...")
    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": message_html,
        "parse_mode": "HTML",
    }).encode("utf-8")

    try:
        req = urllib.request.Request(api_url, data=payload, method="POST")
        with urllib.request.urlopen(req, timeout=20) as resp:
            res_data = json.loads(resp.read().decode("utf-8"))
            if res_data.get("ok"):
                print(f"Successfully sent HTML message to {chat_id}")
                return True
            print(f"Warning: HTML mode returned ok=false: {res_data}")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"Warning: HTML mode failed with HTTP {e.code}: {err_body}")
    except Exception as e:
        print(f"Warning: HTML mode failed: {e}")

    # Fallback to plain text
    print(f"Retrying with plain-text fallback for {chat_id}...")
    clean_text = re.sub(r"<[^>]+>", "", message_html)
    plain_text = html.unescape(clean_text)

    if len(plain_text) > 4000:
        plain_text = plain_text[:3990] + "... (truncated)"

    fb_payload = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": plain_text,
    }).encode("utf-8")

    try:
        req = urllib.request.Request(api_url, data=fb_payload, method="POST")
        with urllib.request.urlopen(req, timeout=20) as resp:
            fb_data = json.loads(resp.read().decode("utf-8"))
            if fb_data.get("ok"):
                print(f"Successfully sent plain-text fallback to {chat_id}")
                return True
            print(f"Error: Plain text fallback returned ok=false: {fb_data}")
            return False
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"::error::Plain text fallback failed with HTTP {e.code}: {err_body}")
        return False
    except Exception as e:
        print(f"::error::Plain text fallback failed: {e}")
        return False


def main():
    bot_token = os.environ.get("BOT_TOKEN", "").strip()
    group_id = os.environ.get("GROUP_ID", "").strip()
    channel_id = os.environ.get("CHANNEL_ID", "").strip()
    rel_name = os.environ.get("REL_NAME", "").strip()
    rel_tag = os.environ.get("REL_TAG", "").strip()
    rel_url = os.environ.get("REL_URL", "").strip()
    rel_body = os.environ.get("REL_BODY", "").strip()
    repo = os.environ.get("REPO", "").strip()
    gh_token = os.environ.get("GH_TOKEN", "").strip()
    event_action = os.environ.get("EVENT_ACTION", "").strip()
    event_name = os.environ.get("EVENT_NAME", "").strip()

    if not bot_token:
        print("Error: TELEGRAM_BOT_TOKEN is not configured.")
        sys.exit(1)

    # Handle manual trigger or missing release data
    if (not rel_name or not rel_body) and rel_tag:
        print(f"Fetching release details for tag: {rel_tag}")
        try:
            rel_info = fetch_release_data(repo, rel_tag, gh_token)
            rel_name = rel_name or rel_info.get("name", "")
            rel_body = rel_body or rel_info.get("body", "")
            rel_url = rel_url or rel_info.get("url", "")
        except Exception as e:
            print(f"Warning: Could not fetch release data from GitHub API: {e}")

    if not rel_tag:
        print("Error: No release tag provided and no release event data found.")
        sys.exit(1)

    # Status & Emoji
    emoji = "🚀"
    status = "New Release Published"
    if event_action == "edited":
        emoji = "✏️"
        status = "Release Notes Updated"
    elif event_name == "workflow_dispatch":
        emoji = "📢"
        status = "Manual Notification"

    features_block = extract_features(rel_body)
    changelog = extract_changelog(rel_body)

    # Limit changelog length to stay well below Telegram's 4096 limit
    if len(changelog) > 2500:
        changelog = changelog[:2500] + "... (truncated)"

    # HTML Entity Escaping (critical for Telegram HTML parse_mode)
    esc_tag = html.escape(rel_tag, quote=False)
    esc_name = html.escape(rel_name, quote=False)
    esc_features = html.escape(features_block, quote=False)
    esc_changelog = html.escape(changelog, quote=False)
    esc_url = html.escape(rel_url, quote=True)

    message_html = f"""<b>{emoji} {status}</b>

<pre><code class="language-markdown">Kernel Name: OnePlus Kernels with KSUN &amp; SUSFS
Version / Tag: {esc_tag}
Title: {esc_name}
Device: Any supported OnePlus device (Check GitHub for your device)

{esc_features}

Changelog:
{esc_changelog}</code></pre>

<b>Important:</b>
- Flash via Kernel Flasher (for KernelSU/Next) or FKM.
- If you run into issues, please provide logs in the GitHub repository.
- Support the development by leaving a 🌟 on GitHub!

🔗 <a href="{esc_url}">Download Release on GitHub</a>"""

    success = True
    for chat in [group_id, channel_id]:
        if chat:
            if not send_telegram(bot_token, chat, message_html):
                success = False

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
