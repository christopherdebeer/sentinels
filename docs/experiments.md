# Experiments

Anything that calls itself a wellness device and ships without a falsification plan is, by default, a placebo. The whole point of this project is to actually find out whether the device does what we hope. This document lays out the experimental protocols — from informal n=1 self-tests through to a small pre-registered pilot.

The methodology has to take placebo, novelty, and reporting bias seriously. People who buy a £20 chest pendant claiming nervous-system benefits will report nervous-system benefits. The interesting question is whether the effect survives a design that makes it hard to be self-fulfilling.

## Protocol 1: n=1 self-experiment (informal but honest)

Purpose: detect a self-perceptible effect, if one exists. Decide whether the project is worth pursuing further.

### Design

- **Duration:** 4 weeks
- **Conditions:** Device-on days vs. device-off days, randomised in blocks of 1 week (Latin square over 4 weeks gives balanced sequence: AB BA BA AB or similar).
- **Allocation:** A simple cron job assigns conditions in advance for the full 4 weeks; the schedule is sealed. The wearer doesn't know the next day's condition until that morning, and ideally not even then — the device is set up to autonomously activate or remain silent according to schedule.
- **Daily measurements:**
  - Morning and evening **STAI-state** (State-Trait Anxiety Inventory — short form, ~6 items)
  - Morning and evening **PANAS** (Positive and Negative Affect Schedule — short form, 10 items)
  - **HRV** (RMSSD) from existing wearable, morning resting measurement
  - One free-text journal entry per day (post-hoc qualitative coding)
- **Pre-registered analysis:** paired Wilcoxon on daily mean of each scale, on/off. Effect direction predicted in advance. Primary outcome: STAI-S evening score.

### What this can and cannot tell us

This protocol can tell us:
- Whether *I* perceive a difference, in a way that's not entirely contaminated by knowing-which-day-it-is.
- Whether HRV moves measurably (a more objective signal).
- What qualitative experience accompanies the device — the journal entries are likely to be the most informative output.

This protocol cannot tell us:
- Whether the effect generalises beyond me. (It might be entirely an effect of paying attention to one's environment, which the device merely cues.)
- Whether the effect would survive a true blind. The wearer always knows the condition (they hear the device or they don't); only the *schedule* is unknown.

A null result here is very informative — it would mean the effect, if real, isn't large enough for *me* to notice in 4 weeks. A positive result is suggestive but not yet evidence — it justifies the next protocol, not a product launch.

## Protocol 2: Small pilot study (n ≈ 20–30, within-subject crossover)

Purpose: estimate effect size, evaluate practical usability, generate the data needed to power a real RCT.

### Design

- **Recruitment:** healthy adults working in office or home-office environments, voluntary, no compensation beyond the device itself.
- **Crossover structure:** 2-week active condition, 2-week sham condition (a device that is identical in every way except that the speaker is electrically muted), randomised order, 1-week washout between.
- **Sham fidelity:** the sham device emits an inaudible signal in the ultrasonic range so its mic-based ambient calibration runs identically and the device behaves identically from outside. Wearer reports compliance ("did you wear it?" log) but isn't told which condition they're in.
- **Outcomes:**
  - **Primary:** STAI-T-Y change scores between conditions (within-subject)
  - **Secondary:** weekly PANAS, perceived stress (PSS-10), sleep quality (PSQI subset)
  - **Objective:** if available, HRV (RMSSD) from any wearable the participant already uses; we will not require a specific device
  - **Behavioural:** simple working-memory probe administered weekly via app (digit-span — same task as Stobbe et al. used)
- **Pre-registration:** OSF or aspredicted.org. Hypotheses, primary outcome, and analysis plan committed before data collection begins. Public link from this repo.

### Why crossover, not parallel groups

Variance in baseline anxiety between people is much larger than the effect we're trying to detect. Within-subject crossover removes that variance and gives us the statistical power that a small N otherwise wouldn't.

### Why a sham device, not a placebo bracelet

Because the device's *behaviour* is the salient thing — clipping to your shirt, having a battery, etc. A sham device that does everything except emit sound is the cleanest control. The risk: participants may be able to tell, even in a quiet room, that the device is not playing audio. We mitigate by:
- Using a very quiet base "active" volume so the difference from sham is subtle
- Including a small set of "blind check" questions in exit interviews to estimate participants' guessing accuracy
- If guessing accuracy is high (>70%), reporting that limitation prominently and considering it a partial confound

### What this can and cannot tell us

A pilot with N=20 is not powered to detect small effects with confidence. What it *can* do:
- Estimate effect size to power a properly-sized RCT
- Identify dropout reasons and usability friction
- Identify side-effects we didn't anticipate
- Test the sham fidelity (do participants guess condition correctly?)
- Surface qualitative experience that would inform v2 of the device

Any positive pilot result should be reported with effect-size confidence intervals that include null effects, and treated as *encouraging the next study*, not as evidence of efficacy.

## Protocol 3: Properly-powered RCT (out of scope for now)

If Protocol 2 produces an encouraging effect-size estimate, the next step is a pre-registered, properly-powered, ideally externally-conducted RCT. This is out of scope for this repository in its current form — it is what success at the pilot stage would justify investing in.

A sketch of what it would look like:
- ~150–200 participants, parallel-group RCT
- 4-week intervention
- Pre-registered primary outcome (likely STAI-T change at 4 weeks)
- Active sham control
- Blinding of participants and outcome assessors
- Independent statistical pre-analysis plan
- Conducted with a research collaborator (university partnership ideal)

## Ablations worth running (within Protocol 2)

If the pilot shows any signal at all, the high-value follow-ups are:

1. **Volume sensitivity.** Run sub-arms at 45, 50, 55 dB(A) target SPL. Yu et al. 2025 predicts a peak around 45–50; we should be able to see this.
2. **Procedural vs. looped.** Same audio content delivered as a 30-minute loop vs. procedural assembly. This tests the "habituation" hypothesis directly.
3. **Bird-aware mode on/off.** Probably too subtle to detect at N=20 but worth attempting.
4. **Pendant vs. open-ear.** Different physical form factors, same audio. Tests the "sound in the world vs. in your head" hypothesis.

Each of these would need its own arm and increases N requirements; better to do them sequentially as separate sub-studies.

## Things that would falsify the project

To be honest about what would make this project wrong rather than just unproven:

- **Pilot null with reasonable power.** If a well-controlled pilot with adequate sample size produces a confidence interval tightly around zero, the device probably isn't doing the thing.
- **Effect dependent entirely on novelty.** If the within-subject effect disappears after week 1, we're measuring "people respond to a new thing", not the hypothesised mechanism.
- **Effect equal to sham device that emits *anything* mildly pleasant** (e.g., a small fountain sound). If birdsong-specific design isn't necessary and any nature-coded ambient sound works equally well, the design constraints in this repo are over-specified and the project should pivot.
- **Effect inverts above a chronic-exposure threshold** that's lower than expected. If wearing the device 8h/day for 2 weeks makes things worse, that's a different (and worse) shape of failure than "no effect" and would need careful handling.

If any of these come back, the right response is a write-up explaining what we found and what we got wrong, not a pivot to a new wellness narrative.

## Ethics & consent

- For Protocol 1 (self-experiment), no formal review needed; results posted as personal write-up.
- For Protocol 2 (pilot), needs proper informed consent and ideally light institutional review. If conducted as a personal-research project, a written consent form, a clear "you can withdraw at any time", and a pre-shared protocol are the minimum.
- All participants must be informed up front that this is **research**, not a product, and that no efficacy claims are being made.
- Data minimisation: collect what the protocol needs, nothing more. No raw audio from the mic ever leaves the device; only summary SPL features.

## What gets published

Regardless of result:

- The pre-registration links
- The full anonymised dataset (with participant consent)
- The analysis code
- A write-up — including null results — posted publicly
- A note in this repository pointing to all of the above

Negative results are scientifically valuable and almost never published. This project commits in advance to publishing whatever we find.
