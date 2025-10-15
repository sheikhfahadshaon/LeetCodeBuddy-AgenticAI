
import requests
import json

def fetch_problem_data(problem_slug):
    url = "https://leetcode.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "Referer": f"https://leetcode.com/problems/{problem_slug}/"
    }
    
    # GraphQL query for LeetCode problem details
    query = """
    query getQuestionDetail($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionId
        title
        titleSlug
        content
        difficulty
        likes
        dislikes
        topicTags {
          name
          slug
        }
      }
    }
    """

    variables = {"titleSlug": problem_slug}

    response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data["data"]["question"]
    else:
        raise Exception(f"Request failed with status code {response.status_code}")

if __name__ == "__main__":
    problem_slug = "two-sum"
    problem_data = fetch_problem_data(problem_slug)

    print("📘 Title:", problem_data["title"])
    print("🔥 Difficulty:", problem_data["difficulty"])
    print("❤️ Likes:", problem_data["likes"])
    print("💬 Description (HTML):")
    print(problem_data["content"][:300], "...")  # printing first 300 chars only
