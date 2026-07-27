from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "989-Y5-R10-EM-lock-signature-input-or-alpha-source-normalization-owner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def md_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "988_doc",
            "path": "988-Y5-R10-alphaEM-WEP-clock-joint-prior-or-EM-lock-theorem.md",
            "role": "immediate handoff selecting EM-lock/source-normalization owner",
            "needle": "DEC988_3_best_next",
        },
        {
            "source_id": "988_em_lock_gate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_988_EM_LOCK_THEOREM_GATE.csv",
            "role": "EM-lock clauses to audit",
            "needle": "EMLOCK988_5_theorem_verdict",
        },
        {
            "source_id": "988_WEP_pressure",
            "path": "source-intake/mts_residuals/P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv",
            "role": "beta_source_alpha pressure target",
            "needle": "WEP988_WAS651_0_alpha_Coulomb",
        },
        {
            "source_id": "988_normalization",
            "path": "source-intake/mts_residuals/P8_Y5_R10_988_NORMALIZATION_GATES.csv",
            "role": "normalization quarantine and beta_source distinction",
            "needle": "NORM988_2_beta_source_not_screen",
        },
        {
            "source_id": "765_doc",
            "path": "765-Y5-R10-parent-vertical-generator-norm-and-Maxwell-kinetic-inheritance-or-alpha-source-fill.md",
            "role": "vertical-generator norm theorem and counterexamples",
            "needle": "VGN765_5_alpha_zero_conditional",
        },
        {
            "source_id": "765_MKI",
            "path": "source-intake/mts_residuals/P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv",
            "role": "Maxwell kinetic inheritance gate",
            "needle": "MKI765_2_unique_F2",
        },
        {
            "source_id": "765_counterexamples",
            "path": "source-intake/mts_residuals/P8_Y5_R10_765_RESCALING_COUNTEREXAMPLE_LEDGER.csv",
            "role": "legal counterexamples while parent signatures are unsigned",
            "needle": "RCE765_0_lambda_F2",
        },
        {
            "source_id": "767_doc",
            "path": "767-Y5-R10-parent-matter-functor-no-alpha-vertex-or-WEP-closure.md",
            "role": "no-alpha vertex and matter functor remain unsigned",
            "needle": "PMR767_3_no_alpha_mass_vertex",
        },
        {
            "source_id": "767_source_fill",
            "path": "source-intake/mts_residuals/P8_Y5_R10_767_SOURCE_FILL_SCHEMA.csv",
            "role": "source-fill schemas for no-alpha and beta_source branches",
            "needle": "SFS767_3_beta_source_alpha",
        },
        {
            "source_id": "651_WEP_stress",
            "path": "source-intake/mts_residuals/P8_Y5_R10_651_WEP_ALPHA_STRESS_TEST.csv",
            "role": "MICROSCOPE pressure and beta targets",
            "needle": "WAS651_1_surface_binding",
        },
    ]
    rows: list[dict[str, str]] = []
    for spec in specs:
        path = source_path(spec["path"])
        text = read_text(path)
        rows.append(
            {
                "source_id": spec["source_id"],
                "role": spec["role"],
                "path": spec["path"],
                "exists": flag(path.exists()),
                "needle_found": flag(spec["needle"] in text),
                "needle": spec["needle"],
                "valid_for_claim": "false",
            }
        )
    return rows


def EM_lock_signature_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "ELA989_0_TQ_owner",
            "clause": "parent charge generator owner",
            "required_parent_signature": "T_Q is a compact vertical generator in the varied parent action with fixed lattice/norm data",
            "contract_form": "A_Q=A^Q T_Q, exp(2*pi*T_Q)=1, Lie_v <T_Q,T_Q>_P=0",
            "current_evidence": "765 gives the exact theorem shape but says T_Q is not supplied as a parent-action object",
            "verdict": "unsigned",
            "blocks": "charge unit and A_Q normalization can be rescaled",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "ELA989_1_unique_F2",
            "clause": "unique Maxwell kinetic term",
            "required_parent_signature": "observed F_Q^2 is only the T_Q subblock of one parent curvature norm",
            "contract_form": "S_EM=-(C_P/4) int mu_obs <F,F>_P; g_EM^-2=C_P <T_Q,T_Q>_P; no DeltaS=-(lambda_A/4) int F_Q^2",
            "current_evidence": "765 explicitly retains lambda_A F_Q^2 as a legal counterexample",
            "verdict": "fails_current_corpus",
            "blocks": "alpha_EM can remain a free or branch-dependent coefficient",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "ELA989_2_current_owner",
            "clause": "charge-current/source normalization owner",
            "required_parent_signature": "matter current, charge labels, and Maxwell source normalization descend from the same T_Q Noether owner",
            "contract_form": "S_int=sum_A n_A int A_Q J_A with n_A representation/lattice data and Lie_v n_A=0",
            "current_evidence": "765 retains current rescaling and 988 keeps beta_source_alpha as unowned",
            "verdict": "unsigned",
            "blocks": "WEP/R10 source-test strength can float independently of clock alpha drift",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "ELA989_3_readout_descent",
            "clause": "dimensionless alpha readout descent",
            "required_parent_signature": "Hodge star, coframe, and hbar*c readout are quotient-fixed for alpha_EM",
            "contract_form": "Lie_v ln alpha_EM = -Lie_v ln(g_EM^-2) - Lie_v ln(hbar*c/readout factors) = 0",
            "current_evidence": "765 retains coframe/Hodge/readout leakage as possible",
            "verdict": "unsigned",
            "blocks": "clock/spectroscopy alpha channel can re-enter through units or observed coframe",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "ELA989_4_no_alpha_vertex",
            "clause": "matter functor no-alpha/no-mass vertex",
            "required_parent_signature": "S_matter descends through one observed matter functor and has no alpha_EM(chi_X), f_A(chi_X)F^2, m_A(chi_X), or binding-response vertex",
            "contract_form": "delta S_matter/dchi_X|ehat,theta_A=0 and Lie_v theta_A=0",
            "current_evidence": "767 re-audit says no-alpha/mass vertex remains explicit closure, not theorem",
            "verdict": "unsigned",
            "blocks": "composition-dependent Coulomb and mass/binding channels remain physical fallback rows",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "ELA989_5_total",
            "clause": "EM-lock theorem promotion",
            "required_parent_signature": "ELA989_0 through ELA989_4 all signed by parent action or exact quotient theorem",
            "contract_form": "then b_theta_alpha_EM=0, C_C=0 locally, and clock/WEP alpha channels close structurally",
            "current_evidence": "multiple clauses unsigned and one unique-F2 clause fails current corpus",
            "verdict": "not_promoted",
            "blocks": "no clock/WEP/btheta/local-GR claim",
            "valid_for_claim": "false",
        },
    ]


def parent_input_candidate_rows() -> list[dict[str, str]]:
    return [
        {
            "input_id": "PIC989_0_parent_charge_generator",
            "needed_for": "ELA989_0_TQ_owner",
            "required_columns_or_objects": "generator_id,parent_bundle,compact_lattice,norm_owner,norm_value_or_symbol,source_path,valid_for_claim",
            "minimum_parent_action_clause": "parent action names T_Q and fixes its normalization independently of matter representation choices",
            "current_status": "candidate_missing",
            "if_missing": "generator/current rescaling remains legal",
            "valid_for_claim": "false",
        },
        {
            "input_id": "PIC989_1_unique_Maxwell_subblock",
            "needed_for": "ELA989_1_unique_F2",
            "required_columns_or_objects": "curvature_norm_owner,FQ_subblock,coefficient_owner,independent_F2_forbidden_by,source_path,valid_for_claim",
            "minimum_parent_action_clause": "only one curvature norm produces F_Q^2; all standalone lambda_A F_Q^2 terms are forbidden by symmetry/domain",
            "current_status": "candidate_missing_and_counterexample_active",
            "if_missing": "alpha_EM normalization remains unowned",
            "valid_for_claim": "false",
        },
        {
            "input_id": "PIC989_2_Noether_current_owner",
            "needed_for": "ELA989_2_current_owner",
            "required_columns_or_objects": "current_id,Noether_owner,charge_unit_owner,matter_coupling_owner,source_normalization_owner,source_path,valid_for_claim",
            "minimum_parent_action_clause": "the same T_Q fixes charge labels, A_Q coupling, and source/test normalization",
            "current_status": "candidate_missing",
            "if_missing": "beta_source_alpha remains a free finite-branch debt",
            "valid_for_claim": "false",
        },
        {
            "input_id": "PIC989_3_dimensionless_readout",
            "needed_for": "ELA989_3_readout_descent",
            "required_columns_or_objects": "readout_id,Hodge_owner,coframe_owner,hbar_c_status,vertical_derivative,source_path,valid_for_claim",
            "minimum_parent_action_clause": "dimensionless alpha readout is quotient-fixed and local coframe silent",
            "current_status": "candidate_missing",
            "if_missing": "clock/fine-structure drift can re-enter",
            "valid_for_claim": "false",
        },
        {
            "input_id": "PIC989_4_no_alpha_vertex",
            "needed_for": "ELA989_4_no_alpha_vertex",
            "required_columns_or_objects": "operator,forbidden_by,vertical_derivative,matter_functor_owner,source_path,valid_for_claim",
            "minimum_parent_action_clause": "ordinary representation constants are internal data and have zero vertical derivative",
            "current_status": "candidate_missing",
            "if_missing": "Damour-Donoghue composition charges remain active fallback inputs",
            "valid_for_claim": "false",
        },
    ]


def beta_source_owner_rows() -> list[dict[str, str]]:
    pressure_rows = read_csv_rows(OUT / "P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv")
    pressure_by_id = {row.get("import_id", ""): row for row in pressure_rows}
    alpha = pressure_by_id.get("WEP988_WAS651_0_alpha_Coulomb", {})
    surface = pressure_by_id.get("WEP988_WAS651_1_surface_binding", {})
    return [
        {
            "owner_id": "BSO989_0_definition",
            "quantity": "beta_source_alpha",
            "role": "source/force normalization multiplying the finite alpha WEP channel",
            "formula_context": "eta_AB_alpha = DeltaQ_alpha_AB * beta_source_alpha * b_alpha * tau_WEP",
            "owner_needed": "parent source functional or Noether current normalization that fixes local source/test coupling strength",
            "current_status": "unowned",
            "target_or_bound": "must be zero by EM-lock/no-alpha theorem or numerically below WEP target",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "BSO989_1_alpha_only_target",
            "quantity": "beta_source_alpha_max_alpha_only",
            "role": "finite alpha survival target using 651 alpha/Coulomb smoke channel",
            "formula_context": f"eta_bound / unit_source_eta_prediction = {alpha.get('required_abs_beta_source_max', 'MISSING')}",
            "owner_needed": "derived source normalization suppression for alpha/Coulomb channel",
            "current_status": "numeric_target_only_not_derived",
            "target_or_bound": alpha.get("required_abs_beta_source_max", "MISSING"),
            "valid_for_claim": "false",
        },
        {
            "owner_id": "BSO989_2_robust_surface_including_target",
            "quantity": "beta_source_alpha_max_robust",
            "role": "more conservative finite-branch target if surface/binding channel is retained",
            "formula_context": f"eta_bound / unit_source_eta_prediction = {surface.get('required_abs_beta_source_max', 'MISSING')}",
            "owner_needed": "derived suppression that also covers surface/binding composition response",
            "current_status": "numeric_target_only_not_derived",
            "target_or_bound": surface.get("required_abs_beta_source_max", "MISSING"),
            "valid_for_claim": "false",
        },
        {
            "owner_id": "BSO989_3_not_clock_screen",
            "quantity": "beta_source_alpha vs S_lab_alpha",
            "role": "prevents fake escape by confusing time-drift screening with force-source normalization",
            "formula_context": "clock product controls b_alpha*tau_clock; WEP force uses beta_source_alpha*b_alpha*tau_WEP",
            "owner_needed": "separate parent map relating tau_clock, tau_WEP, and source normalization if they are to be identified",
            "current_status": "separate_debt",
            "target_or_bound": "cannot set beta_source_alpha=S_lab_alpha without a parent theorem",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "BSO989_4_failure_action",
            "quantity": "finite alpha branch",
            "role": "decision if no EM-lock or source-normalization owner appears",
            "formula_context": "finite alpha remains closure-only/nonclaim",
            "owner_needed": "either EM-lock theorem-zero or source-backed beta_source/tau map",
            "current_status": "closure_only_if_unowned",
            "target_or_bound": "no WEP/clock/local-GR promotion",
            "valid_for_claim": "false",
        },
    ]


def route_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC989_0_EM_lock_attempt",
            "route": "derive theorem-zero",
            "result": "not_signed",
            "reason": "unique Maxwell F2 fails current corpus and other required signatures are unsigned",
            "next_action": "do not claim b_theta_alpha_EM=0",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC989_1_finite_branch",
            "route": "finite beta_source_alpha suppression",
            "result": "allowed_only_as_debt",
            "reason": "numeric target exists but source-normalization owner is missing",
            "next_action": "treat beta_source_alpha as an explicit parent-action input requirement",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC989_2_project_position",
            "route": "coupling sector status",
            "result": "coupling_bottleneck_is_now_exactly_localized",
            "reason": "the missing object is not generic coupling; it is T_Q/F2/current/readout/no-alpha ownership or beta_source_alpha source normalization",
            "next_action": "fold this into a minimal parent action coupling contract",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC989_3_best_next",
            "route": "next checkpoint",
            "result": "990-Y5-R10-minimal-parent-action-coupling-contract-EM-matter-GR-reentry.md",
            "reason": "the next useful step is writing the parent-action clauses that must be true before local GR/Newton reentry can honestly proceed",
            "next_action": "build a minimal parent action coupling contract tying EM-lock, matter functor, source normalization, and EH/PPN reentry gates",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG989_0_EM_lock_zero",
            "claim": "b_theta_alpha_EM=0 is proved",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "EM-lock signatures are not parent-signed and unique F2 currently fails",
        },
        {
            "gate_id": "CG989_1_beta_source_bound",
            "claim": "beta_source_alpha is below MICROSCOPE target",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "only numeric targets exist; no parent source-normalization owner exists",
        },
        {
            "gate_id": "CG989_2_clock_or_WEP_pass",
            "claim": "clock or WEP alpha channel passes",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "clock product and WEP force source remain separate unowned maps",
        },
        {
            "gate_id": "CG989_3_local_GR",
            "claim": "local GR/Newton/PPN follows from alpha sector",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "alpha-sector discipline is necessary but not sufficient for EH/PPN reduction",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "990-Y5-R10-minimal-parent-action-coupling-contract-EM-matter-GR-reentry.md",
            "objective": "write the minimal parent-action coupling contract that would make EM-lock, matter functor, source normalization, and local GR/Newton reentry derivable instead of closure-only",
            "include": "T_Q/F2/current/readout clauses, no-alpha/no-mass matter functor, beta_source fallback, EH/PPN reentry dependencies, claim gates",
            "exclude": "WEP pass, clock pass, local-GR claim, invented numeric beta_source, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
        }
    ]


def is_positive_number(value: str) -> bool:
    try:
        return float(value) > 0.0
    except (TypeError, ValueError):
        return False


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_timestamp = SCRIPT_START_UTC.timestamp()
    for dirpath, _, filenames in os.walk(FORMALIZATION):
        for filename in filenames:
            path = Path(dirpath) / filename
            try:
                if path.stat().st_mtime > start_timestamp:
                    count += 1
            except OSError:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, str]],
    EM_lock_audit: list[dict[str, str]],
    parent_inputs: list[dict[str, str]],
    beta_source: list[dict[str, str]],
    decisions: list[dict[str, str]],
    claims: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    EM_lock_ok = any(row["audit_id"] == "ELA989_5_total" and row["verdict"] == "not_promoted" for row in EM_lock_audit)
    unique_F2_fail_ok = any(row["audit_id"] == "ELA989_1_unique_F2" and row["verdict"] == "fails_current_corpus" for row in EM_lock_audit)
    parent_inputs_ok = all(row["valid_for_claim"] == "false" and "candidate_missing" in row["current_status"] for row in parent_inputs)
    beta_alpha_ok = any(row["owner_id"] == "BSO989_1_alpha_only_target" and is_positive_number(row["target_or_bound"]) for row in beta_source)
    beta_robust_ok = any(row["owner_id"] == "BSO989_2_robust_surface_including_target" and is_positive_number(row["target_or_bound"]) for row in beta_source)
    decision_ok = any(row["decision_id"] == "DEC989_3_best_next" and "990-Y5-R10" in row["result"] for row in decisions)
    claims_ok = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claims)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V989_0_sources", "result": "pass" if sources_ok else "fail", "detail": "all local source files exist and needles are found"},
        {"check_id": "V989_1_EM_lock_not_promoted", "result": "pass" if EM_lock_ok else "fail", "detail": "EM-lock theorem remains conditional/nonclaim"},
        {"check_id": "V989_2_unique_F2_counterexample", "result": "pass" if unique_F2_fail_ok else "fail", "detail": "lambda_F2 counterexample keeps unique F2 unsigned"},
        {"check_id": "V989_3_parent_inputs_not_faked", "result": "pass" if parent_inputs_ok else "fail", "detail": "parent input rows remain candidate-missing nonclaims"},
        {"check_id": "V989_4_beta_alpha_target", "result": "pass" if beta_alpha_ok else "fail", "detail": "alpha-only beta_source numeric target imported"},
        {"check_id": "V989_5_beta_robust_target", "result": "pass" if beta_robust_ok else "fail", "detail": "surface-including robust beta_source numeric target imported"},
        {"check_id": "V989_6_claim_gates_safe", "result": "pass" if claims_ok else "fail", "detail": "EM-lock/beta/clock/WEP/local-GR claims remain blocked"},
        {"check_id": "V989_7_next_decision", "result": "pass" if decision_ok else "fail", "detail": "990 parent-action coupling contract target selected"},
        {"check_id": "V989_8_next_target_written", "result": "pass" if next_ok else "fail", "detail": "next target row is present and nonclaim"},
        {"check_id": "V989_9_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    return [
        {**row, "generated_utc": stamp()}
        for row in checks
    ] + [
        {
            "check_id": "V989_READY",
            "result": "pass" if ready else "fail",
            "detail": "989 checkpoint pack validation summary",
            "generated_utc": stamp(),
        }
    ]


def write_doc(
    sources: list[dict[str, str]],
    EM_lock_audit: list[dict[str, str]],
    parent_inputs: list[dict[str, str]],
    beta_source: list[dict[str, str]],
    decisions: list[dict[str, str]],
    claims: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    lines = [
        "# 989 Y5 R10: EM-Lock Signature Input Or Alpha Source-Normalization Owner",
        "",
        "Status: `Y5_R10_989_EM_lock_signature_audit_fails_to_promote_unique_F2_counterexample_active_beta_source_owner_debt_exact_nonclaim`",
        "",
        "Claim ceiling: no EM-lock zero, no `b_theta_alpha_EM` bound, no WEP pass, no clock pass, no local-GR/Newton claim.",
        "",
        "## Readout",
        "",
        "989 tried the clean route first. The EM-lock theorem is still the right shape: if the parent owns `T_Q`, unique `F_Q^2`, charge/current normalization, dimensionless readout descent, and no-alpha matter vertices, then the local alpha channel closes exactly.",
        "",
        "But the present corpus does not sign it. The decisive current blocker is the allowed independent `lambda_A F_Q^2` term, with current/readout/no-alpha clauses also unsigned. Therefore the finite branch is not evidence; it becomes an explicit source-normalization debt: `beta_source_alpha` must be parent-owned, zero, or below the MICROSCOPE pressure targets.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "role", "exists", "needle_found", "path"]),
        "",
        "## EM-Lock Signature Audit",
        "",
        md_table(EM_lock_audit, ["audit_id", "clause", "required_parent_signature", "contract_form", "current_evidence", "verdict", "blocks", "valid_for_claim"]),
        "",
        "## Parent Input Candidate Ledger",
        "",
        md_table(parent_inputs, ["input_id", "needed_for", "required_columns_or_objects", "minimum_parent_action_clause", "current_status", "if_missing", "valid_for_claim"]),
        "",
        "## Beta Source Owner Ledger",
        "",
        md_table(beta_source, ["owner_id", "quantity", "role", "formula_context", "owner_needed", "current_status", "target_or_bound", "valid_for_claim"]),
        "",
        "## Route Decisions",
        "",
        md_table(decisions, ["decision_id", "route", "result", "reason", "next_action", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(claims, ["gate_id", "claim", "gate_pass", "claim_allowed", "why_not"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["check_id", "result", "detail", "generated_utc"]),
        "",
        "## Next Target",
        "",
        md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register()
    EM_lock_audit = EM_lock_signature_audit_rows()
    parent_inputs = parent_input_candidate_rows()
    beta_source = beta_source_owner_rows()
    decisions = route_decision_rows()
    claims = claim_gate_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, EM_lock_audit, parent_inputs, beta_source, decisions, claims, next_target)

    write_csv(OUT / "P8_Y5_R10_989_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv", EM_lock_audit)
    write_csv(OUT / "P8_Y5_R10_989_PARENT_INPUT_CANDIDATE_LEDGER.csv", parent_inputs)
    write_csv(OUT / "P8_Y5_R10_989_BETA_SOURCE_OWNER_LEDGER.csv", beta_source)
    write_csv(OUT / "P8_Y5_R10_989_ROUTE_DECISION_MATRIX.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_989_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_989_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_989_VALIDATION.csv", validation)
    write_doc(sources, EM_lock_audit, parent_inputs, beta_source, decisions, claims, validation, next_target)


if __name__ == "__main__":
    main()
