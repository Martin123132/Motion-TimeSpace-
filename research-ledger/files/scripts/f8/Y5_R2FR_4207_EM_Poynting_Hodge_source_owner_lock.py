from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()

CHECKPOINT = "4207"
CLAIM_ID = "L-048"
BRANCH_ID = "MTS_R2FR_Y5_EM_POYNTING_HODGE_OWNER_4207"
DECISION = (
    "EM_POYNTING_HODGE_SOURCE_OWNER_LOCK_IMPORTED_INTO_4206_"
    "POYNTING_IS_HILBERT_FLUX_NOT_EXTRA_BACKGROUND_FORCE_HODGE_DEFORMATION_GATES_RETAINED_NONCLAIM"
)
FORMAL_PATH = FORMAL / "223-PPC4161-EM-Poynting-Hodge-source-owner-lock.md"
DOC_PATH = POST / "4207-Y5-R2FR-EM-Poynting-Hodge-source-owner-lock-or-side-channel-bound.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_MARKER = "PPC4161_EM_POYNTING_HODGE_SOURCE_OWNER_4207"
PACKET_MARKER = "PPC4161_PACKET_EM_POYNTING_HODGE_SOURCE_OWNER_4207"
NEXT_TARGET = "4208-Y5-R2FR-MTS-Hodge-deformation-zero-or-Maxwell-constitutive-bound.md"

SOURCES = {
    "SRC4207_00_4206_decision": (
        SOURCE_DIR / "P8_Y5_R2FR_4206_DECISION.csv",
        "EM_Poynting_owner_still_required",
        "4206 says EM/Poynting source ownership is still required.",
    ),
    "SRC4207_01_185_source": (
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "S_EM[A,g_obs]",
        "Hilbert source action includes EM with the observed metric.",
    ),
    "SRC4207_02_190_selector": (
        FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md",
        "Maxwell-Hodge/Poynting stress ownership;",
        "Parent selector names Maxwell-Hodge/Poynting as a source leak to own.",
    ),
    "SRC4207_03_191_theorem": (
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "S_i = -T_EM(n,e_i) = (E cross B)_i.",
        "Maxwell-Hodge/Poynting owner theorem.",
    ),
    "SRC4207_04_192_boundary": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "F_rad[tau] != 0  =>  route as boundary charge",
        "Radiative flux is boundary/Hamiltonian routed, not hidden bulk source.",
    ),
    "SRC4207_05_4000_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4000_EM_STRESS_POYNTING_THEOREM.csv",
        "Poynting intuition is legitimate",
        "EM stress/Poynting theorem source rows.",
    ),
    "SRC4207_06_4127_once": (
        SOURCE_DIR / "P8_Y5_R2FR_4127_POYNTING_ONCE_THEOREM.csv",
        "c_Poynt_extra=0",
        "Poynting once-only theorem.",
    ),
    "SRC4207_07_4155_once_lock": (
        SOURCE_DIR / "P8_Y5_R2FR_4155_POYNTING_ONCE_LOCK.csv",
        "EXTRA_POYNTING_COEFFICIENT_ZERO_BY_SINGLE_SOURCE_FUNCTIONAL",
        "Worldtube/Hilbert Poynting once-lock.",
    ),
    "SRC4207_08_4174_gate": (
        SOURCE_DIR / "P8_Y5_R2FR_4174_EM_POYNTING_OWNER_GATE.csv",
        "No independent S_Poynting_background",
        "EM owner gate forbids a standalone Poynting background term.",
    ),
    "SRC4207_09_4175_identification": (
        SOURCE_DIR / "P8_Y5_R2FR_4175_POYNTING_STRESS_IDENTIFICATION.csv",
        "Poynting flux is a component of T_EM",
        "Poynting stress identification rows.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def common() -> Dict[str, str]:
    return {"timestamp_utc": now(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_rows() -> List[Dict[str, str]]:
    rows = []
    for source_id, (path, needle, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "exists": str(path.exists()),
                "required_text": needle,
                "required_text_found": str(needle in text),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def owner_chain_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "PO4207_0_same_hodge_action",
            "S_MH[A,g_obs] = -1/4 int sqrt(-g_obs) F_mu_nu F^mu_nu",
            "EM uses the same observed metric/coframe/Hodge star as local gravity and matter.",
            "conditional_private_selector",
        ),
        (
            "PO4207_1_Hilbert_stress",
            "T_EM^{mu nu} = F^{mu alpha}F^nu_alpha - 1/4 g_obs^{mu nu}F^2",
            "EM energy, pressure, momentum density and stress are inside T_total once.",
            "standard_variational_identity",
        ),
        (
            "PO4207_2_Poynting_identification",
            "S_i = -T_EM(n,e_i) = (E x B)_i",
            "Poynting is energy-flux through the same Hilbert stress, not an extra force field.",
            "exact_local_frame_identity",
        ),
        (
            "PO4207_3_internal_exchange",
            "nabla_mu T_EM^{mu nu}=-F^{nu lambda}J_lambda and nabla_mu T_matter^{mu nu}=+F^{nu lambda}J_lambda",
            "Lorentz force is internal matter-EM exchange; total Hilbert source remains conserved.",
            "ward_exchange_identity",
        ),
        (
            "PO4207_4_once_only",
            "M_trial = M_H[J_H_total] + c_Poynt_extra int S_Poynting dot n dA => c_Poynt_extra=0",
            "adding Poynting again double-counts energy already in the source functional.",
            "single_source_functional_lock",
        ),
        (
            "PO4207_5_radiative_route",
            "F_rad[tau] != 0 => boundary/Hamiltonian flux row, not static bulk source",
            "radiation is not erased; it is routed instead of hidden in local PPN.",
            "boundary_guard",
        ),
    ]
    return [
        {
            **common(),
            "owner_id": owner_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for owner_id, formula, meaning, status in rows
    ]


def background_interpretation_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "BI4207_0_safe_background",
            "Poynting as flow through the observed Hodge/coframe background",
            "safe if the background owner is g_obs/e_obs/*_g and the flux is T_EM^{0i}",
            "supports Martin-style flow intuition without adding a new force",
        ),
        (
            "BI4207_1_unsafe_background",
            "standalone Poynting/background source term",
            "unsafe if it is added after T_EM is already in T_total",
            "double-counts EM energy or creates a hidden preferred-frame source",
        ),
        (
            "BI4207_2_MTS_deformation",
            "MTS-specific Hodge deformation delta(*_MTS)",
            "allowed only as a named residual coefficient if parent action contains it",
            "becomes Delta_Hodge_EM or C_XF2 bound row, not a free local-GR pass",
        ),
        (
            "BI4207_3_bound_fields",
            "Coulomb/magnetostatic bound fields",
            "owned by M_H^dress through T_EM and S_binding",
            "not an extra mass correction if one Hilbert source functional is used",
        ),
        (
            "BI4207_4_open_flux",
            "open radiative EM flux",
            "boundary/Hamiltonian channel, not zero by assumption",
            "keeps radiation physical while protecting compact local PPN",
        ),
    ]
    return [
        {
            **common(),
            "interpretation_id": interpretation_id,
            "branch": branch,
            "condition": condition,
            "verdict": verdict,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for interpretation_id, branch, condition, verdict in rows
    ]


def retained_gate_rows() -> List[Dict[str, str]]:
    rows = [
        ("EG4207_0_delta_Hodge_EM", "observed Hodge/coframe not parent-owned", "Maxwell constitutive/readout residual", "derive same Hodge owner or fill constitutive bound"),
        ("EG4207_1_delta_w_EM", "species/readout EM source weight survives", "WEP/clock/source-normalization residual", "prove no independent EM weights or bound them"),
        ("EG4207_2_C_XF2", "extra MTS X F^2 coupling", "scalar/vector EM side-channel", "parent-forbid, screen, or empirically bound"),
        ("EG4207_3_C_JQ", "hidden EM-current multiplier or charge normalization drift", "charge/source-current residual", "derive charge normalization or bound"),
        ("EG4207_4_Delta_rad_Poynting", "net radiative Poynting flux crosses collar", "Hamiltonian/source-mass drift", "route as boundary flux or fill source row"),
        ("EG4207_5_Delta_internal_exchange", "matter-EM exchange not owned by one action", "apparent source nonconservation", "derive Ward exchange cancellation"),
        ("EG4207_6_c_Poynt_extra", "extra standalone Poynting source coefficient", "double count / hidden force", "zero by once-only theorem if single source functional parent-signed"),
    ]
    return [
        {
            **common(),
            "gate_id": gate_id,
            "failure_condition": failure_condition,
            "residual": residual,
            "required_repair": required_repair,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for gate_id, failure_condition, residual, required_repair in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "Poynting_owned_as_Hilbert_flux": "True",
            "extra_Poynting_coefficient_zero_conditional": "True",
            "safe_background_interpretation_written": "True",
            "Hodge_deformation_gates_retained": "True",
            "radiative_flux_boundary_routed": "True",
            "global_parent_adoption": "False",
            "public_local_GR_claim": "False",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def claim_firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4207_0_no_extra_Poynting_force", "Do not add a standalone Poynting/background force after Maxwell-Hodge stress is already in T_total."),
        ("FW4207_1_no_Hodge_overclaim", "Observed Maxwell-Hodge ownership does not prove EM unification, charge quantization, alpha, or QED."),
        ("FW4207_2_no_radiation_erasure", "Open EM radiation is boundary/Hamiltonian flux, not silently zero."),
        ("FW4207_3_no_second_metric", "A second EM metric/coframe/Hodge star reopens WEP, clock and PPN residuals."),
        ("FW4207_4_no_binding_double_count", "Matter-EM binding energy is counted once in S_binding/M_H^dress, not again as a source correction."),
        ("FW4207_5_no_global_adoption_claim", "This imports a private selector theorem into the current gate; it is not global parent adoption."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule in rows
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "summary": "4207 welds the existing Maxwell-Hodge/Poynting theorem into the current local-GR/source-coupling gate: Poynting is legitimate energy flow through the observed Hodge/coframe Hilbert stress, not an extra background force; Hodge deformation and radiative flux gates stay retained.",
            "local_GR_claim": "False",
            "public_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "The safe Poynting interpretation is now locked; the remaining EM risk is whether MTS modifies the Hodge/constitutive relation or current normalization.",
            "route_A": "prove delta(*_MTS)=0 and no extra X F^2/current couplings in compact local collars",
            "route_B": "derive charge/current normalization with same observed Hodge owner",
            "route_C": "if not, fill Delta_Hodge_EM, C_XF2, C_JQ and Delta_rad_Poynting bound rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def all_rows() -> Dict[str, List[Dict[str, str]]]:
    return {
        "P8_Y5_R2FR_4207_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4207_POYNTING_OWNER_CHAIN.csv": owner_chain_rows(),
        "P8_Y5_R2FR_4207_BACKGROUND_INTERPRETATION.csv": background_interpretation_rows(),
        "P8_Y5_R2FR_4207_RETAINED_GATES.csv": retained_gate_rows(),
        "P8_Y5_R2FR_4207_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4207_CLAIM_FIREWALL.csv": claim_firewall_rows(),
        "P8_Y5_R2FR_4207_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4207_NEXT_TARGET.csv": next_target_rows(),
    }


def write_docs() -> None:
    formal = f"""# 223 - PPC4161 EM Poynting Hodge Source Owner Lock

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint welds the older Maxwell-Hodge/Poynting result into the current 4205-4206 local-GR/source-coupling gate.

## Owner Chain

Inside the compact local selector:

```text
S_MH[A,g_obs] = -1/4 int sqrt(-g_obs) F_mu_nu F^mu_nu.
```

Hilbert variation gives:

```text
T_EM^mu_nu =
F^mu_alpha F^nu_alpha
- 1/4 g_obs^mu_nu F_alpha_beta F^alpha_beta.
```

For a local observer:

```text
rho_EM = T_EM(n,n) = 1/2(E^2+B^2),
S_i = -T_EM(n,e_i) = (E x B)_i.
```

So the Poynting vector is real physical flow, but in the safe branch it is a component of the Maxwell-Hodge Hilbert stress, not a second gravitational source.

## Background-Flow Interpretation

The safe MTS reading is:

```text
Poynting flow = energy transport through the observed Hodge/coframe structure.
```

The unsafe reading is:

```text
T_total already contains T_EM,
then add a separate Poynting/background source term.
```

That would double-count or create a hidden preferred-frame/current channel. The once-only lock is:

```text
M_trial = M_H[J_H_total] + c_Poynt_extra int_boundary S_Poynting dot n dA
=> c_Poynt_extra = 0
```

when the single source functional is parent-signed.

## Retained Gates

This does not derive all of EM. The live gates are:

```text
Delta_Hodge_EM,
delta_w_EM,
C_XF2,
C_JQ,
Delta_rad_Poynting,
Delta_internal_exchange.
```

If MTS changes the Hodge/constitutive relation, charge normalization, or radiation boundary routing, those become explicit residual rows rather than hidden assumptions.
"""
    checkpoint = f"""# 4207 - Y5 R2FR EM Poynting Hodge Source Owner Lock Or Side-Channel Bound

Decision: `{DECISION}`

4207 locks the useful version of the Poynting intuition:

```text
Poynting = EM energy-flow through the observed Hodge/coframe Hilbert stress.
```

It rejects the unsafe version:

```text
Poynting = extra standalone local gravitational source after T_EM is already counted.
```

The remaining EM risk is now cleanly named: MTS-specific Hodge deformation, extra `X F^2` coupling, hidden current normalization, or unrouted radiative flux.
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(checkpoint, encoding="utf-8")


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker not in text:
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write("\n\n" + block.strip() + "\n")


def update_registers() -> None:
    claim_row = (
        f'{CLAIM_ID},em_local_gr,"The Maxwell-Hodge/Poynting source-owner theorem is welded into the current local-GR gate: Poynting is Hilbert EM energy flux through the observed Hodge/coframe structure, not an extra background force; Hodge deformation and current/radiation side-channel gates remain retained.",'
        f'"4207 source audit, owner chain, background interpretation rows, retained gates, decision row and firewall.",'
        f'private_EM_Poynting_Hodge_owner_nonclaim_side_channels_retained,'
        f'"Prove MTS Hodge deformation/current side-channels vanish or fill Delta_Hodge_EM, C_XF2, C_JQ and radiative Poynting bound rows.",'
        f'"The Poynting intuition is useful only if it is owned by the single Maxwell-Hodge Hilbert source; adding it again would double-count."'
    )
    if f"{CLAIM_ID}," not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(claim_row + "\n")

    spine_block = f"""### PPC4161 EM Poynting Hodge Source Owner - 4207

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4207 locks the safe Poynting interpretation:

```text
S_i = -T_EM(n,e_i) = (E x B)_i.
```

Poynting flow is physical energy transport through the observed Hodge/coframe Hilbert stress. It is not an extra background force to add after `T_EM` is already in `T_total`. MTS-specific Hodge deformation/current/radiative channels remain explicit gates."""
    append_once(SPINE_PATH, SPINE_MARKER, spine_block)

    packet_block = f"""## PPC4161 Packet EM Poynting Hodge Source Owner - 4207

Marker: `{PACKET_MARKER}`

The packet now treats Poynting as legitimate source-current flow inside Maxwell-Hodge Hilbert stress. The next EM problem is not Poynting itself; it is whether MTS changes the Hodge/constitutive/current side in a way that has to be bounded."""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4207_SOURCE_REGISTER.csv"]
    owner = rows_by_file["P8_Y5_R2FR_4207_POYNTING_OWNER_CHAIN.csv"]
    interpretation = rows_by_file["P8_Y5_R2FR_4207_BACKGROUND_INTERPRETATION.csv"]
    gates = rows_by_file["P8_Y5_R2FR_4207_RETAINED_GATES.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4207_DECISION.csv"]
    all_rows_flat = [row for rows in rows_by_file.values() for row in rows]
    checks = [
        ("VAL4207_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source)),
        ("VAL4207_1_source_needles", "all source needles found", all(row["required_text_found"] == "True" for row in source)),
        ("VAL4207_2_owner_chain", "owner chain includes action, stress, Poynting and once-only rows", {"PO4207_0_same_hodge_action", "PO4207_1_Hilbert_stress", "PO4207_2_Poynting_identification", "PO4207_4_once_only"}.issubset({row["owner_id"] for row in owner})),
        ("VAL4207_3_boundary_route", "radiative boundary route represented", any(row["owner_id"] == "PO4207_5_radiative_route" for row in owner)),
        ("VAL4207_4_background_split", "safe and unsafe background interpretations written", {"BI4207_0_safe_background", "BI4207_1_unsafe_background", "BI4207_2_MTS_deformation"}.issubset({row["interpretation_id"] for row in interpretation})),
        ("VAL4207_5_retained_gates", "retained EM gates include Hodge, XF2, current and radiative flux", {"EG4207_0_delta_Hodge_EM", "EG4207_2_C_XF2", "EG4207_3_C_JQ", "EG4207_4_Delta_rad_Poynting"}.issubset({row["gate_id"] for row in gates})),
        ("VAL4207_6_decision_nonclaim", "decision keeps parent adoption false and Hodge gates retained", decision[0]["global_parent_adoption"] == "False" and decision[0]["Hodge_deformation_gates_retained"] == "True"),
        ("VAL4207_7_once_lock", "extra Poynting coefficient zero is only conditional", decision[0]["extra_Poynting_coefficient_zero_conditional"] == "True"),
        ("VAL4207_8_next_target_Hodge", "next target points at Hodge/constitutive bound", "Hodge" in decision[0]["next_target"]),
        ("VAL4207_9_no_claim_flags", "all generated claim flags remain false", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows_flat)),
        ("VAL4207_10_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4207_11_claim_register", "claim register contains L-048", CLAIM_ID + "," in read_text(CLAIMS_PATH)),
        ("VAL4207_12_spine_marker", "spine marker present", SPINE_MARKER in read_text(SPINE_PATH)),
        ("VAL4207_13_packet_marker", "packet marker present", PACKET_MARKER in read_text(PACKET_PATH)),
    ]
    return [
        {
            **common(),
            "check_id": check_id,
            "check": check,
            "passed": str(bool(passed)),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, check, passed in checks
    ]


def write_all() -> None:
    rows_by_file = all_rows()
    write_docs()
    update_registers()
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)
    validation = validate(rows_by_file)
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4207_VALIDATION.csv", validation)
    if not all(row["passed"] == "True" for row in validation):
        failed = [row for row in validation if row["passed"] != "True"]
        raise RuntimeError(f"4207 validation failed: {failed}")
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4207_VALIDATION.csv'}")
    print("rows=14 validation checks")


if __name__ == "__main__":
    main()
