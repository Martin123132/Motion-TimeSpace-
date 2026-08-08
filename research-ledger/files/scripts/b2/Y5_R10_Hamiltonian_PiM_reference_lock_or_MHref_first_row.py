from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def missing(value: object) -> bool:
    text = str(value or "").strip()
    upper = text.upper()
    return text == "" or upper.startswith("MISSING") or upper.startswith("NOT_COMPUTED") or text.startswith("FILL_")


def source_path(path_text: str) -> Path:
    candidate = Path(path_text)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1017_0_1016_next", "source-intake/mts_residuals/P8_Y5_R10_1016_NEXT_TARGET.csv", "M_H_ref plus B_zero_flux", "1016 handoff target."),
        ("SRC1017_1_1016_schema", "source-intake/mts_residuals/P8_Y5_R10_1016_FIRST_INPUT_SCHEMA.csv", "FIS1016_0_M_H_ref", "1016 first input schema."),
        ("SRC1017_2_1016_selector", "source-intake/mts_residuals/P8_Y5_R10_1016_PARENT_SELECTOR_CONTRACT.csv", "PSC1016_5_dressed_source_charge", "1016 selector denominator contract."),
        ("SRC1017_3_664_integrability", "source-intake/mts_residuals/P8_Y5_R10_664_INTEGRABILITY_ATTEMPT.csv", "HCI664_6_integrability_verdict", "664 integrability attempt."),
        ("SRC1017_4_664_fill", "source-intake/mts_residuals/P8_Y5_R10_664_FIRST_RESIDUAL_FILL.csv", "FB554_0_HPiM_integrability_reference_bound", "664 first residual fill row."),
        ("SRC1017_5_554_integrability", "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_CHARGE_INTEGRABILITY_REFERENCE_ATTEMPT.csv", "HCI554_6_integrability_verdict", "554 integrability reference attempt."),
        ("SRC1017_6_554_fill", "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_INTEGRABILITY_SOURCE_EQUALITY_FILL_ROWS.csv", "FB554_0_HPiM_integrability_reference_bound", "554 fill row."),
        ("SRC1017_7_665_zero", "source-intake/mts_residuals/P8_Y5_R10_665_THEOREM_ZERO_ATTEMPT.csv", "TZ665_5_verdict", "665 theorem-zero attempt."),
        ("SRC1017_8_665_fill", "source-intake/mts_residuals/P8_Y5_R10_665_FIRST_FILL_ROW_STAGED.csv", "FB5540_input_M_H_ref", "665 first fill row staged."),
        ("SRC1017_9_666_parent_lock", "source-intake/mts_residuals/P8_Y5_R10_666_PARENT_LOCK_ATTEMPT.csv", "PLA666_2_integrable_theta_Qtau", "666 parent boundary/reference lock attempt."),
        ("SRC1017_10_666_hunt", "source-intake/mts_residuals/P8_Y5_R10_666_FB5540_SOURCE_VALUE_HUNT_LEDGER.csv", "SVH666_0_delta_H_tau", "666 source value hunt ledger."),
        ("SRC1017_11_667_variation", "source-intake/mts_residuals/P8_Y5_R10_667_VARIATION_LEDGER.csv", "VL667_4_integrability_curl", "667 variation ledger."),
        ("SRC1017_12_667_terms", "source-intake/mts_residuals/P8_Y5_R10_667_FB5540_TERM_MAP.csv", "TM667_4_M_H_ref", "667 FB5540 term map."),
        ("SRC1017_13_667_fallback", "source-intake/mts_residuals/P8_Y5_R10_667_RESIDUAL_FALLBACK_ROWS.csv", "RF667_0_LX_theta_Qtau_owner", "667 residual fallback rows."),
    ]
    rows = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": path_text,
                "exists": str(path.exists()).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "generated_utc": stamp(),
            }
        )
    return rows


def reference_lock_rows() -> list[dict[str, str]]:
    rows = [
        (
            "HRL1017_0_variation_formula",
            "Hamiltonian variation is defined by covariant phase space",
            "delta H_tau[S] = integral_S(delta Q_tau^MTS - i_tau Theta_total) - delta H_ref[S]",
            "conditional_formal_step",
            "formal definition only; not an integrability theorem",
        ),
        (
            "HRL1017_1_integrability_curl",
            "field-space curl of delta H_tau vanishes",
            "I_tau(delta1,delta2)=integral_S i_tau omega_total + curl(delta H_ref)=0",
            "fail_current_claim",
            "L_X, Theta_X, Q_X, reference curl, tau/domain/projector variations are not computed",
        ),
        (
            "HRL1017_2_reference_lock",
            "reference subtraction is fixed once and derivative-silent",
            "partial_{source,r,t,frame,lambda} Delta_ref = 0",
            "fail_current_claim",
            "B_ref is named but not selected by a current parent principle",
        ),
        (
            "HRL1017_3_boundary_flux_zero",
            "extra symplectic/boundary/projector leakage is zero or fixed",
            "integral_boundary(delta Q_tau^extra - i_tau Theta_extra)+delta B_class = 0",
            "fail_current_claim",
            "boundary class/nohair and projector silence remain unsigned",
        ),
        (
            "HRL1017_4_tau_lock",
            "one observed time generator is used by source, charge, clocks, and readout",
            "tau_source = tau_charge = tau_clock = tau_readout and delta tau = 0",
            "fail_current_claim",
            "observed coframe/matter functor selecting tau is not parent-derived",
        ),
        (
            "HRL1017_5_MHref_denominator",
            "M_H_ref is a positive same-frame dressed source denominator",
            "M_H_ref = G_ref^-1 integral_S Q_tau^MTS, with same tau and observed frame",
            "fail_current_claim",
            "worldtube source equality and Poisson/Gauss/orbital readout remain downstream",
        ),
        (
            "HRL1017_6_FB5540_zero_law",
            "FB554_0 vanishes componentwise",
            "epsilon_HPiM_integrability_abs = |delta_H_tau_nonintegrable|/M_H_ref + |Delta_ref|/M_H_ref + |symplectic_boundary_flux|/M_H_ref = 0",
            "fail_current_claim",
            "at least integrability curl, reference lock, boundary flux, tau lock, and denominator remain unsigned",
        ),
    ]
    return [
        {
            "lock_id": lock_id,
            "required_lock": required_lock,
            "mathematical_form": mathematical_form,
            "current_status": current_status,
            "failure_if_missing": failure_if_missing,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for lock_id, required_lock, mathematical_form, current_status, failure_if_missing in rows
    ]


def theorem_attempt_rows() -> list[dict[str, str]]:
    rows = [
        (
            "HPT1017_0_EH_reference",
            "EH with stationary boundary conditions has a known conditional integrable charge route",
            "known_conditional_reference",
            "shows the route is mathematically legitimate",
            "MTS has not inherited the EH symplectic charge sector-by-sector",
        ),
        (
            "HPT1017_1_parent_theta_Qtau",
            "current MTS supplies explicit L_X, Theta_X, Q_X, and C_tau decomposition",
            "not_derived",
            "would make the integrability curl computable instead of schematic",
            "sector Lagrangian owner is missing",
        ),
        (
            "HPT1017_2_reference_superselection",
            "B_ref is selected by parent branch/topology/fixed stationarity and cannot absorb source calibration",
            "not_derived",
            "would zero or bound Delta_ref_over_MH without reference-only cheating",
            "parent reference functional remains missing",
        ),
        (
            "HPT1017_3_boundary_class_nohair",
            "B_class/C_top/chi_B are parent-owned and carry no compact linked mass flux",
            "not_derived",
            "would zero symplectic_boundary_flux and B_zero_flux terms",
            "boundary class selection and projector silence are unsigned",
        ),
        (
            "HPT1017_4_denominator_guard",
            "M_H_ref is not orbital GM, bare mass, or reference-only normalization",
            "guardrail_pass_no_denominator_theorem",
            "prevents circular normalization of R_eq and FB554_0 rows",
            "source-measure equality and Gauss/orbital readout are downstream",
        ),
        (
            "HPT1017_5_verdict",
            "Hamiltonian PiM reference/integrability lock is signed for current MTS",
            "fail_current_claim",
            "would open the first stable source-charge gate",
            "not signed; use source-ready row schema or sector-owner target",
        ),
    ]
    return [
        {
            "attempt_id": attempt_id,
            "claim": claim,
            "current_status": current_status,
            "would_close": would_close,
            "current_blocker": current_blocker,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for attempt_id, claim, current_status, would_close, current_blocker in rows
    ]


def first_row_schema_rows() -> list[dict[str, str]]:
    rows = [
        (
            "MHR1017_0_M_H_ref_denominator",
            "M_H_ref",
            "positive dressed source charge denominator from same-frame Hamiltonian/Noether charge",
            "system_id;tau_id;surface_outer;Q_tau_integral;G_ref;H_ref;M_H_ref;units;reference_rule;source_path;assumptions;valid_for_claim",
            "MISSING_STABLE_MH_REF",
            "source-intake/mts_residuals/P8_Y5_R10_665_FIRST_FILL_ROW_STAGED.csv",
        ),
        (
            "MHR1017_1_delta_H_tau_nonintegrable",
            "delta_H_tau_nonintegrable_over_MH",
            "field-space curl obstruction of the Hamiltonian source charge normalized by M_H_ref",
            "system_id;surface_pair;field_variation_pair;integrability_curl;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "MISSING_INTEGRABILITY_NUMERIC_OR_THEOREM_ZERO",
            "source-intake/mts_residuals/P8_Y5_R10_666_FB5540_SOURCE_VALUE_HUNT_LEDGER.csv",
        ),
        (
            "MHR1017_2_Delta_ref",
            "Delta_ref_over_MH;H_ref_shift",
            "reference subtraction shift and derivative profile normalized by M_H_ref",
            "system_id;reference_branch;surface_pair;Delta_ref;H_ref_shift;M_H_ref;derivative_profile;units;source_path;assumptions;valid_for_claim",
            "MISSING_REFERENCE_NUMERIC_OR_THEOREM_ZERO",
            "source-intake/mts_residuals/P8_Y5_R10_666_FB5540_SOURCE_VALUE_HUNT_LEDGER.csv",
        ),
        (
            "MHR1017_3_symplectic_boundary_flux",
            "symplectic_boundary_flux_over_MH;B_zero_flux;Delta_symp",
            "boundary/projector/non-EH symplectic leakage through linked surfaces normalized by M_H_ref",
            "system_id;surface_pair;boundary_rule;symplectic_boundary_flux;B_zero_flux;Delta_symp;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "MISSING_SYMPLECTIC_BOUNDARY_NUMERIC_OR_THEOREM_ZERO",
            "source-intake/mts_residuals/P8_Y5_R10_666_FB5540_SOURCE_VALUE_HUNT_LEDGER.csv",
        ),
        (
            "MHR1017_4_tau_lock",
            "time_generator_lock",
            "certificate or bounded mismatch for tau_source=tau_charge=tau_clock=tau_readout",
            "system_id;tau_source;tau_charge;tau_clock;tau_readout;mismatch_bound;units;source_path;assumptions;valid_for_claim",
            "MISSING_TAU_LOCK_CERTIFICATE",
            "source-intake/mts_residuals/P8_Y5_R10_665_FIRST_FILL_ROW_STAGED.csv",
        ),
        (
            "MHR1017_5_FB5540_total",
            "epsilon_HPiM_integrability_abs",
            "no-cancellation total for FB554_0 with denominator and every numerator component present",
            "system_id;epsilon_HPiM_integrability_abs;component_sum_abs;M_H_ref;normalization;source_path;assumptions;valid_for_claim",
            "NOT_COMPUTED_COMPONENTS_MISSING",
            "source-intake/mts_residuals/P8_Y5_R10_665_FIRST_FILL_ROW_STAGED.csv",
        ),
    ]
    return [
        {
            "row_id": row_id,
            "quantity": quantity,
            "definition": definition,
            "required_columns": required_columns,
            "current_status": current_status,
            "source_path": path_text,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for row_id, quantity, definition, required_columns, current_status, path_text in rows
    ]


def runner_rows(schema: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for row in schema:
        reasons = []
        if missing(row["current_status"]):
            reasons.append("MISSING_THEOREM_OR_SOURCE_INPUT")
        if not flag(row["valid_for_claim"]):
            reasons.append("VALID_FOR_CLAIM_FALSE")
        rows.append(
            {
                "runner_id": row["row_id"].replace("MHR1017", "MRR1017"),
                "row_id": row["row_id"],
                "quantity": row["quantity"],
                "computed_status": "blocked_missing_inputs",
                "claim_allowed": "false",
                "failure_reasons": ";".join(reasons),
                "generated_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, str]]:
    gates = [
        ("CG1017_0_reference_lock_written", "Hamiltonian reference/integrability lock is explicit", "true", "HRL1017 rows split variation, curl, reference, boundary, tau, denominator, and total law", "false"),
        ("CG1017_1_integrability_zero", "delta_H_tau_nonintegrable_over_MH is theorem-zero", "false", "L_X/Theta_X/Q_X and integrability curl are not computed", "false"),
        ("CG1017_2_reference_zero", "Delta_ref_over_MH and H_ref_shift are theorem-zero", "false", "B_ref is not parent-selected and derivative-silent", "false"),
        ("CG1017_3_boundary_zero", "symplectic boundary flux, B_zero_flux, and Delta_symp are theorem-zero", "false", "boundary class/nohair/projector silence are unsigned", "false"),
        ("CG1017_4_MHref_claim", "M_H_ref is a stable same-frame denominator", "false", "source-measure equality and Gauss/orbital readout remain downstream", "false"),
        ("CG1017_5_first_row_claim_ready", "M_H_ref plus FB554_0 numerator rows are source-backed and normalized", "false", "all first-row schema entries are missing/nonclaim", "false"),
        ("CG1017_6_Newton_local_GR", "Newton/local-GR gates can reopen", "false", "stable Hamiltonian source charge is not derived", "false"),
        ("CG1017_7_guardrail", "Hamiltonian reference-lock guardrail is installed", "true", "no reference-only zero, bare mass denominator, or unnormalized R_eq scoring is allowed", "false"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "reason": reason,
            "claim_allowed": claim_allowed,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for gate_id, claim, gate_pass, reason, claim_allowed in gates
    ]


def decision_rows() -> list[dict[str, str]]:
    rows = [
        {
            "decision_id": "DEC1017_0_reference_lock",
            "decision": "FB554_0 is still the right first hard local-GR source-charge lock.",
            "because": "without integrable H_tau, fixed H_ref, zero boundary/symplectic flux, tau lock, and stable M_H_ref, Pi_M^H is only notation.",
            "next_action": "derive the missing sector Lagrangian/boundary owners or keep first-row source hunt nonclaim",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1017_1_no_MHref_shortcut",
            "decision": "M_H_ref cannot be replaced by orbital GM, bare mass, or reference-only 1.",
            "because": "that would normalize the obstruction with the readout the theorem is supposed to derive.",
            "next_action": "require Q_tau integral plus fixed reference before scoring R_eq or FB554_0",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1017_2_first_row_schema",
            "decision": "The first source-backed row must include denominator and numerator pieces together.",
            "because": "delta_H_tau_nonintegrable, Delta_ref, and boundary flux are meaningless as evidence without M_H_ref and no-cancellation bookkeeping.",
            "next_action": "do not run R10/R11/local comparisons until all FB554_0 components are real",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1017_3_next_target",
            "decision": "The next root target is sector Lagrangian/boundary owner or first FB554_0 source row.",
            "because": "667 shows the exact missing owners: L_X/Theta_X/Q_X, B_ref, B_class/C_top/chi_B, tau, and source readout.",
            "next_action": "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md",
            "valid_for_claim": "false",
        },
    ]
    for row in rows:
        row["generated_utc"] = stamp()
    return rows


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md",
            "objective": "derive L_X/Theta_X/Q_X plus B_ref/B_class/tau ownership for the Hamiltonian source charge, or fill a source-backed FB554_0 row with M_H_ref and all numerator components",
            "include": "L_X, Theta_X, Q_X, omega_X, B_ref, B_class, C_top, chi_B, tau lock, M_H_ref, delta_H_tau_nonintegrable, Delta_ref, symplectic_boundary_flux, source paths",
            "exclude": "reference-only zero, bare mass denominator, orbital GM denominator, unnormalized R_eq, cancellation between unknowns, Newton/local-GR claim, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    changed = []
    for candidate in FORMALIZATION.rglob("*"):
        if candidate.is_file() and datetime.fromtimestamp(candidate.stat().st_mtime, timezone.utc) >= STARTED:
            changed.append(candidate)
    return changed


def validation_rows(
    sources: list[dict[str, str]],
    locks: list[dict[str, str]],
    attempts: list[dict[str, str]],
    schema: list[dict[str, str]],
    runner: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    required_locks = {
        "HRL1017_1_integrability_curl",
        "HRL1017_2_reference_lock",
        "HRL1017_3_boundary_flux_zero",
        "HRL1017_4_tau_lock",
        "HRL1017_5_MHref_denominator",
        "HRL1017_6_FB5540_zero_law",
    }
    required_quantities = {
        "M_H_ref",
        "delta_H_tau_nonintegrable_over_MH",
        "Delta_ref_over_MH;H_ref_shift",
        "symplectic_boundary_flux_over_MH;B_zero_flux;Delta_symp",
        "time_generator_lock",
        "epsilon_HPiM_integrability_abs",
    }
    checks = [
        ("V1017_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all source paths exist and needles are present"),
        ("V1017_1_lock_split_complete", required_locks.issubset({row["lock_id"] for row in locks}), "reference lock splits integrability, reference, boundary, tau, denominator, and total law"),
        ("V1017_2_lock_blocks_claim", any(row["lock_id"] == "HRL1017_6_FB5540_zero_law" and row["current_status"] == "fail_current_claim" for row in locks) and all(not flag(row["valid_for_claim"]) for row in locks), "FB554_0 zero law remains nonclaim"),
        ("V1017_3_theorem_attempt_complete", any(row["attempt_id"] == "HPT1017_5_verdict" and row["current_status"] == "fail_current_claim" for row in attempts), "theorem attempt records current failure"),
        ("V1017_4_denominator_guard", any(row["attempt_id"] == "HPT1017_4_denominator_guard" and row["current_status"] == "guardrail_pass_no_denominator_theorem" for row in attempts), "M_H_ref guardrail is explicit"),
        ("V1017_5_first_row_schema_complete", required_quantities.issubset({row["quantity"] for row in schema}), "first row schema covers denominator and all FB554_0 numerator terms"),
        ("V1017_6_first_row_schema_nonclaim", all(missing(row["current_status"]) and not flag(row["valid_for_claim"]) for row in schema), "all first row schema entries remain missing and nonclaim"),
        ("V1017_7_runner_refuses", len(runner) == len(schema) and all(row["computed_status"] == "blocked_missing_inputs" and not flag(row["claim_allowed"]) for row in runner), "runner refuses missing first row entries"),
        ("V1017_8_claim_gates_blocked", all(not flag(row["claim_allowed"]) and not flag(row["valid_for_claim"]) for row in gates), "reference, M_H_ref, Newton, and local-GR claims remain blocked"),
        ("V1017_9_guardrail_written", any(row["gate_id"] == "CG1017_7_guardrail" and flag(row["gate_pass"]) for row in gates), "Hamiltonian reference-lock guardrail is installed"),
        ("V1017_10_decision_written", any(row["decision_id"] == "DEC1017_3_next_target" for row in decisions), "1018 root target decision is written"),
        ("V1017_11_next_target_written", len(next_target) == 1 and "1018-Y5-R10-sector-Lagrangian-boundary-owner" in next_target[0]["next_target"], "1018 target row is present and nonclaim"),
        ("V1017_12_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    rows = [{"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()} for check_id, passed, detail in checks]
    rows.insert(0, {"check_id": "V1017_SUMMARY", "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail", "detail": "1017 Hamiltonian PiM reference-lock/MHref validation summary", "generated_utc": stamp()})
    return rows


def write_doc(
    sources: list[dict[str, str]],
    locks: list[dict[str, str]],
    attempts: list[dict[str, str]],
    schema: list[dict[str, str]],
    runner: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1017 Y5 R10 Hamiltonian PiM reference lock or MHref first row",
            "",
            "**Status:** `FB554_0` is now split into the exact reference-lock law: integrability curl, fixed reference, symplectic/boundary flux, tau lock, and a stable same-frame `M_H_ref` denominator. Current MTS does not prove those pieces zero and has no source-backed first row.",
            "",
            "**Claim ceiling:** no stable Hamiltonian source charge, `M_H_ref`, `R_eq` scoring, measured-GM closure, Newton/GR reduction, R10/R11 pass, PPN pass, or local-GR claim is allowed from 1017.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## Reference-lock law",
            md_table(locks, ["lock_id", "required_lock", "mathematical_form", "current_status", "failure_if_missing", "valid_for_claim"]),
            "## Theorem attempt",
            md_table(attempts, ["attempt_id", "claim", "current_status", "would_close", "current_blocker", "valid_for_claim"]),
            "## MHref first-row schema",
            md_table(schema, ["row_id", "quantity", "definition", "required_columns", "current_status", "valid_for_claim"]),
            "## First-row runner",
            md_table(runner, ["runner_id", "row_id", "quantity", "computed_status", "claim_allowed", "failure_reasons"]),
            "## Claim gate",
            md_table(gates, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Validation",
            md_table(validations, ["check_id", "result", "detail", "generated_utc"]),
            "## Next target",
            md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    locks = reference_lock_rows()
    attempts = theorem_attempt_rows()
    schema = first_row_schema_rows()
    runner = runner_rows(schema)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, locks, attempts, schema, runner, gates, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1017_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1017_REFERENCE_LOCK_LAW.csv", locks)
    write_csv(OUT / "P8_Y5_R10_1017_THEOREM_ATTEMPT.csv", attempts)
    write_csv(OUT / "P8_Y5_R10_1017_MHREF_FIRST_ROW_SCHEMA.csv", schema)
    write_csv(OUT / "P8_Y5_R10_1017_FIRST_ROW_RUNNER.csv", runner)
    write_csv(OUT / "P8_Y5_R10_1017_CLAIM_GATE.csv", gates)
    write_csv(OUT / "P8_Y5_R10_1017_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1017_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1017_VALIDATION.csv", validations)
    write_doc(sources, locks, attempts, schema, runner, gates, decisions, next_target, validations)


if __name__ == "__main__":
    main()
