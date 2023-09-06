import sys
from data_fetcher import (
    get_user_data,
    get_track_list,
    get_track_data,
    get_track_progresses,
    FetchDataError,
)
from html_generator import generate_track_readme_content
from file_writer import write_to_output
from logging_singleton import LoggingSingleton
from config_reader import OUTPUT_FILE, USER_ID


# Main execution
if __name__ == "__main__":
    try:
        # Fetch user data and track list from Hyperskill API
        user_data = get_user_data(USER_ID)
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
                        LoggingSingleton().error(
                            f"Error fetching progress data for track '{track_data.get('title')}': {progress_error}")

        # Combine all track content into the README
        full_readme_content = f"""# Hyperskill Projects Repository

Welcome to my Hyperskill Projects Repository! This repository serves as a centralized hub for documenting and storing my practical software development work completed on the Hyperskill platform.

## Overview

In this repository, you will find a collection of project folders, each corresponding to a project I've worked on as part of my learning journey on Hyperskill. Each project folder contains detailed information about the project, including its purpose, key features, and how to build and run it.

## Tracks
{track_readme_content}

## License

This repository is open source and available under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code as long as you include the appropriate attribution.

## Contact

If you have any questions, suggestions, or would like to collaborate, please don't hesitate to reach out to me:

Happy coding!
"""

        # Write the generated content to the README file
        write_to_output(full_readme_content, OUTPUT_FILE)
        print(f"README file generated successfully and saved to '{OUTPUT_FILE}'")

    except FetchDataError as api_error:
        LoggingSingleton().error(f"Error fetching data from the Hyperskill API: {api_error}")
        sys.exit(f"Error fetching data from the Hyperskill API: {api_error}")
    except Exception as e:
        LoggingSingleton().error(f"An unexpected error occurred: {e}")
        sys.exit(f"An unexpected error occurred: {e}")
