from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1385-Y5-R10-RAB-canonical-mass-gap-and-coupling-parent-contract.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1385_SOURCE_REGISTER.csv"
CONTRACT_PATH = SRC_DIR / "P8_Y5_R10_1385_CANONICAL_GAP_COUPLING_CONTRACT.csv"
ZERO_ROUTE_PATH = SRC_DIR / "P8_Y5_R10_1385_GC_ZERO_ROUTE_AUDIT.csv"
FINITE_ROWS_PATH = SRC_DIR / "P8_Y5_R10_1385_FINITE_CHANNEL_ACQUISITION_ROWS.csv"
ARENA_GATES_PATH = SRC_DIR / "P8_Y5_R10_1385_ARENA_PROJECTION_REFUSAL_GATES.csv"
RUNNER_FEED_PATH = SRC_DIR / "P8_Y5_R10_1385_RUNNER_FEED_UPDATE.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1385_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1385_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1385_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1385_VALIDATION.csv"

STATUS = (
    "canonical_mass_gap_and_coupling_parent_contract_written_"
    "zero_route_unsigned_finite_beta_fallback_ready_nonclaim"
)
CLAIM_CEILING = (
    "canonical_gap_coupling_contract_only_no_parent_signed_gc_zero_no_finite_beta_score_"
    "no_R10_no_PPN_no_WEP_no_Newton_no_local_GR_pass"
)

SOURCE_ROWS = [
    {
        "source_id": "SRC1385_0_1384_doc",
        "source_path": "1384-Y5-R10-RAB-Zm-parent-coefficient-law-derivation-attempt-or-F2-normalization-pivot.md",
        "required_anchor": "NEXT1384_0_1385",
        "purpose": "handoff from canonical pivot to mass-gap/coupling contract",
    },
    {
        "source_id": "SRC1385_1_1384_next",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1384_NEXT_TARGET.csv",
        "required_anchor": "NEXT1384_0_1385",
        "purpose": "machine-readable 1385 target",
    },
    {
        "source_id": "SRC1385_2_1384_pivot",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1384_FIELD_REDEFINITION_INVARIANT_PIVOT.csv",
        "required_anchor": "IPV1384_4_verdict",
        "purpose": "canonical invariant pivot rows",
    },
    {
        "source_id": "SRC1385_3_1384_first_fill",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1384_FIRST_FILL_ROW_SELECTION.csv",
        "required_anchor": "FFR1384_4_selection",
        "purpose": "selected first-fill pair mu_m^2 and g_c",
    },
    {
        "source_id": "SRC1385_4_1036_beta",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1036_BETA_SOURCE_TEST_DERIVATION.csv",
        "required_anchor": "BETA1036_4_quotient_zero",
        "purpose": "source/test beta law and quotient-zero branch",
    },
    {
        "source_id": "SRC1385_5_1036_decision",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1036_DECISION_LEDGER.csv",
        "required_anchor": "DEC1036_1_coupling_law_status",
        "purpose": "corrected coupling law beta_source times beta_test",
    },
    {
        "source_id": "SRC1385_6_1229_theorem",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1229_LOCAL_GR_SOURCE_COUPLING_THEOREM_CONTRACT.csv",
        "required_anchor": "THM1229_1_iff",
        "purpose": "universal source coupling iff contract",
    },
    {
        "source_id": "SRC1385_7_1229_clauses",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1229_UNIVERSAL_SOURCE_COUPLING_CLAUSE_AUDIT.csv",
        "required_anchor": "CLC1229_0_single_action_scale",
        "purpose": "unsigned clauses needed for universal source coupling",
    },
    {
        "source_id": "SRC1385_8_1229_counterexamples",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1229_SOURCE_COUPLING_COUNTEREXAMPLE_LEDGER.csv",
        "required_anchor": "CEX1229_0_action_multiplier",
        "purpose": "active counterexamples if source multipliers survive",
    },
    {
        "source_id": "SRC1385_9_1044_pullback",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv",
        "required_anchor": "MPD1044_1_chain_rule_identity",
        "purpose": "matter pullback chain-rule identity and sufficient zero clauses",
    },
    {
        "source_id": "SRC1385_10_1045_functor",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "required_anchor": "MFS1045_4_no_shadow_frame",
        "purpose": "parent matter functor and no-shadow-frame signature audit",
    },
    {
        "source_id": "SRC1385_11_1087_descent",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1087_PARENT_MATTER_DESCENT_ATTEMPT.csv",
        "required_anchor": "PMD1087_4_pre_action_weights",
        "purpose": "matter descent attempt with action-weight leak",
    },
    {
        "source_id": "SRC1385_12_1023_descent",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1023_COUPLING_DESCENT_AUDIT.csv",
        "required_anchor": "CDA1023_4_verdict",
        "purpose": "coupling descent verdict",
    },
    {
        "source_id": "SRC1385_13_930_chain",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_930_COUPLING_DERIVATION_CHAIN.csv",
        "required_anchor": "KD930_1_chain_integral",
        "purpose": "topological/source coupling ratio clue",
    },
    {
        "source_id": "SRC1385_14_1077_wep",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1077_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv",
        "required_anchor": "WCO1077_1_conditional_theorem",
        "purpose": "conditional WEP coupling-owner theorem",
    },
    {
        "source_id": "SRC1385_15_this_script",
        "source_path": "scripts/Y5_R10_RAB_canonical_mass_gap_and_coupling_parent_contract.py",
        "required_anchor": "STATUS",
        "purpose": "1385 generator",
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


def contract_rows() -> list[dict[str, str]]:
    return [
        {
            "contract_id": "CGC1385_0_canonical_action",
            "object": "canonical local memory mode",
            "formal_contract": "S_phi=integral sqrt(-g)[-1/2(nabla phi)^2 -1/2 mu_m^2(X_B) phi^2 + phi J_c + L_residual]",
            "derivation_status": "CONDITIONAL_FROM_1384_CANONICALIZATION",
            "required_missing_clause": "parent adoption of canonical local branch, field domain, source/bath/boundary class",
            "if_closed": "runner can use physical mu_m^2 and J_c instead of normalization-dependent Z_m/F2",
            "if_open": "keep canonical branch nonclaim",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "CGC1385_1_mass_gap",
            "object": "mu_m^2(X_B)",
            "formal_contract": "mu_m^2=F2/(Z_m L0^2)>0, with one universal local/cosmology law or a parent zero/no-pole alternative",
            "derivation_status": "FORMULA_DERIVED_VALUE_NOT_SOURCED",
            "required_missing_clause": "parent Hessian/kinetic ratio or direct canonical mass-gap theorem with units and branch domain",
            "if_closed": "ell_tr=1/sqrt(mu_m^2) and support suppression can be scored algebraically",
            "if_open": "no numeric transition length or R10 range",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "CGC1385_2_canonical_source",
            "object": "J_c and g_c(X_B)",
            "formal_contract": "J_c = g_c(X_B) T_obs + J_species + J_frame + J_boundary + J_readout, in canonical phi normalization",
            "derivation_status": "CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "required_missing_clause": "matter descent/source map in canonical variables, source worldtube, and no-shadow-frame theorem",
            "if_closed": "finite local residuals can be routed through beta_source beta_test or theorem-zero g_c=0",
            "if_open": "coupling remains the main local obstruction",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "CGC1385_3_zero_coupling_route",
            "object": "g_c=0 theorem",
            "formal_contract": "if S_matter descends through quotient-owned observed coframe and v_phi is vertical, with constants/action weights/no-shadow frames silent, then delta_phi S_matter=0 and beta_source=beta_test=0",
            "derivation_status": "EXACT_CONDITIONAL_ROUTE_UNSIGNED",
            "required_missing_clause": "q-kernel, observed coframe functor, matter lift, constant superselection, no action weights, no boundary/readout tails",
            "if_closed": "finite fifth-force/R10/WEP/PPN coupling channel theorem-zero, subject to stress/source residual checks",
            "if_open": "finite beta acquisition rows remain mandatory",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "CGC1385_4_universal_finite_route",
            "object": "universal nonzero canonical coupling",
            "formal_contract": "if m_A^eff=A(phi)m_A for all ordinary matter, beta_source=beta_test=partial_phi ln A = g_c and alpha-like exchange scales as beta_source beta_test, not linear g_c",
            "derivation_status": "STANDARD_VARIATION_CONDITIONAL_NOT_SOURCED",
            "required_missing_clause": "parent-signed universal A(phi), phi normalization, source/test profile factors, same observed-G calibration",
            "if_closed": "WEP may be structurally safer but PPN/R10/clock/orbital bounds still score finite residuals",
            "if_open": "no finite coupling score",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "CGC1385_5_species_marker_route",
            "object": "species/material/marker coupling",
            "formal_contract": "if beta_A differs by species/material/source preparation, eta_WEP, clock drift, source-charge, and R10 source/test products remain active",
            "derivation_status": "COUNTEREXAMPLES_ACTIVE",
            "required_missing_clause": "no inert source scalars, no species action weights, species-blind measure/coframe, connected matter category",
            "if_closed": "species split can collapse to universal or zero coupling branch",
            "if_open": "WEP/source-charge rows remain retained",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "CGC1385_6_no_single_coupling_shortcut",
            "object": "local exchange amplitude",
            "formal_contract": "observable finite exchange requires beta_source*beta_test plus profile/tail factors; a single naked c_g cannot score R10/PPN unless one leg is explicitly packed and sourced",
            "derivation_status": "CORRECTED_LAW_IMPORTED_FROM_1036",
            "required_missing_clause": "declaration of beta convention and whether Qbar/K already includes a source leg",
            "if_closed": "future alpha(lambda) templates avoid linear-coupling mistakes",
            "if_open": "all alpha rows remain invalid",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "CGC1385_7_verdict",
            "object": "canonical gap-coupling contract",
            "formal_contract": "local branch first physical pair is mu_m^2(X_B) and g_c/beta_source,beta_test; cleanest route is g_c=0 from matter descent, fallback is finite beta acquisition",
            "derivation_status": "CONTRACT_READY_ZERO_ROUTE_UNSIGNED",
            "required_missing_clause": "parent-signed matter descent or source-backed finite beta rows",
            "if_closed": "move toward genuine local GR reduction test",
            "if_open": "keep local GR/Newton/PPN/R10 claims blocked",
            "valid_for_claim": "False",
        },
    ]


def zero_route_rows() -> list[dict[str, str]]:
    return [
        {
            "zero_id": "GZ1385_0_q_kernel",
            "zero_clause": "canonical memory variation lies in the quotient kernel",
            "mathematical_condition": "Dq_loc[v_phi]=0",
            "current_evidence": "1044/1045/1087 state the chain-rule route but keep quotient/coframe functor unsigned",
            "status": "UNSIGNED",
            "if_missing": "metric/coframe matter coupling can survive as beta_geom",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "GZ1385_1_observed_coframe",
            "zero_clause": "ordinary matter sees only the quotient-owned observed coframe/metric",
            "mathematical_condition": "e_obs=Obs_e(q(Phi)); Lie_vphi e_obs=0; no hidden A(phi), B(phi), or independent connection",
            "current_evidence": "MFS1045_1 and MFS1045_4 are sufficient signatures but not parent signed",
            "status": "UNSIGNED",
            "if_missing": "universal or species-dependent Weyl/disformal finite coupling remains legal",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "GZ1385_2_matter_lift",
            "zero_clause": "vertical lift on ordinary matter is fixed/gauge",
            "mathematical_condition": "delta_vphi Psi_A=0 or owned gauge/Lorentz/diffeomorphism lift with boundary-only variation",
            "current_evidence": "MPD1044_4 and PMD1087_2 give the sufficient sublemma but parent map is missing",
            "status": "UNSIGNED",
            "if_missing": "matter field variation can contribute J_c",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "GZ1385_3_constants",
            "zero_clause": "masses, charges, clocks, and representation constants are phi-blind",
            "mathematical_condition": "Lie_vphi theta_A=0",
            "current_evidence": "MPD1044_3 and PMD1087_3 keep constant superselection unsigned",
            "status": "UNSIGNED",
            "if_missing": "clock/WEP/fifth-force source-charge rows remain active",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "GZ1385_4_action_weights",
            "zero_clause": "no independent species/source action multiplier survives",
            "mathematical_condition": "S_matter is not sum_A w_A S_A unless w_A is quotient-equivalent/common or null-projected",
            "current_evidence": "THM1229_2 and CEX1229_0 show active countermodels; CLC1229 clauses unsigned",
            "status": "ACTIVE_COUNTEREXAMPLE",
            "if_missing": "universal source coupling and Newton source normalization fail",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "GZ1385_5_boundary_readout",
            "zero_clause": "boundary/readout/projector tails do not reintroduce phi source",
            "mathematical_condition": "J_boundary=J_readout=J_projector=0 or finite bounded below arena locks",
            "current_evidence": "1023 keeps projector/boundary coupling open; 1229 readout reweighting counterexample active",
            "status": "UNSIGNED",
            "if_missing": "tau_WEP, R10, clocks, orbital and PPN arena kernels must be filled",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "GZ1385_6_verdict",
            "zero_clause": "g_c=0 theorem route",
            "mathematical_condition": "all GZ1385_0 through GZ1385_5 close together before variation/readout",
            "current_evidence": "conditional route exists; at least one active counterexample remains",
            "status": "ZERO_ROUTE_NOT_CLOSED",
            "if_missing": "finite beta_source/beta_test acquisition is required",
            "valid_for_claim": "False",
        },
    ]


def finite_rows() -> list[dict[str, str]]:
    return [
        {
            "row_id": "FCA1385_0_mu_m2",
            "quantity": "mu_m^2(X_B)",
            "definition": "canonical memory mass gap controlling lambda_m=1/sqrt(mu_m^2)",
            "units": "length^-2 or mass^2 in chosen units",
            "required_source": "parent Hessian/kinetic ratio or direct canonical mass-gap theorem",
            "blocks_if_missing": "range;transition length;R10 lambda;profile suppression",
            "current_status": "MISSING_SOURCE_BACKED_CANONICAL_GAP",
            "valid_for_claim": "False",
        },
        {
            "row_id": "FCA1385_1_beta_source",
            "quantity": "beta_source",
            "definition": "canonical source leg beta_s=partial_phi ln m_source^eff or equivalent source-current variation",
            "units": "dimensionless if phi is Planck/canonical-normalized; otherwise declared canonical units",
            "required_source": "source worldtube and matter/source descent map",
            "blocks_if_missing": "R10 alpha;Newton source normalization;source-charge WEP",
            "current_status": "MISSING_SOURCE_BETA",
            "valid_for_claim": "False",
        },
        {
            "row_id": "FCA1385_2_beta_test",
            "quantity": "beta_test",
            "definition": "canonical test leg beta_t=partial_phi ln m_test^eff or equivalent test-body variation",
            "units": "same convention as beta_source",
            "required_source": "test-body matter action in observed coframe plus material/composition map",
            "blocks_if_missing": "R10 alpha;WEP;clock/orbital test response",
            "current_status": "MISSING_TEST_BETA",
            "valid_for_claim": "False",
        },
        {
            "row_id": "FCA1385_3_beta_product",
            "quantity": "beta_source*beta_test",
            "definition": "finite exchange amplitude product; universal Weyl branch gives c_g^2, not c_g",
            "units": "dimensionless product after convention lock",
            "required_source": "beta convention, profile factors, G_N calibration, and no hidden source leg already packed",
            "blocks_if_missing": "all alpha(lambda) and local finite-force scoring",
            "current_status": "PRODUCT_LAW_READY_VALUES_MISSING",
            "valid_for_claim": "False",
        },
        {
            "row_id": "FCA1385_4_Phi_S",
            "quantity": "Phi_S",
            "definition": "canonical boundary/source amplitude feeding exterior profile",
            "units": "canonical field units",
            "required_source": "boundary/source theorem or finite amplitude bound",
            "blocks_if_missing": "Delta_phi, gradient, Q_alg, stress envelope",
            "current_status": "MISSING_CANONICAL_AMPLITUDE",
            "valid_for_claim": "False",
        },
        {
            "row_id": "FCA1385_5_epsilon_Z",
            "quantity": "epsilon_Z",
            "definition": "epsilon_Z=|nabla ln Z_m|/mu_m correction to locally frozen canonicalization",
            "units": "dimensionless",
            "required_source": "X_B local variation theorem or bound",
            "blocks_if_missing": "clean plateau/canonical branch beyond frozen-X_B approximation",
            "current_status": "MISSING_XB_GRADIENT_BOUND",
            "valid_for_claim": "False",
        },
        {
            "row_id": "FCA1385_6_tail_envelope",
            "quantity": "epsilon_tail",
            "definition": "sum of hidden frame, readout, boundary, projector, source-normalization and non-EH tails with no-cancellation policy",
            "units": "arena-dependent residual units",
            "required_source": "tail component bounds or theorem-zero clauses",
            "blocks_if_missing": "R10/PPN/WEP/clock/orbital pass",
            "current_status": "MISSING_TAIL_ENVELOPE",
            "valid_for_claim": "False",
        },
    ]


def arena_rows() -> list[dict[str, str]]:
    return [
        {
            "arena_id": "ARG1385_0_R10",
            "arena": "short-range R10 alpha(lambda)",
            "minimum_inputs": "mu_m^2; beta_source; beta_test; beta convention; profile/tail envelope; source-backed bound curve",
            "refusal": "no alpha(lambda) row if any beta leg or range is missing; no linear c_g shortcut",
            "status": "BLOCKED",
            "claim_allowed": "False",
        },
        {
            "arena_id": "ARG1385_1_PPN",
            "arena": "PPN/local GR residual vector",
            "minimum_inputs": "canonical coupling projection into gamma-1,beta-1,alpha1,alpha2,alpha3,xi plus stress/source-normalization tails",
            "refusal": "universal coupling alone is not a PPN pass; finite residual vector must score",
            "status": "BLOCKED",
            "claim_allowed": "False",
        },
        {
            "arena_id": "ARG1385_2_WEP",
            "arena": "WEP/source charge",
            "minimum_inputs": "composition/material beta_A matrix, tau_WEP projection, source worldtube, same-frame observed coframe",
            "refusal": "direct coframe WEP or eta formula does not prove source-charge WEP",
            "status": "BLOCKED",
            "claim_allowed": "False",
        },
        {
            "arena_id": "ARG1385_3_clocks",
            "arena": "clocks/constants",
            "minimum_inputs": "phi-dependence of alpha_EM, masses, clock standards, or theorem-zero constant superselection",
            "refusal": "constant-sector silence must be parent signed, not assumed",
            "status": "BLOCKED",
            "claim_allowed": "False",
        },
        {
            "arena_id": "ARG1385_4_orbital_Newton",
            "arena": "orbital/Newton source normalization",
            "minimum_inputs": "constant universal coupling, calibrated Hilbert source, no species/range/radial/time/frame derivative hair",
            "refusal": "measured GM absorption is allowed only for global constants, not local/range/species residuals",
            "status": "BLOCKED",
            "claim_allowed": "False",
        },
        {
            "arena_id": "ARG1385_5_local_GR",
            "arena": "local GR reduction",
            "minimum_inputs": "g_c=0 theorem or finite residual vector below all local bounds, plus memory stress/source/boundary tails",
            "refusal": "canonical contract alone is not a GR limit",
            "status": "BLOCKED",
            "claim_allowed": "False",
        },
    ]


def runner_rows() -> list[dict[str, str]]:
    return [
        {
            "feed_id": "RUF1385_0_canonical_gap",
            "runner_change": "replace Z_m/F2 numeric scoring with mu_m^2(X_B)",
            "formula": "lambda_m=ell_tr=1/sqrt(mu_m^2)",
            "status": "SYMBOLIC_READY_VALUE_MISSING",
            "claim_allowed": "False",
        },
        {
            "feed_id": "RUF1385_1_zero_route",
            "runner_change": "add theorem-zero branch for g_c=0 only if all matter descent clauses close",
            "formula": "Dq[v_phi]=0 and S_matter descends => delta_phi S_matter=0",
            "status": "CONDITIONAL_ROUTE_UNSIGNED",
            "claim_allowed": "False",
        },
        {
            "feed_id": "RUF1385_2_finite_beta",
            "runner_change": "finite exchange uses beta_source*beta_test",
            "formula": "alpha_X(lambda) ~ K(lambda) beta_s beta_t + epsilon_tail",
            "status": "PRODUCT_LAW_READY_VALUES_MISSING",
            "claim_allowed": "False",
        },
        {
            "feed_id": "RUF1385_3_no_cancellation",
            "runner_change": "tail envelope is additive/no-cancellation unless parent identity is derived",
            "formula": "|residual_total| <= scored only from source-backed component bounds; unknown tails block",
            "status": "NO_CANCELLATION_POLICY_ACTIVE",
            "claim_allowed": "False",
        },
        {
            "feed_id": "RUF1385_4_verdict",
            "runner_change": "1385 provides canonical contract, not scoreable predictions",
            "formula": "mu_m^2 plus zero-coupling theorem or finite beta pair",
            "status": "NONCLAIM_RUNNER_CONTRACT_READY",
            "claim_allowed": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE1385_0_sources",
            "gate": "all cited sources exist and anchors are present",
            "status": "PASS",
            "reason": "source register validates against local corpus",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1385_1_contract",
            "gate": "canonical gap/coupling parent contract exists",
            "status": "PASS_CONTRACT_READY",
            "reason": "CGC1385 rows define mu_m^2, J_c/g_c, zero route, finite beta route and no-single-coupling policy",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1385_2_zero_route",
            "gate": "g_c=0 theorem is parent signed",
            "status": "BLOCKED_ZERO_ROUTE_UNSIGNED",
            "reason": "GZ1385_6 records active unsigned clauses/counterexamples",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1385_3_finite_route",
            "gate": "finite beta_source/beta_test scoring is source-backed",
            "status": "BLOCKED_FINITE_ROWS_MISSING",
            "reason": "mu_m^2, beta_s, beta_t, Phi_S, epsilon_Z and tail envelope are missing",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1385_4_arenas",
            "gate": "R10/PPN/WEP/clock/orbital projections can score",
            "status": "BLOCKED_ARENA_PROJECTIONS_MISSING",
            "reason": "arena gates all remain blocked with explicit missing inputs",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1385_5_local_claim",
            "gate": "local GR / Newton / PPN / R10 pass can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1385 is a parent contract and fork selection, not a derived local GR limit",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1385_0_best_route",
            "decision": "try g_c=0 theorem first",
            "because": "a parent-signed matter descent/no-shadow/no-action-weight proof gives the cleanest GR reduction and avoids fitted finite fifth-force tuning",
            "next_action": "attack the quotient-kernel matter descent clauses as one package",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1385_1_fallback",
            "decision": "finite coupling fallback is beta_source times beta_test",
            "because": "two-body exchange and 1036 forbid a single naked coupling score; universal c_g enters as c_g^2 unless a source leg is explicitly packed",
            "next_action": "if zero theorem fails, create a beta_s/beta_t acquisition runner",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1385_2_project_status",
            "decision": "coupling is the live local-GR bottleneck",
            "because": "range without coupling is invisible; coupling without range cannot be scored; both must be parent-owned or bounded",
            "next_action": "1386 should try to close the matter-descent zero theorem before any numeric local tests",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1385_0_1386",
            "next_doc": "1386-Y5-R10-RAB-canonical-coupling-zero-theorem-or-beta-acquisition-runner.md",
            "next_script": "scripts/Y5_R10_RAB_canonical_coupling_zero_theorem_or_beta_acquisition_runner.py",
            "task": "try to prove the canonical g_c=0 theorem by closing the matter descent/no-shadow/no-action-weight clauses as one parent package; if it fails, build finite beta_source/beta_test acquisition rows",
            "success_condition": "either g_c=0 has a parent-signed theorem scaffold, or beta_source/beta_test nonclaim acquisition rows exist with arena routing and local claims blocked",
            "do_not_claim": "local GR;Newton limit;PPN pass;R10 pass;WEP pass;q_loc=0;numeric alpha(lambda);GitHub-ready result",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def validation_rows(
    sources: list[dict[str, str]],
    contracts: list[dict[str, str]],
    zero: list[dict[str, str]],
    finite: list[dict[str, str]],
    arenas: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    all_sources_ok = all(row["exists"] == "True" and row["anchor_found"] == "True" for row in sources)
    contract_ready = any(row["contract_id"] == "CGC1385_7_verdict" and row["derivation_status"] == "CONTRACT_READY_ZERO_ROUTE_UNSIGNED" for row in contracts)
    zero_blocked = any(row["zero_id"] == "GZ1385_6_verdict" and row["status"] == "ZERO_ROUTE_NOT_CLOSED" for row in zero)
    finite_nonclaim = all(row["valid_for_claim"] == "False" and row["current_status"].startswith(("MISSING", "PRODUCT")) for row in finite)
    arenas_blocked = all(row["status"] == "BLOCKED" and row["claim_allowed"] == "False" for row in arenas)
    local_blocked = any(row["gate_id"] == "GATE1385_5_local_claim" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    outputs = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        CONTRACT_PATH,
        ZERO_ROUTE_PATH,
        FINITE_ROWS_PATH,
        ARENA_GATES_PATH,
        RUNNER_FEED_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
        Path("scripts/Y5_R10_RAB_canonical_mass_gap_and_coupling_parent_contract.py"),
    ]
    outside_formalization = all("formalization-workbench" not in str(ROOT / path) for path in outputs)
    overall = all([all_sources_ok, contract_ready, zero_blocked, finite_nonclaim, arenas_blocked, local_blocked, outside_formalization])
    return [
        {
            "validation_id": "VAL1385_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if all_sources_ok else "FAIL",
            "details": "; ".join(f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources),
        },
        {
            "validation_id": "VAL1385_1_contract",
            "check": "canonical gap/coupling contract is written",
            "status": "PASS" if contract_ready else "FAIL",
            "details": "CGC1385_7 records contract-ready but zero-route-unsigned verdict.",
        },
        {
            "validation_id": "VAL1385_2_zero_refusal",
            "check": "g_c=0 is not falsely claimed",
            "status": "PASS" if zero_blocked else "FAIL",
            "details": "GZ1385_6 keeps ZERO_ROUTE_NOT_CLOSED.",
        },
        {
            "validation_id": "VAL1385_3_finite_rows",
            "check": "finite coupling rows remain nonclaim",
            "status": "PASS" if finite_nonclaim else "FAIL",
            "details": "All FCA1385 rows are missing/product-law placeholders with valid_for_claim=False.",
        },
        {
            "validation_id": "VAL1385_4_arena_refusal",
            "check": "local arenas remain blocked",
            "status": "PASS" if arenas_blocked and local_blocked else "FAIL",
            "details": "ARG1385 rows and GATE1385_5 block local/R10/PPN/WEP claims.",
        },
        {
            "validation_id": "VAL1385_5_scope",
            "check": "generated outputs stay inside post-checkpoint-work and outside formalization-workbench",
            "status": "PASS" if outside_formalization else "FAIL",
            "details": f"ROOT={ROOT}; output_count={len(outputs)}; formalization_touched=False",
        },
        {
            "validation_id": "VAL1385_6_overall",
            "check": "overall 1385 validation",
            "status": "PASS" if overall else "FAIL",
            "details": "1385 writes the canonical mass-gap/coupling parent contract and selects zero theorem before finite beta fallback.",
        },
    ]


def write_doc(
    sources: list[dict[str, str]],
    contracts: list[dict[str, str]],
    zero: list[dict[str, str]],
    finite: list[dict[str, str]],
    arenas: list[dict[str, str]],
    runner: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    generated = datetime.now(timezone.utc).isoformat()
    body = f"""# 1385 - Y5 R10 RAB Canonical Mass-Gap And Coupling Parent Contract

**Generated:** {generated}

**Current verdict:** the local branch now has the right physical fork. The canonical range is controlled by `mu_m^2(X_B)`, but local tests only see it through coupling. The clean route is a parent-signed `g_c=0` theorem from matter descent; the honest fallback is finite `beta_source * beta_test` acquisition.

**Discipline move:** no single naked coupling can score a local test. Universal finite coupling enters both source and test legs unless a source leg is explicitly packed and sourced. If the zero theorem does not close, `R10`, `PPN`, `WEP`, clocks, orbital, and Newton/source-normalization rows all need finite acquisition.

**Claim ceiling:** {CLAIM_CEILING}

## Source Register

{md_table(sources)}

## Canonical Gap-Coupling Contract

{md_table(contracts)}

## `g_c=0` Zero-Route Audit

{md_table(zero)}

## Finite Channel Acquisition Rows

{md_table(finite)}

## Arena Projection Refusal Gates

{md_table(arenas)}

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
    contracts = contract_rows()
    zero = zero_route_rows()
    finite = finite_rows()
    arenas = arena_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, contracts, zero, finite, arenas, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(CONTRACT_PATH, contracts)
    write_csv(ZERO_ROUTE_PATH, zero)
    write_csv(FINITE_ROWS_PATH, finite)
    write_csv(ARENA_GATES_PATH, arenas)
    write_csv(RUNNER_FEED_PATH, runner)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, contracts, zero, finite, arenas, runner, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1385 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()
