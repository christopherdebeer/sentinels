"""
Regenerate figures/validation.png — a 2x2 plate comparing the rendered
engine output (new_engine.wav) against the reference dawn-chorus
recording (preview.mp3) on four metrics:

  ┌─────────────────────────┬─────────────────────────┐
  │  onset density drift    │  inter-call gap distrib.│
  ├─────────────────────────┼─────────────────────────┤
  │  averaged spectrum      │  side-by-side spectrogram│
  └─────────────────────────┴─────────────────────────┘

Dependencies: librosa, matplotlib, scipy, numpy (same as analyse.py).
This script does not reimplement the engine — it reads the already-
rendered new_engine.wav produced by render_engine_offline.py, so the
figure always reflects the currently-committed index.html engine.

Usage (from repo root or any CWD):
    python3 audio/analysis/produce_validation_figure.py
"""
import numpy as np
import librosa
import scipy.signal as signal
import matplotlib as mpl
import matplotlib.pyplot as plt
from pathlib import Path

ANALYSIS = Path(__file__).resolve().parent
OUT = ANALYSIS / "figures"
OUT.mkdir(exist_ok=True)

REAL = ANALYSIS / "preview.mp3"
ENG = ANALYSIS / "new_engine.wav"

# Project palette — match the landing-page figure aesthetic.
PAPER = "#f5f0e6"
INK = "#1a1612"
INK_SOFT = "#3d362e"
INK_FAINT = "#6b5f51"
MOSS = "#5a6b4a"
MOSS_DEEP = "#404e35"
RUST = "#a85a3a"

mpl.rcParams.update({
    "figure.facecolor": PAPER,
    "axes.facecolor": PAPER,
    "savefig.facecolor": PAPER,
    "savefig.bbox": "tight",
    "savefig.dpi": 130,
    "axes.edgecolor": INK_FAINT,
    "axes.labelcolor": INK_SOFT,
    "axes.titlecolor": INK,
    "xtick.color": INK_FAINT,
    "ytick.color": INK_FAINT,
    "text.color": INK,
    "font.family": "serif",
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.titleweight": "normal",
    "axes.grid": False,
    "legend.frameon": False,
    "legend.fontsize": 9,
})


def analyse(path, label, sr=22050):
    y, _ = librosa.load(str(path), sr=sr, mono=True)
    duration = len(y) / sr

    # Long-term averaged spectrum
    n_fft = 4096
    S = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=n_fft // 4))
    freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
    ltas = np.mean(S, axis=1)
    ltas_db = 20 * np.log10(ltas / ltas.max() + 1e-10)

    # Bird-band onset detection (same parameters as validate.py)
    sos = signal.butter(4, [1500, 8000], btype="band", fs=sr, output="sos")
    y_band = signal.sosfilt(sos, y)
    o_env = librosa.onset.onset_strength(y=y_band, sr=sr, hop_length=1024)
    onset_frames = librosa.onset.onset_detect(
        onset_envelope=o_env, sr=sr, hop_length=1024,
        backtrack=False, pre_max=4, post_max=4,
        pre_avg=4, post_avg=4, delta=0.07, wait=2,
    )
    onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=1024)
    gaps = np.diff(onset_times)
    gaps = gaps[gaps > 0]

    # Density drift (calls/min in 10s windows for short, 30s for long)
    win = 30.0 if duration > 60 else 10.0
    edges = np.arange(0, duration + win, win)
    density_counts = np.histogram(onset_times, bins=edges)[0]
    density_rate = density_counts * (60 / win)
    density_t = edges[:-1] + win / 2

    # Spectrogram (first 60s only — we only show the first minute)
    strip_len = min(len(y), 60 * sr)
    y_strip = y[:strip_len]
    S_strip = np.abs(librosa.stft(y_strip, n_fft=1024, hop_length=256))
    S_db = librosa.amplitude_to_db(S_strip, ref=np.max)
    strip_sec = strip_len / sr

    return dict(
        label=label, duration=duration, sr=sr,
        freqs=freqs, ltas_db=ltas_db,
        onset_times=onset_times, gaps=gaps,
        density_t=density_t, density_rate=density_rate, win=win,
        S_db=S_db, strip_sec=strip_sec,
    )


def main():
    if not REAL.exists():
        raise SystemExit(f"missing {REAL} — run `curl` in README.md to fetch preview.mp3")
    if not ENG.exists():
        raise SystemExit(f"missing {ENG} — run render_engine_offline.py first")

    real = analyse(REAL, "real (squashy555)")
    eng = analyse(ENG, "engine")

    fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)

    # ───────── Panel A: onset density over time ─────────
    ax = axes[0, 0]
    ax.plot(real["density_t"], real["density_rate"],
            color=MOSS_DEEP, lw=1.2, label=f"real — {real['duration']:.0f}s, mean {real['density_rate'].mean():.0f}/min")
    ax.plot(eng["density_t"], eng["density_rate"],
            color=RUST, lw=1.2, label=f"engine — {eng['duration']:.0f}s, mean {eng['density_rate'].mean():.0f}/min")
    ax.set_xlabel("time (s)")
    ax.set_ylabel("onsets per minute")
    ax.set_title("Onset density", loc="left", pad=6)
    ax.legend(loc="lower right")
    ax.grid(True, color=INK_FAINT, alpha=0.15, linewidth=0.5)

    # ───────── Panel B: gap distribution ─────────
    ax = axes[0, 1]
    max_gap = max(np.percentile(real["gaps"], 98),
                  np.percentile(eng["gaps"], 98),
                  1.5)
    bins = np.linspace(0, max_gap, 40)
    ax.hist(real["gaps"], bins=bins, density=True,
            color=MOSS, alpha=0.55, edgecolor=MOSS_DEEP,
            label=f"real (μ={np.log(real['gaps']).mean():.2f}, σ={np.log(real['gaps']).std():.2f})")
    ax.hist(eng["gaps"], bins=bins, density=True,
            color=RUST, alpha=0.40, edgecolor=RUST,
            label=f"engine (μ={np.log(eng['gaps']).mean():.2f}, σ={np.log(eng['gaps']).std():.2f})")
    ax.set_xlabel("inter-onset gap (s)")
    ax.set_ylabel("density")
    ax.set_title("Gap distribution (log-normal fit parameters)", loc="left", pad=6)
    ax.legend(loc="upper right")
    ax.grid(True, color=INK_FAINT, alpha=0.15, linewidth=0.5)

    # ───────── Panel C: averaged spectrum overlay ─────────
    ax = axes[1, 0]
    # Clip to audible / bird-relevant range for readability
    f_r, db_r = real["freqs"], real["ltas_db"]
    f_e, db_e = eng["freqs"], eng["ltas_db"]
    r_mask = (f_r >= 100) & (f_r <= 12000)
    e_mask = (f_e >= 100) & (f_e <= 12000)
    ax.semilogx(f_r[r_mask], db_r[r_mask],
                color=MOSS_DEEP, lw=1.4, label="real")
    ax.semilogx(f_e[e_mask], db_e[e_mask],
                color=RUST, lw=1.2, label="engine", alpha=0.9)
    ax.axvspan(1000, 8000, color=MOSS, alpha=0.06, label="bird band")
    # −10 dB guide line
    ax.axhline(-10, color=INK_FAINT, lw=0.8, alpha=0.5, linestyle=":")
    ax.annotate("−10 dB", xy=(110, -10), xytext=(110, -8),
                fontsize=8, color=INK_FAINT)
    ax.set_xlim(100, 12000)
    ax.set_ylim(-60, 2)
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("relative power (dB, peak-normalised)")
    ax.set_title("Averaged spectrum", loc="left", pad=6)
    ax.legend(loc="lower center")
    ax.grid(True, color=INK_FAINT, alpha=0.15, linewidth=0.5)

    # ───────── Panel D: 60s spectrogram side-by-side ─────────
    ax = axes[1, 1]
    # Build a combined image: [real | gap | engine]
    r_S = real["S_db"]
    e_S = eng["S_db"]
    # Equalise frame counts (use the shorter of the two)
    n_cols = min(r_S.shape[1], e_S.shape[1])
    r_strip = r_S[:, :n_cols]
    e_strip = e_S[:, :n_cols]
    gap_cols = int(n_cols * 0.03)  # 3% visual separator
    separator = np.full((r_strip.shape[0], gap_cols), -80)
    combined = np.concatenate([r_strip, separator, e_strip], axis=1)
    # 60s each side
    strip_sec = min(real["strip_sec"], eng["strip_sec"])
    total_sec = strip_sec * 2 + strip_sec * 0.03
    img = ax.imshow(combined, aspect="auto", origin="lower", cmap="bone_r",
                    vmin=-60, vmax=0,
                    extent=[0, total_sec, 0, real["sr"] / 2])
    ax.set_ylim(500, 9000)
    ax.set_xlabel(f"time (s) — real (left, 0–{strip_sec:.0f}s) | engine (right, 0–{strip_sec:.0f}s)")
    ax.set_ylabel("frequency (Hz)")
    ax.set_title("Spectrogram, first minute of each", loc="left", pad=6)
    # Separator guide lines
    ax.axvline(strip_sec, color=PAPER, lw=2)
    ax.axvline(strip_sec + strip_sec * 0.03, color=PAPER, lw=2)

    plt.suptitle("Engine vs. reference dawn chorus — four-panel validation plate",
                 x=0.02, y=1.02, ha="left",
                 fontsize=13, color=INK, style="italic")

    out = OUT / "validation.png"
    plt.savefig(out)
    plt.close()
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
