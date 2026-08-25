import streamlit as st
import fitz
import re
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="ResearchGraph AI",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 ResearchGraph AI")
st.write("AI-powered university research knowledge graph")

st.divider()

# -------------------------
# PDF UPLOAD
# -------------------------

st.subheader("📚 Upload Research Papers")

uploaded_files = st.file_uploader(
    "Choose research papers",
    type=["pdf"],
    accept_multiple_files=True
)


# -------------------------
# ENTITY DETECTION
# -------------------------

def detect_entities(text):

    text_lower = text.lower()

    topic_keywords = [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "data science",
        "computer vision",
        "natural language processing",
        "cyber security",
        "cybersecurity",
        "blockchain",
        "internet of things",
        "iot",
        "cloud computing",
        "data structures",
        "algorithms",
        "database",
        "programming",
        "software engineering"
    ]

    dataset_keywords = [
        "cifar-10",
        "cifar-100",
        "mnist",
        "imagenet",
        "kaggle",
        "uci",
        "iris dataset",
        "mimic",
        "plantvillage"
    ]

    method_keywords = [
        "neural network",
        "convolutional neural network",
        "cnn",
        "random forest",
        "decision tree",
        "support vector machine",
        "svm",
        "regression",
        "classification",
        "clustering",
        "k-means",
        "deep learning",
        "sorting",
        "searching",
        "linear search",
        "binary search"
    ]

    topics = []

    for keyword in topic_keywords:
        if keyword in text_lower:
            topics.append(keyword.title())

    datasets = []

    for keyword in dataset_keywords:
        if keyword in text_lower:
            datasets.append(keyword.upper())

    methods = []

    for keyword in method_keywords:
        if keyword in text_lower:
            methods.append(keyword.upper())

    # Researcher detection
    researcher_pattern = (
        r"\b(?:Dr\.|Prof\.|Professor)\s+"
        r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2}"
    )

    researchers = re.findall(
        researcher_pattern,
        text
    )

    researchers = list(dict.fromkeys(researchers))
    topics = list(dict.fromkeys(topics))
    datasets = list(dict.fromkeys(datasets))
    methods = list(dict.fromkeys(methods))

    return {
        "researchers": researchers,
        "topics": topics,
        "datasets": datasets,
        "methods": methods
    }


# -------------------------
# PROCESS MULTIPLE PAPERS
# -------------------------

if uploaded_files:

    st.success(
        f"{len(uploaded_files)} research paper(s) uploaded! ✅"
    )

    all_papers = {}

    # -------------------------
    # ANALYZE ALL PAPERS
    # -------------------------

    if st.button("🔍 Analyze All Research Papers"):

        for uploaded_file in uploaded_files:

            document = fitz.open(
                stream=uploaded_file.read(),
                filetype="pdf"
            )

            text = ""

            for page in document:
                text += page.get_text() + "\n"

            entities = detect_entities(text)

            all_papers[uploaded_file.name] = {
                "text": text,
                "entities": entities
            }

        st.session_state["all_papers"] = all_papers

        st.success(
            "All research papers analyzed successfully! ✅"
        )


# -------------------------
# DISPLAY RESULTS
# -------------------------

if "all_papers" in st.session_state:

    all_papers = st.session_state["all_papers"]

    st.divider()

    st.subheader("📚 Research Papers")

    for paper_name, paper_data in all_papers.items():

        st.write("### 📄 " + paper_name)

        entities = paper_data["entities"]

        col1, col2 = st.columns(2)

        with col1:

            st.write("👨‍🔬 **Researchers**")

            if entities["researchers"]:

                for researcher in entities["researchers"]:
                    st.write("• " + researcher)

            else:
                st.write("No researchers detected")

            st.write("🔬 **Research Topics**")

            if entities["topics"]:

                for topic in entities["topics"]:
                    st.write("• " + topic)

            else:
                st.write("No topics detected")

        with col2:

            st.write("🗃️ **Datasets**")

            if entities["datasets"]:

                for dataset in entities["datasets"]:
                    st.write("• " + dataset)

            else:
                st.write("No datasets detected")

            st.write("⚙️ **Methods**")

            if entities["methods"]:

                for method in entities["methods"]:
                    st.write("• " + method)

            else:
                st.write("No methods detected")


    # -------------------------
    # COMBINED KNOWLEDGE GRAPH
    # -------------------------

    st.divider()

    st.subheader("🕸️ Combined Research Knowledge Graph")

    G = nx.Graph()

    # -------------------------
    # ADD PAPERS AND ENTITIES
    # -------------------------

    for paper_name, paper_data in all_papers.items():

        entities = paper_data["entities"]

        # Paper node
        G.add_node(
            paper_name,
            type="paper"
        )

        # Researchers
        for researcher in entities["researchers"]:

            G.add_node(
                researcher,
                type="researcher"
            )

            G.add_edge(
                paper_name,
                researcher,
                relation="AUTHORED BY"
            )

        # Topics
        for topic in entities["topics"]:

            G.add_node(
                topic,
                type="topic"
            )

            G.add_edge(
                paper_name,
                topic,
                relation="STUDIES"
            )

        # Datasets
        for dataset in entities["datasets"]:

            G.add_node(
                dataset,
                type="dataset"
            )

            G.add_edge(
                paper_name,
                dataset,
                relation="USES DATASET"
            )

        # Methods
        for method in entities["methods"]:

            G.add_node(
                method,
                type="method"
            )

            G.add_edge(
                paper_name,
                method,
                relation="USES METHOD"
            )


    # -------------------------
    # CONNECT RELATED PAPERS
    # -------------------------

    paper_names = list(all_papers.keys())

    for i in range(len(paper_names)):

        for j in range(i + 1, len(paper_names)):

            paper_a = paper_names[i]
            paper_b = paper_names[j]

            entities_a = all_papers[paper_a]["entities"]
            entities_b = all_papers[paper_b]["entities"]

            shared_topics = (
                set(entities_a["topics"])
                & set(entities_b["topics"])
            )

            shared_methods = (
                set(entities_a["methods"])
                & set(entities_b["methods"])
            )

            shared_datasets = (
                set(entities_a["datasets"])
                & set(entities_b["datasets"])
            )

            shared_researchers = (
                set(entities_a["researchers"])
                & set(entities_b["researchers"])
            )

            total_shared = (
                len(shared_topics)
                + len(shared_methods)
                + len(shared_datasets)
                + len(shared_researchers)
            )

            if total_shared > 0:

                G.add_edge(
                    paper_a,
                    paper_b,
                    relation=f"RELATED ({total_shared})"
                )


    # -------------------------
    # DRAW GRAPH
    # -------------------------

    fig, ax = plt.subplots(
        figsize=(18, 12)
    )

    pos = nx.spring_layout(
        G,
        seed=42,
        k=2.5,
        iterations=150
    )

    paper_nodes = [
        n for n, d in G.nodes(data=True)
        if d.get("type") == "paper"
    ]

    researcher_nodes = [
        n for n, d in G.nodes(data=True)
        if d.get("type") == "researcher"
    ]

    topic_nodes = [
        n for n, d in G.nodes(data=True)
        if d.get("type") == "topic"
    ]

    dataset_nodes = [
        n for n, d in G.nodes(data=True)
        if d.get("type") == "dataset"
    ]

    method_nodes = [
        n for n, d in G.nodes(data=True)
        if d.get("type") == "method"
    ]

    # Paper nodes
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=paper_nodes,
        node_size=5000
    )

    # Researcher nodes
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=researcher_nodes,
        node_size=2800
    )

    # Topic nodes
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=topic_nodes,
        node_size=3000
    )

    # Dataset nodes
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=dataset_nodes,
        node_size=2800
    )

    # Method nodes
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=method_nodes,
        node_size=2800
    )

    # Edges
    nx.draw_networkx_edges(
        G,
        pos,
        width=1.5
    )

    # Labels
    nx.draw_networkx_labels(
        G,
        pos,
        font_size=8,
        font_weight="bold"
    )

    # Relationship labels
    edge_labels = nx.get_edge_attributes(
        G,
        "relation"
    )

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        font_size=6
    )

    ax.set_axis_off()

    st.pyplot(fig)


    # -------------------------
    # GRAPH STATISTICS
    # -------------------------

    st.divider()

    st.subheader("📊 Knowledge Graph Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Research Papers",
            len(all_papers)
        )

    with col2:

        st.metric(
            "Knowledge Nodes",
            G.number_of_nodes()
        )

    with col3:

        st.metric(
            "Relationships",
            G.number_of_edges()
        )


    # -------------------------
    # RELATED RESEARCH PAPERS
    # -------------------------

    st.divider()

    st.subheader("🔗 Related Research Papers")

    paper_names = list(all_papers.keys())

    if len(paper_names) >= 2:

        found_relationship = False

        for i in range(len(paper_names)):

            for j in range(i + 1, len(paper_names)):

                paper_a = paper_names[i]
                paper_b = paper_names[j]

                entities_a = all_papers[paper_a]["entities"]
                entities_b = all_papers[paper_b]["entities"]

                # Shared topics
                shared_topics = (
                    set(entities_a["topics"])
                    & set(entities_b["topics"])
                )

                # Shared methods
                shared_methods = (
                    set(entities_a["methods"])
                    & set(entities_b["methods"])
                )

                # Shared datasets
                shared_datasets = (
                    set(entities_a["datasets"])
                    & set(entities_b["datasets"])
                )

                # Shared researchers
                shared_researchers = (
                    set(entities_a["researchers"])
                    & set(entities_b["researchers"])
                )

                total_shared = (
                    len(shared_topics)
                    + len(shared_methods)
                    + len(shared_datasets)
                    + len(shared_researchers)
                )

                # Only show related papers
                if total_shared > 0:

                    found_relationship = True

                    st.write(
                        f"### 📄 {paper_a} ↔ 📄 {paper_b}"
                    )

                    if shared_topics:

                        st.write(
                            "**🔬 Shared Topics:** "
                            + ", ".join(
                                sorted(shared_topics)
                            )
                        )

                    if shared_methods:

                        st.write(
                            "**⚙️ Shared Methods:** "
                            + ", ".join(
                                sorted(shared_methods)
                            )
                        )

                    if shared_datasets:

                        st.write(
                            "**🗃️ Shared Datasets:** "
                            + ", ".join(
                                sorted(shared_datasets)
                            )
                        )

                    if shared_researchers:

                        st.write(
                            "**👨‍🔬 Shared Researchers:** "
                            + ", ".join(
                                sorted(shared_researchers)
                            )
                        )

                    # Relationship strength
                    if total_shared >= 5:

                        strength = "🟢 Very High"

                    elif total_shared >= 3:

                        strength = "🟡 High"

                    else:

                        strength = "🟠 Moderate"

                    st.write(
                        f"**🔗 Relationship Strength:** "
                        f"{strength}"
                    )

                    st.write(
                        f"**Shared Knowledge Elements:** "
                        f"{total_shared}"
                    )

                    st.divider()

        if not found_relationship:

            st.info(
                "No shared research entities were detected "
                "between the uploaded papers."
            )

    else:

        st.info(
            "Upload at least two research papers "
            "to compare them."
        )