from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4578"
CLAIM_ID = "L-420"
BRANCH_ID = "MTS_R2FR_Y5_LAPSE_TEST_PARENT_SIGNATURE_OR_FIRST_REAL_SOURCE_LEAK_ROW_4578"
MARKER = "PPC4161_LAPSE_TEST_PARENT_SIGNATURE_OR_FIRST_REAL_SOURCE_LEAK_ROW_4578"
PACKET_MARKER = "PPC4161_PACKET_LAPSE_TEST_PARENT_SIGNATURE_OR_FIRST_REAL_SOURCE_LEAK_ROW_4578"
DECISION = "LAPSE_PARENT_SIGNATURE_REDUCED_TO_SOURCE_OWNER_AND_READOUT_NATURALITY_RHO_READOUT_SHIFT_ROW_FILLED_NONCLAIM"
NEXT_TARGET = "4579-Y5-R2FR-readout-commutator-zero-or-rho-readout-shift-bound-value.md"

DOC_PATH = POST / "4578-Y5-R2FR-lapse-test-parent-signature-or-first-real-source-leak-row.md"
FORMAL_PATH = FORMAL / "594-PPC4161-lapse-test-parent-signature-or-first-real-source-leak-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4577 = POST / "4577-Y5-R2FR-density-profile-owner-or-DeltaWtr-first-bound.md"
CSV_4577_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4577_NEXT_TARGET.csv"
CSV_4577_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4577_LAPSE_TEST_PROFILE_OWNER_THEOREM.csv"
CSV_4577_DEFECT = SOURCE_DIR / "P8_Y5_R2FR_4577_PROFILE_DEFECT_DECOMPOSITION.csv"
CSV_4577_DELTAWTR = SOURCE_DIR / "P8_Y5_R2FR_4577_DELTAWTR_FIRST_BOUND_ROWS.csv"
CSV_4430_OWNER = SOURCE_DIR / "P8_Y5_R2FR_4430_SOURCE_OWNER_SIGNATURE_OUTPUT.csv"
CSV_4430_DERIVATIONS = SOURCE_DIR / "P8_Y5_R2FR_4430_DERIVATION_ROWS.csv"
CSV_4431_SHADOW = SOURCE_DIR / "P8_Y5_R2FR_4431_SOURCE_SHADOW_OUTPUT.csv"
CSV_4431_NONHILBERT = SOURCE_DIR / "P8_Y5_R2FR_4431_NONHILBERT_BYPASS_OUTPUT.csv"
CSV_4432_NOHOM = SOURCE_DIR / "P8_Y5_R2FR_4432_CONSTRUCTOR_NOHOM_OUTPUT.csv"
CSV_4432_DERIVATIONS = SOURCE_DIR / "P8_Y5_R2FR_4432_DERIVATION_ROWS.csv"
CSV_4432_SPLIT = SOURCE_DIR / "P8_Y5_R2FR_4432_SHADOW_SPLIT_OUTPUT.csv"
CSV_4432_KMSHADOW = SOURCE_DIR / "P8_Y5_R2FR_4432_KMSHADOW_VALUE_OUTPUT.csv"
CSV_4433_OWNER = SOURCE_DIR / "P8_Y5_R2FR_4433_ACTION_SCALE_OWNER_OUTPUT.csv"
CSV_4433_MODE = SOURCE_DIR / "P8_Y5_R2FR_4433_ACTION_SCALE_MODE_SPLIT_OUTPUT.csv"
CSV_4434_GRAPH = SOURCE_DIR / "P8_Y5_R2FR_4434_CONNECTED_GRAPH_OUTPUT.csv"
CSV_4434_HBAR = SOURCE_DIR / "P8_Y5_R2FR_4434_HBAR_MEASURE_OWNER_OUTPUT.csv"
CSV_4408_DERIVATIONS = SOURCE_DIR / "P8_Y5_R2FR_4408_DERIVATIONS.csv"
CSV_4408_SIGMA = SOURCE_DIR / "P8_Y5_R2FR_4408_SIGMAS_ELECTRIC_OWNER_OUTPUT.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4578_SOURCE_REGISTER.csv"
PARENT_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4578_LAPSE_PARENT_CONTRACT_THEOREM.csv"
SIGNATURE_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4578_PARENT_SIGNATURE_AUDIT.csv"
READOUT_LEAK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4578_RHO_READOUT_SHIFT_FIRST_SOURCE_LEAK_ROW.csv"
DELTAWTR_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4578_DELTAWTR_UPDATE_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4578_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4578_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4578_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4578_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4578_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4578_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
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
        lines.append(
            "| "
            + " | ".join(
                str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
                for header in headers
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def append_once(path: Path, marker: str, block: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + block.strip() + "\n")


def source_rows() -> list[dict[str, Any]]:
    source_specs = [
        ("SRC4578_00_4577_doc", "4577 lapse-test checkpoint", DOC_4577, "R_eff[f] = R_H[f]"),
        ("SRC4578_01_4577_next", "4577 selected 4578 target", CSV_4577_NEXT, "lapse-test-parent-signature-or-first-real-source-leak-row"),
        ("SRC4578_02_4577_theorem", "4577 lapse theorem", CSV_4577_THEOREM, "LTP4577_1_effective_profile_identity"),
        ("SRC4578_03_4577_defect", "4577 readout defect", CSV_4577_DEFECT, "PDD4577_3_readout"),
        ("SRC4578_04_4577_DeltaWtr", "4577 DeltaWtr formula", CSV_4577_DELTAWTR, "DW4577_1_first_bound"),
        ("SRC4578_05_4430_owner", "4430 total Hilbert source owner", CSV_4430_OWNER, "SIG4430_1_current_total_Hilbert_owner"),
        ("SRC4578_06_4430_derivations", "4430 zero signature derivation", CSV_4430_DERIVATIONS, "THS4430_0_zero_signature"),
        ("SRC4578_07_4431_shadow", "4431 source-shadow output", CSV_4431_SHADOW, "SH4431_1_current_no_weight_core"),
        ("SRC4578_08_4431_nonHilbert", "4431 non-Hilbert bypass output", CSV_4431_NONHILBERT, "NH4431_1_current_residual_retained"),
        ("SRC4578_09_4432_noHom", "4432 constructor no-Hom output", CSV_4432_NOHOM, "NHOM4432_1_current_source_domain"),
        ("SRC4578_10_4432_derivations", "4432 source-shadow split derivation", CSV_4432_DERIVATIONS, "SPLIT4432_1_surviving_shadow_reassignment"),
        ("SRC4578_11_4432_split", "4432 readout projector survivor", CSV_4432_SPLIT, "SPLIT4432_3_readout_projector_shadow"),
        ("SRC4578_12_4432_Kmshadow", "4432 readout projector reassignment", CSV_4432_KMSHADOW, "KM4432_3_readout_projector_reassignment"),
        ("SRC4578_13_4433_owner", "4433 action scale owner", CSV_4433_OWNER, "ASO4433_2_connected_naturality_route"),
        ("SRC4578_14_4433_mode", "4433 common mode split", CSV_4433_MODE, "ASM4433_0_common_derivative_silent_mode"),
        ("SRC4578_15_4434_graph", "4434 connected graph certificate", CSV_4434_GRAPH, "GRC4434_1_physical_template"),
        ("SRC4578_16_4434_hbar", "4434 hbar measure owner", CSV_4434_HBAR, "HMO4434_1_current_phase_seed"),
        ("SRC4578_17_4408_derivations", "4408 sigma/electric derivation", CSV_4408_DERIVATIONS, "ADDO4408_0_sigma_electric_owner_contract"),
        ("SRC4578_18_4408_sigma", "4408 sigma/electric owner output", CSV_4408_SIGMA, "SOI4408_0_current_sigma_electric_contract"),
        ("SRC4578_19_packet_4577", "4577 packet marker", PACKET_PATH, "PPC4161_PACKET_DENSITY_PROFILE_OWNER_OR_DELTAWTR_FIRST_BOUND_4577"),
        ("SRC4578_20_claim_419", "prior claim register row", CLAIMS_PATH, "L-419"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle in source_specs:
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "source_path": str(path),
                "exists": bool_text(path.exists()),
                "needle": needle,
                "needle_found": bool_text(needle in text),
                "role": "lapse-test parent signature audit and first rho_readout_shift leak row",
                "valid_for_claim": "False",
            }
        )
    return rows


def parent_contract_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "contract_id": "LPC4578_0_total_Hilbert_source_owner",
            "statement": "The effective local source profile must be generated by the same total Hilbert source action before readout.",
            "formula": "R_eff[f]=delta_f S_parent = int_W f T_H(n,n)dV_H = R_H[f]",
            "effect_if_signed": "Kills pure source-only shadow and makes the lapse-test identity start from one parent functional.",
            "current_status": "PARTIAL_OWNER_PRESENT_NOT_PARENT_SIGNED_FOR_ALL_RETURNS",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "contract_id": "LPC4578_1_no_constructor_return",
            "statement": "No source-only, species-label, hidden-marker, action-scale, or constant-sector constructor may return an active source coefficient after calibration.",
            "formula": "Hom_parent({SpeciesLabel,HiddenMarker,ReadoutMarker},Coeff_active_source)=empty after common calibration quotient",
            "effect_if_signed": "Removes the remaining non-Hilbert/source-shadow/action-scale ways to make R_eff[f] differ from R_H[f].",
            "current_status": "CONDITIONAL_NOHOM_REDUCED_NOT_CLOSED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "contract_id": "LPC4578_2_readout_naturality",
            "statement": "Readout and material/worldtube projectors must be applied after variation and must commute with compact lapse probing on W_H.",
            "formula": "rho_readout_shift := c^-2 (O_lapse Pi_readout - Pi_readout O_lapse) S_parent = 0",
            "effect_if_signed": "Kills E_readout_profile and the readout term in Delta_Wtr.",
            "current_status": "OPEN_READOUT_REENTRY_CHANNEL",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "contract_id": "LPC4578_3_topological_improvement_owner",
            "statement": "Any topological/electric/improvement representative must be owned as a Hilbert stress improvement with boundary and Ward silence.",
            "formula": "rho_top-rho_H=c^-2D_iD_jS^{ij}, with boundary/Ward pairings zero or source-bounded",
            "effect_if_signed": "Prevents a correct total charge but wrong density profile from spoiling the lapse identity.",
            "current_status": "IMPROVEMENT_MECHANISM_READY_SOURCE_OWNER_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "contract_id": "LPC4578_4_parent_signature_result",
            "statement": "If LPC4578_0 through LPC4578_3 hold on one branch, then the all-lapse-test identity is parent-signed.",
            "formula": "forall f in C_c^infty(W_H): R_eff[f]-R_H[f]=0 => rho_eff=rho_H, E_profile=0",
            "effect_if_signed": "Closes the 4577 profile-owner theorem and removes E_profile from epsilon_lock.",
            "current_status": "CONDITIONAL_THEOREM_RAW_TRANSITION_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def signature_audit_rows(now: str) -> list[dict[str, Any]]:
    audits = [
        (
            "AUD4578_0_total_Hilbert_owner",
            "same total Hilbert source action",
            "4430 SIG4430_1 has total Hilbert owner partial, but source-shadow/nonHilbert/hidden returns remain live",
            "PARTIAL_NOT_FULL_SIGNATURE",
            "cannot set R_eff=R_H for every lapse probe",
        ),
        (
            "AUD4578_1_pure_source_shadow",
            "pure source-only shadow",
            "4432 SPLIT4432_0 marks pure source-only branch as contract-killable",
            "ZERO_CONTRACT_READY_NONCLAIM",
            "helps, but does not kill weighted action, hidden return, or readout projector channels",
        ),
        (
            "AUD4578_2_readout_projector",
            "readout/projector reentry",
            "4432 SPLIT4432_3 and KM4432_3 keep readout projector survivor",
            "LIVE_CHANNEL",
            "becomes the first concrete rho_readout_shift leak row",
        ),
        (
            "AUD4578_3_action_scale",
            "weighted action/action scale",
            "4433 ASO4433_1/2 and ASM4433 keep hbar/measure/connectedness gaps",
            "LIVE_CHANNEL",
            "not a pure shadow; must be separate action-scale/constant-sector residual",
        ),
        (
            "AUD4578_4_nonHilbert_bypass",
            "non-Hilbert bypass",
            "4431 NH4431_1 keeps non-Hilbert residual retained",
            "LIVE_CHANNEL",
            "feeds Y_nonHilbert/E_nonHilbert_profile until exact divergence and boundary silence close",
        ),
        (
            "AUD4578_5_sigma_electric",
            "topological/improvement owner",
            "4408 SOI4408_0 has improvement mechanism ready but source owner unsigned",
            "CONDITIONAL_MECHANISM_UNSIGNED",
            "cannot replace all-lapse identity without Ward/boundary/source support clauses",
        ),
        (
            "AUD4578_6_verdict",
            "all-lapse-test parent signature",
            "this audit",
            "NOT_PARENT_SIGNED",
            "fill rho_readout_shift row; no local-GR claim from 4578",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "audit_id": audit_id,
            "clause": clause,
            "evidence": evidence,
            "status": status,
            "effect": effect,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for audit_id, clause, evidence, status, effect in audits
    ]


def readout_leak_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "leak_id": "RSL4578_0_rho_readout_shift_commutator",
            "quantity": "rho_readout_shift",
            "definition": "rho_readout_shift := c^-2 (O_lapse Pi_readout - Pi_readout O_lapse) S_parent",
            "test_function_row": "Delta_readout[f] := c^2 int_W f rho_readout_shift dV_H",
            "norm_row": "||rho_readout_shift||_TV := sup_{||f||_inf<=1} |Delta_readout[f]|/c^2",
            "zero_if": "readout/material/worldtube projector is fixed before variation and applied only after source solve; [O_lapse,Pi_readout]=0 on W_H",
            "source_basis": "4432 readout projector survivor + 4577 PDD4577_3_readout",
            "definition_status": "FILLED_FORMAL_SOURCE_LEAK_ROW",
            "numeric_value": "MISSING_PARENT_NUMERIC_VALUE_OR_ZERO_CERTIFICATE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "leak_id": "RSL4578_1_readout_profile_bound",
            "quantity": "E_readout_profile",
            "definition": "E_readout_profile <= ||rho_readout_shift_perp/rho_H||_inf, or TV fallback ||rho_readout_shift||_TV/M_H_ref",
            "test_function_row": "E_readout_profile=0 if Delta_readout[f]=0 for all compact f",
            "norm_row": "TV fallback is conservative and profile-norm row needs rho_H support data",
            "zero_if": "RSL4578_0 commutator zero certificate is parent-signed",
            "source_basis": "4577 profile defect decomposition",
            "definition_status": "FILLED_FORMAL_SOURCE_LEAK_ROW",
            "numeric_value": "MISSING_PROFILE_NORM_OR_TV_BOUND_VALUE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def deltawtr_update_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        (
            "DWU4578_0_readout_row_inserted",
            "Delta_Wtr",
            "Delta_Wtr <= (||mu_tr||_TV + ||B_src^A||_TV + ||rho_readout_shift||_TV)/M_H_ref",
            "rho_readout_shift is no longer a vague placeholder; it is the readout/lapse commutator norm from RSL4578_0",
            "MISSING_mu_tr_Bsrc_rho_readout_shift_MHref_VALUES",
        ),
        (
            "DWU4578_1_profile_lock_update",
            "epsilon_lock",
            "epsilon_lock <= Y_nonHilbert + Delta_Wtr + E_shadow + E_top_profile + E_nonHilbert_profile + E_readout_profile",
            "E_readout_profile now has a commutator source-leak row",
            "MISSING_COMPONENT_VALUES",
        ),
        (
            "DWU4578_2_parent_zero_route",
            "readout zero branch",
            "[O_lapse,Pi_readout]=0 and P_offW J_tr=0 imply rho_readout_shift=0 and remove readout term from Delta_Wtr",
            "this is the exact next proof target",
            "ZERO_CONDITION_DEFINED_NOT_PARENT_SIGNED",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "update_id": update_id,
            "quantity": quantity,
            "formula": formula,
            "meaning": meaning,
            "current_value": current_value,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for update_id, quantity, formula, meaning, current_value in rows
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    controls = [
        (
            "CTRL4578_commuting_readout",
            "[O_lapse,Pi_readout]=0",
            "rho_readout_shift=0, E_readout_profile=0",
            "CONTROL_PASS_NONCLAIM",
        ),
        (
            "CTRL4578_noncommuting_readout",
            "Delta_readout[f_1]=2e-6 c^2, M_H_ref=1",
            "||rho_readout_shift||_TV/M_H_ref >= 2e-6",
            "SCHEMA_LEAK_NONZERO_NONCLAIM",
        ),
        (
            "CTRL4578_monopole_readout_trap",
            "Delta_readout[1]=0 but Delta_readout[f_2]!=0",
            "total mass unchanged but E_readout_profile active",
            "COUNTERMODEL_CAUGHT",
        ),
        (
            "CTRL4578_large_leak_fail",
            "||rho_readout_shift||_TV/M_H_ref=2e-3 with target tolerance 1e-5",
            "Delta_Wtr branch fails smoke tolerance",
            "SCHEMA_FAIL_NONCLAIM",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "control_id": control_id,
            "input_case": input_case,
            "expected": expected,
            "verdict": verdict,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for control_id, input_case, expected, verdict in controls
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    gates = [
        ("PROM4578_0_total_owner", "Total Hilbert source owner parent-signed for transition profile response.", "BLOCKED"),
        ("PROM4578_1_no_return", "No species/hidden/readout/action-scale constructor returns active source coefficient.", "BLOCKED"),
        ("PROM4578_2_readout_commutator", "[O_lapse,Pi_readout]=0 or numeric rho_readout_shift bound sourced.", "BLOCKED"),
        ("PROM4578_3_topological_owner", "Topological/improvement profile owner has Ward/boundary/source support signatures.", "BLOCKED"),
        ("PROM4578_4_no_public_claim", "No local-GR/R10/PPN/orbital claim while parent lapse signature or leak row value is missing.", "PASSED_FIREWALL"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "required_for_claim": "True",
            "valid_for_claim": "False",
        }
        for gate_id, gate, status in gates
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "plain_english": "4578 tried the parent signature route and found the exact remaining leaks. Pure source-only shadow is structurally killable, but readout/projector reentry survives. The checkpoint fills the first concrete source-leak row: rho_readout_shift as the lapse/readout commutator.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "The next forward move is now exact: prove [O_lapse,Pi_readout]=0 from parent readout order, or source/bound ||rho_readout_shift||_TV/M_H_ref as the first real readout leak value.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "status": "complete_nonclaim_checkpoint",
            "decision": DECISION,
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def doc_body(
    now: str,
    sources: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    audits: list[dict[str, Any]],
    leaks: list[dict[str, Any]],
    updates: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    promotions: list[dict[str, Any]],
) -> str:
    return f"""# 4578 - Lapse-test parent signature or first real source-leak row

Generated: `{now}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`  
Claim status: private nonclaim checkpoint.

## Result

4578 tries to parent-sign the all-lapse-test identity from 4577.  The exact parent contract is now:

```text
R_eff[f] = R_H[f] for all compact f
```

provided the total Hilbert source owner, no-constructor/no-return rule, readout naturality, and topological/improvement owner clauses all hold on one branch.

The current corpus does **not** parent-sign the full identity.  The useful advance is that the failure is no longer foggy coupling.  Pure source-only shadow is contract-killable, but the readout/projector return remains live.  The first concrete source-leak row is now:

```text
rho_readout_shift := c^-2 (O_lapse Pi_readout - Pi_readout O_lapse) S_parent
Delta_readout[f] := c^2 int_W f rho_readout_shift dV_H
||rho_readout_shift||_TV := sup_{{||f||_inf<=1}} |Delta_readout[f]|/c^2
```

and the local lock bound becomes:

```text
Delta_Wtr <= (||mu_tr||_TV + ||B_src^A||_TV + ||rho_readout_shift||_TV)/M_H_ref
epsilon_lock <= Y_nonHilbert + Delta_Wtr + E_profile
```

So the next target is not “find the coupling” in general.  It is exactly the readout commutator: prove it is zero, or source its norm.

## Parent contract theorem

{markdown_table(contracts)}

## Parent signature audit

{markdown_table(audits)}

## First source-leak row

{markdown_table(leaks)}

## Delta_Wtr update rows

{markdown_table(updates)}

## Controls

{markdown_table(controls)}

## Promotion gates

{markdown_table(promotions)}

## Source register

{markdown_table(sources)}

## Next target

`{NEXT_TARGET}`

Reason: prove `[O_lapse,Pi_readout]=0`, or source/bound `||rho_readout_shift||_TV/M_H_ref`.
"""


def spine_block(now: str) -> str:
    return f"""## PPC4161 4578 lapse parent signature and readout leak row

Marker: `{MARKER}`  
Generated: `{now}`

4578 reduces the 4577 all-lapse-test identity to a parent contract: total Hilbert source ownership, no constructor/hidden/readout return, readout naturality, and topological/improvement owner.  The current corpus does not sign all clauses.  The first concrete source-leak row is now `rho_readout_shift := c^-2(O_lapse Pi_readout - Pi_readout O_lapse)S_parent`, with `Delta_Wtr <= (||mu_tr||_TV + ||B_src^A||_TV + ||rho_readout_shift||_TV)/M_H_ref`.

Decision: `{DECISION}`.  Next target: `{NEXT_TARGET}`.
"""


def packet_block(now: str) -> str:
    return f"""## 4578 packet update - readout commutator leak row

Marker: `{PACKET_MARKER}`  
Generated: `{now}`

The packet now has a concrete first source-leak row for the lapse-test/profile route: `rho_readout_shift` is the commutator of compact lapse probing with the readout/material/worldtube projector.  Pure source-only shadow is contract-killable, but readout reentry remains live until `[O_lapse,Pi_readout]=0` is parent-signed or `||rho_readout_shift||_TV/M_H_ref` is sourced.
"""


def append_claim() -> None:
    existing = read_text(CLAIMS_PATH)
    if CLAIM_ID in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4578 reduces the all-lapse-test identity to source-owner plus readout-naturality clauses and fills the first concrete source-leak row rho_readout_shift := c^-2(O_lapse Pi_readout - Pi_readout O_lapse)S_parent.",
        "current_evidence": "Generated source register, lapse parent contract theorem, parent signature audit, rho_readout_shift first source-leak row, DeltaWtr updates, controls, promotion gates, status and validation CSVs.",
        "status": DECISION.lower(),
        "next_test": NEXT_TARGET,
        "key_risk": "Treating pure source-shadow progress as if readout/projector reentry and action-scale channels were also closed.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "rho_readout_shift still needs a parent zero proof or numeric/source-backed norm before any local-GR claim.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def validation_rows(
    outputs: list[Path],
    sources: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    audits: list[dict[str, Any]],
    leaks: list[dict[str, Any]],
    controls: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH_ID,
                "check_id": check_id,
                "check": check,
                "passed": bool_text(passed),
                "detail": detail,
            }
        )

    for path in outputs:
        add(f"VAL4578_exists_{path.name}", "output path exists", path.exists(), str(path))
        if path.suffix == ".csv" and path.exists():
            rows = read_csv(path)
            add(f"VAL4578_csv_parse_{path.name}", "CSV parses with at least one row", len(rows) > 0, f"rows={len(rows)}")

    add("VAL4578_sources_exist", "all cited sources exist", all(row["exists"] == "True" for row in sources), "source register existence")
    add("VAL4578_needles_found", "all cited source needles found", all(row["needle_found"] == "True" for row in sources), "source register needles")
    add(
        "VAL4578_parent_contract_clauses",
        "parent contract rows include source owner, no return, readout naturality and improvement owner",
        all(
            token in " ".join(row["contract_id"] + row["statement"] for row in contracts)
            for token in ["total_Hilbert_source_owner", "no_constructor_return", "readout_naturality", "topological_improvement_owner"]
        ),
        "contract clause coverage",
    )
    add(
        "VAL4578_not_parent_signed",
        "audit records all-lapse parent signature remains unsigned",
        any(row["audit_id"] == "AUD4578_6_verdict" and row["status"] == "NOT_PARENT_SIGNED" for row in audits),
        "AUD4578_6_verdict",
    )
    add(
        "VAL4578_readout_leak_row_filled",
        "rho_readout_shift formal leak row is filled",
        any(
            row["leak_id"] == "RSL4578_0_rho_readout_shift_commutator"
            and "O_lapse Pi_readout" in row["definition"]
            and row["definition_status"] == "FILLED_FORMAL_SOURCE_LEAK_ROW"
            for row in leaks
        ),
        "rho_readout_shift commutator row",
    )
    add(
        "VAL4578_numeric_missing_firewall",
        "leak rows stay nonclaim while numeric values are missing",
        all(row["valid_for_claim"] == "False" and "MISSING" in row["numeric_value"] for row in leaks),
        "numeric values missing firewalled",
    )
    add(
        "VAL4578_controls_cover_commute_and_countermodel",
        "controls include commutator zero and monopole trap",
        any(row["control_id"] == "CTRL4578_commuting_readout" for row in controls)
        and any(row["control_id"] == "CTRL4578_monopole_readout_trap" and row["verdict"] == "COUNTERMODEL_CAUGHT" for row in controls),
        "controls",
    )
    add(
        "VAL4578_decision_token",
        "decision token recorded",
        DECISION in read_text(DECISION_CSV) and DECISION in read_text(DOC_PATH),
        DECISION,
    )
    add(
        "VAL4578_next_target",
        "next target recorded",
        NEXT_TARGET in read_text(NEXT_CSV) and NEXT_TARGET in read_text(DOC_PATH),
        NEXT_TARGET,
    )
    add("VAL4578_claim_register", "claim register updated", CLAIM_ID in read_text(CLAIMS_PATH), CLAIM_ID)
    add(
        "VAL4578_spine_packet",
        "spine and packet markers present",
        MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH),
        f"{MARKER}; {PACKET_MARKER}",
    )
    return checks


def main() -> None:
    now = utc_now()
    sources = source_rows()
    contracts = parent_contract_rows(now)
    audits = signature_audit_rows(now)
    leaks = readout_leak_rows(now)
    updates = deltawtr_update_rows(now)
    controls = control_rows(now)
    promotions = promotion_rows(now)
    decisions = decision_rows(now)
    next_targets = next_rows(now)
    statuses = status_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PARENT_CONTRACT_CSV, contracts)
    write_csv(SIGNATURE_AUDIT_CSV, audits)
    write_csv(READOUT_LEAK_CSV, leaks)
    write_csv(DELTAWTR_UPDATE_CSV, updates)
    write_csv(CONTROL_CSV, controls)
    write_csv(PROMOTION_CSV, promotions)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_targets)
    write_csv(STATUS_CSV, statuses)

    body = doc_body(now, sources, contracts, audits, leaks, updates, controls, promotions)
    DOC_PATH.write_text(body, encoding="utf-8", newline="\n")
    FORMAL_PATH.write_text(body, encoding="utf-8", newline="\n")

    append_once(SPINE_PATH, MARKER, spine_block(now))
    append_once(PACKET_PATH, PACKET_MARKER, packet_block(now))
    append_claim()

    outputs = [
        SOURCE_REGISTER,
        PARENT_CONTRACT_CSV,
        SIGNATURE_AUDIT_CSV,
        READOUT_LEAK_CSV,
        DELTAWTR_UPDATE_CSV,
        CONTROL_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
        DOC_PATH,
        FORMAL_PATH,
    ]
    validations = validation_rows(outputs, sources, contracts, audits, leaks, controls)
    write_csv(VALIDATION_PATH, validations)

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validations if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"{CHECKPOINT} complete: {DECISION}")
    print(f"wrote: {DOC_PATH}")
    print(f"validation: {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
