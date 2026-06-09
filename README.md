# Converted Sports Stream JSON

Auto-updated every 20 minutes. Converts Monirul's Sports JSON into toffee-proxy compatible format.

## JSON URL

```
https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/converted.json
```

## Play URL Format

```
https://toffee-proxy.digantapostv1.workers.dev/play?source=RAW_JSON_URL_ENCODED&id=CHANNEL_ID
```

## JSON Structure

```json
{
  "lastUpdated": "2026-06-09T00:00:00Z",
  "totalStreams": 10,
  "liveCount": 3,
  "channels": [
    {
      "id": "hayate-shizuoka-vs-dragons-npb-farm-leagues",
      "name": "Hayate Shizuoka Vs Dragons | Npb Farm Leagues",
      "status": "LIVE",
      "logo": "https://...",
      "link": "https://...m3u8",
      "referer": "https://iframe.rumsport10.live/",
      "origin": "https://iframe.rumsport10.live"
    }
  ]
}
```
