from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4526"
CLAIM_ID = "L-368"
MARKER = "PPC4161_VERTICAL_INVOLUTION_SOURCE_HUNT_OR_FIRST_SOURCE_NORMALIZED_COEFFICIENT_FILL_4526"
PACKET_MARKER = "PPC4161_PACKET_VERTICAL_INVOLUTION_SOURCE_HUNT_OR_FIRST_SOURCE_NORMALIZED_COEFFICIENT_FILL_4526"
DECISION = "LEAKAGE_PARITY_BRIDGES_TO_PARENT_Z_ONLY_CONDITIONALLY_GR_PARITY_SOURCE_SUBPIECES_ZERO_SCALAR_ACTION_COEFFICIENTS_LIVE"
NEXT_TARGET = "4527-Y5-R2FR-scalar-action-asymmetry-coefficient-or-auxiliary-Z-principal-symbol-hunt.md"

FORMAL_PATH = FORMAL / "542-PPC4161-vertical-involution-source-hunt-or-first-source-normalized-coefficient-fill.md"
DOC_PATH = POST / "4526-Y5-R2FR-vertical-involution-source-hunt-or-first-source-normalized-coefficient-fill.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4526_SOURCE_REGISTER.csv"
HUNT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4526_VERTICAL_INVOLUTION_SOURCE_HUNT.csv"
BRIDGE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4526_ZL_TO_Z_PARENT_BRIDGE_THEOREM.csv"
COEFFICIENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4526_FIRST_SOURCE_NORMALIZED_COEFFICIENT_ROWS.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4526_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4526_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4526_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4526_NEXT_TARGET.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4526_VALIDATION.csv"

DOC_4525 = POST / "4525-Y5-R2FR-parent-Z-algebraic-action-derivation-or-source-normalized-first-coefficient-fill.md"
FORMAL_4525 = FORMAL / "541-PPC4161-parent-Z-algebraic-action-derivation-or-source-normalized-first-coefficient-fill.md"
VALIDATION_4525 = SOURCE_DIR / "P8_Y5_BRR545_4525_VALIDATION.csv"
THEOREM_4525 = SOURCE_DIR / "P8_Y5_R2FR_4525_QUOTIENT_EVEN_MORSE_BOTT_Z_THEOREM.csv"
SIGNATURE_4525 = SOURCE_DIR / "P8_Y5_R2FR_4525_PARENT_SIGNATURE_REQUIREMENTS.csv"
COEFFICIENT_4525 = SOURCE_DIR / "P8_Y5_R2FR_4525_SOURCE_NORMALIZED_COEFFICIENT_FILL_ROWS.csv"

FORMAL_126 = FORMAL / "126-scalar-evenness-origin.md"
FORMAL_127 = FORMAL / "127-signed-leakage-coordinate-map.md"
FORMAL_128 = FORMAL / "128-leakage-frame-symmetry.md"
DOC_4195 = POST / "4195-Y5-R2FR-parent-ZL-parity-signature-or-Jres-numeric-profile-smoke.md"
PARITY_4195 = SOURCE_DIR / "P8_Y5_R2FR_4195_PARITY_LEMMA.csv"
SIGNATURE_4195 = SOURCE_DIR / "P8_Y5_R2FR_4195_PARENT_SIGNATURE_AUDIT.csv"
JRES_4195 = SOURCE_DIR / "P8_Y5_R2FR_4195_JRES_CONSEQUENCE.csv"
VALIDATION_4195 = SOURCE_DIR / "P8_Y5_BRR545_4195_VALIDATION.csv"

DOC_4446 = POST / "4446-Y5-R2FR-adopt-GR-parity-SM-import-or-source-backed-material-Req-value.md"
DOC_4447 = POST / "4447-Y5-R2FR-GR-parity-source-universality-to-local-PPN-residual-vector-or-material-values.md"
VALIDATION_4446 = SOURCE_DIR / "P8_Y5_BRR545_4446_VALIDATION.csv"
VALIDATION_4447 = SOURCE_DIR / "P8_Y5_BRR545_4447_VALIDATION.csv"
REDUCTION_4446 = SOURCE_DIR / "P8_Y5_R2FR_4446_REDUCTION_ROWS.csv"
ROLLUP_4447 = SOURCE_DIR / "P8_Y5_R2FR_4447_RESIDUAL_ROLLUP.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def line_of(path: Path, needle: str) -> int:
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def snippet(path: Path, needle: str) -> str:
    for line in text(path).splitlines():
        if needle in line:
            return line.strip()
    return ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(out)


def append_once(path: Path, marker: str, body: str) -> None:
    current = text(path)
    if marker in current:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="") as handle:
        if current and not current.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + body.strip() + "\n")


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4526_00_formal4525", "4525 formal handoff", FORMAL_4525, "PPC4161_PARENT_Z_ALGEBRAIC_ACTION_DERIVATION_OR_SOURCE_NORMALIZED_FIRST_COEFFICIENT_FILL_4525", "parent Z mechanism"),
        ("SRC4526_01_post4525", "4525 post handoff", DOC_4525, "4526-Y5-R2FR-vertical-involution-source-hunt-or-first-source-normalized-coefficient-fill.md", "declared 4526 target"),
        ("SRC4526_02_val4525", "4525 validation", VALIDATION_4525, "VAL4525_OVERALL", "previous validation pass"),
        ("SRC4526_03_theorem4525", "4525 quotient-even theorem", THEOREM_4525, "QEZ4525_1_even_involution", "general parent Z action mechanism"),
        ("SRC4526_04_signature4525", "4525 signature requirements", SIGNATURE_4525, "SIG4525_0_vertical_involution", "needed parent involution"),
        ("SRC4526_05_coeff4525", "4525 coefficient rows", COEFFICIENT_4525, "COF4525_0_epsilon_odd", "first coefficient route"),
        ("SRC4526_06_even126", "126 scalar evenness", FORMAL_126, "scalar_evenness_origin_parity_candidate_not_parent_derived", "parity theorem-shaped but unsigned"),
        ("SRC4526_07_signed127", "127 signed leakage coordinates", FORMAL_127, "parity_symmetry_parent_derived = false", "signed stage built, symmetry unsigned"),
        ("SRC4526_08_sym128", "128 leakage-frame symmetry", FORMAL_128, "scalar_linear_terms_removed = false", "scalar channels survive ordinary frame symmetry"),
        ("SRC4526_09_doc4195", "4195 parent ZL parity", DOC_4195, "ZL_PARITY_EVENNESS_LEMMA_PROVED_UNDER_LEAKAGE_INVOLUTION_PARENT_OWNERSHIP_OPEN_JRES_POWER_REMAINS_CONDITIONAL", "conditional leakage involution lemma"),
        ("SRC4526_10_lemma4195", "4195 parity lemma", PARITY_4195, "LEM4195_1_leakage_involution", "R_L leakage involution condition"),
        ("SRC4526_11_sig4195", "4195 parent signature audit", SIGNATURE_4195, "SIG4195_0_parent_action", "parent action invariance missing"),
        ("SRC4526_12_jres4195", "4195 residual consequence", JRES_4195, "CONS4195_2_bulk_Jres", "Jres power consequence"),
        ("SRC4526_13_val4195", "4195 validation", VALIDATION_4195, "VAL4195_4_parent_rows_unsigned", "parent rows unsigned"),
        ("SRC4526_14_doc4446", "4446 GR-parity SM import", DOC_4446, "Adopted the GR-parity standard-matter import/no-source-prefactor invariant", "private source material zero subbranch"),
        ("SRC4526_15_doc4447", "4447 source-universality residual", DOC_4447, "Source pieces of WEP, PPN, `Gdot/G`, clock and orbital rows are zero", "private source residual zero propagation"),
        ("SRC4526_16_val4446", "4446 validation", VALIDATION_4446, "VAL4446_9_residual_vector", "4446 validation"),
        ("SRC4526_17_val4447", "4447 validation", VALIDATION_4447, "VAL4447_9_residual_rollup", "4447 validation"),
        ("SRC4526_18_red4446", "4446 reduction rows", REDUCTION_4446, "RED4446", "private source reduction rows"),
        ("SRC4526_19_roll4447", "4447 residual rollup", ROLLUP_4447, "RU4447_0_source_weight_subvector", "source residual rollup"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, role, path, needle, note in specs:
        body = text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in body,
                "line": line_of(path, needle),
                "evidence_snippet": snippet(path, needle),
                "note": note,
                "valid_for_claim": False,
            }
        )
    return rows


def hunt_rows() -> list[dict[str, Any]]:
    return [
        {
            "hunt_id": "HUNT4526_0_scalar_evenness_origin",
            "candidate_source": str(FORMAL_126),
            "line": line_of(FORMAL_126, "scalar_evenness_origin_parity_candidate_not_parent_derived"),
            "evidence": "Scalar evenness has a parity/isotropy theorem form, but parent derivation is explicitly false.",
            "maps_to_4525_signature": "SIG4525_0_vertical_involution",
            "status": "THEOREM_SHAPED_NOT_PARENT_SIGNED",
            "effect": "usable as a sublemma, not as local-GR closure",
            "valid_for_claim": False,
        },
        {
            "hunt_id": "HUNT4526_1_signed_leakage_stage",
            "candidate_source": str(FORMAL_127),
            "line": line_of(FORMAL_127, "parity_symmetry_parent_derived = false"),
            "evidence": "Signed leakage coordinates exist as candidates, so parity has coordinates to act on.",
            "maps_to_4525_signature": "QEZ4525_0_field_space_split",
            "status": "CANDIDATE_SUBBUNDLE_COORDINATES",
            "effect": "supports a leakage subbundle bridge from z_L to z, but not full ker(Dpi)",
            "valid_for_claim": False,
        },
        {
            "hunt_id": "HUNT4526_2_frame_symmetry_limit",
            "candidate_source": str(FORMAL_128),
            "line": line_of(FORMAL_128, "scalar_linear_terms_removed = false"),
            "evidence": "Leakage-frame rotations/reflections kill vector/tensor linears only; true scalar channels can still enter linearly.",
            "maps_to_4525_signature": "SIG4525_3_source_evenness",
            "status": "PARTIAL_REJECTION_FOR_SCALAR_CHANNELS",
            "effect": "forces scalar coefficients a_theta, a_dotB and a_Lcg into fallback rows unless stronger parent extremum exists",
            "valid_for_claim": False,
        },
        {
            "hunt_id": "HUNT4526_3_leakage_involution_lemma",
            "candidate_source": str(DOC_4195),
            "line": line_of(DOC_4195, "ZL_PARITY_EVENNESS_LEMMA_PROVED_UNDER_LEAKAGE_INVOLUTION_PARENT_OWNERSHIP_OPEN_JRES_POWER_REMAINS_CONDITIONAL"),
            "evidence": "A leakage involution lemma is already proved under parent ownership.",
            "maps_to_4525_signature": "SIG4525_0_vertical_involution",
            "status": "EXACT_CONDITIONAL_SUBLEMMA",
            "effect": "bridges 4525 to existing work if R_L extends to the full parent vertical kernel",
            "valid_for_claim": False,
        },
        {
            "hunt_id": "HUNT4526_4_parent_action_invariance",
            "candidate_source": str(SIGNATURE_4195),
            "line": line_of(SIGNATURE_4195, "SIG4195_0_parent_action"),
            "evidence": "4195 audit marks S_parent[Phi]=S_parent[R_L Phi] as missing.",
            "maps_to_4525_signature": "SIG4525_0_vertical_involution",
            "status": "NOT_FOUND",
            "effect": "epsilon_I/action-asymmetry row remains live",
            "valid_for_claim": False,
        },
        {
            "hunt_id": "HUNT4526_5_private_GR_parity_source_piece",
            "candidate_source": str(DOC_4446),
            "line": line_of(DOC_4446, "Adopted the GR-parity standard-matter import/no-source-prefactor invariant"),
            "evidence": "Inside the private PPC4161 branch, GR-parity standard-matter import/no-source-prefactor is adopted.",
            "maps_to_4525_signature": "SIG4525_3_source_evenness",
            "status": "PRIVATE_BRANCH_SOURCE_SUBPIECE_ZERO",
            "effect": "source-weight/material-reentry coefficients can be zero inside this private branch, but not public claim-grade",
            "valid_for_claim": False,
        },
        {
            "hunt_id": "HUNT4526_6_source_residual_rollup",
            "candidate_source": str(DOC_4447),
            "line": line_of(DOC_4447, "Source pieces of WEP, PPN, `Gdot/G`, clock and orbital rows are zero"),
            "evidence": "Source pieces of WEP/PPN/Gdot/clocks/orbits are zero inside private branch.",
            "maps_to_4525_signature": "SIG4525_3_source_evenness",
            "status": "PRIVATE_SOURCE_RESIDUAL_ZERO_SUBSECTOR",
            "effect": "narrows source-current fallback to non-source survivors plus scalar/action symmetry breaking",
            "valid_for_claim": False,
        },
    ]


def bridge_rows() -> list[dict[str, Any]]:
    return [
        {
            "bridge_id": "BRG4526_0_embedding",
            "statement": "If the signed leakage coordinates z_L^a of 127 embed into the 4525 vertical collar z^A with z_L=P_L z and the parent quotient satisfies pi(I_q Phi)=pi(Phi), then the 4195 leakage involution R_L is the restriction of the 4525 vertical involution I_q.",
            "formula": "I_q: z=(z_L,z_rest)->(-z_L,I_rest z_rest), pi∘I_q=pi",
            "status": "DERIVED_CONDITIONAL_EMBEDDING",
            "claim_effect": "does not claim; supplies exact bridge condition",
            "valid_for_claim": False,
        },
        {
            "bridge_id": "BRG4526_1_action_evenness",
            "statement": "If S_parent, measure, coframe, connection, projector and boundary class commute with I_q, then the first vertical force in the leakage subbundle vanishes.",
            "formula": "S[I_q Phi]=S[Phi] => P_L delta_z S|_0=0",
            "status": "DERIVED_CONDITIONAL_NOT_SOURCED",
            "claim_effect": "reduces F_1=0 to a concrete action-invariance source hunt",
            "valid_for_claim": False,
        },
        {
            "bridge_id": "BRG4526_2_scalar_channel_obstruction",
            "statement": "Ordinary leakage-frame rotations/reflections do not remove scalar signed channels z_theta, z_dotB and z_Lcg. They need a stronger parent extremum, exclusion rule, or finite coefficient bound.",
            "formula": "f=f0+a_theta z_theta+a_dotB z_dotB+a_Lcg z_Lcg+O(z^2)",
            "status": "OBSTRUCTION_RETAINED",
            "claim_effect": "prevents using 126-128 as full vertical evenness",
            "valid_for_claim": False,
        },
        {
            "bridge_id": "BRG4526_3_private_source_narrowing",
            "statement": "4446/4447 narrow the source sector in the private PPC4161 branch: standard matter source-weight/material-reentry pieces are zero there, so they need not be counted in the first symmetry-breaking coefficient row for that branch.",
            "formula": "epsilon_source_private = epsilon_non_source + epsilon_scalar + epsilon_boundary + epsilon_wave",
            "status": "PRIVATE_BRANCH_NARROWING",
            "claim_effect": "moves one source subpiece from MISSING to private-zero/nonclaim",
            "valid_for_claim": False,
        },
        {
            "bridge_id": "BRG4526_4_full_parent_Z_verdict",
            "statement": "The full 4525 parent-Z mechanism is not yet sourced: action involution, auxiliary principal-zero, Morse-Bott Hessian and scalar-channel stationarity remain open.",
            "formula": "QEZ4525 claim=false until SIG4525_0..3 are parent-signed",
            "status": "NO_LOCAL_GR_CLAIM",
            "claim_effect": "route continues to 4527 coefficient/principal-symbol hunt",
            "valid_for_claim": False,
        },
    ]


def coefficient_rows() -> list[dict[str, Any]]:
    return [
        {
            "coefficient_id": "COF4526_0_epsilon_I",
            "quantity": "epsilon_I",
            "definition": "normalized action-asymmetry defect under the candidate parent involution",
            "formula": "epsilon_I := ||S_parent[Phi]-S_parent[I_q Phi]||/(V_loc E_ref)",
            "source_status": "FORMULA_FILLED_SOURCE_VALUE_MISSING",
            "arena_effect": "if nonzero, feeds retained J_A before alpha/PPN/clock/orbit projection",
            "current_value": "MISSING_NUMERIC_ACTION_DEFECT",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COF4526_1_a_theta",
            "quantity": "a_theta",
            "definition": "linear scalar-channel coefficient for expansion/clock-flow leakage",
            "formula": "a_theta := partial f_local/partial z_theta |_{z=0}",
            "source_status": "FORMULA_FILLED_VALUE_MISSING",
            "arena_effect": "survives 128 unless parent scalar extremum is proved",
            "current_value": "MISSING_NUMERIC_OR_ZERO_THEOREM",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COF4526_2_a_dotB",
            "quantity": "a_dotB",
            "definition": "linear scalar-channel coefficient for time/domain envelope drift",
            "formula": "a_dotB := partial f_local/partial z_dotB |_{z=0}",
            "source_status": "FORMULA_FILLED_VALUE_MISSING",
            "arena_effect": "feeds local drift/Gdot/clock residual if not zero",
            "current_value": "MISSING_NUMERIC_OR_ZERO_THEOREM",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COF4526_3_a_Lcg",
            "quantity": "a_Lcg",
            "definition": "linear scalar-channel coefficient for coarse-graining scale leakage",
            "formula": "a_Lcg := partial f_local/partial z_Lcg |_{z=0}",
            "source_status": "FORMULA_FILLED_VALUE_MISSING",
            "arena_effect": "weak blocker but must be zeroed or bounded",
            "current_value": "MISSING_NUMERIC_OR_ZERO_THEOREM",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COF4526_4_epsilon_source_material_private",
            "quantity": "epsilon_source_material_private",
            "definition": "source-weight/material-readout reentry defect inside the private GR-parity SM import branch",
            "formula": "epsilon_source_material_private := 0 in the private 4446/4447 branch",
            "source_status": "PRIVATE_BRANCH_ZERO_NONCLAIM",
            "arena_effect": "narrows WEP/PPN/Gdot/clock/orbital source subpieces, but does not close non-source residuals",
            "current_value": "0_PRIVATE_BRANCH_ONLY",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COF4526_5_epsilon_Poynting_wave",
            "quantity": "epsilon_Poynting_wave",
            "definition": "EM/Poynting boundary or radiative wave-flux defect when no-flux is not parent-owned",
            "formula": "epsilon_Poynting_wave := ||int_boundary v_A^nu T^EM_{mu nu} n^mu dSigma||/E_ref",
            "source_status": "FORMULA_FILLED_PROFILE_MISSING",
            "arena_effect": "retained boundary/source numerator for R10/PPN/clock/EM tests",
            "current_value": "MISSING_NO_FLUX_CERTIFICATE_OR_PROFILE",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COF4526_6_total_symmetry_breaking_bound",
            "quantity": "epsilon_symbreak_abs",
            "definition": "no-cancellation absolute envelope for symmetry-breaking residuals",
            "formula": "epsilon_symbreak_abs <= |epsilon_I|+|a_theta z_theta|+|a_dotB z_dotB|+|a_Lcg z_Lcg|+|epsilon_Poynting_wave|+sum_abs(non_source_survivors)",
            "source_status": "NO_CANCELLATION_BOUND_FORM_FILLED_VALUES_MISSING",
            "arena_effect": "feeds 4524 alpha/PPN/clock/orbit residual runner once coefficients/profiles are sourced",
            "current_value": "SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG4526_0_source_hunt",
            "gate": "real source hunt for vertical involution completed",
            "status": "PASS_PARTIAL_CANDIDATES_FOUND",
            "detail": "126/127/4195 provide conditional leakage parity; 128 blocks scalar-channel closure; 4446/4447 narrow source subpieces privately",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4526_1_parent_involution",
            "gate": "parent action invariant under I_q",
            "status": "BLOCKED_NOT_FOUND",
            "detail": "4195 explicitly marks S_parent[Phi]=S_parent[R_L Phi] missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4526_2_source_subpiece",
            "gate": "GR-parity source/material subpiece zero",
            "status": "PRIVATE_BRANCH_ZERO_NONCLAIM",
            "detail": "usable inside the private PPC4161 branch only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4526_3_local_GR",
            "gate": "local GR / Newton claim",
            "status": "BLOCKED",
            "detail": "scalar action asymmetry, auxiliary principal symbol, Morse-Bott Hessian and Poynting/no-flux profile remain open",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4526_0",
            "decision": DECISION,
            "meaning": "The corpus contains a usable conditional leakage parity lemma and private GR-parity source narrowing, but not a parent-owned full vertical involution. The branch moves forward by converting the surviving scalar/action/wave defects into source-normalized coefficient rows.",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "claim_id": CLAIM_ID,
            "marker": MARKER,
            "decision": DECISION,
            "claim_status": "private_conditional_nonclaim_source_hunt_and_coefficient_fill",
            "created_at_utc": now(),
            "next_target": NEXT_TARGET,
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "attack epsilon_I/action-asymmetry and auxiliary Z principal symbol as the two sharp parent-action clauses",
            "why": "If epsilon_I=0 and the vertical kinetic block vanishes, the parent-Z route becomes much stronger; if not, 4524 has the coefficient rows to score it.",
            "valid_for_claim": False,
        }
    ]


def validate(sources: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    csv_paths = [
        SOURCE_REGISTER,
        HUNT_CSV,
        BRIDGE_CSV,
        COEFFICIENT_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    parse_issues: list[str] = []
    for path in csv_paths:
        try:
            rows = read_csv(path)
            if not rows:
                parse_issues.append(f"{path.name}:empty")
        except Exception as error:
            parse_issues.append(f"{path.name}:{error}")

    hunt_statuses = {row.get("status") for row in read_csv(HUNT_CSV)}
    coeff_ids = {row.get("coefficient_id") for row in read_csv(COEFFICIENT_CSV)}
    bridge_ids = {row.get("bridge_id") for row in read_csv(BRIDGE_CSV)}
    rows = [
        {
            "validation_id": "VAL4526_00_sources",
            "status": "PASS" if all(row["exists"] and row["needle_found"] for row in sources) else "FAIL",
            "detail": "all source paths exist and source needles are found",
        },
        {
            "validation_id": "VAL4526_01_hunt",
            "status": "PASS" if {"EXACT_CONDITIONAL_SUBLEMMA", "NOT_FOUND", "PRIVATE_BRANCH_SOURCE_SUBPIECE_ZERO"}.issubset(hunt_statuses) else "FAIL",
            "detail": "source hunt records conditional lemma, missing parent action, and private source-zero subpiece",
        },
        {
            "validation_id": "VAL4526_02_bridge",
            "status": "PASS" if "BRG4526_4_full_parent_Z_verdict" in bridge_ids else "FAIL",
            "detail": "ZL-to-parent-Z bridge verdict present",
        },
        {
            "validation_id": "VAL4526_03_coefficients",
            "status": "PASS" if {"COF4526_0_epsilon_I", "COF4526_4_epsilon_source_material_private", "COF4526_6_total_symmetry_breaking_bound"}.issubset(coeff_ids) else "FAIL",
            "detail": "action-asymmetry, private source zero and total bound rows present",
        },
        {
            "validation_id": "VAL4526_04_claims_blocked",
            "status": "PASS" if all(str(row.get("valid_for_claim", "")).lower() == "false" for row in gates) else "FAIL",
            "detail": "all claim gates remain blocked",
        },
        {
            "validation_id": "VAL4526_05_csv_parse",
            "status": "PASS" if not parse_issues else "FAIL",
            "detail": ";".join(parse_issues) if parse_issues else "all generated CSV files parse and have rows",
        },
        {
            "validation_id": "VAL4526_06_pycache_absent",
            "status": "PASS" if not (SCRIPT_DIR / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after cleanup",
        },
    ]
    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append({"validation_id": "VAL4526_OVERALL", "status": overall, "detail": "4526 vertical involution source hunt and coefficient fill"})
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    hunt: list[dict[str, Any]],
    bridge: list[dict[str, Any]],
    coefficients: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4526 — Vertical Involution Source Hunt Or First Source-Normalized Coefficient Fill

Marker: `{MARKER}`  
Packet marker: `{PACKET_MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}`  
Status: private conditional non-claim; source hunt completed, coefficient route sharpened.

## What Actually Moved

The source hunt did find something useful: the old `126–128` leakage-parity path and `4195` parent-`Z_L` parity lemma are exactly the substructure needed for the 4525 parent-`Z` mechanism. But they only cover a leakage subbundle unless the parent theory supplies an involution `I_q` on the full vertical kernel.

The honest improvement is this:

```text
4525 needed: parent vertical involution I_q
4195 gives: conditional leakage involution R_L
4526 bridge: R_L works if it extends to I_q and S_parent[I_q Phi]=S_parent[Phi]
```

That full parent action signature is not found. However, `4446/4447` do narrow the source side inside the private PPC4161 branch: standard-matter source-weight/material-readout pieces can be carried as private-zero/nonclaim subpieces. The live obstruction is now sharper: scalar action asymmetry, scalar-channel stationarity, auxiliary/principal-symbol rank, Hessian lock, and Poynting/no-flux profiles.

## Source Hunt

{table(hunt)}

## ZL To Parent-Z Bridge

{table(bridge)}

## First Source-Normalized Coefficient Rows

{table(coefficients)}

## Claim Gates

{table(gates)}

## Decision

{table(decisions)}

## Sources

{table(sources)}

## Validation

{table(validation)}

## Next

`{NEXT_TARGET}`.
"""


def append_claim_once() -> None:
    current = text(CLAIMS_PATH)
    if f"{CLAIM_ID}," in current:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_r2fr_vertical_involution",
        "claim": "4526 performs the vertical-involution source hunt, bridges prior Z_L parity work to the 4525 parent-Z mechanism conditionally, and fills first source-normalized symmetry-breaking coefficient rows.",
        "current_evidence": "Generated source-hunt rows, ZL-to-parent-Z bridge theorem, coefficient rows, claim gates and validation P8_Y5_BRR545_4526_VALIDATION.csv.",
        "status": "conditional_internal_nonclaim_source_hunt_partial_narrowing",
        "next_test": NEXT_TARGET,
        "key_risk": "The full parent action involution, auxiliary principal-zero block and Morse-Bott Hessian are not sourced; private GR-parity source zero is not a public local-GR claim.",
        "sector": "local_gr_newton",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Treating the leakage subbundle parity lemma or private source-material zero as full parent-Z local-GR closure.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    hunt = hunt_rows()
    bridge = bridge_rows()
    coefficients = coefficient_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    status = status_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(HUNT_CSV, hunt)
    write_csv(BRIDGE_CSV, bridge)
    write_csv(COEFFICIENT_CSV, coefficients)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, gates)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, hunt, bridge, coefficients, gates, decisions, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4526 Vertical Involution Source Hunt Or First Source-Normalized Coefficient Fill

Marker: `{MARKER}`  
The parent-Z route now reuses prior leakage-parity work instead of circling it: `126–128` and `4195` provide a conditional `Z_L` parity sublemma, while 4526 gives the bridge condition needed to extend it to the full parent vertical involution `I_q`. The source hunt does not find the full parent action invariance, but `4446/4447` narrow standard-matter source/material pieces to private-zero subpieces. Remaining live coefficients are action asymmetry, scalar-channel linears, Poynting/wave flux, auxiliary principal symbol and Hessian lock.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4526 Packet Integration

Marker: `{PACKET_MARKER}`  
The PPC4161 packet now has a concrete bridge from old leakage parity to the new parent-Z action mechanism, plus source-normalized coefficient rows for the symmetry-breaking fallback. Next target: `{NEXT_TARGET}`.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
