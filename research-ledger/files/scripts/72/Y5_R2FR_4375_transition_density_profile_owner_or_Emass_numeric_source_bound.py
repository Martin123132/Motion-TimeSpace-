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

CHECKPOINT = "4375"
CLAIM_ID = "L-216"
MARKER = "PPC4161_TRANSITION_DENSITY_PROFILE_OWNER_OR_EMASS_NUMERIC_SOURCE_BOUND_4375"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_DENSITY_PROFILE_OWNER_OR_EMASS_NUMERIC_SOURCE_BOUND_4375"
DECISION = "DENSITY_PROFILE_OWNER_THEOREM_DERIVED_SOURCE_SHADOW_COUNTERMODEL_RETAINED_EPROFILE_BOUND_READY_NONCLAIM"
NEXT_TARGET = "4376-Y5-R2FR-transition-source-shadow-ban-or-Eprofile-first-source-density-row.md"

FORMAL_PATH = FORMAL / "391-PPC4161-transition-density-profile-owner-or-Emass-numeric-source-bound.md"
DOC_PATH = POST / "4375-Y5-R2FR-transition-density-profile-owner-or-Emass-numeric-source-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4375_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4375_00_4374_formal": (
        FORMAL / "390-PPC4161-transition-same-worldtube-source-mass-owner-or-Emass-bound.md",
        "rho_eff(y)=rho_H(y) on W_H",
        "4374 sets the density-profile owner target.",
    ),
    "SRC4375_01_4374_clauses": (
        SOURCE_DIR / "P8_Y5_R2FR_4374_DENSITY_OWNER_CLAUSES.csv",
        "DC4374_1_pointwise_Hilbert_density",
        "4374 identifies pointwise Hilbert density as the key strengthening.",
    ),
    "SRC4375_02_185_source_measure": (
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "T_H^munu = -2/sqrt(-g_obs) delta S_src/delta g_obs_munu.",
        "185 defines the common Hilbert source stress from the same local source action.",
    ),
    "SRC4375_03_226_visible": (
        FORMAL / "226-PPC4161-standard-visible-matter-import-contract.md",
        "T_H = -2/sqrt(-g_obs) delta S_vis/delta g_obs.",
        "4210 imports calibrated visible matter as the standard Hilbert source.",
    ),
    "SRC4375_04_187_T00": (
        FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md",
        "T_00 = rho_H c^2 + higher order",
        "187 identifies rho_H through the weak-field T00 source.",
    ),
    "SRC4375_05_194_T00": (
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "T_00 = rho_H c^2.",
        "194 repeats the calibrated Poisson source density definition.",
    ),
    "SRC4375_06_227_owner": (
        FORMAL / "227-PPC4161-Htau-MHsource-parent-charge-owner.md",
        "int_W rho_H dV_H = M_H^dress[W_H;tau]",
        "4211 supplies the source-charge owner contract but not a full pointwise profile proof.",
    ),
    "SRC4375_07_191_poynting": (
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "T_EM^mu_nu =",
        "4175 makes EM/Poynting energy part of the same Hilbert stress rather than a hidden source.",
    ),
    "SRC4375_08_worldtube_measure": (
        SOURCE_DIR / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
        "T510_1_worldtube_source_measure",
        "worldtube source measure must be dressed Hamiltonian/Noether charge, not bare mass.",
    ),
    "SRC4375_09_total_hilbert_owner": (
        SOURCE_DIR / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_TOTAL_HILBERT_SOURCE_OWNER_AUDIT.csv",
        "THO2615_1_total_hilbert_derivative",
        "total Hilbert derivative owner route for ordinary active source.",
    ),
    "SRC4375_10_exchange_collapse": (
        SOURCE_DIR / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_NOETHER_EXCHANGE_COLLAPSE_THEOREM.csv",
        "NEC2615_2_weight_collapse",
        "Noether exchange collapse blocks relative source weights if ordinary matter graph is connected.",
    ),
    "SRC4375_11_selector_coupling": (
        SOURCE_DIR / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_WORLDTUBE_HILBERT_COUPLING_SELECTOR_THEOREM.csv",
        "WSC2577_1_worldtube_selector",
        "worldtube/source selector must be fixed before readout.",
    ),
    "SRC4375_12_source_bridge": (
        SOURCE_DIR / "P8_Y5_SOURCE_BRIDGE_2466_HILBERT_CURRENT_DESCENT.csv",
        "HIL2466_0_define_T",
        "matter current descent defines Hilbert stress as candidate universal source object.",
    ),
    "SRC4375_13_geometry": (
        SOURCE_DIR / "P8_Y5_R2FR_4371_SOURCE_SUPPORT_GEOMETRY.csv",
        "SUP4371_2_Sun_Earth_average",
        "K_N(s) geometry rows score any retained profile residual.",
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
            "theorem_id": "TH4375_0_Hilbert_density_profile_owner",
            "statement": "If the active local source density is defined by the same Hilbert T00 density used in the EH/Poisson equation, then the density-profile residual is zero.",
            "formula": "rho_H := T_H(n,n)/c^2; rho_eff := T_H(n,n)/c^2 on W_H => rho_eff(y)=rho_H(y) => E_profile=0",
            "derivation": "Both densities are the same functional derivative of S_vis/S_src with respect to the same observed metric/coframe and the same local observer n before readout.",
            "status": "DERIVED_CONDITIONAL_THEOREM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4375_1_same_action_profile_law",
            "statement": "Matter, EM/Poynting and binding energy must be included once in T_H before forming rho_H.",
            "formula": "T_H=T_matter+T_EM+T_binding+T_impr_exact+T_rest_top/zero; rho_H=T_H(n,n)/c^2",
            "derivation": "The Hilbert derivative of one visible/source action owns the local profile; EM flux is not a second background density and binding stress is not an optional after-fit correction.",
            "status": "DERIVED_CONDITIONAL_PROFILE_DEFINITION",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4375_2_source_shadow_countermodel",
            "statement": "A source-shadow density can keep the same integrated mass while changing E_profile, so the source-shadow ban is required.",
            "formula": "rho_eff = rho_H(1+sigma); int_W rho_H sigma dV=0; sigma_perp != 0 => E_profile=||sigma_perp||_inf>0",
            "derivation": "The monopole integral vanishes but the pointwise/profile residual survives and contributes through the exterior Green kernel.",
            "status": "COUNTERMODEL_DERIVED_RETAINED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4375_3_profile_Green_transfer",
            "statement": "If the profile owner is unsigned, the retained source-density residual has an exact Newtonian Green transfer.",
            "formula": "deltaPhi_profile(x)=-G_cal int_W rho_H(y) sigma_perp(y)/|x-y| dV_y",
            "derivation": "Substitute rho_eff-rho_H=rho_H sigma_perp into the 4369/4373 Poisson perturbation equation.",
            "status": "DERIVED_TRANSFER_LAW",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4375_4_profile_bound_gate",
            "statement": "The profile residual inherits the same K_N(s) exterior support score as E_mass.",
            "formula": "|deltaa_profile|/|a_N| <= K_N(s) E_profile",
            "derivation": "Apply the zero-monopole compact-source exterior bound to sigma_perp with E_profile=||sigma_perp||_inf.",
            "status": "DERIVED_SCORE_GATE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def profile_owner_clause_rows() -> List[Dict[str, str]]:
    return [
        {
            "clause_id": "PO4375_0_same_action",
            "required_clause": "rho_H and rho_eff are both generated from the same local source action S_vis/S_src",
            "mathematical_form": "T_H=-2/sqrt(-g_obs) delta S_src/delta g_obs; rho_eff=rho_H=T_H(n,n)/c^2",
            "current_evidence": "185 and 226 provide the private source action/Hilbert stress clause",
            "status": "PRIVATE_CONDITIONAL",
            "failure_mode": "source-shadow functional or non-Hilbert current defines rho_eff",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "PO4375_1_same_metric_coframe",
            "required_clause": "same observed metric/coframe and local observer n define T00 and readout",
            "mathematical_form": "n_source=n_readout and e_obs_source=e_obs_readout",
            "current_evidence": "4210/4211 source-charge contract; 4354 tau/frame rows",
            "status": "CONDITIONAL_NOT_GLOBAL",
            "failure_mode": "density profile and orbital/clock readout live in different frames",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "PO4375_2_all_visible_energy_once",
            "required_clause": "matter, binding and Maxwell-Hodge EM/Poynting stress are included once in T_H",
            "mathematical_form": "T_H=T_matter+T_EM+T_binding+T_impr_exact+T_rest_top/zero",
            "current_evidence": "185, 191 and 226",
            "status": "PRIVATE_CONDITIONAL",
            "failure_mode": "EM/binding/Poynting energy is omitted or double counted as hidden background source",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "PO4375_3_no_source_shadow_density",
            "required_clause": "no independent source-only density sigma_shadow with zero total mass but nonzero profile",
            "mathematical_form": "not exists sigma_shadow: int rho_H sigma_shadow dV=0 and sigma_shadow_perp != 0",
            "current_evidence": "2615 names source-shadow ban but leaves it parent unsigned",
            "status": "OPEN_KEY_BLOCKER",
            "failure_mode": "same M_Hdress, different density profile, nonzero E_profile",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "PO4375_4_worldtube_pre_readout",
            "required_clause": "W_H=supp(T_H(n,n)) is fixed before exterior/orbital/readout restriction",
            "mathematical_form": "W_H := supp(T_H(n,n)) before scoring",
            "current_evidence": "2577 worldtube selector and 227 owner contract",
            "status": "CONDITIONAL_NOT_GLOBAL",
            "failure_mode": "source support is clipped or selected after seeing residuals",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "PO4375_5_no_topological_profile_replacement",
            "required_clause": "topological/Hamiltonian charge may define total mass but cannot replace the local density profile unless it equals Hilbert T00 as a distribution",
            "mathematical_form": "J_top = J_H + dB with zero profile contribution, not only int_S J_top=int_W rho_H dV",
            "current_evidence": "510/2577 warn that the closed topological current can be the wrong object",
            "status": "OPEN_FOR_PROFILE_CLAIM",
            "failure_mode": "correct total charge with wrong local distribution",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "PO4375_6_no_transition_bulk_profile",
            "required_clause": "transition/common-mode hair enters only M_Hdress or boundary charge, not independent bulk density profile",
            "mathematical_form": "sigma_transition_perp=0 or retained in E_transition",
            "current_evidence": "4355/4356 common-mode transition law",
            "status": "CONDITIONAL_RAW_SHELL_UNSIGNED",
            "failure_mode": "transition shell creates a hidden zero-monopole density profile",
            "valid_for_claim": "False",
        },
    ]


def countermodel_rows() -> List[Dict[str, str]]:
    return [
        {
            "countermodel_id": "CM4375_0_zero_monopole_shadow",
            "setup": "rho_eff=rho_H(1+sigma) on W_H with int_W rho_H sigma dV=0",
            "what_passes": "integrated M_Hdress and monopole Gauss mass can remain unchanged",
            "what_fails": "E_profile=||sigma_perp||_inf can be nonzero and produce multipole/profile acceleration residuals",
            "lesson": "total mass equality is not density-profile ownership",
            "status": "RETAINED_UNTIL_SOURCE_SHADOW_BAN_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM4375_1_topological_wrong_distribution",
            "setup": "a closed topological representative has the same linking charge but not the same T_H(n,n) distribution",
            "what_passes": "surface charge conservation",
            "what_fails": "local Poisson density profile and interior/boundary multipoles",
            "lesson": "Hamiltonian/topological equality must be distributional or density-profile preserving",
            "status": "RETAINED_UNTIL_TOPOLOGICAL_HILBERT_EQUALITY_PROFILE_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM4375_2_em_poynting_double_count",
            "setup": "Poynting/binding energy is counted once in T_H and again as a background source density",
            "what_passes": "one can tune the total source charge",
            "what_fails": "source density profile and local conservation",
            "lesson": "visible energy must enter once through Hilbert stress or boundary flux, never as a second density",
            "status": "BLOCKED_IN_PRIVATE_MAXWELL_HODGE_BRANCH_BUT_RETAINED_OUTSIDE",
            "valid_for_claim": "False",
        },
    ]


def eprofile_bound_rows() -> List[Dict[str, str]]:
    support_rows = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4371_SOURCE_SUPPORT_GEOMETRY.csv")
    rows: List[Dict[str, str]] = [
        {
            "bound_id": "EPB4375_GENERAL",
            "support_id": "GENERAL",
            "source_body": "compact Hilbert worldtube W_H",
            "test_body_or_readout": "external local readout",
            "profile_variable": "sigma_perp=(rho_eff-rho_H)/rho_H - <(rho_eff-rho_H)/rho_H>_rho",
            "E_profile_definition": "E_profile=||sigma_perp||_inf",
            "green_transfer": "deltaPhi_profile(x)=-G_cal int_W rho_H sigma_perp/|x-y| dV",
            "pass_formula": "E_profile <= delta_N/K_N(s)",
            "current_status": "BOUND_TEMPLATE_DERIVED_SOURCE_PROFILE_MISSING",
            "valid_for_claim": "False",
        }
    ]
    for support in support_rows:
        rows.append(
            {
                "bound_id": f"EPB4375_{support['support_id']}",
                "support_id": support["support_id"],
                "source_body": support["source_body"],
                "test_body_or_readout": support["test_body_or_readout"],
                "profile_variable": "sigma_perp",
                "E_profile_definition": "E_profile=||sigma_perp||_inf",
                "green_transfer": "profile Green transfer scored through K_N(s)",
                "pass_formula": f"E_profile <= delta_N/{support['selected_K_N']}",
                "current_status": "GEOMETRY_READY_SOURCE_PROFILE_MISSING",
                "valid_for_claim": "False",
            }
        )
    rows.append(
        {
            "bound_id": "EPB4375_moment_refinement",
            "support_id": "MOMENT_REFINED",
            "source_body": "known density profile",
            "test_body_or_readout": "external multipole-sensitive readout",
            "profile_variable": "sigma_perp with moments M_L=int_W rho_H sigma_perp y^L dV",
            "E_profile_definition": "E_profile_moment := sum_L C_L |M_L|/(M_H r^L)",
            "green_transfer": "deltaPhi_profile expanded in zero-monopole multipoles",
            "pass_formula": "E_profile_moment <= delta_N before using coarse sup bound",
            "current_status": "OPTIONAL_TIGHTER_BOUND_REQUIRES_REAL_PROFILE",
            "valid_for_claim": "False",
        }
    )
    return rows


def source_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "input_id": "IN4375_0_density_profile",
            "needed_quantity": "rho_H(y) and any proposed rho_eff(y) on the same W_H",
            "units": "mass density or energy density/c^2",
            "source_path_required": "yes",
            "acceptance_rule": "must state action/source owner and whether profile is Hilbert T00, topological representative, transition shell, or empirical matter model",
            "current_status": "MISSING_NUMERIC_PROFILE",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4375_1_common_mode_subtraction",
            "needed_quantity": "<sigma>_rho = M_H^-1 int_W rho_H sigma dV",
            "units": "dimensionless",
            "source_path_required": "derived from same density profile",
            "acceptance_rule": "subtract common monopole before E_profile scoring",
            "current_status": "FORMULA_READY_INPUT_MISSING",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4375_2_support_geometry",
            "needed_quantity": "source radius/support R and readout radius r",
            "units": "length",
            "source_path_required": "yes",
            "acceptance_rule": "must be fixed before scoring and paired with K_N(s)",
            "current_status": "AVAILABLE_FOR_SOLAR_SYSTEM_EXAMPLES_FROM_4371",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4375_3_profile_moments",
            "needed_quantity": "optional zero-monopole multipole moments M_L",
            "units": "mass*length^L",
            "source_path_required": "yes if used",
            "acceptance_rule": "may tighten bound but cannot replace source owner theorem",
            "current_status": "OPTIONAL_NOT_FILLED",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4375_0_profile_zero",
            "claim_tested": "E_profile=0",
            "required_inputs": "all PO4375 clauses close on the same branch, especially no source-shadow density and no topological wrong-distribution replacement",
            "status": "BLOCKED_SOURCE_SHADOW_AND_PROFILE_EQUALITY_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4375_1_profile_bound",
            "claim_tested": "finite E_profile pass",
            "required_inputs": "source-backed rho_H/rho_eff profile or theorem-zero profile plus K_N(s)/delta_N arena threshold",
            "status": "BOUND_FORM_DERIVED_INPUT_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4375_2_Emass",
            "claim_tested": "E_mass pass",
            "required_inputs": "E_profile plus E_PiH, E_I, E_ref, E_tau, E_boundary, E_transition, E_readout zero/bound rows",
            "status": "FORBIDDEN_EPROFILE_AND_OTHER_COMPONENTS_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4375_3_local_GR",
            "claim_tested": "local GR/Newton/PPN pass",
            "required_inputs": "all E_perp components zeroed/bounded and PPN/clock/orbital projections fixed",
            "status": "FORBIDDEN_COMPONENTS_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4375_0",
            "decision": DECISION,
            "summary": (
                "4375 derives the exact density-profile owner theorem: if the active bulk source density is the same Hilbert T00 density T_H(n,n)/c^2 from the same S_vis/S_src before readout, then rho_eff=rho_H pointwise and E_profile=0. "
                "This is stronger and cleaner than total mass equality. The current corpus has private conditional support from 185/226/187/194/191, but the full claim is blocked by the source-shadow/topological wrong-distribution countermodel and by branch-global readout/profile ownership. "
                "Fallback is now scoreable: sigma_perp is defined, deltaPhi_profile has a Green integral, and E_profile <= delta_N/K_N(s) is ready once a real profile or theorem-zero certificate exists."
            ),
            "next_target": NEXT_TARGET,
            "why_next": "the source-shadow ban is the exact missing clause between private Hilbert T00 density and claim-grade E_profile=0.",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4375_0",
            "object": "Hilbert density profile theorem",
            "status": "DERIVED_CONDITIONAL",
            "note": "same T_H(n,n)/c^2 source density gives E_profile=0.",
        },
        {
            "status_id": "STAT4375_1",
            "object": "source-shadow countermodel",
            "status": "RETAINED",
            "note": "same total mass can hide nonzero zero-monopole profile sigma_perp.",
        },
        {
            "status_id": "STAT4375_2",
            "object": "profile bound",
            "status": "GREEN_TRANSFER_AND_KN_GATE_READY",
            "note": "E_profile can be scored once rho_H/rho_eff or a theorem-zero certificate is supplied.",
        },
        {
            "status_id": "STAT4375_3",
            "object": "next work",
            "status": "SOURCE_SHADOW_BAN_OR_FIRST_PROFILE_ROW",
            "note": "prove no source-shadow/topological wrong-distribution density, or fill a real E_profile source row.",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4375_0",
            "target": NEXT_TARGET,
            "question": "Can the source-shadow/topological wrong-distribution countermodel be forbidden, or must E_profile receive its first real density row?",
            "preferred_route": "derive no source-shadow density from same-action Hilbert derivative, Noether exchange connectivity, and source-label grammar",
            "alternate_route": "fill rho_H/rho_eff profile input rows and score E_profile through the Green/K_N gate",
            "avoid": "using total charge equality or calibrated visible matter alone as a density-profile proof",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    theorems: List[Dict[str, str]],
    clauses: List[Dict[str, str]],
    countermodels: List[Dict[str, str]],
    bounds: List[Dict[str, str]],
    inputs: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# PPC4161 transition: density-profile owner or E_mass numeric source bound

Marker: `{MARKER}`

Private checkpoint: `{CHECKPOINT}`  
UTC stamp: `{STAMP}`  
Decision: `{DECISION}`

## Result

4375 closes the logical gap exposed by 4374 as far as current evidence permits.

The clean density-profile law is:

```text
T_H = -2/sqrt(-g_obs) delta S_src/delta g_obs,
rho_H := T_H(n,n)/c^2,
rho_eff := T_H(n,n)/c^2 on W_H
  => rho_eff(y)=rho_H(y)
  => E_profile=0.
```

This is the right route: it derives the profile from the Hilbert source density itself, not from orbital `GM`, fitted `G`, or a topological charge chosen after readout.

But the theorem is conditional. The retained countermodel is:

```text
rho_eff = rho_H(1+sigma),
int_W rho_H sigma dV = 0,
sigma_perp != 0
  => same total mass but E_profile=||sigma_perp||_inf > 0.
```

So 4375 does not claim local GR. It identifies the exact missing clause: forbid any source-shadow/topological/projector density that preserves total charge while changing the local profile.

The finite fallback is now scoreable:

```text
sigma_perp = (rho_eff-rho_H)/rho_H - <(rho_eff-rho_H)/rho_H>_rho,
deltaPhi_profile(x) = -G_cal int_W rho_H(y) sigma_perp(y)/|x-y| dV_y,
|deltaa_profile|/|a_N| <= K_N(s) E_profile.
```

## Source Register

{md_table(sources, ["source_id", "path", "path_exists", "needle", "needle_found", "line_number", "role"])}

## Theorems

{md_table(theorems, ["theorem_id", "statement", "formula", "derivation", "status"])}

## Profile Owner Clauses

{md_table(clauses, ["clause_id", "required_clause", "mathematical_form", "current_evidence", "status", "failure_mode"])}

## Countermodels

{md_table(countermodels, ["countermodel_id", "setup", "what_passes", "what_fails", "lesson", "status"])}

## E_profile Bound Rows

{md_table(bounds, ["bound_id", "support_id", "source_body", "test_body_or_readout", "E_profile_definition", "green_transfer", "pass_formula", "current_status"])}

## Source Input Rows

{md_table(inputs, ["input_id", "needed_quantity", "units", "source_path_required", "acceptance_rule", "current_status"])}

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
    text = f"""# 4375: density-profile owner or E_mass numeric source bound

Marker: `{MARKER}`

## What changed

- Derived the conditional Hilbert density-profile theorem: same `T_H(n,n)/c^2` source density gives `E_profile=0`.
- Kept the source-shadow/topological wrong-distribution countermodel because total mass equality is not profile equality.
- Added the exact Green transfer for retained `sigma_perp`.
- Added `E_profile <= delta_N/K_N(s)` source-density input gates.

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Next target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "alternate_route", "avoid"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_spine_update() -> None:
    block = f"""
## 4375 Transition density-profile owner

Marker: `{MARKER}`

4375 derives the clean profile zero theorem:

```text
rho_H := T_H(n,n)/c^2,
rho_eff := T_H(n,n)/c^2 on W_H
=> rho_eff(y)=rho_H(y)
=> E_profile=0.
```

The theorem is conditional because a source-shadow/topological wrong-distribution density can preserve total mass while changing the profile:

```text
rho_eff=rho_H(1+sigma),
int_W rho_H sigma dV=0,
sigma_perp != 0.
```

The retained bound is exact enough to score later:

```text
deltaPhi_profile(x)=-G_cal int_W rho_H sigma_perp/|x-y| dV,
|deltaa_profile|/|a_N| <= K_N(s) E_profile.
```

Next target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, block)


def write_packet_update() -> None:
    block = f"""
## 4375 packet update: Hilbert density-profile owner

Marker: `{PACKET_MARKER}`

Packet update: `E_profile=0` now has a clean conditional theorem: the active bulk source density must be exactly the Hilbert energy density `T_H(n,n)/c^2` from the same visible/source action on the same worldtube before readout. The live blocker is no longer vague density language; it is the source-shadow/topological wrong-distribution countermodel. If that cannot be banned, `sigma_perp` is retained and scored by the Green/K_N profile gate.
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
                "4375 derives the density-profile owner theorem: if rho_H and rho_eff are both the same Hilbert source density T_H(n,n)/c^2 from the same S_vis/S_src on the same worldtube before readout, then rho_eff(y)=rho_H(y) and E_profile=0. "
                "The theorem remains conditional because a source-shadow/topological wrong-distribution density can preserve the integrated mass while leaving sigma_perp nonzero. "
                "If unsigned, sigma_perp has an exact profile Green transfer deltaPhi_profile=-G_cal int rho_H sigma_perp/|x-y| dV and the local score gate |deltaa_profile|/|a_N| <= K_N(s)E_profile. "
                "No local-GR/Newton/PPN/clock/orbital claim fires."
            ),
            "4375 source register, theorem rows, profile owner clauses, countermodels, E_profile bound rows, source input rows, claim gates, decision, status, next target and validation CSV.",
            "density_profile_owner_theorem_conditional_source_shadow_countermodel_retained_nonclaim",
            "Prove the source-shadow/topological wrong-distribution ban, or fill the first real rho_H/rho_eff profile row and score E_profile.",
            "Claiming density-profile equality from total charge equality; double-counting EM/Poynting/binding energy; using topological charge equality as distributional equality.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4375_SOURCE_REGISTER.csv")
    theorems = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4375_THEOREM_ROWS.csv")
    clauses = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4375_PROFILE_OWNER_CLAUSES.csv")
    countermodels = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4375_COUNTERMODELS.csv")
    bounds = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4375_EPROFILE_BOUND_ROWS.csv")
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4375_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": str(bool(passed)),
                "detail": detail,
            }
        )

    add("VAL4375_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited local source exists")
    add("VAL4375_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited local source needle resolves")
    add(
        "VAL4375_2_profile_theorem",
        any(row["theorem_id"] == "TH4375_0_Hilbert_density_profile_owner" and "E_profile=0" in row["formula"] for row in theorems),
        "Hilbert density-profile zero theorem exists",
    )
    add(
        "VAL4375_3_countermodel_retained",
        any(row["countermodel_id"] == "CM4375_0_zero_monopole_shadow" for row in countermodels)
        and any(row["clause_id"] == "PO4375_3_no_source_shadow_density" and row["status"] == "OPEN_KEY_BLOCKER" for row in clauses),
        "source-shadow countermodel and open blocker are retained",
    )
    add(
        "VAL4375_4_green_transfer",
        any("deltaPhi_profile" in row["green_transfer"] for row in bounds),
        "profile Green transfer rows exist",
    )
    add(
        "VAL4375_5_kn_gate",
        any("E_profile <= delta_N/K_N(s)" in row["pass_formula"] for row in bounds),
        "general K_N E_profile gate exists",
    )
    add("VAL4375_6_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4375_7_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4375_8_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4375_9_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4375_10_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4375_11_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4375_12_no_claim_rows",
        all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path))
        and all(row.get("claim_allowed", "False") == "False" for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add("VAL4375_13_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    return validations


def main() -> None:
    sources = source_rows()
    theorems = theorem_rows()
    clauses = profile_owner_clause_rows()
    countermodels = countermodel_rows()
    bounds = eprofile_bound_rows()
    inputs = source_input_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4375_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4375_THEOREM_ROWS.csv": theorems,
        "P8_Y5_R2FR_4375_PROFILE_OWNER_CLAUSES.csv": clauses,
        "P8_Y5_R2FR_4375_COUNTERMODELS.csv": countermodels,
        "P8_Y5_R2FR_4375_EPROFILE_BOUND_ROWS.csv": bounds,
        "P8_Y5_R2FR_4375_SOURCE_INPUT_ROWS.csv": inputs,
        "P8_Y5_R2FR_4375_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4375_DECISION.csv": decisions,
        "P8_Y5_R2FR_4375_STATUS.csv": statuses,
        "P8_Y5_R2FR_4375_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = []
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, theorems, clauses, countermodels, bounds, inputs, gates, decisions, statuses, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
