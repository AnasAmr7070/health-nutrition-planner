import streamlit as st
import plotly.express as px
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

st.set_page_config(
    page_title="Elite Fitness & Nutrition Suite Pro",
    page_icon="⚡",
    layout="centered"
)

# =========================================================
# Custom Luxury CSS Styling
# =========================================================
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f19;
        color: #f8fafc;
    }
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #4ade80);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 25px;
    }
    .stButton > button {
        background: linear-gradient(90deg, #0284c7, #0369a1);
        color: white;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        transition: 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #38bdf8, #0284c7);
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
    }
    div[data-testid="stMetricValue"] {
        color: #38bdf8;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">⚡ ELITE FITNESS & NUTRITION SUITE</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Discipline, Power & Aesthetic Mastery - Your Ultimate Professional Hub.</p>', unsafe_allow_html=True)

st.divider()

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "📊 Calories", 
    "🔍 Food DB", 
    "⚖️ Ideal Wt", 
    "💊 Supps",
    "🏋️‍♂️ 1RM",
    "💪 Workouts",
    "📈 TDEE",
    "🧊 Body Fat",
    "💧 Hydration",
    "🥗 Swapper"
])

# =========================================================
# Tab 1: Calories, Chart & PDF Export
# =========================================================
with tab1:
    st.markdown("### 📊 Daily Calories, Macros & Water Calculator")
    
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

    if st.button("Calculate Targets 🚀", use_container_width=True, key="btn_t1"):
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
            
            chart_data = {
                "Macro": ["Protein", "Carbs", "Fats"],
                "Grams": [protein, carbs, fats]
            }
            fig = px.pie(chart_data, values="Grams", names="Macro", color="Macro",
                         color_discrete_map={"Protein": "#38bdf8", "Carbs": "#4ade80", "Fats": "#f43f5e"})
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#fff")
            st.plotly_chart(fig, use_container_width=True)

            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            p.setFont("Helvetica-Bold", 16)
            p.drawString(100, 750, "Elite Fitness Planner - Summary Report")
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
# Tab 2: Food Database
# =========================================================
with tab2:
    st.markdown("### 🔍 Search Food Database (Protein & Calories)")
    search_query = st.text_input("Enter food item to search (e.g., chicken, oats, eggs, tuna):", key="t2_search").strip().lower()

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
# Tab 3: Ideal Weight
# =========================================================
with tab3:
    st.markdown("### ⚖️ Ideal Weight Range Calculator")
    bmi_height_input = st.text_input("Enter height in cm:", value="175", key="t3_height_text")

    if st.button("Calculate Ideal Weight Range ⚖️", use_container_width=True, key="btn_t3"):
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
# Tab 4: Supplement Dosage
# =========================================================
with tab4:
    st.markdown("### 💊 Supplement Dosage Calculator (Age 16+)")
    supp_age_input = st.text_input("Enter your age:", value="18", key="t4_age_text")

    try:
        supp_age = float(supp_age_input)
        if supp_age < 16:
            st.error("[!] Supplement guidance is designed for individuals aged 16 and above.")
            st.info("For your age group, focus primarily on whole foods and adequate sleep!")
        else:
            supp_weight_input = st.text_input("Enter your weight in kg:", value="75", key="t4_weight_text")
            training = st.radio("Do you practice resistance/weight training?", ["yes", "no"], key="t4_training")

            if st.button("Get Supplement Dosage 💊", use_container_width=True, key="btn_t4"):
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
# Tab 5: 1RM Strength Calculator
# =========================================================
with tab5:
    st.markdown("### 🏋️‍♂️ 1RM Strength & Percentage Calculator")
    st.caption("Calculate your One-Rep Max based on the Epley Formula.")

    weight_lifted_input = st.text_input("Weight Lifted (kg):", value="80", key="t5_w")
    reps_input = st.text_input("Reps Performed:", value="5", key="t5_r")

    if st.button("Calculate 1RM 🏋️‍♂️", use_container_width=True, key="btn_t5"):
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

# =========================================================
# Tab 6: Workout Splits (8 Comprehensive Training Programs)
# =========================================================
with tab6:
    st.markdown("### 💪 Advanced Workout Splits & Volume Guide")
    st.caption("Choose from 8 professional training routines tailored for muscle hypertrophy and strength.")

    split_choice = st.selectbox("Select Training Program", [
        "1. Arnold Split (Chest/Back, Shoulders/Arms, Legs)",
        "2. Push / Pull / Legs (PPL - 3 Days or 6 Days)",
        "3. Upper / Lower Body Split (4 Days)",
        "4. Bro Split / Body Part Split (5 Days)",
        "5. Full Body Workout (3 Days - Beginner/Intermediate)",
        "6. PHUL Routine (Power Hypertrophy Upper Lower)",
        "7. Upper / Lower / PPL Hybrid (5 Days)",
        "8. German Volume Training - GVT (10x10 Method)"
    ], key="t6_split")

    if "Arnold" in split_choice:
        st.markdown("""
        **🔥 Arnold Split (The Classic Legendary Routine):**
        * **Day 1 & 4 (Chest & Back):** Bench Press, Incline DB Press, Pull-ups, Barbell Rows, Pullovers.
        * **Day 2 & 5 (Shoulders & Arms):** Overhead Press, Lateral Raises, Barbell Curls, Skull Crushers.
        * **Day 3 & 6 (Legs & Abs):** Squats, Romanian Deadlifts, Leg Press, Calf Raises, Hanging Leg Raises.
        """)
    elif "Push / Pull / Legs" in split_choice:
        st.markdown("""
        **⚡ PPL Routine (Push / Pull / Legs):**
        * **Push Day:** Bench Press, Overhead Press, Incline Flyes, Triceps Pushdowns.
        * **Pull Day:** Deadlifts / Barbell Rows, Lat Pulldowns, Face Pulls, Barbell Curls.
        * **Legs Day:** Barbell Squats, Bulgarian Split Squats, Leg Curls, Standing Calf Raises.
        """)
    elif "Upper / Lower" in split_choice:
        st.markdown("""
        **🔄 Upper / Lower Split (Balanced 4-Day Frequency):**
        * **Upper Day 1 & 2:** Bench Press, Bent-Over Rows, Overhead Press, Pull-ups, Biceps/Triceps supersets.
        * **Lower Day 1 & 2:** Barbell Squats, Romanian Deadlifts, Leg Press, Seated Calf Raises.
        """)
    elif "Bro Split" in split_choice:
        st.markdown("""
        **🎯 Classic Bro Split (1 Muscle Group per Day):**
        * **Day 1:** Chest | **Day 2:** Back | **Day 3:** Shoulders | **Day 4:** Arms (Biceps/Triceps) | **Day 5:** Legs.
        """)
    elif "Full Body" in split_choice:
        st.markdown("""
        **🟢 Full Body Routine (3 Days/Week):**
        * Great for beginners or busy schedules. Focuses on compound movements: Squats, Bench Press, Rows, Overhead Press, and Deadlifts.
        """)
    elif "PHUL" in split_choice:
        st.markdown("""
        **⚡ PHUL Routine (Power Hypertrophy Upper Lower):**
        * Combines strength (power days) with higher rep ranges (hypertrophy days) for maximum muscle growth.
        """)
    elif "Hybrid" in split_choice:
        st.markdown("""
        **🔗 Upper / Lower / PPL Hybrid (5 Days):**
        * Upper Body, Lower Body, Push, Pull, Legs. An optimal blend of frequency and recovery.
        """)
    else:
        st.markdown("""
        **💥 German Volume Training (GVT - 10x10):**
        * Advanced shock routine performing 10 sets of 10 reps on main compound lifts to force extreme muscle adaptation.
        """)
    
    st.info("💡 **Volume Rule:** Aim for 10 to 20 working sets per muscle group weekly for optimal hypertrophy.")

# =========================================================
# Tab 7: Adaptive TDEE Tracker
# =========================================================
with tab7:
    st.markdown("### 📈 Adaptive TDEE & Weight Plateau Breaker")
    st.caption("Adjust your daily intake if your weight stalls over 2 weeks.")

    curr_weight = st.text_input("Current Weight (kg):", value="75", key="t7_w")
    current_cals = st.text_input("Current Daily Calories (kcal):", value="2500", key="t7_c")
    weight_trend = st.selectbox("Weight status over the last 2 weeks:", [
        "Dropping steadily (Good for Cut)",
        "Stuck / Plateau (No change)",
        "Gaining too fast"
    ], key="t7_trend")

    if st.button("Get Adaptive Advice 🔄", use_container_width=True, key="btn_t7"):
        if "Stuck" in weight_trend:
            st.warning("⚠️ **Plateau Detected!** Your body has adapted to your current calories.")
            st.info("👉 **Action:** Drop your daily intake by **200 - 300 kcal** or increase daily steps by 2,000 steps.")
        elif "Gaining" in weight_trend:
            st.success("💡 You are in a caloric surplus. If bulking, this is normal. If cutting, reduce fats/carbs by 200 kcal.")
        else:
            st.success("✅ Your current caloric intake is optimal. Keep consistency!")

# =========================================================
# Tab 8: Body Fat & FFMI Calculator
# =========================================================
with tab8:
    st.markdown("### 🧊 Body Fat Percentage & FFMI Estimator")
    st.caption("Estimate your body composition and lean muscle mass index.")

    b_weight = st.text_input("Weight (kg):", value="75", key="t8_w")
    b_height = st.text_input("Height (cm):", value="175", key="t8_h")
    b_waist = st.text_input("Waist Circumference (cm):", value="82", key="t8_waist")

    if st.button("Calculate Body Composition 📊", use_container_width=True, key="btn_t8"):
        try:
            w = float(b_weight)
            h = float(b_height)
            waist = float(b_waist)

            fat_mass = waist * 0.74 - w * 0.08 - 10
            body_fat_pct = max(5.0, min(45.0, (fat_mass / w) * 100))
            lean_mass = w * (1 - (body_fat_pct / 100))
            ffmi = lean_mass / ((h / 100) ** 2)

            st.success("ESTIMATED RESULTS")
            st.metric("Estimated Body Fat", f"{body_fat_pct:.1f}%")
            st.metric("Fat-Free Mass Index (FFMI)", f"{ffmi:.1f}")
            
            if ffmi > 22:
                st.info("💪 Great muscular development (Advanced natural range).")
            else:
                st.info("📈 Keep building solid lean mass through progressive overload and high protein.")
        except ValueError:
            st.error("Please enter valid numeric measurements.")

# =========================================================
# Tab 9: Hydration & Supplement Timing
# =========================================================
with tab9:
    st.markdown("### 💧 Smart Hydration Schedule & Supplement Timing")
    st.caption("Optimize when to take your supplements and water throughout the day.")

    st.markdown("""
    ### ⏰ Supplement Timing Guide:
    * **Creatine Monohydrate:** Any time of day consistently, preferably post-workout with carbs/water.
    * **L-Citrulline / L-Arginine:** 30 to 45 minutes *before* your workout for maximum pump.
    * **Whey Protein:** Post-workout or anytime you need to complete your daily protein target.
    * **Omega-3 & Vitamins:** Taken with your largest meal containing healthy fats for better absorption.

    ### 💧 Daily Water Distribution Schedule:
    * **Morning (Upon waking):** 500 ml (Jumpstart metabolism)
    * **Pre-Workout:** 300 - 400 ml
    * **During Workout:** 150 ml every 15-20 minutes
    * **Post-Workout & Evening:** Remainder of your calculated daily liters.
    """)

# =========================================================
# Tab 10: Macro Swapper & Food Alternatives
# =========================================================
with tab10:
    st.markdown("### 🥗 Food Alternative & Macro Swapper")
    st.caption("Find clean protein or carb substitutes with similar nutritional value.")

    source_food = st.selectbox("Select primary food item you want to swap:", [
        "Chicken Breast (100g)",
        "White Rice (100g cooked)",
        "Oats (100g raw)",
        "Lean Beef (100g)"
    ], key="t10_food")

    if st.button("Find Healthy Alternatives 🔄", use_container_width=True, key="btn_t10"):
        st.success("RECOMMENDED ALTERNATIVES")
        if "Chicken" in source_food:
            st.write("• **Turkey Breast:** Similar high protein, very low fat.")
            st.write("• **White Fish / Tilapia:** Excellent lean protein source.")
            st.write("• **Canned Tuna in Water:** Quick and high protein alternative.")
        elif "Rice" in source_food:
            st.write("• **Sweet Potatoes:** Excellent clean complex carbs and fiber.")
            st.write("• **Quinoa:** High protein grain alternative.")
            st.write("• **Oats / Brown Rice:** Slow-digesting complex carbohydrates.")
        elif "Oats" in source_food:
            st.write("• **Sweet Potato & Eggs:** Great clean morning carbs.")
            st.write("• **Brown Rice Cakes:** Fast digesting pre-workout carb source.")
        else:
            st.write("• **Chicken Breast:** High protein low fat substitute.")
            st.write("• **Salmon / Shrimp:** Great alternative protein sources.")