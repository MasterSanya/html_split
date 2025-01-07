from bs4 import BeautifulSoup
from typing import List


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
    fragments = []  # List to store the resulting fragments
    current_fragment = ""  # Current fragment being built

    # Tags that are allowed to be split (block-level elements)
    splittable_tags = {"p", "div", "span", "ul", "ol", "strong", "b", "i"}

    def add_to_fragment(content: str):
        """
        Adds content to the current fragment, or starts a new fragment if the length limit is exceeded.

        Parameters:
        - content (str): The content to add to the fragment.
        """
        nonlocal current_fragment
        if len(content) > max_len:
            raise ValueError(f"Cannot split tag exceeding {
                             max_len} characters: {content}")

        # Start a new fragment if adding the content would exceed the max length
        if len(current_fragment) + len(content) > max_len:
            fragments.append(current_fragment)
            current_fragment = content
        else:
            current_fragment += content

    def process_element(element):
        """
        Recursively processes an HTML element and adds its content to the fragments.

        Parameters:
        - element: A BeautifulSoup element or string.
        """
        nonlocal current_fragment
        if isinstance(element, str):
            add_to_fragment(element)
        else:
            # If the element is splittable and its length exceeds max_len, split its children
            if element.name in splittable_tags:
                for child in element.children:
                    process_element(child)
            else:
                # Non-splittable tags must remain intact
                tag_as_string = str(element)
                if len(tag_as_string) > max_len:
                    raise ValueError(f"Cannot split tag exceeding {
                                     max_len} characters: {tag_as_string[:50]}...")
                # Add the whole tag if it fits
                if len(current_fragment) + len(tag_as_string) > max_len:
                    fragments.append(current_fragment)
                    current_fragment = tag_as_string
                else:
                    current_fragment += tag_as_string

    # Process the entire document
    for child in soup.children:
        process_element(child)

    # Add the final fragment if there's remaining content
    if current_fragment:
        fragments.append(current_fragment)

    return fragments
