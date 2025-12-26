import csv
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

@pytest.mark.parametrize("user_type", ["valid_user", "invalid_user"])
@pytest.mark.flaky(reruns=2)
def test_e2e_flow(driver, config, user_type):
    driver.get(config["url"])
    login = LoginPage(driver)
    creds = config[user_type]

    login.login(creds["username"], creds["password"])
    driver.save_screenshot("screenshots/login.png")

    if user_type == "invalid_user":
        assert "locked" in login.get_error_message().lower()
        return

    inventory = InventoryPage(driver)
    assert inventory.get_title() == "Products"

    with open("data/products.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            inventory.add_product_to_cart(row["product_name"])

    cart = CartPage(driver)
    cart.go_to_cart()
    driver.save_screenshot("screenshots/cart.png")

    cart.checkout()

    checkout = CheckoutPage(driver)
    checkout.fill_details()
    checkout.finish_order()
    driver.save_screenshot("screenshots/confirmation.png")

    assert "Thank you for your order!" in checkout.get_confirmation()
