"""Content package: curriculum, learn lessons, problems, and lookups.

Importing this module triggers the side effect of importing every
problem module, which populates the `PROBLEMS` registry. The data is
held in plain Python dictionaries — this is intentional. It keeps the
content greppable, diffable, and trivially editable in a code editor.
"""
from __future__ import annotations

from typing import Iterator

from .curriculum import CURRICULUM
from .learn import LEARN_LESSONS
from .problems import PROBLEMS


def get_step(step_id: int) -> dict | None:
    for step in CURRICULUM:
        if step["id"] == step_id:
            return step
    return None


def get_lesson(lesson_id: str) -> dict | None:
    for lesson in LEARN_LESSONS:
        if lesson["id"] == lesson_id:
            return lesson
    return None


def get_problem(problem_id: str) -> dict | None:
    if problem_id in PROBLEMS:
        return PROBLEMS[problem_id]
    # Walk the curriculum to find the step/lecture context for a stub.
    for step in CURRICULUM:
        for lecture in step["lectures"]:
            if problem_id in lecture["problems"]:
                return _stub_problem(problem_id, step, lecture)
    return None


def iter_all_problems() -> Iterator[dict]:
    """Walk the curriculum in display order and yield every problem.

    Problems that have no detailed write-up yet still appear here — we
    fall back to a small "coming soon" stub so the sheet stays complete.
    """
    for step in CURRICULUM:
        for lecture in step["lectures"]:
            for problem_id in lecture["problems"]:
                problem = PROBLEMS.get(problem_id)
                if problem is None:
                    problem = _stub_problem(problem_id, step, lecture)
                yield problem


def _stub_problem(problem_id: str, step: dict, lecture: dict) -> dict:
    """Build a placeholder entry for a problem that has no write-up yet."""
    pretty = problem_id.replace("-", " ").title()
    return {
        "id": problem_id,
        "title": pretty,
        "step_id": step["id"],
        "step_title": step["title"],
        "lecture_id": lecture["id"],
        "lecture_title": lecture["title"],
        "tags": [],
        "status": "coming-soon",
        "understanding": (
            "A deep, step-by-step write-up for this problem is coming "
            "soon. It will follow the same teaching template used "
            "everywhere else on this site:\n\n"
            "1. Problem Understanding — what the problem is really "
            "asking, in plain language.\n"
            "2. Brute Force Approach — the most natural first attempt, "
            "with a worked example and Python code commented line by "
            "line.\n"
            "3. Thought Process Breakdown — how a real beginner moves "
            "from the brute force to a better idea.\n"
            "4. Optimized Approach — the better algorithm, with the "
            "insight that unlocks it.\n"
            "5. Deep Concept Explanation — why it actually works.\n"
            "6. Final Summary — what pattern this teaches and how to "
            "recognize it next time."
        ),
    }


def search_content(query: str) -> list[dict]:
    """Plain substring search across problems and learn lessons.

    Cheap and good enough for a content site of this size. We return a
    list of `{kind, item, snippet}` dicts ordered with problems first.
    """
    q = query.lower().strip()
    if not q:
        return []
    results: list[dict] = []
    for problem in iter_all_problems():
        haystack = " ".join(
            str(problem.get(field, ""))
            for field in (
                "title",
                "understanding",
                "thought_process",
                "deep_concept",
                "summary",
            )
        ).lower()
        if q in problem["title"].lower() or q in haystack:
            results.append(
                {
                    "kind": "problem",
                    "id": problem["id"],
                    "title": problem["title"],
                    "url": f"/practice/problem/{problem['id']}",
                    "tags": problem.get("tags", []),
                }
            )
    for lesson in LEARN_LESSONS:
        text = (lesson["title"] + " " + lesson.get("body", "")).lower()
        if q in text:
            results.append(
                {
                    "kind": "lesson",
                    "id": lesson["id"],
                    "title": lesson["title"],
                    "url": f"/learn/{lesson['id']}",
                    "tags": lesson.get("tags", []),
                }
            )
    return results


__all__ = [
    "CURRICULUM",
    "LEARN_LESSONS",
    "PROBLEMS",
    "get_step",
    "get_lesson",
    "get_problem",
    "iter_all_problems",
    "search_content",
]
