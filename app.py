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

# --- סרגל צד: הנחיות כתיבה והזנת פונקציה ---
st.sidebar.header("📝 איך מזינים פונקציה?")
st.sidebar.info("""
השתמש בסימנים הבאים:
* **חזקה:** `**` (למשל `x**2`)
* **כפל:** `*` (למשל `2*x`)
* **חילוק:** `/` (למשל `1/x`)
* **דוגמה:** `x**2 / (x**2 - 4)`
""")

input_func = st.sidebar.text_input("הזן פונקציה לחקירה:", "x**2 / (x**2 + 2*x - 3)")

if input_func:
    x = sp.symbols('x')
    try:
        clean_func_str = input_func.replace(" ", "")
        f = sp.sympify(clean_func_str)
        num, den = sp.fraction(f)
        
        # חישוב תחום הגדרה - סינון ממשיים בלבד
        true_domain_raw = sp.solve(den, x)
        true_pts = sorted([format_num(sol.evalf()) for sol in true_domain_raw if sol.is_real])
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
                    st.info("נראה שזו לא התשובה הנכונה. נסה שוב בעזרת הרמזים.")
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
                                st.write(f"المקדמים הם: $a={a}, b={b}, c={c}$")
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
            
            # 1. אסימפטוטות אנכיות
            st.subheader("1. אסימפטוטות אנכיות")
            with st.expander("💡 רמז מפורט: איך מוצאים אסימפטוטה אנכית?"):
                st.write("""
                אסימפטוטה אנכית היא ישר שהגרף מתקרב אליו מאוד אבל לעולם לא נוגע בו. 
                היא מתרחשת בערכי ה-x שגורמים למכנה להיות אפס (אלו שמצאת בשלב הקודם).
                
                **איך בודקים?**
                אם מצאת ש-x=3 מאפס את המכנה, המשוואה היא פשוט $x=3$. 
                אם יש כמה ערכים, נכתוב אותם מופרדים בפסיק.
                """)
                st.info(f"הערכים שמאפסים את המכנה הם: **{true_pts_str}**")

            user_asymp = st.text_input("מהן משוואות האסימפטוטות האנכיות? (למשל: x=1, x=-3):", key="asymp_input")
            
            # משוב בזמן אמת לאנכיות
            if user_asymp:
                try:
                    clean_v = user_asymp.replace('x', '').replace('=', '').strip()
                    user_v_pts = sorted([float(p.strip()) for p in clean_v.split(",")])
                    if np.allclose(user_v_pts, [float(p) for p in true_pts]):
                        st.success("מעולה! אלו האסימפטוטות האנכיות.")
                    else:
                        st.warning("עדיין לא מדויק, בדוק שוב את הערכים.")
                except: pass

            # 2. אסימפטוטה אופקית
            st.subheader("2. אסימפטוטה אופקית")
            with st.expander("💡 רמז מפורט: אסימפטוטה אופקית"):
                st.markdown("""
                בודקים את החזקה הגבוהה ביותר:
                1. **חזקה גבוהה למטה:** האסימפטוטה היא $y = 0$.
                2. **חזקות שוות:** מחלקים את המקדמים. דוגמה: $\\frac{4x^2}{2x^2} \implies y=2$.
                3. **חזקה גבוהה למעלה:** אין אסימפטוטה אופקית.
                """)

            user_horiz = st.text_input("מהי משוואת האסימפטוטה האופקית? (y = ? או 'אין'):", key="horiz_input")
            
            # משוב בזמן אמת לאופקית
            if user_horiz:
                try:
                    true_h = sp.limit(f, x, sp.oo)
                    clean_h = user_horiz.replace('y', '').replace('=', '').strip()
                    if clean_h.lower() == "אין":
                        correct_h = not true_h.is_finite
                    else:
                        correct_h = np.isclose(float(clean_h), float(true_h))
                    
                    if correct_h:
                        st.success("בדיוק! זו האסימפטוטה האופקית.")
                    else:
                        st.warning("לא בדיוק. בדוק שוב את יחס החזקות.")
                except: pass

            if st.button("הצג פתרון סופי וסרטט גרף"):
                fig = go.Figure()
                for pt in true_pts:
                    fig.add_vline(x=float(pt), line_dash="dash", line_color="red", annotation_text=f"x={pt}")
                h_val = sp.limit(f, x, sp.oo)
                if h_val.is_finite:
                    fig.add_hline(y=float(h_val), line_dash="dash", line_color="blue", annotation_text=f"y={format_num(h_val)}")
                
                fig.update_xaxes(zeroline=True, zerolinewidth=4, zerolinecolor='black', range=[-10, 10])
                fig.update_yaxes(zeroline=True, zerolinewidth=4, zerolinecolor='black', range=[-10, 10])
                fig.update_layout(plot_bgcolor='white', height=500)
                st.plotly_chart(fig)
                
                st.markdown("---")
                st.subheader("השלב הבא: גזירה")
                st.latex(r"f'(x) = " + sp.latex(sp.simplify(sp.diff(f, x))))

    except Exception as e:
        st.error("הביטוי לא תקין. בדוק את הוראות הכתיבה בסרגל הצד.")

if st.sidebar.button("התחל חקירה חדשה"):
    st.session_state.clear()
    st.rerun()
