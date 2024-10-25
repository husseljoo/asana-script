import re
import os


def parse_task_file(file_path):
    tasks = []
    with open(file_path, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]
        # print(lines)

        for i in range(0, len(lines), 6):
            name = lines[i].strip().replace("-", "_").replace(" ", "_")
            name = re.sub(r"_{2,}", "_", name)
            task = {
                "task_name": name,
                "company_name": lines[i + 1],
                "task_type": lines[i + 2].lower(),
                "topic_section": lines[i + 3],
                "asana_link": lines[i + 4],
                "gemspec_link": lines[i + 5],
            }
            tasks.append(task)
    return tasks


def create_todo_file(task_names, output_path, mode="w"):
    todo_content = "\n".join(f"- [ ] [[{task}]]" for task in task_names)

    with open(output_path, mode, encoding="utf-8") as file:
        file.write("\n")
        file.write(todo_content + "\n\n")
        file.write("\n")


file_path = "./tasks.txt"
tasks = parse_task_file(file_path)

# create the todofile
todo_path = "/home/husseljo/obsidian/cybersecurity/gematik-test/asana_todos.md"
task_names = [task["task_name"] for task in tasks]
create_todo_file(task_names, todo_path, mode="w")
print(f"created todo: {todo_path}")
# # Append more tasks if needed
# more_task_names = ["Task 6 - Performance Optimization", "Task 7 - Deployment"]
# create_todo_file(more_task_names, output_path, mode="a")

# create the notes themselves
BASE_DIR = "/home/husseljo/obsidian/cybersecurity/gematik-test"
os.makedirs(BASE_DIR, exist_ok=True)
task_types = {"progu": "ProGu", "sigu": "SiGu", "bsi": "BSI"}

for task in tasks:

    task_dir = os.path.join(BASE_DIR, task["company_name"], task_types[task["task_type"]], task["topic_section"].lower())
    os.makedirs(task_dir, exist_ok=True)
    file_path = os.path.join(task_dir, task["task_name"] + ".md")

    with open(file_path, "a", encoding="utf-8") as file:
        file.write("\n")
        file.write(f"[asana_link ]({task['asana_link']})\n")
        file.write(f"[gemspec_link]({task['gemspec_link']})\n")
        file.write("\n")

    print(f"Created {file_path}")
