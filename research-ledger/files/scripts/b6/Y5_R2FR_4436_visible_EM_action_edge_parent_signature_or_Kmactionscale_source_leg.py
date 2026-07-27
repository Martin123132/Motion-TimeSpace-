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

from action_density_edge_gate import evaluate_k_source_leg_rows, write_csv  # noqa: E402
from visible_em_action_signature_gate import evaluate_signature_rows  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4436"
CLAIM_ID = "L-277"
MARKER = "PPC4161_VISIBLE_EM_ACTION_EDGE_PARENT_SIGNATURE_OR_KMACTIONSCALE_SOURCE_LEG_4436"
PACKET_MARKER = "PPC4161_PACKET_VISIBLE_EM_ACTION_EDGE_PARENT_SIGNATURE_OR_KMACTIONSCALE_SOURCE_LEG_4436"
DECISION = "VISIBLE_EM_EDGE_PARENT_SIGNED_INSIDE_STANDARD_VISIBLE_IMPORT_BRANCH_SCALE_CURRENT_LOCKS_REMAIN_KMACTIONSCALE_SOURCE_LEG_NOT_NUMERIC"
NEXT_TARGET = "4437-Y5-R2FR-EM-charge-current-unique-F2-owner-or-Kmactionscale-source-value.md"

FORMAL_PATH = FORMAL / "452-PPC4161-visible-EM-action-edge-parent-signature-or-Kmactionscale-source-leg.md"
DOC_PATH = POST / "4436-Y5-R2FR-visible-EM-action-edge-parent-signature-or-Kmactionscale-source-leg.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4436_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4436_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4436_DERIVATION_ROWS.csv"
SIGNATURE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4436_VISIBLE_EM_SIGNATURE_INPUT.csv"
SIGNATURE_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4436_VISIBLE_EM_SIGNATURE_OUTPUT.csv"
STRESS_EXCHANGE_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4436_EM_STRESS_EXCHANGE_ROWS.csv"
RESIDUAL_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4436_EM_SCALE_CURRENT_RESIDUAL_ROWS.csv"
KLEG_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4436_K_ACTION_SOURCE_LEG_INPUT.csv"
KLEG_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4436_K_ACTION_SOURCE_LEG_OUTPUT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4436_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4436_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4436_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4436_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "visible_em_action_signature_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4436_visible_EM_action_edge_parent_signature_or_Kmactionscale_source_leg.py"
ACTION_EDGE_GATE = SCRIPT_DIR / "action_density_edge_gate.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4435 = SOURCE_DIR / "P8_Y5_R2FR_4435_NEXT_TARGET.csv"
FORMAL_451 = FORMAL / "451-PPC4161-parent-owned-action-density-graph-edge-certificate-or-first-Kmactionscale-source-leg.md"
FORMAL_191 = FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md"
FORMAL_223 = FORMAL / "223-PPC4161-EM-Poynting-Hodge-source-owner-lock.md"
FORMAL_277 = FORMAL / "277-PPC4161-visible-EM-action-domain-fork-or-constitutive-bound.md"
LEDGER3463 = SOURCE_DIR / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv"
ALPHA3464 = SOURCE_DIR / "P8_Y5_R2FR_3464_EM_ALPHA_CHARGE_OWNER_AUDIT.csv"
OWNER3465 = SOURCE_DIR / "P8_Y5_R2FR_3465_EM_OWNER_PACKAGE_AUDIT.csv"
VEM3505 = SOURCE_DIR / "P8_Y5_R2FR_3505_VISIBLE_EM_ACTION_DOMAIN_THEOREM.csv"
VEB3505 = SOURCE_DIR / "P8_EM_visible_action_domain_exhaustion_no_chiEM_bound_vector.csv"
RED3506 = SOURCE_DIR / "P8_Y5_R2FR_3506_RESIDUAL_REDUCTION_MAP.csv"
BOUND3503 = SOURCE_DIR / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv"
POYNTING3502 = SOURCE_DIR / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv"
ALPHA_RESIDUAL3507 = SOURCE_DIR / "P8_EM_scalar_coupling_owner_alpha_residual.csv"
TNG1470 = SOURCE_DIR / "P8_Y5_R10_1470_TYPED_VISIBLE_ACTION_GRAMMAR_ATTEMPT.csv"
KLEG4435 = SOURCE_DIR / "P8_Y5_R2FR_4435_K_ACTION_SOURCE_LEG_OUTPUT.csv"

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
        {"source_id": "SRC4436_00_4435_next", "path": NEXT_4435, "needle": "4436-Y5-R2FR-visible-EM-action-edge-parent-signature", "role": "4435 handoff."},
        {"source_id": "SRC4436_01_451_formal", "path": FORMAL_451, "needle": "EDGE4435_1_L_to_EM_reduction", "role": "first edge reduction."},
        {"source_id": "SRC4436_02_277_visible_branch", "path": FORMAL_277, "needle": "signed only inside the 4210 standard-visible-import branch", "role": "standard visible branch signature."},
        {"source_id": "SRC4436_03_191_poynting_owner", "path": FORMAL_191, "needle": "Poynting vector is not a separate background field", "role": "Maxwell-Hodge/Poynting theorem."},
        {"source_id": "SRC4436_04_223_owner_lock", "path": FORMAL_223, "needle": "So the Poynting vector is real physical flow", "role": "Poynting once-only lock."},
        {"source_id": "SRC4436_05_3463_stress_ledger", "path": LEDGER3463, "needle": "EM3463_2_poynting", "role": "EM stress and exchange ledger."},
        {"source_id": "SRC4436_06_3464_alpha_owner", "path": ALPHA3464, "needle": "EAC3464_5_verdict", "role": "alpha/current normalization gap."},
        {"source_id": "SRC4436_07_3465_owner_package", "path": OWNER3465, "needle": "EMO3465_5_verdict", "role": "EM owner package gap."},
        {"source_id": "SRC4436_08_3505_visible_domain", "path": VEM3505, "needle": "VEM3505_7_verdict", "role": "visible EM action-domain verdict."},
        {"source_id": "SRC4436_09_3505_bound_vector", "path": VEB3505, "needle": "VEB3505_6_C_XF2", "role": "unique F2/source-prefactor guard."},
        {"source_id": "SRC4436_10_3506_reduction", "path": RED3506, "needle": "RED3506_5_C_XF2", "role": "scalar F2 coupling throat."},
        {"source_id": "SRC4436_11_3503_bound_vector", "path": BOUND3503, "needle": "EMB3503_3_C_JQ", "role": "current normalization guard."},
        {"source_id": "SRC4436_12_3502_poynting_vector", "path": POYNTING3502, "needle": "EMF3502_5_matter_EM_internal_exchange", "role": "internal exchange / Poynting component map."},
        {"source_id": "SRC4436_13_3507_alpha_residual", "path": ALPHA_RESIDUAL3507, "needle": "ARE3507_1_C_XF2", "role": "alpha scalar coupling residual."},
        {"source_id": "SRC4436_14_tng1470", "path": TNG1470, "needle": "TNG1470_1_type_theorem", "role": "typed no-hidden-visible coefficient theorem."},
        {"source_id": "SRC4436_15_kleg4435", "path": KLEG4435, "needle": "KLEG4435_2_EM_action_scale_component", "role": "previous EM action-scale source-leg row."},
        {"source_id": "SRC4436_16_gate", "path": GATE_PATH, "needle": "def evaluate_signature_row", "role": "4436 gate script."},
        {"source_id": "SRC4436_17_generator", "path": GENERATOR_PATH, "needle": "CHECKPOINT = \"4436\"", "role": "4436 generator script."},
        {"source_id": "SRC4436_18_action_edge_gate", "path": ACTION_EDGE_GATE, "needle": "def evaluate_k_source_leg_row", "role": "K source-leg evaluator."},
    ]


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for spec in source_specs():
        source_path = Path(spec["path"])
        needle = str(spec["needle"])
        content = text(source_path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "path": str(source_path),
                "path_exists": source_path.exists(),
                "needle": needle,
                "needle_found": needle in content,
                "line_number": line_of(source_path, needle),
                "role": spec["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "VEM4436_0_standard_visible_branch_edge_signature",
            "claim": "The visible EM edge is parent-signed inside the standard visible import branch.",
            "derivation": "4261 writes S_visible_parent=S_vis_standard[g_obs,A,psi,theta_obs]+DeltaS_MTS_visible and sets DeltaS_MTS_visible=0 before variation in the 4210 private local-GR baseline. Since S_vis_standard contains S_Maxwell-Hodge[A,g_obs;alpha_EM_obs] and binding/current terms on the same observed Hilbert line, the L_parent->EM action edge is signed in that branch.",
            "consequence": "The 4435 edge gap is not blank: the standard local branch owns the EM Hodge/stress/Poynting edge. This is still private and branch-conditional, not a global MTS Maxwell derivation.",
            "status": "BRANCH_EXACT_EDGE_SIGNATURE_SCALE_GATES_OPEN",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "VEM4436_1_maxwell_hodge_stress_exchange",
            "claim": "Poynting is a Hilbert stress-current component, not an extra source force.",
            "derivation": "Variation of S_MH[A,g_obs] gives T_EM. In a local frame T_EM^{0i} is the Poynting flux, and Maxwell-matter exchange obeys nabla_mu T_EM^{mu nu}=-F^{nu lambda}J_lambda with the opposite matter term. Therefore only T_matter+T_EM is conserved and sourced as one Hilbert current.",
            "consequence": "The Poynting intuition is useful, but the safe route is once-only ownership inside T_total; adding a second background Poynting force would double-count.",
            "status": "EXACT_CONDITIONAL_STRESS_EXCHANGE_THEOREM",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "VEM4436_2_global_parent_signature_not_proved",
            "claim": "The global MTS parent has not derived the same visible EM action domain.",
            "derivation": "3505 keeps the visible EM action-domain theorem as exact but not parent-derived, while 3506 and 3465 retain independent constitutive, hidden Hodge, F2, current, readout and radiative counterbranches.",
            "consequence": "The edge can be used only as a private standard-branch certificate. It cannot be promoted to global local-GR/Maxwell evidence.",
            "status": "GLOBAL_PARENT_SIGNATURE_RETAINED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "VEM4436_3_scale_current_coupling_throat",
            "claim": "The EM action edge does not yet supply the calibrated source-coupling value.",
            "derivation": "The action edge fixes the Hodge/stress owner in the branch, but alpha_EM, charge-current normalization, unique F2/no hidden f_X(Phi)F2, and radiative/readout preservation are still separate owner locks.",
            "consequence": "This is the exact coupling throat: close unique F2 plus current owner, or keep K_m_EM_action_scale*C_EM_action_scale as a bound-only product.",
            "status": "COUPLING_SCALE_CURRENT_LOCKS_OPEN",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "VEM4436_4_no_bound_inversion",
            "claim": "The local Ti/Pt-style bound remains a ceiling, not a theory coefficient.",
            "derivation": f"The one-channel scale target remains abs(product)<={D_MHAT_ONE_CHANNEL_CEILING:.12e}; this constrains any nonzero residual product but cannot define K_m_action_scale, C_action_scale or an EM binding/source leg.",
            "consequence": "The next numerical route must source parent coefficients and source legs independently, then compare them to the bound.",
            "status": "BOUND_ONLY_NOT_COEFFICIENT",
            "valid_for_claim": False,
        },
    ]


def signature_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "EMS4436_0_standard_visible_import_branch",
            "branch": "4210 standard-visible import / private local-GR baseline",
            "action_block_present": True,
            "observed_hodge_owned": True,
            "same_parent_action_line": True,
            "parent_owned_action_domain": True,
            "unique_F2_no_extra_prefactor": False,
            "charge_current_owner": False,
            "fixed_representation_constants": True,
            "no_species_source_prefactor": True,
            "readout_after_variation": True,
            "radiative_closure": False,
            "poynting_once_only": True,
            "source_path": str(FORMAL_277),
            "input_valid": True,
            "valid_for_claim": False,
            "notes": "Branch-level EM action edge is signed for Hodge/stress/Poynting ownership; scale/current/radiative locks remain open.",
        },
        {
            "row_id": "EMS4436_1_global_parent_MTS_deformation_branch",
            "branch": "global MTS visible deformation branch",
            "action_block_present": True,
            "observed_hodge_owned": False,
            "same_parent_action_line": False,
            "parent_owned_action_domain": False,
            "unique_F2_no_extra_prefactor": False,
            "charge_current_owner": False,
            "fixed_representation_constants": False,
            "no_species_source_prefactor": False,
            "readout_after_variation": False,
            "radiative_closure": False,
            "poynting_once_only": False,
            "source_path": str(VEM3505),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Global parent visible EM generator remains unsigned; all deformation residuals stay live.",
        },
        {
            "row_id": "EMS4436_2_poynting_once_only_guard",
            "branch": "Maxwell-Hodge Hilbert stress branch",
            "action_block_present": True,
            "observed_hodge_owned": True,
            "same_parent_action_line": True,
            "parent_owned_action_domain": True,
            "unique_F2_no_extra_prefactor": False,
            "charge_current_owner": False,
            "fixed_representation_constants": True,
            "no_species_source_prefactor": True,
            "readout_after_variation": True,
            "radiative_closure": False,
            "poynting_once_only": True,
            "source_path": str(FORMAL_191),
            "input_valid": True,
            "valid_for_claim": False,
            "notes": "Poynting is owned once as EM Hilbert flux; open radiation/normalization gates are not erased.",
        },
        {
            "row_id": "EMS4436_3_unique_F2_current_scale_lock",
            "branch": "EM coupling normalization branch",
            "action_block_present": True,
            "observed_hodge_owned": True,
            "same_parent_action_line": True,
            "parent_owned_action_domain": False,
            "unique_F2_no_extra_prefactor": False,
            "charge_current_owner": False,
            "fixed_representation_constants": False,
            "no_species_source_prefactor": True,
            "readout_after_variation": True,
            "radiative_closure": False,
            "poynting_once_only": True,
            "source_path": str(OWNER3465),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "This is the unresolved alpha/current/unique-F2 owner lock.",
        },
        {
            "row_id": "EMS4436_4_readout_radiative_closure_lock",
            "branch": "effective/readout preservation branch",
            "action_block_present": True,
            "observed_hodge_owned": True,
            "same_parent_action_line": True,
            "parent_owned_action_domain": False,
            "unique_F2_no_extra_prefactor": False,
            "charge_current_owner": False,
            "fixed_representation_constants": False,
            "no_species_source_prefactor": True,
            "readout_after_variation": False,
            "radiative_closure": False,
            "poynting_once_only": True,
            "source_path": str(VEB3505),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Readout/radiative regeneration can reintroduce EM coefficient dependence unless separately signed or bounded.",
        },
    ]


def stress_exchange_rows() -> List[Dict[str, object]]:
    return [
        {"row_id": "STX4436_0_action", "object": "S_MH[A,g_obs]", "result": "standard visible branch owns Maxwell-Hodge action block", "formula": "S_MH=-1/4 int sqrt(-g_obs) F^2 + int A.J", "status": "BRANCH_SIGNED_NONCLAIM", "source_path": str(FORMAL_277), "valid_for_claim": False},
        {"row_id": "STX4436_1_stress", "object": "T_EM", "result": "Hilbert stress follows from metric/coframe variation", "formula": "T_EM^{mu nu}=F^{mu alpha}F^nu_alpha-1/4 g_obs^{mu nu}F^2", "status": "EXACT_CONDITIONAL", "source_path": str(LEDGER3463), "valid_for_claim": False},
        {"row_id": "STX4436_2_poynting", "object": "S_Poynting", "result": "Poynting flux is T_EM^{0i} or -T_EM(n,e_i)", "formula": "S=E x H", "status": "ONCE_ONLY_HILBERT_FLUX", "source_path": str(FORMAL_191), "valid_for_claim": False},
        {"row_id": "STX4436_3_exchange", "object": "matter-EM exchange", "result": "Lorentz force is internal exchange, not total source nonconservation", "formula": "nabla T_EM=-FJ; nabla T_matter=+FJ", "status": "EXACT_CONDITIONAL", "source_path": str(POYNTING3502), "valid_for_claim": False},
    ]


def residual_rows() -> List[Dict[str, object]]:
    return [
        {"residual_id": "RES4436_0_C_XF2", "symbol": "C_XF2", "meaning": "hidden/motion/time coefficient multiplying F_Q^2", "current_status": "UNIQUE_F2_PARENT_LOCK_OPEN", "next_action": "derive no independent F2 coefficient from parent typed action grammar or source a bound", "source_path": str(RED3506), "valid_for_claim": False},
        {"residual_id": "RES4436_1_C_JQ", "symbol": "C_JQ", "meaning": "charge/current normalization ambiguity", "current_status": "CHARGE_CURRENT_OWNER_OPEN", "next_action": "derive parent current/representation charge owner and fixed normalization", "source_path": str(BOUND3503), "valid_for_claim": False},
        {"residual_id": "RES4436_2_b_alpha", "symbol": "b_alpha_X", "meaning": "vertical derivative of effective alpha", "current_status": "ALPHA_SAME_OWNER_RELATION_OPEN", "next_action": "prove same-owner relation 2 z_g = z_lambda or keep alpha/WEP/clock bound", "source_path": str(ALPHA_RESIDUAL3507), "valid_for_claim": False},
        {"residual_id": "RES4436_3_Phi_EM_rad", "symbol": "Phi_EM_rad", "meaning": "radiative/background Poynting boundary flux", "current_status": "BOUNDARY_FLUX_RETAINED", "next_action": "prove closed stationary collar or source flux over test window", "source_path": str(POYNTING3502), "valid_for_claim": False},
        {"residual_id": "RES4436_4_C_EM_readout", "symbol": "C_EM_readout", "meaning": "readout/loop regeneration of EM coefficient", "current_status": "READOUT_RADIATIVE_CLOSURE_OPEN", "next_action": "prove readout-after-variation and EFT preservation or fill product bounds", "source_path": str(OWNER3465), "valid_for_claim": False},
    ]


def kleg_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "KLEG4436_0_poynting_extra_side_channel_zero",
            "product": "C_EM_extra_Poynting_side_channel",
            "coefficient_value": "DERIVED_ZERO",
            "units": "dimensionless",
            "parent_coefficient_source": str(FORMAL_191),
            "source_leg": "Maxwell-Hodge Hilbert stress once-only Poynting flux",
            "source_leg_units": "dimensionless_branch_indicator",
            "projection": "extra bulk/background Poynting source coefficient = 0 inside once-only Maxwell-Hodge branch",
            "bound_value": "0",
            "no_bound_inversion_guard": True,
            "source_path": str(FORMAL_191),
            "input_valid": True,
            "valid_for_claim": False,
            "notes": "This closes only the double-counted Poynting side-channel inside the private branch; it is not a numeric K_m_action_scale value.",
        },
        {
            "row_id": "KLEG4436_1_EM_action_scale_component",
            "product": "K_m_EM_action_scale*C_EM_action_scale",
            "coefficient_value": "MISSING_PARENT_COEFFICIENT",
            "units": "dimensionless",
            "parent_coefficient_source": "MISSING_UNIQUE_F2_CURRENT_ALPHA_OWNER",
            "source_leg": "MISSING_EM_BINDING_OR_ALPHA_CURRENT_SOURCE_LEG",
            "source_leg_units": "dimensionless_or_binding_fraction",
            "projection": f"{DELTA_Q_MHAT:.5f}*abs(K_m_EM_action_scale*C_EM_action_scale) <= {ETA_BOUND:.12e}",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "no_bound_inversion_guard": True,
            "source_path": str(KLEG4435),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Still missing the parent coefficient/source leg after EM edge signature split.",
        },
        {
            "row_id": "KLEG4436_2_bound_target_only",
            "product": "K_m_EM_action_scale*C_EM_action_scale_effective",
            "coefficient_value": f"BOUND_ONLY_{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "units": "dimensionless",
            "parent_coefficient_source": "MISSING_PARENT_SOURCE",
            "source_leg": "MISSING_SOURCE_LEG",
            "source_leg_units": "MISSING_SOURCE_LEG_UNITS",
            "projection": f"abs(K_m_EM_action_scale*C_EM_action_scale_effective) <= {D_MHAT_ONE_CHANNEL_CEILING:.12e} only as one-channel target",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "no_bound_inversion_guard": True,
            "source_path": str(KLEG4435),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Bound target only; no inversion into a theory coefficient.",
        },
    ]


def claim_gate_rows(signatures: Sequence[Mapping[str, str]], klegs: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    signature_rows = {row["row_id"]: row for row in signatures}
    kleg_rows = {row["row_id"]: row for row in klegs}
    no_claims = not any(row.get("valid_for_claim") == "True" for row in signatures) and not any(row.get("valid_for_claim") == "True" for row in klegs)
    return [
        {"gate_id": "CG4436_0_standard_branch_edge_signature", "claim": "standard visible branch signs EM action edge", "passed": signature_rows["EMS4436_0_standard_visible_import_branch"].get("current_status") == "VISIBLE_EM_EDGE_SIGNATURE_READY_SCALE_GATES_OPEN", "valid_for_claim": False, "detail": "Hodge/stress/Poynting edge signed; scale/current/radiative locks open."},
        {"gate_id": "CG4436_1_global_parent_not_signed", "claim": "global MTS parent EM generator remains unsigned", "passed": signature_rows["EMS4436_1_global_parent_MTS_deformation_branch"].get("valid_for_claim") == "False", "valid_for_claim": False, "detail": "Global deformation branch keeps residuals live."},
        {"gate_id": "CG4436_2_poynting_once_only", "claim": "extra Poynting background source is zero only inside once-only Maxwell-Hodge branch", "passed": kleg_rows["KLEG4436_0_poynting_extra_side_channel_zero"].get("current_status") == "K_ACTION_SOURCE_LEG_READY_NONCLAIM", "valid_for_claim": False, "detail": "Closes double counting, not the action-scale coupling value."},
        {"gate_id": "CG4436_3_kmactionscale_missing", "claim": "K_m_EM_action_scale source leg remains missing", "passed": kleg_rows["KLEG4436_1_EM_action_scale_component"].get("current_status") == "K_ACTION_SOURCE_LEG_CONTRACT_ONLY", "valid_for_claim": False, "detail": "Unique F2/current/alpha owner must be derived or sourced."},
        {"gate_id": "CG4436_4_bound_not_coefficient", "claim": "bound-only product is not a coefficient source", "passed": kleg_rows["KLEG4436_2_bound_target_only"].get("current_status") == "K_ACTION_SOURCE_LEG_BOUND_TARGET_ONLY", "valid_for_claim": False, "detail": "No bound inversion."},
        {"gate_id": "CG4436_5_residual_vector", "claim": "scale/current residual vector staged", "passed": len(residual_rows()) == 5, "valid_for_claim": False, "detail": "C_XF2, C_JQ, b_alpha, Phi_EM_rad, C_EM_readout are separated."},
        {"gate_id": "CG4436_6_no_public_claim", "claim": "4436 emits no local-GR/Maxwell/R10 public claim", "passed": no_claims, "valid_for_claim": False, "detail": "Private branch progress only."},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4436_0",
            "decision": DECISION,
            "summary": "4436 turns the visible EM handoff into a real branch-level result: inside the standard visible import/private local-GR branch, the Maxwell-Hodge action owns the EM stress and Poynting flux, so L_parent->EM is signed as an action edge for Hodge/stress purposes. The global MTS parent still has not derived that EM generator, and the calibrated coupling scale remains open through unique F2, charge-current/alpha owner, readout/radiative closure and source-leg values.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4436_0_edge", "status": "VISIBLE_EM_EDGE_SIGNED_IN_STANDARD_VISIBLE_BRANCH", "detail": "The first graph edge is not merely template-level in the private standard branch; it has Maxwell-Hodge action ownership there.", "valid_for_claim": False},
        {"status_id": "STAT4436_1_poynting", "status": "POYNTING_ONCE_ONLY_SIDE_CHANNEL_ZERO_BRANCH", "detail": "Extra Poynting background force is killed only as double counting inside the once-only Hilbert stress branch.", "valid_for_claim": False},
        {"status_id": "STAT4436_2_coupling", "status": "UNIQUE_F2_CHARGE_CURRENT_ALPHA_OWNER_OPEN", "detail": "The actual coupling throat is now C_XF2/C_JQ/b_alpha/radiative-readout, not generic EM stress.", "valid_for_claim": False},
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4436_0",
            "target": NEXT_TARGET,
            "objective": "Derive the EM charge/current plus unique F2 owner, or fill the first parent-sourced K_m_EM_action_scale value.",
            "derive_first": "prove a same-owner theorem: fixed Maxwell kinetic normalization, fixed charge-current representation, and alpha readout share one parent level so hidden/motion/time derivatives cannot generate C_XF2, C_JQ or b_alpha.",
            "fallback": "source numeric parent coefficient/source-leg rows for K_m_EM_action_scale*C_EM_action_scale with units, projection, and no-bound-inversion guard.",
            "avoid": "treating the standard visible branch as global MTS adoption; using Poynting twice; using the experimental ceiling as a coefficient.",
            "valid_for_claim": False,
        }
    ]


def build_doc(
    sources: Sequence[Mapping[str, object]],
    signatures: Sequence[Mapping[str, str]],
    klegs: Sequence[Mapping[str, str]],
    gates: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 452 PPC4161 visible EM action edge parent signature or Kmactionscale source leg

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4436 takes the leap that 4435 set up.

- The `L_parent -> EM` graph edge is now signed inside the **standard visible import / private local-GR branch**: `S_Maxwell-Hodge[A,g_obs]` lives on the same observed Hilbert action line, so EM stress and Poynting flux are owned there.
- The exact stress identity remains: Poynting is a component of `T_EM`, and matter-EM Lorentz force is internal exchange inside `T_matter + T_EM`.
- This is not a global MTS Maxwell derivation. Outside the standard visible branch, constitutive/Hodge, hidden `F^2`, current normalization, alpha/readout and radiation counterbranches remain live.
- The actual coupling throat is now sharper: `C_XF2`, `C_JQ`, `b_alpha_X`, `Phi_EM_rad`, and `C_EM_readout`.
- The finite `K_m_EM_action_scale*C_EM_action_scale` route remains source-leg missing; the local bound is still only a ceiling.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## Visible EM Signature Gate

{table(signatures)}

## EM Stress Exchange Rows

{table(stress_exchange_rows())}

## Scale / Current Residual Rows

{table(residual_rows())}

## K Action-Scale Source Leg Gate

{table(klegs)}

## Claim Gates

{table(gates)}

## Decision

{table(decision_rows())}

## Next Target

{table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4436 - visible EM action edge parent signature or Kmactionscale source leg

Marker: `{MARKER}`

Private checkpoint generated at `{STAMP}`.

## What changed

- Promoted the visible EM edge to a branch-level action signature inside the standard visible import branch.
- Kept global MTS EM action ownership unsigned.
- Killed only the double-counted extra Poynting side-channel inside Maxwell-Hodge Hilbert stress.
- Isolated the real coupling throat: unique `F^2`, charge/current owner, alpha/readout/radiative closure, and the missing `K_m_EM_action_scale` source leg.

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
        "domain": "em_local_gr",
        "claim": "4436 parent-signs the L_parent->EM action edge only inside the standard visible import/private local-GR branch: Maxwell-Hodge owns EM stress and Poynting flux there. Global MTS visible EM generator, unique F2/current/alpha owner, readout/radiative closure and K_m_EM_action_scale source leg remain unsigned.",
        "current_evidence": "4436 source register, derivation rows, visible EM signature gate, EM stress exchange rows, residual rows, K source-leg rows, claim gates, decision, status, next target and validation CSV.",
        "status": "visible_EM_edge_signed_inside_standard_visible_branch_scale_current_locks_open_nonclaim",
        "next_test": "Derive same-owner unique F2 plus charge-current/alpha theorem or fill first K_m_EM_action_scale source leg.",
        "key_risk": "Promoting branch EM import to global MTS adoption; double-counting Poynting; using a bound as a coefficient.",
        "sector": "em_local_gr",
        "evidence": "4436 source register, derivation rows, visible EM signature gate, EM stress exchange rows, residual rows, K source-leg rows, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Derive same-owner unique F2 plus charge-current/alpha theorem or fill first K_m_EM_action_scale source leg.",
        "risk": "Promoting branch EM import to global MTS adoption; double-counting Poynting; using a bound as a coefficient.",
    }
    rows.append({fieldname: new_row.get(fieldname, "") for fieldname in fieldnames})
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_spine_and_packet() -> None:
    spine_section = """## 4436 local spine update: visible EM edge signed in standard branch

4436 turns the first graph edge from a mere template into a branch-level certificate inside the standard visible import/private local-GR branch. Maxwell-Hodge owns EM stress and Poynting once there, so the next hard problem is no longer generic EM stress ownership. The hard problem is the coupling throat: unique `F^2`, charge/current and alpha owner, readout/radiative preservation, and a real `K_m_EM_action_scale` source leg.
"""
    packet_section = f"""## 4436 packet update: EM edge signed, coupling throat isolated

`{PACKET_MARKER}`

Private packet result: use the standard visible branch as a legitimate local EM stress/Poynting edge certificate, but do not globalize it. Next, attack the same-owner theorem for `C_XF2`, `C_JQ` and `b_alpha_X`, or fill a sourced `K_m_EM_action_scale*C_EM_action_scale` row.
"""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    signatures = {row["row_id"]: row for row in rows_from(SIGNATURE_OUTPUT)}
    klegs = {row["row_id"]: row for row in rows_from(KLEG_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in signatures.values()) and not any(row.get("valid_for_claim") == "True" for row in klegs.values())
    checks = [
        ("VAL4436_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4436_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4436_2_standard_branch_edge", signatures["EMS4436_0_standard_visible_import_branch"].get("current_status") == "VISIBLE_EM_EDGE_SIGNATURE_READY_SCALE_GATES_OPEN", "standard branch signs EM edge but leaves scale gates open"),
        ("VAL4436_3_global_not_signed", signatures["EMS4436_1_global_parent_MTS_deformation_branch"].get("valid_for_claim") == "False", "global MTS visible EM generator remains unsigned"),
        ("VAL4436_4_poynting_guard", klegs["KLEG4436_0_poynting_extra_side_channel_zero"].get("current_status") == "K_ACTION_SOURCE_LEG_READY_NONCLAIM", "extra Poynting side-channel killed only as branch nonclaim"),
        ("VAL4436_5_kleg_missing", klegs["KLEG4436_1_EM_action_scale_component"].get("current_status") == "K_ACTION_SOURCE_LEG_CONTRACT_ONLY", "EM action-scale source leg remains missing"),
        ("VAL4436_6_bound_only", klegs["KLEG4436_2_bound_target_only"].get("current_status") == "K_ACTION_SOURCE_LEG_BOUND_TARGET_ONLY", "bound-only row remains non-coefficient"),
        ("VAL4436_7_residual_vector", len(rows_from(RESIDUAL_ROWS)) == 5 and "RES4436_0_C_XF2" in text(RESIDUAL_ROWS), "scale/current residual vector written"),
        ("VAL4436_8_stress_rows", len(rows_from(STRESS_EXCHANGE_ROWS)) == 4 and "STX4436_2_poynting" in text(STRESS_EXCHANGE_ROWS), "EM stress exchange rows written"),
        ("VAL4436_9_no_claim_outputs", no_claims, "no output row is claim-ready"),
        ("VAL4436_10_claim_gate_no_claim", any(row["gate_id"] == "CG4436_6_no_public_claim" and row["passed"] == "True" for row in gates), "claim gate explicitly blocks public claim"),
        ("VAL4436_11_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-277"),
        ("VAL4436_12_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4436_13_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4436_14_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4436_15_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4436_16_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4436_17_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(SIGNATURE_INPUT, signature_input_rows())
    write_csv(SIGNATURE_OUTPUT, evaluate_signature_rows(SIGNATURE_INPUT))
    write_csv(STRESS_EXCHANGE_ROWS, stress_exchange_rows())
    write_csv(RESIDUAL_ROWS, residual_rows())
    write_csv(KLEG_INPUT, kleg_input_rows())
    write_csv(KLEG_OUTPUT, evaluate_k_source_leg_rows(KLEG_INPUT))
    signatures = rows_from(SIGNATURE_OUTPUT)
    klegs = rows_from(KLEG_OUTPUT)
    gates = claim_gate_rows(signatures, klegs)
    write_csv(CLAIM_GATES, gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), signatures, klegs, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()
