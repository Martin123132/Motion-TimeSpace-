from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "873-Y5-R10-local-matter-trace-charge-zero-theorem-or-coefficient-fill.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_873_SOURCE_REGISTER.csv"
THEOREM_PATH = RESIDUALS / "P8_Y5_R10_873_LOCAL_TRACE_CHARGE_ZERO_THEOREM.csv"
CLAUSE_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_873_PROOF_CLAUSE_AUDIT.csv"
COUNTEREXAMPLE_PATH = RESIDUALS / "P8_Y5_R10_873_COUNTEREXAMPLE_LEDGER.csv"
FALLBACK_PATH = RESIDUALS / "P8_Y5_R10_873_COEFFICIENT_FILL_FALLBACK.csv"
ROUTE_CHOICE_PATH = RESIDUALS / "P8_Y5_R10_873_ROUTE_CHOICE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_873_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_873_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_873_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_873_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_873_VALIDATION.csv"

PRIOR_VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_872_VALIDATION.csv"

STATUS = "Y5_R10_873_local_trace_charge_zero_conditional_theorem_parent_signature_missing_nonclaim"
CLAIM_CEILING = "conditional_QT_zero_theorem_only_no_cT_zero_no_WEP_R10_PPN_Newton_or_local_GR_claim"
NEXT_TARGET = "874-Y5-R10-parent-qloc-verticality-signature-or-cT-coefficient-fill.md"

GENERATED_CSV_PATHS = [
    SOURCE_REGISTER_PATH,
    THEOREM_PATH,
    CLAUSE_AUDIT_PATH,
    COUNTEREXAMPLE_PATH,
    FALLBACK_PATH,
    ROUTE_CHOICE_PATH,
    CLAIM_GUARD_PATH,
    DECISION_PATH,
    NEXT_TARGET_PATH,
    NONCLAIM_SUMMARY_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "872_doc",
        "path": POST_CHECKPOINT / "872-Y5-R10-cT-parent-projection-coefficient-or-theorem-zero-return.md",
        "needles": [
            "ZR872_0_local_vertical_charge_zero",
            "CO872_2_Q_T_over_m",
            "873-Y5-R10-local-matter-trace-charge-zero-theorem-or-coefficient-fill.md",
        ],
        "role": "immediate local trace-charge zero handoff",
    },
    {
        "source_id": "872_validation",
        "path": PRIOR_VALIDATION_PATH,
        "needles": [
            "V872_4_zero_theorem_route_selected,pass",
            "V872_7_all_rows_nonclaim,pass",
            "V872_8_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "864_local_global_split",
        "path": POST_CHECKPOINT / "864-Y5-R10-local-global-quotient-split-and-endpoint-stationarity-parent-clause.md",
        "needles": [
            "Dq_FLRW[v_T]",
            "Dq_loc[U][v_T] = 0",
            "PC864_2_local_matter_descent",
        ],
        "role": "trace direction local-vertical clause",
    },
    {
        "source_id": "410_matter_functor",
        "path": POST_CHECKPOINT / "410-quotient-matter-functor-theorem-attempt.md",
        "needles": [
            "S_matter = sum_A S_A",
            "factorization/no-marker/no-class-charge premises",
            "counterexample_functors_written",
        ],
        "role": "quotient matter functor and counterexamples",
    },
    {
        "source_id": "626_descent_signature",
        "path": POST_CHECKPOINT / "626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md",
        "needles": [
            "S_matter[Phi,Psi] = Sbar_matter[q(Phi),Psi,theta]",
            "Lie_v S_matter = 0",
            "QMS626_2_matter_descent",
        ],
        "role": "quotient-invariant matter action signature",
    },
    {
        "source_id": "762_geometry_stack",
        "path": POST_CHECKPOINT / "762-Y5-R10-geometry-stack-descent-or-coupling-source-fill.md",
        "needles": [
            "GSD762_0_stack_definition",
            "GSD762_5_stack_verdict",
            "GCE762_0_measure_weyl",
        ],
        "role": "measure/coframe/connection/derivative descent blocker",
    },
    {
        "source_id": "767_WEP_closure",
        "path": POST_CHECKPOINT / "767-Y5-R10-parent-matter-functor-no-alpha-vertex-or-WEP-closure.md",
        "needles": [
            "PMR767_3_no_alpha_mass_vertex",
            "WQ767_0_one_observed_geometry",
            "AWP767_2_MICROSCOPE_beta_target",
        ],
        "role": "WEP/no-alpha vertex pressure and closure quarantine",
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


def theorem_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "QTZ873_0_definition",
            "statement": "Define the local trace matter charge of body/species A by Q_T^A := partial_{v_T} m_A or equivalently the v_T derivative of its local matter action.",
            "derivation": "This is the charge that enters alpha_T_AB = Q_T^A Q_T^B/(4*pi*Z_T*G_obs*m_A*m_B) if a local trace carrier exists.",
            "proof_status": "definition_only",
            "parent_status": "not_claim",
            "what_it_buys": "connects the coupling problem to a single matter-charge zero target",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "QTZ873_1_chain_rule_zero",
            "statement": "If S_A=Sbar_A[Obs_loc(q_loc(Phi)),Psi_A,theta_A] and partial_{v_T} theta_A=0 with v_T in ker(Dq_loc), then Q_T^A=0.",
            "derivation": "partial_{v_T} S_A = (delta S_A/dObs_loc) DObs_loc(Dq_loc[v_T]) + (partial S_A/partial theta_A) partial_{v_T}theta_A = 0.",
            "proof_status": "conditional_theorem_valid",
            "parent_status": "premises_not_parent_signed",
            "what_it_buys": "kills direct R10/WEP/clock trace charge if the local quotient and no-marker premises close",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "QTZ873_2_observable_corollary",
            "statement": "If Q_T^A=0 for all local bodies and clocks, then alpha_T_AB=0, eta_AB trace contribution=0, and clock trace charge=0.",
            "derivation": "The 872 projection formulas are bilinear or linear in Q_T/m or its species/clock derivative.",
            "proof_status": "conditional_corollary_valid",
            "parent_status": "depends_on_QTZ873_1",
            "what_it_buys": "turns c_T local matter coupling off without fitting a tiny coupling",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "QTZ873_3_verdict",
            "statement": "The chain-rule proof shape is correct, but not currently parent-derived.",
            "derivation": "The required local quotient, trace verticality, matter stack descent, and no-marker constant-sector clauses are still unsigned in the corpus.",
            "proof_status": "conditional_not_promoted",
            "parent_status": "signature_missing",
            "what_it_buys": "identifies the exact parent signature needed before the first q_loc coupling can close",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def proof_clause_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "clause_id": "PC873_0_parent_q_loc",
            "required_clause": "q_loc[U]: Phi -> Q_loc(U) exists as a parent-owned local quotient before matter variation",
            "current_status": "not_parent_signed",
            "source_evidence": "864 writes the split as sufficient contract; 626 requires q before matter descent",
            "if_signed": "the charge-zero theorem has a real quotient map to use",
            "if_failed": "v_T may be a physical local variable and Q_T must be filled/bounded",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "PC873_1_trace_verticality",
            "required_clause": "v_T belongs to ker(Dq_loc[U]) for ordinary local labs, sources, rods, clocks, and PPN domains",
            "current_status": "central_unsigned_clause",
            "source_evidence": "864 states Dq_loc[U][v_T]=0 but does not derive the classification",
            "if_signed": "trace endpoint can be FLRW-visible while locally matter-blind",
            "if_failed": "c_T becomes a real local coupling with R10/WEP/PPN pressure",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "PC873_2_matter_stack_descent",
            "required_clause": "measure, coframe/metric, connection, and derivative operator all factor through q_loc",
            "current_status": "not_parent_signed",
            "source_evidence": "762 shows each stack layer can leak representative data if not descended",
            "if_signed": "ordinary matter has no direct v_T geometry derivative",
            "if_failed": "coframe, clocks, spin, EM, or derivative couplings can reintroduce trace charge",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "PC873_3_no_marker_constants",
            "required_clause": "theta_A, alpha_EM, masses, binding responses, and species labels carry no v_T or Q_trace marker charge",
            "current_status": "not_parent_signed",
            "source_evidence": "410 and 767 keep constant-sector/no-alpha/no-marker clauses open",
            "if_signed": "clock/WEP species charge vanishes rather than needing MICROSCOPE tuning",
            "if_failed": "Q_T^A/m_A can be species-dependent and must be bounded",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "PC873_4_boundary_and_reduced_EFT_silence",
            "required_clause": "no boundary/exact local flux or reduced readout EFT reintroduces v_T after quotienting",
            "current_status": "open",
            "source_evidence": "410 counterexamples and 626 boundary term clause remain open",
            "if_signed": "the zero theorem is stable under local integration and EFT readout",
            "if_failed": "zero can be an artifact of chosen variables while local residual remains",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def counterexample_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "counterexample_id": "CE873_0_universal_weyl_trace_carrier",
            "legal_if_unsigned": "matter metric contains A_T(phi_T)^2 g_obs before quotient descent",
            "damage": "WEP may look safe but R10/orbital/common-frame fifth force survives",
            "blocks": "Q_T_zero, c_T_zero, R10 pass",
            "required_response": "prove A_T descends through q_loc with v_T vertical, or fill Q_T/Z_T/m_T coefficients",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "counterexample_id": "CE873_1_species_constant_marker",
            "legal_if_unsigned": "theta_A or binding energy depends on Q_trace or v_T differently by species",
            "damage": "MICROSCOPE/WEP and clock charges activate even if geometry is common",
            "blocks": "WEP and clock silence",
            "required_response": "prove no-marker/no-alpha/no-mass vertex or retain species-charge fallback",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "counterexample_id": "CE873_2_connection_or_derivative_marker",
            "legal_if_unsigned": "omega_m or D_m includes representative torsion/nonmetricity/trace marker",
            "damage": "spin, wave, EM, and clock sectors can see v_T despite coframe descent",
            "blocks": "clock/EM/local-GR matter descent",
            "required_response": "derive full geometry-stack descent, not only metric descent",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "counterexample_id": "CE873_3_boundary_flux_tail",
            "legal_if_unsigned": "P_loc exact/boundary trace current has local flux or tail",
            "damage": "a nominally global trace endpoint still sources compact local domains",
            "blocks": "P_loc J_trace zero and c_T zero",
            "required_response": "prove support/no-tail/relative cohomology silence or keep c_T bound route",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "counterexample_id": "CE873_4_reduced_readout_EFT_marker",
            "legal_if_unsigned": "post-quotient effective action adds Q_trace-dependent local operator",
            "damage": "the parent variables look quotient-clean but the readout EFT reintroduces the charge",
            "blocks": "theorem-zero promotion",
            "required_response": "derive no-extension/minimality rule or label closure explicitly",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def fallback_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "fallback_id": "FB873_0_QT_universal",
            "coefficient": "Q_T_over_m_universal",
            "definition": "common local trace charge per inertial mass if Q_T^A/m_A is the same for all bodies",
            "value": "MISSING_PARENT_INPUT_OR_ZERO_THEOREM",
            "needed_for": "R10/orbital common force and GM absorption audit",
            "claim_gate": "invalid until parent-derived numeric value or Q_T=0 theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fallback_id": "FB873_1_QT_species_delta",
            "coefficient": "Delta_AB_Q_T_over_m",
            "definition": "species/composition difference in local trace charge",
            "value": "MISSING_PARENT_INPUT_OR_NO_MARKER_THEOREM",
            "needed_for": "WEP/MICROSCOPE and clock composition channels",
            "claim_gate": "invalid until no-marker theorem or sourced species coefficients",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fallback_id": "FB873_2_clock_trace_response",
            "coefficient": "C_T_clock_i",
            "definition": "trace-direction response of clock transition i",
            "value": "MISSING_CLOCK_FUNCTIONAL",
            "needed_for": "clock/redshift residual",
            "claim_gate": "invalid until matter constants/clock functional descend through q_loc",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fallback_id": "FB873_3_trace_carrier_norm_range",
            "coefficient": "Z_T_and_m_T",
            "definition": "kinetic normalization and mass/range of any nonzero local trace carrier",
            "value": "MISSING_PARENT_QUADRATIC_SECTOR",
            "needed_for": "R10 alpha(lambda) and finite-range orbital residual",
            "claim_gate": "invalid until local trace carrier is parent-owned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fallback_id": "FB873_4_metric_source_response",
            "coefficient": "C_T_metric_and_C_T_source",
            "definition": "metric/PPN and source-normalization response to local trace charge",
            "value": "MISSING_RESPONSE_OPERATOR",
            "needed_for": "PPN gamma/beta and Newtonian source normalization",
            "claim_gate": "invalid until observed metric and GM absorption are parent-derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC873_0_selected",
            "route": "parent_qloc_verticality_signature_or_cT_coefficient_fill",
            "status": "selected",
            "reason": "the chain-rule zero is valid if v_T is local-vertical; the unsolved problem is now the parent signature for q_loc and v_T classification",
            "include": "q_loc parent ownership, v_T kernel proof, matter-stack descent, no-marker constants, coefficient-fill fallback",
            "exclude": "claiming Q_T=0 now, fitting free coupling, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG873_0_no_QT_zero_claim",
            "claim": "Q_T^A=0 is parent-derived",
            "status": "forbidden",
            "reason": "the proof is conditional; q_loc ownership, v_T verticality, stack descent, and no-marker constants remain unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG873_1_no_WEP_R10_claim",
            "claim": "R10/WEP/clock channels are safe",
            "status": "forbidden",
            "reason": "the observable corollary only follows if Q_T^A=0 is parent-signed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG873_2_no_local_GR_claim",
            "claim": "local GR/Newton follows",
            "status": "forbidden",
            "reason": "closing matter trace charge is only one coupling; q_loc, EH operator, projector stress, and source normalization remain open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG873_3_allowed_private_result",
            "claim": "local trace-charge zero has a valid conditional proof and exact parent-signature debts",
            "status": "allowed_private_nonclaim",
            "reason": "873 sharpens the derivation route without pretending closure is theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D873_0",
            "finding": "conditional_QT_zero_theorem_valid",
            "reason": "the chain-rule proof is correct if matter factors through q_loc and v_T is in the local quotient kernel",
            "status": STATUS,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D873_1",
            "finding": "parent_signature_missing",
            "reason": "q_loc ownership, trace verticality, geometry-stack descent, no-marker constants, and boundary/EFT silence remain unsigned",
            "status": STATUS,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D873_2",
            "finding": "next_target_parent_verticality",
            "reason": "the right next fight is not another data row but proving or rejecting v_T in ker(Dq_loc) from the parent action",
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
            "objective": "derive the parent signature that puts v_T in ker(Dq_loc[U]) for local matter domains, or switch to explicit c_T coefficient fill",
            "include": "parent q_loc definition, compatibility with q_FLRW, trace verticality, domain scope, no-marker constants, fallback coefficient rows",
            "exclude": "using conditional charge-zero as a claim, free fitted c_T, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "proved the local trace-charge zero lemma conditionally and mapped exact parent-signature debts",
            "best_partial_result": "Q_T^A=0 follows by chain rule if matter descends through q_loc and v_T is local-vertical",
            "hard_blockers": "parent q_loc ownership, v_T kernel proof, geometry-stack descent, no-marker constants, boundary/EFT silence",
            "what_is_not_claimed": "Q_T zero, c_T zero, R10/WEP/clock/PPN/orbital pass, Newton/local-GR reduction",
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
    theorem_rows_value: list[dict[str, object]],
    clause_rows: list[dict[str, object]],
    counter_rows: list[dict[str, object]],
    fallback_rows_value: list[dict[str, object]],
    decision_rows_value: list[dict[str, object]],
) -> list[dict[str, str]]:
    validation_rows: list[dict[str, str]] = []

    sources_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    validation_rows.append(
        {
            "check_id": "V873_0_sources_exist_and_needles",
            "result": "pass" if sources_ok else "fail",
            "detail": "all source paths exist and needles are present" if sources_ok else "one or more source checks failed",
        }
    )

    prior_ok, prior_detail = validation_file_clean(PRIOR_VALIDATION_PATH)
    validation_rows.append(
        {
            "check_id": "V873_1_prior_872_clean",
            "result": "pass" if prior_ok else "fail",
            "detail": prior_detail,
        }
    )

    conditional_theorem = any(row["theorem_id"] == "QTZ873_1_chain_rule_zero" and row["proof_status"] == "conditional_theorem_valid" for row in theorem_rows_value)
    validation_rows.append(
        {
            "check_id": "V873_2_conditional_theorem_written",
            "result": "pass" if conditional_theorem else "fail",
            "detail": "Q_T chain-rule zero theorem recorded as conditional",
        }
    )

    not_promoted = any(row["theorem_id"] == "QTZ873_3_verdict" and row["proof_status"] == "conditional_not_promoted" for row in theorem_rows_value)
    validation_rows.append(
        {
            "check_id": "V873_3_theorem_not_promoted",
            "result": "pass" if not_promoted else "fail",
            "detail": "Q_T zero verdict remains not promoted",
        }
    )

    clauses_unsigned = all(row["current_status"] != "parent_signed" for row in clause_rows)
    validation_rows.append(
        {
            "check_id": "V873_4_parent_clauses_unsigned",
            "result": "pass" if clauses_unsigned else "fail",
            "detail": "all parent-signature clauses remain unsigned/open",
        }
    )

    counterexamples_ready = len(counter_rows) >= 5
    validation_rows.append(
        {
            "check_id": "V873_5_counterexamples_recorded",
            "result": "pass" if counterexamples_ready else "fail",
            "detail": f"counterexample_rows={len(counter_rows)}",
        }
    )

    fallback_missing_nonclaim = all("MISSING" in row["value"] and row["valid_for_claim"] == "false" for row in fallback_rows_value)
    validation_rows.append(
        {
            "check_id": "V873_6_fallback_rows_blocked_nonclaim",
            "result": "pass" if fallback_missing_nonclaim else "fail",
            "detail": "fallback coefficient rows remain missing and nonclaim",
        }
    )

    claim_false = all(row["claim_allowed"] == "false" for row in decision_rows_value)
    validation_rows.append(
        {
            "check_id": "V873_7_claim_allowed_false",
            "result": "pass" if claim_false else "fail",
            "detail": "decision rows keep claim_allowed=false",
        }
    )

    all_nonclaim = not any_valid_for_claim_true(GENERATED_CSV_PATHS)
    validation_rows.append(
        {
            "check_id": "V873_8_all_rows_nonclaim",
            "result": "pass" if all_nonclaim else "fail",
            "detail": "all generated rows valid_for_claim=false",
        }
    )

    formalization_count = formalization_workbench_modified_count()
    validation_rows.append(
        {
            "check_id": "V873_9_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        }
    )

    validation_rows.append(
        {
            "check_id": "V873_10_route_selected",
            "result": "pass",
            "detail": NEXT_TARGET,
        }
    )

    validation_rows.append(
        {
            "check_id": "V873_11_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        }
    )

    return validation_rows


def markdown_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
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
    theorem_rows_value: list[dict[str, object]],
    clause_rows: list[dict[str, object]],
    counter_rows: list[dict[str, object]],
    fallback_rows_value: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_value: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    source_fields = ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"]
    theorem_fields = ["theorem_id", "statement", "derivation", "proof_status", "parent_status", "what_it_buys", "valid_for_claim", "generated_utc"]
    clause_fields = ["clause_id", "required_clause", "current_status", "source_evidence", "if_signed", "if_failed", "valid_for_claim", "generated_utc"]
    counter_fields = ["counterexample_id", "legal_if_unsigned", "damage", "blocks", "required_response", "valid_for_claim", "generated_utc"]
    fallback_fields = ["fallback_id", "coefficient", "definition", "value", "needed_for", "claim_gate", "valid_for_claim", "generated_utc"]
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
            "# 873 - Y5/R10 Local Matter Trace-Charge Zero Theorem or Coefficient Fill",
            "",
            f"Status: `{STATUS}`  ",
            f"Claim ceiling: `{CLAIM_CEILING}`  ",
            f"Generated UTC: `{generated_utc}`",
            "",
            "Current result: **the chain-rule zero theorem is valid as mathematics, but not parent-signed as physics**. If local matter really descends only through `q_loc` and `v_T in ker(Dq_loc)`, then every local matter trace charge `Q_T^A` vanishes. That would kill the cleanest `c_T` R10/WEP/clock coupling. The current corpus still has to sign the parent `q_loc` map, trace verticality, matter stack descent, no-marker constants, and boundary/EFT silence.",
            "",
            "## Nonclaim Summary",
            markdown_table(summary_rows, summary_fields),
            "## Source Register",
            markdown_table(source_rows, source_fields),
            "## Local Trace-Charge Zero Theorem",
            markdown_table(theorem_rows_value, theorem_fields),
            "## Proof Clause Audit",
            markdown_table(clause_rows, clause_fields),
            "## Counterexample Ledger",
            markdown_table(counter_rows, counter_fields),
            "## Coefficient Fill Fallback",
            markdown_table(fallback_rows_value, fallback_fields),
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
    theorem_rows_value = theorem_rows(generated_utc)
    clause_rows = proof_clause_rows(generated_utc)
    counter_rows = counterexample_rows(generated_utc)
    fallback_rows_value = fallback_rows(generated_utc)
    route_rows = route_choice_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decision_rows_value = decision_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)
    summary_rows = nonclaim_summary_rows(generated_utc)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(THEOREM_PATH, theorem_rows_value, ["theorem_id", "statement", "derivation", "proof_status", "parent_status", "what_it_buys", "valid_for_claim", "generated_utc"])
    write_csv(CLAUSE_AUDIT_PATH, clause_rows, ["clause_id", "required_clause", "current_status", "source_evidence", "if_signed", "if_failed", "valid_for_claim", "generated_utc"])
    write_csv(COUNTEREXAMPLE_PATH, counter_rows, ["counterexample_id", "legal_if_unsigned", "damage", "blocks", "required_response", "valid_for_claim", "generated_utc"])
    write_csv(FALLBACK_PATH, fallback_rows_value, ["fallback_id", "coefficient", "definition", "value", "needed_for", "claim_gate", "valid_for_claim", "generated_utc"])
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
        theorem_rows_value,
        clause_rows,
        counter_rows,
        fallback_rows_value,
        decision_rows_value,
    )
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])
    write_output_doc(
        generated_utc,
        source_rows,
        theorem_rows_value,
        clause_rows,
        counter_rows,
        fallback_rows_value,
        route_rows,
        guard_rows,
        decision_rows_value,
        next_rows,
        summary_rows,
        validation_rows,
    )

    failed = [row for row in validation_rows if row["result"] != "pass"]
    if failed:
        raise SystemExit(f"873 validation failed: {failed}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")


if __name__ == "__main__":
    main()
