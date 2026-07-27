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

DOC = ROOT / "3254-Y5-R2FR-first-component-current-Gram-row-or-parent-signature-clause-lock-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3254_SOURCE_REGISTER.csv",
    "derivation": OUT / "P8_Y5_R2FR_3254_EM_STRESS_CURRENT_DERIVATION.csv",
    "gram_row": OUT / "P8_Y5_R2FR_3254_EM_COMPONENT_CURRENT_GRAM_ROW.csv",
    "bounds": OUT / "P8_Y5_R2FR_3254_EM_CURRENT_NORM_BOUND_ROWS.csv",
    "ctw_update": OUT / "P8_Y5_R2FR_3254_CTW_GRAM_MATRIX_UPDATE.csv",
    "signature_lock": OUT / "P8_Y5_R2FR_3254_PARENT_SIGNATURE_CLAUSE_LOCK.csv",
    "gates": OUT / "P8_Y5_R2FR_3254_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3254_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3254_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_R2FR_3254_VALIDATION.csv",
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
                    hits.append(f"L{line_number}:{clean[:240]}")
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
            "SRC3254_3253_handoff",
            ROOT / "3253-Y5-R2FR-parent-ordinary-sector-action-signature-or-C_Tw-component-current-norm-intake-under-AX1090.md",
            "3253 selected EM/Coulomb as first component-current Gram target",
            ["NEXT3253_0_3254", "EM/Coulomb", "lambda_max"],
        ),
        (
            "SRC3254_3253_finite_law",
            OUT / "P8_Y5_R2FR_3253_CTW_FINITE_GRAM_OPERATOR_LAW.csv",
            "finite Gram/eigenvalue C_Tw law",
            ["CTWG3253_1_exact_gram_operator_norm", "lambda_max"],
        ),
        (
            "SRC3254_3253_intake",
            OUT / "P8_Y5_R2FR_3253_CTW_COMPONENT_CURRENT_NORM_INTAKE_SCHEMA.csv",
            "component-current intake row for EM/Coulomb",
            ["DCW1231_4_EM_Coulomb_binding", "MISSING_COMPONENT_CURRENT_GRAM_ROW"],
        ),
        (
            "SRC3254_1231_basis",
            OUT / "P8_Y5_R10_1231_DISCONNECTED_COMPONENT_RESIDUAL_BASIS.csv",
            "disconnected component basis containing EM/Coulomb binding",
            ["DCW1231_4_EM_Coulomb_binding", "delta w_EM"],
        ),
        (
            "SRC3254_3250_identity",
            OUT / "P8_Y5_R2FR_3250_EM_STRESS_PROJECTION_AND_FLUX_NORM_IDENTITY.csv",
            "Maxwell stress/Poynting identities already derived",
            ["EMF3250_0_projection", "EMF3250_1_boundary_L1_bound"],
        ),
        (
            "SRC3254_3250_doc",
            ROOT / "3250-Y5-R2FR-Hilbert-current-eobs-tau-owner-or-source-worldtube-flux-norm-row-under-AX1090.md",
            "same-frame Hilbert-current identity and EM flux bridge",
            ["J_H[tau]", "EM Stress Projection"],
        ),
        (
            "SRC3254_3249_poynting_row",
            OUT / "P8_Y5_R2FR_3249_SOURCE_WORLDTUBE_POYNTING_BOUND_ROW.csv",
            "source-worldtube Poynting finite bound row",
            ["SWP3249_0_source_worldtube_Poynting_bound", "closure(supp J_H[tau])"],
        ),
        (
            "SRC3254_3246_doc",
            ROOT / "3246-Y5-R2FR-first-Poynting-Jtot-score-row-or-boundary-frame-source-acquisition-under-AX1090.md",
            "first Poynting Jtot score row and regime classifier",
            ["REG3246_1_electrostatic", "PJS3246_0_first_component"],
        ),
        (
            "SRC3254_3234_doc",
            ROOT / "3234-Y5-R2FR-Poynting-boundary-flux-silence-or-finite-bound-under-AX1090.md",
            "Poynting functional, finite bound, and no-F2 shortcut guard",
            ["Phi_Poynting", "F^2=0 does not imply"],
        ),
        (
            "SRC3254_1397_uniqueF2",
            OUT / "P8_Y5_R10_1397_UNIQUE_MAXWELL_F2_PROOF_AUDIT.csv",
            "unique Maxwell F2 proof status",
            ["UMF1397_6_exact_conditional_theorem", "UMF1397_7_current_verdict"],
        ),
        (
            "SRC3254_1400_residual",
            OUT / "P8_Y5_R10_1400_FINITE_EM_LOCAL_RESIDUAL_VECTOR.csv",
            "finite EM local residual vector",
            ["REM1400_7_beta_EM", "REM1400_9_local_PPN"],
        ),
        (
            "SRC3254_1234_em_owner",
            OUT / "P8_Y5_R10_1234_EM_OWNER_UNIQUENESS_PROOF_ATTEMPT.csv",
            "EM owner uniqueness blockers",
            ["EMU1234_2_unique_F2", "EMU1234_6_verdict"],
        ),
        (
            "SRC3254_1233_em_edge",
            OUT / "P8_Y5_R10_1233_EM_CURRENT_EDGE_OWNER_PROOF_ATTEMPT.csv",
            "electron-photon edge conditional theorem",
            ["EME1233_2_current_ward_edge", "EME1233_4_graph_edge_verdict"],
        ),
        (
            "SRC3254_987_normal_forms",
            OUT / "P8_Y5_R10_987_EM_NORMAL_FORMS.csv",
            "Coulomb/alpha normal-form split",
            ["EMNF987_4_verdict", "EMNF987_1_finite_alphaEM_X"],
        ),
        (
            "SRC3254_989_em_lock",
            OUT / "P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv",
            "EM lock signature audit",
            ["ELA989_1_unique_F2", "ELA989_5_total"],
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


def derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "derivation_id": "EMD3254_0_component_selection",
            "object": "DCW1231_4_EM_Coulomb_binding",
            "formal_statement": "Select the EM/Coulomb binding residual component delta_w_EM as the first finite C_Tw component-current target.",
            "derivation_gain": "links source coupling, Maxwell stress, Poynting flux, alpha/EM residuals, and WEP material response in one component",
            "current_status": "SELECTED_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "EMD3254_1_stress_tensor",
            "object": "T_EM_obs",
            "formal_statement": "T_EM_obs[mn] := kappa_EM^-1(F_m a F_n^a - 1/4 g_obs[mn] F_ab F^ab), with kappa_EM fixed by the unit convention and parent EM owner.",
            "derivation_gain": "turns the EM component row into the standard Maxwell Hilbert stress object rather than an ad hoc force coefficient",
            "current_status": "FORMAL_MAXWELL_STRESS_ROW_READY_UNIT_OWNER_MISSING",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "EMD3254_2_current_form",
            "object": "J_EM[tau]",
            "formal_statement": "j_EM[tau]_nu := T_EM_obs[mu nu] tau^mu and J_EM[tau] := star_eobs(j_EM[tau]) on A_ext.",
            "derivation_gain": "fills the exact component-current definition demanded by 3253: J_c=star_eobs(T_c_obs(tau,.))",
            "current_status": "EXACT_DEFINITION_READY",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "EMD3254_3_gram_self_entry",
            "object": "G_J[EM,EM]",
            "formal_statement": "G_J[EM,EM] := <J_EM,J_EM>_J = integral_Aext w_J g_J^{-1}(j_EM,j_EM) dmu_eobs, or the declared equivalent current norm.",
            "derivation_gain": "first diagonal Gram entry is now a real integral contract, not a blank norm label",
            "current_status": "INTEGRAL_CONTRACT_READY_NUMERIC_FIELDS_MISSING",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "EMD3254_4_cross_entries",
            "object": "G_J[EM,d]",
            "formal_statement": "G_J[EM,d] := <J_EM,J_d>_J for d in {electron, light_quark, QCD_gluon, nuclear_surface, measure_readout}.",
            "derivation_gain": "prevents a false diagonal/RSS claim: exact C_Tw needs cross-current overlaps unless orthogonality is proved",
            "current_status": "CROSS_ENTRY_SCHEMA_READY",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "EMD3254_5_poynting_bridge",
            "object": "boundary_flux_projection",
            "formal_statement": "For observed orthonormal u,n, T_EM(u,n)=S_EM dot n; boundary/collar Poynting rows are projections of the same J_EM stress-current object, not a separate residual species.",
            "derivation_gain": "connects the earlier Poynting work to the C_Tw Gram row and avoids double-counting EM stress",
            "current_status": "BRIDGE_DERIVED_CONDITIONAL_ON_FRAME_AND_UNIT_OWNER",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "EMD3254_6_no_F2_shortcut",
            "object": "guardrail",
            "formal_statement": "F_ab F^ab=0 or unique-F2 scalar silence cannot by itself set J_EM, T_EM(u,n), or G_J[EM,EM] to zero.",
            "derivation_gain": "keeps radiative/null EM and Poynting stress from being incorrectly erased",
            "current_status": "GUARDRAIL_ACTIVE",
            "valid_for_claim": "false",
        },
    ]


def gram_rows() -> list[dict[str, Any]]:
    return [
        {
            "gram_id": "GJ3254_EM_EM_SELF",
            "basis_component_id": "DCW1231_4_EM_Coulomb_binding",
            "component": "EM/Coulomb binding contribution",
            "residual_symbol": "delta_w_EM",
            "J_c": "J_EM[tau] := star_eobs(T_EM_obs(tau,.))",
            "gram_entry": "G_J[EM,EM] = <J_EM,J_EM>_J",
            "integral_contract": "integral_Aext w_J g_J^{-1}(j_EM,j_EM) dmu_eobs",
            "required_inputs": "unit_system;kappa_EM;A_ext;w_J;g_J or current norm;tau_id;e_obs_id;F_obs or E/B fields;dmu_eobs",
            "current_value": "MISSING_GJ_EM_EM_NUMERIC_VALUE",
            "units": "MISSING_CURRENT_GRAM_UNITS",
            "source_path": "MISSING_FIELD_PROFILE_OR_DATA_SOURCE",
            "valid_for_claim": "false",
        },
        {
            "gram_id": "GJ3254_EM_ALL_CROSS",
            "basis_component_id": "DCW1231_4_EM_Coulomb_binding",
            "component": "EM/current overlap with every other disconnected source component",
            "residual_symbol": "delta_w_EM x delta_w_d",
            "J_c": "J_EM and J_d",
            "gram_entry": "G_J[EM,d] = <J_EM,J_d>_J",
            "integral_contract": "integral_Aext w_J g_J^{-1}(j_EM,j_d) dmu_eobs",
            "required_inputs": "component stress decomposition for d;orthogonality theorem or all cross integrals",
            "current_value": "MISSING_GJ_EM_D_CROSS_VALUES",
            "units": "MISSING_CURRENT_GRAM_UNITS",
            "source_path": "MISSING_COMPONENT_STRESS_SOURCE_PATHS",
            "valid_for_claim": "false",
        },
        {
            "gram_id": "GJ3254_EM_DIAGONAL_SAFE_BOUND",
            "basis_component_id": "DCW1231_4_EM_Coulomb_binding",
            "component": "safe diagonal contribution to C_Tw upper bound",
            "residual_symbol": "delta_w_EM",
            "J_c": "||J_EM||_J",
            "gram_entry": "C_Tw_upper^2 receives + ||J_EM||_J^2",
            "integral_contract": "valid only as an upper-bound contribution unless cross entries/orthogonality are supplied",
            "required_inputs": "a bound on ||J_EM||_J in the same J norm used by 3253",
            "current_value": "BOUND_FORM_ONLY",
            "units": "MISSING_CURRENT_NORM_UNITS",
            "source_path": "P8_Y5_R2FR_3254_EM_CURRENT_NORM_BOUND_ROWS.csv",
            "valid_for_claim": "false",
        },
    ]


def bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "EMB3254_0_L1_energy_current_bound",
            "quantity": "||J_EM[tau]||_L1(A_ext)",
            "bound_formula": "||J_EM||_L1 <= C_star C_tau kappa_EM^-1 (||E||_L2(A_ext)^2 + ||B||_L2(A_ext)^2)",
            "derivation": "Maxwell stress is quadratic in F; contract with bounded tau and integrate the energy-density envelope",
            "required_inputs": "C_star;C_tau;kappa_EM;E_L2;B_L2;A_ext;unit convention",
            "current_value": "MISSING_E_B_L2_AND_UNIT_CONSTANTS",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "EMB3254_1_L2_current_bound",
            "quantity": "||J_EM[tau]||_L2(A_ext)",
            "bound_formula": "||J_EM||_L2 <= C_star C_tau kappa_EM^-1 (||E||_L4(A_ext)^2 + ||B||_L4(A_ext)^2)",
            "derivation": "quadratic stress requires L4 field control for an L2 current norm, unless an L_infty x L2 mixed envelope is sourced",
            "required_inputs": "E_L4;B_L4 or E_Linf/B_Linf with L2 norms;A_ext;unit convention",
            "current_value": "MISSING_L4_OR_AMPLITUDE_ENVELOPE",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "EMB3254_2_boundary_poynting_projection",
            "quantity": "||S_EM dot n||_L1(boundary)",
            "bound_formula": "||S_EM dot n||_L1(B) <= kappa_EM^-1 ||E_T||_L2(B)||B_T||_L2(B)",
            "derivation": "Cauchy-Schwarz on the observed boundary projection T_EM(u,n)=S_EM dot n",
            "required_inputs": "boundary B;unit u,n;surface measure;E_T_L2;B_T_L2;kappa_EM",
            "current_value": "MISSING_BOUNDARY_E_B_NORMS",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "EMB3254_3_static_coulomb_warning",
            "quantity": "EM/Coulomb binding current",
            "bound_formula": "quiet electrostatic fields can have S_EM dot n=0 while T_EM(tau,.) and Coulomb binding energy are nonzero",
            "derivation": "Poynting flux silence is not the same as EM stress-current silence",
            "required_inputs": "do not use zero Poynting flux as zero G_J[EM,EM]",
            "current_value": "GUARDRAIL_ACTIVE",
            "valid_for_claim": "false",
        },
    ]


def ctw_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "CTWU3254_0_first_Gram_row",
            "target": "C_Tw finite Gram matrix",
            "previous_status": "component-current intake row had MISSING_COMPONENT_CURRENT_GRAM_ROW",
            "new_status": "EM self/cross Gram integral contracts and E/B norm bounds are written",
            "effect": "one component can now be filled by supplying Maxwell field profiles or stress-current norms in the declared arena",
            "valid_for_claim": "false",
        },
        {
            "update_id": "CTWU3254_1_operator_bound",
            "target": "weighted-source piece of D_A J_H",
            "previous_formula": "||D_A J_H||_weighted <= sqrt(lambda_max(G_J,G_Sigma)) ||delta_w||_Sigma",
            "new_formula": "same formula, with G_J[EM,EM] and G_J[EM,d] now defined as explicit Maxwell-stress current integrals",
            "effect": "future numeric work has an actual matrix slot to fill",
            "valid_for_claim": "false",
        },
        {
            "update_id": "CTWU3254_2_no_double_count",
            "target": "Poynting vs EM/Coulomb source residual",
            "previous_status": "Poynting rows and source-weight rows were adjacent but not formally joined",
            "new_status": "Poynting boundary flux is recorded as a boundary projection of J_EM/T_EM, not an independent extra EM component",
            "effect": "reduces bookkeeping ambiguity in the local source branch",
            "valid_for_claim": "false",
        },
    ]


def signature_lock_rows() -> list[dict[str, Any]]:
    return [
        {
            "lock_id": "PSL3254_0_unique_Maxwell_owner",
            "parent_signature_clause": "unique observed Maxwell F2 / fixed EM owner",
            "status": "STILL_UNSIGNED",
            "why_not_closed": "lambda_A F_Q^2 remains a legal current-corpus counterexample",
            "finite_fallback": "keep lambda_A/b_alpha_EM rows and EM stress-current Gram row",
            "valid_for_claim": "false",
        },
        {
            "lock_id": "PSL3254_1_current_normalization_owner",
            "parent_signature_clause": "same charge-current/source normalization owner",
            "status": "STILL_UNSIGNED",
            "why_not_closed": "charge Ward current does not by itself fix gravitational source normalization or source-label forgetting",
            "finite_fallback": "EM component source weight delta_w_EM remains in G_Sigma/G_J until source-label theorem closes",
            "valid_for_claim": "false",
        },
        {
            "lock_id": "PSL3254_2_readout_Hodge_units",
            "parent_signature_clause": "quotient-fixed Hodge/coframe/hbar*c readout",
            "status": "STILL_UNSIGNED",
            "why_not_closed": "dimensionless alpha and measured EM stress can drift through readout unless the parent readout map is signed",
            "finite_fallback": "record kappa_EM/unit convention as required input before any score",
            "valid_for_claim": "false",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG3254_0_EM_current_definition",
            "claim": "J_EM[tau]=star_eobs(T_EM_obs(tau,.)) component current definition is exact",
            "gate_pass": "true",
            "reason": "directly follows from 3250 Hilbert current identity and standard Maxwell stress definition",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3254_1_first_Gram_row_contract",
            "claim": "first EM Gram self/cross integral contract is written",
            "gate_pass": "true",
            "reason": "G_J[EM,EM] and G_J[EM,d] are explicit current-inner-product integrals",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3254_2_EM_Gram_numeric",
            "claim": "EM Gram entries are numeric/source-backed",
            "gate_pass": "false",
            "reason": "A_ext, tau, e_obs, kappa_EM, current norm, E/B profiles, units, and cross stress decompositions are still missing",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3254_3_EM_zero",
            "claim": "EM/Coulomb component makes zero contribution to C_Tw",
            "gate_pass": "false",
            "reason": "Poynting flux silence or F^2 silence does not imply Maxwell stress-current silence",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3254_4_parent_EM_owner",
            "claim": "unique parent EM owner closes source coupling structurally",
            "gate_pass": "false",
            "reason": "unique F2, current normalization, readout, and no-alpha/binding vertices remain unsigned",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3254_5_local_GR_Newton_Maxwell",
            "claim": "local GR/Newton/Maxwell source branch is derived or bounded enough to claim",
            "gate_pass": "false",
            "reason": "only one component-current row is structurally filled; numeric source-side bound and full residual vector remain open",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3254_0_progress",
            "decision": "Treat EM/Coulomb as the first concrete C_Tw Gram component",
            "because": "it is the shared pressure point for Maxwell stress, Poynting flux, alpha/EM residuals, and material source coupling",
            "next_action": "source or derive the actual A_ext/tau/e_obs/current-norm/E-B input pack",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3254_1_guardrail",
            "decision": "Do not use F2=0 or no Poynting flux as an EM stress zero theorem",
            "because": "static Coulomb binding can be gravitationally relevant even when normal Poynting flux vanishes",
            "next_action": "score Maxwell stress-current norm, not scalar F2 alone",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3254_2_parent_route",
            "decision": "Keep parent EM owner route alive but do not spend this checkpoint pretending it is closed",
            "because": "unique F2 fails current corpus and current normalization/readout clauses remain unsigned",
            "next_action": "use finite Gram row while separately attacking unique-F2/current-owner theorem",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3254_0_3255",
            "selection": "selected_primary",
            "next_checkpoint": "3255-Y5-R2FR-EM-Gram-row-input-pack-or-static-Coulomb-stress-envelope-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_3255_EM_Gram_row_input_pack_or_static_Coulomb_stress_envelope.py",
            "objective": "Build the actual input pack for G_J[EM,EM]: choose A_ext/current norm/unit convention and derive a static Coulomb stress envelope or mark the exact source fields required.",
            "guardrail": "No Maxwell/local-GR/Newton claim unless the row has sourced E/B norms or a parent EM-owner zero theorem.",
            "valid_for_claim": "false",
        }
    ]


def markdown_doc(
    sources: list[dict[str, Any]],
    derivations: list[dict[str, Any]],
    gram: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    ctw_updates: list[dict[str, Any]],
    signature_locks: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 3254 - First component-current Gram row or parent signature clause lock under AX1090",
            f"Generated: `{RUN_UTC}`",
            "Private derivation checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, or public source-coupling success.",
            "## Summary\n"
            "- `3254` takes the `3253` Gram/eigenvalue fallback and fills the first real component slot: EM/Coulomb binding.\n"
            "- The exact component current is now `J_EM[tau] := star_eobs(T_EM_obs(tau,.))`, with `T_EM` the Maxwell Hilbert stress in the observed frame.\n"
            "- The first Gram entries are explicit: `G_J[EM,EM]=<J_EM,J_EM>_J` and `G_J[EM,d]=<J_EM,J_d>_J`.\n"
            "- This is a proper leap forward: future `C_Tw` work can fill a matrix row from field profiles or stress-current norms, rather than merely saying `MISSING_C_Tw`.\n"
            "- The parent theorem still does not close: unique Maxwell `F^2`, current normalization, readout/Hodge units, and no-alpha/binding vertices remain unsigned.\n"
            "- Guardrail: Poynting flux silence or `F^2=0` cannot be used to erase EM/Coulomb stress; static Coulomb energy can remain as source stress.",
            "## EM Stress Current Derivation",
            md_table(
                derivations,
                ["derivation_id", "object", "formal_statement", "derivation_gain", "current_status", "valid_for_claim"],
            ),
            "## EM Component Current Gram Row",
            md_table(
                gram,
                [
                    "gram_id",
                    "basis_component_id",
                    "component",
                    "residual_symbol",
                    "J_c",
                    "gram_entry",
                    "integral_contract",
                    "required_inputs",
                    "current_value",
                    "valid_for_claim",
                ],
            ),
            "## EM Current Norm Bound Rows",
            md_table(
                bounds,
                ["bound_id", "quantity", "bound_formula", "derivation", "required_inputs", "current_value", "valid_for_claim"],
            ),
            "## C_Tw Gram Matrix Update",
            md_table(
                ctw_updates,
                ["update_id", "target", "previous_status", "new_status", "effect", "valid_for_claim"],
            ),
            "## Parent Signature Clause Lock",
            md_table(
                signature_locks,
                ["lock_id", "parent_signature_clause", "status", "why_not_closed", "finite_fallback", "valid_for_claim"],
            ),
            "## Claim Gates",
            md_table(gates, ["claim_gate_id", "claim", "gate_pass", "reason", "claim_allowed"]),
            "## Decisions",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(
                next_target,
                ["next_id", "selection", "next_checkpoint", "next_script", "objective", "guardrail", "valid_for_claim"],
            ),
            "## Source Register",
            md_table(
                sources,
                ["source_id", "source_path", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"],
            ),
            "## Validation",
            md_table(validation, ["validation_id", "passed", "requirement", "evidence"]),
            "## Working Verdict\n"
            "`3254` does not close the coupling theorem, but it does something more useful than circling: it turns the EM/Coulomb piece of `C_Tw` into a concrete Maxwell-stress current row. The next move is now forced and practical: pick the arena/norm/unit convention and derive or source the static Coulomb/EM field envelope for `G_J[EM,EM]`.",
        ]
    ) + "\n"


def validation_rows(
    sources: list[dict[str, Any]],
    derivations: list[dict[str, Any]],
    gram: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, passed: bool, requirement: str, evidence_text: str) -> None:
        rows.append(
            {
                "validation_id": validation_id,
                "passed": bool_str(passed),
                "requirement": requirement,
                "evidence": evidence_text,
            }
        )

    source_paths_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" and row["evidence_hits"] != "NO_MATCH" for row in sources)
    add("VAL3254_0_sources_exist_parse_hit", source_paths_ok, "every cited source exists, parses, and has evidence hits", str(source_paths_ok))

    outputs_parse = all(csv_ok(path) for key, path in OUTPUTS.items() if key != "validation")
    add("VAL3254_1_output_csvs_parse", outputs_parse, "all 3254 output CSVs parse before validation write", str(outputs_parse))

    jem_def = any(row["derivation_id"] == "EMD3254_2_current_form" and "star_eobs" in row["formal_statement"] for row in derivations)
    add("VAL3254_2_jem_definition", jem_def, "J_EM current definition is written", str(jem_def))

    gram_self = any(row["gram_id"] == "GJ3254_EM_EM_SELF" and "G_J[EM,EM]" in row["gram_entry"] for row in gram)
    gram_cross = any(row["gram_id"] == "GJ3254_EM_ALL_CROSS" and "G_J[EM,d]" in row["gram_entry"] for row in gram)
    add("VAL3254_3_gram_entries", gram_self and gram_cross, "EM self and cross Gram entries are written", f"self={gram_self} cross={gram_cross}")

    bound_guard = any(row["bound_id"] == "EMB3254_3_static_coulomb_warning" and "GUARDRAIL_ACTIVE" in row["current_value"] for row in bounds)
    l2_bound = any(row["bound_id"] == "EMB3254_1_L2_current_bound" and "L4" in row["required_inputs"] for row in bounds)
    add("VAL3254_4_bounds_and_guard", bound_guard and l2_bound, "EM current bounds and static Coulomb guard are present", f"guard={bound_guard} l2_bound={l2_bound}")

    missing_markers = all(
        any(
            "MISSING_" in str(row.get(column, ""))
            for column in ["required_inputs", "current_value", "units", "source_path"]
        )
        or row.get("current_value") in {"BOUND_FORM_ONLY", "GUARDRAIL_ACTIVE"}
        for row in gram + bounds
    )
    nonclaim_rows = all(row["valid_for_claim"] == "false" for row in gram + bounds + derivations)
    add("VAL3254_5_nonclaim_missing_markers", missing_markers and nonclaim_rows, "rows preserve missing markers and remain nonclaim", f"missing={missing_markers} nonclaim={nonclaim_rows}")

    claim_allowed_false = all(row["claim_allowed"] == "false" for row in gates)
    numeric_blocked = any(row["claim_gate_id"] == "CG3254_2_EM_Gram_numeric" and row["gate_pass"] == "false" for row in gates)
    local_blocked = any(row["claim_gate_id"] == "CG3254_5_local_GR_Newton_Maxwell" and row["gate_pass"] == "false" for row in gates)
    add("VAL3254_6_claims_blocked", claim_allowed_false and numeric_blocked and local_blocked, "numeric EM Gram and local-GR/Newton/Maxwell claims remain blocked", f"allowed_false={claim_allowed_false} numeric={numeric_blocked} local={local_blocked}")

    output_scope_ok = all(str(path).startswith(str(ROOT)) for path in [DOC, *OUTPUTS.values()])
    add("VAL3254_7_output_scope", output_scope_ok, "all generated files stay in post-checkpoint-work", str(output_scope_ok))

    formalization_3254_files = []
    if FW.exists():
        formalization_3254_files = [path for path in FW.rglob("*3254*") if path.is_file()]
    add("VAL3254_8_formalization_untouched", not formalization_3254_files, "no 3254 files are written under formalization-workbench", f"file_count={len(formalization_3254_files)}")

    next_present = bool(next_rows())
    add("VAL3254_9_next_target", next_present, "3255 next target is selected", str(next_present))

    overall = all(row["passed"] == "true" for row in rows)
    add("VAL3254_OVERALL", overall, "3254 validation overall", "all required validation rows passed" if overall else "one or more validation rows failed")
    return rows


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_register()
    derivations = derivation_rows()
    gram = gram_rows()
    bounds = bound_rows()
    ctw_updates = ctw_update_rows()
    signature_locks = signature_lock_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["derivation"], derivations)
    write_csv(OUTPUTS["gram_row"], gram)
    write_csv(OUTPUTS["bounds"], bounds)
    write_csv(OUTPUTS["ctw_update"], ctw_updates)
    write_csv(OUTPUTS["signature_lock"], signature_locks)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    validation = validation_rows(sources, derivations, gram, bounds, gates)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(
        markdown_doc(sources, derivations, gram, bounds, ctw_updates, signature_locks, gates, decisions, next_target, validation),
        encoding="utf-8",
    )

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    overall = next(row for row in validation if row["validation_id"] == "VAL3254_OVERALL")
    print(f"{overall['validation_id']}={overall['passed']}")
    print(DOC)
    for name, path in OUTPUTS.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
