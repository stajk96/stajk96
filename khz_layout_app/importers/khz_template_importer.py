from __future__ import annotations

import re
from io import BytesIO
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from core.models import (
    ImportedMetricObservation,
    ImportedSheetParseResult,
    KHZTemplateParseResult,
)


SCHEMA_PATH = Path("data/khz_template_schema.yaml")


def _norm(text: Any) -> str:
    s = str(text or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return re.sub(r"_+", "_", s).strip("_")


def _contains_token(value: str, token: str) -> bool:
    return token in value or value in token


def load_khz_schema(path: str | Path = SCHEMA_PATH) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def detect_khz_template_by_sheets(sheet_names: list[str], schema: dict[str, Any]) -> bool:
    known = {_norm(x) for x in schema.get("known_sheet_tokens", [])}
    actual = {_norm(x) for x in sheet_names}
    return len(actual.intersection(known)) >= 2


def detect_header_row(raw_df: pd.DataFrame, expected_tokens: list[str], max_scan_rows: int = 30) -> tuple[int | None, float, list[int]]:
    best_row = None
    best_score = -1.0
    candidates: list[int] = []
    token_norm = [_norm(t) for t in expected_tokens]

    for i in range(min(max_scan_rows, len(raw_df))):
        row_values = [_norm(v) for v in raw_df.iloc[i].tolist() if str(v).strip() not in {"", "nan", "None"}]
        if not row_values:
            continue
        hits = 0
        for t in token_norm:
            if any(_contains_token(cell, t) for cell in row_values):
                hits += 1
        score = hits / max(len(token_norm), 1)
        if score > best_score:
            best_score = score
            best_row = i
        if score >= 0.35:
            candidates.append(i)

    return best_row, max(best_score, 0.0), candidates


def normalize_semantic_columns(columns: list[Any], schema: dict[str, Any]) -> dict[str, str]:
    synonyms = schema.get("column_synonyms", {})
    out: dict[str, str] = {}
    for c in columns:
        c_norm = _norm(c)
        if c_norm.startswith("unnamed") or not c_norm:
            continue
        for canonical, syns in synonyms.items():
            syn_norm = [_norm(s) for s in syns]
            if any(_contains_token(c_norm, s) for s in syn_norm):
                out[str(c)] = canonical
                break
    return out


def _to_float(v: Any) -> float | None:
    try:
        if v is None or str(v).strip() == "":
            return None
        return float(v)
    except Exception:
        return None


def _to_bool(v: Any) -> bool | None:
    t = str(v).strip().lower()
    if t in {"yes", "y", "true", "1", "required"}:
        return True
    if t in {"no", "n", "false", "0", "optional"}:
        return False
    return None


def _pick(row: pd.Series, reverse_map: dict[str, str], key: str) -> Any:
    source = reverse_map.get(key)
    return row.get(source) if source else None


def parse_layout_sheet(raw_df: pd.DataFrame, sheet_name: str, schema: dict[str, Any]) -> ImportedSheetParseResult:
    expected = schema.get("layout_expected_header_tokens", [])
    header_row, confidence, candidates = detect_header_row(raw_df, expected)
    warnings: list[str] = []

    if header_row is None:
        return ImportedSheetParseResult(sheet_name=sheet_name, recognized=False, header_row=None, header_confidence=0.0, warnings=["No probable header row detected."])

    if len(candidates) > 1:
        warnings.append(f"Multiple possible header rows detected: {candidates}")
    if confidence < 0.45:
        warnings.append("Header row uncertain; please review columns manually.")

    header = raw_df.iloc[header_row].tolist()
    body = raw_df.iloc[header_row + 1 :].copy()
    body.columns = header
    body = body.dropna(how="all")

    semantic = normalize_semantic_columns(list(body.columns), schema)
    reverse_map = {v: k for k, v in semantic.items()}

    observations: list[ImportedMetricObservation] = []
    for idx, row in body.iterrows():
        metric_name = str(_pick(row, reverse_map, "metric_name") or "").strip()
        metric_code = str(_pick(row, reverse_map, "metric_code") or "").strip()
        observed = _to_float(_pick(row, reverse_map, "observed_value"))
        score = _to_float(_pick(row, reverse_map, "score"))

        if not metric_name and not metric_code:
            continue

        observations.append(
            ImportedMetricObservation(
                source_sheet=sheet_name,
                source_row=int(idx) + 1,
                category=str(_pick(row, reverse_map, "category") or ""),
                metric_code=metric_code,
                metric_name=metric_name,
                unit=str(_pick(row, reverse_map, "unit") or ""),
                threshold_low=_to_float(_pick(row, reverse_map, "threshold_low")),
                threshold_high=_to_float(_pick(row, reverse_map, "threshold_high")),
                observed_value=observed,
                score=score,
                severity=str(_pick(row, reverse_map, "severity") or ""),
                required_flag=_to_bool(_pick(row, reverse_map, "required_flag")),
                evidence_source=str(_pick(row, reverse_map, "evidence_source") or ""),
                comments=str(_pick(row, reverse_map, "comments") or ""),
                next_step=str(_pick(row, reverse_map, "next_step") or ""),
            )
        )

    if not observations:
        warnings.append("No metric observations extracted from this sheet.")
    if reverse_map.get("score") and not reverse_map.get("severity"):
        warnings.append("Score column detected but not severity column.")

    return ImportedSheetParseResult(
        sheet_name=sheet_name,
        recognized=True,
        header_row=header_row,
        header_confidence=confidence,
        normalized_columns=sorted(set(semantic.values())),
        warnings=warnings,
        observations=observations,
    )


def map_layout_observations_to_canonical(observations: list[ImportedMetricObservation], schema: dict[str, Any]) -> tuple[dict[str, float], list[ImportedMetricObservation]]:
    rules = schema.get("metric_mapping_rules", {})
    mapped: dict[str, list[float]] = {k: [] for k in rules.keys()}
    unmapped: list[ImportedMetricObservation] = []

    for obs in observations:
        key_text = f"{obs.metric_code} {obs.metric_name}".lower()
        match_key = None
        for canonical_var, keywords in rules.items():
            if any(k.lower() in key_text for k in keywords):
                match_key = canonical_var
                break

        if not match_key:
            obs.mapping_confidence = 0.0
            unmapped.append(obs)
            continue

        # Conservative value mapping: score if available, else observed value clipped.
        raw_val = obs.score if obs.score is not None else obs.observed_value
        if raw_val is None:
            obs.mapping_confidence = 0.25
            unmapped.append(obs)
            continue

        # Convert to index scale around 1.0, conservative bounds.
        normalized = max(0.6, min(1.4, float(raw_val) / 100 if float(raw_val) > 3 else float(raw_val)))
        mapped[match_key].append(normalized)
        obs.mapping_confidence = 0.75
        obs.mapped_variable = match_key

    aggregated = {k: round(sum(v) / len(v), 3) for k, v in mapped.items() if v}
    return aggregated, unmapped


def parse_khz_template_workbook(file) -> KHZTemplateParseResult:
    schema = load_khz_schema()
    payload = file.getvalue() if hasattr(file, "getvalue") else file.read()
    xls = pd.ExcelFile(BytesIO(payload))

    detected = detect_khz_template_by_sheets(xls.sheet_names, schema)
    sheet_map = {_norm(k): v for k, v in schema.get("sheet_name_map", {}).items()}

    recognized_sheets: list[str] = []
    unrecognized_sheets: list[str] = []
    results: list[ImportedSheetParseResult] = []
    all_obs: list[ImportedMetricObservation] = []
    warnings: list[str] = []

    for sh in xls.sheet_names:
        sh_norm = _norm(sh)
        category = sheet_map.get(sh_norm)
        raw = pd.read_excel(BytesIO(payload), sheet_name=sh, header=None)

        if category == "layout":
            res = parse_layout_sheet(raw, sh, schema)
            results.append(res)
            all_obs.extend(res.observations)
            warnings.extend(res.warnings)
            if res.recognized:
                recognized_sheets.append(sh)
            else:
                unrecognized_sheets.append(sh)
        elif category in {"picking", "dock", "site_profile", "scenarios"}:
            recognized_sheets.append(sh)
            results.append(ImportedSheetParseResult(sheet_name=sh, recognized=True, warnings=["Sheet recognized but semantic parser is not yet specialized for this sheet type."]))
        else:
            unrecognized_sheets.append(sh)

    mapped_intermediate, unmapped = map_layout_observations_to_canonical(all_obs, schema)

    baseline_fields = {}
    if "staging_efficiency_index" in mapped_intermediate:
        baseline_fields["zone_separation_quality"] = mapped_intermediate["staging_efficiency_index"]
    if "slotting_quality_index" in mapped_intermediate:
        baseline_fields["abc_slotting_compliance"] = mapped_intermediate["slotting_quality_index"]

    confidence = 0.0
    if results:
        confidence = round(sum(r.header_confidence for r in results if r.recognized) / max(len([r for r in results if r.recognized]), 1), 3)

    return KHZTemplateParseResult(
        workbook_mode="KHZ structured site template",
        detected=detected,
        recognized_sheets=recognized_sheets,
        unrecognized_sheets=unrecognized_sheets,
        sheet_results=results,
        mapped_intermediate=mapped_intermediate,
        mapped_baseline_fields=baseline_fields,
        unmapped_observations=unmapped,
        validation_warnings=warnings,
        confidence_score=confidence,
    )
