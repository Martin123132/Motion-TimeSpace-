#!/usr/bin/env python3
"""Audit whether the locked late-time branch is ready for field-theory promotion."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"
FORMALIZATION_WORKBENCH = WORK_DIR.parent / "formalization-workbench"

LOCKED_BRANCH = "MTS_locked_2over27"
LOCKED_B_MEM = 2.0 / 27.0
CLAIM_CEILING = "promotion_contract_private_audit_no_unified_theory_or_CMB_or_local_GR_claim"


SOURCE_DOCS = [
    {
        "source_id": "growth_perturbation_contract",
        "source_type": "checkpoint_doc",
        "role": "defines perturbation, conservation, CMB, and local-GR promotion gates",
        "path": WORK_DIR / "131-growth-perturbation-contract.md",
        "notes": "primary contract: F_fric, mu, S_mem, Q^nu, CMB Boltzmann boundary, local PPN locks",
    },
    {
        "source_id": "high_sound_speed_or_auxiliary_owner",
        "source_type": "checkpoint_doc",
        "role": "stress-tests whether memory perturbations can be effectively smooth",
        "path": WORK_DIR / "135-high-sound-speed-or-auxiliary-memory-owner.md",
        "notes": "conditional effective owner; not a full parent perturbation derivation",
    },
    {
        "source_id": "consolidated_locked_branch",
        "source_type": "checkpoint_doc",
        "role": "separates frozen empirical closure from derived parent theory",
        "path": WORK_DIR / "141-consolidated-locked-memory-branch-contract.md",
        "notes": "locks B_mem=2/27 as empirical closure and blocks amplitude overclaim",
    },
    {
        "source_id": "domain_selector_action_attempt",
        "source_type": "checkpoint_doc",
        "role": "audits whether the domain selector is variationally derived",
        "path": WORK_DIR / "143-domain-selector-variational-action-attempt.md",
        "notes": "zero-knob domain selector not derived; D remains closure-level",
    },
    {
        "source_id": "frozen_branch_empirical_scorecard",
        "source_type": "checkpoint_doc",
        "role": "summarizes late-time empirical stack and CMB bridge boundary",
        "path": WORK_DIR / "144-frozen-branch-empirical-holdout-scorecard.md",
        "notes": "late-time survives; CMB bridge unresolved",
    },
    {
        "source_id": "fresh_CC_Hz_holdout",
        "source_type": "checkpoint_doc",
        "role": "source-locked cosmic chronometer H(z) holdout",
        "path": WORK_DIR / "145-fresh-CC-Hz-source-locked-holdout.md",
        "notes": "fresh source-locked H(z) competitive draw",
    },
    {
        "source_id": "growth_covariance_holdout",
        "source_type": "checkpoint_doc",
        "role": "source-locked SDSS/eBOSS growth covariance holdout",
        "path": WORK_DIR / "146-source-locked-growth-covariance-holdout.md",
        "notes": "growth covariance preferred/draw under GR-proxy growth",
    },
    {
        "source_id": "ELG_grid_holdout",
        "source_type": "checkpoint_doc",
        "role": "non-Gaussian ELG grid likelihood holdout",
        "path": WORK_DIR / "147-ELG-grid-likelihood-holdout.md",
        "notes": "ELG grid competitive draw; diagnostic combined card preferred",
    },
]


RUN_INPUTS = [
    {
        "source_id": "run_134_subhorizon_gate",
        "run_name": "20260531-191200-subhorizon-suppressed-growth-correction-gate",
        "role": "subhorizon correction gate feeding perturbation contract",
    },
    {
        "source_id": "run_135_high_sound_speed",
        "run_name": "20260531-192900-high-sound-speed-or-auxiliary-memory-owner",
        "role": "effective smooth-memory owner attempt",
    },
    {
        "source_id": "run_141_consolidated_branch",
        "run_name": "20260531-210000-consolidated-locked-memory-branch-contract",
        "role": "locked branch consolidation",
    },
    {
        "source_id": "run_143_domain_selector",
        "run_name": "20260531-213000-domain-selector-variational-action-attempt",
        "role": "domain selector promotion audit",
    },
    {
        "source_id": "run_144_empirical_scorecard",
        "run_name": "20260531-214500-frozen-branch-empirical-holdout-scorecard",
        "role": "empirical holdout scorecard",
    },
    {
        "source_id": "run_145_fresh_CC_Hz",
        "run_name": "20260531-221500-fresh-CC-Hz-source-locked-holdout",
        "role": "fresh source-locked H(z) holdout",
    },
    {
        "source_id": "run_146_growth_covariance",
        "run_name": "20260531-224500-source-locked-growth-covariance-holdout",
        "role": "source-locked SDSS/eBOSS growth covariance holdout",
    },
    {
        "source_id": "run_147_ELG_grid",
        "run_name": "20260531-231500-ELG-grid-likelihood-holdout",
        "role": "non-Gaussian ELG grid holdout",
    },
]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def path_status(path: Path) -> dict[str, Any]:
    exists = path.exists()
    return {
        "path": str(path),
        "exists": "yes" if exists else "no",
        "sha256": sha256_file(path) if exists and path.is_file() else "",
    }


def run_status(run_name: str) -> str:
    status_path = RUNS_ROOT / run_name / "status.json"
    payload = read_json(status_path)
    return str(payload.get("status", "missing_status_json"))


def make_source_register() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCE_DOCS:
        status = path_status(source["path"])
        rows.append(
            {
                "source_id": source["source_id"],
                "source_type": source["source_type"],
                "role": source["role"],
                "path": status["path"],
                "exists": status["exists"],
                "sha256": status["sha256"],
                "status": "available" if status["exists"] == "yes" else "missing",
                "notes": source["notes"],
            }
        )

    for run in RUN_INPUTS:
        run_dir = RUNS_ROOT / run["run_name"]
        status_path = run_dir / "status.json"
        decision_path = run_dir / "results" / "decision.csv"
        for source_type, path, notes in [
            ("run_dir", run_dir, run["role"]),
            ("run_status_json", status_path, run_status(run["run_name"])),
            ("run_decision_csv", decision_path, "machine decision table"),
        ]:
            status = path_status(path)
            rows.append(
                {
                    "source_id": run["source_id"],
                    "source_type": source_type,
                    "role": run["role"],
                    "path": status["path"],
                    "exists": status["exists"],
                    "sha256": status["sha256"],
                    "status": "available" if status["exists"] == "yes" else "missing",
                    "notes": notes,
                }
            )
    return rows


def make_empirical_readiness_scorecard() -> list[dict[str, Any]]:
    return [
        {
            "arena": "SN+BAO full-covariance robustness",
            "checkpoint": "144",
            "baseline": "fitted LCDM",
            "primary_metric": "delta_BIC",
            "locked_result": "-5.259466877748764",
            "status": "locked_preferred",
            "interpretation": "late-time background branch wins this card against fitted LCDM under the frozen B_mem rule",
            "claim_limit": "background likelihood only; no perturbation or CMB promotion",
            "source_paths": str(WORK_DIR / "144-frozen-branch-empirical-holdout-scorecard.md"),
        },
        {
            "arena": "BAO-only release holdout",
            "checkpoint": "144",
            "baseline": "fitted LCDM",
            "primary_metric": "delta_BIC",
            "locked_result": "DR2=-2.108368627321081; DR1=-0.8483738675035859",
            "status": "preferred_or_draw",
            "interpretation": "BAO-only releases do not erase the locked branch; DR2 is preferred and DR1 is a draw",
            "claim_limit": "BAO background only",
            "source_paths": str(WORK_DIR / "144-frozen-branch-empirical-holdout-scorecard.md"),
        },
        {
            "arena": "BAO+H(z), no CMB",
            "checkpoint": "144",
            "baseline": "fitted LCDM/wCDM/CPL branches",
            "primary_metric": "branch stability",
            "locked_result": "10/10 production branches draw; delta_BIC range [-1.9014668577456,-0.5803932783513801]",
            "status": "competitive_draw",
            "interpretation": "the branch stays on the cards when H(z) is added without CMB calibration pressure",
            "claim_limit": "late-time expansion only",
            "source_paths": str(WORK_DIR / "144-frozen-branch-empirical-holdout-scorecard.md"),
        },
        {
            "arena": "fresh cosmic chronometer H(z)",
            "checkpoint": "145",
            "baseline": "fitted LCDM",
            "primary_metric": "delta_BIC",
            "locked_result": "+0.33256956910347313",
            "status": "competitive_draw",
            "interpretation": "source-locked CC15 BC03 primary is a narrow draw rather than a loss",
            "claim_limit": "H(z) source-locked holdout only",
            "source_paths": str(WORK_DIR / "145-fresh-CC-Hz-source-locked-holdout.md"),
        },
        {
            "arena": "SDSS/eBOSS Gaussian growth covariance",
            "checkpoint": "146",
            "baseline": "fitted LCDM/wCDM/CPL with shared sigma8 treatment",
            "primary_metric": "delta_chi2",
            "locked_result": "primary_all=-2.30357028036; RSD_only=-0.334685976748; jackknife_failures=0",
            "status": "preferred_or_draw",
            "interpretation": "under the GR-proxy growth equation, the source-locked covariance card is favourable without giving baselines a free pass",
            "claim_limit": "not a derived MTS perturbation theory",
            "source_paths": str(WORK_DIR / "146-source-locked-growth-covariance-holdout.md"),
        },
        {
            "arena": "SDSS/eBOSS ELG non-Gaussian grid",
            "checkpoint": "147",
            "baseline": "fitted LCDM/wCDM/CPL grid scoring",
            "primary_metric": "delta_chi2",
            "locked_result": "ELG_vs_LCDM=+0.03750180074447895; diagnostic_Gaussian_plus_ELG=-2.2660684796112336",
            "status": "competitive_draw",
            "interpretation": "the non-Gaussian ELG branch does not reverse the favourable Gaussian growth card",
            "claim_limit": "diagnostic combined sum is not an official joint likelihood",
            "source_paths": str(WORK_DIR / "147-ELG-grid-likelihood-holdout.md"),
        },
        {
            "arena": "compressed CMB distance score",
            "checkpoint": "144 plus 116",
            "baseline": "compressed distance priors",
            "primary_metric": "stress-test readout",
            "locked_result": "compressed-distance draw only",
            "status": "stress_draw_only",
            "interpretation": "useful as a boundary stress test, but it is not a Boltzmann-level CMB pass",
            "claim_limit": "no CMB promotion",
            "source_paths": f"{WORK_DIR / '144-frozen-branch-empirical-holdout-scorecard.md'}; {WORK_DIR / '116-locked-2over27-CMB-distance-score.md'}",
        },
        {
            "arena": "late-to-CMB transfer and joint bridge",
            "checkpoint": "144 plus 117-120",
            "baseline": "late-time to early-time calibration bridge",
            "primary_metric": "bridge status",
            "locked_result": "late-to-CMB transfer fail; joint bridge mixed",
            "status": "not_promoted",
            "interpretation": "this is the unresolved belt-round: the late-time branch has not been promoted through CMB physics",
            "claim_limit": "must not claim MTS passes CMB",
            "source_paths": f"{WORK_DIR / '117-locked-2over27-late-CMB-transfer-gate.md'}; {WORK_DIR / '120-joint-calibration-red-team-and-repair-options.md'}",
        },
    ]


def make_promotion_requirement_matrix() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "P01",
            "requirement": "locked background equation is encoded with frozen B_mem=2/27",
            "current_status": "pass",
            "evidence": "141 consolidates rho_M=rho_Lambda+B_mem A with B_mem fixed; 144-147 keep the frozen rule",
            "blocking_issue": "none for empirical closure",
            "promotion_condition": "continue to treat B_mem as predeclared unless a parent theorem derives it",
            "source_paths": f"{WORK_DIR / '141-consolidated-locked-memory-branch-contract.md'}; {WORK_DIR / '144-frozen-branch-empirical-holdout-scorecard.md'}",
        },
        {
            "gate_id": "P02",
            "requirement": "pressure and activation mechanics are not silently promoted",
            "current_status": "conditional_pass",
            "evidence": "pressure/activation routes are fenced as conditional mechanics, not completed derivations",
            "blocking_issue": "mechanics are plausible but still require parent ownership",
            "promotion_condition": "derive pressure, activation shape, and regularity from the same parent action",
            "source_paths": str(WORK_DIR / "141-consolidated-locked-memory-branch-contract.md"),
        },
        {
            "gate_id": "P03",
            "requirement": "effective high-sound-speed or auxiliary owner suppresses clustering",
            "current_status": "conditional_effective",
            "evidence": "135 gives an effective route but does not fully derive the perturbation action",
            "blocking_issue": "effective smoothness is not the same as a parent perturbation theorem",
            "promotion_condition": "prove smooth-memory/no-clustering theorem or derive controlled modified-growth terms",
            "source_paths": str(WORK_DIR / "135-high-sound-speed-or-auxiliary-memory-owner.md"),
        },
        {
            "gate_id": "P04",
            "requirement": "parent perturbation action names metric, matter, memory, and perturbation variables",
            "current_status": "fail_missing_derivation",
            "evidence": "131 defines required field content but no completed parent action supplies it",
            "blocking_issue": "no derived delta_U_mem or equivalent perturbation owner",
            "promotion_condition": "write a variational perturbation action and derive linear equations",
            "source_paths": str(WORK_DIR / "131-growth-perturbation-contract.md"),
        },
        {
            "gate_id": "P05",
            "requirement": "Bianchi/conservation contract is satisfied",
            "current_status": "partial_contract",
            "evidence": "131 allows separate conservation or controlled exchange Q^nu with Q^nu->0 locally",
            "blocking_issue": "Q^nu is a contract target, not a derived tensor expression",
            "promotion_condition": "derive nabla_mu(T_m+T_mem)^{mu nu}=0 and either Q^nu=0 or controlled Q^nu",
            "source_paths": str(WORK_DIR / "131-growth-perturbation-contract.md"),
        },
        {
            "gate_id": "P06",
            "requirement": "growth equation derives F_fric(a,k), mu(a,k), and S_mem(a,k)",
            "current_status": "fail_missing_derivation",
            "evidence": "146 growth success uses a GR-proxy growth equation, not derived MTS perturbation functions",
            "blocking_issue": "no field-theoretic mu/slip/source prediction exists yet",
            "promotion_condition": "derive F_fric, mu, eta_slip/Sigma, and S_mem with GR limits",
            "source_paths": f"{WORK_DIR / '131-growth-perturbation-contract.md'}; {WORK_DIR / '146-source-locked-growth-covariance-holdout.md'}",
        },
        {
            "gate_id": "P07",
            "requirement": "CMB Boltzmann-level interface is defined",
            "current_status": "fail_missing_derivation",
            "evidence": "compressed CMB distances are stress tests only; late-to-CMB transfer remains unresolved",
            "blocking_issue": "no CLASS/CAMB-ready memory stress, sound speed, anisotropic stress, or recombination-era map",
            "promotion_condition": "define Boltzmann variables and run CMB spectra, not just compressed priors",
            "source_paths": f"{WORK_DIR / '131-growth-perturbation-contract.md'}; {WORK_DIR / '117-locked-2over27-late-CMB-transfer-gate.md'}",
        },
        {
            "gate_id": "P08",
            "requirement": "local GR and PPN silence are derived",
            "current_status": "fail_missing_derivation",
            "evidence": "131 states local locks Phi=Psi, G_eff/G->1, Q^nu->0, and local memory force->0",
            "blocking_issue": "no completed proof derives these from the parent branch",
            "promotion_condition": "derive local q_loc^nu suppression and PPN residual vector below bounds",
            "source_paths": str(WORK_DIR / "131-growth-perturbation-contract.md"),
        },
        {
            "gate_id": "P09",
            "requirement": "domain selector D is selected by a zero-knob variational mechanism",
            "current_status": "fail_missing_derivation",
            "evidence": "143 finds auxiliary selector safe conditionally, but domain selection itself remains closure-level",
            "blocking_issue": "no zero-knob Euler equation selects the physical domain",
            "promotion_condition": "derive D and boundary exchange from parent variables without rescue knobs",
            "source_paths": str(WORK_DIR / "143-domain-selector-variational-action-attempt.md"),
        },
        {
            "gate_id": "P10",
            "requirement": "amplitude B_mem=2/27 is derived rather than fitted or retrofitted",
            "current_status": "blocked_for_promotion",
            "evidence": "141 explicitly marks B_mem=2/27 as empirical locked closure",
            "blocking_issue": "amplitude theorem remains open",
            "promotion_condition": "derive 2/27 from a normalized boundary/current/action law before claiming prediction",
            "source_paths": str(WORK_DIR / "141-consolidated-locked-memory-branch-contract.md"),
        },
        {
            "gate_id": "P11",
            "requirement": "baselines receive the same stress tests",
            "current_status": "pass",
            "evidence": "144-147 compare against fitted LCDM/wCDM/CPL or shared-sigma8 baselines rather than testing MTS alone",
            "blocking_issue": "official joint likelihood still needed for publication-grade comparison",
            "promotion_condition": "keep baseline parity in every future jackknife/data split",
            "source_paths": f"{WORK_DIR / '144-frozen-branch-empirical-holdout-scorecard.md'}; {WORK_DIR / '146-source-locked-growth-covariance-holdout.md'}; {WORK_DIR / '147-ELG-grid-likelihood-holdout.md'}",
        },
        {
            "gate_id": "P12",
            "requirement": "public claim discipline is enforced",
            "current_status": "pass_control",
            "evidence": "all late-time wins/draws are claim-limited as private empirical/theory-discipline checkpoints",
            "blocking_issue": "none if claim ceiling is obeyed",
            "promotion_condition": "only promote after P04-P10 are satisfied",
            "source_paths": str(WORK_DIR / "144-frozen-branch-empirical-holdout-scorecard.md"),
        },
    ]


def make_claim_ladder() -> list[dict[str, Any]]:
    return [
        {
            "claim_tier": "private_internal",
            "claim_status": "allowed_now",
            "statement": "The frozen 2/27 late-time branch is empirically alive and worth theory-promotion work.",
            "not_allowed_upgrade": "The unified field theory is established.",
            "needed_before_upgrade": "complete perturbation, CMB, local-GR, domain, and amplitude derivations",
        },
        {
            "claim_tier": "late_time_background",
            "claim_status": "allowed_now",
            "statement": "Against fair fitted baselines, the branch wins or draws several late-time background rounds.",
            "not_allowed_upgrade": "The branch explains all cosmological observations.",
            "needed_before_upgrade": "official joint likelihood and CMB-compatible perturbation sector",
        },
        {
            "claim_tier": "growth_effective",
            "claim_status": "allowed_with_warning",
            "statement": "Under a GR-proxy growth treatment, source-locked growth covariance and ELG scoring do not disfavor the branch.",
            "not_allowed_upgrade": "MTS has derived growth perturbations.",
            "needed_before_upgrade": "derive F_fric, mu, slip/Sigma, and S_mem from parent equations",
        },
        {
            "claim_tier": "CMB",
            "claim_status": "forbidden_now",
            "statement": "MTS passes CMB.",
            "not_allowed_upgrade": "Any CMB pass claim from compressed-distance stress tests.",
            "needed_before_upgrade": "Boltzmann-level implementation and spectra comparison",
        },
        {
            "claim_tier": "local_GR",
            "claim_status": "forbidden_now",
            "statement": "MTS derives local GR or PPN silence.",
            "not_allowed_upgrade": "Treating local silence as proven because the background branch works.",
            "needed_before_upgrade": "derive q_loc^nu suppression, G_eff/G->1, Phi=Psi, and bounded PPN residuals",
        },
        {
            "claim_tier": "amplitude",
            "claim_status": "forbidden_now",
            "statement": "B_mem=2/27 is derived.",
            "not_allowed_upgrade": "Calling the frozen empirical closure a prediction.",
            "needed_before_upgrade": "derive the amplitude from boundary/current/action normalization",
        },
    ]


def make_next_work_queue() -> list[dict[str, Any]]:
    return [
        {
            "priority": "1",
            "target": "149-smooth-memory-or-controlled-growth-theorem.md",
            "question": "Can the memory sector be smooth enough to justify the GR-proxy growth success, or must it generate controlled modified growth?",
            "deliverable": "derive delta_U_mem=0 theorem or explicit F_fric, mu, slip/Sigma, and S_mem equations",
            "acceptance_gate": "GR limit recovered; no free mu_0/sigma8 rescue; local PPN limits stated",
        },
        {
            "priority": "2",
            "target": "150-Boltzmann-interface-contract.md",
            "question": "What exact variables would CLASS/CAMB need to propagate the memory branch through CMB physics?",
            "deliverable": "w(a), c_s^2(a,k), c_vis^2/slip, source terms, early-time limit, recombination-era behavior",
            "acceptance_gate": "compressed CMB replaced by spectra-level contract",
        },
        {
            "priority": "3",
            "target": "151-local-PPN-silence-theorem.md",
            "question": "Can q_loc^nu suppression and local GR be derived rather than assumed?",
            "deliverable": "local exchange/current profile, amplitude bound, PPN residual vector",
            "acceptance_gate": "G_eff/G->1, Phi=Psi, Q^nu->0 with quantitative bounds",
        },
        {
            "priority": "4",
            "target": "152-official-joint-likelihood-wrapper.md",
            "question": "If empirical work continues, can all current wins/draws survive an official joint wrapper?",
            "deliverable": "single reproducible likelihood runner with baseline parity and frozen MTS parameters",
            "acceptance_gate": "SN/BAO/H(z)/growth/ELG branches reproduce checkpoint numbers before extension",
        },
    ]


def make_boxing_scorecard() -> list[dict[str, Any]]:
    return [
        {
            "round": "late-time expansion",
            "card": "MTS ahead or drawing",
            "judge_note": "SN+BAO and BAO-only give real cards; H(z) keeps it competitive",
            "risk": "background-only success can still fail at perturbations",
        },
        {
            "round": "growth holdouts",
            "card": "MTS drawing to ahead under GR-proxy",
            "judge_note": "source-locked covariance is favourable and ELG grid is a draw",
            "risk": "the growth equation is borrowed/proxy until derived",
        },
        {
            "round": "CMB",
            "card": "not scored as a win",
            "judge_note": "compressed distances are only sparring; late-to-CMB bridge is unresolved",
            "risk": "Boltzmann-level physics can overturn late-time comfort",
        },
        {
            "round": "local GR",
            "card": "title belt not awarded",
            "judge_note": "local locks are known targets, not proven consequences",
            "risk": "without local silence, MTS becomes another phenomenological cosmology rather than a GR-reducing field theory",
        },
        {
            "round": "parent action and amplitude",
            "card": "promising but blocked",
            "judge_note": "B_mem=2/27 is frozen and productive, but still empirical closure",
            "risk": "amplitude and domain selector must be derived before public promotion",
        },
    ]


def make_gate_results(source_rows: list[dict[str, Any]], promotion_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = sum(1 for row in source_rows if row["exists"] != "yes")
    failed_promotions = [
        row
        for row in promotion_rows
        if row["current_status"] in {"fail_missing_derivation", "blocked_for_promotion"}
    ]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing_sources={missing_sources}",
            "decision": "audit usable only if every cited source exists",
        },
        {
            "gate": "late_time_empirical_stack",
            "status": "pass",
            "evidence": "SN+BAO preferred; BAO/H(z)/fresh CC/growth/ELG draw or better under frozen branch",
            "decision": "empirical branch remains alive and worth promotion work",
        },
        {
            "gate": "baseline_parity",
            "status": "pass",
            "evidence": "LCDM/wCDM/CPL or shared-sigma8 baselines are scored on the same tests",
            "decision": "do not treat baseline fragility as an MTS-only failure mode",
        },
        {
            "gate": "perturbation_promotion",
            "status": "fail",
            "evidence": "missing derived perturbation action and F_fric/mu/S_mem/slip equations",
            "decision": "growth results remain effective/proxy, not derived field-theory evidence",
        },
        {
            "gate": "CMB_promotion",
            "status": "fail",
            "evidence": "compressed distance stress only; late-to-CMB transfer unresolved",
            "decision": "no CMB claim",
        },
        {
            "gate": "local_GR_promotion",
            "status": "fail",
            "evidence": "local q_loc^nu, PPN residuals, and G_eff/Phi/Psi limits not derived",
            "decision": "no local-GR reduction claim",
        },
        {
            "gate": "amplitude_and_domain_promotion",
            "status": "fail",
            "evidence": "B_mem=2/27 and D selector remain closure-level",
            "decision": "no parent-theory promotion until amplitude/domain theorem is supplied",
        },
        {
            "gate": "claim_discipline",
            "status": "pass_control",
            "evidence": f"failed_promotion_requirements={len(failed_promotions)}; claim_ceiling={CLAIM_CEILING}",
            "decision": "late-time branch can be discussed as serious, not as completed unified theory",
        },
    ]


def make_decision() -> list[dict[str, Any]]:
    return [
        {
            "item": "status",
            "verdict": "late_time_empirical_branch_ready_for_theory_promotion_work_not_promoted",
            "evidence": "empirical cards are strong enough to justify derivation work; promotion blocked by perturbation/CMB/local-GR/amplitude/domain gaps",
        },
        {
            "item": "best_next_target",
            "verdict": "149-smooth-memory-or-controlled-growth-theorem.md",
            "evidence": "growth and ELG holdouts are now good enough that the decisive next move is deriving the perturbation owner",
        },
        {
            "item": "claim_ceiling",
            "verdict": CLAIM_CEILING,
            "evidence": "private audit only; no public CMB, local-GR, amplitude, or unified-theory claim",
        },
        {
            "item": "boxing_readout",
            "verdict": "MTS_is_on_the_cards_late_time_belt_requires_field_theory_rounds",
            "evidence": "the branch can win/draw rounds without a knockout, but title promotion requires derived GR/CMB/perturbation limits",
        },
    ]


def run_audit(output_root: Path, timestamp: str | None = None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-promotion-contract-audit"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = make_source_register()
    empirical_rows = make_empirical_readiness_scorecard()
    promotion_rows = make_promotion_requirement_matrix()
    claim_rows = make_claim_ladder()
    next_rows = make_next_work_queue()
    boxing_rows = make_boxing_scorecard()
    gate_rows = make_gate_results(source_rows, promotion_rows)
    decision_rows = make_decision()

    write_csv(
        results_dir / "source_register.csv",
        source_rows,
        ["source_id", "source_type", "role", "path", "exists", "sha256", "status", "notes"],
    )
    write_csv(
        results_dir / "empirical_readiness_scorecard.csv",
        empirical_rows,
        [
            "arena",
            "checkpoint",
            "baseline",
            "primary_metric",
            "locked_result",
            "status",
            "interpretation",
            "claim_limit",
            "source_paths",
        ],
    )
    write_csv(
        results_dir / "promotion_requirement_matrix.csv",
        promotion_rows,
        [
            "gate_id",
            "requirement",
            "current_status",
            "evidence",
            "blocking_issue",
            "promotion_condition",
            "source_paths",
        ],
    )
    write_csv(
        results_dir / "claim_ladder.csv",
        claim_rows,
        ["claim_tier", "claim_status", "statement", "not_allowed_upgrade", "needed_before_upgrade"],
    )
    write_csv(
        results_dir / "next_work_queue.csv",
        next_rows,
        ["priority", "target", "question", "deliverable", "acceptance_gate"],
    )
    write_csv(
        results_dir / "boxing_scorecard.csv",
        boxing_rows,
        ["round", "card", "judge_note", "risk"],
    )
    write_csv(
        results_dir / "gate_results.csv",
        gate_rows,
        ["gate", "status", "evidence", "decision"],
    )
    write_csv(
        results_dir / "decision.csv",
        decision_rows,
        ["item", "verdict", "evidence"],
    )

    failed_promotion_count = sum(
        1
        for row in promotion_rows
        if row["current_status"] in {"fail_missing_derivation", "blocked_for_promotion"}
    )
    missing_source_count = sum(1 for row in source_rows if row["exists"] != "yes")
    status = {
        "status": decision_rows[0]["verdict"],
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "locked_branch": LOCKED_BRANCH,
        "locked_B_mem": LOCKED_B_MEM,
        "missing_source_count": missing_source_count,
        "failed_promotion_requirement_count": failed_promotion_count,
        "empirical_card": "late_time_wins_or_draws",
        "promotion_card": "blocked_until_perturbation_CMB_local_GR_amplitude_domain_derivations",
        "generated": [
            "source_register.csv",
            "empirical_readiness_scorecard.csv",
            "promotion_requirement_matrix.csv",
            "claim_ladder.csv",
            "next_work_queue.csv",
            "boxing_scorecard.csv",
            "gate_results.csv",
            "decision.csv",
            "status.json",
        ],
        "next_target": "149-smooth-memory-or-controlled-growth-theorem.md",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_audit(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
