import requests
from typing import List, Dict, Any, Optional

API_URL = "https://graphql.anilist.co"


def fetch_trending_anime(page: int) -> List[Dict[str, Any]]:
    query = f"""
    query {{
        Page(page: {page}, perPage: 12) {{
            media(sort: TRENDING_DESC, type: ANIME) {{
                id
                title {{
                    romaji
                    english
                }}
                trending
                averageScore
                coverImage {{
                    large
                }}
            }}
        }}
    }}
    """
    response = requests.post(API_URL, json={"query": query})
    if response.status_code != 200:
        print(f"HTTP Error: {response.status_code}")
        print(response.text)
        return []

    data = response.json()
    if "errors" in data:
        print(f"GraphQL Errors: {data['errors']}")
        return []

    animes = []
    for anime in data["data"]["Page"]["media"]:
        rating = (
            anime.get("averageScore", 0) // 20
        )  # Convert averageScore to stars (1-5)
        anime_info = {
            "judul": anime["title"]["romaji"],
            "rating": rating,
            "gambar": anime["coverImage"]["large"],
            "id": anime["id"],
        }
        animes.append(anime_info)

    return animes


def anime_info(id: int) -> Dict[str, Optional[Any]]:
    query = """
    query ($id: Int) {
        Media(id: $id) {
            title {
                romaji
                english
            }
            description
            trailer {
                id
                site
                thumbnail
            }
            coverImage {
                large
            }
            bannerImage
            episodes
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
            season
            seasonYear
            studios {
                nodes {
                    name
                }
            }
            duration
            genres
            averageScore
        }
    }
    """
    variables = {"id": id}
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    response = requests.post(
        API_URL, json={"query": query, "variables": variables}, headers=headers
    )

    if response.status_code != 200:
        print(f"HTTP Error: {response.status_code}")
        print(response.text)
        return {}

    data = response.json()
    if "errors" in data:
        print(f"GraphQL Errors: {data['errors']}")
        return {}

    media = data.get("data", {}).get("Media")
    if not media:
        print(f"No data found for anime with ID: {id}")
        return {}

    anime_details = {
        "title": media["title"]["romaji"],
        "description": media.get("description"),
        "coverImage": media["coverImage"]["large"],
        "bannerImage": media.get("bannerImage"),
        "trailer": media.get("trailer"),
        "episodes": media.get("episodes"),
        "startDate": (
            f"{media['startDate']['year']}-{media['startDate']['month']}-{media['startDate']['day']}"
            if media.get("startDate")
            else None
        ),
        "endDate": (
            f"{media['endDate']['year']}-{media['endDate']['month']}-{media['endDate']['day']}"
            if media.get("endDate")
            else None
        ),
        "season": (
            f"{media.get('season')} {media.get('seasonYear')}"
            if media.get("season") and media.get("seasonYear")
            else None
        ),
        "studio": (
            media["studios"]["nodes"][0]["name"]
            if media.get("studios", {}).get("nodes")
            else None
        ),
        "duration": media.get("duration"),
        "genres": media.get("genres"),
        "score": media.get("averageScore"),
    }
    return anime_details


if __name__ == "__main__":
    trending_animes = fetch_trending_anime()
    for anime in trending_animes:
        print(anime)

    anime = anime_info(152137)
    print(anime)
