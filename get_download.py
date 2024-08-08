API_LINK = "https://otakudesu-unofficial-api.vercel.app/v1"


def cari_anime(query: str):
    response = requests.get(f"{API_LINK}/search/{query}")
    if response.status_code != 200:
        print(f"HTTP Error: {response.status_code}")
        print(response.text)
        return []

    data = response.json()
    if "Error" in data:
        print(f"Errors: {data['errors']}")
        return []

    hasil = []
    for anime in data.get("data", []):
        judul = anime["title"]
        slug = anime["slug"]

        isian = {"Judul": judul, "Slug": slug}
        hasil.append(isian)

    return hasil  # Mengembalikan list hasil, bukan isian


def get_episode(slug: str):
    response = requests.get(f"{API_LINK}/anime/{slug}")
    if response.status_code != 200:
        print(f"HTTP Error: {response.status_code}")
        print(response.text)
        return []

    data = response.json()
    if "Error" in data:
        print(f"Errors: {data['errors']}")
        return []

    hasil = []
    for episode in data.get("data", []).get("episode_lists", []):
        slug = episode["slug"]
        eps = episode["episode"]

        isi = {"Slug": slug, "Episode": eps}
        hasil.append(isi)

    return hasil


import requests


def get_download(slug: str):
    response = requests.get(f"{API_LINK}/episode/{slug}")
    if response.status_code != 200:
        print(f"HTTP Error: {response.status_code}")
        print(response.text)
        return []

    data = response.json()
    if "Error" in data:
        print(f"Errors: {data['errors']}")
        return []

    episode_info = data.get("data", {})
    episode_description = episode_info.get("episode", "No description available")

    download_links = []
    for format_type in ["mp4", "mkv"]:
        for resolution in episode_info.get("download_urls", {}).get(format_type, []):
            res = resolution["resolution"]
            urls = resolution["urls"]
            for url in urls:
                provider = url["provider"]
                link = url["url"]
                download_links.append(
                    {
                        "Episode": episode_description,
                        "Format": format_type,
                        "Resolution": res,
                        "Provider": provider,
                        "URL": link,
                    }
                )

    return download_links


def main():
    episode = get_episode("shikanoko-nokotan-sub-indo")
    slugs = []
    for slug in episode:
        slug_ = slug["Slug"]
        slugs.append(slug_)
    for slug in slugs:
        data = get_download(slug)
        urls = []
        for item in data:
            provider = item["Provider"]
            link = item["URL"]
            resolution = item["Resolution"]
            format_type = item["Format"]
            eps = item["Episode"]

            isi = {
                "Episode": eps,
                "Provider": provider,
                "URL": link,
                "Resolution": resolution,
                "Format": format_type,
            }
            urls.append(isi)
        print(urls)

    # data = get_download("sknk-episode-3-sub-indo")
    # for item in data:
    #     provider = item["Provider"]
    #     link = item["URL"]
    #     resolution = item["Resolution"]
    #     format_type = item["Format"]
    #     eps = item["Episode"]
    #     print(f"{eps} - {provider} - {resolution} - {format_type} - {link}")


# Example usage
if __name__ == "__main__":
    main()
