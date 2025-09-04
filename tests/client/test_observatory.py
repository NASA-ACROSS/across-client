from unittest.mock import MagicMock

from across.client.client import Observatory
from across.sdk.v1 import Observatory as sdkObservatory


class TestObservatory:
    """
    Unit tests for the `Observatory` client class.

    These tests validate the behavior of the `Observatory` wrapper
    around the Across SDK by mocking out the underlying API calls.
    """

    def test_get_observatory_should_return_observatory(self, fake_observatory: sdkObservatory) -> None:
        """
        Ensure that `Observatory.get()` returns the expected observatory
        object when the SDK call is mocked.

        Args:
            fake_observatory (sdkObservatory):
                A mocked `sdkObservatory` instance returned by the patched API.
        """
        observatory = Observatory(across_client=MagicMock())
        result = observatory.get("123")
        assert result == fake_observatory

    def test_get_observatory_should_be_called_with_value(self, mock_observatory_api: MagicMock) -> None:
        """
        Verify that `Observatory.get()` calls the underlying
        `ObservatoryApi.get_observatory()` with the correct
        observatory ID.

        Args:
            mock_observatory_api (MagicMock):
                A mocked instance of `ObservatoryApi`.
        """
        observatory = Observatory(across_client=MagicMock())
        observatory.get("123")
        mock_observatory_api.get_observatory.assert_called_once_with(observatory_id="123")

    def test_get_observatories_should_return_observatories(self, fake_observatory: sdkObservatory) -> None:
        """
        Ensure that `Observatory.get_many()` returns a list of
        observatories when the SDK call is mocked.

        Args:
            fake_observatory (sdkObservatory):
                A mocked `sdkObservatory` instance returned by the patched API.
        """
        observatory = Observatory(across_client=MagicMock())
        result = observatory.get_many()
        assert result == [fake_observatory]
