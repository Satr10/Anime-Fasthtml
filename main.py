from fasthtml.common import *
from fasthtml.components import NotStr
from utils import fetch_trending_anime, anime_info
from components import *

# Inisialisasi aplikasi dengan header dan pengaturan lainnya
app, rt = fast_app(
    hdrs=(
        NotStr("<title>Anime</title>"),
        Link(href="/static/styles/tailwind.css", rel="stylesheet"),
        Script(src="https://cdn.jsdelivr.net/npm/theme-change@2.0.2/index.js"),
    ),
    pico=False,
    live=True,
)


@app.get("/")
def home():
    navbar_links = {
        "Home": "/",
        "About": "/about",
        "Contact": "/contact",
        "Trending": "/trending",
    }
    trending_animes = fetch_trending_anime(1, 12)
    return (
        Title("Anime"),
        Body(
            create_navbar(navbar_links),
            warning(),
            kumpulan_kartu("Trending Anime", trending_animes),
            pemisah(),
            footer(),
        ),
    )


@app.get("/anime/{id}")
def anime_page(id: int):
    navbar_links = {
        "Home": "/",
        "About": "/about",
        "Contact": "/contact",
        "Trending": "/trending",
    }
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
                ),
            ),
            footer(),
        ),
    )


@app.get("/about")
def about_page():
    pass


@app.get("/contact")
def contact_page():
    pass


@app.get("/trending")
def redirect_to_trending_page():
    return RedirectResponse(url="/trending/1")


@app.get("/trending/{page:int}")
def trending_page(page: int = 1, limit: int = 36):
    page = int(page)
    navbar_links = {
        "Home": "/",
        "About": "/about",
        "Contact": "/contact",
        "Trending": "/trending",
    }
    trending_animes = fetch_trending_anime(page)
    return (
        Title("Anime | Trending"),
        Body(
            create_navbar(navbar_links),
            warning(),
            kumpulan_kartu("Trending Anime", trending_animes),
            pemisah(),
            page_navigation(page, 9999),
            footer(),
        ),
    )


@app.exception_handler(HTTPException)
def handler_404(request: Request, exc: HTTPException):
    return HTMLResponse(
        f"<h1>{exc.status_code} - {exc.detail}</h1>", status_code=exc.status_code
    )


serve()
