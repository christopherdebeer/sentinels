# Tuning report

> Programmatic analysis of *"Dawn Chorus Birdsong"* by squashy555
> ([Freesound #573080](https://freesound.org/people/squashy555/sounds/573080/),
> CC0, recorded Burton-on-Trent UK, May 2021), compared to the
> Sentinels procedural audio engine. Source: `analyse.py`, full
> numerical results in `results.json`, figures in `figures/`.

## Headline findings

The engine's overall *frame* — bird-band synthesis with sweep / trill / pip / warble voices, heavy-tailed gap timing, slow drift — is structurally correct. The numerical specifics are wrong in five distinct ways, listed below in approximate order of audible impact.

### 1. Pure-tone synthesis lacks harmonics — biggest gap

Real bird calls have rich harmonic content. A song thrush note at 2 kHz fundamental has visible energy at 4 kHz, 6 kHz, sometimes 8 kHz. The engine's sine-wave oscillators produce only the fundamental, which is why the comparison spectrogram (`comparison.png`, bottom-right) shows real birdsong reaching 9 kHz while the engine's content stops at 5 kHz.

**Why this matters most:** the brain isn't doing isolated frequency detection — it's doing *spectral pattern* recognition. A real call's harmonic ladder is part of what makes it readable as "bird" rather than "tone." Pure sines are the single biggest reason the engine sounds synthetic.

**Recommended fix:** replace `OscillatorNode` with a small bank of summed oscillators producing a harmonic series. For each voice, generate the fundamental at full amplitude, the 2nd harmonic at -8 dB, the 3rd at -14 dB, the 4th at -20 dB. This is cheap (4× the oscillator count, still well within ESP32 / Web Audio budget) and qualitatively transformative. Alternative: use `WaveShaperNode` with a soft-saturation curve to add harmonics passively — fewer nodes, slightly less control.

### 2. Frequency centre is biased ~660 Hz too low

The recording's spectral peak is at **4258 Hz**. The engine's frequency centre drifts between 2400–4800 Hz with a *mean* of 3600 Hz — biased systematically below the natural peak.

**Recommended fix:** centre the engine's frequency band around 4200 Hz, with smaller drift range. New parameters:

| | Current | Recommended |
|---|---|---|
| Centre frequency | 2400–4800 Hz | 3800–4600 Hz |
| Mean centre | 3600 Hz | 4200 Hz |

### 3. Spectral character is **not** what drifts; density is

The recording's spectral centroid is remarkably stable: coefficient of variation 0.024 across nearly 9 minutes. The engine drifts the frequency centre over a ±28% range — an order of magnitude more variation than real soundscapes show.

Conversely, the recording's *density* is highly variable: 6 to 42 calls/min within minute-scale windows, with a coefficient of variation of 0.51. The engine's density drift is much more sedate, modulated by a slow sinusoid.

**Recommended fix:** invert the priorities. Reduce frequency drift to ±5% around centre. Increase density variability through a faster, less periodic mechanism. Two suggestions:

- **Density modulator: pink-noise envelope on top of the slow sine.** Pink noise gives natural-feeling fluctuation at multiple timescales — slower than white noise (avoids twitchy density changes) but faster than the current single sine. Implementation: precompute a 30-min pink-noise sequence sampled at 1 Hz, normalise to ±0.4, multiply onto density.
- **Burst behaviour:** real chorus has 10–30 second "bursts" of higher density (a single bird triggering responses, then settling). Add an occasional stochastic density spike: every 30–90 seconds, 50% chance of a 2× density multiplier for 8–20 seconds.

### 4. Inter-call gap distribution is the right shape, wrong scale

The recording's gaps follow a clean log-normal: μ=0.67, σ=0.98 in log-space, equivalent to a mean of ~3.0s, median 2.35s, with a long tail to 17.9s. The engine's ad-hoc formula (`base_gap * (0.3 + u^2.5 * 2.5)`) produces a heavy-tailed distribution but at mean ~1.7s — too fast.

**Recommended fix:** replace the formula with proper log-normal sampling parameterised by the density slider:

```javascript
// At slider value 0.5 (mid-density), match the observed real-world parameters
function sampleGap(densitySliderValue) {
  // Density slider 0..1 maps to lognormal mu shift
  // Higher density = lower mu = shorter gaps
  const mu = 0.67 - (densitySliderValue - 0.5) * 1.4; // ranges ~1.4 down to 0
  const sigma = 0.98;
  // Box-Muller for normal sample, then exp for lognormal
  const u1 = Math.random(), u2 = Math.random();
  const z = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
  return Math.exp(mu + sigma * z);
}
```

This gives the engine the right *shape* (log-normal heavy tail with characteristic short-gap concentration) while keeping the user's density slider in control.

### 5. Missing low-frequency continuous bed

The recording has a continuous low-amplitude band of energy at 1500–2500 Hz throughout — distant chorus, ambient, or both. It's never silent. The engine's silences between calls are absolute silences, which makes the synthetic chorus feel "punctuated" rather than embedded in an environment.

**Recommended fix:** add a quiet pink-noise bed band-passed to 1.5–3 kHz, gain set to roughly -45 dB below the loudest synthesised call. Cheap to implement (one filtered noise node), and the brain reads continuous low-level chorus content as "we are in a place full of birds" rather than "we are in a quiet room with occasional bird sounds." This is a perceptually significant change.

The recording also has discrete sustained tones at 800–1000 Hz (song thrush phrasing), but reproducing these properly would require a fifth voice type. Lower priority — the bed addition is more important.

## Numerical summary

| Metric | Real recording | Engine (current) | Engine (recommended) |
|---|---|---|---|
| Call rate (mean) | 20.0 / min | 35.4 / min | 20 / min at slider 0.5 |
| Inter-call gap mean | 3.00 s | 1.69 s | ~3.0 s at slider 0.5 |
| Gap distribution | log-normal μ=0.67 σ=0.98 | ad-hoc heavy-tail | log-normal as fitted |
| Frequency peak | 4258 Hz | ~3600 Hz | 4200 Hz |
| Frequency drift CV | 0.024 | 0.28 | ~0.05 |
| Density CV | 0.51 | ~0.10 (slow drift only) | ~0.40 (pink + bursts) |
| Harmonic content | rich, to ~9 kHz | none (pure sines) | 4-partial bank |
| Continuous bed | -45 to -50 dB | none | -45 dB pink, 1.5–3 kHz |

## What this analysis does *not* show

A few caveats on scope:

- **Single recording.** Generalising from one 9-minute recording is the obvious limitation. A second analysis pass on `dawn chorus.wav` (squashy555 #341675) and the Peak District set would tell us whether these parameters are *characteristic* of UK temperate dawn chorus or specific to Burton-on-Trent in spring 2021. Recommended as a follow-up before committing the engine parameters.
- **Onset detection is approximate.** With a delta of 0.07 and dense overlapping content, the 177 detected onsets include some false positives and miss some quiet events. The *distribution* of inter-call gaps is robust to these errors; the absolute call rate is less so.
- **No psychoacoustic validation.** "More realistic spectrum" is not the same as "more calming" — it's possible (though unlikely) that the engine's slightly-synthetic character is part of why it sounds quietly composed rather than chaotic. Worth A/B-testing the original engine against the tuned version before committing.
- **The recording is downsampled to 22.05 kHz** for analysis (memory constraints). The original is 44.1 kHz. Content above 11 kHz, if any, isn't measured here. For the bird-band domain we care about, this is fine.

## What I'd change first, second, third

If I had to rank the changes by audible impact for least implementation effort:

1. **Add harmonics** (15 minutes of code; transformative). This is the change that makes the engine stop sounding like a synth and start sounding like birds.
2. **Add the continuous low-frequency bed** (15 minutes; significant impact). Changes the *spatial* feel of the soundscape.
3. **Replace the gap formula with proper log-normal sampling** (10 minutes; medium impact). Audible but subtle.
4. **Re-centre the frequency band on 4200 Hz** (5 minutes; small but free). Cheap correction.
5. **Density modulator with pink noise + burst events** (30 minutes; medium impact, hardest to get right). Worth doing but worth A/B testing — real chorus density variability may not be what we *want* on a desk for sustained background.

Items 1–4 are unambiguous improvements. Item 5 introduces variability that could either feel more natural (good) or be more attention-grabbing (bad for the project's intent — the device should be *available to be ignored*). Worth implementing behind a "naturalistic" toggle and testing both versions.
