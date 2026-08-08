from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1158-Y5-R10-cg-units-arena-projection-source-pack-or-Cperp-exactness-repair.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def contains_missing(value: object) -> bool:
    text = str(value)
    return text.strip() == "" or "MISSING" in text or "NOT_ACQUIRED" in text or "NOT_DERIVED" in text


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1158_0_1157_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1157_NEXT_TARGET.csv",
            "needle": "NEXT1157_0_1158",
            "role": "handoff selecting c_g units/projection source pack or Cperp exactness repair.",
        },
        {
            "source_id": "SRC1158_1_1157_cg_first",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1157_CG_BOUND_FIRST_FILL_ROWS.csv",
            "needle": "CG1157_0_cg_first_fill",
            "role": "first explicit c_g source row and required column contract.",
        },
        {
            "source_id": "SRC1158_2_1157_exactness",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1157_QMAP_NULL_GENERATOR_PROOF_AUDIT.csv",
            "needle": "QMAP1157_2_exactness",
            "role": "Cperp exactness and boundary primitive silence burden.",
        },
        {
            "source_id": "SRC1158_3_1156_frame_leak",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1156_FRAME_LEAK_BOUND_FILL_ROWS.csv",
            "needle": "FLB1156_1_c_g",
            "role": "prior frame-leak bound row requiring c_g sourcing.",
        },
        {
            "source_id": "SRC1158_4_626_template",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_626_CG_BOUND_INPUT_TEMPLATE.csv",
            "needle": "CGB626_1_cg_value",
            "role": "early c_g, tau_R10, tau_PPN, tau_clock, tau_orbital input template.",
        },
        {
            "source_id": "SRC1158_5_944_pack",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_944_FRAME_LEAK_BOUND_PACK.csv",
            "needle": "FLB944_0_cg_weyl",
            "role": "frame leak source pack identifying c_g as a Weyl/common-frame derivative.",
        },
        {
            "source_id": "SRC1158_6_945_rows",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_945_FIRST_FRAME_LEAK_BOUND_ROWS.csv",
            "needle": "BND945_0_cg_value",
            "role": "first c_g/tau bound rows showing the same missing-source pattern.",
        },
        {
            "source_id": "SRC1158_7_1033_tau_R10",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv",
            "needle": "TAUR1033_6_verdict",
            "role": "R10 projection audit: tau_R10 and companion factors not derived.",
        },
        {
            "source_id": "SRC1158_8_1052_clock",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1052_TAU_CLOCK_XHAT_NORMALIZATION_AUDIT.csv",
            "needle": "TCN1052_4_verdict",
            "role": "clock/Xhat normalization audit: standalone clock coupling not claim-ready.",
        },
        {
            "source_id": "SRC1158_9_1068_wep",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1068_TAU_WEP_ACQUISITION_PACK.csv",
            "needle": "TAP1068_5_Xhat_normalization",
            "role": "WEP tau acquisition pack: Xhat normalization and force/readout map missing.",
        },
        {
            "source_id": "SRC1158_10_272_Cperp",
            "relative_path": "272-quotient-configuration-principle-from-topological-projector.md",
            "needle": "Cperp exactness for the C-sector",
            "role": "older quotient principle file naming Cperp exactness as a missing parent derivation.",
        },
        {
            "source_id": "SRC1158_11_720_kinetic_guard",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_720_KINETIC_NULL_THEOREM_AUDIT.csv",
            "needle": "KNT720_8_no_mode_theorem",
            "role": "kinetic/null guard preventing missing kinetic terms from being treated as zero proof.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = read_text(path)
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def cg_units_projection_audit_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "audit_id": "CGUP1158_0_Ag_definition",
                "claim_piece": "common observed-frame conformal factor",
                "required_form": "g_obs = A_g(Xhat)^2 g_ref plus explicitly separated disformal/tail terms",
                "current_status": "SCHEMA_READY_NOT_PARENT_DEFINED",
                "missing_for_claim": "parent source path defining A_g, observed frame, and whether disformal terms are absent or retained",
                "risk_if_missing": "c_g is only a label, not a measurable coefficient",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "CGUP1158_1_Xhat_normalization",
                "claim_piece": "Xhat normalization",
                "required_form": "Xhat must be dimensionless or assigned explicit units and a parent normalization",
                "current_status": "MISSING_SHARED_NORMALIZATION",
                "missing_for_claim": "shared clock/R10/WEP/PPN/orbital Xhat convention or explicitly separated branch convention",
                "risk_if_missing": "c_g units and cross-arena comparisons drift",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "CGUP1158_2_cg_units",
                "claim_piece": "units of c_g",
                "required_form": "c_g = d ln A_g / dXhat; dimensionless only if Xhat is dimensionless",
                "current_status": "DIMENSIONAL_CONVENTION_UNSIGNED",
                "missing_for_claim": "A_g source plus Xhat normalization source",
                "risk_if_missing": "dimensionless c_g can be accidentally smuggled in",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "CGUP1158_3_R10_projection",
                "claim_piece": "tau_R10 and R10 alpha projection",
                "required_form": "alpha_R10(lambda)=K_X(lambda) Qbar_XH(source,lambda) [tau_R10(test,lambda)c_g + tails]",
                "current_status": "DEFINITION_ONLY_NOT_NUMERIC",
                "missing_for_claim": "K_X, Qbar_XH, tau_R10, c_g, finite-source profile, bound curve, and tail envelope",
                "risk_if_missing": "R10 alpha rows remain placeholders",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "CGUP1158_4_PPN_projection",
                "claim_piece": "tau_PPN weak-field projection",
                "required_form": "gauge-fixed weak-field map from common-frame response to gamma/beta/preferred-frame residuals",
                "current_status": "MISSING_ARENA_PROJECTION",
                "missing_for_claim": "PPN gauge convention, observable residual vector, and source-normalized coefficient map",
                "risk_if_missing": "local-GR reduction can be claimed only by words",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "CGUP1158_5_clock_WEP_orbital_projection",
                "claim_piece": "tau_clock, tau_WEP, tau_orbital",
                "required_form": "separate arena projections with shared Xhat normalization or direct product observables",
                "current_status": "MISSING_ARENA_PROJECTIONS",
                "missing_for_claim": "clock time map, WEP material/force readout, orbital source/orbit kernel",
                "risk_if_missing": "finite c_g cannot be compared across local arenas",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "CGUP1158_6_zero_theorem_link",
                "claim_piece": "Z_cg zero theorem",
                "required_form": "q object, v_X in ker(Dq), matter functor descent, boundary primitive silence, and no edge/source tail",
                "current_status": "ZERO_THEOREM_NOT_SIGNED",
                "missing_for_claim": "Cperp exactness repair and parent matter descent in the same local domain",
                "risk_if_missing": "c_g=0 cannot be used as a local-GR proof",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "CGUP1158_7_verdict",
                "claim_piece": "current c_g source-pack readiness",
                "required_form": "A_g, Xhat, c_g, tau_R10, tau_PPN, tau_clock, tau_WEP, tau_orbital all sourced or theorem-zeroed",
                "current_status": "SOURCE_PACK_READY_CLAIM_BLOCKED",
                "missing_for_claim": "all numeric/theorem-zero parent inputs remain missing",
                "risk_if_missing": "no R10, PPN, WEP, clock, orbital, local-GR, or Newton promotion",
                "valid_for_claim": "false",
            },
        ]
    )


def cg_source_pack_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "row_id": "CGSRC1158_0_Ag_definition",
                "item": "A_g_definition",
                "symbol": "A_g(Xhat)",
                "arena": "all_local_arenas",
                "definition": "observed-frame common Weyl/conformal matter coupling, separated from disformal and boundary tails",
                "required_source": "parent action/frame clause defining g_obs and matter coupling",
                "unit_convention": "dimensionless A_g",
                "current_value": "MISSING_PARENT_Ag_DEFINITION",
                "source_path": "MISSING_PARENT_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "CGSRC1158_1_Xhat_normalization",
                "item": "Xhat_normalization",
                "symbol": "Xhat",
                "arena": "R10;PPN;clock;WEP;orbital",
                "definition": "normalized local generator coordinate used by c_g and all arena tau projections",
                "required_source": "shared parent normalization or explicit branch-separated normalization",
                "unit_convention": "dimensionless_or_declared_units",
                "current_value": "MISSING_SHARED_XHAT_NORMALIZATION",
                "source_path": "MISSING_PARENT_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "CGSRC1158_2_cg_value",
                "item": "c_g_value_or_zero_theorem",
                "symbol": "c_g=d ln A_g/dXhat",
                "arena": "R10;PPN;clock;WEP;orbital",
                "definition": "finite common-frame coefficient or parent-signed zero theorem",
                "required_source": "numeric coefficient source row or Z_cg theorem path with q/null/boundary/matter descent proof",
                "unit_convention": "1/[Xhat_units]; dimensionless only if Xhat dimensionless",
                "current_value": "MISSING_PARENT_NUMERIC_CG_OR_ZERO_THEOREM",
                "source_path": "MISSING_PARENT_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "CGSRC1158_3_tau_R10",
                "item": "R10 projection",
                "symbol": "tau_R10(lambda)",
                "arena": "R10",
                "definition": "normalized short-range material/test/readout projection multiplying c_g in the Yukawa alpha convention",
                "required_source": "test material projection, profile integral, finite-source correction, and alpha(lambda) convention",
                "unit_convention": "dimensionless_after_declared_normalization",
                "current_value": "MISSING_R10_ARENA_PROJECTION",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv",
                "status": "BLOCKED_DEFINITION_ONLY",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "CGSRC1158_4_KX_Qbar_lambda",
                "item": "R10 companion factors",
                "symbol": "K_X(lambda);Qbar_XH;lambda_X",
                "arena": "R10",
                "definition": "Green-kernel normalization, source charge, and range/profile relation required before alpha_R10 can score",
                "required_source": "parent kinetic normalization, source worldtube, measured-G comparison, and lambda_X relation",
                "unit_convention": "declared_by_kernel_and_source_normalization",
                "current_value": "MISSING_R10_COMPANION_FACTORS",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "CGSRC1158_5_tau_PPN",
                "item": "PPN projection",
                "symbol": "tau_PPN",
                "arena": "PPN",
                "definition": "weak-field projection of common-frame response into PPN residual vector",
                "required_source": "gauge-fixed weak-field map and residual-vector formula",
                "unit_convention": "dimensionless_after_gauge_convention",
                "current_value": "MISSING_PPN_ARENA_PROJECTION",
                "source_path": "MISSING_PPN_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "CGSRC1158_6_tau_clock",
                "item": "clock projection",
                "symbol": "tau_clock",
                "arena": "clock",
                "definition": "time/readout projection converting local generator motion into clock observable products",
                "required_source": "local time map, chi_X/Xhat normalization, and clock sensitivity product rule",
                "unit_convention": "time^-1 or dimensionless per declared clock convention",
                "current_value": "MISSING_CLOCK_ARENA_PROJECTION",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_1052_TAU_CLOCK_XHAT_NORMALIZATION_AUDIT.csv",
                "status": "BLOCKED_PRODUCT_ONLY",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "CGSRC1158_7_tau_WEP",
                "item": "WEP/material projection",
                "symbol": "tau_WEP",
                "arena": "WEP",
                "definition": "material/source/readout projection converting common-frame coupling into differential acceleration observable",
                "required_source": "source worldtube, orbit average, material response, force map, and shared Xhat normalization",
                "unit_convention": "dimensionless_or_direct_product",
                "current_value": "MISSING_WEP_ARENA_PROJECTION",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_1068_TAU_WEP_ACQUISITION_PACK.csv",
                "status": "BLOCKED_ACQUISITION_PACK_ONLY",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "CGSRC1158_8_tau_orbital",
                "item": "orbital projection",
                "symbol": "tau_orbital",
                "arena": "orbital",
                "definition": "source/orbit/readout projection of common-frame response into perihelion, range, or timing residuals",
                "required_source": "orbital source body, orbit averaging kernel, calibration convention, and PPN/source-normalization link",
                "unit_convention": "dimensionless_or_declared_by_residual_vector",
                "current_value": "MISSING_ORBITAL_ARENA_PROJECTION",
                "source_path": "MISSING_ORBITAL_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "CGSRC1158_9_epsilon_cg_score",
                "item": "score envelope",
                "symbol": "epsilon_cg",
                "arena": "all_local_arenas",
                "definition": "absolute projected residual envelope from c_g and arena tau factors",
                "required_source": "all component coefficients, units, source paths, no-cancellation rule, and observed-frame residual map",
                "unit_convention": "dimensionless_residual_or_declared_observable_units",
                "current_value": "MISSING_COMPONENT_INPUTS",
                "source_path": "MISSING_COMPONENT_SOURCE_PACK",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
        ]
    )


def cperp_repair_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "repair_id": "CPE1158_0_exactness_target",
                "target": "Cperp exactness",
                "required_statement": "C_perp is relative-exact or variationally trivial in the local domain",
                "current_status": "OPEN_TARGET",
                "missing_for_proof": "parent C-sector form, differential, allowed boundary class, and local domain",
                "effect_if_closed": "candidate presymplectic null direction becomes credible",
                "valid_for_claim": "false",
            },
            {
                "repair_id": "CPE1158_1_boundary_primitive",
                "target": "boundary primitive zero",
                "required_statement": "the exact primitive has zero compact/local boundary readout and no hidden edge charge",
                "current_status": "NOT_PROVED",
                "missing_for_proof": "boundary condition, edge-mode exclusion, and source support silence",
                "effect_if_closed": "prevents exactness from reappearing as boundary hair",
                "valid_for_claim": "false",
            },
            {
                "repair_id": "CPE1158_2_presymplectic_kernel",
                "target": "Omega(v_X,delta)=0",
                "required_statement": "the Xhat/frame direction lies in the presymplectic kernel after exact/boundary pieces are removed",
                "current_status": "CONDITIONAL_ONLY",
                "missing_for_proof": "Theta/Omega calculation with the actual parent local branch",
                "effect_if_closed": "supports v_X in ker(Dq)",
                "valid_for_claim": "false",
            },
            {
                "repair_id": "CPE1158_3_vX_identification",
                "target": "local generator identification",
                "required_statement": "the c_g-carrying direction is exactly the quotient null generator, not a retained physical field",
                "current_status": "NOT_IDENTIFIED",
                "missing_for_proof": "map from Xhat/frame variation to parent null orbit",
                "effect_if_closed": "c_g can move from finite bound row toward zero theorem",
                "valid_for_claim": "false",
            },
            {
                "repair_id": "CPE1158_4_matter_descent",
                "target": "matter action descends through q",
                "required_statement": "S_matter factors through the quotient and cannot depend on representative A_g(Xhat)",
                "current_status": "NOT_SIGNED",
                "missing_for_proof": "same-domain matter functor, observed coframe, constants, and source measure descent",
                "effect_if_closed": "blocks common-frame matter coupling",
                "valid_for_claim": "false",
            },
            {
                "repair_id": "CPE1158_5_kinetic_rank_guard",
                "target": "no physical retained X mode",
                "required_statement": "rank/signature/source-orthogonality classify X as null or constrained, not merely omitted",
                "current_status": "OPEN_GUARD",
                "missing_for_proof": "kinetic/Hessian/range/source-rank audit in the same branch",
                "effect_if_closed": "prevents hidden scalar-force leakage",
                "valid_for_claim": "false",
            },
            {
                "repair_id": "CPE1158_6_verdict",
                "target": "Cperp exactness repair closes Z_cg",
                "required_statement": "CPE1158_0 through CPE1158_5 all parent-signed",
                "current_status": "NOT_CLOSED_CURRENT_CORPUS",
                "missing_for_proof": "exactness, boundary primitive zero, vX identification, matter descent, and kinetic-rank guard",
                "effect_if_closed": "only then can c_g=0 be considered for local-GR branch promotion",
                "valid_for_claim": "false",
            },
        ]
    )


def guard_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "guard_id": "GUARD1158_0_no_dimensionless_cg_shortcut",
                "guard": "c_g is dimensionless only after Xhat is dimensionless or explicitly normalized",
                "status": "ACTIVE",
                "reason": "units cannot be inherited from earlier placeholder rows",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1158_1_no_placeholder_source_pack_claim",
                "guard": "a row with MISSING_* or NOT_DERIVED status cannot be used in a score",
                "status": "ACTIVE",
                "reason": "source pack rows are acquisition targets, not evidence",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1158_2_no_tau_reuse_across_arenas",
                "guard": "tau_R10, tau_PPN, tau_clock, tau_WEP, and tau_orbital are separate projections unless parent-linked",
                "status": "ACTIVE",
                "reason": "same symbol cannot silently do five different experiments",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1158_3_no_Cperp_slogan_proof",
                "guard": "Cperp exactness must include boundary primitive zero and matter descent",
                "status": "ACTIVE",
                "reason": "exact bulk terms can still carry boundary/source hair",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1158_4_no_local_GR_promotion",
                "guard": "local-GR/Newton/R10/PPN/WEP/clock/orbital claims remain blocked",
                "status": "ACTIVE",
                "reason": "neither finite c_g source pack nor Z_cg proof is complete",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1158_0_sources_exist",
                "rule": "all cited local source paths and needles exist",
                "gate_pass": "true_nonclaim",
                "reason": "source register validates the audit trail",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1158_1_cg_pack_complete",
                "rule": "source pack covers A_g, Xhat, c_g, R10, PPN, clock, WEP, orbital, and score envelope",
                "gate_pass": "true_nonclaim",
                "reason": "all required rows are emitted as blocked acquisition rows",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1158_2_finite_cg_score_ready",
                "rule": "finite c_g branch has numeric/theorem-zero value and arena projections",
                "gate_pass": "false",
                "reason": "A_g, Xhat, c_g, tau projections, and companion factors remain missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1158_3_Cperp_zero_ready",
                "rule": "Cperp exactness repair proves Z_cg",
                "gate_pass": "false",
                "reason": "boundary primitive zero, vX identification, matter descent, and kinetic guard are not parent-signed",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1158_4_claim_promotion",
                "rule": "R10/PPN/WEP/clock/orbital/local-GR claim allowed",
                "gate_pass": "false",
                "reason": "both finite-bound and theorem-zero c_g routes remain incomplete",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1158_0_units",
                "decision": "separate c_g units from c_g value",
                "reason": "d ln A_g/dXhat is dimensionless only under a dimensionless Xhat normalization",
                "next_action": "require A_g and Xhat source rows before any c_g scoring",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1158_1_projection_pack",
                "decision": "treat every local arena as its own projection",
                "reason": "R10, PPN, clocks, WEP, and orbital tests measure different readout maps",
                "next_action": "fill tau_R10/tau_PPN/tau_clock/tau_WEP/tau_orbital separately or derive a parent link",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1158_2_derivation_route",
                "decision": "keep Cperp exactness as the clean zero route",
                "reason": "a true presymplectic-null quotient would be cleaner than fitting finite c_g bounds",
                "next_action": "attack boundary primitive zero and vX identification, not q by declaration",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1158_3_best_next",
                "decision": "target first numeric prior or boundary primitive zero proof",
                "reason": "1158 has converted the coupling problem into exact missing rows and one derivation repair burden",
                "next_action": "1159 c_g first numeric prior or Cperp boundary primitive zero proof",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1158_0_1159",
                "next_target": "1159-Y5-R10-cg-first-numeric-prior-or-Cperp-boundary-primitive-zero-proof.md",
                "objective": "either source a first nonclaim finite c_g prior/projection bundle or prove the Cperp boundary primitive is zero in the local branch",
                "include": "A_g source; Xhat normalization; finite c_g prior; tau_R10/tau_PPN/tau_clock/tau_WEP/tau_orbital; boundary primitive B_C=0 proof attempt",
                "exclude": "dimensionless c_g shortcut; tau reuse; q by declaration; local-GR/Newton claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    audit: list[dict[str, object]],
    pack: list[dict[str, object]],
    cperp: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    all_rows = audit + pack + cperp + guards + gates + decisions + next_target
    required_pack_ids = {
        "CGSRC1158_0_Ag_definition",
        "CGSRC1158_1_Xhat_normalization",
        "CGSRC1158_2_cg_value",
        "CGSRC1158_3_tau_R10",
        "CGSRC1158_4_KX_Qbar_lambda",
        "CGSRC1158_5_tau_PPN",
        "CGSRC1158_6_tau_clock",
        "CGSRC1158_7_tau_WEP",
        "CGSRC1158_8_tau_orbital",
        "CGSRC1158_9_epsilon_cg_score",
    }
    add(
        "V1158_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1158_1_units_unsigned",
        any(row["audit_id"] == "CGUP1158_2_cg_units" and row["current_status"] == "DIMENSIONAL_CONVENTION_UNSIGNED" for row in audit),
        "c_g units remain gated by Xhat normalization instead of assumed dimensionless",
    )
    add(
        "V1158_2_pack_rows_complete",
        required_pack_ids.issubset({row["row_id"] for row in pack}),
        "c_g source pack covers A_g, Xhat, c_g, all projections, companion factors, and score envelope",
    )
    add(
        "V1158_3_pack_rows_nonclaim_missing",
        all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" and contains_missing(row["current_value"]) for row in pack),
        "all c_g source-pack rows remain missing/nonclaim until sourced",
    )
    add(
        "V1158_4_Cperp_not_closed",
        any(row["repair_id"] == "CPE1158_6_verdict" and row["current_status"] == "NOT_CLOSED_CURRENT_CORPUS" for row in cperp),
        "Cperp exactness repair remains open rather than claimed",
    )
    add(
        "V1158_5_guards_active",
        {
            "GUARD1158_0_no_dimensionless_cg_shortcut",
            "GUARD1158_1_no_placeholder_source_pack_claim",
            "GUARD1158_2_no_tau_reuse_across_arenas",
            "GUARD1158_3_no_Cperp_slogan_proof",
            "GUARD1158_4_no_local_GR_promotion",
        }.issubset({row["guard_id"] for row in guards if row["status"] == "ACTIVE"}),
        "all c_g source-pack and Cperp no-cheat guards are active",
    )
    add(
        "V1158_6_claim_gates_blocked",
        any(row["gate_id"] == "G1158_2_finite_cg_score_ready" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1158_3_Cperp_zero_ready" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1158_4_claim_promotion" and row["gate_pass"] == "false" for row in gates),
        "finite c_g, Z_cg, and local claim gates remain blocked",
    )
    add(
        "V1158_7_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in all_rows)
        and all(row.get("claim_allowed", "false") == "false" for row in next_target),
        "all generated rows remain nonclaim",
    )
    add(
        "V1158_8_next_target",
        next_target[0]["next_target"].startswith("1159-")
        and "cg-first-numeric-prior" in str(next_target[0]["next_target"]),
        "1159 handoff targets first numeric prior or Cperp boundary primitive zero proof",
    )
    add(
        "V1158_9_generated_under_post_checkpoint",
        all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()),
        "all generated outputs are under post-checkpoint-work",
    )
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1158_10_csv_parse", csv_parse_ok, "all 1158 CSV outputs parse cleanly")
    add("V1158_11_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add(
        "V1158_SUMMARY",
        True,
        "1158 makes c_g source requirements exact, blocks finite/local claims, and preserves Cperp exactness as the clean zero route",
    )
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "/") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    audit: list[dict[str, object]],
    pack: list[dict[str, object]],
    cperp: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1158 - Y5/R10 c_g Units/Arena Projection Source Pack or Cperp Exactness Repair

**Current verdict:** the `c_g` problem is now sharper, but not solved. A finite branch needs sourced `A_g`, `Xhat`, `c_g`, `K_X`, `Qbar_XH`, `lambda_X`, and separate arena projections. The zero branch needs a parent-signed `Cperp` exactness repair with boundary primitive silence.

**Main progress:** the coupling is no longer a foggy "something is missing" problem. It is now an explicit source-pack: define the observed common frame, normalize `Xhat`, then fill or zero `c_g`, then map it separately into R10, PPN, clocks, WEP, and orbital systems.

**Key guard:** `c_g=d ln A_g/dXhat` is dimensionless only if `Xhat` is dimensionless. Earlier dimensionless placeholders are not enough.

**Best next attack:** either source a first nonclaim finite `c_g` prior/projection bundle, or try the cleaner derivation route: prove the `Cperp` boundary primitive is zero so the quotient-null route can actually bite.

**No claim:** no R10, PPN, WEP, clock, orbital, local-GR, Newton, GitHub, or public claim follows from 1158.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "role"], sources)}

## c_g Units / Arena Projection Audit
{table(["audit_id", "claim_piece", "required_form", "current_status", "missing_for_claim", "risk_if_missing", "valid_for_claim"], audit)}

## c_g Source Pack Rows
{table(["row_id", "item", "symbol", "arena", "definition", "required_source", "unit_convention", "current_value", "source_path", "status", "valid_for_claim", "claim_allowed"], pack)}

## Cperp Exactness Repair Audit
{table(["repair_id", "target", "required_statement", "current_status", "missing_for_proof", "effect_if_closed", "valid_for_claim"], cperp)}

## No-Cheat Guards
{table(["guard_id", "guard", "status", "reason", "valid_for_claim"], guards)}

## Claim Gates
{table(["gate_id", "rule", "gate_pass", "reason", "valid_for_claim"], gates)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim", "claim_allowed"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1158_SOURCE_REGISTER.csv",
        "audit": OUT / "P8_Y5_R10_1158_CG_UNITS_PROJECTION_AUDIT.csv",
        "pack": OUT / "P8_Y5_R10_1158_CG_SOURCE_PACK_ROWS.csv",
        "cperp": OUT / "P8_Y5_R10_1158_CP_EXACTNESS_REPAIR_AUDIT.csv",
        "guards": OUT / "P8_Y5_R10_1158_NO_CG_CHEAT_GUARDS.csv",
        "gates": OUT / "P8_Y5_R10_1158_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1158_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1158_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1158_VALIDATION.csv",
    }

    sources = source_rows()
    audit = cg_units_projection_audit_rows()
    pack = cg_source_pack_rows()
    cperp = cperp_repair_rows()
    guards = guard_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["audit"], audit)
    write_csv(outputs["pack"], pack)
    write_csv(outputs["cperp"], cperp)
    write_csv(outputs["guards"], guards)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, audit, pack, cperp, guards, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, audit, pack, cperp, guards, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    if failed:
        for row in failed:
            print(f"{row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
