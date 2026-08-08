from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1339"
TITLE = "1339-Y5-R10-RAB-source-closure-to-EH-left-hand-local-GR-reduction-gate"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
SOURCE_CLOSURE_IMPORT_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_CLOSURE_IMPORT.csv"
EH_LEFT_HAND_GATE_PATH = OUT_DIR / f"{PACK_ID}_EH_LEFT_HAND_REDUCTION_GATE.csv"
LOVELOCK_CONDITIONAL_PATH = OUT_DIR / f"{PACK_ID}_LOVELOCK_CONDITIONAL_THEOREM.csv"
R11_RESIDUAL_VECTOR_PATH = OUT_DIR / f"{PACK_ID}_R11_RESIDUAL_VECTOR_INTERFACE.csv"
NEWTON_TRANSFER_PATH = OUT_DIR / f"{PACK_ID}_NEWTON_TRANSFER_BLOCKERS.csv"
PPN_COMPLETION_PATH = OUT_DIR / f"{PACK_ID}_PPN_COMPLETION_GATE.csv"
RUNNER_UPDATE_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_UPDATE.csv"
ANTI_SHORTCUT_PATH = OUT_DIR / f"{PACK_ID}_ANTI_SHORTCUT_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1339_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def bool_false(value: object) -> bool:
    return str(value).strip().lower() == "false"


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    for table in tables:
        for row in table:
            if "valid_for_claim" in row and not bool_false(row.get("valid_for_claim", False)):
                return False
            if "claim_allowed" in row and not bool_false(row.get("claim_allowed", False)):
                return False
    return True


def generated_inside_formalization() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [path for path in FORMALIZATION.rglob("*1339*") if path.is_file()]


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1339_0_1338_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1338_NEXT_TARGET.csv",
            "needle": "NEXT1338_0_1339",
            "role": "selected 1339 target",
        },
        {
            "source_id": "SRC1339_1_1338_closure",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1338_NO_SOURCE_SLOT_CLOSURE_CONDITION.csv",
            "needle": "CLOS1338_2_no_source_only_species_slot",
            "role": "explicit source-side closure condition",
        },
        {
            "source_id": "SRC1339_2_1338_local_GR_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1338_LOCAL_GR_BRANCH_CONTRACT.csv",
            "needle": "LGRCON1338_1_geometric_left_hand",
            "role": "local-GR branch contract",
        },
        {
            "source_id": "SRC1339_3_1338_validation",
            "local_path": "source-intake/mts_residuals/P8_Y5_BRR545_1338_VALIDATION.csv",
            "needle": "VAL1338_11_overall",
            "role": "1338 pass gate",
        },
        {
            "source_id": "SRC1339_4_956_left_hand",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_956_LEFT_HAND_EH_NEWTON_GATE_MAP.csv",
            "needle": "LHG956_0_EH_core_selection",
            "role": "prior EH/Newton left-hand gate map",
        },
        {
            "source_id": "SRC1339_5_956_equation_spine",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_956_REDUCTION_EQUATION_SPINE.csv",
            "needle": "REQ956_1_left_hand_residual_split",
            "role": "local equation residual split",
        },
        {
            "source_id": "SRC1339_6_957_spine",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_957_PARENT_LOCAL_GR_SPINE_LEDGER.csv",
            "needle": "PLG957_2_EH_operator",
            "role": "parent local-GR spine ledger",
        },
        {
            "source_id": "SRC1339_7_957_ordering",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_957_DEPENDENCY_ORDERING.csv",
            "needle": "ORD957_1",
            "role": "local-GR dependency ordering",
        },
        {
            "source_id": "SRC1339_8_958_EH_selection",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_958_EH_CORE_SELECTION_ATTEMPT.csv",
            "needle": "EH958_5_verdict",
            "role": "EH-core selection attempt",
        },
        {
            "source_id": "SRC1339_9_958_premises",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_958_EH_PREMISE_AUDIT.csv",
            "needle": "EHP958_P6_second_order",
            "role": "EH premise audit",
        },
        {
            "source_id": "SRC1339_10_958_R11",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_958_R11_OPERATOR_FAMILY_PRIORITY.csv",
            "needle": "R11PRI958_1",
            "role": "R11 operator family priorities",
        },
        {
            "source_id": "SRC1339_11_959_no_extra",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_959_NO_EXTRA_FIELD_CLAUSE_ATTEMPT.csv",
            "needle": "NEF959_5_verdict",
            "role": "no-extra-field clause attempt",
        },
        {
            "source_id": "SRC1339_12_960_R2FR",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_960_R2_FR_ZERO_OR_BOUND_ATTEMPT.csv",
            "needle": "R2FR960_4_verdict",
            "role": "R2/fR zero-or-bound attempt",
        },
        {
            "source_id": "SRC1339_13_963_derivative",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_963_DERIVATIVE_ORDER_AUDIT.csv",
            "needle": "DO963_6_verdict",
            "role": "derivative-order audit",
        },
        {
            "source_id": "SRC1339_14_964_minimality",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_964_MINIMALITY_THEOREM_ATTEMPT.csv",
            "needle": "MIN964_5_verdict",
            "role": "no-higher-derivative minimality attempt",
        },
        {
            "source_id": "SRC1339_15_965_quotient",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_965_PRIMITIVE_QUOTIENT_THEOREM_ATTEMPT.csv",
            "needle": "PQ965_5_verdict",
            "role": "primitive quotient/no-marker theorem attempt",
        },
    ]
    source_register = []
    for spec in source_specs:
        exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "exists": exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    source_closure_import = [
        {
            "import_id": "SCIMP1339_0_source_side",
            "imported_condition": "NoSourceOnlySpeciesSlot plus observed-frame/single-measure/readout-after-variation closure",
            "source": "CLOS1338_0 through CLOS1338_5",
            "status": "EXPLICIT_CLOSURE_NOT_DERIVED",
            "use_in_1339": "right-hand/source side can be treated as a labelled conditional branch only",
            "blocks_claim": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "import_id": "SCIMP1339_1_finite_residual",
            "imported_condition": "if source closure is not adopted, w_A/source/readout residuals remain live",
            "source": "P8_Y5_R10_1338_LIVE_COUNTERMODEL_BOUNDARIES.csv",
            "status": "RETAINED_FALLBACK_BRANCH",
            "use_in_1339": "prevents EH-left-hand algebra from becoming a full local-GR claim",
            "blocks_claim": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    eh_left_hand_gate = [
        {
            "gate_id": "EHGate1339_0_observed_frame",
            "required_condition": "one observed metric/coframe used by matter, source, photons, clocks, and orbital/PPN readout",
            "mathematical_form": "g_obs,e_obs are quotient-owned and common to all local observable maps",
            "current_status": "SOURCE_CLOSURE_LABELLED_NOT_FULL_PPN_SIGNED",
            "if_passes": "same-frame comparison becomes meaningful",
            "if_fails": "frame/readout residual vector remains",
            "blocks_claim": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "EHGate1339_1_metric_only_local_4D",
            "required_condition": "compact local exterior action is local, 4D, diffeo-invariant, metric-only",
            "mathematical_form": "S_ext[g_obs]=int sqrt(-g) L(g,Riemann,nabla Riemann,...) before restrictions",
            "current_status": "NOT_PARENT_DERIVED",
            "if_passes": "Lovelock/second-order selection route can be applied",
            "if_fails": "extra fields/nonlocal operators enter R11 vector",
            "blocks_claim": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "EHGate1339_2_second_order",
            "required_condition": "metric field equations are second order through tested local scales",
            "mathematical_form": "delta S_ext/delta g contains no R2/fR/Ricci2/Weyl2/nonlocal higher-derivative residual",
            "current_status": "CENTRAL_BLOCKER_NOT_DERIVED",
            "if_passes": "EH+Lambda selected by Lovelock-style theorem",
            "if_fails": "R2/fR and curvature-square residuals remain",
            "blocks_claim": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "EHGate1339_3_Levi_Civita",
            "required_condition": "observed connection is Levi-Civita and universally used",
            "mathematical_form": "Gamma_obs = LC(g_obs), T^rho_munu=0, Q_rho_munu=0 or retained",
            "current_status": "NOT_PARENT_DERIVED",
            "if_passes": "torsion/nonmetricity R11 family can close",
            "if_fails": "WEP/clock/light/spin/source connection residuals remain",
            "blocks_claim": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "EHGate1339_4_extra_sector_silence",
            "required_condition": "motion/time/domain/memory/projector/boundary sectors carry no independent exterior stress/charge",
            "mathematical_form": "DeltaE_extra_i in {0,gauge,topological_no_flux,positive_source_free_silent,bounded_residual}",
            "current_status": "ACTIVE_PRIMARY_OBSTRUCTION",
            "if_passes": "EH exterior can be one-parameter up to source charge",
            "if_fails": "R11/q_loc/domain/boundary/memory vector remains",
            "blocks_claim": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "EHGate1339_5_boundary_harmless",
            "required_condition": "boundary/topological terms have no local stress, flux, radial, shear, or preferred-location hair",
            "mathematical_form": "delta S_boundary/delta g local = 0 and Hamiltonian flux at local boundary is harmless",
            "current_status": "CONDITIONAL_NOT_DERIVED",
            "if_passes": "boundary/topological R11 branch can close",
            "if_fails": "gamma/beta/alpha3/xi/Gdot/source-mass residuals remain",
            "blocks_claim": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "EHGate1339_6_source_GM_transfer",
            "required_condition": "EH mass parameter equals Hilbert/worldtube source charge and measured orbital GM",
            "mathematical_form": "mu_EH = G_ref M_H[worldtube] = GM_orbital/c^2",
            "current_status": "NOT_DERIVED",
            "if_passes": "Newtonian mechanics reduction can be attempted",
            "if_fails": "Poisson-looking algebra cannot be identified with measured Newtonian gravity",
            "blocks_claim": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    lovelock_conditional = [
        {
            "theorem_id": "LOV1339_0_conditional_EH_selection",
            "statement": "If the local exterior branch is 4D, local, diffeomorphism-invariant, metric-only, Levi-Civita, second-order, and boundary-harmless, the left-hand operator reduces to EH+Lambda up to normalization.",
            "mathematical_result": "E_munu = a G_munu + b g_munu",
            "proof_status": "MATHEMATICAL_CONDITIONAL_CLEAN",
            "missing_for_MTS": "MTS has not parent-derived the premises",
            "claim_result": "EH_BASELINE_AVAILABLE_ONLY_AS_CONDITIONAL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "LOV1339_1_weak_field_algebra",
            "statement": "If EH+source closure+GM calibration hold, the leading weak-field equation has the Newton/Poisson form.",
            "mathematical_result": "nabla^2 Phi = 4 pi G_eff rho_obs",
            "proof_status": "ALGEBRA_CONDITIONAL_CLEAN",
            "missing_for_MTS": "source closure is explicit not derived; GM calibration and PPN completion remain open",
            "claim_result": "NO_NEWTON_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    r11_residual_vector = [
        {
            "residual_id": "R11V1339_0_R2_fR_scalar",
            "family": "R2/fR scalar mode",
            "coefficient": "c_R2_or_c_fR",
            "affected_tests": "PPN gamma/beta, finite range R10, scalar fifth force",
            "zero_requirement": "parent second-order/no-extra-scalar theorem",
            "bound_requirement": "coefficient units, scalar mass/coupling, alpha(lambda)/PPN map, source path",
            "current_status": "ZERO_OR_BOUND_MISSING",
            "priority": "highest_first",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "R11V1339_1_torsion_nonmetricity",
            "family": "torsion/nonmetricity/independent connection",
            "coefficient": "c_T_or_c_Q",
            "affected_tests": "WEP, clocks, light cones, spin, source charge, PPN",
            "zero_requirement": "Levi-Civita connection theorem",
            "bound_requirement": "connection coefficient units and weak-field/readout map",
            "current_status": "ZERO_OR_BOUND_MISSING",
            "priority": "highest_first",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "R11V1339_2_boundary_topological",
            "family": "boundary/topological terms",
            "coefficient": "c_boundary_or_c_GB",
            "affected_tests": "mass charge, gamma, beta, alpha3, xi, Gdot",
            "zero_requirement": "boundary no-hair/no-flux theorem",
            "bound_requirement": "boundary weak-field map and source-backed residual bound",
            "current_status": "ZERO_OR_BOUND_MISSING",
            "priority": "high",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "R11V1339_3_vector_preferred_frame",
            "family": "vector/preferred-frame/domain selector",
            "coefficient": "epsilon_domain_vector",
            "affected_tests": "alpha1, alpha2, alpha3, xi, orbital anisotropy",
            "zero_requirement": "no preferred-frame/domain vector theorem",
            "bound_requirement": "PPN preferred-frame coefficient map",
            "current_status": "ZERO_OR_BOUND_MISSING",
            "priority": "high",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "R11V1339_4_memory_nonlocal_kernel",
            "family": "nonlocal memory kernel",
            "coefficient": "c_nonlocal_or_K_norm",
            "affected_tests": "Gdot, alpha3, finite range, cosmology/local split",
            "zero_requirement": "local-vacuum memory silence theorem",
            "bound_requirement": "kernel norm, range/time map, source path",
            "current_status": "ZERO_OR_BOUND_MISSING",
            "priority": "medium",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "R11V1339_5_source_normalization_operator",
            "family": "source normalization/domain-projector operator",
            "coefficient": "c_domain_source_normalization_operator",
            "affected_tests": "measured GM, WEP source charge, Newton reduction",
            "zero_requirement": "source closure plus domain/projector stress silence",
            "bound_requirement": "GM/source-normalization weak-field map",
            "current_status": "ZERO_OR_BOUND_MISSING",
            "priority": "high",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    newton_transfer = [
        {
            "blocker_id": "NEW1339_0_EH_operator",
            "needed_for_Newton": "EH+Lambda or bounded weak-field operator",
            "current_status": "CONDITIONAL_ONLY",
            "why_blocks": "Poisson coefficient algebra cannot start from unknown left-hand operator",
            "next_resolution": "derive EH premises or retain R11 residual vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "NEW1339_1_source_closure",
            "needed_for_Newton": "source side equals common calibrated Hilbert T_total",
            "current_status": "EXPLICIT_CLOSURE_NOT_DERIVED",
            "why_blocks": "composition/source weights can alter rho_obs",
            "next_resolution": "derive source closure or keep finite source residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "NEW1339_2_GM_calibration",
            "needed_for_Newton": "exterior mass parameter equals measured orbital GM",
            "current_status": "NOT_DERIVED",
            "why_blocks": "EH-looking equation is not measured Newtonian mechanics without charge transfer",
            "next_resolution": "Noether/Hamiltonian/worldtube/Gauss calibration theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    ppn_completion = [
        {
            "ppn_id": "PPN1339_0_gamma_beta",
            "component": "gamma-1, beta-1",
            "required_status_for_claim": "zero theorem or source-backed residual bound",
            "current_status": "NOT_FILLED",
            "blocks_full_local_GR": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "ppn_id": "PPN1339_1_preferred_frame",
            "component": "alpha1, alpha2, alpha3, xi",
            "required_status_for_claim": "no-vector/no-domain/no-boundary theorem or bound",
            "current_status": "NOT_FILLED",
            "blocks_full_local_GR": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "ppn_id": "PPN1339_2_time_range",
            "component": "Gdot/G, finite-range terms, local memory drift",
            "required_status_for_claim": "local-vacuum silence theorem or bound",
            "current_status": "NOT_FILLED",
            "blocks_full_local_GR": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "ppn_id": "PPN1339_3_readout_frame",
            "component": "clock/light/orbital readout frame consistency",
            "required_status_for_claim": "same-frame readout to O(U^2)",
            "current_status": "NOT_FILLED",
            "blocks_full_local_GR": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_update = [
        {
            "runner_id": "RUN1339_0_EH_left_hand_gate",
            "target": "EH/Newton left-hand local-GR reduction gate",
            "input_status": "GATE_DECOMPOSED",
            "runner_status": "CONDITIONAL_EH_ROUTE_NOT_CLAIMED",
            "score_ready": False,
            "reason": "metric-only/second-order/no-extra-field/LC/source-GM/PPN gates remain open",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1339_1_R11_vector_interface",
            "target": "retained non-EH residual vector",
            "input_status": "INTERFACE_WRITTEN_MISSING_COEFFICIENTS",
            "runner_status": "NONCLAIM_RESIDUAL_ROUTE_READY",
            "score_ready": False,
            "reason": "residual families are identified but zero certificates or source-backed bounds are missing",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    anti_shortcut = [
        {
            "gate_id": "SHORT1339_0_no_source_closure_as_full_GR",
            "shortcut": "use source-side closure as a full local-GR proof",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1339_1_no_Lovelock_without_premises",
            "shortcut": "invoke Lovelock/EH before metric-only second-order premises are parent-signed",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1339_2_no_Newton_from_Poisson_shape_only",
            "shortcut": "claim Newtonian mechanics from Poisson-looking algebra without measured-GM transfer",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1339_3_no_PPN_claim_without_vector",
            "shortcut": "claim local GR before every PPN/readout residual is zeroed or bounded",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1339_0_EH_status",
            "decision": "EH/Newton left-hand route is clean as a conditional theorem but not derived for MTS yet",
            "because": "metric-only, second-order, no-extra-sector, Levi-Civita, boundary-harmless, GM-transfer, and PPN-completion gates remain open",
            "effect": "no local-GR/Newton claim; proceed by deriving or bounding the R11 residual vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1339_1_next_route",
            "decision": "prioritize the first executable EH-core/R11 interface rather than re-auditing the same blockers",
            "because": "the residual families are now named and can be turned into zero-or-bound rows",
            "effect": "next target should either derive metric-only second-order EH selection or build the first R11 coefficient interface",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1339_0_1340",
            "target_file": "1340-Y5-R10-RAB-EH-core-selection-or-first-executable-R11-residual-interface.md",
            "target_script": "scripts/Y5_R10_RAB_EH_core_selection_or_first_executable_R11_residual_interface.py",
            "task": "try to derive the metric-only second-order EH core; if not, create the first executable nonclaim R11 residual interface for R2/fR and torsion/nonmetricity",
            "success_condition": "either EH core premises become parent-signed, or the highest-priority residual families get explicit coefficient/unit/weak-field-map/source requirements",
            "do_not": "do not claim local GR/Newton, do not invoke Lovelock without premises, do not drop source closure labels",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    tables_for_nonclaim = [
        source_register,
        source_closure_import,
        eh_left_hand_gate,
        lovelock_conditional,
        r11_residual_vector,
        newton_transfer,
        ppn_completion,
        runner_update,
        anti_shortcut,
        decision,
        next_target,
    ]

    source_anchor_count = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    source_closure_labelled = all(row["blocks_claim"] is True for row in source_closure_import)
    all_eh_gates_block = all(row["blocks_claim"] is True for row in eh_left_hand_gate)
    lovelock_conditional_only = all(str(row["claim_result"]).startswith(("EH_BASELINE", "NO_NEWTON")) for row in lovelock_conditional)
    r11_interface_missing = all(row["current_status"] == "ZERO_OR_BOUND_MISSING" for row in r11_residual_vector)
    newton_blocked = all(row["valid_for_claim"] is False for row in newton_transfer)
    ppn_blocked = all(row["blocks_full_local_GR"] is True for row in ppn_completion)
    runners_not_scoreable = all(row["score_ready"] is False and row["valid_prediction_row"] is False for row in runner_update)
    shortcuts_enforced = all(row["status"] == "ENFORCED" for row in anti_shortcut)
    nonclaim = all_nonclaim(tables_for_nonclaim)
    formal_clean = len(generated_inside_formalization()) == 0
    next_is_1340 = next_target[0]["target_file"].startswith("1340-")

    validations = [
        validation_row(
            "VAL1339_0_sources_exist",
            "registered local source paths exist and anchors are found",
            source_anchor_count == len(source_register),
            f"{source_anchor_count}/{len(source_register)} source anchors found",
        ),
        validation_row(
            "VAL1339_1_source_closure_labelled",
            "source-side closure is imported only as claim-blocking closure",
            source_closure_labelled,
            ";".join(f"{row['import_id']}={row['status']}" for row in source_closure_import),
        ),
        validation_row(
            "VAL1339_2_EH_gates_block",
            "EH-left-hand gates remain blockers until parent-signed",
            all_eh_gates_block,
            ";".join(f"{row['gate_id']}={row['current_status']}" for row in eh_left_hand_gate),
        ),
        validation_row(
            "VAL1339_3_lovelock_conditional_only",
            "Lovelock/EH route remains conditional only",
            lovelock_conditional_only,
            ";".join(f"{row['theorem_id']}={row['proof_status']}" for row in lovelock_conditional),
        ),
        validation_row(
            "VAL1339_4_R11_interface_missing",
            "R11 residual families are identified but zero/bound inputs remain missing",
            r11_interface_missing,
            ";".join(f"{row['residual_id']}={row['current_status']}" for row in r11_residual_vector),
        ),
        validation_row(
            "VAL1339_5_Newton_blocked",
            "Newtonian mechanics transfer remains blocked",
            newton_blocked,
            ";".join(f"{row['blocker_id']}={row['current_status']}" for row in newton_transfer),
        ),
        validation_row(
            "VAL1339_6_PPN_blocked",
            "PPN/full local-GR completion remains blocked",
            ppn_blocked,
            ";".join(f"{row['ppn_id']}={row['current_status']}" for row in ppn_completion),
        ),
        validation_row(
            "VAL1339_7_runners_not_scoreable",
            "runners refuse local-GR/Newton scoring",
            runners_not_scoreable,
            ";".join(f"{row['runner_id']}={row['runner_status']}" for row in runner_update),
        ),
        validation_row(
            "VAL1339_8_shortcuts_enforced",
            "anti-shortcut gates are enforced",
            shortcuts_enforced,
            ";".join(row["gate_id"] for row in anti_shortcut),
        ),
        validation_row(
            "VAL1339_9_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim,
            "valid_for_claim=false and claim_allowed=false where present",
        ),
        validation_row(
            "VAL1339_10_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            formal_clean,
            f"formalization_generated_output_count={len(generated_inside_formalization())}",
        ),
        validation_row(
            "VAL1339_11_next_target_1340",
            "next target routes to EH core selection or first executable R11 residual interface",
            next_is_1340,
            str(next_target[0]["target_file"]),
        ),
    ]
    validations.append(
        validation_row(
            "VAL1339_12_overall",
            "overall 1339 validation",
            all(row["status"] == "PASS" for row in validations),
            "1339 separates source closure, EH-left-hand conditional route, Newton transfer, PPN completion, and retained R11 residual vector without local-GR claims",
        )
    )

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(SOURCE_CLOSURE_IMPORT_PATH, source_closure_import)
    write_csv(EH_LEFT_HAND_GATE_PATH, eh_left_hand_gate)
    write_csv(LOVELOCK_CONDITIONAL_PATH, lovelock_conditional)
    write_csv(R11_RESIDUAL_VECTOR_PATH, r11_residual_vector)
    write_csv(NEWTON_TRANSFER_PATH, newton_transfer)
    write_csv(PPN_COMPLETION_PATH, ppn_completion)
    write_csv(RUNNER_UPDATE_PATH, runner_update)
    write_csv(ANTI_SHORTCUT_PATH, anti_shortcut)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# {TITLE}

**Current verdict:** 1339 does not claim local GR or Newtonian mechanics. It cleanly separates the source-side closure from the geometric left-hand problem and shows the EH/Newton route is still conditional.

**Main progress:** the path to GR is now sharper: source closure handles the right-hand/source problem, while the left-hand side needs metric-only, local 4D, second-order, Levi-Civita, no-extra-sector, boundary-harmless, GM-transfer, and PPN-completion gates. If these pass, EH+Lambda and the Newton/Poisson limit follow cleanly; they do not pass yet.

**Decision:** proceed to `1340`: either derive the EH core premises or turn the highest-priority non-EH families into executable nonclaim residual interfaces.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Source Closure Import
{markdown_table(source_closure_import, ["import_id", "imported_condition", "source", "status", "use_in_1339", "blocks_claim", "valid_for_claim", "claim_allowed"])}

## EH Left-Hand Reduction Gate
{markdown_table(eh_left_hand_gate, ["gate_id", "required_condition", "mathematical_form", "current_status", "if_passes", "if_fails", "blocks_claim", "valid_for_claim", "claim_allowed"])}

## Lovelock Conditional Theorem
{markdown_table(lovelock_conditional, ["theorem_id", "statement", "mathematical_result", "proof_status", "missing_for_MTS", "claim_result", "valid_for_claim", "claim_allowed"])}

## R11 Residual Vector Interface
{markdown_table(r11_residual_vector, ["residual_id", "family", "coefficient", "affected_tests", "zero_requirement", "bound_requirement", "current_status", "priority", "valid_for_claim", "claim_allowed"])}

## Newton Transfer Blockers
{markdown_table(newton_transfer, ["blocker_id", "needed_for_Newton", "current_status", "why_blocks", "next_resolution", "valid_for_claim", "claim_allowed"])}

## PPN Completion Gate
{markdown_table(ppn_completion, ["ppn_id", "component", "required_status_for_claim", "current_status", "blocks_full_local_GR", "valid_for_claim", "claim_allowed"])}

## Runner Update
{markdown_table(runner_update, ["runner_id", "target", "input_status", "runner_status", "score_ready", "reason", "valid_prediction_row", "valid_for_claim", "claim_allowed"])}

## Anti-Shortcut Gates
{markdown_table(anti_shortcut, ["gate_id", "shortcut", "enforcement", "status", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decision, ["decision_id", "decision", "because", "effect", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
