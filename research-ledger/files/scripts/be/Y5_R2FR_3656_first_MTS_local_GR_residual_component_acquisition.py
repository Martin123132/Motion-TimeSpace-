from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3656"
BRANCH_ID = "MTS_R2FR_Y5_FIRST_MTS_LOCAL_GR_RESIDUAL_COMPONENT_ACQUISITION_3656"
DOC = ROOT / "3656-Y5-R2FR-first-MTS-local-GR-residual-component-acquisition.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_float(value: object) -> float | None:
    text = str(value).strip()
    try:
        return float(text)
    except ValueError:
        return None


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("next_3655", RESIDUALS / "P8_Y5_R2FR_3655_NEXT_TARGET.csv", "delta_gamma_MTS", "3655 selected first actual MTS gamma component"),
        ("fill_3655", RESIDUALS / "P8_Y5_R2FR_3655_FIRST_COMPONENT_FILL_ROWS.csv", "MTS_COMPONENT_NOT_FILLED_PLACEHOLDER_REFUSED", "3655 refused to count placeholder gamma"),
        ("zero_audit_3655", RESIDUALS / "P8_Y5_R2FR_3655_ZERO_CERTIFICATE_COMPONENT_AUDIT.csv", "q_metric_PPN", "metric second-order zero remains unsigned"),
        ("bound_interface_3653", RESIDUALS / "P8_Y5_R2FR_3653_BOUND_INTERFACE_ROWS.csv", "BI3653_0_gamma", "gamma bound interface"),
        ("local_bounds_R3", LOCAL_BOUNDS / "local_bound_claims.csv", "R3_gamma", "Cassini gamma bound anchor"),
        ("motion_load_02", ROOT / "02-motion-load-local-GR-reduction.md", "motion_load_local_GR_reduction_conditional_not_promoted", "conditional local-GR reduction source"),
        ("EH_ledger_425", ROOT / "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md", "EH-to-Poisson bridge is clean if", "EH/source premise ledger"),
        ("weak_field_3652", ROOT / "3652-Y5-R2FR-weak-field-source-Hamiltonian-GM-calibration-or-source-vector-bound.md", "delta ln mu_obs", "source/readout/boundary weak-field residual law"),
        ("local_GR_3653", ROOT / "3653-Y5-R2FR-Newton-Poisson-PPN-zero-vector-gate-or-local-GR-residual-fit.md", "delta_gamma_MTS", "local-GR residual vector source"),
        ("alpha_mass_1048", ROOT / "1048-Y5-R10-no-extra-F2-no-mass-vertex-parent-action-signature-or-alpha-mass-bound-matrix.md", "LOCAL_GR_NOT_SCORE_READY", "PPN source/readout rows remain unscored"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        body = read_text(path)
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in body,
                "role": role,
            }
        )
    return rows


def gamma_derivation_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "derivation_id": "GD3656_0_weak_field_metric",
            "object": "local weak-field metric",
            "statement": "Use g00=-(1+2*Phi_MTS/c^2)+O(c^-4) and gij=(1+2*Psi_MTS/c^2)*delta_ij+O(c^-4) in the observed local frame.",
            "formula": "gamma_MTS = Psi_MTS/Phi_MTS at leading PPN order",
            "status": "KINEMATIC_DEFINITION_DERIVED",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "derivation_id": "GD3656_1_gamma_residual",
            "object": "PPN gamma residual",
            "statement": "The first MTS local-GR component is the weak-field gravitational slip normalized by the Newtonian potential plus source/readout/boundary corrections.",
            "formula": "delta_gamma_MTS = (Psi_MTS-Phi_MTS)/Phi_N + q_readout_gamma + q_source_gamma + q_boundary_gamma",
            "status": "MTS_COMPONENT_FORMULA_ACQUIRED_NOT_NUMERIC",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "derivation_id": "GD3656_2_tracefree_field_equation",
            "object": "spatial trace-free weak-field equation",
            "statement": "At linear order the trace-free ij equation sources slip only through trace-free anisotropic stress/operator/readout/boundary pieces.",
            "formula": "nabla2(Psi_MTS-Phi_MTS) = S_TF_MTS := P_TF(E_nonEH_ij + 8*pi*G*T_extra_ij/c^4 + B_boundary_ij + R_readout_ij)",
            "status": "SLIP_SOURCE_DECOMPOSITION_DERIVED",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "derivation_id": "GD3656_3_gamma_zero_law",
            "object": "conditional gamma zero",
            "statement": "If the same-frame EH trace-free equation is parent-owned and S_TF_MTS=q_source_gamma=q_readout_gamma=q_boundary_gamma=0, then delta_gamma_MTS=0.",
            "formula": "EH_TF_signed and S_TF_MTS=0 and q_readout_gamma=q_source_gamma=q_boundary_gamma=0 => delta_gamma_MTS=0",
            "status": "CONDITIONAL_ZERO_THEOREM_PREMISES_UNSIGNED",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "derivation_id": "GD3656_4_current_verdict",
            "object": "first MTS component status",
            "statement": "The placeholder is replaced by a precise slip functional, but not by a number or theorem-zero certificate.",
            "formula": "delta_gamma_MTS := Slip_TF[local parent action, source, readout, boundary]/Phi_N",
            "status": "FORMULA_PROGRESS_NO_LOCAL_GR_PASS",
            "claim_allowed": False,
        },
    ]


def gamma_component_rows(ts: str) -> list[dict[str, object]]:
    bound_rows = {row["row_id"]: row for row in load_csv(LOCAL_BOUNDS / "local_bound_claims.csv")}
    gamma_bound = bound_rows["R3_gamma"]
    interface = next(row for row in load_csv(RESIDUALS / "P8_Y5_R2FR_3653_BOUND_INTERFACE_ROWS.csv") if row["interface_id"] == "BI3653_0_gamma")
    return [
        {
            **base(ts),
            "component_id": "MTSG3656_0_delta_gamma_formula",
            "observable": interface["observable"],
            "symbol": interface["mts_symbol"],
            "formula": "(Psi_MTS-Phi_MTS)/Phi_N + q_readout_gamma + q_source_gamma + q_boundary_gamma",
            "required_inputs": "Phi_MTS;Psi_MTS;q_readout_gamma;q_source_gamma;q_boundary_gamma",
            "bound_row": "R3_gamma",
            "upper_bound": parse_float(gamma_bound["upper_bound"]),
            "units": gamma_bound["units"],
            "score_ready": False,
            "numeric_value": "MISSING_Phi_Psi_or_zero_certificate",
            "component_status": "MTS_GAMMA_FORMULA_ACQUIRED_VALUE_MISSING",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "component_id": "MTSG3656_1_slip_source_functional",
            "observable": "gravitational_slip_source",
            "symbol": "S_TF_MTS",
            "formula": "P_TF(E_nonEH_ij + 8*pi*G*T_extra_ij/c^4 + B_boundary_ij + R_readout_ij)",
            "required_inputs": "nonEH_tracefree_operator;extra_sector_anisotropic_stress;boundary_tracefree_term;readout_tracefree_term",
            "bound_row": "R3_gamma via delta_gamma_MTS",
            "upper_bound": parse_float(gamma_bound["upper_bound"]),
            "units": "dimensionless after Green normalization by Phi_N",
            "score_ready": False,
            "numeric_value": "MISSING_S_TF_MTS",
            "component_status": "TRACEFREE_SLIP_SOURCE_IDENTIFIED_NOT_FILLED",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "component_id": "MTSG3656_2_gamma_bound_interface",
            "observable": "gamma_minus_1",
            "symbol": "abs(delta_gamma_MTS)",
            "formula": "abs((Psi_MTS-Phi_MTS)/Phi_N + q_readout_gamma + q_source_gamma + q_boundary_gamma) <= 2.3e-05",
            "required_inputs": "numeric slip/readout/source/boundary projection or all-zero certificate",
            "bound_row": "R3_gamma",
            "upper_bound": parse_float(gamma_bound["upper_bound"]),
            "units": gamma_bound["units"],
            "score_ready": False,
            "numeric_value": "MISSING_delta_gamma_MTS",
            "component_status": "BOUND_READY_MTS_VALUE_MISSING",
            "claim_allowed": False,
        },
    ]


def gamma_zero_condition_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("GZ3656_0_same_frame_metric", "same observed local metric/coframe owns both Phi_MTS and Psi_MTS", "q_readout_PPN", "UNSIGNED"),
        ("GZ3656_1_EH_TF_equation", "linear trace-free spatial equation is the EH equation in the observed frame", "q_EH_action;q_metric_PPN", "UNSIGNED"),
        ("GZ3656_2_no_extra_anisotropic_stress", "P_TF(E_nonEH_ij + 8*pi*G*T_extra_ij/c^4)=0 in the local branch", "q_nonEH_PPN;q_source_coupling_PPN", "UNSIGNED"),
        ("GZ3656_3_boundary_silence", "P_TF(B_boundary_ij)=0 on the local domain", "q_boundary_PPN", "UNSIGNED"),
        ("GZ3656_4_source_readout_silence", "q_source_gamma=q_readout_gamma=0 for the local gamma observable", "q_source_coupling_PPN;q_readout_PPN", "UNSIGNED"),
        ("GZ3656_5_gamma_zero_total", "all clauses above hold simultaneously", "delta_gamma_MTS", "NOT_SIGNED"),
    ]
    return [
        {
            **base(ts),
            "condition_id": condition_id,
            "condition": condition,
            "upstream_zero_clause": clause,
            "current_status": status,
            "accepted_as_zero": False,
            "claim_allowed": False,
        }
        for condition_id, condition, clause, status in specs
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3656_0_formula_progress", "delta_gamma_MTS placeholder replaced by weak-field slip formula", "PASSED_FORMULA_GATE", "we now know the exact first component to attack"),
        ("CG3656_1_no_number", "no numeric MTS gamma value is claimed", "ACTIVE_GUARD", "Phi/Psi/slip inputs are still missing"),
        ("CG3656_2_no_zero", "no theorem-zero MTS gamma certificate is claimed", "ACTIVE_GUARD", "trace-free anisotropic stress/readout/boundary clauses are unsigned"),
        ("CG3656_3_bound_interface", "Cassini gamma bound remains the scoring interface", "BOUND_READY_VALUE_MISSING", "abs(delta_gamma_MTS)<=2.3e-5 only scores after prediction"),
        ("CG3656_4_next", "next step targets S_TF_MTS zero proof or gamma coefficient bound", "ANISOTROPIC_STRESS_ZERO_NEXT", "this is the smallest honest route toward local GR"),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "reason": reason,
            "claim_allowed": False,
        }
        for gate_id, gate, status, reason in specs
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status": "DELTA_GAMMA_MTS_SLIP_FORMULA_ACQUIRED_NO_NUMERIC_OR_ZERO_CLAIM",
            "summary": "3656 replaces the gamma placeholder with the weak-field gravitational-slip functional and identifies the exact zero clauses needed for a local-GR gamma pass.",
            "claim_ceiling": "no MTS gamma, PPN, Newtonian, local-GR, source-calibration, clock, orbital, WEP, R10, or EH-dominance pass is claimed",
            "useful_result": "The first component is no longer a fog bank: local gamma reduces to the trace-free anisotropic-stress/operator/readout/boundary source S_TF_MTS.",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3656_0",
            "target_doc": "3657-Y5-R2FR-S_TF_MTS-zero-proof-or-gamma-coefficient-bound.md",
            "target_script": "scripts/Y5_R2FR_3657_S_TF_MTS_zero_proof_or_gamma_coefficient_bound.py",
            "objective": "try to prove S_TF_MTS=0 from local isotropy/same-frame EH ownership, or fill a nonclaim coefficient bound for the gamma slip source",
            "success_gate": "delta_gamma_MTS becomes theorem-zero or receives a numeric/source-backed coefficient bound; otherwise keep the gamma component nonclaim",
        }
    ]


def write_doc(sources, derivation, components, conditions, gates, status, next_target) -> None:
    lines = [
        "# 3656 - First MTS local-GR residual component acquisition",
        "",
        f"**Status:** {status[0]['summary']}",
        "",
        f"**Claim ceiling:** {status[0]['claim_ceiling']}.",
        "",
        "## Main result",
        "",
        "The first actual component target is `delta_gamma_MTS`. In the local weak-field metric, `gamma_MTS=Psi_MTS/Phi_MTS`, so the MTS gamma residual is",
        "",
        "`delta_gamma_MTS = (Psi_MTS-Phi_MTS)/Phi_N + q_readout_gamma + q_source_gamma + q_boundary_gamma`.",
        "",
        "This is progress but not a pass. The placeholder is now a concrete gravitational-slip functional. To make it zero, the parent theory must kill the trace-free source",
        "",
        "`S_TF_MTS = P_TF(E_nonEH_ij + 8*pi*G*T_extra_ij/c^4 + B_boundary_ij + R_readout_ij)`.",
        "",
        "That gives the next sharp route: prove `S_TF_MTS=0` or fill a source-backed gamma coefficient bound. No baseline row counts as MTS evidence.",
        "",
        "## Derivation rows",
    ]
    for row in derivation:
        lines.append(f"- `{row['derivation_id']}`: {row['status']} - `{row['formula']}`")
    lines.extend(["", "## Gamma component rows"])
    for row in components:
        lines.append(f"- `{row['component_id']}`: `{row['symbol']}` - {row['component_status']}")
    lines.extend(["", "## Zero conditions"])
    for row in conditions:
        lines.append(f"- `{row['condition_id']}`: {row['current_status']} - {row['condition']}")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} - {row['gate']}")
    lines.extend(["", "## Next checkpoint", ""])
    lines.append(f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.")
    lines.extend(["", "## Sources"])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows)
    except Exception:
        return False, 0


def validate(ts, output_paths, sources, derivation, components, conditions, gates, status, next_target) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    add("VAL3656_0_sources_exist", all(row["exists"] for row in sources), "every cited local source path exists")
    add("VAL3656_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3656_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3656 outputs written")
    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    add("VAL3656_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3656_4_derivation_rows_present", len(derivation) >= 5 and any(row["derivation_id"] == "GD3656_1_gamma_residual" for row in derivation), "gamma derivation rows present")
    add("VAL3656_5_gamma_formula_acquired", any(row["symbol"] == "delta_gamma_MTS" and "(Psi_MTS-Phi_MTS)/Phi_N" in row["formula"] for row in components), "delta_gamma_MTS formula acquired")
    add("VAL3656_6_slip_source_identified", any(row["symbol"] == "S_TF_MTS" and "P_TF" in row["formula"] for row in components), "trace-free slip source identified")
    add("VAL3656_7_bound_carried", any(row["bound_row"] == "R3_gamma" and parse_float(row["upper_bound"]) == 2.3e-05 for row in components), "Cassini gamma bound carried")
    add("VAL3656_8_no_mts_score_ready", not any(str(row.get("score_ready", "")).lower() == "true" for row in components), "no MTS gamma row made score-ready")
    add("VAL3656_9_zero_conditions_unsigned", all(str(row["accepted_as_zero"]).lower() == "false" for row in conditions), "zero conditions remain unsigned")
    add("VAL3656_10_claim_gates_present", {"CG3656_0_formula_progress", "CG3656_1_no_number", "CG3656_2_no_zero", "CG3656_3_bound_interface", "CG3656_4_next"}.issubset({row["gate_id"] for row in gates}), "core claim gates present")
    generated = sources + derivation + components + conditions + gates + status + next_target
    add("VAL3656_11_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim")
    doc_text = read_text(DOC)
    add("VAL3656_12_doc_written", "delta_gamma_MTS" in doc_text and "S_TF_MTS" in doc_text and "not a pass" in doc_text, "doc records gamma slip formula and nonclaim status")
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3656*", "3656-Y5-R2FR-*", "Y5_R2FR_3656_*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3656_13_no_formalization_leak", not leaks, "no 3656 checkpoint files in formalization-workbench")
    add("VAL3656_14_next_target", next_target[0]["target_doc"].startswith("3657-") and "S_TF_MTS" in next_target[0]["target_doc"], "3657 trace-free slip target selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    derivation = gamma_derivation_rows(ts)
    components = gamma_component_rows(ts)
    conditions = gamma_zero_condition_rows(ts)
    gates = claim_gate_rows(ts)
    status = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3656_SOURCE_REGISTER.csv",
        "derivation": RESIDUALS / "P8_Y5_R2FR_3656_GAMMA_WEAK_FIELD_DERIVATION_ROWS.csv",
        "components": RESIDUALS / "P8_Y5_R2FR_3656_GAMMA_COMPONENT_ROWS.csv",
        "conditions": RESIDUALS / "P8_Y5_R2FR_3656_GAMMA_ZERO_CONDITIONS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3656_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3656_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3656_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3656_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["derivation"], derivation)
    write_csv(outputs["components"], components)
    write_csv(outputs["conditions"], conditions)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, derivation, components, conditions, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, derivation, components, conditions, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3656 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3656 checkpoint with {len(validation)} validation checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
