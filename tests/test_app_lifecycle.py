import logging

import pytest

LOGGER = logging.getLogger(__name__)


@pytest.mark.smoke
@pytest.mark.order(1)
def test_app_can_be_installed(driver, app_settings):
    if not app_settings.app_path:
        pytest.skip("Set ANDROID_APP_PATH to run APK install test.")

    package_name = driver.current_package
    LOGGER.info("Install test started: package=%s apk=%s", package_name, app_settings.app_path)
    if driver.is_app_installed(package_name):
        LOGGER.info("Removing existing app before install: package=%s", package_name)
        driver.remove_app(package_name)

    LOGGER.info("Installing app: %s", app_settings.app_path)
    driver.install_app(str(app_settings.app_path))

    assert driver.is_app_installed(package_name)
    LOGGER.info("Install test passed: package=%s", package_name)


@pytest.mark.smoke
@pytest.mark.order(4)
def test_app_can_be_uninstalled(driver):
    package_name = driver.current_package
    LOGGER.info("Uninstall test started: package=%s", package_name)

    driver.remove_app(package_name)

    assert not driver.is_app_installed(package_name)
    LOGGER.info("Uninstall test passed: package=%s", package_name)
