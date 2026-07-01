# Patrick Spychalski

**Tanggal:** 2026-06-30T17:14:56.616Z
**Likes:** 27
**Comments:** 9
**URL:** https://www.linkedin.com/posts/patrickspychalski_who-is-to-blame-when-an-mql-lead-handoff-activity-7477771670875828224-1M1T

---

Who is to blame when an MQL lead handoff goes wrong-- marketing, or sales? 

This is a trick question. If your GTM org is set up correctly, it's neither. The real responsibility lies on the GTM Engineer. 

I've heard dozens of stories now where marketing leaders tell me the sales team can't convert the leads they're giving them. Then, the sales team then tells me the marketers don't send them qualified leads, and they take too long to send them. 

There is a process that solves this completely. Here's how to build it:

1. Get your marketing and sales teams in a room to agree upon a "perfect" ICP scoring model. They often have different opinions on what their ICP is. This shouldn't be subjective; any mature sales org has enough closed-won deals to reverse engineer a profile. Use your CRM to create this model and then get sign-off from both teams. 

2. Ask your sales team what their ideal handoff system would look like. Do they want a slack noti every time a new lead comes in? Should it go to the CRM? Every team attacks this differently, but adoption is important, so make sure to ask them. 

3. Have your GTM engineer create a system in Claude that:
- Ingests leads from marketing initiatives (ads, website visits, events), into an enrichment environment (like Clay or Claude Code)
- Qualifies those leads using the agreed-upon ICP model
- Enriches qualified leads for key info that the sales team finds to be important when prospecting the lead
- Uses assignment logic to send the lead to the right salesperson
- Sends the qualified, enriched leads via the method of their choice for outreach

This system, if built correctly, sends leads immediately to sales with everything they need to run outreach to them. It also helps eliminate friction between teams. 

The beef ends here! If you're a marketing or sales team member reading this, go pester your automation person to figure this out (and if you don't have one of those, hit us up 🫡 )
