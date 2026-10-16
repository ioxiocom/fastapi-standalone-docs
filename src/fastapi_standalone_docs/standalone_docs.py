from pathlib import Path

from fastapi import FastAPI, applications
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.staticfiles import StaticFiles

import fastapi_standalone_docs


class StandaloneDocs:
    def __init__(
        self,
        app: FastAPI,
        with_google_fonts: bool = False,
        swagger_favicon_url: str | None = None,
        redoc_favicon_url: str | None = None,
    ):
        self.app = app
        self.with_google_fonts = with_google_fonts
        self.static_path = Path(fastapi_standalone_docs.__path__[0]) / "static"

        self.patch_swagger(swagger_favicon_url)
        self.patch_redoc(redoc_favicon_url)

    def get_root_path(self, openapi_url: str) -> str:
        """
        Extract from the openapi_url the root_path the app is served from in this
        request, such as "/myapp1", or "" when it has none.

        An app mounted in another app does not have access to its own prefix: mount()
        doesn't touch app.root_path, the prefix arrives with each request in the ASGI
        scope, and a proxy may even set a different one per request. The functions we
        are patching don't get access to the full request, only the arguments FastAPI
        passes them.

        However FastAPI passes these functions an openapi_url parameter, which it builds
        from the root_path of the request and the openapi_url of the app, making the
        latter a suffix of it. Removing that suffix gives the root_path of the request.

            "/myapp1/openapi.json" - "/openapi.json" -> "/myapp1"
            "/openapi.json"        - "/openapi.json" -> ""

        An openapi_url that doesn't end in the app's own falls back to "", which is
        correct for an app served from the root and the best guess otherwise.
        """
        suffix = self.app.openapi_url or ""
        if suffix and openapi_url.endswith(suffix):
            return openapi_url.removesuffix(suffix)
        return ""

    def patch_swagger(self, swagger_favicon_url: str | None):
        if self.app.openapi_url and self.app.docs_url:
            docs_url = self.app.docs_url

            if not swagger_favicon_url:
                self.app.mount(
                    docs_url + "/fastapi/",
                    StaticFiles(directory=self.static_path / "fastapi"),
                )

            self.app.mount(
                docs_url + "/",
                StaticFiles(directory=self.static_path / "swagger"),
            )

            def patched_get_swagger_ui_html(*args, **kwargs):
                root_path = self.get_root_path(kwargs.get("openapi_url", ""))
                return get_swagger_ui_html(
                    *args,
                    **kwargs,
                    swagger_favicon_url=(
                        swagger_favicon_url
                        or f"{root_path}{docs_url}/fastapi/favicon.png"
                    ),
                    swagger_css_url=f"{root_path}{docs_url}/swagger-ui.css",
                    swagger_js_url=f"{root_path}{docs_url}/swagger-ui-bundle.js",
                )

            applications.get_swagger_ui_html = patched_get_swagger_ui_html

    def patch_redoc(self, redoc_favicon_url: str | None):
        if self.app.openapi_url and self.app.redoc_url:
            redoc_url = self.app.redoc_url

            if not redoc_favicon_url:
                self.app.mount(
                    redoc_url + "/fastapi/",
                    StaticFiles(directory=self.static_path / "fastapi"),
                )

            self.app.mount(
                redoc_url + "/",
                StaticFiles(directory=self.static_path / "redoc"),
            )

            def patched_get_redoc_html(*args, **kwargs):
                root_path = self.get_root_path(kwargs.get("openapi_url", ""))
                return get_redoc_html(
                    *args,
                    **kwargs,
                    redoc_js_url=f"{root_path}{redoc_url}/redoc.standalone.js",
                    redoc_favicon_url=(
                        redoc_favicon_url
                        or f"{root_path}{redoc_url}/fastapi/favicon.png"
                    ),
                    with_google_fonts=self.with_google_fonts,
                )

            applications.get_redoc_html = patched_get_redoc_html
