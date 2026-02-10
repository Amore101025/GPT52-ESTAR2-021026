import os
import random
import time
from dataclasses import dataclass
from typing import Dict, Any, List

import streamlit as st


# =========================
# Page / App Bootstrap
# =========================
st.set_page_config(
    page_title="FormAgent AI — WOW UI",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# i18n (EN / Traditional Chinese)
# =========================
I18N: Dict[str, Dict[str, str]] = {
    "en": {
        "app_title": "FormAgent AI",
        "app_subtitle": "WOW UI • Agent Studio • Note Keeper • Dashboard",
        "theme": "Theme",
        "light": "Light",
        "dark": "Dark",
        "language": "Language",
        "english": "English",
        "zh_tw": "Traditional Chinese",
        "style": "Painter Style",
        "jackpot": "Jackpot",
        "lock_style": "Lock style",
        "style_locked_help": "When enabled, Jackpot cannot change the current style.",
        "status": "Status",
        "provider_health": "Provider Health",
        "configured": "Configured",
        "missing": "Missing",
        "session": "Session",
        "api_keys": "API Keys",
        "keys_desc": "Environment keys are never shown. If missing, you may provide a key for this session only.",
        "from_env": "From ENV",
        "from_session": "From Session",
        "not_set": "Not Set",
        "enter_key": "Enter API key",
        "save_key": "Save (session)",
        "clear_key": "Clear (session)",
        "forms_tab": "FormAgent (Forms)",
        "agent_tab": "Agent Studio",
        "note_tab": "AI Note Keeper",
        "dash_tab": "Dashboard",
        "ui_controls": "UI Controls",
        "quick_actions": "Quick Actions",
        "pipeline_state": "Pipeline State",
        "idle": "Idle",
        "running": "Running",
        "awaiting_edit": "Awaiting Edit",
        "completed": "Completed",
        "error": "Error",
        "demo_hint": "This file focuses on the WOW UI shell (theme, i18n, painter styles, Jackpot). Feature panels are scaffolded based on the prior design.",
        "forms_scaffold_title": "Forms Workspace (Scaffold)",
        "forms_scaffold_body": "Preserved features: Raw Document / PDF Spec ingestion, schema preview, python/jsPDF artifacts. Implement the agent execution in Agent Studio.",
        "agent_scaffold_title": "Agent Studio (Scaffold)",
        "agent_scaffold_body": "Step-by-step agents.yaml execution with per-step model/prompt/max_tokens controls and editable outputs feeding the next step.",
        "note_scaffold_title": "AI Note Keeper (Scaffold)",
        "note_scaffold_body": "Paste notes → organize into Markdown with coral keywords; editable markdown/text; 6 AI Magics including AI Keywords with custom colors.",
        "dash_scaffold_title": "Dashboard (Scaffold)",
        "dash_scaffold_body": "WOW indicators: step timeline, token/cost estimates, provider readiness, artifact readiness, and run report export.",
        "footer": "Deployed on Hugging Face Spaces • Streamlit UI shell • Multi-provider APIs",
    },
    "zh-TW": {
        "app_title": "FormAgent AI",
        "app_subtitle": "WOW 介面 • Agent Studio • 筆記管家 • 儀表板",
        "theme": "主題",
        "light": "淺色",
        "dark": "深色",
        "language": "語言",
        "english": "English",
        "zh_tw": "繁體中文",
        "style": "畫家風格",
        "jackpot": "幸運抽選",
        "lock_style": "鎖定風格",
        "style_locked_help": "啟用後，幸運抽選不會改變目前風格。",
        "status": "狀態",
        "provider_health": "供應商健康狀態",
        "configured": "已設定",
        "missing": "缺少",
        "session": "本次工作階段",
        "api_keys": "API 金鑰",
        "keys_desc": "環境變數中的金鑰永遠不會顯示。若缺少，可僅針對本次工作階段輸入金鑰。",
        "from_env": "來自環境變數",
        "from_session": "來自工作階段",
        "not_set": "未設定",
        "enter_key": "輸入 API 金鑰",
        "save_key": "儲存（僅本次）",
        "clear_key": "清除（僅本次）",
        "forms_tab": "FormAgent（表單）",
        "agent_tab": "Agent Studio",
        "note_tab": "AI 筆記管家",
        "dash_tab": "儀表板",
        "ui_controls": "介面控制",
        "quick_actions": "快速操作",
        "pipeline_state": "流程狀態",
        "idle": "閒置",
        "running": "執行中",
        "awaiting_edit": "等待編輯",
        "completed": "完成",
        "error": "錯誤",
        "demo_hint": "此檔案重點為 WOW UI 外殼（主題、語言、畫家風格、幸運抽選）。其餘功能依照先前設計以骨架方式呈現。",
        "forms_scaffold_title": "表單工作區（骨架）",
        "forms_scaffold_body": "保留功能：Raw Document / PDF Spec 輸入、Schema 預覽、Python/jsPDF 產物。建議在 Agent Studio 實作逐步代理執行。",
        "agent_scaffold_title": "Agent Studio（骨架）",
        "agent_scaffold_body": "逐步執行 agents.yaml：每步可調模型/提示詞/max_tokens，並可編輯輸出再餵給下一步。",
        "note_scaffold_title": "AI 筆記管家（骨架）",
        "note_scaffold_body": "貼上筆記→整理為 Markdown 並以珊瑚色標出關鍵字；可編輯 markdown/text；內建 6 種 AI 魔法含 AI Keywords（自訂顏色）。",
        "dash_scaffold_title": "儀表板（骨架）",
        "dash_scaffold_body": "WOW 指標：步驟時間線、token/成本估計、供應商就緒狀態、產物就緒狀態與執行報告匯出。",
        "footer": "部署於 Hugging Face Spaces • Streamlit 介面外殼 • 多供應商 API",
    },
}


def t(key: str) -> str:
    lang = st.session_state.get("lang", "en")
    return I18N.get(lang, I18N["en"]).get(key, key)


# =========================
# Painter Styles (20)
# =========================
@dataclass(frozen=True)
class PainterStyle:
    name: str
    accent: str
    accent2: str
    bg: str
    panel: str
    text: str
    subtle_text: str
    border: str
    code_bg: str
    paper: str
    paper_border: str
    glow: str


PAINTER_STYLES: Dict[str, PainterStyle] = {
    "Claude Monet": PainterStyle(
        name="Claude Monet",
        accent="#4f8a8b",
        accent2="#a7c5bd",
        bg="#f7fbfb",
        panel="#ffffff",
        text="#0f172a",
        subtle_text="#475569",
        border="#dbeafe",
        code_bg="#0b1220",
        paper="#fbfeff",
        paper_border="#cfe8ea",
        glow="rgba(79,138,139,0.25)",
    ),
    "Vincent van Gogh": PainterStyle(
        name="Vincent van Gogh",
        accent="#1d4ed8",
        accent2="#f59e0b",
        bg="#fff7ed",
        panel="#ffffff",
        text="#111827",
        subtle_text="#4b5563",
        border="#fde68a",
        code_bg="#0b1220",
        paper="#fffdf7",
        paper_border="#fcd34d",
        glow="rgba(245,158,11,0.25)",
    ),
    "Pablo Picasso": PainterStyle(
        name="Pablo Picasso",
        accent="#ef4444",
        accent2="#3b82f6",
        bg="#fafafa",
        panel="#ffffff",
        text="#0f172a",
        subtle_text="#475569",
        border="#e5e7eb",
        code_bg="#0b1220",
        paper="#ffffff",
        paper_border="#d1d5db",
        glow="rgba(239,68,68,0.18)",
    ),
    "Leonardo da Vinci": PainterStyle(
        name="Leonardo da Vinci",
        accent="#7c3aed",
        accent2="#a16207",
        bg="#fbf7ef",
        panel="#ffffff",
        text="#1f2937",
        subtle_text="#6b7280",
        border="#e7d7bf",
        code_bg="#0b1220",
        paper="#fffdf8",
        paper_border="#e7d7bf",
        glow="rgba(124,58,237,0.18)",
    ),
    "Rembrandt": PainterStyle(
        name="Rembrandt",
        accent="#b45309",
        accent2="#92400e",
        bg="#0b0a09",
        panel="#121212",
        text="#f8fafc",
        subtle_text="#cbd5e1",
        border="#292524",
        code_bg="#05070d",
        paper="#151311",
        paper_border="#3f2d1d",
        glow="rgba(180,83,9,0.22)",
    ),
    "Johannes Vermeer": PainterStyle(
        name="Johannes Vermeer",
        accent="#2563eb",
        accent2="#fbbf24",
        bg="#f8fafc",
        panel="#ffffff",
        text="#0f172a",
        subtle_text="#475569",
        border="#dbeafe",
        code_bg="#0b1220",
        paper="#ffffff",
        paper_border="#c7d2fe",
        glow="rgba(37,99,235,0.16)",
    ),
    "Gustav Klimt": PainterStyle(
        name="Gustav Klimt",
        accent="#d97706",
        accent2="#f59e0b",
        bg="#0b0a08",
        panel="#141210",
        text="#fff7ed",
        subtle_text="#fed7aa",
        border="#3b2f1c",
        code_bg="#05070d",
        paper="#171512",
        paper_border="#5b431d",
        glow="rgba(245,158,11,0.24)",
    ),
    "Edvard Munch": PainterStyle(
        name="Edvard Munch",
        accent="#dc2626",
        accent2="#0ea5e9",
        bg="#0b1220",
        panel="#0f172a",
        text="#f8fafc",
        subtle_text="#cbd5e1",
        border="#1f2a44",
        code_bg="#05070d",
        paper="#0b1325",
        paper_border="#243152",
        glow="rgba(220,38,38,0.20)",
    ),
    "Salvador Dalí": PainterStyle(
        name="Salvador Dalí",
        accent="#8b5cf6",
        accent2="#22c55e",
        bg="#fdf4ff",
        panel="#ffffff",
        text="#0f172a",
        subtle_text="#475569",
        border="#f5d0fe",
        code_bg="#0b1220",
        paper="#ffffff",
        paper_border="#f5d0fe",
        glow="rgba(139,92,246,0.18)",
    ),
    "Frida Kahlo": PainterStyle(
        name="Frida Kahlo",
        accent="#16a34a",
        accent2="#dc2626",
        bg="#f0fdf4",
        panel="#ffffff",
        text="#0f172a",
        subtle_text="#475569",
        border="#bbf7d0",
        code_bg="#0b1220",
        paper="#ffffff",
        paper_border="#86efac",
        glow="rgba(22,163,74,0.18)",
    ),
    "Georgia O’Keeffe": PainterStyle(
        name="Georgia O’Keeffe",
        accent="#0ea5e9",
        accent2="#f97316",
        bg="#fff7ed",
        panel="#ffffff",
        text="#111827",
        subtle_text="#4b5563",
        border="#fed7aa",
        code_bg="#0b1220",
        paper="#fffdf8",
        paper_border="#ffd2a6",
        glow="rgba(14,165,233,0.16)",
    ),
    "Wassily Kandinsky": PainterStyle(
        name="Wassily Kandinsky",
        accent="#2563eb",
        accent2="#ef4444",
        bg="#f8fafc",
        panel="#ffffff",
        text="#0f172a",
        subtle_text="#475569",
        border="#e2e8f0",
        code_bg="#0b1220",
        paper="#ffffff",
        paper_border="#e2e8f0",
        glow="rgba(37,99,235,0.16)",
    ),
    "Jackson Pollock": PainterStyle(
        name="Jackson Pollock",
        accent="#111827",
        accent2="#f59e0b",
        bg="#0a0a0a",
        panel="#111111",
        text="#f9fafb",
        subtle_text="#d1d5db",
        border="#262626",
        code_bg="#05070d",
        paper="#121212",
        paper_border="#2a2a2a",
        glow="rgba(245,158,11,0.18)",
    ),
    "Andy Warhol": PainterStyle(
        name="Andy Warhol",
        accent="#ec4899",
        accent2="#22c55e",
        bg="#fff1f2",
        panel="#ffffff",
        text="#111827",
        subtle_text="#4b5563",
        border="#fecdd3",
        code_bg="#0b1220",
        paper="#ffffff",
        paper_border="#fecdd3",
        glow="rgba(236,72,153,0.18)",
    ),
    "Henri Matisse": PainterStyle(
        name="Henri Matisse",
        accent="#0ea5e9",
        accent2="#f97316",
        bg="#f0f9ff",
        panel="#ffffff",
        text="#0f172a",
        subtle_text="#475569",
        border="#bae6fd",
        code_bg="#0b1220",
        paper="#ffffff",
        paper_border="#7dd3fc",
        glow="rgba(249,115,22,0.16)",
    ),
    "Paul Cézanne": PainterStyle(
        name="Paul Cézanne",
        accent="#10b981",
        accent2="#f59e0b",
        bg="#f7fee7",
        panel="#ffffff",
        text="#0f172a",
        subtle_text="#475569",
        border="#d9f99d",
        code_bg="#0b1220",
        paper="#ffffff",
        paper_border="#bef264",
        glow="rgba(16,185,129,0.16)",
    ),
    "Pierre-Auguste Renoir": PainterStyle(
        name="Pierre-Auguste Renoir",
        accent="#fb7185",
        accent2="#60a5fa",
        bg="#fff1f2",
        panel="#ffffff",
        text="#111827",
        subtle_text="#4b5563",
        border="#fecdd3",
        code_bg="#0b1220",
        paper="#ffffff",
        paper_border="#fecdd3",
        glow="rgba(251,113,133,0.18)",
    ),
    "Caravaggio": PainterStyle(
        name="Caravaggio",
        accent="#f97316",
        accent2="#a3e635",
        bg="#070707",
        panel="#101010",
        text="#f8fafc",
        subtle_text="#cbd5e1",
        border="#1f1f1f",
        code_bg="#05070d",
        paper="#0f0f0f",
        paper_border="#2a2a2a",
        glow="rgba(249,115,22,0.20)",
    ),
    "J.M.W. Turner": PainterStyle(
        name="J.M.W. Turner",
        accent="#38bdf8",
        accent2="#fbbf24",
        bg="#f0f9ff",
        panel="#ffffff",
        text="#0f172a",
        subtle_text="#475569",
        border="#bae6fd",
        code_bg="#0b1220",
        paper="#ffffff",
        paper_border="#93c5fd",
        glow="rgba(56,189,248,0.18)",
    ),
    "Hokusai": PainterStyle(
        name="Hokusai",
        accent="#2563eb",
        accent2="#06b6d4",
        bg="#eff6ff",
        panel="#ffffff",
        text="#0f172a",
        subtle_text="#475569",
        border="#bfdbfe",
        code_bg="#0b1220",
        paper="#ffffff",
        paper_border="#bfdbfe",
        glow="rgba(6,182,212,0.16)",
    ),
}

STYLE_NAMES: List[str] = list(PAINTER_STYLES.keys())


# =========================
# Session State Initialization
# =========================
def init_state() -> None:
    ss = st.session_state
    ss.setdefault("lang", "en")
    ss.setdefault("theme_mode", "light")  # light | dark
    ss.setdefault("style_name", "Claude Monet")
    ss.setdefault("style_locked", False)

    # Pipeline status scaffolding
    ss.setdefault("pipeline_status", "idle")  # idle|running|awaiting_edit|completed|error
    ss.setdefault("pipeline_step", 0)
    ss.setdefault("pipeline_total_steps", 6)
    ss.setdefault("last_latency_ms", None)

    # Provider keys in session (NEVER show env keys)
    ss.setdefault("session_keys", {
        "GEMINI_API_KEY": "",
        "OPENAI_API_KEY": "",
        "ANTHROPIC_API_KEY": "",
        "GROK_API_KEY": "",
    })


init_state()


# =========================
# WOW CSS Theming via CSS Variables
# =========================
def apply_wow_css(theme_mode: str, style: PainterStyle) -> None:
    """
    Streamlit doesn't support perfect runtime theme swapping like a SPA,
    but we can achieve a strong WOW effect via CSS variables + custom classes.
    """
    # Theme-aware overrides: when user selects dark, ensure backgrounds are darker.
    # Some painter styles are already dark; for light-only styles, we adjust gently.
    is_dark = (theme_mode == "dark")

    bg = style.bg
    panel = style.panel
    text = style.text
    subtle = style.subtle_text
    border = style.border
    code_bg = style.code_bg
    paper = style.paper
    paper_border = style.paper_border

    if is_dark:
        # If the selected style is light, enforce a dark base while keeping accents.
        # (We detect "light" by checking panel brightness heuristically via known defaults.)
        # This is a design-level adjustment; keep it simple and consistent.
        if panel.lower() in ["#ffffff", "#fffdf8", "#fffdf7", "#fbfeff"]:
            bg = "#0b1220"
            panel = "#0f172a"
            text = "#f8fafc"
            subtle = "#cbd5e1"
            border = "#243152"
            code_bg = "#05070d"
            paper = "#0b1325"
            paper_border = "#243152"

    css = f"""
    <style>
      :root {{
        --wow-accent: {style.accent};
        --wow-accent-2: {style.accent2};
        --wow-bg: {bg};
        --wow-panel: {panel};
        --wow-text: {text};
        --wow-subtle: {subtle};
        --wow-border: {border};
        --wow-code-bg: {code_bg};
        --wow-paper: {paper};
        --wow-paper-border: {paper_border};
        --wow-glow: {style.glow};
        --wow-coral: #FF7F50; /* coral for keyword highlights */
      }}

      /* Global background */
      .stApp {{
        background: var(--wow-bg);
        color: var(--wow-text);
      }}

      /* Reduce Streamlit default padding a bit for a tighter "tool" feel */
      .block-container {{
        padding-top: 1.0rem;
        padding-bottom: 2.2rem;
      }}

      /* Headline styling */
      .wow-title {{
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0;
        line-height: 1.05;
      }}
      .wow-subtitle {{
        margin: 0.15rem 0 0 0;
        color: var(--wow-subtle);
        font-weight: 500;
      }}

      /* "Topbar" card */
      .wow-topbar {{
        border: 1px solid var(--wow-border);
        background: linear-gradient(120deg, rgba(255,255,255,0.04), rgba(0,0,0,0.02));
        border-radius: 16px;
        padding: 14px 16px;
        box-shadow: 0 10px 30px -20px var(--wow-glow);
      }}

      /* Panel card */
      .wow-card {{
        border: 1px solid var(--wow-border);
        border-radius: 16px;
        background: var(--wow-panel);
        padding: 14px 16px;
        box-shadow: 0 18px 50px -35px var(--wow-glow);
      }}

      /* Paper preview surface */
      .wow-paper {{
        background: var(--wow-paper);
        border: 1px solid var(--wow-paper-border);
        border-radius: 16px;
        padding: 14px 16px;
        box-shadow: 0 18px 50px -40px var(--wow-glow);
      }}

      /* Accent pill badges */
      .wow-pill {{
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        border: 1px solid var(--wow-border);
        background: rgba(127,127,127,0.06);
        color: var(--wow-subtle);
        font-weight: 600;
        font-size: 0.85rem;
        margin-right: 6px;
      }}
      .wow-pill-strong {{
        color: var(--wow-text);
        border-color: rgba(0,0,0,0);
        background: linear-gradient(90deg, var(--wow-accent), var(--wow-accent-2));
      }}

      /* Buttons (best effort: Streamlit uses inline styles; we can enhance slightly) */
      button[kind="primary"] {{
        border-radius: 12px !important;
        box-shadow: 0 18px 50px -40px var(--wow-glow) !important;
      }}

      /* Code blocks / text areas */
      textarea, .stCodeBlock, pre {{
        border-radius: 12px !important;
      }}

      /* Coral keyword helper */
      .wow-coral {{
        color: var(--wow-coral);
        font-weight: 700;
      }}

      /* Sidebar tweaks */
      section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(127,127,127,0.06), rgba(0,0,0,0.00));
      }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


apply_wow_css(st.session_state.theme_mode, PAINTER_STYLES[st.session_state.style_name])


# =========================
# Helpers: Provider Key Status
# =========================
PROVIDER_ENV_KEYS = {
    "Gemini": "GEMINI_API_KEY",
    "OpenAI": "OPENAI_API_KEY",
    "Anthropic": "ANTHROPIC_API_KEY",
    "Grok": "GROK_API_KEY",
}


def provider_status(env_key_name: str) -> str:
    """Return 'env', 'session', or 'missing'. Never return the actual key."""
    if os.getenv(env_key_name):
        return "env"
    if st.session_state.session_keys.get(env_key_name):
        return "session"
    return "missing"


def status_badge(status: str) -> str:
    if status == "env":
        return f"<span class='wow-pill wow-pill-strong'>{t('from_env')}</span>"
    if status == "session":
        return f"<span class='wow-pill wow-pill-strong'>{t('from_session')}</span>"
    return f"<span class='wow-pill'>{t('not_set')}</span>"


# =========================
# Jackpot
# =========================
def jackpot_style() -> None:
    if st.session_state.style_locked:
        return
    current = st.session_state.style_name
    candidates = [s for s in STYLE_NAMES if s != current] or STYLE_NAMES
    st.session_state.style_name = random.choice(candidates)


# =========================
# UI: Sidebar Controls
# =========================
with st.sidebar:
    st.markdown(f"### {t('ui_controls')}")

    # Language
    lang = st.selectbox(
        t("language"),
        options=["en", "zh-TW"],
        format_func=lambda x: t("english") if x == "en" else t("zh_tw"),
        index=0 if st.session_state.lang == "en" else 1,
    )
    st.session_state.lang = lang

    # Theme
    theme = st.radio(
        t("theme"),
        options=["light", "dark"],
        format_func=lambda x: t("light") if x == "light" else t("dark"),
        index=0 if st.session_state.theme_mode == "light" else 1,
        horizontal=True,
    )
    st.session_state.theme_mode = theme

    # Style selector + Jackpot
    style_name = st.selectbox(
        t("style"),
        options=STYLE_NAMES,
        index=STYLE_NAMES.index(st.session_state.style_name),
    )
    st.session_state.style_name = style_name

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button(t("jackpot"), use_container_width=True):
            jackpot_style()
    with c2:
        st.session_state.style_locked = st.checkbox(
            t("lock_style"),
            value=st.session_state.style_locked,
            help=t("style_locked_help"),
        )

    st.divider()

    # API Key Manager (Env-first, UI fallback)
    st.markdown(f"### {t('api_keys')}")
    st.caption(t("keys_desc"))

    for provider, env_key in PROVIDER_ENV_KEYS.items():
        st.markdown(f"**{provider}**  {status_badge(provider_status(env_key))}", unsafe_allow_html=True)

        if not os.getenv(env_key):
            # Only show input when missing in ENV.
            # Even then, store in session only; do not display existing session key.
            key_input = st.text_input(
                t("enter_key"),
                type="password",
                key=f"key_input_{env_key}",
                placeholder="••••••••••",
            )
            cols = st.columns([1, 1])
            with cols[0]:
                if st.button(t("save_key"), key=f"save_{env_key}", use_container_width=True):
                    st.session_state.session_keys[env_key] = key_input.strip()
                    st.session_state[f"key_input_{env_key}"] = ""
            with cols[1]:
                if st.button(t("clear_key"), key=f"clear_{env_key}", use_container_width=True):
                    st.session_state.session_keys[env_key] = ""
                    st.session_state[f"key_input_{env_key}"] = ""
        else:
            st.caption(t("configured"))

        st.write("")

    st.divider()
    st.markdown(f"### {t('quick_actions')}")
    if st.button("Reset UI Session State", use_container_width=True):
        for k in list(st.session_state.keys()):
            if k not in ["session_keys"]:  # keep session keys unless user cleared
                del st.session_state[k]
        init_state()
        st.rerun()


# Re-apply CSS after sidebar changes (theme/lang/style)
apply_wow_css(st.session_state.theme_mode, PAINTER_STYLES[st.session_state.style_name])


# =========================
# UI: Topbar + WOW Status Indicators
# =========================
style = PAINTER_STYLES[st.session_state.style_name]

top = st.container()
with top:
    st.markdown(
        f"""
        <div class="wow-topbar">
          <div style="display:flex; justify-content:space-between; align-items:flex-end; gap:16px; flex-wrap:wrap;">
            <div>
              <h1 class="wow-title">{t("app_title")}</h1>
              <div class="wow-subtitle">{t("app_subtitle")}</div>
              <div style="margin-top:10px;">
                <span class="wow-pill wow-pill-strong">{style.name}</span>
                <span class="wow-pill">{t("theme")}: {t("light") if st.session_state.theme_mode=="light" else t("dark")}</span>
                <span class="wow-pill">{t("language")}: {t("english") if st.session_state.lang=="en" else t("zh_tw")}</span>
              </div>
            </div>

            <div style="min-width: 320px;">
              <div style="font-weight:800; margin-bottom:6px;">{t("status")}</div>
              <div style="display:flex; flex-wrap:wrap; gap:8px;">
                <span class="wow-pill">{t("pipeline_state")}: <b>{t(st.session_state.pipeline_status)}</b></span>
                <span class="wow-pill">Step: <b>{st.session_state.pipeline_step}/{st.session_state.pipeline_total_steps}</b></span>
                <span class="wow-pill">Latency: <b>{st.session_state.last_latency_ms if st.session_state.last_latency_ms is not None else "—"} ms</b></span>
              </div>
              <div style="margin-top:8px; color: var(--wow-subtle); font-size: 0.92rem;">
                {t("demo_hint")}
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================
# Main Workspaces
# =========================
tabs = st.tabs([t("forms_tab"), t("agent_tab"), t("note_tab"), t("dash_tab")])


# ---- Forms Workspace (Scaffold) ----
with tabs[0]:
    colA, colB = st.columns([1.05, 1.0], gap="large")

    with colA:
        st.markdown(f"<div class='wow-card'><h3>{t('forms_scaffold_title')}</h3>"
                    f"<div style='color:var(--wow-subtle)'>{t('forms_scaffold_body')}</div></div>",
                    unsafe_allow_html=True)

        st.write("")
        st.markdown("<div class='wow-card'><h4>Input</h4></div>", unsafe_allow_html=True)
        mode = st.radio("Mode", ["PDF Spec", "Raw Document"], horizontal=True)
        sample_spec = """## pdf_spec
title: Device Application Form
fields:
  - label: Device Name
    name: device_name
    type: text
  - label: Submission Type
    name: submission_type
    type: dropdown
    options: [New, Update, Replacement]
  - label: Agree to Terms
    name: agree_terms
    type: checkbox
  - label: Submission Date
    name: submission_date
    type: date
"""
        if mode == "PDF Spec":
            st.text_area("Paste PDF Spec (Markdown)", value=sample_spec, height=220)
        else:
            st.text_area("Paste Raw Form Text", value="Device Name: ______\nSubmission Type: [New/Update]\nAgree to Terms: [ ]", height=220)

        cols = st.columns([1, 1, 1])
        with cols[0]:
            st.button("Generate Structure (via Agents)", type="primary", use_container_width=True)
        with cols[1]:
            st.button("Download Python (.py)", use_container_width=True)
        with cols[2]:
            st.button("Download jsPDF (.js)", use_container_width=True)

    with colB:
        st.markdown("<div class='wow-paper'><h3>Preview (Paper)</h3>"
                    "<div style='color:var(--wow-subtle)'>"
                    "This panel is styled as a document surface. In the full implementation, it renders the extracted form schema with edit controls."
                    "</div>"
                    "<hr style='border:none; border-top:1px solid var(--wow-paper-border); margin:12px 0;'>"
                    "<div><b>Title:</b> Device Application Form</div>"
                    "<div style='margin-top:10px; color:var(--wow-subtle)'>"
                    "Fields: text / dropdown / checkbox / date (preserved from v1.1)."
                    "</div>"
                    "</div>",
                    unsafe_allow_html=True)


# ---- Agent Studio (Scaffold with WOW per-step controls) ----
with tabs[1]:
    left, right = st.columns([1.1, 1.0], gap="large")

    with left:
        st.markdown(f"<div class='wow-card'><h3>{t('agent_scaffold_title')}</h3>"
                    f"<div style='color:var(--wow-subtle)'>{t('agent_scaffold_body')}</div></div>",
                    unsafe_allow_html=True)
        st.write("")

        st.markdown("<div class='wow-card'><h4>Step Controls (Example)</h4></div>", unsafe_allow_html=True)
        step_name = st.selectbox("Agent Step", ["01_extract_structure", "02_validate_repair", "03_generate_fpdf2", "04_generate_jspdf"])
        model = st.selectbox(
            "Model",
            [
                "gpt-4o-mini",
                "gpt-4.1-mini",
                "gemini-2.5-flash",
                "gemini-2.5-flash-lite",
                "gemini-3-flash-preview",
                "anthropic (select in full impl)",
                "grok-4-fast-reasoning",
                "grok-3-mini",
            ],
        )
        max_tokens = st.number_input("max_tokens", min_value=256, max_value=20000, value=12000, step=256)
        prompt = st.text_area("Prompt (editable)", value=f"You are agent {step_name}. Follow SKILL.md and return the required output.", height=180)

        run_cols = st.columns([1, 1, 1])
        with run_cols[0]:
            if st.button("Run Step", type="primary", use_container_width=True):
                st.session_state.pipeline_status = "running"
                st.session_state.pipeline_step = min(st.session_state.pipeline_step + 1, st.session_state.pipeline_total_steps)
                start = time.time()
                time.sleep(0.25)  # placeholder "work"
                st.session_state.last_latency_ms = int((time.time() - start) * 1000)
                st.session_state.pipeline_status = "awaiting_edit"
                st.rerun()
        with run_cols[1]:
            if st.button("Auto-run (scaffold)", use_container_width=True):
                st.session_state.pipeline_status = "running"
                st.session_state.pipeline_step = st.session_state.pipeline_total_steps
                st.session_state.last_latency_ms = 420
                st.session_state.pipeline_status = "completed"
                st.rerun()
        with run_cols[2]:
            if st.button("Reset Pipeline", use_container_width=True):
                st.session_state.pipeline_status = "idle"
                st.session_state.pipeline_step = 0
                st.session_state.last_latency_ms = None
                st.rerun()

    with right:
        st.markdown("<div class='wow-paper'><h3>Output Viewer (Editable)</h3>"
                    "<div style='color:var(--wow-subtle)'>"
                    "In the full implementation: show agent output in Text/Markdown views; allow user edits; pass edited output into the next step."
                    "</div>"
                    "</div>",
                    unsafe_allow_html=True)

        st.write("")
        view = st.radio("View", ["Text", "Markdown"], horizontal=True)
        output_text = st.text_area("Agent Output (editable)", value="{\n  \"title\": \"Device Application Form\",\n  \"fields\": []\n}", height=260)
        st.button("Use edited output for next step", use_container_width=True)


# ---- AI Note Keeper (Scaffold) ----
with tabs[2]:
    a, b = st.columns([1.05, 1.0], gap="large")

    with a:
        st.markdown(f"<div class='wow-card'><h3>{t('note_scaffold_title')}</h3>"
                    f"<div style='color:var(--wow-subtle)'>{t('note_scaffold_body')}</div></div>",
                    unsafe_allow_html=True)
        st.write("")

        note_in = st.text_area("Paste note (txt/markdown)", value="Meeting Notes:\n- Discussed FormAgent UI\n- Need WOW theme + i18n\n- Decide models list\n", height=220)
        cols = st.columns([1, 1, 1])
        with cols[0]:
            st.button("Organize Note", type="primary", use_container_width=True)
        with cols[1]:
            st.button("AI Keywords (Magic)", use_container_width=True)
        with cols[2]:
            st.button("More Magics…", use_container_width=True)

    with b:
        st.markdown("<div class='wow-paper'><h3>Organized Markdown Preview</h3>"
                    "<div style='color:var(--wow-subtle)'>"
                    "In the full implementation: the system outputs organized markdown and highlights keywords in "
                    "<span class='wow-coral'>coral</span>."
                    "</div>"
                    "<hr style='border:none; border-top:1px solid var(--wow-paper-border); margin:12px 0;'>"
                    "<div><b>Summary</b>: WOW UI shell scaffolded.</div>"
                    "<div style='margin-top:10px;'><b>Keywords</b>: "
                    "<span class='wow-coral'>WOW UI</span>, <span class='wow-coral'>i18n</span>, <span class='wow-coral'>Jackpot</span>"
                    "</div>"
                    "</div>",
                    unsafe_allow_html=True)


# ---- Dashboard (WOW Indicators Scaffold) ----
with tabs[3]:
    st.markdown(f"<div class='wow-card'><h3>{t('dash_scaffold_title')}</h3>"
                f"<div style='color:var(--wow-subtle)'>{t('dash_scaffold_body')}</div></div>",
                unsafe_allow_html=True)
    st.write("")

    c1, c2, c3 = st.columns([1, 1, 1], gap="large")

    with c1:
        st.markdown("<div class='wow-paper'><h4>Run Timeline</h4>"
                    "<div style='color:var(--wow-subtle)'>"
                    "Show nodes: step name • model • tokens • elapsed • status."
                    "</div></div>", unsafe_allow_html=True)
        st.write("")
        st.progress(st.session_state.pipeline_step / max(1, st.session_state.pipeline_total_steps))

    with c2:
        st.markdown("<div class='wow-paper'><h4>Provider Readiness</h4></div>", unsafe_allow_html=True)
        for provider, env_key in PROVIDER_ENV_KEYS.items():
            st.write(f"- **{provider}**: `{provider_status(env_key)}`")

    with c3:
        st.markdown("<div class='wow-paper'><h4>Artifacts</h4>"
                    "<div style='color:var(--wow-subtle)'>"
                    "Schema • Python • jsPDF • Preview PDF readiness."
                    "</div></div>", unsafe_allow_html=True)

    st.write("")
    st.caption(t("footer"))
