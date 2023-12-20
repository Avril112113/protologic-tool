import os.path
import shutil
import sys
import argparse
import dotenv

from prototool.config import Config

dotenv.load_dotenv(os.path.join(Config.BASE_PATH, ".env"))  # From tool path.
dotenv.load_dotenv()  # default behaviour

from prototool import ProtoTool, Template
from prototool.simulation import Simulation, SimulationFleet


PROTOTOOL_VERSION = "0.1.0"


# :sigh: argparse can be, less than readable sometimes.
cli = argparse.ArgumentParser(prog="prototool", description="""
A tool to manage ProtoLogic tools and fleets.
This tool can create new fleet projects from templates using `prototool new`.

If you encounter rate limit issues, or want incremental updates for some tools, set the `GITHUB_TOKEN` environment variable.
You can generate one from https://github.com/settings/tokens, it needs no permissions.
'.env' file is loaded if found in CWD or next to prototool executable.

Repo: https://github.com/Avril112113/protologic-tool
""", formatter_class=argparse.RawTextHelpFormatter)

# ~ action ~
cli_action = cli.add_subparsers(dest="action", required=True)

# ~ version
cli_actions_version = cli_action.add_parser("version", help="Gets the current version of ProtoTool.")

# ~ tool
cli_actions_tool = cli_action.add_parser("tool", help="Manage installed tools.")

# ~~ tool_action ~~
cli_actions_tool_action = cli_actions_tool.add_subparsers(dest="tool_action", required=True)

# ~~ list
cli_actions_tool_action_list = cli_actions_tool_action.add_parser("list", help="Lists all downloaded tools.")
cli_actions_tool_action_list.add_argument("--all", "-a", action="store_true", help="List all available tools.")
cli_actions_tool_action_list.add_argument("--detailed", "-d", action="store_true", help="List executables a tool provides.")

# ~~ update
cli_actions_tool_action_update = cli_actions_tool_action.add_parser("update", help="Update a tool if an update is available.")
cli_actions_tool_action_update.add_argument("name", help="Name of the tool to update.")
cli_actions_tool_action_update.add_argument("--full", help="Force full update instead of incremental.")

# ~~ update_all
cli_actions_tool_action_update_all = cli_actions_tool_action.add_parser("update_all", help="Check for updates to all downloaded tools.")

# ~~ delete
cli_actions_tool_action_delete = cli_actions_tool_action.add_parser("delete", help="Delete a tool.")
cli_actions_tool_action_delete.add_argument("name", help="Name of the tool to delete.")

# ~ template
cli_actions_template = cli_action.add_parser("template", help="Template management.")

# ~~ template_action ~~
cli_actions_template_action = cli_actions_template.add_subparsers(dest="template_action", required=True)

# ~~ list ~~
cli_actions_template_action_list = cli_actions_template_action.add_parser("list", help="List available templates.")

# ~ new
cli_actions_new = cli_action.add_parser("new", help="Create a new fleet.")
cli_actions_new.add_argument("path", help="The path to the new fleet.")
cli_actions_new.add_argument("template", help="The template for the new fleet.")
cli_actions_new.add_argument("--delete", action="store_true", help=argparse.SUPPRESS)

# ~ upgrade
cli_actions_upgrade = cli_action.add_parser("upgrade", help="Update a fleet from it's template.")

# ~ sim
cli_actions_sim = cli_action.add_parser("sim", help="Simulate a battle.")
cli_actions_sim.add_argument("--out", default="./sim", help="Directory to save simulation log and replay.")
cli_actions_sim.add_argument("--play", action="store_true", help="Plays the replay in the player once simulated.")
cli_actions_sim.add_argument("path", nargs="*", help="Path to a fleet (directory containing or path to '.wasm').")
cli_actions_sim.add_argument("--debug", "-d", action="append", help="Enable debug for the fleet.")

# ~ play
cli_actions_sim = cli_action.add_parser("play", help="Plays a reply in the player for preview.")
cli_actions_sim.add_argument("path", nargs="?", default=".", help="Path to replay (directory containing or directly to '.json.deflate').")


def _helper_get_template(proto: ProtoTool, path: str) -> Template|None:
	template_name = Template.get_template_name_from_config(path)
	template_type = proto.get_template(template_name)
	if template_type is None:
		print(f"Unknown template '{template_name}'.", file=sys.stderr)
		return None
	return template_type(proto, path)


def _cli_actions_tool_list(proto: ProtoTool, downloaded_only=True, detailed=False):
	if downloaded_only:
		print("Downloaded tools:")
		ordered_tools = sorted(filter(lambda t: t.is_downloaded(), proto.tools.values()), key=lambda t: t.name)
	else:
		print("Available tools:")
		ordered_tools = sorted(proto.tools.values(), key=lambda t: (not t.is_downloaded(), t.name))
	for tool in ordered_tools:
		print(f"  {tool.name}{' (downloaded)' if not downloaded_only and tool.is_downloaded() else ''}")
		if detailed:
			for executable in tool.executables.values():
				print(f"  - {executable.name}")


def _cli_actions_tool_update(proto: ProtoTool, name: str, incremental=True):
	tool = proto.get_tool(name)
	if tool is None:
		print(f"Unknown tool '{name}'.", file=sys.stderr)
		exit(-1)
	elif tool.is_downloaded() and not tool.check_update():
		print(f"No update found for '{name}'.")
		return
	was_downloaded = tool.is_downloaded()
	if tool.update(incremental=incremental):
		if not was_downloaded:
			print(f"Tool '{name}' downloaded.")
		else:
			print(f"Tool '{name}' updated.")


def _cli_actions_tool_delete(proto: ProtoTool, name: str):
	tool = proto.get_tool(name)
	if tool is None:
		print(f"Unknown tool '{name}'.", file=sys.stderr)
		exit(-1)
	elif not tool.is_downloaded():
		print(f"Tool '{name}' not downloaded.", file=sys.stderr)
		exit(-1)
	shutil.rmtree(tool.tool_path)
	print(f"Tool '{name}' deleted.")


def _cli_actions_tool_update_all(proto: ProtoTool):
	print(f"Checking for updates to all downloaded tools.")
	for tool in proto.tools.values():
		if tool.is_downloaded():
			if tool.check_update():
				print(f"  Updating '{tool.name}'")
				tool.update()
			else:
				print(f"  No update for '{tool.name}'")


def _cli_actions_template_list(proto: ProtoTool):
	print("Available templates:")
	for template in proto.templates.values():
		print(f"  - {template.name}")


def _cli_actions_new(proto: ProtoTool, template_name: str, path: str):
	template_type = proto.get_template(template_name)
	if template_type is None:
		print(f"Unknown template '{template_name}'.", file=sys.stderr)
		exit(-1)
	elif os.path.exists(path):
		print(f"Path exists '{path}', ensure a non-existent path.", file=sys.stderr)
		exit(-1)
	os.makedirs(path)
	template: Template = template_type(proto, path)
	template.upgrade()


def _cli_actions_upgrade(proto: ProtoTool):
	template = _helper_get_template(proto, ".")
	if template is None: return
	template.upgrade()


def _cli_actions_sim(proto: ProtoTool, out: str, fleets: list[str], debug: list[str], stdout=True) -> bool:
	sim = Simulation(proto)

	def add_path(fleet_path: str, fleet_debug: bool) -> bool:
		if os.path.isfile(fleet_path):
			fleet = SimulationFleet(fleet_path)
			fleet.debug = fleet_debug
			sim.fleets.append(fleet)
			return True
		elif os.path.isdir(fleet_path):
			template = _helper_get_template(proto, fleet_path)
			if template is None:
				print(f"Fleet '{fleet_path}' not found.", file=sys.stderr)
				return False
			# FIXME: We could end up in infinite recursion.
			for sub_fleet in template.config.get("fleets", []):
				if isinstance(sub_fleet, list):
					sub_fleet_path, sub_fleet_debug = sub_fleet
				else:
					sub_fleet_path, sub_fleet_debug = sub_fleet, False
				if sub_fleet_debug is None:
					sub_fleet_debug = fleet_debug
				add_path(sub_fleet_path, sub_fleet_debug)
		else:
			print(f"Fleet '{fleet_path}' not found.", file=sys.stderr)
			return False
		return False

	for path in fleets + debug:
		add_path(path, path in debug)

	if len(sim.fleets) <= 0:
		print(f"Simulation not run, missing fleets to simulate.", file=sys.stderr)
		return False

	print("Starting simulation.")
	first = True
	for sim_fleet in sim.fleets:
		print(f"{'   ' if first else 'vs '}{sim_fleet.get_fleet_name()}{'  (debug enabled)' if sim_fleet.debug else ''}")
		first = False
	try:
		return sim.run(out, stdout=stdout)
	except KeyboardInterrupt:
		print("Simulation interrupted.", file=sys.stderr)
		return False


def _cli_actions_play(proto: ProtoTool, path: str):
	proto_tool = proto.get_tool("protologic")
	assert proto_tool is not None, "Missing protologic tool?"
	assert proto_tool.is_downloaded(), "Tool 'protologic' is not downloaded."
	player_exe = proto_tool.get_executable("player")
	assert player_exe is not None, "Tool 'protologic' is missing executable 'player'?"
	assert player_exe.exists, "Tool 'protologic' executable 'player' does not exist."

	if os.path.isdir(path):
		replays = list(os.path.join(path, file) for file in os.listdir(path) if file.endswith(".json.deflate"))
		if len(replays) <= 0:
			template = _helper_get_template(proto, path)
			if template is None:
				print(f"Invalid replay file or sim or fleet directory.", file=sys.stderr)
				return
			path = os.path.join(path, "sim")
			replays = list(os.path.join(path, file) for file in os.listdir(path) if file.endswith(".json.deflate"))
		if len(replays) == 1:
			path = replays[0]
		elif len(replays) > 1:
			print(f"Found multiple replays in directory.", file=sys.stderr)
			return
	if not os.path.isfile(path) or not path.endswith(".json.deflate"):
		print(f"Invalid replay file or sim directory.", file=sys.stderr)
		return

	print(f"Starting player '{path}'")
	player_exe.exec([os.path.abspath(path)])


def main():
	args = cli.parse_args()
	proto = ProtoTool()

	if args.action == "version":
		print(f"ProtoTool version: {PROTOTOOL_VERSION}")
	elif args.action == "tool":
		if args.tool_action == "list":
			_cli_actions_tool_list(proto, not args.all, args.detailed)
		elif args.tool_action == "delete":
			_cli_actions_tool_delete(proto, args.name)
		elif args.tool_action == "update":
			_cli_actions_tool_update(proto, args.name, incremental=args.full)
		elif args.tool_action == "update_all":
			_cli_actions_tool_update_all(proto)
		else:
			print(f"ERROR: unhandled tool_action '{args.tool_action}'", file=sys.stderr)
	elif args.action == "template":
		if args.template_action == "list":
			_cli_actions_template_list(proto)
		else:
			print(f"ERROR: unhandled tool_action '{args.tool_action}'", file=sys.stderr)
	elif args.action == "new":
		if args.delete and os.path.exists(args.path):
			shutil.rmtree(args.path)
		_cli_actions_new(proto, args.template, args.path)
	elif args.action == "upgrade":
		_cli_actions_upgrade(proto)
	elif args.action == "sim":
		if len(args.path) <= 0 and (args.debug is None or len(args.debug) <= 0):
			args.path.append(".")
		sim_ok = _cli_actions_sim(proto, args.out, args.path, args.debug if args.debug else [])
		if sim_ok and args.play:
			_cli_actions_play(proto, args.out)
		if not sim_ok:
			exit(-1)
	elif args.action == "play":
		_cli_actions_play(proto, args.path)
	else:
		print(f"ERROR: unhandled action '{args.action}'", file=sys.stderr)


if __name__ == "__main__":
	main()
