from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_no_pole_quotient_LX_route_attempted_q_kernel_inherited_full_no_pole_and_sourcefree_proof_unsigned_nonclaim"
CLAIM_CEILING = "conditional_no_pole_and_positive_sourcefree_proof_audit_only_no_KX_zero_no_qbar_zero_no_R10_no_R11_no_local_GR_claim"
NEXT_TARGET = "671-Y5-R10-parent-Omega-DCX-boundary-charge-owner-or-edge-residual-vector.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "670-Y5-R10-no-pole-quotient-LX-route-or-positive-sourcefree-operator-proof.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "506_energy_identity": RESIDUALS / "P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
    "581_doc": ROOT / "581-Y5-R10-quotient-vertical-no-pole-parent-theorem-attempt.md",
    "581_validation": RESIDUALS / "P8_Y5_BRR545_581_VALIDATION.csv",
    "581_chain": RESIDUALS / "P8_Y5_R10_581_QUOTIENT_VERTICAL_THEOREM_CHAIN.csv",
    "581_certificate": RESIDUALS / "P8_Y5_R10_581_NO_POLE_CERTIFICATE_TEMPLATE.csv",
    "581_boundary": RESIDUALS / "P8_Y5_R10_581_BOUNDARY_CHARGE_AUDIT.csv",
    "582_doc": ROOT / "582-Y5-R10-boundary-charge-and-constraint-algebra-no-pole-audit.md",
    "582_validation": RESIDUALS / "P8_Y5_BRR545_582_VALIDATION.csv",
    "582_nopole_gates": RESIDUALS / "P8_Y5_R10_582_NOPOLE_GATE_STATUS.csv",
    "590_doc": ROOT / "590-Y5-R10-map-DCdagger-to-vertical-generator-or-fill-edge-row-source.md",
    "590_validation": RESIDUALS / "P8_Y5_BRR545_590_VALIDATION.csv",
    "590_dc_map": RESIDUALS / "P8_Y5_R10_590_DCDAGGER_VERTICAL_MAP.csv",
    "590_field_map": RESIDUALS / "P8_Y5_R10_590_FIELD_BY_FIELD_VERTICAL_ACTION_MAP.csv",
    "618_doc": ROOT / "618-Y5-R10-no-pole-source-zero-certificate-after-finite-branch-demotion.md",
    "618_validation": RESIDUALS / "P8_Y5_BRR545_618_VALIDATION.csv",
    "618_nopole_audit": RESIDUALS / "P8_Y5_R10_618_NO_POLE_CERTIFICATE_AUDIT.csv",
    "618_source_zero": RESIDUALS / "P8_Y5_R10_618_SOURCE_ZERO_CERTIFICATE_AUDIT.csv",
    "618_closed_zero": RESIDUALS / "P8_Y5_R10_618_CLOSED_ZERO_ROWS.csv",
    "637_doc": ROOT / "637-Y5-R10-parent-action-quotient-map-and-constant-ownership-derivation.md",
    "637_validation": RESIDUALS / "P8_Y5_BRR545_637_VALIDATION.csv",
    "637_q_map": RESIDUALS / "P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv",
    "669_doc": ROOT / "669-Y5-R10-minimal-LX-sector-operator-owner-or-retained-residual-vector.md",
    "669_validation": RESIDUALS / "P8_Y5_BRR545_669_VALIDATION.csv",
    "669_candidates": RESIDUALS / "P8_Y5_R10_669_MINIMAL_LX_OPERATOR_CANDIDATES.csv",
    "669_gates": RESIDUALS / "P8_Y5_R10_669_LX_OWNER_GATE_TESTS.csv",
    "669_residuals": RESIDUALS / "P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv",
}


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for path in FORMALIZATION_WORKBENCH.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def validation_failures_for(source_id: str) -> list[dict[str, str]]:
    return [row for row in read_csv(SOURCE_PATHS[source_id]) if row.get("result") != "pass"]


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    roles = {
        "506_energy_identity": "positive/source-free operator theorem template",
        "581_doc": "conditional quotient-vertical no-pole theorem",
        "581_validation": "581 validation gate",
        "581_chain": "quotient-vertical theorem chain",
        "581_certificate": "no-pole certificate obligations",
        "581_boundary": "boundary charge audit",
        "582_doc": "constraint algebra and boundary charge no-pole audit",
        "582_validation": "582 validation gate",
        "582_nopole_gates": "no-pole gate status",
        "590_doc": "DCdagger to vertical generator map",
        "590_validation": "590 validation gate",
        "590_dc_map": "DCdagger/Omega-flat map rows",
        "590_field_map": "field-by-field vertical action map",
        "618_doc": "no-pole/source-zero certificate audit",
        "618_validation": "618 validation gate",
        "618_nopole_audit": "no-pole certificate audit rows",
        "618_source_zero": "source-zero certificate audit rows",
        "618_closed_zero": "direct representative-X smuggling closed row",
        "637_doc": "parent quotient map derivation",
        "637_validation": "637 validation gate",
        "637_q_map": "conditional q-map derivation rows",
        "669_doc": "immediate L_X owner/residual-vector handoff",
        "669_validation": "669 validation gate",
        "669_candidates": "minimal L_X branch candidates",
        "669_gates": "L_X owner gates",
        "669_residuals": "R10/R11 residual vector",
    }
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": bool_text(path.exists()),
            "role": roles[source_id],
            "generated_utc": now,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def no_pole_quotient_proof_chain_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "step_id": "NQ670_0_null_distribution",
            "claim": "define local Xhat directions as candidate null/representative directions N_X",
            "mathematical_form": "v_X in N_X subset T Conf_parent",
            "current_result": "conditional_setup_inherited",
            "what_is_proved_now": "if N_X is parent-owned as presymplectic-null/relative-exact, it is a quotient direction",
            "missing_for_claim": "prove actual local Xhat variations are exactly in N_X with vanishing local boundary primitive",
            "claim_effect": "no K_X zero yet",
            "valid_for_claim": "false",
            "source_paths": source_list("637_q_map", "581_chain", "669_candidates"),
            "generated_utc": now,
        },
        {
            "step_id": "NQ670_1_canonical_quotient",
            "claim": "construct q as canonical reduced-space projection",
            "mathematical_form": "q: Conf_parent -> Q_obs = Conf_parent / N_X",
            "current_result": "conditional_math_pass",
            "what_is_proved_now": "if N_X is integrable and parent-invariant, q is not an arbitrary closure axiom",
            "missing_for_claim": "integrability, domain admissibility, and invariance of N_X under parent symmetries",
            "claim_effect": "Dq kernel can be used conditionally",
            "valid_for_claim": "false",
            "source_paths": source_list("637_q_map", "581_chain"),
            "generated_utc": now,
        },
        {
            "step_id": "NQ670_2_kernel_transfer",
            "claim": "vertical Xhat variations lie in the differential kernel of q",
            "mathematical_form": "Dq[v_X]=0",
            "current_result": "partial_zero_kernel_inherited",
            "what_is_proved_now": "this kernel statement follows as math once v_X is tangent to the quotient fibre",
            "missing_for_claim": "does not by itself prove no physical pole, no boundary charge, or no constant/material coupling",
            "claim_effect": "closes only representative-choice leakage, not full R10",
            "valid_for_claim": "false",
            "source_paths": source_list("637_q_map", "618_closed_zero"),
            "generated_utc": now,
        },
        {
            "step_id": "NQ670_3_action_descent",
            "claim": "bulk action descends along q",
            "mathematical_form": "S_bulk[Phi]=S_red[q(Phi)] + boundary/domain terms",
            "current_result": "conditional_only",
            "what_is_proved_now": "if true, first variation along v_X is zero before local field equations",
            "missing_for_claim": "boundary/domain terms and actual parent Lagrangian are not signed",
            "claim_effect": "bulk Hessian degeneracy remains conditional",
            "valid_for_claim": "false",
            "source_paths": source_list("581_chain", "637_doc", "669_gates"),
            "generated_utc": now,
        },
        {
            "step_id": "NQ670_4_no_bulk_hessian_block",
            "claim": "no physical X Hessian/pole exists in the descended bulk action",
            "mathematical_form": "H(v_X,.)=0 modulo constraints; no inverse O_X^{-1}",
            "current_result": "conditional_not_promoted",
            "what_is_proved_now": "if the action truly factors through q, a vertical Green function is absent",
            "missing_for_claim": "parent Omega, DC_X, vertical generator, and degree count are unfilled",
            "claim_effect": "K_X=0 not promoted",
            "valid_for_claim": "false",
            "source_paths": source_list("581_chain", "590_dc_map", "618_nopole_audit"),
            "generated_utc": now,
        },
        {
            "step_id": "NQ670_5_matter_descent",
            "claim": "ordinary matter is blind to vertical Xhat geometry directions",
            "mathematical_form": "S_matter=Sbar_m[Obs(q(Phi)),psi,theta_A] and Lie_vX(theta_A)=0",
            "current_result": "geometry_chain_rule_conditional_constants_open",
            "what_is_proved_now": "geometry pullback term dies if matter descends through q",
            "missing_for_claim": "constant/material-marker ownership and no-extension theorem",
            "claim_effect": "qbar_XT=0 not promoted",
            "valid_for_claim": "false",
            "source_paths": source_list("618_source_zero", "637_doc", "669_residuals"),
            "generated_utc": now,
        },
        {
            "step_id": "NQ670_6_constraint_generator",
            "claim": "C_X is a first-class momentum-map generator of the vertical direction",
            "mathematical_form": "delta G_X = Omega(delta Phi, v_X), G_X=int epsilon C_X + Q_X",
            "current_result": "blocked_parent_Omega_DCX_missing",
            "what_is_proved_now": "590 fixes the category: DCdagger X is Omega-flat(v_X), not v_X itself",
            "missing_for_claim": "explicit parent Omega, DC_X, vertical action on all fields, and reduced nondegeneracy",
            "claim_effect": "no first-class no-pole credit",
            "valid_for_claim": "false",
            "source_paths": source_list("590_dc_map", "590_field_map", "582_nopole_gates"),
            "generated_utc": now,
        },
        {
            "step_id": "NQ670_7_boundary_and_degree_count",
            "claim": "boundary charge is zero and constraints remove the local X pair",
            "mathematical_form": "Q_X=0, K_boundary=0, primary+secondary first-class pair removes X",
            "current_result": "blocked_boundary_and_bracket_not_silenced",
            "what_is_proved_now": "the exact boundary/Dirac gate is known",
            "missing_for_claim": "differentiable zero charge, bracket closure, no edge mode, and phase-space degree count",
            "claim_effect": "Qbar_XH=0 and K_X=0 not promoted",
            "valid_for_claim": "false",
            "source_paths": source_list("581_boundary", "582_nopole_gates", "618_nopole_audit"),
            "generated_utc": now,
        },
        {
            "step_id": "NQ670_8_no_pole_result",
            "claim": "full no-pole theorem would remove the R10 X row",
            "mathematical_form": "Dq[v_X]=0 plus first-class/boundary-silent quotient => K_X=qbar_XT=Qbar_XH=0",
            "current_result": "not_passed",
            "what_is_proved_now": "proof route is sharply specified and partially supported by q-kernel math",
            "missing_for_claim": "NQ670_0 through NQ670_7 must all be parent-signed together",
            "claim_effect": "finite/edge/source residual vector retained",
            "valid_for_claim": "false",
            "source_paths": source_list("581_chain", "618_nopole_audit", "669_residuals"),
            "generated_utc": now,
        },
    ]


def vertical_generator_certificate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "certificate_id": "VGC670_0_parent_Omega",
            "required_object": "parent presymplectic potential and Omega",
            "mathematical_need": "Omega_Y(delta Y,v_X) is the covector identified with DCdagger X",
            "current_status": "missing",
            "if_filled": "turns DCdagger map into a real generator test",
            "if_missing": "vertical generator remains category-correct but unowned",
            "valid_for_claim": "false",
            "source_paths": source_list("590_dc_map", "590_doc"),
            "generated_utc": now,
        },
        {
            "certificate_id": "VGC670_1_DCX_operator",
            "required_object": "linearized constraint operator DC_X",
            "mathematical_need": "delta C_X[delta Y] must be computable before adjoint/zero-mode claims",
            "current_status": "missing",
            "if_filled": "lets the adjoint certificate be checked",
            "if_missing": "C_X could be an inserted identity rather than parent current",
            "valid_for_claim": "false",
            "source_paths": source_list("590_dc_map", "582_doc"),
            "generated_utc": now,
        },
        {
            "certificate_id": "VGC670_2_field_action",
            "required_object": "v_X action on each parent field",
            "mathematical_need": "v_X[g], v_X[Pi], v_X[Gamma/Khat/q_loc], v_X[memory], v_X[matter], v_X[boundary]",
            "current_status": "partially_mapped_not_declared",
            "if_filled": "prevents hidden sectors from keeping a pole/source",
            "if_missing": "no-pole theorem can fail by unmapped field block",
            "valid_for_claim": "false",
            "source_paths": source_list("590_field_map", "669_residuals"),
            "generated_utc": now,
        },
        {
            "certificate_id": "VGC670_3_reduced_nondegeneracy",
            "required_object": "nondegenerate reduced Omega after quotient",
            "mathematical_need": "DCdagger X=0 should imply v_X=0 modulo proper gauge only",
            "current_status": "not_checked",
            "if_filled": "kills fake zero modes/stabilizers",
            "if_missing": "zero covector may be ordinary degeneracy, not no-pole proof",
            "valid_for_claim": "false",
            "source_paths": source_list("590_dc_map", "618_nopole_audit"),
            "generated_utc": now,
        },
        {
            "certificate_id": "VGC670_4_boundary_differentiability",
            "required_object": "differentiable generator with zero boundary charge",
            "mathematical_need": "delta G_X has no uncancelled boundary variation and Q_X=0",
            "current_status": "not_derived",
            "if_filled": "removes edge hair from Qbar_XH",
            "if_missing": "boundary edge residual must be scored",
            "valid_for_claim": "false",
            "source_paths": source_list("581_boundary", "582_nopole_gates"),
            "generated_utc": now,
        },
        {
            "certificate_id": "VGC670_5_bracket_closure",
            "required_object": "first-class constraint algebra",
            "mathematical_need": "{G[epsilon],G[eta]}=G[[epsilon,eta]] with K_boundary=0",
            "current_status": "not_computed",
            "if_filled": "vertical variables are gauge, not physical/second-class leftovers",
            "if_missing": "rank-zero alone is not no-pole",
            "valid_for_claim": "false",
            "source_paths": source_list("582_nopole_gates", "618_nopole_audit"),
            "generated_utc": now,
        },
        {
            "certificate_id": "VGC670_6_matter_quotient",
            "required_object": "matter functor and constants descend to q",
            "mathematical_need": "delta_v S_matter=0 including theta_A and material labels",
            "current_status": "constants_and_markers_open",
            "if_filled": "qbar_XT can be theorem-zero",
            "if_missing": "source/test charge residual remains live",
            "valid_for_claim": "false",
            "source_paths": source_list("618_source_zero", "637_doc"),
            "generated_utc": now,
        },
        {
            "certificate_id": "VGC670_7_domain_guard",
            "required_object": "compact local branch/domain admissibility",
            "mathematical_need": "quotient silence must not overkill cosmology/galaxies/memory sectors",
            "current_status": "guarded_scope_required",
            "if_filled": "local theorem can be scoped without flattening global phenomenology",
            "if_missing": "local no-pole result risks being too broad or too narrow",
            "valid_for_claim": "false",
            "source_paths": source_list("637_q_map", "669_doc"),
            "generated_utc": now,
        },
    ]


def positive_sourcefree_proof_chain_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "step_id": "PSF670_0_operator_form",
            "claim": "physical X branch uses a positive local operator",
            "mathematical_form": "O_X X = -nabla_i(Z_X nabla^i X)+M_X^2 X",
            "current_result": "template_only",
            "needed_to_close": "parent-signed Z_X, M_X^2, field units, and local domain",
            "if_fails": "operator remains residual R11/R10 input",
            "valid_for_claim": "false",
            "source_paths": source_list("506_energy_identity", "669_candidates", "669_residuals"),
            "generated_utc": now,
        },
        {
            "step_id": "PSF670_1_energy_identity",
            "claim": "multiply by X and integrate on compact exterior",
            "mathematical_form": "int_A (Z_X |grad X|^2 + M_X^2 X^2) = int_A X J_X + boundary_flux_X",
            "current_result": "conditional_math_valid",
            "needed_to_close": "operator must be self-adjoint and boundary terms owned",
            "if_fails": "positive no-hair identity cannot be used",
            "valid_for_claim": "false",
            "source_paths": source_list("506_energy_identity", "669_residuals"),
            "generated_utc": now,
        },
        {
            "step_id": "PSF670_2_positive_kinetic",
            "claim": "Z_X>0",
            "mathematical_form": "quadratic kinetic Hessian is positive in local branch",
            "current_result": "missing_parent_input",
            "needed_to_close": "second variation Hessian and normalization",
            "if_fails": "ghost/anti-elliptic/indefinite residual must be scored",
            "valid_for_claim": "false",
            "source_paths": source_list("669_gates", "669_residuals"),
            "generated_utc": now,
        },
        {
            "step_id": "PSF670_3_positive_mass_gap",
            "claim": "M_X^2>0",
            "mathematical_form": "local Hessian curvature in X direction is positive",
            "current_result": "missing_parent_input",
            "needed_to_close": "parent-owned mass gap and lambda_X units",
            "if_fails": "long-range/tachyonic/zero mode remains",
            "valid_for_claim": "false",
            "source_paths": source_list("669_gates", "669_residuals"),
            "generated_utc": now,
        },
        {
            "step_id": "PSF670_4_source_zero",
            "claim": "J_X=0",
            "mathematical_form": "delta_X S_matter + hidden/source terms vanish",
            "current_result": "missing_source_zero_proof",
            "needed_to_close": "matter quotient and no-marker/constant ownership",
            "if_fails": "qbar_XT or source coupling becomes finite residual",
            "valid_for_claim": "false",
            "source_paths": source_list("618_source_zero", "637_doc", "669_residuals"),
            "generated_utc": now,
        },
        {
            "step_id": "PSF670_5_boundary_flux_zero",
            "claim": "boundary_flux_X=0",
            "mathematical_form": "int_boundary X Z_X n.grad X = 0 or exact/proper-gauge killed",
            "current_result": "missing_boundary_lock",
            "needed_to_close": "boundary class/no-hair/projector silence",
            "if_fails": "edge/source residual remains",
            "valid_for_claim": "false",
            "source_paths": source_list("581_boundary", "582_nopole_gates", "669_residuals"),
            "generated_utc": now,
        },
        {
            "step_id": "PSF670_6_zero_profile_result",
            "claim": "positive source-free branch gives X=0",
            "mathematical_form": "Z_X>0, M_X^2>0, J_X=0, boundary_flux_X=0 => X=0",
            "current_result": "conditional_theorem_only",
            "needed_to_close": "PSF670_0 through PSF670_5 must all be signed together",
            "if_fails": "alpha/lambda residual vector retained",
            "valid_for_claim": "false",
            "source_paths": source_list("506_energy_identity", "669_candidates", "669_gates"),
            "generated_utc": now,
        },
        {
            "step_id": "PSF670_7_R10_R11_result",
            "claim": "positive sourcefree proof would silence local R10/R11 X residuals",
            "mathematical_form": "X=0 on local exterior removes active profile even if a formal pole exists",
            "current_result": "not_promoted",
            "needed_to_close": "zero profile plus no edge/source substitute",
            "if_fails": "R10/R11 residual rows remain invalid-for-claim but live",
            "valid_for_claim": "false",
            "source_paths": source_list("669_residuals", "618_nopole_audit"),
            "generated_utc": now,
        },
    ]


def branch_comparison_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "branch_id": "BC670_0_no_pole_quotient",
            "route": "quotient/no-pole",
            "best_use": "local GR-style structural reduction",
            "current_strength": "strongest_if_parent_Omega_DCX_boundary_close",
            "hardest_blocker": "parent Omega/DC_X plus zero boundary charge",
            "fallback": "edge/source residual vector",
            "rank": "1",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "branch_id": "BC670_1_positive_sourcefree",
            "route": "positive source-free operator",
            "best_use": "prove X profile vanishes even if formal physical mode exists",
            "current_strength": "good_conditional_theorem_but_many_parent_inputs_missing",
            "hardest_blocker": "Z_X, M_X^2, J_X=0, boundary_flux_X=0 together",
            "fallback": "finite alpha/lambda score",
            "rank": "2",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "branch_id": "BC670_2_finite_residual",
            "route": "sourced residual vector",
            "best_use": "honest empirical scoring if derivation routes fail",
            "current_strength": "schema_ready_from_669",
            "hardest_blocker": "real parent/source-backed coefficients and units",
            "fallback": "R10/R11 bound-input acquisition",
            "rank": "3",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "branch_id": "BC670_3_countermodel_guard",
            "route": "universal conformal or edge-mode counterexample",
            "best_use": "red-team against fake source-zero/no-pole claims",
            "current_strength": "keeps proof honest",
            "hardest_blocker": "must be explicitly forbidden by parent action, not disliked",
            "fallback": "finite qbar/Qbar/K_X rows",
            "rank": "guardrail",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def r10_r11_zero_or_residual_effect_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "effect_id": "ZE670_0_K_X",
            "target": "K_X=0",
            "zero_route": "full no-pole quotient with no physical Green function",
            "current_status": "MISSING_NO_POLE_CERTIFICATE",
            "why_not_zero_now": "parent Omega/DC_X, first-class closure, and boundary silence are not signed",
            "residual_if_fail": "K_X finite coefficient row from 669",
            "valid_for_claim": "false",
            "source_paths": source_list("618_nopole_audit", "669_residuals"),
            "generated_utc": now,
        },
        {
            "effect_id": "ZE670_1_qbar_XT",
            "target": "qbar_XT=0",
            "zero_route": "matter action and constants descend through q",
            "current_status": "MISSING_MATTER_CONSTANT_OWNERSHIP",
            "why_not_zero_now": "constant/material-marker and no-extension clauses remain open",
            "residual_if_fail": "test-body source charge row from 669",
            "valid_for_claim": "false",
            "source_paths": source_list("618_source_zero", "637_doc", "669_residuals"),
            "generated_utc": now,
        },
        {
            "effect_id": "ZE670_2_Qbar_XH",
            "target": "Qbar_XH=0",
            "zero_route": "boundary charge is zero/exact/proper-gauge and mass projector ignores edge mode",
            "current_status": "MISSING_BOUNDARY_CHARGE_ZERO",
            "why_not_zero_now": "Q_X, K_boundary, and Pi_M^H boundary projection are unclosed",
            "residual_if_fail": "source-body/edge charge row from 669",
            "valid_for_claim": "false",
            "source_paths": source_list("581_boundary", "582_nopole_gates", "669_residuals"),
            "generated_utc": now,
        },
        {
            "effect_id": "ZE670_3_X_profile",
            "target": "X=0 in compact local exterior",
            "zero_route": "positive source-free operator identity",
            "current_status": "MISSING_Z_M_J_BOUNDARY_INPUTS",
            "why_not_zero_now": "Z_X, M_X^2, J_X=0, and boundary_flux_X=0 are not all signed",
            "residual_if_fail": "finite profile alpha/lambda residual",
            "valid_for_claim": "false",
            "source_paths": source_list("506_energy_identity", "669_residuals"),
            "generated_utc": now,
        },
        {
            "effect_id": "ZE670_4_direct_q_loc_X_smuggling",
            "target": "Lie_vX(q_loc)=0",
            "zero_route": "Q_obs pullback for Gamma_eff/Khat/P_loc/connection/reference",
            "current_status": "PARTIAL_ZERO_ROW_RETAINED",
            "why_not_zero_now": "this is vertical-blindness only; it is not q_loc=0 or no-pole",
            "residual_if_fail": "observed q_loc residual remains live",
            "valid_for_claim": "false",
            "source_paths": source_list("618_closed_zero", "637_q_map"),
            "generated_utc": now,
        },
        {
            "effect_id": "ZE670_5_R10_R11",
            "target": "R10/R11 local branch",
            "zero_route": "either no-pole quotient or positive sourcefree theorem closes all relevant channels",
            "current_status": "NO_CLAIM",
            "why_not_zero_now": "no branch currently signs all required clauses",
            "residual_if_fail": "R10/R11 residual vector retained and later sourced",
            "valid_for_claim": "false",
            "source_paths": source_list("669_residuals", "669_doc"),
            "generated_utc": now,
        },
    ]


def evaluator_rows(
    no_pole_rows: list[dict[str, str]],
    vertical_rows: list[dict[str, str]],
    sourcefree_rows: list[dict[str, str]],
    effect_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    all_nonclaim = all(
        row["valid_for_claim"] == "false"
        for row in no_pole_rows + vertical_rows + sourcefree_rows + effect_rows
    )
    return [
        {
            "evaluator_id": "EV670_0_no_pole_attempt",
            "target": "promote K_X=0 by quotient/no-pole",
            "status": "fail_nonclaim",
            "reason": "q-kernel math is inherited conditionally, but parent Omega/DC_X, first-class closure, and boundary silence are unsigned",
            "claim_effect": "no K_X=0, no R10, no local-GR claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV670_1_sourcefree_attempt",
            "target": "prove X=0 by positive source-free operator",
            "status": "fail_nonclaim",
            "reason": "energy identity is valid as a conditional theorem, but Z_X, M_X^2, J_X=0, and boundary_flux_X=0 are missing",
            "claim_effect": "no X-profile-zero claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV670_2_partial_zero",
            "target": "retain closed direct q_loc vertical-blind row",
            "status": "pass_nonclaim",
            "reason": "Lie_vX(q_loc)=0 under Q_obs pullback remains a real internal zero row, but it is not a full local-GR result",
            "claim_effect": "narrows hidden-X leakage only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV670_3_next_route",
            "target": "select next target",
            "status": "parent_Omega_DCX_boundary_first",
            "reason": "this is the shortest route to turning the quotient theorem from conditional into owned no-pole structure",
            "claim_effect": "next derivation only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV670_4_safety",
            "target": "prevent claim promotion",
            "status": "pass" if all_nonclaim else "fail",
            "reason": "all proof, certificate, source-free, and effect rows remain invalid for claim",
            "claim_effect": "private nonclaim checkpoint",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D670_0",
            "status": STATUS,
            "meaning": "670 inherits a real conditional q-kernel/no-pole route but cannot promote K_X=0 or X=0 because the parent generator and boundary certificates remain unsigned",
            "claim_status": CLAIM_CEILING,
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, str]],
    no_pole_rows: list[dict[str, str]],
    vertical_rows: list[dict[str, str]],
    sourcefree_rows: list[dict[str, str]],
    branch_rows: list[dict[str, str]],
    effect_rows: list[dict[str, str]],
    evaluator_data: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    prior_validation_ids = ["581_validation", "582_validation", "590_validation", "618_validation", "637_validation", "669_validation"]
    prior_failures = {
        source_id: validation_failures_for(source_id)
        for source_id in prior_validation_ids
    }
    prior_failure_count = sum(len(rows) for rows in prior_failures.values())
    no_pole_ids = {row["step_id"] for row in no_pole_rows}
    vertical_ids = {row["certificate_id"] for row in vertical_rows}
    sourcefree_ids = {row["step_id"] for row in sourcefree_rows}
    effect_targets = {row["target"] for row in effect_rows}
    all_generated_rows = no_pole_rows + vertical_rows + sourcefree_rows + branch_rows + effect_rows + evaluator_data + decision
    generated_outputs = [
        DOC_PATH,
        RESIDUALS / "P8_Y5_R10_670_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv",
        RESIDUALS / "P8_Y5_R10_670_VERTICAL_GENERATOR_CERTIFICATE.csv",
        RESIDUALS / "P8_Y5_R10_670_POSITIVE_SOURCEFREE_PROOF_CHAIN.csv",
        RESIDUALS / "P8_Y5_R10_670_BRANCH_COMPARISON.csv",
        RESIDUALS / "P8_Y5_R10_670_R10_R11_ZERO_OR_RESIDUAL_EFFECT.csv",
        RESIDUALS / "P8_Y5_R10_670_EVALUATOR.csv",
        RESIDUALS / "P8_Y5_R10_670_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_670_NONCLAIM_SUMMARY.csv",
    ]
    return [
        {
            "check_id": "V670_0_source_paths_exist",
            "result": "pass" if all(row["exists"] == "true" for row in source_rows) else "fail",
            "detail": "all cited source paths exist" if all(row["exists"] == "true" for row in source_rows) else "one or more cited source paths missing",
            "generated_utc": now,
        },
        {
            "check_id": "V670_1_prior_validations_clean",
            "result": "pass" if prior_failure_count == 0 else "fail",
            "detail": ";".join(f"{source_id}={len(rows)}" for source_id, rows in prior_failures.items()),
            "generated_utc": now,
        },
        {
            "check_id": "V670_2_no_pole_chain_coverage",
            "result": "pass" if len(no_pole_rows) >= 9 and "NQ670_8_no_pole_result" in no_pole_ids else "fail",
            "detail": f"no_pole_rows={len(no_pole_rows)} no_pole_result={'NQ670_8_no_pole_result' in no_pole_ids}",
            "generated_utc": now,
        },
        {
            "check_id": "V670_3_vertical_certificate_coverage",
            "result": "pass" if len(vertical_rows) >= 8 and "VGC670_0_parent_Omega" in vertical_ids and "VGC670_4_boundary_differentiability" in vertical_ids else "fail",
            "detail": f"vertical_rows={len(vertical_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "V670_4_positive_sourcefree_coverage",
            "result": "pass" if len(sourcefree_rows) >= 8 and "PSF670_6_zero_profile_result" in sourcefree_ids else "fail",
            "detail": f"sourcefree_rows={len(sourcefree_rows)} zero_profile={'PSF670_6_zero_profile_result' in sourcefree_ids}",
            "generated_utc": now,
        },
        {
            "check_id": "V670_5_effect_rows_cover_zero_targets",
            "result": "pass" if {"K_X=0", "qbar_XT=0", "Qbar_XH=0", "X=0 in compact local exterior"}.issubset(effect_targets) else "fail",
            "detail": ";".join(sorted(effect_targets)),
            "generated_utc": now,
        },
        {
            "check_id": "V670_6_no_claim_rows_promoted",
            "result": "pass" if all(row["valid_for_claim"] == "false" for row in all_generated_rows) else "fail",
            "detail": "all generated rows remain valid_for_claim=false",
            "generated_utc": now,
        },
        {
            "check_id": "V670_7_partial_zero_retained_but_not_promoted",
            "result": "pass"
            if any(row["target"] == "Lie_vX(q_loc)=0" and row["current_status"] == "PARTIAL_ZERO_ROW_RETAINED" for row in effect_rows)
            else "fail",
            "detail": "direct representative-X smuggling zero row retained only as nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "V670_8_next_target_selected",
            "result": "pass" if decision and decision[0]["next_action"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
            "generated_utc": now,
        },
        {
            "check_id": "V670_9_generated_outputs_scoped",
            "result": "pass" if all(str(path).startswith(str(ROOT)) for path in generated_outputs) else "fail",
            "detail": "all 670 outputs target post-checkpoint-work",
            "generated_utc": now,
        },
        {
            "check_id": "V670_10_formalization_workbench_untouched",
            "result": "pass" if formalization_changed_count() == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_changed_count()}",
            "generated_utc": now,
        },
        {
            "check_id": "V670_11_status_nonclaim",
            "result": "pass" if "no_KX_zero" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING else "fail",
            "detail": CLAIM_CEILING,
            "generated_utc": now,
        },
        {
            "check_id": "V670_12_evaluator_nonclaim_passes",
            "result": "pass" if any(row["status"] == "pass_nonclaim" for row in evaluator_data) and evaluator_data[-1]["status"] == "pass" else "fail",
            "detail": ";".join(row["status"] for row in evaluator_data),
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows(
    no_pole_rows: list[dict[str, str]],
    vertical_rows: list[dict[str, str]],
    sourcefree_rows: list[dict[str, str]],
    branch_rows: list[dict[str, str]],
    effect_rows: list[dict[str, str]],
    evaluator_data: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    failures = [row["check_id"] for row in validation if row["result"] != "pass"]
    hard_blockers = [
        "parent_Omega",
        "DC_X",
        "vertical_field_action",
        "boundary_charge_zero",
        "bracket_closure",
        "Z_X",
        "M_X2",
        "J_X_zero",
        "boundary_flux_X_zero",
    ]
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "no_pole_rows": str(len(no_pole_rows)),
            "vertical_certificate_rows": str(len(vertical_rows)),
            "sourcefree_rows": str(len(sourcefree_rows)),
            "branch_rows": str(len(branch_rows)),
            "effect_rows": str(len(effect_rows)),
            "evaluator_rows": str(len(evaluator_data)),
            "hard_blockers": ";".join(hard_blockers),
            "validation_failures": ";".join(failures),
            "next_target": NEXT_TARGET,
            "generated_utc": now,
        }
    ]


def cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, str]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |\n"
    separator = "| " + " | ".join("---" for _ in fields) + " |\n"
    body = "".join("| " + " | ".join(cell(row.get(field, "")) for field in fields) + " |\n" for row in rows)
    return header + separator + body


def write_document(
    source_rows: list[dict[str, str]],
    no_pole_rows: list[dict[str, str]],
    vertical_rows: list[dict[str, str]],
    sourcefree_rows: list[dict[str, str]],
    branch_rows: list[dict[str, str]],
    effect_rows: list[dict[str, str]],
    evaluator_data: list[dict[str, str]],
    decision: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    validation_table = markdown_table(validation, ["check_id", "result", "detail"]) if validation else "_Validation pending final write._\n"
    doc = f"""# 670 - Y5 R10 No-Pole Quotient L_X Route Or Positive Sourcefree Operator Proof

## Verdict

670 tried the best derivation route first.

Result: the quotient/no-pole branch has a real conditional spine, and one partial zero row remains genuinely useful:

```text
If local Xhat is a parent-owned presymplectic-null/relative-exact representative direction,
then q = Conf_parent / N_X gives Dq[v_X] = 0.
Under the existing Q_obs pullback contract, this retains Lie_vX(q_loc)=0.
```

But that is **not** yet `K_X=0`, `qbar_XT=0`, `Qbar_XH=0`, `X=0`, R10, R11, PPN, or local GR.

The full no-pole proof is blocked by parent `Omega/DC_X`, first-class bracket closure, and zero boundary charge. The positive source-free fallback is also blocked because `Z_X`, `M_X^2`, `J_X=0`, and `boundary_flux_X=0` are not parent-signed.

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "source_path", "exists", "role"])}

## No-Pole Quotient Proof Chain

{markdown_table(no_pole_rows, ["step_id", "claim", "mathematical_form", "current_result", "what_is_proved_now", "missing_for_claim", "claim_effect", "valid_for_claim"])}

## Vertical Generator Certificate

{markdown_table(vertical_rows, ["certificate_id", "required_object", "mathematical_need", "current_status", "if_filled", "if_missing", "valid_for_claim"])}

## Positive Sourcefree Proof Chain

{markdown_table(sourcefree_rows, ["step_id", "claim", "mathematical_form", "current_result", "needed_to_close", "if_fails", "valid_for_claim"])}

## Branch Comparison

{markdown_table(branch_rows, ["branch_id", "route", "best_use", "current_strength", "hardest_blocker", "fallback", "rank", "valid_for_claim"])}

## R10/R11 Zero Or Residual Effect

{markdown_table(effect_rows, ["effect_id", "target", "zero_route", "current_status", "why_not_zero_now", "residual_if_fail", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator_data, ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision, ["decision_id", "status", "meaning", "claim_status", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "no_pole_rows", "vertical_certificate_rows", "sourcefree_rows", "branch_rows", "effect_rows", "evaluator_rows", "hard_blockers", "validation_failures", "next_target"])}

## Validation

{validation_table}

## Interpretation

This is a good narrowing, not a defeat. The quotient route now has an actual mathematical hinge: make `v_X` a parent-owned null representative, own the symplectic/momentum-map generator, and kill the boundary charge. If those close, `K_X=0` becomes a serious theorem target rather than an axiom.

The positive source-free route remains the backup theorem. It is cleaner analytically, but more coefficient-heavy: it needs `Z_X>0`, `M_X^2>0`, `J_X=0`, and boundary no-hair all at once.

## Next Target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    no_pole_rows = no_pole_quotient_proof_chain_rows()
    vertical_rows = vertical_generator_certificate_rows()
    sourcefree_rows = positive_sourcefree_proof_chain_rows()
    branch_rows = branch_comparison_rows()
    effect_rows = r10_r11_zero_or_residual_effect_rows()
    evaluator_data = evaluator_rows(no_pole_rows, vertical_rows, sourcefree_rows, effect_rows)
    decision = decision_rows()

    write_csv(RESIDUALS / "P8_Y5_R10_670_SOURCE_REGISTER.csv", source_rows, ["source_id", "source_path", "exists", "role", "generated_utc"])
    write_csv(
        RESIDUALS / "P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv",
        no_pole_rows,
        ["step_id", "claim", "mathematical_form", "current_result", "what_is_proved_now", "missing_for_claim", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_670_VERTICAL_GENERATOR_CERTIFICATE.csv",
        vertical_rows,
        ["certificate_id", "required_object", "mathematical_need", "current_status", "if_filled", "if_missing", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_670_POSITIVE_SOURCEFREE_PROOF_CHAIN.csv",
        sourcefree_rows,
        ["step_id", "claim", "mathematical_form", "current_result", "needed_to_close", "if_fails", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_670_BRANCH_COMPARISON.csv",
        branch_rows,
        ["branch_id", "route", "best_use", "current_strength", "hardest_blocker", "fallback", "rank", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_670_R10_R11_ZERO_OR_RESIDUAL_EFFECT.csv",
        effect_rows,
        ["effect_id", "target", "zero_route", "current_status", "why_not_zero_now", "residual_if_fail", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_670_EVALUATOR.csv",
        evaluator_data,
        ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_670_DECISION.csv",
        decision,
        ["decision_id", "status", "meaning", "claim_status", "next_action", "valid_for_claim", "generated_utc"],
    )

    write_document(source_rows, no_pole_rows, vertical_rows, sourcefree_rows, branch_rows, effect_rows, evaluator_data, decision, [], [])

    validation = validation_rows(source_rows, no_pole_rows, vertical_rows, sourcefree_rows, branch_rows, effect_rows, evaluator_data, decision)
    summary_rows = nonclaim_summary_rows(no_pole_rows, vertical_rows, sourcefree_rows, branch_rows, effect_rows, evaluator_data, validation)
    write_csv(
        RESIDUALS / "P8_Y5_R10_670_NONCLAIM_SUMMARY.csv",
        summary_rows,
        [
            "status",
            "claim_ceiling",
            "no_pole_rows",
            "vertical_certificate_rows",
            "sourcefree_rows",
            "branch_rows",
            "effect_rows",
            "evaluator_rows",
            "hard_blockers",
            "validation_failures",
            "next_target",
            "generated_utc",
        ],
    )
    write_csv(RESIDUALS / "P8_Y5_BRR545_670_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_document(source_rows, no_pole_rows, vertical_rows, sourcefree_rows, branch_rows, effect_rows, evaluator_data, decision, summary_rows, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"no_pole_rows={len(no_pole_rows)}")
    print(f"vertical_certificate_rows={len(vertical_rows)}")
    print(f"sourcefree_rows={len(sourcefree_rows)}")
    print(f"branch_rows={len(branch_rows)}")
    print(f"effect_rows={len(effect_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
