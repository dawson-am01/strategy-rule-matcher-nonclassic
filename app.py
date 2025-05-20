import streamlit as st
import pandas as pd
import json

# --- Set page settings ---
st.set_page_config(page_title="Strategy Rule Matcher – Nonclassic", page_icon="🧩")

st.title("🧩 Strategy Rule Matcher (Nonclassic)")
st.markdown("Match your context against custom rules for basketball player/team incidents.")

st.header("🔧 Query Context")

# --- Predefined options for each entity ---
entity_options = {
    "Brand": ["Brand 1", "Brand 2"],
    "Sport": ["Basketball", "American Football"],
    "Competition": ["NBA", "NFL"],
    "Incident": ["Points", "Assists", "Made Threes", "Rebounds", "Steals", "Blocks"],
    "Player or Team": ["S Curry", "J Brown", "Miami Heat", "Detroit Pistons"],
    "TimeBased": ["Live", "Pre Live", "30", "150", "360", "480", "600", "1440", "2880", "4320", "8640", "Q1", "Q2", "Q3", "Q4", "H1", "H2", "Match"],
    "Cohort": ["Cohort A", "Cohort B"]
}

# --- Default context (all present) ---
default_query_context = {
    "Brand": "Brand 1",
    "Sport": "Basketball",
    "Competition": "NBA",
    "Incident": "Points",
    "Player or Team": "S Curry",
    "TimeBased": "150",
    "Cohort": "Cohort A"
}

# --- Dropdowns for context ---
query_context = {}
for entity, options in entity_options.items():
    selection = st.selectbox(f"{entity}:", options, index=options.index(default_query_context[entity]))
    query_context[entity] = selection

# --- Entity weightings ---
st.header("⚖️ Entity Weightings")

default_weights = {
    "Brand": 1,
    "Sport": 1,
    "Competition": 5,
    "Incident": 7,
    "Player or Team": 10,
    "TimeBased": 15,
    "Cohort": 30
}

entity_weights = {}
for entity in entity_options.keys():
    weight = st.slider(f"Weight for {entity}", 0, 30, value=default_weights[entity])
    entity_weights[entity] = weight

# --- Default Rules (5 examples) ---
default_rules = pd.DataFrame({
    "Permutation": [
        "Brand:Brand 1, Sport:Basketball, TimeBased:H2, Incident:Rebounds, Competition:NFL, Cohort:Cohort A",
        "Brand:Brand 1, Sport:Basketball, Incident:Blocks, Player or Team:Miami Heat",
        "Brand:Brand 1, Sport:Basketball, Player or Team:S Curry, TimeBased:600",
        "Brand:Brand 1, Sport:Basketball, TimeBased:4320, Incident:Assists, Cohort:Cohort A, Competition:NFL",
        "Brand:Brand 1, Sport:Basketball, TimeBased:Pre Live",
        "Brand:Brand 1, Sport:Basketball, Incident:Rebounds, Cohort:Cohort B, TimeBased:30",
        "Brand:Brand 1, Sport:Basketball, Player or Team:Detroit Pistons",
        "Brand:Brand 1, Sport:Basketball, Incident:Assists",
        "Brand:Brand 1, Sport:Basketball, Competition:NFL, Incident:Rebounds, TimeBased:4320, Cohort:Cohort A",
        "Brand:Brand 1, Sport:Basketball, TimeBased:Q2, Cohort:Cohort B, Competition:NBA",
        "Brand:Brand 1, Sport:Basketball, TimeBased:Live",
        "Brand:Brand 1, Sport:Basketball, TimeBased:360, Competition:NBA, Incident:Assists, Player or Team:Detroit Pistons, Cohort:Cohort A",
        "Brand:Brand 1, Sport:Basketball, Competition:NBA, Player or Team:S Curry, Cohort:Cohort A, TimeBased:150, Incident:Made Threes",
        "Brand:Brand 1, Sport:Basketball, Cohort:Cohort A, Incident:Made Threes",
        "Brand:Brand 1, Sport:Basketball, Cohort:Cohort B, Incident:Rebounds, Competition:NFL, Player or Team:S Curry, TimeBased:30",
        "Brand:Brand 1, Sport:Basketball, Competition:NFL, Player or Team:Detroit Pistons, TimeBased:360",
        "Brand:Brand 1, Sport:Basketball, Incident:Made Threes",
        "Brand:Brand 1, Sport:Basketball, Competition:NFL, Incident:Points, Cohort:Cohort B, Player or Team:Detroit Pistons",
        "Brand:Brand 1, Sport:Basketball, Competition:NBA",
        "Brand:Brand 1, Sport:Basketball, Cohort:Cohort A, Incident:Made Threes, TimeBased:Q2, Competition:NFL, Player or Team:J Brown",
        "Brand:Brand 1, Sport:Basketball, TimeBased:Q4, Competition:NBA, Incident:Blocks, Cohort:Cohort B",
        "Brand:Brand 1, Sport:Basketball, Cohort:Cohort A, TimeBased:Live, Incident:Blocks, Competition:NBA",
        "Brand:Brand 1, Sport:Basketball, Player or Team:Detroit Pistons, Incident:Made Threes, Competition:NBA, Cohort:Cohort A, TimeBased:Live",
        "Brand:Brand 1, Sport:Basketball, Player or Team:J Brown, TimeBased:30, Cohort:Cohort B",
        "Brand:Brand 1, Sport:Basketball, Incident:Made Threes, Player or Team:S Curry, Competition:NFL, TimeBased:600",
        "Brand:Brand 1, Sport:Basketball, TimeBased:Q3",
        "Brand:Brand 1, Sport:Basketball, Competition:NBA, Cohort:Cohort B, Player or Team:J Brown",
        "Brand:Brand 1, Sport:Basketball, Player or Team:J Brown, Incident:Blocks",
        "Brand:Brand 1, Sport:Basketball, TimeBased:Match, Cohort:Cohort A, Incident:Steals, Competition:NBA, Player or Team:J Brown",
        "Brand:Brand 1, Sport:Basketball, Competition:NBA, TimeBased:150, Cohort:Cohort B, Incident:Points, Player or Team:S Curry",
        "Brand:Brand 1, Sport:Basketball, Competition:NBA, Cohort:Cohort B, Player or Team:Miami Heat, Incident:Points",
        "Brand:Brand 1, Sport:Basketball, Competition:NFL",
        "Brand:Brand 1, Sport:Basketball, Cohort:Cohort B, Competition:NBA, Player or Team:J Brown, Incident:Made Threes, TimeBased:1440",
        "Brand:Brand 1, Sport:Basketball, Incident:Steals, TimeBased:Q3, Competition:NBA, Cohort:Cohort A",
        "Brand:Brand 1, Sport:Basketball, Competition:NFL, Cohort:Cohort A, TimeBased:480, Incident:Steals",
        "Brand:Brand 1, Sport:Basketball, Incident:Assists, Competition:NBA",
        "Brand:Brand 1, Sport:Basketball, TimeBased:150, Competition:NBA, Cohort:Cohort A, Player or Team:Detroit Pistons, Incident:Blocks",
        "Brand:Brand 1, Sport:Basketball, TimeBased:Q2",
        "Brand:Brand 1, Sport:Basketball, Cohort:Cohort A, Player or Team:S Curry, Incident:Assists",
        "Brand:Brand 1, Sport:Basketball, Competition:NFL, Player or Team:J Brown, Incident:Points, Cohort:Cohort A, TimeBased:Q2",
        "Brand:Brand 1, Sport:Basketball, Player or Team:S Curry, TimeBased:H2, Cohort:Cohort B, Competition:NBA, Incident:Blocks",
        "Brand:Brand 1, Sport:Basketball, Competition:NBA, Player or Team:S Curry, Incident:Steals, Cohort:Cohort B",
        "Brand:Brand 1, Sport:Basketball, Cohort:Cohort A, Incident:Rebounds",
        "Brand:Brand 1, Sport:Basketball, TimeBased:1440, Cohort:Cohort B",
        "Brand:Brand 1, Sport:Basketball, Competition:NFL, TimeBased:Match, Incident:Points, Player or Team:S Curry, Cohort:Cohort A",
        "Brand:Brand 1, Sport:Basketball, Player or Team:Miami Heat, Incident:Assists, Competition:NBA, Cohort:Cohort B",
        "Brand:Brand 1, Sport:Basketball, Player or Team:Miami Heat, Incident:Rebounds",
        "Brand:Brand 1, Sport:Basketball, Incident:Blocks, Cohort:Cohort B, Player or Team:S Curry, Competition:NFL, TimeBased:1440",
        "Brand:Brand 1, Sport:Basketball, Cohort:Cohort A",
        "Brand:Brand 1, Sport:Basketball, TimeBased:Match, Player or Team:S Curry",
    ],
    "Strategy": [
        "strategy_nonclassic_001",
        "strategy_nonclassic_002",
        "strategy_nonclassic_003",
        "strategy_nonclassic_004",
        "strategy_nonclassic_005",
        "strategy_nonclassic_006",
        "strategy_nonclassic_007",
        "strategy_nonclassic_008",
        "strategy_nonclassic_009",
        "strategy_nonclassic_010",
        "strategy_nonclassic_011",
        "strategy_nonclassic_012",
        "strategy_nonclassic_013",
        "strategy_nonclassic_014",
        "strategy_nonclassic_015",
        "strategy_nonclassic_016",
        "strategy_nonclassic_017",
        "strategy_nonclassic_018",
        "strategy_nonclassic_019",
        "strategy_nonclassic_020",
        "strategy_nonclassic_021",
        "strategy_nonclassic_022",
        "strategy_nonclassic_023",
        "strategy_nonclassic_024",
        "strategy_nonclassic_025",
        "strategy_nonclassic_026",
        "strategy_nonclassic_027",
        "strategy_nonclassic_028",
        "strategy_nonclassic_029",
        "strategy_nonclassic_030",
        "strategy_nonclassic_031",
        "strategy_nonclassic_032",
        "strategy_nonclassic_033",
        "strategy_nonclassic_034",
        "strategy_nonclassic_035",
        "strategy_nonclassic_036",
        "strategy_nonclassic_037",
        "strategy_nonclassic_038",
        "strategy_nonclassic_039",
        "strategy_nonclassic_040",
        "strategy_nonclassic_041",
        "strategy_nonclassic_042",
        "strategy_nonclassic_043",
        "strategy_nonclassic_044",
        "strategy_nonclassic_045",
        "strategy_nonclassic_046",
        "strategy_nonclassic_047",
        "strategy_nonclassic_048",
        "strategy_nonclassic_049",
        "strategy_nonclassic_050",
    ]
})

# --- Editable Rule Table ---
st.subheader("📋 Rule Editor")
rules_data = st.data_editor(
    default_rules,
    use_container_width=True,
    num_rows="dynamic",
    height=450
)

# --- Matching Engine ---
if st.button("▶️ Run Matching"):
    try:
        def extract_entity_value(entry):
            entity, value = entry.split(":", 1)
            return entity.strip(), value.strip()

        def compute_score(permutation):
            return sum(entity_weights.get(entity, 0) for entity, _ in map(extract_entity_value, permutation))

        def matches_query(permutation):
            for entity, value in map(extract_entity_value, permutation):
                if query_context.get(entity) != value:
                    return False
            return True

        def includes_brand_and_sport(permutation):
            entities = [e for e, _ in map(extract_entity_value, permutation)]
            return "Brand" in entities and "Sport" in entities

        rules = []
        for _, row in rules_data.iterrows():
            if pd.isna(row["Permutation"]):
                continue
            permutation = [item.strip() for item in row["Permutation"].split(",") if item.strip()]
            strategy = row["Strategy"] if not pd.isna(row["Strategy"]) else None
            rules.append({
                "permutation": permutation,
                "strategy": strategy
            })

        matched_rules = []
        for rule in rules:
            perm = rule["permutation"]
            strategy = rule["strategy"]
            if strategy is None:
                continue
            if not matches_query(perm):
                continue
            if not includes_brand_and_sport(perm):
                continue
            score = compute_score(perm)
            matched_rules.append({
                "Strategy": strategy,
                "Score": score,
                "Permutation": ", ".join(perm)
            })

        matched_rules = sorted(matched_rules, key=lambda x: x["Score"], reverse=True)
        st.success(f"✅ {len(matched_rules)} rule(s) matched your query.")
        st.dataframe(matched_rules, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ Error occurred: {e}")
