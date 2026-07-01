# Eric Nowoslawski

**Tanggal:** 2026-06-29T17:00:06.372Z
**Likes:** 132
**Comments:** 32
**URL:** https://www.linkedin.com/posts/outboundphd_i-scrape-the-entire-united-states-off-google-activity-7477405549056425984-3UVi

---

I scrape the entire United States off Google Maps for $19 a category. Tell your agent to read this post and get it done by end of day.

A huge chunk of the businesses you want to reach funeral homes, HVAC shops, local gyms, etc but they have no LinkedIn presence. The databases scraping LinkedIn never see them. So you have to build the list yourself.

Google Maps is the best place to do it.

The tool is one API endpoint on RapidAPI — "Maps Data" by Aleksandr Vikourev.

The pricing is insane: 3 million requests a month for $100.

One vertical of 20 categories scrapes the entire US for about $100. Most lists you'll want need 3 or 4 categories, so you're looking at way less than that.

How it works:

1. Load all 42,734 US zip codes.
2. Pick your category list.
3. Hit the endpoint per zip, limit to the first 20 results.

You get back the business name, address, rating, phone, and the website, etc.

The one nuance most people miss: find every category a business hides under. A funeral home also shows up as a "memorial park." A restaurant splits into American, Mediterranean, French, Chinese. Use the data to pull every category that fits your ICP, or you'll leave half the list on the table.

Then clean it for free. HTML2Text (open source) pulls the homepage text, and Gemma 4 — the 12 billion parameter one — running locally in Ollama reads every site and confirms it's actually the kind of company you want. Costs you nothing.

I put the US zip code file and 12 million US Google Maps businesses in a free GitHub repo called Cold Outbound Skills. Link in the comments.

Honestly, you don't even need to follow along. Point your AI agent at the video and tell it "set this up for me."
