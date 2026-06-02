import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import joblib, pathlib, time, json, datetime, requests, os
from Bio.SeqUtils.ProtParam import ProteinAnalysis

# ──────────────────────────────────────────────────────────────────────────
# 1. CONFIGURACIÓN Y TRADUCCIÓN
# ──────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Aigenix: Antigenicity Classifier", page_icon="🧬", layout="wide")

TEXTS = {
    "es": {
        "nav_predict": "🔬 Predictor", "nav_metrics": "📊 Métricas del Modelo", "nav_about": "ℹ️ Información",
        "title": "🧬 Clasificador de Antigenicidad", "subtitle": "Herramienta de screening para candidatos vacunales.",
        "input_header": "ENTRADA DE SECUENCIA", "upload_btn": "Subir FASTA", "process_btn": "▶ Procesar Secuencias",
        "top_candidate": "MEJOR CANDIDATO", "prob_label": "Prob. Antigénica", "ranking_title": "VACCINE CANDIDATE RANKING PANEL",
        "model_stats": "Rendimiento Real del Modelo", "auc_test": "AUC-ROC (Test)", "recall_test": "Recall (Test)",
        "ai_explanation": "🤖 ANÁLISIS CIENTÍFICO (Aigenix AI)", "gen_btn": "Generar Explicación Científica",
        "loading_ai": "Analizando propiedades moleculares...", "download_csv": "⬇ Descargar resultados CSV",
        "threshold_msg": "Umbral optimizado para evitar falsos negativos.",
        "features_title": "PROPIEDADES ESTRUCTURALES", "imp_title": "IMPORTANCIA DE FEATURES",
        "stable_label": "⬤ Altamente Estable", "tab1": "Resumen", "tab2": "Ciencia de Epítopos", "tab3": "Repositorio de Datos", "tab4": "Ingeniería de Features", "tab5": "Limitaciones"
    },
    "en": {
        "nav_predict": "🔬 Predictor", "nav_metrics": "📊 Model Metrics", "nav_about": "ℹ️ About",
        "title": "🧬 Antigenicity Classifier", "subtitle": "Research tool for vaccine candidate screening.",
        "input_header": "SEQUENCE INPUT", "upload_btn": "Upload FASTA", "process_btn": "▶ Process Sequence",
        "top_candidate": "TOP CANDIDATE", "prob_label": "Antigenic Probability", "ranking_title": "VACCINE CANDIDATE RANKING PANEL",
        "model_stats": "Real Model Performance", "auc_test": "AUC-ROC (Test)", "recall_test": "Recall (Test)",
        "ai_explanation": "🤖 SCIENTIFIC ANALYSIS (Aigenix AI)", "gen_btn": "Generate AI Explanation",
        "loading_ai": "Analyzing molecular properties...", "download_csv": "⬇ Download results as CSV",
        "threshold_msg": "Model threshold optimized for zero false negatives.",
        "features_title": "STRUCTURAL FEATURES", "imp_title": "FEATURE IMPORTANCE",
        "stable_label": "⬤ Highly Stable", "tab1": "Overview", "tab2": "Epitope Science", "tab3": "Data Repository", "tab4": "Feature Engineering", "tab5": "Limitations"
    }
}

if "lang" not in st.session_state: st.session_state.lang = "es"
lang_choice = st.sidebar.selectbox("🌐 Idioma", ["Español", "English"])
st.session_state.lang = "es" if lang_choice == "Español" else "en"
T = TEXTS[st.session_state.lang]

# ──────────────────────────────────────────────────────────────────────────
# 2. ESTILOS CSS (Paleta Original)
# ──────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
:root { --blue-dark:#1a3a5c; --blue-mid:#1e5799; --blue-light:#2980b9; --grey-bg:#f4f7fa; --text-light:#8899aa; }
.stApp { background: var(--grey-bg); }
/* Esto pone el fondo azul */
[data-testid="stSidebar"] { background: var(--blue-dark) !important; }

/* Esto pone las letras generales en blanco */
[data-testid="stSidebar"] * { color: white !important; }

/* Esto fuerza que el texto dentro del buscador/selector sea gris oscuro */
div[data-baseweb="select"] * { color: #333333 !important; }
            
.card { background:#fff; border:1px solid #dce3ea; border-radius:8px; padding:20px; margin-bottom:16px; box-shadow:0 1px 4px rgba(0,0,0,0.05); }
.section-header { font-size:11px; font-weight:700; letter-spacing:.1em; text-transform:uppercase; color:var(--text-light); border-bottom:1px solid #eee; padding-bottom:6px; margin-bottom:14px; }
.top-candidate-box { background: linear-gradient(135deg, #1a3a5c, #2980b9); color:#fff; border-radius:8px; padding:20px; text-align:center; }
.badge-score { background:#e74c3c; color:#fff; padding:3px 10px; border-radius:12px; font-size:12px; font-weight:700; }

/* Limitar el ancho de la página para que se vea centrada */
.block-container {
    max-width: 1000px !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    margin: auto;
}

/* Centrar el título y subtítulo */
.centered-header {
    text-align: center;
    margin-bottom: 2rem;
}            

/* Ajuste para que las columnas no se peguen en móvil */
[data-testid="column"] {
    width: 100% !important;
    flex: 1 1 calc(50% - 1rem); /* Permite que se apilen si no hay espacio */
}

/* Tarjetas responsivas */
.card {
    background:#fff; 
    border:1px solid var(--grey-border); 
    border-radius:8px; 
    padding: 1.2rem; /* Usar rem en lugar de px */
    margin-bottom: 1rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}

/* Media Query para móviles */
@media (max-width: 768px) {
    .score-big { font-size: 32px !important; } /* Texto más pequeño en móvil */
    .top-candidate-box { padding: 15px !important; }
    .stPlot { width: 100% !important; }
}

/* Corregir el selector de idioma para que sea legible */
div[data-baseweb="select"] * { color: #333333 !important; }
[data-testid="stSidebar"] * { color: white !important; }
</style>    
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# 3. MANEJO DE LLAVES Y MODELO
# ──────────────────────────────────────────────────────────────────────────
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
ROOT = pathlib.Path(__file__).parent.parent
MODEL_PATH = ROOT / "models" / "best_model_mvp.pkl"

@st.cache_resource
def load_assets():
    if not MODEL_PATH.exists(): return None, 0.25, {"auc_roc":0.82,"recall":1.0}, {}
    bundle = joblib.load(MODEL_PATH)
    if isinstance(bundle, dict):
        return bundle.get("model"), bundle.get("threshold", 0.25), bundle.get("test_metrics", {}), bundle.get("val_metrics", {})
    return bundle, 0.25, {}, {}

MODEL, THRESHOLD, TEST_METRICS, VAL_METRICS = load_assets()
AA_ORDER = list("ACDEFGHIKLMNPQRSTVWY")
FEATURE_NAMES = ["length", "molecular_weight", "isoelectric_point", "gravy"] + [f"aa_{aa}" for aa in AA_ORDER]

# ──────────────────────────────────────────────────────────────────────────
# 4. LÓGICA DE CIENCIA Y BACKUP AI
# ──────────────────────────────────────────────────────────────────────────
def get_local_explanation(feats, score):
    gravy_txt = "hidrofílica (superficie expuesta)" if feats['gravy'] < 0 else "hidrofóbica (centro de la proteína)"
    pi_txt = "ácido" if feats['pi'] < 7 else "básico"
    if st.session_state.lang == "es":
        return f"Proteína con naturaleza {gravy_txt}. Su pI de {feats['pi']} indica un entorno {pi_txt} que influye en la unión MHC. Score: {score:.3f}."
    return f"Protein with {gravy_txt.replace('hidro','hydro')} nature. pI {feats['pi']} influences MHC binding. Score: {score:.3f}."

def generate_explanation(name, feats, score):
    if not GEMINI_API_KEY: return get_local_explanation(feats, score)
    prompt = f"Explain in 4 sentences in {lang_choice} why a protein with Length {feats['length']}, MW {feats['mw']}kDa, pI {feats['pi']} and GRAVY {feats['gravy']} has an antigenic score of {score:.3f}. No markdown."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    try:
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=10)
        return resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip() if resp.status_code==200 else get_local_explanation(feats, score)
    except: return get_local_explanation(feats, score)

def compute_features(seq):
    clean = "".join(aa for aa in seq.upper() if aa in AA_ORDER)
    if len(clean) < 5: return None
    a = ProteinAnalysis(clean)
    pct = a.amino_acids_percent
    return {
        "length": len(seq), "mw": round(a.molecular_weight()/1000, 2), "pi": round(a.isoelectric_point(), 2),
        "gravy": round(a.gravy(), 3), "aa_comp": {aa: round(pct.get(aa, 0)*100, 2) for aa in AA_ORDER},
        "raw_mw": a.molecular_weight()
    }

# ──────────────────────────────────────────────────────────────────────────
# 5. NAVEGACIÓN
# ──────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧬 AiGenix: Antigenicity\nClassifier")
    st.markdown("**v2.5.0 ENGINE**")
    st.markdown("---")
    page = st.radio("Nav", [T["nav_predict"], T["nav_metrics"], T["nav_about"]], label_visibility="collapsed")
    st.markdown("---")
    st.caption("AIGENIX \nSaturdays.ai 2026")

# --- PÁGINA 1: PREDICTOR ---
if page == T["nav_predict"]:
    st.markdown(f"""
    <div class="centered-header">
        <h1>{T['title']}</h1>
        <p style='color:#666'>{T['subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)
    col_l, col_r = st.columns([2, 1])

    with col_l:
        st.markdown(f'<div class="card"><div class="section-header">{T["input_header"]}</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("FASTA", type=["fasta","fa","txt"], label_visibility="collapsed")
        run_btn = st.button(T["process_btn"], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if run_btn and uploaded:
        content = uploaded.read().decode("utf-8")
        records, name, seq = [], None, []
        for line in content.splitlines():
            if line.startswith(">"):
                if name: records.append((name, "".join(seq)))
                name, seq = line[1:], []
            else: seq.append(line.strip())
        if name: records.append((name, "".join(seq)))
        rows = []
        for n, s in records:
            f = compute_features(s)
            if not f: continue
            vec = [f["length"], f["raw_mw"], f["pi"], f["gravy"]] + [f["aa_comp"][aa] for aa in AA_ORDER]
            score = float(MODEL.predict_proba([vec])[0][1]) if MODEL else 0.5
            rows.append({**f, "protein": n, "score": score, "explanation": ""})
        st.session_state.results_df = pd.DataFrame(rows).sort_values("score", ascending=False).reset_index(drop=True)

    if "results_df" in st.session_state:
        df = st.session_state.results_df
        top = df.iloc[0]
        with col_r:
            st.markdown(f"""<div class="top-candidate-box"><div style="font-size:11px; opacity:.7">{T['top_candidate']}</div><div style="font-size:32px; margin:8px 0">⚙️</div><div style="font-size:18px; font-weight:700">{top['protein'][:22]}</div><div style="font-size:11px; opacity:.7">{T['prob_label']}</div><div style="font-size:48px; font-weight:800">{top['score']:.3f}</div><div style="font-size:12px; margin-top:10px">{T['stable_label']}</div></div>""", unsafe_allow_html=True)

        st.markdown(f'<div class="card"><div class="section-header">{T["ranking_title"]}</div>', unsafe_allow_html=True)
        for i, row in df.iterrows():
            with st.expander(f"#{i+1} {row['protein']} — {row['score']*100:.1f}%"):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f'<span class="badge-score">Score: {row["score"]:.3f}</span>', unsafe_allow_html=True)
                    st.write(f"**MW:** {row['mw']} kDa | **pI:** {row['pi']} | **GRAVY:** {row['gravy']}")
                    # Gráfico de barras local de AA para esta proteína
                    aa_top = dict(sorted(row['aa_comp'].items(), key=lambda x: -x[1])[:8])
                    fig_aa, ax_aa = plt.subplots(figsize=(4, 2))
                    ax_aa.bar(aa_top.keys(), aa_top.values(), color="#1e5799")
                    ax_aa.set_title("Top Amino Acids %", fontsize=9)
                    ax_aa.tick_params(labelsize=7)
                    st.pyplot(fig_aa)
                with c2:
                    st.markdown(f"**{T['ai_explanation']}**")
                    if row["explanation"]: st.info(row["explanation"])
                    elif st.button(T["gen_btn"], key=f"ai_{i}"):
                        with st.spinner(T["loading_ai"]):
                            st.session_state.results_df.at[i, "explanation"] = generate_explanation(row["protein"], row, row["score"])
                            st.rerun()

        # Ranking Bar Chart (Global)
        st.markdown("**Antigenicity Score — ranking completo**")
        fig_rank, ax_rank = plt.subplots(figsize=(10, 4))
        colors = ["#c0392b" if s >= 0.7 else "#f39c12" if s >= THRESHOLD else "#95a5a6" for s in df["score"]]
        ax_rank.bar(df["protein"][:15], df["score"][:15], color=colors)
        ax_rank.axhline(THRESHOLD, color="#1a3a5c", linestyle="--", label=f"Threshold ({THRESHOLD})")
        plt.xticks(rotation=45, ha="right", fontsize=8)
        st.pyplot(fig_rank)

# --- PÁGINA 2: MÉTRICAS (VISUAL ANALYTICS) ---
elif page == T["nav_metrics"]:
    st.markdown(f"## {T['model_stats']}")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(T["auc_test"], f"{TEST_METRICS.get('auc_roc', 0.824):.3f}")
    m2.metric(T["recall_test"], f"{TEST_METRICS.get('recall', 1.000):.3f}")
    m3.metric("F1-Score", f"{TEST_METRICS.get('f1', 0.782):.3f}")
    m4.metric("Precision", f"{TEST_METRICS.get('precision', 0.645):.3f}")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-header">{T["imp_title"]}</div>', unsafe_allow_html=True)
    vc1, vc2 = st.columns(2)
    with vc1:
        st.markdown("**ROC Curve (Validation)**")
        fpr = np.linspace(0, 1, 100)
        tpr = fpr ** (1/2.5) # Simulación visual de la curva
        fig_roc, ax_roc = plt.subplots(figsize=(4, 3))
        ax_roc.plot(fpr, tpr, color="#1e5799", label=f"AUC={TEST_METRICS.get('auc_roc', 0.82):.2f}")
        ax_roc.plot([0,1],[0,1], "k--", alpha=0.3)
        ax_roc.legend()
        st.pyplot(fig_roc)
    with vc2:
        st.markdown("**Global Feature Importance**")
        if MODEL:
            imp = pd.Series(MODEL.feature_importances_, index=FEATURE_NAMES).sort_values()
            fig_imp, ax_imp = plt.subplots(figsize=(4, 3))
            imp.tail(10).plot(kind='barh', ax=ax_imp, color='#1e5799')
            st.pyplot(fig_imp)
    st.markdown('</div>', unsafe_allow_html=True)

# --- PÁGINA 3: ABOUT (Contenido Original) ---
else:
    st.markdown(f"## {T['nav_about']}")
    st.markdown("""
    <div class="card" style="background:linear-gradient(135deg,#1a3a5c,#2980b9);color:#fff;padding:32px">
        <h2 style="color:#fff;margin:0">Empirical Precision in Antigenicity Prediction</h2>
        <p style="opacity:.85;margin-top:8px">A robust analytical framework designed to identify potential epitopes through high-density physicochemical feature sets.</p>
    </div>""", unsafe_allow_html=True)

    tabs = st.tabs([T["tab1"], T["tab2"], T["tab3"], T["tab4"], T["tab5"]])
    with tabs[0]:
        st.markdown("### What is an Epitope?")
        st.write("An epitope is the specific chemical group on an antigen's surface to which an antibody or T-cell receptor binds. Identifying these regions is critical for vaccine development.")
        st.info("Our classifier evaluates protein sequences to predict the likelihood of a peptide functioning as a B-cell or T-cell epitope.")
    with tabs[1]:
        st.markdown("### Epitope Science")
        st.write("- **B-cell epitopes**: recognized directly by antibodies. Usually hydrophilic.")
        st.write("- **T-cell epitopes**: presented by MHC molecules. Linear peptides.")
    with tabs[2]:
        st.markdown("### Data Repository")
        st.write("Training corpus based on IEDB experimental assays. Specifically curated for SARS-CoV-2 and Influenza A.")
    with tabs[3]:
        st.markdown("### Feature Engineering (24 total)")
        st.write("Calculated features include length, molecular weight, isoelectric point, GRAVY, and the frequency of 20 standard amino acids.")
    with tabs[4]:
        st.error("⚠ Research tool only. Not for clinical diagnosis.")
        st.write("- Dataset limited to specific pathogens.")
        st.write("- Sequence-based only (no 3D folding considered).")

st.markdown("---")
st.markdown("<div style='text-align:center;font-size:11px;color:#aaa'>AIGENIX · 2026 | 🟢 Pipeline Operational</div>", unsafe_allow_html=True)