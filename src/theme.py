from urllib.parse import quote
import streamlit as st

OLIVE = "#556B2F"
BROWN = "#5C4033"
DARK = "#3E2A1F"
TAN = "#8A7355"


def _scene():
    p = []
    # Government building (dome, pediment, columns)
    p.append(f'<g transform="translate(-150,0)" fill="{BROWN}">')
    p.append('<rect x="600" y="385" width="500" height="15"/>')
    p.append('<rect x="620" y="370" width="460" height="15"/>')
    p.append('<rect x="640" y="355" width="420" height="15"/>')
    p.append('<rect x="560" y="290" width="100" height="65"/>')
    p.append('<rect x="1040" y="290" width="100" height="65"/>')
    p.append('<rect x="790" y="140" width="120" height="90"/>')
    p.append('<path d="M780 140 A70 70 0 0 1 920 140 Z"/>')
    p.append('<rect x="848" y="40" width="4" height="32"/>')
    p.append('<circle cx="850" cy="36" r="6"/>')
    p.append('<polygon points="650,230 850,185 1050,230"/>')
    p.append('<rect x="650" y="230" width="400" height="12"/>')
    p.append('<rect x="660" y="242" width="380" height="113"/>')
    for i in range(9):
        p.append(f'<rect x="{682+i*40}" y="250" width="16" height="105" fill="{TAN}"/>')
    p.append('</g>')
    # Scales of justice
    p.append(f'<g transform="translate(-250,0)" fill="{BROWN}" stroke="{BROWN}">')
    p.append('<rect x="1376" y="175" width="8" height="195" stroke="none"/>')
    p.append('<rect x="1340" y="370" width="80" height="14" stroke="none"/>')
    p.append('<circle cx="1380" cy="168" r="11" stroke="none"/>')
    p.append('<line x1="1290" y1="192" x2="1470" y2="192" stroke-width="6"/>')
    for cx in (1290, 1470):
        p.append(f'<line x1="{cx}" y1="192" x2="{cx-30}" y2="270" stroke-width="2"/>')
        p.append(f'<line x1="{cx}" y1="192" x2="{cx+30}" y2="270" stroke-width="2"/>')
        p.append(f'<path d="M{cx-40} 270 Q{cx} 310 {cx+40} 270 Z" stroke="none"/>')
    p.append('</g>')
    # Fort
    p.append(f'<g transform="translate(1260,0)" fill="{OLIVE}">')
    p.append('<rect x="0" y="300" width="340" height="100"/>')
    for x in range(0, 340, 34):
        p.append(f'<rect x="{x+4}" y="282" width="20" height="18"/>')
    for tx in (0, 250):
        p.append(f'<rect x="{tx}" y="190" width="90" height="210"/>')
        for k in range(4):
            p.append(f'<rect x="{tx+k*25}" y="172" width="15" height="18"/>')
        p.append(f'<path d="M{tx+38} 260 v24 h14 v-24 a7 7 0 0 0 -14 0 Z" fill="{DARK}"/>')
        p.append(f'<line x1="{tx+45}" y1="172" x2="{tx+45}" y2="135" stroke="{OLIVE}" stroke-width="3"/>')
        p.append(f'<polygon points="{tx+45},135 {tx+75},145 {tx+45},155"/>')
    p.append(f'<path d="M140 400 V350 A30 30 0 0 1 200 350 V400 Z" fill="{DARK}"/>')
    p.append('</g>')
    p.append(f'<rect x="0" y="392" width="1600" height="8" fill="{OLIVE}"/>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 400">'
            '<g opacity="0.17">' + "".join(p) + '</g></svg>')


CSS = """
<style>
.stApp {
    background-color: #F3EEDC;
    background-image: url("__BG__");
    background-repeat: no-repeat;
    background-position: bottom center;
    background-size: 100% auto;
    background-attachment: fixed;
}
.stApp, .stApp p, .stApp li, .stApp label, .stApp h1, .stApp h2,
.stApp h3, .stApp h4, .stApp input, .stApp textarea, .stApp button,
.stApp [data-baseweb="select"] div, [data-testid="stCaptionContainer"] {
    font-family: "Times New Roman", Times, serif !important;
}
.stApp p, .stApp li, .stApp label { font-size: 1.1rem; }
h1, h2, h3 { color: #3E2A1F !important; }
h1 { border-bottom: 3px double #556B2F; padding-bottom: 0.3rem; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #556B2F 0%, #3E4B1F 100%);
}
[data-testid="stSidebar"] * { color: #F3EEDC !important; }
.block-container {
    background: rgba(243, 238, 220, 0.88);
    border: 1px solid #C9BC93;
    border-radius: 12px;
    padding: 2rem 2.5rem !important;
    margin-top: 1rem;
}
.stButton > button {
    background: #5C4033; color: #F3EEDC; border: none;
    border-radius: 6px; padding: 0.5rem 1.5rem;
}
.stButton > button:hover { background: #556B2F; color: #F3EEDC; }
</style>
"""


def apply_theme():
    uri = "data:image/svg+xml;utf8," + quote(_scene())
    st.markdown(CSS.replace("__BG__", uri), unsafe_allow_html=True)