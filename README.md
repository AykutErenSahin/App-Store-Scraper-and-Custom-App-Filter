
# iOS App Store App Filter

## Overview

This project is a Python script for fetching and filtering iOS App Store metadata using the iTunes Search API.  
It allows you to filter app lists based on custom business rules, such as:

- Developers you've already contacted (tracked via a CSV/Excel file)  
- Apps older than 1 year  
- Apps not updated in the last 90 days
- Only contact one app per developer

The result is a refined list of apps that are more relevant for outreach, partnership, or analysis.

---

## Features

- Fetch app metadata via App Store API  
- Filter out apps by:
  - Contacted developer IDs
  - Release date (exclude apps older than 1 year)
  - Last update date (exclude apps not updated in last 180 days)
- Manage contact history via CSV/Excel  
- Export filtered app lists to CSV  

---

## Requirements

- Python 3.7+  
- Libraries:
  - pandas
  - requests
  - csv
  - json
  - argparse

Install dependencies with:

```bash
pip install pandas requests
```

---

## Usage

```bash
python main.py app_list.csv deal_list.csv
```

**Arguments:**

- `app_list.csv`: The file containing app IDs for which we are trying to retrieve metadata.  
- `deal_list.csv`: The file tracking contacted developer IDs.  

---

## Output

The script will output a filtered CSV file named:

```
filtered_apps_<current_date>.csv
```

This file will include apps that:

- Are not yet contacted  
- Are actively maintained (updated in the last 180 days)  
- Are relatively recent (released within the last 12 months)

---

## Author

Aykut Eren Şahin
