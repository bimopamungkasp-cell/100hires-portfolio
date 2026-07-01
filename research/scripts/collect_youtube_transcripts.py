"""
Cold outreach pipeline for B2B SaaS - research collector.

For each configured YouTube channel, finds recent videos matching cold
outreach / prospecting / lead-gen themes, downloads their transcripts, and
writes them as markdown files under research/youtube-transcripts/<slug>/.

Usage:
    python collect_youtube_transcripts.py --channel patrick-dang
    python collect_youtube_transcripts.py --all
"""
import argparse
import datetime
import re
import time
import sys
from pathlib import Path

import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)

ROOT = Path(__file__).resolve().parents[2]
TRANSCRIPTS_DIR = ROOT / "research" / "youtube-transcripts"
SOURCES_MD = ROOT / "research" / "sources.md"
SKIPPED_LOG = TRANSCRIPTS_DIR / "_skipped.log"

MIN_VIDEOS = 5
MAX_VIDEOS = 8
PRIMARY_WINDOW_DAYS = 365
FALLBACK_WINDOW_DAYS = 730
MAX_FLAT_ENTRIES = 200
MAX_MATCHED_LOOKUPS = 40
REQUEST_DELAY_SECONDS = 1.5

KEYWORDS = [
    "cold email", "cold outreach", "cold call", "cold calling",
    "prospecting", "prospect", "lead gen", "lead generation",
    "outbound", "b2b sales", "b2b saas", "saas sales", "sales outreach",
    "sdr", "appointment setting", "sales script", "follow up email",
    "linkedin outreach", "sales prospecting",
]
KEYWORD_RE = re.compile("|".join(re.escape(k) for k in KEYWORDS), re.IGNORECASE)

CHANNELS = {
    "patrick-dang": {
        "name": "Patrick Dang",
        "url": "https://www.youtube.com/channel/UCLOzkJ9W9fntCGyYfUwMPew",
        "why": (
            "Ex-Oracle/Alibaba B2B sales rep turned full-time creator focused "
            "specifically on cold email, cold outreach, and lead generation "
            "tactics for SaaS and B2B sellers."
        ),
    },
    "alex-berman": {
        "name": "Alex Berman",
        "url": "https://www.youtube.com/channel/UCAr7M4Pz-c1WCpIz3YAJQeQ",
        "why": (
            "Founder of Experiment 27 / Email10k, built his agency almost "
            "entirely on cold email; one of the most cited names in cold "
            "outreach content for B2B agencies and SaaS founders."
        ),
    },
    "tim-dodd": {
        "name": "Tim Dodd",
        "url": "https://www.youtube.com/c/thetimdoddshow",
        "why": (
            "B2B sales trainer covering prospecting and outbound sales "
            "process, relevant as a practitioner voice on outreach cadence "
            "and pipeline building."
        ),
    },
    "jeremy-miner": {
        "name": "Jeremy Miner",
        "url": "https://www.youtube.com/@jeremyminer",
        "why": (
            "Founder of 7th Level Communications, known for NEPQ sales "
            "methodology widely applied to B2B cold calling and objection "
            "handling in outbound sales."
        ),
    },
    "will-barron": {
        "name": "Will Barron",
        "url": "https://www.youtube.com/c/SalesmanPodcast",
        "why": (
            "Host of the Salesman Podcast, interviews top B2B sales "
            "practitioners regularly covering prospecting, outbound, and "
            "SaaS sales strategy."
        ),
    },
}


def log_skip(message: str) -> None:
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().isoformat(timespec="seconds")
    with open(SKIPPED_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"  SKIP: {message}")


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:80]


def fetch_flat_entries(channel_url: str) -> list:
    ydl_opts = {
        "extract_flat": "in_playlist",
        "skip_download": True,
        "quiet": True,
        "no_warnings": True,
        "playlistend": MAX_FLAT_ENTRIES,
    }
    videos_url = channel_url.rstrip("/") + "/videos"
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(videos_url, download=False)
    return info.get("entries") or []


def fetch_full_metadata(video_id: str) -> dict | None:
    ydl_opts = {"quiet": True, "no_warnings": True, "skip_download": True}
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as e:
        log_skip(f"metadata fetch failed for {video_id}: {e}")
        return None
    upload_date_str = info.get("upload_date")  # YYYYMMDD
    if not upload_date_str:
        return None
    upload_date = datetime.datetime.strptime(upload_date_str, "%Y%m%d").date()
    return {
        "id": video_id,
        "title": info.get("title") or "untitled",
        "upload_date": upload_date,
        "url": f"https://www.youtube.com/watch?v={video_id}",
    }


def collect_candidate_videos(channel_url: str) -> list:
    entries = fetch_flat_entries(channel_url)
    candidates = []
    for entry in entries:
        if not entry:
            continue
        title = entry.get("title") or ""
        if not KEYWORD_RE.search(title):
            continue
        video_id = entry.get("id")
        if not video_id:
            continue
        candidates.append(video_id)
        if len(candidates) >= MAX_MATCHED_LOOKUPS:
            break

    results = []
    for video_id in candidates:
        meta = fetch_full_metadata(video_id)
        time.sleep(REQUEST_DELAY_SECONDS)
        if meta:
            results.append(meta)
    return results


def select_videos(candidates: list) -> list:
    today = datetime.date.today()
    candidates_sorted = sorted(candidates, key=lambda v: v["upload_date"], reverse=True)

    def within(days):
        cutoff = today - datetime.timedelta(days=days)
        return [v for v in candidates_sorted if v["upload_date"] >= cutoff]

    selected = within(PRIMARY_WINDOW_DAYS)
    if len(selected) < MIN_VIDEOS:
        selected = within(FALLBACK_WINDOW_DAYS)
    return selected[:MAX_VIDEOS]


def fetch_transcript_text(video_id: str) -> str | None:
    api = YouTubeTranscriptApi()
    try:
        transcript_list = api.list(video_id)
        try:
            transcript = transcript_list.find_manually_created_transcript(["en"])
        except NoTranscriptFound:
            transcript = transcript_list.find_generated_transcript(["en"])
        fetched = transcript.fetch()
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as e:
        log_skip(f"transcript unavailable for {video_id}: {e}")
        return None
    except Exception as e:
        log_skip(f"transcript fetch error for {video_id}: {e}")
        return None
    return "\n".join(snippet.text for snippet in fetched)


def write_transcript_md(slug: str, channel_name: str, video: dict, transcript_text: str) -> Path:
    channel_dir = TRANSCRIPTS_DIR / slug
    channel_dir.mkdir(parents=True, exist_ok=True)
    title_slug = slugify(video["title"])
    file_path = channel_dir / f"{video['id']}-{title_slug}.md"
    front_matter = (
        "---\n"
        f"title: {video['title']}\n"
        f"channel: {channel_name}\n"
        f"url: {video['url']}\n"
        f"published: {video['upload_date'].isoformat()}\n"
        "---\n\n"
    )
    file_path.write_text(front_matter + transcript_text, encoding="utf-8")
    return file_path


def update_sources_md(channel_name: str, channel_url: str, why: str, collected: list) -> None:
    SOURCES_MD.parent.mkdir(parents=True, exist_ok=True)
    existing = SOURCES_MD.read_text(encoding="utf-8") if SOURCES_MD.exists() else ""

    lines = [f"## {channel_name}", "- Platform: YouTube", f"- Channel: {channel_url}", f"- Kenapa dipilih: {why}"]
    if collected:
        lines.append("- Video yang dikumpulkan:")
        for v in collected:
            lines.append(f"  - {v['title']} ({v['upload_date'].isoformat()}) - {v['url']}")
    else:
        lines.append("- Video yang dikumpulkan: (tidak ada video yang cocok ditemukan)")
    section = "\n".join(lines) + "\n\n"

    header_marker = f"## {channel_name}\n"
    if header_marker in existing:
        pattern = re.compile(rf"## {re.escape(channel_name)}\n.*?(?=\n## |\Z)", re.DOTALL)
        existing = pattern.sub(section.rstrip("\n") + "\n", existing)
        new_content = existing
    else:
        if not existing.strip():
            existing = "# Research Sources\n\n"
        new_content = existing.rstrip("\n") + "\n\n" + section

    SOURCES_MD.write_text(new_content, encoding="utf-8")


def process_channel(slug: str) -> None:
    channel = CHANNELS[slug]
    print(f"\n=== Processing channel: {channel['name']} ({slug}) ===")

    print("Fetching candidate videos (title keyword match)...")
    candidates = collect_candidate_videos(channel["url"])
    print(f"Found {len(candidates)} keyword-matching candidates.")

    selected = select_videos(candidates)
    print(f"Selected {len(selected)} videos after date-window filtering.")

    collected = []
    for video in selected:
        print(f"  Fetching transcript: {video['title']} ({video['id']})")
        transcript_text = fetch_transcript_text(video["id"])
        time.sleep(REQUEST_DELAY_SECONDS)
        if transcript_text is None:
            continue
        path = write_transcript_md(slug, channel["name"], video, transcript_text)
        print(f"    Saved: {path.relative_to(ROOT)}")
        collected.append(video)

    update_sources_md(channel["name"], channel["url"], channel["why"], collected)
    print(f"Updated {SOURCES_MD.relative_to(ROOT)} for {channel['name']}.")
    print(f"Done: {len(collected)}/{len(selected)} transcripts saved for {channel['name']}.")


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--channel", choices=sorted(CHANNELS.keys()))
    group.add_argument("--all", action="store_true")
    args = parser.parse_args()

    if args.all:
        for slug in CHANNELS:
            process_channel(slug)
    else:
        process_channel(args.channel)


if __name__ == "__main__":
    sys.exit(main())
