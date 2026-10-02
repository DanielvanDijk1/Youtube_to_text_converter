# transcribe.py
# This is the main script you will run from the terminal in VS Code.
#
# Usage example:
#   python transcribe.py "https://www.youtube.com/watch?v=..."
#
# What it does:
#   1) Reads the YouTube URL from the command line.
#   2) Fetches the transcript (captions) using transcript_fetcher.py.
#   3) Cleans the text using text_utils.py.
#   4) Saves the cleaned transcript as a .txt file in the same folder.

import argparse
import os
from transcript_fetcher import fetch_transcript, transcript_to_text, extract_video_id
from text_utils import clean_text


# ------------------------------------------------------------------------------
# Main function: orchestrates the whole process
# ------------------------------------------------------------------------------
def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Download YouTube transcript (captions only) and save as .txt"
    )

    # First argument: the YouTube URL (required)
    parser.add_argument(
        "url",
        help="YouTube video URL (must have captions enabled)"
    )

    # Optional argument: custom output filename
    # If not provided, we will auto-generate a filename from the video ID
    parser.add_argument(
        "--out",
        default=None,
        help=(
            "Output .txt file path. If not provided, defaults to "
            "<VIDEO_ID>_transcript.txt in the current folder."
        )
    )

    # Parse the arguments given by the user when running the script
    args = parser.parse_args()

    # -------------------------------------------------------------------------
    # Step 1: Fetch the transcript from YouTube
    # -------------------------------------------------------------------------
    # This calls the function in transcript_fetcher.py
    # If the video has no captions, this will raise a RuntimeError
    segments = fetch_transcript(args.url)

    # -------------------------------------------------------------------------
    # Step 2: Convert segments to a single plain text string
    # -------------------------------------------------------------------------
    text = transcript_to_text(segments)

    # -------------------------------------------------------------------------
    # Step 3: Clean the text (remove extra spaces, unwanted characters, etc.)
    # -------------------------------------------------------------------------
    cleaned = clean_text(text)

    # -------------------------------------------------------------------------
    # Step 4: Decide the output filename
    # -------------------------------------------------------------------------
    # Extract the video ID so we can make a sensible default filename
    video_id = extract_video_id(args.url)

    if args.out is None:
        # No custom filename given: use "<VIDEO_ID>_transcript.txt"
        out_path = f"{video_id}_transcript.txt"
    else:
        # Use the custom filename provided via --out
        out_path = args.out
        # Ensure it ends with .txt; if not, add it
        if not out_path.lower().endswith(".txt"):
            out_path += ".txt"

    # -------------------------------------------------------------------------
    # Step 5: Save the cleaned transcript to a .txt file
    # -------------------------------------------------------------------------
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(cleaned)

    # Print a confirmation message with the full path to the created file
    print(f"Transcript saved to: {os.path.abspath(out_path)}")


# ------------------------------------------------------------------------------
# EXAMPLE USAGE WITH HARDCODED URL (OPTIONAL, FOR TESTING ONLY)
# ------------------------------------------------------------------------------
# IF YOU PREFER NOT TO USE THE COMMAND LINE, YOU CAN UNCOMMENT THIS BLOCK
# AND RUN THIS FILE DIRECTLY. THEN YOU ONLY NEED TO CHANGE THE URL BELOW.

# if __name__ == "__main__":
#     # PUT YOUR YOUTUBE URL HERE (MUST HAVE CAPTIONS)
#     TEST_URL = "https://www.youtube.com/watch?v=WRSFRB0ECB8&list=PLyAG6gqVSXihNolbrby8Z8vEetFPCtzBj&index=6"
#
#     # Simulate command-line arguments
#     class FakeArgs:
#         url = TEST_URL
#         out = None
#
#     # Temporarily override argparse behavior
#     import sys
#     original_argv = sys.argv
#     sys.argv = ["transcribe.py"]  # pretend no CLI args
#
#     # Manually run the logic with TEST_URL
#     segments = fetch_transcript(TEST_URL)
#     text = transcript_to_text(segments)
#     cleaned = clean_text(text)
#
#     video_id = extract_video_id(TEST_URL)
#     out_path = f"{video_id}_transcript.txt"
#
#     with open(out_path, "w", encoding="utf-8") as f:
#         f.write(cleaned)
#
#     print(f"Transcript saved to: {os.path.abspath(out_path)}")
#
#     # Restore original argv
#     sys.argv = original_argv


# ------------------------------------------------------------------------------
# NORMAL ENTRY POINT (KEEP THIS AS-IS)
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    main()



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