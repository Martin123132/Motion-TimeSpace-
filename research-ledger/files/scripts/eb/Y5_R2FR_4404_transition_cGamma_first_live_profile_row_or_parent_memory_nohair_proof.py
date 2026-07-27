from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from cGamma_profile_nohair_gate import (  # noqa: E402
    evaluate_aj_rows,
    evaluate_nohair_rows,
    evaluate_product_rows,
    read_csv,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4404"
CLAIM_ID = "L-245"
MARKER = "PPC4161_TRANSITION_CGAMMA_FIRST_LIVE_PROFILE_ROW_OR_PARENT_MEMORY_NOHAIR_PROOF_4404"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_CGAMMA_FIRST_LIVE_PROFILE_ROW_OR_PARENT_MEMORY_NOHAIR_PROOF_4404"
DECISION = "CGAMMA_SPLIT_INTO_MEMORY_NOHAIR_PRODUCT_AND_AJ_PRESSURE_GATES_FINITE_MARGIN_AJ_ZERO_IMPORT_NONCLAIM"
NEXT_TARGET = "4405-Y5-R2FR-transition-cGamma-transition-shell-Pleak-first-two-components-or-profile-bound.md"

FORMAL_PATH = FORMAL / "420-PPC4161-transition-cGamma-first-live-profile-row-or-parent-memory-nohair-proof.md"
DOC_PATH = POST / "4404-Y5-R2FR-transition-cGamma-first-live-profile-row-or-parent-memory-nohair-proof.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4404_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

GATE_PATH = SCRIPT_DIR / "cGamma_profile_nohair_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4404_transition_cGamma_first_live_profile_row_or_parent_memory_nohair_proof.py"

NOHAIR_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4404_CGAMMA_MEMORY_NOHAIR_INPUT.csv"
NOHAIR_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4404_CGAMMA_MEMORY_NOHAIR_OUTPUT.csv"
PRODUCT_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4404_CGAMMA_PRODUCT_PROFILE_INPUT.csv"
PRODUCT_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4404_CGAMMA_PRODUCT_PROFILE_OUTPUT.csv"
AJ_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4404_CGAMMA_AJ_PRESSURE_INPUT.csv"
AJ_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4404_CGAMMA_AJ_PRESSURE_OUTPUT.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4403 = SOURCE_DIR / "P8_Y5_R2FR_4403_NEXT_TARGET.csv"
DERIVATIONS_4403 = SOURCE_DIR / "P8_Y5_R2FR_4403_LOCAL_RESIDUAL_DERIVATIONS.csv"
CLASSIFIER_4403 = SOURCE_DIR / "P8_Y5_R2FR_4403_LOCAL_RESIDUAL_CLASSIFIER_OUTPUT.csv"
CGAMMA_TARGETS_4279 = SOURCE_DIR / "P8_Y5_R2FR_4279_CGAMMA_FULL_BUDGET_TARGETS.csv"
BOUNDS_4287 = SOURCE_DIR / "P8_Y5_R2FR_4287_CGAMMA_PRODUCT_BOUNDS.csv"
PRESSURE_4338 = SOURCE_DIR / "P8_Y5_R2FR_4338_CGAMMA_PRESSURE_ROWS.csv"
FORMAL_202 = FORMAL / "202-PPC4161-same-coframe-source-memory-zero-law.md"
FORMAL_204 = FORMAL / "204-PPC4161-finite-cGamma-product-bound-law.md"
FORMAL_251 = FORMAL / "251-PPC4161-cGamma-support-nohair-or-full-budget-profile-bound-runner.md"
FORMAL_252 = FORMAL / "252-PPC4161-cGamma-parent-memory-equation-or-AJ-coefficient-source-fill.md"
FORMAL_296 = FORMAL / "296-PPC4161-cGamma-parent-memory-equation-AJ-source-coefficient-or-profile-fill.md"
FORMAL_297 = FORMAL / "297-PPC4161-cGamma-transport-Bgrad-routing-zero-or-profile-source-pack.md"
FORMAL_303 = FORMAL / "303-PPC4161-cGamma-AJ-real-profile-or-parent-coefficient-derivation.md"
FORMAL_354 = FORMAL / "354-PPC4161-cGamma-transition-source-kernel-coefficient-fill-or-metric-null-proof.md"

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4404_0_4403_next": (NEXT_4403, "4404-Y5-R2FR-transition-cGamma-first-live-profile-row-or-parent-memory-nohair-proof.md", "4403 handoff to cGamma no-hair/profile work."),
    "SRC4404_1_4403_survivor": (DERIVATIONS_4403, "LCR4403_3_survivor_priority", "4403 cGamma survivor priority."),
    "SRC4404_2_4403_classifier": (CLASSIFIER_4403, "LRC4403_5_cGamma", "4403 retained cGamma classifier output."),
    "SRC4404_3_4279_targets": (CGAMMA_TARGETS_4279, "CGT4279_0_Gdot", "4279 product bounds for cGamma channels."),
    "SRC4404_4_4287_bounds": (BOUNDS_4287, "CPB4287_6_vector", "4287 strict product bounds."),
    "SRC4404_5_4338_pressure": (PRESSURE_4338, "PRS4338_0_finite_margin_collar", "4338 finite-margin AJ pressure rows."),
    "SRC4404_6_202_memory": (FORMAL_202, "c_Gamma_parent_zero = false", "202 memory support still open."),
    "SRC4404_7_204_product": (FORMAL_204, "|c_Gamma * profile_a|", "204 finite cGamma product law."),
    "SRC4404_8_251_nohair": (FORMAL_251, "D_t Xi_0 = 0", "251 no-hair/profile gaps."),
    "SRC4404_9_252_AJ": (FORMAL_252, "A_J,eff_private = A_src + A_lap + A_drift", "252 AJ coefficient ledger."),
    "SRC4404_10_296_AJ_reduction": (FORMAL_296, "A_src = 0", "296 AJ reduction to transport/Bgrad leakage."),
    "SRC4404_11_297_collar": (FORMAL_297, "R_transport_to_local[W_loc] = 0", "297 finite-margin collar zero theorem."),
    "SRC4404_12_303_pressure": (FORMAL_303, "T_res/tau_L >= A_J,eff_private", "303 calculator-ready pressure law."),
    "SRC4404_13_354_transition": (FORMAL_354, "PLEAK4338_2", "354 transition-shell leak split."),
    "SRC4404_14_gate": (GATE_PATH, "def evaluate_aj_rows", "New cGamma no-hair/product/AJ gate."),
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    write_text(path, text + block)


def append_claim_once(path: Path, claim_id: str, row: List[str]) -> None:
    text = read_text(path)
    if f"\n{claim_id}," in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
        write_text(path, text)
    with path.open("a", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerow(row)


def source_register_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(text and needle in text)),
                "valid_for_claim": "False",
            }
        )
    return rows


def derivation_rows() -> List[Dict[str, str]]:
    return [
        {
            "derivation_id": "CG4404_0_memory_nohair_energy_identity",
            "statement": "A true c_Gamma no-hair proof needs a signed dissipative memory equation whose homogeneous compact-collar solution has D_t Xi_0=0, grad_perp Xi_0=0, and no vector/alpha3 profile.",
            "derivation": "For a local scalar memory normal form D_t Xi_0 + mu_Xi Xi_0 - D_Xi Delta_h Xi_0 = S_Xi plus no-flux/anchored zero-mode data, multiply by Xi_0 and integrate. If mu_Xi>0, D_Xi>=0, S_Xi=0, boundary flux is zero, and the zero mode is fixed, the energy identity forces Xi_0=0 or constant; then D_t Xi_0 and grad_perp Xi_0 vanish. Without the signed parent equation and source silence, the proof is conditional only.",
            "new_information": "The no-hair route is exact in form but still lacks parent equation/source-silence authority.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "CG4404_1_product_profile_contract",
            "statement": "If no-hair fails, every c_Gamma channel is a product row C_Gamma,a = |c_Gamma| |profile_a| that must beat its own arena bound.",
            "derivation": "Use the 204/4279 product law. The strict product channels retained here are Gdot, PPN_xi, alpha3/vector, WEP, clocks, stress and R10. Product rows are not bounds on c_Gamma alone unless the profile is independently sourced.",
            "new_information": "The profile route is executable without pretending c_Gamma itself has been measured or derived.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "CG4404_2_AJ_pressure_law",
            "statement": "The c_Gamma AJ pressure route is controlled by T_res/tau_L >= A_J,eff |c_Gamma|/(0.167893843691 Pi_B).",
            "derivation": "4280 reduces A_J,eff to transport/B-gradient leakage; 4281/4338 prove A_J,eff=0 in finite-margin compact collars. In transition shells, the 4287 pressure law gives the exact relaxation requirement. No cross-channel cancellation is credited.",
            "new_information": "We have one useful source-backed conditional row: finite-margin compact collars quiet the AJ channel; transition shells remain the live profile problem.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "CG4404_3_next_reduction",
            "statement": "After this split, the next c_Gamma target is not global c_Gamma smallness; it is the transition-shell leak vector P_leak.",
            "derivation": "4338 already reduces the transition source kernel to P_leak components. The finite-margin collar is quiet, so the remaining non-circling work is to zero or source the first transition components rather than re-auditing c_Gamma generally.",
            "new_information": "The next target becomes P_nonHilbert_action_domain and P_off_worldtube_readout_order, not another generic c_Gamma pass.",
            "valid_for_claim": "False",
        },
    ]


def nohair_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "candidate_id": "NH4404_0_full_parent_nohair_template",
            "route": "parent_memory_nohair_for_Xi0",
            "parent_memory_equation_signed": "False",
            "positive_relaxation_operator": "True",
            "source_terms_zero_or_boundary_routed": "False",
            "static_tau_branch": "True",
            "spatial_gradient_source_absent": "False",
            "transition_shell_excluded_or_projected": "False",
            "zero_mode_fixed": "True",
            "same_tau_coframe_support": "True",
            "D_t_Xi_zero": "False",
            "grad_perp_Xi_zero": "False",
            "alpha3_profile_zero": "False",
            "parent_authority": "MISSING_PARENT_SIGNED_MEMORY_EQUATION",
            "source_path": str(FORMAL_251),
            "input_valid_for_claim": "False",
            "notes": "Exact energy-identity shape exists, but parent equation/source silence are unsigned.",
        },
        {
            "candidate_id": "NH4404_1_finite_margin_AJ_only_not_full_nohair",
            "route": "finite_margin_compact_collar_AJ_zero",
            "parent_memory_equation_signed": "False",
            "positive_relaxation_operator": "False",
            "source_terms_zero_or_boundary_routed": "True",
            "static_tau_branch": "True",
            "spatial_gradient_source_absent": "False",
            "transition_shell_excluded_or_projected": "True",
            "zero_mode_fixed": "False",
            "same_tau_coframe_support": "True",
            "D_t_Xi_zero": "False",
            "grad_perp_Xi_zero": "False",
            "alpha3_profile_zero": "False",
            "parent_authority": "CONDITIONAL_AJ_CHANNEL_ONLY_NOT_FULL_NOHAIR",
            "source_path": str(FORMAL_354),
            "input_valid_for_claim": "False",
            "notes": "Useful AJ-channel zero in finite-margin collars, but not full cGamma no-hair.",
        },
    ]


def product_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "profile_id": "PROD4404_0_missing_live_Gdot_profile",
            "channel": "Gdot_over_G",
            "cGamma_abs": "MISSING_CGAMMA",
            "profile_abs": "MISSING_Dt_Xi0",
            "bound_value": "2.42e-14",
            "units": "yr^-1",
            "source_path": "MISSING_SOURCE_PATH",
            "support_certificate_path": "MISSING_SUPPORT_CERTIFICATE",
            "input_valid_for_claim": "False",
            "notes": "Live Gdot profile still missing.",
        },
        {
            "profile_id": "PROD4404_1_nohair_zero_Gdot_smoke_nonclaim",
            "channel": "Gdot_over_G",
            "cGamma_abs": "1",
            "profile_abs": "0",
            "bound_value": "2.42e-14",
            "units": "yr^-1",
            "source_path": str(GENERATOR_PATH),
            "support_certificate_path": str(GENERATOR_PATH),
            "input_valid_for_claim": "False",
            "notes": "Arithmetic row: no-hair would zero Gdot product.",
        },
        {
            "profile_id": "PROD4404_2_small_xi_profile_nonclaim",
            "channel": "PPN_xi",
            "cGamma_abs": "1",
            "profile_abs": "1e-10",
            "bound_value": "4e-9",
            "units": "dimensionless",
            "source_path": str(GENERATOR_PATH),
            "support_certificate_path": str(GENERATOR_PATH),
            "input_valid_for_claim": "False",
            "notes": "Nonclaim smoke row below xi bound.",
        },
        {
            "profile_id": "PROD4404_3_alpha3_vector_fail_nonclaim",
            "channel": "alpha3_vector",
            "cGamma_abs": "1",
            "profile_abs": "1e-19",
            "bound_value": "4e-20",
            "units": "dimensionless",
            "source_path": str(GENERATOR_PATH),
            "support_certificate_path": str(GENERATOR_PATH),
            "input_valid_for_claim": "False",
            "notes": "Nonclaim smoke row showing alpha3/vector is the brutal channel.",
        },
    ]


def aj_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "pressure_id": "AJ4404_0_missing_live_transition_profile",
            "branch": "raw_transition_live_profile",
            "A_J_eff_abs": "MISSING_AJ",
            "cGamma_abs": "MISSING_CGAMMA",
            "Pi_B": "MISSING_PIB",
            "T_res_over_tauL": "MISSING_TRES",
            "source_path": "MISSING_SOURCE_PATH",
            "support_certificate_path": "MISSING_SUPPORT_CERTIFICATE",
            "input_valid_for_claim": "False",
            "notes": "Live transition-shell AJ profile still missing.",
        },
        {
            "pressure_id": "AJ4404_1_finite_margin_collar_AJ_zero_nonclaim",
            "branch": "finite_margin_compact_collar",
            "A_J_eff_abs": "0",
            "cGamma_abs": "1",
            "Pi_B": "1",
            "T_res_over_tauL": "0",
            "source_path": str(PRESSURE_4338),
            "support_certificate_path": str(FORMAL_354),
            "input_valid_for_claim": "False",
            "notes": "Source-backed conditional AJ zero branch from 4338; nonclaim/private collar only.",
        },
        {
            "pressure_id": "AJ4404_2_raw_transition_strong_window_pass_nonclaim",
            "branch": "raw_transition_default_strong_window",
            "A_J_eff_abs": "1",
            "cGamma_abs": "1",
            "Pi_B": "1",
            "T_res_over_tauL": "5.95614453762",
            "source_path": str(PRESSURE_4338),
            "support_certificate_path": str(FORMAL_303),
            "input_valid_for_claim": "False",
            "notes": "Nonclaim row matching the 4287/4338 strong-window requirement.",
        },
        {
            "pressure_id": "AJ4404_3_raw_transition_underpowered_fail_nonclaim",
            "branch": "raw_transition_underpowered",
            "A_J_eff_abs": "1",
            "cGamma_abs": "1",
            "Pi_B": "1",
            "T_res_over_tauL": "1",
            "source_path": str(PRESSURE_4338),
            "support_certificate_path": str(FORMAL_303),
            "input_valid_for_claim": "False",
            "notes": "Nonclaim row showing ordinary T_res/tau_L=1 is not enough for A_J=1,cGamma=1.",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    gates = {
        "memory_nohair": "full D_t Xi_0/grad/alpha3 no-hair needs parent memory equation and source silence",
        "product_profiles": "product runner exists, but live cGamma/profile rows are missing",
        "AJ_pressure": "finite-margin AJ zero is useful but private/conditional; transition shell profile remains live",
        "local_residual_vector": "cGamma remains a retained survivor in E_res until no-hair or live profile passes",
        "local_GR_Newton_PPN": "local claims remain blocked until cGamma and other survivor residuals are zeroed or bounded",
    }
    return [
        {
            "gate_id": f"CG4404_{index}_{arena}",
            "arena": arena,
            "claim_allowed": "False",
            "reason": reason,
            "valid_for_claim": "False",
        }
        for index, (arena, reason) in enumerate(gates.items())
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4404_0",
            "decision": DECISION,
            "summary": "4404 splits c_Gamma into three executable lanes. Full memory no-hair has a clean energy-identity route but remains parent-unsigned. Product bounds for Gdot, xi and alpha3 now run as explicit |c_Gamma| profile rows; alpha3 is exposed as a very strict channel. The AJ pressure law imports a useful source-backed conditional result: finite-margin compact collars have A_J,eff=0, while raw transition shells require T_res/tau_L >= A_J,eff |c_Gamma|/(0.167893843691 Pi_B). The next target should not re-audit c_Gamma generally; it should attack the transition-shell P_leak components.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": DECISION,
            "timestamp_utc": STAMP,
            "summary": "cGamma split into no-hair/product/AJ lanes; finite-margin AJ zero imported; transition P_leak selected.",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4404_0",
            "target": NEXT_TARGET,
            "question": "Can the first two transition-shell P_leak components be parent-zeroed, or must they become source-backed profile-bound rows?",
            "preferred_route": "prove P_nonHilbert_action_domain q_tr=0 and P_off_worldtube_readout_order q_tr=0 from Hilbert/source-domain/worldtube ownership.",
            "fallback_route": "build finite source-backed leak-bound rows for P_nonHilbert_action_domain and P_off_worldtube_readout_order before scoring PPN/R10/clock/orbital channels.",
            "avoid": "reopening generic cGamma when the live obstruction is now the transition-shell leak vector.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(sources, derivations, nohair_output, product_output, aj_output, gates, decisions, next_targets) -> None:
    text = f"""# 420 PPC4161 transition: cGamma first live profile row or parent memory nohair proof

Marker: `{MARKER}`

## Result

4404 splits `c_Gamma` into three executable lanes:

1. full parent memory no-hair;
2. product-profile rows `C_Gamma,a = |c_Gamma| |profile_a|`;
3. AJ/transition pressure rows.

The useful win is narrow but real: the finite-margin compact collar branch has `A_J,eff_private=0`, so the AJ channel is quiet there. The raw transition shell remains the live problem.

## Source Register

| source | exists | needle found | role |
|---|---:|---:|---|
"""
    for row in sources:
        text += f"| `{row['source_id']}` | {row['path_exists']} | {row['needle_found']} | {row['role']} |\n"

    text += "\n## Derivation\n\n"
    for row in derivations:
        text += f"### {row['derivation_id']}\n\n- Statement: {row['statement']}\n- Derivation: {row['derivation']}\n- New information: {row['new_information']}\n\n"

    text += "\n## Memory No-Hair Gate\n\n"
    for row in nohair_output:
        text += f"- `{row['candidate_id']}`: equation_ready=`{row['equation_ready']}`, source_silence_ready=`{row['source_silence_ready']}`, observable_zero_ready=`{row['observable_zero_ready']}`, certificate_ready=`{row['nohair_certificate_ready']}`, status=`{row['current_status']}`.\n"

    text += "\n## Product Profile Runner\n\n"
    for row in product_output:
        text += f"- `{row['profile_id']}`: channel=`{row['channel']}`, product=`{row['product_value']}`, bound=`{row['bound_value']}`, within=`{row['product_within_bound']}`, status=`{row['current_status']}`.\n"

    text += "\n## AJ Pressure Runner\n\n"
    text += "`T_res/tau_L >= A_J,eff |c_Gamma|/(0.167893843691 Pi_B)`\n\n"
    for row in aj_output:
        text += f"- `{row['pressure_id']}`: A_J=`{row['A_J_eff_abs']}`, Pi_B=`{row['Pi_B']}`, T_res/tau_L=`{row['T_res_over_tauL']}`, required=`{row['required_T_res_over_tauL']}`, pass=`{row['pressure_pass']}`, status=`{row['current_status']}`.\n"

    text += "\n## Claim Gates\n\n"
    for row in gates:
        text += f"- `{row['arena']}`: claim_allowed=`{row['claim_allowed']}` because {row['reason']}.\n"

    text += "\n## Decision\n\n"
    text += f"{decisions[0]['summary']}\n\n"
    text += "## Next Target\n\n"
    text += f"- `{next_targets[0]['target']}`: {next_targets[0]['question']}\n"
    write_text(FORMAL_PATH, text)


def write_post_doc(decisions, next_targets) -> None:
    write_text(
        DOC_PATH,
        f"""# 4404 Y5 R2FR: cGamma first live profile row or parent memory nohair proof

Marker: `{MARKER}`

## Private checkpoint

{decisions[0]['summary']}

## Next

{next_targets[0]['target']}

{next_targets[0]['question']}
""",
    )


def write_spine_update() -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4404 local spine update: cGamma split into no-hair, product, and AJ lanes

Marker: `{MARKER}`

Spine update: `c_Gamma` is no longer a generic fog term. Full memory no-hair needs a parent-signed relaxation equation and source silence. Product channels are explicit `|c_Gamma| |profile_a|` rows. The AJ channel is quiet in finite-margin compact collars, while transition shells reduce to the P_leak vector.
""",
    )


def write_packet_update() -> None:
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4404 packet update: cGamma profile/no-hair gate

Marker: `{PACKET_MARKER}`

Packet update: 4404 adds executable cGamma no-hair, product-profile and AJ pressure gates and routes the next work to transition-shell P_leak.
""",
    )


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4404 splits c_Gamma into three executable lanes: full parent memory no-hair, product-profile rows C_Gamma,a=|c_Gamma||profile_a|, and AJ/transition pressure rows. The finite-margin compact collar branch imports a useful conditional result A_J,eff=0, but full memory no-hair remains parent-unsigned and transition shells still require P_leak zero proofs or source-backed profile bounds. No local-GR/Newton/PPN/R10/clock/orbital claim fires.",
            "4404 source register, cGamma derivations, memory no-hair gate, product profile runner, AJ pressure runner, claim gates, decision, status, next target and validation CSV.",
            "cGamma_nohair_product_AJ_lanes_ready_finite_margin_AJ_zero_nonclaim",
            "Attack transition-shell P_leak first two components or source profile-bound rows.",
            "Calling finite-margin AJ zero full cGamma no-hair, treating product bounds as cGamma values, or reopening generic cGamma instead of P_leak.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4404_SOURCE_REGISTER.csv")
    derivations = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4404_CGAMMA_DERIVATIONS.csv")
    nohair_output = read_csv(NOHAIR_OUTPUT_PATH)
    product_output = read_csv(PRODUCT_OUTPUT_PATH)
    aj_output = read_csv(AJ_OUTPUT_PATH)
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4404_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": str(bool(passed)), "detail": detail})

    add("VAL4404_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source exists")
    add("VAL4404_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited needle resolves")
    add("VAL4404_2_nohair_identity_written", any(row["derivation_id"] == "CG4404_0_memory_nohair_energy_identity" for row in derivations), "memory no-hair energy identity written")
    add("VAL4404_3_product_contract_written", any(row["derivation_id"] == "CG4404_1_product_profile_contract" for row in derivations), "product profile contract written")
    add("VAL4404_4_AJ_law_written", any(row["derivation_id"] == "CG4404_2_AJ_pressure_law" for row in derivations), "AJ pressure law written")
    add("VAL4404_5_nohair_nonclaim", all(row["valid_for_claim"] == "False" for row in nohair_output), "no-hair rows remain nonclaim")
    add("VAL4404_6_nohair_template_blocked", any(row["candidate_id"] == "NH4404_0_full_parent_nohair_template" and row["current_status"] == "CGAMMA_MEMORY_NOHAIR_CERTIFICATE_BLOCKED" for row in nohair_output), "full no-hair template blocks")
    add("VAL4404_7_product_zero_computes", any(row["profile_id"] == "PROD4404_1_nohair_zero_Gdot_smoke_nonclaim" and row["product_value"] == "0" for row in product_output), "zero product computes")
    add("VAL4404_8_product_fail_detected", any(row["profile_id"] == "PROD4404_3_alpha3_vector_fail_nonclaim" and row["current_status"] == "CGAMMA_PRODUCT_BOUND_FAILS" for row in product_output), "alpha3 product fail detected")
    add("VAL4404_9_AJ_finite_margin_zero_passes", any(row["pressure_id"] == "AJ4404_1_finite_margin_collar_AJ_zero_nonclaim" and row["pressure_pass"] == "True" for row in aj_output), "finite-margin AJ zero row passes arithmetic")
    add("VAL4404_10_AJ_underpowered_fails", any(row["pressure_id"] == "AJ4404_3_raw_transition_underpowered_fail_nonclaim" and row["current_status"] == "CGAMMA_AJ_PRESSURE_BOUND_FAILS" for row in aj_output), "underpowered transition fails")
    add("VAL4404_11_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4404_12_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4404_13_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4404_14_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4404_15_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4404_16_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add("VAL4404_17_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4404_18_rows_nonclaim", all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path)), "generated rows remain nonclaim")
    add("VAL4404_19_gate_script_exists", GATE_PATH.exists() and "def evaluate_aj_rows" in read_text(GATE_PATH), "cGamma profile gate exists")
    add("VAL4404_20_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generator cleanup")
    return validations


def remove_pycache() -> None:
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    sources = source_register_rows()
    derivations = derivation_rows()
    nohair_inputs = nohair_input_rows()
    product_inputs = product_input_rows()
    aj_inputs = aj_input_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_paths: List[Path] = [NOHAIR_INPUT_PATH, PRODUCT_INPUT_PATH, AJ_INPUT_PATH]
    write_csv(NOHAIR_INPUT_PATH, nohair_inputs)
    nohair_output = evaluate_nohair_rows(NOHAIR_INPUT_PATH)
    write_csv(NOHAIR_OUTPUT_PATH, nohair_output)
    csv_paths.append(NOHAIR_OUTPUT_PATH)

    write_csv(PRODUCT_INPUT_PATH, product_inputs)
    product_output = evaluate_product_rows(PRODUCT_INPUT_PATH)
    write_csv(PRODUCT_OUTPUT_PATH, product_output)
    csv_paths.append(PRODUCT_OUTPUT_PATH)

    write_csv(AJ_INPUT_PATH, aj_inputs)
    aj_output = evaluate_aj_rows(AJ_INPUT_PATH)
    write_csv(AJ_OUTPUT_PATH, aj_output)
    csv_paths.append(AJ_OUTPUT_PATH)

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4404_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4404_CGAMMA_DERIVATIONS.csv": derivations,
        "P8_Y5_R2FR_4404_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4404_DECISION.csv": decisions,
        "P8_Y5_R2FR_4404_STATUS.csv": statuses,
        "P8_Y5_R2FR_4404_NEXT_TARGET.csv": next_targets,
    }
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, derivations, nohair_output, product_output, aj_output, gates, decisions, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    remove_pycache()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
