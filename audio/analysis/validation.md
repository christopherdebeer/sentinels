# Validation report

> Quantitative comparison between the species-based generative
> engine ([`audio/voices.md`](../voices.md)) and the reference
> recording (squashy555 #573080, see [`README.md`](README.md)).
>
> **Temporal and spectral metrics: eight of nine within ~15%.**
> One metric — density coefficient of variation — is clearly
> off (engine 2.5× burstier than the reference); see §3 below.
> The overall match is good enough to support the claim that the
> engine is *structurally* a dawn-chorus, not a close replica of
> this particular recording.

## Method

1. The engine is hosted in `index.html` as a stateful Web Audio
   scheduler with seven species voices plus a contact-call
   background voice (UK garden cohort).
2. Audio captured by [`render_engine_offline.py`](render_engine_offline.py):
   re-routes the engine's master output to an `OfflineAudioContext`,
   manually advances the simulated clock in 0.6s ticks (matching
   the live `setInterval` cadence), renders 60 seconds at 22.05 kHz.
3. **The engine is rendered at `density = 0.60`** — a fair
   comparison to the reference needs the engine at mid-high
   density, since the squashy555 recording is a full dawn chorus
   (~135 onsets/min) and the on-page default of `density = 0.10`
   produces a near-silent whisper (~24 onsets/min). At 0.60 the
   engine's onset rate matches the reference within 3%.
4. The same analysis pipeline used for the original tuning
   report ([`analyse.py`](analyse.py)): band-passed onset
   detection at 1.5–8 kHz with librosa, STFT spectrum,
   gap-distribution log-normal fit. Applied to both files with
   identical parameters via [`validate.py`](validate.py).
5. Reference recording: full 531 s at 22.05 kHz (resampled from
   the downloaded MP3). Engine: 60 s rendered offline. Rates and
   distributional statistics are duration-invariant; absolute
   counts are not, but rates per-minute are reported.

## Results

| Metric | Real | New engine | Match |
|---|---:|---:|:-:|
| Peak frequency | 3,817 Hz | 3,634 Hz | ✓ (5%) |
| Onset rate | 136/min | 141/min | ✓ (3%) |
| Inter-onset gap, mean | 0.44 s | 0.41 s | ✓ (7%) |
| Inter-onset gap, median | 0.37 s | 0.33 s | ✓ (11%) |
| Inter-onset gap, p90 | 0.70 s | 0.65 s | ✓ (7%) |
| Gap log-normal μ | −0.93 | −1.04 | ✓ (12%) |
| Gap log-normal σ | 0.45 | 0.48 | ✓ (7%) |
| Spectral centroid, mean | 4,214 Hz | 3,708 Hz | ✓ (12%) |
| Density CV (30 s windows) | 0.08 | 0.20 | ✗ (2.5×) |
| −10 dB band | 1696–5319 Hz | 2266–7273 Hz | band shifts up ~500 Hz |

See [`figures/validation.png`](figures/validation.png) for the
four-panel comparison: onset density over time, inter-call gap
distribution with log-normal fits, averaged spectrum across the
bird band, and spectrograms of the first minute of each.

## What this means

### What the engine gets right

**Onset rate and gap distribution match.** This is the core
rhythmic signature of a dawn chorus and it lines up within ~10%
on every gap statistic — mean, median, p90, and the log-normal
fit parameters. The gap distribution is the feature most
strongly linked to the "soundscape continuity" signal the
project's hypothesis depends on.

**Peak frequency and spectral centroid match.** The engine
produces its energy in the right part of the bird band, peaking
around 3.6 kHz against the reference's 3.8 kHz. The spectral
centroid — a rough perceptual brightness measure — sits around
3.7 kHz against real 4.2 kHz. Both are within instrument
tolerance for species-level variation.

**Visible structural features** that the previous ad-hoc engine
did not produce, now visible in the spectrogram:
- Song-thrush phrase repetition (2–4 identical vertical patterns).
- Great-tit two-note teacher-teacher (paired horizontal rails).
- Wren trill (rapid descending stripes).
- Blackbird motif-then-shrill structure.

### What it doesn't get right

**Density CV is 2.5× too high.** Real chorus is remarkably
*uniform* across 30-second windows (CV 0.08: ± ~8% of the mean).
The engine produces more burstiness (CV 0.20: ± ~20%) — audibly
"clumpy" with brief flurries and lulls rather than the steady
haze of a real chorus. This is visible directly in the
spectrogram panel: the reference's first minute reads as a
consistent mid-band mist; the engine's reads as a series of
clusters with visible gaps between.

Two plausible contributors, both tunable without redesign:

1. **Per-strophe timing is too correlated.** Each species
   schedules its next strophe by sampling from its own gap
   distribution. When the gap distribution is wide (log-normal σ
   above ~0.45), a "short gap" from one voice and a "short gap"
   from the next are uncorrelated, which — with eight voices —
   produces occasional synchronised bursts by chance alone.
   Adding a mild negative-feedback term (if the last second had
   many onsets, extend the next gap) would flatten this without
   changing the marginal distributions.
2. **No explicit ambient layer.** Real chorus is heard against
   a continuous substrate of wind-in-foliage, distant traffic,
   and insect noise that adds non-onset energy in the 100–1500 Hz
   band. The engine's continuous-bed is narrowly band-passed at
   ~2200 Hz and contributes little below 1500 Hz. This is both
   a CV issue (ambient fills the lulls) and a spectrum issue
   (see below).

**Sub-1500 Hz energy is missing.** The reference has a long tail
of low-frequency energy from foliage rustle, distant traffic,
and the lower half of the blackbird motif. The engine has very
little energy below 1500 Hz:
- The blackbird voice's low band reaches only down to 1500 Hz
- The continuous bed is band-passed around 2200 Hz with limited skirts
- No explicit "ambient" voice models foliage / wind

The averaged-spectrum panel makes this vivid — the engine's
curve rolls off a full 20 dB below 500 Hz compared to the
reference. Fix would be trivial (widen the bed's band-pass, add
a low-amp pink-noise voice in the 100–500 Hz range), at some
cost in tonal clarity. Not worth doing without listener testing.

**−10 dB band shifts up by ~500 Hz.** Real recording:
1696–5319 Hz. Engine: 2266–7273 Hz. The engine's upper bound is
~2 kHz higher because of the wren and blue-tit contributions in
the 5000–8500 Hz range — which the reference has *less* of than
literature suggests is typical for a UK chorus. Likely a cohort-
balance question: this recording is robin-and-blackbird-heavy;
the engine has proportionally more wren/tit contribution.
Adjustable via the `COHORT_UK_GARDEN` weights.

## Honest caveats

- **One reference recording.** The engine has been validated
  against a single 9-minute recording. A second pass against the
  Peak District set (xeno-canto set 3781) and another from a
  different recordist would tell us how well these matches
  generalise. Worth doing before any further parameter tuning.
- **The match depends on the density slider.** At the on-page
  default of `density = 0.10`, the engine produces ~24 onsets/min
  — a rate that no real dawn chorus reaches, and not a fair
  comparison. The 0.60 used here was chosen to match the reference's
  onset rate; a real comparison across a range of densities would
  tell us whether the distributional shape holds at low and high
  intensities, not just at the one we tuned to.
- **Onset detection is itself approximate.** The detector finds
  acoustic transients above threshold; it conflates closely
  spaced calls and misses very quiet ones. Both files are
  processed identically so the comparison is fair, but absolute
  rates should be read with caution (~±10%).
- **No psychoacoustic validation.** "Close on numerical metrics"
  doesn't necessarily mean "calming". The whole point of the
  experimental protocol in
  [`docs/experiments.md`](../../docs/experiments.md) is to find
  out — not to assume.

## Reproducing

```bash
# 1. From repo root, serve the page so the engine loads in a browser
python3 -m http.server 8765 &

# 2. Render the engine offline (drives headless chromium via Playwright)
python3 audio/analysis/render_engine_offline.py
# → audio/analysis/new_engine.wav (60 s, 22.05 kHz)

# 3. Numerical comparison
python3 audio/analysis/validate.py
# → audio/analysis/validation.json

# 4. Regenerate the validation plate
python3 audio/analysis/produce_validation_figure.py
# → audio/analysis/figures/validation.png
```

First-time setup:

```bash
# Reference recording (12 MB MP3, CC0)
curl -L -o audio/analysis/preview.mp3 \
  "https://freesound.org/data/previews/573/573080_1149179-hq.mp3"

# Python dependencies
python3 -m pip install --user librosa soundfile matplotlib scipy numpy playwright
python3 -m playwright install chromium
```
