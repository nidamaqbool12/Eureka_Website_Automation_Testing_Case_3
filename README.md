Eureka_Website_Automation_Testing_Case_3

Overview

This repository contains the Case_3 automation script. It is developed using Python and Selenium to automate Access_Typed_Open book and book chapter access and download actions on the Eureka website. The script was developed in PyCharm IDE.

Test Case Summary:

This positive test case verifies that a user can successfully access and download assigned Access_Typed_Open books or Access_Typed_Open book chapters from the Eureka Website. The user logs in with valid credentials and, after successful authentication, navigates from the homepage by hovering over the Publications menu and selecting By Open Access Books under the Books section, then selects a book from the list. The user can view available download options, download specific chapters, download complete books, or navigate to a chapter detail page and download the chapter. The download process completes successfully.


Folder Structure

<img width="617" height="325" alt="image" src="https://github.com/user-attachments/assets/a9e42e65-0ed5-4f73-8a4c-c9e2a86cf644" />


.env File

Purpose:


Install dotenv library:

pip install python-dotenv

Python Code to Load .env File:

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv(".env")

# Variables
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
BASE_URL = os.getenv("BASE_URL")

.env File Content:

LOGIN CREDENTIALS

EMAIL=(Your Email)
PASSWORD=(Your Password)

SITE URL

BASE_URL=https://www.eurekaselect.com/

Creating Executable (.exe) File

Install PyInstaller:

pip install pyinstaller

Command to Create Executable:

pyinstaller --onefile --collect-all selenium Case_3.py
