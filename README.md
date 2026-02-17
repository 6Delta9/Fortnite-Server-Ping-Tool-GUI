# Fortnite Ping Tester

**A clean, real-time Windows GUI tool** to ping Fortnite's official data center endpoints and measure latency + packet loss — the **closest possible simulation** of your actual in-game ping.

- Live packet-by-packet display (green = good ping, red = timeout)
- Instant **STOP** button to interrupt long tests
- Clean final summary: Min / Avg / Max ping, packet loss %, sent/received stats
- Tests all 8 current Fortnite matchmaking regions

Perfect for:
- Finding your lowest-ping region before queuing ranked
- Diagnosing ISP routing issues or Wi-Fi vs Ethernet differences
- Comparing ping before/after using a gaming VPN / ExitLag / NoPing
- Competitive players optimizing for sub-30 ms servers

![Fortnite Ping Tester Screenshot](https://via.placeholder.com/720x500.png?text=Fortnite+Ping+Tester+v1.0+-+Europe+Test+Example)  
*(Replace with real screenshot — run the tool, get nice results on your best region, crop nicely, upload as `screenshot.png` or multiple images)*

## Why use this tool instead of others?

Most online ping checkers test generic Cloudflare/Google servers — **this tool hits Epic Games' actual matchmaking ping endpoints** (the same ones Fortnite uses internally).  
→ Your results are **much closer to real in-game ping** than third-party sites.

Epic officially recommends these exact hosts for ping testing:  
(see [Epic Games Support - Latency troubleshooting](https://www.epicgames.com/help/en-US/fortnite-c5719335176219/technical-support-c5719372265755/understanding-latency-or-ping-in-fortnite-a5720393283867))

## Supported Regions (2026)

| Region         | Endpoint                          | Typical Locations Served                  | Best For Players In                  |
|----------------|-----------------------------------|-------------------------------------------|--------------------------------------|
| NA-East        | ping-nae.ds.on.epicgames.com     | East Coast US, Canada Atlantic, Caribbean | Eastern USA, Eastern Canada          |
| NA-Central     | ping-nac.ds.on.epicgames.com     | Central US, Mexico, Dallas area           | Midwest US, Mexico, Texas            |
| NA-West        | ping-naw.ds.on.epicgames.com     | West Coast US, Canada Pacific             | Western USA, Western Canada          |
| Europe         | ping-eu.ds.on.epicgames.com      | Europe (mostly Frankfurt/Paris)           | EU, UK, Middle East (sometimes)      |
| Oceania        | ping-oce.ds.on.epicgames.com     | Australia, New Zealand                    | Australia, NZ, South Pacific         |
| Brazil         | ping-br.ds.on.epicgames.com      | South America (São Paulo)                 | Brazil, Argentina, Chile             |
| Asia           | ping-asia.ds.on.epicgames.com    | Southeast Asia, Japan, Korea              | Japan, Korea, SEA, parts of India    |
| Middle East    | ping-me.ds.on.epicgames.com      | Middle East, parts of Africa/India        | UAE, Saudi, Egypt, South Asia        |

## Features

- **25 pings per test** by default (easy to change in code)
- Real-time results updating every packet
- Color-coded output: green for <60 ms, red for timeouts
- Graceful stop: terminates ping process safely
- Final boxed summary with:
  - Min / Avg (rounded) / Max latency
  - Exact packet loss percentage
  - Sent / Received counts
- Clean, readable Consolas font + dark-friendly background
- No external dependencies beyond standard Python + tkinter
- Threaded → GUI stays responsive during tests

## Requirements

- **Windows** only (uses Windows `ping -n` syntax & CREATE_NO_WINDOW flag)
- **Python 3.6+** (recommended: 3.9 – 3.12)
- tkinter (included with most Windows Python installs; if missing → reinstall Python and check "tcl/tk and IDLE")

No pip installs needed!

## Installation & Usage

1. Clone or download the repo

   ```bash
   git clone https://github.com/YOUR_USERNAME/Fortnite-Ping-Tester.git
   cd Fortnite-Ping-Tester