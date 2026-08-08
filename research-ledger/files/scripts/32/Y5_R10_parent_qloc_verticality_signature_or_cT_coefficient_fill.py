from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "874-Y5-R10-parent-qloc-verticality-signature-or-cT-coefficient-fill.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_874_SOURCE_REGISTER.csv"
SIGNATURE_PATH = RESIDUALS / "P8_Y5_R10_874_PARENT_QLOC_VERTICALITY_SIGNATURE.csv"
DERIVATION_PATH = RESIDUALS / "P8_Y5_R10_874_VERTICALITY_DERIVATION_ATTEMPT.csv"
DOMAIN_SCOPE_PATH = RESIDUALS / "P8_Y5_R10_874_DOMAIN_SCOPE_AUDIT.csv"
CT_FILL_PATH = RESIDUALS / "P8_Y5_R10_874_CT_COEFFICIENT_FILL_LEDGER.csv"
ROUTE_CHOICE_PATH = RESIDUALS / "P8_Y5_R10_874_ROUTE_CHOICE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_874_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_874_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_874_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_874_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_874_VALIDATION.csv"

PRIOR_VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_873_VALIDATION.csv"

STATUS = "Y5_R10_874_parent_qloc_verticality_signature_attempt_not_signed_cT_fill_required_nonclaim"
CLAIM_CEILING = "parent_qloc_verticality_signature_contract_only_no_vT_kernel_no_QT_zero_no_cT_zero_or_local_GR_claim"
NEXT_TARGET = "875-Y5-R10-cT-coefficient-fill-minimal-runner-and-claim-gate.md"

GENERATED_CSV_PATHS = [
    SOURCE_REGISTER_PATH,
    SIGNATURE_PATH,
    DERIVATION_PATH,
    DOMAIN_SCOPE_PATH,
    CT_FILL_PATH,
    ROUTE_CHOICE_PATH,
    CLAIM_GUARD_PATH,
    DECISION_PATH,
    NEXT_TARGET_PATH,
    NONCLAIM_SUMMARY_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "873_doc",
        "path": POST_CHECKPOINT / "873-Y5-R10-local-matter-trace-charge-zero-theorem-or-coefficient-fill.md",
        "needles": [
            "PC873_1_trace_verticality",
            "D873_2",
            "874-Y5-R10-parent-qloc-verticality-signature-or-cT-coefficient-fill.md",
        ],
        "role": "immediate parent q_loc verticality handoff",
    },
    {
        "source_id": "873_validation",
        "path": PRIOR_VALIDATION_PATH,
        "needles": [
            "V873_2_conditional_theorem_written,pass",
            "V873_3_theorem_not_promoted,pass",
            "V873_9_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "864_split_contract",
        "path": POST_CHECKPOINT / "864-Y5-R10-local-global-quotient-split-and-endpoint-stationarity-parent-clause.md",
        "needles": [
            "PC864_0_parent_domains",
            "PC864_1_trace_vertical_split",
            "LGS864_3_not_a_decoupled_patch",
        ],
        "role": "local/global quotient split sufficient contract",
    },
    {
        "source_id": "870_nohair",
        "path": POST_CHECKPOINT / "870-Y5-R10-P_loc-Jtrace-nohair-zero-theorem-or-bound.md",
        "needles": [
            "NH870_1_support_separation",
            "NH870_2_quotient_verticality",
            "PT870_0_compact_U_support",
        ],
        "role": "support/no-tail/no-hair blockers for trace verticality",
    },
    {
        "source_id": "626_descent",
        "path": POST_CHECKPOINT / "626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md",
        "needles": [
            "v in ker(Dq)",
            "S_matter[Phi,Psi] = Sbar_matter[q(Phi),Psi,theta]",
            "QMS626_1_vertical_kernel",
        ],
        "role": "generic quotient descent criterion",
    },
    {
        "source_id": "762_stack_descent",
        "path": POST_CHECKPOINT / "762-Y5-R10-geometry-stack-descent-or-coupling-source-fill.md",
        "needles": [
            "GSD762_5_stack_verdict",
            "GCR762_0_stack_chain_rule",
            "GCE762_2_connection_marker",
        ],
        "role": "geometry-stack descent and counterexamples",
    },
    {
        "source_id": "410_functor_counterexamples",
        "path": POST_CHECKPOINT / "410-quotient-matter-functor-theorem-attempt.md",
        "needles": [
            "selector-kernel condition",
            "marker_extended_quotient",
            "quotient_matter_functor_parent_derived",
        ],
        "role": "quotient functor counterexamples and no-marker debt",
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


def signature_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "signature_id": "QVS874_0_parent_state",
            "required_signature": "One parent configuration Phi supports both q_FLRW and q_loc[U] as derived readouts, not separate sectors.",
            "mathematical_form": "q_FLRW:Phi->Q_FLRW and q_loc[U]:Phi->Q_loc(U), with both maps defined before variation.",
            "current_status": "contract_written_not_parent_signed",
            "if_signed": "local/cosmology split is a unified parent mechanism, not patchwork",
            "if_unsigned": "q_loc verticality cannot be used as theorem-zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "QVS874_1_local_restriction_quotient",
            "required_signature": "q_loc[U] is a compact-domain restriction/jet quotient of local observed fields and excludes boundary/global endpoint coordinates.",
            "mathematical_form": "q_loc[U](Phi) = [j^k Phi|_U]_gauge, observed through local matter geometry stack.",
            "current_status": "not_parent_defined",
            "if_signed": "global trace endpoint variations with no support in U are invisible locally",
            "if_unsigned": "Q_trace may be a local scalar/conformal mode and must be bounded",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "QVS874_2_trace_support_class",
            "required_signature": "v_T is a boundary/FLRW zero-mode direction, not a compact local representative field.",
            "mathematical_form": "Dq_FLRW[v_T] != 0 and j^k(v_T)|_U = 0 or pure gauge/exact for compact non-cosmological U.",
            "current_status": "support_class_not_parent_signed",
            "if_signed": "Dq_loc[U][v_T]=0 follows by restriction",
            "if_unsigned": "P_loc J_trace may have finite-range local support",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "QVS874_3_no_tail_relative_cohomology",
            "required_signature": "boundary/exact trace variations have no local tail, relative cohomology flux, scalar gradient, or vector/tensor hair in U.",
            "mathematical_form": "P_loc J_trace|_U = 0 and P_loc dB_trace|_U = 0 through the tested order.",
            "current_status": "open_nohair_clause",
            "if_signed": "verticality remains stable under integration by parts and boundary terms",
            "if_unsigned": "zero can fail through exact-current or tail leakage",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "QVS874_4_matter_stack_and_no_marker",
            "required_signature": "ordinary matter measure/coframe/connection/derivative/constants factor through q_loc and carry no Q_trace marker.",
            "mathematical_form": "G_matter(Phi)=Gbar(q_loc[U](Phi)); theta_A=theta_A(q_loc) or universal constants with partial_{v_T}theta_A=0.",
            "current_status": "not_parent_signed",
            "if_signed": "873 chain-rule theorem gives Q_T^A=0",
            "if_unsigned": "clock/WEP/species/c_g-like channels remain active",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "QVS874_5_signature_verdict",
            "required_signature": "QVS874_0 through QVS874_4 jointly signed by the parent action.",
            "mathematical_form": "v_T in ker(Dq_loc[U]) for all compact local matter domains.",
            "current_status": "not_signed",
            "if_signed": "Q_T^A=0 can be promoted in a future checkpoint",
            "if_unsigned": "explicit c_T coefficient fill is required before local testing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def derivation_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "derivation_id": "VD874_0_restriction_lemma",
            "attempt": "Assume q_loc[U] only depends on local jets/restrictions of parent fields inside compact U.",
            "derivation": "Dq_loc[U][v_T] = D([j^k Phi|_U]_gauge)[v_T] = [j^k v_T|_U]_gauge.",
            "result": "If j^k v_T|_U=0 or gauge/exact-zero, then Dq_loc[U][v_T]=0.",
            "current_status": "valid_conditional_lemma",
            "blocker": "q_loc[U] as local-jet quotient is not parent-derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "derivation_id": "VD874_1_boundary_support_route",
            "attempt": "Classify v_T as a pure FLRW/boundary endpoint direction with no compact local support.",
            "derivation": "supp(v_T) cap U = empty implies j^k v_T|_U=0 for every local lab/solar-system U.",
            "result": "trace endpoint can be globally visible while local matter sees no trace charge",
            "current_status": "plausible_contract_not_parent_signed",
            "blocker": "870 leaves support separation and no-tail theorem unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "derivation_id": "VD874_2_exact_current_route",
            "attempt": "Treat v_T local remnant as exact/gauge current with zero relative flux through U.",
            "derivation": "if v_T=dB_T and B_T has zero local gauge-invariant flux, then [j^k v_T|_U]_gauge=0.",
            "result": "boundary trace current is a gauge artifact in compact local tests",
            "current_status": "conditional_but_unsigned",
            "blocker": "relative cohomology/current support certificate is absent",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "derivation_id": "VD874_3_failure_mode_local_trace_field",
            "attempt": "Allow a local trace carrier phi_T with finite mass/range or conformal matter metric A_T(phi_T)^2 g.",
            "derivation": "j^k v_T|_U != 0, so Dq_loc[U][v_T] may be nonzero and Q_T^A need not vanish.",
            "result": "verticality fails and c_T must be coefficient-filled/bounded",
            "current_status": "legal_counterbranch_if_signature_fails",
            "blocker": "current parent action does not exclude this branch",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "derivation_id": "VD874_4_verdict",
            "attempt": "Decide whether current corpus signs v_T in ker(Dq_loc[U]).",
            "derivation": "restriction/support proof shape exists, but every needed parent signature remains a contract/open no-hair clause.",
            "result": "verticality is not promoted; c_T coefficient fill becomes the honest next move",
            "current_status": "not_proved",
            "blocker": "parent q_loc definition, v_T support class, no-tail certificate, matter-stack descent, no-marker constants",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def domain_scope_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "domain_id": "DS874_0_lab_R10",
            "domain": "torsion-balance/short-range lab compact U",
            "required_verticality": "Dq_loc[U][v_T]=0 and no finite-range phi_T source",
            "current_status": "not_verified",
            "if_failed": "R10 alpha(lambda) branch activates",
            "fallback_needed": "Z_T,m_T,Q_T^test,Q_T^source",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "domain_id": "DS874_1_solar_system_PPN",
            "domain": "solar-system weak-field exterior U",
            "required_verticality": "no scalar gradient, vector B_0i, or tensor B_TF local trace hair",
            "current_status": "not_verified",
            "if_failed": "PPN gamma/beta/preferred-frame residuals activate",
            "fallback_needed": "C_T_gamma,C_T_beta,C_T_alpha_i plus source normalization",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "domain_id": "DS874_2_clock_WEP",
            "domain": "local clocks/material species domains",
            "required_verticality": "theta_A, alpha_EM, masses, binding responses have partial_{v_T}=0",
            "current_status": "not_parent_signed",
            "if_failed": "clock drift and WEP composition charge activate",
            "fallback_needed": "C_T_clock_i,Delta_AB_Q_T_over_m",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "domain_id": "DS874_3_orbital_sources",
            "domain": "orbital/binary source-normalization domain",
            "required_verticality": "trace effect is absent or constant universal range-independent GM renormalization",
            "current_status": "not_parent_signed",
            "if_failed": "Gdot/G, delta_GM, or anomalous acceleration residual activates",
            "fallback_needed": "C_T_source, alpha_T_AB, lambda_T",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "domain_id": "DS874_4_cosmology_FLRW",
            "domain": "FLRW/global readout",
            "required_verticality": "Dq_FLRW[v_T] != 0 while local Dq_loc[v_T]=0",
            "current_status": "desired_split_not_parent_signed",
            "if_failed": "the same variable cannot both drive cosmology and vanish locally without closure",
            "fallback_needed": "explicit split closure or retained local residual",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def ct_fill_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "fill_id": "CTF874_0_Z_T",
            "coefficient": "Z_T",
            "definition": "local trace carrier kinetic normalization if verticality fails",
            "required_source": "parent quadratic trace sector",
            "current_value": "MISSING_PARENT_INPUT",
            "claim_gate": "blocks R10/orbital amplitude scoring",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "CTF874_1_m_T_lambda_T",
            "coefficient": "m_T_or_lambda_T",
            "definition": "local trace carrier mass/range",
            "required_source": "parent mass gap or support/no-tail rejection",
            "current_value": "MISSING_PARENT_INPUT",
            "claim_gate": "blocks alpha(lambda) and finite-range tests",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "CTF874_2_Q_T_over_m_universal",
            "coefficient": "Q_T_over_m_universal",
            "definition": "universal trace charge per inertial mass",
            "required_source": "matter descent failure branch or source-normalized coupling law",
            "current_value": "MISSING_PARENT_INPUT_OR_ZERO_THEOREM",
            "claim_gate": "blocks R10/orbital common-force scoring",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "CTF874_3_Delta_Q_T_over_m_species",
            "coefficient": "Delta_AB_Q_T_over_m",
            "definition": "species/composition differential trace charge",
            "required_source": "no-marker failure branch or material binding response",
            "current_value": "MISSING_NO_MARKER_RESULT",
            "claim_gate": "blocks WEP/clock scoring",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "CTF874_4_metric_source_response",
            "coefficient": "C_T_gamma,C_T_beta,C_T_clock,C_T_source",
            "definition": "observed metric, clock, and source-normalization response to local trace leakage",
            "required_source": "observed coframe/metric response and GM absorption theorem",
            "current_value": "MISSING_RESPONSE_OPERATOR",
            "claim_gate": "blocks PPN/Newton/local-GR scoring",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC874_0_selected",
            "route": "cT_coefficient_fill_minimal_runner_and_claim_gate",
            "status": "selected",
            "reason": "the verticality proof shape is valid but not parent-signed; local testing now needs explicit c_T coefficient inputs rather than another hidden closure",
            "include": "schema for Z_T, lambda_T, Q_T/m, metric/source response, all nonclaim until sourced or zero theorem appears",
            "exclude": "claiming v_T verticality, claiming Q_T=0, public local-GR claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG874_0_no_vT_kernel_claim",
            "claim": "v_T belongs to ker(Dq_loc[U])",
            "status": "forbidden",
            "reason": "restriction/support proof is conditional and parent q_loc/support/no-tail clauses are unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG874_1_no_QT_zero_claim",
            "claim": "Q_T^A=0 follows for local matter",
            "status": "forbidden",
            "reason": "873 requires v_T verticality plus matter-stack/no-marker clauses; 874 does not sign them",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG874_2_no_local_GR_claim",
            "claim": "local GR/Newton is derived",
            "status": "forbidden",
            "reason": "c_T is one q_loc residual channel and coefficient inputs remain missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG874_3_allowed_private_result",
            "claim": "parent q_loc verticality signature and c_T coefficient-fill fallback are explicit",
            "status": "allowed_private_nonclaim",
            "reason": "874 prevents a conditional quotient split from being smuggled in as a theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D874_0",
            "finding": "restriction_support_lemma_valid_conditionally",
            "reason": "if q_loc is a compact local restriction quotient and v_T has no local support, Dq_loc[v_T]=0 follows",
            "status": STATUS,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D874_1",
            "finding": "parent_signature_not_signed",
            "reason": "q_loc definition, v_T support class, no-tail relative cohomology, matter stack, and no-marker constants remain unsigned",
            "status": STATUS,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D874_2",
            "finding": "cT_coefficient_fill_now_required",
            "reason": "after an explicit verticality attempt, the honest non-theorem branch must fill Z_T, range, charge, and response rows before testing",
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
            "objective": "build a minimal nonclaim c_T coefficient-fill runner/gate using Z_T, lambda_T, Q_T/m, metric/source response, and existing bound rows",
            "include": "schema checks, missing-input blockers, no valid claim rows, optional symbolic alpha/PPN/clock/orbital formulas",
            "exclude": "free fitted coupling, claim scoring with MISSING inputs, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "attempted parent q_loc verticality proof and isolated the exact signature needed",
            "best_partial_result": "Dq_loc[v_T]=0 follows if q_loc is a compact restriction quotient and v_T is boundary/global with no local jet support",
            "hard_blockers": "parent q_loc definition, trace support class, no-tail/cohomology certificate, matter-stack descent, no-marker constants",
            "what_is_not_claimed": "v_T kernel, Q_T zero, c_T zero, R10/WEP/PPN/orbital pass, Newton/local-GR reduction",
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
    signature_rows_value: list[dict[str, object]],
    derivation_rows_value: list[dict[str, object]],
    domain_rows: list[dict[str, object]],
    fill_rows: list[dict[str, object]],
    decision_rows_value: list[dict[str, object]],
) -> list[dict[str, str]]:
    validation_rows: list[dict[str, str]] = []

    sources_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    validation_rows.append(
        {
            "check_id": "V874_0_sources_exist_and_needles",
            "result": "pass" if sources_ok else "fail",
            "detail": "all source paths exist and needles are present" if sources_ok else "one or more source checks failed",
        }
    )

    prior_ok, prior_detail = validation_file_clean(PRIOR_VALIDATION_PATH)
    validation_rows.append(
        {
            "check_id": "V874_1_prior_873_clean",
            "result": "pass" if prior_ok else "fail",
            "detail": prior_detail,
        }
    )

    signature_not_signed = any(row["signature_id"] == "QVS874_5_signature_verdict" and row["current_status"] == "not_signed" for row in signature_rows_value)
    validation_rows.append(
        {
            "check_id": "V874_2_signature_not_signed",
            "result": "pass" if signature_not_signed else "fail",
            "detail": "parent q_loc verticality signature remains not signed",
        }
    )

    conditional_lemma = any(row["derivation_id"] == "VD874_0_restriction_lemma" and row["current_status"] == "valid_conditional_lemma" for row in derivation_rows_value)
    validation_rows.append(
        {
            "check_id": "V874_3_conditional_restriction_lemma_written",
            "result": "pass" if conditional_lemma else "fail",
            "detail": "restriction/support verticality lemma recorded conditionally",
        }
    )

    not_proved = any(row["derivation_id"] == "VD874_4_verdict" and row["current_status"] == "not_proved" for row in derivation_rows_value)
    validation_rows.append(
        {
            "check_id": "V874_4_verticality_not_promoted",
            "result": "pass" if not_proved else "fail",
            "detail": "v_T kernel verdict remains not_proved",
        }
    )

    domains_nonclaim = all(row["valid_for_claim"] == "false" and row["current_status"] != "pass_claim" for row in domain_rows)
    validation_rows.append(
        {
            "check_id": "V874_5_domain_scope_nonclaim",
            "result": "pass" if domains_nonclaim else "fail",
            "detail": f"domain_rows={len(domain_rows)} remain nonclaim",
        }
    )

    fill_missing = all("MISSING" in row["current_value"] and row["valid_for_claim"] == "false" for row in fill_rows)
    validation_rows.append(
        {
            "check_id": "V874_6_cT_fill_rows_missing_nonclaim",
            "result": "pass" if fill_missing else "fail",
            "detail": "all c_T fill rows remain missing and nonclaim",
        }
    )

    claim_false = all(row["claim_allowed"] == "false" for row in decision_rows_value)
    validation_rows.append(
        {
            "check_id": "V874_7_claim_allowed_false",
            "result": "pass" if claim_false else "fail",
            "detail": "decision rows keep claim_allowed=false",
        }
    )

    all_nonclaim = not any_valid_for_claim_true(GENERATED_CSV_PATHS)
    validation_rows.append(
        {
            "check_id": "V874_8_all_rows_nonclaim",
            "result": "pass" if all_nonclaim else "fail",
            "detail": "all generated rows valid_for_claim=false",
        }
    )

    formalization_count = formalization_workbench_modified_count()
    validation_rows.append(
        {
            "check_id": "V874_9_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        }
    )

    validation_rows.append(
        {
            "check_id": "V874_10_route_selected",
            "result": "pass",
            "detail": NEXT_TARGET,
        }
    )

    validation_rows.append(
        {
            "check_id": "V874_11_validation_rows_ready",
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
    signature_rows_value: list[dict[str, object]],
    derivation_rows_value: list[dict[str, object]],
    domain_rows: list[dict[str, object]],
    fill_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_value: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    source_fields = ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"]
    signature_fields = ["signature_id", "required_signature", "mathematical_form", "current_status", "if_signed", "if_unsigned", "valid_for_claim", "generated_utc"]
    derivation_fields = ["derivation_id", "attempt", "derivation", "result", "current_status", "blocker", "valid_for_claim", "generated_utc"]
    domain_fields = ["domain_id", "domain", "required_verticality", "current_status", "if_failed", "fallback_needed", "valid_for_claim", "generated_utc"]
    fill_fields = ["fill_id", "coefficient", "definition", "required_source", "current_value", "claim_gate", "valid_for_claim", "generated_utc"]
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
            "# 874 - Y5/R10 Parent q_loc Verticality Signature or c_T Coefficient Fill",
            "",
            f"Status: `{STATUS}`  ",
            f"Claim ceiling: `{CLAIM_CEILING}`  ",
            f"Generated UTC: `{generated_utc}`",
            "",
            "Current result: **the verticality proof has a clean mathematical shape but is not parent-signed**. If `q_loc[U]` is a compact restriction/jet quotient and `v_T` is a pure boundary/FLRW direction with no local jet support, then `Dq_loc[U][v_T]=0`. The corpus still does not derive the local quotient map, trace support class, no-tail/relative-cohomology certificate, matter-stack descent, or no-marker constants. Therefore `v_T in ker(Dq_loc)` is not claimed and the next honest branch is explicit `c_T` coefficient fill.",
            "",
            "## Nonclaim Summary",
            markdown_table(summary_rows, summary_fields),
            "## Source Register",
            markdown_table(source_rows, source_fields),
            "## Parent q_loc Verticality Signature",
            markdown_table(signature_rows_value, signature_fields),
            "## Verticality Derivation Attempt",
            markdown_table(derivation_rows_value, derivation_fields),
            "## Domain Scope Audit",
            markdown_table(domain_rows, domain_fields),
            "## c_T Coefficient Fill Ledger",
            markdown_table(fill_rows, fill_fields),
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
    signature_rows_value = signature_rows(generated_utc)
    derivation_rows_value = derivation_rows(generated_utc)
    domain_rows = domain_scope_rows(generated_utc)
    fill_rows = ct_fill_rows(generated_utc)
    route_rows = route_choice_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decision_rows_value = decision_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)
    summary_rows = nonclaim_summary_rows(generated_utc)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(SIGNATURE_PATH, signature_rows_value, ["signature_id", "required_signature", "mathematical_form", "current_status", "if_signed", "if_unsigned", "valid_for_claim", "generated_utc"])
    write_csv(DERIVATION_PATH, derivation_rows_value, ["derivation_id", "attempt", "derivation", "result", "current_status", "blocker", "valid_for_claim", "generated_utc"])
    write_csv(DOMAIN_SCOPE_PATH, domain_rows, ["domain_id", "domain", "required_verticality", "current_status", "if_failed", "fallback_needed", "valid_for_claim", "generated_utc"])
    write_csv(CT_FILL_PATH, fill_rows, ["fill_id", "coefficient", "definition", "required_source", "current_value", "claim_gate", "valid_for_claim", "generated_utc"])
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
        signature_rows_value,
        derivation_rows_value,
        domain_rows,
        fill_rows,
        decision_rows_value,
    )
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])
    write_output_doc(
        generated_utc,
        source_rows,
        signature_rows_value,
        derivation_rows_value,
        domain_rows,
        fill_rows,
        route_rows,
        guard_rows,
        decision_rows_value,
        next_rows,
        summary_rows,
        validation_rows,
    )

    failed = [row for row in validation_rows if row["result"] != "pass"]
    if failed:
        raise SystemExit(f"874 validation failed: {failed}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")


if __name__ == "__main__":
    main()
