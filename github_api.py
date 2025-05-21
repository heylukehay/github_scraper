from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
from github_user_scraper import scrape_user

# Initialize Flask app
app = Flask(__name__)
app.json.sort_keys = False

# Define a route to fetch GitHub user data
@app.route('/users/<username>', methods=['GET'])
def github_user(username):
    user_data = scrape_user(username)
    if user_data:
        return jsonify(user_data), 200
    else:
        return jsonify({"error": "User not found"}), 404

# Define a route to fetch GitHub user repositories
@app.route('/users/<username>/repos', methods=['GET'])
def github_user_repos(username):
    # Fetch user repositories from GitHub API
    response = requests.get(f"https://api.github.com/users/{username}/repos")
    if response.status_code == 200:
        repos_data = response.json()
        return jsonify(repos_data)
    else:
        return jsonify({"error": "User not found"}), 404
    
#URL = "https://github.com/octocat"    
#page = requests.get(URL)
#soup = BeautifulSoup(page.content, "html.parser")
#print(soup.prettify()) 
    
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
