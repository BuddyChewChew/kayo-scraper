# Kayo Channel Scraper

> [!WARNING]
> This project is for informational and educational purposes only. The author takes no responsibility for any issues, damages, or losses that may arise from the use of these scripts or the generated files. Use at your own risk.

This script scrapes channel data from the Kayo app.json.gz file and generates both an M3U playlist and an EPG guide.

## Features

- Downloads and decompresses the Kayo app.json.gz file
- Generates an M3U playlist with channel information
- Creates an EPG guide with 24 hours of placeholder programming
- Includes channel logos and metadata

## Requirements

- Python 3.8+
- Required packages: requests, gzip, xmltodict, dateutil

## Installation

1. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the script:
```bash
python kayo_scraper.py
```

The script will generate two files:
- `kayo_channels.m3u`: M3U playlist file
- `kayo_epg.xml`: EPG guide file

## Disclaimer

This project is for educational purposes only. The generated files may not contain accurate or up-to-date programming information. Always refer to the official Kayo app for the most accurate channel listings and programming schedules.
