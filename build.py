# https://stackoverflow.com/questions/76145761/use-poetry-to-create-binary-distributable-with-pyinstaller-on-package

import os
import shutil
import platform
import sys
from glob import iglob
from subprocess import Popen, PIPE

import PyInstaller.__main__

base_dir = os.path.dirname(os.path.abspath(__file__))

dist_dir = os.path.join(base_dir, "dist")
templates_dir = os.path.join(base_dir, "templates")

release_dir = os.path.join(base_dir, "release")


def build_executable():
	print(f"Building on {platform.system()}")
	PyInstaller.__main__.run([
		os.path.join(base_dir, "main.py"),
		"--name", "prototool",
		"--onefile",
		"--workpath", f"./build/{platform.system()}",
		"--specpath", "./build/",
	])


def build_copy_release():
	if os.path.exists(release_dir):
		print("WARNING: release directory exists!", file=sys.stderr)
		input("Press enter to continue.")
	os.makedirs(release_dir, exist_ok=True)

	# Copy executables from ./dist/
	if not os.path.isfile(os.path.join(dist_dir, "prototool")):
		print(f"Missing Linux executable!", file=sys.stderr)
	else:
		os_release_dir = os.path.join(release_dir, "Linux")
		os.makedirs(os_release_dir, exist_ok=True)
		shutil.copy(os.path.join(dist_dir, "prototool"), os_release_dir)
		# Copy template data
		for path in iglob(os.path.join(templates_dir, "*", "data")):
			out = os.path.join(os_release_dir, os.path.relpath(path, base_dir))
			shutil.copytree(path, out)

	if not os.path.isfile(os.path.join(dist_dir, "prototool.exe")):
		print(f"Missing Windows executable!", file=sys.stderr)
	else:
		os_release_dir = os.path.join(release_dir, "Windows")
		os.makedirs(os_release_dir, exist_ok=True)
		shutil.copy(os.path.join(dist_dir, "prototool.exe"), os_release_dir)
		# Copy template data
		for path in iglob(os.path.join(templates_dir, "*", "data")):
			out = os.path.join(os_release_dir, os.path.relpath(path, base_dir))
			shutil.copytree(path, out)


def build():
	if shutil.which("wsl") is not None:
		p = Popen(["wsl", "./build_executable.sh"])
		p.wait()
	build_executable()
	build_copy_release()
	print("Release created.")
