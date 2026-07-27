from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "767-Y5-R10-parent-matter-functor-no-alpha-vertex-or-WEP-closure.md"
NEXT_TARGET = "768-Y5-R10-local-GR-EH-or-R11-reentry-after-alpha-WEP-quarantine.md"
STATUS = "Y5_R10_767_parent_matter_functor_reaudit_confirms_WEP_closure_quarantine_after_alpha_pressure"
CLAIM_CEILING = "parent_matter_functor_reaudit_and_WEP_closure_quarantine_only_no_WEP_Newton_PPN_EH_or_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

MATTER_FUNCTOR_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_767_PARENT_MATTER_FUNCTOR_INPUT_CANDIDATE.csv"
NO_ALPHA_VERTEX_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_767_NO_ALPHA_VERTEX_INPUT_CANDIDATE.csv"
SELECTOR_WARD_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_767_SELECTOR_WARD_INPUT_CANDIDATE.csv"
BETA_SOURCE_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_767_BETA_SOURCE_ALPHA_INPUT_CANDIDATE.csv"
LOCAL_GR_REENTRY_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_767_LOCAL_GR_REENTRY_INPUT_CANDIDATE.csv"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_767_SOURCE_REGISTER.csv"
FUNCTOR_REAUDIT_PATH = RESIDUALS / "P8_Y5_R10_767_PARENT_MATTER_FUNCTOR_REAUDIT.csv"
WEP_QUARANTINE_PATH = RESIDUALS / "P8_Y5_R10_767_WEP_CLOSURE_QUARANTINE.csv"
ALPHA_PRESSURE_IMPORT_PATH = RESIDUALS / "P8_Y5_R10_767_ALPHA_WEP_PRESSURE_IMPORT.csv"
LOCAL_GR_BRIDGE_PATH = RESIDUALS / "P8_Y5_R10_767_LOCAL_GR_BRIDGE.csv"
SOURCE_FILL_PATH = RESIDUALS / "P8_Y5_R10_767_SOURCE_FILL_SCHEMA.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_767_DECISION_MATRIX.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_767_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_767_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_767_VALIDATION.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "766_doc": {
        "path": POST_CHECKPOINT / "766-Y5-R10-finite-alpha-source-fill-clock-first-or-parent-action-source-hunt.md",
        "needles": [
            "Current result: **no parent-action source was found that reactivates alpha-zero",
            "767-Y5-R10-parent-matter-functor-no-alpha-vertex-or-WEP-closure.md",
        ],
        "role": "immediate WEP/no-alpha-vertex handoff",
    },
    "766_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_766_VALIDATION.csv",
        "needles": ["V766_16_validation_rows_ready", "V766_15_formalization_workbench_untouched"],
        "role": "prior validation guard",
    },
    "653_doc": {
        "path": POST_CHECKPOINT / "653-Y5-R10-parent-matter-functor-signature-or-WEP-closure-demotion.md",
        "needles": ["The exact parent signature needed for WEP safety is known", "demoted to an explicit closure axiom"],
        "role": "existing parent matter functor demotion",
    },
    "653_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_653_VALIDATION.csv",
        "needles": ["V653_11_summary_demotes_closure", "V653_2_signature_unsigned"],
        "role": "prior WEP demotion validation",
    },
    "653_signature": {
        "path": RESIDUALS / "P8_Y5_R10_653_PARENT_SIGNATURE_REQUIREMENTS.csv",
        "needles": ["PMF653_0_explicit_parent_matter_functor", "PMF653_3_no_alpha_mass_vertex"],
        "role": "parent matter functor signature requirements",
    },
    "653_closure": {
        "path": RESIDUALS / "P8_Y5_R10_653_WEP_CLOSURE_DEMOTION.csv",
        "needles": ["WCL653_0_one_observed_geometry", "WCL653_2_no_chi_dependent_constants"],
        "role": "explicit WEP closure rows",
    },
    "652_beta_target": {
        "path": RESIDUALS / "P8_Y5_R10_652_SOURCE_NORMALIZATION_TARGET.csv",
        "needles": ["BST652_2_robust_target", "2.887280314062e-05"],
        "role": "WEP beta-source numeric fallback target",
    },
    "654_doc": {
        "path": POST_CHECKPOINT / "654-Y5-R10-local-GR-reduction-spine-under-explicit-WEP-closure.md",
        "needles": ["WEP/common matter geometry is now carried as explicit closure", "EH operator selection"],
        "role": "local-GR spine under WEP closure",
    },
    "654_spine": {
        "path": RESIDUALS / "P8_Y5_R10_654_LOCAL_GR_SPINE.csv",
        "needles": ["LGS654_1_EH_operator_selection", "LGS654_7_weak_field_PPN_readout"],
        "role": "local-GR spine rungs",
    },
    "655_doc": {
        "path": POST_CHECKPOINT / "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md",
        "needles": ["EH-only theorem route remains unsigned", "R11 route exists only as a template"],
        "role": "EH/R11 gate current state",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def text_contains(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return bool(text) and all(needle in text for needle in needles)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def under_post(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            count += 1
    return count


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(spec["path"]),
            "exists": bool_string(Path(spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(spec["path"]), spec["needles"])),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, spec in SOURCES.items()
    ]


def functor_reaudit_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "reaudit_id": "PMR767_0_explicit_parent_matter_functor",
            "required_signature": "S_parent contains S_matter=sum_A S_A[Psi_A, ehat, omega[ehat], theta_A].",
            "current_evidence": "653 lists the exact signature, but 766 adds no parent-action source that derives it.",
            "verdict_after_766": "still_unsigned",
            "risk_if_used": "WEP/common matter frame is smuggled into GR reduction as theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "reaudit_id": "PMR767_1_species_blind_geometry_map",
            "required_signature": "ehat_A(Phi)=ehat(Phi) for every species A.",
            "current_evidence": "representative invariance can control some leaks but does not force a common quotient-invariant F_A(C_D).",
            "verdict_after_766": "still_unsigned",
            "risk_if_used": "species coframes or class metric splits reintroduce WEP violation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "reaudit_id": "PMR767_2_theta_internal_only",
            "required_signature": "partial_chi_X theta_A=0 and species labels are internal representation data only.",
            "current_evidence": "finite-alpha branch shows alpha/constants remain dangerous product-bound channels, not zero theorems.",
            "verdict_after_766": "still_unsigned",
            "risk_if_used": "direct alpha/mass clock/WEP channels are hidden rather than derived away",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "reaudit_id": "PMR767_3_no_alpha_mass_vertex",
            "required_signature": "delta S_matter/dchi_X|ehat,theta_A=0 and no f_A(chi_X)F^2 or m_A(chi_X) vertex survives.",
            "current_evidence": "765/766 retain lambda_A F_Q^2 and finite alpha product bounds; no no-alpha-vertex source was supplied.",
            "verdict_after_766": "hard_blocker_still_unsigned",
            "risk_if_used": "Damour-Donoghue composition charges remain physical and MICROSCOPE pressure applies",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "reaudit_id": "PMR767_4_selector_Ward_identity",
            "required_signature": "nabla_mu(T_matter+T_MTS+T_selector)^mu_nu=0 after selecting ehat.",
            "current_evidence": "selector stress accounting is closure-required in 653/654, not a parent Ward theorem.",
            "verdict_after_766": "open",
            "risk_if_used": "one-geometry selector can hide an unconserved fifth force",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "reaudit_id": "PMR767_5_domain_selection_predata",
            "required_signature": "D_parent(local lab/source domains) is fixed before clock/WEP/R10 fitting.",
            "current_evidence": "650 forbids arena-specific screens; 766 keeps same-screen policy active.",
            "verdict_after_766": "not_parent_derived",
            "risk_if_used": "clock/WEP/local/cosmology split becomes post-hoc arena switching",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def WEP_quarantine_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "closure_id": "WQ767_0_one_observed_geometry",
            "closure_statement": "All matter, photons, clocks, rulers, and standards couple to one observed geometry ehat.",
            "status_after_766": "explicit_closure_not_theorem",
            "allowed_private_use": "organize one-frame local-GR branch",
            "forbidden_use": "claim WEP/source-frame derivation or use as EH/PPN proof",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "closure_id": "WQ767_1_species_blind_geometry_map",
            "closure_statement": "The geometry map from MTS variables to ehat is species-blind.",
            "status_after_766": "explicit_closure_not_theorem",
            "allowed_private_use": "remove direct species coframe split inside the closure branch",
            "forbidden_use": "erase possible quotient-invariant species functions without parent proof",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "closure_id": "WQ767_2_no_chi_dependent_constants",
            "closure_statement": "Local matter constants and alpha_EM do not directly depend on chi_X/C_D.",
            "status_after_766": "explicit_closure_not_theorem",
            "allowed_private_use": "box direct alpha/mass WEP composition channel",
            "forbidden_use": "ignore clock product bounds or lambda_A F_Q^2 counterexample as if alpha zero were derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "closure_id": "WQ767_3_selector_stress_accounting",
            "closure_statement": "Any selector enforcing observed geometry is included in total stress conservation.",
            "status_after_766": "explicit_closure_required_before_use",
            "allowed_private_use": "carry selector as stress/Ward debt in local-GR spine",
            "forbidden_use": "declare selector/domain/projector force harmless without proof or residual row",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "closure_id": "WQ767_4_beta_source_fallback",
            "closure_statement": "If direct alpha composition source survives, beta_source_alpha must satisfy the robust 652 target.",
            "status_after_766": "numeric_fallback_target_retained",
            "allowed_private_use": "stress-test finite-alpha WEP survival",
            "forbidden_use": "use beta target as a derived suppression",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def alpha_pressure_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "pressure_id": "AWP767_0_clock_product_bound",
            "imported_fact": "Yb+ E3/E2 gives |kappa_alpha*tau_clock_time| <= 2.1e-18 yr^-1.",
            "effect_on_WEP_functor": "no-alpha-vertex cannot be hand-waved; alpha silence has to be parent-owned or screened consistently",
            "claim_status": "product_bound_only_not_standalone_kappa",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pressure_id": "AWP767_1_H0_screen",
            "imported_fact": "diagnostic |kappa_alpha*dchi_X/dN| <= 2.93296e-08 if tau_clock_time=H0*dchi_X/dN.",
            "effect_on_WEP_functor": "finite alpha branch requires ultra-screening unless local chi_X silence is derived",
            "claim_status": "diagnostic_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pressure_id": "AWP767_2_MICROSCOPE_beta_target",
            "imported_fact": "if direct alpha/mass WEP channel survives, robust beta_source_alpha target is <= 2.887280314062e-05.",
            "effect_on_WEP_functor": "common-geometry/no-alpha-vertex is now either a parent theorem, an explicit closure, or a numeric source-normalization debt",
            "claim_status": "numeric_target_not_derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pressure_id": "AWP767_3_no_kappa_rescale_escape",
            "imported_fact": "clock product bound makes kappa rescaling alone insufficient because WEP uses the same product screen.",
            "effect_on_WEP_functor": "branch cannot tune kappa_alpha down in WEP while keeping clock branch free",
            "claim_status": "policy_guard",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def local_GR_bridge_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "bridge_id": "LGB767_0_WEP_boxed",
            "local_GR_dependency": "one matter/source/clock frame",
            "status_after_767": "explicit_closure",
            "why_it_matters": "lets private local-GR branch proceed without pretending WEP was derived",
            "next_pressure": "carry closure label into every EH/PPN/source row",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bridge_id": "LGB767_1_EH_operator",
            "local_GR_dependency": "EH-only or executable retained R11 operator vector",
            "status_after_767": "blocked_current_state_from_655",
            "why_it_matters": "matter sees one frame does not make the exterior operator Einstein-Hilbert",
            "next_pressure": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bridge_id": "LGB767_2_Newton_source",
            "local_GR_dependency": "constant G_eff/kappa and measured GM source normalization",
            "status_after_767": "open_residual",
            "why_it_matters": "GR-to-Newton reduction needs the source/charge normalization, not just metric equations",
            "next_pressure": "source-normalization family remains high priority after EH/R11 gate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bridge_id": "LGB767_3_PPN_vector",
            "local_GR_dependency": "gamma=beta=1, alpha_i=xi=0, no Gdot, no finite-range residue",
            "status_after_767": "not_ready",
            "why_it_matters": "local GR claim requires weak-field readout, not only action-level prose",
            "next_pressure": "derive or score PPN/R10/Gdot residual vector after operator/source gates",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def source_fill_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "fill_id": "SFS767_0_parent_matter_functor",
            "artifact": str(MATTER_FUNCTOR_CANDIDATE_PATH),
            "required_columns": "sector;parent_functor;species_blind_geometry;source_path;valid_for_claim",
            "claim_gate": "WEP one-frame branch is parent-derived rather than closure",
            "current_status": f"schema_only_candidate_missing={bool_string(not MATTER_FUNCTOR_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "SFS767_1_no_alpha_vertex",
            "artifact": str(NO_ALPHA_VERTEX_CANDIDATE_PATH),
            "required_columns": "operator;forbidden_by;vertical_derivative;source_path;valid_for_claim",
            "claim_gate": "no alpha_EM(chi_X), f_A(chi_X)F2, m_A(chi_X), or binding response survives",
            "current_status": f"schema_only_candidate_missing={bool_string(not NO_ALPHA_VERTEX_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "SFS767_2_selector_Ward",
            "artifact": str(SELECTOR_WARD_CANDIDATE_PATH),
            "required_columns": "selector;stress_owner;conservation_identity;source_path;valid_for_claim",
            "claim_gate": "selector enforcing one geometry is Bianchi/Ward safe",
            "current_status": f"schema_only_candidate_missing={bool_string(not SELECTOR_WARD_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "SFS767_3_beta_source_alpha",
            "artifact": str(BETA_SOURCE_CANDIDATE_PATH),
            "required_columns": "source_body;channel;beta_source_alpha;bound_target;source_path;valid_for_claim",
            "claim_gate": "if no-alpha theorem fails, beta_source_alpha beats 2.887e-05 robust target",
            "current_status": f"schema_only_candidate_missing={bool_string(not BETA_SOURCE_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "SFS767_4_local_GR_reentry",
            "artifact": str(LOCAL_GR_REENTRY_CANDIDATE_PATH),
            "required_columns": "rung;closure_used;EH_or_R11_status;source_status;valid_for_claim",
            "claim_gate": "local-GR reentry keeps WEP closure visible and attacks EH/R11 gate next",
            "current_status": f"schema_only_candidate_missing={bool_string(not LOCAL_GR_REENTRY_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D767_0_functor_reaudit",
            "decision": "parent matter functor/no-alpha-vertex remains unsigned after 766",
            "why": "finite alpha clock/WEP pressure supplies stronger constraints, not a parent matter action derivation",
            "claim_status": "not_signed",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D767_1_WEP_closure",
            "decision": "retain WEP safety as explicit quarantined closure",
            "why": "653 demotion still holds and is now more important because alpha/WEP pressure is sharper",
            "claim_status": "explicit_closure_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D767_2_GR_reentry",
            "decision": "return to EH/R11 local-GR gate with WEP closure visible",
            "why": "the project goal needs GR/Newton reduction, and WEP is now boxed rather than hidden",
            "claim_status": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU767_0_allowed",
            "allowed_after_767": "use WEP closure as an explicitly labelled private branch condition",
            "forbidden_after_767": "cite WEP/common geometry as parent-derived",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU767_1_allowed",
            "allowed_after_767": "carry beta_source_alpha target if alpha/mass vertex survives",
            "forbidden_after_767": "drop MICROSCOPE pressure after adopting closure language",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU767_2_allowed",
            "allowed_after_767": "resume GR/Newton derivation at EH/R11 operator and source normalization gates",
            "forbidden_after_767": "let matter-frame closure substitute for EH, Newtonian source normalization, PPN, or R10 passes",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "766 alpha pressure does not sign parent matter functor; it confirms WEP closure must stay quarantined",
            "hard_blocker": "species-blind matter functor, no-alpha/mass vertex, and selector Ward identity remain unsigned",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    reaudit: list[dict[str, Any]],
    quarantine: list[dict[str, Any]],
    alpha_pressure: list[dict[str, Any]],
    gr_bridge: list[dict[str, Any]],
    source_fill: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V767_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V767_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all local source needles present"})
    prior_766 = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_766_VALIDATION.csv")
    prior_653 = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_653_VALIDATION.csv")
    validation.append({"check_id": "V767_2_prior_766_clean", "result": "pass" if prior_766 and all(row.get("result") == "pass" for row in prior_766) else "fail", "detail": "766 validation has no failures"})
    validation.append({"check_id": "V767_3_prior_653_clean", "result": "pass" if prior_653 and all(row.get("result") == "pass" for row in prior_653) else "fail", "detail": "653 validation has no failures"})
    validation.append({"check_id": "V767_4_functor_reaudit_unsigned", "result": "pass" if len(reaudit) == 6 and any(row["reaudit_id"] == "PMR767_3_no_alpha_mass_vertex" and row["verdict_after_766"] == "hard_blocker_still_unsigned" for row in reaudit) else "fail", "detail": "matter functor/no-alpha blocker remains unsigned"})
    validation.append({"check_id": "V767_5_WEP_closure_quarantined", "result": "pass" if len(quarantine) == 5 and all("closure" in row["status_after_766"] or "target" in row["status_after_766"] for row in quarantine) else "fail", "detail": "WEP rows remain closure/fallback only"})
    validation.append({"check_id": "V767_6_alpha_pressure_imported", "result": "pass" if len(alpha_pressure) == 4 and any("2.887280314062e-05" in row["imported_fact"] for row in alpha_pressure) else "fail", "detail": "clock/WEP alpha pressure imported"})
    validation.append({"check_id": "V767_7_GR_bridge_returns_to_EH_R11", "result": "pass" if any(row["bridge_id"] == "LGB767_1_EH_operator" and row["status_after_767"] == "blocked_current_state_from_655" for row in gr_bridge) else "fail", "detail": "GR bridge targets EH/R11 reentry"})
    validation.append({"check_id": "V767_8_source_fill_schema_written", "result": "pass" if len(source_fill) == 5 and all(row["valid_for_claim"] == "false" for row in source_fill) else "fail", "detail": "source-fill rows schema-only"})
    candidate_paths = [MATTER_FUNCTOR_CANDIDATE_PATH, NO_ALPHA_VERTEX_CANDIDATE_PATH, SELECTOR_WARD_CANDIDATE_PATH, BETA_SOURCE_CANDIDATE_PATH, LOCAL_GR_REENTRY_CANDIDATE_PATH]
    validation.append({"check_id": "V767_9_candidate_artifacts_not_faked", "result": "pass" if not any(path.exists() for path in candidate_paths) else "fail", "detail": "no claim-input artifacts fabricated"})
    all_generated = reaudit + quarantine + alpha_pressure + gr_bridge + source_fill + decisions + routes + summary
    validation.append({"check_id": "V767_10_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_generated) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V767_11_no_WEP_or_GR_claim", "result": "pass" if "no_WEP_Newton_PPN_EH_or_local_GR_claim" in CLAIM_CEILING else "fail", "detail": "WEP/GR/Newton claims remain blocked"})
    validation.append({"check_id": "V767_12_next_target_selected", "result": "pass" if all(row.get("next_action") == NEXT_TARGET for row in routes) and all(row.get("next_target") == NEXT_TARGET for row in decisions) and summary[0].get("next_target") == NEXT_TARGET else "fail", "detail": NEXT_TARGET})
    output_paths = [
        Path(__file__),
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        FUNCTOR_REAUDIT_PATH,
        WEP_QUARANTINE_PATH,
        ALPHA_PRESSURE_IMPORT_PATH,
        LOCAL_GR_BRIDGE_PATH,
        SOURCE_FILL_PATH,
        DECISION_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]
    validation.append({"check_id": "V767_13_outputs_scoped", "result": "pass" if all(under_post(path) for path in output_paths) else "fail", "detail": "all outputs under post-checkpoint-work"})
    fw_count = formalization_changed_after_cutoff()
    validation.append({"check_id": "V767_14_formalization_workbench_untouched", "result": "pass" if fw_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={fw_count}"})
    validation.append({"check_id": "V767_15_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    reaudit: list[dict[str, Any]],
    quarantine: list[dict[str, Any]],
    alpha_pressure: list[dict[str, Any]],
    gr_bridge: list[dict[str, Any]],
    source_fill: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 767 - Y5 R10 Parent Matter Functor No-Alpha Vertex Or WEP Closure

Start point: 766 sharpened the finite-alpha side: no parent source reactivated `kappa_alpha=0`; clocks now give product bounds, and WEP keeps the `beta_source_alpha <= 2.887e-05` fallback target if a direct alpha/mass source survives.

Current result: **the parent matter functor/no-alpha-vertex theorem is still not signed; WEP safety remains an explicit quarantined closure**. This is not new failure theatre — it is a current-state re-audit of 653 under the sharper 766 alpha pressure. The older demotion still holds, and it is now more important because the clock/WEP channels are no longer vague.

## Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target"])}

## Parent Matter Functor Re-Audit

{markdown_table(reaudit, ["reaudit_id", "required_signature", "current_evidence", "verdict_after_766", "risk_if_used", "valid_for_claim"])}

## WEP Closure Quarantine

{markdown_table(quarantine, ["closure_id", "closure_statement", "status_after_766", "allowed_private_use", "forbidden_use", "valid_for_claim"])}

## Alpha/WEP Pressure Import

{markdown_table(alpha_pressure, ["pressure_id", "imported_fact", "effect_on_WEP_functor", "claim_status", "valid_for_claim"])}

## Local-GR Bridge

{markdown_table(gr_bridge, ["bridge_id", "local_GR_dependency", "status_after_767", "why_it_matters", "next_pressure", "valid_for_claim"])}

## Source-Fill Schema

{markdown_table(source_fill, ["fill_id", "artifact", "required_columns", "claim_gate", "current_status", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "why", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_767", "forbidden_after_767", "next_action", "valid_for_claim"])}

## Local Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

WEP is boxed, not won. That is the right position. The branch can still be used privately as a disciplined closure condition, but it cannot pay the GR/Newton bill. The next push should go back to the metric/operator side: EH-only from the parent action, or an executable retained R11/non-EH vector. That is the path toward a real GR-to-Newton reduction rather than a patchwork escape.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    reaudit = functor_reaudit_rows(generated_utc)
    quarantine = WEP_quarantine_rows(generated_utc)
    alpha_pressure = alpha_pressure_rows(generated_utc)
    gr_bridge = local_GR_bridge_rows(generated_utc)
    source_fill = source_fill_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validate(sources, reaudit, quarantine, alpha_pressure, gr_bridge, source_fill, decisions, routes, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(FUNCTOR_REAUDIT_PATH, reaudit, ["reaudit_id", "required_signature", "current_evidence", "verdict_after_766", "risk_if_used", "valid_for_claim", "generated_utc"])
    write_csv(WEP_QUARANTINE_PATH, quarantine, ["closure_id", "closure_statement", "status_after_766", "allowed_private_use", "forbidden_use", "valid_for_claim", "generated_utc"])
    write_csv(ALPHA_PRESSURE_IMPORT_PATH, alpha_pressure, ["pressure_id", "imported_fact", "effect_on_WEP_functor", "claim_status", "valid_for_claim", "generated_utc"])
    write_csv(LOCAL_GR_BRIDGE_PATH, gr_bridge, ["bridge_id", "local_GR_dependency", "status_after_767", "why_it_matters", "next_pressure", "valid_for_claim", "generated_utc"])
    write_csv(SOURCE_FILL_PATH, source_fill, ["fill_id", "artifact", "required_columns", "claim_gate", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "why", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_PATH, routes, ["route_id", "allowed_after_767", "forbidden_after_767", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, reaudit, quarantine, alpha_pressure, gr_bridge, source_fill, decisions, routes, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        print(f"wrote {OUTPUT_DOC}")
        print(f"wrote {VALIDATION_PATH}")
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)
    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")


if __name__ == "__main__":
    main()
