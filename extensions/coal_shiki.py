# Copyright (c) 2025-2026 Coal and contributors
#
# SPDX-License-Identifier: MIT
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

"""Shiki-based syntax highlighter for Coal language.

This extension integrates Shiki (a JavaScript-based syntax highlighter) with
Python Markdown by using a subprocess to call a Node.js script. It provides
syntax highlighting for the Coal language using the VSCode TextMate grammar.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import TYPE_CHECKING, Any

# Ensure the project root is on sys.path so the 'extensions' package is importable
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from markdown import Extension, Markdown

if TYPE_CHECKING:
    from markdown import Markdown


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

_SHIKI_SCRIPT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "shiki",
    "highlight.mjs"
)


# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

def highlight_coal_code(code: str, lang: str = "coal") -> str:
    """Highlight Coal code using Shiki via Node.js subprocess.

    Args:
        code: The code to highlight.
        lang: The language identifier (default: "coal").

    Returns:
        Highlighted HTML string, or a fallback if Shiki is unavailable.
    """
    # Check if Node.js and the Shiki script are available
    if not os.path.exists(_SHIKI_SCRIPT):
        return f'<pre><code class="language-coal">{code}</code></pre>'

    try:
        # Run the Shiki highlighter script
        result = subprocess.run(
            ["node", _SHIKI_SCRIPT],
            input=json.dumps({"code": code, "lang": lang}),
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
        output = json.loads(result.stdout.strip())
        return output.get("html", f'<pre><code class="language-coal">{code}</code></pre>')
    except (subprocess.SubprocessError, json.JSONDecodeError, OSError):
        # Fallback to unhighlighted code on error
        return f'<pre><code class="language-coal">{code}</code></pre>'


def coal_fence_format(
    source: str,
    language: str,
    css_class: str,
    options: dict[str, Any],
    md: Markdown,
    **kwargs: Any,
) -> str:
    """Format a Coal fenced code block using Shiki.

    This function is used as the format function for the custom fence in
    pymdownx.superfences. It highlights Coal code using Shiki.

    Args:
        source: The code content.
        language: The language identifier.
        css_class: The CSS class for the code block.
        options: Additional options (unused).
        md: The Markdown instance.
        **kwargs: Additional keyword arguments.

    Returns:
        Highlighted HTML for the code block.
    """
    if language == "coal":
        return highlight_coal_code(source, language)
    # For non-coal languages, return None to let Pygments handle it
    return None


def coal_fence_validator(
    language: str,
    _options: dict[str, Any],
    **kwargs: Any,
) -> bool:
    """Validate whether a language should use the Coal Shiki highlighter.

    Args:
        language: The language identifier.
        _options: Additional options (unused).
        **kwargs: Additional keyword arguments.

    Returns:
        True if the language is "coal", False otherwise.
    """
    return language == "coal"


# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

class CoalShikiExtension(Extension):
    """Markdown extension for Coal syntax highlighting via Shiki.

    This extension registers a custom fence handler for the `coal` language
    with pymdownx.superfences, enabling syntax highlighting using Shiki.
    """

    name = "extensions.coal_shiki"

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the extension."""
        self._enabled: bool = kwargs.pop("enabled", True)
        self._kwargs = kwargs

    def extendMarkdown(self, md: Markdown) -> None:
        """Register the custom fence with superfences.

        This method is called by Python Markdown to register the extension.
        It adds a custom fence configuration to the superfences extension.
        """
        if not self._enabled:
            return

        # Get the superfences configuration, creating it if needed
        if "pymdownx.superfences" not in md.mdx_configs:
            md.mdx_configs["pymdownx.superfences"] = {}

        superfences = md.mdx_configs["pymdownx.superfences"]
        if "custom_fences" not in superfences:
            superfences["custom_fences"] = []

        # Add the Coal custom fence
        superfences["custom_fences"].append({
            "name": "coal",
            "class": "language-coal",
            "format": coal_fence_format,
            "validator": coal_fence_validator,
        })


# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

def makeExtension(**kwargs: Any) -> CoalShikiExtension:
    """Create the Coal Shiki extension."""
    return CoalShikiExtension(**kwargs)