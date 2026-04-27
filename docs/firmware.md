# Firmware & Procedural Audio

The hardware is straightforward. The interesting engineering happens here.

The single most important technical bet of this project: **don't loop a recording**. The brainstem mechanism we're trying to engage is doing continuity detection over noisy biological signals, and mammals habituate fast to predictable patterns. A 30-minute high-fidelity field recording on loop will probably underperform a procedurally-assembled soundscape made from short stems played with stochastic timing, slow scene drift, and respect for the time of day.

This document describes the procedural audio architecture, the stem library, and the runtime decisions the firmware has to make.

## Architectural overview

```
   ┌──────────────────────────────────────────────────────────────┐
   │                      Soundscape Engine                       │
   │                                                              │
   │  ┌────────────┐    ┌─────────────┐    ┌──────────────────┐   │
   │  │            │    │             │    │                  │   │
   │  │  Scene     │ ─► │  Voice      │ ─► │  Mixer +         │   │
   │  │  Director  │    │  Allocator  │    │  Spatializer     │   │
   │  │            │    │             │    │  (mono PoC)      │   │
   │  └─────┬──────┘    └──────┬──────┘    └────────┬─────────┘   │
   │        ▲                  ▲                    │             │
   │        │                  │                    ▼             │
   │  ┌─────┴──────┐    ┌──────┴──────┐    ┌──────────────────┐   │
   │  │  Time-of-  │    │  Stem       │    │  Output limiter  │   │
   │  │  day model │    │  library    │    │  (60 dB(A) cap)  │   │
   │  └────────────┘    │  (PSRAM)    │    └────────┬─────────┘   │
   │                    └─────────────┘             │             │
   │                                                ▼             │
   └──────────────────────────────────────────I²S DAC─────────────┘
                                                    │
   ┌────────────────────────────────────────────────┴─────────────┐
   │                      Sensor Fusion                            │
   │  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌─────────┐  │
   │  │ MEMS mic │ ─► │ Ambient  │    │ Light    │    │ IMU /   │  │
   │  │ (1–8 kHz │    │ SPL est. │    │ sensor   │    │ wear    │  │
   │  │ onset    │    │ (RMS,    │    │ (lux,    │    │ detect  │  │
   │  │ detect)  │    │ A-weight)│    │ circ.)   │    │         │  │
   │  └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬────┘  │
   │       │               │               │               │       │
   │       └───────────────┴───────┬───────┴───────────────┘       │
   │                               ▼                               │
   │                    State (sleep / active /                    │
   │                       attenuated / paused)                    │
   └───────────────────────────────────────────────────────────────┘
```

## The stem library

A modest library of short audio fragments stored in PSRAM:

- **30–80 distinct bird calls**, each 0.3–3 seconds, sampled at 22.05 kHz mono. Curated to span the 1–8 kHz band; multiple species; both song fragments and call fragments. ~5–10 MB total uncompressed; fits comfortably in 8MB PSRAM with headroom.
- **A small number of textural beds** — distant low-density chorus, light foliage rustle — for occasional layering. Optional.

Source candidates: Xeno-canto (large open-licensed bird vocalisation library, mostly CC), Macaulay Library (selectively licensed), and any field recording the project commissions or makes itself. Licensing has to be respected; the repository will not redistribute samples without compatible licenses.

## The Scene Director

A small state machine that decides, every few seconds, what the current "scene" should be. State variables:

- **Time of day** (from RTC + light sensor cross-check)
- **Estimated ambient SPL and acoustic activity** (from mic)
- **Energy budget** (from battery state)
- **User preference** (config: "more active" / "calmer", maybe a "scene" choice like "moorland" / "garden" / "forest")

The Director outputs a small set of parameters consumed by the Voice Allocator:

- `target_call_rate` — average calls per minute
- `gap_distribution_params` — parameters for inter-call gap timing (shape and scale of an inverse-Gaussian, say)
- `species_weights` — bias over the stem library
- `density_target` — how many simultaneous voices are permissible
- `scene_drift_rate` — how fast the above values are allowed to change (slow — minutes, not seconds)

A scene is not a recording. It's a *distribution* the Voice Allocator samples from.

## The Voice Allocator

Per-tick, decides whether to trigger a new call, and if so which stem and at what gain/pitch. Maintains 1–4 concurrent voices, each with envelope (attack, decay) and optional pitch-shift (small — ±100 cents max — to add variety without making birds sound wrong).

Gap timing matters more than people expect. Real bird soundscapes have heavy-tailed inter-call distributions: lots of short gaps, occasional long quiet stretches. A Poisson process with a fixed rate produces an audibly artificial cadence. An inverse-Gaussian or log-normal gap distribution feels much more right.

## The Mixer + Limiter

Mixes active voices, applies a final gain trim derived from ambient-SPL estimation, and runs a hard limiter that enforces the 60 dB(A) interlock. The limiter's *job* is to never be hit. If it's clipping, something upstream is wrong.

A-weighting requires actual SPL calibration of the driver — done once per build, stored as a coefficient. This is how the device knows that "DAC output of value X" corresponds to "approximately Y dB(A) at 30 cm."

## Bird-aware mode (optional, charming)

The MEMS mic, already running for ambient SPL estimation, can additionally do simple onset detection in the 1–8 kHz band. A short STFT, look for transients with the right band energy, and the device knows roughly when real birds are singing nearby.

When this signal is high, the Scene Director:
- reduces `target_call_rate` (deferring to the real birds)
- reduces `density_target`
- reduces overall output gain by a few dB

The effect, if it works, should be nearly invisible to the wearer in most environments and uncannily right in the few moments when real birds appear. It also defuses the recursive case where two devices encounter each other.

False positives are mostly fine — the device under-singing for a few seconds is harmless. False negatives (continuing to sing over real birds) are also mostly harmless. So the detector can be cheap.

## Power management

Three states:

| State | Trigger | Power |
|---|---|---|
| **Sleep** | IMU reports stationary > 5 min, or low-light + IMU stationary | <1 mA — RTC and IMU only |
| **Active** | Wear detected, daytime / user-configured hours | ~30–60 mA depending on call density |
| **Paused** | Ambient SPL too high (>65 dB(A) sustained) | ~5 mA — sensors only |

A 300 mAh LiPo running ~50 mA for ~6 active hours and sleeping the rest of the day gives a reasonable single-day battery target with charging via USB-C overnight.

## Configuration interface (BLE)

Bare minimum for the PoC:

- Set scene preference
- Set "active hours" (e.g. 09:00–19:00)
- Volume offset (-6 dB to 0 dB; the absolute envelope is enforced by firmware regardless)
- Firmware update (OTA)
- Telemetry pull: device uptime, battery level, recent ambient SPL distribution, recent call counts

A web app (no native install required) using Web Bluetooth is sufficient for v1. The phone is only needed for occasional configuration and for OTA updates.

## What the firmware deliberately does *not* do

- **No streaming.** No cloud dependency. The device works in airplane mode. This is partly philosophical (a hypervigilance-quieting device that depends on a cloud service is missing the point) and partly practical (latency, battery, privacy).
- **No microphone audio leaving the device.** The mic is used for SPL estimation and onset detection, both of which produce small numerical features. No raw audio is ever transmitted, logged, or stored.
- **No ML models.** The whole system can be implemented with simple DSP and basic statistics. ML would be overkill at this scale and would make the device much harder to reason about.

## Implementation notes

- **Audio framework:** ESP-IDF has solid I²S support; ESP-ADF is the next step up if needed but probably not for PoC.
- **Stem playback:** decode-on-demand from PSRAM; no codec needed if stored as 16-bit PCM. ADPCM compression halves storage at the cost of negligible quality at this bit depth.
- **Mixing:** trivial at 1–4 voices, mono. Sum to 24-bit accumulator, dither to 16-bit, hand to I²S.
- **Scheduling:** FreeRTOS tasks — high-priority audio task fed from a stem-decoding task, low-priority director and sensor tasks.

## Open questions

- How small can the stem library be before the soundscape feels repetitive? My intuition: ~50 distinct stems with stochastic timing and small pitch variation should be indistinguishable from "real" within a 2-hour session. This is testable.
- Is pitch-shifting a single high-quality recording of one species more or less effective than a smaller library of literal recordings of multiple species? Open question, possibly a fun ablation.
- Does adding a textural bed (low-level continuous foliage rustle) help, hurt, or do nothing? This is a feature that could backfire — Stobbe et al. used clean curated soundscapes; we don't know how a more naturalistic mix would compare.

Each of these is a clean A/B for the experimental protocol in [`experiments.md`](experiments.md).
