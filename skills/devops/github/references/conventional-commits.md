# Conventional Commits Cheat Sheet

```
type(scope): short description

[optional body]
[optional footer(s)]
```

## Types
| Type | Purpose |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `docs` | Documentation only |
| `style` | Formatting / lint (no code change) |
| `test` | Adding / fixing tests |
| `chore` | Build / tooling / maintenance |
| `perf` | Performance improvement |
| `ci` | CI config |
| `revert` | Revert a previous commit |

## Formatting tips
- Short description ≤ 50 chars.
- Blank line between subject and body.
- Body wrap ≤ 72 chars.
- Body explains WHY, not WHAT (git diff shows what).
- Use imperative mood: `fix bug` not `fixed bug`.

## Branch naming
`feat/auth`, `fix/login`, `refactor/cache`, `docs/readme`

## Release tags (SemVer)
`MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`
`BREAKING CHANGE:` → major (when in commit body/footer).