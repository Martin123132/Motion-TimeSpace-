from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import os
import time
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5036 = POST / "scripts" / "Y5_R2FR_5036_paired_full_vector_ladder.py"
SCRIPT_5043 = POST / "scripts" / "Y5_R2FR_5043_theorem_first_coarse_E040_multilevel_gate.py"
SCRIPT_5045 = POST / "scripts" / "Y5_R2FR_5045_theorem_scope_falsification_and_quarantine.py"
SCRIPT_5069 = POST / "scripts" / "Y5_R2FR_5069_signed_segment_winding_composition_law.py"
SCRIPT_5084 = POST / "scripts" / "Y5_R2FR_5084_recoil_source_local_cauchy_theorem.py"
SCRIPT_5085 = POST / "scripts" / "Y5_R2FR_5085_same_source_global_collision_removable_extension.py"
SCRIPT_5086 = POST / "scripts" / "Y5_R2FR_5086_outward_same_source_residue_contour_gate.py"
SCRIPT_5088 = POST / "scripts" / "Y5_R2FR_5088_exact_same_source_double_zero_collision_certificate.py"
SCRIPT_5091 = POST / "scripts" / "Y5_R2FR_5091_E040_A11_coarse_multi_double_zero_certificate.py"
SCRIPT_5095 = POST / "scripts" / "Y5_R2FR_5095_same_side_global_cluster_cycle_certificate.py"
SCRIPT_5097 = POST / "scripts" / "Y5_R2FR_5097_E040_S507622_A00_projective_cross_source_cluster_zero.py"
SCRIPT_5099 = POST / "scripts" / "Y5_R2FR_5099_E040_S507622_A10_continuous_subminimum_cycle_certificate.py"
SCRIPT_5101 = POST / "scripts" / "Y5_R2FR_5101_S507622_projective_cluster_argument_independence.py"
SCRIPT_5112 = POST / "scripts" / "Y5_R2FR_5112_recoil_holomorphy_scope_correction.py"
SCRIPT_5113 = POST / "scripts" / "Y5_R2FR_5113_S507614_A00_event_local_recoil_resolution.py"
SCRIPT_5114 = POST / "scripts" / "Y5_R2FR_5114_on_demand_direct_residue_classifier.py"
SCRIPT_5115 = POST / "scripts" / "Y5_R2FR_5115_general_on_demand_owned_direct_residue_classifier.py"
SCRIPT_5117 = POST / "scripts" / "Y5_R2FR_5117_E020_S507615_A14_same_side_cluster_cycle_certificate.py"
SCRIPT_5119 = POST / "scripts" / "Y5_R2FR_5119_S507622_E020_projective_cluster_argument_independence.py"
MANIFEST = POST / "source-intake" / "functional_rg" / "5076" / "locked_central_anchor_pilot_manifest.json"
SOURCE = POST / "source-intake" / "functional_rg" / "5077"
RUNS = SOURCE / "runs"
DRY_RUN_JSON = SOURCE / "central_anchor_pilot_dry_run.json"
RESULT_JSON = SOURCE / "central_anchor_pilot_runner_gate.json"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5077_VALIDATION.csv"
LOCAL_ZERO_CERTIFICATE = POST / "source-intake" / "functional_rg" / "5083" / "owned_g2_local_cauchy_zero_certificate.json"
RECOIL_THEOREM_GATE = POST / "source-intake" / "functional_rg" / "5084" / "recoil_source_local_cauchy_theorem.json"
RECOIL_SCOPE_CORRECTION_GATE = POST / "source-intake" / "functional_rg" / "5112" / "recoil_holomorphy_scope_correction.json"
RECOIL_ZERO_REGISTRY_V1 = POST / "source-intake" / "functional_rg" / "5112" / "event_local_direct_zero_registry.json"
RECOIL_ZERO_REGISTRY_V2_GATE = POST / "source-intake" / "functional_rg" / "5113" / "S507614_A00_event_local_recoil_resolution.json"
RECOIL_ZERO_REGISTRY_V2 = POST / "source-intake" / "functional_rg" / "5113" / "event_local_direct_zero_registry_v2.json"
RECOIL_ZERO_REGISTRY_GATE = POST / "source-intake" / "functional_rg" / "5114" / "on_demand_direct_residue_classifier_gate.json"
RECOIL_ZERO_REGISTRY = POST / "source-intake" / "functional_rg" / "5114" / "event_local_direct_zero_registry_v3.json"
GENERAL_DIRECT_CLASSIFIER_GATE = POST / "source-intake" / "functional_rg" / "5115" / "general_on_demand_owned_direct_classifier_gate.json"
REMOVABLE_EXTENSION_GATE = POST / "source-intake" / "functional_rg" / "5085" / "same_source_global_collision_removable_extension.json"
OUTWARD_CONTOUR_GATE = POST / "source-intake" / "functional_rg" / "5086" / "outward_same_source_residue_contour_gate.json"
DOUBLE_ZERO_COLLISION_GATE = POST / "source-intake" / "functional_rg" / "5088" / "exact_same_source_double_zero_collision_certificate.json"
MULTI_DOUBLE_ZERO_COLLISION_GATE = POST / "source-intake" / "functional_rg" / "5091" / "E040_A11_coarse_multi_double_zero_certificate.json"
SAME_SIDE_CLUSTER_CYCLE_GATE = POST / "source-intake" / "functional_rg" / "5095" / "same_side_global_cluster_cycle_certificate.json"
SAME_SIDE_CLUSTER_E020_GATE = POST / "source-intake" / "functional_rg" / "5117" / "E020_S507615_A14_same_side_cluster_cycle_certificate.json"
PROJECTIVE_CLUSTER_ZERO_GATE = POST / "source-intake" / "functional_rg" / "5097" / "E040_S507622_A00_projective_cross_source_cluster_zero.json"
CONTINUOUS_SUBMINIMUM_CYCLE_GATE = POST / "source-intake" / "functional_rg" / "5099" / "E040_S507622_A10_continuous_subminimum_cycle_certificate.json"
ARGUMENT_INDEPENDENT_PROJECTIVE_GATE = POST / "source-intake" / "functional_rg" / "5101" / "S507622_projective_cluster_argument_independence.json"
E020_PROJECTIVE_CLUSTER_GATE = POST / "source-intake" / "functional_rg" / "5119" / "S507622_E020_projective_cluster_argument_independence.json"
MARKER = "MTS_5077_CENTRAL_ANCHOR_PILOT_RUNNER"
REVISION = "event-local-recoil-zero-registry-runner-v14"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
ANCHOR_ID = "A08"
SMOKE_BASE_IDS = ("A08", "A09")
DOUBLE_ZERO_JOB_KEY = "E020__S507603_N0000__A07__primary24"
MULTI_DOUBLE_ZERO_JOB_KEY = "E040__S507603_N0000__A11__coarse12"
SAME_SIDE_CLUSTER_JOB_KEY = "E040__S507615_N0000__A14__coarse12"
SAME_SIDE_CLUSTER_E020_JOB_KEY = "E020__S507615_N0000__A14__primary24"
PROJECTIVE_CLUSTER_ZERO_JOB_KEY = "E040__S507622_N0000__A00__coarse12"
CONTINUOUS_SUBMINIMUM_CYCLE_JOB_KEY = "E040__S507622_N0000__A10__coarse12"
ARGUMENT_INDEPENDENT_PROJECTIVE_JOB_KEY = "E040__S507622_N0000__A14__coarse12"
E020_PROJECTIVE_CLUSTER_JOB_KEYS = tuple(
    f"E020__S507622_N0000__A{index:02d}__primary24" for index in range(15)
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5036 = load_module("mts_5036_for_5077", SCRIPT_5036)
M5043 = load_module("mts_5043_for_5077", SCRIPT_5043)
M5045 = load_module("mts_5045_for_5077", SCRIPT_5045)
M5069 = load_module("mts_5069_for_5077", SCRIPT_5069)
M5085 = load_module("mts_5085_for_5077", SCRIPT_5085)
M5086 = load_module("mts_5086_for_5077", SCRIPT_5086)
M5088 = load_module("mts_5088_for_5077", SCRIPT_5088)
M5091 = load_module("mts_5091_for_5077", SCRIPT_5091)
M5095 = load_module("mts_5095_for_5077", SCRIPT_5095)
M5097 = load_module("mts_5097_for_5077", SCRIPT_5097)
M5099 = load_module("mts_5099_for_5077", SCRIPT_5099)
M5101 = load_module("mts_5101_for_5077", SCRIPT_5101)
M5115 = load_module("mts_5115_for_5077", SCRIPT_5115)
ORIGINAL_OBTAIN_TOPOLOGY = M5036.M5035.M5034.obtain_topology
ARGUMENT_CERTIFICATE_STEP_LEVELS = (
    *tuple(M5069.FEYNMAN_STEP_LEVELS),
    2048,
)
LOCAL_RESIDUE_RESOLUTION_AUDIT: list[dict[str, Any]] = []
OUTWARD_CONTOUR_AUDIT: list[dict[str, Any]] = []
PROJECTIVE_CLUSTER_ZERO_AUDIT: list[dict[str, Any]] = []
CURRENT_EVENT: dict[str, Any] | None = None
CURRENT_ARGUMENT: dict[str, Any] | None = None


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def install_history_invariant_breakpoints(module: Any) -> None:
    original = module.collision_scaled_breakpoints
    if getattr(original, "_mts_history_invariant", False):
        return

    def near_path_breakpoints(
        start: complex, end: complex, catalog: list[dict[str, Any]]
    ) -> list[float]:
        return original(
            start,
            end,
            [row for row in catalog if bool(row["near_path"])],
        )

    near_path_breakpoints._mts_history_invariant = True
    module.collision_scaled_breakpoints = near_path_breakpoints


def local_zero_certificate() -> dict[str, Any]:
    if not LOCAL_ZERO_CERTIFICATE.exists():
        raise FileNotFoundError(LOCAL_ZERO_CERTIFICATE)
    certificate = json.loads(LOCAL_ZERO_CERTIFICATE.read_text(encoding="utf-8"))
    witness = Path(certificate["arbitrary_precision_witness"])
    if not witness.exists():
        raise FileNotFoundError(witness)
    if M5036.file_digest(witness) != certificate["arbitrary_precision_witness_sha256"]:
        raise RuntimeError("5083 arbitrary-precision witness digest changed")
    if not certificate["accepted_local_zero_certificate"]:
        raise RuntimeError("5083 local zero certificate is not accepted")
    if certificate["general_g2_family_theorem_claimed"] or certificate["broad_5041_theorem_reinstated"]:
        raise RuntimeError("5083 certificate exceeded its event-local scope")
    return certificate


def recoil_scope_correction_gate() -> dict[str, Any]:
    if not RECOIL_SCOPE_CORRECTION_GATE.exists():
        raise FileNotFoundError(RECOIL_SCOPE_CORRECTION_GATE)
    for path in (
        RECOIL_ZERO_REGISTRY_V1,
        RECOIL_ZERO_REGISTRY_V2_GATE,
        RECOIL_ZERO_REGISTRY_V2,
        RECOIL_ZERO_REGISTRY_GATE,
        RECOIL_ZERO_REGISTRY,
        GENERAL_DIRECT_CLASSIFIER_GATE,
    ):
        if not path.exists():
            raise FileNotFoundError(path)
    gate = json.loads(RECOIL_SCOPE_CORRECTION_GATE.read_text(encoding="utf-8"))
    if not gate["passed"] or not gate["runner_integration_authorized"]:
        raise RuntimeError("5112 recoil scope correction is not accepted")
    if not gate["broad_5084_recoil_holomorphy_theorem_rejected"]:
        raise RuntimeError("5112 did not reject the falsified broad 5084 theorem")
    if not gate["stable_catalog_rows_take_precedence_over_the_rejected_structural_theorem"]:
        raise RuntimeError("5112 did not preserve stable numerical residues")
    if gate["event_local_zero_registry_sha256"] != M5036.file_digest(
        RECOIL_ZERO_REGISTRY_V1
    ):
        raise RuntimeError("5112 parent event-local zero registry changed")
    if gate["formalization_workbench_tree_sha256"] != FORMAL_BASELINE:
        raise RuntimeError("5112 formalization baseline changed")
    extension = json.loads(RECOIL_ZERO_REGISTRY_V2_GATE.read_text(encoding="utf-8"))
    if not extension["passed"] or not extension["runner_integration_authorized"]:
        raise RuntimeError("5113 event-local zero extension is not accepted")
    if extension["parent_scope_correction_gate_sha256"] != M5036.file_digest(
        RECOIL_SCOPE_CORRECTION_GATE
    ):
        raise RuntimeError("5113 parent scope-correction gate changed")
    if extension["parent_registry_sha256"] != M5036.file_digest(
        RECOIL_ZERO_REGISTRY_V1
    ):
        raise RuntimeError("5113 parent registry changed")
    if extension["merged_registry_sha256"] != M5036.file_digest(
        RECOIL_ZERO_REGISTRY_V2
    ):
        raise RuntimeError("5113 merged event-local zero registry changed")
    if extension["formalization_workbench_tree_sha256"] != FORMAL_BASELINE:
        raise RuntimeError("5113 formalization baseline changed")
    classifier = json.loads(RECOIL_ZERO_REGISTRY_GATE.read_text(encoding="utf-8"))
    if not classifier["passed"] or not classifier["on_demand_classifier_authorized"]:
        raise RuntimeError("5114 on-demand direct-residue classifier is not accepted")
    if classifier["parent_scope_gate_sha256"] != M5036.file_digest(
        RECOIL_SCOPE_CORRECTION_GATE
    ):
        raise RuntimeError("5114 parent scope gate changed")
    if classifier["parent_extension_gate_sha256"] != M5036.file_digest(
        RECOIL_ZERO_REGISTRY_V2_GATE
    ):
        raise RuntimeError("5114 parent extension gate changed")
    if classifier["parent_registry_sha256"] != M5036.file_digest(
        RECOIL_ZERO_REGISTRY_V2
    ):
        raise RuntimeError("5114 parent registry changed")
    if classifier["merged_registry_sha256"] != M5036.file_digest(
        RECOIL_ZERO_REGISTRY
    ):
        raise RuntimeError("5114 merged registry changed")
    if classifier["formalization_workbench_tree_sha256"] != FORMAL_BASELINE:
        raise RuntimeError("5114 formalization baseline changed")
    general = json.loads(GENERAL_DIRECT_CLASSIFIER_GATE.read_text(encoding="utf-8"))
    if not general["passed"] or not general["general_on_demand_classifier_authorized"]:
        raise RuntimeError("5115 general owned-direct classifier is not accepted")
    if general["parent_classifier_gate_sha256"] != M5036.file_digest(
        RECOIL_ZERO_REGISTRY_GATE
    ):
        raise RuntimeError("5115 parent classifier gate changed")
    if general["formalization_workbench_tree_sha256"] != FORMAL_BASELINE:
        raise RuntimeError("5115 formalization baseline changed")
    return general


def canonical_pairs(value: list[Any]) -> tuple[tuple[str, str], ...]:
    return tuple(
        sorted(tuple(sorted((str(pair[0]), str(pair[1])))) for pair in value)
    )


def event_local_recoil_zero_certificate(
    row: dict[str, Any], job_key: str
) -> dict[str, Any]:
    gate = recoil_scope_correction_gate()
    registry = json.loads(RECOIL_ZERO_REGISTRY.read_text(encoding="utf-8"))
    root = complex(row["root"])
    pairs = canonical_pairs(row["pairs"])
    matches = []
    for candidate in registry["rows"]:
        candidate_root = M5036.complex_from_row(candidate["root"])
        tolerance = float(candidate["root_match_relative_tolerance"])
        if (
            candidate["job_key"] == job_key
            and canonical_pairs(candidate["pairs"]) == pairs
            and abs(root - candidate_root)
            <= tolerance * max(1.0, abs(root), abs(candidate_root))
            and candidate["classification"]
            == "EVENT_LOCAL_ARBITRARY_PRECISION_ZERO"
            and float(candidate["maximum_magnitude"])
            < float(candidate["zero_tolerance"])
        ):
            matches.append(candidate)
    if len(matches) > 1:
        raise RuntimeError(
            f"5112 event-local registry matched {len(matches)} rows in {job_key}"
        )
    if not matches:
        return {
            "passed": False,
            "revision": REVISION,
            "reason": "no exact event-local arbitrary-precision zero row",
            "job_key": job_key,
            "root": {"real": root.real, "imaginary": root.imag},
            "pairs": [list(pair) for pair in pairs],
        }
    candidate = matches[0]
    return {
        "passed": True,
        "revision": REVISION,
        "job_key": job_key,
        "root": candidate["root"],
        "pairs": candidate["pairs"],
        "classification": candidate["classification"],
        "maximum_magnitude": candidate["maximum_magnitude"],
        "zero_tolerance": candidate["zero_tolerance"],
        "scope": candidate["scope"],
        "registry": str(RECOIL_ZERO_REGISTRY),
        "registry_sha256": M5036.file_digest(RECOIL_ZERO_REGISTRY),
        "scope_correction_gate": str(RECOIL_SCOPE_CORRECTION_GATE),
        "scope_correction_gate_sha256": M5036.file_digest(
            RECOIL_SCOPE_CORRECTION_GATE
        ),
        "registry_extension_gate": str(RECOIL_ZERO_REGISTRY_GATE),
        "registry_extension_gate_sha256": M5036.file_digest(
            RECOIL_ZERO_REGISTRY_GATE
        ),
        "broad_5084_theorem_allowed": False,
        "gate": gate["checkpoint_marker"],
        "valid_for_full_MTS_claim": False,
    }


def removable_extension_gate() -> dict[str, Any]:
    if not REMOVABLE_EXTENSION_GATE.exists():
        raise FileNotFoundError(REMOVABLE_EXTENSION_GATE)
    gate = json.loads(REMOVABLE_EXTENSION_GATE.read_text(encoding="utf-8"))
    if not gate["same_source_collision_removable_extension_accepted"]:
        raise RuntimeError("5085 removable collision extension is not accepted")
    recomputed = Path(gate["failed_A11_gate_recomputed"])
    if not recomputed.exists() or M5036.file_digest(recomputed) != gate[
        "failed_A11_gate_recomputed_sha256"
    ]:
        raise RuntimeError("5085 recomputed A11 gate is missing or changed")
    return gate


def outward_contour_gate() -> dict[str, Any]:
    if not OUTWARD_CONTOUR_GATE.exists():
        raise FileNotFoundError(OUTWARD_CONTOUR_GATE)
    gate = json.loads(OUTWARD_CONTOUR_GATE.read_text(encoding="utf-8"))
    if not gate["outward_same_source_contour_gate_accepted"]:
        raise RuntimeError("5086 outward contour gate is not accepted")
    recomputed = Path(gate["recomputed_gate"])
    if not recomputed.exists() or M5036.file_digest(recomputed) != gate[
        "recomputed_gate_sha256"
    ]:
        raise RuntimeError("5086 recomputed A12 gate is missing or changed")
    return gate


def double_zero_collision_gate() -> dict[str, Any]:
    if not DOUBLE_ZERO_COLLISION_GATE.exists():
        raise FileNotFoundError(DOUBLE_ZERO_COLLISION_GATE)
    gate = json.loads(DOUBLE_ZERO_COLLISION_GATE.read_text(encoding="utf-8"))
    if not gate["double_zero_certificate_passed"]:
        raise RuntimeError("5088 double-zero collision certificate is not accepted")
    if not gate["exact_collision_gate_accepted"]:
        raise RuntimeError("5088 exact collision event gate is not accepted")
    if not gate["runner_integration_authorized"]:
        raise RuntimeError("5088 did not authorize runner integration")
    recomputed = Path(gate["gate_path"])
    if not recomputed.exists() or M5036.file_digest(recomputed) != gate[
        "gate_sha256"
    ]:
        raise RuntimeError("5088 recomputed A07 gate is missing or changed")
    if gate["formalization_workbench_tree_sha256"] != FORMAL_BASELINE:
        raise RuntimeError("5088 formalization baseline changed")
    return gate


def multi_double_zero_collision_gate() -> dict[str, Any]:
    if not MULTI_DOUBLE_ZERO_COLLISION_GATE.exists():
        raise FileNotFoundError(MULTI_DOUBLE_ZERO_COLLISION_GATE)
    gate = json.loads(MULTI_DOUBLE_ZERO_COLLISION_GATE.read_text(encoding="utf-8"))
    if not gate["all_exact_collision_roots_certified"]:
        raise RuntimeError("5091 multi-root double-zero certificate is not accepted")
    if not gate["exact_collision_gate_accepted"]:
        raise RuntimeError("5091 exact collision event gate is not accepted")
    if not gate["runner_integration_authorized"]:
        raise RuntimeError("5091 did not authorize runner integration")
    recomputed = Path(gate["gate_path"])
    if not recomputed.exists() or M5036.file_digest(recomputed) != gate["gate_sha256"]:
        raise RuntimeError("5091 recomputed coarse A11 gate is missing or changed")
    if gate["formalization_workbench_tree_sha256"] != FORMAL_BASELINE:
        raise RuntimeError("5091 formalization baseline changed")
    return gate


def projective_cluster_zero_gate() -> dict[str, Any]:
    if not PROJECTIVE_CLUSTER_ZERO_GATE.exists():
        raise FileNotFoundError(PROJECTIVE_CLUSTER_ZERO_GATE)
    gate = json.loads(PROJECTIVE_CLUSTER_ZERO_GATE.read_text(encoding="utf-8"))
    if not gate["projective_cluster_zero_certificate_passed"]:
        raise RuntimeError("5097 projective cluster zero certificate is not accepted")
    if not gate["runner_integration_authorized"]:
        raise RuntimeError("5097 did not authorize runner integration")
    if gate["job_key"] != PROJECTIVE_CLUSTER_ZERO_JOB_KEY:
        raise RuntimeError("5097 job scope changed")
    if gate["source_theorem_module_sha256"] != M5036.file_digest(SCRIPT_5043):
        raise RuntimeError("5097 theorem source changed")
    if gate["formalization_workbench_tree_sha256"] != FORMAL_BASELINE:
        raise RuntimeError("5097 formalization baseline changed")
    return gate


def same_side_cluster_e020_gate() -> dict[str, Any]:
    if not SAME_SIDE_CLUSTER_E020_GATE.exists():
        raise FileNotFoundError(SAME_SIDE_CLUSTER_E020_GATE)
    gate = json.loads(SAME_SIDE_CLUSTER_E020_GATE.read_text(encoding="utf-8"))
    if not gate["same_side_cluster_cycle_certificate_passed"]:
        raise RuntimeError("5117 E020 same-side cluster certificate is not accepted")
    if not gate["production_integration_authorized"]:
        raise RuntimeError("5117 did not authorize production integration")
    if gate["job_key"] != SAME_SIDE_CLUSTER_E020_JOB_KEY:
        raise RuntimeError("5117 job scope changed")
    if gate["parent_cauchy_gate_sha256"] != M5036.file_digest(
        SAME_SIDE_CLUSTER_CYCLE_GATE
    ):
        raise RuntimeError("5117 parent Cauchy gate changed")
    if gate["formalization_workbench_tree_sha256"] != FORMAL_BASELINE:
        raise RuntimeError("5117 formalization baseline changed")
    for row in gate["gate_rows"]:
        path = Path(row["gate_path"])
        if not path.exists() or M5036.file_digest(path) != row["gate_sha256"]:
            raise RuntimeError("5117 recomputed cluster gate is missing or changed")
    return gate


def argument_independent_projective_cluster_zero_gate() -> dict[str, Any]:
    if not ARGUMENT_INDEPENDENT_PROJECTIVE_GATE.exists():
        raise FileNotFoundError(ARGUMENT_INDEPENDENT_PROJECTIVE_GATE)
    gate = json.loads(
        ARGUMENT_INDEPENDENT_PROJECTIVE_GATE.read_text(encoding="utf-8")
    )
    if not gate["argument_independent_projective_cluster_zero_passed"]:
        raise RuntimeError("5101 argument-independent projective zero is not accepted")
    if not gate["runner_integration_authorized"]:
        raise RuntimeError("5101 did not authorize runner integration")
    if gate["authorized_job_scopes"] != [ARGUMENT_INDEPENDENT_PROJECTIVE_JOB_KEY]:
        raise RuntimeError("5101 job scope changed")
    if gate["parent_gate_sha256"] != M5036.file_digest(PROJECTIVE_CLUSTER_ZERO_GATE):
        raise RuntimeError("5101 parent projective gate changed")
    if gate["formalization_workbench_tree_sha256"] != FORMAL_BASELINE:
        raise RuntimeError("5101 formalization baseline changed")
    return gate


def E020_projective_cluster_zero_gate() -> dict[str, Any]:
    if not E020_PROJECTIVE_CLUSTER_GATE.exists():
        raise FileNotFoundError(E020_PROJECTIVE_CLUSTER_GATE)
    gate = json.loads(E020_PROJECTIVE_CLUSTER_GATE.read_text(encoding="utf-8"))
    if not gate["argument_independent_projective_cluster_zero_passed"]:
        raise RuntimeError("5119 E020 projective cluster certificate is not accepted")
    if not gate["runner_integration_authorized"]:
        raise RuntimeError("5119 did not authorize runner integration")
    if tuple(gate["authorized_job_scopes"]) != E020_PROJECTIVE_CLUSTER_JOB_KEYS:
        raise RuntimeError("5119 E020 job scope changed")
    if gate["parent_5097_gate_sha256"] != M5036.file_digest(
        PROJECTIVE_CLUSTER_ZERO_GATE
    ):
        raise RuntimeError("5119 parent 5097 gate changed")
    if gate["parent_5101_gate_sha256"] != M5036.file_digest(
        ARGUMENT_INDEPENDENT_PROJECTIVE_GATE
    ):
        raise RuntimeError("5119 parent 5101 gate changed")
    if gate["formalization_workbench_tree_sha256"] != FORMAL_BASELINE:
        raise RuntimeError("5119 formalization baseline changed")
    return gate


def continuous_subminimum_cycle_gate() -> dict[str, Any]:
    if not CONTINUOUS_SUBMINIMUM_CYCLE_GATE.exists():
        raise FileNotFoundError(CONTINUOUS_SUBMINIMUM_CYCLE_GATE)
    gate = json.loads(CONTINUOUS_SUBMINIMUM_CYCLE_GATE.read_text(encoding="utf-8"))
    if not gate["continuous_subminimum_cycle_certificate_passed"]:
        raise RuntimeError("5099 continuous subminimum cycle is not accepted")
    if not gate["runner_integration_authorized"]:
        raise RuntimeError("5099 did not authorize runner integration")
    if gate["job_key"] != CONTINUOUS_SUBMINIMUM_CYCLE_JOB_KEY:
        raise RuntimeError("5099 job scope changed")
    if gate["subminimum_factor"] != M5099.SUBMINIMUM_FACTOR:
        raise RuntimeError("5099 subminimum factor changed")
    if gate["formalization_workbench_tree_sha256"] != FORMAL_BASELINE:
        raise RuntimeError("5099 formalization baseline changed")
    return gate


def apply_event_local_recoil_zero_registry(
    catalog: list[dict[str, Any]],
    ownership: dict[str, bool],
    job_key: str,
    module: Any,
) -> tuple[list[dict[str, Any]], bool]:
    del module
    gate = recoil_scope_correction_gate()
    if CURRENT_EVENT is None or CURRENT_ARGUMENT is None:
        raise RuntimeError("on-demand residue classifier has no active event/argument")
    for row in catalog:
        if bool(row["stable"]):
            continue
        certificate = event_local_recoil_zero_certificate(row, job_key)
        dynamic_resolution: dict[str, Any] | None = None
        if not certificate["passed"]:
            dynamic_resolution = M5115.resolve_unstable_record(
                row,
                ownership,
                job_key,
                CURRENT_EVENT,
                CURRENT_ARGUMENT,
            )
            if dynamic_resolution["classification"] in {
                "OUT_OF_SCOPE",
                "UNRESOLVED",
            }:
                continue
            certificate = {
                "passed": True,
                "revision": REVISION,
                "classification": dynamic_resolution["classification"],
                "root": dynamic_resolution["root"],
                "pairs": dynamic_resolution["pairs"],
                "on_demand_resolution": dynamic_resolution,
                "classifier_gate": str(GENERAL_DIRECT_CLASSIFIER_GATE),
                "classifier_gate_sha256": M5036.file_digest(
                    GENERAL_DIRECT_CLASSIFIER_GATE
                ),
                "broad_5084_theorem_allowed": False,
                "valid_for_full_MTS_claim": False,
            }
        original = {
            "residue_method": row["residue_method"],
            "outer_residue": str(row["outer_residue"]),
            "inner_residue": str(row["inner_residue"]),
            "residue_stability": float(row["residue_stability"]),
            "numerically_zero": bool(row["numerically_zero"]),
            "stable": bool(row["stable"]),
        }
        if certificate["classification"] == "EVENT_LOCAL_ARBITRARY_PRECISION_ZERO":
            row.update(
                {
                    "residue_method": REVISION,
                    "outer_residue": 0.0j,
                    "inner_residue": 0.0j,
                    "residue": 0.0j,
                    "residue_stability": 0.0,
                    "numerically_zero": True,
                    "stable": True,
                    "included_as_pole_model": False,
                    "event_local_recoil_zero_certificate": certificate,
                }
            )
        elif certificate["classification"] == "STABLE_DIRECT_COMPONENT_NONZERO":
            assert dynamic_resolution is not None
            residue = complex(
                float(dynamic_resolution["mean"]["real"]),
                float(dynamic_resolution["mean"]["imaginary"]),
            )
            stability = float(dynamic_resolution["maximum_spread"]) / max(
                abs(residue), 1.0e-300
            )
            row.update(
                {
                    "residue_method": REVISION,
                    "outer_residue": residue,
                    "inner_residue": residue,
                    "residue": residue,
                    "residue_stability": stability,
                    "numerically_zero": False,
                    "stable": True,
                    "included_as_pole_model": bool(row["near_path"]),
                    "on_demand_direct_nonzero_certificate": certificate,
                }
            )
        else:
            continue
        LOCAL_RESIDUE_RESOLUTION_AUDIT.append(
            {
                "job_key": job_key,
                "pairs": row["pairs"],
                "root": certificate["root"],
                "original_numeric_probe": original,
                "certificate_path": str(RECOIL_ZERO_REGISTRY),
                "certificate_sha256": M5036.file_digest(RECOIL_ZERO_REGISTRY),
                "scope_correction_gate": str(RECOIL_SCOPE_CORRECTION_GATE),
                "scope_correction_gate_sha256": M5036.file_digest(
                    RECOIL_SCOPE_CORRECTION_GATE
                ),
                "classifier_gate": str(GENERAL_DIRECT_CLASSIFIER_GATE),
                "classifier_gate_sha256": M5036.file_digest(
                    GENERAL_DIRECT_CLASSIFIER_GATE
                ),
                "resolution_classification": certificate["classification"],
                "on_demand": dynamic_resolution is not None,
                "certificate": certificate,
            }
        )
    return catalog, all(bool(row["stable"]) for row in catalog)


def apply_local_zero_certificate(
    catalog: list[dict[str, Any]],
    ownership: dict[str, bool],
    job_key: str,
) -> tuple[list[dict[str, Any]], bool]:
    certificate = local_zero_certificate()
    expected_job_prefix = (
        f"{certificate['argument_id'].split('_', 1)[0]}__"
        f"{certificate['event_id']}__"
        f"{certificate['argument_id'].split('_', 1)[1]}__"
    )
    if not job_key.startswith(expected_job_prefix):
        return catalog, all(bool(row["stable"]) for row in catalog)
    pair = tuple(sorted(str(value) for value in certificate["pair"]))
    certificate_root = M5036.complex_from_row(certificate["root"])
    matches = []
    for row in catalog:
        pairs = {
            tuple(sorted(str(value) for value in candidate))
            for candidate in row["pairs"]
        }
        root = complex(row["root"])
        if (
            pair in pairs
            and abs(root - certificate_root) <= 2.0e-10 * max(1.0, abs(root))
            and bool(ownership[certificate["owned_label"]])
            and not bool(ownership[certificate["unowned_label"]])
        ):
            matches.append(row)
    if len(matches) != 1:
        raise RuntimeError(
            f"5083 local certificate matched {len(matches)} rows in {job_key}"
        )
    row = matches[0]
    original = {
        "residue_method": row["residue_method"],
        "outer_residue": str(row["outer_residue"]),
        "inner_residue": str(row["inner_residue"]),
        "residue_stability": float(row["residue_stability"]),
        "numerically_zero": bool(row["numerically_zero"]),
        "stable": bool(row["stable"]),
    }
    row.update(
        {
            "residue_method": REVISION,
            "outer_residue": 0.0j,
            "inner_residue": 0.0j,
            "residue": 0.0j,
            "residue_stability": 0.0,
            "numerically_zero": True,
            "stable": True,
            "included_as_pole_model": False,
            "local_zero_certificate": {
                "path": str(LOCAL_ZERO_CERTIFICATE),
                "sha256": M5036.file_digest(LOCAL_ZERO_CERTIFICATE),
                "scope": certificate["certificate_scope"],
                "analytic_identity": certificate["analytic_identity"],
            },
        }
    )
    LOCAL_RESIDUE_RESOLUTION_AUDIT.append(
        {
            "job_key": job_key,
            "pair": list(certificate["pair"]),
            "root": certificate["root"],
            "original_numeric_probe": original,
            "certificate": str(LOCAL_ZERO_CERTIFICATE),
            "certificate_sha256": M5036.file_digest(LOCAL_ZERO_CERTIFICATE),
            "scope_enforced": "exact event, argument, ownership, pair, and root",
        }
    )
    return catalog, all(bool(candidate["stable"]) for candidate in catalog)


def apply_projective_cluster_zero(
    catalog: list[dict[str, Any]],
    ownership: dict[str, bool],
    job_key: str,
) -> tuple[list[dict[str, Any]], bool]:
    if job_key not in (
        PROJECTIVE_CLUSTER_ZERO_JOB_KEY,
        ARGUMENT_INDEPENDENT_PROJECTIVE_JOB_KEY,
        *E020_PROJECTIVE_CLUSTER_JOB_KEYS,
    ):
        return catalog, all(bool(row["stable"]) for row in catalog)
    if job_key == PROJECTIVE_CLUSTER_ZERO_JOB_KEY:
        gate = projective_cluster_zero_gate()
        certificate_path = PROJECTIVE_CLUSTER_ZERO_GATE
        certificate_function = M5097.projective_cluster_certificate
    elif job_key == ARGUMENT_INDEPENDENT_PROJECTIVE_JOB_KEY:
        gate = argument_independent_projective_cluster_zero_gate()
        certificate_path = ARGUMENT_INDEPENDENT_PROJECTIVE_GATE
        certificate_function = lambda row, ownership, gate: (
            M5101.argument_independent_projective_certificate(
                row, ownership, gate, M5097
            )
        )
    else:
        gate = E020_projective_cluster_zero_gate()
        certificate_path = E020_PROJECTIVE_CLUSTER_GATE
        certificate_function = lambda row, ownership, gate: (
            M5101.argument_independent_projective_certificate(
                row, ownership, gate, M5097
            )
        )
    for row in catalog:
        certificate = certificate_function(row, ownership, gate)
        if not certificate["passed"]:
            continue
        if bool(row["stable"]):
            if not bool(row["numerically_zero"]):
                raise RuntimeError(
                    "stable nonzero residue contradicts the guarded projective theorem: "
                    f"{job_key} {row['pairs']}"
                )
            continue
        original = {
            "residue_method": row["residue_method"],
            "outer_residue": str(row["outer_residue"]),
            "inner_residue": str(row["inner_residue"]),
            "residue_stability": float(row["residue_stability"]),
            "numerically_zero": bool(row["numerically_zero"]),
            "stable": bool(row["stable"]),
        }
        row.update(
            {
                "residue_method": REVISION,
                "outer_residue": 0.0j,
                "inner_residue": 0.0j,
                "residue": 0.0j,
                "residue_stability": 0.0,
                "numerically_zero": True,
                "stable": True,
                "included_as_pole_model": False,
                "projective_cross_source_cluster_zero_certificate": certificate,
            }
        )
        PROJECTIVE_CLUSTER_ZERO_AUDIT.append(
            {
                "job_key": job_key,
                "pairs": row["pairs"],
                "root": certificate["root"],
                "original_numeric_probe": original,
                "certificate": str(certificate_path),
                "certificate_sha256": M5036.file_digest(certificate_path),
                "scope_enforced": (
                    "exact event, argument, projective root pair, additive sources, "
                    "factor suffixes, and physical ownership"
                ),
            }
        )
    return catalog, all(bool(row["stable"]) for row in catalog)


def certified_primary_catalog(
    ownership: dict[str, bool],
    start: complex,
    end: complex,
    required_roots: list[complex],
    global_nodes: int,
    global_residue_nodes: int,
    relative_residue_nodes: int,
    model_distance: float,
) -> tuple[list[dict[str, Any]], bool]:
    catalog, _ = M5036.MREPAIR.repaired_chamber_residue_catalog(
        ownership,
        start,
        end,
        required_roots,
        global_nodes,
        global_residue_nodes,
        relative_residue_nodes,
        model_distance,
    )
    catalog, stable = apply_event_local_recoil_zero_registry(
        catalog,
        ownership,
        M5036.MREPAIR.CURRENT_JOB,
        M5036.N5030,
    )
    if stable:
        return catalog, stable
    catalog, stable = apply_projective_cluster_zero(
        catalog, ownership, M5036.MREPAIR.CURRENT_JOB
    )
    if stable:
        return catalog, stable
    catalog, stable = apply_local_zero_certificate(
        catalog, ownership, M5036.MREPAIR.CURRENT_JOB
    )
    if stable:
        return catalog, stable
    outward_contour_gate()
    return M5086.outward_same_source_repair(
        catalog,
        ownership,
        M5036.N5030,
        M5036.MREPAIR.CURRENT_JOB,
        OUTWARD_CONTOUR_AUDIT,
    )


def restricted_coarse_catalog(
    ownership: dict[str, bool],
    start: complex,
    end: complex,
    required_roots: list[complex],
    global_nodes: int,
    global_residue_nodes: int,
    relative_residue_nodes: int,
    model_distance: float,
) -> tuple[list[dict[str, Any]], bool]:
    recoil_scope_correction_gate()
    original = M5043.M5041.theorem_certificate
    M5043.M5041.theorem_certificate = lambda row, candidate_ownership: (
        event_local_recoil_zero_certificate(row, M5043.CURRENT_JOB)
    )
    try:
        catalog, _ = M5043.theorem_first_chamber_residue_catalog(
            ownership,
            start,
            end,
            required_roots,
            global_nodes,
            global_residue_nodes,
            relative_residue_nodes,
            model_distance,
        )
    finally:
        M5043.M5041.theorem_certificate = original
    catalog, stable = apply_event_local_recoil_zero_registry(
        catalog, ownership, M5043.CURRENT_JOB, M5043.N5030
    )
    if stable:
        return catalog, stable
    catalog, stable = apply_projective_cluster_zero(
        catalog, ownership, M5043.CURRENT_JOB
    )
    if stable:
        return catalog, stable
    catalog, stable = apply_local_zero_certificate(
        catalog, ownership, M5043.CURRENT_JOB
    )
    if stable:
        return catalog, stable
    outward_contour_gate()
    return M5086.outward_same_source_repair(
        catalog,
        ownership,
        M5043.N5030,
        M5043.CURRENT_JOB,
        OUTWARD_CONTOUR_AUDIT,
    )


def make_config(manifest: dict[str, Any], run_id: str) -> dict[str, Any]:
    seeds = [
        *[int(value) for value in manifest["fresh_high_scramble_seeds"]],
        *[int(value) for value in manifest["fresh_low_scramble_seeds"]],
    ]
    arguments = argparse.Namespace(
        run_id=run_id,
        physical_cosines="-0.6,-0.3,0,0.3,0.6",
        epsilons="0.08,0.04,0.02",
        seeds=",".join(str(value) for value in seeds),
        power=0,
        topology_steps=96,
        topology_maximum_steps=49152,
        regulator=1.0e-3,
        boundary_tracking_steps=64,
    )
    config = M5036.make_config(arguments)
    config["checkpoint_marker"] = MARKER
    config["schema_revision"] = REVISION
    config["pilot_manifest"] = str(MANIFEST)
    config["pilot_manifest_digest"] = M5036.file_digest(MANIFEST)
    config["argument_certificate_step_levels"] = list(
        ARGUMENT_CERTIFICATE_STEP_LEVELS
    )
    config["uncertified_topology_action"] = "full_homotopy_fallback"
    config["residue_certificate_policy"] = {
        "rejected_structural_theorem": str(RECOIL_THEOREM_GATE),
        "rejected_structural_theorem_sha256": M5036.file_digest(RECOIL_THEOREM_GATE),
        "scope_correction_gate": str(RECOIL_SCOPE_CORRECTION_GATE),
        "scope_correction_gate_sha256": M5036.file_digest(
            RECOIL_SCOPE_CORRECTION_GATE
        ),
        "event_local_recoil_registry_gate": str(RECOIL_ZERO_REGISTRY_GATE),
        "event_local_recoil_registry_gate_sha256": M5036.file_digest(
            RECOIL_ZERO_REGISTRY_GATE
        ),
        "general_owned_direct_classifier_gate": str(GENERAL_DIRECT_CLASSIFIER_GATE),
        "general_owned_direct_classifier_gate_sha256": M5036.file_digest(
            GENERAL_DIRECT_CLASSIFIER_GATE
        ),
        "event_local_recoil_zero_registry": str(RECOIL_ZERO_REGISTRY),
        "event_local_recoil_zero_registry_sha256": M5036.file_digest(
            RECOIL_ZERO_REGISTRY
        ),
        "stable_numeric_rows_take_precedence": True,
        "event_local_extension": str(LOCAL_ZERO_CERTIFICATE),
        "event_local_extension_sha256": M5036.file_digest(LOCAL_ZERO_CERTIFICATE),
        "broad_5084_theorem_allowed": False,
        "broad_5041_theorem_allowed": False,
    }
    config["removable_global_collision_policy"] = {
        "gate": str(REMOVABLE_EXTENSION_GATE),
        "gate_sha256": M5036.file_digest(REMOVABLE_EXTENSION_GATE),
        "scope": "opposite-ownership direct:g1/g2 u-v same-source coalescences",
        "failure_action": "fail_closed_if_multidirection_limit_does_not_converge",
    }
    config["exact_double_zero_global_collision_policy"] = {
        "single_root_gate": str(DOUBLE_ZERO_COLLISION_GATE),
        "single_root_gate_sha256": M5036.file_digest(DOUBLE_ZERO_COLLISION_GATE),
        "multi_root_gate": str(MULTI_DOUBLE_ZERO_COLLISION_GATE),
        "multi_root_gate_sha256": M5036.file_digest(MULTI_DOUBLE_ZERO_COLLISION_GATE),
        "job_scopes": [DOUBLE_ZERO_JOB_KEY, MULTI_DOUBLE_ZERO_JOB_KEY],
        "owned_residue_limit": "exactly_zero",
        "principal_value_or_half_residue_inserted": False,
        "failure_action": "fall_through_to_5085_then_fail_closed",
    }
    config["same_side_global_cluster_cycle_policy"] = {
        "gate": str(SAME_SIDE_CLUSTER_CYCLE_GATE),
        "gate_sha256": M5036.file_digest(SAME_SIDE_CLUSTER_CYCLE_GATE),
        "E020_extension_gate": str(SAME_SIDE_CLUSTER_E020_GATE),
        "E020_extension_gate_sha256": M5036.file_digest(
            SAME_SIDE_CLUSTER_E020_GATE
        ),
        "job_scopes": [SAME_SIDE_CLUSTER_JOB_KEY, SAME_SIDE_CLUSTER_E020_JOB_KEY],
        "link_relative_distance": M5095.LINK_RELATIVE_DISTANCE,
        "maximum_cluster_isolation_ratio": M5095.MAXIMUM_CLUSTER_ISOLATION_RATIO,
        "identity": "one contour around an isolated same-sign pole cluster equals the sum of its individual residues",
        "failure_action": "fall_back_to_individual_residues_unless_the_isolated_disk_guard_passes",
    }
    config["projective_cross_source_cluster_zero_policy"] = {
        "gate": str(PROJECTIVE_CLUSTER_ZERO_GATE),
        "gate_sha256": M5036.file_digest(PROJECTIVE_CLUSTER_ZERO_GATE),
        "job_scopes": [PROJECTIVE_CLUSTER_ZERO_JOB_KEY],
        "identity": (
            "p_g2=-sqrt(1-x) p_decay at the certified reciprocal q roots; "
            "additive cross-source factor collisions have zero iterated residue"
        ),
        "broad_cross_source_theorem_allowed": False,
        "failure_action": "fail_closed_outside_the_exact_projective_and_ownership_guards",
    }
    config["argument_independent_projective_cluster_zero_policy"] = {
        "gate": str(ARGUMENT_INDEPENDENT_PROJECTIVE_GATE),
        "gate_sha256": M5036.file_digest(ARGUMENT_INDEPENDENT_PROJECTIVE_GATE),
        "parent_gate": str(PROJECTIVE_CLUSTER_ZERO_GATE),
        "parent_gate_sha256": M5036.file_digest(PROJECTIVE_CLUSTER_ZERO_GATE),
        "job_scopes": [ARGUMENT_INDEPENDENT_PROJECTIVE_JOB_KEY],
        "identity": (
            "for p'=lambda p, all four factor roots are ratios of homogeneous "
            "momentum-linear forms and therefore independent of lambda"
        ),
        "broad_cross_source_theorem_allowed": False,
        "failure_action": "fail_closed_outside_the_exact_A14_projective_and_ownership_guards",
    }
    config["E020_projective_cluster_zero_policy"] = {
        "gate": str(E020_PROJECTIVE_CLUSTER_GATE),
        "gate_sha256": M5036.file_digest(E020_PROJECTIVE_CLUSTER_GATE),
        "parent_gate": str(ARGUMENT_INDEPENDENT_PROJECTIVE_GATE),
        "parent_gate_sha256": M5036.file_digest(
            ARGUMENT_INDEPENDENT_PROJECTIVE_GATE
        ),
        "job_scopes": list(E020_PROJECTIVE_CLUSTER_JOB_KEYS),
        "identity": (
            "homogeneous factor-root ratios are independent of the finite "
            "external E020 argument; the guarded additive-source Cauchy residue vanishes"
        ),
        "broad_event_theorem_allowed": False,
        "failure_action": "fail_closed_outside_S507622_E020_and_the_projective_ownership_guards",
    }
    config["continuous_subminimum_global_cycle_policy"] = {
        "gate": str(CONTINUOUS_SUBMINIMUM_CYCLE_GATE),
        "gate_sha256": M5036.file_digest(CONTINUOUS_SUBMINIMUM_CYCLE_GATE),
        "job_scopes": [CONTINUOUS_SUBMINIMUM_CYCLE_JOB_KEY],
        "subminimum_factor": M5099.SUBMINIMUM_FACTOR,
        "identity": (
            "r(q)=eta min_j|z_j(q)| encloses no finite pole; adding all causally "
            "owned residues reconstructs the same global cycle by Cauchy's theorem"
        ),
        "failure_action": "fail_closed_outside_the_exact_regulated_path_certificate",
    }
    config["outward_residue_contour_policy"] = {
        "gate": str(OUTWARD_CONTOUR_GATE),
        "gate_sha256": M5036.file_digest(OUTWARD_CONTOUR_GATE),
        "fractions": list(M5086.OUTWARD_FRACTIONS),
        "failure_action": "fail_closed_unless_two_node_ladders_and_cross_ladder_pass",
    }
    config["source_files"][str(Path(__file__).resolve())] = M5036.file_digest(
        Path(__file__).resolve()
    )
    config["source_files"][str(SCRIPT_5045)] = M5036.file_digest(SCRIPT_5045)
    config["source_files"][str(LOCAL_ZERO_CERTIFICATE)] = M5036.file_digest(
        LOCAL_ZERO_CERTIFICATE
    )
    config["source_files"][str(SCRIPT_5084)] = M5036.file_digest(SCRIPT_5084)
    config["source_files"][str(RECOIL_THEOREM_GATE)] = M5036.file_digest(
        RECOIL_THEOREM_GATE
    )
    config["source_files"][str(SCRIPT_5112)] = M5036.file_digest(SCRIPT_5112)
    config["source_files"][str(SCRIPT_5113)] = M5036.file_digest(SCRIPT_5113)
    config["source_files"][str(SCRIPT_5114)] = M5036.file_digest(SCRIPT_5114)
    config["source_files"][str(SCRIPT_5115)] = M5036.file_digest(SCRIPT_5115)
    config["source_files"][str(RECOIL_SCOPE_CORRECTION_GATE)] = M5036.file_digest(
        RECOIL_SCOPE_CORRECTION_GATE
    )
    config["source_files"][str(RECOIL_ZERO_REGISTRY)] = M5036.file_digest(
        RECOIL_ZERO_REGISTRY
    )
    config["source_files"][str(RECOIL_ZERO_REGISTRY_GATE)] = M5036.file_digest(
        RECOIL_ZERO_REGISTRY_GATE
    )
    config["source_files"][str(GENERAL_DIRECT_CLASSIFIER_GATE)] = M5036.file_digest(
        GENERAL_DIRECT_CLASSIFIER_GATE
    )
    config["source_files"][str(RECOIL_ZERO_REGISTRY_V1)] = M5036.file_digest(
        RECOIL_ZERO_REGISTRY_V1
    )
    config["source_files"][str(RECOIL_ZERO_REGISTRY_V2_GATE)] = M5036.file_digest(
        RECOIL_ZERO_REGISTRY_V2_GATE
    )
    config["source_files"][str(RECOIL_ZERO_REGISTRY_V2)] = M5036.file_digest(
        RECOIL_ZERO_REGISTRY_V2
    )
    config["source_files"][str(SCRIPT_5085)] = M5036.file_digest(SCRIPT_5085)
    config["source_files"][str(REMOVABLE_EXTENSION_GATE)] = M5036.file_digest(
        REMOVABLE_EXTENSION_GATE
    )
    config["source_files"][str(SCRIPT_5086)] = M5036.file_digest(SCRIPT_5086)
    config["source_files"][str(OUTWARD_CONTOUR_GATE)] = M5036.file_digest(
        OUTWARD_CONTOUR_GATE
    )
    config["source_files"][str(SCRIPT_5088)] = M5036.file_digest(SCRIPT_5088)
    config["source_files"][str(DOUBLE_ZERO_COLLISION_GATE)] = M5036.file_digest(
        DOUBLE_ZERO_COLLISION_GATE
    )
    config["source_files"][str(SCRIPT_5091)] = M5036.file_digest(SCRIPT_5091)
    config["source_files"][str(MULTI_DOUBLE_ZERO_COLLISION_GATE)] = M5036.file_digest(
        MULTI_DOUBLE_ZERO_COLLISION_GATE
    )
    config["source_files"][str(SCRIPT_5095)] = M5036.file_digest(SCRIPT_5095)
    config["source_files"][str(SCRIPT_5117)] = M5036.file_digest(SCRIPT_5117)
    config["source_files"][str(SCRIPT_5119)] = M5036.file_digest(SCRIPT_5119)
    config["source_files"][str(SAME_SIDE_CLUSTER_CYCLE_GATE)] = M5036.file_digest(
        SAME_SIDE_CLUSTER_CYCLE_GATE
    )
    config["source_files"][str(SAME_SIDE_CLUSTER_E020_GATE)] = M5036.file_digest(
        SAME_SIDE_CLUSTER_E020_GATE
    )
    config["source_files"][str(E020_PROJECTIVE_CLUSTER_GATE)] = M5036.file_digest(
        E020_PROJECTIVE_CLUSTER_GATE
    )
    config["source_files"][str(SCRIPT_5097)] = M5036.file_digest(SCRIPT_5097)
    config["source_files"][str(PROJECTIVE_CLUSTER_ZERO_GATE)] = M5036.file_digest(
        PROJECTIVE_CLUSTER_ZERO_GATE
    )
    config["source_files"][str(SCRIPT_5099)] = M5036.file_digest(SCRIPT_5099)
    config["source_files"][str(CONTINUOUS_SUBMINIMUM_CYCLE_GATE)] = M5036.file_digest(
        CONTINUOUS_SUBMINIMUM_CYCLE_GATE
    )
    config["source_files"][str(SCRIPT_5101)] = M5036.file_digest(SCRIPT_5101)
    config["source_files"][str(ARGUMENT_INDEPENDENT_PROJECTIVE_GATE)] = M5036.file_digest(
        ARGUMENT_INDEPENDENT_PROJECTIVE_GATE
    )
    config["central_anchor_acceleration"] = {
        "anchor_argument_id": ANCHOR_ID,
        "argument_rule": manifest["argument_topology_rule"],
        "epsilon_rule": manifest["epsilon_topology_rule"],
        "quadrature_breakpoint_rule": manifest["quadrature_breakpoint_rule"],
        "default_enabled": False,
        "valid_for_full_MTS_claim": False,
    }
    config.pop("config_digest", None)
    config["config_digest"] = M5036.canonical_digest(config)
    return config


def pilot_jobs(config: dict[str, Any], manifest: dict[str, Any]) -> list[dict[str, Any]]:
    argument_ids = [row["argument_id"] for row in config["base_arguments"]]
    high_seeds = {int(value) for value in manifest["fresh_high_scramble_seeds"]}
    low_seeds = {int(value) for value in manifest["fresh_low_scramble_seeds"]}
    events = {int(row["seed"]): row for row in config["events"]}
    rows = []
    for seed in sorted(high_seeds):
        event = events[seed]
        for epsilon_id in ("E040", "E020"):
            for base_id in argument_ids:
                rows.append(
                    {
                        "job_key": f"{epsilon_id}__{event['event_id']}__{base_id}__primary24",
                        "profile": "primary24",
                        "epsilon_id": epsilon_id,
                        "event_id": event["event_id"],
                        "base_argument_id": base_id,
                    }
                )
        for base_id in argument_ids:
            rows.append(
                {
                    "job_key": f"E040__{event['event_id']}__{base_id}__coarse12",
                    "profile": "coarse12",
                    "epsilon_id": "E040",
                    "event_id": event["event_id"],
                    "base_argument_id": base_id,
                }
            )
    for seed in sorted(low_seeds):
        event = events[seed]
        for base_id in argument_ids:
            rows.append(
                {
                    "job_key": f"E040__{event['event_id']}__{base_id}__coarse12",
                    "profile": "coarse12",
                    "epsilon_id": "E040",
                    "event_id": event["event_id"],
                    "base_argument_id": base_id,
                }
            )
    return rows


class CentralTopologyManager:
    def __init__(self, run_directory: Path, config: dict[str, Any]):
        self.run_directory = run_directory
        self.config = config
        self.events = M5036.event_lookup(config)
        self.arguments = M5036.argument_lookup(config)
        self.base_order = tuple(
            row["argument_id"] for row in config["base_arguments"]
        )

    def output_path(self, event_id: str, argument_id: str) -> Path:
        return M5036.M5035.M5034.topology_path(
            self.run_directory, event_id, argument_id
        )

    def cached(
        self, event_id: str, argument_id: str
    ) -> tuple[dict[str, Any], Path, float] | None:
        output = self.output_path(event_id, argument_id)
        if not output.exists():
            return None
        candidate = json.loads(output.read_text(encoding="utf-8"))
        if (
            candidate.get("config_digest") == self.config["config_digest"]
            and candidate.get("event_id") == event_id
            and candidate.get("argument_id") == argument_id
        ):
            return candidate, output, 0.0
        return None

    def write_composed(
        self,
        source_document: dict[str, Any],
        source_path: Path,
        event_id: str,
        argument_id: str,
        suite: str,
    ) -> tuple[dict[str, Any], Path, float]:
        cached = self.cached(event_id, argument_id)
        if cached is not None:
            return cached
        argument = self.arguments[argument_id]
        target = M5036.complex_from_row(argument["target_cosine"])
        started = time.monotonic()
        original_step_levels = tuple(M5069.FEYNMAN_STEP_LEVELS)
        if suite != "E040_TO_E020":
            M5069.FEYNMAN_STEP_LEVELS = tuple(
                int(value)
                for value in self.config["argument_certificate_step_levels"]
            )
        try:
            certified, levels = M5069.certify_segment(
                source_document, target, suite
            )
        finally:
            M5069.FEYNMAN_STEP_LEVELS = original_step_levels
        if certified is None:
            certification_runtime = time.monotonic() - started
            document, output, full_runtime = ORIGINAL_OBTAIN_TOPOLOGY(
                self.run_directory,
                self.config,
                self.events[event_id],
                argument,
            )
            document["central_anchor_fallback"] = {
                "reason": "certificate_not_converged",
                "suite": suite,
                "attempted_resolutions": [
                    int(level["resolution"]) for level in levels
                ],
                "certificate_runtime_seconds": certification_runtime,
                "full_homotopy_runtime_seconds": full_runtime,
            }
            document["valid_for_full_MTS_claim"] = False
            atomic_json(output, document)
            return (
                document,
                output,
                certification_runtime + full_runtime,
            )
        transported, diagnostics = M5069.construct_path_transported_document(
            source_document,
            target,
            source_path,
            suite,
            certified,
        )
        if not diagnostics["path_root_transport_valid"]:
            raise RuntimeError(
                f"path root transport failed for {event_id} {argument_id}"
            )
        document = M5069.compose_document(transported, certified)
        runtime = time.monotonic() - started
        document.update(
            {
                "checkpoint_marker": MARKER,
                "revision": REVISION,
                "config_digest": self.config["config_digest"],
                "event_id": event_id,
                "argument_id": argument_id,
                "topology_runtime_seconds": runtime,
                "central_anchor_argument_id": ANCHOR_ID,
                "fresh_kernel_execution_authorized": False,
                "valid_for_full_MTS_claim": False,
            }
        )
        output = self.output_path(event_id, argument_id)
        atomic_json(output, document)
        return document, output, runtime

    def obtain_e040(
        self, event_id: str, base_id: str
    ) -> tuple[dict[str, Any], Path, float]:
        argument_id = f"E040_{base_id}"
        cached = self.cached(event_id, argument_id)
        if cached is not None:
            return cached
        event = self.events[event_id]
        anchor_argument_id = f"E040_{ANCHOR_ID}"
        anchor_cached = self.cached(event_id, anchor_argument_id)
        total_runtime = 0.0
        if anchor_cached is None:
            anchor_cached = ORIGINAL_OBTAIN_TOPOLOGY(
                self.run_directory,
                self.config,
                event,
                self.arguments[anchor_argument_id],
            )
        current_document, current_path, runtime = anchor_cached
        total_runtime += runtime
        if base_id == ANCHOR_ID:
            return current_document, current_path, total_runtime
        anchor_index = self.base_order.index(ANCHOR_ID)
        target_index = self.base_order.index(base_id)
        step = 1 if target_index > anchor_index else -1
        for index in range(anchor_index + step, target_index + step, step):
            next_base_id = self.base_order[index]
            next_argument_id = f"E040_{next_base_id}"
            current_document, current_path, runtime = self.write_composed(
                current_document,
                current_path,
                event_id,
                next_argument_id,
                "E040_ARGUMENT_ADJACENCY",
            )
            total_runtime += runtime
        return current_document, current_path, total_runtime

    def obtain(
        self, event_id: str, epsilon_id: str, base_id: str
    ) -> tuple[dict[str, Any], Path, float]:
        if epsilon_id == "E040":
            return self.obtain_e040(event_id, base_id)
        if epsilon_id != "E020":
            raise ValueError(f"unsupported accelerated epsilon {epsilon_id}")
        argument_id = f"E020_{base_id}"
        cached = self.cached(event_id, argument_id)
        if cached is not None:
            return cached
        source_document, source_path, source_runtime = self.obtain_e040(
            event_id, base_id
        )
        document, output, runtime = self.write_composed(
            source_document,
            source_path,
            event_id,
            argument_id,
            "E040_TO_E020",
        )
        return document, output, source_runtime + runtime


def execute_kernel(
    run_directory: Path,
    config: dict[str, Any],
    manager: CentralTopologyManager,
    job: dict[str, Any],
) -> dict[str, Any]:
    global CURRENT_EVENT, CURRENT_ARGUMENT
    output = run_directory / "jobs" / f"{job['job_key']}.json"
    if output.exists():
        existing = json.loads(output.read_text(encoding="utf-8"))
        if (
            existing.get("config_digest") == config["config_digest"]
            and existing.get("status") == "COMPLETED_CONVERGED"
        ):
            return {**existing, "resumed_from_cache": True}
    event = manager.events[job["event_id"]]
    argument = manager.arguments[
        f"{job['epsilon_id']}_{job['base_argument_id']}"
    ]
    CURRENT_EVENT = event
    CURRENT_ARGUMENT = argument
    started = time.monotonic()
    try:
        topology, topology_path, topology_runtime = manager.obtain(
            job["event_id"], job["epsilon_id"], job["base_argument_id"]
        )
        target = M5036.complex_from_row(argument["target_cosine"])
        if job["profile"] == "primary24":
            module = M5036.N5030
            M5036.M5035.M5034.configure(event, target)
            profile = config["tiers"]["primary24"]
            previous_catalog = module.chamber_residue_catalog
            module.chamber_residue_catalog = certified_primary_catalog
            M5036.MREPAIR.CURRENT_JOB = job["job_key"]
            M5036.MREPAIR.RADIUS_AUDIT.clear()
            LOCAL_RESIDUE_RESOLUTION_AUDIT.clear()
            OUTWARD_CONTOUR_AUDIT.clear()
            PROJECTIVE_CLUSTER_ZERO_AUDIT.clear()
        else:
            module = M5043.N5030
            M5043.M5034.configure(event, target)
            profile = M5043.PROFILES["coarse12"]
            previous_catalog = module.chamber_residue_catalog
            module.chamber_residue_catalog = restricted_coarse_catalog
            M5043.CURRENT_JOB = job["job_key"]
            M5043.THEOREM_AUDIT.clear()
            M5043.CHART_AUDIT.clear()
            M5043.NUMERIC_AUDIT.clear()
            LOCAL_RESIDUE_RESOLUTION_AUDIT.clear()
            OUTWARD_CONTOUR_AUDIT.clear()
            PROJECTIVE_CLUSTER_ZERO_AUDIT.clear()
        removable_extension_gate()
        previous_global_chamber_value = module.global_chamber_value
        same_side_cluster_extension = None
        exact_double_zero_extension = None
        exact_or_original_global_chamber_value = previous_global_chamber_value
        if job["job_key"] in (
            SAME_SIDE_CLUSTER_JOB_KEY,
            SAME_SIDE_CLUSTER_E020_JOB_KEY,
        ):
            if job["job_key"] == SAME_SIDE_CLUSTER_E020_JOB_KEY:
                same_side_cluster_e020_gate()
            same_side_cluster_extension = M5095.CertifiedSameSideClusterGlobalValue(
                module
            )
            exact_or_original_global_chamber_value = same_side_cluster_extension
        elif job["job_key"] == DOUBLE_ZERO_JOB_KEY:
            double_zero_gate = double_zero_collision_gate()
            exact_double_zero_extension = M5088.CertifiedDoubleZeroGlobalExtension(
                module,
                previous_global_chamber_value,
                M5085,
                M5036.complex_from_row(
                    double_zero_gate["relative_collision_root"]
                ),
                set(double_zero_gate["certified_physical_ownership_digests"]),
                bool(double_zero_gate["double_zero_certificate_passed"]),
            )
            exact_or_original_global_chamber_value = exact_double_zero_extension
        elif job["job_key"] == MULTI_DOUBLE_ZERO_JOB_KEY:
            multi_double_zero_gate = multi_double_zero_collision_gate()
            exact_double_zero_extension = M5091.CertifiedMultiDoubleZeroGlobalExtension(
                module,
                previous_global_chamber_value,
                M5085,
                M5088,
                tuple(
                    M5036.complex_from_row(row["relative_collision_root"])
                    for row in multi_double_zero_gate["root_certificates"]
                ),
                set(multi_double_zero_gate["certified_physical_ownership_digests"]),
                bool(multi_double_zero_gate["all_exact_collision_roots_certified"]),
            )
            exact_or_original_global_chamber_value = exact_double_zero_extension
        removable_extension = M5085.CertifiedRemovableGlobalExtension(
            exact_or_original_global_chamber_value
        )
        module.global_chamber_value = removable_extension
        previous_conditioned_base_radius = (
            module.M5028.M5026.conditioned_global_base_radius
        )
        continuous_subminimum_gate = None
        if job["job_key"] == CONTINUOUS_SUBMINIMUM_CYCLE_JOB_KEY:
            continuous_subminimum_gate = continuous_subminimum_cycle_gate()
            module.M5028.M5026.conditioned_global_base_radius = (
                M5099.continuous_subminimum_radius
            )
        kernel_started = time.monotonic()
        try:
            gate = module.fixed_event_integral_gate(
                topology,
                tuple(int(value) for value in profile["relative_orders"]),
                int(profile["global_nodes"]),
                int(profile["global_residue_nodes"]),
                int(profile["relative_residue_nodes"]),
                float(profile["model_distance"]),
                int(config["topology"]["boundary_tracking_steps"]),
                str(profile["relative_quadrature_mode"]),
                float(profile["relative_adaptive_tolerance"]),
                int(profile["relative_adaptive_maximum_intervals"]),
            )
        finally:
            module.chamber_residue_catalog = previous_catalog
            module.global_chamber_value = previous_global_chamber_value
            module.M5028.M5026.conditioned_global_base_radius = (
                previous_conditioned_base_radius
            )
        if job["profile"] == "primary24":
            profile_audit = {
                "residue_radius_adjustment_count": len(
                    M5036.MREPAIR.RADIUS_AUDIT
                ),
                "residue_radius_adjustments": list(
                    M5036.MREPAIR.RADIUS_AUDIT
                ),
                "event_local_residue_resolution_count": len(LOCAL_RESIDUE_RESOLUTION_AUDIT),
                "event_local_residue_resolution_rows": list(LOCAL_RESIDUE_RESOLUTION_AUDIT),
                "projective_cluster_zero_certificate_count": len(
                    PROJECTIVE_CLUSTER_ZERO_AUDIT
                ),
                "projective_cluster_zero_certificate_rows": list(
                    PROJECTIVE_CLUSTER_ZERO_AUDIT
                ),
                "removable_global_collision_extension_count": len(
                    removable_extension.calls
                ),
                "removable_global_collision_extensions": list(
                    removable_extension.calls
                ),
                "exact_double_zero_collision_extension_count": (
                    len(exact_double_zero_extension.calls)
                    if exact_double_zero_extension is not None
                    else 0
                ),
                "exact_double_zero_collision_extensions": (
                    list(exact_double_zero_extension.calls)
                    if exact_double_zero_extension is not None
                    else []
                ),
                "outward_contour_repair_count": len(OUTWARD_CONTOUR_AUDIT),
                "outward_contour_repairs": list(OUTWARD_CONTOUR_AUDIT),
                "same_side_cluster_cycle_audit": (
                    same_side_cluster_extension.summary()
                    if same_side_cluster_extension is not None
                    else None
                ),
                "continuous_subminimum_cycle_audit": (
                    {
                        "gate": str(CONTINUOUS_SUBMINIMUM_CYCLE_GATE),
                        "gate_sha256": M5036.file_digest(
                            CONTINUOUS_SUBMINIMUM_CYCLE_GATE
                        ),
                        "subminimum_factor": M5099.SUBMINIMUM_FACTOR,
                        "job_scope": CONTINUOUS_SUBMINIMUM_CYCLE_JOB_KEY,
                    }
                    if continuous_subminimum_gate is not None
                    else None
                ),
            }
        else:
            profile_audit = {
                "theorem_zero_residue_count": len(M5043.THEOREM_AUDIT),
                "numeric_residue_count": len(M5043.NUMERIC_AUDIT),
                "chart_origin_exclusion_count": len(M5043.CHART_AUDIT),
                "theorem_zero_rows": list(M5043.THEOREM_AUDIT),
                "numeric_residue_rows": list(M5043.NUMERIC_AUDIT),
                "chart_origin_exclusions": list(M5043.CHART_AUDIT),
                "theorem_scope": "5084_guarded_owned_direct_g1_g2",
                "broad_5041_theorem_allowed": False,
                "event_local_residue_resolution_count": len(LOCAL_RESIDUE_RESOLUTION_AUDIT),
                "event_local_residue_resolution_rows": list(LOCAL_RESIDUE_RESOLUTION_AUDIT),
                "projective_cluster_zero_certificate_count": len(
                    PROJECTIVE_CLUSTER_ZERO_AUDIT
                ),
                "projective_cluster_zero_certificate_rows": list(
                    PROJECTIVE_CLUSTER_ZERO_AUDIT
                ),
                "removable_global_collision_extension_count": len(
                    removable_extension.calls
                ),
                "removable_global_collision_extensions": list(
                    removable_extension.calls
                ),
                "exact_double_zero_collision_extension_count": (
                    len(exact_double_zero_extension.calls)
                    if exact_double_zero_extension is not None
                    else 0
                ),
                "exact_double_zero_collision_extensions": (
                    list(exact_double_zero_extension.calls)
                    if exact_double_zero_extension is not None
                    else []
                ),
                "outward_contour_repair_count": len(OUTWARD_CONTOUR_AUDIT),
                "outward_contour_repairs": list(OUTWARD_CONTOUR_AUDIT),
                "same_side_cluster_cycle_audit": (
                    same_side_cluster_extension.summary()
                    if same_side_cluster_extension is not None
                    else None
                ),
                "continuous_subminimum_cycle_audit": (
                    {
                        "gate": str(CONTINUOUS_SUBMINIMUM_CYCLE_GATE),
                        "gate_sha256": M5036.file_digest(
                            CONTINUOUS_SUBMINIMUM_CYCLE_GATE
                        ),
                        "subminimum_factor": M5099.SUBMINIMUM_FACTOR,
                        "job_scope": CONTINUOUS_SUBMINIMUM_CYCLE_JOB_KEY,
                    }
                    if continuous_subminimum_gate is not None
                    else None
                ),
            }
        kernel_runtime = time.monotonic() - kernel_started
        kernel = M5036.M5035.M5034.highest_value(gate)
        direct = M5036.M5035.M5034.KERNEL_MULTIPLIER * kernel
        strict_adaptive_validated = bool(
            gate.get("strict_adaptive_quadrature_converged", False)
        )
        converged = bool(
            gate["fixed_event_crossed_integral_converged"]
            and strict_adaptive_validated
        )
        kernel_output = run_directory / "kernels" / f"{job['job_key']}.json"
        atomic_json(
            kernel_output,
            {
                "checkpoint_marker": MARKER,
                "config_digest": config["config_digest"],
                **job,
                "event": event,
                "argument": argument,
                "topology_file": str(topology_path),
                "fixed_event_integral_gate": gate,
                "strict_adaptive_validated": strict_adaptive_validated,
                "profile_audit": profile_audit,
                "valid_for_full_MTS_claim": False,
            },
        )
        result = {
            "checkpoint_marker": MARKER,
            "config_digest": config["config_digest"],
            **job,
            "seed": int(event["seed"]),
            "sample_index": int(event["sample_index"]),
            "status": "COMPLETED_CONVERGED"
            if converged
            else "COMPLETED_UNCONVERGED",
            "integral_converged": converged,
            "strict_adaptive_validated": strict_adaptive_validated,
            "topology_file": str(topology_path),
            "kernel_file": str(kernel_output),
            "normalized_direct_D_hhh_over_G3": M5036.complex_row(direct),
            "topology_runtime_seconds": topology_runtime,
            "kernel_runtime_seconds": kernel_runtime,
            "job_runtime_seconds": time.monotonic() - started,
            "profile_audit": profile_audit,
            "resumed_from_cache": False,
            "valid_for_full_MTS_claim": False,
        }
    except Exception as error:
        result = {
            "checkpoint_marker": MARKER,
            "config_digest": config["config_digest"],
            **job,
            "status": "FAILED",
            "error_type": type(error).__name__,
            "error": str(error),
            "job_runtime_seconds": time.monotonic() - started,
            "resumed_from_cache": False,
            "valid_for_full_MTS_claim": False,
        }
    atomic_json(output, result)
    return result


def dry_run(manifest: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    jobs = pilot_jobs(config, manifest)
    high_seeds = manifest["fresh_high_scramble_seeds"]
    low_seeds = manifest["fresh_low_scramble_seeds"]
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "dry_run": True,
        "config_digest": config["config_digest"],
        "high_unit_count": len(high_seeds),
        "low_unit_count": len(low_seeds),
        "expected_primary24_job_count": sum(
            job["profile"] == "primary24" for job in jobs
        ),
        "expected_coarse12_job_count": sum(
            job["profile"] == "coarse12" for job in jobs
        ),
        "expected_total_job_count": len(jobs),
        "expected_topology_count": 30 * len(high_seeds)
        + 15 * len(low_seeds),
        "expected_full_homotopy_anchor_count": len(high_seeds)
        + len(low_seeds),
        "expected_constructed_topology_count": 29 * len(high_seeds)
        + 14 * len(low_seeds),
        "default_enabled": False,
        "fresh_execution_started": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(DRY_RUN_JSON, result)
    return result


def smoke_jobs(config: dict[str, Any], manifest: dict[str, Any]) -> list[dict[str, Any]]:
    seed = int(manifest["fresh_high_scramble_seeds"][0])
    event = next(row for row in config["events"] if int(row["seed"]) == seed)
    rows = []
    for epsilon_id in ("E040", "E020"):
        for base_id in SMOKE_BASE_IDS:
            rows.append(
                {
                    "job_key": f"{epsilon_id}__{event['event_id']}__{base_id}__primary24",
                    "profile": "primary24",
                    "epsilon_id": epsilon_id,
                    "event_id": event["event_id"],
                    "base_argument_id": base_id,
                }
            )
    for base_id in SMOKE_BASE_IDS:
        rows.append(
            {
                "job_key": f"E040__{event['event_id']}__{base_id}__coarse12",
                "profile": "coarse12",
                "epsilon_id": "E040",
                "event_id": event["event_id"],
                "base_argument_id": base_id,
            }
        )
    return rows


def run_smoke(
    manifest: dict[str, Any], config: dict[str, Any], run_id: str
) -> dict[str, Any]:
    run_directory = RUNS / run_id
    run_directory.mkdir(parents=True, exist_ok=True)
    config_path = run_directory / "config.json"
    if config_path.exists():
        existing = json.loads(config_path.read_text(encoding="utf-8"))
        if existing["config_digest"] != config["config_digest"]:
            raise RuntimeError("smoke config changed; use a new run id")
    else:
        atomic_json(config_path, config)
    install_history_invariant_breakpoints(M5036.N5030)
    install_history_invariant_breakpoints(M5043.N5030)
    manager = CentralTopologyManager(run_directory, config)
    jobs = smoke_jobs(config, manifest)
    smoke_result_path = run_directory / "smoke_result.json"
    previous_result = (
        json.loads(smoke_result_path.read_text(encoding="utf-8"))
        if smoke_result_path.exists()
        else {}
    )
    rows = []
    started = time.monotonic()
    for job in jobs:
        row = execute_kernel(run_directory, config, manager, job)
        rows.append(row)
        print(
            json.dumps(
                {
                    "job": job["job_key"],
                    "status": row["status"],
                    "seconds": row["job_runtime_seconds"],
                    "resumed": row["resumed_from_cache"],
                }
            ),
            flush=True,
        )
    elapsed = time.monotonic() - started
    executed_count = sum(not row["resumed_from_cache"] for row in rows)
    resumed_count = sum(row["resumed_from_cache"] for row in rows)
    cumulative_fresh = int(
        previous_result.get("cumulative_fresh_job_count", 0)
    ) + executed_count
    cumulative_resumed = int(
        previous_result.get("cumulative_resumed_job_count", 0)
    ) + resumed_count
    first_execution_elapsed = previous_result.get(
        "first_execution_elapsed_seconds"
    )
    if first_execution_elapsed is None and executed_count:
        first_execution_elapsed = elapsed
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "run_id": run_id,
        "job_count": len(rows),
        "completed_converged_count": sum(
            row["status"] == "COMPLETED_CONVERGED" for row in rows
        ),
        "failed_count": sum(row["status"] == "FAILED" for row in rows),
        "invocation_elapsed_seconds": elapsed,
        "first_execution_elapsed_seconds": first_execution_elapsed,
        "recorded_job_runtime_seconds": sum(
            float(row["job_runtime_seconds"]) for row in rows
        ),
        "executed_job_count": executed_count,
        "resumed_job_count": resumed_count,
        "cumulative_fresh_job_count": cumulative_fresh,
        "cumulative_resumed_job_count": cumulative_resumed,
        "resume_contract_exercised": cumulative_resumed >= len(rows),
        "anchor_full_topology_exercised": any(
            row["epsilon_id"] == "E040"
            and row["base_argument_id"] == ANCHOR_ID
            for row in rows
        ),
        "argument_composition_exercised": any(
            row["base_argument_id"] == "A09" for row in rows
        ),
        "epsilon_composition_exercised": any(
            row["epsilon_id"] == "E020" for row in rows
        ),
        "primary24_exercised": any(
            row["profile"] == "primary24" for row in rows
        ),
        "coarse12_exercised": any(
            row["profile"] == "coarse12" for row in rows
        ),
        "runner_integration_smoke_passed": len(rows) == 6
        and all(row["status"] == "COMPLETED_CONVERGED" for row in rows),
        "full_pilot_execution_authorized": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(smoke_result_path, result)
    return result


def write_gate(
    manifest: dict[str, Any], dry: dict[str, Any], smoke: dict[str, Any] | None
) -> dict[str, Any]:
    smoke_passed = bool(smoke and smoke["runner_integration_smoke_passed"])
    resume_exercised = bool(smoke and smoke["resume_contract_exercised"])
    integration_complete = smoke_passed and resume_exercised
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "manifest_path": str(MANIFEST),
        "manifest_locked": bool(manifest["statistical_design_locked"]),
        "dry_run_passed": dry["expected_total_job_count"] == 360
        and dry["expected_full_homotopy_anchor_count"] == 16
        and dry["expected_constructed_topology_count"] == 284,
        "integration_smoke_run": smoke is not None,
        "integration_smoke_passed": smoke_passed,
        "resume_contract_exercised": resume_exercised,
        "runner_integration_complete": integration_complete,
        "full_pilot_execution_authorized": False,
        "default_enabled": False,
        "next_required_gate": "review the smoke and explicitly activate a bounded resumable pilot invocation"
        if integration_complete
        else "repeat the smoke once to exercise cache resume"
        if smoke_passed
        else "run the six-job integration smoke",
        "formalization_workbench_tree_sha256": FORMAL_BASELINE,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        (
            "source_paths_exist",
            all(
                path.exists()
                for path in (
                    SCRIPT_5036,
                    SCRIPT_5043,
                    SCRIPT_5045,
                    SCRIPT_5069,
                    SCRIPT_5084,
                    SCRIPT_5085,
                    SCRIPT_5086,
                    SCRIPT_5088,
                    SCRIPT_5091,
                    SCRIPT_5095,
                    SCRIPT_5112,
                    SCRIPT_5113,
                    SCRIPT_5114,
                    SCRIPT_5115,
                    SCRIPT_5117,
                    SCRIPT_5119,
                    LOCAL_ZERO_CERTIFICATE,
                    RECOIL_THEOREM_GATE,
                    RECOIL_SCOPE_CORRECTION_GATE,
                    RECOIL_ZERO_REGISTRY_V1,
                    RECOIL_ZERO_REGISTRY_V2_GATE,
                    RECOIL_ZERO_REGISTRY_V2,
                    RECOIL_ZERO_REGISTRY_GATE,
                    RECOIL_ZERO_REGISTRY,
                    GENERAL_DIRECT_CLASSIFIER_GATE,
                    REMOVABLE_EXTENSION_GATE,
                    OUTWARD_CONTOUR_GATE,
                    DOUBLE_ZERO_COLLISION_GATE,
                    MULTI_DOUBLE_ZERO_COLLISION_GATE,
                    SAME_SIDE_CLUSTER_CYCLE_GATE,
                    SAME_SIDE_CLUSTER_E020_GATE,
                    E020_PROJECTIVE_CLUSTER_GATE,
                    MANIFEST,
                )
            ),
            "runner, rejected 5084 provenance, 5112 event-local recoil registry, exact collision guards, contour gates, topology constructor, and manifest exist",
        ),
        ("manifest_locked", result["manifest_locked"], "5076 statistical manifest is locked"),
        ("dry_run_counts", result["dry_run_passed"], f"jobs={dry['expected_total_job_count']}; full anchors={dry['expected_full_homotopy_anchor_count']}; constructed={dry['expected_constructed_topology_count']}"),
        ("default_off", not result["default_enabled"], "runner requires explicit --mode smoke or future activation"),
        ("integration_state_consistent", result["runner_integration_complete"] == (result["integration_smoke_passed"] and result["resume_contract_exercised"]), f"smoke={result['integration_smoke_passed']}; resume={result['resume_contract_exercised']}"),
        ("full_execution_blocked", not result["full_pilot_execution_authorized"], "5077 never launches the full pilot"),
        ("formalization_unchanged", result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE, result["formalization_workbench_tree_sha256"]),
        ("claim_discipline", not result["valid_for_full_MTS_claim"], "runner validation is not physical evidence"),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check_id", "passed", "detail", "checkpoint_marker"))
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow(
                {
                    "check_id": f"V5077_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5077 validation failed: {failed}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("dry-run", "smoke"), default="dry-run")
    parser.add_argument("--run-id", default="central_anchor_integration_smoke_v3")
    arguments = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    config = make_config(manifest, arguments.run_id)
    dry = dry_run(manifest, config)
    smoke = (
        run_smoke(manifest, config, arguments.run_id)
        if arguments.mode == "smoke"
        else None
    )
    result = write_gate(manifest, dry, smoke)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
