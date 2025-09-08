import requests
import os
from urllib.parse import urlparse
from pathlib import Path

def is_valid_image(response):
    content_type = response.headers.get('Content-Type', '')
    return content_type.startswith('image/')

def get_filename_from_url(url):
    parsed = urlparse(url)
    name = os.path.basename(parsed.path)
    return name if name else "downloaded_image.jpg"

def download_image(url, dest_folder="Fetched_Images"):
    try:
        # Create folder if not exists
        os.makedirs(dest_folder, exist_ok=True)

        # Send GET request
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Check Content-Type
        if not is_valid_image(response):
            print(f"✗ Skipped: {url} — Not an image.")
            return

        # Extract filename
        filename = get_filename_from_url(url)
        filepath = os.path.join(dest_folder, filename)

        # Check for duplicates
        if os.path.exists(filepath):
            print(f"✓ Skipped: {filename} — Already downloaded.")
            return

        # Save image
        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ Error fetching {url}: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher - Community Edition")
    print("A tool for mindfully collecting images from the web\n")

    # Prompt user for multiple URLs (comma or newline separated)
    print("Enter image URLs (separate by comma or newline).")
    print("Type 'done' on a new line when you're finished:\n")

    urls = []
    while True:
        line = input()
        if line.strip().lower() == "done":
            break
        urls.extend([u.strip() for u in line.split(',') if u.strip()])

    print("\n📥 Starting download...\n")

    for url in urls:
        download_image(url)

    print("\nConnection strengthened. Community enriched.")
    print("A person is a person through other persons. – Ubuntu\n")

if __name__ == "__main__":
    main()
