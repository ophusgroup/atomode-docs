# Relaxation History

View the loss convergence from `generate()` or `shell_relax()`:

```python
cell.plot_shell_relax()
```

Returns a matplotlib figure showing:

- **Total loss** (sum of component losses)
- **Best loss** (running minimum)
- **Bond loss** (mean squared deviation from target bond distance)
- **Angle loss** (mean squared deviation from target bond angle)
- **Repulsion loss** (overlap and non-bonded clearance violations per atom)

## Parameters

```python
cell.plot_shell_relax(log_y=False)
```

- `log_y`: if `True`, use a log scale for the y-axis (useful when loss spans many orders of magnitude).

## Accessing raw history

The history arrays are stored on the supercell:

```python
hist = cell.shell_relax_history
hist["step"]              # step index
hist["loss"]              # total loss per step
hist["best_loss"]
hist["bond_loss"]
hist["angle_loss"]
hist["repulsion_loss"]
```
