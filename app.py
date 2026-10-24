"""Compatibility entry point for the categorized backend application."""

import sys

from backend import app as _backend_app

sys.modules[__name__] = _backend_app

if __name__ == "__main__":
    _backend_app.create_app().run(host="127.0.0.1", port=5000, debug=False)
