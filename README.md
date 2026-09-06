<p align="center">
  <img src="https://raw.githubusercontent.com/Coccinella-Labs/echo/main/.github/assets/thumbnail.png" alt="echo" width="100%">
</p>

# echo

[![Release](https://img.shields.io/github/v/release/libnudget/echo?logo=github&label=latest)](https://github.com/libnudget/echo/releases)

Reusable GitHub Action for suggesting potentially similar issues and upserting a triage comment.

It is designed for issue `opened`, `edited`, or `reopened` events, and it works by:

- fetching a recent set of issues from the target repository
- scoring overlap from issue titles and bodies
- grouping likely matches into open and closed sections
- posting or updating a single bot comment marked with a hidden marker

## Requirements

- GitHub Actions runner with `gh`, `jq`, and `python3`
- `issues: write` permission
- `contents: read` permission

## Example

```yaml
name: Suggest Similar Issues

on:
  issues:
    types: [opened, reopened, edited]

jobs:
  suggest-similar:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      issues: write
    steps:
      - uses: actions/checkout@v4
      - uses: libnudget/echo@main
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          repository: ${{ github.repository }}
          issue_number: ${{ github.event.issue.number }}
          issue_title: ${{ github.event.issue.title }}
          issue_body: ${{ github.event.issue.body }}
```

## Inputs

| Name | Required | Default | Notes |
| --- | --- | --- | --- |
| `github_token` | yes | | Token with issue write access |
| `repository` | yes | | `owner/name` repository |
| `issue_number` | yes | | Current issue number |
| `issue_title` | yes | | Current issue title |
| `issue_body` | no | `""` | Current issue body |
| `issue_limit` | no | `100` | How many issues to fetch |
| `result_limit` | no | `10` | How many scored matches to keep |
| `visible_per_state` | no | `3` | How many open or closed lines to show |
| `marker` | no | `<!-- issue-similarity-check -->` | Hidden marker for comment updates |
| `intro_text` | no | standard text | Comment intro |
| `outro_text` | no | standard text | Comment outro |
| `footer_text` | no | `@libnudget` | Footer mention or link |
| `stopwords_regex` | no | built-in regex | Words ignored during scoring |

## Notes

- The action only comments when it has at least one visible match line.
- Existing bot comments with the same marker are updated instead of duplicated.
- The scoring is intentionally lightweight and heuristic-based.

## License

MIT
