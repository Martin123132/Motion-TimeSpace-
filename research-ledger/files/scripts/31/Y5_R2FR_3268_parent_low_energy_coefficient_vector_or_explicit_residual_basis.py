from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3268-Y5-R2FR-parent-low-energy-coefficient-vector-or-explicit-residual-basis-under-AX1090.md"
DOC_3267 = ROOT / "3267-Y5-R2FR-parent-source-map-signature-for-DD-coordinates-under-AX1090.md"
SIGNATURE_3267 = OUT / "P8_Y5_R2FR_3267_PARENT_DD_SIGNATURE_THEOREM.csv"
SCALE_3267 = OUT / "P8_Y5_R2FR_3267_ARENA_SCALE_RESIDUAL_LAW.csv"
PROJ_3267 = OUT / "P8_Y5_R2FR_3267_OPERATOR_PROJECTION_TARGETS.csv"
CONST_UNIV = OUT / "P8_constant_sector_universality_CONTRACT.csv"
GLOBAL_SUPER = OUT / "P8_global_coupling_superselection_CONTRACT.csv"
KAPPA_SUPER = OUT / "P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv"
MATTER_955 = OUT / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv"
GUARDS_3008 = OUT / "P8_Y5_R2FR_3008_COUPLING_GUARD_ROWS.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3268_SOURCE_REGISTER.csv",
    "coefficient_vector": OUT / "P8_Y5_R2FR_3268_LOW_ENERGY_COEFFICIENT_VECTOR.csv",
    "projection": OUT / "P8_Y5_R2FR_3268_DD_PROJECTION_MATRIX.csv",
    "forks": OUT / "P8_Y5_R2FR_3268_FIXED_VS_VARIABLE_CONSTANT_FORKS.csv",
    "constraints": OUT / "P8_Y5_R2FR_3268_CONDITIONAL_COEFFICIENT_CONSTRAINTS.csv",
    "residual_basis": OUT / "P8_Y5_R2FR_3268_EXPLICIT_RESIDUAL_BASIS.csv",
    "gates": OUT / "P8_Y5_R2FR_3268_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3268_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3268_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3268_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        read_csv(path)
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def evidence(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_number, line in enumerate(handle, start=1):
            lowered_line = line.lower()
            if any(needle in lowered_line for needle in lowered_needles):
                clean = " ".join(line.strip().split())
                if clean:
                    hits.append(f"L{line_number}:{clean[:280]}")
            if len(hits) >= limit:
                break
    return " | ".join(hits) if hits else "NO_MATCH"


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in columns)
        + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC3268_3267_signature",
            DOC_3267,
            "3267 parent-DD signature theorem",
            ["C_g", "D_hatm=C_hatm-C_g", "eta_k=s_k DeltaQ_k dot D"],
        ),
        (
            "SRC3268_3267_signature_csv",
            SIGNATURE_3267,
            "machine-readable parent-DD signature rows",
            ["SIG3267_0_parent_low_energy_vector", "SIG3267_3_failure_normal_form"],
        ),
        (
            "SRC3268_3267_scale_law",
            SCALE_3267,
            "3267 scale/residual law and conditional bounds",
            ["SCALE3267_2_zero_residual_s_equal_1", "SCALE3267_4_eta_sized_residual_s_equal_1"],
        ),
        (
            "SRC3268_constant_sector",
            CONST_UNIV,
            "constant-sector universality contract",
            ["C4_no_constant_running_from_local_MTS", "C7_empirical_fallback"],
        ),
        (
            "SRC3268_global_superselection",
            GLOBAL_SUPER,
            "global coupling superselection contract",
            ["GS0_configuration_factorization", "GS7_scalar_branch_fallback"],
        ),
        (
            "SRC3268_kappa_superselection",
            KAPPA_SUPER,
            "example of a conditional constant/superselection theorem",
            ["T508_0_global_sector", "T508_1_topological_zeroform"],
        ),
        (
            "SRC3268_minimal_matter",
            MATTER_955,
            "minimal matter action source-coupling lemma",
            ["MMA955_5_minimal_schema", "MMA955_6_verdict"],
        ),
        (
            "SRC3268_coupling_guards",
            GUARDS_3008,
            "coupling guard rows against direct X/constant/source vertices",
            ["CG3008_1_no_direct_X_vertex", "CG3008_6_guard_verdict"],
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, role, needles in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def coefficient_vector_rows() -> list[dict[str, Any]]:
    return [
        {
            "coefficient_id": "C3268_g",
            "symbol": "C_g",
            "definition": "L_X ln Lambda_3, or the parent-generator coefficient of the QCD/gluon scale",
            "DD_role": "universal/common scale; enters D_hatm only through C_hatm-C_g",
            "zero_condition": "local constant superselection gives C_g=0",
            "current_status": "UNSIGNED_PARENT_COEFFICIENT",
            "valid_for_claim": "false",
        },
        {
            "coefficient_id": "C3268_hatm",
            "symbol": "C_hatm",
            "definition": "L_X ln hatm, parent-generator coefficient of average light-quark mass",
            "DD_role": "D_hatm=C_hatm-C_g",
            "zero_condition": "local constant superselection gives C_hatm=0; common-mode C_hatm=C_g kills WEP hatm channel",
            "current_status": "UNSIGNED_PARENT_COEFFICIENT",
            "valid_for_claim": "false",
        },
        {
            "coefficient_id": "C3268_e",
            "symbol": "C_e",
            "definition": "L_X ln alpha_EM, parent-generator coefficient of fine-structure/EM response",
            "DD_role": "D_e=C_e",
            "zero_condition": "EM coefficient stationarity or constant superselection gives C_e=0",
            "current_status": "UNSIGNED_PARENT_COEFFICIENT",
            "valid_for_claim": "false",
        },
        {
            "coefficient_id": "C3268_common",
            "symbol": "C_common",
            "definition": "common low-energy mass-scale shift with C_hatm=C_g and C_e=0",
            "DD_role": "invisible to WEP composition difference at dominant DD order",
            "zero_condition": "not required for WEP; must be handled by clock/G/Newton normalization instead",
            "current_status": "DEGENERACY_IDENTIFIED",
            "valid_for_claim": "false",
        },
    ]


def projection_rows() -> list[dict[str, Any]]:
    return [
        {
            "projection_id": "R3268_0_Dhatm",
            "input_vector": "C=(C_g,C_hatm,C_e)",
            "projection_row": "[-1,+1,0]",
            "output": "D_hatm=C_hatm-C_g",
            "WEP_constraint": "conditional |C_hatm-C_g| bound only, not |C_g| and |C_hatm| separately",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "R3268_1_De",
            "input_vector": "C=(C_g,C_hatm,C_e)",
            "projection_row": "[0,0,+1]",
            "output": "D_e=C_e",
            "WEP_constraint": "conditional |C_e| bound",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "R3268_2_null_common_mode",
            "input_vector": "C=(C_g,C_hatm,C_e)",
            "projection_row": "null vector (1,1,0)",
            "output": "D=(0,0)",
            "WEP_constraint": "dominant DD WEP cannot see a pure common QCD/hatm scale shift",
            "valid_for_claim": "false",
        },
    ]


def fork_rows() -> list[dict[str, Any]]:
    return [
        {
            "fork_id": "FORK3268_0_fixed_local_constants",
            "branch": "fixed local standard constants",
            "premise": "L_X ln Lambda_3 = L_X ln hatm = L_X ln alpha_EM = 0 on the connected local branch",
            "consequence": "C_g=C_hatm=C_e=0, hence D_hatm=D_e=0 and dominant DD WEP source is zero before residual epsilons",
            "status": "CLEAN_ZERO_ROUTE_CONDITIONAL",
            "needed_to_promote": "parent superselection/no-running theorem for these constants plus residual epsilon budgets",
            "valid_for_claim": "false",
        },
        {
            "fork_id": "FORK3268_1_common_mass_scale",
            "branch": "common mass-scale variation",
            "premise": "C_hatm=C_g, C_e=0",
            "consequence": "D_hatm=D_e=0 at dominant DD order; not a WEP signal but may affect absolute G/mass/clock normalization",
            "status": "WEP_ZERO_BUT_NOT_FULL_LOCAL_GR",
            "needed_to_promote": "route common mode into Newton/clock/G normalization gates instead of hiding it",
            "valid_for_claim": "false",
        },
        {
            "fork_id": "FORK3268_2_variable_DD_constants",
            "branch": "finite DD source coupling",
            "premise": "C_hatm-C_g or C_e is nonzero",
            "consequence": "use 3265/3266/3267 matrix bounds after parent signature, scale lock, and residual budgets",
            "status": "BOUNDED_BRANCH_CONDITIONAL",
            "needed_to_promote": "signed parent C vector, s_min rows, epsilon rows",
            "valid_for_claim": "false",
        },
        {
            "fork_id": "FORK3268_3_illegal_hidden_vertex",
            "branch": "direct X/material/source/readout coefficient",
            "premise": "alpha_EM(X), m_A(X), source-only weights, or arena-specific s_k are added outside parent low-energy constants",
            "consequence": "DD coordinates are not MTS-owned; term becomes explicit residual or countermodel",
            "status": "FORBIDDEN_FOR_PROMOTION_RETAIN_AS_RESIDUAL",
            "needed_to_promote": "remove by parent action theorem or bound as explicit coefficient",
            "valid_for_claim": "false",
        },
    ]


def bound_lookup() -> dict[str, str]:
    rows = read_csv(SCALE_3267)
    zero = next(row for row in rows if row["law_id"] == "SCALE3267_2_zero_residual_s_equal_1")
    eta = next(row for row in rows if row["law_id"] == "SCALE3267_4_eta_sized_residual_s_equal_1")
    return {
        "Dhatm_zero": zero["Dhatm_bound"],
        "De_zero": zero["De_bound"],
        "Dhatm_eta": eta["Dhatm_bound"],
        "De_eta": eta["De_bound"],
    }


def constraint_rows() -> list[dict[str, Any]]:
    bounds = bound_lookup()
    return [
        {
            "constraint_id": "CONSTR3268_0_zero_residual_Dhatm",
            "assumptions": "parent signature signed; s_MICROSCOPE=s_EOTWASH=1; epsilon=0",
            "coefficient_constraint": "|C_hatm-C_g| <= |D_hatm|_bound",
            "value": bounds["Dhatm_zero"],
            "what_it_does_not_bound": "C_g common mode and C_hatm common mode separately",
            "valid_for_claim": "false",
        },
        {
            "constraint_id": "CONSTR3268_1_zero_residual_De",
            "assumptions": "parent signature signed; s_MICROSCOPE=s_EOTWASH=1; epsilon=0",
            "coefficient_constraint": "|C_e| <= |D_e|_bound",
            "value": bounds["De_zero"],
            "what_it_does_not_bound": "non-DD EM readout/boundary coefficients hidden in epsilon",
            "valid_for_claim": "false",
        },
        {
            "constraint_id": "CONSTR3268_2_eta_residual_Dhatm",
            "assumptions": "parent signature signed; s=1; epsilon_k allowed up to eta_bound_k",
            "coefficient_constraint": "|C_hatm-C_g| <= residual-degraded |D_hatm|_bound",
            "value": bounds["Dhatm_eta"],
            "what_it_does_not_bound": "C_g common mode and C_hatm common mode separately",
            "valid_for_claim": "false",
        },
        {
            "constraint_id": "CONSTR3268_3_eta_residual_De",
            "assumptions": "parent signature signed; s=1; epsilon_k allowed up to eta_bound_k",
            "coefficient_constraint": "|C_e| <= residual-degraded |D_e|_bound",
            "value": bounds["De_eta"],
            "what_it_does_not_bound": "hidden EM coefficient channels outside DD Q'_e",
            "valid_for_claim": "false",
        },
        {
            "constraint_id": "CONSTR3268_4_common_mode_free",
            "assumptions": "dominant two-channel WEP only",
            "coefficient_constraint": "C_common along (1,1,0) is unconstrained by DD WEP material differences",
            "value": "UNBOUNDED_BY_THIS_ARENA",
            "what_it_does_not_bound": "absolute mass-scale/G/clock normalization",
            "valid_for_claim": "false",
        },
    ]


def residual_basis_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RES3268_0_parent_coefficient_vector",
            "symbol": "C_parent=(C_g,C_hatm,C_e)",
            "role": "if not theorem-zero, this is the minimal finite coefficient vector to source or bound",
            "required_columns": "coefficient;value;units;parent_operator;source_path;normalization;valid_for_claim",
            "current_status": "MISSING_NUMERIC_PARENT_VALUES",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RES3268_1_arena_scale",
            "symbol": "s_MICROSCOPE,s_EOTWASH",
            "role": "row-scale/source/readout normalization in eta_k=s_k DeltaQ_k dot D+epsilon_k",
            "required_columns": "arena;s_min;s_max;source_path;readout_model;valid_for_claim",
            "current_status": "MISSING_SCALE_LOCK_OR_LOWER_BOUND",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RES3268_2_omitted_DD_channels",
            "symbol": "epsilon_k",
            "role": "electron mass, delta m, material tensor, source-profile, readout, and non-DD channels",
            "required_columns": "arena;epsilon_abs_bound;channel_breakdown;source_path;units;valid_for_claim",
            "current_status": "MISSING_EPSILON_BUDGETS",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RES3268_3_common_mode",
            "symbol": "C_common",
            "role": "common low-energy mass-scale variation invisible to WEP but relevant to Newton/clock/G branch",
            "required_columns": "coefficient;target_arena;clock_or_G_bound;source_path;valid_for_claim",
            "current_status": "ROUTE_TO_CLOCK_G_NEWTON_NOT_WEP",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG3268_0_coefficient_projection",
            "gate": "DD coefficient projection D=R C derived",
            "passed": "true",
            "reason": "3268 writes R rows and identifies common-mode null direction",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3268_1_fixed_constant_zero_route",
            "gate": "fixed local constants prove D=0",
            "passed": "false",
            "reason": "constant-sector rows are contracts/conditional routes, not current parent-signed theorems",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3268_2_finite_coefficient_values",
            "gate": "finite C_g,C_hatm,C_e values sourced",
            "passed": "false",
            "reason": "3268 gives coefficient constraints and residual basis, not numeric parent coefficient rows",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3268_3_common_mode_routed",
            "gate": "common mode sent to Newton/clock/G gates",
            "passed": "true",
            "reason": "3268 explicitly refuses to treat common mass-scale shifts as WEP constraints",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3268_4_local_GR",
            "gate": "local GR/Newton/Maxwell promotion",
            "passed": "false",
            "reason": "coefficient fork is sharper but parent action/superselection proof remains unsigned",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3268_0",
            "verdict": "LOW_ENERGY_COEFFICIENT_FORK_DERIVED_NOT_SIGNED",
            "what_moved": "WEP source coupling is now |C_hatm-C_g| and |C_e|, with common mode separated from DD bounds.",
            "best_next": "try to prove the fixed-local-constants/superselection branch for C_g,C_hatm,C_e on the local GR branch",
            "fallback_next": "instantiate numeric nonclaim rows for C_parent, s_k, epsilon_k and run bounded comparator only",
            "valid_for_claim": "false",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3268_0_3269",
            "selected": "primary",
            "target_doc": "3269-Y5-R2FR-fixed-local-constants-superselection-for-DD-zero-or-coefficient-runner-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3269_fixed_local_constants_superselection_for_DD_zero_or_coefficient_runner.py",
            "objective": "Attempt to prove local superselection/no-running for Lambda_3, hatm, and alpha_EM; if not, build executable coefficient rows for C_parent, s_k, and epsilon_k.",
            "guardrail": "Do not claim WEP/local-GR pass from fixed constants until the parent action excludes direct X/material/source vertices.",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_count() -> int:
    if not FW.exists():
        return 0
    script_mtime = Path(__file__).stat().st_mtime
    return sum(1 for path in FW.rglob("*") if path.is_file() and path.stat().st_mtime > script_mtime)


def validation_rows() -> list[dict[str, Any]]:
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = source_register()
    constraints = constraint_rows()
    finite_constraints = all(
        row["value"] == "UNBOUNDED_BY_THIS_ARENA" or math.isfinite(float(row["value"]))
        for row in constraints
    )
    common_mode_present = any(row["projection_id"] == "R3268_2_null_common_mode" for row in projection_rows())
    no_claims = all(row["claim_allowed"] == "false" for row in claim_gate_rows())
    validations = [
        {
            "check_id": "VAL3268_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": bool_str(all(row["exists"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["exists"] != "true"),
        },
        {
            "check_id": "VAL3268_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": bool_str(all(row["parse_ok"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["parse_ok"] != "true"),
        },
        {
            "check_id": "VAL3268_2_outputs_parse",
            "check": "all 3268 output CSVs parse",
            "passed": bool_str(all(csv_ok(path) for path in output_paths)),
            "detail": ";".join(str(path) for path in output_paths if not csv_ok(path)),
        },
        {
            "check_id": "VAL3268_3_projection_matrix_present",
            "check": "D=R C projection and common-mode null direction are present",
            "passed": bool_str(common_mode_present),
            "detail": "R rows for Dhatm, De, and common-mode null direction",
        },
        {
            "check_id": "VAL3268_4_constraints_finite_or_marked_unbounded",
            "check": "conditional coefficient constraints are finite or explicitly unbounded",
            "passed": bool_str(finite_constraints),
            "detail": ";".join(f"{row['constraint_id']}={row['value']}" for row in constraints),
        },
        {
            "check_id": "VAL3268_5_claim_gates_false",
            "check": "no 3268 claim gate allows WEP/local-GR promotion",
            "passed": bool_str(no_claims),
            "detail": "all claim_allowed=false",
        },
        {
            "check_id": "VAL3268_6_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3268_7_overall",
            "check": "3268 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3268_7_overall")
    validations[-1]["passed"] = bool_str(overall)
    validations[-1]["detail"] = "all required checks passed" if overall else "one or more checks failed"
    return validations


def write_doc() -> None:
    sources = source_register()
    coefficients = coefficient_vector_rows()
    projection = projection_rows()
    forks = fork_rows()
    constraints = constraint_rows()
    residual_basis = residual_basis_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()
    validations = validation_rows()
    content = f"""# 3268 - Parent low-energy coefficient vector or explicit residual basis under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- `3268` turns the parent-DD signature into the actual low-energy coefficient fork.
- The key map is `C=(C_g,C_hatm,C_e)` and `D=(D_hatm,D_e)=R C`, with `D_hatm=C_hatm-C_g` and `D_e=C_e`.
- Therefore WEP can conditionally bound `C_hatm-C_g` and `C_e`, but **not** the common mode `(C_g,C_hatm,C_e) proportional to (1,1,0)`.
- The clean local-GR route is fixed local constants: if `C_g=C_hatm=C_e=0` on the connected local branch, the dominant DD WEP source is zero before residual epsilons.
- Current MTS still needs a parent-signed constant/superselection/no-direct-vertex theorem, so this remains a derived fork, not a claim.

## Source Register
{md_table(sources, ["source_id", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"])}

## Low-Energy Coefficient Vector
{md_table(coefficients, ["coefficient_id", "symbol", "definition", "DD_role", "zero_condition", "current_status", "valid_for_claim"])}

## DD Projection Matrix
{md_table(projection, ["projection_id", "input_vector", "projection_row", "output", "WEP_constraint", "valid_for_claim"])}

## Fixed vs Variable Constant Forks
{md_table(forks, ["fork_id", "branch", "premise", "consequence", "status", "needed_to_promote", "valid_for_claim"])}

## Conditional Coefficient Constraints
{md_table(constraints, ["constraint_id", "assumptions", "coefficient_constraint", "value", "what_it_does_not_bound", "valid_for_claim"])}

## Explicit Residual Basis
{md_table(residual_basis, ["residual_id", "symbol", "role", "required_columns", "current_status", "valid_for_claim"])}

## Claim Gates
{md_table(gates, ["gate_id", "gate", "passed", "reason", "claim_allowed"])}

## Decision
{md_table(decisions, ["decision_id", "verdict", "what_moved", "best_next", "fallback_next", "valid_for_claim"])}

## Next Target
{md_table(next_targets, ["next_id", "selected", "target_doc", "target_script", "objective", "guardrail", "valid_for_claim"])}

## Validation
{md_table(validations, ["check_id", "check", "passed", "detail"])}

Generated UTC: {RUN_UTC}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    write_csv(OUTPUTS["sources"], source_register())
    write_csv(OUTPUTS["coefficient_vector"], coefficient_vector_rows())
    write_csv(OUTPUTS["projection"], projection_rows())
    write_csv(OUTPUTS["forks"], fork_rows())
    write_csv(OUTPUTS["constraints"], constraint_rows())
    write_csv(OUTPUTS["residual_basis"], residual_basis_rows())
    write_csv(OUTPUTS["gates"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_rows())
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
