# Preserved native adapter import failure

native-half-01 exited1 before its first joint coefficient test. The retained
canonical_math.joint_extractor imports check_parent from the active common
module, even though this extraction does not run the historical stage main.
Our new adapter supplied verify_inputs but not that compatibility name.

The failed attempt and its context/receipts remain in half/ and
native-half-01.*. It is not accepted scientific evidence.

run_native_v2.py supplies check_parent=verify_inputs, retaining the actual
input checks, and writes exclusively to a new LABEL-qualified directory.
No physical equation, gate, grid or parent file is changed; the original
run_native.py is unchanged. This is a diagnosed import repair, not an
automatic restart of a scientific failure or an observation timeout.
