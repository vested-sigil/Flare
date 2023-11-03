class Choice:
    def __init__(self):
        self.actions = registered_actions
        self.plans = []

    def list_plans(self):
        self.plans = [action_name for action_name in self.actions]
        for action_name in self.plans:
            print(f"{self.plans.index(action_name) + 1}. Plan '{action_name}'")

    def list_actions(self):
        action_list = [action_name for action_name in self.actions]
        for action_name in action_list:
            print(f"{action_list.index(action_name) + 1}. Action '{action_name}'")

    def execute_choice(self, choice):
        try:
            choice = int(choice)
            if 1 <= choice <= len(self.plans):
                selected_plan = self.plans[choice - 1]
                return f"Executing plan '{selected_plan}'..."
            elif 1 + len(self.plans) <= choice <= 1 + len(self.actions):
                selected_action = list(self.actions.keys())[choice - 1 - len(self.plans)]
                return f"Executing action '{selected_action}'..."
            else:
                return "Invalid choice. Please select a valid option."
        except ValueError:
            return "Invalid choice. Please enter a numerical value."

class NoteableAPI:
    def __init__(self, base_url='https://app.noteable.io'):
        self.base_url = base_url
        self.api_key = os.getenv('NOTEABLE_API_KEY')

    def get_user_info(self):
        url = f'{self.base_url}/get_user_info'
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.get(url, headers=headers)
        return response.json()

    def get_project_files(self, project_id):
        url = f'{self.base_url}/get_project_files'
        headers = {'Authorization': f'Bearer {self.api_key}'}
        data = {'project_id': project_id}
        response = requests.post(url, headers=headers, data=data)
        return response.json()

    def set_default_project(self, new_default_project_id):
        url = f'{self.base_url}/set_default_project'
        headers = {'Authorization': f'Bearer {self.api_key}'}
        data = {'new_default_project_id': new_default_project_id}
        response = requests.post(url, headers=headers, data=data)
        return response.json()

    def execute_action(self, action_name, params_str=''):
        if action_name == 'load':
            return self.load_rooms()
        elif action_name == 'change':
            room_name = params_str.strip()
            return self.change_room(room_name)
        elif action_name == 'map':
            room_name = params_str.strip()
            return self.map_room(room_name)
        else:
            return "Error: Action not found."

    def load_rooms(self):
        user_info = self.get_user_info()
        default_project_id = user_info['default_project_id']
        project_files = self.get_project_files(default_project_id)

        rooms = {}
        for file in project_files['files']:
            room_name = file['path'].split('.')[0]
            rooms[room_name] = {
                'id': file['id'],
                'notebooks': {}  # This will store the notebooks for this room
            }

        return rooms

    def change_room(self, room_name):
        user_info = self.get_user_info()
        default_project_id = user_info['default_project_id']

        if room_name in default_project_id:
            self.set_default_project(room_name)
            return f"Changed to room: {room_name}"
        else:
            return f"Error: Room '{room_name}' not found."

# Usage:
api = NoteableAPI()
rooms = api.load_rooms()
print(rooms)
api.change_room('Lobby')

