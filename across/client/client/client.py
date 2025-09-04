import across.sdk.v1 as sdk
from across.sdk.v1.abstract_credential_storage import CredentialStorage
from across.sdk.v1.api_client_wrapper import ApiClientWrapper

from ..core.config import config
from .observatory import Observatory


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
        credentials: CredentialStorage | None = None,
    ):
        """
        Initialize a Client instance for the Across API.

        Args:
            client_id (str | None, optional):
                The client ID used for authentication. Required if
                `credentials` is not provided.
            client_secret (str | None, optional):
                The client secret used for authentication. Required if
                `credentials` is not provided.
            credentials (CredentialStorage | None, optional):
                A credentials storage object that can provide authentication
                tokens. If provided, it takes precedence over `client_id`
                and `client_secret`.
        """
        configuration = sdk.Configuration(host=config.HOST, username=client_id, password=client_secret)
        self.across_client = ApiClientWrapper.get_client(configuration=configuration, creds=credentials)

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
