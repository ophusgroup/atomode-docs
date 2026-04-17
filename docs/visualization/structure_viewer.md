# 3D Structure Viewer

Interactive WebGL viewer in Jupyter, built with Three.js.

```python
cell.view_structure()
```

## Controls

- **Drag** to rotate, **scroll** to zoom, **right-click drag** to pan.
- **Atom size** slider: scales sphere radii.
- **Bond radius** slider: cylinder thickness.
- **Bond cutoff** slider: recomputes bonds live using ASE neighbor_list.
- **Bond type checkboxes**: toggle per species-pair (e.g. Si-Si, Si-C, C-C).
- **Slab x/y/z** dual-range sliders: clip the view to a fractional coordinate range.
- **Show/hide** cell outline and bonds.

## Custom initial settings

```python
cell.view_structure(
    atom_scale=0.6,
    bond_cutoff=3.0,
    slab_z=(0.0, 0.5),  # show bottom half only
)
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `atom_scale` | 0.4 | Sphere radius scale factor. |
| `bond_cutoff` | from `shell_target` | Maximum bond length (Angstrom). |
| `bond_radius` | 0.08 | Cylinder radius for bonds (Angstrom). |
| `show_bonds` | True | Render bonds. |
| `show_cell` | True | Render cell outline. |
| `slab_x`, `slab_y`, `slab_z` | (0, 1) | Fractional range to display. |

Colours come from ASE's jmol colour scheme.
