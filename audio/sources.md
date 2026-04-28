# Audio sources

A shortlist of birdsong / dawn-chorus recordings suitable for the Phase 0
pilot, with honest licensing notes. The objective is a single 30–60 minute
seamlessly-looping audio file representing temperate-zone (UK / Northern
European) bird soundscape, suitable for continuous workplace playback.

## Selection criteria

In priority order:

1. **License compatibility.** Research-pilot use is non-commercial, so
   CC-BY-NC is fine. CC0 / CC-BY (commercial-permissive) is preferred
   in case the project ever monetises. Public-domain or
   project-owned recordings are best.
2. **UK / temperate-Northern-European species.** Familiar, plausible.
   Avoids the "tropical chorus on a Edinburgh desk" uncanny-valley.
3. **Low anthropogenic noise.** Anything with traffic, planes, voices,
   or dogs barking is unusable for sustained ambient. The brain locks
   onto the foreign signal and the calming effect inverts.
4. **A single recordist / location ideally.** Mixing recordings made
   with different microphones at different distances produces an
   audible inconsistency that the brain will track as "moving".
5. **Length ≥ 5 minutes raw.** Short recordings can be looped but
   require more aggressive crossfading.
6. **Quality grade A on Xeno-canto, or equivalent on other sources.**
7. **Available as WAV / lossless.** MP3-of-MP3 transcoding losses
   compound. Only re-encode to MP3 once at the final step.

## Primary candidates

### 1. squashy555 — "Dawn Chorus Birdsong" (Freesound #573080)

- **URL:** https://freesound.org/people/squashy555/sounds/573080/
- **License:** **CC0 (public domain, commercial OK).** This is the
  strongest pick from a licensing standpoint.
- **Location:** UK
- **Date recorded:** 29 May 2021, 4:00 AM
- **Species:** robin, goldfinch, song thrush
- **Why it's the top pick:** UK location, CC0 license (zero
  attribution overhead, commercial permissive), spring dawn chorus,
  user reviews confirm low background noise, recorded with a Tascam
  DR07 Mk2 (a respected portable recorder for this purpose).
- **Caveat:** I haven't auditioned it — the listing page indicates
  high quality but you should listen before committing. Search for the
  specific recordist's other sounds for a coherent set.

### 2. squashy555 — "blackbirds at dawn" (Freesound #341675)

- **URL:** https://freesound.org/people/squashy555/sounds/341675/
- **License:** Check page (Freesound shows per-sound license; same
  recordist often consistent but not guaranteed).
- **Length:** 4:51, WAV 16-bit 44.1 kHz stereo (49 MB)
- **Date:** March 2016, 5:30 AM
- **Species:** mostly blackbirds
- **Why it's a strong secondary:** Same recordist as #1 (consistent
  equipment), single dominant species, moderate length suitable for a
  loop with crossfade. Less species-rich than #1 — a feature if you
  want a calmer, less "busy" soundscape, a bug if you want diversity.

### 3. Xeno-canto Set 3781 — Peak District Soundscapes

- **URL:** https://xeno-canto.org/set/3781
- **License:** CC-BY-NC-SA 4.0 (typical for Xeno-canto). Non-
  commercial only.
- **Location:** South West Peak National Park, UK (~400m altitude)
- **Length:** Multiple recordings, 3–30 minutes each
- **Why it's a strong tertiary:** Single recordist (consistent),
  explicitly described as having very little anthropogenic noise
  intrusion, multiple recordings to choose from, UK habitat.
  Longer raw recordings reduce loop-crossfade aggressiveness.
- **Caveat:** NC-SA license — fine for research, blocks commercial
  use, and SA means any derivative work has to be released under
  the same license.

### 4. juskiddink — Birdsong pack (Freesound pack #3675)

- **URL:** https://freesound.org/people/juskiddink/packs/3675/
- **License:** CC-BY (attribution required, commercial OK)
- **Why it's a useful fallback:** Single recordist, multiple
  recordings, UK, CC-BY (commercial-permissive). Reviews praise the
  low ambient white noise.
- **Caveat:** Many recordings in this recordist's catalogue are
  short (< 1 min) — would require more aggressive looping or
  stitching.

### 5. Philip_Goddard — Cot Valley dawn chorus (Freesound #688888)

- **URL:** https://freesound.org/people/Philip_Goddard/sounds/688888/
- **License:** Check page (Freesound).
- **Location:** Cot Valley, Cornwall, UK
- **Why it's interesting:** Recordist's own description praises the
  expansive valley acoustic perspective. Distant dawn chorus has
  a different perceptual quality from close-mic — may feel more
  "outside" and less "in your face" at low volume.

## Recommended approach

Start with **candidate #1 (squashy555 #573080)** as the primary
audio asset for Phase 0. CC0 means zero downstream constraint, the
recordist has consistent technique, and the species are
temperate-UK-familiar. If, on audition, the duration is too short
(reviews don't mention length explicitly), supplement with #2 from
the same recordist for a longer loop.

If — after listening — neither sounds right, fall back to the
Xeno-canto Peak District set (#3) which gives you longer raw material
at the cost of NC licensing.

## What to download

For each candidate that makes the shortlist:

1. **Original-quality file** (WAV preferred; FLAC if available).
2. **License page screenshot or copy** — record the license at the
   point of download. Freesound and Xeno-canto have both changed
   licensing structures historically; get a snapshot for your records.
3. **Recordist attribution string** — even for CC0, attribution is
   polite. Format: `"<title>" by <recordist>, via <source>, <license>`.

## Attribution example

For the project's printed insert and any future publication:

> Dawn chorus audio: "Dawn Chorus Birdsong" by squashy555, via
> Freesound (CC0). Recorded UK, 29 May 2021.

## What's deliberately not on the shortlist

- **YouTube "8 hour relaxing birdsong" videos.** Almost all are
  unlicensed re-uploads of someone else's field recordings, often
  with inaudible looping artefacts and added compression that
  degrades the high-frequency band the brain is doing its detection in.
- **Commercial sample libraries** (BBC Sound Effects Archive,
  Boom Library, etc.). High quality, but licensing and attribution
  for distributed research devices is awkward and often expensive.
  Worth revisiting in Phase 1 if Phase 0 produces signal.
- **Non-bird "nature" recordings** (rivers, wind, rain). The
  hypothesis is specifically about the birdsong-band signal, not
  about nature-coded audio in general. Including water sounds in
  the loop confounds the variable and makes the result
  uninterpretable.
- **Synthetic / generative birdsong** (including the procedural
  Web Audio engine on the project landing page). The whole point
  of Phase 0 is to test the hypothesis with the simplest possible
  audio source. If real recordings work, procedural becomes a
  Phase 1 ablation. If real recordings don't work, procedural
  was never going to.
