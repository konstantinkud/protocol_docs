from pathlib import Path

import markdown
from flask import Flask, abort, render_template

app = Flask(__name__)

DOCS = Path("docs")


def get_pages():
    pages = []

    for file in sorted(DOCS.glob("*.md")):
        pages.append({"slug": file.stem, "title": file.stem.replace("-", " ").title()})

    return pages


@app.route("/")
def index():
    return render_template("index.html", pages=get_pages())


@app.route("/<slug>")
def page(slug):
    file = DOCS / f"{slug}.md"

    if not file.exists():
        abort(404)

    html = markdown.markdown(
        file.read_text(encoding="utf-8"), extensions=["fenced_code", "tables"]
    )

    return render_template(
        "page.html",
        pages=get_pages(),
        content=html,
        title=slug.replace("-", " ").title(),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
