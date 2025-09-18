

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from jinja2 import Environment, FileSystemLoader
from PIL import Image, ImageTk
import os, shutil
from github import Github

class ReadmeBuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub README Builder")
        self.root.geometry("850x900")
        self.root.resizable(True, True)

        os.makedirs('templates', exist_ok=True)
        os.makedirs('output', exist_ok=True)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.template_dir = os.path.join(script_dir, 'templates')
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        self.templates = self.load_templates(self.template_dir)

        self.build_scrollable_ui()

    def load_templates(self, template_dir):
        templates = [f for f in os.listdir(template_dir) if f.endswith('.txt')]
        if not templates:
            messagebox.showwarning("Templates Missing", "No templates found in 'templates' folder.")
        return templates

    def build_scrollable_ui(self):
        canvas = tk.Canvas(self.root)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.entries = {}
        fields = [
            ("Project Name", "entry_name", False),
            ("Description", "entry_desc", True),
            ("Feature 1", "entry_feat1", False),
            ("Feature 2", "entry_feat2", False),
            ("Installation Steps", "entry_install", True),
            ("Tech Stack", "entry_tech", False),
            ("GitHub Link", "entry_git", False),
            ("LinkedIn Link", "entry_linkedin", False),
            ("Screenshot Path", "entry_screenshot", False)
        ]

        for label_text, var_name, multiline in fields:
            frame = tk.Frame(scroll_frame)
            frame.pack(pady=4, fill='x', padx=10)
            tk.Label(frame, text=label_text, width=18, anchor="w").pack(side="left")
            if multiline:
                text_widget = tk.Text(frame, height=4, width=60, wrap='word')
                text_widget.pack(side="left", padx=5)
                self.entries[var_name] = text_widget
            else:
                entry = tk.Entry(frame, width=60)
                entry.pack(side="left", padx=5)
                self.entries[var_name] = entry

        tk.Button(scroll_frame, text="Upload Screenshot", command=self.upload_screenshot, width=20).pack(pady=5)

        template_frame = tk.Frame(scroll_frame)
        template_frame.pack(pady=5)
        tk.Label(template_frame, text="Select Template Style:").pack(side="left")
        self.template_var = tk.StringVar(value=self.templates[0] if self.templates else "")
        self.template_menu = ttk.OptionMenu(template_frame, self.template_var, self.template_var.get(), *self.templates)
        self.template_menu.pack(side="left", padx=5)

        tk.Label(scroll_frame, text="Screenshot Preview:").pack()
        self.image_label = tk.Label(scroll_frame)
        self.image_label.pack(pady=10)

        tk.Label(scroll_frame, text="README Preview:").pack()
        self.preview_box = tk.Text(scroll_frame, height=16, width=95, wrap='word')
        self.preview_box.pack(pady=10)
        self.preview_box.config(state='disabled')

        btn_frame = tk.Frame(scroll_frame)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Preview", command=self.preview_readme, bg="#1976d2", fg="white", width=20).pack(side='left', padx=10)
        tk.Button(btn_frame, text="Generate README", command=self.generate_readme, bg="#388e3c", fg="white", width=20).pack(side='left', padx=10)
        tk.Button(btn_frame, text="Push to GitHub", command=self.push_to_github, bg="#333", fg="white", width=20).pack(side='left', padx=10)

        tk.Button(scroll_frame, text="Clear All Fields", command=self.clear_fields, bg="#f44336", fg="white", width=20).pack(pady=5)

    # Upload screenshot and show preview
    def upload_screenshot(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
        if path:
            filename = os.path.basename(path)
            dest_path = os.path.join('output', filename)
            shutil.copy(path, dest_path)
            widget = self.entries['entry_screenshot']
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
                widget.insert(0, filename)
            self.show_image_preview(dest_path)

    def show_image_preview(self, image_path):
        try:
            img = Image.open(image_path)
            img.thumbnail((300, 200))
            self.img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.img_tk)
            self.image_label.image = self.img_tk
        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load image: {e}")

    def collect_data(self):
        return {
            'project_name': self.get_text_from_entry('entry_name'),
            'description': self.get_text_from_entry('entry_desc'),
            'feature_1': self.get_text_from_entry('entry_feat1'),
            'feature_2': self.get_text_from_entry('entry_feat2'),
            'installation_steps': self.get_text_from_entry('entry_install'),
            'tech_stack': self.get_text_from_entry('entry_tech'),
            'github_link': self.get_text_from_entry('entry_git'),
            'linkedin_link': self.get_text_from_entry('entry_linkedin'),
            'screenshot': self.get_text_from_entry('entry_screenshot')
        }

    def get_text_from_entry(self, name):
        widget = self.entries.get(name)
        if isinstance(widget, tk.Entry):
            return widget.get()
        elif isinstance(widget, tk.Text):
            return widget.get("1.0", tk.END).strip()
        return 

    def preview_readme(self):
        data = self.collect_data()
        selected_template = self.template_var.get()
        try:
            template = self.env.get_template(selected_template)
            output = template.render(data)
            self.preview_box.config(state='normal')
            self.preview_box.delete("1.0", tk.END)
            self.preview_box.insert(tk.END, output)
            self.preview_box.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Preview Error", str(e))

    def generate_readme(self):
       # data = self.collect_data()
        #selected_template = self.template_var.get()
        try:
            print("Generate README clicked")      #debug
            data = self.collect_data()
            template = self.env.get_template(self.template_var.get())
            output = template.render(data)
            output_path = os.path.join('output', 'README.md')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output)
            messagebox.showinfo("Success", f"README.md generated in {output_path}")
        except Exception as e:
            messagebox.showerror("File Write Error", f"Failed to write README.md: {e}")

    def push_to_github(self):
        from tkinter.simpledialog import askstring
        token = askstring("GitHub Token", "Enter your GitHub personal access token:")
        repo_name = askstring("GitHub Repo", "Enter your GitHub repo (username/reponame):")
        if not token or not repo_name:
            messagebox.showwarning("Missing Info", "GitHub token and repository are required.")
            return
        output_path = os.path.join('output', 'README.md')
        if not os.path.exists(output_path):
            messagebox.showerror("Missing File", "README.md not found. Please generate the file first.")
            return

        try:
            g = Github(token)
            repo = g.get_repo(repo_name)
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
            contents = None
            try:
                contents = repo.get_contents("README.md")
                repo.update_file("README.md", "Update README via desktop app", content, contents.sha)
            except Exception:
                repo.create_file("README.md", "Create README via desktop app", content)
            screenshot_file = self.get_text_from_entry('entry_screenshot')
            if screenshot_file and os.path.exists(os.path.join('output', screenshot_file)):
                img_path = os.path.join('output', screenshot_file)
                try:
                    with open(img_path, 'rb') as f:
                        img_data = f.read()
                    img_contents = None
                    try:
                        img_contents = repo.get_contents(screenshot_file)
                        repo.update_file(screenshot_file, "Update screenshot via desktop app", img_data, img_contents.sha)
                    except Exception:
                        repo.create_file(screenshot_file, "Upload screenshot via desktop app", img_data)
                except Exception as img_error:
                    messagebox.showwarning("Image Upload Error", f"Image not uploaded: {img_error}")
            messagebox.showinfo("Success", "README.md and screenshot pushed to GitHub.")
        except Exception as e:
            messagebox.showerror("GitHub Error", f"Failed to push to GitHub: {e}")

    def clear_fields(self):
        for widget in self.entries.values():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)
        if self.templates:
            self.template_var.set(self.templates[0])
        self.image_label.config(image='')
        self.image_label.image = None
        self.preview_box.config(state='normal')
        self.preview_box.delete("1.0", tk.END)
        self.preview_box.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = ReadmeBuilderApp(root)
    root.mainloop()
