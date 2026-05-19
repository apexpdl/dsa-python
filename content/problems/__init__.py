"""Problem registry — aggregates every problem write-up into one dict.

Each topic module exports a `PROBLEMS` list of dictionaries. We merge
them here and keep the order canonical (matching the curriculum).
"""
from __future__ import annotations

from . import (
    step01_basics,
    step01_extras,
    step02_sorting,
    step02_extras,
    step03_arrays,
    step03_extras,
    step04_binary_search,
    step04_extras,
    step05_strings,
    step05_extras,
    step06_linked_list,
    step06_extras,
    step07_recursion,
    step07_extras,
    step08_extras,
    step09_stacks_queues,
    step09_extras,
    step10_sliding_window,
    step10_extras,
    step11_heaps,
    step11_extras,
    step12_greedy,
    step13_trees,
    step13_extras,
    step15_graphs,
    step16_dp,
)


def _build_registry() -> dict[str, dict]:
    registry: dict[str, dict] = {}
    for module in (
        step01_basics,
        step01_extras,
        step02_sorting,
        step02_extras,
        step03_arrays,
        step03_extras,
        step04_binary_search,
        step04_extras,
        step05_strings,
        step05_extras,
        step06_linked_list,
        step06_extras,
        step07_recursion,
    step07_extras,
    step08_extras,
        step09_stacks_queues,
        step09_extras,
        step10_sliding_window,
        step10_extras,
        step11_heaps,
        step11_extras,
        step12_greedy,
        step13_trees,
        step13_extras,
        step15_graphs,
        step16_dp,
    ):
        for problem in getattr(module, "PROBLEMS", []):
            registry[problem["id"]] = problem
    return registry


PROBLEMS: dict[str, dict] = _build_registry()
