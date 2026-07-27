from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4713"
CLAIM_ID = "L-555"
MARKER = "PPC4161_NO_LINEAR_EM_OWNER_EVEN_RESIDUAL_OR_LLINEAR_BOUND_4713"
PACKET_MARKER = "PPC4161_PACKET_NO_LINEAR_EM_OWNER_EVEN_RESIDUAL_OR_LLINEAR_BOUND_4713"
DECISION = "NO_LINEAR_EM_OWNER_EXACT_CONDITIONAL_THEOREM_DERIVED_LLINEAR_BOUND_RETAINED_NONCLAIM"
NEXT_TARGET = "4714-Y5-R2FR-EM-stress-Poynting-current-owner-or-sidechannel-bound.md"

DOC_PATH = POST / "4713-Y5-R2FR-no-linear-EM-owner-even-residual-symmetry-or-Llinear-bound.md"
FORMAL_PATH = FORMAL / "729-PPC4161-no-linear-EM-owner-even-residual-symmetry-or-Llinear-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

CSV_4712_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4712_NEXT_TARGET.csv"
CSV_4712_PACK = SOURCE_DIR / "P8_Y5_R2FR_4712_ROOT_COHERCIVITY_SOURCE_PACK.csv"
CSV_4712_GAP = SOURCE_DIR / "P8_Y5_R2FR_4712_COKERNEL_SPLIT_AND_GAP_THEOREM.csv"
CSV_4712_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4712_VALIDATION.csv"
CSV_4711_ROOT = SOURCE_DIR / "P8_Y5_R2FR_4711_ROOT_NORMAL_EQUATION_CERTIFICATE.csv"
CSV_4711_INPUTS = SOURCE_DIR / "P8_Y5_R2FR_4711_FINITE_ROOT_CLOCK_INPUT_ROWS.csv"
CSV_4710_CERT = SOURCE_DIR / "P8_Y5_R2FR_4710_TAU_ZERO_OR_EXACT_ROOT_BYPASS_CERTIFICATE.csv"
CSV_3222_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_3222_PARENT_ACTION_DEFECT_NORM_CONTRACT.csv"
CSV_3222_VARIATION = SOURCE_DIR / "P8_Y5_R2FR_3222_VARIATION_AND_MAXWELL_LIMIT_PROOF.csv"
CSV_3222_GUARDS = SOURCE_DIR / "P8_Y5_R2FR_3222_STRESS_POYNTING_AND_READOUT_GUARDS.csv"
CSV_3221_DEFECT = SOURCE_DIR / "P8_Y5_R2FR_3221_DEFECT_NORM_SOURCE_ROOT_THEOREM.csv"
CSV_609_NOLIN = SOURCE_DIR / "P8_Y5_R10_609_NO_LINEAR_MARKER_SYMMETRY_GATE.csv"
CSV_4704_VISIBLE = SOURCE_DIR / "P8_Y5_R2FR_4704_VISIBLE_IMAGE_PROOF_ATTEMPT.csv"
CSV_4707_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4707_EXACT_ZERO_CONTRACT_ROWS.csv"
CSV_4707_TAIL = SOURCE_DIR / "P8_Y5_R2FR_4707_READOUT_TAIL_BOUND_ROWS.csv"
CSV_4708_RADIOUT = SOURCE_DIR / "P8_Y5_R2FR_4708_RADIOUT_NATURALITY_THEOREM_ROWS.csv"
CSV_4708_TAILS = SOURCE_DIR / "P8_Y5_R2FR_4708_BRAD_BREADOUT_SOURCE_ROWS_NONCLAIM.csv"
CSV_4709_CLOCK = SOURCE_DIR / "P8_Y5_R2FR_4709_CLOCK_TAU_MAP_THEOREM_ROWS.csv"
CSV_1057_UNIQUE = SOURCE_DIR / "P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv"
CSV_1057_DOMAIN = SOURCE_DIR / "P8_Y5_R10_1057_OPERATOR_DOMAIN_AUDIT.csv"
CSV_1057_COUNTER = SOURCE_DIR / "P8_Y5_R10_1057_F2_COUNTERTERM_LEDGER.csv"
CSV_765_MKI = SOURCE_DIR / "P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv"
CSV_765_RESCALE = SOURCE_DIR / "P8_Y5_R10_765_RESCALING_COUNTEREXAMPLE_LEDGER.csv"
CSV_988_EMLOCK = SOURCE_DIR / "P8_Y5_R10_988_EM_LOCK_THEOREM_GATE.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4713_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4713_NO_LINEAR_OWNER_THEOREM_ROWS.csv"
LLINEAR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4713_LLINEAR_BOUND_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4713_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4713_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4713_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4713_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4713_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4713_VALIDATION.csv"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_of(path: Path, needle: str) -> int:
    for index, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def table(rows: Iterable[dict[str, Any]]) -> str:
    rows = list(rows)
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(header, "")).replace("|", "\\|").replace("\n", " ") for header in headers) + " |")
    return "\n".join(output)


def append_once(path: Path, marker: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    path.write_text(existing.rstrip() + "\n\n" + body.strip() + "\n", encoding="utf-8")


def append_claim_once(timestamp: str) -> None:
    existing = text(CLAIMS_PATH)
    if existing.startswith(CLAIM_ID + ",") or f"\n{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_empirical_interface",
        "claim": "4713 derives the exact no-linear/even-residual EM-owner conditions and defines a finite L_linear leak if those conditions are not parent-signed.",
        "current_evidence": "Generated source register, no-linear theorem rows, L_linear bound rows, promotion gates, firewalls, decision, status, next target and validation.",
        "status": "no_linear_em_owner_conditional_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating ordinary U(1)/diffeomorphism covariance as a proof that linear EM kinetic coefficients are forbidden.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "",
        "title": "No-linear EM owner even-residual symmetry or Llinear bound",
        "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    with CLAIMS_PATH.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or list(row)
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writerow({field: row.get(field, "") for field in fields})


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4713_00_4712_next", CSV_4712_NEXT, "NT4712_0", "handoff to no-linear EM owner"),
        ("SRC4713_01_4712_Llinear", CSV_4712_PACK, "RCP4712_9_Llinear", "deferred L_linear source-pack row"),
        ("SRC4713_02_4712_root", CSV_4712_GAP, "CK4712_2_exact_root_criterion", "exact R_Q root criterion"),
        ("SRC4713_03_4712_finite", CSV_4712_GAP, "CK4712_3_finite_root_bound", "finite R_Q fallback"),
        ("SRC4713_04_4712_validation", CSV_4712_VALIDATION, "VAL4712_OVERALL", "4712 validation"),
        ("SRC4713_05_4711_no_linear", CSV_4711_ROOT, "RNC4711_2_no_linear_EM_owner_contract", "sharp no-linear owner contract"),
        ("SRC4713_06_4711_clock", CSV_4711_ROOT, "RNC4711_3_clock_alpha_closure_if_root_signs", "clock alpha closure if root signs"),
        ("SRC4713_07_4711_input", CSV_4711_INPUTS, "FRC4711_4_Llinear", "finite Llinear input row"),
        ("SRC4713_08_4710_bypass", CSV_4710_CERT, "TZC4710_1_exact_root_bypass", "exact-root clock bypass"),
        ("SRC4713_09_3222_action", CSV_3222_CONTRACT, "DNC3222_1_action_term", "defect-norm EM action term"),
        ("SRC4713_10_3222_no_linear", CSV_3222_CONTRACT, "DNC3222_3_no_linear_defect", "no-linear defect contract"),
        ("SRC4713_11_3222_variation_zero", CSV_3222_VARIATION, "VAR3222_0_coefficient_first_variation", "squared residual first variation zero"),
        ("SRC4713_12_3222_counter", CSV_3222_VARIATION, "VAR3222_3_no_linear_defect_counterexample", "linear defect counterexample"),
        ("SRC4713_13_3221_double", CSV_3221_DEFECT, "DN3221_1_first_derivative_zero", "defect-norm double-zero theorem"),
        ("SRC4713_14_3221_verdict", CSV_3221_DEFECT, "DN3221_5_verdict", "defect-norm owner not parent signed"),
        ("SRC4713_15_609_fixed", CSV_609_NOLIN, "NL609_0_fixed_spurion", "fixed linear covector conditional block"),
        ("SRC4713_16_609_material", CSV_609_NOLIN, "NL609_1_material_marker", "material linear marker survives"),
        ("SRC4713_17_609_verdict", CSV_609_NOLIN, "NL609_4_no_linear_verdict", "no-linear verdict finite branch retained"),
        ("SRC4713_18_4704_image", CSV_4704_VISIBLE, "VIP4704_0_exact_image_zero_theorem", "visible image zero theorem"),
        ("SRC4713_19_4704_hom", CSV_4704_VISIBLE, "VIP4704_1_hidden_Hom_kernel_theorem", "hidden-Hom zero theorem"),
        ("SRC4713_20_4704_counter", CSV_4704_VISIBLE, "VIP4704_2_scalar_functional_countermodel", "hidden scalar countermodel"),
        ("SRC4713_21_4704_bound", CSV_4704_VISIBLE, "VIP4704_4_finite_branch_bound_identity", "finite H_XF2 branch"),
        ("SRC4713_22_4707_nohom", CSV_4707_ZERO, "ZERO4707_1_no_extra_F2_subcase", "no-Hom no-extra-F2 subcase"),
        ("SRC4713_23_4707_tail", CSV_4707_TAIL, "TAIL4707_1_F2_Hom_tail", "F2 Hom finite tail"),
        ("SRC4713_24_4708_rad", CSV_4708_RADIOUT, "RRN4708_0_radiative_naturality_zero", "radiative naturality zero"),
        ("SRC4713_25_4708_readout", CSV_4708_RADIOUT, "RRN4708_1_observed_readout_zero", "readout naturality zero"),
        ("SRC4713_26_4708_tails", CSV_4708_TAILS, "TAIL4708_0_Brad", "B_rad finite row"),
        ("SRC4713_27_4709_clock", CSV_4709_CLOCK, "CTM4709_3_clock_Breadout_zero_branch", "clock B_readout zero branch"),
        ("SRC4713_28_1057_unique", CSV_1057_UNIQUE, "UMS1057_2_no_independent_F2", "unique Maxwell subblock blocker"),
        ("SRC4713_29_1057_domain", CSV_1057_DOMAIN, "OD1057_1_U1_gauge", "U(1) allows kinetic coefficient"),
        ("SRC4713_30_1057_counter", CSV_1057_COUNTER, "CT1057_1_hidden_scalar", "hidden scalar F2 counterterm"),
        ("SRC4713_31_765_mki", CSV_765_MKI, "MKI765_2_unique_F2", "Maxwell kinetic inheritance gate"),
        ("SRC4713_32_765_rescale", CSV_765_RESCALE, "RCE765_0_lambda_F2", "independent lambda_F2 counterexample"),
        ("SRC4713_33_988_lock", CSV_988_EMLOCK, "EMLOCK988_1_unique_Maxwell_F2", "EM lock unique F2 blocker"),
        ("SRC4713_34_3222_stress", CSV_3222_GUARDS, "SPG3222_0_null_wave_guard", "Poynting/stress separate guard"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": line > 0,
                "source_line": line,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "NLO4713_0_linearization_normal_form",
            "claim_piece": "linear EM kinetic leakage isolated",
            "formal_statement": "Near a local branch with residual R_Q, write Z_A=Z_bar(q_obs,theta)+ell_Q[R_Q]+lambda_D <R_Q,R_Q>_P+H_hid+B_rad+B_readout+O(||R_Q||^3). At R_Q=0, D_m ln Z_A is controlled by ell_Q[D_m R_Q], hidden-Hom, radiative and readout derivatives.",
            "derivation": "This is the first Taylor jet of the EM kinetic coefficient around the residual root, with quotient-basic and fixed representation pieces killed by Dq_obs[v]=0. The 3222 counterexample shows ell_Q cannot be silently dropped.",
            "result": "The surviving first-order obstruction is a named L_linear coefficient, not a vague coupling problem.",
            "current_status": "EXACT_LOCAL_NORMAL_FORM_DERIVED",
            "missing_for_claim": "parent proof that ell_Q=0 and hidden/radiative/readout coefficient derivatives vanish on the same branch",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "NLO4713_1_even_residual_double_zero",
            "claim_piece": "even residual owner kills first variation",
            "formal_statement": "If the parent EM kinetic owner depends on the local residual only through an even scalar N_R=<R_Q,R_Q>_P, so Z_A=Z_bar(q_obs,theta)+F_even(N_R) with finite F_even'(0), then D_m Z_A|R_Q=0 = 0 for every regular local variation m.",
            "derivation": "D_m Z_A=F_even'(N_R) D_m N_R and D_m N_R=2<R_Q,D_m R_Q>_P. At the root R_Q=0, the derivative vanishes without setting the local clock velocity or test parameter to zero.",
            "result": "ell_Q=0 and the clock exact-root bypass survives on the bare kinetic coefficient.",
            "current_status": "EXACT_CONDITIONAL_THEOREM_PARENT_EVENNESS_UNSIGNED",
            "missing_for_claim": "source-signed parent action or symmetry showing residual orientation/sign is not a physical coefficient argument",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "NLO4713_2_operator_domain_no_hom_route",
            "claim_piece": "operator-domain exhaustion kills hidden linear slots",
            "formal_statement": "If Coeff(F_Q^2) is not an independent parent target object outside the parent Maxwell/defect-norm image, then maps Hom(C_hid,Coeff(F_Q^2)), material covectors and independent lambda_A F_Q^2 terms are ill-typed; the only visible EM coefficient is q-basic plus the even residual norm.",
            "derivation": "4704 and 4707 reduce hidden-Hom and no-extra-F2 to a typed parent image theorem. A nonconstant scalar multiplier requires a target coefficient object; removing that object removes the derivative rather than tuning it.",
            "result": "L_linear=0 follows if the object-language exhaustion and even-residual owner are both parent-signed.",
            "current_status": "EXACT_CONDITIONAL_OPERATOR_DOMAIN_THEOREM_UNSIGNED",
            "missing_for_claim": "derive the allowed visible operator algebra from MTS primitives, including radiative/readout preservation",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "NLO4713_3_symmetry_countermodel",
            "claim_piece": "ordinary covariance is insufficient",
            "formal_statement": "If the parent allows a material covector ell_Q or hidden invariant scalar I_hid with a visible coefficient target, then Delta S=-1/4 int sqrt(-g)(ell_Q[R_Q]+epsilon I_hid)F_Q^2 is diffeomorphism and U(1) gauge invariant and gives D_m Z_A|root generically nonzero.",
            "derivation": "F_Q^2 is a covariant scalar density and hidden/material scalar coefficients are legal unless the stronger parent operator domain forbids them. This is the 609/1057/3222 countermodel in local-root notation.",
            "result": "No public or internal local-GR pass can be based on ordinary gauge symmetry alone.",
            "current_status": "COUNTERMODEL_RETAINED",
            "missing_for_claim": "none; this is a no-cheat firewall",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "NLO4713_4_same_branch_clock_closure",
            "claim_piece": "clock alpha closure if exact root and no-linear owner sign together",
            "formal_statement": "On one branch, if the 4712 exact R_Q root clauses hold, NLO4713_1 or NLO4713_2 gives L_linear=0, and the 4708/4709 clock readout/radiative tails vanish, then D_tau ln alpha_EM=0 without assuming tau_clock_time=0.",
            "derivation": "Substitute R_Q=0 into the 4710 exact-root bypass and substitute L_linear=0 into the 4713 linearized coefficient law. The remaining clock readout tail is killed only by the same-branch 4709 clock theorem.",
            "result": "This is the clean local-clock route: derive root and owner, do not fit tau silence.",
            "current_status": "EXACT_CONDITIONAL_COMPOSITION_NONCLAIM",
            "missing_for_claim": "same-branch parent signatures for R_Q root, no-linear EM owner, radiative/readout naturality and clock readout",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "NLO4713_5_verdict",
            "claim_piece": "no-linear branch status",
            "formal_statement": "The derivation route is now exact: either prove an even-residual/operator-domain owner and set L_linear=0, or carry L_linear as a finite source coefficient. The current corpus does not yet parent-sign the exact zero.",
            "derivation": "Combines the 3221/3222 double-zero theorem, 4704/4707 typed no-Hom route, 609/1057 countermodels and the 4712 root handoff.",
            "result": DECISION,
            "current_status": "DERIVATION_ADVANCED_NONCLAIM",
            "missing_for_claim": "parent-owned evenness/operator-domain signature or source-backed L_linear bound",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def llinear_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "LL4713_0_Llinear_definition",
            "quantity": "L_linear",
            "formula": "L_linear := Z_A,min^-1 sup_{||u||=1} |ell_Q[A_Q u] + D_u H_hid|, with radiative/readout tails kept separately unless the same branch absorbs them into H_hid.",
            "units": "inverse local-branch parameter or declared EM kinetic coefficient derivative units",
            "zero_condition": "even residual owner plus operator-domain no-Hom/no-extra-F2 theorem",
            "needed_source": "parent action/object-language row proving ell_Q=0 and no hidden/material coefficient target, or a numeric derivative bound",
            "status": "FORMULA_DERIVED_VALUE_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "LL4713_1_exact_root_clock_leak_bound",
            "quantity": "clock alpha leak at exact root",
            "formula": "|D_tau ln alpha_EM| <= L_linear |tau_clock_time| + B_rad_clock + B_readout_clock on the exact R_Q=0 branch; if L_linear=B_rad_clock=B_readout_clock=0, the drift vanishes.",
            "units": "time^-1",
            "zero_condition": "L_linear=0 and 4708/4709 radiative/readout clock tails zero on the same branch",
            "needed_source": "standalone tau_clock_time or zero theorem, plus B_rad/B_readout clock map if L_linear is not zero",
            "status": "BOUND_DERIVED_INPUTS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "LL4713_2_finite_nonroot_clock_bound",
            "quantity": "full finite clock residual",
            "formula": "|D_tau ln alpha_EM| <= L_linear |tau_clock_time| + C_D |Delta m tau_clock_time| + E_HO + E_clock_transport + B_rad_clock + B_readout_clock.",
            "units": "time^-1",
            "zero_condition": "all product factors or tails theorem-zero on one branch",
            "needed_source": "L_linear, tau_clock_time, C_D, Delta m, transport prefactor, B_rad_clock and B_readout_clock",
            "status": "FINITE_FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "LL4713_3_arena_transfer_bound",
            "quantity": "arena EM coefficient leakage",
            "formula": "B_arena,EM <= |K_arena_EM| (L_linear |tau_arena| + B_rad_arena + B_readout_arena + E_same_current_tail).",
            "units": "arena residual units",
            "zero_condition": "same-current owner plus arena tau/readout maps and L_linear=0",
            "needed_source": "K_arena_EM, tau_arena, material/source profile and same-current map for R10, WEP, PPN, orbital or clock arena",
            "status": "TRANSFER_FORMULA_READY_MAPS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "LL4713_4_source_pack_update",
            "quantity": "RCP4712_9_Llinear update",
            "formula": "RCP4712_9 is no longer a vague missing coupling: it is either zero by NLO4713_1/2 or bounded by LL4713_0.",
            "units": "see LL4713_0",
            "zero_condition": "NLO4713_1/2 parent-signed",
            "needed_source": "parent signature or numeric derivative row",
            "status": "SOURCE_PACK_REFINED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def promotion_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "GATE4713_0_RQ_root",
            "gate": "R_Q exact root",
            "required_condition": "4712 exact root clauses sign: lambda_RQ>0, Pi_coker R_Q=0, J_root=0 and B_root=0",
            "current_status": "BLOCKED_SOURCE_PACK_VALUES_MISSING",
            "passes": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "GATE4713_1_even_owner",
            "gate": "even residual owner",
            "required_condition": "EM kinetic coefficient depends on R_Q only through <R_Q,R_Q>_P or another even residual scalar",
            "current_status": "EXACT_THEOREM_DERIVED_PARENT_SIGNATURE_MISSING",
            "passes": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "GATE4713_2_operator_domain",
            "gate": "no independent Coeff(F_Q^2) target",
            "required_condition": "visible operator domain/image theorem forbids lambda_A F_Q^2 and hidden/material Hom into Coeff(F_Q^2)",
            "current_status": "UNSIGNED_OPERATOR_DOMAIN_EXHAUSTION",
            "passes": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "GATE4713_3_radiative_readout",
            "gate": "radiative/readout preservation",
            "required_condition": "RG/threshold/readout maps are quotient-natural on the same branch as the bare owner",
            "current_status": "CONDITIONAL_THEOREMS_VALUES_MISSING",
            "passes": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "GATE4713_4_stress_poynting_current",
            "gate": "full EM stress/Poynting/current transfer",
            "required_condition": "T_EM, Poynting flux, Hodge star and matter current descend from the same owner or are bounded",
            "current_status": "SEPARATE_NEXT_TARGET",
            "passes": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4713_0_no_symmetry_shortcut",
            "rule": "Do not claim U(1) or diffeomorphism covariance forbids linear EM kinetic coefficients; F_Q^2 scalar coefficients are symmetry-legal unless parent operator-domain exhaustion forbids them.",
            "why": "1057/765/3222 supply explicit counterterms.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4713_1_no_tau_fit",
            "rule": "Do not set tau_clock_time=0 to hide a nonzero L_linear; derive tau zero or zero L_linear separately.",
            "why": "4710 made exact-root bypass the clean route, not a fitted clock silence.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4713_2_no_clock_to_R10_transfer",
            "rule": "Do not transfer clock alpha closure to R10, WEP, PPN or orbital systems without arena tau, material profile, source/test current and readout maps.",
            "why": "4708/4709 leave standalone B_readout and arena transfer blocked.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4713_3_no_Poynting_erasure",
            "rule": "Do not treat F_Q^2 coefficient silence as full EM stress/Poynting silence; null radiation can have F_Q^2=0 but nonzero T_EM and Poynting flux.",
            "why": "3222 stress/Poynting guard remains separate and becomes the next target.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4713_0_main",
            "decision": DECISION,
            "meaning": "The no-linear EM owner is now a real theorem target: either even residual/operator-domain parent signatures set L_linear=0, or the leak is carried as an explicit finite coefficient.",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4713_1_next",
            "decision": "ATTACK_EM_STRESS_POYNTING_CURRENT_NEXT",
            "meaning": "Even if L_linear closes, local-GR/Maxwell transfer still needs T_EM, Poynting flux, Hodge/current and source-normalization ownership.",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4713_0",
            "status": "PRIVATE_NONCLAIM",
            "summary": "No-linear EM-owner proof route derived conditionally; current corpus still needs parent signature or a finite L_linear source row.",
            "local_gr_claim": False,
            "clock_claim": False,
            "r10_wep_ppn_orbital_claim": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NT4713_0",
            "target": NEXT_TARGET,
            "reason": "The scalar EM kinetic no-linear route is now exact-conditional; the next high-risk channel is full EM stress/Poynting/current ownership because F_Q^2 silence is not T_EM silence.",
            "derive_first": "prove same-owner Hodge/current/T_EM/Poynting descent or a no-wall-flux theorem",
            "fallback": "stage side-channel coefficient rows for Poynting flux, Hodge leak, current normalization and arena transfer",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_body(timestamp: str, sources: list[dict[str, Any]], theorem: list[dict[str, Any]], llinear: list[dict[str, Any]], gates: list[dict[str, Any]], firewalls: list[dict[str, Any]]) -> str:
    return f"""# 4713 - No-Linear EM Owner: Even Residual Symmetry or `L_linear` Bound

Generated: {timestamp}

Scope: local/private framework work only. No GitHub action.

## Result

This checkpoint moves the coupling problem forward rather than circling it: the linear EM kinetic leak is now an explicit first-jet object.

```text
Z_A = Z_bar(q_obs,theta) + ell_Q[R_Q] + lambda_D <R_Q,R_Q>_P
      + H_hid + B_rad + B_readout + O(||R_Q||^3).
```

At an exact residual root, the squared term has a double zero, but `ell_Q`, hidden-Hom, radiative and readout tails can still generate a first derivative unless a stronger parent owner forbids them.

## Main Derived Law

If the EM kinetic owner depends on the local residual only through an even scalar

```text
N_R = <R_Q,R_Q>_P,
Z_A = Z_bar(q_obs,theta) + F_even(N_R),
```

then

```text
D_m Z_A|R_Q=0 = F_even'(0) * 2<R_Q,D_m R_Q>_P|R_Q=0 = 0.
```

So the clean exact branch is:

```text
R_Q=0 + even residual owner + no independent Coeff(F_Q^2) target
=> L_linear=0.
```

## Bound If The Owner Is Not Signed

```text
L_linear := Z_A,min^-1 sup_{{||u||=1}} |ell_Q[A_Q u] + D_u H_hid|.
```

Clock exact-root leak:

```text
|D_tau ln alpha_EM| <= L_linear |tau_clock_time| + B_rad_clock + B_readout_clock.
```

Full finite branch:

```text
|D_tau ln alpha_EM| <= L_linear |tau_clock_time|
                     + C_D |Delta m tau_clock_time|
                     + E_HO + E_clock_transport
                     + B_rad_clock + B_readout_clock.
```

## Theorem Rows

{table(theorem)}

## `L_linear` Rows

{table(llinear)}

## Promotion Gates

{table(gates)}

## Firewalls

{table(firewalls)}

## Source Register

{table(sources)}

## Decision

`{DECISION}`

Next target: `{NEXT_TARGET}`.
"""


def formal_body(timestamp: str) -> str:
    return f"""# PPC4161 4713 - No-Linear EM Owner / `L_linear` Bound

Generated: {timestamp}

Private nonclaim checkpoint.

Core result:

```text
Z_A = Z_bar(q_obs,theta) + ell_Q[R_Q] + lambda_D <R_Q,R_Q>_P + H_hid + tails.
```

The exact zero route is now:

```text
R_Q=0
+ EM owner depends on R_Q only through <R_Q,R_Q>_P or another even residual scalar
+ no independent Coeff(F_Q^2) hidden/material/readout target
=> L_linear=0.
```

If this is not parent-signed, retain:

```text
|D_tau ln alpha_EM| <= L_linear |tau_clock_time| + B_rad_clock + B_readout_clock
```

and do not promote clock/R10/WEP/PPN/local-GR claims.

Validation: `{VALIDATION_CSV}`.
Next: `{NEXT_TARGET}`.
"""


def write_resume(timestamp: str) -> None:
    RESUME_PATH.write_text(
        f"""# Current Local Resume Bookmark

Generated: {timestamp}

Scope: local/private framework work only. No GitHub push, no public-stage update, no backup-repo operation.

## Latest Local Checkpoint

`4713-Y5-R2FR-no-linear-EM-owner-even-residual-symmetry-or-Llinear-bound.md`

## What Changed

The EM kinetic coupling obstruction is now a first-jet theorem/bound instead of a vague missing coupling:

```text
Z_A = Z_bar(q_obs,theta) + ell_Q[R_Q] + lambda_D <R_Q,R_Q>_P + H_hid + tails.
```

The exact zero route is:

```text
R_Q=0 + even residual owner + no independent Coeff(F_Q^2) target
=> L_linear=0.
```

If that owner is not parent-signed, retain:

```text
|D_tau ln alpha_EM| <= L_linear |tau_clock_time| + B_rad_clock + B_readout_clock.
```

## Current Best Next Target

`{NEXT_TARGET}`

## Do Not Do Next

- Do not claim ordinary U(1)/diffeomorphism symmetry forbids `F_Q^2` coefficients.
- Do not use clock closure as R10/WEP/PPN closure without arena maps.
- Do not erase Poynting or EM stress just because the scalar `F_Q^2` coefficient is quiet.
""",
        encoding="utf-8",
    )


def validation_rows(timestamp: str, sources: list[dict[str, Any]], theorem: list[dict[str, Any]], llinear: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks = [
        ("VAL4713_sources_exist", all(row["path_exists"] for row in sources), "all cited local source paths exist"),
        ("VAL4713_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        ("VAL4713_even_theorem_present", any(row["theorem_id"] == "NLO4713_1_even_residual_double_zero" for row in theorem), "even-residual double-zero theorem present"),
        ("VAL4713_countermodel_present", any(row["theorem_id"] == "NLO4713_3_symmetry_countermodel" for row in theorem), "ordinary symmetry countermodel retained"),
        ("VAL4713_Llinear_definition_present", any(row["row_id"] == "LL4713_0_Llinear_definition" for row in llinear), "L_linear definition row present"),
        ("VAL4713_no_claim_allowed", not any(str(row.get("claim_allowed", "")).lower() == "true" for row in theorem + llinear), "no theorem or bound row allows a claim"),
        ("VAL4713_gates_all_false", not all(bool(row["passes"]) for row in gates), "promotion gates not all passing"),
        ("VAL4713_doc_written", DOC_PATH.exists(), "checkpoint document written"),
        ("VAL4713_formal_written", FORMAL_PATH.exists(), "formal packet document written"),
        ("VAL4713_no_pycache", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": validation_id,
            "passed": bool(passed),
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4713_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "4713 artifacts validate as private nonclaim checkpoint",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> None:
    timestamp = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows(timestamp)
    theorem = theorem_rows(timestamp)
    llinear = llinear_rows(timestamp)
    gates = promotion_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_rows(timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_CSV, theorem)
    write_csv(LLINEAR_CSV, llinear)
    write_csv(PROMOTION_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    DOC_PATH.write_text(doc_body(timestamp, sources, theorem, llinear, gates, firewalls), encoding="utf-8")
    FORMAL_PATH.write_text(formal_body(timestamp), encoding="utf-8")
    append_claim_once(timestamp)

    append_once(
        SPINE_PATH,
        MARKER,
        f"""### {MARKER}

- Claim: `{CLAIM_ID}`.
- Status: private nonclaim.
- Movement: the EM kinetic coupling gap is now a first-jet theorem/bound: exact zero requires `R_Q=0`, an even residual owner and no independent `Coeff(F_Q^2)` target.
- Bound: `L_linear := Z_A,min^-1 sup |ell_Q[A_Q u] + D_u H_hid|`; exact-root clock leak is `|D_tau ln alpha_EM| <= L_linear |tau_clock_time| + B_rad_clock + B_readout_clock`.
- Firewall: ordinary U(1)/diffeomorphism covariance does not forbid scalar `F_Q^2` coefficients; full EM stress/Poynting/current ownership is still separate.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: turns the no-linear EM-owner obstruction into exact even-residual/operator-domain conditions plus a finite `L_linear` leak row.
- Validation: `{VALIDATION_CSV}`.
""",
    )
    write_resume(timestamp)

    shutil.rmtree(POST / "scripts" / "__pycache__", ignore_errors=True)
    validation = validation_rows(timestamp, sources, theorem, llinear, gates)
    write_csv(VALIDATION_CSV, validation)


if __name__ == "__main__":
    main()
