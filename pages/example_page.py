class ExamplePage:
    URL = "https://www.example.com"

    def __init__(self, page):
        self.page = page
        self.heading = page.locator("h1")
        self.learn_more_link = page.get_by_role("link", name="Learn more")

    def goto(self):
        self.page.goto(self.URL)

    def get_heading_text(self):
        return self.heading.inner_text()

    def click_learn_more(self):
        self.learn_more_link.click()


class IanaPage:
    """Page object for the IANA page opened via 'Learn more' on example.com."""

    def __init__(self, page):
        self.page = page
        self.main_nav_links = page.locator("header .navigation a")

    def get_main_link_texts(self):
        return self.main_nav_links.all_inner_texts()
