import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

# הגדרות עמוד - MathBuddy
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

# הזנת פונקציה בסרגל הצידי
input_func = st.sidebar.text_input("הזן פונקציה לחקירה:", "x**2 / (x**2 + 2*x - 3)")

if input_func:
    x = sp.symbols('x')
    try:
        f = sp.sympify(input_func)
        num, den = sp.fraction(f)
        true_domain = sp.solve(den, x)
        
        # הכנת פתרונות נקיים לתחום הגדרה
        true_pts = sorted([format_num(p.evalf()) for p in true_domain])
        true_pts_str = ", ".join([str(p) for p in true_pts])
        
        # --- שלב 1: תחום הגדרה ---
        st.header("שלב 1: תחום הגדרה")
        st.latex(r"f(x) = " + sp.latex(f))
        
        user_domain = st.text_input("מהם הערכים שמאפסים את המכנה? (למשל: 5, 2-):", key="domain_input")
        
        show_step_2 = False
        if user_domain:
            try:
                user_pts = sorted([float(p.strip()) for p in user_domain.split(",")])
                # בדיקה אם המשתמש צדק (עם טולרנטיות לשגיאות עיגול קטנות)
                if np.allclose(user_pts, [float(p) for p in true_pts]):
                    st.success("כל הכבוד! אלו הערכים שמאפסים את המכנה.")
                    show_step_2 = True
                else:
                    st.error("לא בדיוק... נסה שוב.")
            except:
                st.warning("נא להזין מספרים מופרדים בפסיק.")

        if st.button("התייאשתי, הצג פתרון והמשך", key="solve_s1"):
            st.info(f"הערכים המאפסים הם: {true_pts_str}")
            show_step_2 = True

        # --- שלב 2: אסימפטוטות אנכיות ---
        show_step_3 = False
        if show_step_2:
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות אנכיות")
            user_asymp = st.text_input("מהן האסימפטוטות האנכיות? (למשל: 3, 1-):", key="asymp_input")
            
            if user_asymp:
                st.success(f"נכון! אלו נקודות אי-הגדרה, לכן x = {user_asymp} הן אסימפטוטות.")
                show_step_3 = True
            elif st.button("דלג לשלב הבא", key="skip_s2"):
                show_step_3 = True

        # --- שלב 3: אסימפטוטה אופקית ---
        show_plot = False
        if show_step_3:
            st.markdown("---")
            st.header("שלב 3: אסימפטוטה אופקית")
            
            # חישוב אופקית (גבול באינסוף)
            h_asymp = sp.limit(f, x, sp.oo)
            
            st.write("מה קורה ל-y כשהפונקציה שואפת לאינסוף?")
            user_horiz = st.text_input("הזן את משוואת האסימפטוטה האופקית (y=?):", key="horiz_input")
            
            if user_horiz:
                try:
                    if float(user_horiz) == float(h_asymp):
                        st.success(f"מצוין! y = {user_horiz}")
                        show_plot = True
                    else:
                        st.error("לא מדויק. רמז: בדוק את יחס המקדמים.")
                except: pass
            
            if st.button("הצג אסימפטוטה אופקית ושרטט", key="solve_s3"):
                st.info(f"האסימפטוטה האופקית היא y = {h_asymp}")
                show_plot = True

        # --- שרטוט המערכת ---
        if show_plot:
            st.subheader("מערכת הצירים עם ה'שלד' של הפונקציה:")
            fig = go.Figure()
            
            # אסימפטוטות אנכיות (אדום)
            for pt in true_pts:
                fig.add_vline(x=float(pt), line_dash="dash", line_color="red")
            
            # אסימפטוטה אופקית (כחול)
            h_val = float(sp.limit(f, x, sp.oo))
            fig.add_hline(y=h_val, line_dash="dash", line_color="blue", annotation_text=f"y={h_val}")
            
            # עיצוב מערכת צירים חזקה - "הצלב השחור"
            fig.update_xaxes(zeroline=True, zerolinewidth=4, zerolinecolor='black', range=[-10, 10], gridcolor='lightgray')
            fig.update_yaxes(zeroline=True, zerolinewidth=4, zerolinecolor='black', range=[-10, 10], gridcolor='lightgray')
            
            fig.update_layout(plot_bgcolor='white', height=500)
            st.plotly_chart(fig)
            
            st.markdown("---")
            st.subheader("השלב הבא: נגזרת")
            if st.checkbox("בדוק את הנגזרת שלך"):
                st.latex(r"f'(x) = " + sp.latex(sp.simplify(sp.diff(f, x))))

    except Exception as e:
        st.error(f"שגיאה: {e}")

if st.sidebar.button("נקה הכל"):
    st.rerun()
