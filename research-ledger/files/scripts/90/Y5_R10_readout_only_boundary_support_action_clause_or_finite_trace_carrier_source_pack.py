from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_887_readout_boundary_action_clause_written_not_parent_integrated_finite_trace_source_pack_staged_nonclaim"
CLAIM_CEILING = "readout_boundary_clause_and_finite_trace_source_pack_only_no_rank_zero_no_cT_zero_no_R10_PPN_or_local_GR_claim"
NEXT_TARGET = "888-Y5-R10-parent-spine-readout-clause-integration-or-finite-trace-carrier-runner.md"


SOURCE_SPECS = [
    {
        "source_id": "886_doc",
        "path": ROOT / "886-Y5-R10-Htr-zero-pole-rank-test-and-Jtr-source-cokernel-gate.md",
        "needle": "local trace zero-return route now has a real conditional theorem",
        "role": "immediate zero-pole implication handoff",
    },
    {
        "source_id": "886_validation",
        "path": OUT / "P8_Y5_BRR545_886_VALIDATION.csv",
        "needle": "V886_12_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "338_readout_gate",
        "path": ROOT / "338-action-level-exact-readout-gate.md",
        "needle": "source-at-zero != physical spurion",
        "role": "source-at-zero/no-spurion discipline",
    },
    {
        "source_id": "337_exact_readout",
        "path": ROOT / "337-exact-parent-pullback-selection-rule-gate.md",
        "needle": "Projection is applied only to observables/current readout.",
        "role": "exact parent readout rule",
    },
    {
        "source_id": "874_verticality",
        "path": ROOT / "874-Y5-R10-parent-qloc-verticality-signature-or-cT-coefficient-fill.md",
        "needle": "q_loc[U] is a compact-domain restriction/jet quotient",
        "role": "compact local quotient clause",
    },
    {
        "source_id": "870_nohair",
        "path": ROOT / "870-Y5-R10-P_loc-Jtrace-nohair-zero-theorem-or-bound.md",
        "needle": "support(J_trace) is only FLRW zero-mode/global boundary support",
        "role": "boundary support/no-tail debt",
    },
    {
        "source_id": "873_trace_charge_zero",
        "path": ROOT / "873-Y5-R10-local-matter-trace-charge-zero-theorem-or-coefficient-fill.md",
        "needle": "Q_T^A=0 follows by chain rule",
        "role": "matter descent/source zero lemma",
    },
    {
        "source_id": "875_ct_gate",
        "path": ROOT / "875-Y5-R10-cT-coefficient-fill-minimal-runner-and-claim-gate.md",
        "needle": "the c_T testing gate exists and every local claim is blocked for the right reason",
        "role": "coefficient-fill fallback gate",
    },
    {
        "source_id": "437_R10_contract",
        "path": ROOT / "437-R10-alpha-lambda-executable-curve-contract.md",
        "needle": "Anything else remains symbolic and blocks R10 promotion.",
        "role": "finite-carrier R10 curve contract",
    },
    {
        "source_id": "446_no_cheat",
        "path": ROOT / "446-source-owner-current-parent-action-contract.md",
        "needle": "readout variables enter only after variation and cannot backreact",
        "role": "readout/no-cheat action policy",
    },
    {
        "source_id": "878_projector",
        "path": ROOT / "878-Y5-R10-Ptr-parent-projector-definition-and-constraint-rank-test.md",
        "needle": "`P_tr` is now a precise parent-geometry object",
        "role": "P_tr formal object and rank gate",
    },
    {
        "source_id": "885_htr_fill",
        "path": OUT / "P8_Y5_R10_885_HTR_ZERO_POLE_SOURCE_FILL.csv",
        "needle": "HZ885_5_bound_branch",
        "role": "finite trace branch precursor",
    },
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
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: stringify(row.get(field, "")) for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def has_needle(path: Path, needle: str) -> bool:
    return path.exists() and needle in read_text(path)


def md_table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(stringify(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = Path(spec["path"])
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": path,
                "exists": path.exists(),
                "needle_check": "pass" if has_needle(path, str(spec["needle"])) else "fail",
                "role": spec["role"],
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
            "what_changed": "wrote the exact readout-only/boundary-support parent clause P_tr would need and staged the finite trace carrier source pack if that clause cannot be integrated",
            "best_partial_result": "a consistent local-zero clause now exists: P_tr is a post-variation source-at-zero readout R_tr on Sol(S_parent), boundary-supported and absent from compact q_loc variations; if parent-integrated, 886 rank-zero/no-pole/source-cokernel theorem can fire",
            "hard_blockers": "the clause is not yet integrated into the parent spine, boundary no-tail/support is not proved, q_loc compact restriction remains a contract, matter no-marker descent is unsigned, finite-carrier coefficients remain missing",
            "what_is_not_claimed": "P_tr readout-only status, rank-zero, no H_tr pole, J_tr=0, c_T=0, R10/PPN/WEP/clock/orbital pass, local GR/Newton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def readout_boundary_clause_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "clause_id": "RO887_0_parent_split",
            "required_clause": "the parent equations are varied before trace readout is applied",
            "mathematical_form": "S_parent[Phi,Psi]=S_dyn[Phi,Psi]+S_boundary[class data]; R_tr:Sol(S_parent)->Q_trace/Q_* is an observable map, not a local action field",
            "current_status": "contract_written_not_parent_integrated",
            "if_signed": "P_tr is not a local spurion and cannot create local force terms by variation",
            "if_failed": "P_tr may be a real trace carrier and finite-source rows activate",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "RO887_1_source_at_zero",
            "required_clause": "any trace probe source is set to zero before physical field equations are claimed",
            "mathematical_form": "Z[s_tr]=int exp(iS_parent+i s_tr R_tr); physical equations use delta S_parent/delta Phi at s_tr=0",
            "current_status": "supported_by_338_shape_not_trace_parent_signed",
            "if_signed": "exact readout can measure q_trace without shifting local background",
            "if_failed": "s_tr is a physical spurion/counterterm and the amplitude is closure/fitted",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "RO887_2_boundary_support",
            "required_clause": "the trace readout direction has only boundary/FLRW support",
            "mathematical_form": "supp(v_tr) subset partialD_FLRW or relative class; for compact U, j^k v_tr|_U=0 modulo gauge/exact representatives",
            "current_status": "not_parent_signed",
            "if_signed": "rank(P_loc P_tr P_loc^dagger)=0 follows by 886",
            "if_failed": "boundary tail or local conformal trace scalar remains legal",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "RO887_3_q_loc_exclusion",
            "required_clause": "compact q_loc excludes global endpoint/readout class data",
            "mathematical_form": "q_loc[U](Phi)=[j^k Phi|_U]_gauge and Dq_loc[U][v_tr]=0 for U away from cosmological boundary",
            "current_status": "contract_only",
            "if_signed": "local rods/clocks/matter cannot see Q_trace through q_loc",
            "if_failed": "Q_trace is part of local observed geometry and must be bounded",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "RO887_4_no_tail_flux",
            "required_clause": "boundary/exact trace current has no compact local tail or flux",
            "mathematical_form": "P_loc J_trace=0 and P_loc dB_trace=0; no local scalar gradient, vector B_0i, or tensor B_TF survives",
            "current_status": "open_nohair_clause",
            "if_signed": "readout-only boundary support is stable under integration by parts",
            "if_failed": "tail/leakage maps to retained c_T residual vector",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "RO887_5_matter_no_marker",
            "required_clause": "ordinary matter descends through q_loc and constants carry no trace marker",
            "mathematical_form": "S_matter=Sbar[q_loc(Phi),Psi,theta] with partial_{v_tr} theta=0",
            "current_status": "not_parent_signed",
            "if_signed": "J_tr source-cokernel vanishes by 873/886 chain rule",
            "if_failed": "WEP/clock/EM/source-charge coefficients must be filled",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "RO887_6_clause_verdict",
            "required_clause": "RO887_0 through RO887_5 are integrated into the parent spine",
            "mathematical_form": "readout-only + boundary support + q_loc exclusion + no-tail + matter no-marker",
            "current_status": "not_parent_integrated",
            "if_signed": "886 zero-pole theorem can promote the trace branch to theorem-zero in a later checkpoint",
            "if_failed": "finite trace carrier source pack becomes mandatory",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def readout_variation_test_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "test_id": "RVT887_0_variation_order",
            "test": "variation before readout",
            "pass_condition": "delta(S_parent+s_tr R_tr)/delta Phi evaluated at s_tr=0 equals delta S_parent/delta Phi",
            "current_status": "conditional_pass_if_source_at_zero_signed",
            "failure_mode": "readout source is physical and shifts the parent equations",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "test_id": "RVT887_1_local_matrix_elements",
            "test": "local compact support matrix elements vanish",
            "pass_condition": "<eta_U,P_tr zeta_U>=0 for all compact local eta_U,zeta_U after gauge/exact quotient",
            "current_status": "not_tested_parent_Ptr_missing",
            "failure_mode": "rank-one local trace carrier survives",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "test_id": "RVT887_2_boundary_no_flux",
            "test": "no boundary/exact local flux",
            "pass_condition": "integral_partialU B_trace=0 and P_loc dB_trace=0 for lab/solar compact U",
            "current_status": "not_parent_signed",
            "failure_mode": "tail/current leakage creates c_T residual",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "test_id": "RVT887_3_no_marker_matter",
            "test": "matter constants and response have no trace marker",
            "pass_condition": "partial_{v_tr} theta_A=0 and all matter geometry stack layers factor through q_loc",
            "current_status": "not_parent_signed",
            "failure_mode": "WEP/clock/species channels activate",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "test_id": "RVT887_4_integration_verdict",
            "test": "readout boundary clause is parent-integrated",
            "pass_condition": "RVT887_0 through RVT887_3 all close from one parent action/spine",
            "current_status": "fail_for_claim",
            "failure_mode": "finite carrier source pack remains the honest branch",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def finite_trace_source_pack_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "pack_id": "FT887_0_Ptr_Htr",
            "quantity": "P_tr and H_tr",
            "formula_or_schema": "H_tr=P_tr^dagger Hess(S_parent) P_tr",
            "needed_for": "deciding finite carrier versus zero-return",
            "current_status": "MISSING_PARENT_PROJECTOR_HESSIAN",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "FT887_1_Ztr_lambda",
            "quantity": "Z_tr, mu_tr^2, lambda_tr",
            "formula_or_schema": "sigma_2(H_tr)=Z_tr g^{mu nu}k_mu k_nu; m_tr^2=mu_tr^2/Z_tr; lambda_tr=1/m_tr",
            "needed_for": "R10/orbital finite-range shape",
            "current_status": "MISSING_PARENT_SYMBOLS",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "FT887_2_Jtr_Qtr",
            "quantity": "J_tr and Q_tr^A/m_A",
            "formula_or_schema": "J_tr=P_tr^dagger J_parent; Q_tr^A=int_A J_tr",
            "needed_for": "R10, WEP, clocks, orbital source/test amplitudes",
            "current_status": "MISSING_SOURCE_PROJECTION_OR_ZERO_THEOREM",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "FT887_3_R10_alpha_curve",
            "quantity": "alpha_tr(lambda_tr)",
            "formula_or_schema": "alpha_tr_AB=(Q_tr^A/m_A)(Q_tr^B/m_B)/(4*pi Z_tr G_obs) with matching alpha(lambda) bound curve",
            "needed_for": "short-range/fifth-force comparison",
            "current_status": "MISSING_COEFFICIENTS_AND_FULL_BOUND_CURVE",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "FT887_4_PPN_response",
            "quantity": "C_T_gamma and C_T_beta",
            "formula_or_schema": "gamma-1=C_T_gamma c_T, beta-1=C_T_beta c_T or equivalent weak-field response",
            "needed_for": "solar-system PPN comparison",
            "current_status": "MISSING_RESPONSE_OPERATOR",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "FT887_5_clock_WEP_response",
            "quantity": "clock trace response and species differential charge",
            "formula_or_schema": "delta nu_i/nu_i=C_T_clock_i c_T; eta_AB from Delta(Q_tr/m)_AB",
            "needed_for": "clock/redshift/WEP channels",
            "current_status": "MISSING_NO_MARKER_OR_COEFFICIENTS",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "FT887_6_orbital_GM_response",
            "quantity": "orbital acceleration and measured-GM absorption",
            "formula_or_schema": "delta a/a_N=alpha_tr(1+r/lambda_tr)exp(-r/lambda_tr) unless constant universal GM absorption is proved",
            "needed_for": "orbital/binary/Newtonian source normalization",
            "current_status": "MISSING_ORBITAL_BOUND_AND_GM_ABSORPTION",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "FT887_7_source_provenance",
            "quantity": "source paths and units for all finite-carrier rows",
            "formula_or_schema": "each row needs source_file, units, derivation_status, assumptions, valid_for_claim=false until numeric/sourced",
            "needed_for": "preventing symbolic local-GR/R10 promotion",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def fork_decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "fork_id": "FD887_0_if_clause_integrates",
            "condition": "readout-only boundary-support clause is parent-integrated",
            "result": "P_tr rank-zero premises can be promoted for trace branch in a later checkpoint",
            "claim_policy": "still not full local GR until other q_loc/source-normalization channels close",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "fork_id": "FD887_1_if_clause_fails",
            "condition": "P_tr has local support, physical source, tail, or matter marker",
            "result": "finite trace carrier source pack is mandatory",
            "claim_policy": "no R10/PPN/clock/orbital pass until numeric sourced rows exist and compare cleanly",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "fork_id": "FD887_2_current_verdict",
            "condition": "current corpus after 887",
            "result": "clause written but not parent-integrated; finite source pack staged with missing markers",
            "claim_policy": "nonclaim only",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def promotion_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "PG887_0_readout_only",
            "promotion_target": "P_tr is a readout-only source-at-zero boundary observable",
            "required_to_pass": "RO887_0 through RO887_5 integrated into parent spine",
            "current_evidence": "contract written, not parent-integrated",
            "gate_result": "fail_for_claim",
            "next_action": "try parent-spine integration in 888",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG887_1_rank_zero",
            "promotion_target": "local trace rank is zero",
            "required_to_pass": "readout-only boundary support plus compact q_loc/no-tail",
            "current_evidence": "conditional from 886",
            "gate_result": "fail_for_claim",
            "next_action": "do not claim c_T=0 yet",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG887_2_finite_pack_claim",
            "promotion_target": "finite trace carrier is bounded/passed",
            "required_to_pass": "numeric sourced Z_tr, lambda_tr, Q_tr/m, responses, and bound curves",
            "current_evidence": "schema staged with missing markers",
            "gate_result": "fail_for_claim",
            "next_action": "runner only after readout clause fails or source values exist",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG887_3_local_GR",
            "promotion_target": "local GR/Newton is derived",
            "required_to_pass": "trace branch closed plus all other local residual/source-normalization branches closed",
            "current_evidence": "trace branch still nonclaim; broader local stack open",
            "gate_result": "fail_for_claim",
            "next_action": "keep local GR gate blocked",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC887_0_selected",
            "route": "parent_spine_readout_clause_integration_or_finite_trace_carrier_runner",
            "status": "selected",
            "reason": "the exact readout-only clause is now written; the next real decision is whether it can be integrated into the parent spine, otherwise finite-carrier testing must begin",
            "include": "parent spine insertion test, source-at-zero/no-spurion check, boundary support/no-tail, q_loc exclusion, finite-carrier runner skeleton",
            "exclude": "rank-zero claim, c_T zero claim, local-GR/Newton pass, R10/PPN pass, GitHub action, formalization-workbench edits",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG887_0_no_readout_claim",
            "forbidden_claim": "P_tr is proven readout-only",
            "status": "forbidden",
            "reason": "887 writes the clause but does not integrate it into a parent action/spine",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG887_1_no_cT_zero_claim",
            "forbidden_claim": "c_T=0 or trace zero-return is derived",
            "status": "forbidden",
            "reason": "rank-zero/no-pole/source-cokernel premises remain unsigned",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG887_2_no_finite_pass_claim",
            "forbidden_claim": "finite trace carrier passes local tests",
            "status": "forbidden",
            "reason": "finite-carrier source pack has missing parent coefficients and bound inputs",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG887_3_no_local_GR_claim",
            "forbidden_claim": "local GR/Newton follows",
            "status": "forbidden",
            "reason": "trace branch and broader q_loc/source-normalization branches are not closed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG887_4_allowed_private_result",
            "forbidden_claim": "none",
            "status": "allowed_private_nonclaim",
            "reason": "887 cleanly separates the derivation route from the finite-carrier bound route",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D887_0",
            "finding": "readout_boundary_clause_written",
            "reason": "the exact parent clause needed to make P_tr source-at-zero and boundary-supported is now explicit",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D887_1",
            "finding": "not_parent_integrated",
            "reason": "no current parent spine/action file signs RO887_0 through RO887_5 jointly",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D887_2",
            "finding": "finite_source_pack_staged",
            "reason": "if readout-only integration fails, all finite-carrier quantities and arenas are queued with missing markers",
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
            "objective": "try to integrate the readout-only boundary-support clause into the parent spine; if it cannot be integrated, build a finite trace carrier runner from the staged source pack",
            "include": "parent-spine consistency, source-at-zero check, boundary/no-tail proof pressure, finite-carrier schema-to-runner conversion",
            "exclude": "public claim, fitted coupling, R10/local-GR pass, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_886_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_886_VALIDATION.csv"
    return path.exists() and all(row.get("result") == "pass" for row in read_csv(path))


def formalization_changed_count() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime)
            if modified > CUTOFF:
                count += 1
    return count


def all_nonclaim(row_groups: Iterable[list[dict[str, object]]]) -> bool:
    for rows in row_groups:
        for row in rows:
            if stringify(row.get("valid_for_claim", False)) != "false":
                return False
    return True


def validation_rows(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    clause_rows: list[dict[str, object]],
    variation_rows: list[dict[str, object]],
    source_pack_rows: list[dict[str, object]],
    fork_rows: list[dict[str, object]],
    promotion_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    clause_ids = {row["clause_id"] for row in clause_rows}
    source_pack_statuses = [str(row["current_status"]) for row in source_pack_rows]
    row_groups = [
        source_rows,
        clause_rows,
        variation_rows,
        source_pack_rows,
        fork_rows,
        promotion_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        summary_rows,
    ]
    checks = [
        {
            "check_id": "V887_0_sources_exist_and_needles",
            "result": "pass" if all(row["exists"] and row["needle_check"] == "pass" for row in source_rows) else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V887_1_prior_886_clean",
            "result": "pass" if prior_886_clean() else "fail",
            "detail": "P8_Y5_BRR545_886_VALIDATION.csv clean",
        },
        {
            "check_id": "V887_2_readout_clause_complete",
            "result": "pass" if {"RO887_0_parent_split", "RO887_1_source_at_zero", "RO887_2_boundary_support", "RO887_3_q_loc_exclusion", "RO887_4_no_tail_flux", "RO887_5_matter_no_marker", "RO887_6_clause_verdict"}.issubset(clause_ids) else "fail",
            "detail": "readout-only boundary-support clause rows present",
        },
        {
            "check_id": "V887_3_readout_not_promoted",
            "result": "pass" if any(row["clause_id"] == "RO887_6_clause_verdict" and row["current_status"] == "not_parent_integrated" for row in clause_rows) else "fail",
            "detail": "readout clause remains not parent-integrated",
        },
        {
            "check_id": "V887_4_variation_tests_block_claim",
            "result": "pass" if variation_rows and any(row["test_id"] == "RVT887_4_integration_verdict" and row["current_status"] == "fail_for_claim" for row in variation_rows) else "fail",
            "detail": "variation/readout tests do not promote claim",
        },
        {
            "check_id": "V887_5_finite_source_pack_staged",
            "result": "pass" if len(source_pack_rows) >= 8 and all("MISSING" in status or "SCHEMA_READY" in status for status in source_pack_statuses) else "fail",
            "detail": "finite trace source pack rows staged with missing markers",
        },
        {
            "check_id": "V887_6_fork_decision_nonclaim",
            "result": "pass" if fork_rows and all(row["valid_for_claim"] is False for row in fork_rows) else "fail",
            "detail": "fork decision rows remain nonclaim",
        },
        {
            "check_id": "V887_7_promotion_gates_blocked",
            "result": "pass" if promotion_rows and all(row["gate_result"] == "fail_for_claim" for row in promotion_rows) else "fail",
            "detail": "all promotion gates fail for claim",
        },
        {
            "check_id": "V887_8_claim_allowed_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in decision_rows_) else "fail",
            "detail": "decision rows keep claim_allowed=false",
        },
        {
            "check_id": "V887_9_all_rows_nonclaim",
            "result": "pass" if all_nonclaim(row_groups) else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V887_10_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V887_11_route_selected",
            "result": "pass" if route_rows_ and next_target_rows_ and next_target_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V887_12_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]
    return [{**row, "generated_utc": generated_utc} for row in checks]


def write_markdown(
    path: Path,
    generated_utc: str,
    summary_rows: list[dict[str, object]],
    source_rows: list[dict[str, object]],
    clause_rows: list[dict[str, object]],
    variation_rows: list[dict[str, object]],
    source_pack_rows: list[dict[str, object]],
    fork_rows: list[dict[str, object]],
    promotion_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    lines = [
        "# 887 - Y5/R10 Readout-Only Boundary-Support Action Clause or Finite Trace Carrier Source Pack",
        "",
        f"Status: `{STATUS}`  ",
        f"Claim ceiling: `{CLAIM_CEILING}`  ",
        f"Generated UTC: `{generated_utc}`",
        "",
        "Current result: **the clean local-GR route has been narrowed to one parent-spine clause**. `P_tr` must be a post-variation, source-at-zero boundary readout `R_tr:Sol(S_parent)->Q_trace/Q_*`, absent from compact `q_loc` variations and protected by no-tail/no-marker conditions. If that clause is truly parent-integrated, the 886 rank-zero/no-pole/source-cokernel theorem can fire. It is not integrated yet, so the finite trace carrier source pack is staged with every coefficient still missing and nonclaim.",
        "",
        "## Nonclaim Summary",
        md_table(summary_rows),
        "",
        "## Source Register",
        md_table(source_rows),
        "",
        "## Readout Boundary Clause",
        md_table(clause_rows),
        "",
        "## Readout Variation Tests",
        md_table(variation_rows),
        "",
        "## Finite Trace Source Pack",
        md_table(source_pack_rows),
        "",
        "## Fork Decision",
        md_table(fork_rows),
        "",
        "## Promotion Gates",
        md_table(promotion_rows),
        "",
        "## Route Choice",
        md_table(route_rows_),
        "",
        "## Claim Guards",
        md_table(guard_rows),
        "",
        "## Decisions",
        md_table(decision_rows_),
        "",
        "## Next Target",
        md_table(next_target_rows_),
        "",
        "## Validation",
        md_table(validation_rows_),
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    generated_utc = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows(generated_utc)
    summary_rows = nonclaim_summary_rows(generated_utc)
    clause_rows = readout_boundary_clause_rows(generated_utc)
    variation_rows = readout_variation_test_rows(generated_utc)
    source_pack_rows = finite_trace_source_pack_rows(generated_utc)
    fork_rows = fork_decision_rows(generated_utc)
    promotion_rows = promotion_gate_rows(generated_utc)
    route_rows_ = route_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_target_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows,
        clause_rows,
        variation_rows,
        source_pack_rows,
        fork_rows,
        promotion_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        summary_rows,
    )

    outputs = {
        "P8_Y5_R10_887_SOURCE_REGISTER.csv": source_rows,
        "P8_Y5_R10_887_READOUT_BOUNDARY_CLAUSE.csv": clause_rows,
        "P8_Y5_R10_887_READOUT_VARIATION_TESTS.csv": variation_rows,
        "P8_Y5_R10_887_FINITE_TRACE_SOURCE_PACK.csv": source_pack_rows,
        "P8_Y5_R10_887_FORK_DECISION.csv": fork_rows,
        "P8_Y5_R10_887_PROMOTION_GATE.csv": promotion_rows,
        "P8_Y5_R10_887_ROUTE_CHOICE.csv": route_rows_,
        "P8_Y5_R10_887_CLAIM_GUARD.csv": guard_rows,
        "P8_Y5_R10_887_DECISION.csv": decision_rows_,
        "P8_Y5_R10_887_NEXT_TARGET.csv": next_target_rows_,
        "P8_Y5_R10_887_NONCLAIM_SUMMARY.csv": summary_rows,
        "P8_Y5_BRR545_887_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "887-Y5-R10-readout-only-boundary-support-action-clause-or-finite-trace-carrier-source-pack.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows,
        source_rows,
        clause_rows,
        variation_rows,
        source_pack_rows,
        fork_rows,
        promotion_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_887_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
