# github_scraper
A project that scrapes a user's Github webpage in order to recreate the GitHub API. Only returns the fields that are publicly accessible through the Github webpage without authentication/login.

Made using Python and Flask

USAGE
-----

To install the required modules:
---
- Open the terminal
- Set up your virtual environment (if necessary)
- Run the following command: pip install -r requirements.txt
---

To use the program:
---
- Open the terminal
- Run the following command: python github_api.py or python3 github_api.py (depending on which version of python you have installed)
- Open your internet browser and navigate to localhost:5000/users/{USERNAME} to get the information about the user, or localhost:5000/users/{USERNAME}/repos to get the information about the user's repositories.
---

To close the program:
---
- Open the terminal in which the program is running
- Press Control + C to close the server
---
