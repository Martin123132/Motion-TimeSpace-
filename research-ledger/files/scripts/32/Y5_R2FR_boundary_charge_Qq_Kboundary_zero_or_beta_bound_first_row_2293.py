from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_PARENT_QLOC_BOUNDARY_QQ_KBOUNDARY_OR_BETA_2293"
START_TS = datetime.now(timezone.utc).timestamp()
DOC = ROOT / "2293-Y5-R2FR-boundary-charge-Qq-Kboundary-zero-or-beta-bound-first-row.md"


PATHS = {
    "2292_doc": ROOT / "2292-Y5-R2FR-no-physical-q-pole-theorem-or-bounded-beta-runner.md",
    "2292_validation": OUT / "P8_Y5_BRR545_2292_VALIDATION.csv",
    "2292_next": OUT / "P8_Y5_PARENT_QLOC_2292_NEXT_TARGET.csv",
    "2292_nopole": OUT / "P8_Y5_PARENT_QLOC_2292_NO_PHYSICAL_Q_POLE_AUDIT.csv",
    "2292_omega": OUT / "P8_Y5_PARENT_QLOC_2292_OMEGA_DCQ_CLOSURE_AUDIT.csv",
    "2292_claim_gates": OUT / "P8_Y5_PARENT_QLOC_2292_CLAIM_GATES.csv",
    "2292_beta": OUT / "P8_Y5_PARENT_QLOC_2292_BOUNDED_BETA_SOURCE_TEST_TEMPLATE.csv",
    "2245_doc": ROOT / "2245-Y5-R2FR-RAB-boundary-charge-QR-Kboundary-zero-or-beta-bound-first-row.md",
    "2245_validation": OUT / "P8_Y5_BRR545_2245_VALIDATION.csv",
    "2245_compact": OUT / "P8_Y5_PARENT_QLOC_2245_COMPACT_PROPER_BOUNDARY_SILENCE_LEMMA.csv",
    "2245_gate": OUT / "P8_Y5_PARENT_QLOC_2245_QR_KBOUNDARY_CLAIM_GATE.csv",
    "2245_residual": OUT / "P8_Y5_PARENT_QLOC_2245_BOUNDARY_RESIDUAL_BETA_ROW.csv",
    "2245_projection": OUT / "P8_Y5_PARENT_QLOC_2245_FIRST_BETA_PROJECTION_TEMPLATE.csv",
    "2245_alpha3": OUT / "P8_Y5_PARENT_QLOC_2245_ALPHA3_BOUND_ANCHOR_LEDGER.csv",
    "1039_doc": ROOT / "1039-Y5-R10-boundary-charge-QX-Kboundary-zero-or-beta-bound-first-row.md",
    "1039_validation": OUT / "P8_Y5_BRR545_1039_VALIDATION.csv",
    "1039_compact": OUT / "P8_Y5_R10_1039_COMPACT_PROPER_BOUNDARY_SILENCE_LEMMA.csv",
    "1039_gate": OUT / "P8_Y5_R10_1039_QX_KBOUNDARY_CLAIM_GATE.csv",
    "1039_residual": OUT / "P8_Y5_R10_1039_BOUNDARY_RESIDUAL_BETA_ROW.csv",
    "1039_projection": OUT / "P8_Y5_R10_1039_FIRST_BETA_PROJECTION_TEMPLATE.csv",
    "1039_alpha3": OUT / "P8_Y5_R10_1039_ALPHA3_BOUND_ANCHOR_LEDGER.csv",
    "local_bounds": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv",
}


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2293_00_2292_doc",
        "role": "q_branch_handoff",
        "path": PATHS["2292_doc"],
        "needles": ["Q_q", "K_boundary", "2293-Y5-R2FR"],
        "notes": "2292 isolated the q boundary charge/cocycle obstruction.",
    },
    {
        "source_id": "SRC2293_01_2292_validation",
        "role": "prior_validation",
        "path": PATHS["2292_validation"],
        "needles": ["VAL2292_OVERALL", "PASS"],
        "notes": "2292 validation passed with claims blocked.",
    },
    {
        "source_id": "SRC2293_02_2292_next",
        "role": "explicit_next_target",
        "path": PATHS["2292_next"],
        "needles": ["2293-Y5-R2FR-boundary-charge-Qq-Kboundary-zero-or-beta-bound-first-row.md", "Q_q"],
        "notes": "Direct handoff into boundary charge/cocycle or beta-bound first row.",
    },
    {
        "source_id": "SRC2293_03_2292_nopole",
        "role": "q_no_pole_failure",
        "path": PATHS["2292_nopole"],
        "needles": ["NPQ2292_3_boundary_silence", "MISSING_BOUNDARY_CHARGE_ZERO"],
        "notes": "Boundary silence is the active no-pole obstruction.",
    },
    {
        "source_id": "SRC2293_04_2292_omega",
        "role": "q_omega_dcq_closure",
        "path": PATHS["2292_omega"],
        "needles": ["ODQ2292_4_boundary_differentiability", "ODQ2292_5_bracket_closure"],
        "notes": "Parent Omega/DCq and bracket/cocycle remain unsigned.",
    },
    {
        "source_id": "SRC2293_05_2292_claim_gates",
        "role": "q_claim_policy",
        "path": PATHS["2292_claim_gates"],
        "needles": ["CGATE2292_0_no_pole", "False"],
        "notes": "No q no-pole or R10/local-GR pass claim is allowed.",
    },
    {
        "source_id": "SRC2293_06_2292_beta",
        "role": "bounded_beta_fallback",
        "path": PATHS["2292_beta"],
        "needles": ["BB2292_7_beta_product_guard", "CLAIM_BLOCKED"],
        "notes": "If boundary silence does not close, the branch must become a bounded beta_source beta_test row.",
    },
    {
        "source_id": "SRC2293_07_2245_doc",
        "role": "RAB_boundary_precedent",
        "path": PATHS["2245_doc"],
        "needles": ["proper compact", "Q_R", "K_boundary"],
        "notes": "Same R2FR fork derived the narrow compact/proper boundary lemma for R_AB.",
    },
    {
        "source_id": "SRC2293_08_2245_validation",
        "role": "RAB_boundary_validation",
        "path": PATHS["2245_validation"],
        "needles": ["VAL2245_OVERALL", "PASS"],
        "notes": "R_AB boundary checkpoint passed with source-boundary promotion blocked.",
    },
    {
        "source_id": "SRC2293_09_2245_compact",
        "role": "finite_jet_boundary_precedent",
        "path": PATHS["2245_compact"],
        "needles": ["QRK2245_2_QR_zero", "QRK2245_3_Kboundary_zero"],
        "notes": "Finite-jet collar argument to be specialized to q.",
    },
    {
        "source_id": "SRC2293_10_2245_residual",
        "role": "boundary_residual_template",
        "path": PATHS["2245_residual"],
        "needles": ["K_boundary_alpha3", "Qbar_edge_RH"],
        "notes": "R_AB residual beta rows provide the nonclaim fallback pattern.",
    },
    {
        "source_id": "SRC2293_11_1039_doc",
        "role": "generic_X_boundary_precedent",
        "path": PATHS["1039_doc"],
        "needles": ["Q_X", "K_boundary", "alpha3"],
        "notes": "Generic X checkpoint supplies the earlier q-like boundary template.",
    },
    {
        "source_id": "SRC2293_12_1039_validation",
        "role": "generic_X_boundary_validation",
        "path": PATHS["1039_validation"],
        "needles": ["V1039_SUMMARY", "pass"],
        "notes": "1039 validation passed with nonclaim status.",
    },
    {
        "source_id": "SRC2293_13_1039_compact",
        "role": "generic_compact_sublemma",
        "path": PATHS["1039_compact"],
        "needles": ["QK1039_2_QX_zero", "QK1039_3_Kboundary_zero"],
        "notes": "Generic finite-jet collar lemma predecessor.",
    },
    {
        "source_id": "SRC2293_14_1039_alpha3",
        "role": "alpha3_anchor_precedent",
        "path": PATHS["1039_alpha3"],
        "needles": ["Will_2014_PPN_alpha3_table", "4e-20"],
        "notes": "Source-backed preferred-frame anchor; not an MTS claim.",
    },
    {
        "source_id": "SRC2293_15_local_bounds",
        "role": "external_bound_anchor",
        "path": PATHS["local_bounds"],
        "needles": ["Will_2014_PPN_alpha3_table", "alpha3"],
        "notes": "Local bound ledger holding the alpha3 anchor.",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2293_SOURCE_REGISTER.csv",
    "compact_lemma": OUT / "P8_Y5_PARENT_QLOC_2293_COMPACT_PROPER_BOUNDARY_SILENCE_LEMMA.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2293_QQ_KBOUNDARY_CLAIM_GATE.csv",
    "boundary_residuals": OUT / "P8_Y5_PARENT_QLOC_2293_BOUNDARY_RESIDUAL_BETA_ROW.csv",
    "first_projection": OUT / "P8_Y5_PARENT_QLOC_2293_FIRST_BETA_PROJECTION_TEMPLATE.csv",
    "alpha3_anchor": OUT / "P8_Y5_PARENT_QLOC_2293_ALPHA3_BOUND_ANCHOR_LEDGER.csv",
    "mts_template": OUT / "R10_alpha_lambda_curve_MTS_2293_BOUNDARY_QQ_KBOUNDARY_TEMPLATE_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_PARENT_QLOC_2293_RUNNER_SMOKE_STATUS.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2293_PLACEHOLDER_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2293_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2293_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2293_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2293_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2293_VALIDATION.csv",
}

BRANCH_COPY_TARGETS = {
    "queue_boundary": QUEUE / "JR2293_BOUNDARY_QQ_KBOUNDARY_TEMPLATE_NONCLAIM.csv",
    "queue_alpha3": QUEUE / "JR2293_ALPHA3_PROJECTION_TEMPLATE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "boundary_Qq_Kboundary_or_beta_nonclaim_2293.csv",
    "beta_docs": BETA_DOCS / "BOUNDARY_QQ_KBOUNDARY_OR_BETA_2293_NONCLAIM.csv",
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE.mkdir(parents=True, exist_ok=True)
    BETA_DOCS.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8", newline="")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def path_display(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def contains_all(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "role": source["role"],
                "path": str(path),
                "exists": path.exists(),
                "needles_present": contains_all(path, needles),
                "needles": ";".join(needles),
                "notes": source["notes"],
                "valid_for_claim": False,
            }
        )
    return rows


def compact_lemma_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "QQK2293_0_variational_identity",
            "For a differentiable local q-vertical generator G_q[epsilon], the possible obstruction is a finite-jet surface density k_q[delta Y,epsilon] on partial Sigma.",
            "delta G_q[epsilon]=bulk constraint variation + integral_partialSigma k_q[delta Y,epsilon]; Q_q is the boundary functional needed to make G_q differentiable.",
            "STRUCTURAL_IDENTITY_CONDITIONAL_ON_PARENT_GQ",
            "sets the boundary problem but does not prove full q silence",
        ),
        (
            "QQK2293_1_proper_collar_condition",
            "If epsilon_q and every finite jet entering k_q vanish on an open collar of partial Sigma, every local boundary monomial containing epsilon_q or its jets vanishes pointwise.",
            "support(epsilon_q) compactly contained in Sigma implies epsilon_q|partialSigma=nabla^a epsilon_q|partialSigma=0 for the finite derivative order used by the local boundary density.",
            "DERIVED_NARROW_CONDITIONAL_ZERO",
            "proper compact q-representative transformations only",
        ),
        (
            "QQK2293_2_Qq_zero",
            "Under QQK2293_1, Q_q[epsilon]=integral_partialSigma q_q[epsilon]=0 and delta Q_q[epsilon]=0.",
            "q_q and delta q_q are finite-jet local surface expressions in epsilon_q, field data, and their boundary jets; the epsilon_q jet factors vanish on the boundary collar.",
            "DERIVED_NARROW_PROPER_BRANCH_ONLY",
            "kills representative edge charge for compact local gauge variations, not source/worldtube or large transformations",
        ),
        (
            "QQK2293_3_Kboundary_zero",
            "Under QQK2293_1 for both epsilon_q and eta_q, K_boundary[epsilon,eta]=0 for any finite-jet local boundary cocycle.",
            "the cocycle is a surface bilinear in the generators and finite jets; every local boundary term contains at least one vanished generator jet.",
            "DERIVED_NARROW_PROPER_BRANCH_ONLY",
            "compact proper q algebra closes with zero boundary cocycle",
        ),
        (
            "QQK2293_4_GR_charge_guard",
            "The proper-q zero does not erase observed ADM/time/rotation, Newtonian mass, or GR Hamiltonian charges.",
            "the vanishing condition applies only to representative q-vertical parameters; physical Hamiltonian generators remain in the observed metric/coframe boundary sector.",
            "GUARD_RETAINED",
            "prevents deleting GR charges to save the q branch",
        ),
        (
            "QQK2293_5_source_boundary_limit",
            "The compact/proper lemma does not prove Q_q=0 for source worldtubes, non-compact transformations, reference-boundary terms, material readouts, or range-kernel weighted edge projections.",
            "R10, PPN, WEP/clock, and orbital source tests can involve nonzero boundary/support data; those terms must remain explicit beta rows or be separately theorem-zeroed.",
            "FULL_LOCAL_CLAIM_STILL_BLOCKED",
            "source/test beta rows remain active",
        ),
        (
            "QQK2293_6_verdict",
            "Q_q=0 and K_boundary=0 are derived only for the proper compact q-representative sub-branch.",
            "QQK2293_1 through QQK2293_4 close the narrow boundary algebra, while QQK2293_5 blocks promotion to local-GR/R10.",
            "DERIVED_NARROW_SUBLEMMA_FULL_CLAIM_BLOCKED",
            "useful derived brick for GR-reduction hygiene, not an empirical pass",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "lemma_id": row[0],
            "statement": row[1],
            "derivation_or_test": row[2],
            "status": row[3],
            "limitation": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row in rows
    ]


def qq_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "QQG2293_0_proper_compact_sublemma",
            "proper compact q-representative transformations carry no boundary charge or cocycle",
            "conditional_narrow_pass",
            "epsilon_q and required finite jets vanish on a boundary collar, forcing Q_q and K_boundary surface densities to vanish",
            "does not cover source worldtubes, non-proper transformations, reference terms, matter/readout markers, or range-kernel edge rows",
        ),
        (
            "QQG2293_1_full_Qq_zero",
            "Q_q=0 for all local source/test boundaries",
            "fail_current_claim",
            "2292 still lacks parent Omega/DCq, exact primitive/counterterm, reference subtraction, and source-boundary projector orthogonality",
            "derive B_q/Q_q from Theta_Y and allowed boundary class",
        ),
        (
            "QQG2293_2_full_Kboundary_zero",
            "K_boundary=0 for source/test or improper edge transformations",
            "fail_current_claim",
            "compact-collar proof only controls finite-jet terms with vanished generator data",
            "compute bracket/cocycle for differentiable G_q[epsilon] and G_q[eta]",
        ),
        (
            "QQG2293_3_no_pole_promotion",
            "q has no physical local pole in the full GR/Newton branch",
            "fail_current_claim",
            "boundary silence is only one required clause; degree count and matter/no-marker descent still remain",
            "close Omega/DCq, boundary, degree, and matter clauses from one parent action",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": row[0],
            "claim": row[1],
            "gate_status": row[2],
            "evidence": row[3],
            "missing_for_promotion": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row in rows
    ]


def boundary_residual_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BRES2293_0_Qbar_edge_qH",
            "Qbar_edge_qH(lambda)",
            "Qbar_edge_qH(lambda)=integral_partialSigma F_lambda epsilon_q B_q with source/reference projection",
            "non-proper/source boundary values are not killed by the compact representative lemma",
            "B_q owner; F_lambda kernel; source boundary class; Pi_M/Pi_EH projection; units",
        ),
        (
            "BRES2293_1_K_boundary_alpha3_q",
            "K_boundary_alpha3_q",
            "alpha3_MTS_q=K_boundary_alpha3_q * Phi_boundary_local_q",
            "the alpha3 preferred-frame anchor is the cleanest first boundary-flux projection for a q edge/cocycle leak",
            "K_boundary_alpha3_q; Phi_boundary_local_q; projection normalization; theorem-zero or numeric source",
        ),
        (
            "BRES2293_2_reference_mass_projection",
            "Pi_M^H[Q_q_edge]",
            "mass/Hamiltonian reference projector must be orthogonal to Q_q_edge or explicitly bounded",
            "a zero q-boundary proof must not delete physical GR mass/energy charges",
            "reference subtraction; Pi_M action on q edge charge; no-double-count split",
        ),
        (
            "BRES2293_3_matter_readout_marker_edge",
            "Q_q^marker",
            "ordinary material/readout constants must have zero q edge marker or a bounded coefficient vector",
            "q can hide in matter/readout even if compact bulk transformations are silent",
            "no-marker theorem; b_A/b_alpha bounds; WEP/clock projection matrix",
        ),
        (
            "BRES2293_4_no_double_count",
            "Q_q_bulk + Q_q_edge split",
            "bulk beta_source beta_test and edge beta_source beta_test must be orthogonal or explicitly summed in absolute value",
            "prevents cancellation games between no-pole and bounded-beta routes",
            "source/test support split; absolute tail envelope; branch ownership ledger",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": row[0],
            "symbol": row[1],
            "formula_or_contract": row[2],
            "why_retained": row[3],
            "missing_inputs": row[4],
            "score_ready": False,
            "valid_for_claim": False,
        }
        for row in rows
    ]


def first_projection_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FBP2293_0_boundary_alpha3_q",
            "K_boundary_alpha3_q * Phi_boundary_local_q",
            "alpha3",
            "alpha3_MTS_q=K_boundary_alpha3_q * Phi_boundary_local_q",
            "local_bound_claims.csv:Will_2014_PPN_alpha3_table",
            "4e-20",
            "K_boundary_alpha3_q;Phi_boundary_local_q;normalization;source_path or theorem-zero",
            "SOURCE_BACKED_ANCHOR_READY_PROJECTION_MISSING",
        ),
        (
            "FBP2293_1_R10_edge_beta_q",
            "Qbar_edge_qH(lambda) * qbar_qT(lambda)",
            "alpha_R10(lambda)",
            "|alpha_q_edge(lambda)| <= |K_q^R10(lambda)| |Qbar_edge_qH(lambda) qbar_qT(lambda)| + abs_tail",
            "R10 bound curve + source/test q boundary projection",
            "MISSING_CURVE_AND_PROJECTION",
            "B_q;Qbar_edge_qH;qbar_qT;K_q^R10(lambda);source/test support",
            "CLAIM_BLOCKED_UNTIL_SOURCE_BACKED_BOUND_ROW",
        ),
        (
            "FBP2293_2_absolute_tail_gate",
            "boundary_q_abs_tail",
            "all local arenas",
            "unknown Q_q/K_boundary/source-support/marker components add in absolute value; no cancellation credit",
            "R10;alpha3;PPN;WEP;clock;orbital ledgers",
            "multiple",
            "component theorem-zero or numeric/source-backed bound rows",
            "CLAIM_BLOCKED_UNTIL_COMPONENTS_SOURCE_BACKED",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "projection_id": row[0],
            "residual_symbol": row[1],
            "observable": row[2],
            "projection_formula": row[3],
            "external_anchor": row[4],
            "anchor_bound": row[5],
            "missing_mts_inputs": row[6],
            "current_status": row[7],
            "score_ready": False,
            "valid_for_claim": False,
        }
        for row in rows
    ]


def alpha3_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "anchor_id": "A3A2293_0_source_bound",
            "dataset_id": "Will_2014_PPN_alpha3_table",
            "observable": "alpha3",
            "upper_bound": "4e-20",
            "units": "dimensionless",
            "reference": "source-intake/local_bounds/local_bound_claims.csv; prior 1039/2245 alpha3 anchor ledgers",
            "use_in_2293": "anchor only for q boundary alpha3 projection row; not an MTS pass",
            "valid_for_claim": False,
        }
    ]


def mts_template_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "proper_compact_Qq_Kboundary_zero_sublemma",
            "ALL_LOCAL_R10_RANGE",
            "MISSING_EXTENSION_TO_SOURCE_TEST_BOUNDARIES",
            "Q_q=K_boundary=0 only for compact proper q-representative transformations",
            "template_invalid_narrow_sublemma_not_full_R10_branch",
        ),
        (
            "boundary_alpha3_q_projection_template",
            "MISSING_NOT_R10_RANGE",
            "MISSING_K_BOUNDARY_ALPHA3_Q_TIMES_PHI_BOUNDARY_LOCAL_Q",
            "alpha3_MTS_q=K_boundary_alpha3_q * Phi_boundary_local_q",
            "template_invalid_projection_coefficients_missing",
        ),
        (
            "R10_edge_beta_q_template",
            "MISSING_PARENT_LAMBDA_Q",
            "MISSING_KQ_QBAR_EDGE_QH_QBAR_QT",
            "|alpha_q_edge(lambda)| <= |K_q^R10(lambda)| |Qbar_edge_qH qbar_qT| + abs_tail",
            "template_invalid_boundary_source_test_inputs_missing",
        ),
    ]
    return [
        {
            "model": "MTS_source_normalized_Newton_branch",
            "row_type": row[0],
            "lambda_value": row[1],
            "alpha_predicted": row[2],
            "status": row[3],
            "runner_status": row[4],
            "score_ready": False,
            "valid_for_claim": False,
        }
        for row in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "SMOKE2293_0_runner_status",
            "input_rows": 3,
            "claim_valid_rows": 0,
            "numeric_score_rows": 0,
            "runner_would_claim": False,
            "runner_would_score": False,
            "status": "blocked_nonclaim",
            "valid_for_claim": False,
        }
    ]


def refusal_rows(
    compact: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    projections: list[dict[str, Any]],
    mts_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in compact:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": row["lemma_id"].replace("QQK2293", "REF2293_QQK"),
                "object": row["statement"],
                "status": row["status"],
                "refusal_status": "full_boundary_claim_not_promoted",
                "reason": f"{row['status']};CLAIM_POLICY_FALSE",
                "score_ready": False,
                "valid_for_claim": False,
            }
        )
    for row in gates:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": row["gate_id"].replace("QQG2293", "REF2293_QQG"),
                "object": row["claim"],
                "status": row["gate_status"],
                "refusal_status": "boundary_gate_not_claim_promoted",
                "reason": f"{row['missing_for_promotion']};CLAIM_POLICY_FALSE",
                "score_ready": False,
                "valid_for_claim": False,
            }
        )
    for row in residuals:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": row["residual_id"].replace("BRES2293", "REF2293_BRES"),
                "object": row["symbol"],
                "status": row["missing_inputs"],
                "refusal_status": "residual_retained_missing_inputs",
                "reason": f"{row['missing_inputs']};SCORE_READY_FALSE",
                "score_ready": False,
                "valid_for_claim": False,
            }
        )
    for row in projections:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": row["projection_id"].replace("FBP2293", "REF2293_FBP"),
                "object": row["residual_symbol"],
                "status": row["current_status"],
                "refusal_status": "projection_row_rejected_missing_coefficients",
                "reason": f"{row['current_status']};SCORE_READY_FALSE",
                "score_ready": False,
                "valid_for_claim": False,
            }
        )
    for row in mts_rows:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": f"REF2293_MTS_{row['row_type']}",
                "object": row["row_type"],
                "status": row["runner_status"],
                "refusal_status": "runner_template_rejected_nonclaim",
                "reason": f"{row['alpha_predicted']};VALID_FOR_CLAIM_FALSE",
                "score_ready": False,
                "valid_for_claim": False,
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CGATE2293_0_compact_proper_sublemma",
            "compact proper q-representative boundary transformations are silent",
            "conditional_narrow_only",
            "finite-jet boundary terms vanish when the representative generator and required jets vanish on the boundary collar",
        ),
        (
            "CGATE2293_1_full_local_GR",
            "local GR/no-pole q branch is fully closed",
            "false",
            "source worldtubes, reference/mass projection, exactness, counterterms, parent bracket, degree count, and matter/source readout remain unproved",
        ),
        (
            "CGATE2293_2_alpha3_projection",
            "q boundary alpha3 row is score-ready",
            "false",
            "alpha3 external anchor exists but K_boundary_alpha3_q and Phi_boundary_local_q are missing",
        ),
        (
            "CGATE2293_3_R10_boundary_beta",
            "R10 q edge beta row is score-ready",
            "false",
            "B_q/Q_q, source/test supports, K_q^R10(lambda), and valid bound curve are not jointly sourced",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": row[0],
            "claim": row[1],
            "gate_pass": row[2],
            "reason": row[3],
            "valid_for_claim": False,
        }
        for row in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC2293_0_boundary_derivation",
            "A real but narrow boundary result was derived for the q branch: proper compact q-representative transformations have Q_q=0 and K_boundary=0.",
            "finite-jet boundary charges and cocycles vanish pointwise when the generator and required jets vanish on the boundary collar",
            "do not promote to R10/local-GR; attack the non-proper/source boundary formula next",
        ),
        (
            "DEC2293_1_empirical_fallback",
            "The first q boundary projection fallback row is alpha3_MTS_q=K_boundary_alpha3_q*Phi_boundary_local_q.",
            "alpha3 has a tight source-backed anchor and the boundary/cocycle channel is exactly the missing q obstruction",
            "derive or source K_boundary_alpha3_q and Phi_boundary_local_q, or prove both theorem-zero",
        ),
        (
            "DEC2293_2_R10_fallback",
            "The R10 fallback remains a source-test edge product, not a linear c_g-style row.",
            "finite exchange requires both source and test legs; unknown components must add as absolute tails",
            "write B_q/Q_q and the source/test support projection before scoring",
        ),
        (
            "DEC2293_3_next_target",
            "Next target should write the parent q boundary charge formula rather than inventing a numeric coefficient.",
            "a formula for B_q/Q_q decides both the no-pole route and the alpha3/R10 fallback rows",
            "2294-Y5-R2FR-parent-boundary-charge-formula-Bq-or-alpha3-projection-bound.md",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": row[0],
            "decision": row[1],
            "because": row[2],
            "next_action": row[3],
            "valid_for_claim": False,
        }
        for row in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "2294-Y5-R2FR-parent-boundary-charge-formula-Bq-or-alpha3-projection-bound.md",
            "script": "scripts/Y5_R2FR_parent_boundary_charge_formula_Bq_or_alpha3_projection_bound_2294.py",
            "objective": "derive the explicit parent boundary charge density B_q/Q_q from the symplectic potential and allowed q boundary class; if this cannot close, build the nonclaim alpha3/R10 projection coefficient row for K_boundary_alpha3_q, Phi_boundary_local_q, and Qbar_edge_qH",
            "include": "Theta_Y boundary term, B_q surface density, exact/proper split, reference subtraction, Pi_M/Pi_EH projection, K_boundary cocycle formula, alpha3 projection normalization, R10 edge beta source/test support",
            "exclude": "invented K_boundary values, deleting GR charges, naked linear c_g scoring, cancellation between residuals, R10/local-GR pass claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
        }
    ]


def copy_branch_files() -> list[dict[str, Any]]:
    copy_plan = {
        "queue_boundary": OUTPUTS["boundary_residuals"],
        "queue_alpha3": OUTPUTS["first_projection"],
        "branch_wep": OUTPUTS["first_projection"],
        "beta_docs": OUTPUTS["boundary_residuals"],
    }
    rows: list[dict[str, Any]] = []
    for copy_id, src in copy_plan.items():
        dest = BRANCH_COPY_TARGETS[copy_id]
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source": str(src),
                "destination": str(dest),
                "source_exists": src.exists(),
                "destination_exists": dest.exists(),
                "notes": "branch copy for 2293 boundary q/cocycle checkpoint",
            }
        )
    return rows


def parse_all_generated_csvs(extra: list[Path] | None = None) -> bool:
    paths = list(OUTPUTS.values())
    if extra:
        paths.extend(extra)
    for path in paths:
        if path == OUTPUTS["validation"]:
            continue
        try:
            read_csv(path)
        except Exception:
            return False
    return True


def generated_claim_flags_false(extra: list[Path] | None = None) -> bool:
    claim_fields = {"valid_for_claim", "claim_allowed", "score_ready", "runner_would_claim", "runner_would_score"}
    paths = list(OUTPUTS.values())
    if extra:
        paths.extend(extra)
    for path in paths:
        if path == OUTPUTS["validation"]:
            continue
        for row in read_csv(path):
            for field in claim_fields.intersection(row.keys()):
                if str(row[field]).strip().lower() not in {"false", "0", "no"}:
                    return False
    return True


def prior_validations_pass() -> bool:
    return (
        contains_all(PATHS["2292_validation"], ["VAL2292_OVERALL", "PASS"])
        and contains_all(PATHS["2245_validation"], ["VAL2245_OVERALL", "PASS"])
        and contains_all(PATHS["1039_validation"], ["V1039_SUMMARY", "pass"])
    )


def compact_sublemma_present() -> bool:
    rows = read_csv(OUTPUTS["compact_lemma"])
    statuses = {row["lemma_id"]: row["status"] for row in rows}
    return (
        statuses.get("QQK2293_2_Qq_zero") == "DERIVED_NARROW_PROPER_BRANCH_ONLY"
        and statuses.get("QQK2293_3_Kboundary_zero") == "DERIVED_NARROW_PROPER_BRANCH_ONLY"
        and statuses.get("QQK2293_5_source_boundary_limit") == "FULL_LOCAL_CLAIM_STILL_BLOCKED"
    )


def qq_gates_nonclaim() -> bool:
    rows = read_csv(OUTPUTS["claim_gate"])
    return all(row["valid_for_claim"].lower() == "false" and row["claim_allowed"].lower() == "false" for row in rows)


def residuals_retained() -> bool:
    rows = read_csv(OUTPUTS["boundary_residuals"])
    symbols = {row["symbol"] for row in rows}
    return {"Qbar_edge_qH(lambda)", "K_boundary_alpha3_q", "Q_q^marker"}.issubset(symbols) and all(
        row["score_ready"].lower() == "false" for row in rows
    )


def first_projection_has_alpha3_anchor() -> bool:
    rows = read_csv(OUTPUTS["first_projection"])
    return any(
        row["observable"] == "alpha3"
        and row["anchor_bound"] == "4e-20"
        and row["valid_for_claim"].lower() == "false"
        for row in rows
    )


def mts_template_nonclaim() -> bool:
    rows = read_csv(OUTPUTS["mts_template"])
    return rows and all(row["valid_for_claim"].lower() == "false" for row in rows)


def runner_refuses_claim() -> bool:
    rows = read_csv(OUTPUTS["runner"])
    return bool(rows) and rows[0]["runner_would_claim"].lower() == "false" and rows[0]["status"] == "blocked_nonclaim"


def claim_gates_blocked() -> bool:
    rows = read_csv(OUTPUTS["claim_gates"])
    return all(row["valid_for_claim"].lower() == "false" for row in rows) and any(
        row["gate_id"] == "CGATE2293_0_compact_proper_sublemma" and row["gate_pass"] == "conditional_narrow_only"
        for row in rows
    )


def next_target_written() -> bool:
    rows = read_csv(OUTPUTS["next_target"])
    return rows and rows[0]["next_target"].startswith("2294-Y5-R2FR-parent-boundary-charge-formula-Bq")


def branch_copies_parse() -> bool:
    rows = read_csv(OUTPUTS["branch_copies"])
    if len(rows) != len(BRANCH_COPY_TARGETS):
        return False
    for row in rows:
        path = Path(row["destination"])
        if not path.exists():
            return False
        try:
            read_csv(path)
        except Exception:
            return False
    return True


def formalization_2293_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    ignored = {"__pycache__", ".git", ".venv", "venv", "node_modules"}
    count = 0
    for path in FORMALIZATION.rglob("*2293*"):
        if any(part in ignored for part in path.parts):
            continue
        count += 1
    return count


def formalization_touched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return False
    ignored = {"__pycache__", ".git", ".venv", "venv", "node_modules"}
    for path in FORMALIZATION.rglob("*"):
        if any(part in ignored for part in path.parts):
            continue
        try:
            if path.stat().st_mtime >= START_TS:
                return True
        except OSError:
            continue
    return False


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(branch_copies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    branch_copy_paths = [Path(row["destination"]) for row in branch_copies]
    rows = [
        ("VAL2293_00_sources_exist", all(row["exists"] for row in source_rows()), "all direct and registered 2293 source paths exist"),
        ("VAL2293_01_needles_present", all(row["needles_present"] for row in source_rows()), "all cited source needles are present"),
        ("VAL2293_02_prior_validations", prior_validations_pass(), "2292, 2245, and 1039 validations pass overall"),
        ("VAL2293_03_compact_boundary_sublemma", compact_sublemma_present(), "proper compact Q_q/K_boundary zero is derived but source-boundary promotion is blocked"),
        ("VAL2293_04_qq_kboundary_gates_nonclaim", qq_gates_nonclaim(), "Q_q/K_boundary gates keep all claims non-promoted"),
        ("VAL2293_05_boundary_residuals_retained", residuals_retained(), "q boundary/source/test residuals are retained and non-scoreable"),
        ("VAL2293_06_first_projection_alpha3_anchor", first_projection_has_alpha3_anchor(), "first q boundary projection uses source-backed alpha3 anchor but remains nonclaim"),
        ("VAL2293_07_mts_template_nonclaim", mts_template_nonclaim(), "MTS q boundary smoke template has no claim-valid rows"),
        ("VAL2293_08_runner_smoke_refuses_claim", runner_refuses_claim(), "runner smoke refuses to score or claim"),
        ("VAL2293_09_refusal_runner", len(read_csv(OUTPUTS["refusal"])) >= 20 and generated_claim_flags_false(), "placeholder refusal runner blocks boundary and beta claims"),
        ("VAL2293_10_claim_gates_blocked", claim_gates_blocked(), "all empirical/local-GR claim gates remain blocked"),
        ("VAL2293_11_next_target_written", next_target_written(), "next target selects parent B_q/Q_q formula or coefficient row"),
        ("VAL2293_12_csv_parse", parse_all_generated_csvs(branch_copy_paths), "all generated 2293 CSVs parse cleanly"),
        ("VAL2293_13_claim_flags_false", generated_claim_flags_false(branch_copy_paths), "all generated prediction/claim flags remain false"),
        ("VAL2293_14_branch_copies", branch_copies_parse(), "branch/queue copies exist and parse"),
        ("VAL2293_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL2293_16_formalization_no_2293", formalization_2293_count() == 0, "formalization-workbench has no non-venv 2293 artifacts"),
        ("VAL2293_17_formalization_untouched", not formalization_touched_since_start(), "formalization-workbench untouched during 2293 run"),
    ]
    validation = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in rows
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2293_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "2293 derives the narrow compact/proper Q_q and K_boundary silence sublemma, retains source-boundary beta rows, and selects parent B_q/Q_q formula next",
        }
    )
    return validation


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def build_doc(
    sources: list[dict[str, Any]],
    compact: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    projections: list[dict[str, Any]],
    alpha3: list[dict[str, Any]],
    mts_rows: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branch_copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    source_table_rows = [{**row, "path": path_display(Path(row["path"]))} for row in sources]
    branch_table_rows = [
        {**row, "source": path_display(Path(row["source"])), "destination": path_display(Path(row["destination"]))}
        for row in branch_copies
    ]
    return "\n\n".join(
        [
            "# 2293 - Y5/R2FR Boundary Charge Q_q/Kboundary Zero or Beta-Bound First Row",
            "## Verdict\n"
            "- 2293 gets one real derived brick: for proper compact q-representative transformations, where the generator and required finite jets vanish on a boundary collar, both `Q_q` and `K_boundary` vanish.\n"
            "- That is not a local-GR/R10 pass. Source worldtubes, non-proper transformations, reference/mass projections, material/readout markers, and range-kernel edge projections remain live.\n"
            "- The first concrete fallback projection is `alpha3_MTS_q=K_boundary_alpha3_q*Phi_boundary_local_q`, anchored to the source-backed `alpha3 <= 4e-20` row but nonclaim until the MTS projection coefficients are derived, sourced, or theorem-zeroed.",
            "## Source Register\n" + md_table(source_table_rows, ["source_id", "role", "path", "exists", "needles_present", "notes", "valid_for_claim"]),
            "## Compact/Proper Boundary Silence Lemma\n" + md_table(compact, ["lemma_id", "statement", "derivation_or_test", "status", "limitation", "claim_allowed", "valid_for_claim"]),
            "## Q_q/Kboundary Claim Gate\n" + md_table(gates, ["gate_id", "claim", "gate_status", "evidence", "missing_for_promotion", "claim_allowed", "valid_for_claim"]),
            "## Boundary Residual Beta Rows\n" + md_table(residuals, ["residual_id", "symbol", "formula_or_contract", "why_retained", "missing_inputs", "score_ready", "valid_for_claim"]),
            "## First Beta Projection Template\n" + md_table(projections, ["projection_id", "residual_symbol", "observable", "projection_formula", "external_anchor", "anchor_bound", "missing_mts_inputs", "current_status", "score_ready", "valid_for_claim"]),
            "## Alpha3 Anchor Ledger\n" + md_table(alpha3, ["anchor_id", "dataset_id", "observable", "upper_bound", "units", "reference", "use_in_2293", "valid_for_claim"]),
            "## MTS Smoke Template\n" + md_table(mts_rows, ["model", "row_type", "lambda_value", "alpha_predicted", "status", "runner_status", "score_ready", "valid_for_claim"]),
            "## Runner Smoke Status\n" + md_table(runner, ["runner_id", "input_rows", "claim_valid_rows", "numeric_score_rows", "runner_would_claim", "runner_would_score", "status", "valid_for_claim"]),
            "## Placeholder Refusal Runner\n" + md_table(refusal, ["refusal_id", "object", "status", "refusal_status", "reason", "score_ready", "valid_for_claim"]),
            "## Claim Gates\n" + md_table(claim_gates, ["gate_id", "claim", "gate_pass", "reason", "valid_for_claim"]),
            "## Decision Ledger\n" + md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target\n" + md_table(next_target, ["next_target", "script", "objective", "include", "exclude", "valid_for_claim"]),
            "## Branch Copies\n" + md_table(branch_table_rows, ["copy_id", "source", "destination", "source_exists", "destination_exists", "notes"]),
            "## Validation\n" + md_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n"
            "This is a bounded win, not a victory lap. The q branch now has a legitimate compact/proper boundary-silence sublemma, which helps the GR-reduction route because pure representative changes do not automatically carry edge charge. The dangerous bit is still the source/non-proper boundary formula. So the next move is sharp: write `B_q/Q_q` from the parent symplectic potential and boundary class, or keep the branch as explicit bounded beta rows.",
        ]
    ) + "\n"


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    compact = compact_lemma_rows()
    gates = qq_gate_rows()
    residuals = boundary_residual_rows()
    projections = first_projection_rows()
    alpha3 = alpha3_rows()
    mts_rows = mts_template_rows()
    runner = runner_rows()
    refusal = refusal_rows(compact, gates, residuals, projections, mts_rows)
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["compact_lemma"], compact)
    write_csv(OUTPUTS["claim_gate"], gates)
    write_csv(OUTPUTS["boundary_residuals"], residuals)
    write_csv(OUTPUTS["first_projection"], projections)
    write_csv(OUTPUTS["alpha3_anchor"], alpha3)
    write_csv(OUTPUTS["mts_template"], mts_rows)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)
    branch_copies = copy_branch_files()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    remove_pycache()
    validation = validation_rows(branch_copies)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(
        build_doc(
            sources,
            compact,
            gates,
            residuals,
            projections,
            alpha3,
            mts_rows,
            runner,
            refusal,
            claim_gates,
            decisions,
            next_target,
            branch_copies,
            validation,
        ),
        encoding="utf-8",
    )
    remove_pycache()

    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        failed_ids = ", ".join(row["check_id"] for row in failed)
        raise SystemExit(f"2293 validation failed: {failed_ids}")
    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
