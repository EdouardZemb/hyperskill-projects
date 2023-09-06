import json

CONFIG_FILE = "config.json"


def read_config(filename=CONFIG_FILE):
    """
    Reads configuration from a JSON file.

    Args:
        filename (str): The path to the JSON configuration file.

    Returns:
        dict: The configuration data.

    Raises:
        FileNotFoundError: If the configuration file is not found.
        json.JSONDecodeError: If there is an error parsing the JSON configuration.
    """
    try:
        with open(filename, "r") as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        print(f"Configuration file '{filename}' not found.")
        raise
    except json.JSONDecodeError:
        print(f"Error parsing configuration file '{filename}'. Please ensure it's valid JSON.")
        raise


# Read configuration from the JSON file
config = read_config()
user_id = config.get("user_id")
api_url = config.get("api_url")
output_file = config.get("output_file")

# Declare constants that other files can use
USER_ID = user_id
API_URL = api_url
OUTPUT_FILE = output_file
