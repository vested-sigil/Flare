# Main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.screenmanager import ScreenManager, Screen
from toolbox import ToolboxScreen
from project_manager import ProjectManager

class ProjectManagerUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.project_manager = ProjectManager()

        self.file_chooser = FileChooserListView(path=self.project_manager.project_dir, filters=['*.json'])
        self.add_widget(self.file_chooser)

        button_layout = BoxLayout(size_hint_y=None, height=50)
        load_button = Button(text='Load Project', on_press=self.load_project)
        save_button = Button(text='Save Project', on_press=self.save_project)
        new_button = Button(text='New Project', on_press=self.new_project)
        button_layout.add_widget(load_button)
        button_layout.add_widget(save_button)
        button_layout.add_widget(new_button)
        self.add_widget(button_layout)

        self.toolbox = ToolboxScreen()
        self.add_widget(self.toolbox)

    def load_project(self, instance):
        selected_files = self.file_chooser.selection
        if selected_files:
            project_path = selected_files[0]
            project_name = os.path.basename(project_path)[:-5]
            content = self.project_manager.load_project(project_name)
            self.toolbox.load_content(content)

    def save_project(self, instance):
        selected_files = self.file_chooser.selection
        if selected_files:
            project_path = selected_files[0]
            project_name = os.path.basename(project_path)[:-5]
            content = self.toolbox.get_content()
            self.project_manager.save_project(project_name, content)

    def new_project(self, instance):
        project_name = input("Enter a name for the new project: ")  # You can customize this input prompt
        if project_name:
            content = {"objects": []}  # Initialize content for the new project
            self.project_manager.create_project(project_name, content)
            # Optionally, you could notify the user that the new project was created successfully

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'main'
        self.project_manager_ui = ProjectManagerUI()
        self.add_widget(self.project_manager_ui)

class DebugApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        main_screen = MainScreen(name='main')
        toolbox_screen = ToolboxScreen(name='toolbox')

        self.screen_manager.add_widget(main_screen)
        self.screen_manager.add_widget(toolbox_screen)

        return self.screen_manager

if __name__ == '__main__':
    DebugApp().run()

