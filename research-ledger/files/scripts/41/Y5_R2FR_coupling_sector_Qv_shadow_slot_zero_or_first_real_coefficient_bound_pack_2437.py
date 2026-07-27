from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_COUPLING_SECTOR_QV_SHADOW_SLOT_ZERO_OR_FIRST_REAL_COEFFICIENT_BOUND_PACK_2437"
CHECKPOINT_ID = "2437"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2437-Y5-R2FR-coupling-sector-Qv-shadow-slot-zero-or-first-real-coefficient-bound-pack.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2437_SOURCE_REGISTER.csv",
    "coupling_zero": OUT / "P8_Y5_PARENT_QLOC_2437_COUPLING_ZERO_THEOREM_ATTEMPT.csv",
    "shadow_basis": OUT / "P8_Y5_PARENT_QLOC_2437_SHADOW_COEFFICIENT_BASIS.csv",
    "channel_map": OUT / "P8_Y5_PARENT_QLOC_2437_QV_JQ_CHANNEL_MAP.csv",
    "bound_pack": OUT / "P8_Y5_PARENT_QLOC_2437_FIRST_COEFFICIENT_BOUND_PACK_NONCLAIM.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2437_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2437_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2437_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2437_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2437_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_theorem": QUEUE / "JR2437_COUPLING_ZERO_THEOREM_ATTEMPT_NONCLAIM.csv",
    "queue_bounds": QUEUE / "JR2437_FIRST_COEFFICIENT_BOUND_PACK_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "coupling_shadow_coefficient_bound_pack_nonclaim_2437.csv",
    "beta_docs": BETA_DOCS / "COUPLING_SHADOW_BOUND_PACK_2437_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2437_00_2436_handoff",
        "source_path": ROOT / "2436-Y5-R2FR-Qv-sector-piece-ledger-or-real-balpha-bg-source-acquisition.md",
        "needles": ["QVSL2436_2_coupling_source_shadow", "NEXT2436_0_selected", "VAL2436_OVERALL"],
        "role": "fresh handoff selecting coupling/source-shadow as rank-1",
    },
    {
        "source_id": "SRC2437_01_2401_shadow_zero",
        "source_path": ROOT / "2401-Y5-R2FR-source-shadow-functional-exclusion-parent-action-grammar-or-shadow-bound-pack.md",
        "needles": ["SSE2401_3_zero_if_contract_signed", "SBP2401_0_delta_w_shadow", "VAL2401_OVERALL"],
        "role": "exact conditional source-shadow zero theorem",
    },
    {
        "source_id": "SRC2437_02_2402_shadow_basis",
        "source_path": ROOT / "2402-Y5-R2FR-parent-action-normal-form-ownership-signer-or-shadow-coefficient-acquisition.md",
        "needles": ["NFT2402_1_shadow_expansion", "NFT2402_2_zero_condition", "VAL2402_OVERALL"],
        "role": "finite owner-indexed source-shadow coefficient basis",
    },
    {
        "source_id": "SRC2437_03_2403_minimal_candidate",
        "source_path": ROOT / "2403-Y5-R2FR-minimal-parent-action-normal-form-candidate-or-off-contract-coefficient-bound-pack.md",
        "needles": ["MPA2403_5_forbidden_terms", "ADS2403_3_no_shadow", "VAL2403_OVERALL"],
        "role": "minimal parent action candidate with off-contract zero clauses labelled as axioms",
    },
    {
        "source_id": "SRC2437_04_2399_block_refinement",
        "source_path": ROOT / "2399-Y5-R2FR-species-label-forgetting-source-functor-parent-proof-or-deltaw-species-bound.md",
        "needles": ["SLF2399_6_current_verdict", "DWS2399_1_delta_w_block", "VAL2399_OVERALL"],
        "role": "species/source-prefactor refinement to block/source-shadow residual",
    },
    {
        "source_id": "SRC2437_05_2400_exchange_shadow",
        "source_path": ROOT / "2400-Y5-R2FR-ordinary-matter-exchange-graph-connectivity-and-source-shadow-ban-or-deltaw-block-bound.md",
        "needles": ["CONN2400_4_current_verdict", "SSB2400_3_current_verdict", "VAL2400_OVERALL"],
        "role": "exchange graph collapse and source-shadow blocker",
    },
    {
        "source_id": "SRC2437_06_2431_Jq",
        "source_path": ROOT / "2431-Y5-R2FR-Jq-source-leg-zero-theorem-or-component-bound-vector.md",
        "needles": ["JZT2431_1_descent_lemma", "JQC2431_9_total_abs", "VAL2431_OVERALL"],
        "role": "J_q chain-rule descent and absolute component-bound vector",
    },
    {
        "source_id": "SRC2437_07_2432_coeff_functor",
        "source_path": ROOT / "2432-Y5-R2FR-parent-observed-coefficient-functor-or-first-Jq-bound-row.md",
        "needles": ["OCF2432_1_chain_rule", "OBS2432_5_verdict", "VAL2432_OVERALL"],
        "role": "observed coefficient functor and hidden-visible countermodels",
    },
    {
        "source_id": "SRC2437_08_2434_typed_basis",
        "source_path": ROOT / "2434-Y5-R2FR-parent-typed-object-language-and-vertical-basis-certificate-or-balpha-bg-bound-row.md",
        "needles": ["TOL2434_7_verdict", "VBC2434_6_verdict", "VAL2434_OVERALL"],
        "role": "typed object-language and vertical-basis owner gate",
    },
    {
        "source_id": "SRC2437_09_2435_qv_target",
        "source_path": ROOT / "2435-Y5-R2FR-vertical-Noether-charge-Qv-and-typed-target-exclusion-or-balpha-bg-source-row.md",
        "needles": ["QV2435_5_verdict", "TEX2435_4_verdict", "SRCROW2435_3_verdict", "VAL2435_OVERALL"],
        "role": "Q_v extraction and typed target exclusion failure, b_alpha/b_g source skeletons",
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(row.get(key, "")) for key in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        cells = [stringify(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source["source_id"],
                source_path=path,
                path_exists=path.exists(),
                required_needles="; ".join(needles),
                found_needles="; ".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=source["role"],
            )
        )
    return rows


def coupling_zero_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "test_id": "CZT2437_0_define_sector",
            "clause": "coupling/source-shadow sector definition",
            "formula": "S_coup := S_shadow + S_nonminimal + S_frame + S_coeff + S_source_weight + S_postreadout, i.e. every term able to alter T_active, visible coefficients, or q source legs outside minimal observed-frame matter.",
            "current_status": "DEFINED_FINITE_TARGET",
            "consequence": "the old vague coupling worry is a finite object",
            "gate_pass": True,
        },
        {
            "test_id": "CZT2437_1_zero_theorem",
            "clause": "exact conditional zero theorem",
            "formula": "If S_coup is absent by parent grammar, S_ord depends only on q-blind observed objects, coefficients are typed constants or q-blind functors, and readout occurs after variation without reentry, then delta_v S_coup=Theta_coup(v)=mu_coup(v)=Q_v^coup=J_q^coup=0.",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "consequence": "coupling can be killed by construction/theorem, not fitted away",
            "gate_pass": True,
        },
        {
            "test_id": "CZT2437_2_action_normal_form_owner",
            "clause": "parent action normal form signs absence of S_coup",
            "formula": "Arg(S_parent) contains EH/observed geometry, ordinary Hilbert matter, q/residual sector, allowed boundary, but no source-shadow, relative source prefactor, hidden-visible coefficient, or shadow-frame slot.",
            "current_status": "NOT_PARENT_SIGNED",
            "consequence": "2403 can adopt this as a minimal candidate, but adoption is not a derivation",
            "gate_pass": False,
        },
        {
            "test_id": "CZT2437_3_source_shadow_owner",
            "clause": "J_shadow zero",
            "formula": "J_shadow=c_nonminimal J_nonminimal+c_boundary J_boundary+c_projector J_projector+c_frame J_frame+delta_w_decoupled T_D+c_nonHilbert J_nonHilbert=0.",
            "current_status": "FINITE_BASIS_NOT_ZEROED",
            "consequence": "shadow gap is finite but still live",
            "gate_pass": False,
        },
        {
            "test_id": "CZT2437_4_visible_coefficient_owner",
            "clause": "b_alpha/b_g/source-prefactor exclusion",
            "formula": "Hom_parent(hidden/source/readout labels -> alpha, frame, mass, clock, source-weight targets)=empty except fixed representation labels and common calibration.",
            "current_status": "TYPED_TARGET_NOT_PARENT_SIGNED",
            "consequence": "b_alpha, b_g and delta_w_block remain legal residuals",
            "gate_pass": False,
        },
        {
            "test_id": "CZT2437_5_verdict",
            "clause": "coupling-sector Q_v/J_q zero for current MTS",
            "formula": "CZT2437_1 promotes only if CZT2437_2..4 pass in the same parent branch.",
            "current_status": "ZERO_NOT_PROMOTED_BOUND_PACK_REQUIRED",
            "consequence": "move from pure derivation attempt to a source-ready coefficient basis unless a parent constructor theorem is supplied",
            "gate_pass": False,
        },
    ]
    return [base_row(**row) for row in rows]


def shadow_basis_rows() -> list[dict[str, Any]]:
    rows = [
        ("SCB2437_0_delta_w_block", "delta_w_block", "relative active-source weight over disconnected ordinary exchange blocks", "dimensionless", "zero if ordinary exchange graph is one connected source component and no shadow returns", "MISSING_EXCHANGE_GRAPH_CONNECTIVITY_OR_BOUND"),
        ("SCB2437_1_delta_w_shadow", "delta_w_shadow", "effective source-weight leakage from non-Hilbert/post-Hilbert shadow current", "dimensionless_if_J_shadow_normalized_to_T_H", "zero if source-shadow functional is excluded by parent grammar", "MISSING_SOURCE_SHADOW_ZERO_OR_BOUND"),
        ("SCB2437_2_c_nonminimal", "c_nonminimal", "coefficient of explicit nonminimal matter/source coupling", "action_density_or_dimensionless_after_MHref", "zero if no nonminimal owner exists in parent normal form", "MISSING_NONMINIMAL_OWNER_ZERO_OR_BOUND"),
        ("SCB2437_3_c_projector", "c_projector", "coefficient of projector/source-worldtube/readout reentry source term", "arena_projector_units", "zero if Pi_W chain-map and variation-before-readout are parent-signed", "MISSING_PROJECTOR_CHAINMAP_ZERO_OR_BOUND"),
        ("SCB2437_4_c_frame_bg", "b_g", "shadow-frame/coframe Weyl/disformal slope in observed geometry/readout", "dimensionless_or_per_q_unit", "zero if observed frame is quotient-basic and no hidden frame target exists", "MISSING_FRAME_BASICNESS_OR_BOUND"),
        ("SCB2437_5_b_alpha", "b_alpha", "hidden-visible EM/fine-structure/gauge kinetic slope", "dimensionless_or_per_q_unit", "zero if EM/charge levels are fixed representation data with no hidden target", "MISSING_ALPHA_TARGET_EXCLUSION_OR_BOUND"),
        ("SCB2437_6_c_nonHilbert", "c_nonHilbert", "spin/torsion/non-Hilbert current leakage after improvement conventions", "connection_source_units", "zero if Belinfante/improvement and public coframe normal form close", "MISSING_NONHILBERT_OWNER_ZERO_OR_BOUND"),
        ("SCB2437_7_total_abs", "B_coupling_abs", "absolute no-cancellation coupling residual envelope", "sum_of_component_norms", "zero only if every component above is theorem-zero in one parent branch", "SCHEMA_READY_VALUES_MISSING"),
    ]
    return [
        base_row(
            row_id=row_id,
            symbol=symbol,
            definition=definition,
            units=units,
            zero_route=zero_route,
            current_status=status,
            theorem_zero=False,
            source_backed=False,
            score_ready=False,
        )
        for row_id, symbol, definition, units, zero_route, status in rows
    ]


def channel_map_rows() -> list[dict[str, Any]]:
    rows = [
        ("CH2437_0_Qv_coupling", "Q_v^coupling", "Theta_coup(v)-mu_coup(v)", "SCB2437_1_delta_w_shadow;SCB2437_2_c_nonminimal;SCB2437_3_c_projector;SCB2437_4_c_frame_bg", "kernel can carry physical vertical charge if coupling slot survives"),
        ("CH2437_1_Jq_source_norm", "J_q^source_norm", "vertical derivative of active-source normalization", "SCB2437_0_delta_w_block;SCB2437_1_delta_w_shadow", "feeds q no-hair source leg and R10/WEP source charge"),
        ("CH2437_2_Jq_marker", "J_q^marker", "vertical derivative of visible EM/material coefficients", "SCB2437_5_b_alpha", "feeds clocks, EM, WEP composition and particle/material channels"),
        ("CH2437_3_Jq_frame", "J_q^frame", "vertical derivative of observed frame/coframe coefficient", "SCB2437_4_c_frame_bg", "feeds PPN, clocks, R10 and local metric response"),
        ("CH2437_4_projector_readout", "J_q^projector_readout", "post-variation source-worldtube/projector transfer", "SCB2437_3_c_projector", "can mimic source normalization or hide q/body charge in readout"),
        ("CH2437_5_total", "B_total_coupling_to_local", "absolute sum of coupling-sector residual channels", "SCB2437_7_total_abs", "no cancellation allowed; all arenas stay blocked until components are zero or source-backed"),
    ]
    return [
        base_row(
            channel_id=channel_id,
            channel=channel,
            definition=definition,
            component_rows=components,
            local_effect=effect,
            gate_pass=False,
        )
        for channel_id, channel, definition, components, effect in rows
    ]


def bound_pack_rows() -> list[dict[str, Any]]:
    rows = [
        ("CBP2437_0_delta_w_block", "delta_w_block", "WEP;R10;PPN;clock;orbital;source_normalization", "dimensionless", "K_WEP_block;K_R10_block;K_PPN_block;K_clock_block;K_orbital_block", "MISSING_REAL_SOURCE_TABLE_AND_PARENT_BLOCK_BASIS"),
        ("CBP2437_1_delta_w_shadow", "delta_w_shadow", "WEP;R10;PPN;clock;q_loc", "dimensionless_if_normalized", "K_shadow_to_arena", "MISSING_SHADOW_BASIS_AND_SOURCE_BOUNDS"),
        ("CBP2437_2_b_alpha", "b_alpha", "clock;EM;WEP;R10", "dimensionless_or_per_q_unit", "K_alpha_clock;K_alpha_WEP;K_alpha_R10", "MISSING_PARENT_ALPHA_OWNER_AND_SOURCE_BOUND"),
        ("CBP2437_3_b_g", "b_g", "PPN;clock;R10;WEP;orbital", "dimensionless_or_per_q_unit", "K_bg_PPN;K_bg_clock;K_bg_R10", "MISSING_FRAME_OWNER_AND_PRODUCT_LAW_PROJECTION"),
        ("CBP2437_4_c_projector", "c_projector", "R10;orbital;source_normalization;PPN", "operator_or_projector_units", "K_projector_worldtube", "MISSING_CHAINMAP_RESIDUAL_SOURCE_BOUND"),
        ("CBP2437_5_total_abs", "B_coupling_abs", "all_local_arenas", "absolute_component_sum", "sum of nonnegative component projections only", "NO_NUMERIC_FILL_UNTIL_COMPONENTS_SOURCE_BACKED"),
    ]
    return [
        base_row(
            pack_id=pack_id,
            symbol=symbol,
            arena_links=arenas,
            units=units,
            required_projection_coefficients=projections,
            current_status=status,
            numeric_value="",
            source_path="",
            extraction_method="",
            no_cancellation=True,
            source_backed=False,
            score_ready=False,
        )
        for pack_id, symbol, arenas, units, projections, status in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2437_0_coupling_zero", "coupling/source-shadow Q_v and J_q piece is zero", "BLOCKED", "exact conditional theorem exists but parent normal-form/no-shadow/typed target clauses are unsigned"),
        ("CG2437_1_shadow_zero", "J_shadow=0", "BLOCKED", "finite shadow coefficient basis is not zeroed"),
        ("CG2437_2_balpha_bg_zero", "b_alpha=b_g=0", "BLOCKED", "typed target exclusion and vertical basis certificate are not parent-signed"),
        ("CG2437_3_bound_pack_score", "coefficient bound pack can score", "BLOCKED", "pack is schema-ready but has no real source-backed values, q normalization, or projection matrix"),
        ("CG2437_4_local_GR", "local GR/Newton/PPN/WEP/R10 pass", "BLOCKED", "requires coupling zero/bounds plus q no-hair, boundary, projector and total Q_v gates"),
    ]
    return [base_row(claim_id=claim_id, claim=claim, gate_status=status, reason=reason, gate_pass=False) for claim_id, claim, status, reason in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2437_0_theorem_gain", "COUPLING_ZERO_THEOREM_EXACT_BUT_CONDITIONAL", "The zero route is now one compact theorem: absent coupling/shadow slots plus q-blind coefficients imply zero Q_v/J_q coupling channel.", "use this theorem as the contract"),
        ("DEC2437_1_current_failure", "CURRENT_CORPUS_DOES_NOT_SIGN_THE_CONTRACT", "Normal-form absence, source-shadow exclusion, no-hidden-visible targets and vertical basis are not all parent-owned.", "do not claim zero"),
        ("DEC2437_2_bound_basis", "FINITE_BOUND_BASIS_IS_READY", "The fallback is no longer arbitrary: delta_w_block, delta_w_shadow, b_alpha, b_g, c_projector and total absolute envelope are the first rows.", "next can acquire real sources without inventing theory values"),
        ("DEC2437_3_best_next", "MOVE_TO_SOURCE_ACQUISITION_OR_CONSTRUCTOR_SIGNATURE", "Repeating the same theorem has low yield; either sign a parent constructor that forbids the slots, or start real source-backed coefficient acquisition.", "select 2438"),
        ("DEC2437_4_public", "NO_GITHUB_ACTION", "This is private derivation/bound scaffolding; all claim gates remain false.", "continue private framework work"),
    ]
    return [base_row(decision_id=row_id, decision=decision, rationale=rationale, consequence=consequence) for row_id, decision, rationale, consequence in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2437_0_selected",
            selection_status="selected",
            target_file="2438-Y5-R2FR-first-real-coupling-coefficient-bound-source-acquisition-or-no-shadow-constructor-signature.md",
            target_script="scripts/Y5_R2FR_first_real_coupling_coefficient_bound_source_acquisition_or_no_shadow_constructor_signature_2438.py",
            task="either parent-sign a constructor theorem forbidding coupling/source-shadow/hidden-visible coefficient slots, or acquire real source-backed nonclaim bounds for delta_w_block, delta_w_shadow, b_alpha, b_g and c_projector with arena projections",
            acceptance_target="one constructor clause becomes parent-signed, or the first coefficient row has real source path, units, extraction method, projection map, no-cancellation group, and valid_for_claim=false until complete",
            guardrails="do not fabricate values, do not use local bounds as theory coefficients, do not cancel tails, do not claim local GR/R10/PPN/WEP/clock/orbital pass, do not edit formalization-workbench, and do not push GitHub",
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue_theorem", OUTPUTS["coupling_zero"], COPY_TARGETS["queue_theorem"], "coupling zero theorem attempt nonclaim queue"),
        ("queue_bounds", OUTPUTS["bound_pack"], COPY_TARGETS["queue_bounds"], "first coefficient bound pack nonclaim queue"),
        ("branch_wep", OUTPUTS["bound_pack"], COPY_TARGETS["branch_wep"], "WEP/local branch coupling coefficient pack"),
        ("beta_docs", OUTPUTS["shadow_basis"], COPY_TARGETS["beta_docs"], "beta docs coupling-shadow coefficient basis"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target, note in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            base_row(
                copy_id=copy_id,
                source_path=source,
                target_path=target,
                source_exists=source.exists(),
                target_exists=target.exists(),
                notes=note,
            )
        )
    return rows


def formalization_hits() -> list[Path]:
    patterns = [
        "*2437-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2437*",
        "*P8_Y5_BRR545_2437*",
        "*JR2437*",
        "*COUPLING_SHADOW_BOUND_PACK_2437*",
    ]
    hits: list[Path] = []
    if not FORMALIZATION.exists():
        return hits
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return hits


def validation_rows(outputs: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sources = outputs["source_register"]
    rows.append(base_row(check_id="VAL2437_00_sources_exist", status="PASS" if all(row["path_exists"] == True for row in sources) else "FAIL", notes="all cited source paths exist"))
    rows.append(base_row(check_id="VAL2437_01_source_needles", status="PASS" if all(row["needles_found"] == True for row in sources) else "FAIL", notes="all cited source needles are present"))

    coupling = outputs["coupling_zero"]
    rows.append(base_row(check_id="VAL2437_02_conditional_theorem_present", status="PASS" if any(row["test_id"] == "CZT2437_1_zero_theorem" and row["gate_pass"] == True for row in coupling) else "FAIL", notes="coupling zero theorem is written as an exact conditional"))
    rows.append(base_row(check_id="VAL2437_03_zero_not_promoted", status="PASS" if any(row["test_id"] == "CZT2437_5_verdict" and row["gate_pass"] == False for row in coupling) else "FAIL", notes="current MTS coupling zero is not promoted"))

    basis = outputs["shadow_basis"]
    required_symbols = {"delta_w_block", "delta_w_shadow", "b_alpha", "b_g", "B_coupling_abs"}
    present_symbols = {row["symbol"] for row in basis}
    rows.append(base_row(check_id="VAL2437_04_bound_basis_present", status="PASS" if required_symbols.issubset(present_symbols) else "FAIL", notes="finite coupling/source-shadow coefficient basis includes delta_w, b_alpha, b_g and total envelope"))
    rows.append(base_row(check_id="VAL2437_05_basis_nonclaim", status="PASS" if all(row.get("source_backed") == False and row.get("score_ready") == False for row in basis) else "FAIL", notes="shadow coefficient basis remains nonclaim/unscored"))

    pack = outputs["bound_pack"]
    rows.append(base_row(check_id="VAL2437_06_pack_nonclaim_no_values", status="PASS" if all(row.get("numeric_value") == "" and row.get("source_backed") == False and row.get("score_ready") == False for row in pack) else "FAIL", notes="first coefficient pack has no fabricated numeric values"))

    claims = outputs["claim_gates"]
    rows.append(base_row(check_id="VAL2437_07_claims_blocked", status="PASS" if all(row.get("gate_pass") == False and row.get("valid_for_claim") == False for row in claims) else "FAIL", notes="all coupling/local claim gates remain blocked"))
    rows.append(base_row(check_id="VAL2437_08_next_target_written", status="PASS" if outputs["next_target"][0]["target_file"].startswith("2438-") else "FAIL", notes="2438 source-acquisition/constructor target selected"))

    hits = formalization_hits()
    rows.append(base_row(check_id="VAL2437_09_no_formalization_artifacts", status="PASS" if not hits else "FAIL", notes="no 2437 artifacts were written to formalization-workbench" if not hits else "formalization-workbench contains 2437 artifacts", detail="; ".join(str(hit) for hit in hits)))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parses(path)
        rows.append(base_row(check_id=f"VAL2437_CSV_{path.stem}", status="PASS" if ok and count > 0 else "FAIL", notes=f"CSV parses with {count} rows" if ok else "CSV parse failed", detail=detail))

    overall_pass = all(row["status"] == "PASS" for row in rows)
    rows.append(base_row(check_id="VAL2437_OVERALL", status="PASS" if overall_pass else "FAIL", notes="2437 proves the coupling zero route only conditionally, refuses promotion, creates the finite coefficient-bound basis, and selects real source acquisition or constructor signature next"))
    return rows


def write_doc(outputs: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2437 - Y5/R2FR Coupling Sector Qv Shadow Slot Zero Or First Real Coefficient Bound Pack",
        "",
        "## Result",
        "- 2437 takes the leap at the coupling wound: the coupling/source-shadow sector has an exact conditional zero theorem.",
        "- If the parent action truly has no source-shadow, no relative source-prefactor, no hidden-visible coefficient target, and no shadow-frame slot, then the coupling contribution to `Q_v`, `J_q`, `b_alpha`, `b_g`, and source weights vanishes.",
        "- Current MTS does not yet sign those parent clauses.  The result is not a local-GR pass.",
        "- The fallback is now finite rather than vague: `delta_w_block`, `delta_w_shadow`, `b_alpha`, `b_g`, `c_projector`, and an absolute no-cancellation envelope.",
        "- Next useful move is not another restatement: either parent-sign the no-shadow constructor, or acquire the first real source-backed nonclaim bound row.",
        "",
        "## Source Register",
        table(["source_id", "source_path", "path_exists", "needles_found", "role"], outputs["source_register"]),
        "",
        "## Coupling Zero Theorem Attempt",
        table(["test_id", "clause", "formula", "current_status", "consequence", "gate_pass", "valid_for_claim"], outputs["coupling_zero"]),
        "",
        "## Shadow Coefficient Basis",
        table(["row_id", "symbol", "definition", "units", "zero_route", "current_status", "source_backed", "score_ready", "valid_for_claim"], outputs["shadow_basis"]),
        "",
        "## Qv / Jq Channel Map",
        table(["channel_id", "channel", "definition", "component_rows", "local_effect", "gate_pass", "valid_for_claim"], outputs["channel_map"]),
        "",
        "## First Coefficient Bound Pack",
        table(["pack_id", "symbol", "arena_links", "units", "required_projection_coefficients", "current_status", "numeric_value", "source_path", "no_cancellation", "source_backed", "score_ready", "valid_for_claim"], outputs["bound_pack"]),
        "",
        "## Claim Gates",
        table(["claim_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"], outputs["claim_gates"]),
        "",
        "## Decision Ledger",
        table(["decision_id", "decision", "rationale", "consequence", "valid_for_claim"], outputs["decisions"]),
        "",
        "## Next Target",
        table(["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"], outputs["next_target"]),
        "",
        "## Branch Copies",
        table(["copy_id", "source_path", "target_path", "source_exists", "target_exists", "notes"], outputs["branch_copies"]),
        "",
        "## Validation",
        table(["check_id", "status", "notes", "detail"], outputs["validation"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "coupling_zero": coupling_zero_rows(),
        "shadow_basis": shadow_basis_rows(),
        "channel_map": channel_map_rows(),
        "bound_pack": bound_pack_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next_target": next_target_rows(),
    }

    for key, rows in outputs.items():
        write_csv(OUTPUTS[key], rows)

    outputs["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], outputs["branch_copies"])

    outputs["validation"] = validation_rows(outputs)
    write_csv(OUTPUTS["validation"], outputs["validation"])
    write_doc(outputs)

    print(DOC)
    print(OUTPUTS["validation"])
    overall = next(row for row in outputs["validation"] if row["check_id"] == "VAL2437_OVERALL")
    print(f"VAL2437_OVERALL={overall['status']}")


if __name__ == "__main__":
    main()
