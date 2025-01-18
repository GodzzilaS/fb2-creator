import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString as minidom_parseString

import customtkinter as ctk

sections = []
add_section_window = None


def update_preview(*args):
    """Обновляет содержимое текстового поля предпросмотра XML."""
    name_of_file = name_of_file_entry.get()
    genre = genre_entry.get()
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    title = title_entry.get()
    lang = lang_var.get()

    language_map = {
        "Русский": "ru",
        "Английский": "en",
        "Немецкий": "de",
        "Французский": "fr",
    }
    lang_code = language_map.get(lang, "ru")

    root = ET.Element("FictionBook", {
        "xmlns": "http://www.gribuser.ru/xml/fictionbook/2.0",
        "xmlns:xlink": "http://www.w3.org/1999/xlink"
    })

    description = ET.SubElement(root, "description")
    title_info = ET.SubElement(description, "title-info")
    ET.SubElement(title_info, "genre").text = genre if genre else ""

    author = ET.SubElement(title_info, "author")
    ET.SubElement(author, "first-name").text = first_name if first_name else ""
    ET.SubElement(author, "last-name").text = last_name if last_name else ""

    ET.SubElement(title_info, "book-title").text = title if title else ""
    ET.SubElement(title_info, "lang").text = lang_code

    body = ET.SubElement(root, "body")
    for section in sections:
        section_elem = ET.SubElement(body, "section")
        ET.SubElement(section_elem, "title").text = section.get("title", "")
        ET.SubElement(section_elem, "p").text = section.get("p", "")

    rough_string = ET.tostring(root, encoding="utf-8")
    reparsed = minidom_parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="    ")

    preview_textbox.delete("1.0", ctk.END)
    preview_textbox.insert(ctk.END, pretty_xml)

    preview_label_text = f"Предпросмотр {name_of_file}.fb2" if name_of_file else "Предпросмотр"
    preview_label.configure(text=preview_label_text)


def create_fb2_file():
    """Создаёт FB2 файл на основе введённых данных."""
    name_of_file = name_of_file_entry.get()
    if not name_of_file:
        result_label.configure(text="Укажите имя файла!", text_color="red")
        return

    xml_content = preview_textbox.get("1.0", ctk.END).strip()
    with open(f"{name_of_file}.fb2", "w", encoding="utf-8") as file:
        file.write(xml_content)

    result_label.configure(text="Книга успешно создана!", text_color="green")


def open_add_section_window():
    """Открывает окно для добавления секций, если оно не открыто."""
    global add_section_window

    if add_section_window is not None and add_section_window.winfo_exists():
        add_section_window.focus()
        return

    add_section_window = ctk.CTkToplevel(app)
    add_section_window.title("Добавление раздела")
    center_window(add_section_window, 400, 300)

    add_section_window.grab_set()

    ctk.CTkLabel(add_section_window, text="Заголовок секции:").pack(pady=10)
    section_title_entry = ctk.CTkEntry(add_section_window)
    section_title_entry.pack(pady=5, padx=20, fill="x")

    ctk.CTkLabel(add_section_window, text="Текст секции:").pack(pady=10)
    section_text_entry = ctk.CTkEntry(add_section_window)
    section_text_entry.pack(pady=5, padx=20, fill="x")

    def add_section():
        """Добавляет секцию в список и обновляет предпросмотр."""
        section_title = section_title_entry.get()
        section_text = section_text_entry.get()
        if section_title and section_text:
            sections.append({"title": section_title, "p": section_text})
            section_title_entry.delete(0, ctk.END)
            section_text_entry.delete(0, ctk.END)
            update_preview()

    add_section_button = ctk.CTkButton(add_section_window, text="Добавить секцию", command=add_section)
    add_section_button.pack(pady=20)
    add_section_window.focus()


def change_scaling(scaling):
    """Изменяет масштабирование интерфейса."""
    ctk.set_widget_scaling(float(scaling))


def change_theme(theme):
    """Смена темы приложения."""
    ctk.set_appearance_mode("dark" if theme == "тёмная" else "light")


def center_window(window, width, height):
    """Центрирование окна на экране."""
    window.geometry(f"{width}x{height}")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Создаём книги")

center_window(app, 1200, 800)

frame = ctk.CTkFrame(app, width=400)
frame.pack(side="left", padx=20, pady=20, fill="y")

# Поля ввода
ctk.CTkLabel(frame, text="Название файла:").grid(row=0, column=0, pady=5, padx=10, sticky="e")
name_of_file_entry = ctk.CTkEntry(frame, width=250)
name_of_file_entry.grid(row=0, column=1, pady=5, padx=10)

ctk.CTkLabel(frame, text="Жанр:").grid(row=1, column=0, pady=5, padx=10, sticky="e")
genre_entry = ctk.CTkEntry(frame, width=250)
genre_entry.grid(row=1, column=1, pady=5, padx=10)

ctk.CTkLabel(frame, text="Имя автора:").grid(row=2, column=0, pady=5, padx=10, sticky="e")
first_name_entry = ctk.CTkEntry(frame, width=250)
first_name_entry.grid(row=2, column=1, pady=5, padx=10)

ctk.CTkLabel(frame, text="Фамилия автора:").grid(row=3, column=0, pady=5, padx=10, sticky="e")
last_name_entry = ctk.CTkEntry(frame, width=250)
last_name_entry.grid(row=3, column=1, pady=5, padx=10)

ctk.CTkLabel(frame, text="Название книги:").grid(row=4, column=0, pady=5, padx=10, sticky="e")
title_entry = ctk.CTkEntry(frame, width=250)
title_entry.grid(row=4, column=1, pady=5, padx=10)

ctk.CTkLabel(frame, text="Язык книги:").grid(row=5, column=0, pady=5, padx=10, sticky="e")
lang_var = ctk.StringVar(value="Русский")
lang_menu = ctk.CTkOptionMenu(frame, values=["Русский", "Английский", "Немецкий", "Французский"], variable=lang_var,
                              command=lambda _: update_preview())
lang_menu.grid(row=5, column=1, pady=5, padx=10)

# Кнопка для добавления данных
add_data_button = ctk.CTkButton(frame, text="Добавить разделы в книгу", command=open_add_section_window)
add_data_button.grid(row=6, column=0, columnspan=2, pady=20)

# Кнопка создания книги
create_button = ctk.CTkButton(frame, text="Создать книгу", command=create_fb2_file, width=250)
create_button.grid(row=7, column=0, columnspan=2, pady=20)

result_label = ctk.CTkLabel(frame, text="")
result_label.grid(row=8, column=0, columnspan=2, pady=5)

# Поле для предпросмотра XML
preview_frame = ctk.CTkFrame(app)
preview_frame.pack(side="right", padx=20, pady=20, fill="both", expand=True)

preview_label = ctk.CTkLabel(preview_frame, text="Предпросмотр")
preview_label.pack(pady=10)

preview_textbox = ctk.CTkTextbox(preview_frame, wrap="none")
preview_textbox.pack(fill="both", expand=True)

settings_frame = ctk.CTkFrame(app)
settings_frame.place(relx=0.02, rely=0.9, anchor="w")

ctk.CTkLabel(settings_frame, text="Масштабирование:").grid(row=0, column=0, padx=10)
scaling_menu = ctk.CTkOptionMenu(settings_frame, values=["0.8", "1.0", "1.2", "1.5"], command=change_scaling)
scaling_menu.set("1.0")
scaling_menu.grid(row=0, column=1, padx=10)

ctk.CTkLabel(settings_frame, text="Тема:").grid(row=1, column=0, padx=10, pady=5)
theme_menu = ctk.CTkOptionMenu(settings_frame, values=["тёмная", "светлая"], command=change_theme)
theme_menu.set("тёмная")
theme_menu.grid(row=1, column=1, padx=10, pady=5)

for widget in [name_of_file_entry, genre_entry, first_name_entry, last_name_entry, title_entry]:
    widget.bind("<KeyRelease>", update_preview)

update_preview()
app.mainloop()
