# Eric Nowoslawski

**Tanggal:** 2026-06-30T13:45:06.677Z
**Likes:** 55
**Comments:** 14
**URL:** https://www.linkedin.com/posts/outboundphd_i-ran-a-test-to-find-local-business-owners-activity-7477718864844206082-Eso_

---

I ran a test to find local business owners across 5 different providers. The cheapest option won. It was also the best.

Here's the problem with local lead gen: a plumbing company, a dentist, a local shop don't have a LinkedIn profile.

And almost every big database are built on LinkedIn data. So they just don't have these people.

So we put 5 options against each other: SmartLead Email Finder, Prospeo, Blitz API, OpenWebNinja (which is really just a Google search), and an open-source website scrape.

The winner wasn't a paid API.

It was scraping the business's own website with an open-source library and reading it with a local LLM.

Here's the stack:

1. HTML2Text (open source) converts the homepage, about, team, and contact pages into plain text an LLM can read.

2. Gemma 4 (the 12B version) running locally on Ollama reads it and pulls the owner's name. It's on my laptop, it's free, and it doesn't matter how many sites I process, I can just rip through all of them.

3. If that comes up empty, we Google "who owns [business] in [city]" through OpenWeb Ninja including the AI overview answer and parse that with Gemma 4 too.

The whole website-scrape side costs $0, because the LLM runs locally and the library is open source. OpenWebNinja is the only paid piece, and it's cheap.

It's exactly what I'd do if I were to pass to a teammate. "Here's 100 local businesses, go find the owner." They'd check the website and Google it. We just automated that.

We still check Blitz and Prospeo first. If someone literally put "I own this business, here's my site" on their LinkedIn, that fidelity is worth paying for. But when the LinkedIn scrapers miss, the free website scrape catches what they leave behind.

If you do any local lead gen: download HTML2Text, pull Gemma 4 from Ollama, grab an OpenWebNinja key, and point your AI agent at it.
