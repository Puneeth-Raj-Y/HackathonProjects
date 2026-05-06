import spacy
import re
from datetime import datetime
from routes import orders,chat
import os
import logging

logger = logging.getLogger("forgemind.nlp")

try:
    nlp = spacy.load("en_core_web_sm")
    logger.info("Loaded existing spaCy model.")
except OSError:
    logger.warning("spaCy model not found. Downloading 'en_core_web_sm'...")
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")
    logger.info("Successfully downloaded and loaded spaCy model.")

class HybridNLPEngine:
    def __init__(self):
        # Generalized categories for extraction
        self.categories = {
            "electronics": ["laptop", "phone", "monitor", "cable", "sensor"],
            "furniture": ["chair", "desk", "table", "sofa", "bed"],
            "clothing": ["shirt", "pants", "belt", "shoe", "hat"],
            "medical": ["kit", "mask", "cylinder", "glove", "syringe"],
            "industrial": ["machine", "tool", "flange", "bolt", "valve", "engine"],
            "food": ["box", "bag", "kg", "bottle"]
        }

    def split_orders(self, text):
        """Splits complex sentences like 'Need 20 chairs and 10 desks' into separate items."""
        parts = re.split(r'\b(?:and)\b|,(?=\s*\d+)', text, flags=re.IGNORECASE)
        return [p.strip() for p in parts if p.strip()]

    def extract_item_details(self, text):
        """Extracts quantity, product, and specifications from a single order string."""
        doc = nlp(text) if nlp else None
        
        item = {
            "quantity": 1,
            "product_name": "Unknown Product",
            "category": "General",
            "specification": "Standard"
        }

        # 1. Extract Quantity (Avoid extracting number if it's part of an ID like #4)
        clean_text = re.sub(r'#\d+', '', text)
        qty_match = re.search(r'\b(\d+)\b', clean_text)
        if qty_match:
            item["quantity"] = int(qty_match.group(1))

        # Extract potential Order ID for status checks
        id_match = re.search(r'(?:#|order\s+)(\d+)', text.lower())
        order_id = int(id_match.group(1)) if id_match else None
        
        # 2. Extract Product Name & Category
        found_product = False
        words = text.lower().split()
        
        for cat, keywords in self.categories.items():
            for kw in keywords:
                if kw in text.lower():
                    item["category"] = cat
                    kw_idx = text.lower().find(kw)
                    item["product_name"] = kw.title()
                    found_product = True
                    break
            if found_product: break

        if not found_product:
            match = re.search(r'\d+\s+(.*?)(?:\s+for|by|within|at|$)', text.lower())
            if match:
                item["product_name"] = match.group(1).strip().title()

        # 3. Extract Specifications (Adjectives/Materials)
        if doc:
            adjs = [token.text for token in doc if token.pos_ == "ADJ"]
            if adjs:
                item["specification"] = ", ".join(adjs).title()

        return item

    def extract_deadline(self, text):
        if nlp:
            doc = nlp(text)
            for ent in doc.ents:
                if ent.label_ == "DATE":
                    return ent.text
        
        date_match = re.search(r'(?:by|within|on|for)\s+([A-Za-z]+\s+\d+)', text, re.IGNORECASE)
        if date_match:
            return date_match.group(1)
        return "TBD"

    def parse_complex_request(self, text):
        global_deadline = self.extract_deadline(text)
        order_parts = self.split_orders(text)
        
        id_match = re.search(r'(?:#|order\s+)(\d+)', text.lower())
        order_id = int(id_match.group(1)) if id_match else None

        extracted_items = []
        for part in order_parts:
            details = self.extract_item_details(part)
            part_deadline = self.extract_deadline(part)
            if part_deadline == "TBD":
                part_deadline = global_deadline
            details["deadline"] = part_deadline
            extracted_items.append(details)
            
        return {
            "items": extracted_items,
            "deadline": global_deadline, # kept for backward compatibility
            "order_id": order_id
        }

    def classify_intent(self, text):
        text = text.lower()
        if any(re.search(rf'\b{w}\b', text) for w in ["hi", "hello", "hey"]): return "GREETING"
        if any(re.search(rf'\b{w}\b', text) for w in ["update", "where", "status", "track", "check"]): 
            return "QUERY_STATUS"
        if any(re.search(rf'\b{w}\b', text) for w in ["need", "order", "want", "buy", "purchase"]): 
            return "CREATE_ORDER"
        return "UNKNOWN"

nlp_engine = HybridNLPEngine()
