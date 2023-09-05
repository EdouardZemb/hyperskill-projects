import sys
import logging
import json
from data_fetcher import (
    get_user_data,
    get_track_list,
    get_track_data,
    get_track_progresses,
    FetchDataError,
)
from html_generator import generate_track_readme_content
from file_writer import write_to_output

CONFIG_FILE = "config.json"

# Configure logging
logging.basicConfig(filename='hyperskill.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


def read_config(filename):
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
        logging.error(f"Configuration file '{filename}' not found.")
        sys.exit(f"Configuration file '{filename}' not found. Please ensure it exists.")
    except json.JSONDecodeError:
        logging.error(f"Error parsing configuration file '{filename}'. Please ensure it's valid JSON.")
        sys.exit(f"Error parsing configuration file '{filename}'. Please ensure it's valid JSON.")


# Main execution
if __name__ == "__main__":
    # Read configuration from the JSON file
    config = read_config(CONFIG_FILE)
    user_id = config.get("user_id")
    api_url = config.get("api_url")
    output_file = config.get("output_file")

    try:
        # Fetch user data and track list from Hyperskill API
        user_data = get_user_data(user_id)
        track_list = get_track_list()

        track_readme_content = ""

        for track in track_list:
            if track.get("projects"):
                track_data = get_track_data(track.get("id"))
                # check if there is progress in the track
                if track_data.get("progress_id"):
                    try:
                        # Fetch track progress data
                        track_progress = get_track_progresses(user_data.get("id"), track_data.get("progress_id"))
                        # check if there is progress in the track
                        if track_progress.get("completed_projects"):
                            track_readme_content += generate_track_readme_content(user_data, track_data)
                    except FetchDataError as progress_error:
                        logging.error(
                            f"Error fetching progress data for track '{track_data.get('title')}': {progress_error}")

        # Combine all track content into the README
        full_readme_content = f"""# Hyperskill Projects Repository

Welcome to my Hyperskill Projects Repository! This repository serves as a centralized hub for documenting and storing my practical software development work completed on the Hyperskill platform.

## Overview

In this repository, you will find a collection of project folders, each corresponding to a project I've worked on as part of my learning journey on Hyperskill. Each project folder contains detailed information about the project, including its purpose, key features, and how to build and run it.

{track_readme_content}

## License

This repository is open source and available under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code as long as you include the appropriate attribution.

## Contact

If you have any questions, suggestions, or would like to collaborate, please don't hesitate to reach out to me:

Happy coding!
"""

        # Write the generated content to the README file
        write_to_output(full_readme_content, output_file)
        print(f"README file generated successfully and saved to '{output_file}'")

    except FetchDataError as api_error:
        logging.error(f"Error fetching data from the Hyperskill API: {api_error}")
        sys.exit(f"Error fetching data from the Hyperskill API: {api_error}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(f"An unexpected error occurred: {e}")
