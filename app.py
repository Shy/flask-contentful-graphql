from flask import Flask, render_template
import requests
import json
import os

from dotenv import load_dotenv

load_dotenv()


SPACE_ID = os.environ.get("SPACE_ID")
DELIVERY_API_KEY = os.environ.get("DELIVERY_API_KEY")
DEBUG_STATUS = os.environ.get("DEBUG_STATUS")
GRAPHQL_ENDPOINT = f"https://graphql.contentful.com/content/v1/spaces/{SPACE_ID}/"

query = """{
  superheroCollection {
    items {
      name
      role
      image {
        url
        description
      }
    }
  }
}"""
headers = {
    "Content-Type": "application/json", "Authorization": f"Bearer {DELIVERY_API_KEY}",
}

app = Flask(__name__)


def run_query(
    query,
):  # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post(GRAPHQL_ENDPOINT, json={"query": query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception(
            f"Query failed to run by returning code of {request.status_code}. {query}"
        )


@app.route("/")
def home_page():
    result = run_query(query)
    print(result["data"]["superheroCollection"])
    return render_template(
        "index.html", superheroCollection=result["data"]["superheroCollection"]["items"]
    )


if __name__ == "__main__":
    app.debug = DEBUG_STATUS
    app.run()
