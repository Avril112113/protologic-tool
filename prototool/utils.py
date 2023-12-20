import platform
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
