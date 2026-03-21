# Automated Weather Pipeline

Automated pipeline that fetches daily weather from three cities including HuaHin, Bangkok, and Aalborg, stores data in SQLite database, and use AI to generate a bilingual poem. The pipeline publishes automatically to a GitHub page website every evening.

## Site: [https://maximona-ailee.github.io/automated-weather-pipeline/]

## Structure:
```
automated-weather-pipeline/
├── .github/
│   └── workflows/
│       └── pipeline.yml      # GitHub Actions workflow
├── docs/
│   ├── index.html            # GitHub Pages website
│   └── poem.txt              # Generated poem (auto-updated daily)
├── fetch.py                  # Weather fetching + database storage
├── generate.py               # AI poem generation
├── main.py                   # Entry point
├── weather.db                # SQLite database
└── README.md
```

## Tools:
 
| Tool | Purpose |
|------|---------|
| [Open-Meteo API](https://open-meteo.com/) | Free weather forecast data |
| SQLite | Local weather data storage |
| [Groq API](https://groq.com/) | Fast AI inference for poem generation |
| GitHub Actions | Automated daily scheduling |
| GitHub Pages | Free static site hosting |

## Setup
 
1. Clone the repo
```bash
git clone https://github.com/Maximona-Ailee/automated-weather-pipeline.git
cd automated-weather-pipeline
```
 
2. Install dependencies
```bash
pip install requests groq
```
 
3. Set your Groq API key
Add `GROQ_API_KEY` as a GitHub Actions secret:
- Go to **Settings → Secrets and variables → Actions → New repository secret**
 
4. Enable GitHub Pages
- Go to **Settings → Pages**
- Set source to `Deploy from a branch`, branch `main`, folder `/docs`
 
---
 
## How the Automation Works
 
The workflow runs on a cron schedule (`0 19 * * *` = 20:00 Denmark time) and also supports manual triggering via `workflow_dispatch`.
 
```yaml
on:
  schedule:
    - cron: '0 19 * * *'
  workflow_dispatch:
```
 
After running the pipeline, it automatically commits and pushes the updated `poem.txt` back to the repository, which triggers GitHub Pages to redeploy.