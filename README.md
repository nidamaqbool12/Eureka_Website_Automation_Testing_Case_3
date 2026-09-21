Eureka_Website_Automation_Testing_Case_3

Overview

This repository contains the Case_3 automation script. It is developed using Python and Selenium to automate Access_Typed_Open book and book chapter access and download actions on the Eureka website. The script was developed in PyCharm IDE.

Test Case Summary:

This positive test case verifies that a user can successfully access and download assigned Access_Typed_Open books or Access_Typed_Open book chapters from the Eureka Website. The user logs in with valid credentials and, after successful authentication, navigates from the homepage by hovering over the Publications menu and selecting By Open Access Books under the Books section, then selects a book from the list. The user can view available download options, download specific chapters, download complete books, or navigate to a chapter detail page and download the chapter. The download process completes successfully.

Steps in brief:

The user logs in with valid credentials.

After successful authentication, the user navigates to the Publications menu.

The user selects By Open Access Books under the Books section.

The system displays a list of available books.

The user selects a book using the View Details button.

The system redirects the user to the Book Details page.

The user views available download options.

The user downloads individual chapter PDFs.

The user downloads complete book PDFs.

The user can navigate to a chapter detail page and download the chapter.

The user can download a chapter directly from the same page where applicable.

The system verifies that the selected books and chapters are downloaded successfully.

Books Overview for Test Case

First Book Download (View Download Options Only) (4D Fetal Echocardiography)

Second Book Download (Complete Book PDF) (Atmospheric Flow Fields: Theory, Numerical Methods And Software Tools)

Third Book Download (Single Chapter PDF) (4D Fetal Echocardiography)

Fourth Book Download (Detail Page Chapter + Complete Book) (An Ecological Perspective on Health Promotion Systems, Settings & Social Processes)

Fifth Book Download (1 Same Page Chapter + 1 Detail Page Chapter + Complete Book) (Consanguinity - Its Impact, Consequences and Management)

Folder Structure

Eureka_Website_Automation_Testing_Case_3/
│
├── Case#3/
│   │
│   ├── case_3/
│   │   ├── .env                    # Environment variables file (credentials & URL)
│   │   └── Case_3.exe             # Executable file generated from .py script
│   │
│   ├── build/
│   │   └── Case_3/                 # PyInstaller auto-generated files
│   │
│   ├── Case_3.py                   # Main Python automation script
│   ├── Case_3.spec                 # PyInstaller spec file
│   ├── Case_3.xlsx                 # Excel file containing test case details
│   └── README.md

Test Case Details (Excel)

Case_3.xlsx

Contains:

Test Case Description

Steps of Execution

Pre-conditions

Post-conditions

Expected Output

Example Heading:

1 Preconditions:

User must be registered by the admin, have valid login credentials, have access to assigned books, and be logged in successfully to the Eureka Website.

2 Steps of Execution:

Login → Publications → By Open Access Books → Select Book → View Details → View/Download Chapter → Download Complete Book where applicable.

3 Expected Output:

The available Open Access books and their download options are displayed correctly. The user can successfully download individual chapter PDFs and complete book PDFs.

.env File

Purpose:

To securely store login credentials and the base URL.

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
