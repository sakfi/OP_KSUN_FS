# 🤖 How to Automate Release Notes

This guide explains how to auto-generate release descriptions (matching `RELEASE_TEMPLATE.md`)
on every GitHub release or workflow run.

---

## Option 1: GitHub Actions — Auto-generate release body on `make_release: true`

### How it works
Add a step at the end of `build-kernel-release.yml` that:
1. Reads `RELEASE_TEMPLATE.md`
2. Substitutes `{{BUILD_DATE}}`, `{{BUILD_ID}}`, `{{WORKFLOW_URL}}` with real values
3. Creates/updates the GitHub Release using the `gh` CLI

### Step to add in `build-kernel-release.yml` (at the end, after all builds succeed)

```yaml
- name: Create GitHub Release with generated notes
  if: ${{ inputs.make_release == 'true' }}
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    BUILD_DATE=$(date -u '+%Y-%m-%d %H:%M:%S UTC')
    BUILD_ID="${{ github.run_id }}"
    WORKFLOW_URL="https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}"
    TAG="${{ inputs.release_tag }}"  # e.g., v1.0.0-r1

    # Substitute placeholders in the template
    sed \
      -e "s|{{BUILD_DATE}}|$BUILD_DATE|g" \
      -e "s|{{BUILD_ID}}|$BUILD_ID|g" \
      -e "s|{{WORKFLOW_URL}}|$WORKFLOW_URL|g" \
      RELEASE_TEMPLATE.md > /tmp/release_body.md

    # Create or update the release
    gh release create "$TAG" \
      --title "OnePlus Kernels With KSUN & SUSFS integrated — SakFi $TAG" \
      --notes-file /tmp/release_body.md \
      --latest

    # Upload all AnyKernel3 ZIPs as release assets
    gh release upload "$TAG" *.zip --clobber
```

---

## Option 2: Auto-update Changelog section from git log

Add this before the `gh release create` step to dynamically generate the changelog:

```bash
# Get commits since last tag
LAST_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")
if [ -n "$LAST_TAG" ]; then
  CHANGELOG=$(git log "$LAST_TAG"..HEAD --pretty=format:"- %s" --no-merges)
else
  CHANGELOG=$(git log --pretty=format:"- %s" --no-merges -10)
fi

# Insert changelog into the template (replaces the static "This Release" section)
awk -v cl="$CHANGELOG" '/### This Release/{print; print cl; skip=1; next} /### Previous/{skip=0} !skip' \
  RELEASE_TEMPLATE.md > /tmp/release_body.md
```

---

## Option 3: Use a dedicated `release.yml` workflow triggered on tag push

Create `.github/workflows/release.yml`:

```yaml
name: Auto Release Notes

on:
  push:
    tags:
      - 'v*'   # Triggers on any tag like v1.0.0-r1

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0   # Full history for git log

      - name: Generate release notes
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          BUILD_DATE=$(date -u '+%Y-%m-%d %H:%M:%S UTC')
          BUILD_ID="${{ github.run_id }}"
          WORKFLOW_URL="https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}"
          TAG="${{ github.ref_name }}"

          # Dynamic changelog from git log since last tag
          LAST_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")
          if [ -n "$LAST_TAG" ]; then
            CHANGELOG=$(git log "$LAST_TAG"..HEAD --pretty=format:"- %s" --no-merges)
          else
            CHANGELOG=$(git log --pretty=format:"- %s" --no-merges -15)
          fi

          # Substitute template placeholders
          sed \
            -e "s|{{BUILD_DATE}}|$BUILD_DATE|g" \
            -e "s|{{BUILD_ID}}|$BUILD_ID|g" \
            -e "s|{{WORKFLOW_URL}}|$WORKFLOW_URL|g" \
            RELEASE_TEMPLATE.md > /tmp/release_body.md

          # Create release
          gh release create "$TAG" \
            --title "OnePlus Kernels With KSUN & SUSFS integrated — SakFi $TAG" \
            --notes-file /tmp/release_body.md \
            --latest
```

---

## How to use it right now (manual release)

To release your **current commit** right now:

```bash
# 1. Tag your commit (on GitHub website or via git)
git tag v1.0.0-r1
git push origin v1.0.0-r1

# 2. On GitHub website:
#    Go to Releases → "Draft a new release"
#    Pick tag: v1.0.0-r1
#    Copy-paste the content of RELEASE_TEMPLATE.md into the description
#    Fill in BUILD_DATE and BUILD_ID from your last workflow run
#    Upload the AnyKernel3 ZIPs from the workflow artifacts
#    Click "Publish release"
```

---

## Summary

| Method | Automation Level | Best For |
|---|---|---|
| Option 1 (inline step) | ✅ Fully automatic | Existing workflow with `make_release` input |
| Option 2 (dynamic changelog) | ✅ Fully automatic + smart | Auto-changelog from git history |
| Option 3 (dedicated workflow) | ✅ Fully automatic on tag push | Tag-based release flow |
| Manual copy-paste | ❌ Manual | Right now, for current commit |
