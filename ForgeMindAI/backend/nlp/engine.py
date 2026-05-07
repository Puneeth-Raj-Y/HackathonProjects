import logging
import re
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

import spacy

logger = logging.getLogger("forgemind.nlp")

try:
    nlp = spacy.load("en_core_web_sm")
    logger.info("spaCy model loaded successfully")
except Exception as exc:
    nlp = None
    logger.warning("spaCy model unavailable, using fallback parser: %s", exc)

CATEGORY_KEYWORDS = {
    "electronics": ["laptop", "monitor", "computer", "tablet", "phone", "sensor", "router"],
    "industrial": ["bolt", "bolts", "valve", "engine", "gear", "bearing", "tool"],
    "medical": ["kit", "kits", "mask", "glove", "syringe", "bandage", "medical"],
    "furniture": ["chair", "desk", "table", "sofa", "cabinet", "bench"],
    "office": ["paper", "printer", "folder", "stapler", "pen"],
}

GREETING_PATTERNS = re.compile(r"\b(hi|hello|hey|good morning|good afternoon|good evening)\b", re.I)
STATUS_PATTERNS = re.compile(r"\b(status|track|where is|delivery|progress|order\s*#?\d+)\b", re.I)
ORDER_PATTERNS = re.compile(r"\b(need|order|buy|purchase|require|want|ship|deliver)\b", re.I)


def _normalize_product_name(text: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9\s-]", " ", text).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.title() if cleaned else "Unknown Item"


def _infer_category(text: str) -> str:
    lowered = text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            return category
    return "general"


def _extract_deadline(text: str) -> Optional[str]:
    deadline_patterns = [
        r"\bby\s+(today|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
        r"\bby\s+next\s+(week|month|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
        r"\bfor\s+(today|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
    ]
    for pattern in deadline_patterns:
        match = re.search(pattern, text, re.I)
        if match:
            return match.group(1).title() if len(match.groups()) == 1 else match.group(0).replace("by ", "").replace("for ", "").title()
    return None


def _split_segments(message: str) -> List[str]:
    normalized = re.sub(r"\band\b", ",", message, flags=re.I)
    parts = [segment.strip() for segment in re.split(r"[,;\n]", normalized) if segment.strip()]
    return parts if parts else [message.strip()]


def _parse_segment(segment: str) -> Dict[str, Any]:
    deadline = _extract_deadline(segment)
    quantity_match = re.search(r"\b(\d+)\b", segment)
    quantity = int(quantity_match.group(1)) if quantity_match else 1

    cleaned = re.sub(r"\bby\s+.*$", "", segment, flags=re.I)
    cleaned = re.sub(r"\bfor\s+.*$", "", cleaned, flags=re.I)
    cleaned = re.sub(r"\bneed\b|\border\b|\bbuy\b|\bpurchase\b|\bwant\b|\brequire\b|\bdeliver\b|\bship\b", "", cleaned, flags=re.I)
    cleaned = re.sub(r"\b\d+\b", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" ,.-")

    if nlp is not None:
        doc = nlp(cleaned or segment)
        noun_chunks = [chunk.text.strip() for chunk in doc.noun_chunks if chunk.text.strip()]
        if noun_chunks:
            cleaned = noun_chunks[0]

    product_name = _normalize_product_name(cleaned or segment)
    category = _infer_category(product_name)
    specification = "standard"

    if product_name.lower() in {"need", "order", "buy", "purchase", "want", "require"}:
        product_name = "Unknown Item"

    return {
        "product_name": product_name,
        "category": category,
        "quantity": quantity,
        "specification": specification,
        "deadline": deadline,
    }


class NLPWorkflowEngine:
    def classify_intent(self, message: str) -> str:
        text = message.strip().lower()
        if GREETING_PATTERNS.search(text):
            return "GREETING"
        if STATUS_PATTERNS.search(text):
            return "QUERY_STATUS"
        if ORDER_PATTERNS.search(text) or re.search(r"\b\d+\b", text):
            return "CREATE_ORDER"
        return "UNKNOWN"

    def extract_items(self, message: str) -> List[Dict[str, Any]]:
        logger.info("Parsing order message: %s", message)
        segments = _split_segments(message)
        items: List[Dict[str, Any]] = []

        for segment in segments:
            parsed = _parse_segment(segment)
            if parsed["product_name"] != "Unknown Item" or re.search(r"\b\d+\b", segment):
                items.append(parsed)

        if not items:
            items.append(
                {
                    "product_name": _normalize_product_name(message),
                    "category": _infer_category(message),
                    "quantity": 1,
                    "specification": "standard",
                    "deadline": _extract_deadline(message),
                }
            )

        logger.info("Extracted items: %s", items)
        return items

    def summarize_items(self, items: List[Dict[str, Any]]) -> str:
        parts = []
        for item in items:
            parts.append(f"{item['quantity']}x {item['product_name']}")
        return ", ".join(parts)


nlp_engine = NLPWorkflowEngine()
