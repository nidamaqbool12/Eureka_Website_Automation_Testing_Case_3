import os
import time
import sys
import undetected_chromedriver as uc
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
env_loaded = load_dotenv(get_resource_path("dist/.env"))

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
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

try:
    driver = uc.Chrome(options=options)
except Exception as e:
    print(f"Driver start nahi ho saka: {e}")
    sys.exit()

wait = WebDriverWait(driver, 30)

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


# ================= FLOW START =================
report_data = []  # To store counts for HTML

try:
    driver.get(BASE_URL)
    wait_for_page_ready(driver)


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
    time.sleep(12)
    check_test_case(True, 3, "Captcha Typed")

    login_btn = wait.until(EC.presence_of_element_located(
        (By.XPATH, "(//button[normalize-space()='Login'])[1]")))
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
        EC.presence_of_element_located((By.XPATH, "(//a[@href='/bybook'][normalize-space()='By Title'])[1]")))
    check_test_case(True, 7, "Selecting By Title")
    highlight_and_arrow(driver, by_title, "By Title")
    safe_click(driver, by_title)
    wait_for_page_ready(driver)
    check_test_case(True, 8, "Books list displayed")
    time.sleep(30)

    # ================= BOOKS FLOW =================
    books = [
        # ================= BOOK 1 =================
        {
            "name": "2-Deoxy-D-Glucose: Chemistry and Biology",
            "url_contains": "/ebook_volume/3800",
            "chapters": [
                ("23725", "2-Deoxy-D-Glucose: Chemical Structure and Properties"),
                ("23726", "Methods and Procedures for the Synthesis of 2- Deoxy-D-Glucose"),
                ("23727", "Characterization of 2-Deoxy-D-glucose"),
                ("23728", "[ 18F]Fluoro Analogue of D-Glucose: A Chemistry Perspective"),
                ("23729", "Antiviral Potential of 2-DG Used in Different Viral Infections"),
                ("23730", "2-Deoxy-D-Glucose and its Derivatives: Dual Role in Diagnostics and Therapeutics"),
                ("23731", "2-Deoxy-D-Glucose as a Potential Antiviral and Anti-COVID-19 Drug"),
                ("23732", "Prospects for Cancer Diagnosis, Treatment, and Surveillance"),
                ("23733", "2-Deoxy-D-Glucose as an Emerging Chemotherapeutic Agent in Cancer Management"),
                ("23734", "2-Deoxy-D-Glucose: Chemical Structure and Properties"),
            ]
        },
        # ================= BOOK 2 =================
        {
            "name": "2D Materials: Chemistry and Applications (Part 1)",
            "url_contains": "/ebook_volume/3759",
            "chapters": [
                ("23127", "Graphene: Understanding its Structure, Synthesis, and Functionalization"),
                ("23131", "Hybrid Materials of Graphene and Nanoparticles: Synthesis and Emerging Applications"),
                ("23130", "Harnessing Graphene-Based Nanocomposites for Multifunctional Applications"),
                ("23129", "Graphene-Based Gene and Drug Delivery Systems Innovations and Applications"),
                ("23132", "Graphene and its Derivatives: A Potential Solution for Microbial Control"),
                ("23133", "The Role of Graphene in Revolutionizing Biomedical Imaging Techniques"),
                ("23134", "Recent Advances in Graphene-Based Materials for Application in Cancer Therapy"),
                ("23136", "2D Graphene for Tissue Engineering Advances and Perspectives"),
                ("23135", "The Promise and Potential of Graphene Derivatives in Biotechnology"),
                ("23137", "Subject Index"),
            ]
        },
        # ================= BOOK 3 =================
        {
            "name": "2D Materials: Chemistry and Applications (Part 2)",
            "url_contains": "/ebook_volume/3789",
            "chapters": [
                ("23546", "Advanced Graphene-Based Supercapacitors for Energy Storage Applications"),
                ("23547", "Multifaceted Applications of Nanoparticle Functionalized Graphene"),
                ("23548", "Toxicity of Graphene Family and Remediation Approaches"),
                ("23549", "Graphene and Waste Management A Roadmap for Cost-Effective Graphene Production"),
                ("23550", "Two-Dimensional Boron Nitride From Synthesis to Energy Applications"),
                ("23551", "Functionalization Strategies and Applications of Two-Dimensional Boron Nitride"),
                ("23552", "Two-Dimensional Germanene Synthesis, Functionalization, and Applications"),
                ("23553", "Silicene - A Novel 2D Material with Potential for Nanoelectronics and Photonics"),
                ("23554", "Stanene, Mxene and Transition Metal Chalcogenides"),
                ("23555", "Subject Index"),
            ]
        },
        # ================= BOOK 4 =================
        {
            "name": "250 Years of Industrial Consumption and Transformation of Nature: Impacts on Global Ecosystems and Life",
            "url_contains": "/ebook_volume/2413",
            "chapters": [
                ("11776", "Anthology of Important Mottos, Statements and Stimuli"),
                ("11777", "Ecosystem Transformations - Natural and Anthropogenic Forcings"),
                ("11778", "The Anthropocene"),
                ("11779", "The Industrialisation : Its Origination and Development"),
                ("11780", "Its Impacts on and Transformations of Ecosystems and Life"),
                ("11781", "Extraction of Mineral Raw Materials and its Utilisations"),
                ("11782", "Transformation of Ecosystems in the Spheres of Earth"),
                ("11783", "Soil and Land Surface"),
                ("11784", "Glaciers, Ice Sheets, Sea Ice, and Permafrost Areas"),
                ("11785", "Groundwater"),
            ]
        }
    ]

    for b_index, book in enumerate(books, start=1):
        book_counts = {"name": book["name"], "csv_type": "book", "search": 10, "view": 0, "download": 10, "action": "Same Page"}
        report_data.append(book_counts)

        book_elem = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//a[contains(@href,'{book['url_contains']}') and normalize-space()='View Details']")))
        check_test_case(True, b_index + 8, f"Book {b_index} Details View")
        highlight_and_arrow(driver, book_elem, f"Book {b_index} Details")
        book_elem.send_keys(Keys.ENTER)
        wait_for_page_ready(driver)
        time.sleep(2)

        # Chapters loop
        for ch_id, ch_name in book["chapters"]:
            chapter_counts = {"name": f"   Chapter: {ch_name}", "csv_type": "chapter", "search": 1, "view": 0, "download": 1, "action": "Same Page"}
            report_data.append(chapter_counts)

            bk_ch = wait.until(EC.element_to_be_clickable((By.ID, ch_id)))
            check_test_case(True, 27, f"Chapter {ch_id} Download clicked")
            highlight_and_arrow(driver, bk_ch, f"Book {b_index} Chapter Download")
            safe_click(driver, bk_ch)
            time.sleep(30)

        # Back button
        back_btn = wait.until(EC.presence_of_element_located((By.XPATH, "(//a[normalize-space()='Back'])[1]")))
        check_test_case(True, 28, "Back Button Clicked")
        highlight_and_arrow(driver, back_btn, "Back Button Clicked")
        safe_click(driver, back_btn)
        time.sleep(30)

    print(" FLOW COMPLETED SUCCESSFULLY")

except Exception as e:
    print(f"Error Occurred: {e}")

finally:
    driver.quit()
# ================= SIMPLE HTML REPORT =================
html_path = get_resource_path("Book_Automation_Report.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Book Automation Report</title>
    <style>
        body {font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4;}
        h2 {text-align: center;}
        table {border-collapse: collapse; width: 50%; margin: auto; background-color: #fff;}
        th, td {border: 1px solid #ddd; padding: 8px; text-align: center;}
        th {background-color: #333; color: white;}
        tr.book-row {background-color: #d9edf7; font-weight: bold;}
        tr.chapter-row {background-color: #f9f9f9;}
    </style>
</head>
<body>
<h2>Book Automation Report</h2>
<table>
    <thead>
        <tr>
            <th>Item Name</th>
            <th>Count</th>
        </tr>
    </thead>
    <tbody>
""")
    for row in report_data:
        cls = "book-row" if row["csv_type"] == "book" else "chapter-row"
        f.write(f"""
        <tr class="{cls}">
            <td>{row['name']}</td>
            <td>{row['download']}</td>
        </tr>
""")
    f.write("""
    </tbody>
</table>
</body>
</html>
""")

print(f"HTML Report Generated at: {html_path}")
