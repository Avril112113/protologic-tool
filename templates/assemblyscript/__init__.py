import os.path

from prototool.utils import file_replace
from prototool.template import Template, TemplateFile
from prototool.simulation import SimulationFleet, SimulationHook


class AssemblyScriptTemplate(Template):
	name = "assemblyscript"
	tools = ["protologic", "node"]
	files = [
		TemplateFile("data", "."),
		TemplateFile("data/src/protologic", "src/protologic", override=True),
	]
	default_fleets = ["build/release.wasm"]
	hooks = []

	def _upgrade_post(self):
		prototool_tool = self.proto.get_tool("prototool", error=True)
		prototool_exe = prototool_tool.get_executable("prototool")

		node_tool = self.proto.get_tool("node", error=True)
		npm_exe = node_tool.get_executable("npm", error=True)

		file_replace(os.path.join(self.path, "package.json"), {
			"${prototool}": " ".join(prototool_exe.get_shell_args()),
		})

		# Install/update all dependencies
		npm_exe.exec(["install"], cwd=os.path.abspath(self.path), exit_for_code=True)

	def _build(self, mode: int) -> bool:
		node_tool = self.proto.get_tool("node", error=True)
		npx_exe = node_tool.get_executable("npx", error=True)

		# Relative to self.path
		dst = os.path.join("build", "release.wasm")

		print("Building wasm.")
		npx_exe.exec([
			"asc",
			"./src/tick.ts",
			"-b", dst,
		], cwd=os.path.abspath(self.path), exit_for_code=True)

		print("Running wasm-opt")
		binaryen = self.proto.get_tool("binaryen", error=True)
		wasm_opt_exe = binaryen.get_executable("wasm-opt", error=True)
		wasm_opt_exe.exec([
			dst,
			"-o", dst,
			"--enable-simd",
			"--enable-bulk-memory",
			"--strip-dwarf",
			f"-O{4 - mode}",
		], cwd=os.path.abspath(self.path), exit_for_code=True)

		return True
