# 🚌 ROUTELESS // Dynamic Rural Student Transit & Crisis Command

**ROUTELESS** is an interactive, AI-assisted rural transit dispatch and simulation web application built with **Streamlit**, **Plotly**, and **gTTS (Google Text-to-Speech)**. Designed with a high-contrast, beginner-friendly, and gamified interface, it empowers dispatchers, students, children, and elderly community members to monitor live bus fleets, simulate weather/breakdown crises, and dispatch students safely to school or exam centers.

## ✨ Key Features

* **🌐 Multilingual Voice & UI Support:** Full interface and real-time audio announcements in **English**, **हिन्दी (Hindi)**, and **ಕನ್ನಡ (Kannada)**.

* **➕ Direct Student Dispatch & Boarding Passes:** Register walk-in or priority students, assign them to active Government Express Buses or Micro-Feeder Auto-Rickshaws, and generate instant priority boarding tickets with voice confirmation.

* **⚡ 1-Click Crisis & Weather Presets:** Instantly test how the transit network adapts to:

  * *Exam Rush & Rain Challenge* (Disabled buses + +40% crowd surge + flooded bridge)

  * *Perfect Sunny Day* (Nominal operations)

  * *Super Flood & Heavy Trouble* (Severe fleet reduction + landslide/flood detours)

* **🎮 Interactive Live Route Simulator:** Watch buses and feeder shuttles move across rural village corridors (Harohalli, Maralawadi, Sathanur, Kodihalli, Uyyamballi) toward the Kanakapura Edu Hub, automatically rerouting around flooded roads.

* **📊 Real-Time Crowd & Fleet Analytics:** High-contrast interactive bar and donut charts tracking student distribution by village and transport mode allocation.

* **🤖 Friendly Multilingual AI Assistant:** Ask questions via quick-action buttons or chat to check seat coverage, road weather status, or look up individual student boarding assignments by ID or name.

## 🛠️ Tech Stack

* **Frontend & Framework:** [Streamlit](https://streamlit.io/) (Custom high-contrast CSS & keyframe animations)

* **Data Processing:** `pandas`, `numpy`

* **Interactive Visualizations & Maps:** `plotly` (`plotly.express` & `plotly.graph_objects`)

* **Text-to-Speech (Voice AI):** `gTTS` (Google Text-to-Speech)

## 🚀 Installation & Local Setup

1. **Clone the repository:**

   ```
   git clone https://github.com/your-username/routeless.git
   cd routeless
   
   ```

2. **Install the required dependencies:**
   Create a `requirements.txt` file (if not already present) with:

   ```
   streamlit
   pandas
   numpy
   plotly
   gTTS
   
   ```

   Then run:

   ```
   pip install -r requirements.txt
   
   ```

3. **Run the application:**

   ```
   streamlit run app.py
   
   ```

## 🎯 How to Use

1. **Choose Your Language:** Use the top-left sidebar dropdown to switch between **English**, **Hindi**, or **Kannada**.

2. **Test Scenarios:** Click any of the **Fun Quick Scenarios** buttons or adjust the sliders in the sidebar to simulate broken buses, exam crowd surges, or blocked roads.

3. **Dispatch a Student:** Open the **➕ Add & Send a Student** tab, enter a student's name and village stop, pick an available bus or auto-rickshaw, and click **Send Student to School!**

4. **Simulate & Track:** Explore the **🎮 Interactive Bus Game Map** to animate vehicle progress, or use the **🤖 Friendly AI Voice Helper** to query student statuses hands-free.

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).