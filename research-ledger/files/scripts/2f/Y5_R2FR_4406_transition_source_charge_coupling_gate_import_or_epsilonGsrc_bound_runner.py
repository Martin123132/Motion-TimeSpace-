from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from epsilon_Gsrc_bound_gate import (  # noqa: E402
    evaluate_eperp_bound_rows,
    evaluate_source_bridge_rows,
    read_csv,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4406"
CLAIM_ID = "L-247"
MARKER = "PPC4161_TRANSITION_SOURCE_CHARGE_COUPLING_GATE_IMPORT_OR_EPSILONGSRC_BOUND_RUNNER_4406"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_SOURCE_CHARGE_COUPLING_GATE_IMPORT_OR_EPSILONGSRC_BOUND_RUNNER_4406"
DECISION = "EPSILON_GSRC_SOURCE_BRIDGE_IMPORTED_EPERP_COMPONENT_BOUND_RUNNER_READY_PROFILE_OWNER_NEXT_NONCLAIM"
NEXT_TARGET = "4407-Y5-R2FR-transition-density-profile-owner-or-Eprofile-source-shadow-gate.md"

FORMAL_PATH = FORMAL / "422-PPC4161-transition-source-charge-coupling-gate-import-or-epsilonGsrc-bound-runner.md"
DOC_PATH = POST / "4406-Y5-R2FR-transition-source-charge-coupling-gate-import-or-epsilonGsrc-bound-runner.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4406_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
GATE_PATH = SCRIPT_DIR / "epsilon_Gsrc_bound_gate.py"

BRIDGE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4406_SOURCE_BRIDGE_INPUT.csv"
BRIDGE_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4406_SOURCE_BRIDGE_OUTPUT.csv"
EPERP_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4406_EPERP_BOUND_INPUT.csv"
EPERP_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4406_EPERP_BOUND_OUTPUT.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4405 = SOURCE_DIR / "P8_Y5_R2FR_4405_NEXT_TARGET.csv"
FORMAL_421 = FORMAL / "421-PPC4161-transition-cGamma-Pleak-first-two-components-or-profile-bound.md"
FORMAL_370 = FORMAL / "370-PPC4161-Htau-MHref-source-charge-owner-or-finite-GN-drift-bound.md"
FORMAL_385 = FORMAL / "385-PPC4161-transition-nonproduct-Csrc-source-normalization-row-or-owner-no-wA-activation.md"
FORMAL_386 = FORMAL / "386-PPC4161-transition-epsilon-Gsrc-coefficient-bound-or-Xi-owner-edge-proof.md"
FORMAL_387 = FORMAL / "387-PPC4161-transition-source-worldtube-support-bound-or-measure-owner-edge-proof.md"
FORMAL_388 = FORMAL / "388-PPC4161-transition-Eperp-envelope-decomposition-or-measure-owner-action-line-proof.md"
FORMAL_389 = FORMAL / "389-PPC4161-transition-first-Eperp-component-zero-or-bound-measure-source-mass.md"
FORMAL_390 = FORMAL / "390-PPC4161-transition-same-worldtube-source-mass-owner-or-Emass-bound.md"
FORMAL_392 = FORMAL / "392-PPC4161-transition-source-shadow-ban-or-Eprofile-first-source-density-row.md"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4406_00_4405_next": (NEXT_4405, "epsilon_Gsrc", "4405 routes the current chain to source charge/coupling."),
    "SRC4406_01_4405_formal": (FORMAL_421, "source charge/coupling", "4405 identifies source charge/coupling as the next gate."),
    "SRC4406_02_4354_bridge": (FORMAL_370, "D_A ln kappa_eff = 0", "4354 derives the structural source-blind calibrated coupling fork."),
    "SRC4406_03_4354_epsilon": (FORMAL_370, "epsilon_Gsrc <=", "4354 defines the no-cancellation source/coupling envelope."),
    "SRC4406_04_4369_projection": (FORMAL_385, "Pi_Gsrc^C = [0,0,0,1]", "4369 selects epsilon_Gsrc as the non-product source/coupling lane."),
    "SRC4406_05_4370_gate": (FORMAL_386, "K_N(s)=min((1-s)^-2, 2s(1-s)^-3)", "4370 derives the zero-monopole geometry coefficient gate."),
    "SRC4406_06_4371_geometry": (FORMAL_387, "SUP4371_2_Sun_Earth_average", "4371 supplies source-backed geometry examples."),
    "SRC4406_07_4372_decomposition": (FORMAL_388, "E_perp <= E_measure + E_mass + E_transition + E_Xi + E_T.", "4372 decomposes E_perp into named no-cancellation components."),
    "SRC4406_08_4373_components": (FORMAL_389, "E_mass := ||delta_m_perp||_inf.", "4373 attacks measure and mass components."),
    "SRC4406_09_4374_profile": (FORMAL_390, "rho_eff(y)=rho_H(y) on W_H", "4374 shows integrated mass is not enough; profile ownership is required."),
    "SRC4406_10_4376_shadow": (FORMAL_392, "same-action Hilbert derivative + typed no-source-shadow grammar", "4376 identifies source-shadow ban/distributional equality as the E_profile route."),
    "SRC4406_11_gate": (GATE_PATH, "def evaluate_eperp_bound_rows", "Executable epsilon_Gsrc bridge/bound gate."),
}


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def locate(path: Path, needle: str) -> Tuple[bool, int]:
    if not path.exists():
        return False, -1
    for line_number, line in enumerate(text(path).splitlines(), 1):
        if needle in line:
            return True, line_number
    return False, -1


def source_rows() -> List[Dict[str, object]]:
    rows = []
    for source_id, (path, needle, role) in SOURCES.items():
        found, line_number = locate(path, needle)
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": source_id,
            "path": str(path),
            "path_exists": path.exists(),
            "needle": needle,
            "needle_found": found,
            "line_number": line_number,
            "role": role,
            "valid_for_claim": False,
        })
    return rows


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "EG4406_0_structural_source_bridge",
            "object": "local GR/Newton source law",
            "statement": "If kappa_eff is source-blind and the Hamiltonian/Hilbert source charge is the same worldtube mass before readout, then the weak-field Poisson/Gauss/Newton law follows with calibrated G_cal.",
            "result": "This is a fair GR-like structural bridge; numeric G_N prediction is not required at this stage.",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "EG4406_1_monopole_subtraction",
            "object": "epsilon_Gsrc_perp",
            "statement": "The common Hilbert-source monopole is calibration-degenerate, so the physical source-shape residual is epsilon_Gsrc_perp = epsilon_Gsrc - epsilon_bar_H.",
            "result": "Finite Newton/source tests must score the noncommon profile component, not the calibrated common mode.",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "EG4406_2_component_bound",
            "object": "E_perp component runner",
            "statement": "E_perp <= E_measure + E_mass + E_transition + E_Xi + E_T, and |delta a|/|a_N| <= K_N(s) E_perp.",
            "result": "The finite branch is now executable as K_N(s)(component sum) <= delta_N.",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "EG4406_3_profile_owner_next",
            "object": "E_mass/E_profile",
            "statement": "Integrated source mass equality kills only the common monopole; E_mass=0 requires rho_eff(y)=rho_H(y) on the same worldtube before readout.",
            "result": "The next least-circular target is the E_profile/source-shadow parent grammar route, not another total-mass argument.",
            "valid_for_claim": False,
        },
    ]


def bridge_input_rows() -> List[Dict[str, object]]:
    base = {
        "source_blind_kappa_eff": False,
        "same_worldtube": False,
        "Htau_integrable": False,
        "Href_fixed": False,
        "same_tau_frame_surface": False,
        "boundary_flux_routed": False,
        "PiH_glue": False,
        "MHref_positive": False,
        "density_profile_owned": False,
        "public_authority": False,
        "input_valid_for_claim": False,
    }
    current = dict(base)
    current.update({
        "bridge_id": "SB4406_0_current_integrated_bridge_profile_open",
        "branch": "current_private_integrated_source_bridge",
        "source_path": str(FORMAL_390),
        "source_blind_kappa_eff": True,
        "same_worldtube": True,
        "Htau_integrable": True,
        "Href_fixed": True,
        "same_tau_frame_surface": True,
        "boundary_flux_routed": True,
        "PiH_glue": True,
        "MHref_positive": True,
        "density_profile_owned": False,
    })
    future = dict(base)
    future.update({
        "bridge_id": "SB4406_1_future_full_profile_clean_smoke",
        "branch": "future_same_worldtube_profile_owned_clean",
        "source_path": str(FORMAL_390),
        "source_blind_kappa_eff": True,
        "same_worldtube": True,
        "Htau_integrable": True,
        "Href_fixed": True,
        "same_tau_frame_surface": True,
        "boundary_flux_routed": True,
        "PiH_glue": True,
        "MHref_positive": True,
        "density_profile_owned": True,
    })
    public_open = dict(base)
    public_open.update({
        "bridge_id": "SB4406_2_public_or_raw_open_branch",
        "branch": "public_or_raw_transition_open",
        "source_path": str(FORMAL_370),
        "source_blind_kappa_eff": True,
        "same_worldtube": False,
        "Htau_integrable": False,
        "PiH_glue": True,
    })
    return [current, future, public_open]


def eperp_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "EG4406_0_missing_live_components",
            "arena": "Newton_source_normalization",
            "branch": "real_live_row_required",
            "source_path": str(FORMAL_388),
            "K_N": "0.00943177578696",
            "delta_N": "MISSING_DELTA_N",
            "E_measure": "MISSING_E_MEASURE",
            "E_mass": "MISSING_E_MASS",
            "E_transition": "MISSING_E_TRANSITION",
            "E_Xi": "MISSING_E_XI",
            "E_T": "MISSING_E_T",
            "input_valid_for_claim": False,
        },
        {
            "bound_id": "EG4406_1_zero_component_smoke",
            "arena": "Newton_source_normalization",
            "branch": "component_zero_smoke",
            "source_path": str(GATE_PATH),
            "K_N": "0.00943177578696",
            "delta_N": "1e-5",
            "E_measure": "0",
            "E_mass": "0",
            "E_transition": "0",
            "E_Xi": "0",
            "E_T": "0",
            "input_valid_for_claim": False,
        },
        {
            "bound_id": "EG4406_2_small_component_pass_smoke",
            "arena": "Newton_source_normalization",
            "branch": "small_component_schema_smoke",
            "source_path": str(GATE_PATH),
            "K_N": "0.00943177578696",
            "delta_N": "1e-5",
            "E_measure": "1e-7",
            "E_mass": "1e-7",
            "E_transition": "1e-7",
            "E_Xi": "1e-7",
            "E_T": "1e-7",
            "input_valid_for_claim": False,
        },
        {
            "bound_id": "EG4406_3_profile_shadow_fail_control",
            "arena": "Newton_source_normalization",
            "branch": "source_shadow_failure_control",
            "source_path": str(GATE_PATH),
            "K_N": "0.00943177578696",
            "delta_N": "1e-5",
            "E_measure": "0",
            "E_mass": "0.002",
            "E_transition": "0",
            "E_Xi": "0",
            "E_T": "0",
            "input_valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {"gate_id": "G4406_0_structural_bridge", "gate": "calibrated_GR_like_source_bridge", "claim_allowed": False, "reason": "profile density owner and public parent adoption remain unsigned."},
        {"gate_id": "G4406_1_eperp_bound", "gate": "finite_epsilon_Gsrc_perp_score", "claim_allowed": False, "reason": "real component rows and delta_N/projection conventions are missing."},
        {"gate_id": "G4406_2_Eprofile", "gate": "density_profile_source_shadow", "claim_allowed": False, "reason": "rho_eff=rho_H or sigma_shadow_perp bound is not sourced/parent-signed."},
        {"gate_id": "G4406_3_local_GR_Newton", "gate": "local_GR_Newton_PPN_R10", "claim_allowed": False, "reason": "source bridge plus all residual/projection gates are not globally closed."},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [{
        "decision_id": "DEC4406_0",
        "decision": DECISION,
        "summary": "4406 imports the 4354 source-charge/coupling fork into the current 440x chain and makes the finite branch executable. The clean branch is a GR-like calibrated source-blind G_cal plus Hamiltonian/Hilbert source mass, but the physical source-shape residual is epsilon_Gsrc_perp. The runner scores K_N(s)(E_measure+E_mass+E_transition+E_Xi+E_T) against delta_N. The next hard mathematical target is E_profile/source-shadow: prove rho_eff(y)=rho_H(y) before readout, or source sigma_shadow_perp.",
        "claim_allowed": False,
        "valid_for_claim": False,
    }]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4406_0", "item": "source bridge", "status": "STRUCTURAL_GR_LIKE_BRIDGE_IMPORTED", "notes": "calibrated source-blind G_cal is enough for fair GR-style reduction if source mass/profile closes."},
        {"status_id": "STAT4406_1", "item": "epsilon_Gsrc_perp", "status": "COMPONENT_BOUND_RUNNER_READY", "notes": "finite branch scores K_N(s) times the E_perp component sum."},
        {"status_id": "STAT4406_2", "item": "E_mass", "status": "PROFILE_OWNER_REQUIRED", "notes": "integrated mass equality is not enough for profile/transverse residuals."},
        {"status_id": "STAT4406_3", "item": "next target", "status": "EPROFILE_SOURCE_SHADOW_GATE", "notes": NEXT_TARGET},
    ]


def next_target_rows() -> List[Dict[str, object]]:
    return [{
        "next_id": "NT4406_0",
        "target": NEXT_TARGET,
        "question": "Can the parent grammar force rho_eff(y)=rho_H(y) on the same worldtube, or must sigma_shadow_perp/E_profile become the first real source-density row in the current 440x chain?",
        "preferred_route": "prove same-action Hilbert derivative only, no source-only functional/current slot, no hidden/source-label Hom, variation before readout, and distributional topological equality.",
        "fallback_route": "source or bound sigma_shadow_perp, then score E_profile through K_N(s) and the epsilon_Gsrc component runner.",
        "avoid": "claiming E_mass=0 from integrated mass equality or calibrated G alone.",
        "valid_for_claim": False,
    }]


def markdown_table(rows: List[Dict[str, object]]) -> str:
    if not rows:
        return ""
    keys = list(rows[0].keys())
    lines = ["| " + " | ".join(keys) + " |", "| " + " | ".join("---" for _ in keys) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(key, "")).replace("\n", " ") for key in keys) + " |")
    return "\n".join(lines)


def write_formal_doc(sources, derivations, bridge_output, eperp_output, gates, decisions, next_targets) -> None:
    FORMAL_PATH.write_text(
        f"""# 422 PPC4161 transition source charge coupling gate import or epsilonGsrc bound runner

Marker: `{MARKER}`

Generated UTC: `{STAMP}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove public local GR, Newtonian mechanics, Maxwell/EM closure, calibrated `G_N`, R10, PPN, clock, orbital, or WEP safety.

## Result

4406 imports the source-charge/coupling ladder into the current 440x chain.

The clean structural branch is:

```text
D_A ln kappa_eff = 0,
G_cal := c^4 kappa_eff/(8*pi),
int_W rho_H dV_H = M_H^dress[W_H;tau],
rho_eff(y)=rho_H(y) on W_H,
=> nabla^2 Phi_N = 4*pi G_cal rho_H.
```

This is the fair GR-like target: one calibrated universal coupling plus one non-circular Hilbert/Hamiltonian source density. It is not a demand that MTS predicts the numerical value of `G_N` at this stage.

The finite branch is now executable:

```text
epsilon_Gsrc_perp = epsilon_Gsrc - epsilon_bar_H,
E_perp <= E_measure + E_mass + E_transition + E_Xi + E_T,
|delta a|/|a_N| <= K_N(s) E_perp,
K_N(s)=min((1-s)^-2, 2s(1-s)^-3).
```

So the runner score is:

```text
K_N(s)(E_measure+E_mass+E_transition+E_Xi+E_T) <= delta_N.
```

The current obstruction is no longer generic coupling. The sharp next target is `E_profile` inside `E_mass`: prove `rho_eff(y)=rho_H(y)` by banning source-shadow/topological wrong-distribution profiles, or source a real `sigma_shadow_perp` row.

## Source Register

{markdown_table(sources)}

## Derivation Rows

{markdown_table(derivations)}

## Source Bridge Gate Output

{markdown_table(bridge_output)}

## Eperp Bound Gate Output

{markdown_table(eperp_output)}

## Claim Gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next Target

{markdown_table(next_targets)}
""",
        encoding="utf-8",
    )


def write_post_doc(decisions, next_targets) -> None:
    DOC_PATH.write_text(
        f"""# 4406 transition source-charge/coupling gate import

Marker: `{MARKER}`

## Private outcome

4406 imports the old source-coupling ladder into the current route and makes the finite branch executable as a real runner:

```text
K_N(s)(E_measure+E_mass+E_transition+E_Xi+E_T) <= delta_N.
```

The good news: the source bridge is structurally GR-like with calibrated `G_cal`.

The hard news: integrated mass equality is not enough; local GR/Newton needs density-profile ownership or a sourced `E_profile`/source-shadow bound.

## Decision

{markdown_table(decisions)}

## Next

{markdown_table(next_targets)}
""",
        encoding="utf-8",
    )


def append_once(path: Path, marker: str, block: str) -> None:
    current = text(path)
    if marker in current:
        return
    path.write_text(current.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def update_spine() -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""## 4406 local spine update: epsilonGsrc source bridge imported

Marker: `{MARKER}`

Spine update: the source-charge/coupling fork is now current-chain executable. The clean target is calibrated source-blind `G_cal` plus same-worldtube Hilbert/Hamiltonian source density. The finite target is `K_N(s)(E_measure+E_mass+E_transition+E_Xi+E_T) <= delta_N`. Integrated source mass is useful but not enough; `E_mass` requires profile ownership, so the next least-circular target is the `E_profile` source-shadow/distributional-equality gate.
""",
    )


def update_packet() -> None:
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## 4406 packet update: epsilonGsrc component runner

Marker: `{PACKET_MARKER}`

Packet update: 4406 imports the 4354-4376 source-coupling ladder into the current local-GR route. Generic coupling fog is replaced by a concrete source-shape score: `K_N(s)` times the no-cancellation `E_perp` component sum. The next work is density-profile ownership or a real source-shadow profile row.
""",
    )


def update_claims() -> None:
    row = (
        f'{CLAIM_ID},local_gr,'
        f'"4406 imports the source-charge/coupling ladder into the current 440x route. The clean branch is a GR-like calibrated source-blind G_cal plus Hamiltonian/Hilbert source density on the same worldtube. The finite branch is now executable as K_N(s)(E_measure+E_mass+E_transition+E_Xi+E_T)<=delta_N after common monopole subtraction. Integrated mass equality is explicitly not enough for E_mass; density-profile ownership or a source-shadow/E_profile row is next. No local-GR/Newton/PPN/R10/clock/orbital claim fires.",'
        f'"4406 source register, source bridge gate, epsilonGsrc/Eperp bound runner, derivations, claim gates, decision, status, next target and validation CSV.",'
        f'epsilonGsrc_source_bridge_imported_Eperp_component_runner_ready_nonclaim,'
        f'Prove density-profile ownership rho_eff=rho_H or source sigma_shadow_perp/E_profile in the current chain.,'
        f'"Claiming numeric G_N prediction is required here, claiming E_mass=0 from integrated mass equality, or treating a smoke Eperp row as empirical local-GR evidence."\n'
    )
    if f"\n{CLAIM_ID}," not in text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            handle.write(row)


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, object]]:
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4406_SOURCE_REGISTER.csv")
    derivations = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4406_DERIVATIONS.csv")
    bridge_output = read_csv(BRIDGE_OUTPUT)
    eperp_output = read_csv(EPERP_OUTPUT)
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4406_CLAIM_GATES.csv")
    rows: List[Dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail})

    add("VAL4406_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source exists")
    add("VAL4406_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle resolves")
    add("VAL4406_2_derivations_written", len(derivations) >= 4, "derivation rows written")
    add("VAL4406_3_current_bridge_blocks", any(row["bridge_id"] == "SB4406_0_current_integrated_bridge_profile_open" and row["current_status"] == "EPSILON_GSRC_SOURCE_BRIDGE_BLOCKED" for row in bridge_output), "current integrated bridge blocks without profile ownership")
    add("VAL4406_4_future_bridge_nonclaim", any(row["bridge_id"] == "SB4406_1_future_full_profile_clean_smoke" and row["private_clean_bridge"] == "True" and row["claim_allowed"] == "False" for row in bridge_output), "future clean bridge computes but remains nonclaim")
    add("VAL4406_5_missing_eperp_blocks", any(row["bound_id"] == "EG4406_0_missing_live_components" and row["current_status"] == "EPSILON_GSRC_EPERP_BOUND_BLOCKED" for row in eperp_output), "missing live Eperp row blocks")
    add("VAL4406_6_zero_eperp_passes_nonclaim", any(row["bound_id"] == "EG4406_1_zero_component_smoke" and row["within_bound"] == "True" and row["claim_allowed"] == "False" for row in eperp_output), "zero Eperp smoke passes but remains nonclaim")
    add("VAL4406_7_failure_control_detected", any(row["bound_id"] == "EG4406_3_profile_shadow_fail_control" and row["current_status"] == "EPSILON_GSRC_EPERP_BOUND_FAILS" for row in eperp_output), "profile-shadow failure control detected")
    add("VAL4406_8_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "claim gates false")
    add("VAL4406_9_formal_marker", MARKER in text(FORMAL_PATH), "formal marker present")
    add("VAL4406_10_post_marker", MARKER in text(DOC_PATH), "post marker present")
    add("VAL4406_11_spine_marker", MARKER in text(SPINE_PATH), "spine marker present")
    add("VAL4406_12_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker present")
    add("VAL4406_13_claim_row", f"\n{CLAIM_ID}," in text(CLAIMS_PATH), "claim row present")
    add("VAL4406_14_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4406_15_generated_nonclaim", all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path)), "generated rows stay nonclaim")
    add("VAL4406_16_gate_exists", GATE_PATH.exists() and "def evaluate_eperp_bound_rows" in text(GATE_PATH), "epsilon gate script exists")
    add("VAL4406_17_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent")
    return rows


def remove_pycache() -> None:
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    sources = source_rows()
    derivations = derivation_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()
    csv_payloads: Dict[str, List[Dict[str, object]]] = {
        "P8_Y5_R2FR_4406_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4406_DERIVATIONS.csv": derivations,
        "P8_Y5_R2FR_4406_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4406_DECISION.csv": decisions,
        "P8_Y5_R2FR_4406_STATUS.csv": statuses,
        "P8_Y5_R2FR_4406_NEXT_TARGET.csv": next_targets,
    }
    csv_paths: List[Path] = []
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_csv(BRIDGE_INPUT, bridge_input_rows())
    bridge_output = evaluate_source_bridge_rows(BRIDGE_INPUT)
    write_csv(BRIDGE_OUTPUT, bridge_output)
    csv_paths.extend([BRIDGE_INPUT, BRIDGE_OUTPUT])

    write_csv(EPERP_INPUT, eperp_input_rows())
    eperp_output = evaluate_eperp_bound_rows(EPERP_INPUT)
    write_csv(EPERP_OUTPUT, eperp_output)
    csv_paths.extend([EPERP_INPUT, EPERP_OUTPUT])

    write_formal_doc(sources, derivations, bridge_output, eperp_output, gates, decisions, next_targets)
    write_post_doc(decisions, next_targets)
    update_spine()
    update_packet()
    update_claims()
    remove_pycache()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
