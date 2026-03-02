"""
test_advanced_interactions.py - Test Execution Logic 
========================================================================
This test file fulfils ALL requirements from the Case Study and Hands-on Activity:

1. Case Study Requirements:
   - Handle dynamic web elements and AJAX calls ✓
   - Identify web elements using XPath and CSS selectors ✓
   - Implement implicit and explicit waits for asynchronous page loads ✓
   - Integrate with CI tools like Jenkins (see Jenkinsfile) ✓

2. Hands-on Activity Requirements:
   - Identify and handle dynamic web elements ✓
   - Implement waits to synchronize test execution ✓
   - Manage pop-ups and frames ✓
   - Analyze test results using reporting frameworks (pytest-html) ✓

Target Application: https://the-internet.herokuapp.com
"""

import pytest
from selenium.webdriver.common.by import By
from tests.pages.dynamic_controls_page import DynamicControlsPage
from tests.pages.iframe_page import IframePage
from tests.pages.alerts_page import AlertsPage
from tests.utils.wait_utils import wait_for_element_visible, wait_for_text_in_element


# ===========================================================================
# TEST 1: Dynamic Web Elements & AJAX Calls
# Case Study: "Handle dynamic web elements and AJAX calls"
# ===========================================================================
class TestDynamicElements:
    """Tests demonstrating handling of dynamic web elements and AJAX calls."""

    @pytest.mark.dynamic_elements
    @pytest.mark.ajax
    def test_remove_and_add_checkbox_via_ajax(self, driver):
        """
        Test Scenario: Remove a checkbox via an AJAX call and verify
        the dynamic message that appears after the async operation completes.

        Demonstrates:
        - AJAX call handling (Remove button triggers async request)
        - Explicit wait for dynamically loaded message
        - XPath locators with text() and contains()
        """
        page = DynamicControlsPage(driver)
        page.open_page()

        # Verify the checkbox exists before removal
        checkbox = page.find_visible_element(page.CHECKBOX)
        assert checkbox.is_displayed(), "Checkbox should be visible initially"

        # Click Remove — triggers an AJAX call
        page.remove_checkbox()

        # EXPLICIT WAIT for the AJAX response message
        message = page.get_message_text()
        assert "gone" in message.lower(), \
            f"Expected 'gone' in message after AJAX removal, got: '{message}'"

    @pytest.mark.dynamic_elements
    @pytest.mark.ajax
    def test_enable_input_field_via_ajax(self, driver):
        """
        Test Scenario: Enable a disabled text input via an AJAX call,
        then type into it after it becomes interactive.

        Demonstrates:
        - Dynamic element state change (disabled → enabled) via AJAX
        - Explicit wait for element state change
        - CSS Selectors for element identification
        """
        page = DynamicControlsPage(driver)
        page.open_page()

        # Verify input is initially disabled
        assert not page.is_input_enabled(), "Input should be disabled initially"

        # Click Enable — triggers an AJAX call to enable the input
        page.enable_text_input()

        # EXPLICIT WAIT for the confirmation message
        message = page.get_message_text()
        assert "enabled" in message.lower(), \
            f"Expected 'enabled' in message, got: '{message}'"

        # Now the input should be enabled — type into it
        page.type_in_input("Selenium automation test text")


# ===========================================================================
# TEST 2: Frames & Iframes
# Case Study: "Handle frames and iframes efficiently"
# Hands-on Activity: "Manage pop-ups and frames"
# ===========================================================================
class TestFramesAndIframes:
    """Tests demonstrating iframe switching and content interaction."""

    @pytest.mark.frames
    def test_interact_with_iframe_editor(self, driver):
        """
        Test Scenario: Switch into a TinyMCE iframe editor, clear content,
        type new text, verify it, then switch back to the main page.

        Demonstrates:
        - Switching INTO an iframe (driver.switch_to.frame)
        - Interacting with elements INSIDE the iframe
        - Switching BACK to default content (driver.switch_to.default_content)
        - XPath selectors inside iframe context
        """
        page = IframePage(driver)
        page.open_page()

        # Step 1: Switch INTO the iframe
        page.switch_to_editor_frame()

        # Step 2: Clear existing content and type new text inside the iframe
        page.clear_editor_content()
        test_text = "Automated text via Selenium inside an iframe!"
        page.type_in_editor(test_text)

        # Step 3: Verify the text was entered inside the iframe
        editor_content = page.get_editor_text()
        assert test_text in editor_content, \
            f"Expected '{test_text}' in iframe editor, got: '{editor_content}'"

        # Step 4: Switch BACK to the main page content
        page.switch_back_to_main()

        # Step 5: Verify we're back on the main page by reading the heading
        heading = page.get_page_heading()
        assert "Editor" in heading or "An iFrame" in heading, \
            f"Expected page heading after switching back, got: '{heading}'"


# ===========================================================================
# TEST 3: Pop-ups & JavaScript Alerts
# Case Study: "Handle pop-ups and alerts"
# Hands-on Activity: "Manage pop-ups"
# ===========================================================================
class TestAlertsAndPopups:
    """Tests demonstrating JavaScript alert, confirm, and prompt handling."""

    @pytest.mark.alerts
    def test_accept_js_alert(self, driver):
        """
        Test Scenario: Trigger a JS Alert and accept it.

        Demonstrates:
        - Triggering a JavaScript alert
        - Explicit wait for alert to be present
        - Accepting the alert
        - Verifying the result text on the page
        """
        page = AlertsPage(driver)
        page.open_page()

        # Trigger the JS Alert
        page.trigger_js_alert()

        # Accept the alert (uses explicit wait for alert to appear)
        alert_text = page.accept_alert_and_get_text()
        assert "alert" in alert_text.lower(), \
            f"Expected 'alert' in alert text, got: '{alert_text}'"

        # Verify result message on the page
        result = page.get_result_text()
        assert "successfully" in result.lower(), \
            f"Expected success message, got: '{result}'"

    @pytest.mark.alerts
    def test_dismiss_js_confirm(self, driver):
        """
        Test Scenario: Trigger a JS Confirm dialog and dismiss it (click Cancel).

        Demonstrates:
        - Triggering a JavaScript confirm dialog
        - Dismissing (cancelling) the dialog
        - Reading result text to verify the dismiss action
        """
        page = AlertsPage(driver)
        page.open_page()

        # Trigger the JS Confirm
        page.trigger_js_confirm()

        # Dismiss the confirm dialog
        alert_text = page.dismiss_alert_and_get_text()
        assert "confirm" in alert_text.lower(), \
            f"Expected 'confirm' in alert text, got: '{alert_text}'"

        # Verify result message — should indicate Cancel was clicked
        result = page.get_result_text()
        assert "Cancel" in result, \
            f"Expected 'Cancel' in result, got: '{result}'"

    @pytest.mark.alerts
    def test_send_text_to_js_prompt(self, driver):
        """
        Test Scenario: Trigger a JS Prompt, enter text, and verify it appears.

        Demonstrates:
        - Triggering a JavaScript prompt dialog
        - Sending text (keystrokes) to the prompt
        - Accepting the prompt
        - Verifying the entered text in the result
        """
        page = AlertsPage(driver)
        page.open_page()

        # Trigger the JS Prompt
        page.trigger_js_prompt()

        # Send text to the prompt and accept
        test_input = "Hello from Selenium!"
        page.send_text_to_prompt(test_input)

        # Verify the entered text appears in the result
        result = page.get_result_text()
        assert test_input in result, \
            f"Expected '{test_input}' in result, got: '{result}'"


# ===========================================================================
# TEST 4: Comprehensive End-to-End Scenario
# Combines ALL techniques: dynamic elements, frames, alerts, waits
# ===========================================================================
class TestComprehensiveScenario:
    """
    End-to-end test combining all advanced Selenium techniques
    as required by the Case Study and Hands-on Activity.
    """

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_full_advanced_automation_workflow(self, driver):
        """
        Comprehensive Test Scenario covering all requirements:

        1. Navigate to iframe page → switch into iframe → type content → switch back
        2. Navigate to dynamic controls → trigger AJAX → wait for response
        3. Navigate to alerts page → handle JS Alert → verify result

        This single test demonstrates the full breadth of advanced Selenium
        techniques required by the case study and hands-on activity.
        """
        # ===========================================
        # PART 1: IFRAME INTERACTION
        # ===========================================
        iframe_page = IframePage(driver)
        iframe_page.open_page()

        # Switch into the iframe
        iframe_page.switch_to_editor_frame()

        # Interact with content inside the iframe
        iframe_page.clear_editor_content()
        iframe_page.type_in_editor("End-to-end test: iframe content")
        content = iframe_page.get_editor_text()
        assert "iframe content" in content, "Failed to type in iframe"

        # Switch back to main content
        iframe_page.switch_back_to_main()
        heading = iframe_page.get_page_heading()
        assert heading, "Failed to read main page after iframe switch-back"

        # ===========================================
        # PART 2: DYNAMIC ELEMENTS / AJAX CALLS
        # ===========================================
        dynamic_page = DynamicControlsPage(driver)
        dynamic_page.open_page()

        # Trigger AJAX call to enable the input
        dynamic_page.enable_text_input()

        # Explicit wait for AJAX response
        message = dynamic_page.get_message_text()
        assert "enabled" in message.lower(), "AJAX enable failed"

        # Type into the now-enabled input
        dynamic_page.type_in_input("AJAX-enabled input text")

        # ===========================================
        # PART 3: JAVASCRIPT ALERTS / POP-UPS
        # ===========================================
        alerts_page = AlertsPage(driver)
        alerts_page.open_page()

        # Trigger and accept a JS Alert
        alerts_page.trigger_js_alert()
        alerts_page.accept_alert_and_get_text()

        result = alerts_page.get_result_text()
        assert "successfully" in result.lower(), "Alert handling failed"

        # Trigger and dismiss a JS Confirm
        alerts_page.trigger_js_confirm()
        alerts_page.dismiss_alert_and_get_text()

        result = alerts_page.get_result_text()
        assert "Cancel" in result, "Confirm dismiss failed"
