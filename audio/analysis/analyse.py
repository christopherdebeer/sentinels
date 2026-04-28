"""
analyse.py — comprehensive analysis of a real dawn chorus recording,
with side-by-side comparison to the Sentinels procedural audio engine.

Outputs:
  figures/spectrum.png            — frequency content (real)
  figures/spectrogram.png         — time-frequency (real)
  figures/onsets.png              — call detection over time (real)
  figures/gap-distribution.png    — inter-call gap statistics (real)
  figures/density-drift.png       — call rate over time (real)
  figures/spectral-drift.png      — spectral centroid over time (real)
  figures/comparison.png          — real vs synthetic side-by-side
  results.json                    — numeric findings & engine tuning
  tuning-report.md                — human-readable interpretation
"""

import json
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy.signal
import scipy.stats
from pathlib import Path

# ───────── Aesthetic to match the project landing page ─────────
mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],  # what's actually installed
    "axes.facecolor": "#f5f0e6",
    "figure.facecolor": "#f5f0e6",
    "axes.edgecolor": "#3d362e",
    "axes.labelcolor": "#1a1612",
    "axes.titlecolor": "#1a1612",
    "axes.titlesize": 12,
    "axes.titleweight": "normal",
    "axes.labelsize": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.color": "#3d362e",
    "ytick.color": "#3d362e",
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "grid.color": "#1a1612",
    "grid.alpha": 0.08,
    "savefig.facecolor": "#f5f0e6",
    "savefig.bbox": "tight",
    "savefig.dpi": 130,
})

MOSS = "#5a6b4a"
MOSS_DEEP = "#404e35"
RUST = "#a85a3a"
INK = "#1a1612"
INK_FAINT = "#6b5f51"

OUT = Path("figures")
OUT.mkdir(exist_ok=True)

# ═════════════════════════════════════════════════════════════════════
# 1. Load real audio
# ═════════════════════════════════════════════════════════════════════
print("Loading real recording...")
# Downsample to 22.05 kHz for analysis. Bird-band content is below 11 kHz
# so we still capture all the relevant frequencies, but halve memory.
y_stereo, sr = librosa.load("preview.mp3", sr=22050, mono=False)
y = y_stereo.mean(axis=0)  # downmix to mono
del y_stereo  # free memory
duration = len(y) / sr
print(f"  duration: {duration:.1f}s, sr: {sr} Hz, mono shape: {y.shape}")

# ═════════════════════════════════════════════════════════════════════
# 2. Spectral character — power spectral density across the whole recording
# ═════════════════════════════════════════════════════════════════════
print("\n[1/7] Spectral analysis...")
freqs, psd = scipy.signal.welch(y, fs=sr, nperseg=8192, scaling="density")
# Convert to dB, normalise so peak = 0 dB for readability
psd_db = 10 * np.log10(psd + 1e-12)
psd_db = psd_db - psd_db.max()

# Identify the active frequency band where most energy lives
mask_audible = (freqs >= 100) & (freqs <= 12000)
freqs_audible = freqs[mask_audible]
psd_audible = psd_db[mask_audible]
# Find -10 dB band edges (where energy drops to 10% peak)
above_10db = psd_audible >= -10
if above_10db.any():
    band_low = freqs_audible[above_10db].min()
    band_high = freqs_audible[above_10db].max()
else:
    band_low, band_high = 0, 0
# Find peak frequency (excluding very low rumble)
peak_freq = freqs_audible[np.argmax(psd_audible)]

print(f"  -10 dB band: {band_low:.0f}-{band_high:.0f} Hz")
print(f"  peak frequency: {peak_freq:.0f} Hz")

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.semilogx(freqs_audible, psd_audible, color=MOSS_DEEP, lw=1.2)
ax.fill_between(freqs_audible, psd_audible, -80,
                where=(freqs_audible >= 1000) & (freqs_audible <= 8000),
                color=MOSS, alpha=0.12, label="1–8 kHz target band")
ax.axvline(peak_freq, color=RUST, lw=1, ls="--", alpha=0.6,
           label=f"peak: {peak_freq:.0f} Hz")
ax.axvspan(band_low, band_high, color=MOSS, alpha=0.05)
ax.set_xlim(100, 12000)
ax.set_ylim(-60, 2)
ax.set_xlabel("frequency (Hz)")
ax.set_ylabel("relative power (dB)")
ax.set_title("Frequency content of dawn chorus recording", loc="left", pad=12)
ax.text(0.99, 0.05,
        f"–10 dB band: {band_low:.0f}–{band_high:.0f} Hz",
        transform=ax.transAxes, ha="right", color=INK_FAINT, fontsize=9,
        style="italic")
ax.legend(loc="upper right", frameon=False, fontsize=9)
ax.grid(True)
plt.savefig(OUT / "spectrum.png")
plt.close()

# ═════════════════════════════════════════════════════════════════════
# 3. Spectrogram — time-frequency view
# ═════════════════════════════════════════════════════════════════════
print("\n[2/7] Spectrogram...")
S = librosa.stft(y, n_fft=2048, hop_length=1024)
S_db = librosa.amplitude_to_db(np.abs(S), ref=np.max)

fig, ax = plt.subplots(figsize=(11, 4.5))
img = librosa.display.specshow(S_db, sr=sr, hop_length=1024,
                                x_axis="time", y_axis="hz",
                                ax=ax, cmap="bone_r", vmin=-60, vmax=0)
ax.set_ylim(200, 9000)
ax.set_title("Spectrogram — full recording", loc="left", pad=12)
ax.set_ylabel("frequency (Hz)")
ax.set_xlabel("time (s)")
cbar = fig.colorbar(img, ax=ax, format="%+2.0f dB", pad=0.01)
cbar.ax.tick_params(labelsize=8)
plt.savefig(OUT / "spectrogram.png")
plt.close()

# ═════════════════════════════════════════════════════════════════════
# 4. Onset detection — find individual call events
# ═════════════════════════════════════════════════════════════════════
print("\n[3/7] Onset detection...")
# Pre-emphasise the bird-band by high-pass filtering before onset detection
sos = scipy.signal.butter(4, 1500, btype="highpass", fs=sr, output="sos")
y_filtered = scipy.signal.sosfilt(sos, y)

onset_env = librosa.onset.onset_strength(y=y_filtered, sr=sr,
                                          hop_length=1024,
                                          aggregate=np.median)
# Bird chorus is dense and overlapping. Use a lower delta and shorter
# wait window to catch closely-spaced calls. We'll get some false
# positives, but the statistics on inter-call gaps and density-over-time
# remain meaningful even with imperfect detection — what matters is the
# *distribution*, not perfect identification of every individual call.
onsets_frames = librosa.onset.onset_detect(
    onset_envelope=onset_env, sr=sr, hop_length=1024,
    delta=0.07, wait=2, pre_avg=4, post_avg=4, pre_max=4, post_max=4)
onsets_t = librosa.frames_to_time(onsets_frames, sr=sr, hop_length=1024)
n_onsets = len(onsets_t)
overall_rate = n_onsets / duration * 60  # calls per minute

print(f"  detected onsets: {n_onsets}")
print(f"  overall rate: {overall_rate:.1f} calls/minute")

fig, axes = plt.subplots(2, 1, figsize=(11, 5),
                          gridspec_kw={"height_ratios": [2, 1]}, sharex=True)

# Top: spectrogram with onsets overlaid
librosa.display.specshow(S_db, sr=sr, hop_length=1024,
                          x_axis="time", y_axis="hz",
                          ax=axes[0], cmap="bone_r", vmin=-60, vmax=0)
axes[0].set_ylim(800, 9000)
for t in onsets_t:
    axes[0].axvline(t, color=RUST, alpha=0.4, lw=0.6)
axes[0].set_title(f"Detected call onsets — {n_onsets} events, "
                   f"{overall_rate:.1f}/min average", loc="left", pad=12)
axes[0].set_ylabel("freq (Hz)")
axes[0].set_xlabel("")

# Bottom: onset strength envelope
times_env = librosa.frames_to_time(np.arange(len(onset_env)),
                                    sr=sr, hop_length=1024)
axes[1].plot(times_env, onset_env, color=MOSS_DEEP, lw=0.7)
axes[1].fill_between(times_env, onset_env, 0, color=MOSS, alpha=0.2)
axes[1].set_xlabel("time (s)")
axes[1].set_ylabel("onset strength")
axes[1].set_xlim(0, duration)
axes[1].grid(True)
plt.savefig(OUT / "onsets.png")
plt.close()

# ═════════════════════════════════════════════════════════════════════
# 5. Inter-call gap distribution
# ═════════════════════════════════════════════════════════════════════
print("\n[4/7] Gap distribution...")
gaps = np.diff(onsets_t)
print(f"  n gaps: {len(gaps)}")
print(f"  mean gap: {gaps.mean():.3f}s, median: {np.median(gaps):.3f}s")
print(f"  std: {gaps.std():.3f}s, max: {gaps.max():.3f}s")

# Try to fit a log-normal distribution (heavy-tailed, positive)
log_gaps = np.log(gaps[gaps > 0.01])
ln_mu, ln_sigma = log_gaps.mean(), log_gaps.std()
# Fit alternative: exponential
exp_lambda = 1 / gaps.mean()

fig, axes = plt.subplots(1, 2, figsize=(11, 4))

# Linear histogram
axes[0].hist(gaps, bins=60, color=MOSS, alpha=0.6, edgecolor=MOSS_DEEP)
x_lin = np.linspace(0.01, gaps.max(), 300)
# overlay log-normal pdf scaled to histogram
ln_pdf = scipy.stats.lognorm.pdf(x_lin, ln_sigma, scale=np.exp(ln_mu))
ln_pdf_scaled = ln_pdf * len(gaps) * (gaps.max() / 60)
axes[0].plot(x_lin, ln_pdf_scaled, color=RUST, lw=1.5,
              label=f"log-normal fit (μ={ln_mu:.2f}, σ={ln_sigma:.2f})")
axes[0].set_xlabel("inter-call gap (s)")
axes[0].set_ylabel("count")
axes[0].set_title("Gap distribution (linear)", loc="left", pad=8)
axes[0].axvline(gaps.mean(), color=INK, ls="--", lw=0.8, alpha=0.5,
                 label=f"mean: {gaps.mean():.2f}s")
axes[0].axvline(np.median(gaps), color=MOSS_DEEP, ls=":", lw=0.8, alpha=0.7,
                 label=f"median: {np.median(gaps):.2f}s")
axes[0].legend(frameon=False, fontsize=8)
axes[0].grid(True)

# Log-log to show heavy tail clearly
gap_sorted = np.sort(gaps)
ccdf = 1 - np.arange(len(gap_sorted)) / len(gap_sorted)
axes[1].loglog(gap_sorted, ccdf, color=MOSS_DEEP, lw=1)
axes[1].set_xlabel("gap (s)")
axes[1].set_ylabel("P(gap > x)")
axes[1].set_title("Tail behaviour (log-log CCDF)", loc="left", pad=8)
axes[1].grid(True, which="both")
plt.savefig(OUT / "gap-distribution.png")
plt.close()

# ═════════════════════════════════════════════════════════════════════
# 6. Drift — call density and spectral character over time
# ═════════════════════════════════════════════════════════════════════
print("\n[5/7] Drift analysis...")
# Bin onsets into 10-second windows and compute rate
window_s = 10
n_windows = int(duration // window_s)
density_t = np.arange(n_windows) * window_s + window_s / 2
density = np.zeros(n_windows)
for i in range(n_windows):
    t0, t1 = i * window_s, (i + 1) * window_s
    density[i] = ((onsets_t >= t0) & (onsets_t < t1)).sum() * (60 / window_s)

# Spectral centroid over time
spectral_centroid = librosa.feature.spectral_centroid(
    y=y_filtered, sr=sr, hop_length=2048)[0]
sc_times = librosa.frames_to_time(np.arange(len(spectral_centroid)),
                                    sr=sr, hop_length=2048)

fig, axes = plt.subplots(2, 1, figsize=(11, 5.5), sharex=True)
axes[0].plot(density_t, density, color=MOSS_DEEP, lw=1.2)
axes[0].fill_between(density_t, density, 0, color=MOSS, alpha=0.2)
axes[0].axhline(density.mean(), color=RUST, ls="--", lw=0.8, alpha=0.6,
                 label=f"mean: {density.mean():.0f}/min")
axes[0].set_ylabel("calls / minute")
axes[0].set_title(f"Call density drift — bin width {window_s}s",
                   loc="left", pad=8)
axes[0].legend(frameon=False, loc="upper right", fontsize=9)
axes[0].grid(True)

axes[1].plot(sc_times, spectral_centroid, color=MOSS_DEEP, lw=0.6, alpha=0.5)
# Smooth for visible drift
from scipy.ndimage import uniform_filter1d
sc_smooth = uniform_filter1d(spectral_centroid,
                              size=int(len(spectral_centroid) / 30))
axes[1].plot(sc_times, sc_smooth, color=RUST, lw=1.2)
axes[1].axhline(spectral_centroid.mean(), color=INK, ls="--",
                  lw=0.8, alpha=0.4)
axes[1].set_ylabel("spectral centroid (Hz)")
axes[1].set_xlabel("time (s)")
axes[1].set_title("Spectral character drift (smoothed)", loc="left", pad=8)
axes[1].grid(True)
plt.savefig(OUT / "density-drift.png")
plt.close()

density_cv = density.std() / density.mean()  # coefficient of variation
sc_cv = sc_smooth.std() / sc_smooth.mean()
sc_mean = float(spectral_centroid.mean())
print(f"  density CV: {density_cv:.3f}")
print(f"  spectral centroid CV (smoothed): {sc_cv:.3f}")
print(f"  density range: {density.min():.0f} - {density.max():.0f} calls/min")

# Free memory before synthesis stage
del S, S_db, y_filtered, onset_env, spectral_centroid, sc_smooth

# ═════════════════════════════════════════════════════════════════════
# 7. Synthesise comparison: 5 minutes of the engine's logic in Python
# ═════════════════════════════════════════════════════════════════════
print("\n[6/7] Synthesising 5 min from engine logic...")

def synth_engine(duration_s, sr=44100, density=0.4, seed=42):
    """
    Faithful Python port of the Sentinels Web Audio engine in index.html.
    Same voice types, same drift sines, same gap distribution.
    """
    rng = np.random.default_rng(seed)
    n_samples = int(duration_s * sr)
    out = np.zeros(n_samples)
    onsets_synth = []

    t = 0.4
    while t < duration_s - 0.5:
        # Drift sines (same periods as the JS engine)
        drift_rate = 0.5 + 0.4 * np.sin(t * 0.013)
        drift_freq = 0.5 + 0.5 * np.sin(t * 0.008)
        drift_mix  = 0.5 + 0.5 * np.sin(t * 0.021)

        f_center = 2400 + drift_freq * 2400  # 2.4-4.8 kHz

        # Voice selection (same weights as JS)
        weights = {
            "sweep": 3.0,
            "trill": 1.0 + drift_mix * 0.5,
            "pip":   1.5,
            "warble": 0.8 + (1 - drift_mix) * 0.6,
        }
        total = sum(weights.values())
        r = rng.random() * total
        for v, w in weights.items():
            r -= w
            if r <= 0:
                voice = v
                break

        # Render the voice
        if voice == "sweep":
            span = 400 + rng.random() * 1000
            dur = 0.10 + rng.random() * 0.18
            up = rng.random() > 0.5
            f0 = (f_center - span) if up else (f_center + span)
            f1 = (f_center + span * 0.4) if up else (f_center - span * 0.4)
            n = int(dur * sr)
            ts = np.arange(n) / sr
            # piecewise-exponential sweep (approximation of the JS exponentialRampToValueAtTime)
            mid = int(n * 0.35)
            phase1 = 2 * np.pi * np.linspace(f0, f_center, mid).cumsum() / sr
            phase2 = 2 * np.pi * np.linspace(f_center, f1, n - mid).cumsum() / sr + phase1[-1] if mid > 0 else np.array([])
            sig = np.concatenate([np.sin(phase1), np.sin(phase2)]) if mid > 0 else np.sin(phase2)
            env = np.where(ts < 0.01,
                            ts / 0.01 * 0.18,
                            0.18 * np.exp(-(ts - 0.01) * 4 / dur))
            sig = sig[:len(env)] * env
        elif voice == "trill":
            freq = f_center + (rng.random() - 0.5) * 800
            mod_rate = 22 + rng.random() * 16
            dur = 0.25 + rng.random() * 0.30
            n = int(dur * sr)
            ts = np.arange(n) / sr
            mod = 1 + 0.07 / 0.08 * np.sin(2 * np.pi * mod_rate * ts)
            sig = np.sin(2 * np.pi * freq * ts) * 0.08 * mod
            env = np.minimum(np.minimum(ts / 0.015, 1), (dur - ts) / (dur * 0.15))
            sig *= np.maximum(env, 0)
        elif voice == "pip":
            freq = max(800, f_center + (rng.random() - 0.3) * 1400)
            dur = 0.04 + rng.random() * 0.06
            n = int(dur * sr)
            ts = np.arange(n) / sr
            sig = np.sin(2 * np.pi * freq * ts)
            env = np.where(ts < 0.008, ts / 0.008 * 0.13,
                            0.13 * np.exp(-(ts - 0.008) * 5 / dur))
            sig *= env
        elif voice == "warble":
            base = f_center + (rng.random() - 0.5) * 600
            dur = 0.30 + rng.random() * 0.40
            n = int(dur * sr)
            ts = np.arange(n) / sr
            lfo_rate = 6 + rng.random() * 4
            inst_freq = base * (1 + 0.05 * np.sin(2 * np.pi * lfo_rate * ts))
            phase = 2 * np.pi * inst_freq.cumsum() / sr
            sig = np.sin(phase) * 0.11
            env = np.minimum(np.minimum(ts / 0.02, 1), (dur - ts) / (dur * 0.2))
            sig *= np.maximum(env, 0)

        # Place into output buffer
        start_sample = int(t * sr)
        end_sample = min(start_sample + len(sig), n_samples)
        out[start_sample:end_sample] += sig[:end_sample - start_sample]
        onsets_synth.append(t)

        # Pip clusters
        if voice == "pip":
            for offset, prob in [(0.12, 0.5), (0.24, 0.3)]:
                if rng.random() < prob:
                    onsets_synth.append(t + offset)
                    # we won't bother re-rendering, just register the timing

        # Inter-call gap (same heavy-tailed formula as JS)
        base_gap = 0.4 + (1 - density) * (1 - drift_rate * 0.25) * 3.0
        u = rng.random()
        gap = base_gap * (0.3 + u**2.5 * 2.5)
        t += gap

    # Light gain envelope to avoid clipping & match perceived level of real
    out = out * 0.5
    return out, np.array(onsets_synth)

y_synth, onsets_synth = synth_engine(300, sr=sr, density=0.4)
print(f"  synthesised {len(y_synth)/sr:.0f}s, {len(onsets_synth)} call events")

# Run identical analyses on synthetic
freqs_s, psd_s = scipy.signal.welch(y_synth, fs=sr, nperseg=8192,
                                      scaling="density")
psd_s_db = 10 * np.log10(psd_s + 1e-12)
psd_s_db = psd_s_db - psd_s_db.max()

# Synthetic gap distribution (from the recorded onsets)
gaps_synth = np.diff(np.sort(onsets_synth))
gaps_synth = gaps_synth[gaps_synth > 0.01]

# Synthetic call rate
synth_rate = len(onsets_synth) / 300 * 60

print(f"  synth rate: {synth_rate:.1f}/min, real: {overall_rate:.1f}/min")
print(f"  synth gap mean: {gaps_synth.mean():.3f}s, real: {gaps.mean():.3f}s")

# ═════════════════════════════════════════════════════════════════════
# 8. Side-by-side comparison plot
# ═════════════════════════════════════════════════════════════════════
print("\n[7/7] Comparison figure...")
fig, axes = plt.subplots(2, 2, figsize=(12, 7))

# Spectrum overlay
ax = axes[0, 0]
ax.semilogx(freqs_audible, psd_audible, color=MOSS_DEEP, lw=1.4, label="real")
mask_s = (freqs_s >= 100) & (freqs_s <= 12000)
ax.semilogx(freqs_s[mask_s], psd_s_db[mask_s], color=RUST, lw=1.2,
             label="engine", alpha=0.85)
ax.axvspan(1000, 8000, color=MOSS, alpha=0.06)
ax.set_xlim(100, 12000)
ax.set_ylim(-60, 2)
ax.set_xlabel("frequency (Hz)")
ax.set_ylabel("relative power (dB)")
ax.set_title("Spectrum: real vs engine", loc="left", pad=8)
ax.legend(frameon=False, fontsize=9)
ax.grid(True)

# Gap distributions overlay (linear)
ax = axes[0, 1]
bins = np.linspace(0, max(gaps.max(), gaps_synth.max()), 50)
ax.hist(gaps, bins=bins, color=MOSS, alpha=0.5,
         edgecolor=MOSS_DEEP, density=True, label="real")
ax.hist(gaps_synth, bins=bins, color=RUST, alpha=0.4,
         edgecolor=RUST, density=True, label="engine")
ax.set_xlabel("inter-call gap (s)")
ax.set_ylabel("density")
ax.set_title("Gap distribution: real vs engine", loc="left", pad=8)
ax.legend(frameon=False, fontsize=9)
ax.grid(True)

# Density drift comparison
ax = axes[1, 0]
ax.plot(density_t, density, color=MOSS_DEEP, lw=1.0, label="real")
# Compute synth density on same window
n_w_synth = int(300 // window_s)
density_s = np.zeros(n_w_synth)
density_s_t = np.arange(n_w_synth) * window_s + window_s / 2
for i in range(n_w_synth):
    t0, t1 = i * window_s, (i + 1) * window_s
    density_s[i] = ((onsets_synth >= t0) &
                    (onsets_synth < t1)).sum() * (60 / window_s)
ax.plot(density_s_t, density_s, color=RUST, lw=1.0, label="engine", alpha=0.85)
ax.set_xlabel("time (s)")
ax.set_ylabel("calls / minute")
ax.set_title("Call density over time", loc="left", pad=8)
ax.legend(frameon=False, fontsize=9)
ax.grid(True)

# Spectrogram strip — first 60 s of each
ax = axes[1, 1]
real_strip = y[:60 * sr]
synth_strip = y_synth[:60 * sr]
S_r = np.abs(librosa.stft(real_strip, n_fft=1024, hop_length=256))
S_s = np.abs(librosa.stft(synth_strip, n_fft=1024, hop_length=256))
combined = np.concatenate([
    librosa.amplitude_to_db(S_r, ref=np.max),
    np.full((S_r.shape[0], 30), -80),
    librosa.amplitude_to_db(S_s, ref=np.max),
], axis=1)
img = ax.imshow(combined, aspect="auto", origin="lower", cmap="bone_r",
                 vmin=-60, vmax=0,
                 extent=[0, 130, 0, sr / 2])
ax.set_ylim(500, 9000)
ax.set_xlabel("time (s) — real | engine")
ax.set_ylabel("frequency (Hz)")
ax.set_title("60s spectrogram: real (left) | engine (right)",
              loc="left", pad=8)
ax.axvline(60, color="white", lw=2)
ax.axvline(70, color="white", lw=2)

plt.suptitle("Sentinels engine vs real dawn chorus",
              fontsize=13, y=1.00, x=0.13, ha="left",
              color=INK, weight="normal", style="italic")
plt.tight_layout()
plt.savefig(OUT / "comparison.png")
plt.close()

# ═════════════════════════════════════════════════════════════════════
# 9. Save numeric findings
# ═════════════════════════════════════════════════════════════════════
results = {
    "source": {
        "url": "https://freesound.org/people/squashy555/sounds/573080/",
        "title": "Dawn Chorus Birdsong",
        "recordist": "squashy555",
        "license": "CC0",
        "location": "Burton-on-Trent, Staffordshire, UK",
        "date": "2021-05-29 04:00",
        "format_analysed": "Freesound HQ MP3 preview (44.1 kHz stereo, 8:51)",
    },
    "real": {
        "duration_s": float(duration),
        "spectral_band_minus_10db_hz": [float(band_low), float(band_high)],
        "peak_frequency_hz": float(peak_freq),
        "n_call_onsets": int(n_onsets),
        "call_rate_per_minute_mean": float(overall_rate),
        "gap_mean_s": float(gaps.mean()),
        "gap_median_s": float(np.median(gaps)),
        "gap_std_s": float(gaps.std()),
        "gap_max_s": float(gaps.max()),
        "gap_lognormal_mu": float(ln_mu),
        "gap_lognormal_sigma": float(ln_sigma),
        "density_coefficient_of_variation": float(density_cv),
        "density_min_per_min": float(density.min()),
        "density_max_per_min": float(density.max()),
        "spectral_centroid_mean_hz": sc_mean,
        "spectral_centroid_cv_smoothed": float(sc_cv),
    },
    "synthetic_engine": {
        "duration_s": 300,
        "n_call_onsets": int(len(onsets_synth)),
        "call_rate_per_minute_mean": float(synth_rate),
        "gap_mean_s": float(gaps_synth.mean()),
        "gap_median_s": float(np.median(gaps_synth)),
        "frequency_centre_range_hz": [2400, 4800],
        "voice_types": ["sweep", "trill", "pip", "warble"],
    },
    "deltas": {
        "rate_ratio_engine_to_real": float(synth_rate / overall_rate),
        "gap_mean_ratio": float(gaps_synth.mean() / gaps.mean()),
        "peak_freq_distance_hz": float(peak_freq - 3600),  # midpoint of engine band
    },
}

with open("results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nDone. See figures/ and results.json for outputs.")
print(json.dumps(results["deltas"], indent=2))
