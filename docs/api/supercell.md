# Supercell

The central class.  Constructs a periodic simulation cell from a
reference crystal, generates disordered structures via Voronoi grains and
spring-network relaxation, and provides visualisation and export helpers.

```{eval-rst}
.. autoclass:: tricor.Supercell
   :members:
      from_atoms,
      generate,
      shell_relax,
      measure_g3,
      plot_g3,
      plot_g3_compare,
      plot_shell_relax,
      view_structure,
      plot_structure,
      export_trajectory_html,
      export_g3_html
   :inherited-members:
   :undoc-members:
```

## Presets

Ready-to-use parameter dictionaries for silicon are available as
`Supercell.PRESETS`.  See the
[silicon preset summary](../examples/silicon/index.md#preset-summary)
for the full table of values.
