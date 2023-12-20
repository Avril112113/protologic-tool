import abc
import os
import re
import sys
from dataclasses import dataclass
from subprocess import PIPE, STDOUT

from .template import Template
from .prototool import ProtoTool


class SimulationHook(abc.ABC):
	def __init__(self, sim: "Simulation"):
		self.sim = sim

	def on_start(self, out: str): pass

	def on_stdout(self, fleet: "SimulationFleet", line: str, out: str) -> bool: pass

	def on_finish(self, out: str): pass


@dataclass(init=True)
class SimulationFleet:
	path: str
	debug = False
	# If this fleet is from a template.
	template: Template|None = None
	_name_index = 0

	def get_counted_sim_name(self) -> str:
		return self.get_sim_name() if self._name_index <= 0 else f"{self.get_sim_name()} ({self._name_index})"

	def get_sim_name(self) -> str:
		return os.path.basename(self.path).replace(".wasm", "").replace(".wat", "")

	def get_fleet_name(self) -> str:
		if self.template is not None:
			return self.template.name
		return self.get_sim_name()


class Simulation:
	"""Handles running a simulation, along with any hooks."""

	RE_FLEET_DEBUG = re.compile(r"^\[.*?\] (.*?): (.*?)\n$")

	def __init__(self, proto: ProtoTool):
		self.proto = proto
		self.proto_tool = proto.get_tool("protologic")
		assert self.proto_tool is not None, "Missing protologic tool?"
		assert self.proto_tool.is_downloaded(), "Tool 'protologic' is not downloaded."
		self.sim_exe = self.proto_tool.get_executable("sim")
		assert self.sim_exe is not None, "Tool 'protologic' is missing executable 'sim'?"
		assert self.sim_exe.exists, "Tool 'protologic' executable 'sim' does not exist."

		self.fleets: list[SimulationFleet] = []  # appended to externally
		self.hooks: list[SimulationHook] = []

	def run(self, out: str, stdout=True) -> bool:
		if len(self.fleets) <= 0:
			raise ValueError("No fleets to simulate.")

		name_counts: dict[str, int] = {}
		fleets_by_sim_name: dict[str, SimulationFleet] = {}
		for fleet in self.fleets:
			sim_name = fleet.get_sim_name()
			count = name_counts.get(sim_name, 0)
			fleet._name_index = count
			name_counts[sim_name] = count + 1
			fleets_by_sim_name[fleet.get_counted_sim_name()] = fleet

		sim_log_path = os.path.join(out, f"sim.log")
		sim_replay_path = os.path.join(out, f"sim.json.deflate")

		os.makedirs(os.path.dirname(sim_log_path), exist_ok=True)
		for hook in self.hooks:
			hook.on_start(out)
		sim_log_file = open(sim_log_path, "w")
		p = self.sim_exe.exec([
			"--output", sim_replay_path.replace(".json.deflate", "", 1),
			"--debug", *["true" if fleet.debug else "false" for fleet in self.fleets],
			"-f", *[fleet.path for fleet in self.fleets],
		], stdout=PIPE, stderr=STDOUT)
		# for loop will end when the sim process exits.
		sim_exception = False
		for line in p.stdout:
			line = line.decode("utf-8")
			# Replace '\r\n' line endings with '\n' (because Windows)
			if line.endswith("\r\n"):
				line = f"{line[:-2]}\n"
			if line.startswith("Unhandled exception."):
				sim_exception = True
			if (match := self.RE_FLEET_DEBUG.fullmatch(line)) is not None and (groups := match.groups())[0] in fleets_by_sim_name:
				if any(hook.on_stdout(fleets_by_sim_name[groups[0]], groups[1], out) for hook in self.hooks):
					continue
			if stdout:
				sys.stdout.write(line)
			sim_log_file.write(line)
			sim_log_file.flush()  # sim isn't instant, flush the changes for live viewing of log file.
		for hook in self.hooks:
			hook.on_finish(out)
		sim_log_file.close()
		return not sim_exception

	def has_hook(self, hook_type: type[SimulationHook]):
		return any(isinstance(hook, hook_type) for hook in self.hooks)
