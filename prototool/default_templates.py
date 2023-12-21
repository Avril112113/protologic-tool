from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from .prototool import ProtoTool


def add_default_templates(prototool: "ProtoTool"):
	import templates
	prototool.add_template(templates.BlankTemplate)
	prototool.add_template(templates.ProtoLuaTemplate)
	prototool.add_template(templates.AssemblyScriptTemplate)
