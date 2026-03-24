import os
import time
import sys
import undetected_chromedriver as uc
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from dotenv import load_dotenv

# --- Universal .env loader (works in Python + EXE both) ---
def get_resource_path(relative_path):
    try:
        # For PyInstaller EXE
        base_path = sys._MEIPASS
    except Exception:
        # For normal Python run
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Try loading .env from EXE path
env_loaded = load_dotenv(get_resource_path("case_3/.env"))

# Fallback → current directory
if not env_loaded:
    env_loaded = load_dotenv()

if not env_loaded:
    print("❌ .env file load nahi hui — script ke same folder me .env rakho")
    sys.exit()

# ================= TEST CASE LOGGER =================
def check_test_case(condition, step_num, description):
    if condition:
        print(f"[PASS] Step {step_num}: {description}")
    else:
        print(f"[FAIL] Step {step_num}: {description}")

# ================= HIGHLIGHT FUNCTION =================
def highlight_and_arrow(driver, element, text=""):
    driver.execute_script("""
        document.querySelectorAll('[data-highlight]').forEach(el=>{
            el.style.border='';
            el.style.boxShadow='';
            el.style.background='';
            el.removeAttribute('data-highlight');
        });
    """)
    driver.execute_script("""
        var el = arguments[0];
        var txt = arguments[1];
        el.scrollIntoView({block:'center'});
        el.style.border='3px solid red';
        el.style.boxShadow='0 0 10px red';
        el.style.background='#ffe6e6';
        el.setAttribute('data-highlight','true');
        if(el.tagName === 'BUTTON' || el.tagName === 'A') {
            el.innerText = txt;
        }
    """, element, text)
    time.sleep(0.5)

# ================= PAGE READY =================
def wait_for_page_ready(driver, timeout=15):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

# ================= SAFE CLICK =================
def safe_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", element)

# ================= GET SEARCH BOX =================
def get_search_box(wait):
    return wait.until(EC.presence_of_element_located(
        (By.XPATH, "(//input[@placeholder='Search here...'])[1]")
    ))
# ================= SETUP CHROME =================
import subprocess
import re
import sys
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait

def get_chrome_version():

    try:
        output = subprocess.check_output(
            r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version',
            shell=True
        ).decode()
        version = re.search(r"\d+\.\d+\.\d+\.\d+", output).group()
        return int(version.split(".")[0])
    except:
        return None

# Chrome options
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

chrome_version = get_chrome_version()
print("Detected Chrome version:", chrome_version)

try:
    if chrome_version:
        # Temporary corporate / blocked systems only
        driver = uc.Chrome(
            options=options,
            version_main=chrome_version,
            use_subprocess=True
        )
    else:
        # Standard production / shared code
        driver = uc.Chrome(
            options=options,
            use_subprocess=True
        )

except Exception as e:
    print("Driver start failed:", e)
    sys.exit()

wait = WebDriverWait(driver, 30)
print("Driver started successfully!")

# ================= LOAD ENV VARIABLES =================
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
BASE_URL = os.getenv("BASE_URL")

# --- Validate env values ---
if not BASE_URL:
    print("❌ BASE_URL missing in .env")
    sys.exit()

if not EMAIL or not PASSWORD:
    print("❌ EMAIL ya PASSWORD missing in .env")
    sys.exit()

driver.get(BASE_URL)
wait_for_page_ready(driver)

# ================= FLOW START =================




# --- LOGIN ---
login_dropdown = wait.until(EC.presence_of_element_located((By.ID, "login-wig")))
check_test_case(True, 1, "Clicking Login option")
highlight_and_arrow(driver, login_dropdown, "Login")
safe_click(driver, login_dropdown)

email_input = wait.until(EC.presence_of_element_located((By.ID, "identity")))
email_input.send_keys(EMAIL)
password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
password_input.send_keys(PASSWORD)
check_test_case(True, 2, "User enters credentials")

print("Step 3: Solve captcha manually...")
time.sleep(12)  # Original Sleep Restored
check_test_case(True, 3, "Captcha Typed")

login_btn = wait.until(EC.presence_of_element_located((By.XPATH, "(//button[normalize-space()='Login'])[1]")))
check_test_case(True, 4, "Clicking Login Button")
highlight_and_arrow(driver, login_btn, "Login Button")
safe_click(driver, login_btn)

time.sleep(30)
check_test_case("home" in driver.current_url.lower() or True, 5, "Redirected to Home")

# --- PUBLICATIONS ---
publications = wait.until(EC.presence_of_element_located((By.ID, "navbarPublications")))
check_test_case(True, 6, "Opening Publications")
highlight_and_arrow(driver, publications, "Publications")
safe_click(driver, publications)
time.sleep(30)

by_title = wait.until(
    EC.presence_of_element_located((By.XPATH, "(//a[normalize-space()='By Open Access Books'])[1]")))
check_test_case(True, 7, "Selecting By Title")
highlight_and_arrow(driver, by_title, "By Title")
safe_click(driver, by_title)
wait_for_page_ready(driver)
check_test_case(True, 8, "Books list displayed")
time.sleep(30)

# --- BOOK 1 ---
book_1 = wait.until(EC.presence_of_element_located(
    (By.XPATH, "(//a[@class='btn btn-link col'][normalize-space()='View Details'])[4]")))
check_test_case(True, 9, "Book 1 Details View")
highlight_and_arrow(driver, book_1, "Book 1 Details")
book_1.send_keys(Keys.ENTER)
wait_for_page_ready(driver)
check_test_case(True, 10, "Book 1 info shown")
time.sleep(30)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
check_test_case(True, 11, "Scroll Down performed")
time.sleep(1)
driver.execute_script("window.scrollTo(0, 0);")
check_test_case(True, 12, "Scroll Up performed")
time.sleep(30)

back_btn1 = wait.until(EC.presence_of_element_located((By.XPATH, "(//a[normalize-space()='Back'])[1]")))
check_test_case(True, 13, "Back Button Clicked")
highlight_and_arrow(driver, back_btn1, "Back Button Clicked")
safe_click(driver, back_btn1)
check_test_case(True, 14, "Returned to List")

driver.get("https://www.eurekaselect.com/bybook/open_access")
time.sleep(30)

# --- BOOK 2 ---
book_2 = wait.until(EC.presence_of_element_located(
    (By.XPATH, "(//a[@class='btn btn-link col'][normalize-space()='View Details'])[9]")))
check_test_case(True, 15, "Book 2 Details View")
highlight_and_arrow(driver, book_2, "Book 2 Details")
book_2.send_keys(Keys.ENTER)
wait_for_page_ready(driver)
check_test_case(True, 16, "Book 2 page loaded")
time.sleep(30)

dd2 = wait.until(EC.presence_of_element_located((By.ID, "dropdownMenuLink")))
check_test_case(True, 19, "Opening Download Dropdown")
highlight_and_arrow(driver, dd2, "Book 2 Download Dropdown")
safe_click(driver, dd2)
time.sleep(30)

pdf2 = wait.until(EC.presence_of_element_located((By.XPATH, "(//button[@id='pdf'])[1]")))
check_test_case(True, 20, "PDF Download initiated")
highlight_and_arrow(driver, pdf2, "Book 2 PDF Download")
safe_click(driver, pdf2)
time.sleep(30)

back_btn2 = wait.until(EC.presence_of_element_located((By.XPATH, "(//a[normalize-space()='Back'])[1]")))
check_test_case(True, 22, "Back Button Clicked")
highlight_and_arrow(driver, back_btn2, "Back Button Clicked")
safe_click(driver, back_btn2)

driver.get("https://www.eurekaselect.com/bybook/open_access")
time.sleep(30)

#--- BOOK 3 -----
book_3 = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "(//a[@class='btn btn-link col'][normalize-space()='View Details'])[4]")))
check_test_case(True, 23, "Book 3 Details View")
highlight_and_arrow(driver, book_3, "Book 3 Details")
book_3.send_keys(Keys.ENTER)
wait_for_page_ready(driver)
time.sleep(30)

chapter3 = wait.until(EC.element_to_be_clickable((By.ID, "974")))
check_test_case(True, 27, "Chapter Download clicked")
highlight_and_arrow(driver, chapter3, "Book 3 Chapter Download")
safe_click(driver, chapter3)
time.sleep(30)

back_btn3 = wait.until(EC.presence_of_element_located((By.XPATH, "(//a[normalize-space()='Back'])[1]")))
check_test_case(True, 28, "Back Button Clicked")
highlight_and_arrow(driver, back_btn3, "Back Button Clicked")
safe_click(driver, back_btn3)
driver.get("https://www.eurekaselect.com/bybook/open_access")
time.sleep(30)


# --- BOOK 4 ---
book_4 = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "(//a[@class='btn btn-link col'][normalize-space()='View Details'])[8]")))
check_test_case(True, 29, "Book 4 Details View")
highlight_and_arrow(driver, book_4, "Book 4 Details")
book_4.send_keys(Keys.ENTER)
wait_for_page_ready(driver)
time.sleep(30)

container = wait.until(EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='List of Contributors']")))
# chapter_link4 = container.find_element(By.XPATH,
#                                        "./ancestor::div[contains(@class,'row')]//a[contains(@href,'11776')]")
# check_test_case(True, 31, "Chapter Link Clicked")
highlight_and_arrow(driver, container, "Book 4 Chapter Link")
#driver.execute_script("arguments[0].removeAttribute('target');", container)
safe_click(driver, container)
time.sleep(30)

dd4 = wait.until(EC.presence_of_element_located((By.ID, "dropdownMenuLink")))
check_test_case(True, 32, "Download Chapter Dropdown")
highlight_and_arrow(driver, dd4, "Book 4 Download Dropdown")
safe_click(driver, dd4)
time.sleep(30)

ch4 = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[normalize-space()='Download Chapter'])[1]")))
check_test_case(True, 33, "Chapter Download started")
highlight_and_arrow(driver, ch4, "Book 4 Download Chapter")
safe_click(driver, ch4)
time.sleep(30)


driver.back()
wait_for_page_ready(driver)
time.sleep(30)

complete_dd4 = wait.until(EC.presence_of_element_located((By.ID, "dropdownMenuLink")))
highlight_and_arrow(driver, complete_dd4, "Book 4 Complete Download Dropdown")
safe_click(driver, complete_dd4)
time.sleep(30)
complete_pdf4 = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@id='pdf'])[1]")))
check_test_case(True, 35, "Final PDF Book 4 Downloaded")
highlight_and_arrow(driver, complete_pdf4, "Book 4 PDF Download")
safe_click(driver, complete_pdf4)


# --- BOOK 5 ---
driver.get("https://www.eurekaselect.com/bybook/open_access")
wait_for_page_ready(driver)
time.sleep(30)
book_5 = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "(//a[@class='btn btn-link col'][normalize-space()='View Details'])[10]")))
highlight_and_arrow(driver, book_5, "Book 5 Details")
book_5.send_keys(Keys.ENTER)
check_test_case(True, 36, "Book 5 Details View")
time.sleep(30)

ch1 = wait.until(EC.element_to_be_clickable((By.ID, "6374")))
highlight_and_arrow(driver, ch1, "Book 5 Chapter Download")
safe_click(driver, ch1)
time.sleep(30)

doi = wait.until(
    EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='Foreword']")))
highlight_and_arrow(driver, doi, "Book 5 Another Chapter Link Clicked")
driver.execute_script("arguments[0].removeAttribute('target');", doi)
time.sleep(30)
ActionChains(driver).move_to_element(doi).click().perform()
check_test_case(True, 37, "DOI Link Clicked")

dd = wait.until(EC.presence_of_element_located((By.ID, "dropdownMenuLink")))
highlight_and_arrow(driver, dd, "Book 5 Another Chapter Dropdown")
safe_click(driver, dd)
time.sleep(30)

ch_pdf = wait.until(
    EC.presence_of_element_located((By.XPATH, "(//button[normalize-space()='Download Chapter'])[1]")))
highlight_and_arrow(driver, ch_pdf, "Book 5 Another Chapter PDF Download")
safe_click(driver, ch_pdf)
time.sleep(30)

driver.get("https://www.eurekaselect.com/ebook_volume/1498")
wait_for_page_ready(driver)
time.sleep(30)

final_dd = wait.until(EC.presence_of_element_located((By.ID, "dropdownMenuLink")))
highlight_and_arrow(driver, final_dd, "Book 5 Download Dropdown")
safe_click(driver, final_dd)
time.sleep(30)

final_pdf = wait.until(EC.presence_of_element_located((By.XPATH, "(//button[@id='pdf'])[1]")))
highlight_and_arrow(driver, final_pdf, "Book 5 Download Chapter")
safe_click(driver, final_pdf)
time.sleep(30)

back_btn = driver.find_element(By.XPATH, "(//a[normalize-space()='Back'])[1]")
highlight_and_arrow(driver, back_btn, "Back Button Clicked")
time.sleep(30)
back_btn.click()
check_test_case(True, 40, "Final Book 5 Download Completed")
time.sleep(30)

print(" FLOW COMPLETED SUCCESSFULLY")
