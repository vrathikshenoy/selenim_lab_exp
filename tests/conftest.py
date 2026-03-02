"""
conftest.py - Base Framework Setup 
=======================================================
Case Study Requirement: Establish automation best practices with proper
setup/teardown, implicit waits for basic element loading, and integrated
reporting with screenshot capture on failure (Extent Reports equivalent).
"""

import pytest
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# ---------------------------------------------------------------------------
# DRIVER FIXTURE — Setup & Teardown
# ---------------------------------------------------------------------------
@pytest.fixture(scope="function")
def driver(request):
    """
    Pytest fixture to initialize and tear down the Chrome WebDriver.
    - Maximizes the browser window.
    - Sets an IMPLICIT WAIT (10s) to handle basic dynamic element loading.
    - Sets a PAGE LOAD TIMEOUT (30s) for asynchronous page loads.
    - Tears down the driver after each test function using 'yield'.
    """
    chrome_options = Options()
    # Flatpak Chrome — actual binary inside the Flatpak installation
    chrome_options.binary_location = "/home/vrathik/.local/share/flatpak/app/com.google.Chrome/x86_64/stable/e96304f188a8713c46686759c984b35e45b8637571ffb11bfc59c7bd8863f42f/files/extra/chrome"
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Uncomment for headless CI execution:
    # chrome_options.add_argument("--headless=new")

    # Selenium 4 auto-downloads the correct ChromeDriver version
    browser = webdriver.Chrome(options=chrome_options)

    # --- IMPLICIT WAIT: handles basic element loading globally ---
    browser.implicitly_wait(10)

    # --- PAGE LOAD TIMEOUT: handles asynchronous page loads ---
    browser.set_page_load_timeout(30)

    yield browser  # Test runs here

    # --- TEARDOWN ---
    browser.quit()


# ---------------------------------------------------------------------------
# REPORTING HOOKS — Screenshot on Failure (Extent Reports equivalent)
# ---------------------------------------------------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    pytest-html hook to automatically capture a screenshot when a test fails
    and embed it into the HTML report. This fulfills the Extent Reports
    requirement for rich test result analysis with visual evidence.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            # Create screenshots directory if it doesn't exist
            screenshot_dir = os.path.join(os.path.dirname(__file__), "..", "reports", "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)

            # Generate a unique screenshot filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"{item.name}_{timestamp}.png"
            screenshot_path = os.path.join(screenshot_dir, screenshot_name)

            driver.save_screenshot(screenshot_path)

            # Attach screenshot to the pytest-html report
            if hasattr(report, "extras"):
                extra = getattr(report, "extras", [])
            else:
                extra = []

            try:
                from pytest_html import extras as html_extras
                extra.append(html_extras.image(screenshot_path))
                report.extras = extra
            except ImportError:
                pass  # pytest-html not installed, skip embedding
