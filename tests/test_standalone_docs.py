from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_standalone_docs import StandaloneDocs


def test_swagger_default():
    app = FastAPI()
    StandaloneDocs(app)
    client = TestClient(app)

    response = client.get("/docs")
    assert response.status_code == 200

    expected_strings = (
        '<link type="text/css" rel="stylesheet" href="/docs/swagger-ui.css">',
        '<script src="/docs/swagger-ui-bundle.js"></script>',
        '<link rel="shortcut icon" href="/docs/fastapi/favicon.png">',
    )
    for expected_string in expected_strings:
        assert expected_string in response.text

    # No external links/hrefs etc. expected
    assert "https://" not in response.text
    assert "http://" not in response.text

    # Check we can load the files
    expected_resources = (
        "/docs/swagger-ui.css",
        "/docs/swagger-ui-bundle.js",
        "/docs/fastapi/favicon.png",
    )
    for res in expected_resources:
        response = client.get(res)
        assert response.status_code == 200


def test_swagger_custom_url():
    app = FastAPI(docs_url="/my-swagger-url")
    StandaloneDocs(app)
    client = TestClient(app)

    response = client.get("/my-swagger-url")
    assert response.status_code == 200
    expected_strings = (
        '<link type="text/css" rel="stylesheet" href="/my-swagger-url/swagger-ui.css">',
        '<link rel="shortcut icon" href="/my-swagger-url/fastapi/favicon.png">',
        '<script src="/my-swagger-url/swagger-ui-bundle.js"></script>',
    )
    for expected_string in expected_strings:
        assert expected_string in response.text

    # Check we can load the files
    expected_resources = (
        "/my-swagger-url/swagger-ui.css",
        "/my-swagger-url/fastapi/favicon.png",
        "/my-swagger-url/swagger-ui-bundle.js",
    )
    for res in expected_resources:
        response = client.get(res)
        assert response.status_code == 200


def test_swagger_custom_favicon():
    app = FastAPI()
    StandaloneDocs(app, swagger_favicon_url="https://example.com/favicon.ico")
    client = TestClient(app)

    response = client.get("/docs")
    assert response.status_code == 200

    favicon_string = '<link rel="shortcut icon" href="https://example.com/favicon.ico">'
    assert favicon_string in response.text

    # Default favicon path should not be mounted
    response = client.get("/docs/fastapi/favicon.png")
    assert response.status_code == 404


def test_swagger_disabled():
    app = FastAPI(docs_url=None)
    StandaloneDocs(app)
    client = TestClient(app)

    paths = (
        "/docs",
        "/docs/swagger-ui.css",
        "/docs/fastapi/favicon.png",
        "/docs/swagger-ui-bundle.js",
    )
    for path in paths:
        response = client.get(path)
        assert response.status_code == 404


def test_redoc_default():
    app = FastAPI()
    StandaloneDocs(app)
    client = TestClient(app)

    response = client.get("/redoc")
    assert response.status_code == 200

    expected_strings = (
        '<link rel="shortcut icon" href="/redoc/fastapi/favicon.png">',
        '<script src="/redoc/redoc.standalone.js"> </script>',
    )
    for expected_string in expected_strings:
        assert expected_string in response.text

    # No external links/hrefs etc. expected
    assert "https://" not in response.text
    assert "http://" not in response.text

    # Check we can load the files
    expected_resources = (
        "/redoc/logo-mini.svg",
        "/redoc/redoc.standalone.js",
        "/redoc/fastapi/favicon.png",
    )
    for res in expected_resources:
        response = client.get(res)
        assert response.status_code == 200


def test_redoc_custom_url():
    app = FastAPI(redoc_url="/my-redoc-url")
    StandaloneDocs(app)
    client = TestClient(app)

    response = client.get("/my-redoc-url")
    assert response.status_code == 200
    expected_strings = (
        '<link rel="shortcut icon" href="/my-redoc-url/fastapi/favicon.png">',
        '<script src="/my-redoc-url/redoc.standalone.js"> </script>',
    )
    for expected_string in expected_strings:
        assert expected_string in response.text

    # Check we can load the files
    expected_resources = (
        "/my-redoc-url/logo-mini.svg",
        "/my-redoc-url/redoc.standalone.js",
        "/my-redoc-url/fastapi/favicon.png",
    )
    for res in expected_resources:
        response = client.get(res)
        assert response.status_code == 200


def test_redoc_custom_favicon():
    app = FastAPI()
    StandaloneDocs(app, redoc_favicon_url="https://example.com/favicon.ico")
    client = TestClient(app)

    response = client.get("/redoc")
    assert response.status_code == 200

    favicon_string = '<link rel="shortcut icon" href="https://example.com/favicon.ico">'
    assert favicon_string in response.text

    # Default favicon path should not be mounted
    response = client.get("/redoc/fastapi/favicon.png")
    assert response.status_code == 404


def test_redoc_disabled():
    app = FastAPI(redoc_url=None)
    StandaloneDocs(app)
    client = TestClient(app)

    paths = (
        "/redoc",
        "/redoc/logo-mini.svg",
        "/redoc/redoc.standalone.js",
        "/redoc/fastapi/favicon.png",
    )
    for path in paths:
        response = client.get(path)
        assert response.status_code == 404


def test_redoc_with_google_fonts():
    app = FastAPI()
    StandaloneDocs(app, with_google_fonts=True)
    client = TestClient(app)

    response = client.get("/redoc")
    assert response.status_code == 200
    assert "https://fonts.googleapis.com" in response.text


def test_openapi_disabled():
    app = FastAPI(openapi_url=None)
    StandaloneDocs(app)
    client = TestClient(app)

    paths = (
        "/docs",
        "/docs/swagger-ui.css",
        "/docs/fastapi/favicon.png",
        "/docs/swagger-ui-bundle.js",
        "/redoc",
        "/redoc/logo-mini.svg",
        "/redoc/redoc.standalone.js",
        "/redoc/fastapi/favicon.png",
    )
    for path in paths:
        response = client.get(path)
        assert response.status_code == 404


def test_swagger_mounted_app():
    app = FastAPI()
    StandaloneDocs(app)
    main_app = FastAPI()
    main_app.mount("/myapp1", app)
    client = TestClient(main_app)

    response = client.get("/myapp1/docs")
    assert response.status_code == 200

    expected_strings = (
        '<link type="text/css" rel="stylesheet" href="/myapp1/docs/swagger-ui.css">',
        '<script src="/myapp1/docs/swagger-ui-bundle.js"></script>',
        '<link rel="shortcut icon" href="/myapp1/docs/fastapi/favicon.png">',
    )
    for expected_string in expected_strings:
        assert expected_string in response.text

    # No external links/hrefs etc. expected
    assert "https://" not in response.text
    assert "http://" not in response.text

    # Check we can load the files
    expected_resources = (
        "/myapp1/docs/swagger-ui.css",
        "/myapp1/docs/swagger-ui-bundle.js",
        "/myapp1/docs/fastapi/favicon.png",
    )
    for res in expected_resources:
        response = client.get(res)
        assert response.status_code == 200


def test_redoc_mounted_app():
    app = FastAPI()
    StandaloneDocs(app)
    main_app = FastAPI()
    main_app.mount("/myapp1", app)
    client = TestClient(main_app)

    response = client.get("/myapp1/redoc")
    assert response.status_code == 200

    expected_strings = (
        '<script src="/myapp1/redoc/redoc.standalone.js"> </script>',
        '<link rel="shortcut icon" href="/myapp1/redoc/fastapi/favicon.png">',
    )
    for expected_string in expected_strings:
        assert expected_string in response.text

    # No external links/hrefs etc. expected
    assert "https://" not in response.text
    assert "http://" not in response.text

    # Check we can load the files
    expected_resources = (
        "/myapp1/redoc/logo-mini.svg",
        "/myapp1/redoc/redoc.standalone.js",
        "/myapp1/redoc/fastapi/favicon.png",
    )
    for res in expected_resources:
        response = client.get(res)
        assert response.status_code == 200


def test_root_path():
    app = FastAPI(root_path="/api/v1")
    StandaloneDocs(app)
    client = TestClient(app)

    response = client.get("/docs")
    assert response.status_code == 200
    expected_strings = (
        '<link type="text/css" rel="stylesheet" href="/api/v1/docs/swagger-ui.css">',
        '<script src="/api/v1/docs/swagger-ui-bundle.js"></script>',
        '<link rel="shortcut icon" href="/api/v1/docs/fastapi/favicon.png">',
    )
    for expected_string in expected_strings:
        assert expected_string in response.text

    response = client.get("/redoc")
    assert response.status_code == 200
    expected_strings = (
        '<script src="/api/v1/redoc/redoc.standalone.js"> </script>',
        '<link rel="shortcut icon" href="/api/v1/redoc/fastapi/favicon.png">',
    )
    for expected_string in expected_strings:
        assert expected_string in response.text


def test_mounted_app_custom_favicon():
    # A favicon URL given by the caller is used as-is; it may point anywhere, so the
    # caller is the one who knows whether it needs a prefix.
    app = FastAPI()
    StandaloneDocs(
        app,
        swagger_favicon_url="/myapp1/favicon.png",
        redoc_favicon_url="/myapp1/favicon.png",
    )
    main_app = FastAPI()
    main_app.mount("/myapp1", app)
    client = TestClient(main_app)

    for docs_url in ("/myapp1/docs", "/myapp1/redoc"):
        response = client.get(docs_url)
        assert response.status_code == 200
        assert '<link rel="shortcut icon" href="/myapp1/favicon.png">' in response.text


def test_standalone_docs_on_both_apps():
    # Both apps patch the same shared functions (see the disclaimer in the README), but
    # with equal settings each one still serves its own docs, under its own path.
    app = FastAPI()
    StandaloneDocs(app)
    main_app = FastAPI()
    StandaloneDocs(main_app)
    main_app.mount("/myapp1", app)
    client = TestClient(main_app)

    expected = {
        "/docs": (
            '<link type="text/css" rel="stylesheet" href="/docs/swagger-ui.css">',
            '<script src="/docs/swagger-ui-bundle.js"></script>',
            '<link rel="shortcut icon" href="/docs/fastapi/favicon.png">',
        ),
        "/myapp1/docs": (
            '<link type="text/css" rel="stylesheet"'
            ' href="/myapp1/docs/swagger-ui.css">',
            '<script src="/myapp1/docs/swagger-ui-bundle.js"></script>',
            '<link rel="shortcut icon" href="/myapp1/docs/fastapi/favicon.png">',
        ),
        "/redoc": (
            '<script src="/redoc/redoc.standalone.js"> </script>',
            '<link rel="shortcut icon" href="/redoc/fastapi/favicon.png">',
        ),
        "/myapp1/redoc": (
            '<script src="/myapp1/redoc/redoc.standalone.js"> </script>',
            '<link rel="shortcut icon" href="/myapp1/redoc/fastapi/favicon.png">',
        ),
    }

    for docs_url, expected_strings in expected.items():
        response = client.get(docs_url)
        assert response.status_code == 200
        for expected_string in expected_strings:
            assert expected_string in response.text

        # No external links/hrefs etc. expected
        assert "https://" not in response.text
        assert "http://" not in response.text

    # Check we can load the files of both apps
    expected_resources = (
        "/docs/swagger-ui.css",
        "/docs/swagger-ui-bundle.js",
        "/docs/fastapi/favicon.png",
        "/redoc/redoc.standalone.js",
        "/redoc/fastapi/favicon.png",
        "/myapp1/docs/swagger-ui.css",
        "/myapp1/docs/swagger-ui-bundle.js",
        "/myapp1/docs/fastapi/favicon.png",
        "/myapp1/redoc/redoc.standalone.js",
        "/myapp1/redoc/fastapi/favicon.png",
    )
    for res in expected_resources:
        response = client.get(res)
        assert response.status_code == 200
