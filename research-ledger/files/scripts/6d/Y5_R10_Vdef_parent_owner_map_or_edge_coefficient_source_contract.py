from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = POST_CHECKPOINT.parent / "formalization-workbench"
OUTPUT_DOC = POST_CHECKPOINT / "726-Y5-R10-Vdef-parent-owner-map-or-edge-coefficient-source-contract.md"
NEXT_TARGET = "727-Y5-R10-DCdagger-vertical-generator-map-or-source-backed-edge-row.md"
GENERATED_UTC = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)


SOURCES = {
    "725_doc": {
        "path": POST_CHECKPOINT / "725-Y5-R10-edge-runner-inputs-or-Vdef-owner-repair.md",
        "note": "immediate handoff: parent owner map or source edge coefficients",
        "needles": ["726-Y5-R10-Vdef-parent-owner-map-or-edge-coefficient-source-contract.md", "Current verdict: **not closed**", "Both R10 runner branches correctly block"],
    },
    "725_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_725_VALIDATION.csv",
        "note": "prior validation gate",
        "needles": ["V725_10_next_target_selected", "pass", "V725_13_formalization_workbench_untouched"],
    },
    "725_vdef_repair": {
        "path": RESIDUALS / "P8_Y5_R10_725_VDEF_OWNER_REPAIR_ATTEMPT.csv",
        "note": "current Vdef owner repair attempt",
        "needles": ["VOR725_1_parent_symplectic_owner", "missing_theta_Y_Omega_Y_vertical_generator", "false"],
    },
    "725_blockers": {
        "path": RESIDUALS / "P8_Y5_R10_725_EDGE_CLAIM_BLOCKER_LEDGER.csv",
        "note": "current edge claim blockers",
        "needles": ["CB725_0_edge_coefficients", "K_edge, Qbar_edge_XH, and qbar_XT", "true"],
    },
    "725_runner_status": {
        "path": RESIDUALS / "P8_Y5_R10_725_RUNNER_STATUS_SUMMARY.csv",
        "note": "current runner refusal evidence",
        "needles": ["R10_EDGE_SMOKE_725_REVIEW_CANDIDATE", "claim_allowed", "false"],
    },
    "587_doc": {
        "path": POST_CHECKPOINT / "587-Y5-R10-affine-Vdef-parent-source-map-or-edge-prior-tightening.md",
        "note": "older affine source map and multiplier backreaction blocker",
        "needles": ["affine Vdef parent source map", "multiplier X still backreacts", "necessary but not sufficient"],
    },
    "587_source_map": {
        "path": RESIDUALS / "P8_Y5_R10_587_AFFINE_PARENT_SOURCE_MAP.csv",
        "note": "older affine parent source map",
        "needles": ["X_nu", "C_X^nu", "P^{mu nu}[Y]"],
    },
    "587_equations": {
        "path": RESIDUALS / "P8_Y5_R10_587_PARENT_SOURCE_EQUATION_CONTRACT.csv",
        "note": "older multiplier variation equations",
        "needles": ["EQ587_3_Y_backreaction", "delta_Y S_X", "new_hard_blocker"],
    },
    "588_doc": {
        "path": POST_CHECKPOINT / "588-Y5-R10-multiplier-backreaction-kill-or-bound-edge-product.md",
        "note": "older adjoint backreaction theorem",
        "needles": ["(DC)^dagger X", "Noether/first-class identity", "edge product"],
    },
    "588_adjoint": {
        "path": RESIDUALS / "P8_Y5_R10_588_ADJOINT_BACKREACTION_THEOREM.csv",
        "note": "formal adjoint backreaction theorem",
        "needles": ["ABT588_2_adjoint_zero_mode_kill", "(DC)^dagger X", "contract_written_not_proved"],
    },
    "588_budget": {
        "path": RESIDUALS / "P8_Y5_R10_588_EDGE_PRODUCT_FACTOR_BUDGET.csv",
        "note": "edge product factor budget",
        "needles": ["EPB588_9", "608.0783", "0.00234471960478"],
    },
    "589_doc": {
        "path": POST_CHECKPOINT / "589-Y5-R10-adjoint-zero-mode-certificate-or-source-backed-edge-product-row.md",
        "note": "older adjoint zero-mode certificate skeleton",
        "needles": ["DCdagger", "vertical generator", "source-backed edge-product row"],
    },
    "589_certificate": {
        "path": RESIDUALS / "P8_Y5_R10_589_ADJOINT_ZERO_MODE_CERTIFICATE.csv",
        "note": "DCdagger to vertical generator certificate route",
        "needles": ["AZC589_0_adjoint_as_vertical_generator", "best_certificate_route_not_mapped_to_current_parent_fields", "false"],
    },
    "589_sources_required": {
        "path": RESIDUALS / "P8_Y5_R10_589_SOURCES_REQUIRED_TO_CLOSE_CERTIFICATE.csv",
        "note": "missing source objects for adjoint certificate",
        "needles": ["SRC589_1_DC_operator", "vertical_transformation_law", "missing"],
    },
    "589_edge_template": {
        "path": RESIDUALS / "P8_Y5_R10_589_SOURCE_BACKED_EDGE_PRODUCT_ROW_TEMPLATE.csv",
        "note": "source-backed edge row template",
        "needles": ["SBE589_0_required_source_backed_row", "MISSING_SOURCE_BACKED_K_EDGE", "false"],
    },
    "512_doc": {
        "path": POST_CHECKPOINT / "512-match-MTS-symbols-to-local-GR-action-blocks.md",
        "note": "symbol/action block placement",
        "needles": ["q_loc^nu = P_loc", "Pi_M", "not_action_placed"],
    },
    "513_doc": {
        "path": POST_CHECKPOINT / "513-Gamma-Khat-q_loc-first-variation-or-demotion.md",
        "note": "q_loc Ward/stress divergence route",
        "needles": ["q_loc^nu = P_loc nabla_mu T_GK", "conditional_derivation_route", "not_supplied"],
    },
    "539_doc": {
        "path": POST_CHECKPOINT / "539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md",
        "note": "Hamiltonian mass/edge projection candidate",
        "needles": ["Pi_M^H", "Hamiltonian surface charge", "fallback_ready_not_filled"],
    },
    "581_doc": {
        "path": POST_CHECKPOINT / "581-Y5-R10-quotient-vertical-no-pole-parent-theorem-attempt.md",
        "note": "quotient-vertical theorem shape",
        "needles": ["v_X in ker(d pi)", "Q_X[epsilon]=0", "parent projection/universal property"],
    },
    "583_doc": {
        "path": POST_CHECKPOINT / "583-Y5-R10-parent-momentum-map-owner-or-edge-residual-demotion.md",
        "note": "parent momentum-map owner contract",
        "needles": ["i_{v_epsilon} Omega_Y = delta G[epsilon]", "P[Y], J_eff[Y], P_mem[Y]", "edge residual"],
    },
}


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def source_path_string(*keys: str) -> str:
    return ";".join(str(SOURCES[key]["path"]) for key in keys)


def text_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


def csv_contains(path: Path, *needles: str) -> bool:
    return text_contains(path, list(needles))


def prior_validation_clean(path: Path) -> bool:
    rows = read_csv(path)
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def all_valid_false(paths: list[Path]) -> bool:
    for path in paths:
        rows = read_csv(path)
        if not rows:
            continue
        if "valid_for_claim" not in rows[0]:
            continue
        if any(row.get("valid_for_claim", "").lower() != "false" for row in rows):
            return False
    return True


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime)
        if modified > CUTOFF:
            count += 1
    return count


def under_post_checkpoint(paths: list[Path]) -> bool:
    root = POST_CHECKPOINT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root)
        except ValueError:
            return False
    return True


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        cells = []
        for field in fields:
            value = str(row.get(field, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def make_source_register() -> list[dict[str, object]]:
    return [
        {
            "source_id": key,
            "path": str(info["path"]),
            "exists": bool_text(info["path"].exists()),
            "needle_check": bool_text(text_contains(info["path"], info["needles"])),
            "role": info["note"],
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        }
        for key, info in SOURCES.items()
    ]


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    source_register = make_source_register()
    old_budget = read_csv(SOURCES["588_budget"]["path"])
    tightest = min(old_budget, key=lambda row: float(row["alpha_edge_ceiling"]))

    parent_owner_map = [
        {
            "owner_id": "POM726_0_parent_pairing",
            "needed_object": "theta_Y, Omega_Y, or field-space pairing G_ij",
            "role": "defines the adjoint and the Hamiltonian/momentum-map owner",
            "candidate_source": "583/589 momentum-map certificate route",
            "required_equation": "delta L_parent=E_i delta Y^i+d theta_Y(delta Y); Omega_Y=delta theta_Y",
            "current_status": "missing_explicit_parent_pairing",
            "claim_effect": "DCdagger and G[epsilon] are undefined as parent-owned objects",
            "fallback_if_missing": "edge coefficient source contract",
            "valid_for_claim": "false",
            "source_paths": source_path_string("583_doc", "589_sources_required"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "owner_id": "POM726_1_vertical_generator",
            "needed_object": "v_X or v_epsilon on all parent fields",
            "role": "identifies X as quotient/gauge direction rather than physical field",
            "candidate_source": "581 quotient-vertical theorem shape",
            "required_equation": "v_X in ker(d pi); i_v Omega_Y=delta G_X",
            "current_status": "not_constructed",
            "claim_effect": "X cannot be removed from local physical phase space",
            "fallback_if_missing": "finite X/edge residual branch",
            "valid_for_claim": "false",
            "source_paths": source_path_string("581_doc", "583_doc", "589_certificate"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "owner_id": "POM726_2_CX_identity",
            "needed_object": "C_X^nu as Noether/Bianchi/first-class identity",
            "role": "prevents X from imposing a new local equation on GR-like solutions",
            "candidate_source": "587 affine parent source map plus 588 constraint gate",
            "required_equation": "C_X=N(E0) or C_X is the differentiable first-class generator density",
            "current_status": "contract_written_not_owned",
            "claim_effect": "C_X may be second-class/closure-only",
            "fallback_if_missing": "demote to q_loc/edge/PPN residual",
            "valid_for_claim": "false",
            "source_paths": source_path_string("587_source_map", "588_adjoint", "513_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "owner_id": "POM726_3_P_owner",
            "needed_object": "P^{mu nu}[Y]",
            "role": "boundary momentum and divergence superpotential in C_X=-nabla P+J",
            "candidate_source": "affine Vdef coefficient or Noether current coefficient",
            "required_equation": "P^{mu nu}=partial V_def/partial Z_{mu nu} from parent variables, not free insertion",
            "current_status": "promising_but_unfilled",
            "claim_effect": "boundary charge and K_edge remain unowned",
            "fallback_if_missing": "K_edge and Qbar_edge_XH source rows",
            "valid_for_claim": "false",
            "source_paths": source_path_string("587_source_map", "725_vdef_repair"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "owner_id": "POM726_4_J_eff_owner",
            "needed_object": "J_eff^nu[Y]",
            "role": "bulk current/source balancing the divergence superpotential",
            "candidate_source": "Euler-Ward identity for T_GK or memory/source current",
            "required_equation": "nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A, with J_eff owned by the same identity as P",
            "current_status": "not_derived",
            "claim_effect": "q_loc/source-current residual remains live",
            "fallback_if_missing": "q_loc/edge coefficient residual contract",
            "valid_for_claim": "false",
            "source_paths": source_path_string("587_source_map", "513_doc", "512_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "owner_id": "POM726_5_A_owner",
            "needed_object": "A_{mu nu}[Y] or decision to use pure multiplier C_X form",
            "role": "defect/connection part of Z=nabla X-A",
            "candidate_source": "local representative lock/quotient connection",
            "required_equation": "A has a parent transformation law or is absent from the minimal multiplier branch",
            "current_status": "unplaced",
            "claim_effect": "A can become a cancellation tensor if not owned",
            "fallback_if_missing": "drop Z-form and keep only C_X multiplier contract",
            "valid_for_claim": "false",
            "source_paths": source_path_string("587_source_map", "725_vdef_repair"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "owner_id": "POM726_6_DCdagger_map",
            "needed_object": "(DC[Y0])^dagger X mapped to vertical generator",
            "role": "kills multiplier backreaction if proper stabilizers vanish",
            "candidate_source": "589 adjoint zero-mode certificate route",
            "required_equation": "int X_nu DC^nu[delta Y]=int <v_X[Y0],delta Y>_G + boundary",
            "current_status": "not_mapped",
            "claim_effect": "delta_Y S_X can still alter local parent equations",
            "fallback_if_missing": "source-backed edge product row",
            "valid_for_claim": "false",
            "source_paths": source_path_string("588_adjoint", "589_certificate", "589_sources_required"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "owner_id": "POM726_7_boundary_silence",
            "needed_object": "B_X exact/proper-zero plus K_boundary=0",
            "role": "removes edge charge after bulk no-pole is achieved",
            "candidate_source": "586/588 boundary exactness branch",
            "required_equation": "Q_edge[epsilon]=int_boundary epsilon_nu(n_mu P^{mu nu}+B_ct^nu)=0",
            "current_status": "not_derived",
            "claim_effect": "Qbar_edge_XH(lambda) remains possible",
            "fallback_if_missing": "edge projection/source contract",
            "valid_for_claim": "false",
            "source_paths": source_path_string("588_adjoint", "725_vdef_repair"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "owner_id": "POM726_8_projector_owner",
            "needed_object": "Pi_M^H edge projection",
            "role": "decides whether an edge charge enters measured source mass",
            "candidate_source": "Hamiltonian/covariant phase-space charge map",
            "required_equation": "Qbar_edge_XH(lambda)=Pi_M^H[Q_edge^H(lambda)]/M_H with fixed reference subtraction",
            "current_status": "candidate_projection_not_adopted",
            "claim_effect": "source-measure coupling can leak through Qbar_edge_XH",
            "fallback_if_missing": "Qbar_edge_XH source row",
            "valid_for_claim": "false",
            "source_paths": source_path_string("539_doc", "725_blockers"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "owner_id": "POM726_9_matter_quotient",
            "needed_object": "matter quotient map and no-marker coupling",
            "role": "kills ordinary test-body charge qbar_XT",
            "candidate_source": "quotient matter functor / observed metric readout",
            "required_equation": "S_matter[psi,hat_g(q(Y))] and v_X hat_g=0 for all ordinary species/clocks",
            "current_status": "not_signed",
            "claim_effect": "ordinary matter can retain finite X/edge response",
            "fallback_if_missing": "qbar_XT source row",
            "valid_for_claim": "false",
            "source_paths": source_path_string("581_doc", "725_vdef_repair"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    owner_promotion_gate = [
        {
            "gate_id": "OPG726_0_all_parent_objects",
            "claim_condition": "parent pairing, vertical generator, C_X identity, P/J/A owner, boundary, projector, and matter quotient all supplied",
            "current_result": "fail_current_corpus",
            "why": "at least one missing object leaves X as a physical/closure residual instead of pure parent redundancy",
            "if_fail": "no local-GR/no-pole theorem credit",
            "valid_for_claim": "false",
            "source_paths": source_path_string("725_vdef_repair", "589_sources_required"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "OPG726_1_backreaction_kill",
            "claim_condition": "(DC)^dagger X=v_X[Y0] and proper/reference boundary conditions imply X=0",
            "current_result": "not_mapped",
            "why": "affine H_ZZ=0 does not by itself remove delta_Y S_X",
            "if_fail": "multiplier branch is closure-only or residual-bearing",
            "valid_for_claim": "false",
            "source_paths": source_path_string("588_adjoint", "589_certificate"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "OPG726_2_edge_silence",
            "claim_condition": "Q_edge=0, K_boundary=0, and Pi_M^H[Q_edge]=0 under allowed local boundary data",
            "current_result": "not_derived",
            "why": "bulk no-pole can still leak through edge charge",
            "if_fail": "source K_edge and Qbar_edge_XH",
            "valid_for_claim": "false",
            "source_paths": source_path_string("725_blockers", "539_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "OPG726_3_matter_blindness",
            "claim_condition": "delta_X S_matter=0 universally and no representative-marker coefficients survive",
            "current_result": "not_signed",
            "why": "test-body charge must be killed by structure, not fitted small",
            "if_fail": "source qbar_XT or bound it",
            "valid_for_claim": "false",
            "source_paths": source_path_string("581_doc", "725_vdef_repair"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "OPG726_4_current_verdict",
            "claim_condition": "all above gates pass together",
            "current_result": "blocked_for_claim",
            "why": "owner route remains mathematically precise but unsigned",
            "if_fail": "use edge coefficient source contract",
            "valid_for_claim": "false",
            "source_paths": source_path_string("725_doc", "587_doc", "589_doc"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    edge_coefficient_source_contract = [
        {
            "contract_id": "ECSC726_0_lambda_edge",
            "coefficient": "lambda_edge",
            "meaning": "active edge support/range envelope",
            "required_source": "boundary kernel spectrum, support theorem, or source-backed range grid",
            "required_units": "meters",
            "acceptance_gate": "positive numeric lambda grid or theorem-zero no-support certificate",
            "current_status": "missing",
            "claim_failure_if_missing": "cannot choose alpha_bound(lambda)",
            "valid_for_claim": "false",
            "source_paths": source_path_string("725_blockers", "588_budget"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "contract_id": "ECSC726_1_K_edge",
            "coefficient": "K_edge(lambda)",
            "meaning": "edge Green-kernel normalization relative to observed G",
            "required_source": "parent boundary propagator/envelope normalization",
            "required_units": "dimensionless after G_obs normalization",
            "acceptance_gate": "numeric/source-backed function or theorem-zero K_edge=0",
            "current_status": "missing",
            "claim_failure_if_missing": "alpha_edge remains symbolic",
            "valid_for_claim": "false",
            "source_paths": source_path_string("725_blockers", "589_edge_template"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "contract_id": "ECSC726_2_Qbar_edge_XH",
            "coefficient": "Qbar_edge_XH(lambda)",
            "meaning": "projected source-body edge charge per measured mass",
            "required_source": "Hamiltonian Pi_M^H projection of Q_edge with reference subtraction",
            "required_units": "dimensionless mass-normalized charge",
            "acceptance_gate": "numeric/source-backed projected charge or Pi_M^H[Q_edge]=0 theorem",
            "current_status": "missing",
            "claim_failure_if_missing": "source side of edge coupling remains symbolic",
            "valid_for_claim": "false",
            "source_paths": source_path_string("539_doc", "725_blockers", "589_edge_template"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "contract_id": "ECSC726_3_qbar_XT",
            "coefficient": "qbar_XT",
            "meaning": "ordinary test-body X/edge response per mass",
            "required_source": "matter quotient theorem or source-backed test response",
            "required_units": "dimensionless charge per mass",
            "acceptance_gate": "qbar_XT=0 by universal matter descent or finite numeric sourced row",
            "current_status": "missing_or_retained_symbolic",
            "claim_failure_if_missing": "test side of edge coupling remains symbolic",
            "valid_for_claim": "false",
            "source_paths": source_path_string("581_doc", "725_blockers", "589_edge_template"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "contract_id": "ECSC726_4_bulk_edge_split",
            "coefficient": "Q_X=Q_bulk+Q_edge split",
            "meaning": "orthogonal decomposition preventing double-counted source charge",
            "required_source": "projection algebra or covariant phase-space split",
            "required_units": "structural theorem",
            "acceptance_gate": "bulk and edge charges are orthogonal under Pi_M^H/readout pairing",
            "current_status": "missing",
            "claim_failure_if_missing": "alpha_total can double-count the source",
            "valid_for_claim": "false",
            "source_paths": source_path_string("725_blockers", "587_equations"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "contract_id": "ECSC726_5_bound_curve",
            "coefficient": "alpha_bound(lambda)",
            "meaning": "claim-grade local R10 comparison curve",
            "required_source": "digitized/source-backed bound table with provenance and QA",
            "required_units": "dimensionless alpha versus meters",
            "acceptance_gate": "valid_for_claim=true rows with no MISSING markers",
            "current_status": "private_or_placeholder_only",
            "claim_failure_if_missing": "runner remains smoke/guardrail only",
            "valid_for_claim": "false",
            "source_paths": source_path_string("725_runner_status", "588_budget"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    tightest_lambda_m = tightest["lambda_m"]
    tightest_lambda_um = tightest["lambda_um"]
    tightest_ceiling = tightest["alpha_edge_ceiling"]
    source_backed_edge_row_template = [
        {
            "row_id": "SBER726_0_required_source_backed_row",
            "lambda_m": tightest_lambda_m,
            "lambda_um": tightest_lambda_um,
            "K_edge": "MISSING_SOURCE_BACKED_K_EDGE",
            "Qbar_edge_XH": "MISSING_SOURCE_BACKED_QBAR_EDGE_XH",
            "qbar_XT": "MISSING_SOURCE_BACKED_QBAR_XT",
            "alpha_edge_ceiling": tightest_ceiling,
            "alpha_edge_predicted": "MISSING_PRODUCT",
            "source_required": "parent edge kernel; Hamiltonian projection; matter quotient/test response",
            "diagnostic_status": "blocked_until_sources_exist",
            "valid_for_claim": "false",
            "source_paths": source_path_string("588_budget", "589_edge_template"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "row_id": "SBER726_1_equal_three_factor_budget",
            "lambda_m": tightest_lambda_m,
            "lambda_um": tightest_lambda_um,
            "K_edge": tightest["equal_three_factor_max"],
            "Qbar_edge_XH": tightest["equal_three_factor_max"],
            "qbar_XT": tightest["equal_three_factor_max"],
            "alpha_edge_ceiling": tightest_ceiling,
            "alpha_edge_predicted": tightest_ceiling,
            "source_required": "all three factors must be derived or measured below these values",
            "diagnostic_status": "budget_boundary_not_source_backed",
            "valid_for_claim": "false",
            "source_paths": source_path_string("588_budget", "589_edge_template"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "row_id": "SBER726_2_safe_under_budget_smoke",
            "lambda_m": tightest_lambda_m,
            "lambda_um": tightest_lambda_um,
            "K_edge": "0.1",
            "Qbar_edge_XH": "0.1",
            "qbar_XT": "0.1",
            "alpha_edge_ceiling": tightest_ceiling,
            "alpha_edge_predicted": "0.001",
            "source_required": "replace smoke factors with parent/source coefficients before any claim",
            "diagnostic_status": "smoke_under_private_budget_not_source_backed",
            "valid_for_claim": "false",
            "source_paths": source_path_string("588_budget", "589_edge_template"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    next_object_queue = [
        {
            "queue_id": "NOQ726_0_first",
            "target": "map DCdagger to vertical generator",
            "why_next": "this is the shortest theorem route to kill multiplier backreaction",
            "needed_artifact": "explicit DC operator, parent pairing, and v_X transformation law",
            "fallback": "source-backed edge row",
            "priority": "highest",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("588_adjoint", "589_certificate", "589_sources_required"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "queue_id": "NOQ726_1_second",
            "target": "source edge coefficient row at tightest lambda",
            "why_next": "if theorem-zero fails, the tightest local pressure target is already known",
            "needed_artifact": "lambda_edge, K_edge, Qbar_edge_XH, qbar_XT, alpha_bound provenance",
            "fallback": "keep R10/local claims blocked",
            "priority": "high",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("588_budget", "589_edge_template", "725_blockers"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    decision_matrix = [
        {
            "decision_id": "D726_0_parent_owner_map_written",
            "decision": "parent owner map is explicit but incomplete",
            "meaning": "the route is not vague now: missing objects are named and source-linked",
            "claim_status": "nonclaim_mapping",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("725_vdef_repair", "587_source_map", "589_sources_required"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D726_1_owner_route_not_promoted",
            "decision": "do not promote Vdef/no-pole/local-GR",
            "meaning": "H_ZZ=0 plus affine variation is still insufficient without owner/backreaction/boundary/matter gates",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("587_equations", "588_adjoint"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D726_2_edge_source_contract_written",
            "decision": "surviving edge coefficients now have exact source requirements",
            "meaning": "lambda_edge, K_edge, Qbar_edge_XH, qbar_XT, split, and bound curve cannot be handwaved",
            "claim_status": "nonclaim_contract",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("725_blockers", "589_edge_template"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D726_3_next_best_target",
            "decision": "map DCdagger or fill edge row source",
            "meaning": "next work either closes theorem-zero or starts the tightest source-backed coefficient row",
            "claim_status": "next_derivation_target",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("589_doc", "589_certificate"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    nonclaim_summary = [
        {
            "status": "Y5_R10_726_Vdef_parent_owner_map_written_edge_coefficient_source_contract_written_nonclaim",
            "claim_ceiling": "parent_owner_mapping_and_edge_source_contract_only_no_R10_WEP_PPN_Newton_or_local_GR_pass",
            "main_result": "the coupling problem is split into parent-owner theorem requirements versus explicit edge coefficient source requirements",
            "hard_blocker": "DCdagger-to-vertical-generator map, parent pairing, C_X identity, boundary silence, projector owner, and matter quotient remain unsigned",
            "tightest_private_edge_target": f"lambda_um={tightest_lambda_um};alpha_edge_ceiling={tightest_ceiling}",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("725_doc", "587_doc", "588_doc", "589_doc"),
            "generated_utc": GENERATED_UTC,
        }
    ]

    outputs = {
        "source_register": (
            RESIDUALS / "P8_Y5_R10_726_SOURCE_REGISTER.csv",
            source_register,
            ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"],
        ),
        "parent_owner_map": (
            RESIDUALS / "P8_Y5_R10_726_PARENT_OWNER_MAP.csv",
            parent_owner_map,
            [
                "owner_id",
                "needed_object",
                "role",
                "candidate_source",
                "required_equation",
                "current_status",
                "claim_effect",
                "fallback_if_missing",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "owner_promotion_gate": (
            RESIDUALS / "P8_Y5_R10_726_OWNER_PROMOTION_GATE.csv",
            owner_promotion_gate,
            ["gate_id", "claim_condition", "current_result", "why", "if_fail", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "edge_coefficient_source_contract": (
            RESIDUALS / "P8_Y5_R10_726_EDGE_COEFFICIENT_SOURCE_CONTRACT.csv",
            edge_coefficient_source_contract,
            [
                "contract_id",
                "coefficient",
                "meaning",
                "required_source",
                "required_units",
                "acceptance_gate",
                "current_status",
                "claim_failure_if_missing",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "source_backed_edge_row_template": (
            RESIDUALS / "P8_Y5_R10_726_SOURCE_BACKED_EDGE_ROW_TEMPLATE.csv",
            source_backed_edge_row_template,
            [
                "row_id",
                "lambda_m",
                "lambda_um",
                "K_edge",
                "Qbar_edge_XH",
                "qbar_XT",
                "alpha_edge_ceiling",
                "alpha_edge_predicted",
                "source_required",
                "diagnostic_status",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "next_object_queue": (
            RESIDUALS / "P8_Y5_R10_726_NEXT_OBJECT_QUEUE.csv",
            next_object_queue,
            ["queue_id", "target", "why_next", "needed_artifact", "fallback", "priority", "next_target", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "decision_matrix": (
            RESIDUALS / "P8_Y5_R10_726_DECISION_MATRIX.csv",
            decision_matrix,
            ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "nonclaim_summary": (
            RESIDUALS / "P8_Y5_R10_726_NONCLAIM_SUMMARY.csv",
            nonclaim_summary,
            [
                "status",
                "claim_ceiling",
                "main_result",
                "hard_blocker",
                "tightest_private_edge_target",
                "next_target",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
    }

    for path, rows, fields in outputs.values():
        write_csv(path, rows, fields)

    generated_paths = [path for path, _, _ in outputs.values()]
    formalization_count = formalization_changed_after_cutoff()
    edge_contract_coefficients = {row["coefficient"] for row in edge_coefficient_source_contract}
    parent_objects = {row["needed_object"] for row in parent_owner_map}
    validations = [
        {
            "check_id": "V726_0_source_paths_exist",
            "result": "pass" if all(info["path"].exists() for info in SOURCES.values()) else "fail",
            "detail": "all cited source paths exist",
        },
        {
            "check_id": "V726_1_source_needles_present",
            "result": "pass" if all(text_contains(info["path"], info["needles"]) for info in SOURCES.values()) else "fail",
            "detail": "all source files contain expected evidence needles",
        },
        {
            "check_id": "V726_2_prior_725_clean",
            "result": "pass" if prior_validation_clean(SOURCES["725_validation"]["path"]) else "fail",
            "detail": "725 validation has no failures",
        },
        {
            "check_id": "V726_3_725_selected_726",
            "result": "pass" if csv_contains(SOURCES["725_doc"]["path"], "726-Y5-R10-Vdef-parent-owner-map-or-edge-coefficient-source-contract.md") else "fail",
            "detail": "725 selected this checkpoint",
        },
        {
            "check_id": "V726_4_parent_owner_map_complete",
            "result": "pass"
            if len(parent_owner_map) >= 10
            and any("DC" in obj for obj in parent_objects)
            and any("matter" in obj for obj in parent_objects)
            else "fail",
            "detail": f"owner_rows={len(parent_owner_map)}",
        },
        {
            "check_id": "V726_5_owner_promotion_blocks_claim",
            "result": "pass" if all(row["valid_for_claim"] == "false" and row["current_result"] != "pass" for row in owner_promotion_gate) else "fail",
            "detail": f"owner_gate_rows={len(owner_promotion_gate)};claim_rows=0",
        },
        {
            "check_id": "V726_6_edge_coefficient_contract_complete",
            "result": "pass"
            if {"lambda_edge", "K_edge(lambda)", "Qbar_edge_XH(lambda)", "qbar_XT", "Q_X=Q_bulk+Q_edge split", "alpha_bound(lambda)"}.issubset(edge_contract_coefficients)
            and all(row["valid_for_claim"] == "false" for row in edge_coefficient_source_contract)
            else "fail",
            "detail": f"edge_contract_rows={len(edge_coefficient_source_contract)}",
        },
        {
            "check_id": "V726_7_tightest_edge_row_template_nonclaim",
            "result": "pass"
            if tightest_lambda_um == "608.0783"
            and tightest_ceiling == "0.00234471960478"
            and all(row["valid_for_claim"] == "false" for row in source_backed_edge_row_template)
            else "fail",
            "detail": f"tightest_lambda_um={tightest_lambda_um};tightest_ceiling={tightest_ceiling}",
        },
        {
            "check_id": "V726_8_old_587_588_589_integrated",
            "result": "pass"
            if csv_contains(SOURCES["587_source_map"]["path"], "P^{mu nu}[Y]")
            and csv_contains(SOURCES["588_adjoint"]["path"], "(DC)^dagger X")
            and csv_contains(SOURCES["589_certificate"]["path"], "AZC589_0_adjoint_as_vertical_generator")
            else "fail",
            "detail": "affine map, adjoint theorem, and certificate skeleton integrated",
        },
        {
            "check_id": "V726_9_next_target_selected",
            "result": "pass" if all(row["next_target"] == NEXT_TARGET for row in decision_matrix) else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V726_10_no_claim_rows_promoted",
            "result": "pass" if all_valid_false(generated_paths) else "fail",
            "detail": "all generated rows with valid_for_claim remain false",
        },
        {
            "check_id": "V726_11_outputs_scoped",
            "result": "pass" if under_post_checkpoint([OUTPUT_DOC, *generated_paths]) else "fail",
            "detail": "all outputs under post-checkpoint-work",
        },
        {
            "check_id": "V726_12_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V726_13_no_local_arena_claim",
            "result": "pass" if "no_R10_WEP_PPN_Newton_or_local_GR_pass" in nonclaim_summary[0]["claim_ceiling"] else "fail",
            "detail": "R10/WEP/PPN/Newton/local-GR claims remain blocked",
        },
        {
            "check_id": "V726_14_source_register_written",
            "result": "pass" if len(source_register) >= 18 else "fail",
            "detail": f"source_rows={len(source_register)}",
        },
        {
            "check_id": "V726_15_runner_refusal_retained",
            "result": "pass" if csv_contains(SOURCES["725_runner_status"]["path"], "claim_allowed", "false") else "fail",
            "detail": "725 runner refusal remains the active guardrail",
        },
        {
            "check_id": "V726_16_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]

    validation_path = RESIDUALS / "P8_Y5_BRR545_726_VALIDATION.csv"
    write_csv(validation_path, validations, ["check_id", "result", "detail"])

    doc = f"""# 726 - Y5 R10 Vdef Parent Owner Map Or Edge Coefficient Source Contract

## Summary

This checkpoint makes the coupling problem explicit.

There are now two honest routes:

1. **Parent-owner route**: prove the affine/topological `V_def` branch is owned by the parent action, with `DCdagger` mapping to the vertical generator and no proper stabilizers.
2. **Edge-source route**: if the owner route does not close, source the surviving coefficients `lambda_edge`, `K_edge(lambda)`, `Qbar_edge_XH(lambda)`, `qbar_XT`, the bulk/edge split, and `alpha_bound(lambda)`.

Current verdict: **nonclaim**. The route is sharper, but no local-GR/R10/PPN/WEP/Newton claim is promoted.

| Field | Value |
| --- | --- |
| Generated UTC | `{GENERATED_UTC}` |
| Claim status | private/nonclaim checkpoint |
| Tightest private edge target | `lambda_um={tightest_lambda_um}; alpha_edge_ceiling={tightest_ceiling}` |
| Next target | `{NEXT_TARGET}` |

## Parent Owner Map

{markdown_table(parent_owner_map, ["owner_id", "needed_object", "current_status", "claim_effect", "fallback_if_missing", "valid_for_claim"])}

## Owner Promotion Gate

{markdown_table(owner_promotion_gate, ["gate_id", "claim_condition", "current_result", "if_fail", "valid_for_claim"])}

## Edge Coefficient Source Contract

{markdown_table(edge_coefficient_source_contract, ["contract_id", "coefficient", "required_source", "acceptance_gate", "current_status", "claim_failure_if_missing", "valid_for_claim"])}

## Source-Backed Edge Row Template

{markdown_table(source_backed_edge_row_template, ["row_id", "lambda_um", "K_edge", "Qbar_edge_XH", "qbar_XT", "alpha_edge_ceiling", "alpha_edge_predicted", "diagnostic_status", "valid_for_claim"])}

## Next Object Queue

{markdown_table(next_object_queue, ["queue_id", "target", "why_next", "needed_artifact", "priority", "next_target", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decision_matrix, ["decision_id", "decision", "claim_status", "next_target", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(nonclaim_summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "tightest_private_edge_target", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_register, ["source_id", "path", "exists", "needle_check", "role"])}

## Validation

{markdown_table(validations, ["check_id", "result", "detail"])}

## Practical Read

This is the coupling problem in a cleaner box. If the theory can map `(DC)^dagger X` to the actual vertical generator and prove proper stabilizers vanish, the local branch can still become a theorem-zero route. If not, the surviving coupling is not allowed to hide: it needs sourced `lambda_edge`, `K_edge`, `Qbar_edge_XH`, and `qbar_XT` rows, with the tightest private pressure currently near `608.0783 um`.
"""

    OUTPUT_DOC.write_text(doc, encoding="utf-8")
    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {validation_path}")
    print(f"validation_passes={sum(row['result'] == 'pass' for row in validations)}/{len(validations)}")
    print(f"tightest_edge_target=lambda_um:{tightest_lambda_um};alpha:{tightest_ceiling}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
