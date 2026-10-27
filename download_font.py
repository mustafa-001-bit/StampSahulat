import os
import requests

# Pure static TrueType font (No variable tables)
FONT_URL = "https://raw.githubusercontent.com/googlefonts/noto-fonts/main/hinted/ttf/NotoNastaliqUrdu/NotoNastaliqUrdu-Regular.ttf"
DEST_PATH = os.path.join("fonts", "UrduNastaliq.ttf")

print("Static Urdu Nastaliq font download ho raha hai...")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(FONT_URL, headers=headers, timeout=45)
if response.status_code == 200:
    with open(DEST_PATH, "wb") as f:
        f.write(response.content)
    print("Mubarak! Asal Static Urdu font replace ho gaya hai.")
else:
    print(f"Error: {response.status_code}")