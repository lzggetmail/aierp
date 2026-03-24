# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## API Keys

### Tavily Search API
- **用途**: AI专用搜索引擎，用于实时联网搜索
- **API Key**: `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`
- **调用方式**: `curl -s "https://api.tavily.com/search" -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <API_KEY>" -d '{"query":"搜索内容","max_results":5}'`

---

Add whatever helps you do your job. This is your cheat sheet.
