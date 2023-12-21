# ProtoTool for ProtoLogic
A general-purpose tool for managing tools and creating new [protologic](https://github.com/Protologic/Release) fleets.  

What this tool does:  
- Manage tools, like protologic sim & player and binaryen.  
- Check for and update tools.   
- Create new fleets from templates, see [templates](#templates).  
- Run the sim with [additional debug features](#sim-hooks).  
- Run the player.  


## prototool.json
A directory containing `prototool.json` is a valid fleet.  
The format of this file is described below.  
Comments are not valid, but are used here to explain things.  
```json
{
	// Name of the template.
	"template": "blank",
	// Tools to downloaded
	"tools": [
		"protologic",
		"binaryen"
	],
	// Fleets to be simulated if this project is the sim path.
	"fleets": [
		"build/release.wasm",
		// You can also force debug mode.
		["build/release.wasm", true]
	],
	// NOTE: blank template does nothing on build, you can use these instead.
	// A list of commands to run before building.
	"pre_build": [
		["echo", "Pre build action"]
	],
	// A list of commands to run after building.
	"post_build": [
		["echo", "Post build action"],
		// You can also use downloaded tools.
		// Note: If you need to use a local directory, use `./tools` instead.
		["tools/binaryen/wasm-opt", "build/release.wasm", "-O4"]
	]
}
```


## Templates
Currently, there is only 3 templates (`prototool template list`).  
- `blank` - Simple blank template.  
- `assemblyscript` - [AssemblyScript](https://www.assemblyscript.org/), very similar to TypeScript.  [Avril112113/protologic-tool-assemblyscript](https://github.com/Avril112113/protologic-tool-assemblyscript)    
- `protolua` - Lua. [Avril112113/protologic-lua](https://github.com/Avril112113/protologic-lua)  

If you use a different language or setup, use the blank template and setup `"pre_build"` actions.  
*A `rust` template may be added in the future*  


## Sim Hooks
When a sim is run through ProtoTool, templates can add hooks to the log output.  
These allow for additional debugging features.  
There is also ProtoHook which is active by default, unless `--no-hook` is specified.  
See [ProtoHook usage](#protohook-usage) for what it can provide.  

Using hooks is as simple as printing to the sim output when the fleet is in debug mode.  


### ProtoHook usage
The following are available when using the ProtoHook.  

`__protohook__:append:<FILE_NAME>:<DATA>`  
Where `<FILE_NAME>` is a name of a file and `<DATA>` is a line to write to that file.  


## Using or Building from source.
If you want to simply use this tool, check the [releases](https://github.com/Avril112113/protologic-tool/releases).  

Ensure you have [python](https://www.python.org/) 3.10 or greater available.  
Ensure you have [poetry](https://python-poetry.org/) available.  

Run `poetry env use 3.10` create/use a python env.  
Run `poetry install` to install dependencies.  
Test with `poetry run python main.py`  

To build executables;  
run `poetry run build` to create a release.  
If `wsl` is available, a linux build will be created as well.  
Ensure the same is setup in wsl.  
