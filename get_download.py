import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

API_LINK = "https://otakudesu-unofficial-api.vercel.app/v1"

# Gunakan requests.Session untuk mengurangi overhead dari pembuatan koneksi
session = requests.Session()


def request_json(url: str):
    try:
        response = session.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return {}


def cari_anime(query: str):
    data = request_json(f"{API_LINK}/search/{query}")
    if "Error" in data:
        print(f"Errors: {data['errors']}")
        return []

    return [
        {"Judul": anime["title"], "Slug": anime["slug"]}
        for anime in data.get("data", [])
    ]


def get_episode(slug: str):
    data = request_json(f"{API_LINK}/anime/{slug}")
    if "Error" in data:
        print(f"Errors: {data['errors']}")
        return []

    return [
        {"Slug": episode["slug"], "Episode": episode["episode"]}
        for episode in data.get("data", {}).get("episode_lists", [])
    ]


def get_download(slug: str):
    data = request_json(f"{API_LINK}/episode/{slug}")
    if "Error" in data:
        print(f"Errors: {data['errors']}")
        return []

    episode_info = data.get("data", {})
    episode_description = episode_info.get("episode", "No description available")

    download_links = []
    for format_type in ["mp4", "mkv"]:
        for resolution in episode_info.get("download_urls", {}).get(format_type, []):
            for url in resolution["urls"]:
                download_links.append(
                    {
                        "Episode": episode_description,
                        "Format": format_type,
                        "Resolution": resolution["resolution"],
                        "Provider": url["provider"],
                        "URL": url["url"],
                    }
                )

    return download_links


def main():
    episodes = get_episode("shikanoko-nokotan-sub-indo")
    slugs = [episode["Slug"] for episode in episodes]

    urls = []
    with ThreadPoolExecutor() as executor:
        future_to_slug = {executor.submit(get_download, slug): slug for slug in slugs}
        for future in as_completed(future_to_slug):
            data = future.result()
            for item in data:
                urls.append(item)

    print(urls)


# Example usage
if __name__ == "__main__":
    main()
