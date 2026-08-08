from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4723"
CLAIM_ID = "L-565"
MARKER = "PPC4161_PARENT_EH_SIGNATURE_EVIDENCE_HUNT_OR_R2_SOURCE_ROW_4723"
PACKET_MARKER = "PPC4161_PACKET_PARENT_EH_SIGNATURE_EVIDENCE_HUNT_OR_R2_SOURCE_ROW_4723"
DECISION = "PARENT_EH_SELECTOR_EVIDENCE_SUPPORTS_PRIVATE_AMF_IR_ROUTE_BUT_GLOBAL_SIGNATURE_UNSIGNED_R2_SOURCE_ROW_RETAINED_NONCLAIM"
NEXT_TARGET = "4724-Y5-R2FR-visible-cell-cR2-zero-signature-or-R2-mu-bound-runner.md"

DOC_PATH = POST / "4723-Y5-R2FR-parent-EH-signature-evidence-hunt-or-R2-mR-alpha-first-source-row.md"
FORMAL_PATH = FORMAL / "739-PPC4161-parent-EH-signature-evidence-hunt-or-R2-mR-alpha-first-source-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4723_SOURCE_REGISTER.csv"
EVIDENCE_HUNT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4723_PARENT_EH_EVIDENCE_HUNT_ROWS.csv"
VERDICT_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4723_EH_SIGNATURE_VERDICT_MATRIX.csv"
R2_SOURCE_ROW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4723_R2_MR_ALPHA_FIRST_SOURCE_ROW.csv"
R2_HUNT_STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4723_R2_SOURCE_HUNT_STATUS.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4723_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4723_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4723_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4723_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4723_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4723_VALIDATION.csv"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"No rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, block: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    separator = "\n\n" if existing and not existing.endswith("\n\n") else ""
    path.write_text(existing + separator + block.rstrip() + "\n", encoding="utf-8", newline="\n")


def add_claim_once(ts: str) -> None:
    CLAIMS_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not CLAIMS_PATH.exists():
        raise FileNotFoundError(CLAIMS_PATH)
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = handle.seek(0) or next(csv.reader(open(CLAIMS_PATH, encoding="utf-8-sig", newline="")))
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_bridge",
        "claim": "4723 completes the parent-EH evidence hunt: A_MF plus the IR selector supports a private conditional route to the EH/Palatini block, but the global parent signature and MTS-owned R2 mass/coupling rows remain unsigned.",
        "current_evidence": "Generated source register, parent EH evidence hunt, EH signature verdict matrix, first R2 m_R/alpha source row, R2 source-hunt status, promotion gates, firewalls, decision, status, next target and validation.",
        "status": "parent_EH_evidence_hunt_R2_source_row_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating a private A_MF/IR selector route, a standard f(R) template, or a visible-cell zero lemma as a parent-derived MTS prediction.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Selector-signature smuggling or backsolving R2 alpha(lambda) from bounds instead of deriving the parent coefficient.",
        "title": "Parent EH signature evidence hunt or R2 first source row",
        "notes": f"{MARKER}; {DECISION}; generated {ts}",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


SOURCE_SPECS = [
    ("SRC4723_0", POST / "CURRENT_LOCAL_RESUME.md", "4723-Y5-R2FR-parent-EH-signature-evidence-hunt-or-R2-mR-alpha-first-source-row.md", "4722 handoff target."),
    ("SRC4723_1", POST / "4722-Y5-R2FR-parent-two-derivative-signature-insertion-or-R2-alpha-lambda-runner.md", "Parent Signature Insertion Audit", "4722 narrative handoff."),
    ("SRC4723_2", SOURCE_DIR / "P8_Y5_R2FR_4722_PARENT_EH_SIGNATURE_INSERTION_AUDIT.csv", "SIG4722_1_two_derivative_IR", "4722 parent EH signature audit rows."),
    ("SRC4723_3", SOURCE_DIR / "P8_Y5_R2FR_4722_R2_ALPHA_LAMBDA_RUNNER_RESULTS.csv", "BLOCKED_MISSING_PARENT_ALPHA_OR_MASS", "4722 fail-closed R2 alpha(lambda) runner results."),
    ("SRC4723_4", SOURCE_DIR / "P8_Y5_R2FR_4721_TWO_DERIVATIVE_EH_SELECTOR_PROOF_ROWS.csv", "TDEH4721_1_two_derivative_count", "4721 conditional two-derivative EH selector proof."),
    ("SRC4723_5", SOURCE_DIR / "P8_Y5_R2FR_4184_IR_SELECTOR_AXIOM_SET.csv", "SEL4184_2_IR_order", "4184 explicit IR selector clauses."),
    ("SRC4723_6", SOURCE_DIR / "P8_Y5_R2FR_4184_BRANCH_DECISION.csv", "CONDITIONAL_PALATINI_IR_SELECTOR_THEOREM_WRITTEN", "4184 branch decision: selector theorem conditional, parent debts active."),
    ("SRC4723_7", SOURCE_DIR / "P8_Y5_R2FR_4184_RESIDUAL_EFT_BOUND_LEDGER.csv", "RB4184_1_cR2", "4184 c_R2 residual ledger."),
    ("SRC4723_8", SOURCE_DIR / "P8_Y5_R2FR_4449_A_MF_EVIDENCE_OUTPUT.csv", "AMF4449_6_ir_selector", "4449 A_MF adoption evidence and downstream selector status."),
    ("SRC4723_9", SOURCE_DIR / "P8_Y5_R2FR_4539_PARENT_ACTION_SELECTOR_CONTRACT.csv", "PAC4539_4_IR_selector", "4539 exact parent-action selector contract."),
    ("SRC4723_10", SOURCE_DIR / "P8_Y5_R2FR_4539_CONDITIONAL_THEOREM_AND_FAILURE.csv", "TH4539_1_current_failure", "4539 current failure of global parent-derived local GR."),
    ("SRC4723_11", SOURCE_DIR / "P8_Y5_R2FR_4540_IR_NORMAL_FORM_THEOREM.csv", "NFT4540_1_EC_Palatini_selection", "4540 conditional IR normal-form theorem."),
    ("SRC4723_12", SOURCE_DIR / "P8_Y5_R2FR_4540_EFT_RESIDUAL_ENVELOPE.csv", "EFT4540_5_cR2", "4540 active EFT residual envelope."),
    ("SRC4723_13", SOURCE_DIR / "P8_Y5_R2FR_4471_CONTINUUM_SCALING_DERIVATION.csv", "SCL4471_1_quadratic_visible", "4471 visible-cell R2 scaling law."),
    ("SRC4723_14", SOURCE_DIR / "P8_Y5_R2FR_4471_NO_GRAIN_THEOREM.csv", "NG4471_5_verdict", "4471 no-grain zero theorem verdict."),
    ("SRC4723_15", SOURCE_DIR / "P8_Y5_R2FR_4471_FIRST_CR2EFF_INTAKE_ROW.csv", "CR2I4471_2_total_effective_component", "4471 first c_R2_eff intake row."),
    ("SRC4723_16", SOURCE_DIR / "P8_Y5_R2FR_4504_R2FR_SCALARON_VARIATION_LAW.csv", "R2V4504_2_trace", "4504 standard R2/f(R) scalaron variation law."),
    ("SRC4723_17", SOURCE_DIR / "P8_Y5_R2FR_4504_FINITE_BOUND_CONTRACT.csv", "FB4504_1_standard_mu_bound", "4504 finite bound contract."),
    ("SRC4723_18", SOURCE_DIR / "P8_Y5_R2FR_4504_STANDARD_BOUND_IMPORT.csv", "SB4504_2_combined_range", "4504 standard f(R) imported template bound."),
    ("SRC4723_19", SOURCE_DIR / "P8_Y5_PARENT_QLOC_1589_COEFFICIENT_SOURCE_HUNT.csv", "HUNT1589_7_verdict", "1589 parent coefficient source-hunt verdict."),
    ("SRC4723_20", SOURCE_DIR / "P8_Y5_BRR545_1589_VALIDATION.csv", "VAL1589_2_hunt_verdict_blocks", "1589 validation: no parent-owned c_R2/fRR theorem-zero or numeric coefficient."),
    ("SRC4723_21", SOURCE_DIR / "R11_nonEH_operator_vector_executable.csv", "R2_fR_scalar_mode", "R11 non-EH operator vector R2/f(R) missing coefficient row."),
    ("SRC4723_22", SOURCE_DIR / "P8_DOUBLE_ZERO_R11_OPERATOR_MAPPING.csv", "R2_fR_scalar_mode", "R11 double-zero mapping contract for R2/f(R)."),
]


def source_register(ts: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "evidence_weight": "source_backed_local_file" if path.exists() and needle in text else "missing_or_unverified",
                "valid_for_claim": False,
                "timestamp_utc": ts,
            }
        )
    return rows


def source_path_by_id(source_id: str) -> str:
    for row_id, path, _needle, _role in SOURCE_SPECS:
        if row_id == source_id:
            return str(path)
    raise KeyError(source_id)


def evidence_hunt_rows(ts: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_ok = {row["source_id"]: bool(row["exists"]) and bool(row["needle_found"]) for row in sources}
    specs = [
        (
            "EHV4723_0_A_MF_private_support",
            "A_MF motion-frame route",
            "A_MF has enough internal evidence for a private adoption route into Cartan/coframe variables.",
            "SRC4723_8",
            "SUPPORTS_PRIVATE_ADOPTION_NOT_PUBLIC_DERIVATION",
            "A_MF is adopted as a candidate/private axiom input, not derived from older parent grammar.",
            "Keep using A_MF for private derivation tests, but never count it as public proof.",
        ),
        (
            "EHV4723_1_IR_selector_support",
            "EH/Palatini IR selector",
            "A_MF plus locality, one observed coframe, low derivative order, no extra light modes and routed boundary selects the EC/Palatini principal block.",
            "SRC4723_6",
            "CONDITIONAL_SUPPORT",
            "Selector assumptions remain parent debts; they are not signed by the parent object language.",
            "Either parent-sign the selector assumptions or retain every excluded term as a residual coefficient.",
        ),
        (
            "EHV4723_2_nonEH_residual_ledger",
            "R2 and non-EH residuals",
            "The residual ledger already names c_R2, c_D, c_Gamma, c_T, c_bdy and delta_kappa as live channels.",
            "SRC4723_7",
            "BLOCKS_FULL_LOCAL_GR_CLAIM",
            "No-extra-slots is false until the parent grammar kills or bounds these channels.",
            "Attack c_R2 first through a zero proof or bound runner; keep the others queued.",
        ),
        (
            "EHV4723_3_parent_action_contract_failure",
            "Global parent-action signature",
            "The exact parent-action contract exists, but current evidence fails EH/Palatini origin, IR selector derivation, boundary/global no-flux and quotient naturality.",
            "SRC4723_10",
            "GLOBAL_SIGNATURE_UNSIGNED",
            "This is the hard wall: the effective local-GR branch is useful but not yet parent-derived.",
            "Promote only after the parent clauses are signed in the same branch.",
        ),
        (
            "EHV4723_4_normal_form_theorem",
            "IR normal-form route",
            "Under locality, covariance, parity-even sector, one coframe and one-curvature IR order, EC/Palatini reduces to EH after torsion silence.",
            "SRC4723_11",
            "CONDITIONAL_TRUE_SCALE_LAW_MISSING",
            "The parent scale/gap law and no-extra-light-mode theorem are missing.",
            "Derive the scale/gap law or turn it into explicit R10/PPN/orbital bounds.",
        ),
        (
            "EHV4723_5_visible_cell_zero_hint",
            "Visible c_R2_cell zero route",
            "The visible cell R2 contribution scales as ell_cell^2 and vanishes if ell is gauge refinement with smooth c2 and no singular residue.",
            "SRC4723_14",
            "CONDITIONAL_ZERO_HINT",
            "This only kills the visible-cell contribution; total c_R2_eff still has bare, hidden, measure and boundary terms.",
            "Try to parent-sign the no-grain/no-residue package; otherwise fill c_R2_eff components.",
        ),
        (
            "EHV4723_6_R2_scalaron_template",
            "R2/f(R) scalaron fallback",
            "The standard template gives m_R^2=1/(6 mu), lambda_R=sqrt(6 mu), and alpha_eff=1/3 times body-charge/screening factors.",
            "SRC4723_16",
            "FORMULA_READY_MTS_MAP_MISSING",
            "The template is not an MTS prediction until c_R2_eff -> mu and body-charge alpha are parent-owned.",
            "Fill mu/c_R2_eff and alpha_eff rows, or prove selector-zero.",
        ),
        (
            "EHV4723_7_prior_source_hunt",
            "Prior R2 source hunt",
            "The older coefficient hunt found no parent-owned c_R2/fRR theorem-zero, numeric coefficient, finite scalar source map or claim-grade scoring row.",
            "SRC4723_19",
            "NO_CLAIM_READY_PARENT_COEFFICIENT_FOUND",
            "The absence is now a formal source-backed blocker, not a vibe.",
            "Use this as the starting ledger for the 4724 fill/zero attempt.",
        ),
        (
            "EHV4723_8_R11_operator_vector",
            "R11 operator vector",
            "R2_fR_scalar_mode is explicitly present as a missing coefficient/normalization/weak-field-map row.",
            "SRC4723_21",
            "LIVE_OPERATOR_ROW_MISSING_VALUE",
            "The theory has a named channel but not the parent number or exact zero.",
            "Route 4724 to c_R2_eff zero proof or finite mu/R10 runner.",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "evidence_target": target,
            "current_support": support,
            "source_path": source_path_by_id(source_id),
            "source_verified": source_ok[source_id],
            "verdict": verdict,
            "blocker": blocker,
            "next_action": next_action,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for row_id, target, support, source_id, verdict, blocker, next_action in specs
    ]


def verdict_matrix_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        (
            "VER4723_0_A_MF_variables",
            "Motion-frame/Cartan variables admitted.",
            True,
            True,
            False,
            "A_MF adoption is private and candidate-level; older corpus does not derive it globally.",
        ),
        (
            "VER4723_1_geometry_domain",
            "One visible metric/coframe and compatible connection before readout.",
            True,
            True,
            False,
            "Needs parent-owned domain/projector/action clause, not just effective branch declaration.",
        ),
        (
            "VER4723_2_two_derivative_IR",
            "Bulk principal local order restricted to two derivatives / one curvature.",
            True,
            True,
            False,
            "Parent scale/gap law missing; R2/Ricci2/Weyl2 remain residual channels.",
        ),
        (
            "VER4723_3_no_extra_slots",
            "No scalar/vector/disformal/memory/source coefficient target exists in the local collar.",
            False,
            False,
            False,
            "Existing residual envelopes explicitly retain c_R2, c_D, c_Gamma, c_T, c_bdy and delta_kappa.",
        ),
        (
            "VER4723_4_torsion_resolution",
            "Torsion/nonmetricity algebraic, heavy, silent or coefficient-routed.",
            True,
            True,
            False,
            "EC/Palatini reduction is conditional; global torsion/nonmetricity silence not parent-signed.",
        ),
        (
            "VER4723_5_boundary_topological",
            "Boundary/topological pieces fixed, exact, routed or source-blind.",
            True,
            True,
            False,
            "Boundary/global no-flux and source-blind routing are current parent debts.",
        ),
        (
            "VER4723_6_common_normalization",
            "M_EH and lambda_D are common normalizations, not species/source prefactors.",
            True,
            True,
            False,
            "4718 gives a conditional owner law, but the EH local metric limit and parent signature remain unsigned.",
        ),
        (
            "VER4723_7_R2_zero_or_source_row",
            "R2/f(R) channel either exactly zero or has m_R/alpha rows.",
            False,
            False,
            False,
            "No parent-owned c_R2_eff, mu, m_R, alpha_eff, C_body or selector-zero certificate exists.",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "verdict_id": row_id,
            "clause": clause,
            "conditional_support": support,
            "private_branch_ready": private_ready,
            "parent_signed": parent_signed,
            "blocker": blocker,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for row_id, clause, support, private_ready, parent_signed, blocker in specs
    ]


def r2_source_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "R2SRC4723_0_mu_or_cR2eff",
            "quantity": "mu or c_R2_eff_total",
            "required_formula_or_value": "mu = N_MTS_to_fR * c_R2_eff_total in standard f(R)=R+mu R^2 units",
            "current_value": "MISSING_PARENT_c_R2_eff_TOTAL_OR_mu",
            "units": "m^2 after EH/f(R) normalization",
            "source_path": source_path_by_id("SRC4723_17"),
            "source_status": "formula_ready_values_unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_action": "derive c_R2_eff_total=0 or fill numeric mu/c_R2_eff with units and source path",
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "R2SRC4723_1_mR_lambdaR",
            "quantity": "m_R and lambda_R",
            "required_formula_or_value": "m_R^2=1/(6 mu); lambda_R=sqrt(6 mu) in the standard length convention used by 4504",
            "current_value": "MISSING_mu_SO_mR_AND_lambdaR_NOT_NUMERIC",
            "units": "1/m^2 for m_R^2; m for lambda_R",
            "source_path": source_path_by_id("SRC4723_16"),
            "source_status": "standard_template_ready_MTS_mu_missing",
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_action": "do not score R10 until mu is parent-owned or zero",
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "R2SRC4723_2_alpha_eff",
            "quantity": "alpha_eff",
            "required_formula_or_value": "alpha_eff = (1/3) * C_body^2 for unscreened metric f(R), or explicit screened/body-charge value",
            "current_value": "MISSING_C_body_SCREENING_OR_SELECTOR_ZERO",
            "units": "dimensionless",
            "source_path": source_path_by_id("SRC4723_18"),
            "source_status": "template_only_body_charge_missing",
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_action": "derive body/source scalar charge or exact zero before comparing alpha(lambda)",
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "R2SRC4723_3_standard_mu_bound_template",
            "quantity": "standard f(R) template bound",
            "required_formula_or_value": "lambda_R <= 9.306372e+07 m; mu <= 1.443476e+15 m^2 if MTS uses the same normalization",
            "current_value": "1.443476e+15",
            "units": "m^2",
            "source_path": source_path_by_id("SRC4723_18"),
            "source_status": "standard_template_only_not_MTS_claim",
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_action": "use only as a bound target after MTS supplies mu/c_R2_eff and screening branch",
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "R2SRC4723_4_visible_cell_zero_switch",
            "quantity": "Z_no_grain_visible_cell",
            "required_formula_or_value": "Z_no_grain=true iff ell is gauge, c2 smooth, no singular counterterm, and no hidden/bare/measure/boundary residue",
            "current_value": "CONDITIONAL_THEOREM_PARENT_SIGNATURE_UNSIGNED",
            "units": "boolean certificate",
            "source_path": source_path_by_id("SRC4723_14"),
            "source_status": "visible_component_zero_hint_total_zero_unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_action": "try parent-sign no-grain/no-residue package in 4724",
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "R2SRC4723_5_prior_hunt_verdict",
            "quantity": "parent-owned R2 coefficient/source row",
            "required_formula_or_value": "theorem-zero or numeric c_R2/fRR/mu/m_R/alpha_eff row with source path",
            "current_value": "NO_CLAIM_READY_PARENT_COEFFICIENT_FOUND",
            "units": "not_applicable",
            "source_path": source_path_by_id("SRC4723_19"),
            "source_status": "source_hunt_blocker_confirmed",
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_action": "derive zero route or fill finite coefficient row; do not infer from experimental upper bounds",
            "timestamp_utc": ts,
        },
    ]


def r2_hunt_status_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("R2H4723_0_formula_side", "scalaron formula", "ready", "4504 gives standard formulas for trace, lambda_R and alpha_eff template."),
        ("R2H4723_1_bound_template", "standard bound target", "ready_nonclaim", "4504 imports a standard mu/range bound but only after MTS normalization and screening are owned."),
        ("R2H4723_2_bound_curve", "R10 alpha(lambda) curve", "smoke_only", "4722 already joined a nonclaim vector-digitized curve for smoke; claim-grade QA remains separate."),
        ("R2H4723_3_MTS_mu", "MTS mu/c_R2_eff", "missing", "No parent-owned c_R2_eff_total -> mu map or numeric value."),
        ("R2H4723_4_MTS_alpha", "MTS alpha_eff/body charge", "missing", "No parent-owned C_body, screening branch or exact scalar source zero."),
        ("R2H4723_5_selector_zero", "selector-zero branch", "unsigned", "Visible-cell zero is conditional and total c_R2_eff zero is not parent-signed."),
        ("R2H4723_6_verdict", "R2 local-GR pass status", "blocked_nonclaim", "R2/f(R) remains a retained residual branch, not a local-GR pass."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "hunt_id": hunt_id,
            "object": obj,
            "status": status,
            "detail": detail,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for hunt_id, obj, status, detail in specs
    ]


def gate_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4723_0_sources_verified", "All 4723 source paths exist and needles are found.", True, "NONE"),
        ("GATE4723_1_parent_EH_signature_signed", "Parent action signs A_MF, domain, IR order, no-extra-slots, boundary, torsion and normalization in one branch.", False, "PARENT_SIGNATURE_UNSIGNED"),
        ("GATE4723_2_selector_assumptions_parent_derived", "IR selector assumptions are derived from parent grammar rather than adopted.", False, "SELECTOR_ASSUMPTIONS_NOT_PARENT_DERIVED"),
        ("GATE4723_3_R2_mu_numeric_or_zero", "MTS supplies numeric mu/c_R2_eff or exact parent selector-zero.", False, "MISSING_PARENT_MU_OR_ZERO_CERTIFICATE"),
        ("GATE4723_4_R2_alpha_numeric_or_zero", "MTS supplies alpha_eff/body charge/screening or exact zero.", False, "MISSING_PARENT_ALPHA_OR_BODY_CHARGE"),
        ("GATE4723_5_R2_bound_claim_ready", "R10/gamma/beta/orbital bound comparison has claim-grade data and MTS prediction inputs.", False, "BOUND_SIDE_AND_MTS_SIDE_NOT_CLAIM_READY"),
        ("GATE4723_6_public_local_GR_claim", "Local GR branch is parent-derived with no unbounded non-EH residuals.", False, "EFFECTIVE_PRIVATE_BRANCH_ONLY"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "condition": condition,
            "passed": passed,
            "blocker": blocker,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for gate_id, condition, passed, blocker in specs
    ]


def firewall_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4723_0_private_adoption_not_public_proof", "Do not treat A_MF private adoption as a parent derivation."),
        ("FW4723_1_selector_not_covariance_only", "Do not claim covariance alone selects EH; the selector uses extra IR/field-content assumptions."),
        ("FW4723_2_no_visible_cell_overclaim", "Do not turn visible c_R2_cell zero into total c_R2_eff zero without no-bare/no-hidden/no-measure/no-boundary signatures."),
        ("FW4723_3_no_bound_backsolve", "Do not infer MTS mu or alpha by backsolving experimental bounds."),
        ("FW4723_4_no_calibrated_G_scale_hack", "Do not use measured G, GM or Planck-length declarations as the parent cell scale."),
        ("FW4723_5_no_R2_localGR_pass", "Do not call R10/PPN/local-GR passed until R2/f(R) mass and coupling are source-backed or zero."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for firewall_id, rule in specs
    ]


def status_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4723_0_local_only",
            "status": "local_files_only_no_github_action",
            "detail": "Generated under post-checkpoint-work and formalization-workbench only.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4723_1_science_verdict",
            "status": "private_EH_route_supported_global_parent_signature_unsigned",
            "detail": "The private route is stronger than a vibe, but not yet a public local-GR derivation.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def decision_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "parent_EH_result": "private A_MF/IR route supported; global parent signature unsigned",
            "R2_result": "standard scalaron formulas ready; MTS mu/m_R/alpha rows missing; visible-cell zero route conditional only",
            "local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": ts,
        }
    ]


def next_target_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "The best leap-forward target is the c_R2 gate: either parent-sign total c_R2_eff=0 via visible-cell/no-grain/no-residue, or run the standard mu/R10 finite-bound branch as a nonclaim runner.",
            "first_task": "Attempt total c_R2_eff zero signature: visible cell + no bare + no hidden B L^-1 B + no measure + no boundary.",
            "fallback_task": "If any term remains unsigned, build the finite mu/lambda/alpha bound runner without claiming local GR.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def markdown_bullets(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(ts: str, evidence_rows: list[dict[str, Any]], verdict_rows: list[dict[str, Any]], r2_rows: list[dict[str, Any]], gate_rows_: list[dict[str, Any]]) -> None:
    doc = f"""# 4723 - Parent EH Signature Evidence Hunt or R2 mR/Alpha First Source Row

Generated: `{ts}`

## Purpose

4723 checks whether the parent EH selector is already source-backed strongly enough to promote the local branch, and if not, records the first exact `R2/f(R)` mass/coupling source row needed for a real bound runner.

## What Moved Forward

- The EH route is no longer just informal: `A_MF` plus the 4184 IR selector gives a coherent private route to the EC/Palatini/EH principal block.
- The public/global signature still fails: the parent corpus has not signed the selector assumptions, no-extra-light-mode law, boundary/no-flux law, quotient naturality, or total `c_R2_eff=0`.
- The `R2/f(R)` fallback is sharpened to exact missing rows: `mu/c_R2_eff_total`, `m_R/lambda_R`, and `alpha_eff/body charge`.
- The visible-cell `c_R2_cell -> 0` route is useful, but it only kills one component unless no-bare/no-hidden/no-measure/no-boundary signatures are also proved.

## Parent EH Evidence Hunt

{markdown_bullets(evidence_rows, "row_id", "verdict")}

## EH Signature Verdict Matrix

{markdown_bullets(verdict_rows, "verdict_id", "blocker")}

## R2 First Source Row

{markdown_bullets(r2_rows, "row_id", "current_value")}

## Gates

{markdown_bullets(gate_rows_, "gate_id", "blocker")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 739 - Parent EH Signature Evidence Hunt or R2 mR/Alpha First Source Row

Generated: `{ts}`

## Branch Result

The current branch has a serious private path to local EH: `A_MF` plus the explicit IR selector coherently lands on the EC/Palatini/EH principal block. It is not yet a public parent theorem because the parent action has not signed the selector, no-extra-mode, boundary/no-flux, quotient-naturality or total `c_R2_eff` zero clauses in one branch.

## Exact Missing R2 Inputs

- `mu = N_MTS_to_fR c_R2_eff_total` or exact `c_R2_eff_total=0`.
- `m_R^2=1/(6 mu)` and `lambda_R=sqrt(6 mu)` after the MTS normalization map is owned.
- `alpha_eff=(1/3) C_body^2` or a parent-owned screened/body-charge value.
- The standard `mu <= 1.443476e+15 m^2` row remains template-only until MTS owns `mu` and the body-charge branch.

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_and_packet(ts: str) -> None:
    spine_block = f"""### {MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Derivation gain: the parent-EH evidence is sorted into support versus blockers; the private `A_MF` + IR route is coherent, while the global parent signature remains unsigned.
- R2/f(R) gain: the first source row now names exactly what must be derived or sourced: `mu/c_R2_eff_total`, `m_R/lambda_R`, `alpha_eff/body charge`, or exact selector-zero.
- Next: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: converts the parent-EH selector question into a source-backed evidence matrix and converts the R2 fallback into exact missing mass/coupling rows.
- Validation: `{VALIDATION_CSV}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{ts}`

## Latest completed checkpoint

`{DOC_PATH.name}`

## Decision

`{DECISION}`

## What moved forward

- Parent EH evidence was split into private-support rows and global-signature blockers.
- The R2/f(R) fallback now has an exact first source row for `mu/c_R2_eff_total`, `m_R/lambda_R`, and `alpha_eff/body charge`.
- The visible-cell `c_R2_cell` zero route is preserved as the best next derivation attempt, but total `c_R2_eff=0` is not claimed.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
"""
    write_text(RESUME_PATH, resume)


def cleanup_pycache() -> None:
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def parse_csv(path: Path) -> bool:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def validation_rows(
    sources: list[dict[str, Any]],
    evidence_rows_: list[dict[str, Any]],
    verdict_rows_: list[dict[str, Any]],
    r2_rows_: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    ts: str,
) -> list[dict[str, Any]]:
    csv_paths = [
        SOURCE_REGISTER_CSV,
        EVIDENCE_HUNT_CSV,
        VERDICT_MATRIX_CSV,
        R2_SOURCE_ROW_CSV,
        R2_HUNT_STATUS_CSV,
        GATES_CSV,
        FIREWALL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_TARGET_CSV,
    ]
    checks: list[tuple[str, bool, str]] = [
        ("VAL4723_0_sources_exist", all(bool(row["exists"]) for row in sources), "all cited 4723 source paths exist"),
        ("VAL4723_1_needles_found", all(bool(row["needle_found"]) for row in sources), "all cited 4723 source needles found"),
        ("VAL4723_2_support_and_blockers_written", any("SUPPORT" in row["verdict"] for row in evidence_rows_) and any("BLOCK" in row["verdict"] or "UNSIGNED" in row["verdict"] or "MISSING" in row["verdict"] for row in evidence_rows_), "evidence hunt contains support and blocker rows"),
        ("VAL4723_3_global_parent_signature_blocked", not any(bool(row["parent_signed"]) for row in verdict_rows_), "no EH signature verdict row is promoted to parent-signed"),
        ("VAL4723_4_R2_source_rows_nonclaim", all(not bool(row["valid_for_claim"]) and not bool(row["claim_allowed"]) for row in r2_rows_), "R2 source rows remain nonclaim"),
        ("VAL4723_5_required_R2_inputs_named", all(any(token in str(row["current_value"]) or token in str(row["required_formula_or_value"]) for row in r2_rows_) for token in ["mu", "m_R", "alpha_eff"]), "mu, m_R and alpha_eff are named in source rows"),
        ("VAL4723_6_claim_gates_closed", all(not bool(row["claim_allowed"]) for row in gates) and not any(row["passed"] for row in gates if row["gate_id"] != "GATE4723_0_sources_verified"), "all claim gates remain closed except source verification"),
        ("VAL4723_7_docs_written", DOC_PATH.exists() and FORMAL_PATH.exists(), "checkpoint and formal documents written"),
        ("VAL4723_8_spine_packet_markers", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), "spine and packet markers inserted"),
        ("VAL4723_9_resume_updated", NEXT_TARGET in read_text(RESUME_PATH), "resume points to 4724 next target"),
        ("VAL4723_10_csv_parse", all(parse_csv(path) for path in csv_paths), "all generated 4723 CSV files parse cleanly"),
        ("VAL4723_11_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
    ]
    overall = all(result for _check_id, result, _detail in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "timestamp_utc": ts,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4723_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "4723 parent EH evidence hunt or R2 source-row validation",
            "timestamp_utc": ts,
        }
    )
    return rows


def main() -> None:
    ts = now()
    cleanup_pycache()

    sources = source_register(ts)
    evidence = evidence_hunt_rows(ts, sources)
    verdicts = verdict_matrix_rows(ts)
    r2_rows_ = r2_source_rows(ts)
    r2_status = r2_hunt_status_rows(ts)
    gates = gate_rows(ts)
    firewalls = firewall_rows(ts)
    decisions = decision_rows(ts)
    statuses = status_rows(ts)
    next_targets = next_target_rows(ts)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(EVIDENCE_HUNT_CSV, evidence)
    write_csv(VERDICT_MATRIX_CSV, verdicts)
    write_csv(R2_SOURCE_ROW_CSV, r2_rows_)
    write_csv(R2_HUNT_STATUS_CSV, r2_status)
    write_csv(GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(ts, evidence, verdicts, r2_rows_, gates)
    update_spine_and_packet(ts)
    add_claim_once(ts)
    cleanup_pycache()
    validations = validation_rows(sources, evidence, verdicts, r2_rows_, gates, ts)
    write_csv(VALIDATION_CSV, validations)


if __name__ == "__main__":
    main()
