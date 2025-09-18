'''
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from jinja2 import Environment, FileSystemLoader
from PIL import Image, ImageTk
from PIL import ImageGrab      # for capturing screenshots
import os

# Ensure required folders exist
os.makedirs('templates', exist_ok=True)
os.makedirs('output', exist_ok=True)

def upload_screenshot():
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
    entry_screenshot.delete(0, tk.END)
    entry_screenshot.insert(0, path)

def generate_readme():
    selected_template = template_var.get()
    #env = Environment(loader=FileSystemLoader('templates'))
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(script_dir, 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))

    
    try:
        template = env.get_template(selected_template)
    except Exception as e:
        messagebox.showerror("Template Error", f"Template not found: {selected_template}")
        return

    data = {
        'project_name': entry_name.get(),
        'description': entry_desc.get(),
        'feature_1': entry_feat1.get(),
        'feature_2': entry_feat2.get(),
        'installation_steps': entry_install.get(),
        'tech_stack': entry_tech.get(),
        'github_link': entry_git.get(),
        'linkedin_link': entry_linkedin.get(),
        'screenshot': entry_screenshot.get()
    }

    output = template.render(data)
    preview_box.delete("1.0", tk.END)
    preview_box.insert(tk.END, output)

    with open('output/README.md', 'w',encoding='utf-8') as f:
        f.write(output)

    messagebox.showinfo("Success", "README.md generated in output folder!")

# --- Clear All Fields Function ---
def clear_fields():
    for entry in entries.values():
        entry.delete(0, tk.END)
    preview_box.delete("1.0", tk.END)
    template_var.set("basic_readme.txt")  # Reset dropdown to default

#------implimenting dark mode function
dark_mode = False
def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode

    bg_color = "#121212" if dark_mode else "#ffffff"
    fg_color = "#f0f0f0" if dark_mode else "#000000"

    root.configure(bg=bg_color)

    for widget in root.winfo_children():
        # Skip buttons with custom colors
        if isinstance(widget, tk.Button):
            if widget["text"] == "Generate README":
                continue
            if widget["text"] == "Clear All Fields":
                continue

        try:
            widget.configure(bg=bg_color, fg=fg_color)
        except:
            pass

    preview_box.configure(bg=bg_color, fg=fg_color, insertbackground=fg_color)

#--- screenshot preview function
def handle_screenshot():
    # Your existing screenshot logic
    screenshot_path = "screenshot.png"
    # Save screenshot to file
    image = ImageGrab.grab()
    image.save(screenshot_path)

    # Load and resize for preview
    img = Image.open(screenshot_path)
    img = img.resize((300, 200))  # Adjust size as needed
    img_tk = ImageTk.PhotoImage(img)

    # Update canvas
    image_canvas.config(image=img_tk)
    image_canvas.image = img_tk  # Keep reference to avoid garbage collection

#clear preview 
def clear_preview():
    image_canvas.config(image='')
    image_canvas.image = None

# GUI Setup
root = tk.Tk()
root.title("GitHub Portfolio Builder") 
root.geometry("800x750")

fields = [
    ("Project Name", "entry_name"),
    ("Description", "entry_desc"),
    ("Feature 1", "entry_feat1"),
    ("Feature 2", "entry_feat2"),
    ("Installation Steps", "entry_install"),
    ("Tech Stack", "entry_tech"),
    ("GitHub Link", "entry_git"),
    ("LinkedIn Link", "entry_linkedin"),
    ("Screenshot Path", "entry_screenshot")
]

entries = {}
for label_text, var_name in fields:
    frame = tk.Frame(root)
    frame.pack(pady=4)
    label = tk.Label(frame, text=label_text, width=18, anchor="w")
    label.pack(side="left")
    entry = tk.Entry(frame, width=60)
    entry.pack(side="left")
    entries[var_name] = entry

entry_name = entries["entry_name"]
entry_desc = entries["entry_desc"]
entry_feat1 = entries["entry_feat1"]
entry_feat2 = entries["entry_feat2"]
entry_install = entries["entry_install"]
entry_tech = entries["entry_tech"]
entry_git = entries["entry_git"]
entry_linkedin = entries["entry_linkedin"]
entry_screenshot = entries["entry_screenshot"]

# Screenshot Upload Button
upload_btn = tk.Button(root, text="Upload Screenshot", command=upload_screenshot)
upload_btn.pack(pady=5)

# Template Selector
template_frame = tk.Frame(root)
template_frame.pack(pady=5)
tk.Label(template_frame, text="Select Template Style:").pack(side="left")
template_var = tk.StringVar(value="basic_readme.txt")
template_options = ["basic_readme.txt", "emoji_readme.txt", "minimal_readme.txt"]
template_menu = tk.OptionMenu(template_frame, template_var, *template_options)
template_menu.pack(side="left")

# Generate Button
generate_btn = tk.Button(root, text="Generate README", command=generate_readme, bg="#4CAF50", fg="white", height=2, width=30)
generate_btn.pack(pady=10)
clear_btn = tk.Button(root, text="Clear All Fields", command=clear_fields, bg="#f44336", fg="white", height=2, width=30)
clear_btn.pack(pady=5)

#--- generating toggle button ---
dark_btn = tk.Button(root, text="Toggle Dark Mode", command=toggle_dark_mode, bg="#333", fg="white", height=2, width=30)
dark_btn.pack(pady=5)

# Preview Box
tk.Label(root, text="Live Preview:").pack()
preview_box = tk.Text(root, height=15, width=95)
preview_box.pack(pady=10)

# for screenshot
screenshot_button = ttk.Button(root, text="Capture Screenshot", command=handle_screenshot)
screenshot_button.pack(pady=(0, 5))

clear_button = ttk.Button(root, text="Clear Preview", command=clear_preview)
clear_button.pack()

root.mainloop()
'''



import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from jinja2 import Environment, FileSystemLoader
from PIL import Image, ImageTk, ImageGrab
import os, shutil
import uuid

class ReadmeBuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub README Builder")
        self.root.geometry("820x800")
        
        # Create necessary folders if not exist
        os.makedirs('templates', exist_ok=True)
        os.makedirs('output', exist_ok=True)
        os.makedirs('screenshots', exist_ok=True)
        
        #self.dark_mode = False
        
        # Setup Jinja environment for templates
        script_dir = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(script_dir, 'templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))
        
        # Load templates dynamically
        self.templates = self.load_templates(template_dir)
        
        # Build UI components
        self.build_ui()
    
    def load_templates(self, template_dir):
        # Scan the templates folder for .txt files to populate templates list
        templates = []
        for file in os.listdir(template_dir):
            if file.endswith('.txt'):
                templates.append(file)
        if not templates:
            messagebox.showwarning("Templates Missing", "No templates found in 'templates' folder.")
        return templates
    
    def build_ui(self):
        # Define input fields with possible multiline ones
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

        self.entries = {}
        for label_text, var_name, multiline in fields:
            frame = tk.Frame(self.root, bg=self.get_bg())
            frame.pack(pady=4, fill='x', padx=10)
            
            label = tk.Label(frame, text=label_text, width=18, anchor="w", bg=self.get_bg(), fg=self.get_fg())
            label.pack(side="left")
            
            if multiline:
                text_widget = tk.Text(frame, height=4, width=60, wrap='word', bg=self.get_entry_bg(), fg=self.get_fg(), insertbackground=self.get_fg())
                text_widget.pack(side="left", padx=5)
                self.entries[var_name] = text_widget
            else:
                entry = tk.Entry(frame, width=60, bg=self.get_entry_bg(), fg=self.get_fg(), insertbackground=self.get_fg())
                entry.pack(side="left", padx=5)
                self.entries[var_name] = entry

        # Screenshot upload button
        upload_btn = tk.Button(self.root, text="Upload Screenshot", command=self.upload_screenshot, bg=self.get_btn_bg(), fg=self.get_btn_fg(), height=1, width=20)
        upload_btn.pack(pady=5)
        
        # Template Selector
        template_frame = tk.Frame(self.root, bg=self.get_bg())
        template_frame.pack(pady=5)
        
        tk.Label(template_frame, text="Select Template Style:", bg=self.get_bg(), fg=self.get_fg()).pack(side="left")
        self.template_var = tk.StringVar(value=self.templates[0] if self.templates else "")
        self.template_menu = ttk.OptionMenu(template_frame, self.template_var, self.template_var.get(), *self.templates)
        self.template_menu.pack(side="left", padx=5)
        
        # Generate and clear buttons
        generate_btn = tk.Button(self.root, text="Generate README", command=self.generate_readme, bg="#4CAF50", fg="white", height=2, width=30)
        generate_btn.pack(pady=10)
        
        clear_btn = tk.Button(self.root, text="Clear All Fields", command=self.clear_fields, bg="#f44336", fg="white", height=2, width=30)
        clear_btn.pack(pady=5)
        
        # Dark mode toggle
        #self.dark_btn = tk.Button(self.root, text="Toggle Dark Mode", command=self.toggle_dark_mode, bg="#333", fg="white", height=2, width=30)
        #self.dark_btn.pack(pady=5)
        
        # Live preview label and text box
        tk.Label(self.root, text="Live Preview:", bg=self.get_bg(), fg=self.get_fg()).pack()
        self.preview_box = tk.Text(self.root, height=15, width=95, bg=self.get_entry_bg(), fg=self.get_fg(), insertbackground=self.get_fg())
        self.preview_box.pack(pady=10)
        
        # Screenshot capture and preview
        screenshot_frame = tk.Frame(self.root, bg=self.get_bg())
        screenshot_frame.pack(pady=5)
        
        capture_btn = ttk.Button(screenshot_frame, text="Capture Screenshot", command=self.handle_screenshot)
        capture_btn.pack(side='left', padx=5)
        
        clear_preview_btn = ttk.Button(screenshot_frame, text="Clear Preview", command=self.clear_preview)
        clear_preview_btn.pack(side='left', padx=5)
        
        self.image_label = tk.Label(self.root, bg=self.get_bg())
        self.image_label.pack(pady=10)
        
    def get_bg(self):
        return "#121212" if self.dark_mode else "#ffffff"
    
    def get_fg(self):
        return "#f0f0f0" if self.dark_mode else "#000000"
    
    def get_entry_bg(self):
        return "#232323" if self.dark_mode else "#ffffff"
    
    def get_btn_bg(self):
        return "#222222" if self.dark_mode else "#4CAF50"
    
    def get_btn_fg(self):
        return "#f0f0f0" if self.dark_mode else "#ffffff"
    
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

    '''def upload_screenshot(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
        if path:
            widget = self.entries['entry_screenshot']
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
                widget.insert(0, path)
            self.show_image_preview(path)

    def show_image_preview(self, image_path):
        try:
            img = Image.open(image_path)
            img.thumbnail((300, 200))
            self.img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.img_tk)
        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load image: {e}")'''
    
    def generate_readme(self):
        # Basic validation
        project_name = self.get_text_from_entry('entry_name')
        if not project_name.strip():
            messagebox.showwarning("Input Required", "Project Name is required!")
            return
        
        selected_template = self.template_var.get()
        try:
            template = self.env.get_template(selected_template)
        except Exception:
            messagebox.showerror("Template Error", f"Template not found: {selected_template}")
            return
        
        data = {
            'project_name': project_name,
            'description': self.get_text_from_entry('entry_desc'),
            'feature_1': self.get_text_from_entry('entry_feat1'),
            'feature_2': self.get_text_from_entry('entry_feat2'),
            'installation_steps': self.get_text_from_entry('entry_install'),
            'tech_stack': self.get_text_from_entry('entry_tech'),
            'github_link': self.get_text_from_entry('entry_git'),
            'linkedin_link': self.get_text_from_entry('entry_linkedin'),
            'screenshot': self.get_text_from_entry('entry_screenshot')
        }
        
        output = template.render(data)
        self.preview_box.delete("1.0", tk.END)
        self.preview_box.insert(tk.END, output)
        
        try:
            output_path = os.path.join('output', 'README.md')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output)
            messagebox.showinfo("Success", f"README.md generated in {output_path}")
        except Exception as e:
            messagebox.showerror("File Write Error", f"Failed to write README.md: {e}")
    
    def get_text_from_entry(self, name):
        widget = self.entries.get(name)
        if isinstance(widget, tk.Entry):
            return widget.get()
        elif isinstance(widget, tk.Text):
            return widget.get("1.0", tk.END).strip()
        return ""
    
    def clear_fields(self):
        for widget in self.entries.values():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)
        self.preview_box.delete("1.0", tk.END)
        if self.templates:
            self.template_var.set(self.templates[0])
        self.clear_preview()
    
    '''def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        bg = self.get_bg()
        fg = self.get_fg()
        entry_bg = self.get_entry_bg()
        
        self.root.configure(bg=bg)
        
        # Update all widgets colors
        for widget in self.root.winfo_children():
            if isinstance(widget, (tk.Frame, tk.Label, tk.Button, tk.Text)):
                try:
                    widget.configure(bg=bg, fg=fg)
                except:
                    pass
                
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    try:
                        if isinstance(child, tk.Text):
                            child.configure(bg=entry_bg, fg=fg, insertbackground=fg)
                        else:
                            child.configure(bg=bg, fg=fg)
                    except:
                        pass
        
        # Update buttons with special colors
        # Update Generate and Clear buttons specifically
        for btn in self.root.winfo_children():
            if isinstance(btn, tk.Button):
                if btn["text"] == "Generate README":
                    btn.configure(bg="#4CAF50", fg="white")
                elif btn["text"] == "Clear All Fields":
                    btn.configure(bg="#f44336", fg="white")
                elif btn["text"] == "Toggle Dark Mode":
                    btn.configure(bg="#333", fg="white")
        
        # Update preview box separately
        self.preview_box.configure(bg=entry_bg, fg=fg, insertbackground=fg)
        self.image_label.configure(bg=bg)'''
    
    def handle_screenshot(self):
        # Save a unique screenshot file
        screenshot_filename = f"screenshots/screenshot_{uuid.uuid4().hex[:8]}.png"
        image = ImageGrab.grab()
        try:
            image.save(screenshot_filename)
            self.entries['entry_screenshot'].delete(0, tk.END)
            self.entries['entry_screenshot'].insert(0, screenshot_filename)
            self.show_image_preview(screenshot_filename)
        except Exception as e:
            messagebox.showerror("Screenshot Error", f"Failed to capture/save screenshot: {e}")
    
    def clear_preview(self):
        self.image_label.config(image='')
        self.image_label.image = None
        if isinstance(self.entries['entry_screenshot'], tk.Entry):
            self.entries['entry_screenshot'].delete(0, tk.END)
    

if __name__ == "__main__":
    root = tk.Tk()
    app = ReadmeBuilderApp(root)
    root.mainloop()

    
    '''

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from jinja2 import Environment, FileSystemLoader
from PIL import Image, ImageTk
import os, shutil
from github import Github  # pip install PyGithub

class ReadmeBuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub README Builder")
        self.root.geometry("820x900")

        os.makedirs('templates', exist_ok=True)
        os.makedirs('output', exist_ok=True)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.template_dir = os.path.join(script_dir, 'templates')
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        self.templates = self.load_templates(self.template_dir)

        self.build_ui()

    def load_templates(self, template_dir):
        templates = []
        for file in os.listdir(template_dir):
            if file.endswith('.txt'):
                templates.append(file)
        if not templates:
            messagebox.showwarning("Templates Missing", "No templates found in 'templates' folder.")
        return templates

    def build_ui(self):
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

        self.entries = {}
        for label_text, var_name, multiline in fields:
            frame = tk.Frame(self.root)
            frame.pack(pady=4, fill='x', padx=10)

            label = tk.Label(frame, text=label_text, width=18, anchor="w")
            label.pack(side="left")

            if multiline:
                text_widget = tk.Text(frame, height=4, width=60, wrap='word')
                text_widget.pack(side="left", padx=5)
                self.entries[var_name] = text_widget
            else:
                entry = tk.Entry(frame, width=60)
                entry.pack(side="left", padx=5)
                self.entries[var_name] = entry

        # Screenshot upload
        upload_btn = tk.Button(self.root, text="Upload Screenshot", command=self.upload_screenshot, width=20)
        upload_btn.pack(pady=5)

        # Template selector
        template_frame = tk.Frame(self.root)
        template_frame.pack(pady=5)
        tk.Label(template_frame, text="Select Template Style:").pack(side="left")
        self.template_var = tk.StringVar(value=self.templates[0] if self.templates else "")
        self.template_menu = ttk.OptionMenu(template_frame, self.template_var, self.template_var.get(), *self.templates)
        self.template_menu.pack(side="left", padx=5)

        # Screenshot preview
        tk.Label(self.root, text="Screenshot Preview:").pack()
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)

        # Preview box
        tk.Label(self.root, text="README Preview:").pack()
        self.preview_box = tk.Text(self.root, height=16, width=95, wrap='word')
        self.preview_box.pack(pady=10)
        self.preview_box.config(state='disabled')

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        preview_btn = tk.Button(btn_frame, text="Preview", command=self.preview_readme, bg="#1976d2", fg="white", width=20)
        preview_btn.pack(side='left', padx=10)
        generate_btn = tk.Button(btn_frame, text="Generate README", command=self.generate_readme, bg="#388e3c", fg="white", width=20)
        generate_btn.pack(side='left', padx=10)
        push_btn = tk.Button(btn_frame, text="Push to GitHub", command=self.push_to_github, bg="#333", fg="white", width=20)
        push_btn.pack(side='left', padx=10)

        clear_btn = tk.Button(self.root, text="Clear All Fields", command=self.clear_fields, bg="#f44336", fg="white", width=20)
        clear_btn.pack(pady=5)

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
        return ""

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
''' 