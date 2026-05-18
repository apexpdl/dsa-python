"""Markdown rendering used inside Jinja templates.

We use the `markdown` library with fenced code blocks and tables. Code
blocks get class names so Prism (loaded from a CDN in the base template)
highlights them on the client side.
"""
from __future__ import annotations

import markdown as _markdown
from markupsafe import Markup

_MD = _markdown.Markdown(
    extensions=[
        "fenced_code",
        "tables",
        "sane_lists",
        "toc",
    ],
    output_format="html5",
)


def md(text: str | None) -> Markup:
    """Render markdown to safe HTML for use inside templates.

    Content authors are trusted (it's our own teaching material), so we
    do not strip HTML. The output is wrapped in `Markup` so Jinja does
    not escape it.
    """
    if not text:
        return Markup("")
    _MD.reset()
    return Markup(_MD.convert(text))
