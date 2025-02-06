from pathlib import Path
from typing import Any, Dict

import jinja2


class TemplateRenderer:
    def __init__(self, template_name: str = "basic"):
        self.env = jinja2.Environment(
            # loader=jinja2.PackageLoader("crab", f"data/templates/{template_name}"),
            loader=jinja2.FileSystemLoader(f"src/crab/data/templates/{template_name}"),
            autoescape=False,
            keep_trailing_newline=True,
        )

    def render(
        self,
        target_dir: Path,
        context: Dict[str, Any],
    ) -> None:
        # Create project directory
        target_dir.mkdir(parents=True, exist_ok=True)

        # Copy and render all template files
        for template_path in self.env.list_templates():
            template = self.env.get_template(template_path)
            rendered_content = template.render(**context)

            # Replace {{ project_name }} in paths
            output_path = target_dir / template_path.replace(
                "{{ project_name }}", context["project_name"]
            )
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(rendered_content)
