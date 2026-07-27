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

CHECKPOINT = "4532"
CLAIM_ID = "L-374"
MARKER = "PPC4161_PARENT_MATTER_FUNCTOR_SIGNATURE_OR_REAL_EIGENMODE_INPUT_ACQUISITION_4532"
PACKET_MARKER = "PPC4161_PACKET_PARENT_MATTER_FUNCTOR_SIGNATURE_OR_REAL_EIGENMODE_INPUT_ACQUISITION_4532"
DECISION = "PARENT_MATTER_FUNCTOR_SIGNATURE_IS_A_CLEAN_SUFFICIENT_THEOREM_BUT_REAL_EIGENMODE_INPUTS_REMAIN_PARTIAL_NONCLAIM"
NEXT_TARGET = "4533-Y5-R2FR-action-measure-owner-proof-or-first-real-eigenmode-source-pack.md"

FORMAL_PATH = FORMAL / "548-PPC4161-parent-matter-functor-signature-or-real-eigenmode-input-acquisition.md"
DOC_PATH = POST / "4532-Y5-R2FR-parent-matter-functor-signature-or-real-eigenmode-input-acquisition.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4532_SOURCE_REGISTER.csv"
FUNCTOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4532_PARENT_MATTER_FUNCTOR_SIGNATURE.csv"
ACQUISITION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4532_REAL_EIGENMODE_INPUT_ACQUISITION_MATRIX.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4532_EIGENMODE_INPUT_VALIDATOR_RESULTS.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4532_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4532_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4532_NEXT_TARGET.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4532_VALIDATION.csv"

DOC_4531 = POST / "4531-Y5-R2FR-observed-coframe-matter-descent-or-first-eigenmode-local-bound-runner.md"
VALIDATION_4531 = SOURCE_DIR / "P8_Y5_BRR545_4531_VALIDATION.csv"
DESCENT_4531 = SOURCE_DIR / "P8_Y5_R2FR_4531_OBSERVED_COFRAME_DESCENT_THEOREM.csv"
PREACTION_4531 = SOURCE_DIR / "P8_Y5_R2FR_4531_PREACTION_WEIGHT_NO_GO_AND_FINITE_ROW.csv"
RUNNER_4531 = SOURCE_DIR / "P8_Y5_R2FR_4531_FIRST_EIGENMODE_RUNNER_RESULTS.csv"
NO_SPECIES_CONTRACT = SOURCE_DIR / "P8_no_species_source_charge_CONTRACT.csv"
BAN_1416 = SOURCE_DIR / "P8_Y5_R10_1416_SOURCE_SLOT_CURRENT_RESCALING_BAN_ATTEMPT.csv"
RD_CONTRACT = SOURCE_DIR / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv"
RD_VARIATION = SOURCE_DIR / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv"
REQ_1573 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1573_TAU_R10_REQUIRED_INPUTS.csv"
SCORING_1573 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1573_TAU_R10_SCORING_INTERFACE_TEMPLATE_NONCLAIM.csv"
EXT_1579 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1579_EXTERNAL_BOUND_AUDIT.csv"
DRY_1579 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1579_COMPARATOR_DRY_RUN.csv"
GATE_3099 = SOURCE_DIR / "P8_Y5_R2FR_3099_ZX_MX2_TAUPPN_INPUT_GATE.csv"
BOUND_3099 = SOURCE_DIR / "P8_Y5_R2FR_3099_CG_NORMALIZED_BOUND_ROW.csv"
RANGE_3099 = SOURCE_DIR / "P8_Y5_R2FR_3099_RANGE_BRANCH_CLASSIFIER.csv"
KI_3897 = SOURCE_DIR / "P8_Y5_R2FR_3897_MEMORY_KI_PROJECTION_DERIVATION.csv"
PHY_3897 = SOURCE_DIR / "P8_Y5_R2FR_3897_FIRST_PHYSICAL_MEMORY_ROW_SKELETON.csv"
STATUS_3897 = SOURCE_DIR / "P8_Y5_R2FR_3897_STATUS.csv"
SIK_3308 = SOURCE_DIR / "P8_Y5_R2FR_3308_SOURCE_COEFFICIENT_SIK_GATE.csv"
PROXY_3308 = SOURCE_DIR / "P8_Y5_R2FR_3308_UNIT_MODE_FACTOR_SENSITIVITY_PROXY.csv"


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
        body.append("| " + " | ".join(str(row.get(field, "")).replace("\n", "<br>") for field in fields) + " |")
    return "\n".join([header, sep, *body])


def as_float(value: Any) -> float | None:
    try:
        value_text = str(value).strip()
        if not value_text or value_text.upper().startswith(("MISSING", "REVIEW", "SYMBOLIC", "CANDIDATE", "FORMAL", "NOT_", "BLOCK")):
            return None
        return float(value_text)
    except (TypeError, ValueError):
        return None


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4532_00_doc4531", "4531 handoff", DOC_4531, "4532-Y5-R2FR-parent-matter-functor-signature-or-real-eigenmode-input-acquisition.md", "immediate target"),
        ("SRC4532_01_val4531", "4531 validation", VALIDATION_4531, "VAL4531_OVERALL", "prior step validated"),
        ("SRC4532_02_descent4531", "4531 observed-coframe theorem", DESCENT_4531, "OCD4531_5_exact_zero_theorem", "exact theorem premise"),
        ("SRC4532_03_preact4531", "4531 pre-action no-go", PREACTION_4531, "PA4531_0_countermodel", "surviving countermodel"),
        ("SRC4532_04_runner4531", "4531 eigenmode runner results", RUNNER_4531, "RUN4531_EIG4531_live_missing", "live runner block"),
        ("SRC4532_05_no_species", "no species source charge contract", NO_SPECIES_CONTRACT, "S1_matter_factorization", "matter functor source"),
        ("SRC4532_06_ban1416", "1416 source slot ban", BAN_1416, "BAN1416_6_verdict", "grammar not proved"),
        ("SRC4532_07_rd_contract", "response doublet contract", RD_CONTRACT, "RD516_3_positive_operator", "positive operator candidate"),
        ("SRC4532_08_rd_variation", "response doublet variation", RD_VARIATION, "AV517_5_positive_theorem", "energy identity candidate"),
        ("SRC4532_09_req1573", "1573 required R10 inputs", REQ_1573, "REQ1573_0_ZR", "Z_R/M_R input requirements"),
        ("SRC4532_10_score1573", "1573 scoring template", SCORING_1573, "SCORE1573_0_symbolic_kernel", "symbolic R10 alpha formula"),
        ("SRC4532_11_ext1579", "1579 external bound audit", EXT_1579, "EXT1579_0_R10", "external R10 bound status"),
        ("SRC4532_12_dry1579", "1579 comparator dry-run", DRY_1579, "DRY1579_0_R10", "blocked comparator"),
        ("SRC4532_13_gate3099", "3099 ZX/MX2 gate", GATE_3099, "ZMG3099_1_ZX_positive", "Z_X/M_X2 gate"),
        ("SRC4532_14_bound3099", "3099 normalized bound row", BOUND_3099, "NGB3099_0_alpha_proxy_input", "proxy PPN bound"),
        ("SRC4532_15_range3099", "3099 range classifier", RANGE_3099, "RBC3099_5_current_AX1090", "range branch status"),
        ("SRC4532_16_ki3897", "3897 K_i projection map", KI_3897, "KI3897_5_R10", "symbolic K_i coverage"),
        ("SRC4532_17_phy3897", "3897 first physical rows", PHY_3897, "PHY3897_1_gamma_coefficient_row", "physical row skeleton"),
        ("SRC4532_18_status3897", "3897 status", STATUS_3897, "PASS_MEMORY_KI_PROJECTION_MAP_DERIVED", "symbolic projection status"),
        ("SRC4532_19_sik3308", "3308 source coefficient gate", SIK_3308, "SIK3308_2_combined", "finite source coefficient gate"),
        ("SRC4532_20_proxy3308", "3308 unit-mode proxy", PROXY_3308, "UP3308_LC3308_scalar_WEP3306_0_MICROSCOPE_Ti_Pt", "diagnostic sensitivity proxy"),
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


def functor_rows() -> list[dict[str, Any]]:
    return [
        {
            "signature_id": "PMF4532_0_parent_functor",
            "clause": "ordinary matter action is a parent natural transformation through observed coframe data",
            "mathematical_form": "S_m = Σ_A S_A[ψ_A, e_obs(q(Φ)), ω[e_obs], A_gauge, θ_univ] + dB_A",
            "derivation_effect": "for v in ker Dq and gauge/on-shell matter lift, the observed-geometry variation term in δ_v S_m vanishes",
            "would_close": "D_q Sbar · Dq[v]",
            "current_status": "SUFFICIENT_THEOREM_WRITTEN_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "signature_id": "PMF4532_1_single_measure_owner",
            "clause": "one parent action measure and one matter functor exclude per-species source multipliers",
            "mathematical_form": "Hom(SpeciesLabel, Coeff_active_source)=∅ inside constructors of S_parent",
            "derivation_effect": "rules out S_m=Σ_A w_A S_A as a legal active-source modification",
            "would_close": "pre-action source weight countermodel",
            "current_status": "THE_NEEDED_MOVE_BUT_OBJECT_LANGUAGE_OWNER_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "signature_id": "PMF4532_2_representation_labels",
            "clause": "masses, charges, spins, material labels are representation data, not active gravitational source coefficients",
            "mathematical_form": "Lie_v θ_univ=0 and ∂θ/∂Z=0 unless an explicit retained residual coefficient is emitted",
            "derivation_effect": "constant/material source-current terms vanish or become finite coefficient rows",
            "would_close": "Σ_r J_θ^r Lie_v θ_r",
            "current_status": "CONTRACTED_NOT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "signature_id": "PMF4532_3_boundary_and_effective_action",
            "clause": "boundary/readout/effective action preserves the same observed-coframe functor or emits residuals",
            "mathematical_form": "δ_v B_A=0/proper or B_A enters |J|+|B| envelope; S_eff has no new f_X F²/source-normalization operator unless retained",
            "derivation_effect": "prevents Poynting/nonminimal EM/readout terms from hiding inside theorem-zero",
            "would_close": "boundary and readout re-entry leakage",
            "current_status": "SPLIT_DERIVED_VALUES_OR_ZERO_CLAUSES_MISSING",
            "valid_for_claim": False,
        },
        {
            "signature_id": "PMF4532_4_exact_J_zero",
            "clause": "parent functor signature plus Dq verticality implies source-current zero",
            "mathematical_form": "PMF4532_0..3 and Dq[v]=0 ⇒ δ_v S_m=0 ⇒ J_A=0",
            "derivation_effect": "feeds the SGK local-zero theorem without a closure axiom",
            "would_close": "source-current premise of local GR branch",
            "current_status": "THEOREM_CLEAN_APPLICATION_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "signature_id": "PMF4532_5_failure_policy",
            "clause": "if any functor signature clause fails, emit finite eigenmode/source rows rather than claiming local GR",
            "mathematical_form": "α_i(λ_i)=K_i Q_iS Q_iT/(G_N M_S m_T m_i²), λ_i=√h_i/m_i",
            "derivation_effect": "turns failed exact descent into a scoreable residual path",
            "would_close": "anti-circling policy",
            "current_status": "RUNNER_READY_INPUTS_PARTIAL",
            "valid_for_claim": False,
        },
    ]


def acquisition_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "ACQ4532_0_h_i_or_ZR",
            "runner_symbol": "h_i / Z_R",
            "best_current_source": str(REQ_1573),
            "candidate_value": "MISSING_ZR",
            "candidate_status": "EXPLICIT_REQUIRED_INPUT_MISSING",
            "usable_now": False,
            "why": "1573 requires positive same-frame parent-normalized kinetic value; no numeric/source-backed row found.",
            "next_evidence": "parent quadratic block or positive operator theorem with units",
            "valid_for_claim": False,
        },
        {
            "input_id": "ACQ4532_1_m_i2_or_MR2",
            "runner_symbol": "m_i^2 / M_R^2",
            "best_current_source": str(REQ_1573),
            "candidate_value": "MISSING_MR2",
            "candidate_status": "EXPLICIT_REQUIRED_INPUT_MISSING",
            "usable_now": False,
            "why": "mass/range denominator is not sourced; range branch cannot be classified.",
            "next_evidence": "parent Hessian/mass-gap eigenvalue with units or no-pole theorem",
            "valid_for_claim": False,
        },
        {
            "input_id": "ACQ4532_2_K_i_projection",
            "runner_symbol": "K_i",
            "best_current_source": str(KI_3897),
            "candidate_value": "symbolic K_gamma, K_Gdot, K_R10 maps; alpha3/alpha2/xi candidate zero rows",
            "candidate_status": "SYMBOLIC_PROJECTION_MAP_DERIVED_NUMERIC_VALUES_MISSING",
            "usable_now": False,
            "why": "3897 derives arena projection structure but not numeric K_i for the first physical SGK/Kvert mode.",
            "next_evidence": "observed metric/readout coefficients c_space,c_lapse,c_R10 or parent-signed symmetry zero",
            "valid_for_claim": False,
        },
        {
            "input_id": "ACQ4532_3_Q_iS_Q_iT",
            "runner_symbol": "Q_iS,Q_iT / beta_S,beta_T",
            "best_current_source": str(REQ_1573),
            "candidate_value": "MISSING_SOURCE_CHARGE; MISSING_TEST_CHARGE",
            "candidate_status": "EXPLICIT_REQUIRED_INPUT_MISSING",
            "usable_now": False,
            "why": "matter functor/source-current zero is conditional and no finite source/test charge row is source-backed.",
            "next_evidence": "parent matter descent zero or material response tensor/source charge rows",
            "valid_for_claim": False,
        },
        {
            "input_id": "ACQ4532_4_alpha_bound_R10",
            "runner_symbol": "alpha_bound(lambda)",
            "best_current_source": str(EXT_1579),
            "candidate_value": "390 reviewed candidate curve rows",
            "candidate_status": "EXTERNAL_REVIEW_CANDIDATE_NONCLAIM",
            "usable_now": False,
            "why": "external curve exists as reviewed candidate but accepted_for_scoring=false and live MTS λ/α inputs are missing.",
            "next_evidence": "manual/official QA acceptance plus internal MTS λ_i/α_i row",
            "valid_for_claim": False,
        },
        {
            "input_id": "ACQ4532_5_alpha_proxy_PPN",
            "runner_symbol": "PPN proxy bound",
            "best_current_source": str(BOUND_3099),
            "candidate_value": "0.00578801540146505096",
            "candidate_status": "SOURCE_BACKED_PROXY_NONCLAIM",
            "usable_now": False,
            "why": "proxy bound is useful for diagnostics but not the first Kvert eigenmode without Z_X, τ_PPN, S_PPN and range transfer.",
            "next_evidence": "same-parent Z_X/M_X²/τ_PPN/S_PPN normalization",
            "valid_for_claim": False,
        },
        {
            "input_id": "ACQ4532_6_WEP_unit_proxy",
            "runner_symbol": "unit mode-factor sensitivity proxy",
            "best_current_source": str(PROXY_3308),
            "candidate_value": "1.0345834325e-15 first MICROSCOPE unit proxy",
            "candidate_status": "DIAGNOSTIC_ONLY_NONCLAIM",
            "usable_now": False,
            "why": "proxy assumes |K_i|=1 and lacks exact materials, source charge and confidence convention.",
            "next_evidence": "real K_i(lambda), exact material/source vectors and confidence conversion",
            "valid_for_claim": False,
        },
        {
            "input_id": "ACQ4532_7_live_runner_row",
            "runner_symbol": "complete first eigenmode row",
            "best_current_source": str(RUNNER_4531),
            "candidate_value": "BLOCKED_MISSING_INPUTS",
            "candidate_status": "RUNNER_REFUSES_LIVE_ROW",
            "usable_now": False,
            "why": "live row lacks every numeric MTS-side input and alpha bound.",
            "next_evidence": "replace live row placeholders with source-backed values",
            "valid_for_claim": False,
        },
    ]


def validator_rows(acquisition: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    usable = 0
    for row in acquisition:
        numeric = as_float(row["candidate_value"])
        local_source_exists = Path(row["best_current_source"]).exists()
        source_backed = local_source_exists and "MISSING" not in str(row["candidate_value"]) and "NONCLAIM" not in row["candidate_status"]
        claim_ready = bool(row["usable_now"] and numeric is not None and source_backed and row["valid_for_claim"])
        usable += int(claim_ready)
        rows.append(
            {
                "validation_row_id": f"VALRUN4532_{row['input_id']}",
                "input_id": row["input_id"],
                "numeric_value_detected": numeric is not None,
                "source_path_exists": local_source_exists,
                "source_backed_candidate": source_backed,
                "usable_now": row["usable_now"],
                "claim_ready": claim_ready,
                "status": "ACCEPT_CLAIM_INPUT" if claim_ready else "REJECT_NONCLAIM_OR_MISSING",
                "reason": row["why"],
            }
        )
    rows.append(
        {
            "validation_row_id": "VALRUN4532_OVERALL",
            "input_id": "all",
            "numeric_value_detected": False,
            "source_path_exists": True,
            "source_backed_candidate": False,
            "usable_now": False,
            "claim_ready": usable > 0,
            "status": "NO_CLAIM_GRADE_EIGENMODE_INPUTS" if usable == 0 else "CLAIM_INPUTS_PRESENT",
            "reason": "partial proxy/candidate rows exist, but no complete source-backed h_i,m_i,K_i,Q_iS,Q_iT,alpha_bound set exists",
        }
    )
    return rows


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG4532_0_functor_theorem",
            "gate": "parent matter functor sufficient theorem",
            "status": "PASS_FORMAL",
            "detail": "one clean theorem now states exactly what signs J_A=0.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4532_1_no_source_weight_application",
            "gate": "apply no-preaction-weight grammar to current MTS",
            "status": "BLOCKED_UNSIGNED",
            "detail": "object-language/action-measure owner remains unsigned; pre-action w_A countermodel remains legal.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4532_2_real_eigenmode_inputs",
            "gate": "find complete source-backed eigenmode input set",
            "status": "BLOCKED_PARTIAL_NONCLAIM_INPUTS_ONLY",
            "detail": "symbolic K_i, proxy bounds and reviewed R10 curve exist; h_i/m_i²/source/test charges remain missing.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4532_3_runner_claim",
            "gate": "first eigenmode local-bound runner can claim",
            "status": "BLOCKED",
            "detail": "validator finds no claim-grade complete row.",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4532_0",
            "decision": DECISION,
            "meaning": "The derivation route is now exact enough to be useful: parent matter functor plus no active source-weight grammar would close J_A=0. The empirical route also has real partial ingredients, but no complete source-backed first eigenmode input set exists yet.",
            "next_action": NEXT_TARGET,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "try action-measure/object-language owner proof for no w_A; if it does not sign, build the first real source pack for Z_R/M_R²/K_i/Q_iS/Q_iT/alpha_bound",
            "why": "This is the exact remaining fork: theorem-zero via grammar, or real finite input pack for testing.",
            "valid_for_claim": False,
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    functor: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    validator: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    source_failures = [row["source_id"] for row in sources if not row["path_exists"] or not row["needle_found"]]
    checks.append(
        {
            "validation_id": "VAL4532_00_sources",
            "status": "PASS" if not source_failures else "FAIL",
            "detail": "all source paths exist and needles found" if not source_failures else ";".join(source_failures),
        }
    )
    functor_ids = {row["signature_id"] for row in functor}
    checks.append(
        {
            "validation_id": "VAL4532_01_functor",
            "status": "PASS" if {"PMF4532_0_parent_functor", "PMF4532_1_single_measure_owner", "PMF4532_4_exact_J_zero"} <= functor_ids else "FAIL",
            "detail": "parent functor, single-measure owner and exact J-zero clauses present",
        }
    )
    acquisition_ids = {row["input_id"] for row in acquisition}
    needed = {"ACQ4532_0_h_i_or_ZR", "ACQ4532_1_m_i2_or_MR2", "ACQ4532_2_K_i_projection", "ACQ4532_4_alpha_bound_R10"}
    checks.append(
        {
            "validation_id": "VAL4532_02_acquisition",
            "status": "PASS" if needed <= acquisition_ids else "FAIL",
            "detail": "eigenmode acquisition matrix covers h/m/K and bound inputs",
        }
    )
    overall_validator = next((row for row in validator if row["validation_row_id"] == "VALRUN4532_OVERALL"), {})
    checks.append(
        {
            "validation_id": "VAL4532_03_validator",
            "status": "PASS" if overall_validator.get("status") == "NO_CLAIM_GRADE_EIGENMODE_INPUTS" else "FAIL",
            "detail": "validator correctly rejects partial/nonclaim inputs",
        }
    )
    checks.append(
        {
            "validation_id": "VAL4532_04_claims_blocked",
            "status": "PASS" if all(row["valid_for_claim"] is False for row in gates) else "FAIL",
            "detail": "all claim gates remain blocked",
        }
    )
    csv_files = [SOURCE_REGISTER, FUNCTOR_CSV, ACQUISITION_CSV, RUNNER_CSV, GATES_CSV, DECISION_CSV, NEXT_CSV]
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
            "validation_id": "VAL4532_05_csv_parse",
            "status": "PASS" if not parse_failures else "FAIL",
            "detail": "all generated CSV files parse and have rows" if not parse_failures else ";".join(parse_failures),
        }
    )
    checks.append(
        {
            "validation_id": "VAL4532_06_pycache_absent",
            "status": "PASS" if not (SCRIPT_DIR / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after cleanup",
        }
    )
    overall = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "validation_id": "VAL4532_OVERALL",
            "status": overall,
            "detail": "4532 parent matter functor signature and real eigenmode input acquisition matrix" if overall == "PASS" else "4532 validation failed",
        }
    )
    return checks


def build_doc(
    sources: list[dict[str, Any]],
    functor: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    validator: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> str:
    return f"""# 4532 — Parent Matter Functor Signature Or Real Eigenmode Input Acquisition

Marker: `{MARKER}`  
Packet marker: `{PACKET_MARKER}`  
Decision: `{DECISION}`  
Generated: `{now()}`

## What Moved

- The exact route is now reduced to one sharp parent signature: ordinary matter must be a functor of the observed coframe/connection and universal constants, with one action measure and no active species/source multiplier.
- That theorem would close `J_A=0` cleanly, but current sources still do not parent-sign the object-language/action-measure owner that forbids `w_A S_A`.
- The empirical route is no longer empty: the corpus has symbolic `K_i` projections, proxy PPN/WEP diagnostics, and an external R10 candidate curve, but it does **not** have a complete claim-grade first eigenmode input set.
- The validator therefore rejects the live eigenmode route while preserving the partial rows as acquisition targets.

## Parent Matter Functor Signature

{md_table(functor)}

## Real Eigenmode Input Acquisition Matrix

{md_table(acquisition)}

## Eigenmode Input Validator Results

{md_table(validator)}

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
        "domain": "local_gr_newton_r2fr_matter_functor_eigenmode_acquisition",
        "claim": "4532 sharpens the parent matter-functor/no-source-weight signature and audits real first-eigenmode input availability.",
        "current_evidence": "Generated parent matter functor signature, eigenmode acquisition matrix, validator results, claim gates and validation P8_Y5_BRR545_4532_VALIDATION.csv.",
        "status": "conditional_internal_nonclaim_partial_inputs_found_no_complete_row",
        "next_test": NEXT_TARGET,
        "key_risk": "Partial symbolic K_i/proxy bounds/reviewed curves are not complete source-backed h_i,m_i,K_i,Q_iS,Q_iT,alpha_bound rows.",
        "sector": "local_gr_newton",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Promoting a sufficient matter-functor theorem or partial proxy inputs into local-GR/Newton/R10 evidence.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    functor = functor_rows()
    acquisition = acquisition_rows()
    validator = validator_rows(acquisition)
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(FUNCTOR_CSV, functor)
    write_csv(ACQUISITION_CSV, acquisition)
    write_csv(RUNNER_CSV, validator)
    write_csv(GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, functor, acquisition, validator, gates)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, functor, acquisition, validator, gates, decisions, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4532 Parent Matter Functor Signature Or Real Eigenmode Input Acquisition

Marker: `{MARKER}`  
The local-GR source-current route is now pinned to one sharp parent signature: matter must factor through `e_obs(q(Phi))`, `omega[e_obs]`, gauge data and universal constants, with one parent action measure and no active species/source multiplier. The finite route finds partial ingredients — symbolic `K_i`, proxy PPN/WEP diagnostics and reviewed R10 curve plumbing — but no complete source-backed first eigenmode row. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4532 Packet Integration

Marker: `{PACKET_MARKER}`  
The PPC4161 packet now has the matter-functor/no-source-weight theorem target and a real input acquisition matrix for the first finite eigenmode. No local-GR/Newton/R10 claim is promoted.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
