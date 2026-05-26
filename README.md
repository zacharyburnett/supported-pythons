# supported-pythons

[![test](https://github.com/zacharyburnett/supported-pythons/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/zacharyburnett/supported-pythons/actions/workflows/test.yml)

retrieve active (not end-of-life) minor versions of Python supported by a Python package

| input         | description                                                                                         |
| ------------- | --------------------------------------------------------------------------------------------------- |
| `package`     | path to Python package source containing `pyproject.toml`, from which to retrieve `requires-python` |
| `no-eoas`     | omit end-of-active-support versions of Python                                                       |
| `latest-only` | only return the latest supported minor version of Python                                            |

```yaml
- uses: actions/checkout@v6
  with:
    repository: spacetelescope/romancal
- id: supported-pythons
  uses: zacharyburnett/supported-pythons@v1.0.0
  with:
    package: .
- run: echo ${{ steps.supported-pythons.outputs.versions }}
```

```json
["3.11", "3.12", "3.13", "3.14"]
```
