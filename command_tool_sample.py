import tkinter as tk

# 表示したいボタンの内容を静的なクラスとして管理する
class CommandButtons():
    # そのタイミングで表示したいtkボタンのリスト
    buttons = []

    # 表示されているボタンを削除する
    @classmethod
    def destroy_buttons(cls):
        for button in cls.buttons:
            button.destroy()
        cls.buttons = []

    # ボタンを追加する
    @classmethod
    def add_button(cls, button: tk.Button):
        cls.buttons.append(button)

    # ボタンを表示する
    @classmethod
    def show_buttons(cls):
        if cls.buttons == []:
            destroy_buttons()
        else:
            for i, button in enumerate(cls.buttons):
                button.grid(
                    in_=button_frame,
                    row=i//3, # 商を求める 10個目のボタンだったら10を3で割った商が3なので3行目になる
                    column=i%3, # 3列で改行
                )

def add_command(command):
    shown_command_list.append(command)
    command_str = " ".join(shown_command_list) # showing_command_listをスペースで区切って文字列にする　例: /time add 1000
    command_txt_entry.insert(tk.END, command_str)


def callback(command) -> 'function': # tk.Buttonのcommandに入れるために関数を返す
    def click_button():
        print(command,"がクリックされた")

        # 入力されたコマンドをテキストボックスに表示(追加)する
        command_txt_entry.delete(0, tk.END)
        add_command(command)

        # 表示されているボタンを削除する
        CommandButtons.destroy_buttons()

        # テキストボックスのコマンドをもとにボタンを作成する
        cmd_list = get_next_command_list(current_command_list=" ".join(shown_command_list))
        create_button(cmd_list=cmd_list)

        return

    return click_button # 関数を返す
    

def get_next_command_list(current_command_list):
    # 数が多くなっちゃったら別のファイルで管理してimportしてもいいかも
    # この内部の処理は完全じゃないです

    if current_command_list == "":
        next_cmd_list = ['/time', '/say']
        return next_cmd_list

    if current_command_list == "/time":
        next_cmd_list = ['add', 'set', 'query']
        return next_cmd_list

    if current_command_list == "/time add":
        next_cmd_list = ['1000', '10000', '100000']
        return next_cmd_list

    if current_command_list == "/time set":
        next_cmd_list = ['noon', 'midnight', 'day', 'night']
        return next_cmd_list

    if current_command_list == "end":
        sys.exit()

    return ['end']

def create_button(cmd_list):
    for i,command_name in enumerate(cmd_list):
        # ボタン作成と配置
        CommandButtons.add_button(
            tk.Button(
                button_frame, 
                text=command_name, 
                height=2, 
                command=callback(command_name) # commandは関数を入力するので
            )
        )
        CommandButtons.show_buttons()



# ウィンドウ作成
root = tk.Tk()
# ウィンドウサイズ
root.columnconfigure(0, minsize=250)
root.rowconfigure([0, 1], minsize=100)
# root.geometry("300x200")

cmd_line_frame = tk.Frame(
    root, 
    width=280, 
    height=40, 
    borderwidth=3, 
    relief="groove",
    background="red"
)

button_frame = tk.Frame(
    root, 
    width=280, 
    height=150, 
    borderwidth=3, 
    relief="groove",
    background="blue"
)

# フレームの配置
cmd_line_frame.grid(row=0, column=0)
button_frame.grid(row=1, column=0)

# cmd_line_frame内のウィジェットの定義と配置
command_title = tk.Label(cmd_line_frame, text="コマンド")
command_txt_entry = tk.Entry(cmd_line_frame)
command_title.grid(row=0, column=0)
command_txt_entry.grid(row=0, column=1)

# 最初に定義表示したいボタンだけここで定義する
cmd_list = ['/time', '/say']

# テキストボックスに表示されるコマンドを管理するリスト
shown_command_list = []

create_button(cmd_list)

# メインループ
root.mainloop()