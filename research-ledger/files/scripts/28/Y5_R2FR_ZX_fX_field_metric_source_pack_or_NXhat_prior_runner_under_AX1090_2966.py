from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_SOURCE = ROOT / "source-intake" / "beta-source" / "docs"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight" / "docs"
WEP_SOURCES = ROOT / "source-intake" / "wep-sources"
QUARANTINE_1848 = ROOT / "source-intake" / "microscope" / "quarantine" / "1848"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2966"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2966-Y5-R2FR-ZX-fX-field-metric-source-pack-or-NXhat-prior-runner-under-AX1090.md"

SRC_2965_DOC = ROOT / "2965-Y5-R2FR-NXhat-field-metric-owner-or-first-prior-slot-under-AX1090.md"
SRC_2965_NEXT = RESIDUALS / "P8_Y5_R2FR_2965_NEXT_TARGET.csv"
SRC_2965_OWNER = RESIDUALS / "P8_Y5_R2FR_2965_NXHAT_FIELD_METRIC_OWNER_GATE.csv"
SRC_2965_PRIOR = RESIDUALS / "P8_Y5_R2FR_2965_NXHAT_FIRST_PRIOR_SLOT_NONCLAIM.csv"
SRC_2965_RESCALING = RESIDUALS / "P8_Y5_R2FR_2965_RESCALING_GUARD_AUDIT.csv"
SRC_2965_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2965_VALIDATION.csv"
SRC_2157_METRIC = SOURCE_WEIGHT / "AFRAME_PARENT_METRIC_TRACE_2157_NONCLAIM.csv"
SRC_2197_ZX = BETA_SOURCE / "PARENT_QLOC_ZX_RESIDUE_OWNER_CONTRACT_2197_NONCLAIM.csv"
SRC_1847_LOCKS = RESIDUALS / "P8_Y5_PARENT_QLOC_1847_FIELD_NORMALIZATION_LOCKS.csv"
SRC_1848_METRIC = QUARANTINE_1848 / "P8_Y5_PARENT_QLOC_1848_PARENT_METRIC_ATTEMPT.csv"
SRC_2211_ZM = BETA_SOURCE / "PARENT_QLOC_ZM_OWNER_AUDIT_2211_NONCLAIM.csv"
SRC_2217_RDP = BETA_SOURCE / "PARENT_QLOC_RESPONSE_DOUBLET_DENSITY_2217_NONCLAIM.csv"
SRC_2213_RANK_ZERO = BETA_SOURCE / "PARENT_QLOC_RANK_ZERO_SOURCE_CURRENT_2213_NONCLAIM.csv"
SRC_2206_WARD = BETA_SOURCE / "PARENT_QLOC_WARD_IDENTITY_2206_NONCLAIM.csv"
SRC_2676_OWNER = WEP_SOURCES / "action_scale_measure_owner_wip_nonclaim_2676.csv"
SRC_2912_CONSTRAINT = PARENT_ACTION / "Constraint_first_Z_elimination_2912_NONCLAIM.csv"
SRC_2940_SECTORS = PARENT_ACTION / "Sector_certificate_matrix_2940_NONCLAIM.csv"
SRC_2954_FIELD = PARENT_ACTION / "field_space_law_audit_2954_NONCLAIM.csv"
SRC_2963_PROMOTION = RESIDUALS / "P8_Y5_R2FR_2963_PROMOTION_RULES.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2966_SOURCE_REGISTER.csv",
    "derivation": RESIDUALS / "P8_Y5_R2FR_2966_CONDITIONAL_DERIVATION_LEDGER.csv",
    "source_pack": RESIDUALS / "P8_Y5_R2FR_2966_ZX_FX_FIELD_METRIC_SOURCE_PACK_GATE.csv",
    "route_triage": RESIDUALS / "P8_Y5_R2FR_2966_PARENT_METRIC_ROUTE_TRIAGE.csv",
    "prior_runner": RESIDUALS / "P8_Y5_R2FR_2966_NXHAT_PRIOR_RUNNER_INTAKE_NONCLAIM.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2966_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2966_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2966_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2966_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2966_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "source_pack_copy": PARENT_ACTION / "ZX_fX_field_metric_source_pack_2966_NOT_DERIVED.csv",
    "prior_runner_copy": LOCAL_BOUNDS / "NXhat_prior_runner_intake_2966_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2966_PARENT_METRIC_ROUTE_OR_ZXFX_PRIOR_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def all_semicolon_paths_exist(paths: str) -> bool:
    return all(Path(path).exists() for path in paths.split(";") if path)


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2966_00_2965_doc", SRC_2965_DOC, "NEXT2965_0_2966;Z_X f_X^2", "2965 handoff"),
        ("SRC2966_01_2965_next", SRC_2965_NEXT, "NEXT2965_0_2966", "machine-readable 2966 target"),
        ("SRC2966_02_2965_owner", SRC_2965_OWNER, "FM2965_2_ZX_fX_product;FM2965_5_verdict", "N_Xhat owner gate"),
        ("SRC2966_03_2965_prior", SRC_2965_PRIOR, "NXHAT2965_1_ZX_fX_product;NXHAT2965_3_acceptance_rule", "prior slot input"),
        ("SRC2966_04_2965_rescaling", SRC_2965_RESCALING, "RG2965_1_product_invariant;RG2965_3_limit", "rescaling guard"),
        ("SRC2966_05_2965_validation", SRC_2965_VALIDATION, "VAL2965_OVERALL", "2965 validation"),
        ("SRC2966_06_2157_metric", SRC_2157_METRIC, "PML2157_0_parent_metric_object;PML2157_3_stress_bianchi_variation;PML2157_5_verdict", "metric pack contract"),
        ("SRC2966_07_2197_ZX", SRC_2197_ZX, "ZOC2197_2_schur_complement;ZOC2197_3_metric_lock;ZOC2197_5_verdict", "Z_X ownership contract"),
        ("SRC2966_08_1847_locks", SRC_1847_LOCKS, "FNL1847_1_canonical_metric;FNL1847_4_CX_tie", "field normalization locks"),
        ("SRC2966_09_1848_metric", SRC_1848_METRIC, "PM1848_0_metric_target;PM1848_5_cross_block_guard;PM1848_6_verdict", "parent metric attempt"),
        ("SRC2966_10_2211_ZM", SRC_2211_ZM, "ZMO2211_0_parent_quadratic_form;ZMO2211_5_verdict", "quadratic operator owner audit"),
        ("SRC2966_11_2217_RDP", SRC_2217_RDP, "RDP2217_0_parent_action_ansatz;RDP2217_3_Hessian_owner;RDP2217_4_density_verdict", "response-doublet density candidate"),
        ("SRC2966_12_2213_rank_zero", SRC_2213_RANK_ZERO, "RZS2213_2_rank_zero_silence_theorem;RZS2213_4_verdict", "rank-zero fallback"),
        ("SRC2966_13_2206_Ward", SRC_2206_WARD, "WID2206_1_if_parent_action;WID2206_4_current_verdict", "Ward/Bianchi route"),
        ("SRC2966_14_2676_owner", SRC_2676_OWNER, "OWN2676_2_hilbert_current_sublemma;OWN2676_4_verdict", "matter current owner"),
        ("SRC2966_15_2912_constraint", SRC_2912_CONSTRAINT, "CFP2912_2_second_class_route;CFP2912_4_rank_zero_algebraic;CFP2912_5_current_verdict", "constraint-first branch"),
        ("SRC2966_16_2940_sectors", SRC_2940_SECTORS, "SEC2940_3_GK_q_loc;SEC2940_9_total", "sector certificate matrix"),
        ("SRC2966_17_2954_field", SRC_2954_FIELD, "LAW2954_0_exact_second_variation;LAW2954_6_verdict", "field-space law"),
        ("SRC2966_18_2963_promotion", SRC_2963_PROMOTION, "PROM2963_1_Xhat;PROM2963_6_verdict", "runner promotion rule"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def derivation_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DER2966_0_parent_quadratic_form",
            "parent local field-space block",
            "S2=1/2 int sqrt(h)[G_AB h^ij partial_i deltaPhi^A partial_j deltaPhi^B + H_AB deltaPhi^A deltaPhi^B] plus explicitly retained source/boundary terms.",
            "CONDITIONAL_FIELD_THEORY_TEMPLATE",
            "standard second variation; source pack must identify G_AB, H_AB, domain and source split",
            True,
            False,
        ),
        (
            "DER2966_1_project_to_X",
            "single X direction",
            "deltaPhi^A=f_X e_X^A x gives Z_x=f_X^2 G_AB e_X^A e_X^B and M_x^2=f_X^2 H_AB e_X^A e_X^B when cross blocks are absent or Schur-reduced.",
            "DERIVED_CONDITIONALLY",
            "this is the exact invariant bridge from parent metric to the 2965 N_Xhat slot",
            True,
            False,
        ),
        (
            "DER2966_2_metric_amplitude_invariant",
            "Z_X f_X^2",
            "the physical normalization is G_X f_X^2, equivalently Z_X f_X^2 in the raw-coordinate convention; raw Z_X alone is coordinate-dependent.",
            "INVARIANT_DERIVED",
            "under x->a x, Z_x->Z_x/a^2 and source derivatives transform oppositely, so products cannot be tuned after local tests",
            True,
            False,
        ),
        (
            "DER2966_3_vacuum_lock",
            "canonical finite-route lock",
            "if a parent Ward/metric theorem gives Z_X f_X^2=rho_vac^(1/2), then beta_eff=ell_vac^2 M_X^2/Z_X=U''(0) for the same branch.",
            "CLEAN_CONTRACT_CONDITIONAL",
            "this is the attractive low-scrutiny theorem target, but the Ward/metric theorem is not signed",
            True,
            False,
        ),
        (
            "DER2966_4_schur_guard",
            "mixed-sector protection",
            "with coupled residuals, use G_eff=G_XX-G_Xa G_ab^{-1} G_bX and the analogous Hessian Schur block, or prove cross blocks vanish.",
            "DERIVED_GUARDRAIL",
            "prevents a one-scalar local branch from hiding memory/domain/projector/metric tails",
            True,
            False,
        ),
        (
            "DER2966_5_stress_bianchi_guard",
            "variation compatibility",
            "M_AB, e_X, f_X and V_eff must vary inside the parent stress tensor so Bianchi/Ward conservation accounts for the same normalization used in local tests.",
            "DERIVED_REQUIREMENT",
            "a fixed number is not enough; the metric pack must be variational, not pasted after readout",
            True,
            False,
        ),
    ]
    return [
        add_common(
            {
                "derivation_id": derivation_id,
                "object": obj,
                "statement": statement,
                "status": status,
                "effect": effect,
                "conditional_math_available": conditional,
                "accepted_for_scoring": accepted,
            }
        )
        for derivation_id, obj, statement, status, effect, conditional, accepted in rows
    ]


def source_pack_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PACK2966_0_parent_metric",
            "M_AB",
            "one parent field-space metric/principal-symbol block on the physical quotient before readout",
            "TARGET_DEFINED_NOT_OWNED",
            "2157/1848 define M_AB/G_X, 2211 requests the quadratic operator, but no parent action branch signs it",
            False,
            "source-signed parent action and field-space metric",
        ),
        (
            "PACK2966_1_X_direction",
            "e_X",
            "normalized X direction/eigenvector in the same parent metric, with gauge/constraint quotient fixed",
            "MISSING_EIGENBASIS_AND_QUOTIENT",
            "2965 names Xhat but 2951/2197 keep field identity and source branch unsigned",
            False,
            "field identity, eigenbasis, quotient tangent and units",
        ),
        (
            "PACK2966_2_amplitude",
            "f_X",
            "parent amplitude/field-unit map connecting dimensionless x to physical field displacement",
            "MISSING_AMPLITUDE_OWNER",
            "2157 gives X_phys=f_X x conditionally; 1847 forbids choosing it from local bounds",
            False,
            "parent rods/clocks/readout or field unit theorem",
        ),
        (
            "PACK2966_3_ZX_fX",
            "Z_X f_X^2",
            "source-backed invariant metric/amplitude product, ideally Z_X f_X^2=rho_vac^(1/2)",
            "CLEAN_CONTRACT_NOT_SIGNED",
            "2954/2157/1847 align on the target, but no Ward/current norm or defect theorem owns it",
            False,
            "parent Ward/current norm or defect Hessian theorem with units",
        ),
        (
            "PACK2966_4_stress_bianchi",
            "stress/Bianchi variation",
            "delta_g(M_AB,e_X,f_X,V_eff) enters the parent stress so conservation and source normalization use the same object",
            "MISSING_STRESS_BIANCHI_VARIATION",
            "2157 flags this as mandatory; 2206/2940 keep the parent Ward route unsigned",
            False,
            "Bianchi-compatible parent variation and source silence/bounds",
        ),
        (
            "PACK2966_5_schur",
            "Schur/cross-block guard",
            "cross metric/Hessian/source blocks vanish, are positive Schur-complemented, or are retained as residual coefficients",
            "MISSING_BLOCK_DIAGONAL_OR_SCHUR_PROOF",
            "2197/1848/2211 all keep mixed sectors unresolved",
            False,
            "cross-Hessian matrix, positive orthogonal block theorem and residual ledger",
        ),
        (
            "PACK2966_6_same_branch_coupling",
            "lambda_X/K_X/beta_source/test",
            "same parent normalization feeds range, source/test charges and R10/PPN couplings",
            "MISSING_COUPLING_NORMALIZATION_LEDGER",
            "1847 C_X tie and 2663 K_X normalization remain nonclaim",
            False,
            "one source ledger tying Z_X f_X^2, lambda_X, K_X and beta rows",
        ),
        (
            "PACK2966_7_verdict",
            "Z_X f_X^2 source pack",
            "PACK2966_0 through PACK2966_6 close from one parent branch",
            "ZX_FX_SOURCE_PACK_NOT_ACQUIRED",
            "conditional derivation is good; source ownership is still missing",
            False,
            "do not score R10/PPN/local-GR; triage parent route next",
        ),
    ]
    return [
        add_common(
            {
                "pack_id": pack_id,
                "object": obj,
                "required_payload": payload,
                "current_status": status,
                "evidence_summary": evidence,
                "payload_acquired": acquired,
                "missing_for_claim": missing,
            }
        )
        for pack_id, obj, payload, status, evidence, acquired, missing in rows
    ]


def route_triage_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ROUTE2966_0_response_doublet",
            "response-doublet density",
            "RDP2217 writes S_GK=-int sqrt(-g) Gamma_eff with Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4)",
            "BEST_NEXT_DERIVATION_TARGET",
            "strongest local skeleton for M_AB and double-zero, but not parent-adopted and lacks kinetic principal symbol",
            "try parent adoption/Khat match; if no gradient block appears, switch to rank-zero algebraic branch",
        ),
        (
            "ROUTE2966_1_defect_hessian",
            "defect potential Hessian",
            "M_AB=partial_A partial_B V_def|0 could own the metric/amplitude if V_def and units are parent-signed",
            "SECONDARY_ROUTE",
            "partial trace/flow support exists, but full V_def, cross terms and stress variation are not derived",
            "keep as backup to response-doublet route",
        ),
        (
            "ROUTE2966_2_Ward_current_norm",
            "Ward/current norm",
            "M_AB=<J_A,J_B> or a current inner product could own the metric through symmetry",
            "HIGH_SCRUTINY_ROUTE",
            "needs current basis, inner product, sign, source universality and stress/Bianchi variation",
            "do not lead with this unless response-doublet and defect routes fail",
        ),
        (
            "ROUTE2966_3_rank_zero",
            "rank-zero algebraic branch",
            "if no kinetic Z_AB exists, local silence may be algebraic: M_AB Z^B=J_A+B_A+C_A^CDB+R_A",
            "GR_REDUCTION_FALLBACK_ROUTE",
            "best path for derived local GR if finite-range coupling stays unowned; not an R10 Yukawa claim",
            "promote only after source/boundary/readout terms close or are bounded",
        ),
    ]
    return [
        add_common(
            {
                "route_id": route_id,
                "route": route,
                "candidate_basis": basis,
                "status": status,
                "why": why,
                "next_action": action,
            }
        )
        for route_id, route, basis, status, why, action in rows
    ]


def prior_runner_rows() -> list[dict[str, Any]]:
    source_paths = ";".join(
        str(path)
        for path in [
            SRC_2965_PRIOR,
            SRC_2965_OWNER,
            SRC_2157_METRIC,
            SRC_2197_ZX,
            SRC_1847_LOCKS,
            SRC_1848_METRIC,
            SRC_2211_ZM,
            SRC_2217_RDP,
            SRC_2213_RANK_ZERO,
            SRC_2963_PROMOTION,
        ]
    )
    rows = [
        (
            "ZXFX2966_0_invariant_slot",
            "Z_X f_X^2",
            "field_metric_times_amplitude_squared",
            "MISSING_PARENT_SIGNED_PRODUCT",
            "single invariant normalization slot for future prior/smoke rows; lower scrutiny than raw N_Xhat",
            "PROM2963_1_Xhat",
        ),
        (
            "ZXFX2966_1_route_label",
            "source_pack_route",
            "categorical",
            "candidate_values: response_doublet; defect_hessian; Ward_current_norm; rank_zero_fallback",
            "forces future rows to state which parent route owns the value",
            "PACK2966_7_verdict",
        ),
        (
            "ZXFX2966_2_no_claim_policy",
            "promotion policy",
            "policy",
            "valid_for_claim=false until PACK2966_0..6 are source-backed and no MISSING markers remain",
            "prevents using a fitted prior as a field-theory derivation",
            "PROM2963_6_verdict",
        ),
    ]
    return [
        add_common(
            {
                "runner_row_id": row_id,
                "symbol": symbol,
                "units": units,
                "numeric_or_theorem_value": value,
                "role": role,
                "runner_hook": hook,
                "source_path": source_paths,
                "source_path_exists": all_semicolon_paths_exist(source_paths),
                "accepted_for_scoring": False,
                "no_cancellation_policy": True,
            }
        )
        for row_id, symbol, units, value, role, hook in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2966_0_source_pack", "Z_X f_X^2 source pack acquired", False, "ZX_FX_SOURCE_PACK_NOT_ACQUIRED"),
        ("CG2966_1_parent_metric", "M_AB/e_X/f_X parent-owned", False, "FIELD_METRIC_OWNER_MISSING"),
        ("CG2966_2_stress_bianchi", "stress/Bianchi variation closes", False, "VARIATIONAL_OWNER_MISSING"),
        ("CG2966_3_schur", "Schur/cross-block guard closes", False, "MIXED_BLOCKS_OPEN"),
        ("CG2966_4_runner", "2963 runner can accept an MTS normalization row", False, "VALID_MTS_ROWS_ZERO"),
        ("CG2966_5_local_tests", "R10/PPN/clock/orbital scoring allowed", False, "LOCAL_TEST_CLAIMS_BLOCKED"),
        ("CG2966_6_GR_Newton", "derived local GR/Newton reduction claimed", False, "NO_LOCAL_GR_OR_NEWTON_CLAIM"),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
            }
        )
        for gate_id, claim, passed, status in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC2966_0_derivation",
            "conditional source-pack derivation succeeded",
            "the exact relationship between parent metric, X direction, f_X and Z_X f_X^2 is now written",
            "use the formula as a contract, not as a claim",
        ),
        (
            "DEC2966_1_source_pack",
            "source pack not acquired",
            "current corpus does not sign M_AB/e_X/f_X/stress/Schur/source coupling from one parent branch",
            "keep all local-test claims blocked",
        ),
        (
            "DEC2966_2_route",
            "response-doublet route selected first",
            "it already has the cleanest M_AB/double-zero skeleton; the missing part is parent adoption plus kinetic/principal-symbol status",
            "attack response-doublet parent density next",
        ),
        (
            "DEC2966_3_fallback",
            "rank-zero branch remains live",
            "if no kinetic Z_AB exists, the right GR route may be algebraic source elimination rather than finite Yukawa range",
            "do not force a finite-range branch if the parent action is algebraic",
        ),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": action,
            }
        )
        for decision_id, decision, because, action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2966_0_2967",
                "priority": "selected_primary",
                "next_doc": "2967-Y5-R2FR-response-doublet-parent-density-adoption-or-rank-zero-switch-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_response_doublet_parent_density_adoption_or_rank_zero_switch_under_AX1090_2967.py",
                "objective": "Try to promote or reject the response-doublet parent-density route for M_AB/Z_X f_X^2 by checking parent adoption, Khat/Gamma matching, kinetic principal symbol, units, domain, stress variation and source silence. If no kinetic branch exists, switch explicitly to rank-zero algebraic local-GR route.",
                "include": "response-doublet density;Gamma_eff;Khat match;M_AB;Z_AB principal symbol;double-zero;units;domain;stress/Bianchi;rank-zero fallback;source/boundary residuals",
                "exclude": "R10 alpha claim;PPN claim;clock/orbital claim;local-GR claim;GitHub action;formalization-workbench edits;fitted beta;raw mode-count beta=3;normalization from local bounds",
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("source_pack_copy", OUTPUTS["source_pack"], BRANCH_OUTPUTS["source_pack_copy"]),
        ("prior_runner_copy", OUTPUTS["prior_runner"], BRANCH_OUTPUTS["prior_runner_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        shutil.copyfile(source, target)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "copy_path": str(target),
                    "source_exists": source.exists(),
                    "copy_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = all_rows["sources"]
    generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    csv_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2966_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2966_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all cited source anchors found", True),
        ("VAL2966_2_derivation_written", any(row["derivation_id"] == "DER2966_2_metric_amplitude_invariant" and row["conditional_math_available"] is True for row in all_rows["derivation"]), "metric/amplitude invariant derivation is recorded", True),
        ("VAL2966_3_source_pack_blocked", any(row["pack_id"] == "PACK2966_7_verdict" and row["payload_acquired"] is False for row in all_rows["source_pack"]), "Z_X f_X^2 source pack remains blocked", True),
        ("VAL2966_4_route_selected", any(row["route_id"] == "ROUTE2966_0_response_doublet" and row["status"] == "BEST_NEXT_DERIVATION_TARGET" for row in all_rows["route_triage"]), "response-doublet route selected as next derivation target", True),
        ("VAL2966_5_prior_runner_nonclaim", all(row["accepted_for_scoring"] is False and row["valid_for_claim"] is False for row in all_rows["prior_runner"]), "prior-runner rows remain nonclaim", True),
        ("VAL2966_6_prior_paths_exist", all(row["source_path_exists"] is True for row in all_rows["prior_runner"]), "prior-runner rows cite existing paths", True),
        ("VAL2966_7_claims_blocked", all(row["condition_passed"] is False and row["claim_allowed"] is False for row in all_rows["claims"]), "all claim gates remain blocked", True),
        ("VAL2966_8_next_target_written", any(row["next_id"] == "NEXT2966_0_2967" for row in all_rows["next"]), "2967 next target selected", True),
        ("VAL2966_9_branches_exist", all(Path(row["copy_path"]).exists() for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2966_10_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2966_11_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2966_12_formalization_clean", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no 2966 outputs were written to formalization-workbench", True),
        ("VAL2966_13_doc_written", DOC.exists(), "2966 markdown checkpoint exists", True),
    ]
    overall = all(passed == required for _, passed, _, required in checks)
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "required": required,
            }
        )
        for validation_id, passed, check, required in checks
    ]
    rows.append(add_common({"validation_id": "VAL2966_OVERALL", "passed": overall, "check": "2966 validation overall", "required": True}))
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2966 - Y5 R2FR: Z_X f_X field-metric source pack or N_Xhat prior-runner under AX1090

Status: `Y5_R2FR_2966_ZX_fX_conditional_derivation_written_source_pack_not_acquired_response_doublet_route_selected`

Claim ceiling: `no_ZX_fX_claim_no_NXhat_promotion_no_lambda_claim_no_R10_PPN_clock_orbital_claim_no_local_GR_no_Newton_no_public_claim`

2966 asks whether the invariant normalization/coupling pack can be sourced now.

- Conditional derivation: a parent quadratic field-space block gives `Z_x=f_X^2 G_AB e_X^A e_X^B`; this is the invariant bridge behind the `N_Xhat` slot.
- The attractive theorem target remains `Z_X f_X^2=rho_vac^(1/2)`, because then `beta_eff=U''(0)` in the same branch.
- The source pack is not acquired: `M_AB`, `e_X`, `f_X`, stress/Bianchi variation, Schur/cross-block control and same-branch coupling normalization are not all signed.
- Route triage selects the response-doublet density as the next derivation attempt; if it has no kinetic/principal-symbol branch, the honest fallback is rank-zero algebraic local-GR rather than a fake finite-range branch.

## Source Register

{md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## Conditional Derivation Ledger

{md_table(all_rows["derivation"], ["derivation_id", "object", "status", "conditional_math_available", "accepted_for_scoring", "effect"])}

## Z_X f_X Source Pack Gate

{md_table(all_rows["source_pack"], ["pack_id", "object", "current_status", "payload_acquired", "missing_for_claim"])}

## Parent Metric Route Triage

{md_table(all_rows["route_triage"], ["route_id", "route", "status", "why", "next_action"])}

## N_Xhat Prior-Runner Intake

{md_table(all_rows["prior_runner"], ["runner_row_id", "symbol", "numeric_or_theorem_value", "accepted_for_scoring", "role"])}

## Claim Gates

{md_table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{md_table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(all_rows["branches"], ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_register_rows(),
        "derivation": derivation_rows(),
        "source_pack": source_pack_rows(),
        "route_triage": route_triage_rows(),
        "prior_runner": prior_runner_rows(),
        "claims": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }

    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    print(f"2966 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
