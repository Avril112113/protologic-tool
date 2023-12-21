from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from .prototool import ProtoTool

from .tool import Executable, GithubTool, SystemTool


def add_default_tools(prototool: "ProtoTool"):
	prototool.add_tool(GithubTool("protologic")
		.set_repo("Protologic/Release")
		.set_update_branch(paths=[
			{"Windows": "Sim/Windows", "Linux": "Sim/Linux", "Darwin": "Sim/MacOS"},
			{"Windows": "Player/Windows", "Linux": "Player/Linux", "Darwin": "Player/MacOS"},
		])
		.add_executable(Executable("sim")
			.set_exe({"Windows": "Sim/Windows/Protologic.Terminal.exe", "Linux": "Sim/Linux/Protologic.Terminal", "Darwin": "Sim/MacOS/Protologic.Terminal"})
		)
		.add_executable(Executable("player")
			.set_exe({"Windows": "Player/Windows/SaturnsEnvy.exe", "Linux": "Player/Linux/SaturnsEnvy", "Darwin": "Player/MacOS/build.app/Contents/MacOS/SaturnsEnvy"})
		)
	)

	prototool.add_tool(GithubTool("binaryen")
		.set_repo("WebAssembly/binaryen")
		.set_update_release([{"Windows": "x86_64-windows", "Linux": "x86_64-linux", "Darwin": "x86_64-macos"}])
		.add_executable(Executable("wasm2js")
			.set_exe({"Windows": "bin/wasm2js.exe", "Linux": "bin/wasm2js", "Darwin": "bin/wasm2js"})
		)
		.add_executable(Executable("wasm-as")
			.set_exe({"Windows": "bin/wasm-as.exe", "Linux": "bin/wasm-as", "Darwin": "bin/wasm-as"})
		)
		.add_executable(Executable("wasm-ctor-eval")
			.set_exe({"Windows": "bin/wasm-ctor-eval.exe", "Linux": "bin/wasm-ctor-eval", "Darwin": "bin/wasm-ctor-eval"})
		)
		.add_executable(Executable("wasm-dis")
			.set_exe({"Windows": "bin/wasm-dis.exe", "Linux": "bin/wasm-dis", "Darwin": "bin/wasm-dis"})
		)
		.add_executable(Executable("wasm-emsripten-finalize")
			.set_exe({"Windows": "bin/wasm-emsripten-finalize.exe", "Linux": "bin/wasm-emsripten-finalize", "Darwin": "bin/wasm-emsripten-finalize"})
		)
		.add_executable(Executable("wasm-fuzz-lattices")
			.set_exe({"Windows": "bin/wasm-fuzz-lattices.exe", "Linux": "bin/wasm-fuzz-lattices", "Darwin": "bin/wasm-fuzz-lattices"})
		)
		.add_executable(Executable("wasm-fuzz-types")
			.set_exe({"Windows": "bin/wasm-fuzz-types.exe", "Linux": "bin/wasm-fuzz-types", "Darwin": "bin/wasm-fuzz-types"})
		)
		.add_executable(Executable("wasm-merge")
			.set_exe({"Windows": "bin/wasm-merge.exe", "Linux": "bin/wasm-merge", "Darwin": "bin/wasm-merge"})
		)
		.add_executable(Executable("wasm-metadce")
			.set_exe({"Windows": "bin/wasm-metadce.exe", "Linux": "bin/wasm-metadce", "Darwin": "bin/wasm-metadce"})
		)
		.add_executable(Executable("wasm-opt")
			.set_exe({"Windows": "bin/wasm-opt.exe", "Linux": "bin/wasm-opt", "Darwin": "bin/wasm-opt"})
		)
		.add_executable(Executable("wasm-reduce")
			.set_exe({"Windows": "bin/wasm-reduce.exe", "Linux": "bin/wasm-reduce", "Darwin": "bin/wasm-reduce"})
		)
		.add_executable(Executable("wasm-shell")
			.set_exe({"Windows": "bin/wasm-shell.exe", "Linux": "bin/wasm-shell", "Darwin": "bin/wasm-shell"})
		)
		.add_executable(Executable("wasm-split")
			.set_exe({"Windows": "bin/wasm-split.exe", "Linux": "bin/wasm-split", "Darwin": "bin/wasm-split"})
		)
	)

	prototool.add_tool(GithubTool("wizer")
		.set_repo("bytecodealliance/wizer")
		.set_update_release([{"Windows": "x86_64-windows", "Linux": "x86_64-linux", "Darwin": "x86_64-macos"}])
		.add_executable(Executable("wizer")
			.set_exe({"Windows": "wizer.exe", "Linux": "wizer", "Darwin": "wizer"})
		)
	)

	prototool.add_tool(SystemTool("node")
		.add_executable(Executable("node")
			.find_exe("node")
			.set_url("https://nodejs.org/")
		)
		.add_executable(Executable("npm")
			.find_exe("npm")
			.set_url("https://nodejs.org/")
		)
		.add_executable(Executable("npx")
			.find_exe("npx")
			.set_url("https://nodejs.org/")
		)
	)

	prototool.add_tool(GithubTool("protolua")
		.set_repo("Avril112113/protologic-lua")
		.set_update_release(allow_pre_release=True, paths=[
			"build",
			"lua_template",
			"lua_typing",
		])
	)