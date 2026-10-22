import os
import html
import streamlit as st
from src.ingest import load_and_chunk
from src.vectorstore import build_store, load_store
from src.chains import (
    summarize_policy, answer_question, compare_policies,
    analyze_impact, simplify_clause
)
from src.theme import apply_theme

POLICY_DIR = "data/policies"

# ---- EDIT THESE THREE LINES with your real details ----
STUDENT_NAME = "Afifa"
CLASS_NAME = "Prompt Engineering and LLM Application Development"
GUIDE_NAME = "Dr. M. Vijay"
# --------------------------------------------------------

DEFAULT_COMPARE_TOPICS = (
    "curriculum, examinations and assessment, technology and online "
    "learning, flexibility, funding and cost"
)

st.set_page_config(page_title="Education Policy Intelligence", layout="wide")
apply_theme()
st.markdown(
    """<style>
    .stApp, .stApp p, .stApp li, .stApp label, .stApp h1, .stApp h2,
    .stApp h3, .stApp h4, .stApp div, .stApp input, .stApp textarea,
    .stApp select, .stApp button, [data-testid="stSidebar"] *:not([data-testid="stIconMaterial"]),
    .chip, .home-title, .home-lead {
        font-family: "Times New Roman", Times, serif !important;
    }
    [data-testid="stIconMaterial"] {
        font-family: "Material Symbols Rounded" !important;
    }
    code, pre {
        font-family: monospace !important;
    }
    </style>""",
    unsafe_allow_html=True,
)
os.makedirs(POLICY_DIR, exist_ok=True)


def list_policies():
    return sorted(f for f in os.listdir(POLICY_DIR) if f.lower().endswith(".pdf"))


@st.cache_resource(show_spinner="Preparing policy index (first time only)...")
def get_store(filename):
    path = os.path.join("stores", os.path.splitext(filename)[0])
    if os.path.exists(path):
        return load_store(path)
    chunks = load_and_chunk(os.path.join(POLICY_DIR, filename))
    return build_store(chunks, persist_dir=path)


@st.cache_data(show_spinner="Reading policy...")
def get_summary_text(filename):
    chunks = load_and_chunk(os.path.join(POLICY_DIR, filename))
    # Short policies have fewer than 30 chunks, so fall back to the first 20.
    selected = chunks[10:30] if len(chunks) > 30 else chunks[:20]
    return " ".join(c.page_content for c in selected)


def show_json(obj):
    """Show the impact-analysis JSON in a readable way."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                st.markdown(f"**{key}**")
                show_json(value)
            else:
                st.markdown(f"**{key}:** {value}")
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, (dict, list)):
                show_json(item)
                st.divider()
            else:
                st.markdown(f"- {item}")
    else:
        st.write(obj)


# ------------------------------------------------------------------
# Home page
# ------------------------------------------------------------------
HOME_CSS = """<style>
.home-title{font-size:3rem;font-weight:700;line-height:1.12;letter-spacing:-0.01em;color:#2B2118;margin:0.5rem 0 0.8rem 0;}
.home-lead{font-size:1.25rem;line-height:1.55;color:#4A3520;max-width:34rem;margin:0 0 1.1rem 0;}
.chips{margin:0.4rem 0 0 0;}
.chip{display:inline-block;border:1px solid #B9AB7C;border-radius:4px;padding:0.1rem 0.6rem;margin:0 0.4rem 0.4rem 0;font-size:0.95rem;color:#4A3520;background:#FBF7EA;}
.chips-label{font-size:1rem;color:#6B4A2B;margin-bottom:0.35rem;}
.spec{background:#FBF7EA;border:1px solid #D2C6A0;border-left:6px solid #5F6B2E;border-radius:6px;padding:1.1rem 1.3rem;margin-top:0.8rem;}
.spec-label{font-size:0.9rem;color:#6B4A2B;margin-bottom:0.5rem;}
.spec-q{font-size:1.15rem;font-weight:700;color:#2B2118;margin-bottom:0.5rem;}
.spec-a{font-size:1.05rem;color:#2B2118;margin-bottom:0.9rem;}
.spec-src{background:#EFE7CC;border-radius:4px;padding:0.7rem 0.9rem;font-size:0.95rem;line-height:1.5;color:#4A3520;}
.spec-src-name{font-size:0.88rem;font-weight:700;color:#6B4A2B;margin-bottom:0.25rem;}
.sec{font-size:1.5rem;font-weight:700;color:#2B2118;margin:2.2rem 0 0.6rem 0;padding-top:0;}
.row{display:flex;gap:1.2rem;padding:0.75rem 0;border-bottom:1px solid #D2C6A0;}
.row-name{min-width:10rem;font-weight:700;color:#4A3520;}
.row-desc{color:#4A3520;line-height:1.5;}
.step{display:flex;gap:0.9rem;padding:0.6rem 0;}
.step-num{font-size:1.6rem;font-weight:700;color:#5F6B2E;min-width:1.6rem;line-height:1.2;}
.step-title{font-weight:700;color:#2B2118;}
.step-text{color:#4A3520;line-height:1.5;}
.foot{margin-top:2.5rem;padding-top:0.9rem;border-top:1px solid #B9AB7C;color:#6B4A2B;font-size:0.98rem;}
</style>"""

FEATURES = [
    ("Summarize", "Condense a long policy into its main points."),
    ("Ask Questions", "Get an answer with the passages it came from, so you can check it."),
    ("Compare Policies", "Put two policies side by side on the same topics."),
    ("Impact Analysis", "See how a policy affects students, teachers and institutions."),
    ("Explain Simply", "Turn a difficult clause into plain language."),
]

STEPS = [
    ("Retrieve", "The app searches the policy PDF for the passages that match your question."),
    ("Reason", "A structured prompt tells the model to use only those passages."),
    ("Check", "Ask Questions shows the passages behind each answer, so nothing has to be taken on trust."),
]


def render_home(policies):
    st.markdown(HOME_CSS, unsafe_allow_html=True)

    left, right = st.columns([3, 2], gap="large")

    with left:
        st.markdown(
            '<div class="home-title">AI-Powered Education Policy Intelligence</div>'
            '<div class="home-lead">Read, question, compare and explain Indian '
            'education policy, with every answer tied to the policy text.</div>',
            unsafe_allow_html=True,
        )
        if policies:
            chips = "".join(
                '<span class="chip">%s</span>'
                % html.escape(os.path.splitext(p)[0].replace("_", " "))
                for p in policies
            )
            st.markdown(
                '<div class="chips-label">%d policies loaded</div>'
                '<div class="chips">%s</div>' % (len(policies), chips),
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="chips-label">No policies loaded yet. '
                'Add a PDF on the Upload Policy page.</div>',
                unsafe_allow_html=True,
            )

    with right:
        st.markdown(
            '<div class="spec">'
            '<div class="spec-label">Example of an answer with its source</div>'
            '<div class="spec-q">What age group does the RTE Act cover?</div>'
            '<div class="spec-a">Children from six to fourteen years of age.</div>'
            '<div class="spec-src">'
            '<div class="spec-src-name">Passage used (RTE Act 2009, Section 3, summarised)</div>'
            'Every child aged six to fourteen has the right to free and '
            'compulsory education in a neighbourhood school until elementary '
            'education is complete.'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    feat_col, step_col = st.columns([1, 1], gap="large")

    with feat_col:
        st.markdown('<div class="sec">What you can do</div>', unsafe_allow_html=True)
        rows = "".join(
            '<div class="row"><div class="row-name">%s</div>'
            '<div class="row-desc">%s</div></div>' % (name, text)
            for name, text in FEATURES
        )
        st.markdown(rows, unsafe_allow_html=True)

    with step_col:
        st.markdown('<div class="sec">How an answer is made</div>', unsafe_allow_html=True)
        steps = "".join(
            '<div class="step"><div class="step-num">%d</div><div>'
            '<div class="step-title">%s</div>'
            '<div class="step-text">%s</div></div></div>' % (i, title, text)
            for i, (title, text) in enumerate(STEPS, 1)
        )
        st.markdown(steps, unsafe_allow_html=True)

    st.markdown(
        '<div class="foot">%s, %s. Guide: %s.</div>'
        % (html.escape(STUDENT_NAME), html.escape(CLASS_NAME), html.escape(GUIDE_NAME)),
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------------
# Navigation
# ------------------------------------------------------------------
PAGES = [
    "Home", "Upload Policy", "Summary", "Ask Questions",
    "Compare Policies", "Impact Analysis", "Explain Simply",
]
page = st.sidebar.radio("Navigate", PAGES)
policies = list_policies()

if page == "Home":
    render_home(policies)

elif page == "Upload Policy":
    st.header("Upload a policy PDF")
    file = st.file_uploader("Choose a PDF", type="pdf")
    if file and st.button("Save and index"):
        with open(os.path.join(POLICY_DIR, file.name), "wb") as f:
            f.write(file.getbuffer())
        get_store(file.name)
        st.success(f"{file.name} saved and indexed. Refresh the page to see it in the lists.")

elif not policies:
    st.warning("No policies found. Add a PDF on the Upload Policy page first.")

elif page == "Summary":
    st.header("Policy Summary")
    choice = st.selectbox("Policy", policies)
    if st.button("Summarize"):
        try:
            with st.spinner("Summarizing..."):
                st.markdown(summarize_policy(get_summary_text(choice)))
        except Exception as e:
            st.error(f"Could not summarize right now. Please try again in a minute. ({e})")

elif page == "Ask Questions":
    st.header("Ask a question")
    choice = st.selectbox("Policy", policies)
    question = st.text_input("Your question")
    if question and st.button("Get answer"):
        try:
            store = get_store(choice)
            with st.spinner("Searching the policy and writing an answer..."):
                docs = store.similarity_search(question, k=4)
                answer = answer_question(store, question)
            st.markdown(answer)
            with st.expander("Source passages used"):
                for i, d in enumerate(docs, 1):
                    page_no = d.metadata.get("page")
                    label = f"Passage {i}"
                    if isinstance(page_no, int):
                        label += f" (page {page_no + 1})"
                    st.markdown(f"**{label}**")
                    st.write(d.page_content)
        except Exception as e:
            st.error(f"Could not answer right now. Please try again in a minute. ({e})")

elif page == "Compare Policies":
    st.header("Compare two policies")
    col_a, col_b = st.columns(2)
    with col_a:
        name_a = st.selectbox("First policy", policies, index=0)
    with col_b:
        name_b = st.selectbox(
            "Second policy", policies, index=1 if len(policies) > 1 else 0
        )
    topics = st.text_input("Topics to compare", value=DEFAULT_COMPARE_TOPICS)
    if st.button("Compare"):
        if name_a == name_b:
            st.warning("Please choose two different policies.")
        else:
            try:
                with st.spinner("Finding the relevant passages in both policies..."):
                    store_a = get_store(name_a)
                    store_b = get_store(name_b)
                    docs_a = store_a.similarity_search(topics, k=6)
                    docs_b = store_b.similarity_search(topics, k=6)
                    text_a = "\n\n".join(d.page_content for d in docs_a)
                    text_b = "\n\n".join(d.page_content for d in docs_b)
                    label_a = os.path.splitext(name_a)[0].replace("_", " ")
                    label_b = os.path.splitext(name_b)[0].replace("_", " ")
                    result = compare_policies(label_a, text_a, label_b, text_b)
                st.markdown(result)
            except Exception as e:
                st.error(f"Could not compare right now. Please try again in a minute. ({e})")

elif page == "Impact Analysis":
    st.header("Impact analysis by stakeholder")
    choice = st.selectbox("Policy", policies)
    question = st.text_input(
        "Whose situation do you want to analyse?",
        value="How does this policy affect engineering and higher education students?",
    )
    if question and st.button("Analyse impact"):
        try:
            store = get_store(choice)
            with st.spinner("Analysing..."):
                result = analyze_impact(store, question)
            if isinstance(result, dict) and "raw" in result:
                st.info("The model did not return structured JSON, so the raw text is shown.")
                st.markdown(result["raw"])
            else:
                show_json(result)
                with st.expander("Show raw JSON"):
                    st.json(result)
        except Exception as e:
            st.error(f"Could not analyse right now. Please try again in a minute. ({e})")

elif page == "Explain Simply":
    st.header("Explain in simple language")
    clause = st.text_area("Paste a policy clause")
    if clause and st.button("Simplify"):
        try:
            with st.spinner("Simplifying..."):
                st.write(simplify_clause(clause))
        except Exception as e:
            st.error(f"Could not simplify right now. Please try again in a minute. ({e})")
