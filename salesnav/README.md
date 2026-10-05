# Sales Navigator lead collector

1. On your own computer: `git clone` this repo, `git checkout claude/practical-noether-gdwus8`, `pip install openpyxl`.
2. Install the **Claude in Chrome** extension and log in to Sales Navigator in that Chrome.
3. In the repo folder run `claude` and say: **"Use the salesnav-lead-collector agent to process the next 15 companies."**
   - It reads `queue.csv`, opens each company's search, records every lead on all result pages into `leads.csv`, and marks the company done.
   - Run it again for the next batch. It picks up where it stopped.
4. Get emails and phones: in Sales Nav, save the leads to a Lead List, then run Apollo / Lusha / ContactOut on that list and export it as `salesnav/enriched.csv`.
5. Run `python3 scripts/merge_salesnav_leads.py` to build the **Sales Nav Leads** sheet in the workbook (ranked by priority, with emails and phones filled from `enriched.csv`).

Keep batches small (about 15 companies, a few batches a day). Automated browsing at high volume can get a LinkedIn account restricted.
