import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
import re

# הגדרות עמוד
st.set_page_config(page_title="MathBuddy", layout="centered")

st.title("🧪 מעבדת החקירה של שמעון")
st.write("בוא נחקור את הפונקציה צעד אחר צעד.")

# פונקציית עזר לעיצוב מספרים
def format_num(n):
    try:
        n_float = float(n)
        return int(n_float) if n_float.is_integer() else round(n_float, 2)
    except:
        return n

# פונקציה לחילוץ נקודות בפורמט (x,y)
def extract_points(text):
    found = re.findall(r'\(\s*(-?\d*\.?\d+)\s*,\s*(-?\d*\.?\d+)\s*\)', text)
    return sorted([(float(x), float(y)) for x, y in found])

# הזנת פונקציה
input_func = st.sidebar.text_input("הזן פונקציה לחקירה:", "x**2 / (x**2 + 2*x - 3)")

if input_func:
    x = sp.symbols('x')
    try:
        f = sp.sympify(input_func)
        num, den = sp.fraction(f)
        true_domain = sp.solve(den, x)
        true_pts = sorted([format_num(p.evalf()) for p in true_domain])
        true_pts_str = ", ".join([str(p) for p in true_pts])
        
        # --- שלב 1: תחום הגדרה ---
        st.header("שלב 1: תחום הגדרה")
        st.latex(r"f(x) = " + sp.latex(f))
        
        user_domain = st.text_input("הזן את הערכים שמאפסים את המכנה (למשל: 5, 2-):", key="domain_input")
        show_step_2 = False

        if user_domain:
            try:
                user_pts_list = sorted([float(p.strip()) for p in user_domain.split(",")])
                if np.allclose(user_pts_list, [float(p) for p in true_pts]):
                    st.success("כל הכבוד! אלו בדיוק הערכים שמאפסים את המכנה.")
                    show_step_2 = True
                else:
                    st.info("נראה שזו לא התשובה הנכונה. הסתכל ברמזים למעלה.")
            except: pass
        
        if st.session_state.get('force_step_2'): show_step_2 = True

        # --- שלב 2: אסימפטוטות ---
        show_step_3 = False
        if show_step_2:
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות")
            
            with st.expander("💡 רמזים לאסימפטוטות"):
                st.write("**אנכיות:** הערכים שמאפסים מכנה.")
                st.write("**אופקיות:** יחס חזקות. אם החזקות שוות, חלק מקדמים.")

            u_asymp = st.text_input("משוואות אנכיות (למשל: x=1, x=-3):", key="asymp_in")
            u_horiz = st.text_input("משוואה אופקית (y=?):", key="horiz_in")

            if u_asymp and u_horiz:
                try:
                    # בדיקה לוגית של התשובה
                    true_h = sp.limit(f, x, sp.oo)
                    clean_v = [float(val) for val in re.findall(r'-?\d*\.?\d+', u_asymp)]
                    clean_h = float(re.findall(r'-?\d*\.?\d+', u_horiz)[0])
                    
                    if np.allclose(sorted(clean_v), [float(p) for p in true_pts]) and np.isclose(clean_h, float(true_h)):
                        st.success("מעולה! בוא נמשיך לנקודות חיתוך.")
                        show_step_3 = True
                    else:
                        st.info("זו לא התשובה הנכונה. נסה שוב או לחץ על הצג פתרון.")
                except: st.warning("בדוק את פורמט הכתיבה (למשל x=1).")

        # --- שלב 3: נקודות חיתוך ---
        if show_step_3 or st.session_state.get('force_plot'):
            st.markdown("---")
            st.header("שלב 3: נקודות חיתוך עם הצירים")
            
            user_x_int = st.text_input("חיתוך עם ציר x בפורמט (x,y):", key="x_int")
            user_y_int = st.text_input("חיתוך עם ציר y בפורמט (x,y):", key="y_int")

            if st.button("הצג פיתרון ושרטט"):
                st.session_state['force_plot'] = True
                
                # חישוב מתמטי לגרף
                x_roots = [r for r in sp.solve(num, x) if r not in true_domain]
                true_x_pts = sorted([(float(r.evalf()), 0.0) for r in x_roots])
                try: true_y_pt = [(0.0, float(f.subs(x, 0).evalf()))] if 0 not in true_domain else []
                except: true_y_pt = []

                # יצירת הגרף האינטראקטיבי המקורי
                fig = go.Figure()
                
                # הוספת אסימפטוטות
                for pt in true_pts:
                    fig.add_vline(x=float(pt), line_dash="dash", line_color="red", annotation_text=f"x={pt}")
                h_lim = sp.limit(f, x, sp.oo)
                if h_lim.is_finite:
                    fig.add_hline(y=float(h_lim), line_dash="dash", line_color="blue", annotation_text=f"y={format_num(h_lim)}")

                # הוספת נקודות חיתוך
                for p in true_x_pts:
                    fig.add_trace(go.Scatter(x=[p[0]], y=[0], mode='markers+text', text=[f"({format_num(p[0])},0)"], textposition="bottom center", marker=dict(color='green', size=12)))
                for p in true_y_pt:
                    fig.add_trace(go.Scatter(x=[0], y=[p[1]], mode='markers+text', text=[f"(0,{format_num(p[1])})"], textposition="middle right", marker=dict(color='orange', size=12)))

                # עיצוב הגרף (החזרת הצירים השחורים העבים)
                fig.update_xaxes(zeroline=True, zerolinewidth=4, zerolinecolor='black', range=[-10, 10])
                fig.update_yaxes(zeroline=True, zerolinewidth=4, zerolinecolor='black', range=[-10, 10])
                fig.update_layout(plot_bgcolor='white', height=500, showlegend=False)
                st.plotly_chart(fig)

    except Exception as e:
        st.error("שגיאה בניתוח הפונקציה.")

if st.sidebar.button("התחל מחדש"):
    st.session_state.clear()
    st.rerun()
