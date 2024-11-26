## Getting Started & Installation:

- ### Prerequisite:

  - Download [Python3.x](https://www.python.org/downloads/).

- ### Installation:

  E.g If you downloaded `Python 3.8.7` above, then

  **Steps to setup virtual environment**

  - Create a virtual environment:

    `python3.8 -m venv test_env`

  - Activate the virtual environment:

    `source test_env/bin/activate`

  - Build the virtual environment:(must be present in [project root directory](https://github.com/TeamBenign/WolfTrack6.0))

    `pip install -r requirements.txt`

- ### Run Instructions

  **To run/test the site locally:**

  - Clone [WolfTrack github repo](https://github.com/TeamBenign/WolfTrack6.0).

  - Navigate to [project directory](https://github.com/TeamBenign/WolfTrack6.0).

  - Run `python main.py` or `python3 main.py` <br> <br>
    If there is a certificate error coming up for nltk stopwords download: <br>

    - search for "Install Certificates.command" in finder and open it. Its a script that will install required Certificates. <br>
    - Run the above command again.

  - Site will be hosted at:
    `http://127.0.0.1:5000/`

- ### Adzuna API Setup
**Create an Account:**

  Go to the Adzuna Developer portal developer.adzuna.com.
  Sign up for an account to access the API. You might need to provide some basic details about your application, such as the name, purpose, and contact information.

**Get API Credentials:**

  Log in to your Adzuna Developer account.
  Find the section to create an API application.
  Create a new application to generate API credentials (usually API keys or tokens). These credentials are necessary to authenticate your requests to the Adzuna API.

**Change URL:**

  Update the adzuna_url in your app.py - using the newly obtained credentials. This updated URL should reflect the API endpoint along with your authentication credentials for accessing the Adzuna API.

- ### Google Gemini API Setup

**Create an Account:**  
Sign up for a [Google Cloud account](https://cloud.google.com/) if you haven’t already.

**Create a Project:**  
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one from the project dropdown.

**Enable the Google Gemini API**  

1. In the Cloud Console, go to **APIs & Services > Library**.
2. Search for **Google Gemini API**.
3. Click on the API and select **Enable**.

**Set Up API Authentication**  

**Create API Credentials:**
1. Go to **APIs & Services > Credentials** in the Google Cloud Console.
2. Click **Create Credentials** and select either **API Key** or **OAuth 2.0 Client ID** (OAuth is recommended for better security).

**Set Up OAuth Consent Screen (for OAuth 2.0):**
1. Configure the consent screen with your app details, including name and contact info.
2. Set up an **OAuth 2.0 Client ID** with your application type (e.g., Web Application).
3. Save the **Client ID** and **Client Secret** for later use.
