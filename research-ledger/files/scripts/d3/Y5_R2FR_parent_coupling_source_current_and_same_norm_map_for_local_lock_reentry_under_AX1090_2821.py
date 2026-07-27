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
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2821-Y5-R2FR-parent-coupling-source-current-and-same-norm-map-for-local-lock-reentry-under-AX1090.md"

SRC_2820_NEXT = RESIDUALS / "P8_Y5_R2FR_2820_NEXT_TARGET.csv"
SRC_2820_DECISION = RESIDUALS / "P8_Y5_R2FR_2820_DECISION_LEDGER.csv"
SRC_2820_EXTRACTION = RESIDUALS / "P8_Y5_R2FR_2820_EQ_MU_GAB_EXTRACTION_STATUS.csv"
SRC_2820_REENTRY = RESIDUALS / "P8_Y5_R2FR_2820_LOCAL_LOCK_REENTRY_GATE.csv"
SRC_1549_VARIATION = RESIDUALS / "P8_Y5_PARENT_QLOC_1549_VARIATIONAL_SOURCE_CURRENT_LAW.csv"
SRC_2225_VARIATION = RESIDUALS / "P8_Y5_PARENT_QLOC_2225_VARIATIONAL_SOURCE_CURRENT_GATE.csv"
SRC_2445_JQ = RESIDUALS / "P8_Y5_PARENT_QLOC_2445_JQ_SOURCE_CURRENT_EXTRACTION_ATTEMPT.csv"
SRC_2445_SCHEMA = RESIDUALS / "P8_Y5_PARENT_QLOC_2445_SOURCE_CURRENT_CERTIFICATE_SCHEMA.csv"
SRC_1541_DQVM = RESIDUALS / "P8_Y5_PARENT_QLOC_1541_DQVM_FINITE_COUPLING_ROW_NONCLAIM.csv"
SRC_1670_CHAIN = RESIDUALS / "P8_Y5_PARENT_QLOC_1670_CQM_DQZ_CHAIN_RULE_THEOREM.csv"
SRC_2570_DQ = RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2570_DQ_VERTICAL_GENERATOR_LEDGER.csv"
SRC_2431_ZERO = RESIDUALS / "P8_Y5_PARENT_QLOC_2431_JQ_DESCENT_ZERO_THEOREM.csv"
SRC_2431_BOUND = RESIDUALS / "P8_Y5_PARENT_QLOC_2431_JQ_TO_Q_RESIDUAL_BOUND_LAW.csv"
SRC_2759_PACK = RESIDUALS / "P8_Y5_R2FR_2759_FINITE_JQ_SOURCE_PACK.csv"
SRC_2759_ZERO = RESIDUALS / "P8_Y5_R2FR_2759_JQ_ZERO_THEOREM_TRANSFER.csv"
SRC_2760_COUNTER = RESIDUALS / "P8_Y5_R2FR_2760_COUNTERMODEL_TO_JQ_MAP.csv"
SRC_2760_DECISION = RESIDUALS / "P8_Y5_R2FR_2760_DECISION_LEDGER.csv"
SRC_1088_THEOREM = RESIDUALS / "P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv"
SRC_1088_SIGNATURE = RESIDUALS / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv"
SRC_1090_SYNTHESIS = RESIDUALS / "P8_Y5_R10_1090_SYNTHESIS_ATTEMPT.csv"
SRC_2795_COVERAGE = RESIDUALS / "P8_Y5_R2FR_2795_MOMS_CLAUSE_COVERAGE_MATRIX.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2821_SOURCE_REGISTER.csv",
    "identity": RESIDUALS / "P8_Y5_R2FR_2821_PARENT_COUPLING_IDENTITY_AUDIT.csv",
    "jq_map": RESIDUALS / "P8_Y5_R2FR_2821_JQ_COMPONENT_MAP_FOR_LOCAL_LOCK.csv",
    "same_norm": RESIDUALS / "P8_Y5_R2FR_2821_SAME_NORM_PRODUCT_CONTRACT.csv",
    "dqvm": RESIDUALS / "P8_Y5_R2FR_2821_DQVM_VERTICAL_RESPONSE_STATUS.csv",
    "zero_route": RESIDUALS / "P8_Y5_R2FR_2821_ORDINARY_MATTER_ZERO_ROUTE_AUDIT.csv",
    "reentry": RESIDUALS / "P8_Y5_R2FR_2821_LOCAL_LOCK_REENTRY_DECISION.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2821_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2821_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2821_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2821_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2821_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "source_weight": SOURCE_WEIGHT / "parent_coupling_source_current_2821_NONCLAIM.csv",
    "local_bound": LOCAL_BOUNDS / "same_norm_local_lock_reentry_2821_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2821_FIRST_SAME_NORM_JQ_COMPONENT_BOUND_NEXT.csv",
}

BRANCH_ID = "MTS_R2FR_PARENT_COUPLING_SOURCE_CURRENT_2821"


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def csv_parses(path: Path) -> bool:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    row["generated_utc"] = ts()
    return row


def source_row(source_id: str, path: Path, anchors: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    anchor_list = [anchor for anchor in anchors.split(";") if anchor]
    missing = [anchor for anchor in anchor_list if anchor not in text]
    return nonclaim(
        {
            "source_id": source_id,
            "source_path": str(path),
            "anchors": anchors,
            "role": role,
            "path_exists": path.exists(),
            "anchors_found": not missing,
            "missing_anchors": ";".join(missing),
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2821_0_2820_next", SRC_2820_NEXT, "NEXT2820_0_2821", "2820 handoff into parent coupling/source-current map"),
        ("SRC2821_1_2820_decision", SRC_2820_DECISION, "DEC2820_3_next", "anti-circling decision: attack coupling next"),
        ("SRC2821_2_2820_extraction", SRC_2820_EXTRACTION, "EXT2820_4_Jq;EXT2820_5_Dqvm", "Jq and Dqvm missing inputs"),
        ("SRC2821_3_2820_reentry", SRC_2820_REENTRY, "LLG2820_6_local_reentry", "local-lock reentry blocker"),
        ("SRC2821_4_1549_variation", SRC_1549_VARIATION, "VAR1549_0_variational_definition;VAR1549_5_current_verdict", "conditional variational source-current law"),
        ("SRC2821_5_2225_variation", SRC_2225_VARIATION, "VAR2225_0_definition;VAR2225_4_verdict", "Jq frontier gate"),
        ("SRC2821_6_2445_jq", SRC_2445_JQ, "JQX2445_0_target;JQX2445_5_verdict", "direct Jq extraction attempt"),
        ("SRC2821_7_2445_schema", SRC_2445_SCHEMA, "SCS2445_0_parent_L_term;SCS2445_5_promotion_gate", "source-current certificate schema"),
        ("SRC2821_8_1541_dqvm", SRC_1541_DQVM, "DQC1541_0_C_qm_definition;DQC1541_4_Scg_envelope", "Dqvm finite coupling row"),
        ("SRC2821_9_1670_chain", SRC_1670_CHAIN, "CR1670_2_coframe_derivative;CR1670_4_zero_routes", "conditional chain-rule response law"),
        ("SRC2821_10_2570_dq", SRC_2570_DQ, "DQ2570_3_RAB;DQ2570_7_boundary", "vertical generator obstruction ledger"),
        ("SRC2821_11_2431_zero", SRC_2431_ZERO, "JZT2431_1_descent_lemma;JZT2431_5_total_verdict", "Jq descent zero theorem attempt"),
        ("SRC2821_12_2431_bound", SRC_2431_BOUND, "JQB2431_0_functional_norm;JQB2431_4_verdict", "component no-cancellation bound law"),
        ("SRC2821_13_2759_pack", SRC_2759_PACK, "JQPACK2759_0_total;JQPACK2759_8_same_branch_lock", "R2FR Jq source pack"),
        ("SRC2821_14_2759_zero", SRC_2759_ZERO, "JQZ2759_1_conditional_matter_transfer;JQZ2759_3_current_verdict", "conditional ordinary-matter zero transfer"),
        ("SRC2821_15_2760_counter", SRC_2760_COUNTER, "CM2760_0_alpha;CM2760_5_finite_range", "hidden-visible countermodel map"),
        ("SRC2821_16_2760_decision", SRC_2760_DECISION, "DEC2760_2_coupling_gap;DEC2760_4_next", "coupling gap localized"),
        ("SRC2821_17_1088_theorem", SRC_1088_THEOREM, "THM1088_5_conclusion;THM1088_6_current_corpus_verdict", "conditional MOMS ordinary-matter zero theorem"),
        ("SRC2821_18_1088_signature", SRC_1088_SIGNATURE, "MOMS1088_0_action_form;MOMS1088_7_verdict", "minimal ordinary-matter signature clauses"),
        ("SRC2821_19_1090_synthesis", SRC_1090_SYNTHESIS, "SYN1090_7_zero_theorem_if_axioms;SYN1090_8_verdict", "MOMS synthesis failure"),
        ("SRC2821_20_2795_coverage", SRC_2795_COVERAGE, "MOMS2794_7_all_in_one", "latest MOMS clause coverage status"),
    ]
    return [source_row(*spec) for spec in specs]


def identity_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "CID2821_0_variational_definition",
            "J_q is defined only by parent variation",
            "delta S_matter|_W = int_W dV_e J_A delta q^A + boundary",
            "EXACT_CONDITIONAL_IDENTITY",
            "requires S_matter[q] or q(Phi) before readout/projector reduction",
            SRC_1549_VARIATION,
            "VAR1549_0_variational_definition",
        ),
        (
            "CID2821_1_chain_rule_source",
            "q(Phi) chain rule",
            "delta_Phi S_matter contains J_A Dq^A[delta Phi]",
            "EXACT_CONDITIONAL_IDENTITY",
            "requires parent q map and vertical generator relation",
            SRC_1549_VARIATION,
            "VAR1549_2_chain_rule_from_parent_fields",
        ),
        (
            "CID2821_2_hilbert_proxy_guard",
            "Hilbert stress may source q only through owned projector",
            "J_A = P_A^{mu nu} T_mu_nu only if P_A^{mu nu}=delta g_obs_mu_nu/delta q^A is parent-derived",
            "CONDITIONAL_NOT_OWNED",
            "otherwise importing GR/WEP stress smuggles the coupling",
            SRC_1549_VARIATION,
            "VAR1549_3_Hilbert_proxy_limit",
        ),
        (
            "CID2821_3_no_readout_source",
            "arena residuals cannot define J_q",
            "J_q != fitted GM, alpha(lambda), gamma-1, beta-1, clock drift, or orbital residual",
            "PASS_GUARD_NONCLAIM",
            "source current must precede empirical projection",
            SRC_2225_VARIATION,
            "VAR2225_3_no_readout",
        ),
        (
            "CID2821_4_same_norm_pairing",
            "local-lock forcing term is a same-norm dual product",
            "|<J_q,Dq[v_m]>| <= ||J_q||_{E_q*} ||Dq[v_m]||_{E_q}",
            "EXACT_CONDITIONAL_BOUND",
            "requires one accepted E_q norm shared by source and response",
            SRC_1541_DQVM,
            "DQC1541_1_stress_coupling",
        ),
        (
            "CID2821_5_parent_verdict",
            "parent coupling map",
            "the identity is exact but no parent Lagrangian supplies the q-dependence/projector/norm",
            "NOT_PARENT_EXTRACTED",
            "no 2818 local-lock reentry from coupling yet",
            SRC_2445_JQ,
            "JQX2445_5_verdict",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "identity_id": identity_id,
                "statement": statement,
                "formula": formula,
                "status": status,
                "blocker": blocker,
                "source_path": str(source_path),
                "source_anchor": anchor,
                "anchor_found": anchor in read_text(source_path),
                "conditional_math_valid": status.startswith("EXACT") or status.startswith("PASS"),
                "parent_signed": False,
                "feeds_2818_reentry": False,
            }
        )
        for identity_id, statement, formula, status, blocker, source_path, anchor in specs
    ]


def jq_map_rows() -> list[dict[str, Any]]:
    specs = [
        ("JQM2821_0_total", "j_q_total", "j_matter+j_const+j_weight+j_shadow+j_readout+j_boundary+j_curvature+j_tail", "SYMBOLIC_DECOMPOSITION_ONLY", "every live component needs theorem-zero or source-backed bound", "bookkeeping only"),
        ("JQM2821_1_matter", "j_matter", "ordinary matter vertical source leg", "CONDITIONAL_ZERO_NOT_PROMOTED", "MOMS/AX1090 signature is not parent-signed", "PPN/WEP/clock source silence if derived"),
        ("JQM2821_2_const", "j_const", "alpha/masses/clocks/representation constants", "MISSING_CONSTANT_SUPERSELECTION_OR_VALUE", "fixed constant sector or retained sensitivities missing", "EM, clocks, WEP, particle ratios"),
        ("JQM2821_3_weight", "j_weight", "pre-action source/species weights", "MISSING_PARENT_EXCLUSION_OR_VALUE", "common measure/source-label forgetting theorem missing", "source normalization, WEP, orbital"),
        ("JQM2821_4_shadow", "j_shadow", "conformal/disformal/source-only frame", "MISSING_NO_SHADOW_THEOREM_OR_VALUE", "operator-domain/no-shadow theorem missing", "PPN gamma, WEP, clocks"),
        ("JQM2821_5_readout", "j_readout", "post-variation material/readout/source-worldtube projection", "MISSING_VARIATION_ORDER_OR_VALUE", "variation-before-readout rule not owned by one parent branch", "clock calibration, WEP material basis, orbital source"),
        ("JQM2821_6_boundary", "j_boundary", "compact source boundary/domain support", "MISSING_BOUNDARY_CLASS_OR_VALUE", "body charge/no-flux theorem or explicit bound missing", "finite-range, orbital, local force"),
        ("JQM2821_7_curvature", "j_curvature", "higher-curvature/Weyl2 q-source leg", "MISSING_PARENT_COEFFICIENT_OR_BOUND", "D_q curvature coefficient theorem or bound missing", "R10/local geometry residual"),
        ("JQM2821_8_same_branch_lock", "same_branch_lock", "numerator, denominator, q normalization, and projection share one branch", "REQUIRED_GUARD", "prevents denominator/numerator mixing", "all local-lock and PPN scoring"),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "map_id": map_id,
                "coefficient": coeff,
                "definition": definition,
                "status": status,
                "missing_for_claim": missing,
                "arena_risk": arena,
                "source_path": str(SRC_2759_PACK),
                "source_anchor": coeff if coeff != "same_branch_lock" else "JQPACK2759_8_same_branch_lock",
                "parent_signed": False,
                "numeric_value_present": False,
                "source_backed": False,
            }
        )
        for map_id, coeff, definition, status, missing, arena in specs
    ]


def same_norm_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SN2821_0_Eq",
            "E_q",
            "positive q-sector norm used by both source and response",
            "MISSING_PARENT_NORM",
            "G_AB and mu_q^2 remain unsigned from 2820",
            False,
        ),
        (
            "SN2821_1_Tsource",
            "T_source_norm := ||J_q||_{E_q*}",
            "dual source norm",
            "CONDITIONAL_ONLY",
            "can be defined once E_q and J_q are parent-owned",
            False,
        ),
        (
            "SN2821_2_Cqm",
            "C_qm := ||Dq[v_m]||_{E_q}",
            "same-norm vertical response coefficient",
            "CONDITIONAL_ONLY",
            "Dq[v_m] cannot be measured until q map and E_q exist",
            False,
        ),
        (
            "SN2821_3_product",
            "S_cg <= 1/2 T_source_norm C_qm + S_direct + S_boundary + S_extra",
            "absolute no-cancellation coupling envelope",
            "FORMULA_READY_INPUTS_MISSING",
            "1541 envelope imports cleanly but inputs are missing",
            False,
        ),
        (
            "SN2821_4_no_mixed_norm",
            "same branch and same E_q norm",
            "guard against mixing closure denominator with unrelated numerator",
            "PASS_GUARD_NONCLAIM",
            "all future rows must cite one branch owner",
            False,
        ),
    ]
    return [
        nonclaim(
            {
                "contract_id": contract_id,
                "object": obj,
                "role": role,
                "status": status,
                "blocker": blocker,
                "reentry_allowed": reentry_allowed,
                "source_path": str(SRC_1541_DQVM),
                "source_anchor": "DQC1541_4_Scg_envelope",
            }
        )
        for contract_id, obj, role, status, blocker, reentry_allowed in specs
    ]


def dqvm_rows() -> list[dict[str, Any]]:
    specs = [
        ("DQV2821_0_chain_template", "any v in ker(Dq_parent)", "DObs[v]=DObs_bar(Dq[v])=0 if Obs is q-basic", "EXACT_CONDITIONAL_TEMPLATE", "template supplies no actual q_parent/v/readout functor", SRC_2570_DQ, "DQ2570_0_chain_rule_template"),
        ("DQV2821_1_RAB", "v_R changing R_AB", "current observer-cell map treats R_AB as explicit residual", "REJECTED_FOR_OBSERVER_CELL_MAP", "Dq[v_R] != 0 under current map", SRC_2570_DQ, "DQ2570_3_RAB"),
        ("DQV2821_2_memory_frame", "v_memory/v_tau_private", "may be silent only if public coframe/time functor is insensitive", "UNSIGNED", "preferred-frame and clock residuals remain live", SRC_2570_DQ, "DQ2570_4_memory_frame"),
        ("DQV2821_3_boundary", "boundary/corner/reference variation", "bulk vertical silence does not remove boundary charge", "UNSIGNED", "boundary charge can contaminate local source/readout", SRC_2570_DQ, "DQ2570_7_boundary"),
        ("DQV2821_4_Cqm_status", "Dq[v_m] in E_q", "C_qm requires q/e/Z/local norms in the same branch", "CONDITIONAL_NOT_COMPUTABLE", "normed vertical response remains unavailable", SRC_1670_CHAIN, "CR1670_3_product_bound"),
    ]
    return [
        nonclaim(
            {
                "dqvm_id": dqvm_id,
                "direction": direction,
                "statement": statement,
                "status": status,
                "blocker": blocker,
                "source_path": str(source_path),
                "source_anchor": anchor,
                "anchor_found": anchor in read_text(source_path),
                "parent_signed": False,
                "feeds_2818_reentry": False,
            }
        )
        for dqvm_id, direction, statement, status, blocker, source_path, anchor in specs
    ]


def zero_route_rows() -> list[dict[str, Any]]:
    specs = [
        ("ZRO2821_0_descent_lemma", "If every non-q sector descends through q-blind observed objects, its vertical source current is zero.", "EXACT_CONDITIONAL_THEOREM", "parent observed-object functor and all-field vertical generator still unsigned", SRC_2431_ZERO, "JZT2431_1_descent_lemma"),
        ("ZRO2821_1_moms_transfer", "If full MOMS/AX1090 ordinary-matter signature is parent-signed, j_q^matter=0.", "CONDITIONAL_THEOREM_TRANSFERRED", "MOMS signature clauses are not derived in one parent action", SRC_2759_ZERO, "JQZ2759_1_conditional_matter_transfer"),
        ("ZRO2821_2_moms_signature", "MOMS action form, quotient observables, matter bundle, constants, no weights, variation order, and no-shadow domain.", "MINIMAL_SIGNATURE_NOT_DERIVED", "current files provide a future contract, not a parent derivation", SRC_1088_SIGNATURE, "MOMS1088_7_verdict"),
        ("ZRO2821_3_synthesis_failure", "Composition of existing contracts does not derive MOMS.", "SYNTHESIS_FAILS_MISSING_AXIOMS", "parent action object, matter category, constants, measure/current owner, and operator domain missing", SRC_1090_SYNTHESIS, "SYN1090_8_verdict"),
        ("ZRO2821_4_latest_coverage", "No single source signs all MOMS clauses.", "NO_PARENT_SIGNATURE_SOURCE_FOUND", "must derive parent ordinary-matter action signature or keep finite component bounds", SRC_2795_COVERAGE, "MOMS2794_7_all_in_one"),
        ("ZRO2821_5_countermodels", "Hidden-visible coefficient/readout maps remain legal countermodels.", "COUNTERMODEL_COMPONENTS_LIVE", "alpha, mass, source weight, shadow, readout, and finite-range channels remain live", SRC_2760_COUNTER, "CM2760_0_alpha"),
    ]
    return [
        nonclaim(
            {
                "zero_route_id": route_id,
                "statement": statement,
                "status": status,
                "blocker": blocker,
                "source_path": str(source_path),
                "source_anchor": anchor,
                "anchor_found": anchor in read_text(source_path),
                "theorem_zero_adopted": False,
                "ordinary_matter_zero_claimed": False,
            }
        )
        for route_id, statement, status, blocker, source_path, anchor in specs
    ]


def reentry_rows() -> list[dict[str, Any]]:
    specs = [
        ("RE2821_0_identity", "parent coupling identity", "AVAILABLE_CONDITIONAL", "chain-rule/source-current law is exact if parent slots exist", True, False),
        ("RE2821_1_Jq", "J_q", "NOT_PARENT_EXTRACTED", "full source-current map is component-decomposed but unsourced", False, False),
        ("RE2821_2_Dqvm", "Dq[v_m]", "NOT_COMPUTABLE_IN_EQ", "q map and E_q norm are absent", False, False),
        ("RE2821_3_Eq", "E_q", "MISSING_PARENT_NORM", "G_AB/mu_q not parent-derived", False, False),
        ("RE2821_4_ordinary_zero", "ordinary matter zero route", "CONDITIONAL_ONLY", "MOMS/AX1090 signature not parent-signed", True, False),
        ("RE2821_5_component_bounds", "finite J_q component bounds", "SCHEMA_READY_VALUES_MISSING", "no source-backed component rows yet", True, False),
        ("RE2821_6_local_lock", "2818 local-lock reentry", "REFUSED", "same-norm J_q and Dq[v_m] are not supplied", False, False),
        ("RE2821_7_claims", "local GR/Newton/PPN/R10 claims", "BLOCKED_NO_CLAIM", "closure/coupling remains nonclaim", False, False),
    ]
    return [
        nonclaim(
            {
                "reentry_id": reentry_id,
                "object": obj,
                "status": status,
                "reason": reason,
                "conditional_piece_available": conditional,
                "reentry_allowed": allowed,
                "source_path": str(SRC_2820_REENTRY),
            }
        )
        for reentry_id, obj, status, reason, conditional, allowed in specs
    ]


def gate_rows(rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["anchors_found"] for row in rows["sources"])
    parent_coupling = any(row["parent_signed"] for row in rows["identity"])
    jq_extracted = any(row["coefficient"] == "j_q_total" and row["source_backed"] for row in rows["jq_map"])
    dqvm_extracted = any(row["feeds_2818_reentry"] for row in rows["dqvm"])
    ordinary_zero = any(row["ordinary_matter_zero_claimed"] for row in rows["zero_route"])
    reentry = any(row["reentry_allowed"] for row in rows["reentry"])
    specs = [
        ("CG2821_0_sources", "source anchors present", sources_ok, "all imported coupling ledgers are reproducible"),
        ("CG2821_1_identity", "conditional coupling identity stated", True, "exact chain-rule law is now explicit"),
        ("CG2821_2_parent_coupling", "parent coupling map signed", parent_coupling, "no parent Lagrangian q-dependence/projector/norm supplied"),
        ("CG2821_3_Jq", "J_q extracted or theorem-zero", jq_extracted or ordinary_zero, "component map exists but no promoted zero or source-backed value"),
        ("CG2821_4_Dqvm", "Dq[v_m] extracted in E_q", dqvm_extracted, "no accepted q map/E_q norm"),
        ("CG2821_5_same_norm_product", "same-norm product can feed N_lock", reentry, "T_source_norm*C_qm remains conditional"),
        ("CG2821_6_local_claim", "local GR/Newton/PPN/R10 claim", False, "no sourced local branch exists"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "gate_passed": passed,
                "status": "PASS_NONCLAIM" if passed else "BLOCKED",
                "reason": reason,
            }
        )
        for gate_id, claim, passed, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2821_0_result", "The coupling identity is derived conditionally, not parent-signed.", "CONDITIONAL_IDENTITY_ONLY", "J_q is only legal as a variational source current before readout; no parent Lagrangian supplies it", "do not reopen local-lock reentry"),
        ("DEC2821_1_component_map", "Keep the finite J_q component map as the live bookkeeping object.", "COMPONENT_VECTOR_REQUIRED", "hidden-visible countermodels remain legal until theorem-zero or bounds close them", "source or zero each component independently"),
        ("DEC2821_2_no_smuggling", "Reject Hilbert-stress/readout shortcuts.", "GUARD_ACTIVE", "using T_mu_nu or arena residuals without an owned projector would import GR/fitting into the coupling", "require a parent projector or finite source row"),
        ("DEC2821_3_next", "Next target is first same-norm J_q component bound/zero row.", "NEXT_2822_COMPONENT_BOUND", "one concrete component row advances testing more than repeating the full functor contract", "try ordinary-matter zero certificate first; otherwise produce finite component bound rows"),
    ]
    return [
        nonclaim(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, result, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2821_0_2822",
                "status": "selected_primary",
                "target_doc": "2822-Y5-R2FR-first-same-norm-Jq-component-bound-or-zero-row-for-local-lock-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_first_same_norm_Jq_component_bound_or_zero_row_for_local_lock_under_AX1090_2822.py",
                "mission": "attempt the first concrete same-norm J_q component closure: prove the ordinary-matter zero row from a parent MOMS/AX1090 signature, or produce finite nonclaim component-bound rows for j_const, j_weight, j_shadow, j_readout, j_boundary, and j_curvature",
                "acceptance": "write one branch-locked component row with source path, units/normalization, q/E_q branch, theorem-zero premises or numeric bound placeholder, and valid_for_claim=false unless fully sourced",
                "forbidden": "do not set coefficients to zero by taste; do not use arena residuals as source currents; do not mix norms/branches; do not claim local GR/Newton/PPN/R10; do not edit formalization-workbench",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("BR2821_0_source_weight", OUTPUTS["jq_map"], BRANCH_OUTPUTS["source_weight"], "source-weight copy of Jq component map"),
        ("BR2821_1_local_bound", OUTPUTS["same_norm"], BRANCH_OUTPUTS["local_bound"], "local-bound copy of same-norm product contract"),
        ("BR2821_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue for first same-norm Jq component bound"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_table, copy_path, purpose in specs:
        copy_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_table, copy_path)
        rows.append(
            nonclaim(
                {
                    "copy_id": copy_id,
                    "source_table": str(source_table),
                    "copy_path": str(copy_path),
                    "purpose": purpose,
                    "exists": copy_path.exists(),
                }
            )
        )
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "source_paths", "source_table", "copy_path"}
    paths: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in keys:
                value = row.get(key)
                if value is None:
                    continue
                for token in str(value).split(";"):
                    item = token.strip()
                    if not item or item.startswith("http"):
                        continue
                    path = Path(item)
                    if not path.is_absolute():
                        path = ROOT / item
                    paths.append(path)
    return paths


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name == "validation":
            continue
        for row in rows:
            for key in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if str(row.get(key, "")).lower() == "true":
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            try:
                if path.stat().st_mtime >= start:
                    return False
            except OSError:
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2821_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2821_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2821_2_identity_conditional", any(row["identity_id"] == "CID2821_4_same_norm_pairing" and row["conditional_math_valid"] for row in rows_by_name["identity"]), "same-norm source/response identity is conditionally valid"),
        ("VAL2821_3_no_parent_coupling", not any(row["parent_signed"] for row in rows_by_name["identity"]), "no parent coupling map was accepted"),
        ("VAL2821_4_jq_components_nonclaim", not any(row["source_backed"] for row in rows_by_name["jq_map"]), "Jq components remain unsourced/nonclaim"),
        ("VAL2821_5_zero_not_adopted", not any(row["ordinary_matter_zero_claimed"] for row in rows_by_name["zero_route"]), "ordinary-matter zero theorem not promoted"),
        ("VAL2821_6_reentry_blocked", not any(row["reentry_allowed"] for row in rows_by_name["reentry"]), "local-lock reentry remains blocked"),
        ("VAL2821_7_next_target_2822", any(row["next_id"] == "NEXT2821_0_2822" and row["selected"] for row in rows_by_name["next"]), "first same-norm Jq component bound selected next"),
        ("VAL2821_8_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2821_9_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2821_10_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2821_11_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2821_12_no_claim_flags", no_claim_flags(rows_by_name), "no score_ready, valid_prediction_row, valid_for_claim, or claim_allowed flag is true"),
        ("VAL2821_13_generated_under_post_checkpoint", all(str(path).startswith(str(ROOT)) for path in output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2821_14_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2821_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": ts(),
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2821_OVERALL",
            "passed": overall,
            "detail": "2821 derives the conditional coupling/source-current identity, refuses parent promotion because J_q, Dq[v_m], and E_q remain unsigned, and selects a first same-norm Jq component bound/zero row next.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2821 - Y5 R2FR Parent Coupling Source Current And Same Norm Map For Local Lock Reentry Under AX1090

Status: `Y5_R2FR_2821_conditional_coupling_identity_derived_parent_coupling_not_signed_component_bound_next`

## Private Verdict

2821 makes real progress, but not the kind that allows a claim yet.

The coupling law itself is now clean: `J_q` is the variational source current dual to `q`, and the local-lock forcing term is controlled by the same-norm product `|<J_q,Dq[v_m]>| <= ||J_q||_E* ||Dq[v_m]||_E`. That is an honest mathematical identity, not a fit.

The problem is parent ownership. The corpus still does not supply a single parent matter/readout action with owned `q` dependence, an owned Hilbert-to-q projector, an accepted `E_q` norm, or a computable `Dq[v_m]`. Ordinary matter can be zero only under the MOMS/AX1090 signature, but that signature is still a contract rather than a derived action.

So the branch does not reenter 2818 scoring. The productive next move is component-level: prove or bound one `J_q` source component in the same branch/norm, starting with the ordinary-matter zero row and falling back to finite nonclaim component bounds.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Parent Coupling Identity Audit

{markdown_table(rows["identity"], ["identity_id", "statement", "status", "blocker", "conditional_math_valid", "parent_signed", "feeds_2818_reentry", "valid_for_claim"])}

## Jq Component Map For Local Lock

{markdown_table(rows["jq_map"], ["map_id", "coefficient", "status", "missing_for_claim", "arena_risk", "source_backed", "valid_for_claim"])}

## Same Norm Product Contract

{markdown_table(rows["same_norm"], ["contract_id", "object", "status", "blocker", "reentry_allowed", "valid_for_claim"])}

## Dqvm Vertical Response Status

{markdown_table(rows["dqvm"], ["dqvm_id", "direction", "status", "blocker", "parent_signed", "feeds_2818_reentry", "valid_for_claim"])}

## Ordinary Matter Zero Route

{markdown_table(rows["zero_route"], ["zero_route_id", "statement", "status", "blocker", "theorem_zero_adopted", "ordinary_matter_zero_claimed", "valid_for_claim"])}

## Local Lock Reentry Decision

{markdown_table(rows["reentry"], ["reentry_id", "object", "status", "reason", "conditional_piece_available", "reentry_allowed", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows["gates"], ["claim_gate_id", "claim", "gate_passed", "status", "reason", "claim_allowed"])}

## Decision Ledger

{markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "next_action", "valid_for_claim"])}

## Next Target

{markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_rows()
    rows["identity"] = identity_rows()
    rows["jq_map"] = jq_map_rows()
    rows["same_norm"] = same_norm_rows()
    rows["dqvm"] = dqvm_rows()
    rows["zero_route"] = zero_route_rows()
    rows["reentry"] = reentry_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "identity", "jq_map", "same_norm", "dqvm", "zero_route", "reentry", "gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])

    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2821_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2821_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
