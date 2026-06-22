# GitHub Actions CI Troubleshooting

## Auto-Fix Loop

When asked to fix failing CI automatically:

1. **Check CI status**: `gh pr checks` or `gh run list --branch $(git branch --show-current) --limit 5`
2. **Read failure logs**: `gh run view <RUN_ID> --log-failed`
   - Fallback without `gh`:
     ```bash
     RUN_ID=<id>
     curl -sL -H "Authorization: token $GITHUB_TOKEN" \
       https://api.github.com/repos/$GH_OWNER/$GH_REPO/actions/runs/$RUN_ID/logs \
       -o /tmp/ci-logs.zip && cd /tmp && unzip -o ci-logs.zip -d ci-logs && cat ci-logs/*.txt
     ```
3. **Apply fix**: edit source, commit with conventional commit, push.
4. **Re-check CI**. Repeat ≤3 times, then ask the user if still failing.

## Common Actions
```bash
gh run watch                    # stream live
gh run rerun <RUN_ID>           # rerun entire run
gh run cancel <RUN_ID>          # cancel running workflow
gh run list --workflow <NAME>   # filter by workflow
```

## Output Dependent Status Checks
Inspecting branch protection with `required_status_checks` is the source of truth; do not guess from package.json or similar.