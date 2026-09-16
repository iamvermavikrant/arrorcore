# arrorcore

**Playwright + Python test automation framework — Proof of Concept**

A lightweight, extensible UI test automation framework built with Playwright and pytest, using the Page Object Model (POM). This POC demonstrates the framework end-to-end against a public site ([example.com](https://www.example.com)) with two sample test cases and two report formats — a quick static report and a rich, interactive Allure report.

---

## 1. Tools & technology used

| Tool | Purpose |
|---|---|
| [Python](https://www.python.org/) | Core language |
| [Playwright](https://playwright.dev/python/) | Browser automation (Chromium/Firefox/WebKit) |
| [pytest](https://docs.pytest.org/) | Test runner and assertions |
| [pytest-playwright](https://github.com/microsoft/playwright-pytest) | Playwright fixtures (`page`, `browser`, etc.) for pytest |
| [pytest-html](https://github.com/pytest-dev/pytest-html) | Quick, self-contained static HTML report |
| [Allure](https://allurereport.org/) (`allure-pytest` + Allure commandline) | Rich, interactive test report with steps, timing, severity, and screenshots |

**Design pattern:** Page Object Model (POM) — each web page is represented by a Python class (in `pages/`) that owns its locators and actions. Tests (in `tests/`) only describe *what* to verify, not *how* to find elements — this keeps tests short, readable, and easy to maintain as the app's UI changes.

---

## 2. Project structure

```
arrorcore/
├── pages/
│   └── example_page.py       # Page Objects: ExamplePage, IanaPage
├── tests/
│   └── test_example_domain.py  # TC001, TC002
├── reports/                   # Generated on each run (git-ignored, except a sample snapshot)
│   ├── report.html            # Static pytest-html report
│   ├── allure-results/        # Raw Allure result files (json)
│   └── allure-report/         # Built Allure HTML site
├── conftest.py                # Shared pytest/Playwright fixtures (e.g. viewport size)
├── pytest.ini                 # pytest configuration
└── requirements.txt           # Python dependencies
```

---

## 3. Setup

### Prerequisites
- Python 3.10+
- Node.js (only needed for the Allure commandline tool)
- Java 8+ (Allure commandline runs on the JVM)

### Install

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Playwright's browser binaries
playwright install

# 4. Install the Allure commandline (only needed to view the Allure report)
npm install -g allure-commandline
```

---

## 4. Configuration

**`pytest.ini`** — central pytest configuration:

```ini
[pytest]
addopts = --html=reports/report.html --self-contained-html --alluredir=reports/allure-results --clean-alluredir
testpaths = tests
```

- `--html` / `--self-contained-html` → generates the static report as a single portable HTML file
- `--alluredir` → writes raw Allure result JSON files for each test run
- `--clean-alluredir` → clears old results before each run, so the report always reflects the latest run
- `testpaths = tests` → limits test discovery to the `tests/` directory

**`conftest.py`** — shared fixtures, e.g. a fixed 1280×800 browser viewport for consistent, reproducible runs.

No secrets, environment URLs, or credentials are hardcoded outside the page objects — for a real client project, the target base URL would move to an environment variable or a `--base-url` CLI flag so the same suite can run against dev/staging/prod.

---

## 5. Running the tests

```bash
pytest                          # headless run, all tests
pytest --headed                 # run with a visible browser (good for demos)
pytest --browser firefox        # run against Firefox instead of Chromium
pytest -k tc001                 # run a single test by name
```

Each run regenerates:
- `reports/report.html` — static report
- `reports/allure-results/` — raw data for the Allure report

---

## 6. Test case walkthrough

Both tests target [https://www.example.com](https://www.example.com), a stable public page ideal for a framework demo since its content never changes.

### TC001 — Assert the "Example Domain" text is displayed

| Step | Action |
|---|---|
| 1 | Navigate to `https://www.example.com` |
| 2 | Read the `<h1>` heading text |
| 3 | Assert it equals exactly `"Example Domain"` |

```python
def test_tc001_assert_example_domain_text(page):
    example_page = ExamplePage(page)
    example_page.goto()
    assert example_page.get_heading_text() == "Example Domain"
```

### TC002 — Click "Learn more" and assert the main navigation links

| Step | Action |
|---|---|
| 1 | Navigate to `https://www.example.com` |
| 2 | Click the **Learn more** link |
| 3 | Wait for the destination page (IANA) to finish loading |
| 4 | Read only the **main header navigation** links (not footer/body links) |
| 5 | Assert they are exactly `["Domains", "Protocols", "Numbers", "About"]` |

```python
def test_tc002_click_learn_more_and_assert_main_links(page):
    example_page = ExamplePage(page)
    example_page.goto()
    example_page.click_learn_more()
    page.wait_for_load_state("networkidle")

    iana_page = IanaPage(page)
    link_texts = iana_page.get_main_link_texts()
    assert link_texts == ["Domains", "Protocols", "Numbers", "About"]
```

This case is intentionally scoped to the header navigation (`header .navigation a`) rather than every link on the page — it's a good example of writing a precise, non-brittle locator instead of asserting against the entire page.

Both tests are also annotated with `@allure.feature`, `@allure.story`, `@allure.severity`, and `allure.step(...)` blocks, and attach a screenshot at the key verification point — this is what powers the detailed Allure report below.

---

## 7. Reports

### Static HTML report (fast, no extra tooling)

Just open the file — no server needed:

```bash
open reports/report.html        # macOS
start reports/report.html       # Windows
```

### Allure report (recommended for the demo — much more informative)

Allure reports load their data via AJAX, so `index.html` must be served, not opened directly with `file://`. The simplest way:

```bash
allure serve reports/allure-results
```

This builds the report and opens it in your browser in one step. Alternatively, to build a persisted copy:

```bash
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

**What the Allure report shows that the static one doesn't:**
- Pass/fail dashboard with trend and pass percentage
- Tests grouped by **Feature → Story** (Behaviors tab) instead of a flat list
- Per-test **severity** (critical, normal, etc.)
- A **step-by-step timeline** for each test, with duration per step
- **Screenshots** attached at key assertion points, viewable inline

A sample snapshot is included at `reports/allure_snapshot.png` for quick reference without running anything.

---

## 8. Suggested demo flow for the client

1. Show the repo structure and explain the Page Object Model briefly (`pages/` vs `tests/`).
2. Run `pytest --headed` live so they see the browser drive through TC001 and TC002.
3. Run `allure serve reports/allure-results` and walk through:
   - Overview dashboard (100% pass rate)
   - Suites → drill into TC002 → show the step timeline and attached screenshot
4. Mention this same structure scales to a real app: more page objects, more test files, and the base URL/credentials would move to config/environment variables per target environment (dev/staging/prod).
