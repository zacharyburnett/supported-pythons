# supported-pythons

[![test](https://github.com/zacharyburnett/supported-pythons/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/zacharyburnett/supported-pythons/actions/workflows/test.yml)

retrieve active (not end-of-life) minor versions of Python supported by a Python package

| input         | description                                           |
| ------------- | ----------------------------------------------------- |
| `package`     | package source repository containing `pyproject.toml` |
| `package-ref` | branch or tag of package source                       |
| `no-eoas`     | also omit end-of-active-support versions of Python    |

| output     | description                           |
| ---------- | ------------------------------------- |
| `versions` | Python minor versions as a JSON list  |
| `oldest`   | oldest supported Python minor version |
| `latest`   | latest supported Python minor version |

```yaml
jobs:
  supported-pythons:
    runs-on: ubuntu-latest
    steps:
      - id: supported-pythons
        uses: zacharyburnett/supported-pythons@2.0.0
        with:
          package: spacetelescope/romancal
    outputs:
      versions: ${{ steps.supported-pythons.outputs.versions }}
  test:
    needs: supported-pythons
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ${{ fromJSON(needs.supported-pythons.outputs.versions) }}
    steps:
      - uses: actions/setup-python@v6
        with:
          python-version: ${{ matrix.python-version }}
      - uses: actions/checkout@v6
      - run: pip install . pytest
      - run: pytest
```
