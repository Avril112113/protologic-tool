from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from .prototool import ProtoTool

from templates import *


def add_default_templates(prototool: "ProtoTool"):
	prototool.add_template(BlankTemplate)
