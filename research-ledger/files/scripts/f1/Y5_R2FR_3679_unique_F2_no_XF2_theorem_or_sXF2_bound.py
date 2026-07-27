from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3679"
BRANCH_ID = "MTS_R2FR_Y5_UNIQUE_F2_NO_XF2_THEOREM_OR_SXF2_BOUND_3679"
DOC = ROOT / "3679-Y5-R2FR-unique-F2-no-XF2-theorem-or-sXF2-bound.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        rows = load_csv(path)
        return True, len(rows)
    except Exception:
        return False, 0


def parse_float(value: object) -> float:
    return float(str(value).strip())


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3678", RESIDUALS / "P8_Y5_R2FR_3678_NEXT_TARGET.csv", "unique-Maxwell-F2/no hidden XF2", "3678 selected the unique-F2/no-XF2 or s_XF2 bound target"),
        ("component_3678", RESIDUALS / "P8_Y5_R2FR_3678_SEM_COMPONENT_BOUND_REQUIREMENTS.csv", "SCB3678_1_s_XF2", "3678 exposed s_XF2 as the scalar Maxwell kinetic component inside s_EM"),
        ("allocation_3678", RESIDUALS / "P8_Y5_R2FR_3678_SEM_TARGET_ALLOCATION_ROWS.csv", "ALLOC3678_0_O1_gFXR", "3678 equal no-cancellation component budgets"),
        ("proof_3664", RESIDUALS / "P8_Y5_R2FR_3664_UNIQUE_F2_PROOF_ATTEMPT.csv", "COUNTERTERM_LEGAL_WITH_CURRENT_PARENT_GRAMMAR", "prior unique-F2 proof attempt found the hidden scalar counterterm legal"),
        ("closure_3665", RESIDUALS / "P8_Y5_R2FR_3665_UNIQUE_F2_CLOSURE_AUDIT.csv", "REJECT_ZERO_RETAIN_FINITE_COUPLING_INPUT", "prior closure audit retained finite F2 coupling input"),
        ("gates_3528", RESIDUALS / "P8_Y5_R2FR_3528_UNIQUE_F2_INHERITANCE_GATES.csv", "IF23528_2_no_hidden_F2_coefficient", "unique-F2 inheritance gate blocked by scalar obstruction"),
        ("domain_3528", RESIDUALS / "P8_Y5_R2FR_3528_OPERATOR_DOMAIN_RESULT.csv", "OP3528_2_hidden_scalar_lambda", "operator domain result keeps hidden scalar lambda branch live"),
        ("owner_3620", RESIDUALS / "P8_Y5_R2FR_3620_EM_SOURCE_OWNER_THEOREM_ATTEMPT.csv", "ESO3620_2_unique_F2", "EM/source owner packet says unique F2 closes only with current/source owner"),
        ("finite_3620", RESIDUALS / "P8_Y5_R2FR_3620_FINITE_F2_SOURCE_COEFFICIENT_ROWS.csv", "FSC3620_0_lambda_F2", "finite lambda_F2 row remains missing zero or numeric bound"),
        ("alpha_identity_3507", RESIDUALS / "P8_Y5_R2FR_3507_ALPHA_COUPLING_IDENTITY.csv", "ALPHA3507_1_vertical_residual_law", "canonical alpha identity links lambda_A and current normalization"),
        ("owner_gate_3507", RESIDUALS / "P8_Y5_R2FR_3507_PARENT_OWNER_GATE.csv", "GATE3507_1_no_independent_F2_counterterm", "parent owner gate for no independent F2 counterterm is unsigned"),
        ("doc_3506", ROOT / "3506-Y5-R2FR-parent-visible-EM-generator-signature-or-first-constitutive-bound-runner.md", "not killed by symmetry", "visible EM generator reduction leaves scalar gauge coupling throat"),
        ("doc_3620", ROOT / "3620-Y5-R2FR-EM-source-coupling-owner-or-F2-coefficient-bound.md", "lambda_F2=b_alpha=kappa_J=w_EM=0", "source-coupling owner packet closes only if all EM/source clauses sign together"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, relevance in specs:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "relevance": relevance,
            }
        )
    return rows


def allocation_values() -> dict[str, float]:
    rows = load_csv(RESIDUALS / "P8_Y5_R2FR_3678_SEM_TARGET_ALLOCATION_ROWS.csv")
    by_id = {row["allocation_id"]: row for row in rows}
    return {
        "o1_sem": parse_float(by_id["ALLOC3678_0_O1_gFXR"]["target_abs_s_EM"]),
        "o1_component": parse_float(by_id["ALLOC3678_0_O1_gFXR"]["equal_component_budget"]),
        "fourpi_sem": parse_float(by_id["ALLOC3678_1_4pi_gFXR"]["target_abs_s_EM"]),
        "fourpi_component": parse_float(by_id["ALLOC3678_1_4pi_gFXR"]["equal_component_budget"]),
    }


def theorem_audit_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "UF23679_0_target_theorem",
            "unique Maxwell F2/no hidden XF2 theorem",
            "parent action owns exactly one visible Maxwell kinetic block and has no independent hidden scalar multiplier f_X(X_N)F_Q^2",
            "TARGET_NOT_PROVED",
            "the desired zero would set s_XF2=0",
            "continue to clause audit",
        ),
        (
            "UF23679_1_visible_rank_reduction",
            "visible U(1), locality, reciprocity, and observed Hodge reduce the principal EM action to Maxwell form up to scalar/topological coefficients",
            "visible naturality removes anisotropic principal/skewon clutter but leaves scalar lambda_A and theta_A slots",
            "USEFUL_REDUCTION_NOT_ZERO",
            "the problem is narrowed to a scalar gauge-kinetic owner, not solved",
            "map lambda_A to s_XF2",
        ),
        (
            "UF23679_2_counterterm_legality",
            "Delta L = -(1/4) f_X(X_N) F_Q^2",
            "the term is gauge invariant, diffeomorphism invariant, local, and scalar if X_N is a parent-allowed hidden invariant",
            "COUNTERTERM_LEGAL_WITH_CURRENT_PARENT_GRAMMAR",
            "s_XF2 is not killed by gauge/diffeomorphism symmetry",
            "need a stronger parent-domain or no-Hom theorem",
        ),
        (
            "UF23679_3_no_hidden_visible_hom",
            "Hom(hidden residual scalars, visible F_Q^2)=0",
            "the parent grammar must prove hidden residual scalars have no morphism into the visible Maxwell kinetic coefficient",
            "NO_PARENT_SIGNATURE_FOUND",
            "hidden scalar lambda branch remains live",
            "retain finite coefficient branch",
        ),
        (
            "UF23679_4_operator_domain_exhaustion",
            "visible F2 image exhaustion",
            "all visible F_Q^2 terms must be images of the parent curvature norm, not extra representatives/readouts",
            "NOT_DERIVED_CURRENT_CORPUS",
            "ordinary symmetry cannot distinguish parent-owned lambda_A from an independent scalar dressing",
            "do not claim unique-F2 inheritance",
        ),
        (
            "UF23679_5_source_owner_packet",
            "F2/current/source coupling must close together",
            "closing lambda_A alone is insufficient if g_J, alpha readout, EM Hilbert weight, or source current can move the same physical knob",
            "OWNER_PACKET_UNSIGNED",
            "the coupling can migrate from F2 into current normalization",
            "use alpha identity with z_g retained",
        ),
        (
            "UF23679_6_verdict",
            "s_XF2 theorem-zero",
            "UF23679_1 through UF23679_5 must all close",
            "THEOREM_NOT_PROVED_RETAIN_CANONICAL_BOUND_BRANCH",
            "s_XF2=0 is not claimed; s_XF2 is promoted to a canonical component with exact alpha/current identity",
            "next target is z_g current owner or source-backed alpha/clock/WEP bound",
        ),
    ]
    return [
        {
            **base(ts),
            "audit_id": audit_id,
            "clause": clause,
            "required_signature": required_signature,
            "current_status": current_status,
            "consequence": consequence,
            "next_action": next_action,
            "source_signed": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for audit_id, clause, required_signature, current_status, consequence, next_action in specs
    ]


def canonical_map_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "MAP3679_0_action_block",
            "canonical EM/current block",
            "S_EM,J = -1/4 int lambda_A(X_hat) F_Q wedge *_obs F_Q + int g_J(X_hat) A_Q.J_Q",
            "lambda_A is the scalar Maxwell kinetic multiplier and g_J is the source/current normalization",
            "both are canonical X_hat functions after Z_X normalization",
            "DEFINITION_BRANCH_NONCLAIM",
        ),
        (
            "MAP3679_1_sXF2_definition",
            "scalar F2 component",
            "s_XF2 = D_Xhat ln lambda_A",
            "this is the canonical coefficient of hidden/motion/time dependence in the Maxwell kinetic block",
            "sign convention uses lambda_A as kinetic multiplier; inverse-coupling conventions flip the displayed sign",
            "PROMOTED_CANONICAL_COMPONENT",
        ),
        (
            "MAP3679_2_current_leg",
            "current normalization leg",
            "z_g = D_Xhat ln g_J",
            "current/source coupling drift is a physically equivalent place for the same charge normalization pressure to hide",
            "z_g must be zeroed or bounded before alpha data can isolate s_XF2",
            "LIVE_OWNER_THROAT",
        ),
        (
            "MAP3679_3_alpha_identity",
            "fine-structure vertical residual",
            "b_alpha_X = D_Xhat ln alpha_eff = 2 z_g - s_XF2",
            "canonical normalization gives g_eff=g_J/sqrt(lambda_A), so alpha_eff is proportional to g_eff^2",
            "exact identity inherited from 3507; it blocks pretending alpha bounds hit s_XF2 alone",
            "DERIVED_IDENTITY",
        ),
        (
            "MAP3679_4_zg_zero_branch",
            "current-owner closure branch",
            "if z_g=0 then s_XF2 = -b_alpha_X",
            "a parent proof that charge/current normalization descends rigidly would turn alpha-clock/WEP bounds into direct s_XF2 bounds",
            "requires source-current owner theorem, not a convention choice",
            "CONDITIONAL_DIRECT_BOUND_ROUTE",
        ),
        (
            "MAP3679_5_zg_live_branch",
            "current-owner open branch",
            "s_XF2 = 2 z_g - b_alpha_X",
            "without z_g closure, alpha data bounds a combination and the F2 coefficient can trade against source normalization",
            "future runner must score both variables or prove one zero",
            "RETAIN_TWO_KNOB_ROUTE",
        ),
        (
            "MAP3679_6_canonicalization_warning",
            "field-dependent normalization warning",
            "F(A)=lambda_A^(-1/2)[F_c - 1/2 dln(lambda_A) wedge A_c]",
            "setting lambda_A=1 by field convention is not a proof when X_hat varies; derivative interactions and current/readout terms move elsewhere",
            "prevents gauge-normalization sleight of hand",
            "NO_CONVENTION_SHORTCUT",
        ),
    ]
    return [
        {
            **base(ts),
            "map_id": map_id,
            "object": obj,
            "formula": formula,
            "meaning": meaning,
            "condition_or_warning": condition_or_warning,
            "status": status,
            "claim_allowed": False,
            "score_ready": False,
        }
        for map_id, obj, formula, meaning, condition_or_warning, status in specs
    ]


def bound_rows(ts: str) -> list[dict[str, object]]:
    values = allocation_values()
    specs = [
        (
            "SXF23679_0_equal_budget_O1",
            "abs(s_XF2)",
            f"{values['o1_component']:.12e}",
            "dimensionless canonical transfer",
            "3678 equal 8-leg no-cancellation budget under |g_FXR|<=1",
            str(RESIDUALS / "P8_Y5_R2FR_3678_SEM_TARGET_ALLOCATION_ROWS.csv"),
            "PRIVATE_TARGET_NOT_EVIDENCE",
            "budget only; not a measurement or parent derivation",
            False,
        ),
        (
            "SXF23679_1_equal_budget_4pi",
            "abs(s_XF2)",
            f"{values['fourpi_component']:.12e}",
            "dimensionless canonical transfer",
            "3678 equal 8-leg no-cancellation budget under |g_FXR|<=4pi",
            str(RESIDUALS / "P8_Y5_R2FR_3678_SEM_TARGET_ALLOCATION_ROWS.csv"),
            "PRIVATE_TARGET_NOT_EVIDENCE",
            "stricter budget only; not a measurement or parent derivation",
            False,
        ),
        (
            "SXF23679_2_alpha_clock_route",
            "b_alpha_X = 2 z_g - s_XF2",
            "MISSING_ALPHA_CLOCK_BOUND_VALUE",
            "dimensionless canonical vertical derivative",
            "clock/spectroscopy/fine-structure route",
            "MISSING_ALPHA_CLOCK_BOUND_SOURCE_PATH_OR_LOCAL_LEDGER_ROW",
            "MISSING_SOURCE_AND_ZG_OWNER",
            "cannot isolate s_XF2 until z_g is zeroed or jointly fitted",
            False,
        ),
        (
            "SXF23679_3_WEP_R10_route",
            "composition/source response from alpha sector",
            "MISSING_ALPHA_SOURCE_COMPOSITION_MAP",
            "dimensionless projected source coupling",
            "WEP/R10/local-source route",
            "MISSING_WEP_R10_BOUND_SOURCE_PATH_OR_LOCAL_LEDGER_ROW",
            "MISSING_SOURCE_MAP_AND_ARENA_PROJECTION",
            "requires material/source projection and z_g bookkeeping",
            False,
        ),
        (
            "SXF23679_4_parent_zg_zero_route",
            "abs(s_XF2) = abs(b_alpha_X)",
            "MISSING_ZG_ZERO_THEOREM_AND_ALPHA_BOUND",
            "dimensionless canonical transfer",
            "derivation-first route through charge/current owner",
            str(RESIDUALS / "P8_Y5_R2FR_3507_PARENT_OWNER_GATE.csv"),
            "CONDITIONAL_DIRECT_BOUND_ROUTE",
            "valid only if parent proves z_g=0 without reintroducing readout/source coefficients",
            False,
        ),
    ]
    return [
        {
            **base(ts),
            "bound_id": bound_id,
            "quantity": quantity,
            "bound_or_value": bound_or_value,
            "units": units,
            "route": route,
            "source_path_or_missing": source_path_or_missing,
            "status": status,
            "interpretation": interpretation,
            "valid_for_claim": valid_for_claim,
            "claim_allowed": False,
            "score_ready": False,
        }
        for bound_id, quantity, bound_or_value, units, route, source_path_or_missing, status, interpretation, valid_for_claim in specs
    ]


def alpha_link_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "ALINK3679_0_canonical_normalization",
            "g_eff = g_J/sqrt(lambda_A)",
            "canonical EM field normalization",
            "this is the exact reason F2 and current normalization cannot be treated independently",
            "DERIVED_FROM_3507",
        ),
        (
            "ALINK3679_1_alpha_residual",
            "b_alpha_X = 2 z_g - s_XF2",
            "vertical fine-structure residual",
            "alpha bounds constrain the difference between current drift and F2 drift",
            "DERIVED_IDENTITY",
        ),
        (
            "ALINK3679_2_sXF2_direct_if_zg_zero",
            "z_g=0 => s_XF2=-b_alpha_X",
            "current-owner theorem route",
            "this is the cleanest way to convert alpha/clock/WEP evidence into s_XF2 evidence",
            "CONDITIONAL_ON_PARENT_OWNER",
        ),
        (
            "ALINK3679_3_two_knob_if_zg_live",
            "z_g live => s_XF2=2z_g-b_alpha_X",
            "joint-bound route",
            "if z_g survives, the next test must fit or bound the two-dimensional vector rather than hammer only MTS",
            "BOUND_VECTOR_REQUIRED",
        ),
    ]
    return [
        {
            **base(ts),
            "link_id": link_id,
            "identity": identity,
            "arena": arena,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
            "score_ready": False,
        }
        for link_id, identity, arena, meaning, status in specs
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3679_0_unique_F2",
            "unique-F2/no-XF2 theorem does not close under current parent grammar",
            "REJECT_ZERO_FOR_NOW",
            "the counterterm f_X(X_N)F_Q^2 is legal under ordinary gauge/diffeomorphism symmetry",
            "do not circle; carry the finite scalar coefficient forward in canonical units",
        ),
        (
            "DEC3679_1_progress",
            "the live obstruction is now a two-knob identity, not a vague missing coupling",
            "PROMOTE_SXF2_ZG_IDENTITY",
            "s_XF2=D_Xhat ln lambda_A and b_alpha_X=2 z_g-s_XF2 gives a concrete attack surface",
            "attack z_g owner or build a source-backed two-knob bound runner",
        ),
        (
            "DEC3679_2_best_next",
            "derive z_g=0 before importing alpha bounds if possible",
            "DERIVATION_FIRST_ROUTE",
            "if current/source normalization is parent-rigid, alpha/clock/WEP data can directly bound s_XF2",
            "next checkpoint should target current owner or alpha bound route",
        ),
        (
            "DEC3679_3_claim_discipline",
            "no local-GR, Maxwell, WEP/R10, or public claim",
            "PRIVATE_NONCLAIM",
            "budgets are internal targets and source-backed alpha/WEP bounds are not yet attached",
            "keep work private and avoid GitHub promotion from this checkpoint",
        ),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "decision": decision,
            "status": status,
            "reason": reason,
            "next_action": next_action,
            "claim_allowed": False,
            "score_ready": False,
        }
        for decision_id, decision, status, reason, next_action in specs
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3679_0_sXF2_zero", "claim s_XF2=0", "BLOCKED_NONCLAIM", "unique-F2/no-XF2 theorem is not parent-signed"),
        ("CG3679_1_sXF2_numeric", "score finite s_XF2", "BLOCKED_SOURCE_MISSING", "alpha/clock/WEP source rows and z_g owner are missing"),
        ("CG3679_2_alpha_direct_bound", "treat alpha bound as direct s_XF2 bound", "BLOCKED_ZG_LIVE", "b_alpha_X=2 z_g-s_XF2 unless z_g=0 is proved"),
        ("CG3679_3_local_GR", "claim local-GR/PPN pass", "BLOCKED_NONCLAIM", "EM/source coupling residual vector remains open"),
        ("CG3679_4_public_or_github", "public/GitHub promotion", "BLOCKED_PRIVATE", "private derivation checkpoint only"),
    ]
    return [
        {
            **base(ts),
            "claim_gate_id": claim_gate_id,
            "gate": gate,
            "status": status,
            "reason": reason,
            "claim_allowed": False,
            "score_ready": False,
        }
        for claim_gate_id, gate, status, reason in specs
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    values = allocation_values()
    return [
        {
            **base(ts),
            "status": "UNIQUE_F2_ZERO_NOT_PROVED_SXF2_CANONICAL_ALPHA_IDENTITY_PROMOTED_NONCLAIM",
            "summary": "3679 rejects a shortcut unique-F2/no-XF2 zero proof under the current parent grammar because hidden scalar F2 dressing is not killed by gauge/diffeomorphism symmetry. It converts the obstruction into the canonical identity s_XF2=D_Xhat ln lambda_A and b_alpha_X=2 z_g-s_XF2, with z_g=D_Xhat ln g_J.",
            "claim_ceiling": "no s_XF2 zero, alpha-bound, source-coupling, Maxwell/local-GR, WEP/R10, PPN, or public claim is made",
            "useful_result": f"the internal 3678 component targets are |s_XF2|<={values['o1_component']:.12e} under |g_FXR|<=1 and |s_XF2|<={values['fourpi_component']:.12e} under |g_FXR|<=4pi; these are target budgets, not evidence",
            "next_missing_piece": "derive z_g=0 from parent current/source owner, or build a source-backed alpha/clock/WEP two-knob bound route for b_alpha_X=2 z_g-s_XF2",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3679_0",
            "target_doc": "3680-Y5-R2FR-zg-current-owner-or-alpha-bound-route-for-sXF2.md",
            "target_script": "scripts/Y5_R2FR_3680_zg_current_owner_or_alpha_bound_route_for_sXF2.py",
            "objective": "derive the parent current/source owner condition z_g=0 so alpha/clock/WEP data directly bounds s_XF2, or build a nonclaim two-knob bound route for b_alpha_X=2 z_g-s_XF2",
            "success_gate": "either z_g is theorem-zero from parent charge/current ownership, or the next runner has sourced alpha/clock/WEP rows that explicitly retain z_g and do not treat alpha drift as direct s_XF2 evidence",
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    theorem_audit: list[dict[str, object]],
    maps: list[dict[str, object]],
    bounds: list[dict[str, object]],
    alpha_links: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3679 - Unique-F2/no-XF2 theorem or s_XF2 bound",
        "",
        f"**Status:** {status[0]['status']}",
        "",
        "This checkpoint takes the 3678 throat seriously rather than just writing another missing-piece note. The unique-F2/no hidden-XF2 theorem is attempted and rejected under the current parent grammar: a hidden scalar multiplier `f_X(X_N)F_Q^2` is **not killed by gauge/diffeomorphism symmetry**.",
        "",
        "## Main result",
        "",
        "`s_XF2 = D_Xhat ln lambda_A` is promoted as the canonical scalar Maxwell-kinetic residual.",
        "",
        "The fine-structure/current identity is:",
        "",
        "`b_alpha_X = 2 z_g - s_XF2`, with `z_g = D_Xhat ln g_J`.",
        "",
        "Therefore alpha/clock/WEP evidence cannot be used as a direct `s_XF2` bound unless the parent theory first proves `z_g=0`. If `z_g=0`, then `s_XF2 = -b_alpha_X`.",
        "",
        "## Theorem audit",
    ]
    for row in theorem_audit:
        lines.append(f"- `{row['audit_id']}`: {row['current_status']} - {row['clause']} -> {row['consequence']}")
    lines.extend(["", "## Canonical map"])
    for row in maps:
        lines.append(f"- `{row['map_id']}`: {row['status']} - `{row['formula']}`")
    lines.extend(["", "## Bound/input rows"])
    for row in bounds:
        lines.append(f"- `{row['bound_id']}`: {row['status']} - `{row['quantity']}` -> `{row['bound_or_value']}`; {row['interpretation']}")
    lines.extend(["", "## Alpha/current links"])
    for row in alpha_links:
        lines.append(f"- `{row['link_id']}`: {row['status']} - `{row['identity']}` -> {row['meaning']}")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['status']} - {row['decision']} -> {row['next_action']}")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['claim_gate_id']}`: {row['status']} - {row['gate']} because {row['reason']}")
    lines.extend(
        [
            "",
            "## Next target",
            f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.",
            "",
            "## Sources",
        ]
    )
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['source_path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    ts: str,
    output_paths: list[Path],
    sources: list[dict[str, object]],
    theorem_audit: list[dict[str, object]],
    maps: list[dict[str, object]],
    bounds: list[dict[str, object]],
    alpha_links: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    generated = sources + theorem_audit + maps + bounds + alpha_links + decisions + gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3679*", "3679-Y5-R2FR-*", "P8_Y5*3679*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    audit_statuses = {str(row["current_status"]) for row in theorem_audit}
    map_formulas = " ".join(str(row["formula"]) for row in maps)
    bound_by_id = {str(row["bound_id"]): row for row in bounds}

    add("VAL3679_0_sources_exist", all(row["exists"] for row in sources), "every cited source path exists")
    add("VAL3679_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3679_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3679 outputs written")
    add("VAL3679_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3679_4_counterterm_legal", "COUNTERTERM_LEGAL_WITH_CURRENT_PARENT_GRAMMAR" in audit_statuses, "theorem audit records legal hidden scalar F2 counterterm")
    add("VAL3679_5_no_hom_missing", any(row["audit_id"] == "UF23679_3_no_hidden_visible_hom" and row["current_status"] == "NO_PARENT_SIGNATURE_FOUND" for row in theorem_audit), "no hidden-visible Hom theorem remains unsigned")
    add("VAL3679_6_verdict_nonzero", any(row["audit_id"] == "UF23679_6_verdict" and row["current_status"] == "THEOREM_NOT_PROVED_RETAIN_CANONICAL_BOUND_BRANCH" for row in theorem_audit), "s_XF2 zero is not claimed")
    add("VAL3679_7_sXF2_map", "s_XF2 = D_Xhat ln lambda_A" in map_formulas, "canonical s_XF2 map present")
    add("VAL3679_8_alpha_identity", "b_alpha_X = D_Xhat ln alpha_eff = 2 z_g - s_XF2" in map_formulas, "alpha-current-F2 identity present")
    add("VAL3679_9_budget_rows", all(key in bound_by_id for key in ["SXF23679_0_equal_budget_O1", "SXF23679_1_equal_budget_4pi"]) and all(parse_float(bound_by_id[key]["bound_or_value"]) > 0 for key in ["SXF23679_0_equal_budget_O1", "SXF23679_1_equal_budget_4pi"]), "O1 and 4pi s_XF2 component budgets are positive numeric rows")
    add("VAL3679_10_bound_routes_nonclaim", all(row["claim_allowed"] is False and row["score_ready"] is False and row["valid_for_claim"] is False for row in bounds), "all bound/input rows remain nonclaim")
    add("VAL3679_11_alpha_route_blocked", any(row["bound_id"] == "SXF23679_2_alpha_clock_route" and "z_g" in row["interpretation"] and str(row["bound_or_value"]).startswith("MISSING_") for row in bounds), "alpha/clock route keeps z_g and missing source explicit")
    add("VAL3679_12_decision_next", next_target[0]["target_doc"].startswith("3680-") and "z_g" in next_target[0]["objective"], "3680 selects z_g current owner or alpha bound route")
    add("VAL3679_13_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" or str(row.get("score_ready", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim and unscoreable")
    add("VAL3679_14_doc_written", "not killed by gauge/diffeomorphism symmetry" in doc_text and "s_XF2 = D_Xhat ln lambda_A" in doc_text and "b_alpha_X = 2 z_g - s_XF2" in doc_text, "doc records the theorem rejection and canonical identity")
    add("VAL3679_15_claim_gates_blocked", all(row["claim_allowed"] is False and row["score_ready"] is False for row in gates), "claim gates remain blocked")
    add("VAL3679_16_no_formalization_leak", not leaks, "no 3679 checkpoint files in formalization-workbench")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    theorem_audit = theorem_audit_rows(ts)
    maps = canonical_map_rows(ts)
    bounds = bound_rows(ts)
    alpha_links = alpha_link_rows(ts)
    decisions = decision_rows(ts)
    gates = claim_gate_rows(ts)
    status = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3679_SOURCE_REGISTER.csv",
        "theorem": RESIDUALS / "P8_Y5_R2FR_3679_UNIQUE_F2_THEOREM_AUDIT.csv",
        "maps": RESIDUALS / "P8_Y5_R2FR_3679_SXF2_CANONICAL_MAP_ROWS.csv",
        "bounds": RESIDUALS / "P8_Y5_R2FR_3679_SXF2_BOUND_INPUT_ROWS.csv",
        "alpha": RESIDUALS / "P8_Y5_R2FR_3679_ALPHA_IDENTITY_LINK_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3679_DECISION_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3679_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3679_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3679_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3679_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["theorem"], theorem_audit)
    write_csv(outputs["maps"], maps)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["alpha"], alpha_links)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, theorem_audit, maps, bounds, alpha_links, decisions, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, theorem_audit, maps, bounds, alpha_links, decisions, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3679 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3679 checkpoint: unique-F2 zero rejected for now; s_XF2 mapped to b_alpha_X=2 z_g-s_XF2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
