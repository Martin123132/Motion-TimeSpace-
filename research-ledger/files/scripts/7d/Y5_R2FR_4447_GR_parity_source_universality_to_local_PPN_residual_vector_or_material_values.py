from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from ppn_source_universality_gate import (  # noqa: E402
    evaluate_material_rows,
    evaluate_ppn_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4447"
CLAIM_ID = "L-289"
MARKER = "PPC4161_GR_PARITY_SOURCE_UNIVERSALITY_TO_LOCAL_PPN_RESIDUAL_VECTOR_4447"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_UNIVERSALITY_PPN_SUBVECTOR_4447"
DECISION = "SOURCE_UNIVERSALITY_PIECES_PROPAGATED_TO_PPN_VECTOR_PRIVATE_BRANCH_NON_SOURCE_RESIDUALS_AND_MATERIAL_VALUES_REMAIN_NONCLAIM"
NEXT_TARGET = "4448-Y5-R2FR-non-source-PPN-residual-survivor-map-or-first-material-Req-value.md"

FORMAL_PATH = FORMAL / "463-PPC4161-GR-parity-source-universality-to-local-PPN-residual-vector-or-material-values.md"
DOC_PATH = POST / "4447-Y5-R2FR-GR-parity-source-universality-to-local-PPN-residual-vector-or-material-values.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4447_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4447_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4447_DERIVATION_ROWS.csv"
PPN_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4447_PPN_SOURCE_RESIDUAL_INPUT.csv"
PPN_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4447_PPN_SOURCE_RESIDUAL_OUTPUT.csv"
MATERIAL_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4447_MATERIAL_REQ_INPUT.csv"
MATERIAL_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4447_MATERIAL_REQ_OUTPUT.csv"
RESIDUAL_ROLLUP = SOURCE_DIR / "P8_Y5_R2FR_4447_RESIDUAL_ROLLUP.csv"
REDUCTION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4447_REDUCTION_ROWS.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4447_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4447_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4447_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4447_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "ppn_source_universality_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4447_GR_parity_source_universality_to_local_PPN_residual_vector_or_material_values.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4446 = SOURCE_DIR / "P8_Y5_R2FR_4446_NEXT_TARGET.csv"
FORMAL_462 = FORMAL / "462-PPC4161-adopt-GR-parity-SM-import-or-source-backed-material-Req-value.md"
ADOPTION_OUTPUT_4446 = SOURCE_DIR / "P8_Y5_R2FR_4446_GR_PARITY_ADOPTION_OUTPUT.csv"
RESIDUAL_VECTOR_4446 = SOURCE_DIR / "P8_Y5_R2FR_4446_SOURCE_UNIVERSALITY_RESIDUAL_VECTOR.csv"
MATERIAL_OUTPUT_4446 = SOURCE_DIR / "P8_Y5_R2FR_4446_MATERIAL_REQ_OUTPUT.csv"
FORMAL_180 = FORMAL / "180-PPC4161-private-local-packet-integration.md"
FORMAL_185 = FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md"
FORMAL_187 = FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md"
FORMAL_188 = FORMAL / "188-PPC4161-full-PPN-readout-vector.md"
FORMAL_189 = FORMAL / "189-PPC4161-local-empirical-validation-pack.md"
FORMAL_190 = FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md"
FORMAL_222 = FORMAL / "222-PPC4161-calibrated-GN-bridge-and-source-charge-caveat.md"
MIN_RESIDUAL_VECTOR = SOURCE_DIR / "P8_MIN_PARENT_LOCAL_GR_RESIDUAL_VECTOR.csv"
DOMAIN_RESIDUAL_VECTOR = SOURCE_DIR / "P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv"
PROMOTION_GATES = SOURCE_DIR / "P8_LOCAL_GR_RESIDUAL_PROMOTION_GATES.csv"
BOUND_REGISTER = SOURCE_DIR / "P8_LOCAL_GR_RESIDUAL_BOUND_REGISTER.csv"
LOCAL_TEMPLATE = SOURCE_DIR / "MTS_local_residual_predictions_TEMPLATE.csv"
SOURCE_NORM_TEMPLATE = SOURCE_DIR / "P8_source_normalization_residual_vector_TEMPLATE.csv"
POST_4378 = POST / "4378-Y5-R2FR-transition-topological-profile-moment-zero-or-first-multipole-bound-row.md"


def text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def rows_from(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def source_specs() -> List[Dict[str, object]]:
    return [
        {"source_id": "SRC4447_00_next4446", "path": NEXT_4446, "needle": "4447-Y5-R2FR-GR-parity-source-universality-to-local-PPN-residual-vector-or-material-values.md", "role": "4446 handoff."},
        {"source_id": "SRC4447_01_formal462", "path": FORMAL_462, "needle": "Delta_w_A=0 becomes branch-internal", "role": "4446 private source-weight zero derivation."},
        {"source_id": "SRC4447_02_4446_adoption_output", "path": ADOPTION_OUTPUT_4446, "needle": "GR_PARITY_SM_IMPORT_PRIVATE_BRANCH_ADOPTED_NONCLAIM", "role": "machine-readable private adoption status."},
        {"source_id": "SRC4447_03_4446_residual_vector", "path": RESIDUAL_VECTOR_4446, "needle": "RU4446_0_Delta_w_A", "role": "source-universality residual vector input."},
        {"source_id": "SRC4447_04_4446_material_output", "path": MATERIAL_OUTPUT_4446, "needle": "MATERIAL_REQ_SOURCE_CANDIDATES_READY_VALUES_MISSING", "role": "material/R_eq values remain open."},
        {"source_id": "SRC4447_05_private_packet_ppn_gate", "path": FORMAL_180, "needle": "local PPN readout gate for `gamma`, `beta`, `alpha_i`, `xi`, `zeta_i`, and `Gdot/G`", "role": "PPN readout gate originally required."},
        {"source_id": "SRC4447_06_private_packet_no_weights", "path": FORMAL_180, "needle": "There are no independent source weights `w_A`", "role": "source weights absent in private packet."},
        {"source_id": "SRC4447_07_hilbert_measure", "path": FORMAL_185, "needle": "All ordinary local source sectors use the same observed metric/coframe and the same volume measure.", "role": "single Hilbert source measure."},
        {"source_id": "SRC4447_08_deltaZH_zero", "path": FORMAL_185, "needle": "delta_ZH = 0", "role": "source normalization drift zero inside private packet."},
        {"source_id": "SRC4447_09_newton_readout", "path": FORMAL_187, "needle": "Orbital data is now a test of the derived branch, not an input to it.", "role": "Newton/orbital anti-circularity guard."},
        {"source_id": "SRC4447_10_full_ppn_vector", "path": FORMAL_188, "needle": "R_PPN =", "role": "private PPN vector target."},
        {"source_id": "SRC4447_11_ppn_reactivation", "path": FORMAL_188, "needle": "the corresponding named PPN residual reopens", "role": "non-source residual reactivation rule."},
        {"source_id": "SRC4447_12_empirical_pack", "path": FORMAL_189, "needle": "R_PPN = 0,", "role": "private empirical prediction vector."},
        {"source_id": "SRC4447_13_quarantine", "path": FORMAL_190, "needle": "The named residual row reopens.", "role": "anti-smuggling quarantine rule."},
        {"source_id": "SRC4447_14_GN_bridge", "path": FORMAL_222, "needle": "MTS does not need to numerically predict G_N to reduce to GR/Newton.", "role": "G_N calibration caveat."},
        {"source_id": "SRC4447_15_poynting_danger", "path": FORMAL_222, "needle": "EM/Poynting Hilbert stress", "role": "EM/current source side-channel that remains next danger."},
        {"source_id": "SRC4447_16_min_vector", "path": MIN_RESIDUAL_VECTOR, "needle": "AR511_2_direct_matter_charge", "role": "minimum parent residual survivor list."},
        {"source_id": "SRC4447_17_domain_vector", "path": DOMAIN_RESIDUAL_VECTOR, "needle": "LRV_DOMAIN_R11_SOURCE_NORMALIZATION", "role": "domain/projector non-source residual survivor."},
        {"source_id": "SRC4447_18_promotion_gates", "path": PROMOTION_GATES, "needle": "G482_local_GR_vector", "role": "promotion gate still failing globally."},
        {"source_id": "SRC4447_19_bound_register", "path": BOUND_REGISTER, "needle": "LRV_DOMAIN_R11_SOURCE_NORMALIZATION", "role": "bound rows still unfilled."},
        {"source_id": "SRC4447_20_local_template", "path": LOCAL_TEMPLATE, "needle": "R3_gamma", "role": "local residual prediction template."},
        {"source_id": "SRC4447_21_source_norm_template", "path": SOURCE_NORM_TEMPLATE, "needle": "P8_species_source_charge", "role": "source-normalization residual template."},
        {"source_id": "SRC4447_22_req_fallback", "path": POST_4378, "needle": "HARMONIC_NULL_MOMENT_ZERO_THEOREM", "role": "R_eq/topological fallback precedent."},
        {"source_id": "SRC4447_23_gate", "path": GATE_PATH, "needle": "def evaluate_ppn_row", "role": "4447 PPN source-universality gate."},
        {"source_id": "SRC4447_24_generator", "path": GENERATOR_PATH, "needle": 'CHECKPOINT = "4447"', "role": "4447 generator script."},
    ]


def source_rows() -> List[Dict[str, object]]:
    rows = []
    for spec in source_specs():
        path = Path(spec["path"])
        needle = str(spec["needle"])
        line = line_of(path, needle)
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": spec["source_id"],
            "path": str(path),
            "path_exists": path.exists(),
            "needle": needle,
            "needle_found": line > 0,
            "line_number": line,
            "role": spec["role"],
            "valid_for_claim": False,
        })
    return rows


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "PPN4447_D0_source_subspace_projection",
            "claim": "4446 closes only the source-universality subspace of the local PPN residual vector.",
            "derivation": "The 4446 branch gives Delta_w_A=0 and material readout reentry=0 because matter/species/material labels have no morphism into the active source coefficient. Therefore any PPN residual component whose only live support is source weighting or material reentry has zero source-piece inside PPC4161.",
            "consequence": "WEP source-charge, source-normalization pieces of gamma/beta/Gdot, and source-split pieces of alpha/zeta/clock/orbital rows can be marked source-zero privately.",
            "status": "SOURCE_UNIVERSALITY_SUBSPACE_ZERO_PRIVATE_BRANCH",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "PPN4447_D1_no_full_vector_smuggling",
            "claim": "The same move does not erase non-source residuals.",
            "derivation": "The 188/190 reactivation rules say that if same-metric EH readout, no-vector/projector drift, no scalar/disformal bulk residual, Hilbert conservation, or boundary silence is rejected, the named residual row reopens. A source-weight zero cannot prove those separate clauses.",
            "consequence": "Domain/projector, boundary, memory drift, finite-range, scalar/disformal and EM/Poynting side channels remain explicit survivor rows.",
            "status": "NON_SOURCE_RESIDUALS_PRESERVED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "PPN4447_D2_GN_caveat",
            "claim": "MTS can still reduce to GR/Newton with calibrated universal G_N; it need not derive the numerical value of G_N at this gate.",
            "derivation": "The 222 bridge separates numerical prediction of G_N from the universal source-blind coupling requirement. 4447 therefore tests source universality, not a numeric G_N derivation.",
            "consequence": "The local branch remains serious if the coupling is constant and source-blind, but the public claim still needs non-source residual closure and empirical bound rows.",
            "status": "GN_NUMERIC_VALUE_NOT_REQUIRED_HERE",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "PPN4447_D3_material_values_still_open",
            "claim": "Material/R_eq values are not filled by source universality.",
            "derivation": "A material label cannot re-enter the active source coefficient inside the branch, but empirical WEP/clock/orbital rows still require material inventory conventions, projection coefficients, residual values and arena bounds.",
            "consequence": "4448 should either attack the survivor map for non-source PPN rows or source the first material/R_eq value.",
            "status": "MATERIAL_REQ_VALUES_REMAIN_OPEN",
            "valid_for_claim": False,
        },
    ]


def ppn_input_rows() -> List[Dict[str, object]]:
    base = {
        "private_branch_adopted": True,
        "delta_w_zero": True,
        "material_reentry_zero": True,
        "hilbert_source_single": True,
        "ppn_mapping_present": True,
        "source_piece_named": True,
        "non_source_residual_preserved": True,
        "public_claim_false": True,
        "source_piece_value": "0",
        "full_observable_claim": False,
        "input_valid_for_claim": False,
        "public_authority": False,
    }
    rows = [
        ("PPN4447_0_WEP_eta_source_charge", "WEP", "eta_AB", "composition/source-weight contribution to WEP eta", "material inventory values and direct matter-charge survivor rows remain empirical", FORMAL_185),
        ("PPN4447_1_gamma_minus_1_source_norm", "PPN", "gamma_minus_1", "source-normalization contribution to gamma-1", "metric principal block, scalar/disformal and domain-projector residuals remain separate", FORMAL_188),
        ("PPN4447_2_beta_minus_1_source_norm", "PPN", "beta_minus_1", "source-normalization contribution to beta-1", "EH self-interaction/nonlinear metric readout remains the non-source clause", FORMAL_188),
        ("PPN4447_3_alpha1_alpha2_source_frame", "PPN", "alpha1_alpha2", "species/source-frame contribution to preferred-frame parameters", "domain/projector vector residuals remain active until zeroed or bounded", FORMAL_188),
        ("PPN4447_4_alpha3_source_split", "PPN", "alpha3", "source-split contribution to alpha3", "boundary flux and domain-projector alpha3 rows remain active until zeroed or bounded", FORMAL_188),
        ("PPN4447_5_xi_zeta_source_nonconservation", "PPN", "xi_zeta_i", "source-weight contribution to anisotropy/nonconservation rows", "boundary/projector/Hilbert-conservation side channels remain separate", FORMAL_188),
        ("PPN4447_6_Gdot_over_G_source_drift", "local_drift", "Gdot_over_G", "source-measure/material-reentry contribution to local G drift", "memory/nonlocal kappa drift channels remain named survivor rows if parent clauses fail", FORMAL_185),
        ("PPN4447_7_clock_redshift_material_reentry", "clock", "redshift_alpha", "material-reentry contribution to clock redshift violation", "clock/Hodge/EM stress and material projection values remain empirical", FORMAL_189),
        ("PPN4447_8_orbital_GM_material_reentry", "orbital", "GM_source_charge", "material-reentry contribution to orbital measured source charge", "Hilbert charge to worldtube/orbital measured mass glue remains empirical", FORMAL_187),
    ]
    materialized = []
    for row_id, arena, observable, piece, survivors, source_path in rows:
        row = dict(base)
        row.update({
            "row_id": row_id,
            "arena": arena,
            "observable": observable,
            "residual_piece": piece,
            "source_path": str(source_path),
            "non_source_residuals": survivors,
            "notes": "Source-universality contribution only; no full observable/public PPN claim.",
        })
        materialized.append(row)
    public_control = dict(base)
    public_control.update({
        "row_id": "PPN4447_9_full_public_PPN_control",
        "arena": "PPN_public_control",
        "observable": "full_R_PPN",
        "residual_piece": "attempted full public PPN vector from source-universality alone",
        "source_path": str(FORMAL_190),
        "non_source_residuals": "domain/projector, boundary, scalar/disformal, memory, EM/Poynting, empirical bound rows",
        "public_claim_false": False,
        "full_observable_claim": True,
        "notes": "Negative control: source-universality alone must not claim full local GR.",
    })
    materialized.append(public_control)
    return materialized


def material_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "MAT4447_0_material_projection_live",
            "arena": "WEP_clock_orbital_material_inventory",
            "quantity": "material_projection_Req",
            "material_inventory_named": True,
            "source_candidates_recorded": True,
            "component_convention_defined": False,
            "projection_coeff_numeric": False,
            "residual_value_numeric": False,
            "arena_bound_numeric": False,
            "readout_no_reentry": True,
            "projection_coeff": "MISSING_MATERIAL_PROJECTION_COEFF",
            "residual_value": "MISSING_MATERIAL_RESIDUAL_VALUE",
            "arena_bound": "MISSING_ARENA_BOUND",
            "source_path": str(MATERIAL_OUTPUT_4446),
            "input_valid_for_claim": False,
            "public_authority": False,
            "notes": "Carried forward: material labels do not source gravity, but empirical projection values are still missing.",
        },
        {
            "row_id": "MAT4447_1_Req_compact_live",
            "arena": "Newton_PPN_orbital_same_current",
            "quantity": "R_eq_compact_test",
            "material_inventory_named": True,
            "source_candidates_recorded": True,
            "component_convention_defined": False,
            "projection_coeff_numeric": False,
            "residual_value_numeric": False,
            "arena_bound_numeric": False,
            "readout_no_reentry": True,
            "projection_coeff": "MISSING_P_REQ_COMPACT",
            "residual_value": "MISSING_REQ_COMPACT_TEST_VALUE",
            "arena_bound": "MISSING_ARENA_BOUND",
            "source_path": str(POST_4378),
            "input_valid_for_claim": False,
            "public_authority": False,
            "notes": "Carried forward: compact R_eq still has no source-backed numeric comparator value.",
        },
        {
            "row_id": "MAT4447_2_smoke_pass",
            "arena": "schema_smoke",
            "quantity": "material_projection_Req",
            "material_inventory_named": True,
            "source_candidates_recorded": True,
            "component_convention_defined": True,
            "projection_coeff_numeric": True,
            "residual_value_numeric": True,
            "arena_bound_numeric": True,
            "readout_no_reentry": True,
            "projection_coeff": "1",
            "residual_value": "2e-7",
            "arena_bound": "1e-5",
            "source_path": str(MATERIAL_OUTPUT_4446),
            "input_valid_for_claim": False,
            "public_authority": False,
            "notes": "Positive schema control only.",
        },
        {
            "row_id": "MAT4447_3_fail_control",
            "arena": "schema_smoke",
            "quantity": "material_projection_Req",
            "material_inventory_named": True,
            "source_candidates_recorded": True,
            "component_convention_defined": True,
            "projection_coeff_numeric": True,
            "residual_value_numeric": True,
            "arena_bound_numeric": True,
            "readout_no_reentry": True,
            "projection_coeff": "1",
            "residual_value": "0.003",
            "arena_bound": "1e-5",
            "source_path": str(MATERIAL_OUTPUT_4446),
            "input_valid_for_claim": False,
            "public_authority": False,
            "notes": "Negative schema control must fail the bound.",
        },
    ]


def residual_rollup_rows() -> List[Dict[str, object]]:
    return [
        {
            "rollup_id": "RU4447_0_source_weight_subvector",
            "subvector": "Delta_w_A/material_reentry source pieces",
            "status": "ZERO_INSIDE_PRIVATE_GR_PARITY_IMPORT_BRANCH",
            "affected_rows": "WEP eta; gamma source-norm; beta source-norm; alpha_i source-frame; xi/zeta source-nonconservation; Gdot source-measure; clock/orbital material reentry",
            "still_alive": "non-source metric/domain/projector/boundary/memory/EM/material-value rows",
            "valid_for_claim": False,
        },
        {
            "rollup_id": "RU4447_1_full_PPN_vector",
            "subvector": "full R_PPN public vector",
            "status": "NOT_CLAIMED_FROM_SOURCE_UNIVERSALITY_ALONE",
            "affected_rows": "full_R_PPN",
            "still_alive": "same-metric EH readout, no scalar/disformal bulk, no domain/projector vector drift, Hilbert conservation, boundary silence, empirical bounds",
            "valid_for_claim": False,
        },
        {
            "rollup_id": "RU4447_2_material_Req_values",
            "subvector": "material/R_eq empirical values",
            "status": "MISSING_NUMERIC_VALUES",
            "affected_rows": "WEP; clock; orbital; compact R_eq",
            "still_alive": "component convention, projection coefficient, residual value, arena bound, source path",
            "valid_for_claim": False,
        },
        {
            "rollup_id": "RU4447_3_GN_numeric_value",
            "subvector": "Newton constant numerical value",
            "status": "NOT_REQUIRED_FOR_THIS_REDUCTION_GATE",
            "affected_rows": "Newton/GR reduction",
            "still_alive": "universal constant calibration and source-blindness; no species/material dependence",
            "valid_for_claim": False,
        },
    ]


def reduction_rows() -> List[Dict[str, object]]:
    return [
        {
            "reduction_id": "RED4447_0_source_universality_to_ppn_pieces",
            "from_problem": "hidden source weights and material active-source reentry",
            "to_problem": "source-universality pieces of local PPN/Newton/WEP/clock/orbital residual vector",
            "status": "PRIVATE_SOURCE_SUBVECTOR_ZERO",
            "reason": "4446 gives no SpeciesLabel/MaterialLabel -> active source coefficient and one Hilbert source measure.",
            "valid_for_claim": False,
        },
        {
            "reduction_id": "RED4447_1_full_local_gr_to_survivor_map",
            "from_problem": "public local-GR/PPN claim",
            "to_problem": "non-source survivor map plus material/R_eq value acquisition",
            "status": "PUBLIC_CLAIM_STILL_BLOCKED",
            "reason": "Source-zero rows cannot prove metric principal block, boundary silence, domain/projector silence, memory silence or EM/Poynting Hilbert closure.",
            "valid_for_claim": False,
        },
        {
            "reduction_id": "RED4447_2_next_target",
            "from_problem": "post-4447 local branch",
            "to_problem": NEXT_TARGET,
            "status": "NEXT_DERIVATION_TARGET_SELECTED",
            "reason": "The useful leap is now a survivor map: exactly which non-source rows remain, and which one is cheapest to derive or bound next.",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(ppn_outputs: Sequence[Mapping[str, str]], material_outputs: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    ppn = {row["row_id"]: row for row in ppn_outputs}
    material = {row["row_id"]: row for row in material_outputs}
    source_rows_local = rows_from(SOURCE_REGISTER)
    no_claim = not any(row.get("valid_for_claim") == "True" for row in ppn_outputs) and not any(row.get("valid_for_claim") == "True" for row in material_outputs)
    source_private_rows = [row for key, row in ppn.items() if key.startswith("PPN4447_") and key != "PPN4447_9_full_public_PPN_control"]
    return [
        {"gate_id": "CG4447_0_sources_exist", "claim": "all cited source paths exist", "passed": all(row["path_exists"] == "True" for row in source_rows_local), "valid_for_claim": False, "detail": "Source register path-backed."},
        {"gate_id": "CG4447_1_needles_found", "claim": "all cited source needles found", "passed": all(row["needle_found"] == "True" for row in source_rows_local), "valid_for_claim": False, "detail": "No vibe-only source propagation."},
        {"gate_id": "CG4447_2_source_subvector_zero", "claim": "source-universality pieces of PPN residual vector are zero in private branch", "passed": all(row.get("current_status") == "PPN_SOURCE_UNIVERSALITY_COMPONENT_ZERO_PRIVATE_NONCLAIM" for row in source_private_rows), "valid_for_claim": False, "detail": "Delta_w_A/material-reentry pieces propagated to WEP, PPN, clock and orbital rows."},
        {"gate_id": "CG4447_3_public_control_blocked", "claim": "source-universality alone does not claim full public PPN vector", "passed": ppn["PPN4447_9_full_public_PPN_control"].get("current_status") == "PPN_SOURCE_UNIVERSALITY_PARTIAL_CLAUSES_OPEN", "valid_for_claim": False, "detail": "Public-control row stays blocked because public_claim_false is intentionally false."},
        {"gate_id": "CG4447_4_non_source_preserved", "claim": "non-source residuals are preserved", "passed": all(row.get("non_source_residual_preserved") == "True" for row in source_private_rows) and "domain/projector" in text(RESIDUAL_ROLLUP).lower(), "valid_for_claim": False, "detail": "No boundary/domain/memory/EM side channel erased."},
        {"gate_id": "CG4447_5_material_live_values_missing", "claim": "material and R_eq live rows remain value-missing", "passed": material["MAT4447_0_material_projection_live"].get("current_status") == "MATERIAL_REQ_SOURCE_CANDIDATES_READY_VALUES_MISSING" and material["MAT4447_1_Req_compact_live"].get("current_status") == "MATERIAL_REQ_SOURCE_CANDIDATES_READY_VALUES_MISSING", "valid_for_claim": False, "detail": "Material/R_eq empirical scoring still needs numeric inputs."},
        {"gate_id": "CG4447_6_material_controls", "claim": "material gate has pass and fail controls", "passed": material["MAT4447_2_smoke_pass"].get("current_status") == "MATERIAL_REQ_VALUE_SCHEMA_PASS_NONCLAIM" and material["MAT4447_3_fail_control"].get("current_status") == "MATERIAL_REQ_VALUE_FAILS_BOUND", "valid_for_claim": False, "detail": "Schema control behaves."},
        {"gate_id": "CG4447_7_GN_caveat_kept", "claim": "G_N numerical derivation is not smuggled into this gate", "passed": "NOT_REQUIRED_FOR_THIS_REDUCTION_GATE" in text(RESIDUAL_ROLLUP), "valid_for_claim": False, "detail": "Universal calibrated G_N caveat remains explicit."},
        {"gate_id": "CG4447_8_no_public_claim", "claim": "4447 emits no public local-GR/PPN claim", "passed": no_claim, "valid_for_claim": False, "detail": "Every row remains private nonclaim."},
        {"gate_id": "CG4447_9_next_target_written", "claim": "next target selected", "passed": NEXT_CSV.exists() and NEXT_TARGET in text(NEXT_CSV), "valid_for_claim": False, "detail": NEXT_TARGET},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4447_0",
            "decision": DECISION,
            "summary": "4447 does the useful propagation step: the 4446 GR-parity source-universality result now maps into the source-weight/material-reentry pieces of WEP, PPN, Gdot, clock and orbital residual rows. This is progress, not a public local-GR claim. Non-source residuals survive explicitly, especially domain/projector, boundary, scalar/disformal, memory and EM/Poynting Hilbert-stress side channels. Material/R_eq numeric values remain missing.",
            "next_target": NEXT_TARGET,
            "public_claim": False,
            "valid_for_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "root_result": "source-universality pieces of local residual vector zero inside private PPC4161 branch",
            "closed_inside_private_branch": "source-weight/material-reentry contributions to WEP eta, gamma/beta source normalization, alpha_i source-frame, xi/zeta source-nonconservation, Gdot source drift, clock/orbital material reentry",
            "still_missing": "non-source PPN survivor closure; material/R_eq values; empirical public bound rows; global parent-action adoption",
            "next_target": NEXT_TARGET,
            "public_claim": False,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4447_0",
            "target": NEXT_TARGET,
            "objective": "Build a survivor map for non-source local PPN residuals, then either derive the cheapest survivor zero or source the first material/R_eq empirical value.",
            "derive_first": "separate gamma/beta metric-principal clauses, alpha_i/xi domain-projector clauses, zeta/Hilbert conservation clauses, Gdot memory/kappa drift clauses, and EM/Poynting source-current clauses",
            "fallback": "fill one material/R_eq row with units, projection coefficient, residual value, bound, source path and no-cancellation guard",
            "risk": "mistaking source universality for full local-GR closure; ignoring EM/Poynting as a hidden current/source side-channel",
            "valid_for_claim": False,
        }
    ]


def build_doc(sources: Sequence[Mapping[str, object]], ppn_outputs: Sequence[Mapping[str, object]], material_outputs: Sequence[Mapping[str, object]], gates: Sequence[Mapping[str, object]]) -> str:
    return f"""# 463 PPC4161 GR-parity source-universality to local PPN residual vector or material values

Marker: `{MARKER}`

Decision: `{DECISION}`

Claim register: `{CLAIM_ID}`

## Result

4447 propagates the 4446 result instead of circling it:

```text
Delta_w_A = 0 and material-source reentry = 0
=> the source-universality pieces of the local residual vector are zero inside PPC4161.
```

This touches WEP, PPN, `Gdot/G`, clock and orbital rows, but only the source-weight/material-reentry pieces. It does **not** erase non-source residuals: metric principal readout, scalar/disformal leakage, domain/projector drift, boundary flux, memory/kappa drift, EM/Poynting Hilbert-stress closure and empirical material/`R_eq` values remain live.

## Source Register

{table(sources)}

## Derivation Rows

{table(rows_from(DERIVATION_ROWS))}

## PPN Source Residual Gate

{table(ppn_outputs)}

## Material / R_eq Value Gate

{table(material_outputs)}

## Residual Rollup

{table(rows_from(RESIDUAL_ROLLUP))}

## Reduction Rows

{table(rows_from(REDUCTION_ROWS))}

## Claim Gates

{table(gates)}

## Decision

{table(rows_from(DECISION_CSV))}

## Status

{table(rows_from(STATUS_CSV))}

## Next Target

{table(rows_from(NEXT_CSV))}
"""


def post_doc() -> str:
    return f"""# 4447 Y5 R2FR GR-parity source-universality to local PPN residual vector or material values

Private checkpoint generated at `{STAMP}`.

Summary:
- Propagated the 4446 source-universality result into the source-weight/material-reentry pieces of the local residual vector.
- Source pieces of WEP, PPN, `Gdot/G`, clock and orbital rows are zero inside the private PPC4161 branch.
- This is not full local-GR closure: non-source PPN survivors and material/`R_eq` values remain open.

Next target: `{NEXT_TARGET}`
"""


def update_claims_register() -> None:
    rows = rows_from(CLAIMS_PATH)
    fieldnames = list(rows[0].keys()) if rows else ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk", "sector", "evidence", "next_action", "risk"]
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_source_coupling",
        "claim": "4447 propagates the private 4446 source-universality result into source-weight/material-reentry pieces of WEP, PPN, Gdot, clock and orbital residual rows. It does not claim full local GR: non-source residuals and material/R_eq values remain open.",
        "current_evidence": "4447 source register, derivation rows, PPN source-residual gate, material/R_eq value gate, residual rollup, reduction rows, claim gates, decision, status, next target and validation CSV.",
        "status": "source_universality_ppn_source_subvector_zero_private_nonclaim_non_source_survivors_open",
        "next_test": "Map non-source PPN survivor rows or fill the first material/R_eq empirical value.",
        "key_risk": "Confusing source-universality subvector closure with full local-GR/PPN closure.",
        "sector": "local_gr_source_coupling",
        "evidence": "4447 source register, derivation rows, PPN source-residual gate, material/R_eq value gate, residual rollup, reduction rows, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Map non-source PPN survivor rows or fill the first material/R_eq empirical value.",
        "risk": "Confusing source-universality subvector closure with full local-GR/PPN closure.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(new_row)


def append_marker_section(path: Path, marker: str, section: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    write_text(path, existing.rstrip() + "\n\n" + section.strip() + "\n")


def write_spine_and_packet() -> None:
    spine_section = f"""## Local GR Source Coupling Update - Source Universality PPN Subvector

Marker: `{MARKER}`  
Source checkpoint: `4447-Y5-R2FR-GR-parity-source-universality-to-local-PPN-residual-vector-or-material-values.md`  
Claim register row: `{CLAIM_ID}`

The private PPC4161 branch now has a source-universality subvector map: `Delta_w_A=0` and material active-source reentry `=0` propagate into source-weight/material-reentry pieces of WEP, PPN, `Gdot/G`, clock and orbital residual rows. This is not full local-GR closure. Domain/projector, boundary, memory, scalar/disformal, EM/Poynting and material-value rows remain live.
"""
    packet_section = f"""## PPC4161 Packet Addendum - Source Universality PPN Subvector

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4447-Y5-R2FR-GR-parity-source-universality-to-local-PPN-residual-vector-or-material-values.md`

The packet now records that source-weight/material-reentry pieces of the local PPN/Newton/WEP/clock/orbital residual vector are zero inside the private branch. The packet also keeps the reactivation rule: non-source residual rows reopen unless their own action-level clauses are signed.
"""
    append_marker_section(SPINE_PATH, MARKER, spine_section)
    append_marker_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    ppn = {row["row_id"]: row for row in rows_from(PPN_OUTPUT)}
    material = {row["row_id"]: row for row in rows_from(MATERIAL_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    ppn_private = [row for key, row in ppn.items() if key != "PPN4447_9_full_public_PPN_control"]
    no_claims = not any(row.get("valid_for_claim") == "True" for row in ppn.values()) and not any(row.get("valid_for_claim") == "True" for row in material.values())
    checks = [
        ("VAL4447_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4447_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4447_2_ppn_private_rows_zero", all(row.get("current_status") == "PPN_SOURCE_UNIVERSALITY_COMPONENT_ZERO_PRIVATE_NONCLAIM" for row in ppn_private), "source-universality PPN pieces zero privately"),
        ("VAL4447_3_public_control_blocked", ppn["PPN4447_9_full_public_PPN_control"].get("current_status") == "PPN_SOURCE_UNIVERSALITY_PARTIAL_CLAUSES_OPEN", "full public PPN control is blocked"),
        ("VAL4447_4_non_source_preserved", all(row.get("non_source_residual_preserved") == "True" for row in ppn_private) and "NON_SOURCE_RESIDUALS_PRESERVED" in text(DERIVATION_ROWS), "non-source residuals explicitly preserved"),
        ("VAL4447_5_material_live_missing", material["MAT4447_0_material_projection_live"].get("current_status") == "MATERIAL_REQ_SOURCE_CANDIDATES_READY_VALUES_MISSING", "material live values missing"),
        ("VAL4447_6_req_live_missing", material["MAT4447_1_Req_compact_live"].get("current_status") == "MATERIAL_REQ_SOURCE_CANDIDATES_READY_VALUES_MISSING", "R_eq live values missing"),
        ("VAL4447_7_material_smoke_pass", material["MAT4447_2_smoke_pass"].get("current_status") == "MATERIAL_REQ_VALUE_SCHEMA_PASS_NONCLAIM", "material smoke pass works"),
        ("VAL4447_8_material_fail_control", material["MAT4447_3_fail_control"].get("current_status") == "MATERIAL_REQ_VALUE_FAILS_BOUND", "material fail control fails"),
        ("VAL4447_9_residual_rollup", all(key in text(RESIDUAL_ROLLUP) for key in ("RU4447_0_source_weight_subvector", "RU4447_1_full_PPN_vector", "RU4447_2_material_Req_values")), "residual rollup written"),
        ("VAL4447_10_no_claim_outputs", no_claims, "no output row is public claim-ready"),
        ("VAL4447_11_claim_gate_no_claim", any(row["gate_id"] == "CG4447_8_no_public_claim" and row["passed"] == "True" for row in gates), "claim gate explicitly blocks public claim"),
        ("VAL4447_12_all_claim_gates_pass", all(row["passed"] == "True" for row in gates), "all claim gates pass"),
        ("VAL4447_13_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-289"),
        ("VAL4447_14_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4447_15_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4447_16_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4447_17_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4447_18_next_gate", any(row["gate_id"] == "CG4447_9_next_target_written" and row["passed"] == "True" for row in gates), "next target claim gate is true"),
        ("VAL4447_19_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4447_20_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(PPN_INPUT, ppn_input_rows())
    write_csv(PPN_OUTPUT, evaluate_ppn_rows(PPN_INPUT))
    write_csv(MATERIAL_INPUT, material_input_rows())
    write_csv(MATERIAL_OUTPUT, evaluate_material_rows(MATERIAL_INPUT))
    write_csv(RESIDUAL_ROLLUP, residual_rollup_rows())
    write_csv(REDUCTION_ROWS, reduction_rows())
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    ppn_outputs = rows_from(PPN_OUTPUT)
    material_outputs = rows_from(MATERIAL_OUTPUT)
    gates = claim_gate_rows(ppn_outputs, material_outputs)
    write_csv(CLAIM_GATES, gates)
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), ppn_outputs, material_outputs, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()
