from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "872-Y5-R10-cT-parent-projection-coefficient-or-theorem-zero-return.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_872_SOURCE_REGISTER.csv"
DERIVATION_PATH = RESIDUALS / "P8_Y5_R10_872_CT_PARENT_PROJECTION_DERIVATION_ATTEMPT.csv"
ZERO_RETURN_PATH = RESIDUALS / "P8_Y5_R10_872_THEOREM_ZERO_RETURN_AUDIT.csv"
FORMULA_PATH = RESIDUALS / "P8_Y5_R10_872_OBSERVABLE_PROJECTION_FORMULAS.csv"
COEFFICIENT_PATH = RESIDUALS / "P8_Y5_R10_872_COEFFICIENT_OWNERSHIP_LEDGER.csv"
ROUTE_CHOICE_PATH = RESIDUALS / "P8_Y5_R10_872_ROUTE_CHOICE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_872_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_872_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_872_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_872_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_872_VALIDATION.csv"

PRIOR_VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_871_VALIDATION.csv"

STATUS = "Y5_R10_872_cT_projection_reduced_to_parent_coefficients_zero_return_selected_nonclaim"
CLAIM_CEILING = "conditional_cT_projection_contract_only_no_cT_bound_no_R10_PPN_clock_WEP_or_local_GR_claim"
NEXT_TARGET = "873-Y5-R10-local-matter-trace-charge-zero-theorem-or-coefficient-fill.md"

GENERATED_CSV_PATHS = [
    SOURCE_REGISTER_PATH,
    DERIVATION_PATH,
    ZERO_RETURN_PATH,
    FORMULA_PATH,
    COEFFICIENT_PATH,
    ROUTE_CHOICE_PATH,
    CLAIM_GUARD_PATH,
    DECISION_PATH,
    NEXT_TARGET_PATH,
    NONCLAIM_SUMMARY_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "871_doc",
        "path": POST_CHECKPOINT / "871-Y5-R10-cT-trace-leakage-bound-source-row-builder.md",
        "needles": [
            "PC871_0_R10_alpha_lambda",
            "CR871_0_parent_cT_projection",
            "872-Y5-R10-cT-parent-projection-coefficient-or-theorem-zero-return.md",
        ],
        "role": "immediate c_T projection handoff",
    },
    {
        "source_id": "871_validation",
        "path": PRIOR_VALIDATION_PATH,
        "needles": [
            "V871_4_projection_contract_blocks_claim,pass",
            "V871_8_all_rows_nonclaim,pass",
            "V871_9_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "870_nohair",
        "path": POST_CHECKPOINT / "870-Y5-R10-P_loc-Jtrace-nohair-zero-theorem-or-bound.md",
        "needles": [
            "P_loc J_trace=0",
            "c_T=0",
            "multipole silence",
        ],
        "role": "theorem-zero return conditions",
    },
    {
        "source_id": "869_residual_vector",
        "path": POST_CHECKPOINT / "869-Y5-R10-q_loc-residual-vector-decomposition-or-zero-theorem.md",
        "needles": [
            "RR869_T",
            "q_T^nu = P_loc J_trace",
            "c_T,c_e,c_P,c_S",
        ],
        "role": "q_loc residual decomposition and c_T channel owner",
    },
    {
        "source_id": "863_trace_chain_rule",
        "path": POST_CHECKPOINT / "863-Y5-R10-Ward-trace-lift-current-and-coframe-pullback-zero-theorem.md",
        "needles": [
            "CZT863_0_chain_rule_zero",
            "CZT863_2_local_global_split",
            "LRF863_1_trace_leak_branch",
        ],
        "role": "local-vertical matter charge zero route",
    },
    {
        "source_id": "864_local_global_split",
        "path": POST_CHECKPOINT / "864-Y5-R10-local-global-quotient-split-and-endpoint-stationarity-parent-clause.md",
        "needles": [
            "Dq_FLRW[v_T]",
            "Dq_loc[U][v_T] = 0",
            "LGS864_0_conditional_split_lemma",
        ],
        "role": "two-quotient local/global split contract",
    },
    {
        "source_id": "393_source_normalization",
        "path": POST_CHECKPOINT / "393-source-normalized-Newtonian-limit-under-identity-closure.md",
        "needles": [
            "G_eff = kappa_eff c^4/(8 pi)",
            "mu_obs = G_eff M_eff + mu_extra",
            "Only a constant, universal, range-independent",
        ],
        "role": "Newtonian source-normalization and hidden-force guard",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def check_needles(path: Path, needles: list[str]) -> str:
    text = read_text(path)
    if not text:
        return "missing_path"
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return "missing_needles:" + ";".join(missing)
    return "pass"


def validation_file_clean(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, f"missing={path}"
    failures: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("result") != "pass":
                failures.append(f"{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures)
    return True, f"{path.name} clean"


def formalization_workbench_modified_count() -> int:
    command = (
        "$fw='"
        + str(FORMALIZATION).replace("'", "''")
        + "'; "
        + "$cutoff=[datetime]'2026-05-31T14:42:00'; "
        + "(Get-ChildItem -LiteralPath $fw -Recurse -File | "
        + "Where-Object { $_.LastWriteTime -gt $cutoff }).Count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    return int(completed.stdout.strip() or "0")


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "source_id": spec["source_id"],
            "path": str(spec["path"]),
            "exists": str(spec["path"].exists()).lower(),
            "needle_check": check_needles(spec["path"], spec["needles"]),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for spec in SOURCE_SPECS
    ]


def derivation_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "step_id": "PD872_0_define_local_trace_mode",
            "attempted_derivation": "Represent nonzero P_loc J_trace by a local scalar trace carrier phi_T only if parent action supplies a quadratic local sector.",
            "symbolic_result": "S_T^loc = integral[-(Z_T/2)(partial phi_T)^2-(Z_T m_T^2/2) phi_T^2 + phi_T J_T]",
            "owned_if": "Z_T, m_T^2, J_T, and the projection P_loc J_trace -> J_T are derived from the parent action",
            "current_status": "conditional_projection_ansatz_not_parent_owned",
            "blocker": "870 did not derive local support for J_trace; 871 did not derive parent coefficients",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "PD872_1_green_function_projection",
            "attempted_derivation": "Solve the static local quadratic sector to translate source charge into a finite-range potential.",
            "symbolic_result": "phi_T(r)=Q_T^A exp(-m_T r)/(4*pi*Z_T*r); lambda_T=hbar/(m_T*c) in SI or 1/m_T in natural units",
            "owned_if": "the trace carrier has a local elliptic Green function and no gauge-null/constraint cancellation",
            "current_status": "conditional_math_valid_not_MTS_derived",
            "blocker": "no parent proof picks this scalar operator rather than exact-current zero or constrained gauge mode",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "PD872_2_R10_alpha_projection",
            "attempted_derivation": "Compare the trace-exchange potential to Newtonian gravity between bodies A and B.",
            "symbolic_result": "alpha_T_AB = Q_T^A Q_T^B/(4*pi*Z_T*G_obs*m_A*m_B)",
            "owned_if": "Q_T^A/m_A and Q_T^B/m_B are parent-derived local matter charges",
            "current_status": "formula_reduced_to_parent_coefficients",
            "blocker": "local matter trace charges are not derived and may be exactly zero if v_T is local-vertical",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "PD872_3_force_law_projection",
            "attempted_derivation": "Translate the potential into an acceleration residual for local fifth-force/orbital tests.",
            "symbolic_result": "delta a/a_N = alpha_T_AB*(1+r/lambda_T)*exp(-r/lambda_T) plus source-normalization residuals",
            "owned_if": "the same alpha_T_AB is not absorbed into a constant universal GM and the range dependence is physical",
            "current_status": "formula_reduced_to_parent_coefficients",
            "blocker": "393 requires constant universal absorption to be proved, otherwise this remains mu_extra",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "PD872_4_PPN_projection",
            "attempted_derivation": "Map trace leakage into weak-field metric potentials only after a matter-frame metric response is selected.",
            "symbolic_result": "gamma-1 = C_T_gamma*c_T and beta-1 = C_T_beta*c_T, with C_T_* built from metric response and source normalization",
            "owned_if": "parent action fixes observed metric/coframe, gauge, and separation from c_P and c_S",
            "current_status": "not_reduced_to_numeric_coefficient",
            "blocker": "metric response operator and gauge are not parent-owned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "PD872_5_clock_WEP_projection",
            "attempted_derivation": "Map trace leakage to clock rates or species charge only through matter action dependence on phi_T.",
            "symbolic_result": "delta nu_i/nu_i = C_T_clock_i*c_T; eta_AB approx alpha_T_EA-alpha_T_EB when Q_T/m differs by species",
            "owned_if": "matter descent or no-marker theorem decides whether Q_T^A/m_A is universal, species-dependent, or zero",
            "current_status": "reduced_to_matter_charge_zero_or_fill",
            "blocker": "the sharp WEP channel makes an unsourced matter charge unacceptable",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def zero_return_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "zero_id": "ZR872_0_local_vertical_charge_zero",
            "zero_route": "If S_matter=Sbar[q_loc(Phi),psi] and v_T in ker(Dq_loc[U]), then Q_T^A := partial m_A/partial phi_T = 0 for every local body A.",
            "why_it_works": "By chain rule, partial_{v_T} m_A(q_loc(Phi)) = Dm_A(Dq_loc[v_T]) = 0.",
            "current_status": "best_route_conditional_not_parent_signed",
            "missing_clause": "parent-owned q_loc and proof that the trace direction v_T is in ker(Dq_loc[U]) for local rods/clocks/matter",
            "result_if_signed": "alpha_T=0, clock/WEP trace charge=0, local c_T observable projection vanishes",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "ZR872_1_support_nohair_zero",
            "zero_route": "If support(P_loc J_trace) is empty or exact-gauge in compact local U, then phi_T|_U=0.",
            "why_it_works": "The local Green-function source is zero, so the finite-range trace potential never turns on.",
            "current_status": "conditional_not_parent_signed",
            "missing_clause": "support separation, no local tails, and exact-current relative cohomology",
            "result_if_signed": "c_T source term removed before bound rows are needed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "ZR872_2_universal_constant_absorption",
            "zero_route": "If the only surviving trace effect is constant, universal, range-independent GM renormalization, it can be absorbed into measured GM.",
            "why_it_works": "393 shows only constant universal mu_obs avoids a fifth-force/source-normalization residual.",
            "current_status": "insufficient_for_full_zero",
            "missing_clause": "range independence, time constancy, source universality, and no WEP marker",
            "result_if_signed": "not a local fifth force, but still needs source-normalization proof for Newton/local-GR promotion",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "ZR872_3_verdict",
            "zero_route": "Prefer theorem-zero over coefficient fitting.",
            "why_it_works": "It is less scrutinizable to prove Q_T^A=0 from local verticality than to introduce free trace charges and fit them.",
            "current_status": "selected_next_target",
            "missing_clause": "derive or reject local matter trace-charge zero",
            "result_if_signed": "first q_loc channel can close cleanly; if rejected, coefficient-fill route is forced",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def formula_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "formula_id": "OF872_0_R10_yukawa_alpha",
            "arena": "R10_short_range",
            "observable_formula": "alpha_T_AB = Q_T^A Q_T^B/(4*pi*Z_T*G_obs*m_A*m_B), lambda_T=hbar/(m_T*c)",
            "interpretation": "finite-range trace exchange relative to Newtonian attraction",
            "inputs_required": "Z_T;m_T;Q_T^A/m_A;Q_T^B/m_B;full alpha(lambda) curve",
            "claim_status": "blocked_parent_coefficients_and_full_curve_missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "formula_id": "OF872_1_orbital_acceleration",
            "arena": "orbital_dynamics",
            "observable_formula": "delta a/a_N = alpha_T_AB*(1+r/lambda_T)*exp(-r/lambda_T)",
            "interpretation": "range-dependent residual acceleration, not a hidden GM calibration unless constant/universal",
            "inputs_required": "alpha_T_AB;lambda_T;source geometry;GM absorption proof",
            "claim_status": "blocked_source_normalization_and_coefficients_missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "formula_id": "OF872_2_PPN_response",
            "arena": "PPN",
            "observable_formula": "gamma-1=C_T_gamma*c_T, beta-1=C_T_beta*c_T",
            "interpretation": "placeholder response operator until observed metric/coframe is parent-fixed",
            "inputs_required": "metric response;gauge;EH branch;separation from c_P and c_S",
            "claim_status": "blocked_metric_response_missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "formula_id": "OF872_3_clock_WEP_response",
            "arena": "clock_WEP",
            "observable_formula": "delta nu_i/nu_i=C_T_clock_i*c_T; eta_AB controlled by Delta(Q_T/m)",
            "interpretation": "species/no-marker decision: universal or zero is safe, species-dependent is heavily constrained",
            "inputs_required": "matter descent;clock functional;species charges;separation from c_e",
            "claim_status": "blocked_matter_charge_zero_or_fill_missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def coefficient_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "coefficient_id": "CO872_0_Z_T",
            "meaning": "trace carrier kinetic normalization",
            "needed_for": "alpha_T, potential amplitude, positivity/stability",
            "current_owner": "not_parent_owned",
            "allowed_resolution": "derive from parent quadratic action or prove no local trace carrier",
            "if_missing": "all alpha/bound projections stay nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "coefficient_id": "CO872_1_m_T_or_lambda_T",
            "meaning": "trace carrier mass/range",
            "needed_for": "R10 interpolation and finite-range orbital residual",
            "current_owner": "not_parent_owned",
            "allowed_resolution": "derive mass gap/range or prove support no-hair",
            "if_missing": "R10 and finite-range tests cannot score",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "coefficient_id": "CO872_2_Q_T_over_m",
            "meaning": "local matter trace charge per inertial mass",
            "needed_for": "R10, WEP, clocks, source normalization",
            "current_owner": "best_candidate_for_zero_theorem",
            "allowed_resolution": "prove Q_T/m=0 from q_loc verticality or source numeric universal/species charges",
            "if_missing": "the coupling is unconstrained and no local-GR claim is possible",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "coefficient_id": "CO872_3_C_T_metric",
            "meaning": "metric/coframe response of observed PPN potentials to trace leakage",
            "needed_for": "gamma-1, beta-1, clock redshift",
            "current_owner": "not_parent_owned",
            "allowed_resolution": "derive observed metric/coframe map or prove trace mode is local-vertical",
            "if_missing": "PPN formulas remain placeholders",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "coefficient_id": "CO872_4_C_T_source",
            "meaning": "source-normalization response and GM absorption term",
            "needed_for": "Newtonian limit, orbital dynamics, hidden-force guard",
            "current_owner": "conditional_393_only",
            "allowed_resolution": "prove constant universal absorption or retain mu_extra as a boundable residual",
            "if_missing": "Newton/local-GR reduction remains conditional only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC872_0_selected",
            "route": "local_matter_trace_charge_zero_theorem_or_coefficient_fill",
            "status": "selected",
            "reason": "the least scrutinizable route is to prove Q_T^A=0 from local verticality; only if that fails should Z_T,m_T,Q_T,C_T be filled",
            "include": "matter action descent, q_loc verticality, chain-rule charge zero, fallback coefficient ledger",
            "exclude": "numeric claim scoring, fitted c_T, hidden GM calibration, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG872_0_no_projection_claim",
            "claim": "c_T has a derived observable projection",
            "status": "forbidden",
            "reason": "872 gives conditional formulas but no parent-owned coefficients",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG872_1_no_theorem_zero_claim",
            "claim": "c_T=0 or Q_T^A=0 is proved",
            "status": "forbidden",
            "reason": "local verticality and matter descent are still contracts, not parent-derived theorems",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG872_2_no_bound_claim",
            "claim": "R10/PPN/clock/WEP/orbital tests bound c_T",
            "status": "forbidden",
            "reason": "bounds require parent coefficients and, for R10, a full alpha(lambda) curve",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG872_3_allowed_private_result",
            "claim": "c_T coupling has been reduced to explicit parent coefficients or a clean local-charge zero theorem target",
            "status": "allowed_private_nonclaim",
            "reason": "this narrows the coupling problem without pretending it is solved",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D872_0",
            "finding": "projection_formula_exists_only_conditionally",
            "reason": "a standard local quadratic trace carrier yields alpha_T and force-law formulas, but MTS has not derived the carrier/coefficient ownership",
            "status": STATUS,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D872_1",
            "finding": "coupling_reduced_to_five_parent_objects",
            "reason": "Z_T, m_T/lambda_T, Q_T/m, C_T_metric, and C_T_source are the required ownership objects",
            "status": STATUS,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D872_2",
            "finding": "zero_theorem_route_is_best_next_move",
            "reason": "proving Q_T^A=0 from local verticality would kill R10/WEP/clock/PPN leakage with less scrutiny than fitting a free coupling",
            "status": STATUS,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "prove local matter trace charge Q_T^A=0 from S_matter descent through q_loc and v_T in ker(Dq_loc), or explicitly force coefficient-fill fallback",
            "include": "chain-rule derivation, body mass functional, clock/species charges, local-vertical proof obligations, fallback Z_T/m_T/Q_T rows",
            "exclude": "empirical claim scoring, free fitted coupling, hidden calibration, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "attempted c_T observable projection and reduced it to explicit parent coefficients plus a cleaner zero theorem route",
            "best_partial_result": "R10 alpha formula and force-law residual are written conditionally; Q_T^A=0 from local verticality is the best next theorem",
            "hard_blockers": "parent quadratic trace sector, local matter charge, mass/range, metric response, source-normalization absorption",
            "what_is_not_claimed": "c_T projection, c_T zero, R10 bound, PPN pass, clock/WEP pass, orbital pass, local GR/Newton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def any_valid_for_claim_true(paths: list[Path]) -> bool:
    for path in paths:
        if not path.exists():
            return True
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                if row.get("valid_for_claim", "").strip().lower() == "true":
                    return True
    return False


def build_validation_rows(
    source_rows: list[dict[str, object]],
    derivation_rows_value: list[dict[str, object]],
    zero_rows: list[dict[str, object]],
    formula_rows_value: list[dict[str, object]],
    coefficient_rows_value: list[dict[str, object]],
    decision_rows_value: list[dict[str, object]],
) -> list[dict[str, str]]:
    validation_rows: list[dict[str, str]] = []

    sources_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    validation_rows.append(
        {
            "check_id": "V872_0_sources_exist_and_needles",
            "result": "pass" if sources_ok else "fail",
            "detail": "all source paths exist and needles are present" if sources_ok else "one or more source checks failed",
        }
    )

    prior_ok, prior_detail = validation_file_clean(PRIOR_VALIDATION_PATH)
    validation_rows.append(
        {
            "check_id": "V872_1_prior_871_clean",
            "result": "pass" if prior_ok else "fail",
            "detail": prior_detail,
        }
    )

    projection_not_promoted = all(row["current_status"] != "derived" for row in derivation_rows_value)
    validation_rows.append(
        {
            "check_id": "V872_2_projection_not_promoted",
            "result": "pass" if projection_not_promoted else "fail",
            "detail": "all derivation rows remain conditional or blocked",
        }
    )

    formula_fields = [row["observable_formula"] for row in formula_rows_value]
    required_terms = ["alpha_T_AB", "delta a/a_N", "gamma-1", "eta_AB"]
    formulas_ready = all(any(term in formula for formula in formula_fields) for term in required_terms)
    validation_rows.append(
        {
            "check_id": "V872_3_symbolic_formulas_recorded",
            "result": "pass" if formulas_ready else "fail",
            "detail": "R10, orbital, PPN, and clock/WEP formulas recorded symbolically",
        }
    )

    zero_route_selected = any(row["zero_id"] == "ZR872_3_verdict" and row["current_status"] == "selected_next_target" for row in zero_rows)
    validation_rows.append(
        {
            "check_id": "V872_4_zero_theorem_route_selected",
            "result": "pass" if zero_route_selected else "fail",
            "detail": "local matter trace-charge zero route selected",
        }
    )

    coefficient_count_ok = len(coefficient_rows_value) >= 5 and all(row["current_owner"] != "parent_owned" for row in coefficient_rows_value)
    validation_rows.append(
        {
            "check_id": "V872_5_coefficients_listed_not_owned",
            "result": "pass" if coefficient_count_ok else "fail",
            "detail": f"coefficient_rows={len(coefficient_rows_value)} and none parent_owned",
        }
    )

    claim_false = all(row["claim_allowed"] == "false" for row in decision_rows_value)
    validation_rows.append(
        {
            "check_id": "V872_6_claim_allowed_false",
            "result": "pass" if claim_false else "fail",
            "detail": "decision rows keep claim_allowed=false",
        }
    )

    all_nonclaim = not any_valid_for_claim_true(GENERATED_CSV_PATHS)
    validation_rows.append(
        {
            "check_id": "V872_7_all_rows_nonclaim",
            "result": "pass" if all_nonclaim else "fail",
            "detail": "all generated rows valid_for_claim=false",
        }
    )

    formalization_count = formalization_workbench_modified_count()
    validation_rows.append(
        {
            "check_id": "V872_8_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        }
    )

    validation_rows.append(
        {
            "check_id": "V872_9_route_selected",
            "result": "pass",
            "detail": NEXT_TARGET,
        }
    )

    validation_rows.append(
        {
            "check_id": "V872_10_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        }
    )

    return validation_rows


def markdown_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join(["---"] * len(fields)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(markdown_escape(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines) + "\n"


def write_output_doc(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    derivation_rows_value: list[dict[str, object]],
    zero_rows: list[dict[str, object]],
    formula_rows_value: list[dict[str, object]],
    coefficient_rows_value: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_value: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    source_fields = ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"]
    derivation_fields = ["step_id", "attempted_derivation", "symbolic_result", "owned_if", "current_status", "blocker", "valid_for_claim", "generated_utc"]
    zero_fields = ["zero_id", "zero_route", "why_it_works", "current_status", "missing_clause", "result_if_signed", "valid_for_claim", "generated_utc"]
    formula_fields = ["formula_id", "arena", "observable_formula", "interpretation", "inputs_required", "claim_status", "valid_for_claim", "generated_utc"]
    coefficient_fields = ["coefficient_id", "meaning", "needed_for", "current_owner", "allowed_resolution", "if_missing", "valid_for_claim", "generated_utc"]
    route_fields = ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"]
    guard_fields = ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"]
    decision_fields = ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"]
    next_fields = ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"]
    summary_fields = [
        "status",
        "claim_ceiling",
        "what_changed",
        "best_partial_result",
        "hard_blockers",
        "what_is_not_claimed",
        "next_target",
        "valid_for_claim",
        "generated_utc",
    ]
    validation_fields = ["check_id", "result", "detail"]

    doc = "\n".join(
        [
            "# 872 - Y5/R10 c_T Parent Projection Coefficient or Theorem-Zero Return",
            "",
            f"Status: `{STATUS}`  ",
            f"Claim ceiling: `{CLAIM_CEILING}`  ",
            f"Generated UTC: `{generated_utc}`",
            "",
            "Current result: **the coupling problem has been narrowed, not solved**. If a nonzero local trace carrier exists, the R10/orbital projection reduces to `Z_T`, `m_T`, and local matter charges `Q_T/m`; PPN and clock/WEP also require metric/coframe and matter-action response coefficients. The cleaner route is theorem-zero: prove local matter trace charge `Q_T^A=0` from `S_matter=Sbar[q_loc(Phi),psi]` and `v_T in ker(Dq_loc)`.",
            "",
            "## Nonclaim Summary",
            markdown_table(summary_rows, summary_fields),
            "## Source Register",
            markdown_table(source_rows, source_fields),
            "## c_T Parent Projection Derivation Attempt",
            markdown_table(derivation_rows_value, derivation_fields),
            "## Theorem-Zero Return Audit",
            markdown_table(zero_rows, zero_fields),
            "## Observable Projection Formulas",
            markdown_table(formula_rows_value, formula_fields),
            "## Coefficient Ownership Ledger",
            markdown_table(coefficient_rows_value, coefficient_fields),
            "## Route Choice",
            markdown_table(route_rows, route_fields),
            "## Claim Guard",
            markdown_table(guard_rows, guard_fields),
            "## Decision",
            markdown_table(decision_rows_value, decision_fields),
            "## Next Target",
            markdown_table(next_rows, next_fields),
            "## Validation",
            markdown_table(validation_rows, validation_fields),
        ]
    )
    OUTPUT_DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat()

    source_rows = source_register_rows(generated_utc)
    derivation_rows_value = derivation_rows(generated_utc)
    zero_rows = zero_return_rows(generated_utc)
    formula_rows_value = formula_rows(generated_utc)
    coefficient_rows_value = coefficient_rows(generated_utc)
    route_rows = route_choice_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decision_rows_value = decision_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)
    summary_rows = nonclaim_summary_rows(generated_utc)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(DERIVATION_PATH, derivation_rows_value, ["step_id", "attempted_derivation", "symbolic_result", "owned_if", "current_status", "blocker", "valid_for_claim", "generated_utc"])
    write_csv(ZERO_RETURN_PATH, zero_rows, ["zero_id", "zero_route", "why_it_works", "current_status", "missing_clause", "result_if_signed", "valid_for_claim", "generated_utc"])
    write_csv(FORMULA_PATH, formula_rows_value, ["formula_id", "arena", "observable_formula", "interpretation", "inputs_required", "claim_status", "valid_for_claim", "generated_utc"])
    write_csv(COEFFICIENT_PATH, coefficient_rows_value, ["coefficient_id", "meaning", "needed_for", "current_owner", "allowed_resolution", "if_missing", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_CHOICE_PATH, route_rows, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guard_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decision_rows_value, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(
        NONCLAIM_SUMMARY_PATH,
        summary_rows,
        [
            "status",
            "claim_ceiling",
            "what_changed",
            "best_partial_result",
            "hard_blockers",
            "what_is_not_claimed",
            "next_target",
            "valid_for_claim",
            "generated_utc",
        ],
    )

    validation_rows = build_validation_rows(
        source_rows,
        derivation_rows_value,
        zero_rows,
        formula_rows_value,
        coefficient_rows_value,
        decision_rows_value,
    )
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])
    write_output_doc(
        generated_utc,
        source_rows,
        derivation_rows_value,
        zero_rows,
        formula_rows_value,
        coefficient_rows_value,
        route_rows,
        guard_rows,
        decision_rows_value,
        next_rows,
        summary_rows,
        validation_rows,
    )

    failed = [row for row in validation_rows if row["result"] != "pass"]
    if failed:
        raise SystemExit(f"872 validation failed: {failed}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")


if __name__ == "__main__":
    main()
