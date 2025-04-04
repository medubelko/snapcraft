# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright 2022,2024 Canonical Ltd.
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

"""Unit tests for SnapConfig class."""

from unittest.mock import MagicMock, patch

import pytest
from snaphelpers import SnapCtlError

from snapcraft.snap_config import SnapConfig, get_snap_config


@pytest.fixture
def mock_config():
    with patch(
        "snapcraft.snap_config.SnapConfigOptions", autospec=True
    ) as mock_snap_config:
        yield mock_snap_config


@pytest.fixture()
def mock_is_running_from_snap(mocker):
    yield mocker.patch(
        "snapcraft.snap_config.is_snapcraft_running_from_snap", return_value=True
    )


def test_unmarshal():
    """Verify unmarshalling works as expected."""
    config = SnapConfig.unmarshal({"provider": "lxd"})

    assert config.provider == "lxd"


def test_unmarshal_not_a_dictionary():
    """Verify unmarshalling with data that is not a dictionary raises an error."""
    error = "Project data is not a dictionary"
    with pytest.raises(TypeError, match=error):
        SnapConfig.unmarshal("provider=lxd")  # type: ignore


def test_unmarshal_invalid_provider_error():
    """Verify unmarshalling with an invalid provider raises an error."""
    error = "provider\n  Input should be 'lxd' or 'multipass'"
    with pytest.raises(ValueError, match=error):
        SnapConfig.unmarshal({"provider": "invalid-value"})


def test_unmarshal_extra_data_error():
    """Verify unmarshalling with extra data raises an error."""
    error = "test\n  Extra inputs are not permitted"
    with pytest.raises(ValueError, match=error):
        SnapConfig.unmarshal({"provider": "lxd", "test": "test"})


@pytest.mark.parametrize("provider", ["lxd", "multipass"])
def test_get_snap_config(mock_config, mock_is_running_from_snap, provider):
    """Verify getting a valid snap config."""

    def fake_as_dict():
        return {"provider": provider}

    mock_config.return_value.as_dict.side_effect = fake_as_dict
    config = get_snap_config()

    assert config == SnapConfig(provider=provider)


def test_get_snap_config_empty(mock_config, mock_is_running_from_snap):
    """Verify getting an empty config returns a default SnapConfig."""

    def fake_as_dict():
        return {}

    mock_config.return_value.as_dict.side_effect = fake_as_dict
    config = get_snap_config()

    assert config == SnapConfig()


def test_get_snap_config_not_from_snap(mock_is_running_from_snap):
    """Verify None is returned when snapcraft is not running from a snap."""
    mock_is_running_from_snap.return_value = False

    assert get_snap_config() is None


@pytest.mark.parametrize("error", [AttributeError, SnapCtlError(process=MagicMock())])
def test_get_snap_config_handle_init_error(
    error, mock_config, mock_is_running_from_snap
):
    """An error when initializing the snap config object should return None."""
    mock_config.side_effect = error

    assert get_snap_config() is None


@pytest.mark.parametrize("error", [AttributeError, SnapCtlError(process=MagicMock())])
def test_get_snap_config_handle_fetch_error(
    error, mock_config, mock_is_running_from_snap
):
    """An error when fetching the snap config should return None."""
    mock_config.return_value.fetch.side_effect = error

    assert get_snap_config() is None
