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

CHECKPOINT = "4374"
CLAIM_ID = "L-215"
MARKER = "PPC4161_TRANSITION_SAME_WORLDTUBE_SOURCE_MASS_OWNER_OR_EMASS_BOUND_4374"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_SAME_WORLDTUBE_SOURCE_MASS_OWNER_OR_EMASS_BOUND_4374"
DECISION = "SAME_TOTAL_MASS_NOT_ENOUGH_DENSITY_PROFILE_OWNER_OR_EMASS_BOUND_REQUIRED_NONCLAIM"
NEXT_TARGET = "4375-Y5-R2FR-transition-density-profile-owner-or-Emass-numeric-source-bound.md"

FORMAL_PATH = FORMAL / "390-PPC4161-transition-same-worldtube-source-mass-owner-or-Emass-bound.md"
DOC_PATH = POST / "4374-Y5-R2FR-transition-same-worldtube-source-mass-owner-or-Emass-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4374_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4374_00_4373_formal": (
        FORMAL / "389-PPC4161-transition-first-Eperp-component-zero-or-bound-measure-source-mass.md",
        "E_mass := ||delta_m_perp||_inf.",
        "4373 defines the E_mass object to refine.",
    ),
    "SRC4374_01_4373_mass": (
        SOURCE_DIR / "P8_Y5_R2FR_4373_MASS_OWNER_ATTEMPT.csv",
        "MO4373_1_conditional_zero_theorem",
        "4373 gives the same-worldtube conditional zero attempt.",
    ),
    "SRC4374_02_4354_formal": (
        FORMAL / "370-PPC4161-Htau-MHref-source-charge-owner-or-finite-GN-drift-bound.md",
        "int_W rho_H dV_H = M_H^dress",
        "4354 provides the integrated Hamiltonian/Hilbert source-mass bridge.",
    ),
    "SRC4374_03_4354_source_rows": (
        SOURCE_DIR / "P8_Y5_R2FR_4354_SOURCE_CHARGE_ROWS.csv",
        "SC4354_9_full_source_charge",
        "4354 lists same-worldtube, Htau/Href, integrability, reference, tau/frame, boundary and denominator gates.",
    ),
    "SRC4374_04_186_mass_glue": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "Pi_M := Pi_M^H",
        "186 locks Pi_M to the Hamiltonian/Hilbert charge inside the private selector.",
    ),
    "SRC4374_05_187_poisson": (
        FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md",
        "int_W rho_H dV = M_H^dress",
        "187 connects rho_H to Poisson/Gauss/Newton source mass.",
    ),
    "SRC4374_06_194_calibrated": (
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "No orbital `GM`",
        "194 enforces anti-circularity for M_Hdress, rho_H and G_cal.",
    ),
    "SRC4374_07_192_boundary": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "F_rad[tau] != 0  =>  route as boundary charge",
        "4176/192 routes nonzero radiative flux as boundary charge rather than hidden bulk mass.",
    ),
    "SRC4374_08_4178_reactivation": (
        SOURCE_DIR / "P8_Y5_R2FR_4178_REACTIVATION_LEDGER.csv",
        "RE4178_2_wrong_mass_charge",
        "4178 marks wrong mass/worldtube mismatch as a local-test reactivation edge.",
    ),
    "SRC4374_09_4355_transition": (
        FORMAL / "371-PPC4161-transition-shell-same-worldtube-nonHilbert-residue-or-bounded-source-hair.md",
        "epsilon_tr_hair <=",
        "4355 keeps transition source hair as a finite no-cancellation source residual unless kernel membership closes.",
    ),
    "SRC4374_10_4356_common_mode": (
        SOURCE_DIR / "P8_Y5_R2FR_4356_THEOREM_ROWS.csv",
        "TH4356_0_static_monopole_common_mode",
        "4356 identifies safe transition source dressing as stationary l=0 universal range-free common mode.",
    ),
    "SRC4374_11_4371_geometry": (
        SOURCE_DIR / "P8_Y5_R2FR_4371_SOURCE_SUPPORT_GEOMETRY.csv",
        "SUP4371_2_Sun_Earth_average",
        "4371 supplies K_N(s) support factors for exterior mass residual scoring.",
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


def theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "TH4374_0_density_profile_zero",
            "statement": "E_mass is zero only when the source density profile, not merely the integrated mass, is the same Hilbert density on the same worldtube before readout.",
            "formula": "rho_eff(y)=rho_H(y) on W_H and supp(rho_eff)=supp(rho_H) => delta_m(y)=0 => E_mass=0",
            "derivation": "Substitute rho_eff=rho_H into delta_m=(rho_eff-rho_H)/rho_H; the Hilbert-weighted common mode and transverse part both vanish.",
            "status": "DERIVED_CONDITIONAL_THEOREM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4374_1_total_mass_not_enough",
            "statement": "The 186/187/194 integrated mass bridge kills the monopole but does not by itself kill E_mass.",
            "formula": "int_W rho_H delta_m dV=0 does not imply ||delta_m_perp||_inf=0",
            "derivation": "A positive-negative density redistribution with zero Hilbert-weighted integral leaves the exterior monopole unchanged but leaves multipole/profile residuals that enter the K_N(s) bound.",
            "status": "DERIVED_FIREWALL",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4374_2_mass_owner_residual_split",
            "statement": "If pointwise density ownership is not signed, E_mass is bounded by named same-worldtube residual channels with no cancellation.",
            "formula": "E_mass <= E_profile + E_PiH + E_I + E_ref + E_tau + E_boundary + E_transition + E_readout",
            "derivation": "Write delta_m_perp as the sum of profile, projector/Htau, integrability, reference, tau/frame, boundary, transition and readout-order defects; apply the sup-norm triangle inequality.",
            "status": "DERIVED_BOUND_DECOMPOSITION",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4374_3_exterior_mass_score_transfer",
            "statement": "The 4370/4371 exterior Newton support gate scores the mass-owner residual split directly.",
            "formula": "|deltaa_mass|/|a_N| <= K_N(s)*(E_profile+E_PiH+E_I+E_ref+E_tau+E_boundary+E_transition+E_readout)",
            "derivation": "Substitute TH4374_2 into the 4373 mass component gate |deltaa_mass|/|a_N| <= K_N(s) E_mass.",
            "status": "DERIVED_SCORE_CHAIN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def clause_rows() -> List[Dict[str, str]]:
    return [
        {
            "clause_id": "DC4374_0_same_worldtube_support",
            "required_clause": "same compact Hilbert worldtube and source support before readout",
            "zeroes": "support/profile domain mismatch",
            "current_evidence": "SC4354_0 and 186/187 define W_H and M_Hdress",
            "current_status": "CONDITIONAL_NOT_GLOBAL",
            "fallback_residual": "E_profile_domain",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "DC4374_1_pointwise_Hilbert_density",
            "required_clause": "rho_eff(y)=rho_H(y), not just equal integrated mass",
            "zeroes": "E_profile",
            "current_evidence": "187 and 194 define rho_H as Poisson source density; no separate pointwise profile owner is globally signed",
            "current_status": "OPEN_KEY_STRENGTHENING",
            "fallback_residual": "E_profile",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "DC4374_2_PiH_Htau_glue",
            "required_clause": "Pi_M=Pi_M^H and ell_M(Pi_M^H J_H_total)=H_tau[S_link]-H_ref",
            "zeroes": "E_PiH",
            "current_evidence": "186 and 4354 give private selector zero",
            "current_status": "ZERO_INSIDE_PRIVATE_SELECTOR_ONLY",
            "fallback_residual": "E_PiH",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "DC4374_3_Htau_integrability",
            "required_clause": "Hamiltonian one-form is exact for all allowed local variations",
            "zeroes": "E_I",
            "current_evidence": "4354 imports H_tau integrability operator",
            "current_status": "OPERATOR_DERIVED_FULL_ZERO_CONDITIONAL",
            "fallback_residual": "E_I",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "DC4374_4_fixed_reference",
            "required_clause": "H_ref fixed before source/radius/frame/readout variation",
            "zeroes": "E_ref",
            "current_evidence": "4354 imports 4215 reference-lock theorem",
            "current_status": "CONDITIONAL_ZERO_THEOREM",
            "fallback_residual": "E_ref",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "DC4374_5_same_tau_frame_surface",
            "required_clause": "same tau, linking surface and observed coframe for source, clocks, orbit and PPN readout",
            "zeroes": "E_tau",
            "current_evidence": "4354 imports 4216 tau/surface/frame theorem",
            "current_status": "CONDITIONAL_ZERO_THEOREM",
            "fallback_residual": "E_tau",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "DC4374_6_boundary_flux_routing",
            "required_clause": "boundary/radiative/EM/Poynting flux is zero, fixed, or routed as Hamiltonian boundary charge, not hidden bulk mass",
            "zeroes": "E_boundary",
            "current_evidence": "192/4176 and 4354 boundary rows",
            "current_status": "CONDITIONAL_ZERO_WITH_ROUTED_FLUX_FALLBACK",
            "fallback_residual": "E_boundary",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "DC4374_7_transition_common_mode",
            "required_clause": "transition residue is stationary l=0 universal range-free same-metric Hilbert source dressing",
            "zeroes": "E_transition",
            "current_evidence": "4355/4356 derive conditional source-kernel/common-mode law",
            "current_status": "CONDITIONAL_THEOREM_RAW_SHELL_UNSIGNED",
            "fallback_residual": "E_transition",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "DC4374_8_readout_after_variation",
            "required_clause": "exterior/orbital/test readout is post-solve and cannot define the source density",
            "zeroes": "E_readout",
            "current_evidence": "186/187/194 anti-circularity plus 4355 full-domain readout import",
            "current_status": "PRIVATE_BRANCH_CONDITIONAL",
            "fallback_residual": "E_readout",
            "valid_for_claim": "False",
        },
    ]


def residual_rows() -> List[Dict[str, str]]:
    return [
        {
            "residual_id": "ER4374_0_profile",
            "symbol": "E_profile",
            "definition": "||[(rho_eff-rho_H)/rho_H]_perp||_inf after removing only the Hilbert-weighted common monopole",
            "zero_if": "rho_eff(y)=rho_H(y) pointwise on the same W_H",
            "source_anchor": "187/194 rho_H plus new density-profile owner clause",
            "status": "OPEN_KEY_INPUT",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "ER4374_1_PiH",
            "symbol": "E_PiH",
            "definition": "|ell_M(Pi_M^H J_H_total)-(H_tau[S_link]-H_ref)|/|M_Hdress| promoted to density/readout mismatch if outside private selector",
            "zero_if": "Pi_M/H_tau private selector is globally branch-adopted before readout",
            "source_anchor": "186; SC4354_2",
            "status": "PRIVATE_ZERO_ONLY",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "ER4374_2_integrability",
            "symbol": "E_I",
            "definition": "|I_MTS|/M_H_ref as mass-charge curl/profile leakage",
            "zero_if": "full MTS Hamiltonian one-form curl vanishes",
            "source_anchor": "SC4354_3",
            "status": "CONDITIONAL_ZERO",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "ER4374_3_reference",
            "symbol": "E_ref",
            "definition": "(|R_ref_selector|+|R_ref_source|+|R_ref_radius|+|R_ref_frame|+|R_ref_fit|+|R_ref_boundary|)/M_H_ref",
            "zero_if": "H_ref fixed and derivative-silent before readout",
            "source_anchor": "SC4354_4",
            "status": "CONDITIONAL_ZERO",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "ER4374_4_tau",
            "symbol": "E_tau",
            "definition": "(|R_tau_split|+|R_surface_motion|+|R_frame_coframe|+|R_clock_readout|+|R_orbital_readout|+|R_units|)/M_H_ref",
            "zero_if": "same tau/surface/e_obs branch selected before variation",
            "source_anchor": "SC4354_5",
            "status": "CONDITIONAL_ZERO",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "ER4374_5_boundary",
            "symbol": "E_boundary",
            "definition": "(|R_diff_owner|+|R_corner_edge|+|R_rad_flux|+|R_source_crossing|+|R_memory_pullback|+|R_improvement|)/M_H_ref",
            "zero_if": "differentiability-owned no-flux collar holds or flux is routed as Hamiltonian boundary charge",
            "source_anchor": "192; SC4354_6",
            "status": "CONDITIONAL_ZERO_WITH_FLUX_ROUTE",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "ER4374_6_transition",
            "symbol": "E_transition",
            "definition": "transition hair contribution epsilon_tr_hair projected into the source-density profile",
            "zero_if": "transition is stationary l=0 universal range-free same-metric Hilbert common-mode dressing",
            "source_anchor": "4355; 4356",
            "status": "CONDITIONAL_RAW_SHELL_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "ER4374_7_readout",
            "symbol": "E_readout",
            "definition": "source profile/readout-order mismatch if exterior/orbital/test readout defines or clips the source after variation",
            "zero_if": "variation and source solve occur on the full domain before exterior/readout restriction",
            "source_anchor": "186/187/194 anti-circularity; 4355 full-domain import",
            "status": "PRIVATE_BRANCH_CONDITIONAL",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "ER4374_8_total",
            "symbol": "E_mass",
            "definition": "E_profile + E_PiH + E_I + E_ref + E_tau + E_boundary + E_transition + E_readout",
            "zero_if": "all component residuals zero on one branch",
            "source_anchor": "TH4374_2",
            "status": "NO_CANCELLATION_SUM",
            "valid_for_claim": "False",
        },
    ]


def score_rows() -> List[Dict[str, str]]:
    support_rows = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4371_SOURCE_SUPPORT_GEOMETRY.csv")
    expression = "E_profile+E_PiH+E_I+E_ref+E_tau+E_boundary+E_transition+E_readout"
    rows: List[Dict[str, str]] = [
        {
            "score_id": "MS4374_GENERAL",
            "support_id": "GENERAL",
            "source_body": "compact source W_H",
            "test_body_or_readout": "external local readout",
            "K_N": "K_N(s)",
            "mass_residual_sum": expression,
            "fractional_residual": f"|deltaa_mass|/|a_N| <= K_N(s)*({expression})",
            "pass_formula": f"{expression} <= delta_N/K_N(s)",
            "current_status": "BOUND_CHAIN_DERIVED_INPUTS_MISSING",
            "valid_for_claim": "False",
        }
    ]
    for support in support_rows:
        rows.append(
            {
                "score_id": f"MS4374_{support['support_id']}",
                "support_id": support["support_id"],
                "source_body": support["source_body"],
                "test_body_or_readout": support["test_body_or_readout"],
                "K_N": support["selected_K_N"],
                "mass_residual_sum": expression,
                "fractional_residual": f"|deltaa_mass|/|a_N| <= {support['selected_K_N']}*({expression})",
                "pass_formula": f"{expression} <= delta_N/{support['selected_K_N']}",
                "current_status": "GEOMETRY_READY_COMPONENT_VALUES_MISSING",
                "valid_for_claim": "False",
            }
        )
    return rows


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4374_0_total_mass_bridge",
            "claim_tested": "integrated source mass bridge closes E_mass",
            "required_inputs": "pointwise/profile density owner as well as int_W rho_H dV=M_Hdress",
            "status": "REJECTED_TOTAL_MASS_NOT_ENOUGH",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4374_1_Emass_zero",
            "claim_tested": "E_mass=0",
            "required_inputs": "all DC4374 clauses close on the same branch, especially rho_eff(y)=rho_H(y)",
            "status": "BLOCKED_PROFILE_OWNER_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4374_2_Emass_bound",
            "claim_tested": "finite E_mass local Newton pass",
            "required_inputs": "numeric or theorem-zero rows for E_profile, E_PiH, E_I, E_ref, E_tau, E_boundary, E_transition and E_readout",
            "status": "BOUND_CHAIN_DERIVED_INPUTS_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4374_3_local_GR",
            "claim_tested": "local GR/Newton/PPN pass",
            "required_inputs": "E_mass plus E_measure/E_transition/E_Xi/E_T and PPN/clock/orbital closures",
            "status": "FORBIDDEN_COMPONENTS_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4374_0",
            "decision": DECISION,
            "summary": (
                "4374 tightens the mass-owner route. The existing 186/187/194 and 4354 chain is genuinely strong for the integrated monopole: it gives a non-circular Hamiltonian/Hilbert source mass and calibrated G_cal. "
                "But E_mass was defined as a profile/transverse source mismatch, so equal total mass is not enough. A zero-monopole density redistribution can leave E_mass nonzero and still perturb exterior fields through support/multipole geometry. "
                "Therefore the clean zero route now requires pointwise/profile Hilbert density ownership on the same worldtube before readout. If that is not signed, E_mass must be scored by the no-cancellation sum E_profile+E_PiH+E_I+E_ref+E_tau+E_boundary+E_transition+E_readout."
            ),
            "next_target": NEXT_TARGET,
            "why_next": "the new key object is E_profile; closing it would turn the private source-mass bridge into a much stronger local-GR/Newton branch.",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4374_0",
            "object": "integrated mass bridge",
            "status": "STRONG_PRIVATE_MONOPOLE_RESULT",
            "note": "186/187/194/4354 are useful and non-circular, but they control total source charge rather than the full E_mass profile.",
        },
        {
            "status_id": "STAT4374_1",
            "object": "E_mass zero route",
            "status": "PROFILE_OWNER_REQUIRED",
            "note": "E_mass=0 needs rho_eff(y)=rho_H(y) on the same worldtube before readout.",
        },
        {
            "status_id": "STAT4374_2",
            "object": "E_mass bound route",
            "status": "NO_CANCELLATION_SUM_DERIVED",
            "note": "E_mass now decomposes into eight named residual channels instead of a single foggy missing input.",
        },
        {
            "status_id": "STAT4374_3",
            "object": "exterior score",
            "status": "K_N_TRANSFER_READY",
            "note": "4371 geometry can score the mass residual sum once component values are zeroed or sourced.",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4374_0",
            "target": NEXT_TARGET,
            "question": "Can MTS parent-sign rho_eff(y)=rho_H(y) on W_H, or must E_profile become a finite source-density row?",
            "preferred_route": "derive density-profile ownership from Hilbert T00/source measure descent before readout",
            "alternate_route": "source or bound E_profile and score the full E_mass residual sum with K_N(s)",
            "avoid": "claiming E_mass=0 from integrated mass equality alone",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    theorems: List[Dict[str, str]],
    clauses: List[Dict[str, str]],
    residuals: List[Dict[str, str]],
    scores: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# PPC4161 transition: same-worldtube source-mass owner or E_mass bound

Marker: `{MARKER}`

Private checkpoint: `{CHECKPOINT}`  
UTC stamp: `{STAMP}`  
Decision: `{DECISION}`

## Result

4374 makes the source-mass route sharper rather than softer.

The existing local packet already has a strong private integrated source-charge chain:

```text
Pi_M = Pi_M^H,
M_H^dress[W_H;tau] = H_tau[S_link] - H_ref,
int_W rho_H dV = M_H^dress,
G_cal := c^4 kappa_eff/(8*pi).
```

That is good GR/Newton scaffolding. But it is not enough for the `E_mass` object from 4373, because:

```text
int_W rho_H delta_m dV = 0
  does not imply
||delta_m_perp||_inf = 0.
```

Equal total mass kills only the common monopole. A zero-monopole redistribution can still create a profile/multipole residual. Therefore the exact zero law is:

```text
rho_eff(y)=rho_H(y) on W_H
and same support/readout branch
  => E_mass=0.
```

If this pointwise/profile density-owner clause is not signed, the fallback is a real no-cancellation bound:

```text
E_mass <= E_profile + E_PiH + E_I + E_ref
        + E_tau + E_boundary + E_transition + E_readout.
```

and the exterior Newton score is:

```text
|deltaa_mass|/|a_N|
 <= K_N(s) (E_profile+E_PiH+E_I+E_ref+E_tau+E_boundary+E_transition+E_readout).
```

No local-GR/Newton/PPN claim fires from 4374.

## Source Register

{md_table(sources, ["source_id", "path", "path_exists", "needle", "needle_found", "line_number", "role"])}

## Theorems

{md_table(theorems, ["theorem_id", "statement", "formula", "derivation", "status"])}

## Density Owner Clauses

{md_table(clauses, ["clause_id", "required_clause", "zeroes", "current_evidence", "current_status", "fallback_residual"])}

## E_mass Residual Decomposition

{md_table(residuals, ["residual_id", "symbol", "definition", "zero_if", "source_anchor", "status"])}

## Geometry Score

{md_table(scores, ["score_id", "support_id", "source_body", "test_body_or_readout", "K_N", "mass_residual_sum", "pass_formula", "current_status"])}

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
    text = f"""# 4374: same-worldtube source-mass owner or E_mass bound

Marker: `{MARKER}`

## What changed

- Proved that equal integrated source mass is not enough to set `E_mass=0`.
- Promoted the clean zero target to pointwise/profile Hilbert density ownership: `rho_eff(y)=rho_H(y)` on `W_H`.
- Split `E_mass` into eight no-cancellation residual channels.
- Connected the residual sum to the existing `K_N(s)` exterior Newton support gate.

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Next target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "alternate_route", "avoid"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_spine_update() -> None:
    block = f"""
## 4374 Transition same-worldtube source-mass owner

Marker: `{MARKER}`

4374 tightens the local GR/Newton mass bridge. The existing private chain

```text
Pi_M=Pi_M^H,
M_H^dress=H_tau[S_link]-H_ref,
int_W rho_H dV=M_H^dress
```

is a strong non-circular integrated source-charge result. It does **not** by itself prove `E_mass=0`, because `E_mass` is a profile/transverse density mismatch:

```text
int_W rho_H delta_m dV=0 does not imply ||delta_m_perp||_inf=0.
```

The clean zero law is now:

```text
rho_eff(y)=rho_H(y) on W_H => E_mass=0.
```

Otherwise:

```text
E_mass <= E_profile+E_PiH+E_I+E_ref+E_tau+E_boundary+E_transition+E_readout.
```

Next target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, block)


def write_packet_update() -> None:
    block = f"""
## 4374 packet update: source mass needs density-profile ownership

Marker: `{PACKET_MARKER}`

Packet update: the Hamiltonian/Hilbert source mass chain is useful but only monopole-level unless it owns the density profile. `E_mass=0` now requires `rho_eff(y)=rho_H(y)` on the same worldtube before readout. If not, the local branch carries a no-cancellation sum: `E_profile+E_PiH+E_I+E_ref+E_tau+E_boundary+E_transition+E_readout`, scored by the existing `K_N(s)` geometry gate.
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
                "4374 derives the same-worldtube source-mass owner refinement. "
                "The integrated Hamiltonian/Hilbert mass chain Pi_M=Pi_M^H, M_Hdress=H_tau-H_ref and int_W rho_H dV=M_Hdress is strong but does not by itself set E_mass=0, because zero monopole mismatch does not imply zero density/profile mismatch. "
                "The exact zero theorem is rho_eff(y)=rho_H(y) on the same W_H before readout, which implies E_mass=0. "
                "If profile ownership is unsigned, E_mass is bounded by E_profile+E_PiH+E_I+E_ref+E_tau+E_boundary+E_transition+E_readout and scored by K_N(s). "
                "No local-GR/Newton/PPN/clock/orbital claim fires."
            ),
            "4374 source register, theorem rows, density owner clauses, E_mass residual decomposition, geometry score rows, claim gates, decision, status, next target and validation CSV.",
            "same_worldtube_source_mass_profile_owner_required_nonclaim",
            "Derive density-profile Hilbert ownership rho_eff(y)=rho_H(y), or source/bound E_profile and score the E_mass residual sum.",
            "Claiming E_mass=0 from integrated mass equality; treating orbital GM as source definition; hiding transition/boundary/readout profile residuals in calibration.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4374_SOURCE_REGISTER.csv")
    theorems = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4374_THEOREM_ROWS.csv")
    clauses = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4374_DENSITY_OWNER_CLAUSES.csv")
    residuals = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4374_EMASS_RESIDUAL_DECOMPOSITION.csv")
    scores = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4374_GEOMETRY_SCORE.csv")
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4374_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": str(bool(passed)),
                "detail": detail,
            }
        )

    add("VAL4374_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited local source exists")
    add("VAL4374_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited local source needle resolves")
    add(
        "VAL4374_2_total_mass_firewall",
        any(row["theorem_id"] == "TH4374_1_total_mass_not_enough" and "does not imply" in row["formula"] for row in theorems),
        "integrated-mass-not-enough theorem exists",
    )
    add(
        "VAL4374_3_density_profile_clause",
        any(row["clause_id"] == "DC4374_1_pointwise_Hilbert_density" and row["fallback_residual"] == "E_profile" for row in clauses),
        "pointwise density-profile owner clause exists",
    )
    add(
        "VAL4374_4_residual_split",
        {row["symbol"] for row in residuals} == {"E_profile", "E_PiH", "E_I", "E_ref", "E_tau", "E_boundary", "E_transition", "E_readout", "E_mass"},
        "E_mass split has exact named components",
    )
    add(
        "VAL4374_5_score_chain",
        any("E_profile+E_PiH+E_I+E_ref+E_tau+E_boundary+E_transition+E_readout" in row["pass_formula"] for row in scores),
        "geometry score uses residual sum",
    )
    add("VAL4374_6_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4374_7_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4374_8_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4374_9_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4374_10_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4374_11_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4374_12_no_claim_rows",
        all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path))
        and all(row.get("claim_allowed", "False") == "False" for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add("VAL4374_13_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    return validations


def main() -> None:
    sources = source_rows()
    theorems = theorem_rows()
    clauses = clause_rows()
    residuals = residual_rows()
    scores = score_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4374_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4374_THEOREM_ROWS.csv": theorems,
        "P8_Y5_R2FR_4374_DENSITY_OWNER_CLAUSES.csv": clauses,
        "P8_Y5_R2FR_4374_EMASS_RESIDUAL_DECOMPOSITION.csv": residuals,
        "P8_Y5_R2FR_4374_GEOMETRY_SCORE.csv": scores,
        "P8_Y5_R2FR_4374_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4374_DECISION.csv": decisions,
        "P8_Y5_R2FR_4374_STATUS.csv": statuses,
        "P8_Y5_R2FR_4374_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = []
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, theorems, clauses, residuals, scores, gates, decisions, statuses, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
