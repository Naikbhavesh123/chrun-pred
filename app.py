import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import math

st.set_page_config(page_title="ChurnIQ", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');
:root{--g:#10b981;--a:#f59e0b;--r:#ef4444;--b:#3b82f6;--c:#22d3ee;--v:#8b5cf6;--t:#f1f5f9;--m:#64748b;--bdr:rgba(255,255,255,0.08);--glass:rgba(255,255,255,0.04);--font:'Outfit',sans-serif;}
@keyframes bg{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
html,body,[data-testid="stAppViewContainer"]{font-family:var(--font)!important;}
[data-testid="stAppViewContainer"]{background:linear-gradient(135deg,#020817,#060d20,#0a0a2e,#060d20,#020817)!important;background-size:400% 400%!important;animation:bg 20s ease infinite!important;}
#MainMenu,footer,[data-testid="stDecoration"],[data-testid="stToolbar"]{display:none!important;}
[data-testid="stSidebar"]{background:rgba(2,8,23,0.97)!important;border-right:1px solid var(--bdr)!important;}
[data-testid="stSidebar"] label,[data-testid="stSidebar"] p{color:#94a3b8!important;font-family:var(--font)!important;}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p{font-size:.78rem!important;font-weight:500!important;}
.main .block-container{padding:2rem 3rem 4rem!important;max-width:100%!important;}
::-webkit-scrollbar{width:4px}::-webkit-scrollbar-thumb{background:#1e293b;border-radius:99px}
.hero{text-align:center;padding:2.8rem 2rem 2rem}
.badge{display:inline-block;border-radius:99px;padding:.3rem 1rem;font-size:.68rem;letter-spacing:.15em;text-transform:uppercase;color:var(--c);background:rgba(34,211,238,.08);border:1px solid rgba(34,211,238,.25);margin-bottom:1.2rem;font-weight:500}
.htitle{font-size:clamp(1.8rem,4vw,2.9rem);font-weight:900;letter-spacing:-.03em;line-height:1.1;background:linear-gradient(135deg,#f1f5f9 30%,#22d3ee 65%,#8b5cf6 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin:0 0 1rem}
.hsub{color:var(--m);font-size:.88rem;max-width:580px;margin:0 auto;line-height:1.75}
.hrule{width:56px;height:2px;margin:1.5rem auto 0;border-radius:99px;background:linear-gradient(90deg,var(--b),var(--c))}
.gc{background:var(--glass);backdrop-filter:blur(20px);border:1px solid var(--bdr);border-radius:20px;padding:1.6rem 1.8rem;position:relative;overflow:hidden;transition:border-color .3s,background .3s}
.gc::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.1),transparent)}
.gc:hover{border-color:rgba(99,179,237,.35);background:rgba(255,255,255,.07)}
.kpi{background:var(--glass);border:1px solid var(--bdr);border-radius:20px;padding:1.4rem 1rem;text-align:center;position:relative;overflow:hidden;transition:all .35s;cursor:default}
.kpi:hover{transform:translateY(-5px);box-shadow:0 20px 50px rgba(0,0,0,.45);border-color:rgba(99,179,237,.35)}
.kpi::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px}
.kpi.bl::after{background:linear-gradient(90deg,#3b82f6,#22d3ee)}.kpi.gr::after{background:linear-gradient(90deg,#10b981,#34d399)}
.kpi.vi::after{background:linear-gradient(90deg,#8b5cf6,#a78bfa)}.kpi.am::after{background:linear-gradient(90deg,#f59e0b,#fcd34d)}
.kpi.re::after{background:linear-gradient(90deg,#ef4444,#f97316)}
.ki{font-size:1.5rem;margin-bottom:.5rem}.kl{font-size:.62rem;letter-spacing:.15em;text-transform:uppercase;color:var(--m);margin-bottom:.4rem;font-weight:500}
.kv{font-size:1.85rem;font-weight:800;letter-spacing:-.03em;line-height:1}.ks{font-size:.7rem;color:var(--m);margin-top:.35rem}
.sec{font-size:.62rem;letter-spacing:.2em;text-transform:uppercase;color:var(--m);display:flex;align-items:center;gap:.6rem;margin:2rem 0 1rem;font-weight:600}
.sec::after{content:'';flex:1;height:1px;background:var(--bdr)}
.probwrap{text-align:center;padding:2rem 1rem 1.5rem}
.probnum{font-size:5rem;font-weight:900;letter-spacing:-.05em;line-height:1}
.problbl{font-size:.65rem;letter-spacing:.2em;text-transform:uppercase;color:var(--m);margin-top:.4rem}
.rbadge{display:inline-block;border-radius:99px;padding:.4rem 1.3rem;font-size:.75rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;margin-top:.9rem}
.rlow{background:rgba(16,185,129,.12);color:#10b981;border:1px solid rgba(16,185,129,.3)}
.rmed{background:rgba(245,158,11,.12);color:#f59e0b;border:1px solid rgba(245,158,11,.3)}
.rhi{background:rgba(239,68,68,.12);color:#ef4444;border:1px solid rgba(239,68,68,.3)}
.gwrap{display:flex;justify-content:center;padding:.5rem 0 1rem}
.dwrap{display:flex;justify-content:center;padding:.5rem 0 .8rem}
@keyframes fb{from{width:0}to{width:var(--w)}}
.pw{margin:.9rem 0}.pr{display:flex;justify-content:space-between;font-size:.72rem;color:var(--m);margin-bottom:.4rem}
.pt{height:8px;background:rgba(255,255,255,.05);border-radius:99px;overflow:hidden;border:1px solid var(--bdr)}
.pf{height:100%;border-radius:99px;animation:fb 1.3s cubic-bezier(.4,0,.2,1) forwards}
.bchart{width:100%}.brow{display:flex;align-items:center;gap:.8rem;margin-bottom:.75rem}
.blbl{width:160px;font-size:.75rem;color:#94a3b8;text-align:right;flex-shrink:0}
.bout{flex:1;height:10px;background:rgba(255,255,255,.05);border-radius:99px;overflow:hidden;border:1px solid var(--bdr)}
.bin{height:100%;border-radius:99px;animation:fb 1s ease forwards}
.bval{width:44px;font-size:.72rem;color:#64748b;font-family:'JetBrains Mono',monospace}
.ii{display:flex;align-items:flex-start;gap:.9rem;padding:.85rem 1rem;border-radius:12px;background:rgba(255,255,255,.025);border:1px solid var(--bdr);margin-bottom:.65rem;transition:background .2s}
.ii:hover{background:rgba(255,255,255,.045)}
.idot{width:8px;height:8px;border-radius:50%;margin-top:5px;flex-shrink:0}
.it{font-size:.82rem;color:var(--t);line-height:1.5}.is{font-size:.7rem;color:var(--m);margin-top:.12rem}
.pill{display:inline-block;border-radius:99px;padding:.22rem .75rem;font-size:.68rem;font-weight:600;letter-spacing:.04em;margin:.2rem}
.pb{background:rgba(59,130,246,.14);color:#60a5fa;border:1px solid rgba(59,130,246,.25)}
.pg{background:rgba(16,185,129,.14);color:#34d399;border:1px solid rgba(16,185,129,.25)}
.pr2{background:rgba(239,68,68,.14);color:#f87171;border:1px solid rgba(239,68,68,.25)}
.pv{background:rgba(139,92,246,.14);color:#a78bfa;border:1px solid rgba(139,92,246,.25)}
.ssec{font-size:.62rem;letter-spacing:.18em;text-transform:uppercase;color:var(--m);display:flex;align-items:center;gap:.5rem;margin:1.2rem 0 .7rem;font-weight:600}
.ssec::after{content:'';flex:1;height:1px;background:var(--bdr)}
.stButton>button{width:100%!important;background:linear-gradient(135deg,#3b82f6,#8b5cf6)!important;color:#fff!important;border:none!important;border-radius:14px!important;padding:.85rem 1rem!important;font-family:var(--font)!important;font-weight:700!important;font-size:1rem!important;letter-spacing:.03em!important;transition:all .3s!important;box-shadow:0 4px 24px rgba(59,130,246,.3)!important}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 8px 32px rgba(59,130,246,.45)!important}
[data-testid="stExpander"]{background:var(--glass)!important;border:1px solid var(--bdr)!important;border-radius:16px!important;margin-top:1rem!important}
[data-testid="stExpander"] summary{color:var(--t)!important;font-family:var(--font)!important;font-weight:600!important}
.footer{text-align:center;padding:2.5rem 0 1rem;font-size:.68rem;color:#1e293b;letter-spacing:.12em;text-transform:uppercase}
.gg{text-shadow:0 0 30px rgba(16,185,129,.55)}.ga{text-shadow:0 0 30px rgba(245,158,11,.55)}.gr2{text-shadow:0 0 30px rgba(239,68,68,.55)}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ── Model ────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model(path):
    try:
        import xgboost  # noqa
    except ImportError:
        raise ImportError("xgboost not installed — add to requirements.txt")
    with open(path, "rb") as f:
        return pickle.load(f)

def get_model():
    path = "churn_complete_model.pkl"
    if not os.path.exists(path):
        return None, f"Model file '{path}' not found."
    try:
        return load_model(path), None
    except Exception as e:
        return None, str(e)


# ── Feature engineering ──────────────────────────────────────
def build_df(plan, fee, usage, tickets, failures, tenure, login, model):
    d = {"monthly_fee":[float(fee)],"avg_weekly_usage_hours":[float(usage)],
         "support_tickets":[int(tickets)],"payment_failures":[int(failures)],
         "tenure_months":[int(tenure)],"last_login_days_ago":[int(login)],
         "plan_type_Premium":[1 if plan=="Premium" else 0],"plan_type_Standard":[0]}
    df = pd.DataFrame(d)
    try:
        fn = model.get_booster().feature_names
        if fn: df = df.reindex(columns=fn, fill_value=0)
    except Exception:
        pass
    return df


# ── Business logic ───────────────────────────────────────────
def eng_score(usage, login, tickets, tenure):
    s = min(usage/40,1)*40 + max(0,(30-login)/30)*30 + min(tenure/24,1)*20 - min(tickets/10,1)*10
    return max(0, min(100, round(s,1)))

def risk(prob):
    if prob < .40: return "LOW RISK",    "#10b981","rlow","gg"
    if prob < .70: return "MEDIUM RISK", "#f59e0b","rmed","ga"
    return             "HIGH RISK",   "#ef4444","rhi","gr2"

def rec(prob):
    if prob >= .70: return ("🚨 Immediate intervention required.",
        "Assign a dedicated CSM, offer 30% loyalty discount, schedule health-check within 48h.")
    if prob >= .40: return ("⚠️ Proactive retention action advised.",
        "Send re-engagement email, highlight unused features, offer one-time upgrade incentive.")
    return ("✅ Customer is stable and engaged.",
        "Maintain regular touchpoints, enrol in upsell campaign and referral programme.")


# ── SVG charts (zero external deps) ─────────────────────────
def gauge(prob, color):
    pct = round(prob*100,1)
    ang = prob*180
    r,cx,cy,sw = 100,150,128,18
    def pt(d):
        a = math.radians(180-d)
        return cx+r*math.cos(a), cy-r*math.sin(a)
    def arc(s,e):
        sx,sy=pt(s); ex,ey=pt(e); lg=1 if e-s>90 else 0
        return f"M{sx:.1f},{sy:.1f} A{r},{r} 0 {lg},0 {ex:.1f},{ey:.1f}"
    segs="".join(f'<path d="{arc(s,e)}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-opacity=".18"/>'
                 for s,e,c in [(0,72,"#10b981"),(72,126,"#f59e0b"),(126,180,"#ef4444")])
    sx,sy=pt(0); ex,ey=pt(ang); lg=1 if ang>90 else 0
    fg=f'<path d="M{sx:.1f},{sy:.1f} A{r},{r} 0 {lg},0 {ex:.1f},{ey:.1f}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" opacity=".92"/>'
    nr=math.radians(180-ang); nx=cx+(r-6)*math.cos(nr); ny=cy-(r-6)*math.sin(nr)
    ndl=(f'<line x1="{cx}" y1="{cy}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="{color}" stroke-width="2.5" stroke-linecap="round"/>'
         f'<circle cx="{cx}" cy="{cy}" r="5" fill="{color}"/>')
    ticks="".join(f'<text x="{pt(d)[0]:.1f}" y="{pt(d)[1]+16:.1f}" text-anchor="middle" fill="#475569" font-size="9" font-family="Outfit,sans-serif">{v}</text>'
                  for v,d in [(0,0),(40,72),(70,126),(100,180)])
    return f"""<div class="gwrap"><svg width="300" height="158" viewBox="0 0 300 155">
      {segs}{fg}{ndl}{ticks}
      <text x="{cx}" y="{cy-16}" text-anchor="middle" fill="{color}" font-size="30" font-weight="800" font-family="Outfit,sans-serif">{pct}%</text>
      <text x="{cx}" y="{cy-2}" text-anchor="middle" fill="#475569" font-size="8.5" font-family="Outfit,sans-serif" letter-spacing="2">CHURN RISK</text>
    </svg></div>"""

def donut(prob, color):
    ch=round(prob*100,1); re=round((1-prob)*100,1)
    cx,cy,r,sw=90,90,65,20; C=2*math.pi*r
    cd=C*prob; rd=C*(1-prob)
    rc="#10b981" if prob<.4 else "#f59e0b" if prob<.7 else "#334155"
    return f"""<div class="dwrap"><svg width="180" height="180" viewBox="0 0 180 180">
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{rc}" stroke-width="{sw}"
              stroke-dasharray="{rd:.2f} {C:.2f}" transform="rotate(-90 {cx} {cy})" opacity=".7"/>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{sw}"
              stroke-dasharray="{cd:.2f} {C:.2f}" stroke-dashoffset="{-rd:.2f}" transform="rotate(-90 {cx} {cy})"/>
      <text x="{cx}" y="{cy-6}" text-anchor="middle" fill="{color}" font-size="22" font-weight="800" font-family="Outfit,sans-serif">{ch}%</text>
      <text x="{cx}" y="{cy+12}" text-anchor="middle" fill="#475569" font-size="8.5" font-family="Outfit,sans-serif" letter-spacing="1.5">CHURN</text>
    </svg></div>
    <div style="text-align:center;margin-top:.2rem;">
      <span class="pill pg">Retain {re}%</span><span class="pill pr2">Churn {ch}%</span>
    </div>"""

def barchart(inp):
    rows=[("Monthly Fee ($)",inp["monthly_fee"],500,"#22d3ee"),
          ("Weekly Usage (hrs)",inp["avg_weekly_usage_hours"],80,"#10b981" if inp["avg_weekly_usage_hours"]>=10 else "#ef4444"),
          ("Support Tickets",inp["support_tickets"],20,"#ef4444" if inp["support_tickets"]>=3 else "#10b981"),
          ("Payment Failures",inp["payment_failures"],10,"#ef4444" if inp["payment_failures"]>=2 else "#10b981"),
          ("Tenure (months)",inp["tenure_months"],60,"#10b981" if inp["tenure_months"]>=6 else "#f59e0b"),
          ("Days Since Login",inp["last_login_days_ago"],90,"#ef4444" if inp["last_login_days_ago"]>14 else "#10b981")]
    h='<div class="bchart">'
    for lbl,val,mx,col in rows:
        p=min(val/mx*100,100)
        h+=(f'<div class="brow"><span class="blbl">{lbl}</span>'
            f'<div class="bout"><div class="bin" style="width:{p:.1f}%;background:linear-gradient(90deg,{col},{col}88);"></div></div>'
            f'<span class="bval">{val}</span></div>')
    return h+"</div>"


# ── Sidebar ──────────────────────────────────────────────────
def sidebar():
    with st.sidebar:
        st.markdown("""<div style="text-align:center;padding:.4rem 0 .8rem;">
          <div style="font-size:1.4rem;">🚀</div>
          <div style="font-family:'Outfit',sans-serif;font-weight:800;font-size:1rem;color:#f1f5f9;">ChurnIQ</div>
          <div style="font-size:.6rem;color:#475569;letter-spacing:.15em;text-transform:uppercase;margin-top:.15rem;">Intelligence Platform</div>
        </div><hr style="border-color:rgba(255,255,255,.06);margin:.6rem 0 .4rem;">""", unsafe_allow_html=True)
        st.markdown('<div class="ssec">🗂 Subscription</div>', unsafe_allow_html=True)
        plan = st.selectbox("Plan Type", ["Basic","Premium"])
        fee  = st.slider("Monthly Fee ($)", 0, 500, 79)
        st.markdown('<div class="ssec">📈 Engagement</div>', unsafe_allow_html=True)
        usage  = st.slider("Avg Weekly Usage (hrs)", 0.0, 80.0, 14.0, 0.5)
        tenure = st.slider("Tenure (months)", 0, 60, 11)
        login  = st.slider("Days Since Last Login", 0, 90, 9)
        st.markdown('<div class="ssec">🔧 Support & Billing</div>', unsafe_allow_html=True)
        tickets  = st.number_input("Support Tickets",  0, 50, 1)
        failures = st.number_input("Payment Failures", 0, 20, 0)
        st.markdown("<br>", unsafe_allow_html=True)
        clicked = st.button("🔮  Predict Churn Risk")
        model, err = get_model()
        st.markdown('<hr style="border-color:rgba(255,255,255,.06);margin:1.2rem 0 .8rem;">', unsafe_allow_html=True)
        if model:
            st.markdown("""<div style="font-size:.7rem;color:#10b981;text-align:center;background:rgba(16,185,129,.08);
              border-radius:8px;padding:.45rem;border:1px solid rgba(16,185,129,.2);">✅ Model Loaded</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div style="font-size:.7rem;color:#f59e0b;text-align:center;background:rgba(245,158,11,.08);
              border-radius:8px;padding:.45rem;border:1px solid rgba(245,158,11,.2);">⚠️ {err}</div>""", unsafe_allow_html=True)
    return plan, fee, usage, tickets, failures, tenure, login, clicked, model, err


# ── Pages ────────────────────────────────────────────────────
def hero():
    st.markdown("""<div class="hero">
      <div class="badge">Enterprise Intelligence Platform</div>
      <h1 class="htitle">🚀 SaaS Customer Churn<br>Intelligence Platform</h1>
      <p class="hsub">Real-time churn risk scoring powered by machine learning.
        Identify at-risk customers, understand behaviour drivers,
        and take targeted retention actions before it's too late.</p>
      <div class="hrule"></div>
    </div>""", unsafe_allow_html=True)

def idle():
    st.markdown('<div class="sec">📡 System Ready</div>', unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    for col,icon,lbl,val,cls in [(c1,"🧠","Model","XGBoost","bl"),(c2,"📊","Features","7 Inputs","vi"),(c3,"⚡","Latency","< 50ms","gr")]:
        with col:
            st.markdown(f"""<div class="kpi {cls}"><div class="ki">{icon}</div>
              <div class="kl">{lbl}</div><div class="kv" style="font-size:1.2rem;color:#f1f5f9;">{val}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div class="gc" style="text-align:center;padding:3rem 2rem;">
      <div style="font-size:2.8rem;margin-bottom:1rem;">🎯</div>
      <div style="font-family:'Outfit',sans-serif;font-size:1.05rem;font-weight:600;color:#f1f5f9;margin-bottom:.6rem;">Configure Customer Profile</div>
      <div style="font-size:.82rem;color:#64748b;max-width:360px;margin:0 auto;line-height:1.75;">
        Set parameters in the sidebar and click <strong style="color:#60a5fa;">Predict Churn Risk</strong>.</div>
      <div style="margin-top:1.5rem;">
        <span class="pill pb">Machine Learning</span>
        <span class="pill pg">Real-time Scoring</span>
        <span class="pill pv">Retention Intelligence</span>
      </div></div>""", unsafe_allow_html=True)

def results(prob, inp, plan):
    lbl,col,bcls,gcls = risk(prob)
    pct=round(prob*100,1); ret=round((1-prob)*100,1)
    eng=eng_score(inp["avg_weekly_usage_hours"],inp["last_login_days_ago"],inp["support_tickets"],inp["tenure_months"])
    rt,rb=rec(prob)
    kc="re" if prob>=.7 else "am" if prob>=.4 else "gr"
    ec="gr" if eng>=60 else "am" if eng>=35 else "re"
    ecol="#10b981" if eng>=60 else "#f59e0b" if eng>=35 else "#ef4444"

    st.markdown('<div class="sec">📊 Prediction Results</div>', unsafe_allow_html=True)
    k1,k2,k3=st.columns(3)
    with k1: st.markdown(f"""<div class="kpi {kc}"><div class="ki">🎯</div><div class="kl">Churn Risk Score</div>
      <div class="kv {gcls}" style="color:{col};">{pct}%</div><div class="ks">{lbl}</div></div>""", unsafe_allow_html=True)
    with k2: st.markdown(f"""<div class="kpi {ec}"><div class="ki">⚡</div><div class="kl">Engagement Score</div>
      <div class="kv" style="color:{ecol};">{eng}<span style="font-size:1.1rem;">/100</span></div>
      <div class="ks">Usage · Recency · Tenure</div></div>""", unsafe_allow_html=True)
    with k3: st.markdown(f"""<div class="kpi bl"><div class="ki">🔒</div><div class="kl">Retention Probability</div>
      <div class="kv" style="color:#22d3ee;">{ret}%</div><div class="ks">Likelihood to stay</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    cg,cd=st.columns([3,2])
    with cg: st.markdown(f"""<div class="gc"><div class="probwrap">
        <div class="problbl">Churn Probability</div>
        <div class="probnum {gcls}" style="color:{col};">{pct}%</div>
        <div><span class="rbadge {bcls}">{lbl}</span></div>
      </div>{gauge(prob,col)}</div>""", unsafe_allow_html=True)
    with cd: st.markdown(f"""<div class="gc" style="height:100%;">
        <div style="font-size:.62rem;letter-spacing:.15em;text-transform:uppercase;color:#64748b;font-weight:600;margin-bottom:.5rem;">Retention vs Churn Split</div>
        {donut(prob,col)}</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec">📉 Risk Breakdown</div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="gc">
      <div class="pw"><div class="pr"><span>Overall Churn Risk</span><span>{pct}%</span></div>
        <div class="pt"><div class="pf" style="--w:{pct}%;width:{pct}%;background:linear-gradient(90deg,{col},{col}88);"></div></div></div>
      <div class="pw"><div class="pr"><span>Engagement Health</span><span>{eng}/100</span></div>
        <div class="pt"><div class="pf" style="--w:{eng}%;width:{eng}%;background:linear-gradient(90deg,#10b981,#34d399);"></div></div></div>
      <div class="pw"><div class="pr"><span>Retention Probability</span><span>{ret}%</span></div>
        <div class="pt"><div class="pf" style="--w:{ret}%;width:{ret}%;background:linear-gradient(90deg,#3b82f6,#22d3ee);"></div></div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    rb2="#ef4444" if prob>=.7 else "#f59e0b" if prob>=.4 else "#10b981"
    rbg="rgba(239,68,68,.05)" if prob>=.7 else "rgba(245,158,11,.05)" if prob>=.4 else "rgba(16,185,129,.05)"
    st.markdown(f"""<div class="gc" style="border-color:{rb2}44;background:{rbg};">
      <div style="font-family:'Outfit',sans-serif;font-size:1rem;font-weight:700;color:#f1f5f9;margin-bottom:.55rem;">{rt}</div>
      <div style="font-size:.83rem;color:#94a3b8;line-height:1.75;">{rb}</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📊  Customer Risk Analysis  —  Full Intelligence Report"):
        st.markdown('<div class="sec">📌 Feature Signal Analysis</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="gc">{barchart(inp)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec">🔍 Key Churn Drivers</div>', unsafe_allow_html=True)
        items=[]
        if inp["last_login_days_ago"]>14: items.append(("#ef4444",f"Inactivity — {inp['last_login_days_ago']} days since last login","High dormancy is the strongest leading churn indicator."))
        if inp["payment_failures"]>=2:    items.append(("#ef4444",f"Billing Friction — {inp['payment_failures']} payment failures","Repeated failures signal involuntary churn risk."))
        if inp["avg_weekly_usage_hours"]<5: items.append(("#f59e0b",f"Low Engagement — {inp['avg_weekly_usage_hours']:.1f} hrs/week","Customers using <5 hrs/week churn 3x more often."))
        if inp["support_tickets"]>=3:     items.append(("#f59e0b",f"Support Friction — {inp['support_tickets']} tickets","High ticket volume indicates unresolved pain points."))
        if inp["tenure_months"]<4:        items.append(("#f59e0b","Early Tenure Risk — onboarding window","First 3 months have the highest voluntary churn rate."))
        if inp["avg_weekly_usage_hours"]>=15: items.append(("#10b981",f"Strong Usage — {inp['avg_weekly_usage_hours']:.1f} hrs/week","High usage is the strongest retention predictor."))
        if inp["tenure_months"]>=12:      items.append(("#10b981",f"Loyal Tenure — {inp['tenure_months']} months","Long-term customers have significantly lower churn probability."))
        if not items: items.append(("#10b981","Profile looks balanced","No major risk signals detected."))
        for c,t,s in items:
            st.markdown(f"""<div class="ii"><div class="idot" style="background:{c};box-shadow:0 0 6px {c}88;"></div>
              <div><div class="it"><strong>{t}</strong></div><div class="is">{s}</div></div></div>""", unsafe_allow_html=True)
        st.markdown('<div class="sec">📋 Input Summary</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({"Feature":["Plan","Monthly Fee","Weekly Usage","Support Tickets","Payment Failures","Tenure","Days Since Login"],
            "Value":[plan,f"${inp['monthly_fee']:.0f}",f"{inp['avg_weekly_usage_hours']:.1f}",inp["support_tickets"],inp["payment_failures"],inp["tenure_months"],inp["last_login_days_ago"]]}),
            use_container_width=True, hide_index=True)


# ── Main ─────────────────────────────────────────────────────
def main():
    hero()
    plan,fee,usage,tickets,failures,tenure,login,clicked,model,err = sidebar()
    if clicked:
        if model is None:
            st.error(f"Model unavailable: {err}")
        else:
            with st.spinner("Running prediction engine…"):
                try:
                    inp={"monthly_fee":fee,"avg_weekly_usage_hours":usage,"support_tickets":tickets,
                         "payment_failures":failures,"tenure_months":tenure,"last_login_days_ago":login}
                    X=build_df(plan,fee,usage,tickets,failures,tenure,login,model)
                    prob=float(model.predict_proba(X)[0][1])
                    results(prob,inp,plan)
                except Exception as e:
                    st.error(f"Prediction failed: {e}")
                    st.exception(e)
    else:
        idle()
    st.markdown('<div class="footer">ChurnIQ · SaaS Churn Intelligence · Powered by XGBoost &amp; Streamlit</div>', unsafe_allow_html=True)

if __name__=="__main__":
    main()