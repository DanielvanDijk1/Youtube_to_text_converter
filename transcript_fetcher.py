# transcript_fetcher.py
# This file handles:
#   1) Extracting the YouTube video ID from a URL
#   2) Fetching the transcript (captions) from YouTube
#   3) Converting the list of caption segments into one plain text string

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import re


# ------------------------------------------------------------------------------
# 1) Extract YouTube video ID from different URL formats
# ------------------------------------------------------------------------------
def extract_video_id(url: str) -> str:
    """
    Given a YouTube URL, return the 11-character video ID.

    Example:
        https://www.youtube.com/watch?v=WRSFRB0ECB8
        becomes:
        WRSFRB0ECB8
    """

    patterns = [
        r"(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([A-Za-z0-9_-]{11})"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)

        if match:
            return match.group(1)

    raise ValueError(f"Could not extract YouTube video ID from: {url}")


# ------------------------------------------------------------------------------
# 2) Fetch transcript (captions) for a given YouTube URL
# ------------------------------------------------------------------------------
def fetch_transcript(url: str, languages=("en", "en-US", "en-GB")) -> list[dict]:
    """
    Fetch captions for a YouTube video.

    The function tries, in order:
      1) Manually-created English captions.
      2) Auto-generated English captions.
      3) Any available caption language.

    It returns a list of dictionaries in this format:

        [
            {
                "text": "Example caption text",
                "start": 0.0,
                "duration": 4.5
            }
        ]
    """

    # Get the YouTube video ID from the full URL
    video_id = extract_video_id(url)

    try:
        # CREATE THE API OBJECT.
        # In version 1.2.4, YouTubeTranscriptApi must be instantiated first.
        ytt_api = YouTubeTranscriptApi()

        # GET THE LIST OF ALL AVAILABLE CAPTION TRACKS.
        # Old code used .list_transcripts(...).
        # Current package version uses .list(...).
        transcript_list = ytt_api.list(video_id)

        # We will store the selected caption track here.
        chosen_transcript = None

        # ----------------------------------------------------------------------
        # First choice: manually-created English captions
        # ----------------------------------------------------------------------
        try:
            chosen_transcript = (
                transcript_list.find_manually_created_transcript(languages)
            )
        except NoTranscriptFound:
            pass

        # ----------------------------------------------------------------------
        # Second choice: auto-generated English captions
        # ----------------------------------------------------------------------
        if chosen_transcript is None:
            try:
                chosen_transcript = (
                    transcript_list.find_generated_transcript(languages)
                )
            except NoTranscriptFound:
                pass

        # ----------------------------------------------------------------------
        # Third choice: any available caption track, in any language
        # ----------------------------------------------------------------------
        if chosen_transcript is None:
            chosen_transcript = next(iter(transcript_list), None)

        # If there are no tracks at all, stop with a clear error.
        if chosen_transcript is None:
            raise NoTranscriptFound(video_id)

        # DOWNLOAD THE SELECTED CAPTION TRACK.
        # .fetch() returns a FetchedTranscript object.
        fetched_transcript = chosen_transcript.fetch()

        # CONVERT THE PACKAGE'S TRANSCRIPT OBJECT INTO A NORMAL LIST OF DICTS.
        # This preserves compatibility with transcribe.py and transcript_to_text().
        segments = []

        for snippet in fetched_transcript:
            segments.append(
                {
                    "text": snippet.text,
                    "start": snippet.start,
                    "duration": snippet.duration,
                }
            )

        return segments

    except (TranscriptsDisabled, NoTranscriptFound) as error:
        raise RuntimeError(
            f"No transcript available for video {video_id}"
        ) from error


# ------------------------------------------------------------------------------
# 3) Convert list of transcript segments into one plain text string
# ------------------------------------------------------------------------------
def transcript_to_text(segments: list[dict]) -> str:
    """
    Join caption segments into one plain-text transcript.

    It takes this:
        [{"text": "Hello"}, {"text": "world"}]

    And returns:
        "Hello world"
    """

    return " ".join(
        segment["text"].replace("\n", " ")
        for segment in segments
    )



# ==============================================================================
# HOW TO RUN THIS YOUTUBE TRANSCRIPT TOOL
# ==============================================================================
#
# 1) KEEP THESE THREE FILES IN THE SAME FOLDER:
#
#       transcript_fetcher.py
#       text_utils.py
#       transcribe.py
#
#    DO NOT RENAME transcript_fetcher.py OR text_utils.py.
#    transcribe.py imports functions from both of them.
#
#
# 2) OPEN THIS FOLDER IN VS CODE.
#
#    In VS Code, go to:
#
#       Terminal -> New Terminal
#
#    A terminal will open at the bottom of VS Code.
#
#
# 3) MAKE SURE THE TERMINAL IS IN THIS FOLDER.
#
#    The terminal prompt should end with something similar to:
#
#       ...\Youtube_tool>
#
#    If it does NOT, move into the folder by typing:
#
#       cd Youtube_tool
#
#    Then press Enter.
#
#
# 4) INSTALL THE REQUIRED LIBRARY.
#
#    THIS IS ONLY NEEDED ONCE FOR THIS PYTHON INSTALLATION.
#
#    Type this in the VS CODE TERMINAL, NOT IN A .PY FILE:
#
#       pip install youtube-transcript-api
#
#    Wait until you see a message beginning with:
#
#       Successfully installed ...
#
#
# 5) RUN THE TOOL TO CREATE A TRANSCRIPT.
#
#    Type this in the VS CODE TERMINAL, NOT IN A .PY FILE:
#
#       python transcribe.py "PASTE_YOUTUBE_URL_HERE" --out "YOUR_OUTPUT_NAME.txt"
#
#    EXAMPLE:
#
#       python transcribe.py "https://www.youtube.com/watch?v=sNxD4PYWPfg&list=PLyAG6gqVSXihNolbrby8Z8vEetFPCtzBj&index=5" --out "Python Hedge Fund Tutorial p.2.txt"
#
#    IMPORTANT:
#       - REPLACE THE URL INSIDE THE FIRST PAIR OF QUOTATION MARKS.
#       - REPLACE THE OUTPUT FILE NAME AFTER --out.
#       - KEEP QUOTATION MARKS AROUND BOTH THE URL AND FILE NAME.
#       - USE ONLY THE DIRECT YOUTUBE URL.
#       - DO NOT USE MARKDOWN LINK FORMATTING SUCH AS [URL](URL).
#
#
# 6) FIND THE OUTPUT FILE.
#
#    After the script runs successfully, the terminal prints:
#
#       Transcript saved to: C:\...\Youtube_tool\YOUR_OUTPUT_NAME.txt
#
#    The .txt file is created in the SAME FOLDER as these three Python files.
#    It will appear in both:
#
#       - VS Code Explorer
#       - Windows File Explorer
#
#
# 7) FOR THE NEXT VIDEO:
#
#    DO NOT EDIT transcript_fetcher.py, text_utils.py, OR transcribe.py.
#    Run the same terminal command again, but change:
#
#       - The YouTube URL
#       - The file name after --out
#
#
# ==============================================================================