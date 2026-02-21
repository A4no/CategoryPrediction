from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import csv

class DataFinder:
    def __init__(self, url):
        self.url = url
        chrome_options = Options()
        
        # --- ԱՅՍՏԵՂ ՓՈՓՈԽՈՒԹՅՈՒՆ ԵՆՔ ԱՐԵԼ ---
        # headless-ը հանված է, որպեսզի պատուհանը բացվի
        chrome_options.add_argument("--window-size=1200,900") 
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Պահում ենք նկարների անջատումը, որ ավելի արագ լինի, բայց եթե ուզում ես նկարներն էլ տեսնել,
        # կարող ես ջնջել ստորև բերված 2 տողը:
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(options=chrome_options)

    def safe_click(self, element):
        # Էկրանը սքրոլ ենք անում դեպի կոճակը, որ տեսնես՝ ինչ է կատարվում
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.5) 
        self.driver.execute_script("arguments[0].click();", element)

    def open_page(self):
        print(f"Մուտք ենք գործում {self.url}...")
        self.driver.get(self.url)

    def find_data_sport(self):
        try:
            # Օգտագործում ենք քո տրամադրած սելեկտորը
            link = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#menu-item-769 > a"))
            )
            self.safe_click(link)
            print("Culture բաժինը բացվեց:")
        except Exception as e:
            print("Սխալ՝ բաժինը չգտնվեց:", str(e)[:50])
            return

        results_list = []
        n = 11
        numbers_to_click = [6, 8, 9, 10] + [n] * 500 

        for i, num in enumerate(numbers_to_click):
            try:
                # Սպասում ենք բեռնմանը
                content = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div[1]/div'))
                )
                
                # Տեքստի մշակում
                text_data = content.text
                clean_text = re.sub(r'[^a-zA-Z\s]', '', text_data).replace('\n', ' ').strip()
                results_list.append([clean_text + ","])
                
                print(f"Էջ {i+1} մշակված է:")

                # Գտնում ենք հաջորդ էջի կոճակը
                xpath = f"/html/body/main/div/div/div[1]/div/div[11]/ul/li[{num}]/a"
                button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                
                # Սեղմում ենք կոճակը
                self.safe_click(button)
                
                # Դադար ենք տալիս, որ դու հասցնես աչքով տեսնել փոփոխությունը
                time.sleep(1.5) 

            except Exception as e:
                print(f"Պրոցեսն ավարտվեց {i+1} էջում:")
                break
        
        # CSV պահպանում
        try:
            with open('sport.csv', 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
                writer.writerow(['Sport'])
                writer.writerows(results_list)
            print(f"Ֆայլը պահպանվեց: {len(results_list)} տող:")
        except Exception as e:
            print("Ֆայլի սխալ:", e)

    def close(self):
        # Ծրագրի վերջում բրաուզերը միանգամից չփակելու համար
        input("Սեղմեք Enter բրաուզերը փակելու համար...")
        self.driver.quit()

url = 'https://en.aravot.am/'

def main():
    data = DataFinder(url)
    try:
        data.open_page()
        data.find_data_sport()
    except Exception as error:
        print("Գլխավոր սխալ: " + str(error))
    finally:
        data.close()

if __name__ == '__main__':
    main()
    