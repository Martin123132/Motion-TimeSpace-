from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_885_parent_charge_lattice_Ward_norm_attempted_not_derived_Htr_zero_pole_source_fill_staged_nonclaim"
CLAIM_CEILING = "charge_lattice_Ward_norm_and_Htr_zero_pole_source_fill_only_no_Qstar_derivation_no_zero_return_no_R10_PPN_or_local_GR_claim"
NEXT_TARGET = "886-Y5-R10-Htr-zero-pole-rank-test-and-Jtr-source-cokernel-gate.md"


SOURCE_SPECS = [
    {
        "source_id": "884_doc",
        "path": ROOT / "884-Y5-R10-charge-unit-superselection-parent-clause-or-cT-P0-source-acquisition.md",
        "needle": "the `Q_*` route is now an exact parent-clause target",
        "role": "immediate parent charge-unit clause handoff",
    },
    {
        "source_id": "884_validation",
        "path": OUT / "P8_Y5_BRR545_884_VALIDATION.csv",
        "needle": "V884_11_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "884_clause",
        "path": OUT / "P8_Y5_R10_884_CHARGE_UNIT_PARENT_CLAUSE.csv",
        "needle": "CU884_2_charge_lattice",
        "role": "charge lattice clause to be attempted",
    },
    {
        "source_id": "884_p0",
        "path": OUT / "P8_Y5_R10_884_CT_P0_SOURCE_ACQUISITION.csv",
        "needle": "P0_884_0_Htr",
        "role": "priority-0 retained trace source rows",
    },
    {
        "source_id": "883_doc",
        "path": ROOT / "883-Y5-R10-Qstar-superselection-or-Ward-norm-sector-and-cT-source-pack-prioritization.md",
        "needle": "`Q_*` can be mathematically quarantined as a fixed unit",
        "role": "fixed-unit/superselection precursor",
    },
    {
        "source_id": "879_doc",
        "path": ROOT / "879-Y5-R10-parent-trace-covector-and-pairing-source-or-closure.md",
        "needle": "`P_tr` is demoted to closure-only",
        "role": "trace covector and parent pairing blocker",
    },
    {
        "source_id": "878_doc",
        "path": ROOT / "878-Y5-R10-Ptr-parent-projector-definition-and-constraint-rank-test.md",
        "needle": "`P_tr` is now a precise parent-geometry object",
        "role": "formal P_tr construction and rank tests",
    },
    {
        "source_id": "877_doc",
        "path": ROOT / "877-Y5-R10-parent-trace-Hessian-source-hunt-and-minimal-action-skeleton.md",
        "needle": "the parent trace-Hessian route is still alive",
        "role": "minimal H_tr skeleton",
    },
    {
        "source_id": "876_doc",
        "path": ROOT / "876-Y5-R10-trace-sector-ZT-lambdaT-parent-input-or-zero-return.md",
        "needle": "principal-symbol normalization of the projected trace Hessian",
        "role": "Z_tr/lambda_tr parent-Hessian contract",
    },
    {
        "source_id": "863_Ward_trace",
        "path": ROOT / "863-Y5-R10-Ward-trace-lift-current-and-coframe-pullback-zero-theorem.md",
        "needle": "Q_* = unit(J_trace,parent)",
        "role": "Ward trace current and local projection silence",
    },
    {
        "source_id": "337_exact_readout",
        "path": ROOT / "337-exact-parent-pullback-selection-rule-gate.md",
        "needle": "q_trace = 2/27",
        "role": "conditional exact trace readout",
    },
    {
        "source_id": "338_readout_gate",
        "path": ROOT / "338-action-level-exact-readout-gate.md",
        "needle": "source-at-zero",
        "role": "no-spurion readout discipline",
    },
    {
        "source_id": "109_boundary_charge",
        "path": ROOT / "109-boundary-charge-two-ninth-theorem-attempt.md",
        "needle": "boundary_charge_unit_defined",
        "role": "prior normalized boundary charge failure",
    },
    {
        "source_id": "97_canonical_R",
        "path": ROOT / "97-canonical-R-theorem-attempt.md",
        "needle": "normalized_boundary_charge_derived",
        "role": "prior canonical R/Qstar failure",
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
            "what_changed": "attempted the charge-lattice/Ward-norm proof path for Q_* and staged the H_tr zero-pole/source-cokernel fallback rows",
            "best_partial_result": "the exact promotion contract is now sharper: Q_* must be a nonzero generator/norm of a relative trace charge sector, and P_tr/H_tr can only be reopened after either that sector is parent-signed or the local trace Hessian/source branch is filled",
            "hard_blockers": "no integer period map, no parent charge metric/Hodge pairing, no proof that q_trace=2/27 is an integral charge unit, no parent P_tr/H_tr, no local no-pole/source-cokernel theorem",
            "what_is_not_claimed": "Q_* derivation, DeltaR prediction, parent P_tr/H_tr, c_T zero-return, R10/PPN/WEP/clock/orbital pass, local GR/Newton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def charge_lattice_attempt_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "lattice_id": "CL885_0_closed_current",
            "required_clause": "J_trace is a closed/conserved parent current",
            "mathematical_form": "d J_trace = 0 or nabla_mu J_trace^mu = boundary endpoint balance with no local leak",
            "attempt_result": "conditional_current_only",
            "missing_signature": "863 writes the Ward-current balance shape but does not derive J_trace from S_parent or prove J_local_leak=0",
            "promotion_effect_if_closed": "allows period/integral charge tests to be meaningful",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "lattice_id": "CL885_1_integer_periods",
            "required_clause": "relative trace current has integer periods",
            "mathematical_form": "[J_trace/Q_*] in H_rel^Z and integral_Sigma J_trace = n_Sigma Q_*",
            "attempt_result": "not_derived",
            "missing_signature": "no parent cycle basis, integral quantization rule, or cohomology-to-action theorem is present",
            "promotion_effect_if_closed": "Q_* becomes a charge generator instead of a fitted scale",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "lattice_id": "CL885_2_nonzero_generator",
            "required_clause": "the trace charge generator is finite and nonzero",
            "mathematical_form": "0 < |Q_*| < infinity and Q_* = generator image(period map J_trace)",
            "attempt_result": "not_derived",
            "missing_signature": "882 rejected endpoint-only Q_* variation and no independent generator theorem replaces it",
            "promotion_effect_if_closed": "R=Q/Q_* and endpoint P_tr normalization are legal without varying Q_*",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "lattice_id": "CL885_3_exact_readout_bridge",
            "required_clause": "q_trace=2/27 is a charge readout compatible with the lattice",
            "mathematical_form": "DeltaQ_trace/Q_* = 3 q_trace = 2/9 with q_trace=2/27",
            "attempt_result": "conditional_readout_not_lattice",
            "missing_signature": "337/338 support a no-spurion readout shape, but not an integer/rational lattice owner for Q_*",
            "promotion_effect_if_closed": "DeltaR=2/9 could be tied to a parent charge sector rather than a closure",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "lattice_id": "CL885_4_sector_decomposition",
            "required_clause": "parent solution space decomposes into fixed trace-charge sectors",
            "mathematical_form": "Sol(S_parent)=union_[Q_*] Sol_[Q_*] with delta Q_*=0 inside one sector",
            "attempt_result": "clause_written_not_parent_signed",
            "missing_signature": "884 writes the sector contract, but no parent action/source declares it",
            "promotion_effect_if_closed": "883 scale-cancelled endpoint projector can re-enter without the 882 Q_* obstruction",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "lattice_id": "CL885_5_lattice_verdict",
            "required_clause": "Q_* is derived as a parent charge lattice unit",
            "mathematical_form": "CL885_0 through CL885_4 close jointly",
            "attempt_result": "not_derived_fail_for_claim",
            "missing_signature": "current corpus supplies a precise theorem target, not the lattice proof",
            "promotion_effect_if_closed": "would reopen Q_*, P_tr, H_tr, endpoint arrow, and local-silence tests",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def ward_norm_attempt_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "ward_id": "WN885_0_pairing_measure",
            "required_clause": "parent owns the Ward-current inner product",
            "mathematical_form": "Q_*^2 = <J_trace,J_trace>_parent via a parent Hodge/measure/charge metric",
            "attempt_result": "missing_pairing_measure",
            "missing_signature": "879 found no parent charge metric, kinetic pairing, or constrained pseudo-inverse that owns the trace norm",
            "promotion_effect_if_closed": "Q_* is fixed before data and has physical units/source path",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "ward_id": "WN885_1_norm_is_predata",
            "required_clause": "the norm is independent of SN/BAO/R10/PPN fitting",
            "mathematical_form": "d Q_*/d(data score)=0 and source owner is written before empirical comparison",
            "attempt_result": "policy_gate_only",
            "missing_signature": "a no-calibration rule exists, but not the actual norm source",
            "promotion_effect_if_closed": "prevents amplitude/coupling laundering",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "ward_id": "WN885_2_local_silence",
            "required_clause": "Ward norm has no local marker or source leakage",
            "mathematical_form": "partial_mu Q_*=0, partial_A Q_*=0, P_loc J_trace=0",
            "attempt_result": "not_parent_signed",
            "missing_signature": "863/870/878 keep local-global quotient split, boundary no-hair, and source-cokernel silence conditional",
            "promotion_effect_if_closed": "Q_* does not itself create PPN/WEP/clock hair",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "ward_id": "WN885_3_exact_readout_bridge",
            "required_clause": "Ward current normalizes the exact trace readout",
            "mathematical_form": "Q_trace/Q_* = 3 q_trace and q_trace=2/27 as parent readout",
            "attempt_result": "conditional_only",
            "missing_signature": "exact readout exists as a reduced/post-variation object but not as an action-owned Ward norm",
            "promotion_effect_if_closed": "ties rational readout to charge current rather than closure",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "ward_id": "WN885_4_norm_verdict",
            "required_clause": "Q_* is derived as a Ward-current norm",
            "mathematical_form": "WN885_0 through WN885_3 close jointly",
            "attempt_result": "not_derived_fail_for_claim",
            "missing_signature": "no parent current pairing/norm theorem is available",
            "promotion_effect_if_closed": "fixed-unit/superselection branch could be promoted to theorem target with source path",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def htr_zero_pole_fill_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "p0_id": "HZ885_0_Ptr_owner",
            "quantity": "P_tr",
            "formula_or_test": "P_tr=v_tr tensor ell_tr, ell_tr=DQ_trace, v_tr=K_parent^-1 ell_tr/<ell_tr,K_parent^-1 ell_tr>",
            "current_status": "CLOSURE_ONLY_PENDING_QSTAR_KPARENT",
            "required_source": "parent charge unit plus parent pairing/pseudo-inverse",
            "next_action": "either close charge lattice/Ward norm or keep P_tr as symbolic closure",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "p0_id": "HZ885_1_Htr",
            "quantity": "H_tr",
            "formula_or_test": "H_tr=P_tr^dagger Hess(S_parent) P_tr on the physical quotient tangent space",
            "current_status": "MISSING_PARENT_HESSIAN",
            "required_source": "second variation of actual parent action after gauge/constraint reduction",
            "next_action": "construct minimal local Hessian block or prove P_tr has rank zero locally",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "p0_id": "HZ885_2_zero_pole",
            "quantity": "rank/no-pole certificate",
            "formula_or_test": "rank(P_loc P_tr P_loc^dagger)=0 or reduced inverse of H_tr has no source-coupled pole",
            "current_status": "MISSING_RANK_NOPOLE_TEST",
            "required_source": "constraint-rank calculation, gauge bracket, or compact-support no-hair theorem",
            "next_action": "run theorem audit before any finite-range alpha scoring",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "p0_id": "HZ885_3_Jtr_source_cokernel",
            "quantity": "J_tr and source-cokernel projection",
            "formula_or_test": "J_tr=P_tr^dagger J_parent and <u_tr,J_tr>=0 for all physical local trace cokernel modes",
            "current_status": "MISSING_SOURCE_COKERNEL",
            "required_source": "matter descent/source owner, or P_loc J_trace=0 theorem",
            "next_action": "decide zero-return versus retained finite trace coupling",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "p0_id": "HZ885_4_Ztr_mtr_lambda",
            "quantity": "Z_tr, mu_tr^2, m_tr, lambda_tr",
            "formula_or_test": "sigma_2(H_tr)=Z_tr g^{mu nu}k_mu k_nu; m_tr^2=mu_tr^2/Z_tr; lambda_tr=1/m_tr",
            "current_status": "MISSING_PARENT_SYMBOLS",
            "required_source": "principal and zeroth-order symbols of H_tr if finite carrier survives",
            "next_action": "only fill after H_tr exists and pole branch survives",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "p0_id": "HZ885_5_bound_branch",
            "quantity": "retained finite trace branch",
            "formula_or_test": "alpha_tr_AB=Q_tr^A Q_tr^B/(4*pi Z_tr G_obs m_A m_B) with finite lambda_tr",
            "current_status": "NONCLAIM_SCHEMA_ONLY",
            "required_source": "numeric/sourced Z_tr, lambda_tr, source charges, and real bound curves",
            "next_action": "prepare source rows only after zero-pole/source-cokernel attempt fails",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "p0_id": "HZ885_6_verdict",
            "quantity": "trace zero-or-bound branch",
            "formula_or_test": "zero-return if HZ885_0..3 close to zero; otherwise retain HZ885_4..5 for bounds",
            "current_status": "BLOCKED_NONCLAIM",
            "required_source": "parent P_tr/H_tr and source-cokernel/no-pole result",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def promotion_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "PG885_0_Qstar_lattice",
            "promotion_target": "Q_* is a parent charge-lattice generator",
            "required_to_pass": "closed J_trace, integer periods, nonzero generator, superselection sectors",
            "current_evidence": "contract only",
            "gate_result": "fail_for_claim",
            "next_action": "derive relative-cohomology/integrality theorem or abandon Q_* promotion",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG885_1_Qstar_Ward_norm",
            "promotion_target": "Q_* is a Ward-current norm",
            "required_to_pass": "parent current pairing, pre-data norm, local no-marker/no-leak",
            "current_evidence": "missing_pairing_measure",
            "gate_result": "fail_for_claim",
            "next_action": "derive parent Hodge/measure/charge metric or keep closure-only",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG885_2_Ptr_Htr",
            "promotion_target": "P_tr and H_tr are parent-owned",
            "required_to_pass": "Q_* plus K_parent/pseudo-inverse plus Hess(S_parent) trace block",
            "current_evidence": "P_tr closure-only, H_tr missing",
            "gate_result": "fail_for_claim",
            "next_action": "H_tr zero-pole rank/source-cokernel gate",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG885_3_zero_return",
            "promotion_target": "local trace branch zero-returns",
            "required_to_pass": "rank-zero or no physical pole plus zero source-cokernel",
            "current_evidence": "not_tested/missing source-cokernel",
            "gate_result": "fail_for_claim",
            "next_action": "attempt rank/no-pole/source-cokernel theorem in 886",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG885_4_local_GR",
            "promotion_target": "MTS locally reduces to GR/Newton from trace branch",
            "required_to_pass": "Q_* sector, P_tr/H_tr, no local pole/source, all other q_loc channels controlled",
            "current_evidence": "trace branch not closed and other local residuals remain open",
            "gate_result": "fail_for_claim",
            "next_action": "do not claim; continue zero-or-bound derivation route",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC885_0_selected",
            "route": "Htr_zero_pole_rank_test_and_Jtr_source_cokernel_gate",
            "status": "selected",
            "reason": "the charge-lattice/Ward-norm route is precise but not closed; the lowest-scrutiny next move is to prove no local trace pole/source, or else honestly retain a bounded trace carrier",
            "include": "rank(P_loc P_tr P_loc^dagger), reduced H_tr pole test, J_tr source-cokernel, P_loc J_trace, finite-carrier fallback rows",
            "exclude": "Q_* claim, DeltaR claim, local-GR/Newton pass, R10/PPN pass, fitted coupling, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG885_0_no_Qstar_claim",
            "forbidden_claim": "Q_* is derived",
            "status": "forbidden",
            "reason": "neither charge lattice nor Ward-current norm is parent-signed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG885_1_no_DeltaR_claim",
            "forbidden_claim": "DeltaR=2/9 is a parent prediction",
            "status": "forbidden",
            "reason": "exact readout remains conditional and the absolute charge unit/endpoint arrow are unsigned",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG885_2_no_Htr_zero_claim",
            "forbidden_claim": "the local trace Hessian has no physical pole/source",
            "status": "forbidden",
            "reason": "rank/no-pole/source-cokernel tests are staged but not executed/proved",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG885_3_no_local_GR_claim",
            "forbidden_claim": "MTS reduces to GR/Newton locally",
            "status": "forbidden",
            "reason": "trace branch and other q_loc residual channels remain open",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG885_4_allowed_private_result",
            "forbidden_claim": "none",
            "status": "allowed_private_nonclaim",
            "reason": "885 narrows the blocker to either a real charge-sector proof or a local H_tr zero-pole/source-cokernel proof",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D885_0",
            "finding": "charge_lattice_attempt_failed_for_claim",
            "reason": "closed current, integer periods, nonzero generator, and sector decomposition are not parent-signed",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D885_1",
            "finding": "Ward_norm_attempt_failed_for_claim",
            "reason": "no parent current pairing/Hodge/measure/charge metric fixes Q_*",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D885_2",
            "finding": "Htr_zero_pole_source_cokernel_is_next",
            "reason": "if Q_* remains closure-only, the honest low-scrutiny path is proving no local trace carrier/source or retaining it as a bounded nonclaim branch",
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
            "objective": "test whether the local trace branch has rank zero/no physical pole and zero source-cokernel; if not, retain sourced finite-carrier rows without claiming local GR",
            "include": "P_loc P_tr rank, reduced H_tr inverse/pole, gauge/constraint reduction, J_tr source-cokernel, P_loc J_trace, finite trace branch fallback",
            "exclude": "public claim, fitted Q_*, fitted c_T, R10/local-GR pass, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_884_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_884_VALIDATION.csv"
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
    lattice_rows: list[dict[str, object]],
    ward_rows: list[dict[str, object]],
    htr_rows: list[dict[str, object]],
    promotion_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    htr_ids = {row["p0_id"] for row in htr_rows}
    row_groups = [
        source_rows,
        lattice_rows,
        ward_rows,
        htr_rows,
        promotion_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        summary_rows,
    ]
    checks = [
        {
            "check_id": "V885_0_sources_exist_and_needles",
            "result": "pass" if all(row["exists"] and row["needle_check"] == "pass" for row in source_rows) else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V885_1_prior_884_clean",
            "result": "pass" if prior_884_clean() else "fail",
            "detail": "P8_Y5_BRR545_884_VALIDATION.csv clean",
        },
        {
            "check_id": "V885_2_charge_lattice_attempted",
            "result": "pass" if len(lattice_rows) >= 6 and any(row["lattice_id"] == "CL885_5_lattice_verdict" for row in lattice_rows) else "fail",
            "detail": "charge-lattice proof audit constructed",
        },
        {
            "check_id": "V885_3_charge_lattice_not_derived",
            "result": "pass" if any(row["lattice_id"] == "CL885_5_lattice_verdict" and row["attempt_result"] == "not_derived_fail_for_claim" for row in lattice_rows) else "fail",
            "detail": "Q_* charge lattice remains not derived",
        },
        {
            "check_id": "V885_4_Ward_norm_not_derived",
            "result": "pass" if any(row["ward_id"] == "WN885_4_norm_verdict" and row["attempt_result"] == "not_derived_fail_for_claim" for row in ward_rows) else "fail",
            "detail": "Ward-current norm remains not derived",
        },
        {
            "check_id": "V885_5_Htr_zero_pole_rows_ready",
            "result": "pass" if {"HZ885_1_Htr", "HZ885_2_zero_pole", "HZ885_3_Jtr_source_cokernel"}.issubset(htr_ids) else "fail",
            "detail": "H_tr/no-pole/J_tr source-cokernel rows present",
        },
        {
            "check_id": "V885_6_Htr_rows_block_claims",
            "result": "pass" if all("MISSING" in str(row["current_status"]) or "CLOSURE_ONLY" in str(row["current_status"]) or "NONCLAIM" in str(row["current_status"]) or "BLOCKED" in str(row["current_status"]) for row in htr_rows) else "fail",
            "detail": "all H_tr branch rows remain blocked/nonclaim",
        },
        {
            "check_id": "V885_7_promotion_gates_blocked",
            "result": "pass" if promotion_rows and all(row["gate_result"] == "fail_for_claim" for row in promotion_rows) else "fail",
            "detail": "all promotion gates fail for claim",
        },
        {
            "check_id": "V885_8_claim_allowed_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in decision_rows_) else "fail",
            "detail": "decision rows keep claim_allowed=false",
        },
        {
            "check_id": "V885_9_all_rows_nonclaim",
            "result": "pass" if all_nonclaim(row_groups) else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V885_10_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V885_11_route_selected",
            "result": "pass" if route_rows_ and next_target_rows_ and next_target_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V885_12_validation_rows_ready",
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
    lattice_rows: list[dict[str, object]],
    ward_rows: list[dict[str, object]],
    htr_rows: list[dict[str, object]],
    promotion_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    lines = [
        "# 885 - Y5/R10 Parent Charge Lattice or Htr P0 Zero-Pole Source Fill",
        "",
        f"Status: `{STATUS}`  ",
        f"Claim ceiling: `{CLAIM_CEILING}`  ",
        f"Generated UTC: `{generated_utc}`",
        "",
        "Current result: **the charge-unit route was attempted in its cleanest form and still does not close from the current corpus**. A legal `Q_*` theorem would need a parent-owned relative trace charge lattice or a Ward-current norm: closed `J_trace`, integer periods or a charge metric, a nonzero generator, pre-data sector labels, and local silence. The existing files give a sharp contract and useful endpoint algebra, but not those parent signatures. So the best route is now the local trace zero-or-bound gate: prove `P_tr/H_tr` has no local source-coupled pole and zero source-cokernel, or retain a finite trace carrier as a bounded nonclaim branch.",
        "",
        "## Nonclaim Summary",
        md_table(summary_rows),
        "",
        "## Source Register",
        md_table(source_rows),
        "",
        "## Charge Lattice Attempt",
        md_table(lattice_rows),
        "",
        "## Ward Norm Attempt",
        md_table(ward_rows),
        "",
        "## Htr Zero-Pole / Source-Cokernel Fill",
        md_table(htr_rows),
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
    lattice_rows = charge_lattice_attempt_rows(generated_utc)
    ward_rows = ward_norm_attempt_rows(generated_utc)
    htr_rows = htr_zero_pole_fill_rows(generated_utc)
    promotion_rows = promotion_gate_rows(generated_utc)
    route_rows_ = route_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_target_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows,
        lattice_rows,
        ward_rows,
        htr_rows,
        promotion_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        summary_rows,
    )

    outputs = {
        "P8_Y5_R10_885_SOURCE_REGISTER.csv": source_rows,
        "P8_Y5_R10_885_CHARGE_LATTICE_ATTEMPT.csv": lattice_rows,
        "P8_Y5_R10_885_WARD_NORM_ATTEMPT.csv": ward_rows,
        "P8_Y5_R10_885_HTR_ZERO_POLE_SOURCE_FILL.csv": htr_rows,
        "P8_Y5_R10_885_PROMOTION_GATE.csv": promotion_rows,
        "P8_Y5_R10_885_ROUTE_CHOICE.csv": route_rows_,
        "P8_Y5_R10_885_CLAIM_GUARD.csv": guard_rows,
        "P8_Y5_R10_885_DECISION.csv": decision_rows_,
        "P8_Y5_R10_885_NEXT_TARGET.csv": next_target_rows_,
        "P8_Y5_R10_885_NONCLAIM_SUMMARY.csv": summary_rows,
        "P8_Y5_BRR545_885_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "885-Y5-R10-parent-charge-lattice-or-Htr-P0-zero-pole-source-fill.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows,
        source_rows,
        lattice_rows,
        ward_rows,
        htr_rows,
        promotion_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_885_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
