from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3339-Y5-R2FR-parent-source-coupling-decomposition-under-AX1090.md"

SOURCES = [
    {
        "source_id": "SRC3339_0_3338_doc",
        "path": ROOT / "3338-Y5-R2FR-PPN-projector-patch-geometry-source-contract-under-AX1090.md",
        "role": "3338 handoff for PPN projector, patch scale, and next coupling target",
    },
    {
        "source_id": "SRC3339_1_3338_contact",
        "path": OUT / "P8_Y5_R2FR_3338_CONTACT_UNIVERSALITY_CONTRACT.csv",
        "role": "contact universality branches",
    },
    {
        "source_id": "SRC3339_2_3338_acquisition",
        "path": OUT / "P8_Y5_R2FR_3338_SOURCE_ACQUISITION_ROWS.csv",
        "role": "ell_s, ell_c, contact tensor, and spectral-tail missing inputs",
    },
    {
        "source_id": "SRC3339_3_3293_local_gr_coupling",
        "path": OUT / "P8_Y5_R2FR_3293_LOCAL_GR_MATTER_COUPLING_REDUCTION.csv",
        "role": "prior local-GR matter coupling reduction rows",
    },
    {
        "source_id": "SRC3339_4_2783_wep_owner",
        "path": OUT / "P8_Y5_R2FR_2783_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv",
        "role": "prior parent WEP coupling owner theorem attempt",
    },
    {
        "source_id": "SRC3339_5_2577_worldtube",
        "path": OUT / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_WORLDTUBE_HILBERT_COUPLING_SELECTOR_THEOREM.csv",
        "role": "worldtube/Hilbert source selector and coupling baseline",
    },
    {
        "source_id": "SRC3339_6_2577_implications",
        "path": OUT / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_NEWTON_GR_IMPLICATIONS.csv",
        "role": "Newton/local-GR implications of source-selector coupling closure",
    },
    {
        "source_id": "SRC3339_7_3117_em_priority",
        "path": OUT / "P8_Y5_R2FR_3117_EM_COUPLING_OWNER_ALPHA_PRIORITY.csv",
        "role": "EM alpha/current/Hodge coupling owner split",
    },
    {
        "source_id": "SRC3339_8_3337_contact",
        "path": OUT / "P8_Y5_R2FR_3337_CONTACT_THEOREM.csv",
        "role": "contact zero/derivative scaling theorem",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3339_SOURCE_REGISTER.csv",
    "decomposition": OUT / "P8_Y5_R2FR_3339_COUPLING_DECOMPOSITION_THEOREM.csv",
    "absorption": OUT / "P8_Y5_R2FR_3339_MEASURED_G_ABSORPTION_THEOREM.csv",
    "residuals": OUT / "P8_Y5_R2FR_3339_RESIDUAL_CHANNEL_VECTOR.csv",
    "kernel": OUT / "P8_Y5_R2FR_3339_KERNEL_CONTACT_SCALE_OWNER.csv",
    "em": OUT / "P8_Y5_R2FR_3339_MAXWELL_EM_STRESS_COUPLING_ROUTE.csv",
    "requirements": OUT / "P8_Y5_R2FR_3339_PARENT_SIGNATURE_REQUIREMENTS.csv",
    "gates": OUT / "P8_Y5_R2FR_3339_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3339_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3339_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3339_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()
B_GAMMA = 2.3e-5
F_COMP = 0.30
B_COMP = F_COMP * B_GAMMA


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1800) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: compact(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def sha256_prefix(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()[:16]


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    result: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            try:
                stat = item.stat()
            except OSError:
                continue
            result[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return result


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        rows.append(
            {
                "source_id": source["source_id"],
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "sha256_prefix": sha256_prefix(path),
                "role": source["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def decomposition_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "CDEC3339_0_parent_current_definition",
            "statement": "define the parent source current by J_A^{mu nu}:=(2/sqrt(-g_obs)) delta S_matter_A/delta g_obs_{mu nu}, with all ordinary sectors varied against the same observed metric/coframe",
            "derivation": "A Hilbert stress/current is the unique object that the local metric perturbation can couple to without adding a post-variation species selector.",
            "zero_condition": "all matter sectors use the same g_obs/coframe, action measure, and variation rule",
            "residual_if_failed": "species-dependent source selector or non-Hilbert current",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CDEC3339_1_common_mode_split",
            "statement": "split the total source current as J^{mu nu}=kappa_* T^{mu nu}+Delta J^{mu nu}",
            "derivation": "Choose kappa_* from the Newtonian T00/Poisson slot; the common mode kappa_*T is measured-G calibration, while Delta J is the physical residual source coupling.",
            "zero_condition": "Delta J^{mu nu}=0 up to boundary/improvement terms and scale-suppressed derivative contacts",
            "residual_if_failed": "PPN/WEP/clock/EM residual channels receive P[Delta J]",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CDEC3339_2_irreducible_channel_projection",
            "statement": "project Delta J into trace/common, traceless-metric, species, spin/antisymmetric, EM-Hodge, derivative/contact, and boundary channels",
            "derivation": "After the Newtonian common mode is fixed, only non-common tensor structure can affect gamma, beta, WEP, clocks, EM propagation, or orbital residuals.",
            "zero_condition": "all non-common projections vanish or are bounded below the arena threshold",
            "residual_if_failed": "local-GR branch becomes an explicit residual-vector branch rather than a theorem-zero branch",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CDEC3339_3_bianchi_conservation_guard",
            "statement": "the local GR branch requires nabla_mu Delta J^{mu nu}=0 or a signed compensating field equation",
            "derivation": "The Einstein/PPN left side is divergence-constrained by the Bianchi identity; an unbalanced source residual is a fifth-force or nonconservation channel, not GR.",
            "zero_condition": "parent diffeomorphism invariance plus no external source selector gives nabla_mu T^{mu nu}=0 and no unbalanced Delta J",
            "residual_if_failed": "Bianchi/conservation violation must be routed to clock, WEP, orbital, or boundary tests",
            "valid_for_claim": "false",
        },
    ]


def absorption_rows() -> list[dict[str, Any]]:
    return [
        {
            "absorption_id": "GABS3339_0_measured_G_absorbs_common_mode",
            "claim": "a single universal common mode kappa_* multiplying the total Hilbert stress is not a PPN anomaly after measured-G calibration",
            "formula": "kappa_* T^{00} -> measured G_N rho in the Newtonian Poisson slot",
            "derivation": "Local Newtonian experiments fix the product kappa_* times source normalization; a pure common rescaling is the definition of the calibrated Newtonian slot.",
            "claim_gate": "allowed only if the same kappa_* multiplies matter, EM stress, pressure/stress, and clock sectors",
            "valid_for_claim": "false",
        },
        {
            "absorption_id": "GABS3339_1_relative_weights_cannot_hide",
            "claim": "species-relative weights w_A cannot be absorbed into one G_N",
            "formula": "J^{mu nu}=kappa_* sum_A (1+eta_A)T_A^{mu nu}; eta_A-eta_B survives WEP/source-composition projections",
            "derivation": "A single measured G can calibrate one common coefficient, not independent weights for different source/test compositions.",
            "claim_gate": "requires eta_A=0 for all ordinary sectors or finite WEP/source-composition bounds",
            "valid_for_claim": "false",
        },
        {
            "absorption_id": "GABS3339_2_tensor_ratio_cannot_hide",
            "claim": "different temporal/spatial/trace couplings cannot be hidden inside Newtonian G",
            "formula": "Delta J_TL^{ij}:=J^{ij}-kappa_*T^{ij} and Delta J_tracefree feed gamma/beta/stress residuals",
            "derivation": "G_N fixes mostly the slow-motion T00 source; gamma and beta test how the same source curves spatial and nonlinear metric components.",
            "claim_gate": "requires tensor-ratio equality or explicit PPN response bound",
            "valid_for_claim": "false",
        },
        {
            "absorption_id": "GABS3339_3_boundary_improvement_silence",
            "claim": "improvement currents can be harmless only if they are exact boundary terms with zero exterior flux/readout",
            "formula": "Delta J^{mu nu}=nabla_lambda B^{lambda mu nu}, with P_PPN Delta J=0 on the exterior comparison patch",
            "derivation": "Divergence/improvement terms can change local representatives without changing the exterior Hilbert charge only when their boundary projection vanishes.",
            "claim_gate": "requires source worldtube, boundary, and readout projector to be fixed before fitting",
            "valid_for_claim": "false",
        },
    ]


def residual_channel_rows() -> list[dict[str, Any]]:
    return [
        {
            "channel_id": "RES3339_0_common_trace",
            "projection": "P_common[Delta J]",
            "zero_route": "absorbed into measured G_N if universal across all sectors",
            "observable_risk": "none after calibration if exactly common",
            "bound_formula": "not scored separately unless Dln(kappa_*) or source normalization varies",
            "status": "CONDITIONAL_ZERO_ROUTE",
            "valid_for_claim": "false",
        },
        {
            "channel_id": "RES3339_1_tensor_anisotropy",
            "projection": "P_TL[Delta J]",
            "zero_route": "same Hilbert tensor ratio for T00, Tij, pressure, and stress",
            "observable_risk": "PPN gamma/beta and orbital stress residuals",
            "bound_formula": "epsilon_tensor <= ||P_PPN G_PPN P_TL Delta J||/||kappa_* T00||",
            "status": "PPN_BOUND_REQUIRED_IF_NONZERO",
            "valid_for_claim": "false",
        },
        {
            "channel_id": "RES3339_2_species_WEP",
            "projection": "P_species[Delta J]",
            "zero_route": "one species-blind matter action measure and no source-only weights w_A",
            "observable_risk": "WEP, source-composition, clock-composition, R10 material residuals",
            "bound_formula": "epsilon_WEP <= max_{A,B}|eta_A-eta_B| after common-mode removal",
            "status": "WEP_BOUND_REQUIRED_IF_NONZERO",
            "valid_for_claim": "false",
        },
        {
            "channel_id": "RES3339_3_spin_clock",
            "projection": "P_spin_or_clock[Delta J]",
            "zero_route": "no independent spin/torsion/clock-channel coupling outside the public metric/coframe",
            "observable_risk": "clock anisotropy, spin-polarized tests, preferred-frame channels",
            "bound_formula": "epsilon_clock <= ||P_clock Delta J||/||kappa_*T||",
            "status": "CLOCK_BOUND_REQUIRED_IF_NONZERO",
            "valid_for_claim": "false",
        },
        {
            "channel_id": "RES3339_4_EM_Hodge_stress",
            "projection": "P_EM[Delta J]",
            "zero_route": "Maxwell/Hodge action uses the same public metric/coframe and same kappa_* Hilbert stress owner",
            "observable_risk": "light bending, Shapiro delay, EM stress/Poynting, alpha/current/Hodge hidden residuals",
            "bound_formula": "epsilon_EM <= |delta_ZA| + |delta_star| + |delta_J| + ||P_EM Delta T_EM||/||T_EM||",
            "status": "EM_STRESS_ROUTE_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "channel_id": "RES3339_5_derivative_contact",
            "projection": "P_derivative_contact[Delta J]",
            "zero_route": "ultralocal Hilbert coupling or universal contact absorbed into measured constants",
            "observable_risk": "finite-size PPN/contact floor",
            "bound_formula": "epsilon_contact <= C_contact(ell_c/L_PPN)^p_contact",
            "status": "CONTACT_SCALE_OWNER_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "channel_id": "RES3339_6_boundary_worldtube",
            "projection": "P_boundary[Delta J]",
            "zero_route": "fixed worldtube/Hilbert source class and zero exterior boundary flux",
            "observable_risk": "source mass drift, orbital GM mismatch, PPN boundary leakage",
            "bound_formula": "epsilon_boundary <= ||P_exterior dB||/||kappa_*T||",
            "status": "WORLDTUBE_BOUND_REQUIRED_IF_NONZERO",
            "valid_for_claim": "false",
        },
    ]


def kernel_contact_rows() -> list[dict[str, Any]]:
    return [
        {
            "kernel_id": "KERN3339_0_ultralocal_Hilbert",
            "coupling_kernel": "K^{mu nu}_{alpha beta}(x,y)=kappa_* delta^{mu nu}_{alpha beta} delta(x-y)",
            "derivation": "The source current is exactly local Hilbert stress; no finite-width kernel exists after measured-G calibration.",
            "ell_c_owner": "ell_c=0 for the residual contact channel",
            "contact_result": "epsilon_contact_PPN=0 if tensor universality and boundary silence are also signed",
            "status": "BEST_ZERO_ROUTE",
            "valid_for_claim": "false",
        },
        {
            "kernel_id": "KERN3339_1_even_isotropic_finite_kernel",
            "coupling_kernel": "K(z)=delta(z)+m2 nabla^2 delta(z)/2+O(ell_c^4 nabla^4)",
            "derivation": "A centered even finite-range kernel has no first moment; the first surviving long-wavelength correction is second derivative.",
            "ell_c_owner": "ell_c^2 := m2 := integral |z|^2 K(z) dz / integral K(z) dz",
            "contact_result": "p_contact=2 unless the second moment is also absorbed or symmetry-forbidden",
            "status": "DERIVATIVE_CONTACT_BOUND_ROUTE",
            "valid_for_claim": "false",
        },
        {
            "kernel_id": "KERN3339_2_second_moment_absorbed",
            "coupling_kernel": "K(z)=delta(z)+m4 nabla^4 delta(z)/24+...",
            "derivation": "If the zeroth and second-derivative local terms are absorbed by calibration or forbidden by symmetry, the fourth-order term dominates.",
            "ell_c_owner": "ell_c^4 := m4 with C_contact carrying tensor/readout constants",
            "contact_result": "p_contact=4 route from 3337/3338",
            "status": "STRONG_SCALE_SUPPRESSION_ROUTE",
            "valid_for_claim": "false",
        },
        {
            "kernel_id": "KERN3339_3_odd_or_species_kernel",
            "coupling_kernel": "K_A(z) has odd moment or species-dependent coefficient",
            "derivation": "Odd moments generate first-derivative/bias terms; species-dependent kernels cannot be absorbed into one G_N.",
            "ell_c_owner": "requires finite source-backed kernel moments for each sector",
            "contact_result": "retains explicit WEP/contact floor",
            "status": "FAIL_OR_BOUND_ROUTE",
            "valid_for_claim": "false",
        },
    ]


def em_coupling_rows() -> list[dict[str, Any]]:
    return [
        {
            "em_id": "EM3339_0_public_Hodge_Maxwell",
            "condition": "S_EM=-lambda_0/4 integral sqrt(-g_obs) F_{mu nu}F^{mu nu} with lambda_0 constant and hidden-independent",
            "consequence": "T_EM^{mu nu} is the Hilbert stress of the same observed metric/coframe, so EM stress couples through the same kappa_* common mode",
            "local_residual": "no local alpha/Hodge/current residual from lambda_0 alone; alpha number may remain calibrated rather than derived",
            "status": "LOCAL_MAXWELL_GR_ROUTE_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "em_id": "EM3339_1_hidden_F2_coefficient",
            "condition": "lambda(y)F^2 or hidden-visible coefficient map survives vertical variation",
            "consequence": "Lie_v lambda creates b_alpha and EM stress/current residuals",
            "local_residual": "clock/WEP/R10/EM propagation channels reopen",
            "status": "FAIL_OR_BOUND_ROUTE",
            "valid_for_claim": "false",
        },
        {
            "em_id": "EM3339_2_current_owner",
            "condition": "charge/current lattice J_Q is fixed representation/q-basic data",
            "consequence": "delta_J=0; source/test charge normalization does not float independently",
            "local_residual": "if q_A(y) weights exist then delta_J_A=Lie_v ln q_A and WEP/R10 source legs reopen",
            "status": "CURRENT_OWNER_GATE",
            "valid_for_claim": "false",
        },
        {
            "em_id": "EM3339_3_poynting_stress_readout",
            "condition": "Poynting flux and radiation stress are read from the same public Hodge metric",
            "consequence": "EM energy flow contributes to Hilbert T_EM with the same source coupling as matter",
            "local_residual": "private constitutive/background-flow tensor C_constitutive creates birefringence/stress residuals if not zero",
            "status": "POYNTING_BACKGROUND_CHECK",
            "valid_for_claim": "false",
        },
    ]


def requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "req_id": "REQ3339_0_parent_Hilbert_action",
            "requirement": "one parent matter action varied with respect to the observed metric/coframe",
            "closes": "defines T^{mu nu} and J^{mu nu} without post-variation source selectors",
            "current_status": "CONDITIONAL_FROM_PRIOR_ROWS_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "req_id": "REQ3339_1_common_kappa",
            "requirement": "one universal kappa_* for matter, EM, pressure/stress, and clock sectors",
            "closes": "measured-G absorption of common mode",
            "current_status": "NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "req_id": "REQ3339_2_no_species_weights",
            "requirement": "no species-indexed source weights w_A outside representation/gauge data",
            "closes": "WEP/source-composition residual zero",
            "current_status": "WEP_OWNER_THEOREM_CONDITIONAL_ONLY",
            "valid_for_claim": "false",
        },
        {
            "req_id": "REQ3339_3_public_Maxwell_Hodge",
            "requirement": "EM kinetic/Hodge/current owner is public, q-basic, and hidden-independent",
            "closes": "Maxwell stress and Poynting couple through Hilbert T_EM",
            "current_status": "EM_PRIORITY_SPLIT_EXISTS_NOT_CLOSED",
            "valid_for_claim": "false",
        },
        {
            "req_id": "REQ3339_4_kernel_moments",
            "requirement": "ell_c, C_contact, p_contact are derived from the parent coupling kernel or proven ultralocal",
            "closes": "3338 contact floor evaluation",
            "current_status": "DERIVATION_ROUTE_NOW_DEFINED_BUT_PARENT_INPUT_MISSING",
            "valid_for_claim": "false",
        },
        {
            "req_id": "REQ3339_5_bianchi_balance",
            "requirement": "nabla_mu Delta J^{mu nu}=0 or compensator equation is signed",
            "closes": "conservation/covariance gate",
            "current_status": "NOT_SIGNED_FOR_RESIDUAL_CHANNELS",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3339_0_decomposition_theorem",
            "claim": "source coupling can be decomposed into common measured-G mode plus residual channels",
            "passed": "true",
            "reason": "J=kappa_*T+Delta J with projectors to tensor/species/spin/EM/contact/boundary channels",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3339_1_absorption_rule",
            "claim": "measured G absorption is legitimate only for a universal common Hilbert stress coefficient",
            "passed": "true",
            "reason": "single G_N calibrates one common T00 coefficient and cannot hide species/tensor/EM relative weights",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3339_2_kernel_owner_route",
            "claim": "ell_c and p_contact have an owner route through local or finite-range coupling kernels",
            "passed": "true",
            "reason": "ultralocal Hilbert gives ell_c=0; centered finite kernel gives p=2; second-moment silence gives p=4",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3339_3_parent_signature_closed",
            "claim": "parent action signs all zero conditions",
            "passed": "false",
            "reason": "Hilbert action, common kappa, no species weights, public Maxwell/Hodge, kernel moments, and Bianchi balance are not all parent-signed",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3339_4_local_GR_claim",
            "claim": "MTS local-GR/PPN/Maxwell source coupling is claim-ready",
            "passed": "false",
            "reason": "3339 derives the exact coupling fork but does not yet attach the parent action clauses or numeric residual bounds",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3339_0",
            "question": "Did 3339 just circle the missing coupling?",
            "answer": "no",
            "reason": "it turns coupling into the equation J=kappa_*T+Delta J and identifies exactly which projections are absorbable, zeroable, or empirically boundable",
            "next_action": "try to sign J=kappa_*T from the parent action syntax or build finite residual rows for the nonzero projections",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3339_1",
            "question": "Can Newton's constant be derived here?",
            "answer": "not yet; but its role is clarified",
            "reason": "G_N can calibrate the universal common coupling kappa_*, while relative tensor/species/EM weights remain physical and cannot be hidden in G_N",
            "next_action": "look for a parent normalization principle for kappa_* separately from local-GR residual silence",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3339_2",
            "question": "Does EM/Poynting help the route?",
            "answer": "yes, as a coupling discriminator",
            "reason": "if EM stress/Poynting comes from the same public Hodge metric, it supports universal Hilbert coupling; hidden F2/Hodge/current maps create measurable residuals",
            "next_action": "tie the EM stress owner rows to the parent Hilbert source clause",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3340-Y5-R2FR-parent-Hilbert-source-clause-or-finite-residual-vector-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3340_parent_Hilbert_source_clause_or_finite_residual_vector.py",
            "objective": "search/construct the exact parent action clause that signs J=kappa_*T for matter+EM, or emit finite residual vector rows for tensor/species/spin/EM/contact/boundary channels",
            "must_include": "parent action syntax; variation target; common kappa; no species weights; public Maxwell/Hodge; kernel moment owner; Bianchi balance; no local-GR claim unless all zero gates close",
            "fallback_if_failed": "promote residual-channel vector to empirical bound acquisition rather than repeating missing-source ledgers",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_rows()
    decomposition = decomposition_rows()
    absorption = absorption_rows()
    residuals = residual_channel_rows()
    kernel = kernel_contact_rows()
    em = em_coupling_rows()
    requirements = requirement_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3339_0_sources_exist",
            "check": "all cited local source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3339_1_sources_parse",
            "check": "all cited local source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3339_2_outputs_parse",
            "check": "all 3339 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3339_3_decomposition",
            "check": "decomposition includes J=kappa*T+DeltaJ and Bianchi guard",
            "passed": any("J^{mu nu}=kappa_* T^{mu nu}+Delta J^{mu nu}" in row["statement"] for row in decomposition)
            and any("nabla_mu Delta J" in row["statement"] for row in decomposition),
            "detail": "",
        },
        {
            "check_id": "VAL3339_4_absorption_rule",
            "check": "measured-G common mode and no-hidden-relative-weight rules are present",
            "passed": any("absorbs common mode" in row["absorption_id"] or "common mode" in row["claim"] for row in absorption)
            and any("cannot be absorbed" in row["claim"] for row in absorption),
            "detail": "",
        },
        {
            "check_id": "VAL3339_5_residual_channels",
            "check": "residual vector includes tensor, species, spin/clock, EM, contact, and boundary channels",
            "passed": {"RES3339_1_tensor_anisotropy", "RES3339_2_species_WEP", "RES3339_3_spin_clock", "RES3339_4_EM_Hodge_stress", "RES3339_5_derivative_contact", "RES3339_6_boundary_worldtube"}.issubset(
                {row["channel_id"] for row in residuals}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3339_6_kernel_contact_owner",
            "check": "kernel route includes ultralocal ell_c=0, p=2 finite kernel, p=4 second-moment route, and fail branch",
            "passed": any("ell_c=0" in row["ell_c_owner"] for row in kernel)
            and any("p_contact=2" in row["contact_result"] for row in kernel)
            and any("p_contact=4" in row["contact_result"] for row in kernel)
            and any(row["status"] == "FAIL_OR_BOUND_ROUTE" for row in kernel),
            "detail": "",
        },
        {
            "check_id": "VAL3339_7_em_route",
            "check": "EM route includes public Hodge/Maxwell, hidden F2 failure, current owner, and Poynting stress",
            "passed": {"EM3339_0_public_Hodge_Maxwell", "EM3339_1_hidden_F2_coefficient", "EM3339_2_current_owner", "EM3339_3_poynting_stress_readout"}.issubset(
                {row["em_id"] for row in em}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3339_8_requirements",
            "check": "parent signature requirements include Hilbert action, common kappa, WEP, EM, kernel, and Bianchi",
            "passed": {"REQ3339_0_parent_Hilbert_action", "REQ3339_1_common_kappa", "REQ3339_2_no_species_weights", "REQ3339_3_public_Maxwell_Hodge", "REQ3339_4_kernel_moments", "REQ3339_5_bianchi_balance"}.issubset(
                {row["req_id"] for row in requirements}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3339_9_no_claim",
            "check": "local-GR claim gates remain false while theorem/route gates pass",
            "passed": all(
                row["passed"] == "true"
                for row in gates
                if row["gate_id"] in {"GATE3339_0_decomposition_theorem", "GATE3339_1_absorption_rule", "GATE3339_2_kernel_owner_route"}
            )
            and all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3339_3_parent_signature_closed", "GATE3339_4_local_GR_claim"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3339_10_next_3340",
            "check": "next target is parent Hilbert source clause or finite residual vector, not another vague audit",
            "passed": any("J=kappa_*T" in row["objective"] and "finite residual vector" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3339_11_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3339_12_overall",
            "check": "3339 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def render_doc() -> str:
    lines: list[str] = [
        "# 3339 - Parent source-coupling decomposition under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "3339 attacks the coupling directly.",
        "",
        "The local-GR source route is now reduced to the decomposition:",
        "",
        "`J^{mu nu} = kappa_* T^{mu nu} + Delta J^{mu nu}`",
        "",
        "where `kappa_* T^{mu nu}` is the universal Hilbert-stress common mode and `Delta J^{mu nu}` is everything that cannot be hidden inside measured `G_N`.",
        "",
        "Measured `G_N` can absorb one universal common coefficient. It cannot absorb species-relative weights, different temporal/spatial tensor ratios, hidden EM/Hodge/current coefficients, spin/clock couplings, or boundary/source-worldtube drift.",
        "",
        "The exact local-GR zero route is therefore:",
        "",
        "`Delta J^{mu nu} = nabla_lambda B^{lambda mu nu} + O((ell_c/L)^p)`",
        "",
        "with zero exterior readout of the boundary/improvement term, universal metric contact absorbed into measured constants, and scale-suppressed derivative contact below the PPN budget.",
        "",
        "The important improvement is that `ell_c` now has an owner route: ultralocal Hilbert coupling gives residual `ell_c=0`; a centered finite kernel gives `p_contact=2`; second-moment silence gives `p_contact=4`.",
        "",
        "No local-GR/PPN/Maxwell claim is made, because the parent action still has to sign the Hilbert source clause and the EM/current/Hodge owner.",
        "",
        "## Source Register",
        "",
    ]
    for row in source_rows():
        lines.append(
            f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} parse_ok={row['parse_ok']} role={row['role']}"
        )
    sections = [
        ("Coupling Decomposition Theorem", decomposition_rows(), "theorem_id"),
        ("Measured-G Absorption Theorem", absorption_rows(), "absorption_id"),
        ("Residual Channel Vector", residual_channel_rows(), "channel_id"),
        ("Kernel Contact Scale Owner", kernel_contact_rows(), "kernel_id"),
        ("Maxwell/EM Stress Coupling Route", em_coupling_rows(), "em_id"),
        ("Parent Signature Requirements", requirement_rows(), "req_id"),
        ("Promotion Gates", promotion_gate_rows(), "gate_id"),
        ("Decision Ledger", decision_rows(), "decision_id"),
        ("Next Target", next_target_rows(), "target_doc"),
    ]
    for title, rows, key_name in sections:
        lines.extend(["", f"## {title}", ""])
        for row in rows:
            label = row.get(key_name, "")
            body = "; ".join(f"{key}={value}" for key, value in row.items() if key != key_name)
            lines.append(f"- `{label}`: {body}")
    lines.extend(
        [
            "",
            "## Test Notes",
            "",
            "- This checkpoint is private and nonclaim.",
            "- It is a derivation/contract checkpoint: it moves the coupling problem into a residual-vector theorem instead of leaving it as a vague missing input.",
            "- It does not derive the numerical value of `G_N` or `alpha`; it separates calibration of common constants from dangerous hidden relative couplings.",
            "- `formalization-workbench` is not modified.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_rows())
    write_csv(OUTPUTS["decomposition"], decomposition_rows())
    write_csv(OUTPUTS["absorption"], absorption_rows())
    write_csv(OUTPUTS["residuals"], residual_channel_rows())
    write_csv(OUTPUTS["kernel"], kernel_contact_rows())
    write_csv(OUTPUTS["em"], em_coupling_rows())
    write_csv(OUTPUTS["requirements"], requirement_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
