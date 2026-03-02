"""
iframe_page.py - Page Object for Iframe Interaction
====================================================
Case Study: Handle frames and iframes efficiently.
Hands-on Activity: Switch to an iframe, interact with content inside,
and switch back to the main page.

Target: https://the-internet.herokuapp.com/iframe
"""

from selenium.webdriver.common.by import By
from tests.pages.base_page import BasePage


class IframePage(BasePage):
    """
    Page Object for the WYSIWYG Editor (iFrame) page.
    Demonstrates switching into an iframe, interacting with its content,
    and switching back to the default content.
    """

    URL = "https://the-internet.herokuapp.com/iframe"

    # --- LOCATORS ---

    # CSS Selector — the iframe element itself
    EDITOR_IFRAME = (By.CSS_SELECTOR, "#mce_0_ifr")

    # XPath inside the iframe — the editable body
    EDITOR_BODY = (By.XPATH, "//body[@id='tinymce']")

    # XPath with contains() — paragraph content inside the iframe
    EDITOR_PARAGRAPH = (By.XPATH, "//body[@id='tinymce']//p")

    # CSS Selector — page heading (outside iframe, on main page)
    PAGE_HEADING = (By.CSS_SELECTOR, "h3")

    def open_page(self):
        """Navigate to the iframe editor page."""
        self.open(self.URL)

    def switch_to_editor_frame(self):
        """
        Switch into the TinyMCE editor iframe.
        Demonstrates: Frame/Iframe switching as required by the case study.
        """
        self.switch_to_frame(self.EDITOR_IFRAME)

    def clear_editor_content(self):
        """
        Clear the existing content in the iframe editor using JavaScript.
        Must be called AFTER switching into the iframe.
        Note: TinyMCE uses a contenteditable div, not a standard input field,
        so we use JavaScript to clear the innerHTML instead of .clear().
        """
        editor = self.find_visible_element(self.EDITOR_BODY)
        self.execute_js("arguments[0].innerHTML = '';", editor)

    def type_in_editor(self, text):
        """
        Type text into the iframe editor using JavaScript.
        Must be called AFTER switching into the iframe.
        Note: TinyMCE contenteditable requires JS to set content reliably.
        """
        editor = self.find_visible_element(self.EDITOR_BODY)
        self.execute_js("arguments[0].innerText = arguments[1];", editor, text)

    def get_editor_text(self):
        """
        Get the current text from the iframe editor body via JavaScript.
        Must be called AFTER switching into the iframe.
        """
        editor = self.find_visible_element(self.EDITOR_BODY)
        return self.execute_js("return arguments[0].textContent;", editor)

    def switch_back_to_main(self):
        """
        Switch back to the main page from the iframe.
        Demonstrates: Returning to default content after iframe interaction.
        """
        self.switch_to_main_content()

    def get_page_heading(self):
        """
        Get the page heading text (outside the iframe).
        Must be called AFTER switching back to main content.
        """
        return self.get_text(self.PAGE_HEADING)
