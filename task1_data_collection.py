import requests
import time
import json
import os
from datetime import datetime

# Base URL
BASE_URL = "https://hacker-news.firebaseio.com/v0"
HEADERS = {"User-Agent":"TrendPulse/1.0"}

# Created a dictionary with all 5 categories as keys and matching keywords as list of values
# This dictionary is later used for assigning the category of each story based on the keywords that are present in the title of the story
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# A constant variable to ensure each category will have atmost 25 stories only
CATEGORY_MAX = 25

# Python function that fetches the top stories
def fetch_ids_of_top_stories():
    print("Extracting the data from the given API..........")

    try:
       url = f"{BASE_URL}/topstories.json"
       response = requests.get(url, headers=HEADERS)
       response.raise_for_status()
       return response.json()[:500]
    # If any run-time error(Exception more formally) arises, then it would be gracefully handled by the except block
    # then this block returns whatever we managed to fetch
    except:
        return []
    

# A python function that retrieves the details of each story based on the story ID
def fetch_each_story(story_id):
    
    # All the details of stories are stored in this path. Iterating through the IDs of each story, fetching the details of each story.
    url = f"{BASE_URL}/item/{story_id}.json"

    try:
        # For each iteration, only the details of one story is fetched, and then immediately returned to the invoker
        response = requests.get(url, headers=HEADERS)

        # After making a request to the given API/URL checks if it failed using raise_for_status()
        # If failed, then jumps to except block to handle it gracefully
        # Else parse JSON
        response.raise_for_status()
        return response.json()
    
    # If at all no story details are present with the given ID, then nothing will be returned
    except Exception as e:
        print(f"Error fetching story with ID {story_id}: {e}")
        return None
    

# A python function to categorize each story
def categorization(title): 

    # Converting the title of the story to lower case    
    title = title.lower()
    if not title:
        return []

    matched = []

    # Iterating through the keys, values of list in the CATEGORIES dictionary
    for category, keywords in CATEGORIES.items():

        for keyword in keywords:
            if keyword in title:
                matched.append(category)
        # If at all any value matches with the given title, then the story is categorized under {category}
                break
    
    # If the title doesn't match any keyword, then Nothing is returned, and it is categorized under nothing
    return matched

def collect_stories(story_ids):
    # A dictionary with all categories as keys with all the values initialized to 0 to keep track of the number of stories per category
    category_counts = {cat : [] for cat in CATEGORIES.keys()}

    print("Fetching individual story details")
    fetched_stories = []

    for story_id in story_ids:
        story = fetch_each_story(story_id)
        if story and story.get("type") == "story" and story.get("title"):
            fetched_stories.append(story)

    print(f"Fetched {len(fetched_stories)} valid stories.")

    for category in CATEGORIES.keys():

    # Iterating through the story_ids one by one
        for story in fetched_stories:
            
            if len(category_counts[category]) >= CATEGORY_MAX:
                break

            matched_categories = categorization(story.get("title"))

            if category in matched_categories:
                category_counts[category].append({
                    "post_id": story.get("id"),
                    "title": story.get("title"),
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", ""),
                    "collected_at": datetime.now().isoformat(),
                })
        print(f"{category}: {len(category_counts[category])} stories collected.")
        time.sleep(2)

    all_stories = [story for stories in category_counts.values() for story in stories]
    return all_stories


def save_stories(stories):
    if not os.path.exists("data"):
        os.makedirs("data")

    filename = f"data/hacker_news_stories_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(stories, f, indent=4)
    return filename


# Main function. Handles everything
def main():

    # Calls the function 'fetch_ids_of_top_stories' and the result (Stories IDs) are stored in the variable story_ids
    story_ids = fetch_ids_of_top_stories()
    if not story_ids:
        print("No story IDs fetched. Exiting.")
        return
    
    stories = collect_stories(story_ids)
        
    filename = save_stories(stories)

    print(f"Collected {len(stories)} stories. Saved to the file {filename}")

# The main function is called to execute the entire process
if __name__ == "__main__":
    main()