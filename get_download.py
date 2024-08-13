import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

API_LINK = "https://otakudesu-unofficial-api.vercel.app/v1"

# Gunakan requests.Session untuk mengurangi overhead dari pembuatan koneksi


def ambil_dua_kata(teks):
    kata = teks.split()
    return " ".join(kata[:2])


def ambil_tiga_kata(teks):
    kata = teks.split()
    return " ".join(kata[:3])


def request_json(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return {}


def cari_anime(query: str):
    query_tiga_kata = ambil_tiga_kata(query).replace(" ", "%20")
    print(f"Searching with three words: {query_tiga_kata}")
    data = request_json(f"{API_LINK}/search/{query_tiga_kata}")

    # Jika hasil kosong, coba dengan dua kata
    if not data.get("data"):
        query_dua_kata = ambil_dua_kata(query).replace(" ", "%20")
        print(f"No results found, searching with two words: {query_dua_kata}")
        data = request_json(f"{API_LINK}/search/{query_dua_kata}")

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


def get_batch_downloads(slugs: str):
    pass


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
