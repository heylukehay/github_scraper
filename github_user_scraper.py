from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

base_url = "https://github.com"

def scrape_user(username):
    """
    Scrape GitHub user data.
    
    Args:
        username (str): GitHub username to scrape.
    
    Returns:
        dict: A dictionary containing user data.
    """
    # URL for the GitHub user profile
    html_url = f"{base_url}/{username}"
    # Send a GET request to the URL
    page = requests.get(html_url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Extract user data
    user_data = {
        "login": soup.find("meta", {"name": "octolytics-dimension-user_login"})["content"],
        "id": int(soup.find("meta", {"name": "octolytics-dimension-user_id"})["content"]),
        "avatar_url": soup.find("img", class_="avatar")["src"],
        "url": f"https://api.{base_url}/users/{username}",
        "html_url": html_url,
        "type": "User",
        "name": soup.find("span", class_="p-name").text.strip(),
        "company": soup.find("span", class_="p-org").text.strip() if soup.find("span", class_="p-org") else None,
        "blog": soup.find_next_sibling("a", class_="u-url").text.strip() if soup.find("a", class_="u-url") else "",
        "location": soup.find("span", class_="p-label").text.strip() if soup.find("span", class_="p-label") else None,
        "bio": soup.find("div", class_="p-note").text.strip(),
        "twitter_username": soup.find("a", href=f"https://twitter.com/{username}").text.strip() if soup.find("a", href=f"https://twitter.com/{username}") else None,
        "public_repos": int(soup.find("a", href=f"/{username}?tab=repositories").find("span", class_="Counter").text.strip()),
        "followers": parse_follow_count(html_url, extract_follow_string(soup, username, "followers"), "followers"),
        "following": parse_follow_count(html_url, extract_follow_string(soup, username, "following"), "following"),
    }

    return user_data

def parse_follow_count(url, follow_string, follow_type):
    """
    Parse the follower/following count from the GitHub user profile page.
    
    Args:
        url (str): URL of the GitHub user profile.
        follow_string (str): String representation of the follower/following count.
        follow_type (str): Type of follow count to extract ("followers" or "following").
    
    Returns:
        int: Follower count.
    """

    follows = convert_follow_string_to_number(follow_string)

    if follows < 1000:
        return follows
    
    # Shortcut for large follow counts
 
    # Calculate the number of pages to skip
    follows_per_page = 50

    # Accounting for github's followers/following element rounding up at 50
    follows -= 50
    follow_page = int(follows/follows_per_page) + 1  
    

    url = f"{url}?tab={follow_type}&page={follow_page}"

    # Send a GET request to the URL
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")   

    while True:
        next_element = soup.find("a", string=lambda text: "next" in text.strip().lower())

        follows_list = soup.findAll("div", class_="table-fixed")
        for follow in follows_list:
            follows += 1

        if next_element is None:
            break
            
        next_url = next_element["href"] 

        page = requests.get(next_url)
        soup = BeautifulSoup(page.content, "html.parser")
    
    return follows

def extract_follow_string(soup, username, follow_type):
    """
    Extract the follower/following count from the GitHub user profile page.
    
    Args:
        soup (BeautifulSoup): BeautifulSoup object of the GitHub user profile page.
        username (str): GitHub username to scrape.
        follow_type (str): Type of follow count to extract ("followers" or "following").
    
    Returns:
        str: Follower/following count as a string.
    """
    follow_element = soup.find("a", href=f"{base_url}/{username}?tab={follow_type}")
    if follow_element:
        return follow_element.text.replace(follow_type, "").replace("follower", "").strip()
    return None

def convert_follow_string_to_number(follow_string):
    """
    Convert a string representation of a follower/following count to an integer.
    
    Args:
        follow_string (str): String representation of the follower/following count.
    
    Returns:
        int: Follower/following count as an integer.
    """
    # Remove commas and convert to integer
    if "k" in follow_string:
        return int(float(follow_string.replace("k", "")) * 1000)
    elif "m" in follow_string:
        return int(float(follow_string.replace("m", "")) * 1000000)
    else:
        return int(follow_string)