import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import json

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

API_LINK = "https://otakudesu-unofficial-api.vercel.app/v1"


def cari_anime(query: str):
    response = requests.get(f"{API_LINK}/search/{query}")
    try:
        response.raise_for_status()
        data = response.json()
        if "Error" in data:
            logging.error(f"Error in API response: {data['errors']}")
            return []
        return [
            {"Judul": anime["title"], "Slug": anime["slug"]}
            for anime in data.get("data", [])
        ]
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching anime search results: {e}")
        return []
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding API response: {e}")
        return []


def get_episode(slug: str):
    response = requests.get(f"{API_LINK}/anime/{slug}")
    try:
        response.raise_for_status()
        data = response.json()
        if "Error" in data:
            logging.error(f"Error in API response: {data['errors']}")
            return []
        return [
            {"Slug": episode["slug"], "Episode": episode["episode"]}
            for episode in data.get("data", {}).get("episode_lists", [])
        ]
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching episodes for slug {slug}: {e}")
        return []
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding API response for slug {slug}: {e}")
        return []


def get_download(slug: str):
    response = requests.get(f"{API_LINK}/episode/{slug}")
    try:
        response.raise_for_status()
        data = response.json()
        if "Error" in data:
            logging.error(f"Error in API response: {data['errors']}")
            return []
        episode_info = data.get("data", {})
        episode_description = episode_info.get("episode", "No description available")
        return [
            {
                "Episode": episode_description,
                "Format": format_type,
                "Resolution": resolution["resolution"],
                "Provider": url["provider"],
                "URL": url["url"],
            }
            for format_type in ["mp4", "mkv"]
            for resolution in episode_info.get("download_urls", {}).get(format_type, [])
            for url in resolution["urls"]
        ]
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching download links for slug {slug}: {e}")
        return []
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding API response for slug {slug}: {e}")
        return []


def fetch_episode_data(slug: str):
    return get_download(slug)


def main():
    episode_slugs = [
        episode["Slug"] for episode in get_episode("shikanoko-nokotan-sub-indo")
    ]

    download_links = []
    with ThreadPoolExecutor() as executor:
        future_to_slug = {
            executor.submit(fetch_episode_data, slug): slug for slug in episode_slugs
        }
        for future in as_completed(future_to_slug):
            slug = future_to_slug[future]
            try:
                data = future.result()
                download_links.extend(data)
            except Exception as e:
                logging.error(f"Error fetching data for slug {slug}: {e}")

    logging.info(download_links)


if __name__ == "__main__":
    main()
