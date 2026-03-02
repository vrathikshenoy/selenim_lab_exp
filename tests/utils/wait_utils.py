"""
wait_utils.py - Explicit Wait Utilities (Step 3 of agent.md)
============================================================
Case Study Requirement: Implement implicit AND explicit waits to handle
asynchronous page loads and AJAX calls. Do NOT use time.sleep().
Hands-on Activity: Implement waits to synchronize test execution with
dynamic web elements that load asynchronously via AJAX.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


DEFAULT_TIMEOUT = 15  # seconds


def wait_for_element_visible(driver, locator, timeout=DEFAULT_TIMEOUT):
    """
    EXPLICIT WAIT: Waits until an element is visible on the page.
    Used for elements that appear after AJAX calls or dynamic page loads.

    Args:
        driver: WebDriver instance
        locator: Tuple of (By strategy, locator string), e.g. (By.XPATH, "//div[@id='content']")
        timeout: Maximum wait time in seconds

    Returns:
        WebElement once it becomes visible

    Raises:
        TimeoutException if element is not visible within timeout
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return element
    except TimeoutException:
        raise TimeoutException(
            f"Element with locator {locator} was not visible after {timeout} seconds. "
            "This may indicate an AJAX call has not completed or the element is dynamically hidden."
        )


def wait_for_element_clickable(driver, locator, timeout=DEFAULT_TIMEOUT):
    """
    EXPLICIT WAIT: Waits until an element is clickable.
    Essential for buttons/links that are rendered but not yet interactive
    (e.g., after an AJAX response updates the DOM).

    Args:
        driver: WebDriver instance
        locator: Tuple of (By strategy, locator string)
        timeout: Maximum wait time in seconds

    Returns:
        WebElement once it becomes clickable
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        return element
    except TimeoutException:
        raise TimeoutException(
            f"Element with locator {locator} was not clickable after {timeout} seconds."
        )


def wait_for_alert_present(driver, timeout=DEFAULT_TIMEOUT):
    """
    EXPLICIT WAIT: Waits for a JavaScript alert/pop-up to appear.
    Required by the Hands-on Activity to manage pop-ups and alerts.

    Args:
        driver: WebDriver instance
        timeout: Maximum wait time in seconds

    Returns:
        Alert object once it appears
    """
    try:
        alert = WebDriverWait(driver, timeout).until(
            EC.alert_is_present()
        )
        return alert
    except TimeoutException:
        raise TimeoutException(
            f"No alert was present after {timeout} seconds."
        )


def wait_for_element_present(driver, locator, timeout=DEFAULT_TIMEOUT):
    """
    EXPLICIT WAIT: Waits until an element is present in the DOM
    (it may or may not be visible). Useful for elements loaded via AJAX
    that are added to the DOM but not yet displayed.

    Args:
        driver: WebDriver instance
        locator: Tuple of (By strategy, locator string)
        timeout: Maximum wait time in seconds

    Returns:
        WebElement once it is present in the DOM
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return element
    except TimeoutException:
        raise TimeoutException(
            f"Element with locator {locator} was not present in DOM after {timeout} seconds."
        )


def wait_for_frame_available(driver, frame_locator, timeout=DEFAULT_TIMEOUT):
    """
    EXPLICIT WAIT: Waits until a frame/iframe is available and switches to it.
    Required by the Hands-on Activity to manage frames and iframes.

    Args:
        driver: WebDriver instance
        frame_locator: Frame name, id, index, or WebElement
        timeout: Maximum wait time in seconds

    Returns:
        True if switched to frame successfully
    """
    try:
        WebDriverWait(driver, timeout).until(
            EC.frame_to_be_available_and_switch_to_it(frame_locator)
        )
        return True
    except TimeoutException:
        raise TimeoutException(
            f"Frame {frame_locator} was not available after {timeout} seconds."
        )


def wait_for_text_in_element(driver, locator, text, timeout=DEFAULT_TIMEOUT):
    """
    EXPLICIT WAIT: Waits until specific text is present in an element.
    Useful for verifying AJAX responses that update text content dynamically.

    Args:
        driver: WebDriver instance
        locator: Tuple of (By strategy, locator string)
        text: The text to wait for
        timeout: Maximum wait time in seconds

    Returns:
        True if the text is found in the element
    """
    try:
        return WebDriverWait(driver, timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )
    except TimeoutException:
        raise TimeoutException(
            f"Text '{text}' was not found in element {locator} after {timeout} seconds."
        )
