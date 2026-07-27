from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3322-Y5-R2FR-Ci-projection-and-composite-contact-tail-gate-for-epsilon-grad-under-AX1090.md"

SRC_ACTION = REPO / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"
SRC_GRAVITY = REPO / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity.md"
SRC_COMPACT = REPO / "core-mts-framework" / "gravity" / "gravity-as-emergent-mass-geometry-scaling-in-motion-timespace.md"

SOURCES = [
    {
        "source_id": "SRC3322_0_3319_doc",
        "path": ROOT / "3319-Y5-R2FR-psi-coarse-graining-no-finite-public-residue-or-Bi-bound-under-AX1090.md",
        "role": "linear public-readout split and composite-tail caveat",
    },
    {
        "source_id": "SRC3322_1_3320_doc",
        "path": ROOT / "3320-Y5-R2FR-local-first-gradient-silence-or-gradient-envelope-under-AX1090.md",
        "role": "epsilon_grad exact condition and norm-bound fallback",
    },
    {
        "source_id": "SRC3322_2_3321_doc",
        "path": ROOT / "3321-Y5-R2FR-smoothing-kernel-scale-separation-bound-for-epsilon-grad-under-AX1090.md",
        "role": "Gaussian smoothing transfer and threshold handoff",
    },
    {
        "source_id": "SRC3322_3_3321_thresholds",
        "path": OUT / "P8_Y5_R2FR_3321_EPSILON_GRAD_THRESHOLD_ROWS.csv",
        "role": "arena threshold formulas needing C_i and epsilon_composite",
    },
    {
        "source_id": "SRC3322_4_action_metric",
        "path": SRC_ACTION,
        "role": "emergent metric from smoothed psi-gradient covariance and matter/EH action",
    },
    {
        "source_id": "SRC3322_5_gravity_ppn",
        "path": SRC_GRAVITY,
        "role": "solar weak-field PPN margin language",
    },
    {
        "source_id": "SRC3322_6_compact_newton",
        "path": SRC_COMPACT,
        "role": "compact-system Newtonian recovery language",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3322_SOURCE_REGISTER.csv",
    "operator": OUT / "P8_Y5_R2FR_3322_OPERATOR_BOUND.csv",
    "ci_gate": OUT / "P8_Y5_R2FR_3322_CI_RESPONSE_GATE.csv",
    "composite": OUT / "P8_Y5_R2FR_3322_COMPOSITE_TAIL_GATE.csv",
    "threshold": OUT / "P8_Y5_R2FR_3322_ARENA_THRESHOLD_FORMULAS.csv",
    "gates": OUT / "P8_Y5_R2FR_3322_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3322_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3322_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3322_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1200) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: compact(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def sha256_prefix(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()[:16]


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    result: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            try:
                stat = item.stat()
            except OSError:
                continue
            result[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return result


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        source_path = source["path"]
        rows.append(
            {
                "source_id": source["source_id"],
                "path": str(source_path),
                "exists": bool_str(source_path.exists()),
                "parse_ok": bool_str(parse_ok(source_path)),
                "sha256_prefix": sha256_prefix(source_path),
                "role": source["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def operator_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "OP3322_0_public_readout_split",
            "object": "g_pub[psi_bar+pi]",
            "derived_statement": "g_pub = eta + S[grad psi_bar grad psi_bar] + 2 S[grad psi_bar sym grad pi] + S[grad pi grad pi]",
            "math_status": "IMPORTED_FROM_3319_AND_REWRITTEN_AS_LINEAR_PLUS_COMPOSITE",
            "claim_impact": "single-pi finite local residue can only come from the linear term unless a tadpole/mixing converts the composite term into a one-particle pole",
            "valid_for_claim": "false",
        },
        {
            "row_id": "OP3322_1_linear_vertex",
            "object": "V_i(lambda)",
            "derived_statement": "V_i(lambda)=Pi_i W_i S_ell[grad psi_bar sym grad(.)] restricted to the arena band k~1/lambda",
            "math_status": "DEFINITION_FROM_PUBLIC_READOUT_AND_ARENA_PROJECTION",
            "claim_impact": "the dangerous local coupling is not a free scalar; it is the projected linear vertex of the smoothed metric readout",
            "valid_for_claim": "false",
        },
        {
            "row_id": "OP3322_2_cauchy_schwarz_gate",
            "object": "B_i_tree",
            "derived_statement": "|B_i_tree(lambda)| <= ||Pi_i W_i||^2 ||D H_pi(lambda) D^dagger|| epsilon_grad(lambda)^2",
            "math_status": "DERIVED_OPERATOR_NORM_BOUND",
            "claim_impact": "this proves the quadratic epsilon_grad dependence once Pi_i, W_i, and H_pi are bounded operators",
            "valid_for_claim": "false",
        },
        {
            "row_id": "OP3322_3_Ci_definition",
            "object": "C_i(lambda,S,H_pi)",
            "derived_statement": "C_i(lambda,S,H_pi)=||Pi_i W_i||^2 ||D S_ell H_pi(lambda) S_ell^dagger D^dagger|| times source-normalization factors",
            "math_status": "DERIVED_RESPONSE_COEFFICIENT_DEFINITION",
            "claim_impact": "C_i is now a calculable projection/propagator/source-normalization object, not an unnamed fudge factor",
            "valid_for_claim": "false",
        },
        {
            "row_id": "OP3322_4_total_residual_bound",
            "object": "R_i^MTS",
            "derived_statement": "|R_i^MTS(lambda)| <= C_i(lambda) [epsilon_bg T_grad(lambda)+epsilon_boundary+epsilon_kernel_aniso]^2 + epsilon_composite_i(lambda)",
            "math_status": "DERIVED_NO_CANCELLATION_ENVELOPE",
            "claim_impact": "local tests can be scored by upper bounds; no favourable cancellation is allowed",
            "valid_for_claim": "false",
        },
    ]


def ci_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CI3322_0_projection_norm",
            "quantity": "||Pi_i W_i||",
            "needed_for": "PPN/R10/WEP/clock arena response",
            "current_state": "SYMBOLIC_BOUNDED_OPERATOR",
            "pass_condition": "define arena projection and source window, then prove finite norm or source a numeric upper bound",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CI3322_1_propagator_norm",
            "quantity": "||D S_ell H_pi S_ell^dagger D^dagger||",
            "needed_for": "range-dependent response coefficient",
            "current_state": "FORMULA_DERIVED_NUMERIC_VALUE_MISSING",
            "pass_condition": "parent action supplies Z_pi and M_pi^2, or a conservative band-limited propagator envelope",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CI3322_2_source_normalization",
            "quantity": "source-normalization factors",
            "needed_for": "Newton constant / matter coupling calibration",
            "current_state": "NOT_PARENT_OWNED_YET",
            "pass_condition": "derive kappa=8 pi G/c^4 or match the Poisson/Newtonian limit from psi covariance without re-inserting it silently",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CI3322_3_Ci_numeric",
            "quantity": "C_i(lambda)",
            "needed_for": "claim-ready local bound comparison",
            "current_state": "BLOCKED_BY_CI3322_0_TO_CI3322_2",
            "pass_condition": "every factor in C_i has a parent source path, unit convention, and numeric or conservative upper bound",
            "valid_for_claim": "false",
        },
    ]


def composite_tail_rows() -> list[dict[str, Any]]:
    return [
        {
            "tail_id": "TAIL3322_0_no_tadpole",
            "tail": "epsilon_tad_i",
            "origin": "linearization of S[grad pi grad pi] around a non-stationary or mis-normalized local vacuum",
            "zero_condition": "parent vacuum is stationary and the one-point pi tadpole vanishes in the local branch",
            "current_state": "NOT_PARENT_SIGNED",
            "claim_effect": "if not zero, it can regenerate a single-pi pole and destroy the local branch",
            "valid_for_claim": "false",
        },
        {
            "tail_id": "TAIL3322_1_two_particle",
            "tail": "epsilon_loop_i",
            "origin": "two-pi exchange / loop / composite spectral branch from S[grad pi grad pi]",
            "zero_condition": "not generally zero; becomes short-range if H_pi has a mass gap or if arena projection removes the branch",
            "current_state": "MASS_GAP_OR_PROJECTION_MISSING",
            "claim_effect": "must be bounded separately from the tree epsilon_grad^2 term",
            "valid_for_claim": "false",
        },
        {
            "tail_id": "TAIL3322_2_contact",
            "tail": "epsilon_contact_i",
            "origin": "coincident or finite-size source contact term from the quadratic public readout",
            "zero_condition": "vanishes outside source support or is absorbed into calibrated local counterterms with no finite fifth-force residue",
            "current_state": "SOURCE_SIZE_COUNTERTERM_RULE_MISSING",
            "claim_effect": "R10/lab bounds need this term isolated because contact leakage can mimic a short-range force",
            "valid_for_claim": "false",
        },
        {
            "tail_id": "TAIL3322_3_boundary",
            "tail": "epsilon_boundary_i",
            "origin": "finite kernel support, integration by parts, or local patch boundary leakage",
            "zero_condition": "compact support or falloff kills boundary functional for the tested arena",
            "current_state": "BOUNDARY_RULE_PARTIAL",
            "claim_effect": "kept inside epsilon_eff until the parent local patch construction signs it away",
            "valid_for_claim": "false",
        },
        {
            "tail_id": "TAIL3322_4_kernel_anisotropy",
            "tail": "epsilon_kernel_aniso_i",
            "origin": "non-isotropic smoothing kernel or material/source anisotropy",
            "zero_condition": "isotropic kernel and isotropic first moment in the local vacuum",
            "current_state": "NOT_NUMERICALLY_BOUNDED",
            "claim_effect": "needed for WEP and clock/EM sectors where material orientation can matter",
            "valid_for_claim": "false",
        },
    ]


def arena_threshold_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena": "PPN_local_GR",
            "residual_bound": "|gamma-1|,|beta-1|,|alpha_PF| <= C_PPN epsilon_eff^2 + epsilon_composite_PPN",
            "epsilon_eff": "epsilon_bg T_grad(lambda_solar)+epsilon_boundary+epsilon_kernel_aniso",
            "claim_gate": "requires C_PPN numeric/source bound and epsilon_composite_PPN below PPN residual limits",
            "valid_for_claim": "false",
        },
        {
            "arena": "R10_short_range",
            "residual_bound": "|alpha_psi(lambda)| <= C_R10(lambda) epsilon_eff(lambda)^2 + epsilon_composite_R10(lambda)",
            "epsilon_eff": "epsilon_bg T_grad(lambda)+epsilon_boundary+epsilon_kernel_aniso",
            "claim_gate": "requires source-backed alpha_bound(lambda), C_R10(lambda), and noncontact finite-range tail split",
            "valid_for_claim": "false",
        },
        {
            "arena": "WEP",
            "residual_bound": "eta_AB <= C_WEP epsilon_eff^2 |Delta q_AB| + epsilon_composite_WEP",
            "epsilon_eff": "composition-weighted local gradient leak",
            "claim_gate": "requires material response Delta q_AB and anisotropic/composite tail bound",
            "valid_for_claim": "false",
        },
        {
            "arena": "clocks_EM_Poynting",
            "residual_bound": "|delta nu/nu| or EM stress residual <= C_clock epsilon_eff^2 + epsilon_EM_Poynting_tail",
            "epsilon_eff": "clock/field projection of the same public metric readout",
            "claim_gate": "requires Maxwell stress/Poynting source projection and clock observable normalization",
            "valid_for_claim": "false",
        },
        {
            "arena": "orbital_Newton",
            "residual_bound": "|delta a/a_Newton| <= C_orb epsilon_eff^2 + epsilon_composite_orb",
            "epsilon_eff": "compact-system local branch leak",
            "claim_gate": "requires Poisson/Newton normalization and compact-source C_orb bound",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3322_0_operator_bound",
            "claim": "C_i epsilon_grad^2 tree-residue bound is derived",
            "passed": "true",
            "reason": "Cauchy/operator-norm bound follows from the linear public readout vertex and bounded arena projection/propagator",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3322_1_Ci_numeric",
            "claim": "C_i is numerically/source bounded for local arenas",
            "passed": "false",
            "reason": "projection norm, propagator normalization, and matter/Newton source normalization are not yet parent-owned",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3322_2_composite_zero",
            "claim": "epsilon_composite_i is zero or bounded below local-test limits",
            "passed": "false",
            "reason": "no-tadpole, mass-gap/projection, contact/counterterm, and boundary clauses remain unsigned",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3322_3_local_GR_pass",
            "claim": "local GR/Newton/PPN branch passes",
            "passed": "false",
            "reason": "the bound form is now sharper, but C_i and epsilon_composite are not claim-grade",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3322_0",
            "question": "Did 3322 move beyond saying C_i is missing?",
            "answer": "yes",
            "reason": "C_i has been decomposed into arena projection, smoothing/propagator norm, and source-normalization factors with an operator-norm proof of the epsilon_grad^2 bound",
            "next_action": "derive or source the three C_i factors rather than treating C_i as a fog coefficient",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3322_1",
            "question": "What is the main danger left?",
            "answer": "the composite tail",
            "reason": "S[grad pi grad pi] is harmless for single-pi tree exchange only if no tadpole/mixing appears and its two-particle/contact branch is short-range or bounded",
            "next_action": "prove no-tadpole/mass-gap/contact silence or keep epsilon_composite as explicit nuisance",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3322_2",
            "question": "Where does the coupling problem now sit?",
            "answer": "inside source normalization",
            "reason": "GR itself inserts G through kappa; MTS can only claim a deeper route if the psi covariance normalization matches the Poisson/Newton limit without smuggling kappa back in",
            "next_action": "attack source normalization/Newton constant matching next",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3323-Y5-R2FR-parent-source-normalization-and-composite-no-tadpole-gate-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3323_parent_source_normalization_and_composite_no_tadpole_gate.py",
            "objective": "derive the parent conditions that fix source normalization/Newton coupling and remove the composite one-particle tail, or force both into explicit nuisance bounds",
            "must_include": "Poisson limit; kappa/G normalization; no-tadpole condition; two-pi mass-gap/projection condition; contact/counterterm rule; EM/Poynting stress projection note",
            "fallback_if_failed": "local branch remains a bounded closure with explicit C_i and epsilon_composite nuisance parameters",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    operator = operator_bound_rows()
    ci_rows = ci_gate_rows()
    composite = composite_tail_rows()
    thresholds = arena_threshold_rows()
    gates = promotion_gate_rows()
    output_paths = [output_path for output_key, output_path in OUTPUTS.items() if output_key != "validation"]
    fw_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3322_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all(source["exists"] == "true" for source in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3322_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": all(source["parse_ok"] == "true" for source in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3322_2_outputs_parse",
            "check": "all 3322 non-validation outputs parse",
            "passed": all(output_path.exists() and parse_ok(output_path) for output_path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3322_3_operator_bound",
            "check": "operator bound contains C_i and epsilon_grad squared",
            "passed": any("C_i" in row["object"] or "C_i" in row["derived_statement"] for row in operator)
            and any("epsilon_grad(lambda)^2" in row["derived_statement"] or "epsilon_eff^2" in row["derived_statement"] for row in operator),
            "detail": "",
        },
        {
            "check_id": "VAL3322_4_Ci_factors",
            "check": "C_i gate includes projection, propagator, and source normalization",
            "passed": {"||Pi_i W_i||", "||D S_ell H_pi S_ell^dagger D^dagger||", "source-normalization factors"}.issubset(
                {row["quantity"] for row in ci_rows}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3322_5_composite_tails",
            "check": "composite gate includes tadpole, loop, contact, boundary, and anisotropy tails",
            "passed": {"epsilon_tad_i", "epsilon_loop_i", "epsilon_contact_i", "epsilon_boundary_i", "epsilon_kernel_aniso_i"}.issubset(
                {row["tail"] for row in composite}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3322_6_arena_thresholds",
            "check": "arena threshold formulas include PPN, R10, WEP, clocks/EM, and orbital/Newton",
            "passed": {"PPN_local_GR", "R10_short_range", "WEP", "clocks_EM_Poynting", "orbital_Newton"}.issubset(
                {row["arena"] for row in thresholds}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3322_7_no_full_claim",
            "check": "C_i numeric, composite zero, and local-GR gates remain false",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3322_1_Ci_numeric", "GATE3322_2_composite_zero", "GATE3322_3_local_GR_pass"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3322_8_next_source_normalization",
            "check": "next target attacks source normalization and no-tadpole gate",
            "passed": any("source normalization" in row["objective"] and "no-tadpole" in row["must_include"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3322_9_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3322_10_overall",
            "check": "3322 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def render_doc() -> str:
    lines: list[str] = [
        "# 3322 - C_i projection and composite/contact-tail gate for epsilon_grad under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "3322 turns the previous `C_i` placeholder into an actual operator contract.",
        "",
        "Start from the public metric readout",
        "",
        "`g_pub[psi] = eta + S[grad psi grad psi]`.",
        "",
        "For `psi = psi_bar + pi`, the split is",
        "",
        "`delta g_pub = 2 S[grad psi_bar sym grad pi] + S[grad pi grad pi]`.",
        "",
        "The first term gives the tree-level single-`pi` local residue. For an arena projection/window `Pi_i W_i` and band-limited propagator `H_pi(lambda)`, Cauchy-Schwarz gives",
        "",
        "`|B_i_tree(lambda)| <= ||Pi_i W_i||^2 ||D S_ell H_pi(lambda) S_ell^dagger D^dagger|| epsilon_grad(lambda)^2`.",
        "",
        "So",
        "",
        "`C_i(lambda,S,H_pi)=||Pi_i W_i||^2 ||D S_ell H_pi(lambda) S_ell^dagger D^dagger|| x source_normalization_i`.",
        "",
        "This is real progress: the local branch no longer has a nameless coupling fog. The remaining coupling problem is sharply isolated into projection norm, propagator normalization, and source/Newton normalization.",
        "",
        "The second term, `S[grad pi grad pi]`, is the dangerous composite tail. It does not create a single-`pi` tree pole if the parent vacuum has no tadpole/mixing, but it can still create two-particle, contact, boundary, or anisotropic residuals. Therefore the safe no-cancellation bound is",
        "",
        "`|R_i^MTS(lambda)| <= C_i(lambda) [epsilon_bg T_grad(lambda)+epsilon_boundary+epsilon_kernel_aniso]^2 + epsilon_composite_i(lambda)`.",
        "",
        "No local-GR/R10/WEP/clock/orbital claim follows yet. The branch has improved from unknown to bounded-contract form.",
        "",
        "## Source Register",
        "",
    ]
    for row in source_register_rows():
        lines.append(
            f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} parse_ok={row['parse_ok']} role={row['role']}"
        )
    sections = [
        ("Operator Bound", operator_bound_rows(), "row_id"),
        ("C_i Response Gate", ci_gate_rows(), "gate_id"),
        ("Composite Tail Gate", composite_tail_rows(), "tail_id"),
        ("Arena Threshold Formulas", arena_threshold_rows(), "arena"),
        ("Promotion Gates", promotion_gate_rows(), "gate_id"),
        ("Decision Ledger", decision_rows(), "decision_id"),
        ("Next Target", next_target_rows(), "target_doc"),
    ]
    for title, rows, key_name in sections:
        lines.extend(["", f"## {title}", ""])
        for row in rows:
            label = row.get(key_name, "")
            body = "; ".join(f"{key}={value}" for key, value in row.items() if key != key_name)
            lines.append(f"- `{label}`: {body}")
    lines.extend(
        [
            "",
            "## Test Notes",
            "",
            "- This checkpoint is private and nonclaim.",
            "- Every output row keeps `valid_for_claim=false`.",
            "- The formalization workbench is not modified.",
            "- `C_i` is now a calculable contract, but not yet a sourced number.",
            "- `epsilon_composite_i` remains the main local-GR risk until no-tadpole/contact/mass-gap clauses are parent-signed.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["operator"], operator_bound_rows())
    write_csv(OUTPUTS["ci_gate"], ci_gate_rows())
    write_csv(OUTPUTS["composite"], composite_tail_rows())
    write_csv(OUTPUTS["threshold"], arena_threshold_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
