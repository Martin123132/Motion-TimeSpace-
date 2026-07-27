from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_BOUNDARY_CHARGE_QQ_KBOUNDARY_ZERO_OR_BETA_BOUND_FIRST_ROW_2427"
CHECKPOINT_ID = "2427"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2427-Y5-R2FR-boundary-charge-Qq-Kboundary-zero-or-beta-bound-first-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2427_SOURCE_REGISTER.csv",
    "compact_lemma": OUT / "P8_Y5_PARENT_QLOC_2427_COMPACT_PROPER_BOUNDARY_SILENCE_LEMMA.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2427_QQ_KBOUNDARY_CLAIM_GATE.csv",
    "boundary_residual": OUT / "P8_Y5_PARENT_QLOC_2427_BOUNDARY_RESIDUAL_BETA_ROW.csv",
    "first_projection": OUT / "P8_Y5_PARENT_QLOC_2427_FIRST_BETA_PROJECTION_TEMPLATE.csv",
    "alpha3_anchor": OUT / "P8_Y5_PARENT_QLOC_2427_ALPHA3_BOUND_ANCHOR_LEDGER.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2427_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2427_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2427_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2427_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2427_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2427_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_boundary": QUEUE / "JR2427_BOUNDARY_QQ_KBOUNDARY_TEMPLATE_NONCLAIM.csv",
    "queue_alpha3": QUEUE / "JR2427_ALPHA3_PROJECTION_TEMPLATE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "boundary_Qq_Kboundary_or_beta_nonclaim_2427.csv",
    "beta_docs": BETA_DOCS / "BOUNDARY_QQ_KBOUNDARY_OR_BETA_2427_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2427_00_2426_handoff",
        "source_path": ROOT / "2426-Y5-R2FR-no-physical-q-pole-theorem-or-bounded-beta-runner.md",
        "needles": ["NEXT2426_0_selected", "NPQ2426_3_boundary_silence", "VAL2426_OVERALL"],
        "role": "current handoff into Q_q/K_boundary or beta-bound first row",
    },
    {
        "source_id": "SRC2427_01_2426_validation",
        "source_path": OUT / "P8_Y5_BRR545_2426_VALIDATION.csv",
        "needles": ["VAL2426_OVERALL", "PASS"],
        "role": "confirms 2426 passed before 2427",
    },
    {
        "source_id": "SRC2427_02_2426_no_pole",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2426_NO_PHYSICAL_Q_POLE_AUDIT.csv",
        "needles": ["NPQ2426_3_boundary_silence", "FAIL_CURRENT_CLAIM_NO_POLE_NOT_PROVED"],
        "role": "machine-readable no-pole obstruction",
    },
    {
        "source_id": "SRC2427_03_2426_beta",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2426_BOUNDED_BETA_SOURCE_TEST_TEMPLATE.csv",
        "needles": ["BB2426_7_beta_product_guard", "c_g^2"],
        "role": "bounded beta fallback with c_g^2 product guard",
    },
    {
        "source_id": "SRC2427_04_2293_precedent",
        "source_path": ROOT / "2293-Y5-R2FR-boundary-charge-Qq-Kboundary-zero-or-beta-bound-first-row.md",
        "needles": ["QQK2293_6_verdict", "BRES2293_1_K_boundary_alpha3_q", "VAL2293_OVERALL"],
        "role": "prior q boundary charge/cocycle checkpoint",
    },
    {
        "source_id": "SRC2427_05_2245_compact",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2245_COMPACT_PROPER_BOUNDARY_SILENCE_LEMMA.csv",
        "needles": ["DERIVED_NARROW_PROPER_BRANCH_ONLY", "FULL_LOCAL_CLAIM_STILL_BLOCKED"],
        "role": "R_AB compact/proper finite-jet collar lemma precedent",
    },
    {
        "source_id": "SRC2427_06_1039_compact",
        "source_path": OUT / "P8_Y5_R10_1039_COMPACT_PROPER_BOUNDARY_SILENCE_LEMMA.csv",
        "needles": ["DERIVED_NARROW_PROPER_BRANCH_ONLY", "FULL_LOCAL_CLAIM_STILL_BLOCKED"],
        "role": "generic finite-jet collar lemma predecessor",
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


def compact_lemma_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            lemma_id="QQK2427_0_variational_identity",
            statement="For a differentiable local q-vertical generator G_q[epsilon], the obstruction is a finite-jet surface density k_q[delta Y,epsilon] on partial Sigma.",
            derivation_or_test="delta G_q[epsilon]=bulk constraint variation + integral_partialSigma k_q[delta Y,epsilon]; Q_q makes G_q differentiable.",
            status="STRUCTURAL_IDENTITY_CONDITIONAL_ON_PARENT_GQ",
            limitation="sets the boundary problem but does not prove full q silence",
        ),
        base_row(
            lemma_id="QQK2427_1_proper_collar_condition",
            statement="If epsilon_q and every finite jet entering k_q vanish on an open collar of partial Sigma, every local boundary monomial containing epsilon_q or its jets vanishes pointwise.",
            derivation_or_test="support(epsilon_q) compactly contained in Sigma implies epsilon_q and its finite required jets vanish at the boundary.",
            status="DERIVED_NARROW_CONDITIONAL_ZERO",
            limitation="proper compact q-representative transformations only",
        ),
        base_row(
            lemma_id="QQK2427_2_Qq_zero",
            statement="Under the compact/proper collar condition, Q_q[epsilon]=0 and delta Q_q[epsilon]=0.",
            derivation_or_test="q_q and delta q_q are finite-jet local surface expressions; all required epsilon_q jet factors vanish on the boundary collar.",
            status="DERIVED_NARROW_PROPER_BRANCH_ONLY",
            limitation="does not kill source-worldtube, non-proper, or large transformation edge charge",
        ),
        base_row(
            lemma_id="QQK2427_3_Kboundary_zero",
            statement="Under the compact/proper collar condition for both epsilon_q and eta_q, K_boundary[epsilon,eta]=0 for finite-jet local boundary cocycles.",
            derivation_or_test="the cocycle is a surface bilinear in generators and finite jets; every local boundary term contains at least one vanished generator jet.",
            status="DERIVED_NARROW_PROPER_BRANCH_ONLY",
            limitation="compact proper q algebra closes with zero boundary cocycle only in the representative sub-branch",
        ),
        base_row(
            lemma_id="QQK2427_4_GR_charge_guard",
            statement="The proper-q zero does not erase ADM/time/rotation, Newtonian mass, or GR Hamiltonian charges.",
            derivation_or_test="the vanishing condition applies only to representative q-vertical parameters; physical generators remain in the observed metric/coframe boundary sector.",
            status="GUARD_RETAINED",
            limitation="prevents deleting GR charges to save the q branch",
        ),
        base_row(
            lemma_id="QQK2427_5_source_boundary_limit",
            statement="The compact/proper lemma does not prove Q_q=0 for source worldtubes, non-compact transformations, reference-boundary terms, material readouts, or range-kernel edge projections.",
            derivation_or_test="R10, PPN, WEP/clock, and orbital tests can involve nonzero boundary/support data.",
            status="FULL_LOCAL_CLAIM_STILL_BLOCKED",
            limitation="source/test beta rows remain active",
        ),
        base_row(
            lemma_id="QQK2427_6_verdict",
            statement="Q_q=0 and K_boundary=0 are derived only for the proper compact q-representative sub-branch.",
            derivation_or_test="QQK2427_1 through QQK2427_4 close the narrow boundary algebra; QQK2427_5 blocks promotion to local-GR/R10.",
            status="DERIVED_NARROW_SUBLEMMA_FULL_CLAIM_BLOCKED",
            limitation="useful derived brick for GR-reduction hygiene, not an empirical pass",
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="QQG2427_0_proper_compact_sublemma", claim="proper compact q-representative transformations carry no boundary charge or cocycle", gate_status="conditional_narrow_pass", evidence="finite-jet boundary terms vanish when generator and required jets vanish on boundary collar", missing_for_promotion="does not cover source worldtubes, non-proper transformations, reference terms, matter/readout markers, or range-kernel edge rows"),
        base_row(gate_id="QQG2427_1_full_Qq_zero", claim="Q_q=0 for all local source/test boundaries", gate_status="fail_current_claim", evidence="compact-collar proof only covers proper representative transformations", missing_for_promotion="derive B_q/Q_q from Theta_Y and allowed boundary class"),
        base_row(gate_id="QQG2427_2_full_Kboundary_zero", claim="K_boundary=0 for source/test or improper edge transformations", gate_status="fail_current_claim", evidence="source/non-proper cocycle not computed", missing_for_promotion="compute bracket/cocycle for differentiable G_q[epsilon] and G_q[eta]"),
        base_row(gate_id="QQG2427_3_no_pole_promotion", claim="q has no physical local pole in the full GR/Newton branch", gate_status="fail_current_claim", evidence="boundary silence is only one required clause", missing_for_promotion="close Omega/DCq, boundary, degree, and matter clauses from one parent action"),
    ]


def boundary_residual_rows() -> list[dict[str, Any]]:
    return [
        base_row(residual_id="BRES2427_0_Qbar_edge_qH", symbol="Qbar_edge_qH(lambda)", formula_or_contract="Qbar_edge_qH(lambda)=integral_partialSigma F_lambda epsilon_q B_q with source/reference projection", why_retained="non-proper/source boundary values are not killed by compact representative lemma", missing_inputs="B_q owner; F_lambda kernel; source boundary class; Pi_M/Pi_EH projection; units", score_ready=False),
        base_row(residual_id="BRES2427_1_K_boundary_alpha3_q", symbol="K_boundary_alpha3_q", formula_or_contract="alpha3_MTS_q=K_boundary_alpha3_q * Phi_boundary_local_q", why_retained="alpha3 preferred-frame anchor is a clean first boundary/cocycle projection for a q leak", missing_inputs="K_boundary_alpha3_q; Phi_boundary_local_q; projection normalization; theorem-zero or numeric source", score_ready=False),
        base_row(residual_id="BRES2427_2_reference_mass_projection", symbol="Pi_M^H[Q_q_edge]", formula_or_contract="mass/Hamiltonian reference projector must be orthogonal to Q_q_edge or explicitly bounded", why_retained="zero q-boundary proof must not delete physical GR mass/energy charges", missing_inputs="reference subtraction; Pi_M action on q edge charge; no-double-count split", score_ready=False),
        base_row(residual_id="BRES2427_3_matter_readout_marker_edge", symbol="Q_q^marker", formula_or_contract="material/readout constants must have zero q edge marker or bounded coefficient vector", why_retained="q can hide in matter/readout even if compact bulk transformations are silent", missing_inputs="no-marker theorem; b_A/b_alpha bounds; WEP/clock projection matrix", score_ready=False),
        base_row(residual_id="BRES2427_4_no_double_count", symbol="Q_q_bulk + Q_q_edge split", formula_or_contract="bulk and edge beta products must be orthogonal or explicitly summed in absolute value", why_retained="prevents cancellation games between no-pole and bounded-beta routes", missing_inputs="source/test support split; absolute tail envelope; branch ownership ledger", score_ready=False),
    ]


def first_projection_rows() -> list[dict[str, Any]]:
    return [
        base_row(projection_id="FBP2427_0_boundary_alpha3_q", coefficient="K_boundary_alpha3_q * Phi_boundary_local_q", target="alpha3", formula="alpha3_MTS_q=K_boundary_alpha3_q * Phi_boundary_local_q", comparator_anchor="local_bound_claims.csv:Will_2014_PPN_alpha3_table", comparator_bound="4e-20", missing_for_score="K_boundary_alpha3_q;Phi_boundary_local_q;normalization;source_path or theorem-zero", status="SOURCE_BACKED_ANCHOR_READY_PROJECTION_MISSING", score_ready=False),
        base_row(projection_id="FBP2427_1_R10_edge_beta_q", coefficient="Qbar_edge_qH(lambda) * qbar_qT(lambda)", target="alpha_R10(lambda)", formula="|alpha_q_edge(lambda)| <= |K_q^R10(lambda)| |Qbar_edge_qH(lambda) qbar_qT(lambda)| + abs_tail", comparator_anchor="R10 bound curve + source/test q boundary projection", comparator_bound="MISSING_CURVE_AND_PROJECTION", missing_for_score="B_q;Qbar_edge_qH;qbar_qT;K_q^R10(lambda);source/test support", status="CLAIM_BLOCKED_UNTIL_SOURCE_BACKED_BOUND_ROW", score_ready=False),
        base_row(projection_id="FBP2427_2_absolute_tail_gate", coefficient="boundary_q_abs_tail", target="all local arenas", formula="unknown Q_q/K_boundary/source-support/marker components add in absolute value; no cancellation credit", comparator_anchor="R10;alpha3;PPN;WEP;clock;orbital ledgers", comparator_bound="multiple", missing_for_score="component theorem-zero or numeric/source-backed bound rows", status="CLAIM_BLOCKED_UNTIL_COMPONENTS_SOURCE_BACKED", score_ready=False),
    ]


def alpha3_anchor_rows() -> list[dict[str, Any]]:
    return [
        base_row(anchor_id="A3A2427_0_source_bound", source="Will_2014_PPN_alpha3_table", quantity="alpha3", bound_value="4e-20", units="dimensionless", source_path="source-intake/local_bounds/local_bound_claims.csv; prior 1039/2245/2293 alpha3 anchor ledgers", use="anchor only for q boundary alpha3 projection row; not an MTS pass"),
    ]


def refusal_rows(
    compact: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    projections: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in compact:
        rows.append(base_row(refusal_id=f"REF2427_{row['lemma_id']}", attempted_claim=row["statement"], result=row["status"], reason=f"full_boundary_claim_not_promoted; {row['limitation']}", score_ready=False))
    for row in gates:
        rows.append(base_row(refusal_id=f"REF2427_{row['gate_id']}", attempted_claim=row["claim"], result=row["gate_status"], reason=f"boundary_gate_not_claim_promoted; {row['missing_for_promotion']}", score_ready=False))
    for row in residuals:
        rows.append(base_row(refusal_id=f"REF2427_{row['residual_id']}", attempted_claim=row["symbol"], result="residual_retained_missing_inputs", reason=row["missing_inputs"], score_ready=False))
    for row in projections:
        rows.append(base_row(refusal_id=f"REF2427_{row['projection_id']}", attempted_claim=row["coefficient"], result="projection_row_rejected_missing_coefficients", reason=row["status"], score_ready=False))
    return rows


def public_claim_gates() -> list[dict[str, Any]]:
    return [
        base_row(claim_id="CGATE2427_0_compact_proper_sublemma", claim="compact proper q-representative boundary transformations are silent", gate_pass="conditional_narrow_only", reason="finite-jet boundary terms vanish when representative generator and required jets vanish on boundary collar"),
        base_row(claim_id="CGATE2427_1_full_local_GR", claim="local GR/no-pole q branch is fully closed", gate_pass="false", reason="source worldtubes, reference/mass projection, exactness, counterterms, parent bracket, degree count, and matter/source readout remain unproved"),
        base_row(claim_id="CGATE2427_2_alpha3_projection", claim="q boundary alpha3 row is score-ready", gate_pass="false", reason="alpha3 external anchor exists but K_boundary_alpha3_q and Phi_boundary_local_q are missing"),
        base_row(claim_id="CGATE2427_3_R10_boundary_beta", claim="R10 q edge beta row is score-ready", gate_pass="false", reason="B_q/Q_q, source/test supports, K_q^R10(lambda), and valid bound curve are not jointly sourced"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2427_0_boundary_derivation", decision="NARROW_COMPACT_PROPER_QQ_KBOUNDARY_ZERO_DERIVED", rationale="finite-jet boundary charges and cocycles vanish pointwise when the representative generator and required jets vanish on the boundary collar", consequence="do not promote to R10/local-GR; attack non-proper/source boundary formula next"),
        base_row(decision_id="DEC2427_1_empirical_fallback", decision="FIRST_BOUNDARY_PROJECTION_IS_ALPHA3_TEMPLATE", rationale="alpha3 has a tight source-backed anchor and boundary/cocycle is the active q obstruction", consequence="derive/source K_boundary_alpha3_q and Phi_boundary_local_q, or theorem-zero both"),
        base_row(decision_id="DEC2427_2_R10_fallback", decision="R10_EDGE_REMAINS_SOURCE_TEST_PRODUCT", rationale="finite exchange requires source and test legs; unknown components add as absolute tails", consequence="write B_q/Q_q and source/test support projection before scoring"),
        base_row(decision_id="DEC2427_3_next", decision="WRITE_PARENT_BQ_QQ_FORMULA_NEXT", rationale="explicit B_q/Q_q decides both no-pole route and alpha3/R10 fallback rows", consequence="2428 parent boundary charge formula or alpha3 projection bound"),
        base_row(decision_id="DEC2427_4_claim_policy", decision="KEEP_PRIVATE_NONCLAIM", rationale="derived sublemma is narrow and empirical projection coefficients are missing", consequence="no GitHub action"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2427_0_selected",
            selection_status="selected",
            target_file="2428-Y5-R2FR-parent-boundary-charge-formula-Bq-or-alpha3-projection-bound.md",
            target_script="scripts/Y5_R2FR_parent_boundary_charge_formula_Bq_or_alpha3_projection_bound_2428.py",
            objective="derive the explicit parent boundary charge density B_q/Q_q from the symplectic potential and allowed q boundary class; if this cannot close, build the nonclaim alpha3/R10 projection coefficient row for K_boundary_alpha3_q, Phi_boundary_local_q, and Qbar_edge_qH",
            success_condition="B_q surface density and exact/proper split are parent-signed, or alpha3/R10 edge projection rows remain source-ready nonclaim with missing coefficients explicit",
            do_not_do="do not invent K_boundary values, delete GR charges, score naked linear c_g, cancel residuals, claim R10/local-GR pass, edit formalization-workbench, or push GitHub",
        )
    ]


def copy_branch_rows(boundary_rows: list[dict[str, Any]], projection_rows: list[dict[str, Any]], decision_ledger: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copy_specs = [
        ("queue_boundary", OUTPUTS["boundary_residual"], COPY_TARGETS["queue_boundary"], boundary_rows),
        ("queue_alpha3", OUTPUTS["first_projection"], COPY_TARGETS["queue_alpha3"], projection_rows),
        ("branch_wep", OUTPUTS["first_projection"], COPY_TARGETS["branch_wep"], projection_rows),
        ("beta_docs", OUTPUTS["boundary_residual"], COPY_TARGETS["beta_docs"], boundary_rows),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_path, target_path, copied_rows in copy_specs:
        write_csv(target_path, copied_rows)
        rows.append(
            base_row(
                copy_id=f"BC2427_{copy_id}",
                source_path=source_path,
                target_path=target_path,
                target_exists=target_path.exists(),
                row_count=len(copied_rows),
                purpose="boundary q/cocycle nonclaim handoff",
            )
        )
    return rows


def formalization_has_2427_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2427-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2427*",
        "*P8_Y5_BRR545_2427*",
        "*Y5_R2FR_boundary_charge_Qq_Kboundary_zero_or_beta_bound_first_row_2427*",
        "*JR2427*",
        "*BOUNDARY_QQ_KBOUNDARY_OR_BETA_2427*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def flags_safe(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            for key in ("valid_for_claim", "claim_allowed", "score_ready"):
                value = row.get(key)
                if value is True or stringify(value).lower() == "true":
                    return False
    return True


def build_validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_copy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    compact = rows_by_name["compact_lemma"]
    gates = rows_by_name["claim_gate"]
    residuals = rows_by_name["boundary_residual"]
    projections = rows_by_name["first_projection"]
    next_rows = rows_by_name["next_target"]

    csv_results = []
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        parses, row_count, message = csv_parses(path)
        csv_results.append((name, parses, row_count, message))
    for copy_key, copy_path in COPY_TARGETS.items():
        parses, row_count, message = csv_parses(copy_path)
        csv_results.append((f"copy_{copy_key}", parses, row_count, message))

    checks = [
        ("VAL2427_SOURCES_EXIST", all(row["path_exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL2427_NEEDLES_FOUND", all(row["needles_found"] for row in source_rows), "all source needles found"),
        ("VAL2427_COMPACT_SUBLEMMA", any(row["lemma_id"] == "QQK2427_6_verdict" and "DERIVED_NARROW" in row["status"] for row in compact), "proper compact Q_q/K_boundary zero sublemma recorded"),
        ("VAL2427_FULL_CLAIM_BLOCKED", any(row["gate_id"] == "QQG2427_1_full_Qq_zero" and row["gate_status"] == "fail_current_claim" for row in gates), "full source-boundary Q_q zero remains blocked"),
        ("VAL2427_BOUNDARY_RESIDUALS", {row["residual_id"] for row in residuals} >= {"BRES2427_0_Qbar_edge_qH", "BRES2427_1_K_boundary_alpha3_q", "BRES2427_4_no_double_count"}, "boundary/source/test residual rows retained"),
        ("VAL2427_ALPHA3_TEMPLATE", any(row["projection_id"] == "FBP2427_0_boundary_alpha3_q" and row["comparator_bound"] == "4e-20" for row in projections), "alpha3 projection anchor recorded as nonclaim template"),
        ("VAL2427_NEXT_SELECTED", any(row["route_id"] == "NEXT2427_0_selected" and "boundary-charge-formula" in row["target_file"] for row in next_rows), "parent B_q/Q_q formula selected next"),
        ("VAL2427_FLAGS_SAFE", flags_safe(rows_by_name), "no claim/score flags are true"),
        ("VAL2427_BRANCH_COPIES", all(row["target_exists"] for row in branch_copy_rows), "branch copy files written"),
        ("VAL2427_CSV_PARSE", all(item[1] and item[2] > 0 for item in csv_results), "all generated CSV and branch copies parse with rows"),
        ("VAL2427_NO_FORMALIZATION_OUTPUT", not formalization_has_2427_artifacts(), "no 2427 artifacts written into formalization-workbench"),
    ]

    rows = [
        base_row(
            validation_id=validation_id,
            status="PASS" if passed else "FAIL",
            detail=detail,
            fatal=not passed,
        )
        for validation_id, passed, detail in checks
    ]
    overall_passed = all(row["status"] == "PASS" for row in rows)
    rows.append(
        base_row(
            validation_id="VAL2427_OVERALL",
            status="PASS" if overall_passed else "FAIL",
            detail="2427 derives the narrow compact/proper Q_q and K_boundary silence sublemma, retains source-boundary beta rows, and selects parent B_q/Q_q formula next",
            fatal=not overall_passed,
        )
    )
    return rows


def write_document(rows_by_name: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> None:
    content = f"""# 2427 Y5 R2FR Boundary Charge Qq/Kboundary Zero Or Beta-Bound First Row

## Result

2427 gets a real but narrow derived brick: for proper compact `q`-representative transformations, where the generator and required finite jets vanish on a boundary collar, both `Q_q` and `K_boundary` vanish.

That is useful GR-reduction hygiene, not a local-GR/R10 pass. Source worldtubes, non-proper transformations, reference/mass projections, material/readout markers, and range-kernel edge projections remain live. The first concrete fallback projection is `alpha3_MTS_q=K_boundary_alpha3_q*Phi_boundary_local_q`, anchored to the source-backed `alpha3 <= 4e-20` row but nonclaim until the MTS projection coefficients are derived, sourced, or theorem-zeroed.

## Practical Status

- **Derived:** compact/proper representative `Q_q=0` and `K_boundary=0` sublemma.
- **Not derived:** full source-boundary `Q_q=0`, full `K_boundary=0`, no-pole promotion, or local-GR/Newton pass.
- **Fallback retained:** boundary alpha3 and R10 edge beta templates, with absolute no-cancellation tails.
- **Next target:** explicit parent `B_q/Q_q` boundary charge formula from the symplectic potential and boundary class.

## Source Register

{table(["source_id", "source_path", "path_exists", "needles_found", "role"], rows_by_name["source_register"])}

## Compact/Proper Boundary Silence Lemma

{table(["lemma_id", "statement", "derivation_or_test", "status", "limitation"], rows_by_name["compact_lemma"])}

## Qq/Kboundary Claim Gate

{table(["gate_id", "claim", "gate_status", "evidence", "missing_for_promotion"], rows_by_name["claim_gate"])}

## Boundary Residual Beta Rows

{table(["residual_id", "symbol", "formula_or_contract", "why_retained", "missing_inputs", "score_ready"], rows_by_name["boundary_residual"])}

## First Beta Projection Template

{table(["projection_id", "coefficient", "target", "formula", "comparator_anchor", "comparator_bound", "missing_for_score", "status", "score_ready"], rows_by_name["first_projection"])}

## Alpha3 Anchor

{table(["anchor_id", "source", "quantity", "bound_value", "units", "source_path", "use"], rows_by_name["alpha3_anchor"])}

## Refusal Runner

{table(["refusal_id", "attempted_claim", "result", "reason", "score_ready"], rows_by_name["refusal"])}

## Claim Gates

{table(["claim_id", "claim", "gate_pass", "reason"], rows_by_name["claim_gates"])}

## Decision Ledger

{table(["decision_id", "decision", "rationale", "consequence"], rows_by_name["decision"])}

## Next Target

{table(["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do"], rows_by_name["next_target"])}

## Validation

{table(["validation_id", "status", "detail", "fatal"], validation_rows)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    compact = compact_lemma_rows()
    gates = claim_gate_rows()
    residuals = boundary_residual_rows()
    projections = first_projection_rows()

    rows_by_name = {
        "source_register": source_register_rows(),
        "compact_lemma": compact,
        "claim_gate": gates,
        "boundary_residual": residuals,
        "first_projection": projections,
        "alpha3_anchor": alpha3_anchor_rows(),
        "refusal": refusal_rows(compact, gates, residuals, projections),
        "claim_gates": public_claim_gates(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    branch_copy_rows = copy_branch_rows(
        rows_by_name["boundary_residual"],
        rows_by_name["first_projection"],
        rows_by_name["decision"],
    )
    rows_by_name["branch_copies"] = branch_copy_rows
    write_csv(OUTPUTS["branch_copies"], branch_copy_rows)

    validation_rows = build_validation_rows(rows_by_name, branch_copy_rows)
    write_csv(OUTPUTS["validation"], validation_rows)
    write_document(rows_by_name, validation_rows)
    remove_pycache()

    overall = next(row for row in validation_rows if row["validation_id"] == "VAL2427_OVERALL")
    print(f"{DOC}")
    print(f"{OUTPUTS['validation']}")
    print(f"VAL2427_OVERALL={overall['status']}")


if __name__ == "__main__":
    main()
