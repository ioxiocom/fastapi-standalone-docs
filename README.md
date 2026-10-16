# FastAPI Standalone Docs

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/ioxiocom/fastapi-standalone-docs/publish.yaml)](https://github.com/ioxiocom/fastapi-standalone-docs/actions/workflows/publish.yaml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PyPI](https://img.shields.io/pypi/v/fastapi-standalone-docs)](https://pypi.org/project/fastapi-standalone-docs/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastapi-standalone-docs)](https://pypi.org/project/fastapi-standalone-docs/)
[![License: MIT](https://img.shields.io/pypi/l/fastapi-standalone-docs)](https://opensource.org/license/mit/)

Host FastAPI Swagger UI and ReDoc without any third party CDNs. Handy if you want to be
able to use the docs offline or want to avoid loading content from 3rd party CDNs due to
privacy reasons.

This library was heavily inspired by
[fastapi-offline-swagger-ui](https://github.com/ahmetoner/fastapi-offline-swagger-ui),
but we wanted a way to take it into use with less boilerplate code and also have it
hosted on PyPI.

## Installation

The package is available on PyPI:

```bash
pip install fastapi-standalone-docs
```

## Usage

Import `StandaloneDocs` and pass in the FastAPI application to it:

```python
from fastapi import FastAPI
from fastapi_standalone_docs import StandaloneDocs

app = FastAPI()
StandaloneDocs(app=app)
```

The static files will by default be served from subpaths of the `docs_url` and
`redoc_url` as you've specified in your FastAPI app. The library doesn't make any
assumption on any particular path being reserved for the library. And if you disable
either of the two UIs, the corresponding files won't either be served unnecessarily.

This example would move the Swagger UI and the static files needed for it to the path
`/swagger` and disable the ReDoc interface and the static files needed by it:

```python
from fastapi import FastAPI
from fastapi_standalone_docs import StandaloneDocs

app = FastAPI(docs_url="/swagger", redoc_url=None)
StandaloneDocs(app=app)
```

By default, the library will use the FastAPI favicons, and they're served from
`{docs_url}/fastapi/favicon.png` and `{redoc_url}/fastapi/favicon.png`. You can use your
own favicons like this, which will also disable the FastAPI icons:

```python
from fastapi import FastAPI
from fastapi_standalone_docs import StandaloneDocs

app = FastAPI()
StandaloneDocs(
    app=app,
    redoc_favicon_url="/favicon.png",
    swagger_favicon_url="/favicon.png",
)
```

To make the docs truly stand alone the Google Fonts are by default disabled (they are
used in the ReDoc interface). If you want to enable them just set
`with_google_fonts=True`, like this:

```python
from fastapi import FastAPI
from fastapi_standalone_docs import StandaloneDocs

app = FastAPI()
StandaloneDocs(
    app=app,
    with_google_fonts=True,
)
```

### Disclaimer

**Note!** If you create multiple FastAPI apps in the same runtime (quite unlikely
use-case), for example by mounting one app inside another, using StandaloneDocs on one
of them will affect the other ones as well, as the library patches two of the shared
functions (`get_swagger_ui_html` and `get_redoc_html`). Thus, the library should not be
used in such a setup unless all the apps will use StandaloneDocs with the same settings
and the same `docs_url`, `redoc_url` and `openapi_url` on the FastAPI app itself. If any
of those differ, only the app that called StandaloneDocs last will serve its docs
correctly.

## Development

PRs are welcome!

This project is using [uv](https://docs.astral.sh/uv/), so please ensure you've
[installed it](https://docs.astral.sh/uv/getting-started/installation/). To set up the
project run:

```bash
uv sync
uv run pre-commit install
```

Running tests locally (pre-commit hooks, mypy, pytest and a dependency audit):

```bash
uv run invoke test
```

Updating the static files from the CDNs:

```bash
uv run update-fastapi-standalone-docs
```

If you want to test using it locally in some other project, in that project run this
(make sure to adjust the path to the local repo):

```bash
uv add --editable ../fastapi-standalone-docs
```

## License

The code of this library itself is released under the [MIT license](./LICENSE). Please
however note that this library also contains parts of
[ReDoc](./src/fastapi_standalone_docs/static/redoc/), which is licensed under the
[MIT license](./src/fastapi_standalone_docs/static/redoc/redoc.standalone.js.LICENSE.txt),
[Swagger UI](./src/fastapi_standalone_docs/static/swagger/), which is licensed under the
[Apache 2.0 License](./src/fastapi_standalone_docs/static/swagger/LICENSE), as well as
parts of [FastAPI](./src/fastapi_standalone_docs/static/fastapi) (the favicon), which is
licensed under the [MIT license](./src/fastapi_standalone_docs/static/fastapi/LICENSE).
