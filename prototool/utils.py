import platform
import re
from typing import Literal, Iterable, TypeVar


T = TypeVar("T")

OS_STR = Literal["Windows", "Linux", "Darwin"]
REDUCE_OS = T | dict[OS_STR, T]


def reduce_os_dict(path: T | dict[OS_STR, T] | Iterable[T] | Iterable[dict[OS_STR, T]]):
	if isinstance(path, (list, tuple)):
		# reduce iterable.
		return [reduce_os_dict(p) for p in path]
	if isinstance(path, dict):
		# reduce dict with OS as key.
		return path.get(platform.system(), None)
	return path


def file_replace(path: str, repl: dict[str, str]):
	with open(path, "r") as f:
		data = f.read()
	rep = {re.escape(k): v for k, v in repl.items()}
	data = re.sub(
		"|".join(rep.keys()),
		lambda m: rep[re.escape(m.group(0))],
		data
	)
	with open(path, "w") as f:
		f.write(data)
