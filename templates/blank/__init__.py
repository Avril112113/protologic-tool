from prototool.template import Template, TemplateFile
from prototool.simulation import SimulationFleet, SimulationHook


class BlankTemplate(Template):
	name = "blank"
	tools = ["protologic"]
	files = []
	default_fleets = ["example.wasm"]
	hooks = []
