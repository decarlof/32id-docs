===================================================
NV200D triggered-step buffer programming
===================================================

Load the per-axis coded-aperture position list into the two
Piezosystem Jena NV200D/NET controllers and arm them so each
rising edge on TRG IN advances to the next position in the buffer.
Run once at session setup (or whenever the random list needs
regenerating); the controllers then drive themselves frame-by-frame
from the FPGA trigger for the rest of the session.

.. note::

   These are the same two controllers and actuator relocated from
   2-BM, re-addressed on the 32-ID private subnet. See
   :doc:`../manual/manual_020` for the hardware inventory (hostnames,
   IPs, MAC-bound axis assignment, actuator specs).


Name
----

``nv200_trigger_step``


Source
------

Three sibling scripts live under
`procedures/ <https://github.com/xray-imaging/32id-procedures/tree/main/procedures>`__
in the ``32id-procedures`` repo. All three share the same core (asyncio
Telnet to both NV200D controllers, position-list generation, waveform-buffer
load, FPGA-trigger arm, clean cleanup on exit) and differ only in the extra
features they layer on top:

- `nv200_trigger_step.py
  <https://github.com/xray-imaging/32id-procedures/blob/main/procedures/nv200_trigger_step.py>`__
  — the base script. Ported from ``2bm-procedures``; only the two controller
  IPs (``10.54.102.8`` / ``10.54.102.46``) differ. Output filenames include
  a ``YYYYMMDD-HHMMSS`` timestamp so successive runs don't overwrite each
  other.
- `nv200_trigger_step_range.py
  <https://github.com/xray-imaging/32id-procedures/blob/main/procedures/nv200_trigger_step_range.py>`__
  — adds a ``--range MAX_UM`` argument that caps the upper end of the
  generated position list, so patterns can span a sub-region of the
  actuator's full 0–100 µm stroke without dropping ``--n``.
- `nv200_trigger_step_tomoscan.py
  <https://github.com/xray-imaging/32id-procedures/blob/main/procedures/nv200_trigger_step_tomoscan.py>`__
  — **recommended for production tomo sessions.** Includes the ``--range``
  argument above and additionally hooks into tomoscan via three EPICS
  subscriptions:

  * on every ``StartScan 0 → 1`` transition the piezos are re-armed at
    index 0 (first camera frame is always at ``positions[0]``);
  * on ``ScanStatus`` becoming ``"Scan complete"`` the piezos are disarmed
    (stray pulses between scans can't advance the buffer);
  * ``ExposureTime`` changes automatically caput a matching delay to
    ``32idMZ1:SG:GateDly-2_DLY`` and ``32idMZ1:SG:GateDly-3_DLY``
    (100 ns per unit, so 0.5 s = 5 000 000).

- **Release notes**: `32id-procedures CHANGELOG
  <https://github.com/xray-imaging/32id-procedures/blob/main/CHANGELOG.md>`__

.. note::

   **Deployment (32-ID).** The procedure runs on ``txmthree`` as user
   ``usertxm``, from the checkout at
   ``~/conda/32id-procedures-decarlof``, under the dedicated ``nv200``
   conda env (Python 3.12). Both controllers are reachable from this
   host.


Devices
-------

- :doc:`../manual/manual_020`: ``CodedApertureFineDrive_X``
  (Piezosystem Jena NV200D/NET, ``piexo3.xray.aps.anl.gov`` at
  ``10.54.102.8``)
- :doc:`../manual/manual_020`: ``CodedApertureFineDrive_Y``
  (Piezosystem Jena NV200D/NET, ``piexo4.xray.aps.anl.gov`` at
  ``10.54.102.46``)
- :doc:`../manual/manual_020`: the coded-aperture XY flexure stage
  itself (Piezosystem Jena ``nanoSXY 120 CAP``, T-223-06D)

.. note::

   As at 2-BM, a ``JenaNV200D`` EPICS IOC is deployed at 32-ID (runs
   on ``txm4`` as ``usertxm`` under procServ + ``screen``; see
   :doc:`../manual/manual_030` for the full IOC operation walk-through).
   Because the NV200D allows only one Telnet connection at a time, the
   IOC must be stopped for the duration of the script and restarted
   when the script exits.


Preconditions
-------------

- **EPICS IOC `JenaNV200D` is stopped.** The NV200D allows only
  one Telnet connection at a time; if the IOC holds the connection,
  the script cannot connect.
- **Network reachable to both controllers.** ``ping 10.54.102.8``
  and ``ping 10.54.102.46`` should both succeed.
- **The `nv200` conda environment is active.** As at 2-BM, the
  script runs under a dedicated ``nv200`` conda env (Python 3.12)
  that has the ``nv200`` + ``numpy`` libraries installed. The
  ``_tomoscan`` variant additionally requires ``pyepics``::

    conda activate nv200

  To recreate it from scratch::

    conda create -n nv200 python=3.12 -y
    conda activate nv200
    pip install nv200 numpy pyepics
- **Coded-aperture stage is mechanically aligned in the beam path.**
  The position list spans the full 0–100 µm closed-loop stroke; if
  the stage is mis-aligned the random walk will produce nonsense
  aperture positions even though the script runs cleanly.
- **Softglue GateDly delays are set for the current exposure time.**
  ``32idMZ1:SG:GateDly-2_DLY`` and ``32idMZ1:SG:GateDly-3_DLY``
  should be set so each per-axis piezo step pulse arrives after the
  camera has finished integrating the frame (typically 5 ms delay
  for a standard exposure — ``DLY = 50000`` in 10 MHz clock cycles).
  See the *Softglue configuration for the coded-aperture fly-scan*
  subsection of the NV200D block in :doc:`../manual/manual_020` for
  the caQtDM screens, the delay math, and the ``UpCntr-3`` /
  ``UpCntr-4`` pulse-count verification recipe. **Not required when
  running the ``_tomoscan`` variant** — that script mirrors
  ``32id:TomoScan:ExposureTime`` into both GateDly PVs automatically.


To run
------

From ``txm4`` as ``usertxm``, activate the dedicated ``nv200``
conda env and change into the ``32id-procedures`` checkout::

    ssh usertxm@txm4
    (base) usertxm@txm4 ~ $ conda activate nv200
    (nv200) usertxm@txm4 ~ $ cd ~/conda/32id-procedures-decarlof/procedures/

Inspect the argument list of each variant with ``-h``.

Base variant::

    (nv200) usertxm@txm4 ~/.../procedures $ python nv200_trigger_step.py -h
    usage: nv200_trigger_step.py [-h] [--random] [--n N]

Range variant — adds ``--range MAX_UM``::

    (nv200) usertxm@txm4 ~/.../procedures $ python nv200_trigger_step_range.py -h
    usage: nv200_trigger_step_range.py [-h] [--random] [--n N] [--range MAX_UM]

Tomoscan variant — adds ``--tomoscan-prefix PREFIX`` on top of the range
variant (default prefix is ``32id:TomoScan:``)::

    (nv200) usertxm@txm4 ~/.../procedures $ python nv200_trigger_step_tomoscan.py -h
    usage: nv200_trigger_step_tomoscan.py [-h] [--random] [--n N]
                                          [--range MAX_UM] [--tomoscan-prefix PREFIX]


Parameters
----------

.. list-table::
   :header-rows: 1
   :widths: 25 20 12 8 35

   * - Argument
     - Type
     - Default
     - Variants
     - Description
   * - ``--n N``
     - integer, 1 ≤ N ≤ 1024
     - 256
     - all
     - Number of positions to load into each controller's waveform
       buffer. 1024 is the NV200D hardware maximum.
   * - ``--random``
     - flag (no value)
     - off
     - all
     - If set, positions are uniformly sampled from the effective
       stroke range (compressive-sensing dithered sampling). If unset,
       positions are evenly spaced (``numpy.linspace``).
   * - ``--range MAX_UM``
     - float, 0 < MAX ≤ 100
     - full stroke
     - ``_range``, ``_tomoscan``
     - Upper limit of the generated position list in µm. Positions
       span ``[actuator_min, MAX_UM]``. Rejected if outside the
       actuator's own reported range.
   * - ``--tomoscan-prefix PREFIX``
     - string
     - ``32id:TomoScan:``
     - ``_tomoscan``
     - PV prefix of the tomoscan instance to monitor. The script
       subscribes to ``<PREFIX>StartScan``, ``<PREFIX>ScanStatus``,
       and ``<PREFIX>ExposureTime``.


Steps
-----

.. list-table::
   :header-rows: 1
   :widths: 5 30 65

   * - #
     - Action
     - Command / call
   * - 1
     - Activate the dedicated conda environment.
     - ``conda activate nv200``
   * - 2
     - Change directory to the ``32id-procedures`` checkout (on
       ``txm4`` as ``usertxm``).
     - ``cd ~/conda/32id-procedures-decarlof/procedures``
   * - 3
     - Run the recommended variant (``_tomoscan``) with the desired
       parameters. Base or ``_range`` variants are also available.
     - ``python nv200_trigger_step_tomoscan.py [--n N] [--random] [--range MAX_UM]``
   * - 4
     - Wait for the three subscription confirmations
       (``StartScan``, ``ScanStatus``, ``ExposureTime``) and the
       "Running. Each rising edge on TRG IN ..." line. The script
       blocks here.
     - watch console output
   * - 5
     - (Optional) verify the saved position files match the
       intended sampling pattern.
     - ``head -5 positions_x_YYYYMMDD-HHMMSS.txt`` (random will
       look random; linspace will be evenly spaced)
   * - 6
     - Run the tomography fly-scans normally. Every ``StartScan``
       re-arms the piezos at index 0 and every ``ScanStatus →
       "Scan complete"`` disarms them; ``ExposureTime`` changes are
       propagated to both GateDly PVs. No operator intervention on
       the script's terminal between scans.
     - operator-side; standard tomoscan acquisition
   * - 7
     - When the session ends, return to the script's terminal and
       press Enter (restores direct command control on both piezos
       and disconnects the tomoscan PV subscriptions).
     - keyboard


Postconditions
--------------

On a successful run:

- Both NV200D controllers have their waveform buffer loaded with
  N positions spanning ``[posmin, MAX_UM]`` (default ``MAX_UM =``
  full 100 µm stroke).
- ``TriggerInFunction = WAVEFORM_STEP`` on both controllers (the
  device-side trigger arms the per-edge step advance).
- ``positions_x_YYYYMMDD-HHMMSS.txt`` and
  ``positions_y_YYYYMMDD-HHMMSS.txt`` saved to the current working
  directory as a per-run provenance record (both files share the
  same timestamp so paired X/Y lists are trivial to identify).
  Successive runs create new files rather than overwriting.
- (``_tomoscan`` variant only) The script prints its three
  subscription lines and issues an initial GateDly caput matching
  the current ``ExposureTime`` value.

After the operator presses Enter and the script exits cleanly:

- Both controllers have ``TriggerInFunction = DISABLED`` and the
  waveform generator stopped (direct command control restored).
- ``pid.set_mode(CLOSED_LOOP)`` re-issued and ``move_to_position(0.0)``
  called on each, so the setpoint source is back to serial and the
  EPICS IOC can drive them immediately (see :doc:`../manual/manual_030`
  for details on this handoff).
- Telnet connections closed; the ``JenaNV200D`` EPICS IOC can be
  restarted to reclaim the connections.
- (``_tomoscan`` variant only) All four EPICS PV subscriptions
  (``StartScan``, ``ScanStatus``, ``ExposureTime``, both ``GateDly``
  writers) are torn down.

(The waveform buffer contents persist in RAM until the controller
is power-cycled; the script's optional ``save_to_eeprom()`` path
can persist the buffer across power cycles if needed.)


Failure modes
-------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Symptom
     - Recovery
   * - Step 3 raises ``ConnectionRefusedError`` / Telnet refused
     - The ``JenaNV200D`` EPICS IOC is still running. Stop it
       (precondition 1) and re-run.
   * - Step 3 raises ``ValueError: position outside actuator
       range``
     - The position list contains values outside 0–100 µm. Should
       only happen if the stroke limits the controller reports
       (``posmin`` / ``posmax``) have been edited; verify with
       ``caget`` after restarting the IOC.
   * - Step 3 raises ``ValueError: Maximum 1024 positions``
     - ``--n`` larger than 1024. Reduce to the device maximum.
   * - Network timeout to one of the IPs
     - Check ``ping 10.54.102.8`` and ``10.54.102.46``. If
       unreachable, check the Piezosystem-Jena-controller-side
       network configuration (Lantronix XPort).
   * - Script runs but tomography acquisitions do not advance the
       piezo positions during fly-scan
     - Two likely causes. **(a)** The FPGA-output-to-NV200D-TRG-IN
       cable mapping may be wrong. Documented mapping:
       X → ``FPGA out2`` → ``32idMZ1:SG:GateDly-2_DLY``, Y →
       ``FPGA out3`` → ``32idMZ1:SG:GateDly-3_DLY`` (see the *FPGA
       trigger* field in the NV200D block of
       :doc:`../manual/manual_020`). Verify the physical coax runs
       at the softGlueZynq patch panel match. **(b)** The GateDly
       block(s) may be dropping pulses. Open ``softGlueZynqAll.adl``
       and watch ``UpCntr-3`` (JenaX) and ``UpCntr-4`` (JenaY)
       during a live scan — both should increment on every camera
       trigger and stay within one count of each other. Drift
       between them (or one stuck at zero) localises the fault to
       that specific trigger path. See the *Softglue configuration
       for the coded-aperture fly-scan / Pulse-count verification*
       subsection in :doc:`../manual/manual_020`.
   * - Script exits cleanly but ``positions_*.txt`` not saved
     - The script must be run from a writable directory. ``cd`` to
       a writable location (step 2) before running.


Notes
-----

- The 1024-position cap is the NV200D's onboard arbitrary-waveform
  generator buffer size, not a beamline-specific limit. 256 positions
  per axis is the operational default.
- ``--random`` is the current operational mode for compressive-
  sensing dithered tomography reconstructions; ``--linspace``
  (default if the flag is omitted) produces a deterministic raster.
