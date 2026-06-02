from pathlib import Path
import os
import shutil
import subprocess
import markdown
import yaml
from xml.sax.saxutils import escape
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, date

# Jinja setup
env = Environment(loader=FileSystemLoader("templates"))
index_template = env.get_template("index.j2")
post_template = env.get_template("post.j2")
tag_template = env.get_template("tag.j2")
notfound_template = env.get_template("404.j2")

# Paths
DIST = Path("dist")
POSTS_DIR = Path("content/posts")
STATIC_DIR = Path("static")

# Clean dist
if DIST.exists():
    shutil.rmtree(DIST)

(DIST / "post").mkdir(parents=True, exist_ok=True)
(DIST / "static").mkdir(parents=True, exist_ok=True)

# Date formatting (display)
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

# Load markdown post
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

# Resolve commit hash
try:
    commit_short = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
    commit_full = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
except Exception:
    commit_short = os.environ.get("COMMIT", "unknown")
    commit_full = os.environ.get("COMMIT_FULL", commit_short)

# Build posts
posts = []

for file in POSTS_DIR.glob("*.md"):
    post = load_post(file)
    posts.append(post)

    print(f"Writing post: {post['slug']}.html")

    output = post_template.render(
        title=post["title"],
        date=post["date_long"],
        content=post["content"],
        url=post["url"],
        commit_short=commit_short,
        commit_full=commit_full
    )

    (DIST / "post" / f"{post['slug']}.html").write_text(output)

# Sort posts (NEWEST FIRST)
posts.sort(key=lambda x: x["date_raw"] or datetime.min, reverse=True)

# Build index
tags = sorted({post["tag"] for post in posts if post["tag"]})
index_html = index_template.render(posts=posts, tags=tags, commit_short=commit_short, commit_full=commit_full)
(DIST / "index.html").write_text(index_html)

# Build tag pages
for tag in tags:
    tag_posts = [p for p in posts if p["tag"] == tag]
    tag_dir = DIST / "tags" / tag
    tag_dir.mkdir(parents=True, exist_ok=True)
    print(f"Writing tag page: tags/{tag}")
    tag_html = tag_template.render(tag=tag, posts=tag_posts, commit_short=commit_short, commit_full=commit_full)
    (tag_dir / "index.html").write_text(tag_html)

# Build 404 page
(DIST / "404.html").write_text(notfound_template.render(commit_short=commit_short, commit_full=commit_full))

# Copy static files
shutil.copytree(STATIC_DIR, DIST / "static", dirs_exist_ok=True)

# Copy CNAME for GitHub Pages
if Path("CNAME").exists():
    shutil.copy("CNAME", DIST / "CNAME")

# RSS feed
def build_feed(posts):
    items = []

    for post in posts:
        if not post["date_raw"]:
            continue

        items.append(f"""
        <item>
            <title>{escape(post['title'])}</title>
            <link>https://lordhck.com{post['url']}</link>
            <description>{escape(post['title'])}</description>
            <pubDate>{post['date_raw'].strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
            <guid>https://lordhck.com{post['url']}</guid>
        </item>
        """)

    return f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>Lordhck</title>
    <link>https://lordhck.com</link>
    <description>Personal blog</description>
    {''.join(items)}
</channel>
</rss>
"""

feed_xml = build_feed(posts)
(DIST / "feed.xml").write_text(feed_xml)

print("Build complete.")
