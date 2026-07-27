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

CHECKPOINT = "4266"
CLAIM_ID = "L-107"
BRANCH = "MTS_R2FR_Y5_DQ_SOURCE_READOUT_HILBERT_CHARGE_ZERO_OR_COEFF_REMAINDER_4266"
DECISION = "DQ_SOURCE_READOUT_ADOPTED_FOR_HILBERT_CHARGE_BRANCH_COEFFICIENT_OWNER_RETAINED_NONCLAIM"
MARKER = "PPC4161_DQ_SOURCE_READOUT_HILBERT_CHARGE_ZERO_OR_COEFF_REMAINDER_4266"
PACKET_MARKER = "PPC4161_PACKET_DQ_SOURCE_READOUT_HILBERT_CHARGE_ZERO_OR_COEFF_REMAINDER_4266"
NEXT_TARGET = "4267-Y5-R2FR-Dq-coeff-common-coupling-owner-or-Newton-constant-calibration-bound.md"

FORMAL_PATH = FORMAL / "282-PPC4161-Dq-source-readout-Hilbert-charge-zero-or-coefficient-remainder.md"
DOC_PATH = POST / "4266-Y5-R2FR-Dq-source-readout-or-coefficient-prefactor-zero.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4266_VALIDATION.csv"
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

LIVE_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4254_DQ_COMPONENT_VALUES_CANDIDATE.csv"
LOCAL_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4266_DQ_COMPONENT_VALUES_CANDIDATE.csv"

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
    "SRC4266_00_4177_quotient": SourceSpec(
        "SRC4266_00_4177_quotient",
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "S_matter = Sbar_m[psi, g_obs(q), A(q), theta(q)].",
        "Quotient-natural matter descent gives the chain-rule base.",
    ),
    "SRC4266_01_4210_visible": SourceSpec(
        "SRC4266_01_4210_visible",
        FORMAL / "226-PPC4161-standard-visible-matter-import-contract.md",
        "S_matter[psi,g_obs,theta_obs]",
        "Standard visible matter import fixes the observed matter domain.",
    ),
    "SRC4266_02_4219_dq_contract": SourceSpec(
        "SRC4266_02_4219_dq_contract",
        FORMAL / "235-PPC4161-Dq-source-readout-coupling-marker-zero-or-bound.md",
        "Dq_source_readout[v]=0",
        "Componentwise Dq zero contract names source-readout as its own leg.",
    ),
    "SRC4266_03_4265_formal": SourceSpec(
        "SRC4266_03_4265_formal",
        FORMAL / "281-PPC4161-Dq-matter-action-domain-zero-or-source-prefactor-bound.md",
        "Hamiltonian charge to observed mass readout",
        "4265 explicitly left source-readout and coefficient ownership to this step.",
    ),
    "SRC4266_04_4265_split": SourceSpec(
        "SRC4266_04_4265_split",
        SOURCE_DIR / "P8_Y5_R2FR_4265_SOURCE_PREFACTOR_SPLIT_ROWS.csv",
        "SPL4265_2_measured_mass_map",
        "Measured-source map was retained as a live source-readout gate.",
    ),
    "SRC4266_05_1113_contract": SourceSpec(
        "SRC4266_05_1113_contract",
        POST / "1113-Y5-R10-parent-owned-readout-descent-contract-or-alpha-product-input-acquisition.md",
        "source functor sees total observed stress, not species-labelled pairs",
        "Parent-owned readout contract gives the label-forgetting target.",
    ),
    "SRC4266_06_1116_generators": SourceSpec(
        "SRC4266_06_1116_generators",
        POST / "1116-Y5-R10-invariant-generator-kill-list-or-coupling-prior-source-pack.md",
        "species_charge_constants",
        "Surviving source/species constants remain a coefficient or generator debt if not typed out.",
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
            "4266 adopts Dq_source_readout=0 and its C1 row only for the Hilbert/ADM source-charge branch: "
            "the observed source is a post-solution functional of q-basic g_obs, theta_obs and the Hilbert stress "
            "already controlled by 4265. This kills hidden vertical source-readout variation, but it does not derive "
            "the numerical Newton constant, kappa/G normalization, boundary/projector ownership, or hidden species-weight coefficients."
        ),
        "current_evidence": (
            "4266 source register, Hilbert source-readout theorem rows, coefficient/source remainder split, "
            "Dq_source_readout adoption row, updated component candidate, decision and firewall."
        ),
        "status": "private_Dq_source_readout_conditional_zero_adopted_for_Hilbert_charge_branch_nonclaim",
        "next_test": "Attack Dq_coeff next; 4254 remains blocked by coefficient ownership plus geometry/tau/boundary/constants.",
        "key_risk": "Mistaking post-solution source-charge q-basicity for a derivation of G_N or for silence of hidden coefficient/species weights.",
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


def source_readout_theorem_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "SRCRO4266_0_definition_split",
            "source readout component",
            "Dq_source_readout is restricted here to post-solution source-charge readout from observed Hilbert stress and observed collar data, not to coefficient owners or boundary selectors.",
            "DEFINITION_SPLIT",
            "pre-variation species weights and coupling scales are excluded from the adopted zero",
        ),
        (
            "SRCRO4266_1_hilbert_stress_qbasic",
            "Hilbert stress q-basicity",
            "With S_matter=Sbar_m[psi,g_obs,theta_obs] and theta_obs fixed, T_obs := -2/sqrt|g| dSbar_m/dg_obs is a functional of q-observed fields, so delta_v T_obs=0 for v in ker(Dq).",
            "CONDITIONAL_THEOREM",
            "depends on 4265 and fails if direct hidden matter operators or hidden species weights enter before variation",
        ),
        (
            "SRCRO4266_2_charge_readout_zero",
            "source charge readout zero",
            "For Q_src=Qbar_src[T_obs,g_obs,Sigma_obs,xi_obs] with the source collar/projector assigned outside this component, delta_v Q_src=DQbar_src[Dq v]=0.",
            "CONDITIONAL_ZERO_FOR_HILBERT_SOURCE_READOUT",
            "boundary/projector variation remains in Dq_boundary_projector",
        ),
        (
            "SRCRO4266_3_common_mode_split",
            "common calibration split",
            "For an observed GM-like product, delta_v(kappa_cal Q_src)=(delta_v kappa_cal) Q_src+kappa_cal delta_v Q_src; 4266 kills only the second term.",
            "COEFFICIENT_REMAINDER_RETAINED",
            "kappa_cal, G_N, ell_J and unit-normalization owners remain Dq_coeff or tomography constants",
        ),
        (
            "SRCRO4266_4_relative_source_silence",
            "relative source label silence",
            "If the source functor sees total observed stress and not species-labelled hidden pairs, relative source-label readout derivatives vanish in this branch.",
            "CONDITIONAL_LABEL_FORGETTING",
            "species_charge_constants remain a Dq_coeff/generator debt if promoted to parent data",
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


def remainder_split_rows() -> List[Dict[str, str]]:
    raw = [
        ("REM4266_0_kappa_G_owner", "delta_v kappa_cal_or_G_N", "common coupling/calibration scale", "Dq_coeff_or_tomography_constants", "RETAINED"),
        ("REM4266_1_ellJ_owner", "delta_v ell_J_or_source_current_norm", "source-current normalization owner", "Dq_coeff", "RETAINED"),
        ("REM4266_2_boundary_projector", "delta_v Sigma_obs_or_worldtube_projector", "source collar/domain/projector choice", "Dq_boundary_projector", "RETAINED"),
        ("REM4266_3_species_weight", "delta_v w_A_hidden", "hidden pre-variation species/source weight", "Dq_coeff_or_generator_debt", "RETAINED_IF_ADDED"),
        ("REM4266_4_hilbert_charge", "delta_v Q_src_Hilbert", "post-solution observed Hilbert/ADM source charge", "Dq_source_readout", "ZERO_IN_STANDARD_BRANCH"),
        ("REM4266_5_relative_label_readout", "delta_v Delta_source_label", "relative species label readout after total-stress forgetting", "Dq_source_readout", "ZERO_IF_LABEL_FORGETTING_BRANCH"),
    ]
    return [
        {
            **common(),
            "remainder_id": remainder_id,
            "coefficient_or_tail": coefficient,
            "meaning": meaning,
            "assigned_live_gate": gate,
            "4266_status": status,
            "deformation_requirement": "MISSING_SOURCE_BACKED_BOUND_OR_ZERO_PROOF_IF_REOPENED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for remainder_id, coefficient, meaning, gate, status in raw
    ]


def adoption_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "adoption_id": "ADOPT4266_Dq_source_readout",
            "component": "Dq_source_readout",
            "old_epsilon": "MISSING_ZERO_PROOF_OR_PROFILE_Dq_source_readout",
            "new_epsilon": "0.0",
            "new_epsilon_C1": "0.0",
            "adoption_status": "ADOPTED_CONDITIONAL_ZERO_FOR_HILBERT_SOURCE_READOUT_BRANCH_ONLY",
            "source_path": str(FORMAL_PATH),
            "conditions": (
                "observed source charge is a post-solution Hilbert/ADM functional of q-basic g_obs, theta_obs and T_obs; "
                "source collar/projector is assigned to Dq_boundary_projector; kappa/G/unit owners and hidden species weights remain Dq_coeff or generator debts"
            ),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def component_candidate_rows() -> List[Dict[str, str]]:
    previous = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
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
        if probe == "Dq_source_readout":
            updated["epsilon"] = "0.0"
            updated["epsilon_C1"] = "0.0"
            updated["source_path"] = str(FORMAL_PATH)
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
                    "epsilon": "0.0" if probe == "Dq_source_readout" else (adoption_4267.get("new_epsilon", "0.0") if probe == "Dq_coeff" and adoption_4267 else (adoption_4268.get("new_epsilon", "0.0") if probe == "Dq_boundary_projector" and adoption_4268 else (adoption_4269.get("new_epsilon", "0.0") if probe == "Dq_tau" and adoption_4269 else f"MISSING_ZERO_PROOF_OR_PROFILE_{probe}"))),
                    "epsilon_C1": "0.0" if probe == "Dq_source_readout" else (adoption_4267.get("new_epsilon_C1", "0.0") if probe == "Dq_coeff" and adoption_4267 else (adoption_4268.get("new_epsilon_C1", "0.0") if probe == "Dq_boundary_projector" and adoption_4268 else (adoption_4269.get("new_epsilon_C1", "0.0") if probe == "Dq_tau" and adoption_4269 else f"MISSING_C1_ZERO_PROOF_OR_PROFILE_{probe}"))),
                    "source_path": str(FORMAL_PATH) if (probe != "Dq_coeff" or not adoption_4267) and (probe != "Dq_boundary_projector" or not adoption_4268) and (probe != "Dq_tau" or not adoption_4269) else (str(FORMAL_4267_PATH) if probe == "Dq_coeff" else (str(FORMAL_4268_PATH) if probe == "Dq_boundary_projector" else str(FORMAL_4269_PATH))),
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
            "DEC4266_0_adopt_source_readout",
            "Adopt Dq_source_readout=0 for the standard Hilbert/ADM source-charge readout branch.",
            "Observed source charge is a post-solution functional of q-basic Hilbert stress, so hidden vertical variation dies by chain rule.",
            NEXT_TARGET,
        ),
        (
            "DEC4266_1_retain_coeff_owner",
            "Do not derive G_N, kappa, ell_J, or source-current normalization here.",
            "The product delta_v(kappa Q_src) leaves a coefficient-owner term even when delta_v Q_src=0.",
            "Attack Dq_coeff next.",
        ),
        (
            "DEC4266_2_4254_progress",
            "4254 should now lose Dq_source_readout from the missing list while staying blocked by honest remaining rows.",
            "This moves the local-GR ladder from source-readout leak to coefficient/geometry/tau/boundary debts.",
            "Rerun 4254 after 4266.",
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
        ("FW4266_0_G_shortcut", "using Hilbert source-readout zero to claim a derivation of numerical G_N", "DQ_COEFF_OR_CALIBRATION_CONSTANT_GATE_REQUIRED"),
        ("FW4266_1_species_shortcut", "hiding hidden species weights inside the post-solution source charge", "DQ_COEFF_OR_GENERATOR_DEBT_REQUIRED"),
        ("FW4266_2_boundary_shortcut", "absorbing changing source/worldtube projectors into Q_src", "DQ_BOUNDARY_PROJECTOR_REQUIRED"),
        ("FW4266_3_WEP_claim_jump", "treating source-readout q-basicity as a WEP/R10/local-GR pass", "REMAINING_COMPONENTS_AND_TOMOGRAPHY_REQUIRED"),
        ("FW4266_4_coeff_claim_jump", "declaring Dq_coeff zero because Q_src is q-basic", "SEPARATE_COEFFICIENT_OWNER_THEOREM_REQUIRED"),
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
            "status_id": "STATUS4266_0",
            "summary": (
                "4266 moves Dq_source_readout from missing to a conditional zero for the Hilbert/ADM source-charge branch, "
                "while retaining kappa/G/source-current coefficient owners and boundary/projector terms as separate live gates."
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
            "objective": "Attack Dq_coeff: decide whether kappa/G/ell_J/common source-current normalization is fixed calibration, parent-owned constant, or finite coefficient bound.",
            "avoid": "Do not pretend GR derives G_N numerically; distinguish calibrated common coupling from hidden vertical coefficient drift.",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 282 - PPC4161 Dq-source-readout Hilbert-charge zero or coefficient remainder

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4266 does not prove public local GR, WEP, R10, PPN, measured `G_N`, or a numerical source-coupling value.

It adopts:

```text
Dq_source_readout = 0
```

only for the standard Hilbert/ADM source-charge readout branch.

## Split

Closed here:

```text
Q_src = Qbar_src[T_obs, g_obs, Sigma_obs, xi_obs]
T_obs = -2/sqrt|g_obs| delta Sbar_m / delta g_obs
```

where `S_matter` already descends by 4265 and the source readout is post-solution.

Not closed here:

```text
kappa/G/ell_J coefficient owner,
source-current normalization,
hidden species/source weights w_A(Phi),
changing source collar/worldtube/projector,
domain selector reentry,
numeric value of G_N.
```

Those stay in `Dq_coeff`, `Dq_boundary_projector`, tomography constants, or finite bound rows.

## Hilbert source-readout theorem

If:

```text
S_matter = Sbar_m[psi, g_obs, theta_obs],
delta_v g_obs = 0,
delta_v theta_obs = 0,
v in ker(Dq),
```

then:

```text
delta_v T_obs = 0.
```

If the source charge is:

```text
Q_src = Qbar_src[T_obs, g_obs, Sigma_obs, xi_obs],
```

with the collar/projector assigned outside this component, then:

```text
delta_v Q_src = D Qbar_src[Dq v] = 0.
```

Therefore:

```text
Dq_source_readout = 0,
Dq_source_readout_C1 = 0
```

for the standard Hilbert/ADM source-readout branch.

## Coefficient tax

For an observed Newtonian product:

```text
delta_v(kappa_cal Q_src)
= (delta_v kappa_cal) Q_src + kappa_cal delta_v Q_src.
```

4266 kills only:

```text
kappa_cal delta_v Q_src.
```

The surviving term:

```text
(delta_v kappa_cal) Q_src
```

is the next `Dq_coeff` problem. This is the same reason GR uses a coupling constant; deriving or calibrating its numerical value is a different gate.

## 4254 feed

The live component candidate is updated:

```text
Dq_source_readout = 0.0,
Dq_source_readout_C1 = 0.0.
```

The row remains `valid_for_claim=false` because the complete 4254 source-probe/tomography gate still needs coefficient, geometry, tau, boundary/projector and constants.

## Next target

`{NEXT_TARGET}` should attack `Dq_coeff`.
"""


def checkpoint_doc() -> str:
    return f"""
# 4266 - Y5 R2FR Dq-source-readout or coefficient-prefactor zero

Packet marker: `{PACKET_MARKER}`

## Result

4266 adopts:

```text
Dq_source_readout = 0.0,
Dq_source_readout_C1 = 0.0
```

for the standard Hilbert/ADM source-charge readout branch only.

The coefficient owner remains live:

```text
delta_v(kappa_cal Q_src) = (delta_v kappa_cal) Q_src.
```

## Claim status

Private nonclaim. This narrows the component ledger without smuggling a derivation of `G_N`, WEP, R10, or local-GR safety.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    theorems = csv_rows(paths["theorems"])
    remainder = csv_rows(paths["remainder"])
    adoption = csv_rows(paths["adoption"])
    local_candidate = csv_rows(paths["local_candidate"])
    live_candidate = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
    live_source = [row for row in live_candidate if row.get("probe_id") == "Dq_source_readout"]
    live_matter = [row for row in live_candidate if row.get("probe_id") == "Dq_matter"]
    live_theta = [row for row in live_candidate if row.get("probe_id") == "Dq_theta_marker"]
    live_em = [row for row in live_candidate if row.get("probe_id") == "Dq_EM"]
    live_coeff = [row for row in live_candidate if row.get("probe_id") == "Dq_coeff"]
    coeff_adoption = dq_coeff_4267_adoption_row()
    rows = [
        ("VAL4266_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4266_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4266_2_hilbert_charge_zero_theorem",
            any(row["status"] == "CONDITIONAL_ZERO_FOR_HILBERT_SOURCE_READOUT" for row in theorems),
            "Hilbert source-readout zero theorem emitted",
        ),
        (
            "VAL4266_3_coeff_remainder_retained",
            any(row["assigned_live_gate"] == "Dq_coeff_or_tomography_constants" for row in remainder)
            and any(row["assigned_live_gate"] == "Dq_boundary_projector" for row in remainder),
            "coefficient and boundary/projector remainders retained",
        ),
        (
            "VAL4266_4_adoption_row",
            bool(adoption)
            and adoption[0]["new_epsilon"] == "0.0"
            and adoption[0]["adoption_status"] == "ADOPTED_CONDITIONAL_ZERO_FOR_HILBERT_SOURCE_READOUT_BRANCH_ONLY",
            "Dq_source_readout adoption row emitted",
        ),
        (
            "VAL4266_5_local_candidate_numeric",
            any(row.get("probe_id") == "Dq_source_readout" and row.get("epsilon") == "0.0" and row.get("epsilon_C1") == "0.0" for row in local_candidate),
            "local 4266 candidate has numeric source-readout zero",
        ),
        (
            "VAL4266_6_live_4254_updated",
            bool(live_source)
            and live_source[0].get("epsilon") == "0.0"
            and live_source[0].get("epsilon_C1") == "0.0"
            and live_source[0].get("source_path") == str(FORMAL_PATH),
            "live 4254 candidate Dq_source_readout updated",
        ),
        (
            "VAL4266_7_preserve_prior_adoptions",
            bool(live_em)
            and live_em[0].get("epsilon") == "0.0"
            and bool(live_theta)
            and live_theta[0].get("epsilon") == "0.0"
            and bool(live_matter)
            and live_matter[0].get("epsilon") == "0.0",
            "prior Dq_EM, Dq_theta_marker and Dq_matter adoptions preserved",
        ),
        (
            "VAL4266_8_coeff_not_smuggled_or_later_sourced",
            bool(live_coeff)
            and (live_coeff[0].get("epsilon") != "0.0" or (bool(coeff_adoption) and live_coeff[0].get("source_path") == str(FORMAL_4267_PATH))),
            "Dq_coeff remains live after 4266 unless a later sourced 4267 adoption is present",
        ),
        ("VAL4266_9_claim_row", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4266_10_formal_doc", MARKER in read_text(FORMAL_PATH), "formal marker present"),
        ("VAL4266_11_checkpoint_doc", PACKET_MARKER in read_text(DOC_PATH), "checkpoint marker present"),
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
    source_path = SOURCE_DIR / "P8_Y5_R2FR_4266_SOURCE_REGISTER.csv"
    theorem_path = SOURCE_DIR / "P8_Y5_R2FR_4266_SOURCE_READOUT_THEOREM.csv"
    remainder_path = SOURCE_DIR / "P8_Y5_R2FR_4266_REMAINDER_SPLIT_ROWS.csv"
    adoption_path = SOURCE_DIR / "P8_Y5_R2FR_4266_DQ_SOURCE_READOUT_ADOPTION.csv"
    decision_path = SOURCE_DIR / "P8_Y5_R2FR_4266_DECISION.csv"
    firewall_path = SOURCE_DIR / "P8_Y5_R2FR_4266_CLAIM_FIREWALL.csv"
    status_path = SOURCE_DIR / "P8_Y5_R2FR_4266_STATUS.csv"
    next_path = SOURCE_DIR / "P8_Y5_R2FR_4266_NEXT_TARGET.csv"

    component_candidate = component_candidate_rows()
    write_csv(source_path, source_rows())
    write_csv(theorem_path, source_readout_theorem_rows())
    write_csv(remainder_path, remainder_split_rows())
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
        "remainder": remainder_path,
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
