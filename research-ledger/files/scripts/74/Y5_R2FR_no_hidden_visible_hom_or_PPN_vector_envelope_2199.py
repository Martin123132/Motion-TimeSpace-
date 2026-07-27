from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2199"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2199-Y5-R2FR-no-hidden-visible-hom-or-PPN-vector-envelope.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2199_SOURCE_REGISTER.csv",
    "operator_domain_attempt": OUT / "P8_Y5_PARENT_QLOC_2199_OPERATOR_DOMAIN_ATTEMPT.csv",
    "hidden_obstruction": OUT / "P8_Y5_PARENT_QLOC_2199_HIDDEN_INVARIANT_OBSTRUCTION.csv",
    "ppn_vector_envelope": OUT / "P8_Y5_PARENT_QLOC_2199_PPN_VECTOR_ENVELOPE.csv",
    "residual_prior_queue": OUT / "P8_Y5_PARENT_QLOC_2199_RESIDUAL_PRIOR_QUEUE.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2199_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2199_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2199_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2199_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2199_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2199_HIDDEN_HOM_BLOCK_AND_PPN_VECTOR_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2199_PPN_VECTOR_ENVELOPE_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "PARENT_QLOC_OPERATOR_DOMAIN_ATTEMPT_2199_NONCLAIM.csv",
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


def formalization_has_2199_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2199-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2199*",
        "*P8_Y5_BRR545_2199*",
        "*Y5_R2FR_no_hidden_visible_hom_or_PPN_vector_envelope_2199*",
        "*JR2199*",
        "*PARENT_QLOC_OPERATOR_DOMAIN_ATTEMPT_2199*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2198_doc",
            ROOT / "2198-Y5-R2FR-beta-source-zero-or-bounded-component-pack.md",
            ["Best next attack: try the no-hidden-visible-hom theorem first", "VAL2198_OVERALL", "Cassini gives `|alpha_PPN|"],
            "2198 handoff to no-hidden-visible-hom theorem or PPN vector envelope.",
        ),
        (
            "2198_next",
            OUT / "P8_Y5_PARENT_QLOC_2198_NEXT_TARGET.csv",
            ["NEXT2198_0_2199", "do not turn Cassini proxy into direct c_g bound", "do not claim local GR"],
            "Machine-readable 2199 target.",
        ),
        (
            "1923_doc",
            ROOT / "1923-Y5-R2FR-parent-operator-domain-no-hidden-visible-hom-or-residual-prior-pack.md",
            ["OPERATOR_DOMAIN_THEOREM_NOT_DERIVED", "hidden invariant scalar obstruction survives", "RESIDUAL_PRIOR_PACK_STAGED_NONCLAIM"],
            "Latest R2FR operator-domain/no-hidden-visible-hom attempt.",
        ),
        (
            "1091_doc",
            ROOT / "1091-Y5-R10-parent-operator-domain-no-hidden-visible-hom-theorem-or-MOMS-closure.md",
            ["surviving scalar kills the theorem", "THEOREM_NOT_DERIVED_CURRENT_CORPUS", "product functor theorem would work if parent-signed"],
            "R10 predecessor proving the exact obstruction.",
        ),
        (
            "2161_doc",
            ROOT / "2161-Y5-R2FR-parent-NX-lambda-extraction-or-PPN-vector-envelope.md",
            ["full PPN residual vector", "VAL2161_OVERALL", "raw `c_g`"],
            "Current PPN vector envelope route.",
        ),
        (
            "2161_ppn_vector",
            OUT / "P8_Y5_PARENT_QLOC_2161_PPN_VECTOR_ENVELOPE.csv",
            ["PVE2161_6_total_abs_guard", "SOURCE_PROXY_ONLY", "MISSING_ZX_TAU_RANGE"],
            "Machine-readable PPN vector envelope with Cassini proxy ceiling.",
        ),
        (
            "2159_axiom_reduction",
            OUT / "P8_Y5_PARENT_QLOC_2159_MISSING_AXIOM_REDUCTION.csv",
            ["AXR2159_1_no_hidden_visible_hom", "BEST_NEXT_DERIVATION_TARGET", "SELECT_OPERATOR_DOMAIN_OR_CG_TRANSLATION_NEXT"],
            "Missing axiom reduction selecting no-hidden-visible-hom as smallest beam.",
        ),
        (
            "2198_component_vector",
            OUT / "P8_Y5_PARENT_QLOC_2198_BOUNDED_COMPONENT_VECTOR.csv",
            ["BCV2198_0_cg", "BCV2198_6_total", "COMPONENT_VECTOR_READY_VALUES_MISSING"],
            "Current component vector from 2198.",
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


def operator_domain_attempt_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            theorem_id="ODH2199_0_target",
            clause="no hidden-visible coefficient homomorphism",
            mathematical_statement="Hom(C_hid, Coeff(O_vis)) is absent or constant for visible EM, mass, clock, source-weight, shadow-frame and marker coefficients",
            current_status="TARGET_SHARP",
            obstruction="none at definition level",
            effect_if_signed="kills b_alpha, b_A, b_marker, delta_kappa_A and shadow-frame source maps at once",
        ),
        base_row(
            theorem_id="ODH2199_1_symmetry_insufficient",
            clause="diffeomorphism/gauge covariance",
            mathematical_statement="covariance and visible gauge symmetry allow f(I_hid)F^2, m_A(I_hid) psi_bar psi, A_g(I_hid)^2 g and source weights",
            current_status="INSUFFICIENT_FOR_THEOREM",
            obstruction="legal scalar coefficient functions survive",
            effect_if_signed="not applicable; this route is rejected as proof",
        ),
        base_row(
            theorem_id="ODH2199_2_scalar_counterexample",
            clause="surviving hidden invariant scalar",
            mathematical_statement="if I in O(C_hid)^inv and dI != 0, then c(I)=c0+epsilon I is a nonconstant visible coefficient map",
            current_status="COUNTEREXAMPLE_SURVIVES",
            obstruction="hidden invariant algebra triviality is not parent-signed",
            effect_if_signed="forces next target to O(C_hid)^inv=R, exact shift/no-hair, or profile-zero theorem",
        ),
        base_row(
            theorem_id="ODH2199_3_product_functor",
            clause="product/sequester functor",
            mathematical_statement="S_vis=S_vis[q(Phi),theta_rep] with no Hom(C_hid,Coeff(O_vis)) would remove hidden-visible coefficient maps",
            current_status="EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            obstruction="parent product functor and radiative/readout closure are unsigned",
            effect_if_signed="would close the ordinary-matter signature beam and reopen source-zero",
        ),
        base_row(
            theorem_id="ODH2199_4_radiative_readout",
            clause="EFT/readout closure",
            mathematical_statement="bare sequester must survive effective action and readout reductions",
            current_status="RADIATIVE_READOUT_CLOSURE_UNSIGNED",
            obstruction="b_alpha, b_clock, marker and readout coefficients can re-enter",
            effect_if_signed="prevents post-readout leakage from rebuilding qbar_XT",
        ),
        base_row(
            theorem_id="ODH2199_5_verdict",
            clause="derive no-hidden-visible-hom now",
            mathematical_statement="ODH2199_0 plus no scalar obstruction plus product/radiative closure",
            current_status="THEOREM_NOT_DERIVED_CURRENT_CORPUS",
            obstruction="surviving hidden invariant scalar plus unsigned product/radiative closure",
            effect_if_signed="not signed; retain PPN/component vector and hidden-invariant algebra target",
        ),
    ]


def hidden_obstruction_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            obstruction_id="HIO2199_0_invariant_scalar",
            obstruction="nonconstant hidden invariant scalar I_hid",
            dangerous_map="I_hid -> f_X(I_hid)F^2, m_A(I_hid), clock(I_hid), A_g(I_hid), source_weight(I_hid)",
            current_status="NOT_EXCLUDED",
            required_theorem="O(C_hid)^inv=R or exact shift/no-hair/profile-zero theorem",
        ),
        base_row(
            obstruction_id="HIO2199_1_alpha_owner",
            obstruction="visible EM/fine-structure normalization owner unsigned",
            dangerous_map="alpha_EM(X), gauge kinetic coefficient, electromagnetic binding marker",
            current_status="B_ALPHA_RETAINED",
            required_theorem="parent charge-generator norm/topological level/radiative closure theorem",
        ),
        base_row(
            obstruction_id="HIO2199_2_matter_spectrum",
            obstruction="ordinary matter spectrum/constants not parent-owned",
            dangerous_map="m_A(X), y_A(X), binding energies and material labels",
            current_status="B_A_AND_MARKER_RETAINED",
            required_theorem="fixed representation/superselection theorem",
        ),
        base_row(
            obstruction_id="HIO2199_3_source_weight",
            obstruction="source-only class/species weight not ruled out",
            dangerous_map="kappa_A(X), w_A(X), source-label leakage",
            current_status="DELTA_KAPPA_RETAINED",
            required_theorem="common measure/current normalization and source-label forgetting",
        ),
        base_row(
            obstruction_id="HIO2199_4_readout_tail",
            obstruction="post-variation readout or support/domain tail",
            dangerous_map="C_readout, Delta_W_support, q_domain, q_boundary",
            current_status="READOUT_AND_SUPPORT_TAILS_RETAINED",
            required_theorem="variation-before-readout and boundary/support silence",
        ),
    ]


def ppn_vector_envelope_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            vector_id="PVE2199_0_cg",
            component="common conformal coupling",
            formula="alpha_cg=tau_g*S_PPN(lambda_X,env)*c_g/sqrt(Z_X)",
            current_status="MISSING_ZX_TAU_RANGE",
            observable_link="Cassini gamma/Shapiro; source-backed proxy only",
            no_cancellation=True,
        ),
        base_row(
            vector_id="PVE2199_1_disformal",
            component="disformal/preferred-frame tail",
            formula="alpha_dis=tau_dis*b_dis",
            current_status="MISSING_DISFORMAL_PPN_PROJECTION",
            observable_link="PPN gamma; preferred-frame; clocks",
            no_cancellation=True,
        ),
        base_row(
            vector_id="PVE2199_2_nonH",
            component="non-Hilbert/source-current tail",
            formula="alpha_nonH=tau_nonH*q_nonH",
            current_status="MISSING_NONHILBERT_PPN_PROJECTION",
            observable_link="PPN gamma; orbital source normalization",
            no_cancellation=True,
        ),
        base_row(
            vector_id="PVE2199_3_support",
            component="support/domain local-projection tail",
            formula="alpha_support=tau_support*Delta_W_support+tau_domain*q_domain",
            current_status="MISSING_SUPPORT_DOMAIN_PPN_PROJECTION",
            observable_link="finite-source and domain readout",
            no_cancellation=True,
        ),
        base_row(
            vector_id="PVE2199_4_boundary",
            component="boundary/local flux tail",
            formula="alpha_boundary=tau_boundary*q_boundary",
            current_status="MISSING_BOUNDARY_PPN_PROJECTION",
            observable_link="PPN/orbital/local-GR boundary terms",
            no_cancellation=True,
        ),
        base_row(
            vector_id="PVE2199_5_readout",
            component="measured-G/readout calibration tail",
            formula="alpha_readout=tau_readout*C_readout",
            current_status="MISSING_READOUT_PPN_PROJECTION",
            observable_link="observed GM/gamma extraction",
            no_cancellation=True,
        ),
        base_row(
            vector_id="PVE2199_6_total_abs_guard",
            component="absolute PPN residual vector",
            formula="|alpha_PPN_total| <= |alpha_cg|+|alpha_dis|+|alpha_nonH|+|alpha_support|+|alpha_boundary|+|alpha_readout|",
            current_status="SCHEMA_READY_VALUES_MISSING",
            observable_link="no one-parameter c_g pass until vector is controlled",
            no_cancellation=True,
        ),
        base_row(
            vector_id="PVE2199_7_source_proxy_ceiling",
            component="Cassini scalar proxy ceiling",
            formula="|alpha_PPN_total| <= 0.005788015401465051 only if this vector is the actual MTS PPN observable",
            current_status="SOURCE_PROXY_ONLY",
            observable_link="pressure/target, not direct claim",
            no_cancellation=True,
        ),
    ]


def residual_prior_queue_rows() -> list[dict[str, Any]]:
    specs = [
        ("RQP2199_0_balpha", "b_alpha", "EM/gauge kinetic/readout alpha channel", "clock;WEP;R10;EM", "MISSING_PARENT_THEOREM_OR_SOURCE_BACKED_PRIOR"),
        ("RQP2199_1_bA", "b_A", "mass/material/species coefficient", "WEP;clock;R10;composition", "MISSING_PARENT_THEOREM_OR_SOURCE_BACKED_PRIOR"),
        ("RQP2199_2_bmarker", "b_marker", "material/source/readout marker", "WEP_source_charge;clock;R10;readout", "MISSING_PARENT_THEOREM_OR_SOURCE_BACKED_PRIOR"),
        ("RQP2199_3_delta_kappa", "delta_kappa_A", "source-only current/species weight", "WEP_source_charge;orbital;R10_source_mass", "MISSING_PARENT_THEOREM_OR_SOURCE_BACKED_PRIOR"),
        ("RQP2199_4_qnonH", "q_nonH", "non-Hilbert/domain/support tail", "PPN;R10;orbital;local_GR", "MISSING_PARENT_THEOREM_OR_SOURCE_BACKED_PRIOR"),
        ("RQP2199_5_total", "qbar_constants_abs_prior", "absolute no-cancellation envelope", "WEP;R10;clock;PPN;local_GR", "SOURCE_READY_SCHEMA_ONLY_NONCLAIM"),
    ]
    return [
        base_row(
            prior_id=prior_id,
            symbol=symbol,
            definition=definition,
            observable_link=observable_link,
            current_status=status,
            needed_for_claim="parent theorem-zero or numeric/source-backed prior width; Xhat normalization; arena projection; no-cancellation policy",
            score_ready=False,
        )
        for prior_id, symbol, definition, observable_link, status in specs
    ]


def claim_gate_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    theorem_blocked = any(row["theorem_id"] == "ODH2199_5_verdict" and row["current_status"] == "THEOREM_NOT_DERIVED_CURRENT_CORPUS" for row in rows_by_name["operator_domain_attempt"])
    vector_ready_nonclaim = any(row["vector_id"] == "PVE2199_6_total_abs_guard" and row["current_status"] == "SCHEMA_READY_VALUES_MISSING" for row in rows_by_name["ppn_vector_envelope"])
    return [
        base_row(
            gate_id="CG2199_0_operator_domain",
            gate="no-hidden-visible-hom theorem derived",
            status="BLOCKED_NONCLAIM" if theorem_blocked else "FAIL",
            implication="visible coefficient maps remain live until hidden invariant algebra/product/radiative closure is signed.",
        ),
        base_row(
            gate_id="CG2199_1_ppn_vector",
            gate="PPN residual vector explicit enough as fallback",
            status="PASS_NONCLAIM" if vector_ready_nonclaim else "FAIL",
            implication="the honest comparison object is the vector envelope, not raw c_g.",
        ),
        base_row(
            gate_id="CG2199_2_cassini_direct",
            gate="Cassini gives direct MTS c_g bound",
            status="BLOCKED_NONCLAIM",
            implication="Cassini remains source-backed proxy pressure only.",
        ),
        base_row(
            gate_id="CG2199_3_local_GR_claim",
            gate="local GR/Newton or empirical pass",
            status="BLOCKED_NONCLAIM",
            implication="No local-GR, R10, PPN, clock, orbital, WEP or public claim follows from 2199.",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2199_0_theorem",
            decision="NO_HIDDEN_VISIBLE_HOM_NOT_DERIVED",
            rationale="A surviving hidden invariant scalar can generate exactly the forbidden visible coefficient maps.",
            selection_status="selected",
        ),
        base_row(
            decision_id="DEC2199_1_vector",
            decision="PPN_VECTOR_ENVELOPE_PROMOTED_AS_HONEST_FALLBACK_OBJECT",
            rationale="The vector is explicit enough to carry Cassini pressure without pretending raw c_g is bound.",
            selection_status="selected",
        ),
        base_row(
            decision_id="DEC2199_2_next",
            decision="ATTACK_HIDDEN_INVARIANT_TRIVIALITY_NEXT",
            rationale="The no-hidden-visible theorem now reduces to whether the hidden/local invariant algebra has nonconstant scalars.",
            selection_status="selected",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2199_0_2200",
            selection_status="selected",
            target_file="2200-Y5-R2FR-hidden-invariant-algebra-triviality-or-PPN-vector-source-row.md",
            target_script="scripts/Y5_R2FR_hidden_invariant_algebra_triviality_or_PPN_vector_source_row_2200.py",
            objective="try to prove O(C_hid)^inv=R, exact shift/no-hair, or profile-zero removes hidden coefficient maps; if unsigned, source the first PPN vector component row",
            success_condition="hidden invariant scalar obstruction closes by theorem or at least one PPN vector component becomes source-backed/nonclaim with units and observable link",
            do_not_do="do not assume product sequestering, do not use covariance/gauge invariance as a ban, do not turn Cassini proxy into direct c_g bound, do not claim local GR",
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["residual_prior_queue"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["ppn_vector_envelope"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["operator_domain_attempt"], BRANCH_COPIES["source_weight"]),
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
            if truthy(row.get("claim_allowed", False)) or truthy(row.get("valid_for_claim", False)):
                return False
    return True


def all_score_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if "score_ready" in row and truthy(row["score_ready"]):
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []
    sources = rows_by_name["source_register"]
    validations.append(base_row(validation_id="VAL2199_00_sources_exist", status="PASS" if all(row["path_exists"] for row in sources) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in sources)}/{len(sources)} sources exist"))
    validations.append(base_row(validation_id="VAL2199_01_needles_found", status="PASS" if all(row["needles_found"] for row in sources) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in sources)}/{len(sources)} source needle sets found"))

    theorem = rows_by_name["operator_domain_attempt"]
    theorem_ok = any(row["theorem_id"] == "ODH2199_5_verdict" and row["current_status"] == "THEOREM_NOT_DERIVED_CURRENT_CORPUS" for row in theorem)
    counterexample_ok = any(row["theorem_id"] == "ODH2199_2_scalar_counterexample" and row["current_status"] == "COUNTEREXAMPLE_SURVIVES" for row in theorem)
    validations.append(base_row(validation_id="VAL2199_02_theorem_attempt", status="PASS" if theorem_ok and counterexample_ok else "FAIL", detail=f"theorem_blocked={theorem_ok};scalar_counterexample={counterexample_ok}"))

    obstructions = rows_by_name["hidden_obstruction"]
    obstruction_ok = len(obstructions) >= 5 and any(row["obstruction_id"] == "HIO2199_0_invariant_scalar" and row["current_status"] == "NOT_EXCLUDED" for row in obstructions)
    validations.append(base_row(validation_id="VAL2199_03_obstruction_ledger", status="PASS" if obstruction_ok else "FAIL", detail="hidden invariant and visible coefficient obstructions retained"))

    vector = rows_by_name["ppn_vector_envelope"]
    vector_ok = any(row["vector_id"] == "PVE2199_6_total_abs_guard" and row["current_status"] == "SCHEMA_READY_VALUES_MISSING" for row in vector) and any(row["vector_id"] == "PVE2199_7_source_proxy_ceiling" and row["current_status"] == "SOURCE_PROXY_ONLY" for row in vector)
    validations.append(base_row(validation_id="VAL2199_04_ppn_vector", status="PASS" if vector_ok else "FAIL", detail="PPN vector envelope and Cassini proxy-only ceiling retained"))

    priors = rows_by_name["residual_prior_queue"]
    priors_ok = priors and all(not truthy(row.get("score_ready", False)) for row in priors)
    validations.append(base_row(validation_id="VAL2199_05_prior_queue", status="PASS" if priors_ok else "FAIL", detail=f"prior_rows={len(priors)};score_ready_false={priors_ok}"))

    gates = rows_by_name["claim_gate"]
    gates_ok = any(row["gate_id"] == "CG2199_0_operator_domain" and row["status"] == "BLOCKED_NONCLAIM" for row in gates) and any(row["gate_id"] == "CG2199_1_ppn_vector" and row["status"] == "PASS_NONCLAIM" for row in gates)
    validations.append(base_row(validation_id="VAL2199_06_claim_gate", status="PASS" if gates_ok else "FAIL", detail="operator theorem blocked; vector fallback passes only nonclaim"))

    decisions = {row["decision"] for row in rows_by_name["decision"] if row["selection_status"] == "selected"}
    validations.append(base_row(validation_id="VAL2199_07_decision", status="PASS" if "ATTACK_HIDDEN_INVARIANT_TRIVIALITY_NEXT" in decisions else "FAIL", detail="decision selects hidden invariant triviality next"))

    routes = {row["route_id"] for row in rows_by_name["next_target"] if row["selection_status"] == "selected"}
    validations.append(base_row(validation_id="VAL2199_08_next_target", status="PASS" if "NEXT2199_0_2200" in routes else "FAIL", detail="2200 target selected"))

    validations.append(base_row(validation_id="VAL2199_09_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))
    validations.append(base_row(validation_id="VAL2199_10_score_flags_false", status="PASS" if all_score_flags_false(rows_by_name) else "FAIL", detail="no generated row is score-ready"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok and count > 0
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2199_11_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copies = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2199_12_branch_copies", status="PASS" if copies and all(row["copied"] for row in copies) else "FAIL", detail=";".join(str(row["target_path"]) for row in copies)))
    validations.append(base_row(validation_id="VAL2199_13_formalization_clean", status="PASS" if not formalization_has_2199_artifacts() else "FAIL", detail="formalization-workbench has no 2199 artifacts"))
    remove_pycache()
    validations.append(base_row(validation_id="VAL2199_14_pycache_absent", status="PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = "PASS" if all(row["status"] == "PASS" for row in validations) else "FAIL"
    validations.append(base_row(validation_id="VAL2199_OVERALL", status=overall, detail="2199 rejects current no-hidden-visible-hom derivation, carries the PPN vector envelope, and selects hidden invariant algebra triviality next"))
    return validations


def render_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n".join(
        [
            "# 2199 - Y5/R2FR No Hidden-Visible Hom Or PPN Vector Envelope",
            "",
            "## Current Verdict",
            "",
            "2199 takes the theorem route seriously and rejects it as a current claim. The no-hidden-visible-hom target is exact and high leverage: if the parent object language forbids maps from hidden/local invariants into visible EM, mass, clock, marker, source-weight and shadow-frame coefficients, then several coupling channels die at once.",
            "",
            "But the current corpus does not prove that ban. A surviving hidden invariant scalar `I_hid` immediately generates legal visible coefficient maps such as `f(I_hid)F^2`, `m_A(I_hid)`, `A_g(I_hid)^2 g`, or source weights. Covariance and gauge symmetry do not forbid these maps. Product/sequester logic would help only if parent-signed and radiatively/readout closed.",
            "",
            "Therefore the honest fallback is the full PPN no-cancellation vector. Cassini pressure remains useful only as a source-backed proxy ceiling on the vector, not as a direct raw `c_g` bound.",
            "",
            "## Source Register",
            "",
            md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "",
            "## Operator-Domain Attempt",
            "",
            md_table(rows_by_name["operator_domain_attempt"], ["theorem_id", "clause", "mathematical_statement", "current_status", "obstruction", "effect_if_signed", "valid_for_claim"]),
            "",
            "## Hidden Invariant Obstruction",
            "",
            md_table(rows_by_name["hidden_obstruction"], ["obstruction_id", "obstruction", "dangerous_map", "current_status", "required_theorem", "valid_for_claim"]),
            "",
            "## PPN Vector Envelope",
            "",
            md_table(rows_by_name["ppn_vector_envelope"], ["vector_id", "component", "formula", "current_status", "observable_link", "no_cancellation", "valid_for_claim"]),
            "",
            "## Residual Prior Queue",
            "",
            md_table(rows_by_name["residual_prior_queue"], ["prior_id", "symbol", "definition", "observable_link", "current_status", "needed_for_claim", "score_ready", "valid_for_claim"]),
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
            "This is a root-cause move. The theorem failed, but it failed in the useful place: hidden invariant algebra. If `O(C_hid)^inv=R` or an equivalent exact shift/no-hair/profile-zero result closes, the source/coupling branch improves dramatically. If it does not, we stop chasing silence and score the full residual vector.",
            "",
            "Best next attack: hidden invariant algebra triviality. It is the cleanest way to remove the scalar counterexample at the root.",
            "",
        ]
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "operator_domain_attempt": operator_domain_attempt_rows(),
        "hidden_obstruction": hidden_obstruction_rows(),
        "ppn_vector_envelope": ppn_vector_envelope_rows(),
        "residual_prior_queue": residual_prior_queue_rows(),
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
