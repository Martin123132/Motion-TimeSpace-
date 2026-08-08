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

CHECKPOINT = "4245"
CLAIM_ID = "L-086"
BRANCH = "MTS_R2FR_Y5_HL_QBASIC_STRIP_DQ_BOUND_FIRST_ROW_4245"
DECISION = "HL_QBASIC_SUBPROFILE_ADOPTED_EXACTLY_DQ_RESIDUAL_REDUCED_TO_HPERP_FIRST_GEOM_BOUND_ROW_STAGED_NONCLAIM"
MARKER = "PPC4161_HL_QBASIC_STRIP_DQ_BOUND_FIRST_ROW_4245"
PACKET_MARKER = "PPC4161_PACKET_HL_QBASIC_STRIP_DQ_BOUND_FIRST_ROW_4245"
NEXT_TARGET = "4246-Y5-R2FR-Hperp-geometry-zero-certificate-or-epsilon-geom-profile-fill.md"

FORMAL_PATH = FORMAL / "261-PPC4161-HL-qbasic-strip-and-Dq-bound-first-input-row.md"
DOC_PATH = POST / "4245-Y5-R2FR-HL-argument-qbasic-adoption-or-Dq-bound-first-input-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4245_VALIDATION.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4245_00_4244_next": SourceSpec(
        "SRC4245_00_4244_next",
        SOURCE_DIR / "P8_Y5_R2FR_4244_NEXT_TARGET.csv",
        "4245-Y5-R2FR-HL-argument-qbasic-adoption-or-Dq-bound-first-input-row.md",
        "4244 selected the H_L argument adoption target.",
    ),
    "SRC4245_01_4244_formal": SourceSpec(
        "SRC4245_01_4244_formal",
        FORMAL / "260-PPC4161-Dq-component-zero-adoption-or-Hperp-bound-input-fill.md",
        "selector theorem for v + H_L argument certificate",
        "4244 adoption rule requiring H_L argument certificate.",
    ),
    "SRC4245_02_4239_formal": SourceSpec(
        "SRC4245_02_4239_formal",
        FORMAL / "255-PPC4161-parent-source-orthogonality-or-M2-profile-sampler-dry-run.md",
        "H_L = H_q + H_perp",
        "4239 H_L split and source-orthogonality for q-basic part.",
    ),
    "SRC4245_03_4239_decomposition": SourceSpec(
        "SRC4245_03_4239_decomposition",
        SOURCE_DIR / "P8_Y5_R2FR_4239_HL_DECOMPOSITION.csv",
        "Pi_kerDq H_L",
        "Machine-readable H_q/Hperp decomposition.",
    ),
    "SRC4245_04_4240_audit": SourceSpec(
        "SRC4245_04_4240_audit",
        SOURCE_DIR / "P8_Y5_R2FR_4240_HPERP_QBASIC_AUDIT.csv",
        "H_L=H_q",
        "4240 rejection of full H_L q-basic shortcut.",
    ),
    "SRC4245_05_qnatural": SourceSpec(
        "SRC4245_05_qnatural",
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "V_q := ker(Dq),",
        "Quotient kernel and vertical silence theorem.",
    ),
    "SRC4245_06_component_theorem": SourceSpec(
        "SRC4245_06_component_theorem",
        FORMAL / "235-PPC4161-Dq-source-readout-coupling-marker-zero-or-bound.md",
        "Dq_geom[v]=0,",
        "Eight componentwise Dq zero clauses for admitted q-basic v.",
    ),
    "SRC4245_07_projector_bound": SourceSpec(
        "SRC4245_07_projector_bound",
        FORMAL / "230-PPC4161-projector-stress-curl-zero-or-bound.md",
        "|R_wall|",
        "Geometry/projector fallback residual terms.",
    ),
    "SRC4245_08_projector_clause": SourceSpec(
        "SRC4245_08_projector_clause",
        FORMAL / "230-PPC4161-projector-stress-curl-zero-or-bound.md",
        "P_loc=P_bar(q)",
        "Geometry/coframe descent clause for the first component-bound row.",
    ),
    "SRC4245_09_boundary": SourceSpec(
        "SRC4245_09_boundary",
        FORMAL / "233-PPC4161-boundary-corner-curl-zero-or-flux-bound.md",
        "I_boundary + I_corner = 0.",
        "Boundary no-flux support for excluding boundary projector leakage when signed.",
    ),
    "SRC4245_10_visible_EM": SourceSpec(
        "SRC4245_10_visible_EM",
        FORMAL / "234-PPC4161-visible-EM-material-curl-zero-or-residual-bound.md",
        "|R_Hodge|",
        "Hodge/readout residual source for geometry and EM separation.",
    ),
    "SRC4245_11_coeff_lock": SourceSpec(
        "SRC4245_11_coeff_lock",
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "D_A ln kappa_eff = 0.",
        "Coefficient marker lock source.",
    ),
    "SRC4245_12_4244_adoption": SourceSpec(
        "SRC4245_12_4244_adoption",
        SOURCE_DIR / "P8_Y5_R2FR_4244_DQ_COMPONENT_ADOPTION_MATRIX.csv",
        "Dq_geom[H_L]",
        "4244 component adoption matrix.",
    ),
}


COMPONENTS = [
    ("Dq_geom", "epsilon_geom", "R_Dq_geom_Hperp"),
    ("Dq_tau", "epsilon_tau", "R_Dq_tau_Hperp"),
    ("Dq_matter", "epsilon_matter", "R_Dq_matter_Hperp"),
    ("Dq_source_readout", "epsilon_source_readout", "R_Dq_source_readout_Hperp"),
    ("Dq_theta_marker", "epsilon_theta_marker", "R_Dq_theta_marker_Hperp"),
    ("Dq_boundary_projector", "epsilon_boundary_projector", "R_Dq_boundary_projector_Hperp"),
    ("Dq_EM", "epsilon_EM", "R_Dq_EM_Hperp"),
    ("Dq_coeff", "epsilon_coeff", "R_Dq_coeff_Hperp"),
]


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
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def append_once(path: Path, marker: str, block: str) -> None:
    current = read_text(path)
    if marker in current:
        return
    write_text(path, current.rstrip() + "\n\n" + block.strip())


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


def split_theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "theorem_id": "HLSTRIP4245_0_split",
            "statement": "H_L = H_q + Hperp with H_q := Pi_kerDq H_L and Hperp := (1-Pi_kerDq)H_L",
            "formula": "H_L = Pi_kerDq H_L + (1-Pi_kerDq)H_L",
            "status": "adopted_from_4239_4243",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "HLSTRIP4245_1_qbasic_component_zero",
            "statement": "For every component differential Dq_i, the q-basic piece has Dq_i[H_q]=0.",
            "formula": "H_q in ker(Dq) => Dq_i[H_q]=0 for all i",
            "status": "private_selector_pass",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "HLSTRIP4245_2_component_reduction",
            "statement": "Linearity of the first variation gives Dq_i[H_L]=Dq_i[Hperp].",
            "formula": "Dq_i[H_L]=Dq_i[H_q]+Dq_i[Hperp]=Dq_i[Hperp]",
            "status": "derived_exact_reduction",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "HLSTRIP4245_3_no_full_zero",
            "statement": "The exact reduction is not a proof that Hperp=0 or that any Dq_i[Hperp] vanishes.",
            "formula": "Dq_i[H_L]=Dq_i[Hperp] does not imply Dq_i[Hperp]=0",
            "status": "anti_smuggling_guard",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def component_reduction_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for component, epsilon, residual in COMPONENTS:
        rows.append(
            {
                **common(),
                "component": f"{component}[H_L]",
                "qbasic_piece": f"{component}[H_q]",
                "qbasic_piece_status": "exact_zero_private_selector",
                "reduced_live_component": f"{component}[Hperp]",
                "reduction_formula": f"{component}[H_L] = {component}[Hperp]",
                "epsilon_bound": epsilon,
                "residual_name": residual,
                "adoption_gain": "H_L_argument_problem_stripped_to_Hperp_only",
                "zero_status": "not_zero_claimed",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def first_bound_row() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "bound_id": "EGEOM4245_0_first_component_row",
            "component": "Dq_geom[Hperp]",
            "quantity": "epsilon_geom",
            "definition": "epsilon_geom >= ||Dq_geom[Hperp]|| in the local observed-geometry/coframe/projector slot",
            "derived_envelope": "epsilon_geom <= epsilon_Oloc + epsilon_coframe + epsilon_projector + epsilon_wall + epsilon_Hodge_geom",
            "zero_route": "P_loc=P_bar(q), e_obs=e_bar(q), Hodge=Hodge[g_obs], source/readout factors through q, and no active selector wall for Hperp",
            "profile_fill_columns": "system_id;collar_id;norm_Dq_geom_Hperp;epsilon_Oloc;epsilon_coframe;epsilon_projector;epsilon_wall;epsilon_Hodge_geom;units;source_path;assumptions;valid_for_claim",
            "source_support": "SRC4245_07_projector_bound;SRC4245_08_projector_clause;SRC4245_10_visible_EM",
            "numeric_value": "MISSING",
            "units": "geometry_component_Dq_norm",
            "current_status": "first_real_bound_row_formula_staged_numeric_profile_missing",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def residual_budget_rows() -> List[Dict[str, str]]:
    eps_terms = " + ".join(f"w_{epsilon.replace('epsilon_', '')} {epsilon}^2" for _, epsilon, _ in COMPONENTS)
    return [
        {
            **common(),
            "budget_id": "HLSTRIP4245_0_reduced_EDq",
            "formula": f"E_Dq,Hperp^2 := {eps_terms}",
            "interpretation": "After exact q-basic stripping, only Hperp component defects enter the Dq norm.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "budget_id": "HLSTRIP4245_1_reduced_source_bound",
            "formula": "|S_A Hperp^A| <= C_S C_perp E_Dq,Hperp",
            "interpretation": "Same Hperp source bound as 4243, but now the H_L argument debt has been reduced to Hperp-only components.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "budget_id": "HLSTRIP4245_2_first_component_insert",
            "formula": "E_Dq,Hperp^2 >= w_geom epsilon_geom^2, epsilon_geom >= ||Dq_geom[Hperp]||",
            "interpretation": "The geometry component is the first concrete fill target; it cannot be dropped or hidden in source/readout prose.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "DEC4245",
            "decision": DECISION,
            "scoreable_now": "False",
            "zero_claim_allowed": "False",
            "reason": "The q-basic subprofile H_q is exactly silent in every component, but the non-q defect Hperp remains and now carries the whole Dq burden.",
            "selected_route": "Attack Dq_geom[Hperp] first because it is the root observed-geometry/coframe gate feeding PPN, clocks, R10 and matter readout.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4245_0_no_Hperp_zero", "Dq_i[H_L]=Dq_i[Hperp] is not Hperp=0."),
        ("FW4245_1_no_component_zero", "The q-basic piece is zero; the Hperp component still needs theorem-zero or a sourced epsilon."),
        ("FW4245_2_no_numeric_claim", "The epsilon_geom row has a derived envelope but no numeric profile yet."),
        ("FW4245_3_no_geometry_to_all", "A future geometry pass would not automatically close tau, matter, EM, boundary or coefficient components."),
        ("FW4245_4_private_only", "No local-GR, R10, PPN, clock, orbital or GitHub/public claim follows from 4245."),
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
            "status": DECISION,
            "summary": "4245 exactly strips the q-basic H_q contribution from every Dq component and leaves a sharper Hperp-only residual problem, with epsilon_geom staged as the first concrete component-bound row.",
            "scoreable_now": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "task": "Prove Dq_geom[Hperp]=0 from observed-geometry/coframe descent and no-wall selector clauses, or fill epsilon_geom from an actual Hperp geometry profile.",
            "reason": "Geometry/coframe is the least avoidable component: if it survives, local PPN/readout leakage survives; if it closes, the remaining components are cleaner.",
            "valid_for_claim": "False",
        }
    ]


def all_generated_groups() -> List[List[Dict[str, str]]]:
    return [
        source_rows(),
        split_theorem_rows(),
        component_reduction_rows(),
        first_bound_row(),
        residual_budget_rows(),
        decision_rows(),
        firewall_rows(),
        status_rows(),
        next_target_rows(),
    ]


def formal_doc() -> str:
    return f"""
# 261 - PPC4161 H_L q-basic strip and Dq bound first input row

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. 4245 does not claim local GR, PPN safety, R10 safety, clock safety, EM closure, or `Hperp=0`.

## Exact Strip Theorem

From 4239 and 4243:

```text
H_L = H_q + Hperp,
H_q := Pi_kerDq H_L,
Hperp := (1 - Pi_kerDq) H_L.
```

Because `H_q in ker(Dq)`, every component differential kills the q-basic piece:

```text
Dq_i[H_q] = 0.
```

The component differentials are first variations, so they are linear on the tangent argument:

```text
Dq_i[H_L]
= Dq_i[H_q] + Dq_i[Hperp]
= Dq_i[Hperp].
```

This is the 4245 adoption result. It does **not** prove full `H_L` q-basicity. It proves that the only remaining Dq debt is the non-q defect.

## Reduced Live Problem

Instead of eight vague `Dq_i[H_L]` rows, the live rows are now:

```text
Dq_geom[Hperp],
Dq_tau[Hperp],
Dq_matter[Hperp],
Dq_source_readout[Hperp],
Dq_theta_marker[Hperp],
Dq_boundary_projector[Hperp],
Dq_EM[Hperp],
Dq_coeff[Hperp].
```

Thus

```text
E_Dq,Hperp^2 := sum_i w_i epsilon_i^2,
epsilon_i >= ||Dq_i[Hperp]||,
|S_A Hperp^A| <= C_S C_perp E_Dq,Hperp.
```

## First Bound Row

The first concrete row is the observed-geometry/coframe component:

```text
epsilon_geom >= ||Dq_geom[Hperp]||.
```

Its derived non-cancellation envelope is:

```text
epsilon_geom
<= epsilon_Oloc
 + epsilon_coframe
 + epsilon_projector
 + epsilon_wall
 + epsilon_Hodge_geom.
```

The zero route is equally precise:

```text
P_loc=P_bar(q),
e_obs=e_bar(q),
Hodge=Hodge[g_obs],
source/readout factors through q,
no active selector wall for Hperp
=> Dq_geom[Hperp]=0.
```

If any clause fails, `epsilon_geom` must be filled from a real local Hperp geometry profile. No cancellation between terms is allowed.

## Next Target

`{NEXT_TARGET}` should prove `Dq_geom[Hperp]=0` from observed-geometry/coframe descent and no-wall clauses, or fill `epsilon_geom` with real profile data.
"""


def checkpoint_doc() -> str:
    return f"""
# 4245 - H_L argument q-basic adoption or Dq-bound first input row

**Status:** `{DECISION}`.

## What changed

4245 proves the useful part of the `H_L` adoption:

```text
H_L = H_q + Hperp,
Dq_i[H_q]=0,
Dq_i[H_L]=Dq_i[Hperp].
```

So the q-basic piece is no longer part of the obstruction. The whole Dq burden is now on `Hperp`.

## First concrete row

The first component-bound row is:

```text
epsilon_geom >= ||Dq_geom[Hperp]||
```

with envelope:

```text
epsilon_geom <= epsilon_Oloc + epsilon_coframe + epsilon_projector + epsilon_wall + epsilon_Hodge_geom.
```

## Next target

`{NEXT_TARGET}`
"""


def update_claim_register() -> None:
    path = FORMAL / "02-claims-register.csv"
    if CLAIM_ID in read_text(path):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "4245 exactly strips the q-basic H_q contribution from every Dq_i[H_L] component, reducing the live H_L argument debt to Dq_i[Hperp] only, and stages epsilon_geom as the first concrete geometry/coframe bound row.",
        "current_evidence": "4245 source register, H_L split theorem, Dq component reduction matrix, first geometry bound row, residual budget, decision and firewall.",
        "status": "private_HL_qbasic_strip_Hperp_only_Dq_nonclaim",
        "next_test": "Prove Dq_geom[Hperp]=0 from observed-geometry/coframe descent and no-wall selector clauses, or fill epsilon_geom from a real Hperp geometry profile.",
        "key_risk": "Confusing H_q silence with Hperp silence would smuggle the local-GR result; epsilon_geom is not numeric yet.",
    }
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def update_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 H_L q-basic strip and first Dq bound row

Marker: `{MARKER}`

4245 proves the clean decomposition step:

```text
H_L = H_q + Hperp,
Dq_i[H_q]=0,
Dq_i[H_L]=Dq_i[Hperp].
```

The local cGamma/Hperp problem is therefore not a generic `H_L` problem anymore; it is specifically the non-q defect problem. The first concrete component row is:

```text
epsilon_geom >= ||Dq_geom[Hperp]||.
```
"""
    packet_block = f"""
## Packet Update - H_L q-basic strip

Marker: `{PACKET_MARKER}`

The q-basic part of `H_L` is exactly adopted and removed from all Dq components. The remaining Hperp-only residual begins with the observed-geometry/coframe row `epsilon_geom`.
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
    theorem = split_theorem_rows()
    reductions = component_reduction_rows()
    first_row = first_bound_row()
    budgets = residual_budget_rows()
    all_rows = [row for group in all_generated_groups() for row in group]

    add("VAL4245_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources), "source register")
    add("VAL4245_1_needles_found", "all source needles found", all(row["required_text_found"] == "True" for row in sources), "source register")
    add("VAL4245_2_split_theorem", "split theorem contains H_L=H_q+Hperp", any("H_L = H_q + Hperp" in row["statement"] for row in theorem), "split theorem")
    add("VAL4245_3_qbasic_zero", "q-basic component zero theorem exists", any("Dq_i[H_q]=0" in row["formula"] for row in theorem), "split theorem")
    add("VAL4245_4_component_reduction", "all components reduce to Hperp", len(reductions) == 8 and all("[Hperp]" in row["reduced_live_component"] for row in reductions), "component reduction")
    add("VAL4245_5_no_zero_claim", "no component claims zero", all(row["zero_status"] == "not_zero_claimed" for row in reductions), "component reduction")
    add("VAL4245_6_first_geom_row", "first geometry bound row exists", first_row[0]["quantity"] == "epsilon_geom" and "Dq_geom[Hperp]" in first_row[0]["component"], "first bound row")
    add("VAL4245_7_geom_envelope", "geometry row has explicit non-cancellation envelope", "epsilon_Oloc" in first_row[0]["derived_envelope"] and "epsilon_Hodge_geom" in first_row[0]["derived_envelope"], "first bound row")
    add("VAL4245_8_budget_hperp_only", "budget uses E_Dq,Hperp", any("E_Dq,Hperp" in row["formula"] for row in budgets), "residual budget")
    add("VAL4245_9_decision_nonclaim", "decision keeps scoreable false", decision_rows()[0]["scoreable_now"] == "False", "decision")
    add("VAL4245_10_docs_written", "formal and checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), f"{FORMAL_PATH}; {DOC_PATH}")
    add("VAL4245_11_claim_register", "claims register contains L-086", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), str(FORMAL / "02-claims-register.csv"))
    add("VAL4245_12_spine_marker", "spine contains marker", MARKER in read_text(FORMAL / "07-unification-spine.md"), str(FORMAL / "07-unification-spine.md"))
    add("VAL4245_13_packet_marker", "packet contains marker", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), str(FORMAL / "180-PPC4161-private-local-packet-integration.md"))
    add("VAL4245_14_no_claim_flags", "no generated row is valid for claim", all(row.get("valid_for_claim") != "True" for row in all_rows), "all generated groups")
    add("VAL4245_15_next_target", "next target selected", next_target_rows()[0]["next_target"] == NEXT_TARGET, NEXT_TARGET)
    return rows


def main() -> None:
    paths = {
        "source": SOURCE_DIR / "P8_Y5_R2FR_4245_SOURCE_REGISTER.csv",
        "theorem": SOURCE_DIR / "P8_Y5_R2FR_4245_HL_SPLIT_THEOREM.csv",
        "components": SOURCE_DIR / "P8_Y5_R2FR_4245_DQ_COMPONENT_REDUCTION_MATRIX.csv",
        "first_bound": SOURCE_DIR / "P8_Y5_R2FR_4245_FIRST_DQ_BOUND_INPUT_ROW.csv",
        "budget": SOURCE_DIR / "P8_Y5_R2FR_4245_RESIDUAL_BUDGET.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4245_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4245_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4245_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4245_NEXT_TARGET.csv",
    }
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    write_csv(paths["source"], source_rows())
    write_csv(paths["theorem"], split_theorem_rows())
    write_csv(paths["components"], component_reduction_rows())
    write_csv(paths["first_bound"], first_bound_row())
    write_csv(paths["budget"], residual_budget_rows())
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
