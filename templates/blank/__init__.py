from prototool.template import Template, TemplateFile


class BlankTemplate(Template):
	name = "blank"
	tools = ["protologic"]
	files = []
	default_fleets = [["example.wasm", True]]
