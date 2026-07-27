from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3657"
BRANCH_ID = "MTS_R2FR_Y5_STF_MTS_ZERO_PROOF_OR_GAMMA_COEFFICIENT_BOUND_3657"
DOC = ROOT / "3657-Y5-R2FR-S_TF_MTS-zero-proof-or-gamma-coefficient-bound.md"


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
    try:
        return float(str(value).strip())
    except ValueError:
        return None


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("next_3656", RESIDUALS / "P8_Y5_R2FR_3656_NEXT_TARGET.csv", "S_TF_MTS", "3656 selected the trace-free slip source"),
        ("gamma_components_3656", RESIDUALS / "P8_Y5_R2FR_3656_GAMMA_COMPONENT_ROWS.csv", "MTSG3656_1_slip_source_functional", "3656 gamma slip source functional"),
        ("gamma_zero_3656", RESIDUALS / "P8_Y5_R2FR_3656_GAMMA_ZERO_CONDITIONS.csv", "GZ3656_2_no_extra_anisotropic_stress", "3656 unsigned zero conditions"),
        ("validation_3656", RESIDUALS / "P8_Y5_BRR545_3656_VALIDATION.csv", "VAL3656_6_slip_source_identified", "3656 validation evidence"),
        ("local_bounds_R3", LOCAL_BOUNDS / "local_bound_claims.csv", "R3_gamma", "Cassini gamma bound anchor"),
        ("motion_load_02", ROOT / "02-motion-load-local-GR-reduction.md", "conditional on accepting", "conditional local-GR reduction, not parent proof"),
        ("EH_ledger_425", ROOT / "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md", "EH-to-Poisson bridge is clean if", "same-frame EH/source premises still retained"),
        ("weak_field_3652", ROOT / "3652-Y5-R2FR-weak-field-source-Hamiltonian-GM-calibration-or-source-vector-bound.md", "q_source", "source/readout/boundary residual law"),
        ("local_GR_3653", ROOT / "3653-Y5-R2FR-Newton-Poisson-PPN-zero-vector-gate-or-local-GR-residual-fit.md", "q_nonEH_PPN", "non-EH PPN residual slot"),
        ("parent_zero_3655", RESIDUALS / "P8_Y5_R2FR_3655_ZERO_CERTIFICATE_COMPONENT_AUDIT.csv", "q_nonEH_PPN", "3655 did not sign non-EH/readout/source zero clauses"),
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


def stf_zero_proof_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "proof_id": "STF3657_0_projector_definition",
            "object": "trace-free projector",
            "statement": "For any local spatial tensor A_ij, P_TF[A]_ij = A_ij - delta_ij A^k_k/3.",
            "formula": "S_TF_MTS=P_TF(E_nonEH_ij + 8*pi*G*T_extra_ij/c^4 + B_boundary_ij + R_readout_ij)",
            "zero_status": "DEFINITION_LOCKED",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "proof_id": "STF3657_1_perfect_fluid_piece",
            "object": "isotropic perfect-fluid stress",
            "statement": "A rest-frame perfect-fluid pressure term has T_ij=p delta_ij, hence P_TF[T_ij]=0.",
            "formula": "P_TF[p delta_ij]=0",
            "zero_status": "PARTIAL_ZERO_DERIVED_FOR_ISOTROPIC_MATTER_ONLY",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "proof_id": "STF3657_2_radial_gradient_counterexample",
            "object": "radial scalar/vector-gradient stress",
            "statement": "Local spherical symmetry does not by itself kill trace-free stress: a radial field X(r) gives a nonzero STF tensor unless its gradient/curvature obeys stronger conditions.",
            "formula": "P_TF[partial_i X partial_j X]=X_prime^2(n_i n_j-delta_ij/3); P_TF[partial_i partial_j X]=(X_second-X_prime/r)(n_i n_j-delta_ij/3)",
            "zero_status": "ISOTROPY_ALONE_REJECTED",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "proof_id": "STF3657_3_strong_zero_condition",
            "object": "strong local zero condition",
            "statement": "S_TF_MTS can be theorem-zero only if non-EH trace-free operators, extra-sector anisotropic stress, boundary STF terms, and readout STF terms vanish in the same observed frame.",
            "formula": "P_TF(E_nonEH)=0 and P_TF(T_extra)=0 and P_TF(B_boundary)=0 and P_TF(R_readout)=0 => S_TF_MTS=0",
            "zero_status": "CONDITIONAL_ZERO_THEOREM_PREMISES_UNSIGNED",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "proof_id": "STF3657_4_verdict",
            "object": "S_TF_MTS zero proof",
            "statement": "Current corpus does not parent-sign the strong zero condition; the honest path is a coefficient bound unless a future parent action kills radial-gradient/operator STF pieces.",
            "formula": "S_TF_MTS remains live; local isotropy is insufficient evidence",
            "zero_status": "ZERO_PROOF_NOT_CLOSED_COEFFICIENT_BOUND_REQUIRED",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
    ]


def gamma_coefficient_bound_rows(ts: str) -> list[dict[str, object]]:
    bounds = {row["row_id"]: row for row in load_csv(LOCAL_BOUNDS / "local_bound_claims.csv")}
    gamma = bounds["R3_gamma"]
    upper = parse_float(gamma["upper_bound"])
    measured = parse_float(gamma["measured_value"])
    sigma = parse_float(gamma["one_sigma"])
    return [
        {
            **base(ts),
            "bound_id": "GCB3657_0_Cgamma_TF_total",
            "coefficient": "C_gamma_TF_total",
            "definition": "observable normalized gamma-slip envelope abs(G_TF[S_TF_MTS]/Phi_N + q_readout_gamma + q_source_gamma + q_boundary_gamma)",
            "bound_formula": "C_gamma_TF_total <= abs(delta_gamma_MTS)_obs_bound",
            "numeric_upper_bound": upper,
            "units": gamma["units"],
            "source_row": "R3_gamma",
            "source_value": measured,
            "source_one_sigma": sigma,
            "source_reference": gamma["reference_path_or_url"],
            "bound_status": "SOURCE_BACKED_OBSERVATIONAL_BOUND_NONCLAIM",
            "score_ready": False,
            "valid_for_prediction_claim": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "bound_id": "GCB3657_1_CnonEH_TF",
            "coefficient": "C_nonEH_TF_gamma",
            "definition": "normalized contribution of trace-free non-EH local operators to gamma slip",
            "bound_formula": "abs(C_nonEH_TF_gamma) <= C_gamma_TF_total if other STF/readout/source/boundary pieces are zero or separately bounded",
            "numeric_upper_bound": upper,
            "units": gamma["units"],
            "source_row": "R3_gamma",
            "source_value": measured,
            "source_one_sigma": sigma,
            "source_reference": gamma["reference_path_or_url"],
            "bound_status": "CONDITIONAL_COMPONENT_BOUND_NEEDS_DECOMPOSITION",
            "score_ready": False,
            "valid_for_prediction_claim": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "bound_id": "GCB3657_2_Cgradient_TF",
            "coefficient": "C_gradient_TF_gamma",
            "definition": "normalized trace-free radial-gradient/second-derivative contribution from any surviving MTS local field",
            "bound_formula": "abs(C_gradient_TF_gamma) <= C_gamma_TF_total only after readout/source/boundary/non-gradient pieces are zero/bounded",
            "numeric_upper_bound": upper,
            "units": gamma["units"],
            "source_row": "R3_gamma",
            "source_value": measured,
            "source_one_sigma": sigma,
            "source_reference": gamma["reference_path_or_url"],
            "bound_status": "CONDITIONAL_COMPONENT_BOUND_NEEDS_FIELD_PROFILE",
            "score_ready": False,
            "valid_for_prediction_claim": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "bound_id": "GCB3657_3_delta_gamma_MTS",
            "coefficient": "delta_gamma_MTS",
            "definition": "first actual MTS local-GR residual component after 3656",
            "bound_formula": "abs(delta_gamma_MTS) <= 2.3e-05 for any viable local branch",
            "numeric_upper_bound": upper,
            "units": gamma["units"],
            "source_row": "R3_gamma",
            "source_value": measured,
            "source_one_sigma": sigma,
            "source_reference": gamma["reference_path_or_url"],
            "bound_status": "FIRST_MTS_COMPONENT_HAS_NUMERIC_BOUND_NOT_NUMERIC_PREDICTION",
            "score_ready": False,
            "valid_for_prediction_claim": False,
            "claim_allowed": False,
        },
    ]


def delta_gamma_status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status_id": "DGS3657_0_formula",
            "symbol": "delta_gamma_MTS",
            "formula": "(Psi_MTS-Phi_MTS)/Phi_N + q_readout_gamma + q_source_gamma + q_boundary_gamma",
            "current_status": "FORMULA_ACQUIRED",
            "numeric_prediction_status": "MISSING",
            "zero_certificate_status": "NOT_SIGNED",
            "bound_status": "NUMERIC_OBSERVATIONAL_BOUND_AVAILABLE",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "status_id": "DGS3657_1_zero_route",
            "symbol": "S_TF_MTS",
            "formula": "P_TF(E_nonEH_ij + 8*pi*G*T_extra_ij/c^4 + B_boundary_ij + R_readout_ij)",
            "current_status": "TRACEFREE_ZERO_ROUTE_REQUIRES_STRONGER_THAN_ISOTROPY",
            "numeric_prediction_status": "MISSING",
            "zero_certificate_status": "BLOCKED_BY_RADIAL_GRADIENT_COUNTEREXAMPLE",
            "bound_status": "BOUND_ENVELOPE_AVAILABLE",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3657_0_isotropy_not_enough", "local isotropy/spherical symmetry alone cannot prove S_TF_MTS=0", "PASSED_COUNTEREXAMPLE_GATE", "radial gradients generate nonzero trace-free tensors"),
        ("CG3657_1_partial_zero", "perfect-fluid isotropic stress has zero STF part", "PARTIAL_ZERO_ONLY", "this helps ordinary matter but not extra MTS operators/gradients"),
        ("CG3657_2_coefficient_bound", "Cassini gamma gives a numeric bound on total normalized gamma slip", "PASSED_BOUND_GATE_NONCLAIM", "C_gamma_TF_total <= 2.3e-05"),
        ("CG3657_3_no_prediction", "no numeric MTS prediction is claimed", "ACTIVE_GUARD", "component decomposition and field profiles are still missing"),
        ("CG3657_4_next", "next step must derive no-gradient/no-STF operator condition or fill field-profile coefficients", "PROFILE_OR_OPERATOR_ZERO_NEXT", "this is the smallest route to a real delta_gamma_MTS score"),
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
            "status": "STF_ZERO_PROOF_REJECTS_ISOTROPY_ALONE_GAMMA_COEFFICIENT_BOUND_FILLED",
            "summary": "3657 proves ordinary isotropic stress is harmless, rejects isotropy-alone as a zero proof because radial gradients can source STF slip, and fills a Cassini-backed nonclaim gamma coefficient bound.",
            "claim_ceiling": "no MTS gamma prediction, PPN pass, local-GR pass, Newtonian pass, source-calibration pass, WEP/R10/clock/orbital pass, or EH-dominance pass is claimed",
            "useful_result": "The local gamma branch now has a real bound C_gamma_TF_total<=2.3e-5 and a precise next derivation target: eliminate or bound radial-gradient/non-EH STF sources.",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3657_0",
            "target_doc": "3658-Y5-R2FR-no-gradient-STF-operator-condition-or-gamma-profile-coefficient.md",
            "target_script": "scripts/Y5_R2FR_3658_no_gradient_STF_operator_condition_or_gamma_profile_coefficient.py",
            "objective": "try to derive a parent no-gradient/no-STF operator condition for the local branch; failing that, express C_gradient_TF_gamma in terms of local field profile amplitudes and ranges",
            "success_gate": "delta_gamma_MTS obtains either a signed no-STF condition or a profile coefficient formula tied to C_gamma_TF_total<=2.3e-5",
        }
    ]


def write_doc(sources, proof_rows, bounds, status_rows_, delta_rows, gates, next_target) -> None:
    lines = [
        "# 3657 - S_TF_MTS zero proof or gamma coefficient bound",
        "",
        f"**Status:** {status_rows_[0]['summary']}",
        "",
        f"**Claim ceiling:** {status_rows_[0]['claim_ceiling']}.",
        "",
        "## Main result",
        "",
        "This checkpoint takes the leap at `S_TF_MTS` instead of circling the missing-gamma label. The useful result is sharp: ordinary isotropic pressure is harmless, but local isotropy/spherical symmetry alone does **not** prove `S_TF_MTS=0`.",
        "",
        "For a radial local field `X(r)`,",
        "",
        "`P_TF[partial_i X partial_j X] = X_prime^2 (n_i n_j-delta_ij/3)`",
        "",
        "and",
        "",
        "`P_TF[partial_i partial_j X] = (X_second-X_prime/r)(n_i n_j-delta_ij/3)`.",
        "",
        "So a surviving radial-gradient or second-derivative operator can create gamma slip even in a spherical local branch. The zero proof needs a stronger parent condition: no trace-free non-EH operator, no extra anisotropic stress, no boundary STF term, and no readout STF term in the same observed frame.",
        "",
        "Since that parent condition is not signed yet, 3657 fills the honest numeric handle: Cassini gives `C_gamma_TF_total <= 2.3e-05` as a source-backed nonclaim bound on total normalized gamma slip.",
        "",
        "## STF zero-proof attempt",
    ]
    for row in proof_rows:
        lines.append(f"- `{row['proof_id']}`: {row['zero_status']} - {row['statement']}")
    lines.extend(["", "## Gamma coefficient bounds"])
    for row in bounds:
        lines.append(f"- `{row['bound_id']}`: `{row['coefficient']}` <= `{row['numeric_upper_bound']}` - {row['bound_status']}")
    lines.extend(["", "## Delta-gamma status"])
    for row in delta_rows:
        lines.append(f"- `{row['status_id']}`: `{row['symbol']}` - {row['current_status']} / {row['bound_status']}")
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


def validate(ts, output_paths, sources, proof_rows, bounds, delta_rows, gates, status_rows_, next_target) -> list[dict[str, object]]:
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

    add("VAL3657_0_sources_exist", all(row["exists"] for row in sources), "every cited local source path exists")
    add("VAL3657_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3657_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3657 outputs written")
    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    add("VAL3657_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3657_4_counterexample_present", any(row["zero_status"] == "ISOTROPY_ALONE_REJECTED" and "X_prime" in row["formula"] for row in proof_rows), "radial-gradient counterexample recorded")
    add("VAL3657_5_partial_zero_present", any(row["zero_status"] == "PARTIAL_ZERO_DERIVED_FOR_ISOTROPIC_MATTER_ONLY" for row in proof_rows), "ordinary isotropic matter partial zero recorded")
    add("VAL3657_6_zero_not_accepted", not any(str(row["accepted_as_zero"]).lower() == "true" for row in proof_rows), "no full S_TF zero accepted")
    add("VAL3657_7_gamma_bound_numeric", any(row["coefficient"] == "C_gamma_TF_total" and parse_float(row["numeric_upper_bound"]) == 2.3e-05 for row in bounds), "Cassini gamma coefficient bound filled")
    add("VAL3657_8_bounds_nonclaim", not any(str(row.get("score_ready", "")).lower() == "true" or str(row.get("valid_for_prediction_claim", "")).lower() == "true" for row in bounds), "coefficient bounds remain nonclaim")
    add("VAL3657_9_delta_status_bound_available", any(row["symbol"] == "delta_gamma_MTS" and row["bound_status"] == "NUMERIC_OBSERVATIONAL_BOUND_AVAILABLE" for row in delta_rows), "delta_gamma_MTS has observational bound status")
    add("VAL3657_10_claim_gates_present", {"CG3657_0_isotropy_not_enough", "CG3657_2_coefficient_bound", "CG3657_3_no_prediction", "CG3657_4_next"}.issubset({row["gate_id"] for row in gates}), "core claim gates present")
    generated = sources + proof_rows + bounds + delta_rows + gates + status_rows_ + next_target
    add("VAL3657_11_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim")
    doc_text = read_text(DOC)
    add("VAL3657_12_doc_written", "C_gamma_TF_total <= 2.3e-05" in doc_text and "does **not** prove" in doc_text and "radial-gradient" in doc_text, "doc records counterexample and coefficient bound")
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3657*", "3657-Y5-R2FR-*", "Y5_R2FR_3657_*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3657_13_no_formalization_leak", not leaks, "no 3657 checkpoint files in formalization-workbench")
    add("VAL3657_14_next_target", next_target[0]["target_doc"].startswith("3658-") and "no-gradient" in next_target[0]["target_doc"], "3658 no-gradient/profile target selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    proof_rows = stf_zero_proof_rows(ts)
    bounds = gamma_coefficient_bound_rows(ts)
    delta_rows = delta_gamma_status_rows(ts)
    gates = claim_gate_rows(ts)
    status_rows_ = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3657_SOURCE_REGISTER.csv",
        "proof": RESIDUALS / "P8_Y5_R2FR_3657_STF_ZERO_PROOF_ATTEMPT.csv",
        "bounds": RESIDUALS / "P8_Y5_R2FR_3657_GAMMA_COEFFICIENT_BOUND_ROWS.csv",
        "delta": RESIDUALS / "P8_Y5_R2FR_3657_DELTA_GAMMA_STATUS_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3657_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3657_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3657_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3657_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["proof"], proof_rows)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["delta"], delta_rows)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status_rows_)
    write_csv(outputs["next"], next_target)
    write_doc(sources, proof_rows, bounds, status_rows_, delta_rows, gates, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, proof_rows, bounds, delta_rows, gates, status_rows_, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3657 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3657 checkpoint with {len(validation)} validation checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
