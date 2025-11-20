from across.client import Client
from across.client.apis import (
    Filter,
    Instrument,
    Observation,
    Observatory,
    Schedule,
    Telescope,
    VisibilityCalculator,
)
from across.sdk.v1.api_client_wrapper import ApiClientWrapper


class TestClient:
    """
    Unit tests for the `Client` class.

    These tests validate that the `Client` correctly initializes
    its internal API client and provides access to service objects
    such as `Observatory`.
    """

    def test_client_should_return_client(self) -> None:
        """
        Verify that instantiating a `Client` creates a valid
        `ApiClientWrapper` instance and assigns it to
        `client.across_client`.
        """
        client = Client()
        assert isinstance(client.across_client, ApiClientWrapper)

    def test_client_observatory_should_return_observatory(self) -> None:
        """
        Verify that the `observatory` property of a `Client`
        returns an instance of the `Observatory` service client.
        """
        client = Client()
        assert isinstance(client.observatory, Observatory)

    def test_client_telescope_should_return_telescope(self) -> None:
        """
        Verify that the `telescope` property of a `Client`
        returns an instance of the `Telescope` service client.
        """
        client = Client()
        assert isinstance(client.telescope, Telescope)

    def test_client_instrument_should_return_instrument(self) -> None:
        """
        Verify that the `instrument` property of a `Client`
        returns an instance of the `Instrument` service client.
        """
        client = Client()
        assert isinstance(client.instrument, Instrument)

    def test_client_filter_should_return_filter(self) -> None:
        """
        Verify that the `filter` property of a `Client`
        returns an instance of the `Filter` service client.
        """
        client = Client()
        assert isinstance(client.filter, Filter)

    def test_client_schedule_should_return_schedule(self) -> None:
        """
        Verify that the `schedule` property of a `Client`
        returns an instance of the `Schedule` service client.
        """
        client = Client()
        assert isinstance(client.schedule, Schedule)

    def test_client_observation_should_return_observation(self) -> None:
        """
        Verify that the `observation` property of a `Client`
        returns an instance of the `Observation` service client.
        """
        client = Client()
        assert isinstance(client.observation, Observation)

    def test_client_visibility_calculator_should_return_visibility_calculator(self) -> None:
        """
        Verify that the `VisibilityCalculator` property of a `Client`
        returns an instance of the `VisibilityCalculator` service client.
        """
        client = Client()
        assert isinstance(client.visibility_calculator, VisibilityCalculator)
