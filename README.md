# supported-pythons

[![test](https://github.com/zacharyburnett/supported-pythons/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/zacharyburnett/supported-pythons/actions/workflows/test.yml)

retrieve active (not end-of-life) minor versions of Python supported by a Python package

| input         | description                                              |
| ------------- | -------------------------------------------------------- |
| `package`     | package source repository containing `pyproject.toml`    |
| `package-ref` | branch / tag of package                                  |
| `no-eoas`     | also omit end-of-active-support versions of Python       |
| `latest-only` | only return the latest supported minor version of Python |

```yaml
- id: supported-pythons
  uses: zacharyburnett/supported-pythons@v1.1.0
  with:
    package: spacetelescope/romancal
- run: echo ${{ steps.supported-pythons.outputs.versions }}
```

```json
["3.11", "3.12", "3.13", "3.14"]
```
