from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "README.md",
    "README_EN.md",
    "CITATION.cff",
    "RIGHTS.md",
    "papers/risk-aware-predictive-maintenance-ko.pdf",
    "papers/risk-aware-predictive-maintenance-en.pdf",
    "papers/read-ko.md",
    "papers/read-en.md",
    "docs/EASY_GUIDE_KO.md",
    "docs/RESEARCH_FLOW_KO.md",
    "docs/RESULTS_AT_A_GLANCE.md",
}
EXPECTED_PREVIEWS = {"ko": 13, "en": 15}
MARKDOWN_LINK = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
HTML_LINK = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']", re.IGNORECASE)


def local_target(markdown_file: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().split(" ", 1)[0].strip("<>")
    if not target or target.startswith(("#", "http://", "https://", "mailto:")):
        return None
    target = unquote(target.split("#", 1)[0].split("?", 1)[0])
    return (markdown_file.parent / target).resolve()


def main() -> int:
    errors: list[str] = []

    for relative in sorted(REQUIRED):
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")

    for pdf in sorted((ROOT / "papers").glob("*.pdf")):
        if pdf.read_bytes()[:5] != b"%PDF-":
            errors.append(f"invalid PDF signature: {pdf.relative_to(ROOT)}")

    for language, expected in EXPECTED_PREVIEWS.items():
        pages = sorted((ROOT / "assets" / "paper-preview" / language).glob("page-*.jpg"))
        if len(pages) != expected:
            errors.append(
                f"{language} preview count is {len(pages)}; expected {expected}"
            )

    for markdown_file in sorted(ROOT.rglob("*.md")):
        text = markdown_file.read_text(encoding="utf-8")
        targets = MARKDOWN_LINK.findall(text) + HTML_LINK.findall(text)
        for raw_target in targets:
            resolved = local_target(markdown_file, raw_target)
            if resolved is not None and not resolved.exists():
                errors.append(
                    f"broken local link in {markdown_file.relative_to(ROOT)}: {raw_target}"
                )

    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Repository validation passed.")
    print("- required research files: present")
    print("- PDF signatures: valid")
    print("- mobile previews: 13 Korean pages, 15 English pages")
    print("- local Markdown links: resolved")
    return 0


if __name__ == "__main__":
    sys.exit(main())
