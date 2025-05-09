import mistune
from mistune.renderers.html import HTMLRenderer
import re


def is_html(text: str) -> bool:
    """Check if text contains HTML tags, ignoring tags inside code blocks."""
    # First split by code blocks
    parts = []
    in_code_block = False
    current_part = []

    for line in text.split("\n"):
        if line.startswith("```"):
            if in_code_block:
                # End of code block
                parts.append("".join(current_part))
                current_part = []
            in_code_block = not in_code_block
            continue

        if not in_code_block:
            current_part.append(line + "\n")

    # Add any remaining text
    if current_part:
        parts.append("".join(current_part))

    # Check for HTML tags only in non-code parts
    html_pattern = re.compile(r"<[^>]+>")
    return any(bool(html_pattern.search(part)) for part in parts)


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
