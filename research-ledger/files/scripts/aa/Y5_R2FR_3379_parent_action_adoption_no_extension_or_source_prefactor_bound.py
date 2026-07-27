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
DOC = ROOT / "3379-Y5-R2FR-parent-action-adoption-no-extension-or-source-prefactor-bound-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3379_SOURCE_REGISTER.csv",
    "adoption_theorem": OUT / "P8_Y5_R2FR_3379_PARENT_ACTION_ADOPTION_NO_EXTENSION_THEOREM.csv",
    "source_prefactor": OUT / "P8_Y5_R2FR_3379_SOURCE_PREFACTOR_TYPING_GATE.csv",
    "marker_extension": OUT / "P8_Y5_R2FR_3379_MARKER_EXTENSION_GATE.csv",
    "countermodels": OUT / "P8_Y5_R2FR_3379_SURVIVING_COUNTERMODEL_LEDGER.csv",
    "bound_rows": OUT / "P8_Y5_R2FR_3379_SOURCE_PREF_MARKER_BOUND_ROWS_NONCLAIM.csv",
    "numeric_scan": OUT / "P8_Y5_R2FR_3379_SOURCE_PREF_MARKER_NUMERIC_SCAN.csv",
    "transfer_update": OUT / "P8_Y5_R2FR_3379_PARENT_ACTION_TRANSFER_UPDATE_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3379_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3379_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3379_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3379_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3379_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3379_0_3378_doc", ROOT / "3378-Y5-R2FR-parent-action-minimal-line-or-source-bound-inputs-under-AX1090.md", "3378 parent-action line handoff"),
    ("SRC3379_1_3378_next", OUT / "P8_Y5_R2FR_3378_NEXT_TARGET.csv", "3378 selected adoption/no-extension target"),
    ("SRC3379_2_3378_action_line", OUT / "P8_Y5_R2FR_3378_MINIMAL_PARENT_ACTION_LINE.csv", "3378 minimal parent action line"),
    ("SRC3379_3_3378_smuggling", OUT / "P8_Y5_R2FR_3378_NO_SMUGGLING_TESTS.csv", "3378 no-smuggling tests"),
    ("SRC3379_4_3364_no_prefactor", OUT / "P8_Y5_R2FR_3364_NO_SOURCE_PREFACTOR_THEOREM_ATTEMPT.csv", "latest no-source-prefactor theorem attempt"),
    ("SRC3379_5_3056_typed_prefactor", OUT / "P8_Y5_R2FR_3056_TYPED_NO_SOURCE_PREFACTOR_GRAMMAR_ATTEMPT.csv", "typed no-source-prefactor grammar"),
    ("SRC3379_6_2645_parent_clause", OUT / "P8_Y5_NO_SOURCE_PREFACTOR_2645_PARENT_ACTION_CLAUSE_ATTEMPT.csv", "parent no-source-prefactor clause"),
    ("SRC3379_7_2685_zero_contract", OUT / "P8_Y5_R2FR_2685_PARENT_SOURCE_PREFACTOR_ZERO_THEOREM_CONTRACT_NONCLAIM.csv", "source-prefactor zero theorem contract"),
    ("SRC3379_8_no_extension_1468", OUT / "P8_Y5_R10_1468_VISIBLE_ACTION_GRAMMAR_NO_EXTENSION_AUDIT.csv", "visible action grammar no-extension audit"),
    ("SRC3379_9_no_extension_2726", OUT / "P8_Y5_R2FR_2726_NO_EXTENSION_LC_PROOF_AUDIT.csv", "no-extension/LC proof audit"),
    ("SRC3379_10_extension_3204", OUT / "P8_Y5_R2FR_3204_EXPLICIT_ACTION_EXTENSION.csv", "explicit extension safety candidate"),
    ("SRC3379_11_marker_3370", OUT / "P8_Y5_R2FR_3370_NO_SHADOW_NO_MARKER_THEOREM.csv", "no-shadow/no-marker theorem"),
    ("SRC3379_12_marker_functor_3235", OUT / "P8_Y5_R2FR_3235_NO_MARKER_SOURCE_FUNCTOR_GATE.csv", "no-marker source functor gate"),
    ("SRC3379_13_marker_survivors_3096", OUT / "P8_Y5_R2FR_3096_SURVIVING_MARKER_FAMILY_AUDIT.csv", "surviving marker family audit"),
    ("SRC3379_14_marker_partial_3096", OUT / "P8_Y5_R2FR_3096_PARTIAL_NO_MARKER_THEOREM.csv", "partial no-marker theorem"),
]

NUMERIC_SCAN_TARGETS = [
    ("Delta_w_AB", OUT / "P8_Y5_R2FR_3364_NO_SOURCE_PREFACTOR_THEOREM_ATTEMPT.csv", "source-weight finite residual policy"),
    ("epsilon_Wchan", OUT / "P8_Y5_R2FR_3056_TYPED_NO_SOURCE_PREFACTOR_GRAMMAR_ATTEMPT.csv", "typed source/readout channel residual"),
    ("Xi_JH_DqZ_A", OUT / "P8_Y5_NO_SOURCE_PREFACTOR_2645_PARENT_ACTION_CLAUSE_ATTEMPT.csv", "source-prefactor component row"),
    ("E_no_extension_minimality", OUT / "P8_Y5_R2FR_2726_NO_EXTENSION_LC_PROOF_AUDIT.csv", "no-extension minimality residual"),
    ("J_marker_bound", OUT / "P8_Y5_R2FR_3235_NO_MARKER_SOURCE_FUNCTOR_GATE.csv", "marker/source functor residual"),
    ("qbar_marker", OUT / "P8_Y5_R2FR_3370_NO_SHADOW_NO_MARKER_THEOREM.csv", "no-marker visible-source residual"),
    ("b_marker", OUT / "P8_Y5_R2FR_3096_SURVIVING_MARKER_FAMILY_AUDIT.csv", "surviving marker bound family"),
]

BAD_STATUS_TOKENS = (
    "MISSING",
    "NOT_DERIVED",
    "NOT_PROVED",
    "NOT_SIGNED",
    "NOT_PARENT",
    "UNSIGNED",
    "CONDITIONAL",
    "COUNTERMODEL",
    "SURVIVES",
    "LIVE",
    "NONCLAIM",
    "FALSE",
    "FAIL",
    "OPEN",
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


def adoption_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "ADOPT3379_0_closed_parent_domain",
            "claim_piece": "closed field/object list before variation",
            "statement": "Conf_parent and Args(S_parent) must be fixed before variation; readout, projection, source-worldtube and arena maps are maps from solution space to observables, not new source arguments.",
            "result": "REQUIRED_NOT_DERIVED",
            "why": "Without a closed domain, source-only prefactors and marker functors can return as extra legal arguments.",
            "residual_if_missing": "R_parent_action_missing;epsilon_action_smuggling",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "ADOPT3379_1_typed_matter_functor",
            "claim_piece": "ordinary matter functor has one observed stack",
            "statement": "Allowed ordinary matter terms have type S_A[psi_A; e_obs(qPhi), D_obs, A_obs, theta_A(qPhi)] with one common measure/action line.",
            "result": "VALID_CONDITIONAL_TYPED_GRAMMAR",
            "why": "If this typed grammar is parent-signed, w_A(Z)S_A and kappa_A(Z)T_A are untypeable rather than merely absent from the preferred ansatz.",
            "residual_if_missing": "Delta_w_AB;delta_ellJ",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "ADOPT3379_2_no_source_prefactor",
            "claim_piece": "no source-only species/readout prefactor",
            "statement": "No w_A(X), kappa_A(X), c_A(source), H-channel or W-channel source rescaling may appear before Hilbert variation, except a universal common action scale absorbed into G_ref/kappa.",
            "result": "EXACT_CONDITIONAL_THEOREM_COUNTERMODEL_SURVIVES",
            "why": "Pre-action weighted matter S_matter=sum_A w_A S_A is covariant and Ward-compatible unless the parent grammar makes w_A untypeable.",
            "residual_if_missing": "Delta_w_AB;epsilon_Wchan;Xi_JH_DqZ_A",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "ADOPT3379_3_no_second_source_metric",
            "claim_piece": "no hidden source frame",
            "statement": "The parent grammar must forbid e_source=A_g(X)e_obs or disformal B_g(X) channels outside e_obs(qPhi).",
            "result": "CONDITIONAL_NO_SHADOW_THEOREM_NOT_PARENT_SIGNED",
            "why": "A common hidden frame can be WEP-blind yet still shift clocks, PPN, R10 or source normalization.",
            "residual_if_missing": "c_g;b_dis;R_frame_source_split",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "ADOPT3379_4_no_marker_functor",
            "claim_piece": "no material/constant/readout marker functor",
            "statement": "Masses, material constants, alpha_EM, clock constants, isotope/preparation labels and source-domain markers must be quotient-owned, superselected, or retained as residual coefficients.",
            "result": "PARTIAL_FIXED_SPURION_EXCLUSION_ONLY",
            "why": "Fixed empty-background spurions can be excluded, but co-moving material markers and quotient-invariant local scalars remain legal without a stronger no-extension theorem.",
            "residual_if_missing": "b_marker;b_alpha;J_marker_bound;qbar_marker",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "ADOPT3379_5_no_readout_reentry",
            "claim_piece": "no post-variation reentry",
            "statement": "Radiative/effective/readout maps must not enlarge coefficient domains or reenter before variation; Pi_M, B_ref and source masks cannot be chosen after residuals are inspected.",
            "result": "REENTRY_CLOSURE_NOT_DERIVED",
            "why": "A clean bare matter functor can still be spoiled by effective coefficients or readout projectors that reintroduce source labels.",
            "residual_if_missing": "C_eff_source_tail;epsilon_PiM_parent;epsilon_Bref",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "ADOPT3379_6_verdict",
            "claim_piece": "parent-action adoption/no-extension theorem",
            "statement": "If ADOPT3379_0 through ADOPT3379_5 are parent-signed in the 3378 action grammar, source-prefactor/marker families are theorem-zero or common-mode constants; otherwise they remain explicit finite residuals.",
            "result": "VALID_CONDITIONAL_THEOREM_NOT_CURRENT_CLAIM",
            "why": "The corpus has a precise grammar target and partial no-go results, but not the adoption/uniqueness theorem needed to promote local-GR source coupling.",
            "residual_if_missing": "epsilon_source_pref_marker_abs",
            "valid_for_claim": "false",
        },
    ]


def source_prefactor_rows() -> list[dict[str, str]]:
    return [
        {"gate_id": "SPG3379_0_universal_common_scale", "source_prefactor_family": "universal common action scale", "typing_result": "ALLOWED_ONLY_IF_COMMON_MODE", "effect": "can be absorbed into G_ref/kappa once 3377 coefficient owner is signed", "countermodel": "if not common-mode, it becomes relative source weighting", "valid_for_claim": "false"},
        {"gate_id": "SPG3379_1_species_weight", "source_prefactor_family": "w_A S_A or kappa_A T_A", "typing_result": "FORBIDDEN_CONDITIONAL_NOT_PARENT_SIGNED", "effect": "would set Delta_w_AB=0 if grammar is signed", "countermodel": "covariant pre-action weighted matter survives Ward/Bianchi", "valid_for_claim": "false"},
        {"gate_id": "SPG3379_2_readout_channel_weight", "source_prefactor_family": "a_H/a_W or H/W channel source leg", "typing_result": "FORBIDDEN_IF_READOUT_COORDINATES_NOT_PARENT_SOURCE_SLOTS", "effect": "kills epsilon_Wchan only after W/lapse/source convention ownership", "countermodel": "readout spurion sigma_W makes the weight typeable", "valid_for_claim": "false"},
        {"gate_id": "SPG3379_3_boundary_source_weight", "source_prefactor_family": "B_ref/H_ref/source-domain weight", "typing_result": "FORBIDDEN_IF_REFERENCE_SOURCE_BLIND", "effect": "prevents boundary bookkeeping from becoming active source scale", "countermodel": "source-dependent H_ref shifts measured GM", "valid_for_claim": "false"},
        {"gate_id": "SPG3379_4_post_variation_weight", "source_prefactor_family": "post-Hilbert source mask", "typing_result": "NOT_PARENT_SOURCE_IF_AFTER_VARIATION", "effect": "demotes to readout/projection residual, not source theorem", "countermodel": "can still affect observables if not bounded", "valid_for_claim": "false"},
    ]


def marker_extension_rows() -> list[dict[str, str]]:
    return [
        {"marker_id": "MEXT3379_0_fixed_spurion", "family": "fixed external spurion/covector", "status": "CONDITIONALLY_EXCLUDED", "reason": "not field, gauge, quotient pullback, universal constant or varied matter datum", "residual_if_survives": "epsilon_action_smuggling", "valid_for_claim": "false"},
        {"marker_id": "MEXT3379_1_common_frame", "family": "hidden common Weyl/conformal frame", "status": "LIVE_UNLESS_CG_ZERO_OR_BOUNDED", "reason": "can be WEP-blind but shift clocks/PPN/R10/source scale", "residual_if_survives": "c_g;qbar_geom", "valid_for_claim": "false"},
        {"marker_id": "MEXT3379_2_disformal_frame", "family": "hidden disformal/profile frame", "status": "LIVE_UNLESS_BDIS_ZERO_OR_BOUNDED", "reason": "can vanish in one limit while surviving in clock/orbit/PPN projections", "residual_if_survives": "b_dis", "valid_for_claim": "false"},
        {"marker_id": "MEXT3379_3_material_constants", "family": "mass ratios, isotope/material/preparation labels", "status": "LIVE_UNLESS_SUPERSELECTED_OR_BOUNDED", "reason": "co-moving material labels are not killed by fixed-spurion exclusion", "residual_if_survives": "b_marker;Delta_w_AB", "valid_for_claim": "false"},
        {"marker_id": "MEXT3379_4_alpha_clock_constants", "family": "alpha_EM, binding constants, clock transition markers", "status": "LIVE_UNLESS_CONSTANT_OWNER_SIGNED", "reason": "clock/fine-structure observations bound drift but do not prove zero", "residual_if_survives": "b_alpha;clock_marker_bound", "valid_for_claim": "false"},
        {"marker_id": "MEXT3379_5_readout_tail", "family": "domain, support, non-Hilbert, boundary/readout tail", "status": "LIVE_UNLESS_SOURCE_TAIL_CLOSED", "reason": "can reenter after ordinary matter functor descends", "residual_if_survives": "qbar_nonH;qbar_support;qbar_domain;qbar_boundary", "valid_for_claim": "false"},
    ]


def countermodel_rows() -> list[dict[str, str]]:
    return [
        {"countermodel_id": "CM3379_0_pre_action_weight", "construction": "S_matter=sum_A w_A S_A[psi_A,e_obs]", "why_survives": "covariant, additive and Ward-compatible unless w_A is untypeable", "what_breaks": "source universality and WEP/Newton source normalization", "repair": "typed parent object language or Delta_w_AB bound", "valid_for_claim": "false"},
        {"countermodel_id": "CM3379_1_common_WEP_blind_frame", "construction": "e_source=A_g(X)e_obs for all species", "why_survives": "universal coupling can pass WEP while shifting clocks/PPN/R10", "what_breaks": "same observed source frame", "repair": "no-shadow theorem parent-signed or c_g bound", "valid_for_claim": "false"},
        {"countermodel_id": "CM3379_2_covariant_marker_scalar", "construction": "theta_A=theta_A(qPhi,I_perp) with I_perp quotient-invariant or co-moving", "why_survives": "not a fixed external spurion", "what_breaks": "no-marker/source-functor theorem", "repair": "no-natural-marker theorem or b_marker bound", "valid_for_claim": "false"},
        {"countermodel_id": "CM3379_3_effective_reentry", "construction": "radiative/readout map generates Z_eff(q,K,X;mu) or source-tail coefficients after variation", "why_survives": "effective maps can preserve covariance while enlarging coefficient domain", "what_breaks": "variation-before-readout source ownership", "repair": "radiative no-reentry theorem or C_eff_source_tail bound", "valid_for_claim": "false"},
        {"countermodel_id": "CM3379_4_PiM_postfit", "construction": "Pi_M selected after source-transfer residuals are inspected", "why_survives": "projector algebra can be written without parent origin", "what_breaks": "mass projection becomes fitted selector", "repair": "Pi_M parent algebra or epsilon_PiM_parent bound", "valid_for_claim": "false"},
        {"countermodel_id": "CM3379_5_boundary_absorption", "construction": "H_ref/B_ref depends on source or readout branch", "why_survives": "finite charge subtraction can be covariant but source-dependent", "what_breaks": "G/M_H_ref calibration", "repair": "reference lock or epsilon_Bref bound", "valid_for_claim": "false"},
    ]


def bound_rows() -> list[dict[str, str]]:
    return [
        {"row_id": "SPM3379_0_Delta_w_AB", "symbol": "Delta_w_AB", "definition": "relative pre-action source/species weight residual", "bound_formula": "|w_A/w_B-1| or projected WEP/source-normalization bound", "required_inputs": "species pair, projection arena, source weights or WEP bound, no-cancellation rule", "current_status": "FINITE_RESIDUAL_RETAINED", "valid_for_claim": "false"},
        {"row_id": "SPM3379_1_epsilon_Wchan", "symbol": "epsilon_Wchan", "definition": "readout-channel source prefactor residual", "bound_formula": "|a_W/a_H-1| after source/readout convention lock", "required_inputs": "W/H channel definitions, source convention, projection owner", "current_status": "TYPED_GRAMMAR_CONDITIONAL_BOUND_REQUIRED", "valid_for_claim": "false"},
        {"row_id": "SPM3379_2_cg_bdis", "symbol": "c_g_b_dis", "definition": "hidden common frame/Weyl/disformal source metric residual", "bound_formula": "|c_g|+|b_dis| in local clock/PPN/R10/source projection", "required_inputs": "frame map, e_obs lock, c_g,b_dis coefficients, arena projections", "current_status": "NO_SHADOW_CONDITIONAL_NOT_PARENT_SIGNED", "valid_for_claim": "false"},
        {"row_id": "SPM3379_3_b_marker", "symbol": "b_marker", "definition": "material/constant/readout marker sensitivity residual", "bound_formula": "sum_A |partial ln theta_A/partial X| |Delta X| projected to arena", "required_inputs": "marker family, sensitivity, bound arena, source path", "current_status": "MARKER_FAMILIES_LIVE", "valid_for_claim": "false"},
        {"row_id": "SPM3379_4_C_eff_source_tail", "symbol": "C_eff_source_tail", "definition": "radiative/effective/readout reentry source coefficient", "bound_formula": "||effective source coefficient outside parent grammar|| in declared arena norm", "required_inputs": "effective map, coefficient domain, readout/projection map, units", "current_status": "NO_REENTRY_NOT_DERIVED", "valid_for_claim": "false"},
        {"row_id": "SPM3379_5_E_no_extension_minimality", "symbol": "E_no_extension_minimality", "definition": "parent no-extension/minimality failure residual", "bound_formula": "indicator or norm for legal action extensions outside PAL3378 grammar", "required_inputs": "complete field inventory, allowed morphism list, extension audit", "current_status": "NO_EXTENSION_NOT_PROVED", "valid_for_claim": "false"},
        {"row_id": "SPM3379_6_epsilon_source_pref_marker_abs", "symbol": "epsilon_source_pref_marker_abs", "definition": "combined source-prefactor/marker envelope", "bound_formula": "|Delta_w_AB|+|epsilon_Wchan|+|c_g|+|b_dis|+|b_marker|+|C_eff_source_tail|", "required_inputs": "component rows above, common units/projections, no-cancellation rule", "current_status": "ENVELOPE_READY_NUMERIC_MISSING", "valid_for_claim": "false"},
    ]


def row_mentions_symbol(row: dict[str, str], symbol: str) -> bool:
    haystack = " ".join(str(value) for value in row.values()).lower()
    if symbol.lower() in haystack:
        return True
    aliases = {
        "Delta_w_AB": ("Delta_w", "w_A", "prefactor"),
        "epsilon_Wchan": ("epsilon_Wchan", "a_W", "W-channel"),
        "Xi_JH_DqZ_A": ("Xi_JH", "DqZ"),
        "E_no_extension_minimality": ("no_extension", "minimality", "E_no_extension"),
        "J_marker_bound": ("J_marker", "marker"),
        "qbar_marker": ("qbar_marker", "marker"),
        "b_marker": ("b_marker", "material"),
    }
    return any(alias.lower() in haystack for alias in aliases.get(symbol, ()))


def row_claimish(row: dict[str, str]) -> bool:
    text = " ".join(str(value) for value in row.values()).upper()
    valid_fields = [
        str(row.get("valid_for_claim", "")).lower(),
        str(row.get("claim_allowed", "")).lower(),
        str(row.get("score_ready", "")).lower(),
        str(row.get("valid_prediction_row", "")).lower(),
        str(row.get("passes_now", "")).lower(),
        str(row.get("parent_signed", "")).lower(),
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
                    for key in ("result", "current_status", "status", "status_after_3096", "gap", "missing_for_claim")
                    if row.get(key, "")
                )
                for row in matching[:3]
            )
            if not status_excerpt:
                status_excerpt = "MATCHING_ROWS_NONCLAIM_OR_SCHEMA_ONLY"
        rows.append(
            {
                "scan_id": f"SCAN3379_{index}_{symbol}",
                "symbol": symbol,
                "source_path": str(path),
                "source_exists": bool_text(path.exists()),
                "matching_rows": str(len(matching)),
                "claim_valid_rows": str(len(claimish)),
                "status_excerpt": status_excerpt,
                "scan_result": "SOURCE_BACKED_CLAIM_ROW_FOUND" if claimish else "NO_SOURCE_BACKED_CLAIM_ROW",
                "valid_for_claim": "false",
            }
        )
    return rows


def transfer_update_rows() -> list[dict[str, str]]:
    return [
        {"update_id": "UPD3379_0_if_adoption_signed", "condition": "ADOPT3379_0..5 parent-signed", "local_GR_effect": "source-only prefactors, second source metrics, marker functors and readout reentry drop from source coupling residuals", "remaining_blockers": "sector Theta/Q_tau certificates, PiM parent origin, boundary lock and full PPN vector", "current_status": "CONDITIONAL_BRANCH_NOT_CURRENT_CLAIM", "valid_for_claim": "false"},
        {"update_id": "UPD3379_1_current_branch", "condition": "current MTS corpus", "local_GR_effect": "source-prefactor/marker families remain explicit nonclaim bound rows", "remaining_blockers": "typed parent object language, no-extension/no-reentry, no-natural-marker, source scale adoption", "current_status": "SOURCE_PREF_MARKER_RESIDUALS_RETAINED", "valid_for_claim": "false"},
        {"update_id": "UPD3379_2_project_strategy", "condition": "adoption theorem fails as current claim", "local_GR_effect": "do not keep circling; move to parent type-system proof or external finite bounds for the retained families", "remaining_blockers": "quantitative bound acquisition or stronger grammar theorem", "current_status": "NEXT_ROUTE_SELECTED", "valid_for_claim": "false"},
    ]


def runner_rows() -> list[dict[str, str]]:
    return [
        {"run_id": "RUN3379_0_typed_no_prefactor", "test": "typed grammar forbids source-only prefactors", "result": "PASS_CONDITIONAL_THEOREM", "detail": "if only q-owned observed matter stack and common action line are admissible, w_A/kappa_A are untypeable", "claim_allowed": "false", "valid_for_claim": "false"},
        {"run_id": "RUN3379_1_Ward_route", "test": "use Ward/Bianchi conservation to forbid pre-action weights", "result": "REFUSED_INSUFFICIENT", "detail": "pre-action weighted matter can remain covariant and conserved", "claim_allowed": "false", "valid_for_claim": "false"},
        {"run_id": "RUN3379_2_marker_route", "test": "exclude all markers by fixed-spurion no-go", "result": "PARTIAL_ONLY", "detail": "fixed external spurions are excluded, but common frames/material constants/readout tails survive", "claim_allowed": "false", "valid_for_claim": "false"},
        {"run_id": "RUN3379_3_current_parent_signature", "test": "promote no-extension/adoption for current MTS", "result": "BLOCKED_NOT_PARENT_SIGNED", "detail": "typed parent object language, no-extension, no-marker and no-reentry theorems are not signed", "claim_allowed": "false", "valid_for_claim": "false"},
        {"run_id": "RUN3379_4_numeric_scan", "test": "find claim-valid source-prefactor/marker rows", "result": "NO_CLAIM_ROW_FOUND", "detail": "current rows are conditional, finite-policy, live-countermodel, or nonclaim", "claim_allowed": "false", "valid_for_claim": "false"},
    ]


def gate_rows(source_ok: bool) -> list[dict[str, str]]:
    return [
        {"gate_id": "GATE3379_0_sources", "claim": "all required 3379 source paths exist and parse", "gate_pass": bool_text(source_ok), "reason": "source register validates local inputs", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3379_1_typed_prefactor", "claim": "no-source-prefactor theorem is valid conditionally", "gate_pass": "true", "reason": "typed matter grammar would make source-only weights untypeable if parent-signed", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3379_2_parent_adoption", "claim": "typed grammar is adopted as unique MTS parent action language", "gate_pass": "false", "reason": "parent type-system/no-extension theorem is missing", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3379_3_countermodels", "claim": "surviving countermodels are eliminated", "gate_pass": "false", "reason": "pre-action weights, common frames, markers, effective reentry, PiM and boundary countermodels remain legal or unbounded", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3379_4_bound_rows", "claim": "source-prefactor/marker bound rows are score-ready", "gate_pass": "false", "reason": "numeric scan finds no claim-valid rows", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3379_5_local_GR", "claim": "3378 parent action can now promote local GR source coupling", "gate_pass": "false", "reason": "adoption/no-extension fails as current claim", "claim_allowed": "false", "valid_for_claim": "false"},
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {"decision_id": "DEC3379_0_progress", "decision": "The no-source-prefactor theorem is exact but only conditional.", "because": "typed parent grammar can make source weights untypeable, but the grammar is not parent-adopted by current MTS.", "next_action": "prove the parent type-system/no-extension theorem or retain finite prefactor rows", "valid_for_claim": "false"},
        {"decision_id": "DEC3379_1_hard_limit", "decision": "Ward/Bianchi conservation is not enough.", "because": "pre-action weighted matter can be covariant and conserved while still changing active source normalization.", "next_action": "do not use conservation alone as source-universality evidence", "valid_for_claim": "false"},
        {"decision_id": "DEC3379_2_current_status", "decision": "Current MTS still cannot promote the 3378 parent action line.", "because": "source-only prefactors, common hidden frames, material markers and readout reentry are not eliminated in one signed parent grammar.", "next_action": "move to either a parent type-system proof or bound acquisition for Delta_w_AB/c_g/b_marker/source-tail rows", "valid_for_claim": "false"},
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {"target_id": "3380-Y5-R2FR-parent-type-system-or-source-prefactor-bound-acquisition-under-AX1090.md", "target_script": "scripts/Y5_R2FR_3380_parent_type_system_or_source_prefactor_bound_acquisition.py", "objective": "try to derive the parent object-language/type-system that makes source-only weights and marker functors untypeable; if it fails, acquire finite WEP/clock/R10/PPN source-prefactor bounds", "why_next": "3379 shows no-extension cannot be claimed from Ward/covariance alone; the next fork is stronger grammar theorem or real bound rows", "valid_for_claim": "false"},
        {"target_id": "3381-Y5-R2FR-full-PPN-vector-after-source-prefactor-guard-or-bound-pack-under-AX1090.md", "target_script": "scripts/Y5_R2FR_3381_full_PPN_vector_after_source_prefactor_guard_or_bound_pack.py", "objective": "carry source-prefactor/marker residuals into gamma, beta, alpha_i, zeta_i and xi without hiding coupling failures", "why_next": "the PPN vector is the next empirical local-GR gate after source prefactor and marker families are either killed or explicitly bounded", "valid_for_claim": "false"},
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
    formalization_hits = list(FW.rglob("*3379*")) if FW.exists() else []
    theorem_ids = {row["theorem_id"] for row in rows_by_name["adoption_theorem"]}
    prefactor_ids = {row["gate_id"] for row in rows_by_name["source_prefactor"]}
    marker_ids = {row["marker_id"] for row in rows_by_name["marker_extension"]}
    countermodel_ids = {row["countermodel_id"] for row in rows_by_name["countermodels"]}
    bound_symbols = {row["symbol"] for row in rows_by_name["bound_rows"]}
    scan_results = {row["scan_result"] for row in rows_by_name["numeric_scan"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    checks = [
        ("VAL3379_0_sources_exist_parse", "all cited local source paths exist and parse", source_ok, ""),
        ("VAL3379_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3379_2_adoption_theorem", "adoption theorem covers closed domain, typed matter, no prefactor, no second metric, no marker, no reentry and verdict", {"ADOPT3379_0_closed_parent_domain", "ADOPT3379_1_typed_matter_functor", "ADOPT3379_2_no_source_prefactor", "ADOPT3379_3_no_second_source_metric", "ADOPT3379_4_no_marker_functor", "ADOPT3379_5_no_readout_reentry", "ADOPT3379_6_verdict"}.issubset(theorem_ids), ""),
        ("VAL3379_3_source_prefactor_gate", "source-prefactor gate covers common scale, species, readout, boundary and post-variation weights", {"SPG3379_0_universal_common_scale", "SPG3379_1_species_weight", "SPG3379_2_readout_channel_weight", "SPG3379_3_boundary_source_weight", "SPG3379_4_post_variation_weight"}.issubset(prefactor_ids), ""),
        ("VAL3379_4_marker_extension_gate", "marker gate covers fixed spurion, common frame, disformal, material constants, alpha/clock and tails", {"MEXT3379_0_fixed_spurion", "MEXT3379_1_common_frame", "MEXT3379_2_disformal_frame", "MEXT3379_3_material_constants", "MEXT3379_4_alpha_clock_constants", "MEXT3379_5_readout_tail"}.issubset(marker_ids), ""),
        ("VAL3379_5_countermodels", "countermodels cover pre-action weight, common frame, marker scalar, reentry, PiM and boundary absorption", {"CM3379_0_pre_action_weight", "CM3379_1_common_WEP_blind_frame", "CM3379_2_covariant_marker_scalar", "CM3379_3_effective_reentry", "CM3379_4_PiM_postfit", "CM3379_5_boundary_absorption"}.issubset(countermodel_ids), ""),
        ("VAL3379_6_bound_rows", "bound rows cover source weights, readout channel, frame, marker, reentry, extension and envelope", {"Delta_w_AB", "epsilon_Wchan", "c_g_b_dis", "b_marker", "C_eff_source_tail", "E_no_extension_minimality", "epsilon_source_pref_marker_abs"}.issubset(bound_symbols), ""),
        ("VAL3379_7_numeric_scan_blocks_claim", "numeric scan finds no source-backed claim rows", scan_results == {"NO_SOURCE_BACKED_CLAIM_ROW"}, ""),
        ("VAL3379_8_runner_blocks_claim", "runner passes conditional grammar but blocks current claim", "PASS_CONDITIONAL_THEOREM" in runner_results and "REFUSED_INSUFFICIENT" in runner_results and "PARTIAL_ONLY" in runner_results and "BLOCKED_NOT_PARENT_SIGNED" in runner_results and "NO_CLAIM_ROW_FOUND" in runner_results, ""),
        ("VAL3379_9_gates_block_local", "promotion gates allow conditional theorem but block parent adoption, countermodels, bound rows and local GR", gate_map.get("GATE3379_1_typed_prefactor") == "true" and gate_map.get("GATE3379_2_parent_adoption") == "false" and gate_map.get("GATE3379_5_local_GR") == "false", ""),
        ("VAL3379_10_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3379_11_next_target", "next target moves to type-system proof or bound acquisition", rows_by_name["next"][0]["target_id"].startswith("3380-Y5-R2FR-parent-type-system"), ""),
        ("VAL3379_12_write_scope_outside_formalization", "no 3379 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
    ]
    checks.append(("VAL3379_13_overall", "3379 validation overall", all(passed for _, _, passed, _ in checks), "all required checks passed" if all(passed for _, _, passed, _ in checks) else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3379 - Y5/R2FR parent-action adoption no-extension or source-prefactor bound under AX1090",
        "",
        "## Summary",
        "- 3379 attacks the adoption/uniqueness gap left by 3378: can the minimal parent action grammar forbid source-only prefactors, second source metrics, post-variation projectors, and marker functors?",
        "- Derivation result: a clean conditional no-source-prefactor theorem exists. If ordinary matter has only the typed parent form `S_A[psi_A; e_obs(qPhi), D_obs, A_obs, theta_A(qPhi)]` with one common measure/action line, then `w_A(X)S_A` and `kappa_A(X)T_A` are untypeable.",
        "- Hard limit: Ward/Bianchi conservation is not enough. A covariant pre-action weighted matter sector can remain conserved while changing active source normalization.",
        "- Marker/no-extension result: fixed external spurions are conditionally excluded, but common hidden frames, disformal frames, material constants, alpha/clock markers, domain/support tails, and effective readout reentry survive without a stronger parent type-system theorem.",
        "- Current verdict: adoption/no-extension is not parent-signed for current MTS. The no-prefactor theorem is exact as a grammar theorem, but current MTS has not derived that grammar from its core object language.",
        "- Fallback result: `Delta_w_AB`, `epsilon_Wchan`, `c_g_b_dis`, `b_marker`, `C_eff_source_tail`, `E_no_extension_minimality`, and `epsilon_source_pref_marker_abs` are explicit nonclaim rows.",
        "- Best next strike is the type-system fork: either derive the parent object-language that makes those terms untypeable, or acquire finite WEP/clock/R10/PPN bounds for them.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## Adoption / No-extension Theorem Attempt",
        md_table(rows_by_name["adoption_theorem"]),
        "## Source-prefactor Typing Gate",
        md_table(rows_by_name["source_prefactor"]),
        "## Marker Extension Gate",
        md_table(rows_by_name["marker_extension"]),
        "## Surviving Countermodel Ledger",
        md_table(rows_by_name["countermodels"]),
        "## Bound Rows",
        md_table(rows_by_name["bound_rows"]),
        "## Numeric Scan",
        md_table(rows_by_name["numeric_scan"]),
        "## Transfer Update",
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
        "adoption_theorem": adoption_theorem_rows(),
        "source_prefactor": source_prefactor_rows(),
        "marker_extension": marker_extension_rows(),
        "countermodels": countermodel_rows(),
        "bound_rows": bound_rows(),
        "numeric_scan": numeric_scan_rows(),
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
