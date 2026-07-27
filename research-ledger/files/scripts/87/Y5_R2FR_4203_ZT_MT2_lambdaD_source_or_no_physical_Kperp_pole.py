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

CHECKPOINT = "4203"
CLAIM_ID = "L-044"
BRANCH_ID = "MTS_R2FR_Y5_NO_PHYSICAL_KPERP_POLE_4203"
DECISION = (
    "NO_PHYSICAL_KPERP_POLE_THEOREM_CONDITIONAL_GR_TT_STATIC_BRANCH_ZERO_"
    "INDEPENDENT_MTS_TENSOR_POLE_STILL_UNSIGNED_NONCLAIM"
)
FORMAL_PATH = FORMAL / "219-PPC4161-no-physical-Kperp-pole-theorem.md"
DOC_PATH = POST / "4203-Y5-R2FR-ZT-MT2-lambdaD-source-or-no-physical-Kperp-pole.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_MARKER = "PPC4161_NO_PHYSICAL_KPERP_POLE_4203"
PACKET_MARKER = "PPC4161_PACKET_NO_PHYSICAL_KPERP_POLE_4203"
NEXT_TARGET = "4204-Y5-R2FR-parent-identity-Kperp-is-GR-TT-or-independent-tensor-source-pack.md"

SOURCES = {
    "SRC4203_00_4202_nopole": (
        SOURCE_DIR / "P8_Y5_R2FR_4202_NO_PHYSICAL_POLE_ROUTES.csv",
        "NP4202_2_EH_TT_not_new_field",
        "4202 no-physical-pole alternatives.",
    ),
    "SRC4203_01_4202_decision": (
        SOURCE_DIR / "P8_Y5_R2FR_4202_DECISION.csv",
        "coercivity_formula",
        "4202 decision and LT denominator.",
    ),
    "SRC4203_02_218_formal": (
        FORMAL / "218-PPC4161-parent-tensor-operator-LT-coercivity.md",
        "or prove no physical `K_perp` pole",
        "4202 formal no-pole handoff.",
    ),
    "SRC4203_03_61_ansatz": (
        FORMAL / "61-local-ppn-tensor-ansatz.md",
        "transverse homogeneous freedom",
        "Local ansatz defines Kperp as transverse homogeneous freedom.",
    ),
    "SRC4203_04_192_boundary": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "F_rad[tau] != 0  =>  route as boundary charge, not hidden bulk current.",
        "Radiative boundary charge routing.",
    ),
    "SRC4203_05_59_ppn": (
        FORMAL / "59-local-ppn-branch-framework.md",
        "local PPN branch fails",
        "PPN branch requires full metric observables.",
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


def theorem_clause_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "NP4203_0_identity",
            "Kperp identity",
            "K_perp is ordinary GR transverse-traceless homogeneous metric freedom, not an independent MTS tensor field",
            "would prevent new source coupling and new PPN pole",
            "unsigned",
        ),
        (
            "NP4203_1_stationary_ppn",
            "stationary local PPN branch",
            "partial_tau K_perp=0 in compact local PPN scoring domain",
            "turns GR TT wave equation into static elliptic harmonic problem",
            "conditional",
        ),
        (
            "NP4203_2_boundary_routing",
            "radiative boundary routing",
            "nonzero F_rad is routed as Hamiltonian/radiation boundary charge, not hidden bulk potential",
            "keeps gravitational radiation out of static local PPN residual",
            "conditional_private_selector",
        ),
        (
            "NP4203_3_finite_energy_decay",
            "finite-energy/decay or Dirichlet data",
            "K_perp has zero local static boundary data or decays at infinity after source support separation",
            "enables uniqueness/no-static-TT-hair theorem",
            "unsigned",
        ),
        (
            "NP4203_4_kernel_gauge",
            "kernel/gauge/topology certificate",
            "no nontrivial stationary TT kernel survives the observed quotient and local topology",
            "blocks Neumann/topological/gauge zero-mode loophole",
            "unsigned",
        ),
        (
            "NP4203_5_no_extra_source",
            "no independent MTS TT source",
            "P_TT(source/current/domain leakage)=0 for the extra MTS sector",
            "separates ordinary GR radiation from new local tensor force",
            "unsigned",
        ),
        (
            "NP4203_6_total_certificate",
            "no physical Kperp pole certificate",
            "all clauses signed => W_i^K=0 in stationary compact local PPN and Kperp not scored as extra local force",
            "would close Kperp local PPN branch without numeric source pack",
            "not_parent_signed",
        ),
    ]
    return [
        {
            **common(),
            "clause_id": clause_id,
            "clause": clause,
            "mathematical_statement": statement,
            "effect_if_signed": effect,
            "current_status": status,
            "parent_signed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for clause_id, clause, statement, effect, status in rows
    ]


def proof_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "PR4203_0_wave_to_static",
            "ordinary GR TT equation",
            "Box h_TT=0; stationarity gives Delta h_TT=0",
            "requires Kperp=GR TT identity and no extra MTS source",
            "conditional",
        ),
        (
            "PR4203_1_energy",
            "static harmonic uniqueness",
            "0=int h_TT Delta h_TT = -int |D h_TT|^2 + boundary",
            "zero/decay boundary makes boundary term vanish",
            "derived_conditional",
        ),
        (
            "PR4203_2_zero",
            "finite-energy static result",
            "D h_TT=0; decay/Dirichlet plus kernel certificate gives h_TT=0",
            "kills static local PPN Kperp hair",
            "derived_conditional",
        ),
        (
            "PR4203_3_radiative_routing",
            "nonstationary TT branch",
            "partial_tau h_TT != 0 is gravitational radiation/boundary charge, not static PPN potential",
            "routes to radiation sector rather than local-GR residual",
            "conditional_private_selector",
        ),
        (
            "PR4203_4_failure",
            "independent MTS tensor pole",
            "if Kperp has its own source/operator not identical to GR TT, return to 4202 source pack",
            "prevents hiding an extra tensor force behind GR words",
            "active_guard",
        ),
    ]
    return [
        {
            **common(),
            "proof_id": proof_id,
            "step": step,
            "formula": formula,
            "premise": premise,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for proof_id, step, formula, premise, status in rows
    ]


def branch_decision_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "BR4203_0_static_GR_TT",
            "Kperp=ordinary GR TT and stationary compact local branch",
            "W_i^K=0; I_T/B_T/Z_Tmode not scored as extra local force",
            "best_route_but_identity_unsigned",
        ),
        (
            "BR4203_1_radiative_GR_TT",
            "Kperp=ordinary GR TT but nonstationary/radiative",
            "route as gravitational radiation/Hamiltonian boundary charge",
            "not_static_PPN_residual",
        ),
        (
            "BR4203_2_independent_MTS_TT",
            "Kperp is independent parent tensor pole/source",
            "must use 4202 coefficient source pack and PPN inequalities",
            "active_fallback_if_identity_fails",
        ),
        (
            "BR4203_3_current_state",
            "identity with GR TT is not parent-signed",
            "no-pole route remains conditional; finite source-pack branch stays active",
            "current_state_nonclaim",
        ),
    ]
    return [
        {
            **common(),
            "branch_id_row": branch_id_row,
            "condition": condition,
            "action": action,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for branch_id_row, condition, action, status in rows
    ]


def source_pack_update_rows() -> List[Dict[str, str]]:
    rows = [
        ("W_i^K", "0", "only if NP4203 total certificate is parent-signed", "missing_parent_identity_certificate"),
        ("I_T", "0_or_radiation_boundary", "only if no incoming hidden tensor mode and radiative TT is routed", "missing_no_incoming_certificate"),
        ("Z_Tmode", "0", "only if stationary TT kernel/topology/gauge certificate is signed", "missing_kernel_certificate"),
        ("B_T", "0_or_boundary_charge", "only if boundary no-flux/Hamiltonian routing is signed for tensor sector", "missing_boundary_certificate"),
        ("S_T", "0", "only if no independent MTS TT source projection is signed", "missing_source_projection_zero"),
        ("C_T", "not_applicable_if_no_pole", "if Kperp has no physical pole; otherwise use 4202 C_T<=1/(Z_T lambda_D+M_T2)", "missing_branch_identity"),
    ]
    return [
        {
            **common(),
            "symbol": symbol,
            "value_if_signed": value_if_signed,
            "required_certificate": required_certificate,
            "current_status": current_status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for symbol, value_if_signed, required_certificate, current_status in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "no_pole_theorem_shape_derived": "True",
            "Kperp_equals_GR_TT_parent_signed": "False",
            "static_TT_zero_if_signed": "True",
            "radiative_route": "boundary_or_GR_radiation_sector",
            "independent_tensor_fallback_active": "True",
            "numeric_score_ready": "False",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def claim_firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4203_0_no_GR_word_magic", "Calling Kperp TT or gravitational does not prove it is ordinary GR TT."),
        ("FW4203_1_static_only", "The zero theorem applies to stationary/static PPN, not incoming waves."),
        ("FW4203_2_radiation_not_hidden_force", "Radiative TT must be routed as radiation/boundary charge, not local static potential."),
        ("FW4203_3_identity_or_source_pack", "If Kperp is an independent MTS pole, return to 4202 coefficients."),
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
            "summary": "4203 derives the conditional no-extra-pole theorem: ordinary GR TT static compact local Kperp vanishes or routes as radiation, but identity with GR TT is not parent-signed.",
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
            "why": "The no-pole theorem is clean if Kperp is ordinary GR TT; the next gate must parent-sign that identity or accept the independent tensor source-pack route.",
            "route_A": "prove Kperp is ordinary GR TT/gauge/radiation already counted by the metric sector",
            "route_B": "prove observed quotient weights W_i^K vanish for Kperp",
            "route_C": "if not, fill independent tensor source-pack coefficients from 4202",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def all_rows() -> Dict[str, List[Dict[str, str]]]:
    return {
        "P8_Y5_R2FR_4203_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4203_NO_POLE_THEOREM_CLAUSES.csv": theorem_clause_rows(),
        "P8_Y5_R2FR_4203_STATIC_TT_PROOF.csv": proof_rows(),
        "P8_Y5_R2FR_4203_BRANCH_DECISION.csv": branch_decision_rows(),
        "P8_Y5_R2FR_4203_SOURCE_PACK_UPDATE.csv": source_pack_update_rows(),
        "P8_Y5_R2FR_4203_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4203_CLAIM_FIREWALL.csv": claim_firewall_rows(),
        "P8_Y5_R2FR_4203_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4203_NEXT_TARGET.csv": next_target_rows(),
    }


def write_docs() -> None:
    formal = f"""# 219 - PPC4161 No Physical Kperp Pole Theorem

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint derives the clean no-extra-pole theorem shape, but does not parent-sign that `K_perp` is ordinary GR TT/gauge/radiation rather than an independent MTS tensor pole.

## Theorem Shape

If:

```text
K_perp = ordinary GR transverse-traceless homogeneous metric freedom,
partial_tau K_perp = 0 in the compact local PPN branch,
no independent MTS TT source projects onto it,
boundary/radiative pieces are routed as Hamiltonian or gravitational-radiation charges,
no stationary TT kernel survives the observed quotient,
```

then the static local equation is:

```text
Delta K_perp = 0.
```

The energy identity gives:

```text
0 = int K_perp Delta K_perp
  = - int |D K_perp|^2 + boundary.
```

With zero/routed boundary and finite-energy decay:

```text
K_perp = 0
```

in stationary compact local PPN. Nonstationary TT is gravitational radiation, not a hidden static local force.

## Verdict

This is the best clean route: if parent-signed, `W_i^K=0` for static local PPN and `C_T` becomes unnecessary. But the parent identity is not signed yet. If `K_perp` is an independent MTS tensor pole, the 4202 source-pack branch remains active.
"""
    checkpoint = f"""# 4203 - Y5 R2FR ZT MT2 lambdaD Source Or No Physical Kperp Pole

Decision: `{DECISION}`

4203 takes the clean route first. Static ordinary GR TT hair vanishes under compact stationary PPN/no-radiation conditions:

```text
Delta K_perp=0,
zero/routed boundary,
finite energy,
no TT kernel
=> K_perp=0.
```

Radiative TT is routed as gravitational radiation/boundary charge. This would remove `Kperp` as an extra local force if the parent proves `Kperp` is ordinary GR TT/gauge/radiation. That identity is not yet signed, so the independent tensor source-pack route remains active.
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
        f'{CLAIM_ID},local_gr,"The no-physical-Kperp-pole theorem is derived conditionally: ordinary GR TT static local hair vanishes or routes as radiation, '
        f'but the parent identity Kperp=GR TT/gauge/radiation is unsigned.","4203 source audit, no-pole clauses, static TT proof, branch decision, '
        f'source-pack update, decision row and firewall.",private_no_Kperp_pole_theorem_nonclaim_parent_identity_unsigned,'
        f'"Parent-sign Kperp as ordinary GR TT/gauge/radiation or return to independent tensor source-pack coefficients.",'
        f'"Using the words TT or gravitational radiation without the parent identity would hide an independent tensor force."'
    )
    if f"{CLAIM_ID}," not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(claim_row + "\n")

    spine_block = f"""### PPC4161 No Physical Kperp Pole Theorem - 4203

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4203 derives the clean conditional route:

```text
Kperp = ordinary GR TT, stationary compact PPN, zero/routed boundary, no kernel
=> Kperp = 0.
```

Radiative TT is routed as gravitational radiation/boundary charge, not hidden local potential. The route remains nonclaim until the parent proves `Kperp` is ordinary GR TT/gauge/radiation rather than an independent MTS tensor pole."""
    append_once(SPINE_PATH, SPINE_MARKER, spine_block)

    packet_block = f"""## PPC4161 Packet No Physical Kperp Pole Theorem - 4203

Marker: `{PACKET_MARKER}`

Inside the private packet, the cleanest `Kperp` escape hatch is now explicit: if it is only ordinary GR TT/gauge/radiation, static compact local PPN has no extra `Kperp` force. If that parent identity fails, the packet must use the 4202 finite tensor coefficient route."""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4203_SOURCE_REGISTER.csv"]
    clauses = rows_by_file["P8_Y5_R2FR_4203_NO_POLE_THEOREM_CLAUSES.csv"]
    proof = rows_by_file["P8_Y5_R2FR_4203_STATIC_TT_PROOF.csv"]
    branch = rows_by_file["P8_Y5_R2FR_4203_BRANCH_DECISION.csv"]
    update = rows_by_file["P8_Y5_R2FR_4203_SOURCE_PACK_UPDATE.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4203_DECISION.csv"]
    all_rows_flat = [row for rows in rows_by_file.values() for row in rows]
    checks = [
        ("VAL4203_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source)),
        ("VAL4203_1_source_needles", "all source needles found", all(row["required_text_found"] == "True" for row in source)),
        ("VAL4203_2_clauses_complete", "no-pole theorem has identity, stationarity, boundary, kernel and source clauses", len(clauses) == 7),
        ("VAL4203_3_static_proof", "static TT proof includes zero result and radiative routing", any(row["proof_id"] == "PR4203_2_zero" for row in proof) and any(row["proof_id"] == "PR4203_3_radiative_routing" for row in proof)),
        ("VAL4203_4_independent_fallback", "independent MTS tensor fallback remains active", any(row["branch_id_row"] == "BR4203_2_independent_MTS_TT" for row in branch)),
        ("VAL4203_5_source_pack_update", "source-pack update contains W_i^K and C_T consequences", any(row["symbol"] == "W_i^K" for row in update) and any(row["symbol"] == "C_T" for row in update)),
        ("VAL4203_6_decision_nonclaim", "decision keeps parent identity unsigned", decision[0]["Kperp_equals_GR_TT_parent_signed"] == "False"),
        ("VAL4203_7_no_claim_flags", "all generated claim flags remain false", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows_flat)),
        ("VAL4203_8_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4203_9_claim_register", "claim register contains L-044", CLAIM_ID + "," in read_text(CLAIMS_PATH)),
        ("VAL4203_10_spine_marker", "spine marker present", SPINE_MARKER in read_text(SPINE_PATH)),
        ("VAL4203_11_packet_marker", "packet marker present", PACKET_MARKER in read_text(PACKET_PATH)),
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
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4203_VALIDATION.csv", validation)
    if not all(row["passed"] == "True" for row in validation):
        failed = [row for row in validation if row["passed"] != "True"]
        raise RuntimeError(f"4203 validation failed: {failed}")
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4203_VALIDATION.csv'}")
    print("rows=12 validation checks")


if __name__ == "__main__":
    main()
