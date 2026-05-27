"""Script to generate a sample Excel file for testing"""
import pandas as pd

tasks = [
    {"Task": "Finalize Q2 report", "Assignee": "Alessandro", "Due Date": "2026-05-30", "Status": "In Progress", "Priority": "High"},
    {"Task": "Review design mockups", "Assignee": "Marco", "Due Date": "2026-05-28", "Status": "Todo", "Priority": "Medium"},
    {"Task": "Update API documentation", "Assignee": "Sara", "Due Date": "2026-06-01", "Status": "Done", "Priority": "Low"},
    {"Task": "Client presentation prep", "Assignee": "Alessandro", "Due Date": "2026-05-29", "Status": "In Progress", "Priority": "High"},
    {"Task": "Bug fixes sprint 12", "Assignee": "Dev Team", "Due Date": "2026-06-05", "Status": "Todo", "Priority": "Medium"},
]

df = pd.DataFrame(tasks)
df.to_excel("sample_tasks.xlsx", index=False)
print("Created sample_tasks.xlsx")
