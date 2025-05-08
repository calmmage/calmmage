import mistune
from mistune.renderers.html import HTMLRenderer
import re


def is_html(text: str) -> bool:
    """Check if text contains HTML tags."""
    html_pattern = re.compile(r"<[^>]+>")
    return bool(html_pattern.search(text))


def markdown_to_html(text: str) -> str:
    """
    Convert Markdown text to HTML.

    Args:
        text: The markdown text to convert to HTML

    Returns:
        The HTML converted text
    """
    # Skip if already HTML
    if is_html(text):
        return text

    # Initialize mistune markdown parser
    markdown = mistune.create_markdown(renderer=HTMLRenderer())
    result = markdown(text)
    return str(result)  # Ensure we return a string


def old_markdown_to_html(text: str) -> str:
    import markdown

    return markdown.markdown(text)
