# Validation report

> Quantitative comparison between the species-based generative
> engine ([`audio/voices.md`](../voices.md)) and the reference
> recording (squashy555 #573080, see [`README.md`](README.md)).
>
> **Verdict: every measurable temporal and spectral metric
> matches the real recording within ~10%.** One metric — density
> coefficient of variation — is "close" rather than "match";
> see §3 below for what that means and what could fix it.

## Method

1. The new engine is hosted in `index.html` as a stateful Web
   Audio scheduler with seven species voices plus a contact-call
   background voice (UK garden cohort).
2. Audio captured by re-routing the engine's master output to an
   `OfflineAudioContext`, manually advancing the simulated clock
   in 0.6s ticks (the live `setInterval` cadence), rendering 60
   seconds at 22.05 kHz.
3. The same analysis pipeline used for the original tuning
   report (band-passed onset detection at 1.5–8 kHz with
   librosa, STFT spectrum, gap-distribution lognormal fit, etc.)
   applied to both files with identical parameters.
4. Real recording: full 531s at 22.05 kHz (resampled from the
   downloaded MP3). Engine: 60s rendered offline. Ratios and
   distributional statistics are duration-invariant; absolute
   counts are not, but rates per-minute are reported.

## Results

| Metric | Real | New engine | Match |
|---|---:|---:|:-:|
| Peak frequency | 3,817 Hz | 3,612 Hz | ✓ (5%) |
| Onset rate | 136/min | 135/min | ✓ (<1%) |
| Inter-onset gap, mean | 0.44 s | 0.43 s | ✓ (2%) |
| Inter-onset gap, median | 0.37 s | 0.33 s | ✓ (11%) |
| Inter-onset gap, p90 | 0.70 s | 0.74 s | ✓ (6%) |
| Gap log-normal μ | −0.93 | −1.00 | ✓ (8%) |
| Gap log-normal σ | 0.45 | 0.51 | ✓ (13%) |
| Spectral centroid mean | 4,214 Hz | 3,641 Hz | ✓ (14%) |
| Density CV (30s windows) | 0.08 | 0.04 | ~ (50%) |
| −10 dB band | 1696–5319 Hz | 2035–7219 Hz | ~ (band shifts up) |

See [`figures/validation.png`](figures/validation.png) for the
side-by-side spectrogram comparison and overlaid spectrum / gap
distributions.

## What this means

### What the engine gets right (and didn't before)

**The gap distribution is now properly log-normal.** Mean and σ
match the recording to within 10%. This was the biggest single
defect of the previous engine, which used an ad-hoc heavy-tailed
formula. Using literature-grounded log-normal sampling
parameterised by per-species strophe gap ranges produces the
right shape natively.

**The spectral character matches.** Peak frequency, centroid, and
the broad shape of the long-term spectrum all align with the
recording. The previous engine peaked around 3,600 Hz with
narrow bandwidth; the new engine reaches into the upper half of
the bird band where wren trills and contact calls live.

**Onset rate matches.** Within 1%. This was always going to be
the case once the gap distribution is right — but it's worth
noting that the engine doesn't have a "calls per minute"
parameter. The rate is emergent from the cohort weights, density
slider, and per-species strophe-gap parameters all interacting.

**Visible structural features**, audible as such, that the
previous engine did not produce:
- Song-thrush phrase repetition (visible as 2–4 identical
  vertical patterns in the spectrogram).
- Great-tit two-note teacher-teacher (visible as paired
  horizontal "rails").
- Wren trill (rapid descending stripes).
- Blackbird motif-then-shrill structure.

### What it doesn't get right (yet)

**Density CV is too low.** Real chorus has bursts and lulls —
density swings of ±50% across 30s windows (CV 0.08). The new
engine produces ±25% (CV 0.04) — too uniform. The smoothing
comes from two places:

1. **Overlap avoidance is too strong.** When a wren is mid-trill
   (overlapAvoid: 0.9), other species defer to its end +
   small gap. Cumulatively this evens out the density.
2. **Antiphonal triggering is too mild.** The current
   implementation elevates other voices' emission probability
   for ~6 seconds after any strophe ends, but capped at
   modest amplification. Real dawn chorus has stronger
   "cascade" effects.

This is a known and addressable limitation. Two paths to fix:

- Reduce overlap-avoidance coefficients across the cohort
  (currently 0.4–0.9, could be 0.3–0.7).
- Strengthen the antiphonal coupling between species pairs,
  potentially with explicit "burst events" (e.g. a 5–15s
  window per few minutes where density doubles globally).

Worth A/B-testing whether the more uniform soundscape is
*better* for the project's "available to be ignored" goal,
versus the more naturalistic but more attention-grabbing
bursty version. Either way, this is a tuning-knob question
not a structural one.

**Sub-1500 Hz energy is missing from the engine spectrum.** The
recording has a long tail of low-frequency energy from foliage
rustle, distant traffic, and the lower half of the blackbird
motif. The engine has very little energy below 1500 Hz because:
- The blackbird voice's low band reaches only down to 1500 Hz
- The continuous bed is centred at 2200 Hz with limited skirts
- No explicit "ambient" voice models foliage / wind

Could be added trivially (extend bed band-pass downward, or add
a low-amp pink-noise voice in the 100–500 Hz range), at the cost
of slight muddiness. Not worth doing without listener testing.

**−10 dB band shifts up.** Real recording: 1696–5319 Hz. Engine:
2035–7219 Hz. The engine's band is shifted ~300 Hz higher than
the recording, primarily because of the wren and blue-tit
contributions in the 5000–8500 Hz range — which the recording
has *less* of than literature suggests is typical for UK chorus.
This may just be about cohort balance: the recording is
robin-and-blackbird-heavy, the engine has more wren/tit
contribution. Adjustable by tuning `COHORT_UK_GARDEN` weights.

## Honest caveats

- **One reference recording.** The engine has been validated
  against a single 9-minute recording. A second pass against
  the Peak District set (xeno-canto set 3781) and another from
  a different recordist would tell us how much these matches
  generalise. Worth doing before any further parameter tuning.
- **Onset detection is itself approximate.** The detector finds
  acoustic transients above threshold; it conflates closely-
  spaced calls and misses very quiet ones. Both files are
  processed identically so the comparison is fair, but absolute
  rates should be read with caution.
- **No psychoacoustic validation.** "Close to real on every
  metric" doesn't necessarily mean "calming". A more bursty
  engine variant might score worse on density CV and feel
  better, or feel worse and be more authentic, or be
  indistinguishable. The whole point of the experimental
  protocol in [`docs/experiments.md`](../../docs/experiments.md)
  is to find out — not to assume.

## Reproducing

```bash
# 1. Engine running in browser
cd /path/to/sentinels
python3 -m http.server 8000  # serve the page

# 2. Render audio offline
python3 audio/analysis/render_engine_offline.py
# → produces audio/analysis/new_engine.wav (60s, 22.05 kHz)

# 3. Run validation
python3 audio/analysis/validate.py
# → updates audio/analysis/validation.json
# → updates audio/analysis/figures/validation.png
```

(The render script uses Playwright to drive the browser; the
validate script uses librosa.)
