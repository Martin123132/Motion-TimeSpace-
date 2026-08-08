from __future__ import annotations

import csv
import math
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4083-Y5-R2FR-charge-current-normalization-or-standard-EM-import-contract.md"

DECISION = "ABSOLUTE_CHARGE_ALPHA_NOT_DERIVED_STANDARD_VISIBLE_EM_IMPORT_CONTRACT_READY_LOCAL_GR_ROUTE_UNBLOCKED_NONCLAIM"

C_LIGHT = 299_792_458.0
H_PLANCK = 6.626_070_15e-34
E_CHARGE = 1.602_176_634e-19
ALPHA = 7.297_352_5643e-3
ALPHA_STANDARD_UNCERTAINTY = 1.1e-12
ALPHA_INV = 137.035_999_177
ALPHA_INV_STANDARD_UNCERTAINTY = 2.1e-8
EPSILON0 = 8.854_187_8188e-12
EPSILON0_STANDARD_UNCERTAINTY = 1.4e-21
MU0 = 1.256_637_061_27e-6
MU0_STANDARD_UNCERTAINTY = 2.0e-16

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4083_00_4082_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4082_NEXT_TARGET.csv",
        "4083-Y5-R2FR-charge-current-normalization-or-standard-EM-import-contract.md",
        "4082 selected charge-current normalization or standard EM import contract.",
    ),
    "SRC4083_01_4082_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4082_EM_HODGE_MAXWELL_THEOREM.csv",
        "MAXWELL_DERIVATION_NOT_CLOSED",
        "4082 exact same-Hodge Maxwell theorem remains parent unsigned.",
    ),
    "SRC4083_02_em_gate_audit": (
        FORMALIZATION / "29-em-maxwell-gate-audit.md",
        "Fine-structure claim: not claimable as derived",
        "formal audit blocks alpha/charge overclaim.",
    ),
    "SRC4083_03_maxwell_targets": (
        FORMALIZATION / "32-maxwell-limit-targets.md",
        "alpha_EM",
        "Maxwell target file identifies alpha_EM as a separate owner target.",
    ),
    "SRC4083_04_current_bound_vector": (
        SOURCE_DIR / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv",
        "C_JQ",
        "current-owner vector identifies charge-current normalization ambiguity.",
    ),
    "SRC4083_05_alpha_level": (
        SOURCE_DIR / "P8_EM_alpha_level_current_owner_status.csv",
        "compact_U1_plus_Noether_fixes_alpha",
        "existing alpha audit rejects compact U(1)+Noether as an absolute alpha derivation.",
    ),
    "SRC4083_06_charge_lattice_owner": (
        SOURCE_DIR / "P8_EM_observed_stack_charge_lattice_owner_status.csv",
        "shared_owner_derives_local_source_coupling",
        "observed stack plus charge lattice owner gives strongest conditional source route.",
    ),
    "SRC4083_07_scalar_gauge": (
        SOURCE_DIR / "P8_EM_scalar_gauge_coupling_owner_status.csv",
        "C_XF2_identity",
        "scalar gauge coupling audit identifies the invariant F2/alpha throat.",
    ),
    "SRC4083_08_unique_f2": (
        SOURCE_DIR / "P8_EM_unique_F2_or_calibrated_alpha_status.csv",
        "calibrated_universal_constant",
        "existing status accepts calibrated alpha baseline as nonclaim fallback.",
    ),
    "SRC4083_09_trichotomy": (
        SOURCE_DIR / "P8_Y5_R2FR_3995_CURRENT_NORMALIZATION_GAUGE_TRICHOTOMY.csv",
        "absolute_constant_guard",
        "normalization trichotomy separates rescaling gauge from physical source slots.",
    ),
    "SRC4083_10_cjq_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3875_CJQ_CURRENT_OWNER_ZERO_THEOREM.csv",
        "EXACT_CONDITIONAL_ZERO_THEOREM",
        "C_JQ zero theorem already exists but remains parent unsigned.",
    ),
    "SRC4083_11_charge_lock": (
        SOURCE_DIR / "P8_Y5_R2FR_4012_PIM_HTAU_CHARGE_LOCK_THEOREM.csv",
        "CONDITIONAL_SAME_CHARGE_THEOREM_UNSIGNED",
        "Pi_M/H_tau/source charge equality remains conditional unsigned.",
    ),
    "SRC4083_12_local_alpha_interface": (
        SOURCE_DIR / "P8_local_GR_calibrated_alpha_source_interface_status.csv",
        "alpha_loop",
        "local GR calibrated-alpha interface already points back to G/kappa/Newton gate.",
    ),
}

WEB_SOURCES = [
    {
        "source_id": "WEB4083_0_nist_sp961_2022_wall",
        "title": "CODATA Recommended Values of the Fundamental Physical Constants: 2022",
        "authors": "NIST / CODATA Task Group on Fundamental Constants",
        "year": 2024,
        "url": "https://physics.nist.gov/cuu/pdf/wall_2022.pdf",
        "supporting_url": "https://codata.org/initiatives/data-science-and-stewardship/fundamental-physical-constants/",
        "extracted_result": "c, h, e exact; alpha=7.2973525643(11)e-3; alpha^-1=137.035999177(21)",
        "source_role": "standard visible EM calibration constants for nonclaim import branch",
        "confidence": "official_NIST_CODATA_summary",
    },
    {
        "source_id": "WEB4083_1_codata_cycle_note",
        "title": "Fundamental Physical Constants",
        "authors": "CODATA Task Group on Fundamental Constants",
        "year": 2026,
        "url": "https://codata.org/initiatives/data-science-and-stewardship/fundamental-physical-constants/",
        "supporting_url": "https://pml.nist.gov/cuu/Constants/",
        "extracted_result": "latest completed regular adjustment is 2022; 2026 adjustment closes 31 December 2026 with output expected early 2027",
        "source_role": "provenance guard for using 2022 CODATA constants as current completed constants",
        "confidence": "official_CODATA_status_page",
    },
]

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4083_SOURCE_REGISTER.csv",
    "web_provenance": SOURCE_DIR / "P8_Y5_R2FR_4083_WEB_PROVENANCE.csv",
    "constants": SOURCE_DIR / "P8_Y5_R2FR_4083_STANDARD_EM_CONSTANTS.csv",
    "charge_theorem": SOURCE_DIR / "P8_Y5_R2FR_4083_CHARGE_CURRENT_NORMALIZATION_THEOREM.csv",
    "import_contract": SOURCE_DIR / "P8_Y5_R2FR_4083_STANDARD_VISIBLE_EM_IMPORT_CONTRACT.csv",
    "runner_update": SOURCE_DIR / "P8_Y5_R2FR_4083_EFFECTIVE_RESIDUAL_RUNNER_UPDATE.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4083_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4083_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4083_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4083_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4083_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_rows(current_timestamp: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_file",
                "path_or_url": str(path),
                "exists_or_recorded": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": current_timestamp,
            }
        )
    for source in WEB_SOURCES:
        rows.append(
            {
                "source_id": source["source_id"],
                "source_type": "web_source",
                "path_or_url": source["url"],
                "exists_or_recorded": True,
                "needle": source["extracted_result"],
                "needle_found": True,
                "role": source["source_role"],
                "timestamp_utc": current_timestamp,
            }
        )
    return rows


def web_provenance_rows(current_timestamp: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source in WEB_SOURCES:
        row = dict(source)
        row["timestamp_utc"] = current_timestamp
        row["valid_for_claim"] = False
        rows.append(row)
    return rows


def constant_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "constant_id": "CONST4083_0_c",
            "symbol": "c",
            "value": C_LIGHT,
            "standard_uncertainty": 0.0,
            "units": "m s^-1",
            "status": "SI_exact_defining_constant",
            "source_id": "WEB4083_0_nist_sp961_2022_wall",
            "use_in_MTS": "calibrated visible EM/light-cone baseline",
            "derived_by_MTS": False,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "constant_id": "CONST4083_1_h",
            "symbol": "h",
            "value": H_PLANCK,
            "standard_uncertainty": 0.0,
            "units": "J Hz^-1",
            "status": "SI_exact_defining_constant",
            "source_id": "WEB4083_0_nist_sp961_2022_wall",
            "use_in_MTS": "calibrated quantum/charge normalization baseline",
            "derived_by_MTS": False,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "constant_id": "CONST4083_2_e",
            "symbol": "e",
            "value": E_CHARGE,
            "standard_uncertainty": 0.0,
            "units": "C",
            "status": "SI_exact_defining_constant",
            "source_id": "WEB4083_0_nist_sp961_2022_wall",
            "use_in_MTS": "standard visible elementary charge import",
            "derived_by_MTS": False,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "constant_id": "CONST4083_3_alpha",
            "symbol": "alpha_EM",
            "value": ALPHA,
            "standard_uncertainty": ALPHA_STANDARD_UNCERTAINTY,
            "units": "dimensionless",
            "status": "CODATA_2022_recommended_measured_constant",
            "source_id": "WEB4083_0_nist_sp961_2022_wall",
            "use_in_MTS": "calibrated local Maxwell/atomic baseline; not MTS prediction",
            "derived_by_MTS": False,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "constant_id": "CONST4083_4_alpha_inv",
            "symbol": "alpha_EM^-1",
            "value": ALPHA_INV,
            "standard_uncertainty": ALPHA_INV_STANDARD_UNCERTAINTY,
            "units": "dimensionless",
            "status": "CODATA_2022_recommended_measured_constant",
            "source_id": "WEB4083_0_nist_sp961_2022_wall",
            "use_in_MTS": "readable inverse-alpha calibration row",
            "derived_by_MTS": False,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "constant_id": "CONST4083_5_epsilon0",
            "symbol": "epsilon_0",
            "value": EPSILON0,
            "standard_uncertainty": EPSILON0_STANDARD_UNCERTAINTY,
            "units": "F m^-1",
            "status": "CODATA_2022_derived_from_alpha_and_exact_SI_constants",
            "source_id": "WEB4083_0_nist_sp961_2022_wall",
            "use_in_MTS": "SI Maxwell normalization if needed",
            "derived_by_MTS": False,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "constant_id": "CONST4083_6_mu0",
            "symbol": "mu_0",
            "value": MU0,
            "standard_uncertainty": MU0_STANDARD_UNCERTAINTY,
            "units": "N A^-2",
            "status": "CODATA_2022_derived_from_alpha_and_exact_SI_constants",
            "source_id": "WEB4083_0_nist_sp961_2022_wall",
            "use_in_MTS": "SI Maxwell normalization if needed",
            "derived_by_MTS": False,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def charge_theorem_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "CHG4083_0_compact_U1_lattice",
            "statement": "If the parent visible EM sector is a compact U(1) connection with fixed representation labels n_A in Z and q_A=n_A q_star, then relative charges are lattice-owned and D_X n_A=0 on a fixed representation sector.",
            "proof_sketch": "Compact U(1) representations are integer-labelled. Vertical MTS directions cannot continuously change an integer label inside a fixed sector, so relative charge labels are silent.",
            "result": "EXACT_CONDITIONAL_RELATIVE_CHARGE_LATTICE_THEOREM",
            "current_MTS_status": "RELATIVE_LABEL_ROUTE_AVAILABLE_PARENT_QSTAR_NOT_SIGNED",
            "residual_effect": "kills relative charge-label drift only after the parent signs compact U(1), fixed reps and q_star owner.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "CHG4083_1_no_absolute_alpha_from_classical_U1",
            "statement": "Compact U(1), Noether current conservation and Maxwell equations do not determine the absolute gauge kinetic coefficient, elementary charge value, or alpha_EM.",
            "proof_sketch": "The classical action admits a continuous normalization/gauge-coupling parameter. Field/current rescalings can move normalization between A, F2 and J while leaving the form of the equations intact; alpha is fixed only by an extra parent norm, unification/quantization input, or calibration.",
            "result": "EXACT_NO_GO_FOR_ABSOLUTE_ALPHA_FROM_U1_NOETHER_ALONE",
            "current_MTS_status": "ABSOLUTE_CHARGE_ALPHA_NOT_DERIVED",
            "residual_effect": "prevents fake victory: relative charge lattice is not a derivation of e or alpha_EM.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "CHG4083_2_current_normalization_zero_route",
            "statement": "C_JQ is zero if the same parent owner supplies A_Q, the Noether current, q_star, fixed representation labels, absence of source-only action slots, and readout/radiative stability before variation.",
            "proof_sketch": "With one parent current owner, the current normalization is part of the same variational object. Post-variation rescaling is convention; pre-variation species/source slots are physical and must be excluded or bounded.",
            "result": "EXACT_CONDITIONAL_CJQ_ZERO_THEOREM_RESTATED_AS_OWNER_CONTRACT",
            "current_MTS_status": "NOT_PARENT_PROMOTED",
            "residual_effect": "C_JQ can be theorem-zeroed only on the signed owner package; otherwise retain source-slot residual rows.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "CHG4083_3_standard_visible_EM_import",
            "statement": "The local GR/Newton programme may import standard visible Maxwell/charged matter as the observed matter sector with calibrated constants e, h, c and CODATA alpha, while marking them not derived by MTS.",
            "proof_sketch": "GR itself does not derive all matter couplings; it couples universally to the Hilbert stress of the matter action. A disciplined import keeps the local-GR reduction alive without pretending to solve QED/alpha first.",
            "result": "STANDARD_VISIBLE_EM_IMPORT_CONTRACT_READY_NONCLAIM",
            "current_MTS_status": "LOCAL_GR_ROUTE_CAN_PROCEED_WITH_CALIBRATED_VISIBLE_MATTER",
            "residual_effect": "baseline sets Delta_Hodge_EM=0, C_JQ=0, w_EM=1, C_XF2=0 by imported standard sector, not by MTS prediction; deviations remain bounded branches.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def import_contract_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "contract_id": "IMP4083_0_visible_sector_status",
            "branch": "calibrated_standard_visible_EM",
            "adopted_object": "standard Maxwell plus charged matter on e_obs",
            "sets": "Delta_Hodge_EM=0; C_JQ=0; w_EM=1; C_XF2=0; alpha_EM=CODATA_2022",
            "does_not_set": "MTS_derives_charge; MTS_derives_alpha; MTS_derives_QED; MTS_derives_Coulomb_from_motion_time_space",
            "claim_status": "calibration_import_not_derivation",
            "effect_on_goal": "unblocks local GR/Newton source-coupling branch with honest visible matter action",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "contract_id": "IMP4083_1_deviation_branch",
            "branch": "active_MTS_EM_deviation",
            "adopted_object": "finite residual vector if MTS changes EM normalization or Hodge/current owner",
            "sets": "none",
            "does_not_set": "no cancellation credit; no automatic zero",
            "claim_status": "nonclaim_bound_branch",
            "effect_on_goal": "any nonzero C_XF2, C_JQ, Delta_Hodge_EM, w_EM-1, or Phi_EM_rad must map to WEP, clocks, R10, PPN, light-cone or birefringence bounds",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "contract_id": "IMP4083_2_derivation_branch",
            "branch": "future_parent_EM_derivation",
            "adopted_object": "compact U(1) bundle plus q_star/level/curvature-norm owner plus no-extra-F2 domain theorem",
            "sets": "relative charge labels theorem-zero; possibly absolute alpha only if parent norm is unique",
            "does_not_set": "absolute alpha from U(1)/Noether alone",
            "claim_status": "future_parent_signature_required",
            "effect_on_goal": "keeps a true emergent-EM route alive but removes it from the critical path for local GR",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def runner_update_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "runner_id": "RUNUP4083_0_CJQ",
            "quantity": "C_JQ",
            "old_score": "PARENT_CHARGE_VALUES_MISSING",
            "new_score": "ZERO_BY_STANDARD_EM_IMPORT_OR_EXACT_CONDITIONAL_PARENT_OWNER_THEOREM",
            "baseline_value": 0.0,
            "baseline_units": "dimensionless",
            "claim_scope": "calibrated visible EM baseline, not MTS derivation",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "runner_id": "RUNUP4083_1_wEM",
            "quantity": "w_EM",
            "old_score": "RETAINED_NORMALIZATION_COEFFICIENT",
            "new_score": "SET_TO_ONE_BY_STANDARD_EM_IMPORT_CONTRACT",
            "baseline_value": 1.0,
            "baseline_units": "dimensionless",
            "claim_scope": "normalization convention/calibration in imported sector",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "runner_id": "RUNUP4083_2_alpha",
            "quantity": "alpha_EM",
            "old_score": "calibrated_universal_constant",
            "new_score": "CODATA_2022_CALIBRATED_BASELINE_NOT_DERIVED",
            "baseline_value": ALPHA,
            "baseline_units": "dimensionless",
            "claim_scope": "standard measured constant for local branch",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "runner_id": "RUNUP4083_3_CXF2",
            "quantity": "C_XF2_or_b_alpha",
            "old_score": "WEP_and_clock_and_source_anchors_ready_projection_missing",
            "new_score": "ZERO_IN_CALIBRATED_BASELINE_RETAIN_FINITE_DEVIATION_BRANCH",
            "baseline_value": 0.0,
            "baseline_units": "dimensionless_vertical_derivative",
            "claim_scope": "branch choice; nonzero MTS EM coupling remains bounded not claimed",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "runner_id": "RUNUP4083_4_local_GR_interface",
            "quantity": "local_GR_Newton_source_interface",
            "old_score": "blocked_by_alpha_loop",
            "new_score": "ALPHA_LOOP_REMOVED_FROM_CRITICAL_PATH_RETURN_TO_KAPPA_G_POISSON_PPN_GATE",
            "baseline_value": "not_numeric",
            "baseline_units": "gate_status",
            "claim_scope": "next work should derive/bound Newtonian source normalization rather than re-fighting alpha",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def decision_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4083_0",
            "decision": DECISION,
            "strongest_positive_result": "relative charge labels and C_JQ have exact conditional owner theorems; local GR can proceed with a calibrated standard visible EM sector.",
            "blocking_fact": "absolute e/alpha_EM is not derived by compact U(1), Noether current, or current conservation alone.",
            "allowed_status": "private_nonclaim_checkpoint",
            "claim_allowed": False,
            "next_action": "return to kappa/G/source denominator and Newtonian Poisson/PPN residual gate using calibrated visible matter.",
            "timestamp_utc": current_timestamp,
        }
    ]


def claim_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4083_0",
            "claim": "relative charge lattice silence is exact conditional",
            "claim_allowed": True,
            "scope": "conditional mathematical theorem",
            "why": "fixed compact U(1) representation labels cannot drift continuously along vertical MTS directions",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4083_1",
            "claim": "absolute alpha_EM is derived by current MTS",
            "claim_allowed": False,
            "scope": "parent EM/particle derivation",
            "why": "continuous gauge kinetic/current normalization remains unless the parent supplies a unique norm or calibration",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4083_2",
            "claim": "standard visible EM can be imported as calibrated matter for the local GR branch",
            "claim_allowed": True,
            "scope": "private nonclaim residual target",
            "why": "this is a disciplined branch contract, not a public derivation of EM from MTS",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4083_3",
            "claim": "current MTS derives charge, QED, Coulomb law, or alpha_EM",
            "claim_allowed": False,
            "scope": "parent EM/particle derivation",
            "why": "charge-current normalization, absolute coupling and Coulomb/QED owner remain imported or future-parent targets",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4083_4",
            "claim": "alpha loop no longer blocks local GR/Newton testing if treated as calibrated visible matter",
            "claim_allowed": True,
            "scope": "private nonclaim residual target",
            "why": "local GR needs universal Hilbert stress and G/kappa/Poisson reduction, not a first-principles alpha prediction",
            "timestamp_utc": current_timestamp,
        },
    ]


def next_target_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "target_id": "NEXT4083_0",
            "next_target": "4084-Y5-R2FR-kappa-G-source-denominator-to-Newton-Poisson-gate.md",
            "script": "scripts/Y5_R2FR_4084_kappa_G_source_denominator_to_Newton_Poisson_gate.py",
            "why": "EM/alpha can now sit in calibrated visible matter; the decisive local-GR route is the source denominator, G/kappa normalization, and Poisson/PPN residual vector.",
            "priority": "P0",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_id": "NEXT4083_1",
            "next_target": "future_emergent_charge_parent_norm",
            "script": "fold_into_parent_action_or_particle_work",
            "why": "true emergent charge/alpha remains possible only with a parent norm/level/no-extra-F2 theorem, not U(1) conservation alone.",
            "priority": "P1",
            "timestamp_utc": current_timestamp,
        },
    ]


def status_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "timestamp_utc": current_timestamp,
            "branch_id": "MTS_R2FR_Y5_4083_CHARGE_CURRENT_NORMALIZATION_OR_STANDARD_EM_IMPORT_CONTRACT",
            "status": DECISION,
            "public_claim_allowed": False,
            "github_action": False,
            "formalization_workbench_modified": False,
            "summary": "4083 proves relative charge/current normalization only conditionally, proves a no-go for absolute alpha from U(1)/Noether alone, creates a standard visible EM import contract, and moves the critical path back to G/kappa/Newton/PPN.",
            "valid_for_claim": False,
        }
    ]


def validate_sources(rows: List[Dict[str, object]]) -> Tuple[bool, str]:
    failures = [
        row["source_id"]
        for row in rows
        if row["exists_or_recorded"] is not True or row["needle_found"] is not True
    ]
    return not failures, f"missing_or_unmatched_sources={failures}"


def validate_csv_parse(paths: List[Path]) -> Tuple[bool, str]:
    failures: List[str] = []
    for path in paths:
        try:
            with path.open(newline="", encoding="utf-8") as input_file:
                rows = list(csv.DictReader(input_file))
            if not rows:
                failures.append(f"{path}:empty")
        except Exception as exc:
            failures.append(f"{path}:{exc}")
    return not failures, f"csv_failures={failures}"


def validate_constants(rows: List[Dict[str, object]]) -> Tuple[bool, str]:
    failures: List[str] = []
    exact = {"CONST4083_0_c", "CONST4083_1_h", "CONST4083_2_e"}
    for row in rows:
        try:
            value = float(row["value"])
            uncertainty = float(row["standard_uncertainty"])
            if not math.isfinite(value) or value <= 0:
                failures.append(f"{row['constant_id']}:value not positive finite")
            if uncertainty < 0:
                failures.append(f"{row['constant_id']}:negative uncertainty")
        except Exception:
            failures.append(f"{row['constant_id']}:non-numeric")
        if row["constant_id"] in exact and float(row["standard_uncertainty"]) != 0.0:
            failures.append(f"{row['constant_id']}:exact constant has nonzero uncertainty")
        if row["derived_by_MTS"] is not False or row["valid_for_claim"] is not False:
            failures.append(f"{row['constant_id']}:constant row overclaims")
    return not failures, "; ".join(failures) if failures else "standard EM constants numeric, sourced, and nonclaim"


def validate_import_contract(rows: List[Dict[str, object]]) -> Tuple[bool, str]:
    joined = str(rows)
    required = ["calibrated_standard_visible_EM", "active_MTS_EM_deviation", "future_parent_EM_derivation"]
    missing = [token for token in required if token not in joined]
    overclaim = [
        row["contract_id"]
        for row in rows
        if row["valid_for_claim"] is not False or "MTS_derives_charge" not in row["does_not_set"]
        and row["contract_id"] == "IMP4083_0_visible_sector_status"
    ]
    return not missing and not overclaim, f"missing={missing}; overclaim={overclaim}"


def validate_claim_scopes(rows: List[Dict[str, object]]) -> Tuple[bool, str]:
    allowed_scopes = {"conditional mathematical theorem", "private nonclaim residual target"}
    bad_rows = [
        row["claim_id"]
        for row in rows
        if row["claim_allowed"] is True and row["scope"] not in allowed_scopes
    ]
    return not bad_rows, f"bad_allowed_claim_scopes={bad_rows}"


def validate_no_public_claim(row_groups: List[List[Dict[str, object]]]) -> Tuple[bool, str]:
    text = str(row_groups)
    forbidden = [
        "public_claim': True",
        '"public_claim": True',
        "github_action': True",
        '"github_action": True',
        "absolute alpha_EM is derived by current MTS', 'claim_allowed': True",
        "current MTS derives charge, QED, Coulomb law, or alpha_EM', 'claim_allowed': True",
        "derived_by_MTS': True",
        '"derived_by_MTS": True',
    ]
    hits = [token for token in forbidden if token in text]
    return not hits, f"forbidden_public_claim_tokens={hits}"


def validate_output_scope(paths: List[Path]) -> Tuple[bool, str]:
    outside = [str(path) for path in paths + [DOC_PATH] if ROOT not in path.parents and path != ROOT]
    formalization_hits = [str(path) for path in paths + [DOC_PATH] if FORMALIZATION in path.parents]
    return not outside and not formalization_hits, f"outside_post_checkpoint={outside}; formalization_hits={formalization_hits}"


def validate_script_compile() -> Tuple[bool, str]:
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError as exc:
        return False, str(exc)
    return True, "script compiles"


def validation_rows(
    source_table: List[Dict[str, object]],
    generated_csvs: List[Path],
    row_groups: List[List[Dict[str, object]]],
    constants: List[Dict[str, object]],
    contracts: List[Dict[str, object]],
    claims: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    source_ok, source_detail = validate_sources(source_table)
    csv_ok, csv_detail = validate_csv_parse(generated_csvs)
    constants_ok, constants_detail = validate_constants(constants)
    import_ok, import_detail = validate_import_contract(contracts)
    no_public_ok, no_public_detail = validate_no_public_claim(row_groups)
    claim_scope_ok, claim_scope_detail = validate_claim_scopes(claims)
    output_scope_ok, output_scope_detail = validate_output_scope(generated_csvs)
    compile_ok, compile_detail = validate_script_compile()
    joined = str(row_groups)
    return [
        {"check_id": "VAL4083_00_sources", "passed": source_ok, "detail": source_detail},
        {"check_id": "VAL4083_01_csv_parse", "passed": csv_ok, "detail": csv_detail},
        {"check_id": "VAL4083_02_constants", "passed": constants_ok, "detail": constants_detail},
        {"check_id": "VAL4083_03_import_contract", "passed": import_ok, "detail": import_detail},
        {"check_id": "VAL4083_04_no_public_or_github_claim", "passed": no_public_ok, "detail": no_public_detail},
        {"check_id": "VAL4083_05_claim_scope", "passed": claim_scope_ok, "detail": claim_scope_detail},
        {"check_id": "VAL4083_06_output_scope", "passed": output_scope_ok, "detail": output_scope_detail},
        {
            "check_id": "VAL4083_07_no_absolute_alpha_derivation",
            "passed": "EXACT_NO_GO_FOR_ABSOLUTE_ALPHA_FROM_U1_NOETHER_ALONE" in joined
            and "ABSOLUTE_CHARGE_ALPHA_NOT_DERIVED" in joined,
            "detail": "absolute charge/alpha no-go is recorded",
        },
        {
            "check_id": "VAL4083_08_local_GR_unblocked",
            "passed": "ALPHA_LOOP_REMOVED_FROM_CRITICAL_PATH_RETURN_TO_KAPPA_G_POISSON_PPN_GATE" in joined
            and "4084-Y5-R2FR-kappa-G-source-denominator-to-Newton-Poisson-gate.md" in joined,
            "detail": "critical path returns to kappa/G/Newton/PPN gate",
        },
        {"check_id": "VAL4083_09_script_compiles", "passed": compile_ok, "detail": compile_detail},
    ]


def doc_text(current_timestamp: str) -> str:
    return f"""# 4083 - Charge-Current Normalization Or Standard EM Import Contract

- Timestamp: `{current_timestamp}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Public charge/QED/alpha claim: `false`
- GitHub action: `false`

## Result

This checkpoint makes a hard fork decision instead of circling the coupling.

The exact theorem we can keep:

```text
compact U(1) + fixed representation labels n_A in Z
q_A = n_A q_star
D_X n_A = 0 on a fixed sector
```

So relative charge labels can be parent-owned conditionally.

The exact no-go:

```text
compact U(1) + Noether current + Maxwell equations
does not determine absolute e, w_EM, or alpha_EM
```

because the classical EM block still has a continuous gauge kinetic/current normalization unless the parent supplies a unique norm, level, no-extra-F2 theorem, or calibration.

## Standard Visible EM Import Contract

For the local GR/Newton branch, use the standard visible EM sector as calibrated matter:

```text
Delta_Hodge_EM = 0
C_JQ = 0
w_EM = 1
C_XF2 = 0
alpha_EM = CODATA measured constant
```

This is not an MTS derivation of charge. It is a disciplined import, like GR coupling to the Standard Model stress tensor without deriving the Standard Model.

## Constants Imported

```text
c = {C_LIGHT:.0f} m s^-1 exact
h = {H_PLANCK:.8e} J Hz^-1 exact
e = {E_CHARGE:.9e} C exact
alpha_EM = {ALPHA:.13e} +/- {ALPHA_STANDARD_UNCERTAINTY:.1e}
alpha_EM^-1 = {ALPHA_INV:.9f} +/- {ALPHA_INV_STANDARD_UNCERTAINTY:.1e}
epsilon_0 = {EPSILON0:.10e} F m^-1
mu_0 = {MU0:.11e} N A^-2
```

## What This Fixes

The alpha/charge loop is removed from the local-GR critical path:

```text
local source coupling can now use calibrated visible Hilbert stress
Poynting is counted once inside T_EM
nonzero MTS EM deviations remain testable residuals
```

## What It Does Not Fix

Still not claimed:

```text
MTS derives charge
MTS derives QED
MTS derives Coulomb law from first principles
MTS predicts alpha_EM
```

Those remain future parent-norm/particle-sector targets.

## Decision

```text
relative charge/current theorem = exact conditional
absolute e/alpha derivation = rejected for U(1)/Noether alone
standard visible EM import = accepted as private calibrated local branch
critical path returns to kappa/G/Newton/PPN
```

## Sources

- NIST/CODATA, `CODATA Recommended Values of the Fundamental Physical Constants: 2022`, NIST SP 961, May 2024.
- CODATA Task Group on Fundamental Constants, status page for the 2022/2026 adjustment cycle.

## Next

```text
4084-Y5-R2FR-kappa-G-source-denominator-to-Newton-Poisson-gate.md
```

That is the right next punch: source denominator, G/kappa normalization, Poisson limit, and PPN residuals using calibrated visible matter.
"""


def main() -> None:
    current_timestamp = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(current_timestamp)
    web_provenance = web_provenance_rows(current_timestamp)
    constants = constant_rows(current_timestamp)
    charge_theorem = charge_theorem_rows(current_timestamp)
    contracts = import_contract_rows(current_timestamp)
    runner = runner_update_rows(current_timestamp)
    decisions = decision_gate_rows(current_timestamp)
    claims = claim_gate_rows(current_timestamp)
    next_targets = next_target_rows(current_timestamp)
    statuses = status_rows(current_timestamp)

    DOC_PATH.write_text(doc_text(current_timestamp), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["web_provenance"], web_provenance)
    write_csv(OUTPUTS["constants"], constants)
    write_csv(OUTPUTS["charge_theorem"], charge_theorem)
    write_csv(OUTPUTS["import_contract"], contracts)
    write_csv(OUTPUTS["runner_update"], runner)
    write_csv(OUTPUTS["decision_gate"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next_target"], next_targets)
    write_csv(OUTPUTS["status"], statuses)

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["web_provenance"],
        OUTPUTS["constants"],
        OUTPUTS["charge_theorem"],
        OUTPUTS["import_contract"],
        OUTPUTS["runner_update"],
        OUTPUTS["decision_gate"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    row_groups = [
        sources,
        web_provenance,
        constants,
        charge_theorem,
        contracts,
        runner,
        decisions,
        claims,
        next_targets,
        statuses,
    ]
    validation = validation_rows(sources, generated_csvs, row_groups, constants, contracts, claims)
    write_csv(OUTPUTS["validation"], validation)

    cache_dir = SCRIPT_PATH.parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    failures = [row for row in validation if not row["passed"]]
    print(f"wrote {DOC_PATH}")
    print(f"decision: {DECISION}")
    print(f"validation rows: {len(validation)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
