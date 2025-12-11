from unittest.mock import MagicMock
from uuid import uuid4

import across.sdk.v1 as sdk
from across.client.apis import Telescope


class TestGet:
    """
    Unit tests for the `Telescope.get`.

    These tests validate the behavior of the `Telescope` wrapper
    around the Across SDK by mocking out the underlying API calls.
    """

    def test_should_return_telescope(self, fake_telescope: sdk.Telescope) -> None:
        """
        Ensure that `Telescope.get()` returns the expected telescope
        object when the SDK call is mocked.

        Args:
            fake_telescope (sdk.Telescope):
                A mocked `sdk.Telescope` instance returned by the patched API.
        """
        telescope = Telescope(across_client=MagicMock())
        result = telescope.get(str(uuid4()))
        assert result == fake_telescope

    def test_should_be_called_with_value(self, mock_telescope_api: MagicMock) -> None:
        """
        Verify that `Telescope.get()` calls the underlying
        `TelescopeApi.get_telescope()` with the correct
        telescope ID.

        Args:
            mock_telescope_api (MagicMock):
                A mocked instance of `TelescopeApi`.
        """
        id = str(uuid4())
        observatory = Telescope(across_client=MagicMock())
        observatory.get(id)
        mock_telescope_api.get_telescope.assert_called_once_with(telescope_id=id)


class TestGetMany:
    """
    Unit tests for the `Telescope.get_many`.
    """

    def test_should_return_telescopes(self, fake_telescope: sdk.Telescope) -> None:
        """
        Ensure that `Telescope.get_many()` returns a list of
        telescopes when the SDK call is mocked.
        Args:
            fake_telescope (sdk.Telescope):
                A mocked `sdk.Telescope` instance returned by the patched API.
        """
        telescope = Telescope(across_client=MagicMock())
        result = telescope.get_many()
        assert result == [fake_telescope]

    def test_should_optionally_return_instrument_footprints(
        self,
        mock_telescope_api: MagicMock,
    ) -> None:
        """
        Ensure that `Telescope.get_many()` returns instrument footprints
        when `include_footprints` is set to `True`.
        Args:
            mock_telescope_api (MagicMock):
                A mocked instance of `TelescopeApi`.
        """
        telescope = Telescope(across_client=MagicMock())
        telescope.get_many(include_footprints=True)
        call = mock_telescope_api.get_telescopes.call_args_list[0]
        assert call.kwargs["include_footprints"] is True

    def test_should_optionally_return_instrument_filters(
        self,
        mock_telescope_api: MagicMock,
    ) -> None:
        """
        Ensure that `Telescope.get_many()` returns instrument filters
        when `include_filters` is set to `True`.
        Args:
            mock_telescope_api (MagicMock):
                A mocked instance of `TelescopeApi`.
        """
        telescope = Telescope(across_client=MagicMock())
        telescope.get_many(include_filters=True)
        call = mock_telescope_api.get_telescopes.call_args_list[0]
        assert call.kwargs["include_filters"] is True
