from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2759-Y5-R2FR-jq-source-leg-zero-theorem-or-finite-source-pack-under-AX1090.md"
BRANCH_ID = "MTS_R2FR_AX1090_JQ_SOURCE_LEG_2759"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2759_SOURCE_REGISTER.csv",
    "zero": RESIDUALS / "P8_Y5_R2FR_2759_JQ_ZERO_THEOREM_TRANSFER.csv",
    "signature": RESIDUALS / "P8_Y5_R2FR_2759_MATTER_SIGNATURE_CLAUSE_STATUS.csv",
    "countermodels": RESIDUALS / "P8_Y5_R2FR_2759_COUNTERMODEL_TO_JQ_MAP.csv",
    "pack": RESIDUALS / "P8_Y5_R2FR_2759_FINITE_JQ_SOURCE_PACK.csv",
    "arena": RESIDUALS / "P8_Y5_R2FR_2759_QR_ZERO_AND_ARENA_IMPACT.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2759_DECISION_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2759_CLAIM_GATES.csv",
    "refusal": RESIDUALS / "P8_Y5_R2FR_2759_REFUSAL_RUNNER_NONCLAIM.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2759_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2759_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2759_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "zero_queue": QUEUE / "JR2759_JQ_ZERO_THEOREM_TRANSFER_NONCLAIM.csv",
    "pack_queue": QUEUE / "JR2759_FINITE_JQ_SOURCE_PACK_NONCLAIM.csv",
    "arena_beta": BETA_DOCS / "Q_JQ_SOURCE_LEG_ARENA_IMPACT_2759_NONCLAIM.csv",
    "arena_local": LOCAL_BOUNDS / "jq_source_leg_arena_impact_2759_NONCLAIM.csv",
    "next_queue": QUEUE / "JR2759_NO_HIDDEN_VISIBLE_HOM_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()}:
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    body = ["| " + " | ".join(md(row.get(col, "")) for col in cols) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def local_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["numeric_value_present"] = False
    row["source_backed"] = False
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    return row


def source_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC2759_0_2758_doc",
            "description": "AX1090 Green-domain checkpoint selecting j_q numerator next.",
            "source_path": "2758-Y5-R2FR-q-zero-selector-source-current-or-Green-domain-second-fill-under-AX1090.md",
            "required_needles": "NEXT2758_0_2759;FORM2758_2_qR;VAL2758_OVERALL",
        },
        {
            "source_id": "SRC2759_1_2758_validation",
            "description": "2758 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2758_VALIDATION.csv",
            "required_needles": "VAL2758_OVERALL;True",
        },
        {
            "source_id": "SRC2759_2_2316_doc",
            "description": "prior j_q source-leg zero theorem and finite source pack.",
            "source_path": "2316-Y5-R2FR-jq-source-leg-zero-theorem-or-finite-source-pack.md",
            "required_needles": "JQZ2316_0_definition;JQZ2316_1_conditional_transfer;JQPACK2316_0_total;VAL2316_OVERALL",
        },
        {
            "source_id": "SRC2759_3_2316_validation",
            "description": "2316 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2316_VALIDATION.csv",
            "required_needles": "VAL2316_OVERALL;PASS",
        },
        {
            "source_id": "SRC2759_4_2317_doc",
            "description": "hidden-visible coupling theorem and finite prior interface precedent.",
            "source_path": "2317-Y5-R2FR-no-hidden-visible-hom-jq-zero-or-finite-coefficient-prior.md",
            "required_needles": "NHVH2317_5_verdict;FCP2317_0_b_alpha;VAL2317_OVERALL",
        },
        {
            "source_id": "SRC2759_5_2317_validation",
            "description": "2317 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2317_VALIDATION.csv",
            "required_needles": "VAL2317_OVERALL;PASS",
        },
        {
            "source_id": "SRC2759_6_1088_conditional",
            "description": "conditional ordinary-matter zero theorem.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv",
            "required_needles": "THM1088_5_conclusion",
        },
        {
            "source_id": "SRC2759_7_1090_axioms",
            "description": "missing axiom ledger blocking promotion.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv",
            "required_needles": "AX1090",
        },
    ]
    for row in rows:
        path = local_path(row["source_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        needles = [needle for needle in row["required_needles"].split(";") if needle]
        missing = [needle for needle in needles if needle not in text]
        row["exists"] = path.exists()
        row["needles_present"] = len(missing) == 0
        row["missing_needles"] = ";".join(missing)
        nonclaim(row)
    return rows


def zero_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "JQZ2759_0_definition",
            "Define j_q as the weak-field source-leg numerator in the current q branch.",
            "delta_q S_source = int sqrt(g) j_q L q + O(L^2 q,q^2); q_R=j_q/(n_q^A H_AB n_q^B)",
            "2758 FORM2758_2_qR plus 2316 JQZ2316_0",
            "DEFINITION_IMPORTED_AND_BRANCH_LOCKED",
            "sets the numerator target; does not prove the numerator vanishes",
        ),
        (
            "JQZ2759_1_conditional_matter_transfer",
            "If the full MOMS/AX1090 ordinary-matter signature is parent-signed, then j_q^matter=0.",
            "MOMS signed => delta_v S_matter=0 for v_q in ker(Dq) => j_q^matter=0",
            "1088 conditional theorem and 2316 transfer",
            "CONDITIONAL_THEOREM_TRANSFERRED",
            "strong route to matter-source silence under unsigned premises",
        ),
        (
            "JQZ2759_2_qR_consequence",
            "If M_q^2>0 and same-branch matter numerator is zero, the matter part of q_R vanishes.",
            "M_q^2=n_q^A H_AB n_q^B>0 and j_q^matter=0 => q_R^matter=0",
            "2757/2758 denominator and 1088/2316 numerator theorem",
            "CONDITIONAL_ALGEBRAIC_CONSEQUENCE",
            "removes ordinary-matter q residual leg only, not boundary/curvature/hidden/readout legs",
        ),
        (
            "JQZ2759_3_current_verdict",
            "Current corpus does not promote j_q^matter=0 to a claim.",
            "1089/1090/2316 keep MOMS/AX1090 premises unsigned; finite source pack stays live",
            "2316;2317;1090",
            "ZERO_THEOREM_NOT_PROMOTED",
            "local GR/Newton and R10/PPN scoring remain blocked",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "zero_id": row_id,
                "statement": statement,
                "formula": formula,
                "source_basis": basis,
                "status": status,
                "claim_effect": effect,
            }
        )
        for row_id, statement, formula, basis, status, effect in specs
    ]


def signature_rows() -> list[dict[str, Any]]:
    specs = [
        ("SIG2759_0_action_form", "single ordinary-matter parent action descends through observed quotient variables", "CONDITIONAL_CLAUSE_WRITTEN_NOT_PARENT_DERIVED", "common owner for ordinary matter before readout/fitting", "one source action object is schema/contract, not derived"),
        ("SIG2759_1_quotient_pullback", "v_q in ker(Dq) makes observed coframe/metric/gauge data silent by chain rule", "EXACT_CONDITIONAL_LEMMA", "prevents visible geometry variation from producing j_q", "q, observed coframe, and matter bundle not parent-selected in one action"),
        ("SIG2759_2_constants", "masses, charges, alpha_EM, clocks, and labels are q-trivial or explicit residual fields", "CONSTANT_SUPERSELECTION_UNSIGNED", "kills direct constant-sector contributions to j_q", "hidden-visible coefficient functions remain legal without operator-domain theorem"),
        ("SIG2759_3_no_species_weights", "no independent w_A(q) S_A source weights before variation", "PRE_ACTION_WEIGHT_EXCLUSION_UNSIGNED", "prevents weighted source numerator", "common quantum/action measure owner missing"),
        ("SIG2759_4_variation_order", "variation is taken before empirical readout, material projection, and source-worldtube fitting", "CONDITIONAL_SUBTHEOREM_ONLY", "blocks post-variation creation/erasure of j_q", "detector/readout model not derived from parent action"),
        ("SIG2759_5_no_shadow_domain", "no conformal/disformal/source-only frame, support marker, boundary charge, or hidden-visible coefficient map", "NO_SHADOW_DOMAIN_UNSIGNED", "closes largest surviving direct coupling route into j_q", "no-hidden-visible-hom/operator-domain theorem is not derived"),
        ("SIG2759_6_verdict", "all MOMS/AX1090 clauses are parent-signed together", "MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED", "would promote conditional j_q^matter=0", "1090/2316/2317 show missing axioms and live countermodels"),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "signature_id": row_id,
                "parent_clause": clause,
                "evidence_status": status,
                "needed_for_jq_zero": needed,
                "current_gap": gap,
                "parent_signed": False,
            }
        )
        for row_id, clause, status, needed, gap in specs
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    specs = [
        ("CMJ2759_0_species_weight", "pre-action species/source weights", "j_weight = sum_A (partial_q w_A) T_A", "visible metric can descend while source strength is species/material dependent", "common action measure theorem", "LIVE_FINITE_NUMERATOR_CHANNEL"),
        ("CMJ2759_1_variable_constants", "alpha_EM, masses, clock standards, or material constants vary with hidden/representative variables", "j_const = sum_a (partial_q theta_a)(partial L_matter/partial theta_a)", "WEP, clocks, R10, EM rows can receive composition-dependent coupling", "constant superselection plus no-hidden-visible-hom", "LIVE_FINITE_NUMERATOR_CHANNEL"),
        ("CMJ2759_2_shadow_frame", "conformal/disformal/source-only matter frame", "j_shadow from partial_q A_A, partial_q B_A, or source-only metric coefficients", "fifth-force residual hides outside observed coframe chain rule", "no-shadow/domain plus target exclusion", "LIVE_FINITE_NUMERATOR_CHANNEL"),
        ("CMJ2759_3_post_variation_readout", "readout/material projection after variation changes source normalization", "j_readout from source-worldtube, calibration, or material-selector dependence", "source current can be manufactured by readout rather than parent dynamics", "variation-before-readout theorem", "LIVE_FINITE_NUMERATOR_CHANNEL"),
        ("CMJ2759_4_boundary_domain", "support/domain marker, boundary charge, or local source profile shifts under v_q", "j_boundary or Q_R hair not killed by bulk matter descent", "bulk zero can coexist with finite local/compact-source residuals", "parent boundary class/no-flux/no-charge theorem", "LIVE_FINITE_NUMERATOR_CHANNEL"),
        ("CMJ2759_5_hidden_visible_hom", "hidden/representative variables hom into visible coefficients", "j_hom from f_X F^2, m_A(X), A_A(X), detector coefficients", "coupling survives coframe descent unless coefficient domain is closed", "AX1090 no-hidden-visible-hom/operator-domain theorem", "BEST_NEXT_DERIVATION_TARGET"),
        ("CMJ2759_6_curvature_tail", "Weyl/higher-curvature source coupling", "j_curvature or D_qWeyl2 C^2 enters source_q", "local vacuum/background curvature can source q even if ordinary matter leg vanishes", "higher-curvature no-tower theorem or coefficient bound", "LIVE_FINITE_NUMERATOR_CHANNEL"),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "countermodel_id": row_id,
                "surviving_channel": channel,
                "jq_map": jq_map,
                "damage_if_live": damage,
                "killed_by": killed_by,
                "current_status": status,
            }
        )
        for row_id, channel, jq_map, damage, killed_by, status in specs
    ]


def pack_rows() -> list[dict[str, Any]]:
    specs = [
        ("JQPACK2759_0_total", "j_q_total", "j_q = j_matter + j_const + j_weight + j_shadow + j_readout + j_boundary + j_curvature + j_tail", "q Euler-source / weak-field L coefficient; branch-normalization dependent", "SYMBOLIC_DECOMPOSITION_ONLY", "parent action, source normalization, units, coefficient values, and source paths for every nonzero term", "bookkeeping only"),
        ("JQPACK2759_1_matter", "j_matter", "ordinary-matter vertical source leg; zero under full MOMS/AX1090 signature", "same as j_q_total", "CONDITIONAL_ZERO_NOT_PROMOTED", "MOMS/AX1090 parent signature", "PPN/WEP/clock source silence if derived"),
        ("JQPACK2759_2_weight", "j_weight", "pre-action source/species weighting contribution", "partial_q w_A times Hilbert/source density", "MISSING_PARENT_EXCLUSION_OR_VALUE", "common action measure theorem or source-backed bound", "WEP/source normalization"),
        ("JQPACK2759_3_const", "j_const", "constant-sector derivative contribution from alpha_EM, masses, clocks, representation labels", "sum_a partial_q theta_a partial L_matter/partial theta_a", "MISSING_CONSTANT_SUPERSELECTION_OR_VALUE", "fixed constant sector or sourced sensitivities", "EM, clocks, WEP, particle/constant tests"),
        ("JQPACK2759_4_shadow", "j_shadow", "conformal/disformal/source-only frame contribution", "partial_q frame coefficient times matter stress/source density", "MISSING_NO_SHADOW_THEOREM_OR_VALUE", "no-hidden-visible-hom/operator-domain theorem", "PPN gamma, WEP, clocks, local force"),
        ("JQPACK2759_5_readout", "j_readout", "post-variation material/readout/source-worldtube projection contribution", "normalization dependent; same branch as nHn denominator", "MISSING_VARIATION_DOMAIN_ORDER_OR_VALUE", "variation-before-readout theorem and detector/source model", "source normalization, PPN, orbital"),
        ("JQPACK2759_6_boundary", "j_boundary", "compact-source boundary/domain support contribution, including Q_R hair", "boundary flux or effective source charge", "MISSING_BOUNDARY_CLASS_OR_VALUE", "no-flux/no-charge theorem or explicit bound", "PPN local force, orbital, finite-range residual"),
        ("JQPACK2759_7_curvature", "j_curvature", "higher-curvature/Weyl2 or D_q Weyl source coupling contribution", "curvature-source normalization dependent", "MISSING_PARENT_COEFFICIENT_OR_BOUND", "D_qWeyl2 coefficient theorem or sourced bound", "R10/local geometry residual"),
        ("JQPACK2759_8_same_branch_lock", "same_branch_lock", "denominator nHn, numerator j_* terms, q normalization, and P_obs projection must be from same parent branch", "guard condition", "REQUIRED_GUARD", "branch-locked parent action/source-normalization proof", "prevents mixing closure denominator with unrelated source numerator"),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "pack_id": row_id,
                "coefficient": coeff,
                "definition": definition,
                "units_or_normalization": units,
                "source_status": status,
                "missing_for_claim": missing,
                "arena_use": arena,
            }
        )
        for row_id, coeff, definition, units, status, missing, arena in specs
    ]


def arena_rows() -> list[dict[str, Any]]:
    specs = [
        ("ARENA2759_0_PPN_gamma", "PPN gamma/light/Shapiro", "gamma-1 = q_R + ... = j_q/(n_q H n_q) + retained q_loc/source terms", "ordinary-matter q_R leg drops out if MOMS/AX1090 and same-branch denominator are signed", "MOMS unsigned; boundary/source normalization/q_loc channels remain"),
        ("ARENA2759_1_R10", "R10 short-range alpha(lambda)", "alpha_q(lambda_q=xi_q) depends on K_q, Qbar_qH, qbar_qT, and finite j_q source pack", "ordinary-matter source leg may vanish; curvature/boundary/hidden coupling legs still need coefficients", "xi_q numeric/source, K_q/Qbar/qbar couplings, real bound curve, and j_q coefficient ownership"),
        ("ARENA2759_2_clocks_WEP", "clocks/WEP/composition", "eta or clock residual receives j_const, j_weight, j_shadow, and j_readout unless MOMS/AX1090 closes them", "MOMS would kill ordinary matter composition source channels in the q leg", "constant superselection, no-species-weight, no-shadow, readout-order clauses unsigned"),
        ("ARENA2759_3_orbital_Newton", "Newton/orbital/source normalization", "local orbital residual must carry q_R plus delta_beta and observed-GM/source-normalization terms", "only one q_R numerator leg is removed if j_matter=0", "Newtonian source charge theorem, beta completion, boundary domain ownership"),
        ("ARENA2759_4_local_GR", "derived local GR/Newton limit", "local residual vector = {j_q/(nHn), q_loc, Q_R/boundary, delta_beta, delta_GM, curvature tail, hidden-visible hom terms}", "residual vector is shorter and cleaner, not empty", "MOMS not signed and non-j_q residual vector not zeroed or bounded"),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "arena_id": row_id,
                "arena": arena,
                "updated_formula": formula,
                "if_jq_zero": if_zero,
                "still_blocked_by": blocked,
                "score_ready": False,
            }
        )
        for row_id, arena, formula, if_zero, blocked in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2759_0_definition", "j_q branch definition imported", "Q_R_NUMERATOR_LOCKED_TO_JQ_OVER_NHN", "q_R now has a clean numerator/denominator split"),
        ("DEC2759_1_conditional_zero", "ordinary matter source zero", "CONDITIONAL_ONLY_NOT_PROMOTED", "MOMS/AX1090 signature would kill j_matter but remains unsigned"),
        ("DEC2759_2_finite_pack", "finite source pack", "LIVE_AND_REQUIRED", "all hidden/visible coupling channels must be theorem-zero or source-backed before scoring"),
        ("DEC2759_3_best_next", "next derivation target", "NO_HIDDEN_VISIBLE_HOM_OPERATOR_DOMAIN", "largest surviving coupling leak covers constants, EM, mass, shadow frames, source weights, and readouts"),
        ("DEC2759_4_next", "next target", "NEXT_2760_NO_HIDDEN_VISIBLE_HOM_JQ_ZERO_OR_FINITE_COEFFICIENT_PRIOR", "attempt coefficient-domain theorem; if not, stage finite coupling priors"),
    ]
    return [nonclaim({"branch_id": BRANCH_ID, "decision_id": row_id, "decision": decision, "result": result, "reason": reason}) for row_id, decision, result, reason in specs]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2759_0_sources", "source paths and needles valid", "PASS_NONCLAIM", "audit reproducible"),
        ("GATE2759_1_conditional_transfer", "conditional MOMS/AX1090 -> j_q^matter=0 theorem transferred", "PASS_NONCLAIM", "theorem route sharper but conditional"),
        ("GATE2759_2_MOMS_signed", "ordinary-matter signature parent-signed", "BLOCKED_NO_CLAIM", "j_q^matter=0 cannot be claimed"),
        ("GATE2759_3_finite_values", "finite j_q source pack numeric/source-backed", "BLOCKED_NO_CLAIM", "R10/PPN/clock/orbital scoring blocked"),
        ("GATE2759_4_same_branch", "numerator, denominator, projection, and source normalization branch-locked", "BLOCKED_NO_CLAIM", "cannot mix closure denominator with unrelated source coefficients"),
        ("GATE2759_5_local_GR", "local GR/Newton derived", "BLOCKED_NO_CLAIM", "residual vector not empty"),
    ]
    return [nonclaim({"claim_gate_id": row_id, "claim_gate": gate, "status": status, "reason": reason}) for row_id, gate, status, reason in specs]


def refusal_rows() -> list[dict[str, Any]]:
    specs = [
        ("REF2759_0_claim_jq_zero", "j_q=0 is now proven by the current corpus", "BLOCKED", "only conditional MOMS/AX1090 theorem is transferred; signature remains unsigned"),
        ("REF2759_1_claim_local_GR", "MTS now derives local GR/Newton", "BLOCKED", "even if j_q^matter vanished, q_loc, Q_R/boundary, beta, source-normalization, curvature, and hidden-visible channels remain"),
        ("REF2759_2_score_tests", "R10/PPN/WEP/clock tests can be scored from 2759", "BLOCKED", "finite source pack is symbolic and branch-normalization dependent"),
        ("REF2759_3_use_countermodels_as_values", "countermodel j_q terms are numerical priors", "BLOCKED", "countermodels are live residual channels until parent coefficients or bounds are sourced"),
    ]
    return [nonclaim({"branch_id": BRANCH_ID, "refusal_id": row_id, "attempted_claim": claim, "status": status, "reason": reason, "runner_allows_claim": False}) for row_id, claim, status, reason in specs]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2759_0_2760",
                "status": "selected_primary",
                "target_doc": "2760-Y5-R2FR-no-hidden-visible-hom-jq-zero-or-finite-coefficient-prior-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_no_hidden_visible_hom_jq_zero_or_finite_coefficient_prior_under_AX1090_2760.py",
                "mission": "attack the largest coupling leak: prove visible coefficient functors exclude hidden/source-only targets, or stage finite coupling priors b_alpha, b_mu, b_mA, b_nuc, delta_w_A, shadow-frame derivatives, and readout tau terms",
                "acceptance": "either parent-signed no-hidden-visible-hom/operator-domain theorem, or complete nonclaim finite coupling prior interface with all arena scores blocked",
                "forbidden": "do not claim local GR/Newton, do not set priors to zero without theorem, do not score tests without source-backed priors, do not edit formalization-workbench, no GitHub action",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"copy_id": "BR2759_0_zero_queue", "source_table": rel(OUTPUTS["zero"]), "copy_path": rel(BRANCH_OUTPUTS["zero_queue"]), "purpose": "j_q zero theorem transfer", "exists": BRANCH_OUTPUTS["zero_queue"].exists()}),
        nonclaim({"copy_id": "BR2759_1_pack_queue", "source_table": rel(OUTPUTS["pack"]), "copy_path": rel(BRANCH_OUTPUTS["pack_queue"]), "purpose": "finite j_q source pack", "exists": BRANCH_OUTPUTS["pack_queue"].exists()}),
        nonclaim({"copy_id": "BR2759_2_arena_beta", "source_table": rel(OUTPUTS["arena"]), "copy_path": rel(BRANCH_OUTPUTS["arena_beta"]), "purpose": "beta/PPN arena impact", "exists": BRANCH_OUTPUTS["arena_beta"].exists()}),
        nonclaim({"copy_id": "BR2759_3_arena_local", "source_table": rel(OUTPUTS["arena"]), "copy_path": rel(BRANCH_OUTPUTS["arena_local"]), "purpose": "local-bound arena impact", "exists": BRANCH_OUTPUTS["arena_local"].exists()}),
        nonclaim({"copy_id": "BR2759_4_next_queue", "source_table": rel(OUTPUTS["next"]), "copy_path": rel(BRANCH_OUTPUTS["next_queue"]), "purpose": "RAB queue for no-hidden-visible-hom", "exists": BRANCH_OUTPUTS["next_queue"].exists()}),
    ]


def pycache_path() -> Path:
    return Path(__file__).resolve().parent / "__pycache__"


def remove_pycache() -> None:
    pycache = pycache_path()
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    start = SCRIPT_START_UTC.timestamp()
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start)


def validation_rows(
    sources: list[dict[str, Any]],
    zero: list[dict[str, Any]],
    signature: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    pack: list[dict[str, Any]],
    arena: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    zero_ok = any(row["zero_id"] == "JQZ2759_3_current_verdict" and row["status"] == "ZERO_THEOREM_NOT_PROMOTED" for row in zero)
    signature_ok = any(row["signature_id"] == "SIG2759_6_verdict" and row["evidence_status"] == "MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED" for row in signature)
    countermodel_ok = {"CMJ2759_0_species_weight", "CMJ2759_1_variable_constants", "CMJ2759_2_shadow_frame", "CMJ2759_5_hidden_visible_hom"}.issubset({row["countermodel_id"] for row in countermodels})
    pack_ok = {"j_q_total", "j_matter", "j_weight", "j_const", "j_shadow", "j_readout", "j_boundary", "j_curvature", "same_branch_lock"}.issubset({row["coefficient"] for row in pack})
    arena_ok = all(row["score_ready"] is False for row in arena) and any(row["arena_id"] == "ARENA2759_4_local_GR" for row in arena)
    decision_ok = any(row["decision_id"] == "DEC2759_4_next" and row["result"] == "NEXT_2760_NO_HIDDEN_VISIBLE_HOM_JQ_ZERO_OR_FINITE_COEFFICIENT_PRIOR" for row in decisions)
    gates_ok = any(row["claim_gate_id"] == "GATE2759_5_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    refusal_ok = all(row["runner_allows_claim"] is False for row in refusal)
    next_ok = next_target[0]["selected"] is True and "2760" in next_target[0]["target_doc"]
    no_claim_flags_ok = all(
        row.get("valid_for_claim") is False and row.get("claim_allowed") is False
        for block in [zero, signature, countermodels, pack, arena, decisions, gates, refusal, next_target]
        for row in block
    )
    branch_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    csv_ok = True
    csv_bits: list[str] = []
    for key, path in {**OUTPUTS, **BRANCH_OUTPUTS}.items():
        if key == "validation":
            continue
        try:
            rows = read_csv(path)
            csv_bits.append(f"{path.name}:{len(rows)}:ok")
        except Exception as exc:
            csv_ok = False
            csv_bits.append(f"{path.name}:ERROR:{exc}")
    pycache_ok = not pycache_path().exists()
    formalization_count = formalization_recent_count()
    formalization_ok = formalization_count == 0
    rows = [
        {"validation_id": "VAL2759_0_sources", "passed": source_ok, "detail": "all source paths exist and needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2759_1_zero_not_promoted", "passed": zero_ok, "detail": "j_q zero theorem remains conditional/nonclaim", "timestamp_utc": ts()},
        {"validation_id": "VAL2759_2_signature_block", "passed": signature_ok, "detail": "MOMS/AX1090 parent ordinary-matter signature remains unsigned", "timestamp_utc": ts()},
        {"validation_id": "VAL2759_3_countermodels", "passed": countermodel_ok, "detail": "major coupling countermodels mapped to j_q channels", "timestamp_utc": ts()},
        {"validation_id": "VAL2759_4_source_pack", "passed": pack_ok, "detail": "finite j_q source pack is explicit and complete", "timestamp_utc": ts()},
        {"validation_id": "VAL2759_5_arena_blocks", "passed": arena_ok, "detail": "all arena rows remain blocked/nonclaim", "timestamp_utc": ts()},
        {"validation_id": "VAL2759_6_next", "passed": decision_ok and next_ok, "detail": "2760 no-hidden-visible-hom/operator-domain target selected", "timestamp_utc": ts()},
        {"validation_id": "VAL2759_7_claim_gates", "passed": gates_ok and no_claim_flags_ok, "detail": "local GR/Newton and generated claim flags remain blocked", "timestamp_utc": ts()},
        {"validation_id": "VAL2759_8_refusal_runner", "passed": refusal_ok, "detail": "refusal runner blocks j_q/local/test claims", "timestamp_utc": ts()},
        {"validation_id": "VAL2759_9_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2759_10_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2759_11_pycache_absent", "passed": pycache_ok, "detail": f"scripts __pycache__ absent={pycache_ok}", "timestamp_utc": ts()},
        {"validation_id": "VAL2759_12_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_count}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2759_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2759 transfers the conditional MOMS/AX1090 ordinary-matter zero theorem into q_R=j_q/(nHn) language, refuses promotion because the signature remains unsigned, stages finite j_q source channels, keeps all local/PPN/R10/WEP/clock/orbital scores blocked, and selects no-hidden-visible-hom/operator-domain as the next coupling target.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2759 - Y5 R2/f(R): j_q Source-Leg Zero Theorem Or Finite Source Pack Under AX1090

Status: `Y5_R2FR_2759_jq_zero_conditional_finite_source_pack_live`

## Private Verdict

2759 attacks the numerator.

With 2758, the finite local q residual is now:

`q_R = j_q / (n_q^A H_AB n_q^B)`.

The good news: the conditional ordinary-matter theorem transfers cleanly. If the full MOMS/AX1090 matter signature is parent-signed, the ordinary matter source leg vanishes: `j_q^matter=0`, and therefore `q_R^matter=0` on the same positive-Hessian branch.

The hard stop: that signature is not parent-signed. Constants, source weights, shadow frames, readout/material projection, boundary hair, curvature terms, and hidden-visible coefficient homomorphisms remain live numerator channels.

So the local-GR route is sharper, not closed. The next coupling target is no-hidden-visible-hom/operator-domain: either visible coefficients cannot depend on hidden/representative variables, or each finite coupling prior must be sourced before tests are scored.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## j_q Zero Theorem Transfer

{markdown_table(data["zero"], ["zero_id", "statement", "formula", "source_basis", "status", "claim_effect", "valid_for_claim"])}

## Matter Signature Clause Status

{markdown_table(data["signature"], ["signature_id", "parent_clause", "evidence_status", "needed_for_jq_zero", "current_gap", "parent_signed", "valid_for_claim"])}

## Countermodel To j_q Map

{markdown_table(data["countermodels"], ["countermodel_id", "surviving_channel", "jq_map", "damage_if_live", "killed_by", "current_status", "valid_for_claim"])}

## Finite j_q Source Pack

{markdown_table(data["pack"], ["pack_id", "coefficient", "definition", "units_or_normalization", "source_status", "missing_for_claim", "arena_use", "valid_for_claim"])}

## q_R Zero And Arena Impact

{markdown_table(data["arena"], ["arena_id", "arena", "updated_formula", "if_jq_zero", "still_blocked_by", "score_ready", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "result", "reason", "valid_for_claim"])}

## Claim Gates

{markdown_table(data["gates"], ["claim_gate_id", "claim_gate", "status", "reason", "valid_for_claim"])}

## Refusal Runner

{markdown_table(data["refusal"], ["refusal_id", "attempted_claim", "status", "reason", "runner_allows_claim", "valid_for_claim"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is the coupling checkpoint. If `j_q` can be zero-proved in the same parent branch, the local q residual shrinks hard. If not, every surviving coupling becomes a finite prior/source row. The next lock is the hidden-visible coefficient domain: EM constants, masses, shadow frames, source weights, and readout maps cannot be hand-waved.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    zero = zero_rows()
    signature = signature_rows()
    countermodels = countermodel_rows()
    pack = pack_rows()
    arena = arena_rows()
    decisions = decision_rows()
    gates = gate_rows()
    refusal = refusal_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["zero"], zero)
    write_csv(OUTPUTS["signature"], signature)
    write_csv(OUTPUTS["countermodels"], countermodels)
    write_csv(OUTPUTS["pack"], pack)
    write_csv(OUTPUTS["arena"], arena)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["zero_queue"], zero)
    write_csv(BRANCH_OUTPUTS["pack_queue"], pack)
    write_csv(BRANCH_OUTPUTS["arena_beta"], arena)
    write_csv(BRANCH_OUTPUTS["arena_local"], arena)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    remove_pycache()
    validation = validation_rows(sources, zero, signature, countermodels, pack, arena, decisions, gates, refusal, next_target)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "zero": zero,
        "signature": signature,
        "countermodels": countermodels,
        "pack": pack,
        "arena": arena,
        "decisions": decisions,
        "gates": gates,
        "refusal": refusal,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    remove_pycache()

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2759 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
