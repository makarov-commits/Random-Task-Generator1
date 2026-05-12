import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("550x620")

        self.tasks = [
            {"text": "Прочитать статью по Python", "category": "study"},
            {"text": "Сделать утреннюю зарядку", "category": "sport"},
            {"text": "Написать отчёт за неделю", "category": "work"},
            {"text": "Повторить конспект лекции", "category": "study"},
            {"text": "Пробежать 2 км", "category": "sport"},
            {"text": "Ответить на рабочие письма", "category": "work"}
        ]
        self.history = []
        self.history_file = "task_history.json"

        self.category_map = {"Все": "all", "Учёба": "study", "Спорт": "sport", "Работа": "work"}
        self.reverse_category_map = {v: k for k, v in self.category_map.items()}

        self.setup_ui()
        self.load_history()

    def setup_ui(self):
        ttk.Label(self.root, text="Фильтр по типу задачи:").pack(pady=(10, 0))
        self.category_var = tk.StringVar(value="Все")
        self.filter_combo = ttk.Combobox(self.root, textvariable=self.category_var,
                                         values=["Все", "Учёба", "Спорт", "Работа"], state="readonly")
        self.filter_combo.pack(pady=5)

        self.gen_btn = ttk.Button(self.root, text=" Сгенерировать задачу", command=self.generate_task)
        self.gen_btn.pack(pady=10)

        self.current_label = ttk.Label(self.root, text="Нажмите кнопку, чтобы получить задачу", 
                                       font=("Segoe UI", 12, "bold"), wraplength=480, justify="center")
        self.current_label.pack(pady=10)

        ttk.Label(self.root, text=" История сгенерированных задач:").pack(pady=(10, 0))
        self.history_list = tk.Listbox(self.root, height=10, width=65, font=("Consolas", 10))
        self.history_list.pack(pady=5)

        add_frame = ttk.LabelFrame(self.root, text=" Добавить новую задачу")
        add_frame.pack(pady=10, fill="x", padx=10)

        self.new_task_entry = ttk.Entry(add_frame, font=("Segoe UI", 11))
        self.new_task_entry.pack(side="left", padx=(10, 5), fill="x", expand=True)
        
        self.new_cat_var = tk.StringVar(value="Учёба")
        self.new_cat_combo = ttk.Combobox(add_frame, textvariable=self.new_cat_var,
                                          values=["Учёба", "Спорт", "Работа"], width=10, state="readonly")
        self.new_cat_combo.pack(side="left", padx=5)
        
        self.add_btn = ttk.Button(add_frame, text="Добавить", command=self.add_task)
        self.add_btn.pack(side="left", padx=(5, 10))

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text=" Сохранить историю", command=self.save_history).pack(side="left", padx=5)
        ttk.Button(btn_frame, text=" Загрузить историю", command=self.load_history).pack(side="left", padx=5)

    def get_filtered_tasks(self):
        cat_key = self.category_map[self.category_var.get()]
        if cat_key == "all":
            return self.tasks
        return [t for t in self.tasks if t["category"] == cat_key]

    def generate_task(self):
        filtered = self.get_filtered_tasks()
        if not filtered:
            messagebox.showwarning("Внимание", "В выбранной категории нет задач!")
            return

        chosen = random.choice(filtered)
        record = {
            "text": chosen["text"],
            "category": chosen["category"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(record)
        
        self.current_label.config(
            text=f"[{self.reverse_category_map[chosen['category']]}] {chosen['text']}"
        )
        self.update_history_ui()
        self.save_history()

    def add_task(self):
        new_text = self.new_task_entry.get().strip()
        new_cat = self.category_map[self.new_cat_var.get()]

        if not new_text:
            messagebox.showerror("Ошибка ввода", "Задача не может быть пустой!")
            return

        self.tasks.append({"text": new_text, "category": new_cat})
        self.new_task_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", f"Задача добавлена в список!")

    def save_history(self):
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
                self.update_history_ui()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить историю: {e}")

    def update_history_ui(self):
        self.history_list.delete(0, tk.END)
        for h in reversed(self.history):
            self.history_list.insert(0, f"[{self.reverse_category_map[h['category']]}] {h['text']} | {h['timestamp']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()
