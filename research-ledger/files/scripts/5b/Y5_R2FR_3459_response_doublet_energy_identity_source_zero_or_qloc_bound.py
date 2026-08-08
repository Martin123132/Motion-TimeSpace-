from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3459-Y5-R2FR-response-doublet-energy-identity-source-zero-or-q_loc-bound-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "script_3459": Path(__file__).resolve(),
    "doc_3458": ROOT / "3458-Y5-R2FR-live-MTS-action-instantiation-of-Hilbert-Khat-contract-under-AX1090.md",
    "candidate_3458": OUT / "P8_Y5_R2FR_3458_PARENT_ACTION_CANDIDATE.csv",
    "residual_3458": OUT / "P8_Y5_R2FR_3458_RESIDUAL_VECTOR_AFTER_INSTANTIATION.csv",
    "energy_target_3458": OUT / "P8_Y5_R2FR_3458_ENERGY_IDENTITY_TARGET.csv",
    "doc_1011": ROOT / "1011-Y5-R10-response-doublet-source-current-zero-or-q_loc-bound-fill.md",
    "theorem_1011": OUT / "P8_Y5_R10_1011_RESPONSED_DOUBLET_THEOREM_ATTEMPT.csv",
    "bound_1011": OUT / "P8_Y5_R10_1011_QLOC_BOUND_FILL_ROWS.csv",
    "doublet_action_3413": OUT / "P8_Y5_R2FR_3413_RESPONSE_DOUBLET_ACTION.csv",
    "kmetric_3419": OUT / "P8_Y5_R2FR_3419_RESPONSE_DOUBLET_KMETRIC_EXPANSION.csv",
    "adoption_2967": OUT / "P8_Y5_R2FR_2967_RESPONSE_DOUBLET_ADOPTION_GATE.csv",
    "owner_2977": OUT / "P8_Y5_R2FR_2977_RESPONSE_DOUBLET_OWNER_LOCK_AUDIT.csv",
    "doublet_variation": OUT / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv",
    "doublet_contract": OUT / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
    "euler_source": OUT / "P8_RESPONSE_DOUBLET_EULER_SOURCE_LEDGER.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body: list[str] = []
    for row in rows:
        vals = []
        for field in fields:
            vals.append(str(row.get(field, "")).replace("\n", "<br>").replace("|", "/"))
        body.append("| " + " | ".join(vals) + " |")
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    roles = {
        "script_3459": "generator for this checkpoint",
        "doc_3458": "live Hilbert-Khat instantiation predecessor",
        "candidate_3458": "parent action candidate input",
        "residual_3458": "residual vector input",
        "energy_target_3458": "energy identity target input",
        "doc_1011": "older response-doublet source-current theorem/bound attempt",
        "theorem_1011": "old doublet obstruction theorem rows",
        "bound_1011": "old q_loc bound fill rows",
        "doublet_action_3413": "newer doublet action rows",
        "kmetric_3419": "K_metric expansion at Z=0",
        "adoption_2967": "response-doublet adoption gate",
        "owner_2977": "response-doublet owner lock audit",
        "doublet_variation": "response-doublet variation rows",
        "doublet_contract": "response-doublet contract rows",
        "euler_source": "Euler source ledger",
    }
    return [
        {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "source_id": key,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[key],
        }
        for key, path in SOURCES.items()
    ]


def energy_identity_derivation() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "EID3459_0_operator_definition",
            "statement": "For the 3458 doublet sector, define L_AB Z^B := M_AB Z^B - nabla_mu(H_AB^{mu nu} nabla_nu Z^B) + lower-order covariant terms after gauge/constraint removal.",
            "derived_result": "Euler equation has normal form L_AB Z^B = J_A + B_A in the local collar, where J_A is source/readout work and B_A denotes boundary/improvement support.",
            "needed_condition": "L_AB self-adjoint on the declared local domain",
            "status": "FORMAL_NORMAL_FORM",
            "source_path": str(SOURCES["candidate_3458"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "step_id": "EID3459_1_integrated_identity",
            "statement": "Multiply by Z^A, integrate over U, and integrate derivative terms by parts.",
            "derived_result": "int_U Z^A L_AB Z^B = int_U Z^A J_A + boundary_flux[Z,H,n,B_GK]",
            "needed_condition": "all boundary terms are either included in boundary_flux or canceled by an improvement term",
            "status": "DERIVED_ENERGY_IDENTITY",
            "source_path": str(SOURCES["doublet_variation"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "step_id": "EID3459_2_positive_operator_bound",
            "statement": "If L_AB is positive on the quotient/gauge-fixed domain with spectral floor lambda_min>0, then int Z L Z >= lambda_min ||Z||^2.",
            "derived_result": "lambda_min ||Z||^2 <= ||Z|| ||J|| + |boundary_flux|",
            "needed_condition": "lambda_min positive, units declared, and zero modes/gauge modes removed",
            "status": "CONDITIONAL_POSITIVE_BOUND",
            "source_path": str(SOURCES["owner_2977"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "step_id": "EID3459_3_sharp_amplitude_envelope",
            "statement": "Solve the quadratic inequality lambda_min x^2 <= x j + b for x=||Z||, j=||J||, b=|boundary_flux|.",
            "derived_result": "||Z|| <= (||J|| + sqrt(||J||^2 + 4 lambda_min |boundary_flux|))/(2 lambda_min)",
            "needed_condition": "lambda_min>0 and nonnegative boundary-flux envelope",
            "status": "DERIVED_AMPLITUDE_BOUND",
            "source_path": str(SOURCES["energy_target_3458"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "step_id": "EID3459_4_zero_theorem",
            "statement": "If J_A=0 and boundary_flux=0, positivity gives ||Z||=0.",
            "derived_result": "Z=0, Gamma_X-Gamma0=0, first variation vanishes, K_H has no linear local tail, and q_loc=0 provided K_hat=K_H and P_loc(0)=0.",
            "needed_condition": "source-current zero, boundary no-flux, Hilbert-Khat branch adoption, and projector ownership",
            "status": "CONDITIONAL_LOCAL_ZERO_THEOREM",
            "source_path": str(SOURCES["doublet_contract"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def source_zero_gate() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "SZG3459_0_exchange_symmetry",
            "candidate_zero": "exchange symmetry Z -> -Z forbids odd linear source terms",
            "current_status": "CONDITIONAL_ONLY",
            "why_not_closed": "exchange symmetry must cover matter, clocks, readout, source normalization, boundary and stress channels",
            "live_counterpressure": "Y5 source-normalization and Y6 extra-stress channels can be exchange-even and still physical",
            "next_evidence": "parent source-current owner theorem or explicit residual coefficient",
            "source_path": str(SOURCES["doc_1011"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "SZG3459_1_source_current",
            "candidate_zero": "J_A=0 on compact local branch",
            "current_status": "NOT_DERIVED",
            "why_not_closed": "old and current ledgers retain source/readout work and source-normalization debts",
            "live_counterpressure": "relative source weights and measured-G/source calibration can survive covariance",
            "next_evidence": "source-label-forgetting plus same Hilbert Noether current owner",
            "source_path": str(SOURCES["euler_source"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "SZG3459_2_boundary_flux",
            "candidate_zero": "boundary_flux=0",
            "current_status": "OPEN",
            "why_not_closed": "boundary/support/collar terms can survive even when bulk density is quadratic",
            "live_counterpressure": "KME3419_4 boundary terms can be O(1) or O(Z)",
            "next_evidence": "fixed reference class, compact support, or explicit boundary improvement",
            "source_path": str(SOURCES["kmetric_3419"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "SZG3459_3_positive_floor",
            "candidate_zero": "lambda_min>0 after gauge and constraint removal",
            "current_status": "FORMAL_CANDIDATE_ONLY",
            "why_not_closed": "M_AB/H_AB owner, units, gauge quotient, zero-mode removal and local domain are unsigned",
            "live_counterpressure": "a zero mode would turn the amplitude theorem into a bound-only branch",
            "next_evidence": "spectral floor row or symbolic positivity proof",
            "source_path": str(SOURCES["owner_2977"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def residual_bounds() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "RDB3459_0_Z_amplitude",
            "quantity": "||Z||",
            "bound_formula": "||Z|| <= (||J|| + sqrt(||J||^2 + 4 lambda_min |B_flux|))/(2 lambda_min)",
            "zero_limit": "J=0 and B_flux=0 imply Z=0",
            "missing_inputs": "lambda_min;J_norm;B_flux_norm;domain_U;norm_convention;source_path",
            "status": "FORMULA_DERIVED_INPUTS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "RDB3459_1_q_loc_Hilbert_branch",
            "quantity": "Q_q_loc",
            "bound_formula": "Q_q_loc <= N_P [Q_source_work + Q_boundary_flux] when K_hat=K_H; add Q_DeltaK if old K_hat remains independent",
            "zero_limit": "source work, boundary flux and Delta_K all zero",
            "missing_inputs": "N_P;Q_source_work;Q_boundary_flux;Q_DeltaK;P_loc definition",
            "status": "RESIDUAL_BOUND_STRUCTURE_READY",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "RDB3459_2_second_order_stress_tail",
            "quantity": "T_GK local tail",
            "bound_formula": "||T_GK|| <= C_T ||Z||^2 + C_grad ||nabla Z||^2 plus boundary/improvement terms",
            "zero_limit": "Z=0 and boundary/improvement zero",
            "missing_inputs": "C_T;C_grad;gradient elliptic estimate;boundary term",
            "status": "TAIL_BOUND_TEMPLATE_READY",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "RDB3459_3_PPN_envelope",
            "quantity": "delta_PPN from q_loc",
            "bound_formula": "|delta gamma_PPN| <= c^2 N_G N_D Q_q_loc/(2 U_min)",
            "zero_limit": "Q_q_loc=0",
            "missing_inputs": "N_G;N_D;U_min;metric solution map",
            "status": "PPN_MAP_STILL_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def theorem_status() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "THS3459_0_math_progress",
            "question": "Did the derivation move forward?",
            "answer": "Yes. The response-doublet route now has a derived energy identity, a sharp amplitude bound, and an exact zero theorem under named source/boundary/positivity clauses.",
            "verdict": "DERIVATION_PROGRESS_REAL",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "status_id": "THS3459_1_local_GR_claim",
            "question": "Can local GR or PPN be claimed?",
            "answer": "No. The source-current owner, boundary flux, positivity floor, projector, and PPN map remain unsigned or input-missing.",
            "verdict": "CLAIM_BLOCKED_BUT_BOUNDABLE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "status_id": "THS3459_2_root_pressure",
            "question": "What is the next root pressure?",
            "answer": "The source-current owner is now the sharpest blocker: especially Y5 measured-G/source normalization and visible matter/readout descent.",
            "verdict": "ATTACK_SOURCE_OWNER_NEXT",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3459_0_best_next",
            "decision": "Keep the response-doublet route alive, but move the main attack from algebraic double-zero to source-current ownership.",
            "reason": "The energy identity proves that if source and boundary terms vanish, the amplitude vanishes. Therefore the remaining fight is whether the parent theory really gives J_A=B_flux=0 or only a small bounded residual.",
            "next_action": "Derive source-label forgetting / same Noether current owner for J_A=0, or emit source-normalization residual bounds.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3460-Y5-R2FR-source-current-owner-for-doublet-or-Y5-source-normalization-bound-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_3460_source_current_owner_for_doublet_or_Y5_source_normalization_bound.py",
            "objective": "Attack J_A=0 directly by deriving the parent source-current owner/source-label-forgetting theorem for visible matter and measured-G/source normalization; if it fails, emit explicit Y5 source-normalization residual bounds feeding 3459.",
            "success_gate": "Either J_A=0 is parent-derived for the local branch, or J_norm/Y5 source-normalization residual rows are concrete enough to plug into RDB3459_0 and RDB3459_1.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def formalization_modified_count_since(start_utc: datetime) -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        try:
            mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        except OSError:
            continue
        if mtime >= start_utc:
            count += 1
    return count


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    energy_rows = rows_by_name["energy_identity_derivation"]
    gate_rows = rows_by_name["source_zero_gate"]
    bound_rows = rows_by_name["residual_bounds"]
    status_rows = rows_by_name["theorem_status"]
    next_rows = rows_by_name["next_target"]

    generated_paths = [
        OUT / "P8_Y5_R2FR_3459_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R2FR_3459_ENERGY_IDENTITY_DERIVATION.csv",
        OUT / "P8_Y5_R2FR_3459_SOURCE_ZERO_GATE.csv",
        OUT / "P8_Y5_R2FR_3459_RESIDUAL_BOUNDS.csv",
        OUT / "P8_Y5_R2FR_3459_THEOREM_STATUS.csv",
        OUT / "P8_Y5_R2FR_3459_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R2FR_3459_NEXT_TARGET.csv",
    ]
    csv_parse_ok = True
    csv_details: list[str] = []
    for path in generated_paths:
        try:
            parsed = read_csv(path)
            csv_details.append(f"{path.name}:{len(parsed)}")
        except Exception as exc:
            csv_parse_ok = False
            csv_details.append(f"{path.name}:{exc}")

    checks: list[dict[str, Any]] = []
    checks.append(
        {
            "check_id": "VAL3459_0_sources_exist",
            "description": "all source paths exist",
            "passed": all(bool(row["exists"]) for row in source_rows),
            "detail": f"{sum(1 for row in source_rows if row['exists'])}/{len(source_rows)} source paths exist",
        }
    )
    checks.append(
        {
            "check_id": "VAL3459_1_energy_identity_derived",
            "description": "energy identity and integrated source/boundary form are present",
            "passed": any(row["step_id"] == "EID3459_1_integrated_identity" and "int_U Z^A L_AB Z^B" in str(row["derived_result"]) for row in energy_rows),
            "detail": ";".join(row["step_id"] for row in energy_rows),
        }
    )
    checks.append(
        {
            "check_id": "VAL3459_2_sharp_bound_present",
            "description": "sharp amplitude bound is present",
            "passed": any("sqrt(||J||^2 + 4 lambda_min |boundary_flux|)" in str(row["derived_result"]) for row in energy_rows)
            and any("sqrt(||J||^2 + 4 lambda_min |B_flux|)" in str(row["bound_formula"]) for row in bound_rows),
            "detail": ";".join(row["bound_id"] for row in bound_rows),
        }
    )
    checks.append(
        {
            "check_id": "VAL3459_3_source_gates_explicit",
            "description": "source, boundary and positivity gates are explicit",
            "passed": {"SZG3459_1_source_current", "SZG3459_2_boundary_flux", "SZG3459_3_positive_floor"}.issubset(
                {row["gate_id"] for row in gate_rows}
            ),
            "detail": ";".join(row["gate_id"] for row in gate_rows),
        }
    )
    checks.append(
        {
            "check_id": "VAL3459_4_no_claims",
            "description": "all theorem/bound/status rows remain nonclaim",
            "passed": all(
                str(row.get("claim_allowed", "False")) == "False"
                for rows in rows_by_name.values()
                for row in rows
                if isinstance(row, dict)
            ),
            "detail": "claim_allowed=false across generated rows",
        }
    )
    checks.append(
        {
            "check_id": "VAL3459_5_csv_parse",
            "description": "generated CSV files parse cleanly",
            "passed": csv_parse_ok,
            "detail": ";".join(csv_details),
        }
    )
    checks.append(
        {
            "check_id": "VAL3459_6_next_target_3460",
            "description": "next target is source-current owner/Y5 bound",
            "passed": len(next_rows) == 1 and "3460-Y5-R2FR-source-current-owner" in str(next_rows[0]["next_doc"]),
            "detail": str(next_rows[0]["next_doc"]) if next_rows else "missing next row",
        }
    )
    checks.append(
        {
            "check_id": "VAL3459_7_progress_not_claim",
            "description": "status distinguishes derivation progress from local-GR claim",
            "passed": any(row["verdict"] == "DERIVATION_PROGRESS_REAL" for row in status_rows)
            and any(row["verdict"] == "CLAIM_BLOCKED_BUT_BOUNDABLE" for row in status_rows),
            "detail": ";".join(row["verdict"] for row in status_rows),
        }
    )
    modified_count = formalization_modified_count_since(start_utc)
    checks.append(
        {
            "check_id": "VAL3459_8_formalization_untouched",
            "description": "formalization-workbench unchanged during this script",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        }
    )
    overall = all(bool(row["passed"]) for row in checks)
    checks.append(
        {
            "check_id": "VAL3459_9_overall",
            "description": "3459 response-doublet energy identity checkpoint is internally valid",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
        }
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3459 - Response-Doublet Energy Identity, Source Zero, Or q_loc Bound Under AX1090",
        "",
        "## Purpose",
        "",
        "This checkpoint derives the energy identity behind the 3458 response-doublet parent action. The point is to turn the remaining local-GR gap into a proof-or-bound problem: either the source and boundary terms vanish and the doublet amplitude is zero, or the same identity gives a quantitative residual envelope.",
        "",
        "## Source Register",
        "",
        md_table(rows_by_name["source_register"]),
        "",
        "## Energy Identity Derivation",
        "",
        md_table(rows_by_name["energy_identity_derivation"]),
        "",
        "## Source Zero Gate",
        "",
        md_table(rows_by_name["source_zero_gate"]),
        "",
        "## Residual Bounds",
        "",
        md_table(rows_by_name["residual_bounds"]),
        "",
        "## Theorem Status",
        "",
        md_table(rows_by_name["theorem_status"]),
        "",
        "## Decision Ledger",
        "",
        md_table(rows_by_name["decision_ledger"]),
        "",
        "## Next Target",
        "",
        md_table(rows_by_name["next_target"]),
        "",
        "## Validation",
        "",
        md_table(rows_by_name["validation"]),
        "",
        "## Bottom Line",
        "",
        "- Derived: `int_U Z^A L_AB Z^B = int_U Z^A J_A + boundary_flux`, with the sharp amplitude envelope for `||Z||`.",
        "- Conditional win: if `J_A=0`, boundary flux is zero, `lambda_min>0`, `K_hat=K_H`, and `P_loc(0)=0`, then the doublet amplitude vanishes and the local `q_loc` branch is zero.",
        "- Remaining blocker: the source-current owner, especially Y5 measured-G/source normalization, is now the next root pressure.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "energy_identity_derivation": energy_identity_derivation(),
        "source_zero_gate": source_zero_gate(),
        "residual_bounds": residual_bounds(),
        "theorem_status": theorem_status(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }
    output_map = {
        "source_register": OUT / "P8_Y5_R2FR_3459_SOURCE_REGISTER.csv",
        "energy_identity_derivation": OUT / "P8_Y5_R2FR_3459_ENERGY_IDENTITY_DERIVATION.csv",
        "source_zero_gate": OUT / "P8_Y5_R2FR_3459_SOURCE_ZERO_GATE.csv",
        "residual_bounds": OUT / "P8_Y5_R2FR_3459_RESIDUAL_BOUNDS.csv",
        "theorem_status": OUT / "P8_Y5_R2FR_3459_THEOREM_STATUS.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3459_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3459_NEXT_TARGET.csv",
    }
    for name, path in output_map.items():
        write_csv(path, rows_by_name[name])
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    write_csv(OUT / "P8_Y5_BRR545_3459_VALIDATION.csv", rows_by_name["validation"])
    write_doc(rows_by_name)
    print(f"wrote {DOC}")
    print("wrote 8 csv outputs")


if __name__ == "__main__":
    main()
