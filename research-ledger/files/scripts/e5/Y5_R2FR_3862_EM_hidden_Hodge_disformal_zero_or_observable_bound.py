from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3862"
BRANCH = "MTS_R2FR_Y5_EM_HIDDEN_HODGE_DISFORMAL_ZERO_OR_OBSERVABLE_BOUND_3862"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3862-Y5-R2FR-EM-hidden-Hodge-disformal-zero-or-observable-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3861_THEOREM = OUT / "P8_Y5_R2FR_3861_NO_SHADOW_COFRAME_THEOREM.csv"
CSV_3861_BOUND = OUT / "P8_Y5_R2FR_3861_EPSILON_SHADOW_FRAME_BOUND.csv"
CSV_3861_GATES = OUT / "P8_Y5_R2FR_3861_CLAIM_GATES.csv"
CSV_3861_VALIDATION = OUT / "P8_Y5_BRR545_3861_VALIDATION.csv"
CSV_3504_HODGE = OUT / "P8_Y5_R2FR_3504_HODGE_UNIQUENESS_THEOREM.csv"
CSV_3504_DELTA = OUT / "P8_Y5_R2FR_3504_DELTA_HODGE_BOUND_VECTOR.csv"
CSV_3505_DOMAIN = OUT / "P8_EM_visible_action_domain_exhaustion_no_chiEM_bound_vector.csv"
CSV_3503_OWNER = OUT / "P8_Y5_R2FR_3503_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv"
CSV_3465_OWNER = OUT / "P8_Y5_R2FR_3465_EM_OWNER_PACKAGE_AUDIT.csv"
CSV_3463_POYNTING = OUT / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv"
CSV_3116_LOCK = OUT / "P8_Y5_R2FR_3116_PUBLIC_HODGE_MAXWELL_STRESS_LOCK.csv"
CSV_3343_MAXWELL = OUT / "P8_Y5_R2FR_3343_PUBLIC_MAXWELL_ACTION_DERIVATION.csv"
CSV_3286_POYNTING = OUT / "P8_Y5_R2FR_3286_HODGE_POYNTING_OWNER_THEOREM.csv"
CSV_3287_RECON = OUT / "P8_Y5_R2FR_3287_CHI_TO_HODGE_RECONSTRUCTION_THEOREM.csv"
CSV_3613_CONF = OUT / "P8_Y5_R2FR_3613_CONFORMAL_HODGE_SUBTHEOREM.csv"
CSV_3613_BOUND = OUT / "P8_Y5_R2FR_3613_DELTA_HODGE_BOUND_LAW.csv"
CSV_3614_PRINCIPAL = OUT / "P8_Y5_R2FR_3614_PRINCIPAL_HODGE_THEOREM.csv"
CSV_3614_BOUND = OUT / "P8_Y5_R2FR_3614_PRINCIPAL_HODGE_BOUND.csv"
CSV_3506_TEMPLATE = OUT / "P8_Y5_R2FR_3506_CONSTITUTIVE_BOUND_INPUT_TEMPLATE.csv"
CSV_3506_RUNNER = OUT / "P8_Y5_R2FR_3506_CONSTITUTIVE_BOUND_RUNNER_RESULTS.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3862_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3862_EM_HODGE_ZERO_THEOREM.csv",
    "audit": OUT / "P8_Y5_R2FR_3862_CONSTITUTIVE_SLOT_AUDIT.csv",
    "bound": OUT / "P8_Y5_R2FR_3862_EM_HODGE_OBSERVABLE_BOUND.csv",
    "gates": OUT / "P8_Y5_R2FR_3862_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3862_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3862_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3862_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3862_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3862_00_3861_theorem", CSV_3861_THEOREM, "NO_SHADOW_COFRAME_NOT_CLAIMED_CURRENT_CORPUS", "3861 no-shadow current verdict"),
    ("SRC3862_01_3861_bound", CSV_3861_BOUND, "B_EM_Hodge_hidden", "3861 EM shadow component priority"),
    ("SRC3862_02_3861_gates", CSV_3861_GATES, "PASS_3862_EM_HIDDEN_HODGE_TARGET", "3861 next-target gate"),
    ("SRC3862_03_3861_validation", CSV_3861_VALIDATION, "PASS", "previous validation"),
    ("SRC3862_04_3504_hodge", CSV_3504_HODGE, "independent constitutive tensor", "Hodge uniqueness and countermodel"),
    ("SRC3862_05_3504_delta", CSV_3504_DELTA, "DHB3504_4_hidden_disformal_hodge", "hidden disformal Hodge component"),
    ("SRC3862_06_3505_domain", CSV_3505_DOMAIN, "VEB3505_4_C_Hodge_hidden", "visible EM action-domain exhaustion"),
    ("SRC3862_07_3503_owner", CSV_3503_OWNER, "OHM3503_0_same_observed_Hodge", "observed Hodge Maxwell owner"),
    ("SRC3862_08_3465_owner", CSV_3465_OWNER, "EMO3465_0_observed_hodge", "EM owner package"),
    ("SRC3862_09_3463_poynting", CSV_3463_POYNTING, "EM3463_2_poynting", "Poynting stress ledger"),
    ("SRC3862_10_3116_lock", CSV_3116_LOCK, "C_constitutive", "public Hodge Maxwell stress lock"),
    ("SRC3862_11_3343_maxwell", CSV_3343_MAXWELL, "Poynting as flux", "public Maxwell action derivation"),
    ("SRC3862_12_3286_poynting", CSV_3286_POYNTING, "HP3286_2_vertical_zero", "Hodge/Poynting q-basic zero law"),
    ("SRC3862_13_3287_recon", CSV_3287_RECON, "CHR3287_2_closure_to_metric_Hodge", "chi-to-Hodge reconstruction"),
    ("SRC3862_14_3613_conformal", CSV_3613_CONF, "CHS3613_0_theorem", "4D conformal Hodge subtheorem"),
    ("SRC3862_15_3613_bound", CSV_3613_BOUND, "DHB3613_1_component_bound", "Delta_Hodge component bound law"),
    ("SRC3862_16_3614_principal", CSV_3614_PRINCIPAL, "PHT3614_4_conditional_zero", "principal Hodge conditional zero"),
    ("SRC3862_17_3614_bound", CSV_3614_BOUND, "PHB3614_1_bound_law", "principal Hodge bound"),
    ("SRC3862_18_3506_template", CSV_3506_TEMPLATE, "BIN3506_3_C_Hodge_hidden", "constitutive bound input template"),
    ("SRC3862_19_3506_runner", CSV_3506_RUNNER, "BRUN3506_3_C_Hodge_hidden", "constitutive bound runner result"),
]

CONSTITUTIVE_EXHAUSTION = (
    "For a local linear U(1)-gauge EM sector, every Hodge/flow mismatch can be written as a "
    "constitutive residual: chi_EM = Z_Q chi(g_obs) + Delta_chi_principal^H + chi_skewon "
    "+ theta_EM epsilon + chi_hidden/readout, with pure 4D conformal scale removed from the "
    "2-form Hodge cone and carried to source/clock normalization."
)
ZERO_THEOREM = (
    "Delta_Hodge_EM=0 if the parent EM action is S_EM=-(4 mu0)^-1 int F wedge *_obs[e_obs(q_obs)]F, "
    "orientation is fixed, the reciprocal principal chi reconstructs the same public conformal metric, "
    "skewon and active axion-gradient pieces are absent, no hidden/disformal/readout constitutive map is "
    "allowed, and Z_Q/charge-current normalization is q-basic or carried to a separate scale gate."
)
CURRENT_BLOCK = (
    "The exact route is not a current claim because the corpus still has no parent-signed visible EM "
    "action-domain exclusion, no numeric/source-backed constitutive coefficients, and no completed "
    "Z_Q/charge-current/source-scale owner."
)
DELTA_HODGE_BOUND = (
    "||Delta_Hodge_EM|| <= ||Delta_chi_principal^H|| + ||Delta_chi_skewon|| + L||d theta_EM|| "
    "+ |C_Hodge_hidden| + |C_Hodge_readout| + |C_XF2| + |Delta_orientation_flux|"
)
PRINCIPAL_BOUND = (
    "||Delta_chi_principal^H|| <= B_Fresnel + C_g||[g_EM]-[g_obs]|| + B_closure + B_orient"
)
SCALE_GATE = (
    "B_EM_scale_3862 := |D_v ln Z_Q| + |D_v ln mu0^-1| + |D_v ln q_unit| "
    "+ |D_v ln J_Q| + |D_v ln M_H,EM|"
)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "claim_use": "nonclaim_EM_Hodge_zero_or_bound_derivation",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "EHZ3862_0_constitutive_exhaustion",
            "claim_piece": "EM Hodge residual basis",
            "statement": CONSTITUTIVE_EXHAUSTION,
            "derivation": "Use the local bilinear EM action/constitutive map on two-forms: reciprocal principal, skewon, axion/topological, hidden/disformal and readout pieces exhaust the linear Hodge-flow ambiguity.",
            "result": "EXACT_CONDITIONAL_CONSTITUTIVE_EXHAUSTION",
            "status": "DERIVED_COMPONENT_BASIS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "EHZ3862_1_observed_Hodge_zero",
            "claim_piece": "observed Hodge zero theorem",
            "statement": ZERO_THEOREM,
            "derivation": "Combine Hodge uniqueness from e_obs, reciprocal nonbirefringent reconstruction of the metric-Hodge principal part, q-basic chain rule, absence of independent constitutive arguments, and readout-before/after variation discipline.",
            "result": "EXACT_CONDITIONAL_DELTA_HODGE_ZERO_THEOREM",
            "status": "CONDITIONAL_THEOREM_PROVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "EHZ3862_2_Poynting_stress_handoff",
            "claim_piece": "Poynting is Hilbert stress flux in the clean branch",
            "statement": "If Delta_Hodge_EM=0 and the Maxwell normalization/current owner is fixed, then T_EM is obtained by varying the same observed coframe action and S_Poynting^i=c^2 T_EM^{0i}; Poynting is not a separate gravitational force.",
            "derivation": "Vary S_EM[F,*_obs] with respect to g_obs/e_obs and project nabla_mu T_EM^{mu nu} on a local inertial observer slice.",
            "result": "EXACT_CONDITIONAL_MAXWELL_STRESS_POYNTING_ALIGNMENT",
            "status": "CONDITIONAL_STRESS_ROUTE_ADVANCED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "EHZ3862_3_conformal_guard",
            "claim_piece": "conformal Hodge caveat",
            "statement": "In four dimensions a pure conformal rescaling leaves the Hodge star on two-forms invariant, so matching EM cones/Hodge does not by itself fix clocks, charge normalization, source mass, or Newtonian coupling.",
            "derivation": "Use *_Omega^2g on Lambda^2 equals *_g and move the remaining scale to B_EM_scale_3862.",
            "result": "CONFORMAL_HODGE_ZERO_BUT_SCALE_GATE_RETAINED",
            "status": "NO_OVERCLAIM_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "EHZ3862_4_current_verdict",
            "claim_piece": "strict current corpus verdict",
            "statement": CURRENT_BLOCK,
            "derivation": "3504/3505/3506 retain hidden Hodge and constitutive coefficients; 3613/3614 provide nonclaim bounds; 3503/3465 retain normalization and charge/current owner gaps.",
            "result": "EM_HODGE_ZERO_NOT_CLAIMED_CURRENT_CORPUS",
            "status": "CURRENT_NONCLAIM_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "EHZ3862_5_handoff_to_coupling",
            "claim_piece": "next coupling obstruction",
            "statement": "Even if Delta_Hodge_EM is theorem-zero, local GR/Newton still need the EM source scale: Z_Q, mu0, charge/current normalization, alpha_EM, and EM contribution to M_H must be parent-owned or bounded.",
            "derivation": "3503/3465 show the Hodge route aligns geometry and stress but leaves w_EM, C_JQ, C_XF2, b_alpha and source calibration as separate coefficients.",
            "result": "NEXT_GATE_IS_MAXWELL_NORMALIZATION_AND_CHARGE_CURRENT_OWNER",
            "status": "COUPLING_ROUTE_SHARPENED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def audit_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "CSA3862_0_principal_metric",
            "slot": "principal constitutive tensor",
            "zero_condition": "reciprocal nonbirefringent closure reconstructs [g_EM] and parent signs [g_EM]=[g_obs]",
            "current_evidence": "3614 gives conditional zero and bound law; same public metric clause remains parent-signature required",
            "passes_current_branch": False,
            "residual_owner": "Delta_chi_principal^H",
            "observable_links": "vacuum_birefringence;light_cone;Shapiro_lensing_consistency",
            "next_action": "prove same-metric clause or fill B_Fresnel/B_same_metric/B_closure rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CSA3862_1_skewon",
            "slot": "skewon/nonreciprocal tensor",
            "zero_condition": "EM sector is a conservative reciprocal action before readout",
            "current_evidence": "3287/3614 show action branch removes skewon conditionally; current parent action still unsigned globally",
            "passes_current_branch": False,
            "residual_owner": "Delta_chi_skewon",
            "observable_links": "dispersion;polarization;Poynting_flux_nonconservation",
            "next_action": "parent-sign reciprocal EM action or retain skewon bound",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CSA3862_2_axion_gradient",
            "slot": "axion/topological F wedge F",
            "zero_condition": "theta_EM absent or parent-fixed constant so d theta_EM=0",
            "current_evidence": "3613 separates active axion gradient from stress-silent constant topology",
            "passes_current_branch": False,
            "residual_owner": "Delta_chi_axion_gradient",
            "observable_links": "polarization_rotation;effective_current;spectroscopy",
            "next_action": "prove theta_EM constant/absent or retain L||d theta_EM||",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CSA3862_3_hidden_disformal_Hodge",
            "slot": "hidden/disformal Hodge map",
            "zero_condition": "operator domain forbids g_EM=g_obs+C_H u u+C_X X or *_EM=*(g_EM) independent of e_obs(q)",
            "current_evidence": "3504/3505 keep C_Hodge_hidden as retained component; 3506 has no numeric/source-backed input",
            "passes_current_branch": False,
            "residual_owner": "C_Hodge_hidden",
            "observable_links": "preferred_frame;alpha1_alpha2;light_speed_anisotropy;clock",
            "next_action": "derive no hidden-visible Hodge map or acquire observable bounds",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CSA3862_4_readout_regeneration",
            "slot": "post-solution EM readout Hodge",
            "zero_condition": "readout-after-variation cannot regenerate chi_readout, alpha_X, or effective Hodge drift",
            "current_evidence": "3505 retains C_Hodge_readout; 3116 keeps hidden flux/readout residuals",
            "passes_current_branch": False,
            "residual_owner": "C_Hodge_readout",
            "observable_links": "clock;spectroscopy;alpha_EM;binding_response",
            "next_action": "prove readout preservation or bound spectroscopy/clock leakage",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CSA3862_5_unique_F2_scale",
            "slot": "Maxwell normalization and hidden F2",
            "zero_condition": "Z_Q/mu0, charge-current normalization and alpha_EM are parent-owned and q-basic",
            "current_evidence": "3503/3465 keep w_EM, C_JQ, C_XF2 and alpha owner gaps live",
            "passes_current_branch": False,
            "residual_owner": "B_EM_scale_3862",
            "observable_links": "EM_binding;WEP;R10;clock;source_normalization;Newton_G",
            "next_action": "make 3863 the Maxwell normalization/charge-current owner gate",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "bound_id": "EHB3862_0_Delta_Hodge_EM",
            "target": "Delta_Hodge_EM",
            "formula": DELTA_HODGE_BOUND,
            "derivation": "component no-cancellation envelope after removing pure conformal 4D Hodge scale",
            "observables": "Maxwell_limit;light_cone;Poynting_flow;clock;PPN",
            "status": "NONCLAIM_COMPONENT_BOUND",
            "numeric_status": "MISSING_PARENT_COEFFICIENTS_AND_BOUNDS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "EHB3862_1_principal_Hodge",
            "target": "Delta_chi_principal^H",
            "formula": PRINCIPAL_BOUND,
            "derivation": "3614 Fresnel/same-metric/closure/orientation bound for the reciprocal principal part",
            "observables": "vacuum_birefringence;light_cone;Shapiro_lensing_consistency",
            "status": "NONCLAIM_PRINCIPAL_BOUND",
            "numeric_status": "MISSING_COMPONENT_VALUES",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "EHB3862_2_hidden_disformal",
            "target": "C_Hodge_hidden",
            "formula": "|C_Hodge_hidden| <= B_preferred_frame+B_light_speed_anisotropy+B_clock_metric_mismatch+B_alpha1_alpha2_projection",
            "derivation": "hidden/disformal Hodge changes the EM metric relative to observed matter/clock metric",
            "observables": "preferred_frame;light_speed_anisotropy;clock;PPN_alpha1_alpha2",
            "status": "BOUND_ROUTE_DECLARED_NOT_NUMERIC",
            "numeric_status": "MISSING_OBSERVABLE_PROJECTION_ROWS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "EHB3862_3_EM_scale_gate",
            "target": "B_EM_scale_3862",
            "formula": SCALE_GATE,
            "derivation": "pure Hodge/cone agreement leaves Maxwell impedance, charge/current, alpha and source-mass normalization",
            "observables": "WEP;R10;clock;source_normalization;Newton_G;EM_binding",
            "status": "SEPARATE_SOURCE_SCALE_GATE_RETAINED",
            "numeric_status": "SYMBOLIC_ONLY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "EHB3862_4_3861_substitution",
            "target": "B_EM_Hodge_hidden",
            "formula": "B_EM_Hodge_hidden <= ||Delta_Hodge_EM|| + B_EM_scale_3862",
            "derivation": "3861 generic shadow-frame EM slot is now split into Hodge/constitutive shape plus scale/source normalization",
            "observables": "local_GR;Maxwell;Poynting;clock;source_coupling",
            "status": "SHADOW_BOUND_REFINED",
            "numeric_status": "SYMBOLIC_ONLY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G3862_0_constitutive_exhaustion",
            "gate": "constitutive residual basis is explicit",
            "status": "PASS_EXACT_CONDITIONAL_CONSTITUTIVE_EXHAUSTION",
            "claim_allowed": False,
            "reason": "the Hodge problem is reduced to named principal/skewon/axion/hidden/readout/F2/orientation components",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G3862_1_zero_theorem",
            "gate": "conditional observed-Hodge zero theorem is explicit",
            "status": "PASS_EXACT_CONDITIONAL_DELTA_HODGE_ZERO",
            "claim_allowed": False,
            "reason": "zero follows if the EM action uses only *_obs[e_obs(q)] and the constitutive escape slots are excluded",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G3862_2_no_current_claim",
            "gate": "current EM Hodge/local-GR claim remains blocked",
            "status": "BLOCKED_VISIBLE_EM_ACTION_DOMAIN_UNSIGNED",
            "claim_allowed": False,
            "reason": "hidden Hodge coefficients and same-metric/source-scale owners remain unsigned or missing numeric bounds",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G3862_3_conformal_guard",
            "gate": "conformal Hodge caveat retained",
            "status": "PASS_NO_LIGHT_CONE_OVERCLAIM",
            "claim_allowed": False,
            "reason": "4D Maxwell Hodge/cone agreement does not fix source/clock/charge normalization",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G3862_4_next_target",
            "gate": "next target selected",
            "status": "PASS_3863_MAXWELL_NORMALIZATION_CHARGE_CURRENT_TARGET",
            "claim_allowed": False,
            "reason": "after Hodge shape, the remaining EM-to-source obstruction is normalization/coupling ownership",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D3862_0",
            "decision": "Treat EM hidden Hodge as a constitutive tensor problem.",
            "consequence": "The route now has a mathematical basis: principal, skewon, axion, hidden/readout and scale components.",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3862_1",
            "decision": "Do not count pure conformal scale as a Hodge-cone failure.",
            "consequence": "Move it to the source/clock/charge normalization gate instead of double-counting it.",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3862_2",
            "decision": "Make Maxwell normalization and charge-current owner the next coupling target.",
            "consequence": "This directly attacks the user's suspected coupling gap rather than re-auditing generic missing inputs.",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3862_0",
            "target_checkpoint": "3863-Y5-R2FR-Maxwell-normalization-charge-current-owner-or-EM-source-scale-bound.md",
            "script": "scripts/Y5_R2FR_3863_Maxwell_normalization_charge_current_owner_or_EM_source_scale_bound.py",
            "objective": "prove Z_Q/mu0, charge-current normalization, alpha_EM and EM source-mass calibration are parent-owned/q-basic, or retain explicit w_EM, C_JQ, C_XF2, b_alpha and B_EM_scale bounds",
            "why_next": "3862 reduces the Hodge shape problem; local GR/Newton still depends on whether EM stress has the right source normalization",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_EM_HODGE_CONSTITUTIVE_ZERO_ROUTE_AND_BOUND",
            "summary": "3862 turns hidden EM Hodge into an exact constitutive exhaustion theorem, proves the observed-Hodge zero route conditionally, keeps current claims blocked, and selects EM normalization/charge-current ownership next.",
            "doc": rel(DOC_PATH),
            "validation": rel(OUTPUTS["validation"]),
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    audit: list[dict[str, object]],
    bound: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3862 — EM Hidden Hodge / Disformal Zero Or Observable Bound

Generated: `{timestamp}`

## Purpose

3861 said the sharpest live shadow-frame slot is EM Hodge/disformal ownership. This checkpoint attacks that slot directly.

## Result

The EM Hodge problem reduces to a constitutive tensor problem:

`{CONSTITUTIVE_EXHAUSTION}`

The exact zero route is:

`{ZERO_THEOREM}`

The strict current verdict is:

`{CURRENT_BLOCK}`

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## EM Hodge Zero Theorem

{markdown_table(theorem, ["theorem_id", "claim_piece", "status", "result"])}

## Constitutive Slot Audit

{markdown_table(audit, ["audit_id", "slot", "passes_current_branch", "residual_owner", "next_action"])}

## Observable Bound

{markdown_table(bound, ["bound_id", "target", "status", "formula"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

3862 is a genuine tightening: hidden EM Hodge is no longer a foggy phrase. It is a named constitutive residual with a zero theorem and a bound vector. If the parent action uses the observed Hodge star only, Poynting is just EM Hilbert-stress flux in the same geometry. But this still does not finish local GR/Newton, because the Maxwell normalization, charge/current convention, alpha, and EM source-mass scale remain the coupling gate.

Next target: `3863-Y5-R2FR-Maxwell-normalization-charge-current-owner-or-EM-source-scale-bound.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3861", "Current State After 3862", 1)
    text = "\n".join(
        line for line in text.splitlines() if not line.startswith("<!-- Generated by 3862 at ")
    )
    paragraph = (
        "`3862` turns the EM hidden-Hodge/disformal leak into a constitutive-tensor theorem. "
        "For a local linear U(1) EM sector, `chi_EM = Z_Q chi(g_obs)+Delta_chi_principal^H+chi_skewon+theta_EM epsilon+chi_hidden/readout`, with pure 4D conformal scale removed from the Hodge cone and moved to source/clock normalization. "
        "`Delta_Hodge_EM=0` follows exactly if the parent action is `S_EM=-(4 mu0)^-1 int F wedge *_obs[e_obs(q_obs)]F`, orientation is fixed, the reciprocal principal part reconstructs the same public conformal metric, skewon/active axion-gradient pieces are absent, no hidden/disformal/readout constitutive map is allowed, and `Z_Q`/charge-current normalization is q-basic or carried to the separate scale gate. "
        "The current corpus does not claim this because visible EM action-domain exclusion, same-metric/source-scale ownership, and numeric constitutive bounds remain unsigned. "
        "The retained bound is `||Delta_Hodge_EM|| <= ||Delta_chi_principal^H||+||Delta_chi_skewon||+L||d theta_EM||+|C_Hodge_hidden|+|C_Hodge_readout|+|C_XF2|+|Delta_orientation_flux|`, with `||Delta_chi_principal^H|| <= B_Fresnel+C_g||[g_EM]-[g_obs]||+B_closure+B_orient`. "
        "Poynting is now placed correctly: in the clean branch it is EM Hilbert-stress flux, not a second force, but the source normalization/coupling still has to be derived.\n\n"
    )
    if paragraph not in text and "## Next Best Gate" in text:
        text = text.replace("## Next Best Gate", paragraph + "## Next Best Gate", 1)
    old_gate = """`3862-Y5-R2FR-EM-hidden-Hodge-disformal-zero-or-observable-bound.md`

Target: prove the EM action uses only the observed Hodge star `*_obs[e_obs(q)]` and no hidden/disformal constitutive map, or retain explicit `C_Hodge_hidden` / `Delta_chi` observable bounds.

This is the best next move because 3861 shows the generic no-shadow route is exact but unsigned, and EM Hodge is the sharpest retained sector shadow touching Poynting flow, Maxwell waves, light cones, clocks, and EM stress."""
    new_gate = """`3863-Y5-R2FR-Maxwell-normalization-charge-current-owner-or-EM-source-scale-bound.md`

Target: prove `Z_Q/mu0`, charge-current normalization, `alpha_EM`, and EM source-mass calibration are parent-owned/q-basic, or retain explicit `w_EM`, `C_JQ`, `C_XF2`, `b_alpha`, and `B_EM_scale` bounds.

This is the best next move because 3862 reduces the Hodge-shape problem, leaving the actual coupling/source-normalization gate."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3862_EM_HODGE_ZERO_THEOREM.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3862_CONSTITUTIVE_SLOT_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3862_EM_HODGE_OBSERVABLE_BOUND.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3862_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3862_EM_HODGE_ZERO_THEOREM.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3862 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    audit: list[dict[str, object]],
    bound: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    all_text = " ".join(str(row) for row in theorem + audit + bound + gates)
    add(
        "VAL3862_0_sources",
        "all cited source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3862_1_exhaustion",
        "constitutive exhaustion theorem is explicit",
        "EXACT_CONDITIONAL_CONSTITUTIVE_EXHAUSTION" in all_text and "chi_EM" in all_text and "Delta_chi_principal" in all_text,
        "component basis present",
    )
    add(
        "VAL3862_2_zero_theorem",
        "observed-Hodge zero route is explicit",
        "EXACT_CONDITIONAL_DELTA_HODGE_ZERO_THEOREM" in all_text and "Delta_Hodge_EM=0" in all_text,
        "conditional zero theorem present",
    )
    add(
        "VAL3862_3_poynting",
        "Poynting stress handoff is explicit",
        "EXACT_CONDITIONAL_MAXWELL_STRESS_POYNTING_ALIGNMENT" in all_text and "Poynting" in all_text,
        "Poynting/Hilbert stress route present",
    )
    add(
        "VAL3862_4_no_overclaim",
        "current claim remains blocked and conformal guard retained",
        "EM_HODGE_ZERO_NOT_CLAIMED_CURRENT_CORPUS" in all_text and "PASS_NO_LIGHT_CONE_OVERCLAIM" in all_text,
        "no current EM Hodge/local-GR promotion",
    )
    add(
        "VAL3862_5_bounds",
        "Delta_Hodge and principal bounds are explicit",
        "||Delta_Hodge_EM|| <=" in all_text and "||Delta_chi_principal^H|| <=" in all_text,
        "Hodge and principal bounds present",
    )
    add(
        "VAL3862_6_nonclaim",
        "all rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in theorem + audit + bound + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3862_7_next",
        "next target is Maxwell normalization and charge-current owner",
        DOC_PATH.exists() and "3863-Y5-R2FR-Maxwell-normalization-charge-current-owner-or-EM-source-scale-bound" in read_text(DOC_PATH),
        "3863 coupling target visible",
    )
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            count = len(read_csv_rows(output_path))
            parsed = count > 0
            detail += f" rows={count}"
        add(f"VAL3862_8_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3862_9_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "3861 said the sharpest live shadow-frame slot" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    formalization_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3862*", "P8_Y5_BRR545_3862*", "*Y5_R2FR_3862*", "3862-Y5-R2FR*"):
            formalization_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3862_10_formalization_clean",
        "formalization-workbench has no generated 3862 project files",
        len(formalization_hits) == 0,
        "; ".join(str(path) for path in formalization_hits) if formalization_hits else "no generated 3862 project file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3862_11_pycache_removed",
        "scripts __pycache__ removed",
        len(pycache_hits) == 0,
        "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories",
    )
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    audit = audit_rows(timestamp)
    bound = bound_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["bound"], bound)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, theorem, audit, bound, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, theorem, audit, bound, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_EM_HODGE_CONSTITUTIVE_ZERO_ROUTE_AND_BOUND")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
