"""Compare new engine output against the squashy555 reference."""
import numpy as np
import librosa
import scipy.signal as signal
import json
from pathlib import Path

ANALYSIS = Path("/home/claude/sentinels/audio/analysis")

def analyse(path, label):
    y, sr = librosa.load(str(path), sr=22050, mono=True)
    duration = len(y) / sr
    print(f"\n{label}: {duration:.1f}s @ {sr}Hz")

    n_fft = 4096
    S = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=n_fft//4))
    freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
    ltas = np.mean(S, axis=1)
    peak_freq = freqs[np.argmax(ltas)]

    ltas_db = 20 * np.log10(ltas / ltas.max() + 1e-10)
    above = ltas_db > -10
    band_idx = np.where(above)[0]
    band_lo = freqs[band_idx[0]] if len(band_idx) else 0
    band_hi = freqs[band_idx[-1]] if len(band_idx) else 0

    sos = signal.butter(4, [1500, 8000], btype='band', fs=sr, output='sos')
    y_band = signal.sosfilt(sos, y)
    o_env = librosa.onset.onset_strength(y=y_band, sr=sr, hop_length=1024)
    onsets = librosa.onset.onset_detect(
        onset_envelope=o_env, sr=sr, hop_length=1024,
        backtrack=False, pre_max=4, post_max=4,
        pre_avg=4, post_avg=4, delta=0.07, wait=2,
    )
    onset_times = librosa.frames_to_time(onsets, sr=sr, hop_length=1024)
    n_onsets = len(onset_times)
    rate = n_onsets / duration * 60

    gaps = np.diff(onset_times)
    if len(gaps) > 0:
        gap_mean = float(np.mean(gaps))
        gap_med = float(np.median(gaps))
        gap_p90 = float(np.percentile(gaps, 90))
        positive = gaps[gaps > 0]
        log_gaps = np.log(positive) if len(positive) else np.array([0])
        gap_mu = float(np.mean(log_gaps))
        gap_sigma = float(np.std(log_gaps))
    else:
        gap_mean = gap_med = gap_p90 = gap_mu = gap_sigma = 0

    win = 30 if duration > 60 else 10
    edges = np.arange(0, duration+win, win)
    density = np.histogram(onset_times, bins=edges)[0] * (60/win)
    density_cv = float(density.std() / density.mean()) if (len(density) > 1 and density.mean() > 0) else 0

    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]

    return {
        'label': label, 'duration_s': float(duration),
        'peak_freq_hz': float(peak_freq),
        'band_minus10db_hz': [float(band_lo), float(band_hi)],
        'n_onsets': int(n_onsets), 'onset_rate_per_min': float(rate),
        'gap_mean_s': gap_mean, 'gap_median_s': gap_med, 'gap_p90_s': gap_p90,
        'gap_lognormal_mu': gap_mu, 'gap_lognormal_sigma': gap_sigma,
        'density_cv': density_cv,
        'centroid_mean_hz': float(np.mean(centroid)),
        'centroid_std_hz': float(np.std(centroid)),
    }

real = analyse(ANALYSIS / "preview.mp3", "REAL squashy555")
new = analyse(ANALYSIS / "new_engine.wav", "NEW ENGINE")

print()
print("="*78)
print(f"  {'Metric':<28s} {'Real':>16s} {'New engine':>16s}   Verdict")
print("="*78)
metrics = [
    ('peak_freq_hz', 'peak frequency', '%.0f Hz'),
    ('onset_rate_per_min', 'onset rate', '%.1f/min'),
    ('gap_mean_s', 'inter-onset gap mean', '%.2f s'),
    ('gap_median_s', 'inter-onset gap median', '%.2f s'),
    ('gap_p90_s', 'inter-onset gap p90', '%.2f s'),
    ('gap_lognormal_mu', 'gap lognormal mu', '%.2f'),
    ('gap_lognormal_sigma', 'gap lognormal sigma', '%.2f'),
    ('density_cv', 'density CV (windows)', '%.2f'),
    ('centroid_mean_hz', 'centroid mean', '%.0f Hz'),
]
for key, name, fmt in metrics:
    r = real[key]; n = new[key]
    if r == 0:
        print(f"  {name:<28s} {fmt % r:>16s} {fmt % n:>16s}")
        continue
    delta = abs(n - r) / abs(r)
    verdict = "match" if delta < 0.25 else ("close" if delta < 0.6 else "off")
    print(f"  {name:<28s} {fmt % r:>16s} {fmt % n:>16s}   {verdict}")

# Band
rb = real['band_minus10db_hz']; nb = new['band_minus10db_hz']
print(f"  {'-10 dB band':<28s} {'%.0f-%.0f Hz' % tuple(rb):>16s} {'%.0f-%.0f Hz' % tuple(nb):>16s}")

with open(ANALYSIS / "validation.json", 'w') as f:
    json.dump({'real': real, 'new_engine': new}, f, indent=2)
print(f"\nSaved: {ANALYSIS}/validation.json")
