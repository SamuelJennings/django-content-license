# History

## Unreleased

### Changed (BREAKING)

* **Support matrix narrowed to actively-supported releases**: Python **≥3.11** (was ≥3.10)
  and Django **5.2 LTS + 6.0** (dropped 3.2/4.1/4.2/5.0). Aligns with the django-mvp family
  standard. Consumers on older Python/Django should pin an earlier release.

### Internal / tooling

* CI now delegates to the shared `django-mvp/shared` reusable workflows (`tests.yml`, `build.yml`).
* Dev toolchain consolidated into the `fairdm-dev-tools` bundle (pytest, ruff, black, mypy, deptry).
* Modernised pre-commit config; test runner is now pytest (pytest-django).
* Fixed a broken `django_db_setup` override in `tests/conftest.py` that prevented the suite
  from running under pytest.
* Corrected the PyPI license classifier (MIT, was mislabelled BSD).

## 0.1.0 (2023-01-22)

* First release on PyPI.
