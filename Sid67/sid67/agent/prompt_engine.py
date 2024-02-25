import jinja2


class PromptEngine:
    """an abstraction for the jinja2 templating engine with some Sid specific functionality."""

    def __init__(self, package:str, templates_directory: str):
        self.env = jinja2.Environment(
            loader=jinja2.PackageLoader(package, templates_directory),
        )

    def render(self, template: str, **kwargs) -> str:
        """renders a template with kwargs"""
        return self.env.get_template(template).render(**kwargs)