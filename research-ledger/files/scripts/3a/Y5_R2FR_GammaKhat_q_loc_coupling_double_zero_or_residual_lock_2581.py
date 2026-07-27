from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_GAMMAKHAT_QLOC_COUPLING_2581"
CHECKPOINT_ID = "2581"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2581-Y5-R2FR-GammaKhat-q_loc-coupling-double-zero-or-residual-lock.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_GAMMAKHAT_QLOC_2581_SOURCE_REGISTER.csv",
    "proof_gate": OUT / "P8_Y5_GAMMAKHAT_QLOC_2581_DERIVATION_PROOF_GATE.csv",
    "residual_interface": OUT / "P8_Y5_GAMMAKHAT_QLOC_2581_OFFICIAL_RESIDUAL_INTERFACE.csv",
    "local_test_map": OUT / "P8_Y5_GAMMAKHAT_QLOC_2581_LOCAL_TEST_MAP.csv",
    "claim_gates": OUT / "P8_Y5_GAMMAKHAT_QLOC_2581_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_GAMMAKHAT_QLOC_2581_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_GAMMAKHAT_QLOC_2581_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_GAMMAKHAT_QLOC_2581_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2581_VALIDATION.csv",
}

COPY_TARGETS = {
    "proof_gate": QUEUE / "JR2581_GAMMAKHAT_QLOC_DERIVATION_PROOF_GATE_NONCLAIM.csv",
    "residual_interface": LOCAL_BOUNDS / "GammaKhat_q_loc_official_residual_interface_2581_NONCLAIM.csv",
    "local_test_map": QUEUE / "JR2581_QLOC_LOCAL_TEST_MAP_NONCLAIM.csv",
    "next_target": QUEUE / "JR2581_RESPONSE_DOUBLET_OR_QLOC_BOUND_NEXT.csv",
}

SOURCES = [
    {
        "source_id": "SRC2581_00_2580_handoff",
        "source_path": ROOT / "2580-Y5-R2FR-parent-extra-sector-inventory-coupling-map-or-leakage-bounds.md",
        "needles": ["NEXT2580_0_selected", "EI2580_0_GK", "VAL2580_OVERALL"],
        "role": "active handoff selecting Gamma/Khat/q_loc first",
    },
    {
        "source_id": "SRC2581_01_1010_GK_gate",
        "source_path": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
        "needles": ["GKT1010_6_verdict", "QRES1010_0_q_loc_vector", "V1010_SUMMARY"],
        "role": "prior q_loc derivation route and residual retention gate",
    },
    {
        "source_id": "SRC2581_02_GK_contract",
        "source_path": OUT / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
        "needles": ["GK513_0_action_existence", "GK513_3_double_zero", "GK513_5_boundary_no_flux"],
        "role": "first-variation/action/integrability contract",
    },
    {
        "source_id": "SRC2581_03_GK_tests",
        "source_path": OUT / "P8_GAMMA_KHAT_QLOC_GATE_TESTS.csv",
        "needles": ["G513_1_conditional_action_route", "G513_2_current_MTS_action", "G513_4_local_GR_claim"],
        "role": "current gate tests for q_loc derivation",
    },
    {
        "source_id": "SRC2581_04_GK_residual",
        "source_path": OUT / "P8_GAMMA_KHAT_QLOC_RESIDUAL_OR_DEMOTION.csv",
        "needles": ["QR513_0_nonvariational_stress", "QR513_2_double_zero_fails", "QR513_4_boundary_flux"],
        "role": "residual/demotion fallback rows",
    },
    {
        "source_id": "SRC2581_05_GK_validation",
        "source_path": OUT / "P8_GAMMA_KHAT_QLOC_VALIDATION.csv",
        "needles": ["V513_4_no_overclaim", "local_GR_claim_allowed=false"],
        "role": "prior validation that no overclaim is allowed",
    },
    {
        "source_id": "SRC2581_06_symbol_map",
        "source_path": OUT / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
        "needles": ["q_loc^nu", "Gamma_eff", "K_hat"],
        "role": "symbol map defining q_loc as derived residual not fundamental field",
    },
    {
        "source_id": "SRC2581_07_response_doublet",
        "source_path": OUT / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
        "needles": ["RD516_1_even_scalar_density", "RD516_2_metric_response", "RD516_4_zero_odd_source"],
        "role": "candidate response-doublet route to Gamma/Khat double-zero",
    },
    {
        "source_id": "SRC2581_08_2580_validation",
        "source_path": OUT / "P8_Y5_BRR545_2580_VALIDATION.csv",
        "needles": ["VAL2580_OVERALL", "PASS"],
        "role": "previous checkpoint validation",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {"timestamp_utc": now(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, **row}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as error:
        return False, 0, str(error)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": str(path),
                    "exists": path.exists(),
                    "missing_needles": ";".join(missing),
                    "source_pass": path.exists() and not missing,
                    "role": source["role"],
                }
            )
        )
    return rows


def proof_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GK2581_0_action_existence", "S_GK exists", "there is a local diffeomorphism-invariant scalar action S_GK[g,Phi] whose Hilbert stress is T_GK", "NOT_SUPPLIED_CURRENT_CORPUS", "without S_GK, Gamma/Khat/q_loc is bookkeeping not derived dynamics"),
        ("GK2581_1_metric_response", "K_hat equals metric response", "K_hat^{mu nu}=2/sqrt(-g) delta[sqrt(-g) Gamma_eff]/delta g_{mu nu} plus derivative/boundary terms", "NOT_MATCHED_TO_CURRENT_SYMBOLS", "without response match, q_loc is not a Ward/Euler residual"),
        ("GK2581_2_Helmholtz", "T_GK is variational", "delta(sqrt(-g)T_GK^{mu nu})/delta g_{alpha beta} satisfies Helmholtz symmetry up to boundary terms", "NOT_CHECKED_CURRENT_CLAIM", "without integrability, no action exists for the proposed stress"),
        ("GK2581_3_Euler_closure", "q_loc vanishes on shell", "nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A + boundary, so E_A=0 and boundary=0 imply q_loc^nu=0", "NOT_DERIVED", "without Euler closure, q_loc is a physical local force/source-exchange residual"),
        ("GK2581_4_double_zero", "local fixed point has zero amplitude and zero first variation", "T_GK(Phi0)=0 and partial_A T_GK(Phi0)=0", "NOT_MATCHED", "without double-zero, F1 survives in PPN/source-normalization hair"),
        ("GK2581_5_projector_owner", "P_loc is parent-owned", "P_loc=P_parent(Phi0), partial_A P_loc(Phi0)=0 and projection commutes with local readout limit", "OPEN", "without projector ownership, projected zero can hide force components"),
        ("GK2581_6_boundary_silence", "boundary/symplectic no-flux", "integral_boundary Delta(theta_GK,Q_GK,tau)=0 or fixed topological subtraction", "OPEN", "bulk zero can still leak through local mass/force boundary terms"),
        ("GK2581_7_verdict", "derive q_loc^nu=0 for current MTS", "all GK2581_0 through GK2581_6 pass with source/equation paths and parent signatures", "QLOC_ZERO_NOT_DERIVED_CURRENT_CORPUS", "q_loc must remain the official local residual interface"),
    ]
    return [
        stamp(
            {
                "gate_id": gate_id,
                "required_clause": clause,
                "mathematical_form": form,
                "current_status": status,
                "failure_if_missing": failure,
                "valid_for_claim": False,
            }
        )
        for gate_id, clause, form, status, failure in rows
    ]


def residual_interface_rows() -> list[dict[str, Any]]:
    rows = [
        ("QLOC2581_0_q_loc_vector", "q_loc^nu", "P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})", "retained_until_S_GK_metric_response_Helmholtz_Euler_double_zero_boundary_proved", "PPN_alpha_i_xi;source_normalization_R11;local_force;clock_orbital"),
        ("QLOC2581_1_Gamma_metric_response_gap", "Delta_K", "K_hat - K_metric[Gamma_eff]", "retained_symbolic_gap", "metric_response;PPN;source_mass"),
        ("QLOC2581_2_Helmholtz_gap", "H_GK", "antisymmetric second-variation obstruction for proposed T_GK", "retained_symbolic_gap", "action_existence;local_GR"),
        ("QLOC2581_3_Euler_source_gap", "J_GK", "source-current work in Gamma/Khat Euler identity", "retained_symbolic_gap", "PPN_preferred_frame;source_exchange"),
        ("QLOC2581_4_boundary_gap", "B_GK", "boundary/symplectic work from S_GK integrations by parts", "retained_symbolic_gap", "boundary_flux;R10;R11"),
        ("QLOC2581_5_projector_gap", "P_loc_commutator", "failure of P_loc to be parent-owned and commute with fixed-point/readout limit", "retained_symbolic_gap", "domain_projector;preferred_frame"),
        ("QLOC2581_TOTAL", "q_loc_residual_abs", "absolute no-cancellation envelope over q_loc, metric-response, Helmholtz, Euler, boundary and projector gaps", "MISSING_COMPONENT_INPUTS", "local_GR;PPN;R10;R11;WEP"),
    ]
    return [
        stamp(
            {
                "residual_id": residual_id,
                "symbol": symbol,
                "definition": definition,
                "status": status,
                "observable_link": observable,
                "units": "dimensionless_or_force_per_mass_or_declared_per_projection",
                "numeric_value": "MISSING_NUMERIC_VALUE",
                "source_path": "MISSING_SOURCE_PATH",
                "score_ready": False,
                "valid_for_claim": False,
            }
        )
        for residual_id, symbol, definition, status, observable in rows
    ]


def local_test_rows() -> list[dict[str, Any]]:
    rows = [
        ("TEST2581_0_PPN_alpha", "PPN preferred-frame/conservation vector", "project q_loc^nu into alpha_i, zeta_i, xi source terms", "MISSING_PROJECTION_COEFFICIENTS", "PPN"),
        ("TEST2581_1_R10", "short-range/local fifth-force residual", "map q_loc profile to alpha(lambda) or force-law residual rows", "MISSING_QLOC_PROFILE_AND_UNITS", "R10"),
        ("TEST2581_2_R11_source", "source-normalization residual", "map q_loc/Gamma/Khat gaps to R11 measured-source residuals", "MISSING_SOURCE_NORMALIZATION_MAP", "R11;Newton"),
        ("TEST2581_3_clock_orbital", "clock/orbital residual", "project local q_loc into clock drift or orbital anomalous acceleration terms", "MISSING_ARENA_PROJECTION", "clocks;orbital"),
        ("TEST2581_4_boundary", "boundary/source flux residual", "map B_GK and theta/Q gaps to linked-surface mass drift", "MISSING_BOUNDARY_FLUX_MAP", "Newton;R10;R11"),
    ]
    return [
        stamp(
            {
                "test_id": test_id,
                "arena": arena,
                "map_required": map_required,
                "current_status": status,
                "observable_link": observable,
                "valid_for_claim": False,
            }
        )
        for test_id, arena, map_required, status, observable in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2581_0_conditional_route", "conditional variational route for q_loc zero is explicit", "PASS_GUARDRAIL", "the exact theorem path is written", True),
        ("CG2581_1_action", "S_GK is supplied and parent-signed", "BLOCKED_NONCLAIM", "no accepted S_GK action source exists", False),
        ("CG2581_2_metric_Helmholtz", "metric response and Helmholtz conditions pass", "BLOCKED_NONCLAIM", "K_hat response and integrability are not checked/matched", False),
        ("CG2581_3_Euler_double_zero", "Euler closure and double-zero derive q_loc=0", "BLOCKED_NONCLAIM", "source-current, boundary and fixed-point certificates are missing", False),
        ("CG2581_4_residual_interface", "q_loc residual is retained explicitly", "PASS_GUARDRAIL", "q_loc is not hidden or zeroed by plateau axiom", True),
        ("CG2581_5_local_GR", "local-GR/Newton can be claimed from GK sector", "BLOCKED_NONCLAIM", "q_loc and source/PiM residuals remain live", False),
        ("CG2581_6_no_shortcuts", "plateau silence, bookkeeping stress or fitted cancellation can prove q_loc=0", "PASS_GUARDRAIL", "all shortcuts are refused", True),
    ]
    return [
        stamp(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_status": status,
                "reason": reason,
                "gate_pass": gate_pass,
                "claim_allowed": False,
            }
        )
        for gate_id, claim, status, reason, gate_pass in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2581_0_route",
            "decision": "QLOC_ZERO_ROUTE_PRECISE_BUT_UNSIGNED",
            "reason": "S_GK + metric response + Helmholtz + Euler closure + double-zero + projector + boundary would derive q_loc=0",
            "effect": "proof target is exact",
        },
        {
            "decision_id": "DEC2581_1_current",
            "decision": "QLOC_ZERO_NOT_DERIVED_CURRENT_CORPUS",
            "reason": "current sources do not supply parent-signed action, response, integrability, fixed-point and boundary certificates",
            "effect": "no local-GR claim",
        },
        {
            "decision_id": "DEC2581_2_residual",
            "decision": "QLOC_RESIDUAL_INTERFACE_LOCKED",
            "reason": "until the theorem closes, q_loc is the official local force/PPN/R10/R11 residual interface",
            "effect": "future tests can bind it without pretending it vanished",
        },
        {
            "decision_id": "DEC2581_3_next",
            "decision": "RESPONSE_DOUBLET_OR_QLOC_BOUND_SELECTED_NEXT",
            "reason": "response doublet is the most concrete candidate route to an even/double-zero Gamma sector; if it fails, populate finite q_loc test rows",
            "effect": "2582 should try the response-doublet certificates or build q_loc bound inputs",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2581_0_selected",
            "selection_status": "selected",
            "target_file": "2582-Y5-R2FR-response-doublet-GammaKhat-metric-response-or-q_loc-bound-fill.md",
            "target_script": "scripts/Y5_R2FR_response_doublet_GammaKhat_metric_response_or_q_loc_bound_fill_2582.py",
            "task": "test whether the response/memory doublet can provide Gamma_eff evenness, K_hat metric-response equality, positive operator, zero odd source, PPN lock and boundary no-flux; if not, populate source-backed q_loc residual bound rows",
            "acceptance_target": "response doublet parent-signs the GK route, or q_loc residual rows gain units/projections/source paths while remaining nonclaim",
            "guardrails": "no plateau axiom; no bookkeeping stress; no fitted cancellation; no local-GR claim; no GitHub; no formalization-workbench edits",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "proof_gate": OUTPUTS["proof_gate"],
        "residual_interface": OUTPUTS["residual_interface"],
        "local_test_map": OUTPUTS["local_test_map"],
        "next_target": OUTPUTS["next_target"],
    }
    rows: list[dict[str, Any]] = []
    for key, source in copy_map.items():
        target = COPY_TARGETS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            stamp(
                {
                    "copy_id": f"COPY2581_{key}",
                    "source_path": str(source),
                    "target_path": str(target),
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append(stamp({"check_id": check_id, "status": "PASS" if passed else "FAIL", "notes": notes, "detail": detail}))

    add("VAL2581_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and required needles are present")
    add(
        "VAL2581_01_q_loc_zero_blocked",
        any(row["gate_id"] == "GK2581_7_verdict" and row["current_status"] == "QLOC_ZERO_NOT_DERIVED_CURRENT_CORPUS" for row in data["proof_gate"]),
        "q_loc zero remains blocked",
    )
    add(
        "VAL2581_02_required_proof_clauses",
        len(data["proof_gate"]) >= 8 and all(row["valid_for_claim"] is False for row in data["proof_gate"]),
        "all GK proof clauses are explicit and nonclaim",
    )
    required_symbols = {"q_loc^nu", "Delta_K", "H_GK", "J_GK", "B_GK", "P_loc_commutator"}
    actual_symbols = {row["symbol"] for row in data["residual_interface"]}
    add(
        "VAL2581_03_residual_interface",
        required_symbols.issubset(actual_symbols) and all(row["score_ready"] is False and row["valid_for_claim"] is False for row in data["residual_interface"]),
        "q_loc residual interface is official and nonclaim",
    )
    add(
        "VAL2581_04_local_test_map",
        len(data["local_test_map"]) >= 5 and all(row["valid_for_claim"] is False for row in data["local_test_map"]),
        "local test maps are staged but not claim-ready",
    )
    add(
        "VAL2581_05_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"]),
        "no gate allows q_loc zero or local-GR claim",
    )
    add(
        "VAL2581_06_next_target_written",
        any(row["route_id"] == "NEXT2581_0_selected" for row in data["next"]),
        "2582 response-doublet/q_loc-bound target selected",
    )
    add(
        "VAL2581_07_branch_copies",
        all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]),
        "nonclaim branch copies exist",
    )

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2581*", "*P8_Y5_GAMMAKHAT_QLOC_2581*", "*JR2581*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2581_08_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2581 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2581_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2581_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2581_OVERALL",
        overall,
        "2581 keeps q_loc zero blocked, locks q_loc as the official local residual interface, and selects response-doublet or q_loc bound fill next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            values.append(value.replace("|", "\\|").replace("\n", " "))
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2581 Y5 R2FR GammaKhat q_loc Coupling Double-Zero Or Residual Lock",
        "",
        "**Status:** private nonclaim derivation checkpoint. `q_loc^nu -> 0` is not derived for current MTS.",
        "",
        "**Main result:** the exact derivation route is now locked: `S_GK` must exist, `K_hat` must be the metric response of `Gamma_eff`, Helmholtz integrability must pass, Euler/Ward closure must make the divergence on-shell zero, `T_GK(Phi0)=0`, `partial_A T_GK(Phi0)=0`, `P_loc` must be parent-owned, and boundary/symplectic flux must vanish. Current sources do not prove that package. Therefore `q_loc^nu` is retained as the official local residual interface for PPN/R10/R11/clock/orbital testing until the route is parent-signed.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Derivation Proof Gate",
        markdown_table(data["proof_gate"], ["gate_id", "required_clause", "mathematical_form", "current_status", "failure_if_missing", "valid_for_claim"]),
        "",
        "## Official Residual Interface",
        markdown_table(data["residual_interface"], ["residual_id", "symbol", "definition", "status", "observable_link", "units", "numeric_value", "source_path", "score_ready", "valid_for_claim"]),
        "",
        "## Local Test Map",
        markdown_table(data["local_test_map"], ["test_id", "arena", "map_required", "current_status", "observable_link", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    data = {
        "sources": source_register_rows(),
        "proof_gate": proof_gate_rows(),
        "residual_interface": residual_interface_rows(),
        "local_test_map": local_test_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["proof_gate"], data["proof_gate"])
    write_csv(OUTPUTS["residual_interface"], data["residual_interface"])
    write_csv(OUTPUTS["local_test_map"], data["local_test_map"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2581_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
