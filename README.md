# Venus Chetwani · Interactive Resume

A scroll-driven platformer resume. Scroll to run through six levels (About, Skills, Experience, Projects, Education, Contact), collect coins, press **Enter** to jump.

**Quick view:** a plain one-page version of the resume. Phones open it by default, and on desktop it opens from the "Quick view" button or the hint under the hero. Link straight to it with `https://venuschetwanii.github.io/#quick`, which is handy for job applications.

## Files
- `index.html` — self-contained build that GitHub Pages serves. Don't edit it by hand; it is generated from `src/`.
- `src/` — editable source (`Interactive Resume.dc.html` + its runtime `support.js`). Serve the folder over HTTP to run it.
- `tools/sync.py` — copies the source into `index.html`.
- `Venus Chetwani Resume.pdf` — linked from the Download buttons.

## To update
1. Edit `src/Interactive Resume.dc.html`.
   - Resume text appears twice: once in the game levels and once in the `QUICK VIEW` block near the end of the markup. Edit both.
2. Run `python tools/sync.py` from the repo root to rebuild `index.html`.
3. Open `index.html` in a browser to check, then commit and push.

Resume PDF: replace `Venus Chetwani Resume.pdf` (keep the same filename).
