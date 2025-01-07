# HTML Split Tool

This repository provides a Python tool for splitting large HTML messages into smaller fragments while preserving the integrity of the HTML structure.

## Main Script

The main script for this tool is:

```bash
python split_msg.py <html_file_path> --max-len <max_length>
```


- `<html_file_path>` – path to the source HTML file.
- `--max-len` – maximum length for each message fragment.

## Repository Structure

- `src/`: Contains the core splitting logic (`msg_split.py`).
- `tests/`: Unit tests for validating the splitting behavior.
  - `html/source.html`: A sample HTML file for testing purposes.
  - `test_msg_split.py`: Test cases for the `split_html_message` function.
- `split_msg.py`: The main executable script for running the tool.
- `requirements.txt`: List of Python dependencies required to run the project.
- `README.md`: This file with instructions for usage and repository details.


## How to Run Tests

Run the unit tests using:

```bash
python -m unittest discover -s tests -t .
```

Ensure you have all dependencies installed before running the tests.

## Requirements

- Python 3.x
- BeautifulSoup4

## Contributing

Contributions are welcome! Please submit a pull request or open an issue if you have suggestions or find bugs.
