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

CHECKPOINT = "4265"
CLAIM_ID = "L-106"
BRANCH = "MTS_R2FR_Y5_DQ_MATTER_ACTION_DOMAIN_ZERO_OR_SOURCE_PREFACTOR_BOUND_4265"
DECISION = "DQ_MATTER_ACTION_DOMAIN_ADOPTED_AS_CONDITIONAL_ZERO_SOURCE_WEIGHT_AND_READOUT_PREFACTORS_RETAINED_NONCLAIM"
MARKER = "PPC4161_DQ_MATTER_ACTION_DOMAIN_ZERO_OR_SOURCE_PREFACTOR_BOUND_4265"
PACKET_MARKER = "PPC4161_PACKET_DQ_MATTER_ACTION_DOMAIN_ZERO_OR_SOURCE_PREFACTOR_BOUND_4265"
NEXT_TARGET = "4266-Y5-R2FR-Dq-source-readout-or-coefficient-prefactor-zero.md"

FORMAL_PATH = FORMAL / "281-PPC4161-Dq-matter-action-domain-zero-or-source-prefactor-bound.md"
DOC_PATH = POST / "4265-Y5-R2FR-Dq-matter-action-domain-zero-or-source-prefactor-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4265_VALIDATION.csv"

LIVE_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4254_DQ_COMPONENT_VALUES_CANDIDATE.csv"
LOCAL_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4265_DQ_COMPONENT_VALUES_CANDIDATE.csv"

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
    "SRC4265_00_4177_quotient": SourceSpec(
        "SRC4265_00_4177_quotient",
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "S_matter = Sbar_m[psi, g_obs(q), A(q), theta(q)].",
        "Quotient naturality matter-action descent theorem.",
    ),
    "SRC4265_01_4210_visible": SourceSpec(
        "SRC4265_01_4210_visible",
        FORMAL / "226-PPC4161-standard-visible-matter-import-contract.md",
        "S_matter[psi,g_obs,theta_obs]",
        "Standard visible matter import uses one observed metric and theta_obs.",
    ),
    "SRC4265_02_4219_dq_contract": SourceSpec(
        "SRC4265_02_4219_dq_contract",
        FORMAL / "235-PPC4161-Dq-source-readout-coupling-marker-zero-or-bound.md",
        "Dq_matter[v]=0",
        "Componentwise Dq zero contract includes matter row.",
    ),
    "SRC4265_03_2570_signature": SourceSpec(
        "SRC4265_03_2570_signature",
        SOURCE_DIR / "P8_Y5_FIELD_QUOTIENT_2570_FIELD_SIGNATURE_ATTEMPT.csv",
        "FSIG2570_1_ordinary_matter",
        "Ordinary matter descends through public geometry in source hierarchy.",
    ),
    "SRC4265_04_2570_matter_gate": SourceSpec(
        "SRC4265_04_2570_matter_gate",
        SOURCE_DIR / "P8_Y5_FIELD_QUOTIENT_2570_MATTER_DESCENT_GATE.csv",
        "MD2570_0_chain_rule",
        "Exact conditional chain-rule theorem for ordinary matter descent.",
    ),
    "SRC4265_05_2643_leak_rows": SourceSpec(
        "SRC4265_05_2643_leak_rows",
        SOURCE_DIR / "P8_Y5_COMMON_DESCENT_DQZ_2643_DQZ_JH_LEAK_BOUND_ROWS.csv",
        "LEAK2643_3_source_weight_seam",
        "Source-weight countermodel stays retained after matter-domain closure.",
    ),
    "SRC4265_06_4264_theorem": SourceSpec(
        "SRC4265_06_4264_theorem",
        SOURCE_DIR / "P8_Y5_R2FR_4264_THETA_MARKER_THEOREM.csv",
        "TMT4264_3_matter_descent_chain_rule",
        "4264 already closed theta-marker leg of matter chain rule.",
    ),
    "SRC4265_07_4264_formal": SourceSpec(
        "SRC4265_07_4264_formal",
        SOURCE_DIR / "P8_Y5_R2FR_4264_THETA_MARKER_THEOREM.csv",
        "source-only prefactors remain a separate Dq_matter/source_readout gate",
        "4264 firewall preventing source-prefactor shortcut.",
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
            "4265 adopts Dq_matter=0 and its C1 row only for the ordinary matter action-domain part of the "
            "standard local branch: S_matter[psi,g_obs,theta_obs] factors through the observed metric/coframe and "
            "the q-basic theta markers already closed by 4264. Source-only species weights, measured-source maps, "
            "worldtube/projector readouts and coefficient owners are not erased; they remain in Dq_source_readout, "
            "Dq_coeff, boundary/projector and tomography constants."
        ),
        "current_evidence": (
            "4265 source register, matter-domain theorem rows, source-prefactor split rows, Dq_matter adoption row, "
            "updated component candidate, decision and firewall."
        ),
        "status": "private_Dq_matter_action_domain_conditional_zero_adopted_source_prefactors_retained_nonclaim",
        "next_test": "Attack Dq_source_readout or Dq_coeff next; 4254 remains blocked by those rows plus geometry/tau/boundary/constants.",
        "key_risk": "Using matter action-domain descent to hide WEP/source-weight or measured-mass readout prefactors.",
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


def matter_theorem_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "MAT4265_0_action_domain",
            "ordinary matter action-domain component",
            "Dq_matter here means direct hidden/representative dependence in S_matter beyond psi, g_obs and theta_obs.",
            "DEFINITION_SPLIT",
            "source weights and readout projectors are assigned to other live components",
        ),
        (
            "MAT4265_1_chain_rule_zero",
            "matter descent chain-rule zero",
            "If S_matter=Sbar[psi,g_obs(q),theta_obs] and theta_obs is fixed as in 4264, then delta_v S_matter has no direct Dq_matter term.",
            "CONDITIONAL_ZERO_IN_STANDARD_BRANCH",
            "does not erase source-only prefactors",
        ),
        (
            "MAT4265_2_C1_zero",
            "matter C1 silence",
            "If the matter action-domain is the same on the compact collar and no hidden environment/matter field enters before variation, then nabla(Dq_matter)=0.",
            "CONDITIONAL_C1_ZERO_IN_STANDARD_BRANCH",
            "fails for spatially varying direct matter couplings",
        ),
        (
            "MAT4265_3_prefactor_split",
            "source-prefactor split",
            "Terms of the form w_A(Phi) S_A, measured-source maps, worldtube projectors and coefficient normalizations are not part of the closed Dq_matter row; they remain in Dq_source_readout, Dq_coeff or boundary/projector rows.",
            "NO_SMUGGLE_SPLIT",
            "protects WEP and measured-G/GM tests",
        ),
        (
            "MAT4265_4_deformation_bound",
            "direct matter deformation bound",
            "If S_matter contains hidden direct couplings before variation, retain epsilon_matter_direct <= ||delta_v S_matter_direct||/M_H_ref plus no-cancellation source/readout tails.",
            "RETAINED_BOUND_FORK",
            "requires numeric/source-backed coefficient rows if reopened",
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


def prefactor_split_rows() -> List[Dict[str, str]]:
    raw = [
        ("SPL4265_0_species_weight", "Delta_w_species_A", "pre-variation species/source action weight", "Dq_source_readout_or_Dq_coeff"),
        ("SPL4265_1_source_worldtube", "Delta_worldtube_domain", "measured source/worldtube selector changes source before variation", "Dq_source_readout_or_Dq_boundary_projector"),
        ("SPL4265_2_measured_mass_map", "Pi_M_readout_tail", "Hamiltonian/source charge to measured mass map reenters source", "Dq_source_readout"),
        ("SPL4265_3_coupling_scale", "e_kappaG_or_ellJ_owner", "coupling/source-current scale owner is not fixed", "Dq_coeff_or_tomography_constants"),
        ("SPL4265_4_direct_matter_hidden", "epsilon_matter_direct", "direct hidden matter operator inside S_matter before variation", "Dq_matter_bound_if_present"),
    ]
    return [
        {
            **common(),
            "split_id": split_id,
            "coefficient": coefficient,
            "meaning": meaning,
            "assigned_live_gate": assigned_gate,
            "standard_branch_status": "0_for_Dq_matter_action_domain" if assigned_gate == "Dq_matter_bound_if_present" else "retained_not_closed_by_Dq_matter",
            "deformation_requirement": "MISSING_SOURCE_BACKED_BOUND_OR_ZERO_PROOF_IF_PRESENT",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for split_id, coefficient, meaning, assigned_gate in raw
    ]


def adoption_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "adoption_id": "ADOPT4265_Dq_matter",
            "component": "Dq_matter",
            "old_epsilon": "MISSING_ZERO_PROOF_OR_PROFILE_Dq_matter",
            "new_epsilon": "0.0",
            "new_epsilon_C1": "0.0",
            "adoption_status": "ADOPTED_CONDITIONAL_ZERO_FOR_STANDARD_MATTER_ACTION_DOMAIN_ONLY",
            "source_path": str(FORMAL_PATH),
            "conditions": (
                "S_matter factors through psi, g_obs and theta_obs before variation; theta_obs fixed by 4264; "
                "no direct hidden matter operator; source-only weights/readout projectors/coefficient owners stay in other live gates"
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
        if probe == "Dq_matter":
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
                    "epsilon": "0.0" if probe == "Dq_matter" else f"MISSING_ZERO_PROOF_OR_PROFILE_{probe}",
                    "epsilon_C1": "0.0" if probe == "Dq_matter" else f"MISSING_C1_ZERO_PROOF_OR_PROFILE_{probe}",
                    "source_path": str(FORMAL_PATH),
                    "valid_for_claim": "False",
                }
            )
    return output


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4265_0_adopt_matter_domain",
            "Adopt Dq_matter=0 for the standard ordinary matter action-domain only.",
            "The ordinary matter Lagrangian descends through g_obs and theta_obs; 4264 already closed theta marker leakage.",
            NEXT_TARGET,
        ),
        (
            "DEC4265_1_retain_source_prefactors",
            "Species/source weights, measured-source maps and coefficient owners remain live.",
            "This prevents WEP, measured-GM and source-normalization shortcuts.",
            "Attack Dq_source_readout or Dq_coeff next.",
        ),
        (
            "DEC4265_2_4254_progress",
            "4254 should now lose Dq_matter from the missing list while staying blocked by honest remaining rows.",
            "That is real narrowing of the Hperp/Dq problem.",
            "Rerun 4254 after 4265.",
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
        ("FW4265_0_wep_shortcut", "using Dq_matter zero to remove relative species/source weights", "DQ_SOURCE_READOUT_OR_DQ_COEFF_REQUIRED"),
        ("FW4265_1_mass_readout_shortcut", "using matter descent to identify Hilbert charge with measured GM/worldtube mass", "SOURCE_READOUT_GATE_REQUIRED"),
        ("FW4265_2_hidden_operator", "hiding direct hidden matter operators inside S_matter", "DIRECT_MATTER_BOUND_REQUIRED"),
        ("FW4265_3_theta_reentry", "letting material constants reenter after 4264 via matter labels", "THETA_MARKER_BOUND_REQUIRED"),
        ("FW4265_4_claim_jump", "treating Dq_matter zero as local-GR/PPN/WEP pass", "REMAINING_COMPONENTS_AND_TOMOGRAPHY_REQUIRED"),
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
            "status_id": "STATUS4265_0",
            "summary": (
                "4265 moves Dq_matter from missing to a conditional zero for the ordinary matter action-domain, "
                "while explicitly retaining source/readout prefactors and coefficient owners as separate live gates."
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
            "objective": "Attack Dq_source_readout or Dq_coeff to handle measured-source maps, species/source weights, kappa/G normalization and coefficient-owner slots.",
            "avoid": "Do not absorb relative source weights into a calibrated common G_N/GM mode unless the common-mode projector is explicitly declared.",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 281 - PPC4161 Dq-matter action-domain zero or source-prefactor bound

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4265 does not prove WEP, measured `G_N`, measured `GM`, source normalization, PPN, R10, or public local GR.

It adopts:

```text
Dq_matter = 0
```

only for the ordinary matter action-domain part of the standard local branch.

## Split

Closed here:

```text
S_matter = Sbar[psi, g_obs(q), theta_obs]
```

with `theta_obs` fixed by 4264.

Not closed here:

```text
w_A(Phi) S_A,
measured-source/worldtube maps,
Hamiltonian charge to observed mass readout,
boundary/source projectors,
kappa/G/ell_J coefficient owners,
direct hidden matter operators if added.
```

Those stay in `Dq_source_readout`, `Dq_coeff`, `Dq_boundary_projector`, or explicit bound rows.

## Matter-domain theorem

If:

```text
delta_v g_obs = 0,
delta_v theta_obs = 0,
S_matter has no direct hidden-parent argument,
```

then:

```text
delta_v S_matter
= (delta S_matter/delta g_obs) delta_v g_obs
 + (delta S_matter/delta theta_obs) delta_v theta_obs
= 0.
```

Therefore:

```text
Dq_matter = 0,
Dq_matter_C1 = 0
```

for the standard matter action-domain branch.

## Source-prefactor tax

If the parent branch contains:

```text
w_A(Phi) S_A,
Delta_w_species,
Pi_M readout reentry,
source-worldtube selector before variation,
kappa/G/ell_J coefficient drift,
```

then it is not killed by this theorem. It must be bounded or proved zero separately.

## 4254 feed

The live component candidate is updated:

```text
Dq_matter = 0.0,
Dq_matter_C1 = 0.0.
```

The row remains `valid_for_claim=false` because the complete 4254 source-probe/tomography gate still needs other Dq components and constants.

## Next target

`{NEXT_TARGET}` should attack `Dq_source_readout` or `Dq_coeff`.
"""


def checkpoint_doc() -> str:
    return f"""
# 4265 - Y5 R2FR Dq-matter action-domain zero or source-prefactor bound

Packet marker: `{PACKET_MARKER}`

## Result

4265 adopts:

```text
Dq_matter = 0.0,
Dq_matter_C1 = 0.0
```

for the standard ordinary matter action-domain only.

Source/readout prefactors remain live and must be handled next.

## Claim status

Private nonclaim. This narrows the component ledger without smuggling WEP or measured-mass closure.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    theorems = csv_rows(paths["theorems"])
    split = csv_rows(paths["split"])
    adoption = csv_rows(paths["adoption"])
    local_candidate = csv_rows(paths["local_candidate"])
    live_candidate = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
    live_matter = [row for row in live_candidate if row.get("probe_id") == "Dq_matter"]
    live_theta = [row for row in live_candidate if row.get("probe_id") == "Dq_theta_marker"]
    live_em = [row for row in live_candidate if row.get("probe_id") == "Dq_EM"]
    rows = [
        ("VAL4265_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4265_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4265_2_matter_zero_theorem",
            any(row["status"] == "CONDITIONAL_ZERO_IN_STANDARD_BRANCH" for row in theorems),
            "matter action-domain zero theorem emitted",
        ),
        (
            "VAL4265_3_source_prefactors_retained",
            any(row["assigned_live_gate"] == "Dq_source_readout_or_Dq_coeff" for row in split)
            and any(row["coefficient"] == "Delta_w_species_A" for row in split),
            "source/species weights retained outside Dq_matter",
        ),
        (
            "VAL4265_4_adoption_row",
            bool(adoption)
            and adoption[0]["new_epsilon"] == "0.0"
            and adoption[0]["adoption_status"] == "ADOPTED_CONDITIONAL_ZERO_FOR_STANDARD_MATTER_ACTION_DOMAIN_ONLY",
            "Dq_matter adoption row emitted",
        ),
        (
            "VAL4265_5_local_candidate_numeric",
            any(row.get("probe_id") == "Dq_matter" and row.get("epsilon") == "0.0" and row.get("epsilon_C1") == "0.0" for row in local_candidate),
            "local 4265 candidate has numeric matter zero",
        ),
        (
            "VAL4265_6_live_4254_updated",
            bool(live_matter)
            and live_matter[0].get("epsilon") == "0.0"
            and live_matter[0].get("epsilon_C1") == "0.0"
            and live_matter[0].get("source_path") == str(FORMAL_PATH),
            "live 4254 candidate Dq_matter updated",
        ),
        (
            "VAL4265_7_preserve_prior_adoptions",
            bool(live_em)
            and live_em[0].get("epsilon") == "0.0"
            and bool(live_theta)
            and live_theta[0].get("epsilon") == "0.0",
            "prior Dq_EM and Dq_theta_marker adoptions preserved",
        ),
        ("VAL4265_8_claim_row", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4265_9_formal_doc", MARKER in read_text(FORMAL_PATH), "formal marker present"),
        ("VAL4265_10_checkpoint_doc", PACKET_MARKER in read_text(DOC_PATH), "checkpoint marker present"),
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
    source_path = SOURCE_DIR / "P8_Y5_R2FR_4265_SOURCE_REGISTER.csv"
    theorem_path = SOURCE_DIR / "P8_Y5_R2FR_4265_MATTER_DOMAIN_THEOREM.csv"
    split_path = SOURCE_DIR / "P8_Y5_R2FR_4265_SOURCE_PREFACTOR_SPLIT_ROWS.csv"
    adoption_path = SOURCE_DIR / "P8_Y5_R2FR_4265_DQ_MATTER_ADOPTION.csv"
    decision_path = SOURCE_DIR / "P8_Y5_R2FR_4265_DECISION.csv"
    firewall_path = SOURCE_DIR / "P8_Y5_R2FR_4265_CLAIM_FIREWALL.csv"
    status_path = SOURCE_DIR / "P8_Y5_R2FR_4265_STATUS.csv"
    next_path = SOURCE_DIR / "P8_Y5_R2FR_4265_NEXT_TARGET.csv"

    component_candidate = component_candidate_rows()
    write_csv(source_path, source_rows())
    write_csv(theorem_path, matter_theorem_rows())
    write_csv(split_path, prefactor_split_rows())
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
        "split": split_path,
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
