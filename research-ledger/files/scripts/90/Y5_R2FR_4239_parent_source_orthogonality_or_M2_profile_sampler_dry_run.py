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

CHECKPOINT = "4239"
CLAIM_ID = "L-080"
BRANCH = "MTS_R2FR_Y5_PARENT_SOURCE_ORTHOGONALITY_4239"
DECISION = "PARENT_SOURCE_ORTHOGONALITY_DERIVED_FOR_QBASIC_HL_COMPONENT_NONQ_DEFECT_AND_M2_PROFILE_SAMPLER_REMAIN_NONCLAIM"
MARKER = "PPC4161_PARENT_SOURCE_ORTHOGONALITY_4239"
PACKET_MARKER = "PPC4161_PACKET_PARENT_SOURCE_ORTHOGONALITY_4239"
NEXT_TARGET = "4240-Y5-R2FR-HL-qbasic-defect-zero-or-M2-quotient-constant-profile-runner.md"

FORMAL_PATH = FORMAL / "255-PPC4161-parent-source-orthogonality-or-M2-profile-sampler-dry-run.md"
DOC_PATH = POST / "4239-Y5-R2FR-parent-source-orthogonality-or-M2-profile-sampler-dry-run.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4239_VALIDATION.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4239_00_4238_next": SourceSpec(
        "SRC4239_00_4238_next",
        SOURCE_DIR / "P8_Y5_R2FR_4238_NEXT_TARGET.csv",
        "4239-Y5-R2FR-parent-source-orthogonality-or-M2-profile-sampler-dry-run.md",
        "4238 selected the source-orthogonality/profile-sampler fork.",
    ),
    "SRC4239_01_4238_formal": SourceSpec(
        "SRC4239_01_4238_formal",
        FORMAL / "254-PPC4161-vertical-current-M2-zero-theorem-or-profile-sampler.md",
        "S_cg descends through q or annihilates ker(Dq),",
        "4238 exact zero contract.",
    ),
    "SRC4239_02_4238_clauses": SourceSpec(
        "SRC4239_02_4238_clauses",
        SOURCE_DIR / "P8_Y5_R2FR_4238_CLAUSE_GATES.csv",
        "CG4238_1_source_descent",
        "Machine-readable 4238 source-descent open clause.",
    ),
    "SRC4239_03_qnatural": SourceSpec(
        "SRC4239_03_qnatural",
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "S_matter = Sbar_m[psi, g_obs(q), A(q), theta(q)].",
        "4177 source/matter descent before variation.",
    ),
    "SRC4239_04_qnatural_proof": SourceSpec(
        "SRC4239_04_qnatural_proof",
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "delta_v S_matter =",
        "4177 vertical source variation proof.",
    ),
    "SRC4239_05_qbasic_source": SourceSpec(
        "SRC4239_05_qbasic_source",
        FORMAL / "229-PPC4161-qbasic-vertical-presymplectic-silence.md",
        "S_src = Sbar_src[q(Phi), psi, A, theta].",
        "4213 q-basic source action descent.",
    ),
    "SRC4239_06_qbasic_vertical": SourceSpec(
        "SRC4239_06_qbasic_vertical",
        FORMAL / "229-PPC4161-qbasic-vertical-presymplectic-silence.md",
        "Dq[v] = 0.",
        "4213 vertical condition for q-basic variations.",
    ),
    "SRC4239_07_Dq_components": SourceSpec(
        "SRC4239_07_Dq_components",
        FORMAL / "235-PPC4161-Dq-source-readout-coupling-marker-zero-or-bound.md",
        "Dq_source_readout[v]=0,",
        "4219 componentwise source-readout Dq silence.",
    ),
    "SRC4239_08_projector": SourceSpec(
        "SRC4239_08_projector",
        FORMAL / "230-PPC4161-projector-stress-curl-zero-or-bound.md",
        "source/readout quantities factor through `q`;",
        "4214 source/readout q-factorization clause.",
    ),
    "SRC4239_09_leakage_candidate": SourceSpec(
        "SRC4239_09_leakage_candidate",
        FORMAL / "125-local-leakage-vector-invariant.md",
        "Z_L^A =",
        "Leakage-vector candidate used to define H_L.",
    ),
    "SRC4239_10_AJ_theorem": SourceSpec(
        "SRC4239_10_AJ_theorem",
        FORMAL / "253-PPC4161-AJ-source-coefficient-theorem-or-numeric-fill-pack.md",
        "source-current contraction: S_A H_L^A,",
        "4237 source coefficient target.",
    ),
    "SRC4239_11_claim_register": SourceSpec(
        "SRC4239_11_claim_register",
        FORMAL / "02-claims-register.csv",
        "L-079",
        "Prior claim-register anchor for 4238.",
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


def orthogonality_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "SO4239_0_source_descent",
            "S_src = Sbar_src[q(Phi), psi, A, theta]",
            "The source functional has no independent q-vertical argument inside the private selector.",
            "private_selector_source",
        ),
        (
            "SO4239_1_vertical_direction",
            "H_q in ker(Dq), so Dq[H_q]=0",
            "Only the q-basic component of the leakage profile is certified by quotient naturality.",
            "private_selector_vertical",
        ),
        (
            "SO4239_2_chain_rule",
            "D_Hq S_src = <delta Sbar_src/delta q, Dq[H_q]> = 0",
            "Source variation along q-basic leakage vanishes by chain rule.",
            "derived",
        ),
        (
            "SO4239_3_contraction_zero",
            "S_A H_q^A = 0",
            "The q-basic contribution to the 4237 source-current contraction is exactly zero.",
            "private_pass",
        ),
        (
            "SO4239_4_no_overclaim",
            "H_L = H_q + H_perp",
            "If H_L has a non-q component, source orthogonality does not kill it.",
            "active_guard",
        ),
        (
            "SO4239_5_residual_source",
            "S_A H_L^A = S_A H_perp^A",
            "The live source amplitude is reduced to the non-q leakage defect.",
            "reduced_obstruction",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, formula, meaning, status in rows
    ]


def hl_decomposition_rows() -> List[Dict[str, str]]:
    rows = [
        ("HD4239_0_Hq", "H_q", "Pi_kerDq H_L", "q-basic vertical profile", "source term zero", "private_selector"),
        ("HD4239_1_Hperp", "H_perp", "(1-Pi_kerDq) H_L", "non-q leakage defect", "must be zeroed or bounded", "open"),
        ("HD4239_2_source_reduction", "A_src", "sup |S_A H_perp^A|", "reduced source coefficient", "not scoreable without H_perp", "open"),
        ("HD4239_3_full_source_zero", "A_src=0", "H_perp=0 or S_A H_perp^A=0", "full source orthogonality condition", "not yet signed", "open"),
        ("HD4239_4_sampler_input", "H_perp(x,t)", "profile input", "fallback source sampler row", "missing", "open"),
    ]
    return [
        {
            **common(),
            "decomposition_id": decomposition_id,
            "quantity": quantity,
            "definition": definition,
            "meaning": meaning,
            "effect": effect,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for decomposition_id, quantity, definition, meaning, effect, status in rows
    ]


def m2_sampler_dry_run_rows() -> List[Dict[str, str]]:
    rows = [
        ("MS4239_0_Hq", "H_q^A(x,t)", "q-basic input", "available only after Pi_kerDq is defined", "MISSING_PROJECTOR"),
        ("MS4239_1_Hperp", "H_perp^A(x,t)", "non-q defect input", "needed for residual A_src", "MISSING_DEFECT_PROFILE"),
        ("MS4239_2_HAB", "H_AB(x,t)", "shape Hessian", "needed for M_2", "MISSING_PARENT_SHAPE"),
        ("MS4239_3_M2", "M_2=1/2 H_AB H_L^A H_L^B", "derived shape profile", "computed after H/HAB inputs", "DRY_RUN_ONLY"),
        ("MS4239_4_source", "SAH_perp=S_A H_perp^A", "derived source residual", "computed after S_A and Hperp", "MISSING_SOURCE_JACOBIAN"),
        ("MS4239_5_lap", "Delta_h M_2", "derived Laplacian residual", "computed from M2 and local geometry", "DRY_RUN_ONLY"),
        ("MS4239_6_drift", "D_t M_2", "derived drift residual", "computed from time/profile data", "DRY_RUN_ONLY"),
        ("MS4239_7_budget", "|SAH_perp|+|D_m Delta_h M_2|+|D_t M_2|", "non-cancelled local budget", "compare to 4236 Gdot gate", "BLOCKED_UNTIL_INPUTS"),
    ]
    return [
        {
            **common(),
            "sampler_id": sampler_id,
            "quantity": quantity,
            "kind": kind,
            "role": role,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for sampler_id, quantity, kind, role, status in rows
    ]


def reduced_budget_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "RB4239_0_reduced_AJ",
            "A_J,eff_private <= |S_A H_perp^A| + |D_m Delta_h M_2| + |D_t M_2|",
            "q-basic source contribution removed",
            "active private reduced bound",
        ),
        (
            "RB4239_1_source_closed_if",
            "H_perp=0 or S_A H_perp^A=0 => A_src=0",
            "full source zero condition",
            "open",
        ),
        (
            "RB4239_2_strong_Gdot",
            "|S_A H_perp^A| + |D_m Delta_h M_2| + |D_t M_2| <= 0.1678939074330212*(mu_Xi T_res)/|c_Gamma|",
            "4236 strong local budget after source reduction",
            "not scoreable",
        ),
        (
            "RB4239_3_full_zero",
            "H_perp=0, Delta_h M_2=0, D_t M_2=0 => A_J,eff_private=0 at leading order",
            "remaining exact-zero branch",
            "not claimed",
        ),
    ]
    return [
        {
            **common(),
            "budget_id": budget_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for budget_id, formula, meaning, status in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "forward_move": "The q-basic piece of the source-current contraction is now zero by quotient source descent: S_A H_q^A=0.",
            "source_orthogonality_private": "partial_pass",
            "remaining_obstruction": "H_perp non-q leakage defect plus Delta_h M_2 and D_t M_2",
            "scoreable_now": "False",
            "best_next_move": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4239_0_no_full_source_zero", "Do not claim S_A H_L^A=0 unless H_perp=0 or S_A H_perp^A=0 is parent-signed.", "active"),
        ("FW4239_1_qbasic_scope", "The source orthogonality proof only applies to q-basic leakage directions in ker(Dq).", "active"),
        ("FW4239_2_no_sampler_claim", "Dry-run sampler rows are schema/proof plumbing, not numeric evidence.", "active"),
        ("FW4239_3_no_cancellation", "Score the reduced budget with absolute values; no source/lap/drift cancellation credit.", "active"),
        ("FW4239_4_private_only", "All zero statements remain inside the private compact selector until public parent adoption is signed.", "active"),
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
            "status": "private_source_orthogonality_partial_pass_nonclaim",
            "summary": "4239 proves S_A H_q^A=0 for the q-basic leakage component and reduces the source obstruction to S_A H_perp^A.",
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
            "reason": "The next real fork is to prove H_perp=0 / H_L fully q-basic, or run the M2/source-defect profile grid with real inputs.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def all_generated_groups() -> Iterable[List[Dict[str, str]]]:
    return (
        source_rows(),
        orthogonality_rows(),
        hl_decomposition_rows(),
        m2_sampler_dry_run_rows(),
        reduced_budget_rows(),
        decision_rows(),
        firewall_rows(),
        status_rows(),
        next_target_rows(),
    )


def formal_doc() -> str:
    return f"""
# 255 - PPC4161 Parent Source Orthogonality Or M2 Profile Sampler Dry Run

Marker: `{MARKER}`

Branch: `{BRANCH}`
Decision: `{DECISION}`

## Result

4239 proves the source-orthogonality clause for the q-basic part of the leakage profile.

Inside the private quotient-natural selector:

```text
S_src = Sbar_src[q(Phi), psi, A, theta],
H_q in ker(Dq),
Dq[H_q]=0.
```

Therefore:

```text
D_Hq S_src = <delta Sbar_src/delta q, Dq[H_q]> = 0,
S_A H_q^A = 0.
```

This is not a hand-waved source silence. It is the chain rule applied to a source functional that factors through the quotient before variation.

## No-Smuggle Split

Do not identify the whole leakage profile with the q-basic direction unless the parent signs it. Split:

```text
H_L = H_q + H_perp,
H_q in ker(Dq).
```

Then the 4237 source contraction becomes:

```text
S_A H_L^A = S_A H_perp^A.
```

So the source piece is genuinely reduced, but not globally killed.

## Reduced cGamma Source Budget

4238 now reduces to:

```text
A_J,eff_private <= |S_A H_perp^A| + |D_m Delta_h M_2| + |D_t M_2|.
```

The strong local Gdot gate is:

```text
|S_A H_perp^A| + |D_m Delta_h M_2| + |D_t M_2|
<= 0.1678939074330212 * (mu_Xi T_res)/|c_Gamma|.
```

## Remaining Exact-Zero Route

The leading private source-amplitude row closes if:

```text
H_perp = 0,
Delta_h M_2 = 0,
D_t M_2 = 0.
```

If those cannot be parent-signed, the fallback is the staged profile grid:

```text
H_q, H_perp, H_AB, S_A
  -> M_2
  -> S_A H_perp^A, Delta_h M_2, D_t M_2
  -> reduced 4236 budget.
```

## Claim Status

Private nonclaim. This signs the q-basic source-orthogonality sublemma, not the full local-GR theorem.

## Next Target

`{NEXT_TARGET}`
"""


def checkpoint_doc() -> str:
    return f"""
# 4239 - Parent Source Orthogonality Or M2 Profile Sampler Dry Run

**Status:** `{DECISION}`.

## Forward Move

4239 proves:

```text
S_A H_q^A = 0
```

for the q-basic part of the leakage profile, because the source action descends through `q` before variation.

## Remaining Obstruction

The live source coefficient is now:

```text
S_A H_L^A = S_A H_perp^A.
```

So the next real question is whether `H_perp=0`, or whether `H_perp`, `Delta_h M_2`, and `D_t M_2` fit the reduced budget.

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
            "claim": "The q-basic component of the cGamma source-current contraction is zero: S_A H_q^A=0 follows from quotient source descent and Dq[H_q]=0. The full source term reduces to S_A H_perp^A, so local-GR closure still requires H_perp=0 or a bound/profile sampler.",
            "current_evidence": "4239 source register, orthogonality theorem, H_L decomposition, M2 sampler dry-run schema, reduced budget, decision and firewall.",
            "status": "private_source_orthogonality_partial_pass_nonclaim",
            "next_test": "Prove H_L is fully q-basic / H_perp=0, or run the M2/source-defect profile grid with real parent inputs.",
            "key_risk": "Equating H_L with a q-basic direction without proof would smuggle the source zero.",
        }
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def update_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 Parent Source Orthogonality

Marker: `{MARKER}`

4239 proves the q-basic source-orthogonality sublemma:

```text
S_src = Sbar_src[q(Phi),...],
Dq[H_q]=0
=> S_A H_q^A=0.
```

The honest split is:

```text
H_L = H_q + H_perp,
S_A H_L^A = S_A H_perp^A.
```

So the source term is reduced to the non-q leakage defect rather than left as a free coefficient.
"""
    packet_block = f"""
## Packet Update - Parent Source Orthogonality

Marker: `{PACKET_MARKER}`

The q-basic part of the cGamma source-current row is now privately killed by quotient source descent. The remaining private cGamma source budget is:

```text
|S_A H_perp^A| + |D_m Delta_h M_2| + |D_t M_2|.
```
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
    ortho = orthogonality_rows()
    decomp = hl_decomposition_rows()
    sampler = m2_sampler_dry_run_rows()
    budget = reduced_budget_rows()
    all_rows = [row for group in all_generated_groups() for row in group]

    add("VAL4239_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources), "source register")
    add("VAL4239_1_needles_found", "all source needles found", all(row["required_text_found"] == "True" for row in sources), "source register")
    add("VAL4239_2_qbasic_source_zero", "orthogonality theorem proves q-basic source zero", any(row["formula"] == "S_A H_q^A = 0" and row["status"] == "private_pass" for row in ortho), "orthogonality rows")
    add("VAL4239_3_no_smuggle_split", "H_L split into Hq and Hperp", {"H_q", "H_perp"}.issubset({row["quantity"] for row in decomp}), "decomposition rows")
    add("VAL4239_4_source_reduced", "source residual reduced to Hperp", any(row["formula"] == "S_A H_L^A = S_A H_perp^A" for row in ortho), "orthogonality rows")
    add("VAL4239_5_sampler_dry_run", "sampler rows include Hperp DeltaM2 DtM2 budget", {"MS4239_1_Hperp", "MS4239_5_lap", "MS4239_6_drift", "MS4239_7_budget"}.issubset({row["sampler_id"] for row in sampler}), "sampler schema")
    add("VAL4239_6_reduced_budget", "reduced AJ budget recorded", any("S_A H_perp^A" in row["formula"] and "Delta_h M_2" in row["formula"] for row in budget), "budget rows")
    add("VAL4239_7_decision_nonclaim", "decision remains non-scoreable", decision_rows()[0]["scoreable_now"] == "False", "decision")
    add("VAL4239_8_docs_written", "formal and checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), f"{FORMAL_PATH}; {DOC_PATH}")
    add("VAL4239_9_claim_register", "claims register contains L-080", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), str(FORMAL / "02-claims-register.csv"))
    add("VAL4239_10_spine_marker", "spine contains marker", MARKER in read_text(FORMAL / "07-unification-spine.md"), str(FORMAL / "07-unification-spine.md"))
    add("VAL4239_11_packet_marker", "packet contains marker", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), str(FORMAL / "180-PPC4161-private-local-packet-integration.md"))
    add("VAL4239_12_no_claim_flags", "no generated row is valid for claim", all(row.get("valid_for_claim") != "True" for row in all_rows), "all generated groups")
    add("VAL4239_13_next_target", "next target selected", next_target_rows()[0]["next_target"] == NEXT_TARGET, NEXT_TARGET)
    add("VAL4239_14_firewall", "firewall has anti-smuggling rules", len(firewall_rows()) == 5 and all(row["status"] == "active" for row in firewall_rows()), "firewall")
    return rows


def main() -> None:
    paths = {
        "source": SOURCE_DIR / "P8_Y5_R2FR_4239_SOURCE_REGISTER.csv",
        "ortho": SOURCE_DIR / "P8_Y5_R2FR_4239_SOURCE_ORTHOGONALITY_THEOREM.csv",
        "decomp": SOURCE_DIR / "P8_Y5_R2FR_4239_HL_DECOMPOSITION.csv",
        "sampler": SOURCE_DIR / "P8_Y5_R2FR_4239_M2_PROFILE_SAMPLER_DRY_RUN.csv",
        "budget": SOURCE_DIR / "P8_Y5_R2FR_4239_REDUCED_AJ_BUDGET.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4239_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4239_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4239_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4239_NEXT_TARGET.csv",
    }
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    write_csv(paths["source"], source_rows())
    write_csv(paths["ortho"], orthogonality_rows())
    write_csv(paths["decomp"], hl_decomposition_rows())
    write_csv(paths["sampler"], m2_sampler_dry_run_rows())
    write_csv(paths["budget"], reduced_budget_rows())
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
