# GitHub Auth Setup Reference

## Detection Flow (PreFlight / no-auth path)
```bash
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH=gh
else
  AUTH=git
  if [ -z "$GITHUB_TOKEN" ]; then
    if [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=*** ~/.hermes/.env; then
      GITHUB_TOKEN=*** "^GITHUB_TOKEN=*** ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\n\r')
    elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then
      GITHUB_TOKEN=*** "github.com" ~/.git-credentials | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
    fi
  fi
fi
```

## Method 1: Git-Only

Option A — HTTPS PAT: Create a classic token at `https://github.com/settings/tokens` with scopes `repo`, `workflow`, `read:org`. Use `git config --global credential.helper store`, or paste PAT at password prompt.

Option B — SSH key: `ssh-keygen -t ed25519`, add public key to GitHub→Settings→SSH→New SSH key. Test with `ssh -T git@github.com`.

## Method 2: gh CLI

```bash
gh auth login                        # interactive browser flow
echo "<token>" | gh auth login --with-token   # headless
gh auth status                       # verify
```

## Using the API without gh
```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `git push` asks for password | GitHub deprecated password auth; use PAT as password or switch to SSH |
| `remote: Permission to X denied` | Token likely lacks `repo` scope |
| `ssh: connect to host github.com port 22: Connection refused` | Use port 443 fallback: add `Host github.com` / `Port 443` / `Hostname ssh.github.com` to `~/.ssh/config` |
| `gh: command not found` | No admin rights / not in PATH; use Method 1 |