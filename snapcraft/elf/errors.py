# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright 2016-2022 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Helpers to parse and handle ELF binary files."""

from pathlib import Path

from snapcraft import errors


class PatcherError(errors.SnapcraftError):
    """Failed to patch an ELF file."""

    def __init__(self, path: Path, *, cmd: list[str], code: int) -> None:
        self.path = path
        self.cmd = cmd
        self.code = code

        super().__init__(f"Error patching ELF file: {cmd} failed with exit code {code}")


class CorruptedElfFile(errors.SnapcraftError):
    """Not a valid ELF file."""

    def __init__(self, path: Path, error: Exception) -> None:
        self.path = path

        super().__init__(f"Error parsing ELF file {str(path)!r}: {str(error)}")


class DynamicLinkerNotFound(errors.SnapcraftError):
    """Failed to find the dynamic linker for this platform."""

    def __init__(self, path: Path) -> None:
        super().__init__(f"Dynamic linker {str(path)!r} not found.")
