# Supercell

The central class.  Constructs a periodic simulation cell from a
reference crystal and provides the full disorder-generation pipeline
(Voronoi grain build → optional orientation refinement → FIRE-style
relaxation), measurement, visualisation, and HTML-export helpers.

```{eval-rst}
.. currentmodule:: tricor

.. autoclass:: Supercell
   :no-index:
   :show-inheritance:

   .. rubric:: Construction
   .. automethod:: from_atoms

   .. rubric:: Generation
   .. automethod:: generate

   .. rubric:: Orientation refinement
   .. automethod:: refine_initial_orientations
   .. automethod:: refine_grains
   .. automethod:: refine_grains_coarse_to_fine

   .. rubric:: Relaxation
   .. automethod:: shell_relax
   .. automethod:: bond_relax
   .. automethod:: enforce_hard_core
   .. automethod:: thermal_relax
   .. automethod:: monte_carlo

   .. rubric:: Measurement
   .. automethod:: measure_g3
   .. automethod:: sync_g3

   .. rubric:: Inline visualisation (Jupyter)
   .. automethod:: view_structure
   .. automethod:: plot_structure
   .. automethod:: plot_g2
   .. automethod:: plot_g3
   .. automethod:: plot_g3_compare
   .. automethod:: plot_shell_relax
   .. automethod:: plot_thermal_relax
   .. automethod:: plot_thermal_before_after
   .. automethod:: plot_monte_carlo

   .. rubric:: HTML export
   .. automethod:: export_trajectory_html
   .. automethod:: export_g3_html
   .. automethod:: export_g2_html

   .. rubric:: Class attributes
   .. autoattribute:: PRESETS
```

## Presets

Ready-to-use parameter dictionaries available as `Supercell.PRESETS`.
See the
[silicon preset summary](../examples/silicon/index.md#preset-summary)
for the per-regime values used in the static examples.
