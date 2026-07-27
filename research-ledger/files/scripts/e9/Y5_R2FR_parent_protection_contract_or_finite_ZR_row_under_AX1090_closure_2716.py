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

DOC = ROOT / "2716-Y5-R2FR-parent-protection-contract-or-finite-ZR-row-under-AX1090-closure.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2716_SOURCE_REGISTER.csv",
    "parent_protection_audit": RESIDUALS / "P8_Y5_R2FR_2716_PARENT_PROTECTION_AUDIT.csv",
    "proof_attempts": RESIDUALS / "P8_Y5_R2FR_2716_PROOF_ATTEMPT_LEDGER.csv",
    "finite_operator_law": RESIDUALS / "P8_Y5_R2FR_2716_FINITE_RAB_OPERATOR_LAW.csv",
    "finite_row_scaffold": RESIDUALS / "P8_Y5_R2FR_2716_FINITE_ZR_JR_RAB_ROW_SCAFFOLD.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2716_CLAIM_GATES.csv",
    "blocker_stack": RESIDUALS / "P8_Y5_R2FR_2716_CURRENT_BLOCKER_STACK.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2716_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2716_NEXT_TARGET.csv",
    "project_snapshot": RESIDUALS / "P8_Y5_R2FR_2716_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2716_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2716_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_arena_projection": LOCAL_BOUNDS / "finite_RAB_local_arena_projection_2716_NONCLAIM.csv",
    "finite_source_weight": SOURCE_WEIGHT / "finite_ZR_JR_RAB_row_gate_2716_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2716_PARENT_PROTECTION_OR_FINITE_RAB_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def normalize(value: Any) -> str:
    if isinstance(value, bool):
        return bool_text(value)
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
        "source_id": "SRC2716_0_2715_gate",
        "label": "2715 minimal weak-field auxiliary gate",
        "path": ROOT / "2715-Y5-R2FR-minimal-weak-field-auxiliary-action-gate-under-AX1090-closure.md",
        "needles": [
            "AUX2715_4_joint_contract",
            "FRF2715_0_ZR",
            "NEXT2715_0_selected",
            "VAL2715_OVERALL",
        ],
        "use": "immediate parent target and nonclaim finite fallback inherited from 2715",
    },
    {
        "source_id": "SRC2716_1_1567_contract",
        "label": "1567 parent protection contract",
        "path": ROOT / "1567-Y5-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md",
        "needles": [
            "CON1567_0_parent_sorts",
            "CON1567_6_joint_contract",
            "THM1567_0_statement",
            "ACQ1567_1_ZR",
        ],
        "use": "full clause list and conditional theorem for R_AB protection",
    },
    {
        "source_id": "SRC2716_2_1568_coefficients",
        "label": "1568 missing coefficient ledger",
        "path": ROOT / "1568-Y5-RAB-parent-contract-derivation-from-MTS-primitives-or-first-live-ZR-row.md",
        "needles": [
            "COEFF1568_0_ZR",
            "COEFF1568_1_JR",
            "COEFF1568_3_tau_R10",
        ],
        "use": "shows finite internal coefficients and projection kernels remain missing",
    },
    {
        "source_id": "SRC2716_3_1867_object_language",
        "label": "1867 object-language radial-cell audit",
        "path": ROOT / "1867-Y5-R2FR-object-language-radial-cell-constraint-or-finite-ZRJR-intake.md",
        "needles": [
            "TOC1867_1_derived_cell",
            "OLA1867_2_derivative_exclusion",
            "CMA1867_0_locality_scalar",
            "FINT1867_0_ZR",
        ],
        "use": "separates exact identity from unsigned dynamical prohibition",
    },
    {
        "source_id": "SRC2716_4_nonpropagating_constraint",
        "label": "07 nonpropagating reciprocity constraint",
        "path": ROOT / "07-nonpropagating-reciprocity-constraint.md",
        "needles": [
            "S_constraint = integral lambda_R R_AB.",
            "R_AB = 0.",
            "no R_AB kinetic term;",
        ],
        "use": "early exact closure route and kinetic-route demotion",
    },
    {
        "source_id": "SRC2716_5_observer_map",
        "label": "10 observer-map symplectic contract",
        "path": ROOT / "10-observer-map-symplectic-contract.md",
        "needles": [
            "R_AB = ln(T^2 S) = 2 ln(J_q).",
            "gamma - 1 = 0 after R_AB=0.",
            "derive R_AB=0 from the parent theory",
        ],
        "use": "local-GR payoff and the warning that R_AB=0 must be parent-derived",
    },
    {
        "source_id": "SRC2716_6_vacuum_action_contract",
        "label": "04 vacuum reciprocity action contract",
        "path": ROOT / "04-vacuum-reciprocity-action-contract.md",
        "needles": [
            "R_AB = ln(A B) = ln(T^2 S).",
            "d/dr [ W(r,L,fields) dR_AB/dr ] = J_R",
            "J_R = 0 in local vacuum",
        ],
        "use": "finite source equation and no-hair target before the AX1090 closure phase",
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


def parent_protection_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "PPC2716_0_definition_identity",
            "clause": "R_AB = 2 ln(J_q) = ln(T^2 S)",
            "status": "SIGNED_AS_DEFINITION_ONLY",
            "what_it_proves": "the object being protected is unambiguous",
            "what_it_does_not_prove": "R_AB has no kinetic term, source, boundary charge, or readout regeneration",
            "parent_signed": False,
            "claim_credit": False,
            "source_anchor": "1867 TOC1867_1; 10 observer-map identity",
            "next_need": "turn definition into typed parent object-language exclusion if possible",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "PPC2716_1_parent_sorts",
            "clause": "R_AB is auxiliary compatibility data, not a physical scalar",
            "status": "CANDIDATE_NOT_PARENT_SIGNED",
            "what_it_proves": "would block the ordinary scalar countermodel at the type level",
            "what_it_does_not_prove": "typed primitive list is not derived from MTS primitives under AX1090 closure",
            "parent_signed": False,
            "claim_credit": False,
            "source_anchor": "1567 CON1567_0; 2715 AUX2715_1",
            "next_need": "derive parent primitive/constructor grammar from MTS objects rather than closure convenience",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "PPC2716_2_action_image_exhaustion",
            "clause": "ParentGenerate produces algebraic Lambda_R(R_AB-C_AB) only",
            "status": "UNSIGNED_ACTION_IMAGE_EXHAUSTION",
            "what_it_proves": "would remove direct R_AB matter source and independent kinetic additions",
            "what_it_does_not_prove": "no hidden extension marker, coframe determinant, or effective readout can regenerate R_AB terms",
            "parent_signed": False,
            "claim_credit": False,
            "source_anchor": "1567 CON1567_1; 1867 OLA1867_1",
            "next_need": "prove exhaustion of the parent action image",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "PPC2716_3_operator_exclusion",
            "clause": "no D R_AB, D Lambda_R, vertical metric, or Sobolev norm constructor",
            "status": "CONDITIONAL_ON_UNSIGNED_TYPE_RULE",
            "what_it_proves": "would set Z_R and derivative reciprocal hair to theorem-zero",
            "what_it_does_not_prove": "the no-derivative grammar is parent-owned rather than imposed",
            "parent_signed": False,
            "claim_credit": False,
            "source_anchor": "1567 CON1567_5; 2715 AUX2715_2",
            "next_need": "find a parent reason the derivative constructor is illegal",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "PPC2716_4_matter_descent",
            "clause": "delta S_matter / delta R_AB = 0",
            "status": "UNSIGNED_MATTER_DESCENT",
            "what_it_proves": "would kill J_R in the reciprocal Euler equation",
            "what_it_does_not_prove": "mass, clock, EM, material labels, or local source readouts cannot depend on R_AB",
            "parent_signed": False,
            "claim_credit": False,
            "source_anchor": "1567 CON1567_2; 1867 TOC1867_4",
            "next_need": "derive universal matter descent from observed metric/coframe coupling",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "PPC2716_5_boundary_readout_silence",
            "clause": "boundary, corner, and readout terms cannot carry Q_R/R_AB hair",
            "status": "UNSIGNED_BOUNDARY_READOUT_STABILITY",
            "what_it_proves": "would kill B_R, Q_R, tau leakage, and readout regeneration",
            "what_it_does_not_prove": "source-worldtube/corner terms and reduction maps preserve the algebraic constraint",
            "parent_signed": False,
            "claim_credit": False,
            "source_anchor": "1567 CON1567_3; 1567 CON1567_4; 1867 TOC1867_5",
            "next_need": "boundary no-charge theorem or finite B_R/Q_R row",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "PPC2716_6_joint_contract",
            "clause": "CON1567_0 through CON1567_5 all hold together",
            "status": "CONTRACT_WRITTEN_NOT_SIGNED",
            "what_it_proves": "would eliminate J_R, B_R, readout regeneration, and Z_R before local readout",
            "what_it_does_not_prove": "no clause is independently sufficient; local-GR credit cannot be spent yet",
            "parent_signed": False,
            "claim_credit": False,
            "source_anchor": "1567 CON1567_6; 1567 THM1567_0; 2715 AUX2715_4",
            "next_need": "either sign a clause from parent primitives or run finite-residual source acquisition",
            "timestamp_utc": ts(),
        },
    ]


def proof_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "ATT2716_0_identity_route",
            "route": "use R_AB=2 ln(J_q) as compatibility data",
            "result": "EXACT_IDENTITY_BUT_NOT_DYNAMICS",
            "reason": "an identity names the reciprocal cell mode but does not forbid a local action from assigning it stiffness/source terms",
            "countermodel": "L_eff includes 0.5 Z_R |D R_AB|^2 + 0.5 M_R^2 R_AB^2 + J_R R_AB",
            "claim_allowed": False,
            "next_action": "seek typed parent grammar or keep finite coefficients",
            "timestamp_utc": ts(),
        },
        {
            "attempt_id": "ATT2716_1_lambda_constraint_route",
            "route": "insert Lambda_R R_AB or Lambda_R(R_AB-C_AB)",
            "result": "EXACT_IF_INSERTED_CLOSURE_ONLY",
            "reason": "variation gives the desired algebraic condition, but lambda_R origin/zero-stress/Dirac/boundary clauses remain unsigned",
            "countermodel": "closure multiplier can be added by hand without proving it belongs to MTS parent dynamics",
            "claim_allowed": False,
            "next_action": "derive multiplier from parent phase-volume/object-language mechanics",
            "timestamp_utc": ts(),
        },
        {
            "attempt_id": "ATT2716_2_operator_zero_route",
            "route": "declare no derivative constructor for R_AB",
            "result": "CONDITIONAL_ZERO_NOT_SIGNED",
            "reason": "operator exclusion would prove Z_R=0 only after parent sort/action image exhaustion is signed",
            "countermodel": "ordinary locality permits a dimensionless scalar strain with finite Z_R unless the grammar forbids it",
            "claim_allowed": False,
            "next_action": "hunt for parent constructor grammar or source Z_R",
            "timestamp_utc": ts(),
        },
        {
            "attempt_id": "ATT2716_3_source_silence_route",
            "route": "set J_R=B_R=Q_R=0 from vacuum/locality",
            "result": "NO_CHARGE_NOT_DERIVED",
            "reason": "vacuum source silence and asymptotic flatness do not by themselves erase boundary hair or matter-induced reciprocal charge",
            "countermodel": "finite J_eff from matter descent failure, boundary corner term, or readout regeneration",
            "claim_allowed": False,
            "next_action": "separate matter descent proof from boundary no-charge proof",
            "timestamp_utc": ts(),
        },
        {
            "attempt_id": "ATT2716_4_verdict",
            "route": "parent protection contract under AX1090 closure",
            "result": "NO_PROTECTIVE_CLAUSE_PARENT_SIGNED_IN_2716",
            "reason": "definition-level exactness is real, but every claim-making prohibition still needs parent ownership",
            "countermodel": "finite residual operator remains internally consistent and must be bounded if not eliminated",
            "claim_allowed": False,
            "next_action": "emit strict nonclaim finite operator/scaffold and attack normalization next",
            "timestamp_utc": ts(),
        },
    ]


def finite_operator_law_rows() -> list[dict[str, Any]]:
    return [
        {
            "law_id": "LAW2716_0_finite_action",
            "statement": "S_R^finite = integral sqrt(h) [0.5 Z_R h^ij D_i R_AB D_j R_AB + 0.5 M_R^2 R_AB^2 + J_eff R_AB] + B_R boundary",
            "derivation_status": "FALLBACK_ACTION_IF_PARENT_ZERO_FAILS",
            "requires": "finite Z_R; finite M_R^2; source map J_eff; boundary class B_R; normalization of R_AB",
            "claim_credit": False,
            "use": "minimal conservative countermodel and bound branch",
            "timestamp_utc": ts(),
        },
        {
            "law_id": "LAW2716_1_euler_operator",
            "statement": "(-Z_R Delta_h + M_R^2) R_AB = J_eff plus boundary/readout terms",
            "derivation_status": "FORMAL_VARIATION_OF_FALLBACK_ACTION",
            "requires": "positive operator signs and boundary conditions",
            "claim_credit": False,
            "use": "turns vague reciprocal leakage into a bounded residual equation",
            "timestamp_utc": ts(),
        },
        {
            "law_id": "LAW2716_2_transition_length",
            "statement": "ell_R = sqrt(Z_R / M_R^2) when Z_R>0 and M_R^2>0 in the same normalization",
            "derivation_status": "DIMENSIONAL_OPERATOR_RESULT",
            "requires": "numeric same-frame Z_R and M_R^2 or theorem-zero of one branch",
            "claim_credit": False,
            "use": "range scale for R10, PPN, clock, and orbital projections",
            "timestamp_utc": ts(),
        },
        {
            "law_id": "LAW2716_3_amplitude_bound",
            "statement": "|R_AB|_local <= ||G_R|| ||J_eff||, with G_R(k)=1/(Z_R k^2 + M_R^2); long wavelength envelope |R_AB| <= |J_eff|/M_R^2",
            "derivation_status": "GREEN_OPERATOR_BOUND_CONDITIONAL_ON_POSITIVITY",
            "requires": "positive norm, source norm, domain, boundary term, and units",
            "claim_credit": False,
            "use": "first honest amplitude law for the local residual branch",
            "timestamp_utc": ts(),
        },
        {
            "law_id": "LAW2716_4_arena_projection",
            "statement": "residual_i = tau_i R_AB for i in {R10, PPN, clock, orbital}, after each tau_i is derived in the same readout convention",
            "derivation_status": "PROJECTION_TEMPLATE_NOT_SOURCE_READY",
            "requires": "tau_R10, tau_PPN, tau_clock, tau_orbital from parent/readout map",
            "claim_credit": False,
            "use": "blocks scorekeeping until internal coefficients and arena projections exist",
            "timestamp_utc": ts(),
        },
    ]


def finite_row_scaffold_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "FZR2716_0_ZR",
            "quantity": "Z_R",
            "role": "gradient stiffness of reciprocal cell residual",
            "symbolic_formula": "coefficient of 0.5 h^ij D_i R_AB D_j R_AB in the finite fallback action",
            "units_or_dimension": "parent_action_density_weight_for_dimensionless_R_AB_gradient; exact units require parent action normalization",
            "normalization": "R_AB dimensionless; R_AB=2 ln(J_q)=ln(T^2 S)",
            "source_path": str(ROOT / "1567-Y5-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md"),
            "arena_map": "sets ell_R=sqrt(Z_R/M_R^2) and the high-k Green suppression",
            "status": "SOURCE_READY_SYMBOLIC_NONCLAIM",
            "blockers": "MISSING_NUMERIC_PARENT_COEFFICIENT;MISSING_ACTION_NORMALIZATION;MISSING_POSITIVE_OPERATOR_CERTIFICATE",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "row_id": "FZR2716_1_MR2",
            "quantity": "M_R^2",
            "role": "mass/Hessian stiffness suppressing R_AB residual amplitude",
            "symbolic_formula": "coefficient of 0.5 R_AB^2 in the finite fallback action",
            "units_or_dimension": "same_parent_weight_as_Z_R_over_length_squared after normalization",
            "normalization": "same R_AB normalization and same measure as Z_R",
            "source_path": str(ROOT / "1568-Y5-RAB-parent-contract-derivation-from-MTS-primitives-or-first-live-ZR-row.md"),
            "arena_map": "long-wavelength amplitude envelope |R_AB|<=|J_eff|/M_R^2",
            "status": "SOURCE_READY_SYMBOLIC_NONCLAIM",
            "blockers": "MISSING_NUMERIC_PARENT_COEFFICIENT;MISSING_HESSIAN_SOURCE;MISSING_SAME_FRAME_UNITS",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "row_id": "FZR2716_2_JEFF",
            "quantity": "J_eff = J_R + J_boundary + J_readout",
            "role": "effective reciprocal source after matter, boundary, and readout leakage",
            "symbolic_formula": "right-hand side of (-Z_R Delta_h + M_R^2) R_AB = J_eff",
            "units_or_dimension": "Euler-source units conjugate to dimensionless R_AB",
            "normalization": "must use same measure/coframe and source convention as Z_R and M_R^2",
            "source_path": str(ROOT / "1867-Y5-R2FR-object-language-radial-cell-constraint-or-finite-ZRJR-intake.md"),
            "arena_map": "drives residual amplitude entering R10/PPN/clock/orbital projections",
            "status": "SOURCE_READY_SYMBOLIC_NONCLAIM",
            "blockers": "MISSING_MATTER_DESCENT_MAP;MISSING_BOUNDARY_NO_CHARGE_OR_BOUND;MISSING_READOUT_REGENERATION_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "row_id": "FZR2716_3_BR_QR",
            "quantity": "B_R / Q_R",
            "role": "boundary/corner reciprocal charge or flux",
            "symbolic_formula": "boundary term in Green solution or integrated reciprocal charge",
            "units_or_dimension": "boundary momentum/flux conjugate to dimensionless R_AB",
            "normalization": "same boundary orientation and domain as local source worldtube",
            "source_path": str(ROOT / "04-vacuum-reciprocity-action-contract.md"),
            "arena_map": "can mimic exterior hair even when bulk J_R is small",
            "status": "SOURCE_READY_SYMBOLIC_NONCLAIM",
            "blockers": "MISSING_BOUNDARY_CLASS;MISSING_NO_CHARGE_THEOREM;MISSING_FINITE_FLUX_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "row_id": "FZR2716_4_TAU_R10",
            "quantity": "tau_R10",
            "role": "projection from R_AB residual to short-range alpha(lambda) comparison",
            "symbolic_formula": "alpha_R10(lambda) = tau_R10(lambda;source,readout) * R_AB_profile",
            "units_or_dimension": "dimensionless alpha per dimensionless R_AB after source normalization",
            "normalization": "must pair internal MTS source normalization with external R10 convention",
            "source_path": str(ROOT / "1567-Y5-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md"),
            "arena_map": "R10",
            "status": "SOURCE_READY_SYMBOLIC_NONCLAIM",
            "blockers": "MISSING_TAU_R10_PROJECTION;MISSING_SOURCE_TEST_CHARGE_MAP;MISSING_NUMERIC_INTERNAL_COEFFICIENTS",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "row_id": "FZR2716_5_TAU_LOCAL",
            "quantity": "tau_PPN; tau_clock; tau_orbital",
            "role": "projection from R_AB residual to local metric, clock, and orbital residual vectors",
            "symbolic_formula": "residual_i = tau_i * G_R[J_eff] for i in PPN, clock, orbital",
            "units_or_dimension": "arena-specific residual per dimensionless R_AB",
            "normalization": "same observed metric/readout convention as local-GR reduction",
            "source_path": str(ROOT / "10-observer-map-symplectic-contract.md"),
            "arena_map": "PPN;clock;orbital",
            "status": "SOURCE_READY_SYMBOLIC_NONCLAIM",
            "blockers": "MISSING_TAU_PPN_PROJECTION;MISSING_TAU_CLOCK_PROJECTION;MISSING_TAU_ORBITAL_PROJECTION;MISSING_LOCAL_READOUT_KERNEL",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE2716_0_parent_protection",
            "claim": "R_AB parent protection contract is signed",
            "status": "BLOCKED",
            "required_before_claim": "all CON1567_0-5 clauses parent-signed under AX1090 closure",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "gate_id": "GATE2716_1_ZR_zero",
            "claim": "Z_R=0 theorem-zero",
            "status": "BLOCKED",
            "required_before_claim": "parent no-derivative grammar or signed vertical-null contradiction",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "gate_id": "GATE2716_2_JEFF_zero",
            "claim": "J_eff=0 including matter, boundary, and readout",
            "status": "BLOCKED",
            "required_before_claim": "matter descent, boundary no-charge, and readout stability theorem",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "gate_id": "GATE2716_3_local_GR_Newton",
            "claim": "local GR/Newton reduction from MTS",
            "status": "BLOCKED",
            "required_before_claim": "q_R/beta/local residual vector zero or bounded below experimental thresholds",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "gate_id": "GATE2716_4_R10_PPN_clock_orbital",
            "claim": "finite branch passes local tests",
            "status": "BLOCKED",
            "required_before_claim": "numeric Z_R,M_R^2,J_eff,B_R and tau projections with source paths",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "gate_id": "GATE2716_5_public_or_github",
            "claim": "public-facing update",
            "status": "NOT_REQUESTED_BLOCKED_BY_PRIVATE_SCOPE",
            "required_before_claim": "explicit user request and public-safe claim audit",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
    ]


def blocker_stack_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BLK2716_0_parent_object_language",
            "missing_item": "typed parent primitive/constructor grammar for R_AB",
            "effect": "cannot forbid independent R_AB scalar countermodel",
            "best_next_attack": "derive from motion-time-space primitive map or keep finite row",
            "claim_blocked": "Z_R zero; local GR",
            "timestamp_utc": ts(),
        },
        {
            "blocker_id": "BLK2716_1_action_image_exhaustion",
            "missing_item": "proof ParentGenerate has no hidden R_AB derivative/source slots",
            "effect": "operator zero remains a rule, not a theorem",
            "best_next_attack": "write normal-form/exhaustion theorem or source Z_R",
            "claim_blocked": "q_R zero; R10/PPN",
            "timestamp_utc": ts(),
        },
        {
            "blocker_id": "BLK2716_2_matter_boundary_readout",
            "missing_item": "J_R, B_R, Q_R, and readout regeneration zero or finite bounds",
            "effect": "local source can move R_AB away from zero",
            "best_next_attack": "split matter descent from boundary no-charge",
            "claim_blocked": "PPN;clock;orbital;local GR",
            "timestamp_utc": ts(),
        },
        {
            "blocker_id": "BLK2716_3_numeric_normalization",
            "missing_item": "same-frame Z_R, M_R^2, J_eff, tau_i numerical normalization",
            "effect": "finite branch cannot score against data",
            "best_next_attack": "Green-kernel normalization runner with source-ready symbolic rows",
            "claim_blocked": "R10;PPN;clock;orbital comparison",
            "timestamp_utc": ts(),
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2716_0_identity_signed_only",
            "decision": "accept R_AB identity as exact but not claim-making",
            "rationale": "definition-level success is real and useful, but it does not remove dynamics",
            "allowed": True,
            "claim_credit": False,
            "timestamp_utc": ts(),
        },
        {
            "decision_id": "DEC2716_1_no_parent_clause_signed",
            "decision": "do not promote parent protection contract in 2716",
            "rationale": "each protective clause still depends on unsigned parent grammar, matter descent, or boundary/readout silence",
            "allowed": True,
            "claim_credit": False,
            "timestamp_utc": ts(),
        },
        {
            "decision_id": "DEC2716_2_finite_operator_branch",
            "decision": "emit finite R_AB operator law and strict nonclaim source-ready scaffold",
            "rationale": "if the zero theorem is not derivable yet, the residual must be bounded rather than hidden",
            "allowed": True,
            "claim_credit": False,
            "timestamp_utc": ts(),
        },
        {
            "decision_id": "DEC2716_3_next_target",
            "decision": "attack Green-kernel normalization or parent coefficient zero next",
            "rationale": "this is the shortest path to either a theorem-zero or a testable finite residual bound",
            "allowed": True,
            "claim_credit": False,
            "timestamp_utc": ts(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2716_0_selected",
            "status": "selected_primary",
            "target_doc": "2717-Y5-R2FR-finite-RAB-green-kernel-normalization-or-parent-coefficient-zero-under-AX1090-closure.md",
            "target_script": "scripts/Y5_R2FR_finite_RAB_green_kernel_normalization_or_parent_coefficient_zero_under_AX1090_closure_2717.py",
            "mission": "derive the same-frame finite R_AB Green-kernel amplitude law with explicit normalization requirements, or prove Z_R/J_eff theorem-zero from parent coefficients",
            "acceptance": "one parent coefficient is theorem-zero/source-normalized, or all finite residual rows gain explicit unit/source/normalization blockers without claim leakage",
            "forbidden": "score R10/PPN/clock/orbital; treat symbolic rows as numeric; edit formalization-workbench; GitHub action",
            "selected": True,
            "claim_allowed": False,
            "timestamp_utc": ts(),
        }
    ]


def project_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "snapshot_id": "SNAP2716_0_status",
            "sector": "local-GR bridge",
            "state": "conditional exact route exists, but parent-signed protection still absent",
            "confidence": "promising structure, not claimable",
            "next_need": "parent object-language or finite residual normalization",
            "timestamp_utc": ts(),
        },
        {
            "snapshot_id": "SNAP2716_1_derived_piece",
            "sector": "reciprocal cell identity",
            "state": "R_AB=2 ln(J_q)=ln(T^2 S) remains exact and useful",
            "confidence": "high as definition",
            "next_need": "prove this identity is compatibility data only",
            "timestamp_utc": ts(),
        },
        {
            "snapshot_id": "SNAP2716_2_finite_branch",
            "sector": "finite local residuals",
            "state": "fallback operator (-Z_R Delta + M_R^2)R_AB=J_eff now explicit",
            "confidence": "useful nonclaim scaffold",
            "next_need": "numeric/source normalization or theorem-zero",
            "timestamp_utc": ts(),
        },
        {
            "snapshot_id": "SNAP2716_3_public_status",
            "sector": "publication/GitHub",
            "state": "private checkpoint only",
            "confidence": "safe",
            "next_need": "no public action unless explicitly requested",
            "timestamp_utc": ts(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "COPY2716_0_local_arena_projection",
            "source_table": "P8_Y5_R2FR_2716_FINITE_ZR_JR_RAB_ROW_SCAFFOLD.csv",
            "copy_path": str(BRANCH_OUTPUTS["local_arena_projection"]),
            "purpose": "quarantine local R10/PPN/clock/orbital projection rows as nonclaim",
            "exists": BRANCH_OUTPUTS["local_arena_projection"].exists(),
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "copy_id": "COPY2716_1_finite_source_weight",
            "source_table": "P8_Y5_R2FR_2716_FINITE_ZR_JR_RAB_ROW_SCAFFOLD.csv",
            "copy_path": str(BRANCH_OUTPUTS["finite_source_weight"]),
            "purpose": "quarantine source-weight coefficient scaffold as nonclaim",
            "exists": BRANCH_OUTPUTS["finite_source_weight"].exists(),
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "copy_id": "COPY2716_2_next_queue",
            "source_table": "P8_Y5_R2FR_2716_NEXT_TARGET.csv",
            "copy_path": str(BRANCH_OUTPUTS["next_queue"]),
            "purpose": "queue 2717 without touching formalization-workbench",
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
        except Exception as exc:  # pragma: no cover - validation reporting path
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
    parent_audit: list[dict[str, Any]],
    finite_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    branches: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    csv_paths = [
        OUTPUTS["source_register"],
        OUTPUTS["parent_protection_audit"],
        OUTPUTS["proof_attempts"],
        OUTPUTS["finite_operator_law"],
        OUTPUTS["finite_row_scaffold"],
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
    no_parent_claim = all(row["claim_credit"] is False for row in parent_audit)
    finite_nonclaim = all(row["valid_for_claim"] is False for row in finite_rows)
    finite_has_sources = all(Path(row["source_path"]).exists() for row in finite_rows)
    branch_ok = all(Path(row["copy_path"]).exists() and row["valid_for_claim"] is False for row in branches)
    gates_false = all(row["claim_allowed"] is False for row in gates)
    formalization_count = formalization_recent_changed_count()
    no_github_outputs = all(".git" not in str(path).lower() and "github" not in str(path).lower() for path in csv_paths)
    rows = [
        {
            "validation_id": "VAL2716_0_sources",
            "passed": source_ok,
            "detail": "all source paths exist and required needles found" if source_ok else "missing source or needle",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2716_1_doc_written",
            "passed": DOC.exists(),
            "detail": str(DOC),
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2716_2_csv_parse",
            "passed": csv_ok,
            "detail": csv_detail,
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2716_3_no_parent_protection_claim",
            "passed": no_parent_claim,
            "detail": "definition identity receives no claim credit; all protective clauses remain unsigned",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2716_4_finite_rows_nonclaim",
            "passed": finite_nonclaim,
            "detail": "all finite Z_R/J_eff/tau rows keep valid_for_claim=false",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2716_5_finite_rows_have_local_sources",
            "passed": finite_has_sources,
            "detail": "every finite scaffold row points to an existing local source path",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2716_6_branch_copies",
            "passed": branch_ok,
            "detail": "branch copies exist and remain nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2716_7_claim_gates_all_false",
            "passed": gates_false,
            "detail": "no R10/PPN/local-GR/GitHub claim gate opened",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2716_8_no_formalization_recent_changes",
            "passed": formalization_count == 0,
            "detail": f"formalization_recent_changed_count={formalization_count}",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2716_9_no_github_outputs",
            "passed": no_github_outputs,
            "detail": "no GitHub/public-output path was written",
            "timestamp_utc": ts(),
        },
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(
        {
            "validation_id": "VAL2716_OVERALL",
            "passed": overall,
            "detail": "2716 keeps the parent-protection contract unsigned, derives the finite R_AB operator fallback, emits strict nonclaim finite rows, and selects 2717 normalization/theorem-zero work",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    parent_audit: list[dict[str, Any]],
    attempts: list[dict[str, Any]],
    laws: list[dict[str, Any]],
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
        "# 2716 - Y5/R2FR Parent Protection Contract Or Finite Z_R Row Under AX1090 Closure",
        "",
        "## Private Verdict",
        "",
        "2716 tries the clean route first: sign at least one claim-making parent-protection clause for `R_AB`. It does **not** close. The exact identity `R_AB=2 ln(J_q)=ln(T^2 S)` is kept as a real definition-level result, but definition is not dynamics. Without a parent-owned type/action-image theorem, a finite reciprocal residual countermodel survives.",
        "",
        "So 2716 moves the branch forward honestly: the residual is now represented by a strict nonclaim finite operator, `(-Z_R Delta_h + M_R^2) R_AB = J_eff`, with `ell_R=sqrt(Z_R/M_R^2)` and arena residuals `residual_i=tau_i R_AB`. No local-GR, Newton, R10, PPN, clock, orbital, or public/GitHub claim is opened.",
        "",
        "## Claim Ceiling",
        "",
        "- No parent-protection clause is treated as signed from 2716.",
        "- No `Z_R=0`, `J_eff=0`, `q_R=0`, `beta/gamma=GR`, local-GR, Newton, R10, PPN, clock, or orbital pass is claimed.",
        "- Symbolic finite rows are source-ready scaffolds only; they are not numeric coefficients.",
        "- No `formalization-workbench` edits and no GitHub/public-output action are allowed from this checkpoint.",
        "",
        "## Source Register",
        "",
        markdown_table(
            sources,
            ["source_id", "label", "path", "exists", "required_needles_found", "missing_needles", "use", "claim_credit"],
        ),
        "",
        "## Parent Protection Audit",
        "",
        markdown_table(
            parent_audit,
            [
                "audit_id",
                "clause",
                "status",
                "what_it_proves",
                "what_it_does_not_prove",
                "parent_signed",
                "claim_credit",
                "source_anchor",
                "next_need",
            ],
        ),
        "",
        "## Proof Attempt Ledger",
        "",
        markdown_table(
            attempts,
            ["attempt_id", "route", "result", "reason", "countermodel", "claim_allowed", "next_action"],
        ),
        "",
        "## Finite R_AB Operator Law",
        "",
        markdown_table(
            laws,
            ["law_id", "statement", "derivation_status", "requires", "claim_credit", "use"],
        ),
        "",
        "## Finite Z_R/J_eff/Tau Row Scaffold",
        "",
        markdown_table(
            finite_rows,
            [
                "row_id",
                "quantity",
                "role",
                "symbolic_formula",
                "units_or_dimension",
                "normalization",
                "source_path",
                "arena_map",
                "status",
                "blockers",
                "valid_for_claim",
            ],
        ),
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
        markdown_table(
            next_rows,
            ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "claim_allowed"],
        ),
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
        "This is a useful checkpoint, but not because it magically proves local GR. It tells us exactly what kind of bridge we still need. `R_AB` is nailed down as the right object, but we still have to prove the parent theory refuses to let it behave like a normal scalar. Until that proof exists, the honest engineering version is the finite operator law: stiffness, mass, source, boundary, and arena projection. That is now precise enough to attack instead of circling the same fog-bank.",
        "",
        "Best next strike: 2717 should either find a parent reason one of `Z_R`, `J_eff`, or the derivative constructor is zero, or normalize the finite Green-kernel branch enough that local tests become a real bound problem rather than a slogan.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    for directory in (RESIDUALS, LOCAL_BOUNDS, SOURCE_WEIGHT, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    parent_audit = parent_protection_audit_rows()
    attempts = proof_attempt_rows()
    laws = finite_operator_law_rows()
    finite_rows = finite_row_scaffold_rows()
    gates = claim_gate_rows()
    blockers = blocker_stack_rows()
    decisions = decision_ledger_rows()
    next_rows = next_target_rows()
    snapshot = project_snapshot_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["parent_protection_audit"], parent_audit)
    write_csv(OUTPUTS["proof_attempts"], attempts)
    write_csv(OUTPUTS["finite_operator_law"], laws)
    write_csv(OUTPUTS["finite_row_scaffold"], finite_rows)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["blocker_stack"], blockers)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)
    write_csv(OUTPUTS["project_snapshot"], snapshot)

    write_csv(BRANCH_OUTPUTS["local_arena_projection"], finite_rows)
    write_csv(BRANCH_OUTPUTS["finite_source_weight"], finite_rows)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_rows)

    branches = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], branches)

    pending_validation = [
        {
            "validation_id": "VAL2716_PENDING",
            "passed": False,
            "detail": "pre-validation placeholder for first doc write",
            "timestamp_utc": ts(),
        }
    ]
    write_doc(
        sources,
        parent_audit,
        attempts,
        laws,
        finite_rows,
        gates,
        blockers,
        decisions,
        next_rows,
        snapshot,
        branches,
        pending_validation,
    )

    validation = validation_rows(sources, parent_audit, finite_rows, gates, branches)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(
        sources,
        parent_audit,
        attempts,
        laws,
        finite_rows,
        gates,
        blockers,
        decisions,
        next_rows,
        snapshot,
        branches,
        validation,
    )

    overall = next(row for row in validation if row["validation_id"] == "VAL2716_OVERALL")
    print(f"2716 complete: {overall['passed']} - {overall['detail']}")
    print(DOC)


if __name__ == "__main__":
    main()
