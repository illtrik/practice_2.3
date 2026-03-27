import tkinter as tk
from tkinter import scrolledtext
import http.client
import urllib.parse

urls = [
    "https://github.com/",
    "https://www.binance.com/en",
    "https://tomtit.tomsk.ru/",
    "https://jsonplaceholder.typicode.com/",
    "https://moodle.tomtit-tomsk.ru/"
]


def get_status_text(status_code):
    if status_code == 200:
        return "доступен"
    elif status_code == 404:
        return "не найден"
    elif status_code == 403:
        return "вход запрещен"
    elif status_code == 500:
        return "ошибка сервера"
    else:
        return "не доступен"


def check_urls():
    output_text.delete(1.0, tk.END)  # Очистить поле перед новым выводом
    for url in urls:
        parsed_url = urllib.parse.urlparse(url)
        connection = None
        status_code = None
        try:
            if parsed_url.scheme == "https":
                connection = http.client.HTTPSConnection(parsed_url.netloc, timeout=10)
            else:
                connection = http.client.HTTPConnection(parsed_url.netloc, timeout=10)

            path = parsed_url.path
            if not path:
                path = "/"
            if parsed_url.query:
                path += "?" + parsed_url.query

            connection.request("GET", path)
            response = connection.getresponse()
            status_code = response.status

        except Exception as e:
            status_code = None

        finally:
            if connection:
                connection.close()

        if status_code is None:
            status_text = "не доступен"
            code_display = "нет ответа"
        else:
            status_text = get_status_text(status_code)
            code_display = status_code

        output_text.insert(tk.END, f"{url} - {status_text} - {code_display}\n")


root = tk.Tk()
root.title("Проверка статусов URL")
root.geometry("700x400")

check_button = tk.Button(root, text="Проверить статусы", command=check_urls, font=("Arial", 14))
check_button.pack(pady=10)

output_text = scrolledtext.ScrolledText(root, width=80, height=20, font=("Courier New", 12))
output_text.pack(pady=10)

root.mainloop()