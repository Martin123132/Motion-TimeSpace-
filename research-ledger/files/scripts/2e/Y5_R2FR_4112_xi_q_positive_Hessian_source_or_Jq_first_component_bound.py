from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4112-Y5-R2FR-xi-q-positive-Hessian-source-or-Jq-first-component-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_XI_Q_JQ_TO_LOCAL_GR_CONTRACT_4112"
CHECKPOINT_ID = "4112"
DECISION = "XI_Q_JQ_EM_BRANCH_IMPORTED_TO_MINIMAL_LOCAL_GR_CONTRACT_BIANCHI_NEXT"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4112_00_4111_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4111_NEXT_TARGET.csv",
        "4112-Y5-R2FR-xi-q-positive-Hessian-source-or-Jq-first-component-bound.md",
        "4111 selected the xi_q/J_q fork as the next current-chain target.",
    ),
    "SRC4112_01_3611_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3611_STATUS.csv",
        "XI_Q_NOT_OWNED_JQ_MATTER_BULK_BOUND_LAW_FILLED",
        "3611 separated lowercase xi_q from source-overlap Xi and filled the first J_q matter bound law.",
    ),
    "SRC4112_02_3612_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3612_STATUS.csv",
        "JQ_MATTER_EM_POYNTING_SUBCOMPONENT_BOUND_FILLED_XI_OWNER_STILL_MISSING",
        "3612 converted the EM/Poynting part of J_q into a theorem-zero-or-bound vector.",
    ),
    "SRC4112_03_3613_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3613_STATUS.csv",
        "DELTA_HODGE_BOUND_FILLED",
        "3613 filled the Delta_Hodge_EM aggregate bound and zeroed pure conformal Hodge only.",
    ),
    "SRC4112_04_3617_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3617_STATUS.csv",
        "KTHETA_SYMBOLIC_DERIVED",
        "3617 derived the K_theta screen root-split projection bridge.",
    ),
    "SRC4112_05_3618_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3618_STATUS.csv",
        "SCREEN_ZERO_ROUTE_DERIVED",
        "3618 derived the conditional h_split=0 route for the observed-Hodge Maxwell branch.",
    ),
    "SRC4112_06_3619_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3619_STATUS.csv",
        "CONDITIONAL_EM_DOMAIN_THEOREM",
        "3619 wrote the conditional visible EM action-domain theorem and typed nonzero screen rows.",
    ),
    "SRC4112_07_3620_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3620_STATUS.csv",
        "EM_SOURCE_OWNER_CONDITIONAL_THEOREM",
        "3620 isolated the all-or-nothing EM source-coupling owner theorem.",
    ),
    "SRC4112_08_3623_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3623_STATUS.csv",
        "COUPLING_GAP_REDUCED",
        "3623 proved compact charge quantization alone cannot derive alpha/source calibration.",
    ),
    "SRC4112_09_3624_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3624_STATUS.csv",
        "MINIMAL_LOCAL_GR_CONTRACT_WRITTEN_NO_CLAIM",
        "3624 wrote the minimal local-GR contract with calibrated constants plus explicit residual vector.",
    ),
    "SRC4112_10_3624_residual_vector": (
        SOURCE_DIR / "P8_Y5_R2FR_3624_EXPLICIT_MTS_RESIDUAL_VECTOR.csv",
        "RV3624_6_PPN_total",
        "3624 explicit residual vector, including PPN no-cancellation envelope.",
    ),
    "SRC4112_11_3624_next": (
        SOURCE_DIR / "P8_Y5_R2FR_3624_NEXT_TARGET.csv",
        "3625-Y5-R2FR-Bianchi-residual-closure-or-first-PPN-envelope-runner.md",
        "3624 selected Bianchi/residual closure or PPN envelope as next target.",
    ),
    "SRC4112_12_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4112_xi_q_positive_Hessian_source_or_Jq_first_component_bound.py",
        "Reproducible generator for this 4112 current-chain checkpoint.",
    ),
}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def bool_string(value: bool) -> str:
    return "True" if value else "False"


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def row_base() -> dict:
    return {
        "timestamp_utc": TIMESTAMP,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
    }


def source_register_rows() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                **row_base(),
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_string(path.exists()),
                "needle": needle,
                "needle_found": bool_string(needle in text),
                "role": role,
                "claim_allowed": bool_string(False),
                "valid_for_claim": bool_string(False),
            }
        )
    return rows


def imported_chain_rows() -> List[dict]:
    chain = [
        (
            "IMP4112_0_3611",
            "xi_q/J_q fork",
            "lambda_q=xi_q exact conditional ratio retained; xi_q/H_AB not owned; J_q^matter_bulk bound law filled",
            "turns q from abstract operator debt into either quotient-zero or physical residual range xi_q",
            "SRC4112_01_3611_status",
        ),
        (
            "IMP4112_1_3612",
            "EM/Poynting J_q subcomponent",
            "bound EM/Poynting is inside total Hilbert stress under common-owner clauses; residual vector kept otherwise",
            "answers the Poynting concern without pretending flux vanishes by wording",
            "SRC4112_02_3612_status",
        ),
        (
            "IMP4112_2_3613",
            "Hodge/conformal split",
            "Delta_Hodge_EM has named bound components; pure conformal scale is zero only for 4D Maxwell two-form Hodge",
            "keeps clock/source/alpha normalization scale alive instead of hiding it",
            "SRC4112_03_3613_status",
        ),
        (
            "IMP4112_3_3617",
            "GRB/Fresnel projection bridge",
            "K_theta derived through physical polarization screen operator, not scalar double-root shortcut",
            "creates an actual comparison bridge while blocking claims until parent screen inputs exist",
            "SRC4112_04_3617_status",
        ),
        (
            "IMP4112_4_3618",
            "screen split zero route",
            "observed-Hodge Maxwell branch gives h_split=0 conditionally; nonzero branches typed by operator dimension",
            "GRB birefringence does not hit the local branch if visible EM action-domain exhaustion closes",
            "SRC4112_05_3618_status",
        ),
        (
            "IMP4112_5_3619",
            "visible EM action-domain theorem",
            "two-derivative visible EM action reduces to observed-Hodge Maxwell plus topological axion if no hidden slots survive",
            "turns independent chi_EM into a forbidden-by-domain or explicit coefficient row problem",
            "SRC4112_06_3619_status",
        ),
        (
            "IMP4112_6_3620",
            "EM source-coupling owner",
            "A_Q, F_Q^2, J_Q, alpha_EM, Poynting/Hilbert stress and source mass must share one owner packet",
            "identifies the coupling throat without letting a knob move from F2 into current/source readout",
            "SRC4112_07_3620_status",
        ),
        (
            "IMP4112_7_3623",
            "calibrated-constant strategy",
            "compact U(1) alone cannot derive alpha/source calibration; measured G_eff/alpha_eff are acceptable if residuals close",
            "matches how GR treats G while preserving the stricter MTS residual burden",
            "SRC4112_08_3623_status",
        ),
        (
            "IMP4112_8_3624",
            "minimal local-GR contract",
            "EH/Newton/Maxwell forms use calibrated constants plus explicit MTS residual vector",
            "moves the project from hunting every numerical constant to deriving equation form and killing/bounding residuals",
            "SRC4112_09_3624_status",
        ),
    ]
    return [
        {
            **row_base(),
            "import_id": import_id,
            "imported_step": imported_step,
            "result": result,
            "why_it_matters": why_it_matters,
            "source_id": source_id,
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for import_id, imported_step, result, why_it_matters, source_id in chain
    ]


def xi_q_jq_rows() -> List[dict]:
    rows = [
        (
            "XJ4112_0_xi_ratio",
            "xi_q positive-Hessian fork",
            "M_q^2=n_q^A H_AB n_q^B; Z_q=xi_q^2 n_q^A H_AB n_q^B => lambda_q=xi_q",
            "EXACT_CONDITIONAL_RATIO_IMPORTED",
            "parent xi_q, positive H_AB, q-normal, domain and boundary are not owned",
        ),
        (
            "XJ4112_1_quotient_zero",
            "q no-pole branch",
            "if pi/v_q quotient certificate closes, q is representative-only and has no physical pole",
            "CONDITIONAL_NO_POLE_ROUTE_RETAINED",
            "parent pi and Dpi[v_q]=0 component certificate unsigned",
        ),
        (
            "XJ4112_2_physical_q",
            "physical q residual branch",
            "if q is physical, its finite range is not arbitrary: lambda_q=xi_q and source is J_q",
            "PHYSICAL_BRANCH_SHARPENED",
            "xi_q/H_AB or first J_q subcomponent theorem/bound still required",
        ),
        (
            "XJ4112_3_jq_matter_bulk",
            "J_q^matter_bulk",
            "ordinary matter contribution has absolute no-cancellation bound over geometry, constants, source weights, boundary, readout and non-Hilbert pieces",
            "FIRST_COMPONENT_BOUND_LAW_IMPORTED",
            "subcomponents must be theorem-zeroed or source-backed individually",
        ),
        (
            "XJ4112_4_em_poynting_subcomponent",
            "J_q^EM/Poynting",
            "bound EM/Poynting is Hilbert stress under common-owner clauses; flux/Hodge/normalization/readout tails remain explicit residuals",
            "SUBCOMPONENT_ADVANCED",
            "observed Hodge, source current, stationary boundary and normalization owners not jointly parent-signed",
        ),
    ]
    return [
        {
            **row_base(),
            "row_id": row_id,
            "object": obj,
            "formula_or_statement": formula,
            "status": status,
            "remaining_gate": gate,
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for row_id, obj, formula, status, gate in rows
    ]


def em_screen_spine_rows() -> List[dict]:
    rows = [
        (
            "EMS4112_0_hodge_bound",
            "Delta_Hodge_EM",
            "||Delta_Hodge_EM|| <= ||Delta_chi_principal|| + ||Delta_chi_skewon|| + L||d theta_EM|| + |C_Hodge_hidden| + |C_Hodge_readout| + |Delta_orientation_flux|",
            "AGGREGATE_BOUND_IMPORTED",
            "SRC4112_03_3613_status",
        ),
        (
            "EMS4112_1_conformal_guard",
            "pure conformal Hodge piece",
            "4D Maxwell Hodge on two-forms is conformally invariant, but source mass/clocks/alpha/current scale remain live",
            "SUBTHEOREM_ZERO_FOR_HODGE_ONLY",
            "SRC4112_03_3613_status",
        ),
        (
            "EMS4112_2_ktheta_bridge",
            "K_theta",
            "K_theta(s)=C_screen k0^(s+1) I_s(z)/(4 gamma0 M_*^s H0); s=1 gives K_Fresnel=C_screen M_pl/(4 gamma0 M_*)",
            "SCREEN_ROOT_SPLIT_DERIVED",
            "SRC4112_04_3617_status",
        ),
        (
            "EMS4112_3_hsplit_zero",
            "visible Maxwell screen split",
            "same_metric && observed_Hodge && unique_F2 && no_chi_EM && no_HD_screen && constant_or_absent_axion_gradient => h_split=0",
            "CONDITIONAL_ZERO_ROUTE_IMPORTED",
            "SRC4112_05_3618_status",
        ),
        (
            "EMS4112_4_domain_theorem",
            "visible EM action-domain",
            "if local EM arguments are only A_Q, F_Q=dA_Q, e_obs(q), fixed current/representation data and orientation, the two-derivative principal action is observed-Hodge Maxwell plus topological axion",
            "EXACT_CONDITIONAL_DOMAIN_THEOREM",
            "SRC4112_06_3619_status",
        ),
        (
            "EMS4112_5_source_owner_packet",
            "F2/current/Hilbert source coupling",
            "A_Q, T_Q/N_Q, unique F2, J_Q, alpha_eff, T_EM and Poynting source mass must share one parent owner or finite rows remain",
            "COUPLING_THROAT_IDENTIFIED",
            "SRC4112_07_3620_status",
        ),
    ]
    return [
        {
            **row_base(),
            "spine_id": spine_id,
            "object": obj,
            "formula_or_statement": formula,
            "status": status,
            "source_id": source_id,
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for spine_id, obj, formula, status, source_id in rows
    ]


def local_gr_contract_rows() -> List[dict]:
    rows = [
        (
            "LGC4112_0_calibrated_constants",
            "G_eff and alpha_eff",
            "calibrated low-energy constants are allowed at local-GR reduction stage",
            "GR measures G; MTS must derive the equation form and suppress extra residuals before claiming more",
        ),
        (
            "LGC4112_1_metric_equation",
            "Einstein-Hilbert normal form",
            "G_mn+Lambda_eff g_mn = kappa_eff(T_matter_mn+T_EM_mn)+DeltaE_MTS_mn",
            "DeltaE_MTS must be theorem-zeroed or projected below local tests",
        ),
        (
            "LGC4112_2_newton_limit",
            "Newton/Poisson weak field",
            "nabla^2 Phi = 4*pi*G_eff*rho_H + delta_Newton_MTS",
            "rho_H must be fixed before orbital fitting and delta_Newton_MTS must close or be bounded",
        ),
        (
            "LGC4112_3_maxwell_hilbert",
            "Maxwell Hilbert stress and Poynting flow",
            "T_EM enters the same Hilbert source slot; T_EM^{0i}=S_Poynting^i/c^2 in local inertial frame",
            "observed Hodge/current/source ownership and boundary flux branches remain open",
        ),
        (
            "LGC4112_4_ppn_vector",
            "PPN/no-cancellation envelope",
            "Delta_PPN_abs=|gamma-1|+|beta-1|+|alpha_i|+|zeta_i|+|xi|+readout/source terms",
            "every component needs independent theorem-zero or source-backed bound",
        ),
        (
            "LGC4112_5_bianchi",
            "Bianchi/conservation compatibility",
            "nabla_m[DeltaE_MTS^{mn}-kappa_eff DeltaT_MTS^{mn}]=0",
            "next target because residual zeroing must be Noether-consistent",
        ),
    ]
    return [
        {
            **row_base(),
            "contract_id": contract_id,
            "contract_piece": piece,
            "formula_or_statement": formula,
            "required_next": next_step,
            "source_id": "SRC4112_09_3624_status",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for contract_id, piece, formula, next_step in rows
    ]


def residual_gate_rows() -> List[dict]:
    residuals = [
        ("RG4112_0_DeltaE", "DeltaE_MTS_mn", "EH dominance/Lovelock/locality theorem or local-test projection bound", "PPN;R10;orbital;clocks"),
        ("RG4112_1_source_weight", "DeltaT_source;w_EM;kappa_J;delta_ellJ", "same Noether/Hilbert source owner or WEP/Newton/clock bound", "WEP;Newton_GM;R10;PPN;clocks"),
        ("RG4112_2_coupling_drift", "delta_kappa;b_alpha;lambda_F2", "calibrated constants allowed, drift/independent coefficients must close or be bounded", "Gdot;alpha_dot;clock spectroscopy;WEP"),
        ("RG4112_3_q_loc", "q_loc^nu", "Ward/local vacuum zero or PPN/R10/clock/orbital map", "PPN preferred-frame;R10;clocks;orbital"),
        ("RG4112_4_GK_stress", "T_GK_mn;T_tau/P_mn", "positive/no-hair/stealth theorem or metric Green-function bound", "PPN gamma,beta;orbital;R10"),
        ("RG4112_5_PiM_boundary", "delta_PiM;Phi_EM_boundary;Q_boundary", "fixed-before-readout Pi_M and no-flux/reference theorem or boundary flux row", "Newton_GM;R10;R11;orbital energy"),
        ("RG4112_6_PPN_total", "Delta_PPN_abs", "no cancellation-only pass; map every component to theorem-zero or bound", "all local GR/PPN tests"),
        ("RG4112_7_Bianchi", "Noether/Bianchi residual closure", "derive parent conservation for retained residual vector before claiming local GR", "consistency gate for all residuals"),
    ]
    return [
        {
            **row_base(),
            "gate_id": gate_id,
            "symbol": symbol,
            "required_result": required,
            "observable_links": links,
            "current_status": "LIVE_ZERO_OR_BOUND_REQUIRED",
            "source_id": "SRC4112_10_3624_residual_vector",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for gate_id, symbol, required, links in residuals
    ]


def decision_rows() -> List[dict]:
    decisions = [
        (
            "DEC4112_0_import",
            "The old 3611-3624 q/J_q/EM chain is promoted into the active 411x spine instead of being rediscovered.",
            "IMPORT_COMPLETE",
            "use 4112 as current-chain bookmark",
        ),
        (
            "DEC4112_1_progress",
            "The project moved from abstract coupling missingness to a minimal local-GR contract with explicit residual vector.",
            "REAL_ADVANCE",
            "do not restart from raw q/Jq unless a source refutes the imported chain",
        ),
        (
            "DEC4112_2_claim_guard",
            "No local-GR/Newton/Maxwell/PPN claim is allowed yet.",
            "CLAIM_BLOCKED_NOT_WORK_BLOCKED",
            "derive Bianchi closure or build first PPN/Newton residual envelope",
        ),
        (
            "DEC4112_3_next",
            "The next current-chain target is Bianchi residual closure or the first executable PPN/Newton residual envelope.",
            "NEXT_TARGET_SELECTED",
            "4113-Y5-R2FR-Bianchi-residual-closure-or-first-PPN-envelope-runner.md",
        ),
    ]
    return [
        {
            **row_base(),
            "decision_id": decision_id,
            "decision": decision,
            "status": status,
            "next_action": next_action,
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for decision_id, decision, status, next_action in decisions
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "next_id": "NEXT4112_0",
            "target_doc": "4113-Y5-R2FR-Bianchi-residual-closure-or-first-PPN-envelope-runner.md",
            "target_script": "scripts/Y5_R2FR_4113_Bianchi_residual_closure_or_first_PPN_envelope_runner.py",
            "objective": "derive parent Noether/Bianchi closure for the explicit MTS residual vector; if that cannot close, build the first executable PPN/Newton no-cancellation residual envelope with nonclaim source rows",
            "success_gate": "either nabla_m[DeltaE_MTS-kappa DeltaT_MTS] closes from parent symmetry, or every residual component is mapped to a concrete PPN/Newton bound interface",
            "reason": "4112 imports the q/Jq/EM route into a minimal local-GR contract; Bianchi/conservation is the least optional consistency gate before testing.",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
    ]


def status_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "status_id": "STATUS4112_0",
            "decision": DECISION,
            "strongest_result": "4112 imports the useful 3611-3624 derivation ladder into the active 411x spine: xi_q is still unsigned, but J_q matter/EM/Poynting/Hodge/screen/source-coupling branches have been compressed into a minimal local-GR contract with calibrated G_eff/alpha_eff and an explicit residual vector.",
            "what_changed": "The route no longer asks MTS to derive numerical G or alpha immediately; it asks MTS to derive EH/Newton/Maxwell form and theorem-zero or bound every extra residual.",
            "still_missing": "parent Bianchi/Noether closure, EH dominance, source mass/worldtube glue, beta/PPN completion, q_loc/GK/PiM residual bounds, and joint EM source-current ownership",
            "claim_state": "no local_GR_Newton_Maxwell_PPN_WEP_R10_R11 claim",
            "next_target": "4113 Bianchi residual closure or first PPN/Newton envelope runner",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
    ]


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4112_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4112_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4112_IMPORTED_DERIVATION_CHAIN": SOURCE_DIR / "P8_Y5_R2FR_4112_IMPORTED_DERIVATION_CHAIN.csv",
        "P8_Y5_R2FR_4112_XI_Q_JQ_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4112_XI_Q_JQ_STATUS.csv",
        "P8_Y5_R2FR_4112_EM_POYNTING_HODGE_SCREEN_SPINE": SOURCE_DIR / "P8_Y5_R2FR_4112_EM_POYNTING_HODGE_SCREEN_SPINE.csv",
        "P8_Y5_R2FR_4112_LOCAL_GR_CALIBRATED_CONTRACT": SOURCE_DIR / "P8_Y5_R2FR_4112_LOCAL_GR_CALIBRATED_CONTRACT.csv",
        "P8_Y5_R2FR_4112_RESIDUAL_VECTOR_NEXT_GATES": SOURCE_DIR / "P8_Y5_R2FR_4112_RESIDUAL_VECTOR_NEXT_GATES.csv",
        "P8_Y5_R2FR_4112_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4112_DECISION_GATE.csv",
        "P8_Y5_R2FR_4112_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4112_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4112_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4112_STATUS.csv",
    }


def markdown_table(rows: List[dict], columns: List[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    imported = imported_chain_rows()
    xi_jq = xi_q_jq_rows()
    em_spine = em_screen_spine_rows()
    contract = local_gr_contract_rows()
    residuals = residual_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    status = status_rows()[0]

    lines = [
        "# 4112 - xi_q positive-Hessian source or Jq first-component bound",
        "",
        "## Verdict",
        "4112 closes the current-chain bookkeeping gap: the useful older `3611-3624` q/J_q/EM/local-GR derivation ladder is now imported into the active `411x` spine.",
        "",
        "The strongest result is not a public claim. It is a cleaner local-GR strategy: calibrated `G_eff` and `alpha_eff` are allowed just as GR uses measured `G`, but every extra MTS residual must be theorem-zeroed or bounded. That is the right boxing stance: win by equation form plus residual discipline, not by pretending constants have been predicted from nothing.",
        "",
        "## Strongest Current Result",
        f"- `{status['decision']}`",
        f"- {status['strongest_result']}",
        f"- {status['what_changed']}",
        "",
        "## Imported Derivation Chain",
        markdown_table(imported, ["import_id", "imported_step", "result", "why_it_matters"]),
        "",
        "## xi_q / J_q State",
        markdown_table(xi_jq, ["row_id", "object", "formula_or_statement", "status", "remaining_gate"]),
        "",
        "## EM / Poynting / Hodge Spine",
        markdown_table(em_spine, ["spine_id", "object", "formula_or_statement", "status"]),
        "",
        "## Minimal Local-GR Contract",
        markdown_table(contract, ["contract_id", "contract_piece", "formula_or_statement", "required_next"]),
        "",
        "## Residuals Still on the Board",
        markdown_table(residuals, ["gate_id", "symbol", "required_result", "observable_links", "current_status"]),
        "",
        "## Decisions",
        markdown_table(decisions, ["decision_id", "decision", "status", "next_action"]),
        "",
        "## Next Target",
        markdown_table(next_target, ["target_doc", "target_script", "objective", "success_gate"]),
        "",
        "## Claim Ceiling",
        "- No local-GR, Newton, Maxwell-source, PPN, WEP, R10, R11, or GitHub/public claim follows from 4112.",
        "- This is a private current-chain spine import and next-target selection.",
        "- The next proof target is Bianchi/Noether consistency for the explicit residual vector.",
        "",
        "## Outputs",
        "- `P8_Y5_R2FR_4112_SOURCE_REGISTER.csv`",
        "- `P8_Y5_R2FR_4112_IMPORTED_DERIVATION_CHAIN.csv`",
        "- `P8_Y5_R2FR_4112_XI_Q_JQ_STATUS.csv`",
        "- `P8_Y5_R2FR_4112_EM_POYNTING_HODGE_SCREEN_SPINE.csv`",
        "- `P8_Y5_R2FR_4112_LOCAL_GR_CALIBRATED_CONTRACT.csv`",
        "- `P8_Y5_R2FR_4112_RESIDUAL_VECTOR_NEXT_GATES.csv`",
        "- `P8_Y5_R2FR_4112_DECISION_GATE.csv`",
        "- `P8_Y5_R2FR_4112_NEXT_TARGET.csv`",
        "- `P8_Y5_R2FR_4112_STATUS.csv`",
        "- `P8_Y5_BRR545_4112_VALIDATION.csv`",
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4112_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4112_IMPORTED_DERIVATION_CHAIN"], imported_chain_rows())
    write_csv(outputs["P8_Y5_R2FR_4112_XI_Q_JQ_STATUS"], xi_q_jq_rows())
    write_csv(outputs["P8_Y5_R2FR_4112_EM_POYNTING_HODGE_SCREEN_SPINE"], em_screen_spine_rows())
    write_csv(outputs["P8_Y5_R2FR_4112_LOCAL_GR_CALIBRATED_CONTRACT"], local_gr_contract_rows())
    write_csv(outputs["P8_Y5_R2FR_4112_RESIDUAL_VECTOR_NEXT_GATES"], residual_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4112_DECISION_GATE"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4112_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4112_STATUS"], status_rows())
    write_doc()
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                **row_base(),
                "check_id": check_id,
                "check": check,
                "passed": bool_string(passed),
                "detail": detail,
                "claim_allowed": bool_string(False),
            }
        )

    missing_sources = [source_id for source_id, (path, _, _) in LOCAL_SOURCES.items() if not path.exists()]
    missing_needles = []
    for source_id, (path, needle, _) in LOCAL_SOURCES.items():
        if path.exists() and needle not in read_text(path):
            missing_needles.append(f"{source_id}:{needle}")
    add("VAL4112_0_sources_exist", "every local source path exists", not missing_sources, ";".join(missing_sources) or "all sources exist")
    add("VAL4112_1_sources_contain_needles", "every local source contains its expected needle", not missing_needles, ";".join(missing_needles) or "all needles found")

    parse_ok = True
    parse_counts = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4112_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    imported_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4112_IMPORTED_DERIVATION_CHAIN"]))
    chain_ok = all(token in imported_text for token in ["3611", "3624", "minimal local-GR contract", "K_theta"])
    add("VAL4112_3_import_chain", "import chain covers xi/Jq through local-GR contract", chain_ok, "chain tokens checked")

    xi_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4112_XI_Q_JQ_STATUS"]))
    xi_ok = all(token in xi_text for token in ["lambda_q=xi_q", "J_q^matter_bulk", "J_q^EM/Poynting", "CONDITIONAL_NO_POLE_ROUTE_RETAINED"])
    add("VAL4112_4_xi_jq", "xi_q/J_q status contains quotient, physical and matter/EM branches", xi_ok, "xi/Jq tokens checked")

    em_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4112_EM_POYNTING_HODGE_SCREEN_SPINE"]))
    em_ok = all(token in em_text for token in ["Delta_Hodge_EM", "K_theta", "h_split=0", "unique F2", "Poynting"])
    add("VAL4112_5_em_spine", "EM/Poynting/Hodge/screen spine imported", em_ok, "EM spine tokens checked")

    contract_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4112_LOCAL_GR_CALIBRATED_CONTRACT"]))
    contract_ok = all(token in contract_text for token in ["G_eff", "alpha_eff", "Einstein-Hilbert", "Newton/Poisson", "Bianchi"])
    add("VAL4112_6_local_gr_contract", "local-GR calibrated contract present", contract_ok, "contract tokens checked")

    residual_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4112_RESIDUAL_VECTOR_NEXT_GATES"]))
    residual_ok = all(token in residual_text for token in ["DeltaE_MTS", "q_loc", "Delta_PPN_abs", "Noether/Bianchi"])
    add("VAL4112_7_residuals", "residual vector next gates include major local-GR blockers", residual_ok, "residual tokens checked")

    decision_rows_local = parse_csv(outputs["P8_Y5_R2FR_4112_DECISION_GATE"])
    next_decision = any(row.get("status") == "NEXT_TARGET_SELECTED" and "4113" in row.get("next_action", "") for row in decision_rows_local)
    add("VAL4112_8_decision", "decision gate selects 4113 Bianchi/PPN target", next_decision, str(decision_rows_local))

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4112_NEXT_TARGET"])
    next_ok = len(next_rows) == 1 and next_rows[0].get("target_doc") == "4113-Y5-R2FR-Bianchi-residual-closure-or-first-PPN-envelope-runner.md"
    add("VAL4112_9_next_target", "next target is 4113 Bianchi residual closure or PPN runner", next_ok, str(next_rows))

    status_rows_local = parse_csv(outputs["P8_Y5_R2FR_4112_STATUS"])
    status_ok = bool(status_rows_local) and status_rows_local[0].get("decision") == DECISION and "no local_GR" in status_rows_local[0].get("claim_state", "")
    add("VAL4112_10_status", "status records current-chain import and no-claim state", status_ok, "status row checked")

    all_rows = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") for row in all_rows)
    add("VAL4112_11_no_claim_flags", "all generated rows remain no-claim", no_claim, f"row_count={len(all_rows)}")

    output_paths = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4112*")) or any(
            FORMALIZATION.rglob("4112-Y5-R2FR*")
        )
    add("VAL4112_12_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4112_13_compile", "generator script compiles", compile_ok, compile_detail)

    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4112_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
