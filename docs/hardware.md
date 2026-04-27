# Hardware

A proof-of-concept device that can plausibly emit calibrated ambient-safety soundscapes can be built for under $30 in components, in a few weekends, with parts that will arrive in a Tuesday-morning post.

This document covers form-factor trade-offs, the recommended PoC build, the bill of materials, and the acoustic constraints the design has to respect.

## Form factor: three options

### A. Pendant / lapel projector (recommended for PoC)

A small, brooch-sized device worn at the chest or hung from a lanyard, with the speaker firing outward into the local soundscape.

- ✅ **Acoustically honest.** The sound has a place in the world, not in your head. This matters: the brainstem effect we're after is "the environment is safe", not "I am being told the environment is safe through earbuds."
- ✅ **Shareable presence.** Two people in a room benefit from one device.
- ✅ **No occlusion.** Doesn't interfere with conversation, situational awareness, or other audio.
- ❌ **Bleed.** In a quiet office, colleagues will hear it. May be a feature; may be a bug.
- ❌ **SPL at the ear is uncontrolled.** A device set to 50 dB(A) at the chest is much louder at the ear when you lean down to read.

This is the most interesting design and the one the project is built around.

### B. Open-ear earbud / bone conduction

A pair of earbuds running in transparent / open mode, or temple-mounted bone-conduction transducers.

- ✅ **SPL at the ear is exactly controllable.** Easy to hold the calibrated 45–55 dB(A) envelope.
- ✅ **Real binaural spatialisation** is possible — birds left, right, near, far.
- ❌ **Sound is "in your head"**, which may undercut the felt-sense of "the environment is safe."
- ❌ **Wearer-only.** No shared presence.
- ❌ **Battery and weight are tighter constraints.**

### C. Desktop / room emitter

A small puck on a desk that does the same job as the pendant but stationary.

- ✅ **No power budget concerns.** Wall power is cheap.
- ✅ **Better drivers possible** — full-range or even small two-way.
- ❌ **Not wearable**, and only useful where you place it. The original brief was *small wearable*.

A future product family probably wants all three. The pendant is the most informative first build.

## Recommended PoC architecture

```
                ┌──────────────────────────────────────────┐
                │             Pendant Enclosure             │
                │                                            │
   Light ─────► │ ┌──────────────┐    ┌──────────────────┐  │
   sensor       │ │              │    │                  │  │
                │ │   ESP32-S3   │ ◄─►│   I²S DAC        │ ─┼─► Driver
   IMU   ─────► │ │   (PSRAM)    │    │   MAX98357A      │  │   (28mm)
   (LIS3DH)     │ │              │    │   or PCM5102     │  │
                │ │              │    └──────────────────┘  │
   MEMS  ─────► │ │              │                          │
   mic          │ │              │ ◄── BLE ─────────────────┼─► Phone app
   (INMP441)    │ └──────┬───────┘                          │   (config + telemetry)
                │        │                                  │
                │   3.7V LiPo, 200–400 mAh                  │
                │   USB-C charging (TP4056 or built-in)     │
                └────────────────────────────────────────────┘
```

## Bill of materials (PoC, single unit)

| Component | Part | Approx. cost (GBP) |
|---|---|---|
| MCU + audio + Wi-Fi/BLE | ESP32-S3-WROOM-1 (with 8MB PSRAM) | £4–6 |
| I²S DAC + amp | MAX98357A breakout (3.2W class-D) | £2–3 |
| Speaker driver | 28mm 4Ω 2W full-range, mylar cone | £2–4 |
| MEMS microphone | INMP441 I²S | £2–3 |
| Accelerometer (optional, "is being worn") | LIS3DH I²C | £1–2 |
| Light sensor (optional, circadian behaviour) | VEML7700 I²C | £1–2 |
| Battery | 3.7V 300 mAh LiPo, JST connector | £3–4 |
| Charging IC + USB-C | TP4056 module with USB-C | £1–2 |
| Soft/rigid PCB | OSHPark or JLCPCB, 5x quantity | £8–12 amortised to £2–3 each |
| Enclosure | 3D-printed PETG or resin | ~£1 in filament |
| Lanyard / clip | Off-the-shelf | £1–2 |
| **Total per unit** | | **~£20–30** |

## Acoustic constraints the design has to respect

These are not soft suggestions. They are the difference between a device that does what we hope and a device that increases stress while looking like it doesn't.

### 1. SPL envelope

Target effective SPL at the listener's ear: **45–55 dB(A)**. Hard cap: **60 dB(A)**. Floor: **40 dB(A)** (below this, ambient noise wins and the signal is meaningless).

For a pendant at ~30cm from the ear, with typical small-driver efficiency, this corresponds roughly to driver-output of ~50–65 dB(A) SPL at 10cm. Specific tuning will need to be measured per build.

### 2. Frequency band

Energy concentrated in **1,000–8,000 Hz**. Below ~700 Hz, small drivers can't reproduce content cleanly anyway. Above ~10 kHz, there's no payload — bird vocalisation falls off. A high-pass at 800 Hz protects the driver from low-frequency content it can't produce, and the system from wasting amplifier headroom.

### 3. Ambient adaptation

The MEMS mic is **not optional**. The device must:

- Continuously estimate ambient noise floor (e.g., A-weighted SPL averaged over 30s windows).
- When ambient rises, the device must *attenuate* (not boost) — it's a quiet signal that loses meaning when shouted over.
- When ambient is too loud (~> 65 dB(A) sustained), the device should pause output entirely. A signal heard over noise is not the signal we want.
- When ambient drops (e.g. you walk into a library), the device drops with it, holding a roughly constant SNR.

### 4. The 60 dB(A) interlock

This is a hard interlock, not a guideline. If output combined with ambient ever exceeds 60 dB(A) at the estimated ear position, the device clips itself. Yu et al. (2025) is the only study that's directly tested this volume range, but the inversion above 60 dB(A) is consistent with the broader stress/noise literature, and getting this wrong is the difference between the device helping and the device adding to the problem.

## Optional but valuable features

### Wear detection (LIS3DH)

If the device is sat on a desk, it should sleep. A simple movement-tap heuristic plus orientation sensing handles this. Saves significant battery.

### Circadian behaviour (VEML7700)

Real soundscapes have a daily structure: dawn chorus is louder and more diverse, midday is quieter, dusk has its own pattern, night is mostly silent. A device that ignores the time of day will feel synthetic. A device that respects it will feel uncannily right. Light sensor + RTC in the ESP32 give us this for ~£2.

### Bird-aware mode (the cherry on top)

The MEMS mic, already required for ambient calibration, can also do simple onset detection in the 1–8 kHz band. When real birds sing nearby, the device's procedural birds briefly defer — fewer calls, longer gaps. This would feel uncannily right and, as a side effect, neatly avoids the recursive embarrassment of two of these devices serenading each other on a park bench.

This is firmware, not hardware, but the hardware has to support it. The recommended INMP441 MEMS mic does.

## What's deliberately not in the PoC

- **Custom DSP chip.** ESP32-S3 has enough horsepower to do procedural audio synthesis, light onset detection, and BLE concurrently with PSRAM headroom. A custom DSP belongs in a v2 if/when the concept is validated.
- **Multiple drivers / stereo / spatial audio.** Pendant form factor doesn't benefit; cost doubles. Save it for the open-ear variant.
- **Companion app polish.** A simple BLE config and telemetry interface is enough for PoC. App design is a v2 concern.
- **Custom enclosure tooling.** 3D-printed in PETG is fine for the first 5–20 units. Injection moulding or aluminium milling is a v2 concern.

## Open questions

- Does the pendant form factor's "sound in the world" advantage actually matter, or does the open-ear variant — with controllable SPL and binaural spatialisation — produce a stronger effect? This is an experimentally answerable question and is part of the methodology in [`experiments.md`](experiments.md).
- How much does driver quality matter at 50 dB(A)? At quiet volumes, distortion may matter more than absolute frequency response. A worthwhile experiment.
- Is bone conduction better than air conduction for this application? Bone conduction is novel and slightly uncanny; if the brainstem reads it as an intra-skull event rather than an environmental one, the effect may not transfer.
