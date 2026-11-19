# Bootstrap import repair

The first extension-forcing launch (forcing-half-02) exited before importing the scientific implementation: its thin wrapper attempted to import the retained parent module before common.py added the retained source directories. No forcing folder, packet or numerical check was produced. The already completed source, held-out and mean calculations are preserved and will not be relaunched.

build_extension_forcing_v2.py imports common first, then uses the identical retained forcing implementation and boundary adapter. The inspected continuation uses forcing-half-03, with the original failed receipt and script retained. This changes module discovery only, not arithmetic, data, grids, tolerances or fitted values. run_pipeline_v2.ps1 refuses an unexpected failure state and does not retry a numerical failure.

