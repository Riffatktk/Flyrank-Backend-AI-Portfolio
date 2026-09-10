/**
 * case-studies.js — renders CASES (from cases.js) into #cs-list.
 * You should never need to edit this file to add a new case;
 * edit cases.js instead.
 */
(function () {
  const list = document.getElementById("cs-list");
  if (!list || typeof CASES === "undefined") return;

  const esc = (str) =>
    String(str).replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
    }[c]));

  list.innerHTML = CASES.map((c) => `
    <article class="cs-card">
      <div class="cs-card-top">
        <span class="cs-id">${esc(c.id)}</span>
        <span class="cs-date">${esc(c.date)}</span>
      </div>
      <h3 class="cs-title">${esc(c.title)}</h3>
      <div class="cs-stack">
        ${c.stack.map((s) => `<span class="cs-tag">${esc(s)}</span>`).join("")}
      </div>
      <p class="cs-beat"><span class="cs-beat-label">problem</span>${esc(c.problem)}</p>
      <p class="cs-beat"><span class="cs-beat-label">did</span>${esc(c.action)}</p>
      <p class="cs-beat"><span class="cs-beat-label">result</span>${esc(c.result)}</p>
      <div class="cs-links">
        ${c.links && c.links.repo ? `<a href="${esc(c.links.repo)}" target="_blank" rel="noopener">repo</a>` : ""}
        ${c.links && c.links.writeup ? `<a href="${esc(c.links.writeup)}" target="_blank" rel="noopener">write-up</a>` : ""}
      </div>
    </article>
  `).join("");
})();