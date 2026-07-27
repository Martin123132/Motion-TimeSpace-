from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4129-Y5-R2FR-observed-hodge-current-owner-clause.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_OBSERVED_HODGE_CURRENT_OWNER_CLAUSE_4129"
CHECKPOINT_ID = "4129"
DECISION = "STANDARD_VISIBLE_EM_BASELINE_LOCKED_PARENT_OWNER_UNSIGNED_DEVIATION_BOUNDS_FILLED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4129_00_4128_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4128_NEXT_TARGET.csv",
        "4129-Y5-R2FR-observed-hodge-current-owner-clause.md",
        "4128 selected observed Hodge/current owner clause.",
    ),
    "SRC4129_01_4128_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4128_STATUS.csv",
        "STATIONARY_LOCAL_PHI_EM_RAD_ZERO_DERIVED_RADIATIVE_BOUND_RETAINED",
        "Current-chain stationary Poynting flux zero.",
    ),
    "SRC4129_02_4128_local_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4128_LOCAL_COUPLING_STATUS.csv",
        "REMAINING_EM_COUPLING_TERMS_EXPLICIT",
        "Remaining EM/source owner blockers after Poynting reductions.",
    ),
    "SRC4129_03_4082_hodge": (
        SOURCE_DIR / "P8_Y5_R2FR_4082_EM_HODGE_MAXWELL_THEOREM.csv",
        "EXACT_CONDITIONAL_SAME_HODGE_MAXWELL_THEOREM",
        "Same-Hodge Maxwell theorem and conformal guard.",
    ),
    "SRC4129_04_4083_charge": (
        SOURCE_DIR / "P8_Y5_R2FR_4083_CHARGE_CURRENT_NORMALIZATION_THEOREM.csv",
        "STANDARD_VISIBLE_EM_IMPORT_CONTRACT_READY_NONCLAIM",
        "Charge/current theorem plus standard visible EM import contract.",
    ),
    "SRC4129_05_4014_owner": (
        SOURCE_DIR / "P8_Y5_R2FR_4014_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv",
        "OHN4014_6_full_EM_owner_branch",
        "Observed Hodge/Maxwell owner theorem package.",
    ),
    "SRC4129_06_4014_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_4014_EM_OWNER_AUDIT.csv",
        "EOA4014_6_absolute_alpha_guard",
        "EM owner audit and alpha overclaim guard.",
    ),
    "SRC4129_07_4014_finite": (
        SOURCE_DIR / "P8_Y5_R2FR_4014_HODGE_F2_CURRENT_FINITE_ROWS.csv",
        "EMOWN4014_0_master",
        "Finite owner vector for Hodge/F2/current residuals.",
    ),
    "SRC4129_08_3862_hodge_zero": (
        SOURCE_DIR / "P8_Y5_R2FR_3862_EM_HODGE_ZERO_THEOREM.csv",
        "EXACT_CONDITIONAL_DELTA_HODGE_ZERO_THEOREM",
        "Observed Hodge zero theorem and coupling handoff.",
    ),
    "SRC4129_09_3863_norm": (
        SOURCE_DIR / "P8_Y5_R2FR_3863_MAXWELL_NORMALIZATION_OWNER_THEOREM.csv",
        "EXACT_CONDITIONAL_EM_SOURCE_SCALE_ZERO_THEOREM",
        "Maxwell normalization owner theorem.",
    ),
    "SRC4129_10_3875_current": (
        SOURCE_DIR / "P8_Y5_R2FR_3875_CJQ_CURRENT_OWNER_ZERO_THEOREM.csv",
        "DERIVED_FIXED_SECTOR_ZERO",
        "Current owner theorem with fixed representation subzero.",
    ),
    "SRC4129_11_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4129_observed_hodge_current_owner_clause.py",
        "Reproducible generator for this 4129 checkpoint.",
    ),
}


def row_base() -> dict:
    return {"timestamp_utc": TIMESTAMP, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        row = row_base()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(contains(path, needle)),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def branch_contract_rows() -> List[dict]:
    data = [
        (
            "BRC4129_0_standard_visible_em_import",
            "standard_visible_EM_baseline",
            "Use the usual local Maxwell/charged-matter action on g_obs/e_obs with calibrated constants e, hbar, c, mu0/epsilon0 or alpha.",
            "Delta_Hodge_EM=0, beta_ZQ=0, beta_JQ=0, and C_XF2=0 by baseline matter-sector definition, not by new MTS prediction.",
            "This is sufficient for local GR reduction baseline because GR also couples to a supplied matter action rather than deriving alpha.",
            "BASELINE_IMPORT_CONTRACT_LOCKED_NONCLAIM",
        ),
        (
            "BRC4129_1_parent_owner_prediction",
            "parent_owned_EM_prediction",
            "Derive A_Q,F_Q,J_Q,*obs,Z_Q and representation labels from the MTS parent action/q-map with no extra F2/current/readout slots.",
            "Would make beta_Hodge_EM=beta_ZQ=beta_JQ=0 as an MTS theorem.",
            "Current corpus has conditional routes but does not parent-sign the whole owner package.",
            "PARENT_OWNER_UNSIGNED",
        ),
        (
            "BRC4129_2_deviation_branch",
            "deviation_bound_branch",
            "Retain every departure from standard visible EM as an explicit residual coefficient with units, observable links, and bound requirements.",
            "No deviation may hide inside source normalization or fitted GM.",
            "This is the empirical discipline branch for MTS-specific EM effects.",
            "DEVIATION_BOUNDS_REQUIRED",
        ),
    ]
    rows: List[dict] = []
    for branch_id, branch, definition, zero_effect, meaning, status in data:
        row = row_base()
        row.update(
            {
                "branch_id_local": branch_id,
                "branch": branch,
                "definition": definition,
                "zero_effect": zero_effect,
                "meaning": meaning,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def owner_clause_rows() -> List[dict]:
    data = [
        (
            "OCL4129_0_beta_Hodge_EM",
            "beta_Hodge_EM",
            "A_N ln *_EM or A_N chi_EM relative to *_obs[e_obs(q)]",
            "zero in standard visible EM baseline; theorem-zero if parent action-domain exhaustion signs Args(S_EM)={A_Q,F_Q,e_obs(q),orientation,fixed constants}",
            "not parent-signed as MTS prediction",
            "CONDITIONAL_ZERO_BASELINE_LOCKED",
        ),
        (
            "OCL4129_1_beta_ZQ",
            "beta_ZQ",
            "A_N ln Z_Q, Maxwell kinetic/action normalization drift",
            "zero in standard visible EM baseline; theorem-zero if parent curvature norm fixes C_P N_Q and no extra F2/readout slots exist",
            "not parent-signed as MTS prediction; absolute alpha not derived",
            "CONDITIONAL_ZERO_BASELINE_LOCKED",
        ),
        (
            "OCL4129_2_beta_JQ",
            "beta_JQ",
            "A_N ln J_Q or charge/current normalization drift",
            "zero in standard visible EM baseline; theorem-zero if same parent current owner fixes A_Q,J_Q,q_star, representation labels, and readout stability",
            "fixed representation labels give a useful subzero, but full current normalization remains unsigned",
            "PARTIAL_SUBZERO_BASELINE_LOCKED",
        ),
        (
            "OCL4129_3_beta_alpha_invariant",
            "b_alpha",
            "b_alpha=2 z_g - s_XF2, invariant under A_Q rescaling",
            "baseline imports constant alpha; parent prediction requires no-extra-F2 plus current owner plus source/readout closure",
            "physical invariant throat for any MTS-specific alpha/source response",
            "INVARIANT_DEVIATION_THROAT_RETAINED",
        ),
    ]
    rows: List[dict] = []
    for clause_id, symbol, definition, zero_route, current_status, status in data:
        row = row_base()
        row.update(
            {
                "clause_id": clause_id,
                "symbol": symbol,
                "definition": definition,
                "zero_route": zero_route,
                "current_status": current_status,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def imported_baseline_zero_rows() -> List[dict]:
    data = [
        (
            "IBZ4129_0_Hodge",
            "Delta_Hodge_EM",
            "0",
            "baseline branch uses observed Maxwell Hodge star *_obs[e_obs]",
            "standard local visible EM action supplied as matter sector",
            "valid as local-GR baseline input, not MTS derivation",
        ),
        (
            "IBZ4129_1_ZQ",
            "D_A ln Z_Q",
            "0",
            "baseline branch holds Maxwell kinetic normalization fixed in calibrated units",
            "constant alpha/mu0/e are imported empirical constants",
            "does not predict numerical alpha",
        ),
        (
            "IBZ4129_2_JQ",
            "D_A ln J_Q",
            "0",
            "baseline branch fixes current normalization and representation labels before readout",
            "standard charged matter sector supplied",
            "relative charge-label drift separately zero on fixed representation sectors",
        ),
        (
            "IBZ4129_3_CXF2",
            "C_XF2",
            "0",
            "baseline branch has no MTS hidden/motion/time F^2 counterterm",
            "standard visible EM action only",
            "MTS-specific F2 deviations must use bound branch",
        ),
    ]
    rows: List[dict] = []
    for zero_id, symbol, value, condition, authority, caveat in data:
        row = row_base()
        row.update(
            {
                "zero_id": zero_id,
                "symbol": symbol,
                "value": value,
                "condition": condition,
                "authority": authority,
                "caveat": caveat,
                "status": "BASELINE_ZERO_NOT_PARENT_PREDICTION",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def finite_bound_rows() -> List[dict]:
    data = [
        (
            "FBR4129_0_Delta_Hodge_EM",
            "Delta_Hodge_EM",
            "|Delta_chi_principal|+|Delta_chi_skewon|+L|dtheta_EM|+|C_Hodge_hidden|+|C_Hodge_readout|+|Delta_orientation_flux|",
            "dimensionless_or_tensor_owner_norm",
            "birefringence; dispersion; polarization rotation; EM cone; PPN preferred-frame",
            "observed Hodge owner theorem or public EM propagation/constitutive bounds",
        ),
        (
            "FBR4129_1_beta_ZQ",
            "beta_ZQ",
            "D_A ln Z_Q_eff with no-extra-F2/readout terms separated",
            "dimensionless per normalized A_N",
            "alpha drift; EM binding; WEP; clocks; Newton source mass",
            "parent curvature norm owner or finite Maxwell normalization bound",
        ),
        (
            "FBR4129_2_beta_JQ",
            "beta_JQ",
            "D_A ln J_Q_eff after fixed representation labels and current readout are separated",
            "dimensionless per normalized A_N",
            "Lorentz exchange; charge/current conservation; WEP; R10; source current",
            "same-current owner certificate or current normalization bound",
        ),
        (
            "FBR4129_3_b_alpha",
            "b_alpha",
            "b_alpha=2 z_g-s_XF2",
            "dimensionless per normalized A_N",
            "fine-structure drift; spectroscopy; clocks; R10; source coupling",
            "no-extra-F2 theorem plus current owner, or alpha-source product bound",
        ),
        (
            "FBR4129_4_EM_owner_static_total",
            "epsilon_EM_owner_static_4129",
            "|Delta_Hodge_EM|+|beta_ZQ|+|beta_JQ|+|b_alpha|+|C_EM_readout|+|DeltaJ_total|+|dB_impr|",
            "dimensionless_or_declared_component_norm",
            "local stationary Maxwell stress/source coupling",
            "all components zero or source-backed numeric bounds",
        ),
    ]
    rows: List[dict] = []
    for bound_id, symbol, formula, units, observable_links, required_input in data:
        row = row_base()
        row.update(
            {
                "bound_id": bound_id,
                "symbol": symbol,
                "formula": formula,
                "units": units,
                "observable_links": observable_links,
                "required_input": required_input,
                "status": "NONCLAIM_BOUND_SCHEMA_FILLED",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def no_overclaim_guard_rows() -> List[dict]:
    data = [
        (
            "NOG4129_0_alpha_value",
            "Do not claim MTS derives the numerical fine-structure constant or elementary charge from this checkpoint.",
            "GR reduction needs a supplied/local matter action with calibrated constants; absolute alpha prediction is a separate harder problem.",
            "ACTIVE",
        ),
        (
            "NOG4129_1_conformal_scale",
            "Do not treat EM cone/Hodge agreement as clock/source/impedance normalization.",
            "4D Maxwell Hodge on two-forms is conformally invariant, so scale/source gates remain.",
            "ACTIVE",
        ),
        (
            "NOG4129_2_baseline_vs_prediction",
            "Separate standard visible EM import from MTS-predicted EM deviations.",
            "Baseline zeros support local GR reduction only; deviations need parent theorem or empirical bounds.",
            "ACTIVE",
        ),
        (
            "NOG4129_3_no_gm_absorption",
            "Do not absorb EM owner residuals into fitted GM or source calibration.",
            "Any live EM source residual must appear in the finite vector and arena rows.",
            "ACTIVE",
        ),
    ]
    rows: List[dict] = []
    for guard_id, guard, reason, status in data:
        row = row_base()
        row.update(
            {
                "guard_id": guard_id,
                "guard": guard,
                "reason": reason,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[dict]:
    data = [
        (
            "DEC4129_0_baseline_locked",
            "The local-GR baseline may import standard visible Maxwell/charged matter with calibrated constants; this sets Hodge/current/normalization residuals to zero as baseline input, not as an MTS prediction.",
            "STANDARD_VISIBLE_EM_BASELINE_LOCKED",
            "use this branch when testing whether MTS can reduce to GR without solving all of QED first",
        ),
        (
            "DEC4129_1_parent_owner_unsigned",
            "The MTS parent-owned EM theorem is still unsigned because Hodge domain exhaustion, parent curvature norm, no-extra-F2, current owner, and readout closure are not all signed.",
            "PARENT_EM_OWNER_UNSIGNED",
            "keep deviation branch explicit",
        ),
        (
            "DEC4129_2_bounds_filled",
            "The three requested blockers beta_Hodge_EM, beta_ZQ, and beta_JQ now have precise nonclaim bound schemas.",
            "BOUND_SCHEMAS_FILLED",
            "next attack should target no-extra-F2/b_alpha because it is the invariant source-coupling throat",
        ),
        (
            "DEC4129_3_next",
            "Next target is the no-extra-F2 / b_alpha invariant throat.",
            "NEXT_NO_EXTRA_F2_BALPHA_SELECTED",
            "try to prove no independent visible F2 coefficient or fill alpha/source product bounds",
        ),
    ]
    rows: List[dict] = []
    for decision_id, decision, status, next_action in data:
        row = row_base()
        row.update(
            {
                "decision_id": decision_id,
                "decision": decision,
                "status": status,
                "next_action": next_action,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def status_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "status_id": "STATUS4129_0",
            "result": DECISION,
            "summary": (
                "4129 locks the clean distinction between standard visible EM as a calibrated local-GR matter-sector "
                "baseline and a stronger MTS parent-owned EM prediction. In the baseline branch, Delta_Hodge_EM, beta_ZQ, "
                "beta_JQ, and C_XF2 are zero by the imported standard Maxwell/charged-matter action, not by a new MTS "
                "derivation. The parent-owner theorem remains unsigned, so beta_Hodge_EM, beta_ZQ, beta_JQ, and b_alpha "
                "also get explicit nonclaim bound schemas."
            ),
            "baseline_em_locked": "True",
            "parent_em_owner_signed": "False",
            "bound_schemas_filled": "True",
            "score_ready": "False",
            "claim_state": "no local_GR, Newton, PPN, R10, Gdot, clock, EM prediction, Maxwell derivation, alpha derivation, or source-normalization pass",
            "next_target": "4130 no-extra-F2 b_alpha invariant throat",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4129_0",
            "target_doc": "4130-Y5-R2FR-no-extra-F2-balpha-invariant-throat.md",
            "target_script": "scripts/Y5_R2FR_4130_no_extra_F2_balpha_invariant_throat.py",
            "objective": (
                "attack the invariant alpha/source-coupling throat b_alpha=2 z_g-s_XF2 by trying to prove no independent "
                "visible F2 coefficient exists in the parent object language; if unsigned, stage alpha/source product bounds"
            ),
            "success_gate": "C_XF2/s_XF2 is parent-excluded, or b_alpha gets source-backed nonclaim bound schemas with clock, spectroscopy, R10, and WEP links",
            "reason": "4129 permits local-GR baseline import but leaves MTS-predicted EM deviations controlled by the invariant b_alpha throat.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4129_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4129_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4129_BRANCH_CONTRACT": SOURCE_DIR / "P8_Y5_R2FR_4129_BRANCH_CONTRACT.csv",
        "P8_Y5_R2FR_4129_OWNER_CLAUSES": SOURCE_DIR / "P8_Y5_R2FR_4129_OWNER_CLAUSES.csv",
        "P8_Y5_R2FR_4129_IMPORTED_BASELINE_ZEROS": SOURCE_DIR / "P8_Y5_R2FR_4129_IMPORTED_BASELINE_ZEROS.csv",
        "P8_Y5_R2FR_4129_FINITE_BOUND_SCHEMAS": SOURCE_DIR / "P8_Y5_R2FR_4129_FINITE_BOUND_SCHEMAS.csv",
        "P8_Y5_R2FR_4129_NO_OVERCLAIM_GUARDS": SOURCE_DIR / "P8_Y5_R2FR_4129_NO_OVERCLAIM_GUARDS.csv",
        "P8_Y5_R2FR_4129_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4129_DECISION_GATES.csv",
        "P8_Y5_R2FR_4129_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4129_STATUS.csv",
        "P8_Y5_R2FR_4129_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4129_NEXT_TARGET.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    status = status_rows()[0]
    sections = [
        "# 4129 - Observed Hodge / Current Owner Clause",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- Local-GR baseline branch may use standard visible Maxwell/charged matter with calibrated constants.",
        "- That baseline zero is not an MTS prediction of `alpha`, `e`, or absolute EM normalization.",
        "- MTS-specific EM deviations remain in explicit bound schemas for `beta_Hodge_EM`, `beta_ZQ`, `beta_JQ`, and `b_alpha`.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(["", "## Branch Contract", "", "| branch | status | meaning |", "|---|---|---|"])
    for row in branch_contract_rows():
        sections.append(f"| {row['branch']} | {row['status']} | {row['meaning']} |")
    sections.extend(["", "## Owner Clauses", "", "| symbol | status | current_status |", "|---|---|---|"])
    for row in owner_clause_rows():
        sections.append(f"| {row['symbol']} | {row['status']} | {row['current_status']} |")
    sections.extend(["", "## Bound Schemas", "", "| symbol | units | status |", "|---|---|---|"])
    for row in finite_bound_rows():
        sections.append(f"| {row['symbol']} | {row['units']} | {row['status']} |")
    sections.extend(["", "## Claim Ceiling", "", f"- {status['claim_state']}.", "- This checkpoint separates GR-compatible matter import from MTS-predicted EM structure.", "", "## Next Target", "", "- `4130-Y5-R2FR-no-extra-F2-balpha-invariant-throat.md`", ""])
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4129_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4129_BRANCH_CONTRACT": branch_contract_rows,
        "P8_Y5_R2FR_4129_OWNER_CLAUSES": owner_clause_rows,
        "P8_Y5_R2FR_4129_IMPORTED_BASELINE_ZEROS": imported_baseline_zero_rows,
        "P8_Y5_R2FR_4129_FINITE_BOUND_SCHEMAS": finite_bound_rows,
        "P8_Y5_R2FR_4129_NO_OVERCLAIM_GUARDS": no_overclaim_guard_rows,
        "P8_Y5_R2FR_4129_DECISION_GATES": decision_rows,
        "P8_Y5_R2FR_4129_STATUS": status_rows,
        "P8_Y5_R2FR_4129_NEXT_TARGET": next_target_rows,
    }
    for key, writer in writers.items():
        write_csv(outputs[key], writer())
    write_doc(outputs)
    return outputs


def flatten_rows(paths: Iterable[Path]) -> str:
    parts: List[str] = []
    for path in paths:
        for row in parse_csv(path):
            parts.append(" ".join(str(value) for value in row.values()))
    return " ".join(parts)


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, description: str, passed: bool, detail: str) -> None:
        row = row_base()
        row.update({"check_id": check_id, "description": description, "passed": str(bool(passed)), "detail": detail})
        checks.append(row)

    sources = source_register()
    add(
        "VAL4129_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add("VAL4129_1_doc", "checkpoint markdown exists and names decision", DOC_PATH.exists() and DECISION in DOC_PATH.read_text(encoding="utf-8"), str(DOC_PATH))

    parse_ok = True
    parse_counts: Dict[str, object] = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4129_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    branch_text = flatten_rows([outputs["P8_Y5_R2FR_4129_BRANCH_CONTRACT"]])
    branch_ok = all(token in branch_text for token in ["standard_visible_EM_baseline", "parent_owned_EM_prediction", "deviation_bound_branch"])
    add("VAL4129_3_branch_contract", "three branch contract separates baseline, parent prediction, and deviation bounds", branch_ok, "branch tokens checked")

    clause_text = flatten_rows([outputs["P8_Y5_R2FR_4129_OWNER_CLAUSES"]])
    clause_ok = all(token in clause_text for token in ["beta_Hodge_EM", "beta_ZQ", "beta_JQ", "b_alpha"])
    add("VAL4129_4_owner_clauses", "owner clauses cover beta_Hodge_EM, beta_ZQ, beta_JQ, and b_alpha", clause_ok, "owner tokens checked")

    zero_text = flatten_rows([outputs["P8_Y5_R2FR_4129_IMPORTED_BASELINE_ZEROS"]])
    zero_ok = all(token in zero_text for token in ["Delta_Hodge_EM", "D_A ln Z_Q", "D_A ln J_Q", "C_XF2", "BASELINE_ZERO_NOT_PARENT_PREDICTION"])
    add("VAL4129_5_baseline_zeros", "baseline zero rows are explicit and not parent predictions", zero_ok, "zero tokens checked")

    bound_text = flatten_rows([outputs["P8_Y5_R2FR_4129_FINITE_BOUND_SCHEMAS"]])
    bound_ok = all(token in bound_text for token in ["Delta_Hodge_EM", "beta_ZQ", "beta_JQ", "b_alpha", "epsilon_EM_owner_static_4129", "NONCLAIM_BOUND_SCHEMA_FILLED"])
    add("VAL4129_6_bound_schemas", "finite bound schemas cover requested owner terms and alpha throat", bound_ok, "bound tokens checked")

    guard_text = flatten_rows([outputs["P8_Y5_R2FR_4129_NO_OVERCLAIM_GUARDS"]])
    guard_ok = all(token in guard_text for token in ["numerical fine-structure", "conformally invariant", "standard visible EM import", "fitted GM"])
    add("VAL4129_7_guards", "no-overclaim guards block alpha, conformal, baseline, and GM absorption overclaims", guard_ok, "guard tokens checked")

    decision_text = flatten_rows([outputs["P8_Y5_R2FR_4129_DECISION_GATES"]])
    decision_ok = all(token in decision_text for token in ["STANDARD_VISIBLE_EM_BASELINE_LOCKED", "PARENT_EM_OWNER_UNSIGNED", "BOUND_SCHEMAS_FILLED", "NEXT_NO_EXTRA_F2_BALPHA_SELECTED"])
    add("VAL4129_8_decisions", "decision gates record baseline, unsigned parent owner, bounds, and next target", decision_ok, "decision tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4129_STATUS"])
    status_ok = bool(status) and status[0].get("result") == DECISION and status[0].get("baseline_em_locked") == "True" and status[0].get("parent_em_owner_signed") == "False"
    add("VAL4129_9_status", "status records baseline lock and unsigned parent owner", status_ok, "status row checked")

    nxt = parse_csv(outputs["P8_Y5_R2FR_4129_NEXT_TARGET"])
    next_ok = len(nxt) == 1 and nxt[0].get("target_doc") == "4130-Y5-R2FR-no-extra-F2-balpha-invariant-throat.md"
    add("VAL4129_10_next_target", "next target is no-extra-F2 b_alpha invariant throat", next_ok, str(nxt))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    add("VAL4129_11_no_claim_flags", "all generated rows remain no-claim and invalid for claim", no_claim, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4129*")) or any(FORMALIZATION.rglob("4129-Y5-R2FR*"))
    add("VAL4129_12_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4129_13_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4129_VALIDATION.csv"
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
