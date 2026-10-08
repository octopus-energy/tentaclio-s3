#!/usr/bin/env python
"""Verify that the git tag matches the package version."""
import os
import sys
from pathlib import Path
import tomllib


def main():
    # Read tentaclio-s3 package version from pyproject.toml:
    pyproject_path = Path(__file__).resolve().parent.parent / "pyproject.toml"

    with pyproject_path.open("rb") as f:
        pyproject = tomllib.load(f)

    package_version = pyproject.get("project", {}).get("version")
    if not package_version:
        print("✗ ERROR: Could not find tentaclio-s3 package version in pyproject.toml")
        sys.exit(1)

    # Get git tag from GitHub Release Action:
    git_tag = os.getenv("GITHUB_REF_NAME")
    if not git_tag:
        print("✗ ERROR: No GitHub release tag found")
        sys.exit(1)

    # Verify GitHub release tag matches the package version:
    if git_tag != package_version:
        print(
            f"✗ ERROR: GitHub release tag '{git_tag}' does not match package version "
            f"'{package_version}'"
        )
        sys.exit(1)

    print(f"✓ Version verified: {package_version}")
    sys.exit(0)


if __name__ == "__main__":
    main()
