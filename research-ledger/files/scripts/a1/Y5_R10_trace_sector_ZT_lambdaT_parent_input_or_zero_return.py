from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

STATUS = "Y5_R10_876_trace_sector_Hessian_contract_written_ZT_lambdaT_not_parent_filled_zero_return_not_proved_nonclaim"
CLAIM_CEILING = "trace_sector_quadratic_contract_only_no_numeric_ZT_lambdaT_no_zero_return_no_R10_PPN_WEP_or_local_GR_claim"
NEXT_TARGET = "877-Y5-R10-parent-trace-Hessian-source-hunt-and-minimal-action-skeleton.md"


SOURCES = [
    {
        "source_id": "875_doc",
        "path": ROOT / "875-Y5-R10-cT-coefficient-fill-minimal-runner-and-claim-gate.md",
        "needle": "the c_T testing gate exists",
        "role": "immediate handoff: Z_T/lambda_T gate",
    },
    {
        "source_id": "875_validation",
        "path": OUT / "P8_Y5_BRR545_875_VALIDATION.csv",
        "needle": "V875_10_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "874_verticality",
        "path": ROOT / "874-Y5-R10-parent-qloc-verticality-signature-or-cT-coefficient-fill.md",
        "needle": "c_T Coefficient Fill Ledger",
        "role": "missing Z_T/lambda_T ledger",
    },
    {
        "source_id": "872_projection",
        "path": ROOT / "872-Y5-R10-cT-parent-projection-coefficient-or-theorem-zero-return.md",
        "needle": "S_T^loc",
        "role": "conditional local trace carrier projection",
    },
    {
        "source_id": "870_nohair",
        "path": ROOT / "870-Y5-R10-P_loc-Jtrace-nohair-zero-theorem-or-bound.md",
        "needle": "P_loc J_trace=0",
        "role": "zero-return/no-hair source",
    },
    {
        "source_id": "864_split",
        "path": ROOT / "864-Y5-R10-local-global-quotient-split-and-endpoint-stationarity-parent-clause.md",
        "needle": "Dq_loc[U][v_T]=0",
        "role": "local/global quotient split condition",
    },
    {
        "source_id": "407_action_sketch",
        "path": ROOT / "407-primitive-relational-quotient-action-sketch.md",
        "needle": "Action Skeleton",
        "role": "candidate parent-action skeleton",
    },
    {
        "source_id": "869_residual_vector",
        "path": ROOT / "869-Y5-R10-q_loc-residual-vector-decomposition-or-zero-theorem.md",
        "needle": "q_loc Residual Vector Decomposition",
        "role": "trace/coframe/projector/source residual context",
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
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def has_needle(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


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


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "wrote the exact parent trace-sector Hessian contract needed to own Z_T, m_T, lambda_T, and zero-return",
            "best_partial_result": "Z_T and lambda_T are no longer vague couplings: they are the principal and mass/range data of H_T=P_T^dagger Hess(S_parent) P_T",
            "hard_blockers": "explicit parent Hessian, trace projector P_T, source projection J_T, kinetic sign, mass gap/range, no-local-pole certificate",
            "what_is_not_claimed": "numeric Z_T, numeric lambda_T, no local trace carrier, R10 pass, PPN pass, clock/WEP pass, orbital pass, local GR/Newton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def trace_sector_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "contract_id": "QTC876_0_parent_mode",
            "required_object": "trace fluctuation phi_T",
            "mathematical_form": "phi_T := P_T delta Phi, where P_T is a parent-owned trace/local projection and not a fitted test scalar",
            "if_signed": "local trace carrier is an actual parent degree/readout branch",
            "current_status": "projection_not_parent_defined",
            "blocker": "P_T and local trace support class are not derived from the parent configuration space",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "QTC876_1_Hessian_operator",
            "required_object": "quadratic trace operator H_T",
            "mathematical_form": "H_T := P_T^dagger (delta^2 S_parent/dPhi^2)|_background P_T",
            "if_signed": "Z_T and m_T can be read from the parent Hessian rather than chosen",
            "current_status": "formal_contract_written",
            "blocker": "no explicit parent Hessian has been extracted for the local trace channel",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "QTC876_2_kinetic_normalization",
            "required_object": "Z_T",
            "mathematical_form": "principal_symbol(H_T) = Z_T g^{mu nu} k_mu k_nu on the scalar trace subspace",
            "if_signed": "Z_T>0 gives a non-ghost local scalar normalization; Z_T=0 pushes to constraint/gauge zero-return",
            "current_status": "missing_parent_input",
            "blocker": "principal symbol of the trace Hessian is not known",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "QTC876_3_mass_range",
            "required_object": "m_T and lambda_T",
            "mathematical_form": "H_T approx Z_T(-box + m_T^2); lambda_T=1/m_T in natural units or hbar/(m_T c) in SI",
            "if_signed": "R10/orbital range becomes a prediction or a proved non-propagating limit",
            "current_status": "missing_parent_input",
            "blocker": "trace-sector zeroth-order Hessian coefficient/mass gap is not derived",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "QTC876_4_source_projection",
            "required_object": "J_T and Q_T",
            "mathematical_form": "delta S_int = integral sqrt(-g) phi_T J_T; Q_T^A = integral_A J_T",
            "if_signed": "alpha_T and WEP/clock charges become computable or vanish if J_T=0",
            "current_status": "missing_parent_input_or_zero_theorem",
            "blocker": "matter descent/no-marker and boundary current projection remain unsigned",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "QTC876_5_claim_rule",
            "required_object": "claim promotion rule",
            "mathematical_form": "claim allowed only if H_T, P_T, J_T, Z_T, m_T/lambda_T, and source paths are parent-owned and numeric, or if zero-return clauses all close",
            "if_signed": "local trace branch can be scored without free coupling smuggling",
            "current_status": "rule_written",
            "blocker": "current rows satisfy neither numeric-coefficient branch nor theorem-zero branch",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def derivation_attempt_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "attempt_id": "DA876_0_Hessian_extraction",
            "attempt": "expand the parent action to second order around a local background and project onto phi_T",
            "formal_result": "delta^2 S_parent[phi_T]/2 = 1/2 integral sqrt(-g) phi_T H_T phi_T",
            "status": "valid_formal_derivation",
            "not_promoted_because": "S_parent and P_T are not explicit enough to compute H_T",
            "output": "H_T contract, not numeric Z_T/m_T",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "DA876_1_ZT_readout",
            "attempt": "read kinetic normalization from the principal symbol of H_T",
            "formal_result": "Z_T = coefficient of g^{mu nu} k_mu k_nu in sigma_2(H_T) after canonical trace projection",
            "status": "formula_ready_parent_input_missing",
            "not_promoted_because": "the trace-sector principal symbol is not present in the corpus",
            "output": "Z_T remains MISSING_PARENT_HESSIAN",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "DA876_2_lambda_readout",
            "attempt": "read range from the trace-sector mass gap",
            "formal_result": "m_T^2 = mu_T^2/Z_T and lambda_T = 1/m_T, provided Z_T>0 and m_T^2>0",
            "status": "formula_ready_parent_input_missing",
            "not_promoted_because": "mu_T^2 and Z_T are not parent-computed",
            "output": "lambda_T remains MISSING_PARENT_HESSIAN",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "DA876_3_zero_return_branch",
            "attempt": "test whether the local trace sector has no propagating scalar pole",
            "formal_result": "if H_T is gauge/constraint-only and J_T has zero projection on its physical cokernel, phi_T has no local force Green function",
            "status": "conditional_zero_return",
            "not_promoted_because": "constraint rank, gauge bracket, and source-cokernel projection are not proven",
            "output": "zero-return branch remains open, not claimed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "DA876_4_finite_carrier_branch",
            "attempt": "retain a finite local trace carrier if H_T has a physical pole and J_T is nonzero",
            "formal_result": "phi_T(r)=Q_T exp(-m_T r)/(4*pi*Z_T*r); alpha_T_AB=Q_T^A Q_T^B/(4*pi Z_T G_obs m_A m_B)",
            "status": "conditional_bound_branch",
            "not_promoted_because": "Z_T, m_T, Q_T, and full R10 curve are not claim-ready",
            "output": "bound branch remains schema-only",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "DA876_5_verdict",
            "attempt": "derive or reject Z_T/lambda_T now",
            "formal_result": "the exact extraction equations are known, but the parent Hessian data are absent",
            "status": "not_derived",
            "not_promoted_because": "current corpus has action sketches and contracts, not a computable trace Hessian",
            "output": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def zero_return_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "zero_id": "ZR876_0_trace_support",
            "required_clause": "v_T is boundary/FLRW support only, not a compact local field",
            "mathematical_test": "j^k(v_T)|_U=0 or pure local gauge for every compact lab/solar-system U",
            "current_status": "not_parent_signed",
            "if_signed": "P_T has no local compact support and phi_T is not a local force carrier",
            "if_failed": "finite-range trace carrier branch activates",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "ZR876_1_no_scalar_pole",
            "required_clause": "H_T has no physical scalar pole in the local spectrum",
            "mathematical_test": "rank/constraint analysis removes trace pole from the reduced Green function",
            "current_status": "not_tested",
            "if_signed": "lambda_T is not a physical local range because there is no propagator",
            "if_failed": "derive Z_T and m_T then score bounds",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "ZR876_2_source_cokernel_silence",
            "required_clause": "J_T has zero projection onto any physical local trace cokernel",
            "mathematical_test": "<u_T,J_T>=0 for all physical homogeneous trace modes u_T",
            "current_status": "not_parent_signed",
            "if_signed": "no local trace force even if a formal constrained variable exists",
            "if_failed": "local matter/source charge Q_T must be filled or bounded",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "ZR876_3_exact_current_no_tail",
            "required_clause": "boundary/exact trace currents have no local tail or relative cohomology flux",
            "mathematical_test": "P_loc dB_trace|_U=0 and no B_0i/B_TF/scalar-gradient hair",
            "current_status": "open_from_870",
            "if_signed": "endpoint trace memory cannot leak into R10/PPN/orbital/clock arenas",
            "if_failed": "c_T remains a retained residual channel",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "ZR876_4_matter_no_marker",
            "required_clause": "local matter constants and geometry stack do not carry trace markers",
            "mathematical_test": "S_matter=Sbar[Obs_loc(q_loc(Phi)),psi,theta] with partial_{v_T} theta=0",
            "current_status": "not_parent_signed",
            "if_signed": "Q_T^A=0 by the 873 chain-rule theorem",
            "if_failed": "WEP/clock/species trace charges must be bounded",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "ZR876_5_verdict",
            "required_clause": "all zero-return clauses close jointly",
            "mathematical_test": "no support + no pole + no source projection + no tail + no marker",
            "current_status": "not_proved",
            "if_signed": "set local trace branch to theorem-zero and return to other q_loc channels",
            "if_failed": "fill the Hessian/source coefficients and test against local data",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def parent_input_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "input_id": "PI876_0_P_T",
            "input": "P_T",
            "meaning": "parent trace projection from delta Phi to phi_T",
            "needed_for": "defining H_T and deciding local support",
            "current_value": "MISSING_PARENT_PROJECTOR",
            "units": "operator",
            "status": "missing",
            "source_path": str(ROOT / "407-primitive-relational-quotient-action-sketch.md"),
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "input_id": "PI876_1_H_T",
            "input": "H_T",
            "meaning": "projected parent Hessian P_T^dagger delta^2S P_T",
            "needed_for": "Z_T, mass gap, pole/constraint test",
            "current_value": "MISSING_PARENT_HESSIAN",
            "units": "action_second_variation",
            "status": "missing",
            "source_path": str(ROOT / "407-primitive-relational-quotient-action-sketch.md"),
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "input_id": "PI876_2_Z_T",
            "input": "Z_T",
            "meaning": "trace carrier kinetic normalization",
            "needed_for": "R10/orbital alpha amplitude and ghost check",
            "current_value": "MISSING_PARENT_HESSIAN",
            "units": "parent_defined",
            "status": "missing",
            "source_path": str(OUT / "P8_Y5_R10_875_CT_INPUT_SCHEMA.csv"),
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "input_id": "PI876_3_mu_T2",
            "input": "mu_T^2",
            "meaning": "trace-sector zeroth-order Hessian coefficient before canonical normalization",
            "needed_for": "m_T^2=mu_T^2/Z_T",
            "current_value": "MISSING_PARENT_HESSIAN",
            "units": "parent_defined_mass_squared_times_Z",
            "status": "missing",
            "source_path": str(OUT / "P8_Y5_R10_875_CT_INPUT_SCHEMA.csv"),
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "input_id": "PI876_4_lambda_T",
            "input": "lambda_T",
            "meaning": "finite local trace range if m_T^2>0",
            "needed_for": "R10 interpolation and orbital force profile",
            "current_value": "MISSING_PARENT_HESSIAN",
            "units": "length",
            "status": "missing",
            "source_path": str(OUT / "P8_Y5_R10_875_CT_INPUT_SCHEMA.csv"),
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "input_id": "PI876_5_J_T",
            "input": "J_T",
            "meaning": "source projection coupled to phi_T",
            "needed_for": "Q_T/m and all local force/clock/WEP amplitudes",
            "current_value": "MISSING_PARENT_SOURCE_PROJECTION_OR_ZERO_THEOREM",
            "units": "source_density_parent_defined",
            "status": "missing_or_zero_return",
            "source_path": str(ROOT / "873-Y5-R10-local-matter-trace-charge-zero-theorem-or-coefficient-fill.md"),
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "input_id": "PI876_6_no_local_pole_certificate",
            "input": "no_local_trace_pole",
            "meaning": "rank/constraint/no-hair certificate that zero-return is legal",
            "needed_for": "theorem-zero branch instead of numeric bounds",
            "current_value": "MISSING_CONSTRAINT_RANK_AND_NOHAIR_PROOF",
            "units": "proof_certificate",
            "status": "missing",
            "source_path": str(ROOT / "870-Y5-R10-P_loc-Jtrace-nohair-zero-theorem-or-bound.md"),
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def observable_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "observable_id": "OI876_0_R10",
            "arena": "R10_short_range",
            "impact": "needs Z_T, lambda_T, Q_T^test, Q_T^source, and a full alpha(lambda) curve",
            "current_gate": "blocked",
            "reason": "Hessian/source coefficients missing and R10 source rows remain anchor-only nonclaim",
            "next_action": "derive H_T or prove no local trace pole/source",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "observable_id": "OI876_1_orbital",
            "arena": "orbital_dynamics",
            "impact": "finite-range trace exchange gives delta a/a_N=alpha_T(1+r/lambda_T)exp(-r/lambda_T)",
            "current_gate": "blocked",
            "reason": "lambda_T and source-normalization/GM absorption are not parent-owned",
            "next_action": "derive range and source response or route to zero-return",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "observable_id": "OI876_2_PPN",
            "arena": "PPN",
            "impact": "trace scalar pole or metric-response leakage can shift gamma/beta",
            "current_gate": "blocked",
            "reason": "H_T is only one ingredient; observed metric/coframe response remains separate",
            "next_action": "do not score PPN until trace sector and metric response are both owned",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "observable_id": "OI876_3_clock_WEP",
            "arena": "clock_WEP",
            "impact": "J_T and no-marker clauses decide whether clocks/species carry trace charge",
            "current_gate": "blocked",
            "reason": "Q_T^A=0 is conditional and species/no-marker constants are unsigned",
            "next_action": "prove matter no-marker descent or retain species charge rows",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "observable_id": "OI876_4_local_GR",
            "arena": "local_GR_Newton",
            "impact": "closing trace sector removes only c_T; c_e, c_P, c_S still remain",
            "current_gate": "blocked",
            "reason": "local GR needs q_loc zero or bounds across all residual channels",
            "next_action": "after c_T, continue coframe/projector/source normalization stack",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC876_0_selected",
            "route": "parent_trace_Hessian_source_hunt_and_minimal_action_skeleton",
            "status": "selected",
            "reason": "the extraction equations are fixed, but no explicit parent trace Hessian/source exists to evaluate them",
            "include": "source hunt for parent action terms, P_T definition, H_T skeleton, kinetic/mass/source rows, zero-pole branch",
            "exclude": "free fitted Z_T/lambda_T, local-GR claim, R10 scoring, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG876_0_no_numeric_ZT_claim",
            "claim": "Z_T is derived or numeric",
            "status": "forbidden",
            "reason": "principal symbol of the parent trace Hessian has not been computed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG876_1_no_lambda_claim",
            "claim": "lambda_T or m_T is derived",
            "status": "forbidden",
            "reason": "mass gap/zeroth-order Hessian coefficient is missing",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG876_2_no_zero_return_claim",
            "claim": "no local trace carrier exists",
            "status": "forbidden",
            "reason": "support, pole, source-cokernel, no-tail, and no-marker clauses are not jointly signed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG876_3_no_local_GR_claim",
            "claim": "MTS reduces to local GR/Newton",
            "status": "forbidden",
            "reason": "trace sector is only c_T and remains unresolved; other q_loc residual channels remain open",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG876_4_allowed_private_result",
            "claim": "private derivation contract for Z_T/lambda_T is now exact",
            "status": "allowed_private_nonclaim",
            "reason": "876 turns the coupling hunt into a parent-Hessian extraction problem instead of vibe-coupling",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D876_0",
            "finding": "ZT_lambdaT_extraction_law_written",
            "reason": "Z_T is the trace Hessian principal coefficient and lambda_T follows from the trace mass gap",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D876_1",
            "finding": "zero_return_not_proved",
            "reason": "no local support/no scalar pole/source-cokernel/no-tail/no-marker clauses are still unsigned",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D876_2",
            "finding": "parent_Hessian_source_hunt_required",
            "reason": "current action sketches do not contain enough operator data to compute H_T",
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
            "objective": "hunt the corpus for parent trace-sector action terms and assemble the minimal H_T=P_T^dagger Hess(S_parent)P_T skeleton, or explicitly mark the route as closure-only",
            "include": "P_T source, H_T principal symbol, mass term, source projection J_T, constraint/gauge pole test, zero-return branch",
            "exclude": "numeric fitted couplings, R10/local-GR claims, public prose, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_875_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_875_VALIDATION.csv"
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
    contract_rows: list[dict[str, object]],
    derivation_rows: list[dict[str, object]],
    zero_rows: list[dict[str, object]],
    input_rows: list[dict[str, object]],
    observable_rows_: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
) -> list[dict[str, str]]:
    generated_sets = [
        source_rows,
        contract_rows,
        derivation_rows,
        zero_rows,
        input_rows,
        observable_rows_,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        summary_rows,
    ]
    source_ok = all(row["exists"] is True and row["needle_check"] == "pass" for row in source_rows)
    contract_text = " ".join(str(row.get("mathematical_form", "")) for row in contract_rows)
    missing_inputs_ok = all("MISSING" in str(row.get("current_value", "")) for row in input_rows)
    zero_not_proved = any(row.get("zero_id") == "ZR876_5_verdict" and row.get("current_status") == "not_proved" for row in zero_rows)
    derivation_not_promoted = any(row.get("attempt_id") == "DA876_5_verdict" and row.get("status") == "not_derived" for row in derivation_rows)
    claim_guards_closed = all(row.get("status") != "allowed_claim" for row in guard_rows) and all(
        row.get("claim_allowed") is False for row in decision_rows_
    )
    route_selected = next_target_rows_[0]["next_target"] == NEXT_TARGET and route_rows_[0]["status"] == "selected"
    fw_count = formalization_changed_count()
    checks = [
        ("V876_0_sources_exist_and_needles", source_ok, "all source paths exist and needles are present"),
        ("V876_1_prior_875_clean", prior_875_clean(), "P8_Y5_BRR545_875_VALIDATION.csv clean"),
        ("V876_2_contract_contains_Hessian_ZT_lambda", "H_T" in contract_text and "Z_T" in contract_text and "lambda_T" in contract_text, "trace Hessian, Z_T, and lambda_T extraction contract recorded"),
        ("V876_3_derivation_not_promoted", derivation_not_promoted, "Z_T/lambda_T derivation verdict remains not_derived"),
        ("V876_4_zero_return_not_promoted", zero_not_proved, "zero-return verdict remains not_proved"),
        ("V876_5_parent_inputs_missing_nonclaim", missing_inputs_ok and len(input_rows) == 7, "all parent input rows remain missing/nonclaim"),
        ("V876_6_observable_gates_blocked", all(row.get("current_gate") == "blocked" for row in observable_rows_), "all observable gates blocked"),
        ("V876_7_claim_allowed_false", claim_guards_closed, "claim guards and decision rows keep claim_allowed=false"),
        ("V876_8_all_rows_nonclaim", all_nonclaim(generated_sets), "all generated rows valid_for_claim=false"),
        ("V876_9_formalization_workbench_untouched", fw_count == 0, f"formalization_changed_after_cutoff={fw_count}"),
        ("V876_10_route_selected", route_selected, NEXT_TARGET),
        ("V876_11_validation_rows_ready", True, "validation table constructed"),
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
    contract_rows: list[dict[str, object]],
    derivation_rows: list[dict[str, object]],
    zero_rows: list[dict[str, object]],
    input_rows: list[dict[str, object]],
    observable_rows_: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    sections = [
        "# 876 - Y5/R10 Trace-Sector Z_T Lambda_T Parent Input or Zero Return",
        "",
        f"Status: `{STATUS}`  ",
        f"Claim ceiling: `{CLAIM_CEILING}`  ",
        f"Generated UTC: `{generated_utc}`",
        "",
        "Current result: **the coupling target is now an exact parent-Hessian problem, not a mystery constant**. "
        "`Z_T` must be the principal-symbol normalization of the projected trace Hessian "
        "`H_T=P_T^dagger (delta^2 S_parent) P_T`, and `lambda_T` must come from its mass gap. "
        "If that trace Hessian has no physical local scalar pole and no source projection, the branch can zero-return. "
        "The current corpus does not yet provide the parent Hessian, projector, source projection, or no-pole certificate, "
        "so all R10/PPN/clock/WEP/orbital/local-GR claims remain blocked.",
        "",
        "## Nonclaim Summary",
        md_table(summary_rows),
        "",
        "## Source Register",
        md_table(source_rows),
        "",
        "## Trace-Sector Quadratic Contract",
        md_table(contract_rows),
        "",
        "## Derivation Attempt",
        md_table(derivation_rows),
        "",
        "## Zero-Return Audit",
        md_table(zero_rows),
        "",
        "## Parent Input Ledger",
        md_table(input_rows),
        "",
        "## Observable Impact",
        md_table(observable_rows_),
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
    summary_rows = nonclaim_summary_rows(generated_utc)
    contract_rows = trace_sector_contract_rows(generated_utc)
    derivation_rows = derivation_attempt_rows(generated_utc)
    zero_rows = zero_return_rows(generated_utc)
    input_rows = parent_input_rows(generated_utc)
    observable_rows_ = observable_rows(generated_utc)
    route_rows_ = route_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_target_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        source_rows,
        contract_rows,
        derivation_rows,
        zero_rows,
        input_rows,
        observable_rows_,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        summary_rows,
    )

    outputs = {
        "P8_Y5_R10_876_SOURCE_REGISTER.csv": source_rows,
        "P8_Y5_R10_876_TRACE_SECTOR_QUADRATIC_CONTRACT.csv": contract_rows,
        "P8_Y5_R10_876_DERIVATION_ATTEMPT.csv": derivation_rows,
        "P8_Y5_R10_876_ZERO_RETURN_AUDIT.csv": zero_rows,
        "P8_Y5_R10_876_PARENT_INPUT_LEDGER.csv": input_rows,
        "P8_Y5_R10_876_OBSERVABLE_IMPACT.csv": observable_rows_,
        "P8_Y5_R10_876_ROUTE_CHOICE.csv": route_rows_,
        "P8_Y5_R10_876_CLAIM_GUARD.csv": guard_rows,
        "P8_Y5_R10_876_DECISION.csv": decision_rows_,
        "P8_Y5_R10_876_NEXT_TARGET.csv": next_target_rows_,
        "P8_Y5_R10_876_NONCLAIM_SUMMARY.csv": summary_rows,
        "P8_Y5_BRR545_876_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "876-Y5-R10-trace-sector-ZT-lambdaT-parent-input-or-zero-return.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows,
        source_rows,
        contract_rows,
        derivation_rows,
        zero_rows,
        input_rows,
        observable_rows_,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_876_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
