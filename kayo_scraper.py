import requests
import gzip
import xmltodict
from datetime import datetime, timedelta
import json

class KayoScraper:
    def __init__(self):
        self.base_url = "https://github.com/matthuisman/i.mjh.nz/raw/refs/heads/master/Kayo/app.json.gz"
        self.m3u_file = "kayo_channels.m3u"
        self.epg_file = "kayo_epg.xml"

    def download_data(self):
        """Download and decompress the app.json.gz file"""
        response = requests.get(self.base_url)
        if response.status_code == 200:
            return gzip.decompress(response.content)
        else:
            raise Exception(f"Failed to download data: {response.status_code}")

    def generate_m3u(self, channels):
        """Generate M3U playlist file"""
        with open(self.m3u_file, 'w', encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            for channel in channels:
                if 'stream' in channel:
                    f.write(f"#EXTINF:-1 group-title=\"Kayo\" tvg-id=\"{channel['id']}\" tvg-name=\"{channel['name']}\" tvg-logo=\"{channel.get('logo', '')}\",{channel['name']}\n")
                    f.write(f"{channel['stream']}\n")
        print(f"M3U file generated with {len(channels)} channels.")

    def generate_epg(self, channels):
        """Generate EPG XML file"""
        epg = {
            "tv": {
                "@generator-info-name": "Kayo EPG Generator",
                "@generator-info-url": "https://github.com/matthuisman/i.mjh.nz",
                "@source-info-url": "https://github.com/matthuisman/i.mjh.nz",
                "channel": [],
                "programme": []
            }
        }

        # Add channels to EPG
        for channel in channels:
            if 'stream' in channel:
                epg['tv']['channel'].append({
                    "@id": channel['id'],
                    "display-name": [channel['name']],
                    "icon": [{"@src": channel.get('logo', '')}] if channel.get('logo') else []
                })

        # Add placeholder programmes (24 hours of programming)
        now = datetime.utcnow()
        for channel in channels:
            if 'stream' in channel:
                for i in range(24):
                    start_time = now + timedelta(hours=i)
                    end_time = start_time + timedelta(hours=1)
                    epg['tv']['programme'].append({
                        "@channel": channel['id'],
                        "@start": start_time.strftime("%Y%m%d%H%M%S") + " +0000",
                        "@stop": end_time.strftime("%Y%m%d%H%M%S") + " +0000",
                        "title": ["Placeholder Program"],
                        "desc": ["This is a placeholder program. Please check the official Kayo app for accurate programming information."],
                        "category": ["Placeholder"]
                    })

        # Write EPG to file
        with open(self.epg_file, 'w', encoding='utf-8') as f:
            f.write(xmltodict.unparse(epg, pretty=True))
        print("EPG file generated.")

    def run(self):
        """Main function to run the scraper"""
        try:
            # Download and parse data
            data = self.download_data()
            channels = json.loads(data)

            # Generate M3U playlist
            self.generate_m3u(channels)

            # Generate EPG
            self.generate_epg(channels)

            print("Scraping completed successfully!")
            print(f"M3U playlist saved to: {self.m3u_file}")
            print(f"EPG guide saved to: {self.epg_file}")

        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    scraper = KayoScraper()
    scraper.run()
