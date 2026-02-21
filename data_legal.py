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
        
        # --- ՏԵՍԱՆԵԼԻ ՌԵԺԻՄԻ ԿԱՐԳԱՎՈՐՈՒՄՆԵՐ ---
        # Հեռացրել ենք --headless-ը, որպեսզի պատուհանը բացվի
        chrome_options.add_argument("--window-size=1366,768")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Նկարները թողնում ենք միացված, որ տեսարանը լրիվ լինի (կամ 2-ի փոխարեն դիր 1)
        prefs = {"profile.managed_default_content_settings.images": 1}
        chrome_options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(options=chrome_options)

    def safe_click(self, element):
        # Էջը սքրոլ ենք անում դեպի կոճակը, որ տեսնես գործողությունը
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)
        time.sleep(0.8) # Դադար, որ մարդու աչքի համար տեսանելի լինի
        self.driver.execute_script("arguments[0].click();", element)

    def open_page(self):
        print(f"Բացվում է կայքը... {self.url}")
        self.driver.get(self.url)

    def find_data_politis(self):
        
        # 1. Politics բաժնի հղումը
        try:
            politics_link = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-item-773"]/ag'))
            )
            self.safe_click(politics_link)
            print("Politics բաժինը բացվեց:")
        except Exception as e:
            print(f"Չհաջողվեց գտնել բաժինը: {e}")
            return

        results_list = []
        n = 11
        numbers_to_click = [6, 8, 9, 10] + [n] * 500 

        for i, num in enumerate(numbers_to_click):
            try:
                # Սպասում ենք կոնտենտին
                content_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'col-md-8'))
                )
                
                # Տեքստի քաղում և ստորակետի ավելացում
                text_data = content_element.text
                clean_text = re.sub(r'[^a-zA-Z\s]', '', text_data).replace('\n', ' ').strip()
                results_list.append(clean_text + ",")
                
                print(f"Էջ {i+1} մշակված է: Կոճակը՝ {num}")

                # 2. Հաջորդ էջի կոճակը (Օգտագործում ենք CSS Selector, քանի որ քո տրամադրածը CSS էր)
                css_selector = f"body > main > div > div > div.col-md-8 > div > div.post-pagination.clearfix > ul > li:nth-child({num}) > a"
                button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
                )
                
                self.safe_click(button)
                time.sleep(1.5) # Դադար, որ տեսնես էջի բեռնումը
                
            except Exception as e:
                print(f"Ավարտ կամ սխալ {i+1}-րդ էջում: {str(e)[:50]}")
                break
        
        # 3. Պահպանում ենք քո ուզած label,text ձևաչափով
        df = pd.DataFrame({
            'label': ['Politics'] * len(results_list),
            'text': results_list
        })
        
        df.to_csv('legal.csv', index=False, encoding='utf-8-sig')
        print(f"Ավարտված է: {len(results_list)} տող պահպանվեց 'politics.csv' ֆայլում:")

    def close(self):
        # Վերջում բրաուզերը միանգամից չփակելու համար
        input("Սեղմեք Enter բրաուզերը փակելու համար...")
        self.driver.quit()

if __name__ == '__main__':
    data = DataFinder('https://en.aravot.am/')
    try:
        data.open_page()
        data.find_data_politis()
    except Exception as error:
        print("Գլխավոր սխալ: " + str(error))
    finally:
        data.close()