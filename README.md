# scare-deer

Using AI to scare deer so they don't eat my girlfriend's flowers.

A DIY wildlife camera that watches the garden at our country house, detects deer using object detection, and (eventually) scares them off before the flowers become a salad bar.

<!-- TODO: Add a photo or short gif here -->

## Why

Deer kept eating the flowers. Commercial deterrents are dumb — motion sensors trigger on everything (cats, birds, wind). A camera that can tell *deer* apart from everything else only reacts when it should. It's also a fun excuse to run a computer vision model against a real, uncontrolled environment instead of a benchmark dataset.

## How it works

```
camera capture  →  deer detection (YOLO)  →  deterrence trigger
```

1. **Capture** — the camera periodically captures frames of the garden. <!-- TODO: motion-triggered or interval? what resolution/fps? -->
2. **Detect** — frames are run through a YOLO object detection model to classify whether a deer is present. <!-- TODO: which YOLO version/variant, pretrained on COCO or fine-tuned? confidence threshold? -->
3. **Deter** — on a positive detection, the system triggers a deterrent. <!-- TODO: what's the plan/state here — sound, lights, sprinkler? See Status below. -->

## Hardware

- Camera: Raspberry Pi Camera module v2
- Compute: Raspberry Pi 5 Enkortsdator Model B 8 GB 
- Deterrent: `TBD`

## Repository structure

- `camera/` — image capture from the camera
- `analysis/` — detection and analysis of captured frames
- `shared/` — code shared between the camera and analysis components
- `devlog.txt` — running notes on what I tried, what broke, and why

## Status

This is a work in progress. Honest state of things:

- [X] Frame capture from camera <!-- TODO: check off what's actually done -->
- [X] Deer detection with YOLO
- [ ] Detection validated on real footage from the garden
- [ ] Deterrence hardware
- [ ] Fully automated capture → detect → deter loop

<!-- TODO: one or two sentences on results so far, even informal: "Detection works on daytime footage; night frames are still unreliable" is exactly the kind of honest detail that makes this credible. -->

## Running it

<!-- TODO: minimal instructions, e.g.: -->
```bash
pip install -r requirements.txt   # TODO: add a requirements.txt if there isn't one
python camera/main.py             # TODO: actual entry points
```

## Roadmap

<!-- TODO: pick the real ones -->
- Fine-tune the model on footage from this specific garden
- Night-time detection (IR?)
- Close the loop: automatic deterrence on detection
- Stats over time: when do the deer actually show up?
