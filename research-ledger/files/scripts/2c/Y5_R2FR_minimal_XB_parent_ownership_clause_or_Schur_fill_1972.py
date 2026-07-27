from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "1972-Y5-R2FR-minimal-XB-parent-ownership-clause-or-Schur-fill.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1972_VALIDATION.csv"

SOURCES = {
    "1971_doc": {
        "path": ROOT / "1971-Y5-R2FR-XB-curvature-independence-or-two-field-Schur-coefficient.md",
        "needles": ["CXR1971_1_exact_zero_condition", "CXR1971_2_verticality_not_enough", "NEXT1971_0_primary"],
    },
    "1971_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1971_VALIDATION.csv",
        "needles": ["VAL1971_OVERALL", "PASS"],
    },
    "85_XB_invariants": {
        "path": FORMALIZATION / "85-coarse-graining-invariants-XB.md",
        "needles": ["coarse_graining_invariants_XB_candidate_bundle_v1", "X_B = {", "A_curv", "This file does not prove the coarse-graining theorem."],
    },
    "83_parent_equations": {
        "path": FORMALIZATION / "83-parent-equations-v1.md",
        "needles": ["X_B cannot be selected differently", "q^nu = nabla^nu Gamma_eff - nabla_mu K_hat", "coarse-graining theorem for X_B"],
    },
    "1306_XB_domain": {
        "path": ROOT / "1306-Y5-R10-RAB-Zm-parent-function-or-XB-domain-range.md",
        "needles": ["FRA1306_1_XB_dependent", "XDG1306_0_argument_list", "XDG1306_4_arena_rule"],
    },
    "826_Ward_audit": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_826_WARD_BIANCHI_AUDIT.csv",
        "needles": ["W826_1_external_XB_spurion", "W826_3_Khat_required"],
    },
    "1349_KMTS_owner": {
        "path": ROOT / "1349-Y5-R10-RAB-KMTS-trace-projection-owner-or-memory-closure-declaration.md",
        "needles": ["KMTS1349_3_Ward_closure", "RESP1349_2_external_profiles"],
    },
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(row_id: str) -> dict[str, object]:
    return {
        "branch": BRANCH,
        "row_id": row_id,
        "valid_for_claim": False,
        "public_claim": False,
        "created_utc": stamp(),
    }


def ensure_dirs() -> None:
    for directory in (MTS_RESIDUALS, SOURCE_WEIGHT_DOCS, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, source_spec in SOURCES.items():
        path = source_spec["path"]
        needles = source_spec["needles"]
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        missing = [needle for needle in needles if needle not in text]
        row = base(source_id)
        row.update(
            {
                "source_path": str(path),
                "purpose": "1972 minimal X_B parent-ownership clause or Schur fill",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def minimal_clause_rows() -> list[dict[str, object]]:
    entries = [
        (
            "OWN1972_0_clause_target",
            "minimal X_B ownership clause",
            "Find a parent object X_env such that X_env=X_env[I_top,q_env,boundary_class] and D X_env[delta Phi_R]=0 for compact local curvature variations preserving branch/boundary data.",
            "TARGET_DEFINED",
            "This would make C_XR=0 without tuning a small coefficient.",
        ),
        (
            "OWN1972_1_relative_theorem",
            "relative curvature-independence theorem",
            "If X_env depends only on fixed topological/boundary/branch data and local variations delta Phi_R have compact support inside D_loc, then D X_env[delta Phi_R]=0.",
            "RELATIVE_CXR_ZERO_THEOREM",
            "The theorem is mathematically clean if the parent supplies X_env and the allowed-variation class.",
        ),
        (
            "OWN1972_2_required_variation_class",
            "allowed local curvature variation",
            "delta Phi_R changes g_obs/R_geom in the local exterior but preserves branch labels, boundary cohomology, and global coarse-graining data.",
            "VARIATION_CLASS_REQUIRED",
            "Without this tangent-space split, C_XR cannot be evaluated honestly.",
        ),
        (
            "OWN1972_3_Ward_safe_owner",
            "not an external spurion",
            "X_env must be a parent-owned field/label whose ancestors are varied, constrained, or topological; merely holding X_B fixed by hand fails Ward/Bianchi.",
            "SPURION_FIREWALL_REQUIRED",
            "This keeps the zero theorem from becoming a hidden nonconservation trick.",
        ),
        (
            "OWN1972_4_source_boundary_silence",
            "source/bath/boundary completion",
            "Source, bath, and boundary terms must either be independent of X_env under delta Phi_R or included in the same silent/topological variation theorem.",
            "SIDE_CHANNELS_REQUIRED",
            "C_XR=0 alone is not enough if source/boundary vertices reintroduce B_YR.",
        ),
        (
            "OWN1972_5_same_arena_rule",
            "same parent coefficient law",
            "The geometry-blind coefficient owner cannot be switched per galaxy/cosmology/local test after seeing data.",
            "ARENA_RULE_REQUIRED",
            "Protects the field-theory route from becoming a patchwork selector.",
        ),
        (
            "OWN1972_6_current_clause_status",
            "current corpus does not sign OWN1972_0..5",
            "The required X_env/variation split is not present as a parent action clause in the inspected source trail.",
            "MINIMAL_CLAUSE_NOT_SOURCE_SIGNED",
            "The clean zero route is a future architecture option, not a current derivation.",
        ),
    ]
    rows = []
    for row_id, object_name, clause, status, implication in entries:
        row = base(row_id)
        row.update(
            {
                "object": object_name,
                "clause": clause,
                "status": status,
                "implication": implication,
            }
        )
        rows.append(row)
    return rows


def current_xb_compatibility_rows() -> list[dict[str, object]]:
    entries = [
        (
            "XBI1972_0_current_XB_contains_curvature",
            "formalization-workbench 85 defines X_B with A_curv built from C_abs and R_abs",
            "A_curv = c^2 L_cg [w_C C_abs + w_R R_abs]/(c H_bg)",
            "CONTRADICTS_GEOMETRY_BLIND_ZERO_FOR_FULL_XB",
            "A full-bundle X_B cannot satisfy D X_B[delta Phi_R]=0 generically because it deliberately contains curvature diagnostics.",
        ),
        (
            "XBI1972_1_generic_derivative",
            "generic variation of the curvature diagnostic is nonzero",
            "delta A_curv ~= (c L_cg/H_bg)(w_C delta C_abs + w_R delta R_abs) + scale-response terms",
            "CXR_GENERALLY_NONZERO_IF_A_CURV_ENTERS_ACTION_COEFFICIENTS",
            "R2/fR danger is real if memory/action coefficients depend on the full X_B bundle.",
        ),
        (
            "XBI1972_2_safe_split_architecture",
            "possible repair: split coefficient owner from routing diagnostics",
            "X_B -> (X_env, X_route), with action coefficients Z_m,V_R,F_L depending only on geometry-blind X_env while A_curv lives only in a Ward-safe routing/readout sector",
            "SPLIT_ROUTE_IDENTIFIED_UNSIGNED",
            "This is the least destructive way to keep useful X_B diagnostics without forcing C_XR into the EH action.",
        ),
        (
            "XBI1972_3_forbidden_hide",
            "forbidden repair: call A_curv non-dynamical after using it in action coefficients",
            "A_curv in coefficients but fixed in variation is an external-spurion move unless a parent constraint/auxiliary action owns it",
            "FORBIDDEN_AS_THEOREM",
            "No local-GR claim may use this shortcut.",
        ),
        (
            "XBI1972_4_current_verdict",
            "full current X_B bundle does not support C_XR=0",
            "Because X_B includes curvature norms, the full-bundle zero theorem fails unless the active coefficient dependence excludes the curvature components or a projector annihilates them.",
            "FULL_XB_ZERO_ROUTE_FAILS_CURRENT_DEFINITION",
            "The next real leap is X_env/X_route split proof or Schur coefficient fill.",
        ),
    ]
    rows = []
    for row_id, finding, formula, status, consequence in entries:
        row = base(row_id)
        row.update(
            {
                "finding": finding,
                "formula": formula,
                "status": status,
                "consequence": consequence,
            }
        )
        rows.append(row)
    return rows


def route_split_rows() -> list[dict[str, object]]:
    entries = [
        (
            "ROUTE1972_0_geometry_blind_env",
            "X_env is branch/topological/boundary data",
            "C_XR=0 relative theorem can close if source/bath/boundary side channels are silent",
            "BEST_THEOREM_ROUTE_BUT_NOT_CURRENT_XB",
            "requires explicit split from A_curv-style diagnostics",
        ),
        (
            "ROUTE1972_1_full_invariant_bundle",
            "coefficients depend on the full X_B bundle from 85",
            "C_XR is generically nonzero because A_curv contains curvature norms",
            "SCHUR_ROUTE_REQUIRED",
            "must fill C_XR/H_X/H_mX rather than claim EH silence",
        ),
        (
            "ROUTE1972_2_readout_only_routing",
            "A_curv used only after variation as a diagnostic/routing label",
            "may be safe only if parent action coefficients do not depend on A_curv and Ward/Khat owner covers routing stress",
            "POSSIBLE_BUT_OWNER_MISSING",
            "needs a firewall proving routing diagnostics are not action couplings",
        ),
        (
            "ROUTE1972_3_auxiliary_constraint",
            "A_curv promoted to auxiliary constrained variable",
            "could be varied with a constraint action, but then its multiplier/stress contributes to the Schur/Khat block",
            "LIVE_FIELD_ROUTE",
            "not a zero theorem; source the auxiliary block",
        ),
        (
            "ROUTE1972_4_decision",
            "do not claim C_XR=0 for current full X_B",
            "either split X_env/X_route or fill the finite Schur coefficient matrix",
            "ROUTE_DECISION_NONCLAIM",
            "prevents the theory from smuggling a curvature diagnostic into the EH action",
        ),
    ]
    rows = []
    for row_id, route, result, status, next_action in entries:
        row = base(row_id)
        row.update({"route": route, "result": result, "status": status, "next_action": next_action})
        rows.append(row)
    return rows


def schur_fill_rows() -> list[dict[str, object]]:
    entries = [
        (
            "FILL1972_0_CXR",
            "C_XR or B_XR",
            "C_XR^A = delta X_B^A/delta R_geom; for A_curv branch include w_C,w_R,L_cg,H_bg and derivative of curvature norms",
            "MISSING_NUMERIC_OR_THEOREM_VALUE",
            "units: [X_B]/[R_geom]; source must state active X_B component and local branch",
        ),
        (
            "FILL1972_1_HX",
            "H_X",
            "second variation/operator for active X_B or auxiliary environment block",
            "MISSING_OPERATOR",
            "needed to invert the X_B response safely",
        ),
        (
            "FILL1972_2_Hm",
            "H_m",
            "-nabla_mu(Z_m nabla^mu)+V_mm plus source/boundary corrections",
            "PARTIAL_TEMPLATE_ONLY",
            "template exists but Z_m,V_mm,domain,sign still missing",
        ),
        (
            "FILL1972_3_HmX",
            "H_mX / V_mX",
            "mixed memory-environment Hessian for V_R(m;X_B), Z_m(X_B), and source terms",
            "MISSING_COUPLING",
            "the coupling bottleneck in literal form",
        ),
        (
            "FILL1972_4_BYR",
            "B_YR vector",
            "B_YR=(B_mR_direct+B_source+B_boundary, B_XR)",
            "MISSING_VECTOR",
            "required before Delta c_R2 can be computed",
        ),
        (
            "FILL1972_5_cR2",
            "generated R2/fR coefficient",
            "Delta c_R2=-1/2 B_YR^T H_Y^{-1} B_YR plus bare/measure/boundary terms under parent sign convention",
            "FORMULA_READY_VALUES_MISSING",
            "cannot compare to R11 bound curve until FILL1972_0..4 close",
        ),
        (
            "FILL1972_6_claim_guard",
            "claim eligibility",
            "all FILL rows require numeric/theorem value, units, domain, source path, and valid_for_claim=true before scoring",
            "CLAIM_BLOCKED",
            "keeps the Schur path honest and executable later",
        ),
    ]
    rows = []
    for row_id, object_name, formula, status, requirement in entries:
        row = base(row_id)
        row.update(
            {
                "object": object_name,
                "formula": formula,
                "status": status,
                "requirement": requirement,
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> list[dict[str, object]]:
    entries = [
        ("RUN1972_0_relative_clause", "OWN1972_1_relative_theorem", "PASS_RELATIVE_THEOREM", "geometry-blind X_env would give C_XR=0"),
        ("RUN1972_1_current_clause", "OWN1972_6_current_clause_status", "REJECTED_UNSIGNED", "minimal parent clause is not source-signed"),
        ("RUN1972_2_current_XB", "XBI1972_4_current_verdict", "REJECTED_FULL_XB_ZERO", "current full X_B contains curvature diagnostics"),
        ("RUN1972_3_schur_fill", "FILL1972_0..6", "REJECTED_MISSING_VALUES", "Schur inputs are staged but not source-backed"),
        ("RUN1972_VERDICT", "all_rows", "FULL_XB_CXR_ZERO_FAILS_SPLIT_OR_SCHUR_NEXT_NONCLAIM", "do not claim EH; choose X_env/X_route split proof or finite coefficient fill"),
    ]
    rows = []
    for row_id, input_row, runner_status, reason in entries:
        row = base(row_id)
        row.update(
            {
                "input_row": input_row,
                "runner_status": runner_status,
                "reason": reason,
                "accepted_for_claim": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    entries = [
        ("CG1972_0_geometry_blind_Xenv", "geometry-blind X_env parent clause is signed", "FAIL_BLOCKED", "relative theorem only, no source-signed parent clause"),
        ("CG1972_1_full_XB_CXR_zero", "current full X_B has C_XR=0", "FAIL_REJECTED", "A_curv curvature component makes generic C_XR nonzero"),
        ("CG1972_2_split_firewall", "X_env/X_route split firewall is derived", "FAIL_BLOCKED", "not yet built"),
        ("CG1972_3_schur_coefficients", "finite Schur coefficient pack is scoreable", "FAIL_BLOCKED", "C_XR/H_X/H_mX/B_YR values missing"),
        ("CG1972_4_EH_second_order", "EH second-order local action is derived", "FAIL_BLOCKED", "R2/fR gate open"),
        ("CG1972_5_local_GR_Newton", "local GR/Newton follows", "FAIL_BLOCKED", "EH plus PPN/matter gates remain"),
    ]
    rows = []
    for row_id, claim, status, reason in entries:
        row = base(row_id)
        row.update({"claim": claim, "status": status, "reason": reason})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    entries = [
        (
            "DEC1972_0_main_result",
            "FULL_XB_ZERO_ROUTE_REJECTED",
            "The current X_B candidate contains curvature diagnostics, so the full-bundle C_XR=0 theorem cannot be true generically.",
            "stop trying to prove C_XR=0 for the current full X_B bundle",
        ),
        (
            "DEC1972_1_best_next",
            "SPLIT_XB_OR_FILL_SCHUR",
            "To keep the local EH route alive, action coefficients must depend on a geometry-blind X_env, while curvature diagnostics move to a routing/readout sector with a Ward-safe owner; otherwise fill the Schur matrix.",
            "test the X_env/X_route split firewall next",
        ),
        (
            "DEC1972_2_project_read",
            "A_REAL_LEAP_NOT_A_DEAD_END",
            "This converts a vague coupling worry into a concrete architecture decision: split the variable or score the induced higher-curvature term.",
            "if split fails, begin C_XR first-row coefficient acquisition",
        ),
    ]
    rows = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1972_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1973-Y5-R2FR-XB-env-route-split-firewall-or-CXR-first-row.md",
            "target_script": "scripts/Y5_R2FR_XB_env_route_split_firewall_or_CXR_first_row_1973.py",
            "objective": "derive a firewall splitting geometry-blind action coefficient owner X_env from curvature routing diagnostics X_route, or fill the first nonclaim C_XR coefficient row",
            "acceptance_output": "split firewall theorem checklist or source-backed C_XR acquisition row template",
            "nonclaim_rule": "no EH/local-GR claim while full X_B contains active curvature diagnostics in action coefficients",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1972_0_project_position")
    row.update(
        {
            "strongest_result": "The clean X_B zero theorem is compatible only with a geometry-blind X_env, not with the current full X_B bundle containing A_curv.",
            "what_improved": "The local EH obstruction is now an architecture decision: split coefficient-owner variables from routing diagnostics or calculate the induced Schur/R2 term.",
            "still_missing": "X_env/X_route firewall, active coefficient dependency list, Ward-safe routing owner, C_XR, H_X, H_mX, source/bath/boundary vertices, units",
            "claim_status": "private nonclaim; current full-bundle C_XR=0 rejected",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1972_SOURCE_REGISTER.csv",
    "minimal_clause": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1972_MINIMAL_XB_OWNERSHIP_CLAUSE.csv",
    "xb_compatibility": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1972_CURRENT_XB_COMPATIBILITY_AUDIT.csv",
    "route_split": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1972_ROUTE_SPLIT_DECISION.csv",
    "schur_fill": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1972_SCHUR_FILL_INPUT_PACK.csv",
    "runner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1972_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1972_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1972_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1972_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1972_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "XB_OWNERSHIP_OR_SCHUR_1972_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1972_XB_SPLIT_OR_SCHUR_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1972_0_nonclaim_weight"),
            "artifact": "1972 minimal X_B parent ownership clause or Schur fill",
            "weight": "FULL_XB_ZERO_REJECTED_SPLIT_OR_SCHUR",
            "reason": "current full X_B includes curvature diagnostics; clean C_XR zero requires a geometry-blind coefficient owner",
        }
    ]
    queue = [
        {
            **base("AQ1972_0_Xenv_Xroute_split"),
            "target": "X_env/X_route split firewall",
            "needed_inputs": "active coefficient dependency list; proof coefficients ignore A_curv; Ward/Khat owner for routing diagnostics",
            "priority": "HIGHEST",
        },
        {
            **base("AQ1972_1_CXR_first_row"),
            "target": "first C_XR coefficient row",
            "needed_inputs": "active X_B component; derivative wrt R_geom; units; local branch; source path; nonclaim bound status",
            "priority": "FALLBACK_IF_SPLIT_FAILS",
        },
    ]
    return {
        "source_register": source_register(),
        "minimal_clause": minimal_clause_rows(),
        "xb_compatibility": current_xb_compatibility_rows(),
        "route_split": route_split_rows(),
        "schur_fill": schur_fill_rows(),
        "runner": runner_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
        "snapshot": snapshot_rows(),
        "source_weight": source_weight,
        "queue": queue,
    }


def validation_row(validation_id: str, status: str, detail: str) -> dict[str, object]:
    return {
        "validation_id": validation_id,
        "status": status,
        "detail": detail,
        "valid_for_claim": False,
        "public_claim": False,
    }


def formalization_hits() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = ("1972-", "*_1972_*", "*Y5*1972*", "*VAL1972*", "*P8*1972*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1972_00_sources", "PASS" if sources_ok else "FAIL", "all source paths exist and needles found"))

    theorem_ok = any(row["row_id"] == "OWN1972_1_relative_theorem" and row["status"] == "RELATIVE_CXR_ZERO_THEOREM" for row in tables["minimal_clause"])
    unsigned_ok = any(row["row_id"] == "OWN1972_6_current_clause_status" and row["status"] == "MINIMAL_CLAUSE_NOT_SOURCE_SIGNED" for row in tables["minimal_clause"])
    rows.append(validation_row("VAL1972_01_minimal_clause", "PASS" if theorem_ok and unsigned_ok else "FAIL", "minimal ownership clause formulated but unsigned"))

    curvature_ok = any(row["row_id"] == "XBI1972_0_current_XB_contains_curvature" and row["status"] == "CONTRADICTS_GEOMETRY_BLIND_ZERO_FOR_FULL_XB" for row in tables["xb_compatibility"])
    reject_ok = any(row["row_id"] == "XBI1972_4_current_verdict" and row["status"] == "FULL_XB_ZERO_ROUTE_FAILS_CURRENT_DEFINITION" for row in tables["xb_compatibility"])
    rows.append(validation_row("VAL1972_02_xb_compatibility", "PASS" if curvature_ok and reject_ok else "FAIL", "current full X_B zero route rejected"))

    split_ok = any(row["row_id"] == "ROUTE1972_2_readout_only_routing" and row["status"] == "POSSIBLE_BUT_OWNER_MISSING" for row in tables["route_split"])
    schur_required = any(row["row_id"] == "ROUTE1972_1_full_invariant_bundle" and row["status"] == "SCHUR_ROUTE_REQUIRED" for row in tables["route_split"])
    rows.append(validation_row("VAL1972_03_route_split", "PASS" if split_ok and schur_required else "FAIL", "split-or-Schur route selected"))

    fill_ok = all(row["status"] in {"MISSING_NUMERIC_OR_THEOREM_VALUE", "MISSING_OPERATOR", "PARTIAL_TEMPLATE_ONLY", "MISSING_COUPLING", "MISSING_VECTOR", "FORMULA_READY_VALUES_MISSING", "CLAIM_BLOCKED"} for row in tables["schur_fill"])
    rows.append(validation_row("VAL1972_04_schur_fill", "PASS" if fill_ok else "FAIL", "Schur fill rows staged as nonclaim missing inputs"))

    runner_ok = any(row["row_id"] == "RUN1972_VERDICT" and row["runner_status"] == "FULL_XB_CXR_ZERO_FAILS_SPLIT_OR_SCHUR_NEXT_NONCLAIM" for row in tables["runner"])
    rows.append(validation_row("VAL1972_05_runner", "PASS" if runner_ok else "FAIL", "runner blocks full-X_B C_XR zero claim"))

    gate_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(row["row_id"] == "CG1972_1_full_XB_CXR_zero" and row["status"] == "FAIL_REJECTED" for row in tables["claim_gate"])
    rows.append(validation_row("VAL1972_06_claim_gates", "PASS" if gate_ok else "FAIL", "all claim gates blocked or rejected"))

    decision_ok = any(row["decision"] == "FULL_XB_ZERO_ROUTE_REJECTED" for row in tables["decision"])
    rows.append(validation_row("VAL1972_07_decision", "PASS" if decision_ok else "FAIL", "decision ledger records full-X_B zero rejection"))

    next_ok = tables["next"][0]["target_doc"] == "1973-Y5-R2FR-XB-env-route-split-firewall-or-CXR-first-row.md"
    rows.append(validation_row("VAL1972_08_next_target", "PASS" if next_ok else "FAIL", "1973 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1972_09_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1972_10_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1972_11_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1972_12_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1972_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1972_OVERALL", overall, "1972 minimal X_B parent ownership clause or Schur fill"))
    return rows


def markdown_table(rows: list[dict[str, object]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, object]]], validation_rows: list[dict[str, object]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("Minimal X_B Ownership Clause", tables["minimal_clause"]),
        ("Current X_B Compatibility Audit", tables["xb_compatibility"]),
        ("Route Split Decision", tables["route_split"]),
        ("Schur Fill Input Pack", tables["schur_fill"]),
        ("Runner Dryrun", tables["runner"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1972 Y5 R2FR: Minimal X_B Parent Ownership Clause Or Schur Fill",
        "",
        "Private checkpoint. This tests whether the clean `C_XR=0` route from 1971 can be made compatible with the existing `X_B` definition.",
        "",
        "Verdict: the full current `X_B` bundle cannot honestly be geometry-blind, because `85-coarse-graining-invariants-XB.md` includes `A_curv`, built from curvature norms. A relative theorem exists for a geometry-blind `X_env`, but that is not the same as the present full `X_B` bundle. Therefore the next serious move is either an `X_env/X_route` split firewall or a finite two-field Schur coefficient fill.",
        "",
        "No EH/Newton/local-GR claim follows from this checkpoint.",
        "",
    ]
    for title, table_rows in sections:
        lines.extend([f"## {title}", "", markdown_table(table_rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    tables = build_tables()
    for output_name, path in OUTPUTS.items():
        write_csv(path, tables[output_name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1972_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
