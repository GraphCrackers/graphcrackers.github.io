#!/usr/bin/env python3
"""Validate GraphCrackers' static site without third-party dependencies."""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.errors: list[str] = []
        self.links: list[tuple[str, str]] = []
        self.ids: set[str] = set()
        self.duplicate_ids: set[str] = set()
        self.has_title = False
        self.has_description = False
        self.has_stylesheet = False
        self.in_title = False
        self.title_text = ""

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = dict(attrs_list)
        if "style" in attrs:
            self.errors.append("인라인 style 속성이 있습니다")
        if tag in {"style", "script"}:
            self.errors.append(f"인라인 <{tag}> 요소가 있습니다")
        element_id = attrs.get("id")
        if element_id:
            if element_id in self.ids:
                self.duplicate_ids.add(element_id)
            self.ids.add(element_id)
        if tag == "a" and attrs.get("href"):
            self.links.append((attrs["href"] or "", attrs.get("target") or ""))
        if tag == "img" and not attrs.get("alt"):
            self.errors.append("alt 없는 이미지가 있습니다")
        if tag == "meta" and attrs.get("name") == "description" and attrs.get("content"):
            self.has_description = True
        if tag == "link" and attrs.get("rel") == "stylesheet" and attrs.get("href") == "/assets/style.css":
            self.has_stylesheet = True
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False
            self.has_title = bool(self.title_text.strip())

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_text += data


def resolve_internal(root: Path, page: Path, href: str) -> tuple[Path, str] | None:
    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc or href.startswith(("mailto:", "tel:")):
        return None
    path_text = unquote(parsed.path)
    if not path_text:
        target = page
    elif path_text.startswith("/"):
        target = root / path_text.lstrip("/")
    else:
        target = page.parent / path_text
    if target.is_dir() or path_text.endswith("/"):
        target = target / "index.html"
    return target.resolve(), unquote(parsed.fragment)


def validate(root: Path) -> list[str]:
    failures: list[str] = []
    pages: dict[Path, PageParser] = {}
    for page in sorted(root.rglob("*.html")):
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        pages[page.resolve()] = parser
        label = page.relative_to(root)
        for error in parser.errors:
            failures.append(f"{label}: {error}")
        if not parser.has_title:
            failures.append(f"{label}: title이 없습니다")
        if not parser.has_description:
            failures.append(f"{label}: meta description이 없습니다")
        if not parser.has_stylesheet:
            failures.append(f"{label}: /assets/style.css를 사용하지 않습니다")
        for duplicate_id in sorted(parser.duplicate_ids):
            failures.append(f"{label}: id '{duplicate_id}'가 중복됩니다")

    for page, parser in pages.items():
        label = page.relative_to(root)
        for href, target_attr in parser.links:
            resolved = resolve_internal(root, page, href)
            if resolved is None:
                parsed = urlparse(href)
                if parsed.scheme in {"http", "https"} and target_attr != "_blank":
                    failures.append(f"{label}: 외부 링크에 target=_blank가 없습니다: {href}")
                continue
            target, fragment = resolved
            if not target.is_file():
                failures.append(f"{label}: 끊어진 내부 링크: {href}")
                continue
            if fragment and target.suffix == ".html":
                target_parser = pages.get(target)
                if target_parser is None or fragment not in target_parser.ids:
                    failures.append(f"{label}: 존재하지 않는 앵커: {href}")

    combined = "\n".join(path.read_text(encoding="utf-8") for path in root.rglob("*.html"))
    for forbidden in ("chief@", "{{", "}}", 'style="'):
        if forbidden in combined:
            failures.append(f"전체 문서: 금지 또는 미완성 문자열이 있습니다: {forbidden}")
    if not (root / ".nojekyll").exists():
        failures.append(".nojekyll 파일이 없습니다")

    css = (root / "assets" / "style.css").read_text(encoding="utf-8")
    colors = dict(re.findall(r"--([\w-]+):\s*(#[0-9a-fA-F]{6})", css))
    for foreground in ("ink", "ink-2", "accent-text"):
        for background in ("ground", "paper"):
            if contrast_ratio(colors[foreground], colors[background]) < 4.5:
                failures.append(f"대비비 4.5:1 미만: --{foreground} / --{background}")
    return failures


def contrast_ratio(first: str, second: str) -> float:
    def luminance(value: str) -> float:
        channels = [int(value[index:index + 2], 16) / 255 for index in (1, 3, 5)]
        linear = [channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4 for channel in channels]
        return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

    light, dark = sorted((luminance(first), luminance(second)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    failures = validate(root)
    if failures:
        print("검증 실패")
        for failure in failures:
            print(f"- {failure}")
        return 1
    page_count = len(list(root.rglob("*.html")))
    print(f"검증 통과: HTML {page_count}개, 내부 링크·메타데이터·단일 CSS·금지 문자열 확인")
    return 0


if __name__ == "__main__":
    sys.exit(main())
