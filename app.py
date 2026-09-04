import streamlit as st
import plotly.express as px
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

st.set_page_config(
    page_title="Health & Nutrition Planner v4.0",
    page_icon="🏋️",
    layout="centered"
)

st.title("🏋️ HEALTH & NUTRITION SMART PLANNER v4.0")
st.caption("All-in-one assistant for calories, food database, ideal weight, supplements, and 1RM calculation.")

st.divider()

# إضافة التبويب الخامس لحاسبة 1RM
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Calorie & Macro Calculator", 
    "🔍 Food Database", 
    "⚖️ Ideal Weight Check", 
    "💊 Supplement Dosage",
    "🏋️‍♂️ 1RM Strength Calculator"
])

# =========================================================
# التبويب الأول: السعرات + الرسم البياني + ملف PDF
# =========================================================
with tab1:
    st.header("Daily Calories, Macros & Water Calculator")
    
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Gender", ["male", "female"], key="t1_gender")
        weight_input = st.text_input("Weight (kg)", value="70", key="t1_weight_text")
        height_input = st.text_input("Height (cm)", value="175", key="t1_height_text")
    with col2:
        age_input = st.text_input("Age", value="20", key="t1_age_text")
        goal_choice = st.selectbox("Select Goal", [
            "1. Cut (Fat Loss)",
            "2. Maintain Weight",
            "3. Bulk (Muscle Gain)"
        ])

    if st.button("Calculate Targets 🚀", type="primary", use_container_width=True):
        try:
            weight = float(weight_input)
            height = float(height_input)
            age = float(age_input)

            bmr = (10 * weight) + (6.25 * height) - (5 * age) + (5 if gender == "male" else -161)
            tdee = bmr * 1.4

            if "Cut" in goal_choice:
                target_calories = tdee - 500
                goal_name = "Fat Loss (Cutting)"
                tip = "Focus on high-protein foods, fiber, and stay in a calorie deficit."
            elif "Bulk" in goal_choice:
                target_calories = tdee + 400
                goal_name = "Muscle Gain (Bulking)"
                tip = "Ensure progressive overload in workouts and eat clean complex carbs."
            else:
                target_calories = tdee
                goal_name = "Weight Maintenance"
                tip = "Keep your activity level consistent and monitor your weekly average weight."

            protein = weight * 2
            fats = (target_calories * 0.25) / 9
            carbs = (target_calories - (protein * 4) - (fats * 9)) / 4
            water_liters = weight * 0.033

            st.success(f"RESULTS FOR GOAL: {goal_name.upper()}")
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Calories", f"{target_calories:.0f} kcal")
            m2.metric("Protein", f"{protein:.1f} g")
            m3.metric("Carbs", f"{carbs:.1f} g")
            m4.metric("Fats", f"{fats:.1f} g")

            st.info(f"💧 **Recommended Water:** {water_liters:.1f} Liters/day")
            st.warning(f"💡 **Smart Tip:** {tip}")

            st.divider()
            st.subheader("📊 Macros Distribution Chart")
            
            # رسم بياني دائرى للمكروز
            chart_data = {
                "Macro": ["Protein", "Carbs", "Fats"],
                "Grams": [protein, carbs, fats]
            }
            fig = px.pie(chart_data, values="Grams", names="Macro", color="Macro",
                         color_discrete_map={"Protein": "#FF4B4B", "Carbs": "#1C83E1", "Fats": "#00C0F2"})
            st.plotly_chart(fig, use_container_width=True)

            # إنزال التقرير بصيغة PDF
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            p.setFont("Helvetica-Bold", 16)
            p.drawString(100, 750, "Health & Nutrition Planner - Summary Report")
            p.setFont("Helvetica", 12)
            p.drawString(100, 720, f"Goal: {goal_name}")
            p.drawString(100, 700, f"Daily Calories: {target_calories:.0f} kcal")
            p.drawString(100, 680, f"Protein: {protein:.1f} g")
            p.drawString(100, 660, f"Carbs: {carbs:.1f} g")
            p.drawString(100, 640, f"Fats: {fats:.1f} g")
            p.drawString(100, 620, f"Recommended Water: {water_liters:.1f} L/day")
            p.save()
            buffer.seek(0)

            st.download_button(
                label="📄 Download Report as PDF",
                data=buffer,
                file_name="Nutrition_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        except ValueError:
            st.error("Please enter valid numbers for Weight, Height, and Age.")

# =========================================================
# التبويب الثاني: البحث في قاعدة البيانات
# =========================================================
with tab2:
    st.header("Search Food Database (20+ Items)")
    search_query = st.text_input("Enter food item to search (e.g., chicken, oats, eggs, tuna):").strip().lower()

    if search_query:
        st.subheader("Search Results:")
        if "chicken" in search_query or "دجاج" in search_query or "صدور" in search_query:
            st.write("**Item:** Chicken Breast (Cooked - 100g)")
            st.info("Calories: 165 kcal | Protein: 31g | Carbs: 0g | Fats: 3.6g")
        elif "cottage" in search_query or "قريش" in search_query or "جبنة" in search_query:
            st.write("**Item:** Cottage Cheese (100g)")
            st.info("Calories: 98 kcal | Protein: 11g | Carbs: 3.4g | Fats: 4.3g")
        elif "beef" in search_query or "لحم" in search_query:
            st.write("**Item:** Lean Ground Beef (Cooked - 100g)")
            st.info("Calories: 217 kcal | Protein: 26g | Carbs: 0g | Fats: 11.8g")
        elif "fish" in search_query or "سمك" in search_query:
            st.write("**Item:** White Fish / Tilapia Fillet (Cooked - 100g)")
            st.info("Calories: 128 kcal | Protein: 26g | Carbs: 0g | Fats: 2.7g")
        elif "salmon" in search_query or "سلمون" in search_query:
            st.write("**Item:** Salmon Fillet (Cooked - 100g)")
            st.info("Calories: 206 kcal | Protein: 22g | Carbs: 0g | Fats: 12g")
        elif "tuna" in search_query or "تونا" in search_query:
            st.write("**Item:** Canned Tuna in Water (100g)")
            st.info("Calories: 116 kcal | Protein: 26g | Carbs: 0g | Fats: 1g")
        elif "egg" in search_query or "بيض" in search_query:
            st.write("**Item:** Whole Large Egg (50g)")
            st.info("Calories: 72 kcal | Protein: 6.3g | Carbs: 0.4g | Fats: 4.8g")
        elif "oats" in search_query or "شوفان" in search_query:
            st.write("**Item:** Rolled Oats (Raw - 100g)")
            st.info("Calories: 389 kcal | Protein: 16.9g | Carbs: 66g | Fats: 6.9g")
        elif "rice" in search_query or "ارز" in search_query:
            st.write("**Item:** White Rice (Cooked - 100g)")
            st.info("Calories: 130 kcal | Protein: 2.7g | Carbs: 28g | Fats: 0.3g")
        else:
            st.error(f"No item found for '{search_query}' in local database.")

# =========================================================
# التبويب الثالث: حاسبة الوزن المثالي
# =========================================================
with tab3:
    st.header("Ideal Weight Range Calculator")
    bmi_height_input = st.text_input("Enter height in cm:", value="175", key="t3_height_text")

    if st.button("Calculate Ideal Weight Range ⚖️", use_container_width=True):
        try:
            bmi_height = float(bmi_height_input)
            height_m = bmi_height / 100
            min_ideal_weight = 18.5 * (height_m ** 2)
            max_ideal_weight = 24.9 * (height_m ** 2)

            st.success("IDEAL WEIGHT REPORT")
            st.write(f"**Height:** {bmi_height:.0f} cm")
            st.metric("Healthy Weight Range", f"{min_ideal_weight:.1f} kg - {max_ideal_weight:.1f} kg")
        except ValueError:
            st.error("Please enter a valid number for height.")

# =========================================================
# التبويب الرابع: جرعات المكملات
# =========================================================
with tab4:
    st.header("Supplement Dosage Calculator (Age 16+)")
    supp_age_input = st.text_input("Enter your age:", value="18", key="t4_age_text")

    try:
        supp_age = float(supp_age_input)
        if supp_age < 16:
            st.error("[!] Supplement guidance is designed for individuals aged 16 and above.")
            st.info("For your age group, focus primarily on whole foods and adequate sleep!")
        else:
            supp_weight_input = st.text_input("Enter your weight in kg:", value="75", key="t4_weight_text")
            training = st.radio("Do you practice resistance/weight training?", ["yes", "no"], key="t4_training")

            if st.button("Get Supplement Dosage 💊", use_container_width=True):
                supp_weight = float(supp_weight_input)
                st.success("RECOMMENDED SUPPLEMENT DOSAGES")

                if training == "yes":
                    creatine_dose = "7 - 10 grams / day (Consistently)" if supp_weight >= 100 else "5 grams / day (Consistently)"
                else:
                    creatine_dose = "Not required (Optional for non-athletes)"

                whey_dose = "1 to 2 Scoops / day (To fill daily protein gap)" if training == "yes" else "1 Scoop / day (Only if diet lacks protein)"

                st.write(f"• **Creatine Monohydrate:** {creatine_dose}")
                st.write(f"• **Whey Protein:** {whey_dose}")
                st.write("• **Omega-3 Fish Oil:** 1000 - 2000 mg / day (With meals)")
                st.write("• **Multivitamin / Zinc:** 1 Tablet / day (General health support)")
    except ValueError:
        st.error("Please enter valid numbers.")

# =========================================================
# التبويب الخامس الجديد: حاسبة قوة التمرين (1RM)
# =========================================================
with tab5:
    st.header("1RM Strength & Percentage Calculator")
    st.caption("Calculate your One-Rep Max based on the Epley Formula.")

    weight_lifted_input = st.text_input("Weight Lifted (kg):", value="80", key="t5_w")
    reps_input = st.text_input("Reps Performed:", value="5", key="t5_r")

    if st.button("Calculate 1RM 🏋️‍♂️", use_container_width=True):
        try:
            w = float(weight_lifted_input)
            r = float(reps_input)

            if r == 1:
                one_rm = w
            else:
                one_rm = w * (1 + (r / 30))

            st.success(f"Estimated 1RM: **{one_rm:.1f} kg**")

            st.subheader("Training Load Percentages:")
            st.write(f"• **90% (Strength):** {one_rm * 0.90:.1f} kg")
            st.write(f"• **80% (Hypertrophy):** {one_rm * 0.80:.1f} kg")
            st.write(f"• **70% (Endurance):** {one_rm * 0.70:.1f} kg")
        except ValueError:
            st.error("Please enter valid numbers for weight and reps.")