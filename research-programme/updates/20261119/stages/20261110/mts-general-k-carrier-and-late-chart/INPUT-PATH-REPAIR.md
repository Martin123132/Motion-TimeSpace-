# Windows sealed-path lookup repaired before tests

The first syntactically valid freeze process, PID36288 created1794354949.3620815, stopped before frozen-inputs.json was written and before any numerical test. Its terminal receipt remains failed with exactly KeyError('runs/cold-v4/config.json'). The old late-stage seal records nested keys with Windows backslashes; the new lookup used forward-slash text keys.

The pre-repair run_checks.py SHA256 was 7f503de56a9de90e426aa2d320ccd8acbc0264a73b0e76caf9f75be1a7d8be48. The lookup now converts BOTH the sealed relative keys and requested relative names to pathlib.Path before comparison. It still verifies each file's unchanged SHA256 and the retained seal itself; no missing path is waived or invented.

The repaired freeze uses the distinct freeze-native-paths receipt. The failed freeze receipt is not overwritten, retried under its old identity or counted as a scientific pass. Final cleanup accepts only this specifically identified exited failure, alongside completed workers. The original process was absent on the external check; no process was killed. The prior draft parsing error is separately documented.
