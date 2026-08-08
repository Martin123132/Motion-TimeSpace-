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

CHECKPOINT = "4206"
CLAIM_ID = "L-047"
BRANCH_ID = "MTS_R2FR_Y5_CALIBRATED_GN_BRIDGE_4206"
DECISION = (
    "CALIBRATED_GN_BRIDGE_IMPORTED_INTO_4205_STRUCTURAL_NEWTON_COUPLING_CLOSED_"
    "NUMERIC_G_NOT_PREDICTED_HTAU_PARENT_CHARGE_CAVEAT_ACTIVE_NONCLAIM"
)
FORMAL_PATH = FORMAL / "222-PPC4161-calibrated-GN-bridge-and-source-charge-caveat.md"
DOC_PATH = POST / "4206-Y5-R2FR-calibrated-GN-bridge-or-source-charge-caveat.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_MARKER = "PPC4161_CALIBRATED_GN_BRIDGE_4206"
PACKET_MARKER = "PPC4161_PACKET_CALIBRATED_GN_BRIDGE_4206"
NEXT_TARGET = "4207-Y5-R2FR-Hamiltonian-source-charge-parent-owner-or-EM-Poynting-stress-owner.md"

SOURCES = {
    "SRC4206_00_4205_decision": (
        SOURCE_DIR / "P8_Y5_R2FR_4205_DECISION.csv",
        "source_coupling_GN_normalized",
        "4205 identified kappa_eff/G_N normalization as the coupling clause.",
    ),
    "SRC4206_01_182_ZH": (
        FORMAL / "182-PPC4161-ZH-source-measure-and-kappa-lock.md",
        "kappa_eff = kappa_* Z_H",
        "Source-measure split and physical leak channels.",
    ),
    "SRC4206_02_183_topological_lock": (
        FORMAL / "183-PPC4161-topological-kappa-star-lock-or-ZH-bound.md",
        "S_top[kappa_*, A_3] = int_M A_3 wedge d(kappa_*).",
        "Candidate topological kappa-star lock.",
    ),
    "SRC4206_03_185_Hilbert_source": (
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "T_parent^H = Z_0 T_H",
        "Hilbert source-measure descent closes delta_ZH in the private packet.",
    ),
    "SRC4206_04_186_worldtube_charge": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "M_H^dress[W_H;tau] = H_tau[S_link] - H_ref",
        "Hamiltonian/worldtube mass readout glue in the private packet.",
    ),
    "SRC4206_05_187_Newton_readout": (
        FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md",
        "nabla^2 Phi_N = 4*pi G_N rho_H.",
        "Poisson/Gauss/Newton readout from Hamiltonian source charge.",
    ),
    "SRC4206_06_188_PPN": (
        FORMAL / "188-PPC4161-full-PPN-readout-vector.md",
        "dot(G_eff)/G_eff = 0.",
        "Full private PPN vector uses coupling lock.",
    ),
    "SRC4206_07_190_quarantine": (
        FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md",
        "D_A ln kappa_* = 0 and delta_ZH = 0;",
        "Parent-action selector/quarantine clauses.",
    ),
    "SRC4206_08_194_calibrated_law": (
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "G_cal := c^4 kappa_eff/(8*pi).",
        "Calibrated source coupling law and numeric-G firewall.",
    ),
    "SRC4206_09_202_delta_kappa": (
        FORMAL / "202-PPC4161-same-coframe-source-memory-zero-law.md",
        "delta_kappa = 0.",
        "Joint zero-law says source-coupling drift closes only inside selector.",
    ),
    "SRC4206_10_1017_HTau_caveat": (
        POST / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
        "Pi_M^H is only notation.",
        "Later strict R10 audit keeps H_tau/M_H_ref parent ownership caveat active.",
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


def coupling_chain_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "CC4206_0_source_measure_factorization",
            "kappa_eff = kappa_* Z_H = kappa_* Z_0 exp(delta_ZH)",
            "separates universal coupling from physical source-measure leakage",
            "from_182",
        ),
        (
            "CC4206_1_kappa_lock",
            "D_A ln kappa_* = 0",
            "topological/superselection lock kills drift if parent-adopted",
            "conditional_from_183",
        ),
        (
            "CC4206_2_Hilbert_measure_descent",
            "T_parent^H = Z_0 T_H and delta_ZH = 0",
            "one common source normalization, no species/readout/range weights",
            "private_selector_from_185",
        ),
        (
            "CC4206_3_calibrated_coupling",
            "G_cal := c^4 kappa_eff/(8*pi)",
            "this is the Newton/GR source-coupling bridge; numeric value is calibrated unless a parent scale law fixes kappa_*",
            "from_194",
        ),
        (
            "CC4206_4_Poisson_readout",
            "nabla^2 Phi_N = 4*pi G_cal rho_H",
            "weak-field EH 00 equation gives Newtonian Poisson law for the same Hilbert density",
            "from_187_194",
        ),
        (
            "CC4206_5_exterior_acceleration",
            "a_r = -G_cal M_H^dress/r^2",
            "Newton acceleration follows from Gauss charge if M_H^dress is parent-owned",
            "conditional_mass_charge",
        ),
        (
            "CC4206_6_no_drift_vector",
            "D_A ln G_eff = D_A ln kappa_* + D_A delta_ZH = 0",
            "Gdot/species/frame/range/readout coupling residuals vanish only in the selector",
            "private_selector_from_185_188_202",
        ),
    ]
    return [
        {
            **common(),
            "chain_id": chain_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for chain_id, formula, meaning, status in rows
    ]


def calibration_theorem_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "GT4206_0_GR_standard",
            "GR does not predict numeric G_N; it uses one universal empirically calibrated coupling.",
            "MTS local reduction should be judged on same structural target, not a stricter fake target.",
            "methodology_gate",
        ),
        (
            "GT4206_1_MTS_structural_equivalence",
            "If kappa_eff is constant, source-blind and same-Hilbert-source, define G_N^obs := c^4 kappa_eff/(8*pi).",
            "then the Newton coefficient and EH matter coupling match GR after one calibration.",
            "conditional_selector_theorem",
        ),
        (
            "GT4206_2_non_circularity",
            "The calibration is non-circular only if rho_H/M_H^dress are defined before orbital readout.",
            "no orbital GM, fitted acceleration or measured G may define the mass charge.",
            "anti_circularity_guard",
        ),
        (
            "GT4206_3_numeric_G_firewall",
            "numeric(G_N) predicted = false unless a parent scale law fixes kappa_* and Z_0.",
            "this is not a failure of local GR reduction; it is a separate fundamental-constant prediction problem.",
            "public_claim_firewall",
        ),
        (
            "GT4206_4_HTau_caveat",
            "M_H^dress = H_tau[S_link]-H_ref remains parent-charge caveated by later strict audits.",
            "the structural coupling bridge is written, but the source-charge owner still needs parent symplectic proof.",
            "active_caveat",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "statement": statement,
            "effect": effect,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, statement, effect, status in rows
    ]


def reopening_rows() -> List[Dict[str, str]]:
    rows = [
        ("RG4206_0_kappa_drift", "D_A ln kappa_* != 0", "Gdot/G, frame/readout/source residual", "bound D_A ln kappa_* or parent-adopt topological lock"),
        ("RG4206_1_source_measure_leak", "D_A delta_ZH != 0", "WEP/species/range/environment residual", "prove Hilbert common measure or source-backed ZH derivative bounds"),
        ("RG4206_2_non_Hilbert_source", "T_parent^H != Z_0 T_H", "matter/EM/binding source mismatch", "derive single source functor and EM/Poynting Hilbert ownership"),
        ("RG4206_3_mass_charge_caveat", "H_tau/M_H_ref not parent-owned", "Newton source mass becomes notation or hidden fit", "derive MTS theta/Q_tau/integrability/fixed-reference charge"),
        ("RG4206_4_extra_Kperp_source", "K_extra_source != 0", "local PPN tensor residual", "use 4205 score_i gate or parent-sign no independent TT source"),
        ("RG4206_5_memory_hair", "c_Gamma local memory support survives", "same-coframe source-normalized PPN/clock residual", "prove support/projector silence or bound c_Gamma"),
        ("RG4206_6_numeric_G_claim", "claiming numeric G_N from calibration", "overclaim/fake derivation", "keep numeric G empirical unless parent scale law exists"),
    ]
    return [
        {
            **common(),
            "gate_id": gate_id,
            "failure_condition": failure_condition,
            "residual_reopened": residual_reopened,
            "required_repair": required_repair,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for gate_id, failure_condition, residual_reopened, required_repair in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "structural_kappa_to_GN_bridge": "True",
            "single_calibrated_G_allowed_like_GR": "True",
            "numeric_G_predicted": "False",
            "global_parent_adoption": "False",
            "Htau_parent_charge_caveat_active": "True",
            "EM_Poynting_owner_still_required": "True",
            "Kperp_independent_score_still_required_if_extra_source": "True",
            "local_GR_public_claim": "False",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def claim_firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4206_0_no_numeric_G_prediction", "Do not present calibrated G_cal as a numerical prediction of Newton's constant."),
        ("FW4206_1_no_orbital_GM_import", "Do not use observed orbital GM, fitted acceleration, or measured G to define rho_H or M_H^dress."),
        ("FW4206_2_no_global_adoption_claim", "The coupling bridge is private-selector structural unless the parent action signs the selector."),
        ("FW4206_3_no_HTau_shortcut", "Hamiltonian source charge still needs MTS theta/Q_tau, integrability, fixed reference and positivity ownership."),
        ("FW4206_4_no_EM_side_channel", "Matter/EM/binding source ownership must include Maxwell-Hodge/Poynting Hilbert stress or source side-channels reopen."),
        ("FW4206_5_no_Kperp_escape", "Any independent Kperp source still uses the 4205 score gate; coupling calibration does not erase it."),
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
            "summary": "4206 imports the calibrated kappa_eff-to-G_N law into the 4205 gate: structural Newton coupling is closed inside the private selector after one GR-like calibration, but numerical G is not predicted and H_tau/source-charge parent ownership remains active.",
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
            "why": "The coupling coefficient is now structurally calibrated; the next leap is source ownership: Hamiltonian mass charge and EM/Poynting Hilbert stress must be parent-owned, or they become bound rows.",
            "route_A": "derive MTS theta/Q_tau/H_tau integrability and fixed H_ref for M_H^dress",
            "route_B": "derive Maxwell-Hodge/Poynting stress as the EM Hilbert source contribution",
            "route_C": "if either fails, keep explicit source-charge or EM side-channel bound rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def all_rows() -> Dict[str, List[Dict[str, str]]]:
    return {
        "P8_Y5_R2FR_4206_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4206_COUPLING_CHAIN.csv": coupling_chain_rows(),
        "P8_Y5_R2FR_4206_CALIBRATION_THEOREM.csv": calibration_theorem_rows(),
        "P8_Y5_R2FR_4206_REOPENING_GATES.csv": reopening_rows(),
        "P8_Y5_R2FR_4206_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4206_CLAIM_FIREWALL.csv": claim_firewall_rows(),
        "P8_Y5_R2FR_4206_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4206_NEXT_TARGET.csv": next_target_rows(),
    }


def write_docs() -> None:
    formal = f"""# 222 - PPC4161 Calibrated GN Bridge And Source-Charge Caveat

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint answers the coupling question directly:

```text
MTS does not need to numerically predict G_N to reduce to GR/Newton.
```

GR itself uses one universal empirically calibrated `G_N`. The serious local-reduction requirement is instead:

```text
one constant source-blind coupling,
one Hilbert source measure,
one Hamiltonian/Hilbert mass charge,
no drift/species/frame/range/readout leakage.
```

## Coupling Chain

The private selector chain gives:

```text
kappa_eff = kappa_* Z_H = kappa_* Z_0 exp(delta_ZH)
D_A ln kappa_* = 0
delta_ZH = 0
D_A ln kappa_eff = 0
G_cal := c^4 kappa_eff/(8*pi).
```

Then the weak-field readout is:

```text
nabla^2 Phi_N = 4*pi G_cal rho_H
Phi_N = -G_cal M_H^dress/r
a_r = -G_cal M_H^dress/r^2.
```

So the `4205` coupling clause is structurally closed inside the private selector after one GR-like calibration:

```text
G_N^obs := G_cal.
```

## What This Does Not Claim

```text
numeric(G_N) predicted = false;
global MTS parent adoption = false;
public local-GR claim = false.
```

The later strict source-charge audits keep an active caveat:

```text
M_H^dress = H_tau[S_link] - H_ref
```

still needs parent-owned MTS `theta`, `Q_tau`, integrability, fixed reference, and positivity before the mass charge is globally signed rather than selector-defined.

## Current Verdict

This removes one unfair burden: MTS can be GR-competitive with a calibrated universal `G_N`, provided the coupling is constant and source-blind. The next real danger is not the numerical value of `G`; it is source ownership: `H_tau/M_H^dress` and EM/Poynting Hilbert stress.
"""
    checkpoint = f"""# 4206 - Y5 R2FR Calibrated GN Bridge Or Source-Charge Caveat

Decision: `{DECISION}`

4206 imports the existing calibrated source-coupling law into the 4205 gate.

The local coupling bridge is:

```text
G_cal := c^4 kappa_eff/(8*pi),
kappa_eff = kappa_* Z_0,
D_A ln kappa_eff = 0.
```

This means MTS can reduce to the GR/Newton coupling structure with one calibrated `G_N`, just like GR, without pretending to predict the numerical value of `G`.

The caveat is still sharp:

```text
M_H^dress = H_tau[S_link] - H_ref
```

must be parent-owned, not imported from orbital `GM` or left as notation.
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
        f'{CLAIM_ID},local_gr,"The calibrated kappa_eff-to-G_N bridge is imported into the 4205 local-GR gate: structural Newton coupling closes inside the private selector with one GR-like empirical calibration, while numeric G prediction remains false and H_tau source-charge ownership remains caveated.",'
        f'"4206 source audit, coupling chain, calibration theorem, reopening gates, decision row and firewall.",'
        f'private_calibrated_GN_bridge_nonclaim_HTau_caveat_active,'
        f'"Parent-own H_tau/M_Hdress and Maxwell-Hodge/Poynting source stress, or fill source-charge/EM side-channel bound rows.",'
        f'"A universal calibrated G is acceptable for GR reduction; the dangerous shortcut is importing orbital GM or hiding source-measure drift."'
    )
    if f"{CLAIM_ID}," not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(claim_row + "\n")

    spine_block = f"""### PPC4161 Calibrated GN Bridge - 4206

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4206 answers the coupling fork from 4205. Inside the private selector:

```text
G_cal := c^4 kappa_eff/(8*pi),
kappa_eff = kappa_* Z_0,
D_A ln kappa_eff = 0.
```

This structurally recovers the GR/Newton coupling after one empirical calibration `G_N^obs := G_cal`. It does not predict the numerical value of `G_N`, and it keeps the `H_tau/M_H^dress` source-charge parent caveat active."""
    append_once(SPINE_PATH, SPINE_MARKER, spine_block)

    packet_block = f"""## PPC4161 Packet Calibrated GN Bridge - 4206

Marker: `{PACKET_MARKER}`

The private packet now treats `G_N` the same way GR does: one universal calibrated coupling is acceptable. The remaining hard source problem is not the value of `G`; it is parent ownership of the Hamiltonian mass charge and EM/Poynting Hilbert stress."""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4206_SOURCE_REGISTER.csv"]
    chain = rows_by_file["P8_Y5_R2FR_4206_COUPLING_CHAIN.csv"]
    theorem = rows_by_file["P8_Y5_R2FR_4206_CALIBRATION_THEOREM.csv"]
    reopening = rows_by_file["P8_Y5_R2FR_4206_REOPENING_GATES.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4206_DECISION.csv"]
    all_rows_flat = [row for rows in rows_by_file.values() for row in rows]
    checks = [
        ("VAL4206_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source)),
        ("VAL4206_1_source_needles", "all source needles found", all(row["required_text_found"] == "True" for row in source)),
        ("VAL4206_2_chain_has_Gcal", "coupling chain has G_cal definition", any(row["chain_id"] == "CC4206_3_calibrated_coupling" for row in chain)),
        ("VAL4206_3_chain_has_Poisson", "coupling chain has Newton/Poisson readout", any(row["chain_id"] == "CC4206_4_Poisson_readout" for row in chain)),
        ("VAL4206_4_GR_calibration_methodology", "theorem records GR-like calibration standard", any(row["theorem_id"] == "GT4206_0_GR_standard" for row in theorem)),
        ("VAL4206_5_numeric_G_firewall", "theorem blocks numerical G prediction", any(row["theorem_id"] == "GT4206_3_numeric_G_firewall" for row in theorem)),
        ("VAL4206_6_HTau_caveat", "theorem keeps H_tau caveat active", any(row["theorem_id"] == "GT4206_4_HTau_caveat" for row in theorem)),
        ("VAL4206_7_reopening_gates", "reopening gates include source measure, mass charge, EM and Kperp hazards", {"RG4206_1_source_measure_leak", "RG4206_3_mass_charge_caveat", "RG4206_2_non_Hilbert_source", "RG4206_4_extra_Kperp_source"}.issubset({row["gate_id"] for row in reopening})),
        ("VAL4206_8_decision_nonclaim", "decision keeps numeric G false and Htau caveat active", decision[0]["numeric_G_predicted"] == "False" and decision[0]["Htau_parent_charge_caveat_active"] == "True"),
        ("VAL4206_9_next_target_source_owner", "next target points at source ownership", "source-charge" in decision[0]["next_target"] or "source" in decision[0]["next_target"]),
        ("VAL4206_10_no_claim_flags", "all generated claim flags remain false", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows_flat)),
        ("VAL4206_11_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4206_12_claim_register", "claim register contains L-047", CLAIM_ID + "," in read_text(CLAIMS_PATH)),
        ("VAL4206_13_spine_marker", "spine marker present", SPINE_MARKER in read_text(SPINE_PATH)),
        ("VAL4206_14_packet_marker", "packet marker present", PACKET_MARKER in read_text(PACKET_PATH)),
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
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4206_VALIDATION.csv", validation)
    if not all(row["passed"] == "True" for row in validation):
        failed = [row for row in validation if row["passed"] != "True"]
        raise RuntimeError(f"4206 validation failed: {failed}")
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4206_VALIDATION.csv'}")
    print("rows=15 validation checks")


if __name__ == "__main__":
    main()
