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
DOC = ROOT / "3375-Y5-R2FR-worldtube-source-measure-selector-or-Rworldtube-bound-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3375_SOURCE_REGISTER.csv",
    "selector_theorem": OUT / "P8_Y5_R2FR_3375_WORLDTUBE_SOURCE_MEASURE_SELECTOR_THEOREM.csv",
    "parent_contract": OUT / "P8_Y5_R2FR_3375_PARENT_ACTION_SELECTOR_CONTRACT.csv",
    "signature_audit": OUT / "P8_Y5_R2FR_3375_PARENT_SIGNATURE_AUDIT.csv",
    "residual_rows": OUT / "P8_Y5_R2FR_3375_RWORLDTUBE_BOUND_ROWS_NONCLAIM.csv",
    "numeric_scan": OUT / "P8_Y5_R2FR_3375_RWORLDTUBE_NUMERIC_SCAN.csv",
    "poynting_rows": OUT / "P8_Y5_R2FR_3375_POYNTING_SOURCE_WORLD_TUBE_PLACEMENT.csv",
    "countermodels": OUT / "P8_Y5_R2FR_3375_COUNTERMODEL_LEDGER.csv",
    "transfer_update": OUT / "P8_Y5_R2FR_3375_SOURCE_TRANSFER_UPDATE_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3375_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3375_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3375_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3375_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3375_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3375_0_3374_doc", ROOT / "3374-Y5-R2FR-topological-Hilbert-equality-or-Req-bound-under-AX1090.md", "3374 same-object equality handoff"),
    ("SRC3375_1_3374_next", OUT / "P8_Y5_R2FR_3374_NEXT_TARGET.csv", "3374 selected worldtube/source-measure selector"),
    ("SRC3375_2_3374_same_object", OUT / "P8_Y5_R2FR_3374_SAME_OBJECT_LEMMA_ATTEMPT.csv", "same-object lemma requiring parent worldtube ownership"),
    ("SRC3375_3_3374_signature", OUT / "P8_Y5_R2FR_3374_PARENT_SIGNATURE_AUDIT.csv", "3374 missing source signatures"),
    ("SRC3375_4_3372_doc", ROOT / "3372-Y5-R2FR-Hilbert-source-transfer-chain-or-first-tail-numeric-row-under-AX1090.md", "Hilbert source-transfer chain"),
    ("SRC3375_5_parent_worldtube_clauses", OUT / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv", "parent worldtube/source-measure glue clauses"),
    ("SRC3375_6_worldtube_source_theorem", OUT / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv", "worldtube source-measure theorem"),
    ("SRC3375_7_worldtube_source_proof", OUT / "P8_WORLDTUBE_SOURCE_MEASURE_PROOF_SKETCH.csv", "worldtube source-measure proof sketch"),
    ("SRC3375_8_parent_action_contract", OUT / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv", "parent action source-worldtube contract"),
    ("SRC3375_9_hilbert_glue_attempt", OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv", "Hilbert worldtube glue theorem attempt"),
    ("SRC3375_10_hilbert_glue_cert", OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv", "Hilbert worldtube certificate gaps"),
    ("SRC3375_11_selector_coupling_2577", OUT / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_WORLDTUBE_HILBERT_COUPLING_SELECTOR_THEOREM.csv", "coupling/source-selector theorem"),
    ("SRC3375_12_htau_2938", OUT / "P8_Y5_R2FR_2938_HTAU_WORLDTUBE_SOURCE_MEASURE_THEOREM_ATTEMPT.csv", "Hamiltonian source-measure identity attempt"),
    ("SRC3375_13_matter_descent_2611", OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv", "matter descent/worldtube owner audit"),
    ("SRC3375_14_no_shadow_2503", OUT / "P8_Y5_NO_SHADOW_2503_WORLDTUBE_HILBERT_SELECTOR_THEOREM.csv", "no-shadow worldtube Hilbert selector"),
    ("SRC3375_15_gm_2595_components", OUT / "P8_Y5_GM_TRANSFER_2595_COMPONENT_ROWS.csv", "GM source-transfer residual components"),
    ("SRC3375_16_boundary_status", OUT / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv", "boundary/reference/M_H_ref first-row status"),
    ("SRC3375_17_poynting_3249", OUT / "P8_Y5_R2FR_3249_SOURCE_WORLDTUBE_POYNTING_BOUND_ROW.csv", "Poynting source-worldtube placement"),
    ("SRC3375_18_flux_norm_3250", OUT / "P8_Y5_R2FR_3250_SOURCE_WORLDTUBE_FLUX_NORM_ROW.csv", "Poynting/source-worldtube flux norm row"),
]

NUMERIC_SCAN_TARGETS = [
    ("R_worldtube_glue", OUT / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv", "worldtube glue theorem rows"),
    ("R_source_measure", OUT / "P8_Y5_R2FR_2938_HTAU_WORLDTUBE_SOURCE_MEASURE_THEOREM_ATTEMPT.csv", "Hamiltonian source-measure residual"),
    ("R_Wsupport", OUT / "P8_Y5_R2FR_3249_SOURCE_WORLDTUBE_POYNTING_BOUND_ROW.csv", "source support selector residual"),
    ("M_H_ref", OUT / "P8_Y5_GM_TRANSFER_2595_COMPONENT_ROWS.csv", "positive same-frame source denominator"),
    ("B_zero_flux", OUT / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv", "boundary/reference flux row"),
    ("Poynting_flux_norm", OUT / "P8_Y5_R2FR_3250_SOURCE_WORLDTUBE_FLUX_NORM_ROW.csv", "EM Poynting flux/source-worldtube row"),
]

BAD_STATUS_TOKENS = (
    "MISSING",
    "NOT_COMPUTED",
    "NOT_DERIVED",
    "NOT_YET",
    "BLOCKED",
    "UNSIGNED",
    "NONCLAIM",
    "TEMPLATE",
    "FORM_ONLY",
    "CONTRACT_ONLY",
    "CONDITIONAL",
    "FALSE",
)


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def parse_csv(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            list(csv.DictReader(handle))
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def parse_text(path: Path) -> tuple[bool, str]:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, path, role in LOCAL_SOURCES:
        exists = path.exists()
        parse_ok = False
        parse_error = ""
        if exists:
            parse_ok, parse_error = parse_csv(path) if path.suffix.lower() == ".csv" else parse_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "parse_ok": bool_text(parse_ok),
                "role": role,
                "parse_error": parse_error,
                "valid_for_claim": "false",
            }
        )
    return rows


def selector_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "WSS3375_0_unique_observed_matter_frame",
            "claim_piece": "observed source frame is selected by the parent matter action",
            "statement": "Take S_matter = S_matter[psi_m, e_obs(q(Phi)), omega[e_obs], theta(q(Phi))] with no second representative metric/coframe in the ordinary source readout.",
            "derivation": "The Hilbert source current is then the functional derivative of the same action used by clocks and rods: J_H[tau] := tau contracted with delta S_matter/delta e_obs. This makes the source-current object action-owned rather than orbit-fit-owned.",
            "current_status": "VALID_CONDITIONAL_SELECTOR_LEMMA_NOT_PARENT_SIGNED",
            "residual_if_missing": "R_frame_source_split",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "WSS3375_1_worldtube_support_selector",
            "claim_piece": "worldtube is fixed before empirical readout",
            "statement": "Define W_source := closure(supp J_H[tau]) on a compact regular support branch, with linked S1,S2 chosen in the exterior of this same W_source.",
            "derivation": "If J_H is already a parent functional of e_obs and tau, then changing an orbital, clock, PPN, or galaxy readout parameter cannot change W_source unless that parameter changes the parent source current itself. The support drift is therefore a named residual, not hidden freedom.",
            "current_status": "VALID_CONDITIONAL_SELECTOR_LEMMA_NOT_PARENT_SIGNED",
            "residual_if_missing": "R_Wsupport",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "WSS3375_2_parent_Noether_Hamiltonian_charge",
            "claim_piece": "source measure is the dressed Hamiltonian/Noether charge",
            "statement": "For covariant L_parent, J_tau = Theta(Phi,L_tau Phi)-i_tau L_parent = dQ_tau + C_tau on shell, and M_H[S] := N_G^{-1} int_S Q_tau - H_ref is fixed before readout.",
            "derivation": "The active gravitational source is not bare rest mass. It is the dressed charge that includes stress, binding, EM/Poynting flux bookkeeping, boundary reference, and extra-sector residuals according to the same parent variation.",
            "current_status": "STANDARD_CPS_ROUTE_CONDITIONAL_MTS_INPUTS_OPEN",
            "residual_if_missing": "R_source_measure;R_Htau_integrability;R_reference_selector",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "WSS3375_3_exterior_Gauss_worldtube_glue",
            "claim_piece": "surface charge and source worldtube read the same mass",
            "statement": "In A = ext(W_source) between linked surfaces S1,S2, M_H[S2]-M_H[S1] = int_A(C_EH + C_extra + C_projector + C_boundary + C_EM_exchange).",
            "derivation": "If the annulus is source-free and every non-EH/projector/boundary/EM exchange term is zero or bounded, then M_H[S] is independent of linking surface and equals the selected source measure up to the retained residual.",
            "current_status": "VALID_CONDITIONAL_GAUSS_IDENTITY_NOT_CLOSED_FOR_MTS",
            "residual_if_missing": "R_worldtube_glue",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "WSS3375_4_topological_representative_now_owned",
            "claim_piece": "topological mass current becomes the same Hilbert object",
            "statement": "Set J_M_top := M_source[W_source] omega_W, where omega_W is the parent-owned Poincare-dual representative of the selected Hilbert worldtube and int_link omega_W=1.",
            "derivation": "This is the missing bridge from 3374: topology is no longer an independent conserved label; it is the representative of the Hilbert/Noether source measure selected before readout.",
            "current_status": "VALID_CONDITIONAL_BRIDGE_REQUIRES_PD_AND_REFERENCE_SIGNATURES",
            "residual_if_missing": "R_eq_integral;epsilon_wrong_conserved_object",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "WSS3375_5_selector_verdict",
            "claim_piece": "worldtube/source selector theorem",
            "statement": "If WSS3375_0 through WSS3375_4 are parent-signed in one q/e_obs/tau/N_G/H_ref branch, then W_source=supp(delta S_matter/delta e_obs), Q_M is the Hilbert/Noether source measure before readout, and R_worldtube_glue=0.",
            "derivation": "The route is derivable as a conditional theorem. The current corpus has the contract and exact support/Noether/Gauss chain, but not the explicit parent Lagrangian, integrability, reference, boundary, extra-sector silence, or positive M_H_ref signatures needed to claim it.",
            "current_status": "VALID_CONDITIONAL_THEOREM_NOT_CURRENT_CLAIM",
            "residual_if_missing": "R_worldtube_glue/M_H_ref",
            "valid_for_claim": "false",
        },
    ]


def parent_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "contract_id": "WSC3375_0_parent_action_line",
            "required_contract": "single covariant parent action",
            "exact_requirement": "S_parent[Phi,psi_m] = int L_grav(Phi,dPhi) + L_matter(psi_m,e_obs(q(Phi)),omega[e_obs],theta(q(Phi))) + dB_ref, with all source couplings fixed before readout.",
            "forbidden_shortcut": "introducing a source mask, fit mass, galaxy/orbital readout, or hidden representative metric after data are known",
            "closes": "source-current ownership;anti-circularity",
            "current_status": "CONTRACT_EXACT_PARENT_LAGRANGIAN_MISSING",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "WSC3375_1_eobs_tau_lock",
            "required_contract": "same observed frame and time generator",
            "exact_requirement": "e_obs, tau, surface orientation, source support, and clock/orbital readout branch are fixed together by q(Phi), not separately fitted.",
            "forbidden_shortcut": "using one frame to define mass and another to read local acceleration or clock rate",
            "closes": "R_frame_source_split;R_Wsupport",
            "current_status": "NEEDS_PARENT_SIGNATURE",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "WSC3375_2_Hamiltonian_measure_not_bare_mass",
            "required_contract": "dressed source measure",
            "exact_requirement": "M_source[W] is H_tau[S]-H_ref minus explicit exterior residuals, not int rho_rest unless the parent proves the dressing terms vanish.",
            "forbidden_shortcut": "equating active gravitational mass to bare rest mass or luminous mass without binding/field/reference terms",
            "closes": "wrong mass measure;measured GM circularity",
            "current_status": "DEFINITION_CORRECTION_READY_NOT_NUMERIC",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "WSC3375_3_EM_Poynting_placement",
            "required_contract": "Poynting flux is either public Hilbert stress or explicit residual",
            "exact_requirement": "If EM is in L_matter[e_obs,A], T_EM and the Poynting vector are part of J_H/H_tau; if EM uses a hidden Hodge/current normalization, retain R_Poynting_worldtube.",
            "forbidden_shortcut": "allowing wave/Poynting energy to alter source mass while omitting it from the source measure",
            "closes": "EM source-current leakage",
            "current_status": "PLACEMENT_DERIVED_INPUT_NORMS_MISSING",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "WSC3375_4_fixed_normalization",
            "required_contract": "N_G/G_ref/kappa_MTS/source-current scale fixed before readout",
            "exact_requirement": "The same coefficient normalizes H_tau, weak-field Gauss law, Newtonian acceleration, and PPN expansion.",
            "forbidden_shortcut": "using source coupling to absorb residuals after orbital comparison",
            "closes": "delta_kappa;delta_ellJ;M_H_ref denominator",
            "current_status": "COUPLING_BASELINE_NOT_DERIVED",
            "valid_for_claim": "false",
        },
    ]


def signature_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "SIG3375_0_parent_Lagrangian",
            "required_signature": "explicit L_parent and symplectic potential Theta",
            "evidence": "PAC537_0 and HWS2938_1 remain contract/open rows; no full MTS parent Lagrangian variation is present",
            "current_status": "MISSING_PARENT_SIGNATURE",
            "blocks": "WSS3375_2;WSC3375_0",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SIG3375_1_unique_eobs_matter_descent",
            "required_signature": "matter descends only through e_obs(q(Phi)) and public matter fields",
            "evidence": "PAC537_1, matter descent 2611, no-shadow 2503, and 3370 support the contract but do not parent-sign every matter/readout sector",
            "current_status": "PARTIAL_CONTRACT_NOT_GLOBAL_SIGNATURE",
            "blocks": "WSS3375_0;WSS3375_1",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SIG3375_2_support_regular_compact",
            "required_signature": "compact regular W_source support and linked surfaces are action-selected before readout",
            "evidence": "WSC2577_1 and HWS2938_4 give exact selector definition but current status is WORLDTUBE_OWNER_OPEN",
            "current_status": "SELECTOR_LEMMA_OPEN",
            "blocks": "R_Wsupport",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SIG3375_3_Htau_integrability_reference",
            "required_signature": "H_tau integrable with source-blind H_ref",
            "evidence": "HWS2938_2 and HWS2938_3 mark integrability and reference selector unsigned",
            "current_status": "MISSING_INTEGRABILITY_AND_REFERENCE_LOCK",
            "blocks": "R_Htau_integrability;R_reference_selector;M_H_ref",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SIG3375_4_exterior_residual_silence",
            "required_signature": "nonEH, projector, boundary, domain, memory, EM/Poynting and frame exchange terms zero or bounded in A",
            "evidence": "3371/3374 retain hidden-tail, boundary, projector, and extra-charge silence rows; 3249/3250 place Poynting but lack norms",
            "current_status": "CHANNEL_SILENCE_OPEN",
            "blocks": "R_worldtube_glue;R_Poynting_worldtube;B_zero_flux",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SIG3375_5_PD_topological_representative",
            "required_signature": "omega_W is the PD representative of the same selected Hilbert worldtube",
            "evidence": "3374 proves same-class lemma only conditionally; PD/source-worldtube signature is still missing",
            "current_status": "MISSING_PARENT_SIGNATURE",
            "blocks": "R_eq_integral;wrong conserved object guard",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SIG3375_6_same_normalization",
            "required_signature": "same N_G/G_ref/kappa/source-current scale in H_tau, Newton, and PPN",
            "evidence": "WSC2577_6 and PAC537_8 name the coupling baseline, but current status is not derived/not reached",
            "current_status": "COUPLING_BASELINE_OPEN",
            "blocks": "Newton/local-GR calibrated source coupling",
            "valid_for_claim": "false",
        },
    ]


def residual_rows() -> list[dict[str, str]]:
    return [
        {
            "row_id": "RWB3375_0_R_worldtube_glue",
            "symbol": "R_worldtube_glue",
            "definition": "finite exterior annulus mismatch between parent Hamiltonian surface charge and selected Hilbert worldtube source measure",
            "bound_formula": "|int_A(C_extra+C_projector+C_boundary+C_EM_exchange+C_frame)|/|M_H_ref|",
            "required_inputs": "system_id,S1,S2,W_source,tau,e_obs,C_terms,M_H_ref,units,source_path",
            "current_status": "THEOREM_CONDITIONAL_NUMERIC_MISSING",
            "test_arena": "Newton;PPN;orbital;clock;R10",
            "valid_for_claim": "false",
        },
        {
            "row_id": "RWB3375_1_R_Wsupport",
            "symbol": "R_Wsupport",
            "definition": "support drift of W_source under readout/coupling variation",
            "bound_formula": "dist_support(W_source(theta_readout), W_source(parent))/L_source or distributional ||D_readout J_H||",
            "required_inputs": "support topology,J_H variation,tau/e_obs lock,regular support certificate",
            "current_status": "SCHEMA_READY_SUPPORT_METRIC_MISSING",
            "test_arena": "source selection;WEP;local-GR",
            "valid_for_claim": "false",
        },
        {
            "row_id": "RWB3375_2_R_source_measure",
            "symbol": "R_source_measure",
            "definition": "difference between dressed Hamiltonian/Noether mass and any proposed interior source integral",
            "bound_formula": "|M_source[W] - (H_tau[S]-H_ref)|/|M_H_ref|",
            "required_inputs": "H_tau,H_ref,interior rho_H,field/binding dressing,B_zero_flux,M_H_ref",
            "current_status": "FORMULA_READY_NUMERIC_MISSING",
            "test_arena": "Newtonian source mass;PPN;orbital systems",
            "valid_for_claim": "false",
        },
        {
            "row_id": "RWB3375_3_R_Htau_integrability",
            "symbol": "R_Htau_integrability",
            "definition": "covariant phase space curl/path dependence in the Hamiltonian source charge",
            "bound_formula": "|int_S i_tau omega_total(delta1,delta2)+curl(delta H_ref)|/|M_H_ref|",
            "required_inputs": "Theta,Q_tau,omega_total,tau,surface lock,H_ref variation,M_H_ref",
            "current_status": "INPUTS_MISSING_NONCLAIM",
            "test_arena": "Hamiltonian charge;source normalization",
            "valid_for_claim": "false",
        },
        {
            "row_id": "RWB3375_4_R_reference_selector",
            "symbol": "R_reference_selector",
            "definition": "source-dependence of the reference background or subtraction",
            "bound_formula": "|D_source H_ref|/|M_H_ref|",
            "required_inputs": "reference selector Sigma_ref,H_ref,source labels,derivative audit",
            "current_status": "REFERENCE_LOCK_UNSIGNED",
            "test_arena": "finite mass;clock;orbital",
            "valid_for_claim": "false",
        },
        {
            "row_id": "RWB3375_5_R_Poynting_worldtube",
            "symbol": "R_Poynting_worldtube",
            "definition": "EM wave/Poynting energy crossing the selected source-worldtube boundary not already included in public Hilbert stress",
            "bound_formula": "mu0^-1 ||E_T||_L2(B)||B_T||_L2(B)/|M_H_ref| plus collar T_EM(u,n) term",
            "required_inputs": "unit system,E/B norms,boundary measure,orientation,public-Hodge certificate,M_H_ref",
            "current_status": "PLACED_BUT_INPUT_NORMS_MISSING",
            "test_arena": "EM;Poynting vector;Maxwell stress;source coupling",
            "valid_for_claim": "false",
        },
        {
            "row_id": "RWB3375_6_M_H_ref",
            "symbol": "M_H_ref",
            "definition": "positive same-frame Hamiltonian source mass denominator",
            "bound_formula": "M_H_ref := H_tau[S_refed] in the same tau/e_obs/N_G branch, with M_H_ref>0",
            "required_inputs": "H_tau,H_ref,N_G,tau,e_obs,source system,units,positivity certificate",
            "current_status": "MISSING_DENOMINATOR",
            "test_arena": "all normalized local residuals",
            "valid_for_claim": "false",
        },
    ]


def row_mentions_symbol(row: dict[str, str], symbol: str) -> bool:
    haystack = " ".join(str(value) for value in row.values()).lower()
    symbol_l = symbol.lower()
    if symbol_l in haystack:
        return True
    aliases = {
        "R_worldtube_glue": ("worldtube glue", "M_source[W]", "exterior annulus"),
        "R_source_measure": ("source measure", "H_tau", "M_source"),
        "R_Wsupport": ("support", "W_source"),
        "M_H_ref": ("M_H_ref", "H_ref"),
        "B_zero_flux": ("B_zero", "boundary"),
        "Poynting_flux_norm": ("Poynting", "S_EM", "T_EM"),
    }
    return any(alias.lower() in haystack for alias in aliases.get(symbol, ()))


def row_claimish(row: dict[str, str]) -> bool:
    text = " ".join(str(value) for value in row.values()).upper()
    valid_fields = [
        str(row.get("valid_for_claim", "")).lower(),
        str(row.get("claim_allowed", "")).lower(),
        str(row.get("valid_prediction_row", "")).lower(),
        str(row.get("score_ready", "")).lower(),
    ]
    has_positive_flag = any(value == "true" for value in valid_fields)
    has_bad_token = any(token in text for token in BAD_STATUS_TOKENS)
    return has_positive_flag and not has_bad_token


def numeric_scan_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, (symbol, path, role) in enumerate(NUMERIC_SCAN_TARGETS):
        csv_rows = read_csv_rows(path)
        matching = [row for row in csv_rows if row_mentions_symbol(row, symbol)]
        claimish = [row for row in matching if row_claimish(row)]
        status_excerpt = "NO_MATCHING_ROWS"
        if matching:
            status_excerpt = " | ".join(
                ";".join(
                    str(row.get(key, ""))
                    for key in ("status", "current_status", "MTS_current_status", "derivation_status", "computed_value")
                    if row.get(key, "")
                )
                for row in matching[:3]
            )
            if not status_excerpt:
                status_excerpt = "MATCHING_ROWS_NONCLAIM_OR_SCHEMA_ONLY"
        rows.append(
            {
                "scan_id": f"SCAN3375_{index}_{symbol}",
                "symbol": symbol,
                "source_path": str(path),
                "source_exists": bool_text(path.exists()),
                "matching_rows": str(len(matching)),
                "claim_valid_rows": str(len(claimish)),
                "status_excerpt": status_excerpt,
                "scan_result": "SOURCE_BACKED_NUMERIC_ROW_FOUND" if claimish else "NO_SOURCE_BACKED_NUMERIC_ROW",
                "valid_for_claim": "false",
            }
        )
    return rows


def poynting_rows() -> list[dict[str, str]]:
    return [
        {
            "placement_id": "POY3375_0_public_EM_branch",
            "branch": "Maxwell/EM action uses public e_obs/Hodge star",
            "source_measure_effect": "Poynting vector and EM stress are already part of the Hilbert current and Hamiltonian charge",
            "formula": "J_H[tau] includes T_EM(tau,n); source flux term is accounted inside M_source[W]",
            "current_status": "CONDITIONAL_PLACEMENT_OK_INPUT_NORMS_STILL_MISSING",
            "residual": "R_Poynting_worldtube=0 only after public-Hodge and boundary flux signatures",
            "valid_for_claim": "false",
        },
        {
            "placement_id": "POY3375_1_hidden_EM_branch",
            "branch": "EM wave/current/Hodge normalization uses hidden or second frame structure",
            "source_measure_effect": "Poynting flux becomes an explicit source-worldtube exchange residual",
            "formula": "R_Poynting_worldtube >= ||S_EM dot n||_L1(B)/|M_H_ref| plus collar stress term",
            "current_status": "NONCLAIM_BOUND_ROW_REQUIRED",
            "residual": "R_Poynting_worldtube retained",
            "valid_for_claim": "false",
        },
        {
            "placement_id": "POY3375_2_theory_policy",
            "branch": "do not ignore wave energy",
            "source_measure_effect": "The Poynting vector is not an optional add-on; it must either be included in T_EM/H_tau or explicitly bounded",
            "formula": "M_source[W] = M_matter + M_EM + M_binding + M_boundary + residuals",
            "current_status": "POLICY_LOCK_FOR_FUTURE_DERIVATIONS",
            "residual": "blocks Maxwell/source-coupling claims if omitted",
            "valid_for_claim": "false",
        },
    ]


def countermodel_rows() -> list[dict[str, str]]:
    return [
        {
            "countermodel_id": "CM3375_0_two_metric_readout",
            "weak_premise": "source current and local readout use the same frame",
            "construction": "matter source support is defined with e_source while clocks/orbits use e_obs",
            "what_breaks": "W_source can be fixed but not the worldtube seen by the local acceleration/clock channel",
            "repair": "single e_obs matter descent or explicit R_frame_source_split",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM3375_1_bare_rest_mass_confusion",
            "weak_premise": "interior rest mass equals active gravitational source",
            "construction": "binding energy, EM/Poynting flux, pressure, boundary reference or extra-sector energy contributes to H_tau",
            "what_breaks": "M_source[W] != int rho_rest dV",
            "repair": "define source measure as dressed Hamiltonian charge with residual rows",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM3375_2_source_mask_after_fit",
            "weak_premise": "worldtube support is parent fixed",
            "construction": "support/domain cutoff is chosen after an orbital or PPN residual is inspected",
            "what_breaks": "worldtube theorem becomes a fitted mask",
            "repair": "W_source=closure(supp delta S_matter/delta e_obs) before readout plus R_Wsupport if unstable",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM3375_3_reference_subtraction_carries_source",
            "weak_premise": "Hamiltonian reference is source blind",
            "construction": "H_ref changes with source mass, radius, composition, or tau branch",
            "what_breaks": "finite surface mass is shifted by bookkeeping",
            "repair": "reference selector lock or R_reference_selector",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM3375_4_poynting_hidden_leak",
            "weak_premise": "EM/waves do not affect source measure",
            "construction": "Poynting flux crosses the source boundary through a hidden Hodge/current normalization not included in public T_EM",
            "what_breaks": "Maxwell/source coupling and local mass conservation disagree",
            "repair": "public EM Hilbert stress branch or R_Poynting_worldtube bound",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM3375_5_coupling_absorption",
            "weak_premise": "same source charge automatically calibrates Newtonian G",
            "construction": "kappa_MTS or ell_J is adjusted after source transfer to match GM",
            "what_breaks": "theory derives conservation but not the measured inverse-square coefficient",
            "repair": "fixed N_G/G_ref/kappa/source-current normalization before readout",
            "valid_for_claim": "false",
        },
    ]


def transfer_update_rows() -> list[dict[str, str]]:
    return [
        {
            "update_id": "STU3375_0_if_selector_signed",
            "condition": "W_source=supp(delta S_matter/delta e_obs) and M_source[W]=H_tau[S]-H_ref are parent-signed",
            "source_transfer_effect": "wrong-worldtube and wrong-source-measure guards drop from the 3372/3374 source-transfer chain",
            "remaining_blockers": "boundary zero flux;PD representative;M_H_ref positivity;fixed G/kappa;PPN expansion",
            "current_status": "CONDITIONAL_BRANCH_NOT_CURRENT_CLAIM",
            "valid_for_claim": "false",
        },
        {
            "update_id": "STU3375_1_current_branch",
            "condition": "current MTS corpus",
            "source_transfer_effect": "R_worldtube_glue, R_source_measure, R_Wsupport, R_reference_selector, R_Poynting_worldtube and M_H_ref stay explicit",
            "remaining_blockers": "parent Lagrangian, Theta/Q_tau, integrability, reference, extra-sector silence and coupling baseline",
            "current_status": "TRANSFER_RESIDUAL_RETAINED",
            "valid_for_claim": "false",
        },
        {
            "update_id": "STU3375_2_practical_gain",
            "condition": "3375 selector theorem adopted as target contract",
            "source_transfer_effect": "future derivations must either use the same Hilbert/Hamiltonian source measure or produce a bound row; no hidden mass-source switches",
            "remaining_blockers": "exact parent action and numeric rows",
            "current_status": "ANTI_CIRCULARITY_GATE_SHARPENED",
            "valid_for_claim": "false",
        },
    ]


def runner_rows() -> list[dict[str, str]]:
    return [
        {
            "run_id": "RUN3375_0_support_selector",
            "test": "derive W_source from the parent Hilbert current",
            "result": "PASS_CONDITIONAL_LEMMA",
            "detail": "W_source=closure(supp J_H[tau]) is exact once J_H is the unique e_obs matter functional derivative",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3375_1_source_measure",
            "test": "identify active source mass with parent Hamiltonian/Noether charge",
            "result": "PASS_CONDITIONAL_DEFINITION_CORRECTION",
            "detail": "the active source is dressed H_tau-H_ref, not bare rest mass; current MTS lacks Theta/Q_tau/H_ref signatures",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3375_2_current_parent_signature",
            "test": "promote worldtube/source-measure selector in current corpus",
            "result": "BLOCKED_NOT_PARENT_SIGNED",
            "detail": "explicit parent action, integrable H_tau, source-blind reference, boundary flux, extra-sector silence and coupling normalization are open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3375_3_numeric_scan",
            "test": "find source-backed R_worldtube/M_H_ref or Poynting/source rows",
            "result": "NO_NUMERIC_ROW_FOUND",
            "detail": "current rows are formula/contract/conditional/nonclaim; no positive same-frame M_H_ref row is available",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3375_4_local_GR",
            "test": "use selector theorem to claim Newton/local GR",
            "result": "REFUSED",
            "detail": "selector theorem is a necessary bridge but boundary zero, weak-field normalization and PPN residuals remain",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def gate_rows(source_ok: bool) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE3375_0_sources",
            "claim": "all required 3375 source paths exist and parse",
            "gate_pass": bool_text(source_ok),
            "reason": "source register validates every cited local input",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3375_1_worldtube_selector",
            "claim": "W_source is parent-owned before readout",
            "gate_pass": "false",
            "reason": "conditional support selector is clean but parent action/e_obs/matter descent signatures remain incomplete",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3375_2_source_measure",
            "claim": "Q_M/M_source is the same Hilbert/Noether source measure",
            "gate_pass": "false",
            "reason": "H_tau integrability, Theta/Q_tau extraction, reference lock and M_H_ref are not signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3375_3_poynting",
            "claim": "Poynting/EM stress is harmless for source coupling",
            "gate_pass": "false",
            "reason": "public EM branch is placed, but flux norms and public-Hodge/source-worldtube inputs are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3375_4_Rworldtube_bound",
            "claim": "R_worldtube_glue/M_H_ref bound row is score-ready",
            "gate_pass": "false",
            "reason": "numeric scan finds no source-backed R_worldtube or positive M_H_ref row",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3375_5_Newton_local_GR",
            "claim": "Newton/local-GR source coupling is established",
            "gate_pass": "false",
            "reason": "selector theorem is conditional and coupling/boundary/PPN gates remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC3375_0_progress",
            "decision": "The source worldtube problem has a derivable route, not just a closure axiom.",
            "because": "define the source from the same Hilbert functional derivative and Hamiltonian charge used by the parent action; then W_source and M_source are selected before readout.",
            "next_action": "demand an explicit parent action/e_obs/tau/H_ref branch or retain R_worldtube_glue",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3375_1_key_correction",
            "decision": "The active source measure should be dressed Hamiltonian mass, not bare rest mass.",
            "because": "binding energy, EM/Poynting stress, pressure, boundary reference and extra-sector dressing are exactly where source-coupling mistakes can hide.",
            "next_action": "carry M_source[W]=H_tau-H_ref-residuals into the Newton/PPN branch",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3375_2_current_status",
            "decision": "Current MTS still cannot claim local GR source coupling.",
            "because": "parent Lagrangian, integrability, reference lock, boundary zero, extra-sector silence, Poynting inputs, and G/kappa normalization remain unsigned or numeric-missing.",
            "next_action": "keep all residual rows nonclaim and attack boundary zero/reference lock next",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3376-Y5-R2FR-boundary-zero-flux-or-Bzero-first-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3376_boundary_zero_flux_or_Bzero_first_row.py",
            "objective": "prove exact/reference term zero linked-surface flux or stage B_zero_flux/M_H_ref as the first source-transfer boundary row",
            "why_next": "3375 pins down the source selector conditionally; boundary/reference flux is now the sharpest finite-shell obstruction before source transfer can promote",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3377-Y5-R2FR-weak-field-source-normalization-or-Gref-kappa-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3377_weak_field_source_normalization_or_Gref_kappa_bound.py",
            "objective": "derive the same N_G/G_ref/kappa/source-current scale in H_tau, Poisson/Newton and PPN readout, or stage delta_kappa/delta_ellJ rows",
            "why_next": "after source ownership and boundary flux, the remaining local-GR hinge is calibration of the same charge into the inverse-square coefficient",
            "valid_for_claim": "false",
        },
    ]


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    offenders: list[str] = []
    for path in paths:
        if not path.exists() or path.suffix.lower() != ".csv":
            continue
        for index, row in enumerate(read_csv_rows(path), start=2):
            if "valid_for_claim" in row and row["valid_for_claim"].strip().lower() != "false":
                offenders.append(f"{path.name}:line{index}:{row['valid_for_claim']}")
    return not offenders, "; ".join(offenders)


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in rows_by_name["source_register"])
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation" and path.suffix.lower() == ".csv"]
    parse_results = [parse_csv(path)[0] for path in output_csvs if path.exists()]
    flags_ok, flag_detail = all_claim_flags_false(output_csvs)
    formalization_hits = list(FW.rglob("*3375*")) if FW.exists() else []
    theorem_ids = {row["theorem_id"] for row in rows_by_name["selector_theorem"]}
    contract_ids = {row["contract_id"] for row in rows_by_name["parent_contract"]}
    audit_ids = {row["audit_id"] for row in rows_by_name["signature_audit"]}
    residual_symbols = {row["symbol"] for row in rows_by_name["residual_rows"]}
    scan_results = {row["scan_result"] for row in rows_by_name["numeric_scan"]}
    placement_ids = {row["placement_id"] for row in rows_by_name["poynting_rows"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    checks = [
        ("VAL3375_0_sources_exist_parse", "all cited local source paths exist and parse", source_ok, ""),
        ("VAL3375_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3375_2_selector_theorem", "selector theorem covers e_obs, W_source, H_tau, Gauss glue, topological ownership and verdict", {"WSS3375_0_unique_observed_matter_frame", "WSS3375_1_worldtube_support_selector", "WSS3375_2_parent_Noether_Hamiltonian_charge", "WSS3375_3_exterior_Gauss_worldtube_glue", "WSS3375_4_topological_representative_now_owned", "WSS3375_5_selector_verdict"}.issubset(theorem_ids), ""),
        ("VAL3375_3_parent_contract", "parent contract covers action line, e_obs/tau lock, dressed source, Poynting placement and normalization", {"WSC3375_0_parent_action_line", "WSC3375_1_eobs_tau_lock", "WSC3375_2_Hamiltonian_measure_not_bare_mass", "WSC3375_3_EM_Poynting_placement", "WSC3375_4_fixed_normalization"}.issubset(contract_ids), ""),
        ("VAL3375_4_signature_audit", "signature audit covers parent action, e_obs, support, H_tau/reference, exterior silence, PD and normalization", {"SIG3375_0_parent_Lagrangian", "SIG3375_1_unique_eobs_matter_descent", "SIG3375_2_support_regular_compact", "SIG3375_3_Htau_integrability_reference", "SIG3375_4_exterior_residual_silence", "SIG3375_5_PD_topological_representative", "SIG3375_6_same_normalization"}.issubset(audit_ids), ""),
        ("VAL3375_5_residual_rows", "residual rows cover worldtube, support, source measure, Hamiltonian, reference, Poynting and M_H_ref", {"R_worldtube_glue", "R_Wsupport", "R_source_measure", "R_Htau_integrability", "R_reference_selector", "R_Poynting_worldtube", "M_H_ref"}.issubset(residual_symbols), ""),
        ("VAL3375_6_numeric_scan_blocks_claim", "numeric scan finds no source-backed numeric rows", scan_results == {"NO_SOURCE_BACKED_NUMERIC_ROW"}, ""),
        ("VAL3375_7_poynting_placed", "Poynting branch is placed as public Hilbert stress or explicit residual", {"POY3375_0_public_EM_branch", "POY3375_1_hidden_EM_branch", "POY3375_2_theory_policy"}.issubset(placement_ids), ""),
        ("VAL3375_8_countermodels", "countermodels cover two-frame, bare-mass, post-fit mask, reference, Poynting and coupling absorption failures", len(rows_by_name["countermodels"]) >= 6, ""),
        ("VAL3375_9_runner_blocks_claim", "runner marks conditional lemmas but blocks current claim", "PASS_CONDITIONAL_LEMMA" in runner_results and "PASS_CONDITIONAL_DEFINITION_CORRECTION" in runner_results and "BLOCKED_NOT_PARENT_SIGNED" in runner_results and "NO_NUMERIC_ROW_FOUND" in runner_results and "REFUSED" in runner_results, ""),
        ("VAL3375_10_gates_block_local", "promotion gates block selector, source measure, Poynting, Rworldtube bound and local GR", gate_map.get("GATE3375_1_worldtube_selector") == "false" and gate_map.get("GATE3375_2_source_measure") == "false" and gate_map.get("GATE3375_3_poynting") == "false" and gate_map.get("GATE3375_4_Rworldtube_bound") == "false" and gate_map.get("GATE3375_5_Newton_local_GR") == "false", ""),
        ("VAL3375_11_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3375_12_next_target", "next target moves to boundary zero/reference or weak-field source normalization", rows_by_name["next"][0]["target_id"].startswith("3376-Y5-R2FR-boundary-zero-flux"), ""),
        ("VAL3375_13_write_scope_outside_formalization", "no 3375 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
    ]
    checks.append(("VAL3375_14_overall", "3375 validation overall", all(passed for _, _, passed, _ in checks), "all required checks passed" if all(passed for _, _, passed, _ in checks) else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3375 - Y5/R2FR worldtube source-measure selector or R_worldtube bound under AX1090",
        "",
        "## Summary",
        "- 3375 attacks the physical ownership step left by 3374: the topological current only helps if the source worldtube and mass measure are selected by the parent Hilbert/Noether action before readout.",
        "- Derivation result: a clean conditional selector theorem exists. If matter couples to one observed frame `e_obs(q(Phi))`, then `W_source=closure(supp(delta S_matter/delta e_obs contracted with tau))` is parent-selected rather than fit-selected.",
        "- Source-measure correction: the active local source is the dressed Hamiltonian/Noether charge `M_source[W]=H_tau[S]-H_ref-residuals`, not bare rest mass unless binding, field, Poynting, boundary, and extra-sector dressing are proven silent.",
        "- Poynting result: EM/wave energy is not ignored. It is either part of public Hilbert stress in the same `e_obs` branch, or it becomes the explicit `R_Poynting_worldtube` residual.",
        "- Current verdict: the theorem is not a current MTS claim. The corpus still lacks the explicit parent Lagrangian, integrable `H_tau`, source-blind `H_ref`, boundary zero flux, extra-sector silence, positive `M_H_ref`, and fixed `G_ref/kappa` normalization.",
        "- Fallback result: `R_worldtube_glue/M_H_ref`, `R_source_measure/M_H_ref`, `R_Wsupport`, `R_reference_selector`, `R_Poynting_worldtube`, and `M_H_ref` are explicit nonclaim rows.",
        "- Best next strike is boundary/reference zero flux: prove `B_zero_flux=0` for linked surfaces or stage the first source-backed `B_zero_flux/M_H_ref` row.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## Selector Theorem Attempt",
        md_table(rows_by_name["selector_theorem"]),
        "## Parent Action Selector Contract",
        md_table(rows_by_name["parent_contract"]),
        "## Parent Signature Audit",
        md_table(rows_by_name["signature_audit"]),
        "## R_worldtube Bound Rows",
        md_table(rows_by_name["residual_rows"]),
        "## Numeric Scan",
        md_table(rows_by_name["numeric_scan"]),
        "## Poynting Source-worldtube Placement",
        md_table(rows_by_name["poynting_rows"]),
        "## Countermodel Ledger",
        md_table(rows_by_name["countermodels"]),
        "## Source-transfer Update",
        md_table(rows_by_name["transfer_update"]),
        "## Nonclaim Runner",
        md_table(rows_by_name["runner"]),
        "## Promotion Gates",
        md_table(rows_by_name["gates"]),
        "## Decision Ledger",
        md_table(rows_by_name["decision"]),
        "## Validation",
        md_table(rows_by_name["validation"]),
        "## Next Target",
        md_table(rows_by_name["next"]),
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_register = source_rows()
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in source_register)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register,
        "selector_theorem": selector_theorem_rows(),
        "parent_contract": parent_contract_rows(),
        "signature_audit": signature_audit_rows(),
        "residual_rows": residual_rows(),
        "numeric_scan": numeric_scan_rows(),
        "poynting_rows": poynting_rows(),
        "countermodels": countermodel_rows(),
        "transfer_update": transfer_update_rows(),
        "runner": runner_rows(),
        "gates": gate_rows(source_ok),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUTS)} CSV outputs under {OUT}")
    print(f"Generated UTC {RUN_UTC}")


if __name__ == "__main__":
    main()
