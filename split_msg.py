import click
from src.msg_split import split_html_message


@click.command()
@click.argument('file', type=click.File('r', encoding='utf-8'))
@click.option('--max-len', default=4096, help='Maximum length for each message fragment.')
def main(file, max_len):
    """
    Splits an HTML file into smaller fragments of the specified length.

    Args:
        file (file): The source HTML file to be split.
        max_len (int): Maximum length of each fragment.
    """
    # Read the content of the provided file
    source = file.read()
    try:
        # Attempt to split the HTML content into fragments
        fragments = list(split_html_message(source, max_len))
        # Print each fragment with its index and length
        for i, fragment in enumerate(fragments, start=1):
            print(f"\nFragment #{i}: {len(fragment)} characters")
            print(fragment)
            print("-" * 40)
    except ValueError as e:
        # Print an error message if splitting fails due to constraints
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
