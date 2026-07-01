# 100Hires Portfolio Project
## Bimo Pamungkas — Junior Growth Marketing Specialist

---

## Step 1: Tools Installed

### 1. Cursor IDE
- Website: cursor.com
- AI-powered code editor used as the main development environment
- Status: Already installed and running

### 2. Claude Code (Cursor Extension)
- Developer: Anthropic
- AI assistant extension integrated directly into Cursor IDE
- Status: Successfully installed

### 3. Codex (Cursor Extension)
- Developer: OpenAI
- AI coding agent extension for Cursor IDE
- Status: Successfully installed

**Steps Completed:**
- [x] Cursor IDE installed and connected to GitHub
- [x] Claude Code extension installed (by Anthropic)
- [x] Codex extension installed (by OpenAI)
- [x] GitHub account verified
- [x] Created public repository: 100hires-portfolio
- [x] Created and edited this README.md file

**Issues Encountered & How I Solved Them:**

*Issue 1: Could not find Extensions panel with Ctrl+Shift+X initially*
Solution: Cursor opened in a different view (Cloud Agents). Clicked "Editor Window" to switch to the correct editor view, then Ctrl+Shift+X worked.

*Issue 2: Claude Code not found in Customize Marketplace*
Solution: The Customize section is for plugins, not extensions. Used the correct Extensions panel (Ctrl+Shift+X) and found Claude Code by Anthropic with 28M installs.

---

## Step 2: Research Project — Cold Outreach Pipeline for B2B SaaS

### Topic Chosen
**Cold outreach pipeline for B2B SaaS.** I picked this over the other 7 options because it overlaps directly with outbound work I already do professionally, which made it easier to judge whether a source was genuinely tactical versus just generic sales content.

### Approach
I split the 10 experts into two collection methods based on what each platform's API/tooling actually supports well:

- **5 YouTube creators** — collected via `youtube-transcript-api` (official captions API, not scraping). Videos were filtered by upload date and title keywords (cold email, prospecting, lead gen, outbound, B2B/SaaS sales) to avoid pulling off-topic content.
- **5 LinkedIn authors** — collected via a no-login/no-cookie Apify scraper (`harvestapi/linkedin-profile-posts`), which pulls public post data without requiring a personal LinkedIn session. This was a deliberate choice: LinkedIn's ToS makes cookie-based scraping with a personal account risky, so I used a public-data-only method instead.

Full list of experts, why each was chosen, and links to every piece of content collected: **[research/sources.md](research/sources.md)**

### Repository Structure
```
research/
├── sources.md                     # All 10 experts, rationale, links to every source
├── scripts/
│   └── collect_youtube_transcripts.py
├── youtube-transcripts/
│   ├── patrick-dang/       (7 transcripts)
│   ├── alex-berman/        (8 transcripts)
│   ├── tim-dodd/           (8 transcripts)
│   ├── jeremy-miner/       (8 transcripts)
│   └── will-barron/        (7 transcripts)
└── linkedin-posts/
    ├── josh-braun/         (8 posts)
    ├── jack-reamer/        (8 posts)
    ├── alex-vacca/         (7 posts)
    ├── patrick-spychalski/ (8 posts)
    └── eric-nowoslawski/   (8 posts)
```

**Total: 10 experts, 77 individual sources (38 YouTube transcripts + 39 LinkedIn posts).**

### Quality Control
Volume wasn't the goal — relevance was. After the first LinkedIn scrape, I manually reviewed all 40 posts for topical relevance. One expert I'd originally picked (Samantha McKenna) turned out to have a recent post history skewed toward personal branding rather than outreach tactics, so I swapped her for Eric Nowoslawski (Growth Engine X), whose recent posts were 8/8 directly on-topic (reply rate optimization, list-building automation, AI-assisted prospecting). This is documented in the commit history and in `sources.md`.

### Issues Encountered & How I Solved Them

**Issue 1: YouTube transcript API got IP-blocked mid-batch**
After collecting transcripts for 3 of 5 channels, the transcript endpoint started returning 429s tied to my IP, not per-video rate limiting. Switching to a different network (mobile hotspot) resolved it; no changes to the script were needed.

**Issue 2: Wrong LinkedIn profile URLs returned 0 or partial results**
Two of the five LinkedIn profiles I initially used had incorrect slugs (e.g. `alexvacca` instead of the correct `alex-vacca`), which silently returned 0-2 posts instead of erroring. Cross-checked each profile via search before re-running to get full 7-8 post batches.

**Issue 3: GitHub branch protection blocked direct pushes to `main`**
Pushing the LinkedIn research folder directly to `main` was rejected by repository branch protection rules. Solved by pushing to a feature branch and merging via Pull Request instead — which also left a cleaner, more reviewable commit history.

**Issue 4: First LinkedIn push accidentally skipped `sources.md`**
The initial LinkedIn commit added the post files but missed updating `sources.md` with the corresponding source entries. Caught this during a manual QA pass and backfilled all 5 LinkedIn sections in a follow-up PR.

---

*Created as part of the 100Hires selection process | June–July 2026*
