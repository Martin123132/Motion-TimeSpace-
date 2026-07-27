from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_DIR = POST / "scripts"

CHECKPOINT = "4826"
CLAIM_ID = "L-668"
MARKER = "PPC4161_PIM_COMMUTATOR_ZERO_OR_FIRST_ICOMMUTATOR_BOUND_ROW_4826"
PACKET_MARKER = "PPC4161_PACKET_PIM_COMMUTATOR_ZERO_OR_FIRST_ICOMMUTATOR_BOUND_ROW_4826"
DECISION = "PIM_COMMUTATOR_ZERO_UNSIGNED_FIRST_ICOMMUTATOR_BOUND_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4827-Y5-R2FR-projector-stress-zero-or-first-TPiM-bound-row.md"

DOC_PATH = POST / "4826-Y5-R2FR-PiM-commutator-zero-or-first-Icommutator-bound-row.md"
FORMAL_PATH = FORMAL / "842-PPC4161-PiM-commutator-zero-or-first-Icommutator-bound-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "PiM_commutator_obstruction_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4826_SOURCE_REGISTER.csv"
ZERO_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4826_PIM_COMMUTATOR_ZERO_AUDIT.csv"
BOUND_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4826_ICOMMUTATOR_BOUND_CONTRACT.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4826_PIM_COMMUTATOR_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4826_PIM_COMMUTATOR_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4826_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4826_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4826_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4826_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4826_VALIDATION.csv"

SOURCE_PATHS = {
    "resume": RESUME_PATH,
    "4825_doc": POST / "4825-Y5-R2FR-BY5-source-functor-zero-or-first-source-normalization-row.md",
    "1013_doc": POST / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
    "1014_doc": POST / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
    "obstruction_vector": SOURCE_DIR / "P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv",
    "commutator_gate": SOURCE_DIR / "P8_Y5_PIM_COMMUTATOR_GATE.csv",
    "radial_input": SOURCE_DIR / "P8_Y5_PIM_RADIAL_BOUND_INPUT.csv",
    "fill_template": SOURCE_DIR / "P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv",
    "pim_algebra": SOURCE_DIR / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
    "pim_stress": SOURCE_DIR / "P8_PiM_projector_variation_stress_CONTRACT.csv",
    "parent_identity": SOURCE_DIR / "P8_PARENT_SOURCE_IDENTITY_ATTEMPT.csv",
    "flux_residual": SOURCE_DIR / "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
    "worldtube_runner": SOURCE_DIR / "P8_WORLDTUBE_MEFF_RESIDUAL_RUNNER.csv",
    "runner": RUNNER,
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(dict.fromkeys(field for row in rows for field in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def md_safe(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_safe(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker not in existing:
        write_text(path, existing.rstrip() + "\n\n" + text.strip() + "\n")


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4826_00_resume", SOURCE_PATHS["resume"], "4826-Y5-R2FR-PiM-commutator", "4825 selected the PiM commutator target."),
        ("SRC4826_01_4825_doc", SOURCE_PATHS["4825_doc"], "BY5Z4825_3_flux_closure", "BY5 zero route points at flux closure."),
        ("SRC4826_02_1013_doc", SOURCE_PATHS["1013_doc"], "OBS1013_1_PiM_commutator", "1013 names the exact commutator obstruction."),
        ("SRC4826_03_1014_doc", SOURCE_PATHS["1014_doc"], "PCC1014_1_I_commutator", "1014 splits zero proof from coefficient bound."),
        ("SRC4826_04_obstruction_vector", SOURCE_PATHS["obstruction_vector"], "OBS1013_1_PiM_commutator", "machine obstruction row from 1013."),
        ("SRC4826_05_commutator_gate", SOURCE_PATHS["commutator_gate"], "PC521_0_product_rule", "product-rule and no-closure-from-algebra gate."),
        ("SRC4826_06_radial_input", SOURCE_PATHS["radial_input"], "PI521_1_commutator_profile", "radial source-hair input template."),
        ("SRC4826_07_fill_template", SOURCE_PATHS["fill_template"], "PIF537_1_I_commutator", "explicit I_commutator fill template."),
        ("SRC4826_08_pim_algebra", SOURCE_PATHS["pim_algebra"], "PM5_projector_variation_owned", "projector algebra is conditional, not closure."),
        ("SRC4826_09_pim_stress", SOURCE_PATHS["pim_stress"], "PV2_Hodge_DeWitt_metric_dependence_retained", "projector-stress retention if Hodge route is used."),
        ("SRC4826_10_parent_identity", SOURCE_PATHS["parent_identity"], "I499_3_parent_source_identity", "exact Hilbert mass closure residual identity."),
        ("SRC4826_11_flux_residual", SOURCE_PATHS["flux_residual"], "SMR509_1_Delta_PiM", "source-measure residual map."),
        ("SRC4826_12_worldtube_runner", SOURCE_PATHS["worldtube_runner"], "MR510_3_projector_hair", "worldtube projector-hair blocker."),
        ("SRC4826_13_runner", SOURCE_PATHS["runner"], "def evaluate_row", "4826 executable runner."),
    ]


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def zero_audit(timestamp: str) -> list[dict[str, Any]]:
    clauses = [
        ("PIMZ4826_0_product_rule", "retain full product rule", "d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H", "EXACT_ACTIVE", "do not promote Pi_M algebra into closure"),
        ("PIMZ4826_1_parent_fixed_PiM", "Pi_M fixed before readout", "Pi_M is parent charge data, not a post-fit mask", "NOT_PARENT_DERIVED", "finite I_commutator row"),
        ("PIMZ4826_2_source_current_domain", "J_H in Pi_M domain", "Hilbert mass current lives in the parent source-current space", "CONDITIONAL_UNSIGNED", "source-current descent row"),
        ("PIMZ4826_3_covariant_constancy", "commuting chain map", "D Pi_M=0 on compact local exterior source domain", "NOT_DERIVED", "operator norm dPiM bound"),
        ("PIMZ4826_4_Hilbert_topological_equality", "right closed object", "Pi_M J_H=J_M_top+dB_zero", "KEY_BLOCKER", "R_eq integral row"),
        ("PIMZ4826_5_boundary_zero_flux", "no boundary improvement leak", "int_boundary dB_zero=0", "FAIL_OPEN", "B_zero_flux row"),
        ("PIMZ4826_6_projector_stress_silence", "no Hodge/projector metric stress", "delta_g Pi_M stress is zero or bounded", "RETAINED_IF_USED", "T_PiM bound row"),
        ("PIMZ4826_7_worldtube_glue", "source equals exterior charge", "worldtube M_source equals Pi_M exterior M_eff", "CORE_MISSING", "worldtube glue theorem or residual"),
        ("PIMZ4826_8_no_measured_GM_absorption", "anti-circularity", "measured GM cannot absorb radial/projector hair", "GUARD_WRITTEN_NOT_SATISFIED", "forbidden-source guard"),
    ]
    return [
        {
            "clause_id": clause_id,
            "claim_piece": claim_piece,
            "math_form": math_form,
            "current_result": current_result,
            "finite_fallback": finite_fallback,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for clause_id, claim_piece, math_form, current_result, finite_fallback in clauses
    ]


def bound_contract(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("ICB4826_0_zero", "I_commutator_bound_abs=0", "all zero clauses parent-signed in same branch", "conditional_only"),
        ("ICB4826_1_direct_integral", "I_commutator_abs", "finite-annulus integral of [d,Pi_M]J_H with M_eff normalization", "runner_ready_values_missing"),
        ("ICB4826_2_operator_bound", "annulus_measure*JH_norm*(dPiM_norm+domain_variation)+boundary_transition", "operator/profile bound for unclosed Pi_M chain map", "runner_ready_values_missing"),
        ("ICB4826_3_radial_feed", "epsilon_radial_Meff=c_M*I_commutator/M_eff_ref", "source-normalization radial hair contribution", "feed_ready_values_missing"),
        ("ICB4826_4_BY5_feed", "BY5_commutator_feed=tau_BY5_commutator*epsilon_radial_Meff", "commutator contribution into BY5 finite row", "feed_ready_values_missing"),
    ]
    return [
        {
            "contract_id": contract_id,
            "quantity": quantity,
            "definition": definition,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for contract_id, quantity, definition, status in rows
    ]


def runner_inputs(timestamp: str) -> list[dict[str, Any]]:
    doc_1014 = str(SOURCE_PATHS["1014_doc"])
    vec_1013 = str(SOURCE_PATHS["obstruction_vector"])
    base = {
        "source_signed": "true",
        "units_signed": "true",
        "same_branch_signed": "true",
        "no_cancellation_guard": "true",
        "source_path": doc_1014,
        "timestamp_utc": timestamp,
    }
    zero_flags = {
        "fixed_parent_PiM_signed": "true",
        "source_current_domain_signed": "true",
        "covariant_constancy_signed": "true",
        "Hilbert_topological_equality_signed": "true",
        "boundary_zero_flux_signed": "true",
        "projector_stress_silence_signed": "true",
        "worldtube_glue_signed": "true",
        "no_readout_mask_signed": "true",
        "no_measured_GM_absorption_signed": "true",
    }
    rows: list[dict[str, Any]] = [
        {
            "row_id": "RUN4826_0_live_zero_missing",
            "route_type": "commutator_zero",
            "route": "live zero audit",
            "source_path": doc_1014,
            "equation_ref": "PCT1014_2_commutator_zero",
            "notes": "physical branch remains unsigned",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4826_1_conditional_zero_pass",
            "route_type": "commutator_zero",
            "route": "conditional parent-signed zero",
            "equation_ref": "PCT1014 zero route",
            "notes": "nonclaim theorem-shape smoke row",
            **base,
            **zero_flags,
        },
        {
            "row_id": "RUN4826_2_forbidden_post_readout_mask",
            "route_type": "commutator_zero",
            "route": "forbidden closure",
            "equation_ref": "PRS1014_4_post_readout_mask",
            "notes": "POST_READOUT_MASK cannot derive Pi_M commutator zero",
            **base,
            **zero_flags,
        },
        {
            "row_id": "RUN4826_3_live_bound_missing",
            "route_type": "direct_bound",
            "route": "live I_commutator row missing",
            "source_path": str(SOURCE_PATHS["radial_input"]),
            "equation_ref": "PI521_1_commutator_profile",
            "I_commutator_abs": "MISSING_I_COMMUTATOR",
            "c_M_abs": "MISSING_c_M",
            "M_eff_ref_abs": "MISSING_MEFF",
            "notes": "no physical source-backed I_commutator value yet",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4826_4_direct_Icommutator_smoke_pass",
            "route_type": "direct_bound",
            "route": "direct finite I_commutator smoke",
            "source_path": vec_1013,
            "equation_ref": "OBS1013_1_PiM_commutator",
            "I_commutator_abs": "0.04",
            "c_M_abs": "1.0",
            "M_eff_ref_abs": "2.0",
            "notes": "nonclaim direct integral smoke row",
            **{k: base[k] for k in ("source_signed", "units_signed", "same_branch_signed", "no_cancellation_guard")},
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4826_5_operator_Icommutator_smoke_pass",
            "route_type": "operator_bound",
            "route": "operator bound smoke",
            "source_path": doc_1014,
            "equation_ref": "PCC1014_1_I_commutator",
            "dPiM_operator_norm_abs": "0.10",
            "JH_annulus_norm_abs": "0.40",
            "annulus_measure_abs": "2.0",
            "domain_selector_variation_abs": "0.05",
            "boundary_transition_abs": "0.01",
            "c_M_abs": "1.0",
            "M_eff_ref_abs": "2.0",
            "notes": "nonclaim operator/profile smoke row",
            **{k: base[k] for k in ("source_signed", "units_signed", "same_branch_signed", "no_cancellation_guard")},
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4826_6_BY5_commutator_feed_smoke_pass",
            "route_type": "BY5_feed",
            "route": "commutator feeds BY5",
            "source_path": doc_1014,
            "equation_ref": "epsilon_radial_Meff=c_M I_commutator/M_eff_ref",
            "I_commutator_abs": "0.05",
            "c_M_abs": "1.2",
            "M_eff_ref_abs": "3.0",
            "tau_BY5_commutator_abs": "2.0",
            "notes": "nonclaim BY5 feed smoke row",
            **{k: base[k] for k in ("source_signed", "units_signed", "same_branch_signed", "no_cancellation_guard")},
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4826_7_forbidden_cancellation_bound",
            "route_type": "direct_bound",
            "route": "forbidden cancellation",
            "source_path": doc_1014,
            "equation_ref": "PCC1014_1_I_commutator",
            "I_commutator_abs": "0.0",
            "c_M_abs": "1.0",
            "M_eff_ref_abs": "1.0",
            "notes": "CANCEL_UNKNOWN_COMPONENTS is not a derivation",
            **{k: base[k] for k in ("source_signed", "units_signed", "same_branch_signed", "no_cancellation_guard")},
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4826_8_forbidden_measured_GM_source",
            "route_type": "BY5_feed",
            "route": "forbidden measured GM absorption",
            "source_path": doc_1014,
            "equation_ref": "measured GM readout",
            "I_commutator_abs": "0.01",
            "c_M_abs": "1.0",
            "M_eff_ref_abs": "1.0",
            "tau_BY5_commutator_abs": "1.0",
            "notes": "MEASURED_GM_AS_SOURCE cannot source the commutator",
            **{k: base[k] for k in ("source_signed", "units_signed", "same_branch_signed", "no_cancellation_guard")},
            "timestamp_utc": timestamp,
        },
    ]
    return rows


def run_runner() -> None:
    subprocess.run([sys.executable, str(RUNNER), str(RUNNER_INPUT), str(RUNNER_OUTPUT)], check=True)


def build_decision(timestamp: str, outputs: list[dict[str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4826_0",
            "decision": DECISION,
            "basis": "live zero clauses and live I_commutator values are missing; conditional zero and finite smoke routes execute; forbidden routes fail closed",
            "zero_claim": False,
            "finite_bound_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def build_claim_gates(timestamp: str, outputs: list[dict[str, str]]) -> list[dict[str, Any]]:
    by_id = {row["row_id"]: row for row in outputs}
    return [
        {
            "gate_id": "CG4826_0_zero",
            "claim": "[d,Pi_M]J_H=0 is parent-signed",
            "passed": by_id["RUN4826_0_live_zero_missing"]["runner_status"] == "PIM_COMMUTATOR_ZERO_PASS_NONCLAIM",
            "claim_allowed": False,
            "reason": "live parent zero clauses remain unsigned",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CG4826_1_Icommutator",
            "claim": "source-backed I_commutator row exists",
            "passed": by_id["RUN4826_3_live_bound_missing"]["runner_status"] == "PIM_COMMUTATOR_DIRECT_BOUND_PASS_NONCLAIM",
            "claim_allowed": False,
            "reason": "live row remains missing; smoke rows only check arithmetic and failure modes",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CG4826_2_anti_circularity",
            "claim": "no measured GM or readout mask is used as source",
            "passed": by_id["RUN4826_2_forbidden_post_readout_mask"]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE"
            and by_id["RUN4826_8_forbidden_measured_GM_source"]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
            "claim_allowed": False,
            "reason": "forbidden paths fail closed",
            "timestamp_utc": timestamp,
        },
    ]


def build_status(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "decision": DECISION,
            "claim_allowed": False,
            "physics_status": "PiM commutator zero remains unsigned; first I_commutator and BY5-feed bound contracts are executable but nonclaim",
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def build_next_target(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "reason": "if Pi_M commutator is not zero, the next retained obstruction is projector variation stress T_PiM; it must be zeroed or bounded before local-GR/Newton promotion",
            "success_condition": "derive projector-stress silence or produce first T_PiM weak-field/PPN/source-normalization bound row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def build_docs(timestamp: str, sources: list[dict[str, Any]], audit: list[dict[str, Any]], contract: list[dict[str, Any]], outputs: list[dict[str, str]], validations: list[dict[str, Any]]) -> None:
    doc = f"""# 4826 - PiM Commutator Zero Or First Icommutator Bound Row

Marker: `{MARKER}`

## Summary

4826 attacks the `Pi_M` source-coupling tooth directly:

```text
d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H
I_commutator = int_A_ext [d,Pi_M]J_H
epsilon_radial_Meff = c_M I_commutator / M_eff_ref
BY5_commutator_feed = tau_BY5_commutator epsilon_radial_Meff
```

The exact-zero path remains unsigned because parent-fixed `Pi_M`, topological/Hilbert equality, boundary-zero flux, projector-stress silence, worldtube glue and anti-circular measured-GM rules are not all signed in the same branch. The useful advance is that the finite route is now executable: a direct `I_commutator` row or an operator/profile bound can feed the source-normalization `BY5` ledger without using measured `GM` as a broom.

## Source register

{md_table(sources, ['source_id', 'exists', 'needle_found', 'role'])}

## Zero audit

{md_table(audit, ['clause_id', 'claim_piece', 'current_result', 'finite_fallback'])}

## Bound contract

{md_table(contract, ['contract_id', 'quantity', 'definition', 'status'])}

## Runner output

{md_table(outputs, ['row_id', 'runner_status', 'I_commutator_bound_abs', 'epsilon_radial_Meff_from_Icomm_abs', 'BY5_commutator_feed_abs', 'missing_for_claim'])}

## Decision

`{DECISION}`

Next target: `{NEXT_TARGET}`

## Validation

{md_table(validations, ['validation_id', 'result', 'details'])}
"""
    formal = f"""# 842 - PPC4161 PiM commutator zero or first Icommutator bound row

Marker: `{MARKER}`

4826 makes the `Pi_M` commutator obstruction executable rather than rhetorical. The live branch does **not** prove `[d,Pi_M]J_H=0`, because topological/Hilbert equality, boundary silence, projector-stress silence and worldtube glue are still unsigned. The finite branch now has a direct integral route and an operator/profile route:

```text
I_commutator_bound = |int_A [d,Pi_M]J_H|
epsilon_radial_Meff = c_M I_commutator_bound / M_eff_ref
BY5_commutator_feed = tau_BY5_commutator epsilon_radial_Meff
```

Smoke rows verify the arithmetic and the anti-circularity guards. Measured `GM`, post-readout masks, and cancellation-only arguments fail closed. No local-GR/Newton/source-normalization claim is allowed from this checkpoint.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)
    write_text(FORMAL_PATH, formal)


def update_claims(timestamp: str) -> None:
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "PiM_commutator_zero_or_first_Icommutator_bound_row",
        "current_evidence": "4826 converts the PiM commutator obstruction into an executable zero-or-finite I_commutator/BY5-feed runner; live zero and live source-backed values remain missing.",
        "status": "PiM_commutator_runner_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "topological-Hilbert equality, projector-stress silence, worldtube glue, and source-backed I_commutator values remain missing",
        "sector": "local_gr_Newton_source_coupling",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "smoke rows pass but live PiM commutator rows are not source-backed",
        "title": "PiM commutator zero or first Icommutator bound row",
        "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    if CLAIMS_PATH.exists():
        rows = read_csv(CLAIMS_PATH)
        if any(existing.get("claim_id") == CLAIM_ID for existing in rows):
            return
        fields = list(rows[0].keys()) if rows else list(row.keys())
        for key in row:
            if key not in fields:
                fields.append(key)
        rows.append(row)
        with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
    else:
        write_csv(CLAIMS_PATH, [row])


def update_spine_and_packet(timestamp: str) -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""## PPC4161 4826 PiM commutator runner

`{MARKER}`. The `Pi_M` commutator is now a direct local source-coupling gate: either `[d,Pi_M]J_H=0` is parent-signed, or `I_commutator` is bounded and fed into `epsilon_radial_Meff`/`BY5`. The live branch remains nonclaim because topological-Hilbert equality, projector-stress silence and worldtube glue remain unsigned. Decision: `{DECISION}`.""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## 4826 PiM commutator zero-or-bound runner

`{MARKER}` turns the `Pi_M` commutator from a named blocker into an executable local-GR/Newton source-coupling obstruction. Conditional zero passes only if all parent clauses are signed; direct/operator smoke rows compute finite `I_commutator` and `BY5` feeds; measured-GM and readout-mask shortcuts fail closed. Next: `{NEXT_TARGET}`.""",
    )


def update_resume(timestamp: str) -> None:
    text = f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4826-Y5-R2FR-PiM-commutator-zero-or-first-Icommutator-bound-row.md`
Marker: `{MARKER}`

## Where we are

4826 made the `Pi_M` commutator obstruction executable:

```text
d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H
I_commutator = int_A_ext [d,Pi_M]J_H
epsilon_radial_Meff = c_M I_commutator / M_eff_ref
BY5_commutator_feed = tau_BY5_commutator epsilon_radial_Meff
```

## Live blockers

- `[d,Pi_M]J_H=0` is not parent-signed.
- Parent-fixed `Pi_M`, topological/Hilbert equality, boundary-zero flux, projector-stress silence, and worldtube glue remain open.
- No source-backed physical `I_commutator` row exists yet.
- Measured `G`/`GM`, post-readout masks, and cancellation-only routes are explicitly forbidden.

## Next target

`{NEXT_TARGET}`
"""
    write_text(RESUME_PATH, text)


def validate(timestamp: str, outputs: list[dict[str, str]], sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {row["row_id"]: row for row in outputs}
    checks = [
        ("VAL4826_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        ("VAL4826_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found"),
        ("VAL4826_02_live_zero_blocked", by_id["RUN4826_0_live_zero_missing"]["runner_status"] == "BLOCKED_PIM_COMMUTATOR_ZERO_CLAUSES", "live zero remains blocked"),
        ("VAL4826_03_conditional_zero_pass", by_id["RUN4826_1_conditional_zero_pass"]["runner_status"] == "PIM_COMMUTATOR_ZERO_PASS_NONCLAIM", "conditional parent-signed zero computes"),
        ("VAL4826_04_forbidden_mask_fails", by_id["RUN4826_2_forbidden_post_readout_mask"]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", "post-readout mask fails closed"),
        ("VAL4826_05_live_bound_blocked", by_id["RUN4826_3_live_bound_missing"]["runner_status"] == "BLOCKED_PIM_COMMUTATOR_DIRECT_BOUND_INPUTS", "live I_commutator row missing"),
        ("VAL4826_06_direct_smoke_pass", by_id["RUN4826_4_direct_Icommutator_smoke_pass"]["runner_status"] == "PIM_COMMUTATOR_DIRECT_BOUND_PASS_NONCLAIM", "direct I_commutator smoke passes"),
        ("VAL4826_07_operator_smoke_pass", by_id["RUN4826_5_operator_Icommutator_smoke_pass"]["runner_status"] == "PIM_COMMUTATOR_OPERATOR_BOUND_PASS_NONCLAIM", "operator I_commutator smoke passes"),
        ("VAL4826_08_BY5_feed_smoke_pass", by_id["RUN4826_6_BY5_commutator_feed_smoke_pass"]["runner_status"] == "PIM_COMMUTATOR_BY5_FEED_PASS_NONCLAIM", "BY5 feed smoke passes"),
        ("VAL4826_09_forbidden_cancellation_fails", by_id["RUN4826_7_forbidden_cancellation_bound"]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", "cancellation shortcut fails closed"),
        ("VAL4826_10_forbidden_GM_fails", by_id["RUN4826_8_forbidden_measured_GM_source"]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", "measured GM source shortcut fails closed"),
        ("VAL4826_11_no_claim_allowed", all(str(row.get("claim_allowed", "")).lower() == "false" for row in outputs), "no runner row allows a claim"),
    ]
    return [
        {
            "validation_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "details": details,
            "timestamp_utc": timestamp,
        }
        for check_id, passed, details in checks
    ]


def main() -> int:
    timestamp = now()
    py_compile.compile(str(RUNNER), doraise=True)
    py_compile.compile(__file__, doraise=True)

    sources = source_register(timestamp)
    audit = zero_audit(timestamp)
    contract = bound_contract(timestamp)
    inputs = runner_inputs(timestamp)
    write_csv(SOURCE_REGISTER, sources)
    write_csv(ZERO_AUDIT, audit)
    write_csv(BOUND_CONTRACT, contract)
    write_csv(RUNNER_INPUT, inputs)

    run_runner()
    outputs = read_csv(RUNNER_OUTPUT)
    decisions = build_decision(timestamp, outputs)
    gates = build_claim_gates(timestamp, outputs)
    status = build_status(timestamp)
    next_rows = build_next_target(timestamp)
    validations = validate(timestamp, outputs, sources)

    write_csv(DECISION_CSV, decisions)
    write_csv(CLAIM_GATES, gates)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_TARGET_CSV, next_rows)
    write_csv(VALIDATION_CSV, validations)

    build_docs(timestamp, sources, audit, contract, outputs, validations)
    update_claims(timestamp)
    update_spine_and_packet(timestamp)
    update_resume(timestamp)

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validations if row["result"] != "PASS"]
    if failed:
        raise RuntimeError(f"4826 validation failed: {failed}")
    print(f"{MARKER} complete")
    print(f"doc={DOC_PATH}")
    print(f"validation={VALIDATION_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
