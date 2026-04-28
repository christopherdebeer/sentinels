# Analysis

Programmatic analysis of the recommended Phase 0 audio source —
[squashy555 / Dawn Chorus Birdsong](https://freesound.org/people/squashy555/sounds/573080/)
(CC0, recorded Burton-on-Trent UK, May 2021) — informing the
parameters of the procedural audio engine on the project landing page.

Read [`tuning-report.md`](tuning-report.md) for the findings and
recommended engine changes. Read [`results.json`](results.json) for
the raw numbers.

## What's here

```
analyse.py            — single-script analysis pipeline
tuning-report.md      — human-readable findings & engine tuning recipe
results.json          — numerical findings
figures/
  spectrum.png        — frequency content of the real recording
  spectrogram.png     — full time-frequency view (real)
  onsets.png          — detected call events overlaid on spectrogram
  gap-distribution.png — inter-call gap statistics with log-normal fit
  density-drift.png   — call rate & spectral centroid over time
  comparison.png      — real vs engine, side-by-side, four panels
```

The audio file itself (`preview.mp3`) is not committed to the
repository — see "Reproducing" below to fetch it.

## Reproducing

```bash
cd audio/analysis

# Fetch the Freesound HQ preview (12 MB, CC0)
curl -L -o preview.mp3 \
  "https://freesound.org/data/previews/573/573080_1149179-hq.mp3"

# Install the Python deps
pip install librosa soundfile matplotlib scipy numpy

# Run the pipeline (~30 seconds)
python3 analyse.py
```

The script downsamples to 22.05 kHz on load to keep memory under
control. Bird-band content is below 11 kHz so all relevant frequencies
are preserved, but if you want full-rate analysis (44.1 kHz) edit
the `sr=22050` parameter in `librosa.load(...)`.

## Approach notes

The analysis is structured as four parallel investigations:

**Spectral character.** Welch's method on the full mono mixdown
yields a power spectral density. We measure the –10 dB band and
identify the peak frequency. This tells us where the energy is
and where the engine should aim.

**Temporal statistics.** Onset detection in the bird-band
(high-pass filtered above 1.5 kHz) yields ~180 events across
the 9-minute recording. We compute the inter-call gap
distribution and fit a log-normal — the parametric family that
matches the observed shape. This tells us how to space synthetic
events.

**Drift / non-stationarity.** Two parallel measures of how the
soundscape changes over time: (a) bin onsets into 10s windows
to track call rate, (b) spectral centroid over the full duration
to track frequency character. The relative coefficients of
variation tell us *what* drifts and *what doesn't*.

**Engine comparison.** A faithful Python port of the
JavaScript audio engine in `index.html` synthesises 5 minutes
of audio with the same drift sines, voice types, and gap formula.
We run the same analyses on the synthetic and produce side-by-side
plots showing where it falls short.

## Caveats

- **Single recording.** A second pass on `dawn chorus.wav`
  (squashy555 #341675) and the Peak District set would tell us
  whether these parameters are characteristic of UK temperate
  dawn chorus or specific to one location/morning.
- **Onset detection is approximate.** Detection threshold tuned
  loose enough to find dense, overlapping events; some false
  positives, some missed quiet events. Distributions are robust
  to this; absolute call rates less so.
- **Downsampled.** Source is 44.1 kHz; analysis is at 22.05 kHz
  (memory-constrained). Bird-band content (≤ 8 kHz) is preserved
  faithfully.
- **No psychoacoustic validation.** "Closer to real" ≠ "more
  calming." Worth A/B-testing the tuned engine against the
  original before committing.
