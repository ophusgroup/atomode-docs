# Rotating Movie

Export a 360-degree rotating movie of the supercell.

## MP4 (recommended)

Requires `ffmpeg` on the system path.

```python
cell.plot_structure(
    output='structure.mp4',
    fps=60,
    duration=6.0,
)
```

## GIF fallback

Pure Python, no ffmpeg needed.

```python
cell.plot_structure(
    output='structure.gif',
    fps=30,
    duration=4.0,
)
```

## Full options

```python
cell.plot_structure(
    output='structure.mp4',
    width=1024,
    height=1024,
    fps=60,
    duration=6.0,
    elevation=15.0,
    atom_size=10.0,
    colormap='Reds',
    background='white',
)
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `output` | required | Path to `.mp4` or `.gif` output. |
| `width`, `height` | 1024, 1024 | Pixel dimensions. |
| `fps` | 60 | Frames per second. |
| `duration` | 6.0 | Seconds (one full 360 rotation). |
| `elevation` | 15.0 | Camera elevation in degrees. |
| `atom_size` | 10.0 | Marker size for atoms. |
| `colormap` | `"Reds"` | Matplotlib colormap for depth-coloured bonds. |
| `background` | `"white"` | Figure background colour. |
