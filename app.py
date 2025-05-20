import streamlit as st
import pandas as pd
import json

# --- Set page settings ---
st.set_page_config(page_title="Strategy Rule Matcher", page_icon="🎯")

st.title("🎯 Strategy Rule Matcher")
st.markdown("Match your query context against rules, with dropdown and slider-based inputs.")

st.header("🔧 Query Context")

# --- Predefined options for each entity ---
entity_options = {
    "Brand": ["Brand 1", "Brand 2"],
    "Sport": ["Basketball", "American Football"],
    "Competition": ["NBA", "NFL", "La Liga", "EPL"],
    "Incident": ["Points", "Assists", "Made Threes", "Rebounds", "Steals", "Blocks"],
    "Player or Team": ["S Curry", "J Brown", "Miami Heat", "Detroit Pistons"],
    "TimeBased": ["Live", "Pre Live", "30", "150", "360", "480", "600", "1440", "2880", "4320", "8640", "Q1", "Q2", "Q3", "Q4", "H1", "H2", "Match"],
    "Cohort": ["Cohort A", "Cohort B"]
}

# --- Default selections ---
default_query_context = {
    "Brand": "Brand 1",
    "Sport": "Basketball",
    "Competition": "NBA",
    "Incident": "Points",
    "Player or Team": "S Curry"
    "TimeBased": "150",
    "Cohort": "Cohort A"
}

# --- Query Context Dropdowns ---
query_context = {}
for entity, options in entity_options.items():
    selection = st.selectbox(
        f"{entity}:",
        options,
        index=options.index(default_query_context.get(entity, options[0]))
    )
    query_context[entity] = selection

# --- Entity Weightings with Sliders ---
st.header("⚖️ Entity Weightings")

default_weights = {
    "Brand": 1,
    "Sport": 1,
    "Competition": 5,
    "Incident": 7,
    "Player or Team": "10"
    "TimeBased": 15,
    "Cohort": 30
}

entity_weights = {}
for entity in entity_options.keys():
    weight = st.slider(
        f"Weight for {entity}",
        min_value=0,
        max_value=50,
        value=default_weights.get(entity, 1)
    )
    entity_weights[entity] = weight

# --- Rules (latest from user) ---
default_rules = pd.DataFrame({
    "Permutation": [
        "Brand:Brand 1, Sport:Basketball, Competition:NBA, Incident:Points",
        "Brand:Brand 1, Sport:Basketball, Competition:NBA, Incident:Points", "Player or Team:S Curry"
        "Brand:Brand 1, Sport:Basketball, Competition:NBA, Incident:Points","TimeBased:Match"
    ],
    "Strategy": [
        "strategy_001",
        "strategy_002",
        "strategy_003",
    ]
})

# --- Rule Editor ---
st.subheader("📋 Define Your Rules")
rules_data = st.data_editor(
    default_rules,
    use_container_width=True,
    num_rows="dynamic",
    height=450
)

# --- Run Matching ---
if st.button("▶️ Run Matching"):
    try:
        def extract_entity_value(entry):
            entity, value = entry.split(":", 1)
            return entity.strip(), value.strip()

        def compute_score(permutation):
            return sum(entity_weights.get(entity, 0) for entity, _ in map(extract_entity_value, permutation))

        # Match only if each entity:value in the rule matches the query context exactly
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

        st.success(f"✅ Found {len(matched_rules)} matching rule(s).")
        st.dataframe(matched_rules, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ An error occurred: {e}")
