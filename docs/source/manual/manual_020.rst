===================
Beamline components
===================

Reference inventory of the physical hardware that makes up 32-ID, walked
from the source to the detector. Each component is listed once, with the
fields needed to drive it (Family / role / intrinsic specs) and the
fields needed to reason about how it moves relative to everything else
(what it is mounted on, what rides on top of it).

This page is the source of truth for the beamline as an assembly. It
follows the same style as the 2-BM ``item_020`` beamline-components
inventory.

.. note::

   "Mounted on" captures the kinematic chain, distinct from compositional
   ownership. A stage mounted on the rotary co-rotates with it; the same
   stage mounted under the rotary translates the rotation axis in lab
   coordinates. Alignment, error propagation, and limit-handling all
   depend on which is which.


Coded aperture (Jena NV200D piezo)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   These are the **same two physical controllers and actuator**
   previously operated at 2-BM (see the 2-BM ``item_020`` beamline
   components page). They were relocated to 32-ID and re-addressed on the
   32-ID private subnet. Axis identity is fixed by controller **MAC
   address** (unchanged by the move), not by IP: the MAC-to-axis binding
   is the same as at 2-BM.

:Role: Beam-shaping coded aperture mounted in the beam upstream of the
   sample. The aperture is stepped through a list of (X, Y) piezo
   positions during a tomography fly-scan to produce randomised /
   dithered sampling for compressive-sensing imaging reconstructions.
:Family: (Pending — neither Camera nor Stage in the traditional
   sense; the mask itself is a beam-path optical element with its
   own positioning piezo; the eventual Family choice for the
   mask is a separate decision from the piezo controller below.)
:cora Asset: ``CodedApertureFineDrive`` (piezo-controller Asset). Family:
   ``MotionController``. Inherited from the 2-BM registration
   (operator-confirmed 2026-06-19); ``SampleFineDrive`` was an earlier
   provisional placeholder and is wrong — the device does not move the
   sample.
:Hutch: 32-ID (TBD — confirm which 32-ID hutch the aperture is installed
   in)
:z position: TBD (fill in from the 32-ID beamline reference table once
   the aperture is positioned in the beam path)
:Hardware (controllers): **Two** Piezosystem Jena **NV200D/NET**
   controllers, one per piezo axis (not a single dual-channel
   controller). Each is Ethernet-attached and addressed via the
   vendor's Telnet interface on port 23 ("NV200/D NET>" prompt).
   Axis is bound to the MAC address (same as 2-BM); the 32-ID IPs and
   hostnames are new:

   ====  ===========================  ================  ============  =====================
   Axis  Hostname                     Controller IP     Vendor model  MAC address
   ====  ===========================  ================  ============  =====================
   X     ``piexo3.xray.aps.anl.gov``  ``10.54.102.8``   NV200D/NET    ``00-80-A3-6F-BD-6E``
   Y     ``piexo4.xray.aps.anl.gov``  ``10.54.102.46``  NV200D/NET    ``00-80-A3-6F-BD-64``
   ====  ===========================  ================  ============  =====================

   The axis↔MAC binding is the source of truth. Verify which MAC answers
   at each IP (``arp -a`` after ``ping``, or the Lantronix XPort web
   page) if the hostname-to-axis assignment is ever in doubt.

   Vendor datasheet: `NV200D-Datasheet.pdf
   <https://www.piezosystem.com/wp-content/uploads/2023/07/NV200D-Datasheet.pdf>`__.

   NOT the NV100D (which lacks the external trigger mode required
   for tomoscan fly-scan integration).
:Actuator: Piezosystem Jena XY flexure stage,
   **nanoSXY 120 CAP**, part number **T-223-06D** (the "D" suffix
   denotes the digital interface variant). Drawing: `nanoSXY-120-CAP
   <https://www.piezosystem.com/wp-content/uploads/2022/04/nanoSXY-120-CAP-Part-Drawing.pdf>`__
   (rev.01, Feb 2019). Key dimensions:

   .. list-table::
      :header-rows: 1
      :widths: 35 65

      * - Property
        - Value
      * - Travel per axis (nominal)
        - 120 µm
      * - Travel per axis (closed-loop)
        - 100 µm
      * - Clear aperture
        - Ø 12.5 mm (centred)
      * - Outer footprint
        - 82 × 79 × 30 mm
      * - Mounting
        - 4× M3 tapped + 4× Ø3 G7 reamed dowel holes (symmetric, on
          both sides); 32 mm / 54 mm / 60 mm hole-pattern centres
      * - Standard cable length
        - 1600 mm (voltage + sensor cables)
      * - Feedback
        - Capacitive (the ``CAP`` in the model)

   The clear aperture is what the coded-aperture mask itself is
   mounted into; the X / Y piezo motion moves the mask within the
   beam.
:Device configuration: Both controllers must be set to **Xon/Xoff**
   (software) flow control via the Lantronix XPort web interface for the
   EPICS support to work correctly.
:IOC: None deployed at 32-ID as of the relocation (the 2-BM deployment
   ran a ``JenaNV200D`` IOC on ``arcturus``). The triggered-step script
   talks to the controllers directly over Telnet; if an EPICS IOC is
   later added it must be stopped while the script runs.
:FPGA trigger: The FPGA sends a TTL pulse to the NV200D **TRG IN**
   connector (pin 3 of the I/O D-Sub, 0/3.3–5 V) to step to the next
   position during the camera readout interval. Each rising edge advances
   the actuator to the next buffered position. FPGA output channels and
   the softGlue GateDelay PVs are 32-ID-specific — TBD (at 2-BM the X/Y
   cables went to FPGA out3/out2 with delay PVs
   ``2bmbMZ1:SG:GateDly-3_DLY`` / ``-2_DLY``).
:Programming procedure: Triggered-step buffer programming. Up to **1024
   positions** (onboard arbitrary-waveform-generator buffer maximum) are
   pre-loaded into each controller; the default is 256 per axis.
   Implementation ported into ``32id-procedures``,
   `procedures/nv200_trigger_step.py
   <https://github.com/xray-imaging/32id-procedures/blob/main/procedures/nv200_trigger_step.py>`__
   (official `nv200 Python library
   <https://pypi.org/project/nv200/>`__-based; connects to both
   controllers concurrently via ``asyncio``). The two controller IPs
   are already set to the 32-ID addresses above.

   Arguments: ``--n N`` (1 ≤ N ≤ 1024, default 256) and ``--random``
   (uniform sampling from the 0–100 µm stroke for compressive-sensing
   dithered sampling; default is evenly-spaced ``numpy.linspace``).
   ``--random`` is the operational mode for compressive-sensing
   reconstructions. After each generation the positions are saved to
   ``positions_x.txt`` / ``positions_y.txt`` in the current working
   directory as a per-Run provenance record.

   Operational constraint: each controller only accepts **one Telnet
   connection at a time**, so the EPICS IOC must be stopped before
   running the script (and restarted afterwards). Buffered positions live
   in controller RAM and are lost on power cycle unless persisted to
   EEPROM via the library's ``save_to_eeprom()``.

.. note::

   **Preconditions for the triggered-step run** (adapted from the 2-BM
   procedure): the dedicated ``nv200`` conda env is active
   (``conda activate nv200``); both controllers are reachable
   (``ping 10.54.102.8`` and ``ping 10.54.102.46``); and the
   coded-aperture stage is mechanically aligned so the 0–100 µm stroke
   maps to sensible aperture positions in the beam. (No ``JenaNV200D``
   IOC is deployed at 32-ID, so there is no IOC to stop.)
