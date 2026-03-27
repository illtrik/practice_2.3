import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests

BASE_URL = "https://api.github.com"


class GitHubApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub Profile Viewer")
        self.root.geometry("600x700")

        self.current_repos = []

        search_frame = tk.Frame(root, pady=10)
        search_frame.pack(fill=tk.X)

        tk.Label(search_frame, text="Имя пользователя GitHub:").pack(side=tk.LEFT, padx=5)
        self.username_entry = tk.Entry(search_frame)
        self.username_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.username_entry.bind('<Return>', lambda event: self.fetch_data())

        self.search_btn = tk.Button(search_frame, text="Найти", command=self.fetch_data)
        self.search_btn.pack(side=tk.LEFT, padx=5)

        self.profile_info = tk.Label(root, text="Введите имя и нажмите 'Найти'", justify=tk.LEFT,
                                     font=("Arial", 10, "bold"))
        self.profile_info.pack(pady=10, padx=10, anchor="w")

        filter_frame = tk.Frame(root, pady=5)
        filter_frame.pack(fill=tk.X)

        tk.Label(filter_frame, text="Фильтр репозиториев:").pack(side=tk.LEFT, padx=5)
        self.filter_entry = tk.Entry(filter_frame)
        self.filter_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.filter_entry.bind('<KeyRelease>', self.apply_filter)

        tk.Label(root, text="Репозитории:").pack(anchor="w", padx=10)
        self.results_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=25)
        self.results_area.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

    def get_user_profile(self, username):
        url = f"{BASE_URL}/users/{username}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось подключиться: {e}")
            return None

    def get_repos(self, username):
        url = f"{BASE_URL}/users/{username}/repos"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            return []
        except:
            return []

    def fetch_data(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showwarning("Внимание", "Введите имя пользователя")
            return

        self.results_area.delete(1.0, tk.END)
        self.filter_entry.delete(0, tk.END)

        profile = self.get_user_profile(username)
        if not profile:
            messagebox.showerror("Ошибка", "Пользователь не найден")
            return

        info_text = (
            f"Логин: {profile.get('login')}\n"
            f"Ссылка: {profile.get('html_url')}\n"
            f"Публичных репозиториев: {profile.get('public_repos')}\n"
            f"Подписчики: {profile.get('followers')} | Подписки: {profile.get('following')}"
        )
        self.profile_info.config(text=info_text)

        self.current_repos = self.get_repos(username)
        self.display_repos(self.current_repos)

    def display_repos(self, repos_list):
        self.results_area.delete(1.0, tk.END)
        if not repos_list:
            self.results_area.insert(tk.END, "Репозитории не найдены.")
            return

        for r in repos_list:
            visibility = "Приватный" if r.get('private') else "Публичный"
            lang = r.get('language') or "Не указан"
            text = (f"📦 {r['name']} ({visibility})\n"
                    f"   Язык: {lang} | ⭐ Просмотры: {r['watchers_count']}\n"
                    f"   Ветка: {r['default_branch']} | Ссылка: {r['html_url']}\n"
                    f"{'-'*60}\n")
            self.results_area.insert(tk.END, text)

    def apply_filter(self, event=None):
        query = self.filter_entry.get().lower()
        filtered = [r for r in self.current_repos if query in r['name'].lower()]
        self.display_repos(filtered)

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubApp(root)
    root.mainloop()