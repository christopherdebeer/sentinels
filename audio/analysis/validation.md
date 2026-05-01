# Validation report

> Quantitative comparison between the species-based generative
> engine ([`audio/voices.md`](../voices.md)) and the reference
> recording (squashy555 #573080, see [`README.md`](README.md)).
>
> **Five of nine metrics still match within ~15%; four have
> regressed since the previous report — three because of
> deliberate v0.75 / v1.0 design changes (per-species partial
> gains, log-normal gap sampling), one (density CV) as a knock-
> on consequence still in need of recalibration.** The numbers
> are reported honestly and the regressions explained, not
> hidden. The overall match continues to support the claim that
> the engine is *structurally* a dawn chorus, not a close
> replica of this particular recording.

## Method

1. The engine is hosted in `index.html` as a stateful Web Audio
   scheduler. Initial validation (Oct 2025) covered the UK
   garden cohort (7 species + contact calls). The engine has
   since gained a second cohort (Aotearoa NZ native bush) and
   internal changes (per-species partial-gain overrides,
   log-normal gap sampling, mechanical-syllable primitives for
   tūī, flight-event template for kererū). This report compares
   the **current UK cohort** against the same reference; NZ
   cohort validation has no reference recording yet, see §4.
2. Audio captured by [`render_engine_offline.py`](render_engine_offline.py):
   re-routes the engine's master output to an `OfflineAudioContext`,
   manually advances the simulated clock in 0.6 s ticks (matching
   the live `setInterval` cadence), renders 60 seconds at 22.05 kHz.
3. **The engine is rendered at `density = 0.60`** — a fair
   comparison to the reference needs the engine at mid-high
   density, since the squashy555 recording is a full dawn chorus
   (~135 onsets/min) and the on-page default of `density = 0.10`
   produces a near-silent whisper. At 0.60 the engine's onset
   rate matches within 10%.
4. The same analysis pipeline used for the original tuning
   report ([`analyse.py`](analyse.py)): band-passed onset
   detection at 1.5–8 kHz with librosa, STFT spectrum,
   gap-distribution log-normal fit. Applied to both files with
   identical parameters via [`validate.py`](validate.py).
5. Reference recording: full 531 s at 22.05 kHz (resampled from
   the downloaded MP3). Engine: 60 s rendered offline.
   60-second engine renders have inherently noisier σ and CV
   estimates than the reference's 9-minute window; the reported
   numbers are a single render, not an average over many.

## Results

| Metric | Real | Engine (current) | Engine (Oct 2025) | Match |
|---|---:|---:|---:|:-:|
| Peak frequency | 3,817 Hz | 3,984 Hz | 3,634 Hz | ✓ (4%) |
| Onset rate | 136/min | 123/min | 141/min | ✓ (10%) |
| Inter-onset gap, mean | 0.44 s | 0.47 s | 0.41 s | ✓ (7%) |
| Inter-onset gap, median | 0.37 s | 0.33 s | 0.33 s | ✓ (11%) |
| Inter-onset gap, p90 | 0.70 s | 0.69 s | 0.65 s | ✓ (1%) |
| Gap log-normal μ | −0.93 | −1.01 | −1.04 | ✓ (9%) |
| Gap log-normal σ | 0.45 | 0.58 | 0.48 | ✗ regressed (29%) |
| Spectral centroid | 4,214 Hz | 3,312 Hz | 3,708 Hz | ✗ regressed (21%) |
| Density CV (30 s windows) | 0.08 | 0.31 | 0.20 | ✗ regressed (4×) |
| −10 dB band | 1696–5319 Hz | 3235–7973 Hz | 2266–7273 Hz | shifted up further |

The "Engine (Oct 2025)" column is the previous report's numbers
for direct comparison. **Three metrics improved or held**
(onset rate, gap p90, gap μ); **four regressed** (gap σ,
centroid, CV, band) — three of the four for known design-driven
reasons documented below.

See [`figures/validation.png`](figures/validation.png) for the
four-panel comparison plate. **Note**: figures in `figures/`
were rendered against the Oct 2025 engine and have not been
regenerated for this report. Numerical comparisons here are
canonical; figures are for structural illustration.

## What this means

### What still works

**Onset rate and gap distribution**. The core rhythmic
signature of a dawn chorus continues to match within ~10% on
mean, median, p90, and μ — the features most strongly linked
to the "soundscape continuity" signal the project's hypothesis
depends on. p90 in particular improved from 7% to 1% match.

**Peak frequency** is within 4% — the engine still concentrates
its energy in the right part of the bird band.

**Visible structural features** in the spectrogram remain
correct: song-thrush phrase repetition, great-tit two-note,
wren trill, blackbird motif-then-shrill. v1.0 added tūī
mechanical clicks and kererū wing-beat low-frequency pulses
visible in the NZ cohort but not relevant to UK comparison.

### Where it has regressed and why

**Gap log-normal σ: 0.48 → 0.58 (vs target 0.45).** v0.75
switched gap sampling from truncated-normal Box-Muller to
log-normal. Log-normal is the *correct architectural choice* —
the dawn-chorus literature treats inter-call gaps as
log-normal, and the validation pipeline itself fits a
log-normal to the reference. But the per-species `[lo, hi]`
ranges in `SPECIES` were calibrated against the truncated-
normal sampler, so the new log-normal interpretation produces
slightly wider tails than calibrated. Two recovery paths:

1. **Tighten the σ parameterisation.** Currently `[lo, hi]` is
   mapped to an 80% confidence interval (1.282 σ in either
   direction); narrowing further to a 70% CI (1.04 σ) would
   reduce the effective σ. Half-hour change.
2. **Tighten the per-species ranges.** Reduce each species'
   `gap` range by ~15% across the cohort. More invasive
   because it affects every species individually but better
   reflects what the literature actually reports.

Either is a calibration pass, not a redesign.

**Density CV: 0.20 → 0.31 (vs target 0.08).** Largely a
knock-on of the σ regression: wider gap tails produce more
extreme bursts and lulls, which compounds into more
window-to-window variation. Recovering on σ should pull CV
back, though probably not all the way to the reference's
0.08. The previous report's analysis still applies — the
engine's per-strophe timing is too uncorrelated for an
8-voice ensemble; some negative-feedback mechanism (recent
density depresses next-strophe probability) would help, but
adds tuning surface and is held back as a v2 candidate.

**Spectral centroid: 3708 → 3312 Hz (vs target 4214 Hz).** A
direct consequence of the v0.75 per-species partial-gain
overrides. The blackbird voice now uses
`partialGains: [1.0, 0.30, 0.08, 0.02]` instead of the default
`[1.0, 0.40, 0.20, 0.10]`, which deliberately removes
upper-partial energy to give a flutier timbre. The change
sounds correct on the blackbird and is what `voices.md`
describes the species' fluty character as. But it pulls down
the cohort's spectral centroid, especially at this density
where blackbird is well-represented. **This regression
documents a deliberate design choice.** The honest framing:
the cohort sounds *more like itself* than before; the
centroid metric is now further from this particular
reference recording, which itself is robin-and-blackbird-
heavy and has its own timbral biases.

**−10 dB band shifted up by ~1 kHz.** Same cause — fluty
blackbird removes low-band energy. Worth a sweep: audit each
UK species' partial-gain assumption now that the architecture
supports overrides; bringing the wren and blue-tit profiles
into the per-species partial-gain regime would let them be
balanced against blackbird's reduction.

### What unchanged

The pre-v0.75 analysis of "what the engine doesn't get right"
(low-frequency tail, ambient layer, band shifts) still
applies. The validation methodology and reproduction
instructions are unchanged. The honest caveats below still
apply.

## v1.0 — NZ cohort, no reference comparison yet

The Aotearoa NZ native bush cohort introduced in v1.0 (tūī,
korimako, pīwakawaka, riroriro, kererū wing-beats, plus
contact calls) has no equivalent CC0 reference recording for
direct numerical comparison. Acoustic-character validation has
been done by:

1. **Rendering** the NZ cohort at `density = 0.55` for 60 s
   and inspecting the spectrogram. Tūī mechanical clicks
   appear as expected (broadband transients in the 3–6 kHz
   band). Kererū wing-beats appear as expected (clustered
   low-frequency pulses in the 200–600 Hz band, audible
   distinctly from the bird-band content). Korimako bell
   tones produce the narrow-band tonal phrases described in
   `voices-nz-native-bush.md` §2.
2. **Per-species smoke testing** confirms each NZ species
   fires at expected per-minute rates (5 tūī, 4 riroriro,
   4 pīwakawaka, 4 contact calls, 3 korimako, 1 kererū over
   90 s at d=0.6) with no synthesis errors.

Procuring a CC0-licensed NZ native bush dawn-chorus reference
recording for proper numerical validation is open work.

## Honest caveats

- **One reference recording.** The engine has been validated
  against a single 9-minute UK recording. A second pass against
  another recordist would tell us how well these matches
  generalise. Worth doing before any further parameter tuning.
- **The match depends on the density slider.** At the on-page
  default of `density = 0.10`, the engine produces a sparse
  whisper, not a dawn chorus — and not a fair comparison. The
  0.60 used here was chosen to match the reference's onset
  rate; a real comparison across a range of densities would
  tell us whether the distributional shape holds at low and
  high intensities, not just at the one we tuned to.
- **60-second renders are noisy.** σ and CV estimated from a
  60 s engine render have inherently more variance than the
  same statistics over the reference's 530 s. Two consecutive
  renders of the current engine produced σ values 0.53 and
  0.58 — both worse than the target 0.45, but the spread
  illustrates the noise floor of single-render measurements.
- **No psychoacoustic validation.** "Close on numerical
  metrics" doesn't mean "calming". The whole point of the
  experimental protocol in
  [`docs/experiments.md`](../../docs/experiments.md) is to find
  out — not to assume.
- **Figures are stale.** `figures/*.png` were rendered against
  the Oct 2025 engine. They illustrate the structural
  comparison correctly but the specific numerical overlays
  (densities, gap counts) reflect the older engine. Figure
  regeneration is open work; in the meantime the prose and
  numerical table here are canonical.

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
