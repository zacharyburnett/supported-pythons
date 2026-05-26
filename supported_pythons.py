# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "click==8.2.1",
#     "packaging==25.0",
#     "requests==2.32.5",
#     "tomli==2.4.0",
# ]
# ///
import warnings
from pathlib import Path

import click
import requests
import tomli
from packaging.specifiers import SpecifierSet
from packaging.version import Version


@click.command()
@click.option(
    "--package-source",
    help="path to Python package source containing `pyproject.toml`",
    default=None,
)
@click.option(
    "--no-eoas",
    help="also omit end-of-active-support versions of Python",
    is_flag=True,
    default=False,
)
def supported_pythons(
    package_source: Path = None,
    no_eoas: bool = False,
) -> list[str]:
    current_python_versions = current_pythons(no_eoas=no_eoas)

    if not package_source:
        supported_versions = current_python_versions
    else:
        try:
            if Path(package_source).exists():
                pyproject_toml_filename = Path(package_source) / "pyproject.toml"
                if pyproject_toml_filename.exists():
                    with open(pyproject_toml_filename, "rb") as pyproject_toml_file:
                        pyproject_toml = tomli.load(pyproject_toml_file)
                    if "project" in pyproject_toml:
                        project_metadata = pyproject_toml["project"]
                        if "requires-python" in project_metadata:
                            python_version_requirements = SpecifierSet(
                                project_metadata["requires-python"]
                            )
                        else:
                            raise KeyError(
                                "`project.requires-python` not found in `pyproject.toml`; ensure your package conforms to PEP621"
                            )
                    else:
                        raise KeyError(
                            "`project` not found in `pyproject.toml`; ensure your package conforms to PEP621"
                        )
                else:
                    raise FileNotFoundError(
                        "could not find `pyproject.toml` in the provided package source; ensure your package conforms to PEP621"
                    )
            else:
                raise FileNotFoundError(
                    f'package not found at "{package_source}"; retrieving metadata from non-local packages is not yet implemented (checkout the package source first)'
                )

            supported_versions = [
                python_version
                for python_version in current_python_versions
                if python_version in python_version_requirements
            ]
        except (KeyError, TypeError, FileNotFoundError) as error:
            warnings.warn(str(error))
            warnings.warn("falling back to current Python versions...")
            supported_versions = current_python_versions

    supported_versions = list(reversed(supported_versions))

    print("[" + ", ".join([f'"{version}"' for version in supported_versions]) + "]")
    return supported_versions


def current_pythons(no_eoas: bool = False) -> list[Version]:
    url = "https://endoflife.date/api/v1/products/python"
    response = requests.get("https://endoflife.date/api/v1/products/python")
    if response.status_code == 200:
        return [
            Version(python_version["name"])
            for python_version in response.json()["result"]["releases"]
            if not python_version["isEoas" if no_eoas else "isEol"]
        ]
    else:
        raise ValueError(
            f"request to {url} returned status code {response.status_code}"
        )


if __name__ == "__main__":
    supported_pythons()
