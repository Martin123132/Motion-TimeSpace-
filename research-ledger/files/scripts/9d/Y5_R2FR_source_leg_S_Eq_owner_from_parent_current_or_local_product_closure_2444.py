from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_SOURCE_LEG_S_EQ_OWNER_FROM_PARENT_CURRENT_OR_PRODUCT_CLOSURE_2444"
CHECKPOINT_ID = "2444"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
HAMILTONIAN = ROOT / "source-intake" / "hamiltonian-source"

DOC = ROOT / "2444-Y5-R2FR-source-leg-S-Eq-owner-from-parent-current-or-local-product-closure.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2444_SOURCE_REGISTER.csv",
    "source_leg_contract": OUT / "P8_Y5_PARENT_QLOC_2444_SOURCE_LEG_DERIVATION_CONTRACT.csv",
    "parent_current_audit": OUT / "P8_Y5_PARENT_QLOC_2444_PARENT_SOURCE_CURRENT_AUDIT.csv",
    "hamiltonian_bridge": OUT / "P8_Y5_PARENT_QLOC_2444_HAMILTONIAN_SOURCE_CHARGE_BRIDGE.csv",
    "product_closure": OUT / "P8_Y5_PARENT_QLOC_2444_LOCAL_PRODUCT_CLOSURE_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2444_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2444_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2444_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2444_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2444_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_contract": QUEUE / "JR2444_SOURCE_LEG_DERIVATION_CONTRACT_NONCLAIM.csv",
    "queue_product_closure": QUEUE / "JR2444_LOCAL_PRODUCT_CLOSURE_LEDGER_NONCLAIM.csv",
    "wep_contract": MICROSCOPE / "source_leg_S_Eq_contract_nonclaim_2444.csv",
    "local_product_closure": LOCAL_BOUNDS / "MTS_local_product_closure_2444_NONCLAIM.csv",
    "hamiltonian_bridge": HAMILTONIAN / "Hamiltonian_source_charge_bridge_2444_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2444_00_2443_doc",
        "source_path": ROOT / "2443-Y5-R2FR-parent-matter-spectrum-owner-signature-or-bmhat-bnuc-source-leg-bound-pack.md",
        "needles": ["NEXT2443_0_selected", "PBP2443_0_S_Eq_b_mhat", "SLO2443_5_verdict", "VAL2443_OVERALL"],
        "role": "fresh handoff selecting S_E^q source-leg derivation or product closure",
    },
    {
        "source_id": "SRC2444_01_2443_source_leg_csv",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2443_SOURCE_LEG_OWNER_AUDIT.csv",
        "needles": ["SLO2443_0_q_normalization", "SLO2443_5_verdict", "BLOCKED_PRODUCT_ONLY"],
        "role": "current source-leg owner audit",
    },
    {
        "source_id": "SRC2444_02_2443_product_pack",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2443_BMHAT_BNUC_PRODUCT_BOUND_PACK.csv",
        "needles": ["PBP2443_0_S_Eq_b_mhat", "PBP2443_4_absolute_envelope", "ONE_COMPONENT_SMOKE_BOUND"],
        "role": "current local product-bound pack",
    },
    {
        "source_id": "SRC2444_03_990_parent_action_contract",
        "source_path": ROOT / "990-Y5-R10-minimal-parent-action-coupling-contract-EM-matter-GR-reentry.md",
        "needles": ["PAC990_4_source_charge", "LAD990_2_source_mass", "DEC990_1_best_derivation_target"],
        "role": "older parent action contract identifying Hamiltonian source charge as live edge",
    },
    {
        "source_id": "SRC2444_04_991_hamiltonian_pim",
        "source_path": ROOT / "991-Y5-R10-Hamiltonian-PiM-FB5540-integrability-reference-lock-or-source-closure.md",
        "needles": ["FB991_4_coupling_source_measure", "HPT991_7_verdict", "CG991_1_Newton_source"],
        "role": "Hamiltonian Pi_M/source mass obstruction ledger",
    },
    {
        "source_id": "SRC2444_05_1066_source_scalar",
        "source_path": OUT / "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
        "needles": ["SSE1066_5_verdict", "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED", "OBSTRUCTION_SURVIVES"],
        "role": "source-only scalar exclusion remains conditional",
    },
    {
        "source_id": "SRC2444_06_1066_tau_wep",
        "source_path": OUT / "P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv",
        "needles": ["TWP1066_7_verdict", "unity_forbidden", "tau_WEP"],
        "role": "WEP projection/tau contract forbids unity shortcut",
    },
    {
        "source_id": "SRC2444_07_1104_signature",
        "source_path": ROOT / "1104-Y5-R10-parent-ordinary-sector-action-signature-or-explicit-closure-ledger.md",
        "needles": ["SIG1104_4_source_weight_exclusion", "SIG1104_8_projection_maps", "THM1104_2_counterexample_if_any_clause_missing"],
        "role": "ordinary-sector signature ledger with source-weight and projection-map gaps",
    },
    {
        "source_id": "SRC2444_08_1105_closure_pack",
        "source_path": ROOT / "1105-Y5-R10-master-no-hidden-visible-coefficient-morphism-or-explicit-closure-pack.md",
        "needles": ["SUB1105_2_source_weight", "FIN1105_2_WEP_alpha_product", "FIN1105_3_WEP_relative_source_weight"],
        "role": "finite closure pack for source-weight and product rows",
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


def source_leg_contract_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "contract_id": "SLC2444_0_definition",
            "object": "S_A^q",
            "formal_definition": "S_A^q[x_readout] := P_arena[ G_q(x_readout,y) J_q^A(y) dmu_y ] / N_A, with J_q^A := delta S_matter,A / delta q and N_A fixed by the same Hamiltonian/source mass convention",
            "meaning": "source q-leg is a derived projected current, not a free coefficient or unity knob",
            "required_inputs": "explicit q; parent matter action; J_q; Green/screen kernel G_q; arena projection P_arena; source normalization N_A",
            "current_status": "EXACT_CONTRACT_INPUTS_MISSING",
            "claim_effect": "isolated b_i cannot be bounded until S_A^q is owned",
        },
        {
            "contract_id": "SLC2444_1_hamiltonian_variant",
            "object": "S_A^q",
            "formal_definition": "S_A^q = partial ln H_tau[A] / partial q |_{tau_obs,B_ref,Rep_A,screen}, if the source body is represented by an integrable fixed-reference Hamiltonian charge",
            "meaning": "source leg can be the logarithmic q-sensitivity of the owned source charge",
            "required_inputs": "H_tau integrability; fixed B_ref; tau lock; source equality; no boundary/source flux leak",
            "current_status": "CONDITIONAL_BRIDGE_TO_991_NOT_CLOSED",
            "claim_effect": "connects WEP/R10 source leg to GR/Newton source-mass gate",
        },
        {
            "contract_id": "SLC2444_2_universal_zero_route",
            "object": "S_A^q*b_i",
            "formal_definition": "If J_q^A=0 for all ordinary matter sectors, or if q is pure gauge/vertical-silent at the local source after projection, then S_A^q=0 and every product S_A^q*b_i vanishes",
            "meaning": "a real theorem-zero route exists but requires a source-current silence proof",
            "required_inputs": "parent variation order; source-current descent; Ward/Bianchi compatibility; no readout reentry",
            "current_status": "NOT_PARENT_SIGNED",
            "claim_effect": "would close WEP/R10/clock source products if proved",
        },
        {
            "contract_id": "SLC2444_3_unity_refusal",
            "object": "S_A^q",
            "formal_definition": "S_A^q != 1 by convention unless the parent q normalization and source current make that equality true in every shared local arena",
            "meaning": "unit choice cannot replace source-current derivation",
            "required_inputs": "q unit; source normalization; shared WEP/R10/clock/PPN projection",
            "current_status": "UNITY_SHORTCUT_FORBIDDEN",
            "claim_effect": "product rows remain products",
        },
        {
            "contract_id": "SLC2444_4_verdict",
            "object": "S_E^q",
            "formal_definition": "S_E^q is derivable only after parent current/charge/projection ownership; otherwise all local tests stay product-closure rows",
            "meaning": "the source leg is now the named throat",
            "required_inputs": "SLC2444_0 or SLC2444_1 implemented with no MISSING markers",
            "current_status": "NOT_DERIVED_PRODUCT_CLOSURE_REQUIRED",
            "claim_effect": "no isolated coefficient claim and no local-GR claim",
        },
    ]
    return [base_row(**row) for row in rows]


def parent_current_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("PCA2444_0_q_owner", "q variable and vertical generator are owned", "q(Phi) and v in ker(Dq) with local source/readout role declared", "PARTIAL_SYMBOL_ONLY", "MISSING_Q_NORMALIZATION", False),
        ("PCA2444_1_parent_L", "parent Lagrangian supplies source current by variation", "J_q^A = delta S_matter,A/delta q before readout/projector reduction", "MISSING_EXPLICIT_PARENT_CURRENT", "no S_E^q integral can be evaluated", False),
        ("PCA2444_2_source_worldtube", "Earth/source worldtube and composition are represented in observed frame", "W_E, T_E, Rep_E, composition map and orbit/readout averaging declared", "MISSING", "no WEP/R10 source leg", False),
        ("PCA2444_3_screen_kernel", "finite-range/screen kernel is shared across local arenas", "G_q(lambda; x,y) or theorem-zero local suppression rule", "MISSING", "R10/WEP/clock/PPN projections can drift apart", False),
        ("PCA2444_4_source_scalar_exclusion", "source-only species weights are forbidden or bounded", "no w_A S_A, kappa_A T_A, beta_source_alpha(Xhat) without source row", "CONDITIONAL_NOT_PARENT_DERIVED", "relative source-weight residual remains", False),
        ("PCA2444_5_Ward_Bianchi", "source current obeys conservation/constraint compatibility", "nabla_mu T_total^{mu nu}=0 with selectors/boundaries varied or retained", "OPEN_PARALLEL_GATE", "hidden source leakage can mimic force residual", False),
        ("PCA2444_6_verdict", "parent current owns S_E^q", "PCA2444_0 through PCA2444_5 all pass", "BLOCKED", "S_E^q is not derivable yet", False),
    ]
    return [
        base_row(
            audit_id=audit_id,
            clause=clause,
            required_form=required_form,
            current_status=status,
            blocker=blocker,
            gate_pass=gate_pass,
        )
        for audit_id, clause, required_form, status, blocker, gate_pass in rows
    ]


def hamiltonian_bridge_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "bridge_id": "HSB2444_0_bridge",
            "source_leg_object": "S_E^q",
            "hamiltonian_object": "H_tau[E]",
            "bridge_formula": "S_E^q = partial ln H_tau[E] / partial q when H_tau is integrable, B_ref is fixed, tau is shared, and source equality is proved before orbital calibration",
            "current_status": "CONDITIONAL_BRIDGE_ONLY",
            "missing_inputs": "theta_total; Q_tau; deltaH curl; B_ref owner; tau lock; source equality",
            "local_effect": "WEP/R10 source leg becomes tied to Newtonian source mass instead of an arena knob",
        },
        {
            "bridge_id": "HSB2444_1_FB5540",
            "source_leg_object": "source mass/source leg normalization",
            "hamiltonian_object": "FB554_0 components",
            "bridge_formula": "FB554_0=0 would remove nonintegrability/reference/tau/boundary/source-measure leakage from the Hamiltonian source charge",
            "current_status": "NOT_PROMOTED_BY_991",
            "missing_inputs": "parent current owner and source-measure coupling descent",
            "local_effect": "no Newton/PPN/R10 source claim while FB554_0 remains open",
        },
        {
            "bridge_id": "HSB2444_2_common_mode_guard",
            "source_leg_object": "common source normalization",
            "hamiltonian_object": "measured G or orbital GM",
            "bridge_formula": "a universal common factor can be calibration-like only after species, time, range and frame derivatives are proved zero",
            "current_status": "GUARD_ACTIVE",
            "missing_inputs": "universality and no relative/range/time source-weight residual theorem",
            "local_effect": "do not absorb relative source leg into measured G",
        },
        {
            "bridge_id": "HSB2444_3_verdict",
            "source_leg_object": "S_E^q local source leg",
            "hamiltonian_object": "GR/Newton source charge",
            "bridge_formula": "the S_E^q problem and Hamiltonian source-mass problem are the same throat seen from WEP and GR/Newton sides",
            "current_status": "SHARPENED_NOT_CLOSED",
            "missing_inputs": "explicit parent source current or Hamiltonian source charge certificate",
            "local_effect": "next target should extract J_q/H_tau owner rather than add another phenomenological coefficient",
        },
    ]
    return [base_row(**row) for row in rows]


def product_closure_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "closure_id": "LPC2444_0_WEP_mhat",
            "arena": "MICROSCOPE_WEP_TiPt",
            "retained_product": "S_E^q*b_mhat",
            "closure_rule": "keep as product bound or theorem-zero; never report b_mhat alone",
            "current_bound_status": "one-component smoke from 2443 only",
            "missing_for_claim": "S_E^q derivation; zero premises; direct/shadow terms; DeltaQ_nuc",
            "valid_for_claim": False,
        },
        {
            "closure_id": "LPC2444_1_WEP_alpha",
            "arena": "MICROSCOPE_WEP_TiPt",
            "retained_product": "S_E^q*b_alpha",
            "closure_rule": "keep as product bound or theorem-zero; no alpha-only WEP closure",
            "current_bound_status": "one-component smoke from 2443 only",
            "missing_for_claim": "source leg; mass-sector zero theorem; source-current owner",
            "valid_for_claim": False,
        },
        {
            "closure_id": "LPC2444_2_R10",
            "arena": "R10_short_range",
            "retained_product": "G_q(lambda)*J_q^source*J_q^test or K_X Qbar_source Qbar_test",
            "closure_rule": "finite-range tests need source/test current and kernel, not standalone b_i",
            "current_bound_status": "schema only",
            "missing_for_claim": "lambda kernel; source/test qbar; real curve; product values",
            "valid_for_claim": False,
        },
        {
            "closure_id": "LPC2444_3_clocks",
            "arena": "clock_ratios_redshift",
            "retained_product": "tau_clock*S_source^q*b_i plus readout tail",
            "closure_rule": "clock rows need shared source/time projection and readout descent",
            "current_bound_status": "partial sensitivity only",
            "missing_for_claim": "tau_clock; source leg; K_mu/K_nuc; readout closure",
            "valid_for_claim": False,
        },
        {
            "closure_id": "LPC2444_4_PPN_Newton",
            "arena": "PPN_Newton_orbital",
            "retained_product": "source-charge/metric-response residual vector",
            "closure_rule": "PPN/Newton scoring is downstream of Hamiltonian source charge and weak-field operator",
            "current_bound_status": "not score-ready",
            "missing_for_claim": "H_tau source equality; weak-field solution; PPN response matrix",
            "valid_for_claim": False,
        },
        {
            "closure_id": "LPC2444_5_verdict",
            "arena": "shared_local_tests",
            "retained_product": "all local coupling/source products",
            "closure_rule": "until S_E^q is derived, local tests are product-closure constraints only",
            "current_bound_status": "PRODUCT_CLOSURE_DEMOTED",
            "missing_for_claim": "parent source current or Hamiltonian source charge",
            "valid_for_claim": False,
        },
    ]
    return [base_row(**row, isolated_coefficient_allowed=False, score_ready=False) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2444_0_contract", "S_E^q has an exact derivation contract", "PASS_NONCLAIM", "source leg is defined as projected parent current or Hamiltonian charge sensitivity", True),
        ("CG2444_1_parent_current", "parent current J_q is extracted", "BLOCKED", "explicit parent matter/source variation is missing", False),
        ("CG2444_2_hamiltonian_bridge", "S_E^q equals owned Hamiltonian source charge sensitivity", "BLOCKED", "FB554_0/H_tau integrability/reference/tau/source equality remain open", False),
        ("CG2444_3_unity_shortcut", "S_E^q can be set to 1", "BLOCKED", "unity shortcut is forbidden without q/source normalization proof", False),
        ("CG2444_4_local_scores", "local WEP/R10/clock/PPN tests can isolate coefficients", "BLOCKED", "only product-closure rows are allowed", False),
        ("CG2444_5_local_GR_Newton", "local GR/Newton reduction is closed", "BLOCKED", "source charge and PPN weak-field operator remain downstream open gates", False),
    ]
    return [
        base_row(claim_id=claim_id, claim=claim, gate_status=status, reason=reason, gate_pass=gate_pass)
        for claim_id, claim, status, reason, gate_pass in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2444_0_definition", "SOURCE_LEG_DEFINED_AS_PARENT_CURRENT_OR_HAMILTONIAN_SENSITIVITY", "this is the non-fog definition of S_E^q", "future source rows must cite J_q or H_tau owner"),
        ("DEC2444_1_not_derived", "S_Eq_NOT_DERIVED_IN_CURRENT_CORPUS", "parent current, q normalization, kernel, and Hamiltonian source charge are not closed", "do not isolate b_i coefficients"),
        ("DEC2444_2_demote", "LOCAL_TESTS_DEMOTED_TO_PRODUCT_CLOSURE", "WEP/R10/clocks/PPN can constrain products only until source leg is owned", "keep valid_for_claim=false"),
        ("DEC2444_3_best_next", "TARGET_Jq_OR_Htau_SOURCE_CURRENT_EXTRACTION", "the next leap should extract the source current, not add more residual names", "select 2445"),
        ("DEC2444_4_public", "NO_GITHUB_ACTION", "private nonclaim checkpoint", "continue goal work privately"),
    ]
    return [
        base_row(decision_id=decision_id, decision=decision, rationale=rationale, consequence=consequence)
        for decision_id, decision, rationale, consequence in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    row = {
        "route_id": "NEXT2444_0_selected",
        "selection_status": "selected",
        "target_file": "2445-Y5-R2FR-Jq-source-current-extraction-from-parent-L-or-Htau-source-charge-certificate.md",
        "target_script": "scripts/Y5_R2FR_Jq_source_current_extraction_from_parent_L_or_Htau_source_charge_certificate_2445.py",
        "task": "try to extract the q-source current J_q=delta S_matter/delta q or Hamiltonian H_tau source-charge certificate from the parent action; otherwise keep S_E^q as product-closure only",
        "acceptance_target": "a sourced symbolic current/charge formula with q normalization and projection inputs, or an explicit refusal ledger proving every local coefficient test remains product-only",
        "guardrails": "do not invent parent L terms; do not set S_E^q or tau_arena to 1; do not absorb relative source weights into G; do not claim WEP/R10/PPN/local GR; do not edit formalization-workbench; do not push GitHub",
    }
    return [base_row(**row)]


def copy_outputs() -> list[dict[str, Any]]:
    copy_specs = {
        "queue_contract": (OUTPUTS["source_leg_contract"], COPY_TARGETS["queue_contract"], "source-leg derivation contract queue"),
        "queue_product_closure": (OUTPUTS["product_closure"], COPY_TARGETS["queue_product_closure"], "local product-closure ledger queue"),
        "wep_contract": (OUTPUTS["source_leg_contract"], COPY_TARGETS["wep_contract"], "WEP source-leg contract branch"),
        "local_product_closure": (OUTPUTS["product_closure"], COPY_TARGETS["local_product_closure"], "local bounds product-closure branch"),
        "hamiltonian_bridge": (OUTPUTS["hamiltonian_bridge"], COPY_TARGETS["hamiltonian_bridge"], "Hamiltonian source charge bridge"),
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

    add("VAL2444_00_sources_exist", all(row["path_exists"] for row in data["source_register"]), "all cited source paths exist")
    add("VAL2444_01_source_needles", all(row["needles_found"] for row in data["source_register"]), "all cited source needles are present")
    add(
        "VAL2444_02_contract_written",
        any(row["contract_id"] == "SLC2444_0_definition" and "J_q" in row["formal_definition"] for row in data["source_leg_contract"]),
        "S_E^q source-current definition is written",
    )
    add(
        "VAL2444_03_unity_forbidden",
        any(row["contract_id"] == "SLC2444_3_unity_refusal" and row["current_status"] == "UNITY_SHORTCUT_FORBIDDEN" for row in data["source_leg_contract"]),
        "S_E^q unity shortcut is forbidden",
    )
    add(
        "VAL2444_04_parent_current_blocked",
        any(row["audit_id"] == "PCA2444_6_verdict" and row["current_status"] == "BLOCKED" for row in data["parent_current_audit"]),
        "parent current owner remains blocked",
    )
    add(
        "VAL2444_05_hamiltonian_bridge_not_closed",
        any(row["bridge_id"] == "HSB2444_3_verdict" and row["current_status"] == "SHARPENED_NOT_CLOSED" for row in data["hamiltonian_bridge"]),
        "Hamiltonian source-charge bridge is sharpened but not closed",
    )
    add(
        "VAL2444_06_product_closure_demoted",
        any(row["closure_id"] == "LPC2444_5_verdict" and row["current_bound_status"] == "PRODUCT_CLOSURE_DEMOTED" for row in data["product_closure"]),
        "local tests are demoted to product-closure constraints",
    )
    add(
        "VAL2444_07_no_isolated_coefficients",
        all(not row["isolated_coefficient_allowed"] and not row["score_ready"] for row in data["product_closure"]),
        "no isolated coefficient rows are score-ready",
    )
    add(
        "VAL2444_08_claim_gates_safe",
        all((row["claim_id"] == "CG2444_0_contract" and row["gate_status"] == "PASS_NONCLAIM") or row["gate_status"] == "BLOCKED" for row in data["claim_gates"]),
        "only the source-leg contract passes as nonclaim; all claims stay blocked",
    )
    add(
        "VAL2444_09_next_target_written",
        len(data["next_target"]) == 1 and data["next_target"][0]["route_id"] == "NEXT2444_0_selected",
        "2445 J_q/H_tau source-current target selected",
    )
    add(
        "VAL2444_10_branch_copies",
        all(row["source_exists"] and row["target_exists"] for row in data["branch_copies"]),
        "branch copies exist",
    )
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            name = path.name
            if any(marker in name for marker in ("2444-", "_2444", "2444_", "P8_Y5_PARENT_QLOC_2444", "P8_Y5_BRR545_2444")):
                formalization_hits.append(path)
    add(
        "VAL2444_11_no_formalization_artifacts",
        len(formalization_hits) == 0,
        "no 2444 artifacts were written to formalization-workbench",
        "; ".join(str(path) for path in formalization_hits),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parses(path)
        add(f"VAL2444_CSV_{path.stem}", ok, f"CSV parses with {count} rows", detail)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2444_OVERALL",
        overall,
        "2444 defines S_E^q as a projected parent source current or Hamiltonian sensitivity, blocks derivation under current evidence, and demotes local tests to product closure",
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2444 - Y5/R2FR Source Leg S_Eq Owner From Parent Current Or Local Product Closure

## Result
- 2444 removes the fog around `S_E^q`: the source leg must be a projected parent source current or the q-sensitivity of an owned Hamiltonian source charge.
- Candidate contract: `S_A^q[x] := P_arena[ integral G_q(x,y) J_q^A(y) dmu_y ] / N_A`, with `J_q^A := delta S_matter,A / delta q`.
- Hamiltonian variant: `S_A^q = partial ln H_tau[A] / partial q` only if `H_tau` is integrable, reference-fixed, tau-locked, and source-equal before orbital calibration.
- The contract is useful, but not derived in the current corpus: parent current, q normalization, source worldtube, screen kernel, Ward/Bianchi compatibility and Hamiltonian source charge remain open.
- Therefore WEP/R10/clock/PPN rows are demoted to product-closure constraints only. No isolated `b_alpha`, `b_mhat`, `b_nuc`, or source-weight claim is allowed.

## Source Register
{table(["source_id", "source_path", "path_exists", "needles_found", "role"], data["source_register"])}

## Source Leg Derivation Contract
{table(["contract_id", "object", "formal_definition", "meaning", "required_inputs", "current_status", "claim_effect", "valid_for_claim"], data["source_leg_contract"])}

## Parent Source Current Audit
{table(["audit_id", "clause", "required_form", "current_status", "blocker", "gate_pass", "valid_for_claim"], data["parent_current_audit"])}

## Hamiltonian Source Charge Bridge
{table(["bridge_id", "source_leg_object", "hamiltonian_object", "bridge_formula", "current_status", "missing_inputs", "local_effect", "valid_for_claim"], data["hamiltonian_bridge"])}

## Local Product Closure Ledger
{table(["closure_id", "arena", "retained_product", "closure_rule", "current_bound_status", "missing_for_claim", "isolated_coefficient_allowed", "score_ready", "valid_for_claim"], data["product_closure"])}

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
        "source_leg_contract": source_leg_contract_rows(),
        "parent_current_audit": parent_current_audit_rows(),
        "hamiltonian_bridge": hamiltonian_bridge_rows(),
        "product_closure": product_closure_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next_target": next_target_rows(),
    }

    for key in [
        "source_register",
        "source_leg_contract",
        "parent_current_audit",
        "hamiltonian_bridge",
        "product_closure",
        "claim_gates",
        "decisions",
        "next_target",
    ]:
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
