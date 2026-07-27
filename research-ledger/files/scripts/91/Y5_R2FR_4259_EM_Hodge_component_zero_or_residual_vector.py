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

CHECKPOINT = "4259"
CLAIM_ID = "L-100"
BRANCH = "MTS_R2FR_Y5_EM_HODGE_COMPONENT_ZERO_OR_RESIDUAL_VECTOR_4259"
DECISION = "DQ_EM_ZERO_REDUCED_TO_VISIBLE_EM_RESIDUAL_VECTOR_POYNTING_DOUBLE_COUNT_FORBIDDEN_NONCLAIM"
MARKER = "PPC4161_EM_HODGE_COMPONENT_ZERO_OR_RESIDUAL_VECTOR_4259"
PACKET_MARKER = "PPC4161_PACKET_EM_HODGE_COMPONENT_ZERO_OR_RESIDUAL_VECTOR_4259"
NEXT_TARGET = "4260-Y5-R2FR-close-Delta-Hodge-EM-or-fill-visible-EM-residual-bound.md"

FORMAL_PATH = FORMAL / "275-PPC4161-EM-Hodge-component-zero-or-residual-vector.md"
DOC_PATH = POST / "4259-Y5-R2FR-EM-Hodge-component-zero-or-residual-vector.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4259_VALIDATION.csv"
ADOPTION_4263_PATH = SOURCE_DIR / "P8_Y5_R2FR_4263_DQ_EM_ADOPTION.csv"
FORMAL_4263_PATH = FORMAL / "279-PPC4161-Dq-EM-closed-collar-adoption-or-radiative-boundary-row.md"
ADOPTION_4264_PATH = SOURCE_DIR / "P8_Y5_R2FR_4264_DQ_THETA_MARKER_ADOPTION.csv"
FORMAL_4264_PATH = FORMAL / "280-PPC4161-Dq-theta-marker-component-zero-or-marker-bound.md"
ADOPTION_4265_PATH = SOURCE_DIR / "P8_Y5_R2FR_4265_DQ_MATTER_ADOPTION.csv"
FORMAL_4265_PATH = FORMAL / "281-PPC4161-Dq-matter-action-domain-zero-or-source-prefactor-bound.md"
ADOPTION_4266_PATH = SOURCE_DIR / "P8_Y5_R2FR_4266_DQ_SOURCE_READOUT_ADOPTION.csv"
FORMAL_4266_PATH = FORMAL / "282-PPC4161-Dq-source-readout-Hilbert-charge-zero-or-coefficient-remainder.md"
ADOPTION_4267_PATH = SOURCE_DIR / "P8_Y5_R2FR_4267_DQ_COEFF_ADOPTION.csv"
FORMAL_4267_PATH = FORMAL / "283-PPC4161-Dq-coeff-fixed-parent-constant-or-Newton-calibration-bound.md"
ADOPTION_4268_PATH = SOURCE_DIR / "P8_Y5_R2FR_4268_DQ_BOUNDARY_PROJECTOR_ADOPTION.csv"
FORMAL_4268_PATH = FORMAL / "284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md"
ADOPTION_4269_PATH = SOURCE_DIR / "P8_Y5_R2FR_4269_DQ_TAU_ADOPTION.csv"
FORMAL_4269_PATH = FORMAL / "285-PPC4161-Dq-tau-reference-time-lock-or-tau-residual-bound.md"
REDUCED_GEOM_4270_PATH = SOURCE_DIR / "P8_Y5_R2FR_4270_DQ_GEOM_REDUCED_CANDIDATE.csv"
FORMAL_4270_PATH = FORMAL / "286-PPC4161-Dq-geom-core-coframe-shadow-or-reduced-epsilon-bound.md"
CORE_GEOM_4271_PATH = SOURCE_DIR / "P8_Y5_R2FR_4271_DQ_GEOM_CORE_FRAME_CANDIDATE.csv"
FORMAL_4271_PATH = FORMAL / "287-PPC4161-core-coframe-shadow-zero-or-first-source-backed-epsilon-row.md"
BOUND_GEOM_4272_PATH = SOURCE_DIR / "P8_Y5_R2FR_4272_DQ_GEOM_BOUND_RUNNER_CANDIDATE.csv"
FORMAL_4272_PATH = FORMAL / "288-PPC4161-parent-no-extra-frame-signature-or-cg-bdis-first-bound-runner.md"

LOCAL_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4259_DQ_COMPONENT_VALUES_CANDIDATE.csv"
COMPONENT_CANDIDATE_4254_PATH = SOURCE_DIR / "P8_Y5_R2FR_4254_DQ_COMPONENT_VALUES_CANDIDATE.csv"
PREVIOUS_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4258_DQ_COMPONENT_VALUES_CANDIDATE.csv"

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
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4259_00_191_owner": SourceSpec(
        "SRC4259_00_191_owner",
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "Poynting vector is not a separate background field",
        "Maxwell-Hodge Hilbert stress owns EM energy flux.",
    ),
    "SRC4259_01_223_lock": SourceSpec(
        "SRC4259_01_223_lock",
        FORMAL / "223-PPC4161-EM-Poynting-Hodge-source-owner-lock.md",
        "c_Poynt_extra = 0",
        "Poynting once-only lock and retained EM gates.",
    ),
    "SRC4259_02_224_hodge": SourceSpec(
        "SRC4259_02_224_hodge",
        FORMAL / "224-PPC4161-Hodge-deformation-zero-or-constitutive-bound.md",
        "Delta_Hodge_EM = 0",
        "Hodge uniqueness and constitutive countermodel.",
    ),
    "SRC4259_03_234_visible": SourceSpec(
        "SRC4259_03_234_visible",
        FORMAL / "234-PPC4161-visible-EM-material-curl-zero-or-residual-bound.md",
        "I_matter_EM = int_S i_tau omega_visible_EM_residual = 0",
        "Visible EM/material residual zero theorem and fallback bound.",
    ),
    "SRC4259_04_235_component": SourceSpec(
        "SRC4259_04_235_component",
        FORMAL / "235-PPC4161-Dq-source-readout-coupling-marker-zero-or-bound.md",
        "Dq_EM[v]=0",
        "Dq componentwise zero route for quotient-natural readouts.",
    ),
    "SRC4259_05_4218_residuals": SourceSpec(
        "SRC4259_05_4218_residuals",
        SOURCE_DIR / "P8_Y5_R2FR_4218_VISIBLE_EM_RESIDUAL_COMPONENTS.csv",
        "R_cPoynt_extra",
        "Visible EM residual vector rows.",
    ),
    "SRC4259_06_4258_map": SourceSpec(
        "SRC4259_06_4258_map",
        SOURCE_DIR / "P8_Y5_R2FR_4258_COMPONENT_ZERO_CLOSURE_AUDIT.csv",
        "MISSING_HL_EM_HODGE_CONSTITUTIVE_ZERO",
        "4258 says Dq_EM is the next explicit component blocker.",
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


def dq_em_4263_adoption_row() -> Dict[str, str]:
    for row in csv_rows(ADOPTION_4263_PATH):
        if (
            row.get("component") == "Dq_EM"
            and row.get("new_epsilon") == "0.0"
            and row.get("adoption_status") == "ADOPTED_CONDITIONAL_ZERO_FOR_STANDARD_VISIBLE_CLOSED_COLLAR_BRANCH"
        ):
            return row
    return {}


def dq_theta_marker_4264_adoption_row() -> Dict[str, str]:
    for row in csv_rows(ADOPTION_4264_PATH):
        if (
            row.get("component") == "Dq_theta_marker"
            and row.get("new_epsilon") == "0.0"
            and row.get("adoption_status") == "ADOPTED_CONDITIONAL_ZERO_FOR_CALIBRATED_QBASIC_VISIBLE_BRANCH"
        ):
            return row
    return {}


def dq_matter_4265_adoption_row() -> Dict[str, str]:
    for row in csv_rows(ADOPTION_4265_PATH):
        if (
            row.get("component") == "Dq_matter"
            and row.get("new_epsilon") == "0.0"
            and row.get("adoption_status") == "ADOPTED_CONDITIONAL_ZERO_FOR_STANDARD_MATTER_ACTION_DOMAIN_ONLY"
        ):
            return row
    return {}


def dq_source_readout_4266_adoption_row() -> Dict[str, str]:
    for row in csv_rows(ADOPTION_4266_PATH):
        if (
            row.get("component") == "Dq_source_readout"
            and row.get("new_epsilon") == "0.0"
            and row.get("adoption_status") == "ADOPTED_CONDITIONAL_ZERO_FOR_HILBERT_SOURCE_READOUT_BRANCH_ONLY"
        ):
            return row
    return {}


def dq_coeff_4267_adoption_row() -> Dict[str, str]:
    for row in csv_rows(ADOPTION_4267_PATH):
        if (
            row.get("component") == "Dq_coeff"
            and row.get("new_epsilon") == "0.0"
            and row.get("adoption_status") == "ADOPTED_CONDITIONAL_ZERO_FOR_FIXED_PARENT_CONSTANT_BRANCH_ONLY"
        ):
            return row
    return {}


def dq_boundary_projector_4268_adoption_row() -> Dict[str, str]:
    for row in csv_rows(ADOPTION_4268_PATH):
        if (
            row.get("component") == "Dq_boundary_projector"
            and row.get("new_epsilon") == "0.0"
            and row.get("adoption_status") == "ADOPTED_CONDITIONAL_ZERO_FOR_FIXED_NOFLUX_COLLAR_BRANCH_ONLY"
        ):
            return row
    return {}


def dq_tau_4269_adoption_row() -> Dict[str, str]:
    for row in csv_rows(ADOPTION_4269_PATH):
        if (
            row.get("component") == "Dq_tau"
            and row.get("new_epsilon") == "0.0"
            and row.get("adoption_status") == "ADOPTED_CONDITIONAL_ZERO_FOR_QBASIC_OBSERVED_TAU_BRANCH_ONLY"
        ):
            return row
    return {}


def dq_geom_4270_reduced_row() -> Dict[str, str]:
    for row in csv_rows(REDUCED_GEOM_4270_PATH):
        if (
            row.get("probe_id") == "Dq_geom"
            and row.get("new_epsilon") == "MISSING_REDUCED_EPSILON_GEOM_CORE_COFRAME_SHADOW"
        ):
            return row
    return {}


def dq_geom_4271_core_row() -> Dict[str, str]:
    for row in csv_rows(CORE_GEOM_4271_PATH):
        if (
            row.get("probe_id") == "Dq_geom"
            and row.get("new_epsilon") == "MISSING_CORE_FRAME_COUPLING_ZERO_OR_NUMERIC_CG_BDIS_BOUND"
        ):
            return row
    return {}


def dq_geom_4272_bound_row() -> Dict[str, str]:
    for row in csv_rows(BOUND_GEOM_4272_PATH):
        if (
            row.get("probe_id") == "Dq_geom"
            and row.get("new_epsilon") == "MISSING_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS"
        ):
            return row
    return {}


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
            "4259 attacks Dq_EM[Hperp]. It proves Poynting is not an extra source once Maxwell-Hodge Hilbert "
            "stress is imported, then reduces the remaining Dq_EM blocker to a visible EM residual vector: "
            "Hodge/constitutive mismatch, charge/current normalization, EM source weights, radiative flux, "
            "internal exchange, material markers, and standalone Poynting double-counting. No Dq_EM zero is claimed."
        ),
        "current_evidence": (
            "4259 source register, EM component zero theorem, residual vector, component candidate update, "
            "decision and firewall."
        ),
        "status": "private_Dq_EM_residual_vector_ready_nonclaim",
        "next_test": (
            "Close Delta_Hodge_EM from parent-visible action ownership or fill source-backed visible EM residual "
            "bound rows."
        ),
        "key_risk": "Counting Poynting twice or declaring Hodge/constitutive residuals zero from gauge covariance alone.",
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
            "EM4259_0_poynting_not_extra_source",
            "Poynting owner theorem",
            "For S_MH[A,g_obs], Hilbert variation gives T_EM. The Poynting vector S_i=-T_EM(n,e_i) is already EM energy flux in T_total, so a standalone Poynting source coefficient is a double count: c_Poynt_extra=0 if the single source functional is parent-signed.",
            "DERIVED_CONDITIONAL",
            "This closes the common Poynting-as-hidden-force shortcut but not all EM residuals.",
        ),
        (
            "EM4259_1_Dq_EM_zero_contract",
            "Dq_EM component zero",
            "Dq_EM[Hperp]=0 follows if the visible EM readout/action factors through q before variation, Maxwell-Hodge uses the same observed coframe/Hodge, charge/material constants are q-basic, no MTS visible-sector residual exists, and radiative flux is boundary-routed.",
            "DERIVED_CONDITIONAL",
            "Needs Hperp/H_L argument certificate plus visible EM residual vector zero.",
        ),
        (
            "EM4259_2_EM_residual_bound",
            "Dq_EM fallback envelope",
            "epsilon_EM <= sum_abs(delta_w_EM, C_XF2, C_JQ, b_alpha, dlnlambda, b_marker, Delta_Hodge_EM, Delta_rad_Poynting, Delta_internal_exchange, c_Poynt_extra) plus normalization by the relevant source/readout scale.",
            "SOURCE_BACKED_BOUND_FORM",
            "No cancellation between EM residual channels.",
        ),
        (
            "EM4259_3_Hodge_priority",
            "Delta_Hodge priority",
            "Delta_Hodge_EM is the first EM subgate because Hodge uniqueness is mathematical once g_obs/e_obs/orientation and the parent-visible Maxwell action domain are signed.",
            "NEXT_DERIVATION_TARGET",
            "Gauge covariance alone does not force chi_EM=chi(g_obs).",
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


def residual_vector_rows() -> List[Dict[str, str]]:
    source_rows_4218 = csv_rows(SOURCE_DIR / "P8_Y5_R2FR_4218_VISIBLE_EM_RESIDUAL_COMPONENTS.csv")
    output: List[Dict[str, str]] = []
    for row in source_rows_4218:
        coefficient = row.get("coefficient", "")
        if coefficient == "M_H_ref":
            continue
        status = "RETAINED_RESIDUAL_ROW"
        if coefficient == "c_Poynt_extra":
            status = "CONDITIONAL_ZERO_BY_ONCE_ONLY_IF_SINGLE_SOURCE_PARENT_SIGNED"
        elif coefficient == "Delta_Hodge_EM":
            status = "PRIORITY_ZERO_OR_BOUND_SUBTARGET"
        elif coefficient == "Delta_internal_exchange":
            status = "CONDITIONAL_ZERO_BY_WARD_EXCHANGE_IF_SINGLE_VISIBLE_ACTION_SIGNED"
        output.append(
            {
                **common(),
                "component": row.get("component", ""),
                "coefficient": coefficient,
                "meaning": row.get("meaning", ""),
                "absolute_component": row.get("absolute_component", ""),
                "source_basis": row.get("source_basis", ""),
                "current_numeric_value": row.get("numeric_value", "MISSING"),
                "status": status,
                "feeds": "epsilon_EM",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    if output:
        return output
    fallback = [
        ("R_w_EM", "delta_w_EM", "independent Maxwell stress/source multiplier"),
        ("R_XF2", "C_XF2", "hidden MTS coupling to F^2 or F wedge F"),
        ("R_JQ", "C_JQ", "charge/current normalization residual"),
        ("R_balpha", "b_alpha", "vertical drift of effective alpha"),
        ("R_dlambda", "dlnlambda_derivative", "varying Maxwell kinetic normalization"),
        ("R_marker", "b_A/b_marker", "material/clock/EM marker drift"),
        ("R_Hodge", "Delta_Hodge_EM", "constitutive/Hodge mismatch"),
        ("R_rad_Poynting", "Delta_rad_Poynting", "open radiative Poynting flux"),
        ("R_internal_exchange", "Delta_internal_exchange", "matter-EM exchange not owned by one action"),
        ("R_cPoynt_extra", "c_Poynt_extra", "standalone Poynting source double count"),
    ]
    return [
        {
            **common(),
            "component": component,
            "coefficient": coefficient,
            "meaning": meaning,
            "absolute_component": f"abs({coefficient})",
            "source_basis": "fallback_4259",
            "current_numeric_value": "MISSING",
            "status": "RETAINED_RESIDUAL_ROW",
            "feeds": "epsilon_EM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for component, coefficient, meaning in fallback
    ]


def em_gate_rows() -> List[Dict[str, str]]:
    raw = [
        ("EMG4259_0_same_hodge_action", "Maxwell-Hodge uses g_obs/e_obs before variation", "conditional_private_selector", "needed for Dq_EM zero"),
        ("EMG4259_1_no_independent_chi", "no independent chi_EM / hidden EM metric / skewon / active axion-gradient", "unsigned_current_corpus", "feeds Delta_Hodge_EM"),
        ("EMG4259_2_charge_qbasic", "charge/current normalization and alpha/material labels are calibrated q-basic constants", "unsigned_or_calibrated_nonclaim", "feeds C_JQ/b_alpha/marker rows"),
        ("EMG4259_3_no_extra_XF2", "no extra MTS X F^2 or F wedge F side-channel", "unsigned_current_corpus", "feeds C_XF2"),
        ("EMG4259_4_poynting_once", "Poynting flux is T_EM^{0i}, not a second source", "derived_conditional_once_only", "feeds c_Poynt_extra"),
        ("EMG4259_5_rad_boundary", "live radiative Poynting flux is boundary/Hamiltonian-routed", "retained_boundary_gate", "feeds Delta_rad_Poynting"),
        ("EMG4259_6_Hperp_argument", "the H_L/Hperp direction is admitted for the EM readout", "missing_HL_EM_argument_certificate", "feeds Dq_EM[Hperp]"),
    ]
    return [
        {
            **common(),
            "gate_id": gate_id,
            "condition": condition,
            "status": status,
            "feeds": feeds,
            "Dq_EM_zero_claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for gate_id, condition, status, feeds in raw
    ]


def component_candidate_rows() -> List[Dict[str, str]]:
    previous = csv_rows(PREVIOUS_COMPONENT_CANDIDATE_PATH)
    adoption_4263 = dq_em_4263_adoption_row()
    adoption_4264 = dq_theta_marker_4264_adoption_row()
    adoption_4265 = dq_matter_4265_adoption_row()
    adoption_4266 = dq_source_readout_4266_adoption_row()
    adoption_4267 = dq_coeff_4267_adoption_row()
    adoption_4268 = dq_boundary_projector_4268_adoption_row()
    adoption_4269 = dq_tau_4269_adoption_row()
    reduced_geom_4270 = dq_geom_4270_reduced_row()
    core_geom_4271 = dq_geom_4271_core_row()
    bound_geom_4272 = dq_geom_4272_bound_row()
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
        if probe == "Dq_EM":
            if adoption_4263:
                updated["epsilon"] = adoption_4263.get("new_epsilon", "0.0")
                updated["epsilon_C1"] = adoption_4263.get("new_epsilon_C1", "0.0")
                updated["source_path"] = str(FORMAL_4263_PATH)
            else:
                updated["epsilon"] = "MISSING_EPSILON_EM_VISIBLE_RESIDUAL_VECTOR"
                updated["epsilon_C1"] = "MISSING_C1_ZERO_PROOF_OR_PROFILE_Dq_EM_PLUS_EM_RESIDUAL_DERIVATIVES"
                updated["source_path"] = str(FORMAL_PATH)
            updated["valid_for_claim"] = "False"
        elif probe == "Dq_theta_marker" and adoption_4264:
            updated["epsilon"] = adoption_4264.get("new_epsilon", "0.0")
            updated["epsilon_C1"] = adoption_4264.get("new_epsilon_C1", "0.0")
            updated["source_path"] = str(FORMAL_4264_PATH)
            updated["valid_for_claim"] = "False"
        elif probe == "Dq_matter" and adoption_4265:
            updated["epsilon"] = adoption_4265.get("new_epsilon", "0.0")
            updated["epsilon_C1"] = adoption_4265.get("new_epsilon_C1", "0.0")
            updated["source_path"] = str(FORMAL_4265_PATH)
            updated["valid_for_claim"] = "False"
        elif probe == "Dq_source_readout" and adoption_4266:
            updated["epsilon"] = adoption_4266.get("new_epsilon", "0.0")
            updated["epsilon_C1"] = adoption_4266.get("new_epsilon_C1", "0.0")
            updated["source_path"] = str(FORMAL_4266_PATH)
            updated["valid_for_claim"] = "False"
        elif probe == "Dq_coeff" and adoption_4267:
            updated["epsilon"] = adoption_4267.get("new_epsilon", "0.0")
            updated["epsilon_C1"] = adoption_4267.get("new_epsilon_C1", "0.0")
            updated["source_path"] = str(FORMAL_4267_PATH)
            updated["valid_for_claim"] = "False"
        elif probe == "Dq_boundary_projector" and adoption_4268:
            updated["epsilon"] = adoption_4268.get("new_epsilon", "0.0")
            updated["epsilon_C1"] = adoption_4268.get("new_epsilon_C1", "0.0")
            updated["source_path"] = str(FORMAL_4268_PATH)
            updated["valid_for_claim"] = "False"
        elif probe == "Dq_tau" and adoption_4269:
            updated["epsilon"] = adoption_4269.get("new_epsilon", "0.0")
            updated["epsilon_C1"] = adoption_4269.get("new_epsilon_C1", "0.0")
            updated["source_path"] = str(FORMAL_4269_PATH)
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
                    "epsilon": adoption_4263.get("new_epsilon", "0.0") if probe == "Dq_EM" and adoption_4263 else (adoption_4264.get("new_epsilon", "0.0") if probe == "Dq_theta_marker" and adoption_4264 else (adoption_4265.get("new_epsilon", "0.0") if probe == "Dq_matter" and adoption_4265 else (adoption_4266.get("new_epsilon", "0.0") if probe == "Dq_source_readout" and adoption_4266 else (adoption_4267.get("new_epsilon", "0.0") if probe == "Dq_coeff" and adoption_4267 else (adoption_4268.get("new_epsilon", "0.0") if probe == "Dq_boundary_projector" and adoption_4268 else ("MISSING_EPSILON_EM_VISIBLE_RESIDUAL_VECTOR" if probe == "Dq_EM" else f"MISSING_ZERO_PROOF_OR_PROFILE_{probe}")))))),
                    "epsilon_C1": adoption_4263.get("new_epsilon_C1", "0.0") if probe == "Dq_EM" and adoption_4263 else (adoption_4264.get("new_epsilon_C1", "0.0") if probe == "Dq_theta_marker" and adoption_4264 else (adoption_4265.get("new_epsilon_C1", "0.0") if probe == "Dq_matter" and adoption_4265 else (adoption_4266.get("new_epsilon_C1", "0.0") if probe == "Dq_source_readout" and adoption_4266 else (adoption_4267.get("new_epsilon_C1", "0.0") if probe == "Dq_coeff" and adoption_4267 else (adoption_4268.get("new_epsilon_C1", "0.0") if probe == "Dq_boundary_projector" and adoption_4268 else f"MISSING_C1_ZERO_PROOF_OR_PROFILE_{probe}"))))),
                    "source_path": str(FORMAL_4263_PATH) if probe == "Dq_EM" and adoption_4263 else (str(FORMAL_4264_PATH) if probe == "Dq_theta_marker" and adoption_4264 else (str(FORMAL_4265_PATH) if probe == "Dq_matter" and adoption_4265 else (str(FORMAL_4266_PATH) if probe == "Dq_source_readout" and adoption_4266 else (str(FORMAL_4267_PATH) if probe == "Dq_coeff" and adoption_4267 else (str(FORMAL_4268_PATH) if probe == "Dq_boundary_projector" and adoption_4268 else str(FORMAL_PATH)))))),
                    "valid_for_claim": "False",
                }
            )
    if reduced_geom_4270:
        for row in output:
            if row.get("probe_id") == "Dq_geom":
                row["epsilon"] = reduced_geom_4270.get("new_epsilon", "MISSING_REDUCED_EPSILON_GEOM_CORE_COFRAME_SHADOW")
                row["epsilon_C1"] = reduced_geom_4270.get("new_epsilon_C1", "MISSING_REDUCED_C1_GEOM_CORE_COFRAME_SHADOW")
                row["source_path"] = str(FORMAL_4270_PATH)
                row["valid_for_claim"] = "False"
    if core_geom_4271:
        for row in output:
            if row.get("probe_id") == "Dq_geom":
                row["epsilon"] = core_geom_4271.get("new_epsilon", "MISSING_CORE_FRAME_COUPLING_ZERO_OR_NUMERIC_CG_BDIS_BOUND")
                row["epsilon_C1"] = core_geom_4271.get("new_epsilon_C1", "MISSING_C1_CORE_FRAME_COUPLING_ZERO_OR_NUMERIC_CG_BDIS_BOUND")
                row["source_path"] = str(FORMAL_4271_PATH)
                row["valid_for_claim"] = "False"
    if bound_geom_4272:
        for row in output:
            if row.get("probe_id") == "Dq_geom":
                row["epsilon"] = bound_geom_4272.get("new_epsilon", "MISSING_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS")
                row["epsilon_C1"] = bound_geom_4272.get("new_epsilon_C1", "MISSING_C1_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS")
                row["source_path"] = str(FORMAL_4272_PATH)
                row["valid_for_claim"] = "False"
    return output


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4259_0_poynting_resolved",
            "Poynting is not the missing hidden force; it is already Maxwell-Hodge Hilbert flux when the safe branch is used.",
            "This directly addresses the Poynting fork without double-counting.",
            "Keep c_Poynt_extra forbidden unless a new explicit source row is introduced.",
        ),
        (
            "DEC4259_1_EM_real_missing",
            "The real Dq_EM blocker is the visible EM residual vector, especially Delta_Hodge_EM and charge/current normalization.",
            "That is a finite closure/bound problem, not vague EM mystery.",
            NEXT_TARGET,
        ),
        (
            "DEC4259_2_component_feed",
            "4254 now receives a Dq_EM placeholder tied to the visible EM residual vector.",
            "No epsilon value is fabricated; downstream remains nonclaim.",
            "Rerun 4254 after any EM residual component is zeroed or bounded.",
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
        ("FW4259_0_poynting_double_count", "adding Poynting as a separate bulk source after T_EM is in T_total", "POYNTING_ONCE_ONLY_REQUIRED"),
        ("FW4259_1_gauge_covariance", "declaring Delta_Hodge_EM=0 from gauge covariance alone", "VISIBLE_EM_ACTION_DOMAIN_REQUIRED"),
        ("FW4259_2_alpha_prediction", "using calibrated visible EM as an alpha_EM prediction", "ALPHA_PREDICTION_SEPARATE_GATE"),
        ("FW4259_3_Dq_EM_zero", "claiming Dq_EM[Hperp]=0 without H_L/Hperp EM argument certificate", "HL_EM_ARGUMENT_REQUIRED"),
        ("FW4259_4_cancellation", "letting EM residual channels cancel each other", "SUM_ABS_RESIDUAL_BOUND_REQUIRED"),
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
            "status_id": "STATUS4259_0",
            "summary": (
                "4259 reduces Dq_EM to a finite visible EM residual vector. Poynting is guarded as Hilbert "
                "flux, not an extra force; Delta_Hodge_EM is the next best subgate."
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
                "Try to close Delta_Hodge_EM by parent-visible Maxwell action ownership, or create source-backed "
                "numeric/bound rows for the retained visible EM residual vector."
            ),
            "avoid": "Do not count Poynting twice and do not infer Hodge uniqueness without the action-domain clause.",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 275 - PPC4161 EM-Hodge component zero or residual vector

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4259 does not prove `Dq_EM[Hperp]=0`, local GR, Maxwell derivation, alpha prediction, PPN safety, R10 safety, or clock safety. It attacks the EM component blocker and replaces vague EM language with a finite residual vector.

## What closes structurally

Inside the safe local branch:

```text
S_MH[A,g_obs] = -1/4 int sqrt(-g_obs) F_mu_nu F^mu_nu,
T_EM^{{mu nu}} = F^{{mu alpha}}F^nu_alpha - 1/4 g_obs^{{mu nu}}F^2,
S_i = -T_EM(n,e_i) = (E x B)_i.
```

Therefore Poynting is not an extra background source. It is EM Hilbert flux already inside `T_total`. A standalone Poynting source term is forbidden unless a new explicit source row is introduced:

```text
c_Poynt_extra = 0
```

under the single-source-functional lock.

## Dq_EM zero contract

The component zero route is:

```text
standard visible EM import
+ same observed Maxwell-Hodge/coframe
+ q-basic charge/current/material labels
+ no DeltaS_MTS_visible
+ radiative flux boundary-routed
+ Hperp admitted for the EM readout
=> Dq_EM[Hperp]=0.
```

Current sources do not sign all clauses, so the component remains nonclaim.

## Retained EM residual vector

The finite fallback is:

```text
epsilon_EM <= sum_abs(
  delta_w_EM,
  C_XF2,
  C_JQ,
  b_alpha,
  dlnlambda,
  b_marker,
  Delta_Hodge_EM,
  Delta_rad_Poynting,
  Delta_internal_exchange,
  c_Poynt_extra
).
```

No cancellation is allowed. `Delta_Hodge_EM` is the best next target because Hodge uniqueness is mathematical once the observed coframe/orientation and parent-visible Maxwell action domain are signed.

## 4254 feed

4259 rewrites the `Dq_EM` component candidate as:

```text
MISSING_EPSILON_EM_VISIBLE_RESIDUAL_VECTOR.
```

This keeps the source-probe runner honest while making the missing physics much sharper.

## Next target

`{NEXT_TARGET}` should close `Delta_Hodge_EM` or fill the visible EM residual-vector bound rows.
"""


def checkpoint_doc() -> str:
    return f"""
# 4259 - Y5 R2FR EM-Hodge component zero or residual vector

Packet marker: `{PACKET_MARKER}`

## Result

4259 attacks `Dq_EM[Hperp]`.

The useful win:

```text
Poynting = Maxwell-Hodge Hilbert flux,
not a second source.
```

The remaining blocker is now finite:

```text
epsilon_EM_visible_residual_vector.
```

## Claim status

Private nonclaim. `Dq_EM` remains open until `Delta_Hodge_EM`, source weights, charge/current normalization, radiative flux, internal exchange, material markers, and the Hperp EM argument certificate are zeroed or bounded.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    theorems = csv_rows(paths["theorems"])
    residuals = csv_rows(paths["residuals"])
    candidates = csv_rows(paths["candidates"])
    em_candidate = [row for row in candidates if row.get("probe_id") == "Dq_EM"]
    adoption_active = bool(dq_em_4263_adoption_row())
    theta_adoption_active = bool(dq_theta_marker_4264_adoption_row())
    matter_adoption_active = bool(dq_matter_4265_adoption_row())
    source_readout_adoption_active = bool(dq_source_readout_4266_adoption_row())
    coeff_adoption_active = bool(dq_coeff_4267_adoption_row())
    boundary_adoption_active = bool(dq_boundary_projector_4268_adoption_row())
    tau_adoption_active = bool(dq_tau_4269_adoption_row())
    rows = [
        ("VAL4259_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4259_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        ("VAL4259_2_poynting_theorem", any("Poynting" in row["name"] for row in theorems), "Poynting theorem emitted"),
        ("VAL4259_3_residual_vector", len(residuals) >= 10, "visible EM residual vector rows emitted"),
        ("VAL4259_4_hodge_priority", any(row["coefficient"] == "Delta_Hodge_EM" for row in residuals), "Delta_Hodge_EM row present"),
        ("VAL4259_5_4254_candidate_written", COMPONENT_CANDIDATE_4254_PATH.exists(), "4254 component candidate path written"),
        (
            "VAL4259_6_Dq_EM_refined",
            bool(em_candidate)
            and (
                "VISIBLE_RESIDUAL_VECTOR" in em_candidate[0].get("epsilon", "")
                or (adoption_active and em_candidate[0].get("epsilon") == "0.0")
            ),
            "Dq_EM candidate refined or preserved from 4263 adoption",
        ),
        ("VAL4259_7_candidate_nonclaim", bool(candidates) and all(row["valid_for_claim"] == "False" for row in candidates), "candidate rows stay nonclaim"),
        (
            "VAL4259_8_no_fake_zero",
            all(
                row.get("epsilon", "") not in {"0", "0.0"}
                or (adoption_active and row.get("probe_id") == "Dq_EM")
                or (theta_adoption_active and row.get("probe_id") == "Dq_theta_marker")
                or (matter_adoption_active and row.get("probe_id") == "Dq_matter")
                or (source_readout_adoption_active and row.get("probe_id") == "Dq_source_readout")
                or (coeff_adoption_active and row.get("probe_id") == "Dq_coeff")
                or (boundary_adoption_active and row.get("probe_id") == "Dq_boundary_projector")
                or (tau_adoption_active and row.get("probe_id") == "Dq_tau")
                for row in candidates
            ),
            "no epsilon zero fabricated except sourced component adoptions",
        ),
        ("VAL4259_9_claim_row", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4259_10_formal_doc", MARKER in read_text(FORMAL_PATH), "formal marker present"),
        ("VAL4259_11_checkpoint_doc", PACKET_MARKER in read_text(DOC_PATH), "checkpoint marker present"),
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
    source_path = SOURCE_DIR / "P8_Y5_R2FR_4259_SOURCE_REGISTER.csv"
    theorem_path = SOURCE_DIR / "P8_Y5_R2FR_4259_EM_COMPONENT_THEOREMS.csv"
    residual_path = SOURCE_DIR / "P8_Y5_R2FR_4259_EM_VISIBLE_RESIDUAL_VECTOR.csv"
    gate_path = SOURCE_DIR / "P8_Y5_R2FR_4259_EM_ZERO_GATES.csv"
    decision_path = SOURCE_DIR / "P8_Y5_R2FR_4259_DECISION.csv"
    firewall_path = SOURCE_DIR / "P8_Y5_R2FR_4259_CLAIM_FIREWALL.csv"
    status_path = SOURCE_DIR / "P8_Y5_R2FR_4259_STATUS.csv"
    next_path = SOURCE_DIR / "P8_Y5_R2FR_4259_NEXT_TARGET.csv"

    candidates = component_candidate_rows()

    write_csv(source_path, source_rows())
    write_csv(theorem_path, theorem_rows())
    write_csv(residual_path, residual_vector_rows())
    write_csv(gate_path, em_gate_rows())
    write_csv(LOCAL_COMPONENT_CANDIDATE_PATH, candidates)
    write_csv(COMPONENT_CANDIDATE_4254_PATH, candidates)
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
        "residuals": residual_path,
        "candidates": LOCAL_COMPONENT_CANDIDATE_PATH,
    }
    validation = validation_rows(paths)
    write_csv(VALIDATION_PATH, validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote 11 csv artifacts")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")


if __name__ == "__main__":
    main()
