from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1382-Y5-R10-RAB-Zm-coefficient-law-admissibility-or-symbolic-prior-pack.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1382_SOURCE_REGISTER.csv"
ADMISSIBILITY_PATH = SRC_DIR / "P8_Y5_R10_1382_ZM_ADMISSIBILITY_SCAFFOLD.csv"
PRIOR_PACK_PATH = SRC_DIR / "P8_Y5_R10_1382_SYMBOLIC_PRIOR_PACK.csv"
RUNNER_FEED_PATH = SRC_DIR / "P8_Y5_R10_1382_RUNNER_FEED_UPDATE.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1382_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1382_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1382_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1382_VALIDATION.csv"

STATUS = (
    "Z_m_admissibility_scaffold_and_symbolic_prior_pack_written_"
    "no_numeric_scoring_no_local_GR_PPN_R10_claim"
)
CLAIM_CEILING = (
    "admissibility_contract_only_no_source_backed_Z_m_law_no_transition_length_"
    "no_Q_alg_no_PPN_no_R10_no_local_GR_pass"
)

SOURCE_ROWS = [
    {
        "source_id": "SRC1382_0_1381_doc",
        "source_path": "1381-Y5-R10-RAB-Zm-sign-value-unit-source-or-kappa-closure-demotion.md",
        "required_anchor": "NEXT1381_0_1382",
        "purpose": "handoff from Z_m sign/value/unit failure to admissibility/prior-pack route",
    },
    {
        "source_id": "SRC1382_1_1381_next",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1381_NEXT_TARGET.csv",
        "required_anchor": "NEXT1381_0_1382",
        "purpose": "machine-readable 1382 target",
    },
    {
        "source_id": "SRC1382_2_1381_audit",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1381_ZM_SIGN_VALUE_UNIT_AUDIT.csv",
        "required_anchor": "ZMS1381_7_verdict",
        "purpose": "records no source-backed sign/value/unit row",
    },
    {
        "source_id": "SRC1382_3_1381_demotion",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1381_KAPPA_CLOSURE_SYMBOLIC_DEMOTION.csv",
        "required_anchor": "KCD1381_4_verdict",
        "purpose": "kappa_m=Z_m demoted to closure-symbolic numeric refusal",
    },
    {
        "source_id": "SRC1382_4_1380_kappa_origin",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1380_KAPPA_ZM_ORIGIN_COEFFICIENT_ROW.csv",
        "required_anchor": "KOR1380_4_parent_status",
        "purpose": "source-backed symbolic slot kappa_m=Z_m but value missing",
    },
    {
        "source_id": "SRC1382_5_826_coefficients",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_826_COEFFICIENT_LEDGER.csv",
        "required_anchor": "C826_0_Zm",
        "purpose": "original Z_m coefficient ledger and same local/cosmology value rule",
    },
    {
        "source_id": "SRC1382_6_826_action_ansatz",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
        "required_anchor": "AA826_1_memory_sector",
        "purpose": "candidate memory-sector action with Z_m(X_B) kinetic coefficient",
    },
    {
        "source_id": "SRC1382_7_970_positive_operator",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
        "required_anchor": "QMA970_2_positivity",
        "purpose": "conditional positive-operator energy identity inputs",
    },
    {
        "source_id": "SRC1382_8_1302_stress_contract",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv",
        "required_anchor": "MSR1302_1_spatial_trace_bound_template",
        "purpose": "stress-bound template requiring Z_m and gradient bounds",
    },
    {
        "source_id": "SRC1382_9_1303_stress_inputs",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1303_K_MEM_STRESS_SIGMA_BOUND_INPUT_LEDGER_NONCLAIM.csv",
        "required_anchor": "KMS1303_0_Zm_abs_bound",
        "purpose": "first missing absolute bound row for |Z_m|",
    },
    {
        "source_id": "SRC1382_10_1304_positive_gap",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1304_ZM_POSITIVE_GAP_MAP_NONCLAIM.csv",
        "required_anchor": "ZPG1304_0_Zm_positive",
        "purpose": "positive ellipticity/gap map for Z_m and memory operator",
    },
    {
        "source_id": "SRC1382_11_1304_operator_owner",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1304_MEMORY_OPERATOR_OWNER_ATTEMPT.csv",
        "required_anchor": "OO1304_1_static_local_operator_map",
        "purpose": "local operator map A_m^{ij}=Z_m h^{ij}",
    },
    {
        "source_id": "SRC1382_12_1304_first_bound",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1304_FIRST_STRESS_BOUND_INPUT_ROWS_NONCLAIM.csv",
        "required_anchor": "KMS1304_0_Zm_bar_first_row",
        "purpose": "first row for Z_m_bar value/source acquisition",
    },
    {
        "source_id": "SRC1382_13_1379_doc",
        "source_path": "1379-Y5-R10-RAB-gradient-completion-parent-signature-or-transition-closure-runner.md",
        "required_anchor": "ell_tr=sqrt(kappa_m L0^2/F2)",
        "purpose": "transition-length formula retained as closure-only branch",
    },
    {
        "source_id": "SRC1382_14_1380_doc",
        "source_path": "1380-Y5-R10-RAB-kappa-origin-or-shell-bound-first-parent-signing-clause.md",
        "required_anchor": "kappa_m` can be identified",
        "purpose": "identifies kappa_m with Z_m as symbolic coefficient slot",
    },
    {
        "source_id": "SRC1382_15_this_script",
        "source_path": "scripts/Y5_R10_RAB_Zm_coefficient_law_admissibility_or_symbolic_prior_pack.py",
        "required_anchor": "STATUS",
        "purpose": "1382 generator",
    },
]


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "/")


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = columns or list(rows[0].keys())
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return ""
    fieldnames = columns or list(rows[0].keys())
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join("---" for _ in fieldnames) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(clean(row.get(column, "")) for column in fieldnames) + " |")
    return "\n".join(lines)


def anchor_found(path: Path, anchor: str) -> bool:
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in SOURCE_ROWS:
        source_path = ROOT / row["source_path"]
        exists = source_path.exists()
        found = anchor_found(source_path, row["required_anchor"])
        rows.append(
            {
                **row,
                "exists": str(exists),
                "anchor_found": str(found),
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def admissibility_rows() -> list[dict[str, str]]:
    return [
        {
            "admissibility_id": "ZAS1382_0_domain_owner",
            "clause": "local branch domain and X_B range must be parent-owned",
            "derived_condition": "D_loc and X_B(D_loc) must be specified before any infimum, supremum, or compactness argument is meaningful",
            "source_basis": "ZMS1381_3_value_range;KMS1304_0_Zm_bar_first_row",
            "current_status": "SCHEMA_ONLY_DOMAIN_AND_XB_RANGE_MISSING",
            "required_input": "source-backed D_loc, X_B_min, X_B_max, frame, and branch definition",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "admissibility_id": "ZAS1382_1_positive_ellipticity",
            "clause": "Z_m must be strictly positive on the local branch",
            "derived_condition": "0 < Z_m_min <= Z_m(X_B) so the scalar-memory kinetic operator is no-ghost and A_m^{ij}=Z_m h^{ij} is positive elliptic",
            "source_basis": "C826_0_Zm;ZPG1304_0_Zm_positive;OO1304_1_static_local_operator_map",
            "current_status": "ADMISSIBILITY_CONSTRAINT_DERIVED_NOT_PARENT_SOURCED",
            "required_input": "parent theorem or coefficient law proving Z_m_min>0 on D_loc",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "admissibility_id": "ZAS1382_2_upper_bound",
            "clause": "Z_m must have a finite upper envelope",
            "derived_condition": "Z_m(X_B) <= Z_m_bar < infinity on the same D_loc; if Z_m is continuous and X_B(D_loc) is compact this follows, otherwise it is a prior not a theorem",
            "source_basis": "ZPG1304_1_Zm_abs_bound;KMS1303_0_Zm_abs_bound;KMS1304_0_Zm_bar_first_row",
            "current_status": "SYMBOLIC_BOUND_VARIABLE_READY_VALUE_MISSING",
            "required_input": "Z_m_bar numeric/theorem bound plus units and source path",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "admissibility_id": "ZAS1382_3_same_value_rule",
            "clause": "the coefficient law must be universal across arenas",
            "derived_condition": "Z_m=Z_m(X_B) is one parent law used in local, cosmology, R10, PPN, clocks, and orbital arenas; no per-test retuning or arena-specific sign flips",
            "source_basis": "C826_0_Zm acceptance gate;ZMS1381_3_value_range",
            "current_status": "ANTI_TUNING_RULE_READY_NOT_NUMERIC",
            "required_input": "single coefficient-law source and explicit map from each arena to X_B",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "admissibility_id": "ZAS1382_4_units_normalization",
            "clause": "Z_m units must be locked by the parent action normalization",
            "derived_condition": "[Z_m]=[L_m]/[(nabla m)^2] and transition scoring additionally requires Z_m/F2 dimensionless in ell_tr=sqrt(Z_m L0^2/F2)",
            "source_basis": "AA826_1_memory_sector;ZMS1381_4_units;KCD1381_4_verdict",
            "current_status": "SYMBOLIC_UNITS_RULE_READY_NORMALIZATION_MISSING",
            "required_input": "field dimension of m, measure convention, L0 normalization, F2 normalization, and frame lock",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "admissibility_id": "ZAS1382_5_smoothness_compactness_route",
            "clause": "finite bounds can be theorem-level only with continuity plus compact range",
            "derived_condition": "if Z_m in C^0(I_X), I_X=X_B(D_loc) compact, and Z_m(X_B)>0 on I_X, then extrema exist and give Z_m_min and Z_m_bar",
            "source_basis": "ZPG1304_1_Zm_abs_bound;KMS1304_0_Zm_bar_first_row",
            "current_status": "PURE_MATH_ROUTE_READY_PARENT_DOMAIN_MISSING",
            "required_input": "continuity class for Z_m and compact parent range I_X",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "admissibility_id": "ZAS1382_6_energy_gap_route",
            "clause": "positive Z_m alone does not bound the local profile",
            "derived_condition": "operator control needs Z_m>=Z_m_min>0, M_m^2>=0 or gap/lifting of zero modes, controlled source J_m, and nonpositive/controlled boundary flux",
            "source_basis": "QMA970_2_positivity;ZPG1304_2_mass_gap;ZPG1304_3_gradient_energy_route",
            "current_status": "CONDITIONAL_ENERGY_ROUTE_READY_INPUTS_MISSING",
            "required_input": "M_m^2/gap, zero-mode treatment, source norm, and boundary flux theorem or bound",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "admissibility_id": "ZAS1382_7_stress_residual_policy",
            "clause": "Z_m cannot create a transition profile and then disappear from stress accounting",
            "derived_condition": "any use of Z_m in ell_tr or local profile keeps the canonical scalar stress and T_ZX/source/bath/boundary residual rows alive until bounded",
            "source_basis": "MSR1302_0_canonical_scalar_stress_form;MSR1302_1_spatial_trace_bound_template",
            "current_status": "RESIDUAL_POLICY_LOCKED_NONCLAIM",
            "required_input": "Z_m_bar, gradient bound, potential subtraction owner, X_B metric response, source/bath and boundary bounds",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "admissibility_id": "ZAS1382_8_verdict",
            "clause": "1382 result",
            "derived_condition": "the admissibility contract is now explicit, but no source-backed coefficient law exists yet; numeric scoring remains refused",
            "source_basis": "aggregate_ZAS1382_0_to_ZAS1382_7",
            "current_status": "ADMISSIBILITY_SCAFFOLD_READY_SYMBOLIC_PRIOR_REQUIRED",
            "required_input": "parent-signed Z_m(X_B) law or external source rows for all symbolic priors",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def prior_pack_rows() -> list[dict[str, str]]:
    return [
        {
            "prior_id": "ZPP1382_0_Zm_min",
            "parameter": "Z_m_min",
            "symbolic_prior": "strictly positive lower bound with 0<Z_m_min<=Z_m(X_B)",
            "required_source": "parent positivity/no-ghost theorem or coefficient-law minimum on I_X",
            "units_rule": "same units as Z_m",
            "current_status": "MISSING_PARENT_VALUE_OR_THEOREM",
            "refusal_gate": "no elliptic/no-ghost scoring and no ell_tr scoring",
            "valid_for_claim": "False",
        },
        {
            "prior_id": "ZPP1382_1_Zm_bar",
            "parameter": "Z_m_bar",
            "symbolic_prior": "finite upper envelope sup_Dloc |Z_m(X_B)|",
            "required_source": "compactness+continuity theorem or source-backed bound row",
            "units_rule": "same units as Z_m",
            "current_status": "MISSING_PARENT_VALUE_OR_BOUND",
            "refusal_gate": "no stress-bound or local residual scoring",
            "valid_for_claim": "False",
        },
        {
            "prior_id": "ZPP1382_2_Zm_units",
            "parameter": "units(Z_m)",
            "symbolic_prior": "[Z_m]=[L_m]/[(nabla m)^2]",
            "required_source": "parent action normalization and field dimension for m",
            "units_rule": "must make Z_m/F2 dimensionless if ell_tr=sqrt(Z_m L0^2/F2) is used",
            "current_status": "MISSING_PARENT_NORMALIZATION",
            "refusal_gate": "no dimensional claim, no numeric transition length",
            "valid_for_claim": "False",
        },
        {
            "prior_id": "ZPP1382_3_XB_range",
            "parameter": "I_X=X_B(D_loc)",
            "symbolic_prior": "compact interval or parent-defined admissible range",
            "required_source": "local branch/domain theorem and X_B map",
            "units_rule": "units inherited from X_B",
            "current_status": "MISSING_DOMAIN_RANGE",
            "refusal_gate": "no extrema theorem for Z_m",
            "valid_for_claim": "False",
        },
        {
            "prior_id": "ZPP1382_4_same_value_rule",
            "parameter": "universal Z_m law",
            "symbolic_prior": "one Z_m(X_B) law shared by local and cosmological branches",
            "required_source": "parent coefficient law and arena projection map",
            "units_rule": "unchanged across arenas",
            "current_status": "RULE_REQUIRED_NOT_FILLED",
            "refusal_gate": "no arena-specific retuning permitted",
            "valid_for_claim": "False",
        },
        {
            "prior_id": "ZPP1382_5_F2_sign_value",
            "parameter": "F2",
            "symbolic_prior": "stable second derivative with sign compatible with Z_m F2>0",
            "required_source": "parent potential expansion around m_*",
            "units_rule": "must share normalization with Z_m in transition-length formula",
            "current_status": "MISSING_PARENT_VALUE_AND_UNITS",
            "refusal_gate": "no ell_tr, U_B, Delta_m, or Q_alg numeric scoring",
            "valid_for_claim": "False",
        },
        {
            "prior_id": "ZPP1382_6_Mm2_gap",
            "parameter": "M_m^2",
            "symbolic_prior": "nonnegative Hessian/gap or explicit zero-mode removal",
            "required_source": "V_R(m;X_B) Hessian and boundary/zero-mode class",
            "units_rule": "operator mass-squared units",
            "current_status": "MISSING_GAP_AND_ZERO_MODE_TREATMENT",
            "refusal_gate": "no energy/nohair profile bound",
            "valid_for_claim": "False",
        },
        {
            "prior_id": "ZPP1382_7_sources_boundary",
            "parameter": "J_m, source/bath, boundary flux",
            "symbolic_prior": "zero theorem or finite bounds for every nonhomogeneous term",
            "required_source": "parent source map, bath status, and boundary flux condition",
            "units_rule": "operator-consistent source and flux units",
            "current_status": "MISSING_SOURCE_BATH_BOUNDARY_THEOREM",
            "refusal_gate": "no local profile suppression or stress residual bound",
            "valid_for_claim": "False",
        },
        {
            "prior_id": "ZPP1382_8_prior_verdict",
            "parameter": "Z_m symbolic prior pack",
            "symbolic_prior": "pack is allowed for algebraic dry-runs only",
            "required_source": "all rows above must be filled before any claim branch",
            "units_rule": "not claim-grade",
            "current_status": "SYMBOLIC_PRIOR_PACK_READY_NONCLAIM",
            "refusal_gate": "blocks local GR, PPN, R10, q_loc=0, and GitHub-ready claims",
            "valid_for_claim": "False",
        },
    ]


def runner_feed_rows() -> list[dict[str, str]]:
    return [
        {
            "feed_id": "RUF1382_0_admissibility",
            "runner_input": "Z_m admissibility scaffold",
            "formula_or_gate": "requires positivity, finite bounds, shared law, units, gap, sources, boundary",
            "status": "SCHEMA_READY_VALUES_MISSING",
            "numeric_scoring": "blocked",
            "claim_allowed": "False",
        },
        {
            "feed_id": "RUF1382_1_symbolic_transition_length",
            "runner_input": "ell_tr=sqrt(Z_m L0^2/F2)",
            "formula_or_gate": "allowed only as symbolic expression until Z_m, F2, L0 units and values are source-backed",
            "status": "SYMBOLIC_ONLY",
            "numeric_scoring": "blocked",
            "claim_allowed": "False",
        },
        {
            "feed_id": "RUF1382_2_stress_residual",
            "runner_input": "memory stress envelope",
            "formula_or_gate": "requires Z_m_bar and gradient/source/boundary bounds before any PPN/R10/local residual scoring",
            "status": "NONCLAIM_RESIDUAL_LEDGER_RETAINED",
            "numeric_scoring": "blocked",
            "claim_allowed": "False",
        },
        {
            "feed_id": "RUF1382_3_prior_pack",
            "runner_input": "symbolic prior pack",
            "formula_or_gate": "dry-run placeholders must carry valid_for_claim=false",
            "status": "READY_FOR_STRICT_VALIDATOR_DRYRUN",
            "numeric_scoring": "blocked",
            "claim_allowed": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE1382_0_sources",
            "gate": "all cited sources exist and anchors are present",
            "status": "PASS",
            "reason": "source register validates against the current local corpus",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1382_1_admissibility",
            "gate": "Z_m admissibility contract exists",
            "status": "PASS_SCAFFOLD_ONLY",
            "reason": "positivity, boundedness, shared-law, units, gap, and residual conditions are explicit",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1382_2_parent_law",
            "gate": "source-backed Z_m(X_B) coefficient law exists",
            "status": "BLOCKED_PARENT_LAW_MISSING",
            "reason": "no parent-signed function, sign theorem, value range, or normalization found",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1382_3_numeric_scoring",
            "gate": "ell_tr/U_B/Q_alg/local residuals can be scored",
            "status": "BLOCKED_SYMBOLIC_PRIORS_ONLY",
            "reason": "Z_m_min, Z_m_bar, F2, L0 normalization, source/boundary inputs are unresolved",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1382_4_local_claim",
            "gate": "local GR / PPN / R10 pass can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "admissibility is a contract, not a solved parent reduction",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1382_0",
            "question": "Did 1382 derive a source-backed Z_m coefficient law?",
            "answer": "No",
            "rationale": "It derived the admissibility conditions a law must satisfy, but the parent law/sign/range/units are still missing.",
            "next_action": "do not score local claims; build a strict symbolic-prior validator/dry-run",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1382_1",
            "question": "Is this progress?",
            "answer": "Yes, but it is infrastructure progress",
            "rationale": "The branch now has a precise shopping list instead of vague 'need coupling' language.",
            "next_action": "target the first row whose fill would unlock the most branches: Z_m_min/Z_m_bar/F2 normalization",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1382_0_1383",
            "next_doc": "1383-Y5-R10-RAB-Zm-symbolic-prior-validator-and-transition-runner-dryrun.md",
            "next_script": "scripts/Y5_R10_RAB_Zm_symbolic_prior_validator_and_transition_runner_dryrun.py",
            "task": "build a strict validator/dry-run for the Z_m symbolic prior pack, refusing numeric scoring unless Z_m_min, Z_m_bar, F2, L0, gap, source, and boundary rows are sourced",
            "success_condition": "validator emits machine-readable refusal gates and algebraic transition inequalities without any local-GR/PPN/R10 claim",
            "do_not_claim": "local GR;PPN pass;R10 pass;q_loc=0;numeric ell_tr;GitHub-ready result",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def validation_rows(
    sources: list[dict[str, str]],
    scaffold: list[dict[str, str]],
    prior_pack: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    all_sources_ok = all(row["exists"] == "True" and row["anchor_found"] == "True" for row in sources)
    no_prior_claims = all(row["valid_for_claim"] == "False" for row in prior_pack)
    local_blocked = any(row["gate_id"] == "GATE1382_4_local_claim" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    scaffold_ready = any(row["admissibility_id"] == "ZAS1382_8_verdict" for row in scaffold)
    outputs = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        ADMISSIBILITY_PATH,
        PRIOR_PACK_PATH,
        RUNNER_FEED_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
        Path("scripts/Y5_R10_RAB_Zm_coefficient_law_admissibility_or_symbolic_prior_pack.py"),
    ]
    outside_formalization = all("formalization-workbench" not in str(ROOT / path) for path in outputs)
    overall = all([all_sources_ok, no_prior_claims, local_blocked, scaffold_ready, outside_formalization])
    return [
        {
            "validation_id": "VAL1382_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if all_sources_ok else "FAIL",
            "details": "; ".join(f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources),
        },
        {
            "validation_id": "VAL1382_1_scaffold",
            "check": "Z_m admissibility scaffold is explicit",
            "status": "PASS" if scaffold_ready else "FAIL",
            "details": "ZAS1382_8 records scaffold-ready but symbolic-prior-required verdict.",
        },
        {
            "validation_id": "VAL1382_2_prior_nonclaim",
            "check": "symbolic prior rows remain nonclaim",
            "status": "PASS" if no_prior_claims else "FAIL",
            "details": "All ZPP1382 rows keep valid_for_claim=False.",
        },
        {
            "validation_id": "VAL1382_3_numeric_refusal",
            "check": "numeric transition/local scoring remains blocked",
            "status": "PASS" if local_blocked else "FAIL",
            "details": "GATE1382_4 keeps BLOCKED_NO_CLAIM.",
        },
        {
            "validation_id": "VAL1382_4_scope",
            "check": "generated outputs stay inside post-checkpoint-work and outside formalization-workbench",
            "status": "PASS" if outside_formalization else "FAIL",
            "details": f"ROOT={ROOT}; output_count={len(outputs)}; formalization_touched=False",
        },
        {
            "validation_id": "VAL1382_5_overall",
            "check": "overall 1382 validation",
            "status": "PASS" if overall else "FAIL",
            "details": "1382 writes a claim-blocking admissibility contract and symbolic prior pack for Z_m.",
        },
    ]


def write_doc(
    sources: list[dict[str, str]],
    scaffold: list[dict[str, str]],
    prior_pack: list[dict[str, str]],
    runner: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    generated = datetime.now(timezone.utc).isoformat()
    body = f"""# 1382 - Y5 R10 RAB Z_m Coefficient-Law Admissibility Or Symbolic Prior Pack

**Generated:** {generated}

**Current verdict:** the derivable part is now clean. If the memory-scalar route uses `Z_m(X_B)`, then a future parent action must prove positivity, finite bounds, shared local/cosmology law, units normalization, a gap/zero-mode rule, and source/boundary control. None of those become numeric evidence here.

**Discipline move:** keep `kappa_m=Z_m` as a symbolic closure coefficient only. The expression `ell_tr=sqrt(Z_m L0^2/F2)` may remain in algebraic dry-runs, but `ell_tr`, `U_B`, `Delta_m`, `Q_alg`, PPN, R10, and local-GR claims stay blocked until every prior row is filled by a source-backed parent law.

**Claim ceiling:** {CLAIM_CEILING}

## Source Register

{md_table(sources)}

## `Z_m(X_B)` Admissibility Scaffold

{md_table(scaffold)}

## Symbolic Prior Pack

{md_table(prior_pack)}

## Runner Feed Update

{md_table(runner)}

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
    scaffold = admissibility_rows()
    prior_pack = prior_pack_rows()
    runner = runner_feed_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, scaffold, prior_pack, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(ADMISSIBILITY_PATH, scaffold)
    write_csv(PRIOR_PACK_PATH, prior_pack)
    write_csv(RUNNER_FEED_PATH, runner)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, scaffold, prior_pack, runner, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1382 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()
