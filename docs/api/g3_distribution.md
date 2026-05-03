# G3Distribution

Stand-alone three-body distribution measurer / target builder.
Most users will use {meth}`tricor.Supercell.measure_g3` rather than
constructing this directly; it's exposed here for users who need
finer control over the histogram axes or who want to compute g3
against a non-cell ASE atoms object.

```{eval-rst}
.. currentmodule:: tricor

.. autoclass:: G3Distribution
   :no-index:
   :show-inheritance:

   .. rubric:: Measurement
   .. automethod:: measure_g3

   .. rubric:: Target construction
   .. automethod:: target_g3

   .. rubric:: Inline visualisation
   .. automethod:: plot_g3
```
