import os

from data_fetcher import get_track_progresses

# Constants
GREEN_SQUARE_IMG = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Solid_green.svg/240px-Solid_green.svg.png"
GREY_SQUARE_IMG = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Grey_Square.svg/240px-Grey_Square.svg.png"


def generate_gamification_html(total_topics, learned_topics):
    """
    Generate gamification HTML for topics progress.

    Args:
        total_topics (int): Total number of topics.
        learned_topics (int): Number of topics learned.

    Returns:
        str: HTML code for gamification progress.
    """
    difference = total_topics - learned_topics
    green_squares = [f'<img src="{GREEN_SQUARE_IMG}" alt="Green Square" width="15"/>' for _ in range(learned_topics)]
    grey_squares = [f'<img src="{GREY_SQUARE_IMG}" alt="Grey Square" width="15"/>' for _ in range(difference)]
    topics_progress_html = " ".join(green_squares + grey_squares)
    return topics_progress_html


def generate_track_readme_content(user_data, track_data):
    """
    Generate README content for a track.

    Args:
        user_data (dict): User data.
        track_data (dict): Track data.

    Returns:
        str: README content.
    """
    track_progress = get_track_progresses(user_data.get("id"), track_data.get("progress_id"))
    track_title = track_data.get("title")
    track_description = track_data.get("description")
    topics_count = track_data.get("topics_count")
    projects_count = len(track_data.get("projects"))
    cover_url = track_data.get("cover")

    # Normalize track title
    normalized_track_title = track_title.lower().replace(" ", "-")

    folder_path = os.path.join("/tracks", normalized_track_title)

    try:
        # Create the folder for the track if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)
    except OSError as e:
        print(f"Error creating folder '{folder_path}': {e}")

    progress_topics = track_progress.get("learned_topics_count")
    progress_projects = len(track_progress.get("completed_projects"))

    percentage_topics_completion = (progress_topics / topics_count) * 100
    percentage_projects_completion = (progress_projects / projects_count) * 100

    cover_image_html = f'<img src="{cover_url}" alt="Track Cover" width="50">'

    readme_content = f"""
### {cover_image_html} [{track_title}]({folder_path})

#### Description
{track_description}

#### Progress
- Topics completion: **{percentage_topics_completion:.2f}%**

{generate_gamification_html(topics_count, progress_topics)}

- Projects completion: **{percentage_projects_completion:.2f}%**

- Total Topics: {topics_count}
- Total Projects: {projects_count}
"""

    return readme_content
