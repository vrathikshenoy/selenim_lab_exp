# Lab Experiment: Advanced Selenium Test Automation

## Aim

To implement advanced Selenium WebDriver techniques for automating test scenarios on complex web applications, covering dynamic web elements, AJAX calls, pop-ups, alerts, frames, iframes, and integrating with Jenkins CI for seamless test automation and reporting.

---

## Objective

1. Handle dynamic web elements and AJAX calls using Selenium WebDriver
2. Identify web elements using advanced XPath and CSS selectors
3. Implement implicit and explicit waits to handle asynchronous page loads
4. Manage JavaScript pop-ups (alert, confirm, prompt) and frames/iframes
5. Establish automation best practices using Page Object Model (POM)
6. Integrate Selenium tests with Jenkins for continuous integration
7. Analyze test results using reporting frameworks (pytest-html — Python equivalent of Extent Reports)

---

## Tools Required

| Tool               | Version | Purpose                                         |
| ------------------ | ------- | ----------------------------------------------- |
| Python             | 3.8+    | Programming language                            |
| Selenium WebDriver | 4.15+   | Browser automation                              |
| Pytest             | 7.4+    | Test framework                                  |
| pytest-html        | 4.1+    | HTML test reporting (Extent Reports equivalent) |
| webdriver-manager  | 4.0+    | Automatic ChromeDriver management               |
| Google Chrome      | Latest  | Target browser                                  |
| Jenkins            | 2.x     | Continuous Integration server                   |
| Git                | Latest  | Version control                                 |

---

## Theory

### 1. Dynamic Web Elements & AJAX Calls

Dynamic web elements are elements whose properties (visibility, state, content) change at runtime, often loaded asynchronously via AJAX (Asynchronous JavaScript and XML) calls. Selenium must wait for these elements to appear/change before interacting with them, as the DOM is updated dynamically without a full page reload.

### 2. XPath and CSS Selectors

- **XPath** is a query language for selecting nodes in XML/HTML documents. Advanced XPath uses axes like `ancestor`, `descendant`, `following-sibling`, and functions like `contains()`, `text()`, `starts-with()` to locate dynamic elements.
- **CSS Selectors** use attribute matching (`[class*='partial']`, `[id^='prefix']`), pseudo-classes (`:nth-child()`), and combinators (`>`, `+`, `~`) for precise element identification.

### 3. Implicit vs Explicit Waits

- **Implicit Wait**: A global timeout set on the driver. Selenium polls the DOM for a specified duration before throwing a `NoSuchElementException`. Applied to all `find_element` calls.
- **Explicit Wait**: A conditional wait using `WebDriverWait` and `ExpectedConditions` that waits for a specific condition (e.g., element visible, clickable, alert present) before proceeding. More precise than implicit waits.
- **`time.sleep()` should never be used** — it causes unnecessary delays and flaky tests.

### 4. Alerts, Pop-ups, Frames & Iframes

- **JavaScript Alerts**: Handled via `driver.switch_to.alert` — supports `accept()`, `dismiss()`, `send_keys()`, and `.text`.
- **Frames/Iframes**: Content inside frames is isolated from the main DOM. Selenium must switch context using `driver.switch_to.frame()` and return using `driver.switch_to.default_content()`.

### 5. Page Object Model (POM)

A design pattern that creates an object repository for UI elements. Each web page has a corresponding Page class containing locators and interaction methods, promoting code reusability and maintainability.

### 6. Continuous Integration (Jenkins)

Jenkins automates test execution on every code change. A `Jenkinsfile` defines the pipeline stages: checkout → environment setup → test execution → report publishing.

---

## Test Plan

### Scope

Automated testing of the web application at [the-internet.herokuapp.com](https://the-internet.herokuapp.com) covering:

| Area                    | Target Page          | Techniques Used                              |
| ----------------------- | -------------------- | -------------------------------------------- |
| Dynamic Elements & AJAX | `/dynamic_controls`  | Explicit waits, CSS selectors, AJAX handling |
| Frames & Iframes        | `/iframe`            | Frame switching, contenteditable interaction |
| JS Alerts & Pop-ups     | `/javascript_alerts` | Alert accept/dismiss/prompt, XPath locators  |

### Test Environment

- **Browser**: Google Chrome (latest)
- **OS**: Linux
- **Framework**: Python + Pytest + Selenium WebDriver
- **Architecture**: Page Object Model (POM)

---

## Test Cases

| TC#  | Test Case                   | Steps                                                                                                                 | Expected Result                                           | Requirement                            |
| ---- | --------------------------- | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- | -------------------------------------- |
| TC01 | Remove checkbox via AJAX    | 1. Open `/dynamic_controls` 2. Click "Remove" button 3. Wait for AJAX response                                        | Checkbox removed, message "It's gone!" displayed          | Dynamic elements, AJAX, explicit waits |
| TC02 | Enable input via AJAX       | 1. Open `/dynamic_controls` 2. Verify input is disabled 3. Click "Enable" 4. Wait for AJAX 5. Type text               | Input enabled, text entered successfully                  | AJAX state change, waits               |
| TC03 | Interact with iframe editor | 1. Open `/iframe` 2. Switch to TinyMCE iframe 3. Clear content 4. Type new text 5. Verify text 6. Switch back to main | Text entered in iframe, heading visible after switch-back | Frames, iframes                        |
| TC04 | Accept JS Alert             | 1. Open `/javascript_alerts` 2. Click "JS Alert" button 3. Accept alert                                               | Alert accepted, "You successfully clicked an alert" shown | Pop-ups, alerts                        |
| TC05 | Dismiss JS Confirm          | 1. Open `/javascript_alerts` 2. Click "JS Confirm" button 3. Dismiss dialog                                           | Dialog dismissed, "You clicked: Cancel" shown             | Pop-ups, confirm dialogs               |
| TC06 | Send text to JS Prompt      | 1. Open `/javascript_alerts` 2. Click "JS Prompt" button 3. Type text 4. Accept                                       | Text entered and displayed in result                      | Pop-ups, prompt dialogs                |
| TC07 | End-to-end workflow         | 1. Iframe interaction 2. Dynamic controls + AJAX 3. Alert handling                                                    | All three scenarios pass in sequence                      | Combined advanced techniques           |

---

## Sample Code

### Project Structure

```
lab_selenium/
├── requirements.txt                        # Python dependencies
├── pytest.ini                              # Pytest configuration
├── Jenkinsfile                             # Jenkins CI/CD pipeline
├── reports/
│   ├── report.html                         # Generated HTML test report
│   └── screenshots/                        # Failure screenshots
└── tests/
    ├── conftest.py                         # Driver fixture + reporting hooks
    ├── test_advanced_interactions.py        # 7 test cases
    ├── pages/
    │   ├── base_page.py                    # Base Page Object class
    │   ├── dynamic_controls_page.py        # Dynamic elements & AJAX
    │   ├── iframe_page.py                  # Iframe interaction
    │   └── alerts_page.py                  # JS Alert handling
    └── utils/
        ├── wait_utils.py                   # Explicit wait functions
        └── element_utils.py                # Alert, frame & element utilities
```

### Key Code Snippets

#### Implicit Wait (conftest.py)

```python
@pytest.fixture(scope="function")
def driver(request):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    browser = webdriver.Chrome(options=chrome_options)
    browser.implicitly_wait(10)          # Implicit wait — 10 seconds
    browser.set_page_load_timeout(30)    # Page load timeout
    yield browser
    browser.quit()
```

#### Explicit Wait (wait_utils.py)

```python
def wait_for_element_visible(driver, locator, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )

def wait_for_alert_present(driver, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.alert_is_present()
    )
```

#### XPath & CSS Locators (dynamic_controls_page.py)

```python
# XPath with contains()
CHECKBOX = (By.XPATH, "//input[@type='checkbox']")
# XPath with text()
MESSAGE = (By.XPATH, "//p[@id='message']")
# XPath with descendant axis
ENABLE_BUTTON = (By.XPATH, "//form[@id='input-example']//descendant::button")
# CSS Selector
TEXT_INPUT = (By.CSS_SELECTOR, "#input-example input[type='text']")
```

#### Alert Handling (element_utils.py)

```python
def accept_alert(driver, timeout=10):
    alert = wait_for_alert_present(driver, timeout)
    alert_text = alert.text
    alert.accept()
    return alert_text
```

#### Iframe Switching (iframe_page.py)

```python
def switch_to_editor_frame(self):
    self.switch_to_frame(self.EDITOR_IFRAME)

def switch_back_to_main(self):
    self.switch_to_main_content()  # driver.switch_to.default_content()
```

#### Jenkinsfile

```groovy
pipeline {
    agent any
    stages {
        stage('Setup Environment') {
            steps {
                sh 'python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'pytest tests/ --html=reports/report.html --self-contained-html -v'
            }
        }
    }
    post {
        always {
            publishHTML(target: [reportDir: 'reports', reportFiles: 'report.html',
                                 reportName: 'Selenium Test Report'])
        }
    }
}
```

---

## Bug Reports

No bugs were found during test execution. All 7 test cases passed successfully.

| Bug ID | Severity | Description   | Status |
| ------ | -------- | ------------- | ------ |
| —      | —        | No bugs found | N/A    |

> Note: If bugs were found, they would be documented here with steps to reproduce, expected vs actual behavior, and severity classification.

---

## Screenshots

### Test Execution — All 7 Tests Passed

```
tests/test_advanced_interactions.py::TestDynamicElements::test_remove_and_add_checkbox_via_ajax      PASSED
tests/test_advanced_interactions.py::TestDynamicElements::test_enable_input_field_via_ajax           PASSED
tests/test_advanced_interactions.py::TestFramesAndIframes::test_interact_with_iframe_editor          PASSED
tests/test_advanced_interactions.py::TestAlertsAndPopups::test_accept_js_alert                       PASSED
tests/test_advanced_interactions.py::TestAlertsAndPopups::test_dismiss_js_confirm                    PASSED
tests/test_advanced_interactions.py::TestAlertsAndPopups::test_send_text_to_js_prompt                PASSED
tests/test_advanced_interactions.py::TestComprehensiveScenario::test_full_advanced_automation_workflow PASSED

7 passed in 36.67s
```

### HTML Report

The generated HTML report is available at `reports/report.html` containing:

- Pass/fail status for every test
- Screenshots automatically captured on failure
- Execution time per test

---

## Result

All **7 test cases passed** successfully in **36.67 seconds**, demonstrating:

1. ✅ Dynamic web elements handled via AJAX with explicit waits
2. ✅ Web elements identified using advanced XPath and CSS selectors
3. ✅ Both implicit (10s global) and explicit waits implemented — no `time.sleep()` used
4. ✅ JavaScript alerts (accept), confirms (dismiss), and prompts (send text) managed
5. ✅ Iframe switching and content manipulation completed
6. ✅ Page Object Model (POM) design pattern established
7. ✅ HTML test report generated with screenshot-on-failure capability
8. ✅ Jenkins CI pipeline configured via `Jenkinsfile` for seamless automation

The experiment successfully demonstrates advanced Selenium WebDriver techniques for testing complex web applications with proper automation best practices, reporting, and CI integration.
