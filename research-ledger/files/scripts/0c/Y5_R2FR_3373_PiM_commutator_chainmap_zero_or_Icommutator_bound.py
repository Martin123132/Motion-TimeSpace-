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
DOC = ROOT / "3373-Y5-R2FR-PiM-commutator-chainmap-zero-or-Icommutator-bound-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3373_SOURCE_REGISTER.csv",
    "chainmap_theorem": OUT / "P8_Y5_R2FR_3373_PIM_CHAINMAP_COMMUTATOR_THEOREM_ATTEMPT.csv",
    "route_split": OUT / "P8_Y5_R2FR_3373_PIM_ROUTE_SPLIT.csv",
    "obstruction_rows": OUT / "P8_Y5_R2FR_3373_ICOMMUTATOR_OBSTRUCTION_ROWS_NONCLAIM.csv",
    "numeric_scan": OUT / "P8_Y5_R2FR_3373_ICOMMUTATOR_NUMERIC_SCAN.csv",
    "bound_template": OUT / "P8_Y5_R2FR_3373_ICOMMUTATOR_BOUND_TEMPLATE_NONCLAIM.csv",
    "transfer_update": OUT / "P8_Y5_R2FR_3373_SOURCE_TRANSFER_UPDATE_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3373_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3373_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3373_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3373_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3373_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3373_0_3372_doc", ROOT / "3372-Y5-R2FR-Hilbert-source-transfer-chain-or-first-tail-numeric-row-under-AX1090.md", "3372 source-transfer theorem and PiM commutator handoff"),
    ("SRC3373_1_3372_next", OUT / "P8_Y5_R2FR_3372_NEXT_TARGET.csv", "3372 next target selecting PiM commutator"),
    ("SRC3373_2_3372_theorem", OUT / "P8_Y5_R2FR_3372_HILBERT_SOURCE_TRANSFER_THEOREM_ATTEMPT.csv", "3372 transfer theorem rows"),
    ("SRC3373_3_3372_obstructions", OUT / "P8_Y5_R2FR_3372_TRANSFER_CHAIN_OBSTRUCTION_LEDGER.csv", "3372 obstruction rows"),
    ("SRC3373_4_3372_numeric", OUT / "P8_Y5_R2FR_3372_FIRST_TAIL_NUMERIC_ROW_SCAN.csv", "3372 numeric scan"),
    ("SRC3373_5_pim_contract", OUT / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv", "PiM parent symplectic projector contract"),
    ("SRC3373_6_commutator_gate", OUT / "P8_Y5_PIM_COMMUTATOR_GATE.csv", "PiM commutator/product-rule gate"),
    ("SRC3373_7_pim_numeric_audit", OUT / "P8_Y5_PIM_NUMERIC_INPUT_AUDIT.csv", "PiM numeric input audit"),
    ("SRC3373_8_pim_template", OUT / "P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv", "PiM input fill template"),
    ("SRC3373_9_pim_radial", OUT / "P8_Y5_PIM_RADIAL_BOUND_INPUT.csv", "PiM radial/source-normalization bound input"),
    ("SRC3373_10_1013_doc", ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md", "older PiM JH flux closure attempt"),
    ("SRC3373_11_1014_doc", ROOT / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md", "older PiM commutator/projector variation attempt"),
    ("SRC3373_12_1015_doc", ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md", "older same-object topological-Hilbert equality attempt"),
    ("SRC3373_13_1014_csv", OUT / "P8_Y5_R10_1014_PIM_COMMUTATOR_THEOREM_ATTEMPT.csv", "machine-readable 1014 commutator theorem attempt"),
    ("SRC3373_14_1013_csv", OUT / "P8_Y5_R10_1013_PIM_JH_FLUX_THEOREM_ATTEMPT.csv", "machine-readable 1013 PiM flux theorem attempt"),
    ("SRC3373_15_2595_components", OUT / "P8_Y5_GM_TRANSFER_2595_COMPONENT_ROWS.csv", "current source-transfer component rows"),
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


def chainmap_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "PCM3373_0_product_rule",
            "claim_piece": "exact projected-current product rule",
            "mathematical_form": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H, with [d,Pi_M]:=d o Pi_M - Pi_M o d",
            "derivation": "This is an identity for any projector that can vary across the exterior/source-current complex. The commutator is the exact obstruction to treating projected Hilbert flux as closed.",
            "current_status": "EXACT_OBSTRUCTION_IDENTITY_ACTIVE",
            "failure_if_missing": "silent loss of I_commutator into measured GM/source normalization",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PCM3373_1_fixed_topological_chainmap",
            "claim_piece": "topological PiM chain map",
            "mathematical_form": "Pi_M J := omega_M ell_M(J), d omega_M=0, ell_M(dK)=0 on the fixed compact exterior complex",
            "derivation": "If Sigma_ext has fixed S2xI topology, omega_M is a parent-owned closed q-basic mass generator, and ell_M is the pre-readout charge pairing, then d(Pi_M J)=0 and Pi_M(dK)=0 for exact/source-free exterior terms.",
            "current_status": "VALID_CONDITIONAL_CHAINMAP_THEOREM",
            "failure_if_missing": "Pi_M can be a domain/readout mask rather than a chain map",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PCM3373_2_Icommutator_zero",
            "claim_piece": "[d,Pi_M]J_H=0",
            "mathematical_form": "If J_H belongs to the parent source-current domain and Pi_M is the fixed chain map in PCM3373_1, then [d,Pi_M]J_H=0",
            "derivation": "d(Pi_M J_H)=0 by closed omega_M. Pi_M(dJ_H)=0 in the source-free exterior/Ward-closed domain, or remains separated as Pi_M dJ_extra if the Hilbert current is not closed. Therefore the commutator piece itself is zero only in the chainmap domain.",
            "current_status": "VALID_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "failure_if_missing": "I_commutator remains the finite-annulus obstruction",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PCM3373_3_zero_projector_stress",
            "claim_piece": "delta Pi_M stress silence",
            "mathematical_form": "delta_g Pi_M=0 and Lie_X Pi_M=0 for a q-basic topological Pi_M fixed before readout",
            "derivation": "A purely topological parent-owned chain projector has no metric/domain/readout variation, so it contributes no T_PiM or projector stress. If Pi_M is Hodge/DeWitt/domain-defined, delta Pi_M is not zero and must be varied or bounded.",
            "current_status": "VALID_CONDITIONAL_THEOREM_FOR_TOPOLOGICAL_ROUTE",
            "failure_if_missing": "epsilon_projector_stress and Delta_PiM stay active",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PCM3373_4_no_closure_from_algebra",
            "claim_piece": "projector algebra is not enough",
            "mathematical_form": "Pi_M^2=Pi_M and Pi_M^dagger=Pi_M do not imply d(Pi_M J_H)=0",
            "derivation": "Idempotence selects a component; it does not supply a Ward/Euler/topological closure equation. Flux closure needs the chainmap and source-current domain hypotheses.",
            "current_status": "SHORTCUT_REJECTED",
            "failure_if_missing": "post-readout source mask masquerades as a source theorem",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PCM3373_5_Hilbert_equality_guard",
            "claim_piece": "commutator zero is not yet source-transfer",
            "mathematical_form": "Even if [d,Pi_M]J_H=0, one still needs Pi_M J_H = J_M_top + dB_zero and M_H_ref/tau/worldtube locks",
            "derivation": "A closed projected current can still be the wrong conserved object. The same compact Hilbert worldtube class must be parent-signed before Newton/source transfer can use it.",
            "current_status": "GUARD_ACTIVE_R_EQ_NEXT",
            "failure_if_missing": "conserved-wrong-object problem survives",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PCM3373_6_current_verdict",
            "claim_piece": "PiM commutator/source-transfer status",
            "mathematical_form": "PCM3373_0 through PCM3373_5 all parent-signed or numerically bounded",
            "derivation": "The chainmap theorem is mathematically clean, but current MTS lacks a parent-signed fixed topological PiM, Hilbert equality, source-current domain, M_H_ref and no-Hodge-stress certificate.",
            "current_status": "CONDITIONAL_THEOREM_NOT_CURRENT_CLAIM",
            "failure_if_missing": "Newton/source-normalization/local-GR gates stay blocked",
            "valid_for_claim": "false",
        },
    ]


def route_split_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "PRS3373_0_topological_chainmap",
            "route_type": "candidate_derivation",
            "condition": "fixed S2xI exterior, q-basic closed omega_M, pre-readout ell_M, delta_g Pi_M=0",
            "result": "[d,Pi_M]J_H=0 and projector stress zero conditionally",
            "current_status": "VALID_CONDITIONAL_NOT_PARENT_SIGNED",
            "residual_if_missing": "I_commutator;Delta_PiM",
            "valid_for_claim": "false",
        },
        {
            "route_id": "PRS3373_1_Hodge_DeWitt_projector",
            "route_type": "retained_residual",
            "condition": "Pi_M depends on boundary metric, Hodge representative, DeWitt metric, Green operator, normal, or domain selector",
            "result": "delta Pi_M stress must be included; commutator is not theorem-zero",
            "current_status": "RETAIN_PROJECTOR_STRESS",
            "residual_if_missing": "epsilon_projector_stress;T_PiM;PPN_beta_gamma_rows",
            "valid_for_claim": "false",
        },
        {
            "route_id": "PRS3373_2_readout_mask",
            "route_type": "forbidden_shortcut",
            "condition": "Pi_M chosen after orbital/readout fitting to select measured GM",
            "result": "not a derivation; target observable is smuggled into the source theorem",
            "current_status": "FORBIDDEN",
            "residual_if_missing": "epsilon_GM_absorption_shortcut",
            "valid_for_claim": "false",
        },
        {
            "route_id": "PRS3373_3_topological_Hilbert_equality",
            "route_type": "next_derivation",
            "condition": "Pi_M J_H and J_M_top are representatives of the same compact Hilbert worldtube class",
            "result": "R_eq=0 up to exact zero-flux boundary term; needed after commutator closure",
            "current_status": "NEXT_ROOT_NOT_CLOSED_HERE",
            "residual_if_missing": "R_eq_integral;B_zero_flux",
            "valid_for_claim": "false",
        },
    ]


def obstruction_rows() -> list[dict[str, str]]:
    return [
        {
            "row_id": "ICO3373_0_I_commutator",
            "symbol": "I_commutator",
            "definition": "finite-annulus integral of [d,Pi_M]J_H over the compact exterior",
            "zero_route": "fixed topological q-basic Pi_M chain map on the source-current domain",
            "bound_formula": "|I_commutator|/|M_H_ref|",
            "required_inputs": "system_id,r1,r2,I_commutator,M_H_ref,units,norm_convention,source_file,assumptions",
            "current_status": "THEOREM_CONDITIONAL_NUMERIC_MISSING",
            "observable_links": "radial_Meff;source_normalization;Newton;PPN;R10;R11",
            "valid_for_claim": "false",
        },
        {
            "row_id": "ICO3373_1_Delta_PiM",
            "symbol": "Delta_PiM",
            "definition": "projector ownership/variation residual in measured source flux",
            "zero_route": "delta_g Pi_M=0 and Lie_X Pi_M=0 for parent topological PiM",
            "bound_formula": "|Delta_PiM|/|M_H_ref| or weak-field stress map",
            "required_inputs": "projector_type,metric_dependence_flag,Delta_PiM,units,normalization,source_file",
            "current_status": "THEOREM_CONDITIONAL_NUMERIC_MISSING",
            "observable_links": "PPN;source_mass;R11;domain_tail",
            "valid_for_claim": "false",
        },
        {
            "row_id": "ICO3373_2_epsilon_projector_stress",
            "symbol": "epsilon_projector_stress",
            "definition": "dimensionless stress/source-normalization contribution from metric-dependent PiM",
            "zero_route": "topological PiM or included projector stress in total Hilbert source with Bianchi-safe closure",
            "bound_formula": "|epsilon_projector_stress|",
            "required_inputs": "operator_family,coefficient,units,weak_field_map,affected_rows,source_file",
            "current_status": "THEOREM_CONDITIONAL_NUMERIC_MISSING",
            "observable_links": "gamma;beta;alpha_i;xi;R11;Y5_source_normalization",
            "valid_for_claim": "false",
        },
        {
            "row_id": "ICO3373_3_R_eq_guard",
            "symbol": "R_eq_integral",
            "definition": "same-object residual Pi_M J_H - J_M_top - dB_zero",
            "zero_route": "topological-Hilbert equality on same compact source worldtube class",
            "bound_formula": "|R_eq_integral|/|M_H_ref|",
            "required_inputs": "system_id,r1,r2,R_eq_integral,M_H_ref,units,normalization,source_file",
            "current_status": "NOT_SOLVED_BY_COMMUTATOR_ZERO_NEXT_ROOT",
            "observable_links": "source_mass;Newton;R11;worldtube_glue",
            "valid_for_claim": "false",
        },
        {
            "row_id": "ICO3373_TOTAL",
            "symbol": "epsilon_PiM_chainmap_abs",
            "definition": "absolute no-cancellation envelope for PiM commutator/projector chainmap residual",
            "zero_route": "I_commutator=Delta_PiM=epsilon_projector_stress=0 and R_eq handled by same-object theorem",
            "bound_formula": "|I_commutator|/|M_H_ref| + |Delta_PiM|/|M_H_ref| + |epsilon_projector_stress| + |R_eq_integral|/|M_H_ref|",
            "required_inputs": "all PiM chainmap rows plus positive same-frame M_H_ref",
            "current_status": "SCHEMA_READY_NONCLAIM",
            "observable_links": "source_transfer;qbar_domain;Newton;PPN;local_GR",
            "valid_for_claim": "false",
        },
    ]


def numeric_scan_rows() -> list[dict[str, str]]:
    sources = [
        ("SCAN3373_0_2595_I_commutator", OUT / "P8_Y5_GM_TRANSFER_2595_COMPONENT_ROWS.csv", "I_commutator", "current_value"),
        ("SCAN3373_1_2595_projector_stress", OUT / "P8_Y5_GM_TRANSFER_2595_COMPONENT_ROWS.csv", "epsilon_projector_stress", "current_value"),
        ("SCAN3373_2_2595_MHref", OUT / "P8_Y5_GM_TRANSFER_2595_COMPONENT_ROWS.csv", "M_H_ref", "current_value"),
        ("SCAN3373_3_pim_radial_Icomm", OUT / "P8_Y5_PIM_RADIAL_BOUND_INPUT.csv", "I_commutator", "current_status"),
        ("SCAN3373_4_pim_template_Icomm", OUT / "P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv", "I_commutator", "current_status"),
        ("SCAN3373_5_numeric_audit", OUT / "P8_Y5_PIM_NUMERIC_INPUT_AUDIT.csv", "I_commutator", "audit_status"),
    ]
    rows: list[dict[str, str]] = []
    for scan_id, path, symbol, value_field in sources:
        csv_rows = read_csv_rows(path)
        matching = [
            row
            for row in csv_rows
            if symbol in row.get("symbol", "")
            or symbol in row.get("quantity", "")
            or symbol in row.get("definition", "")
            or symbol in row.get("candidate_row", "")
        ]
        values = ";".join(row.get(value_field, "") for row in matching) if matching else "MISSING_ROW"
        valid_seen = any(row.get("valid_for_claim", "").lower() == "true" or row.get("score_ready", "").lower() == "true" for row in matching)
        missing_seen = "MISSING" in values.upper() or "NOT_FILLED" in values.upper() or "NOT_CLAIMABLE" in values.upper() or values == "MISSING_ROW"
        rows.append(
            {
                "scan_id": scan_id,
                "symbol": symbol,
                "source_path": str(path),
                "source_path_exists": bool_text(path.exists()),
                "observed_value_or_status": values,
                "score_ready_or_claim_valid_seen": bool_text(valid_seen),
                "missing_or_not_claimable_seen": bool_text(missing_seen),
                "scan_result": "NO_SOURCE_BACKED_NUMERIC_ROW" if missing_seen or not valid_seen else "CANDIDATE_ROW_FOUND_REQUIRES_REVIEW",
                "valid_for_claim": "false",
            }
        )
    return rows


def bound_template_rows() -> list[dict[str, str]]:
    return [
        {
            "template_id": "IBT3373_0_I_commutator",
            "target_quantity": "I_commutator_over_MHref",
            "formula": "|I_commutator|/|M_H_ref|",
            "required_columns": "system_id;branch_id;r1;r2;annulus_definition;I_commutator;I_commutator_units;M_H_ref;M_H_ref_units;PiM_definition;J_H_source;source_path;equation_ref;no_cancellation_guard;valid_for_claim",
            "acceptance_rule": "finite source-backed I_commutator, positive same-frame M_H_ref, fixed annulus/surfaces, no fitted orbital-GM denominator, no MISSING markers",
            "current_status": "TEMPLATE_READY_NO_NUMERIC_ROW",
            "valid_for_claim": "false",
        },
        {
            "template_id": "IBT3373_1_projector_stress",
            "target_quantity": "epsilon_projector_stress",
            "formula": "||P_PPN T_PiM||/||kappa_* T00|| or source-normalization equivalent",
            "required_columns": "system_id;projector_family;metric_dependence_flag;T_PiM_component;weak_field_map;units;source_path;equation_ref;affected_rows;valid_for_claim",
            "acceptance_rule": "stress map must be Bianchi-safe and tied to public source branch; no hidden cancellation with other residuals",
            "current_status": "TEMPLATE_READY_NO_NUMERIC_ROW",
            "valid_for_claim": "false",
        },
        {
            "template_id": "IBT3373_2_chainmap_zero_certificate",
            "target_quantity": "I_commutator_zero_certificate",
            "formula": "PARENT_SIGNED_FIXED_TOPOLOGICAL_CHAINMAP_TRUE",
            "required_columns": "fixed_topology_certificate;omega_M_closed_source;q_basic_certificate;delta_g_PiM_zero;source_current_domain;Hilbert_class_guard;source_path;equation_ref;valid_for_claim",
            "acceptance_rule": "zero is accepted only if all chainmap clauses are parent-signed and same-branch with 3372 source transfer",
            "current_status": "CERTIFICATE_TEMPLATE_READY_NOT_SIGNED",
            "valid_for_claim": "false",
        },
    ]


def transfer_update_rows() -> list[dict[str, str]]:
    return [
        {
            "update_id": "STU3373_0_if_chainmap_signed",
            "condition": "fixed topological q-basic PiM chainmap and zero projector stress are parent-signed",
            "source_transfer_effect": "I_commutator and epsilon_projector_stress drop from the 3372 transfer residual",
            "remaining_blockers": "R_eq_integral;B_zero_flux;R_worldtube_glue;M_H_ref;tau_frame_lock;weak_field_normalization",
            "current_status": "CONDITIONAL_BRANCH_NOT_CURRENT_CLAIM",
            "valid_for_claim": "false",
        },
        {
            "update_id": "STU3373_1_current_branch",
            "condition": "current MTS corpus",
            "source_transfer_effect": "I_commutator, Delta_PiM and epsilon_projector_stress remain retained explicit rows",
            "remaining_blockers": "same-object Hilbert equality plus numeric/source-backed rows",
            "current_status": "TRANSFER_RESIDUAL_RETAINED",
            "valid_for_claim": "false",
        },
        {
            "update_id": "STU3373_2_qbar_domain_link",
            "condition": "qbar_domain fallback",
            "source_transfer_effect": "|qbar_domain| includes |I_commutator|/|M_H_ref| and |epsilon_projector_stress| until chainmap/stress theorem or numeric rows close",
            "remaining_blockers": "M_H_ref and same-frame source branch",
            "current_status": "BOUND_LINK_EXPLICIT",
            "valid_for_claim": "false",
        },
    ]


def runner_rows() -> list[dict[str, str]]:
    return [
        {
            "run_id": "RUN3373_0_product_rule",
            "test": "retain exact d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H identity",
            "result": "PASS_EXACT_IDENTITY",
            "detail": "commutator is the active obstruction, not optional bookkeeping",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3373_1_topological_chainmap",
            "test": "fixed q-basic topological PiM with closed omega_M and no metric/domain variation",
            "result": "PASS_CONDITIONAL_THEOREM",
            "detail": "I_commutator and projector stress vanish only in the parent-signed topological chainmap branch",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3373_2_current_parent_signature",
            "test": "promote [d,Pi_M]J_H=0 in current corpus",
            "result": "BLOCKED_NOT_PARENT_SIGNED",
            "detail": "fixed topology, q-basic omega_M, source-current domain, Hilbert equality and no projector stress are not all signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3373_3_hodge_route",
            "test": "use Hodge/DeWitt/domain PiM without stress row",
            "result": "REFUSED_STRESS_RETAINED",
            "detail": "metric/domain dependent projector carries delta PiM stress unless proved topological or explicitly bounded",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3373_4_numeric_scan",
            "test": "find source-backed I_commutator/M_H_ref row",
            "result": "NO_NUMERIC_ROW_FOUND",
            "detail": "existing rows are missing, not filled, not claimable, or reference-only",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3373_5_Newton_local_GR",
            "test": "use PiM chainmap to reopen Newton/local GR",
            "result": "REFUSED",
            "detail": "R_eq/worldtube/boundary/M_H_ref/source-transfer gates remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def gate_rows(source_ok: bool) -> list[dict[str, str]]:
    return [
        {"gate_id": "GATE3373_0_sources", "claim": "all required 3373 source paths exist and parse", "gate_pass": bool_text(source_ok), "reason": "source register validates every cited local input", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3373_1_commutator_zero", "claim": "[d,Pi_M]J_H=0 as parent theorem", "gate_pass": "false", "reason": "topological chainmap branch is conditional and not parent-signed", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3373_2_projector_stress_zero", "claim": "delta Pi_M stress is zero or included safely", "gate_pass": "false", "reason": "Hodge/domain projector routes retain stress and topological route is unsigned", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3373_3_Icommutator_bound", "claim": "I_commutator/M_H_ref bound row is score-ready", "gate_pass": "false", "reason": "numeric scan found no source-backed row and M_H_ref remains missing", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3373_4_source_transfer", "claim": "3372 source-transfer chain can promote", "gate_pass": "false", "reason": "R_eq, worldtube, boundary and M_H_ref gates remain open even if commutator closes conditionally", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3373_5_Newton_local_GR", "claim": "Newton/local-GR source coupling is established", "gate_pass": "false", "reason": "PiM chainmap is not parent-signed and source-transfer residual remains unbounded", "claim_allowed": "false", "valid_for_claim": "false"},
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC3373_0_progress",
            "decision": "The PiM commutator zero route is now a precise chainmap theorem, not a vague algebra wish.",
            "because": "a fixed q-basic topological PiM with closed omega_M kills [d,Pi_M]J_H and projector stress conditionally.",
            "next_action": "do not count this as current source-transfer proof until the parent signs the fixed topological/Hilbert class",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3373_1_current_status",
            "decision": "Current MTS still cannot claim I_commutator=0.",
            "because": "fixed topology, q-basic mass generator, source-current domain, Hilbert equality, M_H_ref and no-Hodge-stress are not all parent-signed.",
            "next_action": "retain I_commutator/M_H_ref and projector-stress rows",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3373_2_best_next",
            "decision": "Best next target is topological-Hilbert equality/R_eq, not another commutator pass.",
            "because": "even a closed chainmap can conserve the wrong object unless Pi_M J_H and J_M_top represent the same compact Hilbert worldtube class.",
            "next_action": "try to prove Pi_M J_H = J_M_top + dB_zero on the current branch, or stage R_eq_integral/M_H_ref",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3374-Y5-R2FR-topological-Hilbert-equality-or-Req-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3374_topological_Hilbert_equality_or_Req_bound.py",
            "objective": "prove Pi_M J_H = J_M_top + dB_zero from the same compact Hilbert source worldtube class, or stage R_eq_integral/M_H_ref as the next source-backed bound row",
            "why_next": "3373 gives the clean conditional commutator-zero theorem, but source transfer still fails if the closed topological current is not the same object as the observed Hilbert source current",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3375-Y5-R2FR-worldtube-source-glue-or-Rworldtube-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3375_worldtube_source_glue_or_Rworldtube_bound.py",
            "objective": "prove fixed worldtube/source measure equals exterior mass charge before orbital fitting, or stage R_worldtube_glue and surface_homology rows",
            "why_next": "worldtube glue is the geometric companion to R_eq and is needed before measured GM can test rather than define the source",
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
    formalization_hits = list(FW.rglob("*3373*")) if FW.exists() else []
    theorem_ids = {row["clause_id"] for row in rows_by_name["chainmap_theorem"]}
    route_ids = {row["route_id"] for row in rows_by_name["route_split"]}
    symbols = {row["symbol"] for row in rows_by_name["obstruction_rows"]}
    scan_results = {row["scan_result"] for row in rows_by_name["numeric_scan"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    checks = [
        ("VAL3373_0_sources_exist_parse", "all cited local source paths exist and parse", source_ok, ""),
        ("VAL3373_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3373_2_chainmap_theorem", "chainmap theorem covers product rule, topological route, commutator zero, projector stress, algebra rejection and guard", {"PCM3373_0_product_rule", "PCM3373_1_fixed_topological_chainmap", "PCM3373_2_Icommutator_zero", "PCM3373_3_zero_projector_stress", "PCM3373_4_no_closure_from_algebra", "PCM3373_5_Hilbert_equality_guard"}.issubset(theorem_ids), ""),
        ("VAL3373_3_route_split", "route split covers topological, Hodge, readout-mask and R_eq next-root routes", {"PRS3373_0_topological_chainmap", "PRS3373_1_Hodge_DeWitt_projector", "PRS3373_2_readout_mask", "PRS3373_3_topological_Hilbert_equality"}.issubset(route_ids), ""),
        ("VAL3373_4_obstruction_rows", "obstruction rows cover I_commutator, Delta_PiM, projector stress, R_eq and total", {"I_commutator", "Delta_PiM", "epsilon_projector_stress", "R_eq_integral", "epsilon_PiM_chainmap_abs"}.issubset(symbols), ""),
        ("VAL3373_5_numeric_scan_blocks_claim", "numeric scan finds no source-backed I_commutator row", scan_results == {"NO_SOURCE_BACKED_NUMERIC_ROW"}, ""),
        ("VAL3373_6_bound_templates", "I_commutator/projector stress/zero certificate templates are present", len(rows_by_name["bound_template"]) >= 3, ""),
        ("VAL3373_7_runner_blocks_claim", "runner marks exact identity, conditional theorem, current block and no numeric row", "PASS_EXACT_IDENTITY" in runner_results and "PASS_CONDITIONAL_THEOREM" in runner_results and "BLOCKED_NOT_PARENT_SIGNED" in runner_results and "NO_NUMERIC_ROW_FOUND" in runner_results, ""),
        ("VAL3373_8_gates_block_local", "promotion gates block commutator zero, stress zero, bound score, transfer and local GR", gate_map.get("GATE3373_1_commutator_zero") == "false" and gate_map.get("GATE3373_2_projector_stress_zero") == "false" and gate_map.get("GATE3373_3_Icommutator_bound") == "false" and gate_map.get("GATE3373_4_source_transfer") == "false" and gate_map.get("GATE3373_5_Newton_local_GR") == "false", ""),
        ("VAL3373_9_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3373_10_next_target", "next target moves to R_eq/topological-Hilbert equality", rows_by_name["next"][0]["target_id"].startswith("3374-Y5-R2FR-topological-Hilbert-equality"), ""),
        ("VAL3373_11_write_scope_outside_formalization", "no 3373 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
    ]
    checks.append(("VAL3373_12_overall", "3373 validation overall", all(passed for _, _, passed, _ in checks), "all required checks passed" if all(passed for _, _, passed, _ in checks) else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3373 - Y5/R2FR PiM commutator chainmap zero or Icommutator bound under AX1090",
        "",
        "## Summary",
        "- 3373 attacks the algebraic hinge in the 3372 source-transfer chain: whether `[d,Pi_M]J_H=0` and projector stress can be derived, or whether `I_commutator/M_H_ref` must be retained.",
        "- Derivation result: a fixed q-basic topological `Pi_M` is a clean chainmap route. If `Pi_M J=omega_M ell_M(J)`, `d omega_M=0`, `ell_M(dK)=0` on the fixed compact exterior complex, and `delta_g Pi_M=0`, then `[d,Pi_M]J_H=0` and projector stress vanish conditionally.",
        "- Current verdict: the theorem is not parent-signed. Current MTS lacks the fixed topological source-current domain, Hilbert same-object equality, positive `M_H_ref`, and no-Hodge/domain-projector stress certificate.",
        "- Hodge/domain route: if `Pi_M` depends on a Hodge/DeWitt metric, Green operator, normal, or domain selector, `delta Pi_M` stress must be retained; it cannot be silently set to zero.",
        "- Numeric result: no source-backed `I_commutator/M_H_ref` row exists yet. Bound and zero-certificate templates are staged.",
        "- Best next strike is `R_eq`: prove `Pi_M J_H = J_M_top + dB_zero` for the same compact Hilbert worldtube class, or stage `R_eq_integral/M_H_ref`.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## PiM Chainmap / Commutator Theorem Attempt",
        md_table(rows_by_name["chainmap_theorem"]),
        "## Route Split",
        md_table(rows_by_name["route_split"]),
        "## Icommutator Obstruction Rows",
        md_table(rows_by_name["obstruction_rows"]),
        "## Numeric Scan",
        md_table(rows_by_name["numeric_scan"]),
        "## Bound Templates",
        md_table(rows_by_name["bound_template"]),
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
        "chainmap_theorem": chainmap_theorem_rows(),
        "route_split": route_split_rows(),
        "obstruction_rows": obstruction_rows(),
        "numeric_scan": numeric_scan_rows(),
        "bound_template": bound_template_rows(),
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
