def build_sitemap(posts, tags):
    urls = ["https://lordhck.com/"]
    for post in posts:
        urls.append(f"https://lordhck.com{post['url']}")
    for tag in tags:
        urls.append(f"https://lordhck.com/tags/{tag}")
    items = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{items}
</urlset>
"""
