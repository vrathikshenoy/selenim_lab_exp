"""
alerts_page.py - Page Object for JavaScript Alerts
====================================================
Case Study: Handle pop-ups and alerts.
Hands-on Activity: Manage pop-ups and alerts efficiently using
advanced Selenium techniques.

Target: https://the-internet.herokuapp.com/javascript_alerts
"""

from selenium.webdriver.common.by import By
from tests.pages.base_page import BasePage


class AlertsPage(BasePage):
    """
    Page Object for the JavaScript Alerts page.
    Demonstrates handling JS Alert, JS Confirm, and JS Prompt pop-ups.
    """

    URL = "https://the-internet.herokuapp.com/javascript_alerts"

    # --- LOCATORS using XPath and CSS ---

    # XPath with text() — trigger buttons
    JS_ALERT_BUTTON = (By.XPATH, "//button[text()='Click for JS Alert']")
    JS_CONFIRM_BUTTON = (By.XPATH, "//button[text()='Click for JS Confirm']")
    JS_PROMPT_BUTTON = (By.XPATH, "//button[text()='Click for JS Prompt']")

    # CSS Selector — result text display
    RESULT_TEXT = (By.CSS_SELECTOR, "#result")

    def open_page(self):
        """Navigate to the JavaScript Alerts page."""
        self.open(self.URL)

    def trigger_js_alert(self):
        """
        Click button to trigger a JS Alert pop-up.
        Demonstrates: Triggering JavaScript alerts.
        """
        self.click(self.JS_ALERT_BUTTON)

    def trigger_js_confirm(self):
        """
        Click button to trigger a JS Confirm dialog.
        Demonstrates: Triggering JavaScript confirm dialogs.
        """
        self.click(self.JS_CONFIRM_BUTTON)

    def trigger_js_prompt(self):
        """
        Click button to trigger a JS Prompt dialog.
        Demonstrates: Triggering JavaScript prompt dialogs.
        """
        self.click(self.JS_PROMPT_BUTTON)

    def accept_alert_and_get_text(self):
        """
        Accept the current JS alert and return its text.
        Demonstrates: Handling pop-ups — accept action.
        """
        return self.accept_browser_alert()

    def dismiss_alert_and_get_text(self):
        """
        Dismiss the current JS confirm/alert and return its text.
        Demonstrates: Handling pop-ups — dismiss action.
        """
        return self.dismiss_browser_alert()

    def send_text_to_prompt(self, text):
        """
        Type text into a JS Prompt and accept it.
        Demonstrates: Interacting with prompt-type pop-ups.
        """
        from tests.utils.element_utils import send_text_to_alert
        send_text_to_alert(self.driver, text)

    def get_result_text(self):
        """
        Get the result message displayed after interacting with an alert.
        """
        return self.get_text(self.RESULT_TEXT)
