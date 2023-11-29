# Define the default layout properties
default_layout = {
    "background_color": (255, 255, 255),
    "text_color": (0, 0, 0),
    "font_size": 24,
    "padding": 10,
}

# Define the layouts dictionary
layouts = {
    "default": default_layout,
    "menu_horizontal": {
        "type": "horizontal",
        "alignment": "center",
        "spacing": 10,
        **default_layout,
    },
    "menu_vertical": {
        "type": "vertical",
        "alignment": "center",
        "spacing": 10,
        **default_layout,
    },
    "panel_horizontal": {
        "type": "horizontal",
        "alignment": "center",
        "spacing": 10,
        **default_layout,
    },
    "panel_vertical": {
        "type": "vertical",
        "alignment": "center",
        "spacing": 10,
        **default_layout,
    },
    "stack_icons_horizontal": {
        "type": "horizontal",
        "alignment": "center",
        "spacing": 10,
        **default_layout,
    },
    "stack_icons_vertical": {
        "type": "vertical",
        "alignment": "center",
        "spacing": 10,
        **default_layout,
    },
    "menu_top": {
        "type": "vertical",
        "alignment": "top",
        "spacing": 10,
        **default_layout,
    },
    "menu_bottom": {
        "type": "vertical",
        "alignment": "bottom",
        "spacing": 10,
        **default_layout,
    },
    "panel_left": {
        "type": "horizontal",
        "alignment": "left",
        "spacing": 10,
        **default_layout,
    },
    "panel_right": {
        "type": "horizontal",
        "alignment": "right",
        "spacing": 10,
        **default_layout,
    },
    "stack_icons_left": {
        "type": "vertical",
        "alignment": "left",
        "spacing": 10,
        **default_layout,
    },
    "stack_icons_right": {
        "type": "vertical",
        "alignment": "right",
        "spacing": 10,
        **default_layout,
    },
    "menu_left": {
        "type": "horizontal",
        "alignment": "left",
        "spacing": 10,
        **default_layout,
    },
    "menu_right": {
        "type": "horizontal",
        "alignment": "right",
        "spacing": 10,
        **default_layout,
    },
    "panel_top": {
        "type": "vertical",
        "alignment": "top",
        "spacing": 10,
        **default_layout,
    },
    "panel_bottom": {
        "type": "vertical",
        "alignment": "bottom",
        "spacing": 10,
        **default_layout,
    },
    "stack_icons_top": {
        "type": "horizontal",
        "alignment": "top",
        "spacing": 10,
        **default_layout,
    },
    "stack_icons_bottom": {
        "type": "horizontal",
        "alignment": "bottom",
        "spacing": 10,
        **default_layout,
    },
    "grid_2x2": {
        "type": "grid",
        "rows": 2,
        "columns": 2,
        "spacing": 10,
        **default_layout,
    },
    "grid_3x3": {
        "type": "grid",
        "rows": 3,
        "columns": 3,
        "spacing": 10,
        **default_layout,
    },
    "grid_4x4": {
        "type": "grid",
        "rows": 4,
        "columns": 4,
        "spacing": 10,
        **default_layout,
    },
    "list_horizontal": {
        "type": "horizontal",
        "alignment": "center",
        "spacing": 10,
        **default_layout,
    },
    "list_vertical": {
        "type": "vertical",
        "alignment": "center",
        "spacing": 10,
        **default_layout,
    },
    # Add more layouts as needed
}


