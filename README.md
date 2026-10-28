# search-time
# NYT Article Search Interface

A command-line program for searching the New York Times Article Search API. You can set a search query and date range, browse results page by page, count article sections and keyword subjects across every page of results, and export those counts to a CSV file.

By default, the program searches for news articles about **skateboarding** between **2025-01-01** and **2025-02-01**.

---

## Table of Contents

1. [Requirements](#requirements)
2. [Setup](#setup)
3. [Running the Program](#running-the-program)
4. [Menu Guide](#menu-guide)
5. [Understanding Search Parameters](#understanding-search-parameters)
6. [CSV Output](#csv-output)
7. [Important Notes and Limits](#important-notes-and-limits)
8. [Troubleshooting](#troubleshooting)

---

## Requirements

- Python 3.8 or newer
- The `requests` library
- A free NYT Developer API key

Install the dependency:

```bash
pip install requests
```

## Setup

### 1. Get an API key

1. Create an account at [developer.nytimes.com](https://developer.nytimes.com).
2. Create a new app and enable the **Article Search API**.
3. Copy the API key it gives you.

### 2. Add the key to the program

Open the script and paste your key into the `apiKey` variable near the top:

```python
apiKey = 'YOUR_API_KEY_HERE'
```

> **Keep your key private.** Do not post it publicly or commit it to GitHub. A safer option is to store it in an environment variable and load it with `apiKey = os.environ['NYT_API_KEY']`.

## Running the Program

From a terminal, run the script (replace `final.py` with your file name):

```bash
python3 final.py
```

You will see a welcome message and the task menu. Type a number from the menu and press **Enter**. Type `.` and press **Enter** to exit.

---

## Menu Guide

### General

| Option | Task | What it does |
|--------|------|--------------|
| `0` | Help | Shows basic usage instructions. |
| `1` | Show Search Instance | Displays the current search settings (section, query, dates, page). |
| `.` | Exit | Closes the program. |

### Changing Search Parameters

| Option | Task | What it does |
|--------|------|--------------|
| `2` | Change All Search Parameters | Walks you through changing the query, begin date, end date, and page number one after another. |
| `3` | Change Query | Sets a new search term (for example, `surfing`). |
| `4` | Change Begin Date | Sets the start of the date range. |
| `5` | Change End Date | Sets the end of the date range. |
| `6` | Change Page Number | Sets which page of results the "current page" tasks use. |

Dates must be entered as numbers in `YYYYMMDD` format, for example `20250315` for March 15, 2025. The query cannot be empty. If you enter something invalid, the program tells you and keeps the old value.

### Viewing Data (Current Page)

These tasks use the page number currently set in your search instance. Each page contains up to 10 articles.

| Option | Task | What it does |
|--------|------|--------------|
| `7` | Get Number of Hits | Shows how many articles match your search in total. |
| `8` | Get Page Response Data | Prints the raw API response for the current page. |
| `9` | Get Article Names | Lists the headlines of the articles on the current page. |
| `10` | Get Current Page Subjects | Lists the keyword subject types found on the page (such as `subject`, `persons`, `glocations`, `organizations`). |
| `11` | Get Current Page Keywords by Subject | Shows the subjects, then asks you to pick one and lists the keywords under it. |
| `12` | Get Current Page Section Count | Counts how many articles on the page belong to each NYT section (Sports, Style, and so on). |

### Viewing Data (All Pages)

These tasks make one API request per page, pausing 15 seconds between requests, so they can take several minutes.

| Option | Task | What it does |
|--------|------|--------------|
| `13` | Get All Page Subjects | Lists the keyword subject types found across every page of results. |
| `14` | Get All Page Section Counts | Counts articles per section across every page of results. |

### Exporting to CSV

| Option | Task | What it does |
|--------|------|--------------|
| `15` | Load All Page Keyword by Subject Count | Asks you to choose a subject, counts how often each keyword under it appears across all pages, and saves the result to `data.csv`. |
| `16` | Load All Page Section Count Data To CSV | Counts articles per section across all pages and saves the result to `data.csv`. |

---

## Understanding Search Parameters

| Parameter | Current default | Notes |
|-----------|-----------------|-------|
| Query | `skateboarding` | The search term. |
| Section filter | `News` | Only articles with material type "News". This is fixed in the code (`fq`). |
| Begin Date | `20250101` | Format `YYYYMMDD`. |
| End Date | `20250201` | Format `YYYYMMDD`. |
| Page | `0` | Page numbering starts at 0. |

To change the fixed News filter, edit the `fq` value in the `params` dictionary at the top of the `Search` class.

### Keyword subject types

NYT articles are tagged with keywords, and each keyword has a subject type. Common ones:

- `subject`: topics and themes
- `persons`: people mentioned
- `glocations`: geographic locations
- `organizations`: companies, teams, and groups

When you pick a subject for option `11` or `15`, type it exactly as it appears in the list shown on screen.

---

## CSV Output

Options `15` and `16` write a file named `data.csv` in the same folder as the script. It has two columns:

```
Value,Count
Brooklyn (NYC),12
Los Angeles (Calif),9
```

- **Value**: the keyword or section name
- **Count**: how many articles it appeared in

Each export **overwrites** the previous `data.csv`. Rename or move the file if you want to keep it before running another export.

---

## Important Notes and Limits

- **Rate limits.** The NYT API allows roughly 5 requests per minute and 500 per day. The all-pages tasks wait 15 seconds between pages to stay under the per-minute limit, but nearly every menu option makes at least one API request, so heavy use can still hit the limit.
- **Long runtimes.** A search with 100 matching articles needs about 10 pages, which takes around 2.5 minutes. Larger searches take proportionally longer.
- **Page cap.** The Article Search API only serves up to 100 pages (1,000 articles) per search. Narrow your date range if a search has more hits than that.
- **Page number is changed by all-page tasks.** After running options 13, 14, 15, or 16, the "current page" setting will be left on the last page processed. Use option `6` to reset it to `0`.
- **Keyword tasks may not cover every article.** Some keyword tasks currently read keywords from only the first article on each page. Treat those counts as partial until that is updated.

---

## Troubleshooting

**`KeyError: 'response'`**
The API returned an error instead of results. This is usually a rate limit (too many requests too quickly), an invalid API key, or an app that does not have the Article Search API enabled. Wait a few minutes and try again, and confirm your key is correct.

**`IndexError: list index out of range`**
The current page has no articles. This happens when the page number is higher than the number of available pages, or when the search returns zero hits. Check the hit count with option `7` and set the page with option `6`.

**`Invalid Begin Date` / `Invalid End Date` / `Invalid Page Number`**
The value was not a whole number. Enter digits only, with no dashes or slashes (`20250315`, not `2025-03-15`).

**The program seems frozen during options 13 to 16**
It is waiting 15 seconds between pages on purpose. Watch for the `Now running page N` messages to see progress.
