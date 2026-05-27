"""
Slack PM Agent - Reads Excel tasks and posts to Slack channel
"""
import asyncio
import os
from datetime import datetime
import pandas as pd
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()

class SlackPMAgent:
    def __init__(self):
        self.slack_token = os.getenv("SLACK_BOT_TOKEN")
        self.channel_id = os.getenv("SLACK_CHANNEL_ID")
        self.client = WebClient(token=self.slack_token)

    def read_tasks_from_excel(self, file_path: str) -> pd.DataFrame:
        """Read tasks from Excel file"""
        df = pd.read_excel(file_path)
        return df

    def format_task_message(self, task: dict) -> str:
        """Format a task into a PM-style Slack message"""
        message = f"📋 *Task Update*\n"

        if "task" in task or "Task" in task:
            task_name = task.get("task") or task.get("Task")
            message += f"*Task:* {task_name}\n"

        if "assignee" in task or "Assignee" in task:
            assignee = task.get("assignee") or task.get("Assignee")
            message += f"*Assignee:* {assignee}\n"

        if "due_date" in task or "Due Date" in task or "DueDate" in task:
            due = task.get("due_date") or task.get("Due Date") or task.get("DueDate")
            if pd.notna(due):
                if isinstance(due, datetime):
                    due = due.strftime("%Y-%m-%d")
                message += f"*Due:* {due}\n"

        if "status" in task or "Status" in task:
            status = task.get("status") or task.get("Status")
            emoji = "🟢" if status == "Done" else "🟡" if status == "In Progress" else "🔴"
            message += f"*Status:* {emoji} {status}\n"

        if "priority" in task or "Priority" in task:
            priority = task.get("priority") or task.get("Priority")
            message += f"*Priority:* {priority}\n"

        if "notes" in task or "Notes" in task:
            notes = task.get("notes") or task.get("Notes")
            if pd.notna(notes):
                message += f"*Notes:* {notes}\n"

        return message

    def post_message(self, message: str) -> bool:
        """Post a message to Slack channel"""
        try:
            self.client.chat_postMessage(
                channel=self.channel_id,
                text=message,
                mrkdwn=True
            )
            return True
        except SlackApiError as e:
            print(f"Slack API error: {e.response['error']}")
            return False

    def post_summary(self, df: pd.DataFrame) -> bool:
        """Post a summary of all tasks"""
        total = len(df)

        status_col = "status" if "status" in df.columns else "Status" if "Status" in df.columns else None

        summary = f"📊 *Daily Task Summary* - {datetime.now().strftime('%Y-%m-%d')}\n\n"
        summary += f"*Total Tasks:* {total}\n"

        if status_col:
            status_counts = df[status_col].value_counts()
            summary += "\n*By Status:*\n"
            for status, count in status_counts.items():
                emoji = "🟢" if status == "Done" else "🟡" if status == "In Progress" else "🔴"
                summary += f"  {emoji} {status}: {count}\n"

        return self.post_message(summary)

    def run(self, excel_path: str, post_individual: bool = True, post_summary: bool = True):
        """Main entry point - read Excel and post to Slack"""
        print(f"Reading tasks from: {excel_path}")
        df = self.read_tasks_from_excel(excel_path)
        print(f"Found {len(df)} tasks")

        if post_summary:
            print("Posting summary...")
            self.post_summary(df)

        if post_individual:
            print("Posting individual tasks...")
            for _, row in df.iterrows():
                task = row.to_dict()
                message = self.format_task_message(task)
                self.post_message(message)
                print(f"Posted: {task.get('task') or task.get('Task', 'Unknown task')}")

        print("Done!")


async def main():
    agent = SlackPMAgent()
    agent.run("tasks.xlsx")


if __name__ == "__main__":
    asyncio.run(main())
