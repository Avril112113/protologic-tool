import inspect
import json
import os
import abc
import shutil
import sys
import tarfile
import zipfile
from glob import iglob
from typing import TYPE_CHECKING

import requests

from ..config import Config
if TYPE_CHECKING:
	from .executable import Executable


class Tool(abc.ABC):
	"""Represents a group of tools, which come as a bundle. (could be a single tool)"""

	def __init__(self, name: str):
		self.name = name
		self.executables: dict[str, "Executable"] = {}
		self.tool_path = os.path.join(Config.TOOLS_PATH, name)
		self._version_dict_path = os.path.join(self.tool_path, ".version_dict.json")

	def add_executable(self, executable: "Executable"):
		assert executable.tool is None
		self.executables[executable.name] = executable
		executable.tool = self
		return self

	def get_executable(self, name: str, error=False):
		if error and name not in self.executables:
			raise ValueError(f"Tool '{self.name}' is missing executable '{name}'")
		return self.executables.get(name, None)

	def __getitem__(self, item: str):
		return self.get_executable(item)

	@abc.abstractmethod
	def _check_update(self, version_dict: dict) -> bool:
		"""
		:param version_dict: Same as returned by update() -> dict
		"""
		raise NotImplementedError()

	def check_update(self) -> bool:
		if self.is_empemeral:
			version_dict = {}
		else:
			version_dict = self._read_version_dict()
		if version_dict is None:
			return True
		return self._check_update(version_dict)

	@abc.abstractmethod
	def _update(self, version_dict: dict, incremental: bool) -> dict|None:
		"""
		:return: Info about the downloaded update, which is used later to check if a new update is available.
		"""
		raise NotImplementedError()

	def update(self, incremental=True) -> bool:
		"""
		:return: Weather or not to output that the tool was downloaded.
		"""
		if self.is_empemeral:
			self._update({}, incremental=incremental)
			return False
		if os.path.exists(self.tool_path) and not self.is_update_inplace:
			shutil.rmtree(self.tool_path)
		os.makedirs(self.tool_path, exist_ok=True)
		version_dict = self._read_version_dict(default={})
		version_dict = self._update(version_dict, incremental=incremental)
		self._write_version_dict(version_dict)
		return True

	@property
	def is_update_inplace(self):
		"""If true, the tool folder isn't deleted before an update."""
		return False

	@property
	def is_empemeral(self):
		"""If true, no folder is created for the tool and `is_downloaded` uses `_check_update`."""
		return False

	def is_downloaded(self):
		if self.is_empemeral:
			return not self._check_update({})
		return os.path.exists(self._version_dict_path)

	def ensure_available(self):
		"""Will ensure the tool is available and download if not, but will not check for updates."""
		if not self.is_downloaded():
			self.update()

	def _read_version_dict(self, default=None) -> dict | None:
		if os.path.isfile(self._version_dict_path):
			with open(self._version_dict_path, "r") as f:
				return json.load(f)
		return default

	def _write_version_dict(self, version_dict: dict):
		with open(self._version_dict_path, "w") as f:
			json.dump(version_dict, f)

	# Tool utilities, not for public use
	def _tutil_path_arg(self, path: str, cwd=None):
		if os.path.isabs(path):
			return path
		return os.path.abspath(os.path.join(cwd if cwd is not None else self.tool_path, path))

	def _tutil_delete(self, path: str, cwd=None):
		path = self._tutil_path_arg(path, cwd)
		if os.path.isdir(path):
			shutil.rmtree(path)
		else:
			os.remove(path)

	def _tutil_move(self, path_from: str, path_to: str, cwd=None):
		path_from = self._tutil_path_arg(path_from, cwd)
		path_to = self._tutil_path_arg(path_to, cwd)
		if "*" in path_from or "?" in path_from:
			for sub in iglob(path_from, recursive=False):
				shutil.move(sub, path_to)
		else:
			shutil.move(path_from, path_to)

	def _tutil_download(self, url: str, out: str, cwd=None, silent=False):
		out = self._tutil_path_arg(out, cwd)
		if not silent:
			print(f"Downloading '{url}' -> '{out}'")
		data_request = requests.get(url)
		data_request.raise_for_status()
		with open(out, "wb") as f:
			f.write(data_request.content)

	def _tutil_extract(self, path: str, out: str, cwd=None, silent=False):
		path = self._tutil_path_arg(path, cwd)
		out = self._tutil_path_arg(out, cwd)
		if not silent:
			print(f"Extracting '{path}' -> '{out}'")
		shutil.unpack_archive(path, out)
		dir_list = os.listdir(out)
		if len(dir_list) == 1:
			dir_path = os.path.join(out, dir_list[0])
			# TODO: Only use `new_dir_path` actually if needed.
			new_dir_path = os.path.join(out, "_tmp")
			shutil.move(dir_path, new_dir_path)
			dir_path = new_dir_path
			for sub in os.listdir(dir_path):
				print(os.path.join(dir_path, sub), "->", os.path.join(out, sub))
				shutil.move(os.path.join(dir_path, sub), os.path.join(out, sub))
			os.rmdir(dir_path)
