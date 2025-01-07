from bs4 import BeautifulSoup
from typing import List

# Set of block-level tags that can be closed and reopened
BLOCK_TAGS = {"p", "b", "strong", "i", "ul", "ol", "div", "span"}

# Set of inline tags that must not be split
INLINE_TAGS = {"a"}


def split_html_message(html: str, max_len: int) -> List[str]:
    """
    Splits an HTML message into smaller fragments while preserving the HTML structure.

    Parameters:
    - html (str): The HTML content as a string.
    - max_len (int): The maximum allowed length for each fragment.

    Returns:
    - List[str]: A list of HTML fragments.
    """
    soup = BeautifulSoup(html, "html.parser")
    fragments = []
    current_fragment = ""
    open_tags_stack = []

    def add_to_fragment(content: str):
        nonlocal current_fragment
        if len(content) > max_len:
            raise ValueError(f"Cannot split tag exceeding {
                             max_len} characters: {content[:50]}...")

        if len(current_fragment) + len(content) > max_len:
            fragments.append(
                current_fragment + ''.join(f'</{tag}>' for tag in reversed(open_tags_stack)))
            current_fragment = ''.join(
                f'<{tag}>' for tag in open_tags_stack) + content
        else:
            current_fragment += content

    def split_text(text: str):
        nonlocal current_fragment
        while text:
            available_space = max_len - len(current_fragment)
            if len(text) <= available_space:
                add_to_fragment(text)
                break
            else:
                add_to_fragment(text[:available_space])
                fragments.append(
                    current_fragment + ''.join(f'</{tag}>' for tag in reversed(open_tags_stack)))
                current_fragment = ''.join(
                    f'<{tag}>' for tag in open_tags_stack)
                text = text[available_space:]

    def process_element(element):
        nonlocal current_fragment

        if isinstance(element, str):
            split_text(element)
        else:
            tag_name = element.name

            if tag_name in INLINE_TAGS:
                tag_as_string = str(element)
                if len(tag_as_string) > max_len:
                    raise ValueError(f"Cannot split tag exceeding {
                                     max_len} characters: {tag_as_string[:50]}...")
                add_to_fragment(tag_as_string)
                return

            # Handling block-level tags with correct closing and reopening
            if tag_name in BLOCK_TAGS:
                open_tags_stack.append(tag_name)
                open_tag = f"<{tag_name}>"
                close_tag = f"</{tag_name}>"
                add_to_fragment(open_tag)

                for child in element.children:
                    process_element(child)
                    if len(current_fragment) > max_len:
                        fragments.append(current_fragment + close_tag)
                        current_fragment = open_tag

                open_tags_stack.pop()
                add_to_fragment(close_tag)

            else:
                tag_as_string = str(element)
                add_to_fragment(tag_as_string)

    for child in soup.children:
        process_element(child)

    if current_fragment:
        fragments.append(current_fragment)

    return fragments
