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

CHECKPOINT = "4264"
CLAIM_ID = "L-105"
BRANCH = "MTS_R2FR_Y5_DQ_THETA_MARKER_COMPONENT_ZERO_OR_MARKER_BOUND_4264"
DECISION = "DQ_THETA_MARKER_ADOPTED_AS_CONDITIONAL_ZERO_FOR_CALIBRATED_QBASIC_VISIBLE_CONSTANT_BRANCH_MARKER_BOUND_FORK_RETAINED_NONCLAIM"
MARKER = "PPC4161_DQ_THETA_MARKER_COMPONENT_ZERO_OR_MARKER_BOUND_4264"
PACKET_MARKER = "PPC4161_PACKET_DQ_THETA_MARKER_COMPONENT_ZERO_OR_MARKER_BOUND_4264"
NEXT_TARGET = "4265-Y5-R2FR-Dq-matter-or-source-readout-component-zero.md"

FORMAL_PATH = FORMAL / "280-PPC4161-Dq-theta-marker-component-zero-or-marker-bound.md"
DOC_PATH = POST / "4264-Y5-R2FR-Dq-theta-marker-component-zero-or-marker-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4264_VALIDATION.csv"

LIVE_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4254_DQ_COMPONENT_VALUES_CANDIDATE.csv"
LOCAL_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4264_DQ_COMPONENT_VALUES_CANDIDATE.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
PROBE_ORDER = (
    "Dq_geom",
    "Dq_tau",
    "Dq_matter",
    "Dq_source_readout",
    "Dq_theta_marker",
    "Dq_boundary_projector",
    "Dq_EM",
    "Dq_coeff",
)


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4264_00_4177_quotient": SourceSpec(
        "SRC4264_00_4177_quotient",
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "D_v theta_A = D_v m_A = D_v alpha_EM = D_v source_normalization = 0",
        "Quotient-naturality theorem includes constants/material/source markers.",
    ),
    "SRC4264_01_4210_import": SourceSpec(
        "SRC4264_01_4210_import",
        FORMAL / "226-PPC4161-standard-visible-matter-import-contract.md",
        "calibrated/q-basic visible-sector readout constants",
        "Standard visible branch fixes theta_obs as calibrated q-basic data.",
    ),
    "SRC4264_02_4219_dq_contract": SourceSpec(
        "SRC4264_02_4219_dq_contract",
        FORMAL / "235-PPC4161-Dq-source-readout-coupling-marker-zero-or-bound.md",
        "Dq_theta_marker[v]=0",
        "Componentwise Dq zero contract includes theta marker row.",
    ),
    "SRC4264_03_2570_matter_descent": SourceSpec(
        "SRC4264_03_2570_matter_descent",
        SOURCE_DIR / "P8_Y5_FIELD_QUOTIENT_2570_MATTER_DESCENT_GATE.csv",
        "MD2570_0_chain_rule",
        "Matter descent chain rule with q-basic theta_obs.",
    ),
    "SRC4264_04_2643_theta_leak": SourceSpec(
        "SRC4264_04_2643_theta_leak",
        SOURCE_DIR / "P8_Y5_COMMON_DESCENT_DQZ_2643_DQZ_JH_LEAK_BOUND_ROWS.csv",
        "LEAK2643_4_theta_marker",
        "Existing theta/material marker leak bound row.",
    ),
    "SRC4264_05_4262_theorem": SourceSpec(
        "SRC4264_05_4262_theorem",
        SOURCE_DIR / "P8_Y5_R2FR_4262_READOUT_COUPLING_BRANCH_THEOREM.csv",
        "RCT4262_0_typed_constants",
        "4262 branch theorem fixes visible constants before variation.",
    ),
    "SRC4264_06_4262_formal": SourceSpec(
        "SRC4264_06_4262_formal",
        FORMAL / "278-PPC4161-visible-EM-readout-guard-or-charge-normalization-bound.md",
        "D_X theta_obs = 0",
        "4262 formal statement of calibrated theta derivative silence.",
    ),
    "SRC4264_07_4263_map": SourceSpec(
        "SRC4264_07_4263_map",
        SOURCE_DIR / "P8_Y5_R2FR_4263_EM_RESIDUAL_FINAL_BRANCH_MAP.csv",
        "b_A/b_marker",
        "4263 inherited material marker zero in the standard EM branch.",
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
            "4264 adopts Dq_theta_marker=0 and its C1 row as a private conditional component input for the "
            "standard calibrated q-basic visible branch. The result uses quotient-naturality, the 4210 visible "
            "matter import, and the 4262 typed-constant theorem: theta_obs, masses, charges, alpha_EM, hbar, c, "
            "clock standards and material labels are fixed before variation, so no hidden marker derivative or "
            "material/source-label slot exists. If MTS makes any constant, material label, environment marker or "
            "source normalization parent-field-dependent before variation, the marker bound fork reopens."
        ),
        "current_evidence": (
            "4264 source register, theta-marker theorem rows, marker-deformation bound rows, Dq_theta_marker "
            "adoption row, updated component candidate, decision and firewall."
        ),
        "status": "private_Dq_theta_marker_conditional_zero_adopted_for_calibrated_qbasic_branch_nonclaim",
        "next_test": "Attack Dq_matter or Dq_source_readout next; 4254 remains blocked by other components and tomography constants.",
        "key_risk": "Mistaking calibrated q-basic constants for a derivation of their numerical values, or hiding environment/material dependence as a readout label.",
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


def theta_marker_theorem_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "TMT4264_0_component_definition",
            "theta-marker component",
            "Dq_theta_marker measures whether masses, charges, alpha_EM, hbar, c, clock standards, material labels, source normalization or environment labels vary along the local representative/leakage direction.",
            "DEFINITION",
            "separates visible calibration from hidden marker dependence",
        ),
        (
            "TMT4264_1_qbasic_calibrated_zero",
            "q-basic calibrated constants zero",
            "In the 4210 standard branch theta_obs is fixed before variation; therefore D_X theta_obs=0 and Dq_theta_marker=0.",
            "CONDITIONAL_ZERO_IN_STANDARD_BRANCH",
            "does not predict the numerical constants",
        ),
        (
            "TMT4264_2_C1_zero",
            "marker C1 silence",
            "If theta_obs is fixed on the compact local collar and no environment/material marker gradient enters S_parent or S_eff, then nabla(Dq_theta_marker)=0.",
            "CONDITIONAL_C1_ZERO_IN_STANDARD_BRANCH",
            "fails for spatially varying material/environment/source labels",
        ),
        (
            "TMT4264_3_matter_descent_chain_rule",
            "matter descent chain rule",
            "For S_matter=Sbar[psi,e_obs(q),theta_obs] with q-basic theta_obs, delta_v S_matter contains no J_theta Lie_v(theta) term.",
            "EXACT_CONDITIONAL_CHAIN_RULE",
            "source-only prefactors remain a separate Dq_matter/source_readout gate",
        ),
        (
            "TMT4264_4_marker_deformation_bound",
            "marker deformation bound",
            "If any visible constant, material label, source normalization or environmental selector depends on parent hidden fields before variation, retain eps_theta_marker <= ||J_theta Lie_v theta||/||J_ref|| plus marker/readout tails.",
            "RETAINED_BOUND_FORK",
            "no cancellation with EM, WEP, clock, R10 or PPN rows",
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


def marker_bound_rows() -> List[Dict[str, str]]:
    raw = [
        ("MB4264_0_mass_marker", "D_X m_A", "body/source mass label varies with hidden parent field", "WEP;Newton;PPN;orbital"),
        ("MB4264_1_charge_alpha_marker", "D_X alpha_EM_or_charge", "charge/fine-structure label varies before variation", "clock;EM;R10;WEP"),
        ("MB4264_2_clock_marker", "D_X clock_standard", "clock/rod unit depends on hidden marker", "clock;PPN;R10;time"),
        ("MB4264_3_material_marker", "D_X material_label", "composition/material label becomes a source coefficient", "WEP;composition;clock"),
        ("MB4264_4_source_norm_marker", "D_X source_normalization", "measured source normalization changes before variation", "Newton;PPN;orbital;R10"),
        ("MB4264_5_environment_marker", "D_X environment_selector", "local environment/domain marker feeds matter constants", "PPN;clock;R10;WEP"),
    ]
    return [
        {
            **common(),
            "bound_id": bound_id,
            "coefficient": coefficient,
            "meaning": meaning,
            "observable_links": observable_links,
            "standard_branch_status": "0_if_theta_obs_qbasic_calibrated_before_variation",
            "deformation_branch_requirement": "MISSING_SOURCE_BACKED_BOUND_OR_ZERO_PROOF_IF_PARENT_DEPENDENT",
            "valid_for_claim": "False",
        }
        for bound_id, coefficient, meaning, observable_links in raw
    ]


def adoption_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "adoption_id": "ADOPT4264_Dq_theta_marker",
            "component": "Dq_theta_marker",
            "old_epsilon": "MISSING_ZERO_PROOF_OR_PROFILE_Dq_theta_marker",
            "new_epsilon": "0.0",
            "new_epsilon_C1": "0.0",
            "adoption_status": "ADOPTED_CONDITIONAL_ZERO_FOR_CALIBRATED_QBASIC_VISIBLE_BRANCH",
            "source_path": str(FORMAL_PATH),
            "conditions": (
                "theta_obs fixed before variation; calibrated q-basic constants; no hidden mass/charge/clock/material/source-normalization "
                "marker; no environment selector in S_parent or S_eff; no post-readout coefficient reentry"
            ),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def component_candidate_rows() -> List[Dict[str, str]]:
    previous = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
    if not previous:
        previous = [
            {
                **common(),
                "candidate_id": "DQ_COORDINATE_SEMINORM_SMOKE_4255",
                "probe_id": probe,
                "weight": "1.0",
                "epsilon": f"MISSING_ZERO_PROOF_OR_PROFILE_{probe}",
                "epsilon_C1": f"MISSING_C1_ZERO_PROOF_OR_PROFILE_{probe}",
                "source_path": str(FORMAL_PATH),
                "valid_for_claim": "False",
            }
            for probe in PROBE_ORDER
        ]
    output: List[Dict[str, str]] = []
    seen = set()
    for row in previous:
        probe = row.get("probe_id", "")
        if not probe:
            continue
        updated = dict(row)
        updated.update(common())
        if probe == "Dq_theta_marker":
            updated["epsilon"] = "0.0"
            updated["epsilon_C1"] = "0.0"
            updated["source_path"] = str(FORMAL_PATH)
            updated["valid_for_claim"] = "False"
        output.append(updated)
        seen.add(probe)
    for probe in PROBE_ORDER:
        if probe not in seen:
            output.append(
                {
                    **common(),
                    "candidate_id": "DQ_COORDINATE_SEMINORM_SMOKE_4255",
                    "probe_id": probe,
                    "weight": "1.0",
                    "epsilon": "0.0" if probe == "Dq_theta_marker" else f"MISSING_ZERO_PROOF_OR_PROFILE_{probe}",
                    "epsilon_C1": "0.0" if probe == "Dq_theta_marker" else f"MISSING_C1_ZERO_PROOF_OR_PROFILE_{probe}",
                    "source_path": str(FORMAL_PATH),
                    "valid_for_claim": "False",
                }
            )
    return output


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4264_0_adopt_theta_marker",
            "Adopt Dq_theta_marker=0 as a live conditional component candidate for the calibrated q-basic visible branch.",
            "This uses actual quotient/naturality and 4262 typed-constant logic rather than declaring constants derived.",
            NEXT_TARGET,
        ),
        (
            "DEC4264_1_marker_bound_fork",
            "If MTS makes constants or material/source markers parent-field-dependent, the marker bound fork reopens.",
            "That is where WEP, clock, R10, PPN and composition tests bite.",
            "Fill marker coefficient rows or prove no hidden marker object exists.",
        ),
        (
            "DEC4264_2_remaining_4254",
            "4254 remains blocked by other Dq components and tomography constants.",
            "This is still progress: another component row is no longer missing in the standard local branch.",
            "Attack Dq_matter or Dq_source_readout next.",
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
        ("FW4264_0_constant_prediction", "using calibrated theta_obs as a numerical derivation of masses, charges, alpha_EM, hbar or c", "PARENT_SCALE_LAW_REQUIRED"),
        ("FW4264_1_hidden_marker", "hiding composition/environment/source-normalization dependence inside a readout label", "MARKER_BOUND_ROW_REQUIRED"),
        ("FW4264_2_postfit_zero", "setting marker derivatives to zero after fitting rather than before variation by branch typing", "PREVARIATION_QBASIC_DECLARATION_REQUIRED"),
        ("FW4264_3_matter_prefactor", "using theta-marker zero to erase source-only matter prefactors", "DQ_MATTER_OR_SOURCE_READOUT_GATE_SEPARATE"),
        ("FW4264_4_claim_jump", "treating one component zero as full 4254 tomography/local-GR closure", "REMAINING_COMPONENTS_AND_CONSTANTS_REQUIRED"),
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
            "status_id": "STATUS4264_0",
            "summary": (
                "4264 moves Dq_theta_marker from missing to a conditional zero in the calibrated q-basic standard branch, "
                "while retaining explicit bound rows for any hidden material/source/environment marker dependence."
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
            "objective": "Attack Dq_matter or Dq_source_readout, because theta-marker silence does not by itself kill source-only matter prefactors or arena readout maps.",
            "avoid": "Do not use theta-marker zero to erase source weights, readout projectors, tau locks, coefficient owners or geometry rows.",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 280 - PPC4161 Dq-theta-marker component zero or marker bound

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4264 does not derive the numerical values of masses, charges, `alpha_EM`, `hbar`, `c`, material constants, source masses or `G_N`.

It adopts one component row:

```text
Dq_theta_marker = 0
```

only inside the standard calibrated q-basic visible branch.

## Component meaning

`Dq_theta_marker` measures hidden variation of:

```text
m_A,
charges,
alpha_EM,
hbar,
c,
clock standards,
material labels,
source normalization,
environment selectors.
```

The danger is not calibration. The danger is hidden parent-field dependence before variation.

## Branch theorem

In the 4210 branch:

```text
theta_obs = {{m_A, charges, alpha_EM, hbar, c, material labels}}
```

is calibrated/q-basic and fixed before variation.

From 4262:

```text
D_X theta_obs = 0.
```

From quotient naturality:

```text
S_matter = Sbar[psi, g_obs(q), theta_obs],
D_v theta_obs = 0,
Dq[v] = 0 on the theta-marker component.
```

Therefore:

```text
Dq_theta_marker = 0,
Dq_theta_marker_C1 = 0
```

for the standard local branch, provided no material/environment/source-normalization marker is inserted into `S_parent` or `S_eff`.

## Bound fork

If any of the following depends on hidden parent fields before variation:

```text
m_A(Phi),
alpha_EM(Phi),
charge labels(Phi),
clock standards(Phi),
material labels(Phi),
source normalization(Phi),
environment selectors(Phi),
```

then retain:

```text
eps_theta_marker
<= ||J_theta Lie_v theta||/||J_ref||
 + marker/source-label readout tails.
```

No cancellation with WEP, clock, R10, EM, PPN or source-normalization rows is allowed.

## 4254 feed

The live component candidate is updated:

```text
Dq_theta_marker = 0.0,
Dq_theta_marker_C1 = 0.0.
```

The row remains `valid_for_claim=false` because the complete 4254 source-probe/tomography gate still needs other Dq components and constants.

## Next target

`{NEXT_TARGET}` should attack `Dq_matter` or `Dq_source_readout`.
"""


def checkpoint_doc() -> str:
    return f"""
# 4264 - Y5 R2FR Dq-theta-marker component zero or marker bound

Packet marker: `{PACKET_MARKER}`

## Result

4264 adopts:

```text
Dq_theta_marker = 0.0,
Dq_theta_marker_C1 = 0.0
```

inside the calibrated q-basic standard visible branch.

If constants/material/source labels become parent-field-dependent before variation, the marker bound fork reopens.

## Claim status

Private nonclaim. Constants are imported/calibrated, not numerically derived.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    theorems = csv_rows(paths["theorems"])
    bounds = csv_rows(paths["bounds"])
    adoption = csv_rows(paths["adoption"])
    local_candidate = csv_rows(paths["local_candidate"])
    live_candidate = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
    live_theta = [row for row in live_candidate if row.get("probe_id") == "Dq_theta_marker"]
    live_em = [row for row in live_candidate if row.get("probe_id") == "Dq_EM"]
    rows = [
        ("VAL4264_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4264_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4264_2_theta_zero_theorem",
            any(row["status"] == "CONDITIONAL_ZERO_IN_STANDARD_BRANCH" for row in theorems),
            "theta-marker zero theorem emitted",
        ),
        (
            "VAL4264_3_marker_bounds",
            len(bounds) >= 6 and all(row["deformation_branch_requirement"].startswith("MISSING_SOURCE_BACKED") for row in bounds),
            "marker deformation bound rows emitted",
        ),
        (
            "VAL4264_4_adoption_row",
            bool(adoption)
            and adoption[0]["new_epsilon"] == "0.0"
            and adoption[0]["adoption_status"] == "ADOPTED_CONDITIONAL_ZERO_FOR_CALIBRATED_QBASIC_VISIBLE_BRANCH",
            "Dq_theta_marker adoption row emitted",
        ),
        (
            "VAL4264_5_local_candidate_numeric",
            any(row.get("probe_id") == "Dq_theta_marker" and row.get("epsilon") == "0.0" and row.get("epsilon_C1") == "0.0" for row in local_candidate),
            "local 4264 candidate has numeric theta-marker zero",
        ),
        (
            "VAL4264_6_live_4254_updated",
            bool(live_theta)
            and live_theta[0].get("epsilon") == "0.0"
            and live_theta[0].get("epsilon_C1") == "0.0"
            and live_theta[0].get("source_path") == str(FORMAL_PATH),
            "live 4254 candidate Dq_theta_marker updated",
        ),
        (
            "VAL4264_7_preserve_Dq_EM",
            bool(live_em) and live_em[0].get("epsilon") == "0.0" and live_em[0].get("epsilon_C1") == "0.0",
            "prior Dq_EM adoption preserved",
        ),
        ("VAL4264_8_claim_row", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4264_9_formal_doc", MARKER in read_text(FORMAL_PATH), "formal marker present"),
        ("VAL4264_10_checkpoint_doc", PACKET_MARKER in read_text(DOC_PATH), "checkpoint marker present"),
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
    source_path = SOURCE_DIR / "P8_Y5_R2FR_4264_SOURCE_REGISTER.csv"
    theorem_path = SOURCE_DIR / "P8_Y5_R2FR_4264_THETA_MARKER_THEOREM.csv"
    bound_path = SOURCE_DIR / "P8_Y5_R2FR_4264_MARKER_BOUND_ROWS.csv"
    adoption_path = SOURCE_DIR / "P8_Y5_R2FR_4264_DQ_THETA_MARKER_ADOPTION.csv"
    decision_path = SOURCE_DIR / "P8_Y5_R2FR_4264_DECISION.csv"
    firewall_path = SOURCE_DIR / "P8_Y5_R2FR_4264_CLAIM_FIREWALL.csv"
    status_path = SOURCE_DIR / "P8_Y5_R2FR_4264_STATUS.csv"
    next_path = SOURCE_DIR / "P8_Y5_R2FR_4264_NEXT_TARGET.csv"

    component_candidate = component_candidate_rows()
    write_csv(source_path, source_rows())
    write_csv(theorem_path, theta_marker_theorem_rows())
    write_csv(bound_path, marker_bound_rows())
    write_csv(adoption_path, adoption_rows())
    write_csv(LOCAL_COMPONENT_CANDIDATE_PATH, component_candidate)
    write_csv(LIVE_COMPONENT_CANDIDATE_PATH, component_candidate)
    write_csv(decision_path, decision_rows())
    write_csv(firewall_path, firewall_rows())
    write_csv(status_path, status_rows())
    write_csv(next_path, next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()

    paths = {
        "sources": source_path,
        "theorems": theorem_path,
        "bounds": bound_path,
        "adoption": adoption_path,
        "local_candidate": LOCAL_COMPONENT_CANDIDATE_PATH,
    }
    validation = validation_rows(paths)
    write_csv(VALIDATION_PATH, validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote 8 csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")


if __name__ == "__main__":
    main()
