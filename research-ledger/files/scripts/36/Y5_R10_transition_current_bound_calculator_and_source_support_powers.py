from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

from Y5_R10_transition_current_bound_calculator import DEFAULT_OUTPUT, evaluate_file


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
SCRIPT_PATH = POST_CHECKPOINT / "scripts" / "Y5_R10_transition_current_bound_calculator.py"

OUTPUT_DOC = POST_CHECKPOINT / "799-Y5-R10-transition-current-bound-calculator-and-source-support-powers.md"
NEXT_TARGET = "800-Y5-R10-universal-XB-PiB-support-powers-or-Kperp-boundary-zero-lemma.md"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_799_SOURCE_REGISTER.csv"
FORMULA_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_799_TRANSITION_BOUND_FORMULA_REGISTER.csv"
SUPPORT_POWER_PATH = RESIDUALS / "P8_Y5_R10_799_SUPPORT_POWER_GATES.csv"
INPUT_TEMPLATE_PATH = RESIDUALS / "P8_Y5_R10_799_TRANSITION_CALCULATOR_INPUT_TEMPLATE.csv"
SMOKE_OUTPUT_PATH = DEFAULT_OUTPUT
CALCULATOR_POLICY_PATH = RESIDUALS / "P8_Y5_R10_799_CALCULATOR_POLICY.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_799_DERIVATION_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_799_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_799_VALIDATION.csv"

STATUS = "Y5_R10_799_transition_bound_calculator_built_support_powers_required_nonclaim"
CLAIM_CEILING = "calculator_and_support_power_contract_only_no_real_local_bound_pass_no_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    FORMULA_REGISTER_PATH,
    SUPPORT_POWER_PATH,
    INPUT_TEMPLATE_PATH,
    SMOKE_OUTPUT_PATH,
    CALCULATOR_POLICY_PATH,
    DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "798_doc",
        "path": POST_CHECKPOINT / "798-Y5-R10-Gammaeff-local-screening-source-law-or-response-kernel-bound.md",
        "needles": ["GSE798_4_screened_source_scaling", "D798_1_transition_current_selected"],
        "role": "immediate transition-current target",
    },
    {
        "source_id": "798_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_798_VALIDATION.csv",
        "needles": ["V798_6_support_scaling_law,pass", "V798_11_no_local_GR_claim,pass"],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "formal_eq_local_gate",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": ["epsilon_N = |c^2 Kbar_MTS,00| / |4 pi G rho|", "epsilon_q,space = L_sys |q^i| / |K_matter,00|"],
        "role": "local safety definitions",
    },
    {
        "source_id": "formal_eq_transition_formula",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": ["L_tr ~= 4 Delta_B L_B", "|nabla m| ~ M_tr/L_tr", "epsilon_q,tr ~"],
        "role": "older transition-current estimator",
    },
    {
        "source_id": "red_team_transition",
        "path": FORMALIZATION / "06-consistency-red-team.md",
        "needles": ["transition current is now the screening deal-breaker", "epsilon_N,tr ~= 1.37e-2", "do not let the programme say \"the switch screens locally\""],
        "role": "red-team warning and prior bad smoke result",
    },
    {
        "source_id": "spine_support_power_target",
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["derive the support powers `pS`, `pL`, and `pT`", "Pi_B gives the small local unscreened fraction U_B"],
        "role": "spine target for source-support powers",
    },
    {
        "source_id": "798_expansion_csv",
        "path": RESIDUALS / "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
        "needles": ["GSE798_4_screened_source_scaling", "GSE798_5_source_law_verdict"],
        "role": "machine-readable source expansion",
    },
    {
        "source_id": "798_transition_contract_csv",
        "path": RESIDUALS / "P8_Y5_R10_798_TRANSITION_CURRENT_BOUND_CONTRACT.csv",
        "needles": ["TCB798_1_pS_source_support", "TCB798_5_Kperp_boundary"],
        "role": "machine-readable transition-current contract",
    },
]


INPUT_FIELDS = [
    "case_id",
    "row_status",
    "U_B",
    "pS",
    "pL",
    "pT",
    "pB",
    "pK",
    "L_cg",
    "L_tr",
    "L_sys",
    "K_matter_00",
    "rho",
    "F2",
    "A_S",
    "A_L",
    "A_T",
    "A_B",
    "A_K",
    "b_mem",
    "c",
    "G",
    "epsilon_q_limit",
    "epsilon_N_limit",
    "valid_for_claim",
    "source_path",
    "notes",
]


def utc_stamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def needle_status(path: Path, needles: list[str]) -> str:
    if not path.exists():
        return "missing_file"
    text = read_text(path)
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return "missing_needles:" + ";".join(missing)
    return "pass"


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def parse_validation_clean(start: int = 665, end: int = 798) -> tuple[bool, str]:
    if not RESIDUALS.exists():
        return False, "residual directory missing"
    failures: list[str] = []
    found = 0
    for path in RESIDUALS.glob("P8_Y5_BRR545_*_VALIDATION.csv"):
        number_text = path.name.replace("P8_Y5_BRR545_", "").replace("_VALIDATION.csv", "")
        if not number_text.isdigit():
            continue
        number = int(number_text)
        if start <= number <= end:
            found += 1
            with path.open("r", encoding="utf-8", newline="") as handle:
                for row in csv.DictReader(handle):
                    if row.get("result") != "pass":
                        failures.append(f"{path.name}:{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures[:20])
    return found > 0, f"{found} prior validation files clean"


def formalization_change_count() -> int:
    if not FORMALIZATION.exists():
        return -1
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF)


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = spec["path"]
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": str(path),
                "exists": str(path.exists()).lower(),
                "needle_check": needle_status(path, spec["needles"]),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def formula_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "formula_id": "TBF799_0_source_amplitudes",
            "quantity": "source channels",
            "formula": "M_src=A_S U_B^pS; M_mL=A_L U_B^pL; T_trace=A_T U_B^pT; B_boundary=A_B U_B^pB; Kperp=A_K U_B^pK",
            "meaning": "parametrizes how the universal local unscreened fraction suppresses each dangerous channel",
            "required_input": "U_B,pS,pL,pT,pB,pK,A_S,A_L,A_T,A_B,A_K from parent X_B/Pi_B law",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "formula_id": "TBF799_1_q_gamma_quad",
            "quantity": "quadratic Gamma source",
            "formula": "q_gamma_quad = |F2| M_src^2/(L_cg^2 L_tr)",
            "meaning": "source term after F'(m_*)=0 makes the m-channel quadratic",
            "required_input": "F2,M_src,L_cg,L_tr",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "formula_id": "TBF799_2_linear_drift_sources",
            "quantity": "mL/trace/boundary drift",
            "formula": "q_mL=M_mL/(L_cg^2 L_tr); q_trace=T_trace/L_tr; q_boundary=B_boundary/(L_cg^2 L_tr)",
            "meaning": "linear drift terms that survive even if F1 is locked to zero",
            "required_input": "support powers pL,pT,pB and amplitudes A_L,A_T,A_B",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "formula_id": "TBF799_3_bmem_curvature",
            "quantity": "memory curvature/current term",
            "formula": "q_bmem=|b_mem| M_src^2/L_tr^3",
            "meaning": "older transition-current red-team term retained as a separate source",
            "required_input": "b_mem,M_src,L_tr",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "formula_id": "TBF799_4_epsilon_q",
            "quantity": "exchange-current safety",
            "formula": "epsilon_q = L_sys (q_gamma_quad+q_mL+q_trace+q_boundary+q_bmem)/|K_matter,00|",
            "meaning": "dimensionless local exchange/nonconservation residual",
            "required_input": "system length, matter curvature scale, all q-source terms, observational tolerance",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "formula_id": "TBF799_5_epsilon_N_trace",
            "quantity": "Newton/source safety",
            "formula": "epsilon_N_trace = c^2 K_trace_amp/(4 pi G rho)",
            "meaning": "Newton-source contamination from screened trace/baseline channels",
            "required_input": "rho,K_trace_amp,c,G,epsilon_N_limit",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "formula_id": "TBF799_6_Kperp_safety",
            "quantity": "transverse tensor safety",
            "formula": "Kperp_amp=A_K U_B^pK/L_cg^2; epsilon_N_Kperp=c^2 Kperp_amp/(4 pi G rho)",
            "meaning": "longitudinal screening does not control transverse/boundary tensor residue",
            "required_input": "Kperp zero theorem or pK,A_K bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def support_power_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "SPG799_0_U_B_profile",
            "power_or_quantity": "U_B",
            "derivation_needed": "derive U_B=1-Pi_B from one universal X_B/B_env law for local, galaxy, and FLRW regimes",
            "failure_mode": "dataset-specific projector or hand-picked local kill switch",
            "next_action": "source U_B profiles for lab/Solar/clock/orbital systems",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "SPG799_1_pS",
            "power_or_quantity": "pS",
            "derivation_needed": "prove local source support S_cg=O(U_B^pS)",
            "failure_mode": "quadratic F2 channel remains too large despite F1=0",
            "next_action": "derive from coarse-graining/source support theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "SPG799_2_pL",
            "power_or_quantity": "pL",
            "derivation_needed": "prove local stationary point drift grad m_L=O(U_B^pL/L_tr)",
            "failure_mode": "m_L(B_env) transition recreates a linear q_loc source",
            "next_action": "derive m_L(X_B) smoothness/flatness in local branch",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "SPG799_3_pT",
            "power_or_quantity": "pT",
            "derivation_needed": "prove grad(L_cg^-2 F_L)=O(U_B^pT/L_tr)",
            "failure_mode": "trace-baseline gradients act like local Lambda-gradient/fifth-force source",
            "next_action": "derive trace baseline from same memory dynamics as L_cg",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "SPG799_4_pB",
            "power_or_quantity": "pB",
            "derivation_needed": "prove boundary/source-measure residue is O(U_B^pB)",
            "failure_mode": "boundary terms dominate after bulk source is screened",
            "next_action": "derive boundary/source-measure silence theorem or local response bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "SPG799_5_pK",
            "power_or_quantity": "pK",
            "derivation_needed": "prove K_perp=0 or K_perp=O(U_B^pK/L_cg^2)",
            "failure_mode": "transverse tensor residue shifts PPN/Newton even when q_loc source is small",
            "next_action": "attempt Kperp boundary-zero lemma or retain response-vector bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def input_template_rows() -> list[dict[str, object]]:
    missing = {
        "case_id": "template_missing_parent_values",
        "row_status": "blocked_missing_parent_inputs",
        "valid_for_claim": "false",
        "source_path": "MISSING_PARENT_SOURCE_PATH",
        "notes": "claim rows require real sourced U_B,powers,amplitudes,lengths,and local bounds",
    }
    for field in INPUT_FIELDS:
        missing.setdefault(field, "MISSING_PARENT_INPUT")

    toy = {
        "case_id": "toy_strong_support_nonclaim",
        "row_status": "toy_nonclaim_schema_check",
        "U_B": "1e-5",
        "pS": "1",
        "pL": "2",
        "pT": "2",
        "pB": "2",
        "pK": "2",
        "L_cg": "1e13",
        "L_tr": "1e11",
        "L_sys": "1e11",
        "K_matter_00": "1e-24",
        "rho": "1000",
        "F2": "1",
        "A_S": "1",
        "A_L": "1",
        "A_T": "1e-36",
        "A_B": "1",
        "A_K": "1",
        "b_mem": "1",
        "c": "299792458",
        "G": "6.67430e-11",
        "epsilon_q_limit": "1e-5",
        "epsilon_N_limit": "1e-5",
        "valid_for_claim": "false",
        "source_path": "toy_nonclaim_no_physical_source",
        "notes": "illustrative calculator wiring only; not evidence",
    }
    return [missing, toy]


def policy_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "policy_id": "TCP799_0_no_claim_without_real_sources",
            "rule": "passes_symbolic_gate cannot become evidence unless valid_for_claim=true and every numeric input has a source path.",
            "reason": "toy support powers can make almost anything pass if not parent-derived",
            "status": "active",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "policy_id": "TCP799_1_compare_all_local_arenas",
            "rule": "epsilon_q, epsilon_N_trace, epsilon_N_Kperp, PPN, clocks, orbital, R10, and WEP/readout must all pass or be theorem-zero.",
            "reason": "Newton-source safety alone is not local GR",
            "status": "active",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "policy_id": "TCP799_2_universal_projector_only",
            "rule": "U_B and support powers must come from one universal X_B/Pi_B law, not separate local/galaxy/cosmology switches.",
            "reason": "prevents the screening branch becoming a patchwork quilt",
            "status": "active",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D799_0_calculator_built",
            "decision": "Build transition-current bound calculator?",
            "reason": "The local obstruction is now quantitative in U_B,pS,pL,pT,pB,pK,L_tr,L_cg and source amplitudes.",
            "result": "calculator_and_template_built_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D799_1_support_powers_primary",
            "decision": "What blocks a real pass?",
            "reason": "The template cannot be promoted until U_B and support powers are derived from the universal X_B/Pi_B branch.",
            "result": "derive_universal_support_powers_or_demote_to_closure",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D799_2_Kperp_retained",
            "decision": "Can Kperp be ignored?",
            "reason": "No. Kperp remains a separate transverse tensor channel after trace/longitudinal source screening.",
            "result": "Kperp_zero_boundary_or_response_bound_required",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "A runnable transition-current bound calculator now maps U_B support powers, transition width, source amplitudes, and Kperp residue into epsilon_q and Newton-source safety quantities.",
            "hard_blocker": "No local-GR claim: U_B,pS,pL,pT,pB,pK, source amplitudes, transition geometry, and response matrices remain parent-unsourced.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_outputs_scoped() -> bool:
    root = POST_CHECKPOINT.resolve()
    for path in OUTPUT_PATHS:
        resolved_parent = path.parent.resolve()
        if root != resolved_parent and root not in resolved_parent.parents:
            return False
    return True


def validation_rows(
    sources: list[dict[str, object]],
    formulas: list[dict[str, object]],
    powers: list[dict[str, object]],
    template: list[dict[str, object]],
    smoke: list[dict[str, object]],
    policies: list[dict[str, object]],
    decisions: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = parse_validation_clean()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in sources)
    all_nonclaim = all(
        row.get("valid_for_claim") == "false"
        for group in [sources, formulas, powers, template, smoke, policies, decisions, summary]
        for row in group
    )
    formula_ids = {row["formula_id"] for row in formulas}
    formula_complete = formula_ids == {
        "TBF799_0_source_amplitudes",
        "TBF799_1_q_gamma_quad",
        "TBF799_2_linear_drift_sources",
        "TBF799_3_bmem_curvature",
        "TBF799_4_epsilon_q",
        "TBF799_5_epsilon_N_trace",
        "TBF799_6_Kperp_safety",
    }
    power_ids = {row["gate_id"] for row in powers}
    powers_complete = power_ids == {
        "SPG799_0_U_B_profile",
        "SPG799_1_pS",
        "SPG799_2_pL",
        "SPG799_3_pT",
        "SPG799_4_pB",
        "SPG799_5_pK",
    }
    calculator_exists = SCRIPT_PATH.exists() and "q_gamma_quad" in read_text(SCRIPT_PATH) and "epsilon_q" in read_text(SCRIPT_PATH)
    template_has_missing = any(row["case_id"] == "template_missing_parent_values" and "MISSING_PARENT_INPUT" in str(row.values()) for row in template)
    smoke_has_missing_block = any(row["case_id"] == "template_missing_parent_values" and row["numeric_ready"] == "false" for row in smoke)
    smoke_has_numeric_nonclaim = any(row["case_id"] == "toy_strong_support_nonclaim" and row["numeric_ready"] == "true" and row["valid_for_claim"] == "false" for row in smoke)
    no_smoke_claim_pass = all(row["passes_symbolic_gate"] == "false" for row in smoke)
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D799_1_support_powers_primary" for row in decisions)
    formalization_count = formalization_change_count()

    checks = [
        ("V799_0_sources_exist_and_needles", source_ok, "all source paths exist and needles are present"),
        ("V799_1_prior_665_798_clean", prior_clean, prior_detail),
        ("V799_2_outputs_scoped", all_outputs_scoped(), str(POST_CHECKPOINT)),
        ("V799_3_all_rows_nonclaim", all_nonclaim, "all generated rows valid_for_claim=false"),
        ("V799_4_formula_register_complete", formula_complete, "transition formulas registered"),
        ("V799_5_support_power_gates_complete", powers_complete, "U_B,pS,pL,pT,pB,pK gates registered"),
        ("V799_6_calculator_script_present", calculator_exists, str(SCRIPT_PATH)),
        ("V799_7_template_blocks_claim", template_has_missing, "missing parent input template row present"),
        ("V799_8_smoke_missing_row_blocked", smoke_has_missing_block, "missing row remains blocked"),
        ("V799_9_smoke_numeric_nonclaim", smoke_has_numeric_nonclaim, "toy numeric row evaluated as nonclaim"),
        ("V799_10_no_smoke_claim_pass", no_smoke_claim_pass, "no smoke row is promoted to claim"),
        ("V799_11_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V799_12_no_local_GR_claim", all_nonclaim and no_smoke_claim_pass, "local GR/Newton remains blocked"),
        ("V799_13_claim_artifacts_absent", not (POST_CHECKPOINT / "LOCAL_GR_CLAIM.md").exists(), "no local-GR claim artifact present"),
        ("V799_14_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V799_15_validation_rows_ready", True, "validation table constructed"),
    ]
    return [{"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail} for check_id, passed, detail in checks]


def build_doc(
    sources: list[dict[str, object]],
    formulas: list[dict[str, object]],
    powers: list[dict[str, object]],
    template: list[dict[str, object]],
    smoke: list[dict[str, object]],
    policies: list[dict[str, object]],
    decisions: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 799 - Y5 R10 Transition Current Bound Calculator And Source Support Powers

Current result: **the transition-current obstruction is now calculator-ready, but not passed**. The source expansion from 798 is encoded as explicit bound formulas for `epsilon_q`, trace/Newton contamination, and `K_perp` residue. The smoke run proves the schema works and keeps all rows non-claim. A real pass still needs parent-sourced `U_B`, support powers `pS,pL,pT,pB,pK`, transition geometry, source amplitudes, and response matrices.

## Nonclaim Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Transition Bound Formula Register

{markdown_table(formulas, ["formula_id", "quantity", "formula", "meaning", "required_input", "valid_for_claim"])}

## Support Power Gates

{markdown_table(powers, ["gate_id", "power_or_quantity", "derivation_needed", "failure_mode", "next_action", "valid_for_claim"])}

## Calculator Policy

{markdown_table(policies, ["policy_id", "rule", "reason", "status", "valid_for_claim"])}

## Calculator Input Template Preview

{markdown_table(template, ["case_id", "row_status", "U_B", "pS", "pL", "pT", "pB", "pK", "valid_for_claim", "notes"])}

## Smoke Output

{markdown_table(smoke, ["case_id", "row_status", "numeric_ready", "epsilon_q", "epsilon_N_trace", "epsilon_N_Kperp", "passes_symbolic_gate", "valid_for_claim", "notes"])}

## Decision

{markdown_table(decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This is a useful engineering step: the local transition problem is no longer only qualitative. But the calculator cannot be used as evidence until the inputs come from the parent theory. The next theorem target is therefore the universal `X_B -> Pi_B` support-power derivation, with `K_perp` boundary-zero or response-bound running alongside it.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    formulas = formula_rows(generated_utc)
    powers = support_power_rows(generated_utc)
    template = input_template_rows()
    write_csv(INPUT_TEMPLATE_PATH, template, INPUT_FIELDS)
    smoke = evaluate_file(INPUT_TEMPLATE_PATH, SMOKE_OUTPUT_PATH)
    policies = policy_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, formulas, powers, template, smoke, policies, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(FORMULA_REGISTER_PATH, formulas, ["formula_id", "quantity", "formula", "meaning", "required_input", "valid_for_claim", "generated_utc"])
    write_csv(SUPPORT_POWER_PATH, powers, ["gate_id", "power_or_quantity", "derivation_needed", "failure_mode", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(CALCULATOR_POLICY_PATH, policies, ["policy_id", "rule", "reason", "status", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, formulas, powers, template, smoke, policies, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"799 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
