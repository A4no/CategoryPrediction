from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pandas as pd

class DataFinder:
    def __init__(self, url):
        self.url = url
        chrome_options = Options()
        
        # 1. Դարձնում ենք տեսանելի (Visible mode)
        chrome_options.add_argument("--window-size=1200,900")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Նկարները անջատում ենք արագության համար
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(options=chrome_options)

    def safe_click(self, element):
        # Սքրոլ ենք անում դեպի կոճակը և սեղմում
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", element)

    def open_page(self):
        print(f"Բացում ենք կայքը: {self.url}")
        self.driver.get(self.url)

    def find_data_culture(self):
        # 1. Սեղմում ենք Politics (կամ Culture) բաժինը
        # Ուղղված սելեկտոր
        try:
            category_link = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#menu-item-770 > a'))
            )
            self.safe_click(category_link)
            print("Բաժինը բացվեց:")
        except:
            print("Չհաջողվեց գտնել բաժնի կոճակը:")
            return

        results_list = []
        n = 11
        numbers_to_click = [6, 8, 9, 10] + [n] * 500 

        for i, num in enumerate(numbers_to_click):
            try:
                # Սպասում ենք, որ էջի նյութերը բեռնվեն
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#menu-item-770 > a'))
                )
                
                # 2. Վերցնում ենք տեքստը
                content = self.driver.find_element(By.CSS_SELECTOR, 'body > main > div > div > div.col-md-8 > div')
                
                # Մաքրում ենք և ավելացնում ստորակետ տողի վերջում
                clean_text = re.sub(r'[^a-zA-Z\s]', '', content.text).replace('\n', ' ').strip()
                results_list.append(clean_text + ",")
                
                print(f"Էջ {i+1} մշակված է:")

                # 3. Գտնում ենք pagination-ի հաջորդ կոճակը
                xpath = f"/html/body/main/div/div/div[1]/div/div[11]/ul/li[{num}]/a"
                button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                
                self.safe_click(button)
                time.sleep(1) # Թողնում ենք էջը թարմացվի
                
            except Exception as e:
                print(f"Պրոցեսն ավարտվեց կամ սխալ {num} կոճակի մոտ: {str(e)[:50]}")
                break
            
        # 4. Պահպանում ենք CSV
        if results_list:
            df = pd.DataFrame(results_list, columns=['Content'])
            df.to_csv('culture.csv', index=False, encoding='utf-8-sig')
            print(f"Հաջողությամբ պահպանվեց {len(results_list)} տող culture.csv ֆայլում:")
        else:
            print("Տվյալներ չեն հավաքվել:")

    def close(self):
        self.driver.quit()

url = 'https://en.aravot.am/'

def main():
    data = DataFinder(url)
    try:
        data.open_page()
        data.find_data_culture()
    except Exception as error:
        print("Գլխավոր սխալ: " + str(error))
    finally:
        data.close()

if __name__ == '__main__':
    main()