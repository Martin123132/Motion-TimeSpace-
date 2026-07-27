from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1399-Y5-R10-RAB-gauge-level-index-owner-for-lambdaA-or-finite-alphaEM-prior-vector.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1399_SOURCE_REGISTER.csv"
OWNER_AUDIT_PATH = SRC_DIR / "P8_Y5_R10_1399_GAUGE_LEVEL_INDEX_OWNER_AUDIT.csv"
THEOREM_ATTEMPT_PATH = SRC_DIR / "P8_Y5_R10_1399_LEVEL_OWNER_THEOREM_ATTEMPT.csv"
OWNER_VECTOR_PATH = SRC_DIR / "P8_Y5_R10_1399_LAMBDA_A_OWNER_VECTOR.csv"
FINITE_PRIOR_PATH = SRC_DIR / "P8_Y5_R10_1399_FINITE_ALPHAEM_PRIOR_VECTOR.csv"
ARENA_GATE_PATH = SRC_DIR / "P8_Y5_R10_1399_EM_COUPLING_ARENA_GATE.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1399_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1399_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1399_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1399_VALIDATION.csv"

STATUS = (
    "Y5_R10_1399_gauge_level_index_owner_not_found_"
    "lambda_A_finite_alphaEM_prior_vector_retained_nonclaim"
)
CLAIM_CEILING = (
    "gauge_level_index_owner_audit_only_no_lambda_A_zero_no_unique_F2_no_EM_lock_zero_"
    "no_alphaEM_bound_no_WEP_no_clock_no_R10_no_PPN_no_Newton_no_local_GR_pass"
)

SOURCE_ROWS = [
    {
        "source_id": "SRC1399_0_1398_doc",
        "source_path": "1398-Y5-R10-RAB-no-observed-counterterm-action-principle-or-lambdaA-prior-bound.md",
        "required_anchor": "NEXT1398_0_1399",
        "purpose": "handoff selecting gauge level/index owner or finite alphaEM prior vector",
    },
    {
        "source_id": "SRC1399_1_1398_contract",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1398_PARENT_ACTION_SELECTION_CONTRACT.csv",
        "required_anchor": "PAC1398_3_coefficient_owner",
        "purpose": "coefficient-owner clause after pullback no-go",
    },
    {
        "source_id": "SRC1399_2_1398_prior",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1398_LAMBDA_A_PRIOR_BOUND_VECTOR.csv",
        "required_anchor": "LAP1398_0_lambda_A",
        "purpose": "finite lambda_A prior vector to refine",
    },
    {
        "source_id": "SRC1399_3_643_doc",
        "source_path": "643-Y5-R10-alpha-normalization-owner-or-finite-coupling-bound-input-fill.md",
        "required_anchor": "AO643_5_parent_vertical_norm",
        "purpose": "owner-candidate matrix and selected parent vertical norm route",
    },
    {
        "source_id": "SRC1399_4_643_owner_matrix",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_643_OWNER_CANDIDATE_MATRIX.csv",
        "required_anchor": "AO643_1_Dirac_flux_monopole",
        "purpose": "prior candidate routes for alpha normalization owner",
    },
    {
        "source_id": "SRC1399_5_643_rescale",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_643_RESCALING_NO_GO.csv",
        "required_anchor": "RNG643_1_add_independent_F2",
        "purpose": "rescaling and independent F2 no-go",
    },
    {
        "source_id": "SRC1399_6_642_theorem",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_642_THEOREM_ZERO_ATTEMPT.csv",
        "required_anchor": "TA642_4_coupling_normalization",
        "purpose": "compact U1 does not fix g_EM/alpha_EM",
    },
    {
        "source_id": "SRC1399_7_288_doc",
        "source_path": "288-k9-Ward-index-level-attempt.md",
        "required_anchor": "Ward/index theorem exists",
        "purpose": "index/level theorem obstruction",
    },
    {
        "source_id": "SRC1399_8_332_doc",
        "source_path": "332-parent-Hamiltonian-trace-current-gate.md",
        "required_anchor": "Noether/Bianchi selects unit coefficient",
        "purpose": "Noether/Bianchi closure does not select coupling coefficient",
    },
    {
        "source_id": "SRC1399_9_765_counter",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_765_RESCALING_COUNTEREXAMPLE_LEDGER.csv",
        "required_anchor": "RCE765_0_lambda_F2",
        "purpose": "lambda_A remains the decisive counterexample",
    },
    {
        "source_id": "SRC1399_10_this_script",
        "source_path": "scripts/Y5_R10_RAB_gauge_level_index_owner_for_lambdaA_or_finite_alphaEM_prior_vector.py",
        "required_anchor": "STATUS",
        "purpose": "1399 generator",
    },
]


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").strip()


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str] | None = None) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    if columns is None:
        columns = list(rows[0].keys()) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: clean(row.get(column, "")) for column in columns})


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return ""
    if columns is None:
        columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(clean(row.get(column, "")).replace("|", "\\|") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def anchor_found(path: Path, anchor: str) -> bool:
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in SOURCE_ROWS:
        source_path = ROOT / source["source_path"]
        rows.append(
            {
                **source,
                "exists": str(source_path.exists()),
                "anchor_found": str(anchor_found(source_path, source["required_anchor"])),
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def owner_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "owner_id": "GLI1399_0_compact_U1_lattice",
            "candidate_owner": "compact U(1) charge lattice",
            "can_fix": "integer representation labels and relative charge sectors after a base unit exists",
            "cannot_fix": "continuous Maxwell kinetic normalization g_EM^{-2} or standalone lambda_A",
            "test": "A_mu and g_EM can still be rescaled with current/charge units unless T_Q norm and current owner are fixed",
            "status": "SUPPORT_ONLY_NOT_COUPLING_OWNER",
            "required_repair": "fixed base charge unit Q_star and generator norm tied to kinetic coefficient",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "owner_id": "GLI1399_1_Dirac_monopole_flux",
            "candidate_owner": "Dirac or flux quantization",
            "can_fix": "electric-magnetic charge product or flux period if magnetic/topological unit is parent-owned",
            "cannot_fix": "electric coupling alone without a fixed magnetic unit, hbar*c readout, and source normalization",
            "test": "eg=2*pi*n fixes a product; e remains deformable if g_m or flux unit floats",
            "status": "PROMISING_BUT_NOT_PARENT_SUPPLIED",
            "required_repair": "MTS parent magnetic flux unit and local readout silence",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "owner_id": "GLI1399_2_BF_Chern_Simons_level",
            "candidate_owner": "BF/Chern-Simons/topological level",
            "can_fix": "integer boundary response level or charge lattice coefficient",
            "cannot_fix": "4D Maxwell kinetic term unless a bulk-boundary theorem transfers the level into g_EM^{-2}",
            "test": "integer level k may quantize a topological term, while F^2 remains a metric kinetic term with continuous coefficient",
            "status": "LEVEL_DOES_NOT_CURRENTLY_FIX_4D_MAXWELL_KINETIC",
            "required_repair": "bulk inheritance theorem from topological level to observed Maxwell kinetic coefficient",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "owner_id": "GLI1399_3_anomaly_Ward_index",
            "candidate_owner": "anomaly cancellation or Ward/index theorem",
            "can_fix": "representation lattice, charge ratios, or an effective denominator/level",
            "cannot_fix": "low-energy alpha_EM unless the Ward/index theorem also owns the kinetic normalization",
            "test": "current conservation and anomaly cancellation constrain charges but do not by themselves select g_EM^{-2}",
            "status": "INDEX_OWNER_NOT_FOUND",
            "required_repair": "explicit operator/complex/anomaly with fixed index and coefficient map to Maxwell F2",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "owner_id": "GLI1399_4_KK_radius_volume",
            "candidate_owner": "Kaluza-Klein radius or compactification volume",
            "can_fix": "g_EM if the compact radius/volume is fixed by parent geometry",
            "cannot_fix": "local alpha silence if the radius/modulus is dynamical or branch-dependent",
            "test": "g_EM^{-2} proportional to volume/radius still varies unless the modulus is parent-fixed and quotient-silent",
            "status": "DANGEROUS_MODULUS_ROUTE_NOT_DERIVED",
            "required_repair": "fixed radius/volume theorem and no local modulus residual",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "owner_id": "GLI1399_5_parent_vertical_norm",
            "candidate_owner": "parent vertical generator norm",
            "can_fix": "g_EM^{-2}=C_P N_Q if A_Q, T_Q, current, and readout are one parent-owned object",
            "cannot_fix": "lambda_A unless independent F_Q^2 and pullback counterterms are forbidden",
            "test": "1398 pullback no-go keeps q^*(F_Q^2) legal absent no-pullback or operator-basis theorem",
            "status": "BEST_CONTRACT_STILL_UNSIGNED",
            "required_repair": "join vertical norm, no-pullback, current owner, and readout descent",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "owner_id": "GLI1399_6_spectral_unification_RG",
            "candidate_owner": "spectral action, unification boundary, or RG flow",
            "can_fix": "relative gauge kinetic coefficients after UV scale, spectrum, and thresholds are fixed",
            "cannot_fix": "MTS-internal alpha_EM without importing a full particle/threshold sector",
            "test": "a UV relation still needs running, threshold, and matter content to reach local alphaEM",
            "status": "OUTSIDE_CURRENT_PARENT_ACTION",
            "required_repair": "explicit MTS spectral/particle sector and RG map",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "owner_id": "GLI1399_7_finite_empirical",
            "candidate_owner": "finite alphaEM prior/bound programme",
            "can_fix": "nothing derivational; supplies an honest residual vector",
            "cannot_fix": "lambda_A zero, unique F2, or EM-lock",
            "test": "finite lambda_A must face clocks, WEP, R10, and local residual gates without arena-specific screens",
            "status": "FALLBACK_ONLY_NONCLAIM",
            "required_repair": "source-backed finite coefficients and arena projection maps",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def theorem_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "LOT1399_0_charge_lattice_theorem",
            "candidate_statement": "compact U(1) gives integer charge labels n",
            "derivation_status": "CONDITIONAL_SUPPORT",
            "derives": "relative charge representation labels",
            "does_not_derive": "base charge unit, Maxwell kinetic normalization, lambda_A=0",
            "effect_on_lambda_A": "NO_ZERO",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "theorem_id": "LOT1399_1_flux_product_theorem",
            "candidate_statement": "Dirac/flux quantization fixes electric-magnetic product",
            "derivation_status": "NOT_PRESENT_AS_MTS_PARENT_THEOREM",
            "derives": "possible product constraint if a magnetic/topological flux unit exists",
            "does_not_derive": "standalone electric coupling or local alphaEM silence",
            "effect_on_lambda_A": "NO_ZERO_UNLESS_FLUX_UNIT_OWNED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "theorem_id": "LOT1399_2_topological_level_theorem",
            "candidate_statement": "BF/Chern-Simons/integer level fixes Maxwell coefficient",
            "derivation_status": "FAILS_CURRENT_CORPUS_FOR_4D_F2",
            "derives": "at most a topological or boundary response coefficient in current evidence",
            "does_not_derive": "metric 4D F_Q^2 coefficient without a bulk transfer theorem",
            "effect_on_lambda_A": "NO_ZERO",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "theorem_id": "LOT1399_3_Ward_index_theorem",
            "candidate_statement": "Ward/index/anomaly fixes coefficient owner",
            "derivation_status": "NOT_FOUND",
            "derives": "nothing claim-ready beyond an exact target contract",
            "does_not_derive": "operator/index/level mapping to g_EM^{-2}",
            "effect_on_lambda_A": "NO_ZERO",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "theorem_id": "LOT1399_4_vertical_norm_plus_level_theorem",
            "candidate_statement": "if T_Q norm, level/index owner, no-pullback rule, and readout descent all close, then lambda_A is non-deformable",
            "derivation_status": "EXACT_CONDITIONAL_THEOREM_READY_NOT_PROMOTED",
            "derives": "lambda_A=0 or lambda_A absorbed into fixed C_P N_Q only if all clauses are parent-signed",
            "does_not_derive": "any current claim, because every hard clause remains unsigned",
            "effect_on_lambda_A": "CONDITIONAL_ZERO_ONLY",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "theorem_id": "LOT1399_5_current_verdict",
            "candidate_statement": "current level/index owner status",
            "derivation_status": "OWNER_NOT_FOUND_FINITE_VECTOR_REQUIRED",
            "derives": "a sharper owner contract and a safer finite residual vector",
            "does_not_derive": "lambda_A zero, unique F2, EM-lock, alphaEM/local pass",
            "effect_on_lambda_A": "FINITE_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def owner_vector_rows() -> list[dict[str, str]]:
    return [
        {
            "slot_id": "LOV1399_0_k_level",
            "quantity": "k_Q_or_level",
            "meaning": "integer/topological level that would own the gauge coefficient",
            "needed_for": "make g_EM^{-2} non-deformable",
            "current_value": "MISSING_LEVEL_INDEX_OWNER",
            "source_status": "not found in current corpus",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "slot_id": "LOV1399_1_flux_unit",
            "quantity": "Phi_Q_or_magnetic_unit",
            "meaning": "parent-owned magnetic/topological flux unit for Dirac-type product quantization",
            "needed_for": "turn charge product quantization into electric coupling ownership",
            "current_value": "MISSING_PARENT_FLUX_UNIT",
            "source_status": "not supplied by MTS EM branch",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "slot_id": "LOV1399_2_vertical_norm",
            "quantity": "N_Q=<T_Q,T_Q>_P",
            "meaning": "fixed parent norm of the charge generator",
            "needed_for": "inherit g_EM^{-2}=C_P N_Q",
            "current_value": "MISSING_FIXED_N_Q",
            "source_status": "partial template only from 643/765",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "slot_id": "LOV1399_3_no_pullback",
            "quantity": "Z_no_pullback",
            "meaning": "selection rule excluding q^*(F_Q^2) as independent primitive",
            "needed_for": "forbid lambda_A",
            "current_value": "FALSE_CURRENT_CORPUS",
            "source_status": "1398 pullback no-go",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "slot_id": "LOV1399_4_lambda_A",
            "quantity": "lambda_A",
            "meaning": "standalone Maxwell kinetic coefficient",
            "needed_for": "finite residual if not theorem-zero",
            "current_value": "MISSING_PARENT_COEFFICIENT_OR_ZERO_THEOREM",
            "source_status": "explicit nonclaim source row from 1397/1398",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "slot_id": "LOV1399_5_derivative",
            "quantity": "partial_phi_c lambda_A",
            "meaning": "local drift of the finite counterterm",
            "needed_for": "alphaEM, clocks, WEP, R10, and local residual vector",
            "current_value": "MISSING_DERIVATIVE_MAP",
            "source_status": "no parent domain map",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def finite_prior_rows() -> list[dict[str, str]]:
    return [
        {
            "prior_id": "FAP1399_0_alphaEM_residual",
            "residual": "b_alpha_EM(lambda_A)",
            "definition": "-partial_phi_c ln(C_P N_Q + lambda_A) minus readout derivative",
            "current_input": "MISSING_DERIVATIVE_MAP",
            "arena": "alphaEM/clocks",
            "status": "NONCLAIM_INPUT_MISSING",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "prior_id": "FAP1399_1_source_force",
            "residual": "beta_source_alpha b_alpha_EM tau_WEP",
            "definition": "finite WEP/Coulomb source response",
            "current_input": "TARGET_ONLY_alpha<=4.797780522732e-05_robust<=2.887280314062e-05",
            "arena": "WEP",
            "status": "TARGET_ONLY_NOT_DERIVED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "prior_id": "FAP1399_2_R10_material",
            "residual": "beta_EM(lambda_A) and alpha_bulk_ST(lambda)",
            "definition": "finite EM binding leg into short-range force kernel",
            "current_input": "MISSING_KERNEL_COMPOSITION_TAIL_BOUND_CURVE",
            "arena": "R10",
            "status": "NONCLAIM_INPUT_MISSING",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "prior_id": "FAP1399_3_local_vector",
            "residual": "R_EM_local(lambda_A)",
            "definition": "combined local EM residual entering PPN/Newton/GR reduction gates",
            "current_input": "MISSING_JOINED_CURRENT_READOUT_OWNER",
            "arena": "local GR/Newton",
            "status": "LOCAL_VECTOR_INCOMPLETE",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "prior_id": "FAP1399_4_policy",
            "residual": "finite alphaEM prior policy",
            "definition": "finite priors may be used for sensitivity only and cannot replace derivation",
            "current_input": "NONCLAIM_SMOKE_ONLY",
            "arena": "all",
            "status": "PRIOR_CANNOT_PROMOTE_CLAIMS",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def arena_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "ECG1399_0_lambda_owner",
            "arena": "lambda_A owner",
            "dependency": "level/index/monopole/Ward/vertical norm owner",
            "current_blocker": "no candidate owns 4D Maxwell kinetic coefficient and forbids lambda_A",
            "status": "BLOCKED_OWNER_NOT_FOUND",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "ECG1399_1_unique_F2",
            "arena": "unique Maxwell F2",
            "dependency": "lambda_A zero or non-deformable absorption into C_P N_Q",
            "current_blocker": "level/index owner and no-pullback rule missing",
            "status": "BLOCKED_UNIQUE_F2_NOT_PROVED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "ECG1399_2_EM_lock",
            "arena": "EM-lock beta_EM zero",
            "dependency": "unique F2 plus current/readout/no-alpha matter owner",
            "current_blocker": "unique F2 not proved and joined owner missing",
            "status": "BLOCKED_EM_LOCK_NOT_PROMOTED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "ECG1399_3_alphaEM_empirical",
            "arena": "alphaEM/WEP/clock/R10",
            "dependency": "finite alphaEM prior vector with source-backed maps",
            "current_blocker": "derivative, tau, source, material, and R10 inputs missing",
            "status": "BLOCKED_FINITE_VECTOR_NOT_SCOREABLE",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "ECG1399_4_local_GR",
            "arena": "local GR/Newton",
            "dependency": "zero or bounded EM coupling residual inside local residual vector",
            "current_blocker": "EM residual vector incomplete",
            "status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "ECG1399_5_verdict",
            "arena": "all gates",
            "dependency": "owner theorem or source-backed finite vector",
            "current_blocker": "neither exists",
            "status": "ARENA_SCORING_BLOCKED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "claim_id": "GATE1399_0_level_owner",
            "claim": "level/index/monopole/Ward owner fixes g_EM^{-2}",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "candidate routes are support-only, missing, or do not currently fix 4D Maxwell F2",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1399_1_lambda_A_zero",
            "claim": "lambda_A=0",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "no coefficient owner and no no-pullback theorem",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1399_2_EM_lock",
            "claim": "EM-lock closes beta_EM=0",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "unique F2 remains unsigned and finite lambda_A vector remains live",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1399_3_empirical",
            "claim": "alphaEM/WEP/clock/R10 pass",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1399 does not score data and finite-vector inputs remain missing",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1399_4_local_GR",
            "claim": "local GR/Newton reduction can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "EM coupling residual is still not derived away or bounded",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1399_0_owner_result",
            "decision": "do not promote a level/index owner",
            "reason": "current candidates fix charges, products, or boundary responses, not the 4D Maxwell kinetic coefficient",
            "consequence": "lambda_A remains finite/nonclaim",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1399_1_best_derivation_route",
            "decision": "fuse vertical norm, no-pullback, current, and readout into one parent contract",
            "reason": "no single topological owner solved the coupling; the remaining derivable route is a joined parent-action theorem",
            "consequence": "next target builds an all-in EM coupling owner contract",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1399_2_empirical_route",
            "decision": "keep finite alphaEM prior vector visible",
            "reason": "if the joined theorem fails, clocks/WEP/R10/local tests must bound the residual rather than hide it",
            "consequence": "finite vector remains nonclaim until source-backed",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1399_0_1400",
            "target_doc": "1400-Y5-R10-RAB-joined-EM-coupling-owner-contract-or-finite-local-residual-vector.md",
            "target_script": "scripts/Y5_R10_RAB_joined_EM_coupling_owner_contract_or_finite_local_residual_vector.py",
            "task": "try to fuse T_Q norm, no-pullback operator basis, current owner, readout descent, and no-alpha matter vertex into one parent-action EM coupling theorem; if it fails, build the finite EM local residual vector explicitly",
            "success_condition": "either joined EM owner theorem closes the coupling route or every finite alphaEM residual is carried into nonclaim local/empirical gates",
            "do_not_claim": "lambda_A=0;unique F2;EM-lock beta_EM=0;alphaEM bound;WEP pass;clock pass;R10 pass;PPN pass;Newton limit;local GR;q_loc=0;GitHub-ready result",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def validation_rows(
    sources: list[dict[str, str]],
    owners: list[dict[str, str]],
    theorem: list[dict[str, str]],
    owner_vector: list[dict[str, str]],
    finite: list[dict[str, str]],
    arenas: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_ok = all(row["exists"] == "True" and row["anchor_found"] == "True" for row in sources)
    owner_not_found = any(
        row["owner_id"] == "GLI1399_3_anomaly_Ward_index"
        and row["status"] == "INDEX_OWNER_NOT_FOUND"
        for row in owners
    ) and any(
        row["owner_id"] == "GLI1399_5_parent_vertical_norm"
        and row["status"] == "BEST_CONTRACT_STILL_UNSIGNED"
        for row in owners
    )
    theorem_verdict = any(
        row["theorem_id"] == "LOT1399_5_current_verdict"
        and row["derivation_status"] == "OWNER_NOT_FOUND_FINITE_VECTOR_REQUIRED"
        for row in theorem
    )
    owner_vector_nonclaim = all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in owner_vector)
    owner_vector_missing = any("MISSING" in row["current_value"] or row["current_value"].startswith("FALSE") for row in owner_vector)
    finite_nonclaim = all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in finite)
    finite_missing = any("MISSING" in row["current_input"] or "TARGET_ONLY" in row["current_input"] or "NONCLAIM" in row["current_input"] for row in finite)
    arenas_blocked = all(
        row["claim_allowed"] == "False"
        and (row["status"].startswith("BLOCKED") or row["status"] == "ARENA_SCORING_BLOCKED")
        for row in arenas
    )
    gates_blocked = all(row["claim_allowed"] == "False" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        OWNER_AUDIT_PATH,
        THEOREM_ATTEMPT_PATH,
        OWNER_VECTOR_PATH,
        FINITE_PRIOR_PATH,
        ARENA_GATE_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
    ]
    scope_ok = all("formalization-workbench" not in str(ROOT / path) for path in output_paths)
    all_ok = (
        source_ok
        and owner_not_found
        and theorem_verdict
        and owner_vector_nonclaim
        and owner_vector_missing
        and finite_nonclaim
        and finite_missing
        and arenas_blocked
        and gates_blocked
        and scope_ok
    )
    now = datetime.now(timezone.utc).isoformat()
    return [
        {
            "check_id": "VAL1399_0_sources",
            "status": "PASS" if source_ok else "FAIL",
            "detail": "all cited source paths exist and anchors are present",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1399_1_owner_audit",
            "status": "PASS" if owner_not_found else "FAIL",
            "detail": "level/index candidates do not currently own the 4D Maxwell kinetic coefficient",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1399_2_theorem_attempt",
            "status": "PASS" if theorem_verdict else "FAIL",
            "detail": "level-owner theorem remains conditional/nonpromoted and finite vector is required",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1399_3_owner_vector",
            "status": "PASS" if owner_vector_nonclaim and owner_vector_missing else "FAIL",
            "detail": "lambda_A owner vector is explicit, nonclaim, and missing hard parent inputs",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1399_4_finite_vector",
            "status": "PASS" if finite_nonclaim and finite_missing else "FAIL",
            "detail": "finite alphaEM prior vector remains nonclaim and not scoreable",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1399_5_arena_claim_gates",
            "status": "PASS" if arenas_blocked and gates_blocked else "FAIL",
            "detail": "owner, unique F2, EM-lock, empirical, and local-GR claims remain blocked",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1399_6_scope",
            "status": "PASS" if scope_ok else "FAIL",
            "detail": "outputs are confined to post-checkpoint-work paths",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1399_7_overall",
            "status": "PASS" if all_ok else "FAIL",
            "detail": "1399 finds no level/index owner and retains lambda_A finite alphaEM vector as nonclaim",
            "generated_utc": now,
        },
    ]


def write_doc(
    sources: list[dict[str, str]],
    owners: list[dict[str, str]],
    theorem: list[dict[str, str]],
    owner_vector: list[dict[str, str]],
    finite: list[dict[str, str]],
    arenas: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    body = f"""# 1399 Y5 R10 RAB: Gauge Level Index Owner For LambdaA Or Finite AlphaEM Prior Vector

Status: `{STATUS}`

Claim ceiling: `{CLAIM_CEILING}`

**Current verdict:** no level/index/monopole/Ward owner has been found that fixes the observed 4D Maxwell kinetic coefficient and forbids independent `lambda_A`. Compact `U(1)` helps with charge labels; it does not by itself own the continuous coupling.

**Discipline move:** keep `lambda_A` finite and visible. The remaining derivable route is now a joined EM-coupling owner theorem: fixed `T_Q` norm, no-pullback operator basis, same-owner current, quotient-fixed readout, and no-alpha matter vertex must all close together.

## Source Register

{md_table(sources)}

## Gauge Level / Index Owner Audit

{md_table(owners)}

## Level Owner Theorem Attempt

{md_table(theorem)}

## `lambda_A` Owner Vector

{md_table(owner_vector)}

## Finite AlphaEM Prior Vector

{md_table(finite)}

## EM Coupling Arena Gates

{md_table(arenas)}

## Claim Gates

{md_table(gates)}

## Decision Ledger

{md_table(decisions)}

## Next Target

{md_table(next_target)}

## Validation

{md_table(validation)}
"""
    (ROOT / DOC_PATH).write_text(body, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    owners = owner_audit_rows()
    theorem = theorem_attempt_rows()
    owner_vector = owner_vector_rows()
    finite = finite_prior_rows()
    arenas = arena_gate_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, owners, theorem, owner_vector, finite, arenas, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(OWNER_AUDIT_PATH, owners)
    write_csv(THEOREM_ATTEMPT_PATH, theorem)
    write_csv(OWNER_VECTOR_PATH, owner_vector)
    write_csv(FINITE_PRIOR_PATH, finite)
    write_csv(ARENA_GATE_PATH, arenas)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, owners, theorem, owner_vector, finite, arenas, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1399 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()
