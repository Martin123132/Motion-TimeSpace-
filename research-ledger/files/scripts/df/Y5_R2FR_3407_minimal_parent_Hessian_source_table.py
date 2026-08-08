from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3407-Y5-R2FR-minimal-parent-Hessian-source-table-under-AX1090.md"

SOURCES = {
    "doc_3406": ROOT / "3406-Y5-R2FR-parent-Hessian-mode-rank-extractor-under-AX1090.md",
    "next_3406": OUT / "P8_Y5_R2FR_3406_NEXT_TARGET.csv",
    "input_3406": OUT / "P8_Y5_R2FR_3406_HESSIAN_INPUT_STATUS.csv",
    "contract_3406": OUT / "P8_Y5_R2FR_3406_HESSIAN_EXTRACTOR_CONTRACT.csv",
    "theorem_3406": OUT / "P8_Y5_R2FR_3406_MODE_RANK_THEOREM.csv",
    "prop_3406": OUT / "P8_Y5_R2FR_3406_PUBLIC_PROPAGATOR_TESTS.csv",
    "bound_3406": OUT / "P8_Y5_R2FR_3406_RESIDUE_BOUND_INTERFACE.csv",
    "action_blocks": OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
    "hamiltonian_source": OUT / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
    "hilbert_3340": OUT / "P8_Y5_R2FR_3340_PARENT_HILBERT_SOURCE_CLAUSE.csv",
    "hessian_3316": OUT / "P8_Y5_R2FR_3316_HESSIAN_READOUT_DERIVATION.csv",
    "hessian_3317": OUT / "P8_Y5_R2FR_3317_MINIMAL_HESSIAN_FORMULA.csv",
    "effective_3174": OUT / "P8_Y5_R2FR_3174_EFFECTIVE_HESSIAN_EXTRACTION.csv",
    "parent_hessian_3093": OUT / "P8_Y5_R2FR_3093_PARENT_HESSIAN_AUDIT.csv",
    "mode_mass_3302": OUT / "P8_Y5_R2FR_3302_LINEARIZED_MODE_MASS_MAP.csv",
    "operator_triage_3406": OUT / "P8_Y5_R2FR_3406_MODE_FAMILY_TRIAGE.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3407_SOURCE_REGISTER.csv",
    "minimal_requirements": OUT / "P8_Y5_R2FR_3407_MINIMAL_HRJ_REQUIREMENTS.csv",
    "candidate_source_table": OUT / "P8_Y5_R2FR_3407_CANDIDATE_HRJ_SOURCE_TABLE.csv",
    "claim_ready_table": OUT / "P8_Y5_R2FR_3407_CLAIM_READY_HRJ_TABLE.csv",
    "refusal_rules": OUT / "P8_Y5_R2FR_3407_HRJ_REFUSAL_RULES.csv",
    "pole_readiness": OUT / "P8_Y5_R2FR_3407_PUBLIC_POLE_READINESS.csv",
    "missing_input_queue": OUT / "P8_Y5_R2FR_3407_MISSING_INPUT_QUEUE.csv",
    "bound_fallback": OUT / "P8_Y5_R2FR_3407_BOUND_FALLBACK_QUEUE.csv",
    "selector_impact": OUT / "P8_Y5_R2FR_3407_SELECTOR_IMPACT.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3407_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3407_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3407_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3407_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3407_VALIDATION.csv",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fields = list(rows[0].keys())
    clean = lambda value: str(value).replace("\n", " ").replace("|", "/")
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def source_register() -> list[dict[str, Any]]:
    roles = {
        "input_3406": "3406 gap list that 3407 must populate or refuse",
        "action_blocks": "candidate EH/action/source/readout parent blocks",
        "hilbert_3340": "conditional Hilbert matter+EM source clauses",
        "hessian_3316": "formula-grade H_AB/R/G_pub machinery",
        "hessian_3317": "minimal two-channel Hessian algebra",
        "effective_3174": "effective readout/operator candidate",
        "parent_hessian_3093": "parent Hessian missing-sign/mass/source audit",
        "mode_mass_3302": "linearized scalar/spin2 mass templates",
    }
    return [
        {
            "source_id": key,
            "path": str(path),
            "exists": path.exists(),
            "role": roles.get(key, "supporting checkpoint/source evidence"),
            "valid_for_claim": False,
        }
        for key, path in SOURCES.items()
    ]


def minimal_requirements() -> list[dict[str, Any]]:
    return [
        {
            "requirement_id": "HRJ3407_0_branch",
            "object": "stationary branch",
            "required_row": "F_A(Phi0)=0 modulo gauge/fixed boundary",
            "acceptance_rule": "must cite parent Euler expression or exact zero theorem before Hessian entries count",
            "blocks_if_missing": "Hessian around non-solution cannot prove physical mode rank",
            "valid_for_claim": False,
        },
        {
            "requirement_id": "HRJ3407_1_Hhh",
            "object": "metric Hessian H_hh",
            "required_row": "H_hh(k) has positive massless spin-2 principal block proportional to k^2 P^(2)",
            "acceptance_rule": "source-backed parent action or linearized parent equation, with gauge handling and G_ref normalization",
            "blocks_if_missing": "no GR/Newton spin-2 pole can be promoted",
            "valid_for_claim": False,
        },
        {
            "requirement_id": "HRJ3407_2_Rh",
            "object": "metric readout R_h",
            "required_row": "R_{mn,h}=delta g_pub_mn/delta h = identity on observed metric perturbations",
            "acceptance_rule": "same observed coframe/readout theorem through O(U^2), not just notation",
            "blocks_if_missing": "pole may be in the wrong metric sector",
            "valid_for_claim": False,
        },
        {
            "requirement_id": "HRJ3407_3_Jh",
            "object": "metric source covector J_h",
            "required_row": "J_h = 1/2 T_total^{mn} from descended Hilbert matter+EM source",
            "acceptance_rule": "one parent matter/EM action varied before calibration, no species/EM/source-only weights",
            "blocks_if_missing": "massless pole cannot be tied to Newton/Maxwell source",
            "valid_for_claim": False,
        },
        {
            "requirement_id": "HRJ3407_4_Hxx",
            "object": "extra-sector Hessian H_xx",
            "required_row": "H_xx(k)=Z_x k^2 + M_x^2 or stronger positive/gapped operator",
            "acceptance_rule": "same branch units, sign, mass gap, boundary class and source-free Hessian",
            "blocks_if_missing": "extra scalar/vector/domain pole remains live",
            "valid_for_claim": False,
        },
        {
            "requirement_id": "HRJ3407_5_Hhx",
            "object": "cross Hessian H_hx",
            "required_row": "H_hx=0 by symmetry/constraint or included in a positive block with pole residues evaluated",
            "acceptance_rule": "cannot assume block diagonalization by variable choice; must use G_pub invariant",
            "blocks_if_missing": "finite pole or massless-pole contamination may survive",
            "valid_for_claim": False,
        },
        {
            "requirement_id": "HRJ3407_6_RxJx",
            "object": "extra readout/source overlap",
            "required_row": "R_x=0 and J_x=0, or residue B_x(lambda) is computed/bounded",
            "acceptance_rule": "field-redefinition-invariant residue silence, not separate Z/U naming",
            "blocks_if_missing": "TT-only rank and local-GR selector stay blocked",
            "valid_for_claim": False,
        },
    ]


def candidate_source_table() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CAND3407_0_EH_Hhh",
            "sector": "metric_EH_core",
            "H_AB_candidate": "H_hh = linearized variation of (2*kappa0)^-1 int sqrt(-g_obs)(R-2Lambda0)",
            "R_candidate": "R_h = identity_on_delta_g if g_pub=g_obs",
            "J_candidate": "J_h = 1/2 T_total from Hilbert variation",
            "best_source": str(SOURCES["action_blocks"]),
            "evidence_level": "CANDIDATE_ANCHOR_PRESENT",
            "missing_for_claim": "parent action reduction, constant kappa, readout identity through O(U^2), Hilbert source adoption",
            "claim_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "CAND3407_1_Hilbert_Jh",
            "sector": "matter_EM_source",
            "H_AB_candidate": "not a propagating Hessian block; supplies source covector",
            "R_candidate": "matter/EM see g_obs",
            "J_candidate": "T_total^{mn}=(-2/sqrt(-g)) delta(S_matter+S_EM)/delta g_mn; includes Maxwell/Poynting stress",
            "best_source": str(SOURCES["hilbert_3340"]),
            "evidence_level": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "missing_for_claim": "parent adoption, common kappa, public Hodge/current normalization, no hidden source weights",
            "claim_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "CAND3407_2_public_Gpub_formula",
            "sector": "field_redefinition_invariant_readout",
            "H_AB_candidate": "symbolic H_AB(k) from second variation",
            "R_candidate": "R_{mn,A}=delta g_pub_mn/delta Phi^A",
            "J_candidate": "source overlap appears through T^{mn}R_{mn,A}",
            "best_source": str(SOURCES["hessian_3316"]),
            "evidence_level": "FORMULA_DERIVED",
            "missing_for_claim": "actual H_AB entries, actual R map, source covector per parent field",
            "claim_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "CAND3407_3_effective_metric_readout",
            "sector": "effective_metric_operator",
            "H_AB_candidate": "L_eff[h]=delta(G+Lambda g)/delta g * h from effective v1 equation",
            "R_candidate": "E_metric=identity_on_delta_g if ordinary matter/clocks/orbits read same g_mn",
            "J_candidate": "delta K_matter plus delta K_MTS source-side slots",
            "best_source": str(SOURCES["effective_3174"]),
            "evidence_level": "EFFECTIVE_CONDITIONAL_SCAFFOLD",
            "missing_for_claim": "closed parent action derivation, same public readout, compact source selector",
            "claim_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "CAND3407_4_minimal_extra_x",
            "sector": "generic_extra_mode",
            "H_AB_candidate": "H(p)=[[a p,b0+b1 p],[b0+b1 p,M2+z p]]",
            "R_candidate": "R=(1,u)",
            "J_candidate": "source overlap implied by public exchange numerator/residue",
            "best_source": str(SOURCES["hessian_3317"]),
            "evidence_level": "SYMBOLIC_TEST_BED",
            "missing_for_claim": "which MTS field x, parent values for a,b0,b1,M2,z,u, source overlap and boundary class",
            "claim_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "CAND3407_5_Xhat_Hessian",
            "sector": "extra_Xhat_scalar_or_domain",
            "H_AB_candidate": "H_xx=Z_X k^2+M_X^2 with positive Z_X,M_X^2",
            "R_candidate": "R_X missing or conditional",
            "J_candidate": "J_X=0 or bounded required",
            "best_source": str(SOURCES["parent_hessian_3093"]),
            "evidence_level": "AUDIT_ROWS_MISSING_PARENT_SIGN",
            "missing_for_claim": "Euler zero, Z_X sign, M_X^2 mass gap, cross-Hessian, J_X, boundary flux, normalization",
            "claim_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "CAND3407_6_R2_Ricci_Weyl_modes",
            "sector": "quadratic_metric_modes",
            "H_AB_candidate": "R2/fR scalar and Ricci/Weyl massive-spin2 mass templates",
            "R_candidate": "universal metric projection only in pure metric quadratic case",
            "J_candidate": "universal Hilbert source assumed by template, not MTS-derived",
            "best_source": str(SOURCES["mode_mass_3302"]),
            "evidence_level": "TEMPLATE_NOT_MTS_SOURCE_ROW",
            "missing_for_claim": "actual coefficients, signs, source coupling, screening/local profile, exact MTS projection",
            "claim_ready": False,
            "valid_for_claim": False,
        },
    ]


def claim_ready_table() -> list[dict[str, Any]]:
    return [
        {
            "table_id": "CRT3407_0_massless_metric_pole",
            "needed_rows": "CAND3407_0 plus CAND3407_1 plus CAND3407_2",
            "required_status": "parent-signed H_hh, R_h, J_h, common G_ref, boundary/gauge class",
            "current_status": "NOT_READY_FORMULA_AND_CANDIDATES_ONLY",
            "can_evaluate_residue_now": False,
            "claim_ready": False,
            "valid_for_claim": False,
        },
        {
            "table_id": "CRT3407_1_extra_mode_silence",
            "needed_rows": "CAND3407_4/CAND3407_5/CAND3407_6 per operator family",
            "required_status": "H_xx/H_hx/R_x/J_x source rows or exact zero theorem",
            "current_status": "NOT_READY_VALUES_AND_SOURCE_OVERLAPS_MISSING",
            "can_evaluate_residue_now": False,
            "claim_ready": False,
            "valid_for_claim": False,
        },
        {
            "table_id": "CRT3407_2_full_public_exchange",
            "needed_rows": "all H_AB/R/J blocks in one branch",
            "required_status": "single self-adjoint boundary class, zero-mode classification, common units",
            "current_status": "NOT_READY_BOUNDARY_AND_ZERO_MODE_CLASS_OPEN",
            "can_evaluate_residue_now": False,
            "claim_ready": False,
            "valid_for_claim": False,
        },
    ]


def refusal_rules() -> list[dict[str, Any]]:
    return [
        {
            "rule_id": "REF3407_0_no_formula_as_value",
            "rule": "A symbolic formula for H_AB/R/J cannot be used as a residue value.",
            "blocks": "marking G_pub or minimal two-channel algebra as TT-only proof",
            "valid_for_claim": False,
        },
        {
            "rule_id": "REF3407_1_no_effective_scaffold_as_parent",
            "rule": "An effective GR-like operator scaffold cannot be counted as parent-derived EH unless the parent action reduction is signed.",
            "blocks": "importing GR through 3174 effective v1 rows",
            "valid_for_claim": False,
        },
        {
            "rule_id": "REF3407_2_no_variable_name_silence",
            "rule": "Extra modes are silent only by public residue B_i=0/bounded, not by moving coupling between Z_i, U_i, R_i or J_i.",
            "blocks": "field-redefinition leakage",
            "valid_for_claim": False,
        },
        {
            "rule_id": "REF3407_3_no_Hilbert_without_parent_adoption",
            "rule": "Hilbert source formulas are conditional until the parent matter/EM action and public Hodge/current normalization are adopted.",
            "blocks": "using Maxwell/Poynting stress correctly in prose but not in the parent source covector",
            "valid_for_claim": False,
        },
        {
            "rule_id": "REF3407_4_no_boundary_sweep",
            "rule": "H_AB entries are not claim-ready unless self-adjoint boundary/domain class and zero-mode charge are fixed or bounded.",
            "blocks": "edge/domain modes hiding inside local-GR reduction",
            "valid_for_claim": False,
        },
    ]


def pole_readiness() -> list[dict[str, Any]]:
    return [
        {
            "pole_id": "POLE3407_0_GR_TT",
            "pole": "massless TT spin-2",
            "required_inputs": "H_hh, R_h, J_h, G_ref, gauge fixing, boundary class",
            "available_inputs": "EH action candidate, readout candidate, Hilbert source conditional, G_pub formula",
            "readiness": "FORMULA_READY_NOT_RESIDUE_READY",
            "claim_ready": False,
            "valid_for_claim": False,
        },
        {
            "pole_id": "POLE3407_1_scalar",
            "pole": "spin-0 scalar/R2/fR/Xhat",
            "required_inputs": "H_xx, H_hx, R_x, J_x, M_x^2, Z_x, boundary/source profile",
            "available_inputs": "mass templates and Xhat audit only",
            "readiness": "NOT_READY",
            "claim_ready": False,
            "valid_for_claim": False,
        },
        {
            "pole_id": "POLE3407_2_massive_spin2",
            "pole": "massive spin-2 / Weyl-Ricci",
            "required_inputs": "quadratic curvature coefficients, sign/stability, R/J overlap",
            "available_inputs": "template mass/amplitude relation only",
            "readiness": "NOT_READY",
            "claim_ready": False,
            "valid_for_claim": False,
        },
        {
            "pole_id": "POLE3407_3_connection_vector_domain",
            "pole": "connection/vector/domain/memory/bulk modes",
            "required_inputs": "sector Hessian, source/readout overlap, zero-mode class, projection to local tests",
            "available_inputs": "R11 triage and residual formulas",
            "readiness": "NOT_READY_BOUND_ROUTE_ONLY",
            "claim_ready": False,
            "valid_for_claim": False,
        },
    ]


def missing_input_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "MIQ3407_0_parent_action_reduction",
            "needed": "derive S_parent quadratic reduction to EH block plus explicit extra-sector blocks",
            "first_source_to_extend": str(SOURCES["action_blocks"]),
            "why_priority": "without this, H_hh is an anchor not a parent-owned row",
            "valid_for_claim": False,
        },
        {
            "queue_id": "MIQ3407_1_readout_derivative",
            "needed": "derive R_{mn,A}=delta g_pub/delta Phi^A for h and every extra retained field",
            "first_source_to_extend": str(SOURCES["effective_3174"]),
            "why_priority": "R controls whether a mode is physically visible",
            "valid_for_claim": False,
        },
        {
            "queue_id": "MIQ3407_2_source_covector",
            "needed": "derive J_A for matter+EM+Maxwell/Poynting stress and prove J_X=0 or bound it",
            "first_source_to_extend": str(SOURCES["hilbert_3340"]),
            "why_priority": "J controls whether a mode couples to compact sources",
            "valid_for_claim": False,
        },
        {
            "queue_id": "MIQ3407_3_extra_sector_Hessian",
            "needed": "derive Z_X, M_X^2, H_hx and sign/unit conventions for each retained extra family",
            "first_source_to_extend": str(SOURCES["parent_hessian_3093"]),
            "why_priority": "extra pole silence cannot be claimed without this",
            "valid_for_claim": False,
        },
        {
            "queue_id": "MIQ3407_4_boundary_zero_mode",
            "needed": "fix self-adjoint boundary class and classify ker H as gauge versus physical hair",
            "first_source_to_extend": str(SOURCES["contract_3406"]),
            "why_priority": "zero/edge modes can invalidate the pole count",
            "valid_for_claim": False,
        },
    ]


def bound_fallback() -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(SOURCES["bound_3406"]):
        rows.append({
            "fallback_id": "BF3407_" + row["bound_id"].split("_")[-1],
            "quantity": row["quantity"],
            "bound_formula": row["bound_formula"],
            "required_inputs": row["required_inputs"],
            "trigger": "activate if corresponding H_AB/R/J source rows remain unavailable",
            "status": "NOT_SCORE_READY",
            "valid_for_claim": False,
        })
    return rows


def selector_impact() -> list[dict[str, Any]]:
    return [
        {
            "impact_id": "SI3407_0_EH_selector",
            "result": "3407 does not promote the EH selector; it prevents formula-grade rows from being overcounted",
            "reason": "no claim-ready H_AB/R/J table exists yet",
            "next_decision": "derive source rows or switch to residue-bound pack",
            "valid_for_claim": False,
        },
        {
            "impact_id": "SI3407_1_Maxwell_EM",
            "result": "Maxwell/Poynting stress has the correct Hilbert-source slot conditionally",
            "reason": "3340 includes public Maxwell/Hodge route, but parent adoption/Hodge/current normalization remain unsigned",
            "next_decision": "if deriving J_A, include EM stress in T_total rather than boundary shadow flux",
            "valid_for_claim": False,
        },
        {
            "impact_id": "SI3407_2_local_tests",
            "result": "PPN/R10/orbital tests cannot be scored from H_AB/R/J yet",
            "reason": "pole residues are not computable from candidate anchors",
            "next_decision": "prepare fallback bound rows only after refusing unsourced residues",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3407_0_table_written",
            "claim": "minimal H_AB/R/J source table exists",
            "gate_pass": True,
            "reason": "candidate table and claim-ready table are written separately",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3407_1_claim_ready_HRJ",
            "claim": "claim-ready H_AB/R/J rows exist for public pole residues",
            "gate_pass": False,
            "reason": "all claim-ready rows remain false; candidates are formula/anchor/conditional only",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3407_2_TT_rank",
            "claim": "TT-only long-range rank is proven",
            "gate_pass": False,
            "reason": "public pole residues cannot yet be evaluated",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3407_3_EH_selector",
            "claim": "EH selector is parent-signed",
            "gate_pass": False,
            "reason": "depends on claim-ready HRJ rows and TT-only pole test",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3407_0_progress",
            "finding": "the HRJ ingredients are now separated into candidate anchors versus claim-ready source rows",
            "reason": "EH action, Hilbert source and G_pub formulas exist, but not as a complete parent-owned residue table",
            "next_action": "attempt direct derivation of H_hh/R_h/J_h first, because it is the minimum GR pole row",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3407_1_no_claim",
            "finding": "the current corpus still cannot evaluate public pole residues",
            "reason": "parent H_AB entries, R maps, source covectors, boundary class and zero-mode class are not signed together",
            "next_action": "either fill the minimum GR pole row or move to derivative-order residue bounds",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3407_2_best_next",
            "finding": "best next target is the minimum GR pole row derivation",
            "reason": "if H_hh/R_h/J_h closes, the massless Newton pole is anchored; then extra residues can be zeroed or bounded relative to it",
            "next_action": "build 3408 minimum-GR-pole row derivation, then fallback to non-EH bound pack if it fails",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3408-Y5-R2FR-minimum-GR-pole-Hhh-Rh-Jh-derivation-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3408_minimum_GR_pole_Hhh_Rh_Jh_derivation.py",
            "objective": "try to derive the minimum massless metric pole row: H_hh, R_h, J_h and common G_ref from parent action/source/readout clauses",
            "why_next": "this is the smallest constructive row that can anchor Newton/GR before extra modes are bounded",
            "valid_for_claim": False,
        },
        {
            "target_id": "3409-Y5-R2FR-nonEH-residue-bound-pack-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3409_nonEH_residue_bound_pack.py",
            "objective": "turn all nonclaim extra-mode HRJ gaps into no-cancellation R10/PPN/clock/orbital bound rows",
            "why_next": "this is the honest fallback if the minimum GR pole row cannot be parent-signed",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3407_0_scope",
            "check": "writes only 3407 files under post-checkpoint-work",
            "status": "PASS_IF_VALIDATION_TRUE",
            "valid_for_claim": False,
        },
        {
            "runner_id": "RUN3407_1_refusal",
            "check": "candidate anchors are not promoted to claim-ready HRJ rows",
            "status": "NONCLAIM_REFUSAL_ACTIVE",
            "valid_for_claim": False,
        },
        {
            "runner_id": "RUN3407_2_forward",
            "check": "next target derives the minimum GR pole row instead of rescanning generic gaps",
            "status": "FORWARD_DERIVATION_ROUTE",
            "valid_for_claim": False,
        },
    ]


def validation(outputs: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        rows.append({"check_id": check_id, "check": check, "passed": bool(passed), "detail": detail})

    generated_paths = [str(path) for path in OUTPUTS.values()] + [str(DOC)]
    all_nonclaim = all(
        str(row.get("valid_for_claim", False)).lower() == "false"
        for name, table in outputs.items()
        if name != "validation"
        for row in table
    )
    no_claim_ready = not any(str(row.get("claim_ready", False)).lower() == "true" for row in outputs["candidate_source_table"] + outputs["claim_ready_table"] + outputs["pole_readiness"])

    add("VAL3407_0_sources", "all registered sources exist", all(row["exists"] for row in outputs["source_register"]), f"sources={len(outputs['source_register'])}")
    add("VAL3407_1_requirements", "minimal HRJ requirements written", len(outputs["minimal_requirements"]) >= 7, "")
    add("VAL3407_2_candidates", "candidate HRJ source table written", len(outputs["candidate_source_table"]) >= 7, "")
    add("VAL3407_3_claim_ready_refusal", "no candidate is claim-ready", no_claim_ready, "")
    add("VAL3407_4_refusal_rules", "refusal rules written", len(outputs["refusal_rules"]) >= 5, "")
    add("VAL3407_5_pole_readiness", "public pole readiness table written", len(outputs["pole_readiness"]) >= 4, "")
    add("VAL3407_6_missing_queue", "missing H/R/J queue written", len(outputs["missing_input_queue"]) >= 5, "")
    add("VAL3407_7_gates", "TT-rank/EH-selector gates remain blocked", not any(row["gate_pass"] for row in outputs["promotion_gates"] if row["gate_id"] in {"GATE3407_1_claim_ready_HRJ", "GATE3407_2_TT_rank", "GATE3407_3_EH_selector"}), "")
    add("VAL3407_8_no_overclaim", "all generated rows are nonclaim", all_nonclaim, "")
    add("VAL3407_9_scope", "no 3407 output path targets formalization-workbench", "formalization-workbench" not in "\n".join(generated_paths), "")
    add("VAL3407_10_next", "next target derives minimum GR pole row", any("minimum-GR-pole" in row["target_id"] for row in outputs["next_target"]), "")
    overall = all(row["passed"] for row in rows)
    add("VAL3407_11_overall", "3407 validation overall", overall, "all required checks passed" if overall else "one or more checks failed")
    return rows


def write_doc(outputs: dict[str, list[dict[str, Any]]]) -> None:
    parts = [
        "# 3407 - Y5/R2FR minimal parent Hessian source table under AX1090",
        "",
        "## Verdict",
        "",
        "- 3407 builds the minimal `H_AB/R/J_A` table needed for public pole residues, but it does not promote any row to claim-ready.",
        "- The useful result is separation: EH action, Hilbert source, and `G_pub=R H^{-1} R^T` are formula/candidate anchors; they are not yet a parent-owned residue table.",
        "- Maxwell/Poynting stress belongs in the Hilbert source covector conditionally, not as a hidden boundary/source shadow.",
        "- The next constructive move is the minimum GR pole row: derive `H_hh`, `R_h`, `J_h`, common `G_ref`, and boundary/gauge class together.",
        "",
        "## Minimal HRJ Requirements",
        md_table(outputs["minimal_requirements"]),
        "",
        "## Candidate HRJ Source Table",
        md_table(outputs["candidate_source_table"]),
        "",
        "## Claim-Ready HRJ Table",
        md_table(outputs["claim_ready_table"]),
        "",
        "## Refusal Rules",
        md_table(outputs["refusal_rules"]),
        "",
        "## Public Pole Readiness",
        md_table(outputs["pole_readiness"]),
        "",
        "## Missing Input Queue",
        md_table(outputs["missing_input_queue"]),
        "",
        "## Bound Fallback Queue",
        md_table(outputs["bound_fallback"]),
        "",
        "## Selector Impact",
        md_table(outputs["selector_impact"]),
        "",
        "## Promotion Gates",
        md_table(outputs["promotion_gates"]),
        "",
        "## Decision Ledger",
        md_table(outputs["decision_ledger"]),
        "",
        "## Next Target",
        md_table(outputs["next_target"]),
        "",
        "## Validation",
        md_table(outputs["validation"]),
        "",
    ]
    DOC.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "minimal_requirements": minimal_requirements(),
        "candidate_source_table": candidate_source_table(),
        "claim_ready_table": claim_ready_table(),
        "refusal_rules": refusal_rules(),
        "pole_readiness": pole_readiness(),
        "missing_input_queue": missing_input_queue(),
        "bound_fallback": bound_fallback(),
        "selector_impact": selector_impact(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    outputs["validation"] = validation(outputs)
    for key, path in OUTPUTS.items():
        write_csv(path, outputs[key])
    write_doc(outputs)

    if not all(row["passed"] for row in outputs["validation"]):
        raise RuntimeError("3407 validation failed")

    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUTS)} CSV outputs under {OUT}")
    print("; ".join(f"{path.name}={len(outputs[key])}" for key, path in OUTPUTS.items()))


if __name__ == "__main__":
    main()
