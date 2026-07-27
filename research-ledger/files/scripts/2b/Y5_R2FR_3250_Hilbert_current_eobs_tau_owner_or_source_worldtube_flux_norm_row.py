from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3250"
DOC = ROOT / "3250-Y5-R2FR-Hilbert-current-eobs-tau-owner-or-source-worldtube-flux-norm-row-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3250_SOURCE_REGISTER.csv",
    "package": OUT / "P8_Y5_R2FR_3250_SAME_FRAME_PACKAGE_THEOREM.csv",
    "residual": OUT / "P8_Y5_R2FR_3250_DJH_RESIDUAL_VECTOR.csv",
    "em_projection": OUT / "P8_Y5_R2FR_3250_EM_STRESS_PROJECTION_AND_FLUX_NORM_IDENTITY.csv",
    "flux_row": OUT / "P8_Y5_R2FR_3250_SOURCE_WORLDTUBE_FLUX_NORM_ROW.csv",
    "wsource_update": OUT / "P8_Y5_R2FR_3250_WSOURCE_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3250_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3250_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3250_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_R2FR_3250_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        read_csv(path)
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def evidence(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered = [needle.lower() for needle in needles]
    hits: list[str] = []
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_number, line in enumerate(handle, start=1):
            low = line.lower()
            if any(needle in low for needle in lowered):
                clean = " ".join(line.strip().split())
                if clean:
                    hits.append(f"L{line_number}:{clean[:220]}")
            if len(hits) >= limit:
                break
    return " | ".join(hits) if hits else "NO_MATCH"


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC3250_3249_handoff",
            ROOT / "3249-Y5-R2FR-Wsource-JH-tau-eobs-selector-or-source-worldtube-Poynting-bound-row-under-AX1090.md",
            "immediate same-frame package handoff",
            ["W_source", "J_H", "tau", "e_obs", "NEXT3249"],
        ),
        (
            "SRC3250_1044_pullback",
            ROOT / "1044-Y5-R10-matter-pullback-JX-zero-or-qbarXT-bound-row.md",
            "ordinary matter chain-rule pullback theorem",
            ["ordinary-matter chain-rule", "MPD1044_6_source_current_universality", "CG1044"],
        ),
        (
            "SRC3250_1044_derivation_csv",
            OUT / "P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv",
            "machine chain-rule variation rows",
            ["MPD1044_1_chain_rule_identity", "DERIVED_STANDARD_ON_SHELL_IDENTITY"],
        ),
        (
            "SRC3250_1045_functor",
            ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
            "parent matter functor contract",
            ["parent matter functor contract is now exact", "MFS1045_1_observed_coframe_functor", "CG1045"],
        ),
        (
            "SRC3250_1046_shadow_constants",
            ROOT / "1046-Y5-R10-no-shadow-frame-constant-marker-theorem-or-qbar-marker-coefficients.md",
            "no-shadow-frame and constant/marker split",
            ["no-shadow", "constant", "qbar_marker"],
        ),
        (
            "SRC3250_1720_JH",
            ROOT / "1720-Y5-R2FR-observed-Hilbert-current-norm-source-row-or-matter-functor-signature.md",
            "observed Hilbert current definition route",
            ["J_H", "T_obs", "matter functor", "CG1720"],
        ),
        (
            "SRC3250_1721_wA",
            ROOT / "1721-Y5-R2FR-source-prefactor-exclusion-or-wA-current-row.md",
            "source-only prefactor and weighted-current debt",
            ["source-only", "w_A", "C_wH", "CG1721"],
        ),
        (
            "SRC3250_1722_CwH",
            OUT / "P8_Y5_PARENT_QLOC_1722_CWH_BOUND_LAW.csv",
            "weighted Hilbert current norm bound law",
            ["CWHL1722_0_definition", "C_wH", "EXACT_NORM_BOUND_FORM"],
        ),
        (
            "SRC3250_2600_tau",
            ROOT / "2600-Y5-R2FR-Tobs-delta-tau-norm-owner-or-boundary-clock-action-clause.md",
            "moving tau source-current law",
            ["Delta_JH_delta_tau", "C_Tobs_tau", "tau_obs", "CG2600"],
        ),
        (
            "SRC3250_2557_clock",
            ROOT / "2557-Y5-R2FR-Hilbert-current-conservation-scale-and-clock-compatibility-gate.md",
            "Hilbert-current conservation and clock-strain identity",
            ["J_M", "tau", "nabla_mu J_M", "DERIVATION_SHARPENED"],
        ),
        (
            "SRC3250_3136_clock",
            ROOT / "3136-Y5-R2FR-observed-coframe-clock-functional-owner-under-AX1090.md",
            "observed coframe clock functional theorem",
            ["e_obs", "S_matter", "same tau", "parent ownership"],
        ),
        (
            "SRC3250_3234_Poynting",
            ROOT / "3234-Y5-R2FR-Poynting-boundary-flux-silence-or-finite-bound-under-AX1090.md",
            "Poynting/Maxwell stress finite-bound functional",
            ["T_EM(u,n)", "S_EM dot n", "C_flux", "C_coll"],
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, role, needles in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def package_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "SFP3250_0_parent_package",
            "claim_piece": "same-frame source package",
            "statement": "Assume q_loc, e_obs=Obs_e(q_loc(Phi)), tau=tau_obs[e_obs,q_loc], and S_ord=sum_i w_i S_i[psi_i,e_obs,omega[e_obs],theta_i] are fixed by one parent action before readout.",
            "derivation": "This makes observed geometry, time generator, ordinary matter domain, stress definition, and source current one object rather than five separately fitted choices.",
            "current_status": "EXACT_PACKAGE_CONTRACT_NOT_PARENT_SIGNED",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SFP3250_1_vertical_chain",
            "claim_piece": "vertical invisibility",
            "statement": "For e_A in ker(Dq_loc), D_A e_obs=D Obs_e[D_A q_loc]=0; if tau=tau_obs[e_obs,q_loc], then D_A tau=0.",
            "derivation": "This imports 1045/3136 into the 3249 W_source selector without choosing a boundary by hand.",
            "current_status": "FORMAL_CHAIN_EXACT_IF_OBS_E_AND_TAU_OWNER_SIGNED",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SFP3250_2_Hilbert_current_identity",
            "claim_piece": "observed Hilbert current",
            "statement": "J_H[tau] := star_eobs(T_obs(tau,.)), with T_obs^{mu nu}=2/sqrt(-g_obs) delta S_ord/delta g_obs_munu and all ordinary sectors read in the same e_obs frame.",
            "derivation": "This is the lawful source-current identity, not a measured-GM import or a separate galaxy-fit current.",
            "current_status": "DEFINITION_READY_PARENT_PACKAGE_UNSIGNED",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SFP3250_3_DJH_zero_if_signed",
            "claim_piece": "D_A J_H zero theorem",
            "statement": "If D_A e_obs=0, D_A tau=0, D_A theta_i=0, D_A w_i=0 modulo common calibration, vertical matter lifts are gauge/fixed, and boundary terms vanish or are owned, then D_A J_H[tau]=0 as a distribution.",
            "derivation": "Vary J_H=star_eobs(sum_i w_i T_i_obs(tau,.)); each derivative term is killed by one signed package clause.",
            "current_status": "NEW_FUSED_CONDITIONAL_THEOREM",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SFP3250_4_Wsource_consequence",
            "claim_piece": "W_source q-basic",
            "statement": "Under SFP3250_3 plus compact regular support, W_source=closure(supp J_H[tau]) is q-basic and the 3249 collar/frame/normal construction becomes parent-owned.",
            "derivation": "This closes the logical gap between matter-source coupling and the local Poynting boundary selector.",
            "current_status": "CONDITIONAL_ROLLFORWARD_TO_3249",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "DJH3250_0_master_bound",
            "source": "D_A J_H[tau]",
            "bound_form": "||D_A J_H|| <= C_e||D_A e_obs|| + C_tau||D_A tau|| + C_w||delta w|| + C_theta||D_A theta|| + C_shadow||D_A zeta_shadow|| + B_lift + B_support + B_edge",
            "derived_from": "chain rule on star_eobs(sum_i w_i T_i_obs(tau,.))",
            "zero_condition": "all same-frame package clauses parent-signed",
            "current_status": "FUSED_BOUND_FORM_DERIVED_INPUTS_MISSING",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "DJH3250_1_geometry",
            "source": "C_e||D_A e_obs||",
            "bound_form": "zero if e_obs=Obs_e(q_loc(Phi)) and e_A in ker(Dq_loc); otherwise retain observed-frame leak",
            "derived_from": "1045 coframe functor chain rule",
            "zero_condition": "parent signs Obs_e(q_loc) and no hidden coframe re-entry",
            "current_status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "DJH3250_2_tau",
            "source": "C_tau||D_A tau||",
            "bound_form": "Delta_JH_delta_tau <= C_Tobs_tau ||delta tau_obs||_B",
            "derived_from": "2600 exact moving-tau operator law",
            "zero_condition": "tau fixed by same parent time/clock/boundary generator or C_Tobs_tau=0 theorem",
            "current_status": "EXACT_BOUND_FORM_VALUES_MISSING",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "DJH3250_3_weighted_source",
            "source": "C_w||delta w||",
            "bound_form": "C_wH <= C_Tw(A_ext,norm,tau,basis)||delta w||_Sigma",
            "derived_from": "1721/1722 source-prefactor and weighted-current bound",
            "zero_condition": "no-Hom/action-density edge theorem forces delta_w=0 up to common calibration",
            "current_status": "EXACT_BOUND_FORM_PARENT_EDGE_UNSIGNED",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "DJH3250_4_constants_markers",
            "source": "C_theta||D_A theta|| + C_shadow||D_A zeta_shadow||",
            "bound_form": "constant/marker response remains qbar_constants/qbar_marker until no-shadow-frame and superselection split are parent-signed",
            "derived_from": "1044/1045/1046 matter-pullback and no-shadow-frame audits",
            "zero_condition": "theta_i fixed representation data and no hidden Weyl/disformal/material marker vertices",
            "current_status": "CONDITIONAL_ZERO_COEFFICIENTS_MISSING",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "DJH3250_5_lift_boundary_support",
            "source": "B_lift + B_support + B_edge",
            "bound_form": "vertical matter lift, compact support, and boundary edge terms must be owned exact/gauge terms or bounded on W_source collar",
            "derived_from": "1044 boundary/support plus 3249 support regularity",
            "zero_condition": "parent-owned matter bundle lift and regular compact source support",
            "current_status": "UNSIGNED_NONCLAIM",
            "valid_for_claim": "false",
        },
    ]


def em_projection_rows() -> list[dict[str, Any]]:
    return [
        {
            "identity_id": "EMF3250_0_projection",
            "object": "Maxwell stress flux through source-worldtube collar",
            "identity": "T_EM(u,n)=S_EM dot n in an observed orthonormal frame with u timelike unit, n spatial unit, and g_obs(u,n)=0",
            "bound": "use this as the frame-owned meaning of the Poynting term in 3234/3249",
            "required_inputs": "observed Maxwell sector, e_obs frame, unit u,n from q-basic collar",
            "current_status": "FORMAL_IDENTITY_CONDITIONAL_ON_MAXWELL_STRESS_DESCENT",
            "valid_for_claim": "false",
        },
        {
            "identity_id": "EMF3250_1_boundary_L1_bound",
            "object": "normal Poynting flux norm",
            "identity": "S_EM dot n=(1/mu0)(E x B) dot n in SI units, or S_EM dot n=(E x B) dot n in natural units",
            "bound": "||S_EM dot n||_L1(B) <= mu0^-1 ||E_T||_L2(B)||B_T||_L2(B)",
            "required_inputs": "unit convention, E/B field norms on B, surface measure, orientation",
            "current_status": "CAUCHY_SCHWARZ_BOUND_FORM_DERIVED_NUMERIC_INPUTS_MISSING",
            "valid_for_claim": "false",
        },
        {
            "identity_id": "EMF3250_2_collar_bulk_bound",
            "object": "collar Maxwell stress norm",
            "identity": "||T_EM(u,n)||_L1(C) is bounded by the same observed E/B energy-flux envelope on the collar",
            "bound": "||T_EM(u,n)||_L1(C) <= C_geom,units ||E||_L2(C)||B||_L2(C)",
            "required_inputs": "collar volume measure, C_geom, unit system, observed E/B norms",
            "current_status": "BOUND_FORM_DERIVED_NUMERIC_INPUTS_MISSING",
            "valid_for_claim": "false",
        },
        {
            "identity_id": "EMF3250_3_no_F2_shortcut",
            "object": "null/radiative EM guard",
            "identity": "F_mu_nu F^mu_nu=0 does not imply S_EM dot n=0 or T_EM(u,n)=0",
            "bound": "must use flux/stress norm, not scalar F^2 silence",
            "required_inputs": "none; guardrail inherited from 3234",
            "current_status": "GUARDRAIL_ACTIVE",
            "valid_for_claim": "false",
        },
    ]


def flux_norm_rows() -> list[dict[str, Any]]:
    return [
        {
            "flux_row_id": "FNR3250_0_source_worldtube_boundary_flux_norm",
            "component_id": "SWP3249_0_source_worldtube_Poynting_bound",
            "boundary_id": "source_worldtube_Wsource_CONDITIONAL",
            "quantity": "||S_EM dot n||_L1(B)",
            "formula": "||S_EM dot n||_L1(B) <= mu0^-1 ||E_T||_L2(B)||B_T||_L2(B)",
            "unit_system": "MISSING_SI_OR_NATURAL_UNIT_CHOICE",
            "E_norm": "MISSING_E_T_L2_ON_B",
            "B_norm": "MISSING_B_T_L2_ON_B",
            "surface_measure": "MISSING_DSIGMA_B_FROM_QBASIC_COLLAR",
            "orientation": "MISSING_ORIENTATION_FROM_WSOURCE_NORMAL",
            "computed_value": "NOT_COMPUTED",
            "current_status": "FIRST_CONCRETE_FLUX_NORM_ROW_FORM_ONLY",
            "valid_for_claim": "false",
        },
        {
            "flux_row_id": "FNR3250_1_source_worldtube_collar_bulk_norm",
            "component_id": "SWP3249_0_source_worldtube_Poynting_bound",
            "boundary_id": "source_worldtube_Wsource_CONDITIONAL",
            "quantity": "||T_EM(u,n)||_L1(collar)",
            "formula": "||T_EM(u,n)||_L1(C) <= C_geom,units ||E||_L2(C)||B||_L2(C)",
            "unit_system": "MISSING_SI_OR_NATURAL_UNIT_CHOICE",
            "E_norm": "MISSING_E_L2_ON_COLLAR",
            "B_norm": "MISSING_B_L2_ON_COLLAR",
            "surface_measure": "MISSING_COLLAR_VOLUME_MEASURE",
            "orientation": "MISSING_U_N_NORMALIZATION",
            "computed_value": "NOT_COMPUTED",
            "current_status": "COLLAR_BULK_FLUX_NORM_ROW_FORM_ONLY",
            "valid_for_claim": "false",
        },
    ]


def wsource_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "WSU3250_0_DJH_to_Wsource",
            "target": "SEL3249_5_worldtube_fixed",
            "update": "D_A J_H=0 is now decomposed into geometry, tau, weighted-source, constants/markers, lift, support and edge clauses.",
            "if_all_zero": "D_A W_source=0 and source-worldtube collar becomes parent-owned",
            "if_not_zero": "support drift Delta_W_source and Poynting source-worldtube bound rows remain active",
            "current_status": "DECOMPOSITION_ADVANCES_SELECTOR_GATE",
            "valid_for_claim": "false",
        },
        {
            "update_id": "WSU3250_1_flux_norm_to_Poynting",
            "target": "SWP3249_0_source_worldtube_Poynting_bound",
            "update": "Replace opaque MISSING_T_EM_U_N_ON_SOURCE_COLLAR with explicit E/B L2 flux-norm acquisition rows FNR3250_0 and FNR3250_1.",
            "if_all_zero": "Poynting contribution can be theorem-zeroed only by no-flux support or owned exact/proper flux",
            "if_not_zero": "finite flux bound is computable after E/B norms, units and measures are sourced",
            "current_status": "FLUX_NORM_SCHEMA_FILLED_NONCLAIM",
            "valid_for_claim": "false",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG3250_0_fused_theorem",
            "claim": "same-frame package implies D_A J_H=0 conditionally",
            "gate_pass": "true",
            "reason": "chain rule on J_H=star_eobs(T_obs(tau,.)) has all residual channels named",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3250_1_current_parent_package",
            "claim": "current MTS parent action signs e_obs/tau/J_H package",
            "gate_pass": "false",
            "reason": "matter functor, no-shadow/constants, source-prefactor, tau owner and support clauses remain unsigned",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3250_2_DJH_zero_current",
            "claim": "D_A J_H=0 is a current MTS theorem",
            "gate_pass": "false",
            "reason": "DJH residual vector has live nonzero-or-unbounded terms",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3250_3_flux_numeric",
            "claim": "source-worldtube Poynting flux norm is numeric/source-backed",
            "gate_pass": "false",
            "reason": "E/B norms, unit convention, measure and orientation are missing",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3250_4_local_GR_Newton",
            "claim": "local GR/Newton/Maxwell source coupling is derived",
            "gate_pass": "false",
            "reason": "same-frame source package and flux norm remain bound-form only",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3250_0_progress",
            "decision": "Keep the same-frame source package as the main coupling route",
            "because": "it fuses matter functor, clock/tau, Hilbert current, W_source and Poynting boundary into one derivation path",
            "next_action": "attack the source-prefactor/action-density edge and no-shadow/constants clauses before numeric local claims",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3250_1_flux_fallback",
            "decision": "Keep the source-worldtube flux-norm row as the empirical fallback",
            "because": "if D_A J_H cannot be zeroed, the Poynting leakage must be bounded by observed E/B flux norms",
            "next_action": "source or derive E/B collar norms only after the q-basic collar and unit convention are fixed",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3250_2_no_claim",
            "decision": "No local-GR/Maxwell/Newton claim from this checkpoint",
            "because": "the proof is conditional and the numeric fallback still has missing inputs",
            "next_action": "write 3251 against the weighted-source/no-Hom edge or the no-shadow constants split",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3250_0_3251",
            "selection": "selected_primary",
            "next_checkpoint": "3251-Y5-R2FR-source-prefactor-edge-zero-or-same-frame-DJH-residual-first-bound-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_3251_source_prefactor_edge_zero_or_same_frame_DJH_residual_first_bound.py",
            "objective": "Try to prove the no-Hom/action-density edge condition that makes delta_w=0 and removes C_wH from D_A J_H; if not, stage the first same-frame DJH residual bound row with C_Tw, delta_w norm, tau, annulus and units.",
            "guardrail": "do not use covariance/additivity alone to kill source weights; do not import measured GM; no local-GR or WEP claim",
            "valid_for_claim": "false",
        }
    ]


def validation_rows(source_rows: list[dict[str, Any]], generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources_exist = all(row["exists"] == "true" for row in source_rows)
    sources_hit = all(row["evidence_hits"] not in {"MISSING_SOURCE", "NO_MATCH"} for row in source_rows)
    csvs_parse = all(csv_ok(path) for path in generated_csvs)
    under_post_checkpoint = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in [*generated_csvs, DOC])
    formalization_3250 = list(FW.rglob("*3250*")) if FW.exists() else []
    formalization_clean = len(formalization_3250) == 0
    theorem_fused = any(row["theorem_id"] == "SFP3250_3_DJH_zero_if_signed" for row in package_rows())
    residual_vector_present = any(row["residual_id"] == "DJH3250_0_master_bound" for row in residual_rows())
    residuals_nonclaim = all(row["valid_for_claim"] == "false" for row in residual_rows())
    em_projection_present = any(row["identity_id"] == "EMF3250_1_boundary_L1_bound" for row in em_projection_rows())
    flux_rows_nonclaim = all(row["valid_for_claim"] == "false" for row in flux_norm_rows())
    flux_rows_have_missing = any("MISSING_" in ";".join(str(value) for value in row.values()) for row in flux_norm_rows())
    claims_blocked = all(row["claim_allowed"] == "false" for row in gate_rows())
    current_package_false = any(row["claim_gate_id"] == "CG3250_1_current_parent_package" and row["gate_pass"] == "false" for row in gate_rows())
    next_written = bool(next_rows())
    doc_written = DOC.exists()
    checks = [
        ("VAL3250_0_sources_exist", sources_exist, "all cited source paths exist", str(sources_exist)),
        ("VAL3250_1_source_hits", sources_hit, "source evidence hits are present", str(sources_hit)),
        ("VAL3250_2_csvs_parse", csvs_parse, "all generated CSV files parse", str(csvs_parse)),
        ("VAL3250_3_outputs_under_post_checkpoint", under_post_checkpoint, "all outputs are under post-checkpoint-work", str(under_post_checkpoint)),
        ("VAL3250_4_formalization_clean", formalization_clean, "no 3250 outputs in formalization-workbench", f"formalization_3250_count={len(formalization_3250)}"),
        ("VAL3250_5_theorem_fused", theorem_fused, "same-frame D_A J_H zero theorem written", str(theorem_fused)),
        ("VAL3250_6_residual_vector_present", residual_vector_present, "D_A J_H residual vector present", str(residual_vector_present)),
        ("VAL3250_7_residuals_nonclaim", residuals_nonclaim, "D_A J_H residual rows remain nonclaim", str(residuals_nonclaim)),
        ("VAL3250_8_em_projection_present", em_projection_present, "EM stress projection and L1 flux bound present", str(em_projection_present)),
        ("VAL3250_9_flux_rows_nonclaim", flux_rows_nonclaim, "flux norm rows remain nonclaim", str(flux_rows_nonclaim)),
        ("VAL3250_10_flux_rows_have_missing", flux_rows_have_missing, "flux norm rows preserve missing-input markers", str(flux_rows_have_missing)),
        ("VAL3250_11_claims_blocked", claims_blocked, "all claim gates remain blocked", str(claims_blocked)),
        ("VAL3250_12_current_package_false", current_package_false, "current parent package claim remains false", str(current_package_false)),
        ("VAL3250_13_next_written", next_written, "3251 next target written", str(next_written)),
        ("VAL3250_14_doc_written", doc_written, "3250 markdown checkpoint exists", str(doc_written)),
    ]
    rows = [
        {
            "validation_id": validation_id,
            "passed": bool_str(passed),
            "requirement": requirement,
            "evidence": evidence_text,
        }
        for validation_id, passed, requirement, evidence_text in checks
    ]
    rows.append(
        {
            "validation_id": "VAL3250_OVERALL",
            "passed": bool_str(all(row["passed"] == "true" for row in rows)),
            "requirement": "3250 validation overall",
            "evidence": "all required validation rows passed",
        }
    )
    return rows


def write_markdown(
    source_rows: list[dict[str, Any]],
    package: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    em_projection: list[dict[str, Any]],
    flux_rows: list[dict[str, Any]],
    wsource_update: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    lines = [
        "# 3250 - Hilbert current eobs tau owner or source-worldtube flux norm row under AX1090",
        "",
        f"Generated: `{RUN_UTC}`",
        "",
        "Private derivation checkpoint. This does not claim local GR, Newton, Maxwell, PPN, WEP, R10, clocks, orbital closure, or source-coupling closure.",
        "",
        "## Summary",
        "",
        "- `3250` fuses the previous fragments into one same-frame source-package theorem: if `e_obs`, `tau`, ordinary matter, source weights, constants/markers, lift, support and boundary all descend through one parent action, then `D_A J_H[tau]=0`.",
        "- This is the concrete coupling route: `J_H[tau] := star_eobs(T_obs(tau,.))`, and the derivative is no longer vague; it decomposes into geometry, tau, weighted-source, constants/markers, lift/support and edge residuals.",
        "- Current MTS still cannot claim the zero theorem because the no-shadow/constants split, no-source-prefactor/action-density edge, tau owner and compact support clauses remain unsigned.",
        "- The fallback was improved: the source-worldtube Poynting row now has explicit Maxwell flux identities, including `||S_EM dot n||_L1(B) <= mu0^-1 ||E_T||_L2(B)||B_T||_L2(B)`.",
        "- So the work moved forward in two ways: one sharper theorem route, one sharper empirical/numeric bound route.",
        "",
        "## Same-Frame Package Theorem",
        "",
        md_table(package, ["theorem_id", "claim_piece", "statement", "derivation", "current_status", "claim_allowed", "valid_for_claim"]),
        "",
        "## D_A J_H Residual Vector",
        "",
        md_table(residuals, ["residual_id", "source", "bound_form", "derived_from", "zero_condition", "current_status", "valid_for_claim"]),
        "",
        "## EM Stress Projection And Flux Norm",
        "",
        md_table(em_projection, ["identity_id", "object", "identity", "bound", "required_inputs", "current_status", "valid_for_claim"]),
        "",
        "## Source-Worldtube Flux Norm Rows",
        "",
        md_table(flux_rows, ["flux_row_id", "component_id", "boundary_id", "quantity", "formula", "unit_system", "E_norm", "B_norm", "surface_measure", "orientation", "computed_value", "current_status", "valid_for_claim"]),
        "",
        "## W Source Update",
        "",
        md_table(wsource_update, ["update_id", "target", "update", "if_all_zero", "if_not_zero", "current_status", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(gates, ["claim_gate_id", "claim", "gate_pass", "reason", "claim_allowed"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_target, ["next_id", "selection", "next_checkpoint", "next_script", "objective", "guardrail", "valid_for_claim"]),
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["validation_id", "passed", "requirement", "evidence"]),
        "",
        "## Working Verdict",
        "",
        "`3250` does not close the local branch, but it does stop the coupling problem being mush. The exact theorem route is now a same-frame package signature; the exact fallback is a `D_A J_H` residual vector plus an E/B Poynting flux-norm acquisition row. The next best strike is the weighted-source/no-Hom action-density edge, because that removes `C_wH` from the source current without needing data.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register()
    package = package_rows()
    residuals = residual_rows()
    em_projection = em_projection_rows()
    flux_rows = flux_norm_rows()
    wsource_update = wsource_update_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    generated_without_validation = [
        OUTPUTS["sources"],
        OUTPUTS["package"],
        OUTPUTS["residual"],
        OUTPUTS["em_projection"],
        OUTPUTS["flux_row"],
        OUTPUTS["wsource_update"],
        OUTPUTS["gates"],
        OUTPUTS["decision"],
        OUTPUTS["next"],
    ]

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["package"], package)
    write_csv(OUTPUTS["residual"], residuals)
    write_csv(OUTPUTS["em_projection"], em_projection)
    write_csv(OUTPUTS["flux_row"], flux_rows)
    write_csv(OUTPUTS["wsource_update"], wsource_update)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    DOC.write_text(
        "# 3250 - Hilbert current eobs tau owner or source-worldtube flux norm row under AX1090\n\n"
        "Pending final validation table.\n",
        encoding="utf-8",
    )
    validation = validation_rows(source_rows, generated_without_validation)
    write_csv(OUTPUTS["validation"], validation)
    write_markdown(source_rows, package, residuals, em_projection, flux_rows, wsource_update, gates, decisions, next_target, validation)

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    overall = next(row for row in validation if row["validation_id"] == "VAL3250_OVERALL")
    if overall["passed"] != "true":
        raise SystemExit("3250 validation failed")


if __name__ == "__main__":
    main()
