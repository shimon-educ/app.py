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

# פונקציה לחילוץ נקודות בפורמט (x,y) - מטפלת ברווחים וסוגריים
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
                    st.info("נראה שזו לא התשובה הנכונה. אני ממליץ לך להסתכל ברמזים למטה ולנסות שוב. אם תרצה, תוכל גם ללחוץ על 'התייאשתי' כדי לראות את הדרך.")
                    
                    if st.checkbox("צריך רמז ראשון?"):
                        st.write("עליך לפתור את המשוואה:")
                        st.latex(sp.latex(den) + "= 0")
                        
                    if st.checkbox("צריך עזרה בפירוק המכנה?"):
                        st.write("אפשר לכתוב את המכנה כך:")
                        st.latex(sp.latex(sp.factor(den)) + "= 0")

                    if st.button("התייאשתי, הצג פתרון והמשך"):
                        st.success(f"הערכים המאפסים הם: {true_pts_str}")
                        st.session_state['force_step_2'] = True
                        st.rerun()
            except:
                st.warning("נא להזין מספרים מופרדים בפסיק.")

        if st.session_state.get('force_step_2'):
            show_step_2 = True

        # --- שלב 2: אסימפטוטות ---
        show_step_3 = False
        if show_step_2:
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות")
            
            st.subheader("1. אסימפטוטות אנכיות")
            with st.expander("💡 רמז מפורט: אסימפטוטה אנכית"):
                st.write("אלו ערכי ה-x שמצאת בשלב 1 שמאפסים את המכנה.")
                st.info(f"הערכים הם: {true_pts_str}")
            user_asymp = st.text_input("משוואות האסימפטוטות האנכיות (למשל: x=1, x=-3):", key="asymp_input")
            
            st.subheader("2. אסימפטוטה אופקית")
            with st.expander("💡 רמז מפורט: איך מוצאים אסימפטוטה אופקית?"):
                st.write("אנו בודקים את 'מלחמת הכוחות' בין המונה למכנה (החזקה הגבוהה ביותר):")
                st.markdown("""
                1. **החזקה הגבוהה במכנה:** האסימפטוטה היא $y = 0$.
                   * **דוגמה:** $f(x) = \\frac{2x+1}{x^2-4} \implies y = 0$
                2. **החזקות שוות:** מחלקים את המקדמים של החזקות הגבוהות.
                   * **דוגמה:** $f(x) = \\frac{6x^2+1}{2x^2-3} \implies y = \\frac{6}{2} = 3$
                3. **החזקה הגבוהה במונה:** אין אסימפטוטה אופקית.
                   * **דוגמה:** $f(x) = \\frac{x^3}{x^2+1} \implies \text{אין}$
                """)
            user_horiz = st.text_input("משוואת האסימפטוטה האופקית (y = ?):", key="horiz_input")
            
            if user_asymp and user_horiz:
                st.success("מעולה! בוא נמשיך לנקודות חיתוך.")
                show_step_3 = True

        # --- שלב 3: נקודות חיתוך עם הצירים ---
        if show_step_3:
            st.markdown("---")
            st.header("שלב 3: נקודות חיתוך עם הצירים")
            
            # חיתוך עם x
            st.subheader("1. חיתוך עם ציר x")
            with st.expander("💡 רמז: חיתוך עם ציר x"):
                st.write("זה קורה כש- $y=0$. בשבר, זה קורה כשה**מונה** שווה לאפס.")
                st.write("**דוגמה:** ב- $\\frac{x-5}{x+2}$, המונה מתאפס ב- $x=5$, לכן הנקודה היא $(5,0)$.")
            user_x_int = st.text_input("הזן נקודות חיתוך עם ציר x (פורמט: (x,y)):", key="x_int_input")
            
            # חיתוך עם y
            st.subheader("2. חיתוך עם ציר y")
            with st.expander("💡 רמז: חיתוך עם ציר y"):
                st.write("זה קורה כש- $x=0$. מציבים 0 בכל מקום שיש x.")
                st.write("**דוגמה:** ב- $\\frac{x+6}{x-2}$, נציב 0 ונקבל $\\frac{6}{-2}=-3$, לכן הנקודה היא $(0,-3)$.")
            user_y_int = st.text_input("הזן נקודת חיתוך עם ציר y (פורמט: (x,y)):", key="y_int_input")

            # חישוב לוגי
            x_roots = [r for r in sp.solve(num, x) if r not in true_domain]
            true_x_points = sorted([(float(r.evalf()), 0.0) for r in x_roots])
            try:
                true_y_point = [(0.0, float(f.subs(x, 0).evalf()))] if 0 not in true_domain else []
            except: true_y_point = []

            show_plot = False
            if user_x_int and user_y_int:
                u_x = extract_points(user_x_int)
                u_y = extract_points(user_y_int)
                correct_x = (len(u_x) == len(true_x_points)) and all(np.allclose(u_x[i], true_x_points[i]) for i in range(len(u_x)))
                correct_y = (len(u_y) == len(true_y_point)) and all(np.allclose(u_y[i], true_y_point[i]) for i in range(len(u_y)))
                
                if correct_x and correct_y:
                    st.success("מצוין! מצאת את נקודות החיתוך.")
                    show_plot = True
                else:
                    st.info("לא זאת לא התשובה הנכונה, אני ממליץ לך לקרוא את הרמז ולנסות שוב ואם אינך רוצה לנסות שוב לחץ על הצג פיתרון ושרטט")

            if st.button("הצג פיתרון ושרטט"):
                show_plot = True

            if show_plot:
                fig = go.Figure()
                # האסימפטוטות האנכיות מהקוד המקורי שלך
                for pt in true_pts:
                    fig.add_vline(x=float(pt), line_dash="dash", line_color="red", annotation_text=f"x={pt}")
                
                # אסימפטוטה אופקית
                h_val = sp.limit(f, x, sp.oo)
                if h_val.is_finite:
                    fig.add_hline(y=float(h_val), line_dash="dash", line_color="blue", annotation_text=f"y={format_num(h_val)}")

                # הוספת נקודות החיתוך לגרף
                for p in true_x_points:
                    fig.add_trace(go.Scatter(x=[p[0]], y=[0], mode='markers+text', text=[f"({format_num(p[0])},0)"], textposition="bottom center", marker=dict(color='green', size=12), name="חיתוך x"))
                for p in true_y_point:
                    fig.add_trace(go.Scatter(x=[0], y=[p[1]], mode='markers+text', text=[f"(0,{format_num(p[1])})"], textposition="middle right", marker=dict(color='orange', size=12), name="חיתוך y"))

                # העיצוב המקורי שלך (צירים שחורים עבים ורקע לבן)
                fig.update_xaxes(zeroline=True, zerolinewidth=4, zerolinecolor='black', range=[-10, 10])
                fig.update_yaxes(zeroline=True, zerolinewidth=4, zerolinecolor='black', range=[-10, 10])
                fig.update_layout(plot_bgcolor='white', height=500, showlegend=False)
                st.plotly_chart(fig)
                
                # בדיקת נגזרת בסוף כפי שהיה בקוד שלך
                st.markdown("---")
                st.subheader("השלב הבא: גזירה")
                if st.checkbox("בדוק את הנגזרת שחישבת"):
                    st.latex(r"f'(x) = " + sp.latex(sp.simplify(sp.diff(f, x))))

    except Exception as e:
        st.error("הביטוי המתמטי לא תקין.")

if st.sidebar.button("התחל חקירה חדשה"):
    st.session_state.clear()
    st.rerun()
