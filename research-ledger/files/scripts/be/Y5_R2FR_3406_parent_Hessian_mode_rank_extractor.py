from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3406-Y5-R2FR-parent-Hessian-mode-rank-extractor-under-AX1090.md"

SOURCES = {
    "doc_3405": ROOT / "3405-Y5-R2FR-parent-normal-form-EH-selector-proof-attempt-under-AX1090.md",
    "doc_3404": ROOT / "3404-Y5-R2FR-source-calibrated-EH-parent-ownership-audit-under-AX1090.md",
    "next_3405": OUT / "P8_Y5_R2FR_3405_NEXT_TARGET.csv",
    "hyp_3405": OUT / "P8_Y5_R2FR_3405_PARENT_NORMAL_FORM_HYPOTHESES.csv",
    "spin_3405": OUT / "P8_Y5_R2FR_3405_SPIN2_BOOTSTRAP_ROUTE.csv",
    "result_3405": OUT / "P8_Y5_R2FR_3405_SELECTOR_RESULT.csv",
    "bound_3405": OUT / "P8_Y5_R2FR_3405_DERIVATIVE_ORDER_BOUND_LAW.csv",
    "hessian_3093": OUT / "P8_Y5_R2FR_3093_PARENT_HESSIAN_AUDIT.csv",
    "hessian_3316": OUT / "P8_Y5_R2FR_3316_HESSIAN_READOUT_DERIVATION.csv",
    "hessian_3317": OUT / "P8_Y5_R2FR_3317_MINIMAL_HESSIAN_FORMULA.csv",
    "effective_3174": OUT / "P8_Y5_R2FR_3174_EFFECTIVE_HESSIAN_EXTRACTION.csv",
    "projection_3179": OUT / "P8_Y5_R2FR_3179_HESSIAN_PROJECTION_DERIVATION.csv",
    "rank_3201": OUT / "P8_Y5_R2FR_3201_SOURCE_RANK_SEPARATION_LEMMA.csv",
    "coercivity_3202": OUT / "P8_Y5_R2FR_3202_COERCIVITY_AND_ZERO_MODE_GATE.csv",
    "mode_mass_3302": OUT / "P8_Y5_R2FR_3302_LINEARIZED_MODE_MASS_MAP.csv",
    "r11_beta": OUT / "P8_Y5_R11_BETA_COMPONENT_VECTOR.csv",
    "local_eh_r11": OUT / "P8_LOCAL_EH_R11_OPERATOR_AUDIT.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3406_SOURCE_REGISTER.csv",
    "hessian_extractor_contract": OUT / "P8_Y5_R2FR_3406_HESSIAN_EXTRACTOR_CONTRACT.csv",
    "mode_rank_theorem": OUT / "P8_Y5_R2FR_3406_MODE_RANK_THEOREM.csv",
    "public_propagator_tests": OUT / "P8_Y5_R2FR_3406_PUBLIC_PROPAGATOR_TESTS.csv",
    "minimal_two_channel_law": OUT / "P8_Y5_R2FR_3406_MINIMAL_TWO_CHANNEL_HESSIAN_LAW.csv",
    "mode_family_triage": OUT / "P8_Y5_R2FR_3406_MODE_FAMILY_TRIAGE.csv",
    "hessian_input_status": OUT / "P8_Y5_R2FR_3406_HESSIAN_INPUT_STATUS.csv",
    "residue_bound_interface": OUT / "P8_Y5_R2FR_3406_RESIDUE_BOUND_INTERFACE.csv",
    "selector_impact": OUT / "P8_Y5_R2FR_3406_SELECTOR_IMPACT.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3406_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3406_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3406_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3406_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3406_VALIDATION.csv",
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
        "hyp_3405": "parent normal-form hypotheses whose mode-rank premise 3406 tests",
        "spin_3405": "spin-2 bootstrap route requiring parent Hessian/mode-rank extraction",
        "hessian_3093": "parent Hessian audit identifying missing extremum/sign/mass/source rows",
        "hessian_3316": "invariant public propagator formula G_pub=R H^{-1} R^T",
        "hessian_3317": "minimal two-channel Hessian law and finite-pole conditions",
        "effective_3174": "effective metric Hessian extraction from open-system scaffold",
        "coercivity_3202": "coercivity and zero-mode gates",
        "mode_mass_3302": "linearized R2/Ricci/Weyl mode mass templates",
        "r11_beta": "R11 operator families to triage by pole/residue",
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


def hessian_extractor_contract() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "HEX3406_0_stationary_branch",
            "object": "first variation",
            "required_identity": "F_A := delta S_parent/delta Phi^A |_{Phi0}=0 modulo q-basic gauge and fixed boundary terms",
            "why_needed": "a Hessian/mode count around a non-extremal branch is not a physical local vacuum spectrum",
            "current_evidence": "3093 marks branch extremum missing for extra Xhat rows",
            "status": "NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "contract_id": "HEX3406_1_parent_Hessian",
            "object": "quadratic parent action",
            "required_identity": "S_2=1/2 int delta Phi^A H_AB(k) delta Phi^B + 1/2 int T^{mn} R_{mn,A}(k) delta Phi^A",
            "why_needed": "H_AB and readout map R define the physical pole/residue spectrum without field-redefinition games",
            "current_evidence": "3316 derives the formula but not the entries",
            "status": "FORMULA_DERIVED_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "contract_id": "HEX3406_2_public_metric_propagator",
            "object": "observable exchange",
            "required_identity": "G_pub_{mnab}(k)=R_{mn,A}(k)[H^{-1}(k)]^{AB}R_{ab,B}(k)",
            "why_needed": "the local tests see public metric exchange, not arbitrary field labels Z_i and U_i",
            "current_evidence": "3316 exact readout derivation",
            "status": "INVARIANT_FORMULA_DERIVED",
            "valid_for_claim": False,
        },
        {
            "contract_id": "HEX3406_3_massless_spin2_pole",
            "object": "TT spin-2 residue",
            "required_identity": "G_pub = G_ref P^(2)/k^2 + analytic/contact + no extra long-range pole",
            "why_needed": "this is the concrete parent-Hessian version of 'only massless spin-2 is long-range'",
            "current_evidence": "3405 states target; no parent Hessian pole extraction exists",
            "status": "TARGET_NOT_EXTRACTED",
            "valid_for_claim": False,
        },
        {
            "contract_id": "HEX3406_4_extra_mode_residues",
            "object": "scalar/vector/connection/domain/bulk residues",
            "required_identity": "for each extra pole i: B_i=Res_i(T_s G_pub T_t)/Res_GR is zero, gapped-and-bounded, or source/readout silent",
            "why_needed": "an extra field is harmless only if its observable residue is zero/below locks, not merely renamed",
            "current_evidence": "3316 residue-ratio formula; R11 rows lack H_AB/R entries",
            "status": "RESIDUE_FORMULA_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "contract_id": "HEX3406_5_gauge_and_zero_modes",
            "object": "nullspace classification",
            "required_identity": "ker H = q-basic diffeomorphism gauge only; edge/domain zero modes have zero charge or are fixed",
            "why_needed": "extra zero modes are long-range hair unless first-class gauge or boundary-silent",
            "current_evidence": "2858/3202 mark constraint class, boundary charge and zero modes open",
            "status": "ZERO_MODE_AUDIT_OPEN",
            "valid_for_claim": False,
        },
        {
            "contract_id": "HEX3406_6_self_adjoint_boundary",
            "object": "boundary class",
            "required_identity": "H is self-adjoint on the local compact exterior with fixed annulus/reference and no unsourced flux",
            "why_needed": "pole/rank extraction is meaningless if boundary flux supplies hidden physical modes",
            "current_evidence": "3202 and 3403 retain boundary/reference gates",
            "status": "BOUNDARY_CLASS_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
    ]


def mode_rank_theorem() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "MRT3406_0_invariant_spectrum",
            "statement": "The physically relevant local spectrum is the pole/residue decomposition of G_pub=R H^{-1} R^T.",
            "proof": "Under nonsingular field redefinitions Phi->M Phi, H->M^T H M and R->R M, so R H^{-1} R^T is unchanged.",
            "result": "mode-rank must be read from public exchange poles, not from chosen variable names",
            "status": "DERIVED_FROM_3316",
            "valid_for_claim": False,
        },
        {
            "step_id": "MRT3406_1_TT_rank_condition",
            "statement": "If G_pub has one positive massless spin-2 pole and no scalar/vector/connection/domain long-range pole with nonzero residue, then PNF3405_1 is signed.",
            "proof": "The long-range phase space seen by matter/readout contains only the two TT polarizations of the public metric. Gauge zero modes are quotient redundancies and do not count.",
            "result": "the spin-2 bootstrap route in 3405 becomes active",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": False,
        },
        {
            "step_id": "MRT3406_2_extra_pole_no_go",
            "statement": "A nonzero extra pole residue in G_pub blocks local-GR promotion unless it is bounded below the relevant local tests.",
            "proof": "Any extra pole changes the two-source exchange, yielding finite-range, PPN, WEP, clock or preferred-frame signatures depending on spin and coupling.",
            "result": "extra modes become explicit residual rows instead of hidden closure assumptions",
            "status": "OBSTRUCTION_THEOREM",
            "valid_for_claim": False,
        },
        {
            "step_id": "MRT3406_3_current_verdict",
            "statement": "The current corpus has the invariant formula and several conditional toy laws, but no parent-owned H_AB/R extraction sufficient to prove TT-only rank.",
            "proof": "3093, 3316, 3317 and 3405 all keep parent Hessian entries, source/readout residues, zero-mode class and boundary class unsigned.",
            "result": "mode-rank is not claimed; the next task is to source or symbolically derive H_AB and R blocks",
            "status": "NOT_CLAIM_LEVEL",
            "valid_for_claim": False,
        },
    ]


def public_propagator_tests() -> list[dict[str, Any]]:
    return [
        {
            "test_id": "PPT3406_0_field_redefinition",
            "test": "G_pub invariance under Phi -> M Phi",
            "formula": "R H^{-1} R^T = (R M)(M^T H M)^{-1}(M^T R^T)",
            "pass_condition": "identity holds algebraically",
            "current_status": "PASS_FORMAL",
            "valid_for_claim": False,
        },
        {
            "test_id": "PPT3406_1_massless_pole",
            "test": "positive GR pole",
            "formula": "Res_{k^2=0}[T G_pub T] = G_ref T P^(2) T",
            "pass_condition": "positive residue, correct Hilbert source, same G_ref",
            "current_status": "FORMULA_READY_RESIDUE_NOT_EXTRACTED",
            "valid_for_claim": False,
        },
        {
            "test_id": "PPT3406_2_scalar_residue",
            "test": "extra scalar pole silence",
            "formula": "B_0 = Res_{k^2=-m_0^2}[T G_pub T]_{scalar}/Res_GR",
            "pass_condition": "B_0=0, m_0 infinite, or finite-range/PPN bound pass",
            "current_status": "R2_FR_SCALAR_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "test_id": "PPT3406_3_spin2_ghost_residue",
            "test": "massive spin-2/Weyl pole silence",
            "formula": "B_2 = Res_{k^2=-m_2^2}[T G_pub T]_{massive spin2}/Res_GR",
            "pass_condition": "B_2=0 or bounded; sign/ghost handled by parent stability",
            "current_status": "RICCI_WEYL_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "test_id": "PPT3406_4_zero_mode_charge",
            "test": "nullspace is gauge not hair",
            "formula": "v in ker H => R v=0 and J v=0 unless v is q-basic diffeo gauge",
            "pass_condition": "no physical zero mode with source/readout overlap",
            "current_status": "ZERO_MODE_CLASS_OPEN",
            "valid_for_claim": False,
        },
    ]


def minimal_two_channel_law() -> list[dict[str, Any]]:
    return [
        {
            "law_id": "M2H3406_0_ansatz",
            "statement": "For Phi=(h,x), a minimal public Hessian test has H(p)=[[a p, b0+b1 p],[b0+b1 p, M2+z p]], R=(1,u), p=k^2.",
            "consequence": "This is the smallest algebraic model that can fake or spoil a GR pole.",
            "source": str(SOURCES["hessian_3317"]),
            "valid_for_claim": False,
        },
        {
            "law_id": "M2H3406_1_massless_condition",
            "statement": "D(0)=-b0^2, so a GR-like massless pole at p=0 requires b0=0.",
            "consequence": "constant h-x mixing must be forbidden by symmetry/constraint, not fitted away.",
            "source": str(SOURCES["hessian_3317"]),
            "valid_for_claim": False,
        },
        {
            "law_id": "M2H3406_2_finite_pole",
            "statement": "After b0=0, D(p)=p[a M2+(a z-b1^2)p] and p_f=-a M2/(a z-b1^2).",
            "consequence": "derivative mixing generically creates a finite pole unless absent, unobserved, or bounded.",
            "source": str(SOURCES["hessian_3317"]),
            "valid_for_claim": False,
        },
        {
            "law_id": "M2H3406_3_public_residue",
            "statement": "A finite pole is physical only if R adj(H) R^T is nonzero at p_f.",
            "consequence": "source/readout silence is a residue theorem, not a variable-name theorem.",
            "source": str(SOURCES["hessian_3317"]),
            "valid_for_claim": False,
        },
    ]


def mode_family_triage() -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(SOURCES["r11_beta"]):
        family = row["operator_family"]
        if family in {"R2_fR_scalar_mode", "scalar_tensor_class_metric"}:
            mode_channel = "spin0_scalar"
            required_hessian_test = "scalar pole residue B_0=0/gapped/bounded in G_pub"
        elif family in {"Ricci_Weyl_squared"}:
            mode_channel = "massive_spin2_or_four_derivative"
            required_hessian_test = "massive spin-2 pole residue B_2=0/bounded and stability sign handled"
        elif family in {"torsion_nonmetricity"}:
            mode_channel = "connection"
            required_hessian_test = "connection Hessian algebraic/gauge or zero source/readout residue"
        elif family in {"vector_preferred_frame"}:
            mode_channel = "spin1_preferred_frame"
            required_hessian_test = "vector pole absent/aligned/gapped and alpha_i residues below locks"
        elif family in {"nonlocal_memory_kernel", "bulk_X_force_law", "projector_domain_stress"}:
            mode_channel = "extra_domain_bulk_memory"
            required_hessian_test = "kernel/domain/bulk pole absent, massive, source-silent or bounded"
        elif family in {"boundary_topological_terms"}:
            mode_channel = "edge_boundary"
            required_hessian_test = "edge zero mode fixed/topological/source-blind or explicit boundary residue bound"
        else:
            mode_channel = "source_readout_q_loc"
            required_hessian_test = "same source/readout residue and q_loc projection split"
        rows.append({
            "operator_id": row["component_id"],
            "operator_family": family,
            "mode_channel": mode_channel,
            "required_hessian_test": required_hessian_test,
            "current_status": row["status"],
            "claim_ready": False,
            "valid_for_claim": False,
        })
    return rows


def hessian_input_status() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "HIS3406_0_HAB",
            "needed_input": "symbolic parent Hessian block H_AB(k) around the local branch",
            "available_now": "formula for use exists; actual parent entries not extracted",
            "best_source": str(SOURCES["hessian_3316"]),
            "status": "MISSING_PARENT_ENTRIES",
            "valid_for_claim": False,
        },
        {
            "input_id": "HIS3406_1_Rmap",
            "needed_input": "public metric readout derivative R_{mn,A}=delta g_pub_mn/delta Phi^A",
            "available_now": "identity candidate for effective v1 metric; same observed coframe unsigned",
            "best_source": str(SOURCES["effective_3174"]),
            "status": "PARTIAL_READOUT_CANDIDATE",
            "valid_for_claim": False,
        },
        {
            "input_id": "HIS3406_2_Jsource",
            "needed_input": "source covector J_A from descended Hilbert matter/EM action",
            "available_now": "Hilbert source clause conditional; not parent-signed for all sectors",
            "best_source": str(SOURCES["doc_3404"]),
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "input_id": "HIS3406_3_gauge_kernel",
            "needed_input": "classification of ker H into q-basic diffeo gauge versus physical zero modes",
            "available_now": "degree-count audits mark constraint class and boundary charge open",
            "best_source": str(SOURCES["coercivity_3202"]),
            "status": "ZERO_MODE_CLASS_OPEN",
            "valid_for_claim": False,
        },
        {
            "input_id": "HIS3406_4_boundary_domain",
            "needed_input": "self-adjoint boundary/domain class for H and no unsourced edge charge",
            "available_now": "conditional coercivity and zero-mode gates, no parent boundary certificate",
            "best_source": str(SOURCES["coercivity_3202"]),
            "status": "BOUNDARY_CERTIFICATE_MISSING",
            "valid_for_claim": False,
        },
        {
            "input_id": "HIS3406_5_residue_units",
            "needed_input": "common units/sign convention for residue ratios B_i against G_ref",
            "available_now": "3316 ratio formula; no source-backed residues",
            "best_source": str(SOURCES["hessian_3316"]),
            "status": "NORMALIZATION_FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
    ]


def residue_bound_interface() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "RBI3406_0_spin0",
            "quantity": "B_0(lambda_0)",
            "bound_formula": "|B_0| <= min(PPN_gamma_scalar, beta_scalar, R10_alpha(lambda_0), clock/WEP if sourced)",
            "required_inputs": "scalar pole mass, residue sign, source/readout overlap, screening/local profile",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "RBI3406_1_massive_spin2",
            "quantity": "B_2(lambda_2)",
            "bound_formula": "|B_2| <= min(PPN_gamma_beta, finite-range spin2, stability/ghost exclusion)",
            "required_inputs": "Weyl/Ricci coefficient, massive spin2 pole, residue, sign/stability rule",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "RBI3406_2_connection",
            "quantity": "B_conn",
            "bound_formula": "|B_conn| <= min(clock, WEP, lightcone, spin, PPN connection projections)",
            "required_inputs": "torsion/nonmetricity Hessian, hypermomentum/source coupling, readout overlap",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "RBI3406_3_domain_memory_bulk",
            "quantity": "B_X(lambda_X)",
            "bound_formula": "|B_X| <= |R_X H_X^{-1} J_X| / |R_h H_h^{-1} J_h| and arena-specific locks",
            "required_inputs": "H_X, R_X, J_X, boundary flux, local profile and arena projection",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": False,
        },
    ]


def selector_impact() -> list[dict[str, Any]]:
    return [
        {
            "impact_id": "SIM3406_0_EH_selector",
            "target": "PNF3405_1 mode-rank premise",
            "if_3406_passes": "parent owns TT-only long-range mode rank; 3405 EH selector can promote to the next source/readout gates",
            "if_3406_fails": "non-EH residual bound pack is mandatory",
            "current_result": "FORMULA_READY_NOT_EXTRACTED",
            "valid_for_claim": False,
        },
        {
            "impact_id": "SIM3406_1_beta_gamma",
            "target": "beta/gamma metric core",
            "if_3406_passes": "extra scalar/four-derivative metric poles are zero; EH beta/gamma core becomes parent-owned conditional on source/readout",
            "if_3406_fails": "scalar/Ricci/Weyl residues must be scored against PPN/R10",
            "current_result": "BLOCKED_BY_HAB_RMAP_INPUTS",
            "valid_for_claim": False,
        },
        {
            "impact_id": "SIM3406_2_q_loc",
            "target": "q_loc preferred-frame vector",
            "if_3406_passes": "q_loc can be treated as residual divergence of owned sectors; still needs projection split",
            "if_3406_fails": "q_loc remains separate beta/alpha_i/xi danger",
            "current_result": "PROJECTION_SPLIT_STILL_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "impact_id": "SIM3406_3_EM_Maxwell",
            "target": "Maxwell/Poynting Hilbert stress",
            "if_3406_passes": "EM stress lives in source covector J_A through same public metric exchange",
            "if_3406_fails": "hidden Hodge/current readout residues remain explicit source-sector tests",
            "current_result": "SOURCE_COVECTOR_CONDITIONAL",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3406_0_public_formula",
            "claim": "invariant public Hessian propagator formula is available",
            "gate_pass": True,
            "reason": "3316 and 3406 use G_pub=R H^{-1} R^T",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3406_1_parent_HAB",
            "claim": "parent Hessian H_AB and readout R are extracted from MTS parent action",
            "gate_pass": False,
            "reason": "formula exists but entries/source maps remain missing or conditional",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3406_2_TT_only",
            "claim": "only long-range public mode is positive massless spin-2",
            "gate_pass": False,
            "reason": "extra scalar/vector/connection/domain residues are not proven zero or bounded",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3406_3_EH_selector",
            "claim": "3405 EH selector is parent-signed",
            "gate_pass": False,
            "reason": "mode-rank premise remains unextracted",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3406_4_local_GR",
            "claim": "local GR/PPN is derived",
            "gate_pass": False,
            "reason": "requires EH selector plus source/readout/q_loc vector gates",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3406_0_progress",
            "finding": "the mode-rank test is now concrete and field-redefinition invariant",
            "reason": "local tests see pole residues of G_pub=R H^{-1} R^T, not arbitrary Z_i/U_i labels",
            "next_action": "source or symbolically derive the actual parent H_AB and R blocks",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3406_1_verdict",
            "finding": "current corpus does not yet prove TT-only long-range rank",
            "reason": "parent Hessian entries, readout derivative, source covector, zero-mode class and boundary class remain unsigned",
            "next_action": "do not claim EH selector; build a minimal Hessian source table or go to residual bounds",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3406_2_best_next",
            "finding": "best next target is the minimal parent-Hessian input pack",
            "reason": "without H_AB/R/J rows, every later PPN/R10 bound is just a placeholder; with them, the EH selector can be scored cleanly",
            "next_action": "construct 3407 minimal H_AB/R/J source table and refuse unsourced entries",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3407-Y5-R2FR-minimal-parent-Hessian-source-table-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3407_minimal_parent_Hessian_source_table.py",
            "objective": "construct the minimal source-backed H_AB, R_mn,A and J_A table required to evaluate G_pub pole residues",
            "why_next": "this is the first non-circular way to decide whether the parent really has only the TT spin-2 public pole",
            "valid_for_claim": False,
        },
        {
            "target_id": "3408-Y5-R2FR-derivative-order-residue-bound-pack-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3408_derivative_order_residue_bound_pack.py",
            "objective": "if H_AB/R/J cannot be sourced, convert all surviving non-EH pole channels into no-cancellation empirical bound rows",
            "why_next": "this is the honest fallback if the derivation route cannot currently close",
            "valid_for_claim": False,
        },
        {
            "target_id": "3409-Y5-R2FR-q_loc-U2-alpha-vector-projection-split-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3409_q_loc_U2_alpha_vector_projection_split.py",
            "objective": "separate q_loc beta, alpha_i/alpha3 and xi projections after the Hessian-mode fork",
            "why_next": "q_loc remains the highest-danger vector guard once the spin-2 pole story is clarified",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3406_0_scope",
            "check": "writes only 3406 files under post-checkpoint-work",
            "status": "PASS_IF_VALIDATION_TRUE",
            "valid_for_claim": False,
        },
        {
            "runner_id": "RUN3406_1_nonclaim",
            "check": "public propagator formula may be derived, but TT-only rank is not claimed",
            "status": "NONCLAIM_EXTRACTOR",
            "valid_for_claim": False,
        },
        {
            "runner_id": "RUN3406_2_forward",
            "check": "next target asks for actual H_AB/R/J source rows rather than another generic blocker list",
            "status": "FORWARD_INPUT_PACK",
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

    add("VAL3406_0_sources", "all registered sources exist", all(row["exists"] for row in outputs["source_register"]), f"sources={len(outputs['source_register'])}")
    add("VAL3406_1_contract", "Hessian extractor contract written", len(outputs["hessian_extractor_contract"]) >= 7, "")
    add("VAL3406_2_theorem", "mode-rank theorem written", any("G_pub=R H^{-1} R^T" in row["statement"] for row in outputs["mode_rank_theorem"]), "")
    add("VAL3406_3_propagator", "public propagator tests written", len(outputs["public_propagator_tests"]) >= 5, "")
    add("VAL3406_4_two_channel", "minimal two-channel Hessian law written", len(outputs["minimal_two_channel_law"]) >= 4, "")
    add("VAL3406_5_triage", "R11 mode families triaged", len(outputs["mode_family_triage"]) >= 12, "")
    add("VAL3406_6_inputs", "Hessian input status records missing H_AB/R/J", any(row["status"] == "MISSING_PARENT_ENTRIES" for row in outputs["hessian_input_status"]), "")
    add("VAL3406_7_gates", "TT-only/local-GR gates remain blocked", not any(row["gate_pass"] for row in outputs["promotion_gates"] if row["gate_id"] in {"GATE3406_1_parent_HAB", "GATE3406_2_TT_only", "GATE3406_3_EH_selector", "GATE3406_4_local_GR"}), "")
    add("VAL3406_8_no_overclaim", "all generated rows are nonclaim", all_nonclaim, "")
    add("VAL3406_9_scope", "no 3406 output path targets formalization-workbench", "formalization-workbench" not in "\n".join(generated_paths), "")
    add("VAL3406_10_next", "next target is minimal parent-Hessian source table", any("minimal-parent-Hessian-source-table" in row["target_id"] for row in outputs["next_target"]), "")
    overall = all(row["passed"] for row in rows)
    add("VAL3406_11_overall", "3406 validation overall", overall, "all required checks passed" if overall else "one or more checks failed")
    return rows


def write_doc(outputs: dict[str, list[dict[str, Any]]]) -> None:
    parts = [
        "# 3406 - Y5/R2FR parent Hessian mode-rank extractor under AX1090",
        "",
        "## Verdict",
        "",
        "- 3406 turns the spin-2/EH selector into a concrete parent-Hessian pole test.",
        "- The invariant object is `G_pub = R H^{-1} R^T`: local tests see public metric pole residues, not field-label choices like `Z_i` and `U_i` separately.",
        "- The current corpus has the formula and useful toy laws, but it does not yet supply the parent `H_AB`, readout derivative `R`, source covector `J_A`, zero-mode class, or boundary class needed to prove TT-only rank.",
        "- Therefore the EH selector is not claimed. The next non-circular move is a minimal source table for `H_AB/R/J`; the fallback is a residue-bound pack for surviving non-EH poles.",
        "",
        "## Hessian Extractor Contract",
        md_table(outputs["hessian_extractor_contract"]),
        "",
        "## Mode-Rank Theorem",
        md_table(outputs["mode_rank_theorem"]),
        "",
        "## Public Propagator Tests",
        md_table(outputs["public_propagator_tests"]),
        "",
        "## Minimal Two-Channel Hessian Law",
        md_table(outputs["minimal_two_channel_law"]),
        "",
        "## Mode Family Triage",
        md_table(outputs["mode_family_triage"]),
        "",
        "## Hessian Input Status",
        md_table(outputs["hessian_input_status"]),
        "",
        "## Residue Bound Interface",
        md_table(outputs["residue_bound_interface"]),
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
        "hessian_extractor_contract": hessian_extractor_contract(),
        "mode_rank_theorem": mode_rank_theorem(),
        "public_propagator_tests": public_propagator_tests(),
        "minimal_two_channel_law": minimal_two_channel_law(),
        "mode_family_triage": mode_family_triage(),
        "hessian_input_status": hessian_input_status(),
        "residue_bound_interface": residue_bound_interface(),
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
        raise RuntimeError("3406 validation failed")

    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUTS)} CSV outputs under {OUT}")
    print("; ".join(f"{path.name}={len(outputs[key])}" for key, path in OUTPUTS.items()))


if __name__ == "__main__":
    main()
