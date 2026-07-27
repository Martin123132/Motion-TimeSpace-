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
DOC = ROOT / "3372-Y5-R2FR-Hilbert-source-transfer-chain-or-first-tail-numeric-row-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3372_SOURCE_REGISTER.csv",
    "transfer_theorem": OUT / "P8_Y5_R2FR_3372_HILBERT_SOURCE_TRANSFER_THEOREM_ATTEMPT.csv",
    "chain_obstructions": OUT / "P8_Y5_R2FR_3372_TRANSFER_CHAIN_OBSTRUCTION_LEDGER.csv",
    "em_poynting": OUT / "P8_Y5_R2FR_3372_PUBLIC_EM_POYNTING_OWNERSHIP_AUDIT.csv",
    "numeric_scan": OUT / "P8_Y5_R2FR_3372_FIRST_TAIL_NUMERIC_ROW_SCAN.csv",
    "tail_row_template": OUT / "P8_Y5_R2FR_3372_FIRST_TAIL_NUMERIC_ROW_TEMPLATE_NONCLAIM.csv",
    "updated_tail_bound": OUT / "P8_Y5_R2FR_3372_SOURCE_TRANSFER_RESIDUAL_BOUND_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3372_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3372_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3372_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3372_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3372_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3372_0_3371_doc", ROOT / "3371-Y5-R2FR-hidden-source-support-tail-zero-or-qbar-nonH-bound-under-AX1090.md", "3371 hidden-tail decomposition and handoff"),
    ("SRC3372_1_3371_next", OUT / "P8_Y5_R2FR_3371_NEXT_TARGET.csv", "3371 next target selecting source-transfer chain"),
    ("SRC3372_2_3371_source_owner", OUT / "P8_Y5_R2FR_3371_SOURCE_OWNER_TRANSFER_AUDIT.csv", "3371 source-owner audit"),
    ("SRC3372_3_3371_tail_bounds", OUT / "P8_Y5_R2FR_3371_TAIL_COMPONENT_BOUND_ROWS_NONCLAIM.csv", "3371 hidden-tail bound rows"),
    ("SRC3372_4_3340_hilbert_clause", OUT / "P8_Y5_R2FR_3340_PARENT_HILBERT_SOURCE_CLAUSE.csv", "candidate Hilbert source and public Maxwell/Hodge clauses"),
    ("SRC3372_5_2595_gate", OUT / "P8_Y5_GM_TRANSFER_2595_TRANSFER_GATE.csv", "GM transfer component gates"),
    ("SRC3372_6_2595_components", OUT / "P8_Y5_GM_TRANSFER_2595_COMPONENT_ROWS.csv", "GM transfer component rows"),
    ("SRC3372_7_worldtube_glue", OUT / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv", "worldtube/source-measure glue clauses"),
    ("SRC3372_8_pim_contract", OUT / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv", "Pi_M parent projector contract"),
    ("SRC3372_9_boundary_status", OUT / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv", "boundary/reference first-row status"),
    ("SRC3372_10_2594_stack", OUT / "P8_Y5_SOURCE_NORM_2594_THEOREM_STACK.csv", "Y5 source-normalization theorem stack"),
    ("SRC3372_11_2906_split", OUT / "P8_Y5_R2FR_2906_EPSILON_EXTRA_SOURCE_SPLIT.csv", "Y5/Y6 source split"),
    ("SRC3372_12_1008_doc", ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md", "Noether charge extraction limitations"),
    ("SRC3372_13_1009_doc", ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md", "minimum parent current-chain sector contract"),
]


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


def transfer_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "step_id": "HST3372_0_parent_noether_current",
            "claim_piece": "parent Noether current exists",
            "conditional_statement": "For a diffeomorphism-covariant parent action, delta L=E_A delta Phi^A+dTheta gives J_tau=Theta(Phi,L_tau Phi)-i_tau L and dJ_tau=-E_A L_tau Phi.",
            "derivation": "On shell in a compact exterior annulus with no source support, E_A=0 implies dJ_tau=0 up to explicitly retained boundary/projector/source residuals.",
            "current_status": "FORMAL_SHAPE_AVAILABLE_NOT_TOTAL_PARENT_SIGNED",
            "residual_if_missing": "MISSING_PARENT_SOURCE_CHARGE;theta_Qtau_debt",
            "valid_for_claim": "false",
        },
        {
            "step_id": "HST3372_1_charge_decomposition",
            "claim_piece": "mass charge form",
            "conditional_statement": "If J_tau=dQ_M[tau]+C_EH+C_extra+C_projector+C_boundary and all C terms vanish or are bounded, then int_S Q_M[tau] is radially conserved.",
            "derivation": "Integrate dJ_tau=0 over A=S2xI. Stokes gives int_S2 Q_M-int_S1 Q_M = -int_A(C_EH+C_extra+C_projector+C_boundary).",
            "current_status": "CONDITIONAL_THEOREM_WITH_RETAINED_C_TERMS",
            "residual_if_missing": "R_eq_integral;B_zero_flux;epsilon_extra_source",
            "valid_for_claim": "false",
        },
        {
            "step_id": "HST3372_2_PiM_Hilbert_equality",
            "claim_piece": "PiM-projected Hilbert current equals charge",
            "conditional_statement": "If Pi_M is parent-owned, q-basic, charge-preserving, self-adjoint and [d,Pi_M]J_H=0, then M_H[Pi_M J_H]=int_S Q_M[tau] up to boundary exact terms.",
            "derivation": "Use d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H. In the exterior, Ward/Euler closure kills Pi_M dJ_H; the commutator and projector-stress pieces are the only surviving projector obstruction.",
            "current_status": "VALID_CHAINMAP_CONDITIONAL_NOT_PARENT_CLOSED",
            "residual_if_missing": "I_commutator;epsilon_projector_stress;qbar_domain",
            "valid_for_claim": "false",
        },
        {
            "step_id": "HST3372_3_worldtube_glue",
            "claim_piece": "exterior charge equals compact source mass",
            "conditional_statement": "If W is the parent-owned source worldtube and S links W in a fixed homology class, then M_source[W]=int_S Q_M[tau] before orbital fitting.",
            "derivation": "This is the Gauss/Stokes bridge: the exterior charge reads the enclosed source only if the source measure, surfaces and homology class are fixed before readout.",
            "current_status": "CORE_GLUE_NOT_DERIVED",
            "residual_if_missing": "R_worldtube_glue;Delta_W_support;surface_homology_lock",
            "valid_for_claim": "false",
        },
        {
            "step_id": "HST3372_4_boundary_reference",
            "claim_piece": "boundary/reference terms do not shift mass",
            "conditional_statement": "If exact improvements and references are fixed before readout with int_S2 B-int_S1 B=0, then B_zero_flux=Delta_symp=0 for source transfer.",
            "derivation": "Exact does not mean harmless: only the linked-surface difference matters. Nonzero or source-dependent reference terms stay as qbar_boundary.",
            "current_status": "CONDITIONAL_ROUTE_OPEN_FIRST_ROWS_UNFILLED",
            "residual_if_missing": "B_zero_flux;Delta_symp;qbar_boundary",
            "valid_for_claim": "false",
        },
        {
            "step_id": "HST3372_5_public_EM_stress",
            "claim_piece": "EM/Poynting stress belongs to same Hilbert source",
            "conditional_statement": "If S_EM=-(lambda_0/4) integral sqrt(-g_pub)F^2 with hidden-independent lambda_0 and public Hodge star, then T_EM including Poynting flux is part of T_total.",
            "derivation": "Metric variation gives T_EM; variation of A gives the public current. The Poynting vector is an observer decomposition of T_EM, not a separate source owner.",
            "current_status": "VALID_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "residual_if_missing": "delta_star;delta_J;P_EM_DeltaT_EM;qbar_nonH",
            "valid_for_claim": "false",
        },
        {
            "step_id": "HST3372_6_weak_field_normalization",
            "claim_piece": "source charge reduces to Newtonian GM",
            "conditional_statement": "If Q_M[tau] reduces to ADM/Komar/Gauss mass and the same constant G_ref calibrates Poisson's equation, then slow-orbit GM is an output of the transfer chain.",
            "derivation": "The Newtonian limit must be Q_M -> M and grad^2 Phi=4pi G_ref rho. Fitted orbital GM may test this equality but cannot be used as the proof input.",
            "current_status": "LIMIT_TARGET_CONDITIONAL_NOT_DERIVED",
            "residual_if_missing": "epsilon_GM_absorption_shortcut;M_H_ref;tau_frame_lock",
            "valid_for_claim": "false",
        },
        {
            "step_id": "HST3372_7_transfer_verdict",
            "claim_piece": "pre-fit source transfer chain",
            "conditional_statement": "If HST3372_0 through HST3372_6 all hold in one branch, then B_xi/G_eff = M_H[Pi_M J_H] = int_S Q_M[tau] = M_source[W] before orbital fitting.",
            "derivation": "Combine Noether closure, charge decomposition, Pi_M chainmap, worldtube Stokes, boundary zero-flux, public EM Hilbert stress and weak-field normalization.",
            "current_status": "VALID_CONDITIONAL_THEOREM_NOT_CURRENT_CLAIM",
            "residual_if_missing": "qbar_nonH;qbar_support;qbar_domain;qbar_boundary;epsilon_PiM_total_abs",
            "valid_for_claim": "false",
        },
    ]


def chain_obstruction_rows() -> list[dict[str, str]]:
    return [
        {
            "obstruction_id": "OBS3372_0_parent_source_charge",
            "chain_step": "HST3372_0",
            "missing_object": "parent-signed total current J_tau and mass charge Q_M[tau]",
            "evidence": "1008/1009 keep theta/Q_tau total and parent current chain blocked",
            "retained_residual": "MISSING_PARENT_SOURCE_CHARGE",
            "repair_or_bound": "extract total parent theta/Q_tau or retain charge-decomposition residual",
            "valid_for_claim": "false",
        },
        {
            "obstruction_id": "OBS3372_1_R_eq",
            "chain_step": "HST3372_1/HST3372_2",
            "missing_object": "R_eq_integral",
            "evidence": "GMC2595_0 current_value=MISSING_R_EQ_INTEGRAL",
            "retained_residual": "R_eq_integral/M_H_ref",
            "repair_or_bound": "prove Pi_M J_H equals Q_M plus fixed exact term or source R_eq row",
            "valid_for_claim": "false",
        },
        {
            "obstruction_id": "OBS3372_2_commutator",
            "chain_step": "HST3372_2",
            "missing_object": "I_commutator",
            "evidence": "GMT2595_2 PIM_COMMUTATOR_ZERO_NOT_PROVED and PM6 not_parent_derived_next_target",
            "retained_residual": "I_commutator/M_H_ref",
            "repair_or_bound": "prove [d,Pi_M]J_H=0 on physical source-current complex or source numeric commutator bound",
            "valid_for_claim": "false",
        },
        {
            "obstruction_id": "OBS3372_3_projector_stress",
            "chain_step": "HST3372_2",
            "missing_object": "epsilon_projector_stress",
            "evidence": "PM5 projector variation not parent derived; GMC2595_3 missing projector stress map",
            "retained_residual": "epsilon_projector_stress",
            "repair_or_bound": "include delta Pi_M stress in T_total or prove topological/no-stress projector",
            "valid_for_claim": "false",
        },
        {
            "obstruction_id": "OBS3372_4_worldtube_glue",
            "chain_step": "HST3372_3",
            "missing_object": "R_worldtube_glue and surface_homology_lock",
            "evidence": "W504_4 not_yet_derived_core_missing_piece; GMC2595_5 missing surfaces",
            "retained_residual": "R_worldtube_glue/M_H_ref;Delta_W_support",
            "repair_or_bound": "prove fixed worldtube source measure equals exterior charge before readout",
            "valid_for_claim": "false",
        },
        {
            "obstruction_id": "OBS3372_5_boundary_flux",
            "chain_step": "HST3372_4",
            "missing_object": "B_zero_flux and Delta_symp",
            "evidence": "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS has zero claim-valid data/theorem rows",
            "retained_residual": "B_zero_flux/M_H_ref;Delta_symp/M_H_ref",
            "repair_or_bound": "prove fixed zero-flux reference or source boundary numerator rows",
            "valid_for_claim": "false",
        },
        {
            "obstruction_id": "OBS3372_6_MHref_tau",
            "chain_step": "HST3372_6/HST3372_7",
            "missing_object": "positive same-frame M_H_ref and tau_frame_lock",
            "evidence": "GMC2595_4 and GMC2595_6 are missing; boundary status has no claim-valid M_H_ref row",
            "retained_residual": "normalization denominator missing",
            "repair_or_bound": "derive same-frame positive source mass denominator or keep every ratio unscoreable",
            "valid_for_claim": "false",
        },
        {
            "obstruction_id": "OBS3372_7_no_orbital_shortcut",
            "chain_step": "HST3372_6",
            "missing_object": "pre-fit source calibration",
            "evidence": "GMT2595_7 and YSN2594_4 keep observed-GM shortcut forbidden",
            "retained_residual": "epsilon_GM_absorption_shortcut",
            "repair_or_bound": "use orbital GM only as later test output, not denominator/proof input",
            "valid_for_claim": "false",
        },
    ]


def em_poynting_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "EMP3372_0_public_action",
            "question": "When is Poynting ordinary Hilbert stress rather than hidden background force?",
            "answer": "When Maxwell/Hodge uses the same public metric/coframe and hidden-independent lambda_0, Poynting is an observer-frame component of T_EM.",
            "mathematical_form": "S_EM=-(lambda_0/4) int sqrt(-g_pub) F_{mu nu}F^{mu nu}; T_EM=(-2/sqrt(-g_pub))delta S_EM/delta g_pub",
            "status": "VALID_CONDITIONAL_THEOREM",
            "residual_if_missing": "delta_star;delta_J;P_EM_DeltaT_EM",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "EMP3372_1_hidden_hodge_countercase",
            "question": "What if the background field/Hodge rule is X-sensitive?",
            "answer": "Then EM stress is not silently standard; its hidden Hodge/current normalization must enter qbar_nonH or the EM residual vector.",
            "mathematical_form": "epsilon_EM <= |delta_ZA| + |delta_star| + |delta_J| + ||P_EM Delta T_EM||/||T_EM||",
            "status": "RETAINED_RESIDUAL_IF_NOT_PUBLIC",
            "residual_if_missing": "qbar_nonH_EM_piece",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "EMP3372_2_static_radiative_guard",
            "question": "Can static Coulomb stress and radiative Poynting stress be double-counted?",
            "answer": "No. They must be components/projections of the same T_EM, with source/readout decomposition fixed before scoring.",
            "mathematical_form": "P_static T_EM + P_rad T_EM = P_EM T_EM; do not add a separate background-force source unless a hidden sector is retained.",
            "status": "GUARD_ACTIVE_NOT_NUMERIC_ROW",
            "residual_if_missing": "static_radiative_double_count_residual",
            "valid_for_claim": "false",
        },
    ]


def numeric_scan_rows() -> list[dict[str, str]]:
    candidates = [
        ("NUM3372_0_R_eq_integral", OUT / "P8_Y5_GM_TRANSFER_2595_COMPONENT_ROWS.csv", "R_eq_integral", "current_value"),
        ("NUM3372_1_I_commutator", OUT / "P8_Y5_GM_TRANSFER_2595_COMPONENT_ROWS.csv", "I_commutator", "current_value"),
        ("NUM3372_2_B_zero_flux", OUT / "P8_Y5_GM_TRANSFER_2595_COMPONENT_ROWS.csv", "B_zero_flux", "current_value"),
        ("NUM3372_3_epsilon_projector_stress", OUT / "P8_Y5_GM_TRANSFER_2595_COMPONENT_ROWS.csv", "epsilon_projector_stress", "current_value"),
        ("NUM3372_4_M_H_ref", OUT / "P8_Y5_GM_TRANSFER_2595_COMPONENT_ROWS.csv", "M_H_ref", "current_value"),
        ("NUM3372_5_boundary_first_row", OUT / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv", "epsilon_boundary_reference_abs", "status"),
    ]
    rows: list[dict[str, str]] = []
    for scan_id, path, symbol, value_field in candidates:
        source_rows_local = read_csv_rows(path)
        matching = [
            row
            for row in source_rows_local
            if symbol in (row.get("symbol", ""), row.get("quantity", ""), row.get("row_id", ""))
            or symbol == row.get("quantity", "")
        ]
        values = ";".join(row.get(value_field, "") for row in matching) if matching else "MISSING_ROW"
        score_ready = any(row.get("score_ready", "").lower() == "true" or row.get("valid_for_claim", "").lower() == "true" for row in matching)
        has_missing = "MISSING" in values.upper() or "UNFILLED" in values.upper() or values == "MISSING_ROW"
        rows.append(
            {
                "scan_id": scan_id,
                "symbol": symbol,
                "source_path": str(path),
                "source_path_exists": bool_text(path.exists()),
                "observed_value_or_status": values,
                "score_ready_or_claim_valid_seen": bool_text(score_ready),
                "missing_marker_seen": bool_text(has_missing),
                "scan_result": "NO_SOURCE_BACKED_NUMERIC_ROW" if has_missing or not score_ready else "CANDIDATE_ROW_FOUND_REQUIRES_REVIEW",
                "valid_for_claim": "false",
            }
        )
    return rows


def tail_row_template_rows() -> list[dict[str, str]]:
    return [
        {
            "template_id": "TRT3372_0_source_transfer_total",
            "target_quantity": "epsilon_source_transfer_abs",
            "formula": "(|R_eq_integral|+|I_commutator|+|B_zero_flux|+|R_worldtube_glue|)/|M_H_ref| + |epsilon_projector_stress| + |epsilon_EM_hidden|",
            "required_fields": "system_id;branch_id;R_eq_integral;I_commutator;B_zero_flux;R_worldtube_glue;M_H_ref;epsilon_projector_stress;epsilon_EM_hidden;units;source_path;equation_ref;no_cancellation_guard",
            "acceptance_rule": "all numerator/denominator units compatible, M_H_ref positive, source paths exist, no MISSING markers, no fitted orbital-GM denominator",
            "current_status": "TEMPLATE_READY_NO_NUMERIC_ROW",
            "valid_for_claim": "false",
        },
        {
            "template_id": "TRT3372_1_qbar_nonH_bridge",
            "target_quantity": "qbar_nonH_bound",
            "formula": "|q_nonH| + |J_shadow|/|J_H| + |epsilon_species_A| + |epsilon_EM_hidden|",
            "required_fields": "q_nonH;J_shadow;J_H;epsilon_species_A;delta_star;delta_J;T_EM_norm;units;source_path;equation_ref",
            "acceptance_rule": "finite same-branch ratios or parent-signed Hilbert-source zero theorem",
            "current_status": "TEMPLATE_READY_NO_NUMERIC_ROW",
            "valid_for_claim": "false",
        },
        {
            "template_id": "TRT3372_2_qbar_support_domain_boundary_bridge",
            "target_quantity": "qbar_support_domain_boundary_bound",
            "formula": "|Delta_W_support| + |I_commutator|/|M_H_ref| + |epsilon_projector_stress| + |B_zero_flux|/|M_H_ref| + |Delta_symp|/|M_H_ref|",
            "required_fields": "Delta_W_support;I_commutator;epsilon_projector_stress;B_zero_flux;Delta_symp;M_H_ref;surface_homology_lock;tau_frame_lock;source_path",
            "acceptance_rule": "all components source-backed and absolute-summed in one q/e_obs/tau/M_H_ref branch",
            "current_status": "TEMPLATE_READY_NO_NUMERIC_ROW",
            "valid_for_claim": "false",
        },
    ]


def updated_tail_bound_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "STB3372_0_transfer_residual_abs",
            "symbol": "epsilon_source_transfer_abs",
            "formula": "(|R_eq_integral|+|I_commutator|+|B_zero_flux|+|R_worldtube_glue|)/|M_H_ref| + |epsilon_projector_stress| + |epsilon_EM_hidden| + |epsilon_GM_absorption_shortcut|",
            "meaning": "absolute no-cancellation source-transfer residual controlling the shared hidden-tail obstruction",
            "current_status": "FORMULA_DERIVED_VALUES_MISSING",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "STB3372_1_qbar_hidden_tail_link",
            "symbol": "qbar_hidden_tail_bound_abs",
            "formula": "|qbar_hidden_tail| <= |qbar_nonH| + |qbar_support| + |qbar_domain| + |qbar_boundary| <= C_transfer * epsilon_source_transfer_abs + retained_visible_source_terms",
            "meaning": "source-transfer theorem would collapse several 3371 tails at once; without it the components remain explicit",
            "current_status": "LINK_CONDITIONAL_CONSTANT_CTRANSFER_MISSING",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "STB3372_2_Newton_source_gate",
            "symbol": "epsilon_Newton_source_transfer",
            "formula": "source-normalized Newton passes only if epsilon_source_transfer_abs=0 by parent theorem or is below sourced Newton/PPN tolerance without fitted-GM absorption",
            "meaning": "prevents using the observed orbital GM as its own proof",
            "current_status": "GATE_WRITTEN_NOT_SCORED",
            "valid_for_claim": "false",
        },
    ]


def runner_rows() -> list[dict[str, str]]:
    return [
        {
            "run_id": "RUN3372_0_conditional_transfer_theorem",
            "test": "Noether + charge decomposition + PiM chainmap + worldtube glue + boundary zero-flux + public EM + weak-field normalization",
            "result": "PASS_CONDITIONAL_THEOREM",
            "detail": "these clauses imply B_xi/G_eff = M_H[Pi_M J_H] = int_S Q_M[tau] = M_source[W] before orbital fitting",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3372_1_current_parent_signature",
            "test": "promote transfer theorem in current corpus",
            "result": "BLOCKED_NOT_PARENT_SIGNED",
            "detail": "parent theta/Q_tau, PiM commutator/stress, worldtube glue, boundary flux and M_H_ref are not signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3372_2_numeric_row_scan",
            "test": "search existing transfer rows for source-backed numeric tail row",
            "result": "NO_NUMERIC_ROW_FOUND",
            "detail": "existing R_eq, I_commutator, B_zero_flux, projector stress and M_H_ref rows contain MISSING/unfilled/nonclaim markers",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3372_3_EM_Poynting",
            "test": "decide whether Poynting is new force or Hilbert EM stress",
            "result": "PUBLIC_IF_HODGE_PUBLIC_ELSE_RETAINED_RESIDUAL",
            "detail": "Poynting is T_EM under public Maxwell/Hodge; hidden Hodge/current normalization is an explicit residual",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3372_4_local_GR_Newton",
            "test": "use source-transfer theorem to claim local GR/Newton",
            "result": "REFUSED",
            "detail": "the theorem is conditional and no numeric residual bound is available",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def gate_rows(source_ok: bool) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE3372_0_sources",
            "claim": "all required 3372 source paths exist and parse",
            "gate_pass": bool_text(source_ok),
            "reason": "source register validates every cited local input",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3372_1_transfer_theorem",
            "claim": "source-transfer chain is parent theorem",
            "gate_pass": "false",
            "reason": "chain is valid conditionally but parent signatures are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3372_2_first_numeric_tail_row",
            "claim": "first source-backed numeric hidden-tail row exists",
            "gate_pass": "false",
            "reason": "numeric scan found only MISSING/unfilled/nonclaim rows",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3372_3_public_EM",
            "claim": "EM/Poynting source ownership is parent-signed",
            "gate_pass": "false",
            "reason": "public Maxwell/Hodge is conditional; hidden Hodge/current residuals remain if not signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3372_4_Newton_source",
            "claim": "source-normalized Newton is derived",
            "gate_pass": "false",
            "reason": "M_H_ref, transfer chain and no orbital-GM shortcut are not proved",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3372_5_local_GR",
            "claim": "local GR/source coupling is established",
            "gate_pass": "false",
            "reason": "source-transfer residual remains unbounded and left-hand EH/Newton gates remain separate",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC3372_0_progress",
            "decision": "The transfer theorem has been written as an exact conditional chain instead of another checklist.",
            "because": "Noether closure, PiM chainmap, worldtube Stokes, boundary zero-flux, public EM Hilbert stress and Newton normalization now form one theorem target.",
            "next_action": "attack the weakest single link rather than re-auditing all coupling symbols",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3372_1_current_status",
            "decision": "Current MTS still cannot claim the source-transfer theorem.",
            "because": "R_eq, I_commutator, B_zero_flux, projector stress, worldtube glue, M_H_ref and tau/surface lock are all missing or nonclaim.",
            "next_action": "choose one link for a derivation attempt or fill a source-backed row",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3372_2_best_link",
            "decision": "Best next link is Pi_M commutator/chainmap closure.",
            "because": "it is the algebraic hinge between Hilbert source current, worldtube charge and domain/projector tail; if it fails, it gives a concrete numeric target I_commutator/M_H_ref.",
            "next_action": "try to prove [d,Pi_M]J_H=0 from parent q-basic/topological Pi_M, or stage I_commutator bound acquisition",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3372_3_EM_status",
            "decision": "Poynting has been placed correctly.",
            "because": "it is not ignored; it is either Hilbert EM stress under public Hodge or a retained hidden-Hodge/current residual.",
            "next_action": "carry EM ownership through Pi_M/source-transfer rather than spawning an independent EM-force branch here",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3373-Y5-R2FR-PiM-commutator-chainmap-zero-or-Icommutator-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3373_PiM_commutator_chainmap_zero_or_Icommutator_bound.py",
            "objective": "prove [d,Pi_M]J_H=0 and zero projector stress from a parent q-basic/topological Pi_M chainmap, or stage a source-backed I_commutator/M_H_ref bound row",
            "why_next": "3372 shows Pi_M commutator/stress is the sharpest algebraic hinge in the Hilbert-source transfer chain and feeds qbar_domain, source normalization, Newton and PPN",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3374-Y5-R2FR-worldtube-source-glue-or-Rworldtube-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3374_worldtube_source_glue_or_Rworldtube_bound.py",
            "objective": "prove fixed worldtube/source measure equals exterior mass charge before orbital fitting, or stage R_worldtube_glue and surface_homology rows",
            "why_next": "worldtube glue is the next geometric link after Pi_M chainmap and is needed before measured GM can test rather than define the source",
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
    formalization_hits = list(FW.rglob("*3372*")) if FW.exists() else []

    theorem_steps = {row["step_id"] for row in rows_by_name["transfer_theorem"]}
    obstruction_ids = {row["obstruction_id"] for row in rows_by_name["chain_obstructions"]}
    scan_results = {row["scan_result"] for row in rows_by_name["numeric_scan"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}

    checks = [
        ("VAL3372_0_sources_exist_parse", "all cited local source paths exist and parse", source_ok, ""),
        (
            "VAL3372_1_outputs_parse",
            "all generated CSV outputs parse cleanly",
            len(parse_results) == len(output_csvs) and all(parse_results),
            f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}",
        ),
        (
            "VAL3372_2_transfer_theorem_complete",
            "transfer theorem covers Noether, charge, PiM, worldtube, boundary, EM, Newton normalization and verdict",
            {
                "HST3372_0_parent_noether_current",
                "HST3372_1_charge_decomposition",
                "HST3372_2_PiM_Hilbert_equality",
                "HST3372_3_worldtube_glue",
                "HST3372_4_boundary_reference",
                "HST3372_5_public_EM_stress",
                "HST3372_6_weak_field_normalization",
                "HST3372_7_transfer_verdict",
            }.issubset(theorem_steps),
            "",
        ),
        (
            "VAL3372_3_obstructions_complete",
            "obstruction ledger covers parent charge, R_eq, commutator, projector stress, worldtube, boundary, M_H_ref and no orbital shortcut",
            {
                "OBS3372_0_parent_source_charge",
                "OBS3372_1_R_eq",
                "OBS3372_2_commutator",
                "OBS3372_3_projector_stress",
                "OBS3372_4_worldtube_glue",
                "OBS3372_5_boundary_flux",
                "OBS3372_6_MHref_tau",
                "OBS3372_7_no_orbital_shortcut",
            }.issubset(obstruction_ids),
            "",
        ),
        (
            "VAL3372_4_EM_Poynting_audit",
            "EM/Poynting audit distinguishes public Hilbert stress from hidden-Hodge residual",
            len(rows_by_name["em_poynting"]) >= 3,
            "",
        ),
        (
            "VAL3372_5_numeric_scan_blocks_claim",
            "numeric scan finds no source-backed numeric tail row",
            scan_results == {"NO_SOURCE_BACKED_NUMERIC_ROW"},
            "",
        ),
        (
            "VAL3372_6_templates_ready",
            "first tail numeric row templates are present",
            len(rows_by_name["tail_row_template"]) >= 3,
            "",
        ),
        (
            "VAL3372_7_runner_blocks_claim",
            "runner marks theorem conditional, numeric row absent and local-GR refused",
            "PASS_CONDITIONAL_THEOREM" in runner_results
            and "NO_NUMERIC_ROW_FOUND" in runner_results
            and "REFUSED" in runner_results,
            "",
        ),
        (
            "VAL3372_8_gates_block_local",
            "promotion gates block transfer theorem, numeric row, Newton source and local GR",
            gate_map.get("GATE3372_1_transfer_theorem") == "false"
            and gate_map.get("GATE3372_2_first_numeric_tail_row") == "false"
            and gate_map.get("GATE3372_4_Newton_source") == "false"
            and gate_map.get("GATE3372_5_local_GR") == "false",
            "",
        ),
        ("VAL3372_9_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        (
            "VAL3372_10_next_target",
            "next target attacks PiM commutator/chainmap closure",
            rows_by_name["next"][0]["target_id"].startswith("3373-Y5-R2FR-PiM-commutator"),
            "",
        ),
        (
            "VAL3372_11_write_scope_outside_formalization",
            "no 3372 files were written under formalization-workbench",
            not formalization_hits,
            f"hits={len(formalization_hits)}",
        ),
    ]
    checks.append(
        (
            "VAL3372_12_overall",
            "3372 validation overall",
            all(passed for _, _, passed, _ in checks),
            "all required checks passed" if all(passed for _, _, passed, _ in checks) else "one or more checks failed",
        )
    )
    return [
        {
            "check_id": check_id,
            "check": check,
            "passed": bool_text(passed),
            "detail": detail,
        }
        for check_id, check, passed, detail in checks
    ]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3372 - Y5/R2FR Hilbert-source transfer chain or first tail numeric row under AX1090",
        "",
        "## Summary",
        "- 3372 attempts the actual source-transfer theorem behind the hidden-tail blocker: `B_xi/G_eff = M_H[Pi_M J_H] = int_S Q_M[tau] = M_source[W]` before orbital fitting.",
        "- Derivation result: the transfer chain is valid as a conditional theorem if Noether closure, charge decomposition, PiM chainmap, worldtube glue, boundary zero-flux, public EM Hilbert stress, and weak-field normalization all hold in one branch.",
        "- Current verdict: the theorem is not parent-signed. `R_eq_integral`, `I_commutator`, `B_zero_flux`, `epsilon_projector_stress`, `R_worldtube_glue`, `M_H_ref`, `tau_frame_lock`, and surface homology remain missing/nonclaim.",
        "- Numeric-row result: the scan found no existing source-backed numeric hidden-tail row. First-row templates are staged, but not claimable.",
        "- EM/Poynting result: Poynting is handled, not ignored. It is public Hilbert EM stress when the Hodge/Maxwell sector is public; otherwise hidden Hodge/current normalization becomes an explicit residual.",
        "- Best next strike is `Pi_M` commutator/chainmap closure: prove `[d,Pi_M]J_H=0` and zero projector stress, or stage `I_commutator/M_H_ref` as the first numeric tail target.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## Hilbert-source Transfer Theorem Attempt",
        md_table(rows_by_name["transfer_theorem"]),
        "## Transfer Chain Obstruction Ledger",
        md_table(rows_by_name["chain_obstructions"]),
        "## Public EM / Poynting Ownership Audit",
        md_table(rows_by_name["em_poynting"]),
        "## First Tail Numeric Row Scan",
        md_table(rows_by_name["numeric_scan"]),
        "## First Tail Numeric Row Templates",
        md_table(rows_by_name["tail_row_template"]),
        "## Source Transfer Residual Bound",
        md_table(rows_by_name["updated_tail_bound"]),
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
        "transfer_theorem": transfer_theorem_rows(),
        "chain_obstructions": chain_obstruction_rows(),
        "em_poynting": em_poynting_rows(),
        "numeric_scan": numeric_scan_rows(),
        "tail_row_template": tail_row_template_rows(),
        "updated_tail_bound": updated_tail_bound_rows(),
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
