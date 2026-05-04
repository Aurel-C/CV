from __future__ import annotations

from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
TEMPLATE_DIR = ROOT / "templates"
OUTPUTS = [
    ("web.html.j2", "en", ROOT / "index.html"),
    ("web.html.j2", "fr", ROOT / "index.fr.html"),
    ("compact.html.j2", "en", ROOT / "cv_compact.html"),
    ("compact.html.j2", "en", ROOT / "cv_en.pdf"),
    ("compact.html.j2", "fr", ROOT / "cv_fr.pdf"),
    ("compact.html.j2", "fr", ROOT / "cv_compact_fr.html"),
]


def load_data(language: str) -> dict:
    data_file = DATA_DIR / f"{language}.yml"
    with data_file.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def render_template(environment: Environment, template_name: str, language: str, data: dict) -> str:
    template = environment.get_template(template_name)
    return template.render(
        lang=language,
        person=data["person"],
        meta=data["meta"],
        sections=data["sections"],
        labels=data["labels"],
        hidden_sections=data.get("hidden_sections", []),
        education=data["education"],
        experience=data["experience"],
        projects=data["projects"],
        interests=data["interests"],
        conferences=data["conferences"],
        publications=data["publications"],
        skills=data["skills"],
        languages=data["languages"],
    )


def main() -> None:
    environment = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape(["html", "j2"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    for template_name, language, output_path in OUTPUTS:
        data = load_data(language)
        rendered_content = render_template(environment, template_name, language, data)

        if output_path.suffix == ".pdf":
            print(f"Generating PDF: {output_path.name}")
            HTML(string=rendered_content, base_url=str(ROOT)).write_pdf(output_path)
        else:
            print(f"Generating HTML: {output_path.name}")
            output_path.write_text(rendered_content, encoding="utf-8")


if __name__ == "__main__":
    main()
