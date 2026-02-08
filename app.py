import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="MathBuddy", layout="centered")
st.title("🧪 מעבדת החקירה של שמעון")

def fmt(n):
    try:
        v = float(n)
        return int(v) if v.is_integer() else round(v, 2)
    except: return n

# קלט פונקציה
func_in = st.sidebar.text_input("הזן פונקציה:", "x**2 / (x**2 + 2*x - 3)")

if func_in:
    x = sp.symbols('x')
    try:
        f = sp.sympify(func_in)
        num, den = sp.fraction(f)
        
        # חישוב נתונים
        sol_v = sp.solve(den, x)
        pts_v = sorted([fmt(p.evalf()) for p in sol_v])
        sol_h = fmt(sp.limit(f, x, sp.oo).evalf())

        # שלב 1: תחום הגדרה
        st.header("שלב 1: תחום הגדרה")
        st.latex(r"f(x) = " + sp.latex(f))
        
        u_s1 = st.text_input("אילו x מאפסים מכנה?", key="s1")
        ok1 = False
        if u_s1:
            try:
                u_pts = sorted([float(p.strip()) for p in u_s1.split(",")])
                if np.allclose(u_pts, [float(p) for p in pts_v]):
                    st.success("נכון!")
                    ok1 = True
            except: st.error("הזן מספרים עם פסיק")
        
        if not ok1 and st.button("התייאשתי, פתרון"):
            st.session_state['f1'] = True
        if st.session_state.get('f1'): ok1 = True

        # שלב 2: אסימפטוטות אנכיות
        ok2 = False
        if ok1:
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות אנכיות")
            u_s2 = st.text_input("מהן האסימפטוטות האנכיות?", key="s2")
            if u_s2:
                try:
                    u_v = sorted([float(p.strip()) for p in u_s2.split(",")])
                    if np.allclose(u_v, [float(p) for p in pts_v]):
                        st.success("מעולה!")
                        ok2 = True
                except: pass
            if not ok2 and st.button("התייאשתי, סמן גרף"):
                st.session_state['f2'] = True
        if st.session_state.get('f2'): ok2 = True

        # שלב 3: אסימפטוטה אופקית
        ok3 = False
        if ok2:
            st.markdown("---")
            st.header("שלב 3: אופקית")
            with st.expander("🤔 איך מוצאים?"):
                st.write("**חוק יחס המקדמים:** אם החזקה הגבוהה במונה ובמכנה שווה, מחלקים את המקדמים שלהן.")
            
            u_s3 = st.text_input("מהי האסימפטוטה האופקית (y=)?", key="s3")
            if u_s3:
                try:
                    if np.isclose(float(u_s3), float(sol_h)):
                        st.success("נכון!")
                        ok3 = True
                except: pass
            if not ok3 and st.button("התייאשתי, הצג אופקית"):
                st.session_state['f3'] = True
        if st.session_state.get('f3'): ok3 = True

        # שרטוט הגרף
        if ok2:
            st.markdown("---")
            fig = go.Figure()
            # צירים בולטים (4 רביעים)
            fig.update_xaxes(zeroline=True, zerolinewidth=5, zerolinecolor='black', range=[-10,10])
            fig.update_yaxes(zeroline=True, zerolinewidth=5, zerolinecolor='black', range=[-10,10])
            
            for p in pts_v:
                fig.add_vline(x=float(p), line_dash="dash", line_color="red")
            if ok3:
                fig.add_hline(y=float(sol_h), line_dash="dash", line_color="blue")
            
            fig.update_layout(plot_bgcolor='white', title="מפת האסימפטוטות")
            st.plotly_chart(fig)

    except Exception as e:
        st.error("בדוק את כתיבת הפונקציה")

if st.sidebar.button("חקירה חדשה"):
    st.session_state.clear()
    st.rerun()
