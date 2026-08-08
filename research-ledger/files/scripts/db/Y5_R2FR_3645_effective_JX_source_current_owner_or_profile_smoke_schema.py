from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3645"
BRANCH_ID = "MTS_R2FR_Y5_EFFECTIVE_JX_SOURCE_CURRENT_OWNER_OR_PROFILE_SMOKE_SCHEMA_3645"
DOC = ROOT / "3645-Y5-R2FR-effective-JX-source-current-owner-or-profile-smoke-schema.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3645_SOURCE_REGISTER.csv",
        "jx_variation": RESIDUALS / "P8_Y5_R2FR_3645_JX_VARIATION_DERIVATION.csv",
        "component_audit": RESIDUALS / "P8_Y5_R2FR_3645_JX_COMPONENT_OWNER_AUDIT.csv",
        "input_schema": RESIDUALS / "P8_Y5_R2FR_3645_SOURCE_CURRENT_INPUT_SCHEMA.csv",
        "green_map": RESIDUALS / "P8_Y5_R2FR_3645_GREEN_AMPLITUDE_MAP.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3645_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3645_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3645_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3645_VALIDATION.csv",
    }


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("next_3644", RESIDUALS / "P8_Y5_R2FR_3644_NEXT_TARGET.csv", "J_X^eff", "3644 handoff to effective source-current owner"),
        ("owner_3644", RESIDUALS / "P8_Y5_R2FR_3644_PROFILE_SOURCE_OWNER_AUDIT.csv", "MISSING_SOURCE_CURRENT_OWNER", "3644 source owner audit"),
        ("amp_3644", RESIDUALS / "P8_Y5_R2FR_3644_AMPLITUDE_PRIOR_ROWS.csv", "|A_X| <=", "3644 absolute amplitude envelope"),
        ("schema_3644", RESIDUALS / "P8_Y5_R2FR_3644_PROFILE_RUNNER_SCHEMA.csv", "source_paths", "3644 profile runner refusal schema"),
        ("second_variation_1025", RESIDUALS / "P8_Y5_R10_1025_SECOND_VARIATION_DERIVATION.csv", "O_X=-nabla_i", "1025 local operator and range template"),
        ("scalar_inputs_1024", ROOT / "1024-Y5-R10-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md", "ALPHA1024_1_source_current", "1024 source-current no-hair gate"),
        ("beta_split_1036", RESIDUALS / "P8_Y5_R10_1036_BETA_SOURCE_TEST_DERIVATION.csv", "beta_i :=", "1036 point-particle beta/source variation"),
        ("parent_x_audit_1036", RESIDUALS / "P8_Y5_R10_1036_PARENT_X_ACTION_AUDIT.csv", "J_X = -delta_X S_matter", "1036 parent X action audit"),
        ("current_contract_1009", ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md", "PCS1009_6_mass_projector_PiM", "1009 parent current-chain/source-measure contract"),
        ("profile_3643", RESIDUALS / "P8_Y5_R2FR_3643_XN_AMPLITUDE_RANGE_PROFILE_ROWS.csv", "A_X=A_src", "3643 exterior profile amplitude split"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "source_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
            }
        )
    return rows


def jx_variation_rows(ts: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }
    return [
        {
            **base,
            "derivation_id": "JXD3645_0_operator_convention",
            "claim": "Use the 1025 local block with D_X=Z_X in the chosen X_N normalization.",
            "formula": "S_X=int_A sqrt(h)[1/2 D_X h^ij partial_i X_N partial_j X_N + 1/2 M_X^2 X_N^2 - J_X^eff X_N] + B_X",
            "result": "O_X X_N = J_X^eff with O_X=-nabla_i(D_X nabla^i)+M_X^2 after boundary terms are fixed.",
            "status": "CONDITIONAL_VARIATION_IDENTITY",
            "missing_for_claim": "same-branch parent action, D_X, M_X^2, field units, and boundary convention",
        },
        {
            **base,
            "derivation_id": "JXD3645_1_effective_current_definition",
            "claim": "All non-operator dependence on X_N is an effective source current.",
            "formula": "J_X^eff := -(1/sqrt(h)) delta(S_matter+S_hidden+S_domain+S_projector+S_shell)/delta X_N",
            "result": "J_X^eff=J_X^matter+J_X^hidden_domain+J_X^projector+J_X^shell, while boundary and topology enter A_bdy/A_top unless represented as distributions.",
            "status": "EXACT_DEFINITION_AFTER_SIGN_CONVENTION",
            "missing_for_claim": "parent-owned sector actions and source-normalized X_N",
        },
        {
            **base,
            "derivation_id": "JXD3645_2_matter_metric_variation",
            "claim": "Matter coupling is the main fork: quotient descent makes it zero; any X-sensitive mass/readout makes it testable.",
            "formula": "J_X^matter=-(1/(2 sqrt(h))) sqrt(-g_obs) T_obs^ab partial_X g^obs_ab - sum_A (1/sqrt(h)) (partial L_matter/partial c_A) partial_X c_A",
            "result": "Point-particle limit agrees with 1036: J_X^matter contains sum_i beta_i m_i delta^3(x-x_i), beta_i=partial_Xhat ln m_i^eff.",
            "status": "DERIVED_CONDITIONALLY_FROM_STANDARD_VARIATION",
            "missing_for_claim": "parent-owned observed metric/readout, constants, mass functional, and Xhat normalization",
        },
        {
            **base,
            "derivation_id": "JXD3645_3_quotient_zero_gate",
            "claim": "The cleanest local-GR route is not fitting beta small; it is proving matter descends through q.",
            "formula": "If S_matter=Sbar[q(Phi),Psi,theta], v_X in ker(Dq), and Lie_vX theta=0, then delta_vX S_matter=0.",
            "result": "Under all descent/no-marker/no-shadow clauses, J_X^matter=0, beta_s=beta_t=0, and the matter part of A_src vanishes.",
            "status": "THEOREM_ROUTE_EXACT_PREMISES_UNSIGNED",
            "missing_for_claim": "q-kernel certificate, matter functor, no-marker constants, no-shadow readout, and hidden-tail silence",
        },
        {
            **base,
            "derivation_id": "JXD3645_4_hidden_domain_current",
            "claim": "Hidden/domain currents are not optional; they are the stress/current paid by selectors and memory/domain projectors.",
            "formula": "J_X^hidden_domain:=-(1/sqrt(h)) delta(S_hidden+S_domain)/delta X_N",
            "result": "This component is zero only if the parent sector is X-blind, double-zero, or orthogonal to the local projection.",
            "status": "SOURCE_COMPONENT_DEFINED_OWNER_UNSIGNED",
            "missing_for_claim": "domain selector action, memory/hidden field map, stress accounting, and local projection silence",
        },
        {
            **base,
            "derivation_id": "JXD3645_5_projector_current",
            "claim": "Projector/readout variation can fake a source even when bulk equations look source-free.",
            "formula": "J_X^projector:=-(1/sqrt(h)) delta S_projector[Pi_M,P_loc,readout]/delta X_N",
            "result": "Projector current is zero only after Pi_M/P_loc/readout are parent-owned and fixed before calibration.",
            "status": "SOURCE_COMPONENT_DEFINED_OWNER_UNSIGNED",
            "missing_for_claim": "Pi_M origin, P_loc chain rule, readout variation, and fixed-before-readout calibration certificate",
        },
        {
            **base,
            "derivation_id": "JXD3645_6_boundary_shell_current",
            "claim": "Boundary and transition shells either vanish by theorem or enter the amplitude as explicit flux/source terms.",
            "formula": "J_X^shell ~ [D_X n^i partial_i X_N]_Sigma delta_Sigma + delta S_shell/delta X_N; A_bdy from Green boundary flux",
            "result": "No plateau/local-vacuum claim can ignore boundary flux or shell mismatch.",
            "status": "SOURCE_COMPONENT_DEFINED_OWNER_UNSIGNED",
            "missing_for_claim": "boundary class, matching conditions, shell support, and no-flux theorem or bound",
        },
        {
            **base,
            "derivation_id": "JXD3645_7_green_amplitude_map",
            "claim": "Once D_X, M_X^2, ell_X, and J_X^eff are owned, A_src is not free.",
            "formula": "X_N(x)-X_inf=int G_ell(x,y) J_X^eff(y)dV_y + boundary + topology; |A_src| <= C_G(D_X,ell_X) ||J_X^eff||_1",
            "result": "|A_X| <= |A_src[J_matter]|+|A_src[J_hidden_domain]|+|A_proj|+|A_shell|+|A_bdy|+|A_top| with no tuned cancellation credit.",
            "status": "AMPLITUDE_BOUND_DERIVED_CONDITIONALLY",
            "missing_for_claim": "Green normalization, component L1 bounds/zeros, source paths, and operator values",
        },
        {
            **base,
            "derivation_id": "JXD3645_8_verdict",
            "claim": "3645 moves the framework forward by replacing vague coupling language with a runnable refusal contract.",
            "formula": "numeric_profile_run_allowed=false unless every J_X component has theorem_zero=true or a numeric bound with source_path",
            "result": "No local-GR, R10, PPN, clock, orbital, or profile-amplitude pass is claimed here.",
            "status": "CONTRACT_READY_NUMERIC_RUN_REFUSED",
            "missing_for_claim": "owned source-current components or beta/source bound rows",
        },
    ]


def component_audit_rows(ts: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    specs = [
        ("JXC3645_0_matter_quotient", "J_X^matter", "-delta_X S_matter/sqrt(h)", "S_matter descends through q and all constants/readouts are X-blind", "beta_i or T_obs partial_X g_obs bound", "MISSING_MATTER_DESCENT_OR_BETA_BOUND", "A_src_matter;R10;PPN;clock;orbital"),
        ("JXC3645_1_hidden_domain", "J_X^hidden_domain", "-delta_X(S_hidden+S_domain)/sqrt(h)", "hidden/domain sector is double-zero or projection-orthogonal", "L1 bound on hidden/domain current", "MISSING_HIDDEN_DOMAIN_CURRENT_OWNER", "A_src_hidden;PPN;clock"),
        ("JXC3645_2_projector", "J_X^projector", "-delta_X S_projector/sqrt(h)", "Pi_M/P_loc/readout variation vanishes before calibration", "L1 bound on projector current", "MISSING_PROJECTOR_CURRENT_OWNER", "A_proj;GM calibration;PPN"),
        ("JXC3645_3_shell", "J_X^shell", "jump/mismatch distribution on transition support", "matching conditions make shell jump zero", "finite shell source bound and support radius", "MISSING_SHELL_CURRENT_OWNER", "A_shell;orbital;R10"),
        ("JXC3645_4_boundary", "boundary_flux_X", "int_boundary X D_X n.grad X plus boundary variation", "allowed boundary class gives no flux/exact/topological fixed term", "boundary flux bound", "MISSING_BOUNDARY_FLUX_OWNER", "A_bdy;nohair;PPN"),
        ("JXC3645_5_topology", "A_top;Q_X", "harmonic/topological exterior mode", "local topology/cohomology trivial or fixed topological charge zero", "topological charge bound", "MISSING_TOPOLOGY_OWNER", "A_top;long_range"),
        ("JXC3645_6_operator", "D_X;M_X^2;ell_X", "same-branch positive operator and ell_X=sqrt(D_X/M_X^2)", "parent Hessian supplies positive D_X and M_X^2 with units", "source-backed operator/range row", "MISSING_OPERATOR_RANGE_OWNER", "all_profile_channels"),
        ("JXC3645_7_normalization", "Xhat;beta_i;qbar_XT", "field/source normalization linking current to alpha and PPN projections", "Ward/source normalization fixed by parent", "normalization row with no-cancellation guard", "MISSING_SOURCE_NORMALIZATION_OWNER", "R10;PPN;composition"),
    ]
    return [
        {
            **base,
            "component_id": cid,
            "component": component,
            "variation_expression": expression,
            "theorem_zero_gate": zero_gate,
            "numeric_bound_gate": bound_gate,
            "current_status": status,
            "blocks_or_feeds": feeds,
        }
        for cid, component, expression, zero_gate, bound_gate, status, feeds in specs
    ]


def input_schema_rows(ts: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "score_ready": False,
    }
    specs = [
        ("SCHEMA3645_0_run_id", "run_id", True, "identifier", "private profile-source smoke run id", "REQUIRED"),
        ("SCHEMA3645_1_operator", "D_X;M_X2;ell_X", True, "operator;operator;m", "same-branch operator/range values or theorem-zero branch", "REQUIRED_MISSING_VALUES"),
        ("SCHEMA3645_2_matter", "J_matter_theorem_zero;J_matter_L1_bound;beta_source;beta_test", True, "bool;current_units;dimensionless;dimensionless", "matter descent proof or sourced beta/current bounds", "REQUIRED_MISSING_VALUES"),
        ("SCHEMA3645_3_hidden_domain", "J_hidden_domain_theorem_zero;J_hidden_domain_L1_bound", True, "bool;current_units", "hidden/domain source zero or bound", "REQUIRED_MISSING_VALUES"),
        ("SCHEMA3645_4_projector", "J_projector_theorem_zero;J_projector_L1_bound", True, "bool;current_units", "projector/readout source zero or bound", "REQUIRED_MISSING_VALUES"),
        ("SCHEMA3645_5_shell", "J_shell_theorem_zero;J_shell_L1_bound;support_radius", True, "bool;current_units;m", "transition shell zero or finite-support bound", "REQUIRED_MISSING_VALUES"),
        ("SCHEMA3645_6_boundary_topology", "boundary_flux_zero;boundary_flux_bound;topology_zero;Q_X_bound", True, "bool;flux_units;bool;X_N*length", "boundary/topology zero or bound rows", "REQUIRED_MISSING_VALUES"),
        ("SCHEMA3645_7_sources", "source_paths", True, "paths/URLs", "source path for every nonzero value and every theorem-zero certificate", "REQUIRED_FOR_ANY_NUMERIC_RUN"),
        ("SCHEMA3645_8_guard", "no_cancellation_credit", True, "bool", "must be true: components combine by absolute envelope, not tuned cancellation", "REQUIRED_TRUE"),
    ]
    return [
        {
            **base,
            "schema_id": sid,
            "field": field,
            "required": required,
            "units": units,
            "description": description,
            "current_status": status,
        }
        for sid, field, required, units, description, status in specs
    ]


def green_map_rows(ts: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "score_ready": False,
    }
    specs = [
        ("GMAP3645_0_matter", "A_src_matter", "A_src[J_matter]", "<= C_G(D_X,ell_X) ||J_matter||_1", "matter descent theorem or beta/current bound", "MISSING_MATTER_SOURCE_ROW"),
        ("GMAP3645_1_hidden_domain", "A_src_hidden_domain", "A_src[J_hidden_domain]", "<= C_G(D_X,ell_X) ||J_hidden_domain||_1", "hidden/domain zero or current bound", "MISSING_HIDDEN_DOMAIN_SOURCE_ROW"),
        ("GMAP3645_2_projector", "A_proj", "A_src[J_projector] plus readout amplitude", "<= C_G(D_X,ell_X) ||J_projector||_1", "projector zero or current bound", "MISSING_PROJECTOR_SOURCE_ROW"),
        ("GMAP3645_3_shell", "A_shell", "A_src[J_shell]", "<= C_G(D_X,ell_X) ||J_shell||_1", "shell zero or finite support bound", "MISSING_SHELL_SOURCE_ROW"),
        ("GMAP3645_4_boundary", "A_bdy", "Green boundary integral", "<= boundary_flux_bound mapped by G_ell", "boundary no-flux theorem or flux bound", "MISSING_BOUNDARY_FLUX_ROW"),
        ("GMAP3645_5_topology", "A_top;Q_X", "harmonic/topological exterior mode", "<= Q_X_bound or zero", "topology triviality/charge row", "MISSING_TOPOLOGY_ROW"),
        ("GMAP3645_6_total_guard", "A_X_abs", "|A_X| <= |A_src_matter|+|A_src_hidden_domain|+|A_proj|+|A_shell|+|A_bdy|+|A_top|", "no cancellation credit", "all component rows with source_paths", "TOTAL_GUARD_NONCLAIM"),
    ]
    return [
        {
            **base,
            "map_id": mid,
            "amplitude_component": comp,
            "source_map": source_map,
            "bound_law": bound_law,
            "required_input": required_input,
            "current_status": status,
        }
        for mid, comp, source_map, bound_law, required_input, status in specs
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    base = {"timestamp_utc": ts, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "valid_for_claim": False}
    return [
        {
            **base,
            "decision_id": "DEC3645_0_identity_derived",
            "decision": "J_X^eff is now defined by parent variation rather than treated as a vague missing coupling.",
            "status": "SOURCE_CURRENT_IDENTITY_DERIVED_CONDITIONALLY",
        },
        {
            **base,
            "decision_id": "DEC3645_1_cleanest_route",
            "decision": "The lowest-scrutiny route is proving matter quotient descent/no-marker silence, because it gives J_X^matter=0 instead of fitted small beta.",
            "status": "MATTER_DESCENT_ROUTE_PRIORITIZED",
        },
        {
            **base,
            "decision_id": "DEC3645_2_numeric_refusal",
            "decision": "No profile smoke run is allowed until every source component has theorem-zero or a numeric sourced bound.",
            "status": "NUMERIC_PROFILE_RUN_REFUSED",
        },
        {
            **base,
            "decision_id": "DEC3645_3_next",
            "decision": "Next target is the matter-coupling descent theorem or the first explicit beta/source row.",
            "status": "MATTER_COUPLING_DESCENT_OR_BETA_ROW_NEXT",
        },
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": ts,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "JX_EFFECTIVE_SOURCE_CURRENT_DERIVED_AS_CONDITIONAL_CONTRACT",
            "summary": "3645 derives the effective source-current identity, splits J_X^eff into matter, hidden/domain, projector, shell, boundary, and topology channels, and converts the profile amplitude problem into source-current zero/bound rows.",
            "claim_ceiling": "no local-GR/Newton, R10, PPN, clock, orbital, no-hair, or profile-amplitude pass is claimed",
            "useful_result": "the coupling fork is now exact: prove quotient/matter descent for zero, or fill beta/current bounds with source paths",
            "valid_for_claim": False,
        }
    ]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": ts,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3645_0",
            "target_doc": "3646-Y5-R2FR-matter-coupling-descent-or-first-beta-source-row.md",
            "target_script": "scripts/Y5_R2FR_3646_matter_coupling_descent_or_first_beta_source_row.py",
            "objective": "try to prove S_matter=Sbar[q(Phi),Psi,theta] with no-marker/no-shadow constants so J_X^matter=0; if not, emit first beta/source-current rows for source/test bodies with refusal gates",
            "success_gate": "either parent-signed matter descent gives beta_i=0, or beta/source rows have units, source paths, material dependence, and no-cancellation guards",
            "valid_for_claim": False,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_doc(
    src: list[dict[str, object]],
    deriv: list[dict[str, object]],
    audit: list[dict[str, object]],
    schema: list[dict[str, object]],
    green: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    nxt: list[dict[str, object]],
) -> None:
    lines = [
        "# 3645 Y5 R2FR effective JX source current owner or profile smoke schema",
        "",
        f"**Status:** {status[0]['summary']}",
        "",
        "**Claim ceiling:** no local-GR/Newton, R10, PPN, clock, orbital, no-hair, or profile-amplitude pass is claimed from this checkpoint.",
        "",
        "## Main result",
        "",
        "The coupling problem is now an exact variation problem. With the 1025 local operator convention,",
        "",
        "`J_X^eff := -(1/sqrt(h)) delta(S_matter+S_hidden+S_domain+S_projector+S_shell)/delta X_N`.",
        "",
        "Therefore a local-vacuum/GR route needs theorem-zero rows for the source components, not a plateau axiom. The cleanest branch is matter quotient descent: if `S_matter=Sbar[q(Phi),Psi,theta]`, `v_X in ker(Dq)`, and constants/readouts are X-blind, then `J_X^matter=0` and the beta leg vanishes.",
        "",
        "## Derived source split",
    ]
    for row in deriv:
        lines.append(f"- `{row['derivation_id']}`: {row['status']} — {row['result']}")
    lines.extend(["", "## Component owner audit"])
    for row in audit:
        lines.append(f"- `{row['component_id']}`: `{row['component']}` — {row['current_status']}")
    lines.extend(["", "## Smoke-runner refusal schema"])
    for row in schema:
        lines.append(f"- `{row['field']}`: {row['current_status']} — {row['description']}")
    lines.extend(["", "## Green amplitude map"])
    for row in green:
        lines.append(f"- `{row['map_id']}`: `{row['amplitude_component']}` — {row['bound_law']} ({row['current_status']})")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['status']} — {row['decision']}")
    lines.extend(
        [
            "",
            "## Next target",
            "",
            f"`{nxt[0]['target_doc']}` via `{nxt[0]['target_script']}`.",
            "",
            "## Sources",
        ]
    )
    for row in src:
        lines.append(f"- `{row['source_id']}`: `{row['source_path']}` exists={row['source_exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(out: dict[str, Path], src: list[dict[str, object]]) -> list[dict[str, object]]:
    ts = now()
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    add("VAL3645_0_sources_exist", all(bool(row["source_exists"]) for row in src), "all source paths exist")
    add("VAL3645_1_needles_found", all(bool(row["needle_found"]) for row in src), "all source needles found")
    pre = {name: path for name, path in out.items() if name != "validation"}
    add("VAL3645_2_outputs_exist", all(path.exists() for path in pre.values()) and DOC.exists(), "all outputs and doc written before validation")

    parse_ok = True
    counts = []
    parsed: dict[str, list[dict[str, str]]] = {}
    for name, path in pre.items():
        if path.suffix.lower() != ".csv":
            continue
        try:
            parsed[name] = read_csv(path)
            counts.append(f"{name}:{len(parsed[name])}")
        except Exception as exc:  # pragma: no cover - validation path
            parse_ok = False
            counts.append(f"{name}:ERR:{exc}")
    add("VAL3645_3_csv_parse", parse_ok, "; ".join(counts))

    deriv = parsed["jx_variation"]
    audit = parsed["component_audit"]
    schema = parsed["input_schema"]
    green = parsed["green_map"]
    decisions = parsed["decisions"]
    status = parsed["status"]
    nxt = parsed["next_target"]
    generated_groups = [deriv, audit, schema, green, decisions, status, nxt]

    add("VAL3645_4_jx_identity_present", any("J_X^eff :=" in row["formula"] for row in deriv), "effective source-current definition present")
    add("VAL3645_5_matter_beta_and_zero_present", any("beta_i" in row["result"] for row in deriv) and any("J_X^matter=0" in row["result"] for row in deriv), "matter beta law and quotient-zero gate present")
    required_components = {"J_X^matter", "J_X^hidden_domain", "J_X^projector", "J_X^shell", "boundary_flux_X", "A_top;Q_X", "D_X;M_X^2;ell_X"}
    add("VAL3645_6_component_audit_complete", required_components.issubset({row["component"] for row in audit}), "source, boundary, topology, and operator components audited")
    required_fields = {"D_X;M_X2;ell_X", "J_matter_theorem_zero;J_matter_L1_bound;beta_source;beta_test", "J_hidden_domain_theorem_zero;J_hidden_domain_L1_bound", "source_paths", "no_cancellation_credit"}
    add("VAL3645_7_schema_required_fields", required_fields.issubset({row["field"] for row in schema}), "runner schema includes operator, matter, hidden/domain, paths, and no-cancellation guard")
    add("VAL3645_8_green_absolute_guard", any(row["amplitude_component"] == "A_X_abs" and "|A_X| <=" in row["source_map"] for row in green), "absolute amplitude envelope retained")
    add("VAL3645_9_no_score_ready", all(row.get("score_ready", "False").lower() == "false" for table in [schema, green] for row in table), "schema/map rows refuse numeric scoring")
    add("VAL3645_10_nonclaim_all_outputs", all(row.get("valid_for_claim", "False").lower() == "false" for table in generated_groups for row in table), "all generated rows remain nonclaim")
    add("VAL3645_11_decision_next", any(row["status"] == "MATTER_COUPLING_DESCENT_OR_BETA_ROW_NEXT" for row in decisions), "matter coupling descent/beta row selected next")
    add("VAL3645_12_next_target_written", bool(nxt) and "3646" in nxt[0]["target_doc"], "3646 target written")
    add("VAL3645_13_status_honest", status[0]["status"] == "JX_EFFECTIVE_SOURCE_CURRENT_DERIVED_AS_CONDITIONAL_CONTRACT", "status keeps conditional/nonclaim ceiling")
    doc_text = DOC.read_text(encoding="utf-8", errors="replace") if DOC.exists() else ""
    add("VAL3645_14_doc_written", "J_X^eff :=" in doc_text and "matter quotient descent" in doc_text, "doc records source-current identity and clean branch")
    leak_patterns = ["*Y5_R2FR_3645*", "3645-Y5-R2FR-*", "Y5_R2FR_3645_*"]
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in leak_patterns:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3645_15_no_formalization_leak", not leaks, "no 3645 checkpoint files in formalization-workbench")
    add("VAL3645_16_claim_guard", all(row.get("valid_for_claim", "False").lower() == "false" for row in deriv), "derivation rows keep valid_for_claim=false")
    return rows


def main() -> None:
    ts = now()
    out = outputs()
    src = source_register(ts)
    deriv = jx_variation_rows(ts)
    audit = component_audit_rows(ts)
    schema = input_schema_rows(ts)
    green = green_map_rows(ts)
    decisions = decision_rows(ts)
    status = status_rows(ts)
    nxt = next_target_rows(ts)

    write_csv(out["source_register"], src)
    write_csv(out["jx_variation"], deriv)
    write_csv(out["component_audit"], audit)
    write_csv(out["input_schema"], schema)
    write_csv(out["green_map"], green)
    write_csv(out["decisions"], decisions)
    write_csv(out["status"], status)
    write_csv(out["next_target"], nxt)
    write_doc(src, deriv, audit, schema, green, decisions, status, nxt)

    validation = validate(out, src)
    write_csv(out["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3645 validation failed: {failures}")
    print(f"wrote 3645 checkpoint with {len(validation)} validation checks")


if __name__ == "__main__":
    main()
