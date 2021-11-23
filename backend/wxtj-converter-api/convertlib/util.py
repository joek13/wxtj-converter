"""Utility functions for the converter library.
"""

import typing


def _duration_from_ms(duration_ms: int) -> typing.Tuple[int, int]:
    """Converts a duration in milliseconds to a tuple of 2 ints: minutes, seconds
    Args:
        duration_ms (int): The number of milliseconds in this duration.
    Returns:
        typing.Tuple[int, int]: int 2-tuple of the form (minutes, seconds)
    """
    minutes = 0
    seconds = 0

    # how many whole minutes are there in this track?
    minutes = duration_ms // (60 * 1000)

    # how many ms are left over?
    rem = duration_ms % (60 * 1000)

    # convert those ms to (whole) seconds
    seconds = rem // 1000

    return (minutes, seconds)
