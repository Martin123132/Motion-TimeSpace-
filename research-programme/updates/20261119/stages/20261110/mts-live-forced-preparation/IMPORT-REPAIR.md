# Import collision before numerical work

The first launch of check_preparation.py exited with ImportError before
entering its worker context. This stage's wrapper named retained.py
collided with the older action_model module's own retained.py import.
Renamed only the new wrapper to bridge_imports.py and changed its import.
No native capture, numerical evolution, or output packet had begun. The
older loader and all sealed files remain unchanged. The tool returned
process exit code 1; no failed worker was left running.
