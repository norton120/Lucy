from typing import Optional
import jinja2


class PromptEngine:
    """an abstraction for the jinja2 templating engine with some Lucy specific functionality."""

    def __init__(self, package:str, templates_directory: Optional[str]="templates") -> None:
        self.package_name = package
        self.env = jinja2.Environment(
            loader=jinja2.PackageLoader(package, templates_directory),
        )

    def render_core(self, template: str, **kwargs) -> str:
        """renders a memory core template with kwargs"""
        template_file = f"{self.package_name}/memory_cores/{template}.txt"
        return self.env.get_template(template_file).render(**kwargs)