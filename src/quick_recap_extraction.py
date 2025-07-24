import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIG ---
SLACK_URL = "https://app.slack.com/client/T2AAHSB5F"

# --- SETUP SELENIUM ---
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36')
# chrome_options.add_argument('--headless')  # Uncomment for headless mode

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(10)

print(f"Navigating to: {SLACK_URL}")
driver.get(SLACK_URL)
time.sleep(10)  # Wait for JS to load

page_text = driver.find_element('tag name', 'body').text
print("\n--- PAGE TEXT START ---\n")
print(page_text[:2000])  # Print first 2000 chars for inspection
print("\n--- PAGE TEXT END ---\n")

driver.quit()
print("Done.")
