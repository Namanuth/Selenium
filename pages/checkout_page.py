from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE = (By.ID, "continue")
    FINISH = (By.ID, "finish")
    CONFIRMATION = (By.CLASS_NAME, "complete-header")

    def fill_details(self):
        self.find(self.FIRST_NAME).send_keys("Naman")
        self.find(self.LAST_NAME).send_keys("Agarwal")
        self.find(self.POSTAL_CODE).send_keys("110001")
        self.click(self.CONTINUE)

    def finish_order(self):
        self.click(self.FINISH)

    def get_confirmation(self):
        return self.get_text(self.CONFIRMATION)
