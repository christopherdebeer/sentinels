# Voices

> Research-grounded model of bird vocalisations to inform the
> procedural audio engine. Two-level taxonomy: **call types**
> (functional categories that span the acoustic space) and a
> **UK garden cohort** (species presets composed from those types).

This is a working reference, not a finished implementation. The
goal is to give the engine vocabulary that can plausibly be
called *bird-like* in a way that survives close listening,
grounded in citable literature rather than in the engine
author's intuitions about what birds sound like.

---

## Why this matters

The engine's current four voices — sweep, trill, pip, warble —
are reasonable acoustic primitives but they aren't *species*
or *functional categories* in any biologist's taxonomy. The
analysis of the squashy555 recording (see
[`audio/analysis/tuning-report.md`](analysis/tuning-report.md))
showed the engine is now spectrally close to real chorus, but
it's still acoustically *flat* — every voice draws from the same
distribution, every call is independent of every other. Real
chorus has structure: species succession, motif repetition,
overlap avoidance, antiphonal patterns, distinct call
*functions* with distinct acoustic signatures.

The improvements below would take the engine from "spectrally
plausible" to "structurally plausible". Whether they are
audible improvements is a separate question, addressable by
A/B testing (see end of document).

---

## 1. Call types — the functional taxonomy

The literature consistently divides bird vocalisations into
**song** (long, complex, learned, breeding-context, mostly males)
and **call** (short, simple, year-round, function-specific, both
sexes). Both terms are useful, both are fuzzy at the boundaries,
and both subdivide further.

For the engine, I propose seven categories. Each has a clear
acoustic signature, a clear behavioural function, and is
documented in standard ornithological references (Catchpole &
Slater, *Bird Song*, 2008; Marler & Slabbekoorn, *Nature's Music*,
2004; the *Birds of the World* online reference).

### 1.1 Song-types

Songs are the long, structured vocalisations associated with
territory and courtship. They subdivide by *internal structure*:

#### Continuous-warble song
A flowing, multi-syllabic vocalisation with no obvious
repetition structure. **Example:** European robin, dunnock,
blackcap. Engine analogue: extended sequence of varied
short syllables with frequency drift across the syllables.

| Parameter | Value |
|---|---|
| Strophe duration | 2–3 s typical (robin: mean 2.3–2.7 s) |
| Frequency range | 0.2–22 kHz overall, peak energy 3–4 kHz, harmonics 8 kHz |
| Within-strophe gap | ~100 ms between syllables |
| Strophe-to-strophe gap | 2–6 s |
| Source | Verboom (2018, 2019) — Ardea, multiple papers |

#### Repeating-phrase song
Short distinctive phrase, repeated 2–4× before moving to a new
phrase. **Example:** song thrush. Engine analogue: pick a
syllable shape, play it 2–4 times in close succession (~0.5 s
gaps), then pick a new shape.

| Parameter | Value |
|---|---|
| Phrase duration | 0.4–1.0 s |
| Repetitions | 2–4 (sometimes 5) |
| Within-phrase gap | 0.3–0.6 s |
| Strophe duration (3 phrases × 3 reps + grating notes) | ~10 s |
| Frequency | 1.5–6 kHz, broader for "twitter" syllables |
| Source | Wesołowski et al. 2019; Catchpole & Slater 2008 |

#### Two-note motif song
Strophic song built from a 2-note phrase, repeated rapidly.
**Example:** great tit ("teacher-teacher-teacher"). Engine
analogue: alternating two notes, ~0.5 s phrase period,
~5–10 phrases per strophe.

| Parameter | Value |
|---|---|
| Phrase period | ~0.5 s (teacher-teacher) |
| Repetitions per strophe | 5–10 |
| High note | 4.5–5 kHz, slightly downward inflected |
| Low note | 3.5–4.5 kHz, broader range |
| Strophe-to-strophe gap | 3–6 s |
| Source | Slabbekoorn & Peet (2003); BTO; numerous |

#### Trill song
Rapid repetition of one syllable type, often with a wide
frequency sweep within each syllable. **Example:** wren —
"valiant rapid trill", among the most acoustically dense songs
in the European cohort. Engine analogue: closely-spaced (10–20 Hz
repetition rate) sweep syllables.

| Parameter | Value |
|---|---|
| Strophe duration | ~5 s (wren typical) |
| Spectral bandwidth | 2.5–9.2 kHz |
| Syllable repetition rate | 10–20 syllables/s |
| Internal structure | Often clicks → trill → varied pattern |
| Strophe-to-strophe gap | 5–15 s |
| Source | Camacho-Alpízar et al. (multiple); Bioacoustics 2020 |

### 1.2 Call-types

Calls are the short, function-specific vocalisations that
occur year-round and aren't sex-restricted. The functional
categories matter: each has a distinct acoustic signature
shaped by selection pressure for what the call must do.

#### Contact call
Short, often quiet, used between flock members or pair-bonded
birds to maintain proximity. Generally tonal, narrow-band, soft.

| Parameter | Value |
|---|---|
| Duration | 50–150 ms |
| Frequency band | 4–8 kHz typical (varies by species) |
| Modulation | Often mild downward sweep |
| Repetition | Single or ~1 Hz repetition |
| Examples | Long-tailed tit "see-see-see", many warblers |

#### Alarm call
Short, sharp, often rising in frequency, structured to be
*hard to localise* — a feature of selection pressure to evade
predators while warning conspecifics. Distinct functional
classes: **"seet"** (high-pitched, narrow-band, used for aerial
predators) and **"mobbing"** (broad-band, short, repetitive,
used for perched predators).

| Parameter | Value (seet) |
|---|---|
| Duration | 100–500 ms |
| Frequency band | 6–9 kHz (high-pitched, hard to localise) |
| Modulation | Pure-tone or slight sweep |
| Repetition | Often repeated 3–5× |
| Source | Marler 1955 — classic paper on hawk-alarm structure |

| Parameter | Value (mobbing) |
|---|---|
| Duration | 50–200 ms |
| Frequency band | 1–8 kHz (broadband, easy to localise) |
| Repetition | Rapid, 2–10 Hz |
| Examples | Blackbird "chinking", great tit scolding, chickadee |

#### Flight call
Brief, distinctive, used in flight to maintain group cohesion.
Often the most species-specific vocalisation a bird produces.

| Parameter | Value |
|---|---|
| Duration | 50–250 ms |
| Frequency band | 3–9 kHz, often with diagnostic frequency modulation |
| Examples | Blackbird "tsiirr" (102–359 ms, 5.1–9.9 kHz), redwing "tseep" |
| Source | Evstigneeva (2017) — direct measurements |

(Optional: distress, begging, courtship-trill — additional
functional categories that exist in the literature but are
less relevant to a calm dawn-chorus soundscape.)

---

## 2. UK garden cohort — species presets

A short list of species that dominate UK temperate dawn chorus
in gardens, woodland edges, and parks. Each is mapped to one or
more of the call/song types above, with measured acoustic
parameters from the literature where available.

This list is the natural cohort the squashy555 recording was
made in (Burton-on-Trent, May), and corresponds to the species
acoustically dominant in the broader UK and Western European
literature.

### European Robin — *Erithacus rubecula*

- **Primary vocalisation**: Continuous-warble song, with frequent
  trill components ("vibrating components" in Verboom's terminology).
- **Strophe duration**: 2.3–2.7 s
- **Peak energy**: 4 kHz fundamental, harmonics at 8 and 16 kHz
- **Frequency range**: 0.2–22 kHz overall; dominant 3–4 kHz
- **Strophe gap**: 2–6 s
- **Habitat**: Urban robins sing longer, narrower, simpler songs
  than rural conspecifics; minimum frequency rises in noise
  (Golini 2026, Edinburgh study — directly relevant to UK).
- **Key citation**: Verboom 2018a–b, 2019; Golini et al. 2026.

### Common Blackbird — *Turdus merula*

- **Primary vocalisation**: Strophic song. Each strophe is a
  *motif* (low-frequency melody, ~1.5–3 kHz, fluty, 2–4 s) followed
  by a *shrill* (higher-pitched, ~4–6 kHz, broader). Sometimes a
  second motif follows.
- **Strophe duration**: ~3–5 s typical
- **Strophe-to-strophe gap**: "at least a few seconds", typically
  3–10 s (Dabelsteen 1984)
- **Calls**: Distinctive *tsiirr* attraction call, 102–359 ms,
  5.1–9.9 kHz, with two-band structure (high + lower modulated).
  Loud "chinking" alarm.
- **Habitat**: Forest blackbirds sing at lower frequencies with
  longer strophe gaps than urban birds (Nemeth & Brumm 2009).
- **Key citations**: Dabelsteen 1984, 1988; Evstigneeva 2017
  (calls); Nemeth & Brumm 2009 (urban).

### Song Thrush — *Turdus philomelos*

- **Primary vocalisation**: Repeating-phrase song. Each phrase
  repeated **2–4 times** in close succession, then a new phrase.
  This is the diagnostic acoustic feature.
- **Phrase types**: Two distinct categories — **whistle** (loud,
  low-frequency, tonal) and **twitter** (soft, broadband, complex)
  (Wesołowski et al. 2019).
- **Strophe**: A "run of musical phrases", several minutes total,
  highly variable. Repertoire of 100+ phrase types per individual.
- **Frequency**: 1.5–8 kHz typical
- **Habitat**: Urban song thrushes have larger repertoires and
  repeat phrases more often than forest conspecifics
  (Wesołowski 2019).
- **Key citations**: Wesołowski et al. 2019 (BMC Ecology);
  Catchpole & Slater 2008.

### Eurasian Wren — *Troglodytes troglodytes*

- **Primary vocalisation**: Trill song. Rapid (10–20 syllables/s)
  trill, often preceded by clicks or scratchy notes, with
  variable patterns mid-song.
- **Strophe duration**: ~5 s (typical UK measurements)
- **Spectral bandwidth**: 2.5–9.2 kHz (Camacho-Alpízar et al.)
- **Strophe-to-strophe gap**: 5–15 s
- **Behaviour**: Wrens demonstrably **avoid overlapping** other
  wrens' songs — start their songs predominantly right after the
  end of a stimulus song (Naguib et al.). Useful for the
  inter-call structural model.
- **Key citations**: Camacho-Alpízar (multiple); Naguib et al.
  (overlap-avoidance experiments).

### Great Tit — *Parus major*

- **Primary vocalisation**: Two-note motif song,
  "teacher-teacher-teacher". The phrase repeats throughout the
  strophe; population-level dialect variation in number of notes
  per phrase.
- **Phrase**: 2-note phrase, ~0.5 s per phrase
  - High note: 4.5–5 kHz, slight downward inflection
  - Low note: 3.5–4.5 kHz, broader bandwidth
- **Strophe**: 5–10 phrase repetitions per strophe
- **Strophe gap**: 3–6 s
- **Key recognition cue**: Frequency is the dominant feature
  great tits *themselves* use for song-type categorisation
  (Weary 1990 — direct experimental evidence).
- **Key citations**: Slabbekoorn & Peet 2003 (Nature) for urban
  frequency shift; Weary 1990 for categorisation.

### Blue Tit — *Cyanistes caeruleus*

- **Primary vocalisation**: Trill — rapid descending repetition
  of a single high note, ~5–8 kHz, "tsee-tsee-tsee-tsi-hi-hi-hi"
  pattern. Higher-pitched and softer than great tit.
- **Strophe duration**: 1–2 s
- **Strophe-to-strophe gap**: 3–8 s
- **Calls**: Soft "see" contact call, broader-band scolding alarm.

### Dunnock — *Prunella modularis*

- **Primary vocalisation**: Continuous-warble song, similar in
  acoustic character to robin but typically softer and shorter.
- **Strophe duration**: 2–3 s
- **Frequency**: 4–7 kHz
- **Texture**: Less harmonic richness than robin; more
  "scratchy" quality.

### Chaffinch — *Fringilla coelebs* (optional 8th)

- **Primary vocalisation**: Distinctive accelerating-then-flourish
  song — a clear introductory series of 3–5 notes, then a downward-
  cascade trill, then a terminal flourish ("chip-chip-chip-cherry-
  erry-erry-tissi-cheweeo"). Highly stereotyped per individual.
- **Strophe duration**: 2–3 s
- **Frequency**: 2–6 kHz
- **Why optional**: Less common in true urban gardens (more rural-
  edge), but very common in UK woodland chorus.

---

## 3. Structure between calls — interaction model

The single biggest gap between the engine and real chorus isn't
in the calls themselves but in *how they relate to each other*.
The engine currently treats every call as an independent random
event (with shared slow drift); real chorus has structural
correlation at multiple scales.

The literature supports a small set of well-documented
phenomena, each tractable to add to the engine:

### 3.1 Species succession at dawn

Species don't all start singing simultaneously at dawn. There's
a **stereotyped order**, partly driven by relative eye size
(species with larger eyes can forage in lower light, so they
sing earlier; Thomas et al. 2002). For UK garden cohort
roughly: blackbird → robin → song thrush → wren → great tit →
blue tit → dunnock, though the pattern is statistical not
deterministic.

**Engine implication**: For an "auto-sunrise" mode, fade species
in over a 30–45 minute simulated period in roughly that order.
Less relevant for the always-on demo, but worth supporting.

### 3.2 Strophe-gap autocorrelation

Within a song bout from a single bird, strophe-to-strophe gaps
are *more regular* than independent — birds settle into a rhythm.
Modelled by Dabelsteen as Markovian rather than Poisson.

**Engine implication**: When an individual voice is "active",
it should produce strophes with self-correlated gap timing
(e.g. a Gaussian around a per-bird mean), rather than
re-sampling the global gap distribution each time.

### 3.3 Overlap avoidance

Wrens, blackbirds, and several other species **time their
song starts to follow gaps** in conspecific or heterospecific
song (Naguib et al., multiple). The chorus is more "polite"
than independence would predict.

**Engine implication**: When scheduling a new strophe, slightly
bias the start time to avoid overlapping the *end* of an active
strophe. Cheap to implement, perceptually significant.

### 3.4 Antiphonal triggering

A song from one bird increases the probability of another
nearby bird singing in the next few seconds — the "stimulation"
documented in Brown-throated Warbler / dawn-chorus playback
experiments (Hu & Cardoso 2010; multiple). This is the
*structural* mechanism behind dawn-chorus density bursts.

**Engine implication**: When a strophe ends, transiently elevate
the call-rate parameter for the next 3–8 seconds. This produces
the burst structure visible in the squashy555 density-drift plot
(see analysis output) without needing an explicit pink-noise
modulator.

---

## 4. Implementation sketch

Rough plan for an engine refactor that uses these models. Not
written yet — this is the design, not the code.

```
// Per-voice profile (call/song type with parameters)
const VOICES = {
  robinSong: {
    type: 'continuous-warble',
    strophe: { dur: [2.0, 2.8], gap: [2, 6] },
    syllables: { count: [4, 12], gap: [0.08, 0.15] },
    freq: { peak: 4000, range: [3200, 6500], harmonics: 3 },
    behaviour: { antiphonal: 0.4, overlapAvoid: 0.6 },
  },
  blackbirdMotif: {
    type: 'motif-shrill',
    motif: { dur: [1.5, 2.5], freq: [1500, 3000], harmonics: 2 },
    shrill: { dur: [0.4, 0.8], freq: [4000, 6000], harmonics: 3 },
    strophe: { gap: [3, 10] },
    behaviour: { antiphonal: 0.5, overlapAvoid: 0.7 },
  },
  songThrushPhrases: {
    type: 'repeating-phrase',
    phrase: { dur: [0.4, 1.0], reps: [2, 4], internalGap: [0.3, 0.6] },
    nPhrases: [3, 8],
    freq: { range: [1500, 6000], harmonics: 3 },
    behaviour: { antiphonal: 0.3, overlapAvoid: 0.4 },
  },
  greatTitTeacher: {
    type: 'two-note-motif',
    phrase: { period: 0.5, hi: 4750, lo: 4000, dur: 0.18 },
    nReps: [4, 9],
    behaviour: { antiphonal: 0.6, overlapAvoid: 0.5 },
  },
  wrenTrill: {
    type: 'trill-song',
    strophe: { dur: [4, 6] },
    trill: { rate: [12, 18], freq: [3500, 8500] },
    behaviour: { antiphonal: 0.5, overlapAvoid: 0.9 },  // wrens famous for it
  },
  // ...
};

// Cohort presets compose voices
const COHORT_UK_GARDEN = {
  robinSong: { weight: 0.20, density: 1.0 },
  blackbirdMotif: { weight: 0.18, density: 0.7 },
  songThrushPhrases: { weight: 0.10, density: 0.5 },
  greatTitTeacher: { weight: 0.18, density: 0.9 },
  wrenTrill: { weight: 0.10, density: 0.6 },
  blueTitTrill: { weight: 0.10, density: 0.7 },
  dunnockWarble: { weight: 0.08, density: 0.5 },
  // contact / alarm calls modelled as background voices
  contactCall: { weight: 0.06, density: 1.5 },
};

// The scheduler maintains per-voice state (last-strophe time,
// current burst-stimulation level, etc.) and uses the structural
// model to decide what to schedule next, not just when.
```

Two notable shifts from the current engine:

1. **Voices are species-typed compositions of call types**, not
   independent timbral primitives. A "robin" voice is a
   parameter set on the continuous-warble template, not a
   distinct synthesis algorithm.
2. **Scheduling is stateful**. The engine tracks who recently
   sang, biases scheduling against overlap, and amplifies
   density transiently after a strophe ends.

---

## 5. What this gets us — and what it doesn't

**What this gets us, if implemented:**

- Listeners with even passing familiarity should hear a
  recognisably *British* dawn chorus rather than a generic
  "synth birds" texture.
- Structural features (motif repetition, two-note teacher
  phrases, the trill-bird, the warble-bird) give the brain
  pattern-recognition hooks that help the soundscape read as
  *bird* even at very low volumes.
- The interaction model (overlap avoidance, antiphonal bursts)
  produces the density structure the analysis showed was
  missing — without needing an ad-hoc pink-noise modulator.

**What this does *not* get us:**

- **Acoustic precision**. The parameter values above are
  literature-derived; they're approximate. To actually match
  individual species' calls closely we'd need direct measurement
  on a curated reference set (achievable with the same
  `analyse.py` pipeline, applied per-species). For the
  landing-page demo this is overkill; for any move toward using
  the engine as the device's actual audio source, it's required.
- **Individuality**. Real chorus has multiple individuals
  *of the same species* with slightly different songs and timings.
  The engine could model this (per-individual parameter jitter
  drawn at start-of-session) but it adds complexity for marginal
  perceptual gain.
- **A guaranteed perceptual improvement.** "More structurally
  realistic" doesn't necessarily mean "more calming" or "more
  pleasing". It might. It might also be *too* lifelike in a way
  that becomes attention-grabbing rather than ignorable. This
  needs A/B testing.

## 6. A/B test plan (informal)

Before committing the structurally-aware engine as the default,
and given the project's central concern that the soundscape
should be "available to be ignored" rather than attention-grabbing:

1. Implement the new engine behind a toggle in the listen panel
   ("naturalistic" / "minimal").
2. Default position: minimal (current engine).
3. Self-A/B over a couple of work sessions: one morning naturalistic,
   one morning minimal, one morning silence as control. Note
   subjective experience: noticed when? Distracting at any point?
   Comforting? Boring?
4. If naturalistic feels better *and* doesn't pull attention,
   make it default. If it feels more lifelike *but* pulls
   attention, keep it as opt-in.
5. Either way, the science work is in the repo and the model is
   correct — the engineering decision is downstream of perception,
   not upstream of it.

---

## References

Selected, by relevance to engine implementation:

- **Catchpole, C. K., & Slater, P. J. B. (2008).** *Bird Song:
  Biological Themes and Variations* (2nd ed.). Cambridge UP.
  — The standard textbook. Foundational reference for song vs
  call distinction, learning, function.
- **Marler, P., & Slabbekoorn, H. (Eds.). (2004).** *Nature's
  Music: The Science of Birdsong*. Academic Press. — Comprehensive
  multi-author reference for acoustic and behavioural side.
- **Verboom, W. C. (2018a).** Bird vocalizations: call of the
  European robin (*Erithacus rubecula*). — Detailed acoustic
  measurements, robin calls.
- **Verboom, W. C. (2018b).** Bird vocalizations: songs of the
  European robin. — As above, song parameters.
- **Verboom, W. C. (2019).** Bird vocalizations: song repertoire
  of the European robin. — Repertoire structure.
- **Wesołowski et al. (2019).** Habitat-related differences in
  song structure and complexity in song thrush. *BMC Ecology*. —
  Whistle/twitter dichotomy; phrase-repetition characterisation.
- **Slabbekoorn, H., & Peet, M. (2003).** Birds sing at a higher
  pitch in urban noise. *Nature* 424:267. — Great tit urban
  frequency shift; canonical paper.
- **Weary, D. M. (1990).** Categorization of song notes in great
  tits: which acoustic features are used and why?
  *Animal Behaviour*. — Frequency is the dominant categorisation
  feature great tits themselves use.
- **Nemeth, E., & Brumm, H. (2009).** Blackbirds sing higher-
  pitched songs in cities. — Urban/forest comparison, gap timing.
- **Dabelsteen, T. (1984).** An analysis of the full song of the
  Blackbird *Turdus merula*. *Ornis Scandinavica* 15:227–239.
  — Foundational blackbird-song characterisation.
- **Evstigneeva, M. D. (2017).** Species-specific attraction call
  of the blackbird in migration and breeding. — Direct
  measurements of *tsiirr* call (102–359 ms, 5.1–9.9 kHz).
- **Naguib, M., et al.** (multiple) — wren overlap avoidance
  experiments, eg. Naguib & Mennill 2010 *Ethology*.
- **Thomas, R. J., et al. (2002).** Eye size in birds and the
  timing of song at dawn. *Proc. R. Soc. B* 269:831–837. — The
  inefficient-foraging hypothesis for species succession.
- **Hu, Y., & Cardoso, G. C. (2010).** Which birds adjust the
  frequency of vocalizations in urban noise? *Animal Behaviour*.
  — Frequency-shift correlate analysis; succession discussion.
- **Golini et al. (2026).** Effects of anthrophony on song traits
  in European Robins. *Ecology and Evolution*. — Edinburgh
  population study, directly relevant geography.

For acoustic recordings used as ground truth and analysis input,
see [`audio/sources.md`](sources.md) and
[`audio/analysis/README.md`](analysis/README.md).
