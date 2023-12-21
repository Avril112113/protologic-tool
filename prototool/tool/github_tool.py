import base64
import os
from datetime import datetime
from typing import Iterable

from github import Github, Auth
from github.GitReleaseAsset import GitReleaseAsset

from ..utils import reduce_os_dict, REDUCE_OS
from .tool import Tool


class GithubTool(Tool):
	"""A tool that resides on GitHub."""
	__gh = Github(auth=Auth.Token(os.getenv("GITHUB_TOKEN")) if os.getenv("GITHUB_TOKEN") else None)  # Global public GitHub instance.

	gh_repo: str
	gh_update_release: Iterable[str]|bool|None
	gh_update_branch: str|None
	gh_update_paths: str  # Path either within the release, or the branch.
	gh_allow_pre_release: bool|None

	def set_repo(self, repo: str):
		self.gh_repo = repo
		return self

	def set_update_release(self, name_contains: Iterable[REDUCE_OS[str]] = True, paths: Iterable[REDUCE_OS[str]] = ("*",), allow_pre_release=False):
		"""Set to update from releases."""
		self.gh_update_branch = None
		self.gh_update_release = reduce_os_dict(name_contains)
		self.gh_update_paths = reduce_os_dict(paths)
		self.gh_allow_pre_release = allow_pre_release
		return self

	def set_update_branch(self, branch="master", paths: Iterable[REDUCE_OS[str]] = (".",)):
		"""Set to update from a branch."""
		self.gh_update_release = None
		self.gh_update_branch = branch
		self.gh_update_paths = reduce_os_dict(paths)
		return self

	def _check_update(self, version_dict: dict) -> bool:
		if self.gh_update_release is not None:
			return self._check_update_release(version_dict)
		elif self.gh_update_branch is not None:
			return self._check_update_branch(version_dict)
		else:
			raise ValueError(f"Tool '{self.name}' is missing update configuration.")

	def _update(self, version_dict: dict, incremental: bool) -> dict:
		if self.gh_update_release is not None:
			return self._update_from_release(version_dict)
		elif self.gh_update_branch is not None:
			return self._update_from_branch(version_dict, incremental)
		else:
			raise ValueError(f"Tool '{self.name}' is missing update configuration.")

	@property
	def is_update_inplace(self):
		return self.gh_update_branch is not None

	def _get_release_asset(self) -> GitReleaseAsset:
		# Cache between multiple calls, since this will be called potentially from _check_update and _update.
		if hasattr(self, "__gh_release_asset"):
			return self.__gh_release_asset
		repo = self.__gh.get_repo(f"{self.gh_repo}")
		release = next((
			release for release in repo.get_releases()
			if self.gh_allow_pre_release or not release.prerelease
		), None)
		if release is None:
			raise FileNotFoundError(f"Failed to find applicable release.\nAllowPreRelease={self.gh_allow_pre_release}")
		assets = list(
			asset for asset in release.assets
			if self.gh_update_release is True or all(part in asset.name for part in self.gh_update_release)
			if not asset.name.endswith("sha256")
		)
		if len(assets) <= 0:
			raise FileNotFoundError(f"Failed to find applicable asset from release.\nNone contains all: {self.gh_update_release}")
		elif len(assets) >= 2:
			raise FileExistsError(f"Found multiple applicable assets from release.\nAssets: {list(asset.name for asset in assets)}")
		self.__gh_release_asset = assets[0]
		return assets[0]

	def _check_update_release(self, version_dict: dict) -> bool:
		asset = self._get_release_asset()
		current = datetime.fromisoformat(version_dict.get("asset.last_modified", datetime.fromtimestamp(0)))
		return current < asset.updated_at

	def _update_from_release(self, version_dict: dict) -> dict:
		asset = self._get_release_asset()
		self._tutil_download(asset.browser_download_url, asset.name)
		self._tutil_extract(asset.name, "_tmp")
		self._tutil_delete(asset.name)
		for path in self.gh_update_paths:
			self._tutil_move(os.path.join("_tmp", path), ".")
		self._tutil_delete("_tmp")
		return {
			"asset.last_modified": asset.updated_at.isoformat()
		}

	def _check_update_branch(self, version_dict: dict) -> bool:
		repo = self.__gh.get_repo(f"{self.gh_repo}")
		branch = repo.get_branch(self.gh_update_branch)
		return branch.commit.sha != version_dict.get("commit.sha")

	def _update_from_branch(self, version_dict: dict, incremental: bool) -> dict:
		rate_remaining = self.__gh.get_rate_limit().core.remaining
		repo = self.__gh.get_repo(f"{self.gh_repo}")
		branch = repo.get_branch(self.gh_update_branch)
		files_sha = version_dict.get("file.sha", {})
		if not incremental or rate_remaining < 500 or len(files_sha) == 0:
			# Do a full download to prevent a rate limit.
			reason = "Initial" if len(files_sha) == 0 else "Avoiding rate limit, set GITHUB_TOKEN env for incremental updates."
			print(f"Full archive download ({reason})")
			# Not using repo.get_archive_link(), as it's another api call :/
			archive_url = repo.archive_url.replace("{archive_format}", "zipball").replace("{/ref}", f"/{branch.name}")
			self._tutil_download(archive_url, f"{branch.name}.zip")
			self._tutil_extract(f"{branch.name}.zip", "_tmp")
			for path in self.gh_update_paths:
				path = os.path.normpath(path)
				self._tutil_move(os.path.join("_tmp", path), path)
			self._tutil_delete("_tmp")
			self._tutil_delete(f"{branch.name}.zip")
			tree = repo.get_git_tree(branch.name, recursive=True)
			if tree.raw_data["truncated"]:
				raise ValueError("Unhandled: truncated GitTree.")
			for element in tree.tree:
				files_sha[element.path] = element.sha
		else:
			# Incremental update
			# It might cost more on api calls, but overall less data to download.
			print(f"Incremental file update")
			for path in self.gh_update_paths:
				if "*" in path or "?" in path:
					raise NotImplementedError("Glob patterns are not supported for github branch update.")
				else:
					contents = repo.get_contents(path, ref=branch.name)
					if not isinstance(contents, list):
						contents = [contents]
				has_downloaded_item = False
				for content in contents:
					content_path = f"{path}/{content.name}"
					if files_sha.get(content_path, None) == content.sha:
						continue
					out = os.path.join(self.tool_path, os.path.normpath(content_path))
					os.makedirs(os.path.dirname(out), exist_ok=True)
					if content.encoding == "base64":
						with open(out, "wb") as f:
							f.write(content.decoded_content)
						has_downloaded_item = True
						files_sha[content_path] = content.sha
					elif content.download_url is not None:
						self._tutil_download(content.download_url, out, silent=True)
						has_downloaded_item = True
						files_sha[content_path] = content.sha
					elif content.type == "dir":
						tree = repo.get_git_tree(content.sha, recursive=True)
						if tree.raw_data["truncated"]:
							raise ValueError("Unhandled: truncated GitTree.")
						for element in tree.tree:
							if files_sha.get(element.path) == element.sha:
								continue
							if element.type == "blob":
								blob = repo.get_git_blob(element.sha)
								if blob.encoding == "base64":
									with open(out, "wb") as f:
										f.write(base64.b64decode(bytearray(blob.content, "utf-8")))
									has_downloaded_item = True
									files_sha[element.path] = element.sha
								else:
									raise ValueError(f"Unhandled encoding '{blob.encoding}'")
						files_sha[content_path] = content.sha
					else:
						raise ValueError(f"Failed to download '{content.name}', unsupported content type '{content.type}'")
				if has_downloaded_item:
					print(f"- Updated '{path}'")
				else:
					print(f"- No updates for '{path}'")
		return {
			"commit.sha": branch.commit.sha,
			"file.sha": files_sha
		}
