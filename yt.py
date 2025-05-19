import yt_dlp
import argparse
import re
import sys
from urllib.parse import urlparse
from subtitle_utils import convert_and_cleanup_subtitles
from database import load_urls, save_urls, clear_urls

class Config:
    video_url = 'https://youtu.be/NZw6_w1UWBE?si=kJNyHsJQYw0kSdDe'  # Replace with your video URL
    cookies_file = 'cookies.txt'  # Replace with your cookies file path
    output_path = '/storage/9C1C-01E7/Anime/'  # Directory where subtitles will be saved
    

def is_valid_url(url):
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])

def download_subtitles(video_urls, cookies_file, output_path):
    ydl_opts = {
        'writesubtitles': True,
        'skip_download': True,
        'subtitleslangs': ['id'],
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'cookiefile': cookies_file
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(video_urls)
    except Exception as e:
        print(f"Error downloading subtitles: {e}")
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description="Download and convert subtitles from provided URLs.")
    parser.add_argument("url", nargs='?', default=None, help="The video URL")
    parser.add_argument("--multiple-download", action='store_true', help="Flag to enable multiple URL downloads")
    parser.add_argument("--resume", action='store_true', help="Resume interrupted downloads")
    parser.add_argument("--clear-db", action='store_true', help="Clear stored URLs and start fresh")
    args = parser.parse_args()

    config = Config()

    if args.clear_db:
        clear_urls()
        sys.exit("Cleared stored URLs. Exiting.")

    urls = []

    if args.resume:
        urls = load_urls()
        if not urls:
            sys.exit("No URLs to resume. Exiting.")
        print("Resuming downloads from stored URLs...")
    elif args.multiple_download:
        try:
            while True:
                url = input("Enter a video URL (or type 'done' to finish, 'exit' to quit without saving): ").strip()
                if url.lower() == 'exit':
                    sys.exit("Exiting without saving URLs.")
                elif url.lower() == 'done':
                    break
                elif is_valid_url(url):
                    urls.append(url)
                else:
                    print("Invalid URL. Please enter a valid URL.")
        except KeyboardInterrupt:
            sys.exit("\nExiting program due to keyboard interrupt without saving URLs.")

        if not urls:
            sys.exit("No valid URLs provided. Exiting.")

        save_urls(urls)
    else:
        if args.url and is_valid_url(args.url):
            urls.append(args.url)
        elif args.url:
            sys.exit("Provided URL is not valid. Exiting.")
        else:
            sys.exit("No URL provided. Exiting.")

    for url in urls[:]:
        success = download_subtitles([url], config.cookies_file, config.output_path)
        if success:
            convert_and_cleanup_subtitles(config.output_path)
            urls.remove(url)
            save_urls(urls)
            
if __name__ == "__main__":
    main()