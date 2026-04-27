# Sentinels

> *"A quiet park feels different from a quiet office because the parks have sentinels."*

A small, open exploration of a single hypothesis: a wearable device emitting carefully calibrated ambient-safety cues — birdsong-band soundscapes at the volume of quiet conversation — could quiet the brainstem circuitry that runs hypervigilance in the background of urban life.

This repository contains the vision, the supporting research with full citations, technical designs for a proof-of-concept device, and the experiment methodology to actually test whether the thing does anything.

---

## The hypothesis

Mammals appear to use continuous ambient soundscape as a proxy for "no large predator currently moving through the environment." Birdsong, in roughly the 1–8 kHz band at low volume, is a canonical signal that this monitoring system was tuned on. Recent studies (Stobbe et al. 2022; Hammoud et al. 2022) provide reasonable evidence that even *recorded* birdsong produces measurable reductions in anxiety and improvements in mood, with effects persisting for hours after the sound stops. EEG work (Yu et al. 2025) indicates the response is volume-sensitive: alpha activity rises at 45–50 dB(A) and the response inverts above ~60 dB(A).

A small wearable could provide this signal continuously and unobtrusively in environments where real birds are absent — offices, public transit, hospitals, dense urban interiors.

## The bet

What separates a toy from something that might actually work:

- **Real soundscapes are stochastic on multiple timescales.** Looped recordings habituate fast. The brainstem is doing *continuity detection*, not pattern recognition; what it wants is a believable, slowly-drifting natural soundscape, not a 30-minute loop on repeat.
- **Volume is a hard constraint.** Above ~60 dB(A) the response inverts. The device must dynamically attenuate against ambient noise — quieter in a library, louder outdoors, never above the safe envelope.
- **Heard but not foregrounded.** Present in the soundscape the way a fridge hum is — available to be ignored. Not music. Not a podcast. Not asking for attention.

## What's here

- [`docs/research.md`](docs/research.md) — supporting academic sources, with caveats on what each one actually shows
- [`docs/hardware.md`](docs/hardware.md) — prototype hardware design, BOM, form-factor exploration
- [`docs/firmware.md`](docs/firmware.md) — procedural audio architecture (the technical bet, expanded)
- [`docs/experiments.md`](docs/experiments.md) — n=1 self-experiment protocol and pilot study design
- [`index.html`](index.html) — landing page (also served at https://christopherdebeer.github.io/sentinels)

## Status

Early. Speculative. The primary deliverable in the current state of this project is **a falsifiable hypothesis and a clear plan to test it**. No claims about efficacy should be inferred from the existence of this repository.

## Honest disclaimers

1. The "200-million-year-old predator-detection circuit" framing that may circulate alongside this idea is *narrative*, not established neuroscience. The behavioural and EEG effects of birdsong on stress markers are real and replicated; the specific evolutionary-neuroethological story is plausible but not tested.
2. Wellness-coded interventions are notoriously susceptible to placebo, novelty, and reporting-bias effects. Any honest experimental design here has to take that seriously, and the methodology in `docs/experiments.md` does.
3. This is a personal-research project, not a medical device. Not intended to treat, diagnose, or cure anything.

## License

Code: MIT. Written materials: CC BY 4.0. See [LICENSE](LICENSE).
