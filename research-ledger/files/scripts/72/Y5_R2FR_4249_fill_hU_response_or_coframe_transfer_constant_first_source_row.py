from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4249"
CLAIM_ID = "L-090"
BRANCH = "MTS_R2FR_Y5_HU_RESPONSE_BOUND_OR_COFRAME_TRANSFER_FIRST_ROW_4249"
DECISION = "HU_RESPONSE_BOUND_BUILT_SELECTOR_C1_TRANSITION_ROUTES_NUMERIC_INPUTS_MISSING_NONCLAIM"
MARKER = "PPC4161_HU_RESPONSE_BOUND_COFRAME_TRANSFER_ROW_4249"
PACKET_MARKER = "PPC4161_PACKET_HU_RESPONSE_BOUND_COFRAME_TRANSFER_ROW_4249"
NEXT_TARGET = "4250-Y5-R2FR-source-hU-C1-or-selector-leakage-candidate-inputs.md"

FORMAL_PATH = FORMAL / "265-PPC4161-hU-response-bound-or-coframe-transfer-first-source-row.md"
DOC_PATH = POST / "4249-Y5-R2FR-fill-hU-response-or-coframe-transfer-constant-first-source-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4249_VALIDATION.csv"
CANDIDATE_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4249_HU_RESPONSE_INPUTS_CANDIDATE.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4249_00_4248_formal": SourceSpec(
        "SRC4249_00_4248_formal",
        FORMAL / "264-PPC4161-epsilon-geom-profile-sampler-or-coframe-shadow-bound-first-row.md",
        "h_U_response",
        "4248 makes h_U_response the first coframe-shadow input.",
    ),
    "SRC4249_01_4248_validation": SourceSpec(
        "SRC4249_01_4248_validation",
        SOURCE_DIR / "P8_Y5_BRR545_4248_VALIDATION.csv",
        "VAL4248_3_hU_bridge",
        "4248 validation proves the h_U bridge was emitted.",
    ),
    "SRC4249_02_3799_theorem": SourceSpec(
        "SRC4249_02_3799_theorem",
        SOURCE_DIR / "P8_Y5_R2FR_3799_HPERP_CURVATURE_DESCENT_THEOREM.csv",
        "h_U_response",
        "3799 defines h_U_response as the shared Hperp numerator.",
    ),
    "SRC4249_03_3799_doc": SourceSpec(
        "SRC4249_03_3799_doc",
        POST / "3799-Y5-R2FR-Hperp-curvature-descent-zero-or-first-hU-source-row.md",
        "h_U_response=max_A",
        "3799 gives the local definition and source-row gap.",
    ),
    "SRC4249_04_3800_selector_bound": SourceSpec(
        "SRC4249_04_3800_selector_bound",
        SOURCE_DIR / "P8_Y5_R2FR_3800_HU_SELECTOR_LEAKAGE_BOUND_ROWS.csv",
        "h_U_response <= C_HY*epsilon_YV + eta_chart_transition + eta_degen",
        "3800 replaces opaque h_U by selector-leakage inputs.",
    ),
    "SRC4249_05_3800_theorem": SourceSpec(
        "SRC4249_05_3800_theorem",
        SOURCE_DIR / "P8_Y5_R2FR_3800_FULL_RANK_CLEBSCH_BASICNESS_THEOREM.csv",
        "CBT3800_1_full_rank_no_cancellation",
        "3800 proves generic full-rank no-cancellation.",
    ),
    "SRC4249_06_3801_refinement": SourceSpec(
        "SRC4249_06_3801_refinement",
        POST / "3801-Y5-R2FR-qobs-Qshear-spectral-ownership-or-selector-leakage-fill.md",
        "ker(Dq_X)=ker(Dq_obs) cap ker(DX_Q)",
        "3801 gives the exact q_X refinement route.",
    ),
    "SRC4249_07_3801_fill": SourceSpec(
        "SRC4249_07_3801_fill",
        SOURCE_DIR / "P8_Y5_R2FR_3801_SELECTOR_LEAKAGE_FILL_ROWS.csv",
        "SLF3801_9_hU_bound",
        "3801 stages selector-leakage fill rows.",
    ),
    "SRC4249_08_3796_chart": SourceSpec(
        "SRC4249_08_3796_chart",
        POST / "3796-Y5-R2FR-Qshear-eigenframe-chart-or-first-Bperp-arena-fill.md",
        "rank(dY_Q)=4",
        "3796 supplies the conditional Q-shear chart/rank context.",
    ),
    "SRC4249_09_4248_sampler_live": SourceSpec(
        "SRC4249_09_4248_sampler_live",
        POST / "scripts" / "Y5_R2FR_4248_epsilon_geom_profile_sampler_or_coframe_shadow_bound_first_row.py",
        "CANDIDATE_INPUT_PATH",
        "4248 live sampler path.",
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


def append_claim_row() -> None:
    path = FORMAL / "02-claims-register.csv"
    current = read_text(path)
    if f"{CLAIM_ID}," in current:
        return
    row = [
        CLAIM_ID,
        "local_gr",
        "4249 derives a sourceable h_U_response envelope: the inherited selector-leakage route is welded to a local Lie/C1 bound and a transition-width amplitude law, then fed back into the 4248 coframe-shadow sampler contract.",
        "4249 source register, response-bound theorems, input schema, template row, dry-run result, decision and firewall.",
        "private_hU_response_bound_routes_ready_numeric_inputs_missing_nonclaim",
        "Source-fill h_U_C1 or selector leakage inputs, or parent-sign q_X/Q-shear ownership, then rerun 4249 and feed a source-backed h_U_response into 4248.",
        "Treating the C1/transition bound as evidence without real profile derivatives, q_* inverse norm, chart/degen terms, and source paths would smuggle the local-GR pass.",
    ]
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(row)


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


def text_bool(value: Optional[str]) -> bool:
    return str(value or "").strip().lower() in {"true", "yes", "1", "parent_signed_true"}


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for spec in SOURCE_SPECS.values():
        text = read_text(spec.path)
        exists = spec.path.exists()
        rows.append(
            {
                **common(),
                "source_id": spec.source_id,
                "path": str(spec.path),
                "exists": str(exists),
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
            "HRB4249_0_definition",
            "h_U_response target",
            "h_U_response := max_A ||q_*^-1 Lie_{E_A} Hperp||_F / F_ref.",
            "DEFINITION_FROM_3799",
            "This is the local Hperp response numerator feeding 4248.",
            "MISSING_PARENT_HPERP_ZERO_OR_RESPONSE_BOUND",
        ),
        (
            "HRB4249_1_qX_zero_route",
            "q_X quotient zero route",
            "If q_X=(q_obs,X_Q) is parent-selected before EM readout, Pi4 is parent-owned, and same-source/no-extra-force gates survive, then ker(Dq_X) subset ker(DX_Q), dY_Q[V_X]=0, and h_U_response=0 on the refined quotient branch.",
            "EXACT_CONDITIONAL_ZERO_ROUTE",
            "This is a real derivation route, not a numeric fit.",
            "MISSING_QX_PARENT_SIGNATURE_PI4_AND_SAME_SOURCE_RECHECK",
        ),
        (
            "HRB4249_2_selector_leakage_bound",
            "selector leakage finite route",
            "h_U_response <= C_HY*epsilon_YV + eta_chart_transition + eta_degen.",
            "DERIVED_BOUND_FROM_3800_3801",
            "The opaque response is replaced by Q-shear/Pi4 leakage inputs.",
            "MISSING_EPSILON_YV_C_HY_CHART_DEGEN_VALUES",
        ),
        (
            "HRB4249_3_Lie_C1_bound",
            "local Lie/C1 response bound",
            "For a torsion-free local connection and normalized frame generators, ||Lie_E Hperp||_F/F_ref <= h_U_C1 + 2*Omega_E*h_U_profile + eta_Lie_frame; hence h_U_response <= C_qinv*(h_U_C1 + 2*Omega_E*h_U_profile + eta_Lie_frame).",
            "EXACT_TENSOR_CALCULUS_BOUND",
            "This turns h_U_response into derivative/amplitude/frame-norm data.",
            "MISSING_CQINV_HU_C1_HU_PROFILE_OMEGAE_VALUES",
        ),
        (
            "HRB4249_4_transition_width_law",
            "transition-width amplitude law",
            "If Hperp has dimensionless amplitude A_H and varies across thickness ell_tr with scale L_U, then h_U_C1 <= C_shape*A_H*(L_U/ell_tr)+eta_corner, so h_U_response <= C_qinv*(C_shape*A_H*(L_U/ell_tr)+2*Omega_E*A_H+eta_corner+eta_Lie_frame).",
            "DERIVED_PROFILE_REDUCTION",
            "The next numeric source can be a profile amplitude and transition width, not a full tensor field.",
            "MISSING_AH_ELLTR_SHAPE_FRAME_VALUES",
        ),
        (
            "HRB4249_5_4248_bridge",
            "coframe-shadow bridge",
            "epsilon_coframe <= C_coframe_hU*h_U_response_bound + C_coframe_projector*epsilon_Q_projector + C_coframe_eigenchart*epsilon_eigenchart + C_coframe_degeneracy*epsilon_eigen_degeneracy + C_coframe_selector*epsilon_Pi4_selector.",
            "EXECUTABLE_BRIDGE_TO_4248",
            "4249 can feed a source-backed h_U_response_bound into the 4248 sampler.",
            "MISSING_CCOFRAME_OR_RESPONSE_BOUND_CANDIDATE_ROW",
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


def schema_rows() -> List[Dict[str, str]]:
    raw = [
        ("parent_zero_authority", "zero_route", "certificate", "PARENT_SIGNED_QX_HPERP_ZERO or false", "Only accepted with q_X/Pi4/same-source/no-extra-force certificates."),
        ("C_HY", "selector_route", "dimensionless", "operator norm from epsilon_YV to h_U_response", "nonnegative numeric with source path"),
        ("epsilon_YV", "selector_route", "dimensionless", "max_A||D Pi4_X.DX_Q(E_A)||/Y_ref", "nonnegative numeric with source path"),
        ("eta_chart_transition", "selector_route", "dimensionless", "Q-shear chart transition leakage", "nonnegative numeric with source path"),
        ("eta_degen", "selector_route", "dimensionless", "degenerate-eigenframe support leakage", "nonnegative numeric with source path"),
        ("C_qinv", "C1_route;transition_route", "dimensionless", "operator norm of q_*^-1 on the selected response bundle", "nonnegative numeric with source path"),
        ("h_U_C1", "C1_route", "dimensionless", "max normalized first derivative ||nabla Hperp||/(F_ref/L_U)", "nonnegative numeric with source path"),
        ("h_U_profile", "C1_route", "dimensionless", "||Hperp||_F/F_ref amplitude on U_good", "nonnegative numeric with source path"),
        ("Omega_E", "C1_route;transition_route", "dimensionless", "L_U max_A||nabla E_A|| frame/anholonomy norm", "nonnegative numeric with source path"),
        ("eta_Lie_frame", "C1_route;transition_route", "dimensionless", "torsion/frame/regularity remainder for Lie derivative formula", "nonnegative numeric with source path"),
        ("C_shape", "transition_route", "dimensionless", "profile shape constant relating amplitude to derivative", "nonnegative numeric with source path"),
        ("A_H", "transition_route", "dimensionless", "sup ||Hperp||_F/F_ref transition amplitude", "nonnegative numeric with source path"),
        ("L_U_over_ell_tr", "transition_route", "dimensionless", "local domain scale over transition thickness", "nonnegative numeric with source path"),
        ("eta_corner", "transition_route", "dimensionless", "nonsmooth/corner support leakage", "nonnegative numeric with source path"),
        ("C_coframe_hU", "coframe_bridge", "dimensionless", "4248 transfer constant from h_U_response to epsilon_coframe", "nonnegative numeric with source path"),
        ("source_path", "all", "path", "local source evidence path for candidate row", "must exist before valid_for_claim can ever become true"),
        ("valid_for_claim", "all", "boolean", "candidate authorizes claim use", "current generated template sets false"),
    ]
    return [
        {
            **common(),
            "symbol": symbol,
            "route": route,
            "units": units,
            "definition": definition,
            "valid_value_rule": rule,
            "valid_for_claim": "False",
        }
        for symbol, route, units, definition, rule in raw
    ]


def template_rows() -> List[Dict[str, str]]:
    row = {
        **common(),
        "candidate_id": "HU4249_TEMPLATE_0",
        "route_preference": "selector_or_C1_or_transition",
        "parent_zero_authority": "MISSING_PARENT_ZERO_AUTHORITY",
        "C_HY": "MISSING",
        "epsilon_YV": "MISSING",
        "eta_chart_transition": "MISSING",
        "eta_degen": "MISSING",
        "C_qinv": "MISSING",
        "h_U_C1": "MISSING",
        "h_U_profile": "MISSING",
        "Omega_E": "MISSING",
        "eta_Lie_frame": "MISSING",
        "C_shape": "MISSING",
        "A_H": "MISSING",
        "L_U_over_ell_tr": "MISSING",
        "eta_corner": "MISSING",
        "C_coframe_hU": "MISSING",
        "source_path": "MISSING_SOURCE_PATH",
        "valid_for_claim": "False",
        "notes": "Copy to P8_Y5_R2FR_4249_HU_RESPONSE_INPUTS_CANDIDATE.csv only after sourcing real values.",
    }
    return [row]


def candidate_result_rows() -> List[Dict[str, str]]:
    if not CANDIDATE_INPUT_PATH.exists():
        return [
            {
                **common(),
                "candidate_id": "NO_CANDIDATE",
                "status": "NO_CANDIDATE_INPUT_FILE",
                "selector_bound": "MISSING",
                "C1_bound": "MISSING",
                "transition_bound": "MISSING",
                "h_U_response_bound": "MISSING",
                "bridge_hU_for_4248": "MISSING",
                "issues": "P8_Y5_R2FR_4249_HU_RESPONSE_INPUTS_CANDIDATE.csv not present",
                "scoreable_now": "False",
                "valid_for_claim": "False",
            }
        ]

    rows: List[Dict[str, str]] = []
    for index, candidate in enumerate(csv_rows(CANDIDATE_INPUT_PATH)):
        candidate_id = candidate.get("candidate_id") or f"CANDIDATE_{index}"
        source_path = Path(candidate.get("source_path", ""))
        source_exists = source_path.exists() if str(source_path) not in {"", "."} else False
        issues: List[str] = []
        bounds: List[float] = []

        zero_authority = str(candidate.get("parent_zero_authority", "")).strip()
        zero_ready = zero_authority == "PARENT_SIGNED_QX_HPERP_ZERO"
        if zero_ready:
            bounds.append(0.0)

        C_HY = parse_optional_float(candidate.get("C_HY"))
        epsilon_YV = parse_optional_float(candidate.get("epsilon_YV"))
        eta_chart = parse_optional_float(candidate.get("eta_chart_transition"))
        eta_degen = parse_optional_float(candidate.get("eta_degen"))
        selector_bound: Optional[float] = None
        if None not in (C_HY, epsilon_YV, eta_chart, eta_degen):
            selector_bound = C_HY * epsilon_YV + eta_chart + eta_degen  # type: ignore[operator]
            bounds.append(selector_bound)
        else:
            issues.append("MISSING_SELECTOR_ROUTE_INPUTS")

        C_qinv = parse_optional_float(candidate.get("C_qinv"))
        h_U_C1 = parse_optional_float(candidate.get("h_U_C1"))
        h_U_profile = parse_optional_float(candidate.get("h_U_profile"))
        Omega_E = parse_optional_float(candidate.get("Omega_E"))
        eta_Lie_frame = parse_optional_float(candidate.get("eta_Lie_frame"))
        C1_bound: Optional[float] = None
        if None not in (C_qinv, h_U_C1, h_U_profile, Omega_E, eta_Lie_frame):
            C1_bound = C_qinv * (h_U_C1 + 2.0 * Omega_E * h_U_profile + eta_Lie_frame)  # type: ignore[operator]
            bounds.append(C1_bound)
        else:
            issues.append("MISSING_C1_ROUTE_INPUTS")

        C_shape = parse_optional_float(candidate.get("C_shape"))
        A_H = parse_optional_float(candidate.get("A_H"))
        L_U_over_ell_tr = parse_optional_float(candidate.get("L_U_over_ell_tr"))
        eta_corner = parse_optional_float(candidate.get("eta_corner"))
        transition_bound: Optional[float] = None
        if None not in (C_qinv, C_shape, A_H, L_U_over_ell_tr, Omega_E, eta_corner, eta_Lie_frame):
            transition_bound = C_qinv * (
                C_shape * A_H * L_U_over_ell_tr + 2.0 * Omega_E * A_H + eta_corner + eta_Lie_frame
            )  # type: ignore[operator]
            bounds.append(transition_bound)
        else:
            issues.append("MISSING_TRANSITION_ROUTE_INPUTS")

        C_coframe_hU = parse_optional_float(candidate.get("C_coframe_hU"))
        best_bound = min(bounds) if bounds else None
        bridge = C_coframe_hU * best_bound if best_bound is not None and C_coframe_hU is not None else None
        if C_coframe_hU is None:
            issues.append("MISSING_C_COFRAME_HU")
        if not source_exists:
            issues.append("MISSING_OR_BAD_SOURCE_PATH")

        scoreable = best_bound is not None and source_exists
        claim_auth = str(candidate.get("claim_authority", "")).strip() == "PARENT_SIGNED_TRUE"
        valid_for_claim = scoreable and text_bool(candidate.get("valid_for_claim")) and claim_auth
        if not valid_for_claim:
            issues.append("VALID_FOR_CLAIM_FALSE_OR_AUTHORITY_MISSING")

        rows.append(
            {
                **common(),
                "candidate_id": candidate_id,
                "status": "BOUND_COMPUTED_NONCLAIM" if best_bound is not None else "BOUND_NOT_COMPUTED",
                "selector_bound": "MISSING" if selector_bound is None else f"{selector_bound:.12g}",
                "C1_bound": "MISSING" if C1_bound is None else f"{C1_bound:.12g}",
                "transition_bound": "MISSING" if transition_bound is None else f"{transition_bound:.12g}",
                "h_U_response_bound": "MISSING" if best_bound is None else f"{best_bound:.12g}",
                "bridge_hU_for_4248": "MISSING" if bridge is None else f"{bridge:.12g}",
                "issues": ";".join(issues) if issues else "NONE",
                "scoreable_now": str(scoreable),
                "valid_for_claim": str(valid_for_claim),
            }
        )
    return rows


def bridge_template_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "target_file": str(SOURCE_DIR / "P8_Y5_R2FR_4248_EPSILON_GEOM_PROFILE_INPUTS_CANDIDATE.csv"),
            "row_id": "BRIDGE4249_TO_4248",
            "instruction": "When 4249 produces a source-backed h_U_response_bound, copy that value into 4248 h_U_response and retain all other 4248 coframe/projector/eigenchart fields.",
            "required_4249_fields": "h_U_response_bound;C_coframe_hU;source_path;valid_for_claim",
            "current_status": "WAITING_FOR_4249_SOURCE_BACKED_CANDIDATE",
            "valid_for_claim": "False",
        }
    ]


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4249_0_progress",
            "h_U_response is no longer opaque",
            "4249 welds the 3800/3801 selector-leakage bound to a new local Lie/C1 and transition-width bound.",
            "Use sourceable derivative/amplitude/transition-width inputs before rerunning 4248.",
        ),
        (
            "DEC4249_1_current_nonclaim",
            "no current local-GR or arena pass",
            "No source-backed candidate row exists and no parent q_X/Hperp zero certificate is signed.",
            "Keep valid_for_claim=false and do not score PPN/R10/clock/orbital arenas.",
        ),
        (
            "DEC4249_2_next",
            "source h_U_C1 or selector leakage first",
            "The best next move is either parent-sign q_X/Q-shear ownership or fill h_U_C1/A_H/ell_tr/C_qinv from a real local profile.",
            NEXT_TARGET,
        ),
    ]
    return [
        {
            **common(),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "action": action,
            "valid_for_claim": "False",
        }
        for decision_id, decision, rationale, action in raw
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4249_0_no_bound_no_claim", "h_U_response_bound missing", "No local-GR/PPN/R10/clock/orbital claim."),
        ("FW4249_1_no_profile_smuggling", "C1/transition rows unsourced", "Do not infer small response from smooth-looking prose."),
        ("FW4249_2_no_qX_shortcut", "q_X not parent-signed", "Do not refine the quotient after EM readout to force Hperp zero."),
        ("FW4249_3_no_4248_promotion", "4248 sampler waiting for source-backed h_U", "Do not treat a dry-run sampler as evidence."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "blocked_shortcut": shortcut,
            "rule": rule,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, shortcut, rule in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status": DECISION,
            "summary": "4249 derives sourceable selector, C1, and transition-width routes for h_U_response. Current run is nonclaim because no source-backed candidate profile exists.",
            "scoreable_now": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "objective": "Either source-fill h_U_C1/A_H/ell_tr/C_qinv from a real local Hperp profile or parent-sign q_X/Q-shear ownership and same-source recheck.",
            "avoid": "Do not produce local-GR, PPN, R10, clock, or orbital claims from placeholder response bounds.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc() -> None:
    text = f"""
# 265 - PPC4161 h_U response bound or coframe-transfer first source row

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. 4249 does not prove local GR, PPN safety, R10 safety, clock safety, orbital safety, or an EM/source-coupling pass. It does make the next missing numerator sharper: `h_U_response` is now bounded by sourceable selector, C1, and transition-width data.

## What 4248 Needed

4248 left the first coframe-shadow row as:

```text
epsilon_coframe
<= C_coframe_hU*h_U_response
 + C_coframe_projector*epsilon_Q_projector
 + C_coframe_eigenchart*epsilon_eigenchart
 + C_coframe_degeneracy*epsilon_eigen_degeneracy
 + C_coframe_selector*epsilon_Pi4_selector.
```

So the hard numerator is:

```text
h_U_response := max_A ||q_*^-1 Lie_{{E_A}} Hperp||_F/F_ref.
```

## Selector-Leakage Route

The inherited 3800/3801 route gives:

```text
h_U_response <= C_HY*epsilon_YV + eta_chart_transition + eta_degen.
```

where:

```text
epsilon_YV=max_A||D Pi4_X.DX_Q(E_A)||/Y_ref.
```

If instead the parent signs `q_X=(q_obs,X_Q)`, parent-owned `Pi4`, and the same-source/no-extra-force recheck, then `DX_Q[V_X]=0`, hence `dY_Q[V_X]=0`, and this branch can set `h_U_response=0` on the refined quotient. That zero is not claimed here.

## Local Lie/C1 Bound

For a torsion-free local connection and normalized frame generators:

```text
(Lie_E Hperp)_{{ab}}
= E^c nabla_c Hperp_{{ab}}
+ Hperp_{{cb}} nabla_a E^c
+ Hperp_{{ac}} nabla_b E^c.
```

Therefore:

```text
||Lie_E Hperp||_F/F_ref
<= h_U_C1 + 2 Omega_E h_U_profile + eta_Lie_frame.
```

After the quotient inverse:

```text
h_U_response
<= C_qinv*(h_U_C1 + 2 Omega_E h_U_profile + eta_Lie_frame).
```

This is the important reduction: response is not magic. It is a first-derivative profile plus a frame/anholonomy correction.

## Transition-Width Amplitude Law

If `Hperp` has dimensionless amplitude `A_H` and changes across a transition layer of thickness `ell_tr` inside local scale `L_U`, then:

```text
h_U_C1 <= C_shape*A_H*(L_U/ell_tr)+eta_corner.
```

So:

```text
h_U_response
<= C_qinv*(C_shape*A_H*(L_U/ell_tr)
          +2 Omega_E A_H
          +eta_corner
          +eta_Lie_frame).
```

This gives a concrete future data route: sample or bound `A_H`, `ell_tr`, `C_shape`, `C_qinv`, `Omega_E`, and the regularity remainders.

## Executable Candidate Contract

4249 reads optional candidate rows from:

```text
P8_Y5_R2FR_4249_HU_RESPONSE_INPUTS_CANDIDATE.csv
```

and writes:

```text
P8_Y5_R2FR_4249_HU_RESPONSE_BOUND_RESULTS.csv.
```

If no candidate row exists, or if the row lacks real nonnegative numeric inputs and an existing source path, the result remains `MISSING` and `valid_for_claim=false`.

## Next Target

`{NEXT_TARGET}` should either source-fill a real local `Hperp` C1/transition profile or parent-sign the `q_X`/Q-shear ownership route.
"""
    write_text(FORMAL_PATH, text)


def write_checkpoint_doc() -> None:
    text = f"""
# 4249 - fill h_U_response or coframe-transfer constant first source row

**Status:** `{DECISION}`.

## Result

4249 makes the next missing local-geometry numerator concrete:

```text
h_U_response <= C_HY*epsilon_YV + eta_chart_transition + eta_degen
```

or, independently,

```text
h_U_response <= C_qinv*(h_U_C1 + 2 Omega_E h_U_profile + eta_Lie_frame)
```

with the transition-width reduction:

```text
h_U_C1 <= C_shape*A_H*(L_U/ell_tr)+eta_corner.
```

## Current state

No source-backed candidate row exists yet, so the generated result remains `MISSING` and `valid_for_claim=false`.

## Next target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, text)


def update_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 h_U response bound / coframe-transfer row

Marker: `{MARKER}`

4249 removes the black-box status of `h_U_response`. The response can now be attacked through either selector leakage,

```text
h_U_response <= C_HY*epsilon_YV + eta_chart_transition + eta_degen,
```

or a local C1/transition-width profile,

```text
h_U_response <= C_qinv*(h_U_C1 + 2 Omega_E h_U_profile + eta_Lie_frame),
h_U_C1 <= C_shape*A_H*(L_U/ell_tr)+eta_corner.
```

The branch remains nonclaim until those inputs are parent-signed or source-backed.
"""
    packet_block = f"""
## Packet Update - h_U response bound / coframe transfer

Marker: `{PACKET_MARKER}`

The local packet now has a sourceable numerator contract for the 4248 coframe-shadow sampler. The next pressure point is no longer a vague Hperp response but `h_U_C1`, `A_H`, `ell_tr`, `C_qinv`, or the selector-leakage tuple `epsilon_YV/C_HY/eta_chart/eta_degen`.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validation_rows(output_paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = source_rows()
    theorems = theorem_rows()
    schema = schema_rows()
    results = candidate_result_rows()
    validations = [
        ("VAL4249_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4249_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        ("VAL4249_2_selector_bound_present", any("C_HY*epsilon_YV" in row["mathematical_form"] for row in theorems), "selector bound present"),
        ("VAL4249_3_C1_bound_present", any("h_U_C1" in row["mathematical_form"] for row in theorems), "C1 Lie bound present"),
        ("VAL4249_4_transition_law_present", any("L_U/ell_tr" in row["mathematical_form"] for row in theorems), "transition width law present"),
        ("VAL4249_5_schema_has_profile_inputs", all(any(row["symbol"] == symbol for row in schema) for symbol in ["h_U_C1", "A_H", "L_U_over_ell_tr", "C_qinv"]), "schema includes profile inputs"),
        ("VAL4249_6_results_nonclaim", all(row["valid_for_claim"] == "False" for row in results), "current results remain nonclaim"),
        ("VAL4249_7_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal doc written"),
        ("VAL4249_8_checkpoint_doc", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), "checkpoint doc written"),
        ("VAL4249_9_claim_row", f"{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4249_10_spine_marker", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine marker present"),
        ("VAL4249_11_packet_marker", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet marker present"),
    ]
    for name, path in output_paths.items():
        parsed = bool(csv_rows(path))
        validations.append((f"VAL4249_csv_{name}", parsed, f"{path.name} parses"))
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
        "source_register": SOURCE_DIR / "P8_Y5_R2FR_4249_SOURCE_REGISTER.csv",
        "response_theorems": SOURCE_DIR / "P8_Y5_R2FR_4249_HU_RESPONSE_BOUND_THEOREMS.csv",
        "input_schema": SOURCE_DIR / "P8_Y5_R2FR_4249_HU_RESPONSE_INPUT_SCHEMA.csv",
        "input_template": SOURCE_DIR / "P8_Y5_R2FR_4249_HU_RESPONSE_INPUTS_TEMPLATE.csv",
        "results": SOURCE_DIR / "P8_Y5_R2FR_4249_HU_RESPONSE_BOUND_RESULTS.csv",
        "bridge_template": SOURCE_DIR / "P8_Y5_R2FR_4249_TO_4248_BRIDGE_TEMPLATE.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4249_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4249_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4249_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4249_NEXT_TARGET.csv",
    }

    write_formal_doc()
    write_checkpoint_doc()
    append_claim_row()
    update_spine_and_packet()

    write_csv(outputs["source_register"], source_rows())
    write_csv(outputs["response_theorems"], theorem_rows())
    write_csv(outputs["input_schema"], schema_rows())
    write_csv(outputs["input_template"], template_rows())
    write_csv(outputs["results"], candidate_result_rows())
    write_csv(outputs["bridge_template"], bridge_template_rows())
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
