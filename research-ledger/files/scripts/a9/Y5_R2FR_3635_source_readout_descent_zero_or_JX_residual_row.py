from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3635"
BRANCH_ID = "MTS_R2FR_Y5_SOURCE_READOUT_DESCENT_ZERO_OR_JX_RESIDUAL_ROW_3635"
DOC = ROOT / "3635-Y5-R2FR-source-readout-descent-zero-or-JX-residual-row.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def out_paths() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3635_SOURCE_REGISTER.csv",
        "descent_theorem": RESIDUALS / "P8_Y5_R2FR_3635_SOURCE_READOUT_DESCENT_THEOREM.csv",
        "source_current_law": RESIDUALS / "P8_Y5_R2FR_3635_SOURCE_CURRENT_LAW.csv",
        "source_component_gate": RESIDUALS / "P8_Y5_R2FR_3635_SOURCE_READOUT_COMPONENT_GATE.csv",
        "jx_residual_row": RESIDUALS / "P8_Y5_R2FR_3635_JX_SOURCE_RESIDUAL_ROW.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3635_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3635_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3635_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_source_readout_coupling_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3635_VALIDATION.csv",
    }


def source_rows(t: str) -> list[dict[str, object]]:
    sources = [
        (
            "handoff_3634",
            RESIDUALS / "P8_Y5_R2FR_3634_NEXT_TARGET.csv",
            "partial_Z M_obs=0",
            "3634 handoff selecting source/readout descent as highest-pressure coupling target.",
        ),
        (
            "dqz_component_3634",
            RESIDUALS / "P8_Y5_R2FR_3634_DQZ_COMPONENT_EVALUATION.csv",
            "OPEN_HIGHEST_PRESSURE_COMPONENT",
            "source/readout component was identified as the main DqZ bottleneck.",
        ),
        (
            "filled_dqz_3634",
            RESIDUALS / "P8_Y5_R2FR_3634_FILLED_DQZ_ROW.csv",
            "partial_Z M_obs",
            "exact Dq_Z norm formula that this checkpoint refines.",
        ),
        (
            "coupling_law_3629",
            RESIDUALS / "P8_Y5_R2FR_3629_RESPONSE_DOUBLET_COUPLING_LAW.csv",
            "L_AB Z^B + J_A",
            "linearized source-current obstruction for response doublet.",
        ),
        (
            "jz_coefficients_3629",
            RESIDUALS / "P8_Y5_R2FR_3629_JZ_COEFFICIENT_ROWS.csv",
            "JZC3629_3_Newton_source",
            "source/Newton residual row already waiting for a J_Z source profile.",
        ),
        (
            "parent_action_3630",
            RESIDUALS / "P8_Y5_R2FR_3630_PARENT_ACTION_CLAUSE.csv",
            "PAC3630_4_source_normalization",
            "sufficient source-normalization descent clause from the parent action contract.",
        ),
        (
            "retained_dq_1667",
            RESIDUALS / "P8_Y5_PARENT_QLOC_1667_RETAINED_DQ_LEAK_ROWS.csv",
            "Dsource_readout_Dq_leak",
            "retained source/readout leakage row.",
        ),
        (
            "x_residual_669",
            RESIDUALS / "P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv",
            "RV669_2_J_X",
            "existing X-sector source current row to refine if descent fails.",
        ),
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "needle": needle,
            "needle_found": contains(path, needle),
            "role": role,
        }
        for source_id, path, needle, role in sources
    ]


def descent_theorem_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "theorem_id": "SDT3635_0_source_quotient_setup",
            "statement": "Let M_obs be the measured source/readout block: rest mass, GM calibration, Hamiltonian/source charge, and orbit/readout maps.",
            "identity": "M_obs = M_bar(q(Phi)) is the source-readout descent condition",
            "derivation": "For any fibre direction v_Z in ker(Dq), partial_Z M_obs = DM_bar[Dq(v_Z)] = 0.",
            "status": "CONDITIONAL_THEOREM",
            "blocks_if_missing": "if M_obs uses Z directly, the source current J_Z is physical or must be bounded",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SDT3635_1_source_action_zero",
            "statement": "If both geometry and source/readout descend through q, the source action has no linear Z current.",
            "identity": "delta_Z S_source = (delta S_source/delta G_obs) partial_Z G_obs + (delta S_source/delta M_obs) partial_Z M_obs = 0",
            "derivation": "3634 supplies the component split; source descent kills the M_obs term and geometry descent kills the G_obs term.",
            "status": "CONDITIONAL_THEOREM",
            "blocks_if_missing": "geometry-only descent is insufficient because the M_obs derivative can source Z",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SDT3635_2_point_particle_source",
            "statement": "For a compact source represented by a point-particle/readout action, the Z source has a clean split into geometry and mass-readout parts.",
            "identity": "delta_Z S_pp = -int c ds_obs partial_Z mu_obs - 1/2 int mu_obs u^mu u^nu partial_Z g_obs_mn d tau + readout/projector terms",
            "derivation": "If partial_Z g_obs=0, the leading source current is controlled by partial_Z mu_obs and readout/projector derivatives.",
            "status": "DERIVED_SOURCE_CURRENT_FORM",
            "blocks_if_missing": "source mass/readout derivative remains the live coupling row",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SDT3635_3_orbit_GM_calibration",
            "statement": "Newtonian/orbital observables see the combination GM_obs; hiding Z-dependence in measured GM is not a GR reduction.",
            "identity": "partial_Z(GM_obs)=G_obs partial_Z M_obs + M_obs partial_Z G_obs + calibration/projector terms",
            "derivation": "With geometry/G fixed, a nonzero partial_Z M_obs becomes a source-normalization residual feeding R1/R10/R11.",
            "status": "DERIVED_GM_READOUT_GUARD",
            "blocks_if_missing": "GM calibration can absorb a fifth-force-looking coupling unless reported as a residual",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SDT3635_4_verdict",
            "statement": "The source-readout theorem is exact, but the live corpus does not sign M_obs=M_bar(q(Phi)).",
            "identity": "partial_Z M_obs=0 is sufficient for source silence; not currently proven",
            "derivation": "This converts the coupling gap into a single branch: prove source descent or score J_X/J_Z.",
            "status": "THEOREM_SOUND_NOT_PARENT_SIGNED",
            "blocks_if_missing": "open J_X/source-charge residual row",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def source_current_law_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "law_id": "SCL3635_0_general_chain_rule",
            "quantity": "J_Z_source",
            "formula": "J_Z_source = Pi_M^*[(delta L_source/delta G_obs) partial_Z G_obs + (delta L_source/delta M_obs) partial_Z M_obs + (delta L_source/delta B_obs) partial_Z B_obs]",
            "meaning": "the source current is the chain-rule image of every Z-visible readout component",
            "zero_condition": "partial_Z G_obs=partial_Z M_obs=partial_Z B_obs=0",
            "status": "EXACT_CHAIN_RULE_FORM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "law_id": "SCL3635_1_geometry_zero_limit",
            "quantity": "J_Z_source|geometry_zero",
            "formula": "J_Z_source = Pi_M^*[(delta L_source/delta M_obs) partial_Z M_obs + projector/boundary terms]",
            "meaning": "even a perfect metric/coframe quotient leaves a source current if measured source mass/readout depends on Z",
            "zero_condition": "partial_Z M_obs=0 plus projector/boundary silence",
            "status": "COUPLING_BOTTLENECK_EXPOSED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "law_id": "SCL3635_2_positive_operator_profile",
            "quantity": "Z_profile_from_source",
            "formula": "Z^A(x)=-(L^{-1})^{AB}J_B_source + boundary Green terms + O(J^2)",
            "meaning": "if source descent fails, the local branch produces a residual profile that must be bounded, not waved away",
            "zero_condition": "J_B_source=0 and boundary source=0",
            "status": "PROFILE_ROUTE_FROM_3629_RETAINED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "law_id": "SCL3635_3_R10_R11_projection",
            "quantity": "alpha_or_operator_residual",
            "formula": "R_source ~ P_R[L^{-1} Pi_M^*((delta L_source/delta M_obs) partial_Z M_obs)]",
            "meaning": "this is the bridge from source-readout leakage to R1/R10/R11 residual rows",
            "zero_condition": "partial_Z M_obs=0 or projection P_R kills the source theoremically",
            "status": "EXECUTABLE_SYMBOLIC_BRIDGE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def source_component_gate_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "component_id": "SRC3635_0_rest_mass",
            "component": "partial_Z mu_obs",
            "required_zero": "measured rest/source mass is q-owned or fixed external label",
            "current_evidence": "3630 source-normalization clause is sufficient but not parent-signed",
            "status": "OPEN",
            "if_nonzero": "species/source charge row opens; WEP/source charge and R10/R11 affected",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "SRC3635_1_GM_calibration",
            "component": "partial_Z(GM_obs)",
            "required_zero": "Newtonian calibration uses only EH/source quotient variables or reports residual separately",
            "current_evidence": "3629 Newton/source row missing source mass and range profile",
            "status": "OPEN",
            "if_nonzero": "delta_Newton_MTS and alpha(lambda) rows become live",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "SRC3635_2_Hamiltonian_source",
            "component": "partial_Z H_source or Pi_M J_H",
            "required_zero": "Hamiltonian/source projector Pi_M is q-owned and orthogonal to extra charge",
            "current_evidence": "3630 PAC3630_4 calls this charge-current orthogonality not parent-derived",
            "status": "OPEN",
            "if_nonzero": "source normalization and hidden Hamiltonian charge drive J_X/J_Z",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "SRC3635_3_orbit_readout",
            "component": "partial_Z orbit/readout map",
            "required_zero": "orbit and ephemeris readouts are functions of observed metric/source quotient only",
            "current_evidence": "retained Dsource_readout_Dq_leak exists",
            "status": "OPEN",
            "if_nonzero": "orbital residuals and PPN/source projection rows must be scored",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "SRC3635_4_verdict",
            "component": "partial_Z M_obs",
            "required_zero": "all source/readout subcomponents vanish componentwise",
            "current_evidence": "no subcomponent zero is parent-signed",
            "status": "SOURCE_DESCENT_NOT_CLAIMED",
            "if_nonzero": "use J_X source residual row below",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def jx_residual_row(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": "JX3635_0_source_readout_residual",
            "prior_rows": "RV669_2_J_X;JZC3629_3_Newton_source;DQL1667_4_Dsource_readout",
            "symbol": "J_X_source_or_J_Z_source",
            "value_or_formula": "Pi_M^*[(delta L_source/delta M_obs) partial_X M_obs + (delta L_source/delta G_obs) partial_X G_obs + boundary/projector terms]",
            "geometry_zero_reduction": "Pi_M^*[(delta L_source/delta M_obs) partial_X M_obs + boundary/projector terms]",
            "units": "source action density per normalized X/Z field; must be fixed by parent field normalization",
            "feeds": "R1_WEP_source_charge;R10_fifth_force;R11_EH_operator_ledger;orbital_source_projection",
            "zero_condition": "M_obs=M_bar(q), G_obs=G_bar(q), and boundary/projector silence",
            "fill_level": "symbolic_executable_law_not_numeric",
            "score_status": "not_scoreable_until_field_normalization_projection_and_units",
            "source_paths": f"{RESIDUALS / 'P8_Y5_R2FR_3629_RESPONSE_DOUBLET_COUPLING_LAW.csv'};{RESIDUALS / 'P8_Y5_R2FR_3630_PARENT_ACTION_CLAUSE.csv'};{RESIDUALS / 'P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv'}",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def decision_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "DEC3635_0_theorem",
            "decision": "Source/readout descent is sufficient: M_obs=M_bar(q) implies partial_Z M_obs=0 and kills the source part of J_Z when geometry/boundary also descend.",
            "status": "CONDITIONAL_SOURCE_ZERO_THEOREM",
            "next_action": "try to parent-sign M_obs as quotient data rather than merely closure-label it",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3635_1_live_gap",
            "decision": "The live corpus does not sign source/readout descent; rest mass, GM calibration, Hamiltonian source, and orbit readout remain open componentwise.",
            "status": "SOURCE_DESCENT_NOT_CLAIMED",
            "next_action": "keep J_X/J_Z source residual row active",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3635_2_progress",
            "decision": "The coupling gap is now an explicit chain-rule current, not a vague missing coupling.",
            "status": "JX_SYMBOLIC_ROW_FILLED",
            "next_action": "next checkpoint should choose either parent-sign source mass as q-data or normalize the J_X row for scoring",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def status_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "SOURCE_READOUT_THEOREM_DERIVED_JX_SYMBOLIC_ROW_ACTIVE",
            "summary": "3635 derives the source/readout coupling law. If measured source data M_obs descends through q, then partial_Z M_obs=0 and the source part of J_Z dies. If not, the source current is exactly the chain-rule pullback of partial_Z M_obs into the source action, and the J_X/J_Z residual row is active. This turns the coupling worry into a concrete theorem-or-coefficient branch.",
            "claim_ceiling": "no source-zero, local-GR, R10/R11, WEP, Newton, or PPN claim is allowed from 3635",
            "useful_result": "coupling is now localized to M_obs=M_bar(q) versus J_X_source=Pi_M^*[(delta L_source/delta M_obs) partial_X M_obs + ...]",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3635_0",
            "target_doc": "3636-Y5-R2FR-source-mass-quotient-signature-or-JX-normalization.md",
            "target_script": "scripts/Y5_R2FR_3636_source_mass_quotient_signature_or_JX_normalization.py",
            "objective": "attempt to parent-sign measured source mass/GM/Hamiltonian readout as q-data; if that fails, define the field normalization and units needed to make J_X_source scoreable",
            "success_gate": "either M_obs=M_bar(q) is parent-signed for rest mass, GM, Hamiltonian source, and orbit readout, or J_X_source gains explicit normalization, units, and first comparator channel",
            "reason": "3635 derived the exact source-current law; the next unresolved fork is source-mass quotient signature versus scoring normalization.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def canonical_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_object": "source_readout_coupling_law",
            "canonical_status": "CONDITIONAL_SOURCE_ZERO_NOT_SIGNED_JX_ROW_ACTIVE",
            "usable_result": "partial_Z M_obs=0 follows if M_obs descends through q; otherwise J_X_source is the chain-rule source current Pi_M^*[(delta L_source/delta M_obs) partial_X M_obs + ...].",
            "hard_block": "parent-sign M_obs=M_bar(q) or normalize J_X_source for scoring",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def md(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(rows: list[dict[str, object]], cols: list[str]) -> str:
    output = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(col, "")) for col in cols) + " |")
    return "\n".join(output)


def write_doc(
    src: list[dict[str, object]],
    theorem: list[dict[str, object]],
    laws: list[dict[str, object]],
    gates: list[dict[str, object]],
    jx: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    nxt: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 3635 Y5 R2FR source-readout descent zero or JX residual row",
            f"**Status:** {status[0]['summary']}",
            f"**Claim ceiling:** {status[0]['claim_ceiling']}.",
            "## Main result",
            (
                "The coupling question now has a clean theorem-or-coefficient split:\n\n"
                "```text\n"
                "M_obs = M_bar(q(Phi))  =>  partial_Z M_obs = 0\n"
                "J_Z_source = Pi_M^*[(delta L_source/delta G_obs) partial_Z G_obs\n"
                "                     + (delta L_source/delta M_obs) partial_Z M_obs\n"
                "                     + boundary/projector terms].\n"
                "```\n\n"
                "So if the measured source block descends through `q`, source coupling dies. If it does not, the theory has a real `J_X/J_Z` residual current to normalize and test. This is the coupling fork, sharpened."
            ),
            "## Source register",
            table(src, ["source_id", "path", "exists", "needle_found", "role"]),
            "## Source-readout descent theorem",
            table(theorem, ["theorem_id", "statement", "identity", "derivation", "status", "blocks_if_missing"]),
            "## Source current law",
            table(laws, ["law_id", "quantity", "formula", "meaning", "zero_condition", "status"]),
            "## Source component gate",
            table(gates, ["component_id", "component", "required_zero", "current_evidence", "status", "if_nonzero"]),
            "## JX/JZ residual row",
            table(jx, ["row_id", "symbol", "value_or_formula", "geometry_zero_reduction", "units", "feeds", "zero_condition", "fill_level", "score_status"]),
            "## Decisions",
            table(decisions, ["decision_id", "decision", "status", "next_action"]),
            "## Next target",
            table(nxt, ["target_doc", "target_script", "objective", "success_gate"]),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def validate(outputs: dict[str, Path], src: list[dict[str, object]]) -> list[dict[str, object]]:
    t = now()
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": t,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    add("VAL3635_0_sources_exist", all(bool(row["exists"]) for row in src), "all cited source paths exist")
    add("VAL3635_1_needles_found", all(bool(row["needle_found"]) for row in src), "all source needles found")
    pre = {name: path for name, path in outputs.items() if name != "validation"}
    add("VAL3635_2_outputs_exist", all(path.exists() for path in pre.values()) and DOC.exists(), "all pre-validation outputs and doc written")

    details = []
    parse_ok = True
    for name, path in pre.items():
        try:
            count = len(read_csv(path))
            details.append(f"{name}:{count}")
            parse_ok = parse_ok and count > 0
        except Exception as exc:
            details.append(f"{name}:ERR:{exc}")
            parse_ok = False
    add("VAL3635_3_csv_parse", parse_ok, "; ".join(details))

    theorem = read_csv(outputs["descent_theorem"])
    laws = read_csv(outputs["source_current_law"])
    gates = read_csv(outputs["source_component_gate"])
    jx = read_csv(outputs["jx_residual_row"])
    decisions = read_csv(outputs["decision_gates"])
    status = read_csv(outputs["status"])
    nxt = read_csv(outputs["next_target"])

    add("VAL3635_4_descent_identity_present", any("M_obs = M_bar" in row["identity"] for row in theorem), "source quotient identity present")
    add("VAL3635_5_chain_rule_current_present", any("partial_Z M_obs" in row["formula"] and "delta L_source/delta M_obs" in row["formula"] for row in laws), "source current chain-rule law present")
    add("VAL3635_6_point_particle_split_present", any("delta_Z S_pp" in row["identity"] for row in theorem), "point-particle source split present")
    add("VAL3635_7_component_gate_complete", len(gates) == 5 and any(row["component"] == "partial_Z(GM_obs)" for row in gates), "source/readout subcomponents covered")
    add("VAL3635_8_jx_row_filled", bool(jx) and "delta L_source/delta M_obs" in jx[0]["value_or_formula"] and jx[0]["score_status"] == "not_scoreable_until_field_normalization_projection_and_units", "JX source residual row symbolically filled")
    add("VAL3635_9_decision_theorem_or_coefficient", any(row["status"] == "JX_SYMBOLIC_ROW_FILLED" for row in decisions), "decision table records theorem-or-coefficient fork")
    add("VAL3635_10_nonclaim_all_outputs", all(row["valid_for_claim"].lower() == "false" for row in theorem + laws + gates + jx + decisions + status + nxt), "all generated rows remain nonclaim")
    leaks = list(FORMALIZATION.rglob("*3635*")) if FORMALIZATION.exists() else []
    add("VAL3635_11_no_formalization_leak", not leaks, "no 3635 files in formalization-workbench")
    add("VAL3635_12_next_target_written", bool(nxt) and "3636" in nxt[0]["target_doc"], "3636 source mass/JX normalization target written")
    add("VAL3635_13_doc_written", DOC.exists() and "coupling fork" in DOC.read_text(encoding="utf-8", errors="replace"), "checkpoint doc written with coupling fork")
    add("VAL3635_14_canonical_status_written", outputs["canonical_status"].exists() and "CONDITIONAL_SOURCE_ZERO_NOT_SIGNED_JX_ROW_ACTIVE" in outputs["canonical_status"].read_text(encoding="utf-8", errors="replace"), "canonical source-readout status written")
    return rows


def main() -> None:
    t = now()
    outputs = out_paths()
    src = source_rows(t)
    theorem = descent_theorem_rows(t)
    laws = source_current_law_rows(t)
    gates = source_component_gate_rows(t)
    jx = jx_residual_row(t)
    decisions = decision_rows(t)
    status = status_rows(t)
    nxt = next_rows(t)
    canonical = canonical_rows(t)

    write_csv(outputs["source_register"], src)
    write_csv(outputs["descent_theorem"], theorem)
    write_csv(outputs["source_current_law"], laws)
    write_csv(outputs["source_component_gate"], gates)
    write_csv(outputs["jx_residual_row"], jx)
    write_csv(outputs["decision_gates"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next_target"], nxt)
    write_csv(outputs["canonical_status"], canonical)
    write_doc(src, theorem, laws, gates, jx, decisions, status, nxt)

    validation = validate(outputs, src)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3635 validation failed: {failures}")
    print(f"wrote 3635 checkpoint with {len(validation)} validation checks")


if __name__ == "__main__":
    main()
