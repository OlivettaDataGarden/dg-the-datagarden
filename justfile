import "/Users/maartenderuyter/Documents/dg-development/dg_justfile/Justfile"

# Local vars:
IS_PACKAGE := "true"
COMMIT_PREFIX := "DGDG"
REPO_NAME := "dg-the-datagarden"


tox:
    uv run tox
