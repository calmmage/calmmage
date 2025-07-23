import re
from loguru import logger
from pathlib import Path
from pydantic import BaseModel
from typing import List, Optional


class QuarterlyData(BaseModel):
    quarter: str
    gross_bookings: float
    mobility: float
    delivery: float
    total: float


def parse_financial_data(text: str) -> List[QuarterlyData]:
    # Simple regex patterns for financial data
    patterns = {
        'gross_bookings': r'Gross Bookings.*?\$(\d+\.?\d*)',
        'mobility': r'Mobility.*?\$(\d+\.?\d*)',
        'delivery': r'Delivery.*?\$(\d+\.?\d*)',
        'total': r'Total.*?\$(\d+\.?\d*)'
    }

    quarters = []

    # Split text by quarters (this is a basic example, adjust based on actual format)
    quarter_sections = text.split('Q')

    for section in quarter_sections[1:]:  # Skip first empty section
        try:
            quarter = f"Q{section.split()[0]}"
            data = {}

            for key, pattern in patterns.items():
                match = re.search(pattern, section)
                if match:
                    data[key] = float(match.group(1))
                else:
                    data[key] = 0.0

            quarters.append(QuarterlyData(
                quarter=quarter,
                **data
            ))

        except Exception as e:
            logger.error(f"Error parsing quarter data: {e}")
            continue

    return quarters


def format_as_table(data: List[QuarterlyData]) -> str:
    header = "| Quarter | Gross Bookings | Mobility | Delivery | Total |"
    separator = "|---------|----------------|----------|----------|--------|"
    rows = []

    for q in data:
        row = f"| {q.quarter} | ${q.gross_bookings:.1f}B | ${q.mobility:.1f}B | ${q.delivery:.1f}B | ${q.total:.1f}B |"
        rows.append(row)

    return "\n".join([header, separator] + rows)
