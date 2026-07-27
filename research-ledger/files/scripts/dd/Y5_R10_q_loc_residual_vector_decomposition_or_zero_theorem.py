from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "869-Y5-R10-q_loc-residual-vector-decomposition-or-zero-theorem.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_869_SOURCE_REGISTER.csv"
QLOC_IDENTITY_PATH = RESIDUALS / "P8_Y5_R10_869_QLOC_IDENTITY_DECOMPOSITION.csv"
ZERO_THEOREM_PATH = RESIDUALS / "P8_Y5_R10_869_ZERO_THEOREM_ATTEMPT.csv"
RESIDUAL_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_869_RETAINED_RESIDUAL_COEFFICIENT_LEDGER.csv"
OBSERVABLE_MAP_PATH = RESIDUALS / "P8_Y5_R10_869_OBSERVABLE_MAP.csv"
RANKED_TARGET_PATH = RESIDUALS / "P8_Y5_R10_869_RANKED_NEXT_TARGET.csv"
ROUTE_CHOICE_PATH = RESIDUALS / "P8_Y5_R10_869_ROUTE_CHOICE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_869_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_869_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_869_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_869_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_869_VALIDATION.csv"

PRIOR_VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_868_VALIDATION.csv"

STATUS = "Y5_R10_869_q_loc_zero_theorem_conditions_written_residual_vector_retained_nonclaim"
CLAIM_CEILING = "conditional_q_loc_zero_contract_only_no_local_GR_no_Newton_no_PPN_claim"
NEXT_TARGET = "870-Y5-R10-P_loc-Jtrace-nohair-zero-theorem-or-bound.md"

GENERATED_CSV_PATHS = [
    SOURCE_REGISTER_PATH,
    QLOC_IDENTITY_PATH,
    ZERO_THEOREM_PATH,
    RESIDUAL_LEDGER_PATH,
    OBSERVABLE_MAP_PATH,
    RANKED_TARGET_PATH,
    ROUTE_CHOICE_PATH,
    CLAIM_GUARD_PATH,
    DECISION_PATH,
    NEXT_TARGET_PATH,
    NONCLAIM_SUMMARY_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "868_doc",
        "path": POST_CHECKPOINT / "868-Y5-R10-local-GR-reduction-stack-after-endpoint-closure.md",
        "needles": [
            "q_loc_is_next_common_hinge",
            "QL868_0_trace_endpoint_flux",
            "869-Y5-R10-q_loc-residual-vector-decomposition-or-zero-theorem.md",
        ],
        "role": "immediate q_loc handoff",
    },
    {
        "source_id": "868_validation",
        "path": PRIOR_VALIDATION_PATH,
        "needles": [
            "V868_4_q_loc_decomposition_ready,pass",
            "V868_9_all_rows_nonclaim,pass",
            "V868_10_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "863_trace_zero",
        "path": POST_CHECKPOINT / "863-Y5-R10-Ward-trace-lift-current-and-coframe-pullback-zero-theorem.md",
        "needles": [
            "WTC863_4_local_projection_silence",
            "CZT863_0_chain_rule_zero",
            "LRF863_1_trace_leak_branch",
        ],
        "role": "trace projection and coframe chain-rule zero context",
    },
    {
        "source_id": "864_quotient_split",
        "path": POST_CHECKPOINT / "864-Y5-R10-local-global-quotient-split-and-endpoint-stationarity-parent-clause.md",
        "needles": [
            "Dq_FLRW[v_T] = delta Q_trace",
            "Dq_loc[U][v_T] = 0",
            "GN864_2_if_split_fails",
        ],
        "role": "local/global quotient split sufficient clause",
    },
    {
        "source_id": "347_local_GR_attempt",
        "path": POST_CHECKPOINT / "347-local-GR-parent-reduction-theorem-attempt.md",
        "needles": [
            "conditional_GR_reduction_only_no_local_GR_or_PPN_claim",
            "metric variation owned by parent",
            "`N5` projector stress cleared",
        ],
        "role": "local GR parent-reduction fail/pass gates",
    },
    {
        "source_id": "393_Newton_source",
        "path": POST_CHECKPOINT / "393-source-normalized-Newtonian-limit-under-identity-closure.md",
        "needles": [
            "G_eff = kappa_eff c^4/(8 pi)",
            "constant universal",
            "Newtonian/local-GR promoted",
        ],
        "role": "source-normalized Newtonian limit residuals",
    },
    {
        "source_id": "179_PPN_silence",
        "path": POST_CHECKPOINT / "179-local-GR-PPN-silence-contract.md",
        "needles": [
            "q_loc^nu -> 0",
            "gamma = beta = 1",
            "screened effective, not derived",
        ],
        "role": "PPN silence and open q_loc target",
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
    missing_needles = [needle for needle in needles if needle not in text]
    if missing_needles:
        return "missing_needles:" + ";".join(missing_needles)
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


def qloc_identity_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "term_id": "QI869_0_definition",
            "symbolic_piece": "q_loc^nu := P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "role": "total local exchange/residual vector",
            "zero_condition": "the projected parent divergence mismatch vanishes in every local compact test domain",
            "if_nonzero": "local fifth-force/source-exchange residual",
            "status": "definition_target_not_zero_theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "term_id": "QI869_1_trace_endpoint_channel",
            "symbolic_piece": "q_T^nu = P_loc J_trace^nu or P_loc(delta boundary exact trace current)",
            "role": "FLRW trace endpoint leakage",
            "zero_condition": "Q_trace is FLRW-visible but local-vertical and boundary no-hair kills exterior projection",
            "if_nonzero": "trace-memory local force/clock/PPN hair",
            "status": "conditional_zero_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "term_id": "QI869_2_coframe_matter_channel",
            "symbolic_piece": "q_e^nu = P_loc Pi_I^matter",
            "role": "matter/coframe pullback residual",
            "zero_condition": "ordinary matter descends through q_loc and partial_I ehat_loc=0 by chain rule",
            "if_nonzero": "matter stress sources extra selector/projector equations",
            "status": "chain_rule_shape_unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "term_id": "QI869_3_projector_channel",
            "symbolic_piece": "q_P^nu = P_loc(F_P^nu) or P_loc(nabla_mu T_projector^{mu nu})",
            "role": "metric/projector variation residual",
            "zero_condition": "projector stress is zero, pure gauge, boundary-only conserved, or explicitly retained with no local exterior support",
            "if_nonzero": "modified local exterior metric and PPN gamma/beta/slip residual",
            "status": "open_hard",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "term_id": "QI869_4_source_normalization_channel",
            "symbolic_piece": "q_S^nu = P_loc source-normalization drift from Gamma_eff/K_hat",
            "role": "measured GM and Newtonian source residual",
            "zero_condition": "G_eff M_eff is constant, universal, range-independent, and species-independent",
            "if_nonzero": "delta_G, Gdot/G, WEP source charge, or finite-range force",
            "status": "open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def zero_theorem_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "clause_id": "ZT869_0_parent_variation",
            "needed_clause": "parent action owns Gamma_eff, K_hat, projector variation, and all boundary/source stresses",
            "current_evidence": "contracts exist but not full parent variation theorem",
            "zero_result_if_signed": "q_loc can be interpreted as a real parent residual rather than a symbolic bookkeeping object",
            "status": "unsigned",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "ZT869_1_local_quotient_verticality",
            "needed_clause": "Dq_loc[U][v_T]=0 for trace endpoint/projector directions in compact local domains",
            "current_evidence": "864 writes sufficient clause but does not derive q_loc from parent action",
            "zero_result_if_signed": "P_loc J_trace and direct matter pullback can vanish by quotient descent",
            "status": "conditional_not_parent_derived",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "ZT869_2_boundary_nohair",
            "needed_clause": "P_loc J_trace=0 and no shear/vector/clock/range boundary component survives",
            "current_evidence": "listed as open in 861-864 and 868",
            "zero_result_if_signed": "trace endpoint closure stays cosmological and does not become a local force",
            "status": "open",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "ZT869_3_matter_descent",
            "needed_clause": "S_matter depends on parent fields only through the local observed quotient/coframe",
            "current_evidence": "chain-rule proof shape exists; no-marker descent is not signed",
            "zero_result_if_signed": "Pi_I^matter=0 for arbitrary local matter stress",
            "status": "conditional_not_parent_derived",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "ZT869_4_projector_stress_fate",
            "needed_clause": "T_projector is zero, pure gauge, conserved boundary-only, or retained explicitly",
            "current_evidence": "N5/projector stress remains open hard blocker",
            "zero_result_if_signed": "no fake EH exterior from dropped projector variation",
            "status": "open_hard",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "ZT869_5_source_normalization",
            "needed_clause": "measured GM is constant/universal and all source drifts/range/species pieces vanish",
            "current_evidence": "393 shows conditional algebra but no parent absorption theorem",
            "zero_result_if_signed": "Newtonian source limit is not just EH-shaped; it is physically normalized",
            "status": "open",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "ZT869_6_zero_theorem_verdict",
            "needed_clause": "ZT869_0 through ZT869_5 all parent-signed",
            "current_evidence": "multiple clauses are unsigned/open",
            "zero_result_if_signed": "q_loc^nu=0 and local GR/Newton branch becomes promotable subject to PPN verification",
            "status": "not_proved",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def residual_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "residual_id": "RR869_T",
            "coefficient": "c_T",
            "channel": "trace endpoint / boundary no-hair failure",
            "schematic_source": "P_loc J_trace",
            "units_status": "needs source-normalized force or potential units",
            "observable_links": "PPN gamma/beta, clock drift, WEP if composition-coupled, orbital residuals, R10 if finite range",
            "status": "retained_if_zero_theorem_fails",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "RR869_e",
            "coefficient": "c_e",
            "channel": "coframe/matter pullback",
            "schematic_source": "Pi_I^matter",
            "units_status": "needs matter-stress projection normalization",
            "observable_links": "WEP, clock comparisons, nonmetric light cone, matter source drift",
            "status": "retained_if_matter_descent_fails",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "RR869_P",
            "coefficient": "c_P",
            "channel": "projector stress / N5 failure",
            "schematic_source": "F_P^nu or nabla_mu T_projector^{mu nu}",
            "units_status": "needs metric variation/source normalization",
            "observable_links": "gamma-1, beta-1, Phi-Psi, perihelion/orbital precession, lensing slip",
            "status": "retained_if_projector_not_closed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "RR869_S",
            "coefficient": "c_S",
            "channel": "source normalization / measured GM",
            "schematic_source": "delta(G_eff M_eff), mu_extra(lambda), species source charge",
            "units_status": "needs delta_G, Gdot/G, alpha(lambda), eta_WEP units",
            "observable_links": "Newtonian GM, Gdot/G, fifth-force alpha(lambda), WEP, clock/orbital residuals",
            "status": "retained_if_GM_absorption_fails",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def observable_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "observable_id": "OM869_0_PPN_gamma",
            "observable": "gamma-1 / gravitational slip",
            "sensitive_channels": "c_T,c_P,c_S",
            "zero_requirement": "no trace/projector anisotropic exterior support and EH operator selected",
            "current_status": "not_parent_derived",
            "test_or_bound_arena": "Cassini/PPN/lensing/orbital baselines",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "observable_id": "OM869_1_PPN_beta",
            "observable": "beta-1 / nonlinear source hair",
            "sensitive_channels": "c_P,c_S",
            "zero_requirement": "projector stress closed and measured GM constant through nonlinear weak-field order",
            "current_status": "not_parent_derived",
            "test_or_bound_arena": "PPN/orbital baselines",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "observable_id": "OM869_2_clock_WEP",
            "observable": "clock drift and WEP/composition force",
            "sensitive_channels": "c_T,c_e,c_S",
            "zero_requirement": "one local coframe, no-marker matter descent, universal source charge",
            "current_status": "screened_effective_not_parent_derived",
            "test_or_bound_arena": "clock/WEP/local fifth-force baselines",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "observable_id": "OM869_3_R10_fifth_force",
            "observable": "finite-range alpha(lambda)",
            "sensitive_channels": "c_T,c_S",
            "zero_requirement": "no finite-range local trace/source projection",
            "current_status": "source rows not claim-ready",
            "test_or_bound_arena": "R10/Eot-Wash short-range bound curve",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "observable_id": "OM869_4_Newton_GM",
            "observable": "constant measured GM and Gdot/G",
            "sensitive_channels": "c_S",
            "zero_requirement": "G_eff M_eff constant, universal, and source-normalized",
            "current_status": "not_parent_derived",
            "test_or_bound_arena": "orbital dynamics, lunar/planetary timing, local Gdot bounds",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def ranked_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "rank": "1",
            "candidate_target": "P_loc_Jtrace_nohair_zero_theorem",
            "why_first": "trace endpoint/local leakage is the first q_loc term and the cleanest local/global quotient test",
            "success_condition": "prove P_loc J_trace=0 from q_FLRW/q_loc compatibility and boundary no-hair",
            "failure_action": "create c_T bound/source rows for PPN/clock/orbital/R10",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rank": "2",
            "candidate_target": "matter_descent_no_marker_theorem",
            "why_first": "needed for Pi_I^matter=0 and WEP/clock silence",
            "success_condition": "prove S_matter factors only through q_loc observed coframe",
            "failure_action": "retain c_e matter-pullback coefficient rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rank": "3",
            "candidate_target": "N5_projector_stress_fate",
            "why_first": "blocks EH exterior and gamma/beta if nonzero",
            "success_condition": "zero/gauge/boundary-conserved projector stress or explicit retained stress",
            "failure_action": "retain c_P metric/projector coefficient rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rank": "4",
            "candidate_target": "source_normalized_GM_theorem",
            "why_first": "needed after EH shape to get Newton, not just Einstein-shaped algebra",
            "success_condition": "G_eff M_eff is constant universal measured GM",
            "failure_action": "retain c_S delta_G/Gdot/fifth-force/WEP source rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC869_0_selected",
            "route": "P_loc_Jtrace_nohair_zero_theorem_or_bound",
            "status": "selected",
            "reason": "P_loc J_trace is the first and cleanest q_loc term; if it fails, local trace leakage must be bounded before local GR can be claimed",
            "include": "q_FLRW/q_loc compatibility, boundary no-hair, P_loc exact-current silence, c_T fallback rows",
            "exclude": "endpoint root algebra, public local-GR claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG869_0_no_q_loc_zero_claim",
            "claim": "q_loc^nu=0 is derived",
            "status": "forbidden",
            "reason": "zero theorem clauses include unsigned local quotient, boundary no-hair, matter descent, projector stress, and source normalization",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG869_1_no_local_GR_claim",
            "claim": "MTS derives local GR/Newton",
            "status": "forbidden",
            "reason": "q_loc residual vector is decomposed but not zeroed or bounded",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG869_2_no_PPN_claim",
            "claim": "PPN vector passes",
            "status": "forbidden",
            "reason": "observable map is only a ledger; no residual coefficients are yet sourced and scored",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG869_3_allowed_private_result",
            "claim": "q_loc residual vector is now decomposed and ranked",
            "status": "allowed_private_nonclaim",
            "reason": "869 turns a vague local-GR blocker into testable theorem/residual channels",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D869_0",
            "finding": "q_loc_zero_theorem_not_proved",
            "reason": "required local quotient, boundary no-hair, matter descent, projector stress, and source normalization clauses remain unsigned/open",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D869_1",
            "finding": "residual_vector_decomposed",
            "reason": "q_loc split into trace, coframe/matter, projector, and source-normalization channels with observable links",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D869_2",
            "finding": "P_loc_Jtrace_selected_first",
            "reason": "trace endpoint leakage is the first and narrowest zero theorem needed for local/global quotient silence",
            "status": CLAIM_CEILING,
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
            "objective": "derive P_loc J_trace=0 from local/global quotient compatibility and boundary no-hair, or retain c_T source-normalized bound rows",
            "include": "exact-current projection, compact local domain, FLRW-visible/local-vertical split, shear/vector/clock/range no-hair checks, c_T fallback",
            "exclude": "endpoint root algebra, public claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "decomposed q_loc^nu into trace, coframe, projector, and source-normalization residual channels",
            "best_partial_result": "a conditional q_loc zero theorem is now explicit, and its failure branches are mapped to retained coefficients c_T,c_e,c_P,c_S",
            "hard_blockers": "P_loc J_trace no-hair, matter descent, projector stress fate, source-normalized GM",
            "what_is_not_claimed": "q_loc zero, local GR, Newtonian limit, PPN pass",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_csv_rows_nonclaim(paths: list[Path]) -> tuple[bool, str]:
    offenders: list[str] = []
    for path in paths:
        if not path.exists():
            offenders.append(f"{path.name}:missing")
            continue
        with path.open("r", encoding="utf-8", newline="") as handle:
            for index, row in enumerate(csv.DictReader(handle), start=2):
                if row.get("valid_for_claim") != "false":
                    offenders.append(f"{path.name}:{index}")
    if offenders:
        return False, ";".join(offenders)
    return True, "all generated rows valid_for_claim=false"


def csv_table(rows: list[dict[str, object]], fieldnames: list[str]) -> str:
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join(["---"] * len(fieldnames)) + " |",
    ]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "/") for field in fieldnames]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_markdown(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    qloc_rows_: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    residual_rows_: list[dict[str, object]],
    observable_rows_: list[dict[str, object]],
    ranked_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    content = f"""# 869 - q_loc Residual Vector Decomposition Or Zero Theorem

Generated: `{generated_utc}`

Current result: **`q_loc^nu` is now decomposed rather than waved away**. The clean zero theorem is visible: if the parent action owns the local quotient, boundary no-hair, matter descent, projector stress fate, and source-normalized Newtonian charge, then `q_loc^nu=0`. But the current corpus does not sign those clauses. So the honest state is a retained residual vector with four channels: trace endpoint leakage `c_T`, coframe/matter pullback `c_e`, projector stress `c_P`, and source normalization `c_S`. The next theorem target is the first and narrowest channel: prove `P_loc J_trace=0`, or keep `c_T` as a boundable local-residual row.

## Nonclaim Summary

{csv_table(summary_rows, ["status", "claim_ceiling", "what_changed", "best_partial_result", "hard_blockers", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])}

## Source Register

{csv_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])}

## q_loc Identity Decomposition

{csv_table(qloc_rows_, ["term_id", "symbolic_piece", "role", "zero_condition", "if_nonzero", "status", "valid_for_claim", "generated_utc"])}

## Zero Theorem Attempt

{csv_table(theorem_rows, ["clause_id", "needed_clause", "current_evidence", "zero_result_if_signed", "status", "blocks_claim", "valid_for_claim", "generated_utc"])}

## Retained Residual Coefficient Ledger

{csv_table(residual_rows_, ["residual_id", "coefficient", "channel", "schematic_source", "units_status", "observable_links", "status", "valid_for_claim", "generated_utc"])}

## Observable Map

{csv_table(observable_rows_, ["observable_id", "observable", "sensitive_channels", "zero_requirement", "current_status", "test_or_bound_arena", "valid_for_claim", "generated_utc"])}

## Ranked Next Target

{csv_table(ranked_rows, ["rank", "candidate_target", "why_first", "success_condition", "failure_action", "valid_for_claim", "generated_utc"])}

## Route Choice

{csv_table(route_rows, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"])}

## Claim Guard

{csv_table(claim_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])}

## Decision

{csv_table(decision_rows_, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])}

## Next Target

{csv_table(next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])}

## Validation

{csv_table(validation_rows, ["check_id", "result", "detail"])}
"""
    OUTPUT_DOC.write_text(content, encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat()

    source_rows = source_register_rows(generated_utc)
    qloc_rows_ = qloc_identity_rows(generated_utc)
    theorem_rows = zero_theorem_rows(generated_utc)
    residual_rows_ = residual_rows(generated_utc)
    observable_rows_ = observable_rows(generated_utc)
    ranked_rows = ranked_target_rows(generated_utc)
    route_rows = route_choice_rows(generated_utc)
    claim_rows = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)
    summary_rows = nonclaim_summary_rows(generated_utc)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(QLOC_IDENTITY_PATH, qloc_rows_, ["term_id", "symbolic_piece", "role", "zero_condition", "if_nonzero", "status", "valid_for_claim", "generated_utc"])
    write_csv(ZERO_THEOREM_PATH, theorem_rows, ["clause_id", "needed_clause", "current_evidence", "zero_result_if_signed", "status", "blocks_claim", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUAL_LEDGER_PATH, residual_rows_, ["residual_id", "coefficient", "channel", "schematic_source", "units_status", "observable_links", "status", "valid_for_claim", "generated_utc"])
    write_csv(OBSERVABLE_MAP_PATH, observable_rows_, ["observable_id", "observable", "sensitive_channels", "zero_requirement", "current_status", "test_or_bound_arena", "valid_for_claim", "generated_utc"])
    write_csv(RANKED_TARGET_PATH, ranked_rows, ["rank", "candidate_target", "why_first", "success_condition", "failure_action", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_CHOICE_PATH, route_rows, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, claim_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decision_rows_, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary_rows, ["status", "claim_ceiling", "what_changed", "best_partial_result", "hard_blockers", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])

    prior_clean, prior_detail = validation_file_clean(PRIOR_VALIDATION_PATH)
    source_checks_pass = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    decomposition_pass = len(qloc_rows_) == 5 and qloc_rows_[0]["term_id"] == "QI869_0_definition"
    zero_theorem_not_promoted_pass = any(row["clause_id"] == "ZT869_6_zero_theorem_verdict" and row["status"] == "not_proved" for row in theorem_rows)
    residual_coefficients_pass = {row["coefficient"] for row in residual_rows_} == {"c_T", "c_e", "c_P", "c_S"}
    observable_map_pass = len(observable_rows_) == 5 and any(row["observable_id"] == "OM869_3_R10_fifth_force" for row in observable_rows_)
    ranked_target_pass = ranked_rows[0]["candidate_target"] == "P_loc_Jtrace_nohair_zero_theorem"
    route_selected_pass = route_rows[0]["route"] == "P_loc_Jtrace_nohair_zero_theorem_or_bound"
    claim_allowed_false_pass = all(row["claim_allowed"] == "false" for row in decision_rows_)
    formalization_count = formalization_workbench_modified_count()

    validation_rows = [
        {"check_id": "V869_0_sources_exist_and_needles", "result": "pass" if source_checks_pass else "fail", "detail": "all source paths exist and needles are present" if source_checks_pass else "one or more source checks failed"},
        {"check_id": "V869_1_prior_868_clean", "result": "pass" if prior_clean else "fail", "detail": prior_detail},
        {"check_id": "V869_2_q_loc_decomposition_ready", "result": "pass" if decomposition_pass else "fail", "detail": "q_loc split into definition plus four residual channels"},
        {"check_id": "V869_3_zero_theorem_not_promoted", "result": "pass" if zero_theorem_not_promoted_pass else "fail", "detail": "zero theorem verdict remains not_proved"},
        {"check_id": "V869_4_residual_coefficients_ready", "result": "pass" if residual_coefficients_pass else "fail", "detail": "c_T,c_e,c_P,c_S retained"},
        {"check_id": "V869_5_observable_map_ready", "result": "pass" if observable_map_pass else "fail", "detail": "PPN/clock/WEP/R10/Newton observable links recorded"},
        {"check_id": "V869_6_ranked_target_ready", "result": "pass" if ranked_target_pass else "fail", "detail": "P_loc J_trace no-hair selected first"},
        {"check_id": "V869_7_route_selected", "result": "pass" if route_selected_pass else "fail", "detail": NEXT_TARGET},
        {"check_id": "V869_8_claim_allowed_false", "result": "pass" if claim_allowed_false_pass else "fail", "detail": "decision rows keep claim_allowed=false"},
        {"check_id": "V869_9_all_rows_nonclaim", "result": "pending", "detail": "filled after csv nonclaim scan"},
        {"check_id": "V869_10_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V869_11_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]

    nonclaim_pass, nonclaim_detail = all_csv_rows_nonclaim(GENERATED_CSV_PATHS)
    for row in validation_rows:
        if row["check_id"] == "V869_9_all_rows_nonclaim":
            row["result"] = "pass" if nonclaim_pass else "fail"
            row["detail"] = nonclaim_detail

    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])
    write_markdown(
        generated_utc,
        source_rows,
        qloc_rows_,
        theorem_rows,
        residual_rows_,
        observable_rows_,
        ranked_rows,
        route_rows,
        claim_rows,
        decision_rows_,
        next_rows,
        summary_rows,
        validation_rows,
    )

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"status={STATUS}")
    print("partial_result=q_loc zero theorem conditions are explicit; residual coefficients c_T,c_e,c_P,c_S retained")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")
    if failed:
        for row in failed:
            print(f"validation_failure={row['check_id']}:{row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
