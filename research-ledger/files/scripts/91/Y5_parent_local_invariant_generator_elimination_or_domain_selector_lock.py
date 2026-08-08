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
DOC = ROOT / "1514-Y5-parent-local-invariant-generator-elimination-or-domain-selector-lock.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1513_validation": OUT / "P8_Y5_BRR545_1513_VALIDATION.csv",
    "1513_generators": OUT / "P8_Y5_PARENT_MINIMALITY_1513_LOCAL_INVARIANT_GENERATOR_LOCK.csv",
    "1513_r11": OUT / "P8_Y5_PARENT_MINIMALITY_1513_R11_VECTOR_LOCK.csv",
    "1127_doc": ROOT / "1127-Y5-R10-local-vs-FLRW-branch-selector-no-flux-certificate.md",
    "1127_branch": OUT / "P8_Y5_R10_1127_BRANCH_SELECTOR_AUDIT.csv",
    "1128_doc": ROOT / "1128-Y5-R10-parent-branch-selector-ownership-ND-Qcoh-Pcoh.md",
    "1130_doc": ROOT / "1130-Y5-R10-Pcoh-JD-norm-ownership-or-executable-flux-products.md",
    "1130_ownership": OUT / "P8_Y5_R10_1130_PCOH_JD_NORM_OWNERSHIP_AUDIT.csv",
    "1131_doc": ROOT / "1131-Y5-R10-explicit-JD-Pcoh-parent-object-definitions-or-demote.md",
    "1131_demotion": OUT / "P8_Y5_R10_1131_SELECTOR_DEMOTION_LEDGER.csv",
    "1132_doc": ROOT / "1132-Y5-R10-alpha3-flux-product-source-pack-or-zero-theorem.md",
    "1132_products": OUT / "P8_Y5_R10_1132_EXECUTABLE_PRODUCT_MATRIX.csv",
    "348_doc": ROOT / "348-N5-projector-stress-conservation-theorem.md",
    "472_doc": ROOT / "472-domain-projector-alpha3-no-leak-or-R11-link.md",
    "domain_premises": OUT / "P8_DOMAIN_ALPHA3_PREMISE_OWNERSHIP.csv",
    "domain_novector": OUT / "P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv",
    "domain_r11_link": OUT / "P8_DOMAIN_ALPHA3_R11_LINK.csv",
    "domain_coefficients": OUT / "P8_mu_extra_domain_projector_coefficients.csv",
}

DOMAIN_SELECTOR_AUDIT = OUT / "P8_Y5_PARENT_GENERATOR_1514_DOMAIN_SELECTOR_AUDIT.csv"
BRANCH_SELECTOR_ROUTE = OUT / "P8_Y5_PARENT_GENERATOR_1514_BRANCH_SELECTOR_ROUTE_AUDIT.csv"
PROJECTOR_STRESS_GATE = OUT / "P8_Y5_PARENT_GENERATOR_1514_PROJECTOR_STRESS_GATE.csv"
ALPHA3_FLUX_PRODUCT_LOCK = OUT / "P8_Y5_PARENT_GENERATOR_1514_ALPHA3_FLUX_PRODUCT_LOCK.csv"
R11_DOMAIN_LOCK = OUT / "P8_Y5_PARENT_GENERATOR_1514_R11_DOMAIN_LOCK.csv"
DECISION = OUT / "P8_Y5_PARENT_GENERATOR_1514_DECISION.csv"
LOCAL_STATUS = OUT / "P8_Y5_PARENT_GENERATOR_1514_LOCAL_GR_NEWTON_STATUS.csv"
SCORE_READINESS = OUT / "P8_Y5_PARENT_GENERATOR_1514_SCORE_READINESS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_GENERATOR_1514_REJECTION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_GENERATOR_1514_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1514_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1514"
QUAR_DOMAIN = QUARANTINE / "DOMAIN_SELECTOR_AUDIT_NONCLAIM.csv"
QUAR_BRANCH = QUARANTINE / "BRANCH_SELECTOR_ROUTE_AUDIT_NONCLAIM.csv"
QUAR_ALPHA3 = QUARANTINE / "ALPHA3_FLUX_PRODUCT_LOCK_NONCLAIM.csv"
QUAR_R11 = QUARANTINE / "R11_DOMAIN_LOCK_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "GENERATOR_DECISION_NONCLAIM.csv"
BRANCH_DOMAIN = BRANCH_RESIDUALS / "domain_selector_audit_nonclaim_1514.csv"
BRANCH_ALPHA3 = BRANCH_RESIDUALS / "alpha3_flux_product_lock_nonclaim_1514.csv"
BRANCH_R11 = BRANCH_RESIDUALS / "r11_domain_lock_nonclaim_1514.csv"
BRANCH_DECISION_COPY = BRANCH_RESIDUALS / "generator_decision_nonclaim_1514.csv"


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


def domain_selector_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DS1514_0_target",
            "eliminate chi_D as independent local invariant generator",
            "parent proves chi_D is geometry-derived, pure gauge, constant, topological-silent, or otherwise locally unobservable",
            "FAIL_CURRENT_CORPUS",
            "domain selector remains a live generator from the 1513 lock",
            source_list("1513_generators"),
        ),
        (
            "DS1514_1_geometry_identity",
            "geometry-derived branch scalar",
            "chi_D = F[J^k(e_obs)] with no independent variation and no source-dependent readout",
            "NOT_SIGNED",
            "selector can still act as a local/cosmology branch axiom instead of a derived object",
            source_list("1513_generators", "1127_doc"),
        ),
        (
            "DS1514_2_gauge_representative",
            "pure-gauge selector",
            "delta chi_D is vertical in the parent quotient and has no observable projection",
            "NOT_SIGNED",
            "cannot discard selector force terms as gauge artefacts",
            source_list("1128_doc", "1130_ownership"),
        ),
        (
            "DS1514_3_constant_local_limit",
            "constant local representative",
            "nabla chi_D = 0 and delta chi_D = 0 follow from local field equations, not from a fitted plateau axiom",
            "CONDITIONAL_LOCAL_ONLY_NOT_PARENT_DERIVED",
            "local plateau can be used only as closure language, not a theorem",
            source_list("1127_branch", "domain_novector"),
        ),
        (
            "DS1514_4_topological_no_flux",
            "metric-independent topological projector",
            "parent owns a metric-independent P_D and boundary/local projection flux is silent",
            "CONDITIONAL_THEOREM_NO_PARENT_OWNERSHIP",
            "exact stress-zero route exists only if parent owns this projector class",
            source_list("348_doc", "domain_premises"),
        ),
        (
            "DS1514_5_stationary_scalar",
            "stationary scalar no-vector/no-anisotropy lemma",
            "selector scalar is stationary and its vector, anisotropic, and flux projections vanish",
            "CONDITIONAL_NOT_PARENT_DERIVED",
            "no-vector result cannot be promoted without parent ownership and R11 silence",
            source_list("domain_novector", "472_doc"),
        ),
        (
            "DS1514_6_r11_silence",
            "projector/domain R11 silence",
            "all domain/projector operator families are zeroed or bounded in local experiments",
            "FAIL_ACTIVE_R11_VECTOR",
            "domain selector must be retained as an explicit R11 residual family",
            source_list("1513_r11", "domain_r11_link"),
        ),
        (
            "DS1514_7_verdict",
            "chi_D elimination theorem",
            "all clauses DS1514_1 through DS1514_6 close without closure-only assumptions",
            "THEOREM_NOT_PROVEN_CURRENT_CORPUS",
            "lock domain/projector branch and move to epsilon_domain_flux zero/bound",
            source_list("1513_validation", "1132_products"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "clause": clause,
            "required_parent_signature": required,
            "current_status": status,
            "effect": effect,
            "source_paths": sources,
            **flags(),
        }
        for audit_id, clause, required, status, effect, sources in rows
    ]


def branch_selector_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BS1514_0_shape",
            "local-vs-FLRW branch shape",
            "CONDITIONAL_SHAPE_EXISTS",
            "1127 gives the right conditional split shape: local no-flux and FLRW memory can coexist if the branch selector is parent-owned",
            "not enough for derivation",
            source_list("1127_doc", "1127_branch"),
        ),
        (
            "BS1514_1_ownership",
            "N_D / Q_coh / P_coh parent ownership",
            "NOT_CLOSED",
            "1128 does not close parent ownership of the proposed branch objects",
            "selector cannot be promoted",
            source_list("1128_doc"),
        ),
        (
            "BS1514_2_norm",
            "P_coh J_D norm route",
            "NOT_CLOSED",
            "1130 leaves the actual vertical generator, norm, and parent construction unowned",
            "no exact selector scalar",
            source_list("1130_doc", "1130_ownership"),
        ),
        (
            "BS1514_3_cohomology_norm",
            "I_D = ||P_coh J_D||^2",
            "DEMOTED_TO_CLOSURE_ONLY",
            "1131 demotes the cohomology-norm selector route because explicit parent object definitions are unavailable",
            "do not use as derived branch selector",
            source_list("1131_doc", "1131_demotion"),
        ),
        (
            "BS1514_4_global_zero",
            "global all-domain zero",
            "FORBIDDEN",
            "1127 blocks a global all-domain zero because local and FLRW roles differ",
            "must use local theorem or sourced residual, not erase the domain sector",
            source_list("1127_doc"),
        ),
        (
            "BS1514_5_verdict",
            "branch selector route",
            "LOCK_AS_R11_RESIDUAL",
            "branch-selector ownership is not parent-derived in current corpus",
            "keep local-GR branch conditional and nonclaim",
            source_list("1513_generators", "1131_demotion"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": route_id,
            "route_piece": piece,
            "current_status": status,
            "evidence": evidence,
            "decision": decision,
            "source_paths": sources,
            **flags(),
        }
        for route_id, piece, status, evidence, decision, sources in rows
    ]


def projector_stress_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PS1514_0_exact_conditional",
            "metric-independent topological/relative-chain projector",
            "delta_g P_D = 0 plus no local bulk support",
            "EXACT_CONDITIONAL_THEOREM",
            "bulk projector stress vanishes only for this parent-owned class",
            source_list("348_doc", "domain_premises"),
        ),
        (
            "PS1514_1_parent_ownership",
            "parent ownership of stress-free P_D",
            "P_D is supplied by parent geometry/topology, not by external readout policy or Hodge data",
            "MISSING_PARENT_OWNERSHIP",
            "do not set projector stress to zero",
            source_list("domain_premises", "472_doc"),
        ),
        (
            "PS1514_2_hodge_metric_dependent",
            "Hodge/metric-dependent/projected readout selector",
            "delta_g P_D = 0",
            "FAILS_IF_METRIC_DEPENDENT",
            "stress and variation terms must be retained",
            source_list("348_doc", "domain_premises"),
        ),
        (
            "PS1514_3_boundary_projection",
            "boundary/local projection silence",
            "boundary terms and local projection do not inject bulk force/current",
            "NOT_PARENT_SIGNED",
            "boundary-topological safety remains conditional",
            source_list("1127_doc", "472_doc"),
        ),
        (
            "PS1514_4_verdict",
            "projector stress gate",
            "PS1514_0 is parent-owned and PS1514_1 through PS1514_3 are closed",
            "NO_STRESS_ZERO_CLAIM",
            "projector/domain stress remains active in R11",
            source_list("1513_r11", "domain_r11_link"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "object": object_name,
            "exact_if": exact_if,
            "current_status": status,
            "decision": decision,
            "source_paths": sources,
            **flags(),
        }
        for gate_id, object_name, exact_if, status, decision, sources in rows
    ]


def alpha3_flux_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "A3P1514_0_epsilon",
            "epsilon_domain_flux",
            "epsilon_domain_flux = 0 or numeric local bound",
            "shared_factor",
            "MISSING_ZERO_THEOREM_OR_BOUND",
            "shared bottleneck for domain alpha3 products",
            source_list("1132_doc", "1132_products"),
        ),
        (
            "A3P1514_1_domain_product",
            "W_domain_alpha3 * epsilon_domain_flux",
            "abs(W_domain_alpha3 * epsilon_domain_flux) <= 4e-20",
            "epsilon_domain_flux",
            "ACTIVE_NOT_SCOREABLE",
            "highest-pressure local preferred-frame product remains live",
            source_list("472_doc", "domain_coefficients"),
        ),
        (
            "A3P1514_2_r11_product",
            "K_R11_flux_alpha3 * c_R11_flux_alpha3 * epsilon_domain_flux",
            "abs(K_R11_flux_alpha3 * c_R11_flux_alpha3 * epsilon_domain_flux) <= 4e-20",
            "epsilon_domain_flux",
            "ACTIVE_NOT_SCOREABLE",
            "R11 flux alpha3 branch remains live",
            source_list("1132_doc", "domain_r11_link"),
        ),
        (
            "A3P1514_3_source_normalization",
            "c_domain_source_normalization_operator",
            "zero theorem or executable source-normalization vector",
            "source_normalization_operator",
            "MISSING_OPERATOR_ZERO_OR_BOUND",
            "can mimic local coupling leakage if not controlled",
            source_list("domain_coefficients", "1513_r11"),
        ),
        (
            "A3P1514_4_no_cancellation",
            "sibling product cancellation",
            "do not rely on cancellation between W, K, c, and epsilon factors",
            "all_factors",
            "GUARD_ACTIVE",
            "each product needs its own zero theorem or bound",
            source_list("1132_doc"),
        ),
        (
            "A3P1514_5_verdict",
            "alpha3 flux product lock",
            "epsilon_domain_flux plus W/K/c factors sourced or theorem-zeroed",
            "epsilon_domain_flux",
            "LOCK_PRODUCT_SOURCE_PACK",
            "next target should attack epsilon_domain_flux first",
            source_list("1132_products", "domain_coefficients"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "product_id": product_id,
            "product": product,
            "required_bound_or_zero": required,
            "shared_factor": shared_factor,
            "current_status": status,
            "claim_effect": effect,
            "source_paths": sources,
            **flags(),
        }
        for product_id, product, required, shared_factor, status, effect, sources in rows
    ]


def r11_domain_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "R11D1514_0_R5",
            "R5",
            "source_normalization_operator",
            "ACTIVE_DOMAIN_RESIDUAL",
            "domain/source normalization can leak into effective GM or matter coupling",
            source_list("1513_r11", "domain_coefficients"),
        ),
        (
            "R11D1514_1_R6",
            "R6",
            "boundary_topological_terms",
            "ACTIVE_CONDITIONAL_SAFE_ONLY",
            "safe only after boundary/local projection silence and parent-owned topological projector",
            source_list("1513_r11", "348_doc"),
        ),
        (
            "R11D1514_2_R7",
            "R7",
            "projector_domain_stress",
            "ACTIVE_DOMAIN_RESIDUAL",
            "projector stress cannot be zeroed unless P_D is metric-independent and parent-owned",
            source_list("1513_r11", "domain_r11_link"),
        ),
        (
            "R11D1514_3_R8",
            "R8",
            "vector_preferred_frame_alpha3",
            "ACTIVE_DOMAIN_RESIDUAL",
            "domain flux can source alpha3/preferred-frame leakage",
            source_list("domain_r11_link", "domain_coefficients"),
        ),
        (
            "R11D1514_4_R11",
            "R11",
            "full non-EH local operator vector",
            "ACTIVE_OPERATOR_BRANCH",
            "domain selector is locked into the explicit R11 residual stack",
            source_list("1513_r11", "1513_generators"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "lock_id": lock_id,
            "residual_gate": gate,
            "operator_family": family,
            "lock_status": status,
            "reason": reason,
            "source_paths": sources,
            **flags(),
        }
        for lock_id, gate, family, status, reason, sources in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC1514_0_zero_proof",
            "attempt chi_D geometry/gauge/constant/silent elimination",
            "FAILED_CURRENT_CORPUS",
            "multiple required parent signatures are unsigned",
        ),
        (
            "DEC1514_1_lock",
            "lock domain selector/projector branch as explicit R11 residual",
            "R11_DOMAIN_BRANCH_ACTIVE",
            "do not hide branch-selector assumptions inside the local-GR limit",
        ),
        (
            "DEC1514_2_local_gr",
            "local GR/Newton route",
            "CONDITIONAL_ONLY_NO_CLAIM",
            "EH/Newton recovery remains possible but not derived until domain/R11 leakage is zeroed or bounded",
        ),
        (
            "DEC1514_3_next",
            "attack epsilon_domain_flux first",
            "NEXT_1515_EPSILON_DOMAIN_FLUX",
            "shared bottleneck is cleaner than tuning separate coupling factors",
        ),
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
        ("LOCAL1514_0_GR", "derived local GR", "NOT_CLAIMED", "domain selector/R11 leakage not eliminated"),
        ("LOCAL1514_1_Newton", "derived Newtonian limit", "NOT_CLAIMED", "requires EH operator plus clean source normalization and PPN vector"),
        ("LOCAL1514_2_PPN", "PPN pass", "NOT_CLAIMED", "alpha3/domain flux products remain active and unbounded"),
        ("LOCAL1514_3_R10", "R10/local fifth-force pass", "NOT_CLAIMED", "R10 still lacks parent alpha/tau and full bound curve scoring"),
        ("LOCAL1514_4_cosmology", "FLRW memory split", "CONDITIONAL_COMPATIBLE", "1127 branch shape survives only as conditional closure"),
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


def score_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "score_id": "SCORE1514_0",
            "score_target": "local-GR/Newton/R10/PPN score",
            "score_ready": False,
            "blocking_inputs": "parent-owned chi_D/P_D or numeric epsilon_domain_flux/W/K/c bounds",
            "status": "BLOCKED_NONCLAIM",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1514_0_plateau_axiom", "set chi_D local plateau by assertion", "REJECTED", "would smuggle in the local limit rather than derive it"),
        ("REJ1514_1_global_zero", "set the whole domain sector to zero globally", "REJECTED", "would erase the FLRW/cosmology memory branch as well"),
        ("REJ1514_2_hodge_zero", "treat Hodge/metric projector as stress-free", "REJECTED", "metric-dependent projectors vary with g and can carry stress"),
        ("REJ1514_3_cohomology_norm_claim", "claim I_D = ||P_coh J_D||^2 is derived", "REJECTED", "1131 demoted this to closure-only"),
        ("REJ1514_4_cancellation", "rely on W/K/c/epsilon cancellation", "REJECTED", "local preferred-frame bound must survive without tuned cancellations"),
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


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1514_0_1515",
            "next_target": "1515-Y5-parent-epsilon-domain-flux-zero-theorem-or-product-source-pack.md",
            "script": "scripts/Y5_parent_epsilon_domain_flux_zero_theorem_or_product_source_pack.py",
            "objective": "prove epsilon_domain_flux=0 from parent/local geometry, or emit nonclaim product-source rows for epsilon, W_domain_alpha3, K_R11_flux_alpha3, and c_R11_flux_alpha3",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (DOMAIN_SELECTOR_AUDIT, QUAR_DOMAIN),
        (BRANCH_SELECTOR_ROUTE, QUAR_BRANCH),
        (ALPHA3_FLUX_PRODUCT_LOCK, QUAR_ALPHA3),
        (R11_DOMAIN_LOCK, QUAR_R11),
        (DECISION, QUAR_DECISION),
        (DOMAIN_SELECTOR_AUDIT, BRANCH_DOMAIN),
        (ALPHA3_FLUX_PRODUCT_LOCK, BRANCH_ALPHA3),
        (R11_DOMAIN_LOCK, BRANCH_R11),
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
    domain_rows = read_csv(DOMAIN_SELECTOR_AUDIT)
    branch_rows = read_csv(BRANCH_SELECTOR_ROUTE)
    projector_rows = read_csv(PROJECTOR_STRESS_GATE)
    alpha_rows = read_csv(ALPHA3_FLUX_PRODUCT_LOCK)
    r11_rows = read_csv(R11_DOMAIN_LOCK)
    decision_data = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1514_0_sources", all(path.exists() for path in SOURCE_FILES.values()), "all cited 1514 input source paths exist"),
        (
            "VAL1514_1_domain_not_eliminated",
            any(row["audit_id"] == "DS1514_7_verdict" and "NOT_PROVEN" in row["current_status"] for row in domain_rows),
            "domain selector chi_D is explicitly not eliminated",
        ),
        (
            "VAL1514_2_branch_demoted",
            any(row["current_status"] == "DEMOTED_TO_CLOSURE_ONLY" for row in branch_rows),
            "cohomology-norm branch selector route remains closure-only",
        ),
        (
            "VAL1514_3_projector_conditional",
            any(row["current_status"] == "EXACT_CONDITIONAL_THEOREM" for row in projector_rows)
            and any(row["current_status"] == "MISSING_PARENT_OWNERSHIP" for row in projector_rows),
            "projector stress zero is exact only conditionally and parent ownership is missing",
        ),
        (
            "VAL1514_4_alpha3_epsilon_bound",
            any("epsilon_domain_flux" in row["product"] for row in alpha_rows)
            and any("4e-20" in row["required_bound_or_zero"] for row in alpha_rows),
            "alpha3 product lock keeps epsilon_domain_flux and the 4e-20 pressure bound visible",
        ),
        (
            "VAL1514_5_r11_domain_coverage",
            {"R5", "R6", "R7", "R8", "R11"}.issubset({row["residual_gate"] for row in r11_rows}),
            "R11 domain lock covers R5/R6/R7/R8/R11 gates",
        ),
        (
            "VAL1514_6_decision_lock",
            any(row["result"] == "R11_DOMAIN_BRANCH_ACTIVE" for row in decision_data),
            "decision locks domain selector/projector as active R11 residual branch",
        ),
        (
            "VAL1514_7_next_target",
            any("epsilon-domain-flux" in row["next_target"] for row in next_rows),
            "next target attacks epsilon_domain_flux first",
        ),
        ("VAL1514_8_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1514 CSVs parse cleanly"),
        ("VAL1514_9_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        (
            "VAL1514_10_branch_copies",
            all(path.exists() for path in [QUAR_DOMAIN, QUAR_BRANCH, QUAR_ALPHA3, QUAR_R11, QUAR_DECISION, BRANCH_DOMAIN, BRANCH_ALPHA3, BRANCH_R11, BRANCH_DECISION_COPY]),
            "branch/quarantine nonclaim copies written",
        ),
        ("VAL1514_11_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1514_12_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"same_parent_branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1514_13_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1514 refused domain-selector overclaim, locked the domain/projector branch into R11, and selected epsilon_domain_flux for 1515"
            if overall
            else "1514 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |")
    return "\n".join(output)


def write_doc(
    domain_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    projector_rows: list[dict[str, Any]],
    alpha_rows: list[dict[str, Any]],
    r11_rows: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    local_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1514 - Parent Local Invariant Generator Elimination or Domain Selector Lock",
                "",
                "## Verdict",
                "- The chi_D/domain-selector zero proof does not close in the current corpus: the clean geometry/gauge/constant/topological-silent routes all require parent signatures that are still unsigned.",
                "- The useful exact result survives only conditionally: a parent-owned metric-independent topological projector has zero bulk projector stress, but the parent does not yet own that projector class.",
                "- Therefore the domain/projector branch is locked as an explicit R11 residual family, and local GR/Newton remains conditional rather than claimed.",
                "- The next best derivation target is epsilon_domain_flux, because it is the shared bottleneck in the alpha3 pressure products.",
                "",
                "## Domain Selector Audit",
                md_table(domain_rows, ["audit_id", "clause", "current_status", "effect"]),
                "",
                "## Branch Selector Route Audit",
                md_table(branch_rows, ["route_id", "route_piece", "current_status", "decision"]),
                "",
                "## Projector Stress Gate",
                md_table(projector_rows, ["gate_id", "object", "current_status", "decision"]),
                "",
                "## Alpha3 Flux Product Lock",
                md_table(alpha_rows, ["product_id", "product", "required_bound_or_zero", "current_status"]),
                "",
                "## R11 Domain Lock",
                md_table(r11_rows, ["lock_id", "residual_gate", "operator_family", "lock_status"]),
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
    domain_rows = domain_selector_rows()
    branch_rows = branch_selector_rows()
    projector_rows = projector_stress_rows()
    alpha_rows = alpha3_flux_rows()
    r11_rows = r11_domain_rows()
    decisions = decision_rows()
    local_rows = local_status_rows()
    score = score_rows()
    rejections = rejection_rows()
    next_rows = next_target_rows()

    write_csv(DOMAIN_SELECTOR_AUDIT, domain_rows)
    write_csv(BRANCH_SELECTOR_ROUTE, branch_rows)
    write_csv(PROJECTOR_STRESS_GATE, projector_rows)
    write_csv(ALPHA3_FLUX_PRODUCT_LOCK, alpha_rows)
    write_csv(R11_DOMAIN_LOCK, r11_rows)
    write_csv(DECISION, decisions)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(SCORE_READINESS, score)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        DOMAIN_SELECTOR_AUDIT,
        BRANCH_SELECTOR_ROUTE,
        PROJECTOR_STRESS_GATE,
        ALPHA3_FLUX_PRODUCT_LOCK,
        R11_DOMAIN_LOCK,
        DECISION,
        LOCAL_STATUS,
        SCORE_READINESS,
        REJECTION_LEDGER,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(domain_rows, branch_rows, projector_rows, alpha_rows, r11_rows, decisions, local_rows, validation, next_rows)


if __name__ == "__main__":
    main()
