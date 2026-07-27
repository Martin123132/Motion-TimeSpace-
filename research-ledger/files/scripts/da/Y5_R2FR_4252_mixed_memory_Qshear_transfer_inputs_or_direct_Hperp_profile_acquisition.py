from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4252"
CLAIM_ID = "L-093"
BRANCH = "MTS_R2FR_Y5_MIXED_MEMORY_QSHEAR_TRANSFER_INPUTS_OR_DIRECT_HPERP_PROFILE_ACQUISITION_4252"
DECISION = "MIXED_MEMORY_QSHEAR_SYMPLECTIC_EXTRACTOR_BUILT_DIRECT_PROFILE_BRANCH_STILL_SOURCE_BLOCKED_NONCLAIM"
MARKER = "PPC4161_MIXED_MEMORY_QSHEAR_TRANSFER_INPUTS_4252"
PACKET_MARKER = "PPC4161_PACKET_MIXED_MEMORY_QSHEAR_TRANSFER_INPUTS_4252"
NEXT_TARGET = "4253-Y5-R2FR-source-Jacobian-or-first-direct-Hperp-profile-fill.md"

FORMAL_PATH = FORMAL / "268-PPC4161-mixed-memory-Qshear-transfer-inputs-or-direct-Hperp-profile-acquisition.md"
DOC_PATH = POST / "4252-Y5-R2FR-mixed-memory-Qshear-transfer-inputs-or-direct-Hperp-profile-acquisition.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4252_VALIDATION.csv"

JACOBIAN_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4252_JACOBIAN_COMPONENTS_CANDIDATE.csv"
AGGREGATE_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4252_MIXED_TRANSFER_INPUTS_CANDIDATE.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
TARGET_COMPONENTS = ("C1", "D1", "C2", "D2")


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4252_00_4251_formal": SourceSpec(
        "SRC4252_00_4251_formal",
        FORMAL / "267-PPC4161-Hperp-memory-transfer-constant-or-real-profile-source.md",
        "Y_Q = Y_Q(m, Z^a)",
        "4251 handoff to mixed memory-Qshear transfer.",
    ),
    "SRC4252_01_4251_c1": SourceSpec(
        "SRC4252_01_4251_c1",
        FORMAL / "267-PPC4161-Hperp-memory-transfer-constant-or-real-profile-source.md",
        "h_U_C1 <= C_perp1*",
        "4251 C1 mixed-transfer envelope.",
    ),
    "SRC4252_02_3794_constructor": SourceSpec(
        "SRC4252_02_3794_constructor",
        POST / "3794-Y5-R2FR-parent-BQ-owner-constructor-two-pair-CP2-or-finite-profile.md",
        "H_Q=dC1 wedge dD1+dC2 wedge dD2",
        "Two-pair Clebsch parent constructor.",
    ),
    "SRC4252_03_3795_lift": SourceSpec(
        "SRC4252_03_3795_lift",
        POST / "3795-Y5-R2FR-Qflow-two-pair-lift-or-Bperp-profile-first-input.md",
        "A successful lift must supply",
        "Q-flow lift condition for Y_Q ownership.",
    ),
    "SRC4252_04_3796_chart": SourceSpec(
        "SRC4252_04_3796_chart",
        POST / "3796-Y5-R2FR-Qshear-eigenframe-chart-or-first-Bperp-arena-fill.md",
        "Y_Q=(C1,D1,C2,D2)",
        "Q-shear/eigenframe chart route.",
    ),
    "SRC4252_05_3800_pullback": SourceSpec(
        "SRC4252_05_3800_pullback",
        SOURCE_DIR / "P8_Y5_R2FR_3800_FULL_RANK_CLEBSCH_BASICNESS_THEOREM.csv",
        "CBT3800_3_qshear_chain_rule",
        "Pi4 chain rule for Q-shear selector derivatives.",
    ),
    "SRC4252_06_3801_selector": SourceSpec(
        "SRC4252_06_3801_selector",
        SOURCE_DIR / "P8_Y5_R2FR_3801_SELECTOR_LEAKAGE_FILL_ROWS.csv",
        "SLF3801_2_epsilon_YV",
        "Selector leakage finite branch inherited from 3801.",
    ),
    "SRC4252_07_4249_response": SourceSpec(
        "SRC4252_07_4249_response",
        FORMAL / "265-PPC4161-hU-response-bound-or-coframe-transfer-first-source-row.md",
        "h_U_C1 <= C_shape*A_H",
        "4249 response runner target for the Hperp C1 bound.",
    ),
    "SRC4252_08_4250_transition": SourceSpec(
        "SRC4252_08_4250_transition",
        SOURCE_DIR / "P8_Y5_R2FR_4250_TRANSITION_VALUE_EXTRACTION.csv",
        "M_tr_example",
        "4250 nonclaim transition scale, not a curvature transfer by itself.",
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


def append_once(path: Path, marker: str, block: str) -> None:
    current = read_text(path)
    if marker in current:
        return
    write_text(path, current.rstrip() + "\n\n" + block.strip())


def parse_float(value: str) -> Optional[float]:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def truthy(value: str) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def contains_missing_marker(values: Iterable[str]) -> bool:
    return any("MISSING_" in str(value) or "PLACEHOLDER" in str(value) for value in values)


def split_paths(value: str) -> List[Path]:
    if not value:
        return []
    return [Path(piece.strip()) for piece in str(value).split(";") if piece.strip()]


def all_source_paths_exist(value: str) -> bool:
    paths = split_paths(value)
    return bool(paths) and all(path.exists() for path in paths)


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
            "MMQ4252_0_pullback_components",
            "exact mixed pullback component law",
            "Let xi^I=(m,Z^a), Y^A=(C1,D1,C2,D2), and omega_AB be the fixed two-pair symplectic matrix. Then H_Q=Y_Q^*omega_0 has components H_IJ=omega_AB partial_I Y^A partial_J Y^B.",
            "EXACT_DIFFERENTIAL_FORM_COMPONENT_IDENTITY",
            "C_mZ and C_ZZ are no longer black-box constants; they are Jacobian contractions.",
            "MISSING_PARENT_YQ_OR_JACOBIAN_COMPONENTS",
        ),
        (
            "MMQ4252_1_mixed_Ba",
            "memory-Qshear coefficient",
            "B_a := H_ma = C1_m D1_a - C1_a D1_m + C2_m D2_a - C2_a D2_m.",
            "EXACT_SYMPLECTIC_JACOBIAN_CONTRACTION",
            "B_a is the exact bridge from memory transition to Q/shear curvature.",
            "MISSING_NUMERIC_OR_THEOREM_ZERO_Ba_ROWS",
        ),
        (
            "MMQ4252_2_pure_Gab",
            "pure Qshear coefficient",
            "G_ab := H_ab = C1_a D1_b - C1_b D1_a + C2_a D2_b - C2_b D2_a.",
            "EXACT_SYMPLECTIC_JACOBIAN_CONTRACTION",
            "G_ab captures shear/eigenframe curvature that survives even if the memory transition is small.",
            "MISSING_NUMERIC_OR_THEOREM_ZERO_Gab_ROWS",
        ),
        (
            "MMQ4252_3_Pi4_chain_rule",
            "actual vertical generator map",
            "If Y_Q=Pi4(X_Q), then Y_m=D Pi4_X X_m and Y_a=D Pi4_X X_a, so B_a=omega(DPi4 X_m,DPi4 X_a) and G_ab=omega(DPi4 X_a,DPi4 X_b).",
            "EXACT_CHAIN_RULE_FROM_3800",
            "This maps DCdagger-style symbolic language onto the actual vertical/shear generator.",
            "MISSING_PARENT_PI4_Xm_Xa_COMPONENTS",
        ),
        (
            "MMQ4252_4_amplitude_bound",
            "amplitude envelope",
            "With C_mZ=sum_a |B_a|, C_ZZ=sum_a<b |G_ab|, |dm|<=M_tr, and |dZ|<=Z_1, A_H <= C_perp*(C_mZ M_tr Z_1 + C_ZZ Z_1^2 + eta_chart + eta_qproj + eta_background).",
            "DERIVED_BOUND_READY_FOR_SOURCE_ROWS",
            "The 4251 amplitude law now has an extraction recipe.",
            "MISSING_C_mZ_C_ZZ_Z1_Cperp_ETA_VALUES",
        ),
        (
            "MMQ4252_5_C1_bound",
            "C1/profile envelope",
            "With Z_2 bounding the normalized derivative of dZ and L_U/ell_tr bounding the memory wall derivative, h_U_C1 <= C_perp1*(C_mZ M_tr (L_U/ell_tr) Z_1 + C_mZ M_tr Z_2 + C_mZ1 M_tr Z_1 + C_ZZ Z_1 Z_2 + C_ZZ1 Z_1^2 + eta_C1).",
            "DERIVED_C1_BOUND_READY_FOR_SOURCE_ROWS",
            "The C1 branch no longer has to invent C_HM1; it needs Jacobian/profile derivative rows.",
            "MISSING_Z2_C1_TRANSFER_AND_PROFILE_VALUES",
        ),
        (
            "MMQ4252_6_direct_profile_fallback",
            "direct Hperp profile branch",
            "If the parent Jacobian cannot be sourced, the honest alternative is a direct profile: A_H=||Hperp||_F/F_ref and h_U_C1=max||nabla Hperp||/(F_ref/L_U) on U_good.",
            "DIRECT_PROFILE_ACQUISITION_ROUTE",
            "This is the non-smuggling fallback into the 4249 response runner.",
            "MISSING_REAL_HPERP_PROFILE_SOURCE",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "mathematical_form": mathematical_form,
            "derivation_status": status,
            "result_if_signed": result,
            "missing_for_current_claim": missing,
            "valid_for_claim": "False",
        }
        for theorem_id, claim_piece, mathematical_form, status, result, missing in raw
    ]


def coefficient_contract_rows() -> List[Dict[str, str]]:
    raw = [
        ("xi^I", "local coordinate split", "xi=(m,Z^a)", "m is transition memory; Z^a are Q/shear/eigenframe coordinates"),
        ("omega_AB", "fixed Clebsch symplectic form", "omega=dC1 wedge dD1+dC2 wedge dD2", "must be parent-fixed, not fitted from EM readout"),
        ("Y_m", "memory derivative of Clebsch map", "partial_m Y^A or DPi4_X X_m", "source by parent map or theorem zero"),
        ("Y_a", "Q/shear derivative of Clebsch map", "partial_a Y^A or DPi4_X X_a", "source by parent map or theorem zero"),
        ("B_a", "mixed coefficient", "omega_AB Y_m^A Y_a^B", "exact row needed for C_mZ"),
        ("G_ab", "pure Q/shear coefficient", "omega_AB Y_a^A Y_b^B", "exact row needed for C_ZZ"),
        ("C_mZ", "mixed envelope norm", "sum_a |B_a| or declared stronger norm", "feeds A_H and h_U_C1"),
        ("C_ZZ", "pure Q/shear envelope norm", "sum_a<b |G_ab| or declared stronger norm", "feeds A_H and h_U_C1"),
        ("Z_1", "normalized Q/shear first profile", "max_a ||dZ^a||", "must be sourced on U_good"),
        ("Z_2", "normalized Q/shear C1 profile", "max_a ||nabla dZ^a|| in L_U units", "keeps C1 law honest"),
    ]
    return [
        {
            **common(),
            "symbol": symbol,
            "role": role,
            "formula": formula,
            "source_requirement": requirement,
            "valid_for_claim": "False",
        }
        for symbol, role, formula, requirement in raw
    ]


def jacobian_template_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for direction in ("m", "Z:z1", "Z:z2"):
        for component in TARGET_COMPONENTS:
            rows.append(
                {
                    **common(),
                    "candidate_id": "TEMPLATE_ONLY",
                    "derivative_direction": direction,
                    "target_component": component,
                    "value": "MISSING_PARENT_JACOBIAN_COMPONENT",
                    "units": "dimensionless_normalized",
                    "source_path": "MISSING_SOURCE_PATH",
                    "valid_for_claim": "False",
                    "notes": "Copy to P8_Y5_R2FR_4252_JACOBIAN_COMPONENTS_CANDIDATE.csv with sourced numeric rows to compute B_a, G_ab, C_mZ, and C_ZZ.",
                }
            )
    return rows


def aggregate_template_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "candidate_id": "TEMPLATE_ONLY",
            "C_perp": "MISSING_C_PERP",
            "C_mZ": "MISSING_C_mZ",
            "M_tr": "MISSING_M_tr",
            "Z_1": "MISSING_Z_1",
            "C_ZZ": "MISSING_C_ZZ",
            "eta_chart": "MISSING_eta_chart",
            "eta_qproj": "MISSING_eta_qproj",
            "eta_background": "MISSING_eta_background",
            "C_perp1": "MISSING_C_perp1",
            "L_U_over_ell_tr": "MISSING_L_U_over_ell_tr",
            "Z_2": "MISSING_Z_2_OR_ZERO_CERTIFICATE",
            "C_mZ1": "MISSING_C_mZ1",
            "C_ZZ1": "MISSING_C_ZZ1",
            "eta_C1": "MISSING_eta_C1",
            "source_path": "MISSING_SOURCE_PATH",
            "claim_authority": "MISSING_PARENT_AUTHORITY",
            "valid_for_claim": "False",
            "notes": "Aggregate input row for the mixed transfer runner. Rows remain nonclaim unless every numeric value and source path is parent-owned/source-backed.",
        }
    ]


def direct_profile_template_rows() -> List[Dict[str, str]]:
    raw = [
        ("Hperp_profile_path", "direct source path for Hperp on U_good", "path", "MISSING_REAL_HPERP_PROFILE"),
        ("F_ref", "curvature two-form normalization", "curvature_units", "MISSING_F_REF"),
        ("A_H", "||Hperp||_F/F_ref", "dimensionless", "MISSING_A_H"),
        ("h_U_C1", "max||nabla Hperp||/(F_ref/L_U)", "dimensionless", "MISSING_h_U_C1"),
        ("U_good_domain", "local patch/domain definition", "source_path_or_text", "MISSING_U_GOOD"),
        ("boundary_degeneracy_budget", "excluded/controlled bad-set residue", "dimensionless", "MISSING_BOUNDARY_DEGEN_BUDGET"),
    ]
    return [
        {
            **common(),
            "symbol": symbol,
            "definition": definition,
            "units": units,
            "current_value": current_value,
            "required_for_claim": "True",
            "valid_for_claim": "False",
        }
        for symbol, definition, units, current_value in raw
    ]


def component_key(row: Dict[str, str]) -> Tuple[str, str, str]:
    return (
        row.get("candidate_id", "").strip(),
        row.get("derivative_direction", "").strip(),
        row.get("target_component", "").strip(),
    )


def candidate_valid_from_rows(rows: List[Dict[str, str]]) -> bool:
    if not rows:
        return False
    return (
        all(truthy(row.get("valid_for_claim", "")) for row in rows)
        and all(all_source_paths_exist(row.get("source_path", "")) for row in rows)
        and not contains_missing_marker(value for row in rows for value in row.values())
    )


def collect_candidate_components(rows: List[Dict[str, str]]) -> Dict[str, Dict[str, Dict[str, float]]]:
    grouped: Dict[str, Dict[str, Dict[str, float]]] = {}
    for row in rows:
        candidate_id, direction, component = component_key(row)
        if not candidate_id or not direction or component not in TARGET_COMPONENTS:
            continue
        parsed = parse_float(row.get("value", ""))
        if parsed is None:
            continue
        grouped.setdefault(candidate_id, {}).setdefault(direction, {})[component] = parsed
    return grouped


def mixed_B(memory: Dict[str, float], shear: Dict[str, float]) -> float:
    return (
        memory["C1"] * shear["D1"]
        - shear["C1"] * memory["D1"]
        + memory["C2"] * shear["D2"]
        - shear["C2"] * memory["D2"]
    )


def pure_G(first: Dict[str, float], second: Dict[str, float]) -> float:
    return (
        first["C1"] * second["D1"]
        - second["C1"] * first["D1"]
        + first["C2"] * second["D2"]
        - second["C2"] * first["D2"]
    )


def jacobian_extraction_rows() -> List[Dict[str, str]]:
    if not JACOBIAN_CANDIDATE_PATH.exists():
        return [
            {
                **common(),
                "candidate_id": "NO_JACOBIAN_COMPONENT_FILE",
                "row_type": "blocked",
                "status": "BLOCKED_NO_COMPONENT_ROWS",
                "required_file": str(JACOBIAN_CANDIDATE_PATH),
                "B_a": "",
                "G_ab": "",
                "C_mZ_l1": "",
                "C_ZZ_l1": "",
                "claim_allowed": "False",
                "valid_for_claim": "False",
                "notes": "Create sourced rows from the Jacobian template to compute mixed coefficients.",
            }
        ]

    rows = csv_rows(JACOBIAN_CANDIDATE_PATH)
    grouped = collect_candidate_components(rows)
    by_candidate_input: Dict[str, List[Dict[str, str]]] = {}
    for row in rows:
        candidate_id = row.get("candidate_id", "").strip()
        if candidate_id:
            by_candidate_input.setdefault(candidate_id, []).append(row)

    output: List[Dict[str, str]] = []
    for candidate_id, components in grouped.items():
        memory = components.get("m", {})
        shear_keys = sorted(key for key in components if key.startswith("Z:"))
        input_valid = candidate_valid_from_rows(by_candidate_input.get(candidate_id, []))
        missing_memory = [component for component in TARGET_COMPONENTS if component not in memory]
        if missing_memory or not shear_keys:
            output.append(
                {
                    **common(),
                    "candidate_id": candidate_id,
                    "row_type": "blocked",
                    "status": "MISSING_MEMORY_OR_SHEAR_DIRECTIONS",
                    "missing": ";".join(missing_memory) if missing_memory else "MISSING_Z_DIRECTIONS",
                    "claim_allowed": "False",
                    "valid_for_claim": "False",
                }
            )
            continue

        B_values: Dict[str, float] = {}
        G_values: Dict[Tuple[str, str], float] = {}
        missing: List[str] = []
        for shear_key in shear_keys:
            shear = components[shear_key]
            missing_components = [component for component in TARGET_COMPONENTS if component not in shear]
            if missing_components:
                missing.append(f"{shear_key}:{'/'.join(missing_components)}")
                continue
            B_values[shear_key] = mixed_B(memory, shear)

        for index, first_key in enumerate(shear_keys):
            first = components[first_key]
            if any(component not in first for component in TARGET_COMPONENTS):
                continue
            for second_key in shear_keys[index + 1 :]:
                second = components[second_key]
                if any(component not in second for component in TARGET_COMPONENTS):
                    continue
                G_values[(first_key, second_key)] = pure_G(first, second)

        for shear_key, value in B_values.items():
            output.append(
                {
                    **common(),
                    "candidate_id": candidate_id,
                    "row_type": "B_a",
                    "coefficient": f"B_{shear_key[2:]}",
                    "value": f"{value:.12e}",
                    "formula": "C1_m D1_a - C1_a D1_m + C2_m D2_a - C2_a D2_m",
                    "claim_allowed": "False",
                    "valid_for_claim": str(input_valid),
                }
            )
        for (first_key, second_key), value in G_values.items():
            output.append(
                {
                    **common(),
                    "candidate_id": candidate_id,
                    "row_type": "G_ab",
                    "coefficient": f"G_{first_key[2:]}_{second_key[2:]}",
                    "value": f"{value:.12e}",
                    "formula": "C1_a D1_b - C1_b D1_a + C2_a D2_b - C2_b D2_a",
                    "claim_allowed": "False",
                    "valid_for_claim": str(input_valid),
                }
            )
        c_mz_l1 = sum(abs(value) for value in B_values.values())
        c_zz_l1 = sum(abs(value) for value in G_values.values())
        output.append(
            {
                **common(),
                "candidate_id": candidate_id,
                "row_type": "summary",
                "status": "JACOBIAN_COEFFICIENTS_COMPUTED_NONCLAIM" if not missing else "PARTIAL_JACOBIAN_COEFFICIENTS_COMPUTED_NONCLAIM",
                "C_mZ_l1": f"{c_mz_l1:.12e}",
                "C_ZZ_l1": f"{c_zz_l1:.12e}",
                "n_B": str(len(B_values)),
                "n_G": str(len(G_values)),
                "missing": ";".join(missing),
                "claim_allowed": "False",
                "valid_for_claim": str(input_valid and not missing),
            }
        )

    if not output:
        return [
            {
                **common(),
                "candidate_id": "NO_VALID_JACOBIAN_COMPONENT_ROWS",
                "row_type": "blocked",
                "status": "BLOCKED_NO_PARSEABLE_COMPONENTS",
                "required_file": str(JACOBIAN_CANDIDATE_PATH),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        ]
    return output


AGGREGATE_REQUIRED = (
    "C_perp",
    "C_mZ",
    "M_tr",
    "Z_1",
    "C_ZZ",
    "eta_chart",
    "eta_qproj",
    "eta_background",
    "C_perp1",
    "L_U_over_ell_tr",
    "Z_2",
    "C_mZ1",
    "C_ZZ1",
    "eta_C1",
)


def aggregate_transfer_results() -> List[Dict[str, str]]:
    if not AGGREGATE_CANDIDATE_PATH.exists():
        return [
            {
                **common(),
                "candidate_id": "NO_AGGREGATE_INPUT_FILE",
                "status": "BLOCKED_NO_MIXED_TRANSFER_INPUT_ROWS",
                "required_file": str(AGGREGATE_CANDIDATE_PATH),
                "A_H_bound": "",
                "h_U_C1_bound": "",
                "claim_allowed": "False",
                "valid_for_claim": "False",
                "notes": "Fill the aggregate candidate file from source-backed Jacobian/profile rows.",
            }
        ]

    rows = csv_rows(AGGREGATE_CANDIDATE_PATH)
    output: List[Dict[str, str]] = []
    for row in rows:
        candidate_id = row.get("candidate_id", "UNNAMED_CANDIDATE").strip() or "UNNAMED_CANDIDATE"
        parsed = {field: parse_float(row.get(field, "")) for field in AGGREGATE_REQUIRED}
        missing = [field for field, value in parsed.items() if value is None]
        input_valid = (
            truthy(row.get("valid_for_claim", ""))
            and all_source_paths_exist(row.get("source_path", ""))
            and not contains_missing_marker(row.values())
            and not missing
        )
        if missing:
            output.append(
                {
                    **common(),
                    "candidate_id": candidate_id,
                    "status": "BLOCKED_MISSING_NUMERIC_FIELDS",
                    "missing": ";".join(missing),
                    "A_H_bound": "",
                    "h_U_C1_bound": "",
                    "claim_allowed": "False",
                    "valid_for_claim": "False",
                }
            )
            continue

        values = {field: parsed[field] for field in AGGREGATE_REQUIRED if parsed[field] is not None}
        amplitude_inner = (
            values["C_mZ"] * values["M_tr"] * values["Z_1"]
            + values["C_ZZ"] * values["Z_1"] ** 2
            + values["eta_chart"]
            + values["eta_qproj"]
            + values["eta_background"]
        )
        c1_inner = (
            values["C_mZ"] * values["M_tr"] * values["L_U_over_ell_tr"] * values["Z_1"]
            + values["C_mZ"] * values["M_tr"] * values["Z_2"]
            + values["C_mZ1"] * values["M_tr"] * values["Z_1"]
            + values["C_ZZ"] * values["Z_1"] * values["Z_2"]
            + values["C_ZZ1"] * values["Z_1"] ** 2
            + values["eta_C1"]
        )
        A_H_bound = values["C_perp"] * amplitude_inner
        h_U_C1_bound = values["C_perp1"] * c1_inner
        output.append(
            {
                **common(),
                "candidate_id": candidate_id,
                "status": "MIXED_TRANSFER_BOUNDS_COMPUTED_NONCLAIM",
                "A_H_bound": f"{A_H_bound:.12e}",
                "h_U_C1_bound": f"{h_U_C1_bound:.12e}",
                "amplitude_inner": f"{amplitude_inner:.12e}",
                "C1_inner": f"{c1_inner:.12e}",
                "source_path_exists": str(all_source_paths_exist(row.get("source_path", ""))),
                "claim_authority": row.get("claim_authority", ""),
                "claim_allowed": "False",
                "valid_for_claim": str(input_valid),
            }
        )
    return output or [
        {
            **common(),
            "candidate_id": "NO_AGGREGATE_ROWS",
            "status": "BLOCKED_EMPTY_AGGREGATE_FILE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def bridge_rows(aggregate_results: List[Dict[str, str]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    computed = [row for row in aggregate_results if row.get("status") == "MIXED_TRANSFER_BOUNDS_COMPUTED_NONCLAIM"]
    if not computed:
        return [
            {
                **common(),
                "candidate_id": "NO_4252_TO_4249_BRIDGE",
                "bridge_status": "BLOCKED_NO_COMPUTED_MIXED_TRANSFER_RESULT",
                "A_H": "MISSING_4252_A_H_BOUND",
                "h_U_C1": "MISSING_4252_h_U_C1_BOUND",
                "remaining_4249_inputs": "C_qinv;h_U_profile;Omega_E;eta_Lie_frame;C_shape;L_U_over_ell_tr;eta_corner",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        ]
    for row in computed:
        rows.append(
            {
                **common(),
                "candidate_id": row["candidate_id"],
                "bridge_status": "PARTIAL_4249_BRIDGE_READY_NONCLAIM",
                "A_H": row.get("A_H_bound", ""),
                "h_U_C1": row.get("h_U_C1_bound", ""),
                "remaining_4249_inputs": "C_qinv;h_U_profile;Omega_E;eta_Lie_frame;C_shape;L_U_over_ell_tr;eta_corner",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4252_0_progress",
            "C_mZ is now a computable Jacobian contraction, not a verbal missing constant.",
            "Use B_a=omega(Y_m,Y_a) and G_ab=omega(Y_a,Y_b) as the source rows.",
            "Hunt parent Pi4/X_m/X_a rows or theorem zeros.",
        ),
        (
            "DEC4252_1_current_block",
            "No strict current claim is allowed because the parent-owned Jacobian/profile rows are not filled.",
            "This blocks local-GR/PPN/R10/clock/orbital claims while preserving the derivation path.",
            "Do not promote 4250's scalar transition smoke row.",
        ),
        (
            "DEC4252_2_best_next",
            "The best next target is concrete input acquisition: either source Jacobian components or source a direct Hperp profile.",
            "This is now a finite data-entry/proof target rather than another abstract coupling hunt.",
            NEXT_TARGET,
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
        ("FW4252_0_parent_YQ", "parent-owned Y_Q or Pi4(X_Q) missing", "MISSING_PARENT_YQ_OR_PI4", "False"),
        ("FW4252_1_jacobian", "Y_m and Y_a Jacobian rows missing", "MISSING_JACOBIAN_COMPONENT_ROWS", "False"),
        ("FW4252_2_profile", "Z_1/Z_2 and eta rows missing", "MISSING_QSHEAR_PROFILE_ROWS", "False"),
        ("FW4252_3_direct_profile", "direct Hperp profile not sourced", "MISSING_DIRECT_HPERP_PROFILE", "False"),
        ("FW4252_4_claim", "local-GR/PPN/R10/clock/orbital closure not claimed", "NONCLAIM_PRIVATE_GATE", "False"),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "blocked_shortcut": shortcut,
            "reason": reason,
            "claim_allowed": claim_allowed,
            "valid_for_claim": "False",
        }
        for firewall_id, shortcut, reason, claim_allowed in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status": DECISION,
            "summary": "4252 derives the mixed memory-Qshear coefficients as exact symplectic Jacobian contractions and installs an extractor plus templates for source-backed B_a/G_ab, aggregate Hperp bounds, and direct-profile fallback.",
            "scoreable_now": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "objective": "Fill source-backed Y_m/Y_a Jacobian rows from parent Pi4/Q-shear data or acquire the first real direct Hperp profile row on U_good.",
            "avoid": "Do not treat unit-transfer M_tr as Hperp and do not claim local safety from templates.",
            "valid_for_claim": "False",
        }
    ]


def append_claim_row() -> None:
    path = FORMAL / "02-claims-register.csv"
    current = read_text(path)
    if f"{CLAIM_ID}," in current:
        return
    row = [
        CLAIM_ID,
        "local_gr",
        "4252 derives the mixed memory-Qshear transfer constants exactly: B_a=omega(Y_m,Y_a) and G_ab=omega(Y_a,Y_b), with Y_m/Y_a obtained from the Pi4/Q-shear Jacobian when available. It also installs nonclaim extractors/templates for Jacobian rows, aggregate Hperp bounds, and direct Hperp profile fallback.",
        "4252 source register, symplectic Jacobian coefficient theorem, component extraction template, aggregate mixed-transfer runner, direct-profile template, bridge rows, decision and firewall.",
        "private_mixed_memory_qshear_symplectic_extractor_ready_inputs_missing_nonclaim",
        "Source-fill parent Pi4/X_m/X_a Jacobian components or direct Hperp profile rows, then rerun 4252 and feed computed A_H/h_U_C1 into 4249.",
        "Treating the symbolic extractor, template rows, or scalar M_tr smoke scale as a local-GR pass would smuggle Hperp suppression.",
    ]
    with path.open("a", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerow(row)


def write_formal_doc() -> None:
    text = f"""
# 268 - PPC4161 mixed memory-Qshear transfer inputs or direct Hperp profile acquisition

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. 4252 does not prove `Hperp` is small and does not prove local GR, PPN, R10, clock, or orbital safety.

## Main Result

4252 turns the mixed transfer coefficient into a real formula.

Let:

```text
xi^I = (m, Z^a),
Y^A = (C1,D1,C2,D2),
omega_0 = dC1 wedge dD1 + dC2 wedge dD2.
```

Then:

```text
H_Q = Y_Q^* omega_0,
H_IJ = omega_AB partial_I Y^A partial_J Y^B.
```

The mixed and pure Q/shear coefficients are:

```text
B_a = H_ma
    = C1_m D1_a - C1_a D1_m
    + C2_m D2_a - C2_a D2_m,

G_ab = H_ab
     = C1_a D1_b - C1_b D1_a
     + C2_a D2_b - C2_b D2_a.
```

If `Y_Q=Pi4(X_Q)`, this becomes:

```text
Y_m = DPi4_X X_m,
Y_a = DPi4_X X_a,
B_a = omega(DPi4_X X_m, DPi4_X X_a),
G_ab = omega(DPi4_X X_a, DPi4_X X_b).
```

So the missing coupling is no longer a vague `C_HM`; it is a parent Jacobian contraction.

## Bound Interface

With `C_mZ=sum_a |B_a|`, `C_ZZ=sum over a<b |G_ab|`, `|dm|<=M_tr`, and `|dZ|<=Z_1`:

```text
A_H <= C_perp*(C_mZ M_tr Z_1
               + C_ZZ Z_1^2
               + eta_chart + eta_qproj + eta_background).
```

For the C1 branch, with `Z_2` controlling the normalized derivative of `dZ`:

```text
h_U_C1 <= C_perp1*(C_mZ M_tr (L_U/ell_tr) Z_1
                  + C_mZ M_tr Z_2
                  + C_mZ1 M_tr Z_1
                  + C_ZZ Z_1 Z_2
                  + C_ZZ1 Z_1^2
                  + eta_C1).
```

## Direct Profile Alternative

If the Jacobian route cannot be parent-sourced, use the direct profile route:

```text
A_H = ||Hperp||_F/F_ref,
h_U_C1 = max ||nabla Hperp||/(F_ref/L_U)
```

on the selected `U_good` domain. This can feed 4249 without pretending scalar memory alone owns a two-form.

## Extractor Outputs

- `P8_Y5_R2FR_4252_JACOBIAN_COMPONENTS_TEMPLATE.csv` defines the source rows needed for `Y_m` and `Y_a`.
- `P8_Y5_R2FR_4252_JACOBIAN_EXTRACTION_RESULTS.csv` computes `B_a`, `G_ab`, `C_mZ`, and `C_ZZ` if candidate rows exist.
- `P8_Y5_R2FR_4252_MIXED_TRANSFER_RESULTS.csv` computes `A_H` and `h_U_C1` if aggregate rows exist.

## Next Target

`{NEXT_TARGET}` should source-fill parent Jacobian rows or acquire a direct `Hperp` profile.
"""
    write_text(FORMAL_PATH, text)


def write_checkpoint_doc() -> None:
    text = f"""
# 4252 - Mixed memory-Qshear transfer inputs or direct Hperp profile acquisition

**Status:** `{DECISION}`.

## Result

4252 derives the actual mixed transfer coefficients:

```text
B_a = omega(Y_m,Y_a)
    = C1_m D1_a - C1_a D1_m + C2_m D2_a - C2_a D2_m,

G_ab = omega(Y_a,Y_b)
     = C1_a D1_b - C1_b D1_a + C2_a D2_b - C2_b D2_a.
```

For a Q-shear selector `Y_Q=Pi4(X_Q)`, this is:

```text
B_a = omega(DPi4_X X_m, DPi4_X X_a),
G_ab = omega(DPi4_X X_a, DPi4_X X_b).
```

That is the useful move: the coupling is now a sourceable Jacobian contraction, not a black-box coefficient.

## Current Claim Gate

No local-GR/PPN/R10/clock/orbital claim is allowed yet. The extractor is ready, but parent-owned numeric/theorem-zero rows for `Y_m`, `Y_a`, `Z_1`, `Z_2`, and eta terms are still required.

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, text)


def update_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 mixed memory-Qshear transfer inputs

Marker: `{MARKER}`

4252 replaces the vague mixed-transfer constant with exact symplectic Jacobian contractions:

```text
B_a = omega(Y_m,Y_a),
G_ab = omega(Y_a,Y_b).
```

For `Y_Q=Pi4(X_Q)`, this is:

```text
B_a = omega(DPi4_X X_m, DPi4_X X_a),
G_ab = omega(DPi4_X X_a, DPi4_X X_b).
```

The branch remains nonclaim, but the next work is concrete: source the parent Jacobian/profile rows or acquire a direct `Hperp` profile.
"""
    packet_block = f"""
## Packet Update - mixed memory-Qshear transfer inputs

Marker: `{PACKET_MARKER}`

The local packet now has an executable mixed-transfer extractor. `C_mZ` and `C_ZZ` are computed from `B_a=omega(Y_m,Y_a)` and `G_ab=omega(Y_a,Y_b)` when sourced rows exist; until then, the local branch stays private nonclaim.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validation_rows(outputs: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = source_rows()
    theorems = theorem_rows()
    jacobian_results = csv_rows(outputs["jacobian_results"])
    aggregate_results = csv_rows(outputs["mixed_transfer_results"])
    validations = [
        ("VAL4252_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4252_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        ("VAL4252_2_Ba_formula", any(row["theorem_id"] == "MMQ4252_1_mixed_Ba" for row in theorems), "B_a theorem emitted"),
        ("VAL4252_3_Gab_formula", any(row["theorem_id"] == "MMQ4252_2_pure_Gab" for row in theorems), "G_ab theorem emitted"),
        ("VAL4252_4_Pi4_chain", any(row["theorem_id"] == "MMQ4252_3_Pi4_chain_rule" for row in theorems), "Pi4 chain-rule theorem emitted"),
        ("VAL4252_5_jacobian_nonclaim", all(row.get("claim_allowed", "False") == "False" for row in jacobian_results), "Jacobian extractor does not claim closure"),
        ("VAL4252_6_aggregate_nonclaim", all(row.get("claim_allowed", "False") == "False" for row in aggregate_results), "Aggregate runner does not claim closure"),
        ("VAL4252_7_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal doc written"),
        ("VAL4252_8_checkpoint_doc", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), "checkpoint doc written"),
        ("VAL4252_9_claim_row", f"{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4252_10_spine_marker", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine marker present"),
        ("VAL4252_11_packet_marker", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet marker present"),
    ]
    for name, path in outputs.items():
        validations.append((f"VAL4252_csv_{name}", bool(csv_rows(path)), f"{path.name} parses"))
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(passed),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in validations
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        "source_register": SOURCE_DIR / "P8_Y5_R2FR_4252_SOURCE_REGISTER.csv",
        "transfer_theorems": SOURCE_DIR / "P8_Y5_R2FR_4252_MIXED_TRANSFER_THEOREMS.csv",
        "coefficient_contract": SOURCE_DIR / "P8_Y5_R2FR_4252_COEFFICIENT_CONTRACT.csv",
        "jacobian_template": SOURCE_DIR / "P8_Y5_R2FR_4252_JACOBIAN_COMPONENTS_TEMPLATE.csv",
        "jacobian_results": SOURCE_DIR / "P8_Y5_R2FR_4252_JACOBIAN_EXTRACTION_RESULTS.csv",
        "aggregate_template": SOURCE_DIR / "P8_Y5_R2FR_4252_MIXED_TRANSFER_INPUTS_TEMPLATE.csv",
        "mixed_transfer_results": SOURCE_DIR / "P8_Y5_R2FR_4252_MIXED_TRANSFER_RESULTS.csv",
        "direct_profile_template": SOURCE_DIR / "P8_Y5_R2FR_4252_DIRECT_HPERP_PROFILE_TEMPLATE.csv",
        "bridge_rows": SOURCE_DIR / "P8_Y5_R2FR_4252_TO_4249_BRIDGE_ROWS.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4252_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4252_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4252_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4252_NEXT_TARGET.csv",
    }

    write_formal_doc()
    write_checkpoint_doc()
    append_claim_row()
    update_spine_and_packet()

    jacobian_results = jacobian_extraction_rows()
    aggregate_results = aggregate_transfer_results()

    write_csv(outputs["source_register"], source_rows())
    write_csv(outputs["transfer_theorems"], theorem_rows())
    write_csv(outputs["coefficient_contract"], coefficient_contract_rows())
    write_csv(outputs["jacobian_template"], jacobian_template_rows())
    write_csv(outputs["jacobian_results"], jacobian_results)
    write_csv(outputs["aggregate_template"], aggregate_template_rows())
    write_csv(outputs["mixed_transfer_results"], aggregate_results)
    write_csv(outputs["direct_profile_template"], direct_profile_template_rows())
    write_csv(outputs["bridge_rows"], bridge_rows(aggregate_results))
    write_csv(outputs["decision"], decision_rows())
    write_csv(outputs["firewall"], firewall_rows())
    write_csv(outputs["status"], status_rows())
    write_csv(outputs["next_target"], next_target_rows())
    write_csv(VALIDATION_PATH, validation_rows(outputs))

    validation = csv_rows(VALIDATION_PATH)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(outputs)} csv artifacts")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")


if __name__ == "__main__":
    main()
