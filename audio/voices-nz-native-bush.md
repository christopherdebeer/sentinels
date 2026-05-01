# Voices — Aotearoa New Zealand native bush cohort

> A second cohort definition, sibling to the [UK garden
> cohort](voices-uk-garden.md). Captures the dawn chorus of New
> Zealand's native bush — temperate-zone like the UK garden but
> acoustically dissimilar, the result of ~80 million years of
> avian evolution in geographic isolation.

This document is a research-grounded parameter sketch, not yet
implemented in the engine. Its first job is to surface what the
current SPECIES-template architecture can and cannot represent
of the NZ acoustic space — see §6.

---

## Why a NZ cohort

The trigger was a New Zealand trip and the recognition that the
dawn cast there is genuinely different. Not "different species
of thrush" different — *no thrushes at all* different. The
project's central hypothesis (procedurally-assembled birdsong
engages the safety response in any listener) carries an open
sub-question underneath it: does *familiarity* of the acoustic
material modulate that response? Is a New Zealander's brainstem
quieter when listening to tūī and korimako than to robin and
blackbird, or is bird-band birdsong universally calming
regardless of cultural-acoustic history?

The honest answer is we don't know. The literature mostly tests
listeners with their local soundscapes; the universality vs
familiarity distinction is uncontrolled. NZ-vs-UK is one of the
sharpest possible regional contrasts because the two avifaunas
share almost no taxonomic overlap among native species, and
both regions have been studied enough that acoustic parameters
are tractable.

Building this cohort is therefore primarily a *research
instrument* — paired with the UK cohort, it lets us A/B
familiarity at the species level. Secondarily it expands the
engine's acoustic repertoire, which is also good.

---

## Species selection

### Included in v1 (5 voices)

The cohort is restricted to species that are (a) genuinely
dawn-active, (b) reasonably common in mainland native bush
(rather than sanctuary-only), (c) acoustically distinct from
each other, and (d) have measurable parameters in the
literature.

1. **Tūī** — *Prosthemadera novaeseelandiae* (Meliphagidae).
2. **Korimako / bellbird** — *Anthornis melanura* (Meliphagidae).
3. **Pīwakawaka / fantail** — *Rhipidura fuliginosa* (Rhipiduridae).
4. **Riroriro / grey warbler** — *Gerygone igata* (Acanthizidae).
5. **Kererū / NZ wood pigeon wing-beats** — *Hemiphaga novaeseelandiae* (Columbidae) — non-vocal mechanical sound; see §3.

### Considered and excluded

- **Ruru / morepork** (*Ninox novaeseelandiae*). Distinctive
  "more-pork" call but predominantly nocturnal; including it
  shifts the cohort toward dusk-into-dawn rather than the peak
  dawn chorus. Hold for a possible v2 nocturnal/transitional
  cohort.
- **Tīeke / saddleback** (*Philesturnus carunculatus*).
  Acoustically distinctive (rhythmic "ti-eke-ke-ke") but
  functionally absent from most of mainland NZ — survives
  mainly on predator-free islands and fenced sanctuaries.
  Including it would mis-represent the modern dawn soundscape
  most NZers would recognise.
- **Kōkako** (*Callaeas wilsoni*). North Island kōkako song is
  perhaps the most distinctive single sound in NZ ornithology —
  slow, organ-like phrases that sound nothing like any other
  passerine. But the species is functionally absent across
  most of NZ; encountered only in specific sanctuary
  populations (Pureora, Tiritiri Matangi, etc.). Including it
  in a "NZ native bush" cohort would be aspirational rather
  than representative.
- **Kākā, kea, kākāriki** (parrots). Vocally important in some
  bush areas but harsh, screech-dominant, and not central to
  the *dawn* chorus specifically. Could be added in a v2 with
  more parrot-shaped templates.
- **Introduced songbirds** — blackbird, song thrush, starling,
  dunnock, house sparrow, chaffinch, etc. *Abundantly* present
  in modern NZ urban and suburban dawn chorus. A New
  Zealander's actual lifelong acoustic familiarity almost
  certainly includes these alongside natives. Important to
  note for **experimental design** (a familiarity comparison
  shouldn't pretend NZers only hear native birds), but
  excluded from this cohort because the project's research
  question is specifically about the *NZ-distinctive*
  component vs the UK-distinctive component.

A real-world NZ bush dawn is therefore a *blend*: this cohort
plus a fraction of the UK garden cohort. The engine could in
principle be configured to render that blend, but for the
purposes of A/B comparison the cleaner contrast is "pure NZ
native vs pure UK garden".

---

## 1. Tūī — *Prosthemadera novaeseelandiae*

- **Primary vocalisation**: Highly variable mixed song combining
  tonal whistles, fluty notes, repeated phrases, and *non-vocal-
  sounding* elements: clicks, coughs, mechanical whirrs, and
  documented supersonic syllables (above human hearing).
- **Strophe duration**: Highly variable, ~2–8 s; songs are often
  longer than UK passerines because of the diverse syllable
  inventory.
- **Frequency range**: 0.2 to >20 kHz (with documented syllables
  above 20 kHz that listeners cannot hear). Audible-range
  dominant energy 1–6 kHz with strong harmonic content.
- **Strophe gap**: 4–15 s; tūī sing in less continuous bouts
  than UK robins or blackbirds.
- **Distinctive features**:
  - Two functional syringes; can produce two notes simultaneously.
  - Per-individual repertoire varies widely (10–50+ syllable types
    catalogued per bird in some studies). Songs *don't repeat*
    cleanly the way song thrush phrases do.
  - **Mechanical syllables**: clicks (~10 ms broadband transients),
    coughs (~30–60 ms with rough noise), whirrs (~100–300 ms
    AM-modulated tonal). These are not "calls" in the warble/
    trill/motif sense — they're a category the UK cohort doesn't
    have.
  - Occasional pure-tone bell-like notes overlap acoustically
    with korimako; the two species can be confused at distance.
- **Habitat**: Common across native bush, regenerating bush,
  many suburban gardens with native plantings.
- **Key citations**: Hill et al. 2015 (repertoire structure);
  Hill & Lill 1998 (vocal learning); standard reference is
  *Birds of the World* online (Higgins et al.).

## 2. Korimako / bellbird — *Anthornis melanura*

- **Primary vocalisation**: Pure tonal "bell" notes, often
  delivered in short repeated phrases (2–4 notes). Less
  syllabically varied than tūī; more melodically pure.
- **Strophe duration**: 0.6–2.5 s for a phrase; longer continuous
  song bouts of 5–15 s exist.
- **Frequency range**: Dominant 2.5–5 kHz. Tonal energy
  concentrated in narrow bands relative to tūī.
- **Strophe gap**: 2–8 s; korimako sing in more sustained bouts
  than tūī.
- **Distinctive features**:
  - Strong **regional dialects** — different bush regions have
    measurably different bellbird songs; dialect boundaries can
    be sharp. (Brunton & Xu 2008 documented this for North
    Island populations.)
  - Phrases often follow **A-A-B** or **A-B-A** structures
    rather than pure A-A-A repetition.
  - The "chorus" effect emerges from many korimako overlapping
    each other at moderate distance — produces the iconic NZ
    bell-toned dawn ambience.
- **Habitat**: Native bush, increasingly suburban gardens with
  native plants. Recovering range after historical decline.
- **Key citations**: Brunton & Xu 2008, Brunton et al. 2008
  (dialect, vocal learning); *Birds of the World* online.

## 3. Pīwakawaka / fantail — *Rhipidura fuliginosa*

- **Primary vocalisation**: Quick, high-pitched "cheep" calls,
  delivered as short repeated phrases. Less melodically
  developed than tūī/korimako; closer to the UK cohort's
  contact-call register.
- **Strophe duration**: 0.4–1.5 s for a typical phrase.
- **Frequency range**: 4–8 kHz, narrow band, high-pitched.
- **Strophe gap**: 2–10 s; very common at edges and clearings.
- **Distinctive features**:
  - Vocalisations often accompany active foraging movement;
    more constant background "cheeping" than discrete strophe
    events.
  - North Island and South Island subspecies differ slightly
    in plumage; vocalisations broadly consistent.
- **Habitat**: Ubiquitous across NZ — native bush, suburban,
  agricultural margins. Often the first NZ bird a visitor
  hears clearly.
- **Key citations**: *Birds of the World* online (Higgins &
  Steele); Powlesland 1980s ecological work referenced widely.

## 4. Riroriro / grey warbler — *Gerygone igata*

- **Primary vocalisation**: Distinctive **descending trill** —
  a series of slurred notes that descend in both pitch and
  tempo through the song. Often described as the "first
  song of NZ spring".
- **Strophe duration**: 3–6 s for a complete song; the
  characteristic descending pattern occupies most of this.
- **Frequency range**: Roughly 4–7 kHz, with the descending
  pattern sweeping downward through this band.
- **Strophe gap**: 5–20 s; less continuous singers than tūī
  or korimako.
- **Distinctive features**:
  - The descending-trill pattern is acoustically very similar
    to **blue tit** descending trills in the UK cohort —
    convergent acoustic structure across unrelated taxa. Useful
    for engine validation: if the engine handles blue tit and
    riroriro with the same `descending-trill` template, it's
    evidence the template is genuinely functional rather than
    species-specific.
  - Riroriro are tiny (~6 g, smaller than UK wren) and the
    sound is correspondingly thin in timbre; less rich
    harmonic content than larger species.
- **Habitat**: Native bush, regenerating bush, gardens. Common
  across NZ but more often heard than seen.
- **Key citations**: *Birds of the World* online; Gill 1980
  ecological work; widely catalogued on NZ Birds Online and
  xeno-canto.

## 5. Kererū wing-beats — *Hemiphaga novaeseelandiae*

This entry breaks the species-as-vocal-source pattern. Kererū
are vocally quiet — they emit a soft *coo* that's barely
audible at distance. But their **wing-beats** are loud,
distinctive, and a defining acoustic feature of NZ bush.

- **Primary acoustic event**: **Wing-beat whoosh** during flight.
  Broadband mid-frequency pulse; ~200–500 ms duration; recurs at
  the wing-beat rate (~3–5 Hz) for the duration of the flight.
- **Frequency content**: Broadband, dominant energy 200 Hz–2 kHz
  (lower than most birdsong). Aerodynamic noise rather than
  syringeal phonation.
- **Event duration**: 1–4 s of flight, typically.
- **Inter-event gap**: Highly variable; depends on flight
  activity. Could model as 60–300 s background events.
- **Distinctive features**:
  - The current `SPECIES` schema assumes vocal sources; this
    voice is fundamentally different. Two options:
    (a) extend the schema to support `mechanical` events with
    broadband-pulse synthesis, (b) skip kererū from v1 and treat
    it as a v2 schema upgrade. **See §6** for the implementation
    review.
  - Acoustically more like a low-frequency rhythmic thump than a
    bird call — closer to a heartbeat or a distant helicopter
    in spectral character. The fact that it *is* a bird, and
    that NZers learn to recognise it, is part of why including
    it makes the cohort feel authentic.
- **Habitat**: Native bush, suburban with mature trees. Quite
  large birds (~600 g); the wing-beats are loud because of the
  bird's mass.
- **Key citations**: *Birds of the World* online for natural
  history; the wing-beat-as-acoustic-marker observation is
  standard in NZ field-guide commentary rather than from a
  primary acoustic study.

---

## 2. Cohort-level structure

### 2.1 Density and dawn timing

NZ native bush dawn chorus is generally *quieter* and *less
synchronised* than UK garden dawn chorus. Several factors:

- Lower total avian density per hectare than typical UK
  suburban habitat (introduced predators have suppressed many
  native species).
- Tūī and korimako don't all start at the same precise civil
  twilight moment the way UK passerines do; the chorus builds
  gradually.
- Less species overlap means fewer concurrent songs at peak.

For engine purposes: **density baseline should be lower** than
the UK cohort. Where UK garden cohort default is `density: 0.30`
producing ~11 strophes/min, NZ cohort might default to `0.20`
producing ~6–8 strophes/min, with stronger density-CV
(more bursts, longer lulls).

### 2.2 Cohort weights (proposed)

Based on relative dawn-chorus prominence in mainland native bush:

| Species | Weight | Notes |
|---|---|---|
| Tūī | 0.30 | Most prominent vocal contributor in most bush |
| Korimako | 0.25 | Where present, dominant — but more locally variable |
| Pīwakawaka | 0.20 | Ubiquitous, frequent vocaliser |
| Riroriro | 0.15 | Common but less frequent strophe rate |
| Kererū wing-beats | 0.10 | Rare events but distinctive when they occur |

Compare UK garden weights: robin 0.20, blackbird 0.16, song
thrush 0.10, great tit 0.16, wren 0.10, blue tit 0.10, dunnock
0.08, contact-calls 0.10. The NZ cohort is **less even** —
two dominant honeyeaters carrying ~55% of the chorus.

### 2.3 Dialect and individual variation

Both honeyeaters (tūī and korimako) have **strong regional
dialects** — much stronger than any UK garden species. A bellbird
in Banks Peninsula sounds materially different from one in
Northland. The current engine doesn't model regional dialects;
v1 of the NZ cohort would pick a single "neutral" parameter set
per species. A future v2 could parameterise dialects, but this
is a refinement rather than a foundational requirement.

### 2.4 Species succession

UK chorus has a fairly canonical species-succession order at
dawn (robin and blackbird first; thrushes and warblers later;
finches and house sparrows latest). NZ chorus is less ordered —
tūī and korimako begin together; pīwakawaka and riroriro filter
in within minutes. The engine's existing succession logic
(initVoiceState density-spread) handles this adequately without
a per-species sunrise offset.

---

## 3. Sources

The literature on NZ native bird vocalisations is real but
*sparser* than the UK literature, especially for measurable
acoustic parameters. Many of the parameter ranges above are
estimated from descriptive prose in *Birds of the World*
(Cornell Lab) and the *New Zealand Birds Online* encyclopedia
(nzbirdsonline.org.nz), augmented by xeno-canto recordings
inspected manually.

**Primary references**:

- Higgins, Peter, and others. *Handbook of Australian, New
  Zealand & Antarctic Birds* (HANZAB), 7 volumes, 1990–2006.
  The canonical reference; species accounts include
  vocalisation descriptions but rarely tabulated acoustic
  parameters.
- Heather, Barrie, and Hugh Robertson. *The Field Guide to the
  Birds of New Zealand*, revised editions. Less detailed
  acoustically but the standard popular reference.
- Robertson et al. *Atlas of Bird Distribution in New Zealand
  1999–2004*. Distribution; not directly acoustic but useful
  for "is this species actually present in mainland bush".
- *Birds of the World* (Cornell Lab) — online, structured
  species accounts including vocalisation descriptions, with
  citations to primary studies.
- *New Zealand Birds Online* (nzbirdsonline.org.nz) — open
  reference with embedded xeno-canto recordings.

**Specific studies referenced above**:

- Brunton, Dianne H., and Bonnie Xu. 2008. *"Vocal performance
  in three sympatric ... bellbird ...".* (Several papers from
  the Brunton lab on bellbird dialects and vocal learning.)
- Hill, Sarah D., et al. 2015. *"Vocal learning and song
  variation in tūī ..."*
- Hill, Sarah D., and Alan Lill. 1998. *"Auditory mimicry in
  the New Zealand tui ..."*
- Powlesland, Ralph. NZ DOC ecological surveys, 1980s, on
  fantail and other passerines.

**Honest gap**: I am not aware of a single primary-research
paper that tabulates acoustic parameters for a NZ-native
species cohort the way Catchpole & Slater or Marler & Slabbekoorn
do for European passerines. The parameters in this document are
my best-effort triangulation from descriptive sources and
inspection of representative xeno-canto recordings, not from a
single canonical reference. **A xeno-canto-based parameter
extraction pass — running the same `analyse.py` pipeline already
used for the squashy555 reference recording, against curated
recordings of each cohort species — would substantially improve
the parameter quality.** This is captured as a future work item.

---

## 4. Implementation notes for the engine

The engine's current SPECIES schema (in `index.html`, around
line 1147) has these per-species fields:

```js
{
  label: 'robin',
  latin: 'Erithacus rubecula',
  template: 'continuous-warble' | 'motif-shrill' |
            'repeating-phrase' | 'two-note-motif' |
            'trill-song' | 'descending-trill' | 'contact-call',
  strophe: { dur: [lo, hi], gap: [lo, hi] },
  // template-specific fields per species
  amp: 0.16,
  antiphonal: 0.5,
  overlapAvoid: 0.6,
}
```

Plus parallel maps keyed by species name: `VOICE_SPATIAL` (pan/
distance distributions), `VOICE_TINTS` (UI colour), `VOICE_LABELS`
(English + Latin display strings), and `COHORT_UK_GARDEN` (relative
emission weights).

To add NZ species, the architecture suggests:

1. Add NZ species entries to a separate `SPECIES_NZ_BUSH` dict,
   not to the existing `SPECIES`. Cohort selection swaps the
   active SPECIES dict at engine start.
2. Add parallel `VOICE_SPATIAL_NZ`, `VOICE_TINTS_NZ`, `VOICE_LABELS_NZ`,
   `COHORT_NZ_BUSH` maps. The active maps swap together with the
   SPECIES dict.
3. Add a cohort selector — URL parameter `?cohort=nz-bush`
   reads at page load, picks which dicts the engine uses.

Mapping the cohort to existing templates (and a few that need
work — see §6):

| Species | Existing template? | Notes |
|---|---|---|
| Tūī | Partial | Needs `mixed-warble` template + mechanical-syllable primitive (§6.3) |
| Korimako | Yes — `repeating-phrase` | Phrase structure (A-A-B) similar to song thrush; benefits from per-species partial gains for tonal purity (§6.1) |
| Pīwakawaka | Yes — `contact-call` | Direct fit |
| Riroriro | Yes — `descending-trill` | Direct fit — same template as blue tit; cross-cohort use of one template is itself useful evidence the template is functional rather than species-specific |
| Kererū wing-beats | No | Needs `flight-event` template (§6.4) |

**3 of 5 species fit cleanly**, **1 fits partially** (tūī needs
a mechanical-syllable extension), **1 fits not at all** (kererū
wing-beats are a different kind of acoustic event entirely). The
full review of missing engine primitives follows in §6.

---

## 5. Cohort selection in the engine

If both cohorts are eventually shipped, the SPECIES dictionary
becomes per-cohort and the engine needs a cohort selector. Two
implementation paths:

(a) **Cohort as engine state**, switched at runtime via a UI
control. Switching mid-playback requires re-initialising
voiceState; cleanest if cohort changes are infrequent.

(b) **Cohort as URL parameter** (e.g. `?cohort=nz-bush` vs
`?cohort=uk-garden`), set at page load. Simpler implementation;
cohort change requires reload. Adequate for the demo page
where listeners select a cohort once and listen.

(b) is simpler and probably correct for the landing-page demo.
The eventual device firmware would carry the cohort as a config
setting rather than a runtime control — there's no expectation
the device-listener changes regions during a session.

---

## 6. Engine primitives review — missing pieces

This section is the actionable output of writing this cohort
document. Building the NZ cohort surfaces three engine-level
gaps and one schema-level gap. Listed in order from "small
addition" to "schema redesign". (A pre-flight audit confirmed
several primitives are *already* implemented and don't appear
below as gaps: per-strophe spatial positioning via
`StereoPannerNode` + low-pass distance proxy + per-species
`VOICE_SPATIAL` parameters; per-species `antiphonal` and
`overlapAvoid` coefficients; density-coupled emission probability
and gap scaling; structured event emission for UI binding. The
engine is more capable than the gap list below makes it sound.)

### 6.1 Per-species partial-gain ratios

**Status**: Hard-coded in `synthTone`.

`synthTone` uses partial gains `[1.0, 0.40, 0.20, 0.10]` for
fundamental + 3 harmonics. This is a reasonable "warm passerine"
default but doesn't capture timbral variation between species. A
korimako should be more sinusoidal (lower partial gains —
closer to `[1.0, 0.15, 0.05, 0.02]`) than a tūī's tonal phrases.
A great tit's two-note song is brighter than a robin's warble.

Adding a per-species `partialGains` field (with the current array
as default) costs ~3 lines in SPECIES schema, ~5 lines in
`synthTone`. Pays off in subjective realism across both cohorts.

**Effort**: 30 minutes. **Value**: meaningful for korimako bell-tone
fidelity specifically; modest improvement elsewhere.

### 6.2 Strophe gap distribution shape

**Status**: Truncated-normal sampler in `scheduleAhead`.

Current code:

```js
const gapMean = (scaledLo + scaledHi) / 2;
const gapSd = (scaledHi - scaledLo) / 4;
const gap = Math.max(scaledLo * 0.5,
              Math.min(scaledHi * 1.5,
                gapMean + z * gapSd));
```

Problem: a truncated normal makes all gaps narrowly distributed
around a mean. Real chorus — both UK and NZ — has **log-normally**
distributed gaps (the engine's own `analyse.py` measures
`gap_lognormal_mu/sigma`, but the engine doesn't *use* those
values for sampling, only for downstream analysis of recordings).
Log-normal sampling produces most gaps near the median plus a
heavy tail of long lulls — exactly the shape NZ chorus has more
of than UK chorus.

Fix: replace the truncated-normal sample with a log-normal
sample driven by per-species `gap_mu` and `gap_sigma`. Retune
the per-species gap parameters to express `mu`/`sigma` rather
than `[lo, hi]`. Validation against the squashy555 reference
should *improve* slightly (current engine has `gap_lognormal_sigma`
of 0.51 vs real recording's 0.45 — a small mismatch from the
truncated-normal shoehorn).

**Effort**: 1 hour, plus retuning each species' gap parameters
in SPECIES. UK cohort improvement that the NZ cohort surfaces.

### 6.3 Mechanical-syllable primitive (clicks, coughs, whirrs)

**Status**: Genuinely missing. Tūī's repertoire is half-vocal
and half-mechanical; the engine's all-tonal synthesis can't
reproduce the click/cough/whirr categories.

What's needed: a new synthesis path alongside `synthTone`, call
it `synthMechanical`, that produces:

- **Click**: ~10 ms broadband transient (filtered noise burst,
  short envelope). 1–3 lines using an `AudioBufferSourceNode`
  with pre-generated white-noise buffer + bandpass filter +
  sharp envelope.
- **Cough**: ~30–60 ms rough-textured noise pulse (filtered noise
  with mild AM modulation, broader bandwidth).
- **Whirr**: ~100–300 ms tonal pulse with strong AM at ~30–60 Hz
  (small-motor character). Carrier oscillator + LFO on its
  gain.

Then a new template, `mixed-warble`, that accepts a per-syllable-
type distribution. Tūī's emit function draws from
`{tonal: 0.6, click: 0.15, cough: 0.10, whirr: 0.15}` rather
than always producing `synthTone` syllables. The
`continuous-warble` template stays as-is; it's still used by
robin and dunnock.

**Effort**: 1–2 days. New `synthMechanical` family of generators
(~80 lines), `mixed-warble` template implementation (~30 lines),
tūī parameter set (~20 lines), tuning by ear against reference
recording.

**Does this matter?** Yes, for tūī specifically. A pure-tonal
"tūī" is just a warble with the wrong frequencies; it loses the
species' single most distinctive feature. NZers familiar with
tūī would identify the omission immediately. For the
familiarity-vs-novelty research question this matters: a degraded
tūī isn't a fair test of the NZ cohort.

### 6.4 Non-vocal acoustic event support (kererū wing-beats)

**Status**: Schema-level gap. The kererū wing-beat is *not* a
"strophe" — it's a 1–4 second sequence of broadband
low-frequency pulses at ~3–5 Hz. The current engine's
`emitStrophe` family always produces syllable-like events at
bird-band frequencies routed through the spatial chain.

Three options, in increasing scope:

(a) **Skip kererū from v1.** Reduce the cohort to 4 species.
Honest but loses a distinctive part of the soundscape.

(b) **Implement as a special-case `flight-event` template** that
shares the strophe scheduling and spatial machinery but runs a
hard-coded pulse-train synthesis. Doesn't generalise but solves
the immediate problem.

(c) **Generalise to "non-vocal events" as a first-class
category.** Schema gains an `eventType: 'vocal' | 'mechanical'`
field; the cohort can include arbitrary non-vocal events
(kererū wing-beats, woodpecker drumming, kiwi foot-rustling at
night, snipe wing-feather sound during display flight).

(b) is pragmatic. (c) is the right architectural answer if the
project ever includes other mechanically-vocal species (NZ alone
has multiple — kiwi, snipe, takahē). I'd recommend (b) for v1
and revisiting (c) when a third such species is requested.

**Effort**:
- (a): zero, just exclude.
- (b): half-day. New template, kererū parameters, listening tune.
- (c): ~2 days. Schema extension affecting the strophe scheduler,
  the spatial chain (which currently assumes vocal-band frequencies
  and may need broader low-pass cutoff for mechanical sounds), and
  validation across both cohorts.

### 6.5 What I'm *not* listing as gaps

To be explicit about what's adequate as-is:

- **Spatial positioning.** Already implemented (`VOICE_SPATIAL`
  + `samplePosition` + per-strophe pan/distance/low-pass chain).
  NZ cohort just needs `VOICE_SPATIAL` entries — a UK→NZ
  acoustic-position-table extension, not new code.
- **Cohort-density variation.** The existing `density` slider
  + cohort weights handle "NZ chorus is sparser" without engine
  changes. Default density for NZ cohort is just a different
  initial slider value.
- **Subtitle / dot-pulse / debug-panel.** Engine-event emission
  is already structured; UI bindings already work off species
  metadata. NZ cohort just needs entries in `VOICE_LABELS` and
  `VOICE_TINTS`.
- **Schedule fairness.** The current overlap-avoidance and
  antiphonal-stim mechanisms are species-agnostic. They work
  for NZ species without modification.

The gap list above is real, but it's smaller than I expected
when starting this document. Most of what an NZ cohort needs
is parameter data, not new engine code.

---

## 7. Summary — what to build first

A minimum viable NZ cohort that ships in the engine would be:

**v0.5 — UK-template-compatible subset (no engine code changes,
parameter data only)**: korimako (`repeating-phrase`),
pīwakawaka (`contact-call`), riroriro (`descending-trill`).
Three species that fit the existing schema cleanly. Adds entries
to `SPECIES`, `VOICE_SPATIAL`, `VOICE_TINTS`, `VOICE_LABELS`,
plus a cohort-aware loader (URL `?cohort=nz-bush`). Demonstrates
the engine generalises to non-UK species.
**~1 day work** — entirely parameter selection + cohort
plumbing.

**v0.75 — engine-quality polish that benefits both cohorts**:
log-normal gap sampling (§6.2), per-species partial gains (§6.1).
**~half-day** beyond v0.5. Improves UK validation metrics too.

**v1.0 — adequate NZ cohort**: above + tūī with mechanical
syllables (§6.3) + kererū wing-beats via special-case
`flight-event` template (§6.4 option b). Five species.
Recognisable as NZ chorus to a NZer. **~2 days work** beyond v0.75.

**v2** (post-validation, if regional cohorts prove valuable as
research instrument): generalised non-vocal-event schema (§6.4
option c), regional-dialect parameterisation (korimako varies
materially by region), additional NZ species (ruru, tīeke, kākā),
additional regions (Australian bush, North American backyard,
Mediterranean scrub).

The recommended sequence is v0.5 → v0.75 → v1.0, gated on each
step producing audibly reasonable output. **v0.5 is the cheap
probe**: if korimako-pīwakawaka-riroriro played through the
existing engine sounds nothing like NZ bush even with correct
parameters, that itself is information about how much
species-specific synthesis detail matters. The decision to
proceed past v0.5 should depend on the v0.5 listening test, not
on a pre-commitment to ship the full cohort.

---

## 8. Research hooks

This document and the eventual cohort implementation feed two
distinct research uses:

**(a) Familiarity-vs-novelty A/B** — the original motivating
question. Listeners in known regions hear their familiar
cohort vs an unfamiliar one; outcome measures HRV + self-report.
NZ-vs-UK is a maximally-distinct contrast; ideal for
methodological clarity. Requires Phase 1 self-experiment results
to motivate doing this at scale.

**(b) Engine-architecture validation** — does the
species-template architecture handle NZ acoustic structure
cleanly? §6 lists the gaps; building the NZ cohort exercises
each one. If §6.2 mechanical-syllable synthesis works for tūī,
the architecture is more general than its current UK-only
implementation suggests. If it doesn't — if mechanical-vocal
species require a fundamentally different generator family —
that's information about the engine's design boundaries.

Both uses justify the build, in different ways. (b) is
deliverable in software; (a) requires a research protocol that
the project hasn't yet committed to. Build for (b) now if you
build at all; (a) follows when the empirical work calls for it.
