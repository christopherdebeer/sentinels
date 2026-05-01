"""
Render audio from the new species-based engine to a WAV file for
analysis. Drives a headless browser, replaces the engine's audio
context with an OfflineAudioContext, advances time manually, and
exports the rendered buffer as 16-bit PCM WAV.

Requires Playwright. Engine source: ../../index.html

Usage:
    cd audio/analysis
    python3 -m http.server 8765 &  # in another terminal, from repo root
    python3 render_engine_offline.py
"""
import base64
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent / "new_engine.wav"

JS = """
async () => {
  const SR = 22050, DUR = 60;
  const oc = new OfflineAudioContext(1, SR * DUR, SR);
  Sentinels.ctx = oc;
  Sentinels.master = oc.createGain();
  Sentinels.master.gain.value = 0.5;
  Sentinels.master.connect(oc.destination);
  Sentinels.state.playing = true;
  Sentinels.initVoiceState();
  let now = 0;
  Object.values(Sentinels.voiceState).forEach(vs => {
    vs.nextStropheAt = 0.5 + Math.random() * 8;
    vs.activeUntil = 0;
  });
  Sentinels.lastStropheEnd = 0;
  while (now < DUR) {
    Object.defineProperty(oc, 'currentTime', { value: now, configurable: true });
    Sentinels.scheduleAhead();
    now += 0.6;
  }
  const buf = await oc.startRendering();
  const ch = buf.getChannelData(0);
  const view = new DataView(new ArrayBuffer(44 + ch.length * 2));
  let p = 0;
  const w = (s) => { for (let i=0;i<s.length;i++) view.setUint8(p++, s.charCodeAt(i)); };
  w('RIFF'); view.setUint32(p, 36 + ch.length*2, true); p+=4;
  w('WAVEfmt '); view.setUint32(p, 16, true); p+=4;
  view.setUint16(p, 1, true); p+=2; view.setUint16(p, 1, true); p+=2;
  view.setUint32(p, SR, true); p+=4;
  view.setUint32(p, SR*2, true); p+=4;
  view.setUint16(p, 2, true); p+=2; view.setUint16(p, 16, true); p+=2;
  w('data'); view.setUint32(p, ch.length*2, true); p+=4;
  for (let i = 0; i < ch.length; i++) {
    const s = Math.max(-1, Math.min(1, ch[i]));
    view.setInt16(p, s < 0 ? s*0x8000 : s*0x7FFF, true);
    p += 2;
  }
  const bytes = new Uint8Array(view.buffer);
  let bin = '';
  for (let i = 0; i < bytes.length; i++) bin += String.fromCharCode(bytes[i]);
  return btoa(bin);
};
"""

def main():
    with sync_playwright() as pl:
        browser = pl.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
        page = browser.new_page()
        page.goto("http://localhost:8765/")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        b64 = page.evaluate(JS)
        OUT.write_bytes(base64.b64decode(b64))
        print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")
        browser.close()

if __name__ == "__main__":
    main()
