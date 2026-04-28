# Looping recipe

How to take a 5–30 minute field recording and produce a seamlessly
looping audio file suitable for unattended workplace playback.

The loop point is the single most common failure mode in this category.
A clearly audible click, gap, or amplitude jump every N minutes is the
fastest way to break the calming effect — the brain locks onto the
periodicity and starts predicting it. The fix is straightforward: a
crossfade overlap that hides the seam in continuous content rather
than trying to butt-join silence.

Two paths below: a one-line ffmpeg recipe (fastest, scriptable) and an
Audacity workflow (visual, easier to fix problems by hand).

## Constraints to respect

- **Output format must match what the device accepts.** Most
  cheap MP3 players want 16-bit, 44.1 kHz, MP3 CBR (constant
  bitrate) at 128 or 192 kbps. Some are pickier. Test the
  device's preferences before mass-encoding.
- **Filename rules.** Some devices require track001.mp3, some
  hate spaces in filenames, some only read the root directory.
  Check device first; rename last.
- **File size budget.** A 1-hour 192 kbps MP3 is ~85 MB. Even the
  cheapest SD cards can hold dozens of hours, so size isn't the
  constraint — but if the device firmware caps file size (some do
  at 2 GB or 4 GB), check before producing very long files.

## Path A: ffmpeg one-liner (recommended)

Assumes you start with `source.wav` (the downloaded original) and
want a seamless 30-minute MP3 loop.

```bash
# 1. Trim head/tail silence and pick a clean ~30 minute section
ffmpeg -i source.wav \
  -ss 00:00:30 -t 00:30:00 \
  -af "afade=t=in:st=0:d=2,afade=t=out:st=1798:d=2" \
  trimmed.wav

# 2. Cross-overlap the end with the start to hide the loop seam
#    The trick: take 10s from the end, fade it down; take 10s from
#    the start, fade it up; mix them so they overlap. Then prepend
#    the resulting overlap to the middle of the file.
#    Easier in practice via the Audacity recipe below — but for the
#    automation-minded:

ffmpeg -i trimmed.wav -filter_complex "
  [0:a]atrim=start=0:end=1790,asetpts=PTS-STARTPTS[middle];
  [0:a]atrim=start=1790:end=1800,asetpts=PTS-STARTPTS,
       afade=t=out:st=0:d=10[tail];
  [0:a]atrim=start=0:end=10,asetpts=PTS-STARTPTS,
       afade=t=in:st=0:d=10[head];
  [tail][head]amix=inputs=2:duration=longest[crossfade];
  [middle][crossfade]concat=n=2:v=0:a=1
" looped.wav

# 3. Encode to MP3 at the bitrate the device wants
ffmpeg -i looped.wav -codec:a libmp3lame -b:a 192k \
  -ar 44100 -ac 2 sentinels-loop.mp3
```

The result: a 30-minute MP3 where the last 10 seconds and first 10
seconds are *the same content*, crossfaded — so when the device
finishes the file and starts it again, the audio at the loop point
is continuous because it was already continuous in the file.

If your device loops by gaplessly restarting the file, this works.
If your device introduces its own gap between loops (some do — a
~50-200ms silence), no crossfade in the file can fix that; you'd
need a longer single file (60+ minutes) so the gap is rarer, or a
different device.

## Path B: Audacity workflow (recommended if you've never done this)

Audacity is free, cross-platform, and lets you see the waveform
which makes loop-debugging much easier.

1. **Import** `source.wav`. Ctrl+A to select all, then look at the
   waveform. Note any obviously bad sections (foreground voices,
   traffic, dog bark, plane fly-over, prolonged silence).

2. **Trim aggressively.** Select and delete the bad sections. You'd
   rather have 12 minutes of clean recording than 30 minutes that
   includes a single loud van. The brain notices the van.

3. **Find a 5–30 minute clean section.** Mark it with labels (Ctrl+B
   adds a label at the cursor). Aim for a section that starts and
   ends with similar acoustic character — both relatively quiet,
   or both relatively active. Don't end on a bird call cadence — the
   loop will sound like a stuck record.

4. **Set up the crossfade overlap** (this is the key step):
   - Select your chosen section.
   - Edit → Copy.
   - Tracks → Add New → Stereo Track.
   - Paste into the new track at time 0.
   - On the new track, select the *first* 10 seconds.
   - Effect → Fade In.
   - On the *original* track, select the *last* 10 seconds of the
     section.
   - Effect → Fade Out.
   - Move the new (faded-in) track so its start aligns with the
     fade-out region of the original. They now overlap by 10s.
   - Preview by playing across the overlap region; the transition
     should be inaudible. If you can hear a "swell" or "dip", the
     fade curves don't match — try Effect → Crossfade Tracks
     instead which uses an equal-power curve.

5. **Mix down.** Select all, Tracks → Mix → Mix and Render. You
   now have a single track with the crossfade baked in.

6. **Trim to loop boundaries.** Cut the track so it starts at the
   *end* of the fade-in (where the original audio is at full
   amplitude post-crossfade) and ends at the *start* of the fade-out
   (where the original audio is still at full amplitude pre-
   crossfade). The boundaries you trim to are the loop points —
   when the file ends and restarts, those two points connect, and
   they're already continuous content because the fade-in/out
   regions overlapped.

7. **Loop-test.** Tracks → Add New → Stereo Track. Copy your
   trimmed audio. Paste it twice end-to-end. Listen across both
   join points. The second join point is the actual loop test —
   it should be inaudible. If it isn't, the trim boundaries from
   step 6 are wrong; redo with the boundaries shifted.

8. **Export.** File → Export → Export as MP3. Settings:
   - Bit Rate Mode: Constant
   - Quality: 192 kbps
   - Sample Rate: 44100 Hz (set in Project Rate, bottom-left of
     Audacity, before exporting)
   - Channel Mode: Joint Stereo (better than Stereo for spoken
     audio, no real difference for ambient)

## Quality checks before deployment

Before loading the file onto a device that's going to play it for
8 hours a day:

1. **Loop test on the actual hardware.** Don't assume the device
   loops the way the spec implies. Set it playing, leave it for 2
   hours, listen for the seam. If you can hear it, the brain will
   too — even if it's so subtle you barely notice. Subliminal
   periodicity is exactly the kind of thing the hypervigilance
   circuit is good at picking up on.

2. **High-frequency check.** The 1–8 kHz band is the active band.
   If MP3 encoding has rolled off above 6 kHz (often the case at
   128 kbps or below), you're losing the high-frequency content
   that matters most. Check by playing the file through good
   headphones and comparing the *brightness* of the bird calls
   to the original WAV. If the MP3 sounds duller, raise the
   bitrate.

3. **Volume calibration.** Set the device volume to where you
   intend participants to use it. Use a phone dB-meter app at
   1m distance and aim for roughly 45–55 dB(A). If the device's
   minimum volume is already louder than this, it's the wrong
   device. If its maximum is below 45 dB(A) at close range, you
   may need to re-master the audio louder before encoding —
   but be careful, you can't add high-frequency content that
   wasn't there.

## What can go wrong

- **The device adds its own loop gap.** Hardware-level, no fix
  in software. Either accept it (and hope it's short enough not
  to break the effect), use a longer single file, or change device.
- **The MP3 encoder normalises the file.** Some workflows apply
  loudness normalisation by default. If your carefully-crossfaded
  edges get re-normalised, the seam reappears. Disable
  normalisation in the encoder.
- **The device only plays the first 10 seconds repeatedly.** Sounds
  ridiculous but happens — a known firmware bug in cheap MP3 player
  modules where loop-mode actually means restart-on-buffer-flush.
  Test with a long file (5+ minutes minimum) before assuming the
  device plays correctly.
- **Sample rate mismatch.** If the device runs at 22.05 kHz internally
  and you give it a 48 kHz file, it may resample badly, downsample
  noisily, or refuse to play. 16-bit 44.1 kHz is the safest target.
