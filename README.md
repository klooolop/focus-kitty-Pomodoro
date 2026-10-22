# 🐱 Focus Kitty

A Pomodoro timer that lives inside a tiny retro **CRT monitor**, with a cat, a coffee mug, a rain button, and your favourite "study with me" streams playing behind it all.

Everything is one static HTML file. No build step, no framework, no dependencies to install.

> **Vibe-coded, fully.** This whole project was built by chatting with an AI (Claude) and steering by feel: "make it warmer", "the monitor should match the theme", "add a rain button". I'm not pretending I hand-wrote every line. It works, it looks good, and I use it daily.

---

## ✨ Features

### ⏱️ Timer
- Pomodoro presets: **Classic** (25 / 5), **Deep Work** (50 / 10), **Ultradian** (90 / 30), or **Custom** focus and break lengths
- Circular progress ring drawn inside the CRT screen, plus a session progress bar and dots
- Timer keeps real time from the clock, so it stays accurate even when the tab is in the background
- **Auto Start** for the next phase (remembered between visits)
- Alarm sound and browser notifications when a phase ends
- Session stats and history: sessions completed, best streak, total focus time

### 📺 The CRT monitor
- A decorative retro monitor with scanlines, glass reflections, a flickering screen, antennas, knobs and a little pixel cat
- **The monitor follows the active theme**: case, glow, ring, digits, LED and mascot all change colour with the UI
- In break mode the glow switches to the theme's secondary colour

### 🎨 Themes and layouts
| Theme | Vibe |
|---|---|
| Default | Warm ginger / cream |
| Dark | Espresso night |
| B&W | Clean greyscale |
| Black | Pure black, white phosphor |
| Coffee | Roasted brown, amber glow |

- **Arch UI**: a terminal-style layout with no mascot, green/cyan phosphor, monospace everything (remembered between visits)
- **EN / 日本語** toggle for the whole interface

### 🎧 Audio
- **🌧 Rain button**: one click picks a random rain video as your focus sound
- Separate YouTube sound for **focus** and **break** (paste any YouTube link), with a volume slider
- **Spotify** embed (playlist, album or track link)

### 🎬 Background video
- Use any YouTube video or live stream as the page background
- **🎲 Random button**: loads a random past "study with me" stream from James Scholz's channel (skips streams that can't be embedded)
- Seek bar, play / pause, dim slider, and a **Zen mode** that hides the UI so only the video shows

### ⌨️ Keyboard shortcuts
| Key | Action |
|---|---|
| `Space` | Start / pause the timer |
| `R` | Reset |
| `S` | Skip to the next phase |
| `P` | Play / pause the background video |
| `Esc` | Leave Zen mode |

---

## 🚀 Run it

No install needed.

**Locally**
1. Download or clone the repo.
2. Open `index.html` in your browser.

> YouTube embeds work best when the page is served over `http(s)` rather than opened as a plain file. If a video won't load locally, start a tiny server:
> ```bash
> python3 -m http.server 8000
> ```
> then visit `http://localhost:8000`.

**On GitHub Pages**
1. Push `index.html` (and the favicon files) to your repo.
2. Go to **Settings → Pages**, choose your branch and the root folder, and save.
3. Your site will be live at `https://<your-username>.github.io/<repo-name>/`.

---

## 🧩 Customising

Everything lives in `index.html`.

- **Rain videos**: edit the `RAIN_IDS` array in the script.
- **Random background source**: edit `RAND_BG_LISTS` (a YouTube channel's live-streams playlist is `UULV` + the channel ID without its `UC` prefix).
- **Theme colours**: each theme is a block of CSS variables (`body.theme-…`). The monitor has its own `--crt-*` variables in the "CRT THEME SYNC" section at the end of the stylesheet.
- **Presets**: the preset buttons and their durations are near the top of the Timer card.

---

## ⚠️ Known limits

- Theme, language, stats and history reset on reload. Only Auto Start and the layout choice are saved.
- Some YouTube videos and members-only streams disable embedding and can't be used as audio or background.
- Browsers may block autoplay with sound until you click something on the page.
- The CRT is purely decorative, and its 3D motion is intentionally flattened to avoid Safari rendering glitches.

---

## 🛠️ Built with

- Plain **HTML, CSS and JavaScript** in a single file
- [YouTube IFrame Player API](https://developers.google.com/youtube/iframe_api_reference)
- [Spotify embeds](https://developer.spotify.com/documentation/embeds)
- Google Fonts: **Sora**, **JetBrains Mono**, **DM Mono**
- A lot of prompts 🤖

---

## 🙏 Credits

- Background streams: [james vinh scholz](https://www.youtube.com/@jamesvinhscholz) on YouTube. All video and audio content belongs to its respective creators. This project only embeds it through YouTube's official player.
- Code written by [Claude](https://www.anthropic.com/claude), directed by me.

---

## 📄 License

Released under the [MIT License](LICENSE). The license covers the code only, not the YouTube or Spotify content the site embeds, which belongs to its creators.
