from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    CHECKOUT_BTN = (By.ID, "checkout")

    def go_to_cart(self):
        self.click(self.CART_ICON)
        self.wait.until(EC.presence_of_element_located(self.CHECKOUT_BTN))

    def checkout(self):
        self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BTN)).click()
