"""
dynamic_controls_page.py - Page Object for Dynamic Controls
============================================================
Case Study: Handle dynamic web elements and AJAX calls, identify elements
using XPath and CSS selectors.
Hands-on Activity: Automate test scenarios with dynamic web elements that
load asynchronously.

Target: https://the-internet.herokuapp.com/dynamic_controls
"""

from selenium.webdriver.common.by import By
from tests.pages.base_page import BasePage


class DynamicControlsPage(BasePage):
    """
    Page Object for the Dynamic Controls page on the-internet.herokuapp.com.
    Demonstrates handling dynamic web elements and AJAX calls.
    """

    URL = "https://the-internet.herokuapp.com/dynamic_controls"

    # --- LOCATORS using XPath and CSS Selectors ---

    # XPath with contains() — dynamic element identification
    CHECKBOX = (By.XPATH, "//input[@type='checkbox']")

    # CSS Selector — button interaction
    REMOVE_ADD_BUTTON = (By.CSS_SELECTOR, "#checkbox-example button")

    # XPath with text() — identifying by visible text
    MESSAGE = (By.XPATH, "//p[@id='message']")

    # CSS Selector — input field in enable/disable section
    TEXT_INPUT = (By.CSS_SELECTOR, "#input-example input[type='text']")

    # XPath with descendant axis — button in enable section
    ENABLE_DISABLE_BUTTON = (By.XPATH, "//form[@id='input-example']//descendant::button")

    # CSS selector with attribute matching
    LOADING_INDICATOR = (By.CSS_SELECTOR, "#loading")

    def open_page(self):
        """Navigate to the Dynamic Controls page."""
        self.open(self.URL)

    def remove_checkbox(self):
        """
        Click the Remove button to trigger an AJAX call that removes the checkbox.
        Demonstrates: AJAX call handling + explicit wait for element removal.
        """
        self.click(self.REMOVE_ADD_BUTTON)

    def add_checkbox(self):
        """
        Click the Add button to trigger an AJAX call that adds a checkbox back.
        Demonstrates: AJAX call handling + explicit wait for element to appear.
        """
        self.click(self.REMOVE_ADD_BUTTON)

    def get_message_text(self):
        """
        Get the confirmation message that appears after the AJAX call completes.
        Uses explicit wait since the message loads dynamically.
        """
        return self.get_text(self.MESSAGE)

    def enable_text_input(self):
        """
        Click Enable to trigger an AJAX call that enables the text input.
        Demonstrates: Dynamic element state change via AJAX.
        """
        self.click(self.ENABLE_DISABLE_BUTTON)

    def type_in_input(self, text):
        """
        Type text into the input field after it has been enabled.
        Must be called after enable_text_input() and waiting for AJAX.
        """
        self.type_text(self.TEXT_INPUT, text)

    def is_input_enabled(self):
        """Check if the text input field is enabled."""
        element = self.find_visible_element(self.TEXT_INPUT)
        return element.is_enabled()
