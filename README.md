# Web Page Analysis Script

This Python script allows you to analyze a web page to extract visible routes (GET requests) and form details. It also provides options for performing GET requests to the found routes and checking for potential vulnerabilities. The script supports command-line arguments to control its behavior.

## Prerequisites

Before using the script, ensure you have the necessary libraries installed:

- `requests` for making HTTP requests.
- `beautifulsoup4` for parsing HTML content.
- `colorama` for adding colored output to the terminal.
- `PyPDF2` for handling PDF content.
- Python 3.x

You can install these libraries using `pip`:

```bash
pip install requests beautifulsoup4 colorama PyPDF2
```

## Usage

To run the script, use the following command:


```bash
python web_page_analysis.py [URL] [OPTIONS]
```
   
  [URL] is the URL of the web page to analyze.

### Options

```
    --get-requests: Perform GET requests to the found routes.
    --search: Search for all forms and inputs on the page.
    --injections: Check for vulnerabilities using LaTeX injections.
```

### Examples

As an example, I've taken up the challenge we created with PauvreTimo, available here : [here](https://github.com/MarchandRobin/CLOG/tree/main/Third)

To search for forms and inputs on a web page:

```bash
python web_page_analysis.py https://example.com --search
```

![Search](https://github.com/MarchandRobin/LateXI/blob/main/img/search.png?raw=true)

To perform GET requests to found routes:

```bash
python web_page_analysis.py https://example.com --get-requests
```
![REQ](https://github.com/MarchandRobin/LateXI/blob/main/img/get-r.png?raw=true)

To check for vulnerabilities using LaTeX injections:

```bash
python web_page_analysis.py https://example.com --injections
```
![REQ+I](https://github.com/MarchandRobin/LateXI/blob/main/img/get-r+I.png?raw=true)


### Features

- Extracts visible routes (GET requests) and form details from a web page.
- Performs GET requests to the found routes.
- Checks for potential vulnerabilities using LaTeX injections.
- Provides colored output for better visualization.
