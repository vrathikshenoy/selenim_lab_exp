"""
element_utils.py - Advanced Element Interaction Utilities (Step 4 of agent.md)
=============================================================================
Case Study Requirement: Handle dynamic web elements, AJAX calls, identify
elements using XPath and CSS selectors.
Hands-on Activity: Manage pop-ups, alerts, frames, and iframes.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoAlertPresentException, NoSuchFrameException
from tests.utils.wait_utils import (
    wait_for_element_visible,
    wait_for_element_clickable,
    wait_for_alert_present,
    wait_for_frame_available,
)


# ---------------------------------------------------------------------------
# ALERT / POP-UP HANDLERS
# Hands-on Activity: Manage pop-ups and alerts
# ---------------------------------------------------------------------------
def accept_alert(driver, timeout=10):
    """
    Wait for a JavaScript alert to appear, then accept (click OK).
    Handles pop-ups as required by the case study.
    """
    alert = wait_for_alert_present(driver, timeout)
    alert_text = alert.text
    alert.accept()
    return alert_text


def dismiss_alert(driver, timeout=10):
    """
    Wait for a JavaScript alert/confirm dialog to appear, then dismiss (click Cancel).
    """
    alert = wait_for_alert_present(driver, timeout)
    alert_text = alert.text
    alert.dismiss()
    return alert_text


def get_alert_text(driver, timeout=10):
    """
    Wait for a JavaScript alert and retrieve its text without acting on it.
    """
    alert = wait_for_alert_present(driver, timeout)
    return alert.text


def send_text_to_alert(driver, text, timeout=10):
    """
    Wait for a JavaScript prompt, type text into it, and accept.
    Handles prompt-type pop-ups.
    """
    alert = wait_for_alert_present(driver, timeout)
    alert.send_keys(text)
    alert.accept()


# ---------------------------------------------------------------------------
# FRAME / IFRAME HANDLERS
# Hands-on Activity: Manage frames and iframes efficiently
# ---------------------------------------------------------------------------
def switch_to_frame_by_name_or_id(driver, name_or_id, timeout=10):
    """
    Switch into a frame/iframe using its name or id attribute.
    Uses explicit wait to ensure the frame is available before switching.
    """
    wait_for_frame_available(driver, name_or_id, timeout)


def switch_to_frame_by_index(driver, index, timeout=10):
    """
    Switch into a frame/iframe using its index (0-based).
    """
    wait_for_frame_available(driver, index, timeout)


def switch_to_frame_by_element(driver, locator, timeout=10):
    """
    Switch into a frame/iframe using a WebElement locator.
    First waits for the frame element to be visible, then switches to it.
    """
    frame_element = wait_for_element_visible(driver, locator, timeout)
    driver.switch_to.frame(frame_element)


def switch_to_default_content(driver):
    """
    Switch back to the main page content from any frame/iframe.
    """
    driver.switch_to.default_content()


def switch_to_parent_frame(driver):
    """
    Switch to the parent frame (useful for nested frames).
    """
    driver.switch_to.parent_frame()


# ---------------------------------------------------------------------------
# DYNAMIC ELEMENT INTERACTION UTILITIES
# Case Study: Handle dynamic web elements using XPath and CSS selectors
# ---------------------------------------------------------------------------
def click_dynamic_element(driver, locator, timeout=10):
    """
    Wait for a dynamically loaded element to become clickable, then click it.
    Addresses AJAX-loaded buttons/links that appear after async operations.
    """
    element = wait_for_element_clickable(driver, locator, timeout)
    element.click()
    return element


def type_into_dynamic_element(driver, locator, text, timeout=10):
    """
    Wait for a dynamically loaded input field to be visible, clear it, and type text.
    Handles input fields that are rendered after AJAX calls.
    """
    element = wait_for_element_visible(driver, locator, timeout)
    element.clear()
    element.send_keys(text)
    return element


def get_dynamic_element_text(driver, locator, timeout=10):
    """
    Wait for a dynamically loaded element to be visible and retrieve its text.
    Useful for reading content loaded via AJAX responses.
    """
    element = wait_for_element_visible(driver, locator, timeout)
    return element.text


def hover_over_element(driver, locator, timeout=10):
    """
    Wait for an element to be visible and hover over it using ActionChains.
    Useful for elements with hover-triggered dynamic content (tooltips, dropdowns).
    """
    element = wait_for_element_visible(driver, locator, timeout)
    ActionChains(driver).move_to_element(element).perform()
    return element


def scroll_to_element(driver, locator, timeout=10):
    """
    Wait for an element and scroll it into view using JavaScript.
    Handles elements that are off-screen in long/dynamic pages.
    """
    element = wait_for_element_visible(driver, locator, timeout)
    driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", element)
    return element


# ---------------------------------------------------------------------------
# XPATH & CSS SELECTOR STRATEGY EXAMPLES
# Case Study: Identify web elements using XPath and CSS selectors
# ---------------------------------------------------------------------------
"""
ADVANCED XPATH STRATEGIES for dynamic web elements:

1. contains():     (By.XPATH, "//div[contains(@class, 'dynamic-')]")
2. starts-with():  (By.XPATH, "//input[starts-with(@id, 'field_')]")
3. text():         (By.XPATH, "//button[text()='Submit']")
4. contains text:  (By.XPATH, "//span[contains(text(), 'Loading')]")
5. ancestor axis:  (By.XPATH, "//input[@id='email']/ancestor::form")
6. descendant:     (By.XPATH, "//div[@class='container']//descendant::a")
7. following-sibling: (By.XPATH, "//label[text()='Name']/following-sibling::input")
8. parent axis:    (By.XPATH, "//span[@class='error']/parent::div")

ADVANCED CSS SELECTOR STRATEGIES:

1. Attribute contains:    (By.CSS_SELECTOR, "div[class*='dynamic']")
2. Attribute starts-with: (By.CSS_SELECTOR, "input[id^='field_']")
3. Attribute ends-with:   (By.CSS_SELECTOR, "input[id$='_name']")
4. nth-child:             (By.CSS_SELECTOR, "ul.menu > li:nth-child(3)")
5. Direct child:          (By.CSS_SELECTOR, "div.parent > span.child")
6. Adjacent sibling:      (By.CSS_SELECTOR, "h2 + p")
7. Multiple attributes:   (By.CSS_SELECTOR, "input[type='text'][name='search']")
"""
