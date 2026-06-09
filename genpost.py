from pathlib import Path
import markdown
import yaml
from datetime import datetime, date


def format_date(value):
    if not value:
        return "", "", None

    if isinstance(value, datetime):
        dt = value
        long = dt.strftime("%a, %d %b %Y, %H:%M")
    elif isinstance(value, date):
        dt = datetime(value.year, value.month, value.day)
        long = dt.strftime("%a, %d %b %Y")
    else:
        try:
            dt = datetime.strptime(value, "%Y-%m-%d %H:%M")
            long = dt.strftime("%a, %d %b %Y, %H:%M")
        except ValueError:
            d = datetime.strptime(value, "%Y-%m-%d").date()
            dt = datetime(d.year, d.month, d.day)
            long = dt.strftime("%a, %d %b %Y")

    return dt.strftime("%d %b %Y"), long, dt


def load_post(path: Path):
    text = path.read_text()

    meta = {}
    body = text

    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        meta = yaml.safe_load(fm) or {}

    html = markdown.markdown(body)

    formatted_date, formatted_date_long, raw_date = format_date(meta.get("date"))

    return {
        "title": meta.get("title", path.stem),
        "date": formatted_date,
        "date_long": formatted_date_long,
        "date_raw": raw_date,
        "tag": meta.get("tag", "untagged"),
        "slug": path.stem,
        "content": html,
        "url": f"/post/{path.stem}.html"
    }


def build_posts(posts, dist, template, commit_short, commit_full):
    for post in posts:
        print(f"Writing post: {post['slug']}.html")
        output = template.render(
            title=post["title"],
            date=post["date_long"],
            content=post["content"],
            url=post["url"],
            commit_short=commit_short,
            commit_full=commit_full
        )
        (dist / "post" / f"{post['slug']}.html").write_text(output)
