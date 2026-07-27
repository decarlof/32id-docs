==========
Procedures
==========

Structured, cora-consumable recipes for operations on 32-ID hardware.

Each page in this section documents one procedure end-to-end:
preconditions, typed parameters, atomic steps, postconditions, and
known failure modes. The structure is deliberately rigid so that
every page maps cleanly onto a cora ``Method`` definition (see
`cora <https://github.com/xmap/cora>`__: ``Method.parameters_schema``,
``Plan.wiring``, the ``Procedure`` BC).

For the underlying hardware (IPs, intrinsic specs, kinematic chain),
see :doc:`manual/manual_020`.


Current procedures
==================

- :doc:`procedures/item_013` —
  ``nv200_trigger_step``. Loads the per-axis coded-aperture
  position list (default 256, max 1024 positions per axis) into
  both Piezosystem Jena NV200D/NET controllers via Telnet and
  arms them so each rising edge on TRG IN advances to the next
  position in the buffer. ``--random`` selects compressive-sensing
  dithered sampling (the current operational mode); ``--linspace``
  (default) gives an evenly-spaced raster. Run once at session
  setup or whenever the random list needs regenerating;
  controllers then drive themselves frame-by-frame from the FPGA
  trigger for the rest of the session. Targets the two
  ``CodedApertureFineDrive_X`` / ``_Y`` Assets and the coded-
  aperture XY flexure stage on the cora side.


.. toctree::
   :glob:
   :maxdepth: 1
   :hidden:

   procedures/item*
