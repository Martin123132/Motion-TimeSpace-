# Literal adapter comparison

Before running the audit, a read-only text check found that the file-writing tool had added trailing blank lines to the copied adapters. Apart from the declared history-path/index substitutions, their text matches the parent. audit_refinement_v2.py normalizes only trailing whitespace when checking these literal adapter copies; it does not normalize or permit other source changes. The unexecuted earlier audit script is retained because source receipts already recorded its hash. No numerical calculation failed or was repeated for this adjustment.
