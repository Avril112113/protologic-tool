import os.path

from prototool.template import Template, TemplateFile
from prototool.simulation import SimulationFleet, SimulationHook


class ProtoLuaTemplate(Template):
	name = "protolua"
	tools = ["protologic", "protolua"]
	files = [
		TemplateFile("tools/protolua/lua_template", "."),
		TemplateFile("tools/protolua/lua_template/lua/protolua", "./lua/protolua/", override=True),
	]
	default_fleets = [["ship.wasm", True]]
	hooks = []

	def _build(self, mode: int) -> bool:
		protolua_tool = self.proto.get_tool("protolua", error=True)
		wasm_path = os.path.join(protolua_tool.tool_path, "build", "protolua.wasm")

		out_wasm = os.path.join(self.path, "ship.wasm")

		print("Running wizer")
		wizer_tool = self.proto.get_tool("wizer", error=True)
		wizer_exe = wizer_tool.get_executable("wizer", error=True)
		wizer_exe.exec([
			wasm_path,
			"-o", out_wasm,
			"--wasm-simd", "true",
			"--wasm-bulk-memory", "true",
			"--allow-wasi",
			"--mapdir", f"/::{os.path.join(self.path, 'lua')}",
		], exit_for_code=True).wait()

		print("Running wasm-opt")
		binaryen = self.proto.get_tool("binaryen", error=True)
		wasm_opt_exe = binaryen.get_executable("wasm-opt", error=True)
		wasm_opt_exe.exec([
			wasm_path,
			"-o", out_wasm,
			"--enable-simd",
			"--enable-bulk-memory",
			"--strip-dwarf",
			f"-O{4-mode}",
		], exit_for_code=True).wait()
