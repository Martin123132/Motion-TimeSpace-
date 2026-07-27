from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3924"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3924-Y5-R2FR-parent-signature-adoption-minimal-action-clause-or-first-numeric-bound-pack.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3924_SOURCE_REGISTER.csv",
    "clause": SRC / "P8_Y5_R2FR_3924_MINIMAL_PARENT_ACTION_SIGNATURE_CLAUSE.csv",
    "coverage": SRC / "P8_Y5_R2FR_3924_SIGNATURE_TO_THEOREM_COVERAGE.csv",
    "bound": SRC / "P8_Y5_R2FR_3924_FIRST_NUMERIC_BOUND_PACK_IF_NOT_ADOPTED.csv",
    "decision": SRC / "P8_Y5_R2FR_3924_ADOPTION_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3924_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3924_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3924_VALIDATION.csv",
}

MINIMAL_ACTION = (
    "S_parent^loc = S_EH[Q;G_*,Lambda_*] + S_vis[Psi,A,E(Q),theta(Q),c_vis(Q)] "
    "+ S_Y[Q,Y_loc] + S_H[Q,H_priv] + S_int^{>=2}[Q,Y_loc,H_priv] "
    "+ S_R11^{DZ}[Q,Y_loc,Psi] + S_G0[Q,A_3,C_G] + S_B^{top}[Q] + S_proj^{top/readout}"
)
LOCAL_BRANCH = (
    "Y_loc=0, H_priv=0, source-silent q_src collar, fixed q-basic domain, no incoming history tail, "
    "and all visible matter/EM/clocks/orbits read E(Q)"
)
CLAUSE_EFFECT = (
    "If adopted as the local parent branch, the clause signs the 3923 theorem stack; if not adopted, "
    "the 3923 bound pack remains active."
)
BOUND_PACK = (
    "first_bound_pack := {delta_gamma_R11, delta_beta_source, delta_beta_common, P00/Xi_N, "
    "B_escape, Gdot/G, alpha_i/xi, zeta_i}"
)
NEXT_DOC = "3925-Y5-R2FR-minimal-parent-clause-variation-audit-or-Blocal-bound-values.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3925_minimal_parent_clause_variation_audit_or_Blocal_bound_values.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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
        ("SRC3924_00_next", SRC / "P8_Y5_R2FR_3923_NEXT_TARGET.csv", "NEXT3923_0", "3923 selected parent adoption vs bound pack"),
        ("SRC3924_01_theorem", SRC / "P8_Y5_R2FR_3923_LOCAL_GR_CONDITIONAL_THEOREM_STACK.csv", "THM3923_10_total", "3923 local-GR theorem statement"),
        ("SRC3924_02_signatures", SRC / "P8_Y5_R2FR_3923_PARENT_SIGNATURE_CLAUSES.csv", "SIG3923_0_parent_normal_form", "3923 parent normal-form signature"),
        ("SRC3924_03_bounds", SRC / "P8_Y5_R2FR_3923_REMAINING_BOUND_PACK.csv", "BND3923_8_total", "3923 remaining bound pack"),
        ("SRC3924_04_normal_action", SRC / "P8_Y5_R2FR_3905_PARENT_ACTION_NORMAL_FORM.csv", "NF3905_0_action", "3905 parent normal-form action"),
        ("SRC3924_05_Y_quad", SRC / "P8_Y5_R2FR_3905_PARENT_ACTION_NORMAL_FORM.csv", "NF3905_1_memory_quadratic", "quadratic Y sector"),
        ("SRC3924_06_no_shadow", SRC / "P8_Y5_R2FR_3905_PARENT_ACTION_NORMAL_FORM.csv", "NF3905_2_interactions", "no linear visible shadow"),
        ("SRC3924_07_boundary", SRC / "P8_Y5_R2FR_3905_PARENT_ACTION_NORMAL_FORM.csv", "NF3905_3_boundary", "boundary inheritance clause"),
        ("SRC3924_08_constants", SRC / "P8_Y5_R2FR_3905_PARENT_ACTION_NORMAL_FORM.csv", "NF3905_4_constants", "visible constants owner"),
        ("SRC3924_09_EH", SRC / "P8_Y5_R2FR_3906_EH_OPERATOR_SELECTION_CONTRACT.csv", "EH3906_1_action", "EH action normal form"),
        ("SRC3924_10_Hilbert", SRC / "P8_Y5_R2FR_3906_HILBERT_SOURCE_COUPLING_BRIDGE.csv", "SRCBR3906_0_Hilbert", "same-frame Hilbert bridge"),
        ("SRC3924_11_Maxwell", SRC / "P8_Y5_R2FR_3906_HILBERT_SOURCE_COUPLING_BRIDGE.csv", "SRCBR3906_1_Maxwell", "Maxwell Hilbert stress bridge"),
        ("SRC3924_12_G0", SRC / "P8_Y5_R2FR_3909_GSTAR_ZEROFORM_ACTION_BLOCK.csv", "ZF3909_0_action", "Gstar zeroform action block"),
        ("SRC3924_13_R11_sigma", SRC / "P8_Y5_R2FR_3893_R11_SIGMA_FACTORIZATION_INSERTION.csv", "R11S3893_00_candidate_action", "R11 Sigma factorization"),
        ("SRC3924_14_memory_owner", SRC / "P8_Y5_R2FR_3894_MEMORY_PARENT_OWNER_INSERTION.csv", "OWN3894_0_owner", "memory parent variable"),
        ("SRC3924_15_boundary_cert", SRC / "P8_Y5_R2FR_3892_BOUNDARY_TOPOLOGICAL_NOFLUX_CERTIFICATE.csv", "BC3892_0_certificate", "boundary certificate"),
        ("SRC3924_16_projector_cert", SRC / "P8_Y5_R2FR_3892_PROJECTOR_ABSOLUTE_TOPOLOGICAL_CERTIFICATE.csv", "PC3892_0_certificate", "projector certificate"),
        ("SRC3924_17_domain_zero", SRC / "P8_Y5_R2FR_3431_PROJECTOR_VARIATION_NO_STRESS_THEOREM.csv", "DP3431_2_fixed_topological_zero", "fixed topological domain/projector zero"),
        ("SRC3924_18_history", SRC / "P8_Y5_R2FR_3895_MEMORY_BOUNDARY_HISTORY_ZERO_ATTEMPT.csv", "ZERO3895_5_total", "history/boundary total status"),
        ("SRC3924_19_escape", SRC / "P8_Y5_R2FR_3922_DECISION_GATE.csv", "DEC3922_0_combined", "escape combined theorem"),
        ("SRC3924_20_project_state", SRC / "P8_Y5_R2FR_3923_DECISION_GATE.csv", "DEC3923_2_project_state", "3923 project state decision"),
        ("SRC3924_21_validation", SRC / "P8_Y5_BRR545_3923_VALIDATION.csv", "VAL3923_13_no_pycache", "3923 validation handoff"),
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
                    excerpt = line[:760]
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


def clause_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CLA3924_0_fields", "field chart", "Phi=(Q_pub,Y_loc,H_priv,Psi,A); q_parent(Phi)=Q_pub", "public geometry is Q; local/hidden sectors are not direct readout frames", "LOCAL_PARENT_SIGNATURE_CANDIDATE"),
        ("CLA3924_1_action", "minimal local parent action", MINIMAL_ACTION, "single clause containing EH, visible matter/EM, quadratic hidden sectors, double-zero R11, G owner, boundary/projector certificates", "LOCAL_PARENT_SIGNATURE_CANDIDATE"),
        ("CLA3924_2_branch", "local branch surface", LOCAL_BRANCH, "defines the local GR/Newton/Maxwell recovery collar", "LOCAL_BRANCH_SURFACE"),
        ("CLA3924_3_EH", "EH public sector", "S_EH=(2*kappa_*)^-1 int sqrt(-Q)(R[Q]-2Lambda_*) + topological terms", "signs EH operator selector and low-energy GR equation", "SIGNS_IF_ADOPTED"),
        ("CLA3924_4_visible", "visible Hilbert source", "S_vis includes matter and Maxwell action built from E(Q), theta(Q), c_vis(Q), alpha_*", "signs same-frame matter/EM stress and source/readout lock", "SIGNS_IF_ADOPTED"),
        ("CLA3924_5_G0", "constant coupling owner", "S_G0=(2*kappa_0)^-1 int sqrt(-Q)(R-2Lambda_*) + int C_G dA_3 with fixed topological A_3 class", "signs dG_*=0 for local coupling sector", "SIGNS_IF_ADOPTED"),
        ("CLA3924_6_Y", "quadratic residual fibre", "S_Y is quadratic/coercive in Y_loc and S_int has no visible-linear Y/H terms", "removes affine hidden stress at Y_loc=0 and gives bound route if Y not zero", "SIGNS_IF_ADOPTED_WITH_GAP_OR_BOUNDS"),
        ("CLA3924_7_R11", "double-zero R11 selector", "S_R11^{DZ}=int sqrt(-Q) sum_A F_A(Sigma_loc) O_A[Q,Psi] with F_A(0)=F_A'(0)=0", "kills non-topological R11 first variations on Y_loc=0", "SIGNS_IF_ADOPTED"),
        ("CLA3924_8_boundary", "boundary certificate", "S_B^{top}[Q] has fixed relative class, scalar/topological no-flux, no vector/shear/normal exchange", "kills boundary multipoles/alpha3/xi leaks except universal monopole calibration", "SIGNS_IF_ADOPTED"),
        ("CLA3924_9_projector_domain", "projector/domain certificate", "S_proj is topological/readout-only or fixed metric/domain-independent with source equality; domain is q-basic and fixed", "kills delta Pi_M, [d,Pi_M], moving support and hidden projector stress", "SIGNS_IF_ADOPTED"),
        ("CLA3924_10_history", "history/no-tail clause", "local branch has no incoming memory/history tail, or else history enters the numeric bound pack", "cannot be forced globally; local branch or bound split is required", "PARTIAL_SIGNATURE_OR_BOUND"),
        ("CLA3924_11_effect", "adoption effect", CLAUSE_EFFECT, "candidate is strong enough for private local theorem stack but not a public global corpus adoption", "READY_FOR_VARIATION_AUDIT"),
    ]
    return [
        {
            "row_id": row_id,
            "clause": clause,
            "formula_or_statement": formula,
            "effect": effect,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, clause, formula, effect, status in data
    ]


def coverage_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("COV3924_0_parent_normal_form", "SIG3923_0_parent_normal_form", "CLA3924_0_fields;CLA3924_1_action", "covered by product chart and local action split", "COVERED_IF_CLAUSE_ADOPTED"),
        ("COV3924_1_EH_selector", "SIG3923_1_EH_selector", "CLA3924_3_EH", "covered by EH-only public sector plus no extra public operator slot", "COVERED_IF_CLAUSE_ADOPTED"),
        ("COV3924_2_same_frame", "SIG3923_2_same_frame", "CLA3924_4_visible", "covered by E(Q) visible matter/EM/clock/orbit readout", "COVERED_IF_CLAUSE_ADOPTED"),
        ("COV3924_3_Gstar", "SIG3923_3_Gstar", "CLA3924_5_G0", "covered by zeroform/topological coupling owner", "COVERED_IF_CLAUSE_ADOPTED"),
        ("COV3924_4_Meff", "SIG3923_4_Meff", "CLA3924_4_visible;CLA3924_9_projector_domain", "covered if q_src/Hilbert equality and fixed projector/domain are adopted", "COVERED_IF_SOURCE_COLLAR_ADOPTED"),
        ("COV3924_5_R11", "SIG3923_5_R11", "CLA3924_7_R11", "covered by double-zero R11 selector plus topological escape clauses", "COVERED_IF_CLAUSE_ADOPTED"),
        ("COV3924_6_beta_square", "SIG3923_6_beta_square", "CLA3924_3_EH;CLA3924_4_visible", "covered by one-metric EH nonlinear completion after source normalization", "COVERED_IF_CLAUSE_ADOPTED"),
        ("COV3924_7_P00", "SIG3923_7_P00", "CLA3924_7_R11;CLA3924_8_boundary;CLA3924_9_projector_domain", "covered if P00 R11 and escape sources vanish or reduce to universal monopole", "COVERED_IF_ESCAPE_CLAUSES_ADOPTED"),
        ("COV3924_8_boundary", "SIG3923_8_boundary", "CLA3924_8_boundary", "covered by explicit boundary certificate", "COVERED_IF_CLAUSE_ADOPTED"),
        ("COV3924_9_projector", "SIG3923_9_projector", "CLA3924_9_projector_domain", "covered by fixed topological/readout projector with source equality", "COVERED_IF_CLAUSE_ADOPTED"),
        ("COV3924_10_domain", "SIG3923_10_domain", "CLA3924_9_projector_domain", "covered by q-basic fixed domain and no moving support", "COVERED_IF_CLAUSE_ADOPTED"),
        ("COV3924_11_history", "SIG3923_11_history", "CLA3924_10_history", "only local no-incoming-tail branch is covered; otherwise bound pack remains", "PARTIAL_COVERAGE_OR_BOUND"),
    ]
    return [
        {
            "row_id": row_id,
            "signature_row": sig,
            "covering_clause": clause,
            "coverage_statement": statement,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, sig, clause, statement, status in data
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("NUM3924_0_gamma", "delta_gamma_R11", "needs kappa_R,C_TF,U_min,||nabla^-2 P_TF||", "first if R11 STF zero not adopted"),
        ("NUM3924_1_beta_source", "delta_beta_source", "needs A_source,B_source", "first if EH/source square law not adopted"),
        ("NUM3924_2_beta_common", "delta_beta_common", "needs xi_1,xi_2,Delta_sq", "first if common-mode square law not adopted"),
        ("NUM3924_3_Xi", "Xi_N/P00", "needs P00_norm,C0,kappa_R,Green0,xi0,multipoles", "first if P00 harmonic monopole route not adopted"),
        ("NUM3924_4_escape", "B_escape", "needs P00_boundary/projector/domain/history/nonlocal,B_harmonic_boundary,B_deriv", "first if escape certificates not adopted"),
        ("NUM3924_5_Gdot", "Gdot/G", "needs partial_t xi_1 and remaining Gdot components", "first if time derivative silence not adopted"),
        ("NUM3924_6_alpha_xi", "alpha_i/xi", "needs domain/projector/vector/multipole weights and epsilon_domain_projector_abs", "first if no-vector/no-multipole clauses not adopted"),
        ("NUM3924_7_zeta", "zeta_i", "needs non-Hilbert/projector stress leakage vector", "first if Hilbert/Bianchi closure not adopted"),
        ("NUM3924_8_total", "B_local", BOUND_PACK, "absolute-sum no-cancellation scoring pack"),
    ]
    return [
        {
            "row_id": row_id,
            "residual": residual,
            "required_inputs": inputs,
            "use_when": use_when,
            "numeric_value": "",
            "status": "SOURCE_BACKED_NUMERIC_FILL_IF_PARENT_CLAUSE_NOT_ADOPTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, residual, inputs, use_when in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3924_0_clause",
            "decision": "minimal local parent-action signature clause constructed",
            "formula": MINIMAL_ACTION,
            "claim_status": "CANDIDATE_PARENT_SIGNATURE_READY_NOT_GLOBAL_CORPUS_ADOPTED",
            "next_action": "run variation audit clause-by-clause before promotion",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3924_1_coverage",
            "decision": "clause covers all 3923 signatures except history remains local-branch-or-bound",
            "formula": LOCAL_BRANCH,
            "claim_status": "PRIVATE_LOCAL_BRANCH_CANDIDATE",
            "next_action": "audit history/no-tail and boundary/projector/domain variations hardest",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3924_2_bound",
            "decision": "if parent clause is rejected or unsigned, first numeric bound pack is ready",
            "formula": BOUND_PACK,
            "claim_status": "NONCLAIM_BOUND_FALLBACK",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3924_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "vary the minimal parent clause through Q,Y,boundary,projector/domain and history terms; if any variation fails, start filling B_local numeric values",
            "why_this_next": "3924 proposes a candidate signing clause, but promotion requires an explicit variation audit rather than assertion",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_NONCLAIM_CHECKPOINT",
            "summary": "minimal parent-action signature clause constructed with coverage map and fallback numeric bound pack",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3924 - Parent Signature Adoption Minimal Action Clause or First Numeric Bound Pack

Timestamp: `{timestamp}`

## Result

Constructed the minimal local parent-action signature clause:

`{MINIMAL_ACTION}`.

Local branch surface:

`{LOCAL_BRANCH}`.

Decision:

`{CLAUSE_EFFECT}`.

Fallback if the clause is rejected or remains unsigned:

`{BOUND_PACK}`.

## Meaning

This is the first serious candidate for signing the whole local-GR theorem stack without hiding the coupling. It is still not a public claim: the clause must survive an explicit variation audit through `Q`, `Y_loc`, boundary, projector/domain and history terms. If any part fails, the named numeric bound pack remains the route.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3924_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3924_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3924_MINIMAL_PARENT_ACTION_SIGNATURE_CLAUSE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3924_SIGNATURE_TO_THEOREM_COVERAGE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3924_FIRST_NUMERIC_BOUND_PACK_IF_NOT_ADOPTED.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3924_ADOPTION_DECISION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3924_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3924 - Minimal Parent Action Signature Clause

Timestamp: `{timestamp}`

- Candidate local parent action: `{MINIMAL_ACTION}`.
- Local branch surface: `{LOCAL_BRANCH}`.
- Effect: `{CLAUSE_EFFECT}`.
- Fallback numeric pack: `{BOUND_PACK}`.
- Status: private candidate signature only; requires variation audit before any promotion.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3924 - Minimal Parent Action Signature Clause"
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    clause = clause_rows(timestamp)
    coverage = coverage_rows(timestamp)
    bounds = bound_rows(timestamp)
    decisions = decision_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    checks = [
        ("VAL3924_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3924_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3924_02_clause_rows", len(clause) == 12, "minimal parent clause rows emitted"),
        ("VAL3924_03_coverage_rows", len(coverage) == 12, "signature coverage rows emitted"),
        ("VAL3924_04_bound_rows", len(bounds) == 9, "first numeric bound pack rows emitted"),
        ("VAL3924_05_candidate_not_claim", any(row["row_id"] == "DEC3924_0_clause" and "NOT_GLOBAL" in row["claim_status"] for row in decisions), "candidate is not promoted as public claim"),
        ("VAL3924_06_history_partial", any(row["row_id"] == "COV3924_11_history" and row["status"] == "PARTIAL_COVERAGE_OR_BOUND" for row in coverage), "history remains partial or bound"),
        ("VAL3924_07_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in (clause, coverage, bounds, decisions) for row in group), "all new rows are nonclaim"),
        ("VAL3924_08_outputs_not_fwb", all(not FWB in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3924_09_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3924_10_spine_written", SPINE_PATH.exists() and "3924 - Minimal Parent Action Signature Clause" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3924_11_next_target", next_rows(timestamp)[0]["next_doc"] == NEXT_DOC, "next target row emitted"),
        ("VAL3924_12_script_compiles", True, "script compiles"),
        ("VAL3924_13_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    return [
        {
            "row_id": row_id,
            "check": detail,
            "result": "PASS" if passed else "FAIL",
            "timestamp_utc": timestamp,
        }
        for row_id, passed, detail in checks
    ]


def main() -> None:
    timestamp = now_utc()
    source_rows = source_register_rows(timestamp)
    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["clause"], clause_rows(timestamp))
    write_csv(OUTPUTS["coverage"], coverage_rows(timestamp))
    write_csv(OUTPUTS["bound"], bound_rows(timestamp))
    write_csv(OUTPUTS["decision"], decision_rows(timestamp))
    write_csv(OUTPUTS["next"], next_rows(timestamp))
    write_csv(OUTPUTS["status"], status_rows(timestamp, source_rows))
    DOC_PATH.write_text(doc_text(timestamp, source_rows), encoding="utf-8")
    update_spine(timestamp)
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    validation = validation_rows(timestamp, source_rows)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3924 validation failed: {failed}")
    print(f"3924 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
