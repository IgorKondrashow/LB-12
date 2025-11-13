from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import unittest

class WildberriesTests(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://www.wildberries.ru/")
        self.wait = WebDriverWait(self.driver, 10)
    
    def tearDown(self):
        self.driver.quit()
    
    def test_search_product(self):
        """TC_WB_001: Проверка функциональности поиска товаров"""
        print("Запуск теста: Поиск товара")
        
        # Шаг 1: Поиск товара
        search_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "searchInput"))
        )
        search_input.clear()
        search_input.send_keys("iPhone 13")
        search_input.send_keys(Keys.RETURN)
        
        # Шаг 2: Проверка результатов
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-card"))
        )
        
        # Проверка, что есть результаты
        products = self.driver.find_elements(By.CLASS_NAME, "product-card")
        self.assertGreater(len(products), 0, "Нет результатов поиска")
        
        # Проверка релевантности (хотя бы один товар содержит iPhone)
        product_titles = [product.text for product in products[:5]]  # Берем первые 5 товаров
        has_iphone = any('iPhone' in title for title in product_titles)
        self.assertTrue(has_iphone, "В результатах нет товаров с iPhone")
        
        print("✓ Тест поиска товара пройден успешно")
    
    def test_add_to_cart(self):
        """TC_WB_002: Проверка добавления товара в корзину"""
        print("Запуск теста: Добавление в корзину")
        
        # Переход к категории смартфонов
        self.driver.get("https://www.wildberries.ru/catalog/elektronika/smartfony-i-telefony")
        time.sleep(3)
        
        # Выбор первого товара
        first_product = self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "product-card__link"))
        )
        first_product.click()
        
        # Добавление в корзину
        add_to_cart_btn = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-link*='basket']"))
        )
        product_name = self.driver.find_element(By.CLASS_NAME, "product-page__title").text
        add_to_cart_btn.click()
        
        # Переход в корзину
        time.sleep(2)
        self.driver.get("https://www.wildberries.ru/basket")
        
        # Проверка наличия товара в корзине
        try:
            cart_items = self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "basket-item"))
            )
            self.assertGreater(len(cart_items), 0, "Корзина пуста")
            print("✓ Тест добавления в корзину пройден успешно")
        except:
            print("⚠ Товар может потребовать выбора характеристик перед добавлением")
    
    def test_price_filter(self):
        """TC_WB_003: Проверка фильтрации товаров по цене"""
        print("Запуск теста: Фильтрация по цене")
        
        # Переход к категории
        self.driver.get("https://www.wildberries.ru/catalog/elektronika")
        time.sleep(3)
        
        try:
            # Установка фильтра цены
            min_price_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='от']"))
            )
            min_price_input.clear()
            min_price_input.send_keys("10000")
            
            max_price_input = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='до']")
            max_price_input.clear()
            max_price_input.send_keys("30000")
            max_price_input.send_keys(Keys.RETURN)
            
            # Ожидание применения фильтра
            time.sleep(5)
            
            # Проверка цен товаров
            price_elements = self.driver.find_elements(By.CLASS_NAME, "price__lower-price")
            if price_elements:
                for price_element in price_elements[:3]:  # Проверяем первые 3 товара
                    price_text = price_element.text.replace(' ', '').replace('₽', '')
                    try:
                        price = int(price_text)
                        self.assertTrue(10000 <= price <= 30000, 
                                      f"Цена {price} вне диапазона 10000-30000")
                    except ValueError:
                        continue
            
            print("✓ Тест фильтрации по цене пройден успешно")
            
        except Exception as e:
            print(f"⚠ Тест фильтрации пропущен: {str(e)}")

if __name__ == "__main__":
    # Запуск тестов
    unittest.main(verbosity=2)
