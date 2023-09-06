import coreapi
from logging_singleton import LoggingSingleton
from config_reader import API_URL


def fetch_data(action, params=None):
    """
        Fetches data from the Hyperskill API.

        Args:
            action (list): The API action to perform.
            params (dict, optional): Parameters for the API request.

        Returns:
            dict: The API response.

        Raises:
            FetchDataError: If an error occurs while fetching data.
        """
    try:
        client = coreapi.Client()
        schema = client.get(API_URL)
        result = client.action(schema, action, params=params)
        return result
    except coreapi.exceptions.ErrorMessage as e:
        LoggingSingleton().error(f"Error fetching data from API: {e}")
        raise FetchDataError(f"Error fetching data from API: {e}")


# Define a custom exception
class FetchDataError(Exception):
    pass


def get_user_data(user_id):
    endpoint = ["users", "read"]
    params = {"id": user_id}
    result_user = fetch_data(endpoint, params=params)
    return result_user.get("users")[0]


def get_track_list():
    endpoint = ["tracks", "list"]
    result_tracks = fetch_data(endpoint)
    return result_tracks.get("tracks")


def get_track_data(track_id):
    endpoint = ["tracks", "read"]
    params = {"id": track_id}
    result_track = fetch_data(endpoint, params=params)
    return result_track.get("tracks")[0]


def get_track_progresses(user_id, progress_id):
    endpoint = ["progresses", "read"]
    params = {"id": f"{progress_id}-{user_id}"}
    result_progress = fetch_data(endpoint, params=params)
    return result_progress.get("progresses")[0]
