from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2717-Y5-R2FR-finite-RAB-green-kernel-normalization-or-parent-coefficient-zero-under-AX1090-closure.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2717_SOURCE_REGISTER.csv",
    "parent_zero_audit": RESIDUALS / "P8_Y5_R2FR_2717_PARENT_COEFFICIENT_ZERO_AUDIT.csv",
    "operator_normalization": RESIDUALS / "P8_Y5_R2FR_2717_RAB_OPERATOR_NORMALIZATION.csv",
    "green_kernel_certificate": RESIDUALS / "P8_Y5_R2FR_2717_GREEN_KERNEL_CERTIFICATE.csv",
    "arena_projection_contract": RESIDUALS / "P8_Y5_R2FR_2717_ARENA_PROJECTION_CONTRACT.csv",
    "normalized_finite_rows": RESIDUALS / "P8_Y5_R2FR_2717_NORMALIZED_FINITE_RAB_ROWS_NONCLAIM.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2717_CLAIM_GATES.csv",
    "blocker_stack": RESIDUALS / "P8_Y5_R2FR_2717_CURRENT_BLOCKER_STACK.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2717_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2717_NEXT_TARGET.csv",
    "project_snapshot": RESIDUALS / "P8_Y5_R2FR_2717_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2717_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2717_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_bounds": LOCAL_BOUNDS / "finite_RAB_green_kernel_normalization_2717_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "finite_RAB_source_weight_normalization_2717_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2717_FINITE_RAB_SOURCE_NORM_OR_PARENT_ZERO_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return ""
    return str(value)


def md_escape(value: Any) -> str:
    return normalize(value).replace("|", "\\|").replace("\n", "<br>")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="raise")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: normalize(row.get(key, "")) for key in fieldnames})


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


SOURCE_SPECS = [
    {
        "source_id": "SRC2717_0_2716",
        "label": "2716 finite R_AB operator handoff",
        "path": ROOT / "2716-Y5-R2FR-parent-protection-contract-or-finite-ZR-row-under-AX1090-closure.md",
        "needles": [
            "LAW2716_1_euler_operator",
            "LAW2716_3_amplitude_bound",
            "FZR2716_0_ZR",
            "NEXT2716_0_selected",
            "VAL2716_OVERALL",
        ],
        "use": "specific R_AB residual operator and selected 2717 target",
    },
    {
        "source_id": "SRC2717_1_2716_rows",
        "label": "2716 normalized finite-row scaffold",
        "path": RESIDUALS / "P8_Y5_R2FR_2716_FINITE_ZR_JR_RAB_ROW_SCAFFOLD.csv",
        "needles": [
            "FZR2716_0_ZR",
            "FZR2716_1_MR2",
            "FZR2716_2_JEFF",
            "FZR2716_5_TAU_LOCAL",
        ],
        "use": "symbolic finite branch rows to refine into same-frame normalization requirements",
    },
    {
        "source_id": "SRC2717_2_2478_green",
        "label": "2478 residual-source Green-bound certificate",
        "path": ROOT / "2478-Y5-R2FR-residual-source-norm-and-Green-bound-certificate.md",
        "needles": [
            "GRN2478_0_poisson_inverse",
            "GRN2478_1_sup_kernel_bound",
            "GRN2478_2_elliptic_norm_bound",
            "C_GREEN_SYMBOLIC_ONLY",
        ],
        "use": "standard Green-bound guardrails and nonclaim normalization blockers",
    },
    {
        "source_id": "SRC2717_3_2208_source_norm",
        "label": "2208 Green/source-normalization warning",
        "path": ROOT / "2208-Y5-R2FR-PPN-Green-operator-source-normalization-or-R10-range-kernel.md",
        "needles": [
            "PPNL2208_3_source_normalization",
            "R10K2208_0_yukawa_kernel_form",
            "R10K2208_1_alpha_lambda_point_mass_map",
        ],
        "use": "source normalization and Yukawa/range kernel caution before any PPN/R10 score",
    },
    {
        "source_id": "SRC2717_4_1567_contract",
        "label": "1567 parent protection theorem target",
        "path": ROOT / "1567-Y5-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md",
        "needles": [
            "CON1567_5_operator_exclusion",
            "THM1567_0_statement",
            "ACQ1567_1_ZR",
            "ACQ1567_3_JR",
        ],
        "use": "parent coefficient zero route and finite coefficient acquisition list",
    },
    {
        "source_id": "SRC2717_5_1867_object_language",
        "label": "1867 object-language radial-cell blocker",
        "path": ROOT / "1867-Y5-R2FR-object-language-radial-cell-constraint-or-finite-ZRJR-intake.md",
        "needles": [
            "OLA1867_2_derivative_exclusion",
            "OLA1867_3_source_exclusion",
            "CMA1867_0_locality_scalar",
            "FINT1867_0_ZR",
        ],
        "use": "confirms zero theorems are conditional and finite countermodel survives",
    },
]


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = Path(spec["path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "label": spec["label"],
                "path": str(path),
                "exists": path.exists(),
                "required_needles_found": not missing,
                "missing_needles": ";".join(missing),
                "use": spec["use"],
                "claim_credit": False,
                "timestamp_utc": ts(),
            }
        )
    return rows


def parent_zero_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "zero_id": "ZERO2717_0_ZR_operator_exclusion",
            "target": "Z_R=0",
            "candidate_proof": "R_AB is typed auxiliary compatibility data and ParentGenerate has no D R_AB constructor",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "why_not_closed": "typed parent grammar/action-image exhaustion is still unsigned under AX1090 closure",
            "fallback_if_not_zero": "finite Z_R with same-frame action normalization",
            "claim_allowed": False,
            "source_anchor": "1567 CON1567_5; 1867 OLA1867_2; 2716 PPC2716_3",
            "timestamp_utc": ts(),
        },
        {
            "zero_id": "ZERO2717_1_JR_matter_descent",
            "target": "J_R=0",
            "candidate_proof": "matter descends through observed metric/coframe and not directly through R_AB",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "why_not_closed": "universal matter, EM, mass, clock, and material-label descent remains unproved",
            "fallback_if_not_zero": "finite J_matter component inside J_eff",
            "claim_allowed": False,
            "source_anchor": "1567 CON1567_2; 1867 OLA1867_3; 2716 FZR2716_2",
            "timestamp_utc": ts(),
        },
        {
            "zero_id": "ZERO2717_2_BR_QR_boundary",
            "target": "B_R=Q_R=0",
            "candidate_proof": "boundary/corner/readout terms preserve the algebraic compatibility constraint",
            "status": "NO_CHARGE_THEOREM_NOT_SIGNED",
            "why_not_closed": "source-worldtube, corner, harmonic, and readout-regeneration terms are not theorem-zero",
            "fallback_if_not_zero": "finite boundary/readout contribution to J_eff and separate boundary norm",
            "claim_allowed": False,
            "source_anchor": "1567 CON1567_3; 1567 CON1567_4; 2478 boundary/harmonic blockers",
            "timestamp_utc": ts(),
        },
        {
            "zero_id": "ZERO2717_3_MR2_gap",
            "target": "M_R^2>0 or constraint limit M_R^2=infinite",
            "candidate_proof": "parent Hessian gives positive reciprocal-cell stiffness or exact auxiliary elimination",
            "status": "MISSING_PARENT_HESSIAN",
            "why_not_closed": "no sourced Hessian/gap value or exact Dirac elimination certificate exists",
            "fallback_if_not_zero": "keep M_R^2 symbolic and require positivity before Green bounds score",
            "claim_allowed": False,
            "source_anchor": "1568 COEFF1568_0_ZR; 1568 COEFF1568_1_JR; 2716 FZR2716_1_MR2",
            "timestamp_utc": ts(),
        },
        {
            "zero_id": "ZERO2717_4_verdict",
            "target": "parent coefficient zero package",
            "candidate_proof": "joint contract eliminates Z_R, J_eff, boundary/readout leakage",
            "status": "NO_COEFFICIENT_ZERO_CLAIM_IN_2717",
            "why_not_closed": "all zeros remain conditional on unsigned parent protection clauses",
            "fallback_if_not_zero": "use the normalized finite Green-kernel branch below",
            "claim_allowed": False,
            "source_anchor": "2716 PPC2716_6; 1567 THM1567_0",
            "timestamp_utc": ts(),
        },
    ]


def operator_normalization_rows() -> list[dict[str, Any]]:
    return [
        {
            "norm_id": "NORM2717_0_field",
            "object": "R_AB",
            "normalization_statement": "R_AB is dimensionless with R_AB=2 ln(J_q)=ln(T^2 S)",
            "units": "dimensionless",
            "same_frame_requirement": "T,S,J_q and observed metric readout must be in the same local frame/domain",
            "status": "DEFINITION_NORMALIZED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "norm_id": "NORM2717_1_operator",
            "object": "L_R",
            "normalization_statement": "L_R R_AB = (-Z_R Delta_h + M_R^2) R_AB = J_eff",
            "units": "Z_R carries source units times length^2; M_R^2 carries source units for dimensionless R_AB",
            "same_frame_requirement": "Z_R,M_R^2,J_eff,Delta_h and measure sqrt(h) must share one parent action normalization",
            "status": "FORMAL_OPERATOR_NORMALIZED_SYMBOLIC",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "norm_id": "NORM2717_2_range",
            "object": "ell_R",
            "normalization_statement": "ell_R=sqrt(Z_R/M_R^2), valid only for Z_R>0 and M_R^2>0 in the same normalization",
            "units": "length",
            "same_frame_requirement": "same-frame ratio; no mixing fitted lab/solar GM or external range priors with MTS coefficients",
            "status": "CONDITIONAL_SYMBOLIC_RANGE",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "norm_id": "NORM2717_3_source",
            "object": "j_R=J_eff/Z_R",
            "normalization_statement": "after division by Z_R, (-Delta_h+ell_R^-2)R_AB=j_R",
            "units": "length^-2 for dimensionless R_AB in flat local units",
            "same_frame_requirement": "only legal if Z_R is finite, positive, sourced, and not a fitted retune parameter",
            "status": "CONDITIONAL_SOURCE_NORMALIZATION",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "norm_id": "NORM2717_4_boundary",
            "object": "boundary/harmonic sector",
            "normalization_statement": "solution is R_AB=G_R*j_R + R_boundary + R_harmonic",
            "units": "dimensionless R_AB contribution",
            "same_frame_requirement": "boundary orientation, domain collar, source worldtube, and gauge/readout must be fixed",
            "status": "BOUNDARY_NORMALIZATION_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
    ]


def green_kernel_certificate_rows() -> list[dict[str, Any]]:
    return [
        {
            "green_id": "GRN2717_0_flat_yukawa_kernel",
            "domain": "flat/local collar approximation after gauge/domain fixation",
            "formula": "G_R(r)=exp(-r/ell_R)/(4*pi*Z_R*r)",
            "bound": "R_AB(x)=integral G_R(|x-y|) J_eff(y) d^3y + boundary/harmonic",
            "status": "DERIVED_FORMAL_KERNEL_NONCLAIM",
            "missing_input": "Z_R;M_R^2;J_eff;domain;boundary;gauge;source support",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "green_id": "GRN2717_1_sup_separated_support",
            "domain": "observation point separated from bounded source support by d_min>0",
            "formula": "|R_AB|_inf <= V_eff exp(-d_min/ell_R)/(4*pi Z_R d_min)||J_eff||_inf + |R_boundary|",
            "bound": "pointwise conservative bound for R10/lab exterior style estimates",
            "status": "FORMAL_BOUND_NEEDS_GEOMETRY_AND_SOURCE",
            "missing_input": "V_eff;d_min;boundary norm;positive Z_R;ell_R;source norm",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "green_id": "GRN2717_2_L2_coercive_bound",
            "domain": "bounded regular domain with positive operator and controlled boundary",
            "formula": "||R_AB||_L2 <= ||J_eff||_L2/M_R^2 + boundary_term",
            "bound": "coercive massive elliptic estimate for amplitude discipline",
            "status": "FORMAL_BOUND_NEEDS_POSITIVITY",
            "missing_input": "M_R^2>0;source L2 norm;boundary condition;domain measure",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "green_id": "GRN2717_3_gradient_bound",
            "domain": "same coercive domain",
            "formula": "Z_R||grad R_AB||_L2^2 + M_R^2||R_AB||_L2^2 <= ||J_eff||_L2||R_AB||_L2 + boundary_work",
            "bound": "energy inequality showing how source and boundary work control reciprocal hair",
            "status": "ENERGY_BOUND_SHAPE_NONCLAIM",
            "missing_input": "boundary_work sign/bound;positive Z_R;positive M_R^2;source norm",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "green_id": "GRN2717_4_zero_limit",
            "domain": "theorem-zero or infinite-mass auxiliary limit",
            "formula": "if J_eff=0 and boundary/harmonic=0, then R_AB=0; if M_R^2->infinite with finite source, R_AB->0",
            "bound": "shows exact local GR route but only after missing parent zeros/gap are signed",
            "status": "EXACT_CONDITIONAL_NOT_CLAIMED",
            "missing_input": "J_eff zero;boundary zero;positive/infinite gap;parent origin",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
    ]


def arena_projection_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena_id": "ARENA2717_0_R10",
            "arena": "R10 short-range fifth-force",
            "projection_contract": "alpha_R10(lambda)=Pi_R10[G_R*J_eff;source/test charges, apparatus geometry]",
            "kernel_dependency": "ell_R and Yukawa support profile",
            "normalization_needed": "tau_R10(lambda), source/test charge map, material coupling, real alpha(lambda) bound curve",
            "status": "NOT_SCORE_READY",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "arena_id": "ARENA2717_1_PPN",
            "arena": "PPN/local GR",
            "projection_contract": "delta gamma, delta beta, light-deflection and Shapiro residuals = Pi_PPN[R_AB profile + metric-response map]",
            "kernel_dependency": "same Green profile plus weak-field metric readout",
            "normalization_needed": "PPN gauge transform, metric response coefficients, measured-GM no-absorption rule",
            "status": "NOT_SCORE_READY",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "arena_id": "ARENA2717_2_clock",
            "arena": "clock/redshift",
            "projection_contract": "delta nu/nu = Pi_clock[R_AB,readout,tau-frame]",
            "kernel_dependency": "local amplitude and readout stability",
            "normalization_needed": "clock species descent, tau frame, boundary/readout leakage bound",
            "status": "NOT_SCORE_READY",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "arena_id": "ARENA2717_3_orbital",
            "arena": "orbital/precession",
            "projection_contract": "delta a or delta precession = Pi_orbit[grad R_AB, metric residual]",
            "kernel_dependency": "gradient bound and exterior harmonic/monopole control",
            "normalization_needed": "source worldtube, no fitted-GM absorption, multipole/boundary hair bound",
            "status": "NOT_SCORE_READY",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
    ]


def normalized_finite_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NF2717_0_ZR",
            "quantity": "Z_R",
            "normalized_role": "coefficient in G_R(r)=exp(-r/ell_R)/(4*pi*Z_R*r)",
            "required_units": "same action/source normalization as J_eff times length^2",
            "required_source": "parent second variation or theorem-zero of derivative constructor",
            "blocking_reason": "MISSING_NUMERIC_PARENT_COEFFICIENT_OR_OPERATOR_ZERO",
            "claim_gate": "closed",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "row_id": "NF2717_1_MR2",
            "quantity": "M_R^2",
            "normalized_role": "mass/gap term defining ell_R=sqrt(Z_R/M_R^2) and L2 amplitude denominator",
            "required_units": "same action/source normalization as J_eff",
            "required_source": "parent Hessian, auxiliary Dirac elimination, or sourced finite gap",
            "blocking_reason": "MISSING_PARENT_HESSIAN_OR_GAP",
            "claim_gate": "closed",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "row_id": "NF2717_2_JEFF",
            "quantity": "J_eff",
            "normalized_role": "source norm entering ||R_AB|| <= ||G_R||||J_eff||",
            "required_units": "Euler source conjugate to dimensionless R_AB in same measure",
            "required_source": "matter descent map plus boundary/readout source decomposition",
            "blocking_reason": "MISSING_SOURCE_NORM_MAP_AND_BOUNDARY_READOUT_SPLIT",
            "claim_gate": "closed",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "row_id": "NF2717_3_DOMAIN",
            "quantity": "Omega,d_min,V_eff,boundary,harmonic",
            "normalized_role": "domain constants in the pointwise and elliptic Green bounds",
            "required_units": "length/domain measure and dimensionless boundary contribution",
            "required_source": "arena-specific local collar/source-worldtube/gauge package",
            "blocking_reason": "MISSING_DOMAIN_GEOMETRY_AND_BOUNDARY_CLASS",
            "claim_gate": "closed",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "row_id": "NF2717_4_TAU",
            "quantity": "tau_R10,tau_PPN,tau_clock,tau_orbital",
            "normalized_role": "observable projection from R_AB amplitude/gradient to arena residuals",
            "required_units": "arena-specific residual per dimensionless R_AB or gradient",
            "required_source": "parent readout map and test-specific convention",
            "blocking_reason": "MISSING_ARENA_PROJECTION_KERNELS",
            "claim_gate": "closed",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE2717_0_parent_zero",
            "claim": "Z_R/J_eff/boundary/readout theorem-zero",
            "status": "BLOCKED",
            "required_before_claim": "parent protection clauses signed under AX1090 closure",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "gate_id": "GATE2717_1_green_numeric",
            "claim": "finite Green kernel gives numeric local amplitude bound",
            "status": "BLOCKED",
            "required_before_claim": "numeric same-frame Z_R,M_R^2,J_eff and domain/boundary package",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "gate_id": "GATE2717_2_R10",
            "claim": "R10 alpha(lambda) score",
            "status": "BLOCKED",
            "required_before_claim": "tau_R10/source-test charges/apparatus geometry plus real bound curve",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "gate_id": "GATE2717_3_PPN_GR",
            "claim": "local GR/PPN/Newton reduction",
            "status": "BLOCKED",
            "required_before_claim": "R_AB zero or bounded residual vector plus full metric readout/gauge/no-GM-absorption package",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "gate_id": "GATE2717_4_public",
            "claim": "public/GitHub update",
            "status": "NOT_REQUESTED_BLOCKED_BY_PRIVATE_SCOPE",
            "required_before_claim": "explicit user request and public-safe claim language",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
    ]


def blocker_stack_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BLK2717_0_parent_coefficients",
            "missing_item": "Z_R,M_R^2,J_eff source or zero theorem",
            "effect": "kernel is symbolic, not numeric",
            "best_next_attack": "derive parent source norm split for J_eff or coefficient-zero theorem for Z_R",
            "claim_blocked": "R10;PPN;local_GR",
            "timestamp_utc": ts(),
        },
        {
            "blocker_id": "BLK2717_1_source_norm",
            "missing_item": "same-frame ||J_eff|| bound",
            "effect": "amplitude law has no magnitude",
            "best_next_attack": "decompose J_eff into J_matter,J_boundary,J_readout with units/source paths",
            "claim_blocked": "finite local amplitude",
            "timestamp_utc": ts(),
        },
        {
            "blocker_id": "BLK2717_2_domain_boundary",
            "missing_item": "Omega,d_min,V_eff,boundary/harmonic package",
            "effect": "Green constant cannot be used for lab/solar/orbital arenas",
            "best_next_attack": "choose one arena-specific collar package after coefficient/source norm exists",
            "claim_blocked": "R10;clock;orbital",
            "timestamp_utc": ts(),
        },
        {
            "blocker_id": "BLK2717_3_observable_projection",
            "missing_item": "tau_i projection kernels",
            "effect": "R_AB amplitude is not yet an observable residual",
            "best_next_attack": "derive tau_PPN or tau_R10 only after coefficient/source normalization",
            "claim_blocked": "any empirical score",
            "timestamp_utc": ts(),
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2717_0_no_zero_claim",
            "decision": "do not claim parent coefficient zero",
            "rationale": "operator/source/boundary/readout zeros remain conditional on unsigned parent clauses",
            "allowed": True,
            "claim_credit": False,
            "timestamp_utc": ts(),
        },
        {
            "decision_id": "DEC2717_1_kernel_gain",
            "decision": "accept the finite R_AB Green kernel as a real formal normalization gain",
            "rationale": "the branch now has field normalization, kernel form, range scale, and amplitude inequalities",
            "allowed": True,
            "claim_credit": False,
            "timestamp_utc": ts(),
        },
        {
            "decision_id": "DEC2717_2_priority",
            "decision": "prioritize J_eff source-norm split before arena scoring",
            "rationale": "a perfect R10/PPN projection cannot score if the source magnitude is unknown",
            "allowed": True,
            "claim_credit": False,
            "timestamp_utc": ts(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2717_0_selected",
            "status": "selected_primary",
            "target_doc": "2718-Y5-R2FR-Jeff-source-norm-split-or-ZR-theorem-zero-under-AX1090-closure.md",
            "target_script": "scripts/Y5_R2FR_Jeff_source_norm_split_or_ZR_theorem_zero_under_AX1090_closure_2718.py",
            "mission": "split J_eff into matter, boundary, harmonic and readout pieces with units/source paths, while making one last targeted attempt at Z_R theorem-zero from parent no-derivative grammar",
            "acceptance": "either Z_R is parent-zero signed, or J_eff source-norm rows become explicit enough to feed the 2717 Green bound as nonclaim inputs",
            "forbidden": "score R10/PPN; insert numeric placeholders; use fitted GM absorption; edit formalization-workbench; GitHub action",
            "selected": True,
            "claim_allowed": False,
            "timestamp_utc": ts(),
        }
    ]


def project_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "snapshot_id": "SNAP2717_0_status",
            "sector": "local-GR bridge",
            "state": "R_AB finite branch now has explicit kernel/range/amplitude formulas, but remains nonnumeric",
            "confidence": "structural progress; not empirical/local-GR evidence",
            "next_need": "J_eff source norm or parent zero theorem",
            "timestamp_utc": ts(),
        },
        {
            "snapshot_id": "SNAP2717_1_zero_route",
            "sector": "derivation",
            "state": "parent coefficient zeros remain unsigned",
            "confidence": "blocked as claim",
            "next_need": "typed parent no-derivative grammar or matter descent proof",
            "timestamp_utc": ts(),
        },
        {
            "snapshot_id": "SNAP2717_2_testing_route",
            "sector": "empirical readiness",
            "state": "not ready for R10/PPN/clock/orbital scoring",
            "confidence": "honest blocker",
            "next_need": "source norm, domain package, tau projection kernels",
            "timestamp_utc": ts(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "COPY2717_0_local_bounds",
            "source_table": "P8_Y5_R2FR_2717_NORMALIZED_FINITE_RAB_ROWS_NONCLAIM.csv",
            "copy_path": str(BRANCH_OUTPUTS["local_bounds"]),
            "purpose": "quarantine Green-kernel local-bound normalization rows as nonclaim",
            "exists": BRANCH_OUTPUTS["local_bounds"].exists(),
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "copy_id": "COPY2717_1_source_weight",
            "source_table": "P8_Y5_R2FR_2717_NORMALIZED_FINITE_RAB_ROWS_NONCLAIM.csv",
            "copy_path": str(BRANCH_OUTPUTS["source_weight"]),
            "purpose": "quarantine finite source-weight normalization rows as nonclaim",
            "exists": BRANCH_OUTPUTS["source_weight"].exists(),
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "copy_id": "COPY2717_2_next_queue",
            "source_table": "P8_Y5_R2FR_2717_NEXT_TARGET.csv",
            "copy_path": str(BRANCH_OUTPUTS["next_queue"]),
            "purpose": "queue 2718 without touching formalization-workbench",
            "exists": BRANCH_OUTPUTS["next_queue"].exists(),
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
    ]


def csv_parse_details(paths: list[Path]) -> tuple[bool, str]:
    details: list[str] = []
    ok = True
    for path in paths:
        try:
            with path.open("r", newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            if not rows:
                ok = False
                details.append(f"{path.name}:0 rows")
            else:
                details.append(f"{path.name}:{len(rows)}:parsed")
        except Exception as exc:
            ok = False
            details.append(f"{path.name}:ERROR:{exc}")
    return ok, "; ".join(details)


def formalization_recent_changed_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified >= SCRIPT_START_UTC:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    norm_rows: list[dict[str, Any]],
    green_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    finite_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    branches: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    csv_paths = [
        OUTPUTS["source_register"],
        OUTPUTS["parent_zero_audit"],
        OUTPUTS["operator_normalization"],
        OUTPUTS["green_kernel_certificate"],
        OUTPUTS["arena_projection_contract"],
        OUTPUTS["normalized_finite_rows"],
        OUTPUTS["claim_gates"],
        OUTPUTS["blocker_stack"],
        OUTPUTS["decision_ledger"],
        OUTPUTS["next_target"],
        OUTPUTS["project_snapshot"],
        OUTPUTS["branch_copies"],
        *BRANCH_OUTPUTS.values(),
    ]
    csv_ok, csv_detail = csv_parse_details(csv_paths)
    source_ok = all(row["exists"] and row["required_needles_found"] for row in sources)
    zero_claims_false = all(row["claim_allowed"] is False for row in zero_rows)
    norm_nonclaim = all(row["valid_for_claim"] is False for row in norm_rows)
    green_nonclaim = all(row["valid_for_claim"] is False for row in green_rows)
    arena_nonclaim = all(row["valid_for_claim"] is False for row in arena_rows)
    finite_nonclaim = all(row["valid_for_claim"] is False for row in finite_rows)
    gates_false = all(row["claim_allowed"] is False for row in gates)
    branch_ok = all(Path(row["copy_path"]).exists() and row["valid_for_claim"] is False for row in branches)
    formula_ok = any("exp(-r/ell_R)/(4*pi*Z_R*r)" in row["formula"] for row in green_rows)
    amplitude_ok = any("||R_AB||_L2" in row["formula"] for row in green_rows)
    formalization_count = formalization_recent_changed_count()
    no_github_outputs = all(".git" not in str(path).lower() and "github" not in str(path).lower() for path in csv_paths)
    rows = [
        {
            "validation_id": "VAL2717_0_sources",
            "passed": source_ok,
            "detail": "all source paths exist and required needles found" if source_ok else "missing source or needle",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2717_1_doc_written",
            "passed": DOC.exists(),
            "detail": str(DOC),
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2717_2_csv_parse",
            "passed": csv_ok,
            "detail": csv_detail,
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2717_3_parent_zero_nonclaim",
            "passed": zero_claims_false,
            "detail": "all parent coefficient zero attempts remain nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2717_4_normalization_rows_nonclaim",
            "passed": norm_nonclaim,
            "detail": "operator normalization rows keep valid_for_claim=false",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2717_5_green_rows_nonclaim",
            "passed": green_nonclaim and formula_ok and amplitude_ok,
            "detail": "kernel and amplitude formulas present; all Green rows nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2717_6_arena_rows_nonclaim",
            "passed": arena_nonclaim,
            "detail": "R10/PPN/clock/orbital projections remain not score-ready",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2717_7_finite_rows_nonclaim",
            "passed": finite_nonclaim,
            "detail": "normalized finite rows keep valid_for_claim=false",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2717_8_claim_gates_all_false",
            "passed": gates_false,
            "detail": "no local-GR/R10/PPN/public claim gate opened",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2717_9_branch_copies",
            "passed": branch_ok,
            "detail": "branch copies exist and remain nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2717_10_no_formalization_recent_changes",
            "passed": formalization_count == 0,
            "detail": f"formalization_recent_changed_count={formalization_count}",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2717_11_no_github_outputs",
            "passed": no_github_outputs,
            "detail": "no GitHub/public-output path was written",
            "timestamp_utc": ts(),
        },
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(
        {
            "validation_id": "VAL2717_OVERALL",
            "passed": overall,
            "detail": "2717 fails the parent coefficient-zero proof, but normalizes the finite R_AB Green kernel/range/amplitude branch as strict nonclaim and selects J_eff source-norm split next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    norm_rows: list[dict[str, Any]],
    green_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    finite_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    snapshot: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2717 - Y5/R2FR Finite R_AB Green-kernel Normalization Or Parent Coefficient Zero Under AX1090 Closure",
        "",
        "## Private Verdict",
        "",
        "2717 takes the fork honestly. The parent coefficient-zero route does **not** close: `Z_R=0`, `J_eff=0`, boundary no-charge, and readout silence remain conditional on unsigned parent-protection clauses. No local-GR/Newton/PPN/R10 claim is opened.",
        "",
        "The useful progress is the finite branch. With `R_AB` dimensionless, the fallback operator is normalized as `(-Z_R Delta_h + M_R^2) R_AB = J_eff`. When `Z_R>0` and `M_R^2>0` in the same parent-action normalization, `ell_R=sqrt(Z_R/M_R^2)` and the local Yukawa Green kernel is `G_R(r)=exp(-r/ell_R)/(4*pi*Z_R*r)`. That gives real nonclaim amplitude laws, but they still need `Z_R`, `M_R^2`, `J_eff`, domain/boundary constants, and arena projection kernels before tests can score.",
        "",
        "## Claim Ceiling",
        "",
        "- No parent coefficient zero is claimed from 2717.",
        "- No numeric local amplitude, R10, PPN, clock, orbital, local-GR, Newton, or public/GitHub claim is allowed.",
        "- The Green kernel is a formal normalization gain only; symbolic rows remain `valid_for_claim=false`.",
        "- No `formalization-workbench` edits are allowed from this checkpoint.",
        "",
        "## Source Register",
        "",
        markdown_table(sources, ["source_id", "label", "path", "exists", "required_needles_found", "missing_needles", "use", "claim_credit"]),
        "",
        "## Parent Coefficient Zero Audit",
        "",
        markdown_table(zero_rows, ["zero_id", "target", "candidate_proof", "status", "why_not_closed", "fallback_if_not_zero", "claim_allowed", "source_anchor"]),
        "",
        "## Operator Normalization",
        "",
        markdown_table(norm_rows, ["norm_id", "object", "normalization_statement", "units", "same_frame_requirement", "status", "valid_for_claim"]),
        "",
        "## Green Kernel Certificate",
        "",
        markdown_table(green_rows, ["green_id", "domain", "formula", "bound", "status", "missing_input", "valid_for_claim"]),
        "",
        "## Arena Projection Contract",
        "",
        markdown_table(arena_rows, ["arena_id", "arena", "projection_contract", "kernel_dependency", "normalization_needed", "status", "valid_for_claim"]),
        "",
        "## Normalized Finite Rows",
        "",
        markdown_table(finite_rows, ["row_id", "quantity", "normalized_role", "required_units", "required_source", "blocking_reason", "claim_gate", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        markdown_table(gates, ["gate_id", "claim", "status", "required_before_claim", "claim_allowed"]),
        "",
        "## Current Blocker Stack",
        "",
        markdown_table(blockers, ["blocker_id", "missing_item", "effect", "best_next_attack", "claim_blocked"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(decisions, ["decision_id", "decision", "rationale", "allowed", "claim_credit"]),
        "",
        "## Next Target",
        "",
        markdown_table(next_rows, ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "claim_allowed"]),
        "",
        "## Project Status Snapshot",
        "",
        markdown_table(snapshot, ["snapshot_id", "sector", "state", "confidence", "next_need"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(branches, ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        markdown_table(validation, ["validation_id", "passed", "detail", "timestamp_utc"]),
        "",
        "## Plain-English Read",
        "",
        "This is a good engineering-style step. We did not prove the residual disappears, but we stopped treating it like smoke. The local reciprocal leakage branch now has a proper operator, a range, a Green kernel, and amplitude inequalities. That is exactly the kind of object we can later kill by derivation or drag into tests.",
        "",
        "The next best strike is not R10 scoring yet. It is `J_eff`: split the source into matter, boundary, harmonic, and readout pieces with units. If `J_eff` goes to zero by derivation, local GR gets much closer. If it does not, we finally have the right shape for a real bound.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    for directory in (RESIDUALS, LOCAL_BOUNDS, SOURCE_WEIGHT, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    zero_rows = parent_zero_audit_rows()
    norm_rows = operator_normalization_rows()
    green_rows = green_kernel_certificate_rows()
    arena_rows = arena_projection_contract_rows()
    finite_rows = normalized_finite_rows()
    gates = claim_gate_rows()
    blockers = blocker_stack_rows()
    decisions = decision_ledger_rows()
    next_rows = next_target_rows()
    snapshot = project_snapshot_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["parent_zero_audit"], zero_rows)
    write_csv(OUTPUTS["operator_normalization"], norm_rows)
    write_csv(OUTPUTS["green_kernel_certificate"], green_rows)
    write_csv(OUTPUTS["arena_projection_contract"], arena_rows)
    write_csv(OUTPUTS["normalized_finite_rows"], finite_rows)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["blocker_stack"], blockers)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)
    write_csv(OUTPUTS["project_snapshot"], snapshot)

    write_csv(BRANCH_OUTPUTS["local_bounds"], finite_rows)
    write_csv(BRANCH_OUTPUTS["source_weight"], finite_rows)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_rows)

    branches = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], branches)

    pending_validation = [
        {
            "validation_id": "VAL2717_PENDING",
            "passed": False,
            "detail": "pre-validation placeholder for first doc write",
            "timestamp_utc": ts(),
        }
    ]
    write_doc(
        sources,
        zero_rows,
        norm_rows,
        green_rows,
        arena_rows,
        finite_rows,
        gates,
        blockers,
        decisions,
        next_rows,
        snapshot,
        branches,
        pending_validation,
    )

    validation = validation_rows(
        sources,
        zero_rows,
        norm_rows,
        green_rows,
        arena_rows,
        finite_rows,
        gates,
        branches,
    )
    write_csv(OUTPUTS["validation"], validation)
    write_doc(
        sources,
        zero_rows,
        norm_rows,
        green_rows,
        arena_rows,
        finite_rows,
        gates,
        blockers,
        decisions,
        next_rows,
        snapshot,
        branches,
        validation,
    )

    overall = next(row for row in validation if row["validation_id"] == "VAL2717_OVERALL")
    print(f"2717 complete: {overall['passed']} - {overall['detail']}")
    print(DOC)


if __name__ == "__main__":
    main()
