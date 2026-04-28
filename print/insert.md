# Participant insert

The card / leaflet that ships with each device. This is the only
sustained piece of writing the participant will read from the
project, so it has to do real work:

1. **Frame what the device is** — clearly enough that they know it's
   not a sleep machine, not a sleep aid, not a medical device.
2. **Set expectations** — what they will and won't experience, so
   they don't either over-attribute effects to the device or get
   disappointed when nothing dramatic happens.
3. **Obtain informed consent** for participation — what data is
   collected, how it's used, withdrawal rights.
4. **Route to the survey** — the QR code and the prompt to actually
   complete it.
5. **Provide minimal operating instructions** — power, volume,
   what to do if it stops working.

Below: copy for a folded A5 leaflet (4 panels: front, two interior,
back). Set in a serif typeface that matches the project landing page
(Fraunces if licensing permits, otherwise EB Garamond / Crimson Pro).
Cream paper, dark ink, sage accent. Same restrained register as the
website — quiet authority, honest about uncertainty, treating the
participant as a thoughtful adult.

---

## PANEL 1 — Front cover

```
              ┌─────────────────┐
              │                 │
              │   Sentinels     │
              │                 │
              │   ──♪──         │
              │                 │
              │                 │
              └─────────────────┘

      A small device, a quiet study,
      and a question about birdsong.

      —

      Thank you for taking part.
```

## PANEL 2 — Interior left: What this is

```
What this is

You've been given a small speaker that plays a recorded soundscape —
a temperate dawn chorus, mostly birdsong, recorded in the UK. It is
deliberately quiet, designed to be heard at roughly the volume of a
nearby conversation, and to sit in the background of your working day.

The device plays a single audio loop continuously while powered on.
There is no app, no wireless connection, no microphone, no recording.
It does one thing.

What we're trying to find out

There is a small but reasonable body of research suggesting that
recorded birdsong can measurably reduce anxiety and improve mood,
even in people who don't otherwise spend much time around nature.
Most of this research has been done in laboratory conditions, with
short exposures. Almost none of it has tested whether the effect
survives the boring reality of an ordinary working day.

This study is asking that question. Your participation — wearing the
device on your desk, going about your usual work, and answering a
short weekly survey — is what makes the answer possible.

—

What this isn't

This device is not a medical device. It does not treat, diagnose,
or cure anything. It is not a sleep aid. It will not change your
life. It might do nothing at all — that's part of what we're
trying to find out, and a "nothing" result is as scientifically
useful as a positive one.

If at any point you find the device irritating, distracting, or
unwelcome — switch it off. There is no expectation that you keep
it running. The data that "I switched it off after two days because
it bothered me" is itself interesting and worth telling us about.
```

## PANEL 3 — Interior right: How to use it / Survey

```
How to use it

→  Plug the device into a USB power source on your desk.
   Audio begins automatically.

→  The volume control is on the [TOP / SIDE / FRONT — confirm
   from device]. Set it so the soundscape is audible but not
   prominent — quieter than your typing, quieter than nearby
   conversation. If you find yourself listening to it, it's
   too loud.

→  Switch off when you leave the office or finish for the day.
   It's a desk companion, not a constant presence.

→  If the audio stops, won't start, or sounds wrong, please
   email [project email] — don't try to open the device or
   change the audio.

—

The survey

[ QR CODE ]

Please scan this code now to register your participation. It will
take you to a short form (~3 minutes) confirming consent and
collecting baseline information.

After that, we'll send you a brief survey at the end of each week
for [N] weeks. Each weekly survey takes about 5 minutes.

If you'd rather not scan, the form is at:
sentinels.[domain]/[study-id]
```

## PANEL 4 — Back cover: Consent, contact, attribution

```
Your participation is voluntary

You can withdraw at any time, with no consequences and no need
to give a reason. Just stop using the device and stop responding
to the survey, or email us to say so.

What we collect

→  Your survey answers (questions about mood, perceived stress,
   sleep, and your experience of using the device).
→  Your weekly compliance estimate ("approximately how many hours
   did you have it running?").

We do not collect:

→  Audio of any kind. The device has no microphone.
→  Your location, browsing, calendar, or any other passive data.
→  Identifying information beyond what you provide on the
   consent form. Survey responses are linked only by a
   participant ID.

What we do with the data

Aggregated, anonymised results will be published openly —
including null results — at github.com/christopherdebeer/sentinels.
We will not share individual responses with anyone.

Contact

[ project email ]
[ project lead name ]
[ institutional affiliation, if any ]

—

Audio: "Dawn Chorus Birdsong" by squashy555, via Freesound (CC0).
Recorded in the UK, May 2021.

This study has not been reviewed by an external ethics committee.
It is conducted as personal-research and the data will be
treated accordingly. If you have concerns about how the study
is being run, please raise them at the contact address above.
```

---

## Design notes

**Format.** A5 folded landscape (so each panel is A6 portrait when
folded). Folds in half. Or — equally good and cheaper — A6 single
sheet, double-sided: front + study explanation on one side, how-to
+ consent + QR on the other.

**Paper.** A 200–250gsm uncoated stock with a slight cream tone.
Avoid glossy. The whole project is about quiet sensory presence;
the leaflet's haptics should match.

**Type.** Fraunces is the project face. If commercial licensing
is awkward at print volumes, EB Garamond or Crimson Pro are
near-equivalent open-source fallbacks. JetBrains Mono for any
small technical labels (the URL, the participant ID).

**Colour.** Black ink for body. One spot colour — a deep moss
green (~#404e35) — for the project name, the section dividers,
and the QR code frame. Avoid printing the QR code itself in a
non-black colour; scanners handle pure black-on-white best.

**QR code.** Generated at sufficient resolution that it scans
reliably from 30cm. Use error-correction level Q or H so that
a small print imperfection or coffee stain doesn't kill it.
Test scan it from at least three phones before printing.

**Survey URL fallback.** Print the URL underneath the QR code
in a slightly smaller size. Some participants won't scan QR codes
on principle; some will be on devices without cameras.

**Per-device participant ID.** The participant ID is the
mechanism that lets us match a survey response to a device. Each
device's leaflet should have a unique ID printed on it (e.g.
"Participant ID: SNT-042"). Either pre-print as a batch with
sequential IDs, or hand-add with a stamp before distribution.
The QR code can encode this ID as a URL parameter so the survey
auto-fills it.

**Things deliberately not on the leaflet:**

- The full hypothesis with neuroscience. Too long, too clinical,
  primes the participant's expectations. The leaflet says "we're
  testing whether birdsong affects mood at work" because that's
  the honest minimum.
- "Researchers say..." rhetoric. Cite the literature on the
  project website if curious participants want to follow up;
  don't put it on the leaflet, where it functions as advertising.
- Any claim that the device works. The whole point is that we
  don't know.

## Production notes

For a 50-unit pilot, online printing services like Moo, Stationers,
or local print shops can produce these as a short run for £50-100
total. Avoid drop-shipping the printing on the device packaging
itself — the printing on cheap white-label hardware is usually
silkscreen at low resolution and won't render small text well.
Better to keep the device unbranded and let the leaflet carry the
project identity.

If you do silkscreen the device — for production runs above 100
units — keep it minimal: project name, URL, and a small icon. The
leaflet does the heavy lifting.

## Survey platform

Out of scope for this document, but worth flagging: the survey QR
code needs to point somewhere. Options, in order of increasing
effort and decreasing dependency:

1. **Google Forms.** Free, instant, but Google-hosted (some
   participants will baulk).
2. **Microsoft Forms.** Same shape, less Google.
3. **Tally / Typeform / Formspark.** Cleaner aesthetic, free
   tier suffices for 50–200 responses.
4. **Self-hosted on the project Val.town.** Best fit with the
   rest of the project's stack, gives full control over data and
   privacy. Probably 1–2 days of work. Worth it if Phase 0 expands
   to Phase 1.

For Phase 0 with 2-unit-sample-then-50-unit-pilot, options 3 or 4.
The choice is essentially aesthetic and about how much of the
project's identity you want to extend into the survey itself.
