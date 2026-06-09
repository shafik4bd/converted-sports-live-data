import requests
import json
import re
from datetime import datetime, timezone
from urllib.parse import urlparse

SOURCE_URL = "https://raw.githubusercontent.com/sm-monirulislam/Upcoming-and-Live-Sports-Data/refs/heads/main/Sports_data.json"
DEFAULT_LOGO = "https://cdn.pixabay.com/photo/2021/07/02/09/41/live-streaming-6366830_1280.png"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
    "Cache-Control": "no-cache",
}

def fetch_source():
    try:
        r = requests.get(SOURCE_URL, headers=HEADERS, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"❌ Source fetch failed: {e}")
        return None

def get_stream_url(stream):
    return (
        stream.get("stream_url") or
        stream.get("stream_url 1") or
        stream.get("stream_url 2") or
        stream.get("stream_url 3") or
        stream.get("url") or
        stream.get("link") or ""
    )

def make_slug(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-') or "match"

def make_id(name, stream_index, total_streams):
    slug = make_slug(name)
    # stream ১টাই থাকলে suffix নেই, একাধিক হলে -s1, -s2...
    if total_streams == 1:
        return slug
    return f"{slug}-s{stream_index + 1}"

def convert(data):
    matches = data.get("matches", [])
    result = []

    for match in matches:
        streams = match.get("streams", [])
        if not streams:
            continue

        event_name = match.get("event_name") or match.get("title") or "Unknown"
        status = match.get("status", "UNKNOWN")

        # valid stream গুলো আগে filter করো
        valid_streams = []
        for stream in streams:
            url = get_stream_url(stream)
            if url:
                valid_streams.append(stream)

        if not valid_streams:
            continue

        total = len(valid_streams)

        for si, stream in enumerate(valid_streams):
            stream_url = get_stream_url(stream)
            referer = stream.get("stream_referer") or stream.get("referer") or ""
            origin = ""
            if referer:
                try:
                    parsed = urlparse(referer)
                    origin = f"{parsed.scheme}://{parsed.netloc}"
                except:
                    pass

            stream_label = f" Stream {si + 1}" if total > 1 else ""
            full_name = event_name + stream_label

            entry = {
                "id": make_id(event_name, si, total),
                "name": full_name,
                "status": status,
                "logo": DEFAULT_LOGO,
                "link": stream_url,
            }

            if referer:
                entry["referer"] = referer
            if origin:
                entry["origin"] = origin

            result.append(entry)

    return result

def main():
    print("🚀 Fetching source JSON...")
    data = fetch_source()
    if not data:
        print("❌ Failed. Exiting.")
        return

    print(f"✅ Got {len(data.get('matches', []))} matches")
    print("🔄 Converting...")

    converted = convert(data)

    output = {
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "totalStreams": len(converted),
        "liveCount": sum(1 for c in converted if c.get("status") == "LIVE"),
        "channels": converted
    }

    with open("converted.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ converted.json saved!")
    print(f"   📺 Total streams : {output['totalStreams']}")
    print(f"   🔴 Live          : {output['liveCount']}")

if __name__ == "__main__":
    main()
