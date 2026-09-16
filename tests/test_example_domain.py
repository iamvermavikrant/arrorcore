import allure

from pages.example_page import ExamplePage, IanaPage


@allure.feature("Example Domain")
@allure.story("Homepage content")
@allure.title("TC001 - Assert the 'Example Domain' text is displayed")
@allure.severity(allure.severity_level.CRITICAL)
def test_tc001_assert_example_domain_text(page):
    example_page = ExamplePage(page)

    with allure.step("Navigate to example.com"):
        example_page.goto()

    with allure.step("Assert heading text is 'Example Domain'"):
        heading_text = example_page.get_heading_text()
        allure.attach(page.screenshot(), name="homepage", attachment_type=allure.attachment_type.PNG)
        assert heading_text == "Example Domain"


@allure.feature("Example Domain")
@allure.story("Learn more navigation")
@allure.title("TC002 - Click 'Learn more' and assert main nav links on IANA page")
@allure.severity(allure.severity_level.NORMAL)
def test_tc002_click_learn_more_and_assert_main_links(page):
    example_page = ExamplePage(page)

    with allure.step("Navigate to example.com"):
        example_page.goto()

    with allure.step("Click the 'Learn more' link"):
        example_page.click_learn_more()
        page.wait_for_load_state("networkidle")

    with allure.step("Assert only the main nav links are present on the IANA page"):
        iana_page = IanaPage(page)
        iana_page.main_nav_links.first.wait_for()
        link_texts = iana_page.get_main_link_texts()
        allure.attach(page.screenshot(), name="iana-page", attachment_type=allure.attachment_type.PNG)

        expected_main_links = ["Domains", "Protocols", "Numbers", "About"]
        assert link_texts == expected_main_links
