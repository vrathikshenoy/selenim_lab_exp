"""
base_page.py - Base Page Object (POM Pattern)
=============================================
Case Study Requirement: Establish automation best practices with
Page Object Model to ensure maintainability and reusability.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.utils.wait_utils import (
    wait_for_element_visible,
    wait_for_element_clickable,
    wait_for_element_present,
)
from tests.utils.element_utils import (
    switch_to_frame_by_element,
    switch_to_default_content,
    accept_alert,
    dismiss_alert,
)


class BasePage:
    """
    Base Page Object that all page classes inherit from.
    Encapsulates common Selenium operations with built-in waits,
    following Page Object Model best practices.
    """

    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        """Navigate to a URL."""
        self.driver.get(url)

    def get_title(self):
        """Return the current page title."""
        return self.driver.title

    def get_current_url(self):
        """Return the current URL."""
        return self.driver.current_url

    # --- Element interaction with explicit waits ---

    def find_visible_element(self, locator, timeout=10):
        """Wait for and return a visible element."""
        return wait_for_element_visible(self.driver, locator, timeout)

    def find_clickable_element(self, locator, timeout=10):
        """Wait for and return a clickable element."""
        return wait_for_element_clickable(self.driver, locator, timeout)

    def click(self, locator, timeout=10):
        """Wait for element to be clickable, then click."""
        element = wait_for_element_clickable(self.driver, locator, timeout)
        element.click()

    def type_text(self, locator, text, timeout=10):
        """Wait for element to be visible, clear, and type text."""
        element = wait_for_element_visible(self.driver, locator, timeout)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator, timeout=10):
        """Wait for element to be visible and return its text."""
        element = wait_for_element_visible(self.driver, locator, timeout)
        return element.text

    # --- Frame management ---

    def switch_to_frame(self, frame_locator, timeout=10):
        """Switch into a frame/iframe by locator."""
        switch_to_frame_by_element(self.driver, frame_locator, timeout)

    def switch_to_main_content(self):
        """Switch back to the main page from any frame."""
        switch_to_default_content(self.driver)

    # --- Alert management ---

    def accept_browser_alert(self, timeout=10):
        """Accept a JS alert and return its text."""
        return accept_alert(self.driver, timeout)

    def dismiss_browser_alert(self, timeout=10):
        """Dismiss a JS alert and return its text."""
        return dismiss_alert(self.driver, timeout)

    # --- JavaScript execution ---

    def execute_js(self, script, *args):
        """Execute arbitrary JavaScript on the page."""
        return self.driver.execute_script(script, *args)
