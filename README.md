# FastAPI Standalone Docs

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/ioxiocom/fastapi-standalone-docs/publish.yaml)](https://github.com/ioxiocom/fastapi-standalone-docs/actions/workflows/publish.yaml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI](https://img.shields.io/pypi/v/fastapi-standalone-docs)](https://pypi.org/project/fastapi-standalone-docs/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastapi-standalone-docs)](https://pypi.org/project/fastapi-standalone-docs/)
[![License: BSD 3-Clause](https://img.shields.io/pypi/l/fastapi-standalone-docs)](https://opensource.org/license/mit/)

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
use-case), using StandaloneDocs on one of them will affect the other ones as well, as
the library patches two of the shared functions (`get_swagger_ui_html` and
`get_redoc_html`). Thus the library should not be used in a such setup unless all the
apps will use StandaloneDocs with the same settings.

## Development

PRs are welcome!

This project is using [Poetry](https://python-poetry.org/) and
[pre-commit](https://pre-commit.com/), so please ensure you've installed both. To set up
the project with them run:

```bash
pre-commit install
poetry install
```

Running tests locally:

```bash
poetry run invoke test
```

Updating the static files from the CDNs:

```bash
poetry run update-fastapi-standalone-docs
```

If you want to test using it locally in some other project, in that project run this
(make sure to adjust the path to the local repo):

```bash
poetry add ../fastapi-standalone-docs --editable
```

## License

The code of this library itself is released under the [MIT license](./LICENSE). Please
however note that this library also contains parts of
[ReDoc](./fastapi_standalone_docs/static/redoc/), which is licensed under the
[MIT license](./fastapi_standalone_docs/static/redoc/redoc.standalone.js.LICENSE.txt),
[Swagger UI](./fastapi_standalone_docs/static/swagger/), which is licensed under the
[Apache 2.0 License](./fastapi_standalone_docs/static/swagger/LICENSE), as well as parts
of [FastAPI](./fastapi_standalone_docs/static/fastapi) (the favicon), which is licensed
under the [MIT license](./fastapi_standalone_docs/static/fastapi/LICENSE).
