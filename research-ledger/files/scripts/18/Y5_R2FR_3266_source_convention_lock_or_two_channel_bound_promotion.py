from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3266-Y5-R2FR-source-convention-lock-or-two-channel-bound-promotion-under-AX1090.md"
DOC_3265 = ROOT / "3265-Y5-R2FR-second-material-arena-or-parent-no-cancellation-theorem-under-AX1090.md"
DD_TEX = ROOT / "source-intake" / "external-sources" / "damour_donoghue_1007.2792_source" / "DamourDonoghueEPfinal.tex"
EOT_TEX = ROOT / "source-intake" / "external-sources" / "eotwash_0712.0607_source" / "ep.tex"
DELTA_MATRIX = OUT / "P8_Y5_R2FR_3265_TWO_ARENA_DELTA_MATRIX_NONCLAIM.csv"
RANK_3265 = OUT / "P8_Y5_R2FR_3265_RANK_AND_CONDITIONING.csv"
BOUNDS_3265 = OUT / "P8_Y5_R2FR_3265_CONDITIONAL_TWO_CHANNEL_BOUNDS_NONCLAIM.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3266_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3266_RESIDUAL_INCLUSIVE_INVERSION_THEOREM.csv",
    "inverse": OUT / "P8_Y5_R2FR_3266_MATRIX_INVERSE_AND_RESIDUAL_GAINS.csv",
    "clauses": OUT / "P8_Y5_R2FR_3266_SOURCE_CONVENTION_LOCK_CLAUSES.csv",
    "contract": OUT / "P8_Y5_R2FR_3266_PROMOTION_CONTRACT.csv",
    "gates": OUT / "P8_Y5_R2FR_3266_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3266_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3266_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3266_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        read_csv(path)
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def evidence(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_number, line in enumerate(handle, start=1):
            lowered_line = line.lower()
            if any(needle in lowered_line for needle in lowered_needles):
                clean = " ".join(line.strip().split())
                if clean:
                    hits.append(f"L{line_number}:{clean[:280]}")
            if len(hits) >= limit:
                break
    return " | ".join(hits) if hits else "NO_MATCH"


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC3266_3265_handoff",
            DOC_3265,
            "3265 rank-two conditional inversion result",
            ["rank two", "parent source-convention lock", "VAL3265_9_overall"],
        ),
        (
            "SRC3266_DD_two_channel",
            DD_TEX,
            "DD two-channel body-charge convention",
            ["D_{\\hat m} Q'_{\\hat m}", "Q'_{\\hat m}", "Q'_{e}"],
        ),
        (
            "SRC3266_EOTWASH_BeTi",
            EOT_TEX,
            "Eot-Wash Be/Ti arena source and eta row",
            ["beryllium and titanium", "eta(\\mbox{Be}-\\mbox{Ti})", "elliptical layered Earth model"],
        ),
        (
            "SRC3266_delta_matrix",
            DELTA_MATRIX,
            "Two-row DD delta matrix from 3265",
            ["DM3265_0_MICROSCOPE", "DM3265_1_EOTWASH"],
        ),
        (
            "SRC3266_rank",
            RANK_3265,
            "Rank and conditioning result from 3265",
            ["RANK3265_0_two_arena_DD_matrix"],
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, role, needles in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def matrix_values() -> tuple[float, float, float, float, float, float]:
    rows = read_csv(DELTA_MATRIX)
    a = float(rows[0]["Delta_Qhatm_prime"])
    b = float(rows[0]["Delta_Qe_prime"])
    c = float(rows[1]["Delta_Qhatm_prime"])
    d = float(rows[1]["Delta_Qe_prime"])
    b1 = float(rows[0]["eta_abs_bound"])
    b2 = float(rows[1]["eta_abs_bound"])
    return a, b, c, d, b1, b2


def inverse_values() -> tuple[float, float, float, float, float]:
    a, b, c, d, _, _ = matrix_values()
    det = a * d - b * c
    return det, d / det, -b / det, -c / det, a / det


def theorem_rows() -> list[dict[str, Any]]:
    det, inv00, inv01, inv10, inv11 = inverse_values()
    return [
        {
            "theorem_id": "THM3266_0_residual_inclusive_two_arena_inversion",
            "statement": "For eta = A D + epsilon with A rank two, D=A^{-1}(eta-epsilon). Therefore |D_j| is bounded by the absolute inverse row applied to |eta|+|epsilon|.",
            "proof": "A is a 2x2 matrix of DD material-charge differences. det(A) != 0 by 3265. Left-multiply by A^{-1}; take componentwise absolute values and the triangle inequality.",
            "determinant": f"{det:.12e}",
            "result": "|D_hatm| <= |inv00|(b1+e1)+|inv01|(b2+e2); |D_e| <= |inv10|(b1+e1)+|inv11|(b2+e2)",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "THM3266_1_zero_residual_special_case",
            "statement": "If epsilon_1=epsilon_2=0 and the two arenas share the same parent D coordinates, 3265's finite two-channel bounds follow exactly.",
            "proof": "Set e1=e2=0 in THM3266_0.",
            "determinant": f"{det:.12e}",
            "result": f"absolute inverse = [[{inv00:.12e},{inv01:.12e}],[{inv10:.12e},{inv11:.12e}]]",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "THM3266_2_no_unbounded_cancellation",
            "statement": "A cancellation direction for one material row is not a cancellation direction for the other unless D=0, up to residual budgets.",
            "proof": "The nullspaces of two nonparallel rows in R^2 intersect trivially because det(A) != 0.",
            "determinant": f"{det:.12e}",
            "result": "single-row cancellation becomes a bounded parallelogram once residual budgets are supplied",
            "valid_for_claim": "false",
        },
    ]


def inverse_rows() -> list[dict[str, Any]]:
    det, inv00, inv01, inv10, inv11 = inverse_values()
    _, _, _, _, b1, b2 = matrix_values()
    scenarios = [
        ("zero_residual", 0.0, 0.0),
        ("ten_percent_eta_residual", 0.1 * b1, 0.1 * b2),
        ("eta_sized_residual", b1, b2),
    ]
    rows: list[dict[str, Any]] = [
        {
            "gain_id": "GAIN3266_0_inverse_coefficients",
            "scenario": "matrix_inverse",
            "determinant": f"{det:.12e}",
            "inv00_Dhatm_from_MICROSCOPE": f"{inv00:.12e}",
            "inv01_Dhatm_from_EOTWASH": f"{inv01:.12e}",
            "inv10_De_from_MICROSCOPE": f"{inv10:.12e}",
            "inv11_De_from_EOTWASH": f"{inv11:.12e}",
            "Dhatm_bound": "",
            "De_bound": "",
            "valid_for_claim": "false",
        }
    ]
    for scenario, e1, e2 in scenarios:
        rows.append(
            {
                "gain_id": f"GAIN3266_{len(rows)}_{scenario}",
                "scenario": scenario,
                "determinant": f"{det:.12e}",
                "inv00_Dhatm_from_MICROSCOPE": f"{inv00:.12e}",
                "inv01_Dhatm_from_EOTWASH": f"{inv01:.12e}",
                "inv10_De_from_MICROSCOPE": f"{inv10:.12e}",
                "inv11_De_from_EOTWASH": f"{inv11:.12e}",
                "epsilon_MICROSCOPE": f"{e1:.12e}",
                "epsilon_EOTWASH": f"{e2:.12e}",
                "Dhatm_bound": f"{abs(inv00) * (b1 + e1) + abs(inv01) * (b2 + e2):.12e}",
                "De_bound": f"{abs(inv10) * (b1 + e1) + abs(inv11) * (b2 + e2):.12e}",
                "valid_for_claim": "false",
            }
        )
    return rows


def clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "LOCK3266_0_common_field",
            "required_clause": "Both arenas must couple to the same parent MTS residual/source field, not two arena-specific fields.",
            "mathematical_form": "D_i is arena-independent: D_i^MICROSCOPE = D_i^EOTWASH = D_i",
            "status": "UNSIGNED_PARENT_ACTION_CLAUSE",
            "if_missing": "matrix inversion bounds the wrong variables: D_i^1 and D_i^2 rather than one common D_i",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "LOCK3266_1_common_DD_basis",
            "required_clause": "MTS parent source charge must reduce to the same DD basis Q'_hatm,Q'_e used in both material rows.",
            "mathematical_form": "alpha_A-alpha_B = DeltaQ_hatm D_hatm + DeltaQ_e D_e + residual",
            "status": "CONDITIONALLY_DERIVED_FROM_DD_NOT_PARENT_SIGNED",
            "if_missing": "Be/Ti and Ti/Pt rows may be calibration coordinates only",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "LOCK3266_2_source_normalization",
            "required_clause": "Earth/source normalization and eta readout must be absorbed into the same D_i convention or explicit residual epsilons.",
            "mathematical_form": "eta_k = row_k dot D + epsilon_k, with no hidden scale s_k of unknown sign",
            "status": "PARTIAL_SOURCE_BACKING_NOT_PARENT_LOCKED",
            "if_missing": "unknown s_k rescales rows and can fake or erase bounds",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "LOCK3266_3_residual_budget",
            "required_clause": "All omitted channels must be bounded as epsilon_MICROSCOPE and epsilon_EOTWASH.",
            "mathematical_form": "|epsilon_k| <= e_k supplied before promotion",
            "status": "EXACT_BOUND_LAW_DERIVED_BUT_NUMERIC_EPSILONS_MISSING",
            "if_missing": "finite zero-residual bounds remain smoke only",
            "valid_for_claim": "false",
        },
    ]


def contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "CON3266_0_parent_action_signature",
            "deliverable": "parent action/source map clause",
            "must_supply": "variation showing one local parent source current projects to Q'_hatm and Q'_e with arena-independent D_hatm,D_e",
            "acceptance_test": "LOCK3266_0 and LOCK3266_1 become signed without adding experiment-specific coefficients",
            "current_status": "missing",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CON3266_1_residual_rows",
            "deliverable": "epsilon_MICROSCOPE and epsilon_EOTWASH budgets",
            "must_supply": "numeric or theorem-zero bounds on readout, source-profile, omitted DD channels, material tensor errors",
            "acceptance_test": "THM3266_0 computes promoted bounds with explicit e1,e2 instead of zero-residual assumptions",
            "current_status": "law derived; numeric epsilons missing",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CON3266_2_promotion_gate",
            "deliverable": "two-channel WEP promotion row",
            "must_supply": "all source lock clauses signed and residual budgets smaller than chosen tolerance",
            "acceptance_test": "claim_allowed may become true only after validation proves no unsigned clauses remain",
            "current_status": "blocked for claim, not blocked for derivation",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG3266_0_exact_residual_law",
            "gate": "residual-inclusive inversion theorem derived",
            "passed": "true",
            "reason": "A^{-1} propagation law is exact for two rows and explicit epsilons",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3266_1_parent_source_lock",
            "gate": "same parent D coordinates across arenas",
            "passed": "false",
            "reason": "requires parent action/source-map signature, not merely external DD phenomenology",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3266_2_residual_budget",
            "gate": "numeric residual budgets supplied",
            "passed": "false",
            "reason": "epsilon_MICROSCOPE and epsilon_EOTWASH are variables in the theorem, not sourced numbers yet",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3266_3_local_GR",
            "gate": "local GR/Newton/Maxwell promotion",
            "passed": "false",
            "reason": "WEP source-coupling lock is a local-sector gate, not the full local GR derivation",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3266_0",
            "verdict": "EXACT_PROMOTION_CONTRACT_DERIVED_NOT_SIGNED",
            "what_moved": "The vague blocker became eta=A D+epsilon with exact A^{-1} residual propagation; cancellation is no longer hand-wavy.",
            "best_next": "try to derive CON3266_0 parent action/source-map signature directly from the MTS local matter action grammar",
            "fallback_next": "source numeric epsilon budgets and keep the result as a bounded two-channel WEP smoke branch",
            "valid_for_claim": "false",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3266_0_3267",
            "selected": "primary",
            "target_doc": "3267-Y5-R2FR-parent-source-map-signature-for-DD-coordinates-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3267_parent_source_map_signature_for_DD_coordinates.py",
            "objective": "Attempt the actual derivation of the parent source map that makes D_hatm and D_e arena-independent MTS coordinates.",
            "guardrail": "If the parent map introduces arena-specific scale factors, keep them explicit and do not promote the WEP branch.",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_count() -> int:
    if not FW.exists():
        return 0
    script_mtime = Path(__file__).stat().st_mtime
    return sum(1 for path in FW.rglob("*") if path.is_file() and path.stat().st_mtime > script_mtime)


def validation_rows() -> list[dict[str, Any]]:
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = source_register()
    rank_two = read_csv(RANK_3265)[0].get("rank_two") == "true"
    inverse_finite = all(
        math.isfinite(float(row[key]))
        for row in inverse_rows()
        for key in [
            "determinant",
            "inv00_Dhatm_from_MICROSCOPE",
            "inv01_Dhatm_from_EOTWASH",
            "inv10_De_from_MICROSCOPE",
            "inv11_De_from_EOTWASH",
        ]
    )
    promoted = any(row["claim_allowed"] == "true" for row in claim_gate_rows())
    validations = [
        {
            "check_id": "VAL3266_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": bool_str(all(row["exists"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["exists"] != "true"),
        },
        {
            "check_id": "VAL3266_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": bool_str(all(row["parse_ok"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["parse_ok"] != "true"),
        },
        {
            "check_id": "VAL3266_2_rank_input_true",
            "check": "3265 rank-two input is true",
            "passed": bool_str(rank_two),
            "detail": f"rank_two={rank_two}",
        },
        {
            "check_id": "VAL3266_3_inverse_finite",
            "check": "inverse coefficients and residual gains are finite",
            "passed": bool_str(inverse_finite),
            "detail": "all inverse coefficients finite",
        },
        {
            "check_id": "VAL3266_4_outputs_parse",
            "check": "all 3266 output CSVs parse",
            "passed": bool_str(all(csv_ok(path) for path in output_paths)),
            "detail": ";".join(str(path) for path in output_paths if not csv_ok(path)),
        },
        {
            "check_id": "VAL3266_5_no_claim_promotion",
            "check": "no claim gate allows WEP/local-GR promotion",
            "passed": bool_str(not promoted),
            "detail": "all claim_allowed=false",
        },
        {
            "check_id": "VAL3266_6_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3266_7_overall",
            "check": "3266 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3266_7_overall")
    validations[-1]["passed"] = bool_str(overall)
    validations[-1]["detail"] = "all required checks passed" if overall else "one or more checks failed"
    return validations


def write_doc() -> None:
    sources = source_register()
    theorem = theorem_rows()
    inverse = inverse_rows()
    clauses = clause_rows()
    contract = contract_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()
    validations = validation_rows()
    content = f"""# 3266 - Source convention lock or two-channel bound promotion under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- `3266` converts the remaining two-channel WEP issue into an exact residual-inclusive theorem: `eta = A D + epsilon`.
- Since `3265` proved `A` is rank two, the algebra is no longer the blocker; the exact law is `D=A^-1(eta-epsilon)`.
- This gives a clean no-smuggling contract: sign one common parent `D_hatm,D_e` source map and supply residual budgets `epsilon_k`, or do not promote the branch.
- The strongest honest statement is now: cancellation is killed by the second vector **if** the parent source convention is locked.

## Source Register
{md_table(sources, ["source_id", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"])}

## Residual-Inclusive Inversion Theorem
{md_table(theorem, ["theorem_id", "statement", "proof", "determinant", "result", "valid_for_claim"])}

## Matrix Inverse and Residual Gains
{md_table(inverse, ["gain_id", "scenario", "determinant", "inv00_Dhatm_from_MICROSCOPE", "inv01_Dhatm_from_EOTWASH", "inv10_De_from_MICROSCOPE", "inv11_De_from_EOTWASH", "epsilon_MICROSCOPE", "epsilon_EOTWASH", "Dhatm_bound", "De_bound", "valid_for_claim"])}

## Source Convention Lock Clauses
{md_table(clauses, ["clause_id", "required_clause", "mathematical_form", "status", "if_missing", "valid_for_claim"])}

## Promotion Contract
{md_table(contract, ["contract_id", "deliverable", "must_supply", "acceptance_test", "current_status", "valid_for_claim"])}

## Claim Gates
{md_table(gates, ["gate_id", "gate", "passed", "reason", "claim_allowed"])}

## Decision
{md_table(decisions, ["decision_id", "verdict", "what_moved", "best_next", "fallback_next", "valid_for_claim"])}

## Next Target
{md_table(next_targets, ["next_id", "selected", "target_doc", "target_script", "objective", "guardrail", "valid_for_claim"])}

## Validation
{md_table(validations, ["check_id", "check", "passed", "detail"])}

Generated UTC: {RUN_UTC}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    write_csv(OUTPUTS["sources"], source_register())
    write_csv(OUTPUTS["theorem"], theorem_rows())
    write_csv(OUTPUTS["inverse"], inverse_rows())
    write_csv(OUTPUTS["clauses"], clause_rows())
    write_csv(OUTPUTS["contract"], contract_rows())
    write_csv(OUTPUTS["gates"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_rows())
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
