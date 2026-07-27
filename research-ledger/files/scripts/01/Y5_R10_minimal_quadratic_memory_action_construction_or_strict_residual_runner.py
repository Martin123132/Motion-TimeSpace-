from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "970-Y5-R10-minimal-quadratic-memory-action-construction-or-strict-residual-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _field in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join([header, separator, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    since = SCRIPT_START_UTC.astimezone().strftime("%Y-%m-%dT%H:%M:%S")
    literal = str(FORMALIZATION).replace("'", "''")
    command = (
        "$since=[datetime]::Parse('"
        + since
        + "'); "
        + "$count=(Get-ChildItem -LiteralPath '"
        + literal
        + "' -Recurse -File | Where-Object { $_.LastWriteTime -gt $since } | Measure-Object).Count; "
        + "Write-Output $count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    try:
        return int(completed.stdout.strip().splitlines()[-1])
    except (IndexError, ValueError):
        return -2


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "969_doc",
            "path": "969-Y5-R10-parent-memory-operator-owner-hunt-or-readout-domain-certificate.md",
            "role": "handoff selecting minimal quadratic memory action or strict residual runner",
            "needle": "MACT969_0_quadratic_action",
        },
        {
            "source_id": "969_targets",
            "path": "source-intake/mts_residuals/P8_Y5_R10_969_MINIMAL_ACTION_CONSTRUCTION_TARGETS.csv",
            "role": "minimal action construction target table",
            "needle": "MACT969_4_residual_runner",
        },
        {
            "source_id": "967_memory_lemma",
            "path": "source-intake/mts_residuals/P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv",
            "role": "relative positive-operator memory lemma",
            "needle": "MPO967_6_verdict",
        },
        {
            "source_id": "557_doc",
            "path": "557-Y5-Cextra-bulk-memory-range-positive-operator-zero-or-Yukawa-bound-fill.md",
            "role": "earlier positive massive operator attempt and mass-gap warning",
            "needle": "BMR557_5_mass_gap_not_enough",
        },
        {
            "source_id": "557_positive_operator",
            "path": "source-intake/mts_residuals/P8_Y5_CEXTRA_BULK_MEMORY_RANGE_POSITIVE_OPERATOR_ATTEMPT.csv",
            "role": "positive massive elliptic operator template",
            "needle": "positive massive elliptic operator",
        },
        {
            "source_id": "557_force_law",
            "path": "source-intake/mts_residuals/P8_Y5_CEXTRA_BULK_MEMORY_RANGE_FORCE_LAW_MAP.csv",
            "role": "finite memory/range fallback force-law map",
            "needle": "memory_history_kernel",
        },
        {
            "source_id": "476_doc",
            "path": "476-double-zero-memory-coupling-origin-or-coefficient-runner.md",
            "role": "double-zero memory gate requirement",
            "needle": "p >= 2 is the minimum local-GR-safe memory gate",
        },
        {
            "source_id": "476_variation",
            "path": "source-intake/mts_residuals/P8_DOUBLE_ZERO_MEMORY_VARIATION_TEST.csv",
            "role": "linear gate rejection and quadratic gate sufficiency test",
            "needle": "pass_as_sufficient_contract",
        },
        {
            "source_id": "506_energy_identity",
            "path": "source-intake/mts_residuals/P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
            "role": "extra-sector energy identity and memory-kernel silence conditions",
            "needle": "E506_memory_kernel_silence",
        },
        {
            "source_id": "507_acceptance_gates",
            "path": "source-intake/mts_residuals/P8_FIELD_SPECIFIC_SILENCE_ACCEPTANCE_GATES.csv",
            "role": "theorem-zero and numeric-bound acceptance gates",
            "needle": "G507_0_theorem_zero",
        },
        {
            "source_id": "417_boundary",
            "path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "role": "boundary exchange and Bianchi ownership blockers",
            "needle": "Bianchi_gate_owned",
        },
        {
            "source_id": "421_fibre",
            "path": "421-finite-fibre-spectrum-decoupling-theorem-attempt.md",
            "role": "finite-fibre mass gap and source-independence blockers",
            "needle": "universal_stationary_spectrum_derived",
        },
        {
            "source_id": "856_projection",
            "path": "source-intake/mts_residuals/P8_Y5_R10_856_MEMORY_PROJECTION_REPAIR_CONTRACT.csv",
            "role": "memory projection source and conservation guard",
            "needle": "RPC856_1_response_source",
        },
        {
            "source_id": "963_scalar_owner",
            "path": "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md",
            "role": "no-integrated-out-tower and scalar-mode owner blocker",
            "needle": "NES963_3_no_integrated_out_tower",
        },
    ]
    rows = []
    for spec in specs:
        absolute_path = source_path(spec["path"])
        exists = absolute_path.exists()
        needle_found = spec["needle"] in read_text(absolute_path) if exists else False
        rows.append(
            {
                **spec,
                "absolute_path": str(absolute_path),
                "exists": flag(exists),
                "needle_found": flag(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def quadratic_memory_action_construction() -> list[dict[str, str]]:
    specs = [
        {
            "row_id": "QMA970_0_action",
            "construction_piece": "minimal quadratic parent-memory action candidate",
            "mathematical_form": "S_X = 1/2 int_D sqrt(gamma) [A^ij nabla_i X nabla_j X + m_X^2 X^2 - 2 J_X X] + S_boundary",
            "derivation_result": "FORMAL_CANDIDATE_CONSTRUCTED_NOT_PARENT_SIGNED",
            "missing_parent_input": "X as parent/auxiliary variable before readout; A^ij owner; m_X^2 owner; J_X source map; boundary class",
            "effect": "supplies an operator target but not a theorem-zero",
        },
        {
            "row_id": "QMA970_1_variation",
            "construction_piece": "Euler-Lagrange variation",
            "mathematical_form": "delta S_X gives L_X X = J_X with L_X = -nabla_i(A^ij nabla_j) + m_X^2, plus boundary term Pi_X delta X on partial D",
            "derivation_result": "RELATIVE_VARIATION_OK",
            "missing_parent_input": "boundary condition and proof that the varied X-sector is in the parent domain",
            "effect": "if accepted, this is the operator owner 969 was missing",
        },
        {
            "row_id": "QMA970_2_positivity",
            "construction_piece": "positive-operator energy identity",
            "mathematical_form": "<X,L_X X> = int_D [A^ij nabla_i X nabla_j X + m_X^2 X^2] + boundary_flux",
            "derivation_result": "CONDITIONAL_POSITIVITY_OK_INPUTS_UNSIGNED",
            "missing_parent_input": "A^ij positive, m_X^2 >= 0, zero-mode removal, no sign-indefinite memory kernel",
            "effect": "would prove X=0 only when J_X=0 and boundary flux is killed",
        },
        {
            "row_id": "QMA970_3_source_silence",
            "construction_piece": "source decomposition",
            "mathematical_form": "J_X = J_matter + J_chiD_wall + J_boundary_exchange + J_readout + J_history",
            "derivation_result": "NOT_DERIVED",
            "missing_parent_input": "matter blindness; chi_D wall silence; Bianchi-owned boundary current; no pre-variation readout source; local memory kernel",
            "effect": "blocks active positive-operator theorem-zero",
        },
        {
            "row_id": "QMA970_4_boundary_zero_mode",
            "construction_piece": "boundary and zero-mode package",
            "mathematical_form": "Dirichlet X=0 or zero flux plus zero mean/topological class on partial D",
            "derivation_result": "NOT_DERIVED",
            "missing_parent_input": "parent-selected local domain D; relative-current no-hair; constant-sector universality",
            "effect": "constant and boundary hair remain possible",
        },
        {
            "row_id": "QMA970_5_double_zero_tension",
            "construction_piece": "double-zero gated memory branch",
            "mathematical_form": "S_mem = int sqrt(-g) f(chi_D) L_X[X] with f(0)=0 and f_prime(0)=0",
            "derivation_result": "BRANCH_TENSION_FOUND",
            "missing_parent_input": "parent origin for f; proof that operator remains active if X=0 theorem is claimed",
            "effect": "double-zero decouples local stress/selector exchange, but if it gates the kinetic action it also makes the X operator degenerate at chi_D=0 and does not prove X=0",
        },
        {
            "row_id": "QMA970_6_integrated_out_tower",
            "construction_piece": "integrating out X",
            "mathematical_form": "S_eff contains -1/2 <J_X,L_X^{-1}J_X> plus boundary/readout terms when J_X is nonzero",
            "derivation_result": "NOT_DERIVED",
            "missing_parent_input": "no integrated-out curvature/scalar/nonlocal tower certificate",
            "effect": "could regenerate R10/R11/f(R)-like leakage unless J_X and boundary terms are actually zero",
        },
        {
            "row_id": "QMA970_7_verdict",
            "construction_piece": "minimal quadratic action verdict",
            "mathematical_form": "active operator route and double-zero decoupling route are distinct proof branches",
            "derivation_result": "CONSTRUCTION_RELATIVE_NOT_PARENT_CLOSED",
            "missing_parent_input": "branch selection from parent action plus source/boundary/no-tower signatures",
            "effect": "memory remains retained residual or closure branch; no local-GR claim",
        },
    ]
    return [
        {
            **spec,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def branch_audit() -> list[dict[str, str]]:
    specs = [
        {
            "branch_id": "ADB970_0_active_positive_operator",
            "branch": "active positive operator",
            "local_mechanism": "keep L_X active in the local exterior and prove X=0 from positivity, J_X=0, and zero boundary flux",
            "theorem_credit": "possible only under signed source/boundary/gap premises",
            "residual_risk": "if any source or boundary lift survives, X becomes a finite local scalar/Yukawa residual",
            "status": "PROMISING_BUT_UNSIGNED",
            "next_action": "derive J_X=0 and boundary flux zero, or score residual",
        },
        {
            "branch_id": "ADB970_1_double_zero_decoupling",
            "branch": "double-zero decoupling",
            "local_mechanism": "multiply the memory contribution by f(chi_D) with f(0)=f_prime(0)=0",
            "theorem_credit": "closure-silences stress and selector exchange at chi_D=0, but does not prove X=0 if the operator is also switched off",
            "residual_risk": "X can remain unscored hidden data unless observable couplings are proven zero or bounded",
            "status": "CLOSURE_SAFE_NOT_ZERO_PROOF",
            "next_action": "do not use this as a positive-operator theorem-zero",
        },
        {
            "branch_id": "ADB970_2_hybrid_active_hidden_gated_observed",
            "branch": "hybrid active-hidden/gated-observed",
            "local_mechanism": "let X obey an active parent operator while only observed stress/couplings are double-zero gated",
            "theorem_credit": "would be powerful if Bianchi and variation ownership are signed",
            "residual_risk": "risks smuggling readout closure into parent variation or breaking conservation",
            "status": "NOT_DERIVED",
            "next_action": "requires explicit parent split between operator action and observed coupling action",
        },
        {
            "branch_id": "ADB970_3_verdict",
            "branch": "branch fork verdict",
            "local_mechanism": "positive operator kills X; double-zero gate decouples X locally",
            "theorem_credit": "not interchangeable",
            "residual_risk": "conflating them would create a fake local-GR pass",
            "status": "BRANCH_FORK_UNRESOLVED",
            "next_action": "971 must choose or derive the parent branch, otherwise fill strict residual inputs",
        },
    ]
    return [
        {
            **spec,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def source_boundary_gate() -> list[dict[str, str]]:
    specs = [
        {
            "gate_id": "SBG970_0_J_matter",
            "gate": "ordinary matter has no X charge",
            "needed_condition": "J_matter=0 in compact local exterior",
            "gate_pass": "false",
            "blocker": "matter blindness/descent does not yet prove no X vertex",
        },
        {
            "gate_id": "SBG970_1_J_chiD_wall",
            "gate": "domain selector creates no wall source",
            "needed_condition": "J_chiD_wall=0 and no hidden f_prime L_mem exchange",
            "gate_pass": "false",
            "blocker": "double-zero gate is only a requirement/contract, not a parent-derived action origin",
        },
        {
            "gate_id": "SBG970_2_J_boundary_exchange",
            "gate": "boundary exchange current is silent",
            "needed_condition": "relative boundary current exact/zero and Bianchi-owned",
            "gate_pass": "false",
            "blocker": "417 Bianchi/boundary no-hair route remains unsigned",
        },
        {
            "gate_id": "SBG970_3_J_readout",
            "gate": "readout creates no pre-variation source",
            "needed_condition": "readout is after-variation only or excluded from Conf_parent",
            "gate_pass": "false",
            "blocker": "readout certificate is closure discipline, not primitive parent theorem-zero",
        },
        {
            "gate_id": "SBG970_4_J_history",
            "gate": "memory history kernel is local/stable/source-free",
            "needed_condition": "no nonlocal tail, no local history injection, no time drift",
            "gate_pass": "false",
            "blocker": "E506 lists this as a needed condition, not an achieved proof",
        },
        {
            "gate_id": "SBG970_5_boundary_flux",
            "gate": "boundary flux vanishes",
            "needed_condition": "Pi_X delta X or X n.A.grad X boundary term is zero",
            "gate_pass": "false",
            "blocker": "no parent-selected D plus no-hair boundary package",
        },
        {
            "gate_id": "SBG970_6_zero_mode",
            "gate": "constant/topological mode removed or universal",
            "needed_condition": "m_X^2>0 or zero mean/topological class fixed as universal calibration",
            "gate_pass": "false",
            "blocker": "finite-fibre/source-independence and constant-sector universality remain open",
        },
        {
            "gate_id": "SBG970_7_observable_map",
            "gate": "observable couplings are zero or source-backed",
            "needed_condition": "K_clock, K_Gdot, K_R10, K_PPN, K_orbital have units/source paths",
            "gate_pass": "false",
            "blocker": "projection coupling vector remains placeholder/missing",
        },
        {
            "gate_id": "SBG970_8_verdict",
            "gate": "active memory zero source/boundary package",
            "needed_condition": "all previous gates pass",
            "gate_pass": "false",
            "blocker": "zero-source and boundary premises fail; no active memory theorem-zero",
        },
    ]
    return [
        {
            **spec,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def no_integrated_out_tower_gate() -> list[dict[str, str]]:
    specs = [
        {
            "tower_id": "NIT970_0_zero_solution_case",
            "tower_risk": "solving X with J_X=0 and zero boundary data",
            "mechanism": "X=0 or universal constant gives no finite Green-function tail",
            "current_status": "CONDITIONAL_SAFE_ONLY_IF_SOURCE_BOUNDARY_GATES_PASS",
            "blocker": "source and boundary gates do not pass",
        },
        {
            "tower_id": "NIT970_1_nonzero_source_case",
            "tower_risk": "solving X with J_X nonzero",
            "mechanism": "substitution generates nonlocal term -1/2 <J_X,L_X^{-1}J_X>",
            "current_status": "RETAINED_R10_R11_RISK",
            "blocker": "J_X source map has no sourced zero or numeric amplitude",
        },
        {
            "tower_id": "NIT970_2_curvature_coupled_case",
            "tower_risk": "X couples to R, T, boundary curvature, or observed coframe",
            "mechanism": "integrating out can mimic R2/fR/scalar-tensor/local fifth-force operators",
            "current_status": "NOT_EXCLUDED",
            "blocker": "963 no-integrated-out-tower and no-extra-scalar gates remain unsigned",
        },
        {
            "tower_id": "NIT970_3_readout_reduced_case",
            "tower_risk": "varying a readout-reduced action",
            "mechanism": "creates a new EFT branch rather than a parent theorem-zero",
            "current_status": "FORBIDDEN_AS_THEOREM_CREDIT",
            "blocker": "readout-domain certificate forbids smuggling closure into variation",
        },
        {
            "tower_id": "NIT970_4_verdict",
            "tower_risk": "no integrated-out memory/scalar tower",
            "mechanism": "requires exact parent second-order/no-extra-scalar or exact X=0 before reduction",
            "current_status": "NOT_DERIVED",
            "blocker": "active zero theorem and no-extra-scalar signature both remain open",
        },
    ]
    return [
        {
            **spec,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def residual_runner_schema() -> list[dict[str, str]]:
    specs = [
        {
            "field_id": "RRS970_0_row_id",
            "branch": "all",
            "required_input": "row_id and branch label",
            "expected_units": "dimensionless labels",
            "source_requirement": "each row must identify active_positive_operator, double_zero_decoupling, hybrid, or finite_residual",
            "placeholder_status": "schema_only",
        },
        {
            "field_id": "RRS970_1_lambda_gap",
            "branch": "finite_residual",
            "required_input": "lambda_gap or m_X with conversion to range",
            "expected_units": "metres or inverse metres",
            "source_requirement": "parent Hessian/operator source path or real calibrated source",
            "placeholder_status": "MISSING_PARENT_INPUT",
        },
        {
            "field_id": "RRS970_2_J_X_norm",
            "branch": "active_positive_operator_or_finite_residual",
            "required_input": "J_X_norm and decomposition across matter, chiD, boundary, readout, history",
            "expected_units": "operator-normalized source units",
            "source_requirement": "parent current/source derivation with units",
            "placeholder_status": "MISSING_SOURCE_MAP",
        },
        {
            "field_id": "RRS970_3_boundary_lift_norm",
            "branch": "all",
            "required_input": "boundary_lift_norm or exact zero certificate",
            "expected_units": "same norm as X or operator boundary flux",
            "source_requirement": "parent-selected D and no-hair/boundary-current source path",
            "placeholder_status": "MISSING_BOUNDARY_PACKAGE",
        },
        {
            "field_id": "RRS970_4_K_clock",
            "branch": "finite_residual",
            "required_input": "projection coefficient into clock/frequency tests",
            "expected_units": "observable per X",
            "source_requirement": "clock readout/projection derivation and bound source",
            "placeholder_status": "MISSING_ARENA_PROJECTION",
        },
        {
            "field_id": "RRS970_5_K_Gdot",
            "branch": "finite_residual",
            "required_input": "projection coefficient into Gdot/time drift",
            "expected_units": "1/time per X or dimensionless normalized coefficient",
            "source_requirement": "time-drift projection derivation and bound source",
            "placeholder_status": "MISSING_ARENA_PROJECTION",
        },
        {
            "field_id": "RRS970_6_K_R10",
            "branch": "finite_residual",
            "required_input": "Yukawa/fifth-force alpha(lambda) coefficient",
            "expected_units": "dimensionless alpha at range lambda",
            "source_requirement": "source-backed coefficient plus real bound curve",
            "placeholder_status": "MISSING_ARENA_PROJECTION",
        },
        {
            "field_id": "RRS970_7_K_PPN",
            "branch": "finite_residual",
            "required_input": "gamma, beta, alpha1, alpha2, alpha3, xi projection vector",
            "expected_units": "dimensionless PPN coefficients",
            "source_requirement": "weak-field projection map and official bound source",
            "placeholder_status": "MISSING_ARENA_PROJECTION",
        },
        {
            "field_id": "RRS970_8_K_orbital",
            "branch": "finite_residual",
            "required_input": "perihelion/range/orbital residual coefficient",
            "expected_units": "observable residual per X",
            "source_requirement": "orbital projection map and bound source",
            "placeholder_status": "MISSING_ARENA_PROJECTION",
        },
        {
            "field_id": "RRS970_9_valid_for_claim",
            "branch": "all",
            "required_input": "valid_for_claim boolean",
            "expected_units": "boolean",
            "source_requirement": "true only if numeric sourced inputs and bound comparison pass",
            "placeholder_status": "FORCED_FALSE_THIS_CHECKPOINT",
        },
    ]
    return [
        {
            **spec,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def residual_runner_dryrun() -> list[dict[str, str]]:
    specs = [
        {
            "dryrun_id": "RRD970_0_live_current",
            "scenario": "current live memory files",
            "input_summary": "operator owner absent; source/boundary/couplings missing",
            "runner_result": "REJECTED_NOT_SCOREABLE",
            "reject_reason": "missing lambda_gap, J_X_norm, boundary_lift_norm, arena K_i, and bound sources",
        },
        {
            "dryrun_id": "RRD970_1_active_zero_candidate",
            "scenario": "minimal active positive-operator zero branch",
            "input_summary": "formal L_X candidate exists but J_X=0 and boundary flux zero are unsigned",
            "runner_result": "REJECTED_NO_THEOREM_ZERO",
            "reject_reason": "positive operator alone is not enough; source and boundary gates fail",
        },
        {
            "dryrun_id": "RRD970_2_double_zero_candidate",
            "scenario": "double-zero decoupling branch",
            "input_summary": "f(0)=f_prime(0)=0 silences local stress/selector exchange as a contract",
            "runner_result": "REJECTED_AS_ZERO_PROOF",
            "reject_reason": "decoupling does not prove X=0 and cannot replace residual coefficients",
        },
        {
            "dryrun_id": "RRD970_3_hybrid_candidate",
            "scenario": "active hidden operator plus double-zero observed coupling",
            "input_summary": "would preserve X equation while gating local observed stress",
            "runner_result": "REJECTED_PARENT_SPLIT_MISSING",
            "reject_reason": "needs Bianchi/variation owner for operator-action vs observed-coupling split",
        },
        {
            "dryrun_id": "RRD970_4_acceptance_contract",
            "scenario": "future scoreable retained residual row",
            "input_summary": "numeric sourced lambda_gap, J_X_norm, boundary lift, K_i, bound source, and units",
            "runner_result": "WOULD_ACCEPT_IF_ALL_FIELDS_REAL_AND_BOUNDS_PASS",
            "reject_reason": "contract only; no current row has the required real inputs",
        },
    ]
    return [
        {
            **spec,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def claim_gates() -> list[dict[str, str]]:
    specs = [
        {
            "gate_id": "CGATE970_0_parent_action_owner",
            "claim": "minimal quadratic memory action is parent-owned",
            "required_condition": "X-sector appears in S_parent before readout with signed A^ij, m_X^2, J_X, and boundary terms",
            "current_evidence": "formal candidate constructed only",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE970_1_active_memory_zero",
            "claim": "active positive-operator branch proves X=0",
            "required_condition": "positive operator plus J_X=0 plus boundary/zero-mode package",
            "current_evidence": "source and boundary gates fail",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE970_2_double_zero_theorem_zero",
            "claim": "double-zero memory gate proves X=0",
            "required_condition": "operator remains active or independent zero proof exists",
            "current_evidence": "double-zero decouples stress but can degenerate the operator",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE970_3_memory_residual_score",
            "claim": "finite memory residual can be scored against local arenas",
            "required_condition": "numeric sourced lambda, amplitude/source norm, projection K_i, units, and bounds",
            "current_evidence": "strict schema created; all current rows nonclaim",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE970_4_no_integrated_out_tower",
            "claim": "integrating out memory cannot regenerate R10/R11/non-EH leakage",
            "required_condition": "X=0 before reduction or exact no-extra-scalar/no-tower theorem",
            "current_evidence": "963 no-tower gate remains unsigned",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE970_5_local_GR",
            "claim": "local GR/Newton/PPN promotion from memory sector",
            "required_condition": "accepted memory zero theorem or scoreable residual below all local bounds",
            "current_evidence": "neither theorem-zero nor residual score exists",
            "gate_pass": "false",
        },
    ]
    return [
        {
            **spec,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def decisions() -> list[dict[str, str]]:
    specs = [
        {
            "decision_id": "DEC970_0_minimal_action",
            "topic": "minimal quadratic memory action",
            "result": "relative_candidate_only",
            "reason": "variation gives the desired L_X form, but parent ownership, sources, boundary, and no-tower gates are unsigned",
            "next_action": "do not promote; use as a construction target",
        },
        {
            "decision_id": "DEC970_1_branch_tension",
            "topic": "active zero vs double-zero decoupling",
            "result": "fork_must_be_kept_explicit",
            "reason": "positive operator can kill X; double-zero can silence observed stress; they are not the same proof",
            "next_action": "derive a parent branch selector or choose closure-only branch",
        },
        {
            "decision_id": "DEC970_2_residual_runner",
            "topic": "strict memory residual runner",
            "result": "schema_written_nonclaim",
            "reason": "if derivation fails, memory must become a source-backed residual, not a mist parameter",
            "next_action": "fill lambda_gap, J_X_norm, boundary lift, and K_i with real source paths before scoring",
        },
        {
            "decision_id": "DEC970_3_best_next",
            "topic": "next checkpoint",
            "result": "active_vs_double_zero_branch_choice_or_runner_fill",
            "reason": "the current obstruction is not algebraic manipulation; it is choosing what the parent action really owns",
            "next_action": "try to derive active hidden operator plus double-zero observed coupling split; if not, demote memory to retained residual runner",
        },
    ]
    return [
        {
            **spec,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "971-Y5-R10-active-memory-zero-vs-double-zero-decoupling-branch-choice-or-runner-fill.md",
            "objective": "derive whether parent MTS selects an active positive-operator memory zero branch, a double-zero observed-decoupling branch, or a retained finite residual runner",
            "include": "operator-action vs observed-coupling split, Bianchi ownership, source/boundary zero tests, residual input minimums",
            "exclude": "local-GR claim, invented numeric coefficients, readout closure as theorem-zero, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation(
    sources: list[dict[str, str]],
    qma_rows: list[dict[str, str]],
    branch_rows: list[dict[str, str]],
    source_boundary_rows: list[dict[str, str]],
    tower_rows: list[dict[str, str]],
    schema_rows: list[dict[str, str]],
    dryrun_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    formalization_count = formalization_changed_after_start()
    rows = [
        {
            "check_id": "V970_0_source_paths_exist",
            "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail",
            "detail": "all cited local source paths exist",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V970_1_source_needles_found",
            "result": "pass" if all(row["needle_found"] == "true" for row in sources) else "fail",
            "detail": "all source needles found",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V970_2_quadratic_action_constructed",
            "result": "pass"
            if any(row["row_id"] == "QMA970_0_action" and "FORMAL_CANDIDATE" in row["derivation_result"] for row in qma_rows)
            else "fail",
            "detail": "minimal quadratic action candidate is written as a construction target",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V970_3_variation_relative_only",
            "result": "pass"
            if any(row["row_id"] == "QMA970_1_variation" and row["derivation_result"] == "RELATIVE_VARIATION_OK" for row in qma_rows)
            and any(row["row_id"] == "QMA970_7_verdict" and "NOT_PARENT_CLOSED" in row["derivation_result"] for row in qma_rows)
            else "fail",
            "detail": "variation is accepted only as relative construction, not parent closure",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V970_4_branch_tension_recorded",
            "result": "pass"
            if any(row["branch_id"] == "ADB970_3_verdict" and row["status"] == "BRANCH_FORK_UNRESOLVED" for row in branch_rows)
            else "fail",
            "detail": "active positive-operator zero and double-zero decoupling are explicitly separated",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V970_5_source_boundary_gates_blocked",
            "result": "pass" if all(row["gate_pass"] == "false" for row in source_boundary_rows) else "fail",
            "detail": "zero-source and boundary package remain blocked",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V970_6_no_integrated_out_tower_blocked",
            "result": "pass"
            if any(row["tower_id"] == "NIT970_4_verdict" and row["current_status"] == "NOT_DERIVED" for row in tower_rows)
            else "fail",
            "detail": "no integrated-out memory/scalar tower certificate remains unsigned",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V970_7_residual_schema_nonclaim",
            "result": "pass" if all(row["valid_for_claim"] == "false" for row in schema_rows) else "fail",
            "detail": "strict residual schema rows are nonclaim placeholders",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V970_8_dryrun_rejects_current_claims",
            "result": "pass" if all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in dryrun_rows) else "fail",
            "detail": "dry-run blocks live, active-zero, double-zero, and hybrid rows from claim credit",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V970_9_claim_gates_false",
            "result": "pass" if all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows) else "fail",
            "detail": "all memory/local-GR claim gates remain false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V970_10_decisions_nonclaim",
            "result": "pass" if all(row["claim_allowed"] == "false" for row in decision_rows) else "fail",
            "detail": "decision ledger does not promote memory or local GR",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V970_11_next_target_written",
            "result": "pass" if len(target_rows) == 1 and target_rows[0]["valid_for_claim"] == "false" else "fail",
            "detail": "971 branch-choice/residual-fill target selected",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V970_12_formalization_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization-workbench modified-file count since script start is {formalization_count}",
            "generated_utc": stamp(),
        },
    ]
    rows.append(
        {
            "check_id": "V970_13_validation_rows_ready",
            "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail",
            "detail": "970 validation pack assembled",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, str]],
    qma_rows: list[dict[str, str]],
    branch_rows: list[dict[str, str]],
    source_boundary_rows: list[dict[str, str]],
    tower_rows: list[dict[str, str]],
    schema_rows: list[dict[str, str]],
    dryrun_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 970 Y5 R10: Minimal Quadratic Memory Action Construction Or Strict Residual Runner

Status: `Y5_R10_970_minimal_quadratic_memory_action_relative_candidate_branch_fork_found_memory_residual_runner_schema_nonclaim`

Claim ceiling: no parent memory action owner, no memory theorem-zero, no double-zero theorem-zero, no memory residual bound pass, no R10/R11 pass, no EH/Newton/local-GR claim is made.

## Readout

This checkpoint built the minimal action we would want if memory is to be more than a mist:

`S_X = 1/2 int_D sqrt(gamma) [A^ij nabla_i X nabla_j X + m_X^2 X^2 - 2 J_X X] + S_boundary`.

The variation works as a relative construction: it gives `L_X X = J_X`. The positivity route also works mathematically if the operator is signed, the source is zero, and the boundary/zero mode is killed.

But the crucial catch is now explicit. The active positive-operator route and the double-zero route are different beasts:

- Active positive operator can prove `X=0`, but only if `J_X=0` and the boundary package are parent-signed.
- Double-zero coupling can silence local memory stress and selector exchange, but if it gates the kinetic/operator action it can also switch off the very operator that would have proven `X=0`.

So 970 is useful progress, not a local-GR pass. It tells us exactly what has to be owned next: either derive a parent split where the hidden memory operator remains active while observed coupling is double-zero gated, or demote memory to a strict retained residual runner with real sourced amplitudes.

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Quadratic Memory Action Construction

{md_table(qma_rows, ["row_id", "construction_piece", "derivation_result", "missing_parent_input", "effect"])}

## Active Vs Double-Zero Branch Audit

{md_table(branch_rows, ["branch_id", "branch", "local_mechanism", "theorem_credit", "status", "next_action"])}

## Source Boundary Gate

{md_table(source_boundary_rows, ["gate_id", "gate", "needed_condition", "gate_pass", "blocker"])}

## No Integrated-Out Tower Gate

{md_table(tower_rows, ["tower_id", "tower_risk", "current_status", "blocker"])}

## Strict Residual Runner Schema

{md_table(schema_rows, ["field_id", "branch", "required_input", "expected_units", "source_requirement", "placeholder_status", "valid_for_claim"])}

## Strict Residual Runner Dryrun

{md_table(dryrun_rows, ["dryrun_id", "scenario", "runner_result", "reject_reason", "valid_for_claim"])}

## Claim Gate

{md_table(claim_rows, ["gate_id", "claim", "current_evidence", "gate_pass", "claim_allowed"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "topic", "result", "reason", "next_action"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

{md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register()
    qma_rows = quadratic_memory_action_construction()
    branch_rows = branch_audit()
    source_boundary_rows = source_boundary_gate()
    tower_rows = no_integrated_out_tower_gate()
    schema_rows = residual_runner_schema()
    dryrun_rows = residual_runner_dryrun()
    claim_rows = claim_gates()
    decision_rows = decisions()
    target_rows = next_target()
    validation_rows = validation(
        sources,
        qma_rows,
        branch_rows,
        source_boundary_rows,
        tower_rows,
        schema_rows,
        dryrun_rows,
        claim_rows,
        decision_rows,
        target_rows,
    )

    write_csv(
        OUT / "P8_Y5_R10_970_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
        qma_rows,
        ["row_id", "construction_piece", "mathematical_form", "derivation_result", "missing_parent_input", "effect", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_970_ACTIVE_VS_DOUBLE_ZERO_BRANCH_AUDIT.csv",
        branch_rows,
        ["branch_id", "branch", "local_mechanism", "theorem_credit", "residual_risk", "status", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_970_SOURCE_BOUNDARY_GATE.csv",
        source_boundary_rows,
        ["gate_id", "gate", "needed_condition", "gate_pass", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_970_NO_INTEGRATED_OUT_TOWER_GATE.csv",
        tower_rows,
        ["tower_id", "tower_risk", "mechanism", "current_status", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_970_STRICT_RESIDUAL_RUNNER_SCHEMA.csv",
        schema_rows,
        ["field_id", "branch", "required_input", "expected_units", "source_requirement", "placeholder_status", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_970_STRICT_RESIDUAL_RUNNER_DRYRUN.csv",
        dryrun_rows,
        ["dryrun_id", "scenario", "input_summary", "runner_result", "reject_reason", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_970_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_970_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_970_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_970_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(
        sources,
        qma_rows,
        branch_rows,
        source_boundary_rows,
        tower_rows,
        schema_rows,
        dryrun_rows,
        claim_rows,
        decision_rows,
        target_rows,
        validation_rows,
    )


if __name__ == "__main__":
    main()
