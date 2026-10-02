# text_utils.py
# This file handles basic text cleaning and splitting utilities.
# For now we only use clean_text(), but split_into_sentences() is there
# for future analysis if you want to work sentence-by-sentence.

import re
from typing import List


# ------------------------------------------------------------------------------
# 1) Clean the transcript text
# ------------------------------------------------------------------------------
def clean_text(text: str) -> str:
    """
    Basic cleaning of transcript text.

    This function:
      - Replaces multiple spaces / newlines with a single space.
      - Removes most special characters, keeping basic punctuation.
      - Strips leading/trailing whitespace.
    """
    # Replace any run of whitespace (spaces, tabs, newlines) with a single space
    text = re.sub(r"\s+", " ", text)

    # Remove characters that are not:
    #   - word characters (\w = letters, digits, underscore)
    #   - whitespace (\s)
    #   - basic punctuation: . , ! ? ; : ' " ( ) - [ ]
    # Everything else is replaced with a space.
    text = re.sub(r"[^\w\s.,!?;:'\"()\-\[\]]", " ", text)

    # Remove leading/trailing spaces and return
    return text.strip()


# ------------------------------------------------------------------------------
# 2) Split text into sentences (optional, for future use)
# ------------------------------------------------------------------------------
def split_into_sentences(text: str) -> List[str]:
    """
    Split a text into sentences using simple rules.

    This is a basic implementation:
      - Splits on '.', '!', or '?' followed by whitespace.
      - Removes empty results and strips spaces.

    For more accurate sentence splitting, you could later use nltk or spaCy.
    """
    # Regex: split on '. ', '! ', or '? ' (lookbehind ensures we keep the punctuation)
    sentences = re.split(r"(?<=[.!?])\s+", text)

    # Remove any empty strings and strip spaces from each sentence
    return [s.strip() for s in sentences if s.strip()]


# ------------------------------------------------------------------------------
# EXAMPLE USAGE (OPTIONAL, FOR TESTING ONLY)
# ------------------------------------------------------------------------------
# IF YOU WANT TO TEST THIS FILE DIRECTLY, YOU CAN UNCOMMENT THE BLOCK BELOW.
# THIS IS JUST A DEMO; YOU NORMALLY WON'T NEED TO RUN THIS FILE ON ITS OWN.

# if __name__ == "__main__":
#     # PUT A SAMPLE TRANSCRIPT TEXT HERE TO SEE HOW CLEANING WORKS
#     SAMPLE_TEXT = "PASTE_SOME_RAW_TRANSCRIPT_TEXT_HERE"
#
#     cleaned = clean_text(SAMPLE_TEXT)
#     print("Cleaned text:")
#     print(cleaned)









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