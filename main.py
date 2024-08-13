from fasthtml.common import *
from fasthtml.components import NotStr
from utils import (
    fetch_trending_anime,
    anime_info,
    fetch_anime_season,
    fetch_movie,
    get_current_season,
    search_anime,
    ambil_tiga_kata,
)
from components import *
import datetime
from collections import defaultdict
from get_download import cari_anime, get_episode, get_download

COMMON_NAVBAR_LINKS = {
    "Home": "/",
    "Tentang": "/about",
    "Kontak": "/contact",
    "Trending": "/trending/1",
}

# Inisialisasi aplikasi dengan header dan pengaturan lainnya
app, rt = fast_app(
    hdrs=(
        Link(href="/static/styles/styles.css", rel="stylesheet"),
        Link(href="/static/styles/tailwind.css", rel="stylesheet"),
        Script(src="https://cdn.jsdelivr.net/npm/theme-change@2.0.2/index.js"),
        Link(
            rel="apple-touch-icon",
            sizes="180x180",
            href="/static/images/apple-touch-icon.png",
        ),
        Link(
            rel="icon",
            type="image/png",
            sizes="32x32",
            href="/static/images/favicon-32x32.png",
        ),
        Link(
            rel="icon",
            type="image/png",
            sizes="16x16",
            href="/static/images/favicon-16x16.png",
        ),
        Link(rel="manifest", href="/static/images/site.webmanifest"),
        # hanya untuk development
        # Script(src="https://cdn.tailwindcss.com"),
        # Link(
        #     href="https://cdn.jsdelivr.net/npm/daisyui@4.12.10/dist/full.min.css",
        #     type="text/css",
        #     rel="stylesheet",
        # ),
    ),
    pico=False,
)


@app.get("/")
def home():
    navbar_links = COMMON_NAVBAR_LINKS
    trending_animes = fetch_trending_anime(1)
    this_season = fetch_anime_season(1, 12)
    this_season_movies = fetch_movie(1, 12)
    return (
        Title("Anime"),
        Body(
            create_navbar(navbar_links),
            warning(),
            kumpulan_kartu("Trending Anime", trending_animes, "/trending/1"),
            pemisah(),
            kumpulan_kartu("This Season", this_season, "/this-season/1"),
            pemisah(),
            kumpulan_kartu(
                "This Season Movies", this_season_movies, "/season-movies/1"
            ),
            pemisah(),
            footer(),
        ),
    )


@app.get("/anime/{id}")
def anime_page(id: int):
    navbar_links = COMMON_NAVBAR_LINKS
    anime_data = anime_info(id)
    return (
        Title(f"Anime | {anime_data['title']}"),
        Body(
            create_navbar(navbar_links),
            warning(),
            Div(
                Img(
                    src=anime_data["bannerImage"],
                    alt=f"banner of {anime_data['title']}",
                    cls="w-screen object-cover",
                ),
                pemisah(),
                Div(
                    Div(
                        Img(
                            src=anime_data["coverImage"],
                            alt=f"Cover of {anime_data['title']}",
                        )
                    ),
                    Div(
                        H1(anime_data["title"]),
                        P(f"Rating: {anime_data['score']}/10"),
                        P(f"Episodes: {anime_data['episodes']}"),
                        P(f"Season: {anime_data['season']}"),
                        P(f"Genres: {', '.join(anime_data['genres'])}"),
                        P(f"Duration: {anime_data['duration']}"),
                        P(f"Rating: {anime_data['score']}/100"),
                        (
                            P(f"Start Date: {anime_data['startDate']}")
                            if anime_data["startDate"]
                            else None
                        ),
                        (
                            P(f"End Date: {anime_data['endDate']}")
                            if anime_data["endDate"]
                            else None
                        ),
                        (
                            P(f"Studio: {anime_data['studio']}")
                            if anime_data["studio"]
                            else None
                        ),
                    ),
                    cls="flex flex-row items-center gap-4",
                ),
                pemisah(),
                Div(
                    P(NotStr(anime_data["description"])),
                ),
                pemisah(),
                search_section(
                    ambil_tiga_kata(
                        anime_data["title"].replace("[", "").replace("]", "")
                    )  # Untuk menghilangkan tanda kurung, nanti ubah agar lebih rapi
                ),
                pemisah(),
            ),
            footer(),
        ),
    )


def search_section(query: str):
    list_pencarian = cari_anime(query)
    return (
        Div(
            H2("Download", cls="mb-2 text-2xl font-bold"),
            *[
                Div(
                    Button(
                        f"{link['Judul']}",
                        hx_get=f"/get-episodes/{link['Slug']}",
                        hx_swap="outerHTML",
                        hx_target="#episodes-selection",
                        cls="btn btn-primary",
                    ),
                )
                for link in list_pencarian
            ],
            id="episodes-selection",
            cls="flex flex-wrap flex-col gap-4 mx-auto justify-center items-center",
        ),
    )


@app.get("/get-episodes/{slug}")
def get_episodes_page(slug: str):
    episodes = get_episode(slug)
    return (
        Div(
            H2("Episodes", cls="mb-2 text-2xl font-bold"),
            Div(
                *[
                    Div(
                        Button(
                            f"Episode {episode['Episode']}",
                            hx_get=f"/download/{episode['Slug']}",
                            hx_swap="outerHTML",
                            hx_target="#episodes-selection",
                            cls="btn btn-primary flex-1",
                        ),
                    )
                    for episode in episodes
                ],
                cls="flex flex-wrap flex-col gap-2 mx-auto justify-center items-center",
            ),
            id="episodes-selection",
            cls="flex flex-wrap flex-col gap-4 mx-auto justify-center items-center",
        ),
    )


@app.get("/about")
def about_page():
    navbar_links = COMMON_NAVBAR_LINKS
    return (
        Title("Anime | About"),
        Body(
            create_navbar(navbar_links),
            warning(),
            pemisah(),
            footer(),
        ),
    )


@app.get("/contact")
def contact_page():
    navbar_links = COMMON_NAVBAR_LINKS
    return (
        Title("Anime | About"),
        Body(
            create_navbar(navbar_links),
            warning(),
            pemisah(),
            footer(),
        ),
    )


@app.get("/download/{slug}")
def download_page(slug: str):
    downloads = get_download(slug)

    # Mengelompokkan unduhan berdasarkan provider
    grouped_downloads = defaultdict(list)
    for download in downloads:
        grouped_downloads[download["Provider"]].append(download)

    return Div(
        *[
            Div(
                H3(provider, cls="text-xl font-bold mb-2 text-center"),
                Div(
                    *[
                        A(
                            f"Download {download['Episode'].replace('Subtitle Indonesia', '')}, {download['Format']}, {download['Resolution']}",
                            href=f"{download['URL']}",
                            target="_blank",
                            rel="noopener noreferrer",
                            cls="btn btn-primary min-w-96 flex-1",
                        )
                        for download in provider_downloads
                    ],
                    cls="flex gap-4 flex-row flex-wrap",
                ),
                cls="mb-4",
            )
            for provider, provider_downloads in grouped_downloads.items()
        ],
        cls="m-4",
    )


@app.get("/trending")
def redirect_to_trending_page():
    return RedirectResponse(url="/trending/1")


@app.get("/trending/{page:int}")
def trending_page(page: int = 1):
    page = int(page)
    navbar_links = {
        "Home": "/",
        "About": "/about",
        "Contact": "/contact",
        "Trending": "/trending",
    }
    trending_animes = fetch_trending_anime(page, 36)
    has_next_page = len(trending_animes) == 36
    return (
        Title("Anime | Trending"),
        Body(
            create_navbar(navbar_links),
            warning(),
            kumpulan_kartu("Trending Anime", trending_animes, "/trending/1"),
            pemisah(),
            page_navigation(page, has_next_page, "trending"),
            footer(),
        ),
    )


@app.get("/this-season")
def redirect_to_trending_page():
    return RedirectResponse(url="/this-season/1")


@app.get("/this-season/{page:int}")
def this_season_page(page: int = 1):
    page = int(page)
    navbar_links = {
        "Home": "/",
        "About": "/about",
        "Contact": "/contact",
        "Trending": "/trending",
    }
    this_season = fetch_anime_season(page, 36)
    has_next_page = len(this_season) == 36
    return (
        Title(f"Anime | Season {get_current_season()}"),
        Body(
            create_navbar(navbar_links),
            warning(),
            kumpulan_kartu(
                f"Anime Season {get_current_season()} {datetime.datetime.now().year}",
                this_season,
                "/season-movies/1",
            ),
            pemisah(),
            page_navigation(page, has_next_page, "this-season"),
            footer(),
        ),
    )


@app.get("/season-movies")
def redirect_to_trending_page():
    return RedirectResponse(url="/season-movies/1")


@app.get("/season-movies/{page:int}")
def this_season_movies(page: int = 1):
    page = int(page)
    navbar_links = {
        "Home": "/",
        "About": "/about",
        "Contact": "/contact",
        "Trending": "/trending",
    }
    this_season = fetch_movie(page, 36)
    has_next_page = len(this_season) == 36

    return (
        Title(f"Anime | Movies Season {get_current_season()}"),
        Body(
            create_navbar(navbar_links),
            warning(),
            kumpulan_kartu(
                f"Movies Season {get_current_season()} {datetime.datetime.now().year}",
                this_season,
                "/season-movies/1",
            ),
            pemisah(),
            page_navigation(page, has_next_page, "season-movies"),
            footer(),
        ),
    )


@app.get("/search/{query:str}/{page:int}")
def search_page(query: str, page: int = 1):
    navbar_links = COMMON_NAVBAR_LINKS
    search_results = search_anime(query, page=page, limit=36)
    has_next_page = len(search_results) == 36
    return (
        Title(f"Anime | Search: {query}"),
        Body(
            create_navbar(navbar_links, query=query),
            warning(),
            kumpulan_kartu(
                f"Search Results for '{query}'", search_results, f"/search/{query}/1"
            ),
            pemisah(),
            page_navigation(
                page,
                has_next_page,
                f"search/{query}",
            ),
            footer(),
        ),
    )


@app.get("/search")
def search(query: str = Form(...)):
    return RedirectResponse(url=f"/search/{query}/1")


@app.exception_handler(HTTPException)
def handler_404(request: Request, exc: HTTPException):
    return HTMLResponse(
        f"<h1>{exc.status_code} - {exc.detail}</h1>", status_code=exc.status_code
    )


serve()
