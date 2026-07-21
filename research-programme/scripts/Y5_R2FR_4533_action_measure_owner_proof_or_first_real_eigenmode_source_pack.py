from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4533"
CLAIM_ID = "L-375"
MARKER = "PPC4161_ACTION_MEASURE_OWNER_PROOF_OR_FIRST_REAL_EIGENMODE_SOURCE_PACK_4533"
PACKET_MARKER = "PPC4161_PACKET_ACTION_MEASURE_OWNER_PROOF_OR_FIRST_REAL_EIGENMODE_SOURCE_PACK_4533"
DECISION = "ACTION_MEASURE_OWNER_PROOF_REDUCED_TO_CONSTRUCTOR_EXHAUSTION_AND_FIRST_EIGENMODE_SOURCE_PACK_STAGED"
NEXT_TARGET = "4534-Y5-R2FR-constructor-exhaustion-from-MTS-primitives-or-source-pack-value-fill.md"

FORMAL_PATH = FORMAL / "549-PPC4161-action-measure-owner-proof-or-first-real-eigenmode-source-pack.md"
DOC_PATH = POST / "4533-Y5-R2FR-action-measure-owner-proof-or-first-real-eigenmode-source-pack.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4533_SOURCE_REGISTER.csv"
ACTION_MEASURE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4533_ACTION_MEASURE_OWNER_THEOREM_ATTEMPT.csv"
COUNTERMODEL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4533_SOURCE_WEIGHT_COUNTERMODEL_RESOLUTION.csv"
SOURCE_PACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4533_FIRST_REAL_EIGENMODE_SOURCE_PACK.csv"
PACK_VALIDATOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4533_SOURCE_PACK_VALIDATOR_RESULTS.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4533_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4533_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4533_NEXT_TARGET.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4533_VALIDATION.csv"

DOC_4532 = POST / "4532-Y5-R2FR-parent-matter-functor-signature-or-real-eigenmode-input-acquisition.md"
VALIDATION_4532 = SOURCE_DIR / "P8_Y5_BRR545_4532_VALIDATION.csv"
FUNCTOR_4532 = SOURCE_DIR / "P8_Y5_R2FR_4532_PARENT_MATTER_FUNCTOR_SIGNATURE.csv"
ACQ_4532 = SOURCE_DIR / "P8_Y5_R2FR_4532_REAL_EIGENMODE_INPUT_ACQUISITION_MATRIX.csv"
NO_SPECIES_CONTRACT = SOURCE_DIR / "P8_no_species_source_charge_CONTRACT.csv"
GATE_2508 = SOURCE_DIR / "P8_Y5_NO_SHADOW_2508_NO_SOURCE_SLOT_THEOREM_GATES.csv"
AUDIT_2509 = SOURCE_DIR / "P8_Y5_NO_SHADOW_2509_PARENT_CONSTRUCTOR_EXHAUSTION_AUDIT.csv"
ACTION_2526 = SOURCE_DIR / "P8_Y5_NO_SHADOW_2526_MINIMAL_COUPLING_ACTION_CANDIDATE.csv"
SIGN_2526 = SOURCE_DIR / "P8_Y5_NO_SHADOW_2526_ACTION_SIGNING_TESTS.csv"
CONTRACT_2587 = SOURCE_DIR / "P8_Y5_MIN_PARENT_MATTER_2587_ACTION_CONTRACT.csv"
NDV_2612 = SOURCE_DIR / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_NO_DIRECT_MATTER_X_VERTEX_GRAMMAR_ATTEMPT.csv"
HOM_2612 = SOURCE_DIR / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_NO_SOURCE_ONLY_HOM_AUDIT.csv"
SP_2612 = SOURCE_DIR / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_SOURCE_PREFACTOR_CLASSIFICATION.csv"
SZ_2612 = SOURCE_DIR / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_SOURCE_ZERO_STATUS.csv"
SF_2613 = SOURCE_DIR / "P8_Y5_HOM_EXCLUSION_GATE_2613_LABEL_FORGETTING_SOURCE_FUNCTOR_AUDIT.csv"
NSP_2645 = SOURCE_DIR / "P8_Y5_NO_SOURCE_PREFACTOR_2645_PARENT_ACTION_CLAUSE_ATTEMPT.csv"
DWS_2646 = SOURCE_DIR / "P8_Y5_MATTER_NORMALIZATION_OWNER_2646_DELTAW_SPECIES_COEFFICIENT_ROWS_NONCLAIM.csv"
REQ_1573 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1573_TAU_R10_REQUIRED_INPUTS.csv"
EXT_1579 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1579_EXTERNAL_BOUND_AUDIT.csv"
KI_3897 = SOURCE_DIR / "P8_Y5_R2FR_3897_MEMORY_KI_PROJECTION_DERIVATION.csv"
BOUND_3099 = SOURCE_DIR / "P8_Y5_R2FR_3099_CG_NORMALIZED_BOUND_ROW.csv"
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
    body = ["| " + " | ".join(str(row.get(field, "")).replace("\n", "<br>") for field in fields) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4533_00_doc4532", "4532 handoff", DOC_4532, "4533-Y5-R2FR-action-measure-owner-proof-or-first-real-eigenmode-source-pack.md", "immediate target"),
        ("SRC4533_01_val4532", "4532 validation", VALIDATION_4532, "VAL4532_OVERALL", "prior step validated"),
        ("SRC4533_02_functor4532", "4532 matter functor signature", FUNCTOR_4532, "PMF4532_1_single_measure_owner", "single-measure proof target"),
        ("SRC4533_03_acq4532", "4532 eigenmode acquisition matrix", ACQ_4532, "ACQ4532_0_h_i_or_ZR", "source pack inputs"),
        ("SRC4533_04_no_species", "no species source charge contract", NO_SPECIES_CONTRACT, "S1_matter_factorization", "matter factorization contract"),
        ("SRC4533_05_gate2508", "2508 no source slot gates", GATE_2508, "GATE2508_1_nohom", "no-Hom gate"),
        ("SRC4533_06_audit2509", "2509 constructor exhaustion audit", AUDIT_2509, "CEA2509_3_membership", "constructor membership gap"),
        ("SRC4533_07_action2526", "2526 minimal coupling candidate", ACTION_2526, "MCA2526_3_no_source_only_slot", "candidate matter syntax"),
        ("SRC4533_08_sign2526", "2526 action signing tests", SIGN_2526, "AST2526_5_no_source_slot", "candidate not parent signed"),
        ("SRC4533_09_contract2587", "2587 minimal parent matter contract", CONTRACT_2587, "MCA2587_7_current_verdict", "current adoption status"),
        ("SRC4533_10_ndv2612", "2612 no direct matter vertex grammar", NDV_2612, "NDV2612_3_relative_countermodel", "relative weight countermodel"),
        ("SRC4533_11_hom2612", "2612 no source-only Hom audit", HOM_2612, "HOM2612_4_verdict", "Hom exclusion failed"),
        ("SRC4533_12_sp2612", "2612 source prefactor classification", SP_2612, "SP2612_2_relative_species", "relative species class"),
        ("SRC4533_13_sz2612", "2612 source zero status", SZ_2612, "SZ2612_1_delta_w", "delta_w retained"),
        ("SRC4533_14_sf2613", "2613 label forgetting source functor", SF_2613, "SF2613_4_verdict", "source functor unsigned"),
        ("SRC4533_15_nsp2645", "2645 no-source-prefactor attempt", NSP_2645, "NSP2645_7_verdict", "no-prefactor not derived"),
        ("SRC4533_16_dws2646", "2646 delta-w coefficient rows", DWS_2646, "DWS2646_0_delta_w_species", "finite coefficient fallback"),
        ("SRC4533_17_req1573", "1573 R10 required inputs", REQ_1573, "REQ1573_0_ZR", "ZR/MR2 charge inputs"),
        ("SRC4533_18_ext1579", "1579 external bound audit", EXT_1579, "EXT1579_0_R10", "R10 curve nonclaim"),
        ("SRC4533_19_ki3897", "3897 K_i map", KI_3897, "KI3897_5_R10", "symbolic projection"),
        ("SRC4533_20_bound3099", "3099 PPN proxy", BOUND_3099, "NGB3099_0_alpha_proxy_input", "diagnostic bound"),
        ("SRC4533_21_proxy3308", "3308 WEP unit proxy", PROXY_3308, "UP3308_LC3308_scalar_WEP3306_0_MICROSCOPE_Ti_Pt", "diagnostic WEP proxy"),
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


def action_measure_rows() -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "AMO4533_0_target",
            "claim_piece": "action-measure owner theorem",
            "mathematical_statement": "Allowed[S_matter] has one parent measure/action scale and no constructor Hom(SpeciesLabel, Coeff_active_source), except a single universal calibration mode.",
            "proof_move": "If Coeff_active_source is exhausted by ParentGenerate[q(Phi), theta_rep, universal constants, retained residuals], a species-indexed w_A cannot be formed.",
            "result_if_signed": "relative pre-action source weights are untypeable, so partial S_matter/partial w_A is not a live channel.",
            "current_status": "EXACT_PROOF_TARGET_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "proof_id": "AMO4533_1_common_mode",
            "claim_piece": "universal common action factor",
            "mathematical_statement": "S_matter -> w_star S_matter is one universal mode, absorbed into kappa/G calibration after fixing measured G.",
            "proof_move": "Separate common-mode calibration from relative species/source weights using a projector P_perp.",
            "result_if_signed": "common mode is not a WEP/R10/local-force residual by itself.",
            "current_status": "CONDITIONAL_COMMON_MODE_ONLY",
            "valid_for_claim": False,
        },
        {
            "proof_id": "AMO4533_2_ward_insufficiency",
            "claim_piece": "Ward/current ownership is not enough",
            "mathematical_statement": "S_matter=sum_A w_A S_A is covariant, additive, and Ward-compatible while T_source=sum_A w_A T_A.",
            "proof_move": "A Ward identity conserves whichever source the action selected; it does not select the species-blind action.",
            "result_if_signed": "prevents false proof by conservation identity.",
            "current_status": "COUNTERMODEL_CONFIRMED",
            "valid_for_claim": False,
        },
        {
            "proof_id": "AMO4533_3_constructor_exhaustion",
            "claim_piece": "parent constructor exhaustion",
            "mathematical_statement": "Every coefficient reaching source, clocks, masses, WEP, R10, PPN and readout lies in Image(ParentGenerate).",
            "proof_move": "Prove source coefficients cannot be appended as independent primitive extensions, markers, boundary classes, domains, or readout labels.",
            "result_if_signed": "no hidden return route for w_A, kappa_A, source masks, shadow frames or direct alpha/mass vertices.",
            "current_status": "CORE_GAP_NOT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "proof_id": "AMO4533_4_minimal_candidate",
            "claim_piece": "minimal parent matter action candidate",
            "mathematical_statement": "S_parent=S_geom[Phi]+sum_A S_A[psi_A;q(Phi),theta_A]+S_boundary[q(Phi)]",
            "proof_move": "This candidate signs the desired clauses only if adopted as unique parent grammar from MTS primitives.",
            "result_if_signed": "matter descent and no source slot would follow by construction.",
            "current_status": "CANDIDATE_CONTRACT_NOT_UNIQUENESS_PROOF",
            "valid_for_claim": False,
        },
        {
            "proof_id": "AMO4533_5_verdict",
            "claim_piece": "action-measure owner proof verdict",
            "mathematical_statement": "AMO4533_0 through AMO4533_4 would kill w_A only after constructor exhaustion and action-scale owner are derived.",
            "proof_move": "Do not promote an ansatz; keep delta_w/eigenmode source-pack fallback active.",
            "result_if_signed": "J_A source-current zero route can progress toward exact local GR.",
            "current_status": "PROOF_REDUCED_TO_CONSTRUCTOR_EXHAUSTION_NO_CLAIM",
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "CEX4533_0_relative_species_weight",
            "countermodel": "S_matter=sum_A w_A S_A with w_A=w_star(1+epsilon_A)",
            "survives": "covariance, additivity, Hilbert variation and Ward conservation",
            "killed_only_by": "typed parent object-language/action-measure theorem making w_A unformable",
            "finite_fallback": "epsilon_A / Delta_w_species coefficient vector",
            "current_status": "LIVE_COUNTERMODEL_RETAINED",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CEX4533_1_hidden_marker_weight",
            "countermodel": "w_A=w(I_hidden, material marker, domain, boundary class, readout selector)",
            "survives": "ordinary visible matter equations if marker is hidden from matter readout",
            "killed_only_by": "no hidden/marker/domain/boundary/readout Hom into source coefficient",
            "finite_fallback": "marker/domain/readout source coefficient row",
            "current_status": "LIVE_COUNTERMODEL_RETAINED",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CEX4533_2_shadow_frame",
            "countermodel": "g_A=A_A(X)^2 g_obs or disformal species/source frame before variation",
            "survives": "can be WEP-safe in narrow limits but still affect clocks, PPN, R10 or source normalization",
            "killed_only_by": "minimal observed-stack uniqueness and no shadow-frame constructor theorem",
            "finite_fallback": "c_g/disformal/clock-source coefficient row",
            "current_status": "LIVE_UNLESS_PARENT_FORBIDS",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CEX4533_3_direct_alpha_mass_vertex",
            "countermodel": "alpha_EM(X)F^2, m_A(X), q_A X_mu J_A^mu, or theta_A(I_Q,m)",
            "survives": "unless constants are superselected and no direct matter-X vertex is parent-signed",
            "killed_only_by": "constant-sector superselection plus no direct matter vertex grammar",
            "finite_fallback": "alpha/mass/charge coefficient rows",
            "current_status": "POLICY_FORBIDDEN_NOT_PARENT_THEOREM",
            "valid_for_claim": False,
        },
    ]


def source_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "pack_id": "SP4533_0_ZR",
            "quantity": "h_i / Z_R",
            "current_value": "MISSING_ZR",
            "source_path": str(REQ_1573),
            "status": "REQUIRED_INPUT_MISSING",
            "units": "kinetic normalization with same-frame parent units",
            "acceptance": "positive numeric value or parent-signed no-pole/operator-exclusion theorem",
            "valid_for_claim": False,
        },
        {
            "pack_id": "SP4533_1_MR2",
            "quantity": "m_i^2 / M_R^2",
            "current_value": "MISSING_MR2",
            "source_path": str(REQ_1573),
            "status": "REQUIRED_INPUT_MISSING",
            "units": "mass^2 / range denominator",
            "acceptance": "positive numeric mass-gap/range value or exact constraint/no-pole theorem",
            "valid_for_claim": False,
        },
        {
            "pack_id": "SP4533_2_Ki",
            "quantity": "K_i projection",
            "current_value": "symbolic K_gamma/K_Gdot/K_R10; candidate alpha3/alpha2/xi zeros",
            "source_path": str(KI_3897),
            "status": "SYMBOLIC_PROJECTION_ONLY",
            "units": "arena-specific",
            "acceptance": "numeric readout coefficient or parent-signed symmetry zero for selected first mode",
            "valid_for_claim": False,
        },
        {
            "pack_id": "SP4533_3_Q_source_test",
            "quantity": "Q_iS,Q_iT or beta_S,beta_T",
            "current_value": "MISSING_SOURCE_CHARGE; MISSING_TEST_CHARGE",
            "source_path": str(REQ_1573),
            "status": "REQUIRED_INPUT_MISSING",
            "units": "source/test charge normalization",
            "acceptance": "parent matter-descent zero or source-backed material/source response rows",
            "valid_for_claim": False,
        },
        {
            "pack_id": "SP4533_4_R10_bound_curve",
            "quantity": "alpha_bound(lambda)",
            "current_value": "390 reviewed candidate rows",
            "source_path": str(EXT_1579),
            "status": "EXTERNAL_REVIEW_CANDIDATE_NONCLAIM",
            "units": "dimensionless alpha(lambda)",
            "acceptance": "manual/official QA acceptance and internal lambda_i/alpha_i row",
            "valid_for_claim": False,
        },
        {
            "pack_id": "SP4533_5_delta_w_species",
            "quantity": "epsilon_A / Delta_w_species",
            "current_value": "SYMBOLIC_FREE_COEFFICIENT_NO_PARENT_VALUE",
            "source_path": str(DWS_2646),
            "status": "FINITE_FALLBACK_SYMBOLIC",
            "units": "dimensionless relative source/action normalization",
            "acceptance": "parent theorem-zero or numeric/material source vector with no-cancellation norm",
            "valid_for_claim": False,
        },
        {
            "pack_id": "SP4533_6_PPN_proxy",
            "quantity": "alpha_PPN_proxy",
            "current_value": "0.00578801540146505096",
            "source_path": str(BOUND_3099),
            "status": "SOURCE_BACKED_PROXY_NONCLAIM",
            "units": "dimensionless",
            "acceptance": "not a first eigenmode input until Z_X, tau_PPN, S_PPN and range transfer are source-backed",
            "valid_for_claim": False,
        },
        {
            "pack_id": "SP4533_7_WEP_unit_proxy",
            "quantity": "unit mode-factor WEP sensitivity",
            "current_value": "1.0345834325e-15 first MICROSCOPE proxy",
            "source_path": str(PROXY_3308),
            "status": "DIAGNOSTIC_PROXY_NONCLAIM",
            "units": "dimensionless",
            "acceptance": "requires real K_i(lambda), exact material/source vectors and confidence handling",
            "valid_for_claim": False,
        },
    ]


def validator_rows(source_pack: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    accepted = 0
    for row in source_pack:
        status = str(row["status"])
        value = str(row["current_value"])
        source_exists = Path(row["source_path"]).exists()
        numeric_like = any(char.isdigit() for char in value) and "MISSING" not in value and "SYMBOLIC" not in value
        claim_ready = bool(row["valid_for_claim"] and source_exists and numeric_like and "NONCLAIM" not in status and "MISSING" not in status)
        accepted += int(claim_ready)
        rows.append(
            {
                "validator_id": f"SPV4533_{row['pack_id']}",
                "pack_id": row["pack_id"],
                "source_exists": source_exists,
                "numeric_like": numeric_like,
                "status": "ACCEPT_CLAIM_INPUT" if claim_ready else "REJECT_MISSING_SYMBOLIC_OR_NONCLAIM",
                "claim_ready": claim_ready,
                "reason": row["status"],
            }
        )
    rows.append(
        {
            "validator_id": "SPV4533_OVERALL",
            "pack_id": "all",
            "source_exists": True,
            "numeric_like": False,
            "status": "NO_CLAIM_GRADE_SOURCE_PACK",
            "claim_ready": accepted > 0,
            "reason": "source pack has useful partial/proxy rows but no complete claim-grade eigenmode input set",
        }
    )
    return rows


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG4533_0_action_measure_proof",
            "gate": "action-measure/no-Hom theorem target",
            "status": "PASS_EXACT_TARGET",
            "detail": "proof obligation is reduced to constructor exhaustion plus single action-scale owner.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4533_1_current_application",
            "gate": "apply no w_A theorem to current MTS",
            "status": "BLOCKED_CONSTRUCTOR_EXHAUSTION_UNSIGNED",
            "detail": "2508/2509/2612/2645 all keep no-source-prefactor theorem unsigned.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4533_2_source_pack",
            "gate": "first real eigenmode source pack",
            "status": "PASS_STAGED_NONCLAIM",
            "detail": "pack rows for ZR, MR2, Ki, source/test charge, R10 curve and delta_w fallback are explicit.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4533_3_claim",
            "gate": "local GR/Newton/R10 claim",
            "status": "BLOCKED",
            "detail": "neither constructor exhaustion nor complete numeric eigenmode source pack exists.",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4533_0",
            "decision": DECISION,
            "meaning": "This is the real fork: the proof route needs constructor exhaustion from MTS primitives, not another Ward/covariance argument; the finite route has a concrete source pack but no claim-grade complete row yet.",
            "next_action": NEXT_TARGET,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "try constructor exhaustion from MTS primitives first; if it cannot sign, fill the source-pack values in SP4533_0..7",
            "why": "This avoids another loop: either make w_A untypeable, or put real numbers/accepted curves into the finite runner.",
            "valid_for_claim": False,
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    proof: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    source_pack: list[dict[str, Any]],
    validators: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    source_failures = [row["source_id"] for row in sources if not row["path_exists"] or not row["needle_found"]]
    checks.append(
        {
            "validation_id": "VAL4533_00_sources",
            "status": "PASS" if not source_failures else "FAIL",
            "detail": "all source paths exist and needles found" if not source_failures else ";".join(source_failures),
        }
    )
    proof_ids = {row["proof_id"] for row in proof}
    checks.append(
        {
            "validation_id": "VAL4533_01_proof",
            "status": "PASS" if {"AMO4533_0_target", "AMO4533_2_ward_insufficiency", "AMO4533_5_verdict"} <= proof_ids else "FAIL",
            "detail": "action-measure theorem target, Ward insufficiency and verdict rows present",
        }
    )
    cex_ids = {row["countermodel_id"] for row in countermodels}
    checks.append(
        {
            "validation_id": "VAL4533_02_countermodels",
            "status": "PASS" if {"CEX4533_0_relative_species_weight", "CEX4533_1_hidden_marker_weight"} <= cex_ids else "FAIL",
            "detail": "live source-weight countermodels retained",
        }
    )
    pack_ids = {row["pack_id"] for row in source_pack}
    required_pack = {"SP4533_0_ZR", "SP4533_1_MR2", "SP4533_2_Ki", "SP4533_3_Q_source_test", "SP4533_4_R10_bound_curve"}
    checks.append(
        {
            "validation_id": "VAL4533_03_source_pack",
            "status": "PASS" if required_pack <= pack_ids else "FAIL",
            "detail": "first eigenmode source pack covers ZR/MR2/Ki/Q/bound inputs",
        }
    )
    overall_validator = next((row for row in validators if row["validator_id"] == "SPV4533_OVERALL"), {})
    checks.append(
        {
            "validation_id": "VAL4533_04_validator",
            "status": "PASS" if overall_validator.get("status") == "NO_CLAIM_GRADE_SOURCE_PACK" else "FAIL",
            "detail": "source pack validator rejects partial/nonclaim rows",
        }
    )
    checks.append(
        {
            "validation_id": "VAL4533_05_claims_blocked",
            "status": "PASS" if all(row["valid_for_claim"] is False for row in gates) else "FAIL",
            "detail": "all claim gates remain blocked",
        }
    )
    csv_files = [
        SOURCE_REGISTER,
        ACTION_MEASURE_CSV,
        COUNTERMODEL_CSV,
        SOURCE_PACK_CSV,
        PACK_VALIDATOR_CSV,
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
            "validation_id": "VAL4533_06_csv_parse",
            "status": "PASS" if not parse_failures else "FAIL",
            "detail": "all generated CSV files parse and have rows" if not parse_failures else ";".join(parse_failures),
        }
    )
    checks.append(
        {
            "validation_id": "VAL4533_07_pycache_absent",
            "status": "PASS" if not (SCRIPT_DIR / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after cleanup",
        }
    )
    overall = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "validation_id": "VAL4533_OVERALL",
            "status": overall,
            "detail": "4533 action-measure owner proof attempt and first real eigenmode source pack" if overall == "PASS" else "4533 validation failed",
        }
    )
    return checks


def build_doc(
    sources: list[dict[str, Any]],
    proof: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    source_pack: list[dict[str, Any]],
    validators: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> str:
    return f"""# 4533 — Action Measure Owner Proof Or First Real Eigenmode Source Pack

Marker: `{MARKER}`  
Packet marker: `{PACKET_MARKER}`  
Decision: `{DECISION}`  
Generated: `{now()}`

## What Moved

- The no-`w_A` route is now as sharp as it can be without cheating: it needs constructor exhaustion from MTS primitives plus one parent action-scale/measure owner.
- Ward identities, covariance, additivity, Hilbert-current ownership and common `G` calibration are explicitly insufficient against `S_matter=sum_A w_A S_A`.
- The source-pack fallback is no longer abstract: it lists the actual finite inputs needed for the first eigenmode runner and maps each to the best current local source.
- Current result stays private/nonclaim: useful partials exist, but no complete claim-grade eigenmode source pack exists.

## Action-Measure Owner Theorem Attempt

{md_table(proof)}

## Source-Weight Countermodel Resolution

{md_table(countermodels)}

## First Real Eigenmode Source Pack

{md_table(source_pack)}

## Source Pack Validator

{md_table(validators)}

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
        "domain": "local_gr_newton_r2fr_action_measure_source_pack",
        "claim": "4533 reduces the no-source-weight proof to constructor exhaustion/action-measure ownership and stages the first real eigenmode source pack.",
        "current_evidence": "Generated action-measure owner theorem attempt, source-weight countermodel resolution, first eigenmode source pack, validator results, claim gates and validation P8_Y5_BRR545_4533_VALIDATION.csv.",
        "status": "conditional_internal_nonclaim_constructor_exhaustion_required_source_pack_staged",
        "next_test": NEXT_TARGET,
        "key_risk": "Constructor exhaustion is not derived, and the source pack contains partial/proxy/nonclaim rows rather than a complete claim-grade eigenmode.",
        "sector": "local_gr_newton",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Using Ward/covariance/common calibration as if it made w_A untypeable, or treating source-pack proxy rows as empirical evidence.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    proof = action_measure_rows()
    countermodels = countermodel_rows()
    source_pack = source_pack_rows()
    validators = validator_rows(source_pack)
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ACTION_MEASURE_CSV, proof)
    write_csv(COUNTERMODEL_CSV, countermodels)
    write_csv(SOURCE_PACK_CSV, source_pack)
    write_csv(PACK_VALIDATOR_CSV, validators)
    write_csv(GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, proof, countermodels, source_pack, validators, gates)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, proof, countermodels, source_pack, validators, gates, decisions, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4533 Action Measure Owner Proof Or First Real Eigenmode Source Pack

Marker: `{MARKER}`  
The source-current/local-GR route now has a precise proof obligation: constructor exhaustion from MTS primitives plus one action-scale/measure owner must make `w_A` untypeable. Ward/covariance/common-calibration routes are explicitly insufficient. The finite fallback is staged as the first eigenmode source pack: `Z_R`, `M_R^2`, `K_i`, source/test charges, R10 bound curve, `delta_w`, PPN proxy and WEP proxy. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4533 Packet Integration

Marker: `{PACKET_MARKER}`  
The PPC4161 packet now has the action-measure constructor-exhaustion target and a concrete first eigenmode source pack. No local-GR/Newton/R10 claim is promoted.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
