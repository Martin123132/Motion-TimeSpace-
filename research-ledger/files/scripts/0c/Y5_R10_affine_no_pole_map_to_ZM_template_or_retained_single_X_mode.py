from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = POST_CHECKPOINT.parent / "formalization-workbench"
OUTPUT_DOC = POST_CHECKPOINT / "722-Y5-R10-affine-no-pole-map-to-ZM-template-or-retained-single-X-mode.md"
NEXT_TARGET = "723-Y5-R10-affine-X-momentum-map-owner-or-edge-residual-coefficient-pack.md"
GENERATED_UTC = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)


SOURCES = {
    "721_doc": {
        "path": POST_CHECKPOINT / "721-Y5-R10-parent-ZM-source-hunt-or-canonical-mode-template-fill.md",
        "note": "immediate handoff selecting affine/no-pole map first",
        "needles": ["no claim-grade full", "722-Y5-R10-affine-no-pole-map-to-ZM-template-or-retained-single-X-mode.md"],
    },
    "721_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_721_VALIDATION.csv",
        "note": "prior validation",
        "needles": ["V721_6_no_claim_grade_ZM_promoted", "pass", "V721_13_formalization_workbench_untouched"],
    },
    "721_template": {
        "path": RESIDUALS / "P8_Y5_R10_721_PARENT_ZM_TEMPLATE.csv",
        "note": "canonical Z/M template and single-X embedding row",
        "needles": ["PZT721_8_single_X_embedding", "Z_XX,M2_XX", "FORMULA_SOURCE_EXISTS_VALUES_MISSING"],
    },
    "586_doc": {
        "path": POST_CHECKPOINT / "586-Y5-R10-Vdef-owner-action-sketch-or-edge-runner-numeric-priors.md",
        "note": "affine Vdef zero-Hessian/no-pole contract",
        "needles": ["affine", "partial^2 V_def", "conditional_mechanism_found"],
    },
    "586_vdef_csv": {
        "path": RESIDUALS / "P8_Y5_R10_586_VDEF_ACTION_SKETCH.csv",
        "note": "machine-readable affine Vdef action sketch",
        "needles": ["VAS586_1_affine_Vdef_zero_Hessian", "partial^2 V_def/partial Z partial Z=0"],
    },
    "586_theorem_csv": {
        "path": RESIDUALS / "P8_Y5_R10_586_CONDITIONAL_NO_POLE_THEOREM.csv",
        "note": "conditional no-pole theorem clauses",
        "needles": ["CNT586_0_affine_defect_block", "K_X=0", "not_derived"],
    },
    "581_doc": {
        "path": POST_CHECKPOINT / "581-Y5-R10-quotient-vertical-no-pole-parent-theorem-attempt.md",
        "note": "quotient-vertical no-pole theorem shape",
        "needles": ["K_X=0", "not yet theorem ownership", "boundary/constraint"],
    },
    "581_certificate": {
        "path": RESIDUALS / "P8_Y5_R10_581_NO_POLE_CERTIFICATE_TEMPLATE.csv",
        "note": "no-pole certificate obligations",
        "needles": ["NPC581_2_matter_blindness", "NPC581_4_boundary_silence", "unfilled_certificate"],
    },
    "582_doc": {
        "path": POST_CHECKPOINT / "582-Y5-R10-boundary-charge-and-constraint-algebra-no-pole-audit.md",
        "note": "momentum-map and boundary-cocycle no-pole gate",
        "needles": ["momentum map", "K_boundary = 0", "Rank-zero `X` is not enough"],
    },
    "582_gate_csv": {
        "path": RESIDUALS / "P8_Y5_R10_582_NOPOLE_GATE_STATUS.csv",
        "note": "machine-readable no-pole gate status",
        "needles": ["NPG582_5_no_pole_claim", "not_passed", "no_claim"],
    },
    "626_doc": {
        "path": POST_CHECKPOINT / "626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md",
        "note": "matter descent/coupling blocker",
        "needles": ["S_matter[Phi,Psi] = Sbar_matter", "not_signed", "c_g"],
    },
    "579_doc": {
        "path": POST_CHECKPOINT / "579-Y5-R10-parent-Hessian-source-charge-fill-or-theorem-zero-return.md",
        "note": "finite single-X Hessian fallback contract",
        "needles": ["S_X^(2)", "lambda_X", "formula_only"],
    },
    "564_hessian_csv": {
        "path": RESIDUALS / "P8_Y5_R10_564_HESSIAN_EXTRACTION_FORMULA.csv",
        "note": "single-X Hessian extraction formulas",
        "needles": ["H564_1_ZX_extraction", "H564_2_MX_extraction", "conditional_extraction_formula_derived"],
    },
    "607_doc": {
        "path": POST_CHECKPOINT / "607-Y5-R10-compact-shell-parent-coefficient-factorization-or-theorem-zero.md",
        "note": "finite alpha(lambda) factorization fallback",
        "needles": ["alpha_X(lambda_X)", "C_X", "blocked"],
    },
}


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
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


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    source_register = [
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

    affine_to_zm_map = [
        {
            "map_id": "AZM722_0_defect_coordinate",
            "affine_object": "Z_def_munu = nabla_mu X_nu - A_munu[Y]",
            "ZM_destination": "not a physical Z_XX kinetic block if V_def is affine and X is quotient/constraint",
            "mathematical_result": "partial^2 V_def/partial Z_def partial Z_def = 0",
            "current_status": "contract_written_not_parent_sourced",
            "if_passes": "X is excluded from P_phys; no canonical X mode E_X exists",
            "if_fails": "a nonlinear Hessian/pole or edge variable must be retained",
            "valid_for_claim": "false",
            "source_paths": source_path_string("586_doc", "586_vdef_csv"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "map_id": "AZM722_1_affine_action",
            "affine_object": "S_X=int sqrt(-g)[P_munu[Y](nabla_mu X_nu-A_munu[Y])+X_nu J_eff^nu[Y]]+S_boundary",
            "ZM_destination": "constraint row replacing Z_XX/M2_XX as a physical second-order mode",
            "mathematical_result": "delta_X S gives C_X^nu=-nabla_mu P_munu+J_eff^nu plus boundary term",
            "current_status": "conditional_mechanism_not_parent_owned",
            "if_passes": "X is multiplier/gauge, not Yukawa field",
            "if_fails": "retain C_X source and boundary charge rows",
            "valid_for_claim": "false",
            "source_paths": source_path_string("586_doc", "582_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "map_id": "AZM722_2_momentum_map",
            "affine_object": "G[epsilon]=int_Sigma epsilon_nu C_X^nu + Q_boundary[epsilon]",
            "ZM_destination": "first-class constraint degree-count gate",
            "mathematical_result": "{G[epsilon],G[eta]}=G[[epsilon,eta]]+K_boundary[epsilon,eta]",
            "current_status": "parent_symplectic_owner_and_boundary_cocycle_missing",
            "if_passes": "rank-zero X is genuine gauge/no-pole",
            "if_fails": "second-class remnant or edge mode must be scored",
            "valid_for_claim": "false",
            "source_paths": source_path_string("582_doc", "582_gate_csv"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "map_id": "AZM722_3_matter_descent",
            "affine_object": "S_matter descends to quotient data",
            "ZM_destination": "qbar_XT=0 and no matter source projection along X",
            "mathematical_result": "Lie_v S_matter=0 for every vertical v in ker(Dq), up to owned gauge/boundary terms",
            "current_status": "not_signed",
            "if_passes": "ordinary matter does not source/test X",
            "if_fails": "c_g, qbar_XT, and source-charge rows remain active",
            "valid_for_claim": "false",
            "source_paths": source_path_string("626_doc", "581_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "map_id": "AZM722_4_boundary_silence",
            "affine_object": "Q_edge[epsilon] and K_boundary[epsilon,eta]",
            "ZM_destination": "edge contribution to Qbar_XH(lambda) or K_X=0 theorem",
            "mathematical_result": "Q_boundary=0 and K_boundary=0 are required for no active edge alpha row",
            "current_status": "not_zeroed",
            "if_passes": "no boundary/source leakage into local mass channel",
            "if_fails": "edge residual coefficient pack required",
            "valid_for_claim": "false",
            "source_paths": source_path_string("581_doc", "582_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "map_id": "AZM722_5_ZM_verdict",
            "affine_object": "affine/topological no-pole branch",
            "ZM_destination": "P_phys excludes X or retained X block is scored",
            "mathematical_result": "no-pole iff affine Hessian zero + parent momentum map + matter descent + zero boundary charge all hold",
            "current_status": "fail_current_corpus_for_claim",
            "if_passes": "K_X=0 and no active X alpha(lambda) row",
            "if_fails": "retain single-X finite/edge branch",
            "valid_for_claim": "false",
            "source_paths": source_path_string("721_doc", "586_doc", "581_doc", "582_doc", "626_doc"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    no_pole_certificate_audit = [
        {
            "certificate_id": "NPC722_0_affine_hessian_zero",
            "needed_clause": "V_def affine in Z_def",
            "proof_obligation": "show H_ZZ=partial^2 V_def/partial Z_def^2 is exactly zero from the parent block",
            "current_status": "contract_written_not_parent_sourced",
            "claim_effect": "alone insufficient; gives rank-zero candidate only",
            "valid_for_claim": "false",
            "source_paths": source_path_string("586_theorem_csv"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "certificate_id": "NPC722_1_no_hidden_quadratics",
            "needed_clause": "no Pi^2, derivative-Pi, nonlinear V_def, or eliminated auxiliary term regenerates (nabla X)^2",
            "proof_obligation": "parent action forbids hidden quadratic terms after integrating out auxiliaries",
            "current_status": "not_parent_signed",
            "claim_effect": "blocks using H_ZZ=0 as complete no-pole proof",
            "valid_for_claim": "false",
            "source_paths": source_path_string("586_doc", "581_certificate"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "certificate_id": "NPC722_2_momentum_map_owner",
            "needed_clause": "C_X is an equivariant parent momentum map",
            "proof_obligation": "derive parent symplectic form and show C_X generates the vertical symmetry",
            "current_status": "parent_owner_missing",
            "claim_effect": "blocks first-class/no-pole status",
            "valid_for_claim": "false",
            "source_paths": source_path_string("582_doc", "582_gate_csv"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "certificate_id": "NPC722_3_bracket_and_degree_count",
            "needed_clause": "primary/secondary constraints remove the local X pair",
            "proof_obligation": "compute bracket closure and degree count with K_boundary=0",
            "current_status": "not_computed",
            "claim_effect": "rank-zero X could still be second-class or leave an edge/remnant",
            "valid_for_claim": "false",
            "source_paths": source_path_string("581_doc", "582_gate_csv"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "certificate_id": "NPC722_4_matter_blindness",
            "needed_clause": "ordinary matter descends to quotient data",
            "proof_obligation": "prove delta_X S_matter=0 universally, not just for one source",
            "current_status": "not_signed",
            "claim_effect": "blocks qbar_XT=0, WEP, clocks, PPN, and local-GR claims",
            "valid_for_claim": "false",
            "source_paths": source_path_string("626_doc", "581_certificate"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "certificate_id": "NPC722_5_boundary_silence",
            "needed_clause": "Q_boundary=0 and K_boundary=0",
            "proof_obligation": "derive exact/proper-gauge boundary primitive or zero boundary charge/cocycle",
            "current_status": "not_zeroed",
            "claim_effect": "blocks Qbar_XH=0 and K_X=0 as local bound theorem",
            "valid_for_claim": "false",
            "source_paths": source_path_string("581_doc", "582_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "certificate_id": "NPC722_6_no_pole_claim_gate",
            "needed_clause": "all no-pole clauses pass together",
            "proof_obligation": "affine block, no hidden quadratic, momentum map, bracket closure, matter descent, and boundary silence all sourced",
            "current_status": "fail_current_corpus",
            "claim_effect": "do not promote K_X=0, R10 pass, PPN pass, or local-GR recovery",
            "valid_for_claim": "false",
            "source_paths": source_path_string("721_doc", "586_doc", "581_doc", "582_doc", "626_doc"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    retained_single_x_mode_template = [
        {
            "input_id": "RX722_0_branch_flag",
            "symbol": "X_branch",
            "definition": "no-pole candidate if all certificates close; otherwise retained finite/edge single-X branch",
            "current_status": "NO_POLE_NOT_CLAIMED_RETAINED_BRANCH_ACTIVE",
            "required_to_promote": "complete no-pole certificate or numeric finite residual source pack",
            "claim_gate": "blocks_local_X_claim",
            "valid_for_claim": "false",
            "source_paths": source_path_string("721_doc", "581_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "input_id": "RX722_1_ZXX",
            "symbol": "Z_XX=Z_X",
            "definition": "single-X kinetic/Hessian residue if X is a physical positive mode",
            "current_status": "FORMULA_ONLY_VALUE_AND_SIGN_MISSING",
            "required_to_promote": "explicit parent second variation and field normalization",
            "claim_gate": "blocks_ghost_stability_and_K_X",
            "valid_for_claim": "false",
            "source_paths": source_path_string("564_hessian_csv", "579_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "input_id": "RX722_2_M2XX",
            "symbol": "M2_XX=M_X^2",
            "definition": "single-X mass/Hessian curvature if X is a physical positive mode",
            "current_status": "FORMULA_ONLY_VALUE_AND_SIGN_MISSING",
            "required_to_promote": "explicit parent potential/operator Hessian",
            "claim_gate": "blocks_lambda_X",
            "valid_for_claim": "false",
            "source_paths": source_path_string("579_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "input_id": "RX722_3_lambda",
            "symbol": "lambda_X",
            "definition": "sqrt(Z_X/M_X^2) for a positive physical single-X branch",
            "current_status": "CONDITIONAL_LAW_ONLY",
            "required_to_promote": "positive sourced Z_X and M_X^2 with units",
            "claim_gate": "blocks_R10_x_axis_and_orbital_range",
            "valid_for_claim": "false",
            "source_paths": source_path_string("579_doc", "607_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "input_id": "RX722_4_KX",
            "symbol": "K_X",
            "definition": "exchange normalization or zero if no physical Green function exists",
            "current_status": "MISSING_NO_POLE_CERTIFICATE_OR_FINITE_NORMALIZATION",
            "required_to_promote": "K_X=0 theorem or finite K_X from Z_X/sign/G_obs convention",
            "claim_gate": "blocks_alpha_normalization",
            "valid_for_claim": "false",
            "source_paths": source_path_string("581_doc", "607_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "input_id": "RX722_5_qbar_XT",
            "symbol": "qbar_XT",
            "definition": "ordinary test-body charge per mass along X",
            "current_status": "MISSING_MATTER_DESCENT_OR_FINITE_CHARGE",
            "required_to_promote": "quotient matter descent or sourced finite charge",
            "claim_gate": "blocks_WEP_R10_PPN_clock",
            "valid_for_claim": "false",
            "source_paths": source_path_string("626_doc", "579_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "input_id": "RX722_6_Qbar_XH",
            "symbol": "Qbar_XH(lambda_X)",
            "definition": "source body X charge per mass including bulk/projector/boundary channels",
            "current_status": "MISSING_SOURCE_CHARGE_OR_BOUNDARY_ZERO",
            "required_to_promote": "zero source theorem or finite source profile",
            "claim_gate": "blocks_R10_source_amplitude",
            "valid_for_claim": "false",
            "source_paths": source_path_string("581_doc", "582_doc", "607_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "input_id": "RX722_7_edge",
            "symbol": "Q_edge,K_boundary,epsilon_PiM_X",
            "definition": "boundary/edge charge, boundary cocycle, and mass-channel projection leakage",
            "current_status": "MISSING_EDGE_ZERO_OR_FINITE_EDGE_COEFFICIENT",
            "required_to_promote": "zero boundary cocycle/projection or explicit edge residual coefficient",
            "claim_gate": "blocks_no_pole_and_mass_readout",
            "valid_for_claim": "false",
            "source_paths": source_path_string("582_doc"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    mode_decision_branch = [
        {
            "decision_id": "D722_0_affine_map",
            "question": "Does affine Vdef map cleanly to a no-pole ZM branch?",
            "answer": "conditional_only",
            "reason": "H_ZZ=0 is useful, but P/J/A parent ownership, matter descent, and boundary silence are unfilled",
            "decision": "no_pole_not_promoted",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("586_doc", "581_doc", "582_doc", "626_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D722_1_ZM_template",
            "question": "How does this enter the ZM template?",
            "answer": "X is excluded from P_phys only if certificate closes; otherwise Z_XX/M2_XX retained symbolically",
            "reason": "zero Hessian is not automatically first-class gauge and not automatically matter-blind",
            "decision": "retain_single_X_template_until_certificate_closes",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("721_template", "579_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D722_2_next_best",
            "question": "What is the next derivation target?",
            "answer": "own the affine momentum map or demote edge/finite X residual coefficients",
            "reason": "boundary and momentum-map ownership are the live blockers after mapping",
            "decision": "attack_momentum_map_or_edge_residual_pack",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("582_doc", "586_doc"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    local_observable_implications = [
        {
            "arena_id": "LOI722_0_R10_no_pole",
            "arena": "R10 fifth force if no-pole certificate passes",
            "equation_or_rule": "K_X=0, qbar_XT=0, Qbar_XH=0; no active alpha_X(lambda) row",
            "current_status": "blocked_certificate_unfilled",
            "claim_effect": "no R10 pass",
            "valid_for_claim": "false",
            "source_paths": source_path_string("581_doc", "582_gate_csv"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "LOI722_1_R10_finite",
            "arena": "R10 fifth force if retained X/edge branch survives",
            "equation_or_rule": "alpha_X(lambda_X)=epsilon_shell^p C_X(lambda_X), with C_X containing K_X, Qbar_XH, qbar_XT, Z_X normalization",
            "current_status": "blocked_symbolic_coefficients",
            "claim_effect": "no R10 score yet",
            "valid_for_claim": "false",
            "source_paths": source_path_string("607_doc", "579_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "LOI722_2_PPN_WEP_clocks",
            "arena": "PPN/WEP/clocks",
            "equation_or_rule": "ordinary matter charge is zero only if matter descent is parent-signed; otherwise c_g/qbar channels remain",
            "current_status": "blocked_matter_descent_unsigned",
            "claim_effect": "no PPN/WEP/clock pass",
            "valid_for_claim": "false",
            "source_paths": source_path_string("626_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "LOI722_3_Newton_local_GR",
            "arena": "Newton/local-GR limit",
            "equation_or_rule": "local-GR requires no physical X pole plus no edge/source/matter leakage, or a finite branch below all local bounds",
            "current_status": "blocked_no_pole_and_finite_score_unfinished",
            "claim_effect": "no local-GR/Newton recovery claim",
            "valid_for_claim": "false",
            "source_paths": source_path_string("721_doc"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    bound_or_derive_queue = [
        {
            "queue_id": "BDQ722_0_momentum_map_owner",
            "target": "derive C_X as an equivariant parent momentum map",
            "preferred_route": "construct parent symplectic form and show G[epsilon] generates the vertical symmetry with K_boundary=0",
            "fallback_route": "route nonzero K_boundary or nonclosing bracket to edge residual coefficients",
            "priority": "P0",
            "next_artifact": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("582_doc", "586_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "queue_id": "BDQ722_1_boundary_edge",
            "target": "zero or parameterize Q_edge and epsilon_PiM_X",
            "preferred_route": "derive exact/proper-gauge boundary primitive and zero mass-channel projection",
            "fallback_route": "write finite edge coefficient pack for later R10/PPN/orbital scoring",
            "priority": "P0",
            "next_artifact": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("581_doc", "582_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "queue_id": "BDQ722_2_matter_descent",
            "target": "prove quotient-invariant ordinary matter action for X",
            "preferred_route": "show S_matter descends and all representative frame coefficients are absent/gauge",
            "fallback_route": "retain c_g/qbar_XT rows and source bounds",
            "priority": "P1",
            "next_artifact": "after_723_matter_descent_or_cg_qbar_score_pack",
            "valid_for_claim": "false",
            "source_paths": source_path_string("626_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "queue_id": "BDQ722_3_finite_X",
            "target": "finite retained X mode coefficient pack",
            "preferred_route": "avoid if no-pole certificate closes",
            "fallback_route": "fill Z_X, M_X^2, lambda_X, K_X, Qbar_XH, qbar_XT, Q_edge as nonclaim first",
            "priority": "P1",
            "next_artifact": "after_723_retained_X_local_bound_score_pack",
            "valid_for_claim": "false",
            "source_paths": source_path_string("579_doc", "607_doc"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    nonclaim_summary = [
        {
            "status": "Y5_R10_affine_no_pole_maps_to_ZM_as_conditional_rank_zero_skeleton_retained_single_X_template_active_nonclaim",
            "claim_ceiling": "conditional_no_pole_map_and_retained_X_template_only_no_R10_WEP_PPN_Newton_or_local_GR_claim",
            "main_result": "affine Vdef gives an exact zero-Hessian skeleton, but no-pole is not claimable without parent momentum-map ownership, matter descent, and boundary silence",
            "retained_branch": "single-X finite/edge template remains active with Z_X, M_X^2, lambda_X, K_X, qbar_XT, Qbar_XH, Q_edge missing or formula-only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("721_doc", "586_doc", "581_doc", "582_doc", "626_doc"),
            "generated_utc": GENERATED_UTC,
        }
    ]

    outputs = {
        "source_register": (
            RESIDUALS / "P8_Y5_R10_722_SOURCE_REGISTER.csv",
            source_register,
            ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"],
        ),
        "affine_to_zm_map": (
            RESIDUALS / "P8_Y5_R10_722_AFFINE_TO_ZM_MAP.csv",
            affine_to_zm_map,
            [
                "map_id",
                "affine_object",
                "ZM_destination",
                "mathematical_result",
                "current_status",
                "if_passes",
                "if_fails",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "no_pole_certificate_audit": (
            RESIDUALS / "P8_Y5_R10_722_NO_POLE_CERTIFICATE_AUDIT.csv",
            no_pole_certificate_audit,
            [
                "certificate_id",
                "needed_clause",
                "proof_obligation",
                "current_status",
                "claim_effect",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "retained_single_x_mode_template": (
            RESIDUALS / "P8_Y5_R10_722_RETAINED_SINGLE_X_MODE_TEMPLATE.csv",
            retained_single_x_mode_template,
            [
                "input_id",
                "symbol",
                "definition",
                "current_status",
                "required_to_promote",
                "claim_gate",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "mode_decision_branch": (
            RESIDUALS / "P8_Y5_R10_722_MODE_DECISION_BRANCH.csv",
            mode_decision_branch,
            ["decision_id", "question", "answer", "reason", "decision", "next_target", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "local_observable_implications": (
            RESIDUALS / "P8_Y5_R10_722_LOCAL_OBSERVABLE_IMPLICATIONS.csv",
            local_observable_implications,
            ["arena_id", "arena", "equation_or_rule", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "bound_or_derive_queue": (
            RESIDUALS / "P8_Y5_R10_722_BOUND_OR_DERIVE_QUEUE.csv",
            bound_or_derive_queue,
            [
                "queue_id",
                "target",
                "preferred_route",
                "fallback_route",
                "priority",
                "next_artifact",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "nonclaim_summary": (
            RESIDUALS / "P8_Y5_R10_722_NONCLAIM_SUMMARY.csv",
            nonclaim_summary,
            [
                "status",
                "claim_ceiling",
                "main_result",
                "retained_branch",
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
    validations = [
        {
            "check_id": "V722_0_source_paths_exist",
            "result": "pass" if all(info["path"].exists() for info in SOURCES.values()) else "fail",
            "detail": "all cited source paths exist",
        },
        {
            "check_id": "V722_1_source_needles_present",
            "result": "pass" if all(text_contains(info["path"], info["needles"]) for info in SOURCES.values()) else "fail",
            "detail": "all source files contain expected evidence needles",
        },
        {
            "check_id": "V722_2_prior_721_clean",
            "result": "pass" if prior_validation_clean(SOURCES["721_validation"]["path"]) else "fail",
            "detail": "721 validation has no failures",
        },
        {
            "check_id": "V722_3_721_selected_722",
            "result": "pass" if csv_contains(SOURCES["721_doc"]["path"], "722-Y5-R10-affine-no-pole-map-to-ZM-template-or-retained-single-X-mode.md") else "fail",
            "detail": "721 next target matches this checkpoint",
        },
        {
            "check_id": "V722_4_affine_zero_hessian_present",
            "result": "pass" if any(row["mathematical_result"] == "partial^2 V_def/partial Z_def partial Z_def = 0" for row in affine_to_zm_map) else "fail",
            "detail": "affine zero-Hessian map written",
        },
        {
            "check_id": "V722_5_no_pole_not_promoted",
            "result": "pass" if any(row["current_status"] == "fail_current_corpus" for row in no_pole_certificate_audit) else "fail",
            "detail": "no-pole certificate remains blocked",
        },
        {
            "check_id": "V722_6_momentum_boundary_blockers_visible",
            "result": "pass"
            if {"parent_owner_missing", "not_zeroed", "not_computed"}.issubset({row["current_status"] for row in no_pole_certificate_audit})
            else "fail",
            "detail": "momentum-map, boundary, and degree-count blockers preserved",
        },
        {
            "check_id": "V722_7_matter_descent_unsigned",
            "result": "pass" if any(row["current_status"] == "not_signed" for row in no_pole_certificate_audit) else "fail",
            "detail": "matter descent remains unsigned",
        },
        {
            "check_id": "V722_8_retained_X_core_inputs_present",
            "result": "pass"
            if {"Z_XX=Z_X", "M2_XX=M_X^2", "lambda_X", "K_X", "qbar_XT", "Qbar_XH(lambda_X)"}.issubset(
                {row["symbol"] for row in retained_single_x_mode_template}
            )
            else "fail",
            "detail": f"retained_rows={len(retained_single_x_mode_template)}",
        },
        {
            "check_id": "V722_9_local_arenas_blocked",
            "result": "pass" if all(row["current_status"].startswith("blocked_") for row in local_observable_implications) else "fail",
            "detail": "all local observable rows remain blocked",
        },
        {
            "check_id": "V722_10_next_target_selected",
            "result": "pass" if all(row["next_target"] == NEXT_TARGET for row in mode_decision_branch) else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V722_11_no_claim_rows_promoted",
            "result": "pass" if all_valid_false(generated_paths) else "fail",
            "detail": "all generated rows with valid_for_claim remain false",
        },
        {
            "check_id": "V722_12_outputs_scoped",
            "result": "pass" if under_post_checkpoint([OUTPUT_DOC, *generated_paths]) else "fail",
            "detail": "all outputs under post-checkpoint-work",
        },
        {
            "check_id": "V722_13_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V722_14_nonclaim_status",
            "result": "pass" if "nonclaim" in nonclaim_summary[0]["status"] else "fail",
            "detail": "claim ceiling blocks R10/WEP/PPN/Newton/local-GR claims",
        },
        {
            "check_id": "V722_15_source_register_written",
            "result": "pass" if len(source_register) >= 12 else "fail",
            "detail": f"source_rows={len(source_register)}",
        },
        {
            "check_id": "V722_16_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]

    validation_path = RESIDUALS / "P8_Y5_BRR545_722_VALIDATION.csv"
    write_csv(validation_path, validations, ["check_id", "result", "detail"])

    doc = f"""# 722 - Y5 R10 Affine No-Pole Map To ZM Template Or Retained Single-X Mode

## Summary

This checkpoint tries the least-exposed route selected by 721: map the affine/topological no-pole mechanism into the canonical `Z/M` template.

The good result:

`V_def` affine in `Z_def=nabla X-A[Y]` gives `partial^2 V_def/partial Z_def partial Z_def=0`.

That is a real zero-Hessian skeleton. It means a physical `Z_XX/M2_XX` Yukawa block is not forced.

The hard result:

This still does **not** prove no-pole/local-GR. Zero Hessian is only safe if the parent action also proves momentum-map ownership, first-class bracket closure, matter descent, no hidden quadratic regeneration, and zero boundary/edge charge.

Current verdict: no-pole is conditional only; the retained single-`X` finite/edge template remains active.

| Field | Value |
| --- | --- |
| Generated UTC | `{GENERATED_UTC}` |
| Claim status | nonclaim/private checkpoint |
| Next target | `{NEXT_TARGET}` |

## Affine To ZM Map

{markdown_table(affine_to_zm_map, ["map_id", "affine_object", "ZM_destination", "mathematical_result", "current_status", "if_passes", "if_fails", "valid_for_claim"])}

## No-Pole Certificate Audit

{markdown_table(no_pole_certificate_audit, ["certificate_id", "needed_clause", "current_status", "claim_effect", "valid_for_claim"])}

## Retained Single-X Mode Template

{markdown_table(retained_single_x_mode_template, ["input_id", "symbol", "current_status", "required_to_promote", "claim_gate", "valid_for_claim"])}

## Mode Decision Branch

{markdown_table(mode_decision_branch, ["decision_id", "question", "answer", "decision", "next_target", "valid_for_claim"])}

## Local Observable Implications

{markdown_table(local_observable_implications, ["arena_id", "arena", "equation_or_rule", "current_status", "claim_effect", "valid_for_claim"])}

## Bound Or Derive Queue

{markdown_table(bound_or_derive_queue, ["queue_id", "target", "preferred_route", "fallback_route", "priority", "next_artifact", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(nonclaim_summary, ["status", "claim_ceiling", "main_result", "retained_branch", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_register, ["source_id", "path", "exists", "needle_check", "role"])}

## Validation

{markdown_table(validations, ["check_id", "result", "detail"])}

## Verdict

The affine route is the right route to try first: it is cleaner than hoping a finite scalar squeaks past local bounds. But it is not closed. The theorem would be strong if `C_X` is a real parent momentum map, `K_boundary=0`, ordinary matter descends, and the boundary/mass projection is silent. Until then, the correct state is conditional no-pole plus retained single-`X` finite/edge residual template. Next target: own the momentum map or write the edge coefficient pack.
"""

    OUTPUT_DOC.write_text(doc, encoding="utf-8")
    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {validation_path}")
    print(f"validation_passes={sum(row['result'] == 'pass' for row in validations)}/{len(validations)}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
