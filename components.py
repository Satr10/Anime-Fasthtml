from fasthtml.common import *


def create_navbar(links, query: str = ""):
    # links adalah dictionary dengan format: {"text": "url"}

    # Fungsi helper untuk membuat list item
    def create_list_item(text, url):
        return Li(A(text, href=url))

    # Membuat menu items untuk mobile dan desktop
    mobile_menu_items = [create_list_item(text, url) for text, url in links.items()]
    desktop_menu_items = [create_list_item(text, url) for text, url in links.items()]

    return Div(
        # Navbar Start (Logo dan Mobile Menu)
        Div(
            Div(
                # Mobile Menu Toggle Button
                Div(
                    NotStr(
                        """
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-5 w-5">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16"></path>
                    </svg>
                    """
                    ),
                    tabindex="0",
                    role="button",
                    cls="btn btn-ghost lg:hidden",
                ),
                # Mobile Menu Items
                Ul(
                    *mobile_menu_items,
                    tabindex="0",
                    cls="menu menu-sm dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow",
                ),
                cls="dropdown",
            ),
            # Logo
            A("Anime", href="/", cls="btn btn-ghost text-xl"),
            cls="navbar-start",
        ),
        # Navbar Center (Desktop Menu)
        Div(
            Ul(
                *desktop_menu_items,
                cls="menu menu-horizontal px-1",
            ),
            cls="navbar-center hidden lg:flex",
        ),
        # Navbar End (Button)
        Div(
            Form(
                Input(
                    type="text",
                    placeholder="Cari...",
                    cls="input input-bordered w-full max-w-xs",
                    name="query",
                    value=query,
                ),
                method="get",
                action="/search",
            ),
            cls="navbar-end",
        ),
        cls="navbar bg-base-300 rounded-lg ",
    )


def warning():
    warning_state = None
    return (
        Div(
            NotStr(
                """  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    class="stroke-info h-6 w-6 shrink-0">
    <path
      stroke-linecap="round"
      stroke-linejoin="round"
      stroke-width="2"
      d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
  </svg>"""
            ),
            Span("Test"),
            role="alert",
            cls="alert m-4 w-4/5 mx-auto",
        )
        if warning_state
        else None
    )


def kartu(judul: str, rating: int, gambar: str, id: int):
    star_rating = (
        "★" * rating + "☆" * (5 - rating) if rating is not None else "No Rating"
    )
    return Div(
        Figure(
            Img(
                src=gambar,
                alt=f"Cover of {judul}",
                cls="sm:h-80 sm:w-56 w-40 h-64 object-cover",
            )
        ),
        Div(
            A(
                H2(judul, cls="card-title sm:text-lg text-sm line-clamp-2"),
                href=f"/anime/{id}",
            ),
            Span(star_rating, cls="badge badge-primary"),
            cls="card-body sm:w-56 sm:h-32 w-40 h-24",
        ),
        cls="card card-compact bg-base-100 shadow-xl tooltip",
        # data_tip=judul,
    )


def kumpulan_kartu(kategori: str, animes: list, link: str):
    cards = [
        kartu(anime["judul"], anime["rating"], anime["gambar"], anime["id"])
        for anime in animes
    ]
    return Div(
        Div(A(H2(kategori, cls="text-2xl font-bold"), href=link), cls="mb-4"),
        Div(
            *cards,
            cls="flex flex-wrap gap-4 mx-auto justify-center items-center",
        ),
        cls="rounded-lg flex flex-col pt-4 pb-8 my-4 items-center bg-base-200 sm:mx-8",
    )


def pemisah():
    return (Div("-", cls="divider"),)


def footer():
    return Footer(
        Aside(P("Copyright © 2024 - Satrio")),
        cls="footer footer-center bg-base-300 text-base-content p-4",
    )


def page_navigation(current_page: int = 1, has_next_page: bool = False, path: str = ""):
    prev_page = current_page - 1 if current_page > 1 else 1
    next_page = current_page + 1 if has_next_page else current_page
    return Div(
        Div(
            A(
                "«",
                href=f"/{path}/{prev_page}",
                cls="join-item btn",
            ),
            A(
                f"Page {current_page}",
                href=f"/{path}/{current_page}",
                cls="join-item btn",
            ),
            A(
                "»",
                href=f"/{path}/{next_page}",
                cls="join-item btn",
                disabled=not has_next_page,
            ),
            cls="join",
        ),
        cls="flex justify-center",
    )
