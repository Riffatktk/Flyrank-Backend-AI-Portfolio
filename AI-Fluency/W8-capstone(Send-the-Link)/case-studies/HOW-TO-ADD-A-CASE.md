# How I add the next case study

**Where it goes:** `cases.js`, in the portfolio repo, root of the
`case-studies/` folder. Nothing else in the site changes.

**Steps:**
1. Open `cases.js`.
2. Copy the most recent case object, paste it at the top of the `CASES`
   array (newest first), and give it the next `case_0XX` id.
3. Fill in the three beats, same shape as Week 2:
   - **problem** — one or two sentences on what was broken or missing.
   - **did** — what I actually built or changed.
   - **result** — what came of it: a number, a review comment, a thing
     that now works that didn't before.
4. Add the stack tags and a repo link.
5. Commit and push. `case-studies.js` re-renders it automatically —
   no HTML or CSS to touch.

**Time cost:** ~10 minutes once the work itself is done.