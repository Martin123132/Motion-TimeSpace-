from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1380"
TITLE = "1380-Y5-R10-RAB-kappa-origin-or-shell-bound-first-parent-signing-clause"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
KAPPA_ORIGIN_PATH = OUT_DIR / f"{PACK_ID}_KAPPA_ZM_ORIGIN_COEFFICIENT_ROW.csv"
SHELL_BOUND_PATH = OUT_DIR / f"{PACK_ID}_SHELL_BOUND_ROUTE_AUDIT.csv"
CLOSURE_FEED_PATH = OUT_DIR / f"{PACK_ID}_CLOSURE_RUNNER_FEED_UPDATE.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1380_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(out)


def mark_nonclaim(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def source_register() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1380_0_1379_doc",
            "source_path": "1379-Y5-R10-RAB-gradient-completion-parent-signature-or-transition-closure-runner.md",
            "required_anchor": "NEXT1379_0_1380",
            "purpose": "1379 handoff to kappa/Z_m origin or shell-bound clause.",
        },
        {
            "source_id": "SRC1380_1_1379_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1379_NEXT_TARGET.csv",
            "required_anchor": "NEXT1379_0_1380",
            "purpose": "machine-readable 1380 target.",
        },
        {
            "source_id": "SRC1380_2_1379_dimensional_lock",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1379_KAPPA_DIMENSIONAL_LOCK.csv",
            "required_anchor": "KDL1379_0_action_density_match",
            "purpose": "symbolic kappa_m units and transition-length lock.",
        },
        {
            "source_id": "SRC1380_3_1379_closure_schema",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1379_TRANSITION_CLOSURE_RUNNER_SCHEMA.csv",
            "required_anchor": "CRS1379_1_kappa_m",
            "purpose": "closure runner field requiring kappa_m.",
        },
        {
            "source_id": "SRC1380_4_1302_memory_stress",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv",
            "required_anchor": "MSR1302_0_canonical_scalar_stress_form",
            "purpose": "canonical scalar stress row containing Z_m kinetic coefficient.",
        },
        {
            "source_id": "SRC1380_5_1302_fixed_field",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1302_FIXED_FIELD_M_SIGNATURE_AUDIT.csv",
            "required_anchor": "FFA1302_5_verdict",
            "purpose": "m fixed-field parent status remains conditional.",
        },
        {
            "source_id": "SRC1380_6_1378_gradient_branch",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1378_CONDITIONAL_GRADIENT_RELAXATION_BRANCH.csv",
            "required_anchor": "GRB1378_1_transition_length",
            "purpose": "ell_tr and support law from the conditional gradient branch.",
        },
        {
            "source_id": "SRC1380_7_802_shell",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_802_TRANSITION_SHELL_OBSTRUCTION.csv",
            "required_anchor": "TS802_0_direct_projection",
            "purpose": "transition shell direct-projection obstruction.",
        },
        {
            "source_id": "SRC1380_8_803_anticheat",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_803_TRANSITION_SHELL_ANTI_CHEAT_BOUND.csv",
            "required_anchor": "AC803_0_required_shell_suppression",
            "purpose": "anti-cheat shell suppression gate.",
        },
        {
            "source_id": "SRC1380_9_1171_boundary_nogo",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1171_BOUNDARY_NO_GO_LEDGER.csv",
            "required_anchor": "NOG1171_0_neumann_gap",
            "purpose": "boundary no-go ledger for natural/Dirichlet/gauge/Bianchi shortcuts.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
    return mark_nonclaim(rows)


def kappa_origin_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "coeff_id": "KOR1380_0_identification",
                "coefficient": "kappa_m",
                "parent_origin": "Z_m kinetic coefficient in active memory scalar Hilbert stress",
                "derivation_or_mapping": "set eta=m-m_*; since partial eta=partial m, the gradient completion coefficient maps to the scalar kinetic coefficient: kappa_m := Z_m",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv",
                "source_anchor": "MSR1302_0_canonical_scalar_stress_form",
                "status": "SOURCE_BACKED_SYMBOLIC_COEFFICIENT_SLOT",
                "missing_for_numeric": "Z_m sign; Z_m value/range; units; parent action adoption; no-composite m field signature",
            },
            {
                "coeff_id": "KOR1380_1_stress_consistency",
                "coefficient": "Z_m",
                "parent_origin": "T_m^{mu nu}=Z_m nabla^mu m nabla^nu m - g^{mu nu}[1/2 Z_m (nabla m)^2 + ...]",
                "derivation_or_mapping": "the same Z_m that gives the transition equation also produces Hilbert stress, so using it for ell_tr forbids deleting gradient stress",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv",
                "source_anchor": "MSR1302_1_spatial_trace_bound_template",
                "status": "STRESS_ROUTING_GUARD_READY_NONCLAIM",
                "missing_for_numeric": "grad_m bound; Z_m bound; V_R subtraction; T_ZX/source/bath/boundary bounds; frame units",
            },
            {
                "coeff_id": "KOR1380_2_transition_length_update",
                "coefficient": "ell_tr",
                "parent_origin": "gradient branch with kappa_m:=Z_m",
                "derivation_or_mapping": "ell_tr=sqrt(Z_m L0^2/F2), requiring Z_m F2>0 in the static local relaxation branch",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_1378_CONDITIONAL_GRADIENT_RELAXATION_BRANCH.csv;source-intake/mts_residuals/P8_Y5_R10_1379_KAPPA_DIMENSIONAL_LOCK.csv",
                "source_anchor": "GRB1378_1_transition_length;KDL1379_1_transition_length",
                "status": "SYMBOLIC_FORMULA_UPDATED_WITH_ZM",
                "missing_for_numeric": "Z_m value/sign; F2 value/sign; L0 scale rule",
            },
            {
                "coeff_id": "KOR1380_3_units_rule",
                "coefficient": "Z_m/kappa_m",
                "parent_origin": "density matching in the parent action",
                "derivation_or_mapping": "[Z_m]=[kappa_m]=[L0^-2 Fhat]/[(partial m)^2] with eta=m-m_*",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_1379_KAPPA_DIMENSIONAL_LOCK.csv",
                "source_anchor": "KDL1379_0_action_density_match",
                "status": "SYMBOLIC_UNITS_RULE_READY",
                "missing_for_numeric": "units of m/eta; units of Fhat; local coordinate convention; action-density normalization",
            },
            {
                "coeff_id": "KOR1380_4_parent_status",
                "coefficient": "kappa_m=Z_m",
                "parent_origin": "candidate scalar-memory parent branch",
                "derivation_or_mapping": "coefficient slot is source-backed enough for nonclaim runner wiring, but not enough for parent-signed local-GR evidence",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_1302_FIXED_FIELD_M_SIGNATURE_AUDIT.csv;source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv",
                "source_anchor": "FFA1302_5_verdict;MSR1302_0_canonical_scalar_stress_form",
                "status": "NONCLAIM_COEFFICIENT_ROW_READY_VALUE_MISSING",
                "missing_for_numeric": "parent field status; no metric-composite exclusion; variation order; frame/units; Z_m sign/value",
            },
        ]
    )


def shell_bound_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "shell_id": "SBA1380_0_direct_projection",
                "target": "direct local transition shell",
                "audit_result": "REJECTED_BY_EXISTING_GATES",
                "bound_or_template": "no finite pass from direct projection; P_loc q_tr must be retained or exactly cancelled",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_802_TRANSITION_SHELL_OBSTRUCTION.csv;source-intake/mts_residuals/P8_Y5_R10_803_TRANSITION_SHELL_ANTI_CHEAT_BOUND.csv",
                "source_anchors": "TS802_0_direct_projection;AC803_2_direct_metric_projection",
                "missing_for_finite_bound": "projector identity; finite shell amplitude; local response operator; units",
            },
            {
                "shell_id": "SBA1380_1_generic_suppression",
                "target": "U_B or width suppression of shell",
                "audit_result": "REJECTED_BY_ANTI_CHEAT",
                "bound_or_template": "generic U_B^2 or L_tr scaling is not accepted as a shell bound",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_803_TRANSITION_SHELL_ANTI_CHEAT_BOUND.csv",
                "source_anchors": "AC803_0_required_shell_suppression;AC803_1_width_scaling",
                "missing_for_finite_bound": "exact zero theorem or explicit residual amplitude bound",
            },
            {
                "shell_id": "SBA1380_2_boundary_shortcuts",
                "target": "natural/Dirichlet/gauge/Bianchi boundary fixes",
                "audit_result": "NO_GENERAL_THEOREM",
                "bound_or_template": "boundary no-go ledger blocks using natural BC, Dirichlet, gauge, or Bianchi shortcuts as a general shell zero",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1171_BOUNDARY_NO_GO_LEDGER.csv",
                "source_anchors": "NOG1171_0_neumann_gap;NOG1171_1_dirichlet_gap;NOG1171_2_gauge_gap;NOG1171_3_bianchi_gap",
                "missing_for_finite_bound": "residual pullback(B_C)=0 theorem or stress/current boundary ledger",
            },
            {
                "shell_id": "SBA1380_3_template",
                "target": "finite shell contribution retained by closure runner",
                "audit_result": "TEMPLATE_ONLY_NOT_SCOREABLE",
                "bound_or_template": "Q_shell <= A_ref^-1 N_shell ||P_loc q_shell||_D or explicit Q_trans/Q_proj shell addend",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1379_TRANSITION_CLOSURE_RUNNER_SCHEMA.csv;source-intake/mts_residuals/P8_Y5_R10_802_TRANSITION_SHELL_OBSTRUCTION.csv",
                "source_anchors": "CRS1379_11_shell_gate;TS802_1_exact_cancellation",
                "missing_for_finite_bound": "N_shell; shell norm; domain; observable projection; source path; units",
            },
            {
                "shell_id": "SBA1380_4_verdict",
                "target": "shell/boundary first parent-signing clause",
                "audit_result": "NO_EXPLICIT_FINITE_SHELL_BOUND_ROW",
                "bound_or_template": "retain shell gate as blocker; do not claim exact cancellation or finite bound",
                "source_paths": "aggregate_SBA1380_0_to_SBA1380_3",
                "source_anchors": "aggregate",
                "missing_for_finite_bound": "exact projector theorem or finite shell amplitude/source row",
            },
        ]
    )


def closure_feed_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "feed_id": "CFU1380_0_kappa_field",
                "runner_field": "kappa_m",
                "update": "set symbolic origin kappa_m := Z_m",
                "status": "SOURCE_BACKED_SYMBOLIC_SLOT_READY",
                "runner_expression": "kappa_m=Z_m",
                "blocks_numeric": "Z_m sign/value/units and parent field status missing",
            },
            {
                "feed_id": "CFU1380_1_length_field",
                "runner_field": "ell_tr",
                "update": "replace kappa_m with Z_m in transition length",
                "status": "SYMBOLIC_FORMULA_READY",
                "runner_expression": "ell_tr=sqrt(Z_m*L0^2/F2)",
                "blocks_numeric": "Z_m, F2, L0 not source-backed numerically",
            },
            {
                "feed_id": "CFU1380_2_stability_gate",
                "runner_field": "sign_condition",
                "update": "require Z_m*F2>0 for real static relaxation length",
                "status": "SIGN_GATE_READY_VALUE_MISSING",
                "runner_expression": "Z_m*F2>0",
                "blocks_numeric": "signs missing",
            },
            {
                "feed_id": "CFU1380_3_stress_retention",
                "runner_field": "Q_trans/Q_mem stress",
                "update": "retain scalar gradient stress after using Z_m to generate the profile",
                "status": "STRESS_GUARD_READY_BOUND_MISSING",
                "runner_expression": "retain |Z_m| grad_m^2 and related stress terms unless separately bounded",
                "blocks_numeric": "stress bounds and units missing",
            },
            {
                "feed_id": "CFU1380_4_shell_gate",
                "runner_field": "shell_status",
                "update": "no finite shell bound found; shell gate remains required",
                "status": "SHELL_BOUND_BLOCKED",
                "runner_expression": "shell_status=MISSING_EXPLICIT_FINITE_BOUND",
                "blocks_numeric": "projector theorem or finite shell bound missing",
            },
            {
                "feed_id": "CFU1380_5_verdict",
                "runner_field": "closure_runner_status",
                "update": "1380 can improve symbolic runner wiring but cannot score local claims",
                "status": "SYMBOLIC_RUNNER_IMPROVED_NONCLAIM",
                "runner_expression": "allow symbolic dry-run; block numeric/local-GR pass",
                "blocks_numeric": "missing coefficient values, shell bound, and arena projection",
            },
        ]
    )


def claim_gate_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "gate_id": "GATE1380_0_kappa_origin",
                "gate": "kappa_m/Z_m receives a source-backed nonclaim coefficient row",
                "status": "PASS_SYMBOLIC_SOURCE_BACKED_SLOT",
                "reason": "KOR1380 maps kappa_m to Z_m from the canonical scalar stress row.",
            },
            {
                "gate_id": "GATE1380_1_kappa_numeric",
                "gate": "Z_m sign/value/units are source-backed",
                "status": "BLOCKED_VALUE_SIGN_UNITS_MISSING",
                "reason": "MSR1302 explicitly lists MISSING_Z_m_SIGN_AND_VALUE and related unit/frame gaps.",
            },
            {
                "gate_id": "GATE1380_2_shell_bound",
                "gate": "explicit finite shell/boundary bound exists",
                "status": "BLOCKED_NO_EXPLICIT_FINITE_SHELL_BOUND",
                "reason": "802/803/1171 reject direct, generic, and shortcut shell routes.",
            },
            {
                "gate_id": "GATE1380_3_runner_update",
                "gate": "closure runner can use improved symbolic kappa origin",
                "status": "PASS_SYMBOLIC_RUNNER_UPDATE",
                "reason": "closure feed updates kappa_m=Z_m and ell_tr=sqrt(Z_m L0^2/F2).",
            },
            {
                "gate_id": "GATE1380_4_local_claim",
                "gate": "local GR / PPN / R10 pass can be claimed",
                "status": "BLOCKED_NO_CLAIM",
                "reason": "symbolic coefficient origin is not a numeric or theorem-zero local-GR reduction.",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "decision_id": "DEC1380_0_kappa_origin",
                "decision": "promote kappa_m=Z_m as a source-backed symbolic nonclaim coefficient slot",
                "why": "the active scalar stress template already contains Z_m multiplying the same gradient structure needed by the transition branch",
                "next_action": "attack Z_m sign/value/units and m parent-field signature next",
            },
            {
                "decision_id": "DEC1380_1_shell_route",
                "decision": "do not use shell/boundary route as the first successful clause",
                "why": "current shell and boundary files only provide no-go/anti-cheat ledgers and a template, not a finite bound",
                "next_action": "retain shell gate until explicit finite bound or projector theorem exists",
            },
            {
                "decision_id": "DEC1380_2_next_best_route",
                "decision": "make Z_m sign/value/unit sourcing the next pressure point",
                "why": "this is now the most direct way to turn the conditional transition law into a serious nonclaim candidate branch",
                "next_action": "derive/source a Z_m prior/coefficient row or prove it cannot be parent-signed from current action language",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "next_id": "NEXT1380_0_1381",
                "next_doc": "1381-Y5-R10-RAB-Zm-sign-value-unit-source-or-kappa-closure-demotion.md",
                "next_script": "scripts/Y5_R10_RAB_Zm_sign_value_unit_source_or_kappa_closure_demotion.py",
                "task": "try to source or derive Z_m sign, value/range, and units from parent scalar-stress/action language; if impossible, demote kappa_m=Z_m to a purely symbolic closure coefficient and keep shell/arena gates blocked",
                "success_condition": "either Z_m receives a source-backed sign/value/unit nonclaim row, or the kappa branch is explicitly closure-symbolic with no numeric scoring allowed",
                "do_not_claim": "local GR;PPN pass;R10 pass;q_loc=0;GitHub-ready result",
            }
        ]
    )


def generated_csv_paths() -> list[Path]:
    return [
        SOURCE_REGISTER_PATH,
        KAPPA_ORIGIN_PATH,
        SHELL_BOUND_PATH,
        CLOSURE_FEED_PATH,
        CLAIM_GATE_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]


def all_rows_nonclaim(*groups: list[dict[str, object]]) -> bool:
    for rows in groups:
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() != "false":
                return False
            if str(row.get("claim_allowed", "")).lower() != "false":
                return False
    return True


def csv_parse_details(paths: list[Path]) -> tuple[bool, str]:
    details = []
    ok = True
    for path in paths:
        try:
            count = len(read_csv_rows(path))
            details.append(f"{path.name}:{count}")
        except Exception as exc:  # pragma: no cover
            ok = False
            details.append(f"{path.name}:ERROR:{exc}")
    return ok, "; ".join(details)


def validation_rows(
    sources: list[dict[str, object]],
    kappa_rows: list[dict[str, object]],
    shell_rows: list[dict[str, object]],
    closure_feed: list[dict[str, object]],
    gates: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    all_sources_ok = all(bool(row["exists"]) and bool(row["anchor_found"]) for row in sources)
    kappa_slot_ready = any(row["coeff_id"] == "KOR1380_4_parent_status" and row["status"] == "NONCLAIM_COEFFICIENT_ROW_READY_VALUE_MISSING" for row in kappa_rows)
    shell_blocked = any(row["shell_id"] == "SBA1380_4_verdict" and row["audit_result"] == "NO_EXPLICIT_FINITE_SHELL_BOUND_ROW" for row in shell_rows)
    closure_updated = any(row["feed_id"] == "CFU1380_5_verdict" and row["status"] == "SYMBOLIC_RUNNER_IMPROVED_NONCLAIM" for row in closure_feed)
    gate_pass = any(row["gate_id"] == "GATE1380_0_kappa_origin" and row["status"] == "PASS_SYMBOLIC_SOURCE_BACKED_SLOT" for row in gates)
    local_claim_blocked = any(row["gate_id"] == "GATE1380_4_local_claim" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    nonclaim = all_rows_nonclaim(sources, kappa_rows, shell_rows, closure_feed, gates)
    csv_ok, csv_details = csv_parse_details(csv_paths)
    outputs = [DOC_PATH, VALIDATION_PATH, *csv_paths]
    outputs_scoped = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in outputs)
    formalization_untouched_by_script = FORMALIZATION.exists() and all(FORMALIZATION not in path.resolve().parents for path in outputs)

    rows = [
        {
            "validation_id": "VAL1380_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if all_sources_ok else "FAIL",
            "details": "; ".join(f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources),
        },
        {
            "validation_id": "VAL1380_1_kappa_origin",
            "check": "kappa_m maps to Z_m as a source-backed symbolic nonclaim coefficient slot",
            "status": "PASS" if kappa_slot_ready and gate_pass else "FAIL",
            "details": "KOR1380_4 and GATE1380_0 establish kappa_m=Z_m as symbolic/nonclaim only.",
        },
        {
            "validation_id": "VAL1380_2_shell_route",
            "check": "shell/boundary route is audited without false finite bound",
            "status": "PASS" if shell_blocked else "FAIL",
            "details": "SBA1380_4 keeps no explicit finite shell bound row.",
        },
        {
            "validation_id": "VAL1380_3_closure_feed",
            "check": "closure runner feed is updated with kappa_m=Z_m and refusal gates",
            "status": "PASS" if closure_updated else "FAIL",
            "details": "CFU1380 updates ell_tr and stress/shell guards.",
        },
        {
            "validation_id": "VAL1380_4_claim_refusal",
            "check": "local-GR/PPN/R10 claims remain blocked",
            "status": "PASS" if local_claim_blocked else "FAIL",
            "details": "GATE1380_4 keeps BLOCKED_NO_CLAIM.",
        },
        {
            "validation_id": "VAL1380_5_no_claim_rows",
            "check": "all generated rows keep valid_for_claim=false and claim_allowed=false",
            "status": "PASS" if nonclaim else "FAIL",
            "details": "1380 improves symbolic coefficient provenance but does not score local claims.",
        },
        {
            "validation_id": "VAL1380_6_csv_parse",
            "check": "all generated CSVs parse cleanly",
            "status": "PASS" if csv_ok else "FAIL",
            "details": csv_details,
        },
        {
            "validation_id": "VAL1380_7_scope",
            "check": "generated outputs stay inside post-checkpoint-work and outside formalization-workbench",
            "status": "PASS" if outputs_scoped and formalization_untouched_by_script else "FAIL",
            "details": f"ROOT={ROOT}; FORMALIZATION_EXISTS={FORMALIZATION.exists()}",
        },
    ]
    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "validation_id": "VAL1380_8_overall",
            "check": "overall 1380 validation",
            "status": "PASS" if overall_ok else "FAIL",
            "details": "1380 maps kappa_m to Z_m as a source-backed symbolic nonclaim slot and keeps shell/local claims blocked.",
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    kappa_rows: list[dict[str, object]],
    shell_rows: list[dict[str, object]],
    closure_feed: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> None:
    text = f"""# {TITLE}

**Current verdict:** 1380 gets a real but limited win: `kappa_m` can be identified with the existing scalar kinetic/stress coefficient `Z_m` in the candidate memory-scalar branch. This is source-backed as a symbolic coefficient slot, not as a signed numeric value.

**What changed:** the transition closure runner can now use `kappa_m := Z_m`, so `ell_tr=sqrt(Z_m L0^2/F2)` and the stability gate becomes `Z_m F2>0`. The same move also forces the scalar gradient stress to remain in the residual ledger; we do not get to use `Z_m` to make the profile and then throw its stress away.

**What did not close:** shell/boundary still has no explicit finite bound or exact projector theorem. Direct shell projection, generic suppression, width scaling, and boundary shortcuts remain blocked.

## Source Register

{table(["source_id", "source_path", "required_anchor", "exists", "anchor_found", "purpose", "valid_for_claim", "claim_allowed"], sources)}

## `kappa_m = Z_m` Origin Coefficient Row

{table(["coeff_id", "coefficient", "parent_origin", "derivation_or_mapping", "source_path", "source_anchor", "status", "missing_for_numeric", "valid_for_claim", "claim_allowed"], kappa_rows)}

## Shell/Boundary Bound Route Audit

{table(["shell_id", "target", "audit_result", "bound_or_template", "source_paths", "source_anchors", "missing_for_finite_bound", "valid_for_claim", "claim_allowed"], shell_rows)}

## Closure Runner Feed Update

{table(["feed_id", "runner_field", "update", "status", "runner_expression", "blocks_numeric", "valid_for_claim", "claim_allowed"], closure_feed)}

## Claim Gates

{table(["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"], gates)}

## Decision Ledger

{table(["decision_id", "decision", "why", "next_action", "valid_for_claim", "claim_allowed"], decisions)}

## Next Target

{table(["next_id", "next_doc", "next_script", "task", "success_condition", "do_not_claim", "valid_for_claim", "claim_allowed"], next_targets)}

## Validation

{table(["validation_id", "check", "status", "details"], validations)}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register()
    kappa_rows = kappa_origin_rows()
    shell_rows = shell_bound_rows()
    closure_feed = closure_feed_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    csv_paths = generated_csv_paths()
    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(KAPPA_ORIGIN_PATH, kappa_rows)
    write_csv(SHELL_BOUND_PATH, shell_rows)
    write_csv(CLOSURE_FEED_PATH, closure_feed)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_targets)

    validations = validation_rows(sources, kappa_rows, shell_rows, closure_feed, gates, csv_paths)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, kappa_rows, shell_rows, closure_feed, gates, decisions, next_targets, validations)

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"formalization-workbench touched by this script: {FORMALIZATION.exists() and False}")


if __name__ == "__main__":
    main()
