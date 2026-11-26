
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Task Management System")

# Create Task
st.header("Create Task")

with st.form("create_task"):
    title = st.text_input("Task Title")
    description = st.text_area("Description")
    priority = st.selectbox("Priority", ["low", "medium", "high"])

    submitted = st.form_submit_button("Create Task")

    if submitted:
        task_data = {
            "title": title,
            "description": description or None,
            "priority": priority,
            "status": "pending",
            "due_date": None
        }

        try:
            response = requests.post(
                f"{API_URL}/tasks",
                json=task_data
            )

            if response.status_code == 201:
                st.success("Task created successfully!")
            else:
                st.error(response.text)

        except requests.exceptions.RequestException:
            st.error("Could not connect to FastAPI.")

st.divider()

# View Tasks
st.header("All Tasks")

try:
    response = requests.get(f"{API_URL}/tasks")

    if response.status_code == 200:
        tasks = response.json()

        if tasks:
            for task in tasks:
                st.subheader(f"{task['id']}. {task['title']}")
                st.write("Description:", task["description"])
                st.write("Status:", task["status"])
                st.write("Priority:", task["priority"])
                st.divider()
        else:
            st.info("No tasks found.")

except requests.exceptions.RequestException:
    st.error("Could not connect to FastAPI.")

# Update Task Status
st.header("Update Task Status")

task_id = st.number_input("Enter Task ID", min_value=1, step=1)

new_status = st.selectbox(
    "New Status",
    ["pending", "in_progress", "completed"]
)

if st.button("Update Status"):
    try:
        response = requests.patch(
            f"{API_URL}/tasks/{task_id}",
            json={"status": new_status}
        )

        if response.status_code == 200:
            st.success("Task status updated successfully!")
        else:
            st.error(response.text)

    except requests.exceptions.RequestException:
        st.error("Could not connect to FastAPI.")

# Delete Task
st.header("Delete Task")

delete_id = st.number_input(
    "Enter Task ID to Delete",
    min_value=1,
    step=1,
    key="delete_id"
)

if st.button("Delete Task"):
    try:
        response = requests.delete(
            f"{API_URL}/tasks/{delete_id}"
        )

        if response.status_code == 200:
            st.success("Task deleted successfully!")
        else:
            st.error(response.text)

    except requests.exceptions.RequestException:
        st.error("Could not connect to FastAPI.")
