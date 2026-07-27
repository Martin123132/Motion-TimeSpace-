from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2737-Y5-R2FR-source-support-and-inner-charge-theorem-or-bound-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2737_SOURCE_REGISTER.csv",
    "source_zero": RESIDUALS / "P8_Y5_R2FR_2737_SOURCE_SUPPORT_ZERO_AUDIT.csv",
    "inner_zero": RESIDUALS / "P8_Y5_R2FR_2737_INNER_CHARGE_ZERO_AUDIT.csv",
    "envelope": RESIDUALS / "P8_Y5_R2FR_2737_TOTAL_SCG_ENVELOPE_ROWS.csv",
    "first_pair": RESIDUALS / "P8_Y5_R2FR_2737_FIRST_PAIR_BOUND_CONTRACT.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2737_DECISION_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2737_CLAIM_GATES.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2737_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2737_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2737_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "first_pair": LOCAL_BOUNDS / "Nsrc_Ninner_first_pair_bound_2737_NONCLAIM.csv",
    "reopen": SOURCE_WEIGHT / "source_support_inner_charge_reopen_conditions_2737_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2737_WORLDTUBE_PROFILE_INNER_CHARGE_NEXT.csv",
}

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()}:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    body = ["| " + " | ".join(md(row.get(col, "")) for col in cols) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def local_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    return row


def source_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC2737_0_2736_doc",
            "description": "2736 selects N_src and N_inner as the first physical N_lock blockers.",
            "source_path": "2736-Y5-R2FR-Jeff-Bm-source-boundary-silence-or-finite-Nlock-row-under-AX1090.md",
            "required_needles": "N_SRC2736_0_N_src;N_BM2736_0_N_inner;NEXT2736_0_2737",
        },
        {
            "source_id": "SRC2737_1_1542_doc",
            "description": "1542 gives the finite S_cg envelope and first-pair insertion.",
            "source_path": "1542-Y5-q-definition-or-Dqvm-coupling-coefficient-source-pack.md",
            "required_needles": "CQM1542_5_Scg_envelope;RUN1542_2_Npair;FORK1542_1_finite_Cqm",
        },
        {
            "source_id": "SRC2737_2_1543_doc",
            "description": "1543 maps source envelope into arena projection rows.",
            "source_path": "1543-Y5-Cqm-source-norm-local-projection-pack.md",
            "required_needles": "FIN1543_5_S_cg_norm;ARENA1543_0_R10;RUN1543_1_Npair",
        },
        {
            "source_id": "SRC2737_3_1545_doc",
            "description": "1545 guards T_source_norm, direct memory, source-normalization, and boundary terms.",
            "source_path": "1545-Y5-source-norm-and-direct-memory-residual-provenance-pack.md",
            "required_needles": "TS1545_4_verdict;BND1545_0_definition;SCG1545_2_Npair",
        },
        {
            "source_id": "SRC2737_4_1546_doc",
            "description": "1546 rejects orbital-GM import and makes T_source_norm a worldtube/profile problem.",
            "source_path": "1546-Y5-Tsource-worldtube-normalization-or-source-profile-acquisition.md",
            "required_needles": "WT1546_3_no_orbital_GM_import;TDEF1546_4_current_verdict;NEXT1546_0_1547",
        },
        {
            "source_id": "SRC2737_5_2608_source_status",
            "description": "2608 shows affine source silence is narrowed but not zeroed.",
            "source_path": "source-intake/mts_residuals/P8_Y5_AFFINE_SOURCE_GATE_2608_SOURCE_ZERO_STATUS.csv",
            "required_needles": "SZ2608_3_affine_bound;SZ2608_4_source_silence",
        },
        {
            "source_id": "SRC2737_6_2608_bound_rows",
            "description": "2608 gives the explicit U_B-weighted affine source residual form.",
            "source_path": "source-intake/mts_residuals/P8_Y5_AFFINE_SOURCE_GATE_2608_AFFINE_SOURCE_BOUND_ROWS.csv",
            "required_needles": "ASB2608_2_A_affine;ASB2608_3_R_source_affine;ASB2608_4_observable_insert",
        },
        {
            "source_id": "SRC2737_7_2615_source_status",
            "description": "2615 keeps source-shadow and block source channels open.",
            "source_path": "source-intake/mts_residuals/P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_SOURCE_ZERO_STATUS.csv",
            "required_needles": "SZ2615_1_no_source_shadow;SZ2615_4_delta_w_block;SZ2615_5_local_GR",
        },
        {
            "source_id": "SRC2737_8_1529_boundary",
            "description": "1529 blocks boundary/no-flux and zero-mode shortcuts.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1529_BOUNDARY_CERTIFICATE_AUDIT.csv",
            "required_needles": "BND1529_1_boundary_condition;BND1529_2_zero_mode_reference;BND1529_5_verdict",
        },
        {
            "source_id": "SRC2737_9_positive_nohair",
            "description": "positive no-hair warns compact-source inner boundary charge is not automatic zero.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_POSITIVE_OPERATOR_NOHAIR_ATTEMPT.csv",
            "required_needles": "NH562_1_energy_identity;NH562_2_compact_source_inner_boundary;NH562_5_verdict",
        },
    ]
    for row in rows:
        path = local_path(row["source_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        needles = [needle for needle in row["required_needles"].split(";") if needle]
        missing = [needle for needle in needles if needle not in text]
        row["exists"] = path.exists()
        row["needles_present"] = len(missing) == 0
        row["missing_needles"] = ";".join(missing)
        nonclaim(row)
    return rows


def source_zero_rows() -> list[dict[str, Any]]:
    rows = [
        ("SZ2737_0_definition", "N_src", "N_src:=||U_B S_cg,total||_{E*}", "DEFINITION", "defines the source-support contribution to J_eff", "none"),
        ("SZ2737_1_exact_U_B_zero", "U_B=0 on the compact-source exterior annulus", "would force N_src=0 if S_cg,total is finite in the same E* norm", "UNSIGNED_ZERO_ROUTE", "no parent branch proves exact U_B=0 with support/domain conventions", "U_B theorem or source-backed U_B_max=0"),
        ("SZ2737_2_exact_source_projection_zero", "P_ext S_cg,total=0", "would force N_src=0 even with finite U_B", "UNSIGNED_ZERO_ROUTE", "source projection, direct memory, source-shadow, and boundary/history channels are not all killed", "parent source-projection silence theorem"),
        ("SZ2737_3_affine_obstruction", "affine hidden source", "R_source,affine carries ||R_source,affine||_{E*}<=U_B A_affine", "FINITE_ROUTE_ONLY", "2608 keeps A_shift/A_marker unsigned", "A_affine zero theorem or numeric E* bound"),
        ("SZ2737_4_source_shadow_block", "source shadow / block prefactor", "delta_w_block and source-shadow rows survive as sibling source channels", "FINITE_ROUTE_ONLY", "2615 does not exclude source-shadow or disconnected block countermodels", "source-shadow ban and exchange-block connectivity or finite block bound"),
        ("SZ2737_5_verdict", "N_src exact zero", "N_src=0 is not proved; finite bound route is N_src<=U_B,max S_cg,total_norm", "THEOREM_ZERO_NOT_CLOSED", "at least one source-support channel remains unsigned", "worldtube/profile plus source-channel norm pack"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "zero_id": zero_id,
                "target": target,
                "law_or_condition": law,
                "status": status,
                "reason": reason,
                "missing_to_promote": missing,
                "zero_proved": False,
                "source_paths": "2736-Y5-R2FR-Jeff-Bm-source-boundary-silence-or-finite-Nlock-row-under-AX1090.md; 1542-Y5-q-definition-or-Dqvm-coupling-coefficient-source-pack.md; source-intake/mts_residuals/P8_Y5_AFFINE_SOURCE_GATE_2608_SOURCE_ZERO_STATUS.csv; source-intake/mts_residuals/P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_SOURCE_ZERO_STATUS.csv",
            }
        )
        for zero_id, target, law, status, reason, missing in rows
    ]


def inner_zero_rows() -> list[dict[str, Any]]:
    rows = [
        ("IC2737_0_definition", "Q_m^H", "inner compact-source memory/coupling charge entering B_inner", "DEFINITION", "abstract source-boundary charge; exact normalization still needs parent source profile", "source profile, boundary surface, charge convention"),
        ("IC2737_1_exact_zero_charge", "Q_m^H=0", "would remove the leading compact-source boundary hair", "UNSIGNED_ZERO_ROUTE", "positive no-hair warns compact inner boundary is not automatic zero", "Noether/source-silence theorem or charge-neutrality theorem"),
        ("IC2737_2_no_flux_boundary", "no-flux boundary", "would kill boundary work only with zero-mode and domain certificates", "UNSIGNED_ZERO_ROUTE", "1529 has no parent-signed no-flux certificate", "boundary condition plus zero-mode/reference certificate"),
        ("IC2737_3_domain_support", "domain/support motion", "domain work must be zero or bounded in same boundary-dual norm", "FINITE_ROUTE_ONLY", "compact support/excision convention is not source-backed", "worldtube/excision/domain profile"),
        ("IC2737_4_finite_bound", "N_inner", "N_inner <= C_inner |Q_m^H| + N_inner,domain + N_inner,zero_mode", "BOUND_FORM_STAGED_NONCLAIM", "C_inner, Q_m^H, domain and zero-mode norms are missing", "finite boundary-dual norm rows"),
        ("IC2737_5_verdict", "N_inner exact zero", "N_inner=0 is not proved; finite boundary-charge route remains live", "THEOREM_ZERO_NOT_CLOSED", "inner charge and boundary certificates remain unsigned", "shared worldtube/profile and boundary-charge pack"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "inner_id": inner_id,
                "target": target,
                "law_or_condition": law,
                "status": status,
                "reason": reason,
                "missing_to_promote": missing,
                "zero_proved": False,
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_POSITIVE_OPERATOR_NOHAIR_ATTEMPT.csv; source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1529_BOUNDARY_CERTIFICATE_AUDIT.csv; 1545-Y5-source-norm-and-direct-memory-residual-provenance-pack.md",
            }
        )
        for inner_id, target, law, status, reason, missing in rows
    ]


def envelope_rows() -> list[dict[str, Any]]:
    rows = [
        ("ENV2737_0_core_Scg", "S_cg,core", "S_cg,core <= 1/2*T_source_norm*C_qm + S_direct_m + S_source_norm_extra + S_boundary_m", "IMPORTED_CORE_ENVELOPE", "C_qm, T_source_norm, direct/source-normalization/boundary residuals all missing"),
        ("ENV2737_1_affine_source", "A_affine", "||R_source,affine||_{E*}<=U_B A_affine", "ADDITIVE_CHANNEL_STAGED", "A_affine and same E* norm missing"),
        ("ENV2737_2_block_shadow", "A_block_shadow", "source-shadow/block-prefactor residual must be zeroed or bounded separately", "ADDITIVE_CHANNEL_STAGED", "source-shadow ban, exchange graph connectivity, or finite block bound missing"),
        ("ENV2737_3_total_guard", "S_cg,total_norm", "S_cg,total_norm <= S_cg,core + A_affine + A_block_shadow + A_extra_hidden", "CONSERVATIVE_TOTAL_GUARD_NONCLAIM", "A_extra_hidden and common norm/provenance missing"),
        ("ENV2737_4_Nsrc", "N_src", "N_src <= U_B,max S_cg,total_norm", "FIRST_PAIR_SOURCE_BOUND_STAGED", "U_B,max and total source norm missing"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "envelope_id": envelope_id,
                "quantity": quantity,
                "formula_or_rule": formula,
                "status": status,
                "missing_to_promote": missing,
                "source_paths": "1542-Y5-q-definition-or-Dqvm-coupling-coefficient-source-pack.md; source-intake/mts_residuals/P8_Y5_AFFINE_SOURCE_GATE_2608_AFFINE_SOURCE_BOUND_ROWS.csv; source-intake/mts_residuals/P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_SOURCE_ZERO_STATUS.csv",
            }
        )
        for envelope_id, quantity, formula, status, missing in rows
    ]


def first_pair_rows() -> list[dict[str, Any]]:
    rows = [
        ("FP2737_0_pair_definition", "N_pair", "N_pair:=N_src+N_inner", "definition for first source/boundary pair feeding N_lock", "DEFINITION", "none"),
        ("FP2737_1_pair_bound", "N_pair", "N_pair <= U_B,max S_cg,total_norm + C_inner |Q_m^H| + N_inner,domain + N_inner,zero_mode", "absolute no-cancellation first-pair bound", "BOUND_FORM_STAGED_NONCLAIM", "U_B,max; S_cg,total_norm; C_inner; Q_m^H; domain/zero-mode boundary norms"),
        ("FP2737_2_Nlock_insert", "N_lock", "N_lock <= N_pair + N_rest", "keeps first-pair progress separated from remaining J/B components", "INTERFACE_STAGED_NONCLAIM", "N_rest component norms from 2736 remain missing"),
        ("FP2737_3_Delta_m_insert", "Delta_m", "Delta_m <= C_emb (N_pair+N_rest)", "feeds 2735 local-lock amplitude law", "AMPLITUDE_INTERFACE_STAGED", "C_emb/domain constant plus numeric N_pair/N_rest"),
        ("FP2737_4_verdict", "first-pair route", "source/inner exact zero fails current evidence; finite first-pair bound is the honest route", "summary of 2737 theorem attempt", "NOT_SCORE_READY", "shared worldtube/profile and boundary-charge provenance missing"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "pair_id": pair_id,
                "quantity": quantity,
                "formula_or_rule": formula,
                "meaning": meaning,
                "status": status,
                "missing_to_promote": missing,
                "source_paths": "2736-Y5-R2FR-Jeff-Bm-source-boundary-silence-or-finite-Nlock-row-under-AX1090.md; 2735-Y5-R2FR-stationary-source-root-local-lock-or-finite-Delta-m-bound-under-AX1090.md; 1542-Y5-q-definition-or-Dqvm-coupling-coefficient-source-pack.md",
            }
        )
        for pair_id, quantity, formula, meaning, status, missing in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2737_0_source_zero", "Do not claim N_src=0.", "U_B=0 and P_ext S_cg,total=0 are not parent-signed", "source support moves to finite bound route"),
        ("DEC2737_1_inner_zero", "Do not claim N_inner=0.", "Q_m^H/no-flux/zero-mode/domain silence are not parent-signed", "inner charge moves to finite boundary norm route"),
        ("DEC2737_2_first_pair", "Keep N_pair as an explicit first-pair interface.", "it prevents source and boundary leakage from being hidden in N_lock", "future local tests can see exactly what remains missing"),
        ("DEC2737_3_next", "Build one shared worldtube/profile and inner-charge template next.", "T_source_norm, Q_m^H, C_inner, U_B,max, and support maps must be owned together", "next target is profile/provenance, not another abstract silence pass"),
    ]
    return [nonclaim({"decision_id": decision_id, "decision": decision, "because": because, "effect": effect}) for decision_id, decision, because, effect in rows]


def gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2737_0_source_zero", "N_src=0", False, "source support zero theorem not closed"),
        ("GATE2737_1_inner_zero", "N_inner=0", False, "inner charge/no-flux theorem not closed"),
        ("GATE2737_2_pair_numeric", "numeric N_pair", False, "U_B,max, S_cg,total_norm, C_inner, Q_m^H, domain and zero-mode norms are missing"),
        ("GATE2737_3_Nlock_score", "N_lock score-ready", False, "first-pair and remaining component norms are not numeric/theorem-zero"),
        ("GATE2737_4_local_GR", "local GR/Newton/PPN recovery", False, "no exact local lock or finite local residual score"),
        ("GATE2737_5_arena_tests", "R10/PPN/clock/orbital pass", False, "arena projections cannot be run from symbolic first-pair rows"),
    ]
    return [nonclaim({"claim_gate_id": gate_id, "claim": claim, "gate_passed": passed, "claim_allowed": False, "reason": reason}) for gate_id, claim, passed, reason in rows]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2737_0_2738",
                "status": "selected_primary",
                "target_doc": "2738-Y5-R2FR-worldtube-source-profile-and-inner-charge-template-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_worldtube_source_profile_and_inner_charge_template_under_AX1090_2738.py",
                "mission": "create one shared source/worldtube template that can source U_B,max, T_source_norm, S_cg,total_norm, Q_m^H, C_inner, domain/zero-mode norms, and arena support maps without importing orbital GM",
                "acceptance": "fillable rows with units, support/domain convention, norm pair, source paths, and nonclaim placeholders only where unavoidable",
                "forbidden": "do not set T_source_norm=orbital GM; do not set Q_m^H=0 by exterior-vacuum language; do not claim local GR or arena passes",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"copy_id": "BR2737_0_first_pair", "source_table": rel(OUTPUTS["first_pair"]), "copy_path": rel(BRANCH_OUTPUTS["first_pair"]), "purpose": "local-bound nonclaim first-pair N_src/N_inner contract", "exists": BRANCH_OUTPUTS["first_pair"].exists()}),
        nonclaim({"copy_id": "BR2737_1_reopen", "source_table": rel(OUTPUTS["source_zero"]) + ";" + rel(OUTPUTS["inner_zero"]), "copy_path": rel(BRANCH_OUTPUTS["reopen"]), "purpose": "source-weight reopen conditions for exact source support or inner charge silence", "exists": BRANCH_OUTPUTS["reopen"].exists()}),
        nonclaim({"copy_id": "BR2737_2_next_queue", "source_table": rel(OUTPUTS["next"]), "copy_path": rel(BRANCH_OUTPUTS["next_queue"]), "purpose": "RAB acquisition queue for worldtube/profile and inner-charge template", "exists": BRANCH_OUTPUTS["next_queue"].exists()}),
    ]


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    start = SCRIPT_START_UTC.timestamp()
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start)


def validation_rows(
    sources: list[dict[str, Any]],
    source_zero: list[dict[str, Any]],
    inner_zero: list[dict[str, Any]],
    envelope: list[dict[str, Any]],
    first_pair: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    source_zero_blocked = any(row["zero_id"] == "SZ2737_5_verdict" and row["status"] == "THEOREM_ZERO_NOT_CLOSED" for row in source_zero)
    inner_zero_blocked = any(row["inner_id"] == "IC2737_5_verdict" and row["status"] == "THEOREM_ZERO_NOT_CLOSED" for row in inner_zero)
    envelope_ok = any(row["envelope_id"] == "ENV2737_4_Nsrc" for row in envelope)
    first_pair_ok = any(row["pair_id"] == "FP2737_1_pair_bound" for row in first_pair) and all(row["valid_for_claim"] is False for row in first_pair)
    gates_false = all(row["gate_passed"] is False and row["claim_allowed"] is False for row in gates)
    next_ok = next_target[0]["selected"] is True and "worldtube-source-profile" in next_target[0]["target_doc"]
    branch_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    formalization_ok = formalization_recent_count() == 0
    csv_ok = True
    csv_bits: list[str] = []
    for key, path in {**OUTPUTS, **BRANCH_OUTPUTS}.items():
        if key == "validation":
            continue
        try:
            rows = read_csv(path)
            csv_bits.append(f"{path.name}:{len(rows)}:ok")
        except Exception as exc:
            csv_ok = False
            csv_bits.append(f"{path.name}:ERROR:{exc}")
    rows = [
        {"validation_id": "VAL2737_0_sources", "passed": source_ok, "detail": "all source paths exist and required anchors/needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2737_1_source_zero_blocked", "passed": source_zero_blocked, "detail": "N_src exact-zero route is audited and blocked", "timestamp_utc": ts()},
        {"validation_id": "VAL2737_2_inner_zero_blocked", "passed": inner_zero_blocked, "detail": "N_inner exact-zero route is audited and blocked", "timestamp_utc": ts()},
        {"validation_id": "VAL2737_3_total_Scg_envelope", "passed": envelope_ok, "detail": "total S_cg source-support envelope and N_src bound are staged", "timestamp_utc": ts()},
        {"validation_id": "VAL2737_4_first_pair_bound", "passed": first_pair_ok, "detail": "N_pair bound exists and remains nonclaim", "timestamp_utc": ts()},
        {"validation_id": "VAL2737_5_claim_gates_false", "passed": gates_false, "detail": "all local and arena claims remain blocked", "timestamp_utc": ts()},
        {"validation_id": "VAL2737_6_next_target", "passed": next_ok, "detail": "next target is a shared worldtube/profile and inner-charge template", "timestamp_utc": ts()},
        {"validation_id": "VAL2737_7_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2737_8_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2737_9_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_recent_count()}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2737_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2737 rejects exact source-support and inner-charge silence for now, stages the first-pair bound, and selects a shared worldtube/profile template next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2737 - Y5 R2/f(R): Source Support And Inner Charge Theorem Or Bound Under AX1090

Status: `Y5_R2FR_2737_exact_first_pair_silence_blocked_Npair_bound_staged_nonclaim`

## Private Verdict

I tried the clean theorem route first. It does **not** close yet.

The exact route would need both:

`N_src=||U_B S_cg,total||_{{E*}}=0`

and

`N_inner=0` from `Q_m^H=0` plus boundary/no-flux/zero-mode/domain silence.

Current evidence does not sign either one. `U_B=0` is not proved, the total compact-source support still has sibling hidden-source channels, and the compact inner boundary charge is explicitly not automatic.

The useful result is the first-pair bound:

`N_pair <= U_B,max S_cg,total_norm + C_inner |Q_m^H| + N_inner,domain + N_inner,zero_mode`,

then

`N_lock <= N_pair + N_rest` and `Delta_m <= C_emb (N_pair+N_rest)`.

That is the honest bridge toward local GR: not a handwave, not a fake zero, but a fillable source/profile/charge contract.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## Source Support Zero Audit

{markdown_table(data["source_zero"], ["zero_id", "target", "law_or_condition", "status", "reason", "missing_to_promote", "zero_proved", "valid_for_claim"])}

## Inner Charge Zero Audit

{markdown_table(data["inner_zero"], ["inner_id", "target", "law_or_condition", "status", "reason", "missing_to_promote", "zero_proved", "valid_for_claim"])}

## Total S_cg Envelope Rows

{markdown_table(data["envelope"], ["envelope_id", "quantity", "formula_or_rule", "status", "missing_to_promote", "valid_for_claim"])}

## First-Pair Bound Contract

{markdown_table(data["first_pair"], ["pair_id", "quantity", "formula_or_rule", "meaning", "status", "missing_to_promote", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "because", "effect", "valid_for_claim"])}

## Claim Gates

{markdown_table(data["gates"], ["claim_gate_id", "claim", "gate_passed", "claim_allowed", "valid_for_claim", "reason"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is the coupling wound you felt in your bones, but now it has handles. The next move is not “believe harder”; it is one shared worldtube/source-profile template that owns the source size, support, inner charge, and arena maps without sneaking in orbital `GM`. That is the proper engineering version of the leap.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    source_zero = source_zero_rows()
    inner_zero = inner_zero_rows()
    envelope = envelope_rows()
    first_pair = first_pair_rows()
    decisions = decision_rows()
    gates = gate_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["source_zero"], source_zero)
    write_csv(OUTPUTS["inner_zero"], inner_zero)
    write_csv(OUTPUTS["envelope"], envelope)
    write_csv(OUTPUTS["first_pair"], first_pair)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["first_pair"], first_pair)
    write_csv(BRANCH_OUTPUTS["reopen"], [*source_zero, *inner_zero])
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    validation = validation_rows(sources, source_zero, inner_zero, envelope, first_pair, gates, next_target)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "source_zero": source_zero,
        "inner_zero": inner_zero,
        "envelope": envelope,
        "first_pair": first_pair,
        "decisions": decisions,
        "gates": gates,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2737 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
