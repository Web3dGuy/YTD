import os
import subprocess
# must have yt-dlp installed with pip
# FFMPEG shoid be installed and added to path

def download_videos(
    url_file,
    download_path='downloads',
    concurrent_segments=4,
    resolution=1080,
    download_subtitles=True,
    auto_subtitles=True,
    subtitle_langs="en"
):
    """
    Downloads YouTube videos in up to 'resolution' using yt-dlp.
    Optionally downloads subtitles if available.

    :param url_file: Path to the text file containing YouTube URLs.
    :param download_path: Folder to save the downloaded videos.
    :param concurrent_segments: Number of concurrent segments to download per video.
    :param resolution: Max vertical resolution (e.g., 1080).
    :param download_subtitles: If True, attempts to download manually provided subtitles.
    :param auto_subtitles: If True, attempts to download auto-generated subtitles.
    :param subtitle_langs: Which subtitle language(s) to download (e.g., 'en', 'en.*', or 'all').
    """
    # Ensure download folder exists
    os.makedirs(download_path, exist_ok=True)

    # Read the URLs
    with open(url_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]

    # Format code for best video up to <resolution> + best audio
    format_code = f"bestvideo[height<={resolution}]+bestaudio/best"

    # Output template (includes upload_date)
    output_template = os.path.join(download_path, "%(upload_date)s - %(title).200s.%(ext)s")

    # Base command for video
    base_command = [
        "yt-dlp",
        "-f", format_code,
        "--merge-output-format", "mp4",
        "-N", str(concurrent_segments),
        "-o", output_template
    ]

    # If we want subtitles
    if download_subtitles:
        base_command += [
            "--write-subs",            # download manually uploaded subtitles (if available)
            "--sub-langs", subtitle_langs,  # which languages
            "--convert-subs", "srt"   # convert subtitles to .srt
        ]

    # If we also want auto-generated subtitles
    if auto_subtitles:
        base_command.append("--write-auto-subs")

    # Download each URL
    for url in urls:
        print(f"Downloading {url}...")
        command = base_command + [url]
        subprocess.run(command, check=True)

if __name__ == "__main__":
    # Example usage
    download_videos(
        url_file="video_urls.txt",
        download_path="my_downloads",
        concurrent_segments=4,
        resolution=1080,
        download_subtitles=True,   # set to True to get subtitles
        auto_subtitles=True,       # True to also get auto-generated subtitles
        subtitle_langs="en"        # pick your language (or use "all")
    )
