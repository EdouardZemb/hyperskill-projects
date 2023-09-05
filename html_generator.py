# Function to generate gamification HTML
from data_fetcher import get_track_progresses


def generate_gamification_html(total_topics, learned_topics):
    # Calculate the difference between total topics and learned topics
    difference = total_topics - learned_topics

    # Generate small squares to indicate topics progress
    topics_squares = ""
    for _ in range(learned_topics):
        topics_squares += '<span class="square-green"></span>'
    for _ in range(difference):
        topics_squares += '<span class="square-grey"></span>'

    gamification_html = f"""
<div class="topics-progress">
    <h2>Topics Progress</h2>
    {topics_squares}
</div>
"""
    return gamification_html


# Function to generate README content for a track
def generate_track_readme_content(user_data, track_data):
    track_progress = get_track_progresses(user_data.get("id"), track_data.get("progress_id"))
    track_title = track_data.get("title")
    track_description = track_data.get("description")
    topics_count = track_data.get("topics_count")
    projects_count = len(track_data.get("projects"))
    cover_url = track_data.get("cover")

    progress_topics = track_progress.get("learned_topics_count")
    progress_projects = len(track_progress.get("completed_projects"))

    # Calculate the percentage completion of topics and projects
    percentage_topics_completion = (progress_topics / topics_count) * 100
    percentage_projects_completion = (progress_projects / projects_count) * 100

    # Style the cover image with a fixed size
    cover_image_html = f'<img src="{cover_url}" alt="Track Cover" class="cover-image">'

    readme_content = f"""
## {cover_image_html} {track_title}

### Description
{track_description}

### Progress
{generate_gamification_html(topics_count, progress_topics)}

- Percentage Completion of Topics: {percentage_topics_completion:.2f}%
- Percentage Completion of Projects: {percentage_projects_completion:.2f}%

### Total Topics: {topics_count}
### Total Projects: {projects_count}
"""

    return readme_content
