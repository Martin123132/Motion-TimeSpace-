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

from constructor_nohom_kmshadow_gate import (  # noqa: E402
    evaluate_kmshadow_rows,
    evaluate_nohom_rows,
    evaluate_shadow_split_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4432"
CLAIM_ID = "L-273"
MARKER = "PPC4161_SOURCE_SHADOW_CONSTRUCTOR_NOHOM_PROOF_OR_KMSHADOWCSHADOW_FIRST_VALUE_4432"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_SHADOW_CONSTRUCTOR_NOHOM_PROOF_OR_KMSHADOWCSHADOW_FIRST_VALUE_4432"
DECISION = "PURE_SOURCE_SHADOW_COLLAPSES_UNDER_VARIATIONAL_OWNER_CONTRACT_SURVIVING_COUNTERMODEL_REASSIGNED_TO_ACTION_SCALE_HIDDEN_READOUT"
NEXT_TARGET = "4433-Y5-R2FR-action-scale-constant-sector-universality-or-Kmactionscale-first-value.md"

FORMAL_PATH = FORMAL / "448-PPC4161-source-shadow-constructor-noHom-proof-or-KmshadowCshadow-first-value.md"
DOC_PATH = POST / "4432-Y5-R2FR-source-shadow-constructor-noHom-proof-or-KmshadowCshadow-first-value.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4432_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4432_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4432_DERIVATION_ROWS.csv"
NOHOM_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4432_CONSTRUCTOR_NOHOM_INPUT.csv"
NOHOM_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4432_CONSTRUCTOR_NOHOM_OUTPUT.csv"
SPLIT_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4432_SHADOW_SPLIT_INPUT.csv"
SPLIT_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4432_SHADOW_SPLIT_OUTPUT.csv"
KMSHADOW_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4432_KMSHADOW_VALUE_INPUT.csv"
KMSHADOW_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4432_KMSHADOW_VALUE_OUTPUT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4432_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4432_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4432_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4432_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "constructor_nohom_kmshadow_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4432_source_shadow_constructor_noHom_proof_or_KmshadowCshadow_first_value.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4431 = SOURCE_DIR / "P8_Y5_R2FR_4431_NEXT_TARGET.csv"
FORMAL_447 = FORMAL / "447-PPC4161-source-shadow-ban-and-nonHilbert-bypass-zero-or-first-DD-K-value.md"
SHADOW4431 = SOURCE_DIR / "P8_Y5_R2FR_4431_SOURCE_SHADOW_OUTPUT.csv"
KPRODUCT4431 = SOURCE_DIR / "P8_Y5_R2FR_4431_DD_K_PRODUCT_OUTPUT.csv"
CSV_NSS3542 = SOURCE_DIR / "P8_Y5_R2FR_3542_NO_SOURCE_ONLY_SLOT_PROOF_ATTEMPT.csv"
CSV_SF2613 = SOURCE_DIR / "P8_Y5_HOM_EXCLUSION_GATE_2613_LABEL_FORGETTING_SOURCE_FUNCTOR_AUDIT.csv"
CSV_SLF1603 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1603_SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT.csv"
CSV_CONTRACT = SOURCE_DIR / "P8_no_species_source_charge_CONTRACT.csv"
CSV_SPECIES = SOURCE_DIR / "P8_species_source_charge_residual_or_zero.csv"
CSV_CM2508 = SOURCE_DIR / "P8_Y5_NO_SHADOW_2508_SOURCE_ONLY_COUNTERMODELS.csv"
CSV_RSW2508 = SOURCE_DIR / "P8_Y5_NO_SHADOW_2508_SOURCE_WEIGHT_RESIDUAL_ROWS.csv"
CSV_FIRST_DD_STATUS = SOURCE_DIR / "P8_Y5_first_DD_K_value_or_source_leg_status.csv"
CSV_MTS_DD_STATUS = SOURCE_DIR / "P8_Y5_MTS_to_DD_source_map_status.csv"

DELTA_Q_MHAT = 3.330000e-03
ETA_BOUND = 2.8e-15
D_MHAT_ONE_CHANNEL_CEILING = ETA_BOUND / DELTA_Q_MHAT


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
    for index, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return index
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
        {"source_id": "SRC4432_00_4431_next", "path": NEXT_4431, "needle": "constructor/no-Hom", "role": "4431 handoff to constructor/no-Hom."},
        {"source_id": "SRC4432_01_447_formal", "path": FORMAL_447, "needle": "SH4431_0_shadow_ban_theorem", "role": "4431 exact source-shadow theorem."},
        {"source_id": "SRC4432_02_shadow4431", "path": SHADOW4431, "needle": "SH4431_2_wA_countermodel_survives", "role": "current source-shadow countermodel."},
        {"source_id": "SRC4432_03_kproduct4431", "path": KPRODUCT4431, "needle": "K4431_0_K_m_shadow_contract", "role": "first K_m_shadow target."},
        {"source_id": "SRC4432_04_nss3542_nohom", "path": CSV_NSS3542, "needle": "NSS3542_2_noHom", "role": "no-Hom proof clause."},
        {"source_id": "SRC4432_05_nss3542_constructor", "path": CSV_NSS3542, "needle": "NSS3542_3_constructor_exhaustion", "role": "constructor exhaustion gap."},
        {"source_id": "SRC4432_06_sf2613", "path": CSV_SF2613, "needle": "SF2613_0_label_forgetting", "role": "source functor label forgetting."},
        {"source_id": "SRC4432_07_slf1603", "path": CSV_SLF1603, "needle": "SLF1603_1_common_measure_current", "role": "common measure/current gap."},
        {"source_id": "SRC4432_08_contract", "path": CSV_CONTRACT, "needle": "S2_constant_sector_universality", "role": "constant-sector universality contract."},
        {"source_id": "SRC4432_09_species", "path": CSV_SPECIES, "needle": "SSC2675_3_no_bound_inversion_guard", "role": "no bound inversion guard."},
        {"source_id": "SRC4432_10_cm2508", "path": CSV_CM2508, "needle": "CM2508_0_wA_action", "role": "weighted action countermodel."},
        {"source_id": "SRC4432_11_rsw2508", "path": CSV_RSW2508, "needle": "RSW2508_3", "role": "action scale residual."},
        {"source_id": "SRC4432_12_first_dd", "path": CSV_FIRST_DD_STATUS, "needle": "STATUS3545_0", "role": "first DD source-leg status."},
        {"source_id": "SRC4432_13_mts_dd", "path": CSV_MTS_DD_STATUS, "needle": "STAT3544_0_map", "role": "MTS-to-DD map status."},
        {"source_id": "SRC4432_14_gate", "path": GATE_PATH, "needle": "def evaluate_nohom_row", "role": "4432 gate script."},
        {"source_id": "SRC4432_15_generator", "path": GENERATOR_PATH, "needle": "CHECKPOINT = \"4432\"", "role": "4432 generator script."},
    ]


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for spec in source_specs():
        path = Path(spec["path"])
        needle = str(spec["needle"])
        content = text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in content,
                "line_number": line_of(path, needle),
                "role": spec["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "NHOM4432_0_factorization_noHom_theorem",
            "claim": "Constructor exhaustion implies no-Hom into active source coefficients.",
            "derivation": "Let Coeff_active_source be the coefficient object of the active source functor after common G calibration. If Coeff_active_source factors as Image(ParentGenerate[q(Phi), theta_rep, universal constants]) and SpeciesLabel, HiddenMarker and ReadoutMarker are not arguments of ParentGenerate, then every vertical derivative of an active source coefficient along SpeciesLabel/HiddenMarker/readout fibres is zero. Equivalently Hom_parent(SpeciesLabel,Coeff_active_source)=Hom_parent(HiddenMarker,Coeff_active_source)=empty for source-only coefficients.",
            "consequence": "This is the actual mathematical contract needed to kill source-shadow structurally.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "NHOM4432_1_current_reduction",
            "claim": "Current MTS has source-domain label forgetting but not constructor exhaustion.",
            "derivation": "2613 and 3542 support StressTotal-domain/source-label forgetting as a contract. The missing pieces are generator exhaustion, constant-sector universality, hidden-marker absence and readout no-reentry. Therefore no-Hom is reduced to a smaller parent-object-language problem, not solved outright.",
            "consequence": "The next proof target is no longer generic source coupling; it is ParentGenerate exhaustion plus constant-sector universality.",
            "status": "REDUCED_NOT_CLOSED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SPLIT4432_0_pure_source_shadow_elimination",
            "claim": "Pure source-only shadow is not an independent live channel under variational source ownership.",
            "derivation": "A term used only as S_source=sum_A w_A S_A in the gravitational equation but not in the matter action is excluded by the total-Hilbert source owner contract. If the same weighted term is placed inside S_matter before variation, it is no longer a pure source-only shadow; it changes action normalization, inertial equations or constants and belongs to the action-scale/constant-sector residual.",
            "consequence": "C_shadow splits: the pure source-only branch is contract-killable; the surviving weighted-action countermodel is reassigned.",
            "status": "STRUCTURAL_SPLIT_DERIVED_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SPLIT4432_1_surviving_shadow_reassignment",
            "claim": "The surviving 2508 countermodels are action-scale, hidden-return or readout-projector channels.",
            "derivation": "CM2508_0 w_A action and CM2508_5 action-scale weights are not pure source-only if variational ownership is respected. CM2508_3 hidden marker and CM2508_4 readout projector are return channels. They remain finite channels, but the label 'source-shadow' should no longer hide their different mathematical nature.",
            "consequence": "The first next finite route becomes action-scale/constant-sector universality before pretending to fill a single K_m_shadow value.",
            "status": "RESIDUAL_RELABELED_TO_SHARPER_CHANNELS",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "KM4432_0_no_real_Kmshadow_value_yet",
            "claim": "No parent-owned numeric K_m_shadow*C_shadow value exists in the current corpus.",
            "derivation": f"The current corpus has the bound target abs(K_m_shadow*C_shadow)<={D_MHAT_ONE_CHANNEL_CEILING:.12e}, but no parent coefficient, no source leg, no source-independent K map and no sign/alloy policy. The empirical bound cannot define the theory coefficient.",
            "consequence": "The honest next step is to prove action-scale/constant-sector universality or fill that sharper product, not invert MICROSCOPE into a theory value.",
            "status": "FINITE_VALUE_NOT_FOUND_BOUND_TARGET_ONLY",
            "valid_for_claim": False,
        },
    ]


def nohom_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "NHOM4432_0_exact_factorized_noHom_contract",
            "clause": "factorized constructor no-Hom theorem",
            "stress_total_domain": True,
            "parent_generator_exhausted": True,
            "species_label_absent": True,
            "hidden_marker_absent": True,
            "readout_no_reentry": True,
            "constant_sector_universal": True,
            "common_calibration_removed": True,
            "source_path": str(CSV_NSS3542),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Exact no-Hom contract; nonclaim until ParentGenerate and constant sector are signed.",
        },
        {
            "row_id": "NHOM4432_1_current_source_domain",
            "clause": "current stress-total source domain",
            "stress_total_domain": True,
            "parent_generator_exhausted": False,
            "species_label_absent": True,
            "hidden_marker_absent": False,
            "readout_no_reentry": False,
            "constant_sector_universal": False,
            "common_calibration_removed": True,
            "source_path": str(CSV_SF2613),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Label forgetting is clean, but generator exhaustion and reentry clauses remain unsigned.",
        },
        {
            "row_id": "NHOM4432_2_constant_sector_gap",
            "clause": "constant-sector universality",
            "stress_total_domain": True,
            "parent_generator_exhausted": False,
            "species_label_absent": False,
            "hidden_marker_absent": False,
            "readout_no_reentry": False,
            "constant_sector_universal": False,
            "common_calibration_removed": True,
            "source_path": str(CSV_CONTRACT),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Species constants and source normalizations remain legal until the constant sector is parent-derived.",
        },
        {
            "row_id": "NHOM4432_3_bound_inversion_guard",
            "clause": "bound cannot define parent coefficient",
            "stress_total_domain": True,
            "parent_generator_exhausted": False,
            "species_label_absent": False,
            "hidden_marker_absent": False,
            "readout_no_reentry": False,
            "constant_sector_universal": False,
            "common_calibration_removed": True,
            "source_path": str(CSV_SPECIES),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Empirical WEP bound cannot be inverted into a parent coefficient.",
        },
    ]


def shadow_split_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "SPLIT4432_0_pure_source_only_shadow",
            "component": "C_shadow_pure_source_only",
            "definition": "independent source functional used only on gravitational RHS after matter variation",
            "pure_source_only": True,
            "action_scale": False,
            "hidden_return": False,
            "readout_projector": False,
            "killed_by_variational_owner": True,
            "reassigned_channel": "DERIVED_ZERO_IF_TOTAL_HILBERT_SOURCE_OWNER_SIGNED",
            "source_path": str(FORMAL_447),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "This branch is structurally illegal under the total-Hilbert source owner contract.",
        },
        {
            "row_id": "SPLIT4432_1_weighted_action_shadow",
            "component": "C_shadow_weighted_action",
            "definition": "S_matter=sum_A w_A S_A placed before variation",
            "pure_source_only": False,
            "action_scale": True,
            "hidden_return": False,
            "readout_projector": False,
            "killed_by_variational_owner": False,
            "reassigned_channel": "C_action_scale_or_constant_sector",
            "source_path": str(CSV_CM2508),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Survives, but not as pure source-shadow; it is action-scale/constant-sector leakage.",
        },
        {
            "row_id": "SPLIT4432_2_hidden_marker_shadow",
            "component": "C_shadow_hidden_marker",
            "definition": "hidden scalar/domain/boundary marker feeds active source coefficient",
            "pure_source_only": False,
            "action_scale": False,
            "hidden_return": True,
            "readout_projector": False,
            "killed_by_variational_owner": False,
            "reassigned_channel": "C_hidden_return",
            "source_path": str(CSV_CM2508),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Survives as hidden return unless no-Hom/no-marker theorem closes.",
        },
        {
            "row_id": "SPLIT4432_3_readout_projector_shadow",
            "component": "C_shadow_readout_projector",
            "definition": "post-variation material/source-worldtube/readout projector reintroduces coefficient",
            "pure_source_only": False,
            "action_scale": False,
            "hidden_return": False,
            "readout_projector": True,
            "killed_by_variational_owner": False,
            "reassigned_channel": "C_readout_projector",
            "source_path": str(CSV_CM2508),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Survives as readout/projector commutator unless readout no-reentry closes.",
        },
    ]


def kmshadow_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "KM4432_0_pure_source_zero_projection",
            "product": "K_m_shadow*C_shadow_pure_source_only",
            "subcomponent": "C_shadow_pure_source_only",
            "value": "DERIVED_ZERO",
            "units": "dimensionless",
            "parent_source": "TOTAL_HILBERT_SOURCE_OWNER_CONTRACT",
            "source_leg": "not_applicable_zero_branch",
            "projection": "0.00333*abs(K_m_shadow*C_shadow_pure_source_only)=0 if total Hilbert source owner is parent-signed",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "source_path": str(SPLIT_OUTPUT),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Zero projection is conditional/nonclaim because the owner contract is not parent-signed.",
        },
        {
            "row_id": "KM4432_1_action_scale_reassignment",
            "product": "K_m_shadow*C_shadow_weighted_action",
            "subcomponent": "C_shadow_weighted_action",
            "value": "REASSIGNED_C_ACTION_SCALE",
            "units": "dimensionless",
            "parent_source": "MISSING_ACTION_SCALE_PARENT_SOURCE",
            "source_leg": "MISSING_ACTION_SCALE_SOURCE_LEG",
            "projection": f"{DELTA_Q_MHAT:.5f}*abs(K_m_action_scale*C_action_scale) <= {ETA_BOUND:.12e}",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "source_path": str(CSV_RSW2508),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Weighted-action survivor moves to action-scale/constant-sector target.",
        },
        {
            "row_id": "KM4432_2_hidden_return_reassignment",
            "product": "K_m_shadow*C_shadow_hidden_marker",
            "subcomponent": "C_shadow_hidden_marker",
            "value": "REASSIGNED_C_HIDDEN_RETURN",
            "units": "dimensionless",
            "parent_source": "MISSING_HIDDEN_RETURN_PARENT_SOURCE",
            "source_leg": "MISSING_HIDDEN_RETURN_SOURCE_LEG",
            "projection": f"{DELTA_Q_MHAT:.5f}*abs(K_m_hidden*C_hidden_return) <= {ETA_BOUND:.12e}",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "source_path": str(CSV_CM2508),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Hidden-marker survivor moves to hidden return target.",
        },
        {
            "row_id": "KM4432_3_readout_projector_reassignment",
            "product": "K_m_shadow*C_shadow_readout_projector",
            "subcomponent": "C_shadow_readout_projector",
            "value": "REASSIGNED_C_READOUT_PROJECTOR",
            "units": "dimensionless",
            "parent_source": "MISSING_READOUT_PROJECTOR_PARENT_SOURCE",
            "source_leg": "MISSING_READOUT_PROJECTOR_SOURCE_LEG",
            "projection": f"{DELTA_Q_MHAT:.5f}*abs(K_m_readout*C_readout_projector) <= {ETA_BOUND:.12e}",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "source_path": str(CSV_CM2508),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Readout survivor moves to readout no-reentry/commutator target.",
        },
        {
            "row_id": "KM4432_4_original_Kmshadow_bound_target",
            "product": "K_m_shadow*C_shadow_total",
            "subcomponent": "C_shadow_total",
            "value": f"BOUND_ONLY_{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "units": "dimensionless",
            "parent_source": "MISSING_PARENT_SOURCE",
            "source_leg": "MISSING_SOURCE_LEG",
            "projection": f"abs(K_m_shadow*C_shadow_total) <= {D_MHAT_ONE_CHANNEL_CEILING:.12e} only if all subcomponents are collapsed into one effective parameter",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "source_path": str(KPRODUCT4431),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Kept only as a bookkeeping target; sharper subcomponents are preferred.",
        },
    ]


def claim_gate_rows(nohom: Sequence[Mapping[str, str]], split: Sequence[Mapping[str, str]], kmshadow: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    nohom_rows = {row["row_id"]: row for row in nohom}
    split_rows = {row["row_id"]: row for row in split}
    km_rows = {row["row_id"]: row for row in kmshadow}
    no_claims = not any(row.get("valid_for_claim") == "True" for row in nohom) and not any(row.get("valid_for_claim") == "True" for row in split) and not any(row.get("valid_for_claim") == "True" for row in kmshadow)
    return [
        {"gate_id": "CG4432_0_nohom_contract", "claim": "factorized constructor no-Hom theorem staged", "passed": nohom_rows["NHOM4432_0_exact_factorized_noHom_contract"].get("current_status") == "CONSTRUCTOR_NOHOM_CONTRACT_READY_NONCLAIM", "valid_for_claim": False, "detail": "Exact but ParentGenerate/constant sector unsigned."},
        {"gate_id": "CG4432_1_current_reduction", "claim": "current source-domain route reduces to generator/reentry gaps", "passed": nohom_rows["NHOM4432_1_current_source_domain"].get("current_status") == "CONSTRUCTOR_NOHOM_REDUCES_TO_GENERATOR_EXHAUSTION_AND_REENTRY", "valid_for_claim": False, "detail": "This is narrower than generic coupling."},
        {"gate_id": "CG4432_2_constant_sector_gap", "claim": "constant-sector countermodel remains live", "passed": nohom_rows["NHOM4432_2_constant_sector_gap"].get("current_status") == "CONSTRUCTOR_NOHOM_COUNTERMODEL_SURVIVES", "valid_for_claim": False, "detail": "Species constants/source normalization still need derivation."},
        {"gate_id": "CG4432_3_pure_shadow_zero", "claim": "pure source-only shadow branch is contract-killable", "passed": split_rows["SPLIT4432_0_pure_source_only_shadow"].get("current_status") == "SHADOW_PURE_SOURCE_ONLY_ZERO_CONTRACT_READY_NONCLAIM", "valid_for_claim": False, "detail": "Only under parent-signed total-Hilbert owner."},
        {"gate_id": "CG4432_4_weighted_action_reassigned", "claim": "weighted-action countermodel is reassigned", "passed": split_rows["SPLIT4432_1_weighted_action_shadow"].get("current_status") == "SHADOW_REASSIGNED_ACTION_SCALE_OR_BLOCK", "valid_for_claim": False, "detail": "Not pure source-shadow; becomes action-scale/constant-sector."},
        {"gate_id": "CG4432_5_hidden_readout_reassigned", "claim": "hidden/readout shadow pieces are separated", "passed": split_rows["SPLIT4432_2_hidden_marker_shadow"].get("current_status") == "SHADOW_REASSIGNED_HIDDEN_RETURN" and split_rows["SPLIT4432_3_readout_projector_shadow"].get("current_status") == "SHADOW_REASSIGNED_READOUT_PROJECTOR", "valid_for_claim": False, "detail": "Return channels are named separately."},
        {"gate_id": "CG4432_6_K_zero_projection_nonclaim", "claim": "pure source K projection is conditional zero", "passed": km_rows["KM4432_0_pure_source_zero_projection"].get("current_status") == "KM_SHADOW_PRODUCT_INPUT_INVALID_NONCLAIM", "valid_for_claim": False, "detail": "Zero value exists only under unsigned parent owner contract."},
        {"gate_id": "CG4432_7_original_bound_target_retained", "claim": "original total K_m_shadow target retained as bound only", "passed": km_rows["KM4432_4_original_Kmshadow_bound_target"].get("current_status") == "KM_SHADOW_PRODUCT_BOUND_TARGET_ONLY", "valid_for_claim": False, "detail": "Bound target is bookkeeping, not theory value."},
        {"gate_id": "CG4432_8_no_claim_outputs", "claim": "4432 emits no local-GR/WEP/PPN/R10 claim", "passed": no_claims, "valid_for_claim": False, "detail": "All outputs remain private nonclaim rows."},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4432_0",
            "decision": DECISION,
            "summary": "4432 splits the source-shadow coupling instead of treating it as one foggy parameter. Pure source-only shadow is killed by the total-Hilbert variational owner contract if that contract is parent-signed. The famous w_A S_A countermodel survives, but it is not pure source-only shadow; it is action-scale/constant-sector leakage. Hidden marker and readout projector countermodels are also separated into their own return channels. No numeric K_m_shadow*C_shadow is parent-owned yet, and the MICROSCOPE bound remains a bound target only.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4432_0_nohom", "status": "CONSTRUCTOR_NOHOM_REDUCED_TO_PARENTGENERATE_AND_CONSTANT_SECTOR", "detail": "No-Hom now needs ParentGenerate exhaustion plus constant-sector universality, not another Ward argument.", "valid_for_claim": False},
        {"status_id": "STAT4432_1_split", "status": "PURE_SOURCE_SHADOW_CONTRACT_KILLABLE_SURVIVORS_REASSIGNED", "detail": "Pure source-only branch is structurally illegal under total-Hilbert owner; weighted-action branch becomes action-scale/constant-sector.", "valid_for_claim": False},
        {"status_id": "STAT4432_2_k", "status": "NO_PARENT_NUMERIC_KMSHADOW_VALUE_FOUND", "detail": f"Only effective bound target remains: abs(K_m_shadow*C_shadow_total) <= {D_MHAT_ONE_CHANNEL_CEILING:.12e}.", "valid_for_claim": False},
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4432_0",
            "target": NEXT_TARGET,
            "objective": "Prove single action-scale/constant-sector universality for the weighted-action survivor, or fill K_m_action_scale*C_action_scale with parent provenance.",
            "derive_first": "derive one parent action measure/current normalization and constant sector theta_univ so w_A S_A and species-indexed hbar/measure/current normalizations are untypeable.",
            "fallback": "fill K_m_action_scale*C_action_scale with value, units, source leg, parent coefficient source, projection and no-bound-inversion guard.",
            "avoid": "calling the weighted-action survivor pure source-shadow; using MICROSCOPE bound to define the parent coefficient; dropping hidden/readout return channels silently.",
            "valid_for_claim": False,
        }
    ]


def build_doc(sources: Sequence[Mapping[str, object]], nohom: Sequence[Mapping[str, str]], split: Sequence[Mapping[str, str]], kmshadow: Sequence[Mapping[str, str]], gates: Sequence[Mapping[str, object]]) -> str:
    return f"""# 448 PPC4161 source-shadow constructor noHom proof or KmshadowCshadow first value

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4432 makes a real cut through the coupling problem:

- The exact no-Hom theorem is now a factorization theorem: `Coeff_active_source` must be generated only from `q(Phi)`, `theta_rep` and universal constants after common `G` calibration.
- Current MTS has the source-domain/label-forgetting side, but still lacks `ParentGenerate` exhaustion, constant-sector universality, hidden-marker absence and readout no-reentry.
- Pure source-only shadow is contract-killable under total-Hilbert variational source ownership.
- The surviving `S_matter=sum_A w_A S_A` countermodel is not pure source-only shadow; it is action-scale/constant-sector leakage.
- Hidden-marker and readout-projector returns are split into named channels instead of hidden inside `C_shadow`.
- No sourced numeric `K_m_shadow*C_shadow` exists; the old one-channel target remains only a bound/acquisition guard: `abs(K_m_shadow*C_shadow_total) <= {D_MHAT_ONE_CHANNEL_CEILING:.12e}`.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## Constructor No-Hom Gate

{table(nohom)}

## Source-Shadow Split Gate

{table(split)}

## K_m Shadow Value Gate

{table(kmshadow)}

## Claim Gates

{table(gates)}

## Decision

{table(decision_rows())}

## Next Target

{table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4432 - source-shadow constructor noHom proof or KmshadowCshadow first value

Marker: `{MARKER}`

Private checkpoint generated at `{STAMP}`.

## What changed

- Split `C_shadow` into pure source-only, action-scale, hidden-return and readout-projector pieces.
- Showed pure source-only shadow is contract-killable under total-Hilbert variational ownership.
- Reassigned the surviving `w_A S_A` countermodel to action-scale/constant-sector leakage.
- Kept `K_m_shadow*C_shadow_total` as a bound-only guard, not a theory value.

## Decision

{table(decision_rows())}

## Next target

{table(next_rows())}
"""


def upsert_marked_section(path: Path, marker: str, section: str) -> None:
    existing = text(path)
    start = f"<!-- {marker}:START -->"
    end = f"<!-- {marker}:END -->"
    block = f"{start}\n{section.rstrip()}\n{end}\n"
    if start in existing and end in existing:
        before = existing.split(start)[0]
        after = existing.split(end, 1)[1].lstrip("\n")
        write_text(path, before + block + after)
    else:
        separator = "" if existing.endswith("\n") or not existing else "\n"
        write_text(path, existing + separator + block)


def update_claims_register() -> None:
    rows = rows_from(CLAIMS_PATH) if CLAIMS_PATH.exists() else []
    fieldnames = list(rows[0].keys()) if rows else ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk", "sector", "evidence", "next_action", "risk"]
    rows = [row for row in rows if row.get("claim_id") != CLAIM_ID]
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "4432 splits C_shadow into pure source-only, action-scale, hidden-return and readout-projector pieces. Pure source-only shadow is contract-killable under total-Hilbert variational ownership, but the weighted-action countermodel survives as action-scale/constant-sector leakage. No parent-owned numeric K_m_shadow*C_shadow value exists; the bound remains an acquisition guard only.",
        "current_evidence": "4432 source register, derivation rows, constructor no-Hom output, shadow split output, K_m shadow value output, claim gates, decision, status, next target and validation CSV.",
        "status": "pure_source_shadow_contract_killable_survivors_reassigned_to_action_scale_hidden_readout",
        "next_test": "Prove action-scale/constant-sector universality or fill K_m_action_scale*C_action_scale with sourced parent provenance.",
        "key_risk": "Calling weighted action source-shadow instead of action-scale leakage; defining parent coefficients from empirical bounds; silently dropping hidden/readout returns.",
        "sector": "local_gr",
        "evidence": "4432 source register, derivation rows, constructor no-Hom output, shadow split output, K_m shadow value output, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Prove action-scale/constant-sector universality or fill K_m_action_scale*C_action_scale with sourced parent provenance.",
        "risk": "Calling weighted action source-shadow instead of action-scale leakage; defining parent coefficients from empirical bounds; silently dropping hidden/readout returns.",
    }
    rows.append({name: new_row.get(name, "") for name in fieldnames})
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_spine_and_packet() -> None:
    spine_section = f"""## 4432 local spine update: source-shadow split

4432 splits the old `C_shadow` bucket. A pure source-only RHS functional is not a live independent channel under the total-Hilbert variational source-owner contract; if parent-signed, it is zero. The surviving `w_A S_A` countermodel is action-scale/constant-sector leakage, while hidden-marker and readout-projector returns are separate channels. This makes the next route sharper: prove one action scale and universal constant sector, or fill `K_m_action_scale*C_action_scale`.
"""
    packet_section = f"""## 4432 packet update: no more single foggy source-shadow

`{PACKET_MARKER}`

Private packet result: `K_m_shadow*C_shadow` is not ready as one physical number. The pure source-only part is contract-killable; the real survivor is action-scale/constant-sector leakage plus named hidden/readout returns. The next proof target is single action measure/current normalization.
"""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    nohom = {row["row_id"]: row for row in rows_from(NOHOM_OUTPUT)}
    split = {row["row_id"]: row for row in rows_from(SPLIT_OUTPUT)}
    kmshadow = {row["row_id"]: row for row in rows_from(KMSHADOW_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in nohom.values()) and not any(row.get("valid_for_claim") == "True" for row in split.values()) and not any(row.get("valid_for_claim") == "True" for row in kmshadow.values())
    checks = [
        ("VAL4432_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4432_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4432_2_nohom_contract", nohom["NHOM4432_0_exact_factorized_noHom_contract"].get("current_status") == "CONSTRUCTOR_NOHOM_CONTRACT_READY_NONCLAIM", "factorized no-Hom contract staged"),
        ("VAL4432_3_current_reduction", nohom["NHOM4432_1_current_source_domain"].get("current_status") == "CONSTRUCTOR_NOHOM_REDUCES_TO_GENERATOR_EXHAUSTION_AND_REENTRY", "current route reduces to generator/reentry gaps"),
        ("VAL4432_4_constant_gap", nohom["NHOM4432_2_constant_sector_gap"].get("current_status") == "CONSTRUCTOR_NOHOM_COUNTERMODEL_SURVIVES", "constant-sector gap remains live"),
        ("VAL4432_5_pure_shadow_zero", split["SPLIT4432_0_pure_source_only_shadow"].get("current_status") == "SHADOW_PURE_SOURCE_ONLY_ZERO_CONTRACT_READY_NONCLAIM", "pure source-only shadow is contract-killable"),
        ("VAL4432_6_weighted_action_reassigned", split["SPLIT4432_1_weighted_action_shadow"].get("current_status") == "SHADOW_REASSIGNED_ACTION_SCALE_OR_BLOCK", "weighted action reassigned"),
        ("VAL4432_7_hidden_readout_split", split["SPLIT4432_2_hidden_marker_shadow"].get("current_status") == "SHADOW_REASSIGNED_HIDDEN_RETURN" and split["SPLIT4432_3_readout_projector_shadow"].get("current_status") == "SHADOW_REASSIGNED_READOUT_PROJECTOR", "hidden/readout channels split"),
        ("VAL4432_8_zero_projection_nonclaim", kmshadow["KM4432_0_pure_source_zero_projection"].get("current_status") == "KM_SHADOW_PRODUCT_INPUT_INVALID_NONCLAIM", "pure source zero projection remains nonclaim"),
        ("VAL4432_9_action_scale_reassignment", kmshadow["KM4432_1_action_scale_reassignment"].get("current_status") == "KM_SHADOW_PRODUCT_REASSIGNED_NOT_NUMERIC", "action-scale product reassigned"),
        ("VAL4432_10_total_bound_only", kmshadow["KM4432_4_original_Kmshadow_bound_target"].get("current_status") == "KM_SHADOW_PRODUCT_BOUND_TARGET_ONLY", "original K_m_shadow total bound remains bound only"),
        ("VAL4432_11_no_claim_outputs", no_claims, "no output row is claim-ready"),
        ("VAL4432_12_claim_gate_no_claim", any(row["gate_id"] == "CG4432_8_no_claim_outputs" and row["passed"] == "True" for row in gates), "claim gate explicitly blocks public claim"),
        ("VAL4432_13_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-273"),
        ("VAL4432_14_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4432_15_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4432_16_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4432_17_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4432_18_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4432_19_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(NOHOM_INPUT, nohom_input_rows())
    write_csv(NOHOM_OUTPUT, evaluate_nohom_rows(NOHOM_INPUT))
    write_csv(SPLIT_INPUT, shadow_split_input_rows())
    write_csv(SPLIT_OUTPUT, evaluate_shadow_split_rows(SPLIT_INPUT))
    write_csv(KMSHADOW_INPUT, kmshadow_input_rows())
    write_csv(KMSHADOW_OUTPUT, evaluate_kmshadow_rows(KMSHADOW_INPUT))
    nohom = rows_from(NOHOM_OUTPUT)
    split = rows_from(SPLIT_OUTPUT)
    kmshadow = rows_from(KMSHADOW_OUTPUT)
    gates = claim_gate_rows(nohom, split, kmshadow)
    write_csv(CLAIM_GATES, gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), nohom, split, kmshadow, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()
