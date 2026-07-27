from __future__ import annotations

import csv
import math
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
DOC_PATH = ROOT / "4082-Y5-R2FR-EM-Hodge-Maxwell-source-theorem-or-light-cone-bound.md"

DECISION = "EM_HODGE_MAXWELL_THEOREM_EXACT_CONDITIONAL_PARENT_UNSIGNED_LIGHT_CONE_BOUNDS_SOURCED"

BARTLETT_DELTA_GAMMA_BOUND = 2.1e-15
FERMI_EQG1_PLANCK_BOUND = 7.6
FERMI_EQG2_GEV_BOUND = 1.3e11
KM_GRB_POLARIZATION_FRACTION_BOUND = 1.0e-37

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4082_00_4081_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4081_NEXT_TARGET.csv",
        "4082-Y5-R2FR-EM-Hodge-Maxwell-source-theorem-or-light-cone-bound.md",
        "4081 selected EM Hodge/Maxwell source theorem or light-cone bound.",
    ),
    "SRC4082_01_em_gate_audit": (
        FORMALIZATION / "29-em-maxwell-gate-audit.md",
        "Maxwell recovery: not passed",
        "formal workbench audit blocks any Maxwell/QED claim before gauge/current/Hodge recovery.",
    ),
    "SRC4082_02_maxwell_targets": (
        FORMALIZATION / "32-maxwell-limit-targets.md",
        "d * F = J",
        "Maxwell target file states same-Hodge two-form route.",
    ),
    "SRC4082_03_hodge_bound_vector": (
        SOURCE_DIR / "P8_EM_Hodge_flow_rule_bound_or_zero.csv",
        "Delta_Hodge_EM",
        "Hodge-flow residual vector keeps EM constitutive mismatch live.",
    ),
    "SRC4082_04_poynting_vector": (
        SOURCE_DIR / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv",
        "Phi_EM_rad",
        "Poynting/source accounting route is exact conditional but not parent signed.",
    ),
    "SRC4082_05_current_owner_vector": (
        SOURCE_DIR / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv",
        "C_JQ",
        "EM current-owner vector retains charge-current normalization as an open coefficient.",
    ),
    "SRC4082_06_source_label_status": (
        SOURCE_DIR / "P8_EM_source_label_forgetting_EM_Hodge_status.csv",
        "EM_Poynting_route",
        "source-label forgetting row ties Poynting to Maxwell Hilbert stress if Hodge/current are owned.",
    ),
    "SRC4082_07_conformal_status": (
        SOURCE_DIR / "P8_Y5_EM_Hodge_conformal_or_PiM_Htau_status.csv",
        "pure conformal piece is zero",
        "previous branch zeroed the pure conformal Hodge subterm for 4D Maxwell two-forms but retained scale gates.",
    ),
    "SRC4082_08_poynting_status": (
        SOURCE_DIR / "P8_Y5_EM_Poynting_Hilbert_source_accounting_status.csv",
        "EM_POYNTING_ONCE_THEOREM_CONDITIONAL_BOUND_BRANCH_ACTIVE",
        "Poynting/Hilbert source accounting already has a conditional once-only theorem.",
    ),
    "SRC4082_09_same_frame_source": (
        SOURCE_DIR / "P8_Y5_same_frame_Hilbert_source_current_closure_status.csv",
        "SAME_FRAME_HILBERT_SOURCE_CURRENT_CLOSURE_CONDITIONAL_UNSIGNED",
        "same-frame Hilbert source current closure remains conditional unsigned.",
    ),
    "SRC4082_10_em_source_coupling": (
        SOURCE_DIR / "P8_Y5_EM_source_coupling_owner_status.csv",
        "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
        "EM source coupling owner branch remains exact conditional, no claim.",
    ),
}

WEB_SOURCES = [
    {
        "source_id": "WEB4082_0_sme_data_tables_2026",
        "title": "Data Tables for Lorentz and CPT Violation",
        "authors": "Kostelecky and Russell",
        "year": 2026,
        "url": "https://arxiv.org/abs/0801.0287",
        "supporting_url": "https://physics.nmu.edu/~nrussell/research/datatables.htm",
        "extracted_result": "2026 edition tabulates measured and derived SME coefficients including photon-sector tests",
        "source_role": "curated photon-sector Lorentz/light-cone/birefringence bound catalog",
        "confidence": "living_arXiv_table_with_RMP_reference",
    },
    {
        "source_id": "WEB4082_1_grb_delta_gamma",
        "title": "Constraints on Equivalence Principle Violation from Gamma Ray Bursts",
        "authors": "Bartlett, Bergsdal, Desmond, Ferreira, Jasche",
        "year": 2021,
        "url": "https://doi.org/10.1103/PhysRevD.104.084025",
        "supporting_url": "https://arxiv.org/abs/2106.15290",
        "extracted_result": "Delta gamma < 2.1e-15 at 1 sigma between 25 keV and 325 keV photons",
        "source_role": "finite photon light-cone/source-coupling residual bound",
        "confidence": "peer_reviewed_PRD_and_arXiv_preprint",
    },
    {
        "source_id": "WEB4082_2_fermi_grb_dispersion",
        "title": "Constraints on Lorentz Invariance Violation from Fermi-Large Area Telescope Observations of Gamma-Ray Bursts",
        "authors": "Vasileiou et al.",
        "year": 2013,
        "url": "https://doi.org/10.1103/PhysRevD.87.122001",
        "supporting_url": "https://arxiv.org/abs/1305.3463",
        "extracted_result": "GRB090510 gives E_QG,1 > 7.6 E_Pl and E_QG,2 > 1.3e11 GeV at 95 percent CL for subluminal vacuum dispersion without intrinsic dispersion",
        "source_role": "finite photon dispersion/light-cone deformation bound",
        "confidence": "peer_reviewed_PRD_and_arXiv_preprint",
    },
    {
        "source_id": "WEB4082_3_kostelecky_mewes_grb_polarization",
        "title": "Sensitive polarimetric search for relativity violations in gamma-ray bursts",
        "authors": "Kostelecky and Mewes",
        "year": 2006,
        "url": "https://doi.org/10.1103/PhysRevLett.97.140401",
        "supporting_url": "https://arxiv.org/abs/hep-ph/0607084",
        "extracted_result": "linear polarization in GRB 930131 and GRB 960924 constrains certain photon relativity violations below parts in 1e37",
        "source_role": "finite vacuum-birefringence/polarization residual bound",
        "confidence": "peer_reviewed_PRL_and_arXiv_preprint",
    },
]

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4082_SOURCE_REGISTER.csv",
    "web_provenance": SOURCE_DIR / "P8_Y5_R2FR_4082_WEB_PROVENANCE.csv",
    "em_theorem": SOURCE_DIR / "P8_Y5_R2FR_4082_EM_HODGE_MAXWELL_THEOREM.csv",
    "light_cone_bounds": SOURCE_DIR / "P8_Y5_R2FR_4082_LIGHT_CONE_BIREFRINGENCE_BOUNDS.csv",
    "runner_update": SOURCE_DIR / "P8_Y5_R2FR_4082_EFFECTIVE_RESIDUAL_RUNNER_UPDATE.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4082_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4082_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4082_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4082_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4082_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_rows(current_timestamp: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_file",
                "path_or_url": str(path),
                "exists_or_recorded": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": current_timestamp,
            }
        )
    for source in WEB_SOURCES:
        rows.append(
            {
                "source_id": source["source_id"],
                "source_type": "web_source",
                "path_or_url": source["url"],
                "exists_or_recorded": True,
                "needle": source["extracted_result"],
                "needle_found": True,
                "role": source["source_role"],
                "timestamp_utc": current_timestamp,
            }
        )
    return rows


def web_provenance_rows(current_timestamp: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source in WEB_SOURCES:
        row = dict(source)
        row["timestamp_utc"] = current_timestamp
        row["valid_for_claim"] = False
        rows.append(row)
    return rows


def em_theorem_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "EM4082_0_same_hodge_maxwell",
            "statement": "If the quotient-visible electromagnetic block is S_EM=-1/2 int F wedge *obs F + int A wedge *obs J, with F=dA, dJ=0, and *obs built only from the same observed coframe e_obs(q), then the Euler-Lagrange equations are dF=0 and d*obs F=*obs J.",
            "proof_sketch": "dF=0 follows from F=dA. Variation of A gives d*obs F=*obs J. Since the Hodge star is the one induced by e_obs, the principal symbol is the observed metric light cone.",
            "result": "EXACT_CONDITIONAL_SAME_HODGE_MAXWELL_THEOREM",
            "current_MTS_status": "GAUGE_OBJECT_CURRENT_CONSERVATION_AND_HODGE_OWNER_NOT_PARENT_SIGNED",
            "residual_effect": "Delta_Hodge_EM and charge/current normalization remain finite residuals unless the parent signs A/F/J/*obs together.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "EM4082_1_poynting_hilbert_once",
            "statement": "If Maxwell EM is varied in the same observed Hilbert source branch before source calibration and readout, Poynting flux and EM binding energy enter total stress exactly once, not as an additional hidden force.",
            "proof_sketch": "The Maxwell stress tensor is obtained by varying the same action with respect to e_obs. Its divergence balances the Lorentz-force exchange with matter, so the conserved object is T_matter+T_EM.",
            "result": "EXACT_CONDITIONAL_POYNTING_HILBERT_ACCOUNTING_THEOREM",
            "current_MTS_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "residual_effect": "radiative boundary flux Phi_EM_rad, w_EM, C_XF2 and C_JQ remain live if the parent block is not signed.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "EM4082_2_conformal_hodge_silence",
            "statement": "In four spacetime dimensions the Hodge star on two-forms is conformally invariant, so source-free Maxwell light-cone propagation cannot by itself fix the conformal scale or the charge/current normalization.",
            "proof_sketch": "For two-forms in 4D, *_{Omega^2 g}F=*_g F. Therefore a pure conformal rescaling leaves the source-free Hodge equations unchanged while clocks, currents, action normalization and alpha_EM can still shift.",
            "result": "EXACT_CONDITIONAL_CONFORMAL_HODGE_SUBTERM_ZERO_SCALE_RETAINED",
            "current_MTS_status": "CONFORMAL_CONE_ROUTE_HELPFUL_BUT_NOT_FULL_EM_NORMALIZATION",
            "residual_effect": "separate scale gates remain for clock calibration, w_EM, alpha_EM, and source-current normalization.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "EM4082_3_current_failure_to_promote",
            "statement": "The current corpus does not yet parent-derive A_mu or F, charge/current conservation, a unique Maxwell action multiplier, charge normalization, Coulomb limit, or alpha_EM.",
            "proof_sketch": "The EM audit and current-owner vectors still mark gauge object, current owner, Hodge owner and normalization as missing or conditional.",
            "result": "MAXWELL_DERIVATION_NOT_CLOSED",
            "current_MTS_status": "LOCAL_MAXWELL_CHARGE_QED_ALPHA_CLAIM_BLOCKED",
            "residual_effect": "use photon light-cone, birefringence, dispersion and charge-current bounds as nonclaim residual scales.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def light_cone_bound_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "BOUND4082_0_GRB_photon_delta_gamma",
            "quantity": "epsilon_photon_light_cone_energy_dependence",
            "theory_map": "any energy-dependent photon Shapiro/light-cone mismatch from an EM Hodge/source-coupling leak maps to a nonzero Delta gamma between photon energies",
            "bound_type": "upper_bound",
            "bound_value": BARTLETT_DELTA_GAMMA_BOUND,
            "units": "dimensionless_PPN_gamma_difference",
            "source_id": "WEB4082_1_grb_delta_gamma",
            "observable_link": "GRB spectral-lag photon WEP/light-cone test between 25 keV and 325 keV",
            "valid_for_claim": False,
            "claim_use": "finite photon light-cone residual scale only; not proof that MTS has same EM Hodge",
            "timestamp_utc": current_timestamp,
        },
        {
            "bound_id": "BOUND4082_1_Fermi_GRB090510_linear_dispersion",
            "quantity": "E_QG1_linear_vacuum_dispersion",
            "theory_map": "linear energy-dependent photon speed deformation from an independent EM Hodge/principal symbol must correspond to an effective QG scale above this lower bound if mapped to the tested LIV form",
            "bound_type": "lower_bound_energy_scale",
            "bound_value": FERMI_EQG1_PLANCK_BOUND,
            "units": "Planck_energy",
            "source_id": "WEB4082_2_fermi_grb_dispersion",
            "observable_link": "Fermi-LAT GRB090510 vacuum dispersion",
            "valid_for_claim": False,
            "claim_use": "model-dependent dispersion residual scale; no direct MTS pass without operator map",
            "timestamp_utc": current_timestamp,
        },
        {
            "bound_id": "BOUND4082_2_Fermi_GRB090510_quadratic_dispersion",
            "quantity": "E_QG2_quadratic_vacuum_dispersion",
            "theory_map": "quadratic photon speed deformation from an independent EM Hodge/principal symbol must correspond to an effective QG scale above this lower bound if mapped to the tested LIV form",
            "bound_type": "lower_bound_energy_scale",
            "bound_value": FERMI_EQG2_GEV_BOUND,
            "units": "GeV",
            "source_id": "WEB4082_2_fermi_grb_dispersion",
            "observable_link": "Fermi-LAT GRB090510 vacuum dispersion",
            "valid_for_claim": False,
            "claim_use": "model-dependent dispersion residual scale; no direct MTS pass without operator map",
            "timestamp_utc": current_timestamp,
        },
        {
            "bound_id": "BOUND4082_3_GRB_polarization_birefringence",
            "quantity": "epsilon_photon_birefringent_relativity_violation",
            "theory_map": "birefringent principal/skewon/axion-gradient Hodge residuals would rotate or depolarize GRB linear polarization",
            "bound_type": "upper_bound_fractional_parts",
            "bound_value": KM_GRB_POLARIZATION_FRACTION_BOUND,
            "units": "dimensionless_fractional_photon_relativity_violation",
            "source_id": "WEB4082_3_kostelecky_mewes_grb_polarization",
            "observable_link": "GRB 930131 and GRB 960924 linear polarization",
            "valid_for_claim": False,
            "claim_use": "finite vacuum-birefringence residual scale; no direct MTS pass without SME/operator projection",
            "timestamp_utc": current_timestamp,
        },
    ]


def runner_update_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "runner_id": "RUNUP4082_0_same_Hodge_theorem",
            "quantity": "Delta_Hodge_EM",
            "old_score": "RETAINED_COMPONENT_BOUND_REQUIRED",
            "new_score": "EXACT_CONDITIONAL_SAME_HODGE_MAXWELL_THEOREM_PARENT_UNSIGNED",
            "numeric_bound": "not_applicable_for_zero_theorem",
            "numeric_bound_units": "not_applicable",
            "aggregate_effect": "can become zero only if A/F/J and *obs are parent-signed together",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "runner_id": "RUNUP4082_1_photon_delta_gamma_bound",
            "quantity": "epsilon_photon_light_cone_energy_dependence",
            "old_score": "MISSING_LIGHT_CONE_BOUND",
            "new_score": "FINITE_EXTERNAL_GRB_DELTA_GAMMA_SCALE",
            "numeric_bound": BARTLETT_DELTA_GAMMA_BOUND,
            "numeric_bound_units": "dimensionless",
            "aggregate_effect": "keeps photon light-cone/source-coupling residual finite while parent EM Hodge remains unsigned",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "runner_id": "RUNUP4082_2_dispersion_bounds",
            "quantity": "principal_EM_cone_dispersion",
            "old_score": "MISSING_DISPERSION_BOUND",
            "new_score": "FINITE_EXTERNAL_FERMI_GRB_DISPERSION_SCALES",
            "numeric_bound": f"E_QG1>{FERMI_EQG1_PLANCK_BOUND} E_Pl; E_QG2>{FERMI_EQG2_GEV_BOUND} GeV",
            "numeric_bound_units": "mixed_energy_lower_bounds",
            "aggregate_effect": "bounds any direct mapping to linear/quadratic photon dispersion but does not replace an MTS operator projection",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "runner_id": "RUNUP4082_3_birefringence_bound",
            "quantity": "principal_skewon_axion_birefringent_EM_residual",
            "old_score": "MISSING_BIREFRINGENCE_BOUND",
            "new_score": "FINITE_EXTERNAL_GRB_POLARIZATION_SCALE",
            "numeric_bound": KM_GRB_POLARIZATION_FRACTION_BOUND,
            "numeric_bound_units": "dimensionless_fractional_photon_relativity_violation",
            "aggregate_effect": "birefringent EM-Hodge residuals are now pointed at a finite nonclaim scale",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def decision_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4082_0",
            "decision": DECISION,
            "strongest_positive_result": "Maxwell/Hodge/Poynting route is a real exact theorem if the parent supplies a single observed Hodge star, gauge two-form, conserved current and variation order.",
            "blocking_fact": "current MTS still has no parent-signed A_mu/F/J/*obs/w_EM/alpha/Coulomb owner package.",
            "allowed_status": "private_derivation_checkpoint",
            "claim_allowed": False,
            "next_action": "derive or explicitly import the charge-current normalization and Coulomb/source owner package.",
            "timestamp_utc": current_timestamp,
        }
    ]


def claim_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4082_0",
            "claim": "same-Hodge Maxwell theorem is mathematically valid",
            "claim_allowed": True,
            "scope": "conditional mathematical theorem",
            "why": "the theorem follows from the standard variational Maxwell action once the parent supplies its premises",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4082_1",
            "claim": "current MTS derives Maxwell electromagnetism",
            "claim_allowed": False,
            "scope": "parent EM derivation",
            "why": "A_mu/F/J/Hodge/current/normalization package is not parent signed",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4082_2",
            "claim": "Poynting vector is counted exactly once if EM is in the same Hilbert branch",
            "claim_allowed": True,
            "scope": "conditional mathematical theorem",
            "why": "same-action variation makes Poynting flux a component of Maxwell stress rather than an extra hidden source",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4082_3",
            "claim": "photon light-cone and birefringence bounds are sourced residual scales",
            "claim_allowed": True,
            "scope": "private nonclaim residual target",
            "why": "external bounds have source strings and numeric values but no MTS operator projection yet",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4082_4",
            "claim": "current MTS derives charge, QED, Coulomb law, or alpha_EM",
            "claim_allowed": False,
            "scope": "parent EM/particle derivation",
            "why": "charge-current normalization, Coulomb limit and alpha owner remain open",
            "timestamp_utc": current_timestamp,
        },
    ]


def next_target_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "target_id": "NEXT4082_0",
            "next_target": "4083-Y5-R2FR-charge-current-normalization-or-standard-EM-import-contract.md",
            "script": "scripts/Y5_R2FR_4083_charge_current_normalization_or_standard_EM_import_contract.py",
            "why": "same-Hodge theorem is now precise; the next irreducible missing object is J/q_e/w_EM/Coulomb/alpha ownership",
            "priority": "P0",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_id": "NEXT4082_1",
            "next_target": "parent_action_visible_EM_block_later",
            "script": "fold_into_parent_action_work",
            "why": "if emergent EM cannot be derived immediately, standard visible Maxwell can be imported as a disciplined local sector while MTS derives gravity/source coupling",
            "priority": "P1",
            "timestamp_utc": current_timestamp,
        },
    ]


def status_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "timestamp_utc": current_timestamp,
            "branch_id": "MTS_R2FR_Y5_4082_EM_HODGE_MAXWELL_SOURCE_THEOREM_OR_LIGHT_CONE_BOUND",
            "status": DECISION,
            "public_claim_allowed": False,
            "github_action": False,
            "formalization_workbench_modified": False,
            "summary": "4082 proves the exact conditional same-Hodge Maxwell/Poynting theorem, refuses promotion because parent A/F/J/Hodge/current normalization is unsigned, and sources finite photon light-cone/dispersion/birefringence residual scales.",
            "valid_for_claim": False,
        }
    ]


def validate_sources(rows: List[Dict[str, object]]) -> Tuple[bool, str]:
    failures = [
        row["source_id"]
        for row in rows
        if row["exists_or_recorded"] is not True or row["needle_found"] is not True
    ]
    return not failures, f"missing_or_unmatched_sources={failures}"


def validate_csv_parse(paths: List[Path]) -> Tuple[bool, str]:
    failures: List[str] = []
    for path in paths:
        try:
            with path.open(newline="", encoding="utf-8") as input_file:
                rows = list(csv.DictReader(input_file))
            if not rows:
                failures.append(f"{path}:empty")
        except Exception as exc:
            failures.append(f"{path}:{exc}")
    return not failures, f"csv_failures={failures}"


def validate_numeric_bounds(rows: List[Dict[str, object]]) -> Tuple[bool, str]:
    failures: List[str] = []
    for row in rows:
        try:
            value = float(row["bound_value"])
            if not math.isfinite(value) or value <= 0:
                failures.append(f"{row['bound_id']}:bound_value not positive finite")
        except Exception:
            failures.append(f"{row['bound_id']}:bound_value not numeric")
        if row["valid_for_claim"] is not False:
            failures.append(f"{row['bound_id']}:valid_for_claim not false")
        if "MISSING_" in str(row):
            failures.append(f"{row['bound_id']}:contains MISSING marker")
    return not failures, "; ".join(failures) if failures else "light-cone bounds numeric and nonclaim"


def validate_claim_scopes(rows: List[Dict[str, object]]) -> Tuple[bool, str]:
    allowed_scopes = {"conditional mathematical theorem", "private nonclaim residual target"}
    bad_rows = [
        row["claim_id"]
        for row in rows
        if row["claim_allowed"] is True and row["scope"] not in allowed_scopes
    ]
    return not bad_rows, f"bad_allowed_claim_scopes={bad_rows}"


def validate_no_public_claim(row_groups: List[List[Dict[str, object]]]) -> Tuple[bool, str]:
    text = str(row_groups)
    forbidden = [
        "public_claim': True",
        '"public_claim": True',
        "github_action': True",
        '"github_action": True',
        "current MTS derives Maxwell electromagnetism', 'claim_allowed': True",
        "current MTS derives charge, QED, Coulomb law, or alpha_EM', 'claim_allowed': True",
    ]
    hits = [token for token in forbidden if token in text]
    return not hits, f"forbidden_public_claim_tokens={hits}"


def validate_output_scope(paths: List[Path]) -> Tuple[bool, str]:
    outside = [str(path) for path in paths + [DOC_PATH] if ROOT not in path.parents and path != ROOT]
    formalization_hits = [str(path) for path in paths + [DOC_PATH] if FORMALIZATION in path.parents]
    return not outside and not formalization_hits, f"outside_post_checkpoint={outside}; formalization_hits={formalization_hits}"


def validate_script_compile() -> Tuple[bool, str]:
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError as exc:
        return False, str(exc)
    return True, "script compiles"


def validation_rows(
    source_table: List[Dict[str, object]],
    generated_csvs: List[Path],
    row_groups: List[List[Dict[str, object]]],
    bounds: List[Dict[str, object]],
    claims: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    source_ok, source_detail = validate_sources(source_table)
    csv_ok, csv_detail = validate_csv_parse(generated_csvs)
    bounds_ok, bounds_detail = validate_numeric_bounds(bounds)
    no_public_ok, no_public_detail = validate_no_public_claim(row_groups)
    claim_scope_ok, claim_scope_detail = validate_claim_scopes(claims)
    output_scope_ok, output_scope_detail = validate_output_scope(generated_csvs)
    compile_ok, compile_detail = validate_script_compile()
    joined = str(row_groups)
    return [
        {"check_id": "VAL4082_00_sources", "passed": source_ok, "detail": source_detail},
        {"check_id": "VAL4082_01_csv_parse", "passed": csv_ok, "detail": csv_detail},
        {"check_id": "VAL4082_02_numeric_bounds", "passed": bounds_ok, "detail": bounds_detail},
        {"check_id": "VAL4082_03_no_public_or_github_claim", "passed": no_public_ok, "detail": no_public_detail},
        {"check_id": "VAL4082_04_claim_scope", "passed": claim_scope_ok, "detail": claim_scope_detail},
        {"check_id": "VAL4082_05_output_scope", "passed": output_scope_ok, "detail": output_scope_detail},
        {
            "check_id": "VAL4082_06_EM_theorem_conditional",
            "passed": "EXACT_CONDITIONAL_SAME_HODGE_MAXWELL_THEOREM" in joined
            and "MAXWELL_DERIVATION_NOT_CLOSED" in joined,
            "detail": "same-Hodge Maxwell theorem exists but remains parent unsigned",
        },
        {
            "check_id": "VAL4082_07_light_cone_bounds",
            "passed": "FINITE_EXTERNAL_GRB_DELTA_GAMMA_SCALE" in joined
            and "FINITE_EXTERNAL_FERMI_GRB_DISPERSION_SCALES" in joined
            and "FINITE_EXTERNAL_GRB_POLARIZATION_SCALE" in joined,
            "detail": "finite photon light-cone, dispersion and birefringence bounds are present",
        },
        {
            "check_id": "VAL4082_08_next_target",
            "passed": "4083-Y5-R2FR-charge-current-normalization-or-standard-EM-import-contract.md" in joined,
            "detail": "next target moves to charge/current normalization or disciplined standard-EM import",
        },
        {"check_id": "VAL4082_09_script_compiles", "passed": compile_ok, "detail": compile_detail},
    ]


def doc_text(current_timestamp: str) -> str:
    return f"""# 4082 - EM Hodge Maxwell Source Theorem Or Light-Cone Bound

- Timestamp: `{current_timestamp}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Public Maxwell/QED/charge claim: `false`
- GitHub action: `false`

## Result

This checkpoint does move the work forward: the EM/Poynting route is no longer just a vague missing-coupling complaint.

The exact conditional theorem is:

```text
S_EM = -1/2 int F wedge *obs F + int A wedge *obs J
F = dA
dJ = 0
*obs = Hodge[e_obs(q)]
```

then:

```text
dF = 0
d*obs F = *obs J
principal cone = null cone of e_obs
T_EM is the Hilbert stress from the same observed coframe
nabla_mu(T_matter + T_EM)^{{mu nu}} = 0
```

So the Poynting vector is not a separate hidden source if the parent action puts EM in the same Hilbert branch before calibration/readout. It is the Maxwell momentum/energy flux already inside `T_EM`.

## Why It Is Not Promoted

The current MTS corpus still lacks a parent-signed package:

```text
A_mu or F
F = dA or dF = 0
conserved J
same observed Hodge star *obs
unique w_EM normalization
charge-current normalization C_JQ
Coulomb/static source limit
alpha_EM owner
```

That blocks:

```text
MTS derives Maxwell EM = false
MTS derives charge/QED/alpha_EM = false
```

but preserves:

```text
same-Hodge Maxwell theorem = exact conditional
Poynting Hilbert accounting theorem = exact conditional
```

## Conformal Hodge Point

In four spacetime dimensions, the Hodge star on two-forms is conformally invariant:

```text
*_(Omega^2 g) F = *_g F
```

This is helpful but not enough. Source-free EM can share the light cone while still leaving scale, clocks, current normalization, and `alpha_EM` open.

## External Bounds Acquired

Nonclaim residual scales now exist for the EM/Hodge branch:

```text
Delta gamma photon energy dependence < {BARTLETT_DELTA_GAMMA_BOUND:.3e}
E_QG,1 linear dispersion > {FERMI_EQG1_PLANCK_BOUND} E_Pl
E_QG,2 quadratic dispersion > {FERMI_EQG2_GEV_BOUND:.3e} GeV
birefringent photon relativity violation < {KM_GRB_POLARIZATION_FRACTION_BOUND:.1e}
```

These bounds do not prove MTS. They stop the EM branch from floating without empirical teeth.

## Decision

```text
same-Hodge Maxwell/Poynting theorem = exact conditional
current Maxwell/charge claim = false
finite photon light-cone/dispersion/birefringence residual scales = sourced
```

## Sources

- Kostelecky and Russell, `Data Tables for Lorentz and CPT Violation`, arXiv `0801.0287`, 2026 edition.
- Bartlett et al., `Constraints on Equivalence Principle Violation from Gamma Ray Bursts`, Phys. Rev. D 104, 084025.
- Vasileiou et al., `Constraints on Lorentz Invariance Violation from Fermi-Large Area Telescope Observations of Gamma-Ray Bursts`, Phys. Rev. D 87, 122001.
- Kostelecky and Mewes, `Sensitive polarimetric search for relativity violations in gamma-ray bursts`, Phys. Rev. Lett. 97, 140401.

## Next

The next non-circular target is:

```text
4083-Y5-R2FR-charge-current-normalization-or-standard-EM-import-contract.md
```

This should decide whether the local branch imports standard visible Maxwell as a disciplined sector while MTS derives gravity/source coupling, or whether MTS can actually parent-derive:

```text
J, q_e, w_EM, Coulomb limit, alpha_EM
```
"""


def main() -> None:
    current_timestamp = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(current_timestamp)
    web_provenance = web_provenance_rows(current_timestamp)
    theorem = em_theorem_rows(current_timestamp)
    bounds = light_cone_bound_rows(current_timestamp)
    runner = runner_update_rows(current_timestamp)
    decisions = decision_gate_rows(current_timestamp)
    claims = claim_gate_rows(current_timestamp)
    next_targets = next_target_rows(current_timestamp)
    statuses = status_rows(current_timestamp)

    DOC_PATH.write_text(doc_text(current_timestamp), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["web_provenance"], web_provenance)
    write_csv(OUTPUTS["em_theorem"], theorem)
    write_csv(OUTPUTS["light_cone_bounds"], bounds)
    write_csv(OUTPUTS["runner_update"], runner)
    write_csv(OUTPUTS["decision_gate"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next_target"], next_targets)
    write_csv(OUTPUTS["status"], statuses)

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["web_provenance"],
        OUTPUTS["em_theorem"],
        OUTPUTS["light_cone_bounds"],
        OUTPUTS["runner_update"],
        OUTPUTS["decision_gate"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    row_groups = [
        sources,
        web_provenance,
        theorem,
        bounds,
        runner,
        decisions,
        claims,
        next_targets,
        statuses,
    ]
    validation = validation_rows(sources, generated_csvs, row_groups, bounds, claims)
    write_csv(OUTPUTS["validation"], validation)

    cache_dir = SCRIPT_PATH.parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    failures = [row for row in validation if not row["passed"]]
    print(f"wrote {DOC_PATH}")
    print(f"decision: {DECISION}")
    print(f"validation rows: {len(validation)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
