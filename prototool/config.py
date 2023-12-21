import os
import sys
import dotenv


class Config:
	"""
	A config is provided to all other classes in ProtoTool.
	It is used for general configuration, like paths to the base directory and other sub-dirs.
	"""

	# All other paths are based on this.
	# Default: Path to the ran python file, or executable if built with pyinstaller.
	BASE_PATH: str
	# Path for external tools like protologic to be downloaded to.
	TOOLS_PATH: str
	# Path to the 'templates' folder.
	TEMPLATES_PATH: str

	FROZEN = False

	@classmethod
	def update_base_path(cls, path: str):
		cls.BASE_PATH = os.path.abspath(path)
		cls.TOOLS_PATH = os.path.join(cls.BASE_PATH, "tools")
		cls.TEMPLATES_PATH = os.path.join(cls.BASE_PATH, "templates")


if getattr(sys, "frozen", False):
	Config.update_base_path(os.path.dirname(os.path.abspath(sys.executable)))
	Config.FROZEN = True
elif len(sys.argv) > 0 and sys.argv[0].endswith(".py") and os.path.isfile(sys.argv[0]):
	Config.update_base_path(os.path.dirname(os.path.abspath(sys.argv[0])))
else:
	raise FileNotFoundError(f"Failed to set default's for {Config}")


dotenv.load_dotenv(os.path.join(Config.BASE_PATH, ".env"))  # From tool path.
dotenv.load_dotenv()  # default behaviour

