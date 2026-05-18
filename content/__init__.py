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
    """Build a placeholder entry for a problem that has no write-up yet.

    Even stubs carry the new structural fields so the layout looks
    intentional and the reader gets some orientation about what the
    finished write-up will teach.
    """
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
            "A patient, line-by-line write-up of this problem is on the "
            "way. While that lands, here is the orientation you can use "
            "right now.\n\n"
            "Every finished problem on this site follows the same six-"
            "part teaching template, plus a final \"what this teaches "
            "and where it leads\" section. The template is:\n\n"
            "1. **Problem Understanding** — the problem, restated in "
            "plain human language, with examples and what the problem "
            "is really asking versus what it sounds like at first.\n"
            "2. **Brute Force Approach** — the most natural, "
            "least-clever first attempt, with line-by-line Python "
            "comments and an honest complexity discussion.\n"
            "3. **Thought Process Breakdown** — the inner monologue "
            "that a real beginner would have, the false starts that "
            "are productive, and the moment when the better idea "
            "appears.\n"
            "4. **Optimized Approach** — the better algorithm, with "
            "the precise insight that unlocks it.\n"
            "5. **Deep Concept Explanation** — why it actually works, "
            "with real-life analogies and visual mental models.\n"
            "6. **Final Summary** — what pattern it teaches and how "
            "to recognize the same pattern when it is wearing a "
            "different costume next time.\n\n"
            "On top of that, every problem now has **Beginner "
            "Confusion Notes** — long, patient answers to the "
            "questions that beginners actually ask — plus a "
            "**Resources** block with the original Striver "
            "article/video, the LeetCode equivalent (when it exists), "
            "and a brief **What this teaches / Pattern / "
            "Prerequisites / Next problems** map so you always know "
            "where you are in the journey.\n\n"
            "Until the long-form lands, the lesson and earlier "
            "problems linked in the **Prerequisites** below cover "
            "everything you need to attempt this one yourself."
        ),
        "what_this_teaches": (
            "This problem belongs to the **{step}** track and "
            "specifically the **{lecture}** lecture, so it is the "
            "next step in the curriculum after the lecture's earlier "
            "problems. The full write-up will name the exact pattern "
            "and link to similar problems."
        ).format(step=step["title"], lecture=lecture["title"]),
        "pattern": "(to be named in the full write-up)",
        "prerequisite_lessons": [],
        "prerequisite_problems": [],
        "next_problems": [],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course Sheet",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
        ],
        "confusion_notes": [],
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
