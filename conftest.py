import os
import pytest
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="session")
def config():
    with open("config/config.json") as f:
        return json.load(f)

@pytest.fixture
def driver():
    chrome_options = Options()

    if os.getenv("CI"):
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

    # Allow using a pre-installed chromedriver via env var for offline/local dev
    chromedriver_path = os.environ.get("CHROMEDRIVER_PATH")
    driver = None

    if chromedriver_path:
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
    else:
        try:
            # Try to download the matching chromedriver (works in CI)
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            # Fallback: try to use chromedriver on PATH (useful when offline or SSL fails)
            import warnings
            warnings.warn(
                "Failed to download chromedriver (network/SSL issue). Falling back to chromedriver on PATH."
            )
            try:
                driver = webdriver.Chrome(options=chrome_options)
            except Exception as e2:
                # Give user actionable guidance
                raise RuntimeError(
                    "Could not start Chrome driver. If you're offline or seeing SSL errors, either install chromedriver locally and set CHROMEDRIVER_PATH, or fix macOS certs (run the 'Install Certificates.command' that comes with your Python installation), or install chromedriver with Homebrew: 'brew install --cask chromedriver'.\nOriginal error: %s" % e
                ) from e2

    driver.maximize_window()
    yield driver
    driver.quit()
