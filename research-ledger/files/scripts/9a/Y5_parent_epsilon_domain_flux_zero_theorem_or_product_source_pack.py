from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1515-Y5-parent-epsilon-domain-flux-zero-theorem-or-product-source-pack.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1514_validation": OUT / "P8_Y5_BRR545_1514_VALIDATION.csv",
    "1514_alpha3": OUT / "P8_Y5_PARENT_GENERATOR_1514_ALPHA3_FLUX_PRODUCT_LOCK.csv",
    "1514_next": OUT / "P8_Y5_PARENT_GENERATOR_1514_NEXT_TARGET.csv",
    "1133_derivation": OUT / "P8_Y5_R10_1133_FLUX_ZERO_DERIVATION_LEDGER.csv",
    "1133_blockers": OUT / "P8_Y5_R10_1133_HARMONIC_CIRCULATION_BLOCKER.csv",
    "1134_lemma": OUT / "P8_Y5_R10_1134_NO_SWIRL_HARMONIC_LEMMA_AUDIT.csv",
    "1134_contract": OUT / "P8_Y5_R10_1134_CONDITIONAL_THEOREM_CONTRACT.csv",
    "1135_constitutive": OUT / "P8_Y5_R10_1135_FD_GRADIENT_FLOW_CONSTITUTIVE_AUDIT.csv",
    "1135_demotion": OUT / "P8_Y5_R10_1135_EPSILON_CLOSURE_DEMOTION_LEDGER.csv",
    "1136_pack": OUT / "P8_Y5_R10_1136_EPSILON_W_K_C_SOURCE_PACK_FIRST_ROWS.csv",
    "1136_products": OUT / "P8_Y5_R10_1136_ALPHA3_PRODUCT_INEQUALITY_ROWS.csv",
    "1137_couplings": OUT / "P8_Y5_R10_1137_W_K_C_COUPLING_AUDIT.csv",
    "1138_c_zero": OUT / "P8_Y5_R10_1138_C_ZERO_ROUTE_AUDIT.csv",
    "1146_no_flux": OUT / "P8_Y5_R10_1146_NO_FLUX_CERTIFICATE_AUDIT.csv",
    "1146_profile": OUT / "P8_Y5_R10_1146_EPSILON_SOURCE_PROFILE_ROW.csv",
    "1147_acquisition": OUT / "P8_Y5_R10_1147_EPSILON_ACQUISITION_SCAN.csv",
    "1147_demotion": OUT / "P8_Y5_R10_1147_CLOSURE_DEMOTION_LEDGER.csv",
    "1147_pivot": OUT / "P8_Y5_R10_1147_KC_PIVOT_MATRIX.csv",
    "r11_minimum": OUT / "R11_DOMAIN_PROJECTOR_OPERATOR_VECTOR_MINIMUM.csv",
    "r11_skeleton": OUT / "R11_MTS_MINIMUM_EXECUTABLE_VECTOR_SKELETON.csv",
    "1122_flux": OUT / "P8_Y5_R10_1122_REMAINING_FLUX_CONTRACT.csv",
    "1123_alpha3": OUT / "P8_Y5_R10_1123_ALPHA3_FLUX_BOUND_PRODUCT_ROWS.csv",
    "1451_no_slot": OUT / "P8_Y5_R10_1451_NO_SOURCE_ONLY_SLOT_OPERATOR_GRAMMAR_THEOREM_ATTEMPT.csv",
    "1451_decision": OUT / "P8_Y5_R10_1451_DECISION_LEDGER.csv",
}

ZERO_THEOREM_AUDIT = OUT / "P8_Y5_PARENT_EPSILON_1515_ZERO_THEOREM_AUDIT.csv"
CONDITIONAL_CONTRACT = OUT / "P8_Y5_PARENT_EPSILON_1515_CONDITIONAL_FLUX_THEOREM_CONTRACT.csv"
SOURCE_RESCAN = OUT / "P8_Y5_PARENT_EPSILON_1515_SOURCE_ACQUISITION_RESCAN.csv"
PRODUCT_SOURCE_PACK = OUT / "P8_Y5_PARENT_EPSILON_1515_PRODUCT_SOURCE_PACK.csv"
PIVOT_MATRIX = OUT / "P8_Y5_PARENT_EPSILON_1515_C_R11_PIVOT_MATRIX.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_EPSILON_1515_REJECTION_LEDGER.csv"
DECISION = OUT / "P8_Y5_PARENT_EPSILON_1515_DECISION.csv"
LOCAL_STATUS = OUT / "P8_Y5_PARENT_EPSILON_1515_LOCAL_GR_NEWTON_STATUS.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_EPSILON_1515_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1515_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1515"
QUAR_ZERO = QUARANTINE / "EPSILON_ZERO_THEOREM_AUDIT_NONCLAIM.csv"
QUAR_PRODUCTS = QUARANTINE / "EPSILON_PRODUCT_SOURCE_PACK_NONCLAIM.csv"
QUAR_PIVOT = QUARANTINE / "C_R11_PIVOT_MATRIX_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "EPSILON_DECISION_NONCLAIM.csv"
BRANCH_ZERO = BRANCH_RESIDUALS / "epsilon_zero_theorem_audit_nonclaim_1515.csv"
BRANCH_PRODUCTS = BRANCH_RESIDUALS / "epsilon_product_source_pack_nonclaim_1515.csv"
BRANCH_PIVOT = BRANCH_RESIDUALS / "c_r11_pivot_matrix_nonclaim_1515.csv"
BRANCH_DECISION_COPY = BRANCH_RESIDUALS / "epsilon_decision_nonclaim_1515.csv"


def flags() -> dict[str, bool]:
    return {"score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = ["score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "accepted_for_scoring", "passes_for_claim"]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def zero_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "EZ1515_0_target",
            "epsilon_domain_flux = 0",
            "P_loc projection of parent/domain flux vanishes in the observed PPN-safe local coframe",
            "TARGET_RESTATED",
            "definition alone gives no zero or bound",
            source_list("1514_alpha3", "1146_no_flux"),
        ),
        (
            "EZ1515_1_net_flux",
            "stationary conservation / zero surface integral",
            "div F_D = 0 and integral_boundary F_D.n = 0",
            "INSUFFICIENT",
            "coexact circulation or harmonic flux can remain and still source alpha3",
            source_list("1133_derivation", "1133_blockers"),
        ),
        (
            "EZ1515_2_no_swirl",
            "no coexact/circulating local flux",
            "parent derives F_D = -M_D grad zeta_D before readout",
            "MISSING_PARENT_CONSTITUTIVE_LAW",
            "no legal energy identity for the domain flux exists without F_D, M_D, and zeta_D",
            source_list("1134_lemma", "1135_constitutive"),
        ),
        (
            "EZ1515_3_positive_extremum",
            "Neumann positive-mobility extremum",
            "positive elliptic M_D, no-source stationarity, and n.F_D = 0 force zeta_D constant",
            "MATHEMATICALLY_VALID_CONDITIONAL_NOT_PARENT_SIGNED",
            "conditional theorem cannot promote without parent-signed mobility and boundary clauses",
            source_list("1134_contract", "1135_constitutive"),
        ),
        (
            "EZ1515_4_harmonic_topology",
            "harmonic/topological flux exclusion",
            "local H1_rel is trivial or parent branch selector excludes local harmonic class",
            "MISSING_TOPOLOGY_OR_SELECTOR_PROOF",
            "harmonic class can survive conservation and boundary integral tests",
            source_list("1133_blockers", "1134_lemma"),
        ),
        (
            "EZ1515_5_coframe",
            "observed coframe/source normalization",
            "epsilon is zero in the same coframe and normalization used by K_R11*c_R11 alpha3 rows",
            "MISSING_OBSERVABLE_COFRAME_PROOF",
            "representation-zero is not a physical alpha3 zero",
            source_list("1146_no_flux", "1138_c_zero"),
        ),
        (
            "EZ1515_6_FLRW_guard",
            "local zero does not erase cosmology",
            "compact local no-flux theorem is branch-limited and does not impose global all-domain zero",
            "GUARD_TRUE_NONCLAIM",
            "keeps FLRW memory branch alive while local branch remains unclaimed",
            source_list("1514_alpha3", "1134_lemma"),
        ),
        (
            "EZ1515_7_verdict",
            "epsilon zero theorem",
            "EZ1515_1 through EZ1515_6 close from the same parent local branch",
            "THEOREM_NOT_PROVEN_CURRENT_CORPUS",
            "epsilon_domain_flux must stay closure-only or source-bound",
            source_list("1135_demotion", "1147_demotion"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "target": target,
            "needed_statement": needed,
            "current_status": status,
            "consequence": consequence,
            "source_paths": sources,
            **flags(),
        }
        for audit_id, target, needed, status, consequence, sources in rows
    ]


def conditional_contract_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "THM1515_0_strong_conditional",
            "local gradient-flow Neumann no-flux theorem",
            "If F_D=-M_D grad zeta_D, M_D>0 elliptic, div F_D=0, n.F_D=0, H1_rel=0, and observed coframe is fixed independently, then epsilon_domain_flux=0.",
            "Integrate zeta_D div(M_D grad zeta_D)=0 by parts; positivity forces grad zeta_D=0; H1_rel=0 removes harmonic flux; coframe clause prevents gauge hiding.",
            "VALID_CONDITIONAL_NOT_PARENT_SIGNED",
            source_list("1134_contract", "1135_constitutive"),
        ),
        (
            "THM1515_1_existing_parent_upgrade",
            "derive the contract from current MTS parent variables",
            "Find actual parent fields/terms that instantiate F_D, M_D, zeta_D, boundary variation, and coframe normalization.",
            "Would convert the no-flux route from closure to derivation.",
            "NOT_FOUND_IN_CURRENT_CORPUS",
            source_list("1135_constitutive", "1146_no_flux"),
        ),
        (
            "THM1515_2_auxiliary_flux_closure",
            "add an auxiliary flux parent action",
            "S_D_flux with F_i(M_D^{-1})F_j/2 + zeta_D div F can derive F_D=-M_D grad zeta_D.",
            "Mathematically clean but new unless derived from existing structure.",
            "FUTURE_CLOSURE_CONTRACT_ONLY",
            source_list("1135_demotion"),
        ),
        (
            "THM1515_3_numeric_fallback",
            "source or bound epsilon nonzero",
            "Use a real epsilon_abs profile or upper bound with the same normalization as W and K*c alpha3 products.",
            "Turns the theorem problem into a source-backed inequality problem.",
            "NO_REAL_PROFILE_FOUND_CURRENT_CORPUS",
            source_list("1147_acquisition", "1136_pack"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": theorem_id,
            "route": route,
            "statement": statement,
            "proof_or_use": proof,
            "current_status": status,
            "source_paths": sources,
            **flags(),
        }
        for theorem_id, route, statement, proof, status, sources in rows
    ]


def source_rescan_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SRCAN1515_0_latest_profile",
            "1146 epsilon source profile row",
            "MISSING_NUMERIC_EPSILON_ABS; MISSING_SOURCE_PATH",
            "REJECT_AS_SOURCE",
            "template only, not a value or theorem",
            source_list("1146_profile"),
        ),
        (
            "SRCAN1515_1_acquisition_scan",
            "1147 acquisition pass",
            "NO_REAL_EPSILON_DOMAIN_FLUX_PROFILE_FOUND",
            "ACQUISITION_FAILS_CURRENT_CORPUS",
            "all candidates are templates, blockers, wrong-epsilon rows, or unfilled ledgers",
            source_list("1147_acquisition"),
        ),
        (
            "SRCAN1515_2_source_pack",
            "1136 epsilon/W/K/c source pack",
            "epsilon, W, K, c all missing or map-only",
            "SOURCE_PACK_BLOCKED",
            "data contract exists but no claim-valid values exist",
            source_list("1136_pack", "1136_products"),
        ),
        (
            "SRCAN1515_3_coupling_audit",
            "1137 W/K/c audit",
            "W map-only; K contract placeholder; c alias to missing source-normalization",
            "COUPLINGS_BLOCKED",
            "epsilon bound cannot be numerically stated until couplings are sourced or theorem-zero",
            source_list("1137_couplings"),
        ),
        (
            "SRCAN1515_4_verdict",
            "current corpus epsilon source status",
            "no claim-valid epsilon profile, upper bound, or theorem-zero certificate",
            "NO_SOURCE_FOUND",
            "do not continue repeating epsilon source search without new input",
            source_list("1147_demotion", "1514_validation"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "scan_id": scan_id,
            "candidate": candidate,
            "observed_status": status,
            "decision": decision,
            "reason": reason,
            "source_paths": sources,
            **flags(),
        }
        for scan_id, candidate, status, decision, reason, sources in rows
    ]


def product_source_pack_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PSP1515_0_epsilon",
            "epsilon_domain_flux",
            "shared local projected flux factor",
            "MISSING_PROFILE_OR_ZERO_THEOREM",
            "dimensionless observed-coframe projected flux",
            "required by both W*epsilon and K*c*epsilon products",
            source_list("1147_acquisition", "1136_pack"),
        ),
        (
            "PSP1515_1_W",
            "W_domain_alpha3",
            "domain flux to alpha3 weak-field coefficient",
            "MAP_LABEL_ONLY_NOT_NUMERIC_SOURCE",
            "dimensionless alpha3 normalization",
            "needed for abs(W*epsilon)<=4e-20",
            source_list("1137_couplings", "1514_alpha3"),
        ),
        (
            "PSP1515_2_K",
            "K_R11_flux_alpha3",
            "R11 flux-to-alpha3 transfer coefficient",
            "CONTRACT_PLACEHOLDER_NOT_NUMERIC_SOURCE",
            "dimensionless alpha3 transfer",
            "needed for abs(K*c*epsilon)<=4e-20",
            source_list("1122_flux", "1137_couplings"),
        ),
        (
            "PSP1515_3_c",
            "c_R11_flux_alpha3",
            "observed-coframe/source-normalization coefficient",
            "ALIAS_TO_MISSING_R11_SOURCE_NORMALIZATION",
            "dimensionless source-normalization coefficient",
            "ties alpha3 product to measured-GM/Newton source normalization",
            source_list("1137_couplings", "1138_c_zero", "r11_minimum"),
        ),
        (
            "PSP1515_4_Kc_product",
            "K_R11_flux_alpha3*c_R11_flux_alpha3",
            "combined R11 alpha3 coupling product",
            "PRODUCT_SHORTCUT_FORBIDDEN",
            "dimensionless product",
            "allowed only after K and c individually source or theorem-zero",
            source_list("1136_products", "1137_couplings"),
        ),
        (
            "PSP1515_5_domain_product",
            "W_domain_alpha3*epsilon_domain_flux",
            "domain alpha3 product inequality",
            "BLOCKED_MISSING_W_AND_EPSILON",
            "dimensionless alpha3 residual",
            "must satisfy abs(W*epsilon)<=4e-20 independently",
            source_list("1123_alpha3", "1514_alpha3"),
        ),
        (
            "PSP1515_6_R11_product",
            "K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux",
            "R11 alpha3 product inequality",
            "BLOCKED_MISSING_K_c_AND_EPSILON",
            "dimensionless alpha3 residual",
            "must satisfy abs(K*c*epsilon)<=4e-20 independently",
            source_list("1122_flux", "1123_alpha3", "1514_alpha3"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "pack_id": pack_id,
            "quantity": quantity,
            "role": role,
            "current_status": status,
            "units": units,
            "claim_relevance": relevance,
            "source_paths": sources,
            **flags(),
        }
        for pack_id, quantity, role, status, units, relevance, sources in rows
    ]


def pivot_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PIV1515_0_epsilon_continue",
            "continue epsilon source/profile hunt",
            "NO_REAL_SOURCE_FOUND",
            "P2_DEFER",
            "only reopen with new parent theorem or actual epsilon profile source",
            source_list("1147_acquisition", "1147_demotion"),
        ),
        (
            "PIV1515_1_W_domain",
            "derive/source W_domain_alpha3",
            "MAP_LABEL_ONLY",
            "P1_BACKUP",
            "important but narrower than c_R11 for GR/Newton source normalization",
            source_list("1137_couplings"),
        ),
        (
            "PIV1515_2_K_transfer",
            "derive/source K_R11_flux_alpha3",
            "CONTRACT_PLACEHOLDER",
            "P1_BACKUP",
            "still depends on c_R11 and epsilon for the R11 product",
            source_list("1122_flux", "1137_couplings"),
        ),
        (
            "PIV1515_3_c_R11",
            "derive/source c_R11_flux_alpha3 source-normalization operator",
            "ALIAS_TO_MISSING_SOURCE_NORMALIZATION",
            "P0_NEXT",
            "highest overlap with alpha3, measured-GM, Newton source normalization, and local GR reduction",
            source_list("1137_couplings", "1138_c_zero", "r11_minimum", "r11_skeleton"),
        ),
        (
            "PIV1515_4_no_source_slot",
            "common measure/current and no-source-only-slot route",
            "CONDITIONAL_THEOREM_SHAPE_NOT_PARENT_SIGNED",
            "P0_RELATED_PARENT_ROUTE",
            "could structurally kill species/source weights if common measure/current closes",
            source_list("1451_no_slot", "1451_decision"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "pivot_id": pivot_id,
            "candidate_next": candidate,
            "current_state": state,
            "priority": priority,
            "reason": reason,
            "source_paths": sources,
            **flags(),
        }
        for pivot_id, candidate, state, priority, reason, sources in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1515_0_net_flux", "net flux / conservation-only proof", "REJECTED", "zero divergence and zero surface integral do not kill local circulation/harmonic alpha3 vector"),
        ("REJ1515_1_plateau", "epsilon=0 by local plateau axiom", "REJECTED", "would impose the local branch rather than derive it from parent action"),
        ("REJ1515_2_scalar_import", "import scalar no-hair as domain-flux proof", "REJECTED", "scalar profile theorem does not define F_D/M_D/zeta_D or remove coexact flux"),
        ("REJ1515_3_gauge_hide", "set epsilon zero by coframe choice", "REJECTED", "must be zero in observed PPN-safe coframe, not just representation"),
        ("REJ1515_4_product_shortcut", "fill K*c or W*epsilon product directly", "REJECTED", "factors must be individually sourced or parent identity must make the product primitive"),
        ("REJ1515_5_tuned_cancellation", "cancel domain and R11 alpha3 products by sign choice", "REJECTED", "each product must independently close unless a parent identity derives cancellation"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "shortcut": shortcut,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for rejection_id, shortcut, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC1515_0_epsilon_theorem", "epsilon_domain_flux zero theorem", "NOT_PROVEN_KEEP_CLOSURE_ONLY", "missing constitutive law, harmonic/topology exclusion, and observed-coframe proof"),
        ("DEC1515_1_source_profile", "epsilon source/profile acquisition", "NO_REAL_SOURCE_FOUND_CURRENT_CORPUS", "1147 acquisition scan found only templates/blockers/unfilled rows"),
        ("DEC1515_2_product_pack", "alpha3 product source pack", "ACTIVE_NONCLAIM", "epsilon/W/K/c rows remain explicit but not score-ready"),
        ("DEC1515_3_next", "pivot to c_R11 source normalization", "NEXT_1516_C_R11_SOURCE_NORMALIZATION", "best overlap with local GR/Newton measured-GM route and R11 alpha3 product"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in rows
    ]


def local_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("LOCAL1515_0_GR", "derived local GR", "NOT_CLAIMED", "epsilon/domain alpha3 and source-normalization products remain open"),
        ("LOCAL1515_1_Newton", "derived Newtonian source normalization", "NOT_CLAIMED", "c_R11/source-normalization and measured-GM transfer are unresolved"),
        ("LOCAL1515_2_PPN_alpha3", "PPN alpha3 branch", "NOT_CLAIMED", "W*epsilon and K*c*epsilon products are both blocked"),
        ("LOCAL1515_3_R10", "R10/fifth-force branch", "NOT_CLAIMED", "R10 alpha/tau and local source-normalization remain nonclaim"),
        ("LOCAL1515_4_FLRW", "FLRW memory compatibility", "PRESERVED_AS_GUARD_ONLY", "local epsilon theorem is not imposed globally"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": status_id,
            "claim": claim,
            "current_status": status,
            "reason": reason,
            **flags(),
        }
        for status_id, claim, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1515_0_1516",
            "next_target": "1516-Y5-parent-cR11-source-normalization-owner-or-GM-transfer-gate.md",
            "script": "scripts/Y5_parent_cR11_source_normalization_owner_or_GM_transfer_gate.py",
            "objective": "derive or source c_R11_flux_alpha3 / source-normalization as the shared measured-GM/Newton and alpha3 product bottleneck; if not, lock it as an explicit nonclaim bound-input family",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (ZERO_THEOREM_AUDIT, QUAR_ZERO),
        (PRODUCT_SOURCE_PACK, QUAR_PRODUCTS),
        (PIVOT_MATRIX, QUAR_PIVOT),
        (DECISION, QUAR_DECISION),
        (ZERO_THEOREM_AUDIT, BRANCH_ZERO),
        (PRODUCT_SOURCE_PACK, BRANCH_PRODUCTS),
        (PIVOT_MATRIX, BRANCH_PIVOT),
        (DECISION, BRANCH_DECISION_COPY),
    ]
    for source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    modified = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime >= START_TS:
            modified += 1
    return modified


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    zero_rows = read_csv(ZERO_THEOREM_AUDIT)
    source_rows = read_csv(SOURCE_RESCAN)
    product_rows = read_csv(PRODUCT_SOURCE_PACK)
    pivot_data = read_csv(PIVOT_MATRIX)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1515_0_sources", all(path.exists() for path in SOURCE_FILES.values()), "all cited 1515 input source paths exist"),
        (
            "VAL1515_1_zero_not_proven",
            any(row["audit_id"] == "EZ1515_7_verdict" and "NOT_PROVEN" in row["current_status"] for row in zero_rows),
            "epsilon_domain_flux zero theorem remains explicitly unproven",
        ),
        (
            "VAL1515_2_profile_not_found",
            any(row["decision"] == "NO_SOURCE_FOUND" for row in source_rows),
            "source rescan finds no claim-valid epsilon profile",
        ),
        (
            "VAL1515_3_product_pack_blocked",
            any(row["quantity"] == "epsilon_domain_flux" and "MISSING" in row["current_status"] for row in product_rows)
            and any(row["quantity"] == "c_R11_flux_alpha3" and "MISSING" in row["current_status"] for row in product_rows),
            "epsilon/W/K/c product source pack remains explicit and blocked",
        ),
        (
            "VAL1515_4_cR11_selected",
            any(row["pivot_id"] == "PIV1515_3_c_R11" and row["priority"] == "P0_NEXT" for row in pivot_data),
            "c_R11 source-normalization is selected as next high-value target",
        ),
        (
            "VAL1515_5_no_shortcuts",
            any(row["result"] == "ACTIVE_NONCLAIM" for row in decisions),
            "alpha3 product source pack is active but nonclaim",
        ),
        (
            "VAL1515_6_next_target",
            any("cR11-source-normalization" in row["next_target"] for row in next_rows),
            "next target moves to c_R11/source-normalization",
        ),
        ("VAL1515_7_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1515 CSVs parse cleanly"),
        ("VAL1515_8_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        (
            "VAL1515_9_branch_copies",
            all(path.exists() for path in [QUAR_ZERO, QUAR_PRODUCTS, QUAR_PIVOT, QUAR_DECISION, BRANCH_ZERO, BRANCH_PRODUCTS, BRANCH_PIVOT, BRANCH_DECISION_COPY]),
            "branch/quarantine nonclaim copies written",
        ),
        ("VAL1515_10_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1515_11_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"same_parent_branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1515_12_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1515 keeps epsilon closure-only/source-bound, blocks alpha3 product scoring, and pivots to c_R11/source-normalization"
            if overall
            else "1515 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |")
    return "\n".join(output)


def write_doc(
    zero_rows: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    source_rows: list[dict[str, Any]],
    product_rows: list[dict[str, Any]],
    pivots: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    local_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1515 - Parent Epsilon Domain Flux Zero Theorem or Product Source Pack",
                "",
                "## Verdict",
                "- The epsilon_domain_flux zero theorem still does not close: net-flux conservation is too weak, and the parent has not supplied the domain flux constitutive law, harmonic/topology exclusion, or observed-coframe proof.",
                "- No real epsilon source/profile is found in the current corpus; existing epsilon rows are templates, blockers, or unfilled acquisition ledgers.",
                "- The alpha3 product route remains explicit and nonclaim: epsilon, W_domain_alpha3, K_R11_flux_alpha3, and c_R11_flux_alpha3 are all still missing as claim-valid inputs.",
                "- The next best target is c_R11/source-normalization because it touches both the R11 alpha3 product and the local Newton/measured-GM branch.",
                "",
                "## Epsilon Zero Theorem Audit",
                md_table(zero_rows, ["audit_id", "target", "current_status", "consequence"]),
                "",
                "## Conditional Flux Theorem Contract",
                md_table(contracts, ["theorem_id", "route", "current_status", "proof_or_use"]),
                "",
                "## Source Acquisition Rescan",
                md_table(source_rows, ["scan_id", "candidate", "observed_status", "decision"]),
                "",
                "## Product Source Pack",
                md_table(product_rows, ["pack_id", "quantity", "current_status", "claim_relevance"]),
                "",
                "## c_R11 Pivot Matrix",
                md_table(pivots, ["pivot_id", "candidate_next", "current_state", "priority"]),
                "",
                "## Rejection Ledger",
                md_table(rejections, ["rejection_id", "shortcut", "status", "reason"]),
                "",
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "result"]),
                "",
                "## Local GR / Newton Status",
                md_table(local_rows, ["status_id", "claim", "current_status", "reason"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    zero_rows = zero_theorem_rows()
    contracts = conditional_contract_rows()
    source_rows = source_rescan_rows()
    product_rows = product_source_pack_rows()
    pivots = pivot_rows()
    rejections = rejection_rows()
    decisions = decision_rows()
    local_rows = local_status_rows()
    next_rows = next_target_rows()

    write_csv(ZERO_THEOREM_AUDIT, zero_rows)
    write_csv(CONDITIONAL_CONTRACT, contracts)
    write_csv(SOURCE_RESCAN, source_rows)
    write_csv(PRODUCT_SOURCE_PACK, product_rows)
    write_csv(PIVOT_MATRIX, pivots)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(DECISION, decisions)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        ZERO_THEOREM_AUDIT,
        CONDITIONAL_CONTRACT,
        SOURCE_RESCAN,
        PRODUCT_SOURCE_PACK,
        PIVOT_MATRIX,
        REJECTION_LEDGER,
        DECISION,
        LOCAL_STATUS,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(zero_rows, contracts, source_rows, product_rows, pivots, rejections, decisions, local_rows, validation, next_rows)


if __name__ == "__main__":
    main()
