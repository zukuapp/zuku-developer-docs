"""Keep Unicode heading IDs and the previous public API guide's anchor aliases."""
import re
from pymdownx.slugs import slugify


def on_config(config):
    config.mdx_configs.setdefault("toc", {})["slugify"] = slugify(case="lower")
    return config


def on_page_markdown(markdown, **kwargs):
    lines = []
    fence = False
    seen = set()
    for line in markdown.splitlines():
        if line.startswith("```"):
            fence = not fence
        heading = re.match(r"^#{1,6}\s+(.+)$", line) if not fence else None
        if heading:
            text = heading.group(1)
            old = re.sub(r"\s+", "-", re.sub(r"[^\w\s가-힣-]", "", text.lower()).strip())
            new = slugify(case="lower")(text.replace("`", ""), "-")
            if old and old != new and old not in seen:
                lines.extend([f'<span id="{old}"></span>', ""])
                seen.add(old)
        lines.append(line)
    return "\n".join(lines)
