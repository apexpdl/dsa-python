// Client-side progress + bookmarks. Persisted to localStorage so it
// survives reloads but never leaves the browser.
(function () {
  const STORAGE_SOLVED = "dsa-solved-v1";
  const STORAGE_BOOKMARKS = "dsa-bookmarks-v1";

  function readSet(key) {
    try {
      const raw = localStorage.getItem(key);
      if (!raw) return new Set();
      const arr = JSON.parse(raw);
      return new Set(Array.isArray(arr) ? arr : []);
    } catch (_) {
      return new Set();
    }
  }
  function writeSet(key, set) {
    try {
      localStorage.setItem(key, JSON.stringify([...set]));
    } catch (_) {}
  }

  function readObject(key) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : {};
    } catch (_) {
      return {};
    }
  }
  function writeObject(key, obj) {
    try {
      localStorage.setItem(key, JSON.stringify(obj));
    } catch (_) {}
  }

  // Decorate the problem-list items on practice/step pages with a
  // solved checkmark.
  function decorateProblemLists() {
    const solved = readSet(STORAGE_SOLVED);
    document.querySelectorAll("[data-problem-id]").forEach((li) => {
      const id = li.getAttribute("data-problem-id");
      const status = li.querySelector(".problem-status");
      if (!status) return;
      if (solved.has(id)) {
        status.textContent = "✓ solved";
        status.classList.add("solved");
      } else {
        status.textContent = "";
        status.classList.remove("solved");
      }
    });
    // Progress summary on the practice index.
    const summary = document.querySelector("[data-progress-summary]");
    if (summary) {
      const countEl = summary.querySelector("[data-solved-count]");
      const total = summary.querySelector("[data-total-count]");
      if (countEl && total) {
        countEl.textContent = solved.size;
      }
    }
  }

  // On the problem page: toolbar buttons.
  function wireProblemToolbar() {
    const page = document.querySelector(".problem-page");
    if (!page) return;
    const problemId = page.getAttribute("data-problem-id");
    if (!problemId) return;
    const title = document.querySelector(".article-header h1")?.textContent?.trim();
    const bookmarks = readObject(STORAGE_BOOKMARKS);
    const solved = readSet(STORAGE_SOLVED);

    const bookmarkBtn = page.querySelector("[data-toggle-bookmark]");
    const solvedBtn = page.querySelector("[data-toggle-solved]");

    function refresh() {
      if (bookmarkBtn) {
        const isBookmarked = !!bookmarks[problemId];
        bookmarkBtn.querySelector(".bookmark-state").textContent =
          isBookmarked ? "★ Bookmarked" : "☆ Bookmark";
      }
      if (solvedBtn) {
        const isSolved = solved.has(problemId);
        solvedBtn.querySelector(".solved-state").textContent =
          isSolved ? "● Solved" : "○ Mark as solved";
      }
    }

    refresh();

    if (bookmarkBtn) {
      bookmarkBtn.addEventListener("click", () => {
        if (bookmarks[problemId]) {
          delete bookmarks[problemId];
        } else {
          bookmarks[problemId] = {
            id: problemId,
            title: title || problemId,
            url: window.location.pathname,
          };
        }
        writeObject(STORAGE_BOOKMARKS, bookmarks);
        refresh();
      });
    }
    if (solvedBtn) {
      solvedBtn.addEventListener("click", () => {
        if (solved.has(problemId)) {
          solved.delete(problemId);
        } else {
          solved.add(problemId);
        }
        writeSet(STORAGE_SOLVED, solved);
        refresh();
      });
    }
  }

  // Bookmarks page: render items from localStorage.
  function renderBookmarksPage() {
    const list = document.querySelector("[data-bookmarks-list]");
    const tmpl = document.getElementById("bookmark-template");
    if (!list || !tmpl) return;
    const bookmarks = readObject(STORAGE_BOOKMARKS);
    const entries = Object.values(bookmarks);
    const emptyMessage = list.querySelector("[data-bookmarks-empty]");
    if (entries.length === 0) {
      if (emptyMessage) emptyMessage.style.display = "list-item";
      return;
    }
    if (emptyMessage) emptyMessage.style.display = "none";
    for (const entry of entries) {
      const node = tmpl.content.firstElementChild.cloneNode(true);
      const a = node.querySelector("a");
      a.setAttribute("href", entry.url);
      node.querySelector("[data-title]").textContent = entry.title;
      list.appendChild(node);
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    decorateProblemLists();
    wireProblemToolbar();
    renderBookmarksPage();
  });
})();
