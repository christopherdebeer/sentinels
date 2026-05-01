"""
Render audio from the species-based engine to a stereo WAV file for
analysis. Drives a headless browser, replaces the engine's audio
context with a STEREO OfflineAudioContext, advances time manually,
and exports the rendered buffer as 16-bit PCM stereo WAV.

Why stereo: the engine has a per-strophe spatial chain
(StereoPannerNode + low-pass + distance-attenuation). Earlier versions
of this script used mono OfflineAudioContext, which silently downmixed
the spatial chain into a single channel — meaning every spectral and
gap analysis was computed on a downmix and any regression in the
spatial chain would not be detected. Rendering stereo here makes the
spatial behaviour visible to validate.py and any future analyses.

Requires Playwright. Engine source: ../../index.html

Usage:
    python3 -m http.server 8765 &  # from repo root, in another terminal
    python3 audio/analysis/render_engine_offline.py
"""
import base64
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent / "new_engine.wav"

JS = """
async () => {
  const SR = 22050, DUR = 60;
  // Stereo (2 channels) — see module docstring for rationale.
  const oc = new OfflineAudioContext(2, SR * DUR, SR);
  Sentinels.ctx = oc;
  Sentinels.master = oc.createGain();
  Sentinels.master.gain.value = 0.5;
  Sentinels.master.connect(oc.destination);
  Sentinels.state.playing = true;
  Sentinels.state.density = 0.60;  // match published validation
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
  const L = buf.getChannelData(0);
  const R = buf.getChannelData(1);
  const N = L.length;
  // Interleaved stereo PCM, 16-bit
  const ab = new ArrayBuffer(44 + N * 4);
  const v = new DataView(ab);
  let p = 0;
  const w = (s) => { for (let i=0;i<s.length;i++) v.setUint8(p++, s.charCodeAt(i)); };
  w('RIFF'); v.setUint32(p, 36 + N*4, true); p+=4;
  w('WAVEfmt '); v.setUint32(p, 16, true); p+=4;
  v.setUint16(p, 1, true); p+=2;          // PCM
  v.setUint16(p, 2, true); p+=2;          // 2 channels
  v.setUint32(p, SR, true); p+=4;          // sample rate
  v.setUint32(p, SR*4, true); p+=4;        // byte rate (2 channels × 2 bytes)
  v.setUint16(p, 4, true); p+=2;           // block align
  v.setUint16(p, 16, true); p+=2;          // bits per sample
  w('data'); v.setUint32(p, N*4, true); p+=4;
  for (let i = 0; i < N; i++) {
    const sL = Math.max(-1, Math.min(1, L[i]));
    const sR = Math.max(-1, Math.min(1, R[i]));
    v.setInt16(p, sL < 0 ? sL*0x8000 : sL*0x7FFF, true); p += 2;
    v.setInt16(p, sR < 0 ? sR*0x8000 : sR*0x7FFF, true); p += 2;
  }
  const bytes = new Uint8Array(ab);
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
        print(f"Wrote {OUT} ({OUT.stat().st_size} bytes, stereo)")
        browser.close()

if __name__ == "__main__":
    main()
