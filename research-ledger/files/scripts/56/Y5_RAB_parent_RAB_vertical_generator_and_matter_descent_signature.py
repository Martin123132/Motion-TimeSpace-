from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1575"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1575-Y5-RAB-parent-RAB-vertical-generator-and-matter-descent-signature.md"

SOURCE_FILES = {
    "1574_doc": ROOT / "1574-Y5-RAB-R10-matter-charge-and-ZR-MR2-input-row-or-zero-theorem.md",
    "1574_validation": OUT / "P8_Y5_BRR545_1574_VALIDATION.csv",
    "1574_theorem": OUT / "P8_Y5_PARENT_QLOC_1574_RAB_MATTER_CHARGE_ZERO_THEOREM_ATTEMPT.csv",
    "1574_premises": OUT / "P8_Y5_PARENT_QLOC_1574_RAB_MATTER_DESCENT_PREMISE_MATRIX.csv",
    "1573_kernel": OUT / "P8_Y5_PARENT_QLOC_1573_TAU_R10_KERNEL_DERIVATION_CONTRACT.csv",
    "10_observer": ROOT / "10-observer-map-symplectic-contract.md",
    "07_constraint": ROOT / "07-nonpropagating-reciprocity-constraint.md",
    "1519_coframe": OUT / "P8_Y5_PARENT_FRAME_1519_COFRAME_TAU_LOCK_AUDIT.csv",
    "1044_pullback": OUT / "P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv",
    "1486_descent": ROOT / "1486-Y5-R10-RAB-neighbourhood-quotient-descent-or-MOMS-parent-signature-source-map.md",
}

NEEDLES = {
    "1574_doc": ["The matter-charge route is now exact as a conditional theorem", "NEXT_1575_PARENT_RAB_VERTICAL_GENERATOR_AND_MATTER_DESCENT_SIGNATURE"],
    "1574_validation": ["VAL1574_OVERALL", "PASS"],
    "1574_theorem": ["RMC1574_2_zero_if_signed", "EXACT_CONDITIONAL_THEOREM_NOT_SIGNED"],
    "1574_premises": ["RPM1574_0_R_vertical", "NOT_PARENT_SIGNED"],
    "1573_kernel": ["KDER1573_4_alpha_match", "FORMAL_TAU_KERNEL_LAW_DERIVED_CONDITIONAL"],
    "10_observer": ["R_AB = ln(T^2 S) = 2 ln(J_q).", "derive R_AB=0 from the parent theory"],
    "07_constraint": ["S_constraint = integral lambda_R R_AB.", "R_AB = 0."],
    "1519_coframe": ["OCF1519_1_parent_q", "NOT_PARENT_SIGNED"],
    "1044_pullback": ["MPD1044_7_exact_theorem_if_signed", "EXACT_CONDITIONAL_THEOREM"],
    "1486_descent": ["NQD1486_0_target", "TARGET_EXACT"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1575_SOURCE_REGISTER.csv"
VERTICAL_SIGNATURE = OUT / "P8_Y5_PARENT_QLOC_1575_RAB_VERTICAL_GENERATOR_SIGNATURE_ATTEMPT.csv"
COFRAME_VISIBILITY = OUT / "P8_Y5_PARENT_QLOC_1575_RAB_COFAME_VISIBILITY_TRILEMMA.csv"
MATTER_DESCENT = OUT / "P8_Y5_PARENT_QLOC_1575_RAB_MATTER_DESCENT_SIGNATURE.csv"
BETA_GATE = OUT / "P8_Y5_PARENT_QLOC_1575_BETA_ZERO_IMPORT_GATE.csv"
FINITE_COMPONENTS = OUT / "P8_Y5_PARENT_QLOC_1575_RAB_FINITE_COMPONENT_BOUND_INTERFACE.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1575_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1575_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1575_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1575_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1575_VALIDATION.csv"

COPY_TARGETS = {
    VERTICAL_SIGNATURE: [
        QUARANTINE / "RAB_VERTICAL_GENERATOR_SIGNATURE_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_vertical_generator_signature_attempt_nonclaim_1575.csv",
    ],
    COFRAME_VISIBILITY: [
        QUARANTINE / "RAB_COFRAME_VISIBILITY_TRILEMMA_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_coframe_visibility_trilemma_nonclaim_1575.csv",
    ],
    MATTER_DESCENT: [
        QUARANTINE / "RAB_MATTER_DESCENT_SIGNATURE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_matter_descent_signature_nonclaim_1575.csv",
    ],
    BETA_GATE: [
        QUARANTINE / "BETA_ZERO_IMPORT_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "beta_zero_import_gate_nonclaim_1575.csv",
    ],
    FINITE_COMPONENTS: [
        QUARANTINE / "RAB_FINITE_COMPONENT_BOUND_INTERFACE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_finite_component_bound_interface_nonclaim_1575.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_vertical_matter_descent_decision_nonclaim_1575.csv",
    ],
}


def flags() -> dict[str, bool]:
    return {
        "parent_signed": False,
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "parent_signed",
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1575_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, NEEDLES[key]),
                "needles": "; ".join(NEEDLES[key]),
                "purpose": "R_AB vertical-generator and matter-descent signature attempt",
                **flags(),
            }
        )
    return rows


def vertical_signature_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "signature_id": "VERT1575_0_parent_fields",
            "object": "parent local field chart",
            "candidate_contract": "Phi_parent=(q^I, rho_R, eta^a, boundary) with rho_R representing the R_AB residual direction",
            "test": "chart exists on an open neighbourhood and q^I are the observed quotient variables",
            "current_status": "CHART_CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "blocking_gap": "field list/equivalence relation/kernel basis are not supplied by the current parent action",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "signature_id": "VERT1575_1_generator",
            "object": "R_AB vertical generator",
            "candidate_contract": "v_R = partial_rho_R plus owned compensators on pure-gauge variables",
            "test": "Dq[v_R]=0 and v_R is not an observable metric/coframe deformation",
            "current_status": "NOT_PARENT_SIGNED",
            "blocking_gap": "10 records R_AB=ln(T^2 S) as coframe-visible unless a constraint/quotient route removes it",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "signature_id": "VERT1575_2_observed_coframe",
            "object": "observed coframe functor",
            "candidate_contract": "e_obs=Obs_e(q(Phi)) before matter/readout/source fitting",
            "test": "Lie_{v_R} e_obs = D Obs_e[Dq[v_R]]=0",
            "current_status": "EXACT_IF_DQ_ZERO_BUT_OBS_E_NOT_CONSTRUCTED",
            "blocking_gap": "1519 keeps Obs_e(q) not constructed and parent q not signed",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "signature_id": "VERT1575_3_constraint_escape",
            "object": "constraint/no-pole route",
            "candidate_contract": "R_AB is eliminated by lambda_R R_AB or no physical pole before matter coupling",
            "test": "variation gives R_AB=0 and no independent Green kernel/source charge exists",
            "current_status": "BEST_ROUTE_BUT_PARENT_ORIGIN_UNSIGNED",
            "blocking_gap": "07 writes the constraint route but does not derive the lambda_R term from the parent action",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "signature_id": "VERT1575_4_physical_residual_fallback",
            "object": "finite physical R_AB branch",
            "candidate_contract": "if Dq[v_R] != 0 or R_AB remains coframe-visible, beta/Z/M/tail rows must stay finite",
            "test": "no beta-zero or local-GR claim is allowed",
            "current_status": "RETAINED_NONCLAIM_FALLBACK",
            "blocking_gap": "finite branch needs beta_S^R, beta_T^R, Z_R, M_R^2, Xi_R10 and boundary tail inputs",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "signature_id": "VERT1575_5_verdict",
            "object": "v_R in ker(Dq)",
            "candidate_contract": "parent-sign quotient verticality or eliminate R_AB as a constraint/no-pole field",
            "test": "all previous rows close without closure-only axiom adoption",
            "current_status": "FAIL_CURRENT_CLAIM_VERTICALITY_NOT_SIGNED",
            "blocking_gap": "current corpus cannot yet promote v_R in ker(Dq)",
            **flags(),
        },
    ]


def coframe_visibility_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": "TRI1575_0_physical_coframe_residual",
            "route": "R_AB remains a physical coframe residual",
            "condition": "R_AB=ln(T^2 S) changes e_obs or metric readout",
            "consequence": "Dq[v_R] != 0; beta_i^R may be physical; R10/PPN/WEP pressure remains finite",
            "current_status": "OPEN_NONCLAIM",
            "preferred_rank": 3,
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": "TRI1575_1_quotient_representative",
            "route": "R_AB is a representative/fibre coordinate only",
            "condition": "q and e_obs are invariant under v_R on an open neighbourhood",
            "consequence": "matter pullback kills beta_i^R, but only after q/Obs_e/matter/constant/boundary signatures are parent-signed",
            "current_status": "BEST_ZERO_ROUTE_UNSIGNED",
            "preferred_rank": 1,
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": "TRI1575_2_constraint_no_pole",
            "route": "R_AB is absent/nonpropagating by constraint",
            "condition": "lambda_R R_AB or first-class/no-pole action removes the Green kernel before source matching",
            "consequence": "bulk R10 Yukawa exchange is absent, but the parent origin of the constraint and boundary silence must be derived",
            "current_status": "BEST_LOCAL_GR_ROUTE_UNSIGNED",
            "preferred_rank": 2,
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": "TRI1575_3_closure_axiom",
            "route": "declare R_AB vertical or zero by closure",
            "condition": "no parent action/equivalence relation/current-chain proof",
            "consequence": "invalid shortcut; cannot be used for GR reduction",
            "current_status": "REFUSED",
            "preferred_rank": 99,
            **flags(),
        },
    ]


def matter_descent_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "descent_id": "MDS1575_0_action_form",
            "signature_clause": "S_matter=sum_A Sbar_A[Psi_A,e_obs(q(Phi)),omega[e_obs],theta_A]+dB_A",
            "why_needed": "makes ordinary matter depend on parent variables only through quotient-owned observed geometry and fixed labels",
            "current_status": "NOT_PARENT_SIGNED",
            "if_signed": "geometry term in delta_{v_R} S_A vanishes when Dq[v_R]=0",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "descent_id": "MDS1575_1_matter_lift",
            "signature_clause": "delta_{v_R} Psi_A is zero or owned gauge/Lorentz/diffeomorphism lift with only proper boundary variation",
            "why_needed": "prevents a physical matter transformation from reintroducing a source charge",
            "current_status": "NOT_PARENT_SIGNED",
            "if_signed": "matter Euler terms vanish on shell or become exact boundary terms",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "descent_id": "MDS1575_2_constants",
            "signature_clause": "Lie_{v_R} theta_A=0 for masses, charges, alpha_EM, clocks, material labels and standards",
            "why_needed": "prevents hidden material/clock/fine-structure beta channels",
            "current_status": "NOT_PARENT_SIGNED",
            "if_signed": "constant-current term in beta_i^R vanishes",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "descent_id": "MDS1575_3_no_marker",
            "signature_clause": "no source-only prefactor, hidden conformal/disformal frame, marker field, or post-readout EFT counterterm",
            "why_needed": "prevents relative source/test charge after the quotient",
            "current_status": "CONTRACT_WRITTEN_NOT_DERIVED",
            "if_signed": "beta source/test split cannot hide in species weights",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "descent_id": "MDS1575_4_boundary",
            "signature_clause": "B_A[v_R] is zero, exact/proper, compact-support silent, or source-backed in an absolute tail envelope",
            "why_needed": "prevents edge/worldtube/readout terms from becoming alpha_boundary_tail",
            "current_status": "OPEN",
            "if_signed": "boundary contribution to beta_i^R is zero or separately bounded",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "descent_id": "MDS1575_5_verdict",
            "signature_clause": "all clauses hold on an open neighbourhood",
            "why_needed": "imports beta_S^R=beta_T^R=0 and removes bulk R10 source amplitude",
            "current_status": "FAIL_CURRENT_CLAIM_DESCENT_NOT_SIGNED",
            "if_signed": "bulk beta zero can move to a raw theorem row; still check boundary tail and no-pole/constraint status",
            **flags(),
        },
    ]


def beta_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "BZG1575_0_formal_theorem",
            "claim": "if v_R in ker(Dq) and matter descent clauses hold, beta_i^R=0",
            "gate_status": "PASS_FORMAL_CONDITIONAL",
            "reason": "chain rule gives delta_{v_R} S_i=0 when quotient, constants, matter lift and boundary clauses vanish",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "BZG1575_1_verticality",
            "claim": "v_R in ker(Dq)",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "R_AB is coframe-visible unless quotient/constraint/no-pole route is parent-signed",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "BZG1575_2_matter_descent",
            "claim": "ordinary matter descends through q with fixed constants",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "matter functor, constant superselection, no-marker, and boundary clauses remain unsigned",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "BZG1575_3_beta_import",
            "claim": "beta_S^R=beta_T^R=0 can be imported",
            "gate_status": "REFUSED_CURRENT_CORPUS",
            "reason": "formal theorem is not live evidence",
            **flags(),
        },
    ]


def finite_component_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "RFC1575_0_q_visibility",
            "component": "Dq[v_R] or Lie_{v_R} e_obs",
            "required_resolution": "parent-signed zero or numeric bound on coframe/metric response",
            "current_status": "MISSING_VERTICALITY_CERTIFICATE",
            "alpha_effect": "feeds beta_geom or PPN/R10 profile",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "RFC1575_1_constants",
            "component": "Lie_{v_R} theta_A",
            "required_resolution": "constant superselection theorem or source-backed dtheta/dR_AB coefficients",
            "current_status": "MISSING_CONSTANT_SUPERSELECTION_OR_COEFFICIENTS",
            "alpha_effect": "feeds material/clock/fine-structure charge",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "RFC1575_2_marker_source_weight",
            "component": "hidden marker/source-only prefactor",
            "required_resolution": "no-marker/no-Hom theorem or bounded source/test prefactor rows",
            "current_status": "MISSING_NO_MARKER_THEOREM_OR_BOUNDS",
            "alpha_effect": "feeds beta_S^R beta_T^R tail",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "RFC1575_3_boundary_tail",
            "component": "boundary/worldtube/readout/domain tail",
            "required_resolution": "zero/proper/exact boundary theorem or absolute no-cancellation bound",
            "current_status": "MISSING_BOUNDARY_TAIL_ZERO_OR_BOUND",
            "alpha_effect": "feeds alpha_boundary_tail",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "RFC1575_4_parent_row",
            "component": "Z_R and M_R^2",
            "required_resolution": "constraint/no-pole theorem or positive same-frame kinetic/Hessian residues",
            "current_status": "MISSING_ZR_MR2_OR_NO_POLE",
            "alpha_effect": "sets tau_R10 denominator and lambda_R",
            **flags(),
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1575_0_sources",
            "object": "1574 handoff plus observer/coframe/descent evidence",
            "status": "PASS_IF_VALIDATION_PASS",
            "detail": "source register verifies all needles before using the derivation",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1575_1_verticality",
            "object": "v_R in ker(Dq)",
            "status": "FAIL_CURRENT_CLAIM_VERTICALITY_NOT_SIGNED",
            "detail": "R_AB visibility creates a trilemma: physical residual, quotient representative, or constraint/no-pole route",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1575_2_matter_descent",
            "object": "S_matter=Sbar[q,theta]",
            "status": "FAIL_CURRENT_CLAIM_DESCENT_NOT_SIGNED",
            "detail": "matter functor/constant/no-marker/boundary signatures are exact but not parent-signed",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1575_3_beta_zero",
            "object": "beta_S^R=beta_T^R=0",
            "status": "BLOCKED_NO_CLAIM",
            "detail": "formal theorem cannot be imported as a live row",
            **flags(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1575_0_theorem",
            "claim": "R_AB beta-zero theorem exists conditionally",
            "status": "PASS_FORMAL_NONCLAIM",
            "reason": "vertical quotient plus matter descent is sufficient",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1575_1_vertical",
            "claim": "R_AB is quotient-vertical or constrained/no-pole",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "parent q/constraint origin is unsigned",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1575_2_beta_zero",
            "claim": "bulk R10 beta source-test product vanishes",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "beta-zero import refused until verticality and descent are parent-signed",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1575_3_R10_score",
            "claim": "R10 alpha(lambda) can be scored",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "finite components and external acceptance remain missing",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1575_4_local_GR",
            "claim": "derived local GR/Newton branch",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "local source denominator, boundary, PPN, and q_loc followthrough remain open",
            **flags(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1575_0_vertical_trilemma",
            "decision": "RAB_VERTICALITY_NOT_SIGNED_TRILEMMA_EXPLICIT",
            "reason": "R_AB is coframe-visible unless the parent quotient or constraint/no-pole route removes it",
            "consequence": "do not import beta zero; choose quotient/constraint proof or finite component bounds",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1575_1_matter_signature",
            "decision": "MATTER_DESCENT_SIGNATURE_EXACT_BUT_UNSIGNED",
            "reason": "the necessary action form, matter lift, fixed constants, no-marker rule and boundary rule are named precisely",
            "consequence": "these clauses are the future parent-action contract",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1575_2_next",
            "decision": "NEXT_1576_RAB_CONSTRAINT_NO_POLE_OR_QUOTIENT_MAP_CONSTRUCTION",
            "reason": "the least-scrutiny route is to remove R_AB as a physical local pole before attempting numeric beta rows",
            "consequence": "try to derive lambda_R R_AB/no-pole/quotient map from MTS primitives; if it fails, fill finite component bound rows",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1576-Y5-RAB-constraint-no-pole-or-quotient-map-construction.md",
            "script": "scripts/Y5_RAB_constraint_no_pole_or_quotient_map_construction.py",
            "objective": "try to derive a parent-origin lambda_R R_AB constraint, first-class/no-pole status, or explicit quotient map q with R_AB fibre verticality; otherwise stage finite component bound rows",
            "do_not": "do not declare R_AB vertical by axiom; do not score R10; do not claim local GR; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count() -> int:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT.parent), "status", "--short", "--", "formalization-workbench"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return 0
    return len([line for line in result.stdout.splitlines() if line.strip()])


def has_1575_rows(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any("1575" in path.name for path in folder.glob("*.csv"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    vertical = read_csv(VERTICAL_SIGNATURE)
    trilemma = read_csv(COFRAME_VISIBILITY)
    matter = read_csv(MATTER_DESCENT)
    beta = read_csv(BETA_GATE)
    finite = read_csv(FINITE_COMPONENTS)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    checks = [
        ("VAL1575_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist"),
        ("VAL1575_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL1575_2_verticality_not_signed",
            any(row["signature_id"] == "VERT1575_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_VERTICALITY_NOT_SIGNED" for row in vertical),
            "R_AB verticality remains unsigned",
        ),
        (
            "VAL1575_3_trilemma_written",
            len(trilemma) == 4 and any(row["route_id"] == "TRI1575_3_closure_axiom" and row["current_status"] == "REFUSED" for row in trilemma),
            "coframe visibility trilemma and closure refusal written",
        ),
        (
            "VAL1575_4_matter_signature_not_signed",
            any(row["descent_id"] == "MDS1575_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_DESCENT_NOT_SIGNED" for row in matter),
            "matter descent signature remains unsigned",
        ),
        (
            "VAL1575_5_beta_import_refused",
            any(row["gate_id"] == "BZG1575_3_beta_import" and row["gate_status"] == "REFUSED_CURRENT_CORPUS" for row in beta),
            "beta-zero import refused",
        ),
        (
            "VAL1575_6_finite_components_missing",
            all(row["current_status"].startswith("MISSING") for row in finite),
            "finite component interface remains missing-valued",
        ),
        (
            "VAL1575_7_runner_blocks",
            any(row["runner_id"] == "RUN1575_3_beta_zero" and row["status"] == "BLOCKED_NO_CLAIM" for row in runner),
            "runner blocks beta-zero/R10 claim",
        ),
        (
            "VAL1575_8_claim_gates_closed",
            all(row["claim_allowed"] == "False" for row in gates) and any(row["gate_id"] == "GATE1575_0_theorem" for row in gates),
            "claim gates closed while theorem is formal nonclaim",
        ),
        (
            "VAL1575_9_decision_next",
            any(row["decision"] == "NEXT_1576_RAB_CONSTRAINT_NO_POLE_OR_QUOTIENT_MAP_CONSTRUCTION" for row in decisions),
            "decision selects constraint/no-pole or quotient map target",
        ),
        ("VAL1575_10_csv_parse", all(len(read_csv(path)) > 0 for path in generated_csvs), "all generated 1575 CSVs parse cleanly"),
        ("VAL1575_11_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1575_12_no_raw_accepted", not has_1575_rows(RAB_RAW) and not has_1575_rows(RAB_ACCEPTED), "no 1575 rows written to raw/accepted finite directories"),
        ("VAL1575_13_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets), "branch/quarantine nonclaim copies written"),
        ("VAL1575_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1575_15_formalization_untouched", formalization_modified_count() == 0, "formalization-workbench modified-file count is 0"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1575_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1575 R_AB vertical generator and matter descent validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(col, "")) for col in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    vertical: list[dict[str, Any]],
    trilemma: list[dict[str, Any]],
    matter: list[dict[str, Any]],
    beta: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1575 - R_AB Parent Vertical Generator And Matter Descent Signature",
                "## Verdict\n"
                "- The exact beta-zero theorem survives: if `v_R in ker(Dq)` and ordinary matter/constants/boundaries descend through the quotient, then `beta_i^R=0`.\n"
                "- The current corpus still cannot parent-sign `v_R in ker(Dq)` because earlier observer-map work treats `R_AB=ln(T^2 S)` as coframe-visible unless a constraint, no-pole, or quotient construction removes it.\n"
                "- The honest state is a trilemma: physical coframe residual, quotient-representative fibre coordinate, or constraint/no-pole field. Closure-only verticality is refused.\n"
                "- Matter descent is now written as an exact parent-action signature contract, but it is not a live claim row.\n"
                "- No beta-zero import, R10 score, local GR/Newton reduction, PPN, WEP, clock, orbital, `Z_R=0`, `tau_R10=0`, or `q_R=0` claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## R_AB Vertical Generator Signature Attempt",
                md_table(vertical, ["signature_id", "object", "candidate_contract", "test", "current_status", "blocking_gap"]),
                "## Coframe Visibility Trilemma",
                md_table(trilemma, ["route_id", "route", "condition", "consequence", "current_status", "preferred_rank"]),
                "## Matter Descent Signature",
                md_table(matter, ["descent_id", "signature_clause", "why_needed", "current_status", "if_signed"]),
                "## Beta-Zero Import Gate",
                md_table(beta, ["gate_id", "claim", "gate_status", "reason"]),
                "## Finite Component Bound Interface",
                md_table(finite, ["component_id", "component", "required_resolution", "current_status", "alpha_effect"]),
                "## Runner Nonclaim",
                md_table(runner, ["runner_id", "object", "status", "detail"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "consequence"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    vertical = vertical_signature_rows()
    trilemma = coframe_visibility_rows()
    matter = matter_descent_rows()
    beta = beta_gate_rows()
    finite = finite_component_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        VERTICAL_SIGNATURE,
        COFRAME_VISIBILITY,
        MATTER_DESCENT,
        BETA_GATE,
        FINITE_COMPONENTS,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(VERTICAL_SIGNATURE, vertical)
    write_csv(COFRAME_VISIBILITY, trilemma)
    write_csv(MATTER_DESCENT, matter)
    write_csv(BETA_GATE, beta)
    write_csv(FINITE_COMPONENTS, finite)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, vertical, trilemma, matter, beta, finite, runner, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
