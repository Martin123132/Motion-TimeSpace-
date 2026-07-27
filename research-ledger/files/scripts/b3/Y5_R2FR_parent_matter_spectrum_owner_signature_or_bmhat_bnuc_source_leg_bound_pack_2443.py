from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_MATTER_SPECTRUM_OWNER_OR_BMHAT_BNUC_SOURCE_LEG_BOUND_PACK_2443"
CHECKPOINT_ID = "2443"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
CLOCKS = ROOT / "source-intake" / "clocks" / "branch_locked_local"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2443-Y5-R2FR-parent-matter-spectrum-owner-signature-or-bmhat-bnuc-source-leg-bound-pack.md"

ETA_MICROSCOPE_1SIGMA = 2.745906e-15
DELTA_Q_MHAT_PT_MINUS_TI = 3.33e-3
DELTA_Q_E_PT_MINUS_TI = 2.04e-3

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2443_SOURCE_REGISTER.csv",
    "signature": OUT / "P8_Y5_PARENT_QLOC_2443_PARENT_MATTER_SPECTRUM_SIGNATURE_AUDIT.csv",
    "source_leg": OUT / "P8_Y5_PARENT_QLOC_2443_SOURCE_LEG_OWNER_AUDIT.csv",
    "product_bounds": OUT / "P8_Y5_PARENT_QLOC_2443_BMHAT_BNUC_PRODUCT_BOUND_PACK.csv",
    "arena_projection": OUT / "P8_Y5_PARENT_QLOC_2443_SHARED_LOCAL_ARENA_PROJECTION_QUEUE.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2443_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2443_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2443_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2443_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2443_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_product_bounds": QUEUE / "JR2443_BMHAT_BNUC_PRODUCT_BOUND_PACK_NONCLAIM.csv",
    "queue_source_leg": QUEUE / "JR2443_SOURCE_LEG_OWNER_AUDIT_NONCLAIM.csv",
    "wep_branch": MICROSCOPE / "bmhat_bnuc_product_bound_pack_nonclaim_2443.csv",
    "clock_branch": CLOCKS / "shared_local_arena_projection_queue_nonclaim_2443.csv",
    "local_bounds_branch": LOCAL_BOUNDS / "MTS_local_product_bound_pack_2443_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2443_00_2442_doc",
        "source_path": ROOT / "2442-Y5-R2FR-mass-sector-bmhat-owner-or-WEP-nuclear-binding-gap.md",
        "needles": ["MZT2442_4_verdict", "BML2442_0_b_mhat", "NEXT2442_0_selected", "VAL2442_OVERALL"],
        "role": "fresh mass-sector handoff selecting parent matter-spectrum/source-leg bound pack",
    },
    {
        "source_id": "SRC2443_01_2442_validation",
        "source_path": OUT / "P8_Y5_BRR545_2442_VALIDATION.csv",
        "needles": ["VAL2442_OVERALL", "PASS"],
        "role": "machine-readable 2442 pass state",
    },
    {
        "source_id": "SRC2443_02_2442_coefficients",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2442_BMHAT_BNUC_COEFFICIENT_LEDGER.csv",
        "needles": ["BML2442_0_b_mhat", "b_nuc", "S_E^q"],
        "role": "retained mass/binding/source-leg coefficient ledger",
    },
    {
        "source_id": "SRC2443_03_2442_wep_projection",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2442_WEP_NUCLEAR_BINDING_PROJECTION.csv",
        "needles": ["WNB2442_0_current_reduced_formula", "DeltaQ_mhat=3.330000e-03", "NO_CANCELLATION_ENVELOPE_ONLY"],
        "role": "WEP formula requiring mass/binding/source terms",
    },
    {
        "source_id": "SRC2443_04_2441_dd_map",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2441_MTS_TO_DD_CHARGE_MAP.csv",
        "needles": ["DDMAP2441_0_b_alpha_to_De", "DDMAP2441_1_missing_b_mhat", "DDMAP2441_5_verdict"],
        "role": "MTS-to-DD charge map showing alpha partial success and mass gap",
    },
    {
        "source_id": "SRC2443_05_2440_material",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2440_WEP_MATERIAL_SENSITIVITY_BASIS.csv",
        "needles": ["WMS2440_2_Pt_minus_Ti", "3.330000e-03", "2.040000e-03"],
        "role": "source-backed Ti/Pt material sensitivity factors",
    },
    {
        "source_id": "SRC2443_06_1805_bound_matrix",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_1805_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv",
        "needles": ["BM1805_0_alpha_clock", "BM1805_2_WEP_alpha_mass", "BM1805_3_R10_yukawa"],
        "role": "older shared arena matrix for WEP, R10 and clock routes",
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


def signature_rows() -> list[dict[str, Any]]:
    rows = [
        ("MSS2443_0_parent_signature", "matter spectrum owner is declared in parent action", "theta_matter = theta_rep or theta_bar(q(Phi)); no extra smooth hidden-visible coefficient maps", "CONTRACT_SHAPE_READY_NOT_SIGNED", "MISSING_PARENT_ACTION_SIGNATURE", False),
        ("MSS2443_1_no_mass_yukawa_X", "hidden mass/Yukawa/QCD coefficient functions are forbidden", "no m_A(Xhat), y_A(Xhat), Lambda_QCD(Xhat), or equivalent scalar coefficient morphism", "COUNTERVERTEX_STILL_LEGAL", "MISSING_OPERATOR_CLASSIFICATION", False),
        ("MSS2443_2_no_binding_X", "hidden nuclear/EM binding response is forbidden", "no B_A(Xhat), beta_A(Xhat), material_marker_A(Xhat), or isotope-preparation marker", "UNSIGNED", "MISSING_BINDING_RESPONSE_OWNER", False),
        ("MSS2443_3_readout_stability", "effective/radiative/readout reduction preserves the owner rule", "observed mass ratios, binding fractions and clock transition ratios factor through the same q-owner", "UNSIGNED", "MISSING_READOUT_RADIATIVE_CLOSURE", False),
        ("MSS2443_4_shared_source_leg", "the same q-normalized source leg feeds WEP/R10/clocks/PPN", "S_source^q = P_source[q,J_source,screen] with no arena-specific patch", "MISSING", "MISSING_SOURCE_LEG_OWNER", False),
        ("MSS2443_5_verdict", "parent matter-spectrum owner closes b_mhat/b_nuc", "MSS2443_0 through MSS2443_4 all pass", "FAIL_CURRENT_CLAIM_PRODUCT_BOUND_PACK_REQUIRED", "B_MHAT_BNUC_RETAINED", False),
    ]
    return [
        base_row(
            signature_id=signature_id,
            owner_claim=claim,
            required_contract=contract,
            current_status=status,
            blocker=blocker,
            gate_pass=gate_pass,
        )
        for signature_id, claim, contract, status, blocker, gate_pass in rows
    ]


def source_leg_rows() -> list[dict[str, Any]]:
    rows = [
        ("SLO2443_0_q_normalization", "q unit and vertical generator normalization", "shared q scale must be fixed before b_i products become comparable", "MISSING", "cannot split S_E^q from b_i", False),
        ("SLO2443_1_source_body", "Earth/source body q-charge or vertical drive", "S_E^q derived from source Hamiltonian/current, not set to 1", "MISSING", "WEP rows remain product bounds only", False),
        ("SLO2443_2_test_body", "test-material qbar projection", "Ti/Pt material response must use the same q and DD charge convention", "PARTIAL_MHAT_E_ONLY", "b_nuc/material tail not numeric", False),
        ("SLO2443_3_screening", "local screening or suppression rule", "same screen/projection must feed R10, WEP, clocks and PPN", "MISSING", "arena-specific silence would be a patch", False),
        ("SLO2443_4_no_cancellation", "absolute envelope policy", "no WEP pass by tuned cancellation between alpha/mass/shadow/projector terms", "ACTIVE_GUARD", "use product bound pack as upper-envelope only", True),
        ("SLO2443_5_verdict", "source leg owner closes local coupling", "all source-leg clauses are owned", "BLOCKED_PRODUCT_ONLY", "cannot claim WEP/local GR", False),
    ]
    return [
        base_row(
            source_leg_id=source_leg_id,
            clause=clause,
            requirement=requirement,
            current_status=status,
            consequence=consequence,
            gate_pass=gate_pass,
        )
        for source_leg_id, clause, requirement, status, consequence, gate_pass in rows
    ]


def product_bound_rows() -> list[dict[str, Any]]:
    b_mhat_product_bound = ETA_MICROSCOPE_1SIGMA / DELTA_Q_MHAT_PT_MINUS_TI
    b_alpha_product_bound = ETA_MICROSCOPE_1SIGMA / DELTA_Q_E_PT_MINUS_TI
    rows = [
        {
            "bound_id": "PBP2443_0_S_Eq_b_mhat",
            "product_symbol": "S_E^q*b_mhat",
            "arena": "MICROSCOPE_WEP_TiPt",
            "projection": "eta_TiPt includes DeltaQ_mhat(Pt-Ti)*S_E^q*b_mhat",
            "bound_value": f"{b_mhat_product_bound:.6e}",
            "bound_units": "dimensionless product",
            "bound_type": "ONE_COMPONENT_SMOKE_BOUND",
            "zero_premises": "b_alpha=b_nuc=direct_delta_w_block=direct_delta_w_shadow=projector_tail=0",
            "blocker": "S_E^q not separated from b_mhat; zero premises not proven",
            "source_backed_inputs": "MICROSCOPE eta_bound and Damour-Donoghue Ti/Pt DeltaQ_mhat",
        },
        {
            "bound_id": "PBP2443_1_S_Eq_b_alpha",
            "product_symbol": "S_E^q*b_alpha",
            "arena": "MICROSCOPE_WEP_TiPt",
            "projection": "eta_TiPt includes DeltaQ_e(Pt-Ti)*S_E^q*b_alpha",
            "bound_value": f"{b_alpha_product_bound:.6e}",
            "bound_units": "dimensionless product",
            "bound_type": "ONE_COMPONENT_SMOKE_BOUND",
            "zero_premises": "b_mhat=b_nuc=direct_delta_w_block=direct_delta_w_shadow=projector_tail=0",
            "blocker": "mass-sector zero theorem and source leg not proven",
            "source_backed_inputs": "MICROSCOPE eta_bound and Damour-Donoghue Ti/Pt DeltaQ_e",
        },
        {
            "bound_id": "PBP2443_2_S_Eq_b_nuc",
            "product_symbol": "S_E^q*b_nuc",
            "arena": "MICROSCOPE_WEP_TiPt",
            "projection": "eta_TiPt includes DeltaQ_nuc(Pt-Ti)*S_E^q*b_nuc once nuclear/material matrix is sourced",
            "bound_value": "MISSING_DELTA_Q_NUC",
            "bound_units": "dimensionless product",
            "bound_type": "SOURCE_READY_PLACEHOLDER",
            "zero_premises": "requires DeltaQ_nuc or beta_A matrix",
            "blocker": "nuclear/material response matrix not sourced for current MTS coefficient basis",
            "source_backed_inputs": "none beyond existence of mass/binding channel",
        },
        {
            "bound_id": "PBP2443_3_direct_delta_w_abs",
            "product_symbol": "direct_delta_w_block + direct_delta_w_shadow + projector_tail_abs",
            "arena": "MICROSCOPE_WEP_TiPt",
            "projection": "direct non-DD channels must enter eta as absolute envelope terms",
            "bound_value": f"{ETA_MICROSCOPE_1SIGMA:.6e}",
            "bound_units": "dimensionless eta contribution",
            "bound_type": "ONE_COMPONENT_SMOKE_BOUND",
            "zero_premises": "all DD alpha/mass/nuclear channels vanish",
            "blocker": "direct channels are not DD charges and lack source/test projection",
            "source_backed_inputs": "MICROSCOPE eta_bound only",
        },
        {
            "bound_id": "PBP2443_4_absolute_envelope",
            "product_symbol": "WEP_product_envelope",
            "arena": "MICROSCOPE_WEP_TiPt",
            "projection": "|DeltaQ_mhat*S_E^q*b_mhat| + |DeltaQ_e*S_E^q*b_alpha| + |DeltaQ_nuc*S_E^q*b_nuc| + |direct terms| <= eta_bound",
            "bound_value": f"{ETA_MICROSCOPE_1SIGMA:.6e}",
            "bound_units": "dimensionless eta envelope",
            "bound_type": "NO_CANCELLATION_ENVELOPE",
            "zero_premises": "none; all terms retained as magnitudes",
            "blocker": "not numeric until component magnitudes and DeltaQ_nuc are sourced",
            "source_backed_inputs": "MICROSCOPE eta_bound and partial DD Ti/Pt charges",
        },
    ]
    return [base_row(**row, score_ready=False, promoted=False) for row in rows]


def arena_projection_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "arena_id": "SAP2443_0_WEP",
            "arena": "WEP_MICROSCOPE_TiPt",
            "shared_projection": "eta_AB = sum_i DeltaQ_i(AB)*S_E^q*b_i + direct_source_shadow_projector_terms",
            "ready_inputs": "DeltaQ_mhat, DeltaQ_e, eta_bound",
            "missing_inputs": "S_E^q; b_i; DeltaQ_nuc; direct channel projection",
            "status": "PARTIAL_PRODUCT_BOUND_PACK_NONCLAIM",
        },
        {
            "arena_id": "SAP2443_1_R10",
            "arena": "R10_short_range",
            "shared_projection": "alpha_X(lambda) ~ K_X Qbar_source(lambda) Qbar_test(lambda)/(4*pi*Z_X*G_obs), with Qbar containing alpha/mass/nuclear/source-weight pieces",
            "ready_inputs": "legacy matrix schema only",
            "missing_inputs": "lambda_X; K_X; Z_X; Qbar_source/test; real curve claim-grade bounds",
            "status": "SCHEMA_ONLY_NONCLAIM",
        },
        {
            "arena_id": "SAP2443_2_clocks",
            "arena": "clock_ratios_and_redshift",
            "shared_projection": "d ln R_ab = DeltaK_alpha*b_alpha*tau_clock + DeltaK_mu*b_mu*tau_clock + DeltaK_nuc*b_nuc*tau_clock + readout_tail",
            "ready_inputs": "alpha clock sensitivity precedent",
            "missing_inputs": "K_mu/K_nuc; tau_clock; readout descent; mass/nuclear coefficients",
            "status": "PARTIAL_SENSITIVITY_NONCLAIM",
        },
        {
            "arena_id": "SAP2443_3_PPN",
            "arena": "local_GR_PPN_orbital",
            "shared_projection": "PPN residual vector receives metric/source/readout leakage from the same source leg and coefficient owner",
            "ready_inputs": "none numeric in this branch",
            "missing_inputs": "weak-field solution; source Hamiltonian owner; conserved stress-energy/source coupling map",
            "status": "LOCAL_GR_NOT_SCORE_READY",
        },
        {
            "arena_id": "SAP2443_4_verdict",
            "arena": "shared_local_projection",
            "shared_projection": "one q/source/screen rule must feed every local arena",
            "ready_inputs": "WEP product-bound skeleton",
            "missing_inputs": "source-leg owner and material/nuclear matrices",
            "status": "NEXT_TARGET_SOURCE_LEG_OWNER",
        },
    ]
    return [base_row(**row, score_ready=False) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2443_0_parent_matter_owner", "parent matter-spectrum owner is signed", "BLOCKED", "contract exists but no parent rule forbids mass/binding/readout countervertices", False),
        ("CG2443_1_source_leg_owner", "S_E^q source leg is derived", "BLOCKED", "source Hamiltonian/current projection and q normalization are missing", False),
        ("CG2443_2_product_bounds", "WEP product bounds are source-backed smoke rows", "PASS_NONCLAIM", "partial product bounds follow from MICROSCOPE eta and DD Ti/Pt charges under zero-premise assumptions", True),
        ("CG2443_3_numeric_WEP_score", "MTS WEP branch is numerically score-ready", "BLOCKED", "b_i values, S_E^q, DeltaQ_nuc and direct channel projections are missing", False),
        ("CG2443_4_shared_local_tests", "R10/clocks/PPN share a numeric projection", "BLOCKED", "shared source/screen rule is not derived", False),
        ("CG2443_5_local_GR_Newton", "local GR/Newton limit is closed", "BLOCKED", "this is still a coupling/source product ledger, not a PPN derivation", False),
    ]
    return [
        base_row(claim_id=claim_id, claim=claim, gate_status=status, reason=reason, gate_pass=gate_pass)
        for claim_id, claim, status, reason, gate_pass in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2443_0_signature", "PARENT_SIGNATURE_NOT_SIGNED", "mass-sector owner remains a contract, not a theorem in the present parent action", "retain b_mhat/b_nuc"),
        ("DEC2443_1_products", "PRODUCT_BOUND_PACK_ACCEPTED_AS_NONCLAIM", "the WEP scale can constrain products such as S_E^q*b_mhat under explicit zero-premise smoke assumptions", "use rows for future runner plumbing only"),
        ("DEC2443_2_source_leg", "SOURCE_LEG_IS_NEXT_THROAT", "without S_E^q, no local coefficient can be isolated or compared across arenas", "target source Hamiltonian/current owner"),
        ("DEC2443_3_shared_arena", "ONE_LOCAL_PROJECTION_RULE_REQUIRED", "WEP/R10/clocks/PPN cannot each get separate ad hoc screening", "force shared q/source/screen contract"),
        ("DEC2443_4_public", "NO_GITHUB_ACTION", "private nonclaim checkpoint", "continue goal work privately"),
    ]
    return [
        base_row(decision_id=decision_id, decision=decision, rationale=rationale, consequence=consequence)
        for decision_id, decision, rationale, consequence in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    row = {
        "route_id": "NEXT2443_0_selected",
        "selection_status": "selected",
        "target_file": "2444-Y5-R2FR-source-leg-S-Eq-owner-from-parent-current-or-local-product-closure.md",
        "target_script": "scripts/Y5_R2FR_source_leg_S_Eq_owner_from_parent_current_or_local_product_closure_2444.py",
        "task": "derive S_E^q from the parent source Hamiltonian/current and q normalization, or demote local WEP/R10/clock/PPN coefficient tests to product-closure rows only",
        "acceptance_target": "a shared source-leg formula exists for Earth/test/source bodies across local arenas, or all local tests remain explicit product bounds with no isolated coefficient claims",
        "guardrails": "do not set S_E^q=1; do not use arena-specific screening; do not hide direct source-shadow terms; do not claim WEP/local GR; do not edit formalization-workbench; do not push GitHub",
    }
    return [base_row(**row)]


def copy_outputs() -> list[dict[str, Any]]:
    copy_specs = {
        "queue_product_bounds": (OUTPUTS["product_bounds"], COPY_TARGETS["queue_product_bounds"], "product bound pack queue"),
        "queue_source_leg": (OUTPUTS["source_leg"], COPY_TARGETS["queue_source_leg"], "source leg owner audit queue"),
        "wep_branch": (OUTPUTS["product_bounds"], COPY_TARGETS["wep_branch"], "MICROSCOPE WEP branch nonclaim product pack"),
        "clock_branch": (OUTPUTS["arena_projection"], COPY_TARGETS["clock_branch"], "shared local arena projection queue"),
        "local_bounds_branch": (OUTPUTS["product_bounds"], COPY_TARGETS["local_bounds_branch"], "local bounds branch nonclaim product pack"),
    }
    rows: list[dict[str, Any]] = []
    for copy_id, (source, target, notes) in copy_specs.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.exists():
            shutil.copyfile(source, target)
        rows.append(
            base_row(
                copy_id=copy_id,
                source_path=source,
                target_path=target,
                source_exists=source.exists(),
                target_exists=target.exists(),
                notes=notes,
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, ok: bool, notes: str, detail: str = "") -> None:
        rows.append({"check_id": check_id, "status": "PASS" if ok else "FAIL", "notes": notes, "detail": detail})

    add("VAL2443_00_sources_exist", all(row["path_exists"] for row in data["source_register"]), "all cited source paths exist")
    add("VAL2443_01_source_needles", all(row["needles_found"] for row in data["source_register"]), "all cited source needles are present")
    add(
        "VAL2443_02_signature_blocked",
        any(row["signature_id"] == "MSS2443_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_PRODUCT_BOUND_PACK_REQUIRED" for row in data["signature"]),
        "parent matter-spectrum signature remains blocked",
    )
    add(
        "VAL2443_03_source_leg_missing",
        any(row["source_leg_id"] == "SLO2443_5_verdict" and row["current_status"] == "BLOCKED_PRODUCT_ONLY" for row in data["source_leg"]),
        "source leg owner is missing and rows remain product-only",
    )
    required_products = {"S_E^q*b_mhat", "S_E^q*b_alpha", "S_E^q*b_nuc", "WEP_product_envelope"}
    found_products = {row["product_symbol"] for row in data["product_bounds"]}
    add("VAL2443_04_product_rows_present", required_products <= found_products, "mass, alpha, nuclear and envelope product rows are present")
    add(
        "VAL2443_05_no_score_ready_products",
        all(not row["score_ready"] and not row["promoted"] for row in data["product_bounds"]),
        "product rows are not score-ready or promoted",
    )
    add(
        "VAL2443_06_shared_arenas_present",
        {"WEP_MICROSCOPE_TiPt", "R10_short_range", "clock_ratios_and_redshift", "local_GR_PPN_orbital"} <= {row["arena"] for row in data["arena_projection"]},
        "WEP/R10/clock/PPN arenas are queued under one shared local projection policy",
    )
    add(
        "VAL2443_07_claim_gates_safe",
        all((row["claim_id"] == "CG2443_2_product_bounds" and row["gate_status"] == "PASS_NONCLAIM") or row["gate_status"] == "BLOCKED" for row in data["claim_gates"]),
        "only product-bound smoke row passes as nonclaim; claim gates remain blocked",
    )
    add(
        "VAL2443_08_next_target_written",
        len(data["next_target"]) == 1 and data["next_target"][0]["route_id"] == "NEXT2443_0_selected",
        "2444 source-leg owner target selected",
    )
    add(
        "VAL2443_09_branch_copies",
        all(row["source_exists"] and row["target_exists"] for row in data["branch_copies"]),
        "branch copies exist",
    )
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            name = path.name
            if any(marker in name for marker in ("2443-", "_2443", "2443_", "P8_Y5_PARENT_QLOC_2443", "P8_Y5_BRR545_2443")):
                formalization_hits.append(path)
    add(
        "VAL2443_10_no_formalization_artifacts",
        len(formalization_hits) == 0,
        "no 2443 artifacts were written to formalization-workbench",
        "; ".join(str(path) for path in formalization_hits),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parses(path)
        add(f"VAL2443_CSV_{path.stem}", ok, f"CSV parses with {count} rows", detail)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2443_OVERALL",
        overall,
        "2443 converts the live mass/binding coupling problem into explicit nonclaim product-bound rows and selects source-leg derivation next",
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2443 - Y5/R2FR Parent Matter Spectrum Owner Or Bmhat/Bnuc Source-Leg Bound Pack

## Result
- 2443 tries the parent matter-spectrum owner route again and keeps it honest: the contract is now explicit, but it is still not signed by the current parent action.
- The checkpoint therefore builds a nonclaim product-bound pack instead of pretending WEP is solved.
- The useful sourced smoke products are `|S_E^q*b_mhat| <= {ETA_MICROSCOPE_1SIGMA / DELTA_Q_MHAT_PT_MINUS_TI:.6e}` and `|S_E^q*b_alpha| <= {ETA_MICROSCOPE_1SIGMA / DELTA_Q_E_PT_MINUS_TI:.6e}` under explicit one-component zero-premise assumptions.
- `S_E^q*b_nuc` is source-ready but not numeric because the nuclear/material response matrix is still missing.
- The next throat is no longer vague coupling. It is the source leg: derive `S_E^q` from the parent source Hamiltonian/current and q normalization, or keep local tests as product-closure rows only.

## Source Register
{table(["source_id", "source_path", "path_exists", "needles_found", "role"], data["source_register"])}

## Parent Matter Spectrum Signature Audit
{table(["signature_id", "owner_claim", "required_contract", "current_status", "blocker", "gate_pass", "valid_for_claim"], data["signature"])}

## Source Leg Owner Audit
{table(["source_leg_id", "clause", "requirement", "current_status", "consequence", "gate_pass", "valid_for_claim"], data["source_leg"])}

## Bmhat / Bnuc Product Bound Pack
{table(["bound_id", "product_symbol", "arena", "projection", "bound_value", "bound_units", "bound_type", "zero_premises", "blocker", "source_backed_inputs", "score_ready", "promoted", "valid_for_claim"], data["product_bounds"])}

## Shared Local Arena Projection Queue
{table(["arena_id", "arena", "shared_projection", "ready_inputs", "missing_inputs", "status", "score_ready", "valid_for_claim"], data["arena_projection"])}

## Claim Gates
{table(["claim_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"], data["claim_gates"])}

## Decision Ledger
{table(["decision_id", "decision", "rationale", "consequence", "valid_for_claim"], data["decisions"])}

## Next Target
{table(["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"], data["next_target"])}

## Branch Copies
{table(["copy_id", "source_path", "target_path", "source_exists", "target_exists", "notes"], data["branch_copies"])}

## Validation
{table(["check_id", "status", "notes", "detail"], data["validation"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    data: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "signature": signature_rows(),
        "source_leg": source_leg_rows(),
        "product_bounds": product_bound_rows(),
        "arena_projection": arena_projection_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next_target": next_target_rows(),
    }

    for key in ["source_register", "signature", "source_leg", "product_bounds", "arena_projection", "claim_gates", "decisions", "next_target"]:
        write_csv(OUTPUTS[key], data[key])

    data["branch_copies"] = copy_outputs()
    write_csv(OUTPUTS["branch_copies"], data["branch_copies"])

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    data["validation"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)


if __name__ == "__main__":
    main()
