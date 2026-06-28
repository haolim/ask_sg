from dataclasses import dataclass


@dataclass(frozen=True)
class GoldenPair:
    id: str
    user_input: str
    reference: str
    kind: str # "retrieval" | "boundary"
    unique_markers: tuple[str, ...] | None = None # test compound filters



GOLDEN_SET: list[GoldenPair] = [
    GoldenPair(
        id="q1_aggregate_boundary",
        user_input="What was the average resale price of a 4-room flat in Bishan in 2023?",
        reference="I cannot answer that type of question yet.",
        kind="boundary",
    ),
    GoldenPair(
        id="q2_bishan_5room",
        user_input="What was the resale price of a 5-room flat located in Bishan Street 23 and sold in February of 2025?",
        reference="$1,105,000",
        kind="precise_filter",
        unique_markers=("1150000",),
    ),
    GoldenPair(
        id="q3_queenstown_5room_floor_area_storey_level",
        user_input="What was the floor area and storey level of a 5-room flat located in Queenstown Clarence Lane that was sold in November 2025?",
        reference="The floor area is 121 sqm and it is on the 10 to 12 storey range.",
        kind="precise_filter",
        unique_markers=("121 sqm", "10 TO 12")
    ),
    GoldenPair(
        id="q4_recent_5room_transactions",
        user_input="What are some recent 5-room resale transactions sold in 2025?",
        reference="Recent 5-room transactions include flats sold in Bishan, Ang Mo Kio, and Marine Parade",
        kind="retrieval",
    ),
]