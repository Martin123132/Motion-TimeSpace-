from __future__ import annotations

import csv
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
MICRO_RESIDUALS = POST / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"

CHECKPOINT = "4373"
CLAIM_ID = "L-214"
BRANCH = "MTS_R2FR_Y5_TRANSITION_FIRST_EPERP_COMPONENT_ZERO_OR_BOUND_MEASURE_SOURCE_MASS_4373"
MARKER = "PPC4161_TRANSITION_FIRST_EPERP_COMPONENT_ZERO_OR_BOUND_MEASURE_SOURCE_MASS_4373"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_FIRST_EPERP_COMPONENT_ZERO_OR_BOUND_MEASURE_SOURCE_MASS_4373"
DECISION = "FIRST_EPERP_COMPONENT_ZERO_NOT_PARENT_SIGNED_BOUND_TEMPLATES_DERIVED_NONCLAIM"
NEXT_TARGET = "4374-Y5-R2FR-transition-same-worldtube-source-mass-owner-or-Emass-bound.md"

FORMAL_PATH = FORMAL / "389-PPC4161-transition-first-Eperp-component-zero-or-bound-measure-source-mass.md"
DOC_PATH = POST / "4373-Y5-R2FR-transition-first-Eperp-component-zero-or-bound-measure-source-mass.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4373_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4373_00_4372_formal": (
        FORMAL / "388-PPC4161-transition-Eperp-envelope-decomposition-or-measure-owner-action-line-proof.md",
        "E_perp <= E_measure + E_mass + E_transition + E_Xi + E_T.",
        "4372 gives the no-cancellation component envelope to refine.",
    ),
    "SRC4373_01_4372_components": (
        SOURCE_DIR / "P8_Y5_R2FR_4372_EPERP_COMPONENT_ENVELOPES.csv",
        "EP4372_0_measure",
        "4372 names E_measure and E_mass as the first components to attack.",
    ),
    "SRC4373_02_4372_measure_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_4372_MEASURE_OWNER_ACTION_LINE_AUDIT.csv",
        "MA4372_1_species_blind_measure",
        "4372 records the unsigned measure/Jacobian/hbar clause.",
    ),
    "SRC4373_03_4361_premises": (
        SOURCE_DIR / "P8_Y5_R2FR_4361_PREMISE_AUDIT.csv",
        "P4361_2_measure_owner",
        "4361 keeps the parent measure owner premise unsigned.",
    ),
    "SRC4373_04_1606_measure_edge": (
        MICRO_RESIDUALS / "R2FR_parent_owned_edge_audit_nonclaim_1606.csv",
        "EDGE1606_5_measure",
        "1606 leaves species Jacobian exclusion unsigned.",
    ),
    "SRC4373_05_4178_measure_leak": (
        SOURCE_DIR / "P8_Y5_R2FR_4178_REACTIVATION_LEDGER.csv",
        "RE4178_1_ZH_leak",
        "4178 says nonzero source-measure leak reopens local tests.",
    ),
    "SRC4373_06_4178_mass_leak": (
        SOURCE_DIR / "P8_Y5_R2FR_4178_REACTIVATION_LEDGER.csv",
        "RE4178_2_wrong_mass_charge",
        "4178 says mass/source-charge mismatch reopens measured-GM/orbital rows.",
    ),
    "SRC4373_07_186_mass_glue": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "Pi_M := Pi_M^H",
        "186 selects the Hamiltonian/Hilbert mass map before orbital readout.",
    ),
    "SRC4373_08_187_poisson": (
        FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md",
        "int_W rho_H dV = M_H^dress",
        "187 connects the Poisson source density to the Hamiltonian dressed mass.",
    ),
    "SRC4373_09_194_calibrated_source": (
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "No orbital `GM`",
        "194 blocks defining the source mass by fitted orbital GM.",
    ),
    "SRC4373_10_4371_support": (
        SOURCE_DIR / "P8_Y5_R2FR_4371_SOURCE_SUPPORT_GEOMETRY.csv",
        "SUP4371_2_Sun_Earth_average",
        "4371 supplies the support geometry K_N(s) rows used for component bounds.",
    ),
}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: str(row.get(field, "")) for field in fields})


def csv_line(row: Iterable[str]) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(list(row))
    return buffer.getvalue()


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def append_claim_once(path: Path, claim_id: str, row: List[str]) -> None:
    text = read_text(path)
    if f"\n{claim_id}," in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + csv_line(row), encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        line_number = find_line(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
                "valid_for_claim": "False",
            }
        )
    return rows


def measure_zero_rows() -> List[Dict[str, str]]:
    return [
        {
            "row_id": "MZ4373_0_definition",
            "object": "E_measure",
            "statement": "E_measure is the source-measure part of the noncommon source-normalization envelope.",
            "formula": "delta_ZH = delta_ZH_common + delta_ZH_perp; E_measure := ||delta_ZH_perp||_inf",
            "derivation_or_blocker": "Common measure rescaling calibrates G_cal; only the transverse/source-dependent part survives local tests.",
            "status": "DERIVED_DEFINITION",
            "activates_zero": "False",
            "valid_for_claim": "False",
        },
        {
            "row_id": "MZ4373_1_conditional_zero_theorem",
            "object": "E_measure",
            "statement": "A single q-basic species-blind matter measure with no hidden source slot gives E_measure=0.",
            "formula": "S_m=int dmu_* L_m(q(Phi),Psi_A); D_A ln dmu_*=0; no J_A,hbar_A,N_src => delta_ZH_perp=0",
            "derivation_or_blocker": "Variation sees the same measure for every source/species label before readout, so no noncommon measure defect can be formed.",
            "status": "CONDITIONAL_THEOREM_DERIVED_NOT_PARENT_SIGNED",
            "activates_zero": "False",
            "valid_for_claim": "False",
        },
        {
            "row_id": "MZ4373_2_unsigned_parent_clause",
            "object": "measure owner",
            "statement": "The current corpus does not yet parent-sign the measure/Jacobian/hbar/no-field-normalization clause.",
            "formula": "P4361_2=False and EDGE1606_5 parent_owned=False",
            "derivation_or_blocker": "A species Jacobian J_A, effective hbar_A, or source field-normalization can still generate delta_ZH_perp.",
            "status": "ZERO_BLOCKED_UNSIGNED",
            "activates_zero": "False",
            "valid_for_claim": "False",
        },
        {
            "row_id": "MZ4373_3_countermodel_retained",
            "object": "hidden source measure slot",
            "statement": "The minimal countermodel is still legal: multiply one matter sector by a q-nonbasic source-dependent Jacobian.",
            "formula": "dmu_A = dmu_* (1 + zeta_A(Phi)); D_A zeta_A != 0 => E_measure >= ||zeta_A_perp||_inf",
            "derivation_or_blocker": "Because the parent grammar has not excluded this slot globally, the theorem is not active on the full branch.",
            "status": "COUNTERMODEL_NOT_EXCLUDED",
            "activates_zero": "False",
            "valid_for_claim": "False",
        },
    ]


def measure_bound_rows() -> List[Dict[str, str]]:
    support_rows = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4371_SOURCE_SUPPORT_GEOMETRY.csv")
    rows: List[Dict[str, str]] = [
        {
            "bound_id": "MB4373_0_measure_component_gate",
            "support_id": "GENERAL",
            "source_body": "any compact source W",
            "test_body_or_readout": "external local readout",
            "K_N": "K_N(s)",
            "component": "E_measure",
            "definition": "E_measure := ||delta_ZH_perp||_inf",
            "component_only_pass_formula": "E_measure <= delta_N/K_N(s)",
            "full_sum_pass_formula": "E_measure+E_mass+E_transition+E_Xi+E_T <= delta_N/K_N(s)",
            "current_status": "BOUND_TEMPLATE_DERIVED_NO_NUMERIC_E_MEASURE",
            "valid_for_claim": "False",
        }
    ]
    for support in support_rows:
        rows.append(
            {
                "bound_id": f"MB4373_{support['support_id']}",
                "support_id": support["support_id"],
                "source_body": support["source_body"],
                "test_body_or_readout": support["test_body_or_readout"],
                "K_N": support["selected_K_N"],
                "component": "E_measure",
                "definition": "E_measure := ||delta_ZH_perp||_inf",
                "component_only_pass_formula": f"E_measure <= delta_N/{support['selected_K_N']}",
                "full_sum_pass_formula": f"E_measure+E_mass+E_transition+E_Xi+E_T <= delta_N/{support['selected_K_N']}",
                "current_status": "GEOMETRY_READY_MEASURE_VALUE_MISSING",
                "valid_for_claim": "False",
            }
        )
    rows.append(
        {
            "bound_id": "MB4373_derivative_measure_gate",
            "support_id": "CLOCK_OR_GDOT",
            "source_body": "calibrated source measure",
            "test_body_or_readout": "clock/Gdot/range drift",
            "K_N": "arena dependent",
            "component": "D_A E_measure",
            "definition": "E_measure_deriv(A) := L_A ||D_A delta_ZH_perp||_inf",
            "component_only_pass_formula": "L_A||D_A delta_ZH_perp||_inf <= delta_clock_or_Gdot",
            "full_sum_pass_formula": "measure derivative plus remaining derivative tails below arena residual budget",
            "current_status": "BOUND_TEMPLATE_DERIVED_NO_DERIVATIVE_SOURCE",
            "valid_for_claim": "False",
        }
    )
    return rows


def mass_owner_rows() -> List[Dict[str, str]]:
    return [
        {
            "row_id": "MO4373_0_definition",
            "object": "E_mass",
            "statement": "E_mass is the same-worldtube source-mass mismatch part of epsilon_Gsrc_perp.",
            "formula": "rho_eff = rho_H(1+delta_m); delta_m_perp = delta_m - <delta_m>_rho; E_mass := ||delta_m_perp||_inf",
            "derivation_or_blocker": "The common monopole <delta_m>_rho is absorbed by calibration; noncommon spatial/source mismatch drives local residuals.",
            "status": "DERIVED_DEFINITION",
            "activates_zero": "False",
            "valid_for_claim": "False",
        },
        {
            "row_id": "MO4373_1_conditional_zero_theorem",
            "object": "source mass owner",
            "statement": "If the gravitational source mass is exactly the Hamiltonian/Hilbert worldtube charge before readout, E_mass=0.",
            "formula": "Pi_M=Pi_M^H; M_H^dress=int_W rho_H dV=H_tau[S_link]-H_ref; same W_H; no boundary flux => delta_m_perp=0",
            "derivation_or_blocker": "The density sourcing Poisson/G_cal and the readout mass are the same parent charge, so no wrong-mass-charge residual remains.",
            "status": "CONDITIONAL_THEOREM_DERIVED_NOT_GLOBAL_BRANCH_SIGNED",
            "activates_zero": "False",
            "valid_for_claim": "False",
        },
        {
            "row_id": "MO4373_2_supporting_private_selector",
            "object": "formal 186/187/194 chain",
            "statement": "Existing formal notes already implement the desired private selector for M_Hdress, rho_H, and G_cal without orbital GM laundering.",
            "formula": "Pi_M := Pi_M^H; int_W rho_H dV = M_H^dress; G_cal := c^4 kappa_eff/(8*pi)",
            "derivation_or_blocker": "This is strong local-GR scaffolding, but it is not yet sealed against transition/boundary/readout reentry across the full parent branch.",
            "status": "PRIVATE_SELECTOR_SUPPORTS_ROUTE",
            "activates_zero": "False",
            "valid_for_claim": "False",
        },
        {
            "row_id": "MO4373_3_open_reactivation_edges",
            "object": "mass mismatch reentry",
            "statement": "The mass zero theorem is blocked by the still-open wrong-mass-charge and boundary/transition flux reactivation rows.",
            "formula": "RE4178_2 or RE4178_4 nonzero => E_mass may reopen",
            "derivation_or_blocker": "Need one same-branch theorem tying H_ref, boundary flux, transition hair, and source support to the Hilbert owner.",
            "status": "ZERO_BLOCKED_BY_BRANCH_REENTRY",
            "activates_zero": "False",
            "valid_for_claim": "False",
        },
    ]


def mass_bound_rows() -> List[Dict[str, str]]:
    support_rows = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4371_SOURCE_SUPPORT_GEOMETRY.csv")
    rows: List[Dict[str, str]] = [
        {
            "bound_id": "MMB4373_0_mass_component_gate",
            "support_id": "GENERAL",
            "source_body": "any compact source W",
            "test_body_or_readout": "external local readout",
            "K_N": "K_N(s)",
            "component": "E_mass",
            "definition": "E_mass := ||delta_m_perp||_inf",
            "component_only_pass_formula": "E_mass <= delta_N/K_N(s)",
            "full_sum_pass_formula": "E_measure+E_mass+E_transition+E_Xi+E_T <= delta_N/K_N(s)",
            "current_status": "BOUND_TEMPLATE_DERIVED_NO_NUMERIC_E_MASS",
            "valid_for_claim": "False",
        }
    ]
    for support in support_rows:
        rows.append(
            {
                "bound_id": f"MMB4373_{support['support_id']}",
                "support_id": support["support_id"],
                "source_body": support["source_body"],
                "test_body_or_readout": support["test_body_or_readout"],
                "K_N": support["selected_K_N"],
                "component": "E_mass",
                "definition": "E_mass := ||delta_m_perp||_inf",
                "component_only_pass_formula": f"E_mass <= delta_N/{support['selected_K_N']}",
                "full_sum_pass_formula": f"E_measure+E_mass+E_transition+E_Xi+E_T <= delta_N/{support['selected_K_N']}",
                "current_status": "GEOMETRY_READY_MASS_VALUE_MISSING",
                "valid_for_claim": "False",
            }
        )
    rows.append(
        {
            "bound_id": "MMB4373_green_transfer",
            "support_id": "GREEN_KERNEL",
            "source_body": "worldtube W_H",
            "test_body_or_readout": "exterior potential",
            "K_N": "geometry kernel",
            "component": "delta_m_perp",
            "definition": "deltaPhi_mass(x) = -G_cal int_W rho_H(y) delta_m_perp(y)/|x-y| dV_y",
            "component_only_pass_formula": "|grad deltaPhi_mass|/|grad Phi_N| <= delta_N",
            "full_sum_pass_formula": "mass Green residual included in the same no-cancellation sum",
            "current_status": "DERIVED_TRANSFER_NO_SOURCE_DENSITY_BOUND",
            "valid_for_claim": "False",
        }
    )
    return rows


def component_score_rows() -> List[Dict[str, str]]:
    return [
        {
            "component_id": "EP4373_0_measure",
            "symbol": "E_measure",
            "before_4373": "CONDITIONAL_LEMMA_UNSIGNED",
            "after_4373": "CONDITIONAL_ZERO_THEOREM_PLUS_FINITE_BOUND_TEMPLATE",
            "zero_status": "BLOCKED_UNSIGNED_MEASURE_OWNER",
            "bound_status": "GEOMETRY_GATE_READY_SOURCE_VALUE_MISSING",
            "score_contribution": "included in E_measure+E_mass+E_transition+E_Xi+E_T",
            "next_action": "parent-sign species-blind measure/Jacobian/hbar exclusion or source a numeric delta_ZH_perp envelope",
            "valid_for_claim": "False",
        },
        {
            "component_id": "EP4373_1_mass",
            "symbol": "E_mass",
            "before_4373": "PRIVATE_SELECTOR_NOT_GLOBAL",
            "after_4373": "CONDITIONAL_ZERO_THEOREM_PLUS_FINITE_BOUND_TEMPLATE",
            "zero_status": "BLOCKED_BY_BRANCH_REENTRY",
            "bound_status": "GEOMETRY_GATE_READY_SOURCE_VALUE_MISSING",
            "score_contribution": "included in E_measure+E_mass+E_transition+E_Xi+E_T",
            "next_action": "prove same-worldtube source-mass owner across H_ref, boundary flux and transition hair, or source a numeric delta_m_perp envelope",
            "valid_for_claim": "False",
        },
        {
            "component_id": "EP4373_2_transition",
            "symbol": "E_transition",
            "before_4373": "TRANSITION_KERNEL_UNSIGNED",
            "after_4373": "CARRIED_OPEN",
            "zero_status": "NOT_ATTEMPTED_IN_4373",
            "bound_status": "MISSING_COMPONENT_INPUT",
            "score_contribution": "remaining term in no-cancellation sum",
            "next_action": "attack transition kernel membership after first source/mass component route",
            "valid_for_claim": "False",
        },
        {
            "component_id": "EP4373_3_Xi",
            "symbol": "E_Xi",
            "before_4373": "OPEN_TAIL_RETAINED",
            "after_4373": "CARRIED_OPEN",
            "zero_status": "NOT_ATTEMPTED_IN_4373",
            "bound_status": "MISSING_COMPONENT_INPUT",
            "score_contribution": "remaining term in no-cancellation sum",
            "next_action": "prove source-label forgetting/no-hidden-slot clauses or bound Xi components",
            "valid_for_claim": "False",
        },
        {
            "component_id": "EP4373_4_Topen",
            "symbol": "E_T",
            "before_4373": "PROJECTION_MATRIX_INPUTS_OPEN",
            "after_4373": "CARRIED_OPEN",
            "zero_status": "NOT_ATTEMPTED_IN_4373",
            "bound_status": "MISSING_COMPONENT_INPUT",
            "score_contribution": "remaining term in no-cancellation sum",
            "next_action": "fill or zero arena projection matrix components before scoring",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4373_0_measure_zero",
            "claim_tested": "E_measure=0",
            "required_inputs": "single action line; species-blind q-basic measure; no J_A/hbar_A/field-normalization/source-prefactor; variation before readout",
            "status": "BLOCKED_UNSIGNED_PARENT_MEASURE_OWNER",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4373_1_measure_bound",
            "claim_tested": "finite E_measure local-test pass",
            "required_inputs": "numeric/source-backed delta_ZH_perp or derivative envelope plus arena delta_N",
            "status": "BOUND_FORM_DERIVED_INPUT_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4373_2_mass_zero",
            "claim_tested": "E_mass=0",
            "required_inputs": "global same-branch Pi_M=Pi_M^H, same worldtube/support, fixed H_ref, no boundary/transition reentry",
            "status": "BLOCKED_BY_BRANCH_REENTRY",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4373_3_mass_bound",
            "claim_tested": "finite E_mass local-test pass",
            "required_inputs": "numeric/source-backed delta_m_perp envelope plus arena delta_N",
            "status": "BOUND_FORM_DERIVED_INPUT_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4373_4_local_GR",
            "claim_tested": "local GR/Newton/PPN pass",
            "required_inputs": "all five E_perp components zeroed or bounded, plus PPN/clock/orbital arena closures",
            "status": "FORBIDDEN_COMPONENTS_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4373_0",
            "decision": DECISION,
            "summary": (
                "4373 did not merely restate missing inputs: it derived the exact first-component zero theorems and the finite fallback gates. "
                "E_measure would vanish if the parent action has one q-basic species-blind matter measure with no J_A/hbar_A/source-prefactor slot, but the corpus has not signed that clause. "
                "E_mass would vanish if the Poisson source density and measured mass are the same Hamiltonian/Hilbert worldtube charge on the same branch; 186/187/194 strongly support the selector, but boundary/transition/readout reentry is not globally closed. "
                "Both components now have component-only and full-sum K_N(s) bound forms. No local-GR/Newton/PPN claim fires."
            ),
            "next_target": NEXT_TARGET,
            "why_next": "E_mass is closest to the existing GR/Newton scaffold because 186/187/194 already define Pi_M, rho_H and G_cal without orbital GM laundering.",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4373_0",
            "object": "E_measure",
            "status": "ZERO_THEOREM_DERIVED_BUT_UNSIGNED",
            "note": "the theorem is mathematically clean, but source Jacobian/hbar/normalization slots remain legal until parent grammar excludes them.",
        },
        {
            "status_id": "STAT4373_1",
            "object": "E_measure bound",
            "status": "FINITE_GATE_DERIVED",
            "note": "E_measure can now be tested by E_measure <= delta_N/K_N(s), but no numeric/source-backed delta_ZH_perp exists yet.",
        },
        {
            "status_id": "STAT4373_2",
            "object": "E_mass",
            "status": "ZERO_THEOREM_DERIVED_PRIVATE_SELECTOR_SUPPORTED",
            "note": "the same-worldtube Hilbert mass route is promising but not globally branch-signed.",
        },
        {
            "status_id": "STAT4373_3",
            "object": "E_mass bound",
            "status": "FINITE_GATE_DERIVED",
            "note": "E_mass can now be tested by E_mass <= delta_N/K_N(s), but no numeric/source-backed delta_m_perp exists yet.",
        },
        {
            "status_id": "STAT4373_4",
            "object": "next work",
            "status": "MASS_OWNER_BRIDGE",
            "note": "best next route is to close or bound the same-worldtube source-mass owner because it directly locks MTS to GR/Newton.",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4373_0",
            "target": NEXT_TARGET,
            "question": "Can the same-worldtube source-mass owner be made global, or must E_mass become a sourced finite residual?",
            "preferred_route": "prove Pi_M=Pi_M^H, int_W rho_H dV=M_H^dress, fixed H_ref, no boundary flux and no transition-hair reentry on one branch",
            "alternate_route": "source or bound delta_m_perp and score it with K_N(s)",
            "avoid": "using the private selector as public local-GR proof before branch reentry is closed",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    measure_zero: List[Dict[str, str]],
    measure_bounds: List[Dict[str, str]],
    mass_owner: List[Dict[str, str]],
    mass_bounds: List[Dict[str, str]],
    components: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# PPC4161 transition: first E_perp component zero or bound, measure/source-mass route

Marker: `{MARKER}`

Private checkpoint: `{CHECKPOINT}`  
UTC stamp: `{STAMP}`  
Decision: `{DECISION}`

## Result

4373 attacks the first two `E_perp` components instead of adding another foggy ledger.

The source-measure component is now precise:

```text
delta_ZH = delta_ZH_common + delta_ZH_perp,
E_measure := ||delta_ZH_perp||_inf.
```

Conditional zero theorem:

```text
S_m = int dmu_* L_m(q(Phi), Psi_A),
D_A ln dmu_* = 0,
no J_A, hbar_A, N_src, or field-normalization source slot
  => E_measure = 0.
```

This theorem is not activated because the parent measure owner clause remains unsigned.

The same-source mass component is also precise:

```text
rho_eff = rho_H(1 + delta_m),
delta_m_perp = delta_m - <delta_m>_rho,
E_mass := ||delta_m_perp||_inf.
```

Conditional zero theorem:

```text
Pi_M = Pi_M^H,
M_H^dress = int_W rho_H dV = H_tau[S_link] - H_ref,
same W_H and no boundary/transition reentry
  => E_mass = 0.
```

This route is stronger than vibes: formal notes 186/187/194 already support the private selector. It still does not become a public local-GR claim until the same branch also closes `H_ref`, boundary flux, transition hair, and readout reentry.

For both components, the fallback gate is now explicit:

```text
E_component <= delta_N/K_N(s)
```

for a component-only test, and

```text
E_measure + E_mass + E_transition + E_Xi + E_T <= delta_N/K_N(s)
```

for the full no-cancellation local source score.

## Source Register

{md_table(sources, ["source_id", "path", "path_exists", "needle", "needle_found", "line_number", "role"])}

## Measure Zero Attempt

{md_table(measure_zero, ["row_id", "object", "statement", "formula", "derivation_or_blocker", "status", "activates_zero"])}

## Measure Bound Gate

{md_table(measure_bounds, ["bound_id", "support_id", "source_body", "test_body_or_readout", "K_N", "component", "component_only_pass_formula", "full_sum_pass_formula", "current_status"])}

## Mass Owner Attempt

{md_table(mass_owner, ["row_id", "object", "statement", "formula", "derivation_or_blocker", "status", "activates_zero"])}

## Mass Mismatch Bound Gate

{md_table(mass_bounds, ["bound_id", "support_id", "source_body", "test_body_or_readout", "K_N", "component", "component_only_pass_formula", "full_sum_pass_formula", "current_status"])}

## Component Score Update

{md_table(components, ["component_id", "symbol", "before_4373", "after_4373", "zero_status", "bound_status", "next_action"])}

## Claim Gates

{md_table(gates, ["gate_id", "claim_tested", "required_inputs", "status", "claim_allowed"])}

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Status

{md_table(statuses, ["status_id", "object", "status", "note"])}

## Next Target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "alternate_route", "avoid"])}
"""
    FORMAL_PATH.write_text(text, encoding="utf-8")


def write_post_doc(decisions: List[Dict[str, str]], next_targets: List[Dict[str, str]]) -> None:
    text = f"""# 4373: first E_perp component zero or bound, measure/source-mass route

Marker: `{MARKER}`

## What changed

- Derived the exact conditional zero theorem for `E_measure`.
- Derived the exact finite bound gate for `E_measure`.
- Derived the exact conditional zero theorem for `E_mass`.
- Derived the exact finite bound gate for `E_mass`.
- Selected the next route: same-worldtube source-mass owner before wider tails.

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Next target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "alternate_route", "avoid"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_spine_update() -> None:
    block = f"""
## 4373 Transition first E_perp component zero/bound

Marker: `{MARKER}`

4373 turns the first two local-source obstruction components into explicit theorems and gates:

```text
E_measure := ||delta_ZH_perp||_inf,
E_mass := ||delta_m_perp||_inf.
```

`E_measure=0` follows from one q-basic species-blind matter measure with no Jacobian/hbar/source-prefactor/field-normalization slot, but that parent clause remains unsigned. `E_mass=0` follows when `Pi_M=Pi_M^H` and `M_H^dress=int_W rho_H dV=H_tau[S_link]-H_ref` on the same worldtube with no boundary/transition/readout reentry. Formal notes 186/187/194 support this selector but do not yet globally branch-sign it.

Fallback gates are now explicit:

```text
E_component <= delta_N/K_N(s),
E_measure+E_mass+E_transition+E_Xi+E_T <= delta_N/K_N(s).
```

Next target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, block)


def write_packet_update() -> None:
    block = f"""
## 4373 packet update: E_measure/E_mass zero-or-bound gates

Marker: `{PACKET_MARKER}`

Packet update: the first two `E_perp` components now have exact conditional zero routes and finite K_N(s) fallback gates. `E_measure` is blocked by unsigned measure/Jacobian/hbar owner clauses. `E_mass` is the better next attack because the existing GR/Newton chain already defines `Pi_M`, `rho_H`, `M_H^dress`, and `G_cal`; the remaining problem is making that selector global against boundary/transition/readout reentry.
"""
    append_once(PACKET_PATH, PACKET_MARKER, block)


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            (
                "4373 derives the first E_perp component zero-or-bound laws. "
                "For source measure, E_measure := ||delta_ZH_perp||_inf and a single q-basic species-blind matter measure with no J_A/hbar_A/source-prefactor/field-normalization slot would imply E_measure=0, but the parent measure owner clause remains unsigned. "
                "For source mass, E_mass := ||delta_m_perp||_inf and Pi_M=Pi_M^H with M_H^dress=int_W rho_H dV=H_tau[S_link]-H_ref on the same worldtube and no boundary/transition/readout reentry would imply E_mass=0. "
                "Existing 186/187/194 notes support the private selector, but not global branch closure. "
                "Both components now have fallback gates E_component <= delta_N/K_N(s) and full-sum scoring inside E_measure+E_mass+E_transition+E_Xi+E_T. No local-GR/Newton/PPN/clock/orbital claim fires."
            ),
            "4373 source register, measure zero attempt, measure bound gate, mass owner attempt, mass mismatch bound gate, component score update, claim gates, decision, status, next target and validation CSV.",
            "first_component_zero_or_bound_theorems_derived_unsigned_nonclaim",
            "Close the same-worldtube source-mass owner across H_ref, boundary flux, transition hair and readout reentry, or source a numeric E_mass envelope.",
            "Using the private mass selector as a public local-GR proof; claiming E_measure=0 while source Jacobian/hbar/normalization slots remain legal; treating component-only gates as full E_perp closure.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4373_SOURCE_REGISTER.csv")
    measure_zero = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4373_MEASURE_ZERO_ATTEMPT.csv")
    measure_bounds = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4373_MEASURE_BOUND_GATE.csv")
    mass_owner = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4373_MASS_OWNER_ATTEMPT.csv")
    mass_bounds = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4373_MASS_MISMATCH_BOUND_GATE.csv")
    components = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4373_COMPONENT_SCORE_UPDATE.csv")
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4373_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": str(bool(passed)),
                "detail": detail,
            }
        )

    add("VAL4373_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited local source exists")
    add("VAL4373_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited local source needle resolves")
    add(
        "VAL4373_2_measure_definition",
        any("E_measure := ||delta_ZH_perp||_inf" in row["formula"] for row in measure_zero),
        "E_measure definition derived",
    )
    add(
        "VAL4373_3_measure_zero_blocked",
        any(row["status"] == "ZERO_BLOCKED_UNSIGNED" for row in measure_zero) and all(row["activates_zero"] == "False" for row in measure_zero),
        "measure zero theorem is not falsely activated",
    )
    add(
        "VAL4373_4_measure_bound_gate",
        any("E_measure <= delta_N/K_N(s)" in row["component_only_pass_formula"] for row in measure_bounds),
        "general E_measure bound gate exists",
    )
    add(
        "VAL4373_5_mass_definition",
        any("E_mass := ||delta_m_perp||_inf" in row["formula"] for row in mass_owner),
        "E_mass definition derived",
    )
    add(
        "VAL4373_6_mass_zero_blocked",
        any(row["status"] == "ZERO_BLOCKED_BY_BRANCH_REENTRY" for row in mass_owner) and all(row["activates_zero"] == "False" for row in mass_owner),
        "mass zero theorem is not falsely activated",
    )
    add(
        "VAL4373_7_mass_bound_gate",
        any("E_mass <= delta_N/K_N(s)" in row["component_only_pass_formula"] for row in mass_bounds),
        "general E_mass bound gate exists",
    )
    add(
        "VAL4373_8_component_updates",
        {row["symbol"] for row in components} == {"E_measure", "E_mass", "E_transition", "E_Xi", "E_T"},
        "component score update keeps all five E_perp terms",
    )
    add("VAL4373_9_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4373_10_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4373_11_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4373_12_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4373_13_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4373_14_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4373_15_no_claim_rows",
        all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path))
        and all(row.get("claim_allowed", "False") == "False" for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add("VAL4373_16_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    return validations


def main() -> None:
    sources = source_rows()
    measure_zero = measure_zero_rows()
    measure_bounds = measure_bound_rows()
    mass_owner = mass_owner_rows()
    mass_bounds = mass_bound_rows()
    components = component_score_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4373_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4373_MEASURE_ZERO_ATTEMPT.csv": measure_zero,
        "P8_Y5_R2FR_4373_MEASURE_BOUND_GATE.csv": measure_bounds,
        "P8_Y5_R2FR_4373_MASS_OWNER_ATTEMPT.csv": mass_owner,
        "P8_Y5_R2FR_4373_MASS_MISMATCH_BOUND_GATE.csv": mass_bounds,
        "P8_Y5_R2FR_4373_COMPONENT_SCORE_UPDATE.csv": components,
        "P8_Y5_R2FR_4373_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4373_DECISION.csv": decisions,
        "P8_Y5_R2FR_4373_STATUS.csv": statuses,
        "P8_Y5_R2FR_4373_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = []
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, measure_zero, measure_bounds, mass_owner, mass_bounds, components, gates, decisions, statuses, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()

    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
