from typing import TypeVar, Type

from .tool import Tool
from .template import Template

from .default_tools import add_default_tools
from .default_templates import add_default_templates


TTool = TypeVar("TTool", bound=Tool)
TTemplate = TypeVar("TTemplate", bound=Type[Template])


class ProtoTool:
	"""
	A helper to hold all information and provide commonly used tools.
	"""

	def __init__(self):
		self.tools: dict[str, Tool] = {}
		self.templates: dict[str, Template] = {}
		add_default_tools(self)
		add_default_templates(self)

	def add_tool(self, tool: TTool) -> TTool:
		"""Added tools are simply a config, they do not do anything unless invoked to do so."""
		self.tools[tool.name] = tool
		return tool

	def get_tool(self, name: str, error=False):
		if error and name not in self.tools:
			raise ValueError(f"Missing tool '{name}'")
		return self.tools.get(name, None)

	def add_template(self, template: TTemplate) -> TTemplate:
		"""Added tools are simply a config, they do not do anything unless invoked to do so."""
		self.templates[template.name] = template
		return template

	def get_template(self, name: str, error=False):
		if error and name not in self.templates:
			raise ValueError(f"Missing template '{name}'")
		return self.templates.get(name, None)
