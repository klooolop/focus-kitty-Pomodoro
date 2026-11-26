#!/usr/bin/env python3
"""
Focus Kitty — background video "Fit" patch.

Usage:   python3 apply_fit_patch.py index.html
Result:  index.html is patched in place (a backup is saved as index.html.bak)

What it does
  1. Replaces applyBgQuality() with an aspect-ratio-aware version
       Fit  = whole video visible (letterbox bars if the screen isn't 16:9)
       Fill = video covers the screen (crops the edges)
       Auto = Zen mode -> Fit, normal mode -> Fill
  2. Adds a "Fit" dropdown under the Quality dropdown (+ EN/JP labels)
  3. Recalculates when entering/leaving Zen mode
  4. Zen mode: black bars, and the Arch UI scanlines/vignette are hidden
"""
import re
import shutil
import sys

if len(sys.argv) != 2:
    sys.exit("Usage: python3 apply_fit_patch.py path/to/index.html")

path = sys.argv[1]
with open(path, "r", encoding="utf-8", newline="") as f:
    src = f.read()

if "bgFit" in src:
    sys.exit("Already patched (found 'bgFit'). Nothing to do.")


def must_replace_once(text, old, new, label):
    if text.count(old) != 1:
        sys.exit(f"[{label}] expected exactly 1 match, found {text.count(old)}. File not changed.")
    return text.replace(old, new)


# ---------------------------------------------------------------- 1. JS: applyBgQuality
NEW_JS = r'''// ── BACKGROUND VIDEO FIT ──
// 'auto' = Zen shows the WHOLE video, normal mode fills the screen
// 'fit'  = always show the whole video (bars if the screen isn't 16:9)
// 'fill' = always cover the screen (crops the edges)
let bgFit='auto';
try{const _f=localStorage.getItem('fk-bg-fit');if(['auto','fit','fill'].indexOf(_f)>-1)bgFit=_f;}catch(e){}

function applyBgQuality(){
  const sel=$('bg-quality');if(sel&&sel.value!==bgQuality)sel.value=bgQuality;
  const fsel=$('bg-fit');if(fsel&&fsel.value!==bgFit)fsel.value=bgFit;
  const wrap=$('bg-wrap');if(!wrap)return;
  const ifr=wrap.querySelector('iframe');if(!ifr)return;
  const W=wrap.clientWidth,H=wrap.clientHeight;
  if(!W||!H)return;
  const contain=(bgFit==='fit')||(bgFit==='auto'&&cinemaMode);
  const pick=contain?Math.min:Math.max;      // contain = whole video, cover = crop edges
  const cfg=BG_QUALITY[bgQuality];
  const baseW=cfg?cfg.w:1920, baseH=cfg?cfg.h:1080;
  const scale=pick(W/baseW,H/baseH);

  ifr.style.setProperty('min-width','0');
  ifr.style.setProperty('min-height','0');
  ifr.style.setProperty('top','50%');
  ifr.style.setProperty('left','50%');
  if(cfg){
    // fixed-resolution iframe (YouTube picks quality from its pixel size), scaled to fit/fill
    ifr.style.setProperty('width',cfg.w+'px');
    ifr.style.setProperty('height',cfg.h+'px');
    ifr.style.setProperty('transform','translate(-50%,-50%) scale('+scale+')');
    if(bgPlayer){
      try{bgPlayer.setPlaybackQuality(cfg.q);}catch(e){}
      try{bgPlayer.setPlaybackQualityRange&&bgPlayer.setPlaybackQualityRange(cfg.q,cfg.q);}catch(e){}
    }
  }else{
    // Auto quality: iframe at its real on-screen size, so YouTube chooses the matching resolution
    ifr.style.setProperty('width',(baseW*scale)+'px');
    ifr.style.setProperty('height',(baseH*scale)+'px');
    ifr.style.setProperty('transform','translate(-50%,-50%)');
  }
}
function setBgFit(v){
  if(['auto','fit','fill'].indexOf(v)<0)v='auto';
  bgFit=v;
  try{localStorage.setItem('fk-bg-fit',v);}catch(e){}
  applyBgQuality();
  showToast(t('fitLabel')+': '+t({auto:'fitAuto',fit:'fitFit',fill:'fitFill'}[v]));
}
'''

start = src.find("function applyBgQuality(){")
end = src.find("function setBgQuality(key){")
if start < 0 or end < 0 or end < start:
    sys.exit("[applyBgQuality] could not locate the function boundaries. File not changed.")
src = src[:start] + NEW_JS + src[end:]

# ---------------------------------------------------------------- 2. JS: Zen toggle recalculates
src = must_replace_once(
    src,
    "syncBgPlayButton();refreshTlInterval();",
    "syncBgPlayButton();refreshTlInterval();applyBgQuality();",
    "toggleCinemaMode",
)

# ---------------------------------------------------------------- 3. HTML: Fit dropdown
FIT_ROW = '''

      <div class="sl-row">
        <span class="sl-lbl" data-i18n="fitLabel">Fit</span>
        <select class="inp" id="bg-fit" onchange="setBgFit(this.value)" aria-label="Background video fit">
          <option value="auto" data-i18n="fitAuto">Auto (Zen = full video)</option>
          <option value="fit" data-i18n="fitFit">Fit (always full video)</option>
          <option value="fill" data-i18n="fitFill">Fill (crop edges)</option>
        </select>
      </div>'''

pattern = re.compile(r'(<option value="360p">360p</option>\s*</select>\s*</div>)')
if len(pattern.findall(src)) != 1:
    sys.exit("[Fit dropdown] could not find the Quality dropdown. File not changed.")
src = pattern.sub(lambda m: m.group(1) + FIT_ROW, src, count=1)

# ---------------------------------------------------------------- 4. i18n
src = must_replace_once(
    src,
    "quality:'Quality',qualityAuto:'Auto',",
    "quality:'Quality',qualityAuto:'Auto',fitLabel:'Fit',fitAuto:'Auto (Zen = full video)',"
    "fitFit:'Fit (always full video)',fitFill:'Fill (crop edges)',",
    "i18n en",
)
src = must_replace_once(
    src,
    "quality:'画質',qualityAuto:'自動',",
    "quality:'画質',qualityAuto:'自動',fitLabel:'表示',fitAuto:'自動（禅モードで全体表示）',"
    "fitFit:'全体表示',fitFill:'画面を埋める（端を切る）',",
    "i18n ja",
)

# ---------------------------------------------------------------- 5. CSS
CSS = '''
/* ── ZEN: clean letterbox bars, no Arch scanlines/vignette over the video ── */
body.cinema-mode #bg-wrap{background:#000}
body.cinema-mode #bg-wrap .eng-backdrop{display:none}
body.layout-arch.cinema-mode::before,
body.layout-arch.cinema-mode::after{display:none}
'''
if src.count("</style>") != 1:
    sys.exit("[CSS] expected exactly one </style>. File not changed.")
src = src.replace("</style>", CSS + "</style>", 1)

# ---------------------------------------------------------------- write
shutil.copyfile(path, path + ".bak")
with open(path, "w", encoding="utf-8", newline="") as f:
    f.write(src)

print("Patched OK. Backup saved as " + path + ".bak")
