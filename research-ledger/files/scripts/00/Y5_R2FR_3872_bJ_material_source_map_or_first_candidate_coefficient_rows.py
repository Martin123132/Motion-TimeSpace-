from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3872"
BRANCH = "MTS_R2FR_Y5_BJ_MATERIAL_SOURCE_MAP_OR_FIRST_CANDIDATE_COEFFICIENT_ROWS_3872"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3872-Y5-R2FR-bJ-material-source-map-or-first-candidate-coefficient-rows.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3871_NEXT = OUT / "P8_Y5_R2FR_3871_NEXT_TARGET.csv"
CSV_3871_THEOREM = OUT / "P8_Y5_R2FR_3871_ACTION_MEASURE_OWNER_THEOREM.csv"
CSV_3871_BJ = OUT / "P8_Y5_R2FR_3871_BJ_FIRST_SOURCE_ROW_CONTRACT.csv"
CSV_3868_INPUTS = OUT / "P8_Y5_R2FR_3868_CURRENT_NORMALIZATION_BOUND_INPUT_REQUIREMENTS.csv"
CSV_3868_REDUCED = OUT / "P8_Y5_R2FR_3868_REDUCED_ZG_CORE_ROWS.csv"
CSV_3867_SCHEMA = OUT / "P8_Y5_R2FR_3867_SOURCE_BACKED_INPUT_SCHEMA.csv"
CSV_3867_CANDIDATES = OUT / "P8_Y5_R2FR_3867_SOURCE_BACKED_CANDIDATE_ROWS.csv"
CSV_3863_CHARGE = OUT / "P8_Y5_R2FR_3863_CHARGE_CURRENT_SLOT_AUDIT.csv"
CSV_3863_EM = OUT / "P8_Y5_R2FR_3863_EM_SOURCE_SCALE_BOUND.csv"
CSV_3819_SOURCE = OUT / "P8_Y5_R2FR_3819_FINITE_SOURCE_NORMALIZATION_RESIDUALS.csv"
CSV_3843_QUEUE = OUT / "P8_Y5_R2FR_3843_SOURCE_FILL_QUEUE.csv"
CSV_3829_COEFF = OUT / "P8_Y5_R2FR_3829_SCALAR_COEFFICIENT_OWNER_MAP.csv"
CSV_3837_BETA = OUT / "P8_Y5_R2FR_3837_BETA_BOUND_ROWS.csv"
CSV_1387_FILL = OUT / "P8_Y5_R10_1387_DELTA_W_SOURCE_BETA_FIRST_FILL.csv"
CSV_1052_CLOCK = OUT / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv"
CSV_1052_WEP = OUT / "P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv"
CSV_1052_R10 = OUT / "P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3872_SOURCE_REGISTER.csv",
    "material_map": OUT / "P8_Y5_R2FR_3872_MATERIAL_SOURCE_CLASS_MAP.csv",
    "basis": OUT / "P8_Y5_R2FR_3872_BJ_COEFFICIENT_BASIS.csv",
    "arena_contract": OUT / "P8_Y5_R2FR_3872_ARENA_PROJECTION_CONTRACT.csv",
    "candidate_rows": OUT / "P8_Y5_R2FR_3872_FIRST_CANDIDATE_BJ_COEFFICIENT_ROWS.csv",
    "poynting_bridge": OUT / "P8_Y5_R2FR_3872_POYNTING_SOURCE_BRIDGE.csv",
    "claim_gates": OUT / "P8_Y5_R2FR_3872_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3872_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3872_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3872_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3872_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3872_00_3871_next", CSV_3871_NEXT, "NEXT3871_0", "3871 selected material/source map"),
    ("SRC3872_01_3871_theorem", CSV_3871_THEOREM, "AMT3871_5_verdict", "action-measure owner verdict"),
    ("SRC3872_02_3871_bj", CSV_3871_BJ, "BJS3871_1_Delta_w_A", "first b_J source-row contract"),
    ("SRC3872_03_3868_inputs", CSV_3868_INPUTS, "BIR3868_3_z_Delta_w", "source/current normalization input requirements"),
    ("SRC3872_04_3868_reduced", CSV_3868_REDUCED, "RZG3868_3_newton_local_gr", "reduced source-normalization branch"),
    ("SRC3872_05_3867_schema", CSV_3867_SCHEMA, "SCHEMA3867_5", "projection consistency schema"),
    ("SRC3872_06_3867_candidates", CSV_3867_CANDIDATES, "CAND3867_2_r10_product_law", "source-backed candidate rows"),
    ("SRC3872_07_3863_charge", CSV_3863_CHARGE, "CCA3863_4_EM_binding_source", "EM binding/source slot audit"),
    ("SRC3872_08_3863_em", CSV_3863_EM, "ESB3863_2_EM_source_scale", "EM source-scale envelope"),
    ("SRC3872_09_3819_source", CSV_3819_SOURCE, "R3819_6_total", "Newton/local-GR source-normalization residual"),
    ("SRC3872_10_3843_queue", CSV_3843_QUEUE, "SFQ3843_2", "source normalization / Hilbert measure lock queue"),
    ("SRC3872_11_3829_coeff", CSV_3829_COEFF, "COEFF3829_0_C_t", "local PPN coefficient owner map"),
    ("SRC3872_12_3837_beta", CSV_3837_BETA, "BB3837_1_beta", "integrated beta bound row"),
    ("SRC3872_13_1387_fill", CSV_1387_FILL, "DWB1387_6_first_fill_verdict", "Delta_w/source-beta first-fill pack"),
    ("SRC3872_14_1052_clock", CSV_1052_CLOCK, "ACB1052_1", "clock alpha product bound"),
    ("SRC3872_15_1052_wep", CSV_1052_WEP, "AWP1052_0_alpha_Coulomb", "WEP alpha/Coulomb projection"),
    ("SRC3872_16_1052_r10", CSV_1052_R10, "RAP1052_0_product_law", "R10 product-law projection"),
]

COMPONENT_BASIS = "S_A=(s_m0,s_EM,s_nuc,s_e,s_press,s_rad,s_boundary,s_clock,s_geometry)"
FIRST_ENVELOPE = (
    "b_J,A <= |Delta_w_A|+|D_X ln J_A_measure|+|c_A_pre|+|delta kappa_A|+|z_readout,A|+|K_arena residual|"
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
    rows = []
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
                "claim_use": "nonclaim_material_source_map_and_candidate_coupling_rows",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def material_map_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "MAT3872_0_rest_mass",
            "rest_mass_baryon_lepton",
            "ordinary rest-mass contribution carried by matter fields",
            "s_m0",
            "Hilbert stress of parent-owned matter action",
            "Delta_w_A common mode only; no relative species marker",
            "R3819 source normalization; C_t Newtonian norm",
            "mass source; WEP; Newton; PPN; orbital",
            "COMMON_MODE_CANDIDATE_NOT_PARENT_SIGNED",
        ),
        (
            "MAT3872_1_EM_binding_static",
            "electrostatic_magnetic_binding",
            "Coulomb/magnetic binding and static EM field stress inside material",
            "s_EM",
            "Maxwell/Hilbert stress plus binding contribution to M_H",
            "same parent F2 coefficient and same current owner",
            "3863 EM source-scale; 1052 WEP alpha/Coulomb",
            "WEP; clocks; R10; source mass; local GR",
            "FINITE_COMPONENT_ROW_REQUIRED",
        ),
        (
            "MAT3872_2_nuclear_binding",
            "nuclear_binding_strong_internal",
            "nuclear binding and internal strong-sector mass fraction",
            "s_nuc",
            "effective matter stress after integrating internal modes",
            "no independent nuclear source marker",
            "composition sensitivity vector",
            "WEP; orbital source mass; clocks if transition-sensitive",
            "FINITE_COMPONENT_ROW_REQUIRED",
        ),
        (
            "MAT3872_3_pressure_kinetic",
            "pressure_kinetic_internal_energy",
            "pressure, kinetic, thermal and virial corrections to active density",
            "s_press",
            "Tolman/Hamiltonian active density branch",
            "pressure/binding terms bounded or shown negligible in chosen limit",
            "3819 pressure-binding residual",
            "Newton; PPN; orbital",
            "BOUND_LIMIT_REQUIRED",
        ),
        (
            "MAT3872_4_poynting_radiation",
            "radiation_poynting_boundary_flux",
            "field momentum and energy flux through the source worldtube",
            "s_rad+s_boundary",
            "EM stress plus boundary flux integral",
            "closed stationary worldtube or explicit flux term",
            "3863 EM binding/Poynting source slot",
            "source mass; local GR; orbital; EM",
            "POYNTING_BRIDGE_OPEN_BUT_LOCALIZED",
        ),
        (
            "MAT3872_5_clock_transition",
            "clock_transition_readout",
            "transition-energy sensitivity used as test/readout not bulk source mass",
            "s_clock",
            "frequency readout functional",
            "same Xhat/readout normalization as source branch",
            "1052 clock alpha product ledger",
            "clock drift; alpha variation",
            "PRODUCT_BOUND_AVAILABLE_MTS_TAU_MISSING",
        ),
        (
            "MAT3872_6_R10_lab_materials",
            "short_range_source_test_materials",
            "coated plates/test masses and Yukawa profile material response",
            "s_geometry+s_EM+s_nuc",
            "finite-range source/test density convolution",
            "lambda profile, beta_source, beta_test, K_R10 all share one convention",
            "1052 R10 product law; 3867 R10 candidate",
            "R10; fifth-force alpha(lambda)",
            "PROFILE_KERNEL_REQUIRED",
        ),
        (
            "MAT3872_7_orbital_body",
            "orbital_bulk_source",
            "macroscopic source whose observed mu=GM may hide source normalization",
            "s_m0+s_press+s_boundary",
            "selected active mass/worldtube current",
            "anti-circularity guard: do not fit away G_ref*M_H",
            "3819 GM anti-circularity residual",
            "Newtonian limit; orbital; PPN",
            "SOURCE_LEDGER_REQUIRED",
        ),
        (
            "MAT3872_8_vacuum_exterior",
            "local_vacuum_exterior",
            "no ordinary matter source, but boundary/non-Hilbert tails may remain",
            "s_boundary+s_geometry",
            "exterior field equation and boundary data",
            "compact boundary silence and no extra scalar/local dof",
            "3837 beta and 3843 local source queue",
            "PPN gamma/beta; local GR",
            "BOUNDARY_AND_DOF_GATE_OPEN",
        ),
    ]
    return [
        {
            "material_id": row_id,
            "class": cls,
            "definition": definition,
            "basis_component": component,
            "source_owner_candidate": owner,
            "zero_or_bound_condition": condition,
            "evidence_anchor": evidence,
            "test_arenas": arenas,
            "current_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, cls, definition, component, owner, condition, evidence, arenas, status in rows
    ]


def basis_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "BAS3872_0_basis",
            "material sensitivity vector",
            COMPONENT_BASIS,
            "finite class basis for source/test composition and readout",
            "prevents arbitrary per-test coupling knobs",
            "BASIS_DECLARED_NONCLAIM",
        ),
        (
            "BAS3872_1_Delta_w",
            "Delta_w_A",
            "Delta_w_A = theta_m0*s_m0^A + theta_EM*s_EM^A + theta_nuc*s_nuc^A + theta_press*s_press^A + theta_rad*s_rad^A + theta_bdy*s_boundary^A + theta_clock*s_clock^A",
            "relative pre-variation action/source weight",
            "theta_i must be zero by parent owner or bounded from source-backed material rows",
            "FINITE_LINEAR_BASIS_ROW",
        ),
        (
            "BAS3872_2_beta_w",
            "beta_w_A",
            "beta_w_A = D_Xhat Delta_w_A = sum_i beta_i*s_i^A + sum_i theta_i*D_Xhat(s_i^A)",
            "field-space derivative of source/test action weight",
            "composition derivatives vanish only for fixed material branch",
            "FINITE_DERIVATIVE_BASIS_ROW",
        ),
        (
            "BAS3872_3_measure",
            "D_X ln J_A_measure",
            "D_X ln J_A_measure = sum_i j_i*s_i^A + j_readout,A",
            "species/source measure Jacobian residual",
            "zero if parent measure is species-blind and readout-stable",
            "FINITE_MEASURE_ROW",
        ),
        (
            "BAS3872_4_current",
            "c_A_pre",
            "c_A_pre = sum_i c_i*s_i^A + c_boundary,A",
            "pre-variation current/source coefficient",
            "ill-typed under 3870 grammar unless real current/source selector remains",
            "FINITE_CURRENT_SLOT_ROW",
        ),
        (
            "BAS3872_5_selector",
            "delta kappa_A",
            "delta kappa_A = sum_i kappa_i*s_i^A + kappa_geometry,A",
            "active-source selector deviation",
            "zero only if selected Hilbert/Hamiltonian source is parent-owned",
            "FINITE_SELECTOR_ROW",
        ),
        (
            "BAS3872_6_envelope",
            "b_J,A",
            FIRST_ENVELOPE,
            "first finite source-coupling residual envelope",
            "all terms share material class and arena projection convention",
            "FIRST_BJ_ENVELOPE_NONCLAIM",
        ),
    ]
    return [
        {
            "basis_id": row_id,
            "quantity": quantity,
            "formula": formula,
            "meaning": meaning,
            "promotion_requirement": requirement,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, quantity, formula, meaning, requirement, status in rows
    ]


def arena_contract_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "APC3872_0_WEP",
            "MICROSCOPE_WEP",
            "eta_ST <= |K_WEP|*|beta_source(S)|*|beta_test(A)-beta_test(B)| + b_J,A+B terms",
            "source body class plus two test-material sensitivity vectors",
            "eta bound and composition deltas exist; beta_source/tau/domain still missing",
            "DO_NOT_SCORE_YET",
        ),
        (
            "APC3872_1_R10",
            "R10_short_range",
            "alpha_MTS(lambda)=K_R10(lambda;rho_s,rho_t,profile)*beta_source(lambda)*beta_test(lambda)+epsilon_tail(lambda)",
            "source/test density profile and lambda convention",
            "product law exists; real promoted bound curve and parent beta/kernel missing",
            "DO_NOT_SCORE_YET",
        ),
        (
            "APC3872_2_clock",
            "atomic_clock",
            "d ln(nu_1/nu_2)/dX = (S_clock,1-S_clock,2).beta + z_readout_clock",
            "transition readout vector, not bulk source mass",
            "clock product bound exists; MTS tau/readout coefficient missing",
            "PRODUCT_BOUND_ONLY",
        ),
        (
            "APC3872_3_Newton_PPN",
            "Newton_PPN_local_GR",
            "delta C_t and beta/gamma residuals <= R_source_normalization_total + b_J + EM/Poynting/source terms",
            "active source density/worldtube selector plus exterior readout",
            "3819/3829/3837 provide formulas; source ledger and EH2 vertex not closed",
            "LOCAL_GR_NOT_CLAIMED",
        ),
        (
            "APC3872_4_orbital",
            "orbital_systems",
            "delta ln mu = delta ln G_ref + delta ln M_H_source + selector/worldtube/boundary residual",
            "bulk source mass and observed GM anti-circularity",
            "needs independent source ledger before using orbital fits as theory evidence",
            "ANTI_CIRCULARITY_GUARD",
        ),
        (
            "APC3872_5_EM",
            "EM_source_and_Poynting",
            "Delta T_EM_source <= Hodge/F2/current normalization + boundary Poynting flux + EM binding source scale",
            "Maxwell stress, charge current and boundary flux under one parent source owner",
            "Poynting route is retained as explicit source term, not ignored",
            "SOURCE_BRIDGE_OPEN",
        ),
    ]
    return [
        {
            "arena_id": row_id,
            "arena": arena,
            "projection_formula": formula,
            "required_domain_lock": domain,
            "source_backing_status": backing,
            "runner_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, arena, formula, domain, backing, status in rows
    ]


def candidate_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "CAND3872_0_Delta_w_A",
            "Delta_w_A",
            "theta vector",
            "Delta_w_A = theta · S_A",
            "material sensitivity vector from 3872 map",
            "missing parent theta_i zero proof or numeric upper bounds",
            "READY_FOR_COMPONENT_FILL_NONCLAIM",
        ),
        (
            "CAND3872_1_beta_w_source",
            "beta_w_source",
            "beta source vector",
            "beta_w_source(S)=beta · S_source + theta · D_X S_source",
            "selected source class and Xhat branch",
            "missing beta_i and fixed-composition proof",
            "READY_FOR_SOURCE_BETA_FILL_NONCLAIM",
        ),
        (
            "CAND3872_2_beta_w_test",
            "beta_w_test",
            "beta test vector",
            "beta_w_test(T)=beta · S_test + theta · D_X S_test",
            "test material or clock transition vector",
            "missing beta_i and readout-domain lock",
            "READY_FOR_TEST_BETA_FILL_NONCLAIM",
        ),
        (
            "CAND3872_3_J_measure",
            "J_A_measure",
            "measure vector",
            "D_X ln J_A_measure = j · S_A + j_readout,A",
            "parent measure or finite species/source Jacobian row",
            "missing species-blind measure descent",
            "READY_FOR_MEASURE_FILL_NONCLAIM",
        ),
        (
            "CAND3872_4_c_A_pre",
            "c_A_pre",
            "pre-current vector",
            "c_A_pre = c · S_A + c_boundary,A",
            "typed current/source slot after 3870 grammar",
            "missing zero theorem or finite current-slot coefficient",
            "READY_FOR_CURRENT_SLOT_FILL_NONCLAIM",
        ),
        (
            "CAND3872_5_kappa_A",
            "kappa_A",
            "selector vector",
            "delta kappa_A = kappa · S_A + kappa_geometry,A",
            "active source selector / Hilbert-Hamiltonian map",
            "missing selected-source owner or finite selector row",
            "READY_FOR_SELECTOR_FILL_NONCLAIM",
        ),
        (
            "CAND3872_6_K_WEP",
            "K_WEP",
            "arena kernel",
            "K_WEP maps source beta and test material differential into eta_ST",
            "MICROSCOPE material/source/orbit/readout convention",
            "missing shared source/test domain lock",
            "KERNEL_ROW_REQUIRED_NONCLAIM",
        ),
        (
            "CAND3872_7_K_R10",
            "K_R10(lambda)",
            "arena kernel",
            "K_R10(lambda)=profile convolution of source/test densities and finite-range propagator",
            "R10 lambda/material/profile convention",
            "missing promoted bound curve and parent beta/kernel coefficients",
            "KERNEL_ROW_REQUIRED_NONCLAIM",
        ),
        (
            "CAND3872_8_Poynting_boundary",
            "Phi_EM_boundary",
            "boundary flux",
            "epsilon_Poynting = |int_dt int_boundary S_EM·n dA|/(M_ref c^2)",
            "closed stationary source worldtube or explicit flux accounting",
            "missing worldtube closure/flux bound",
            "POYNTING_SOURCE_ROW_REQUIRED_NONCLAIM",
        ),
        (
            "CAND3872_9_total_bJ",
            "b_J,A",
            "first envelope",
            FIRST_ENVELOPE,
            "one material class plus one arena projection contract",
            "missing coefficients and kernels; no scoring",
            "EXECUTABLE_ENVELOPE_NONCLAIM",
        ),
    ]
    return [
        {
            "candidate_id": row_id,
            "quantity": quantity,
            "coefficient_family": family,
            "candidate_formula": formula,
            "source_or_material_input": material_input,
            "missing_for_claim": missing,
            "status": status,
            "numeric_value": "MISSING_PARENT_OR_SOURCE_BACKED_VALUE",
            "units": "dimensionless_or_declared_arena_units",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, quantity, family, formula, material_input, missing, status in rows
    ]


def poynting_bridge_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "POY3872_0_do_not_ignore",
            "Poynting flux is not a side issue: it is an EM source/boundary contribution to active mass/source normalization.",
            "If the source worldtube is stationary and closed, net flux can vanish; otherwise it must enter Phi_EM_boundary.",
            "retained in CAND3872_8 and APC3872_5",
            "POYNTING_RETAINED",
        ),
        (
            "POY3872_1_zero_route",
            "Phi_EM_boundary=0",
            "requires closed stationary source worldtube, no radiative leakage, and boundary/reference improvement silence",
            "would remove a source-mass and local-GR residual, but not F2/current normalization",
            "EXACT_CONDITIONAL_ZERO_NOT_SIGNED",
        ),
        (
            "POY3872_2_bound_route",
            "epsilon_Poynting = |int_dt int_boundary S_EM·n dA|/(M_ref c^2)",
            "source-backed bound can be inserted per arena/source class if zero route fails",
            "feeds orbital/source mass/local-GR envelopes",
            "FINITE_BOUND_ROUTE_READY",
        ),
    ]
    return [
        {
            "bridge_id": row_id,
            "statement": statement,
            "condition_or_formula": formula,
            "effect_on_framework": effect,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, statement, formula, effect, status in rows
    ]


def claim_gate_rows(
    sources: list[dict[str, object]],
    material: list[dict[str, object]],
    basis: list[dict[str, object]],
    arena: list[dict[str, object]],
    candidates: list[dict[str, object]],
    poynting: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    all_sources = all(row["exists"] and row["needle_found"] for row in sources)
    required_quantities = {"Delta_w_A", "beta_w_source", "beta_w_test", "J_A_measure", "c_A_pre", "kappa_A", "b_J,A"}
    candidate_quantities = {row["quantity"] for row in candidates}
    required_arenas = {"MICROSCOPE_WEP", "R10_short_range", "atomic_clock", "Newton_PPN_local_GR", "orbital_systems", "EM_source_and_Poynting"}
    arena_names = {row["arena"] for row in arena}
    rows = [
        ("G3872_0_sources", "all cited source rows resolved", "PASS" if all_sources else "FAIL", f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved"),
        ("G3872_1_material_map", "material/source classes declared", "PASS" if len(material) >= 8 else "FAIL", f"{len(material)} classes"),
        ("G3872_2_basis", "finite coefficient basis declared", "PASS" if required_quantities.issubset(candidate_quantities) else "FAIL", ",".join(sorted(candidate_quantities))),
        ("G3872_3_arenas", "major local arenas have projection contracts", "PASS" if required_arenas.issubset(arena_names) else "FAIL", ",".join(sorted(arena_names))),
        ("G3872_4_poynting", "Poynting/EM boundary route retained", "PASS" if any("Poynting" in row["statement"] for row in poynting) else "FAIL", "explicit Poynting bridge rows written"),
        ("G3872_5_no_numeric_fabrication", "no row fabricates a numeric parent coefficient", "PASS" if all(row["numeric_value"] == "MISSING_PARENT_OR_SOURCE_BACKED_VALUE" for row in candidates) else "FAIL", "candidate values are symbolic/nonclaim"),
        ("G3872_6_no_claim", "all generated rows remain nonclaim", "PASS", "valid_for_claim=false throughout"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "detail": detail,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, status, detail in rows
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "DEC3872_0",
            "replace free coupling talk with material sensitivity vectors",
            "Delta_w/beta/c/kappa are now finite class-basis rows instead of open-ended knobs",
        ),
        (
            "DEC3872_1",
            "retain Poynting vector as a source/boundary bridge",
            "EM field momentum/flux can affect source normalization unless stationary boundary silence is proved",
        ),
        (
            "DEC3872_2",
            "do not score WEP/R10/clocks/PPN yet",
            "real bounds exist in some arenas but parent beta/kernel/current coefficients are not numeric or theorem-zero",
        ),
        (
            "DEC3872_3",
            "next route is first coefficient fill attempt",
            "the finite basis is now declared; progress requires theta/beta/c/kappa/K rows or a theorem-zero for one family",
        ),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "because": because,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for decision_id, decision, because in rows
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3872_0",
            "target_checkpoint": "3873-Y5-R2FR-first-coefficient-fill-theta-beta-or-poynting-zero.md",
            "script": "scripts/Y5_R2FR_3873_first_coefficient_fill_theta_beta_or_poynting_zero.py",
            "objective": "try to zero or source-fill one coefficient family in the 3872 material basis, prioritizing Poynting boundary silence, Delta_w theta-vector commonness, or WEP/R10 beta-source rows",
            "why_next": "3872 has converted the coupling problem into finite coefficient families; the next leap is to close one family, not add another abstract audit",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "result": "MATERIAL_SOURCE_MAP_AND_FIRST_CANDIDATE_BJ_ROWS_BUILT_NONCLAIM",
            "claim_allowed": False,
            "short_summary": "3872 maps source coupling onto finite material sensitivity classes, keeps Poynting as an explicit EM source/boundary term, and stages first candidate rows for Delta_w, beta_source/test, J_measure, c_A_pre, kappa_A and arena kernels.",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        values = []
        for col in columns:
            value = str(row.get(col, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    material: list[dict[str, object]],
    basis: list[dict[str, object]],
    arena: list[dict[str, object]],
    candidates: list[dict[str, object]],
    poynting: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3872 — b_J Material/Source Map or First Candidate Coefficient Rows

Generated: `{timestamp}`

## Result

3872 stops treating “the coupling” as one foggy missing object. It maps the live source-coupling residual into a finite material/source basis:

`{COMPONENT_BASIS}`

The first executable nonclaim envelope is:

`{FIRST_ENVELOPE}`

This is not a local-GR, WEP, R10, clock, orbital, or EM pass. It is the first finite coefficient scaffold that lets the next checkpoint try to actually close or fill one coupling family.

## Source Register

Resolved `{resolved}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Material / Source Class Map

{markdown_table(material, ["material_id", "class", "basis_component", "zero_or_bound_condition", "test_arenas", "current_status"])}

## Coefficient Basis

{markdown_table(basis, ["basis_id", "quantity", "formula", "promotion_requirement", "status"])}

## Arena Projection Contract

{markdown_table(arena, ["arena_id", "arena", "projection_formula", "required_domain_lock", "runner_status"])}

## First Candidate Coefficient Rows

{markdown_table(candidates, ["candidate_id", "quantity", "candidate_formula", "missing_for_claim", "status"])}

## Poynting / EM Source Bridge

{markdown_table(poynting, ["bridge_id", "condition_or_formula", "effect_on_framework", "status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "detail", "claim_allowed"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "because"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

3872 moves the framework forward by replacing an unconstrained coupling gap with a finite source/material coefficient basis. The most important practical gain is that Poynting/EM binding is now explicitly carried as a source-normalization bridge instead of being silently ignored. The grim bit remains: no coefficient family is parent-zeroed or numerically sourced yet, so no local test is claimable. The next serious leap is to close one family: `theta_i` commonness, `beta_i` source/test rows, `c_A/kappa_A` slot silence, `K_arena`, or Poynting boundary zero.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    start = "<!-- BEGIN 3872 MATERIAL SOURCE MAP -->"
    end = "<!-- END 3872 MATERIAL SOURCE MAP -->"
    block = f"""{start}

## 3872 — Material/source basis for the coupling problem

`3872` turns the live source-coupling problem into a finite material sensitivity basis rather than a generic missing coupling. It declares `S_A=(s_m0,s_EM,s_nuc,s_e,s_press,s_rad,s_boundary,s_clock,s_geometry)` and stages first candidate rows for `Delta_w_A`, `beta_w_source`, `beta_w_test`, `D_X ln J_A_measure`, `c_A_pre`, `kappa_A`, and arena kernels. It also keeps the Poynting vector route alive explicitly: EM field momentum/flux is a source/boundary term that can vanish only under closed stationary worldtube and boundary-silence conditions, otherwise it must be bounded.

Result: no WEP/R10/clock/PPN/orbital/local-GR claim, but the coupling problem is now finite and executable. Next gate: `3873`, try to close or source-fill one coefficient family rather than adding another abstract audit.

Generated outputs:
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3872_MATERIAL_SOURCE_CLASS_MAP.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3872_BJ_COEFFICIENT_BASIS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3872_FIRST_CANDIDATE_BJ_COEFFICIENT_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3872_POYNTING_SOURCE_BRIDGE.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3872_VALIDATION.csv`

<!-- Generated by 3872 at {timestamp} -->
{end}
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else "# Local GR Coupling Spine Current State\n"
    if start in existing and end in existing:
        before = existing.split(start)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        new_text = f"{before}\n\n{block}\n\n{after}".rstrip() + "\n"
    else:
        new_text = existing.rstrip() + "\n\n" + block + "\n"
    SPINE_PATH.write_text(new_text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    material: list[dict[str, object]],
    basis: list[dict[str, object]],
    arena: list[dict[str, object]],
    candidates: list[dict[str, object]],
    poynting: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    checks: list[tuple[str, str, bool, str]] = []
    all_sources = all(row["exists"] and row["needle_found"] for row in sources)
    checks.append(("VAL3872_0_sources", "all cited source paths exist and needles are found", all_sources, f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved"))
    checks.append(("VAL3872_1_material_count", "material/source class map is nontrivial", len(material) >= 8, f"{len(material)} material/source classes"))
    material_classes = {row["class"] for row in material}
    checks.append(("VAL3872_2_poynting_class", "Poynting/radiation class exists", "radiation_poynting_boundary_flux" in material_classes, ",".join(sorted(material_classes))))
    candidate_quantities = {row["quantity"] for row in candidates}
    required_quantities = {"Delta_w_A", "beta_w_source", "beta_w_test", "J_A_measure", "c_A_pre", "kappa_A", "K_WEP", "K_R10(lambda)", "Phi_EM_boundary", "b_J,A"}
    checks.append(("VAL3872_3_candidate_quantities", "candidate rows cover required coefficient families", required_quantities.issubset(candidate_quantities), ",".join(sorted(candidate_quantities))))
    arena_names = {row["arena"] for row in arena}
    required_arenas = {"MICROSCOPE_WEP", "R10_short_range", "atomic_clock", "Newton_PPN_local_GR", "orbital_systems", "EM_source_and_Poynting"}
    checks.append(("VAL3872_4_arena_contracts", "arena projection contracts cover local tests", required_arenas.issubset(arena_names), ",".join(sorted(arena_names))))
    checks.append(("VAL3872_5_basis_formula", "finite basis contains theta and beta decomposition", any("theta · S_A" in row["candidate_formula"] for row in candidates) and any("beta · S_source" in row["candidate_formula"] for row in candidates), "theta/beta formulas present"))
    checks.append(("VAL3872_6_poynting_bridge", "Poynting bridge has zero and bound routes", any(row["bridge_id"] == "POY3872_1_zero_route" for row in poynting) and any(row["bridge_id"] == "POY3872_2_bound_route" for row in poynting), f"{len(poynting)} Poynting rows"))
    checks.append(("VAL3872_7_no_numeric_fabrication", "candidate numeric values remain placeholders", all(row["numeric_value"] == "MISSING_PARENT_OR_SOURCE_BACKED_VALUE" for row in candidates), "no fabricated numbers"))
    checks.append(("VAL3872_8_no_claim_rows", "all generated analytical rows are nonclaim", all(str(row.get("valid_for_claim")) == "False" for collection in [material, basis, arena, candidates, poynting] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3872_9_gates", "claim gates include blocked/no-claim discipline", any(row["gate_id"] == "G3872_6_no_claim" and row["status"] == "PASS" for row in gates), "no-claim gate present"))
    checks.append(("VAL3872_10_doc", "markdown checkpoint exists with expected bottom line", DOC_PATH.exists() and "3872 moves the framework forward" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3872_11_spine", "spine updated with 3872 block", SPINE_PATH.exists() and "BEGIN 3872 MATERIAL SOURCE MAP" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key not in {"validation"}]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            count = len(read_csv_rows(path))
            parse_details.append(f"{path.name}:{count}")
        except Exception as exc:  # pragma: no cover - validation detail
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3872_12_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [path for path in FWB.rglob("*3872*") if path.is_file()]
    checks.append(("VAL3872_13_formalization_untouched", "no generated 3872 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3872_14_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3872_15_claim_gates_no_claim", "no claim gate allows a claim", all(str(row["claim_allowed"]) == "False" for row in gates), "claim_allowed=false"))
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    material = material_map_rows(timestamp)
    basis = basis_rows(timestamp)
    arena = arena_contract_rows(timestamp)
    candidates = candidate_rows(timestamp)
    poynting = poynting_bridge_rows(timestamp)
    gates = claim_gate_rows(sources, material, basis, arena, candidates, poynting, timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["material_map"], material)
    write_csv(OUTPUTS["basis"], basis)
    write_csv(OUTPUTS["arena_contract"], arena)
    write_csv(OUTPUTS["candidate_rows"], candidates)
    write_csv(OUTPUTS["poynting_bridge"], poynting)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, material, basis, arena, candidates, poynting, gates, decisions, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, material, basis, arena, candidates, poynting, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_MATERIAL_SOURCE_MAP_FIRST_COEFFICIENT_ROWS")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
