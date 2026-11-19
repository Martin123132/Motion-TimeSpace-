# Preserved reporting failure

forcing-half-01 exited1 after finishing the first256-phase numerical packet. The traceback is a TypeError in the final report expression abs(background_defects): background_defects is a Python list, not a NumPy array. The underlying packet was written before this report serialization failed; the old script, packet, logs and receipts are retained under half/forcing-01.

build_forcing_v2.py changes this expression to np.abs(background_defects) and uses a NEW forcing-02 output. It does not change equations, input packets, derivatives, phase grid, physical gates or numerical methods. Because the complete acceptance summary was not written, the first node is recomputed once with this diagnosed reporting fix rather than pretending the failed run is a complete acceptance receipt. This is an inspected implementation repair, not a numerical-gate relaxation or an observation-timeout restart.
