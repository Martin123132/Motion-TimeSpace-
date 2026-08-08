from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4617"
CLAIM_ID = "L-459"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_SCALAR_FUNCTIONAL_EXHAUSTION_4617"
MARKER = "PPC4161_PARENT_SCALAR_FUNCTIONAL_EXHAUSTION_OR_FIRST_HOM_BOUND_4617"
PACKET_MARKER = "PPC4161_PACKET_PARENT_SCALAR_FUNCTIONAL_EXHAUSTION_4617"
DECISION = "PARENT_SCALAR_FUNCTIONAL_EXHAUSTION_REDUCED_TO_TRANSITIVE_FIBRE_TRIVIALITY_NONCLAIM_FIRST_HXF2_VECTOR_READY"
NEXT_TARGET = "4618-Y5-R2FR-memory-class-scalar-nohair-or-first-HXF2-value.md"

DOC_PATH = POST / "4617-Y5-R2FR-parent-scalar-functional-exhaustion-or-first-Hom-bound-value.md"
FORMAL_PATH = FORMAL / "633-PPC4161-parent-scalar-functional-exhaustion-or-first-Hom-bound-value.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4617_SOURCE_REGISTER.csv"
SCALAR_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4617_PARENT_SCALAR_FUNCTIONAL_THEOREM.csv"
FIBRE_CERT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4617_TRANSITIVE_FIBRE_CERTIFICATE_ROWS.csv"
HXF2_VECTOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4617_HXF2_COMPONENT_VECTOR_NONCLAIM.csv"
EM_CONSEQUENCE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4617_EM_COUPLING_CONSEQUENCE_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4617_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4617_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4617_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4617_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4617_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4617_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4617_VALIDATION.csv"

CSV_4616_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4616_NEXT_TARGET.csv"
CSV_4616_PROOF = SOURCE_DIR / "P8_Y5_R2FR_4616_VISIBLE_IMAGE_PROOF_ATTEMPT.csv"
CSV_4616_HOM = SOURCE_DIR / "P8_Y5_R2FR_4616_HIDDEN_HOM_BOUND_ROWS_NONCLAIM.csv"
CSV_4426_DERIVATION = SOURCE_DIR / "P8_Y5_R2FR_4426_DERIVATION_ROWS.csv"
CSV_4426_FIBRE = SOURCE_DIR / "P8_Y5_R2FR_4426_TRANSITIVE_FIBRE_OUTPUT.csv"
CSV_4426_CSOURCE = SOURCE_DIR / "P8_Y5_R2FR_4426_CSOURCE_VECTOR_OUTPUT.csv"
CSV_4213_QBASIC = SOURCE_DIR / "P8_Y5_R2FR_4213_QBASIC_VERTICAL_THEOREM.csv"
CSV_3142_EM_QBASIC = SOURCE_DIR / "P8_Y5_R2FR_3142_EM_QBASIC_THEOREM.csv"
CSV_980_THEOREM = SOURCE_DIR / "P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv"
CSV_980_COUNTER = SOURCE_DIR / "P8_Y5_R10_980_COUNTEREXAMPLE_LEDGER.csv"
CSV_2659_THEOREM = SOURCE_DIR / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv"

PUBLIC_STAGE = Path("D:/Users/ollet/Desktop/Motion-TimeSpace-public-stage")
BACKUP_REPO = Path("D:/Users/ollet/Desktop/laptop-back-up-")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


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
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
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
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines)


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for number, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return number
    return 0


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    suffix = "\n" if text.endswith("\n") or not text else "\n\n"
    write_text(path, text + suffix + block.strip() + "\n")


def git_clean(path: Path) -> bool:
    if not path.exists() or not (path / ".git").exists():
        return True
    result = subprocess.run(["git", "-C", str(path), "status", "--porcelain"], text=True, capture_output=True, check=False)
    return result.returncode == 0 and result.stdout.strip() == ""


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4617_00_4616_next", CSV_4616_NEXT, "4617-Y5-R2FR-parent-scalar-functional-exhaustion-or-first-Hom-bound-value.md", "4616 selected parent scalar-functional exhaustion."),
        ("SRC4617_01_4616_proof", CSV_4616_PROOF, "VIP4616_3_reduced_exact_bottleneck", "4616 reduced the gap to Scal_parent^vis."),
        ("SRC4617_02_4616_hom", CSV_4616_HOM, "HOM4616_0_C_XF2_kernel_norm", "4616 staged H_XF2 bound rows."),
        ("SRC4617_03_4426_derivation", CSV_4426_DERIVATION, "HFT4426_0_transitive_fibre_lemma", "4426 transitive fibre invariant-triviality theorem."),
        ("SRC4617_04_4426_fibre", CSV_4426_FIBRE, "HFT4426_1_exact_transitive_lemma", "4426 fibre certificate output."),
        ("SRC4617_05_4426_csource", CSV_4426_CSOURCE, "CSVIN4426_3_memory", "4426 finite surviving generator vector."),
        ("SRC4617_06_4213_qbasic", CSV_4213_QBASIC, "QVP4213_1_pullback_action", "4213 q-basic vertical action criterion."),
        ("SRC4617_07_3142_em", CSV_3142_EM_QBASIC, "EMQ3142_2_balpha_zero", "3142 q-basic EM sector consequence."),
        ("SRC4617_08_980_obstruction", CSV_980_THEOREM, "NMF980_2_scalar_obstruction_lemma", "980 scalar obstruction lemma."),
        ("SRC4617_09_980_counter", CSV_980_COUNTER, "CEX980_4_memory_class_scalar", "980 memory/class scalar counterexample."),
        ("SRC4617_10_2659_typed", CSV_2659_THEOREM, "ODT2659_1_exact_typed_theorem", "2659 typed coefficient-domain theorem."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in specs:
        text = read_text(path)
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": source_id,
            "path": str(path),
            "path_exists": path.exists(),
            "needle": needle,
            "needle_found": needle in text,
            "line": line_of(path, needle),
            "role": role,
            "valid_for_claim": False,
            "timestamp_utc": now,
        })
    return rows


def scalar_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "PSF4617_0_transitive_fibre_triviality",
            "claim_piece": "hidden invariant scalar exhaustion",
            "formal_statement": "Let F_q be the hidden fibre over an observed local state q and G_v a parent vertical group acting transitively on F_q. If admissible hidden scalars are G_v-invariant smooth functions, then O(F_q)^G_v = R.",
            "derivation": "For p1,p2 in F_q, transitivity gives g in G_v with p2=g p1. Invariance gives I(p2)=I(g p1)=I(p1). Since F_q is connected and homogeneous, I is constant.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "current_status": "GAUGE_ACTION_SPAN_AND_FIBRE_REGULARITY_UNSIGNED",
            "source_refs": "HFT4426_0_transitive_fibre_lemma;HFT4426_1_exact_transitive_lemma",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "PSF4617_1_EM_F2_Hom_consequence",
            "claim_piece": "F2 hidden-Hom zero from invariant triviality",
            "formal_statement": "If O(F_q)^G_v=R and Coeff(F_Q^2) is parent-image/fixed, then every hidden scalar map into the EM F2 coefficient is constant; therefore H_XF2=0 and D_v lambda_F2=0.",
            "derivation": "4616 reduced the coupling gap to hidden/readout/material scalar maps into Coeff(F_Q^2). The transitive-fibre theorem kills the hidden scalar part; typed image/no-target kills nonconstant coefficient maps.",
            "result": "EXACT_CONDITIONAL_EM_COUPLING_ZERO",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "source_refs": "VIP4616_0_exact_image_zero_theorem;VIP4616_1_hidden_Hom_kernel_theorem;EMQ3142_2_balpha_zero",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "PSF4617_2_qbasic_action_route",
            "claim_piece": "q-basic parent action route",
            "formal_statement": "If L_parent|loc=q^*L_red+dB_vert and the EM sector is q-basic with fixed Z_Q=C_P N_Q, then vertical bulk variations and b_alpha vanish before local readout.",
            "derivation": "The q-basic chain rule kills D_v q-owned data, while the q-basic EM sector has no independent lambda_A or hidden f_X F_Q^2 coefficient.",
            "result": "EXACT_CONDITIONAL_ACTION_ROUTE",
            "current_status": "PULLBACK_ACTION_AND_NO_EXTRA_F2_UNSIGNED",
            "source_refs": "QVP4213_1_pullback_action;EMQ3142_0_qbasic_sector;EMQ3142_2_balpha_zero",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "PSF4617_3_scalar_obstruction_guard",
            "claim_piece": "surviving scalar obstruction",
            "formal_statement": "If any nonconstant hidden invariant scalar I_hid survives, lambda_F2=lambda_0+epsilon I_hid remains a legal coefficient unless the parent object language forbids Coeff(F_Q^2) as a target.",
            "derivation": "980 proves the obstruction: one invariant scalar can feed a continuous coefficient. 4616 specializes this to the EM F2 coefficient.",
            "result": "COUNTERMODEL_RETAINED",
            "current_status": "MEMORY_DOMAIN_READOUT_GENERATORS_LIVE",
            "source_refs": "NMF980_2_scalar_obstruction_lemma;CEX980_4_memory_class_scalar;VIP4616_2_scalar_functional_countermodel",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "PSF4617_4_finite_vector_fallback",
            "claim_piece": "H_XF2 component vector",
            "formal_statement": "If invariant triviality is unsigned, H_XF2 is bounded by the absolute component vector C_fibre+C_domain+C_chiD+C_memory+C_time+C_species+C_readout plus radiative/readout F2 tails.",
            "derivation": "4426 already decomposes surviving hidden generators; 4617 imports that decomposition specifically as the EM F2 Hom-bound vector.",
            "result": "FINITE_VECTOR_CONTRACT_STAGED",
            "current_status": "NO_NUMERIC_OR_DERIVED_ZERO_VALUES",
            "source_refs": "CSVIN4426_0_fibre through CSVIN4426_6_readout;HOM4616_0_C_XF2_kernel_norm",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def fibre_certificate_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "certificate_id": "FIB4617_0_current_kernel",
            "clause": "q-map and vertical kernel",
            "q_map_defined": True,
            "vertical_distribution_defined": True,
            "gauge_action_parent_signed": False,
            "action_spans_kernel": False,
            "fibre_connected_regular": False,
            "invariant_policy_signed": False,
            "generator_elimination_complete": False,
            "radiative_readout_closure": False,
            "status": "VERTICAL_KERNEL_DEFINED_NOT_GAUGE_ORBIT",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "certificate_id": "FIB4617_1_exact_if_signed",
            "clause": "connected transitive fibre theorem",
            "q_map_defined": True,
            "vertical_distribution_defined": True,
            "gauge_action_parent_signed": True,
            "action_spans_kernel": True,
            "fibre_connected_regular": True,
            "invariant_policy_signed": True,
            "generator_elimination_complete": True,
            "radiative_readout_closure": True,
            "status": "WOULD_SIGN_O_FQ_INVARIANTS_EQUALS_R_AND_HXF2_ZERO",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "certificate_id": "FIB4617_2_current_gap",
            "clause": "surviving generator debt",
            "q_map_defined": True,
            "vertical_distribution_defined": True,
            "gauge_action_parent_signed": False,
            "action_spans_kernel": False,
            "fibre_connected_regular": False,
            "invariant_policy_signed": True,
            "generator_elimination_complete": False,
            "radiative_readout_closure": False,
            "status": "FINITE_GENERATOR_VECTOR_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def hxf2_vector_rows(now: str) -> list[dict[str, Any]]:
    components = [
        ("HXF24617_0_fibre", "C_fibre", "finite_cell_fibre_spectrum", "R10_PPN_clock_source_mass_projection_required", "P8_Y5_R2FR_4426_CSOURCE_VECTOR_OUTPUT.csv"),
        ("HXF24617_1_domain", "C_domain", "relative_boundary_domain_class", "local_GR_PPN_R10_orbital_projection_required", "P8_Y5_R2FR_4426_CSOURCE_VECTOR_OUTPUT.csv"),
        ("HXF24617_2_chiD", "C_chiD", "domain_selector_chi_D", "local_GR_R10_cosmology_split_projection_required", "P8_Y5_R2FR_4426_CSOURCE_VECTOR_OUTPUT.csv"),
        ("HXF24617_3_memory", "C_memory_F2", "memory_or_class_scalar", "clock_PPN_R10_cosmology_projection_required", "P8_Y5_R2FR_4426_CSOURCE_VECTOR_OUTPUT.csv"),
        ("HXF24617_4_time", "C_time_F2", "orientation_time_arrow", "preferred_frame_clock_PPN_projection_required", "P8_Y5_R2FR_4426_CSOURCE_VECTOR_OUTPUT.csv"),
        ("HXF24617_5_species", "C_species_F2", "species_charge_constants", "WEP_clock_R10_source_mass_projection_required", "P8_Y5_R2FR_4426_CSOURCE_VECTOR_OUTPUT.csv"),
        ("HXF24617_6_readout", "C_readout_F2", "readout_projector", "measured_G_PPN_clock_WEP_projection_required", "P8_Y5_R2FR_4426_CSOURCE_VECTOR_OUTPUT.csv"),
        ("HXF24617_7_rad", "C_rad_F2", "radiative_threshold_tail", "clock_spectroscopy_alpha_projection_required", "P8_Y5_R2FR_4616_HIDDEN_HOM_BOUND_ROWS_NONCLAIM.csv"),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, symbol, generator, projection, source_name in components:
        rows.append({
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "symbol": symbol,
            "generator": generator,
            "contributes_to": "H_XF2",
            "value": "MISSING_NUMERIC_OR_DERIVED_ZERO",
            "units": "dimensionless derivative contribution",
            "parent_variation_basis": "MISSING_PARENT_VARIATION_BASIS",
            "observable_projection": projection,
            "source_path": str(SOURCE_DIR / source_name),
            "bound_formula": f"H_XF2 >= abs({symbol}) as no-cancellation component unless theorem-zero",
            "next_action": "derive theorem-zero or fill source-backed value",
            "input_valid": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        })
    return rows


def em_consequence_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "EMC4617_0_exact_branch",
            "branch": "transitive fibre + q-basic EM + no target Coeff(F_Q^2)",
            "consequence": "H_XF2=0; s_XF2=0; b_alpha_X=2 z_g up to readout/radiative terms; if same-current z_g=0 then b_alpha_X=0",
            "claim_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "EMC4617_1_finite_branch",
            "branch": "hidden invariant or readout/radiative scalar survives",
            "consequence": "H_XF2 <= sum_i |C_i^F2| + |C_rad_F2| + |C_readout_F2|; use K_A H_XF2 in R10/PPN/clock/orbital arenas",
            "claim_status": "NONCLAIM_VALUE_ROWS_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "EMC4617_2_first_priority",
            "branch": "least-scrutiny next finite target",
            "consequence": "Attack C_memory_F2 first: either memory/class scalar is gauge/no-hair/profile-zero, or it becomes the first explicit H_XF2 coefficient.",
            "claim_status": "NEXT_TARGET_SELECTED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4617_0_no_Dq_shortcut",
            "rule": "Dq[v]=0 alone does not kill hidden scalar coefficients; invariant algebra triviality or coefficient-domain exclusion is required.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4617_1_no_gauge_word_shortcut",
            "rule": "Do not call the hidden fibre gauge unless a parent vertical action spans the kernel and the fibre is connected/regular.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4617_2_no_public_claim",
            "rule": "This checkpoint is a private derivation advance, not a local-GR/Maxwell/alpha pass.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4617_0_vertical_gauge_action",
            "claim_blocked": "O(F_q)^G=R and H_XF2=0",
            "missing_signature": "parent-signed vertical gauge/representative group action",
            "next_action": "construct action or fill H_XF2 component values",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4617_1_kernel_span",
            "claim_blocked": "hidden invariant triviality",
            "missing_signature": "vertical action spans all coefficient-relevant kernel directions",
            "next_action": "prove span or keep C_fibre/C_memory/C_readout rows",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4617_2_memory_class_scalar",
            "claim_blocked": "first finite Hom row",
            "missing_signature": "memory/class scalar no-hair, profile-zero, or numeric parent coefficient",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["needle_found"] for row in sources)
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4617_0_exact_exhaustion",
            "requirement": "transitive connected fibre + invariant observable policy + generator elimination + q-basic EM + no Coeff(F_Q^2) target + radiative/readout closure",
            "current_status": "BLOCKED_PARENT_SIGNATURE_UNSIGNED",
            "sources_valid": sources_ok,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4617_1_first_HXF2_value",
            "requirement": "source-backed C_memory_F2 or theorem-zero memory/class scalar route, plus arena projection",
            "current_status": "BLOCKED_VALUE_MISSING",
            "sources_valid": sources_ok,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4617_0",
            "decision": DECISION,
            "what_changed": "The scalar-functional exhaustion route is no longer a vague parent-domain demand: it is reduced to hidden-fibre invariant triviality plus EM q-basic/no-target clauses.",
            "claim_status": "NONCLAIM_PRIVATE_DERIVATION_STAGE",
            "exact_path": "prove hidden fibre is connected transitive parent gauge/representative orbit, then O(F_q)^G=R and H_XF2=0",
            "fallback_path": "fill H_XF2 component vector, first priority C_memory_F2",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "status": "PRIVATE_NONCLAIM_DERIVATION_ADVANCE",
            "summary": "Parent scalar-functional exhaustion is reduced to connected transitive fibre invariant triviality; finite H_XF2 component vector is staged.",
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": now,
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "timestamp_utc": now,
            "next_target": NEXT_TARGET,
            "why": "The first live generator most directly capable of feeding F_Q^2 is memory/class scalar leakage.",
            "derive_path": "prove memory/class scalar is gauge, q-basic constant, no-hair/profile-zero, or has no target Coeff(F_Q^2)",
            "fallback_path": "fill C_memory_F2 as first H_XF2 value with units, parent variation basis and arena projections",
            "claim_allowed": False,
        }
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4617 - Parent Scalar-Functional Exhaustion Or First Hom Bound Value

Generated UTC: `{now}`

Marker: `{MARKER}`

## Result

4617 attacks the coupling bottleneck directly.

The exact route is now:

```text
F_q = hidden fibre over observed q
G_v acts connected-transitively on F_q
admissible hidden scalars are G_v-invariant
=> O(F_q)^G_v = R
=> H_XF2 = 0
```

That is the strongest non-hand-wavy way to kill hidden scalar leakage into `Coeff(F_Q^2)`.

Current corpus status: the theorem shape is exact, but the parent-signed vertical gauge action, kernel span, connected fibre regularity, generator elimination and radiative/readout closure are not all signed. Therefore no claim fires.

The finite fallback is explicit:

```text
H_XF2 <= |C_fibre|+|C_domain|+|C_chiD|+|C_memory_F2|+|C_time_F2|+|C_species_F2|+|C_readout_F2|+|C_rad_F2|.
```

The next least-scrutiny target is `C_memory_F2`: either prove memory/class scalar no-hair/profile-zero/no-target, or fill it as the first real `H_XF2` value.

## Source Register

{markdown_table(tables["sources"])}

## Parent Scalar Functional Theorem

{markdown_table(tables["scalar_theorem"])}

## Transitive Fibre Certificate Rows

{markdown_table(tables["fibre_certificate"])}

## H_XF2 Component Vector Nonclaim

{markdown_table(tables["hxf2_vector"])}

## EM Coupling Consequences

{markdown_table(tables["em_consequence"])}

## Controls

{markdown_table(tables["controls"])}

## Claim Blockers

{markdown_table(tables["blockers"])}

## Promotion Gates

{markdown_table(tables["promotion"])}

## Decision

{markdown_table(tables["decision"])}

## Status

{markdown_table(tables["status"])}

## Next Target

`{NEXT_TARGET}`
"""


def build_formal(now: str) -> str:
    return f"""# PPC4161 Formal Addendum 633 - Parent Scalar-Functional Exhaustion Or First Hom Bound

Generated UTC: `{now}`

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

## Transitive Fibre Route

Let `F_q` be the hidden fibre over observed local state `q`, and let `G_v` be a parent vertical group acting transitively on `F_q`. If admissible hidden scalars are `G_v`-invariant, then

```text
O(F_q)^{{G_v}} = R.
```

Thus any hidden scalar map into `Coeff(F_Q^2)` is constant. Combined with the 4616 image/no-target theorem,

```text
H_XF2 = 0,
D_v lambda_F2 = 0.
```

## Current Limit

The current corpus has the exact theorem but not the parent signature: vertical gauge action, kernel span, connected fibre regularity, generator elimination and radiative/readout closure remain unsigned.

## Finite Branch

If memory/domain/readout generators survive,

```text
H_XF2 <= |C_fibre|+|C_domain|+|C_chiD|+|C_memory_F2|+|C_time_F2|+|C_species_F2|+|C_readout_F2|+|C_rad_F2|.
```

Next target: `{NEXT_TARGET}`.
"""


def append_claim_once() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = {
        "claim_id": CLAIM_ID,
        "sector": "local_gr_empirical_interface",
        "claim": "4617 reduces parent scalar-functional exhaustion for the EM F2 coupling to connected transitive hidden-fibre invariant triviality, and stages the finite H_XF2 component vector if the theorem is not parent-signed.",
        "evidence": "Generated scalar theorem rows, transitive fibre certificate rows, H_XF2 component vector, EM consequence rows, controls, blockers, promotion gates, decision, status, next target and validation.",
        "status": "parent_scalar_functional_exhaustion_transitive_fibre_theorem_nonclaim_HXF2_vector_staged",
        "next_action": NEXT_TARGET,
        "risk": "Calling hidden directions gauge without a parent vertical action spanning the kernel, or treating Dq[v]=0 as invariant algebra triviality.",
        "owner": "local_gr",
        "source_path": str(DOC_PATH),
        "next_target": NEXT_TARGET,
        "notes": "No b_alpha, Maxwell, WEP, clock, R10, Newton or local-GR pass until fibre triviality and EM no-target/readout/current clauses are signed or H_XF2 component values are source-backed.",
    }
    existing = read_text(CLAIMS_PATH)
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not existing.endswith("\n"):
            handle.write("\n")
        writer.writerow(row)


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        })

    missing_sources = [row["source_id"] for row in tables["sources"] if not row["path_exists"] or not row["needle_found"]]
    add("VAL4617_00_sources_exist_and_needles_found", not missing_sources, "missing: " + ",".join(missing_sources) if missing_sources else "all cited paths/needles found")

    csv_paths = [
        SOURCE_REGISTER, SCALAR_THEOREM_CSV, FIBRE_CERT_CSV, HXF2_VECTOR_CSV, EM_CONSEQUENCE_CSV,
        CONTROL_CSV, BLOCKERS_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV,
    ]
    csv_ok = True
    details: list[str] = []
    for path in csv_paths:
        parsed = read_csv(path)
        details.append(f"{path.name}:{len(parsed)}")
        csv_ok = csv_ok and bool(parsed)
    add("VAL4617_01_csv_parse", csv_ok, ";".join(details))

    theorem_text = "\n".join(str(row) for row in tables["scalar_theorem"])
    fibre_text = "\n".join(str(row) for row in tables["fibre_certificate"])
    vector_text = "\n".join(str(row) for row in tables["hxf2_vector"])
    em_text = "\n".join(str(row) for row in tables["em_consequence"])
    add("VAL4617_02_transitive_theorem", "O(F_q)^G_v = R" in theorem_text and "EXACT_CONDITIONAL_THEOREM" in theorem_text, "transitive fibre theorem present")
    add("VAL4617_03_countermodel_guard", "lambda_F2=lambda_0+epsilon I_hid" in theorem_text and "COUNTERMODEL_RETAINED" in theorem_text, "scalar obstruction retained")
    add("VAL4617_04_fibre_certificate", "VERTICAL_KERNEL_DEFINED_NOT_GAUGE_ORBIT" in fibre_text and "WOULD_SIGN_O_FQ_INVARIANTS_EQUALS_R" in fibre_text, "fibre certificate rows present")
    add("VAL4617_05_HXF2_vector", "C_memory_F2" in vector_text and "C_readout_F2" in vector_text and "C_rad_F2" in vector_text, "H_XF2 vector rows present")
    add("VAL4617_06_EM_consequence", "H_XF2=0" in em_text and "C_memory_F2" in em_text, "EM consequence rows present")

    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "claim_pass", "empirical_pass_claimed", "score_ready"} and value is True:
                    all_false = False
    add("VAL4617_07_no_claim_true", all_false, "no generated row promotes a claim")
    add("VAL4617_08_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4617_09_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4617_10_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4617_11_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4617_12_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4617_13_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4617_14_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4617_15_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4617_OVERALL", all(row["status"] == "PASS" for row in rows), "4617 scalar-functional exhaustion checkpoint")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "scalar_theorem": scalar_theorem_rows(now),
        "fibre_certificate": fibre_certificate_rows(now),
        "hxf2_vector": hxf2_vector_rows(now),
        "em_consequence": em_consequence_rows(now),
        "controls": control_rows(now),
        "blockers": blocker_rows(now),
        "promotion": [],
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    tables["promotion"] = promotion_rows(now, tables["sources"])
    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(SCALAR_THEOREM_CSV, tables["scalar_theorem"])
    write_csv(FIBRE_CERT_CSV, tables["fibre_certificate"])
    write_csv(HXF2_VECTOR_CSV, tables["hxf2_vector"])
    write_csv(EM_CONSEQUENCE_CSV, tables["em_consequence"])
    write_csv(CONTROL_CSV, tables["controls"])
    write_csv(BLOCKERS_CSV, tables["blockers"])
    write_csv(PROMOTION_CSV, tables["promotion"])
    write_csv(DECISION_CSV, tables["decision"])
    write_csv(STATUS_CSV, tables["status"])
    write_csv(NEXT_CSV, tables["next"])
    write_text(DOC_PATH, build_doc(now, tables))
    write_text(FORMAL_PATH, build_formal(now))
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## PPC4161 Local Addendum - Parent Scalar-Functional Exhaustion Or First Hom Bound

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

4617 reduces the EM hidden-Hom coupling route to hidden-fibre invariant triviality. If the hidden fibre over observed `q` is a connected transitive parent gauge/representative orbit, then `O(F_q)^G=R`; combined with the 4616 visible-image/no-target theorem this gives `H_XF2=0` and `D_v lambda_F2=0`. Current MTS does not parent-sign the gauge action/span/regularity/generator-elimination package, so the fallback is the explicit `H_XF2` vector with first target `C_memory_F2`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - Parent Scalar-Functional Exhaustion Or First Hom Bound

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The private packet now has a genuine derivation fork: prove hidden invariant scalars are constants by connected transitive fibre geometry, or quantify the first finite EM Hom component. Next target is memory/class scalar no-hair/profile-zero or a first source-backed `C_memory_F2` value.
""",
    )
    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4617 validation failed: {failed}")
    print(f"4617 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
