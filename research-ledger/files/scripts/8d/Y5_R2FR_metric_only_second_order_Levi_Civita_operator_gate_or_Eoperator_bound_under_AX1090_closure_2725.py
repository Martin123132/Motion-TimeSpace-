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

DOC = ROOT / "2725-Y5-R2FR-metric-only-second-order-Levi-Civita-operator-gate-or-Eoperator-bound-under-AX1090-closure.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2725_SOURCE_REGISTER.csv",
    "clause_audit": RESIDUALS / "P8_Y5_R2FR_2725_METRIC_SECOND_LC_CLAUSE_AUDIT.csv",
    "relative_theorem": RESIDUALS / "P8_Y5_R2FR_2725_RELATIVE_EH_OPERATOR_THEOREM.csv",
    "countermodels": RESIDUALS / "P8_Y5_R2FR_2725_OPERATOR_COUNTERMODEL_LEDGER.csv",
    "contract": RESIDUALS / "P8_Y5_R2FR_2725_PARENT_OPERATOR_CONTRACT.csv",
    "residual_rows": RESIDUALS / "P8_Y5_R2FR_2725_OPERATOR_RESIDUAL_ROWS_NONCLAIM.csv",
    "ejeff_update": RESIDUALS / "P8_Y5_R2FR_2725_EJEFF_UPDATE_VECTOR_NONCLAIM.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2725_CLAIM_GATES.csv",
    "blocker_stack": RESIDUALS / "P8_Y5_R2FR_2725_CURRENT_BLOCKER_STACK.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2725_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2725_NEXT_TARGET.csv",
    "project_snapshot": RESIDUALS / "P8_Y5_R2FR_2725_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2725_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2725_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_bounds": LOCAL_BOUNDS / "metric_only_second_order_LC_operator_rows_2725_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "metric_only_second_order_LC_EJeff_update_2725_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2725_PARENT_NO_EXTENSION_MINIMALITY_AND_LC_DESCENT_NEXT.csv",
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
        "source_id": "SRC2725_0_2724",
        "label": "2724 handoff",
        "path": ROOT / "2724-Y5-R2FR-EH-left-hand-weak-field-operator-gauge-domain-or-Poisson-residual-row-under-AX1090-closure.md",
        "needles": [
            "LHS2724_5_verdict",
            "FOP2724_0_E_operator_metric_only",
            "FOP2724_1_E_second_order_HD",
            "FOP2724_2_E_connection_LC",
            "NEXT2724_0_selected",
            "VAL2724_OVERALL",
        ],
        "use": "direct handoff selecting metric-only, second-order and Levi-Civita operator gate",
    },
    {
        "source_id": "SRC2725_1_439",
        "label": "439 EH-only premise ladder",
        "path": ROOT / "439-EH-only-exterior-parent-premise-ladder.md",
        "needles": [
            "P3_no_extra_local_propagating_fields",
            "P4_metric_compatibility_connection",
            "P6_second_order_metric_equations",
            "conditional_theorem_shape",
        ],
        "use": "earlier parent-premise ladder for EH-only exterior selection",
    },
    {
        "source_id": "SRC2725_2_440",
        "label": "440 metric-only second-order attempt",
        "path": ROOT / "440-metric-only-second-order-sector-reduction-attempt.md",
        "needles": [
            "metric-only cannot be assumed before varying the extra sectors",
            "central_open",
            "higher_curvature_metric_operators",
            "torsion_nonmetricity_connection",
        ],
        "use": "shows integrating out extra sectors can regenerate non-EH operators",
    },
    {
        "source_id": "SRC2725_3_958",
        "label": "958 EH core operator selection",
        "path": ROOT / "958-Y5-R10-EH-core-operator-selection-or-executable-R11-nonEH-vector.md",
        "needles": [
            "EH958_1_Lovelock_route",
            "EH958_2_extra_field_obstruction",
            "EH958_5_verdict",
        ],
        "use": "confirms EH route is clean but parent premises are not derived",
    },
    {
        "source_id": "SRC2725_4_959",
        "label": "959 no-extra-field clause",
        "path": ROOT / "959-Y5-R10-local-second-order-metric-only-no-extra-field-clause-or-R11-priority-fill.md",
        "needles": [
            "NEF959_3_R2_fR_obstruction",
            "NEF959_4_torsion_nonmetricity_obstruction",
            "NEF959_5_verdict",
            "CGATE959_0_EH_operator",
        ],
        "use": "identifies R2/fR and torsion/nonmetricity as first priority operator families",
    },
    {
        "source_id": "SRC2725_5_960",
        "label": "960 R2/fR and torsion gate",
        "path": ROOT / "960-Y5-R10-R2-fR-scalar-mode-zero-or-bound-and-torsion-Levi-Civita-gate.md",
        "needles": [
            "R2FR960_4_verdict",
            "LC960_4_verdict",
            "torsion/nonmetricity: LC routes known, parent proof/bounds missing",
        ],
        "use": "R2/fR filter and Levi-Civita route are clean but not parent closed",
    },
    {
        "source_id": "SRC2725_6_962_csv",
        "label": "962 R2/fR relative zero proof",
        "path": RESIDUALS / "P8_Y5_R10_962_R2FR_ZERO_PROOF_ATTEMPT.csv",
        "needles": [
            "R2Z962_5_relative_zero_theorem",
            "RELATIVE_THEOREM_PROVEN_PARENT_PREMISE_UNSIGNED",
        ],
        "use": "relative theorem proving R2/fR zero if parent second-order/no-extra-scalar premise is signed",
    },
    {
        "source_id": "SRC2725_7_963",
        "label": "963 parent second-order signature",
        "path": ROOT / "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md",
        "needles": [
            "NES963_5_verdict",
            "NO_EXECUTABLE_OWNER_FOUND",
            "CGATE963_3_local_GR_promotion",
        ],
        "use": "parent second-order signature and coefficient-owner audit did not close",
    },
    {
        "source_id": "SRC2725_8_964",
        "label": "964 no-higher-derivative minimality",
        "path": ROOT / "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md",
        "needles": [
            "MIN964_5_verdict",
            "CM964_0_EH_plus_R2",
            "CM964_2_marker_prefactor",
            "DEC964_0_theorem_result",
        ],
        "use": "best minimality/no-extension derivation shot failed; countermodels remain legal",
    },
    {
        "source_id": "SRC2725_9_R11_gate",
        "label": "R11 EH-only or executable gate",
        "path": RESIDUALS / "R11_EH_ONLY_OR_EXECUTABLE_VECTOR_GATE.csv",
        "needles": [
            "EHV1_EH_only_ladder_closed",
            "EHV2_Lovelock_assumptions_earned",
            "EHV3_connection_compatibility_earned",
            "EHV8_local_GR_or_Newton_promotion",
        ],
        "use": "machine-readable gate refusing EH-only unless premise ladder, Lovelock assumptions and connection compatibility are earned",
    },
    {
        "source_id": "SRC2725_10_R11_vector",
        "label": "R11 executable vector",
        "path": RESIDUALS / "R11_nonEH_operator_vector_executable.csv",
        "needles": [
            "R2_fR_scalar_mode",
            "torsion_nonmetricity",
            "Ricci_Weyl_squared",
            "nonlocal_memory_kernel",
        ],
        "use": "canonical retained non-EH operator families, still mostly missing numeric or zero coefficients",
    },
    {
        "source_id": "SRC2725_11_1104",
        "label": "1104 ordinary-sector signature",
        "path": ROOT / "1104-Y5-R10-parent-ordinary-sector-action-signature-or-explicit-closure-ledger.md",
        "needles": [
            "SIG1104_1_EH_or_R11_operator",
            "THM1104_3_GR_reduction_condition",
            "CG1104_4_local_GR_Newton",
        ],
        "use": "local GR/Newton needs field-operator side plus source side; ordinary signature alone is insufficient",
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


def clause_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "MSC2725_0_metric_only_target",
            "clause": "observed compact exterior has no non-metric or extra local propagating field in the operator",
            "derivation_attempt": "vary full parent action first, solve extra fields, then test whether on-shell S_eff[g_obs] contains only EH/Lambda plus harmless boundary",
            "current_result": "NOT_PARENT_SIGNED",
            "why": "440 says metric-only cannot be assumed before varying extra sectors; 958/959 keep scalar/vector/domain/projector/memory/connection families retained",
            "residuals_emitted": "E_nonmetric_extra_field;E_auxiliary_reentry;E_boundary_topological",
            "claim_allowed": False,
        },
        {
            "audit_id": "MSC2725_1_second_order_target",
            "clause": "surviving metric equation is second order for arbitrary local compact exterior perturbations",
            "derivation_attempt": "use second-order filter: nonlinear f(R), R^2, Ricci^2, Weyl^2 and nonlocal kernels must be zero, topological, redundant, or bounded",
            "current_result": "RELATIVE_FILTER_CLEAN_ABSOLUTE_ZERO_UNSIGNED",
            "why": "962 proves the relative f(R) filter, but 963/964 show the parent no-higher-derivative/minimality signature is not proved",
            "residuals_emitted": "E_second_order_minimality;E_R2FR_scalar;E_RicciWeyl_tensor;E_nonlocal_memory",
            "claim_allowed": False,
        },
        {
            "audit_id": "MSC2725_2_Levi_Civita_target",
            "clause": "observed connection is Levi-Civita of g_obs and matter/light/spin use that same connection",
            "derivation_attempt": "close by metric formalism only, or by Palatini/connection variation with zero hypermomentum and no torsion/nonmetricity",
            "current_result": "CONDITIONAL_ROUTE_KNOWN_PARENT_PROOF_MISSING",
            "why": "960 says LC routes are known, but no parent action equation kills all independent connection residues; R11 gate marks connection compatibility failed",
            "residuals_emitted": "E_connection_metric_affine;E_hypermomentum_connection",
            "claim_allowed": False,
        },
        {
            "audit_id": "MSC2725_3_Lovelock_activation",
            "clause": "Lovelock/EH selection can be activated",
            "derivation_attempt": "combine local 4D diffeo-invariant metric-only second-order LC premises",
            "current_result": "MATHEMATICAL_THEOREM_AVAILABLE_NOT_MTS_DERIVED",
            "why": "439 and 1339 give the conditional theorem shape, but the parent has not earned the premises",
            "residuals_emitted": "E_operator_core",
            "claim_allowed": False,
        },
        {
            "audit_id": "MSC2725_4_verdict",
            "clause": "MTS parent derives EH left-hand operator",
            "derivation_attempt": "synthesize 439/440/958-964/2724 into a direct parent operator proof",
            "current_result": "EH_OPERATOR_NOT_DERIVED_CURRENT_CORPUS",
            "why": "countermodels remain legal: EH+R2, integrated-out scalar, marker-prefactor F(sigma)R, nonlocal memory kernel, and metric-affine connection branch",
            "residuals_emitted": "operator residual ledger remains mandatory",
            "claim_allowed": False,
        },
    ]


def relative_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "THM2725_0_relative_EH_operator",
            "statement": "If the compact exterior parent action descends to a local 4D diffeo-invariant metric-only second-order Levi-Civita action, with all extra sectors either topological/boundary-silent or absent, then the local metric operator is EH plus Lambda up to normalization.",
            "status": "RELATIVE_THEOREM_CLEAN",
            "proof_source": str(ROOT / "439-EH-only-exterior-parent-premise-ladder.md"),
            "missing_for_MTS": "parent-signed descent clauses MSC2725_0 through MSC2725_2",
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM2725_1_metric_only_descent_contract",
            "statement": "Metric-only descent requires varying every extra sector before substitution; any surviving stress, source-normalization operator, or on-shell Delta S_A[g] is retained rather than hidden.",
            "status": "CONTRACT_DERIVED_NOT_SATISFIED",
            "proof_source": str(ROOT / "440-metric-only-second-order-sector-reduction-attempt.md"),
            "missing_for_MTS": "sector-by-sector zero/topological/no-flux/positive no-hair certificate",
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM2725_2_second_order_filter",
            "statement": "For metric f(R), nonzero f_RR creates higher-derivative/scalar dynamics; therefore c_R2=c_fR=0 follows only if exact second-order/no-extra-scalar parent premises are signed.",
            "status": "RELATIVE_R2FR_ZERO_THEOREM_PROVEN_PARENT_PREMISE_UNSIGNED",
            "proof_source": str(RESIDUALS / "P8_Y5_R10_962_R2FR_ZERO_PROOF_ATTEMPT.csv"),
            "missing_for_MTS": "no-higher-derivative minimality/no-extension theorem from the parent",
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM2725_3_LC_connection_filter",
            "statement": "Gamma=LC[g_obs] follows if the parent has no independent connection, or if connection variation is Palatini-EH-like with zero hypermomentum and no projective/torsion/nonmetricity residue.",
            "status": "CONDITIONAL_LC_ROUTE_ONLY",
            "proof_source": str(ROOT / "960-Y5-R10-R2-fR-scalar-mode-zero-or-bound-and-torsion-Levi-Civita-gate.md"),
            "missing_for_MTS": "parent connection variation or no-independent-connection clause",
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM2725_4_failure_rule",
            "statement": "If any clause fails, the local branch is not a derived EH/local-GR branch; it is an EH-plus-explicit-residual branch until residuals are zeroed or bounded.",
            "status": "CLAIM_REJECTION_RULE_DERIVED",
            "proof_source": str(RESIDUALS / "R11_EH_ONLY_OR_EXECUTABLE_VECTOR_GATE.csv"),
            "missing_for_MTS": "operator residual coefficients or zero theorems",
            "claim_allowed": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "CM2725_0_EH_plus_R2",
            "legal_if_not_forbidden": "S=S_EH+epsilon int sqrt(-g) R^2",
            "why_it_blocks": "local, 4D and diffeo-invariant but produces scalar/fourth-order trace mode unless epsilon=0 or decoupled",
            "killed_by": "parent no-higher-derivative/minimality theorem or sourced scalar-mode bound",
            "currently_killed": False,
        },
        {
            "countermodel_id": "CM2725_1_integrated_out_scalar",
            "legal_if_not_forbidden": "S=S_EH+int sqrt(-g)[-M^2 phi^2/2 + beta phi R]",
            "why_it_blocks": "solving phi can generate R^2 even if the primitive action looked second order",
            "killed_by": "no-extra-scalar/no-integrated-out tower theorem with readout/source equivalence",
            "currently_killed": False,
        },
        {
            "countermodel_id": "CM2725_2_marker_prefactor",
            "legal_if_not_forbidden": "S=int sqrt(-g) F(sigma_marker) R + S_sigma",
            "why_it_blocks": "quotient-invariant marker or class scalar can act like scalar-tensor/f(R) leakage",
            "killed_by": "primitive quotient no-natural-marker theorem plus local value/gradient silence",
            "currently_killed": False,
        },
        {
            "countermodel_id": "CM2725_3_nonlocal_memory_kernel",
            "legal_if_not_forbidden": "S=S_EH+int sqrt(-g) R Box^-1 R or compact memory kernel",
            "why_it_blocks": "covariant memory/history terms can change weak-field response and finite-range channels",
            "killed_by": "locality/minimality theorem or executable nonlocal kernel bound",
            "currently_killed": False,
        },
        {
            "countermodel_id": "CM2725_4_metric_affine_connection",
            "legal_if_not_forbidden": "independent Gamma, torsion T, nonmetricity Q, or spin-connection couplings",
            "why_it_blocks": "Levi-Civita and universal matter/light/spin connection do not follow automatically",
            "killed_by": "no-independent-connection theorem or Palatini-EH zero-hypermomentum variation",
            "currently_killed": False,
        },
        {
            "countermodel_id": "CM2725_5_boundary_topological_leak",
            "legal_if_not_forbidden": "boundary, Gauss-Bonnet-like, domain wall or projector terms with local flux/stress",
            "why_it_blocks": "topological-safe cases are harmless only if exact zero variation and boundary flux are controlled",
            "killed_by": "boundary/topological no-flux certificate in observed local collar",
            "currently_killed": False,
        },
    ]


def contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "PC2725_0_full_variation_first",
            "future_parent_action_requirement": "write S_parent[g_obs, Gamma?, Z_A, Psi, theta] and vary before eliminating Z_A",
            "acceptance_test": "every eliminated sector has a source path, Euler equation, stress contribution and boundary term",
            "failure_effect": "metric-only descent cannot be claimed",
            "status": "REQUIRED_NOT_SATISFIED",
            "claim_allowed": False,
        },
        {
            "contract_id": "PC2725_1_no_extension_minimality",
            "future_parent_action_requirement": "prove no natural quotient-invariant marker, scalar, vector, nonlocal memory, or integrated-out tower can couple to curvature in the local branch",
            "acceptance_test": "countermodels CM2725_0 through CM2725_3 are impossible, not merely unfavoured",
            "failure_effect": "R2/fR/scalar/nonlocal operator rows stay retained",
            "status": "REQUIRED_NOT_SATISFIED",
            "claim_allowed": False,
        },
        {
            "contract_id": "PC2725_2_second_order_signature",
            "future_parent_action_requirement": "prove the effective observed metric equation is second order through tested local scales",
            "acceptance_test": "c_R2,c_fR,c_Ricci,c_Weyl,c_nonlocal are zero/topological/redundant or source-bounded",
            "failure_effect": "EH operator cannot be selected by Lovelock",
            "status": "REQUIRED_NOT_SATISFIED",
            "claim_allowed": False,
        },
        {
            "contract_id": "PC2725_3_LC_descent",
            "future_parent_action_requirement": "prove observed connection is Levi-Civita or derive it from connection variation",
            "acceptance_test": "torsion T, nonmetricity Q, hypermomentum and independent-connection couplings vanish or are bounded",
            "failure_effect": "clock/light/spin/WEP/PPN connection rows remain retained",
            "status": "REQUIRED_NOT_SATISFIED",
            "claim_allowed": False,
        },
        {
            "contract_id": "PC2725_4_boundary_harmless",
            "future_parent_action_requirement": "prove boundary/topological/projector/domain pieces have zero local metric variation and no observable flux",
            "acceptance_test": "boundary stress and local collar flux vanish in the same observed frame",
            "failure_effect": "boundary/domain operator rows remain retained",
            "status": "REQUIRED_NOT_SATISFIED",
            "claim_allowed": False,
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "EOP2725_0_E_nonmetric_extra_field",
            "quantity": "E_nonmetric_extra_field",
            "definition": "norm(sum of scalar/vector/domain/projector/memory extra-field metric operator contributions)/norm(EH operator)",
            "feeds": "E_operator_metric_only;E_operator_core;R11",
            "source_path": str(ROOT / "958-Y5-R10-EH-core-operator-selection-or-executable-R11-nonEH-vector.md"),
            "units_need": "dimensionless operator norm after observed-frame normalization",
            "missing": "sector zero/topological/no-flux/no-hair certificates or executable coefficient rows",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "EOP2725_1_E_auxiliary_reentry",
            "quantity": "E_auxiliary_reentry",
            "definition": "norm(operator terms regenerated by solving auxiliary/hidden-sector equations and substituting back into S_eff[g])",
            "feeds": "E_operator_metric_only;E_second_order_HD",
            "source_path": str(ROOT / "440-metric-only-second-order-sector-reduction-attempt.md"),
            "units_need": "dimensionless effective-action operator residual",
            "missing": "proof eliminated sectors do not create f(R), R^2, Yukawa or nonlocal kernels",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "EOP2725_2_E_second_order_minimality",
            "quantity": "E_second_order_minimality",
            "definition": "binary-or-norm residual for missing parent no-higher-derivative/minimality signature",
            "feeds": "E_second_order_HD;E_operator_core",
            "source_path": str(ROOT / "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md"),
            "units_need": "zero theorem or dimensionless retained-operator envelope",
            "missing": "no-extension/minimality theorem excluding curvature towers and marker couplings",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "EOP2725_3_E_R2FR_scalar",
            "quantity": "E_R2FR_scalar",
            "definition": "retained scalar/fourth-order contribution from R^2, f(R), or scalaron-equivalent branch",
            "feeds": "E_second_order_HD;R10;PPN",
            "source_path": str(RESIDUALS / "P8_Y5_R10_962_R2FR_ZERO_PROOF_ATTEMPT.csv"),
            "units_need": "coefficient units, scalar mass/range, alpha(lambda), gamma/beta projection",
            "missing": "parent-signed c_R2=c_fR=0 or numeric scalar-mode bound inputs",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "EOP2725_4_E_RicciWeyl_tensor",
            "quantity": "E_RicciWeyl_tensor",
            "definition": "retained spin-2/tensor higher-curvature contribution from Ricci^2 or Weyl^2 families",
            "feeds": "E_second_order_HD;PPN;wave/local operator ledger",
            "source_path": str(RESIDUALS / "R11_nonEH_operator_vector_executable.csv"),
            "units_need": "coefficient units, normalization scale, weak-field slip/wave-sector map",
            "missing": "zero theorem or coefficient/bound source for Ricci/Weyl-squared rows",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "EOP2725_5_E_nonlocal_memory",
            "quantity": "E_nonlocal_memory",
            "definition": "retained nonlocal/history kernel contribution such as R Box^-1 R or compact memory response",
            "feeds": "E_second_order_HD;R9;R10;R11",
            "source_path": str(ROOT / "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md"),
            "units_need": "kernel norm, locality scale, weak-field projection",
            "missing": "locality theorem or executable memory-kernel coefficient/bound",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "EOP2725_6_E_connection_metric_affine",
            "quantity": "E_connection_metric_affine",
            "definition": "torsion/nonmetricity/independent-connection correction to observed weak-field operator",
            "feeds": "E_connection_LC;WEP;clocks;light;spin;PPN",
            "source_path": str(ROOT / "960-Y5-R10-R2-fR-scalar-mode-zero-or-bound-and-torsion-Levi-Civita-gate.md"),
            "units_need": "connection scale, coefficient units, observed-frame normalization",
            "missing": "no-independent-connection or Palatini/zero-hypermomentum proof",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "EOP2725_7_E_hypermomentum_connection",
            "quantity": "E_hypermomentum_connection",
            "definition": "matter/source spin, dilation, shear or hypermomentum source leakage into independent connection",
            "feeds": "E_connection_LC;source normalization;WEP/clocks/spin",
            "source_path": str(RESIDUALS / "R11_EH_ONLY_OR_EXECUTABLE_VECTOR_GATE.csv"),
            "units_need": "dimensionless matter-connection coupling residual",
            "missing": "universal matter connection descent and zero hypermomentum/source coupling certificate",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "EOP2725_8_E_boundary_topological",
            "quantity": "E_boundary_topological",
            "definition": "local metric variation or flux from boundary, Gauss-Bonnet-like, projector or domain terms that are not exactly harmless",
            "feeds": "E_operator_metric_only;E_domain_boundary;E_extra_sector_LHS",
            "source_path": str(ROOT / "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md"),
            "units_need": "boundary/collar flux norm and observed-frame stress normalization",
            "missing": "exact topological/boundary no-flux certificate in local collar",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def ejeff_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "EJ2725_0_operator_core",
            "formula": "E_operator_core := E_nonmetric_extra_field + E_auxiliary_reentry + E_second_order_minimality + E_connection_metric_affine + E_boundary_topological",
            "status": "FORMAL_VECTOR_NONCLAIM",
            "claim_allowed": False,
        },
        {
            "update_id": "EJ2725_1_second_order_HD_refinement",
            "formula": "E_second_order_HD := E_second_order_minimality + E_R2FR_scalar + E_RicciWeyl_tensor + E_nonlocal_memory + E_auxiliary_reentry",
            "status": "FORMAL_VECTOR_NONCLAIM",
            "claim_allowed": False,
        },
        {
            "update_id": "EJ2725_2_connection_LC_refinement",
            "formula": "E_connection_LC := E_connection_metric_affine + E_hypermomentum_connection",
            "status": "FORMAL_VECTOR_NONCLAIM",
            "claim_allowed": False,
        },
        {
            "update_id": "EJ2725_3_2724_carry_forward",
            "formula": "E_Poisson_residual keeps 2724 decomposition, with E_operator_metric_only/E_second_order_HD/E_connection_LC now expanded by 2725 rows",
            "status": "DEPENDENCY_LEDGER_NONCLAIM",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE2725_0_metric_only",
            "claim": "local observed exterior operator is metric-only",
            "status": "BLOCKED",
            "required_before_claim": "full variation-first parent descent and zero/topological/no-flux certificates for all extra sectors",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2725_1_second_order",
            "claim": "local observed metric equation is second order",
            "status": "BLOCKED",
            "required_before_claim": "no-extension/minimality theorem or sourced bounds for R2/fR, Ricci/Weyl and nonlocal rows",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2725_2_Levi_Civita",
            "claim": "observed connection is Levi-Civita",
            "status": "BLOCKED",
            "required_before_claim": "no-independent-connection or Palatini/zero-hypermomentum proof plus matter/light/spin connection lock",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2725_3_EH_operator",
            "claim": "EH left-hand operator is parent-derived",
            "status": "BLOCKED",
            "required_before_claim": "metric-only, second-order, LC, boundary and source/operator clauses all pass",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2725_4_local_GR_Newton",
            "claim": "local GR/Newton follows",
            "status": "BLOCKED",
            "required_before_claim": "EH/R11 operator gate plus kappa/source/GM/readout/PPN gates",
            "claim_allowed": False,
        },
    ]


def blocker_stack_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BLK2725_0_no_extension",
            "missing_item": "parent no-extension/minimality theorem",
            "effect": "legal countermodels can append scalar, curvature-square, marker or nonlocal operators",
            "best_next_attack": "try to prove primitive parent object admits no natural local marker or curvature-tower extension",
            "claim_blocked": True,
        },
        {
            "blocker_id": "BLK2725_1_variation_first",
            "missing_item": "full parent action varied before elimination",
            "effect": "metric-only could be an artefact of substituting sectors too early",
            "best_next_attack": "write variation-first parent action contract and mark closure-only clauses",
            "claim_blocked": True,
        },
        {
            "blocker_id": "BLK2725_2_R2FR_scalar",
            "missing_item": "absolute c_R2=c_fR zero or numeric scalar-mode bound",
            "effect": "second-order/EH route cannot be promoted",
            "best_next_attack": "either parent-sign 962 activator or keep R2/fR runner nonclaim",
            "claim_blocked": True,
        },
        {
            "blocker_id": "BLK2725_3_connection",
            "missing_item": "LC connection descent",
            "effect": "WEP/clocks/light/spin/source and PPN can see torsion/nonmetricity",
            "best_next_attack": "derive no-independent-connection or Palatini zero-hypermomentum branch",
            "claim_blocked": True,
        },
        {
            "blocker_id": "BLK2725_4_boundary",
            "missing_item": "boundary/topological local flux silence",
            "effect": "operator can carry local collar/domain stress even if bulk looks EH",
            "best_next_attack": "source boundary no-flux theorem or finite flux row",
            "claim_blocked": True,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2725_0_no_EH_claim",
            "decision": "Do not claim metric-only, second-order, Levi-Civita, EH, local GR or Newton.",
            "rationale": "The parent has not killed legal non-EH countermodels.",
            "allowed": True,
            "claim_credit": False,
        },
        {
            "decision_id": "DEC2725_1_not_circling",
            "decision": "Consolidate prior EH/R11 work into one parent operator contract instead of repeating separate blockers.",
            "rationale": "The next proof must attack no-extension/minimality and LC descent directly.",
            "allowed": True,
            "claim_credit": False,
        },
        {
            "decision_id": "DEC2725_2_next",
            "decision": "Select parent no-extension/minimality and LC descent as the next target.",
            "rationale": "This is the upstream route that could genuinely earn EH; otherwise the branch becomes explicit closure/residual only.",
            "allowed": True,
            "claim_credit": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2725_0_selected",
            "status": "selected_primary",
            "target_doc": "2726-Y5-R2FR-parent-no-extension-minimality-and-LC-descent-or-Eoperator-bound-under-AX1090-closure.md",
            "target_script": "scripts/Y5_R2FR_parent_no_extension_minimality_and_LC_descent_or_Eoperator_bound_under_AX1090_closure_2726.py",
            "mission": "try to prove the parent admits no natural curvature-coupled marker/scalar/nonlocal extension and derive LC connection descent; if not, demote EH operator route to explicit residual/closure-only",
            "acceptance": "either countermodels CM2725_0-CM2725_4 are killed by parent theorem, or each receives retained nonclaim coefficient/bound rows",
            "forbidden": "infer EH from observed Newton success; use Lovelock before premises; hide R11 rows; edit formalization-workbench; GitHub action",
            "selected": True,
            "claim_allowed": False,
        }
    ]


def project_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "snapshot_id": "SNAP2725_0_operator_route",
            "sector": "EH/local operator",
            "state": "relative theorem clean; parent premise not earned",
            "confidence": "high on conditional theorem, low on current proof closure",
            "next_need": "no-extension/minimality and LC descent",
        },
        {
            "snapshot_id": "SNAP2725_1_project_status",
            "sector": "GR/Newton reduction",
            "state": "not dead, but not claimable; exact missing parent clauses are now named",
            "confidence": "medium route viability, high nonclaim discipline",
            "next_need": "kill countermodels or retain them quantitatively",
        },
        {
            "snapshot_id": "SNAP2725_2_empirical_path",
            "sector": "R10/PPN/local tests",
            "state": "waiting on operator coefficients or zero theorems",
            "confidence": "high that scoring now would be premature",
            "next_need": "operator residual vector with real coefficients/bounds",
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "COPY2725_0_local_bounds",
            "source_table": str(OUTPUTS["residual_rows"]),
            "copy_path": str(BRANCH_OUTPUTS["local_bounds"]),
            "purpose": "local/R10/PPN branches can ingest refined operator residual rows without claim credit",
            "exists": BRANCH_OUTPUTS["local_bounds"].exists(),
            "valid_for_claim": False,
        },
        {
            "copy_id": "COPY2725_1_source_weight",
            "source_table": str(OUTPUTS["ejeff_update"]),
            "copy_path": str(BRANCH_OUTPUTS["source_weight"]),
            "purpose": "source-weight branch receives refined E_operator/E_second_order/E_connection decomposition",
            "exists": BRANCH_OUTPUTS["source_weight"].exists(),
            "valid_for_claim": False,
        },
        {
            "copy_id": "COPY2725_2_next_queue",
            "source_table": str(OUTPUTS["next_target"]),
            "copy_path": str(BRANCH_OUTPUTS["next_queue"]),
            "purpose": "queues decisive 2726 no-extension/minimality and LC descent target",
            "exists": BRANCH_OUTPUTS["next_queue"].exists(),
            "valid_for_claim": False,
        },
    ]


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        if not rows:
            return False, 0, "empty"
        return True, len(rows), "ok"
    except Exception as exc:
        return False, 0, repr(exc)


def recent_formalization_changes() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime >= start:
            count += 1
    return count


def validation_rows(
    source_rows: list[dict[str, Any]],
    clause_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    ejeff: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    required_quantities = {
        "E_nonmetric_extra_field",
        "E_auxiliary_reentry",
        "E_second_order_minimality",
        "E_R2FR_scalar",
        "E_RicciWeyl_tensor",
        "E_nonlocal_memory",
        "E_connection_metric_affine",
        "E_hypermomentum_connection",
        "E_boundary_topological",
    }
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    parse_results = [(*parse_csv(path), path) for path in csv_paths]
    parse_detail = "; ".join(
        f"{path.name}:{row_count}:{detail}" if passed else f"{path.name}:{detail}"
        for passed, row_count, detail, path in parse_results
    )
    branch_paths_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    formalization_recent_changed_count = recent_formalization_changes()
    source_ok = all(row["exists"] is True and row["required_needles_found"] is True for row in source_rows)
    clause_nonclaim = all(row["claim_allowed"] is False for row in clause_rows)
    theorem_nonclaim = all(row["claim_allowed"] is False for row in theorem_rows)
    countermodels_live = all(row["currently_killed"] is False for row in countermodels)
    contract_nonclaim = all(row["claim_allowed"] is False for row in contract)
    residual_nonclaim = (
        {row["quantity"] for row in residuals} == required_quantities
        and all(row["valid_for_claim"] is False for row in residuals)
    )
    ejeff_nonclaim = all(row["claim_allowed"] is False for row in ejeff)
    gates_false = all(row["claim_allowed"] is False for row in gates)
    no_github_outputs = all("github" not in str(path).lower() for path in csv_paths + [DOC])
    rows = [
        {
            "validation_id": "VAL2725_0_sources",
            "passed": source_ok,
            "detail": "all source paths exist and required needles found",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2725_1_doc_written",
            "passed": DOC.exists(),
            "detail": str(DOC),
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2725_2_csv_parse",
            "passed": all(result[0] for result in parse_results),
            "detail": parse_detail,
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2725_3_clause_nonclaim",
            "passed": clause_nonclaim,
            "detail": "metric-only, second-order and LC audit rows remain nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2725_4_relative_theorems_nonclaim",
            "passed": theorem_nonclaim,
            "detail": "relative EH/R2FR/LC theorems do not promote MTS without parent clauses",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2725_5_countermodels_live",
            "passed": countermodels_live,
            "detail": "all listed countermodels remain live unless future parent theorem kills them",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2725_6_contract_nonclaim",
            "passed": contract_nonclaim,
            "detail": "future parent-action contract is required but not satisfied",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2725_7_residual_rows_complete_nonclaim",
            "passed": residual_nonclaim,
            "detail": "operator residual rows include extra-field, auxiliary, minimality, R2/fR, Ricci/Weyl, nonlocal, connection, hypermomentum and boundary components",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2725_8_ejeff_update_nonclaim",
            "passed": ejeff_nonclaim,
            "detail": "E_operator/E_second_order/E_connection decompositions remain formal/nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2725_9_claim_gates_all_false",
            "passed": gates_false,
            "detail": "no metric-only, second-order, LC, EH, Newton, PPN or local-GR gate opened",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2725_10_branch_copies",
            "passed": branch_paths_ok,
            "detail": "branch copies exist and remain nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2725_11_no_formalization_recent_changes",
            "passed": formalization_recent_changed_count == 0,
            "detail": f"formalization_recent_changed_count={formalization_recent_changed_count}",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2725_12_no_github_outputs",
            "passed": no_github_outputs,
            "detail": "no GitHub/public-output path was written",
            "timestamp_utc": ts(),
        },
    ]
    overall = all(row["passed"] is True for row in rows)
    rows.append(
        {
            "validation_id": "VAL2725_OVERALL",
            "passed": overall,
            "detail": "2725 consolidates metric-only/second-order/LC operator gate, refuses EH promotion, writes parent operator contract, and selects no-extension/minimality plus LC descent next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2725 - Y5/R2FR Metric-Only Second-Order Levi-Civita Operator Gate Or Eoperator Bound Under AX1090 Closure

## Private Verdict

2725 takes the direct shot at the EH operator premise. The result is not a promotion, but it is a real tightening.

The relative theorem is clean: if the compact local exterior branch is genuinely metric-only, local, 4D, diffeomorphism-invariant, second-order, and Levi-Civita, then the Lovelock/EH operator follows up to normalization and Lambda/background terms.

The MTS parent has not yet earned those premises. The live countermodels are too concrete to ignore: `EH+R^2`, integrated-out scalar reentry, marker-prefactor `F(sigma)R`, nonlocal memory kernels, and metric-affine torsion/nonmetricity. Therefore:

`EH operator = conditional route, not derived MTS claim`.

The useful progress is that 2725 stops the circling: the next proof must attack a parent no-extension/minimality theorem and Levi-Civita descent directly, or the EH route is closure/residual-only.

## Claim Ceiling

- No metric-only, second-order, Levi-Civita, EH, Newton, PPN, local-GR, R10, clock, orbital, WEP, or public claim is opened.
- Lovelock/EH is kept as a relative theorem only.
- All new operator rows are `valid_for_claim=false`.
- No `formalization-workbench` edits, GitHub action, or public-output path is allowed from this checkpoint.

## Source Register

{markdown_table(rows["source_register"], ["source_id", "label", "path", "exists", "required_needles_found", "missing_needles", "use", "claim_credit"])}

## Metric-Only / Second-Order / Levi-Civita Clause Audit

{markdown_table(rows["clause_audit"], ["audit_id", "clause", "derivation_attempt", "current_result", "why", "residuals_emitted", "claim_allowed"])}

## Relative EH Operator Theorem

{markdown_table(rows["relative_theorem"], ["theorem_id", "statement", "status", "proof_source", "missing_for_MTS", "claim_allowed"])}

## Operator Countermodel Ledger

{markdown_table(rows["countermodels"], ["countermodel_id", "legal_if_not_forbidden", "why_it_blocks", "killed_by", "currently_killed"])}

## Future Parent Operator Contract

{markdown_table(rows["contract"], ["contract_id", "future_parent_action_requirement", "acceptance_test", "failure_effect", "status", "claim_allowed"])}

## Operator Residual Rows

{markdown_table(rows["residual_rows"], ["row_id", "quantity", "definition", "feeds", "source_path", "units_need", "missing", "status", "valid_for_claim"])}

## E_Jeff Update

{markdown_table(rows["ejeff_update"], ["update_id", "formula", "status", "claim_allowed"])}

## Claim Gates

{markdown_table(rows["claim_gates"], ["gate_id", "claim", "status", "required_before_claim", "claim_allowed"])}

## Current Blocker Stack

{markdown_table(rows["blocker_stack"], ["blocker_id", "missing_item", "effect", "best_next_attack", "claim_blocked"])}

## Decision Ledger

{markdown_table(rows["decision_ledger"], ["decision_id", "decision", "rationale", "allowed", "claim_credit"])}

## Next Target

{markdown_table(rows["next_target"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "claim_allowed"])}

## Project Status Snapshot

{markdown_table(rows["project_snapshot"], ["snapshot_id", "sector", "state", "confidence", "next_need"])}

## Branch Copies

{markdown_table(rows["branch_copies"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is the sharpest honest status: GR is not being smuggled in, but the route is still alive. The EH theorem is waiting behind a locked door. The key is not more weak-field algebra; the key is a parent principle strong enough to forbid every legal non-EH extension, plus a connection proof that really gives Levi-Civita. If we can earn that, the GR reduction gets serious fast. If we cannot, MTS must own the residual operator vector and fight experimentally.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    clause = clause_audit_rows()
    theorem = relative_theorem_rows()
    countermodels = countermodel_rows()
    contract = contract_rows()
    residuals = residual_rows()
    ejeff = ejeff_update_rows()
    gates = claim_gate_rows()
    blockers = blocker_stack_rows()
    decisions = decision_ledger_rows()
    next_rows = next_target_rows()
    snapshot = project_snapshot_rows()

    data: dict[str, list[dict[str, Any]]] = {
        "source_register": source_rows,
        "clause_audit": clause,
        "relative_theorem": theorem,
        "countermodels": countermodels,
        "contract": contract,
        "residual_rows": residuals,
        "ejeff_update": ejeff,
        "claim_gates": gates,
        "blocker_stack": blockers,
        "decision_ledger": decisions,
        "next_target": next_rows,
        "project_snapshot": snapshot,
    }

    for key, table_rows in data.items():
        write_csv(OUTPUTS[key], table_rows)

    write_csv(BRANCH_OUTPUTS["local_bounds"], residuals)
    write_csv(BRANCH_OUTPUTS["source_weight"], ejeff)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_rows)

    copies = branch_copy_rows()
    data["branch_copies"] = copies
    write_csv(OUTPUTS["branch_copies"], copies)

    data["validation"] = [
        {
            "validation_id": "VAL2725_PRE_DOC",
            "passed": False,
            "detail": "pre-document placeholder",
            "timestamp_utc": ts(),
        }
    ]
    write_doc(data)

    validation = validation_rows(source_rows, clause, theorem, countermodels, contract, residuals, ejeff, gates)
    data["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    write_doc(data)

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2725 validation failed: {failed}")

    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
