"""Learn lessons: long-form conceptual primers for absolute beginners.

Each lesson is a dictionary with `id`, `title`, `tags`, `summary`, and
`body` (markdown). They are intentionally wordy — the goal is to build
intuition, not to be reference material.
"""
from __future__ import annotations

from .arrays import LESSON as ARRAYS
from .strings import LESSON as STRINGS
from .hashing import LESSON as HASHING
from .recursion import LESSON as RECURSION
from .sorting import LESSON as SORTING
from .searching import LESSON as SEARCHING
from .two_pointers import LESSON as TWO_POINTERS
from .sliding_window import LESSON as SLIDING_WINDOW
from .stacks import LESSON as STACKS
from .queues import LESSON as QUEUES
from .linked_lists import LESSON as LINKED_LISTS
from .trees import LESSON as TREES
from .backtracking import LESSON as BACKTRACKING
from .dp import LESSON as DP

LEARN_LESSONS: list[dict] = [
    ARRAYS,
    STRINGS,
    HASHING,
    RECURSION,
    SORTING,
    SEARCHING,
    TWO_POINTERS,
    SLIDING_WINDOW,
    STACKS,
    QUEUES,
    LINKED_LISTS,
    TREES,
    BACKTRACKING,
    DP,
]
