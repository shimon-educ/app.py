import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

# הגדרות עמוד
st.set_page_config(page_title="MathBuddy", layout="centered")

st.title("🧪 מעבדת החקירה של שמעון")
st.write("בוא נחקור את הפונקציה צעד אחר צעד.")

# --- סרגל צד: הנחיות כתיבה והזנת פונקציה ---
st.sidebar.header("📝 איך מזינים פונקציה?")
st.sidebar.info("""
השתמש בסימנים הבאים:
* **חזקה:** `**` (למשל `x**2`)
* **כפל:** `*` (למשל `2*x`)
* **חילוק:** `/` (למשל `1/x`)
* **דוגמה:** `x/(x**3 - 8)`
""")

raw_input = st.sidebar.text_input("הזן פונקציה לחקירה:", "x**2 / (x**2 + 2*x - 3)")
input_func = raw_input.replace(" ", "") # ניקוי רווחים אוטומטי

# פונקציית עזר לעיצוב מספרים
def format_num(n):
    try:
        n_float = float(n)
        return int(n_float) if n_float.is_integer() else round(n_float, 2)
    except:
        return n

if input_func:
    x = sp.symbols('x')
    try:
        f = sp.sympify(input_func)
        num, den = sp.fraction(f)
        
        # חישוב תחום הגדרה - רק פתרונות ממשיים (פותר את בעיית החזקה השלישית)
        true_domain_raw = sp.solve(den, x)
        true_pts = sorted([format_num(sol.evalf()) for sol in true_domain_raw if sol.is_real])
        true_pts_str = ", ".join([str(p) for p in true_pts])
        
        # --- שלב 1: תחום הגדרה ---
        st.header("שלב 1: תחום הגדרה")
        st.latex(r"f(x) = " + sp.latex(f))

        with st.expander("🤔 איך מוצאים תחום הגדרה? (הסבר תיאורטי)"):
            st.write("במתמטיקה, אסור לחלק באפס. לכן עלינו למצוא אילו ערכי x מאפסים את המכנה ולהוציא אותם מהתחום.")
        
        user_domain = st.text_input("הזן את הערכים שמאפסים את המכנה (למשל: 5, 2-):", key="domain_input")
        
        show_step_2 = False
        if user_domain:
            try:
                user_pts = sorted([float(p.strip()) for p in user_domain.split(",")])
                if np.allclose(user_pts, [float(p) for p in true_pts]):
                    st.success("כל הכבוד! אלו בדיוק הערכים שמאפסים את המכנה.")
                    show_step_2 = True
                else:
                    st.info("נראה שזו לא התשובה הנכונה. נסה שוב בעזרת הרמזים.")
                    if st.checkbox("צריך רמז?"):
                        st.write("פתור את המשוואה:")
                        st.latex(sp.latex(den) + "= 0")
                    
                    if st.button("התייאשתי, הצג פתרון והמשך"):
                        st.success(f"הערכים המאפסים הם: {true_pts_str}")
                        st.session_state['force_step_2'] = True
                        st.rerun()
            except:
                st.warning("נא להזין מספרים מופרדים בפסיק.")

        if st.session_state.get('force_step_2'):
            show_step_2 = True

        # --- שלב 2: אסימפטוטות ---
        if show_step_2:
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות")
            
            user_asymp = st.text_input("מהן משוואות האסימפטוטות האנכיות? (x = ?):", key="asymp_input")
            user_horiz = st.text_input("מהי משוואת האסימפטוטה האופקית? (y = ?):", key="horiz_input")
            
            if st.button("הצג פתרון וסרטט"):
                st.subheader("מיקום האסימפטוטות על הצירים:")
                fig = go.Figure()
                for pt in true_pts:
                    fig.add_vline(x=float(pt), line_dash="dash", line_color="red", annotation_text=f"x={pt}")
                
                h_val_lim = sp.limit(f, x, sp.oo)
                if h_val_lim.is_finite:
                    fig.add_hline(y=float(h_val_lim), line_dash="dash", line_color="blue", annotation_text=f"y={format_num(h_val_lim)}")
                
                fig.update_xaxes(zeroline=True, zerolinewidth=4, zerolinecolor='black', range=[-10, 10])
                fig.update_yaxes(zeroline=True, zerolinewidth=4, zerolinecolor='black', range=[-10, 10])
                fig.update_layout(plot_bgcolor='white', height=500)
                st.plotly_chart(fig)

                st.markdown("---")
                st.subheader("השלב הבא: גזירה")
                st.latex(r"f'(x) = " + sp.latex(sp.simplify(sp.diff(f, x))))

    except Exception as e:
        st.error("הביטוי המתמטי לא תקין. בדוק את ההנחיות בסרגל הצד.")

if st.sidebar.button("התחל חקירה חדשה"):
    st.session_state.clear()
    st.rerun()
