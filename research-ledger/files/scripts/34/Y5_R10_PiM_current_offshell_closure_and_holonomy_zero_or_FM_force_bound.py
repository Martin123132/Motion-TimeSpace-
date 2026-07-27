from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC_NAME = "920-Y5-R10-PiM-current-offshell-closure-and-holonomy-zero-or-FM-force-bound.md"
STATUS = "Y5_R10_920_PiM_offshell_closure_not_parent_signed_holonomy_zero_conditional_FM_force_bound_pack_ready_nonclaim"
CLAIM_CEILING = "PiM_offshell_closure_and_holonomy_audit_only_no_mass_gauge_silence_no_Newton_PPN_or_local_GR_claim"
NEXT_TARGET = "921-Y5-R10-FM-force-weak-field-map-and-KBFH-units-bound-runner.md"
GENERATED = datetime.now(timezone.utc).isoformat()
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        cells = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def b(value: bool) -> str:
    return "true" if value else "false"


def source_specs() -> list[dict[str, str]]:
    return [
        {
            "source_id": "919_doc",
            "path": "919-Y5-R10-matter-current-silence-lemma-or-DeltaHT-bound-runner.md",
            "role": "sets off-shell dJ_Pi and exact A_M as the silence clauses",
            "needle": "off-shell parent identity",
        },
        {
            "source_id": "919_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_919_VALIDATION.csv",
            "role": "proves 919 was generated and gated as nonclaim",
            "needle": "V919_12_validation_rows_ready",
        },
        {
            "source_id": "521_PiM_owner",
            "path": "521-Y5-PiM-projector-owner-or-radial-bound-runner.md",
            "role": "Pi_M owner fork and product-rule commutator gate",
            "needle": "[d,Pi_M]J_H = 0.",
        },
        {
            "source_id": "534_topological_certificate",
            "path": "534-Y5-PiM-topological-equality-certificate-or-commutator-bound.md",
            "role": "topological equality certificate requirements",
            "needle": "Current MTS does not yet prove this.",
        },
        {
            "source_id": "535_commutator_runner",
            "path": "535-Y5-PiM-commutator-bound-runner-or-Hilbert-worldtube-glue.md",
            "role": "existing executable commutator/boundary runner template",
            "needle": "Current MTS has no sourced numeric inputs",
        },
        {
            "source_id": "539_Hamiltonian_PiM",
            "path": "539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md",
            "role": "Hamiltonian charge map repair candidate",
            "needle": "not a promotion",
        },
        {
            "source_id": "455_PiM_flux_closure",
            "path": "455-PiM-flux-closure-Ward-or-topological-current-attempt.md",
            "role": "early statement that Ward closure is not enough",
            "needle": "Diffeomorphism Ward conservation of total stress is not enough",
        },
        {
            "source_id": "500_topological_PiM",
            "path": "500-topological-PiM-current-parent-clause-or-radial-bound-runner.md",
            "role": "topological current closes itself but not Hilbert equality",
            "needle": "But it does not yet prove Pi_M J_H = J_M_top.",
        },
        {
            "source_id": "501_Hilbert_equality",
            "path": "501-topological-Hilbert-current-equality-or-radial-bound-runner.md",
            "role": "topological-Hilbert equality theorem remains open",
            "needle": "The equality theorem is not derived.",
        },
        {
            "source_id": "520_Ward_closure",
            "path": "520-Y5-source-current-Ward-closure-or-bound-row.md",
            "role": "projected mass-current closure target and Ward limit",
            "needle": "Ward conservation alone does not prove that",
        },
        {
            "source_id": "PiM_flux_contract",
            "path": "source-intake/mts_residuals/P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
            "role": "machine-readable FC0-FC8 PiM flux closure contract",
            "needle": "FC2_closed_mass_current_equation",
        },
        {
            "source_id": "mass_flux_contract",
            "path": "source-intake/mts_residuals/P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
            "role": "machine-readable mass-flux projector and calibration contract",
            "needle": "MF0_parent_projector_origin",
        },
    ]


def sources() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in source_specs():
        path = ROOT / spec["path"]
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": b(exists),
                "needle_found": b(needle_found),
                "valid_for_claim": "false",
                "generated_utc": GENERATED,
            }
        )
    return rows


def summary_rows() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "current_result": "holonomy-zero has a plausible simply-connected local-domain route, but off-shell closure d(Pi_M J_H)=0 remains unproved",
            "practical_meaning": "the coupling is not dead, but it must now be treated as F_M_force/K_BF_H bound input until PiM closure is parent-signed",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        }
    ]


def closure_rows() -> list[dict[str, object]]:
    return [
        {
            "closure_id": "PCL920_0_factorization",
            "target": "d(Pi_M J_H)=0",
            "identity_or_test": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H",
            "result": "factorization written; zero requires both Hilbert-current closure and projector commutator zero",
            "blocker": "neither term is off-shell parent-signed in the current corpus",
            "parent_signed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "closure_id": "PCL920_1_Hilbert_current",
            "target": "Pi_M dJ_H",
            "identity_or_test": "Ward conservation of T_munu gives current conservation only after matter equations and time-generator assumptions",
            "result": "necessary support, not action-level silence",
            "blocker": "off-shell Noether identity for projected mass current is missing",
            "parent_signed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "closure_id": "PCL920_2_projector_commutator",
            "target": "[d,Pi_M]J_H",
            "identity_or_test": "metric/domain/memory dependence of Pi_M creates product-rule leakage unless Pi_M is absolute or Hamiltonian-owned",
            "result": "topological/Hamiltonian routes are candidates",
            "blocker": "old topological Pi_M can be the wrong conserved object; Hamiltonian Pi_M is not adopted and proved",
            "parent_signed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "closure_id": "PCL920_3_Hilbert_topological_equality",
            "target": "Pi_M J_H = J_M_top + dB_zero",
            "identity_or_test": "topological representative must equal the observed Hilbert source current",
            "result": "existing certificate lists exact clauses",
            "blocker": "equality theorem and zero boundary exact term remain unproved",
            "parent_signed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "closure_id": "PCL920_4_Hamiltonian_repair",
            "target": "Pi_M := Pi_M^H from parent Hamiltonian charge",
            "identity_or_test": "define mass projection from covariant phase-space/Hamiltonian charge rather than readout or independent topology",
            "result": "best conceptual repair route",
            "blocker": "integrability, source-measure glue, and Gauss/PPN readout remain open",
            "parent_signed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def holonomy_rows() -> list[dict[str, object]]:
    return [
        {
            "holonomy_id": "HOL920_0_BF_flatness",
            "condition": "BF/nonpropagating sector gives dA_M=0",
            "math_test": "flat one-form connection",
            "result": "local curvature can vanish",
            "blocker": "flatness alone does not imply exactness on a domain with H1 or defects",
            "status": "conditional_support",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "holonomy_id": "HOL920_1_trivial_H1_domain",
            "condition": "compact local exterior domain has H1(D)=0 and no mass-gauge line defects",
            "math_test": "closed one-form A_M is exact by de Rham/Poincare lemma on the admissible domain",
            "result": "this would close A_M=d lambda_M locally",
            "blocker": "admissible-domain topology is not yet parent-selected for all local test arenas",
            "status": "promising_geometry_condition_not_parent_signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "holonomy_id": "HOL920_2_boundary_gauge",
            "condition": "lambda_M is fixed to zero or universal constant on compact boundaries",
            "math_test": "integral_boundary lambda_M Pi_M J_H carries no variation/source shift",
            "result": "would remove boundary term from the 919 integration-by-parts proof",
            "blocker": "zero boundary flux remains a separate source-normalization clause",
            "status": "not_parent_derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "holonomy_id": "HOL920_3_nontrivial_cycle_fallback",
            "condition": "if H1(D) is nonzero or a defect/handle is allowed",
            "math_test": "A_M_holonomy=max_gamma |integral_gamma A_M|",
            "result": "holonomy becomes an observable residual/bound input",
            "blocker": "needs source-backed local topology or experimental projection",
            "status": "retained_bound_row",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def source_ready_rows() -> list[dict[str, object]]:
    return [
        {
            "row_id": "SR920_0_F_M_force",
            "symbol": "F_M_force",
            "units_or_dimension": "acceleration-equivalent, PPN-force-equivalent, or dimensionless residual after chosen projection",
            "formula": "F_M_force = K_BF_H * P_local(A_M wedge delta(Pi_M J_H)/delta psi)",
            "required_columns": "system_id;arena;projection;K_BF_H;A_M_norm;dPiMJ_leak;boundary_flux;units;source_path",
            "current_status": "schema_ready_missing_numeric_inputs",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "row_id": "SR920_1_K_BF_H",
            "symbol": "K_BF_H",
            "units_or_dimension": "action-normalized coupling; units depend on form normalization of A_M and J_H",
            "formula": "coefficient of integral A_M wedge Pi_M J_H",
            "required_columns": "normalization_convention;A_units;J_units;K_units;parent_source;sign;source_path",
            "current_status": "missing_parent_level_and_units",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "row_id": "SR920_2_dPiMJ_leak",
            "symbol": "dPiMJ_leak",
            "units_or_dimension": "mass-current divergence or normalized shell flux",
            "formula": "dPiMJ_leak = Pi_M dJ_H + [d,Pi_M]J_H",
            "required_columns": "system_id;r_inner;r_outer;PiMdJH;commutator_flux;normalization;source_path",
            "current_status": "maps_to_existing_commutator_runner_without_numeric_inputs",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "row_id": "SR920_3_A_M_holonomy",
            "symbol": "A_M_holonomy",
            "units_or_dimension": "line integral of A_M; dimension set by A_M convention",
            "formula": "A_M_holonomy=max_gamma |integral_gamma A_M|",
            "required_columns": "domain_id;cycle_id;H1_rank;A_integral;defect_flag;boundary_condition;source_path",
            "current_status": "zero_if_H1_zero_and_no_defects_else_bound_input",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "row_id": "SR920_4_B_zero_flux",
            "symbol": "B_zero_flux",
            "units_or_dimension": "mass/current boundary flux or normalized exact-term flux",
            "formula": "B_zero_flux = integral_boundary lambda_M Pi_M J_H or integral_boundary dB_zero",
            "required_columns": "boundary_id;lambda_boundary;flux_value;normalization;zero_flux_theorem_or_bound;source_path",
            "current_status": "missing_zero_boundary_flux_theorem_or_bound",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "BD920_0_offshell_closure",
            "branch": "PiM_current_closure",
            "verdict": "not_parent_signed",
            "reason": "Ward conservation, topological equality, and Hamiltonian PiM remain candidate routes but not off-shell parent identities",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "decision_id": "BD920_1_holonomy_zero",
            "branch": "exact_A_M",
            "verdict": "conditional_geometry_route",
            "reason": "H1(D)=0 plus no defects would make flat A_M exact, but admissible local topology is not parent-selected",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "decision_id": "BD920_2_bound_pack",
            "branch": "FM_force_bound_runner",
            "verdict": "source_ready_schema_written_nonclaim",
            "reason": "F_M_force, K_BF_H, dPiMJ_leak, A_M_holonomy, and B_zero_flux now have required columns",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "CGATE920_0_dPiMJ_zero",
            "claim": "d(Pi_M J_H)=0 is parent-derived off shell",
            "blocker": "Pi_M dJ_H and [d,Pi_M]J_H are not both zero by parent identity",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE920_1_A_exact",
            "claim": "flat A_M is exact with zero compact holonomy",
            "blocker": "requires parent-selected H1(D)=0/no-defect local domain and boundary gauge",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE920_2_coupling_silence",
            "claim": "mass-gauge coupling is silent",
            "blocker": "919 strong theorem lacks off-shell current closure and boundary/holonomy signing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE920_3_local_GR_PPN",
            "claim": "R10/local-GR/PPN branch passes from this route",
            "blocker": "force-bound pack is schema-only and no numeric/source-backed local bounds are loaded",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "build the weak-field map from F_M_force/K_BF_H/dPiMJ_leak/A_M_holonomy to local PPN, WEP, clock, orbital, and R10 bound inputs",
            "include": "units, projection convention, force normalization, link to existing PiM commutator runner, source-path requirements, nonclaim smoke rows",
            "exclude": "claiming silence, claiming local-GR pass, free G/M absorption, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        }
    ]


def formalization_changed_count() -> int:
    formalization = ROOT.parent / "formalization-workbench"
    if not formalization.exists():
        return 0
    return sum(
        1
        for path in formalization.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def all_false(rows: list[dict[str, object]], fields: tuple[str, ...]) -> bool:
    return all(str(row.get(field, "")).strip().lower() != "true" for row in rows for field in fields)


def validation_rows(
    src: list[dict[str, object]],
    closure: list[dict[str, object]],
    holonomy: list[dict[str, object]],
    source_ready: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
) -> list[dict[str, object]]:
    source_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in src)
    prior = OUT / "P8_Y5_BRR545_919_VALIDATION.csv"
    prior_ok = prior.exists() and "V919_12_validation_rows_ready" in read_text(prior)
    false_fields = ("parent_signed", "claim_allowed", "valid_for_claim")
    symbols = {row["symbol"] for row in source_ready}
    required = {"F_M_force", "K_BF_H", "dPiMJ_leak", "A_M_holonomy", "B_zero_flux"}
    changed = formalization_changed_count()
    generated = closure + holonomy + source_ready + decisions + gates
    return [
        {
            "check_id": "V920_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "missing source or needle",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V920_1_prior_919_clean",
            "result": "pass" if prior_ok else "fail",
            "detail": "P8_Y5_BRR545_919_VALIDATION.csv clean" if prior_ok else "919 validation missing or incomplete",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V920_2_offshell_closure_not_signed",
            "result": "pass" if all_false(closure, false_fields) else "fail",
            "detail": "closure factorization written but no parent-signed claim rows",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V920_3_holonomy_conditional_only",
            "result": "pass" if all_false(holonomy, false_fields) and any(row["status"] == "promising_geometry_condition_not_parent_signed" for row in holonomy) else "fail",
            "detail": "H1-zero route is identified as conditional geometry, not promoted",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V920_4_source_ready_rows_nonclaim",
            "result": "pass" if all_false(source_ready, false_fields) and required <= symbols else "fail",
            "detail": "force-bound schema rows include required symbols and remain nonclaim",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V920_5_claim_gates_false",
            "result": "pass" if all_false(gates, false_fields) else "fail",
            "detail": "off-shell closure, exact A, coupling silence, and local-GR gates remain false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V920_6_decisions_nonclaim",
            "result": "pass" if all_false(decisions, false_fields) else "fail",
            "detail": "branch decisions select weak-field bound mapping without promotion",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V920_7_all_generated_rows_nonclaim",
            "result": "pass" if all_false(generated, false_fields) else "fail",
            "detail": "all generated rows keep guarded claim fields false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V920_8_formalization_workbench_untouched",
            "result": "pass" if changed == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={changed}",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V920_9_next_target_selected",
            "result": "pass" if NEXT_TARGET.startswith("921-") else "fail",
            "detail": NEXT_TARGET,
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V920_10_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
            "generated_utc": GENERATED,
        },
    ]


def write_doc(
    src: list[dict[str, object]],
    summary: list[dict[str, object]],
    closure: list[dict[str, object]],
    holonomy: list[dict[str, object]],
    source_ready: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    body = f"""# 920 - Y5/R10 PiM Current Off-Shell Closure And Holonomy Zero Or FM Force Bound

Private coupling/local-source checkpoint. This is not a public R10, WEP, fifth-force, Newton, PPN, local-GR, or unified-field claim.

Status: `{STATUS}`

Claim ceiling: `{CLAIM_CEILING}`

Current result: **zero holonomy has a plausible local-geometry path, but off-shell projected-current closure is still not derived.**

The key split is:

```text
d(Pi_M J_H) = Pi_M dJ_H + [d,Pi_M] J_H.
```

Ward conservation helps the first term only on the right shell. The second term vanishes only if `Pi_M` is parent-owned as an absolute/Hamiltonian mass charge, not a readout mask. That is still open.

For the gauge field:

```text
dA_M=0 and H1(D_local)=0  =>  A_M=d lambda_M.
```

So the holonomy side is not hopeless; it needs parent-selected admissible local domains with no mass-gauge line defects and fixed boundary gauge. Until then, the honest state is: conditional geometry support, no claim, and source-ready bound rows.

## Non-Claim Summary

{md_table(summary, ["status", "claim_ceiling", "current_result", "practical_meaning", "next_target", "valid_for_claim", "generated_utc"])}

## Source Register

{md_table(src, ["source_id", "path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"])}

## Off-Shell Closure Audit

{md_table(closure, ["closure_id", "target", "identity_or_test", "result", "blocker", "parent_signed", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Holonomy Zero Audit

{md_table(holonomy, ["holonomy_id", "condition", "math_test", "result", "blocker", "status", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Source-Ready Force Bound Pack

{md_table(source_ready, ["row_id", "symbol", "units_or_dimension", "formula", "required_columns", "current_status", "valid_for_claim", "generated_utc"])}

## Branch Decision

{md_table(decisions, ["decision_id", "branch", "verdict", "reason", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Claim Gate

{md_table(gates, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Next Target

{md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])}

## Validation

{md_table(validation, ["check_id", "result", "detail", "generated_utc"])}
"""
    (ROOT / DOC_NAME).write_text(body, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    src = sources()
    summary = summary_rows()
    closure = closure_rows()
    holonomy = holonomy_rows()
    source_ready = source_ready_rows()
    decisions = decision_rows()
    gates = gate_rows()
    next_target = next_rows()
    validation = validation_rows(src, closure, holonomy, source_ready, decisions, gates)

    write_csv(OUT / "P8_Y5_R10_920_SOURCE_REGISTER.csv", src, ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_920_NONCLAIM_SUMMARY.csv", summary, ["status", "claim_ceiling", "current_result", "practical_meaning", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_920_OFFSHELL_CLOSURE_AUDIT.csv", closure, ["closure_id", "target", "identity_or_test", "result", "blocker", "parent_signed", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_920_HOLONOMY_ZERO_AUDIT.csv", holonomy, ["holonomy_id", "condition", "math_test", "result", "blocker", "status", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_920_SOURCE_READY_FORCE_BOUND_PACK.csv", source_ready, ["row_id", "symbol", "units_or_dimension", "formula", "required_columns", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_920_BRANCH_DECISION.csv", decisions, ["decision_id", "branch", "verdict", "reason", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_920_CLAIM_GATE.csv", gates, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_920_NEXT_TARGET.csv", next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_BRR545_920_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(src, summary, closure, holonomy, source_ready, decisions, gates, next_target, validation)

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        raise SystemExit(f"validation failed: {failed}")
    print(STATUS)
    print(f"wrote {ROOT / DOC_NAME}")
    print(f"next target: {NEXT_TARGET}")


if __name__ == "__main__":
    main()
