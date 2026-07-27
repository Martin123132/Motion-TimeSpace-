from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4256"
CLAIM_ID = "L-097"
BRANCH = "MTS_R2FR_Y5_DQ_PROJECTION_SPECTRAL_GAP_BRIDGE_4256"
DECISION = "DQ_PROJECTION_KERNEL_ZERO_DERIVED_CONDITIONALLY_SPECTRAL_GAP_AND_COMPONENT_VALUES_STILL_UNSIGNED_NONCLAIM"
MARKER = "PPC4161_DQ_PROJECTION_SPECTRAL_GAP_BRIDGE_4256"
PACKET_MARKER = "PPC4161_PACKET_DQ_PROJECTION_SPECTRAL_GAP_BRIDGE_4256"
NEXT_TARGET = "4257-Y5-R2FR-sign-Dq-projector-and-spectral-gap-or-fill-Dq-component-values.md"

FORMAL_PATH = FORMAL / "272-PPC4161-Dq-projection-spectral-gap-bridge.md"
DOC_PATH = POST / "4256-Y5-R2FR-Dq-projection-spectral-gap-bridge.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4256_VALIDATION.csv"

COMPONENT_CANDIDATE_4254_PATH = SOURCE_DIR / "P8_Y5_R2FR_4254_DQ_COMPONENT_VALUES_CANDIDATE.csv"
CONSTANT_CANDIDATE_4254_PATH = SOURCE_DIR / "P8_Y5_R2FR_4254_TOMOGRAPHY_CONSTANTS_CANDIDATE.csv"
LOCAL_COMPONENT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4256_DQ_COMPONENT_VALUES_CANDIDATE.csv"
LOCAL_CONSTANT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4256_TOMOGRAPHY_CONSTANTS_CANDIDATE.csv"

PROBES = (
    "Dq_geom",
    "Dq_tau",
    "Dq_matter",
    "Dq_source_readout",
    "Dq_theta_marker",
    "Dq_boundary_projector",
    "Dq_EM",
    "Dq_coeff",
)
CANDIDATE_ID = "DQ_COORDINATE_SEMINORM_SMOKE_4255"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4256_00_4245_projection": SourceSpec(
        "SRC4256_00_4245_projection",
        FORMAL / "261-PPC4161-HL-qbasic-strip-and-Dq-bound-first-input-row.md",
        "Hperp := (1 - Pi_kerDq) H_L.",
        "4245 introduces the split H_L=H_q+Hperp using Pi_kerDq.",
    ),
    "SRC4256_01_4245_live_rows": SourceSpec(
        "SRC4256_01_4245_live_rows",
        FORMAL / "261-PPC4161-HL-qbasic-strip-and-Dq-bound-first-input-row.md",
        "Dq_EM[Hperp]",
        "4245 names the eight live Dq probes.",
    ),
    "SRC4256_02_4254_rank_gate": SourceSpec(
        "SRC4256_02_4254_rank_gate",
        FORMAL / "270-PPC4161-fill-source-probe-rank-or-parent-Pi4-Jacobian-row.md",
        "sigma_S^2 = lambda_min",
        "4254 weighted rank gate that consumes component and constant candidates.",
    ),
    "SRC4256_03_4255_guard": SourceSpec(
        "SRC4256_03_4255_guard",
        FORMAL / "271-PPC4161-fill-first-Dq-probe-matrix-row-or-parent-Pi4-source-row.md",
        "eta_Dq_kernel",
        "4255 identifies the physical norm-equivalence and kernel-residue guard.",
    ),
    "SRC4256_04_4255_rank_smoke": SourceSpec(
        "SRC4256_04_4255_rank_smoke",
        SOURCE_DIR / "P8_Y5_R2FR_4255_RANK_SMOKE_RESULT.csv",
        "DQ_COORDINATE_SEMINORM_SMOKE_4255",
        "4255 filled the Dq-coordinate identity matrix candidate.",
    ),
    "SRC4256_05_4255_missing_bridge": SourceSpec(
        "SRC4256_05_4255_missing_bridge",
        SOURCE_DIR / "P8_Y5_R2FR_4255_MISSING_PHYSICAL_BRIDGE_LEDGER.csv",
        "MISSING_PHYSICAL_NORM_EQUIVALENCE",
        "4255 ledger proving the bridge is the current bottleneck.",
    ),
}


def common() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
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
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def append_claim() -> None:
    path = FORMAL / "02-claims-register.csv"
    text = read_text(path)
    if CLAIM_ID in text:
        return
    with path.open(newline="", encoding="utf-8") as handle:
        fieldnames = next(csv.reader(handle))
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": (
            "4256 derives the conditional Dq-projection spectral-gap bridge: if Pi_kerDq is a genuine "
            "projector onto ker(Dq) and Dq restricted to the Hperp complement has a positive local lower "
            "singular gap, then eta_Dq_kernel=0 and C_HDq=1/sigma_Dq_phys. The gap and component values "
            "remain unsigned, so this is nonclaim."
        ),
        "current_evidence": (
            "4256 source register, projection/gap theorem rows, 4254 component/constants candidates, "
            "bridge contract, decision and firewall."
        ),
        "status": "private_Dq_projection_gap_bridge_conditional_nonclaim",
        "next_test": (
            "Sign Pi_kerDq as a true kernel projector and prove/compute sigma_Dq_phys, then fill epsilon_i "
            "and epsilon_i_C1 or source the parent Pi4 Jacobian route."
        ),
        "key_risk": (
            "Using Pi_kerDq notation as if it were a physical closed-range projector would smuggle the local-GR "
            "suppression result."
        ),
    }
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


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
                "valid_for_claim": "False",
            }
        )
    return rows


def theorem_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DQP4256_0_kernel_zero",
            "projection kernel zero",
            "Let K=ker(Dq) and let P=Pi_kerDq be an idempotent projector with range K. Set M=(I-P)E. If h in M and Dq h=0, then h in M∩K={0}; hence ker(Dq|_M)=0 and eta_Dq_kernel=0 for the projected Hperp sector.",
            "DERIVED_CONDITIONAL",
            "Requires P^2=P, range(P)=ker(Dq), and Hperp in the selected complement M.",
        ),
        (
            "DQP4256_1_spectral_gap",
            "physical norm bridge",
            "Define sigma_0(U)=inf_{h in M_U, ||h||_F=1} ||Dq h||_W. If sigma_0(U)>0, then ||Hperp||_F/F_ref <= sigma_0(U)^-1 ||Dq[Hperp]||_W and C_HDq=sigma_0^-1.",
            "DERIVED_CONDITIONAL",
            "Positive gap follows from finite-dimensional compact bundle injectivity or an explicit closed-range/coercive estimate.",
        ),
        (
            "DQP4256_2_infinite_dimensional_guard",
            "closed range guard",
            "In an infinite-dimensional local field sector, injectivity alone is not enough; one needs closed range/coercivity, otherwise sigma_0 may be zero and no physical Hperp bound follows.",
            "NO_SMUGGLE_GUARD",
            "Prevents treating formal component naming as a physical norm theorem.",
        ),
        (
            "DQP4256_3_C1_bridge",
            "differentiated bridge",
            "If sigma_1(U)>0 for the differentiated complement and ||[Dq,nabla]Hperp||_W <= C_raw ||Hperp||_F/F_ref, then ||nabla Hperp||/(F_ref/L_U) <= sigma_1^-1 ||nabla Dq[Hperp]||_W + C_raw/(sigma_1 sigma_0)||Dq[Hperp]||_W.",
            "DERIVED_CONDITIONAL",
            "This maps C_HDq1=sigma_1^-1 and C_comm=C_raw/(sigma_1 sigma_0).",
        ),
        (
            "DQP4256_4_component_values",
            "component envelopes",
            "The theorem does not fill epsilon_i or epsilon_i_C1; those require zero proofs for each Dq_i[Hperp] or real profile/data envelopes.",
            "STILL_REQUIRED",
            "This is now the live numerical/profile socket for 4254.",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "name": name,
            "statement": statement,
            "status": status,
            "guard": guard,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, name, statement, status, guard in raw
    ]


def bridge_contract_rows() -> List[Dict[str, str]]:
    raw = [
        ("projector_idempotent", "P^2=P for P=Pi_kerDq", "UNSIGNED_PARENT_PROJECTOR_CERTIFICATE", "needed for M=(I-P)E"),
        ("projector_range", "range(P)=ker(Dq)", "UNSIGNED_PARENT_PROJECTOR_CERTIFICATE", "needed for eta_Dq_kernel=0"),
        ("projector_complement", "M∩ker(Dq)={0}", "DERIVED_IF_PROJECTOR_CERTIFIED", "gives no hidden Dq-kernel Hperp residue"),
        ("sigma_0_positive", "sigma_0(U)=inf ||Dq h||_W over ||h||_F=1, h in M_U is positive", "UNSIGNED_SPECTRAL_GAP_OR_COERCIVITY", "gives C_HDq=1/sigma_0"),
        ("sigma_1_positive", "sigma_1(U)>0 for differentiated complement", "UNSIGNED_C1_SPECTRAL_GAP", "gives C_HDq1=1/sigma_1"),
        ("commutator_bound", "||[Dq,nabla]Hperp||_W <= C_raw ||Hperp||_F/F_ref", "UNSIGNED_CONNECTION_BOUND", "gives C_comm=C_raw/(sigma_1 sigma_0)"),
        ("component_envelopes", "epsilon_i and epsilon_i_C1 for all eight Dq_i probes", "UNSIGNED_ZERO_PROOF_OR_PROFILE_VALUES", "feeds E_Dq,H and E_Dq,H_C1"),
    ]
    return [
        {
            **common(),
            "contract_id": contract_id,
            "requirement": requirement,
            "status": status,
            "feeds": feeds,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for contract_id, requirement, status, feeds in raw
    ]


def component_candidate_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for probe in PROBES:
        rows.append(
            {
                **common(),
                "candidate_id": CANDIDATE_ID,
                "probe_id": probe,
                "weight": "1.0",
                "epsilon": f"MISSING_ZERO_PROOF_OR_PROFILE_{probe}",
                "epsilon_C1": f"MISSING_C1_ZERO_PROOF_OR_PROFILE_{probe}",
                "source_path": str(FORMAL_PATH),
                "valid_for_claim": "False",
            }
        )
    return rows


def constant_candidate_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "candidate_id": CANDIDATE_ID,
            "C_S": "1.0",
            "C_perp": "MISSING_C_HDq_EQ_SIGMA0_INVERSE",
            "eta_domain": "MISSING_PROJECTOR_KERNEL_ZERO_CERT_OR_0",
            "C_S1": "1.0",
            "nabla_S_norm": "MISSING_C_RAW_COMMUTATOR_BOUND",
            "eta_C1": "MISSING_C1_KERNEL_ZERO_CERT_OR_0",
            "source_path": str(FORMAL_PATH),
            "valid_for_claim": "False",
        }
    ]


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4256_0_kernel_residue",
            "The Dq-kernel residue is not arbitrary anymore: eta_Dq_kernel is exactly zero if Pi_kerDq is a true kernel projector onto ker(Dq).",
            "This is the first real derivation step from the 4245 split toward local suppression.",
            "Sign the projector certificate.",
        ),
        (
            "DEC4256_1_physical_gap",
            "The remaining physical amplitude constant is C_HDq=1/sigma_0, not a free fitted fudge factor.",
            "The route now asks for a spectral gap/coercivity proof or computation.",
            NEXT_TARGET,
        ),
        (
            "DEC4256_2_4254_feed",
            "4254 candidate component and constant files are now present but deliberately nonnumeric/nonclaim.",
            "Rerunning 4254 should move from missing files to missing proofs/values.",
            "Do not convert placeholders into zeros.",
        ),
    ]
    return [
        {
            **common(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": "False",
        }
        for decision_id, decision, reason, next_action in raw
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4256_0_projector", "claiming eta_Dq_kernel=0 without P^2=P and range(P)=ker(Dq)", "PROJECTOR_CERTIFICATE_REQUIRED"),
        ("FW4256_1_gap", "claiming C_HDq finite without sigma_0>0 or coercivity", "SPECTRAL_GAP_REQUIRED"),
        ("FW4256_2_components", "setting epsilon_i=0 by convenience", "EIGHT_COMPONENT_ZERO_PROOFS_OR_PROFILES_REQUIRED"),
        ("FW4256_3_C1", "claiming C1 control without sigma_1 and commutator bound", "C1_GAP_AND_COMMUTATOR_REQUIRED"),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_move": forbidden,
            "required_gate": gate,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden, gate in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STATUS4256_0",
            "summary": (
                "4256 turns the Dq physical-bridge gap into a precise projector plus spectral-gap theorem: "
                "eta_Dq_kernel can be zero by construction, but only after Pi_kerDq is certified; C_HDq is "
                "1/sigma_0, and epsilons still require zero proofs or profiles."
            ),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "objective": (
                "Sign the Pi_kerDq projector certificate and derive/compute sigma_0, sigma_1, and C_raw, "
                "or fill the eight Dq component envelopes from zero proofs/profile data."
            ),
            "avoid": "Do not treat the Dq-coordinate identity or projector notation as a physical norm proof by itself.",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 272 - PPC4161 Dq projection spectral-gap bridge

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4256 does not prove local GR, PPN, R10, clock, orbital, or EM safety. It derives the exact contract under which the 4245 `Pi_kerDq` split becomes a physical suppression theorem.

## Projection-kernel lemma

Let `K=ker(Dq)` and let `P=Pi_kerDq`. If:

1. `P^2=P`,
2. `range(P)=K`,
3. `M=(I-P)E` is the selected `Hperp` complement,

then for `h in M`,

```text
Dq h=0 => h in K,
h in M and h in K => h=0.
```

So:

```text
ker(Dq|_M)=0,
eta_Dq_kernel=0.
```

This is the real use of the 4245 split. It is not yet a public claim because the parent/source-owned certificate for `P=Pi_kerDq` must still be signed.

## Physical norm bridge

Define:

```text
sigma_0(U_good)
  := inf_{{h in M_U, ||h||_F=1}} ||Dq h||_W.
```

If `sigma_0(U_good)>0`, then:

```text
||Hperp||_F/F_ref <= sigma_0(U_good)^-1 ||Dq[Hperp]||_W.
```

So:

```text
C_HDq = 1/sigma_0,
eta_Dq_kernel = 0.
```

Finite-dimensional compact-bundle route: if the residual local `Hperp` sector is finite-rank over compact `U_good`, and `Dq|_M` is continuous and injective, then `sigma_0>0` follows. Infinite-dimensional route: injectivity is not enough; a closed-range/coercive estimate is required.

## C1 bridge

Let:

```text
sigma_1(U_good)
  := inf_{{v in M1_U, ||v||_nabla=1}} ||Dq v||_W.
```

If `sigma_1>0` and:

```text
||[Dq,nabla]Hperp||_W <= C_raw ||Hperp||_F/F_ref,
```

then:

```text
||nabla Hperp||/(F_ref/L_U)
  <= sigma_1^-1 ||nabla Dq[Hperp]||_W
     + C_raw/(sigma_1 sigma_0) ||Dq[Hperp]||_W.
```

So:

```text
C_HDq1 = 1/sigma_1,
C_comm = C_raw/(sigma_1 sigma_0).
```

## 4254 feed

4256 writes nonclaim candidate files for 4254:

- `P8_Y5_R2FR_4254_DQ_COMPONENT_VALUES_CANDIDATE.csv`
- `P8_Y5_R2FR_4254_TOMOGRAPHY_CONSTANTS_CANDIDATE.csv`

They intentionally contain `MISSING_...` placeholders for `sigma_0`, `sigma_1`, `C_raw`, `epsilon_i`, and `epsilon_i_C1`. This should move 4254 from "missing files" to "missing signed proof/value rows".

## Next target

`{NEXT_TARGET}` should sign `Pi_kerDq` as a true kernel projector and prove/compute `sigma_0`, `sigma_1`, and `C_raw`, or fill the eight Dq component envelopes from zero proofs/profile data.
"""


def checkpoint_doc() -> str:
    return f"""
# 4256 - Y5 R2FR Dq projection spectral-gap bridge

Packet marker: `{PACKET_MARKER}`

## Result

The route now has an actual bridge theorem:

```text
P=Pi_kerDq true projector onto ker(Dq)
=> ker(Dq|_Hperp)=0
=> eta_Dq_kernel=0.
```

The physical amplitude constant is no longer vague:

```text
C_HDq = 1/sigma_0,
sigma_0 = inf_{{||h||_F=1, h in Hperp complement}} ||Dq h||_W.
```

## Still blocked

- `Pi_kerDq` must be source-signed as a genuine projector.
- `sigma_0>0` must be proved by finite-dimensional compactness or coercivity, or computed.
- `sigma_1` and the commutator bound must be proved for C1.
- All eight `epsilon_i` and `epsilon_i_C1` rows need zero proofs or profile/data envelopes.

## Claim status

Private nonclaim. This narrows the coupling/local-GR gap; it does not close it.
"""


def validation_rows(artifacts: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(artifacts["source_register"])
    theorems = csv_rows(artifacts["theorems"])
    contract = csv_rows(artifacts["bridge_contract"])
    components = csv_rows(artifacts["local_components"])
    constants = csv_rows(artifacts["local_constants"])
    rows = [
        ("VAL4256_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4256_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        ("VAL4256_2_kernel_theorem", any("eta_Dq_kernel=0" in row["statement"] for row in theorems), "kernel-zero theorem emitted"),
        ("VAL4256_3_gap_contract", any(row["contract_id"] == "sigma_0_positive" for row in contract), "sigma_0 contract emitted"),
        ("VAL4256_4_4254_components_written", COMPONENT_CANDIDATE_4254_PATH.exists(), "4254 component candidate path exists"),
        ("VAL4256_5_4254_constants_written", CONSTANT_CANDIDATE_4254_PATH.exists(), "4254 constants candidate path exists"),
        ("VAL4256_6_components_nonclaim", bool(components) and all(row["valid_for_claim"] == "False" for row in components), "component rows stay nonclaim"),
        ("VAL4256_7_constants_nonclaim", bool(constants) and all(row["valid_for_claim"] == "False" for row in constants), "constant rows stay nonclaim"),
        ("VAL4256_8_no_fake_epsilons", all(row["epsilon"].startswith("MISSING_") and row["epsilon_C1"].startswith("MISSING_") for row in components), "no epsilon zeros fabricated"),
        ("VAL4256_9_claim_row", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4256_10_formal_doc", MARKER in read_text(FORMAL_PATH), "formal doc marker present"),
        ("VAL4256_11_checkpoint_doc", PACKET_MARKER in read_text(DOC_PATH), "checkpoint doc marker present"),
    ]
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(bool(passed)),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in rows
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    source_path = SOURCE_DIR / "P8_Y5_R2FR_4256_SOURCE_REGISTER.csv"
    theorem_path = SOURCE_DIR / "P8_Y5_R2FR_4256_DQ_PROJECTION_GAP_THEOREMS.csv"
    contract_path = SOURCE_DIR / "P8_Y5_R2FR_4256_BRIDGE_CONTRACT.csv"
    decision_path = SOURCE_DIR / "P8_Y5_R2FR_4256_DECISION.csv"
    firewall_path = SOURCE_DIR / "P8_Y5_R2FR_4256_CLAIM_FIREWALL.csv"
    status_path = SOURCE_DIR / "P8_Y5_R2FR_4256_STATUS.csv"
    next_path = SOURCE_DIR / "P8_Y5_R2FR_4256_NEXT_TARGET.csv"

    components = component_candidate_rows()
    constants = constant_candidate_rows()

    write_csv(source_path, source_rows())
    write_csv(theorem_path, theorem_rows())
    write_csv(contract_path, bridge_contract_rows())
    write_csv(LOCAL_COMPONENT_PATH, components)
    write_csv(COMPONENT_CANDIDATE_4254_PATH, components)
    write_csv(LOCAL_CONSTANT_PATH, constants)
    write_csv(CONSTANT_CANDIDATE_4254_PATH, constants)
    write_csv(decision_path, decision_rows())
    write_csv(firewall_path, firewall_rows())
    write_csv(status_path, status_rows())
    write_csv(next_path, next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()

    artifacts = {
        "source_register": source_path,
        "theorems": theorem_path,
        "bridge_contract": contract_path,
        "local_components": LOCAL_COMPONENT_PATH,
        "local_constants": LOCAL_CONSTANT_PATH,
    }
    validation = validation_rows(artifacts)
    write_csv(VALIDATION_PATH, validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote 12 csv artifacts")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")


if __name__ == "__main__":
    main()
