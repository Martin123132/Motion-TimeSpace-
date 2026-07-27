from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3733"
BRANCH_ID = "MTS_R2FR_Y5_HX_AND_HODGE_VARIATION_ZERO_OR_BOUND_3733"
DOC = ROOT / "3733-Y5-R2FR-HX-and-Hodge-variation-zero-or-bound.md"

DOC_3732 = ROOT / "3732-Y5-R2FR-first-arena-response-specialization-Newton-PPN-and-EM.md"
NEXT_3732 = RESIDUALS / "P8_Y5_R2FR_3732_NEXT_TARGET.csv"
VALIDATION_3732 = RESIDUALS / "P8_Y5_BRR545_3732_VALIDATION.csv"
SIGMA_3732 = RESIDUALS / "P8_Y5_R2FR_3732_SIGMA_SPECIALIZATION_ROWS.csv"
DOC_1029 = ROOT / "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md"
DOC_1030 = ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md"
DOC_1031 = ROOT / "1031-Y5-R10-quotient-naturality-terminal-public-metric-proof-or-spm-closure.md"
HEURISTIC_00 = ROOT / "00-martin-fork-heuristics-private.md"
CFC943 = RESIDUALS / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv"
CG_PROVENANCE_1030 = RESIDUALS / "P8_Y5_R10_1030_CG_PROVENANCE_GATE_BINDING.csv"
SPM_1031 = RESIDUALS / "P8_Y5_R10_1031_SPM_CLOSURE_BRANCH.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3732", DOC_3732, "partial_X chi", "3732 identifies H^X and Hodge variation as bottleneck"),
        ("next_3732", NEXT_3732, "3733-Y5-R2FR-HX-and-Hodge-variation-zero-or-bound.md", "3732 handoff"),
        ("validation_3732", VALIDATION_3732, "next_target_3733", "3732 validation"),
        ("sigma_3732", SIGMA_3732, "sigma_EM", "3732 sigma specializations"),
        ("doc_1029", DOC_1029, "no-shadow-frame theorem", "conditional c_g/no-shadow theorem"),
        ("doc_1030", DOC_1030, "single-public-metric parent action", "SPM parent action route and countermodels"),
        ("doc_1031", DOC_1031, "Single Public Metric closure", "SPM closure demotion and finite fallback"),
        ("cfc943", CFC943, "no_shadow_frame_rule", "coframe/no-shadow coupling contract"),
        ("cg_provenance_1030", CG_PROVENANCE_1030, "c_g;b_A;b_alpha;b_dis", "finite coefficient provenance and no-cancellation"),
        ("spm_1031", SPM_1031, "AVAILABLE_AS_CLOSURE_ONLY", "SPM closure branch status"),
        ("heuristic_00", HEURISTIC_00, "Poynting", "EM/Poynting heuristic retained as search direction"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append({
            **base(ts),
            "source_id": source_id,
            "path": str(path),
            "exists": exists,
            "needle": needle,
            "needle_found": needle in text,
            "role": role,
        })
    return rows


def hx_zero_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "HXZ3733_0_definition",
            "H^X_{mu nu}:=partial_X g^matter_{mu nu}|branch = Lie_vX g^matter_{mu nu}",
            "Defines the frame/metric variation that feeds matter trace coupling, PPN/Newton, clocks, and EM stress.",
            "DEFINITION_SHARP",
            "none at definition level",
        ),
        (
            "HXZ3733_1_chain_rule_zero",
            "If g_matter(Phi)=g_pub(q(Phi)) and Dq[v_X]=0, then H^X=Dg_pub[Dq[v_X]]=0.",
            "This is the clean quotient/no-shadow zero theorem for the matter metric derivative.",
            "CONDITIONAL_THEOREM_VALID",
            "parent-signed q-kernel and matter-frame factorization",
        ),
        (
            "HXZ3733_2_shadow_counterbranch",
            "If g_matter=A_g(X)^2 g_pub+B_g(X)U_mu U_nu, then H^X=2 c_g g_pub + b_dis U_mu U_nu + extra terms.",
            "A universal frame coupling is legal unless the parent action excludes it.",
            "FINITE_BRANCH_REQUIRED_IF_NOT_EXCLUDED",
            "c_g,b_dis,extra-frame coefficient rows or no-shadow theorem",
        ),
        (
            "HXZ3733_3_spm_closure",
            "Under explicit SPM closure, independent A_g and B_g slots are excluded, so H^X=0 inside that closure branch only.",
            "This is useful as a model branch but not a derived MTS theorem.",
            "CLOSURE_ONLY_NONCLAIM",
            "parent proof if promoted beyond closure",
        ),
        (
            "HXZ3733_4_verdict",
            "H^X=0 is not claimable in the current parent corpus; the zero theorem is conditional and the finite branch must be retained.",
            "Prevents local GR/Newton/EM recovery from being smuggled through an assumed matter-frame lock.",
            "ZERO_NOT_PARENT_SIGNED",
            "SPM/no-shadow parent action or finite H^X bound pack",
        ),
    ]
    return [
        {
            **base(ts),
            "audit_id": audit_id,
            "clause": clause,
            "meaning": meaning,
            "status": status,
            "missing_for_claim": missing,
            "claim_allowed": False,
        }
        for audit_id, clause, meaning, status, missing in rows
    ]


def hodge_zero_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "CHIZ3733_0_definition",
            "partial_X chi^{mu nu rho sigma}:=Lie_vX chi^{mu nu rho sigma}",
            "Defines the constitutive/Hodge variation that feeds Maxwell stress, waves, Poynting balance, polarization, and charge readout.",
            "DEFINITION_SHARP",
            "none at definition level",
        ),
        (
            "CHIZ3733_1_metric_hodge_chain",
            "If chi=chi_vac[g_matter,theta_EM] then partial_X chi=(delta chi/delta g_matter)[H^X]+(partial chi/partial theta_EM)partial_X theta_EM.",
            "The Hodge route is linked to H^X but also has independent EM constants/material markers.",
            "DERIVED_CHAIN_RULE",
            "H^X, theta_EM quotient ownership, and vacuum/material constitutive law",
        ),
        (
            "CHIZ3733_2_vacuum_zero",
            "If H^X=0, theta_EM=theta_EM(q), and there is no hidden medium/background constitutive slot, then partial_X chi=0.",
            "This is the clean Maxwell/EM stress zero theorem target.",
            "CONDITIONAL_THEOREM_VALID",
            "H^X zero, no-marker EM constants, and no hidden constitutive medium",
        ),
        (
            "CHIZ3733_3_hidden_medium_counterbranch",
            "If chi=chi_vac[g]+chi_hidden(X,flow,material), then partial_X chi can be nonzero even when H^X=0.",
            "A background-flow/Hodge branch is possible but must be bounded as physics, not assumed away.",
            "FINITE_BRANCH_REQUIRED_IF_NOT_EXCLUDED",
            "partial_X chi_hidden or parent Hodge/constitutive rule",
        ),
        (
            "CHIZ3733_4_verdict",
            "partial_X chi=0 is not claimable in the current parent corpus; retain a finite constitutive/Hodge coefficient.",
            "Keeps EM/Poynting alive while blocking an unearned Maxwell recovery claim.",
            "ZERO_NOT_PARENT_SIGNED",
            "parent Hodge rule or finite partial_X chi bound pack",
        ),
    ]
    return [
        {
            **base(ts),
            "audit_id": audit_id,
            "clause": clause,
            "meaning": meaning,
            "status": status,
            "missing_for_claim": missing,
            "claim_allowed": False,
        }
        for audit_id, clause, meaning, status, missing in rows
    ]


def finite_bound_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "FIN3733_0_HX_norm",
            "Hbar_X",
            "||H^X||_A <= 2|c_g| C_g,A + |b_dis| C_dis,A + ||H_extra||_A",
            "dimensionless metric-response norm",
            "Newton_PPN;clock;EM_Poynting;source_coupling",
            "MISSING_CG_BDIS_EXTRA_BOUNDS",
        ),
        (
            "FIN3733_1_trace_source",
            "J_geom_bound",
            "||J_geom||_A <= 1/2 ||T||_A ||H^X||_A",
            "source-current norm",
            "Newton_PPN;R10;clock;orbital",
            "MISSING_STRESS_NORM_AND_HX_BOUND",
        ),
        (
            "FIN3733_2_chi_metric_part",
            "Chibar_metric",
            "||partial_X chi_metric||_A <= C_chi_g,A ||H^X||_A",
            "constitutive-response norm",
            "EM_Poynting;Maxwell_stress;wave",
            "MISSING_CHI_G_DERIVATIVE_AND_HX_BOUND",
        ),
        (
            "FIN3733_3_chi_marker_part",
            "Chibar_marker",
            "||partial_X chi_marker||_A <= C_chi_theta,A |b_alpha| + sum_I C_chi_I,A |b_I|",
            "constitutive-response norm",
            "EM_Poynting;charge;fine_structure;clock",
            "MISSING_EM_MARKER_BOUNDS",
        ),
        (
            "FIN3733_4_chi_hidden_part",
            "Chibar_hidden",
            "||partial_X chi_hidden||_A <= C_flow,A |b_flow| + ||tail_chi||_A",
            "constitutive-response norm",
            "EM_Poynting;background_flow",
            "MISSING_HIDDEN_HODGE_FLOW_BOUND",
        ),
        (
            "FIN3733_5_total_abs_guard",
            "HX_chi_total_abs",
            "total <= Hbar_X + Chibar_metric + Chibar_marker + Chibar_hidden + retained_tails, with no cancellation between unknowns",
            "absolute envelope",
            "all local arenas",
            "MISSING_ALL_COMPONENT_SOURCE_ROWS",
        ),
    ]
    return [
        {
            **base(ts),
            "bound_id": bound_id,
            "quantity": quantity,
            "bound_formula": formula,
            "units": units,
            "observable_links": links,
            "current_status": "BOUND_SCHEMA_READY_VALUES_MISSING",
            "missing_for_claim": missing,
            "source_owned": False,
            "claim_allowed": False,
        }
        for bound_id, quantity, formula, units, links, missing in rows
    ]


def arena_feed_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "FEED3733_0_Newton_PPN",
            "Newton_PPN_bridge",
            "sigma_NP <= C_trace Hbar_X ||T|| + C_dis|b_dis|||T_UU|| + |Delta_GM| + |boundary_NP| + |tail_NP|",
            "Hbar_X,c_g,b_dis,T,T_UU,Delta_GM,boundary_NP,tail_NP",
            "feeds SIG3732_NP and 3729 sigma_A",
        ),
        (
            "FEED3733_1_EM_Poynting",
            "EM_Poynting_bridge",
            "sigma_EM <= C_chi Chibar_total ||F^2|| + C_frame Hbar_X ||T_EM|| + C_J||delta_X J_EM|| + |b_alpha C_alpha| + |tail_EM|",
            "Chibar_total,Hbar_X,F^2,T_EM,delta_X_J_EM,b_alpha,tail_EM",
            "feeds SIG3732_EM and 3729 sigma_A",
        ),
        (
            "FEED3733_2_clock",
            "clock_redshift",
            "sigma_clock <= C_clock_frame Hbar_X + C_clock_alpha Chibar_marker + marker tails",
            "Hbar_X,Chibar_marker,clock sensitivities",
            "feeds clock sigma_A and no-marker gates",
        ),
        (
            "FEED3733_3_R10_source",
            "R10_short_range",
            "beta_source/test products retain Hbar_X through c_g and tails; do not linearize source-test exchange by accident",
            "c_g,tau_R10,K_X,Qbar_XH,tail envelope",
            "keeps R10 product-law guard active",
        ),
    ]
    return [
        {
            **base(ts),
            "feed_id": feed_id,
            "arena": arena,
            "feed_formula": formula,
            "missing_inputs": missing,
            "target": target,
            "ready_for_3729": False,
            "claim_allowed": False,
        }
        for feed_id, arena, formula, missing, target in rows
    ]


def runner_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "runner_id": "RUN3733_0_HX_CHI_ZERO_OR_BOUND",
        "HX_zero_theorem_conditional": True,
        "HX_zero_parent_signed": False,
        "chi_zero_theorem_conditional": True,
        "chi_zero_parent_signed": False,
        "finite_bound_schema_ready": True,
        "finite_values_source_owned": False,
        "status": "ZERO_THEOREMS_CONDITIONAL_BOUND_SCHEMA_READY_VALUES_MISSING",
        "feeds_3732": "Hbar_X and Chibar_total can feed Newton_PPN_bridge and EM_Poynting_bridge once sourced or theorem-zero",
        "claim_allowed": False,
    }]


def theorem_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "THM3733_0_HX_chain_rule",
            "g_matter=g_pub(q(Phi)) and Dq[v_X]=0 imply H^X=0.",
            "This is the exact no-shadow matter metric theorem target.",
            "CONDITIONAL_THEOREM",
        ),
        (
            "THM3733_1_HX_finite_branch",
            "If a Weyl/disformal matter frame is retained, H^X=2 c_g g+b_dis U U+H_extra and must be bounded componentwise.",
            "This is the finite route for local GR/Newton if zero cannot be derived.",
            "FINITE_BOUND_CONTRACT",
        ),
        (
            "THM3733_2_chi_chain_rule",
            "chi=chi[g_matter,theta_EM,hidden] gives partial_X chi=(delta chi/delta g)[H^X]+(partial chi/partial theta)partial_X theta + partial_X chi_hidden.",
            "This is the exact Hodge/constitutive route for Maxwell/EM stress.",
            "DERIVED_CHAIN_RULE",
        ),
        (
            "THM3733_3_chi_zero_conditions",
            "H^X=0, quotient-owned EM constants, and no hidden constitutive slot imply partial_X chi=0.",
            "This is the clean Maxwell/Poynting zero theorem target.",
            "CONDITIONAL_THEOREM",
        ),
        (
            "THM3733_4_no_cancellation",
            "Unknown H^X, marker, hidden-Hodge, and tail terms obey a no cancellation rule: combine them by absolute envelope, not signed cancellation.",
            "Keeps the bound route honest across Newton/PPN/EM.",
            "ANTI_OVERCLAIM",
        ),
    ]
    return [
        {
            **base(ts),
            "theorem_id": theorem_id,
            "clause": clause,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for theorem_id, clause, meaning, status in rows
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    gates = [
        ("CG3733_0_HX_conditional", "PASS_NONCLAIM", "H^X chain-rule zero theorem written"),
        ("CG3733_1_chi_conditional", "PASS_NONCLAIM", "partial_X chi chain-rule zero theorem written"),
        ("CG3733_2_HX_parent", "BLOCKED", "q-kernel and no-shadow matter metric not parent-signed"),
        ("CG3733_3_chi_parent", "BLOCKED", "Hodge/constitutive vacuum rule, EM constants, and hidden medium silence not parent-signed"),
        ("CG3733_4_finite_values", "BLOCKED", "finite Hbar_X and Chibar rows have no numeric/source-owned values"),
        ("CG3733_5_3732_feed", "BLOCKED", "Newton/PPN and EM/Poynting sigma rows remain unscoreable"),
        ("CG3733_6_claim", "BLOCKED", "no local GR/Newton/Maxwell/EM claim allowed"),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "gate_status": status,
            "required_before_claim": required,
            "claim_allowed": False,
        }
        for gate_id, status, required in gates
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "DEC3733_0_zero_attempt",
            "ZERO_ROUTE_IS_CLEAN_BUT_NOT_PARENT_SIGNED",
            "H^X and partial_X chi both have exact chain-rule zero theorems, but current corpus lacks the parent signatures.",
        ),
        (
            "DEC3733_1_bound_route",
            "FINITE_BOUND_ROUTE_IS_NOW_COMPONENTIZED",
            "The finite route is no longer vague: Hbar_X, J_geom_bound, Chibar_metric, Chibar_marker, and Chibar_hidden are separate no-cancellation inputs.",
        ),
        (
            "DEC3733_2_EM_status",
            "EM_POYNTING_ROUTE_SURVIVES_AS_HODGE_VARIATION",
            "Poynting/background-flow intuition is preserved as partial_X chi_hidden or a parent Hodge rule, not used as a claim.",
        ),
        (
            "DEC3733_3_next",
            "NEXT_BUILD_HX_CHI_TO_3732_INTERFACE",
            "The next useful move is to make Hbar_X/Chibar_total rows mechanically feed the 3732 Newton/PPN and EM response entries.",
        ),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale in rows
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "status_id": "STATUS3733_0",
        "status": "HX_CHI_ZERO_CONDITIONAL_FINITE_BOUND_SCHEMA_READY",
        "summary": "3733 derives the conditional zero theorems for H^X and partial_X chi, rejects current promotion, and stages finite no-cancellation bound rows feeding Newton/PPN and EM/Poynting.",
        "claim_allowed": False,
    }]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "next_id": "NEXT3733_0",
        "target_doc": "3734-Y5-R2FR-HX-chi-bound-interface-to-Newton-PPN-EM.md",
        "target_script": "scripts/Y5_R2FR_3734_HX_chi_bound_interface_to_Newton_PPN_EM.py",
        "objective": "connect Hbar_X and Chibar_total bound rows to the 3732 Newton/PPN and EM/Poynting response entries so future numeric/theorem-zero values can drive 3729",
        "success_gate": "the interface emits fillable sigma_NP and sigma_EM input rows with exact dependency columns and claim-blocked runner status",
        "claim_allowed": False,
    }]


def validation_rows(ts: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    csv_paths = [path for key, path in paths.items() if key not in {"doc", "validation"}]
    generated = [path for key, path in paths.items() if key != "validation"]
    formal_files = list(FORMALIZATION.rglob("*3733*")) if FORMALIZATION.exists() else []
    formal_files = [path for path in formal_files if path.is_file()]
    hx_text = read_text(paths["hx_zero"])
    chi_text = read_text(paths["chi_zero"])
    finite = parse_csv(paths["finite_bounds"])
    feed = parse_csv(paths["arena_feeds"])
    runner = parse_csv(paths["runner"])[0]
    doc_text = read_text(paths["doc"])
    checks = [
        ("sources_exist", "sources exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "outputs exist", all(path.exists() for path in generated)),
        ("csv_parse", "CSVs parse", all(len(parse_csv(path)) > 0 for path in csv_paths if path.exists())),
        ("HX_zero_audit", "H^X zero audit present", all(token in hx_text for token in ["H^X", "Dq[v_X]=0", "ZERO_NOT_PARENT_SIGNED"])),
        ("chi_zero_audit", "partial_X chi audit present", all(token in chi_text for token in ["partial_X chi", "chi_hidden", "ZERO_NOT_PARENT_SIGNED"])),
        ("finite_bounds", "finite bound rows present", len(finite) == 6),
        ("no_cancellation", "absolute no-cancellation guard present", any(row["quantity"] == "HX_chi_total_abs" for row in finite)),
        ("arena_feeds", "Newton/PPN and EM feed rows present", all(any(row["arena"] == arena for row in feed) for arena in ["Newton_PPN_bridge", "EM_Poynting_bridge"])),
        ("runner_blocks", "runner blocks claims", runner["status"] == "ZERO_THEOREMS_CONDITIONAL_BOUND_SCHEMA_READY_VALUES_MISSING" and runner["claim_allowed"] == "False"),
        ("theorems", "theorem rows include H^X and Hodge chain rules", all(token in read_text(paths["theorems"]) for token in ["H^X=0", "partial_X chi", "no cancellation"])),
        ("claim_gates_blocked", "claim gates block promotion", all(row["claim_allowed"] == "False" for row in parse_csv(paths["claim_gates"]))),
        ("next_target_3734", "next target is 3734 bound interface", all(token in read_text(paths["next_target"]) for token in ["3734", "Hbar_X", "Chibar_total"])),
        ("doc_core_terms", "doc contains H^X and Hodge status", all(token in doc_text for token in ["H^X", "partial_X chi", "Chibar", "Newton_PPN_bridge", "EM_Poynting_bridge"])),
        ("no_formalization_leak", "no 3733 files in formalization-workbench", len(formal_files) == 0),
    ]
    return [
        {
            **base(ts),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "",
        }
        for validation_id, description, result in checks
    ]


def write_doc(paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> None:
    lines = [
        "# 3733 - H^X and Hodge Variation: Zero or Bound",
        "",
        "## Status",
        "- `HX_CHI_ZERO_CONDITIONAL_FINITE_BOUND_SCHEMA_READY`",
        "- `H^X=partial_X g_matter` has a clean chain-rule zero theorem if the matter metric descends through `q` and the vertical direction is in `ker(Dq)`.",
        "- `partial_X chi` has a clean Hodge/constitutive zero theorem if `H^X=0`, EM constants descend through `q`, and no hidden constitutive/background-flow slot remains.",
        "- Neither zero theorem is parent-signed in the current corpus, so the finite no-cancellation bound route stays active.",
        "",
        "## H^X Zero Audit",
    ]
    for row in grouped["hx_zero"]:
        lines.append(f"- `{row['audit_id']}` `{row['status']}`: {row['clause']} | missing: {row['missing_for_claim']}")
    lines.extend(["", "## Hodge/chi Zero Audit"])
    for row in grouped["chi_zero"]:
        lines.append(f"- `{row['audit_id']}` `{row['status']}`: {row['clause']} | missing: {row['missing_for_claim']}")
    lines.extend(["", "## Finite Bound Rows"])
    for row in grouped["finite_bounds"]:
        lines.append(f"- `{row['bound_id']}` `{row['quantity']}`: {row['bound_formula']} | links: {row['observable_links']}")
    lines.extend(["", "## Arena Feeds"])
    for row in grouped["arena_feeds"]:
        lines.append(f"- `{row['feed_id']}` `{row['arena']}`: {row['feed_formula']} | missing: {row['missing_inputs']}")
    lines.extend(["", "## Theorem Rows"])
    for row in grouped["theorems"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['clause']} | {row['meaning']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}` | {row['rationale']}")
    lines.extend(["", "## Next Target"])
    lines.append("- `3734-Y5-R2FR-HX-chi-bound-interface-to-Newton-PPN-EM.md`")
    lines.append("- Objective: connect `Hbar_X` and `Chibar_total` to the 3732 Newton/PPN and EM/Poynting response entries so future numeric or theorem-zero rows can drive 3729.")
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ts = stamp()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3733_SOURCE_REGISTER.csv",
        "hx_zero": RESIDUALS / "P8_Y5_R2FR_3733_HX_ZERO_AUDIT.csv",
        "chi_zero": RESIDUALS / "P8_Y5_R2FR_3733_CHI_ZERO_AUDIT.csv",
        "finite_bounds": RESIDUALS / "P8_Y5_R2FR_3733_FINITE_BOUND_ROWS.csv",
        "arena_feeds": RESIDUALS / "P8_Y5_R2FR_3733_ARENA_FEED_ROWS.csv",
        "runner": RESIDUALS / "P8_Y5_R2FR_3733_RUNNER_STATUS.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3733_THEOREM_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3733_CLAIM_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3733_DECISION_ROWS.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3733_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3733_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3733_VALIDATION.csv",
        "doc": DOC,
    }
    grouped = {
        "source_register": source_register(ts),
        "hx_zero": hx_zero_rows(ts),
        "chi_zero": hodge_zero_rows(ts),
        "finite_bounds": finite_bound_rows(ts),
        "arena_feeds": arena_feed_rows(ts),
        "runner": runner_rows(ts),
        "theorems": theorem_rows(ts),
        "claim_gates": claim_gate_rows(ts),
        "decisions": decision_rows(ts),
        "status": status_rows(ts),
        "next_target": next_target_rows(ts),
    }
    for key, rows in grouped.items():
        write_csv(paths[key], rows)
    write_doc(paths, grouped)
    write_csv(paths["validation"], validation_rows(ts, paths))
    failures = [row for row in parse_csv(paths["validation"]) if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3733 validation failed: {failures}")
    print("wrote 3733 checkpoint: H^X and partial_X chi zero theorems conditional, finite bound schema ready")


if __name__ == "__main__":
    main()
