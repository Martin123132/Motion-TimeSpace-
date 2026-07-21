from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4531"
CLAIM_ID = "L-373"
MARKER = "PPC4161_OBSERVED_COFRAME_MATTER_DESCENT_OR_FIRST_EIGENMODE_LOCAL_BOUND_RUNNER_4531"
PACKET_MARKER = "PPC4161_PACKET_OBSERVED_COFRAME_MATTER_DESCENT_OR_FIRST_EIGENMODE_LOCAL_BOUND_RUNNER_4531"
DECISION = "OBSERVED_COFRAME_DESCENT_THEOREM_IS_EXACT_IF_PARENT_FUNCTOR_SIGNS_AND_FIRST_EIGENMODE_RUNNER_NOW_EXECUTES_NONCLAIM_DRYRUN"
NEXT_TARGET = "4532-Y5-R2FR-parent-matter-functor-signature-or-real-eigenmode-input-acquisition.md"

FORMAL_PATH = FORMAL / "547-PPC4161-observed-coframe-matter-descent-or-first-eigenmode-local-bound-runner.md"
DOC_PATH = POST / "4531-Y5-R2FR-observed-coframe-matter-descent-or-first-eigenmode-local-bound-runner.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4531_SOURCE_REGISTER.csv"
DESCENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4531_OBSERVED_COFRAME_DESCENT_THEOREM.csv"
PREACTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4531_PREACTION_WEIGHT_NO_GO_AND_FINITE_ROW.csv"
INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4531_FIRST_EIGENMODE_INPUT_ROWS.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4531_FIRST_EIGENMODE_RUNNER_RESULTS.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4531_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4531_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4531_NEXT_TARGET.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4531_VALIDATION.csv"

DOC_4530 = POST / "4530-Y5-R2FR-SGK-source-current-zero-or-first-Kvert-eigenvalue-bound.md"
VALIDATION_4530 = SOURCE_DIR / "P8_Y5_BRR545_4530_VALIDATION.csv"
DESCENT_4530 = SOURCE_DIR / "P8_Y5_R2FR_4530_SOURCE_CURRENT_DESCENT_IDENTITY.csv"
BOUNDARY_4530 = SOURCE_DIR / "P8_Y5_R2FR_4530_BOUNDARY_POYNTING_SPLIT.csv"
EIGEN_4530 = SOURCE_DIR / "P8_Y5_R2FR_4530_FIRST_KVERT_EIGENMODE_BOUND_CONTRACT.csv"
DESCENT_1575 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1575_RAB_MATTER_DESCENT_SIGNATURE.csv"
NO_SPECIES_CONTRACT = SOURCE_DIR / "P8_no_species_source_charge_CONTRACT.csv"
BAN_1416 = SOURCE_DIR / "P8_Y5_R10_1416_SOURCE_SLOT_CURRENT_RESCALING_BAN_ATTEMPT.csv"
VERT_1505 = SOURCE_DIR / "P8_Y5_R10_1505_DQ_VERTICALITY_TESTS.csv"
NCO_1079 = SOURCE_DIR / "P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv"
EM_POYNTING = SOURCE_DIR / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def line_of(path: Path, needle: str) -> int:
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def snippet(path: Path, needle: str) -> str:
    for line in text(path).splitlines():
        if needle in line:
            return line.strip()[:360]
    return ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body = []
    for row in rows:
        cells = [str(row.get(field, "")).replace("\n", "<br>") for field in fields]
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, sep, *body])


def as_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        value_text = str(value).strip()
        if not value_text or value_text.upper().startswith("MISSING") or value_text.upper().startswith("CLAIM"):
            return None
        return float(value_text)
    except ValueError:
        return None


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4531_00_doc4530", "4530 handoff", DOC_4530, "4531-Y5-R2FR-observed-coframe-matter-descent-or-first-eigenmode-local-bound-runner.md", "immediate target"),
        ("SRC4531_01_val4530", "4530 validation", VALIDATION_4530, "VAL4530_OVERALL", "prior step validated"),
        ("SRC4531_02_descent4530", "4530 source-current identity", DESCENT_4530, "J4530_0_full_variation_decomposition", "source-current chain rule"),
        ("SRC4531_03_boundary4530", "4530 boundary/Poynting split", BOUNDARY_4530, "B4530_2_radiative_poynting_flux", "boundary/wave split"),
        ("SRC4531_04_eigen4530", "4530 eigenmode contract", EIGEN_4530, "KBE4530_0_first_mode_contract", "first eigenmode formula"),
        ("SRC4531_05_descent1575", "1575 matter descent signature", DESCENT_1575, "MDS1575_0_action_form", "observed-coframe descent row"),
        ("SRC4531_06_nospecies", "no species source charge contract", NO_SPECIES_CONTRACT, "S1_matter_factorization", "matter functor condition"),
        ("SRC4531_07_ban1416", "1416 source slot ban attempt", BAN_1416, "BAN1416_6_verdict", "pre-action weight countermodel"),
        ("SRC4531_08_vert1505", "1505 Dq verticality tests", VERT_1505, "DQT1505_8_acceptance", "verticality gate"),
        ("SRC4531_09_nco1079", "1079 narrow current owner", NCO_1079, "NCO1079_5_species_action_weight", "Hilbert current subtheorem limit"),
        ("SRC4531_10_em_poynting", "EM/Poynting residual vector", EM_POYNTING, "EMF3502_1_radiative_poynting_flux", "radiative/nonminimal EM retained rows"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle, role in specs:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "label": label,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text(path),
                "line": line_of(path, needle),
                "snippet": snippet(path, needle),
                "role": role,
                "valid_for_claim": False,
            }
        )
    return rows


def descent_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "OCD4531_0_parent_functor",
            "claim_piece": "observed-coframe matter functor",
            "mathematical_statement": "There is a parent map q_matter(Phi)=(e_obs(q(Phi)), omega[e_obs], theta_univ) and ordinary matter is S_m=sum_A S_A[psi_A,q_matter(Phi)]+dB_A.",
            "derivation": "If this factorization is parent-signed, every vertical residual v with Dq[v]=0 has no bulk matter source through observed geometry.",
            "closes": "D_q Sbar · Dq[v_A]",
            "current_status": "EXACT_SUFFICIENT_THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "OCD4531_1_matter_lift",
            "claim_piece": "matter field lift is gauge/on-shell",
            "mathematical_statement": "delta_v psi_A is zero, gauge/Lorentz/diffeomorphism-owned, or matter-on-shell with only proper boundary variation.",
            "derivation": "Matter Euler terms then vanish or become exact/proper boundary terms rather than source charge.",
            "closes": "J_direct[v_A]",
            "current_status": "EXACT_CLAUSE_UNSIGNED_FOR_CURRENT_MTS",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "OCD4531_2_constant_sector",
            "claim_piece": "universal constants and labels silent along v",
            "mathematical_statement": "Lie_v theta_univ=0 and no material/source label is promoted into an active source coefficient.",
            "derivation": "This removes the sum_r J_theta^r Lie_v theta_r term in the 4530 decomposition.",
            "closes": "constant/material source-current term",
            "current_status": "PARTLY_CONTRACTED_NOT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "OCD4531_3_no_preaction_weight",
            "claim_piece": "no species/source multiplier inside S_m",
            "mathematical_statement": "Hom(SpeciesLabel,Coeff_active_source)=empty inside the parent action; S_m=sum_A w_A S_A is illegal unless w_A is fixed universal representation data already inside theta_univ.",
            "derivation": "This is the missing move that current ownership alone cannot supply: Hilbert variation inherits w_A if w_A is already in S_m.",
            "closes": "pre-action source weight countermodel",
            "current_status": "NEEDED_FOR_THEOREM_ZERO_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "OCD4531_4_boundary_clause",
            "claim_piece": "proper boundary and worldtube term",
            "mathematical_statement": "delta_v B_A is zero, exact/proper, compact-support silent, or retained in the absolute boundary envelope.",
            "derivation": "Bulk descent is not enough; this clause prevents edge or Poynting flux from masquerading as source silence.",
            "closes": "delta_v B_m",
            "current_status": "BOUNDARY_RETAINED_UNLESS_SIGNED",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "OCD4531_5_exact_zero_theorem",
            "claim_piece": "observed-coframe descent implies J_A=0",
            "mathematical_statement": "If OCD4531_0 through OCD4531_4 and Dq[v_A]=0 hold, then delta_v S_matter=0 and J_A=0.",
            "derivation": "Insert each signed clause into the 4530 full variation identity.",
            "closes": "SGK source-current zero premise",
            "current_status": "THEOREM_DERIVED_APPLICATION_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "OCD4531_6_EM_clause",
            "claim_piece": "Maxwell/EM stress treatment",
            "mathematical_statement": "Minimal stationary EM stress belongs to the same observed Hilbert source; radiative Poynting flux and nonminimal hidden F^2 couplings are retained unless the parent EM functor forbids them.",
            "derivation": "This prevents double-counting bound EM energy while refusing to hide wave/background flux.",
            "closes": "Maxwell/EM stress branch consistency",
            "current_status": "SPLIT_DERIVED_VALUES_OR_ZERO_CLAUSES_MISSING",
            "valid_for_claim": False,
        },
    ]


def preaction_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "PA4531_0_countermodel",
            "object": "pre-action species/source multiplier",
            "countermodel": "S_matter=sum_A w_A S_A[psi_A,e_obs,theta_A]",
            "why_not_killed": "Hilbert variation gives T_obs=sum_A w_A T_A; current ownership only acts after the action is chosen.",
            "theorem_zero_requires": "parent object-language/action-measure proof that w_A is not a legal constructor",
            "finite_fallback": "R_source_weight or current_rescaling coefficient row",
            "current_status": "SURVIVES_WITHOUT_PARENT_GRAMMAR",
            "valid_for_claim": False,
        },
        {
            "row_id": "PA4531_1_allowed_representation_data",
            "object": "ordinary masses/charges/representation constants",
            "countermodel": "theta_A are fixed labels but not active source multipliers",
            "why_not_killed": "labels are allowed as matter representation data; they are harmless only if Lie_v theta_A=0 and no active source coefficient reads them",
            "theorem_zero_requires": "constant-sector universality plus no marker extension",
            "finite_fallback": "constant-sector response coefficient",
            "current_status": "CONTRACTED_NOT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "row_id": "PA4531_2_readout_reentry",
            "object": "post-readout/radiative regeneration",
            "countermodel": "S_eff or readout map regenerates f_X F^2, alpha_X, or source-normalization coefficient",
            "why_not_killed": "variation-before-readout kills retroactive source redefinition but not a parent-signed effective operator",
            "theorem_zero_requires": "readout/effective action descends through the same observed coframe functor",
            "finite_fallback": "R_readout or EM cross-term coefficient",
            "current_status": "RETAINED_PARALLEL_GATE",
            "valid_for_claim": False,
        },
    ]


def eigenmode_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "EIG4531_live_missing",
            "description": "live current-MTS first physical SGK/Kvert mode",
            "h_i": "MISSING_H_I",
            "m_i2": "MISSING_M_I2",
            "K_i": "MISSING_K_I",
            "Q_iS": "MISSING_Q_IS",
            "Q_iT": "MISSING_Q_IT",
            "G_N_Ms_mt": "MISSING_GN_MS_MT",
            "alpha_bound": "MISSING_ALPHA_BOUND",
            "source_path": str(EIGEN_4530),
            "units": "undeclared",
            "valid_for_claim": False,
        },
        {
            "input_id": "EIG4531_toy_nonclaim",
            "description": "toy dry-run row to prove runner math and claim refusal",
            "h_i": "1.0",
            "m_i2": "4.0",
            "K_i": "1.0e-6",
            "Q_iS": "1.0",
            "Q_iT": "1.0",
            "G_N_Ms_mt": "1.0",
            "alpha_bound": "1.0e-6",
            "source_path": "TOY_NONCLAIM_INTERNAL_DRYRUN",
            "units": "dimensionless_normalized_toy",
            "valid_for_claim": False,
        },
    ]


def run_eigenmode_rows(inputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    valid_claim_rows = 0
    for row in inputs:
        h_i = as_float(row["h_i"])
        m_i2 = as_float(row["m_i2"])
        K_i = as_float(row["K_i"])
        Q_iS = as_float(row["Q_iS"])
        Q_iT = as_float(row["Q_iT"])
        denom = as_float(row["G_N_Ms_mt"])
        alpha_bound = as_float(row["alpha_bound"])
        missing = [
            name
            for name, value in [
                ("h_i", h_i),
                ("m_i2", m_i2),
                ("K_i", K_i),
                ("Q_iS", Q_iS),
                ("Q_iT", Q_iT),
                ("G_N_Ms_mt", denom),
                ("alpha_bound", alpha_bound),
            ]
            if value is None
        ]
        valid_for_claim = str(row.get("valid_for_claim", "False")).lower() == "true"
        if missing:
            results.append(
                {
                    "result_id": f"RUN4531_{row['input_id']}",
                    "input_id": row["input_id"],
                    "lambda_i": "",
                    "alpha_i": "",
                    "alpha_bound": row["alpha_bound"],
                    "comparison": "not_run",
                    "status": "BLOCKED_MISSING_INPUTS",
                    "issues": ";".join(missing),
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
            continue
        if h_i <= 0 or m_i2 <= 0 or denom == 0 or alpha_bound < 0:
            results.append(
                {
                    "result_id": f"RUN4531_{row['input_id']}",
                    "input_id": row["input_id"],
                    "lambda_i": "",
                    "alpha_i": "",
                    "alpha_bound": alpha_bound,
                    "comparison": "not_run",
                    "status": "REJECT_BAD_SIGN_OR_DENOMINATOR",
                    "issues": "requires h_i>0, m_i2>0, nonzero denominator, alpha_bound>=0",
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
            continue
        lambda_i = math.sqrt(h_i) / math.sqrt(m_i2)
        alpha_i = K_i * Q_iS * Q_iT / (denom * m_i2)
        comparison = "pass_bound" if abs(alpha_i) <= alpha_bound else "fail_bound"
        claim_allowed = bool(valid_for_claim and comparison == "pass_bound" and str(row["source_path"]).startswith(str(ROOT)))
        valid_claim_rows += int(claim_allowed)
        results.append(
            {
                "result_id": f"RUN4531_{row['input_id']}",
                "input_id": row["input_id"],
                "lambda_i": f"{lambda_i:.12g}",
                "alpha_i": f"{alpha_i:.12g}",
                "alpha_bound": f"{alpha_bound:.12g}",
                "comparison": comparison,
                "status": "DRYRUN_NONCLAIM" if not claim_allowed else "CLAIM_ROW_PASS",
                "issues": "toy_or_nonclaim_row" if not claim_allowed else "",
                "valid_for_claim": valid_for_claim,
                "claim_allowed": claim_allowed,
            }
        )
    results.append(
        {
            "result_id": "RUN4531_OVERALL",
            "input_id": "all",
            "lambda_i": "",
            "alpha_i": "",
            "alpha_bound": "",
            "comparison": "claim_false" if valid_claim_rows == 0 else "claim_candidate",
            "status": "NO_VALID_CLAIM_ROWS" if valid_claim_rows == 0 else "VALID_CLAIM_ROWS_PRESENT",
            "issues": "live row missing; toy row nonclaim" if valid_claim_rows == 0 else "",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return results


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG4531_0_descent_theorem",
            "gate": "derive observed-coframe matter descent sufficient theorem",
            "status": "PASS_FORMAL",
            "detail": "OCD4531 rows prove J_A=0 if parent functor, constants, no pre-action weights and boundary clauses sign.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4531_1_current_application",
            "gate": "apply descent theorem to current MTS",
            "status": "BLOCKED_UNSIGNED",
            "detail": "parent functor, Dq verticality, no source weight and boundary clauses are not yet signed.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4531_2_runner_executable",
            "gate": "execute first eigenmode runner dryrun",
            "status": "PASS_NONCLAIM_DRYRUN",
            "detail": "toy row computes lambda/alpha; live row refuses missing h_i,m_i,K_i,Q_iS,Q_iT/bound inputs.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4531_3_claim_safety",
            "gate": "avoid claiming local GR/Newton/R10",
            "status": "PASS_BLOCKED",
            "detail": "all rows remain invalid for claim until exact theorem signs or numeric source-backed finite rows pass.",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4531_0",
            "decision": DECISION,
            "meaning": "The exact route is sharpened into a parent matter-functor theorem; the empirical fallback is no longer just prose because the first eigenmode lambda/alpha runner executes and refuses the live row until real inputs exist.",
            "next_action": NEXT_TARGET,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "either sign the parent matter functor/no-source-weight grammar or acquire first real h_i,m_i,K_i,Q_iS,Q_iT and bound-curve inputs",
            "why": "This is now the clean fork between derived local GR and scoreable finite residual physics.",
            "valid_for_claim": False,
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    descent: list[dict[str, Any]],
    preaction: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    source_failures = [row["source_id"] for row in sources if not row["path_exists"] or not row["needle_found"]]
    checks.append(
        {
            "validation_id": "VAL4531_00_sources",
            "status": "PASS" if not source_failures else "FAIL",
            "detail": "all source paths exist and needles found" if not source_failures else ";".join(source_failures),
        }
    )
    descent_ids = {row["theorem_id"] for row in descent}
    checks.append(
        {
            "validation_id": "VAL4531_01_descent",
            "status": "PASS" if {"OCD4531_0_parent_functor", "OCD4531_3_no_preaction_weight", "OCD4531_5_exact_zero_theorem"} <= descent_ids else "FAIL",
            "detail": "parent functor, no-preaction-weight and exact zero theorem rows present",
        }
    )
    preaction_ids = {row["row_id"] for row in preaction}
    checks.append(
        {
            "validation_id": "VAL4531_02_countermodel",
            "status": "PASS" if "PA4531_0_countermodel" in preaction_ids else "FAIL",
            "detail": "pre-action weight countermodel is retained rather than hidden",
        }
    )
    input_ids = {row["input_id"] for row in inputs}
    runner_status = {row["result_id"]: row["status"] for row in runner}
    checks.append(
        {
            "validation_id": "VAL4531_03_runner",
            "status": "PASS" if {"EIG4531_live_missing", "EIG4531_toy_nonclaim"} <= input_ids and runner_status.get("RUN4531_EIG4531_live_missing") == "BLOCKED_MISSING_INPUTS" and runner_status.get("RUN4531_EIG4531_toy_nonclaim") == "DRYRUN_NONCLAIM" else "FAIL",
            "detail": "runner blocks live missing row and computes toy nonclaim row",
        }
    )
    checks.append(
        {
            "validation_id": "VAL4531_04_claims_blocked",
            "status": "PASS" if all(row["valid_for_claim"] is False for row in gates) and all(str(row.get("claim_allowed", "False")).lower() == "false" for row in runner) else "FAIL",
            "detail": "all claim gates and runner outputs remain nonclaim",
        }
    )
    csv_files = [
        SOURCE_REGISTER,
        DESCENT_CSV,
        PREACTION_CSV,
        INPUT_CSV,
        RUNNER_CSV,
        GATES_CSV,
        DECISION_CSV,
        NEXT_CSV,
    ]
    parse_failures = []
    for path in csv_files:
        try:
            with path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            if not rows:
                parse_failures.append(path.name)
        except Exception as exc:
            parse_failures.append(f"{path.name}:{exc}")
    checks.append(
        {
            "validation_id": "VAL4531_05_csv_parse",
            "status": "PASS" if not parse_failures else "FAIL",
            "detail": "all generated CSV files parse and have rows" if not parse_failures else ";".join(parse_failures),
        }
    )
    checks.append(
        {
            "validation_id": "VAL4531_06_pycache_absent",
            "status": "PASS" if not (SCRIPT_DIR / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after cleanup",
        }
    )
    overall = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "validation_id": "VAL4531_OVERALL",
            "status": overall,
            "detail": "4531 observed-coframe descent theorem and first eigenmode runner dryrun" if overall == "PASS" else "4531 validation failed",
        }
    )
    return checks


def build_doc(
    sources: list[dict[str, Any]],
    descent: list[dict[str, Any]],
    preaction: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> str:
    return f"""# 4531 — Observed Coframe Matter Descent Or First Eigenmode Local Bound Runner

Marker: `{MARKER}`  
Packet marker: `{PACKET_MARKER}`  
Decision: `{DECISION}`  
Generated: `{now()}`

## What Moved

- The exact theorem route is no longer hand-wavy: if matter is a parent functor of the observed coframe/connection and universal constants, then `J_A=0` follows by the 4530 chain rule.
- The dangerous countermodel is kept explicit: `S_matter=sum_A w_A S_A` survives Hilbert-current ownership unless parent object-language/action-measure grammar forbids `w_A`.
- The finite route is now executable: the first eigenmode runner computes `lambda_i=sqrt(h_i)/m_i` and `alpha_i=K_i Q_iS Q_iT/(G_N M_S m_T m_i^2)`.
- The live row correctly refuses to claim because real `h_i,m_i,K_i,Q_iS,Q_iT` and bound-curve inputs are still absent; a toy row proves the runner math without becoming evidence.

## Observed-Coframe Descent Theorem

{md_table(descent)}

## Pre-Action Weight No-Go

{md_table(preaction)}

## First Eigenmode Input Rows

{md_table(inputs)}

## First Eigenmode Runner Results

{md_table(runner)}

## Claim Gates

{md_table(gates)}

## Decision

{md_table(decisions)}

## Source Register

{md_table(sources)}

## Validation

{md_table(validation)}
"""


def append_once(path: Path, marker: str, block: str) -> None:
    current = text(path)
    if marker in current:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        if current and not current.endswith("\n"):
            handle.write("\n")
        handle.write("\n")
        handle.write(block.strip())
        handle.write("\n")


def append_claim_once() -> None:
    current = text(CLAIMS_PATH)
    if f"{CLAIM_ID}," in current:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_r2fr_matter_descent_eigenmode_runner",
        "claim": "4531 derives the observed-coframe matter-descent sufficient theorem, preserves the pre-action species-weight countermodel, and executes the first Kvert eigenmode nonclaim dry-runner.",
        "current_evidence": "Generated observed-coframe descent theorem, pre-action no-go rows, first eigenmode inputs, runner results, claim gates and validation P8_Y5_BRR545_4531_VALIDATION.csv.",
        "status": "conditional_internal_nonclaim_runner_executable_values_missing",
        "next_test": NEXT_TARGET,
        "key_risk": "Parent matter functor/no-source-weight grammar is unsigned and the live eigenmode row has no numeric source-backed inputs.",
        "sector": "local_gr_newton",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Mistaking the toy dry-run row or formal descent theorem for current MTS local-GR recovery.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    descent = descent_rows()
    preaction = preaction_rows()
    inputs = eigenmode_input_rows()
    runner = run_eigenmode_rows(inputs)
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(DESCENT_CSV, descent)
    write_csv(PREACTION_CSV, preaction)
    write_csv(INPUT_CSV, inputs)
    write_csv(RUNNER_CSV, runner)
    write_csv(GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, descent, preaction, inputs, runner, gates)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, descent, preaction, inputs, runner, gates, decisions, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4531 Observed Coframe Matter Descent Or First Eigenmode Local Bound Runner

Marker: `{MARKER}`  
The local-GR fork now has an exact matter-descent theorem and an executable empirical fallback. If ordinary matter is a parent functor only of `e_obs(q(Phi))`, `omega[e_obs]`, and universal constants, then the 4530 chain rule gives `J_A=0`. If the parent functor/no-source-weight grammar does not sign, the first eigenmode runner computes `lambda_i` and `alpha_i` but refuses the live claim until real `h_i,m_i,K_i,Q_iS,Q_iT` rows exist.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4531 Packet Integration

Marker: `{PACKET_MARKER}`  
The PPC4161 packet now has both lanes active: exact observed-coframe matter descent if parent-signed, and a nonclaim first-eigenmode local-bound runner if not. Next target: `{NEXT_TARGET}`.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
