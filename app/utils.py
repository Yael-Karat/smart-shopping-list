import requests
from bs4 import BeautifulSoup


def search_recipes(ingredients):
    # דוגמה עם אתר מתכונים פופולרי (כמו ynet או allrecipes)
    query = "+".join(ingredients)
    url = f"https://www.allrecipes.com/search/results/?wt={query}"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    recipes = []
    for card in soup.select(".card__detailsContainer"):
        title = card.select_one(".card__title")
        link = card.parent.get("href")
        if title and link:
            recipes.append({"title": title.get_text(strip=True), "link": link})
    return recipes[:5]  # רק 5 ראשונים
