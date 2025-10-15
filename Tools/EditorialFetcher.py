import requests
from bs4 import BeautifulSoup

def fetch_editorial_text(problem_slug):
    """
    Fetches only the textual editorial for a LeetCode problem.
    Example: problem_slug = "two-sum"
    """
    graphql_url = "https://leetcode.com/graphql"
    query = """
    query getEditorial($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        title
        solution {
          content
        }
      }
    }
    """

    headers = {
        "Content-Type": "application/json",
        "Referer": f"https://leetcode.com/problems/{problem_slug}/",
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.post(
        graphql_url,
        json={"query": query, "variables": {"titleSlug": problem_slug}},
        headers=headers
    )

    if response.status_code != 200:
        print(f"❌ Failed to fetch editorial (status {response.status_code})")
        return None

    data = response.json()
    solution = data.get("data", {}).get("question", {}).get("solution", {})
    if not solution or not solution.get("content"):
        print("❌ No editorial found for this problem.")
        return None

    # Extract text only
    html_content = solution["content"]
    soup = BeautifulSoup(html_content, "html.parser")
    text_content = soup.get_text(separator="\n").strip()

    return {
        "title": data["data"]["question"]["title"],
        "text": text_content
    }

if __name__ == "__main__":
    slug = input("Enter LeetCode problem slug (e.g., two-sum): ").strip()
    result = fetch_editorial_text(slug)

    if result:
        print(f"\n📘 Editorial Title: {result['title']}")
        print("\n📝 Editorial Text:\n")
        print(result["text"])
