// Client-side progress + bookmarks + highlights + theme.
// All state lives in localStorage so it survives reloads but never
// leaves the browser.
(function () {
  const STORAGE_SOLVED = "dsa-solved-v1";
  const STORAGE_BOOKMARKS = "dsa-bookmarks-v1";
  const STORAGE_HIGHLIGHTS = "dsa-highlights-v1";
  const STORAGE_THEME = "dsa-theme-v1";

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

  function readArray(key) {
    try {
      const raw = localStorage.getItem(key);
      if (!raw) return [];
      const arr = JSON.parse(raw);
      return Array.isArray(arr) ? arr : [];
    } catch (_) {
      return [];
    }
  }
  function writeArray(key, arr) {
    try {
      localStorage.setItem(key, JSON.stringify(arr));
    } catch (_) {}
  }

  // ------------------------------------------------------------------
  // Theme toggle (dark / light)
  // ------------------------------------------------------------------
  function wireThemeToggle() {
    const btn = document.querySelector("[data-theme-toggle]");
    if (!btn) return;
    btn.addEventListener("click", () => {
      const current = document.documentElement.getAttribute("data-theme");
      const next = current === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      try {
        localStorage.setItem(STORAGE_THEME, next);
      } catch (_) {}
    });
  }

  // ------------------------------------------------------------------
  // Solved / bookmarked decorations on practice list pages
  // ------------------------------------------------------------------
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
    const summary = document.querySelector("[data-progress-summary]");
    if (summary) {
      const countEl = summary.querySelector("[data-solved-count]");
      const total = summary.querySelector("[data-total-count]");
      if (countEl && total) {
        countEl.textContent = solved.size;
      }
    }
  }

  // ------------------------------------------------------------------
  // Problem page toolbar (bookmark / solved)
  // ------------------------------------------------------------------
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

  // ------------------------------------------------------------------
  // Bookmarks page: render items from localStorage
  // ------------------------------------------------------------------
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

  // ------------------------------------------------------------------
  // Text highlighting: select text → floating button → save to storage
  // ------------------------------------------------------------------
  function wireTextHighlights() {
    const popup = document.querySelector("[data-highlight-popup]");
    if (!popup) return;

    // Determine if we're on a page where highlighting makes sense.
    // We only allow selection inside .prose, .article-header, .lesson, etc.
    function isHighlightableNode(node) {
      let n = node;
      while (n) {
        if (n.nodeType === 1) {
          if (n.matches && (n.matches(".prose") || n.matches(".article") ||
                            n.matches(".lesson-body") || n.matches(".problem-page") ||
                            n.matches(".article-header"))) {
            return true;
          }
        }
        n = n.parentNode;
      }
      return false;
    }

    function hidePopup() {
      popup.classList.remove("visible");
    }

    function showPopupAt(rect) {
      // Position the popup just above the selection's bounding box.
      const scrollX = window.scrollX || window.pageXOffset;
      const scrollY = window.scrollY || window.pageYOffset;
      const top = rect.top + scrollY;
      const left = rect.left + scrollX + (rect.width / 2);
      popup.style.top = top + "px";
      popup.style.left = left + "px";
      popup.classList.add("visible");
    }

    function getPageContext() {
      const titleEl =
        document.querySelector(".article-header h1") ||
        document.querySelector(".page-header h1") ||
        document.querySelector("h1");
      const title = (titleEl && titleEl.textContent.trim()) || document.title;
      return {
        title,
        url: window.location.pathname + window.location.search,
      };
    }

    document.addEventListener("selectionchange", () => {
      const sel = window.getSelection();
      if (!sel || sel.isCollapsed) {
        hidePopup();
        return;
      }
      const text = sel.toString().trim();
      if (!text || text.length < 3) {
        hidePopup();
        return;
      }
      const node = sel.anchorNode;
      if (!isHighlightableNode(node)) {
        hidePopup();
        return;
      }
      const range = sel.getRangeAt(0);
      const rect = range.getBoundingClientRect();
      if (rect.width === 0 && rect.height === 0) {
        hidePopup();
        return;
      }
      showPopupAt(rect);
    });

    // Hide the popup on scroll (it would be visually stale).
    let scrollTimer = null;
    window.addEventListener("scroll", () => {
      if (scrollTimer) clearTimeout(scrollTimer);
      scrollTimer = setTimeout(() => {
        const sel = window.getSelection();
        if (!sel || sel.isCollapsed) hidePopup();
      }, 100);
    });

    popup.addEventListener("mousedown", (e) => {
      // Prevent the click from collapsing the selection before we can read it.
      e.preventDefault();
    });
    popup.addEventListener("click", () => {
      const sel = window.getSelection();
      if (!sel || sel.isCollapsed) return;
      const text = sel.toString().trim();
      if (!text) return;
      const context = getPageContext();
      const entry = {
        id: "h_" + Date.now() + "_" + Math.random().toString(36).slice(2, 8),
        text,
        title: context.title,
        url: context.url,
        timestamp: Date.now(),
      };
      const all = readArray(STORAGE_HIGHLIGHTS);
      all.unshift(entry);
      writeArray(STORAGE_HIGHLIGHTS, all);
      // Feedback animation
      popup.textContent = "✓ Saved";
      popup.style.background = "var(--accent)";
      popup.style.color = "white";
      setTimeout(() => {
        hidePopup();
        sel.removeAllRanges();
        popup.textContent = "★ Save highlight";
        popup.style.background = "";
        popup.style.color = "";
      }, 700);
    });
  }

  // ------------------------------------------------------------------
  // Highlights page: render saved highlights
  // ------------------------------------------------------------------
  function renderHighlightsPage() {
    const list = document.querySelector("[data-highlight-list]");
    const tmpl = document.getElementById("highlight-template");
    if (!list || !tmpl) return;
    const entries = readArray(STORAGE_HIGHLIGHTS);
    const emptyMsg = list.querySelector("[data-highlight-empty]");
    if (entries.length === 0) {
      if (emptyMsg) emptyMsg.style.display = "list-item";
      return;
    }
    if (emptyMsg) emptyMsg.style.display = "none";

    function formatTime(ts) {
      const d = new Date(ts);
      const now = new Date();
      const sameDay =
        d.getDate() === now.getDate() &&
        d.getMonth() === now.getMonth() &&
        d.getFullYear() === now.getFullYear();
      if (sameDay) {
        return "today " + d.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" });
      }
      return d.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
    }

    function deriveKind(url) {
      if (url.startsWith("/practice/problem/")) return "problem";
      if (url.startsWith("/practice")) return "practice";
      if (url.startsWith("/learn/")) return "lesson";
      if (url.startsWith("/learn")) return "learn";
      if (url.startsWith("/code")) return "code";
      return "page";
    }

    for (const entry of entries) {
      const node = tmpl.content.firstElementChild.cloneNode(true);
      node.setAttribute("data-id", entry.id);
      node.querySelector("[data-text]").textContent = "“" + entry.text + "”";
      const a = node.querySelector("[data-link]");
      a.setAttribute("href", entry.url);
      a.textContent = entry.title || entry.url;
      const kindEl = node.querySelector("[data-kind]");
      const kind = deriveKind(entry.url);
      kindEl.textContent = kind;
      kindEl.className = "kind kind-" + kind;
      node.querySelector("[data-time]").textContent = formatTime(entry.timestamp);
      const delBtn = node.querySelector("[data-delete]");
      delBtn.addEventListener("click", () => {
        const all = readArray(STORAGE_HIGHLIGHTS).filter((x) => x.id !== entry.id);
        writeArray(STORAGE_HIGHLIGHTS, all);
        node.remove();
        if (all.length === 0) {
          if (emptyMsg) emptyMsg.style.display = "list-item";
        }
      });
      list.appendChild(node);
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    wireThemeToggle();
    decorateProblemLists();
    wireProblemToolbar();
    renderBookmarksPage();
    wireTextHighlights();
    renderHighlightsPage();
  });
})();
