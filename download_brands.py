# download_brands.py
# pip install icrawler

import os
from icrawler.builtin import BingImageCrawler, GoogleImageCrawler

# Pakistani beverage brands (with search-friendly keywords)
BRANDS = {
    "cocacola":   ["Coca Cola bottle Pakistan", "Coke bottle"],
    "pepsi":      ["Pepsi bottle Pakistan", "Pepsi cold drink bottle"],
    "dew":        ["Mountain Dew bottle Pakistan", "Mountain Dew bottle"],
    "mirinda":    ["Mirinda bottle Pakistan", "Mirinda orange bottle"],
    "fizzup":     ["Fizzup drink Pakistan", "Fizzup bottle"],
    "nextcola":   ["Next Cola Pakistan", "Next Cola bottle"],
    "gourmet":    ["Gourmet cola bottle Pakistan", "Gourmet drink bottle"],
    "7up":        ["7up bottle Pakistan", "7up cold drink bottle"],
    "sprite":     ["Sprite bottle Pakistan", "Sprite cold drink bottle"],
    "sting":      ["Sting energy drink Pakistan", "Sting bottle"],
    "slice":      ["Slice mango drink Pakistan", "Slice juice bottle"],
    "fresher":    ["Fresher juice Pakistan", "Fresher mango juice"],
    "nestlejuice":["Nestle juice Pakistan", "Nestle Fruita Vitals"],
    "marinda":    ["Mirinda Pakistan bottle"],  # alt spelling
    "team":       ["Team drink Pakistan", "Team cola bottle"],
    "bubbleup":   ["Bubble Up drink Pakistan", "Bubble Up bottle"],
}

IMAGES_PER_BRAND = 30
OUTPUT_DIR = "dataset"

def download_for_brand(brand, keywords, count):
    folder = os.path.join(OUTPUT_DIR, brand)
    os.makedirs(folder, exist_ok=True)

    # Use primary keyword for folder naming, but crawl multiple keywords
    remaining = count
    per_keyword = max(1, count // len(keywords))

    for kw in keywords:
        if remaining <= 0:
            break
        print(f"[{brand}] Searching: {kw} ({per_keyword} imgs)")
        crawler = BingImageCrawler(
            feeder_threads=1,
            parser_threads=1,
            downloader_threads=4,
            storage={"root_dir": folder},
        )
        try:
            crawler.crawl(
                keyword=kw,
                max_num=per_keyword,
                file_idx_offset="auto",  # avoid overwriting
                min_size=(200, 200),
            )
        except Exception as e:
            print(f"  ⚠️ failed on '{kw}': {e}")
        remaining -= per_keyword

    # Final count
    actual = len([f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))])
    print(f"[{brand}] ✅ {actual} images in {folder}\n")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for brand, keywords in BRANDS.items():
        download_for_brand(brand, keywords, IMAGES_PER_BRAND)

if __name__ == "__main__":
    main()