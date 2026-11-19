# Preparation serialization repair

The first preparation stopped before saving algebra-controls.json or freezing
inputs: NumPy Boolean scalars in the algebra report are not JSON-serializable.
The algebra checks themselves passed. No evolution or score comparison had
started. Preserve prepare-start.json, prepare-failure.json and the original
driver in run_envelope_before_bool_repair.py.

Convert only those report flags to builtin bool. The explicit prepare-resume
entry verifies the two already written norms against the exact retained source
files, instead of overwriting them; it uses a new worker receipt. No equations,
numerical tolerances, predictions or scientific acceptance rules changed.
