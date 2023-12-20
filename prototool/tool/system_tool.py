import os.path

from ..utils import reduce_os_dict, REDUCE_OS
from .tool import Tool
from .executable import Executable


class SystemTool(Tool):
	"""A tool that resides on somewhere on the system and isn't automatically downloaded."""

	is_empemeral = True

	def _check_update(self, version_dict: dict) -> bool:
		return any(not executable.exists for executable in self.executables.values())

	def _update(self, version_dict: dict, incremental: bool):
		for executable in self.executables.values():
			if not executable.exists:
				print(f"Missing '{executable.name}' from '{executable.url if executable.url is not None else '<URL_MISSING>'}'")
			else:
				print(f"Found '{executable.name}' at '{executable.exe_path}'")
