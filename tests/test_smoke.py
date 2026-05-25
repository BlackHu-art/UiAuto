import logging

import pytest
from appium.webdriver.common.appiumby import AppiumBy

LOGGER = logging.getLogger(__name__)


@pytest.mark.smoke
@pytest.mark.order(2)
def test_app_launches(driver):
    LOGGER.info(
        "Launch test started: session_id=%s package=%s activity=%s",
        driver.session_id,
        driver.current_package,
        driver.current_activity,
    )
    assert driver.session_id
    assert driver.current_package
    LOGGER.info("Launch test passed: package=%s activity=%s", driver.current_package, driver.current_activity)


@pytest.mark.sample
@pytest.mark.order(3)
def test_configured_smoke_element_is_visible(driver, app_settings):
    if not app_settings.smoke_accessibility_id:
        pytest.skip("Set SMOKE_ACCESSIBILITY_ID to run this locator-based sample test.")

    LOGGER.info("Checking smoke element: accessibility_id=%s", app_settings.smoke_accessibility_id)
    element = driver.find_element(
        AppiumBy.ACCESSIBILITY_ID,
        app_settings.smoke_accessibility_id,
    )

    assert element.is_displayed()
    LOGGER.info("Smoke element is visible: accessibility_id=%s", app_settings.smoke_accessibility_id)
