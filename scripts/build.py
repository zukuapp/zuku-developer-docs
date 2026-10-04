#!/usr/bin/env python3
"""Build the two public documentation languages with the existing pinned MkDocs toolchain."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, unquote
import gzip
import hashlib
import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT.parent / "artifact"
ASSETS = ROOT / "assets"
PAGES = {
    "README.md", "getting-started.md", "installation.md", "starters/index.md", "starters/html5.md", "starters/phaser.md", "starters/existing-game.md",
    "cli/index.md", "cli/commands.md", "cli/authentication.md", "cli/providers.md", "cli/models.md", "cli/agent.md", "cli/publishing.md", "cli/studio.md",
    "authentication.md", "captcha.md", "contents.md", "media.md", "feeds.md", "social.md", "game-cloud.md", "devconsole.md", "examples.md", "errors.md", "changelog.md", "rate-limits.md",
}
LABELS = {
    "ko": dict(skip="본문으로 이동", primary="주요 메뉴", get_started="시작하기", search="문서 검색", language="Switch to English", other_language="EN", theme="화면 테마 변경", menu="문서 메뉴 열기", documentation="개발 문서", navigation="문서 탐색", workspace="게임 개발 워크스페이스", guide="가이드", choose_starter="만들고 싶은 게임부터 시작하세요", all_starters="모든 Starter", version="CLI", feedback="문서 의견 보내기", page_navigation="이전·다음 문서", previous="이전", next="다음", footer="게임을 만드는 가장 빠른 시작", on_page="이 페이지에서", ready="처음 시작하나요?", first_game="첫 게임 만들기", search_placeholder="문서, 명령어, API 검색…", close="닫기", search_hint="문서, 명령어, API 가이드를 검색하세요.", navigate="이동", open="열기"),
    "en": dict(skip="Skip to content", primary="Primary navigation", get_started="Get started", search="Search docs", language="한국어로 전환", other_language="한국어", theme="Change theme", menu="Open documentation menu", documentation="Documentation", navigation="Documentation navigation", workspace="Game development workspace", guide="Guide", choose_starter="Start with the game you want to build", all_starters="All starters", version="CLI", feedback="Give documentation feedback", page_navigation="Previous and next pages", previous="Previous", next="Next", footer="A faster start for your next game", on_page="On this page", ready="New to ZUKU?", first_game="Build your first game", search_placeholder="Search docs, commands, and APIs…", close="Close", search_hint="Search pages, commands, and API guides.", navigate="navigate", open="open"),
}
NAV = {
    "ko": [
        {"소개": "README.md"},
        {"시작하기": [{"빠른 시작": "getting-started.md"}, {"CLI 설치": "installation.md"}]},
        {"Starters": [{"Starter 선택": "starters/index.md"}, {"Canvas 러너": "starters/html5.md"}, {"Phaser 2D": "starters/phaser.md"}, {"기존 게임 가져오기": "starters/existing-game.md"}]},
        {"ZUKU CLI": [{"CLI 개요": "cli/index.md"}, {"명령어": "cli/commands.md"}, {"로그인": "cli/authentication.md"}, {"Provider 연결": "cli/providers.md"}, {"모델 선택": "cli/models.md"}, {"게임 개발 에이전트": "cli/agent.md"}, {"패키징과 게시": "cli/publishing.md"}, {"ZUKU Studio": "cli/studio.md"}]},
        {"API 가이드": [{"인증": "authentication.md"}, {"캡차": "captcha.md"}, {"콘텐츠 게시": "contents.md"}, {"미디어와 게임 패키지": "media.md"}, {"피드": "feeds.md"}, {"소셜": "social.md"}, {"게임 클라우드": "game-cloud.md"}, {"개발자 콘솔": "devconsole.md"}, {"호출 예제": "examples.md"}]},
        {"참고": [{"오류 해결": "errors.md"}, {"요청 한도": "rate-limits.md"}, {"변경 이력": "changelog.md"}]},
    ],
    "en": [
        {"Introduction": "README.md"},
        {"Get started": [{"Quickstart": "getting-started.md"}, {"Install the CLI": "installation.md"}]},
        {"Starters": [{"Choose a starter": "starters/index.md"}, {"Canvas runner": "starters/html5.md"}, {"Phaser 2D": "starters/phaser.md"}, {"Bring your game": "starters/existing-game.md"}]},
        {"ZUKU CLI": [{"CLI overview": "cli/index.md"}, {"Commands": "cli/commands.md"}, {"Authentication": "cli/authentication.md"}, {"Connect a provider": "cli/providers.md"}, {"Choose a model": "cli/models.md"}, {"Game development agent": "cli/agent.md"}, {"Package and publish": "cli/publishing.md"}, {"ZUKU Studio": "cli/studio.md"}]},
        {"API guides": [{"Authentication": "authentication.md"}, {"Captcha": "captcha.md"}, {"Publish content": "contents.md"}, {"Media and game packages": "media.md"}, {"Feeds": "feeds.md"}, {"Social": "social.md"}, {"Game cloud": "game-cloud.md"}, {"Developer console": "devconsole.md"}, {"Request examples": "examples.md"}]},
        {"Reference": [{"Troubleshooting": "errors.md"}, {"Rate limits": "rate-limits.md"}, {"Changelog": "changelog.md"}]},
    ],
}
STARTERS = {
    "ko": [dict(title="Canvas 러너", description="설치 후 바로 실행하는 작은 점프 게임. 외부 의존성 없이 코드를 바꿔 보세요.", tag="Canvas", meta="외부 의존성 없음", url="starters/html5/", art="canvas"), dict(title="Phaser 2D", description="장면, 입력, 게임 오브젝트를 갖춘 2D Starter. 로컬 엔진을 함께 제공합니다.", tag="Phaser", meta="엔진 포함", url="starters/phaser/", art="phaser"), dict(title="기존 게임 가져오기", description="이미 만든 HTML5 게임을 ZUKU 프로젝트로 정리하고 패키지로 만드세요.", tag="HTML5", meta="마이그레이션", url="starters/existing-game/", art="migrate"), dict(title="에이전트로 만들기", description="게임 아이디어부터 구현, 플레이테스트, 패키징까지 한 흐름으로 이어 가세요.", tag="Agent", meta="계정 연결 필요", url="cli/agent/", art="agent")],
    "en": [dict(title="Canvas runner", description="A small jump game you can run straight away. Change the code with no external dependencies.", tag="Canvas", meta="Zero dependencies", url="starters/html5/", art="canvas"), dict(title="Phaser 2D", description="A 2D starter with scenes, input, and game objects. The local engine is included.", tag="Phaser", meta="Engine included", url="starters/phaser/", art="phaser"), dict(title="Bring your game", description="Turn an existing HTML5 game into a ZUKU project and package it for the platform.", tag="HTML5", meta="Migration", url="starters/existing-game/", art="migrate"), dict(title="Build with the agent", description="Take a game idea through implementation, playtesting, and packaging in a single workflow.", tag="Agent", meta="Account required", url="cli/agent/", art="agent")],
}


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_rows():
    rows = []
    for path in sorted(ROOT.rglob("*")):
        relative = path.relative_to(ROOT)
        if any(part in {".codex", ".git", "__pycache__"} for part in relative.parts):
            continue
        require(not path.is_symlink(), "Symlink in isolated source")
        if path.is_file():
            rows.append(dict(path=str(relative), bytes=path.stat().st_size, sha256=digest(path)))
    return rows


class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()
        self.text = []
        self.article = False
        self.title = []
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.add(values["id"])
        for key in ("href", "src"):
            if key in values:
                self.links.append(values[key])
        if tag == "article":
            self.article = True
        if tag == "h1" and self.article:
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "article":
            self.article = False
        if tag == "h1":
            self.in_title = False

    def handle_data(self, value):
        if self.article:
            self.text.append(value)
        if self.in_title:
            self.title.append(value)


def route_for(page):
    if page == "README.md":
        return ""
    return page[:-8] if page.endswith("index.md") else page[:-3] + "/"


def main():
    (ROOT / ".codex").mkdir(exist_ok=True)
    require(not OUTPUT.exists(), "Refuse overwriting an existing documentation artifact")
    configs = []
    for locale in ("ko", "en"):
        actual = {str(p.relative_to(ROOT / "docs" / locale)) for p in (ROOT / "docs" / locale).rglob("*.md")}
        require(actual == PAGES, f"{locale} document allowlist mismatch: {sorted(actual ^ PAGES)}")
        for path in (ROOT / "docs" / locale).rglob("*"):
            require(not path.is_symlink(), "Symlink in documentation inputs")
            require(path.is_dir() or path.suffix == ".md", "Only public markdown is allowed under locale content")
    OUTPUT.mkdir(mode=0o755)
    for locale in ("ko", "en"):
        home = "/" if locale == "ko" else "/en/"
        output = OUTPUT if locale == "ko" else OUTPUT / "en"
        config = dict(site_name="ZUKU Docs", site_url="https://docs.zuzunza.com" + home, site_description="ZUKU CLI 설치, 게임 Starter, 에이전트와 API 문서" if locale == "ko" else "Install the ZUKU CLI, choose a game starter, and explore agent and API guides", docs_dir=str(ROOT / "docs" / locale), site_dir=str(output), use_directory_urls=True, hooks=[str(ROOT / "scripts" / "hooks.py")], theme=dict(name=None, custom_dir=str(ROOT / "theme"), static_templates=[]), plugins=[], nav=NAV[locale], markdown_extensions=["tables", "fenced_code", "attr_list", "md_in_html", "admonition", "pymdownx.superfences", {"pymdownx.highlight": {"pygments_lang_class": True}}, {"pymdownx.tabbed": {"alternate_style": True}}, {"toc": {"permalink": "#"}}], validation=dict(nav=dict(not_found="warn", omitted_files="warn"), links=dict(not_found="warn", anchors="warn", unrecognized_links="warn")), extra=dict(locale=locale, other_locale="en" if locale == "ko" else "ko", locale_home=home, other_home="/en/" if locale == "ko" else "/", labels=LABELS[locale], starters=STARTERS[locale]))
        config_path = ROOT / f"mkdocs-{locale}.yml"
        config_path.write_text(yaml.safe_dump(config, allow_unicode=True, sort_keys=False))
        configs.append(config_path)
    frozen = source_rows()
    (ROOT / ".codex" / "SOURCE-MANIFEST.json").write_text(json.dumps(dict(schema="zuku-modern-docs-source/1", root=str(ROOT), files=frozen, excluded=[".codex", ".git", "__pycache__"]), indent=2) + "\n")
    for config_path in configs:
        subprocess.run([sys.executable, "-m", "mkdocs", "build", "--strict", "--clean", "--config-file", str(config_path)], check=True, cwd=ROOT)
    shutil.copytree(ASSETS, OUTPUT / "assets", dirs_exist_ok=False)
    records = {}
    documents = {}
    for locale in ("ko", "en"):
        pages = []
        prefix = "" if locale == "ko" else "en/"
        for order, name in enumerate(sorted(PAGES, key=lambda p: (p != "README.md", p != "getting-started.md", p != "installation.md", p))):
            route = prefix + route_for(name)
            file = OUTPUT / route / "index.html"
            require(file.is_file(), f"Missing built route /{route}")
            doc = Document(); doc.feed(file.read_text())
            documents[route] = doc
            title = "".join(doc.title).strip()
            require(bool(title), f"Missing H1 in {route}")
            pages.append(dict(title=title, url="/" + route, text=" ".join(" ".join(doc.text).split()), section="Starter" if "/starters/" in "/" + route else "CLI" if "/cli/" in "/" + route else "Guide", order=order))
        (OUTPUT / "assets" / f"search-{locale}.json").write_text(json.dumps(pages, ensure_ascii=False, separators=(",", ":")) + "\n")
        records[locale] = dict(routes=len(pages), search_documents=len(pages))
    invalid = []
    for route, doc in documents.items():
        base = "https://docs.zuzunza.com/" + route
        for link in doc.links:
            parsed = urlsplit(urljoin(base, link))
            if parsed.netloc != "docs.zuzunza.com":
                continue
            rel = unquote(parsed.path).lstrip("/")
            target = OUTPUT / rel
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                invalid.append(dict(page=route, href=link, reason="missing file")); continue
            if parsed.fragment and target.suffix == ".html":
                key = rel[:-10] if rel.endswith("index.html") else rel
                anchor_doc = documents.get(key)
                if anchor_doc is None:
                    anchor_doc = Document(); anchor_doc.feed(target.read_text())
                if unquote(parsed.fragment) not in anchor_doc.ids:
                    invalid.append(dict(page=route, href=link, reason="missing anchor"))
    (ROOT / ".codex" / "LINK-AUDIT.json").write_text(json.dumps(dict(checked_pages=len(documents), invalid=invalid), indent=2, ensure_ascii=False) + "\n")
    require(not invalid, f"Broken documentation links: {len(invalid)}; see LINK-AUDIT.json")
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", namespace)
    sitemap = ET.Element(f"{{{namespace}}}urlset")
    for route in sorted(documents):
        entry = ET.SubElement(sitemap, f"{{{namespace}}}url")
        ET.SubElement(entry, f"{{{namespace}}}loc").text = "https://docs.zuzunza.com/" + route
    ET.ElementTree(sitemap).write(OUTPUT / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    (OUTPUT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://docs.zuzunza.com/sitemap.xml\n")
    (OUTPUT / "404.html").write_text('<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>문서를 찾을 수 없어요 · Page not found — ZUKU Docs</title><link rel="stylesheet" href="/assets/docs.css"><main class="content prose"><h1>문서를 찾을 수 없어요.</h1><p lang="en">This documentation page could not be found.</p><p><a href="/">한국어 문서</a> · <a href="/en/" lang="en">English documentation</a></p></main></html>')
    for path in list(OUTPUT.rglob("*")):
        if path.is_file() and path.suffix in {".html", ".css", ".js", ".json", ".xml"}:
            data = path.read_bytes()
            if len(data) > 512:
                path.with_name(path.name + ".gz").write_bytes(gzip.compress(data, compresslevel=9, mtime=0))
    files = []
    for path in sorted(OUTPUT.rglob("*")):
        path.chmod(0o755 if path.is_dir() else 0o644)
        if path.is_file():
            files.append(dict(path=str(path.relative_to(OUTPUT)), bytes=path.stat().st_size, sha256=digest(path)))
    require(source_rows() == frozen, "Documentation inputs changed during build")
    proof = dict(schema="zuku-modern-docs-build/1", locales=records, locale_count=2, routes=len(documents), link_errors=0, source_manifest_sha256=digest(ROOT / ".codex" / "SOURCE-MANIFEST.json"), source_before_after_equal=True, generator="existing MkDocs 1.6.1 with custom ZUKU theme", files=files, production_changes=False)
    (ROOT / ".codex" / "BUILD-PROOF.json").write_text(json.dumps(proof, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(dict(routes=len(documents), locales=records, public_files=len(files), link_errors=0)))


if __name__ == "__main__":
    main()
