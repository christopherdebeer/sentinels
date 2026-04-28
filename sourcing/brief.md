# Sourcing brief for Alibaba sourcing agent

> Drop the contents below into the Alibaba sourcing agent. It is written
> as direct instructions to that agent, with all the constraints it needs
> to filter usefully and the questions it should put to suppliers on our
> behalf.

---

## Role and goal

You are sourcing a small audio-playback device for a research pilot, **not** a consumer product launch. Treat this as a B2B buyer brief, not a retail one. We are looking for an existing OEM/ODM product (or a closely-adaptable one) that can be branded and used as a research instrument. We are **not** looking to develop new hardware.

Find me a shortlist of **3–5 candidate products** from **3–5 different suppliers** that genuinely fit the spec below. For each, run an enquiry with the supplier covering the questions in the "Supplier questions" section and report back with their answers, MOQ, unit price at our target volumes, lead time, and an honest assessment of how close the product is to the spec without modification.

Do not give me a long list of weak matches. I would rather have three strong candidates than fifteen marginal ones. If nothing fits well, say so plainly — I would rather know early.

## What the device is for

A small desktop speaker that sits on an office desk, plays a looped recording of birdsong continuously during working hours at a deliberately quiet volume, and carries printed project branding and a QR code linking to a participant survey. Each unit will be given (not sold) to a participant in a research study on workplace ambient soundscapes and stress. Estimated initial run: **50–200 units**. If the pilot is successful, a follow-on order in the **500–2,000 unit** range is plausible but not committed.

The device is the research instrument. We do not need it to be exciting, premium-feeling, or feature-rich. We need it to do one thing reliably and quietly.

## Hard requirements (must-haves)

1. **Loop playback from on-device storage** — SD/TF card or internal flash — playing MP3 or WAV. Bluetooth-only devices are not suitable; we need the audio to play without requiring a phone connection so participants don't have to think about it.
2. **Auto-resume on power-up** — when the device is switched on or plugged in, it should automatically begin playing the loaded loop. No menu navigation, no app pairing, no "press play" step. Critical for compliance — every additional friction step lowers the rate at which the device is actually used.
3. **Quiet maximum volume** — the device's *maximum* output should be conversationally quiet. We are explicitly looking for products with a low ceiling (think baby-sleep / white-noise / sleep-therapy category, not Bluetooth party speakers). A device that can hit 90 dB(A) is a worse fit than one that caps at 60 dB(A), even if both can be turned down.
4. **Mains powered or runs ≥10 hours on a charge** — for a workplace pilot we need it to cover a full working day without intervention. USB-C charging or USB-C constant-power is ideal.
5. **Physically simple controls** — power on/off and volume. We do not want pairing buttons, mode buttons, EQ presets, or any input that lets a participant accidentally change the audio source or the playback content.
6. **Brandable surface** — at minimum, space on the top or front for a silkscreen / pad-print of a logo, a single line of text, and a QR code (~25mm square minimum). Custom moulded enclosures are a plus but not required for the pilot run.
7. **No microphone, no Wi-Fi, no cloud connectivity, no companion app.** This is a privacy/research-integrity requirement, not a cost requirement. Participants need to be able to trust that the device is not listening or transmitting. If a candidate product has a mic for any reason — even just for a hands-free call feature that we wouldn't use — it's disqualified.

## Strong preferences (nice-to-haves)

- A built-in timer or scheduling function (e.g. "play for 8 hours then auto-off") would be excellent. Not required.
- A **tamper-evident seal** on the SD card slot or battery compartment, or an enclosure design where the SD card is internal/non-user-accessible, is preferred — we don't want participants swapping in their own audio.
- A neutral, non-childish aesthetic. Many sleep-machine products are styled for nurseries (pastels, animal shapes); we'd prefer a more adult / office-appropriate look. White, beige, light wood, light grey are all fine. A "Muji-style" or "Scandinavian minimal" aesthetic is the target.
- A run-time counter or simple usage log accessible by the researcher (not the participant) would be a significant bonus — we need to verify compliance and currently plan to do this via daily survey self-report.
- Form factor approximately the size of a hockey puck or small mug — fits on a desk without dominating it.
- Lower max volume is better. A device that maxes at 50 dB(A) at 1 m is a stronger candidate than one that maxes at 70 dB(A).

## Hard exclusions (do not show me)

- Bluetooth speakers with no SD card support
- Smart speakers (Alexa, Google Home, Tmall Genie clones, etc.)
- Any device with a microphone, regardless of stated function
- Karaoke speakers, party speakers, anything marketed on bass response
- White noise machines that *only* play their own preset sounds and cannot accept user audio (these are common — they have a fixed library on internal ROM and no way to load a custom track)
- Devices requiring a phone app for first-time setup
- Children's toys with pre-printed cartoon graphics
- Anything that needs a screen
- Branded consumer electronics being resold (we want OEM/ODM, not "I'm flipping a Marshall speaker")

## Categories to search

These are the right starting categories on Alibaba. Search across all of them, and combine terms with "OEM" and "custom logo":

- "Sound machine sleep OEM"
- "White noise machine custom logo"
- "TF card MP3 player speaker mini"
- "USB MP3 looper speaker"
- "Hotel ambient sound device" / "spa sound machine"
- "Sleep therapy speaker SD card"
- "Industrial MP3 audio player module" — sometimes the cleanest match, often used for retail audio displays, museum exhibits, transit announcements
- "Promotional speaker SD card playback"
- "Meditation timer speaker"

The "industrial MP3 player" / "retail audio module" category is worth specific attention — these devices are designed to play one looped track from an SD card, run for years on mains power, and have no consumer-facing features. They're often the right product wearing the wrong marketing.

## Supplier questions

For each candidate product, please put the following questions to the supplier and report their answers verbatim. Don't paraphrase the supplier's response — I want to see what they actually said, including any awkwardness or evasion.

1. **Audio source confirmation.** Can the device play a custom MP3 (or WAV) file loaded onto an SD card or internal flash? Can the file be looped indefinitely? On power-up, does playback start automatically without any user input?
2. **Microphone confirmation.** Does this device contain a microphone of any kind, for any purpose (calls, voice control, ambient detection)? Please confirm explicitly yes or no.
3. **Wireless confirmation.** Does this device contain any wireless transmitter (Bluetooth, Wi-Fi, NFC, RF) that is *active by default*? If wireless is present but disabled by default, can it be permanently disabled at the firmware level for our order?
4. **Maximum volume.** What is the device's maximum sound pressure level at 1 metre, measured in dB(A)? If you don't have this measurement, what is the rated speaker driver wattage and approximately how loud is it subjectively (e.g. "as loud as a quiet conversation", "as loud as a TV at normal volume")?
5. **Volume adjustment.** Is there a fixed-maximum-volume mode, or can we request a firmware-limited maximum for our order (e.g. "the volume knob's 100% position outputs no more than X dB")?
6. **Power.** Is the device mains-powered, battery-powered, or both? Battery capacity (mAh) and tested runtime at low volume? USB-C, micro-USB, or proprietary charging?
7. **MOQ and pricing tiers.** What is the MOQ? What is the unit price at 100 / 250 / 500 / 1,000 / 2,000 units? Are these prices ex-works, FOB, or DDP? Which port?
8. **Lead time.** From order confirmation, how long for sample? How long for first production run at 100 units? At 500 units?
9. **Customisation scope.** What custom branding can you offer at our volumes? Specifically: silkscreen / pad print on the existing housing, custom packaging, a custom-loaded SD card pre-installed at the factory, a custom enclosure colour, a fully custom enclosure mould. Please give pricing and MOQ for each separately.
10. **Pre-loaded audio.** Can the supplier load our supplied audio file onto each device's SD card or internal flash before shipping? What's the per-unit cost for this? What's the total file size limit?
11. **Tamper resistance.** Is the SD card slot internal (requires opening the case) or user-accessible? If user-accessible, can it be sealed, covered, or moved internally as a customisation?
12. **Certification.** Does the device have CE / UKCA / FCC certification? (We'll need at least CE/UKCA for distribution in the UK.) Are the certifications transferable to our branded version, or do we need to recertify?
13. **Sample.** Cost and lead time for a single sample, shipped to the UK?

## Output format I want from you

For each candidate product, give me:

```
[#1] Product name / supplier name
   Alibaba URL
   Photos: 2–3 representative images
   Quick verdict: [strong / moderate / weak] match, one-line reason
   Spec summary table: form factor, audio source, max volume, mic, wireless, power, controls
   Supplier responses: their full answers to the 13 questions above
   Honest gap analysis: what doesn't match the spec, what would need adapting
   Pricing at 100 / 500 / 2000 units, lead times, sample cost
```

Then a short closing summary:

- Which candidate I should consider first, and why
- Any pattern you noticed across the market (e.g., "the white-noise category is well-served but they all have fixed libraries; the retail-audio-module category has the right behaviour but ugly enclosures")
- Anything you think I'm missing or should reconsider in my brief

Don't sell me the products. Treat this as a sourcing report, not a sales pitch. If a supplier was evasive on the microphone or wireless questions, say so — that's data.

## Two further notes

**On price sensitivity.** This is a research pilot funded out-of-pocket. A device at £8 unit cost is meaningfully different from one at £25, but I'd rather pay £25 for a product that fits than £8 for one I have to fight against. Don't optimise for cheapness past the point where it costs me research validity.

**On supplier reliability.** For a 100–200 unit research pilot, a Gold Supplier with reasonable transaction history matters more than the absolute lowest price. I'd rather have a slightly-overpriced reliable supplier than chase a cheap one and have units arrive late, broken, or in some way different from the sample. Note any supplier flags (very new accounts, unusually low Trust scores, mismatch between stated factory and actual location, etc.) explicitly in your report.
