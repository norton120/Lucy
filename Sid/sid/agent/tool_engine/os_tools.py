from typing import Literal

"""Tools must always be functions in global scope within the targeted module. They must be documented using Google-style docstrings.


These are Operating System tools used by Sid agents to adjust their own memory and other internal settings.
"""


def replace_content_in_segment(segment: Literal['human','persona'], old_content:str, new_content: str):
    """Replace some of the content in a segment of core memory.

    Args:
        segment (str): The segment to replace content within. Must be one of "persona" or "human".
        old_content (str): The old content to replace. Must be an exact match.
        new_content (str): The new content to replace the segment with.

    Returns:
        str: A message indicating the success or failure of the operation.
    """
    raise NotImplementedError

def replace_segment(segment: Literal['human','persona'], new_content: str):
    """Replace all of the content in a segment of core memory.

    Args:
        segment (str): The segment to replace content within. Must be one of "persona" or "human".
        new_content (str): The new content to replace the segment with.

    Returns:
        str: A message indicating the success or failure of the operation.
    """
    raise NotImplementedError

def archive_content(content: str):
    """write content to the archival memory.

    Args:
        content (str): The content to archive.

    Returns:
        str: A message indicating the success or failure of the operation.
    """
    raise NotImplementedError