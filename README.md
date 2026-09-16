# arrorcore

Playwright Python end to end framework

A lightweight Playwright + Python test automation framework (POC), using the Page Object Model and generating both a static HTML report and a richer Allure report.

## Structure

```
arrorcore/
├── pages/                  # Page Objects
│   └── example_page.py
├── tests/                  # Test cases
│   └── test_example_domain.py
├── reports/                # Generated reports (report.html, allure-results/, allure-report/)
├── conftest.py
├── pytest.ini
└── requirements.txt
```

## Setup

```bash
pip install -r requirements.txt
playwright install
```

Allure also needs its commandline tool to build the HTML report from results (not required just to run tests):

```bash
npm install -g allure-commandline
```

## Run tests

```bash
pytest
```

This runs headless by default and generates:
- a self-contained static report at `reports/report.html`
- raw Allure result files in `reports/allure-results/`

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

## Reports

**Static HTML report** — open `reports/report.html` directly in any browser.

**Allure report** — build the interactive HTML report from the results, then serve it (Allure reports fetch data via AJAX, so opening `index.html` directly with `file://` won't load the results — always use `allure open` or `allure serve`):

```bash
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

Or in one step, generate and serve without a separate build folder:

```bash
allure serve reports/allure-results
```

The Allure report includes feature/story grouping, per-step timing, severity levels, and screenshots attached to key steps.
