from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1700"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "1700-Y5-R2FR-parent-grammar-exhaustiveness-proof-or-readout-no-reentry.md"

SOURCE_FILES = {
    "1699_doc": ROOT / "1699-Y5-R2FR-parent-source-owner-grammar-or-finite-WEP-request-pack.md",
    "1699_validation": OUT / "P8_Y5_BRR545_1699_VALIDATION.csv",
    "1699_grammar": OUT / "P8_Y5_PARENT_QLOC_1699_PARENT_SOURCE_OWNER_GRAMMAR.csv",
    "1699_hom": OUT / "P8_Y5_PARENT_QLOC_1699_HOM_EXCLUSION_CONDITIONAL_PROOF.csv",
    "1699_signoffs": OUT / "P8_Y5_PARENT_QLOC_1699_REMAINING_SIGNOFFS.csv",
    "566_no_marker": ROOT / "566-Y5-R10-primitive-quotient-no-marker-parent-clause-or-alpha-coefficient-fill.md",
    "576_source_current": ROOT / "576-Y5-R10-constant-source-current-universality-or-qbar-envelope.md",
    "1030_spm": ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
    "1031_terminal": ROOT / "1031-Y5-R10-quotient-naturality-terminal-public-metric-proof-or-spm-closure.md",
    "1314_parent_primitive": ROOT / "1314-Y5-R10-RAB-finite-alpha-coupling-scorepack-or-parent-primitive-source.md",
    "1016_source_selector": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
    "575_readout_constant": ROOT / "575-Y5-R10-readout-constant-sector-first-lock-or-finite-envelope.md",
}

NEEDLES = {
    "1699_doc": ["NEXT1699_0_primary", "CONDITIONAL_GRAMMAR_NOT_PARENT_SIGNED"],
    "1699_validation": ["VAL1699_OVERALL", "PASS"],
    "1699_grammar": ["G1699_4_forbidden_target", "Coeff_active_source[species]"],
    "1699_hom": ["HP1699_4_Hom_result", "conditional_theorem_inside_grammar"],
    "1699_signoffs": ["SO1699_0_parent_grammar_exhaustiveness", "SO1699_1_readout_no_reentry"],
    "566_no_marker": ["B566_0_parent_clause_not_derived", "Primitive quotient/no-marker clause is sufficient but not forced"],
    "576_source_current": ["CE576_1_species_weighted_kappa", "species-weighted kappa_A source equation"],
    "1030_spm": ["SPD1030_6_verdict", "NOT_DERIVED_CURRENT_CORPUS"],
    "1031_terminal": ["TPM1031_6_verdict", "NOT_DERIVED_CURRENT_CORPUS"],
    "1314_parent_primitive": ["PESC1314_0_parent_grammar", "NOT_FOUND_IN_CURRENT_CORPUS"],
    "1016_source_selector": ["PSC1016_7_coupling_descent_silence", "not_signed_coupling_bound_schema_only"],
    "575_readout_constant": ["FL575_2_universal_source_current_lock", "conditional_Hilbert_sublemma"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1700_SOURCE_REGISTER.csv"
EXHAUSTIVENESS_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1700_EXHAUSTIVENESS_PROOF_AUDIT.csv"
COUNTEREXAMPLE_MERGE = OUT / "P8_Y5_PARENT_QLOC_1700_COUNTEREXAMPLE_MERGE.csv"
SIGNOFF_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1700_PARENT_ACTION_SIGNOFF_CONTRACT.csv"
READOUT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1700_READOUT_NO_REENTRY_TARGET.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1700_RUNNER_REFUSAL.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1700_NEXT_TARGET.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1700_CLAIM_GATE.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1700_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    EXHAUSTIVENESS_AUDIT,
    COUNTEREXAMPLE_MERGE,
    SIGNOFF_CONTRACT,
    READOUT_TARGET,
    RUNNER,
    NEXT_TARGET,
    CLAIM_GATE,
]

CLAIM_CHECKED = [
    EXHAUSTIVENESS_AUDIT,
    COUNTEREXAMPLE_MERGE,
    SIGNOFF_CONTRACT,
    READOUT_TARGET,
    RUNNER,
    NEXT_TARGET,
    CLAIM_GATE,
]

COPY_TARGETS = {
    EXHAUSTIVENESS_AUDIT: [
        QUARANTINE / "EXHAUSTIVENESS_PROOF_AUDIT.csv",
        BRANCH_RESIDUALS / "R2FR_exhaustiveness_proof_audit_1700.csv",
        QUEUE / "JR1700_EXHAUSTIVENESS_PROOF_AUDIT.csv",
    ],
    COUNTEREXAMPLE_MERGE: [
        QUARANTINE / "COUNTEREXAMPLE_MERGE.csv",
        BRANCH_RESIDUALS / "R2FR_counterexample_merge_1700.csv",
        QUEUE / "JR1700_COUNTEREXAMPLE_MERGE.csv",
    ],
    SIGNOFF_CONTRACT: [
        QUARANTINE / "PARENT_ACTION_SIGNOFF_CONTRACT.csv",
        BRANCH_RESIDUALS / "R2FR_parent_action_signoff_contract_1700.csv",
        QUEUE / "JR1700_PARENT_ACTION_SIGNOFF_CONTRACT.csv",
    ],
    READOUT_TARGET: [
        QUARANTINE / "READOUT_NO_REENTRY_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_readout_no_reentry_target_1700.csv",
        QUEUE / "JR1700_READOUT_NO_REENTRY_TARGET.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1700.csv",
        QUEUE / "JR1700_NEXT_TARGET.csv",
    ],
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def bool_cell(value: object) -> bool:
    return str(value).strip().lower() == "true"


def list_cell(values: list[object] | tuple[object, ...]) -> str:
    return ";".join(str(value) for value in values)


def markdown_table(rows: list[dict[str, object]], headers: list[str]) -> str:
    if not rows:
        return "_No rows._"
    table = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        table.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(table)


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for key, path in SOURCE_FILES.items():
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = NEEDLES[key]
        needles_present = exists and all(needle in text for needle in needles)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": key,
                "source_path": str(path),
                "exists": exists,
                "needles_present": needles_present,
                "required_needles": list_cell(needles),
                "use_in_1700": "parent grammar exhaustiveness proof audit and readout no-reentry target",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def exhaustiveness_audit_rows() -> list[dict[str, object]]:
    rows = [
        (
            "EXH1700_0_target",
            "Parent grammar exhaustiveness",
            "Allowed ordinary-matter/source/readout constructors are exactly the G1699 source-owner grammar; no extra source-only coefficient object can be added",
            "target_sharp",
            "would promote the conditional Hom exclusion to a real parent theorem",
            "not proved by current corpus",
        ),
        (
            "EXH1700_1_quotient_no_marker",
            "Primitive quotient/no-marker route",
            "ordinary matter factors through quotient data with no marker/spurion extension",
            "sufficient_but_not_derived",
            "would silence direct selector/constant source channels",
            "566 says this is a sufficient parent clause, not forced",
        ),
        (
            "EXH1700_2_constant_source_current",
            "Constant/source-current universality",
            "one Hilbert/coframe source current, trivial matter constants, one global kappa",
            "conditional_sublemma_only",
            "would remove species-weighted active source normalization",
            "576 keeps species-weighted kappa_A as legal counterexample",
        ),
        (
            "EXH1700_3_single_public_metric",
            "Single public metric/coframe",
            "ordinary matter/readout sees one public coframe with no shadow frame slot",
            "contract_ready_not_theorem",
            "would remove common frame coupling c_g",
            "1030 says covariance/WEP/Ward shortcuts fail",
        ),
        (
            "EXH1700_4_terminal_metric",
            "Terminal public metric route",
            "terminal e_pub plus matter-interface functor through terminal evaluation",
            "terminality_insufficient",
            "would help only if action domain is also restricted",
            "1031 says terminality alone does not restrict pre-terminal functors/labels",
        ),
        (
            "EXH1700_5_parent_primitive_hunt",
            "Parent grammar primitive",
            "a deeper typed no-hidden-visible theorem forbids visible source coefficients before readout",
            "not_found_in_current_corpus",
            "would supply the missing exhaustiveness signature",
            "1314 records this escape hatch as not found",
        ),
        (
            "EXH1700_6_result",
            "Exhaustiveness verdict",
            "the current corpus supports an exact signoff contract, not a proof of exhaustiveness",
            "EXHAUSTIVENESS_NOT_DERIVED",
            "do not promote AX1697/Hom/Delta_w",
            "select readout no-reentry as next contained target",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": aid,
            "attempt": attempt,
            "formal_statement": statement,
            "result": result,
            "would_close": would_close,
            "failure_or_source": failure,
            "parent_derived": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for aid, attempt, statement, result, would_close, failure in rows
    ]


def counterexample_rows() -> list[dict[str, object]]:
    rows = [
        (
            "CM1700_0_marker_spurion",
            "marker/spurion constants",
            "theta_A=theta_A(I_X) or material/readout marker depends on a hidden invariant",
            "ordinary constants carry MTS charge even if geometry is quotient-owned",
            "parent no-marker theorem or finite b_A/b_alpha/material rows",
        ),
        (
            "CM1700_1_species_kappa",
            "species/source weighted active coupling",
            "E_mu_nu=sum_A kappa_A T_A_mu_nu with each T_A conserved",
            "Bianchi/Ward identities do not force all kappa_A equal",
            "global coupling superselection theorem or source-weight finite bounds",
        ),
        (
            "CM1700_2_shadow_frame",
            "common conformal/disformal matter frame",
            "S_matter[Psi,A_g(X)^2 g_obs+B_g(X)U_mu U_nu,theta]",
            "WEP can be quiet while fifth-force/PPN/clock/source effects remain",
            "single public metric theorem or finite c_g/b_dis rows",
        ),
        (
            "CM1700_3_terminal_predependence",
            "terminal object but pre-terminal matter dependence",
            "E_A(q) maps uniquely to e_pub but S_A is evaluated on E_A before the map",
            "terminality does not by itself exclude extra labels/frames",
            "matter-interface functor through terminal evaluation only",
        ),
        (
            "CM1700_4_readout_reentry",
            "post-variation readout/effective source coefficient",
            "projection, EFT, boundary, instrument or material map multiplies the already-varied source",
            "even a clean bare grammar can regenerate source weights after variation",
            "readout/effective no-reentry theorem or finite arena-specific product map",
        ),
        (
            "CM1700_5_nonHilbert_source_tail",
            "non-Hilbert or boundary source current",
            "q_res^nu=nabla_mu K_owner^{mu nu}+q_retained^nu with nonzero flux/support shift",
            "Hilbert current universality does not equal measured local source normalization",
            "source-support/local projection theorem or finite residual vector",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": cid,
            "counterexample_class": cls,
            "construction": construction,
            "what_breaks": breaks,
            "required_repair": repair,
            "blocks_exhaustiveness": True,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for cid, cls, construction, breaks, repair in rows
    ]


def signoff_contract_rows() -> list[dict[str, object]]:
    rows = [
        (
            "SIG1700_0_interface_category",
            "ordinary interface category fixed by parent action",
            "Parent action defines the complete object class seen by ordinary matter, rods, clocks, photons, sources, and readout before any fit",
            "missing",
            "prevents adding new visible source-coefficient objects",
        ),
        (
            "SIG1700_1_terminal_evaluation",
            "matter action terminal-evaluation only",
            "S_matter factors through e_pub/q-owned observed data and cannot evaluate on pre-terminal labelled frames",
            "missing",
            "blocks terminal-predependence and shadow frame countermodels",
        ),
        (
            "SIG1700_2_no_marker_constants",
            "constants/material markers are parent-trivial or retained",
            "m_A, alpha_EM, material labels, clock constants, and representation data cannot depend on hidden/MTS source invariants unless retained as finite rows",
            "missing",
            "blocks marker/spurion and field-rename hiding",
        ),
        (
            "SIG1700_3_global_source_coupling",
            "one global source coupling",
            "active ordinary source is one Hilbert/coframe current with one common kappa/G calibration, not kappa_A or kappa_eff(source)",
            "missing",
            "blocks species/source-weighted active coupling",
        ),
        (
            "SIG1700_4_no_nonHilbert_tail",
            "non-Hilbert/boundary/source tail zero or retained",
            "boundary, memory, domain, projector, support-shift, and non-Hilbert currents are exact zero-flux or explicit finite residuals",
            "missing",
            "prevents source-side local-GR overclaim",
        ),
        (
            "SIG1700_5_readout_no_reentry",
            "readout/effective no-reentry",
            "projection, EFT, material, instrument, clock, and orbit readout maps preserve the parent coefficient domain and cannot recreate source-only weights",
            "selected_next",
            "the most contained next theorem target after exhaustiveness fails",
        ),
        (
            "SIG1700_6_verdict",
            "parent action signoff contract",
            "all SIG1700_0 through SIG1700_5 must be parent-signed before AX1697/Hom/Delta_w can become claim-valid",
            "CONTRACT_READY_NOT_SIGNED",
            "do not call this derived GR/Newton",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "signoff_id": sid,
            "signoff": signoff,
            "required_statement": statement,
            "status": status,
            "purpose": purpose,
            "parent_signed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for sid, signoff, statement, status, purpose in rows
    ]


def readout_target_rows() -> list[dict[str, object]]:
    rows = [
        (
            "RNR1700_0_scope",
            "readout no-reentry theorem target",
            "For every readout/effective map R after parent variation, R maps allowed coefficient-domain objects to allowed readout observables and has no codomain component Coeff_active_source[species]",
            "target_selected",
            "separates post-variation/effective leakage from parent grammar exhaustiveness",
        ),
        (
            "RNR1700_1_maps",
            "maps to audit",
            "projection Pi, EFT/radiative renormalization, material response, clock/spectroscopy response, orbit/GM readout, boundary/support selectors",
            "audit_required",
            "each map can otherwise regenerate a hidden source coefficient",
        ),
        (
            "RNR1700_2_commutator",
            "readout-variation commutator",
            "[delta_parent, R_readout] must not produce source-only coefficient terms; if nonzero, it becomes a finite residual row",
            "formula_target",
            "turns vague readout worries into a testable commutator/residual",
        ),
        (
            "RNR1700_3_arena_split",
            "arena-specific no-transfer rule",
            "R10, WEP, PPN, clocks, orbital, and EM readouts each need their own no-reentry or finite product map",
            "guardrail",
            "prevents clock/WEP/R10 bound transfer by vibes",
        ),
        (
            "RNR1700_4_empirical_path",
            "finite fallback",
            "if no-reentry is not proved, keep beta/tau/material/source/readout factors as explicit finite rows with source paths",
            "fallback_ready",
            "keeps the theory testable instead of closure-only",
        ),
        (
            "RNR1700_5_verdict",
            "next target decision",
            "readout no-reentry is the next best attack because grammar exhaustiveness is blocked but post-variation leakage is smaller and more local",
            "READOUT_NO_REENTRY_SELECTED",
            "target 1701",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "target_id": tid,
            "target": target,
            "formal_statement": statement,
            "status": status,
            "why_next": why,
            "parent_derived": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for tid, target, statement, status, why in rows
    ]


def runner_rows() -> list[dict[str, object]]:
    rows = [
        ("RUN1700_0_exhaustiveness", "claim parent grammar exhaustive", "REJECT_EXHAUSTIVENESS_CLAIM", "prior routes all require missing parent signoffs"),
        ("RUN1700_1_Hom_theorem", "promote Hom exclusion to full parent theorem", "REJECT_HOM_PROMOTION", "Hom proof remains conditional on unsigned grammar"),
        ("RUN1700_2_Delta_w_zero", "set Delta_w_A=0", "REJECT_DELTA_W_ZERO", "source-owner signoff contract not signed"),
        ("RUN1700_3_readout_zero", "claim readout no-reentry proven", "REJECT_READOUT_ZERO", "1700 only selects the target; it does not prove it"),
        ("RUN1700_4_WEP_R10_score", "score WEP/R10 source branch", "REJECT_SCORE", "finite beta/tau/material/source/readout products remain missing"),
        ("RUN1700_5_local_gr", "claim local GR/Newton", "BLOCKED_NO_CLAIM", "right-hand source grammar remains conditional and left-hand GR/Newton gates remain separate"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": rid,
            "case": case,
            "status": status,
            "reason": reason,
            "can_score": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rid, case, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT1700_0_primary",
            "1701-Y5-R2FR-readout-effective-no-reentry-theorem-or-finite-product-map.md",
            "scripts/Y5_R2FR_readout_effective_no_reentry_theorem_or_finite_product_map.py",
            "prove that readout/effective maps cannot recreate source-only coefficients after parent variation; if not, split finite R10/WEP/PPN/clock/orbital product maps",
            "selected",
        ),
        (
            "NEXT1700_1_theory",
            "1701a-Y5-R2FR-readout-variation-commutator-zero-proof.md",
            "scripts/Y5_R2FR_readout_variation_commutator_zero_proof.py",
            "attack [delta_parent,R_readout] source-coefficient silence directly",
            "held_fallback",
        ),
        (
            "NEXT1700_2_empirical",
            "1701b-Y5-R2FR-arena-finite-product-map-skeleton.md",
            "scripts/Y5_R2FR_arena_finite_product_map_skeleton.py",
            "build explicit finite product schemas for R10, WEP, PPN, clocks, orbital, and EM readouts",
            "held_fallback",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": rid,
            "next_target": target,
            "script": script,
            "objective": objective,
            "selection_status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rid, target, script, objective, status in rows
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1700_0_exhaustiveness", "parent grammar exhaustiveness", "BLOCKED_NO_CLAIM", "current corpus supports contract only"),
        ("CG1700_1_Hom_exclusion", "Hom exclusion as parent theorem", "BLOCKED_NO_CLAIM", "conditional on unsigned grammar"),
        ("CG1700_2_Delta_w", "Delta_w_A=0 theorem", "BLOCKED_NO_CLAIM", "parent action signoff contract incomplete"),
        ("CG1700_3_readout_no_reentry", "readout/effective no-reentry theorem", "BLOCKED_NO_CLAIM", "selected next target only"),
        ("CG1700_4_finite_products", "finite R10/WEP/PPN/clock/orbital products scoreable", "BLOCKED_NO_CLAIM", "schemas/source paths still needed"),
        ("CG1700_5_local_GR_Newton", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "source-owner and left-hand field-equation gates remain open"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": cid,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for cid, claim, status, reason in rows
    ]


def all_claim_flags_false(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field in (
                "can_score",
                "accepted_for_scoring",
                "score_ready",
                "valid_prediction_row",
                "valid_for_claim",
                "claim_allowed",
                "parent_derived",
                "parent_signed",
            ):
                if field in row and bool_cell(row[field]):
                    return False
    return True


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validate(
    source_rows_: list[dict[str, object]],
    audit_rows: list[dict[str, object]],
    counter_rows: list[dict[str, object]],
    signoff_rows: list[dict[str, object]],
    readout_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows_)
    exhaustiveness_blocked = any(row["audit_id"] == "EXH1700_6_result" and row["result"] == "EXHAUSTIVENESS_NOT_DERIVED" for row in audit_rows)
    prior_routes_covered = {"Primitive quotient/no-marker route", "Constant/source-current universality", "Single public metric/coframe", "Terminal public metric route", "Parent grammar primitive"}.issubset({str(row["attempt"]) for row in audit_rows})
    counterexamples_complete = len(counter_rows) >= 6 and all(bool_cell(row["blocks_exhaustiveness"]) for row in counter_rows)
    signoff_contract_complete = {"ordinary interface category fixed by parent action", "matter action terminal-evaluation only", "constants/material markers are parent-trivial or retained", "one global source coupling", "non-Hilbert/boundary/source tail zero or retained", "readout/effective no-reentry"}.issubset({str(row["signoff"]) for row in signoff_rows})
    contract_not_signed = all(not bool_cell(row["parent_signed"]) for row in signoff_rows)
    readout_selected = any(row["target_id"] == "RNR1700_5_verdict" and row["status"] == "READOUT_NO_REENTRY_SELECTED" for row in readout_rows)
    readout_not_claimed = all(not bool_cell(row["parent_derived"]) for row in readout_rows)
    runner_blocks = all(not bool_cell(row["can_score"]) for row in runner_rows_)
    next_selected = any(row["route_id"] == "NEXT1700_0_primary" and row["selection_status"] == "selected" for row in next_rows)
    local_gr_blocked = any(row["claim"] == "derived local GR/Newton reduction" and row["status"] == "BLOCKED_NO_CLAIM" for row in claim_rows)
    no_claim_flags = all_claim_flags_false(CLAIM_CHECKED)
    csv_parse = True
    for path in GENERATED:
        try:
            read_csv(path)
        except Exception:
            csv_parse = False
    branch_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = len(list(FORMALIZATION.rglob("*1700*"))) == 0 if FORMALIZATION.exists() else True
    checks = [
        ("VAL1700_0_sources_exist", sources_ok, "all cited local source paths exist and required needles are present"),
        ("VAL1700_1_exhaustiveness_blocked", exhaustiveness_blocked, "parent grammar exhaustiveness is not promoted"),
        ("VAL1700_2_prior_routes_covered", prior_routes_covered, "audit covers no-marker, source-current, SPM, terminal metric, and parent primitive routes"),
        ("VAL1700_3_counterexamples_complete", counterexamples_complete, "counterexample merge covers all live exhaustiveness blockers"),
        ("VAL1700_4_signoff_contract_complete", signoff_contract_complete, "parent action signoff contract includes all required locks"),
        ("VAL1700_5_contract_not_signed", contract_not_signed, "no signoff is marked parent-signed"),
        ("VAL1700_6_readout_selected", readout_selected, "readout no-reentry is selected as the next contained target"),
        ("VAL1700_7_readout_not_claimed", readout_not_claimed, "readout no-reentry is not claimed as derived"),
        ("VAL1700_8_runner_blocks", runner_blocks, "runner blocks exhaustiveness, Hom, Delta_w, readout, score, and local-GR claims"),
        ("VAL1700_9_next_selected", next_selected, "next target selects readout/effective no-reentry or finite product map"),
        ("VAL1700_10_local_gr_blocked", local_gr_blocked, "local GR/Newton claim remains blocked"),
        ("VAL1700_11_no_claim_flags", no_claim_flags, "all generated scoring and claim flags remain false"),
        ("VAL1700_12_csv_parse", csv_parse, "all generated 1700 CSVs parse"),
        ("VAL1700_13_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1700_14_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1700_15_formalization_untouched", formalization_untouched, "no 1700 outputs found under formalization-workbench"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "check_id": cid,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for cid, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1700_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1700 parent grammar exhaustiveness audit and readout no-reentry target validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def write_doc(
    source_rows_: list[dict[str, object]],
    audit_rows: list[dict[str, object]],
    counter_rows: list[dict[str, object]],
    signoff_rows: list[dict[str, object]],
    readout_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1700 - Parent Grammar Exhaustiveness Proof Or Readout No-Reentry

## Verdict

1700 tries to sign the parent source-owner grammar and refuses to fake it. The current corpus does **not** prove grammar exhaustiveness. It proves something slightly weaker but very valuable: the exact parent-action signoff contract is now visible.

The old zero routes all hit the same wall. Quotient/no-marker is sufficient but not forced. Constant/source-current universality is a good conditional sublemma but leaves `kappa_A` legal. Single-public-metric and terminal-public-metric routes sharpen the frame problem but do not restrict the full matter interface by themselves. The parent grammar primitive hunt records no current source for the missing typed no-hidden-visible theorem.

So the source-owner/Hom theorem remains conditional. The next best contained attack is **readout/effective no-reentry**: prove that maps applied after parent variation cannot recreate source-only coefficients, or split those maps into finite arena-specific product rows.

## Source Register

{markdown_table(source_rows_, ["source_key", "source_path", "exists", "needles_present", "use_in_1700"])}

## Exhaustiveness Proof Audit

{markdown_table(audit_rows, ["audit_id", "attempt", "result", "failure_or_source"])}

## Counterexample Merge

{markdown_table(counter_rows, ["counterexample_id", "counterexample_class", "what_breaks", "required_repair"])}

## Parent Action Signoff Contract

{markdown_table(signoff_rows, ["signoff_id", "signoff", "status", "purpose"])}

## Readout No-Reentry Target

{markdown_table(readout_rows, ["target_id", "target", "status", "why_next"])}

## Runner Refusal

{markdown_table(runner_rows_, ["runner_id", "case", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["route_id", "next_target", "objective", "selection_status"])}

## Claim Gates

{markdown_table(claim_rows, ["claim_id", "claim", "status", "reason"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

This is a useful narrowing, not a retreat. The source coupling problem is no longer a fog bank; it is a checklist. If we can prove readout no-reentry, we remove the most annoying post-variation backdoor. If we cannot, we stop giving it theorem credit and force R10/WEP/PPN/clock/orbital branches to carry explicit finite product maps. Very engineering. Less poetry, more load paths.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows_ = source_register_rows()
    audit_rows = exhaustiveness_audit_rows()
    counter_rows = counterexample_rows()
    signoff_rows = signoff_contract_rows()
    readout_rows = readout_target_rows()
    runner_rows_ = runner_rows()
    next_rows = next_target_rows()
    claim_rows = claim_gate_rows()
    write_csv(SOURCE_REGISTER, source_rows_, ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1700", "valid_for_claim", "claim_allowed"])
    write_csv(EXHAUSTIVENESS_AUDIT, audit_rows, ["branch_id", "audit_id", "attempt", "formal_statement", "result", "would_close", "failure_or_source", "parent_derived", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(COUNTEREXAMPLE_MERGE, counter_rows, ["branch_id", "counterexample_id", "counterexample_class", "construction", "what_breaks", "required_repair", "blocks_exhaustiveness", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(SIGNOFF_CONTRACT, signoff_rows, ["branch_id", "signoff_id", "signoff", "required_statement", "status", "purpose", "parent_signed", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(READOUT_TARGET, readout_rows, ["branch_id", "target_id", "target", "formal_statement", "status", "why_next", "parent_derived", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(RUNNER, runner_rows_, ["branch_id", "runner_id", "case", "status", "reason", "can_score", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(NEXT_TARGET, next_rows, ["branch_id", "route_id", "next_target", "script", "objective", "selection_status", "valid_for_claim", "claim_allowed"])
    write_csv(CLAIM_GATE, claim_rows, ["branch_id", "claim_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])
    copy_outputs()
    cleanup_pycache()
    validation_rows = validate(source_rows_, audit_rows, counter_rows, signoff_rows, readout_rows, runner_rows_, next_rows, claim_rows)
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows_, audit_rows, counter_rows, signoff_rows, readout_rows, runner_rows_, next_rows, claim_rows, validation_rows)
    failed = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("1700 validation PASS")


if __name__ == "__main__":
    main()
