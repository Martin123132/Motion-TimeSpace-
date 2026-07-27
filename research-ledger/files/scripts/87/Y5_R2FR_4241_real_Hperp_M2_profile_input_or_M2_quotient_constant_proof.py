from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4241"
CLAIM_ID = "L-082"
BRANCH = "MTS_R2FR_Y5_M2_DEFECT_SPLIT_4241"
DECISION = "M2_QUOTIENT_CONSTANT_NOT_FULLY_DERIVED_CLASSIFIER_CHANNELS_PRUNED_DEFECT_SPLIT_AND_REAL_PROFILE_INPUT_CONTRACT_BUILT_NONCLAIM"
MARKER = "PPC4161_M2_DEFECT_SPLIT_PROFILE_INPUT_CONTRACT_4241"
PACKET_MARKER = "PPC4161_PACKET_M2_DEFECT_SPLIT_PROFILE_INPUT_CONTRACT_4241"
NEXT_TARGET = "4242-Y5-R2FR-M2-defect-source-map-pruning-or-real-profile-input-pack.md"

FORMAL_PATH = FORMAL / "257-PPC4161-real-Hperp-M2-profile-input-or-M2-quotient-constant-proof.md"
DOC_PATH = POST / "4241-Y5-R2FR-real-Hperp-M2-profile-input-or-M2-quotient-constant-proof.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4241_VALIDATION.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4241_00_4240_next": SourceSpec(
        "SRC4241_00_4240_next",
        SOURCE_DIR / "P8_Y5_R2FR_4240_NEXT_TARGET.csv",
        "4241-Y5-R2FR-real-Hperp-M2-profile-input-or-M2-quotient-constant-proof.md",
        "4240 selected real profile input or M2 quotient-constant proof.",
    ),
    "SRC4241_01_4240_formal": SourceSpec(
        "SRC4241_01_4240_formal",
        FORMAL / "256-PPC4161-HL-qbasic-defect-zero-or-M2-quotient-constant-profile-runner.md",
        "A_J,eff_private <= |S_A H_perp^A| + |D_m Delta_h M_2| + |D_t M_2|.",
        "4240 reduced source/M2 budget.",
    ),
    "SRC4241_02_4240_audit": SourceSpec(
        "SRC4241_02_4240_audit",
        SOURCE_DIR / "P8_Y5_R2FR_4240_HPERP_QBASIC_AUDIT.csv",
        "H_perp=0",
        "Machine-readable Hperp zero rejection.",
    ),
    "SRC4241_03_HL_candidate": SourceSpec(
        "SRC4241_03_HL_candidate",
        FORMAL / "125-local-leakage-vector-invariant.md",
        "H_L^A(X_B);",
        "H_L candidate is not parent-derived.",
    ),
    "SRC4241_04_component_pool": SourceSpec(
        "SRC4241_04_component_pool",
        FORMAL / "125-local-leakage-vector-invariant.md",
        "| `H_transport` | `I_rot+I_shear+I_grad` |",
        "Candidate H_L component pool.",
    ),
    "SRC4241_05_smooth_repair": SourceSpec(
        "SRC4241_05_smooth_repair",
        FORMAL / "130-smooth-scalar-channel-repair.md",
        "forbidden from directly entering:",
        "Smooth scalar repair forbids classifier channels as direct local scalar sources.",
    ),
    "SRC4241_06_dotB_repair": SourceSpec(
        "SRC4241_06_dotB_repair",
        FORMAL / "130-smooth-scalar-channel-repair.md",
        "classifier / transition diagnostic.",
        "I_dotB is diagnostic/classifier, not direct M2 source.",
    ),
    "SRC4241_07_Lcg_prune": SourceSpec(
        "SRC4241_07_Lcg_prune",
        FORMAL / "129-scalar-channel-stationarity.md",
        "z_Lcg_pruned_until_reference_derived = true",
        "Lcg channel is pruned until reference is derived.",
    ),
    "SRC4241_08_gradient_power": SourceSpec(
        "SRC4241_08_gradient_power",
        FORMAL / "131-repaired-local-gradient-power.md",
        "Y_2 in {M_2, T_2},",
        "M2 gradient-power theorem form.",
    ),
    "SRC4241_09_gradient_open": SourceSpec(
        "SRC4241_09_gradient_open",
        FORMAL / "131-repaired-local-gradient-power.md",
        "nabla Y_2 bounded;",
        "M2 gradient boundedness remains open.",
    ),
    "SRC4241_10_stationary": SourceSpec(
        "SRC4241_10_stationary",
        FORMAL / "207-PPC4161-memory-fixed-point-equation-and-smooth-minimizer-contract.md",
        "stationary and projected-homogeneous local invariants imply:",
        "Stationary/projected homogeneous local invariant zero route.",
    ),
    "SRC4241_11_M2_descent": SourceSpec(
        "SRC4241_11_M2_descent",
        FORMAL / "254-PPC4161-vertical-current-M2-zero-theorem-or-profile-sampler.md",
        "M_2 descends through projected-homogeneous local invariants,",
        "4238 M2 descent clause.",
    ),
    "SRC4241_12_claim_register": SourceSpec(
        "SRC4241_12_claim_register",
        FORMAL / "02-claims-register.csv",
        "L-081",
        "Prior claim-register anchor for 4240.",
    ),
}


def common() -> Dict[str, str]:
    return {"timestamp_utc": STAMP, "branch_id": BRANCH, "checkpoint_id": CHECKPOINT}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def append_once(path: Path, marker: str, block: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + block.strip() + "\n")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for spec in SOURCE_SPECS.values():
        text = read_text(spec.path)
        rows.append(
            {
                **common(),
                "source_id": spec.source_id,
                "path": str(spec.path),
                "exists": str(spec.path.exists()),
                "required_text": spec.required_text,
                "required_text_found": str(spec.required_text in text),
                "role": spec.role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def component_audit_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "MC4241_0_Htheta",
            "H_theta",
            "classifier_only_pruned_from_M2_source",
            "E_theta can classify screening through U_B/Pi_B but the smooth scalar repair forbids it as a direct M2 source.",
            "no direct Delta_h M2 or D_t M2 row from this channel",
        ),
        (
            "MC4241_1_HdotB",
            "H_dotB",
            "classifier_only_pruned_from_M2_source",
            "I_dotB is a transition diagnostic/classifier, not a direct scalar-source channel.",
            "no direct M2 drift source from this channel",
        ),
        (
            "MC4241_2_HLcg",
            "H_Lcg",
            "pruned_until_reference_derived",
            "z_Lcg/H_Lcg is not allowed as a hidden local source dial until its parent reference is derived.",
            "no direct M2 source contribution",
        ),
        (
            "MC4241_3_Htransport",
            "H_transport",
            "defect_profile_open",
            "Transport/rotation/shear/gradient participation may be a routing eligibility variable but is not parent-zero as local scalar source.",
            "M2_defect_transport profile needed or route-to-nonlocal sector proof",
        ),
        (
            "MC4241_4_HBgrad",
            "H_Bgrad",
            "defect_profile_open",
            "Screening-gradient/transition-shell leakage is precisely where far-local constant-M2 can fail.",
            "M2_defect_Bgrad profile or transition-shell quarantine needed",
        ),
        (
            "MC4241_5_Hperp",
            "H_perp",
            "source_defect_open",
            "4240 rejected Hperp=0; source residual remains S_A Hperp^A.",
            "Hperp profile or zero theorem needed",
        ),
    ]
    return [
        {
            **common(),
            "component_id": component_id,
            "component": component,
            "status": status,
            "rationale": rationale,
            "effect": effect,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for component_id, component, status, rationale, effect in rows
    ]


def m2_split_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "MS4241_0_split",
            "M_2 = M2_pruned_safe + M2_defect",
            "M2_pruned_safe excludes direct classifier-only theta/dotB/Lcg channels; M2_defect carries unresolved transport/Bgrad/Hperp-dependent source-shape pieces.",
            "active split",
        ),
        (
            "MS4241_1_lap_split",
            "Delta_h M_2 = Delta_h M2_defect",
            "If the safe part is quotient-constant/projected homogeneous, only the defect part contributes to the Laplacian row.",
            "conditional_private",
        ),
        (
            "MS4241_2_drift_split",
            "D_t M_2 = D_t M2_defect",
            "If the safe part is stationary, only the defect part contributes to the drift row.",
            "conditional_private",
        ),
        (
            "MS4241_3_reduced_budget",
            "A_J,eff_private <= |S_A Hperp| + |D_m Delta_h M2_defect| + |D_t M2_defect|",
            "4240 budget with pruned classifier channels removed from the direct scalar-source map.",
            "active_nonclaim",
        ),
        (
            "MS4241_4_exact_zero",
            "Hperp=0, Delta_h M2_defect=0, D_t M2_defect=0 => A_J,eff_private=0 at leading order",
            "Remaining exact-zero route after source-map hygiene.",
            "not claimed",
        ),
    ]
    return [
        {
            **common(),
            "split_id": split_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for split_id, formula, meaning, status in rows
    ]


def proof_status_rows() -> List[Dict[str, str]]:
    rows = [
        ("MP4241_0_classifier_prune", "theta/dotB/Lcg not direct M2 source channels", "private_hygiene_pass", "from smooth scalar repair and stationarity gate"),
        ("MP4241_1_transport_zero", "transport/routing variables do not source local M2", "open", "needs route-to-galaxy/nonlocal projector proof or real local profile"),
        ("MP4241_2_Bgrad_zero", "Bgrad/transition-shell variables vanish in tested far-local collar", "open", "needs shell quarantine or profile support bound"),
        ("MP4241_3_Hperp_zero", "Hperp=0", "open", "4240 rejected as not currently derived"),
        ("MP4241_4_M2_constant", "Delta_h M2_defect=D_t M2_defect=0", "open", "needs quotient-constant/harmonic stationary proof"),
        ("MP4241_5_profile_path", "real Hperp/M2defect profile input contract", "selected", "needed if any open zero clause fails"),
    ]
    return [
        {
            **common(),
            "proof_id": proof_id,
            "condition": condition,
            "status": status,
            "evidence_or_need": evidence_or_need,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for proof_id, condition, status, evidence_or_need in rows
    ]


def real_profile_contract_rows() -> List[Dict[str, str]]:
    rows = [
        ("RP4241_0_Hperp", "Hperp^A(x,t)", "dimensionless profile", "source defect S_A Hperp^A", "MISSING_PARENT_PROFILE"),
        ("RP4241_1_SA", "S_A(x,t)", "source-current Jacobian", "source defect contraction", "MISSING_PARENT_SOURCE_JACOBIAN"),
        ("RP4241_2_M2defect", "M2_defect(x,t)", "dimensionless shape profile", "lap/drift source owner", "MISSING_PARENT_SHAPE"),
        ("RP4241_3_DeltaM2defect", "Delta_h M2_defect", "1/length^2 before normalization", "M2 Laplacian row", "MISSING_LOCAL_GEOMETRY_PROFILE"),
        ("RP4241_4_DtM2defect", "D_t M2_defect", "1/time before normalization", "M2 drift row", "MISSING_LOCAL_TIME_PROFILE"),
        ("RP4241_5_Dm", "D_m", "memory diffusion/mobility normalization", "scales Laplacian row", "MISSING_PARENT_NORMALIZATION"),
        ("RP4241_6_budget_owner", "(mu_Xi T_res)/|c_Gamma|", "dimensionless budget owner", "normalizes strong local Gdot gate", "MISSING_TIMESCALE_COUPLING"),
        ("RP4241_7_arena", "arena projection profile_a/J_a", "arena-dependent", "alpha3/Gdot/gradient scoring", "MISSING_ARENA_PROJECTION"),
    ]
    return [
        {
            **common(),
            "profile_id": profile_id,
            "quantity": quantity,
            "units": units,
            "role": role,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for profile_id, quantity, units, role, status in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "forward_move": "M2 is split into pruned-safe classifier hygiene plus M2_defect; classifier-only theta/dotB/Lcg channels are blocked from direct scalar-source use.",
            "M2_constant_claimed": "False",
            "profile_ready_for_real_inputs": "contract_only",
            "scoreable_now": "False",
            "best_next_move": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4241_0_no_classifier_source", "Do not use theta, dotB or Lcg classifier channels as direct M2 scalar source terms.", "active"),
        ("FW4241_1_no_M2_constant_claim", "Do not claim M2 constant while transport/Bgrad/Hperp defect pieces remain open.", "active"),
        ("FW4241_2_no_profile_claim", "Profile input contract rows are not evidence until real parent/local profiles are supplied.", "active"),
        ("FW4241_3_no_cancellation", "Reduced budget remains absolute: no cancellation between source, Laplacian and drift rows.", "active"),
        ("FW4241_4_private_scope", "Source-map pruning is private hygiene, not public local-GR proof.", "active"),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule, status in rows
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status": "private_M2_defect_split_nonclaim",
            "summary": "4241 prunes classifier-only channels from direct M2 source use and reduces the live profile burden to Hperp plus M2_defect transport/Bgrad pieces.",
            "scoreable_now": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "reason": "Next either prove transport/Bgrad/Hperp defect pieces are source-map pruned/routed, or supply real profile inputs for the reduced defect budget.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def all_generated_groups() -> Iterable[List[Dict[str, str]]]:
    return (
        source_rows(),
        component_audit_rows(),
        m2_split_rows(),
        proof_status_rows(),
        real_profile_contract_rows(),
        decision_rows(),
        firewall_rows(),
        status_rows(),
        next_target_rows(),
    )


def formal_doc() -> str:
    return f"""
# 257 - PPC4161 Real Hperp M2 Profile Input Or M2 Quotient Constant Proof

Marker: `{MARKER}`

Branch: `{BRANCH}`
Decision: `{DECISION}`

## Result

4241 does not prove full `M_2` quotient-constant behavior. It does something narrower and useful: it prevents classifier variables from being smuggled into the local scalar source map.

The smooth scalar repair already says `theta`, `dotB`, and `L_cg`-style channels are not allowed as direct local scalar-source terms. Therefore split:

```text
M_2 = M2_pruned_safe + M2_defect.
```

where `M2_pruned_safe` excludes direct classifier-only `theta/dotB/Lcg` source use, and `M2_defect` carries the still-open transport, screening-gradient and non-q leakage pieces.

## Reduced Defect Budget

The live private budget becomes:

```text
A_J,eff_private
  <= |S_A Hperp^A| + |D_m Delta_h M2_defect| + |D_t M2_defect|.
```

The exact zero route is now:

```text
Hperp = 0,
Delta_h M2_defect = 0,
D_t M2_defect = 0.
```

## Component Status

```text
H_theta  -> classifier-only/pruned from direct M2 source,
H_dotB   -> classifier-only/pruned from direct M2 source,
H_Lcg    -> pruned until parent reference is derived,
H_transport -> defect profile open,
H_Bgrad     -> defect profile open,
Hperp       -> source defect open.
```

## Claim Status

Private nonclaim. This is source-map hygiene and defect isolation, not local-GR proof.

## Next Target

`{NEXT_TARGET}`
"""


def checkpoint_doc() -> str:
    return f"""
# 4241 - Real Hperp M2 Profile Input Or M2 Quotient Constant Proof

**Status:** `{DECISION}`.

## Forward Move

4241 splits:

```text
M_2 = M2_pruned_safe + M2_defect.
```

Classifier-only `theta`, `dotB`, and `Lcg` channels are blocked from direct scalar-source use. The remaining live rows are:

```text
S_A Hperp^A,
Delta_h M2_defect,
D_t M2_defect.
```

## Still Missing

Transport/Bgrad/Hperp pieces are not zeroed yet and no real profile input exists.

## Next

`{NEXT_TARGET}`
"""


def update_claim_register() -> None:
    path = FORMAL / "02-claims-register.csv"
    rows = csv_rows(path)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr",
            "claim": "4241 splits M2 into pruned-safe classifier hygiene and M2_defect. Theta/dotB/Lcg channels are blocked from direct scalar-source use, while transport, Bgrad and Hperp remain explicit defect/profile rows. This is a private nonclaim.",
            "current_evidence": "4241 source register, component audit, M2 split rows, proof status, real profile contract, decision and firewall.",
            "status": "private_M2_defect_split_nonclaim",
            "next_test": "Prove transport/Bgrad/Hperp defect pieces are pruned/routed/zero, or supply real profile inputs for the reduced defect budget.",
            "key_risk": "Treating source-map hygiene as a proof that M2 is constant would overclaim.",
        }
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def update_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 M2 Defect Split Profile Input Contract

Marker: `{MARKER}`

4241 blocks classifier-only `theta`, `dotB`, and `Lcg` channels from direct local scalar-source use and splits:

```text
M_2 = M2_pruned_safe + M2_defect.
```

The live reduced private cGamma budget is now:

```text
|S_A Hperp^A| + |D_m Delta_h M2_defect| + |D_t M2_defect|.
```

Transport/Bgrad/Hperp remain explicit defect rows, not hidden constants.
"""
    packet_block = f"""
## Packet Update - M2 Defect Split

Marker: `{PACKET_MARKER}`

The packet now prevents scalar classifier leakage from re-entering the cGamma local source budget. Remaining source/M2 pressure is isolated in `Hperp`, `M2_defect_transport`, and `M2_defect_Bgrad`.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validation_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        rows.append(
            {
                **common(),
                "check_id": check_id,
                "description": description,
                "passed": str(bool(passed)),
                "evidence": evidence,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )

    sources = source_rows()
    components = component_audit_rows()
    split = m2_split_rows()
    proof = proof_status_rows()
    profile = real_profile_contract_rows()
    all_rows = [row for group in all_generated_groups() for row in group]

    add("VAL4241_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources), "source register")
    add("VAL4241_1_needles_found", "all source needles found", all(row["required_text_found"] == "True" for row in sources), "source register")
    add("VAL4241_2_classifier_pruned", "theta/dotB/Lcg channels pruned or classifier-only", {"H_theta", "H_dotB", "H_Lcg"}.issubset({row["component"] for row in components if "pruned" in row["status"] or "classifier_only" in row["status"]}), "component audit")
    add("VAL4241_3_defects_open", "transport/Bgrad/Hperp defects remain open", {"H_transport", "H_Bgrad", "H_perp"}.issubset({row["component"] for row in components if "open" in row["status"]}), "component audit")
    add("VAL4241_4_M2_split", "M2 split row exists", any(row["formula"] == "M_2 = M2_pruned_safe + M2_defect" for row in split), "M2 split")
    add("VAL4241_5_reduced_budget", "reduced defect budget exists", any("M2_defect" in row["formula"] and "Hperp" in row["formula"] for row in split), "M2 split")
    add("VAL4241_6_proof_status", "profile path selected and M2 constant not claimed", any(row["condition"] == "real Hperp/M2defect profile input contract" and row["status"] == "selected" for row in proof) and any(row["condition"] == "Delta_h M2_defect=D_t M2_defect=0" and row["status"] == "open" for row in proof), "proof status")
    add("VAL4241_7_profile_contract", "profile contract has Hperp M2defect source budget rows", {"Hperp^A(x,t)", "M2_defect(x,t)", "(mu_Xi T_res)/|c_Gamma|"}.issubset({row["quantity"] for row in profile}), "profile contract")
    add("VAL4241_8_decision_nonclaim", "decision keeps scoreable false", decision_rows()[0]["scoreable_now"] == "False", "decision")
    add("VAL4241_9_docs_written", "formal and checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), f"{FORMAL_PATH}; {DOC_PATH}")
    add("VAL4241_10_claim_register", "claims register contains L-082", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), str(FORMAL / "02-claims-register.csv"))
    add("VAL4241_11_spine_marker", "spine contains marker", MARKER in read_text(FORMAL / "07-unification-spine.md"), str(FORMAL / "07-unification-spine.md"))
    add("VAL4241_12_packet_marker", "packet contains marker", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), str(FORMAL / "180-PPC4161-private-local-packet-integration.md"))
    add("VAL4241_13_no_claim_flags", "no generated row is valid for claim", all(row.get("valid_for_claim") != "True" for row in all_rows), "all generated groups")
    add("VAL4241_14_next_target", "next target selected", next_target_rows()[0]["next_target"] == NEXT_TARGET, NEXT_TARGET)
    return rows


def main() -> None:
    paths = {
        "source": SOURCE_DIR / "P8_Y5_R2FR_4241_SOURCE_REGISTER.csv",
        "components": SOURCE_DIR / "P8_Y5_R2FR_4241_M2_COMPONENT_AUDIT.csv",
        "split": SOURCE_DIR / "P8_Y5_R2FR_4241_M2_DEFECT_SPLIT.csv",
        "proof": SOURCE_DIR / "P8_Y5_R2FR_4241_M2_PROOF_STATUS.csv",
        "profile": SOURCE_DIR / "P8_Y5_R2FR_4241_REAL_PROFILE_INPUT_CONTRACT.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4241_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4241_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4241_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4241_NEXT_TARGET.csv",
    }
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    write_csv(paths["source"], source_rows())
    write_csv(paths["components"], component_audit_rows())
    write_csv(paths["split"], m2_split_rows())
    write_csv(paths["proof"], proof_status_rows())
    write_csv(paths["profile"], real_profile_contract_rows())
    write_csv(paths["decision"], decision_rows())
    write_csv(paths["firewall"], firewall_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next"], next_target_rows())
    update_claim_register()
    update_spine_and_packet()
    write_csv(VALIDATION_PATH, validation_rows())
    failed_rows = [row for row in csv_rows(VALIDATION_PATH) if row["passed"] != "True"]
    print(f"Decision: {DECISION}")
    print(f"Formal: {FORMAL_PATH}")
    print(f"Checkpoint: {DOC_PATH}")
    print(f"Validation: {VALIDATION_PATH}")
    print(f"Validation rows: {len(csv_rows(VALIDATION_PATH))}; failed: {len(failed_rows)}")
    if failed_rows:
        for failed_row in failed_rows:
            print(f"FAILED {failed_row['check_id']}: {failed_row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
