"""DSA learning platform for absolute beginners.

A Flask web app organized around the Striver A-Z DSA Sheet. Every problem
is treated as a teaching moment: instead of giving a clever solution, we
walk through the human thought process slowly, with deep intuition and
real-life analogies.
"""
from __future__ import annotations

from flask import Flask, abort, render_template, request

from content import (
    CURRICULUM,
    LEARN_LESSONS,
    PROBLEMS,
    get_lesson,
    get_problem,
    get_step,
    iter_all_problems,
    search_content,
)
from content.render import md

app = Flask(__name__)
app.jinja_env.filters["md"] = md


@app.route("/")
def index():
    total_problems = sum(1 for _ in iter_all_problems())
    return render_template(
        "index.html",
        curriculum=CURRICULUM,
        learn_lessons=LEARN_LESSONS,
        total_problems=total_problems,
    )


@app.route("/learn")
def learn_index():
    return render_template("learn_index.html", lessons=LEARN_LESSONS)


@app.route("/learn/<lesson_id>")
def learn_lesson(lesson_id: str):
    lesson = get_lesson(lesson_id)
    if lesson is None:
        abort(404)
    return render_template("lesson.html", lesson=lesson, lessons=LEARN_LESSONS)


@app.route("/practice")
def practice_index():
    return render_template(
        "practice_index.html",
        curriculum=CURRICULUM,
        total_problems=sum(1 for _ in iter_all_problems()),
    )


@app.route("/practice/step/<int:step_id>")
def practice_step(step_id: int):
    step = get_step(step_id)
    if step is None:
        abort(404)
    return render_template("step.html", step=step, curriculum=CURRICULUM)


@app.route("/practice/problem/<problem_id>")
def practice_problem(problem_id: str):
    problem = get_problem(problem_id)
    if problem is None:
        abort(404)
    # Find the step/lecture for breadcrumbs and previous/next navigation.
    flat = list(iter_all_problems())
    ids = [p["id"] for p in flat]
    try:
        idx = ids.index(problem_id)
    except ValueError:
        idx = -1
    prev_problem = flat[idx - 1] if idx > 0 else None
    next_problem = flat[idx + 1] if 0 <= idx < len(flat) - 1 else None
    return render_template(
        "problem.html",
        problem=problem,
        prev_problem=prev_problem,
        next_problem=next_problem,
    )


@app.route("/search")
def search():
    query = (request.args.get("q") or "").strip()
    results = search_content(query) if query else []
    return render_template("search.html", query=query, results=results)


@app.route("/bookmarks")
def bookmarks():
    # Bookmarks live in browser localStorage; the page hydrates from there.
    return render_template("bookmarks.html", problems=PROBLEMS)


@app.errorhandler(404)
def not_found(_):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
