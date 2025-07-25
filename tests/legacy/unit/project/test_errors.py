# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2018, 2021 Canonical Ltd
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
from snapcraft_legacy.project import errors


class TestErrorFormatting:
    scenarios = [
        (
            "MissingSnapcraftYamlError",
            {
                "exception_class": errors.MissingSnapcraftYamlError,
                "kwargs": {"snapcraft_yaml_file_path": ".snapcraft.yaml"},
                "expected_message": (
                    "Could not find .snapcraft.yaml. Are you sure you are "
                    "in the right directory?\n"
                    "To start a new project, use `snapcraft init`"
                ),
            },
        ),
        (
            "DuplicateSnapcraftYamlError",
            {
                "exception_class": errors.DuplicateSnapcraftYamlError,
                "kwargs": {
                    "snapcraft_yaml_file_path": ".snapcraft.yaml",
                    "other_snapcraft_yaml_file_path": "snapcraft.yaml",
                },
                "expected_message": (
                    "Found a '.snapcraft.yaml' and a 'snapcraft.yaml'.\n"
                    "Please remove one and try again."
                ),
            },
        ),
    ]

    def test_error_formatting(self, exception_class, kwargs, expected_message):
        assert str(exception_class(**kwargs)) == expected_message


def test_SnapcraftExperimentalExtensionsRequiredError():
    error = errors.SnapcraftExperimentalExtensionsRequiredError(extension_name="foo")

    assert (
        error.get_brief()
        == "Experimental extension 'foo' is required, but not enabled."
    )
    assert error.get_details() is None
    assert (
        error.get_resolution()
        == "This extension may be enabled with the '--enable-experimental-extensions' parameter."
    )
    assert error.get_docs_url() is None
    assert error.get_exit_code() == 2


def test_UnsupportedBaseError_core():
    error = errors.UnsupportedBaseError(base="core")

    assert (
        error.get_brief()
        == "Using 'core' as a 'base' or 'build-base' is not supported."
    )
    assert (
        error.get_details()
        == "'core' is currently under Extended Security Maintenance which requires a different version of Snapcraft to run."
    )
    assert (
        error.get_resolution()
        == "Switch to Snapcraft's 4.x channel track or consider upgrading to a newer base."
    )
    assert error.get_docs_url() == "https://documentation.ubuntu.com/snapcraft/stable/how-to/crafting/specify-a-base"
    assert error.get_exit_code() == 2


def test_UnsupportedBaseError_other():
    error = errors.UnsupportedBaseError(base="core100")

    assert (
        error.get_brief()
        == "Using 'core100' as a 'base' or 'build-base' is not supported."
    )
    assert error.get_details() is None
    assert error.get_resolution() == "Ensure a valid base is set in 'snapcraft.yaml'."
    assert error.get_docs_url() == "https://documentation.ubuntu.com/snapcraft/stable/how-to/crafting/specify-a-base"
    assert error.get_exit_code() == 2
