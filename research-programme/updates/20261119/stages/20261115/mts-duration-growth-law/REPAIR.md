# Validation receipt serialization repair

The first final-verification worker completed its calculations but failed while serializing numpy boolean scalars to JSON. Its failed worker receipt and empty validation.json are retained; that empty file is not an authoritative result.

verify_stage.py now converts check flags to ordinary Python booleans before serialization. The separately identified verify-stage-v2 worker writes validation-v2.json. No mathematical calculation, threshold, saved input, numerical run or result was changed or rerun for this repair. The sealer explicitly records the one failed validation-only worker and requires passing v2 validation. All task-owned workers must still be verified exited.
