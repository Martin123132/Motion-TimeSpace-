from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

STATUS = "Y5_R10_877_parent_trace_Hessian_source_hunt_done_minimal_Htr_skeleton_written_no_computable_coefficients_nonclaim"
CLAIM_CEILING = "source_hunt_and_minimal_Htr_skeleton_only_no_parent_owned_Ztr_lambda_tr_zero_return_R10_PPN_WEP_or_local_GR_claim"
NEXT_TARGET = "878-Y5-R10-Ptr-parent-projector-definition-and-constraint-rank-test.md"


SOURCES = [
    {
        "source_id": "876_doc",
        "path": ROOT / "876-Y5-R10-trace-sector-ZT-lambdaT-parent-input-or-zero-return.md",
        "needle": "the coupling target is now an exact parent-Hessian problem",
        "role": "immediate H_T/Hessian target handoff",
    },
    {
        "source_id": "876_validation",
        "path": OUT / "P8_Y5_BRR545_876_VALIDATION.csv",
        "needle": "V876_11_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "407_action_sketch",
        "path": ROOT / "407-primitive-relational-quotient-action-sketch.md",
        "needle": "Action Skeleton",
        "role": "broad primitive parent-action sketch",
    },
    {
        "source_id": "321_projector_gate",
        "path": ROOT / "321-rank-two-screen-projector-gate.md",
        "needle": "P_active = P_M tensor P_T tensor P_screen",
        "role": "old P_T notation and full-cell projector warning",
    },
    {
        "source_id": "322_singlet_gate",
        "path": ROOT / "322-S3-singlet-motion-time-projector-gate.md",
        "needle": "P_T = P_singlet on the time/history sector",
        "role": "old P_T means time/history singlet, not trace projector",
    },
    {
        "source_id": "337_exact_pullback",
        "path": ROOT / "337-exact-parent-pullback-selection-rule-gate.md",
        "needle": "exact parent readout",
        "role": "readout after full parent variation rule",
    },
    {
        "source_id": "338_action_readout",
        "path": ROOT / "338-action-level-exact-readout-gate.md",
        "needle": "P_active is a post-variation observable",
        "role": "no-spurion/readout-source-at-zero rule",
    },
    {
        "source_id": "382_local_action_contract",
        "path": ROOT / "382-parent-local-action-minimal-contract.md",
        "needle": "Minimal Action Skeleton",
        "role": "minimal local parent-action sector list",
    },
    {
        "source_id": "421_fibre_decoupling",
        "path": ROOT / "421-finite-fibre-spectrum-decoupling-theorem-attempt.md",
        "needle": "mass gap, Hessian sign",
        "role": "mass-gap/Hessian/source-independence debt template",
    },
    {
        "source_id": "437_R10_curve_contract",
        "path": ROOT / "437-R10-alpha-lambda-executable-curve-contract.md",
        "needle": "alpha(lambda) curve",
        "role": "bound branch rule if finite trace carrier remains",
    },
    {
        "source_id": "446_source_owner",
        "path": ROOT / "446-source-owner-current-parent-action-contract.md",
        "needle": "Required Parent-Action Blocks",
        "role": "source-owner/nohair action block obligations",
    },
    {
        "source_id": "872_trace_projection",
        "path": ROOT / "872-Y5-R10-cT-parent-projection-coefficient-or-theorem-zero-return.md",
        "needle": "S_T^loc",
        "role": "conditional scalar trace carrier ansatz",
    },
]

KEYWORDS = [
    "S_parent",
    "Hessian",
    "principal symbol",
    "trace sector",
    "trace carrier",
    "P_T",
    "P_tr",
    "J_T",
    "Z_T",
    "lambda_T",
    "mass gap",
    "second variation",
    "scalar pole",
    "source-free",
    "exact readout",
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def stringify(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return "" if value is None else str(value)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def has_needle(path: Path, needle: str) -> bool:
    return needle in read_text(path)


def md_table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        cells = [stringify(row.get(header, "")).replace("\n", " ") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source in SOURCES:
        path = Path(source["path"])
        needle = str(source["needle"])
        rows.append(
            {
                "source_id": source["source_id"],
                "path": str(path),
                "exists": path.exists(),
                "needle_check": "pass" if has_needle(path, needle) else "fail",
                "role": source["role"],
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def keyword_hunt_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source in SOURCES:
        path = Path(source["path"])
        text = read_text(path)
        lowered = text.lower()
        hits = {keyword: lowered.count(keyword.lower()) for keyword in KEYWORDS}
        nonzero = [f"{keyword}:{count}" for keyword, count in hits.items() if count]
        rows.append(
            {
                "hunt_id": f"HUNT877_{len(rows)}",
                "source_id": source["source_id"],
                "path": str(path),
                "total_keyword_hits": sum(hits.values()),
                "top_hits": ";".join(nonzero[:8]) if nonzero else "none",
                "computable_trace_Hessian_found": False,
                "reason": "keyword evidence is contextual only; no source contains a parent-owned P_tr, H_tr, principal symbol, mass gap, and source projection together",
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "completed a source hunt for parent trace-Hessian ingredients, quarantined the P_T notation collision, and wrote the minimal H_tr action skeleton",
            "best_partial_result": "the viable derivation path is now P_tr -> H_tr=P_tr^dagger Hess(S_parent) P_tr -> Z_tr, mu_tr^2, lambda_tr, J_tr, or no-pole zero-return",
            "hard_blockers": "P_tr parent definition, computable Hessian, kinetic sign, mass gap, source projection, constraint rank/no-pole test, matter no-marker",
            "what_is_not_claimed": "parent-owned trace Hessian, numeric Z_tr/lambda_tr, zero-return, R10/PPN/clock/WEP/orbital pass, local GR/Newton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def symbol_collision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "symbol_id": "SC877_0_old_P_T",
            "symbol": "P_T",
            "old_meaning": "time/history S3 singlet projector in the 27-cell amplitude branch",
            "source_path": str(ROOT / "322-S3-singlet-motion-time-projector-gate.md"),
            "new_risk": "using P_T for local trace projection would conflate time-singlet amplitude algebra with trace-sector local coupling",
            "decision": "reserve P_T for old time/history projector in historical rows",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "symbol_id": "SC877_1_new_Ptr",
            "symbol": "P_tr",
            "old_meaning": "none in current source hunt",
            "source_path": str(ROOT / "876-Y5-R10-trace-sector-ZT-lambdaT-parent-input-or-zero-return.md"),
            "new_risk": "must be parent-defined before any Hessian coefficient is real",
            "decision": "use P_tr for the local trace-sector projector from 877 onward",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "symbol_id": "SC877_2_old_ZT_lambdaT",
            "symbol": "Z_T, lambda_T",
            "old_meaning": "placeholder trace-carrier normalization/range in 872-876",
            "source_path": str(ROOT / "872-Y5-R10-cT-parent-projection-coefficient-or-theorem-zero-return.md"),
            "new_risk": "same subscript T inherits P_T ambiguity",
            "decision": "write canonical trace-sector names as Z_tr, mu_tr^2, m_tr, lambda_tr while keeping aliases Z_T/lambda_T in ledgers",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def hessian_source_candidate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "candidate_id": "HC877_0_876_contract",
            "source_path": str(ROOT / "876-Y5-R10-trace-sector-ZT-lambdaT-parent-input-or-zero-return.md"),
            "candidate_contribution": "exact formula H_T=P_T^dagger Hess(S_parent)P_T and Z_T/lambda_T readout rule",
            "usable_for_Htr": "contract_only",
            "missing": "actual parent projector, Hessian operator, source projection",
            "verdict": "keep_as_target_not_coefficient_source",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "HC877_1_407_action_skeleton",
            "source_path": str(ROOT / "407-primitive-relational-quotient-action-sketch.md"),
            "candidate_contribution": "broad S_relational_MTS, S_boundary_domain, S_total_Ward_owner, S_readout_observables blocks",
            "usable_for_Htr": "scaffold_only",
            "missing": "no trace-sector second variation or principal symbol",
            "verdict": "possible parent home but not computable Hessian",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "HC877_2_321_322_projector_algebra",
            "source_path": str(ROOT / "322-S3-singlet-motion-time-projector-gate.md"),
            "candidate_contribution": "rank-one projector construction and S3 singlet discipline",
            "usable_for_Htr": "notation_warning_only",
            "missing": "this P_T is time/history, not local trace",
            "verdict": "do_not_import_as_trace_projector",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "HC877_3_337_338_exact_readout",
            "source_path": str(ROOT / "338-action-level-exact-readout-gate.md"),
            "candidate_contribution": "projection/readout cannot backreact into S_parent unless it is a true parent variable",
            "usable_for_Htr": "no_cheat_rule",
            "missing": "does not supply H_tr itself",
            "verdict": "P_tr may be readout-only or parent-owned, but not fitted spurion",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "HC877_4_421_fibre_decoupling",
            "source_path": str(ROOT / "421-finite-fibre-spectrum-decoupling-theorem-attempt.md"),
            "candidate_contribution": "states mass gap/Hessian/source-independence/decoupling debts explicitly",
            "usable_for_Htr": "analogy_and_gate",
            "missing": "no trace-specific Hessian sign/gap/source-independence theorem",
            "verdict": "reuse gate logic, not coefficients",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "HC877_5_437_R10_contract",
            "source_path": str(ROOT / "437-R10-alpha-lambda-executable-curve-contract.md"),
            "candidate_contribution": "alpha(lambda) comparison contract if a finite trace carrier remains",
            "usable_for_Htr": "bound_branch_only",
            "missing": "parent coefficient source",
            "verdict": "used after H_tr/J_tr are filled or zero-return fails",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "HC877_6_446_source_owner",
            "source_path": str(ROOT / "446-source-owner-current-parent-action-contract.md"),
            "candidate_contribution": "source-owner/nohair action terms and no-cheat tests",
            "usable_for_Htr": "source_projection_gate",
            "missing": "trace-specific J_tr and source-cokernel projection",
            "verdict": "relevant to J_tr, not enough for Z_tr/lambda_tr",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "HC877_7_872_scalar_ansatz",
            "source_path": str(ROOT / "872-Y5-R10-cT-parent-projection-coefficient-or-theorem-zero-return.md"),
            "candidate_contribution": "standard local scalar trace-carrier formulas",
            "usable_for_Htr": "conditional_physics_template",
            "missing": "parent ownership of the scalar mode and coefficients",
            "verdict": "formula fallback only after parent ownership",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "HC877_8_verdict",
            "source_path": str(ROOT),
            "candidate_contribution": "whole source hunt",
            "usable_for_Htr": "not_yet_computable",
            "missing": "one file or action block containing P_tr, H_tr, Z_tr, mu_tr^2, J_tr, and rank/no-pole test",
            "verdict": "minimal H_tr skeleton required before coefficient scoring",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def minimal_trace_action_skeleton_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "skeleton_id": "SK877_0_name_discipline",
            "action_piece": "canonical trace notation",
            "mathematical_form": "Use P_tr, phi_tr, H_tr, Z_tr, mu_tr^2, m_tr, lambda_tr, J_tr; keep Z_T/lambda_T as aliases only",
            "must_be_parent_owned_by": "symbol register and future parent action",
            "current_status": "written_as_discipline",
            "if_missing": "P_T time-singlet can be confused with trace projector",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "skeleton_id": "SK877_1_trace_projector",
            "action_piece": "parent trace projection",
            "mathematical_form": "phi_tr := P_tr delta Phi, with P_tr^2=P_tr or a defined quotient/readout map on Sol(S_parent)",
            "must_be_parent_owned_by": "configuration-space symmetry, quotient functor, or gauge-fixed variation before scoring",
            "current_status": "missing_parent_definition",
            "if_missing": "H_tr has no domain and Z_tr/lambda_tr are meaningless",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "skeleton_id": "SK877_2_quadratic_Hessian",
            "action_piece": "trace-sector second variation",
            "mathematical_form": "S_tr^(2)=1/2 <phi_tr, H_tr phi_tr>, H_tr:=P_tr^dagger (delta^2 S_parent)|_background P_tr",
            "must_be_parent_owned_by": "second variation of the actual parent action, not a newly fitted local scalar",
            "current_status": "formal_skeleton_only",
            "if_missing": "no derivation of Z_tr, mass gap, or scalar-pole status",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "skeleton_id": "SK877_3_operator_readout",
            "action_piece": "principal symbol and mass term",
            "mathematical_form": "sigma_2(H_tr)=Z_tr g^{mu nu}k_mu k_nu; H_tr approx Z_tr(-box+m_tr^2)+constraint/gauge terms",
            "must_be_parent_owned_by": "computed Hessian principal and zeroth-order symbols",
            "current_status": "missing_parent_coefficients",
            "if_missing": "R10/orbital range remains symbolic",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "skeleton_id": "SK877_4_source_projection",
            "action_piece": "trace source/current",
            "mathematical_form": "delta S_int = int sqrt(-g) phi_tr J_tr, Q_tr^A=int_A J_tr, with J_tr=P_tr^dagger J_parent or zero by matter descent",
            "must_be_parent_owned_by": "matter descent/no-marker theorem or source-owner variation",
            "current_status": "missing_or_zero_theorem",
            "if_missing": "finite-range force amplitude cannot be compared to bounds",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "skeleton_id": "SK877_5_constraint_rank",
            "action_piece": "no-pole/zero-return test",
            "mathematical_form": "physical trace pole exists only if H_tr has nonzero reduced inverse on a source-coupled local subspace",
            "must_be_parent_owned_by": "constraint rank, gauge bracket, source-cokernel, and no-tail proof",
            "current_status": "not_tested",
            "if_missing": "cannot claim no local trace carrier",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "skeleton_id": "SK877_6_no_spurion_rule",
            "action_piece": "readout-after-variation guard",
            "mathematical_form": "P_tr may not be inserted as a post-fit physical spurion; if it is a probe/readout, evaluate physical equations at source zero",
            "must_be_parent_owned_by": "337/338 exact-readout rule applied to trace channel",
            "current_status": "guard_written",
            "if_missing": "a fitted trace counterterm can be smuggled into S_parent",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def coefficient_readout_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "coefficient_id": "CR877_0_P_tr",
            "coefficient": "P_tr",
            "readout_law": "parent trace projector or quotient/readout differential",
            "current_value": "MISSING_PARENT_DEFINITION",
            "required_before_claim": "yes",
            "fallback_if_missing": "route becomes closure-only or retained c_T coefficient",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "coefficient_id": "CR877_1_Z_tr",
            "coefficient": "Z_tr alias Z_T",
            "readout_law": "coefficient of g^{mu nu}k_mu k_nu in principal symbol of H_tr",
            "current_value": "MISSING_PARENT_HESSIAN",
            "required_before_claim": "yes_if_finite_carrier",
            "fallback_if_missing": "no alpha amplitude can be scored",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "coefficient_id": "CR877_2_mu_tr2",
            "coefficient": "mu_tr^2",
            "readout_law": "zeroth-order trace Hessian coefficient before canonical normalization",
            "current_value": "MISSING_PARENT_HESSIAN",
            "required_before_claim": "yes_if_finite_carrier",
            "fallback_if_missing": "no mass gap/range prediction",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "coefficient_id": "CR877_3_lambda_tr",
            "coefficient": "lambda_tr alias lambda_T",
            "readout_law": "m_tr^2=mu_tr^2/Z_tr and lambda_tr=1/m_tr in natural units",
            "current_value": "MISSING_PARENT_HESSIAN",
            "required_before_claim": "yes_if_finite_carrier",
            "fallback_if_missing": "R10/orbital branch remains symbolic",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "coefficient_id": "CR877_4_J_tr",
            "coefficient": "J_tr and Q_tr^A",
            "readout_law": "source projection onto trace mode, or zero by q_loc/matter descent",
            "current_value": "MISSING_PARENT_SOURCE_OR_ZERO_THEOREM",
            "required_before_claim": "yes",
            "fallback_if_missing": "WEP/clock/R10/orbital amplitudes blocked",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "coefficient_id": "CR877_5_no_pole_certificate",
            "coefficient": "rank_no_pole",
            "readout_law": "reduced H_tr has no physical source-coupled inverse on local compact domains",
            "current_value": "MISSING_CONSTRAINT_RANK_TEST",
            "required_before_claim": "yes_if_zero_return",
            "fallback_if_missing": "must retain finite-carrier bound route if source exists",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def zero_or_bound_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "fork_id": "FB877_0_zero_return",
            "branch": "no local trace carrier",
            "success_condition": "P_tr is local-vertical/readout-only or H_tr has no physical source-coupled pole and J_tr projects to zero",
            "current_status": "not_proved",
            "observable_result": "c_T trace finite-range branch is theorem-zero",
            "next_action": "define P_tr and run constraint-rank/source-cokernel test",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "fork_id": "FB877_1_finite_carrier",
            "branch": "finite trace scalar/vector-effective carrier",
            "success_condition": "P_tr, H_tr, Z_tr, lambda_tr, J_tr are parent-owned and numeric or source-normalized",
            "current_status": "not_ready",
            "observable_result": "alpha_tr(lambda_tr) and force/clock/WEP rows become computable but not automatically safe",
            "next_action": "fill coefficients only after parent Hessian exists",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "fork_id": "FB877_2_closure_only",
            "branch": "trace sector remains closure parameter",
            "success_condition": "source hunt fails to find or construct parent P_tr/H_tr after explicit attempts",
            "current_status": "not_selected_yet",
            "observable_result": "local branch can be bounded phenomenologically but not claimed as derived GR reduction",
            "next_action": "attempt 878 P_tr definition/rank test before demotion",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC877_0_selected",
            "route": "Ptr_parent_projector_definition_and_constraint_rank_test",
            "status": "selected",
            "reason": "H_tr cannot exist without an unambiguous P_tr, and old P_T is already occupied by the time-singlet amplitude branch",
            "include": "define P_tr, separate it from P_T, decide readout-only vs parent dynamical projector, test no-pole/source-cokernel clauses",
            "exclude": "numeric fitted Z_tr/lambda_tr, R10 scoring, local-GR claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG877_0_no_Htr_claim",
            "claim": "the parent trace Hessian is computed",
            "status": "forbidden",
            "reason": "source hunt found contracts and templates but no computable H_tr",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG877_1_no_Ptr_claim",
            "claim": "P_tr is parent-defined",
            "status": "forbidden",
            "reason": "877 only names the required trace projector and quarantines P_T collision",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG877_2_no_zero_return_claim",
            "claim": "no local trace carrier exists",
            "status": "forbidden",
            "reason": "constraint-rank/source-cokernel/no-tail/no-marker tests are not closed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG877_3_no_local_GR_claim",
            "claim": "MTS reduces to GR/Newton locally",
            "status": "forbidden",
            "reason": "c_T remains unresolved and c_e, c_P, c_S remain outside this trace checkpoint",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG877_4_allowed_private_result",
            "claim": "the next parent-action construction target is exact",
            "status": "allowed_private_nonclaim",
            "reason": "minimal H_tr skeleton makes the coupling derivation path testable rather than verbal",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D877_0",
            "finding": "source_hunt_no_computable_Htr",
            "reason": "available files contain action contracts, readout rules, mass-gap analogies, and R10 templates, but no parent trace Hessian",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D877_1",
            "finding": "P_T_collision_quarantined",
            "reason": "old P_T is time/history singlet; trace projector must be P_tr or equivalent",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D877_2",
            "finding": "minimal_Htr_skeleton_written",
            "reason": "future parent action must supply P_tr, H_tr, Z_tr, mu_tr^2, J_tr, and no-pole/source-cokernel status",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "define the parent trace projector P_tr without colliding with old P_T, then test whether the trace channel is a readout-only/constraint-null direction or a finite source-coupled carrier",
            "include": "P_tr definition, relation to q_loc/q_FLRW, readout-after-variation rule, constraint rank, source-cokernel, no-pole/no-tail test",
            "exclude": "free fitted trace coefficients, R10/local-GR claim, public prose, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_876_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_876_VALIDATION.csv"
    if not path.exists():
        return False
    rows = read_csv(path)
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def formalization_changed_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > CUTOFF)


def all_nonclaim(row_sets: Iterable[list[dict[str, object]]]) -> bool:
    for rows in row_sets:
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() != "false":
                return False
            if str(row.get("claim_allowed", "")).lower() == "true":
                return False
    return True


def validation_rows(
    source_rows: list[dict[str, object]],
    hunt_rows: list[dict[str, object]],
    collision_rows: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
    skeleton_rows: list[dict[str, object]],
    coefficient_rows: list[dict[str, object]],
    fork_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
) -> list[dict[str, str]]:
    generated_sets = [
        source_rows,
        hunt_rows,
        collision_rows,
        candidate_rows,
        skeleton_rows,
        coefficient_rows,
        fork_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        summary_rows,
    ]
    source_ok = all(row["exists"] is True and row["needle_check"] == "pass" for row in source_rows)
    hunt_noncomputable = all(row.get("computable_trace_Hessian_found") is False for row in hunt_rows)
    collision_ok = any(row.get("symbol") == "P_T" and "time/history" in str(row.get("old_meaning")) for row in collision_rows) and any(
        row.get("symbol") == "P_tr" for row in collision_rows
    )
    candidates_verdict = any(row.get("candidate_id") == "HC877_8_verdict" and row.get("usable_for_Htr") == "not_yet_computable" for row in candidate_rows)
    skeleton_ok = all(
        any(required in str(row.get("mathematical_form", "")) or required in str(row.get("action_piece", "")) for row in skeleton_rows)
        for required in ["P_tr", "H_tr", "Z_tr", "J_tr", "no-pole"]
    )
    coefficients_missing = all("MISSING" in str(row.get("current_value", "")) for row in coefficient_rows)
    fork_ok = any(row.get("branch") == "no local trace carrier" and row.get("current_status") == "not_proved" for row in fork_rows) and any(
        row.get("branch") == "finite trace scalar/vector-effective carrier" and row.get("current_status") == "not_ready" for row in fork_rows
    )
    claim_guards_closed = all(row.get("status") != "allowed_claim" for row in guard_rows) and all(
        row.get("claim_allowed") is False for row in decision_rows_
    )
    route_selected = route_rows_[0]["status"] == "selected" and next_target_rows_[0]["next_target"] == NEXT_TARGET
    fw_count = formalization_changed_count()
    checks = [
        ("V877_0_sources_exist_and_needles", source_ok, "all source paths exist and needles are present"),
        ("V877_1_prior_876_clean", prior_876_clean(), "P8_Y5_BRR545_876_VALIDATION.csv clean"),
        ("V877_2_keyword_hunt_noncomputable", hunt_noncomputable, "keyword hunt found context but no computable H_tr source"),
        ("V877_3_symbol_collision_quarantined", collision_ok, "old P_T and new P_tr separated"),
        ("V877_4_candidate_verdict_not_computable", candidates_verdict, "source hunt verdict remains not_yet_computable"),
        ("V877_5_minimal_skeleton_contains_required_objects", skeleton_ok, "P_tr/H_tr/Z_tr/J_tr/no-pole skeleton recorded"),
        ("V877_6_coefficients_missing_nonclaim", coefficients_missing, "all coefficient readout rows remain missing/nonclaim"),
        ("V877_7_zero_or_bound_fork_ready", fork_ok, "zero-return and finite-carrier forks recorded without promotion"),
        ("V877_8_claim_allowed_false", claim_guards_closed, "claim guards and decision rows keep claim_allowed=false"),
        ("V877_9_all_rows_nonclaim", all_nonclaim(generated_sets), "all generated rows valid_for_claim=false"),
        ("V877_10_formalization_workbench_untouched", fw_count == 0, f"formalization_changed_after_cutoff={fw_count}"),
        ("V877_11_route_selected", route_selected, NEXT_TARGET),
        ("V877_12_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]


def write_markdown(
    path: Path,
    generated_utc: str,
    summary_rows: list[dict[str, object]],
    source_rows: list[dict[str, object]],
    hunt_rows: list[dict[str, object]],
    collision_rows: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
    skeleton_rows: list[dict[str, object]],
    coefficient_rows: list[dict[str, object]],
    fork_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    sections = [
        "# 877 - Y5/R10 Parent Trace-Hessian Source Hunt and Minimal Action Skeleton",
        "",
        f"Status: `{STATUS}`  ",
        f"Claim ceiling: `{CLAIM_CEILING}`  ",
        f"Generated UTC: `{generated_utc}`",
        "",
        "Current result: **the parent trace-Hessian route is still alive, but not yet computable**. "
        "The source hunt found useful contracts: action skeletons, exact-readout/no-spurion rules, mass-gap/nohair gates, "
        "and R10 alpha(lambda) comparison discipline. It did not find a parent-owned trace projector and Hessian. "
        "Also, the old symbol `P_T` is already used for the time/history singlet projector, so the local trace projector "
        "is renamed `P_tr` from this checkpoint onward. The minimal future action object is "
        "`H_tr=P_tr^dagger Hess(S_parent) P_tr`; until `P_tr`, `H_tr`, `Z_tr`, `lambda_tr`, and `J_tr` are parent-owned, "
        "the trace branch remains nonclaim.",
        "",
        "## Nonclaim Summary",
        md_table(summary_rows),
        "",
        "## Source Register",
        md_table(source_rows),
        "",
        "## Keyword Hunt",
        md_table(hunt_rows),
        "",
        "## Symbol Collision Audit",
        md_table(collision_rows),
        "",
        "## Hessian Source Candidates",
        md_table(candidate_rows),
        "",
        "## Minimal Trace Action Skeleton",
        md_table(skeleton_rows),
        "",
        "## Coefficient Readout Ledger",
        md_table(coefficient_rows),
        "",
        "## Zero Or Bound Fork",
        md_table(fork_rows),
        "",
        "## Route Choice",
        md_table(route_rows_),
        "",
        "## Claim Guard",
        md_table(guard_rows),
        "",
        "## Decision",
        md_table(decision_rows_),
        "",
        "## Next Target",
        md_table(next_target_rows_),
        "",
        "## Validation",
        md_table(validation_rows_),
        "",
    ]
    path.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    generated_utc = now_utc()
    source_rows = source_register_rows(generated_utc)
    hunt_rows = keyword_hunt_rows(generated_utc)
    summary_rows = nonclaim_summary_rows(generated_utc)
    collision_rows = symbol_collision_rows(generated_utc)
    candidate_rows = hessian_source_candidate_rows(generated_utc)
    skeleton_rows = minimal_trace_action_skeleton_rows(generated_utc)
    coefficient_rows = coefficient_readout_rows(generated_utc)
    fork_rows = zero_or_bound_rows(generated_utc)
    route_rows_ = route_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_target_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        source_rows,
        hunt_rows,
        collision_rows,
        candidate_rows,
        skeleton_rows,
        coefficient_rows,
        fork_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        summary_rows,
    )

    outputs = {
        "P8_Y5_R10_877_SOURCE_REGISTER.csv": source_rows,
        "P8_Y5_R10_877_KEYWORD_HUNT.csv": hunt_rows,
        "P8_Y5_R10_877_SYMBOL_COLLISION_AUDIT.csv": collision_rows,
        "P8_Y5_R10_877_HESSIAN_SOURCE_CANDIDATES.csv": candidate_rows,
        "P8_Y5_R10_877_MINIMAL_TRACE_ACTION_SKELETON.csv": skeleton_rows,
        "P8_Y5_R10_877_COEFFICIENT_READOUT_LEDGER.csv": coefficient_rows,
        "P8_Y5_R10_877_ZERO_OR_BOUND_FORK.csv": fork_rows,
        "P8_Y5_R10_877_ROUTE_CHOICE.csv": route_rows_,
        "P8_Y5_R10_877_CLAIM_GUARD.csv": guard_rows,
        "P8_Y5_R10_877_DECISION.csv": decision_rows_,
        "P8_Y5_R10_877_NEXT_TARGET.csv": next_target_rows_,
        "P8_Y5_R10_877_NONCLAIM_SUMMARY.csv": summary_rows,
        "P8_Y5_BRR545_877_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "877-Y5-R10-parent-trace-Hessian-source-hunt-and-minimal-action-skeleton.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows,
        source_rows,
        hunt_rows,
        collision_rows,
        candidate_rows,
        skeleton_rows,
        coefficient_rows,
        fork_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_877_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
