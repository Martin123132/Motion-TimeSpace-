from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_DIR = POST / "scripts"

CHECKPOINT = "4821"
CLAIM_ID = "L-663"
MARKER = "PPC4161_PARENT_VISIBLE_EM_GENERATOR_SIGNATURE_OR_HXF2_FIRST_SOURCE_ROW_4821"
DECISION = "VISIBLE_EM_GENERATOR_PARTIAL_EDGE_SIGNED_HXF2_MEMORY_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4822-Y5-R2FR-kappa-memF2-zero-certificate-or-Zmem-M2mem-source-row.md"

DOC_PATH = POST / "4821-Y5-R2FR-parent-visible-EM-generator-signature-or-HXF2-first-source-row.md"
FORMAL_PATH = FORMAL / "837-PPC4161-parent-visible-EM-generator-signature-or-HXF2-first-source-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "visible_EM_generator_HXF2_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4821_SOURCE_REGISTER.csv"
SIGNATURE_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4821_VISIBLE_EM_GENERATOR_SIGNATURE_DERIVATION.csv"
HXF2_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4821_HXF2_FIRST_SOURCE_CONTRACT.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4821_VISIBLE_EM_HXF2_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4821_VISIBLE_EM_HXF2_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4821_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4821_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4821_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4821_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4821_VALIDATION.csv"

PATHS = {
    "resume": RESUME_PATH,
    "4820_doc": POST / "4820-Y5-R2FR-EM-F2-hardblocker-or-first-qbar-marker-bound-row.md",
    "3506_sig": SOURCE_DIR / "P8_Y5_R2FR_3506_PARENT_VISIBLE_EM_GENERATOR_SIGNATURE.csv",
    "4436_doc": POST / "4436-Y5-R2FR-visible-EM-action-edge-parent-signature-or-Kmactionscale-source-leg.md",
    "4436_out": SOURCE_DIR / "P8_Y5_R2FR_4436_VISIBLE_EM_SIGNATURE_OUTPUT.csv",
    "4617_doc": POST / "4617-Y5-R2FR-parent-scalar-functional-exhaustion-or-first-Hom-bound-value.md",
    "4617_hxf2": SOURCE_DIR / "P8_Y5_R2FR_4617_HXF2_COMPONENT_VECTOR_NONCLAIM.csv",
    "4618_cmemory": SOURCE_DIR / "P8_Y5_R2FR_4618_CMEMORY_F2_VALUE_ROW_NONCLAIM.csv",
    "4619_theorem": SOURCE_DIR / "P8_Y5_R2FR_4619_F2_MEMORY_OWNER_THEOREM.csv",
    "4619_source": SOURCE_DIR / "P8_Y5_R2FR_4619_KAPPA_MEMF2_ZMEM_M2MEM_SOURCE_ROWS_NONCLAIM.csv",
    "4620_numeric": SOURCE_DIR / "P8_Y5_R2FR_4620_KAPPA_MEMF2_FIRST_NUMERIC_ROW_NONCLAIM.csv",
    "4704_visible": SOURCE_DIR / "P8_Y5_R2FR_4704_VISIBLE_IMAGE_PROOF_ATTEMPT.csv",
    "4820_output": SOURCE_DIR / "P8_Y5_R2FR_4820_EMF2_RUNNER_OUTPUT.csv",
    "runner": RUNNER,
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(dict.fromkeys(field for row in rows for field in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4821_00_resume", PATHS["resume"], "4821-Y5-R2FR-parent-visible-EM-generator", "current handoff"),
        ("SRC4821_01_4820", PATHS["4820_doc"], "H_XF2", "4820 exact/finite EM gate"),
        ("SRC4821_02_3506", PATHS["3506_sig"], "GEN3506_5_scalar_gauge_kinetic_owner", "parent visible EM generator signature"),
        ("SRC4821_03_4436_doc", PATHS["4436_doc"], "visible EM action edge parent signature", "branch EM edge signature"),
        ("SRC4821_04_4436_out", PATHS["4436_out"], "VISIBLE_EM_EDGE_SIGNATURE_READY_SCALE_GATES_OPEN", "edge ready but scale gates open"),
        ("SRC4821_05_4617_doc", PATHS["4617_doc"], "H_XF2 <= |C_fibre|", "HXF2 component vector law"),
        ("SRC4821_06_4617_hxf2", PATHS["4617_hxf2"], "HXF24617_3_memory", "first HXF2 memory component"),
        ("SRC4821_07_4618_cmemory", PATHS["4618_cmemory"], "CMF4618_0_first_value_contract", "C_memory_F2 first value contract"),
        ("SRC4821_08_4619_theorem", PATHS["4619_theorem"], "FMO4619_3_finite_derivative_law", "finite memory/F2 identity"),
        ("SRC4821_09_4619_source", PATHS["4619_source"], "KMF4619_0_kappa_memF2", "kappa/Z/source rows"),
        ("SRC4821_10_4620_numeric", PATHS["4620_numeric"], "KNUM4620_0_first_numeric_template", "first numeric row template"),
        ("SRC4821_11_4704_visible", PATHS["4704_visible"], "VIP4704_3_reduced_exact_bottleneck", "visible image bottleneck"),
        ("SRC4821_12_4820_output", PATHS["4820_output"], "EM_F2_FINITE_BOUND_PASS_NONCLAIM", "4820 runner handoff"),
        ("SRC4821_13_runner", PATHS["runner"], "def evaluate_row", "4821 runner"),
    ]


def build_source_register(timestamp: str) -> list[dict[str, Any]]:
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


def signature_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "VES4821_0_edge_signature",
            "piece": "standard visible EM edge",
            "derived_law": "S_Maxwell-Hodge[A,g_obs;alpha_obs] in the 4210 standard branch owns EM stress and Poynting flux before readout.",
            "status": "EDGE_SIGNATURE_READY_PRIVATE_BRANCH",
            "blocks": "unique_F2_no_extra_prefactor; charge_current_owner; radiative_closure",
            "source_refs": "4436;4261;4262;4263",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "VES4821_1_generator_full_signature",
            "piece": "full parent visible EM generator",
            "derived_law": "A full generator signature requires edge ownership plus unique F2/no-Hom, charge-current owner, fixed representation constants, no species prefactor, readout-after-variation and radiative closure.",
            "status": "NOT_SIGNED_CURRENT_CORPUS",
            "blocks": "unique F2/current/radiative gates remain open",
            "source_refs": "3506;4436;4704;4820",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "VES4821_2_no_globalization",
            "piece": "standard branch vs global MTS generator",
            "derived_law": "The fixed q-basic standard branch may set C_XF2=0 as a branch condition, but that cannot be globalized to a dynamic MTS parent generator.",
            "status": "FIREWALL_ACTIVE",
            "blocks": "standard_branch_as_global shortcut",
            "source_refs": "4436;4619;4620",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "VES4821_3_memory_Hom_first_row",
            "piece": "first HXF2 source fallback",
            "derived_law": "If no-Hom/typed-domain zero fails, C_memory_F2=|kappa_memF2/Z_Q_eff| Delta_v m_mem at first order.",
            "status": "EXACT_FINITE_IDENTITY_VALUES_MISSING",
            "blocks": "kappa_memF2; Z_Q_eff_min; Delta_v_m_mem; arena K/tau/source rows",
            "source_refs": "4618;4619;4620",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def hxf2_contract(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "HXF24821_0_zero",
            "quantity": "C_memory_F2",
            "formula": "C_memory_F2=0 if typed-domain/no-Hom, fixed branch, branch extremum, or exact symmetry zero is signed in the same branch with readout/radiative closure.",
            "required_inputs": "zero certificate; same branch; readout/radiative closure",
            "status": "conditional_only",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "HXF24821_1_finite",
            "quantity": "C_memory_F2_abs",
            "formula": "|kappa_memF2| * Delta_v_m_mem_abs / Z_Q_eff_min",
            "required_inputs": "kappa_memF2_abs; Z_Q_eff_min>0; Delta_v_m_mem_abs; source_signed; units_signed; same_branch_signed",
            "status": "source_row_ready_values_missing",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "HXF24821_2_qbar",
            "quantity": "qbar_EM_memory_abs",
            "formula": "K_qbar_EM_abs * C_memory_F2_abs",
            "required_inputs": "K_qbar_EM_abs and HXF24821_1",
            "status": "projection_ready_values_missing",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def runner_input(timestamp: str) -> list[dict[str, Any]]:
    true_edge = {
        "action_block_present": True,
        "observed_hodge_owned": True,
        "same_parent_action_line": True,
        "parent_owned_action_domain": True,
        "fixed_representation_constants": True,
        "no_species_source_prefactor": True,
        "readout_after_variation": True,
        "poynting_once_only": True,
    }
    false_scale = {
        "unique_F2_no_extra_prefactor": False,
        "charge_current_owner": False,
        "radiative_closure": False,
    }
    true_scale = {
        "unique_F2_no_extra_prefactor": True,
        "charge_current_owner": True,
        "radiative_closure": True,
    }
    return [
        {
            "row_id": "RUN4821_0_standard_edge_partial",
            "route_type": "generator_signature",
            "route": "4210 standard visible branch",
            "source_path": str(PATHS["4436_doc"]),
            **true_edge,
            **false_scale,
            "input_valid": True,
            "notes": "edge ready but scale/current/radiative gates open",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4821_1_global_generator_blocked",
            "route_type": "generator_signature",
            "route": "global dynamic MTS visible EM generator",
            "source_path": str(PATHS["3506_sig"]),
            "action_block_present": True,
            "observed_hodge_owned": False,
            "same_parent_action_line": False,
            "parent_owned_action_domain": False,
            "fixed_representation_constants": False,
            "no_species_source_prefactor": False,
            "readout_after_variation": False,
            "poynting_once_only": False,
            **false_scale,
            "input_valid": False,
            "notes": "global parent generator still unsigned",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4821_2_conditional_full_generator_pass",
            "route_type": "generator_signature",
            "route": "conditional full parent generator theorem",
            "source_path": str(PATHS["3506_sig"]),
            **true_edge,
            **true_scale,
            "input_valid": True,
            "notes": "theorem-shape smoke only",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4821_3_forbidden_standard_as_global",
            "route_type": "generator_signature",
            "route": "forbidden branch globalization",
            "source_path": "STANDARD_BRANCH_AS_GLOBAL_ALPHA_OBS_AS_DERIVATION",
            **true_edge,
            **true_scale,
            "input_valid": True,
            "notes": "must fail forbidden guard",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4821_4_live_HXF2_missing",
            "route_type": "hxf2_memory_bound",
            "route": "live first HXF2 memory source",
            "source_path": str(PATHS["4619_source"]),
            "kappa_memF2_abs": "MISSING_KAPPA_MEMF2",
            "Z_Q_eff_min": "MISSING_ZQEFF",
            "Delta_v_m_mem_abs": "MISSING_MEMORY_AMPLITUDE",
            "K_qbar_EM_abs": "MISSING_KQBAR",
            "source_signed": False,
            "units_signed": False,
            "same_branch_signed": False,
            "notes": "live source row must block",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4821_5_HXF2_memory_smoke_pass",
            "route_type": "hxf2_memory_bound",
            "route": "finite C_memory_F2 smoke",
            "source_path": str(PATHS["4619_theorem"]),
            "kappa_memF2_abs": "0.02",
            "Z_Q_eff_min": "2.0",
            "Delta_v_m_mem_abs": "0.3",
            "K_qbar_EM_abs": "0.5",
            "source_signed": True,
            "units_signed": True,
            "same_branch_signed": True,
            "notes": "C_memory=0.003 qbar=0.0015 smoke only",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4821_6_HXF2_memory_zero_smoke",
            "route_type": "hxf2_memory_zero",
            "route": "conditional kappa/extremum zero",
            "source_path": str(PATHS["4620_numeric"]),
            "typed_domain_zero": False,
            "fixed_branch_zero": False,
            "branch_extremum_zero": True,
            "symmetry_zero": False,
            "readout_radiative_closure_signed": True,
            "same_branch_signed": True,
            "notes": "conditional zero smoke only",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4821_7_forbidden_bound_as_source",
            "route_type": "hxf2_memory_bound",
            "route": "forbidden empirical backfit",
            "source_path": "BOUND_AS_SOURCE_FIT_TO_BOUND_MEASURED_G_ABSORPTION",
            "kappa_memF2_abs": "0.02",
            "Z_Q_eff_min": "2.0",
            "Delta_v_m_mem_abs": "0.3",
            "K_qbar_EM_abs": "0.5",
            "source_signed": True,
            "units_signed": True,
            "same_branch_signed": True,
            "notes": "must fail forbidden guard",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4821_0_signature_split",
            "decision": "VISIBLE_EM_EDGE_READY_FULL_GENERATOR_OPEN",
            "meaning": "Standard branch owns EM Hodge/stress/Poynting edge, but full generator fails on unique F2, current owner and radiative closure.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4821_1_HXF2_first_row",
            "decision": "C_MEMORY_F2_SELECTED_AS_FIRST_HXF2_SOURCE_ROW",
            "meaning": "First finite source row is C_memory_F2=|kappa_memF2/Z_Q_eff| Delta_v m_mem, with zero switches retained.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4821_2_next_target",
            "decision": NEXT_TARGET,
            "meaning": "Next best derivation target is kappa_memF2 zero/value plus Zmem/M2mem positive-operator source rows.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    gates = [
        ("G4821_0_no_global_EM_claim", "Do not globalize the 4210 standard branch to a dynamic MTS visible EM generator."),
        ("G4821_1_no_alpha_derivation", "Do not treat calibrated alpha or field normalization as a derivation of unique F2."),
        ("G4821_2_no_HXF2_claim", "Do not claim H_XF2=0 or finite until kappa/Z/amplitude/source rows are real or zero-signed."),
        ("G4821_3_no_bound_backfit", "Do not infer kappa_memF2 or memory amplitude by saturating empirical bounds."),
        ("G4821_4_no_local_GR_claim", "Do not claim local GR/Newton/PPN/R10/clock/orbital closure from 4821."),
    ]
    return [
        {
            "gate_id": gate_id,
            "firewall": firewall,
            "status": "ACTIVE_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, firewall in gates
    ]


def run_runner() -> None:
    subprocess.run(["python", str(RUNNER), str(RUNNER_INPUT), str(RUNNER_OUTPUT)], check=True)


def append_claim_register(timestamp: str) -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    fieldnames = [
        "claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk", "sector",
        "evidence", "next_action", "risk", "title", "notes",
    ]
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "parent_visible_EM_generator_signature_or_HXF2_first_source_row",
        "current_evidence": "4821 composes the EM edge signature with the no-Hom/HXF2 ladder: edge/Hodge/Poynting is branch-ready, full generator remains open, and C_memory_F2 is staged as first finite HXF2 row.",
        "status": "visible_EM_generator_HXF2_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "standard branch globalization; unique F2/current/radiative locks; missing kappa_memF2/Z_Q_eff/Delta_v_m_mem/K rows",
        "sector": "local_gr_EM_source_coupling",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "partial branch signature only; finite HXF2 smoke only; no local-GR/Maxwell claim",
        "title": "Parent visible EM generator signature or HXF2 first source row",
        "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.DictWriter(handle, fieldnames=fieldnames).writerow(row)


def append_once(path: Path, block: str, marker: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    path.write_text(text.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def write_docs(timestamp: str) -> None:
    source_rows = read_csv(SOURCE_REGISTER)
    sig_rows = read_csv(SIGNATURE_ROWS)
    hxf2_rows = read_csv(HXF2_CONTRACT)
    out_rows = read_csv(RUNNER_OUTPUT)
    decisions = read_csv(DECISION_CSV)
    gates = read_csv(CLAIM_GATES)
    doc = f"""# 4821 - Parent visible EM generator signature or HXF2 first source row

Marker: `{MARKER}`
Decision: `{DECISION}`
Claim row: `{CLAIM_ID}` private nonclaim
Generated: `{timestamp}`

## Result

4821 attempts the derivation route first. The result is a clean split:

```text
standard visible branch:
EM edge/Hodge/stress/Poynting ownership = ready inside the calibrated 4210 branch

full parent visible EM generator:
requires unique F2/no-Hom + charge-current owner + radiative/readout closure
current corpus does not sign those clauses

finite fallback:
C_memory_F2 = |kappa_memF2/Z_Q_eff| Delta_v m_mem
qbar_EM_memory = K_qbar_EM C_memory_F2
```

This is a real improvement because the EM/Poynting part is preserved as branch-owned source accounting while the missing coupling is reduced to a named coefficient law rather than a foggy coupling complaint.

## Source register

{md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "role"])}

## Generator signature derivation

{md_table(sig_rows, ["row_id", "piece", "derived_law", "status", "blocks"])}

## HXF2 first-source contract

{md_table(hxf2_rows, ["contract_id", "quantity", "formula", "required_inputs", "status"])}

## Runner output

{md_table(out_rows, ["row_id", "route_type", "runner_status", "edge_signature_ready", "full_generator_ready", "C_memory_F2_abs", "qbar_EM_memory_abs", "claim_allowed"])}

## Claim gates

{md_table(gates, ["gate_id", "firewall", "status", "claim_allowed"])}

## Decision ledger

{md_table(decisions, ["decision_id", "decision", "meaning"])}

## Next target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")
    packet = f"""## {MARKER}

- Doc: `{DOC_PATH}`
- Runner: `{RUNNER}`
- Claim row: `{CLAIM_ID}`
- Decision: `{DECISION}`
- Next: `{NEXT_TARGET}`
- Summary: visible EM edge is branch-ready, full generator remains open, and `C_memory_F2=|kappa_memF2/Z_Q_eff| Delta_v m_mem` is staged as the first `H_XF2` source row.
"""
    append_once(PACKET_PATH, packet, MARKER)
    spine = f"""## {MARKER}

4821 sharpens the EM coupling spine:

```text
edge branch signed: Maxwell-Hodge stress/Poynting once in 4210 branch
full generator open: unique F2 + current owner + radiative/readout closure
first HXF2 row: C_memory_F2=|kappa_memF2/Z_Q_eff| Delta_v m_mem
```

This keeps the Mayweather route alive: do not need to smash alpha prediction; need to keep visible EM source accounting clean and bound/derive the remaining coupling coefficient.
"""
    append_once(SPINE_PATH, spine, MARKER)
    resume = f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4821-Y5-R2FR-parent-visible-EM-generator-signature-or-HXF2-first-source-row.md`
Marker: `{MARKER}`

## Where we are

4821 tried the parent visible EM generator route and found:

```text
EM edge/Hodge/stress/Poynting once = branch-ready in the 4210 standard visible branch.
Full dynamic parent generator = not signed because unique F2/current/radiative gates remain open.
C_memory_F2 = |kappa_memF2/Z_Q_eff| Delta_v m_mem is the first H_XF2 finite row.
```

## Live blockers

- `unique_F2_no_extra_prefactor`, `charge_current_owner`, and `radiative_closure` remain unsigned for the full generator.
- `kappa_memF2`, `Z_Q_eff_min`, `Delta_v_m_mem`, `K_qbar_EM`, and memory positive-operator/source rows are missing.
- The fixed visible branch cannot be globalized into a dynamic MTS derivation.

## Next target

`{NEXT_TARGET}`
"""
    RESUME_PATH.write_text(resume, encoding="utf-8")


def validate(timestamp: str) -> list[dict[str, Any]]:
    source_rows = read_csv(SOURCE_REGISTER)
    out = read_csv(RUNNER_OUTPUT)
    status = {row["row_id"]: row["runner_status"] for row in out}
    qbar = {row["row_id"]: row["qbar_EM_memory_abs"] for row in out}
    claims = read_text(CLAIMS_PATH)
    resume = read_text(RESUME_PATH)
    checks = [
        ("VAL4821_0_sources", all(row["exists"] == "True" and row["needle_found"] == "True" for row in source_rows), str(SOURCE_REGISTER)),
        ("VAL4821_1_signature_rows", len(read_csv(SIGNATURE_ROWS)) >= 4 and "VES4821_1_generator_full_signature" in read_text(SIGNATURE_ROWS), str(SIGNATURE_ROWS)),
        ("VAL4821_2_hxf2_contract", len(read_csv(HXF2_CONTRACT)) >= 3 and "HXF24821_1_finite" in read_text(HXF2_CONTRACT), str(HXF2_CONTRACT)),
        ("VAL4821_3_standard_edge_partial", status.get("RUN4821_0_standard_edge_partial") == "VISIBLE_EM_EDGE_SIGNATURE_READY_SCALE_GATES_OPEN", str(RUNNER_OUTPUT)),
        ("VAL4821_4_global_blocks", status.get("RUN4821_1_global_generator_blocked") == "BLOCKED_VISIBLE_EM_GENERATOR_SIGNATURE", str(RUNNER_OUTPUT)),
        ("VAL4821_5_conditional_full_pass", status.get("RUN4821_2_conditional_full_generator_pass") == "VISIBLE_EM_GENERATOR_SIGNATURE_PASS_NONCLAIM", str(RUNNER_OUTPUT)),
        ("VAL4821_6_forbidden_globalization_fails", status.get("RUN4821_3_forbidden_standard_as_global") == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", str(RUNNER_OUTPUT)),
        ("VAL4821_7_live_hxf2_blocks", status.get("RUN4821_4_live_HXF2_missing") == "BLOCKED_HXF2_MEMORY_SOURCE_INPUTS", str(RUNNER_OUTPUT)),
        ("VAL4821_8_hxf2_smoke_pass", status.get("RUN4821_5_HXF2_memory_smoke_pass") == "HXF2_MEMORY_SOURCE_BOUND_PASS_NONCLAIM" and qbar.get("RUN4821_5_HXF2_memory_smoke_pass", "").startswith("1.500"), str(RUNNER_OUTPUT)),
        ("VAL4821_9_hxf2_zero_smoke", status.get("RUN4821_6_HXF2_memory_zero_smoke") == "HXF2_MEMORY_ZERO_PASS_NONCLAIM", str(RUNNER_OUTPUT)),
        ("VAL4821_10_forbidden_backfit_fails", status.get("RUN4821_7_forbidden_bound_as_source") == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", str(RUNNER_OUTPUT)),
        ("VAL4821_11_claim_gates", all(row["claim_allowed"] == "False" for row in read_csv(CLAIM_GATES)), str(CLAIM_GATES)),
        ("VAL4821_12_claim_register", CLAIM_ID in claims and DECISION in claims, str(CLAIMS_PATH)),
        ("VAL4821_13_resume", NEXT_TARGET in resume and MARKER in resume, str(RESUME_PATH)),
        ("VAL4821_14_docs", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH};{FORMAL_PATH}"),
        ("VAL4821_15_pycache", not (SCRIPT_DIR / "__pycache__").exists(), str(SCRIPT_DIR / "__pycache__")),
    ]
    rows = [
        {
            "check_id": check_id,
            "description": check_id.replace("_", " "),
            "result": "PASS" if passed else "FAIL",
            "evidence": evidence,
            "timestamp_utc": timestamp,
        }
        for check_id, passed, evidence in checks
    ]
    rows.append(
        {
            "check_id": "VAL4821_OVERALL",
            "description": "all 4821 validation gates pass",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "evidence": str(VALIDATION_CSV),
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> int:
    timestamp = now()
    py_compile.compile(str(RUNNER), doraise=True)
    write_csv(SOURCE_REGISTER, build_source_register(timestamp))
    write_csv(SIGNATURE_ROWS, signature_rows(timestamp))
    write_csv(HXF2_CONTRACT, hxf2_contract(timestamp))
    write_csv(RUNNER_INPUT, runner_input(timestamp))
    run_runner()
    write_csv(DECISION_CSV, decision_rows(timestamp))
    write_csv(CLAIM_GATES, claim_gate_rows(timestamp))
    write_csv(STATUS_CSV, [{"checkpoint": CHECKPOINT, "marker": MARKER, "decision": DECISION, "claim_allowed": False, "valid_for_claim": False, "next_target": NEXT_TARGET, "timestamp_utc": timestamp}])
    write_csv(NEXT_TARGET_CSV, [{"checkpoint": CHECKPOINT, "next_target": NEXT_TARGET, "why": "kappa_memF2 zero/value and Zmem/M2mem source rows are the next concrete coupling row.", "valid_for_claim": False, "timestamp_utc": timestamp}])
    append_claim_register(timestamp)
    write_docs(timestamp)
    py_compile.compile(str(Path(__file__)), doraise=True)
    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation_rows = validate(timestamp)
    write_csv(VALIDATION_CSV, validation_rows)
    if validation_rows[-1]["result"] != "PASS":
        print(f"{MARKER}: validation FAIL; inspect {VALIDATION_CSV}")
        return 1
    print(f"{MARKER}: validation PASS; next {NEXT_TARGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
