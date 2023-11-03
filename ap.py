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


class Action:
    def __init__(self, name, function):
        self.name = name
        self.function = function

registered_actions = {}

def register_action(func):
    action_name = func.__name__
    action = Action(action_name, func)
    registered_actions[action_name] = action
    return func

def execute_plan(plan):
    try:
        action_name, params = plan.split('.plan')
        action_name = action_name.strip()
        params = eval(params.strip() or "()")

        action = registered_actions.get(action_name)
        if action:
            action_func = action.function
            result = action_func(*params)
            return result
        else:
            return f"Error: Action '{action_name}' not found."
    except ValueError:
        return "Error: Invalid plan syntax. Please use 'action_name.plan(params)' format."
    except Exception as e:
        return f"Error: {e}"

def check_plan(plan):
    try:
        action_name, params = plan.split('.plan')
        action_name = action_name.strip()
        eval(params.strip() or "()")

        action = registered_actions.get(action_name)
        if action:
            return f"Plan '{plan}' is valid."
        else:
            return f"Error: Action '{action_name}' not found in the plan."
    except ValueError:
        return "Error: Invalid plan syntax. Please use 'action_name.plan(params)' format."
    except Exception as e:
        return f"Error: {e}"

def edit_plan(plan, new_plan):
    try:
        check_result = check_plan(new_plan)
        if "valid" in check_result.lower():
            return f"Plan '{plan}' edited to '{new_plan}'."
        else:
            return check_result
    except Exception as e:
        return f"Error: Unable to edit plan '{plan}'. Reason: {e}"

def plan(action_name, params_str=''):
    return f"{action_name}.plan{params_str}"

@register_action
def greet(name):
    return f"Hello, {name}!"

@register_action
def plan(action):
    return f"Executing plan: {action}"

class AP:
    def __init__(self, point, pair, path):
        self.point = point
        self.pair = pair
        self.path = path

