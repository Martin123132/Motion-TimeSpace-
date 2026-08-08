from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4108-Y5-R2FR-ellJ-source-current-normalization-zero-or-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_ELLJ_NORMALIZATION_GATE_4108"
CHECKPOINT_ID = "4108"
DECISION = (
    "ELLJ_DECOMPOSITION_IMPORTED_PIM_HTAU_SUBDENOMINATOR_CONDITIONAL_"
    "ZERO_ROUTE_ACTIVE_QBASIC_SOURCE_COORDINATE_GATE_NEXT"
)

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4108_00_4107_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4107_NEXT_TARGET.csv",
        "4108-Y5-R2FR-ellJ-source-current-normalization-zero-or-bound.md",
        "4107 selects ell_J source-current normalization as the next coupling denominator.",
    ),
    "SRC4108_01_3601_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3601_ELLJ_NORMALIZATION_THEOREM.csv",
        "ELJ3601_1_exact_decomposition",
        "3601 derives the exact ell_J source-current owner decomposition.",
    ),
    "SRC4108_02_3601_residuals": (
        SOURCE_DIR / "P8_Y5_R2FR_3601_ELLJ_RESIDUALS.csv",
        "ELJR3601_9_R_PiM_plus_R_Htau",
        "3601 identifies R_PiM+R_Htau as the main subdenominator.",
    ),
    "SRC4108_03_3601_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_3601_ELLJ_BOUND_ROWS.csv",
        "ELJB3601_11_ellJ_total",
        "3601 gives source-ready ell_J component bound rows.",
    ),
    "SRC4108_04_3601_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3601_STATUS.csv",
        "ELLJ_SOURCE_CURRENT_NORMALIZATION_DECOMPOSED_PIM_HTAU_NEXT",
        "3601 status identifies PiM/H_tau as the algebraic heart of ell_J.",
    ),
    "SRC4108_05_3602_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3602_PIM_HTAU_SUBDENOMINATOR_THEOREM.csv",
        "PHT3602_3_quotient_zero_theorem",
        "3602 derives the source-coordinate chain-rule zero route for C_M and C_shape.",
    ),
    "SRC4108_06_3602_residuals": (
        SOURCE_DIR / "P8_Y5_R2FR_3602_PIM_HTAU_COMPONENT_RESIDUALS.csv",
        "PHTR3602_0_total",
        "3602 decomposes R_PiM+R_Htau into C_i components.",
    ),
    "SRC4108_07_3602_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_3602_PIM_HTAU_COMPONENT_BOUND_ROWS.csv",
        "PHTB3602_12_total_no_cancellation",
        "3602 gives PiM/H_tau component bound rows.",
    ),
    "SRC4108_08_3602_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3602_STATUS.csv",
        "PIM_HTAU_SUBDENOMINATOR_CONDITIONAL_ZERO_THEOREM_BOUND_BRANCH_ACTIVE",
        "3602 status selects source-coordinate q-basicity as next target.",
    ),
    "SRC4108_09_3602_next": (
        SOURCE_DIR / "P8_Y5_R2FR_3602_NEXT_TARGET.csv",
        "3603-Y5-R2FR-source-coordinate-qbasicity-or-AX-connection-bound.md",
        "3602 selects source-coordinate q-basicity / A_X connection as next target.",
    ),
    "SRC4108_10_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4108_ellJ_source_current_normalization_zero_or_bound.py",
        "Reproducible generator for this 4108 checkpoint.",
    ),
}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_string(value: bool) -> str:
    return "True" if value else "False"


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def row_base() -> dict:
    return {
        "timestamp_utc": TIMESTAMP,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
    }


def source_register_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "source_id": source_id,
            "source_type": "local_checkpoint_or_generator",
            "path_or_url": str(path),
            "needle": needle,
            "role": role,
            "exists": bool_string(path.exists()),
            "contains_needle": bool_string(path.exists() and needle in read_text(path)),
            "valid_for_claim": "False",
        }
        for source_id, (path, needle, role) in LOCAL_SOURCES.items()
    ]


def ellj_decomposition_rows() -> List[dict]:
    entries = [
        (
            "ELJ4108_0_exact_decomposition",
            "z_ellJ",
            "z_ellJ[X] = R_md + R_Ward + R_PiM + R_Htau + R_ref + R_W + R_frame + R_units",
            "ell_J is now an owner decomposition, not a free source-current scale",
            "EXACT_DECOMPOSITION_IMPORTED",
            "SRC4108_01_3601_theorem",
        ),
        (
            "ELJ4108_1_matter_descent",
            "R_md",
            "zero only if S_matter descends as Sbar[q(Phi),psi,theta] with no source-only weight or direct hidden vertex",
            "matter normalization cannot be patched after orbital GM",
            "CONDITIONAL_ZERO_ROUTE_NOT_SIGNED",
            "SRC4108_01_3601_theorem",
        ),
        (
            "ELJ4108_2_Ward_projection",
            "R_Ward",
            "zero only if on-shell Hilbert/Ward conservation implies closed projected mass flux before Pi_M/readout",
            "conservation has to survive projection, boundaries and non-Hilbert tails",
            "CONDITIONAL_ZERO_ROUTE_NOT_SIGNED",
            "SRC4108_01_3601_theorem",
        ),
        (
            "ELJ4108_3_PiM_Htau_core",
            "R_PiM+R_Htau",
            "R_PiM+R_Htau = C_M + C_shape + C_curl + C_domain + C_ref + C_frame + C_units",
            "this is the algebraic heart of z_ellJ",
            "SUBDENOMINATOR_IMPORTED",
            "SRC4108_05_3602_theorem",
        ),
        (
            "ELJ4108_4_reference_support_frame_units",
            "R_ref+R_W+R_frame+R_units",
            "H_ref, W_source, frame/tau/readout and unit conventions must be parent-selected before measured GM",
            "prevents denominator laundering",
            "BOUND_BRANCH_ACTIVE",
            "SRC4108_03_3601_bounds",
        ),
        (
            "ELJ4108_5_conditional_ellJ_zero",
            "z_ellJ=0",
            "if all ell_J owner components vanish by one parent source-current chain, ell_J is source-silent in the G_eff product",
            "clean theorem route, not activated",
            "CONDITIONAL_THEOREM_NOT_CLAIMED",
            "SRC4108_01_3601_theorem",
        ),
    ]
    return [
        {
            **row_base(),
            "row_id": row_id,
            "symbol": symbol,
            "formula_or_condition": formula,
            "meaning": meaning,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row_id, symbol, formula, meaning, status, source_key in entries
    ]


def pim_htau_rows() -> List[dict]:
    entries = [
        (
            "PHT4108_0_exact_components",
            "R_PiM_plus_R_Htau",
            "R_PiM+R_Htau = C_M+C_shape+C_curl+C_domain+C_ref+C_frame+C_units",
            "the subdenominator has seven explicit components",
            "EXACT_COMPONENT_DECOMPOSITION",
            "SRC4108_05_3602_theorem",
        ),
        (
            "PHT4108_1_source_connection",
            "A_X_source_connection",
            "Y(Phi)=(M_H_ref(Phi),sigma^a(Phi)); A_X^I := D_X Y^I",
            "mass/shape terms are source-coordinate connection terms",
            "EXACT_DEFINITION",
            "SRC4108_05_3602_theorem",
        ),
        (
            "PHT4108_2_qbasic_zero",
            "C_M+C_shape",
            "if Y=Ybar(q(Phi)) and v_X in ker(Dq), then A_X=dYbar(Dq(v_X))=0, hence C_M=C_shape=0",
            "this is the best non-plateau route: chain rule plus true verticality",
            "CONDITIONAL_ZERO_THEOREM_DERIVED",
            "SRC4108_05_3602_theorem",
        ),
        (
            "PHT4108_3_Htau_curl",
            "C_curl",
            "zero only if H_tau is integrable and the symplectic boundary term is exact, zero, or separately bounded",
            "Hamiltonian source measure must be a real charge, not a path-dependent denominator",
            "CONDITIONAL_ZERO_ROUTE_NOT_SIGNED",
            "SRC4108_05_3602_theorem",
        ),
        (
            "PHT4108_4_domain_ref_frame_units",
            "C_domain+C_ref+C_frame+C_units",
            "support/domain, H_ref, same-frame readout and denominator units must be selected before measured GM",
            "remaining nonconnection pieces stay live",
            "BOUND_BRANCH_ACTIVE",
            "SRC4108_07_3602_bounds",
        ),
        (
            "PHT4108_5_current_verdict",
            "R_PiM+R_Htau",
            "subdenominator zero is conditional; current live target is q-basic source coordinates and actual verticality",
            "do not promote ell_J, G_eff, Newton or local GR",
            "NO_CLAIM_NEXT_ROUTE_SELECTED",
            "SRC4108_08_3602_status",
        ),
    ]
    return [
        {
            **row_base(),
            "row_id": row_id,
            "symbol": symbol,
            "formula_or_condition": formula,
            "meaning": meaning,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row_id, symbol, formula, meaning, status, source_key in entries
    ]


def bound_rows() -> List[dict]:
    entries = [
        ("BND4108_0_z_ellJ", "z_ellJ", "R_md+R_Ward+R_PiM+R_Htau+R_ref+R_W+R_frame+R_units", "BOUND_REQUIRED_CRITICAL", "SRC4108_03_3601_bounds"),
        ("BND4108_1_R_md", "R_md", "matter descent/source-only multiplier residual", "BOUND_REQUIRED", "SRC4108_03_3601_bounds"),
        ("BND4108_2_R_Ward", "R_Ward", "Ward conservation to projected source-flux residual", "BOUND_REQUIRED", "SRC4108_03_3601_bounds"),
        ("BND4108_3_R_PiM_plus_R_Htau", "R_PiM_plus_R_Htau", "C_M+C_shape+C_curl+C_domain+C_ref+C_frame+C_units", "BOUND_REQUIRED_CRITICAL", "SRC4108_07_3602_bounds"),
        ("BND4108_4_C_M", "C_M", "source mass connection term from A_X^M", "BOUND_OR_QBASIC_ZERO_REQUIRED", "SRC4108_07_3602_bounds"),
        ("BND4108_5_C_shape", "C_shape", "source shape connection term from A_X^a", "BOUND_OR_QBASIC_ZERO_REQUIRED", "SRC4108_07_3602_bounds"),
        ("BND4108_6_C_curl", "C_curl", "H_tau integrability/curl residual", "BOUND_REQUIRED_CRITICAL", "SRC4108_07_3602_bounds"),
        ("BND4108_7_C_domain_ref_frame_units", "C_domain+C_ref+C_frame+C_units", "support/domain/reference/frame/unit residuals", "BOUND_REQUIRED", "SRC4108_07_3602_bounds"),
        ("BND4108_8_A_X", "A_X_source_connection", "A_X^I=D_XY^I=dYbar^I(Dq(v_X)) if q-basic", "NEXT_BOUND_OR_ZERO_TARGET", "SRC4108_07_3602_bounds"),
        ("BND4108_9_total", "epsilon_ellJ_total", "norm of active ell_J and PiM/H_tau residual components", "TOTAL_BOUND_BRANCH_ACTIVE", "SRC4108_03_3601_bounds"),
    ]
    return [
        {
            **row_base(),
            "bound_id": bound_id,
            "symbol": symbol,
            "definition": definition,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for bound_id, symbol, definition, status, source_key in entries
    ]


def promotion_gate_rows() -> List[dict]:
    entries = [
        ("PROM4108_0_ellJ_decomposition", "ell_J exact decomposition", "PASS_EXACT_IDENTITY", "z_ellJ split into source-current owner components"),
        ("PROM4108_1_ellJ_zero", "ell_J source-silent claim", "FAIL_CURRENT_CLAIM", "all owner components are not jointly parent-signed"),
        ("PROM4108_2_PiM_Htau_decomposition", "PiM/H_tau subdenominator", "PASS_EXACT_IDENTITY", "R_PiM+R_Htau split into seven C_i terms"),
        ("PROM4108_3_qbasic_route", "C_M and C_shape zero route", "PASS_CONDITIONAL_THEOREM", "q-basic Y and vertical v_X imply A_X=0, hence C_M=C_shape=0"),
        ("PROM4108_4_subdenominator_claim", "R_PiM+R_Htau zero", "FAIL_CURRENT_CLAIM", "q-basicity, verticality, H_tau curl, support/reference/frame/units remain open"),
        ("PROM4108_5_no_laundering", "no measured-GM laundering", "PASS_GUARD", "ell_J, M_H_ref, H_ref, units and source coordinates must precede orbital readout"),
        ("PROM4108_6_Newton_GR", "constant G/Newton/local-GR promotion", "FAIL_CURRENT_CLAIM", "source-current denominator remains active"),
    ]
    return [
        {
            **row_base(),
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "detail": detail,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for gate_id, gate, status, detail in entries
    ]


def decision_rows() -> List[dict]:
    entries = [
        (
            "DEC4108_0_ellJ",
            "adopt ell_J source-current owner decomposition",
            "z_ellJ is now eight source-current residuals rather than an adjustable denominator",
            "constant G_eff cannot use ell_J as a hidden calibration knob",
            "ELLJ_DECOMPOSITION_CANONICAL",
            "SRC4108_01_3601_theorem",
        ),
        (
            "DEC4108_1_PiM_Htau",
            "adopt PiM/H_tau subdenominator theorem",
            "R_PiM+R_Htau is the algebraic heart and has a chain-rule route for C_M,C_shape",
            "next derivation focuses on q-basic source coordinates and verticality",
            "PIM_HTAU_ROUTE_CANONICAL",
            "SRC4108_05_3602_theorem",
        ),
        (
            "DEC4108_2_next",
            "attack source-coordinate q-basicity next",
            "Y=(M_H_ref,sigma^a)=Ybar(q(Phi)) and Dq(v_X)=0 kills A_X by chain rule",
            "4109 targets A_X source-connection zero or bound rows",
            "NEXT_TARGET_SELECTED",
            "SRC4108_09_3602_next",
        ),
    ]
    return [
        {
            **row_base(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "valid_for_claim": "False",
        }
        for decision_id, decision, reason, consequence, status, source_key in entries
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "next_id": "NEXT4108_0",
            "target_doc": "4109-Y5-R2FR-source-coordinate-qbasicity-or-AX-connection-bound.md",
            "target_script": "scripts/Y5_R2FR_4109_source_coordinate_qbasicity_or_AX_connection_bound.py",
            "objective": "prove Y=(M_H_ref,sigma^a) is q-basic and v_X is vertical so A_X=0; if not, retain A_X^M, A_X^a, partial_M A_X^M and partial_M A_X^a as source-connection bound inputs",
            "success_gate": "C_M and C_shape can be removed only by parent-owned source-coordinate descent and actual verticality, not by calibrating source mass/shape from measured orbital GM",
            "reason": "4108 shows the source-coordinate connection is the best route to killing two critical PiM/H_tau components before numeric scoring",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "status_id": "STATUS4108_0",
            "decision": DECISION,
            "strongest_result": "4108 imports the ell_J decomposition and the PiM/H_tau subdenominator theorem into the current chain. ell_J is no longer a loose normalization: z_ellJ=R_md+R_Ward+R_PiM+R_Htau+R_ref+R_W+R_frame+R_units, with R_PiM+R_Htau=C_M+C_shape+C_curl+C_domain+C_ref+C_frame+C_units. The best zero mechanism is q-basic source coordinates plus vertical residual direction, which gives A_X=0 and kills C_M,C_shape by chain rule.",
            "what_moved_forward": "the source-current normalization problem is reduced to the concrete A_X source-connection/q-basicity gate plus H_tau/domain/reference/frame/unit residuals",
            "still_missing": "matter descent, Ward-to-projected-flux closure, q-basic Y=(M_H_ref,sigma^a), actual Dq(v_X)=0 verticality, H_tau curl zero, support/domain descent, source-blind H_ref, same-frame readout, denominator unit lock",
            "public_status": "no ellJ_constant_Geff_Newton_local_GR_PPN claim",
            "next_target": "4109 source-coordinate q-basicity or AX connection bound",
            "valid_for_claim": "False",
        }
    ]


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4108_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4108_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4108_ELLJ_DECOMPOSITION": SOURCE_DIR / "P8_Y5_R2FR_4108_ELLJ_DECOMPOSITION.csv",
        "P8_Y5_R2FR_4108_PIM_HTAU_SUBDENOMINATOR": SOURCE_DIR / "P8_Y5_R2FR_4108_PIM_HTAU_SUBDENOMINATOR.csv",
        "P8_Y5_R2FR_4108_BOUND_INPUTS": SOURCE_DIR / "P8_Y5_R2FR_4108_BOUND_INPUTS.csv",
        "P8_Y5_R2FR_4108_PROMOTION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4108_PROMOTION_GATES.csv",
        "P8_Y5_R2FR_4108_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4108_DECISION_GATE.csv",
        "P8_Y5_R2FR_4108_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4108_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4108_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4108_STATUS.csv",
    }


def write_doc() -> None:
    lines = [
        "# 4108 - ellJ source-current normalization zero or bound",
        "",
        "## Verdict",
        "4108 makes `ell_J` a real source-current theorem gate instead of a hidden normalization denominator.",
        "",
        "`z_ellJ = R_md + R_Ward + R_PiM + R_Htau + R_ref + R_W + R_frame + R_units`.",
        "",
        "The core is now sharper again:",
        "",
        "`R_PiM + R_Htau = C_M + C_shape + C_curl + C_domain + C_ref + C_frame + C_units`.",
        "",
        "The best non-cheat route is the chain-rule mechanism: if `Y=(M_H_ref,sigma^a)` descends through the parent quotient and the residual direction is truly vertical, then `A_X=dYbar(Dq(v_X))=0`, so `C_M=C_shape=0` before any measured-GM calibration.",
        "",
        f"Decision: `{DECISION}`",
        "",
        "## Concrete Advances",
        "- `ell_J` is decomposed into named source-current owner residuals.",
        "- `R_PiM+R_Htau` is identified as the algebraic heart of the denominator.",
        "- `C_M` and `C_shape` get a real derivation route through q-basicity and verticality.",
        "- Measured-orbital `GM` is explicitly forbidden as the definition of `ell_J`, `M_H_ref`, `H_ref`, source units, or source shape.",
        "",
        "## Still Not Claimed",
        "- `ell_J` source silence.",
        "- Constant measured `G_eff`.",
        "- Newton/local-GR/PPN promotion.",
        "",
        "## Outputs",
        "- `P8_Y5_R2FR_4108_SOURCE_REGISTER.csv`",
        "- `P8_Y5_R2FR_4108_ELLJ_DECOMPOSITION.csv`",
        "- `P8_Y5_R2FR_4108_PIM_HTAU_SUBDENOMINATOR.csv`",
        "- `P8_Y5_R2FR_4108_BOUND_INPUTS.csv`",
        "- `P8_Y5_R2FR_4108_PROMOTION_GATES.csv`",
        "- `P8_Y5_R2FR_4108_DECISION_GATE.csv`",
        "- `P8_Y5_R2FR_4108_NEXT_TARGET.csv`",
        "- `P8_Y5_R2FR_4108_STATUS.csv`",
        "- `P8_Y5_BRR545_4108_VALIDATION.csv`",
        "",
        "## Next target",
        "- `4109-Y5-R2FR-source-coordinate-qbasicity-or-AX-connection-bound.md`",
        "- Objective: prove `Y=(M_H_ref,sigma^a)` is q-basic and `Dq(v_X)=0`, or retain `A_X` source-connection bound rows.",
    ]
    DOC_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4108_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4108_ELLJ_DECOMPOSITION"], ellj_decomposition_rows())
    write_csv(outputs["P8_Y5_R2FR_4108_PIM_HTAU_SUBDENOMINATOR"], pim_htau_rows())
    write_csv(outputs["P8_Y5_R2FR_4108_BOUND_INPUTS"], bound_rows())
    write_csv(outputs["P8_Y5_R2FR_4108_PROMOTION_GATES"], promotion_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4108_DECISION_GATE"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4108_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4108_STATUS"], status_rows())
    write_doc()
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                **row_base(),
                "check_id": check_id,
                "check": check,
                "passed": bool_string(passed),
                "detail": detail,
                "valid_for_claim": "False",
            }
        )

    source_rows = source_register_rows()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "True"]
    missing_needles = [row["source_id"] for row in source_rows if row["contains_needle"] != "True"]
    add("VAL4108_0_sources_exist", "every local source path exists", not missing_sources, ";".join(missing_sources) or "all sources exist")
    add("VAL4108_1_sources_contain_needles", "every local source contains its expected needle", not missing_needles, ";".join(missing_needles) or "all needles found")

    parse_counts = {}
    parse_ok = True
    for name, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[name] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_counts[name] = f"ERROR:{exc}"
            parse_ok = False
    add("VAL4108_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    ellj_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4108_ELLJ_DECOMPOSITION"]))
    ellj_tokens = ["z_ellJ", "R_md", "R_Ward", "R_PiM+R_Htau", "R_ref", "R_W", "R_frame", "R_units"]
    missing_ellj = [token for token in ellj_tokens if token not in ellj_text]
    add("VAL4108_3_ellj_decomposition", "ellJ decomposition includes all owner components", not missing_ellj, ";".join(missing_ellj) or "ellJ tokens present")

    pht_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4108_PIM_HTAU_SUBDENOMINATOR"]))
    pht_tokens = ["C_M", "C_shape", "C_curl", "C_domain", "C_ref", "C_frame", "C_units", "A_X", "Dq(v_X)"]
    missing_pht = [token for token in pht_tokens if token not in pht_text]
    add("VAL4108_4_pim_htau", "PiM/Htau theorem includes seven components and qbasic route", not missing_pht, ";".join(missing_pht) or "PiM/Htau tokens present")

    bound_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4108_BOUND_INPUTS"]))
    bound_tokens = ["z_ellJ", "R_PiM_plus_R_Htau", "C_M", "C_shape", "A_X_source_connection", "epsilon_ellJ_total"]
    missing_bound = [token for token in bound_tokens if token not in bound_text]
    add("VAL4108_5_bounds", "bound rows include ellJ, PiM/Htau, A_X and total rows", not missing_bound, ";".join(missing_bound) or "bound tokens present")

    gates = parse_csv(outputs["P8_Y5_R2FR_4108_PROMOTION_GATES"])
    no_claim = all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for row in gates)
    fail_claims = any(row.get("status") == "FAIL_CURRENT_CLAIM" and "ell_J" in row.get("gate", "") for row in gates)
    qbasic_route = any(row.get("status") == "PASS_CONDITIONAL_THEOREM" and "C_M" in row.get("detail", "") for row in gates)
    add("VAL4108_6_gates", "promotion gates block claims and retain qbasic route", no_claim and fail_claims and qbasic_route, f"no_claim={no_claim}; fail_claims={fail_claims}; qbasic={qbasic_route}")

    decisions = parse_csv(outputs["P8_Y5_R2FR_4108_DECISION_GATE"])
    next_decision = any(row.get("status") == "NEXT_TARGET_SELECTED" and "q-basicity" in row.get("decision", "") for row in decisions)
    add("VAL4108_7_decisions", "decision gate selects source-coordinate q-basicity", next_decision, str(decisions))

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4108_NEXT_TARGET"])
    next_ok = any("4109-Y5-R2FR-source-coordinate-qbasicity-or-AX-connection-bound.md" in row.get("target_doc", "") for row in next_rows)
    add("VAL4108_8_next_target", "next target is source-coordinate qbasicity/A_X", next_ok, str(next_rows))

    status_rows_local = parse_csv(outputs["P8_Y5_R2FR_4108_STATUS"])
    status_text = " ".join(" ".join(row.values()) for row in status_rows_local)
    status_ok = DECISION in status_text and "no ellJ_constant_Geff_Newton_local_GR_PPN claim" in status_text
    add("VAL4108_9_status", "status records decision and no-claim state", status_ok, "status row checked")

    output_paths = list(outputs.values()) + [DOC_PATH, SCRIPT_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4108*")) or any(
            FORMALIZATION.rglob("4108-Y5-R2FR*")
        )
    add("VAL4108_10_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4108_11_compile", "generator script compiles", compile_ok, compile_detail)

    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4108_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
