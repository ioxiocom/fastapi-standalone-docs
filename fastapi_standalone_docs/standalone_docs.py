from pathlib import Path
from typing import Optional

from fastapi import FastAPI, applications
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.staticfiles import StaticFiles

import fastapi_standalone_docs


class StandaloneDocs:
    def __init__(
        self,
        app: FastAPI,
        with_google_fonts: bool = False,
        swagger_favicon_url: Optional[str] = None,
        redoc_favicon_url: Optional[str] = None,
    ):
        self.app = app
        self.with_google_fonts = with_google_fonts
        self.static_path = Path(fastapi_standalone_docs.__path__[0]) / "static"

        self.patch_swagger(swagger_favicon_url)
        self.patch_redoc(redoc_favicon_url)

    def patch_swagger(self, swagger_favicon_url: Optional[str]):
        if self.app.openapi_url and self.app.docs_url:
            if not swagger_favicon_url:
                swagger_favicon_url = self.app.docs_url + "/fastapi/favicon.png"
                self.app.mount(
                    self.app.docs_url + "/fastapi/",
                    StaticFiles(directory=self.static_path / "fastapi"),
                )

            self.app.mount(
                self.app.docs_url + "/",
                StaticFiles(directory=self.static_path / "swagger"),
            )

            def patched_get_swagger_ui_html(*args, **kwargs):
                return get_swagger_ui_html(
                    *args,
                    **kwargs,
                    swagger_favicon_url=swagger_favicon_url,
                    swagger_css_url=self.app.docs_url + "/swagger-ui.css",
                    swagger_js_url=self.app.docs_url + "/swagger-ui-bundle.js",
                )

            applications.get_swagger_ui_html = patched_get_swagger_ui_html

    def patch_redoc(self, redoc_favicon_url: Optional[str]):
        if self.app.openapi_url and self.app.redoc_url:
            if not redoc_favicon_url:
                redoc_favicon_url = self.app.redoc_url + "/fastapi/favicon.png"
                self.app.mount(
                    self.app.redoc_url + "/fastapi/",
                    StaticFiles(directory=self.static_path / "fastapi"),
                )

            self.app.mount(
                self.app.redoc_url + "/",
                StaticFiles(directory=self.static_path / "redoc"),
            )

            def patched_get_redoc_html(*args, **kwargs):
                return get_redoc_html(
                    *args,
                    **kwargs,
                    redoc_js_url=self.app.redoc_url + "/redoc.standalone.js",
                    redoc_favicon_url=redoc_favicon_url,
                    with_google_fonts=self.with_google_fonts,
                )

            applications.get_redoc_html = patched_get_redoc_html
