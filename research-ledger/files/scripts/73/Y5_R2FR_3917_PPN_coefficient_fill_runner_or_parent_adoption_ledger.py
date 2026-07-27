from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3917"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3917-Y5-R2FR-PPN-coefficient-fill-runner-or-parent-adoption-ledger.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3917_SOURCE_REGISTER.csv",
    "adoption": SRC / "P8_Y5_R2FR_3917_PARENT_ADOPTION_LEDGER.csv",
    "gamma": SRC / "P8_Y5_R2FR_3917_DELTA_GAMMA_R11_FILL_ROWS.csv",
    "beta": SRC / "P8_Y5_R2FR_3917_DELTA_BETA_SOURCE_FILL_ROWS.csv",
    "score": SRC / "P8_Y5_R2FR_3917_FIRST_PPN_SCORE_RUNNER_ROWS.csv",
    "decision": SRC / "P8_Y5_R2FR_3917_BRANCH_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3917_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3917_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3917_VALIDATION.csv",
}

GAMMA_EXACT = "delta_gamma_R11 = (Psi_R11-Phi_R11)/(U+Phi_R11)"
GAMMA_LINEAR = "delta_gamma_R11 ~= (Psi_R11-Phi_R11)/U"
GAMMA_SOURCE = "delta_gamma_R11 ~= -(kappa_R/(C_TF*U)) nabla^{-2} P_TF[R11_ij]"
GAMMA_PASS = "abs(delta_gamma_R11) <= 2.3e-05 or theorem-zero via P_TF[R11_ij]=0"
BETA_SOURCE = "delta_beta_source = B_source/A_source^2 - 1"
BETA_PASS = "abs(B_source/A_source^2 - 1) <= 7.8e-05 or theorem-zero via A_source=1 and B_source=1 in the branch"
ADOPTION_VERDICT = "no stronger parent-adoption evidence found beyond conditional EH/DZ routes; proceed with nonclaim coefficient fills"
NEXT_TARGET = "3918-Y5-R2FR-delta-gamma-R11-theorem-zero-or-symbolic-bound-tightening.md"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3917_00_next", SRC / "P8_Y5_R2FR_3916_NEXT_TARGET.csv", "NEXT3916_0", "3916 selected PPN fill/adoption target"),
        ("SRC3917_01_EH", SRC / "P8_Y5_R2FR_3916_R11_SELECTOR_FORK.csv", "FORK3916_0_EH", "EH selector route"),
        ("SRC3917_02_DZ", SRC / "P8_Y5_R2FR_3916_R11_SELECTOR_FORK.csv", "FORK3916_1_DZ", "double-zero route"),
        ("SRC3917_03_fallback", SRC / "P8_Y5_R2FR_3916_R11_SELECTOR_FORK.csv", "FORK3916_3_fallback", "coefficient fallback route"),
        ("SRC3917_04_fill_gamma", SRC / "P8_Y5_R2FR_3916_COEFFICIENT_FILL_QUEUE.csv", "FILL3916_0_delta_gamma_R11", "3916 first gamma fill"),
        ("SRC3917_05_fill_betaR11", SRC / "P8_Y5_R2FR_3916_COEFFICIENT_FILL_QUEUE.csv", "FILL3916_1_delta_beta_R11", "3916 beta R11 fill"),
        ("SRC3917_06_fill_beta_source", SRC / "P8_Y5_R2FR_3916_COEFFICIENT_FILL_QUEUE.csv", "FILL3916_2_delta_beta_source", "3916 beta source fill"),
        ("SRC3917_07_promo", SRC / "P8_Y5_R2FR_3916_LOCAL_GR_PROMOTION_UPDATE.csv", "PROM3916_3_local_GR", "3916 no local-GR promotion"),
        ("SRC3917_08_3915_gamma", SRC / "P8_Y5_R2FR_3915_EXECUTABLE_PPN_RESIDUAL_VECTOR.csv", "PPNR3915_0_gamma", "3915 gamma residual"),
        ("SRC3917_09_3915_beta", SRC / "P8_Y5_R2FR_3915_EXECUTABLE_PPN_RESIDUAL_VECTOR.csv", "PPNR3915_1_beta", "3915 beta residual"),
        ("SRC3917_10_3886_gamma", SRC / "P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv", "COEF3886_00_delta_gamma_R11", "3886 gamma coefficient skeleton"),
        ("SRC3917_11_3886_Asource", SRC / "P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv", "COEF3886_01_A_source", "3886 A_source coefficient"),
        ("SRC3917_12_3886_Bsource", SRC / "P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv", "COEF3886_02_B_source", "3886 B_source coefficient"),
        ("SRC3917_13_3886_beta_source", SRC / "P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv", "COEF3886_03_delta_beta_source", "3886 beta source formula"),
        ("SRC3917_14_3887_gamma", SRC / "P8_Y5_R2FR_3887_R11_PPN_COEFFICIENT_FILL_PIVOT.csv", "FILL3887_1_gamma_R11", "3887 gamma fill pivot"),
        ("SRC3917_15_3887_beta", SRC / "P8_Y5_R2FR_3887_R11_PPN_COEFFICIENT_FILL_PIVOT.csv", "FILL3887_2_beta_source", "3887 beta fill pivot"),
        ("SRC3917_16_1943_exact", SRC / "P8_Y5_PARENT_QLOC_1943_DELTA_GAMMA_R11_DERIVATION.csv", "DG1943_2_delta_gamma_exact", "exact delta gamma expression"),
        ("SRC3917_17_1943_linear", SRC / "P8_Y5_PARENT_QLOC_1943_DELTA_GAMMA_R11_DERIVATION.csv", "DG1943_3_linear_limit", "linear delta gamma expression"),
        ("SRC3917_18_1943_bound", SRC / "P8_Y5_PARENT_QLOC_1943_DELTA_GAMMA_R11_DERIVATION.csv", "DG1943_4_cassini_target", "Cassini gamma target"),
        ("SRC3917_19_1944_slip", SRC / "P8_Y5_PARENT_QLOC_1944_R11_WEAK_FIELD_POTENTIAL_DERIVATION.csv", "WFE1944_3_traceless_spatial_projection", "R11 traceless spatial equation"),
        ("SRC3917_20_1944_solution", SRC / "P8_Y5_PARENT_QLOC_1944_R11_WEAK_FIELD_POTENTIAL_DERIVATION.csv", "WFE1944_4_potential_solution_form", "R11 slip solution"),
        ("SRC3917_21_1944_gamma_law", SRC / "P8_Y5_PARENT_QLOC_1944_R11_WEAK_FIELD_POTENTIAL_DERIVATION.csv", "WFE1944_5_delta_gamma_source_law", "delta gamma source law"),
        ("SRC3917_22_1944_zero", SRC / "P8_Y5_PARENT_QLOC_1944_R11_WEAK_FIELD_POTENTIAL_DERIVATION.csv", "WFE1944_7_local_zero_route", "P_TF zero route"),
        ("SRC3917_23_1944_coeffs", SRC / "P8_Y5_PARENT_QLOC_1944_R11_PROJECTION_COEFFICIENT_LEDGER.csv", "COEF1944_2_PTF", "P_TF coefficient ledger"),
        ("SRC3917_24_validation", SRC / "P8_Y5_BRR545_3916_VALIDATION.csv", "VAL3916_13_no_pycache", "3916 validation handoff"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, purpose in source_specs():
        exists = path.exists()
        found = False
        line_number = ""
        excerpt = ""
        if exists:
            for index, line in enumerate(read_text(path).splitlines(), start=1):
                if needle in line:
                    found = True
                    line_number = str(index)
                    excerpt = line[:500]
                    break
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "needle": needle,
                "purpose": purpose,
                "exists": exists,
                "needle_found": found,
                "line_number": line_number,
                "line_excerpt": excerpt,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def adoption_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("ADOPT3917_0_EH", "EH selector", "CONDITIONAL_ONLY", "3906/3916 route exists but parent global adoption is not newly proved"),
        ("ADOPT3917_1_DZ", "double-zero selector", "CONTRACT_READY_NOT_DERIVED", "Y_loc ownership, Sigma_loc positivity and all-family factorization remain unsigned"),
        ("ADOPT3917_2_parent", "parent adoption decision", "NO_STRONGER_EVIDENCE_FOUND_THIS_PASS", ADOPTION_VERDICT),
        ("ADOPT3917_3_action", "route selection", "PROCEED_TO_COEFFICIENT_FILL", "start with delta_gamma_R11 and delta_beta_source nonclaim rows"),
    ]
    return [
        {
            "row_id": row_id,
            "route_or_gate": route,
            "current_result": result,
            "reason": reason,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, route, result, reason in rows
    ]


def gamma_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("GAM3917_0_exact", "exact residual", GAMMA_EXACT, "requires Phi_R11/Psi_R11 potentials and nonzero denominator", "FORMULA_READY_INPUTS_MISSING"),
        ("GAM3917_1_linear", "linear residual", GAMMA_LINEAR, "requires |Phi_R11|,|Psi_R11| << |U|", "CONTROLLED_LINEAR_LIMIT_READY"),
        ("GAM3917_2_source_law", "R11 source projection", GAMMA_SOURCE, "requires kappa_R, C_TF, U, inverse-Laplacian domain and P_TF[R11_ij]", "SYMBOLIC_BOUND_READY_INPUTS_MISSING"),
        ("GAM3917_3_zero_route", "theorem-zero target", "P_TF[R11_ij]=0 => Psi_R11-Phi_R11=0 => delta_gamma_R11=0", "requires parent-derived local STF/traceless R11 silence", "BEST_DERIVATION_TARGET"),
        ("GAM3917_4_pass_rule", "Cassini-style pass rule", GAMMA_PASS, "requires theorem-zero or numeric source-backed projection", "NONCLAIM_PASS_RULE"),
    ]
    return [
        {
            "row_id": row_id,
            "piece": piece,
            "formula": formula,
            "required_inputs": inputs,
            "status": status,
            "numeric_value": "",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, formula, inputs, status in rows
    ]


def beta_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("BET3917_0_definition", "source beta law", BETA_SOURCE, "requires A_source and B_source from second-order source response", "FORMULA_READY_INPUTS_MISSING"),
        ("BET3917_1_branch_zero", "3914 branch zero", "A_source=1 and B_source=1 inside B_loc => delta_beta_source=0", "requires 3914 source-coupling stack plus EH nonlinear completion", "CONDITIONAL_ZERO_IN_BRANCH"),
        ("BET3917_2_fallback", "fill row", BETA_PASS, "requires numeric/source-backed A_source and B_source if source residual-lock fails", "NONCLAIM_PASS_RULE"),
        ("BET3917_3_R11_split", "R11 beta split", "beta_minus_1 = delta_beta_source + delta_beta_R11 + delta_beta_q_loc + delta_beta_boundary_domain + delta_beta_readout", "requires each component theorem-zero or bounded", "NO_CANCELLATION_ENVELOPE"),
    ]
    return [
        {
            "row_id": row_id,
            "piece": piece,
            "formula": formula,
            "required_inputs": inputs,
            "status": status,
            "numeric_value": "",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, formula, inputs, status in rows
    ]


def score_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("RUN3917_0_gamma_zero", "delta_gamma_R11", "if P_TF[R11_ij]=0 parent-signed then predicted=0", "THEOREM_ZERO_BRANCH_AVAILABLE_NOT_SIGNED", False),
        ("RUN3917_1_gamma_bound", "delta_gamma_R11", GAMMA_SOURCE, "SYMBOLIC_RUNNER_READY_NUMERIC_INPUTS_MISSING", False),
        ("RUN3917_2_beta_zero", "delta_beta_source", "if A_source=B_source=1 in B_loc then predicted=0", "CONDITIONAL_ZERO_BRANCH_AVAILABLE_NOT_PROMOTED", False),
        ("RUN3917_3_beta_bound", "delta_beta_source", BETA_SOURCE, "SYMBOLIC_RUNNER_READY_NUMERIC_INPUTS_MISSING", False),
        ("RUN3917_4_total", "PPN first-fill status", "gamma_R11 first; beta_source second; local-GR claim false", "FIRST_FILL_QUEUE_SELECTED", False),
    ]
    return [
        {
            "row_id": row_id,
            "quantity": quantity,
            "runner_formula": formula,
            "status": status,
            "score_ready": score_ready,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, quantity, formula, status, score_ready in rows
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3917_0_route",
            "decision": "no stronger parent-adoption evidence found; coefficient-fill route is activated",
            "claim_status": "NONCLAIM_COEFFICIENT_FILL",
            "reason": "EH/DZ routes remain conditional; gamma_R11 has the cleanest symbolic source law",
            "next_action": "try to theorem-zero P_TF[R11_ij] before numeric fill",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3917_1_gamma",
            "decision": "delta_gamma_R11 is the first serious PPN coefficient target",
            "claim_status": "FORMULA_READY_INPUTS_MISSING",
            "reason": "Cassini/PPN gamma directly probes the R11 traceless spatial slip",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3917_2_beta",
            "decision": "delta_beta_source is queued second but conditionally zero in B_loc",
            "claim_status": "CONDITIONAL_ZERO_OR_FILL",
            "reason": "3914 closes source coupling, but second-order source response must not be smuggled",
            "next_action": "fill A_source/B_source only if branch-zero route fails",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3917_0",
            "next_doc": NEXT_TARGET,
            "next_script": "scripts/Y5_R2FR_3918_delta_gamma_R11_theorem_zero_or_symbolic_bound_tightening.py",
            "target": "attack P_TF[R11_ij]=0 from EH/DZ/local isotropy first; if it fails, tighten the symbolic bound for delta_gamma_R11 with explicit kappa_R, C_TF, U and inverse-Laplacian input rows",
            "why_this_next": "delta_gamma_R11 is the cleanest first empirical PPN bottleneck and has a derived source-law formula",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "result": "parent-adoption ledger completed; first PPN coefficient fill rows created for delta_gamma_R11 and delta_beta_source",
            "local_gr_claim": False,
            "ppn_claim": False,
            "new_forward_progress": "R11/PPN is now executable at the coefficient level, with gamma_R11 as first theorem-zero/bound target",
            "primary_blocker": "P_TF[R11_ij] zero proof or numeric symbolic-bound inputs",
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(sources: list[dict[str, Any]], timestamp: str) -> None:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3917 — PPN Coefficient Fill Runner or Parent Adoption Ledger

Timestamp: `{timestamp}`

## Result

Parent adoption was checked first. No stronger evidence was found beyond the conditional EH/DZ routes, so this checkpoint activates the coefficient-fill path.

Adoption verdict:
`{ADOPTION_VERDICT}`

Gamma exact:
`{GAMMA_EXACT}`

Gamma linear/source law:
`{GAMMA_SOURCE}`

Gamma pass:
`{GAMMA_PASS}`

Beta source:
`{BETA_SOURCE}`

Beta pass:
`{BETA_PASS}`

## Meaning

- `delta_gamma_R11` is now the first hard PPN coefficient target.
- The best derivation route is `P_TF[R11_ij]=0`, which kills the R11 slip and gives `gamma-1=0`.
- If that proof fails, the symbolic source law is ready for coefficient/bound inputs.
- `delta_beta_source` remains conditionally zero in `B_loc`, but has a fallback formula if the source branch fails.

## Source Register

- Source rows found: `{found}/{len(sources)}`
- Register: `{rel(OUTPUTS['sources'])}`
- Validation: `{rel(OUTPUTS['validation'])}`

## Generated Tables

- `{rel(OUTPUTS['adoption'])}`
- `{rel(OUTPUTS['gamma'])}`
- `{rel(OUTPUTS['beta'])}`
- `{rel(OUTPUTS['score'])}`
- `{rel(OUTPUTS['decision'])}`
- `{rel(OUTPUTS['next'])}`

## Next Target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    block = f"""

<!-- BEGIN 3917 PPN COEFFICIENT FILL LEDGER -->
## 3917 PPN Coefficient Fill Ledger

Timestamp: `{timestamp}`

Adoption verdict:
`{ADOPTION_VERDICT}`

Gamma exact:
`{GAMMA_EXACT}`

Gamma source law:
`{GAMMA_SOURCE}`

Gamma pass:
`{GAMMA_PASS}`

Beta source:
`{BETA_SOURCE}`

Decision: activate coefficient-fill path; first target is theorem-zero or symbolic bound for `delta_gamma_R11`, with `delta_beta_source` queued second.
<!-- END 3917 PPN COEFFICIENT FILL LEDGER -->
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    start = "<!-- BEGIN 3917 PPN COEFFICIENT FILL LEDGER -->"
    end = "<!-- END 3917 PPN COEFFICIENT FILL LEDGER -->"
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        SPINE_PATH.write_text(before + block + "\n" + after, encoding="utf-8")
    else:
        SPINE_PATH.write_text(existing.rstrip() + block + "\n", encoding="utf-8")


def validation_rows(
    sources: list[dict[str, Any]],
    adoption: list[dict[str, Any]],
    gamma: list[dict[str, Any]],
    beta: list[dict[str, Any]],
    score: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL3917_0_sources", "all cited source paths and needles resolve", all(row["exists"] and row["needle_found"] for row in sources), f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} source rows found"))
    checks.append(("VAL3917_1_adoption", "parent adoption ledger selects fill route", any(row["current_result"] == "PROCEED_TO_COEFFICIENT_FILL" for row in adoption), rel(OUTPUTS["adoption"])))
    checks.append(("VAL3917_2_gamma_exact", "gamma exact expression emitted", any(GAMMA_EXACT in row["formula"] for row in gamma), rel(OUTPUTS["gamma"])))
    checks.append(("VAL3917_3_gamma_source", "gamma R11 source law emitted", any(GAMMA_SOURCE in row["formula"] for row in gamma + score), rel(OUTPUTS["gamma"])))
    checks.append(("VAL3917_4_gamma_zero", "P_TF zero route emitted", any("P_TF[R11_ij]=0" in row["formula"] for row in gamma), rel(OUTPUTS["gamma"])))
    checks.append(("VAL3917_5_beta", "beta source formula emitted", any(BETA_SOURCE in row["formula"] for row in beta + score), rel(OUTPUTS["beta"])))
    checks.append(("VAL3917_6_score_nonclaim", "score runner rows exist but are not score-ready", len(score) >= 5 and all(str(row.get("score_ready")) == "False" for row in score), rel(OUTPUTS["score"])))
    checks.append(("VAL3917_7_no_claim", "all generated rows remain nonclaim", all(str(row.get("valid_for_claim")) == "False" for row in adoption + gamma + beta + score + decision), "valid_for_claim false across generated rows"))
    checks.append(("VAL3917_8_next", "next target attacks delta_gamma_R11 zero/bound", "3918-Y5-R2FR-delta-gamma-R11" in read_text(OUTPUTS["next"]), rel(OUTPUTS["next"])))
    checks.append(("VAL3917_9_doc", "3917 markdown checkpoint written", DOC_PATH.exists() and "PPN Coefficient Fill Runner" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3917_10_spine", "spine updated with 3917 block", SPINE_PATH.exists() and "BEGIN 3917 PPN COEFFICIENT FILL LEDGER" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details: list[str] = []
    for path in csv_outputs:
        try:
            rows = read_csv_rows(path)
            parse_details.append(f"{path.name}:{len(rows)}")
            csv_parse_ok = csv_parse_ok and bool(rows)
        except Exception as exc:  # pragma: no cover
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{type(exc).__name__}:{exc}")
    checks.append(("VAL3917_11_csv_parse", "all generated CSV outputs parse cleanly", csv_parse_ok, "; ".join(parse_details)))
    fwb_hits = list(FWB.rglob("*3917*")) if FWB.exists() else []
    checks.append(("VAL3917_12_no_formalization_workbench_edits", "no 3917 files generated in formalization-workbench", not fwb_hits, "; ".join(str(path) for path in fwb_hits[:10]) or "no formalization-workbench hits"))
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    checks.append(("VAL3917_13_no_pycache", "scripts __pycache__ removed", not pycache_hits, "; ".join(str(path) for path in pycache_hits[:10]) or "no __pycache__"))
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    adoption = adoption_rows(timestamp)
    gamma = gamma_rows(timestamp)
    beta = beta_rows(timestamp)
    score = score_rows(timestamp)
    decision = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["adoption"], adoption)
    write_csv(OUTPUTS["gamma"], gamma)
    write_csv(OUTPUTS["beta"], beta)
    write_csv(OUTPUTS["score"], score)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, adoption, gamma, beta, score, decision, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
