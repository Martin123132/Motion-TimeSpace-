from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2198"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2198-Y5-R2FR-beta-source-zero-or-bounded-component-pack.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2198_SOURCE_REGISTER.csv",
    "source_zero_identity": OUT / "P8_Y5_PARENT_QLOC_2198_SOURCE_ZERO_IDENTITY_CURRENT.csv",
    "component_vector": OUT / "P8_Y5_PARENT_QLOC_2198_BOUNDED_COMPONENT_VECTOR.csv",
    "first_proxy_pressure": OUT / "P8_Y5_PARENT_QLOC_2198_FIRST_PROXY_PRESSURE_ROW.csv",
    "translation_blockers": OUT / "P8_Y5_PARENT_QLOC_2198_TRANSLATION_BLOCKER_GATE.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2198_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2198_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2198_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2198_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2198_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2198_BETA_SOURCE_ZERO_COMPONENT_VECTOR_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2198_BOUNDED_COMPONENT_VECTOR_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "PARENT_QLOC_FIRST_PROXY_PRESSURE_2198_NONCLAIM.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        values = []
        for column in columns:
            values.append(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|"))
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2198_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2198-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2198*",
        "*P8_Y5_BRR545_2198*",
        "*Y5_R2FR_beta_source_zero_or_bounded_component_pack_2198*",
        "*JR2198*",
        "*PARENT_QLOC_FIRST_PROXY_PRESSURE_2198*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2197_doc",
            ROOT / "2197-Y5-R2FR-parent-ZX-residue-or-beta-leg-source-first-row.md",
            ["Best next attack: build the beta/source-zero component pack", "SELECT_BETA_OR_SOURCE_ZERO_NEXT", "VAL2197_OVERALL"],
            "Current handoff from Z_X owner failure to beta/source-zero component pack.",
        ),
        (
            "2158_doc",
            ROOT / "2158-Y5-R2FR-JX-qbarXT-source-zero-or-bounded-coupling-component-pack.md",
            ["J_X=qbar_XT=0 is not a current claim", "bounded component rows remain mandatory", "VAL2158_OVERALL"],
            "Existing exact source-zero identity and component vector.",
        ),
        (
            "2158_component_pack",
            OUT / "P8_Y5_PARENT_QLOC_2158_BOUNDED_COUPLING_COMPONENT_PACK.csv",
            ["BCP2158_0_cg", "BCP2158_10_total", "SCHEMA_READY_VALUES_MISSING"],
            "Machine-readable bounded coupling component pack.",
        ),
        (
            "2159_doc",
            ROOT / "2159-Y5-R2FR-parent-ordinary-matter-signature-or-first-coupling-bound-row.md",
            ["Cassini gives a clean scalar-tensor alpha proxy", "SOURCE_BACKED_PROXY_DIRECT_MTS_BOUND_MISSING", "VAL2159_OVERALL"],
            "First source-backed coupling proxy and MOMS failure.",
        ),
        (
            "2159_first_proxy",
            OUT / "P8_Y5_PARENT_QLOC_2159_FIRST_COUPLING_BOUND_SOURCE_ROW.csv",
            ["FBS2159_1_scalar_tensor_alpha_proxy", "0.005788015401465051", "direct_mts_component_bound"],
            "Machine-readable Cassini/scalar-tensor proxy source rows.",
        ),
        (
            "2160_doc",
            ROOT / "2160-Y5-R2FR-PPN-common-frame-cg-translation-and-normalization-gate.md",
            ["alpha_eff_PPN", "SOURCE_PROXY_ONLY", "VAL2160_OVERALL"],
            "PPN translation gate proving Cassini remains proxy-only for current MTS.",
        ),
        (
            "1852_doc",
            ROOT / "1852-Y5-R2FR-PPN-common-frame-cg-translation-gate.md",
            ["|alpha_PPN| <= 0.00578802", "MISSING_NX_FROM_ZX_HESSIAN", "VAL1852_OVERALL"],
            "Original Cassini alpha proxy derivation.",
        ),
        (
            "1849_doc",
            ROOT / "1849-Y5-R2FR-qbarXT-source-zero-or-bounded-coupling-row.md",
            ["qbar_XT=0/J_X=0 is an exact conditional theorem", "SCHEMA_READY_VALUES_MISSING", "VAL1849_OVERALL"],
            "Earlier source-zero or bounded qbar_XT schema.",
        ),
        (
            "1028_doc",
            ROOT / "1028-Y5-R10-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md",
            ["no-marker/constant-descent route is clean as a conditional theorem", "qbar_XT_bound_abs", "CLAIM_BLOCKED"],
            "R10 predecessor for marker/frame/source component pack.",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=path.exists(),
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def source_zero_identity_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            identity_id="SZI2198_0_definition",
            statement="qbar_XT := M_T^-1 delta_{v_X} S_T and J_X is the bulk source coefficient of delta Xhat",
            proof_status="DEFINITION_ONLY",
            missing_premise="parent-owned v_X/Xhat normalization and source measure",
            local_gr_relevance="defines what must vanish for ordinary local matter to see only GR/Newton fields",
        ),
        base_row(
            identity_id="SZI2198_1_chain_rule",
            statement="delta_v S_matter is the sum of observed-frame Lie derivatives, constant/marker derivatives, matter lift/EOM terms and boundary/support terms",
            proof_status="EXACT_CONDITIONAL_IDENTITY",
            missing_premise="observed matter frame, constant sector, matter lift and boundary class must be parent-owned",
            local_gr_relevance="turns source silence into clauses rather than rhetoric",
        ),
        base_row(
            identity_id="SZI2198_2_zero_theorem",
            statement="If Dq[v_X]=0, ordinary matter descends through q, constants/markers are X-trivial, no hidden source weights exist and boundary/support tails vanish, then J_X=qbar_XT=0",
            proof_status="EXACT_THEOREM_UNDER_UNSIGNED_PREMISES",
            missing_premise="single parent ordinary-matter signature proving every premise together",
            local_gr_relevance="cleanest derivation route to local GR source silence",
        ),
        base_row(
            identity_id="SZI2198_3_verdict",
            statement="current MTS does not yet prove J_X=qbar_XT=0",
            proof_status="FAIL_CURRENT_CLAIM_CONTRACT_SHARPENED",
            missing_premise="ordinary-matter signature, no-hidden-visible-hom, common measure, constants and readout order",
            local_gr_relevance="bounded component rows remain mandatory",
        ),
    ]


def component_vector_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            component_id="BCV2198_0_cg",
            symbol="c_g",
            role="universal/common Weyl frame leg",
            current_best_anchor="Cassini gamma / scalar-tensor alpha proxy",
            blocker="MISSING_ZX_TAU_PPN_RANGE_VECTOR",
            bound_status="SOURCE_BACKED_PROXY_TRANSLATION_MISSING",
            no_cancellation_rule="must enter absolute PPN/R10/local residual vector unless theorem-zero closes",
            component_bound_claim=False,
            score_ready=False,
        ),
        base_row(
            component_id="BCV2198_1_bdis",
            symbol="b_dis",
            role="disformal/preferred-frame leg",
            current_best_anchor="PPN/clock/orbital anchors exist only as external pressure",
            blocker="MISSING_DISFORMAL_PROJECTION",
            bound_status="OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING",
            no_cancellation_rule="cannot cancel c_g or q_nonH without signed correlation theorem",
            component_bound_claim=False,
            score_ready=False,
        ),
        base_row(
            component_id="BCV2198_2_bA",
            symbol="b_A",
            role="material mass/species constant marker",
            current_best_anchor="MICROSCOPE/LLR/clock-style anchors",
            blocker="MISSING_MATERIAL_SENSITIVITY_MAP",
            bound_status="OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING",
            no_cancellation_rule="composition tails add in absolute value",
            component_bound_claim=False,
            score_ready=False,
        ),
        base_row(
            component_id="BCV2198_3_balpha",
            symbol="b_alpha",
            role="EM/fine-structure or electromagnetic binding marker",
            current_best_anchor="clock/fine-structure anchors",
            blocker="MISSING_X_PROFILE_OR_TIME_PROJECTION",
            bound_status="OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING",
            no_cancellation_rule="clock/EM marker legs are not killed by universal WEP",
            component_bound_claim=False,
            score_ready=False,
        ),
        base_row(
            component_id="BCV2198_4_delta_kappa",
            symbol="delta_kappa_A",
            role="source-only Hilbert/current weight",
            current_best_anchor="MICROSCOPE/LLR/source-charge pressure",
            blocker="MISSING_SOURCE_COMPOSITION_MAP",
            bound_status="OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING",
            no_cancellation_rule="measured-GM calibration tails remain explicit",
            component_bound_claim=False,
            score_ready=False,
        ),
        base_row(
            component_id="BCV2198_5_nonH_support_boundary",
            symbol="q_nonH;Delta_W_support;q_boundary;C_readout",
            role="non-Hilbert/support/domain/boundary/readout source tail",
            current_best_anchor="LLR/orbital/local-bound pressure",
            blocker="MISSING_ORBITAL_SOURCE_SUPPORT_MAP",
            bound_status="OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING",
            no_cancellation_rule="hidden tails are absolute residuals until theorem-zero or source bounds exist",
            component_bound_claim=False,
            score_ready=False,
        ),
        base_row(
            component_id="BCV2198_6_total",
            symbol="J_X_bound_abs;qbar_XT_bound_abs",
            role="total no-cancellation envelope",
            current_best_anchor="2158 component envelope plus 2159/2160 source-backed proxy rows",
            blocker="MISSING_ALL_DIRECT_TRANSLATION_GATES",
            bound_status="COMPONENT_VECTOR_READY_VALUES_MISSING",
            no_cancellation_rule="|total| <= sum absolute live components in each arena",
            component_bound_claim=False,
            score_ready=False,
        ),
    ]


def first_proxy_pressure_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            proxy_id="FPP2198_0_cassini_gamma",
            arena="PPN",
            observable_or_component="gamma_minus_1",
            proxy_value="6.7e-05",
            formula_or_rule="|central| + 2*sigma from Cassini 2003 as carried by 1851/1852/2159",
            source="https://pubmed.ncbi.nlm.nih.gov/14508481/",
            source_backed_proxy=True,
            direct_mts_component_bound=False,
            notes="real observable pressure, not a direct MTS claim",
        ),
        base_row(
            proxy_id="FPP2198_1_alpha_PPN_proxy",
            arena="PPN",
            observable_or_component="alpha_PPN_proxy",
            proxy_value="0.005788015401465051",
            formula_or_rule="sqrt(delta_gamma/(2-delta_gamma)) for an unscreened massless single-scalar tensor proxy",
            source=str(ROOT / "1852-Y5-R2FR-PPN-common-frame-cg-translation-gate.md"),
            source_backed_proxy=True,
            direct_mts_component_bound=False,
            notes="useful pressure on long-range common-frame branches only after translation gates are explicit",
        ),
        base_row(
            proxy_id="FPP2198_2_alpha_eff_PPN",
            arena="PPN",
            observable_or_component="alpha_eff_PPN",
            proxy_value="abs(alpha_eff_PPN)<=0.005788015401465051",
            formula_or_rule="alpha_eff_PPN=tau_PPN*S_PPN*c_g/sqrt(Z_X)+alpha_vec_tail",
            source=str(ROOT / "2160-Y5-R2FR-PPN-common-frame-cg-translation-and-normalization-gate.md"),
            source_backed_proxy=True,
            direct_mts_component_bound=False,
            notes="right current object is effective/vector alpha, not raw c_g",
        ),
        base_row(
            proxy_id="FPP2198_3_raw_cg_block",
            arena="PPN",
            observable_or_component="c_g",
            proxy_value="MISSING_ZX_TAU_RANGE_VECTOR",
            formula_or_rule="abs(c_g)<=alpha_proxy*sqrt(Z_X)/(abs(tau_PPN*S_PPN)) only when vector tails are zero/bounded",
            source=str(ROOT / "2160-Y5-R2FR-PPN-common-frame-cg-translation-and-normalization-gate.md"),
            source_backed_proxy=True,
            direct_mts_component_bound=False,
            notes="raw c_g remains unbounded in current MTS branch",
        ),
    ]


def translation_blocker_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            blocker_id="TBG2198_0_common_frame",
            blocker="universal common matter frame",
            current_status="NOT_PARENT_SIGNED",
            effect_if_missing="species/frame/readout terms can split PPN, WEP, clock and R10 channels",
            next_action="derive no-hidden-visible-hom or retain frame components",
        ),
        base_row(
            blocker_id="TBG2198_1_NX_ZX",
            blocker="canonical normalization N_X=1/sqrt(Z_X)",
            current_status="MISSING_ZX_PARENT_OWNER",
            effect_if_missing="raw c_g can be rescaled; only alpha_eff proxy is meaningful",
            next_action="do not revisit Z_X as a number; either source parent owner or score effective/vector quantities",
        ),
        base_row(
            blocker_id="TBG2198_2_range_screening",
            blocker="lambda_X/S_PPN range or screening transfer",
            current_status="MISSING_LAMBDA_OR_SCREENING_TRANSFER",
            effect_if_missing="Cassini may be suppressed or irrelevant for short-range/local screened modes",
            next_action="route by range: PPN if solar-long, R10 if short, orbital if intermediate",
        ),
        base_row(
            blocker_id="TBG2198_3_vector_tail",
            blocker="PPN/R10 residual vector contamination",
            current_status="MISSING_ABSOLUTE_COMPONENT_VECTOR_VALUES",
            effect_if_missing="single-parameter c_g bound is fake",
            next_action="fill no-cancellation vector over c_g,b_dis,b_A,b_alpha,delta_kappa,q_nonH,support,boundary,readout",
        ),
        base_row(
            blocker_id="TBG2198_4_hidden_visible_hom",
            blocker="visible constants/markers/source weights as hidden X homomorphisms",
            current_status="OPERATOR_DOMAIN_THEOREM_MISSING",
            effect_if_missing="alpha_EM(X), m_A(X), material labels and source weights remain live",
            next_action="derive no-hidden-visible-hom theorem before claiming source-zero",
        ),
    ]


def claim_gate_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    proxy_ok = any(row["proxy_id"] == "FPP2198_1_alpha_PPN_proxy" and row["source_backed_proxy"] is True for row in rows_by_name["first_proxy_pressure"])
    component_claims_false = all(not truthy(row.get("component_bound_claim", False)) for row in rows_by_name["component_vector"])
    return [
        base_row(
            gate_id="CG2198_0_source_zero",
            gate="J_X=qbar_XT source-zero theorem active",
            status="BLOCKED_NONCLAIM",
            implication="identity is exact but ordinary-matter signature premises are unsigned.",
        ),
        base_row(
            gate_id="CG2198_1_component_vector",
            gate="bounded coupling component vector is claim-ready",
            status="BLOCKED_NONCLAIM" if component_claims_false else "FAIL",
            implication="component rows are staged, but direct translation/source values are missing.",
        ),
        base_row(
            gate_id="CG2198_2_source_proxy",
            gate="first source-backed proxy pressure exists",
            status="PASS_NONCLAIM" if proxy_ok else "FAIL",
            implication="Cassini alpha proxy is real pressure, but direct MTS component bound is false.",
        ),
        base_row(
            gate_id="CG2198_3_local_GR_claim",
            gate="local GR/Newton or empirical pass",
            status="BLOCKED_NONCLAIM",
            implication="No local-GR, R10, PPN, clock, orbital, WEP or public claim follows from 2198.",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2198_0_source_zero",
            decision="SOURCE_ZERO_IDENTITY_RETAINED_AS_EXACT_CONDITIONAL",
            rationale="The chain-rule theorem is the clean local-GR route, but current corpus lacks the parent ordinary-matter signature.",
            selection_status="selected",
        ),
        base_row(
            decision_id="DEC2198_1_component_vector",
            decision="LIVE_COUPLING_COMPONENT_VECTOR_CONSOLIDATED",
            rationale="All surviving coupling loopholes are now assigned to frame, marker, source-weight, non-Hilbert/support/boundary/readout components with no-cancellation policy.",
            selection_status="selected",
        ),
        base_row(
            decision_id="DEC2198_2_empirical_pressure",
            decision="CASSINI_PROXY_ADMITTED_AS_SOURCE_BACKED_PRESSURE_ONLY",
            rationale="The alpha_PPN proxy is numeric and useful, but not a direct MTS c_g bound until N_X, range and vector-tail gates close.",
            selection_status="selected",
        ),
        base_row(
            decision_id="DEC2198_3_next",
            decision="ATTACK_NO_HIDDEN_VISIBLE_HOM_OR_PPN_VECTOR_NEXT",
            rationale="Do not circle Z_X again; either derive the operator-domain theorem that zeros visible markers/source weights, or build the full PPN residual vector.",
            selection_status="selected",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2198_0_2199",
            selection_status="selected",
            target_file="2199-Y5-R2FR-no-hidden-visible-hom-or-PPN-vector-envelope.md",
            target_script="scripts/Y5_R2FR_no_hidden_visible_hom_or_PPN_vector_envelope_2199.py",
            objective="try to derive the operator-domain theorem forbidding alpha_EM(X), m_A(X), shadow frames, material markers and source-only weights; if unsigned, build the full PPN no-cancellation vector envelope",
            success_condition="one visible-marker/source-weight channel becomes theorem-zero or the PPN residual vector is explicit enough to route source-backed proxy pressure without one-parameter c_g claims",
            do_not_do="do not revisit raw Z_X as if parent-owned, do not turn Cassini proxy into direct c_g bound, do not ignore b_dis/q_nonH/support/boundary/readout tails, do not claim local GR",
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["component_vector"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["component_vector"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["first_proxy_pressure"], BRANCH_COPIES["source_weight"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=copy_id, source_path=str(source), target_path=str(target), copied=target.exists()))
    return rows


def all_claim_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if truthy(row.get("claim_allowed", False)):
                return False
            if truthy(row.get("valid_for_claim", False)):
                return False
            if truthy(row.get("direct_mts_component_bound", False)):
                return False
    return True


def all_score_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            for key in ("score_ready", "component_bound_claim"):
                if key in row and truthy(row[key]):
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []
    sources = rows_by_name["source_register"]
    validations.append(base_row(validation_id="VAL2198_00_sources_exist", status="PASS" if all(row["path_exists"] for row in sources) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in sources)}/{len(sources)} sources exist"))
    validations.append(base_row(validation_id="VAL2198_01_needles_found", status="PASS" if all(row["needles_found"] for row in sources) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in sources)}/{len(sources)} source needle sets found"))

    identity = rows_by_name["source_zero_identity"]
    identity_ok = any(row["identity_id"] == "SZI2198_2_zero_theorem" and row["proof_status"] == "EXACT_THEOREM_UNDER_UNSIGNED_PREMISES" for row in identity) and any(row["identity_id"] == "SZI2198_3_verdict" and row["proof_status"] == "FAIL_CURRENT_CLAIM_CONTRACT_SHARPENED" for row in identity)
    validations.append(base_row(validation_id="VAL2198_02_source_zero_identity", status="PASS" if identity_ok else "FAIL", detail="source-zero theorem exact but unsigned"))

    components = rows_by_name["component_vector"]
    required_symbols = {"c_g", "b_dis", "b_A", "b_alpha", "delta_kappa_A", "q_nonH;Delta_W_support;q_boundary;C_readout", "J_X_bound_abs;qbar_XT_bound_abs"}
    seen_symbols = {row["symbol"] for row in components}
    component_ok = required_symbols.issubset(seen_symbols) and all(not truthy(row["component_bound_claim"]) for row in components)
    validations.append(base_row(validation_id="VAL2198_03_component_vector", status="PASS" if component_ok else "FAIL", detail=f"{len(required_symbols.intersection(seen_symbols))}/{len(required_symbols)} components staged; all claims false={all(not truthy(row['component_bound_claim']) for row in components)}"))

    proxy = rows_by_name["first_proxy_pressure"]
    alpha_proxy_ok = any(row["proxy_id"] == "FPP2198_1_alpha_PPN_proxy" and row["proxy_value"] == "0.005788015401465051" and truthy(row["source_backed_proxy"]) and not truthy(row["direct_mts_component_bound"]) for row in proxy)
    raw_cg_blocked = any(row["proxy_id"] == "FPP2198_3_raw_cg_block" and row["proxy_value"] == "MISSING_ZX_TAU_RANGE_VECTOR" for row in proxy)
    validations.append(base_row(validation_id="VAL2198_04_proxy_pressure", status="PASS" if alpha_proxy_ok and raw_cg_blocked else "FAIL", detail=f"alpha_proxy_ok={alpha_proxy_ok};raw_cg_blocked={raw_cg_blocked}"))

    blockers = rows_by_name["translation_blockers"]
    blocker_ids = {row["blocker_id"] for row in blockers}
    blocker_ok = {"TBG2198_1_NX_ZX", "TBG2198_2_range_screening", "TBG2198_3_vector_tail", "TBG2198_4_hidden_visible_hom"}.issubset(blocker_ids)
    validations.append(base_row(validation_id="VAL2198_05_translation_blockers", status="PASS" if blocker_ok else "FAIL", detail="normalization, range, vector and hidden-visible blockers recorded"))

    gates = rows_by_name["claim_gate"]
    gates_ok = any(row["gate_id"] == "CG2198_2_source_proxy" and row["status"] == "PASS_NONCLAIM" for row in gates) and any(row["gate_id"] == "CG2198_3_local_GR_claim" and row["status"] == "BLOCKED_NONCLAIM" for row in gates)
    validations.append(base_row(validation_id="VAL2198_06_claim_gate", status="PASS" if gates_ok else "FAIL", detail="proxy passes only as nonclaim; local claims blocked"))

    decisions = {row["decision"] for row in rows_by_name["decision"] if row["selection_status"] == "selected"}
    validations.append(base_row(validation_id="VAL2198_07_decision", status="PASS" if "ATTACK_NO_HIDDEN_VISIBLE_HOM_OR_PPN_VECTOR_NEXT" in decisions else "FAIL", detail="decision selects no-hidden-visible-hom or PPN vector next"))

    routes = {row["route_id"] for row in rows_by_name["next_target"] if row["selection_status"] == "selected"}
    validations.append(base_row(validation_id="VAL2198_08_next_target", status="PASS" if "NEXT2198_0_2199" in routes else "FAIL", detail="2199 target selected"))

    validations.append(base_row(validation_id="VAL2198_09_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false, claim_allowed=false, direct_mts_component_bound=false"))
    validations.append(base_row(validation_id="VAL2198_10_score_flags_false", status="PASS" if all_score_flags_false(rows_by_name) else "FAIL", detail="no generated row is score-ready or component-bound-claim-ready"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok and count > 0
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2198_11_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copies = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2198_12_branch_copies", status="PASS" if copies and all(row["copied"] for row in copies) else "FAIL", detail=";".join(str(row["target_path"]) for row in copies)))

    validations.append(base_row(validation_id="VAL2198_13_formalization_clean", status="PASS" if not formalization_has_2198_artifacts() else "FAIL", detail="formalization-workbench has no 2198 artifacts"))

    remove_pycache()
    validations.append(base_row(validation_id="VAL2198_14_pycache_absent", status="PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = "PASS" if all(row["status"] == "PASS" for row in validations) else "FAIL"
    validations.append(base_row(validation_id="VAL2198_OVERALL", status=overall, detail="2198 consolidates source-zero identity, bounded coupling component vector, Cassini proxy pressure, and next no-hidden-visible/PPN-vector route without claims"))
    return validations


def render_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n".join(
        [
            "# 2198 - Y5/R2FR Beta Source-Zero Or Bounded Component Pack",
            "",
            "## Current Verdict",
            "",
            "2198 makes the post-`Z_X` move: the local source side is now a component-vector problem, not a vague coupling complaint.",
            "",
            "`J_X=qbar_XT=0` remains the clean derivation route, but it is still conditional on an unsigned ordinary-matter parent signature. The fallback is now explicit: frame, marker, source-weight, non-Hilbert/support/boundary/readout components must be theorem-zero or source-bounded with an absolute no-cancellation envelope.",
            "",
            "The first real empirical pressure is also retained honestly: Cassini gives `|alpha_PPN| <= 0.005788015401465051` as a source-backed scalar-tensor proxy. It is **not** a direct MTS `c_g` bound because `Z_X/N_X`, `tau_PPN`, range/screening and PPN vector-tail gates remain missing.",
            "",
            "## Source Register",
            "",
            md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "",
            "## Source-Zero Identity",
            "",
            md_table(rows_by_name["source_zero_identity"], ["identity_id", "statement", "proof_status", "missing_premise", "local_gr_relevance", "valid_for_claim"]),
            "",
            "## Bounded Component Vector",
            "",
            md_table(rows_by_name["component_vector"], ["component_id", "symbol", "role", "current_best_anchor", "blocker", "bound_status", "no_cancellation_rule", "component_bound_claim", "score_ready", "valid_for_claim"]),
            "",
            "## First Proxy Pressure Row",
            "",
            md_table(rows_by_name["first_proxy_pressure"], ["proxy_id", "arena", "observable_or_component", "proxy_value", "formula_or_rule", "source", "source_backed_proxy", "direct_mts_component_bound", "notes", "valid_for_claim"]),
            "",
            "## Translation Blocker Gate",
            "",
            md_table(rows_by_name["translation_blockers"], ["blocker_id", "blocker", "current_status", "effect_if_missing", "next_action", "valid_for_claim"]),
            "",
            "## Claim Gate",
            "",
            md_table(rows_by_name["claim_gate"], ["gate_id", "gate", "status", "implication", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            "",
            md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"]),
            "",
            "## Next Target",
            "",
            md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"]),
            "",
            "## Branch Copies",
            "",
            md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"]),
            "",
            "## Validation",
            "",
            md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
            "",
            "## Interpretation",
            "",
            "This is a better fighting stance. If the no-hidden-visible-hom theorem closes, source silence becomes a real local-GR route. If it does not, the project still has a disciplined empirical path: score the full PPN/R10/clock/orbital component vector without pretending one parameter did all the work.",
            "",
            "Best next attack: try the no-hidden-visible-hom theorem first because it can kill several coupling channels at once. If it fails, build the PPN vector envelope and keep Cassini as proxy pressure, not a claim.",
            "",
        ]
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "source_zero_identity": source_zero_identity_rows(),
        "component_vector": component_vector_rows(),
        "first_proxy_pressure": first_proxy_pressure_rows(),
        "translation_blockers": translation_blocker_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    rows_by_name["claim_gate"] = claim_gate_rows(rows_by_name)

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])

    DOC.write_text(render_doc(rows_by_name), encoding="utf-8")
    remove_pycache()


if __name__ == "__main__":
    main()
