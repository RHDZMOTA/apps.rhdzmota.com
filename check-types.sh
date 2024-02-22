mkdir -p .mypy_cache
mypy apps_bundle --ignore-missing-imports --install-types --non-interactive --explicit-package-bases
mypy apps --exclude '{{cookiecutter.project_slug}}' --ignore-missing-imports --install-types --non-interactive --explicit-package-bases

