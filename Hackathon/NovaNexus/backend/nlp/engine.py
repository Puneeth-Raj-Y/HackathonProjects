import spacy
import re
from datetime import datetime

try:
    nlp = spacy.load("en_core_web_sm")
except:
    nlp = None

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
        # Simple splitting on 'and' or ',' if followed by a number
        parts = re.split(r'\b(?:and|,)\b(?=\s*\d+)', text, flags=re.IGNORECASE)
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
        # We look for nouns or specific keywords
        found_product = False
        words = text.lower().split()
        
        # Check against category keywords
        for cat, keywords in self.categories.items():
            for kw in keywords:
                if kw in text.lower():
                    item["category"] = cat
                    # Try to capture the specific product name (e.g., 'office chair')
                    # This is a simple heuristic: find the keyword and potentially the word before it
                    kw_idx = text.lower().find(kw)
                    # Basic extraction of the noun phrase around the keyword
                    item["product_name"] = kw.title()
                    found_product = True
                    break
            if found_product: break

        # If not found in categories, use spaCy or Regex
        if not found_product:
            # Heuristic: The text after the number
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
        # Extract DATE using spaCy or Regex
        if nlp:
            doc = nlp(text)
            for ent in doc.ents:
                if ent.label_ == "DATE":
                    return ent.text
        
        # Fallback Regex for dates like "July 20" or "May 15"
        date_match = re.search(r'(?:by|within|on|for)\s+([A-Za-z]+\s+\d+)', text, re.IGNORECASE)
        if date_match:
            return date_match.group(1)
        return "TBD"

    def parse_complex_request(self, text):
        deadline = self.extract_deadline(text)
        order_parts = self.split_orders(text)
        
        # Check for order ID in the whole string
        id_match = re.search(r'(?:#|order\s+)(\d+)', text.lower())
        order_id = int(id_match.group(1)) if id_match else None

        extracted_items = []
        for part in order_parts:
            details = self.extract_item_details(part)
            extracted_items.append(details)
            
        return {
            "items": extracted_items,
            "deadline": deadline,
            "order_id": order_id
        }

    def classify_intent(self, text):
        text = text.lower()
        if any(re.search(rf'\b{w}\b', text) for w in ["hi", "hello", "hey"]): return "GREETING"
        # High priority for status trigger words
        if any(re.search(rf'\b{w}\b', text) for w in ["update", "where", "status", "track", "check"]): 
            return "QUERY_STATUS"
        if any(re.search(rf'\b{w}\b', text) for w in ["need", "order", "want", "buy", "purchase"]): 
            return "CREATE_ORDER"
        return "UNKNOWN"

nlp_engine = HybridNLPEngine()
