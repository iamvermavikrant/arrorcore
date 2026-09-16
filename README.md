# arrorcore

Playwright Python end to end framework

A lightweight Playwright + Python test automation framework (POC), using the Page Object Model and generating a static HTML report.

## Structure

```
arrorcore/
├── pages/                  # Page Objects
│   └── example_page.py
├── tests/                  # Test cases
│   └── test_example_domain.py
├── reports/                # Generated static HTML report (report.html)
├── conftest.py
├── pytest.ini
└── requirements.txt
```

## Setup

```bash
pip install -r requirements.txt
playwright install
```

## Run tests

```bash
pytest
```

This runs headless by default and generates a self-contained static report at `reports/report.html`.

Useful flags:

```bash
pytest --headed              # run with a visible browser
pytest --browser firefox     # run against Firefox (or webkit)
```

## Test cases (example.com POC)

| ID | Description |
|----|-------------|
| TC001 | Assert the page displays the text "Example Domain" |
| TC002 | Click the "Learn more" link and assert the main navigation links on the destination (IANA) page |

## Report

After a run, open `reports/report.html` in any browser to view the static test report.
