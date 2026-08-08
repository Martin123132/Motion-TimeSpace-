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
DOC = ROOT / "3370-Y5-R2FR-no-shadow-frame-no-marker-matter-functor-or-first-qbar-component-bound-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3370_SOURCE_REGISTER.csv",
    "terminal_recheck": OUT / "P8_Y5_R2FR_3370_TERMINAL_PUBLIC_METRIC_RECHECK.csv",
    "theorem": OUT / "P8_Y5_R2FR_3370_NO_SHADOW_NO_MARKER_THEOREM.csv",
    "bound_rows": OUT / "P8_Y5_R2FR_3370_QBAR_GEOM_MARKER_BOUND_ROWS_NONCLAIM.csv",
    "countermodels": OUT / "P8_Y5_R2FR_3370_COUNTERMODEL_LEDGER.csv",
    "runner": OUT / "P8_Y5_R2FR_3370_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3370_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3370_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3370_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3370_VALIDATION.csv",
}

LOCAL_SOURCES = [
    (
        "SRC3370_0_3369_doc",
        ROOT / "3369-Y5-R2FR-extra-response-Y5-source-zero-or-qbarXT-bound-row-under-AX1090.md",
        "3369 current-branch qbar_XT chain-rule source-zero and component envelope",
    ),
    (
        "SRC3370_1_3369_next",
        OUT / "P8_Y5_R2FR_3369_NEXT_TARGET.csv",
        "3369 selects no-shadow/no-marker matter functor as 3370 target",
    ),
    (
        "SRC3370_2_3369_premise",
        OUT / "P8_Y5_R2FR_3369_QBARXT_PARENT_PREMISE_AUDIT.csv",
        "3369 premise audit for q, coframe, matter functor, marker constants and hidden tails",
    ),
    (
        "SRC3370_3_3369_components",
        OUT / "P8_Y5_R2FR_3369_QBARXT_COMPONENT_ROWS_NONCLAIM.csv",
        "3369 qbar_geom and qbar_marker component rows",
    ),
    (
        "SRC3370_4_1028_doc",
        ROOT / "1028-Y5-R10-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md",
        "older no-marker theorem audit and frame/marker bound pack",
    ),
    (
        "SRC3370_5_1029_doc",
        ROOT / "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md",
        "older c_g no-shadow-frame theorem and first numeric coupling row target",
    ),
    (
        "SRC3370_6_1030_doc",
        ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
        "single-public-metric parent-action derivation attempt and shortcut rejections",
    ),
    (
        "SRC3370_7_1031_doc",
        ROOT / "1031-Y5-R10-quotient-naturality-terminal-public-metric-proof-or-spm-closure.md",
        "terminal public metric proof audit and SPM closure verdict",
    ),
    (
        "SRC3370_8_1031_terminal_csv",
        OUT / "P8_Y5_R10_1031_TERMINAL_PUBLIC_METRIC_PROOF_AUDIT.csv",
        "machine-readable terminal-public-metric proof audit",
    ),
    (
        "SRC3370_9_1030_spm_csv",
        OUT / "P8_Y5_R10_1030_PUBLIC_METRIC_ACTION_CONTRACT.csv",
        "machine-readable single-public-metric action contract if present",
    ),
    (
        "SRC3370_10_1029_counter_csv",
        OUT / "P8_Y5_R10_1029_COUNTEREXAMPLE_LEDGER.csv",
        "frame-relabel, common-frame and disformal counterexamples",
    ),
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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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


def terminal_recheck_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "TPR3370_0_3369_target_import",
            "question": "What exactly must 3370 close for the current R2FR branch?",
            "result": "qbar_geom and qbar_marker are the first two visible source-normalization components blocking qbar_XT=0",
            "evidence": "PRE3369_1/PRE3369_3 and QBC3369_0/QBC3369_1",
            "status": "TARGET_SHARPENED",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "TPR3370_1_terminality_alone",
            "question": "Does a terminal public metric/coframe object alone forbid shadow frames?",
            "result": "No. A functor may depend on a non-terminal frame, label, marker, or source normalization before the terminal map.",
            "evidence": "TPM1031_5 and TC1031_0 through TC1031_3",
            "status": "SHORTCUT_REJECTED",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "TPR3370_2_full_contract",
            "question": "What contract would actually kill qbar_geom and qbar_marker?",
            "result": "Q_obs object class plus terminal e_pub plus matter-interface functor through e_pub only plus field-rename guard plus q-kernel ownership.",
            "evidence": "TPM1031_6, SPM1030_1 through SPM1030_6, 3369 premise audit",
            "status": "EXACT_PARENT_SIGNATURE_CONTRACT",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "TPR3370_3_no_shadow_chain_rule",
            "question": "If the full contract is signed, what happens to a Weyl/disformal shadow frame?",
            "result": "A_g and B_g are either absent ordinary-matter arguments or quotient-owned functions; for vertical X, Lie_X ln A_g=0 and Lie_X B_g=0.",
            "evidence": "NST1029_1, TPM1031_3 and chain rule",
            "status": "VALID_CONDITIONAL_THEOREM",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "TPR3370_4_no_marker_chain_rule",
            "question": "If constants and readout markers are quotient-owned, what happens to b_A and b_alpha?",
            "result": "theta_A=theta_A(q) and alpha_EM=alpha_EM(q) give Lie_X theta_A=0 and Lie_X alpha_EM=0 whenever Dq[X]=0.",
            "evidence": "NM1028 audit, PRE3369_3 and chain rule",
            "status": "VALID_CONDITIONAL_THEOREM",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "TPR3370_5_current_verdict",
            "question": "Can current MTS claim no-shadow/no-marker from the parent corpus?",
            "result": "Not yet. The theorem is exact as a branch contract, but the parent action has not signed Q_obs/domain uniqueness, no-extra-frame, no-marker and same-branch clauses together.",
            "evidence": "TPM1031_6, SPM1031 closure branch, PRE3369_5",
            "status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
    ]


def theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "NSM3370_0_matter_functor_domain",
            "statement": "Ordinary matter/readout has source action S_matter = Sbar[Psi, e_pub(q(Phi)), omega[e_pub], theta(q(Phi))] with no representative-field slot.",
            "derivation": "This is the exact domain restriction needed to make representative X invisible to ordinary source/readout variation; it cannot be inferred from covariance, WEP or Ward identities alone.",
            "if_parent_signed_then": "Lie_X S_matter has only Lie_X q terms, hence vanishes for X in ker(Dq).",
            "current_status": "CONTRACT_READY_NOT_PARENT_THEOREM",
            "blocks_current_claim": "matter-interface/domain uniqueness is not parent-signed",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "NSM3370_1_no_shadow_frame",
            "statement": "No ordinary matter metric may contain an independent A_g(X) e_pub or disformal B_g(X) channel outside the quotient-owned public coframe.",
            "derivation": "If A_g/B_g are not arguments, their vertical derivatives are absent. If A_g=Abar(q) and B_g=Bbar(q), Dq[X]=0 gives c_g=Lie_X ln A_g=0 and b_dis=Lie_X B_g=0.",
            "if_parent_signed_then": "qbar_geom=0 for the Weyl/disformal frame-leak piece.",
            "current_status": "VALID_CONDITIONAL_THEOREM",
            "blocks_current_claim": "common Jordan frame, disformal shadow and frame-relabel countermodels remain legal without parent exclusion",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "NSM3370_2_no_marker_constants",
            "statement": "Masses, material constants, EM constants, clock constants and readout markers are quotient-owned or explicitly retained as residual coefficients.",
            "derivation": "For theta_A=theta_A(q), b_A=Lie_X ln theta_A=0. For alpha_EM=alpha_EM(q), b_alpha=Lie_X ln alpha_EM=0. Any non-quotient marker must be retained in the qbar_marker bound.",
            "if_parent_signed_then": "qbar_marker=0 for ordinary constants/readout-marker leakage.",
            "current_status": "VALID_CONDITIONAL_THEOREM",
            "blocks_current_claim": "no-marker theorem is not parent-signed across masses, EM, clock readout and material sensitivities",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "NSM3370_3_combined_visible_source_zero",
            "statement": "Under q-verticality plus the no-shadow-frame/no-marker matter-functor contract, qbar_geom=qbar_marker=0 and the visible ordinary source leg of qbar_XT loses its two largest leakage families.",
            "derivation": "Apply the vertical chain rule to e_pub(q), Abar(q), Bbar(q), theta_A(q) and alpha_EM(q); every visible source/readout variation is proportional to Dq[X].",
            "if_parent_signed_then": "the 3369 qbar_XT envelope drops to qbar_nonH+qbar_support+qbar_boundary+qbar_domain.",
            "current_status": "CONDITIONAL_BRANCH_SIMPLIFICATION",
            "blocks_current_claim": "hidden/source/support/domain/boundary tails and same-branch certificate remain open even if this branch is signed",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "NSM3370_4_current_claim_ceiling",
            "statement": "Current branch may use no-shadow/no-marker only as a conditional theorem or explicit closure branch, not as a derived local-GR claim.",
            "derivation": "1031 demoted Single Public Metric to closure because terminality does not restrict the matter action domain; 3369 still requires one same-branch parent certificate.",
            "if_parent_signed_then": "promote only after the parent action signs the complete contract and hidden/source tails close in the same branch",
            "current_status": "NOT_DERIVED_CURRENT_CORPUS",
            "blocks_current_claim": "missing parent signature and hidden-tail closure",
            "valid_for_claim": "false",
        },
    ]


def bound_rows() -> list[dict[str, str]]:
    return [
        {
            "row_id": "QGM3370_0_qbar_geom",
            "symbol": "qbar_geom",
            "definition": "ordinary test/source X charge from Weyl/disformal observed-frame leakage",
            "zero_condition": "no independent A_g(X) or B_g(X) matter-frame slot, or A_g/B_g factor only through q",
            "bound_formula": "|qbar_geom| <= |tau_g c_g| + |tau_dis b_dis|",
            "required_inputs": "tau_g, c_g, tau_dis, b_dis, arena projection and source path",
            "current_status": "THEOREM_CONDITIONAL_VALUES_MISSING",
            "observable_links": "R10;PPN;clock;WEP-common;local_GR_source",
            "valid_for_claim": "false",
        },
        {
            "row_id": "QGM3370_1_qbar_marker",
            "symbol": "qbar_marker",
            "definition": "ordinary source/readout X charge from masses, material constants, EM constants, clocks and markers",
            "zero_condition": "theta_A, alpha_EM and clock/readout constants are quotient-owned or retained as explicit residuals",
            "bound_formula": "|qbar_marker| <= sum_A |s_A b_A| + |s_alpha b_alpha|",
            "required_inputs": "material sensitivities s_A, b_A rows, s_alpha, b_alpha, composition/readout source paths",
            "current_status": "THEOREM_CONDITIONAL_VALUES_MISSING",
            "observable_links": "WEP;composition_clocks;alpha_EM;R10_materials;atomic_readout",
            "valid_for_claim": "false",
        },
        {
            "row_id": "QGM3370_2_visible_combined",
            "symbol": "qbar_geom_marker_bound_abs",
            "definition": "visible ordinary frame-plus-marker source-normalization leakage envelope",
            "zero_condition": "QGM3370_0 and QGM3370_1 are theorem-zero in the same parent branch",
            "bound_formula": "|qbar_geom_marker| <= |tau_g c_g| + |tau_dis b_dis| + sum_A |s_A b_A| + |s_alpha b_alpha|",
            "required_inputs": "all qbar_geom and qbar_marker inputs, with no cancellation between signs",
            "current_status": "SCHEMA_READY_NONCLAIM",
            "observable_links": "R_nonEH;Newton_source;local_GR;R10;PPN;clock;WEP",
            "valid_for_claim": "false",
        },
        {
            "row_id": "QGM3370_3_remaining_qbarXT",
            "symbol": "qbar_XT_bound_after_visible_contract",
            "definition": "3369 total qbar_XT envelope after conditional removal of visible frame/marker pieces",
            "zero_condition": "no-shadow/no-marker plus hidden non-Hilbert, support, boundary and domain tails all close in one branch",
            "bound_formula": "|qbar_XT| <= |qbar_geom_marker| + |qbar_nonH| + |qbar_support| + |qbar_boundary| + |qbar_domain|",
            "required_inputs": "3370 visible bound rows plus 3371 hidden/source/support/domain rows",
            "current_status": "BLOCKED_PENDING_3371",
            "observable_links": "local_GR;Newton;source_mass;orbital;PPN;R10",
            "valid_for_claim": "false",
        },
    ]


def countermodel_rows() -> list[dict[str, str]]:
    return [
        {
            "countermodel_id": "CM3370_0_common_Jordan_frame",
            "surviving_if": "ordinary matter may use g_m=A_g(X)^2 g_pub",
            "what_survives": "c_g source charge",
            "why_shortcut_fails": "composition WEP can be quiet for a universal frame while common fifth-force/source-normalization effects remain",
            "repair": "prove no-shadow-frame parent domain or source c_g/tau rows",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM3370_1_disformal_shadow",
            "surviving_if": "ordinary matter may use g_m=A_g^2 g_pub+B_g(X)U_mu U_nu",
            "what_survives": "b_dis and velocity/profile dependent local residuals",
            "why_shortcut_fails": "conformal-only checks do not kill disformal response",
            "repair": "include disformal slot in no-shadow theorem or retain tau_dis b_dis bound row",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM3370_2_marker_constants",
            "surviving_if": "m_A, alpha_EM, material constants or clock readout markers depend on X",
            "what_survives": "b_A, b_alpha and material sensitivity terms",
            "why_shortcut_fails": "qbar_geom can vanish while qbar_marker remains",
            "repair": "prove quotient-owned constants/no-marker theorem or source composition-clock and alpha rows",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM3370_3_terminal_label",
            "surviving_if": "Q_obs has a terminal metric but matter functor depends on a non-terminal label before mapping to it",
            "what_survives": "source weights, labels or readout offsets hidden behind terminality",
            "why_shortcut_fails": "terminality is a morphism property, not an action-domain exclusion",
            "repair": "parent-sign terminal-evaluation-only matter functor",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM3370_4_field_rename",
            "surviving_if": "A_g is set to one by redefining constants, G_eff, source mass or clock units",
            "what_survives": "same coupling moves into qbar_marker, qbar_nonH or DeltaGM calibration residual",
            "why_shortcut_fails": "choosing variables does not remove physical source/readout derivatives",
            "repair": "same-branch ledger across geometry, constants, active source, support and measured-GM calibration",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM3370_5_source_only_weight",
            "surviving_if": "matter metric is public but active source normalization carries w_A(X)",
            "what_survives": "hidden non-Hilbert/source-weight tail",
            "why_shortcut_fails": "no-shadow frame does not by itself define the total active source",
            "repair": "3371 hidden-source/support-tail zero proof or qbar_nonH bound",
            "valid_for_claim": "false",
        },
    ]


def runner_rows() -> list[dict[str, str]]:
    return [
        {
            "run_id": "RUN3370_0_strict_descent_branch",
            "test": "q-verticality plus terminal-evaluation-only matter functor plus quotient-owned constants",
            "result": "PASS_CONDITIONAL_THEOREM",
            "detail": "chain rule gives c_g=b_dis=b_A=b_alpha=0 inside that branch",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3370_1_terminality_only",
            "test": "terminal public metric without matter-domain restriction",
            "result": "FAILS_AS_PROOF",
            "detail": "matter can depend on non-terminal objects or labels before the terminal map",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3370_2_covariance_WEP_Ward",
            "test": "derive no-shadow/no-marker from covariance, WEP or Ward identities",
            "result": "SHORTCUTS_REJECTED",
            "detail": "all three allow universal frame, marker, or source-normalization couplings",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3370_3_current_corpus_zero",
            "test": "promote qbar_geom=qbar_marker=0 in current corpus",
            "result": "BLOCKED_NOT_PARENT_SIGNED",
            "detail": "parent action has not signed full Q_obs/domain/constant/no-extra-slot/same-branch certificate",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3370_4_bound_rows",
            "test": "fallback to first qbar_geom/qbar_marker bound rows",
            "result": "SCHEMA_READY_UNSCOREABLE",
            "detail": "formulas and arenas are explicit, but c_g, b_dis, b_A, b_alpha, tau and sensitivity rows are not numeric/source-backed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3370_5_local_GR",
            "test": "use 3370 to claim local GR/Newton/source-side pass",
            "result": "REFUSED",
            "detail": "even signed visible source-zero would still need hidden-tail 3371 and left-hand EH/Newton gates",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def gate_rows(source_ok: bool) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE3370_0_sources",
            "claim": "all required 3370 source paths exist and parse",
            "gate_pass": bool_text(source_ok),
            "reason": "source register validates every cited local input",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3370_1_no_shadow_zero",
            "claim": "c_g=b_dis=0 as parent theorem",
            "gate_pass": "false",
            "reason": "no-extra-frame and matter-interface uniqueness are conditional, not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3370_2_no_marker_zero",
            "claim": "b_A=b_alpha=0 as parent theorem",
            "gate_pass": "false",
            "reason": "quotient-owned constants/no-marker theorem is not signed across masses, EM, clock and material readouts",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3370_3_visible_qbar_zero",
            "claim": "qbar_geom=qbar_marker=0 in the current branch",
            "gate_pass": "false",
            "reason": "the visible theorem is valid only under an unsigned parent contract",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3370_4_bound_score",
            "claim": "finite qbar_geom/qbar_marker bounds can be scored",
            "gate_pass": "false",
            "reason": "no numeric/source-backed c_g, b_dis, b_A, b_alpha, tau or sensitivity rows exist",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3370_5_local_GR",
            "claim": "local GR/Newton reduction follows",
            "gate_pass": "false",
            "reason": "hidden-source/support/domain tails and left-hand EH/Newton gates remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC3370_0_progress",
            "decision": "The no-shadow/no-marker target is now an exact current-branch conditional theorem plus a fallback bound row.",
            "because": "3370 ports the older 1028-1031 frame/marker results into the 3369 qbar_XT/R_nonEH stack and names the first visible leakage components.",
            "next_action": "do not recircle c_g; attack the hidden/source/support/domain tails that still survive even if visible source-zero is granted",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3370_1_claim_ceiling",
            "decision": "No local-GR/Newton/R10/PPN/clock claim is allowed from 3370.",
            "because": "the parent action has not signed the complete matter-functor contract and the fallback rows are nonnumeric.",
            "next_action": "keep 3370 as a derivation contract and nonclaim acquisition ledger",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3370_2_best_next",
            "decision": "Best next target is 3371 hidden-source/support-tail zero or qbar_nonH bound.",
            "because": "even a perfect no-shadow/no-marker proof only removes qbar_geom and qbar_marker; qbar_nonH, qbar_support, qbar_boundary and qbar_domain still block qbar_XT=0.",
            "next_action": "build 3371 and try to prove total active source is Hilbert/public-support only, else emit qbar_nonH/support/domain bound rows",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3370_3_parallel_parent_route",
            "decision": "A deeper parent-signature route remains available but should not replace 3371.",
            "because": "terminal public metric/domain uniqueness would improve the theorem status, but hidden source tails are independently required for local source coupling.",
            "next_action": "reserve a later parent-action signature checkpoint after hidden-tail decomposition is explicit",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3371-Y5-R2FR-hidden-source-support-tail-zero-or-qbar-nonH-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3371_hidden_source_support_tail_zero_or_qbar_nonH_bound.py",
            "objective": "prove no hidden non-Hilbert/source-support/domain tail contributes to qbar_XT, or write qbar_nonH/qbar_support/qbar_domain bound rows",
            "why_next": "3370 narrows visible frame/marker leakage to conditional theorem or explicit bound rows; total source normalization still fails unless hidden/support/domain tails close",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3372-Y5-R2FR-parent-matter-functor-signature-or-explicit-SPM-closure-sync.md",
            "target_script": "scripts/Y5_R2FR_3372_parent_matter_functor_signature_or_explicit_spm_closure_sync.py",
            "objective": "attempt to parent-sign the terminal-evaluation-only matter functor, no-shadow-frame and no-marker constants contract in one branch, or lock it as explicit SPM closure only",
            "why_next": "this is the deeper derivation route for turning 3370 from conditional theorem into parent theorem, but it should follow hidden-tail decomposition to avoid circling c_g",
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
    formalization_hits = list(FW.rglob("*3370*")) if FW.exists() else []

    theorem_ids = {row["theorem_id"] for row in rows_by_name["theorem"]}
    bound_symbols = {row["symbol"] for row in rows_by_name["bound_rows"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}

    checks = [
        (
            "VAL3370_0_sources_exist_parse",
            "all cited local source paths exist and parse",
            source_ok,
            "",
        ),
        (
            "VAL3370_1_outputs_parse",
            "all generated CSV outputs parse cleanly",
            len(parse_results) == len(output_csvs) and all(parse_results),
            f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}",
        ),
        (
            "VAL3370_2_terminal_recheck",
            "terminal recheck rejects terminality-alone and identifies full contract",
            any(row["status"] == "SHORTCUT_REJECTED" for row in rows_by_name["terminal_recheck"])
            and any(row["status"] == "EXACT_PARENT_SIGNATURE_CONTRACT" for row in rows_by_name["terminal_recheck"]),
            "",
        ),
        (
            "VAL3370_3_theorem_rows",
            "theorem rows cover matter functor, no-shadow frame, no-marker constants and claim ceiling",
            {
                "NSM3370_0_matter_functor_domain",
                "NSM3370_1_no_shadow_frame",
                "NSM3370_2_no_marker_constants",
                "NSM3370_4_current_claim_ceiling",
            }.issubset(theorem_ids),
            "",
        ),
        (
            "VAL3370_4_bound_rows",
            "bound rows cover qbar_geom, qbar_marker, visible combined and remaining qbarXT",
            {
                "qbar_geom",
                "qbar_marker",
                "qbar_geom_marker_bound_abs",
                "qbar_XT_bound_after_visible_contract",
            }.issubset(bound_symbols),
            "",
        ),
        (
            "VAL3370_5_countermodels",
            "countermodels block common frame, disformal, marker, terminal-label, rename and source-only shortcuts",
            len(rows_by_name["countermodels"]) >= 6,
            "",
        ),
        (
            "VAL3370_6_runner_blocks_claim",
            "runner keeps current zero/local-GR claims blocked",
            "BLOCKED_NOT_PARENT_SIGNED" in runner_results and "REFUSED" in runner_results,
            "",
        ),
        (
            "VAL3370_7_gates_block_local",
            "promotion gates block visible qbar zero, bound score and local GR",
            gate_map.get("GATE3370_3_visible_qbar_zero") == "false"
            and gate_map.get("GATE3370_4_bound_score") == "false"
            and gate_map.get("GATE3370_5_local_GR") == "false",
            "",
        ),
        (
            "VAL3370_8_no_overclaim_flags",
            "all generated rows with valid_for_claim remain false",
            flags_ok,
            flag_detail,
        ),
        (
            "VAL3370_9_next_target",
            "next target moves to hidden/source/support tails instead of recircling c_g",
            rows_by_name["next"][0]["target_id"].startswith("3371-Y5-R2FR-hidden-source-support-tail"),
            "",
        ),
        (
            "VAL3370_10_write_scope_outside_formalization",
            "no 3370 files were written under formalization-workbench",
            not formalization_hits,
            f"hits={len(formalization_hits)}",
        ),
    ]
    checks.append(
        (
            "VAL3370_11_overall",
            "3370 validation overall",
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
        "# 3370 - Y5/R2FR no-shadow-frame no-marker matter functor or first qbar component bound under AX1090",
        "",
        "## Summary",
        "- 3370 ports the older no-shadow/no-marker work into the current `qbar_XT` / `R_nonEH` branch rather than leaving it as an R10 sidecar.",
        "- Derivation result: the no-shadow/no-marker route is a valid conditional theorem. If ordinary matter/readout is restricted to `S_matter=Sbar[Psi,e_pub(q(Phi)),omega[e_pub],theta(q(Phi))]` and `X in ker(Dq)`, then `c_g=b_dis=b_A=b_alpha=0`, so `qbar_geom=qbar_marker=0`.",
        "- Current verdict: this is not yet a parent theorem. Terminality alone, covariance, WEP and Ward identities do not exclude shadow frames, markers, source weights, or field-renames.",
        "- Fallback result: the first visible leakage rows are now explicit nonclaim bound rows: `|qbar_geom| <= |tau_g c_g| + |tau_dis b_dis|` and `|qbar_marker| <= sum_A |s_A b_A| + |s_alpha b_alpha|`.",
        "- Best next strike is 3371: hidden non-Hilbert/source-support/domain tails. Even a perfect 3370 branch does not by itself prove total local source coupling or local GR.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## Terminal Public Metric Recheck",
        md_table(rows_by_name["terminal_recheck"]),
        "## No-shadow / No-marker Theorem",
        md_table(rows_by_name["theorem"]),
        "## First Visible qbar Bound Rows",
        md_table(rows_by_name["bound_rows"]),
        "## Countermodel Ledger",
        md_table(rows_by_name["countermodels"]),
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
        "terminal_recheck": terminal_recheck_rows(),
        "theorem": theorem_rows(),
        "bound_rows": bound_rows(),
        "countermodels": countermodel_rows(),
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
