from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4248"
CLAIM_ID = "L-089"
BRANCH = "MTS_R2FR_Y5_EPSILON_GEOM_PROFILE_SAMPLER_COFRAME_FIRST_ROW_4248"
DECISION = "EPSILON_GEOM_SAMPLER_BUILT_COFRAME_SHADOW_BOUND_FIRST_ROW_READY_NUMERIC_INPUTS_MISSING_NONCLAIM"
MARKER = "PPC4161_EPSILON_GEOM_SAMPLER_COFRAME_ROW_4248"
PACKET_MARKER = "PPC4161_PACKET_EPSILON_GEOM_SAMPLER_COFRAME_ROW_4248"
NEXT_TARGET = "4249-Y5-R2FR-fill-hU-response-or-coframe-transfer-constant-first-source-row.md"

FORMAL_PATH = FORMAL / "264-PPC4161-epsilon-geom-profile-sampler-or-coframe-shadow-bound-first-row.md"
DOC_PATH = POST / "4248-Y5-R2FR-epsilon-geom-profile-sampler-or-coframe-shadow-bound-first-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4248_VALIDATION.csv"
CANDIDATE_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4248_EPSILON_GEOM_PROFILE_INPUTS_CANDIDATE.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4248_00_4247_next": SourceSpec(
        "SRC4248_00_4247_next",
        SOURCE_DIR / "P8_Y5_R2FR_4247_NEXT_TARGET.csv",
        "4248-Y5-R2FR-epsilon-geom-profile-sampler-or-coframe-shadow-bound-first-row.md",
        "4247 selected epsilon_geom sampler/coframe first row.",
    ),
    "SRC4248_01_4247_formal": SourceSpec(
        "SRC4248_01_4247_formal",
        FORMAL / "263-PPC4161-motion-frame-no-shadow-signature-or-epsilon-geom-numeric-fill.md",
        "epsilon_geom_L1",
        "4247 numeric-fill contract.",
    ),
    "SRC4248_02_4247_contract": SourceSpec(
        "SRC4248_02_4247_contract",
        SOURCE_DIR / "P8_Y5_R2FR_4247_EPSILON_GEOM_NUMERIC_FILL_CONTRACT.csv",
        "epsilon_coframe",
        "4247 epsilon_geom fill pieces.",
    ),
    "SRC4248_03_4247_template": SourceSpec(
        "SRC4248_03_4247_template",
        SOURCE_DIR / "P8_Y5_R2FR_4247_EPSILON_GEOM_TEMPLATE_ROWS.csv",
        "MISSING_HPERP_PROFILE",
        "4247 invalid template row.",
    ),
    "SRC4248_04_3799_theorem": SourceSpec(
        "SRC4248_04_3799_theorem",
        SOURCE_DIR / "P8_Y5_R2FR_3799_HPERP_CURVATURE_DESCENT_THEOREM.csv",
        "h_U_response",
        "3799 derived fallback Hperp response amplitude.",
    ),
    "SRC4248_05_3799_audit": SourceSpec(
        "SRC4248_05_3799_audit",
        SOURCE_DIR / "P8_Y5_R2FR_3799_CURRENT_CORPUS_HPERP_AUDIT.csv",
        "MISSING_HU_AND_TRANSFER_COEFFICIENTS",
        "3799 says h_U numerator and transfer coefficients are missing.",
    ),
    "SRC4248_06_3799_doc": SourceSpec(
        "SRC4248_06_3799_doc",
        POST / "3799-Y5-R2FR-Hperp-curvature-descent-zero-or-first-hU-source-row.md",
        "h_U_response=max_A",
        "3799 doc defines h_U response source row.",
    ),
    "SRC4248_07_3796_profile_rows": SourceSpec(
        "SRC4248_07_3796_profile_rows",
        SOURCE_DIR / "P8_Y5_R2FR_3796_FIRST_BPERP_PROFILE_ROWS.csv",
        "Hperp_norm_over_Fref",
        "Existing Hperp profile rows are missing/nonclaim.",
    ),
    "SRC4248_08_3796_doc": SourceSpec(
        "SRC4248_08_3796_doc",
        POST / "3796-Y5-R2FR-Qshear-eigenframe-chart-or-first-Bperp-arena-fill.md",
        "MISSING_QSHEAR_EIGENFRAME_CHART_OR_HPERP_PROFILE",
        "Q-shear/eigenframe Hperp profile source gap.",
    ),
    "SRC4248_09_230_projector": SourceSpec(
        "SRC4248_09_230_projector",
        FORMAL / "230-PPC4161-projector-stress-curl-zero-or-bound.md",
        "D_v e_obs = 0",
        "Coframe zero clause for q-basic observed-coframe selector.",
    ),
    "SRC4248_10_197_EH": SourceSpec(
        "SRC4248_10_197_EH",
        FORMAL / "197-PPC4161-EH-local-metric-principal-block-origin-gate.md",
        "current_MTS_EH_derivation = false",
        "Current local metric/coframe origin is not parent-derived.",
    ),
}


NUMERIC_COLUMNS = [
    "h_U_response",
    "C_coframe_hU",
    "epsilon_Q_projector",
    "C_coframe_projector",
    "epsilon_eigenchart",
    "C_coframe_eigenchart",
    "epsilon_eigen_degeneracy",
    "C_coframe_degeneracy",
    "epsilon_Pi4_selector",
    "C_coframe_selector",
    "epsilon_wall",
    "epsilon_Hodge_geom",
    "epsilon_Oloc",
    "epsilon_projector",
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


def parse_optional_float(value: Optional[str]) -> Optional[float]:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.upper().startswith("MISSING"):
        return None
    try:
        parsed = float(text)
    except ValueError:
        return None
    if parsed < 0:
        return None
    return parsed


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


def profile_asset_audit_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "AS4248_0_4247_template",
            str(SOURCE_DIR / "P8_Y5_R2FR_4247_EPSILON_GEOM_TEMPLATE_ROWS.csv"),
            "template_exists_invalid",
            "contains MISSING_HPERP_PROFILE; not a numeric source",
        ),
        (
            "AS4248_1_3796_Hperp_rows",
            str(SOURCE_DIR / "P8_Y5_R2FR_3796_FIRST_BPERP_PROFILE_ROWS.csv"),
            "profile_rows_exist_missing_values",
            "Hperp profile rows are present but explicitly missing/nonclaim",
        ),
        (
            "AS4248_2_3799_hU_rows",
            str(POST / "3799-Y5-R2FR-Hperp-curvature-descent-zero-or-first-hU-source-row.md"),
            "hU_definition_exists_values_missing",
            "h_U_profile and h_U_response are defined but not numerically filled",
        ),
        (
            "AS4248_3_candidate_input",
            str(CANDIDATE_INPUT_PATH),
            "candidate_input_missing" if not CANDIDATE_INPUT_PATH.exists() else "candidate_input_present",
            "4248 will compute only if candidate rows contain positive numeric values and real source paths",
        ),
    ]
    return [
        {
            **common(),
            "asset_id": asset_id,
            "path": path,
            "status": status,
            "notes": notes,
            "valid_for_claim": "False",
        }
        for asset_id, path, status, notes in rows
    ]


def sampler_law_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "law_id": "LAW4248_0_hU_to_coframe",
            "quantity": "epsilon_coframe",
            "formula": "epsilon_coframe <= C_coframe_hU*h_U_response + C_coframe_projector*epsilon_Q_projector + C_coframe_eigenchart*epsilon_eigenchart + C_coframe_degeneracy*epsilon_eigen_degeneracy + C_coframe_selector*epsilon_Pi4_selector",
            "derivation_status": "derived_transfer_envelope_nonclaim",
            "meaning": "Coframe shadow is bounded by Hperp vertical response plus Q-shear chart/projector/degeneracy/selector defects.",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "law_id": "LAW4248_1_total_geom",
            "quantity": "epsilon_geom_L1",
            "formula": "epsilon_geom_L1 = epsilon_Oloc + epsilon_coframe + epsilon_projector + epsilon_wall + epsilon_Hodge_geom",
            "derivation_status": "4247_L1_contract_imported",
            "meaning": "Total geometry component bound keeps no-cancellation absolute sum.",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "law_id": "LAW4248_2_zero_route",
            "quantity": "epsilon_coframe=0",
            "formula": "h_U_response=epsilon_Q_projector=epsilon_eigenchart=epsilon_eigen_degeneracy=epsilon_Pi4_selector=0 => epsilon_coframe=0",
            "derivation_status": "conditional_zero_route",
            "meaning": "The zero route is still derivable if Hperp basicness and Q-shear chart ownership close.",
            "valid_for_claim": "False",
        },
    ]


def input_schema_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = [
        {
            **common(),
            "field": "system_id",
            "required": "True",
            "units": "label",
            "description": "local system or arena label",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "field": "collar_id",
            "required": "True",
            "units": "label",
            "description": "compact local collar / U_good identifier",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "field": "Hperp_profile_id",
            "required": "True",
            "units": "label",
            "description": "source profile id for Hperp or theorem-zero certificate",
            "valid_for_claim": "False",
        },
    ]
    for field in NUMERIC_COLUMNS:
        rows.append(
            {
                **common(),
                "field": field,
                "required": "True",
                "units": "dimensionless_nonnegative",
                "description": f"nonnegative input for {field}",
                "valid_for_claim": "False",
            }
        )
    rows.extend(
        [
            {
                **common(),
                "field": "source_path",
                "required": "True",
                "units": "path",
                "description": "real local source path for the profile/theorem values",
                "valid_for_claim": "False",
            },
            {
                **common(),
                "field": "valid_for_claim",
                "required": "True",
                "units": "boolean",
                "description": "must remain false unless every numeric and source-path gate is satisfied",
                "valid_for_claim": "False",
            },
        ]
    )
    return rows


def first_coframe_bound_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "row_id": "ECB4248_0_first_coframe_shadow_bound",
            "quantity": "epsilon_coframe",
            "formula": "epsilon_coframe <= C_coframe_hU*h_U_response + C_coframe_projector*epsilon_Q_projector + C_coframe_eigenchart*epsilon_eigenchart + C_coframe_degeneracy*epsilon_eigen_degeneracy + C_coframe_selector*epsilon_Pi4_selector",
            "primary_missing_inputs": "h_U_response;C_coframe_hU;epsilon_Q_projector;epsilon_eigenchart;epsilon_eigen_degeneracy;epsilon_Pi4_selector;transfer_constants",
            "source_bridge": "3799 h_U_response + 3796 Q-shear chart defects -> 4247 epsilon_coframe",
            "numeric_value": "MISSING",
            "units": "dimensionless_geometry_component_Dq_norm",
            "current_status": "first_coframe_shadow_bound_ready_numeric_inputs_missing",
            "valid_for_claim": "False",
        }
    ]


def compute_sampler_rows() -> List[Dict[str, str]]:
    if not CANDIDATE_INPUT_PATH.exists():
        return [
            {
                **common(),
                "sample_id": "DRY4248_0_no_candidate_input",
                "system_id": "MISSING",
                "collar_id": "MISSING",
                "input_status": "NO_CANDIDATE_INPUT_FILE",
                "epsilon_coframe": "MISSING",
                "epsilon_geom_L1": "MISSING",
                "source_path": str(CANDIDATE_INPUT_PATH),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        ]

    output_rows: List[Dict[str, str]] = []
    for index, row in enumerate(csv_rows(CANDIDATE_INPUT_PATH), start=1):
        missing_numeric = [field for field in NUMERIC_COLUMNS if parse_optional_float(row.get(field)) is None]
        source_path = row.get("source_path", "")
        source_exists = bool(source_path and Path(source_path).exists())
        valid_input_claim = row.get("valid_for_claim", "False") == "True"
        if missing_numeric or not source_exists or not valid_input_claim:
            output_rows.append(
                {
                    **common(),
                    "sample_id": f"DRY4248_{index}_blocked",
                    "system_id": row.get("system_id", "MISSING"),
                    "collar_id": row.get("collar_id", "MISSING"),
                    "input_status": "BLOCKED_MISSING_NUMERIC_OR_SOURCE_OR_CLAIM_FLAG",
                    "missing_numeric": ";".join(missing_numeric),
                    "epsilon_coframe": "MISSING",
                    "epsilon_geom_L1": "MISSING",
                    "source_path": source_path,
                    "claim_allowed": "False",
                    "valid_for_claim": "False",
                }
            )
            continue

        values = {field: parse_optional_float(row.get(field)) for field in NUMERIC_COLUMNS}
        epsilon_coframe = (
            values["C_coframe_hU"] * values["h_U_response"]
            + values["C_coframe_projector"] * values["epsilon_Q_projector"]
            + values["C_coframe_eigenchart"] * values["epsilon_eigenchart"]
            + values["C_coframe_degeneracy"] * values["epsilon_eigen_degeneracy"]
            + values["C_coframe_selector"] * values["epsilon_Pi4_selector"]
        )
        epsilon_geom = (
            values["epsilon_Oloc"]
            + epsilon_coframe
            + values["epsilon_projector"]
            + values["epsilon_wall"]
            + values["epsilon_Hodge_geom"]
        )
        output_rows.append(
            {
                **common(),
                "sample_id": f"DRY4248_{index}_computed_nonclaim",
                "system_id": row.get("system_id", "MISSING"),
                "collar_id": row.get("collar_id", "MISSING"),
                "input_status": "COMPUTED_FROM_CANDIDATE_INPUT_NONCLAIM",
                "missing_numeric": "",
                "epsilon_coframe": repr(epsilon_coframe),
                "epsilon_geom_L1": repr(epsilon_geom),
                "source_path": source_path,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return output_rows


def template_rows() -> List[Dict[str, str]]:
    base = {
        **common(),
        "system_id": "LOCAL_COLLAR_TEMPLATE",
        "collar_id": "MISSING_COLLAR_ID",
        "Hperp_profile_id": "MISSING_HPERP_PROFILE_OR_HU_RESPONSE",
    }
    for field in NUMERIC_COLUMNS:
        base[field] = "MISSING"
    base.update(
        {
            "source_path": "MISSING_SOURCE_PATH",
            "assumptions": "candidate row for 4248 sampler; all numeric values must be nonnegative and source-backed",
            "valid_for_claim": "False",
        }
    )
    return [base]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "DEC4248",
            "decision": DECISION,
            "scoreable_now": "False",
            "reason": "No real Hperp/h_U numeric source is present, but the coframe-shadow bound is now an executable transfer formula tied to 3799 h_U_response and 3796 Q-shear chart defects.",
            "selected_route": "Fill h_U_response or the coframe transfer constant first; then run the sampler to compute epsilon_coframe and epsilon_geom_L1.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rules = [
        ("FW4248_0_no_fake_profile", "Do not fabricate Hperp/h_U numeric values; missing inputs block the sampler."),
        ("FW4248_1_no_chart_smuggling", "Q-shear projector/eigenframe/Pi4 defects remain explicit pieces of epsilon_coframe."),
        ("FW4248_2_no_transfer_constant_guess", "C_coframe_* constants must be sourced or theorem-bounded before scoring."),
        ("FW4248_3_no_arena_claim", "epsilon_geom_L1 is not a PPN/R10/clock residual until arena projection constants are supplied."),
        ("FW4248_4_no_zero_claim", "The sampler computes bounds; it does not prove Hperp=0 or Dq_geom[Hperp]=0."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule in rules
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status": DECISION,
            "summary": "4248 builds the epsilon_geom sampler and first coframe-shadow bound row, tying epsilon_coframe to h_U_response and Q-shear chart defects. Numeric inputs are still missing/nonclaim.",
            "scoreable_now": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "task": "Fill or theorem-bound h_U_response or C_coframe_hU as the first source-backed input for the coframe-shadow sampler.",
            "reason": "The sampler is now ready; the next progress point is replacing one MISSING transfer/profile value with a sourced zero or finite bound.",
            "valid_for_claim": "False",
        }
    ]


def all_generated_groups() -> List[List[Dict[str, str]]]:
    return [
        source_rows(),
        profile_asset_audit_rows(),
        sampler_law_rows(),
        input_schema_rows(),
        first_coframe_bound_rows(),
        compute_sampler_rows(),
        template_rows(),
        decision_rows(),
        firewall_rows(),
        status_rows(),
        next_target_rows(),
    ]


def formal_doc() -> str:
    return f"""
# 264 - PPC4161 epsilon_geom profile sampler or coframe-shadow bound first row

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. 4248 does not supply real local-GR evidence, PPN/R10/clock safety, or a public claim. It builds the sampler and first coframe-shadow bound row.

## Source Bridge

4247 left:

```text
epsilon_geom_L1 = epsilon_Oloc + epsilon_coframe + epsilon_projector + epsilon_wall + epsilon_Hodge_geom.
```

The existing 3799 Hperp chain gives the usable upstream amplitude:

```text
h_U_response := max_A || q_*^{-1} Lie_EA Hperp ||_F / F_ref.
```

So 4248 ties the first fillable geometry piece to that Hperp response:

```text
epsilon_coframe
<= C_coframe_hU h_U_response
 + C_coframe_projector epsilon_Q_projector
 + C_coframe_eigenchart epsilon_eigenchart
 + C_coframe_degeneracy epsilon_eigen_degeneracy
 + C_coframe_selector epsilon_Pi4_selector.
```

This is not decoration. It means the coframe-shadow row is no longer free-floating: it is controlled by the same Hperp/Q-shear basicness debt already derived in 3796-3799.

## Executable Sampler Contract

The sampler reads candidate rows from:

```text
P8_Y5_R2FR_4248_EPSILON_GEOM_PROFILE_INPUTS_CANDIDATE.csv
```

and writes:

```text
P8_Y5_R2FR_4248_EPSILON_GEOM_SAMPLER_RESULTS.csv.
```

It computes only when every numeric input is nonnegative, the source path exists, and the candidate input is explicitly marked source-ready. Otherwise it emits `MISSING` and `valid_for_claim=false`.

## First Bound Row

The first live row is:

```text
epsilon_coframe <= C_coframe_hU*h_U_response + chart/projector/degeneracy/selector terms.
```

The next hard input is either:

```text
h_U_response = 0 or finite sourced bound,
```

or

```text
C_coframe_hU = sourced transfer constant.
```

## Next Target

`{NEXT_TARGET}` should fill or theorem-bound `h_U_response` or `C_coframe_hU`.
"""


def checkpoint_doc() -> str:
    return f"""
# 4248 - epsilon_geom profile sampler or coframe-shadow bound first row

**Status:** `{DECISION}`.

## Result

The `epsilon_geom` numeric-fill route now has an executable sampler and first coframe-shadow bound:

```text
epsilon_coframe
<= C_coframe_hU*h_U_response
 + C_coframe_projector*epsilon_Q_projector
 + C_coframe_eigenchart*epsilon_eigenchart
 + C_coframe_degeneracy*epsilon_eigen_degeneracy
 + C_coframe_selector*epsilon_Pi4_selector.
```

## Current state

No candidate numeric profile exists yet, so the sampler emits `MISSING` rows and keeps `valid_for_claim=false`.

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
        "claim": "4248 builds an executable epsilon_geom profile sampler and the first coframe-shadow bound row. epsilon_coframe is now tied to 3799 h_U_response plus Q-shear projector/eigenchart/degeneracy/selector defects, but numeric profile and transfer inputs remain missing.",
        "current_evidence": "4248 source register, profile asset audit, sampler laws, input schema, first coframe bound row, sampler dry-run results, decision and firewall.",
        "status": "private_epsilon_geom_sampler_ready_numeric_inputs_missing_nonclaim",
        "next_test": "Fill or theorem-bound h_U_response or C_coframe_hU, then rerun the sampler on source-backed candidate rows.",
        "key_risk": "Treating the sampler formula as a numeric local-GR pass would hide missing Hperp profiles and coframe transfer constants.",
    }
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def update_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 epsilon_geom sampler / coframe shadow row

Marker: `{MARKER}`

4248 makes the first geometry profile sampler executable:

```text
epsilon_coframe <= C_coframe_hU*h_U_response
 + C_coframe_projector*epsilon_Q_projector
 + C_coframe_eigenchart*epsilon_eigenchart
 + C_coframe_degeneracy*epsilon_eigen_degeneracy
 + C_coframe_selector*epsilon_Pi4_selector.
```

The route now waits on a source-backed `h_U_response` or coframe transfer constant, not on an undefined geometry leak.
"""
    packet_block = f"""
## Packet Update - epsilon_geom sampler

Marker: `{PACKET_MARKER}`

The local geometry residual has an executable sampler contract. It keeps outputs invalid for claim until source-backed Hperp response and transfer constants are present.
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
    assets = profile_asset_audit_rows()
    laws = sampler_law_rows()
    schema = input_schema_rows()
    first = first_coframe_bound_rows()
    results = compute_sampler_rows()
    all_rows = [row for group in all_generated_groups() for row in group]

    add("VAL4248_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources), "source register")
    add("VAL4248_1_needles_found", "all source needles found", all(row["required_text_found"] == "True" for row in sources), "source register")
    add("VAL4248_2_assets_audited", "profile assets are audited", len(assets) == 4, "asset audit")
    add("VAL4248_3_hU_bridge", "sampler law includes h_U_response", any("h_U_response" in row["formula"] for row in laws), "sampler laws")
    add("VAL4248_4_coframe_first_row", "first coframe bound row exists", first[0]["quantity"] == "epsilon_coframe" and "C_coframe_hU" in first[0]["formula"], "first coframe row")
    add("VAL4248_5_schema_numeric_fields", "input schema includes all numeric columns", set(NUMERIC_COLUMNS).issubset({row["field"] for row in schema}), "input schema")
    add("VAL4248_6_sampler_blocks_missing", "sampler blocks missing candidate input or invalid rows", all(row["valid_for_claim"] == "False" for row in results), "sampler results")
    add("VAL4248_7_template_invalid", "template remains invalid for claim", template_rows()[0]["valid_for_claim"] == "False" and template_rows()[0]["h_U_response"] == "MISSING", "template")
    add("VAL4248_8_decision_nonclaim", "decision keeps scoreable false", decision_rows()[0]["scoreable_now"] == "False", "decision")
    add("VAL4248_9_docs_written", "formal and checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), f"{FORMAL_PATH}; {DOC_PATH}")
    add("VAL4248_10_claim_register", "claims register contains L-089", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), str(FORMAL / "02-claims-register.csv"))
    add("VAL4248_11_spine_marker", "spine contains marker", MARKER in read_text(FORMAL / "07-unification-spine.md"), str(FORMAL / "07-unification-spine.md"))
    add("VAL4248_12_packet_marker", "packet contains marker", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), str(FORMAL / "180-PPC4161-private-local-packet-integration.md"))
    add("VAL4248_13_no_claim_flags", "no generated row is valid for claim", all(row.get("valid_for_claim") != "True" for row in all_rows), "all generated groups")
    add("VAL4248_14_next_target", "next target selected", next_target_rows()[0]["next_target"] == NEXT_TARGET, NEXT_TARGET)
    return rows


def main() -> None:
    paths = {
        "source": SOURCE_DIR / "P8_Y5_R2FR_4248_SOURCE_REGISTER.csv",
        "asset": SOURCE_DIR / "P8_Y5_R2FR_4248_PROFILE_ASSET_AUDIT.csv",
        "laws": SOURCE_DIR / "P8_Y5_R2FR_4248_SAMPLER_LAWS.csv",
        "schema": SOURCE_DIR / "P8_Y5_R2FR_4248_EPSILON_GEOM_PROFILE_INPUT_SCHEMA.csv",
        "first": SOURCE_DIR / "P8_Y5_R2FR_4248_COFRAME_SHADOW_BOUND_FIRST_ROW.csv",
        "results": SOURCE_DIR / "P8_Y5_R2FR_4248_EPSILON_GEOM_SAMPLER_RESULTS.csv",
        "template": SOURCE_DIR / "P8_Y5_R2FR_4248_EPSILON_GEOM_PROFILE_INPUTS_TEMPLATE.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4248_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4248_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4248_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4248_NEXT_TARGET.csv",
    }
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    write_csv(paths["source"], source_rows())
    write_csv(paths["asset"], profile_asset_audit_rows())
    write_csv(paths["laws"], sampler_law_rows())
    write_csv(paths["schema"], input_schema_rows())
    write_csv(paths["first"], first_coframe_bound_rows())
    write_csv(paths["results"], compute_sampler_rows())
    write_csv(paths["template"], template_rows())
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
