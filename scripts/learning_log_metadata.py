#!/usr/bin/env python3
"""Load the canonical Learning Log metadata contract."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


SCHEMA_PATH = "system/LEARNING_LOG_METADATA_SCHEMA.json"


@dataclass(frozen=True)
class DomainPolicy:
    learning_domains: frozenset[str]
    non_learning_domains: frozenset[str]

    @property
    def allowed_domains(self) -> frozenset[str]:
        return self.learning_domains | self.non_learning_domains


def _string_set(raw: object, field: str) -> frozenset[str]:
    if not isinstance(raw, list) or not raw:
        raise ValueError(f"{SCHEMA_PATH}의 {field}는 비어 있지 않은 배열이어야 합니다.")
    if any(not isinstance(item, str) or not item.strip() for item in raw):
        raise ValueError(f"{SCHEMA_PATH}의 {field}에는 비어 있지 않은 문자열만 허용됩니다.")
    values = [item.strip() for item in raw]
    if len(values) != len(set(values)):
        raise ValueError(f"{SCHEMA_PATH}의 {field}에 중복 값이 있습니다.")
    return frozenset(values)


def load_domain_policy(root: Path) -> DomainPolicy:
    schema_path = root / SCHEMA_PATH
    try:
        raw = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"{SCHEMA_PATH}를 읽을 수 없습니다: {error}") from error

    if not isinstance(raw, dict) or raw.get("version") != 1:
        raise ValueError(f"{SCHEMA_PATH}는 지원되는 version 1이어야 합니다.")
    learning = _string_set(raw.get("learning_domains"), "learning_domains")
    non_learning = _string_set(
        raw.get("non_learning_domains"), "non_learning_domains"
    )
    overlap = sorted(learning & non_learning)
    if overlap:
        raise ValueError(
            f"{SCHEMA_PATH}에서 learning/non-learning Domain이 중복됩니다: "
            + ", ".join(overlap)
        )
    return DomainPolicy(learning, non_learning)
