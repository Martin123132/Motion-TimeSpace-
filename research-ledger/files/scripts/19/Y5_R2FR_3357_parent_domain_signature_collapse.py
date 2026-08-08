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
DOC = ROOT / "3357-Y5-R2FR-parent-domain-signature-collapse-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

LOCAL_SOURCES = [
    ("LSRC3357_0_3346_normal", OUT / "P8_Y5_R2FR_3346_PARENT_ACTION_NORMAL_FORM.csv", "3346 candidate parent action normal form"),
    ("LSRC3357_1_3346_allowed", OUT / "P8_Y5_R2FR_3346_ALLOWED_ARGUMENT_INVENTORY.csv", "3346 allowed argument inventory"),
    ("LSRC3357_2_3346_forbidden", OUT / "P8_Y5_R2FR_3346_FORBIDDEN_ARGUMENT_INVENTORY.csv", "3346 forbidden argument inventory"),
    ("LSRC3357_3_3346_closure", OUT / "P8_Y5_R2FR_3346_CLOSURE_CERTIFICATE_ATTEMPT.csv", "3346 closure status"),
    ("LSRC3357_4_3354_alias", OUT / "P8_Y5_R2FR_3354_ALIAS_FAMILY_INVENTORY.csv", "3354 alias closure inventory"),
    ("LSRC3357_5_3354_lemmas", OUT / "P8_Y5_R2FR_3354_ALIAS_ZERO_LEMMA_STEPS.csv", "3354 alias zero lemmas"),
    ("LSRC3357_6_3355_boundary", OUT / "P8_Y5_R2FR_3355_BOUNDARY_CONTACT_DECOMPOSITION.csv", "3355 boundary/contact split"),
    ("LSRC3357_7_3356_collar", OUT / "P8_Y5_R2FR_3356_LOCAL_COLLAR_SUPPORT_THEOREM.csv", "3356 collar support theorem"),
    ("LSRC3357_8_3356_eps", OUT / "P8_Y5_R2FR_3356_EPSILON_CONTACT_UPDATE.csv", "3356 epsilon contact update"),
    ("LSRC3357_9_3356_gates", OUT / "P8_Y5_R2FR_3356_PROMOTION_GATES.csv", "3356 gates"),
]

OUTPUTS = {
    "local_sources": OUT / "P8_Y5_R2FR_3357_LOCAL_SOURCE_REGISTER.csv",
    "signature": OUT / "P8_Y5_R2FR_3357_PARENT_DOMAIN_SIGNATURE_CLAUSES.csv",
    "theorem": OUT / "P8_Y5_R2FR_3357_COLLAPSE_THEOREM_PACKET.csv",
    "residuals": OUT / "P8_Y5_R2FR_3357_RESIDUAL_COLLAPSE_MATRIX.csv",
    "scope": OUT / "P8_Y5_R2FR_3357_CLAIM_SCOPE_SEPARATION.csv",
    "gates": OUT / "P8_Y5_R2FR_3357_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3357_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3357_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3357_VALIDATION.csv",
}


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1800) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: compact(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parseable(path: Path) -> bool:
    try:
        if path.suffix.lower() == ".csv":
            read_csv(path)
        else:
            path.read_text(encoding="utf-8")
        return True
    except Exception:
        return False


def table(rows: list[dict[str, Any]]) -> str:
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
        lines.append("| " + " | ".join(compact(row.get(key, ""), 260).replace("|", "\\|") for key in headers) + " |")
    return "\n".join(lines) + "\n"


def local_source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": bool_str(path.exists()),
            "parseable": bool_str(path.exists() and parseable(path)),
            "usage": usage,
            "valid_for_claim": "false",
        }
        for source_id, path, usage in LOCAL_SOURCES
    ]


def signature_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "SIG3357_0_q_visible_domain",
            "parent_domain_clause": "ordinary matter and EM depend on parent fields only through q-visible geometry/coframe and action-owned gauge/current data",
            "source_authority": "ARG3346_A1; NF3346_0",
            "effect_if_signed": "vertical hidden directions do not vary ordinary matter/EM stress",
            "current_status": "CONDITIONAL_CONTRACT_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "SIG3357_1_single_Hilbert_source_owner",
            "parent_domain_clause": "active source equals Hilbert stress from S_matter + S_EM before readout/source labels",
            "source_authority": "NF3346_2; ARG3346_A2; ARG3346_A3",
            "effect_if_signed": "T_active = T_H^matter + T_H^EM; no post-variation source weights",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "SIG3357_2_no_hidden_coefficients_or_frames",
            "parent_domain_clause": "no hidden coefficient maps, no hidden matter frame, no disformal labelled geometry",
            "source_authority": "ARG3346_F0; ARG3346_F3; GATE3354_1",
            "effect_if_signed": "c_g, b_dis, b_alpha-style ordinary-frame leakage vanishes on the local bulk branch",
            "current_status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "SIG3357_3_no_source_projector_shadow",
            "parent_domain_clause": "no source-only weights, F_shadow, P_material, or P_D/T_D aliases in Args(S_parent)",
            "source_authority": "ARG3346_F1; ARG3346_F2; ARG3346_F5; GATE3354_0",
            "effect_if_signed": "epsilon_source_shadow and alpha_D P_D vanish for the parent bulk source",
            "current_status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "SIG3357_4_readout_after_variation",
            "parent_domain_clause": "P_read/R_read are post-solution maps, not varied parent-action arguments",
            "source_authority": "NF3346_1; ARG3346_F4; GATE3354_2",
            "effect_if_signed": "readout source-shadow is demoted to S_red/readout artifact",
            "current_status": "CONDITIONAL_DEMOTION_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "SIG3357_5_boundary_local_bulk_collar",
            "parent_domain_clause": "local bulk variations are compactly supported away from boundary/contact support",
            "source_authority": "GATE3355_0; GATE3356_0",
            "effect_if_signed": "epsilon_boundary_contact[p]=0 for p outside contact support",
            "current_status": "EXACT_LOCAL_POINTWISE_LEMMA",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "SIG3357_6_surface_integrated_exception",
            "parent_domain_clause": "surface/contact stress is ordinary Hilbert-owned, universal monopole-only, zero, or source-backed bounded",
            "source_authority": "GATE3356_1; GATE3356_2",
            "effect_if_signed": "Newton/PPN integrated source normalization closes",
            "current_status": "OPEN_NOT_SIGNED",
            "valid_for_claim": "false",
        },
    ]


def theorem_packet_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "THM3357_0_parent_action_domain",
            "statement": "Assume SIG3357_0 through SIG3357_5 for the local bulk arena.",
            "derivation_effect": "all ordinary source couplings are q-visible, Hilbert-owned, and readout-free before variation",
            "result": "AX1090_CONDITIONAL_PREMISE_PACKET",
            "valid_for_claim": "false",
        },
        {
            "step_id": "THM3357_1_vertical_hidden_silence",
            "statement": "For v in ker(Dq), delta_v S_matter and delta_v S_EM vanish in the ordinary local bulk source.",
            "derivation_effect": "delta_v S[q(Phi)] = <delta S/dq, Dq(v)> = 0; hidden frames/coefficient aliases are excluded",
            "result": "CONDITIONAL_ZERO",
            "valid_for_claim": "false",
        },
        {
            "step_id": "THM3357_2_Hilbert_source_identity",
            "statement": "The local active source is T_H^{matter}+T_H^{EM} from the same varied action.",
            "derivation_effect": "T_active := -2/sqrt(|g_obs|) delta(S_matter+S_EM)/delta g_obs before source labels/readout",
            "result": "CONDITIONAL_SOURCE_IDENTITY",
            "valid_for_claim": "false",
        },
        {
            "step_id": "THM3357_3_alias_residual_collapse",
            "statement": "source-shadow, hidden-frame, readout, decoupled-block, and local bulk boundary aliases collapse to zero/demotion under the packet.",
            "derivation_effect": "3354 alias lemmas + 3356 collar theorem remove the named fake-source routes in the pointwise bulk arena",
            "result": "LOCAL_BULK_RESIDUALS_ZERO_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "step_id": "THM3357_4_surface_exception",
            "statement": "Surface/contact and integrated multipole source normalization are not closed by the local bulk theorem.",
            "derivation_effect": "whole-body Newton/PPN observables can receive contact distributions unless ordinary-owned, monopole-only, zero, or bounded",
            "result": "EXPLICIT_EXCEPTION_RETAINED",
            "valid_for_claim": "false",
        },
        {
            "step_id": "THM3357_5_current_verdict",
            "statement": "The AX1090 parent-domain packet is a serious conditional local-bulk source theorem, not yet a parent-signed MTS theorem.",
            "derivation_effect": "turns many local-GR blockers into one parent-domain signature problem plus surface/integrated source residual",
            "result": "PROMOTE_TO_INTERNAL_THEOREM_TARGET_NOT_PUBLIC_CLAIM",
            "valid_for_claim": "false",
        },
    ]


def residual_collapse_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RC3357_0_epsilon_source_shadow",
            "residual": "epsilon_source_shadow",
            "bulk_result_under_packet": "0",
            "reason": "single Hilbert source owner; no F_shadow/P_material/source weight",
            "surface_or_global_status": "no extra exception beyond parent signature",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RC3357_1_hidden_frame",
            "residual": "c_g; b_dis; hidden matter frame",
            "bulk_result_under_packet": "0",
            "reason": "ordinary matter/EM see only e_obs(q(Phi)), g_obs(q(Phi))",
            "surface_or_global_status": "constants/source-normalization rename guard still separate",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RC3357_2_readout_shadow",
            "residual": "epsilon_readout_source_shadow",
            "bulk_result_under_packet": "demoted_to_post_solution_readout",
            "reason": "readout is after parent variation; pre-variation insertion is S_red",
            "surface_or_global_status": "reduced EFT branches must stay labelled",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RC3357_3_decoupled_block",
            "residual": "T_D/P_D/alpha_D P_D",
            "bulk_result_under_packet": "0_if_absent_from_Args(S_parent)",
            "reason": "no un-inventoried decoupled source block or source projector argument",
            "surface_or_global_status": "nonuniversal empirical smoke bound remains nonclaim fallback",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RC3357_4_boundary_contact_pointwise",
            "residual": "epsilon_boundary_contact[p]",
            "bulk_result_under_packet": "0_for_p_notin_supp(T_contact)",
            "reason": "compact collar support exclusion",
            "surface_or_global_status": "surface/contact support remains separate",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RC3357_5_surface_integrated_source",
            "residual": "epsilon_boundary_contact_integrated",
            "bulk_result_under_packet": "not_closed",
            "reason": "whole-source Newton/PPN multipoles can include contact distributions",
            "surface_or_global_status": "OPEN_PRIMARY_SURVIVOR",
            "valid_for_claim": "false",
        },
    ]


def claim_scope_rows() -> list[dict[str, Any]]:
    return [
        {
            "scope_id": "SCOPE3357_0_local_bulk_source",
            "claim_scope": "pointwise local bulk source equation away from contact support",
            "status_after_3357": "CONDITIONAL_THEOREM_PACKET_READY",
            "what_is_proven_conditionally": "source side reduces to Hilbert matter+EM stress with no shadow/readout/decoupled/contact bulk alias",
            "why_not_public_claim": "parent-domain clauses are not signed as final MTS action",
            "valid_for_claim": "false",
        },
        {
            "scope_id": "SCOPE3357_1_Maxwell_EM_stress",
            "claim_scope": "Maxwell/EM stress ownership",
            "status_after_3357": "CONDITIONAL_INCLUDED",
            "what_is_proven_conditionally": "S_EM and action-owned gauge/current contribute through same Hilbert variation",
            "why_not_public_claim": "charge/current owner still needs final parent-domain signature",
            "valid_for_claim": "false",
        },
        {
            "scope_id": "SCOPE3357_2_Newtonian_source",
            "claim_scope": "Newtonian Poisson source / measured GM",
            "status_after_3357": "NOT_CLOSED",
            "what_is_proven_conditionally": "bulk fake-source routes are removed",
            "why_not_public_claim": "surface/contact integrated source and GM calibration remain open",
            "valid_for_claim": "false",
        },
        {
            "scope_id": "SCOPE3357_3_PPN_orbital",
            "claim_scope": "PPN/orbital source multipoles",
            "status_after_3357": "NOT_CLOSED",
            "what_is_proven_conditionally": "pointwise contact and alias fog are reduced",
            "why_not_public_claim": "surface stress, source support, and preferred-frame multipoles remain retained",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3357_0_AX1090_conditional_local_bulk_source_theorem",
            "claim": "under the parent-domain packet, local bulk source side reduces to Hilbert matter+EM stress",
            "passed": "true",
            "reason": "3346 normal form + 3354 alias lemmas + 3356 collar theorem collapse fake-source routes in the pointwise bulk arena",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3357_1_current_parent_signature_promoted",
            "claim": "current MTS corpus parent-signs every domain clause",
            "passed": "false",
            "reason": "3346 closure certificate remains NOT_CLOSED; clauses are a theorem target, not final signed action",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3357_2_EM_stress_included_conditionally",
            "claim": "EM stress is included in the same Hilbert source owner under the packet",
            "passed": "true",
            "reason": "NF3346_0 and NF3346_2 include S_EM/e_obs/A_Q in the active source definition",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3357_3_integrated_Newton_PPN_closed",
            "claim": "integrated Newton/PPN source normalization is closed",
            "passed": "false",
            "reason": "surface/contact stress and multipole calibration remain open",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3357_4_local_GR_claim",
            "claim": "local GR/Newton branch is claim-ready",
            "passed": "false",
            "reason": "left-hand EH/Newton operator, parent-domain signature, and surface/integrated source ownership still need closure",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3357_0",
            "question": "Did 3357 move beyond another missing ledger?",
            "answer": "yes: it collapses multiple blockers into a named conditional local-bulk source theorem packet",
            "reason": "the fake-source routes now share one parent-domain signature contract, with a precise surface/integrated exception",
            "next_action": "attack surface stress ownership/contact multipole bound, while separately preparing the left-hand EH/Newton operator gate",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3357_1",
            "question": "Is the route to GR now just one gap?",
            "answer": "no, but it is cleaner",
            "reason": "source side has a strong conditional local-bulk theorem; full GR also needs left-hand Einstein/Newton operator recovery and integrated source calibration",
            "next_action": "split next work into surface source owner and EH/Newton operator recovery",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3358-Y5-R2FR-surface-stress-owner-or-contact-multipole-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3358_surface_stress_owner_or_contact_multipole_bound.py",
            "objective": "prove surface/contact stress is ordinary Hilbert-owned or universal monopole-only, or build a finite no-cancellation contact multipole bound",
            "why_next": "3357 leaves surface/integrated source calibration as the primary source-side survivor",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3359-Y5-R2FR-left-hand-EH-Newton-operator-recovery-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3359_left_hand_EH_Newton_operator_recovery.py",
            "objective": "attack the left-hand EH/Newton side: derive or bound non-Einstein operator residues so the source-side theorem can actually reduce to GR/Newton rather than only clean the source",
            "why_next": "source-side cleanup alone does not prove GR; the geometric operator must reduce to EH/Newton in the local branch",
            "valid_for_claim": "false",
        },
    ]


def render_doc() -> str:
    return "\n".join(
        [
            "# 3357 — Parent-Domain Signature Collapse Under AX1090",
            "",
            f"Generated: `{RUN_UTC}`",
            "",
            "## Summary",
            "- This checkpoint combines 3346, 3354, 3355, and 3356 into one parent-domain signature attempt.",
            "- Real gain: under the AX1090 parent-domain packet, the **local bulk source side** collapses to ordinary Hilbert matter plus EM stress, with source-shadow/readout/hidden-frame/decoupled/contact-bulk aliases removed.",
            "- Claim ceiling: the current corpus still does not parent-sign every clause, and whole-body Newton/PPN source normalization still has a surface/contact survivor.",
            "- So this is a serious internal theorem target, not a public local-GR claim.",
            "",
            "## Local Source Register",
            table(local_source_rows()),
            "## Parent Domain Signature Clauses",
            table(signature_clause_rows()),
            "## Collapse Theorem Packet",
            table(theorem_packet_rows()),
            "## Residual Collapse Matrix",
            table(residual_collapse_rows()),
            "## Claim Scope Separation",
            table(claim_scope_rows()),
            "## Promotion Gates",
            table(promotion_gate_rows()),
            "## Decision Ledger",
            table(decision_rows()),
            "## Next Target",
            table(next_target_rows()),
        ]
    )


def validate_outputs() -> list[dict[str, Any]]:
    local_sources = local_source_rows()
    signature = signature_clause_rows()
    theorem = theorem_packet_rows()
    residuals = residual_collapse_rows()
    scope = claim_scope_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    write_targets_outside_fw = all(not path.resolve().is_relative_to(FW.resolve()) for path in output_paths + [DOC])
    checks: list[dict[str, Any]] = [
        {
            "check_id": "VAL3357_0_local_sources_exist",
            "check": "all cited local source paths exist",
            "passed": all(row["exists"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3357_1_local_sources_parse",
            "check": "all cited local source paths parse",
            "passed": all(row["parseable"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3357_2_outputs_parse",
            "check": "all 3357 non-validation outputs parse",
            "passed": all(path.exists() and parseable(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3357_3_signature_clauses_complete",
            "check": "signature clauses include q-visible domain, Hilbert source, no hidden frames, no source projector, readout, collar, and surface exception",
            "passed": {row["clause_id"] for row in signature}
            == {
                "SIG3357_0_q_visible_domain",
                "SIG3357_1_single_Hilbert_source_owner",
                "SIG3357_2_no_hidden_coefficients_or_frames",
                "SIG3357_3_no_source_projector_shadow",
                "SIG3357_4_readout_after_variation",
                "SIG3357_5_boundary_local_bulk_collar",
                "SIG3357_6_surface_integrated_exception",
            },
            "detail": "",
        },
        {
            "check_id": "VAL3357_4_conditional_theorem_packet_present",
            "check": "collapse theorem packet includes local bulk residual zero and explicit surface exception",
            "passed": any(row["step_id"] == "THM3357_3_alias_residual_collapse" for row in theorem)
            and any(row["step_id"] == "THM3357_4_surface_exception" for row in theorem),
            "detail": "",
        },
        {
            "check_id": "VAL3357_5_residual_matrix_keeps_surface_open",
            "check": "residual matrix zeroes pointwise routes but keeps integrated surface source open",
            "passed": any(row["residual_id"] == "RC3357_4_boundary_contact_pointwise" and row["bulk_result_under_packet"].startswith("0") for row in residuals)
            and any(row["residual_id"] == "RC3357_5_surface_integrated_source" and row["bulk_result_under_packet"] == "not_closed" for row in residuals),
            "detail": "",
        },
        {
            "check_id": "VAL3357_6_EM_scope_included",
            "check": "claim scope explicitly includes Maxwell/EM stress ownership",
            "passed": any(row["scope_id"] == "SCOPE3357_1_Maxwell_EM_stress" for row in scope)
            and any(row["gate_id"] == "GATE3357_2_EM_stress_included_conditionally" and row["passed"] == "true" for row in gates),
            "detail": "",
        },
        {
            "check_id": "VAL3357_7_no_overclaim",
            "check": "parent signature, integrated Newton/PPN, and local GR claims remain false",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3357_1_current_parent_signature_promoted", "GATE3357_3_integrated_Newton_PPN_closed", "GATE3357_4_local_GR_claim"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3357_8_next_targets_include_source_and_operator",
            "check": "next targets include surface source owner and EH/Newton operator recovery",
            "passed": any("surface/contact stress" in row["objective"] for row in next_target_rows())
            and any("EH/Newton" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3357_9_write_scope_outside_formalization",
            "check": "all 3357 write targets are outside formalization-workbench",
            "passed": write_targets_outside_fw,
            "detail": f"write_targets={len(output_paths) + 1}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3357_10_overall",
            "check": "3357 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["local_sources"], local_source_rows())
    write_csv(OUTPUTS["signature"], signature_clause_rows())
    write_csv(OUTPUTS["theorem"], theorem_packet_rows())
    write_csv(OUTPUTS["residuals"], residual_collapse_rows())
    write_csv(OUTPUTS["scope"], claim_scope_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs())
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
