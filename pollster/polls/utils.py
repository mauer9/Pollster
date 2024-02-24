def get_btn_context(sort: str) -> dict:
    sorting_buttons = {
        "date": {"btn": "btn-primary", "href": "-date", "arrow": "img/up.png"},
        "name": {"btn": "btn-primary", "href": "name", "arrow": "img/up.png"},
        "votes": {"btn": "btn-primary", "href": "votes", "arrow": "img/up.png"},
    }

    for key, button in sorting_buttons.items():
        if sort == key:
            button["btn"] = "btn-warning"
            button["href"] = f"-{key}"
        if sort == f"-{key}":
            button["btn"] = "btn-warning"
            button["href"] = key
            button["arrow"] = "img/down.png"

    context = {}
    for key, btn in sorting_buttons.items():
        for name, value in btn.items():
            context[f"{key}_{name}"] = value
    return context
