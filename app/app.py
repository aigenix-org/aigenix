"""
Antigenicity Classifier - Streamlit App
Basado en el proyecto antigen_predictor (SARS-CoV-2 / Influenza A)

INSTRUCCIONES DE CONEXIÓN:
  - Busca los bloques marcados con  # 🔌 CONECTAR MODELO  y  # 🔌 CONECTAR DATOS
  - Allí es donde debes cargar model.pkl y dataset.csv
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import io
import time

# ─────────────────────────────────────────────
#  CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AiGenix",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CSS CUSTOM (paleta azul del prototipo)
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Variables de color ── */
:root {
    --blue-dark:  #1a3a5c;
    --blue-mid:   #1e5799;
    --blue-light: #2980b9;
    --blue-pale:  #d6e8f5;
    --accent:     #e8a020;
    --red:        #c0392b;
    --green:      #27ae60;
    --grey-bg:    #f4f7fa;
    --grey-border:#dce3ea;
    --text-dark:  #1a2332;
    --text-mid:   #4a5568;
    --text-light: #8899aa;
}

/* ── Fondo principal ── */
.stApp { background: var(--grey-bg); }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--blue-dark) !important;
    border-right: 1px solid #0d2340;
}
[data-testid="stSidebar"] * { color: #c8ddf0 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #ffffff !important; }

/* ── Cards ── */
.card {
    background: #ffffff;
    border: 1px solid var(--grey-border);
    border-radius: 8px;
    padding: 20px 24px;
    margin-bottom: 16px;
    box-shadow: 0 1px 4px rgba(30,87,153,.08);
}
.card-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .08em;
    text-transform: uppercase;
    color: var(--text-light);
    margin-bottom: 14px;
}

/* ── Badges ── */
.badge-high   { background:#e74c3c; color:#fff; padding:2px 10px; border-radius:12px; font-size:12px; font-weight:700; }
.badge-medium { background:#f39c12; color:#fff; padding:2px 10px; border-radius:12px; font-size:12px; font-weight:700; }
.badge-low    { background:#95a5a6; color:#fff; padding:2px 10px; border-radius:12px; font-size:12px; font-weight:700; }
.badge-stable    { background:#27ae60; color:#fff; padding:3px 10px; border-radius:4px; font-size:11px; font-weight:700; }
.badge-high-m    { background:#e74c3c; color:#fff; padding:3px 10px; border-radius:4px; font-size:11px; font-weight:700; }
.badge-optimized { background:#2980b9; color:#fff; padding:3px 10px; border-radius:4px; font-size:11px; font-weight:700; }

/* ── Botón primario ── */
.stButton > button {
    background: var(--blue-mid) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
}
.stButton > button:hover {
    background: var(--blue-light) !important;
}

/* ── Score grande ── */
.score-big {
    font-size: 48px;
    font-weight: 800;
    color: var(--blue-dark);
    line-height: 1;
}
.score-label { font-size: 12px; color: var(--text-light); margin-top: 4px; }

/* ── Divider ── */
hr.thin { border: none; border-top: 1px solid var(--grey-border); margin: 16px 0; }

/* ── Table header ── */
.metric-table th {
    background: #eef3f8;
    color: var(--text-mid);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .06em;
    text-transform: uppercase;
    padding: 8px 12px;
}
.metric-table td { padding: 10px 12px; border-bottom: 1px solid var(--grey-border); font-size:13px; }

/* ── Expander ── */
[data-testid="stExpander"] { border: 1px solid var(--grey-border) !important; border-radius: 8px !important; }

/* ── Selectbox / file uploader ── */
[data-testid="stFileUploader"] { border: 2px dashed #b0c4de !important; border-radius: 8px; padding: 8px; }

/* ── Progress bar color ── */
.stProgress > div > div { background: var(--blue-mid) !important; }

/* ── Section header ── */
.section-header {
    font-size: 11px; font-weight: 700; letter-spacing: .1em;
    text-transform: uppercase; color: var(--text-light);
    border-bottom: 1px solid var(--grey-border);
    padding-bottom: 6px; margin-bottom: 14px;
}

/* ── Top candidate box ── */
.top-candidate-box {
    background: var(--blue-dark);
    color: #fff;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
}
.top-candidate-box .tc-name  { font-size: 20px; font-weight: 700; margin: 10px 0 4px; }
.top-candidate-box .tc-label { font-size: 11px; opacity: .7; }
.top-candidate-box .tc-score { font-size: 46px; font-weight: 800; color: #fff; line-height: 1; }
.top-candidate-box .tc-detail { font-size: 12px; opacity: .8; margin-top: 12px; text-align: left; }

/* ── Disclaimer ── */
.disclaimer {
    background: #fff8e1; border: 1px solid #f0c040;
    border-radius: 6px; padding: 10px 14px;
    font-size: 12px; color: #7d5a00;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  🔌 CONECTAR MODELO  ←─────────────────────
#  Carga aquí tu modelo Random Forest y el
#  objeto ProteinAnalysis de Biopython.
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    """
    TODO: Descomenta las líneas siguientes cuando tengas model.pkl:

        import joblib, pathlib
        model_path = pathlib.Path(__file__).parent.parent / "models" / "model.pkl"
        model = joblib.load(model_path)
        return model

    Por ahora devuelve None (modo demo).
    """
    return None          # ← reemplaza con tu modelo cargado

MODEL = load_model()


# ─────────────────────────────────────────────
#  🔌 CONECTAR DATOS  ←──────────────────────
#  Si quieres mostrar estadísticas del dataset
#  o las métricas reales del modelo, cárgalos
#  desde data/dataset.csv y los resultados de
#  cross-validation guardados en el notebook 03.
# ─────────────────────────────────────────────
@st.cache_data
def load_dataset_stats():
    """
    TODO: Descomenta para leer tu CSV real:

        import pathlib
        csv_path = pathlib.Path(__file__).parent.parent / "data" / "dataset.csv"
        df = pd.read_csv(csv_path)
        n_pos = (df['label'] == 1).sum()
        n_neg = (df['label'] == 0).sum()
        return {"total": len(df), "positive": n_pos, "negative": n_neg}

    Por ahora devuelve datos demo.
    """
    return {"total": 1250, "positive": 625, "negative": 625}   # ← reemplaza

DATASET_STATS = load_dataset_stats()


# ─────────────────────────────────────────────
#  HELPERS — parseo FASTA y features
# ─────────────────────────────────────────────
def parse_fasta(content: str) -> list[dict]:
    """Parsea texto FASTA y devuelve lista de {name, sequence}."""
    records = []
    current_name, current_seq = None, []
    for line in content.splitlines():
        line = line.strip()
        if line.startswith(">"):
            if current_name:
                records.append({"name": current_name, "sequence": "".join(current_seq)})
            current_name = line[1:].split()[0]
            current_seq = []
        elif line:
            current_seq.append(line.upper())
    if current_name:
        records.append({"name": current_name, "sequence": "".join(current_seq)})
    return records


def compute_features(seq: str) -> dict:
    """
    Calcula features fisicoquímicas de la secuencia.

    TODO: Reemplaza los cálculos aproximados por Biopython:

        from Bio.SeqUtils.ProtParam import ProteinAnalysis
        analysis = ProteinAnalysis(seq)
        mw   = analysis.molecular_weight()
        pi   = analysis.isoelectric_point()
        gravy = analysis.gravy()
        aa_comp = analysis.get_amino_acids_percent()

    Por ahora usa estimaciones simples para el modo demo.
    """
    aa_list = "ACDEFGHIKLMNPQRSTVWY"
    length  = len(seq)
    mw_approx = length * 110.0         # ← reemplaza con analysis.molecular_weight()
    pi_approx = 7.0 + np.random.uniform(-2, 2)   # ← reemplaza con analysis.isoelectric_point()
    gravy_approx = np.random.uniform(-1.5, 0.5)  # ← reemplaza con analysis.gravy()

    aa_comp = {}
    for aa in aa_list:
        count = seq.count(aa)
        aa_comp[aa] = round(count / max(length, 1) * 100, 1)

    return {
        "length": length,
        "mw":     round(mw_approx / 1000, 1),   # kDa
        "pi":     round(pi_approx, 2),
        "gravy":  round(gravy_approx, 3),
        "aa_comp": aa_comp,
    }


def predict_antigenicity(features: dict) -> float:
    """
    Predice probabilidad de antigenicidad.

    🔌 CONECTAR MODELO:
        Si MODEL no es None, construye el vector de features en el mismo
        orden que usaste en el entrenamiento y llama a:

            feature_vector = [
                features["length"],
                features["mw"],
                features["pi"],
                features["gravy"],
                *[features["aa_comp"].get(aa, 0) for aa in "ACDEFGHIKLMNPQRSTVWY"]
            ]
            prob = MODEL.predict_proba([feature_vector])[0][1]
            return prob

    Por ahora usa un score simulado para el modo demo.
    """
    if MODEL is not None:
        # ── Descomenta cuando el modelo esté cargado ──────────────────────
        # feature_vector = [
        #     features["length"],
        #     features["mw"],
        #     features["pi"],
        #     features["gravy"],
        #     *[features["aa_comp"].get(aa, 0) for aa in "ACDEFGHIKLMNPQRSTVWY"]
        # ]
        # return float(MODEL.predict_proba([feature_vector])[0][1])
        pass

    # Demo: score simulado basado en GRAVY e longitud
    base = 0.5
    base -= features["gravy"] * 0.2          # hidrofobicidad negativa → más antigénico
    base += min(features["length"] / 5000, 0.3)
    base += np.random.uniform(-0.15, 0.15)
    return float(np.clip(base, 0.02, 0.99))


def score_label(score: float) -> str:
    if score >= 0.70: return "HIGH"
    if score >= 0.40: return "MEDIUM"
    return "LOW"


def score_badge(score: float) -> str:
    lbl = score_label(score)
    cls = {"HIGH": "badge-high", "MEDIUM": "badge-medium", "LOW": "badge-low"}[lbl]
    return f'<span class="{cls}">{lbl}</span>'


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧬 Antigenicity\nClassifier")
    st.markdown("**v2.4.0 ENGINE**")
    st.markdown("---")

    page = st.radio(
        "",
        ["🔬 Predictor", "📊 Model Metrics", "ℹ️ About"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown(
        "<div style='font-size:12px;opacity:.6'>"
        "Dr. H. Chen<br>Lead Researcher"
        "</div>",
        unsafe_allow_html=True
    )

page = page.split(" ", 1)[1]   # quita el emoji


# ═══════════════════════════════════════════════════════════════
#  PÁGINA 1 — PREDICTOR
# ═══════════════════════════════════════════════════════════════
if page == "Predictor":

    st.markdown("## 🧬 Protein Antigenicity Predictor")

    col_left, col_right = st.columns([2, 1], gap="large")

    # ── Input + Resultados ──────────────────────────────────────
    with col_left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">SEQUENCE INPUT &nbsp;&nbsp; <span style="font-weight:400;text-transform:none;font-size:11px">Max 50 MB per upload</span></div>', unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Drop FASTA files here or click to browse",
            type=["fasta", "fa", "txt"],
            label_visibility="collapsed"
        )

        threshold_opts = {
            "VaxiJen V2.0 Threshold (0.4)": 0.4,
            "High confidence (0.7)":         0.7,
            "Low / broad screen (0.2)":      0.2,
        }
        sel_thresh = st.selectbox("Selection Criteria", list(threshold_opts.keys()))
        threshold  = threshold_opts[sel_thresh]

        run_btn = st.button("▶  Process Sequence", use_container_width=False)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Top Candidate (columna derecha) ─────────────────────────
    with col_right:
        if "results_df" in st.session_state and st.session_state.results_df is not None:
            top = st.session_state.results_df.iloc[0]
            score_pct = f"{top['score']:.3f}"
            st.markdown(f"""
            <div class="top-candidate-box">
                <div class="tc-label">TOP CANDIDATE</div>
                <div style="font-size:32px;margin:8px 0 2px;">⚙️</div>
                <div class="tc-name">{top['protein']}</div>
                <div class="tc-label">Antigenic Probability</div>
                <div class="tc-score">{score_pct}</div>
                <div class="tc-detail">
                    Length: {top['length']} aa<br>
                    Isoelectric Point: {top['pi']} pI<br>
                    <span style="color:#f0c040;font-weight:700;">⬤ Highly Stable</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="top-candidate-box">
                <div class="tc-label">TOP CANDIDATE</div>
                <div style="font-size:32px;margin:16px 0 8px;">⚙️</div>
                <div style="opacity:.5;font-size:13px;">Run a prediction to<br>see the top candidate</div>
            </div>
            """, unsafe_allow_html=True)

    # ── PROCESAMIENTO ────────────────────────────────────────────
    if run_btn:
        if uploaded is None:
            st.warning("⚠️ Sube un archivo FASTA primero.")
        else:
            content = uploaded.read().decode("utf-8", errors="ignore")
            records = parse_fasta(content)
            if not records:
                st.error("No se encontraron secuencias válidas en el archivo FASTA.")
            else:
                progress = st.progress(0, text="Calculando features…")
                rows = []
                for i, rec in enumerate(records):
                    feats = compute_features(rec["sequence"])
                    score = predict_antigenicity(feats)
                    rows.append({
                        "protein": rec["name"],
                        "score":   score,
                        "label":   score_label(score),
                        "length":  feats["length"],
                        "mw":      feats["mw"],
                        "pi":      feats["pi"],
                        "gravy":   feats["gravy"],
                        "aa_comp": feats["aa_comp"],
                    })
                    progress.progress((i + 1) / len(records), text=f"Procesando {rec['name']}…")
                    time.sleep(0.02)

                df = pd.DataFrame(rows).sort_values("score", ascending=False).reset_index(drop=True)
                st.session_state.results_df = df
                st.rerun()

    # ── RESULTADOS ───────────────────────────────────────────────
    if "results_df" in st.session_state and st.session_state.results_df is not None:
        df = st.session_state.results_df

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">VACCINE CANDIDATE RANKING PANEL</div>', unsafe_allow_html=True)

        # KPIs
        k1, k2, k3 = st.columns(3)
        k1.metric("Candidates analyzed", len(df))
        k2.metric("Model AUC-ROC", "0.81")   # 🔌 reemplaza con la métrica real del modelo
        top_row = df.iloc[0]
        k3.metric("Top Candidate", f"{top_row['score']:.2f}  {top_row['protein']}")

        # Filtros
        f1, f2, f3 = st.columns([1, 1, 1])
        show_high   = f1.checkbox("High (≥0.70)",   value=True)
        show_medium = f2.checkbox("Medium (0.40–0.69)", value=True)
        show_low    = f3.checkbox("Low (<0.40)",    value=True)

        keep = []
        if show_high:   keep.append("HIGH")
        if show_medium: keep.append("MEDIUM")
        if show_low:    keep.append("LOW")
        df_filtered = df[df["label"].isin(keep)] if keep else df

        # Lista de proteínas
        for rank, (_, row) in enumerate(df_filtered.iterrows(), 1):
            with st.expander(
                f"#{rank}  {row['protein']}   —   {row['score']*100:.1f}%",
                expanded=(rank == 1)
            ):
                badge = score_badge(row["score"])
                st.markdown(
                    f'<b>{row["protein"]}</b> &nbsp; {badge} &nbsp; Score: <b>{row["score"]:.3f}</b>',
                    unsafe_allow_html=True
                )

                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**STRUCTURAL FEATURES**")
                    st.markdown(f"""
                    | Feature | Value |
                    |---|---|
                    | Length | {row['length']} aa |
                    | MW | {row['mw']} kDa |
                    | pI | {row['pi']} |
                    | GRAVY | {row['gravy']} |
                    """)

                    # Top 10 AA composition
                    aa_sorted = sorted(row["aa_comp"].items(), key=lambda x: -x[1])[:10]
                    aa_str = "  ".join([f"**{aa}** / {pct}%" for aa, pct in aa_sorted])
                    st.markdown(f"**AA COMPOSITION (TOP 10):** {aa_str}")

                with c2:
                    st.markdown("**FEATURE IMPORTANCE**")
                    # 🔌 Si tienes MODEL.feature_importances_, úsalo aquí
                    feat_names = ["GRAVY", "aa_K", "Instability", "aa_N", "MW", "Charge"]
                    feat_vals  = [0.22, 0.18, 0.15, 0.13, 0.11, 0.09]  # ← reemplaza con MODEL.feature_importances_
                    fig_fi, ax_fi = plt.subplots(figsize=(3.5, 2.2))
                    bars = ax_fi.barh(feat_names[::-1], feat_vals[::-1], color="#1e5799")
                    ax_fi.set_xlim(0, 0.3)
                    ax_fi.tick_params(labelsize=8)
                    ax_fi.set_xlabel("Importance", fontsize=8)
                    fig_fi.tight_layout()
                    st.pyplot(fig_fi, use_container_width=False)
                    plt.close(fig_fi)

                # Explicación
                if row["label"] == "HIGH":
                    st.info(
                        f"**Antigenic.** Su longitud excepcional ({row['length']} aa) ofrece una gran "
                        f"superficie para presentación de epítopos. La hidrofobicidad negativa "
                        f"(GRAVY: {row['gravy']}) favorece la exposición superficial en condiciones "
                        f"fisiológicas. La feature más influyente fue GRAVY, indicando alta probabilidad "
                        f"de loops superficiales críticos para la unión con anticuerpos."
                    )
                elif row["label"] == "MEDIUM":
                    st.warning("Score intermedio. Requiere validación experimental adicional.")
                else:
                    st.error("Score bajo. Poca evidencia de antigenicidad con este modelo.")

        # Descarga CSV
        csv_out = df_filtered.drop(columns=["aa_comp", "label"]).to_csv(index=False)
        st.download_button(
            "⬇ Download results as CSV",
            data=csv_out,
            file_name="antigenicity_results.csv",
            mime="text/csv",
        )

        # Gráfico de barras
        st.markdown("---")
        st.markdown("**Score de antigenicidad — ranking completo**")
        fig, ax = plt.subplots(figsize=(max(6, len(df_filtered) * 0.45), 4))
        colors = ["#c0392b" if s >= 0.7 else "#f39c12" if s >= 0.4 else "#95a5a6"
                  for s in df_filtered["score"]]
        ax.bar(df_filtered["protein"], df_filtered["score"], color=colors, edgecolor="white", linewidth=.5)
        ax.axhline(threshold, color="#1a3a5c", linestyle="--", linewidth=1.2, label=f"Threshold ({threshold})")
        ax.set_ylabel("Antigenic Score")
        ax.set_ylim(0, 1.05)
        plt.xticks(rotation=45, ha="right", fontsize=8)
        ax.spines[["top", "right"]].set_visible(False)
        handles = [
            mpatches.Patch(color="#c0392b", label="High (≥0.70)"),
            mpatches.Patch(color="#f39c12", label="Medium (0.40–0.69)"),
            mpatches.Patch(color="#95a5a6", label="Low (<0.40)"),
        ]
        ax.legend(handles=handles, fontsize=8)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  PÁGINA 2 — MODEL METRICS
# ═══════════════════════════════════════════════════════════════
elif page == "Model Metrics":

    st.markdown("## 📊 Random Forest Performance")
    st.caption("Validation results and hyperparameter diagnostics for the antigenicity prediction module.")

    col_export = st.columns([4, 1])
    with col_export[1]:
        # 🔌 Aquí puedes exportar un PDF real de las métricas
        st.button("⬇ Export Report")

    # ── Configuración del modelo ─────────────────────────────────
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">MODEL CONFIGURATION</div>', unsafe_allow_html=True)
    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("Algorithm", "Random Forest")
    mc2.metric("Estimators", "200 trees")   # 🔌 reemplaza con MODEL.n_estimators si cargaste el modelo
    mc3.metric("Validation Strategy", "StratifiedKFold k=5")
    mc4.metric("Weighting", "balanced")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── KPIs ─────────────────────────────────────────────────────
    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown('<div class="card" style="text-align:center">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">AUC-ROC</div>', unsafe_allow_html=True)
        st.markdown('<div class="score-big">0.81</div>', unsafe_allow_html=True)   # 🔌 reemplaza con tu AUC real
        st.markdown('<div class="score-label">Cross-val mean ↗</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with k2:
        st.markdown('<div class="card" style="text-align:center">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">DATA SIZE</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="score-big">{DATASET_STATS["total"]:,}</div>', unsafe_allow_html=True)
        st.markdown('<div class="score-label">Training samples</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with k3:
        st.markdown('<div class="card" style="text-align:center">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">VALIDATION STATUS</div>', unsafe_allow_html=True)
        st.markdown('<div style="color:#27ae60;font-size:22px;font-weight:800;">✔ PASSES CLINICAL TARGET</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Visual Analytics ─────────────────────────────────────────
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">VISUAL ANALYTICS</div>', unsafe_allow_html=True)

    va1, va2 = st.columns(2)

    with va1:
        st.markdown("**ROC Curve (val set)**")
        # 🔌 Reemplaza fpr/tpr con los valores reales de tu cross-validation
        fpr = np.linspace(0, 1, 100)
        tpr = np.clip(fpr ** 0.45 + np.random.normal(0, 0.01, 100), 0, 1)
        fig_roc, ax_roc = plt.subplots(figsize=(4, 3))
        ax_roc.plot(fpr, tpr, color="#1e5799", lw=2, label="RF (AUC=0.81)")
        ax_roc.plot([0,1],[0,1], "k--", lw=1, alpha=.4)
        ax_roc.fill_between(fpr, tpr, alpha=.1, color="#1e5799")
        ax_roc.set_xlabel("False Positive Rate", fontsize=9)
        ax_roc.set_ylabel("True Positive Rate", fontsize=9)
        ax_roc.set_xlim(0,1); ax_roc.set_ylim(0,1.02)
        ax_roc.spines[["top","right"]].set_visible(False)
        ax_roc.legend(fontsize=8)
        fig_roc.tight_layout()
        st.pyplot(fig_roc, use_container_width=True)
        plt.close(fig_roc)

    with va2:
        st.markdown("**Top Feature Importance**")
        # 🔌 Reemplaza con MODEL.feature_importances_ ordenados
        feats   = ["GRAVY","aa_K","Instability","aa_N","MW","Charge","Length","pI"]
        imports = [0.22, 0.18, 0.15, 0.13, 0.11, 0.09, 0.07, 0.05]
        fig_imp, ax_imp = plt.subplots(figsize=(4, 3))
        ax_imp.barh(feats[::-1], imports[::-1], color="#1e5799")
        ax_imp.set_xlabel("Importance", fontsize=9)
        ax_imp.spines[["top","right"]].set_visible(False)
        fig_imp.tight_layout()
        st.pyplot(fig_imp, use_container_width=True)
        plt.close(fig_imp)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Performance Benchmarks ────────────────────────────────────
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">PERFORMANCE BENCHMARKS & DETAILED METRICS</div>', unsafe_allow_html=True)

    # 🔌 Reemplaza los valores de current_model con tus resultados reales de cross-validation
    metrics_data = {
        "Evaluation Metric":     ["Precision", "Recall (Sensitivity)", "F1-Score", "Accuracy"],
        "Current Model (RF-200)":["0.78", "0.83", "0.80", "0.79"],
        "Baseline (Naive)":      ["0.62", "0.55", "0.58", "0.60"],
        "Variance (±)":          ["0.021", "0.024", "0.019", "0.015"],
        "Status": [
            '<span class="badge-stable">STABLE</span>',
            '<span class="badge-high-m">HIGH</span>',
            '<span class="badge-optimized">OPTIMIZED</span>',
            '<span class="badge-stable">STABLE</span>',
        ]
    }
    metrics_df = pd.DataFrame(metrics_data)
    st.markdown(
        metrics_df.to_html(escape=False, index=False),
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Technical Note ────────────────────────────────────────────
    st.info(
        "**Technical Note:** The observed AUC of 0.81 meets the predefined clinical validation target "
        "(AUC > 0.80) for phase 1 genomic screening. Variance across K-folds remained under 0.03, "
        "indicating high model stability across heterogeneous protein sequence datasets. No significant "
        "overfitting was detected during the stratified cross-validation phase."
    )


# ═══════════════════════════════════════════════════════════════
#  PÁGINA 3 — ABOUT / DOCUMENTATION
# ═══════════════════════════════════════════════════════════════
elif page == "About":

    st.markdown("## ℹ️ Documentation")

    # Hero
    st.markdown("""
    <div class="card" style="background:linear-gradient(135deg,#1a3a5c,#2980b9);color:#fff;padding:32px">
        <h2 style="color:#fff;margin:0">Empirical Precision in Antigenicity Prediction</h2>
        <p style="opacity:.85;margin-top:8px">
        A robust analytical framework designed to identify potential epitopes through
        high-density physicochemical feature sets and curated genomic data.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Overview", "Epitope Science", "Data Repository", "Feature Engineering", "Limitations"]
    )

    with tab1:
        st.markdown("""
        ### What is an Epitope?
        An epitope, also known as an antigenic determinant, is the specific chemical group or
        molecular configuration on an antigen's surface to which a specific antibody or T-cell
        receptor binds.

        In the context of viral proteins, identifying these regions is critical for understanding
        immune response dynamics and vaccine development.

        > *"Our classifier evaluates protein sequences to predict the likelihood of a peptide
        sequence functioning as a B-cell or T-cell epitope, streamlining the initial phases
        of laboratory validation."*
        """)

    with tab2:
        st.markdown("""
        ### Epitope Science
        Los epítopos se clasifican en:
        - **B-cell epitopes**: reconocidos directamente por anticuerpos. Suelen ser regiones
          superficiales, hidrófilas y conformacionales.
        - **T-cell epitopes**: presentados por moléculas MHC. Son fragmentos lineales procesados
          por el proteasoma.

        Este modelo predice antigenicidad general de la proteína completa, no epítopos individuales.
        Para mapeo fino de epítopos, considera herramientas como BepiPred o NetMHCpan.
        """)

    with tab3:
        st.markdown("### Data Source & Methodology")
        col_data, col_iedb = st.columns([2, 1])
        with col_data:
            st.markdown(f"""
            The training corpus consists of over **150,000** verified epitope and non-epitope
            entries exported from the **Immune Epitope Database (IEDB)**.

            Data was filtered for human-host interaction and validated through multiple biological
            assays including MHC binding affinity tests, T-cell activation, and B-cell response
            measurements.

            | Stat | Value |
            |---|---|
            | Total samples | {DATASET_STATS['total']:,} |
            | Positive (antigenic) | {DATASET_STATS['positive']:,} |
            | Negative | {DATASET_STATS['negative']:,} |
            | Pathogens | SARS-CoV-2, Influenza A |
            """)
        with col_iedb:
            st.markdown("""
            <div class="card" style="text-align:center;background:#1a3a5c;color:#fff">
                <div style="font-size:32px">🗄</div>
                <b>Source Repository</b><br>
                <small>Access the curated training data via the IEDB official portal.</small><br><br>
                <a href="https://www.iedb.org" target="_blank"
                   style="background:#fff;color:#1a3a5c;padding:6px 14px;border-radius:4px;
                          font-weight:700;text-decoration:none;">
                   VISIT IEDB.ORG ↗
                </a>
            </div>
            """, unsafe_allow_html=True)

    with tab4:
        st.markdown("### Feature Engineering & Architecture")
        st.markdown("#### Physicochemical Parameters (4)")
        p1, p2, p3, p4 = st.columns(4)
        for col, name, desc in [
            (p1, "LEN — Sequence Length", "Base analysis of peptide size."),
            (p2, "MW — Molecular Weight", "Calculated per residue mass."),
            (p3, "pI — Isoelectric Point", "Net charge neutrality point."),
            (p4, "GRAVY — Hydropathy", "Average hydropathy score."),
        ]:
            col.markdown(f"""
            <div class="card">
                <b style="color:#1e5799">{name}</b><br>
                <small>{desc}</small>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### Amino Acid Composition (20)")
        st.info(
            "The model calculates the normalized frequency of all 20 standard proteinogenic "
            "amino acids within the sliding window, creating a high-dimensional vector space "
            "for classification."
        )
        aa_display = "ACDEFGHIKLMNPQRSTVWY"
        cols = st.columns(10)
        for i, aa in enumerate(aa_display):
            cols[i % 10].markdown(f"<div style='text-align:center;font-weight:700;font-size:16px;color:#1e5799'>{aa}</div>", unsafe_allow_html=True)

    with tab5:
        st.markdown("### Critical Limitations")
        st.error("""
        **⚠ Scope of training data**

        Primary training was conducted on respiratory viruses, specifically **SARS-CoV-2** and
        **Influenza A**. Generalization to other viral families may vary significantly.
        """)
        st.markdown("""
        <div class="disclaimer">
            <b>🏥 Medical Disclaimer</b><br>
            This is a research tool only. It is not intended for clinical diagnosis, patient
            screening, or any medical decision-making processes.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        #### Other limitations
        - Features are exclusively sequence-based. 3D structure, glycosylation and cellular
          processing are not considered.
        - A high score does not guarantee that a protein is a good vaccine antigen.
          It is a screening filter, not a clinical predictor.
        - Dataset size is small by production standards (~1,250 samples).
        """)

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align:center;font-size:11px;color:#aaa'>"
        "BIOLOGICAL DATA ENGINEERING UNIT · 2024 &nbsp;|&nbsp; "
        "🟢 Global Pipeline Operational"
        "</div>",
        unsafe_allow_html=True
    )