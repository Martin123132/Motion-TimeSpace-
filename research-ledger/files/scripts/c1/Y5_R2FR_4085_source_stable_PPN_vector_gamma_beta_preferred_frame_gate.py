from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4085-Y5-R2FR-source-stable-PPN-vector-gamma-beta-preferred-frame-gate.md"

DECISION = "SOURCE_STABLE_PPN_VECTOR_DERIVED_CONDITIONAL_WITH_REAL_BOUNDS_LOCAL_GR_STILL_PARENT_UNSIGNED"
TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4085_00_4084_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4084_NEXT_TARGET.csv",
        "4085-Y5-R2FR-source-stable-PPN-vector-gamma-beta-preferred-frame-gate.md",
        "4084 explicitly selects the source-stable PPN vector as the next local-GR gate.",
    ),
    "SRC4085_01_4084_poisson": (
        SOURCE_DIR / "P8_Y5_R2FR_4084_NEWTON_POISSON_GATE_THEOREM.csv",
        "Delta_PPN_abs remains active",
        "4084 proves only the conditional Newton/Poisson coefficient and leaves PPN active.",
    ),
    "SRC4085_02_4084_denominator": (
        SOURCE_DIR / "P8_Y5_R2FR_4084_SOURCE_DENOMINATOR_GATE.csv",
        "never backfill M_H from GM_orb/G_ref",
        "The same Hilbert source denominator must be kept fixed through PPN order.",
    ),
    "SRC4085_03_4018_ppn_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4018_SECOND_ORDER_PPN_STABILITY_THEOREM.csv",
        "EXACT_CONDITIONAL_GAMMA_THEOREM",
        "4018 supplies the gamma/beta/preferred-frame/conservation conditional theorem.",
    ),
    "SRC4085_04_4018_source_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_4018_PPN_SOURCE_STABILITY_AUDIT.csv",
        "same observed coframe/frame/gauge",
        "4018 records which PPN source-stability clauses remain parent unsigned.",
    ),
    "SRC4085_05_4048_zero_vector": (
        SOURCE_DIR / "P8_Y5_R2FR_4048_CONDITIONAL_PPN_ZERO_VECTOR.csv",
        "Delta_PPN_abs",
        "4048 carries the conditional PPN zero vector selected by the parent-packet route.",
    ),
    "SRC4085_06_3967_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_3967_EMPIRICAL_BOUND_INTERFACE.csv",
        "BND3967_0_gamma",
        "3967 already staged gamma/beta/preferred-frame empirical bound interfaces.",
    ),
    "SRC4085_07_4077_gamma_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_4077_FIRST_NUMERIC_P0_BOUND.csv",
        "BOUND4077_0_cassini_gamma",
        "4077 records the first numeric Cassini gamma bound for the residual runner.",
    ),
    "SRC4085_08_4078_alpha_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4078_SECOND_NUMERIC_P0_BOUND.csv",
        "BOUND4078_0_alpha1_preferred_frame",
        "4078 records preferred-frame alpha1/alpha2 numeric bound rows.",
    ),
    "SRC4085_09_3997_gdot": (
        SOURCE_DIR / "P8_Y5_R2FR_3997_GDOT_PPN_BOUND_VECTOR.csv",
        "Gdot",
        "3997 stages time-varying G/coupling as a local-PPN residual component.",
    ),
}


WEB_SOURCES = [
    {
        "source_id": "WEB4085_0_will_lrr_2014_table4",
        "title": "The Confrontation between General Relativity and Experiment",
        "authors": "Clifford M. Will",
        "year": "2014",
        "url": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
        "source_role": "PPN formalism and current-limit table for gamma, beta, xi, alpha_i, zeta_i",
        "extracted_result": "Table 4: gamma-1 2.3e-5; beta-1 8e-5; xi 4e-9; alpha1 1e-4 and 4e-5; alpha2 2e-9; alpha3 4e-20; zeta1 2e-2; zeta2 4e-5; zeta3 1e-8; zeta4 not independent.",
        "line_hint": "opened lines 137-167",
        "confidence": "review_table_source",
        "timestamp_utc": TIMESTAMP,
    },
    {
        "source_id": "WEB4085_1_cassini_nature_2003",
        "title": "A test of general relativity using radio links with the Cassini spacecraft",
        "authors": "B. Bertotti, L. Iess, P. Tortora",
        "year": "2003",
        "url": "https://doi.org/10.1038/nature01997",
        "supporting_url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
        "source_role": "Cassini Shapiro delay gamma measurement",
        "extracted_result": "gamma = 1 + (2.1 +/- 2.3)e-5",
        "line_hint": "Will review lines 124-126 and PubMed abstract",
        "confidence": "primary_nature_measurement_plus_pubmed_index",
        "timestamp_utc": TIMESTAMP,
    },
]


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def parse_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_string(value: bool) -> str:
    return "True" if value else "False"


def source_register_rows() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_checkpoint_csv",
                "path_or_url": str(path),
                "needle": needle,
                "role": role,
                "exists": bool_string(path.exists()),
                "valid_for_claim": "False",
                "timestamp_utc": TIMESTAMP,
            }
        )
    for row in WEB_SOURCES:
        rows.append(
            {
                "source_id": row["source_id"],
                "source_type": "web_literature",
                "path_or_url": row["url"],
                "needle": row["extracted_result"],
                "role": row["source_role"],
                "exists": "web_checked",
                "valid_for_claim": "False",
                "timestamp_utc": TIMESTAMP,
            }
        )
    rows.append(
        {
            "source_id": "SRC4085_10_script",
            "source_type": "generator_script",
            "path_or_url": str(SCRIPT_PATH),
            "needle": SCRIPT_PATH.name,
            "role": "Reproducible generator for 4085 CSV/doc outputs.",
            "exists": bool_string(SCRIPT_PATH.exists()),
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def theorem_rows() -> List[dict]:
    return [
        {
            "theorem_id": "PPN4085_0_fixed_U_source_denominator",
            "claim_piece": "PPN potential source fixed before higher-order readout",
            "statement": "After 4084 the Newtonian potential entering PPN must be U=G_ref*M_H/r with M_H=int rho_H dV_obs sourced by the parent Hilbert/Hamiltonian charge. It may not be redefined from orbital GM at PPN order.",
            "derivation_or_proof_sketch": "4084 fixed the Poisson coefficient and anti-laundering denominator. PPN gamma and beta are then read as curvature/nonlinear coefficients relative to the same U; changing U later would erase the meaning of gamma-1 and beta-1.",
            "formula": "U := G_ref*M_H/r; Delta_orb := GM_orb - G_ref*M_H is output-only",
            "result": "EXACT_CONDITIONAL_FIXED_SOURCE_DENOMINATOR_FOR_PPN",
            "current_MTS_status": "SOURCE_DENOMINATOR_PARENT_UNSIGNED_BUT_LOCKED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "PPN4085_1_gamma_same_branch_zero",
            "claim_piece": "gamma minus one",
            "statement": "If the local reduced metric operator is EH/EC-only through O(U), the observed coframe/readout is the same for g_00 and g_ij, and no R11/q_loc/projector spatial stress survives, then gamma-1=0 in the fixed-source PPN gauge.",
            "derivation_or_proof_sketch": "In the EH weak-field system with one Hilbert source and one observed metric branch, the scalar and spatial curvature potentials obey the same source equation. Therefore Psi=Phi and the PPN spatial-curvature coefficient gamma is one.",
            "formula": "g_ij=delta_ij*(1+2*gamma*U/c^2)+O(c^-4); EH same-branch => Psi=Phi => gamma-1=0",
            "result": "EXACT_CONDITIONAL_GAMMA_THEOREM_SOURCE_STABLE",
            "current_MTS_status": "EH_OPERATOR_READOUT_R11_SILENCE_PARENT_UNSIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "PPN4085_2_beta_second_order_zero",
            "claim_piece": "beta minus one",
            "statement": "If the EH nonlinear completion is the only O(U^2) operator and the same Hilbert source denominator survives source-current, boundary, q_loc, R11 and readout projections, then beta-1=0.",
            "derivation_or_proof_sketch": "With A_source fixed by the Newtonian term, beta_eff=B_source/A_source^2. EH nonlinearity gives B_source=A_source^2 in the standard PPN gauge; any parent source prefactor or second operator appears as a noncancellable beta residual.",
            "formula": "beta_eff=B_source/A_source^2; EH same-source branch => B_source=A_source^2 => beta-1=0",
            "result": "EXACT_CONDITIONAL_BETA_THEOREM_SOURCE_STABLE",
            "current_MTS_status": "SECOND_ORDER_SOURCE_CURRENT_AND_BOUNDARY_GATES_UNSIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "PPN4085_3_preferred_frame_zero",
            "claim_piece": "alpha1 alpha2 alpha3 xi",
            "statement": "If no independent local vector, domain, coframe, memory or quotient-representative marker survives the observed local projection through PPN order, then alpha1=alpha2=alpha3=xi=0.",
            "derivation_or_proof_sketch": "Preferred-frame and preferred-location PPN parameters require a surviving local structure beyond the metric and Hilbert source. The quotient-invariant local branch must either prove those structures descend silently or pay the alpha_i/xi residual.",
            "formula": "V_extra^mu=0 and Xi_extra=0 => alpha1=alpha2=alpha3=xi=0",
            "result": "EXACT_CONDITIONAL_PREFERRED_FRAME_SILENCE_THEOREM",
            "current_MTS_status": "LOCAL_VECTOR_DOMAIN_COFAME_MEMORY_SILENCE_PARENT_UNSIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "PPN4085_4_conservation_zero",
            "claim_piece": "zeta_i conservation parameters",
            "statement": "If the total Hilbert stress used by the observed metric branch is covariantly conserved by the same Bianchi identity, and no hidden source-current leak remains, then zeta1=zeta2=zeta3=0 while zeta4 remains non-independent in the Will table convention.",
            "derivation_or_proof_sketch": "The zeta sector scores momentum/conservation anomalies. Same-branch EH plus closed total Hilbert stress kills anomalous self-acceleration/conservation terms; zeta4 is not treated as an independent scored local-GR gate here.",
            "formula": "nabla_mu T_H^{mu nu}=0 and no hidden source leak => zeta1=zeta2=zeta3=0; zeta4: not independent",
            "result": "EXACT_CONDITIONAL_CONSERVATION_PPN_THEOREM",
            "current_MTS_status": "BIANCHI_SOURCE_CURRENT_CLOSURE_PARENT_UNSIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "PPN4085_5_no_cancellation_firewall",
            "claim_piece": "absolute PPN residual vector",
            "statement": "The local-GR score is an absolute residual vector. No gamma, beta, alpha_i, xi, zeta_i or Gdot component may be cancelled against another component or absorbed into measured orbital GM.",
            "derivation_or_proof_sketch": "A same-score comparison with GR requires fixed source normalization and separate observed PPN components. Otherwise the branch wins by gauge/bookkeeping rather than by local reduction.",
            "formula": "Delta_PPN_abs_4085=sum_j |R_j| with fixed U=G_ref*M_H/r",
            "result": "ANTI_TUNING_ANTI_ORBITAL_LAUNDERING_GUARD",
            "current_MTS_status": "GUARD_LOCKED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "PPN4085_6_current_failure_to_promote",
            "claim_piece": "claim discipline",
            "statement": "4085 improves the local-GR route from loose missingness to an exact conditional PPN theorem with real bounds, but cannot promote an MTS local-GR claim until the parent EH/source/readout/no-extra-R11 clauses are signed.",
            "derivation_or_proof_sketch": "The mathematical implication is now explicit. The remaining work is not vibes: either prove the parent branch enforces the antecedents, or compute the finite residuals and compare them to the sourced bounds.",
            "formula": "claim_local_GR := all(parent_clauses_signed) and all(|R_j|<=bound_j)",
            "result": "NONCLAIM_CONDITIONAL_LOCAL_GR_GATE_WITH_REAL_PPN_BOUNDS",
            "current_MTS_status": "LOCAL_GR_FALSE_PARENT_UNSIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def bound_rows() -> List[dict]:
    return [
        {
            "bound_id": "BND4085_0_gamma_cassini",
            "observable": "gamma_minus_1",
            "bound_value": "2.3e-5",
            "central_value": "2.1e-5",
            "units": "dimensionless",
            "bound_type": "one_sigma_table_limit",
            "source_id": "WEB4085_0_will_lrr_2014_table4; WEB4085_1_cassini_nature_2003",
            "source_path_or_url": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html; https://doi.org/10.1038/nature01997",
            "extraction_method": "Will Table 4 plus Cassini primary measurement",
            "row_valid_as_bound": "True",
            "valid_for_MTS_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "BND4085_1_beta_perihelion",
            "observable": "beta_minus_1",
            "bound_value": "8.0e-5",
            "central_value": "",
            "units": "dimensionless",
            "bound_type": "current_limit_table",
            "source_id": "WEB4085_0_will_lrr_2014_table4",
            "source_path_or_url": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
            "extraction_method": "Will Table 4 beta-1 perihelion shift row",
            "row_valid_as_bound": "True",
            "valid_for_MTS_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "BND4085_2_alpha1_llr",
            "observable": "alpha1",
            "bound_value": "1.0e-4",
            "central_value": "",
            "units": "dimensionless",
            "bound_type": "current_limit_table",
            "source_id": "WEB4085_0_will_lrr_2014_table4",
            "source_path_or_url": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
            "extraction_method": "Will Table 4 alpha1 lunar laser ranging row",
            "row_valid_as_bound": "True",
            "valid_for_MTS_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "BND4085_3_alpha1_pulsar_companion",
            "observable": "alpha1",
            "bound_value": "4.0e-5",
            "central_value": "",
            "units": "dimensionless",
            "bound_type": "stronger_companion_limit_table",
            "source_id": "WEB4085_0_will_lrr_2014_table4",
            "source_path_or_url": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
            "extraction_method": "Will Table 4 PSR J1738+0333 alpha1 row",
            "row_valid_as_bound": "True",
            "valid_for_MTS_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "BND4085_4_alpha2",
            "observable": "alpha2",
            "bound_value": "2.0e-9",
            "central_value": "",
            "units": "dimensionless",
            "bound_type": "current_limit_table",
            "source_id": "WEB4085_0_will_lrr_2014_table4",
            "source_path_or_url": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
            "extraction_method": "Will Table 4 alpha2 spin-precession row",
            "row_valid_as_bound": "True",
            "valid_for_MTS_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "BND4085_5_alpha3",
            "observable": "alpha3",
            "bound_value": "4.0e-20",
            "central_value": "",
            "units": "dimensionless",
            "bound_type": "current_limit_table",
            "source_id": "WEB4085_0_will_lrr_2014_table4",
            "source_path_or_url": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
            "extraction_method": "Will Table 4 alpha3 pulsar acceleration row",
            "row_valid_as_bound": "True",
            "valid_for_MTS_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "BND4085_6_xi",
            "observable": "xi",
            "bound_value": "4.0e-9",
            "central_value": "",
            "units": "dimensionless",
            "bound_type": "current_limit_table",
            "source_id": "WEB4085_0_will_lrr_2014_table4",
            "source_path_or_url": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
            "extraction_method": "Will Table 4 xi spin-precession row",
            "row_valid_as_bound": "True",
            "valid_for_MTS_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "BND4085_7_zeta1",
            "observable": "zeta1",
            "bound_value": "2.0e-2",
            "central_value": "",
            "units": "dimensionless",
            "bound_type": "combined_ppn_bound",
            "source_id": "WEB4085_0_will_lrr_2014_table4",
            "source_path_or_url": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
            "extraction_method": "Will Table 4 zeta1 combined PPN bounds row",
            "row_valid_as_bound": "True",
            "valid_for_MTS_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "BND4085_8_zeta2",
            "observable": "zeta2",
            "bound_value": "4.0e-5",
            "central_value": "",
            "units": "dimensionless",
            "bound_type": "binary_acceleration_bound",
            "source_id": "WEB4085_0_will_lrr_2014_table4",
            "source_path_or_url": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
            "extraction_method": "Will Table 4 zeta2 binary-acceleration row",
            "row_valid_as_bound": "True",
            "valid_for_MTS_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "BND4085_9_zeta3",
            "observable": "zeta3",
            "bound_value": "1.0e-8",
            "central_value": "",
            "units": "dimensionless",
            "bound_type": "newton_third_law_lunar_bound",
            "source_id": "WEB4085_0_will_lrr_2014_table4",
            "source_path_or_url": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
            "extraction_method": "Will Table 4 zeta3 Newton-third-law row",
            "row_valid_as_bound": "True",
            "valid_for_MTS_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "BND4085_10_gdot_over_g_lunar",
            "observable": "Gdot_over_G",
            "bound_value": "1.3e-12",
            "central_value": "4.0e-13",
            "units": "yr^-1",
            "bound_type": "conservative_llr_envelope_from_4084",
            "source_id": "SRC4085_09_3997_gdot",
            "source_path_or_url": str(SOURCE_DIR / "P8_Y5_R2FR_3997_GDOT_PPN_BOUND_VECTOR.csv"),
            "extraction_method": "Local 3997/4084 staged lunar-laser-ranging Gdot residual scale",
            "row_valid_as_bound": "True",
            "valid_for_MTS_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def stability_gate_rows() -> List[dict]:
    return [
        {
            "gate_id": "GATE4085_0_gamma",
            "observable": "gamma_minus_1",
            "residual_expression": "|delta_gamma_EH| + |delta_gamma_R11| + |delta_gamma_readout| + |delta_gamma_projector|",
            "required_bound": "2.3e-5",
            "units": "dimensionless",
            "pass_condition": "all parent clauses sign zero or finite residual sum <= bound",
            "current_status": "BLOCKED_PARENT_EH_READOUT_R11_UNSIGNED",
            "claim_allowed": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "GATE4085_1_beta",
            "observable": "beta_minus_1",
            "residual_expression": "|delta_beta_source| + |delta_beta_R11| + |delta_beta_q_loc| + |delta_beta_boundary| + |delta_beta_readout|",
            "required_bound": "8.0e-5",
            "units": "dimensionless",
            "pass_condition": "same source denominator through O(U^2) and finite residual sum <= bound",
            "current_status": "BLOCKED_SECOND_ORDER_SOURCE_CURRENT_UNSIGNED",
            "claim_allowed": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "GATE4085_2_preferred_frame",
            "observable": "alpha1_alpha2_alpha3_xi",
            "residual_expression": "|alpha1| + |alpha2| + |alpha3| + |xi| from surviving local vector/domain/coframe/memory markers",
            "required_bound": "min component bounds: alpha1 4.0e-5; alpha2 2.0e-9; alpha3 4.0e-20; xi 4.0e-9",
            "units": "dimensionless",
            "pass_condition": "prove no independent local preferred-frame/location marker or compute every component below bound",
            "current_status": "BLOCKED_LOCAL_VECTOR_DOMAIN_SILENCE_UNSIGNED",
            "claim_allowed": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "GATE4085_3_conservation",
            "observable": "zeta1_zeta2_zeta3",
            "residual_expression": "|zeta1| + |zeta2| + |zeta3| from hidden source-current/conservation leaks",
            "required_bound": "zeta1 2.0e-2; zeta2 4.0e-5; zeta3 1.0e-8",
            "units": "dimensionless",
            "pass_condition": "same Bianchi/Hilbert-current conservation branch or finite component bounds",
            "current_status": "BLOCKED_BIANCHI_SOURCE_CURRENT_CLOSURE_UNSIGNED",
            "claim_allowed": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "GATE4085_4_zeta4_note",
            "observable": "zeta4",
            "residual_expression": "not independently scored in Will Table 4 convention",
            "required_bound": "not_independent",
            "units": "dimensionless",
            "pass_condition": "do not fabricate an independent zeta4 numeric bound",
            "current_status": "TABLE_GUARD_LOCKED",
            "claim_allowed": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "GATE4085_5_gdot",
            "observable": "Gdot_over_G",
            "residual_expression": "|partial_t G_eff/G_eff| from source-coupling or kappa drift",
            "required_bound": "1.3e-12 yr^-1 conservative local staged envelope",
            "units": "yr^-1",
            "pass_condition": "prove constant local kappa/G branch or compute drift below bound",
            "current_status": "BLOCKED_PARENT_CONSTANT_COUPLING_SIGNATURE_UNSIGNED",
            "claim_allowed": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "GATE4085_6_master",
            "observable": "Delta_PPN_abs_4085",
            "residual_expression": "sum of absolute gamma, beta, preferred-frame, conservation and Gdot residual components after fixed-source normalization",
            "required_bound": "componentwise bounds; no cancellation scoring",
            "units": "mixed_component_vector",
            "pass_condition": "every component individually zero or individually below sourced bound",
            "current_status": "BLOCKED_NOT_LOCAL_GR_CLAIM",
            "claim_allowed": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def runner_update_rows() -> List[dict]:
    return [
        {
            "update_id": "RUN4085_0_fixed_denominator",
            "runner_change": "Any local PPN comparator must lock U=G_ref*M_H/r from 4084 before evaluating gamma or beta.",
            "failure_mode": "If M_H is inferred from orbital GM, mark ORBITAL_GM_LAUNDERING_BLOCKED.",
            "output_file": "P8_Y5_R2FR_4085_PPN_STABILITY_GATE.csv",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "update_id": "RUN4085_1_componentwise_bounds",
            "runner_change": "Use sourced component bounds for gamma, beta, alpha_i, xi, zeta1-3 and Gdot/G; do not use a single total chi-style score.",
            "failure_mode": "If any component lacks a numeric prediction or theorem-zero proof, leave local-GR claim false.",
            "output_file": "P8_Y5_R2FR_4085_PPN_BOUND_TABLE.csv",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "update_id": "RUN4085_2_zeta4_guard",
            "runner_change": "Treat zeta4 as not independent under the selected Will table convention; do not fabricate a fake numeric zeta4 bound.",
            "failure_mode": "If a future source chooses an independent zeta4 convention, require a fresh source row and explicit convention switch.",
            "output_file": "P8_Y5_R2FR_4085_PPN_STABILITY_GATE.csv",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def decision_rows() -> List[dict]:
    return [
        {
            "decision_id": "DEC4085_0_main",
            "decision": DECISION,
            "meaning": "The local-GR branch now has an exact conditional source-stable PPN theorem and sourced empirical component bounds, but not a parent-owned proof that MTS satisfies the theorem antecedents.",
            "claim_status": "PRIVATE_NONCLAIM",
            "next_required_move": "Prove parent EH/operator/no-extra-R11 branch, or compute the non-EH/R11 finite residual projections against the 4085 bounds.",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4085_1_scorekeeping",
            "decision": "MAYWEATHER_ROUTE_ALLOWED_COMPONENTWISE_NOT_TAUTological",
            "meaning": "MTS does not need to smash every bound; matching GR-shaped scores is valuable if it is achieved by derivation, not by reusing fitted orbital GM or cancellations.",
            "claim_status": "DISCIPLINE_RULE",
            "next_required_move": "Keep each component separate and compare any baseline theory/runner failure symmetrically.",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def claim_gate_rows() -> List[dict]:
    return [
        {
            "claim_id": "CLAIM4085_0_local_GR",
            "claim": "MTS reduces to local GR through PPN order",
            "allowed": "False",
            "why_not": "EH/EC observed operator, same-frame coframe/readout, source-current closure, no-extra-R11/q_loc/projector stress and preferred-frame silence are not parent-signed.",
            "minimum_unlock": "Parent action proves all theorem antecedents or finite residuals are computed and pass every sourced bound.",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4085_1_Newton_only",
            "claim": "MTS has a conditional Newton/Poisson bridge",
            "allowed": "conditional_private_only",
            "why_not": "4084 derives the coefficient only if the EH/same-source/source-denominator premises are accepted.",
            "minimum_unlock": "Parent source denominator and observed EH branch signature.",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4085_2_public",
            "claim": "Public claim or GitHub promotion from 4085",
            "allowed": "False",
            "why_not": "4085 is a private derivation/bound checkpoint, not a completed local-GR proof.",
            "minimum_unlock": "Separate publication-facing writeup after parent signatures and empirical runner pass.",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            "target_id": "NEXT4085_0",
            "next_target": "4086-Y5-R2FR-parent-EH-operator-signature-or-nonEH-R11-projection.md",
            "script": "scripts/Y5_R2FR_4086_parent_EH_operator_signature_or_nonEH_R11_projection.py",
            "why": "4085 makes PPN scoring explicit. The next decisive move is to prove the parent action really reduces to EH/EC with no extra R11/q_loc/projector stress, or calculate those residual projections.",
            "priority": "P0",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "target_id": "NEXT4085_1",
            "next_target": "PPN_baseline_runner_symmetry",
            "script": "defer_until_nonEH_projection_exists",
            "why": "When a numeric residual exists, compare MTS and standard baseline failures symmetrically rather than treating MTS as guilty by default.",
            "priority": "P1",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            "checkpoint": "4085",
            "status": "private_nonclaim_checkpoint_complete",
            "decision": DECISION,
            "public_claim": "False",
            "github_action": "False",
            "formalization_workbench_modified_by_script": "False",
            "timestamp_utc": TIMESTAMP,
        }
    ]


def validation_rows(output_paths: Iterable[Path], bounds: List[dict], theorem: List[dict]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "check": check,
                "passed": bool_string(passed),
                "detail": detail,
                "timestamp_utc": TIMESTAMP,
            }
        )

    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        exists = path.exists()
        contains = exists and needle in read_text(path)
        add(
            f"VAL4085_SRC_{source_id}",
            "local source exists and contains needle",
            bool(exists and contains),
            f"{path} | needle={needle} | role={role}",
        )

    for path in output_paths:
        rows = parse_csv(path)
        add(
            f"VAL4085_CSV_{path.stem}",
            "generated CSV parses and is non-empty",
            bool(rows),
            f"{path} rows={len(rows)}",
        )

    numeric_bounds_ok = True
    bad_bounds: List[str] = []
    for row in bounds:
        if row.get("row_valid_as_bound") == "True":
            try:
                if float(row["bound_value"]) <= 0.0:
                    raise ValueError("nonpositive")
            except Exception:
                numeric_bounds_ok = False
                bad_bounds.append(row["bound_id"])
    add(
        "VAL4085_BOUNDS_POSITIVE",
        "all claim-relevant empirical bound rows are positive numeric values",
        numeric_bounds_ok,
        "bad_bounds=" + ",".join(bad_bounds) if bad_bounds else "all bound_value fields positive",
    )

    required_observables = {
        "gamma_minus_1",
        "beta_minus_1",
        "alpha1",
        "alpha2",
        "alpha3",
        "xi",
        "zeta1",
        "zeta2",
        "zeta3",
        "Gdot_over_G",
    }
    present = {row["observable"] for row in bounds}
    add(
        "VAL4085_REQUIRED_OBSERVABLES",
        "required PPN observables have source-backed rows",
        required_observables.issubset(present),
        f"missing={sorted(required_observables - present)}",
    )

    theorem_results = {row["result"] for row in theorem}
    required_results = {
        "EXACT_CONDITIONAL_GAMMA_THEOREM_SOURCE_STABLE",
        "EXACT_CONDITIONAL_BETA_THEOREM_SOURCE_STABLE",
        "ANTI_TUNING_ANTI_ORBITAL_LAUNDERING_GUARD",
    }
    add(
        "VAL4085_THEOREM_CORE",
        "gamma theorem, beta theorem and no-cancellation guard are present",
        required_results.issubset(theorem_results),
        f"missing={sorted(required_results - theorem_results)}",
    )

    outputs_inside_post_checkpoint = all(is_under(path, ROOT) for path in output_paths) and is_under(DOC_PATH, ROOT)
    outputs_outside_formalization = all(not is_under(path, FORMALIZATION) for path in output_paths) and not is_under(DOC_PATH, FORMALIZATION)
    add(
        "VAL4085_SCOPE",
        "outputs stay in post-checkpoint-work and not formalization-workbench",
        bool(outputs_inside_post_checkpoint and outputs_outside_formalization),
        f"doc={DOC_PATH}; csv_count={len(list(output_paths))}",
    )

    no_claim = all(row.get("valid_for_claim", "False") != "True" for row in theorem)
    no_claim = no_claim and all(row.get("valid_for_MTS_claim", "False") != "True" for row in bounds)
    no_claim = no_claim and all(row.get("claim_allowed", "False") != "True" for row in stability_gate_rows())
    add(
        "VAL4085_NO_PUBLIC_CLAIM",
        "4085 stays private nonclaim",
        no_claim,
        "local-GR claim remains false until parent signatures or finite residual pass",
    )

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
        compile_detail = "py_compile passed"
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4085_SCRIPT_COMPILES", "generator script compiles", compile_ok, compile_detail)

    return checks


def write_doc() -> None:
    DOC_PATH.write_text(
        f"""# 4085 - Source-Stable PPN Vector Gamma Beta Preferred Frame Gate

- Timestamp: `{TIMESTAMP}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Public local-GR claim: `false`
- GitHub action: `false`

## Result

4084 gave the conditional Newton/Poisson coefficient. 4085 pushes one rung higher: the same source denominator is now carried into the PPN vector.

The fixed potential is:

```text
U = G_ref M_H / r
M_H = int rho_H dV_obs
Delta_orb = GM_orb - G_ref M_H
```

So gamma, beta and the preferred-frame/conservation terms cannot be won by redefining the mass from an orbital readout.

## Conditional PPN Theorem

If the parent branch gives:

```text
EH/EC observed metric operator
same observed coframe/readout for g_00 and g_ij
same Hilbert source denominator through O(U^2)
no extra R11/q_loc/projector spatial stress
no independent local vector/domain/coframe/memory marker
Bianchi-closed total Hilbert stress/source current
```

then:

```text
gamma - 1 = 0
beta - 1 = 0
alpha1 = alpha2 = alpha3 = 0
xi = 0
zeta1 = zeta2 = zeta3 = 0
Gdot/G = 0
```

This is a real forward move: the PPN target is no longer vague. The theorem has exact antecedents and a componentwise empirical scorecard.

## Real Bound Rows Added

The 4085 bound table now includes:

```text
|gamma-1| <= 2.3e-5
|beta-1| <= 8.0e-5
|alpha1| <= 1.0e-4, with stronger companion row 4.0e-5
|alpha2| <= 2.0e-9
|alpha3| <= 4.0e-20
|xi| <= 4.0e-9
|zeta1| <= 2.0e-2
|zeta2| <= 4.0e-5
|zeta3| <= 1.0e-8
|Gdot/G| <= 1.3e-12 yr^-1 staged conservative envelope
```

`zeta4` is explicitly not treated as an independent bound in the selected Will Table 4 convention.

## What Improved

This checkpoint closes the “just circling missingness” failure mode for PPN: the missing clauses are now theorem antecedents with hard consequences. The next job is not to list them again; it is to prove the parent action enforces them or compute the residual vector.

## What Remains Unsigned

```text
parent EH/EC operator signature
same-frame observed coframe/readout map
Pi_M/H_tau/Hilbert source denominator equality through O(U^2)
no-extra R11/q_loc/projector spatial stress
preferred-frame/domain/memory silence
Bianchi/source-current closure
constant local coupling/Gdot branch
```

## Decision

```text
source-stable PPN theorem = exact conditional
empirical PPN bounds = source-backed
local GR claim = still false
next gate = parent EH operator signature or non-EH/R11 projection
```

## Sources

- Clifford M. Will, *The Confrontation between General Relativity and Experiment*, Living Reviews in Relativity, Table 4.
- Bertotti, Iess and Tortora, *A test of general relativity using radio links with the Cassini spacecraft*, Nature 425, 374-376, DOI `10.1038/nature01997`.

## Next

```text
4086-Y5-R2FR-parent-EH-operator-signature-or-nonEH-R11-projection.md
```

That is the clean route of attack: either prove the parent really gives the EH same-source branch, or force the extra MTS operators to show their PPN-size residuals in the open.
""",
        encoding="utf-8",
    )


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    source_register = source_register_rows()
    web_provenance = WEB_SOURCES
    theorem = theorem_rows()
    bounds = bound_rows()
    stability = stability_gate_rows()
    runner_update = runner_update_rows()
    decision = decision_rows()
    claim = claim_gate_rows()
    next_target = next_target_rows()
    status = status_rows()

    outputs = {
        "P8_Y5_R2FR_4085_SOURCE_REGISTER.csv": source_register,
        "P8_Y5_R2FR_4085_WEB_PROVENANCE.csv": web_provenance,
        "P8_Y5_R2FR_4085_SOURCE_STABLE_PPN_THEOREM.csv": theorem,
        "P8_Y5_R2FR_4085_PPN_BOUND_TABLE.csv": bounds,
        "P8_Y5_R2FR_4085_PPN_STABILITY_GATE.csv": stability,
        "P8_Y5_R2FR_4085_EFFECTIVE_RESIDUAL_RUNNER_UPDATE.csv": runner_update,
        "P8_Y5_R2FR_4085_DECISION_GATE.csv": decision,
        "P8_Y5_R2FR_4085_CLAIM_GATE.csv": claim,
        "P8_Y5_R2FR_4085_NEXT_TARGET.csv": next_target,
        "P8_Y5_R2FR_4085_STATUS.csv": status,
    }

    output_paths: List[Path] = []
    for name, rows in outputs.items():
        path = SOURCE_DIR / name
        write_csv(path, rows)
        output_paths.append(path)

    write_doc()

    validation = validation_rows(output_paths, bounds, theorem)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4085_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    shutil.rmtree(SCRIPT_PATH.parent / "__pycache__", ignore_errors=True)

    failures = [row for row in validation if row["passed"] != "True"]
    if failures:
        for failure in failures:
            print(f"VALIDATION_FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)

    print(f"4085 complete: {DECISION}")
    print(f"doc: {DOC_PATH}")
    print(f"csv_dir: {SOURCE_DIR}")
    print(f"validation: {validation_path}")


if __name__ == "__main__":
    main()
