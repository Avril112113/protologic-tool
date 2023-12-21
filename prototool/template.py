import abc
import json
import os.path
import re
import shutil
from dataclasses import dataclass
from glob import iglob
from subprocess import Popen
from typing import TYPE_CHECKING, TypedDict, Callable

from .config import Config
if TYPE_CHECKING:
	from .prototool import ProtoTool
	from .simulation import SimulationHook


def _copytree(src: str, dst: str, override: Callable[[str,str], bool]|None = None, _filter: Callable[[str,str], bool]|None = None, mark: Callable[[str,str], None]|None=None):
	for name in os.listdir(src):
		path = os.path.join(src, name)
		out = os.path.join(dst, name)
		if _filter is None or not _filter(path, out):
			if os.path.isfile(path):
				if not os.path.exists(out) or override is None or override(path, out):
					shutil.copy(path, out)
					if mark is not None:
						mark(path, out)
			elif os.path.isdir(path):
				os.makedirs(out, exist_ok=True)
				_copytree(path, out, override, _filter)
				if mark is not None:
					mark(path, out)


@dataclass(init=True)
class TemplateFile:
	src: str  # Glob
	dst: str
	override: bool = False
	ignore: str|None = None  # Pattern to ignore, if src is a directory.


class TemplateConfig(TypedDict):
	template: str
	tools: list[str]
	fleets: list[str | list[str, bool]]
	pre_build: list[list[str]]|None
	post_build: list[list[str]]|None


class Template(abc.ABC):
	# Name just match folder name.
	@property
	@abc.abstractmethod
	def name(self) -> str: raise NotImplementedError()

	@property
	@abc.abstractmethod
	def tools(self) -> list[str]: raise NotImplementedError()

	@property
	@abc.abstractmethod
	def files(self) -> list[TemplateFile]: raise NotImplementedError()

	@property
	@abc.abstractmethod
	def default_fleets(self) -> list[str|list[str, bool]]: raise NotImplementedError()

	@property
	@abc.abstractmethod
	def hooks(self) -> list[type["SimulationHook"]]: raise NotImplementedError()

	@staticmethod
	def get_template_name_from_config(path: str) -> str|None:
		if not path.endswith("prototool.json"):
			path = os.path.join(path, "prototool.json")
		if os.path.isfile(path):
			with open(path, "r") as f:
				return json.load(f).get("template", None)
		else:
			return None

	path: str
	config: TemplateConfig

	def __init__(self, proto: "ProtoTool", path: str):
		assert os.path.isdir(path)
		self.proto = proto
		self.path = path
		self._config_path = os.path.join(self.path, "prototool.json")
		if os.path.relpath(path, "template") == "." and not os.path.isfile(self._config_path):
			raise FileNotFoundError(f"Attempt to create template in current directory.")
		self._read_config()  # Will create config if it doesn't exist.

		self.template_path = os.path.join(Config.TEMPLATES_PATH, self.name)
		self.data_path = os.path.join(self.template_path, "data")

	def upgrade(self, upgrade_msgs=True):
		# Ensure all required tools are in the config
		for tool_name in self.tools:
			if tool_name not in self.config["tools"]:
				self.config["tools"].append(tool_name)
			tool = self.proto.get_tool(tool_name)
			if tool is None:
				raise ValueError(f"Unknown tool '{tool_name}'.")
			if not tool.is_downloaded():
				print(f"Downloading missing tool '{tool.name}'")
				tool.update()
		self._upgrade_pre()
		for tfile in self.files:
			def _override_handler(s: str, d: str):
				if tfile.override:
					if upgrade_msgs:
						print("Updating", d)
					return True
				return False

			path_parts = tfile.src.split("/")
			if path_parts[0] == "data":
				src = os.path.join(self.data_path, os.path.normpath("/".join(path_parts[1:])))
			elif path_parts[0] == "tools":
				src = os.path.join(Config.TOOLS_PATH, os.path.normpath("/".join(path_parts[1:])))
			else:
				raise FileNotFoundError(f"Template invalid src '{path_parts[0]}'")
			dst = os.path.join(self.path, os.path.normpath(tfile.dst))
			for path in iglob(src, recursive=True):
				if os.path.isfile(path):
					if os.path.exists(tfile.dst):
						if tfile.override:
							if upgrade_msgs:
								print("Updating", dst)
						else:
							continue
					shutil.copy(path, dst)
				elif os.path.isdir(path):
					_copytree(path, dst, override=_override_handler)
		self._upgrade_post()
		self._write_config()

	def build(self, mode: int=0) -> bool:
		# run pre-build scripts from config
		pre_builds = self.config.get("pre_build", None)
		if pre_builds is not None:
			print("Running pre-build actions...")
			for pre_build in pre_builds:
				print(f"~ {' '.join(pre_build)}")
				args = list(pre_build)
				if re.match(r"^tools[\\/]", args[0]):
					args[0] = re.sub(r"^tools[\\/]", re.escape(Config.TOOLS_PATH + os.path.sep), args[0])
				p = Popen(args, shell=True, cwd=self.path)
				p.wait()
				if p.returncode != 0:
					print(f"Returned code: {p.returncode}")
					return False
		# run template build
		ok = self._build(mode)
		# run post-build scripts from config
		post_builds = self.config.get("post_build", None)
		if post_builds is not None:
			print("Running post-build actions...")
			for post_build in post_builds:
				print(f"~ {' '.join(post_build)}")
				args = list(post_build)
				if re.match(r"^tools[/\\]", args[0]):
					args[0] = re.sub(r"^tools[\\/]", re.escape(Config.TOOLS_PATH + os.path.sep), args[0])
				p = Popen(args, shell=True, cwd=self.path)
				p.wait()
				if p.returncode != 0:
					print(f"Returned code: {p.returncode}")
					return False
		return ok

	def _read_config(self):
		if not os.path.isfile(self._config_path):
			# noinspection PyTypeChecker
			self.config = {}
			self._ensure_config()
			self._write_config()
			return
		with open(self._config_path, "r") as f:
			self.config = json.load(f)
		self._ensure_config()

	def _write_config(self):
		with open(self._config_path, "w") as f:
			json.dump(self.config, f, indent="\t")

	def _ensure_config(self):
		self.config.setdefault("template", self.name)
		self.config.setdefault("tools", self.tools)
		self.config.setdefault("fleets", self.default_fleets)

	# Overrideable method for template upgrade
	def _upgrade_pre(self): pass

	# Overrideable method for template upgrade
	def _upgrade_post(self): pass

	# Overrideable method for build action
	def _build(self, mode: int) -> bool: return True
