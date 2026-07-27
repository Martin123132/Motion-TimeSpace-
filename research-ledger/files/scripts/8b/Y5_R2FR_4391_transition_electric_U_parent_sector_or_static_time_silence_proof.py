from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from static_time_silence_gate import evaluate_static_time_rows, read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4391"
CLAIM_ID = "L-232"
MARKER = "PPC4161_TRANSITION_ELECTRIC_U_PARENT_SECTOR_OR_STATIC_TIME_SILENCE_PROOF_4391"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_ELECTRIC_U_PARENT_SECTOR_OR_STATIC_TIME_SILENCE_PROOF_4391"
DECISION = "TAU_COFRAME_U_CANDIDATE_AND_STATIC_SILENCE_LEMMA_DERIVED_PARENT_SIGNATURES_OPEN_NONCLAIM"
NEXT_TARGET = "4392-Y5-R2FR-transition-sigmaS-residual-owner-or-electric-U-bound-row.md"

FORMAL_PATH = FORMAL / "407-PPC4161-transition-electric-U-parent-sector-or-static-time-silence-proof.md"
DOC_PATH = POST / "4391-Y5-R2FR-transition-electric-U-parent-sector-or-static-time-silence-proof.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4391_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
GATE_RUNNER_PATH = SCRIPT_DIR / "static_time_silence_gate.py"
GATE_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4391_STATIC_TIME_GATE_INPUT.csv"
GATE_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4391_STATIC_TIME_GATE_OUTPUT.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4391_0_4390_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4390_NEXT_TARGET.csv",
        "4391-Y5-R2FR-transition-electric-U-parent-sector-or-static-time-silence-proof.md",
        "Explicit 4391 handoff.",
    ),
    "SRC4391_1_4390_U": (
        SOURCE_DIR / "P8_Y5_R2FR_4390_U_CONSTRUCTION_THEOREMS.csv",
        "U4390_0_electric_projector_ansatz",
        "Electric U ansatz to be parent-owned.",
    ),
    "SRC4391_2_tau_audit": (
        SOURCE_DIR / "P8_Y5_R10_684_TAU_GENERATOR_AUDIT.csv",
        "TGA684_5_stationary_generator",
        "Tau generator audit and stationary blocker.",
    ),
    "SRC4391_3_tau_contract": (
        SOURCE_DIR / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
        "TGC685_1_Killing_stationary_route",
        "Killing/time-flow contract.",
    ),
    "SRC4391_4_coframe_contract": (
        SOURCE_DIR / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv",
        "CFC943_1_observed_coframe_descent",
        "Observed coframe descent contract.",
    ),
    "SRC4391_5_coframe_zero": (
        SOURCE_DIR / "P8_Y5_R10_863_COFRAME_ZERO_THEOREM.csv",
        "CZT863_0_chain_rule_zero",
        "Conditional coframe chain-rule zero.",
    ),
    "SRC4391_6_same_coframe": (
        SOURCE_DIR / "P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv",
        "UOC519_0_single_coframe_field",
        "Same observed coframe clause.",
    ),
    "SRC4391_7_observer_map": (
        POST / "10-observer-map-symplectic-contract.md",
        "theta_0 = T c dt",
        "Observer coframe and reciprocal-strain contract.",
    ),
    "SRC4391_8_boundary": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "J_tr^nu = 0 through <=2PN",
        "Private local boundary/no-flux selector.",
    ),
    "SRC4391_9_source": (
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "T_H^munu",
        "Same Hilbert source action and Ward target.",
    ),
    "SRC4391_10_gate_runner": (
        GATE_RUNNER_PATH,
        "REQUIRED_FIELDS",
        "Executable static/time-silence gate.",
    ),
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


def theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "UST4391_0_tau_coframe_u_candidate",
            "statement": "If the observed coframe and tau generator are parent-owned, the electric-U flow is not a new field: u^mu=tau_obs^mu/sqrt(-g_obs(tau_obs,tau_obs)).",
            "derivation": "The same-coframe stack already demands one e_obs for sources, clocks, photons, and orbits. Normalizing the same tau_obs with g_obs gives a unit timelike u tied to the observed clock/source frame rather than a fitted local vector.",
            "effect": "Identifies the correct MTS parent candidate for u^mu.",
            "status": "EXACT_CONDITIONAL_U_CANDIDATE_PARENT_TAU_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "UST4391_1_transverse_S_parent_sector_contract",
            "statement": "The minimal electric sector can use a symmetric tensor S^{mu nu} constrained by u_mu S^{mu nu}=0; equivalently S is a spatial tensor on the observed tau-slices.",
            "derivation": "With h_{mu nu}=g_{mu nu}+u_mu u_nu and D_mu=h_mu^alpha nabla_alpha, a parent S can be declared spatial by S^{mu nu}=h^mu_alpha h^nu_beta S^{alpha beta}. This preserves U^{0i0j}=S^{ij} in the local rest frame.",
            "effect": "Turns the vague missing U-owner into a precise u/S parent-sector signature.",
            "status": "PARENT_SECTOR_CONTRACT_WRITTEN_NOT_MTS_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "UST4391_2_static_time_silence_lemma",
            "statement": "In a parent static branch with L_tau g_obs=0, L_tau S^{mu nu}=0, hypersurface-static slicing, and bounded acceleration/curvature commutators, the leading electric-U pressure/aniso term proportional to nabla_tau nabla_tau S^{ij} vanishes.",
            "derivation": "Choose the local rest frame of u. The 4390 electric split leaves density as c^-2 partial_i partial_j S^{ij}. The dangerous leading ij term is the two-time-derivative slot. If S and the spatial projector are Lie-dragged by tau and the slice has no shift/extrinsic-time drift, partial_0 S^{ij}=0 and hence partial_0 partial_0 S^{ij}=0; only retained acceleration/curvature/boundary terms remain.",
            "effect": "This is the useful proof: the electric branch can avoid scalar-phiR same-order static pressure if the static parent clauses are real.",
            "status": "CONDITIONAL_STATIC_LEMMA_DERIVED_PAYLOAD_REMAINDERS_RETAINED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "UST4391_3_not_a_lapse_cheat",
            "statement": "The static branch cannot be signed by choosing a convenient time coordinate or lapse; tau must be the same source, Hamiltonian, clock, boundary, and orbital generator.",
            "derivation": "The 684/685 tau audit says homogeneous lapse or reparametrization is not evidence unless H_tau, clocks, and H_ref transform consistently. Therefore u^mu from tau only counts if the tau lock is parent-signed.",
            "effect": "Prevents smuggling time-silence through coordinates.",
            "status": "GUARDRAIL_RETAINED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "UST4391_4_remaining_owner",
            "statement": "The remaining hard object is the S-sector owner: S^{ij} must be tied before readout to rho_top-rho_H, not fitted to the density profile after the fact.",
            "derivation": "4390 killed scalar phiR and density-only adoption. 4391 supplies u and static-silence conditions, but the tensor S still needs a parent equation or residual identity.",
            "effect": "Next target becomes sigma/S residual ownership, not another broad source sweep.",
            "status": "S_OWNER_NEXT_TARGET",
            "valid_for_claim": "False",
        },
    ]


def parent_map_rows() -> List[Dict[str, str]]:
    return [
        {
            "object_id": "OBJ4391_0_u",
            "object": "u^mu",
            "candidate_definition": "tau_obs^mu/sqrt(-g_obs(tau_obs,tau_obs))",
            "source_basis": "same observed coframe plus tau generator stack",
            "closed_by_current_math": "formula only",
            "parent_signature_needed": "coframe descent + tau generator/clock/Hamiltonian lock",
            "current_status": "CANDIDATE_DERIVED_PARENT_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "object_id": "OBJ4391_1_h",
            "object": "h_mu_nu",
            "candidate_definition": "g_obs_mu_nu + u_mu u_nu",
            "source_basis": "observed metric/coframe and u",
            "closed_by_current_math": "conditional on u",
            "parent_signature_needed": "same coframe and tau normalization",
            "current_status": "CONDITIONAL",
            "valid_for_claim": "False",
        },
        {
            "object_id": "OBJ4391_2_S",
            "object": "S^{mu nu}",
            "candidate_definition": "parent spatial symmetric tensor with u_mu S^{mu nu}=0; optional scalar-potential construction S=D^{(mu}D^{nu)}sigma_S + trace-controlled term",
            "source_basis": "must be MTS residual-owner sector, not a post-readout fit",
            "closed_by_current_math": "tensor contract only",
            "parent_signature_needed": "S equation/owner tying c^-2 nabla_i nabla_j S^{ij} to rho_top-rho_H",
            "current_status": "OWNER_MISSING",
            "valid_for_claim": "False",
        },
        {
            "object_id": "OBJ4391_3_U",
            "object": "U^{mu alpha nu beta}",
            "candidate_definition": "electric projector from u and S",
            "source_basis": "4390 ansatz",
            "closed_by_current_math": "Riemann symmetries and rest-frame slot",
            "parent_signature_needed": "u/S parent action, Ward identity, boundary and curvature clauses",
            "current_status": "ALGEBRA_READY_PARENT_UNSIGNED",
            "valid_for_claim": "False",
        },
    ]


def gate_input_rows() -> List[Dict[str, str]]:
    script_path = str(Path(__file__).resolve())
    return [
        {
            "candidate_id": "ST4391_0_tau_coframe_formula",
            "branch": "formula_only_u_from_tau",
            "u_from_tau_coframe_formula": "True",
            "coframe_descent_signed": "False",
            "tau_generator_signed": "False",
            "tau_killing_signed": "False",
            "s_tensor_parent_owned": "False",
            "lie_tau_s_signed": "False",
            "hypersurface_static_signed": "False",
            "acceleration_shift_zero_or_bounded": "False",
            "curvature_commutator_zero_or_bounded": "False",
            "ward_conservation_owned": "False",
            "boundary_flux_silent": "False",
            "source_path": script_path,
        },
        {
            "candidate_id": "ST4391_1_private_selector_boundary_help",
            "branch": "PPC4161_private_selector",
            "u_from_tau_coframe_formula": "True",
            "coframe_descent_signed": "False",
            "tau_generator_signed": "False",
            "tau_killing_signed": "False",
            "s_tensor_parent_owned": "False",
            "lie_tau_s_signed": "False",
            "hypersurface_static_signed": "False",
            "acceleration_shift_zero_or_bounded": "False",
            "curvature_commutator_zero_or_bounded": "False",
            "ward_conservation_owned": "False",
            "boundary_flux_silent": "True",
            "source_path": str(FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md"),
        },
        {
            "candidate_id": "ST4391_2_ideal_static_certificate_template",
            "branch": "ideal_required_parent_certificate",
            "u_from_tau_coframe_formula": "True",
            "coframe_descent_signed": "False",
            "tau_generator_signed": "False",
            "tau_killing_signed": "False",
            "s_tensor_parent_owned": "False",
            "lie_tau_s_signed": "False",
            "hypersurface_static_signed": "False",
            "acceleration_shift_zero_or_bounded": "False",
            "curvature_commutator_zero_or_bounded": "False",
            "ward_conservation_owned": "False",
            "boundary_flux_silent": "False",
            "source_path": script_path,
        },
    ]


def remaining_bound_rows() -> List[Dict[str, str]]:
    return [
        {
            "bound_id": "REM4391_0_tau_lock",
            "quantity": "tau_source=tau_charge=tau_clock=tau_boundary=tau_orbit=tau_obs",
            "why_needed": "without one tau, u^mu is a frame choice rather than parent physics",
            "source_path": "MISSING_PARENT_SIGNED_TAU_LOCK",
            "status": "PROOF_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "REM4391_1_S_owner",
            "quantity": "rho_top-rho_H - c^-2 D_i D_j S^{ij}",
            "why_needed": "ties S to the live topological/Hilbert residual before readout",
            "source_path": "MISSING_S_RESIDUAL_OWNER_IDENTITY",
            "status": "PROOF_OR_PROFILE_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "REM4391_2_static_silence",
            "quantity": "L_tau S^{ij}, L_tau g_obs, K_ij, shift/acceleration residues",
            "why_needed": "kills leading ij pressure/aniso from the electric U branch",
            "source_path": "MISSING_STATIC_TIME_SILENCE_CERTIFICATE",
            "status": "PROOF_OR_BOUND_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "REM4391_3_curvature_payload",
            "quantity": "commutator/algebraic U*R terms",
            "why_needed": "retained after the static flat-leading proof",
            "source_path": "MISSING_CURVATURE_PAYLOAD_BOUND",
            "status": "PROOF_OR_BOUND_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "REM4391_4_Ward_payload",
            "quantity": "nabla_mu Delta T_U^{mu nu}",
            "why_needed": "fixed/external S would violate Bianchi consistency",
            "source_path": "MISSING_U_SECTOR_WARD_IDENTITY",
            "status": "PROOF_OR_EXCHANGE_CURRENT_REQUIRED",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    reasons = {
        "local_GR": "u candidate and static lemma are conditional; S owner and Ward/curvature gates remain open",
        "newtonian_limit": "density operator still lacks parent residual identity",
        "PPN": "pressure/aniso silence requires parent-signed static S branch",
        "clock": "tau generator/clock normalization is not parent-signed",
        "EM_Maxwell": "same coframe helps but U sector must not double count Maxwell-Hodge stress",
        "R10_WEP": "source coupling coefficients remain dependent on tau/coframe/S owner signatures",
    }
    return [
        {
            "gate_id": f"CG4391_{index}_{arena}",
            "arena": arena,
            "claim_allowed": "False",
            "reason": reason,
            "valid_for_claim": "False",
        }
        for index, (arena, reason) in enumerate(reasons.items())
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4391_0",
            "decision": DECISION,
            "summary": "4391 derives the parent candidate u^mu from the same tau/coframe stack and proves the conditional static-time-silence lemma for the electric U branch. This is genuine progress, but current sources still do not parent-sign tau, S ownership, Killing/static silence, curvature, or Ward clauses.",
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
            "summary": "u is now identified as normalized tau_obs from e_obs; scalar phiR stays demoted; the next hard object is S/sigma residual ownership plus static tau silence.",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4391_0",
            "target": NEXT_TARGET,
            "question": "Can the parent MTS residual sector supply S^{ij} itself, with c^-2 D_iD_j S^{ij}=rho_top-rho_H before readout?",
            "preferred_route": "derive S or sigma_S from the topological/Hilbert residual owner, then combine it with the static tau/coframe conditions.",
            "fallback_route": "fill electric-U bound rows for S residual mismatch, time-silence leakage, curvature payload, Ward exchange, and boundary flux.",
            "avoid": "introducing S as a fitted post-readout tensor or reviving scalar phiR as a local-GR pass.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    theorems: List[Dict[str, str]],
    parent_map: List[Dict[str, str]],
    gate_output: List[Dict[str, str]],
    remaining: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# 407 PPC4161 transition: electric U parent sector or static-time silence proof

Marker: `{MARKER}`

## Result

4391 proves the useful conditional step:

`u^mu = tau_obs^mu / sqrt(-g_obs(tau_obs,tau_obs))`

is the right MTS candidate for the electric-U flow, provided the same observed coframe and tau generator are parent-signed.

For `U[u,S]`, the local static branch gives:

`Delta rho ~ c^-2 D_i D_j S^{{ij}}`,

while the leading electric-U pressure/aniso time slot vanishes if:

`L_tau g_obs = 0`, `L_tau S^{{ij}} = 0`, hypersurface-static slicing holds, and acceleration/curvature commutators are zero or bounded.

So this route is not dead and not just a ledger. The real remaining problem is now sharply located: parent-own `S^{{ij}}` and the tau/static certificates.

## Source Register

| source | exists | needle found | role |
|---|---:|---:|---|
"""
    for row in sources:
        text += f"| `{row['source_id']}` | {row['path_exists']} | {row['needle_found']} | {row['role']} |\n"
    text += "\n## Theorem Rows\n\n"
    for row in theorems:
        text += f"### {row['theorem_id']}\n\n- Statement: {row['statement']}\n- Derivation: {row['derivation']}\n- Status: `{row['status']}`\n\n"
    text += "## Parent Object Map\n\n"
    for row in parent_map:
        text += f"- `{row['object']}`: {row['candidate_definition']} — status `{row['current_status']}`.\n"
    text += "\n## Static-Time Gate\n\n"
    for row in gate_output:
        text += f"- `{row['candidate_id']}`: pass=`{row['static_time_pass']}`, leading_time_pressure_zero=`{row['leading_time_pressure_zero']}`, closed `{row['closed_clause_count']}/{row['total_clause_count']}`, failed `{row['failed_clauses']}`.\n"
    text += "\n## Remaining Bound/Proof Rows\n\n"
    for row in remaining:
        text += f"- `{row['bound_id']}`: `{row['quantity']}` — {row['why_needed']}.\n"
    text += "\n## Claim Gates\n\n"
    for row in gates:
        text += f"- `{row['arena']}`: claim_allowed=`{row['claim_allowed']}` because {row['reason']}.\n"
    text += "\n## Decision\n\n"
    text += f"{decisions[0]['summary']}\n\n"
    text += "## Next Target\n\n"
    text += f"- `{next_targets[0]['target']}`: {next_targets[0]['question']}\n"
    write_text(FORMAL_PATH, text)


def write_post_doc(decisions: List[Dict[str, str]], next_targets: List[Dict[str, str]]) -> None:
    write_text(
        DOC_PATH,
        f"""# 4391 Y5 R2FR: electric U parent sector or static-time silence proof

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
## 4391 local spine update: tau/coframe electric-U parent route

Marker: `{MARKER}`

Spine update: the electric-U route now has an MTS-native flow candidate, `u^mu=tau_obs^mu/sqrt(-g_obs(tau_obs,tau_obs))`, from the same observed coframe/tau stack. A conditional static-time-silence lemma shows the leading `Delta T^ij_U` time-derivative pressure slot vanishes when `L_tau g_obs=0`, `L_tau S=0`, hypersurface-static slicing, and bounded curvature/acceleration clauses are signed. The route remains nonclaim because tau lock, S residual ownership, Ward conservation, curvature, and boundary certificates are still open.
""",
    )


def write_packet_update() -> None:
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4391 packet update: static-time silence lemma

Marker: `{PACKET_MARKER}`

Packet update: 4391 makes the electric-U branch sharper. The parent flow should be normalized observed tau, not a new fitted vector. If the parent signs static tau/coframe and `L_tau S=0`, then the electric branch can keep `c^-2 D_iD_jS^ij` as density while killing the leading two-time-derivative pressure/aniso slot. Current corpus does not yet sign tau, S owner, or Ward/curvature clauses; next target is the S/sigma residual owner.
""",
    )


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4391 derives the MTS-native parent-flow candidate for the electric-U route: u^mu=tau_obs^mu/sqrt(-g_obs(tau_obs,tau_obs)) from the same observed coframe/tau stack. It also proves the conditional static-time-silence lemma: if L_tau g_obs=0, L_tau S^{ij}=0, hypersurface-static slicing holds, and acceleration/curvature commutators are zero or bounded, then the leading electric-U pressure/aniso term from nabla_tau nabla_tau S^{ij} vanishes while the density term c^-2 D_iD_j S^{ij} remains. This is a construction advance, not a local-GR/Newton/PPN/clock/orbital/R10 claim, because tau lock, S residual ownership, Ward conservation, curvature, and boundary certificates remain unsigned.",
            "4391 source register, parent U/S theorem rows, parent object map, static-time gate input/output, remaining proof/bound rows, claim gates, decision, status, next target and validation CSV.",
            "tau_coframe_u_candidate_static_silence_lemma_derived_S_owner_unsigned_nonclaim",
            "Derive the S/sigma residual owner identity c^-2 D_iD_jS^{ij}=rho_top-rho_H before readout, or fill electric-U bound rows for residual mismatch, time leakage, curvature, Ward exchange and boundary flux.",
            "Treating tau as a coordinate choice, fitting S^{ij} after readout, reviving scalar phiR, or claiming pressure silence without static parent signatures.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4391_SOURCE_REGISTER.csv")
    theorems = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4391_PARENT_U_S_THEOREMS.csv")
    parent_map = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4391_PARENT_OBJECT_MAP.csv")
    gate_output = read_csv(GATE_OUTPUT_PATH)
    remaining = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4391_REMAINING_PROOF_BOUND_ROWS.csv")
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4391_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": str(bool(passed)), "detail": detail})

    add("VAL4391_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source exists")
    add("VAL4391_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited needle resolves")
    add("VAL4391_2_u_candidate", any(row["object"] == "u^mu" and "tau_obs" in row["candidate_definition"] for row in parent_map), "u candidate mapped to tau/coframe")
    add("VAL4391_3_static_lemma", any(row["theorem_id"] == "UST4391_2_static_time_silence_lemma" for row in theorems), "static-time lemma staged")
    add("VAL4391_4_gate_fails_closed", all(row["static_time_pass"] == "False" and row["valid_for_claim"] == "False" for row in gate_output), "static-time candidates fail closed")
    add("VAL4391_5_remaining_rows_nonclaim", len(remaining) >= 5 and all(row["valid_for_claim"] == "False" and "MISSING" in row["source_path"] for row in remaining), "remaining proof/bound rows staged")
    add("VAL4391_6_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4391_7_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4391_8_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4391_9_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4391_10_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4391_11_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4391_12_rows_nonclaim",
        all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path))
        and all(row.get("claim_allowed", "False") == "False" for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add("VAL4391_13_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4391_14_runner_exists", GATE_RUNNER_PATH.exists() and "def evaluate_static_time_rows" in read_text(GATE_RUNNER_PATH), "static-time gate runner exists")
    return validations


def main() -> None:
    sources = source_register_rows()
    theorems = theorem_rows()
    parent_map = parent_map_rows()
    gate_inputs = gate_input_rows()
    remaining = remaining_bound_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4391_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4391_PARENT_U_S_THEOREMS.csv": theorems,
        "P8_Y5_R2FR_4391_PARENT_OBJECT_MAP.csv": parent_map,
        "P8_Y5_R2FR_4391_REMAINING_PROOF_BOUND_ROWS.csv": remaining,
        "P8_Y5_R2FR_4391_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4391_DECISION.csv": decisions,
        "P8_Y5_R2FR_4391_STATUS.csv": statuses,
        "P8_Y5_R2FR_4391_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = [GATE_INPUT_PATH]
    write_csv(GATE_INPUT_PATH, gate_inputs)
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    gate_output = evaluate_static_time_rows(GATE_INPUT_PATH)
    write_csv(GATE_OUTPUT_PATH, gate_output)
    csv_paths.append(GATE_OUTPUT_PATH)

    write_formal_doc(sources, theorems, parent_map, gate_output, remaining, gates, decisions, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
