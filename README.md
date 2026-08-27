# Dunhuang Dance Robot Motion Dataset

Real robot-executable motion data for a three-robot Dunhuang (敦煌) dance performance, recorded on
a Hiwonder Tonybot humanoid robot.

## Overview

- **Platform**: Hiwonder Tonybot, 16 high-voltage bus-servo channels (IDs 1-16), raw positions 0-1000.
- **Content**: 13 sequences — 11 dance sequences covering the three dancer roles of a three-robot
  performance (right dancer, left dancer, center main dancer) plus 2 basic locomotion actions.
- **Format**: one CSV per sequence; each row is `timestamp_ms` (cumulative, derived from the
  choreographer-defined per-frame execution time) followed by the 16 servo positions.
- **Final 3-robot set**: `right_dancer_take_15`, `left_dancer_take_30`, `center_main_take_final`.
- **Choreography development**: the additional takes per role document the choreography's evolution
  (near-identical early versions followed by deliberate revisions).

## Repository structure

| File | Description |
|------|-------------|
| `right_dancer_take_11..15.csv` | right dancer, 5 takes (final: take 15) |
| `left_dancer_take_29.csv`, `left_dancer_take_30.csv`, `left_dancer_take_left1.csv`, `left_dancer_take_leftside.csv` | left dancer, 4 takes (final: take 30) |
| `center_main_take_old.csv`, `center_main_take_final.csv` | center main dancer, 2 versions |
| `basic_back_lean.csv`, `basic_walk_2steps.csv` | basic locomotion actions |
| `manifest.csv` | per-sequence metadata (role, take, frames, duration, description) |
| `convert_rob.py` | converter from raw Hiwonder action files (.rob, ACT-40 format) to CSV |
| `LICENSE` | non-commercial research license |

## CSV format

```
timestamp_ms, ch01, ch02, ..., ch16
0,           500,  500,  ..., 295
30000,       500,  500,  ..., 295
...
```

- `timestamp_ms`: cumulative time in milliseconds (per-frame execution time is choreographer-defined).
- `ch01`-`ch16`: raw servo positions in 0-1000 (full mechanical travel).

## Convert raw action files

The raw recordings are Hiwonder action files (.rob, ACT-40 format). The layout of a frame
(248 bytes at stride 248, starting at byte offset 20) is: 4-byte reserved field, then 16 channels
of 6 bytes (little-endian position u16 + padding), and the frame execution time in ms at offset 244.
See `convert_rob.py` for the complete converter and validation checks.

```bash
python convert_rob.py   # reads .rob files from a source dir, writes the CSVs in this repo
```

## Citation

If you use this dataset, please cite:

> (Author). A Dataset and Robotic Performance System for Dunhuang Dance: Motion Specifications,
> Data Construction, and Analysis. CCAC 2026. Springer CCIS. (To appear)

## License

Non-commercial research use only. See `LICENSE`.
