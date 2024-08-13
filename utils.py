import requests
from datetime import datetime


API_URL = "https://graphql.anilist.co"


def fetch_trending_anime(page: int, limit: int = 12) -> str:
    query = f"""
    query {{
        Page(page: {page}, perPage: {limit}) {{
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
    for anime in data.get("data", {}).get("Page", {}).get("media", []):
        title = anime.get("title", {}).get("romaji", "Unknown Title")
        cover_image = anime.get("coverImage", {}).get("large", "No Image Available")
        average_score = anime.get("averageScore")
        rating = (
            (average_score // 20) if average_score is not None else None
        )  # Convert averageScore to stars (0-5)

        anime_info = {
            "judul": title,
            "rating": rating,
            "gambar": cover_image,
            "id": anime.get("id", "Unknown ID"),
        }
        animes.append(anime_info)

    return animes


def anime_info(id: int) -> str:
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


def get_current_season(date=None):
    if date is None:
        date = datetime.now()
    month = date.month

    if 1 <= month <= 3:
        return "WINTER"
    elif 4 <= month <= 6:
        return "SPRING"
    elif 7 <= month <= 9:
        return "SUMMER"
    elif 10 <= month <= 12:
        return "FALL"
    else:
        return "Unknown"


def fetch_anime_season(
    page: int = 1,
    limit: int = 12,
    seasonYear: int = datetime.now().year,
    season: str = get_current_season(),
) -> str:
    query = f"""
    query {{
        Page(page: {page}, perPage: {limit}) {{
            media(sort: TRENDING_DESC, type: ANIME, status: RELEASING, season: {season}, seasonYear: {seasonYear},  ) {{
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
    for anime in data.get("data", {}).get("Page", {}).get("media", []):
        title = anime.get("title", {}).get("romaji", "Unknown Title")
        cover_image = anime.get("coverImage", {}).get("large", "No Image Available")
        average_score = anime.get("averageScore")
        rating = (
            (average_score // 20) if average_score is not None else None
        )  # Convert averageScore to stars (0-5)

        anime_info = {
            "judul": title,
            "rating": rating,
            "gambar": cover_image,
            "id": anime.get("id", "Unknown ID"),
        }
        animes.append(anime_info)

    return animes


def fetch_movie(
    page: int = 1,
    limit: int = 12,
    seasonYear: int = datetime.now().year,
    season: str = get_current_season(),
) -> str:
    query = f"""
    query {{
        Page(page: {page}, perPage: {limit}) {{
            media(sort: TRENDING_DESC, type: ANIME, season: {season}, seasonYear: {seasonYear}, format: MOVIE ) {{
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
    for anime in data.get("data", {}).get("Page", {}).get("media", []):
        title = anime.get("title", {}).get("romaji", "Unknown Title")
        cover_image = anime.get("coverImage", {}).get("large", "No Image Available")
        average_score = anime.get("averageScore")
        rating = (
            (average_score // 20) if average_score is not None else None
        )  # Convert averageScore to stars (0-5)

        anime_info = {
            "judul": title,
            "rating": rating,
            "gambar": cover_image,
            "id": anime.get("id", "Unknown ID"),
        }
        animes.append(anime_info)

    return animes


def search_anime(title: str, page: int = 1, limit: int = 12) -> str:
    query = f"""
    query {{
        Page(page: {page}, perPage: {limit}) {{
            media(search: "{title}", sort: TRENDING_DESC, type: ANIME) {{
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
    for anime in data.get("data", {}).get("Page", {}).get("media", []):
        title = anime.get("title", {}).get("romaji", "Unknown Title")
        cover_image = anime.get("coverImage", {}).get("large", "No Image Available")
        average_score = anime.get("averageScore")
        rating = (
            (average_score // 20) if average_score is not None else None
        )  # Convert averageScore to stars (0-5)

        anime_info = {
            "judul": title,
            "rating": rating,
            "gambar": cover_image,
            "id": anime.get("id", "Unknown ID"),
        }
        animes.append(anime_info)

    return animes


if __name__ == "__main__":
    data = search_anime("one")
    print(data)
