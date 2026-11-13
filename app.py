
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Management", page_icon="🎓")

st.title("🎓 Student Record Management System")
st.write("Perform Create, Read, Update and Delete operations.")

# Initialize student records
if "students" not in st.session_state:
    st.session_state.students = [
        {"Roll No": 101, "Name": "Aman", "Age": 20, "Course": "CSE"},
        {"Roll No": 102, "Name": "Simran", "Age": 21, "Course": "AI"},
        {"Roll No": 103, "Name": "Rahul", "Age": 20, "Course": "IT"}
    ]

students = st.session_state.students

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Add Student",
    "View Students",
    "Update Student",
    "Delete Student"
])

# ---------------- CREATE ----------------
with tab1:
    st.subheader("Add New Student")

    with st.form("add_form"):
        roll = st.number_input("Roll Number", min_value=1, step=1)
        name = st.text_input("Student Name")
        age = st.number_input("Age", min_value=1, max_value=100)
        course = st.selectbox("Course", ["CSE", "AI", "IT", "ECE"])

        submit = st.form_submit_button("Add Student")

        if submit:
            if not name.strip():
                st.error("Please enter student name.")
            elif any(s["Roll No"] == roll for s in students):
                st.error("Roll number already exists!")
            else:
                students.append({
                    "Roll No": int(roll),
                    "Name": name.strip(),
                    "Age": int(age),
                    "Course": course
                })
                st.success("Student added successfully!")

# ---------------- READ ----------------
with tab2:
    st.subheader("All Student Records")

    if students:
        df = pd.DataFrame(students)
        st.dataframe(df, hide_index=True, use_container_width=True)
        st.write("Total Students:", len(students))
    else:
        st.info("No student records available.")

# ---------------- UPDATE ----------------
with tab3:
    st.subheader("Update Student Details")

    if students:
        roll_numbers = [s["Roll No"] for s in students]

        selected_roll = st.selectbox(
            "Select Roll Number",
            roll_numbers,
            key="update_roll"
        )

        student = next(
            s for s in students if s["Roll No"] == selected_roll
        )

        with st.form("update_form"):
            new_name = st.text_input("Student Name", value=student["Name"])
            new_age = st.number_input(
                "Age", min_value=1, max_value=100,
                value=student["Age"]
            )
            new_course = st.selectbox(
                "Course",
                ["CSE", "AI", "IT", "ECE"],
                index=["CSE", "AI", "IT", "ECE"].index(student["Course"])
            )

            update = st.form_submit_button("Update Student")

            if update:
                if not new_name.strip():
                    st.error("Name cannot be empty.")
                else:
                    student["Name"] = new_name.strip()
                    student["Age"] = int(new_age)
                    student["Course"] = new_course
                    st.success("Student record updated!")

    else:
        st.info("No records available to update.")

# ---------------- DELETE ----------------
with tab4:
    st.subheader("Delete Student Record")

    if students:
        roll_numbers = [s["Roll No"] for s in students]

        delete_roll = st.selectbox(
            "Select Roll Number to Delete",
            roll_numbers,
            key="delete_roll"
        )

        if st.button("Delete Student", type="primary"):
            st.session_state.students = [
                s for s in students if s["Roll No"] != delete_roll
            ]
            st.success("Student deleted successfully!")
            st.rerun()

    else:
        st.info("No records available to delete.")
