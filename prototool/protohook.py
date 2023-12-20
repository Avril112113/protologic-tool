import os
import re
from typing import IO

from .simulation import SimulationHook, SimulationFleet


class ProtoHook(SimulationHook):
	RE_FILE_APPEND = re.compile(r"^__protohook__:append:([\w.]+):(.*)$")
	# A trivial list of extensions to exclude, this isn't a solid protection but it's fine, the sim can't exec these anyway.
	ILLEGAL_SUFFIXES = (".exe", ".cmd", ".bat", ".ps1", ".sh")

	files: dict[str, IO]

	def on_start(self, out: str):
		self.files = {}

	def on_stdout(self, fleet: SimulationFleet, line: str, out: str) -> bool:
		if (match := self.RE_FILE_APPEND.fullmatch(line)) is not None:
			filename, data = match.groups()
			if ".." in filename or filename.endswith(self.ILLEGAL_SUFFIXES):
				return False
			filepath = os.path.normpath(os.path.join(out, fleet.get_counted_sim_name(), filename))
			self._get_file(filepath).write(f"{data}\n")
			return True
		return False

	def on_finish(self, out: str):
		self.files.clear()

	def _get_file(self, filepath: str):
		if filepath in self.files:
			return self.files[filepath]
		os.makedirs(os.path.dirname(filepath), exist_ok=True)
		f = open(filepath, "w")
		self.files[filepath] = f
		return f
