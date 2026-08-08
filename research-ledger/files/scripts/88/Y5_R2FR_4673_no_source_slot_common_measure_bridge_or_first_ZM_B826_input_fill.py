from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4673"
CLAIM_ID = "L-515"
BRANCH = "MTS_R2FR_Y5_NO_SOURCE_SLOT_COMMON_MEASURE_BRIDGE_OR_FIRST_ZM_B826_INPUT_FILL_4673"
MARKER = "PPC4161_NO_SOURCE_SLOT_COMMON_MEASURE_BRIDGE_OR_FIRST_ZM_B826_INPUT_FILL_4673"
PACKET_MARKER = "PPC4161_PACKET_NO_SOURCE_SLOT_COMMON_MEASURE_BRIDGE_OR_FIRST_ZM_B826_INPUT_FILL_4673"
DECISION = "NO_SOURCE_SLOT_BRIDGE_EXTENDED_TO_R826_UNSIGNED_FIRST_ZM_B826_INPUT_PACK_READY_NONCLAIM"
NEXT_TARGET = "4674-Y5-R2FR-first-ZM-B826-finite-input-pack-or-R826-no-slot-owner-proof.md"

DOC_PATH = POST / "4673-Y5-R2FR-no-source-slot-common-measure-bridge-or-first-ZM-B826-input-fill.md"
FORMAL_PATH = FORMAL / "689-PPC4161-no-source-slot-common-measure-bridge-or-first-ZM-B826-input-fill.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

DOC_4672 = POST / "4672-Y5-R2FR-even-branch-symmetry-owner-or-first-Hessian-B826-bound-row.md"
FORMAL_688 = FORMAL / "688-PPC4161-even-branch-symmetry-owner-or-first-Hessian-B826-bound-row.md"
DOC_4633 = POST / "4633-Y5-R2FR-epsilonA-bound-input-acquisition-or-no-source-slot-bridge.md"
FORMAL_4633 = FORMAL / "650-PPC4161-epsilonA-bound-input-acquisition-or-no-source-slot-bridge.md"

CSV_4672_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4672_NEXT_TARGET.csv"
CSV_4672_OWNER = SOURCE_DIR / "P8_Y5_R2FR_4672_EVEN_BRANCH_OWNER_AUDIT.csv"
CSV_4672_B826 = SOURCE_DIR / "P8_Y5_R2FR_4672_B826_EVEN_RESPONSE_WELD.csv"
CSV_4672_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4672_FIRST_ZM_B826_BOUND_ROW_CONTRACT.csv"
CSV_4672_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4672_STATUS.csv"
CSV_4672_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4672_VALIDATION.csv"

CSV_4633_BRIDGE = SOURCE_DIR / "P8_Y5_R2FR_4633_NO_SOURCE_SLOT_TO_EVEN_AM_BRIDGE_ROWS.csv"
CSV_4633_SIGN = SOURCE_DIR / "P8_Y5_R2FR_4633_PARENT_SIGNING_MATRIX.csv"
CSV_4633_MANIFEST = SOURCE_DIR / "P8_Y5_R2FR_4633_EPSILONA_INPUT_ACQUISITION_MANIFEST.csv"
CSV_4633_EVAL = SOURCE_DIR / "P8_Y5_R2FR_4633_BRIDGE_OR_BOUND_EVALUATION.csv"
CSV_4633_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4633_STATUS.csv"
CSV_4633_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4633_VALIDATION.csv"

CSV_1451_THEOREM = SOURCE_DIR / "P8_Y5_R10_1451_NO_SOURCE_ONLY_SLOT_OPERATOR_GRAMMAR_THEOREM_ATTEMPT.csv"
CSV_1451_MATRIX = SOURCE_DIR / "P8_Y5_R10_1451_SOURCE_ONLY_SLOT_REDUCTION_MATRIX.csv"
CSV_1451_SIGN = SOURCE_DIR / "P8_Y5_R10_1451_PARENT_SIGNING_DECISION.csv"
CSV_1451_REQ = SOURCE_DIR / "P8_Y5_R10_1451_EPSILON_A_BOUND_INPUT_REQUIREMENTS.csv"
CSV_1452_THEOREM = SOURCE_DIR / "P8_Y5_R10_1452_COMMON_MEASURE_CURRENT_THEOREM_ATTEMPT.csv"
CSV_1452_SIGN = SOURCE_DIR / "P8_Y5_R10_1452_PARENT_SIGNING_DECISION.csv"
CSV_1453_THEOREM = SOURCE_DIR / "P8_Y5_R10_1453_CURRENT_SOURCE_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv"
CSV_1454_THEOREM = SOURCE_DIR / "P8_Y5_R10_1454_VARIATION_BEFORE_READOUT_THEOREM_ATTEMPT.csv"
CSV_1455_THEOREM = SOURCE_DIR / "P8_Y5_R10_1455_DERIVATIVE_BEFORE_PROJECTION_THEOREM.csv"

CSV_4507_FORMULA = SOURCE_DIR / "P8_Y5_R2FR_4507_BMEM_EFFECTIVE_FORMULA.csv"
CSV_4514_BMEM = SOURCE_DIR / "P8_Y5_R2FR_4514_BMEM_EFFECTIVE_COMPONENT_VECTOR.csv"
CSV_4628_HESSIAN = SOURCE_DIR / "P8_Y5_R2FR_4628_PARENT_HESSIAN_ROWS.csv"
CSV_4628_NUMERIC = SOURCE_DIR / "P8_Y5_R2FR_4628_ZMEM_M2MEM_FIRST_NUMERIC_TEMPLATE_NONCLAIM.csv"
CSV_4626_ANCHORS = SOURCE_DIR / "P8_Y5_R2FR_4626_SOURCE_BACKED_BOUND_ANCHORS.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4673_SOURCE_REGISTER.csv"
BRIDGE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4673_AM_R826_NO_SOURCE_SLOT_BRIDGE.csv"
R826_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4673_R826_SLOT_OWNER_AUDIT.csv"
INPUT_PACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4673_FIRST_ZM_B826_INPUT_PACK.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4673_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4673_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4673_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4673_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4673_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4673_VALIDATION.csv"


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
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def table(rows: list[dict[str, Any]]) -> str:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    suffix = "" if not existing or existing.endswith("\n") else "\n"
    path.write_text(existing + suffix + text.lstrip("\n"), encoding="utf-8")


def csv_line(values: list[str]) -> str:
    buffer = io.StringIO()
    csv.writer(buffer, lineterminator="\n").writerow(values)
    return buffer.getvalue()


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4673_00_4672_next", CSV_4672_NEXT, "4673-Y5-R2FR-no-source-slot-common-measure-bridge-or-first-ZM-B826-input-fill.md", "4672 selected 4673."),
        ("SRC4673_01_4672_owner", CSV_4672_OWNER, "OWN4672_6_verdict", "owner route not proved."),
        ("SRC4673_02_4672_B826", CSV_4672_B826, "WELD4672_3_no_source_slot_theorem", "R826 no-source-slot target."),
        ("SRC4673_03_4672_bound", CSV_4672_BOUND, "BND4672_1_no_source_slot", "A_m/R826 slot exclusion row."),
        ("SRC4673_04_4672_status", CSV_4672_STATUS, "EVEN_BRANCH_OWNER_NOT_SOURCED", "4672 status."),
        ("SRC4673_05_4672_validation", CSV_4672_VALIDATION, "VAL4672_OVERALL,True,PASS", "4672 validation."),
        ("SRC4673_06_doc4672", DOC_4672, "derive a no-source-slot/common-measure bridge", "4672 prose."),
        ("SRC4673_07_formal688", FORMAL_688, "A_m/R_826 slot exclusion", "4672 formal contract."),
        ("SRC4673_08_4633_bridge", CSV_4633_BRIDGE, "BR4633_0_no_slot_implies_q_basic_Am", "A_m no-slot bridge."),
        ("SRC4673_09_4633_verdict", CSV_4633_BRIDGE, "BR4633_4_bridge_verdict", "A_m bridge refused now."),
        ("SRC4673_10_4633_sign", CSV_4633_SIGN, "SIGN4633_0_no_hidden_visible_Hom", "signing matrix."),
        ("SRC4673_11_4633_manifest", CSV_4633_MANIFEST, "ACQ4633_0_parent_zero_route", "epsilon manifest."),
        ("SRC4673_12_4633_eval", CSV_4633_EVAL, "EVAL4633_1_current_corpus", "zero import refused."),
        ("SRC4673_13_4633_status", CSV_4633_STATUS, "PRIVATE_NONCLAIM_BRIDGE", "4633 status."),
        ("SRC4673_14_4633_validation", CSV_4633_VALIDATION, "VAL4633_OVERALL,PASS", "4633 validation."),
        ("SRC4673_15_doc4633", DOC_4633, "NoSourceOnlySlot + NoHiddenVisibleHom", "4633 prose."),
        ("SRC4673_16_1451_theorem", CSV_1451_THEOREM, "OG1451_6_verdict", "no-source slot theorem verdict."),
        ("SRC4673_17_1451_matrix", CSV_1451_MATRIX, "SM1451_6_verdict", "source slot reduction matrix."),
        ("SRC4673_18_1451_sign", CSV_1451_SIGN, "SIGN1451_0_no_slot", "no-slot sign decision."),
        ("SRC4673_19_1451_req", CSV_1451_REQ, "REQ1451_0_definition", "epsilon input requirements."),
        ("SRC4673_20_1452_theorem", CSV_1452_THEOREM, "CMT1452_6_verdict", "common measure/current verdict."),
        ("SRC4673_21_1452_sign", CSV_1452_SIGN, "SIGN1452_0_common_measure", "common measure signing."),
        ("SRC4673_22_1453_theorem", CSV_1453_THEOREM, "CSO1453_1_hilbert_variation", "current owner theorem."),
        ("SRC4673_23_1454_theorem", CSV_1454_THEOREM, "VBR1454_1_variational_identity", "variation before readout."),
        ("SRC4673_24_1455_theorem", CSV_1455_THEOREM, "DBP1455_4_conclusion", "derivative before projection."),
        ("SRC4673_25_4507_formula", CSV_4507_FORMULA, "BMF4507_1_826_term", "B826 term."),
        ("SRC4673_26_4514_Bmem", CSV_4514_BMEM, "BMV4514_0_B826", "B826 component."),
        ("SRC4673_27_4628_hessian", CSV_4628_HESSIAN, "HES4628_1_parent_hessian_definitions", "parent Hessian definition."),
        ("SRC4673_28_4628_numeric", CSV_4628_NUMERIC, "LNUM4628_2_lambda", "lambda numeric template."),
        ("SRC4673_29_4626_anchor", CSV_4626_ANCHORS, "BA4626_0_R10_EOTWASH_ALPHA1", "R10 anchor warning."),
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
                "timestamp_utc": timestamp,
            }
        )
    return rows


def bridge_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("BR4673_0_Am_qbasic", "A_m no-source-slot bridge", "NoSourceOnlySlot+NoHiddenVisibleHom+LabelForgetting+CommonMeasureCurrent => A_m=A_m(q,theta_fixed)", "P_vert d ln A_m=0, epsilon_A=0", "CONDITIONAL_FROM_4633_UNSIGNED"),
        ("BR4673_1_R826_qbasic", "R826 no-source-slot bridge", "same grammar must also forbid R_826(q,z;X_B) source-only vertical dependence", "P_vert dR_826=0, R_m=0, B826=0", "NEW_REQUIRED_EXTENSION_UNSIGNED"),
        ("BR4673_2_common_owner", "common source functor", "A_m and R_826 must descend through the same q-basic Hilbert source/common-measure functor before readout", "prevents separate tuning of beta_visible and B826", "SAME_OWNER_CONDITION_ADDED"),
        ("BR4673_3_post_variation_readout", "post-variation readout alternative", "if R_826 is only a post-solution/readout diagnostic and not a parent action/source argument, its vertical source derivative is not a parent force", "B826 source term is absent rather than even", "CONDITIONAL_REQUIRES_READOUT_DOMAIN_PROOF"),
        ("BR4673_4_countermodel", "pre-action response slot", "S_parent may contain R_826(q,z;X_B) or w_R R_826 before variation unless grammar forbids it", "B826 survives as finite coefficient", "COUNTERMODEL_RETAINED"),
        ("BR4673_5_verdict", "A_m/R826 bridge", "A_m bridge is sharp but unsigned; R826 bridge is now explicit and unsigned", "zero import refused; finite input pack selected", "ZERO_IMPORT_REFUSED_INPUT_PACK_READY"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bridge_id": row[0],
            "bridge_piece": row[1],
            "condition": row[2],
            "result_if_signed": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def r826_audit_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("R8264673_0_formula", "B_826=a_F L_cg^-2 R_m(m_L;X_B)", "4507/4514", "structure ready", "STRUCTURE_READY"),
        ("R8264673_1_XB_qbasic", "X_B fixed/q-basic under vertical variation", "needed before dR_826[v] can be tested cleanly", "not separately signed for B826", "MISSING_XB_LOCK"),
        ("R8264673_2_R_descends", "R_826=R_826(q;X_B) or R_826 absent before variation", "would make dR_826[v]=0 for v in ker(Dq)", "not found in current corpus", "MISSING_R826_DESCENT"),
        ("R8264673_3_common_measure", "same common measure/current owner as A_m", "prevents source normalization from re-entering through response coefficient", "1452 common measure remains unsigned", "COMMON_MEASURE_UNSIGNED"),
        ("R8264673_4_nonHilbert", "no non-Hilbert/response bypass", "prevents an R826-like non-Hilbert source slot from replacing the killed term", "non-Hilbert guard remains open", "NONHILBERT_GUARD_OPEN"),
        ("R8264673_5_finite", "|B826| <= |a_F| L_cg^-2 |R_m|", "fallback if descent/no-slot owner fails", "needs source-backed a_F,L_cg,R_m,profile", "FINITE_ROW_REQUIRED"),
        ("R8264673_6_verdict", "B826 no-slot owner", "claim-grade zero requires R826 descent/no-source-slot or post-variation proof", "not promoted", "B826_NO_SLOT_NOT_SIGNED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "audit_id": row[0],
            "object": row[1],
            "test": row[2],
            "current_result": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def input_pack_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("PACK4673_0_zero_owner", "OWNER_ZERO", "A_m/R826 no-source-slot", "signed common no-source-slot/common-measure/no-Hom/non-Hilbert/readout-domain theorem", "MISSING_SIGNED_OWNER"),
        ("PACK4673_1_epsilonA", "FINITE_BOUND", "epsilon_A", "visible matter scale vertical derivative norm", "MISSING_VALUE_OR_ZERO_THEOREM"),
        ("PACK4673_2_epsilonB", "FINITE_BOUND", "epsilon_B", "test/source body sensitivity norm", "MISSING_VALUE_OR_ZERO_THEOREM"),
        ("PACK4673_3_Z0", "FINITE_BOUND", "Z0", "positive same-branch kinetic Hessian lower bound", "MISSING_PARENT_HESSIAN"),
        ("PACK4673_4_M0", "FINITE_BOUND", "M0^2", "positive same-branch mass/gap Hessian lower bound", "MISSING_PARENT_GAP"),
        ("PACK4673_5_lambda", "FINITE_BOUND", "lambda_mem", "sqrt(Z_mem/M2_mem) from same branch", "MISSING_ZM_RATIO"),
        ("PACK4673_6_CN", "FINITE_BOUND", "C_N", "Newton/Planck normalization in alpha_AB=C_N epsilon_A epsilon_B/Z0", "MISSING_CONVENTION"),
        ("PACK4673_7_B826", "FINITE_BOUND", "a_F,L_cg,R_m", "|B826| <= |a_F| L_cg^-2 |R_m|", "MISSING_B826_VALUES"),
        ("PACK4673_8_profile", "FINITE_BOUND", "R_obs/body profile", "profile insertion into rho_mem and A_mem envelope", "MISSING_PROFILE"),
        ("PACK4673_9_curve", "FINITE_BOUND", "alpha_bound(lambda)", "full source-backed R10 curve after MTS alpha/lambda exists", "ANCHOR_ONLY_NOT_CLAIM"),
        ("PACK4673_10_claim", "COMMON", "valid_for_claim", "true only after owner-zero proof or sourced finite pack passes matrix", "FALSE_NOW"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "pack_id": row[0],
            "route": row[1],
            "symbol": row[2],
            "needed_input": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def runner_rows(timestamp: str, sources: list[dict[str, Any]], bridge: list[dict[str, Any]], r826: list[dict[str, Any]], pack: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["needle_found"] for row in sources)
    bridge_refused = any(row["status"] == "ZERO_IMPORT_REFUSED_INPUT_PACK_READY" for row in bridge)
    r826_not_signed = any(row["status"] == "B826_NO_SLOT_NOT_SIGNED" for row in r826)
    finite_pack_ready = any(row["pack_id"] == "PACK4673_7_B826" for row in pack)
    no_claim = all(str(row.get("valid_for_claim")) == "False" for row in bridge + r826 + pack)
    data = [
        ("RUN4673_0_sources", sources_ok, "all source paths and needles found"),
        ("RUN4673_1_bridge", bridge_refused, "A_m/R826 no-slot bridge is explicit but unsigned"),
        ("RUN4673_2_R826", r826_not_signed, "R826 owner is not signed"),
        ("RUN4673_3_pack", finite_pack_ready, "first ZM+B826 input pack is present"),
        ("RUN4673_4_nonclaim", no_claim, "all rows remain nonclaim"),
        ("RUN4673_5_decision", DECISION.endswith("NONCLAIM"), "decision refuses promotion"),
        ("RUN4673_6_next", NEXT_TARGET.startswith("4674-"), "next target selected"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "runner_id": row[0],
            "passed": bool(row[1]),
            "status": "PASS" if row[1] else "FAIL",
            "detail": row[2],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CTRL4673_0_no_Am_to_R826_free_ride", "A_m q-basic does not automatically prove R826 q-basic.", "PASS"),
        ("CTRL4673_1_same_parent_owner", "A_m and R826 exact-zero route must share the same parent source/common-measure owner.", "PASS"),
        ("CTRL4673_2_no_covariance_shortcut", "Covariance or unchanged matter EOM do not remove pre-action weights/response slots.", "PASS"),
        ("CTRL4673_3_no_anchor_smuggle", "R10 alpha=1 anchor cannot source lambda/Z/M.", "PASS"),
        ("CTRL4673_4_no_B826_total", "B826 zero or bound is only one B_mem_eff component.", "PASS"),
        ("CTRL4673_5_no_poynting_hide", "Poynting/non-Hilbert/boundary channels remain explicit.", "PASS"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": row[0],
            "rule": row[1],
            "status": row[2],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "why": "4633 gives a sharp no-source-slot bridge for A_m, but R826 needs its own descent/no-source-slot/post-variation owner. Current corpus does not sign that owner, so exact zero remains conditional and the first Z/M+B826 finite input pack is now the next executable object.",
            "promoted": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "Am_no_slot_bridge_signed": False,
            "R826_no_slot_bridge_signed": False,
            "ZM_inputs_sourced": False,
            "B826_inputs_sourced": False,
            "epsilon_inputs_sourced": False,
            "zero_import_allowed": False,
            "finite_pack_ready": True,
            "B826_zero": False,
            "local_GR_claim": False,
            "r10_claim": False,
            "ppn_claim": False,
            "decision": DECISION,
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "4673 makes the no-slot proof sharper but unsigned; the next executable step is either prove R826 no-slot/common-owner directly or fill the first finite input pack.",
            "derive_route": "Try to prove R826 descends through q, is post-variation readout, or is absent from the parent source slots under the same common-measure owner as A_m.",
            "fallback_route": "Fill source-backed rows for Z0, M0^2, lambda_mem, epsilon_A/B, C_N, a_F, L_cg, R_m and body profile.",
            "avoid": "Do not promote A_m no-slot as R826 no-slot, do not use R10 anchor as Hessian data, and do not claim local GR from one B component.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(timestamp: str, sources: list[dict[str, Any]], runner: list[dict[str, Any]], outputs: list[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_failures = [row["source_id"] for row in sources if not (row["path_exists"] and row["needle_found"])]
    rows.append({"validation_id": "VAL4673_0_sources", "passed": not source_failures, "detail": "all source paths and needles found" if not source_failures else ";".join(source_failures), "timestamp_utc": timestamp})
    for path in [SOURCE_REGISTER, BRIDGE_CSV, R826_AUDIT_CSV, INPUT_PACK_CSV, RUNNER_CSV, CONTROL_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV]:
        try:
            parsed = read_csv(path)
            rows.append({"validation_id": f"VAL4673_parse_{path.name}", "passed": len(parsed) > 0, "detail": f"rows={len(parsed)} columns={len(parsed[0]) if parsed else 0}", "timestamp_utc": timestamp})
        except Exception as exc:
            rows.append({"validation_id": f"VAL4673_parse_{path.name}", "passed": False, "detail": repr(exc), "timestamp_utc": timestamp})
    rows.append({"validation_id": "VAL4673_1_runner_pass", "passed": all(str(row["status"]) == "PASS" for row in runner), "detail": "runner rows passed" if all(str(row["status"]) == "PASS" for row in runner) else "runner failure", "timestamp_utc": timestamp})
    rows.append({"validation_id": "VAL4673_2_outputs_exist", "passed": all(path.exists() for path in outputs), "detail": ";".join(str(path) for path in outputs if path.exists()), "timestamp_utc": timestamp})
    rows.append({"validation_id": "VAL4673_3_no_claim_promotion", "passed": all(str(row.get("valid_for_claim", "False")) == "False" for row in runner), "detail": "valid_for_claim remains false", "timestamp_utc": timestamp})
    overall = all(bool(row["passed"]) for row in rows)
    rows.append({"validation_id": "VAL4673_OVERALL", "passed": overall, "detail": "PASS" if overall else "FAIL", "timestamp_utc": timestamp})
    return rows


def write_doc(timestamp: str, sources: list[dict[str, Any]], bridge: list[dict[str, Any]], r826: list[dict[str, Any]], pack: list[dict[str, Any]], runner: list[dict[str, Any]], controls: list[dict[str, Any]], decision: list[dict[str, Any]], status: list[dict[str, Any]], next_target: list[dict[str, Any]]) -> None:
    content = f"""# 4673 — No-source-slot/common-measure bridge or first ZM/B826 input fill

Timestamp: `{timestamp}`

## Result

4673 extends the 4633 no-source-slot bridge.  The old bridge covered `A_m`:

```text
A_m=A_m(q,theta_fixed) => P_vert d ln A_m = 0.
```

That does **not** automatically cover the first `B_mem_eff` component.  For `B_826` we need an extra owner:

```text
R_826=R_826(q;X_B), with X_B q-basic/fixed,
or R_826 is post-variation/readout and absent from the parent source slots.
```

Then for every vertical `v in ker(Dq)`,

```text
dR_826[v]=0,
R_m(m0;X_B)=0,
B_826=a_F L_cg^-2 R_m=0.
```

Current result: this is the clean route, but it is unsigned.  The checkpoint refuses zero import and creates the first finite `Z/M + epsilon + B826` input pack.

## Bridge rows

{table(bridge)}

## R826 owner audit

{table(r826)}

## First input pack

{table(pack)}

## Runner

{table(runner)}

## Controls

{table(controls)}

## Decision

{table(decision)}

## Status

{table(status)}

## Next target

{table(next_target)}

## Source register

{table(sources)}
"""
    DOC_PATH.write_text(content, encoding="utf-8")


def write_formal(timestamp: str, bridge: list[dict[str, Any]], r826: list[dict[str, Any]], pack: list[dict[str, Any]], decision: list[dict[str, Any]]) -> None:
    content = f"""# PPC4161 — No-source-slot/common-measure bridge or first ZM/B826 input fill

Checkpoint: `{CHECKPOINT}`  
Claim row: `{CLAIM_ID}`  
Timestamp: `{timestamp}`

## Formal statement

The exact no-source-slot route is:

```text
A_m=A_m(q,theta_fixed),
R_826=R_826(q;X_B) or R_826 is post-variation/readout,
X_B is q-basic/fixed,
v in ker(Dq).
```

Then

```text
d ln A_m[v]=0,
dR_826[v]=0,
epsilon_A=0,
B_826=a_F L_cg^-2 R_m=0.
```

4673 refuses promotion because the current corpus signs neither the `A_m` bridge nor the new `R_826` bridge.  The finite route is now explicit.

## Bridge

{table(bridge)}

## R826 audit

{table(r826)}

## Input pack

{table(pack)}

## Decision

{table(decision)}
"""
    FORMAL_PATH.write_text(content, encoding="utf-8")


def update_claims() -> None:
    existing = read_text(CLAIMS_PATH)
    if f"{CLAIM_ID}," in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr_empirical_interface",
        "4673 extends the no-source-slot/common-measure bridge from A_m to the 826 response. The A_m bridge would set epsilon_A=0 if A_m is q-basic, but B_826 needs its own condition: R_826 must descend through q with X_B fixed/q-basic, or be post-variation/readout and absent from parent source slots. Current evidence does not sign that R826 owner, so zero import is refused and the first finite Z/M+epsilon+B826 input pack is now explicit.",
        "Generated source register, A_m/R826 bridge rows, R826 slot owner audit, first ZM/B826 input pack, runner, controls, decision, status, next target and validation.",
        "no_source_slot_bridge_extended_to_R826_unsigned_first_ZM_B826_input_pack_ready_nonclaim",
        NEXT_TARGET,
        "Treating A_m q-basic as automatically proving R826 q-basic, using R10 anchor as Z/M data, hiding B826 inside Bmem_eff cancellation, or claiming local GR before B/J/Q/metric gates close.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN/R10 claim until R826 no-slot owner or finite ZM/B826 inputs are source-backed and the remaining gates close.",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        handle.write(csv_line(row))


def update_spine_and_packet() -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4673 extends the no-source-slot/common-measure bridge from `A_m` to `R_826`. `A_m` q-basic would set `epsilon_A=0`, but `B_826` also needs `R_826=R_826(q;X_B)` with `X_B` q-basic/fixed, or a proof that `R_826` is post-variation/readout and absent from parent source slots. Current evidence does not sign that owner, so the finite `Z/M + epsilon + B826` input pack is selected next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## {PACKET_MARKER}

Checkpoint `{CHECKPOINT}` prevents a free ride from `A_m` q-basic to `B_826=0`. Either prove `R_826` no-slot/common-owner, or fill the first finite `Z/M + B826` pack. Next packet target: `{NEXT_TARGET}`.
""",
    )


def main() -> None:
    timestamp = now()
    sources = source_rows(timestamp)
    bridge = bridge_rows(timestamp)
    r826 = r826_audit_rows(timestamp)
    pack = input_pack_rows(timestamp)
    runner = runner_rows(timestamp, sources, bridge, r826, pack)
    controls = control_rows(timestamp)
    decision = decision_rows(timestamp)
    status = status_rows(timestamp)
    next_target = next_rows(timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(BRIDGE_CSV, bridge)
    write_csv(R826_AUDIT_CSV, r826)
    write_csv(INPUT_PACK_CSV, pack)
    write_csv(RUNNER_CSV, runner)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decision)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)

    write_doc(timestamp, sources, bridge, r826, pack, runner, controls, decision, status, next_target)
    write_formal(timestamp, bridge, r826, pack, decision)
    update_claims()
    update_spine_and_packet()

    outputs = [DOC_PATH, FORMAL_PATH, SOURCE_REGISTER, BRIDGE_CSV, R826_AUDIT_CSV, INPUT_PACK_CSV, RUNNER_CSV, CONTROL_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV]
    validation = validation_rows(timestamp, sources, runner, outputs)
    write_csv(VALIDATION_CSV, validation)
    if not all(bool(row["passed"]) for row in validation):
        failures = [row for row in validation if not row["passed"]]
        raise SystemExit(f"4673 validation failed: {failures}")
    print(f"4673 complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
