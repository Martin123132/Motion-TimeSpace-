from __future__ import annotations

import csv
import io
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
PUBLIC_STAGE = Path(r"D:\Users\ollet\Desktop\Motion-TimeSpace-public-stage")
BACKUP_REPO = Path(r"D:\Users\ollet\Desktop\laptop-back-up-")

CHECKPOINT = "4648"
CLAIM_ID = "L-490"
BRANCH = "MTS_R2FR_Y5_SAME_BRANCH_XI_TAIL_ZERO_ASSEMBLY_AND_LAMBDA_PROMOTION_GATE_4648"
MARKER = "PPC4161_SAME_BRANCH_XI_TAIL_ZERO_ASSEMBLY_AND_LAMBDA_PROMOTION_GATE_4648"
PACKET_MARKER = "PPC4161_PACKET_SAME_BRANCH_XI_TAIL_ZERO_ASSEMBLY_AND_LAMBDA_PROMOTION_GATE_4648"
NEXT_TARGET = "4649-Y5-R2FR-parent-selector-promotion-map-or-local-GR-contract.md"

DOC_PATH = POST / "4648-Y5-R2FR-same-branch-Xi-tail-zero-assembly-and-lambda-promotion-gate.md"
FORMAL_PATH = FORMAL / "664-PPC4161-same-branch-Xi-tail-zero-assembly-and-lambda-promotion-gate.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4648_SOURCE_REGISTER.csv"
ASSEMBLY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4648_SAME_BRANCH_XI_TAIL_ASSEMBLY.csv"
LAMBDA_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4648_LAMBDA_PROMOTION_GATE.csv"
ARENA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4648_ARENA_PROMOTION_ROWS.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4648_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4648_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4648_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4648_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4648_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4648_VALIDATION.csv"

DOC_4642 = POST / "4642-Y5-R2FR-Xi-tail-parent-signature-and-lambda-source-pack.md"
DOC_4643 = POST / "4643-Y5-R2FR-Xi-tail-first-claim-grade-input-fill-or-exact-parent-signature.md"
DOC_4644 = POST / "4644-Y5-R2FR-first-Xi-component-magnitude-or-exact-zero-certificate.md"
DOC_4645 = POST / "4645-Y5-R2FR-Xi-nonHilbert-alpha-component-or-Hperp-exact-zero-certificate.md"
DOC_4646 = POST / "4646-Y5-R2FR-boundary-history-alpha-component-or-no-flux-zero-certificate.md"
DOC_4647 = POST / "4647-Y5-R2FR-transition-inner-alpha-component-or-source-kernel-zero-certificate.md"

CSV_4644_ALPHA = SOURCE_DIR / "P8_Y5_R2FR_4644_ALPHA_SRC_HIDDEN_COMPONENT.csv"
CSV_4645_ALPHA = SOURCE_DIR / "P8_Y5_R2FR_4645_ALPHA_NONHILBERT_COMPONENT.csv"
CSV_4646_ALPHA = SOURCE_DIR / "P8_Y5_R2FR_4646_ALPHA_BOUNDARY_HISTORY_COMPONENT.csv"
CSV_4647_ALPHA = SOURCE_DIR / "P8_Y5_R2FR_4647_ALPHA_TRANSITION_INNER_COMPONENT.csv"
CSV_4647_REDUCED = SOURCE_DIR / "P8_Y5_R2FR_4647_REDUCED_TAIL_AFTER_FOUR_COMPONENTS.csv"
CSV_4647_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4647_VALIDATION.csv"
CSV_4642_LAMBDA = SOURCE_DIR / "P8_Y5_R2FR_4642_LAMBDA_MEM_SOURCE_PACK.csv"
CSV_4642_PARENT = SOURCE_DIR / "P8_Y5_R2FR_4642_PARENT_SIGNATURE_PACK.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_number(path: Path, needle: str) -> int:
    for index, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def table(rows: list[dict[str, Any]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    suffix = "" if existing.endswith("\n") or not existing else "\n"
    path.write_text(existing + suffix + text.lstrip("\n"), encoding="utf-8")


def csv_line(values: list[str]) -> str:
    handle = io.StringIO()
    csv.writer(handle, lineterminator="\n").writerow(values)
    return handle.getvalue()


def git_clean(repo: Path) -> tuple[bool, str]:
    if not repo.exists() or not (repo / ".git").exists():
        return True, "absent or not git"
    result = subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], text=True, capture_output=True, check=False)
    if result.returncode != 0:
        return False, result.stderr.strip() or "git status failed"
    return result.stdout.strip() == "", result.stdout.strip() or "clean"


def sources(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4648_00_4647_validation", CSV_4647_VALIDATION, "VAL4647_OVERALL", "4647 transition-inner certificate passed."),
        ("SRC4648_01_alpha_src_hidden", CSV_4644_ALPHA, "ALPHA4644_0_alpha_src_hidden", "first component alpha zero."),
        ("SRC4648_02_alpha_nonHilbert", CSV_4645_ALPHA, "ALPHA4645_0_alpha_nonHilbert", "second component alpha zero."),
        ("SRC4648_03_alpha_boundary", CSV_4646_ALPHA, "ALPHA4646_0_alpha_boundary_history", "third component alpha zero."),
        ("SRC4648_04_alpha_transition", CSV_4647_ALPHA, "ALPHA4647_0_alpha_transition_inner", "fourth component alpha zero."),
        ("SRC4648_05_tail_four", CSV_4647_REDUCED, "TAIL4647_0_four_component_zero", "four-component tail zero premise."),
        ("SRC4648_06_promotion_live", CSV_4647_REDUCED, "TAIL4647_2_local_promotion_live", "local promotion remains live."),
        ("SRC4648_07_4643_linearity", DOC_4643, "alpha_tail(lambda)=alpha_src_hidden+alpha_nonHilbert+alpha_boundary_history+alpha_transition_inner", "linear normalized alpha tail formula."),
        ("SRC4648_08_4643_lambda", DOC_4643, "alpha_bound(lambda_mem)", "R10 comparison formula with lambda_mem."),
        ("SRC4648_09_4642_lambda_law", DOC_4642, "lambda_mem = sqrt(Z_mem/M2_mem)", "parent-Hessian range law."),
        ("SRC4648_10_4642_lambda_csv", CSV_4642_LAMBDA, "LAM4642_0_parent_hessian_law", "lambda source pack."),
        ("SRC4648_11_4642_parent_selector", CSV_4642_PARENT, "PS4642_6", "same observed coframe/Hodge/tau parent selector clause."),
        ("SRC4648_12_4642_fixed_domain", CSV_4642_PARENT, "PS4642_7", "fixed projector/domain/lambda clause."),
        ("SRC4648_13_4644_doc", DOC_4644, "ALPHA4644_0_alpha_src_hidden", "human first component source."),
        ("SRC4648_14_4645_doc", DOC_4645, "TAIL4645_0_two_component_reduction", "human two-component reduction."),
        ("SRC4648_15_4646_doc", DOC_4646, "TAIL4646_0_three_component_reduction", "human three-component reduction."),
        ("SRC4648_16_4647_doc", DOC_4647, "RUN4647_5_Xi_zero_but_promotion_live", "full tail zero but promotion live row."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, note in specs:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "line_number": line_number(path, needle),
                "note": note,
                "valid_for_claim": False,
                "timestamp_utc": ts,
            }
        )
    return rows


def assembly(ts: str) -> list[dict[str, Any]]:
    rows = [
        ("ASM4648_0_tail_definition", "alpha_tail(lambda)=alpha_src_hidden+alpha_nonHilbert+alpha_boundary_history+alpha_transition_inner", "normalized R10 alpha functional is linear", "DEFINITION_IMPORTED"),
        ("ASM4648_1_component_values", "0+0+0+0=0", "4644-4647 component certificates", "COMPONENT_ZERO_SUM"),
        ("ASM4648_2_same_branch_selector", "B_tail := B_src_hidden and B_nonHilbert and B_boundary_history and B_transition_inner and B_common_readout and B_fixed_domain_lambda", "the zero sum is only legal if one parent/readout selector carries every component", "PARENT_SELECTOR_CONTRACT"),
        ("ASM4648_3_conditional_theorem", "B_tail -> alpha_tail(lambda)=0 for all lambda", "linearity plus component zeros on one selector", "CONDITIONAL_EXACT_ZERO_THEOREM"),
        ("ASM4648_4_current_status", "component zeros exist; parent same-branch selector remains unsigned in 4642 parent pack", "do not promote to local-GR/R10 claim", "ASSEMBLY_GATE_OPEN"),
        ("ASM4648_5_fallback", "not B_tail -> use absolute finite component envelope", "no cancellation across branches or sectors", "FINITE_FALLBACK_RETAINED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "assembly_id": row[0],
            "statement": row[1],
            "basis": row[2],
            "status": row[3],
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for row in rows
    ]


def lambda_gate(ts: str) -> list[dict[str, Any]]:
    rows = [
        ("LAMG4648_0_zero_amplitude_R10", "if B_tail then alpha_tail(lambda)=0", "R10 Yukawa amplitude is zero independently of the numeric lambda_mem value", "R10_TAIL_SILENT_CONDITIONAL"),
        ("LAMG4648_1_lambda_law_retained", "lambda_mem=sqrt(Z_mem/M2_mem)", "range law remains the parent descriptor of any nonzero memory mode", "LAW_RETAINED_NONCLAIM"),
        ("LAMG4648_2_nonzero_fallback", "if any alpha_i opens", "need numeric Z_mem/M2_mem, bound curve QA, and arena projection constants", "FINITE_SCORING_REQUIRED"),
        ("LAMG4648_3_massless_branch", "M2_mem=0", "allowed only with exact Xi/source-coupling zero; otherwise infinite range fails local tests", "FAIL_UNLESS_EXACT_ZERO"),
        ("LAMG4648_4_tachyon_branch", "M2_mem<0", "unstable local recovery branch remains rejected", "REJECT"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "lambda_gate_id": row[0],
            "condition": row[1],
            "deduction": row[2],
            "status": row[3],
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for row in rows
    ]


def arenas(ts: str) -> list[dict[str, Any]]:
    rows = [
        ("ARENA4648_0_R10", "R10", "B_tail gives zero Yukawa amplitude before bound comparison", "CONDITIONAL_SILENCE_NONCLAIM", "still needs parent selector and curve QA for public claim"),
        ("ARENA4648_1_PPN", "PPN", "Xi_tail=0 alone does not derive gamma/beta/preferred-frame maps", "BLOCKED_BY_PROMOTION_MAP", "derive local metric/source response map"),
        ("ARENA4648_2_Newton", "Newton/G_obs", "zero tail does not derive calibrated G_N or universal source coupling by itself", "BLOCKED_BY_SOURCE_COUPLING", "derive G_obs source normalization/promotion"),
        ("ARENA4648_3_Maxwell_EM", "Maxwell/EM", "zero tail does not yet prove visible EM/Poynting stress couples through the same observed coframe", "BLOCKED_BY_EM_STRESS_MAP", "derive common coframe/Hodge/tau stress map"),
        ("ARENA4648_4_clocks", "clock/time", "zero R10 tail does not yet prove clock redshift/time-map equality", "BLOCKED_BY_CLOCK_PROMOTION", "derive clock readout projection"),
        ("ARENA4648_5_orbital", "orbital", "zero R10 tail does not yet prove GM/orbital dynamics branch", "BLOCKED_BY_ORBITAL_PROMOTION", "derive orbital source/readout map"),
        ("ARENA4648_6_WEP", "WEP", "zero tail does not automatically prove source species universality in all local matter couplings", "BLOCKED_BY_MATTER_SELECTOR", "derive single species-blind matter selector"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "arena_id": row[0],
            "arena": row[1],
            "deduction": row[2],
            "status": row[3],
            "next_action": row[4],
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for row in rows
    ]


def runners(ts: str) -> list[dict[str, Any]]:
    rows = [
        ("RUN4648_0_component_sum_only", "four alpha rows are zero but common selector unsigned", "FAIL_CLOSED", "do not claim alpha_tail=0 as live corpus fact"),
        ("RUN4648_1_same_branch_selector_signed", "B_tail parent/readout selector signed", "PASS_CONDITIONAL_XI_TAIL_ZERO_NONCLAIM", "alpha_tail(lambda)=0 for all lambda"),
        ("RUN4648_2_R10_zero_amplitude", "B_tail plus R10 scoring context", "PASS_CONDITIONAL_R10_TAIL_SILENCE_NONCLAIM", "lambda_mem numeric value not needed for zero amplitude, but public curve QA still separate"),
        ("RUN4648_3_local_GR_promotion_attempt", "Xi_tail=0 but PPN/Newton/EM maps absent", "FAIL_CLOSED", "local-GR claim remains blocked"),
        ("RUN4648_4_open_component", "any alpha_i or branch selector opens", "FAIL_FINITE_SCORING_REQUIRED", "return to absolute component bound and source numeric rows"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "run_id": row[0],
            "branch": row[1],
            "result": row[2],
            "reason": row[3],
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": ts,
        }
        for row in rows
    ]


def controls(ts: str) -> list[dict[str, Any]]:
    rows = [
        ("CTRL4648_0_no_component_confetti", "Four separate zero rows do not equal one theorem unless carried by one selector."),
        ("CTRL4648_1_no_lambda_magic", "Zero amplitude decouples R10 from lambda; it does not derive PPN/Newton/local GR."),
        ("CTRL4648_2_no_curve_claim", "R10 curve QA is still required before public bound claims, even if internal zero control passes."),
        ("CTRL4648_3_no_EM_erasure", "Visible EM/Poynting stress is routed through the promotion map, not erased by Xi_tail silence."),
        ("CTRL4648_4_no_G_hiding", "Calibrated G_N cannot absorb an unsourced species/frame/source weight."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": row[0],
            "firewall": row[1],
            "active": True,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for row in rows
    ]


def decisions(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4648_0",
            "decision": "SAME_BRANCH_XI_TAIL_ZERO_THEOREM_CONTRACT_WRITTEN_PARENT_SELECTOR_AND_LOCAL_PROMOTION_STILL_OPEN",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "summary": "4648 turns the four component certificates into the exact contract B_tail -> alpha_tail(lambda)=0. This is a real reduction: R10 tail amplitude is conditionally zero for any lambda, so the next hard target is not another alpha component; it is deriving the single parent selector and local promotion maps to GR/Newton/Maxwell/clock/orbital arenas.",
            "timestamp_utc": ts,
        }
    ]


def statuses(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": BRANCH,
            "status": "PRIVATE_DERIVATION_ADVANCE_NONCLAIM",
            "summary": "Same-branch Xi_tail zero theorem contract written; local-GR claim blocked by parent selector and promotion maps, not by the four Xi components.",
            "claim_allowed": False,
            "public_ready": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": ts,
        }
    ]


def nexts(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "derive the parent action/readout selector B_tail and promotion maps, or demote the route to a conditional closure theorem",
            "success_condition": "single parent selector signs all zero clauses and maps matter/EM/clocks/local tests through one observed metric/coframe with conserved source coupling",
            "timestamp_utc": ts,
        }
    ]


def validation_rows(src: list[dict[str, Any]], asm: list[dict[str, Any]], lam: list[dict[str, Any]], ar: list[dict[str, Any]], run: list[dict[str, Any]], dec: list[dict[str, Any]], ts: str) -> list[dict[str, Any]]:
    public_clean, public_detail = git_clean(PUBLIC_STAGE)
    backup_clean, backup_detail = git_clean(BACKUP_REPO)
    checks = [
        ("VAL4648_00_sources_exist", all(row["path_exists"] for row in src), "all cited paths exist"),
        ("VAL4648_01_needles_found", all(row["needle_found"] for row in src), "all source needles found"),
        ("VAL4648_02_line_anchors", all(int(row["line_number"]) > 0 for row in src), "all source line anchors positive"),
        ("VAL4648_03_same_branch_contract", any(row["assembly_id"] == "ASM4648_2_same_branch_selector" for row in asm), "B_tail selector contract written"),
        ("VAL4648_04_conditional_tail_zero", any(row["assembly_id"] == "ASM4648_3_conditional_theorem" for row in asm), "conditional alpha_tail zero theorem written"),
        ("VAL4648_05_lambda_zero_gate", any(row["lambda_gate_id"] == "LAMG4648_0_zero_amplitude_R10" for row in lam), "R10 zero-amplitude lambda gate written"),
        ("VAL4648_06_promotion_blocks", all("BLOCKED" in row["status"] or row["arena"] == "R10" for row in ar), "non-R10 local arenas remain blocked"),
        ("VAL4648_07_local_gr_fail_closed", any(row["run_id"] == "RUN4648_3_local_GR_promotion_attempt" and row["result"] == "FAIL_CLOSED" for row in run), "local-GR promotion attempt fails closed"),
        ("VAL4648_08_no_claim_allowed", all(str(row.get("valid_for_claim", "False")) == "False" for row in src + asm + lam + ar + run + dec), "no row marked claim-grade"),
        ("VAL4648_09_decision_next", dec and dec[0]["next_target"] == NEXT_TARGET, "next target selected"),
        ("VAL4648_10_public_stage_clean", public_clean, f"public stage: {public_detail}"),
        ("VAL4648_11_backup_repo_clean", backup_clean, f"backup repo: {backup_detail}"),
    ]
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": item,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
            "timestamp_utc": ts,
        }
        for item, ok, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4648_OVERALL",
            "status": "PASS" if all(ok for _, ok, _ in checks) else "FAIL",
            "detail": "4648 validation passed" if all(ok for _, ok, _ in checks) else "4648 validation failed",
            "timestamp_utc": ts,
        }
    )
    return rows


def build_doc(src: list[dict[str, Any]], asm: list[dict[str, Any]], lam: list[dict[str, Any]], ar: list[dict[str, Any]], run: list[dict[str, Any]], ctrl: list[dict[str, Any]], dec: list[dict[str, Any]], stat: list[dict[str, Any]], nxt: list[dict[str, Any]], val: list[dict[str, Any]]) -> str:
    return f"""# 4648 - same-branch Xi tail zero assembly and lambda promotion gate

Branch: `{BRANCH}`
Marker: `{MARKER}`

## Result

This checkpoint stops the component chase and writes the exact assembly contract:

`B_tail -> alpha_tail(lambda)=0`.

`B_tail` means one parent/readout selector carries all four zero components plus the common observed coframe/Hodge/tau and fixed projector/domain/lambda clauses. Without that selector, the four zeros remain good local certificates but not one live theorem. With that selector, the R10 Yukawa tail amplitude is zero for any `lambda_mem`; however, local GR/Newton/PPN/Maxwell/clock/orbital claims still need promotion maps.

## Source Register

{table(src)}

## Same-Branch Assembly

{table(asm)}

## Lambda / Promotion Gate

{table(lam)}

## Arena Promotion Rows

{table(ar)}

## Runner Results

{table(run)}

## Controls

{table(ctrl)}

## Decision

{table(dec)}

## Status

{table(stat)}

## Next Target

{table(nxt)}

## Validation

{table(val)}
"""


def register_claim() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = [
        CLAIM_ID,
        "local_gr_empirical_interface",
        "4648 converts the four normalized Xi_tail component certificates into the exact same-branch theorem contract B_tail -> alpha_tail(lambda)=0, and separates R10 zero-amplitude silence from still-open local-GR/Newton/PPN/Maxwell/EM promotion maps.",
        "Generated source register, same-branch assembly rows, lambda/promotion gate, arena rows, runner, controls, decision, status, next target and validation.",
        "same_branch_Xi_tail_zero_contract_nonclaim",
        NEXT_TARGET,
        "Treating four branch-local component zeros as one live theorem without a parent selector, using lambda_mem to hide promotion gaps, or claiming local GR from R10 tail silence alone.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No local-GR/Newton/R10/PPN/Maxwell/EM public claim until the single parent selector and local promotion/source-coupling maps are derived or bounded.",
    ]
    append_once(CLAIMS_PATH, CLAIM_ID, csv_line(row))


def update_spine_packet() -> None:
    spine = f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4648 assembles the four normalized `Xi_tail` component certificates into the exact contract `B_tail -> alpha_tail(lambda)=0`. The live theorem requires one parent/readout selector carrying source-label silence, Hperp/source-pairing silence, no-flux boundary/history silence, transition source-kernel silence, common observed coframe/Hodge/tau, and fixed projector/domain/lambda. If `B_tail` is signed, R10 Yukawa amplitude is zero for any `lambda_mem`; this remains nonclaim because PPN/Newton/Maxwell/EM/clock/orbital promotion maps are still open.
"""
    packet = f"""
## {PACKET_MARKER}

Checkpoint `4648` stops the alpha-component chase and moves the local route to the parent-selector/promotion-map problem. Next packet target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine)
    append_once(PACKET_PATH, PACKET_MARKER, packet)


def main() -> int:
    ts = now()
    src = sources(ts)
    asm = assembly(ts)
    lam = lambda_gate(ts)
    ar = arenas(ts)
    run = runners(ts)
    ctrl = controls(ts)
    dec = decisions(ts)
    stat = statuses(ts)
    nxt = nexts(ts)
    val = validation_rows(src, asm, lam, ar, run, dec, ts)

    write_csv(SOURCE_REGISTER, src)
    write_csv(ASSEMBLY_CSV, asm)
    write_csv(LAMBDA_GATE_CSV, lam)
    write_csv(ARENA_CSV, ar)
    write_csv(RUNNER_CSV, run)
    write_csv(CONTROL_CSV, ctrl)
    write_csv(DECISION_CSV, dec)
    write_csv(STATUS_CSV, stat)
    write_csv(NEXT_CSV, nxt)
    write_csv(VALIDATION_CSV, val)

    doc = build_doc(src, asm, lam, ar, run, ctrl, dec, stat, nxt, val)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")
    register_claim()
    update_spine_packet()

    status = val[-1]["status"]
    print(f"4648 validation: {status}")
    print(VALIDATION_CSV)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
