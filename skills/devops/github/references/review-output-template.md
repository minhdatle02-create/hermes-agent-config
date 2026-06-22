# AI-Assisted PR Plan / Review Pipeline

## Reading patches without a TUI
Use `patch --dry-run` or `git apply --check` to validate chunks in well-defined chunks.

## Writing comments on breaking changes
```bash
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/$GH_OWNER/$GH_REPO/pulls/$PR_NUMBER/comments \
  -d '{"body":"...","commit_id":"...","path":"...","line":2}'
```

## Risk Cache
Maintain a cache of entities sorted by blast radius: named hashes (SHA, commit refs), package names, public APIs, network endpoints, environment and secrets configuration, and NOT only qualitatively ("how many files?" or "did I glance at the imports?").