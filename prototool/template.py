import abc
import json
import os.path
import shutil
from typing import TYPE_CHECKING, TypedDict, Callable

if TYPE_CHECKING:
	from prototool import ProtoTool
from prototool.config import Config


def _copytree(src: str, dst: str, override: Callable[[str,str], bool]|None):
	for name in os.listdir(src):
		path = os.path.join(src, name)
		out = os.path.join(dst, name)
		if os.path.isfile(path):
			if override is None or not os.path.exists(out) or override(path, out):
				shutil.copy(path, out)
		elif os.path.isdir(path):
			os.makedirs(out, exist_ok=True)
			_copytree(path, out, override)


class TemplateConfig(TypedDict):
	template: str
	tools: list[str]


class Template(abc.ABC):
	# Name just match folder name.
	@property
	@abc.abstractmethod
	def name(self) -> str: raise NotImplementedError()

	@property
	@abc.abstractmethod
	def tools(self) -> list[str]: raise NotImplementedError()

	# Files to override during an upgrade.
	@property
	@abc.abstractmethod
	def upgrade_files(self) -> list[str]: raise NotImplementedError()

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

	@staticmethod
	def get_template_name_from_config(path: str) -> str|None:
		if not path.endswith("prototool.json"):
			path = os.path.join(path, "prototool.json")
		with open(path, "r") as f:
			return json.load(f).get("template", None)

	def upgrade(self):
		def _override_filter(src, dst) -> bool:
			if dst.replace("\\", "/") in self.upgrade_files:
				print(f"Overriding '{dst}'")
				return True
			return False

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
		_copytree(self.data_path, self.path, override=_override_filter)
		self._upgrade_post()
		self._write_config()

	def _read_config(self):
		if not os.path.isfile(self._config_path):
			# noinspection PyTypeChecker
			self.config = {}
			self._set_default_config()
			self._write_config()
			return
		with open(self._config_path, "r") as f:
			self.config = json.load(f)

	def _write_config(self):
		with open(self._config_path, "w") as f:
			json.dump(self.config, f, indent="\t")

	def _set_default_config(self):
		self.config["template"] = self.name
		self.config["tools"] = self.tools

	# Overrideable method for template upgrade
	def _upgrade_pre(self): pass

	# Overrideable method for template upgrade
	def _upgrade_post(self): pass
