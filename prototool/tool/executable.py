import os
import abc
import shutil
from subprocess import Popen

from ..utils import reduce_os_dict, REDUCE_OS
from .tool import Tool


class Executable(abc.ABC):
	"""
	Represents a config for an external tool.
	Creating a new Tool object should not do anything, only it's methods should perform actions.
	"""

	tool: Tool | None  # Set when added to a group.

	def __init__(self, name: str):
		self.tool = None
		self.name = name
		self._exe_path: str | None = None
		self._required_args: list[str] | None = None
		self.url: str | None = None

	def set_exe(self, exe: REDUCE_OS[str], required_args: list[REDUCE_OS[str]]=None):
		self._exe_path = reduce_os_dict(exe)
		self._required_args = required_args
		return self

	def find_exe(self, exe: REDUCE_OS[str]):
		self._exe_path = reduce_os_dict(exe)
		path = shutil.which(self._exe_path)
		if path is not None:
			# We lower the extension part, it doesn't matter, but it looks nicer.
			self._exe_path = path[:path.rfind(".")] + path[path.rfind("."):].lower()
		return self

	@property
	def exe_path(self) -> str:
		assert self._exe_path is not None
		return os.path.join(self.tool.tool_path, self._exe_path)

	def get_exec_args(self) -> list[str]:
		"""Get the base exec arguments, first being the executable to run and any required args."""
		return [self.exe_path, *(self._required_args if self._required_args is not None else tuple())]

	def get_shell_args(self, rel: str = None) -> list[str]:
		"""Same as get_exec_args, but prettier."""
		path = self.exe_path
		# FIXME: shutil.which(...) is not None, could be pointing to a different file.
		if shutil.which(os.path.basename(path)) is not None:
			path = os.path.basename(path)
		elif rel is not None:
			path = os.path.relpath(path, rel)
		return [path, *(self._required_args if self._required_args is not None else tuple())]

	def set_url(self, url: str):
		self.url = url
		return self

	@property
	def exists(self):
		return self._exe_path is not None and os.path.isfile(self.exe_path)

	def exec(self, args: list[str], wait=True, raise_for_code=True, exit_for_code=False, **kwargs):
		assert self.tool is not None, f"Executable '{self.name}' is not associated with a tool."
		if not self.tool.is_downloaded():
			raise FileNotFoundError(f"Tool '{self.tool.name}' is not downloaded.")
		elif self._exe_path is None or not os.path.isfile(self.exe_path):
			raise FileNotFoundError(f"Tool '{self.name}' is missing '{self.exe_path}'")
		p = Popen([*self.get_exec_args(), *args], **kwargs)
		if wait:
			p.wait()
			if exit_for_code and p.returncode != 0:
				exit(p.returncode)
			elif raise_for_code and p.returncode != 0:
				raise ValueError(f"Return code: {p.returncode}")
		return p
