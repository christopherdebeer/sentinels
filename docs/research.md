# Research

This document collects the academic literature that supports — or constrains — the project hypothesis, and tries to be honest about what each paper actually shows versus what the idea wants it to show.

## Summary of evidence

| Claim | Strength | Primary sources |
|---|---|---|
| Recorded birdsong reduces state anxiety in healthy adults | Moderate (medium effect size, single online RCT) | Stobbe et al. 2022 |
| Encountering birds in everyday life improves mental wellbeing for hours afterward, including in those diagnosed with depression | Moderate (large EMA study, observational) | Hammoud et al. 2022 |
| Birdsong's restorative effect on EEG alpha activity is volume-dependent and inverts above ~60 dB(A) | Suggestive (small EEG study, n=30) | Yu et al. 2025 |
| Natural soundscapes accelerate stress recovery via autonomic mechanisms (HRV, skin conductance) | Established but heterogeneous | Alvarsson et al. 2010; Annerstedt et al. 2013; multiple reviews |
| The mechanism is specifically a "predator-detection circuit" 200M years old | **Speculative narrative.** Not directly tested. | (no direct source) |

## Primary studies

### Stobbe, E., Sundermann, J., Ascone, L., & Kühn, S. (2022)

**Birdsongs alleviate anxiety and paranoia in healthy participants.**
*Scientific Reports*, 12, 16414.
DOI: [10.1038/s41598-022-20841-0](https://doi.org/10.1038/s41598-022-20841-0)

Randomised online experiment with N=295. Four conditions for 6 minutes: traffic noise (low/high diversity) and birdsong (low/high diversity). Outcomes assessed pre/post.

**What it actually shows:**
- Birdsong (regardless of diversity) significantly reduced state anxiety and paranoia, with **medium effect sizes**.
- Only *high-diversity* birdsong showed a small effect on depressive states.
- Traffic noise increased depressive states (small effect size for low-diversity, medium for high-diversity).
- No effects on cognitive task performance (digit-span, dual n-back).

**Caveats:**
- Online experiment, participants self-reported and self-administered. No physiological measures.
- Single 6-minute exposure; chronic-exposure effects not measured.
- Participants were instructed to set volume to 80% — the *absolute* SPL at the ear was not controlled.
- Authors' explanation for the effect is cautious: birdsong as "a subtle indication of an intact natural environment, detracting attention from stressors that could otherwise signal an acute threat." They do not claim a specific predator-detection circuit.

### Hammoud, R., Tognin, S., Burgess, L., et al. (2022)

**Smartphone-based ecological momentary assessment reveals mental health benefits of birdlife.**
*Scientific Reports*, 12, 17589.
DOI: [10.1038/s41598-022-20207-6](https://doi.org/10.1038/s41598-022-20207-6)

Ecological momentary assessment via the Urban Mind app. 1,292 participants completed 26,856 assessments between April 2018 and October 2021.

**What it actually shows:**
- Real-world encounters with birds (seen or heard) were associated with statistically significant improvements in self-reported mental wellbeing.
- The effect persisted in subsequent assessments — interpreted as lasting up to ~8 hours.
- The association was present in both healthy participants and those with a diagnosis of depression.
- Effects were not explained by co-occurring environmental factors (trees, water, plants) when adjusted for.

**Caveats:**
- **Observational, not experimental.** People who notice birds may already be in better moods, or in environments that are more restorative for other reasons. The authors adjust for several confounders but cannot fully eliminate selection effects.
- Self-report only.
- Sample is voluntary participants who downloaded a wellbeing app — likely skewed toward people already interested in nature/wellbeing.
- "Up to 8 hours" is a maximum from time-lagged regression, not the average duration of effect.

### Yu, et al. (2025)

**Brain activity and restorative effects of birdsong at different sound pressure levels: An electroencephalographic study.**
*Applied Acoustics*.
DOI: [10.1016/j.apacoust.2025](https://www.sciencedirect.com/science/article/abs/pii/S0003682X25006279)

EEG study with 30 participants exposed to birdsong at 40, 45, 50, 55, and 60 dB(A).

**What it actually shows:**
- Subjective Perceived Restorativeness Scale scores peaked at 45 dB(A).
- Alpha wave activity at 45–50 dB(A) was 14.1% higher than the 40 dB(A) (silent) condition.
- At 60 dB(A), EEG-derived "mental stress" was 29% higher.
- P300 component most strongly activated in the 40–50 dB(A) range.

**Caveats:**
- Small sample (n=30).
- Single laboratory session per participant; no measurement of habituation or chronic exposure.
- Specific numbers (14.1%, 29%) are point estimates from this single study and should not be treated as established constants.

This study is the strongest direct evidence for the **volume window** that the device must respect, but its specific quantitative claims should be replicated before being relied upon for design decisions.

## Supporting / contextual literature

### Alvarsson, J. J., Wiens, S., & Nilsson, M. E. (2010)

**Stress recovery during exposure to nature sound and environmental noise.**
*International Journal of Environmental Research and Public Health*, 7(3), 1036–1046.
DOI: [10.3390/ijerph7031036](https://doi.org/10.3390/ijerph7031036)

Skin conductance recovery from a stressor was faster during exposure to nature sounds (including bird calls and a fountain) than during noise. Foundational study for the autonomic-recovery story.

### Sudimac, S., Sale, V., & Kühn, S. (2022)

**How nature nurtures: Amygdala activity decreases as the result of a one-hour walk in nature.**
*Molecular Psychiatry*.
DOI: [10.1038/s41380-022-01720-6](https://doi.org/10.1038/s41380-022-01720-6)

fMRI evidence that one hour in nature reduces amygdala activity, while one hour in an urban environment does not. From the same group as Stobbe et al. — relevant context for what's actually happening in the threat-monitoring circuit.

### Bratman, G. N., et al. (2015)

**Nature experience reduces rumination and subgenual prefrontal cortex activation.**
*PNAS*, 112(28), 8567–8572.
DOI: [10.1073/pnas.1510459112](https://doi.org/10.1073/pnas.1510459112)

A 90-minute walk in nature reduced rumination and reduced activity in the subgenual prefrontal cortex — a region implicated in self-focused negative thought. The neural-correlate side of the broader nature-exposure literature.

### Buxton, R. T., et al. (2021)

**A synthesis of health benefits of natural sounds and their distribution in national parks.**
*PNAS*, 118(14), e2013097118.
DOI: [10.1073/pnas.2013097118](https://doi.org/10.1073/pnas.2013097118)

Meta-analysis: water sounds had the largest effect on positive affect and reduced stress; bird sounds had the largest effect on reducing stress and annoyance. Effect sizes are small to moderate but consistent across the literature.

## What is *not* established

It is worth being explicit about the parts of the popular framing that are **not** supported by the literature cited above:

1. **A specific 200-million-year-old "predator detection" circuit that monitors birdsong continuity.** No paper directly tests this. The closest the literature gets is the Stress Recovery Theory (Ulrich, 1983) and the Biophilia Hypothesis (Wilson, 1984), both of which propose evolutionary explanations but do not isolate a specific neural circuit responsive to birdsong cessation.
2. **That the cessation of birdsong (as opposed to its presence) is the active signal.** This is intuitive but, to my knowledge, untested.
3. **That synthetic/looped birdsong delivered through a small earbud-class speaker would replicate the effects observed in the listed studies.** Stobbe et al. used 6-minute curated soundscapes through headphones at 80% device volume; Hammoud et al. measured real birds in real environments. The leap from "recorded birdsong reduces anxiety in a 6-minute lab session" to "a wearable emitting procedural soundscapes reduces anxiety chronically in daily life" is significant and is the leap this project exists to test.

Stating the gap clearly is the project's most important honesty.

## How this informs the design

- **Frequency band:** target the 1,000–8,000 Hz range where most temperate-zone bird vocalisation sits.
- **Volume envelope:** keep effective SPL at the ear in the 45–55 dB(A) window. Hard cap at 60 dB(A). Mic-based ambient calibration is non-negotiable for a usable wearable.
- **Diversity:** Stobbe et al. found anxiety reduction at both low and high diversity; only high diversity affected depression. Diversity is cheap to provide procedurally — bias toward high.
- **Continuity, not loops:** see [`firmware.md`](firmware.md). Habituation to predictable patterns is the failure mode this project most worries about.
- **Realistic gap structure:** real soundscapes have silences. Constant chirping for 8 hours is unnatural and likely counterproductive.
