from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1234"
TITLE = "1234-Y5-R10-EM-owner-uniqueness-or-quark-gluon-edge-owner-proof"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
EM_UNIQUENESS_PATH = OUT_DIR / f"{PACK_ID}_EM_OWNER_UNIQUENESS_PROOF_ATTEMPT.csv"
EM_BLOCKER_PATH = OUT_DIR / f"{PACK_ID}_EM_OWNER_BLOCKER_LEDGER.csv"
QUARK_GLUON_PATH = OUT_DIR / f"{PACK_ID}_QUARK_GLUON_EDGE_OWNER_FALLBACK.csv"
EDGE_STATUS_PATH = OUT_DIR / f"{PACK_ID}_GRAPH_EDGE_STATUS_UPDATE.csv"
FINITE_EM_PATH = OUT_DIR / f"{PACK_ID}_FINITE_EM_RESIDUAL_BACKSTOP.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1234_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def is_false(row: dict[str, object], key: str) -> bool:
    return not parse_bool(row.get(key, False))


def source_ref(relative_path: str, needle: str) -> str:
    return f"{relative_path}:{needle}"


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > RUN_STARTED_UTC
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1234_0_1233_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1233_NEXT_TARGET.csv",
            "needle": "NEXT1233_0_1234",
            "purpose": "1233 handoff to EM owner uniqueness or quark-gluon edge proof",
        },
        {
            "source_id": "SRC1234_1_1233_edge",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1233_EM_CURRENT_EDGE_OWNER_PROOF_ATTEMPT.csv",
            "needle": "EME1233_4_graph_edge_verdict",
            "purpose": "electron-photon edge demotion",
        },
        {
            "source_id": "SRC1234_2_989_em_lock",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv",
            "needle": "ELA989_5_total",
            "purpose": "EM lock signature blocker ledger",
        },
        {
            "source_id": "SRC1234_3_988_em_gate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_988_EM_LOCK_THEOREM_GATE.csv",
            "needle": "EMLOCK988_5_theorem_verdict",
            "purpose": "EM lock theorem gate",
        },
        {
            "source_id": "SRC1234_4_987_normal_forms",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_987_EM_NORMAL_FORMS.csv",
            "needle": "EMNF987_4_verdict",
            "purpose": "EM normal form alternatives",
        },
        {
            "source_id": "SRC1234_5_1055_parent_action",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
            "needle": "PAC1055_1_EM_owner",
            "purpose": "parent EM owner candidate",
        },
        {
            "source_id": "SRC1234_6_1219_hidden_alpha",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1219_HIDDEN_SCALAR_COUNTEREXAMPLE_LOCK.csv",
            "needle": "HSC1219_1_alpha",
            "purpose": "active hidden alpha/F2 counterexample",
        },
        {
            "source_id": "SRC1234_7_1065_charge_norm",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1065_CHARGE_INTERACTION_NORMALIZATION_AUDIT.csv",
            "needle": "CIN1065_4_verdict",
            "purpose": "charge/current normalization remains conditional",
        },
        {
            "source_id": "SRC1234_8_1232_edges",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1232_ORDINARY_MATTER_GRAPH_EDGE_AUDIT.csv",
            "needle": "EDGE1232_2_quark_gluon",
            "purpose": "quark-gluon edge fallback target",
        },
        {
            "source_id": "SRC1234_9_1232_source_pack",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1232_TIPT_COMPONENT_FRACTION_SOURCE_PACK.csv",
            "needle": "FSP1232_4_QCD_gluon_fraction",
            "purpose": "QCD component source pack gap",
        },
    ]

    source_register = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "absolute_path": str(source_path(spec["local_path"])),
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    em_uniqueness = [
        {
            "proof_id": "EMU1234_0_target",
            "claim_piece": "EM owner uniqueness for EDGE1232_0",
            "formal_statement": "Observed EM is the unique compact U(1) subblock of the parent connection/curvature norm, with fixed generator T_Q, fixed kinetic norm, fixed current normalization, and quotient-fixed readout.",
            "attempt_result": "TARGET_SHARPENED",
            "gap": "all four ownership clauses must be parent-signed together",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "EMU1234_1_charge_generator",
            "claim_piece": "compact charge generator owner",
            "formal_statement": "T_Q is a parent action object with fixed lattice/norm, so charge units cannot be rescaled independently of the matter representation.",
            "attempt_result": "CONDITIONAL_CLAUSE_ONLY",
            "gap": "T_Q is theorem-shape only, not an owned parent-action object",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv", "ELA989_0_TQ_owner"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "EMU1234_2_unique_F2",
            "claim_piece": "unique Maxwell kinetic term",
            "formal_statement": "F_Q^2 descends only from the parent curvature norm; no independent lambda_A F_Q^2 or f(I_hid)F_Q^2 term is in the action domain.",
            "attempt_result": "FAILS_CURRENT_CORPUS",
            "gap": "lambda_A F_Q^2 and hidden scalar gauge-kinetic functions remain legal counterexamples unless typed out",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_988_EM_LOCK_THEOREM_GATE.csv", "EMLOCK988_1_unique_Maxwell_F2"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "EMU1234_3_current_owner",
            "claim_piece": "charge-current normalization owner",
            "formal_statement": "Matter current, charge labels, and Maxwell source normalization descend from the same T_Q Noether owner.",
            "attempt_result": "CONDITIONAL_UNSIGNED",
            "gap": "current rescaling and beta_source_alpha remain unowned",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv", "ELA989_2_current_owner"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "EMU1234_4_readout_descent",
            "claim_piece": "dimensionless alpha/readout descent",
            "formal_statement": "Hodge star, coframe, hbar*c, and spectroscopy/readout factors are quotient-fixed so alpha_EM cannot drift through units.",
            "attempt_result": "CONDITIONAL_UNSIGNED",
            "gap": "coframe/Hodge/readout leakage remains possible",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv", "ELA989_3_readout_descent"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "EMU1234_5_no_alpha_vertex",
            "claim_piece": "no hidden alpha/mass/binding vertex",
            "formal_statement": "S_matter has no alpha_EM(chi_X), f(chi_X)F_Q^2, m_A(chi_X), or binding response vertex after parent quotient and readout.",
            "attempt_result": "CONDITIONAL_UNSIGNED",
            "gap": "HSC1219_1 alpha and matter/binding hidden coefficient counterexamples remain active",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1219_HIDDEN_SCALAR_COUNTEREXAMPLE_LOCK.csv", "HSC1219_1_alpha"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "EMU1234_6_verdict",
            "claim_piece": "EM owner uniqueness signs EDGE1232_0",
            "formal_statement": "EMU1234_1 through EMU1234_5 all parent-signed would sign the electron-photon edge and remove alpha-current drift from that edge.",
            "attempt_result": "EM_OWNER_UNIQUENESS_NOT_CLOSED",
            "gap": "unique_F2 fails current corpus and every other ownership clause is unsigned",
            "source": "EMU1234_1 through EMU1234_5",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    em_blockers = [
        {
            "blocker_id": "EMB1234_0_unique_F2_counterexample",
            "counterexample": "lambda_A F_Q^2 or f(I_hid)F_Q^2",
            "why_it_survives": "visible U(1) and diffeomorphism invariance allow scalar gauge-kinetic functions unless parent typing excludes hidden scalar arguments",
            "required_to_close": "parent typed coefficient domain or unique parent curvature norm",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "EMB1234_1_current_rescaling",
            "counterexample": "current/source normalization rescaling independent of charge measurement",
            "why_it_survives": "Ward identities conserve currents but do not by themselves fix absolute source/force normalization",
            "required_to_close": "single T_Q Noether owner for charge, current, and source normalization",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "EMB1234_2_readout_units",
            "counterexample": "alpha drift through coframe/Hodge/hbar*c/readout units",
            "why_it_survives": "dimensionless readout descent is not parent-signed",
            "required_to_close": "quotient-fixed readout and radiative closure theorem",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "EMB1234_3_matter_vertex",
            "counterexample": "hidden alpha, mass, clock, or binding coefficient in matter/readout sector",
            "why_it_survives": "typed visible coefficient functor is conditional only",
            "required_to_close": "parent matter functor plus no-hidden-visible coefficient theorem",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    quark_gluon = [
        {
            "fallback_id": "QGE1234_0_target",
            "edge": "EDGE1232_2_quark_gluon",
            "claim_piece": "quark-gluon parent graph edge owner",
            "formal_statement": "Light quark mass and QCD/gluon binding components are connected by a parent-owned non-Abelian gauge interaction and hadronization/bound-state map.",
            "attempt_result": "TARGET_STAGED_NOT_PROVED",
            "gap": "strong-sector parent action owner and mass-decomposition basis are not audited in this checkpoint",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "fallback_id": "QGE1234_1_promising_route",
            "edge": "EDGE1232_2_quark_gluon",
            "claim_piece": "nonzero interaction morphism route",
            "formal_statement": "If ordinary matter includes a parent-owned color gauge sector with quarks in nontrivial representations, the quark-gluon edge is nonzero and helps graph connectedness.",
            "attempt_result": "EXACT_CONDITIONAL_ROUTE",
            "gap": "current MTS parent action has not supplied the color-sector owner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "fallback_id": "QGE1234_2_fraction_backstop",
            "edge": "EDGE1232_2_quark_gluon",
            "claim_piece": "finite QCD component branch",
            "formal_statement": "If no parent edge owner is signed, retain F_{B,q}, F_{B,g}, delta w_q, and delta w_g as component-fraction/prior inputs.",
            "attempt_result": "BACKSTOP_ACTIVE",
            "gap": "FSP1232_3 and FSP1232_4 remain missing parent or phenomenological basis",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    edge_status = [
        {
            "edge_id": "EDGE1232_0_electron_photon",
            "prior_status": "CONDITIONAL_MATH_CLEAR_NOT_PARENT_SIGNED",
            "new_status": "EM_OWNER_UNIQUENESS_NOT_CLOSED",
            "reason": "unique F2 fails current corpus; T_Q/current/readout/no-alpha clauses unsigned",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "EDGE1232_1_quark_photon",
            "prior_status": "PENDING_FUTURE_EDGE_OWNER_PROOF",
            "new_status": "PENDING",
            "reason": "not attempted in 1234",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "EDGE1232_2_quark_gluon",
            "prior_status": "PENDING_FUTURE_EDGE_OWNER_PROOF",
            "new_status": "EXACT_CONDITIONAL_ROUTE_STAGED_NOT_SIGNED",
            "reason": "color/QCD parent owner and mass-decomposition basis missing",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    finite_em = [
        {
            "residual_id": "FEM1234_0_alpha_kinetic",
            "quantity": "b_alpha or c_alpha_DD",
            "source_of_residual": "unclosed unique F2 / hidden scalar gauge kinetic counterexample",
            "status": "FINITE_RESIDUAL_ACTIVE",
            "required_to_score": "source-backed coefficient prior or parent EM-lock theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "FEM1234_1_beta_source_alpha",
            "quantity": "beta_source_alpha",
            "source_of_residual": "unowned current/source normalization",
            "status": "FINITE_RESIDUAL_ACTIVE",
            "required_to_score": "parent current owner or numeric beta prior with source path",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "FEM1234_2_readout_alpha",
            "quantity": "tau_clock/tau_WEP/readout alpha transfer",
            "source_of_residual": "unclosed quotient-fixed readout/radiative descent",
            "status": "FINITE_RESIDUAL_ACTIVE",
            "required_to_score": "official readout kernels or parent readout theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1234_0_no_EM_edge_sign",
            "decision": "do not sign EDGE1232_0",
            "because": "EM owner uniqueness fails on unique F2 and remains unsigned on generator/current/readout/no-alpha clauses",
            "next_action": "either derive typed coefficient domain/unique curvature norm or keep finite EM residual rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1234_1_quark_gluon_next",
            "decision": "stage quark-gluon edge as next graph route",
            "because": "EM edge is narrowed but still blocked; a color-sector edge may give a different parent-owner route",
            "next_action": "attack QCD/color parent owner or build QCD component-fraction source rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1234_2_no_claim_promotion",
            "decision": "keep graph, Delta_w, WEP, and local GR blocked",
            "because": "no parent edge is signed and finite residual branch remains active",
            "next_action": "continue derivation-first with nonclaim backstops",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1234_0_EM_owner",
            "claim": "EM owner uniqueness theorem",
            "status": "BLOCKED",
            "reason": "EMU1234_6 verdict=EM_OWNER_UNIQUENESS_NOT_CLOSED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1234_1_EDGE1232_0",
            "claim": "electron-photon edge parent-signed",
            "status": "BLOCKED",
            "reason": "EDGE1232_0 does not count for connected graph",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1234_2_EDGE1232_2",
            "claim": "quark-gluon edge parent-signed",
            "status": "BLOCKED",
            "reason": "QGE1234 route is conditional only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1234_3_graph_connectedness",
            "claim": "ordinary matter graph connected with signed edges",
            "status": "BLOCKED",
            "reason": "no attempted edge is parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1234_4_local_GR",
            "claim": "local GR/Newton source-side reduction",
            "status": "BLOCKED",
            "reason": "source-coupling graph and finite residual rows remain open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1234_0_1235",
            "target_file": "1235-Y5-R10-unique-F2-typed-coefficient-domain-or-QCD-color-edge-owner.md",
            "target_script": "scripts/Y5_R10_unique_F2_typed_coefficient_domain_or_QCD_color_edge_owner.py",
            "task": "attack the exact blocker: either prove hidden scalar coefficient maps into F_Q^2 are ill-typed/absent, or shift to QCD color edge ownership with finite QCD component backstop",
            "success_condition": "unique-F2 blocker is closed or demoted with a precise finite EM residual; if shifting to QCD, the color edge receives a parent-owner proof attempt",
            "do_not_do": "do not claim EM lock, graph connectedness, Delta_w=0, WEP, PPN, local GR, or use finite residual rows as predictions",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_paths = [
        SOURCE_REGISTER_PATH,
        EM_UNIQUENESS_PATH,
        EM_BLOCKER_PATH,
        QUARK_GLUON_PATH,
        EDGE_STATUS_PATH,
        FINITE_EM_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(EM_UNIQUENESS_PATH, em_uniqueness)
    write_csv(EM_BLOCKER_PATH, em_blockers)
    write_csv(QUARK_GLUON_PATH, quark_gluon)
    write_csv(EDGE_STATUS_PATH, edge_status)
    write_csv(FINITE_EM_PATH, finite_em)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(NEXT_PATH, next_target)

    parsed_counts: list[str] = []
    csv_parse_ok = True
    for path in generated_paths:
        try:
            parsed_counts.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_counts.append(f"{path.name}:ERROR:{exc}")

    all_sources_exist = all(parse_bool(row["path_exists"]) for row in source_register)
    all_needles_found = all(parse_bool(row["needle_found"]) for row in source_register)
    all_generated_nonclaim = all(
        is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
        for table in [
            source_register,
            em_uniqueness,
            em_blockers,
            quark_gluon,
            edge_status,
            finite_em,
            decisions,
            claim_gates,
            next_target,
        ]
        for row in table
    )
    em_not_closed = any(row["proof_id"] == "EMU1234_6_verdict" and row["attempt_result"] == "EM_OWNER_UNIQUENESS_NOT_CLOSED" for row in em_uniqueness)
    unique_f2_active = any(row["blocker_id"] == "EMB1234_0_unique_F2_counterexample" and row["status"] == "ACTIVE" for row in em_blockers)
    qcd_staged = any(row["fallback_id"] == "QGE1234_1_promising_route" and row["attempt_result"] == "EXACT_CONDITIONAL_ROUTE" for row in quark_gluon)
    no_edges_signed = all(parse_bool(row["counts_for_connected_graph"]) is False for row in edge_status)
    finite_backstop = len(finite_em) == 3 and all(row["status"] == "FINITE_RESIDUAL_ACTIVE" for row in finite_em)
    gates_blocked = all(row["status"] == "BLOCKED" and is_false(row, "claim_allowed") for row in claim_gates)
    next_is_1235 = next_target[0]["target_file"].startswith("1235-Y5-R10-unique-F2")
    fw_recent = formalization_recent_count()

    validation = [
        validation_row(
            "VAL1234_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(parse_bool(row['path_exists']) for row in source_register)}/{len(source_register)} sources exist",
        ),
        validation_row(
            "VAL1234_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(parse_bool(row['needle_found']) for row in source_register)}/{len(source_register)} needles found",
        ),
        validation_row(
            "VAL1234_2_em_not_closed",
            "EM owner uniqueness is not promoted",
            em_not_closed,
            "EMU1234_6 verdict=EM_OWNER_UNIQUENESS_NOT_CLOSED",
        ),
        validation_row(
            "VAL1234_3_unique_F2_active",
            "unique-F2 counterexample remains active",
            unique_f2_active,
            "EMB1234_0 status=ACTIVE",
        ),
        validation_row(
            "VAL1234_4_qcd_staged",
            "quark-gluon fallback route is staged",
            qcd_staged,
            "QGE1234_1 exact conditional route",
        ),
        validation_row(
            "VAL1234_5_no_edges_signed",
            "no graph edge is counted as parent-signed",
            no_edges_signed,
            "counts_for_connected_graph=false for all updated edges",
        ),
        validation_row(
            "VAL1234_6_finite_backstop",
            "finite EM residual backstop remains active",
            finite_backstop,
            f"finite_em_rows={len(finite_em)}",
        ),
        validation_row(
            "VAL1234_7_claim_gates_blocked",
            "all claim gates remain blocked",
            gates_blocked,
            f"blocked_gates={sum(row['status'] == 'BLOCKED' for row in claim_gates)}/{len(claim_gates)}",
        ),
        validation_row(
            "VAL1234_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_generated_nonclaim,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1234_9_next_target_1235",
            "next target attacks unique-F2 typed domain or QCD edge",
            next_is_1235,
            next_target[0]["target_file"],
        ),
        validation_row(
            "VAL1234_10_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_counts),
        ),
        validation_row(
            "VAL1234_11_formalization_untouched",
            "formalization-workbench untouched during run",
            fw_recent == 0,
            f"formalization_recent_write_count_since_run_start={fw_recent}",
        ),
    ]
    validation.append(
        validation_row(
            "VAL1234_12_overall",
            "overall 1234 validation",
            all(row["status"] == "PASS" for row in validation),
            "1234 refuses EM-owner promotion, identifies unique-F2 as the sharp blocker, and stages QCD edge fallback",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    sections = [
        f"# {TITLE}",
        "",
        "**Current verdict:** 1234 does **not** close EM-owner uniqueness or sign the electron-photon graph edge. The sharp blocker is now `unique F_Q^2`: hidden scalar gauge-kinetic maps and independent Maxwell kinetic terms remain legal unless the parent typed coefficient domain or unique curvature norm is derived.",
        "",
        "**Main progress:** the EM edge is no longer vaguely unsigned. It fails on a named clause (`EMU1234_2_unique_F2`) and keeps finite EM residual backstops. The quark-gluon edge route is staged as the next graph-edge alternative, also nonclaim.",
        "",
        "**No-claim guard:** no EM lock, graph connectedness, `Delta_w=0`, WEP, PPN, clock, orbital, local-GR, or public source-coupling claim is promoted.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source Register",
        markdown_table(source_register, list(source_register[0].keys())),
        "",
        "## EM Owner Uniqueness Proof Attempt",
        markdown_table(em_uniqueness, list(em_uniqueness[0].keys())),
        "",
        "## EM Owner Blocker Ledger",
        markdown_table(em_blockers, list(em_blockers[0].keys())),
        "",
        "## Quark-Gluon Edge Owner Fallback",
        markdown_table(quark_gluon, list(quark_gluon[0].keys())),
        "",
        "## Graph Edge Status Update",
        markdown_table(edge_status, list(edge_status[0].keys())),
        "",
        "## Finite EM Residual Backstop",
        markdown_table(finite_em, list(finite_em[0].keys())),
        "",
        "## Decision Ledger",
        markdown_table(decisions, list(decisions[0].keys())),
        "",
        "## Claim Gates",
        markdown_table(claim_gates, list(claim_gates[0].keys())),
        "",
        "## Next Target",
        markdown_table(next_target, list(next_target[0].keys())),
        "",
        "## Validation",
        markdown_table(validation, list(validation[0].keys())),
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
