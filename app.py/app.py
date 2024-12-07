from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


def fetch_imdb_movie_news():
    url = "https://www.imdb.com/news/top/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        news_list = []
        articles = soup.find_all("div", class_="sc-ed7ef9a2-5 flwTbh")[:4]

        for article in articles:
            try:
                title_element = article.find("a", class_="ipc-link ipc-link--base sc-ed7ef9a2-3 eDjiRr")
                title = title_element.text.strip() if title_element else "No title found"

                description_element = article.find("div", class_="ipc-html-content-inner-div")
                description = description_element.text.strip() if description_element else "No description found"

                image_element = article.find("img", class_="ipc-image")
                image_url = image_element.get("src") if image_element else "No image found"

                news_item = {
                    "title": title,
                    "description": description,
                    "image": image_url
                }
                news_list.append(news_item)

            except Exception as e:
                print(f"Error processing article: {str(e)}")
                continue
        return news_list

    except Exception as e:
        print(f"Error fetching news: {str(e)}")
    return []


@app.route('/imdb_news', methods=['GET'])
def imdb_news():
    news = fetch_imdb_movie_news()
    return jsonify(news)


if __name__ == '__main__':
    app.run(debug=True)
