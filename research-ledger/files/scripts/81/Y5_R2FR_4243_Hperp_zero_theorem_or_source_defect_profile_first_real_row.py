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

CHECKPOINT = "4243"
CLAIM_ID = "L-084"
BRANCH = "MTS_R2FR_Y5_HPERP_DQ_DEFECT_BOUND_4243"
DECISION = "HPERP_ZERO_REDUCED_TO_COMPONENTWISE_DQ_DEFECTS_SOURCE_DEFECT_BOUND_ROW_DERIVED_NUMERIC_PROFILE_OPEN_NONCLAIM"
MARKER = "PPC4161_HPERP_DQ_DEFECT_BOUND_4243"
PACKET_MARKER = "PPC4161_PACKET_HPERP_DQ_DEFECT_BOUND_4243"
NEXT_TARGET = "4244-Y5-R2FR-Dq-component-zero-adoption-or-Hperp-bound-input-fill.md"

FORMAL_PATH = FORMAL / "259-PPC4161-Hperp-zero-theorem-or-source-defect-profile-first-real-row.md"
DOC_PATH = POST / "4243-Y5-R2FR-Hperp-zero-theorem-or-source-defect-profile-first-real-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4243_VALIDATION.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4243_00_4242_next": SourceSpec(
        "SRC4243_00_4242_next",
        SOURCE_DIR / "P8_Y5_R2FR_4242_NEXT_TARGET.csv",
        "4243-Y5-R2FR-Hperp-zero-theorem-or-source-defect-profile-first-real-row.md",
        "4242 selected Hperp zero theorem or first source-defect profile row.",
    ),
    "SRC4243_01_4242_formal": SourceSpec(
        "SRC4243_01_4242_formal",
        FORMAL / "258-PPC4161-M2-defect-source-map-pruning-or-real-profile-input-pack.md",
        "S_A Hperp^A.",
        "4242 isolated Hperp as live source target.",
    ),
    "SRC4243_02_4242_budget": SourceSpec(
        "SRC4243_02_4242_budget",
        SOURCE_DIR / "P8_Y5_R2FR_4242_RESIDUAL_BUDGET.csv",
        "A_J,eff_private <= |S_A Hperp^A|",
        "Machine-readable best-case Hperp-only budget.",
    ),
    "SRC4243_03_Dq_components": SourceSpec(
        "SRC4243_03_Dq_components",
        FORMAL / "235-PPC4161-Dq-source-readout-coupling-marker-zero-or-bound.md",
        "Dq_source_readout[v]=0,",
        "Componentwise Dq zero theorem.",
    ),
    "SRC4243_04_Dq_bound": SourceSpec(
        "SRC4243_04_Dq_bound",
        FORMAL / "235-PPC4161-Dq-source-readout-coupling-marker-zero-or-bound.md",
        "|E_Dq_total|",
        "Dq absolute bound route.",
    ),
    "SRC4243_05_qnatural": SourceSpec(
        "SRC4243_05_qnatural",
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "V_q := ker(Dq),",
        "Quotient vertical kernel source.",
    ),
    "SRC4243_06_qnatural_matter": SourceSpec(
        "SRC4243_06_qnatural_matter",
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "S_matter = Sbar_m[psi, g_obs(q), A(q), theta(q)].",
        "Matter/readout descent before variation.",
    ),
    "SRC4243_07_qbasic": SourceSpec(
        "SRC4243_07_qbasic",
        FORMAL / "229-PPC4161-qbasic-vertical-presymplectic-silence.md",
        "Dq[v] = 0.",
        "q-basic vertical condition.",
    ),
    "SRC4243_08_projector": SourceSpec(
        "SRC4243_08_projector",
        FORMAL / "230-PPC4161-projector-stress-curl-zero-or-bound.md",
        "source/readout quantities factor through `q`;",
        "Projector/source-readout q-factorization clause.",
    ),
    "SRC4243_09_HL_candidate": SourceSpec(
        "SRC4243_09_HL_candidate",
        FORMAL / "125-local-leakage-vector-invariant.md",
        "H_L^A(X_B);",
        "H_L remains candidate-defined, not parent-derived.",
    ),
    "SRC4243_10_input_pack": SourceSpec(
        "SRC4243_10_input_pack",
        SOURCE_DIR / "P8_Y5_R2FR_4242_REAL_INPUT_PACK.csv",
        "Hperp^A(x,t)",
        "Previous Hperp input row.",
    ),
    "SRC4243_11_claim_register": SourceSpec(
        "SRC4243_11_claim_register",
        FORMAL / "02-claims-register.csv",
        "L-083",
        "Prior claim-register anchor for 4242.",
    ),
}


DQ_COMPONENTS = [
    ("DQ4243_0_geom", "Dq_geom[H_L]", "geometry/coframe quotient defect", "MISSING_DQ_GEOM"),
    ("DQ4243_1_tau", "Dq_tau[H_L]", "time-flow/readout quotient defect", "MISSING_DQ_TAU"),
    ("DQ4243_2_matter", "Dq_matter[H_L]", "matter-domain quotient defect", "MISSING_DQ_MATTER"),
    ("DQ4243_3_source", "Dq_source_readout[H_L]", "source-readout quotient defect", "MISSING_DQ_SOURCE_READOUT"),
    ("DQ4243_4_theta", "Dq_theta_marker[H_L]", "clock/material marker quotient defect", "MISSING_DQ_THETA_MARKER"),
    ("DQ4243_5_boundary", "Dq_boundary_projector[H_L]", "boundary/projector quotient defect", "MISSING_DQ_BOUNDARY_PROJECTOR"),
    ("DQ4243_6_EM", "Dq_EM[H_L]", "EM/Hodge/current quotient defect", "MISSING_DQ_EM"),
    ("DQ4243_7_coeff", "Dq_coeff[H_L]", "coupling/coefficient quotient defect", "MISSING_DQ_COEFF"),
]


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


def hperp_theorem_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "HT4243_0_definition",
            "Hperp := (1 - Pi_kerDq) H_L",
            "Hperp is the part of the leakage profile not certified as q-basic.",
            "definition",
        ),
        (
            "HT4243_1_zero_condition",
            "all_i Dq_i[H_L]=0 => Hperp=0",
            "Componentwise q-basic ownership kills the non-q leakage defect.",
            "conditional theorem",
        ),
        (
            "HT4243_2_source_zero",
            "Hperp=0 => S_A Hperp^A=0",
            "The live source-current contraction vanishes only after Hperp is killed.",
            "conditional theorem",
        ),
        (
            "HT4243_3_defect_norm",
            "E_Dq,H^2 := sum_i w_i ||Dq_i[H_L]||^2",
            "Positive component norm measuring how far H_L is from q-basic.",
            "derived bound owner",
        ),
        (
            "HT4243_4_Hperp_bound",
            "||Hperp|| <= C_perp E_Dq,H",
            "Source defect is bounded by quotient-defect norm if Pi_kerDq is stable.",
            "conditional bound",
        ),
        (
            "HT4243_5_source_bound",
            "|S_A Hperp^A| <= C_S C_perp E_Dq,H",
            "First real source-defect bound row: Hperp is no longer vague.",
            "symbolic nonclaim",
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


def dq_component_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for component_id, component, meaning, status in DQ_COMPONENTS:
        rows.append(
            {
                **common(),
                "component_id": component_id,
                "component": component,
                "meaning": meaning,
                "zero_for_Hperp_claim": "required",
                "bound_status": status,
                "numeric_value": "MISSING",
                "source_path": "MISSING_PARENT_COMPONENT_ROW",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def source_defect_bound_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "SB4243_0_symbolic_bound",
            "A_src,Hperp := |S_A Hperp^A| <= C_S C_perp E_Dq,H",
            "symbolic_bound",
            "nonclaim until C_S, C_perp and E_Dq,H component values are sourced",
        ),
        (
            "SB4243_1_best_case",
            "E_Dq,H=0 => A_src,Hperp=0",
            "exact_zero_branch",
            "requires all Dq_i[H_L] zero clauses",
        ),
        (
            "SB4243_2_budget",
            "C_S C_perp E_Dq,H <= 0.1678939074330212*(mu_Xi T_res)/|c_Gamma|",
            "strong_Gdot_budget_branch",
            "scoreable only after Dq profile and budget owner inputs exist",
        ),
        (
            "SB4243_3_first_profile_row",
            "Hperp/S_A first real row is replaced by Dq component profile pack",
            "profile_contract",
            "Dq component rows are the first source-ready form; no fabricated numbers",
        ),
    ]
    return [
        {
            **common(),
            "bound_id": bound_id,
            "formula": formula,
            "row_type": row_type,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for bound_id, formula, row_type, status in rows
    ]


def input_fill_rows() -> List[Dict[str, str]]:
    rows = [
        ("IF4243_0_CS", "C_S", "source-current Lipschitz norm", "MISSING_SOURCE_OPERATOR_NORM"),
        ("IF4243_1_Cperp", "C_perp", "stable projection/quotient complement norm", "MISSING_QUOTIENT_GEOMETRY_NORM"),
        ("IF4243_2_EDqH", "E_Dq,H", "combined componentwise Dq defect of H_L", "MISSING_DQ_COMPONENT_VALUES"),
        ("IF4243_3_muT_cGamma", "(mu_Xi T_res)/|c_Gamma|", "strong local budget owner", "MISSING_TIMESCALE_COUPLING"),
        ("IF4243_4_arena", "profile_a/J_a", "PPN/Gdot/gradient arena projection", "MISSING_ARENA_PROJECTION"),
    ]
    return [
        {
            **common(),
            "input_id": input_id,
            "quantity": quantity,
            "role": role,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for input_id, quantity, role, status in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "forward_move": "Hperp is reduced to a componentwise Dq defect norm; source row becomes |S_A Hperp| <= C_S C_perp E_Dq,H.",
            "Hperp_zero_claimed": "False",
            "scoreable_now": "False",
            "best_next_move": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4243_0_no_Hperp_zero", "Do not claim Hperp=0 until all componentwise Dq_i[H_L] rows are zero.", "active"),
        ("FW4243_1_no_geometry_only", "Geometry-only Dq silence is insufficient; matter/source/EM/coefficient/readout components are required.", "active"),
        ("FW4243_2_no_fabricated_profile", "No numeric Hperp/S_A profile row is valid until parent component values are sourced.", "active"),
        ("FW4243_3_absolute_bound", "Use absolute Dq component bound; no cancellation between Dq defects.", "active"),
        ("FW4243_4_private_scope", "This is a private nonclaim bound row, not a local-GR proof.", "active"),
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
            "status": "private_Hperp_Dq_defect_bound_nonclaim",
            "summary": "4243 reduces Hperp to componentwise Dq defects and gives the symbolic source bound |S_A Hperp| <= C_S C_perp E_Dq,H.",
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
            "reason": "Next either adopt/prove all Dq component zeros for H_L, or fill source-backed Dq component bounds plus C_S/C_perp.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def all_generated_groups() -> Iterable[List[Dict[str, str]]]:
    return (
        source_rows(),
        hperp_theorem_rows(),
        dq_component_rows(),
        source_defect_bound_rows(),
        input_fill_rows(),
        decision_rows(),
        firewall_rows(),
        status_rows(),
        next_target_rows(),
    )


def formal_doc() -> str:
    return f"""
# 259 - PPC4161 Hperp zero theorem or source defect profile first real row

Marker: `{MARKER}`

Branch: `{BRANCH}`
Decision: `{DECISION}`

## Result

4243 reduces the live row:

```text
S_A Hperp^A
```

to componentwise quotient defects.

Define:

```text
Hperp := (1 - Pi_kerDq) H_L,
E_Dq,H^2 := sum_i w_i ||Dq_i[H_L]||^2.
```

If every component is q-basic:

```text
Dq_geom[H_L]=0,
Dq_tau[H_L]=0,
Dq_matter[H_L]=0,
Dq_source_readout[H_L]=0,
Dq_theta_marker[H_L]=0,
Dq_boundary_projector[H_L]=0,
Dq_EM[H_L]=0,
Dq_coeff[H_L]=0,
```

then:

```text
Hperp=0,
S_A Hperp^A=0.
```

## Bound Row

If the component defects do not all vanish, the first honest source-defect row is:

```text
|S_A Hperp^A| <= C_S C_perp E_Dq,H.
```

The strong local budget becomes:

```text
C_S C_perp E_Dq,H
<= 0.1678939074330212 * (mu_Xi T_res)/|c_Gamma|.
```

## Claim Status

Private nonclaim. No numeric profile was fabricated. The row becomes scoreable only after `Dq_i[H_L]`, `C_S`, `C_perp`, the timescale/coupling owner, and arena projections are sourced.

## Next Target

`{NEXT_TARGET}`
"""


def checkpoint_doc() -> str:
    return f"""
# 4243 - Hperp zero theorem or source defect profile first real row

**Status:** `{DECISION}`.

## Forward Move

4243 turns the live source row into:

```text
|S_A Hperp^A| <= C_S C_perp E_Dq,H.
```

So `Hperp` is no longer a foggy missing function; it is a componentwise `Dq` defect.

## Still Missing

All `Dq_i[H_L]` component values, `C_S`, `C_perp`, budget owner and arena projections are unfilled.

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
            "claim": "4243 reduces the live Hperp source row to componentwise Dq defects: Hperp=0 follows if every Dq_i[H_L] component vanishes, otherwise |S_A Hperp| <= C_S C_perp E_Dq,H. This is private nonclaim until component values and norms are sourced.",
            "current_evidence": "4243 source register, Hperp theorem rows, Dq component matrix, source-defect bound rows, input-fill ledger, decision and firewall.",
            "status": "private_Hperp_Dq_defect_bound_nonclaim",
            "next_test": "Adopt/prove all Dq component zeros for H_L or fill source-backed Dq component bounds plus C_S/C_perp.",
            "key_risk": "Geometry-only quotient silence would overclaim; source/readout, matter, EM and coefficient components must also vanish or be bounded.",
        }
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def update_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 Hperp Dq Defect Bound

Marker: `{MARKER}`

4243 reduces the live cGamma source row:

```text
S_A Hperp^A
```

to a componentwise quotient-defect bound:

```text
|S_A Hperp^A| <= C_S C_perp E_Dq,H,
E_Dq,H^2 = sum_i w_i ||Dq_i[H_L]||^2.
```

The exact-zero route is now all componentwise `Dq_i[H_L]=0`; otherwise these components become source-backed bound rows.
"""
    packet_block = f"""
## Packet Update - Hperp Dq Defect Bound

Marker: `{PACKET_MARKER}`

The local cGamma branch no longer treats `Hperp` as an undefined profile. It is a Dq-defect vector with explicit geometry, tau, matter, source-readout, marker, boundary, EM and coefficient rows.
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
    theorem = hperp_theorem_rows()
    components = dq_component_rows()
    bounds = source_defect_bound_rows()
    inputs = input_fill_rows()
    all_rows = [row for group in all_generated_groups() for row in group]

    add("VAL4243_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources), "source register")
    add("VAL4243_1_needles_found", "all source needles found", all(row["required_text_found"] == "True" for row in sources), "source register")
    add("VAL4243_2_Hperp_defined", "Hperp definition row exists", any(row["formula"] == "Hperp := (1 - Pi_kerDq) H_L" for row in theorem), "theorem rows")
    add("VAL4243_3_Dq_zero_route", "all-Dq zero route exists", any("all_i Dq_i[H_L]=0" in row["formula"] for row in theorem), "theorem rows")
    add("VAL4243_4_source_bound", "source bound row exists", any("C_S C_perp E_Dq,H" in row["formula"] for row in bounds), "bound rows")
    add("VAL4243_5_components", "eight Dq components listed", len(components) == 8 and all(row["zero_for_Hperp_claim"] == "required" for row in components), "Dq component rows")
    add("VAL4243_6_missing_values", "component values remain missing/nonclaim", all(row["numeric_value"] == "MISSING" and row["valid_for_claim"] == "False" for row in components), "Dq component rows")
    add("VAL4243_7_input_fill", "input fill rows include CS Cperp EDqH", {"C_S", "C_perp", "E_Dq,H"}.issubset({row["quantity"] for row in inputs}), "input fill rows")
    add("VAL4243_8_decision_nonclaim", "decision keeps scoreable false", decision_rows()[0]["scoreable_now"] == "False", "decision")
    add("VAL4243_9_docs_written", "formal and checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), f"{FORMAL_PATH}; {DOC_PATH}")
    add("VAL4243_10_claim_register", "claims register contains L-084", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), str(FORMAL / "02-claims-register.csv"))
    add("VAL4243_11_spine_marker", "spine contains marker", MARKER in read_text(FORMAL / "07-unification-spine.md"), str(FORMAL / "07-unification-spine.md"))
    add("VAL4243_12_packet_marker", "packet contains marker", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), str(FORMAL / "180-PPC4161-private-local-packet-integration.md"))
    add("VAL4243_13_no_claim_flags", "no generated row is valid for claim", all(row.get("valid_for_claim") != "True" for row in all_rows), "all generated groups")
    add("VAL4243_14_next_target", "next target selected", next_target_rows()[0]["next_target"] == NEXT_TARGET, NEXT_TARGET)
    return rows


def main() -> None:
    paths = {
        "source": SOURCE_DIR / "P8_Y5_R2FR_4243_SOURCE_REGISTER.csv",
        "theorem": SOURCE_DIR / "P8_Y5_R2FR_4243_HPERP_DQ_THEOREM.csv",
        "components": SOURCE_DIR / "P8_Y5_R2FR_4243_DQ_COMPONENT_BOUND_MATRIX.csv",
        "bounds": SOURCE_DIR / "P8_Y5_R2FR_4243_SOURCE_DEFECT_BOUND_ROWS.csv",
        "inputs": SOURCE_DIR / "P8_Y5_R2FR_4243_INPUT_FILL_LEDGER.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4243_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4243_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4243_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4243_NEXT_TARGET.csv",
    }
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    write_csv(paths["source"], source_rows())
    write_csv(paths["theorem"], hperp_theorem_rows())
    write_csv(paths["components"], dq_component_rows())
    write_csv(paths["bounds"], source_defect_bound_rows())
    write_csv(paths["inputs"], input_fill_rows())
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
