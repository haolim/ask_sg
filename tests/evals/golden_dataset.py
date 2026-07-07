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
        unique_markers=("1,105,000",),
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
        kind="boundary",
    ),
    GoldenPair(
        id="q5_maisonette_serangoon",
        user_input="Show me executive maisonette flats in Serangoon",
        reference="Executive maisonette flats located in Serangoon town, typically 140-160 sqm with the Maisonette flat model",
        kind="retrieval",
    ),
    GoldenPair(
        id="q6_high_floor_central",
        user_input="high-floor flats near the city centre",
        reference="Flats in Central Area town on higher storey ranges such as 16 TO 18 or above",
        kind="retrieval",
    ),
    GoldenPair(
        id="q7_premium_apartment_bukit_panjang",
        user_input="premium apartment flats in Bukit Panjang",
        reference="5-room Premium Apartment flats in Bukit Panjang town along Senja Road",
        kind="retrieval",
    ),
    GoldenPair(
        id="q8_large_family_flat_bishan",
        user_input="spacious family flat in Bishan",
        reference="Larger 4-room and 5-room flats in Bishan town suitable for families, around 84-123 sqm",
        kind="retrieval",
    ),
    GoldenPair(
        id="q9_new_generation_hougang",
        user_input="New Generation flats in Hougang",
        reference="New Generation model flats in Hougang town, commonly 4-room around 105 sqm",
        kind="retrieval",
    ),
]