from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1386-Y5-R10-RAB-canonical-coupling-zero-theorem-or-beta-acquisition-runner.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1386_SOURCE_REGISTER.csv"
THEOREM_ATTEMPT_PATH = SRC_DIR / "P8_Y5_R10_1386_GC_ZERO_THEOREM_ATTEMPT.csv"
CLAUSE_MATRIX_PATH = SRC_DIR / "P8_Y5_R10_1386_PARENT_PACKAGE_CLAUSE_MATRIX.csv"
BETA_RUNNER_PATH = SRC_DIR / "P8_Y5_R10_1386_BETA_ACQUISITION_RUNNER_ROWS.csv"
ARENA_ROUTING_PATH = SRC_DIR / "P8_Y5_R10_1386_ARENA_ROUTING.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1386_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1386_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1386_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1386_VALIDATION.csv"

STATUS = (
    "canonical_coupling_zero_theorem_attempt_failed_parent_package_unsigned_"
    "beta_acquisition_runner_written_nonclaim"
)
CLAIM_CEILING = (
    "conditional_gc_zero_theorem_and_beta_acquisition_schema_only_no_parent_signed_zero_"
    "no_beta_score_no_R10_no_PPN_no_WEP_no_Newton_no_local_GR_pass"
)

SOURCE_ROWS = [
    {
        "source_id": "SRC1386_0_1385_doc",
        "source_path": "1385-Y5-R10-RAB-canonical-mass-gap-and-coupling-parent-contract.md",
        "required_anchor": "NEXT1385_0_1386",
        "purpose": "handoff from canonical gap/coupling contract",
    },
    {
        "source_id": "SRC1386_1_1385_next",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1385_NEXT_TARGET.csv",
        "required_anchor": "NEXT1385_0_1386",
        "purpose": "machine-readable 1386 target",
    },
    {
        "source_id": "SRC1386_2_1385_zero",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1385_GC_ZERO_ROUTE_AUDIT.csv",
        "required_anchor": "GZ1385_6_verdict",
        "purpose": "zero-route status and unsigned clauses",
    },
    {
        "source_id": "SRC1386_3_1385_finite",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1385_FINITE_CHANNEL_ACQUISITION_ROWS.csv",
        "required_anchor": "FCA1385_3_beta_product",
        "purpose": "finite coupling fallback rows",
    },
    {
        "source_id": "SRC1386_4_1044_pullback",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv",
        "required_anchor": "MPD1044_7_exact_theorem_if_signed",
        "purpose": "exact conditional matter pullback theorem",
    },
    {
        "source_id": "SRC1386_5_1045_functor",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "required_anchor": "MFS1045_6_verdict",
        "purpose": "parent matter functor signature verdict",
    },
    {
        "source_id": "SRC1386_6_1087_descent",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1087_PARENT_MATTER_DESCENT_ATTEMPT.csv",
        "required_anchor": "PMD1087_6_verdict",
        "purpose": "parent matter descent theorem failure",
    },
    {
        "source_id": "SRC1386_7_1229_theorem",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1229_LOCAL_GR_SOURCE_COUPLING_THEOREM_CONTRACT.csv",
        "required_anchor": "THM1229_2_countermodel",
        "purpose": "universal source coupling theorem and active finite countermodel",
    },
    {
        "source_id": "SRC1386_8_1229_clauses",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1229_UNIVERSAL_SOURCE_COUPLING_CLAUSE_AUDIT.csv",
        "required_anchor": "CLC1229_7_single_GN_normalization",
        "purpose": "universal source coupling parent clauses",
    },
    {
        "source_id": "SRC1386_9_1229_counterexamples",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1229_SOURCE_COUPLING_COUNTEREXAMPLE_LEDGER.csv",
        "required_anchor": "CEX1229_0_action_multiplier",
        "purpose": "active source coupling counterexamples",
    },
    {
        "source_id": "SRC1386_10_1036_beta",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1036_BETA_SOURCE_TEST_DERIVATION.csv",
        "required_anchor": "BETA1036_3_common_Weyl_cg",
        "purpose": "finite beta source/test derivation",
    },
    {
        "source_id": "SRC1386_11_1036_template",
        "source_path": "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_1036_PARENT_X_BETA_TEMPLATE_NONCLAIM.csv",
        "required_anchor": "universal_weyl_cg_squared_template",
        "purpose": "nonclaim R10 beta product template",
    },
    {
        "source_id": "SRC1386_12_1077_wep",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1077_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv",
        "required_anchor": "WCO1077_5_verdict",
        "purpose": "WEP coupling-owner theorem failure",
    },
    {
        "source_id": "SRC1386_13_1023_descent",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1023_COUPLING_DESCENT_AUDIT.csv",
        "required_anchor": "CDA1023_4_verdict",
        "purpose": "coupling descent verdict",
    },
    {
        "source_id": "SRC1386_14_this_script",
        "source_path": "scripts/Y5_R10_RAB_canonical_coupling_zero_theorem_or_beta_acquisition_runner.py",
        "required_anchor": "STATUS",
        "purpose": "1386 generator",
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
        rows.append(
            {
                **row,
                "exists": str(source_path.exists()),
                "anchor_found": str(anchor_found(source_path, row["required_anchor"])),
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def theorem_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "attempt_id": "GCT1386_0_chain_rule",
            "claim_piece": "canonical matter variation identity",
            "mathematical_statement": "delta_vphi S_A = 1/2 int sqrt(-g_obs) T_A^{mu nu} Lie_vphi g_obs_munu + sum_i int J_theta_i Lie_vphi theta_i + boundary/gauge/E_Psi terms",
            "proof_status": "STANDARD_CHAIN_RULE_IMPORTED",
            "current_result": "if every term on the right is parent-zero, beta_A=0",
            "blocking_gap": "the zero of each term is conditional, not parent-signed as one package",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "GCT1386_1_sufficient_theorem",
            "claim_piece": "exact conditional g_c=0 theorem",
            "mathematical_statement": "Dq[v_phi]=0, e_obs=Obs(q), theta_A phi-blind, matter lift fixed/gauge, no action weights, no shadow frame, and boundary/readout silence imply delta_vphi S_matter=0",
            "proof_status": "EXACT_CONDITIONAL_THEOREM_WRITTEN",
            "current_result": "beta_source=beta_test=g_c=0 follows only if all clauses close before variation/readout",
            "blocking_gap": "clauses are spread across contracts but not signed by one parent action",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "GCT1386_2_counterexample_test",
            "claim_piece": "action-weight obstruction",
            "mathematical_statement": "S_matter=sum_A w_A S_A with constant w_A can preserve isolated classical equations while changing Hilbert source weights",
            "proof_status": "COUNTEREXAMPLE_ACTIVE",
            "current_result": "g_c=0/universal-source theorem is not claim-grade in current corpus",
            "blocking_gap": "no parent object-language/action-measure theorem excludes w_A or proves w_A=w_*",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "GCT1386_3_descent_package_test",
            "claim_piece": "single parent matter package",
            "mathematical_statement": "the q-kernel, observed coframe, matter bundle, constants, current owner, action scale, and boundary projection must be one parent signature",
            "proof_status": "PACKAGE_NOT_SIGNED",
            "current_result": "conditional pieces do not compose into a theorem because active countermodels can enter through unsigned seams",
            "blocking_gap": "parent action syntax and ordinary matter category are not fixed enough",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "GCT1386_4_zero_verdict",
            "claim_piece": "g_c=0 theorem verdict",
            "mathematical_statement": "the theorem route is mathematically sharp but not closed by current evidence",
            "proof_status": "ZERO_THEOREM_NOT_CLOSED_CURRENT_CORPUS",
            "current_result": "finite beta_source/beta_test acquisition runner is required as fallback",
            "blocking_gap": "action-weight exclusion and source/current owner are highest-pressure next clauses",
            "valid_for_claim": "False",
        },
    ]


def clause_matrix_rows() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "PCM1386_0_q_kernel",
            "parent_clause": "canonical phi direction is quotient-vertical",
            "required_certificate": "Dq_loc[v_phi]=0 from parent quotient map",
            "current_status": "UNSIGNED",
            "counterexample_if_open": "phi moves observed geometry or source labels",
            "source_anchor": "GZ1385_0_q_kernel;MFS1045_0_parent_field_quotient",
            "next_action": "derive q_loc and v_phi from parent, not post-readout",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "PCM1386_1_observed_coframe",
            "parent_clause": "observed coframe/metric descends only through q",
            "required_certificate": "e_obs=Obs_e(q(Phi)) and Lie_vphi e_obs=0",
            "current_status": "SUFFICIENT_SIGNATURE_NOT_PARENT_SIGNED",
            "counterexample_if_open": "hidden Weyl/disformal frame gives universal finite g_c",
            "source_anchor": "MFS1045_1_observed_coframe_functor;MFS1045_4_no_shadow_frame",
            "next_action": "prove no A(phi), B(phi), independent connection, or shadow frame",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "PCM1386_2_matter_bundle_lift",
            "parent_clause": "ordinary matter bundle/lift is parent-owned",
            "required_certificate": "Psi_A in Gamma(E_A[e_obs]) and delta_vphi Psi_A is fixed/gauge/boundary-only",
            "current_status": "MATTER_CATEGORY_NOT_PARENT_CONSTRUCTED",
            "counterexample_if_open": "matter field lift creates a physical J_c source",
            "source_anchor": "MFS1045_2_matter_bundle_functor;MFS1045_3_vertical_lift;PMD1087_2_matter_lift",
            "next_action": "construct ordinary matter functor in parent action",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "PCM1386_3_constants",
            "parent_clause": "ordinary constants are phi-blind representation/superselection data",
            "required_certificate": "Lie_vphi theta_A=0 for masses, charges, alpha_EM, clock standards, material labels",
            "current_status": "CONSTANT_SUPERSELECTION_UNSIGNED",
            "counterexample_if_open": "clock/WEP/fine-structure source charges survive",
            "source_anchor": "MPD1044_3_constants_zero;PMD1087_3_material_constants",
            "next_action": "prove constant-sector superselection or add residual coefficient rows",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "PCM1386_4_action_weight_exclusion",
            "parent_clause": "no independent species/source action multiplier",
            "required_certificate": "S_matter has one action scale/measure or w_A=w_* quotient-equivalent/null-projected",
            "current_status": "ACTIVE_COUNTEREXAMPLE",
            "counterexample_if_open": "S_matter=sum_A w_A S_A preserves local classical form but breaks source universality",
            "source_anchor": "THM1229_2_countermodel;CEX1229_0_action_multiplier;PMD1087_4_pre_action_weights",
            "next_action": "derive object-language/action-measure exclusion of inert source scalars",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "PCM1386_5_source_current_owner",
            "parent_clause": "single Hilbert/source current owner before readout",
            "required_certificate": "delta S_matter/delta e_obs gives one common T_eff and descends with Bianchi/Noether closure",
            "current_status": "NOT_DERIVED",
            "counterexample_if_open": "non-Hilbert current or source-normalization weight survives",
            "source_anchor": "WCO1077_4_current_owner;CLC1229_6_noether_bianchi_closure",
            "next_action": "derive current/source normalization functor",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "PCM1386_6_boundary_readout",
            "parent_clause": "boundary/readout/projector tails are silent or bounded",
            "required_certificate": "variation before readout plus boundary/local projection silence",
            "current_status": "UNSIGNED_BOUNDARY_LOCAL_PROJECTION",
            "counterexample_if_open": "bulk zero theorem is spoiled by tau_WEP/R10/clock/orbital projection",
            "source_anchor": "CLC1229_3_variation_before_readout;CLC1229_5_boundary_projection_silence;PMD1087_5_hidden_domain_boundary",
            "next_action": "derive projection silence or score tails",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "PCM1386_7_package_verdict",
            "parent_clause": "all clauses close as one parent package",
            "required_certificate": "PCM1386_0 through PCM1386_6 all parent-signed before scoring",
            "current_status": "PACKAGE_FAILS_CURRENT_CLAIM",
            "counterexample_if_open": "finite beta runner remains mandatory",
            "source_anchor": "PMD1087_6_verdict;GCT1386_4_zero_verdict",
            "next_action": "attack action-weight exclusion first or proceed to finite beta acquisition",
            "valid_for_claim": "False",
        },
    ]


def beta_runner_rows() -> list[dict[str, str]]:
    return [
        {
            "beta_id": "BAR1386_0_convention",
            "quantity": "beta convention",
            "formula": "declare whether beta_A=partial_phi ln m_A^eff is dimensionless and whether 4pi G_N, M_Pl, or Z_X factors are absorbed",
            "required_source": "canonical phi normalization, G_N calibration, source/test action convention",
            "units": "convention row",
            "arena_use": "all finite coupling arenas",
            "status": "MISSING_CONVENTION_LOCK",
            "valid_for_claim": "False",
        },
        {
            "beta_id": "BAR1386_1_mu_m2",
            "quantity": "mu_m^2(X_B)",
            "formula": "lambda_m=1/sqrt(mu_m^2)",
            "required_source": "parent canonical mass-gap law or no-pole theorem",
            "units": "length^-2",
            "arena_use": "R10 range; profile suppression; PPN finite range",
            "status": "MISSING_CANONICAL_GAP",
            "valid_for_claim": "False",
        },
        {
            "beta_id": "BAR1386_2_beta_source",
            "quantity": "beta_source",
            "formula": "beta_s=partial_phi ln m_source^eff or source-current derivative in canonical variables",
            "required_source": "source worldtube, Hilbert current, no measured-G absorption cheat",
            "units": "dimensionless after convention lock",
            "arena_use": "R10 source leg; Newton source normalization; WEP source charge",
            "status": "MISSING_SOURCE_BETA",
            "valid_for_claim": "False",
        },
        {
            "beta_id": "BAR1386_3_beta_test",
            "quantity": "beta_test",
            "formula": "beta_t=partial_phi ln m_test^eff or test-body action derivative",
            "required_source": "test-body material action, composition map, clock/material standard map",
            "units": "same as beta_source",
            "arena_use": "R10 test leg; WEP; clocks; orbital test response",
            "status": "MISSING_TEST_BETA",
            "valid_for_claim": "False",
        },
        {
            "beta_id": "BAR1386_4_beta_product",
            "quantity": "beta_source*beta_test",
            "formula": "alpha_X(lambda)=K_X(lambda) beta_s beta_t + epsilon_tail(lambda); universal Weyl branch gives c_g^2",
            "required_source": "beta_s, beta_t, K_X/profile factor, tail envelope, bound curve",
            "units": "dimensionless alpha after convention lock",
            "arena_use": "R10 alpha(lambda); finite fifth-force estimates",
            "status": "PRODUCT_FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": "False",
        },
        {
            "beta_id": "BAR1386_5_species_matrix",
            "quantity": "beta_A matrix",
            "formula": "Delta beta_AB=beta_A-beta_B and/or eta_source_AB from source/test beta differences",
            "required_source": "material/composition basis, species labels, parent no-marker or finite coefficients",
            "units": "dimensionless",
            "arena_use": "WEP, clocks, composition dependence",
            "status": "MISSING_SPECIES_BETA_MATRIX",
            "valid_for_claim": "False",
        },
        {
            "beta_id": "BAR1386_6_tail_envelope",
            "quantity": "epsilon_tail",
            "formula": "epsilon_tail=sum_abs(hidden frame, readout, boundary, projector, non-EH, source-normalization tails)",
            "required_source": "component theorem-zero or finite bounds with no-cancellation policy",
            "units": "arena-dependent",
            "arena_use": "all local arenas",
            "status": "MISSING_TAIL_COMPONENT_BOUNDS",
            "valid_for_claim": "False",
        },
        {
            "beta_id": "BAR1386_7_runner_verdict",
            "quantity": "finite beta acquisition runner",
            "formula": "runner can parse rows but must refuse scoring until BAR1386_0 through BAR1386_6 are claim-grade",
            "required_source": "complete finite acquisition pack",
            "units": "not claim-grade",
            "arena_use": "future R10/PPN/WEP runner",
            "status": "SCHEMA_READY_NO_NUMERIC_SCORING",
            "valid_for_claim": "False",
        },
    ]


def arena_rows() -> list[dict[str, str]]:
    return [
        {
            "arena_id": "ROUTE1386_0_R10",
            "arena": "R10 alpha(lambda)",
            "zero_route_if_closed": "g_c=0 and no tails -> alpha_X=0 for canonical coupling channel",
            "finite_route_if_open": "alpha_X(lambda)=K_X beta_s beta_t + epsilon_tail",
            "blocked_by": "mu_m^2, beta_s, beta_t, K_X, tail envelope, bound curve",
            "status": "BLOCKED",
            "claim_allowed": "False",
        },
        {
            "arena_id": "ROUTE1386_1_PPN",
            "arena": "PPN residual vector",
            "zero_route_if_closed": "matter coupling channel zero; still check memory stress/source/boundary tails",
            "finite_route_if_open": "project beta/profile/tails into gamma-1,beta-1,alpha1,alpha2,alpha3,xi",
            "blocked_by": "arena projection kernels and tail component bounds",
            "status": "BLOCKED",
            "claim_allowed": "False",
        },
        {
            "arena_id": "ROUTE1386_2_WEP",
            "arena": "WEP/source charge",
            "zero_route_if_closed": "beta_A common/zero and source weights theorem-zero",
            "finite_route_if_open": "score Delta beta_AB or tau_WEP product against WEP bounds",
            "blocked_by": "composition matrix, source worldtube, tau_WEP projection",
            "status": "BLOCKED",
            "claim_allowed": "False",
        },
        {
            "arena_id": "ROUTE1386_3_clocks",
            "arena": "clocks/constants",
            "zero_route_if_closed": "theta_A phi-blind superselection",
            "finite_route_if_open": "score beta_alpha, beta_mass, beta_clock against clock/constant drift bounds",
            "blocked_by": "constant-sector parent theorem or finite coefficients",
            "status": "BLOCKED",
            "claim_allowed": "False",
        },
        {
            "arena_id": "ROUTE1386_4_Newton_orbital",
            "arena": "Newton/orbital source normalization",
            "zero_route_if_closed": "single source current and one constant G_N calibration",
            "finite_route_if_open": "score source-normalization drift/range/species/frame residuals",
            "blocked_by": "action-weight exclusion, current owner, no measured-G absorption cheat",
            "status": "BLOCKED",
            "claim_allowed": "False",
        },
        {
            "arena_id": "ROUTE1386_5_local_GR",
            "arena": "local GR reduction",
            "zero_route_if_closed": "all coupling channels theorem-zero plus stress/source/boundary tails bounded",
            "finite_route_if_open": "requires complete local residual vector below bounds",
            "blocked_by": "zero theorem not closed and beta runner not filled",
            "status": "BLOCKED",
            "claim_allowed": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE1386_0_sources",
            "gate": "all cited sources exist and anchors are present",
            "status": "PASS",
            "reason": "source register validates against local corpus",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1386_1_conditional_theorem",
            "gate": "conditional g_c=0 theorem is written",
            "status": "PASS_CONDITIONAL_THEOREM",
            "reason": "chain-rule theorem and sufficient parent package are explicit",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1386_2_parent_zero",
            "gate": "g_c=0 theorem is parent-signed",
            "status": "BLOCKED_PARENT_PACKAGE_UNSIGNED",
            "reason": "action-weight/source-current/coframe/matter package clauses remain unsigned",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1386_3_beta_runner",
            "gate": "finite beta acquisition runner exists",
            "status": "PASS_SCHEMA_ONLY",
            "reason": "BAR1386 rows define finite acquisition inputs with valid_for_claim=false",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1386_4_numeric",
            "gate": "finite beta/R10/PPN/WEP scoring can run",
            "status": "BLOCKED_VALUES_MISSING",
            "reason": "mu_m^2, beta_s, beta_t, convention, species matrix, tail envelope and arena kernels are missing",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1386_5_local_claim",
            "gate": "local GR / Newton / PPN / R10 / WEP pass can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1386 is a theorem attempt plus fallback schema, not a derived local GR limit",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1386_0_zero_theorem",
            "decision": "conditional g_c=0 theorem is correct but unsigned",
            "because": "chain-rule descent works only if all parent package clauses close together before readout",
            "next_action": "attack the action-weight/source-current owner clauses first",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1386_1_counterexample",
            "decision": "action-weight counterexample is the highest-pressure obstruction",
            "because": "S_matter=sum_A w_A S_A can hide from isolated classical equations while breaking source universality",
            "next_action": "derive object-language/action-measure exclusion or retain Delta_w/beta rows",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1386_2_fallback",
            "decision": "finite beta acquisition runner is staged",
            "because": "if zero theorem fails, local tests require source/test beta legs plus tails, not a single coupling",
            "next_action": "fill beta_s/beta_t only after convention and source/test worldtube rows exist",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1386_0_1387",
            "next_doc": "1387-Y5-R10-RAB-action-weight-exclusion-or-source-beta-first-fill.md",
            "next_script": "scripts/Y5_R10_RAB_action_weight_exclusion_or_source_beta_first_fill.py",
            "task": "try to exclude independent species/source action weights w_A from the parent object language and action measure; if it fails, create the first finite Delta_w/beta_source row with source requirements",
            "success_condition": "either the action-weight counterexample is killed by a parent-signed clause, or a nonclaim source beta/action-weight acquisition row is ready and all local claims remain blocked",
            "do_not_claim": "local GR;Newton limit;PPN pass;R10 pass;WEP pass;q_loc=0;numeric alpha(lambda);GitHub-ready result",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def validation_rows(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    matrix: list[dict[str, str]],
    beta: list[dict[str, str]],
    arenas: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    all_sources_ok = all(row["exists"] == "True" and row["anchor_found"] == "True" for row in sources)
    conditional_theorem = any(row["attempt_id"] == "GCT1386_1_sufficient_theorem" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM_WRITTEN" for row in theorem)
    zero_not_closed = any(row["attempt_id"] == "GCT1386_4_zero_verdict" and row["proof_status"] == "ZERO_THEOREM_NOT_CLOSED_CURRENT_CORPUS" for row in theorem)
    package_fails = any(row["clause_id"] == "PCM1386_7_package_verdict" and row["current_status"] == "PACKAGE_FAILS_CURRENT_CLAIM" for row in matrix)
    beta_schema = any(row["beta_id"] == "BAR1386_7_runner_verdict" and row["status"] == "SCHEMA_READY_NO_NUMERIC_SCORING" for row in beta)
    beta_nonclaim = all(row["valid_for_claim"] == "False" for row in beta)
    arenas_blocked = all(row["status"] == "BLOCKED" and row["claim_allowed"] == "False" for row in arenas)
    local_blocked = any(row["gate_id"] == "GATE1386_5_local_claim" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    outputs = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        THEOREM_ATTEMPT_PATH,
        CLAUSE_MATRIX_PATH,
        BETA_RUNNER_PATH,
        ARENA_ROUTING_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
        Path("scripts/Y5_R10_RAB_canonical_coupling_zero_theorem_or_beta_acquisition_runner.py"),
    ]
    outside_formalization = all("formalization-workbench" not in str(ROOT / path) for path in outputs)
    overall = all([all_sources_ok, conditional_theorem, zero_not_closed, package_fails, beta_schema, beta_nonclaim, arenas_blocked, local_blocked, outside_formalization])
    return [
        {
            "validation_id": "VAL1386_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if all_sources_ok else "FAIL",
            "details": "; ".join(f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources),
        },
        {
            "validation_id": "VAL1386_1_conditional_theorem",
            "check": "conditional g_c=0 theorem is written",
            "status": "PASS" if conditional_theorem else "FAIL",
            "details": "GCT1386_1 records the exact sufficient theorem.",
        },
        {
            "validation_id": "VAL1386_2_zero_refusal",
            "check": "g_c=0 is not falsely claimed",
            "status": "PASS" if zero_not_closed and package_fails else "FAIL",
            "details": "GCT1386_4 and PCM1386_7 keep the parent package unsigned.",
        },
        {
            "validation_id": "VAL1386_3_beta_schema",
            "check": "finite beta fallback schema exists and remains nonclaim",
            "status": "PASS" if beta_schema and beta_nonclaim else "FAIL",
            "details": "BAR1386 rows define beta acquisition and keep valid_for_claim=False.",
        },
        {
            "validation_id": "VAL1386_4_arena_refusal",
            "check": "arena routing remains blocked",
            "status": "PASS" if arenas_blocked and local_blocked else "FAIL",
            "details": "ROUTE1386 rows and GATE1386_5 block local/R10/PPN/WEP claims.",
        },
        {
            "validation_id": "VAL1386_5_scope",
            "check": "generated outputs stay inside post-checkpoint-work and outside formalization-workbench",
            "status": "PASS" if outside_formalization else "FAIL",
            "details": f"ROOT={ROOT}; output_count={len(outputs)}; formalization_touched=False",
        },
        {
            "validation_id": "VAL1386_6_overall",
            "check": "overall 1386 validation",
            "status": "PASS" if overall else "FAIL",
            "details": "1386 writes the conditional g_c=0 theorem, rejects current closure, and stages finite beta acquisition.",
        },
    ]


def write_doc(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    matrix: list[dict[str, str]],
    beta: list[dict[str, str]],
    arenas: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    generated = datetime.now(timezone.utc).isoformat()
    body = f"""# 1386 - Y5 R10 RAB Canonical Coupling Zero Theorem Or Beta Acquisition Runner

**Generated:** {generated}

**Current verdict:** the `g_c=0` theorem is mathematically sharp but not parent-signed. The chain-rule proof works if quotient verticality, observed coframe descent, matter lift, constant silence, action-weight exclusion, source-current ownership, and boundary/readout silence all close as one parent package. Current corpus does not close that package.

**Fallback:** finite local coupling must be acquired as `beta_source * beta_test` with a declared convention, canonical range `mu_m^2`, source/test worldtubes, species matrix, and no-cancellation tail envelope. No single naked `c_g` score is allowed.

**Claim ceiling:** {CLAIM_CEILING}

## Source Register

{md_table(sources)}

## `g_c=0` Theorem Attempt

{md_table(theorem)}

## Parent Package Clause Matrix

{md_table(matrix)}

## Beta Acquisition Runner Rows

{md_table(beta)}

## Arena Routing

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
    theorem = theorem_attempt_rows()
    matrix = clause_matrix_rows()
    beta = beta_runner_rows()
    arenas = arena_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, theorem, matrix, beta, arenas, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(THEOREM_ATTEMPT_PATH, theorem)
    write_csv(CLAUSE_MATRIX_PATH, matrix)
    write_csv(BETA_RUNNER_PATH, beta)
    write_csv(ARENA_ROUTING_PATH, arenas)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, theorem, matrix, beta, arenas, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1386 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()
