from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4523"
CLAIM_ID = "L-365"
MARKER = "PPC4161_SAME_BRANCH_PARENT_SIGNATURE_AUDIT_OR_FIRST_ALPHA_RUNNER_4523"
PACKET_MARKER = "PPC4161_PACKET_SAME_BRANCH_PARENT_SIGNATURE_AUDIT_OR_FIRST_ALPHA_RUNNER_4523"
DECISION = "SAME_BRANCH_PARENT_SIGNATURE_FAILS_FOR_CLAIM_RANK_ZERO_CONTRACT_WRITTEN_ALPHA_RESIDUAL_RUNNER_TRIGGERED"
NEXT_TARGET = "4524-Y5-R2FR-first-finite-residual-alpha-smoke-runner-or-parent-Z-action-signature.md"

FORMAL_PATH = FORMAL / "539-PPC4161-same-branch-parent-signature-audit-or-first-alpha-runner.md"
DOC_PATH = POST / "4523-Y5-R2FR-same-branch-parent-signature-audit-or-first-alpha-runner.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4523_SOURCE_REGISTER.csv"
PARENT_SIGNATURE = SOURCE_DIR / "P8_Y5_R2FR_4523_PARENT_SIGNATURE_AUDIT.csv"
BRANCH_COMPAT = SOURCE_DIR / "P8_Y5_R2FR_4523_SAME_BRANCH_COMPATIBILITY_MATRIX.csv"
RZ_ACTION_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4523_RANK_ZERO_PARENT_ACTION_CONTRACT.csv"
RUNNER_TRIGGER = SOURCE_DIR / "P8_Y5_R2FR_4523_FIRST_ALPHA_RESIDUAL_RUNNER_TRIGGER.csv"
RUNNER_INPUTS = SOURCE_DIR / "P8_Y5_R2FR_4523_FIRST_ALPHA_RUNNER_INPUTS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4523_DECISION.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4523_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4523_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4523_NEXT_TARGET.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4523_VALIDATION.csv"

FORMAL_4522 = FORMAL / "538-PPC4161-rank-M-lock-and-retained-current-firewall-or-alpha-runner.md"
DOC_4522 = POST / "4522-Y5-R2FR-rank-M-lock-and-retained-current-firewall-or-alpha-runner.md"
CLAUSES_4522 = SOURCE_DIR / "P8_Y5_R2FR_4522_CLAUSE_AUDIT.csv"
FBA_4522 = SOURCE_DIR / "P8_Y5_R2FR_4522_FINITE_BOUND_OR_ALPHA_RUNNER.csv"
FIREWALL_4522 = SOURCE_DIR / "P8_Y5_R2FR_4522_RETAINED_CURRENT_FIREWALL.csv"
DECISION_4522 = SOURCE_DIR / "P8_Y5_R2FR_4522_RANK_ZERO_DECISION_MATRIX.csv"

FORMAL_190 = FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md"
FORMAL_191 = FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md"
FORMAL_192 = FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md"
FORMAL_193 = FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md"
FORMAL_194 = FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md"
FORMAL_195 = FORMAL / "195-PPC4161-local-GR-private-closure-summary-and-parent-adoption-burden-map.md"
FORMAL_196 = FORMAL / "196-PPC4161-minimal-parent-action-adoption-matrix.md"

PARENT_CLAUSE_TESTS = SOURCE_DIR / "P8_Y5_BRR545_PARENT_ACTION_CLAUSE_TESTS.csv"
PARENT_ZERO_CONTRACT = SOURCE_DIR / "P8_Y5_BRR545_PARENT_ACTION_ZERO_THEOREM_CONTRACT.csv"
MIN_PARENT_TEST_CASES = SOURCE_DIR / "P8_Y5_MINIMAL_PARENT_ACTION_TEST_CASES.csv"
ADOPTION_2537 = SOURCE_DIR / "P8_Y5_NO_SHADOW_2537_ADOPTION_DECISION_MATRIX.csv"
MUC_2537 = SOURCE_DIR / "P8_Y5_NO_SHADOW_2537_MINIMAL_UNIVERSAL_MATTER_COUPLING_SIGNATURE.csv"
MCA_2587 = SOURCE_DIR / "P8_Y5_MIN_PARENT_MATTER_2587_ADOPTION_GATE.csv"
DM_2587 = SOURCE_DIR / "P8_Y5_MIN_PARENT_MATTER_2587_DOMAIN_MOTION_ROWS.csv"
LOCAL_RANK_901 = SOURCE_DIR / "P8_Y5_R10_901_LOCAL_RANK_ZERO_CERTIFICATE.csv"
NO_TOWER_2623 = SOURCE_DIR / "P8_Y5_PRIMITIVE_QUOTIENT_GATE_2623_NO_INTEGRATED_OUT_TOWER_AUDIT.csv"
NO_MARKER_2623 = SOURCE_DIR / "P8_Y5_PRIMITIVE_QUOTIENT_GATE_2623_NO_NATURAL_MARKER_AUDIT.csv"
CONSTRAINT_GATES_2263 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2263_CONSTRAINT_ALGEBRA_GATES.csv"


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


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(out)


def append_once(path: Path, marker: str, body: str) -> None:
    current = text(path)
    if marker in current:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="") as handle:
        if current and not current.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + body.strip() + "\n")


def source_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC4523_00_formal4522", "4522 formal handoff", FORMAL_4522, "PPC4161_RANK_M_LOCK_AND_RETAINED_CURRENT_FIREWALL_OR_ALPHA_RUNNER_4522", "rank/M theorem handoff"),
        ("SRC4523_01_post4522", "4522 post handoff", DOC_4522, "4523-Y5-R2FR-same-branch-parent-signature-audit-or-first-alpha-runner.md", "declared next target"),
        ("SRC4523_02_clauses4522", "4522 clause audit", CLAUSES_4522, "CLA4522_6_same_branch", "same-branch next gate"),
        ("SRC4523_03_fba4522", "4522 alpha/residual runner", FBA_4522, "FBA4522_1_finite_rank_alpha", "alpha runner contract"),
        ("SRC4523_04_firewall4522", "4522 retained current firewall", FIREWALL_4522, "RCF4522_7_verdict", "J_retained not closed"),
        ("SRC4523_05_decision4522", "4522 rank-zero decision", DECISION_4522, "RZD4522_4_current_verdict", "no claim verdict"),
        ("SRC4523_06_selector190", "parent selector quarantine", FORMAL_190, "PPC4161_PARENT_ACTION_SELECTOR_OR_LOCAL_QUARANTINE", "private selector theorem"),
        ("SRC4523_07_poynting191", "Maxwell-Hodge/Poynting owner", FORMAL_191, "PPC4161_MAXWELL_HODGE_POYNTING_STRESS_OWNER_THEOREM", "EM stress owner"),
        ("SRC4523_08_boundary192", "boundary no-flux", FORMAL_192, "PPC4161_LOCAL_BOUNDARY_NO_FLUX_SECTOR_INTERFACE_THEOREM", "boundary theorem"),
        ("SRC4523_09_qnat193", "quotient naturality", FORMAL_193, "PPC4161_QUOTIENT_NATURALITY_VERTICAL_SILENCE_THEOREM", "vertical silence"),
        ("SRC4523_10_kappa194", "calibrated source coupling", FORMAL_194, "PPC4161_CALIBRATED_SOURCE_COUPLING_KAPPA_TO_GN_LAW", "kappa-to-G law"),
        ("SRC4523_11_burden195", "local closure burden map", FORMAL_195, "PPC4161_LOCAL_GR_PRIVATE_CLOSURE_BURDEN_MAP", "parent adoption burden"),
        ("SRC4523_12_adoption196", "minimal parent adoption matrix", FORMAL_196, "PPC4161_MINIMAL_PARENT_ACTION_ADOPTION_MATRIX", "adoption verdicts"),
        ("SRC4523_13_parent_tests", "parent clause tests", PARENT_CLAUSE_TESTS, "CT552_7_no_cheat_policy", "policy pass, values missing"),
        ("SRC4523_14_parent_contract", "parent zero theorem contract", PARENT_ZERO_CONTRACT, "BZTC552_6_extra_sector_no_charge", "extra sector no-charge clause"),
        ("SRC4523_15_min_cases", "minimal parent test cases", MIN_PARENT_TEST_CASES, "EW538_C_residual_bound_branch", "residual-bound branch"),
        ("SRC4523_16_adoption2537", "adoption decision matrix", ADOPTION_2537, "ADM2537_3_decision", "adoption not claim-ready"),
        ("SRC4523_17_muc2537", "minimal universal matter coupling", MUC_2537, "MUC2537_6_verdict", "matter coupling branch verdict"),
        ("SRC4523_18_mca2587", "minimal parent matter adoption", MCA_2587, "AD2587_0_action_adoption", "matter action adoption gate"),
        ("SRC4523_19_dm2587", "domain motion rows", DM_2587, "DM2587_TOTAL", "matter-action obstruction total"),
        ("SRC4523_20_rank901", "local rank-zero certificate", LOCAL_RANK_901, "LRZ901_3_verdict", "rank-zero fails for claim"),
        ("SRC4523_21_notower2623", "no integrated-out tower audit", NO_TOWER_2623, "TOW2623_4_overall", "tower countermodels"),
        ("SRC4523_22_nomarker2623", "no natural marker audit", NO_MARKER_2623, "MRK2623_6_overall", "marker theorem not derived"),
        ("SRC4523_23_constraint2263", "constraint algebra gates", CONSTRAINT_GATES_2263, "CAG2263_6_verdict", "constraint algebra not closed"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, role, path, needle, note in specs:
        body = text(path)
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": source_id,
            "role": role,
            "path": str(path),
            "exists": path.exists(),
            "needle": needle,
            "needle_found": needle in body,
            "line": line_of(path, needle),
            "note": note,
            "valid_for_claim": False,
        })
    return rows


def parent_signature_rows() -> list[dict[str, object]]:
    return [
        {"signature_id": "PSA4523_0_selector_scope", "clause": "compact local <=2PN selector collar", "current_evidence": "190/192 define a private compact local collar with no-flux scope", "signature_status": "PRIVATE_CONDITIONAL_COMPATIBLE", "blocks_claim": "global adoption false", "valid_for_claim": False},
        {"signature_id": "PSA4523_1_EH_block", "clause": "EH/local metric principal block", "current_evidence": "196 marks EH/local principal block as hard root, not globally parent-derived", "signature_status": "UNSIGNED_EFFECTIVE_GR_ROOT", "blocks_claim": "principal block origin not derived from MTS", "valid_for_claim": False},
        {"signature_id": "PSA4523_2_Hilbert_source", "clause": "single q-basic Hilbert matter/EM source functor", "current_evidence": "190/191/194 give private Hilbert/Maxwell/kappa structure; 2537/2587 keep adoption false", "signature_status": "PRIVATE_CONDITIONAL_NOT_PARENT_SIGNED", "blocks_claim": "source-owner/no-source-slot gates remain open", "valid_for_claim": False},
        {"signature_id": "PSA4523_3_boundary", "clause": "boundary no-flux/routed charge", "current_evidence": "192 and 4521 supply conditional no-flux; parent tests keep boundary flux unclaimed", "signature_status": "PRIVATE_CONDITIONAL_NOT_GLOBAL", "blocks_claim": "boundary/cohomology and radiative clauses not globally signed", "valid_for_claim": False},
        {"signature_id": "PSA4523_4_quotient", "clause": "quotient naturality before variation", "current_evidence": "193 supplies exact private theorem; 196 calls it adoption axiom/closure until parent category", "signature_status": "ADOPTION_AXIOM_OR_CLOSURE", "blocks_claim": "q category and all-sector naturality not globally derived", "valid_for_claim": False},
        {"signature_id": "PSA4523_5_kappa", "clause": "calibrated universal kappa/G law", "current_evidence": "194 gives structural G_cal=c^4 kappa_eff/(8*pi), numeric G empirical", "signature_status": "STRUCTURAL_PRIVATE_NUMERIC_EMPIRICAL", "blocks_claim": "does not predict numerical G_N", "valid_for_claim": False},
        {"signature_id": "PSA4523_6_rankZ", "clause": "rank(Z_AB)=0 in physical quotient", "current_evidence": "4522 requires this; 901 rank certificate fails for claim", "signature_status": "UNSIGNED_BLOCKER", "blocks_claim": "rank-zero certificate absent", "valid_for_claim": False},
        {"signature_id": "PSA4523_7_Mlock", "clause": "M_AB coercive/invertible or constraint-owned", "current_evidence": "4522 derives lock theorem; 2263 constraint gates not closed; no m_min", "signature_status": "UNSIGNED_BLOCKER", "blocks_claim": "M lock/eigenvalue/constraint proof absent", "valid_for_claim": False},
        {"signature_id": "PSA4523_8_Jretained", "clause": "J_retained=0", "current_evidence": "4522 firewall; no-marker/no-tower/source-owner audits remain unsigned", "signature_status": "UNSIGNED_BLOCKER", "blocks_claim": "retained source channels remain live", "valid_for_claim": False},
        {"signature_id": "PSA4523_9_same_branch", "clause": "all clauses coexist in one parent branch", "current_evidence": "no file currently signs EH+Hilbert+boundary+quotient+rankZ+Mlock+Jretained together", "signature_status": "FAILS_FOR_CLAIM", "blocks_claim": "private closures are not one parent-signed theorem", "valid_for_claim": False},
    ]


def branch_compat_rows() -> list[dict[str, object]]:
    return [
        {"compat_id": "SBC4523_0_core_selector", "group": "PPC4161 local selector", "compatible_with_rank_zero": "yes as a private effective branch", "conflict_or_gap": "does not include a parent-owned Z algebraic sector", "result": "COMPATIBLE_INCOMPLETE", "valid_for_claim": False},
        {"compat_id": "SBC4523_1_EH_Hilbert_kappa", "group": "EH + Hilbert source + kappa", "compatible_with_rank_zero": "yes", "conflict_or_gap": "numeric G and EH origin remain empirical/effective", "result": "PRIVATE_COMPATIBLE", "valid_for_claim": False},
        {"compat_id": "SBC4523_2_boundary_qnat_readout", "group": "boundary + quotient naturality + readout", "compatible_with_rank_zero": "yes if same q-owned branch", "conflict_or_gap": "readout/projector/reduced-action counterbranches retained", "result": "CONDITIONAL", "valid_for_claim": False},
        {"compat_id": "SBC4523_3_rank_M", "group": "rank(Z)=0 + M_AB lock", "compatible_with_rank_zero": "required", "conflict_or_gap": "no same-branch parent signature or m_min/constraint closure", "result": "BLOCKER", "valid_for_claim": False},
        {"compat_id": "SBC4523_4_no_retained_current", "group": "J_retained firewall", "compatible_with_rank_zero": "required", "conflict_or_gap": "marker/tower/non-Hilbert/source-weight countermodels remain", "result": "BLOCKER", "valid_for_claim": False},
        {"compat_id": "SBC4523_5_overall", "group": "same-branch theorem", "compatible_with_rank_zero": "not yet proven", "conflict_or_gap": "enough private clauses exist to write a contract, not enough to claim derived local GR", "result": "FAIL_CLAIM_TRIGGER_RUNNER", "valid_for_claim": False},
    ]


def rz_action_rows() -> list[dict[str, object]]:
    return [
        {"contract_id": "RZPA4523_0_total_branch", "required_action_term": "S_parent|loc = S_PPC4161_selector + S_Z_alg + S_constraints + dB_qowned", "mathematical_role": "single action owns all clauses before readout", "current_status": "CONTRACT_WRITTEN_NOT_SOURCED", "if_missing": "private closures remain stitched, not claim-grade", "valid_for_claim": False},
        {"contract_id": "RZPA4523_1_no_Z_kinetic", "required_action_term": "S_Z_alg has no Z_AB nabla Z nabla Z principal symbol on Q_phys", "mathematical_role": "rank(Z_AB)=0", "current_status": "UNSIGNED", "if_missing": "finite-rank alpha(lambda) or spectral branch", "valid_for_claim": False},
        {"contract_id": "RZPA4523_2_M_lock", "required_action_term": "1/2 int sqrt(-g) Z^A M_AB(q) Z^B with M_AB coercive or constraint-owned", "mathematical_role": "M_AB Z^B=0 => Z=0 and finite bound uses m_min", "current_status": "UNSIGNED_NO_MMIN", "if_missing": "rank-zero route cannot close; bound needs m_min", "valid_for_claim": False},
        {"contract_id": "RZPA4523_3_no_source_vertex", "required_action_term": "no linear Z coupling to matter, EM, kappa, source normalization, readout, boundary, memory, marker or tower", "mathematical_role": "J_retained=B=CDB=R=0 in same branch", "current_status": "UNSIGNED_COUNTERMODELS_LIVE", "if_missing": "finite source/current residual rows", "valid_for_claim": False},
        {"contract_id": "RZPA4523_4_constraint_nulls", "required_action_term": "any null M directions are first/second-class constraints with differentiable charge, bracket preservation, boundary silence and reduced nondegeneracy", "mathematical_role": "prevents null M from becoming underdetermined physics", "current_status": "UNSIGNED_2263_NOT_CLOSED", "if_missing": "reject null branch or score residuals", "valid_for_claim": False},
        {"contract_id": "RZPA4523_5_readout_order", "required_action_term": "q/readout/support/projector fixed before variation or postprocess only", "mathematical_role": "prevents readout reentry", "current_status": "CONDITIONAL_NOT_GLOBAL", "if_missing": "readout residual runner", "valid_for_claim": False},
        {"contract_id": "RZPA4523_6_decision", "required_action_term": "current corpus source for RZPA4523_0-5", "mathematical_role": "claim gate", "current_status": "NOT_FOUND", "if_missing": "trigger first alpha/residual runner", "valid_for_claim": False},
    ]


def runner_trigger_rows() -> list[dict[str, object]]:
    return [
        {"trigger_id": "RTR4523_0_same_branch", "test": "Do all 4520-4522 clauses have one parent action source?", "result": "FAIL_FOR_CLAIM", "reason": "selector exists privately, but rankZ/M/Jretained source clauses are not signed", "runner_action": "activate finite residual/alpha dry runner", "valid_for_claim": False},
        {"trigger_id": "RTR4523_1_rank_zero_bound", "test": "Can rank-zero residual bound run numerically?", "result": "DRYRUN_BLOCKED", "reason": "m_min(M_AB), J_retained, B, CDB, R norms and K_obs missing", "runner_action": "write source input pack", "valid_for_claim": False},
        {"trigger_id": "RTR4523_2_finite_alpha", "test": "Can alpha(lambda) run numerically?", "result": "DRYRUN_BLOCKED", "reason": "Z/M/Q_source/q_test/calibration/full bound curve missing", "runner_action": "write alpha input pack", "valid_for_claim": False},
        {"trigger_id": "RTR4523_3_parent_Z_action", "test": "Could next work still prove parent Z action?", "result": "YES_BUT_SOURCE_REQUIRED", "reason": "contract RZPA4523 supplies exact action signature to hunt", "runner_action": NEXT_TARGET, "valid_for_claim": False},
    ]


def runner_input_rows() -> list[dict[str, object]]:
    rows = [
        {"input_id": "AIR4523_0_mmin", "runner": "rank_zero_bound", "quantity": "m_min(M_AB)", "required_evidence": "parent action Hessian/eigenvalue or constraint Schur complement", "current_status": "MISSING", "valid_for_claim": False},
        {"input_id": "AIR4523_1_Jretained_norm", "runner": "rank_zero_bound", "quantity": "||J_retained||", "required_evidence": "zero theorem or source-backed retained-current profile", "current_status": "MISSING", "valid_for_claim": False},
        {"input_id": "AIR4523_2_B_norm", "runner": "rank_zero_bound", "quantity": "||B_A||", "required_evidence": "boundary no-flux theorem in same branch or boundary flux profile", "current_status": "MISSING_SAME_BRANCH", "valid_for_claim": False},
        {"input_id": "AIR4523_3_CDB_norm", "runner": "rank_zero_bound", "quantity": "||C_A^CDB||", "required_evidence": "component zeros or K_conn/K_domain/K_boundary/K_comm norms", "current_status": "MISSING", "valid_for_claim": False},
        {"input_id": "AIR4523_4_R_norm", "runner": "rank_zero_bound", "quantity": "||R_A||", "required_evidence": "pure postprocess/readout theorem in same branch or readout reentry bound", "current_status": "MISSING_SAME_BRANCH", "valid_for_claim": False},
        {"input_id": "AIR4523_5_Kobs", "runner": "rank_zero_bound", "quantity": "K_obs projection to PPN/R10/clock/orbit", "required_evidence": "arena transfer operator", "current_status": "MISSING", "valid_for_claim": False},
    ]
    for row in read_csv(FBA_4522):
        if row.get("runner_id", "").startswith("FBA4522_") and "alpha input inherited" in row.get("case", ""):
            rows.append({
                "input_id": row["runner_id"].replace("FBA4522", "AIR4523"),
                "runner": "finite_alpha",
                "quantity": row["bound_formula"],
                "required_evidence": row["required_inputs"],
                "current_status": row["current_status"],
                "valid_for_claim": False,
            })
    return rows


def decision_rows() -> list[dict[str, object]]:
    return [
        {"decision_id": "DEC4523_0", "decision": DECISION, "meaning": "same-branch parent signature is not claim-grade; rank-zero action contract is now explicit; alpha/residual runner is triggered but dry-run blocked pending source inputs", "next_target": NEXT_TARGET, "valid_for_claim": False}
    ]


def claim_rows() -> list[dict[str, object]]:
    return [
        {"gate_id": "CG4523_0_same_branch", "claim": "same-branch parent signature closes", "passed": False, "blocker": "no parent source signs EH+Hilbert+boundary+quotient+rankZ+Mlock+Jretained together", "valid_for_claim": False},
        {"gate_id": "CG4523_1_rank_zero", "claim": "rank-zero local residual vanishes", "passed": False, "blocker": "rankZ/M/Jretained clauses unsigned", "valid_for_claim": False},
        {"gate_id": "CG4523_2_alpha_runner", "claim": "alpha/residual runner score-ready", "passed": False, "blocker": "numeric/source-backed input rows missing", "valid_for_claim": False},
        {"gate_id": "CG4523_3_local_GR", "claim": "local GR/Newton/PPN pass", "passed": False, "blocker": "parent signature and empirical score gates remain incomplete", "valid_for_claim": False},
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "same-branch audit; explicit rank-zero parent action contract; first alpha/residual runner trigger and source input pack",
            "not_derived": "parent-signed rankZ/M/Jretained same-branch theorem; numeric alpha/residual score",
            "claim_status": "NONCLAIM",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated": now(),
        }
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NT4523_0",
            "target_file": NEXT_TARGET,
            "task": "either source the parent Z algebraic action signature RZPA4523 or run the first finite residual/alpha smoke runner using the input pack written here",
        }
    ]


def validate(sources: list[dict[str, object]], parent: list[dict[str, object]], compat: list[dict[str, object]], action: list[dict[str, object]], triggers: list[dict[str, object]], inputs: list[dict[str, object]], claims: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append({"validation_id": validation_id, "status": "PASS" if ok else "FAIL", "detail": detail})

    add("VAL4523_00_sources", all(row["exists"] and row["needle_found"] for row in sources), "all source paths exist and source needles are found")
    add("VAL4523_01_parent_audit", any(row["signature_id"] == "PSA4523_9_same_branch" and row["signature_status"] == "FAILS_FOR_CLAIM" for row in parent), "same-branch parent signature fails for claim")
    add("VAL4523_02_compat", any(row["compat_id"] == "SBC4523_5_overall" and row["result"] == "FAIL_CLAIM_TRIGGER_RUNNER" for row in compat), "compatibility matrix triggers runner")
    add("VAL4523_03_action_contract", any(row["contract_id"] == "RZPA4523_6_decision" and row["current_status"] == "NOT_FOUND" for row in action), "rank-zero parent action source not found")
    add("VAL4523_04_runner_trigger", any(row["trigger_id"] == "RTR4523_1_rank_zero_bound" for row in triggers) and any(row["trigger_id"] == "RTR4523_2_finite_alpha" for row in triggers), "rank-zero and finite-alpha runner triggers exist")
    add("VAL4523_05_inputs", any(row["input_id"] == "AIR4523_0_mmin" for row in inputs) and any(row["runner"] == "finite_alpha" for row in inputs), "residual and alpha input rows exist")
    add("VAL4523_06_claims_blocked", all(str(row["passed"]).lower() == "false" and str(row["valid_for_claim"]).lower() == "false" for row in claims), "all claim gates remain blocked")
    csv_paths = [SOURCE_REGISTER, PARENT_SIGNATURE, BRANCH_COMPAT, RZ_ACTION_CONTRACT, RUNNER_TRIGGER, RUNNER_INPUTS, DECISION_CSV, CLAIM_GATES, STATUS_CSV, NEXT_CSV]
    parse_ok = True
    detail = []
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            detail.append(f"{path.name}:{len(parsed)}")
        except Exception as exc:  # noqa: BLE001
            parse_ok = False
            detail.append(f"{path.name}:{exc}")
    add("VAL4523_07_csv_parse", parse_ok, ";".join(detail))
    add("VAL4523_08_next_target", NEXT_TARGET in text(NEXT_CSV), NEXT_TARGET)
    add("VAL4523_09_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after cleanup")
    add("VAL4523_OVERALL", all(row["status"] == "PASS" for row in rows), "4523 same-branch parent signature audit or first alpha runner")
    return rows


def build_doc(sources: list[dict[str, object]], parent: list[dict[str, object]], compat: list[dict[str, object]], action: list[dict[str, object]], triggers: list[dict[str, object]], inputs: list[dict[str, object]], decision: list[dict[str, object]], claims: list[dict[str, object]], status: list[dict[str, object]], next_target: list[dict[str, object]], validation: list[dict[str, object]]) -> str:
    return f"""# 4523 - Same-Branch Parent Signature Audit Or First Alpha Runner

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4522 gave the full conditional theorem. 4523 asks the hard question: are those clauses signed by one parent branch?

Current answer: **not claim-grade**.

The PPC4161 selector is compatible with the local branch as a private effective-GR selector, and it already contains strong EH/Hilbert/EM/boundary/quotient/kappa pieces. But the current corpus does not sign the extra rank-zero requirements in the same parent action:

- `rank(Z_AB)=0`;
- locked/coercive `M_AB` or constraint-owned nulls;
- `J_retained=0` against non-Hilbert, marker, kernel, tower, readout, calibration and source-worldtube counterbranches.

So 4523 writes the exact parent action contract that would make the theorem real, then triggers the finite residual/alpha runner path. The runner is deliberately dry-run blocked until the source-backed inputs exist. No local-GR claim is promoted.

## Source Register

{table(sources)}

## Parent Signature Audit

{table(parent)}

## Same-Branch Compatibility Matrix

{table(compat)}

## Rank-Zero Parent Action Contract

{table(action)}

## First Alpha/Residual Runner Trigger

{table(triggers)}

## First Alpha Runner Inputs

{table(inputs)}

## Decision

{table(decision)}

## Claim Gates

{table(claims)}

## Status

{table(status)}

## Next Target

{table(next_target)}

## Validation

{table(validation)}
"""


def append_claim_once() -> None:
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_r2fr_same_branch_signature",
        "claim": "4523 audits same-branch parent-signature compatibility for the rank-zero local theorem, finds claim-grade signing absent, writes the exact parent Z-action contract, and triggers finite alpha/residual runner inputs.",
        "current_evidence": "Generated parent signature audit, same-branch compatibility matrix, RZ parent action contract, runner trigger/input CSVs, and validation P8_Y5_BRR545_4523_VALIDATION.csv.",
        "status": "conditional_internal_nonclaim_runner_triggered",
        "next_test": NEXT_TARGET,
        "key_risk": "Using private selector compatibility as parent-signed local GR; alpha/residual inputs remain missing.",
        "sector": "local_gr_newton",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "If parent Z-action signature cannot be sourced, the branch must be tested by finite residual/alpha scoring.",
    }
    if not CLAIMS_PATH.exists():
        write_csv(CLAIMS_PATH, [row])
        return
    existing = read_csv(CLAIMS_PATH)
    if any(existing_row.get("claim_id") == CLAIM_ID for existing_row in existing):
        return
    headers = list(existing[0].keys()) if existing else list(row.keys())
    with CLAIMS_PATH.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writerow({header: row.get(header, "") for header in headers})


def main() -> None:
    sources = source_rows()
    parent = parent_signature_rows()
    compat = branch_compat_rows()
    action = rz_action_rows()
    triggers = runner_trigger_rows()
    inputs = runner_input_rows()
    decision = decision_rows()
    claims = claim_rows()
    status = status_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PARENT_SIGNATURE, parent)
    write_csv(BRANCH_COMPAT, compat)
    write_csv(RZ_ACTION_CONTRACT, action)
    write_csv(RUNNER_TRIGGER, triggers)
    write_csv(RUNNER_INPUTS, inputs)
    write_csv(DECISION_CSV, decision)
    write_csv(CLAIM_GATES, claims)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, parent, compat, action, triggers, inputs, claims)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, parent, compat, action, triggers, inputs, decision, claims, status, next_target, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4523 Same-Branch Parent Signature Audit Or First Alpha Runner

Marker: `{MARKER}`  
4523 audits whether the complete conditional rank-zero theorem from 4522 is signed by one parent branch. It is not claim-grade: the PPC4161 selector is privately compatible, but `rank(Z_AB)=0`, the `M_AB` lock and `J_retained=0` are not sourced in the same parent action. The exact `S_Z_alg` parent-action contract is now written; absent that source, the finite residual/alpha runner path is triggered.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4523 Packet Integration

Marker: `{PACKET_MARKER}`  
The packet now has a hard fork: either source the parent algebraic `Z` action contract, or run finite residual/alpha scoring from the 4523 input pack. This prevents the private selector from being mistaken for a parent-signed local-GR proof. Next target: `{NEXT_TARGET}`.
""",
    )
    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
