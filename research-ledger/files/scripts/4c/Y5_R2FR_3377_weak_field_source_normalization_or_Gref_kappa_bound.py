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
DOC = ROOT / "3377-Y5-R2FR-weak-field-source-normalization-or-Gref-kappa-bound-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3377_SOURCE_REGISTER.csv",
    "normalization_theorem": OUT / "P8_Y5_R2FR_3377_WEAK_FIELD_SOURCE_NORMALIZATION_THEOREM.csv",
    "coefficient_contract": OUT / "P8_Y5_R2FR_3377_COEFFICIENT_IDENTITY_CONTRACT.csv",
    "signature_audit": OUT / "P8_Y5_R2FR_3377_NORMALIZATION_SIGNATURE_AUDIT.csv",
    "residual_rows": OUT / "P8_Y5_R2FR_3377_GREF_KAPPA_RESIDUAL_ROWS_NONCLAIM.csv",
    "numeric_scan": OUT / "P8_Y5_R2FR_3377_GREF_KAPPA_NUMERIC_SCAN.csv",
    "ppn_update": OUT / "P8_Y5_R2FR_3377_NEWTON_PPN_UPDATE_NONCLAIM.csv",
    "guardrails": OUT / "P8_Y5_R2FR_3377_G_IS_PARAMETER_GUARDRAILS.csv",
    "runner": OUT / "P8_Y5_R2FR_3377_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3377_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3377_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3377_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3377_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3377_0_3376_doc", ROOT / "3376-Y5-R2FR-boundary-zero-flux-or-Bzero-first-row-under-AX1090.md", "3376 boundary/reference handoff"),
    ("SRC3377_1_3376_next", OUT / "P8_Y5_R2FR_3376_NEXT_TARGET.csv", "3376 selected weak-field normalization"),
    ("SRC3377_2_3362_Gref", OUT / "P8_Y5_R2FR_3362_GREF_OWNER_AND_NEWTON_LIMIT.csv", "G_ref owner and Newton limit"),
    ("SRC3377_3_2723_kappa_Gref", OUT / "P8_Y5_R2FR_2723_KAPPA_GREF_THEOREM_ATTEMPT.csv", "kappa/G_ref theorem attempt"),
    ("SRC3377_4_2578_coupling_gate", OUT / "P8_Y5_PIM_HAMILTONIAN_COUPLING_2578_COUPLING_BASELINE_GATE.csv", "coupling baseline gate"),
    ("SRC3377_5_2578_implications", OUT / "P8_Y5_PIM_HAMILTONIAN_COUPLING_2578_NEWTON_LOCAL_GR_IMPLICATIONS.csv", "Newton/local-GR implications"),
    ("SRC3377_6_2928_baseline_rows", OUT / "P8_Y5_R2FR_2928_KAPPA_ELLJ_COUPLING_BASELINE_ROWS.csv", "kappa/ellJ coupling residual rows"),
    ("SRC3377_7_2692_poisson", OUT / "P8_Y5_R2FR_2692_NEWTON_POISSON_NORMALIZATION_DERIVATION.csv", "Newton/Poisson normalization derivation"),
    ("SRC3377_8_2724_poisson_rows", OUT / "P8_Y5_R2FR_2724_FINITE_POISSON_OPERATOR_ROWS_NONCLAIM.csv", "finite Poisson operator residuals"),
    ("SRC3377_9_868_newton_contract", OUT / "P8_Y5_R10_868_NEWTON_SOURCE_NORMALIZATION_CONTRACT.csv", "Newton source normalization contract"),
    ("SRC3377_10_2178_v_source", OUT / "P8_Y5_PARENT_QLOC_2178_V_NEWTON_SOURCE_CONVENTION_DERIVATION.csv", "v-source Newton convention"),
    ("SRC3377_11_2177_ppn_convention", OUT / "P8_Y5_PARENT_QLOC_2177_PPN_SOURCE_CONVENTION_GATE.csv", "PPN source convention gate"),
    ("SRC3377_12_2576_law", OUT / "P8_Y5_HCORE_QR_COUPLING_2576_NEWTON_PPN_COEFFICIENT_LAW.csv", "Newton/PPN coefficient law"),
    ("SRC3377_13_2502_law", OUT / "P8_Y5_NO_SHADOW_2502_NEWTON_PPN_COEFFICIENT_LAW.csv", "earlier Newton/PPN coefficient law"),
    ("SRC3377_14_source_norm_template", OUT / "P8_source_normalized_Newton_branch_STACK.csv", "source-normalized Newton branch stack"),
    ("SRC3377_15_boundary_status", OUT / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv", "M_H_ref denominator status"),
    ("SRC3377_16_worldtube_3375", OUT / "P8_Y5_R2FR_3375_WORLDTUBE_SOURCE_MEASURE_SELECTOR_THEOREM.csv", "source/worldtube selector theorem"),
]

NUMERIC_SCAN_TARGETS = [
    ("delta_kappa", OUT / "P8_Y5_R2FR_2928_KAPPA_ELLJ_COUPLING_BASELINE_ROWS.csv", "kappa baseline residual"),
    ("delta_ellJ", OUT / "P8_Y5_R2FR_2928_KAPPA_ELLJ_COUPLING_BASELINE_ROWS.csv", "source-current scale residual"),
    ("epsilon_Gref_match", OUT / "P8_Y5_R2FR_2928_KAPPA_ELLJ_COUPLING_BASELINE_ROWS.csv", "G_ref match residual"),
    ("Delta_boundary_coupling", OUT / "P8_Y5_R2FR_2928_KAPPA_ELLJ_COUPLING_BASELINE_ROWS.csv", "boundary coupling residual"),
    ("delta_KC", OUT / "P8_Y5_HCORE_QR_COUPLING_2576_NEWTON_PPN_COEFFICIENT_LAW.csv", "v action/source coefficient residual"),
    ("epsilon_M", OUT / "P8_Y5_HCORE_QR_COUPLING_2576_NEWTON_PPN_COEFFICIENT_LAW.csv", "mass-current glue residual"),
    ("Delta_Newton_v_coupled", OUT / "P8_Y5_HCORE_QR_COUPLING_2576_NEWTON_PPN_COEFFICIENT_LAW.csv", "coupled Newton residual"),
    ("kappa_v", OUT / "P8_Y5_HCORE_QR_COUPLING_2576_NEWTON_PPN_COEFFICIENT_LAW.csv", "second-order beta source ledger"),
    ("beta_minus_1", OUT / "P8_Y5_NO_SHADOW_2502_NEWTON_PPN_COEFFICIENT_LAW.csv", "PPN beta residual"),
    ("M_H_ref", OUT / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv", "positive source denominator"),
]

BAD_STATUS_TOKENS = (
    "MISSING",
    "NOT_DERIVED",
    "NOT_REACHED",
    "NOT_CLAIMED",
    "NOT_CURRENT",
    "OPEN",
    "UNSIGNED",
    "CONDITIONAL",
    "TEMPLATE",
    "NONCLAIM",
    "FALSE",
    "FAIL",
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


def normalization_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "WFS3377_0_EH_coefficient_owner",
            "claim_piece": "EH parent coefficient defines the gravitational constant",
            "statement": "If the local parent branch contains S_EH=(c^4/16*pi*G_ref) int sqrt(-g_obs) R[g_obs] or equivalently G_mn=kappa_MTS T_mn with kappa_MTS=8*pi*G_ref/c^4, then G_ref is parent-owned.",
            "derivation": "The absolute SI value of G_ref need not be derived for GR reduction; what must be derived is that one fixed coefficient appears before readout and is not source/radius/frame dependent.",
            "current_status": "VALID_CONDITIONAL_PARAMETER_OWNER_NOT_FULL_PARENT_SIGNATURE",
            "residual_if_missing": "delta_kappa;epsilon_Gref_match",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "WFS3377_1_Hilbert_source_scale",
            "claim_piece": "source-current normalization is fixed by matter variation",
            "statement": "If S_matter uses the same e_obs(q(Phi)) and J_H[tau] is delta S_matter/delta e_obs contracted with tau, then ell_J=1 in that branch and no separate source-current rescaling is allowed after readout.",
            "derivation": "The source mass in the weak-field equation, Hamiltonian charge, and PPN potentials is the same Hilbert/Noether source measure selected in 3375.",
            "current_status": "VALID_CONDITIONAL_SOURCE_SCALE_OWNER_NOT_GLOBAL_SIGNATURE",
            "residual_if_missing": "delta_ellJ;epsilon_M",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "WFS3377_2_EH_to_Poisson",
            "claim_piece": "same coefficient gives the Poisson equation",
            "statement": "In the weak-field observed frame, G_00^(1)=2 nabla^2 Phi_N/c^2 and T_00=rho_H c^2 imply nabla^2 Phi_N=4*pi*G_ref*rho_H when kappa_MTS=8*pi*G_ref/c^4.",
            "derivation": "This is the clean Newton coefficient map: the coefficient is inherited from the parent EH term and the source density is inherited from the Hilbert source current, not from orbital GM fitting.",
            "current_status": "EXACT_CONDITIONAL_WEAK_FIELD_ALGEBRA_NOT_CURRENT_CLAIM",
            "residual_if_missing": "R_Poisson_norm;E_Poisson_residual",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "WFS3377_3_Hamiltonian_Gauss_same_constant",
            "claim_piece": "surface charge and Poisson/Gauss mass use one normalization",
            "statement": "The Hamiltonian charge must use the same coefficient: M_H[S]=N_G int_S Q_tau-H_ref with N_G chosen by the EH symplectic charge so exterior Gauss gives Phi_N=-G_ref M_H/r.",
            "derivation": "If N_G, H_ref, or Pi_M carries a different normalization, conservation can hold while the measured inverse-square amplitude is wrong.",
            "current_status": "VALID_CONDITIONAL_HAMILTONIAN_MATCH_MHREF_MISSING",
            "residual_if_missing": "epsilon_Gref_match;M_H_ref;Delta_boundary_coupling",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "WFS3377_4_v_branch_source_action",
            "claim_piece": "constrained v branch has an exact source-normalization target",
            "statement": "For g_tt=-exp(v)c^2, Phi_N=(c^2/2)v. Newton requires v=-2G_ref M/(c^2 r). A leading action L_v=-(c^4/32*pi*G_ref)|grad v|^2-rho_H c^2 v/2 gives nabla^2 v=8*pi*G_ref rho_H/c^2.",
            "derivation": "This supplies a non-magic coefficient target for MTS: parent-derive the v kinetic coefficient and matter coupling, or carry delta_KC.",
            "current_status": "EXACT_CONDITIONAL_ACTION_TARGET_PARENT_NORMALIZATION_MISSING",
            "residual_if_missing": "delta_KC",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "WFS3377_5_PPN_same_U",
            "claim_piece": "same source potential feeds PPN",
            "statement": "If the same U=G_ref M_H/r fixes v=-2U/c^2 and the reciprocal readout A=exp(v), B=exp(-v) is parent-owned in the same gauge, then gamma=1 at first order and beta=1 only if the quadratic source ledger kappa_v vanishes.",
            "derivation": "PPN is not a separate fit. The same coefficient and source mass must control clocks, spatial curvature, null propagation, and second-order terms.",
            "current_status": "GAMMA_BETA_SHAPE_CONDITIONAL_KAPPA_V_OPEN",
            "residual_if_missing": "kappa_v;beta_minus_1;PPN_vector",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "WFS3377_6_normalization_verdict",
            "claim_piece": "calibrated source coupling theorem",
            "statement": "If WFS3377_0 through WFS3377_5 are parent-signed in one q/e_obs/tau/H_ref/Pi_M branch, then the same G_ref/kappa/source-current scale controls H_tau, Poisson/Newton and PPN readout.",
            "derivation": "This would move MTS from a fitted source-amplitude branch to a GR-like calibrated local limit. Current corpus has exact conditional maps, not the parent action signatures.",
            "current_status": "VALID_CONDITIONAL_THEOREM_NOT_CURRENT_CLAIM",
            "residual_if_missing": "Delta_coupling_baseline_abs;Delta_Newton_v_coupled",
            "valid_for_claim": "false",
        },
    ]


def coefficient_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "contract_id": "COEF3377_0_kappa_Gref",
            "coefficient": "kappa_MTS <-> G_ref",
            "required_identity": "kappa_MTS=8*pi*G_ref/c^4 and d kappa_MTS=0 on connected local exterior branches",
            "forbidden_shortcut": "setting G_ref from measured orbital GM after source/readout comparison",
            "residual": "delta_kappa;epsilon_Gref_match",
            "current_status": "CONDITIONAL_OWNER_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "COEF3377_1_NG_charge",
            "coefficient": "N_G",
            "required_identity": "N_G is the normalization induced by the same EH symplectic/Hamiltonian charge that defines G_ref",
            "forbidden_shortcut": "choosing surface-charge normalization separately from Poisson/Newton normalization",
            "residual": "epsilon_Gref_match;M_H_ref",
            "current_status": "HAMILTONIAN_MATCH_OPEN",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "COEF3377_2_ellJ",
            "coefficient": "ell_J",
            "required_identity": "ell_J=1 or fixed parent constant in the same Hilbert source-current normalization before readout",
            "forbidden_shortcut": "rescaling source mass after seeing Newton, WEP, PPN or orbital residuals",
            "residual": "delta_ellJ;epsilon_M",
            "current_status": "SOURCE_SCALE_OWNER_OPEN",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "COEF3377_3_v_action_ratio",
            "coefficient": "C_v/K_v",
            "required_identity": "C_v c^4/(16*pi*G_ref*K_v)=1, equivalently the v kinetic and matter-source terms imply nabla^2 v=8*pi*G_ref rho_H/c^2",
            "forbidden_shortcut": "using reciprocal readout shape without deriving the v source equation amplitude",
            "residual": "delta_KC",
            "current_status": "ACTION_RATIO_TARGET_EXACT_PARENT_MISSING",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "COEF3377_4_ppn_quadratic",
            "coefficient": "kappa_v",
            "required_identity": "kappa_v=-eta_v+kappa_source_quad+kappa_PiM+kappa_boundary+kappa_readout+kappa_operator+kappa_coupling=0 or bounded",
            "forbidden_shortcut": "claiming local GR from first-order gamma/Newton shape only",
            "residual": "beta_minus_1=kappa_v/2",
            "current_status": "SECOND_ORDER_LEDGER_OPEN",
            "valid_for_claim": "false",
        },
    ]


def signature_audit_rows() -> list[dict[str, str]]:
    return [
        {"audit_id": "SIG3377_0_parent_EH_coefficient", "required_signature": "explicit local EH coefficient or equivalent parent equation convention", "evidence": "3362 and 2723 supply exact conditional map; total parent action sector certificate still missing", "current_status": "MISSING_PARENT_SIGNATURE", "blocks": "WFS3377_0", "valid_for_claim": "false"},
        {"audit_id": "SIG3377_1_same_Hilbert_source", "required_signature": "same Hilbert source current in e_obs/tau branch", "evidence": "3375 conditionally selects source measure; global matter descent/source scale remains unsigned", "current_status": "PARTIAL_CONDITIONAL", "blocks": "WFS3377_1", "valid_for_claim": "false"},
        {"audit_id": "SIG3377_2_weak_field_gauge", "required_signature": "weak-field gauge and Phi_N/v definition fixed in the observed frame", "evidence": "2692 and 2178 give exact templates; parent readout/gauge ownership is conditional", "current_status": "GAUGE_READOUT_LOCK_OPEN", "blocks": "WFS3377_2;WFS3377_4", "valid_for_claim": "false"},
        {"audit_id": "SIG3377_3_Hamiltonian_charge_match", "required_signature": "N_G, Q_tau, H_ref and M_H_ref match the same G_ref branch", "evidence": "3375/3376 retain H_ref, M_H_ref and boundary/reference rows as nonclaim", "current_status": "MHREF_AND_REFERENCE_OPEN", "blocks": "WFS3377_3", "valid_for_claim": "false"},
        {"audit_id": "SIG3377_4_extra_stress_silence", "required_signature": "extra-sector stress and projector/operator corrections do not renormalize the local 00 equation", "evidence": "2724 and 2578 retain E_extra, PiM, boundary and source residuals", "current_status": "RESIDUAL_ROWS_RETAINED", "blocks": "R_Poisson_norm;Delta_Newton_v_coupled", "valid_for_claim": "false"},
        {"audit_id": "SIG3377_5_PPN_second_order", "required_signature": "same source potential controls gamma, beta and preferred-frame/conservation PPN terms", "evidence": "2177/2576 give shape and ledger; kappa_v and full PPN vector remain open", "current_status": "PPN_VECTOR_OPEN", "blocks": "WFS3377_5", "valid_for_claim": "false"},
    ]


def residual_rows() -> list[dict[str, str]]:
    return [
        {"row_id": "GKR3377_0_delta_kappa", "symbol": "delta_kappa", "definition": "variation or mismatch of kappa_MTS relative to the fixed local EH comparator", "bound_formula": "|D ln kappa_MTS| or |kappa_MTS c^4/(8*pi*G_ref)-1|", "required_inputs": "kappa_MTS,G_ref,local branch,source/radius/frame derivative,source_path", "current_status": "MISSING_CONSTANT_KAPPA_PROOF_OR_VALUE", "test_arena": "Newton;PPN;clock;orbital;R10", "valid_for_claim": "false"},
        {"row_id": "GKR3377_1_delta_ellJ", "symbol": "delta_ellJ", "definition": "hidden source-current scale drift relative to Hilbert source normalization", "bound_formula": "|D ln ell_J| or |ell_J/ell_J_parent-1|", "required_inputs": "ell_J,J_H,e_obs,tau,matter descent branch,source_path", "current_status": "MISSING_CONSTANT_ELLJ_PROOF_OR_VALUE", "test_arena": "Newton;WEP;PPN;orbital", "valid_for_claim": "false"},
        {"row_id": "GKR3377_2_epsilon_Gref_match", "symbol": "epsilon_Gref_match", "definition": "mismatch between EH coefficient, Hamiltonian charge normalization and Poisson/Newton G_ref", "bound_formula": "|G_Htau/G_Poisson-1| + |G_PPN/G_Poisson-1|", "required_inputs": "N_G,Q_tau,H_ref,kappa_MTS,G_ref,Poisson coefficient,PPN U convention", "current_status": "MATCH_NOT_DERIVED", "test_arena": "Newton;PPN;local-GR", "valid_for_claim": "false"},
        {"row_id": "GKR3377_3_delta_KC", "symbol": "delta_KC", "definition": "v-action/source coefficient residual", "bound_formula": "C_v c^4/(16*pi*G_ref*K_v)-1", "required_inputs": "C_v,K_v,G_ref,v kinetic term,matter v coupling", "current_status": "ACTION_COEFFICIENT_TARGET_EXACT_NUMERIC_MISSING", "test_arena": "Newton constrained v branch", "valid_for_claim": "false"},
        {"row_id": "GKR3377_4_Delta_Newton_v_coupled", "symbol": "Delta_Newton_v_coupled", "definition": "coupled Newton amplitude residual with no cancellation credit", "bound_formula": "(1+delta_KC)(1+epsilon_M)(1+delta_kappa)(1+delta_ellJ)-1", "required_inputs": "delta_KC,epsilon_M,delta_kappa,delta_ellJ", "current_status": "SOURCE_READY_VALUES_MISSING", "test_arena": "Newton;orbital;local-GR", "valid_for_claim": "false"},
        {"row_id": "GKR3377_5_kappa_v", "symbol": "kappa_v", "definition": "second-order PPN beta-source ledger including coupling effects", "bound_formula": "-eta_v+kappa_source_quad+kappa_PiM+kappa_boundary+kappa_readout+kappa_operator+kappa_coupling", "required_inputs": "second-order expansion,source quadratic,PiM,boundary,readout,operator,coupling terms", "current_status": "PPN_SECOND_ORDER_LEDGER_OPEN", "test_arena": "PPN beta;local-GR", "valid_for_claim": "false"},
        {"row_id": "GKR3377_6_beta_minus_1", "symbol": "beta_minus_1", "definition": "PPN beta residual in constrained v branch", "bound_formula": "beta-1=kappa_v/2", "required_inputs": "kappa_v full vector row", "current_status": "CONDITIONAL_ON_KAPPA_V", "test_arena": "PPN", "valid_for_claim": "false"},
        {"row_id": "GKR3377_7_M_H_ref", "symbol": "M_H_ref", "definition": "positive same-frame Hamiltonian source mass denominator", "bound_formula": "M_H_ref>0 in same H_tau/G_ref/e_obs/tau/source branch", "required_inputs": "H_tau,H_ref,N_G,e_obs,tau,source system,positivity certificate", "current_status": "MISSING_DENOMINATOR", "test_arena": "all normalized local residuals", "valid_for_claim": "false"},
    ]


def row_mentions_symbol(row: dict[str, str], symbol: str) -> bool:
    haystack = " ".join(str(value) for value in row.values()).lower()
    if symbol.lower() in haystack:
        return True
    aliases = {
        "delta_kappa": ("kappa", "Dln(kappa"),
        "delta_ellJ": ("ell_J", "ellJ"),
        "epsilon_Gref_match": ("G_ref", "Gref", "epsilon_Gref"),
        "Delta_boundary_coupling": ("boundary_coupling", "Delta_boundary"),
        "delta_KC": ("delta_KC", "C_v"),
        "epsilon_M": ("epsilon_M", "mass-current"),
        "Delta_Newton_v_coupled": ("Delta_Newton", "coupled Newton"),
        "kappa_v": ("kappa_v", "beta"),
        "beta_minus_1": ("beta-1", "beta_minus"),
        "M_H_ref": ("M_H_ref", "denominator"),
    }
    return any(alias.lower() in haystack for alias in aliases.get(symbol, ()))


def row_claimish(row: dict[str, str]) -> bool:
    text = " ".join(str(value) for value in row.values()).upper()
    valid_fields = [
        str(row.get("valid_for_claim", "")).lower(),
        str(row.get("claim_allowed", "")).lower(),
        str(row.get("score_ready", "")).lower(),
        str(row.get("valid_prediction_row", "")).lower(),
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
                    for key in ("status", "current_status", "result", "target_bound_or_zero", "missing")
                    if row.get(key, "")
                )
                for row in matching[:3]
            )
            if not status_excerpt:
                status_excerpt = "MATCHING_ROWS_NONCLAIM_OR_SCHEMA_ONLY"
        rows.append(
            {
                "scan_id": f"SCAN3377_{index}_{symbol}",
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


def ppn_update_rows() -> list[dict[str, str]]:
    return [
        {"update_id": "PPN3377_0_Newton", "condition": "WFS3377_0..4 signed and Delta_Newton_v_coupled=0", "effect": "Newtonian inverse-square amplitude follows from parent coefficient rather than orbital GM backfill", "current_status": "CONDITIONAL_NOT_CURRENT_CLAIM", "valid_for_claim": "false"},
        {"update_id": "PPN3377_1_gamma", "condition": "same v/U source convention and reciprocal readout A=exp(v), B=exp(-v) owned in PPN gauge", "effect": "gamma=1 shape is available at first order", "current_status": "SHAPE_PASS_CONDITIONAL_SOURCE_CONVENTION_OPEN", "valid_for_claim": "false"},
        {"update_id": "PPN3377_2_beta", "condition": "same source normalization plus kappa_v=0 or finite bound", "effect": "beta-1=kappa_v/2 can be promoted only after full second-order ledger closes", "current_status": "BETA_LEDGER_OPEN", "valid_for_claim": "false"},
        {"update_id": "PPN3377_3_preferred_frame", "condition": "same source frame, no kappa/ellJ drift, no hidden readout vector/tau branch", "effect": "alpha_i/zeta_i/xi terms can be tested without source-normalization ambiguity", "current_status": "FULL_PPN_VECTOR_STILL_OPEN", "valid_for_claim": "false"},
    ]


def guardrail_rows() -> list[dict[str, str]]:
    return [
        {"guard_id": "GUARD3377_0_GR_does_not_derive_G", "statement": "MTS does not need to derive the numerical SI value of G_ref to reduce to GR/Newton.", "why": "GR treats G as a universal coupling constant; the reduction requirement is same-constant ownership and no hidden drift.", "failure_prevented": "false demand that MTS compute 6.674e-11 before local-GR reduction", "valid_for_claim": "false"},
        {"guard_id": "GUARD3377_1_no_orbital_backfill", "statement": "Measured GM cannot be used to define G_ref, ell_J, N_G, or M_H_ref before the theorem is tested.", "why": "That would turn calibrated source coupling into a fitted amplitude.", "failure_prevented": "circular Newton recovery", "valid_for_claim": "false"},
        {"guard_id": "GUARD3377_2_no_cancellation_credit", "statement": "delta_KC, epsilon_M, delta_kappa, and delta_ellJ must close independently or be bounded; cancellations do not count as derivation.", "why": "Opposite-sign hidden errors can imitate Newton while failing clocks, PPN or WEP.", "failure_prevented": "Mayweather footwork turning into accounting fraud, basically", "valid_for_claim": "false"},
        {"guard_id": "GUARD3377_3_parameter_now_topology_later", "statement": "A future MTS parent action may try to derive G_ref topologically, but current local-GR reduction only requires fixed parent ownership.", "why": "This keeps the hard numerical-constant programme separate from the immediate GR/Newton reduction gate.", "failure_prevented": "overclaiming a deeper derivation not yet present", "valid_for_claim": "false"},
    ]


def runner_rows() -> list[dict[str, str]]:
    return [
        {"run_id": "RUN3377_0_EH_to_Poisson", "test": "derive Newton coefficient from EH coefficient and Hilbert source", "result": "PASS_CONDITIONAL_ALGEBRA", "detail": "kappa_MTS=8*pi*G_ref/c^4 gives nabla^2 Phi_N=4*pi*G_ref rho_H in the signed weak-field frame", "claim_allowed": "false", "valid_for_claim": "false"},
        {"run_id": "RUN3377_1_v_source_target", "test": "derive v-branch action target", "result": "PASS_CONDITIONAL_ACTION_TARGET", "detail": "L_v coefficient c^4/(32*pi*G_ref) and matter coupling rho c^2 v/2 imply nabla^2 v=8*pi*G_ref rho/c^2", "claim_allowed": "false", "valid_for_claim": "false"},
        {"run_id": "RUN3377_2_current_parent_signature", "test": "promote calibrated source coupling in current corpus", "result": "BLOCKED_NOT_PARENT_SIGNED", "detail": "parent coefficient, source scale, H_tau normalization, M_H_ref and full PPN ledger are still unsigned/nonclaim", "claim_allowed": "false", "valid_for_claim": "false"},
        {"run_id": "RUN3377_3_numeric_scan", "test": "find source-backed kappa/ellJ/Gref/PPN/M_H_ref rows", "result": "NO_NUMERIC_ROW_FOUND", "detail": "current rows are conditional, template, nonclaim or missing values", "claim_allowed": "false", "valid_for_claim": "false"},
        {"run_id": "RUN3377_4_absolute_G", "test": "require MTS to derive numerical G_ref before GR reduction", "result": "REFUSED_AS_UNNECESSARY_FOR_LOCAL_GR_REDUCTION", "detail": "fixed parent parameter is enough for GR-style reduction; topological derivation of G is future stronger route", "claim_allowed": "false", "valid_for_claim": "false"},
    ]


def gate_rows(source_ok: bool) -> list[dict[str, str]]:
    return [
        {"gate_id": "GATE3377_0_sources", "claim": "all required 3377 source paths exist and parse", "gate_pass": bool_text(source_ok), "reason": "source register validates local inputs", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3377_1_EH_Gref", "claim": "G_ref/kappa is parent-owned", "gate_pass": "false", "reason": "conditional EH coefficient map exists but total parent action signature is missing", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3377_2_ellJ_source", "claim": "source-current scale ell_J is fixed", "gate_pass": "false", "reason": "same Hilbert source route exists but global matter/source normalization remains unsigned", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3377_3_Htau_Poisson_match", "claim": "H_tau, Poisson and Newton use one normalization", "gate_pass": "false", "reason": "N_G/H_ref/M_H_ref and Gref match rows remain nonclaim", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3377_4_PPN", "claim": "PPN vector is locally GR after normalization", "gate_pass": "false", "reason": "gamma/beta shape is conditional but kappa_v/full PPN vector remains open", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3377_5_local_GR", "claim": "calibrated local GR/Newton source coupling is established", "gate_pass": "false", "reason": "normalization theorem is conditional and residual rows have no claim-valid source-backed values", "claim_allowed": "false", "valid_for_claim": "false"},
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {"decision_id": "DEC3377_0_progress", "decision": "The coupling problem is now a coefficient-identity theorem, not an undefined feeling.", "because": "one parent coefficient must feed EH, H_tau, Poisson/Newton and PPN; every mismatch has a named residual.", "next_action": "write the minimal parent action line that owns e_obs, Theta, Q_tau, B_ref, Pi_M, kappa_MTS and ell_J", "valid_for_claim": "false"},
        {"decision_id": "DEC3377_1_GR_constant_policy", "decision": "Do not waste effort demanding a numerical derivation of G_ref before local-GR reduction.", "because": "GR also takes G as a universal coupling; MTS can compete if it proves fixed ownership and no hidden source-scale drift.", "next_action": "separate local-GR reduction from future topological/superselection G derivation", "valid_for_claim": "false"},
        {"decision_id": "DEC3377_2_current_status", "decision": "Current MTS still cannot claim calibrated Newton/PPN coupling.", "because": "the algebraic maps are clean, but parent coefficient, source scale, Hamiltonian normalization, M_H_ref, and PPN second-order ledger are not signed.", "next_action": "retain delta_kappa, delta_ellJ, epsilon_Gref_match, delta_KC, Delta_Newton_v_coupled and kappa_v rows", "valid_for_claim": "false"},
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {"target_id": "3378-Y5-R2FR-parent-action-minimal-line-or-source-bound-inputs-under-AX1090.md", "target_script": "scripts/Y5_R2FR_3378_parent_action_minimal_line_or_source_bound_inputs.py", "objective": "write the minimal parent action line that owns e_obs, Theta, Q_tau, B_ref, Pi_M, kappa_MTS and ell_J, or demote calibrated source coupling to closure-only", "why_next": "3375-3377 have turned local-GR recovery into a chain of conditional theorems; the shared missing object is the explicit parent variation", "valid_for_claim": "false"},
        {"target_id": "3379-Y5-R2FR-full-PPN-vector-after-source-normalization-or-bound-pack-under-AX1090.md", "target_script": "scripts/Y5_R2FR_3379_full_PPN_vector_after_source_normalization_or_bound_pack.py", "objective": "use the normalized source convention to bind gamma, beta, alpha_i, zeta_i and xi residuals without hiding coupling failures", "why_next": "once the parent action line is explicit, the second-order PPN vector is the next local-GR test", "valid_for_claim": "false"},
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
    formalization_hits = list(FW.rglob("*3377*")) if FW.exists() else []
    theorem_ids = {row["theorem_id"] for row in rows_by_name["normalization_theorem"]}
    contract_ids = {row["contract_id"] for row in rows_by_name["coefficient_contract"]}
    audit_ids = {row["audit_id"] for row in rows_by_name["signature_audit"]}
    residual_symbols = {row["symbol"] for row in rows_by_name["residual_rows"]}
    scan_results = {row["scan_result"] for row in rows_by_name["numeric_scan"]}
    guard_ids = {row["guard_id"] for row in rows_by_name["guardrails"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    checks = [
        ("VAL3377_0_sources_exist_parse", "all cited local source paths exist and parse", source_ok, ""),
        ("VAL3377_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3377_2_normalization_theorem", "theorem covers EH owner, Hilbert source, Poisson, Htau/Gauss, v action, PPN and verdict", {"WFS3377_0_EH_coefficient_owner", "WFS3377_1_Hilbert_source_scale", "WFS3377_2_EH_to_Poisson", "WFS3377_3_Hamiltonian_Gauss_same_constant", "WFS3377_4_v_branch_source_action", "WFS3377_5_PPN_same_U", "WFS3377_6_normalization_verdict"}.issubset(theorem_ids), ""),
        ("VAL3377_3_coefficient_contract", "contract covers kappa/Gref, N_G, ell_J, v action ratio and PPN quadratic", {"COEF3377_0_kappa_Gref", "COEF3377_1_NG_charge", "COEF3377_2_ellJ", "COEF3377_3_v_action_ratio", "COEF3377_4_ppn_quadratic"}.issubset(contract_ids), ""),
        ("VAL3377_4_signature_audit", "signature audit covers parent coefficient, Hilbert source, gauge, Hamiltonian match, stress silence and PPN", {"SIG3377_0_parent_EH_coefficient", "SIG3377_1_same_Hilbert_source", "SIG3377_2_weak_field_gauge", "SIG3377_3_Hamiltonian_charge_match", "SIG3377_4_extra_stress_silence", "SIG3377_5_PPN_second_order"}.issubset(audit_ids), ""),
        ("VAL3377_5_residual_rows", "residual rows cover coupling, source-scale, Newton and PPN normalization", {"delta_kappa", "delta_ellJ", "epsilon_Gref_match", "delta_KC", "Delta_Newton_v_coupled", "kappa_v", "beta_minus_1", "M_H_ref"}.issubset(residual_symbols), ""),
        ("VAL3377_6_numeric_scan_blocks_claim", "numeric scan finds no source-backed numeric rows", scan_results == {"NO_SOURCE_BACKED_NUMERIC_ROW"}, ""),
        ("VAL3377_7_guardrails", "guardrails separate fixed G parameter from forbidden backfill and no-cancellation rule", {"GUARD3377_0_GR_does_not_derive_G", "GUARD3377_1_no_orbital_backfill", "GUARD3377_2_no_cancellation_credit", "GUARD3377_3_parameter_now_topology_later"}.issubset(guard_ids), ""),
        ("VAL3377_8_runner_blocks_claim", "runner passes conditional algebra/action targets but blocks current claim", "PASS_CONDITIONAL_ALGEBRA" in runner_results and "PASS_CONDITIONAL_ACTION_TARGET" in runner_results and "BLOCKED_NOT_PARENT_SIGNED" in runner_results and "NO_NUMERIC_ROW_FOUND" in runner_results, ""),
        ("VAL3377_9_gates_block_local", "promotion gates block EH/Gref, ellJ, Htau/Poisson, PPN and local GR", gate_map.get("GATE3377_1_EH_Gref") == "false" and gate_map.get("GATE3377_2_ellJ_source") == "false" and gate_map.get("GATE3377_3_Htau_Poisson_match") == "false" and gate_map.get("GATE3377_4_PPN") == "false" and gate_map.get("GATE3377_5_local_GR") == "false", ""),
        ("VAL3377_10_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3377_11_next_target", "next target moves to minimal parent action line", rows_by_name["next"][0]["target_id"].startswith("3378-Y5-R2FR-parent-action-minimal-line"), ""),
        ("VAL3377_12_write_scope_outside_formalization", "no 3377 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
    ]
    checks.append(("VAL3377_13_overall", "3377 validation overall", all(passed for _, _, passed, _ in checks), "all required checks passed" if all(passed for _, _, passed, _ in checks) else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3377 - Y5/R2FR weak-field source normalization or Gref/kappa bound under AX1090",
        "",
        "## Summary",
        "- 3377 attacks calibrated source coupling: the same `G_ref/kappa_MTS/source-current` normalization must feed `H_tau`, Poisson/Newton, and PPN readout.",
        "- Derivation result: the weak-field algebra is clean. If `kappa_MTS=8*pi*G_ref/c^4` and the source is the same Hilbert current, then `G_00^(1)=2 nabla^2 Phi_N/c^2` gives `nabla^2 Phi_N=4*pi*G_ref*rho_H`.",
        "- v-branch result: for `g_tt=-exp(v)c^2`, `Phi_N=(c^2/2)v`; a leading action `L_v=-(c^4/32*pi*G_ref)|grad v|^2-rho_H c^2 v/2` gives `nabla^2 v=8*pi*G_ref*rho_H/c^2` and the target `v=-2G_ref M/(c^2 r)`.",
        "- Guardrail: MTS does not need to derive the numerical SI value of `G_ref` to reduce to GR/Newton. It must prove one fixed parent constant, not fit `G`, `ell_J`, `N_G`, or `M_H_ref` after readout.",
        "- Current verdict: calibrated source coupling is not parent-signed. The corpus lacks the explicit parent coefficient, global source-current scale, Hamiltonian normalization, positive `M_H_ref`, and full PPN second-order closure.",
        "- Fallback result: `delta_kappa`, `delta_ellJ`, `epsilon_Gref_match`, `delta_KC`, `Delta_Newton_v_coupled`, `kappa_v`, `beta_minus_1`, and `M_H_ref` remain explicit nonclaim rows.",
        "- Best next strike is the minimal parent action line: write the one parent variation that owns `e_obs`, `Theta`, `Q_tau`, `B_ref`, `Pi_M`, `kappa_MTS`, and `ell_J`, or demote calibrated source coupling to closure-only.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## Weak-field Source-normalization Theorem",
        md_table(rows_by_name["normalization_theorem"]),
        "## Coefficient Identity Contract",
        md_table(rows_by_name["coefficient_contract"]),
        "## Normalization Signature Audit",
        md_table(rows_by_name["signature_audit"]),
        "## Gref/Kappa Residual Rows",
        md_table(rows_by_name["residual_rows"]),
        "## Numeric Scan",
        md_table(rows_by_name["numeric_scan"]),
        "## Newton/PPN Update",
        md_table(rows_by_name["ppn_update"]),
        "## G Parameter Guardrails",
        md_table(rows_by_name["guardrails"]),
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
        "normalization_theorem": normalization_theorem_rows(),
        "coefficient_contract": coefficient_contract_rows(),
        "signature_audit": signature_audit_rows(),
        "residual_rows": residual_rows(),
        "numeric_scan": numeric_scan_rows(),
        "ppn_update": ppn_update_rows(),
        "guardrails": guardrail_rows(),
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
