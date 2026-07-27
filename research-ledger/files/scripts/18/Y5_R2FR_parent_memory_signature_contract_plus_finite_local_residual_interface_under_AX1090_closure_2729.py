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

DOC = ROOT / "2729-Y5-R2FR-parent-memory-signature-contract-plus-finite-local-residual-interface-under-AX1090-closure.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2729_SOURCE_REGISTER.csv",
    "contract": RESIDUALS / "P8_Y5_R2FR_2729_PARENT_MEMORY_SIGNATURE_CONTRACT.csv",
    "audit": RESIDUALS / "P8_Y5_R2FR_2729_SIGNATURE_CLAUSE_ACTIVATION_AUDIT.csv",
    "finite": RESIDUALS / "P8_Y5_R2FR_2729_FINITE_MEMORY_RESIDUAL_INPUT_INTERFACE.csv",
    "arena": RESIDUALS / "P8_Y5_R2FR_2729_ARENA_PROJECTION_INTERFACE.csv",
    "r10": RESIDUALS / "P8_Y5_R2FR_2729_R10_ALPHA_SMOKE_ROWS_NONCLAIM.csv",
    "refusal": RESIDUALS / "P8_Y5_R2FR_2729_REFUSAL_AND_SCORE_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2729_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2729_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2729_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2729_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_interface": LOCAL_BOUNDS / "memory_finite_residual_interface_2729_NONCLAIM.csv",
    "r10_smoke": LOCAL_BOUNDS / "memory_R10_alpha_smoke_rows_2729_NONCLAIM.csv",
    "source_weight_contract": SOURCE_WEIGHT / "memory_parent_signature_contract_2729_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2729_MEMORY_FIRST_SOURCE_ROW_OR_TEST_PREP_NEXT.csv",
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


def markdown_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    head = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    body = [
        "| " + " | ".join(str(row.get(col, "")).replace("\n", " ") for col in cols) + " |"
        for row in rows
    ]
    return "\n".join([head, sep, *body])


def source_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC2729_0_2728_handoff",
            "path": DOC.parent / "2728-Y5-R2FR-memory-positive-operator-local-silence-or-residual-row-under-AX1090-closure.md",
            "needles": ["NEXT2728_0_selected", "EMEM2728_6_E_memory_scalar_generator", "VAL2728_OVERALL"],
            "description": "2728 selected parent signature plus finite residual interface",
        },
        {
            "source_id": "SRC2729_1_2037_finite_runner_pattern",
            "path": DOC.parent / "2037-Y5-R2FR-finite-local-residual-runner-and-bound-map.md",
            "needles": ["Finite Local Residual Runner", "CAND2037_0_ZRR", "AP2037_0_R10"],
            "description": "existing finite residual refusal/scoring interface pattern",
        },
        {
            "source_id": "SRC2729_2_899_bound_interface_pattern",
            "path": DOC.parent / "899-Y5-R10-trace-residual-vector-source-pack-and-local-bound-interface.md",
            "needles": ["Trace Residual Source Pack", "LBI899_0_R10_alpha_lambda", "RSP899_0"],
            "description": "cross-arena local bound interface pattern",
        },
        {
            "source_id": "SRC2729_3_2626_memory_owner",
            "path": DOC.parent / "2626-Y5-R2FR-parent-memory-operator-owner-hunt-or-memory-residual-template.md",
            "needles": ["MOA2626_9_verdict", "MRI2626_6_observable_vector", "ZPT2626_4_current_verdict"],
            "description": "memory owner/sign/source template",
        },
        {
            "source_id": "SRC2729_4_2627_source_boundary",
            "path": DOC.parent / "2627-Y5-R2FR-parent-memory-source-boundary-map-or-finite-residual-bound-pack.md",
            "needles": ["JX2627_6_total_verdict", "RBP2627_4_local_projection", "BZ2627_5_current_verdict"],
            "description": "J_X and boundary finite residual rows",
        },
        {
            "source_id": "SRC2729_5_1980_sign_contract",
            "path": DOC.parent / "1980-Y5-R2FR-parent-memory-positivity-lemma-or-closure.md",
            "needles": ["GATE1980_0_Zm", "GATE1980_1_M2", "NEG1980_0_extremum_not_gap"],
            "description": "Z_m/M_X^2 sign and extremum-not-gap warnings",
        },
        {
            "source_id": "SRC2729_6_2728_local_copy",
            "path": LOCAL_BOUNDS / "memory_positive_operator_residual_rows_2728_NONCLAIM.csv",
            "needles": ["EMEM2728_6_E_memory_scalar_generator", "PARENT_OWNER_PLUS_SIGN_PLUS_SOURCE_PLUS_BOUNDARY_PLUS_PROJECTION"],
            "description": "machine-readable 2728 local-bound handoff",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        path: Path = spec["path"]
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="ignore") if exists else ""
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "description": spec["description"],
                "source_path": str(path),
                "exists": exists,
                "needles_present": not missing,
                "missing_needles": ";".join(missing),
                "valid_for_claim": False,
            }
        )
    return rows


def contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "PMC2729_0_field_owner",
            "parent_action_clause": "Conf_parent contains a typed memory/class scalar X or a quotient scalar X=q_X(Phi), with units and admissible delta X variations.",
            "would_sign": "parent X owner",
            "needed_source": "field list plus action argument list showing X or q_X(Phi)",
            "current_status": "UNSIGNED_CONTRACT",
            "failure_if_absent": "E_memory_parent_owner remains active",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PMC2729_1_domain_selector",
            "parent_action_clause": "The local exterior D and boundary class partial D are selected by covariant parent conditions, not by posthoc scoring/readout.",
            "would_sign": "domain D and zero-mode class",
            "needed_source": "parent local-branch/domain selector with no wall-stress source",
            "current_status": "UNSIGNED_CONTRACT",
            "failure_if_absent": "domain wall/source-selector residual remains active",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PMC2729_2_quadratic_block",
            "parent_action_clause": "The X-sector second variation contains 1/2 int_D sqrt(h)[Z_X h^ij partial_i X partial_j X + M_X^2 X^2] plus explicitly bounded corrections.",
            "would_sign": "operator L_X",
            "needed_source": "second-variation calculation or parent action term",
            "current_status": "UNSIGNED_CONTRACT",
            "failure_if_absent": "operator remains ansatz/candidate only",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PMC2729_3_positive_signs",
            "parent_action_clause": "Z_X>=Z_min>0 and M_X^2>=0, or M_X^2>=M_min^2>0 after quotienting constant/gauge zero modes; correction norm eta_X is below the spectral floor.",
            "would_sign": "positive operator and lambda_gap",
            "needed_source": "field-space metric sign, strict Hessian or spectral gap theorem, correction bound",
            "current_status": "UNSIGNED_CONTRACT",
            "failure_if_absent": "positive-operator proof cannot activate",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PMC2729_4_source_decomposition",
            "parent_action_clause": "J_X splits into kinetic-affine, matter, observed-slot, chi-wall, boundary, history and readout components, each zero by theorem or bounded with units.",
            "would_sign": "J_X=0 or finite source norm",
            "needed_source": "component variation map and no-source/no-marker clauses",
            "current_status": "UNSIGNED_CONTRACT",
            "failure_if_absent": "finite J_X norm row required",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PMC2729_5_boundary_zero",
            "parent_action_clause": "Boundary term n_i A^ij X partial_j X vanishes, is nonnegative, is Dirichlet-fixed, or is replaced by a sourced boundary_lift_norm.",
            "would_sign": "boundary no-hair or finite boundary lift",
            "needed_source": "parent boundary condition, exact/topological primitive, or boundary norm",
            "current_status": "UNSIGNED_CONTRACT",
            "failure_if_absent": "boundary memory residual can leak into PPN/clocks/R10/orbits",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PMC2729_6_no_tower_return",
            "parent_action_clause": "Integrating out or solving X does not regenerate an R2/f(R)/R11-like local carrier or source-coupled pole.",
            "would_sign": "no hidden memory/scalar tower",
            "needed_source": "effective-action after-elimination audit",
            "current_status": "UNSIGNED_CONTRACT",
            "failure_if_absent": "E_memory_tower_return remains active",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PMC2729_7_observable_projection",
            "parent_action_clause": "Observable maps K_R10, K_PPN, K_clock, K_Gdot, K_orbital and K_WEP convert X/grad X into bounded local residual vectors with units.",
            "would_sign": "arena scoring interface",
            "needed_source": "weak-field/readout/source-normalization response map",
            "current_status": "UNSIGNED_CONTRACT",
            "failure_if_absent": "finite memory residual remains not scoreable",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PMC2729_8_activation_verdict",
            "parent_action_clause": "All previous clauses are parent-signed before memory no-hair or finite local score is allowed.",
            "would_sign": "memory branch closure",
            "needed_source": "PMC2729_0..7 pass with source paths",
            "current_status": "CONTRACT_READY_NOT_ACTIVATED",
            "failure_if_absent": "no local-GR/Newton/R10/PPN/clock/orbital/WEP claim",
            "valid_for_claim": False,
        },
    ]


def audit_rows() -> list[dict[str, Any]]:
    rows = []
    for row in contract_rows():
        rows.append(
            {
                "audit_id": row["clause_id"].replace("PMC", "PMA"),
                "clause_id": row["clause_id"],
                "signed_now": False,
                "why_not_signed": row["current_status"],
                "required_evidence": row["needed_source"],
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    return rows


def finite_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "MFI2729_0_lambda_gap",
            "quantity": "lambda_gap_X",
            "formula": "lambda_gap_X >= Z_min*lambda_1(D) + M_min^2 - eta_X after zero-mode projection",
            "value": "MISSING_VALUE",
            "units": "1/length^2",
            "required_sources": "Z_min;lambda_1(D);M_min^2;eta_X;zero-mode class",
            "blocks": "X amplitude, R10 range, PPN/clock/orbital suppression",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
        },
        {
            "input_id": "MFI2729_1_JX_norm",
            "quantity": "||J_X||",
            "formula": "||J_X|| <= sum ||J_X^component|| over kinetic,matter,observed,chi,boundary,history,readout",
            "value": "MISSING_VALUE",
            "units": "operator-normalized source units",
            "required_sources": "component source map with units or zero theorem",
            "blocks": "all finite memory amplitude rows",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
        },
        {
            "input_id": "MFI2729_2_boundary_lift",
            "quantity": "boundary_lift_norm_X",
            "formula": "norm of nonzero boundary data or proof boundary contribution vanishes",
            "value": "MISSING_VALUE",
            "units": "X norm or flux norm",
            "required_sources": "parent boundary condition; exact primitive; zero-flux/Dirichlet class",
            "blocks": "PPN/clock/R10/orbital boundary leakage",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
        },
        {
            "input_id": "MFI2729_3_X_L2",
            "quantity": "||X||_L2",
            "formula": "||X||_L2 <= (||J_X||_L2 + boundary_lift_norm_X)/lambda_gap_X",
            "value": "DERIVED_ONLY_IF_INPUTS_EXIST",
            "units": "X units*sqrt(volume)",
            "required_sources": "MFI2729_0;MFI2729_1;MFI2729_2",
            "blocks": "observable projection amplitude",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
        },
        {
            "input_id": "MFI2729_4_gradX_L2",
            "quantity": "||grad X||_L2",
            "formula": "Z_min||grad X||_L2^2 + M_min^2||X||_L2^2 <= ||J_X||||X|| + boundary terms",
            "value": "DERIVED_ONLY_IF_INPUTS_EXIST",
            "units": "X units/length*sqrt(volume)",
            "required_sources": "Z_min;M_min^2;J_X;boundary terms",
            "blocks": "gradient-sensitive PPN/clock/orbital rows",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
        },
        {
            "input_id": "MFI2729_5_X_inf",
            "quantity": "||X||_infty",
            "formula": "||X||_infty <= C_ell(D,Z,M)(||J_X||_Lp + boundary_norm)",
            "value": "MISSING_REGULARITY_CONSTANT",
            "units": "X units",
            "required_sources": "elliptic constant, p-norm source, domain regularity",
            "blocks": "pointwise local residual claims",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
        },
        {
            "input_id": "MFI2729_6_source_charge",
            "quantity": "Q_X/m",
            "formula": "matter/source charge projection along X, or zero by quotient-blind matter theorem",
            "value": "MISSING_VALUE",
            "units": "dimensionless or parent charge per inertial mass",
            "required_sources": "matter functor/source worldtube/quotient-blindness theorem",
            "blocks": "R10/WEP/orbital fifth-force rows",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
        },
        {
            "input_id": "MFI2729_7_projection_vector",
            "quantity": "K_i,K_i_grad",
            "formula": "Delta O_i <= K_i||X|| + K_i_grad||grad X||",
            "value": "MISSING_VALUE",
            "units": "arena-specific",
            "required_sources": "R10, PPN, clock, Gdot, orbital, WEP response maps",
            "blocks": "every empirical score",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
        },
    ]


def arena_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena_id": "APR2729_0_R10",
            "arena": "R10_short_range_inverse_square",
            "prediction_shape": "lambda_X=sqrt(Z_X/M_X^2); alpha_X_AB=(Q_XA/m_A)*(Q_XB/m_B)/(4*pi*Z_X*G_obs), only after all inputs are sourced",
            "requires_memory_inputs": "Z_X;M_X^2;Q_X/m;G_obs normalization;lambda_gap",
            "requires_bound_inputs": "claim-grade alpha_bound(lambda) curve",
            "current_status": "BLOCKED_MISSING_MEMORY_INPUTS",
            "valid_for_claim": False,
        },
        {
            "arena_id": "APR2729_1_PPN",
            "arena": "PPN_solar_system",
            "prediction_shape": "gamma-1,beta-1,alpha_i,xi = K_PPN_i*epsilon_X after observed-metric gauge/source-normalization split",
            "requires_memory_inputs": "K_PPN_i;epsilon_X from ||X||/||gradX||;source-normalization map",
            "requires_bound_inputs": "Cassini/VLBI/ephemeris/preferred-frame bound rows",
            "current_status": "BLOCKED_MISSING_WEAK_FIELD_RESPONSE",
            "valid_for_claim": False,
        },
        {
            "arena_id": "APR2729_2_CLOCK_GDOT",
            "arena": "clock_redshift_and_Gdot",
            "prediction_shape": "delta nu/nu=K_clock||X||+K_clock_grad||gradX||; Gdot/G=K_Gdot*memory_tail",
            "requires_memory_inputs": "clock functional, same-frame map, history-tail/boundary split",
            "requires_bound_inputs": "clock comparison/redshift/Gdot bound source rows",
            "current_status": "BLOCKED_MISSING_CLOCK_FUNCTIONAL",
            "valid_for_claim": False,
        },
        {
            "arena_id": "APR2729_3_ORBITAL",
            "arena": "orbital_Newton_source",
            "prediction_shape": "delta a/a_N includes alpha_X exp(-r/lambda_X)(1+r/lambda_X) plus GM/source-normalization residue",
            "requires_memory_inputs": "alpha_X;lambda_X;C_source;delta_GM;chosen orbital observable",
            "requires_bound_inputs": "LLR/ephemeris/Gdot/anomalous acceleration source rows",
            "current_status": "BLOCKED_MISSING_ORBITAL_MAP",
            "valid_for_claim": False,
        },
        {
            "arena_id": "APR2729_4_WEP",
            "arena": "WEP_material_composition",
            "prediction_shape": "eta_AB controlled by Delta_AB(Q_X/m) or zero by no-marker theorem",
            "requires_memory_inputs": "material/source charge split; species functional; no-marker theorem or numeric delta",
            "requires_bound_inputs": "MICROSCOPE/Eotvos material-pair bound rows",
            "current_status": "BLOCKED_MISSING_MATERIAL_SOURCE",
            "valid_for_claim": False,
        },
        {
            "arena_id": "APR2729_5_LOCAL_GR_AGGREGATE",
            "arena": "local_GR_Newton_reduction",
            "prediction_shape": "memory residual must be theorem-zero or below all local arenas while EH/no-extension/source-normalization gates also close",
            "requires_memory_inputs": "all MFI2729 rows plus non-memory local-GR gates",
            "requires_bound_inputs": "R10;PPN;WEP;clock;orbital;Newton source-normalization evidence",
            "current_status": "BLOCKED_MEMORY_IS_ONE_GATE_NOT_WHOLE_PROOF",
            "valid_for_claim": False,
        },
    ]


def r10_rows() -> list[dict[str, Any]]:
    return [
        {
            "model_id": "MTS_memory_residual_vector",
            "branch_id": "R10_memory_symbolic_refusal",
            "curve_id": "MR2729_R10_0_missing_alpha",
            "lambda_value": "MISSING_LAMBDA_X",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_ALPHA_X",
            "alpha_bound": "MISSING_BOUND_LOOKUP",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "force_law_form": "Yukawa-like alpha_X_AB exp(-r/lambda_X), nonclaim placeholder",
            "derivation_status": "MISSING_ZX_MX2_QX_PARENT_INPUTS",
            "formula_reference": "alpha_X_AB=(Q_XA/m_A)*(Q_XB/m_B)/(4*pi*Z_X*G_obs)",
            "valid_for_claim": False,
            "notes": "must fail/refuse until lambda_X, alpha_X, source paths, units and bound curve provenance are claim-ready",
        },
        {
            "model_id": "MTS_memory_zero_route",
            "branch_id": "R10_memory_zero_unsigned",
            "curve_id": "MR2729_R10_1_unsigned_zero",
            "lambda_value": "MISSING_NO_LOCAL_MEMORY_CARRIER_PROOF",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_ZERO_THEOREM_NOT_SIGNED",
            "alpha_bound": "MISSING_BOUND_LOOKUP",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "force_law_form": "zero only if memory no-hair/source charge theorem is parent-signed",
            "derivation_status": "ZERO_ROUTE_UNSIGNED_NONCLAIM",
            "formula_reference": "alpha_X=0 only if X=0 or Q_X=0 is parent-signed",
            "valid_for_claim": False,
            "notes": "keeps the honest zero route visible without converting it into a pass",
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "REF2729_0_signature", "gate": "parent memory signature accepted", "status": "REFUSED", "reason": "all contract clauses are unsigned", "score_allowed": False, "valid_for_claim": False},
        {"gate_id": "REF2729_1_finite_values", "gate": "finite residual rows accepted", "status": "REFUSED", "reason": "values/units/source paths/equation refs missing", "score_allowed": False, "valid_for_claim": False},
        {"gate_id": "REF2729_2_r10", "gate": "R10 alpha(lambda) smoke score", "status": "REFUSED", "reason": "lambda_X and alpha_X are placeholders and bound curve is not invoked as claim-ready", "score_allowed": False, "valid_for_claim": False},
        {"gate_id": "REF2729_3_local_gr", "gate": "local GR/Newton promotion", "status": "REFUSED", "reason": "memory branch is unresolved and other EH/no-extension gates remain outside this file", "score_allowed": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2729_0_contract_written",
            "decision": "PARENT_MEMORY_SIGNATURE_CONTRACT_WRITTEN",
            "rationale": "the exact clauses that would activate memory no-hair are now explicit and source-checkable",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2729_1_interface_written",
            "decision": "FINITE_MEMORY_RESIDUAL_INTERFACE_WRITTEN",
            "rationale": "failed proof route now becomes concrete lambda_gap/J_X/boundary/K_i rows instead of fog",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2729_2_no_score",
            "decision": "DO_NOT_RUN_CLAIM_SCORE",
            "rationale": "all prediction rows are placeholders or unsigned theorem routes",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2729_0_selected",
            "status": "selected_primary",
            "target_doc": "2730-Y5-R2FR-memory-first-source-row-acquisition-or-local-test-refusal-smoke-under-AX1090-closure.md",
            "target_script": "scripts/Y5_R2FR_memory_first_source_row_acquisition_or_local_test_refusal_smoke_under_AX1090_closure_2730.py",
            "mission": "try to fill one real source-backed memory row (Z_X, M_X^2, J_X component, boundary_lift, Q_X or K_i); if none exists, run a refusal smoke proving the interface blocks all fake local-test claims",
            "acceptance": "one row becomes source-backed but still nonclaim, or refusal smoke proves no placeholder can score",
            "forbidden": "claim-ready pass from placeholders; GitHub action; formalization-workbench edits",
            "selected": True,
            "valid_for_claim": False,
        }
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        {"copy_id": "COPY2729_0_local_interface", "source_table": str(OUTPUTS["finite"]), "copy_path": str(BRANCH_OUTPUTS["local_interface"]), "purpose": "local bound branch receives memory finite residual interface", "exists": BRANCH_OUTPUTS["local_interface"].exists(), "valid_for_claim": False},
        {"copy_id": "COPY2729_1_r10_smoke", "source_table": str(OUTPUTS["r10"]), "copy_path": str(BRANCH_OUTPUTS["r10_smoke"]), "purpose": "R10 branch receives explicit refusal smoke rows", "exists": BRANCH_OUTPUTS["r10_smoke"].exists(), "valid_for_claim": False},
        {"copy_id": "COPY2729_2_source_weight_contract", "source_table": str(OUTPUTS["contract"]), "copy_path": str(BRANCH_OUTPUTS["source_weight_contract"]), "purpose": "source-weight branch receives exact parent signature contract", "exists": BRANCH_OUTPUTS["source_weight_contract"].exists(), "valid_for_claim": False},
        {"copy_id": "COPY2729_3_next_queue", "source_table": str(OUTPUTS["next"]), "copy_path": str(BRANCH_OUTPUTS["next_queue"]), "purpose": "queues first source-row acquisition or refusal smoke", "exists": BRANCH_OUTPUTS["next_queue"].exists(), "valid_for_claim": False},
    ]


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    arena: list[dict[str, Any]],
    r10: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    contract_ready = len(contract) == 9 and contract[-1]["current_status"] == "CONTRACT_READY_NOT_ACTIVATED"
    audit_false = all(row["signed_now"] is False and row["valid_for_claim"] is False for row in audit)
    finite_refuses = all(row["score_status"] == "NOT_SCOREABLE" and row["valid_for_claim"] is False for row in finite)
    arena_refuses = all(row["current_status"].startswith("BLOCKED") and row["valid_for_claim"] is False for row in arena)
    r10_refuses = all("MISSING" in row["lambda_value"] and row["valid_for_claim"] is False for row in r10)
    gates_refuse = all(row["score_allowed"] is False and row["valid_for_claim"] is False for row in refusal)
    branch_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    formalization_ok = formalization_recent_count() == 0
    csv_parse_ok = True
    parse_bits = []
    for key, path in {**OUTPUTS, **BRANCH_OUTPUTS}.items():
        if key == "validation":
            continue
        try:
            rows = read_csv(path)
            parse_bits.append(f"{path.name}:{len(rows)}:ok")
        except Exception as exc:
            csv_parse_ok = False
            parse_bits.append(f"{path.name}:ERROR:{exc}")

    rows = [
        {"validation_id": "VAL2729_0_sources", "passed": source_ok, "detail": "all source paths exist and needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2729_1_contract_ready", "passed": contract_ready, "detail": "parent memory signature contract written but not activated", "timestamp_utc": ts()},
        {"validation_id": "VAL2729_2_audit_false", "passed": audit_false, "detail": "no parent clause is signed or claim-valid", "timestamp_utc": ts()},
        {"validation_id": "VAL2729_3_finite_refuses", "passed": finite_refuses, "detail": "finite memory residual interface refuses missing inputs", "timestamp_utc": ts()},
        {"validation_id": "VAL2729_4_arena_refuses", "passed": arena_refuses, "detail": "all arena projection rows remain blocked", "timestamp_utc": ts()},
        {"validation_id": "VAL2729_5_r10_refuses", "passed": r10_refuses, "detail": "R10 smoke rows contain MISSING placeholders and valid_for_claim=false", "timestamp_utc": ts()},
        {"validation_id": "VAL2729_6_score_gates_refuse", "passed": gates_refuse, "detail": "no score/pass/local-GR claim is allowed", "timestamp_utc": ts()},
        {"validation_id": "VAL2729_7_branch_outputs", "passed": branch_ok, "detail": "local/source-weight/RAB branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2729_8_csv_parse", "passed": csv_parse_ok, "detail": "; ".join(parse_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2729_9_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_recent_count()}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2729_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2729 writes exact parent memory signature contract and finite residual interface, with all scoring refused",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2729 — Y5 R2/f(R): Parent Memory Signature Contract Plus Finite Local Residual Interface Under AX1090 Closure

Status: `Y5_R2FR_2729_parent_memory_signature_contract_written_finite_residual_interface_refuses_placeholders_nonclaim`

## Private Verdict

This checkpoint turns the memory gap into an engineering contract. If MTS is going to derive local GR through the memory no-hair route, the parent action must sign the clauses below: parent `X`, parent-selected `D`, quadratic operator block, positive signs/gap, zero-or-bounded `J_X`, boundary/zero-mode package, no tower return, and arena projection maps.

The contract is now precise, but it is **not activated**. No clause has a source-backed parent proof in this file. Therefore every finite local residual row remains `NOT_SCOREABLE`, every R10 smoke row is a forced refusal, and no local-GR/Newton/R10/PPN/clock/orbital/WEP claim is opened.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## Parent Memory Signature Contract

{markdown_table(data["contract"], ["clause_id", "parent_action_clause", "would_sign", "needed_source", "current_status", "failure_if_absent", "valid_for_claim"])}

## Signature Clause Activation Audit

{markdown_table(data["audit"], ["audit_id", "clause_id", "signed_now", "why_not_signed", "required_evidence", "claim_allowed", "valid_for_claim"])}

## Finite Memory Residual Input Interface

{markdown_table(data["finite"], ["input_id", "quantity", "formula", "value", "units", "required_sources", "blocks", "score_status", "valid_for_claim"])}

## Arena Projection Interface

{markdown_table(data["arena"], ["arena_id", "arena", "prediction_shape", "requires_memory_inputs", "requires_bound_inputs", "current_status", "valid_for_claim"])}

## R10 Alpha Smoke Rows

{markdown_table(data["r10"], ["model_id", "branch_id", "curve_id", "lambda_value", "lambda_units", "alpha_predicted", "alpha_bound", "alpha_bound_source", "force_law_form", "derivation_status", "formula_reference", "valid_for_claim", "notes"])}

## Refusal And Score Gates

{markdown_table(data["refusal"], ["gate_id", "gate", "status", "reason", "score_allowed", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is the socket. The theory can now either plug in a real parent memory action/signature source, or it cannot. If it can, the memory no-hair theorem becomes live. If it cannot, the exact missing quantities are already shaped as finite residual rows for tests. That is good progress: not a win by knockout, but the ring ropes are now real instead of painted on the floor.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    contract = contract_rows()
    audit = audit_rows()
    finite = finite_rows()
    arena = arena_rows()
    r10 = r10_rows()
    refusal = refusal_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["contract"], contract)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["finite"], finite)
    write_csv(OUTPUTS["arena"], arena)
    write_csv(OUTPUTS["r10"], r10)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["local_interface"], finite)
    write_csv(BRANCH_OUTPUTS["r10_smoke"], r10)
    write_csv(BRANCH_OUTPUTS["source_weight_contract"], contract)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    validation = validation_rows(sources, contract, audit, finite, arena, r10, refusal)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "contract": contract,
        "audit": audit,
        "finite": finite,
        "arena": arena,
        "r10": r10,
        "refusal": refusal,
        "decisions": decisions,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2729 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
