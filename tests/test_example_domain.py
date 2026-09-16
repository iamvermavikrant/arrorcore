from pages.example_page import ExamplePage, IanaPage


def test_tc001_assert_example_domain_text(page):
    """TC001 - Assert the heading text 'Example Domain' is displayed."""
    example_page = ExamplePage(page)
    example_page.goto()

    assert example_page.get_heading_text() == "Example Domain"


def test_tc002_click_learn_more_and_assert_main_links(page):
    """TC002 - Click 'Learn more' and assert only the main nav links on the new page."""
    example_page = ExamplePage(page)
    example_page.goto()
    example_page.click_learn_more()
    page.wait_for_load_state("networkidle")

    iana_page = IanaPage(page)
    iana_page.main_nav_links.first.wait_for()
    link_texts = iana_page.get_main_link_texts()

    expected_main_links = ["Domains", "Protocols", "Numbers", "About"]
    assert link_texts == expected_main_links
