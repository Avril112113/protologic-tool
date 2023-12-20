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

	group: Tool|None  # Set when added to a group.

	def __init__(self, name: str):
		self.group = None
		self.name = name
		self.exe_path: str | False = False
		self.url: str | None = None

	def set_exe(self, exe: REDUCE_OS[str]):
		self.exe_path = reduce_os_dict(exe)
		return self

	def find_exe(self, exe: REDUCE_OS[str]):
		self.exe_path = reduce_os_dict(exe)
		path = shutil.which(self.exe_path)
		if path is not None:
			# We lower the extension part, it doesn't matter, but it looks nicer.
			self.exe_path = path[:path.rfind(".")] + path[path.rfind("."):].lower()
		return self

	def set_url(self, url: str):
		self.url = url
		return self

	@property
	def exists(self):
		return os.path.isfile(self.exe_path)

	def exec(self, args: list[str]):
		assert self.group is not None
		if self.exe_path is None:
			raise FileNotFoundError(f"Tool '{self.name}' has not been downloaded.")
		elif self.exe_path is False:
			raise FileNotFoundError(f"Tool '{self.name}' is not supposed to be executed.")
		elif not os.path.isfile(self.exe_path):
			raise FileNotFoundError(f"Tool '{self.name}' is missing '{self.exe_path}'")

		raise NotImplementedError()
