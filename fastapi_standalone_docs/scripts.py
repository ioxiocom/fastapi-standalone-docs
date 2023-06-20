from pathlib import Path
from typing import List
from urllib.request import urlretrieve

import fastapi_standalone_docs

FASTAPI_FILES = [
    "https://fastapi.tiangolo.com/img/favicon.png",
    "https://raw.githubusercontent.com/tiangolo/fastapi/master/LICENSE",
]

SWAGGER_FILES = [
    "https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/LICENSE",
    "https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css",
    "https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui-bundle.js",
]

REDOC_FILES = [
    "https://cdn.jsdelivr.net/npm/redoc@2.0.0/bundles/redoc.standalone.js.LICENSE.txt",
    "https://cdn.jsdelivr.net/npm/redoc@2.0.0/bundles/redoc.standalone.js",
    "https://cdn.redoc.ly/redoc/logo-mini.svg",
]


def update_docs():
    static_path = Path(fastapi_standalone_docs.__path__[0]) / "static"
    fastapi_path = static_path / "fastapi"
    swagger_path = static_path / "swagger"
    redoc_path = static_path / "redoc"

    fastapi_path.mkdir(parents=True, exist_ok=True)
    swagger_path.mkdir(parents=True, exist_ok=True)
    redoc_path.mkdir(parents=True, exist_ok=True)

    download_files(fastapi_path, FASTAPI_FILES)
    download_files(swagger_path, SWAGGER_FILES)
    download_files(redoc_path, REDOC_FILES)

    patch_redoc_logo(target=static_path / "redoc")


def download_files(destination: Path, urls: List[str]) -> None:
    for url in urls:
        filename = url.split("/")[-1]
        urlretrieve(url, destination / filename)


def patch_redoc_logo(target: Path):
    file = target / "redoc.standalone.js"
    content = file.read_text(encoding="utf-8")
    content = content.replace(
        '"https://cdn.redoc.ly/redoc/logo-mini.svg"',
        'window.location.pathname+"/logo-mini.svg"',
    )
    file.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    update_docs()
