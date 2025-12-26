from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class InventoryPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")

    def add_product_to_cart(self, product_name):
        add_btn = (
            By.XPATH,
            f"//div[text()='{product_name}']/ancestor::div[@class='inventory_item']//button"
        )
        self.click(add_btn)

    def get_title(self):
        return self.get_text(self.TITLE)
