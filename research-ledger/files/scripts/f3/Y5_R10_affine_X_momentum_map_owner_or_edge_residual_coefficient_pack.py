from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = POST_CHECKPOINT.parent / "formalization-workbench"
OUTPUT_DOC = POST_CHECKPOINT / "723-Y5-R10-affine-X-momentum-map-owner-or-edge-residual-coefficient-pack.md"
NEXT_TARGET = "724-Y5-R10-edge-residual-alpha-envelope-or-owner-repair.md"
GENERATED_UTC = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)


SOURCES = {
    "722_doc": {
        "path": POST_CHECKPOINT / "722-Y5-R10-affine-no-pole-map-to-ZM-template-or-retained-single-X-mode.md",
        "note": "immediate handoff: own momentum map or write edge pack",
        "needles": ["723-Y5-R10-affine-X-momentum-map-owner-or-edge-residual-coefficient-pack.md", "conditional no-pole", "retained single-`X`"],
    },
    "722_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_722_VALIDATION.csv",
        "note": "prior validation",
        "needles": ["V722_5_no_pole_not_promoted", "pass", "V722_13_formalization_workbench_untouched"],
    },
    "722_retained_x": {
        "path": RESIDUALS / "P8_Y5_R10_722_RETAINED_SINGLE_X_MODE_TEMPLATE.csv",
        "note": "current retained single-X template",
        "needles": ["RX722_7_edge", "Q_edge,K_boundary,epsilon_PiM_X", "MISSING_EDGE_ZERO_OR_FINITE_EDGE_COEFFICIENT"],
    },
    "583_doc": {
        "path": POST_CHECKPOINT / "583-Y5-R10-parent-momentum-map-owner-or-edge-residual-demotion.md",
        "note": "older direct owner-or-edge fork to integrate into current chain",
        "needles": ["parent momentum-map owner not derived", "Qbar_edge_XH", "alpha_edge(lambda)"],
    },
    "583_owner_attempt": {
        "path": RESIDUALS / "P8_Y5_R10_583_PARENT_MOMENTUM_MAP_OWNER_ATTEMPT.csv",
        "note": "machine-readable owner attempt",
        "needles": ["OMA583_5_verdict", "owner_not_derived_edge_template_required", "false"],
    },
    "583_contract": {
        "path": RESIDUALS / "P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv",
        "note": "Noether/momentum-map contract",
        "needles": ["NMC583_0_symplectic_potential", "NMC583_3_momentum_map", "missing"],
    },
    "583_edge": {
        "path": RESIDUALS / "P8_Y5_R10_583_EDGE_RESIDUAL_DEMOTION.csv",
        "note": "edge residual demotion rows",
        "needles": ["ED583_0_edge_charge_definition", "Qbar_edge_XH", "symbolic_residual"],
    },
    "583_alpha": {
        "path": RESIDUALS / "P8_Y5_R10_583_EDGE_ALPHA_TEMPLATE.csv",
        "note": "edge alpha template",
        "needles": ["EAT583_0_edge_alpha", "K_edge(lambda)*Qbar_edge_XH(lambda)*qbar_XT", "false"],
    },
    "582_doc": {
        "path": POST_CHECKPOINT / "582-Y5-R10-boundary-charge-and-constraint-algebra-no-pole-audit.md",
        "note": "momentum-map and boundary-cocycle gate",
        "needles": ["C_X", "K_boundary = 0", "Rank-zero `X` is not enough"],
    },
    "582_momentum_csv": {
        "path": RESIDUALS / "P8_Y5_R10_582_MOMENTUM_MAP_CLOSURE_THEOREM.csv",
        "note": "momentum-map closure theorem rows",
        "needles": ["MMT582_2_equivariance", "parent_owner_missing", "false"],
    },
    "582_boundary_csv": {
        "path": RESIDUALS / "P8_Y5_R10_582_BOUNDARY_DIFFERENTIABILITY_AUDIT.csv",
        "note": "boundary differentiability blockers",
        "needles": ["BD582_1_charge_value", "Q_X[epsilon]", "not_zeroed"],
    },
    "222_doc": {
        "path": POST_CHECKPOINT / "222-parent-X-sector-degree-count-and-boundary-action.md",
        "note": "first-order X and boundary momentum contract",
        "needles": ["J_eff^nu", "boundary", "zero propagating `X` degree count derived"],
    },
    "223_doc": {
        "path": POST_CHECKPOINT / "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md",
        "note": "constraint algebra and P[Y] owner blocker",
        "needles": ["C_X^nu", "constraint closure: not derived", "P[Y]"],
    },
    "235_doc": {
        "path": POST_CHECKPOINT / "235-projector-stress-variation-or-nohair-constraint-algebra.md",
        "note": "projector/no-hair bracket blocker",
        "needles": ["P[Y] and P_mem", "bracket closure is not computed", "local GR or PPN promoted"],
    },
    "626_doc": {
        "path": POST_CHECKPOINT / "626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md",
        "note": "matter descent/coupling blocker",
        "needles": ["S_matter[Phi,Psi] = Sbar_matter", "not_signed", "c_g"],
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

    momentum_map_owner_audit = [
        {
            "audit_id": "MMO723_0_parent_lagrangian",
            "needed_object": "explicit parent Lagrangian L_parent[Y]",
            "mathematical_role": "defines the variational identity delta L=E_i delta Y^i+d theta_Y",
            "current_status": "missing_explicit_parent_L",
            "if_missing": "Noether current and momentum map remain template-only",
            "valid_for_claim": "false",
            "source_paths": source_path_string("583_contract", "223_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "MMO723_1_symplectic_potential",
            "needed_object": "theta_Y and Omega_Y=delta theta_Y",
            "mathematical_role": "lets i_v Omega_Y be checked against delta G_X",
            "current_status": "missing",
            "if_missing": "C_X cannot be promoted to Hamiltonian momentum map",
            "valid_for_claim": "false",
            "source_paths": source_path_string("583_contract", "582_momentum_csv"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "MMO723_2_vertical_generator",
            "needed_object": "v_X action on Y, P_mem, boundary fields, and matter/readout fields",
            "mathematical_role": "defines the quotient direction before variation",
            "current_status": "missing",
            "if_missing": "X verticality remains asserted conditionally, not proved",
            "valid_for_claim": "false",
            "source_paths": source_path_string("583_contract", "626_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "MMO723_3_constraint_identity",
            "needed_object": "C_X^nu=-nabla_mu P[Y]^{mu nu}+J_eff[Y]^nu from one parent variation",
            "mathematical_role": "prevents hand-inserting the constraint after the fact",
            "current_status": "template_only",
            "if_missing": "P/J owner remains a formal contract, not a theorem",
            "valid_for_claim": "false",
            "source_paths": source_path_string("223_doc", "583_owner_attempt"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "MMO723_4_equivariance",
            "needed_object": "{G[epsilon],G[eta]}=G[[epsilon,eta]]+K_boundary[epsilon,eta]",
            "mathematical_role": "decides first-class no-pole versus edge/central remnant",
            "current_status": "not_computed",
            "if_missing": "no-pole cannot be claimed from rank-zero X",
            "valid_for_claim": "false",
            "source_paths": source_path_string("582_doc", "235_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "MMO723_5_boundary_zero",
            "needed_object": "Q_boundary=0 and K_boundary=0 or proper-gauge restriction",
            "mathematical_role": "kills edge hair and mass-channel leakage",
            "current_status": "not_derived",
            "if_missing": "edge residual coefficient pack is required",
            "valid_for_claim": "false",
            "source_paths": source_path_string("582_boundary_csv", "222_doc", "583_edge"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "MMO723_6_matter_descent",
            "needed_object": "ordinary matter/readout descends to quotient data",
            "mathematical_role": "sets qbar_XT=0 and removes WEP/clock/PPN charge",
            "current_status": "not_signed",
            "if_missing": "qbar_XT and c_g-style coupling rows remain active",
            "valid_for_claim": "false",
            "source_paths": source_path_string("626_doc", "722_retained_x"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "MMO723_7_verdict",
            "needed_object": "full parent momentum-map owner certificate",
            "mathematical_role": "would allow K_X=0 and no active alpha_X(lambda) row",
            "current_status": "fail_current_corpus",
            "if_missing": "demote to edge/finite residual pack",
            "valid_for_claim": "false",
            "source_paths": source_path_string("722_doc", "583_doc"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    edge_residual_coefficient_pack = [
        {
            "edge_id": "ERP723_0_boundary_momentum",
            "symbol": "B_X^nu",
            "definition": "boundary momentum/current conjugate to vertical X variation",
            "formula": "B_X^nu = n_mu P[Y]^{mu nu} + B_ct^nu when a counterterm exists",
            "current_status": "SYMBOLIC_RESIDUAL",
            "zero_condition": "B_X=0, exact, pure gauge, or proper-gauge killed on compact boundary",
            "if_nonzero": "feeds Q_edge^H(lambda)",
            "valid_for_claim": "false",
            "source_paths": source_path_string("222_doc", "582_boundary_csv", "583_edge"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "edge_id": "ERP723_1_edge_charge",
            "symbol": "Q_edge^H(lambda)",
            "definition": "source-body edge charge/envelope for compact local body H",
            "formula": "Q_edge^H(lambda)=int_{partial H} dS F_lambda(s) epsilon_nu B_X^nu(s)",
            "current_status": "SYMBOLIC_RESIDUAL",
            "zero_condition": "edge charge vanishes by exact/proper-gauge boundary theorem",
            "if_nonzero": "source amplitude enters alpha_edge(lambda)",
            "valid_for_claim": "false",
            "source_paths": source_path_string("583_edge"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "edge_id": "ERP723_2_projected_edge_charge",
            "symbol": "Qbar_edge_XH(lambda)",
            "definition": "mass-normalized edge charge after Hamiltonian/mass-channel projection",
            "formula": "Qbar_edge_XH(lambda)=Pi_M^H[Q_edge^H(lambda)]/M_H",
            "current_status": "SYMBOLIC_RESIDUAL",
            "zero_condition": "Pi_M^H[Q_edge]=0 including reference-boundary terms",
            "if_nonzero": "explicit source coefficient in local bounds",
            "valid_for_claim": "false",
            "source_paths": source_path_string("583_edge", "582_boundary_csv"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "edge_id": "ERP723_3_boundary_cocycle",
            "symbol": "K_boundary[epsilon,eta]",
            "definition": "boundary/central term in the would-be constraint algebra",
            "formula": "{G[epsilon],G[eta]}=G[[epsilon,eta]]+K_boundary[epsilon,eta]",
            "current_status": "UNCOMPUTED_RESIDUAL",
            "zero_condition": "equivariant momentum map with no central extension on compact branch",
            "if_nonzero": "edge mode or central extension blocks first-class no-pole",
            "valid_for_claim": "false",
            "source_paths": source_path_string("582_doc", "583_edge"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "edge_id": "ERP723_4_projector_leak",
            "symbol": "epsilon_PiM_X(lambda)",
            "definition": "mass-channel leakage of edge/projector/source charge into measured mass readout",
            "formula": "epsilon_PiM_X(lambda)=Pi_M^H[Q_edge^H(lambda)]/Q_edge^H(lambda) when denominator is nonzero",
            "current_status": "SYMBOLIC_RESIDUAL",
            "zero_condition": "projector stress owned and mass channel orthogonal to edge charge",
            "if_nonzero": "measured mass normalization carries X edge hair",
            "valid_for_claim": "false",
            "source_paths": source_path_string("583_edge", "235_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "edge_id": "ERP723_5_test_charge",
            "symbol": "qbar_XT",
            "definition": "ordinary test-body X response per mass",
            "formula": "qbar_XT=0 only if matter quotient blindness/no-marker theorem is parent-signed; otherwise retain finite charge row",
            "current_status": "MISSING_MATTER_DESCENT_OR_FINITE_CHARGE",
            "zero_condition": "S_matter descends to quotient data and no representative coefficients survive",
            "if_nonzero": "edge exchange couples to ordinary matter",
            "valid_for_claim": "false",
            "source_paths": source_path_string("626_doc", "722_retained_x"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "edge_id": "ERP723_6_edge_normalization",
            "symbol": "K_edge(lambda)",
            "definition": "edge exchange normalization or envelope kernel",
            "formula": "K_edge(lambda) must be derived from boundary propagator/envelope or bounded as a nonclaim parameter",
            "current_status": "MISSING_EDGE_RANGE_OR_NORMALIZATION",
            "zero_condition": "no edge propagator/charge after owner certificate",
            "if_nonzero": "normalizes alpha_edge(lambda)",
            "valid_for_claim": "false",
            "source_paths": source_path_string("583_alpha", "607_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "edge_id": "ERP723_7_edge_alpha",
            "symbol": "alpha_edge(lambda)",
            "definition": "explicit edge residual fifth-force amplitude",
            "formula": "alpha_edge(lambda)=K_edge(lambda)*Qbar_edge_XH(lambda)*qbar_XT",
            "current_status": "TEMPLATE_NONCLAIM",
            "zero_condition": "K_edge=0 or Qbar_edge_XH=0 or qbar_XT=0 by parent theorem",
            "if_nonzero": "compare only after real lambda/envelope and bound curve are sourced",
            "valid_for_claim": "false",
            "source_paths": source_path_string("583_alpha", "722_retained_x"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    owner_or_edge_decision = [
        {
            "decision_id": "D723_0_owner_attempt",
            "question": "Can current files derive C_X as a parent momentum map?",
            "answer": "no",
            "reason": "Omega/theta, vertical generator, parent Vdef/P/J/Pmem owner, bracket closure, and boundary zero are still missing",
            "decision": "do_not_promote_no_pole",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("583_doc", "582_doc", "223_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D723_1_edge_pack",
            "question": "What happens if boundary or cocycle survives?",
            "answer": "edge residual becomes explicit",
            "reason": "Q_edge, Qbar_edge_XH, K_boundary, epsilon_PiM_X, K_edge, and qbar_XT are named coefficient rows",
            "decision": "edge_residual_coefficient_pack_written",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("583_edge", "583_alpha"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D723_2_current_route",
            "question": "What is next?",
            "answer": "build edge residual alpha envelope or repair owner",
            "reason": "the current chain needs a runnable nonclaim edge envelope before any local data score, unless the owner certificate closes",
            "decision": "go_to_724_edge_envelope_or_owner_repair",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("722_doc", "583_doc"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    local_observable_router = [
        {
            "arena_id": "LOR723_0_R10_no_pole",
            "arena": "R10 if owner certificate closes",
            "route": "K_X=0, Qbar_edge_XH=0, qbar_XT=0; remove active X alpha row",
            "current_status": "blocked_owner_certificate_unfilled",
            "claim_effect": "no R10 pass",
            "valid_for_claim": "false",
            "source_paths": source_path_string("722_doc", "583_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "LOR723_1_R10_edge",
            "arena": "R10 if edge survives",
            "route": "alpha_edge(lambda)=K_edge(lambda)*Qbar_edge_XH(lambda)*qbar_XT",
            "current_status": "blocked_symbolic_edge_coefficients",
            "claim_effect": "no R10 score yet",
            "valid_for_claim": "false",
            "source_paths": source_path_string("583_alpha", "583_edge"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "LOR723_2_R10_bulk_plus_edge",
            "arena": "R10 if both bulk and edge survive",
            "route": "alpha_total(lambda)=K_X(lambda)*(Qbar_bulk_XH(lambda)+Qbar_edge_XH(lambda))*qbar_XT, with separate provenance",
            "current_status": "blocked_bulk_and_edge_coefficients",
            "claim_effect": "no combined score",
            "valid_for_claim": "false",
            "source_paths": source_path_string("607_doc", "583_alpha"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "LOR723_3_PPN_WEP_clocks",
            "arena": "PPN/WEP/clocks",
            "route": "matter descent must kill qbar_XT/c_g; otherwise finite coupling residuals must be scored separately",
            "current_status": "blocked_matter_descent_unsigned",
            "claim_effect": "no PPN/WEP/clock pass",
            "valid_for_claim": "false",
            "source_paths": source_path_string("626_doc", "722_retained_x"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "LOR723_4_Newton_local_GR",
            "arena": "Newton/local-GR",
            "route": "local-GR requires owner certificate or all bulk/edge/matter residuals below bounds",
            "current_status": "blocked_no_pole_and_score_unfinished",
            "claim_effect": "no Newton/local-GR recovery claim",
            "valid_for_claim": "false",
            "source_paths": source_path_string("722_doc", "583_doc"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    bound_or_derive_queue = [
        {
            "queue_id": "BDQ723_0_owner_repair",
            "target": "parent momentum-map repair",
            "preferred_route": "write explicit parent theta_Y/Omega_Y and vertical generator v_X, then compute i_v Omega and K_boundary",
            "fallback_route": "retain edge residual envelope",
            "priority": "P0",
            "next_artifact": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("583_contract", "582_momentum_csv"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "queue_id": "BDQ723_1_edge_envelope",
            "target": "edge residual alpha envelope",
            "preferred_route": "derive/bound K_edge(lambda), Qbar_edge_XH(lambda), and epsilon_PiM_X(lambda)",
            "fallback_route": "write nonclaim prior grid and keep all rows invalid for claim",
            "priority": "P0",
            "next_artifact": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("583_edge", "583_alpha"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "queue_id": "BDQ723_2_matter_charge",
            "target": "matter descent or qbar_XT/c_g pack",
            "preferred_route": "prove quotient-invariant matter action",
            "fallback_route": "retain finite test-body charge rows and source local bounds",
            "priority": "P1",
            "next_artifact": "after_724_matter_descent_or_qbar_cg_bound_pack",
            "valid_for_claim": "false",
            "source_paths": source_path_string("626_doc"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    nonclaim_summary = [
        {
            "status": "Y5_R10_affine_X_momentum_map_owner_not_derived_edge_residual_coefficient_pack_integrated_nonclaim",
            "claim_ceiling": "momentum_map_owner_attempt_and_edge_residual_pack_only_no_R10_WEP_PPN_Newton_or_local_GR_claim",
            "main_result": "the current corpus still lacks the parent momentum-map certificate, so no-pole is not promoted",
            "edge_result": "edge residual coefficients are explicit: Q_edge, Qbar_edge_XH, K_boundary, epsilon_PiM_X, K_edge, qbar_XT, alpha_edge",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("722_doc", "583_doc", "583_edge", "583_alpha"),
            "generated_utc": GENERATED_UTC,
        }
    ]

    outputs = {
        "source_register": (
            RESIDUALS / "P8_Y5_R10_723_SOURCE_REGISTER.csv",
            source_register,
            ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"],
        ),
        "momentum_map_owner_audit": (
            RESIDUALS / "P8_Y5_R10_723_MOMENTUM_MAP_OWNER_AUDIT.csv",
            momentum_map_owner_audit,
            [
                "audit_id",
                "needed_object",
                "mathematical_role",
                "current_status",
                "if_missing",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "edge_residual_coefficient_pack": (
            RESIDUALS / "P8_Y5_R10_723_EDGE_RESIDUAL_COEFFICIENT_PACK.csv",
            edge_residual_coefficient_pack,
            [
                "edge_id",
                "symbol",
                "definition",
                "formula",
                "current_status",
                "zero_condition",
                "if_nonzero",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "owner_or_edge_decision": (
            RESIDUALS / "P8_Y5_R10_723_OWNER_OR_EDGE_DECISION.csv",
            owner_or_edge_decision,
            ["decision_id", "question", "answer", "reason", "decision", "next_target", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "local_observable_router": (
            RESIDUALS / "P8_Y5_R10_723_LOCAL_OBSERVABLE_ROUTER.csv",
            local_observable_router,
            ["arena_id", "arena", "route", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "bound_or_derive_queue": (
            RESIDUALS / "P8_Y5_R10_723_BOUND_OR_DERIVE_QUEUE.csv",
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
            RESIDUALS / "P8_Y5_R10_723_NONCLAIM_SUMMARY.csv",
            nonclaim_summary,
            [
                "status",
                "claim_ceiling",
                "main_result",
                "edge_result",
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
    edge_symbols = {row["symbol"] for row in edge_residual_coefficient_pack}
    validations = [
        {
            "check_id": "V723_0_source_paths_exist",
            "result": "pass" if all(info["path"].exists() for info in SOURCES.values()) else "fail",
            "detail": "all cited source paths exist",
        },
        {
            "check_id": "V723_1_source_needles_present",
            "result": "pass" if all(text_contains(info["path"], info["needles"]) for info in SOURCES.values()) else "fail",
            "detail": "all source files contain expected evidence needles",
        },
        {
            "check_id": "V723_2_prior_722_clean",
            "result": "pass" if prior_validation_clean(SOURCES["722_validation"]["path"]) else "fail",
            "detail": "722 validation has no failures",
        },
        {
            "check_id": "V723_3_722_selected_723",
            "result": "pass" if csv_contains(SOURCES["722_doc"]["path"], "723-Y5-R10-affine-X-momentum-map-owner-or-edge-residual-coefficient-pack.md") else "fail",
            "detail": "722 next target matches this checkpoint",
        },
        {
            "check_id": "V723_4_prior_583_integrated",
            "result": "pass" if csv_contains(SOURCES["583_doc"]["path"], "edge residual template", "parent momentum-map owner not derived") else "fail",
            "detail": "old 583 owner-or-edge fork integrated",
        },
        {
            "check_id": "V723_5_owner_not_promoted",
            "result": "pass" if any(row["current_status"] == "fail_current_corpus" for row in momentum_map_owner_audit) else "fail",
            "detail": "momentum-map owner remains blocked",
        },
        {
            "check_id": "V723_6_owner_blockers_visible",
            "result": "pass"
            if {"missing_explicit_parent_L", "missing", "template_only", "not_computed", "not_derived", "not_signed"}.issubset(
                {row["current_status"] for row in momentum_map_owner_audit}
            )
            else "fail",
            "detail": "parent L, symplectic data, bracket, boundary, and matter blockers preserved",
        },
        {
            "check_id": "V723_7_edge_coefficients_present",
            "result": "pass"
            if {"Q_edge^H(lambda)", "Qbar_edge_XH(lambda)", "K_boundary[epsilon,eta]", "epsilon_PiM_X(lambda)", "K_edge(lambda)", "qbar_XT", "alpha_edge(lambda)"}.issubset(edge_symbols)
            else "fail",
            "detail": f"edge_rows={len(edge_residual_coefficient_pack)}",
        },
        {
            "check_id": "V723_8_edge_template_nonclaim",
            "result": "pass" if all(row["valid_for_claim"] == "false" for row in edge_residual_coefficient_pack) else "fail",
            "detail": "all edge coefficient rows remain nonclaim",
        },
        {
            "check_id": "V723_9_local_arenas_blocked",
            "result": "pass" if all(row["current_status"].startswith("blocked_") for row in local_observable_router) else "fail",
            "detail": "all local observable routes remain blocked",
        },
        {
            "check_id": "V723_10_next_target_selected",
            "result": "pass" if all(row["next_target"] == NEXT_TARGET for row in owner_or_edge_decision) else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V723_11_no_claim_rows_promoted",
            "result": "pass" if all_valid_false(generated_paths) else "fail",
            "detail": "all generated rows with valid_for_claim remain false",
        },
        {
            "check_id": "V723_12_outputs_scoped",
            "result": "pass" if under_post_checkpoint([OUTPUT_DOC, *generated_paths]) else "fail",
            "detail": "all outputs under post-checkpoint-work",
        },
        {
            "check_id": "V723_13_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V723_14_nonclaim_status",
            "result": "pass" if "nonclaim" in nonclaim_summary[0]["status"] else "fail",
            "detail": "claim ceiling blocks R10/WEP/PPN/Newton/local-GR claims",
        },
        {
            "check_id": "V723_15_source_register_written",
            "result": "pass" if len(source_register) >= 12 else "fail",
            "detail": f"source_rows={len(source_register)}",
        },
        {
            "check_id": "V723_16_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]

    validation_path = RESIDUALS / "P8_Y5_BRR545_723_VALIDATION.csv"
    write_csv(validation_path, validations, ["check_id", "result", "detail"])

    doc = f"""# 723 - Y5 R10 Affine-X Momentum Map Owner Or Edge Residual Coefficient Pack

## Summary

This checkpoint integrates the older 583 owner-or-edge fork into the current 720-722 `Z/M` chain.

The attempted elegant route is:

`i_v Omega_Y = delta G_X[epsilon]`, with `G_X[epsilon]=int_Sigma epsilon_nu C_X^nu + Q_boundary[epsilon]`.

If that parent momentum map exists, is equivariant, has `K_boundary=0`, and ordinary matter descends, then the affine `X` branch can be a real no-pole theorem.

Current verdict: **not derived**. The corpus still lacks the explicit parent `theta_Y/Omega_Y`, vertical generator, parent-owned `P[Y], J_eff[Y], P_mem[Y]`, bracket closure, and boundary zero.

So the edge does not get hidden. It is demoted into explicit residual coefficients:

`alpha_edge(lambda)=K_edge(lambda)*Qbar_edge_XH(lambda)*qbar_XT`.

| Field | Value |
| --- | --- |
| Generated UTC | `{GENERATED_UTC}` |
| Claim status | nonclaim/private checkpoint |
| Next target | `{NEXT_TARGET}` |

## Momentum Map Owner Audit

{markdown_table(momentum_map_owner_audit, ["audit_id", "needed_object", "current_status", "if_missing", "valid_for_claim"])}

## Edge Residual Coefficient Pack

{markdown_table(edge_residual_coefficient_pack, ["edge_id", "symbol", "formula", "current_status", "zero_condition", "if_nonzero", "valid_for_claim"])}

## Owner Or Edge Decision

{markdown_table(owner_or_edge_decision, ["decision_id", "question", "answer", "decision", "next_target", "valid_for_claim"])}

## Local Observable Router

{markdown_table(local_observable_router, ["arena_id", "arena", "route", "current_status", "claim_effect", "valid_for_claim"])}

## Bound Or Derive Queue

{markdown_table(bound_or_derive_queue, ["queue_id", "target", "preferred_route", "fallback_route", "priority", "next_artifact", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(nonclaim_summary, ["status", "claim_ceiling", "main_result", "edge_result", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_register, ["source_id", "path", "exists", "needle_check", "role"])}

## Validation

{markdown_table(validations, ["check_id", "result", "detail"])}

## Verdict

This is a useful fork, not a defeat. The no-pole theorem still has a clean mathematical shape, but it cannot be cashed without the parent symplectic/momentum-map certificate. Until that arrives, edge hair is not allowed to hide behind the word gauge. It becomes `Q_edge`, `Qbar_edge_XH`, `K_boundary`, `epsilon_PiM_X`, `K_edge`, `qbar_XT`, and `alpha_edge(lambda)`. Next move: either build an edge alpha envelope as nonclaim data plumbing, or repair the owner by writing the missing parent symplectic structure.
"""

    OUTPUT_DOC.write_text(doc, encoding="utf-8")
    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {validation_path}")
    print(f"validation_passes={sum(row['result'] == 'pass' for row in validations)}/{len(validations)}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
