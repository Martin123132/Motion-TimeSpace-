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

from residual_coefficient_status_gate import evaluate_targets, read_csv, write_csv  # noqa: E402
from residual_coefficient_status_gate import evaluate_coefficient_row  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4450"
CLAIM_ID = "L-292"
MARKER = "PPC4161_EXTRA_INVARIANT_RESIDUAL_COEFFICIENT_STATUS_AFTER_AMF_4450"
PACKET_MARKER = "PPC4161_PACKET_EXTRA_INVARIANT_RESIDUAL_COEFFICIENT_STATUS_AFTER_AMF_4450"
DECISION = "A_MF_ADOPTION_INTEGRATED_RESIDUAL_COEFFICIENTS_SPLIT_INTO_PRIVATE_ROUTED_SUBSET_AND_FINITE_SURVIVORS_cT_SPIN_SELECTED_NEXT_NONCLAIM"
NEXT_TARGET = "4451-Y5-R2FR-torsion-spin-residual-cT-zero-or-contact-bound.md"

FORMAL_PATH = FORMAL / "466-PPC4161-extra-invariant-residual-coefficient-map-to-PPN-R10-clocks-or-parent-scale-law.md"
DOC_PATH = POST / "4450-Y5-R2FR-extra-invariant-residual-coefficient-map-to-PPN-R10-clocks-or-parent-scale-law.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4450_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4450_SOURCE_REGISTER.csv"
COEFF_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4450_COEFFICIENT_STATUS_INPUT.csv"
COEFF_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4450_COEFFICIENT_STATUS_OUTPUT.csv"
TARGET_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4450_TARGET_SCORE_INPUT.csv"
TARGET_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4450_TARGET_SCORE_OUTPUT.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4450_DERIVATION_ROWS.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4450_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4450_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4450_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4450_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "residual_coefficient_status_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4450_extra_invariant_residual_coefficient_map_to_PPN_R10_clocks_or_parent_scale_law.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4449 = SOURCE_DIR / "P8_Y5_R2FR_4449_NEXT_TARGET.csv"
FORMAL_465 = FORMAL / "465-PPC4161-parent-motion-frame-A-MF-adoption-or-derived-flow-symmetry.md"
FORMAL_200 = FORMAL / "200-PPC4161-Palatini-IR-normal-form-selector-under-AMF.md"
FORMAL_201 = FORMAL / "201-PPC4161-extra-invariant-residual-coefficient-map.md"
FORMAL_202 = FORMAL / "202-PPC4161-same-coframe-source-memory-zero-law.md"
FORMAL_222 = FORMAL / "222-PPC4161-calibrated-GN-bridge-and-source-charge-caveat.md"
FORMAL_223 = FORMAL / "223-PPC4161-EM-Poynting-Hodge-source-owner-lock.md"
FORMAL_295 = FORMAL / "295-PPC4161-residual-EFT-coefficient-zero-or-local-test-bound-pack.md"
OUT_4184_LEDGER = SOURCE_DIR / "P8_Y5_R2FR_4184_RESIDUAL_EFT_BOUND_LEDGER.csv"
OUT_4185_MAP = SOURCE_DIR / "P8_Y5_R2FR_4185_RESIDUAL_COEFFICIENT_ARENA_MAP.csv"
OUT_4185_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4185_BOUND_INTERFACE_MATRIX.csv"
OUT_4206_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4206_STATUS.csv"
OUT_4207_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4207_STATUS.csv"
OUT_4279_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4279_STATUS.csv"
OUT_4448_SURV = SOURCE_DIR / "P8_Y5_R2FR_4448_SURVIVOR_MAP_OUTPUT.csv"
OUT_4449_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4449_STATUS.csv"


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
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def source_specs() -> List[Dict[str, object]]:
    return [
        {"source_id": "SRC4450_00_next4449", "path": NEXT_4449, "needle": "4450-Y5-R2FR-extra-invariant-residual-coefficient-map-to-PPN-R10-clocks-or-parent-scale-law.md", "role": "4449 selected the residual coefficient ledger."},
        {"source_id": "SRC4450_01_formal465", "path": FORMAL_465, "needle": "does not select the Einstein-Cartan/Palatini normal form", "role": "A_MF adoption still leaves coefficients open."},
        {"source_id": "SRC4450_02_formal200", "path": FORMAL_200, "needle": "Everything excluded becomes an explicit residual coefficient", "role": "conditional Palatini selector under A_MF."},
        {"source_id": "SRC4450_03_4184_ledger", "path": OUT_4184_LEDGER, "needle": "RB4184_0_cT", "role": "original residual coefficient ledger."},
        {"source_id": "SRC4450_04_4185_map", "path": OUT_4185_MAP, "needle": "RC4185_0_cD", "role": "coefficient-to-arena map."},
        {"source_id": "SRC4450_05_4185_bound", "path": OUT_4185_BOUND, "needle": "BI4185_0_PPN", "role": "bound interface scaffolds."},
        {"source_id": "SRC4450_06_formal201", "path": FORMAL_201, "needle": "The residuals are now explicit", "role": "formal residual coefficient map."},
        {"source_id": "SRC4450_07_formal202", "path": FORMAL_202, "needle": "=> c_D = 0.", "role": "same-coframe private zero for c_D."},
        {"source_id": "SRC4450_08_formal222", "path": FORMAL_222, "needle": "MTS does not need to numerically predict G_N", "role": "calibrated Newton coupling caveat."},
        {"source_id": "SRC4450_09_formal223", "path": FORMAL_223, "needle": "Poynting vector is real physical flow", "role": "Poynting once-only Hilbert owner."},
        {"source_id": "SRC4450_10_formal295", "path": FORMAL_295, "needle": "c_T_spin", "role": "survivor bound pack after private routing."},
        {"source_id": "SRC4450_11_4279_status", "path": OUT_4279_STATUS, "needle": "c_Gamma plus c_R2/Lambda/spin-torsion finite rows remain", "role": "reduced residual finite survivor set."},
        {"source_id": "SRC4450_12_4448_survivor", "path": OUT_4448_SURV, "needle": "SURV4448_2_nonEH_R11_vector", "role": "nonEH/R11 empirical fallback row."},
        {"source_id": "SRC4450_13_4449_status", "path": OUT_4449_STATUS, "needle": "IR selector assumptions and residual coefficient/scale/bound ledger", "role": "current post-A_MF status."},
        {"source_id": "SRC4450_14_4206_status", "path": OUT_4206_STATUS, "needle": "NUMERIC_G_NOT_PREDICTED", "role": "structural Newton coupling status."},
        {"source_id": "SRC4450_15_4207_status", "path": OUT_4207_STATUS, "needle": "Poynting is legitimate energy flow", "role": "EM/Poynting status."},
        {"source_id": "SRC4450_16_gate", "path": GATE_PATH, "needle": "def evaluate_coefficient_row", "role": "4450 residual status gate."},
        {"source_id": "SRC4450_17_generator", "path": GENERATOR_PATH, "needle": 'CHECKPOINT = "4450"', "role": "4450 generator script."},
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


def coefficient_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "coefficient_id": "C4450_0_cD",
            "coefficient": "c_D",
            "family": "second metric / disformal same-coframe leak",
            "local_gr_role": "would break WEP, clock, EM/Hodge and Poynting ownership if finite",
            "observable_arenas": "WEP;clocks;EM propagation;Poynting/Hilbert stress",
            "source_paths": f"{FORMAL_202};{OUT_4185_MAP}",
            "parent_route": "single observed coframe plus Hilbert matter/EM descent gives c_D=0 inside private selector",
            "parent_route_status": "PRIVATE_ZERO_ROUTED",
            "scale_status": "NOT_REQUIRED_IF_PRIVATE_ZERO",
            "bound_status": "SOURCE_BOUND_NUMERIC_NOT_REQUIRED_UNLESS_REOPENED",
            "current_class": "private_routed_subset",
            "selected_next": False,
            "public_claim_false": True,
        },
        {
            "coefficient_id": "C4450_1_deltaKappa",
            "coefficient": "delta_kappa",
            "family": "source-coupling drift",
            "local_gr_role": "would make Newton coupling species/time/frame dependent",
            "observable_arenas": "Newton coefficient;orbital GM;Gdot/G;clock/local G",
            "source_paths": f"{FORMAL_222};{OUT_4206_STATUS};{OUT_4185_MAP}",
            "parent_route": "universal calibrated G_N plus source-blind kappa/Hilbert charge lock; numeric G is not predicted",
            "parent_route_status": "PRIVATE_STRUCTURAL_COUPLING",
            "scale_status": "CALIBRATED_UNIVERSAL_G_ONLY",
            "bound_status": "MEASURED_G_ENVELOPE_NOT_NUMERIC_PARENT_PREDICTION",
            "current_class": "private_routed_subset",
            "selected_next": False,
            "public_claim_false": True,
        },
        {
            "coefficient_id": "C4450_2_cBdy",
            "coefficient": "c_bdy",
            "family": "unrouted boundary or edge charge",
            "local_gr_role": "would leak Hamiltonian/radiative boundary charge into bulk local equations",
            "observable_arenas": "orbital mass leakage;radiation reaction;clock/source drift",
            "source_paths": f"{FORMAL_295};{OUT_4185_MAP}",
            "parent_route": "fixed/exact/Hamiltonian-routed boundary; compact no-flux private guard",
            "parent_route_status": "PRIVATE_ZERO_ROUTED",
            "scale_status": "NOT_REQUIRED_IF_BOUNDARY_ROUTED",
            "bound_status": "FLUX_BOUND_ONLY_IF_REOPENED",
            "current_class": "private_routed_subset",
            "selected_next": False,
            "public_claim_false": True,
        },
        {
            "coefficient_id": "C4450_3_cPoynt_extra",
            "coefficient": "c_Poynt_extra",
            "family": "double-counted EM/Poynting source",
            "local_gr_role": "would add a second background force instead of Hilbert stress flow",
            "observable_arenas": "EM stress;preferred frame;WEP;clock;R10 EM background",
            "source_paths": f"{FORMAL_223};{OUT_4207_STATUS}",
            "parent_route": "Poynting is Maxwell-Hodge Hilbert stress flux, not an extra source term",
            "parent_route_status": "PRIVATE_ZERO_ROUTED",
            "scale_status": "NOT_REQUIRED_IF_HODGE_OWNER_LOCK_HOLDS",
            "bound_status": "DELTA_HODGE_OR_RADIATIVE_FLUX_BOUND_IF_REOPENED",
            "current_class": "private_routed_subset",
            "selected_next": False,
            "public_claim_false": True,
        },
        {
            "coefficient_id": "C4450_4_cGamma",
            "coefficient": "c_Gamma",
            "family": "local memory coupling",
            "local_gr_role": "MTS-specific local hair; can reopen PPN, clocks, R10 and local-G variation",
            "observable_arenas": "PPN;clocks;R10;Gdot/G;orbital",
            "source_paths": f"{FORMAL_295};{OUT_4279_STATUS};{OUT_4185_MAP}",
            "parent_route": "local memory support/projector silence or finite profile product bounds",
            "parent_route_status": "FINITE_SURVIVOR_OPEN",
            "scale_status": "PARENT_SCREENING_SCALE_NOT_NUMERIC",
            "bound_status": "PRODUCT_BOUNDS_SYMBOLIC_READY_SOURCE_VALUES_MISSING",
            "current_class": "finite_survivor",
            "selected_next": False,
            "public_claim_false": True,
        },
        {
            "coefficient_id": "C4450_5_cR2_MR",
            "coefficient": "c_R2/M_R",
            "family": "curvature-square / higher-derivative finite-range tail",
            "local_gr_role": "would introduce Yukawa/short-range or higher-derivative orbital correction",
            "observable_arenas": "R10 alpha(lambda);orbital precession;cosmology consistency",
            "source_paths": f"{FORMAL_200};{OUT_4185_BOUND};{FORMAL_295}",
            "parent_route": "derive high parent mass scale M_R or exact low-energy absence",
            "parent_route_status": "FINITE_SURVIVOR_OPEN",
            "scale_status": "PARENT_SCALE_MR_MISSING",
            "bound_status": "R10_OR_ORBITAL_BOUND_INTERFACE_READY_VALUES_MISSING",
            "current_class": "finite_survivor",
            "selected_next": False,
            "public_claim_false": True,
        },
        {
            "coefficient_id": "C4450_6_cT_spin",
            "coefficient": "c_T_spin",
            "family": "spin/torsion contact channel",
            "local_gr_role": "last torsion residual after static Kperp routing; local GR needs torsion algebraic zero/heavy/contact-bound",
            "observable_arenas": "PPN preferred frame;spin/torsion clocks;R10/contact force",
            "source_paths": f"{FORMAL_200};{FORMAL_295};{OUT_4184_LEDGER};{OUT_4185_MAP}",
            "parent_route": "prove torsion is algebraic and proportional only to microscopic spin current, zero in spinless macroscopic local branch, or derive heavy/contact bound",
            "parent_route_status": "FINITE_SURVIVOR_OPEN",
            "scale_status": "TORSION_MASS_OR_CONTACT_SCALE_MISSING",
            "bound_status": "SPIN_TORSION_OR_CONTACT_BOUND_MISSING",
            "current_class": "finite_survivor",
            "selected_next": True,
            "public_claim_false": True,
        },
        {
            "coefficient_id": "C4450_7_nonEH_R11",
            "coefficient": "nonEH_R11_vector",
            "family": "non-EH domain/readout coefficient vector",
            "local_gr_role": "public scoring fallback if parent selector stalls",
            "observable_arenas": "alpha_i;xi;R11;source normalization;material Req",
            "source_paths": f"{OUT_4448_SURV};{FORMAL_201}",
            "parent_route": "do after torsion/finite survivor route or as empirical fallback",
            "parent_route_status": "EMPIRICAL_FALLBACK_OPEN",
            "scale_status": "NOT_A_PARENT_SCALE_LAW",
            "bound_status": "MATERIAL_AND_R10_ROWS_MISSING",
            "current_class": "empirical_fallback",
            "selected_next": False,
            "public_claim_false": True,
        },
    ]


def target_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "target_id": "T4450_0_cT_spin",
            "target": "torsion-spin residual c_T_spin zero/heavy/contact-bound",
            "why": "direct GR-reduction hinge after A_MF: EH/Palatini only reduces cleanly when torsion is algebraic, spin-supported, zero in spinless local matter, heavy, or bounded",
            "derivation_leverage": 5,
            "clean_theorem_route": 3,
            "already_chased_penalty": 0,
            "dependency_penalty": 2,
            "empirical_fallback_penalty": 0,
            "next_artifact": NEXT_TARGET,
        },
        {
            "target_id": "T4450_1_cR2_MR",
            "target": "curvature-square parent scale M_R or R10/orbital bound",
            "why": "important finite-range tail, but needs parent scale or reviewed R10/orbital projection before it becomes clean",
            "derivation_leverage": 4,
            "clean_theorem_route": 1,
            "already_chased_penalty": 0,
            "dependency_penalty": 4,
            "empirical_fallback_penalty": 0,
            "next_artifact": "later-cR2-MR-parent-scale-or-R10-bound.md",
        },
        {
            "target_id": "T4450_2_cGamma",
            "target": "local memory c_Gamma profile/source coefficient fill",
            "why": "still crucial, but the existing chain already chased it through support/projector/profile/AJ routes and left source coefficients open",
            "derivation_leverage": 5,
            "clean_theorem_route": 1,
            "already_chased_penalty": 2,
            "dependency_penalty": 5,
            "empirical_fallback_penalty": 0,
            "next_artifact": "later-cGamma-source-coefficients-or-profile-bound.md",
        },
        {
            "target_id": "T4450_3_nonEH_R11",
            "target": "nonEH/R11 vector or material values",
            "why": "useful empirical fallback, but less derivational than killing the remaining torsion channel",
            "derivation_leverage": 3,
            "clean_theorem_route": 0,
            "already_chased_penalty": 0,
            "dependency_penalty": 4,
            "empirical_fallback_penalty": 2,
            "next_artifact": "later-nonEH-R11-or-material-bound-runner.md",
        },
    ]


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "D4450_0_A_MF_not_enough",
            "claim": "A_MF owns the Cartan variables privately but does not by itself select local GR.",
            "derivation": "4449 signs A_MF only as a private parent-branch axiom candidate. 4184/200 says the Palatini/EH principal block follows only after locality, IR order, no-extra-light-mode, same-coframe, boundary and parity selector clauses. Therefore every excluded invariant must be carried as an explicit coefficient rather than silently dropped.",
            "consequence": "The next work is coefficient routing/zero/scale/bound, not another A_MF loop.",
            "status": "AMF_INTEGRATED_COEFFICIENT_LEDGER_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4450_1_private_routed_subset",
            "claim": "Some previously scary rows are not the next derivation target.",
            "derivation": "Inside the private selector, same coframe routes c_D, universal calibrated source coupling routes delta_kappa without predicting numeric G, boundary/Hamiltonian routing handles c_bdy, and Maxwell-Hodge ownership prevents a separate Poynting force. These remain non-public because parent adoption is open, but they should not be re-attacked unless their reactivation guards fail.",
            "consequence": "Do not waste the next pass circling Poynting, calibrated G, or c_D unless a guard reopens.",
            "status": "PRIVATE_ROUTED_SUBSET_RECOVERED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4450_2_finite_survivor_subset",
            "claim": "The surviving coefficient problem is now smaller.",
            "derivation": "After private routing, the hard finite rows are c_Gamma, c_R2/M_R, local Lambda/nonEH tails and c_T_spin. c_Gamma has already been pursued through profile/source coefficient gates; c_R2 needs a parent scale or reviewed short-range/orbital curve; c_T_spin is the cleanest remaining local-GR theorem target.",
            "consequence": "The best next leap is the torsion-spin residual zero/heavy/contact-bound branch.",
            "status": "FINITE_SURVIVORS_REDUCED_cT_SPIN_SELECTED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4450_3_next_theorem_shape",
            "claim": "The next theorem should try to prove a torsion-spin local branch law.",
            "derivation": "Under A_MF/Cartan variables, show torsion is auxiliary/algebraic and sourced only by microscopic spin current; for spinless macroscopic local test bodies T^A vanishes or is contact-suppressed. If that cannot be proved, build the PPN/spin-clock/R10 contact bound row explicitly.",
            "consequence": NEXT_TARGET,
            "status": "NEXT_TARGET_WRITTEN",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [{
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "claim_id": CLAIM_ID,
        "decision": DECISION,
        "private_routed_subset": "c_D;delta_kappa;c_bdy;c_Poynt_extra",
        "finite_survivor_subset": "c_Gamma;c_R2/M_R;c_T_spin;nonEH_R11/material_fallback",
        "selected_next": NEXT_TARGET,
        "public_claim": False,
        "valid_for_claim": False,
        "generated_utc": STAMP,
    }]


def status_rows() -> List[Dict[str, object]]:
    return [{
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "claim_id": CLAIM_ID,
        "decision": DECISION,
        "A_MF_private_adopted": True,
        "residual_coefficients_mapped": True,
        "private_routed_rows_recovered": True,
        "finite_survivors_remaining": True,
        "selected_next_derivation": "c_T_spin",
        "numeric_G_predicted": False,
        "local_GR_public_claim": False,
        "next_target": NEXT_TARGET,
        "valid_for_claim": False,
        "generated_utc": STAMP,
    }]


def next_rows() -> List[Dict[str, object]]:
    return [{
        "next_id": "NT4450_0",
        "target": NEXT_TARGET,
        "objective": "Try to prove or bound the remaining spin/torsion contact coefficient after A_MF and private routing.",
        "derive_first": "derive auxiliary/algebraic torsion sourced only by microscopic spin current, zero in spinless macroscopic local branch, or parent heavy scale",
        "fallback": "build PPN preferred-frame, spin-clock, and R10/contact bound rows for finite c_T_spin",
        "risk": "pretending torsion is absent because GR is torsionless rather than deriving or bounding its MTS residual coefficient",
        "valid_for_claim": False,
    }]


def claim_gate_rows() -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    coeffs = rows_from(COEFF_OUTPUT)
    targets = rows_from(TARGET_OUTPUT)
    status = rows_from(STATUS_CSV)[0]
    selected = [row for row in targets if row.get("selected") == "True"]
    return [
        {"gate_id": "CG4450_0_sources_exist", "claim": "all cited source paths exist", "passed": all(row["path_exists"] == "True" for row in sources), "valid_for_claim": False, "detail": "Source register path-backed."},
        {"gate_id": "CG4450_1_needles_found", "claim": "all cited source needles found", "passed": all(row["needle_found"] == "True" for row in sources), "valid_for_claim": False, "detail": "Residual coefficient map is sourced."},
        {"gate_id": "CG4450_2_all_coeff_rows_sourced", "claim": "all coefficient rows have existing sources", "passed": all(row["source_paths_exist"] == "True" for row in coeffs), "valid_for_claim": False, "detail": "No vibe-only coefficient row."},
        {"gate_id": "CG4450_3_private_routed_recovered", "claim": "private-routed subset identified", "passed": all(row["current_status"] in {"PRIVATE_ZERO_ROUTED_PARENT_ADOPTION_OPEN", "PRIVATE_STRUCTURAL_COUPLING_CALIBRATED_G_NOT_PREDICTED"} for row in coeffs if row["coefficient_id"] in {"C4450_0_cD", "C4450_1_deltaKappa", "C4450_2_cBdy", "C4450_3_cPoynt_extra"}), "valid_for_claim": False, "detail": "Closed-private rows are not selected again."},
        {"gate_id": "CG4450_4_finite_survivors_not_claimed", "claim": "finite survivors remain nonclaim", "passed": all(row["valid_for_claim"] == "False" for row in coeffs if row["current_class"] == "finite_survivor"), "valid_for_claim": False, "detail": "cGamma/cR2/cT_spin need parent scale/zero/bound."},
        {"gate_id": "CG4450_5_cT_selected", "claim": "c_T_spin selected as next target", "passed": len(selected) == 1 and selected[0]["target_id"] == "T4450_0_cT_spin" and any(row["coefficient_id"] == "C4450_6_cT_spin" and row["selected_next"] == "True" for row in coeffs), "valid_for_claim": False, "detail": NEXT_TARGET},
        {"gate_id": "CG4450_6_no_numeric_G_prediction", "claim": "numeric G is not claimed", "passed": status.get("numeric_G_predicted") == "False", "valid_for_claim": False, "detail": "GR-like calibrated universal G only."},
        {"gate_id": "CG4450_7_no_public_local_GR_claim", "claim": "no public local-GR claim emitted", "passed": all(row["claim_allowed"] == "False" for row in coeffs), "valid_for_claim": False, "detail": "Every coefficient row remains nonclaim."},
        {"gate_id": "CG4450_8_next_target_written", "claim": "next target selected", "passed": NEXT_CSV.exists() and NEXT_TARGET in text(NEXT_CSV), "valid_for_claim": False, "detail": NEXT_TARGET},
    ]


def build_doc() -> str:
    return f"""# 466 PPC4161 extra invariant residual coefficient map to PPN R10 clocks or parent scale law

Marker: `{MARKER}`

Decision: `{DECISION}`

Claim register: `{CLAIM_ID}`

## Result

4450 does the post-`A_MF` cleanup rather than looping the same missing-item list.

```text
A_MF gives the private Cartan branch variables.
It does not by itself erase every extra invariant.
The coefficient problem is now split into:
1. private-routed rows that should not be re-attacked unless a guard fails;
2. finite survivor rows that need a parent zero, parent scale, screening law, or source-backed bound.
```

The next derivation target is `c_T_spin`: prove the torsion-spin residual is auxiliary/zero/heavy/contact-bounded, or keep local-GR reduction explicitly blocked.

## Source Register

{table(rows_from(SOURCE_REGISTER))}

## Coefficient Status

{table(rows_from(COEFF_OUTPUT))}

## Target Score

{table(rows_from(TARGET_OUTPUT))}

## Derivation Rows

{table(rows_from(DERIVATION_ROWS))}

## Claim Gates

{table(rows_from(CLAIM_GATES))}

## Decision

{table(rows_from(DECISION_CSV))}

## Status

{table(rows_from(STATUS_CSV))}

## Next Target

{table(rows_from(NEXT_CSV))}
"""


def post_doc() -> str:
    return f"""# 4450 Y5 R2FR extra invariant residual coefficient map to PPN R10 clocks or parent scale law

Private checkpoint generated at `{STAMP}`.

Summary:
- `A_MF` is integrated into the residual coefficient ledger.
- `c_D`, `delta_kappa`, `c_bdy`, and `c_Poynt_extra` are recovered as private-routed rows, not public claims.
- `c_Gamma`, `c_R2/M_R`, and `c_T_spin` remain finite survivor rows.
- The next best derivation target is `c_T_spin`, because torsion is the cleanest remaining local-GR reduction hinge after the motion-frame branch.

Next target: `{NEXT_TARGET}`
"""


def update_claims_register() -> None:
    rows = rows_from(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = list(rows[0].keys()) if rows else ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk", "sector", "evidence", "next_action", "risk"]
    row = {field: "" for field in fieldnames}
    payload = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_derivation",
        "claim": "4450 integrates A_MF adoption with the residual invariant coefficient ledger: private-routed rows are recovered, finite survivors remain nonclaim, and c_T_spin is selected as the next derivation/bound target.",
        "current_evidence": "4450 source register, coefficient status gate, target score, derivation rows, claim gates, decision, status, next target and validation CSV.",
        "status": "residual_coefficients_split_private_routed_vs_finite_survivor_cT_spin_next_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating private-routed rows or finite survivor rows as public local-GR proof.",
        "sector": "local_gr_parent_derivation",
        "evidence": "4450 source register, coefficient status gate, target score, derivation rows, claim gates, decision, status, next target and validation CSV.",
        "next_action": NEXT_TARGET,
        "risk": "Treating private-routed rows or finite survivor rows as public local-GR proof.",
    }
    for key, value in payload.items():
        if key in row:
            row[key] = value
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writerow(row)


def append_marker_section(path: Path, marker: str, section: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    write_text(path, existing.rstrip() + "\n\n" + section.strip() + "\n")


def write_spine_and_packet() -> None:
    spine_section = f"""## Local GR Parent-Derivation Update - Residual Coefficient Status After A_MF

Marker: `{MARKER}`  
Source checkpoint: `4450-Y5-R2FR-extra-invariant-residual-coefficient-map-to-PPN-R10-clocks-or-parent-scale-law.md`  
Claim register row: `{CLAIM_ID}`

After private `A_MF` adoption, the residual invariant ledger is split into private-routed rows and finite survivor rows. `c_D`, `delta_kappa`, `c_bdy`, and `c_Poynt_extra` are not the next derivation target unless their guards fail. The remaining local-GR reduction hinge selected here is `c_T_spin`: prove torsion is algebraic/zero/heavy/contact-bounded, or keep the branch explicitly blocked.
"""
    packet_section = f"""## PPC4161 Packet Addendum - Residual Coefficient Status After A_MF

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4450-Y5-R2FR-extra-invariant-residual-coefficient-map-to-PPN-R10-clocks-or-parent-scale-law.md`

Inside the private packet, `A_MF` no longer sends the work back to Poynting, calibrated `G`, or same-coframe `c_D` unless their guards fail. The next packet theorem target is `c_T_spin`: torsion-spin residual zero/heavy/contact-bound.
"""
    append_marker_section(SPINE_PATH, MARKER, spine_section)
    append_marker_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows() -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    coeffs = rows_from(COEFF_OUTPUT)
    targets = rows_from(TARGET_OUTPUT)
    gates = rows_from(CLAIM_GATES)
    selected = [row for row in targets if row.get("selected") == "True"]
    checks = [
        ("VAL4450_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4450_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4450_2_coeff_sources_exist", all(row["source_paths_exist"] == "True" for row in coeffs), "every coefficient row is source-backed"),
        ("VAL4450_3_private_routed_subset", all(row["current_status"] in {"PRIVATE_ZERO_ROUTED_PARENT_ADOPTION_OPEN", "PRIVATE_STRUCTURAL_COUPLING_CALIBRATED_G_NOT_PREDICTED"} for row in coeffs if row["current_class"] == "private_routed_subset"), "private-routed subset recovered"),
        ("VAL4450_4_finite_survivors_nonclaim", all(row["valid_for_claim"] == "False" for row in coeffs if row["current_class"] == "finite_survivor"), "finite survivor rows remain nonclaim"),
        ("VAL4450_5_cT_selected", len(selected) == 1 and selected[0]["target_id"] == "T4450_0_cT_spin", "c_T_spin target selected by score"),
        ("VAL4450_6_all_claim_gates", all(row["passed"] == "True" for row in gates), "all claim gates pass"),
        ("VAL4450_7_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-292"),
        ("VAL4450_8_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4450_9_post_doc", DOC_PATH.exists() and "Private checkpoint" in text(DOC_PATH), "post checkpoint doc exists"),
        ("VAL4450_10_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4450_11_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4450_12_next_target", NEXT_CSV.exists() and NEXT_TARGET in text(NEXT_CSV), "next target written"),
        ("VAL4450_13_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(COEFF_INPUT, coefficient_input_rows())
    write_csv(COEFF_OUTPUT, [evaluate_coefficient_row(row) for row in rows_from(COEFF_INPUT)])
    write_csv(TARGET_INPUT, target_input_rows())
    write_csv(TARGET_OUTPUT, evaluate_targets(TARGET_INPUT))
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_csv(CLAIM_GATES, claim_gate_rows())
    write_text(FORMAL_PATH, build_doc())
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows())


if __name__ == "__main__":
    main()
