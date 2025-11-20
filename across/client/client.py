import across.sdk.v1 as sdk
from across.sdk.v1.abstract_credential_storage import CredentialStorage
from across.sdk.v1.api_client_wrapper import ApiClientWrapper

from .apis import Filter, Instrument, Observation, Observatory, Schedule, Telescope, VisibilityCalculator
from .core.config import config


class Client:
    """
    Client wrapper for interacting with the Across API.

    This class initializes an API client using either direct credentials
    (`client_id`, `client_secret`) or a stored credentials object
    (`CredentialStorage`). It exposes higher-level service objects,
    such as the SSA objects for the across-server
    """

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        creds_store: CredentialStorage | None = None,
    ):
        """
        Initialize a Client instance for the Across API.

        Credentials can be provided through the following resolution order:
          1. Direct arguments to the Client constructor.
          2. Credential Storage interface.
          3. Environment variables: `ACROSS_SERVER_ID` and `ACROSS_SERVER_SECRET`
        Args:
            client_id (str | None, optional):
                The client ID used for authentication.
            client_secret (str | None, optional):
                The client secret used for authentication.
            credentials (CredentialStorage | None, optional):
                A credentials storage object that can provide authentication
                tokens. If provided, it takes precedence over `client_id`
                and `client_secret`.
        """
        configuration = sdk.Configuration(host=config.HOST, username=client_id, password=client_secret)
        self.across_client = ApiClientWrapper.get_client(configuration=configuration, creds=creds_store)

        # configuration.access_token needs to be populated
        self.across_client.refresh()

    @property
    def observatory(self) -> Observatory:
        """
        Get an `Observatory` instance for interacting with the API.

        The `Observatory` provides methods to query observatory-related resources in the Across API.

        Returns:
            Observatory: An initialized `Observatory` client bound to
            this Client’s API session.
        """
        return Observatory(self.across_client)

    @property
    def telescope(self) -> Telescope:
        """
        Get an `Telescope` instance for interacting with the API.

        The `Telescope` provides methods to query telescope-related resources in the Across API.

        Returns:
            Telescope: An initialized `Telescope` client bound to
            this Client’s API session.
        """
        return Telescope(self.across_client)

    @property
    def instrument(self) -> Instrument:
        """
        Get an `Instrument` instance for interacting with the API.

        The `Instrument` provides methods to query instrument-related resources in the Across API.

        Returns:
            Instrument: An initialized `Instrument` client bound to
            this Client’s API session.
        """
        return Instrument(self.across_client)

    @property
    def filter(self) -> Filter:
        """
        Get an `Filter` instance for interacting with the API.

        The `Filter` provides methods to query filter-related resources in the Across API.

        Returns:
            Filter: An initialized `Filter` client bound to
            this Client’s API session.
        """
        return Filter(self.across_client)

    @property
    def schedule(self) -> Schedule:
        """
        Get an `Schedule` instance for interacting with the API.

        The `Schedule` provides methods to query schedule-related resources in the Across API.

        Returns:
            Schedule: An initialized `Schedule` client bound to
            this Client’s API session.
        """
        return Schedule(self.across_client)

    @property
    def observation(self) -> Observation:
        """
        Get an `Observation` instance for interacting with the API.

        The `Observation` provides methods to query observation-related resources in the Across API.

        Returns:
            Observation: An initialized `Observation` client bound to
            this Client’s API session.
        """
        return Observation(self.across_client)

    @property
    def visibility_calculator(self) -> VisibilityCalculator:
        """
        Get a `VisibilityCalculator` instance for interacting with the API.

        The `VisibilityCalculator` provides methods to calculate visibility windows
        for instruments in the Across API.

        Returns:
            VisibilityCalculator: An initialized `VisibilityCalculator` client bound to
            this Client’s API session.
        """
        return VisibilityCalculator(self.across_client)
