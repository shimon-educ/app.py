import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

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

# הזנת פונקציה
input_func = st.sidebar.text_input("הזן פונקציה לחקירה:", "x**2 / (x**2 + 2*x - 3)")

if input_func:
    x = sp.symbols('x')
    try:
        f = sp.sympify(input_func)
        num, den = sp.fraction(f)
        true_domain = sp.solve(den, x)
        
        # הכנת פתרונות נקיים
        true_pts = sorted([format_num(p.evalf()) for p in true_domain])
        true_pts_str = ", ".join([str(p) for p in true_pts])
        
        # --- שלב 1: תחום הגדרה ---
        st.header("שלב 1: תחום הגדרה")
        st.latex(r"f(x) = " + sp.latex(f))

        with st.expander("🤔 איך מוצאים תחום הגדרה? (הסבר תיאורטי)"):
            st.write("""
            **מה זה בכלל תחום הגדרה?**
            במתמטיקה, אסור לחלק באפס. לכן עלינו למצוא אילו ערכי x מאפסים את המכנה ולהוציא אותם מהתחום.
            **השלבים:** משווים את המכנה לאפס ($המכנה = 0$) ופתורים את המשוואה.
            """)
        
        user_domain = st.text_input("הזן את הערכים שמאפסים את המכנה (למשל: 5, 2-):", key="domain_input")
        
        show_step_2 = False
        
        if user_domain:
            try:
                user_pts = sorted([float(p.strip()) for p in user_domain.split(",")])
                if np.allclose(user_pts, [float(p) for p in true_pts]):
                    st.success("כל הכבוד! אלו בדיוק הערכים שמאפסים את המכנה.")
                    show_step_2 = True
                else:
                    st.error("לא בדיוק... הערכים האלו לא מאפסים את המכנה.")
                    
                    if st.checkbox("צריך רמז ראשון?"):
                        st.write("עליך לפתור את המשוואה:")
                        st.latex(sp.latex(den) + "= 0")
                        
                    if st.checkbox("צריך עזרה בפירוק המכנה?"):
                        st.write("אפשר לכתוב את המכנה כך:")
                        st.latex(sp.latex(sp.factor(den)) + "= 0")

                    if st.button("התייאשתי, הצג פתרון והמשך"):
                        st.info("מהלך הפתרון באמצעות נוסחת השורשים:")
                        try:
                            p = sp.Poly(den, x)
                            coeffs = p.all_coeffs()
                            if len(coeffs) == 3:
                                a, b, c = [format_num(v) for v in coeffs]
                                st.write(f"המקדמים הם: $a={a}, b={b}, c={c}$")
                                st.latex(r"x_{1,2} = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
                                delta = b**2 - 4*a*c
                                st.latex(f"x_{{1,2}} = \\frac{{-({b}) \\pm \\sqrt{{{b}^2 - 4 \\cdot {a} \\cdot {c}}}}}{{2 \\cdot {a}}}")
                                st.latex(f"x_{{1,2}} = \\frac{{{-b} \\pm \\sqrt{{{delta}}}}}{{{2*a}}}")
                        except: pass
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
            
            st.subheader("1. אסימפטוטות אנכיות")
            # התיקון כאן: שינוי הדוגמה ל-x=?
            user_asymp = st.text_input("מהן משוואות האסימפטוטות האנכיות? (x = ?):", key="asymp_input")
            
            st.subheader("2. אסימפטוטה אופקית")
            user_horiz = st.text_input("מהי משוואת האסימפטוטה האופקית? (y = ?):", key="horiz_input")
            
            show_plot = False
            if user_asymp and user_horiz:
                true_horiz_lim = sp.limit(f, x, sp.oo)
                try:
                    # ניקוי הקלט מהתלמיד (הסרת 'x=' או 'y=' אם נכתבו)
                    clean_asymp = user_asymp.replace('x', '').replace('=', '').strip()
                    clean_horiz = user_horiz.replace('y', '').replace('=', '').strip()
                    
                    user_asy_pts = sorted([float(p.strip()) for p in clean_asymp.split(",")])
                    correct_v = np.allclose(user_asy_pts, [float(p) for p in true_pts])
                    
                    if clean_horiz.lower() == "אין":
                        correct_h = not true_horiz_lim.is_finite
                    else:
                        correct_h = np.isclose(float(clean_horiz), float(true_horiz_lim))
                    
                    if correct_v and correct_h:
                        st.success("מעולה! מצאת את כל האסימפטוטות.")
                        show_plot = True
                    else:
                        if not correct_v:
                            st.error("יש טעות באסימפטוטות האנכיות.")
                            with st.expander("🔍 רמז לאסימפטוטה אנכית"):
                                st.write("היזכר בערכים שמאפסים את המכנה שמצאת בשלב הקודם:")
                                st.info(f"הערכים היו: **{true_pts_str}**")
                                st.write("אלו בדיוק המקומות בהם הגרף ייעצר וייצור קו אנכי מהצורה x=מספר.")
                        
                        if not correct_h:
                            st.error("יש טעות באסימפטוטה האופקית.")
                            with st.expander("🔍 רמז לאסימפטוטה אופקית"):
                                st.write("בדוק את החזקה הגבוהה ביותר במונה לעומת המכנה:")
                                st.info("""
                                1. המכנה 'חזק' יותר? האסימפטוטה היא **y = 0**.
                                2. החזקות שוות? חלק את המקדם של המונה במקדם של המכנה.
                                3. המונה 'חזק' יותר? **אין** אסימפטוטה אופקית.
                                """)
                except:
                    st.warning("ודא שהזנת מספרים תקינים באסימפטוטות.")

            if st.button("הצג פתרון וסרטט"):
                show_plot = True

            if show_plot:
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
                if st.checkbox("בדוק את הנגזרת שחישבת"):
                    st.latex(r"f'(x) = " + sp.latex(sp.simplify(sp.diff(f, x))))

    except Exception as e:
        st.error("הביטוי המתמטי לא תקין.")

if st.sidebar.button("התחל חקירה חדשה"):
    st.session_state.clear()
    st.rerun()
