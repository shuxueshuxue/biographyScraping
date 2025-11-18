"""
Download celebrity photos from Wikipedia
Uses publicly available images
"""

import requests
from pathlib import Path
import time

# Celebrity names and their Wikipedia image URLs
# These are publicly available photos from Wikipedia/Wikimedia Commons
CELEBRITIES = {
    "steve_jobs": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Steve_Jobs_Headshot_2010-CROP_%28cropped_2%29.jpg/440px-Steve_Jobs_Headshot_2010-CROP_%28cropped_2%29.jpg",
    "oprah_winfrey": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Oprah_in_2014.jpg/440px-Oprah_in_2014.jpg",
    "elon_musk": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Elon_Musk_Royal_Society_%28crop2%29.jpg/440px-Elon_Musk_Royal_Society_%28crop2%29.jpg",
    "albert_einstein": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Albert_Einstein_Head.jpg/440px-Albert_Einstein_Head.jpg",
    "marie_curie": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Marie_Curie_c._1920s.jpg/440px-Marie_Curie_c._1920s.jpg",
    "nelson_mandela": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Nelson_Mandela_1994.jpg/440px-Nelson_Mandela_1994.jpg",
    "maya_angelou": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Angelou_at_Clinton_inauguration_%28cropped_2%29.jpg/440px-Angelou_at_Clinton_inauguration_%28cropped_2%29.jpg",
    "stephen_hawking": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Stephen_Hawking.StarChild.jpg/440px-Stephen_Hawking.StarChild.jpg",
    "malala_yousafzai": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Malala_Yousafzai_2015.jpg/440px-Malala_Yousafzai_2015.jpg",
    "barack_obama": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/President_Barack_Obama.jpg/440px-President_Barack_Obama.jpg",
}

def download_photos():
    """Download celebrity photos to frontend/images/"""

    output_dir = Path("frontend/images")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Downloading celebrity photos...")
    print("="*80)

    for name, url in CELEBRITIES.items():
        output_file = output_dir / f"{name}.jpg"

        if output_file.exists():
            print(f"✓ {name}.jpg already exists")
            continue

        try:
            print(f"Downloading {name}...", end=" ")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            with open(output_file, 'wb') as f:
                f.write(response.content)

            print("✓")
            time.sleep(0.5)  # Be nice to Wikipedia servers

        except Exception as e:
            print(f"✗ Error: {e}")

    print("="*80)
    print(f"Downloaded {len(list(output_dir.glob('*.jpg')))} photos to {output_dir}")

if __name__ == "__main__":
    download_photos()
