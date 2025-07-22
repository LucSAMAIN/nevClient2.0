# app/utils/theme.py
import wx


THEME_NAME = "Graphite"

_themes = {
    "Purple" : {
        "hard" : "#AA60C8",
        "mid"  : "#D69ADE",
        "soft" : "#EABDE6",
        "light": "#FFDFEF",
    },
    "Light Blue" : {
        "hard" : "#007ACC",
        "mid"  : "#66B2FF",
        "soft" : "#B3D7FF",
        "light": "#E6F2FF",
    },
    "Green" : {
        "hard" : "#2E8B57",
        "mid"  : "#3CB371",
        "soft" : "#98FB98",
        "light": "#E0FFE0",
    },
    "Orange" : {
        "hard" : "#FF8C00",
        "mid"  : "#FFA500",
        "soft" : "#FFDAB9",
        "light": "#FFF5E1",
    },
    "Red" : {
        "hard" : "#DC143C",
        "mid"  : "#F08080",
        "soft" : "#FFA07A",
        "light": "#FFE4E1",
    },
    "Teal" : {
        "hard" : "#008080",
        "mid"  : "#20B2AA",
        "soft" : "#AFEEEE",
        "light": "#E0FFFF",
    },
    "Graphite" : {
        "hard" : "#2F4F4F",
        "mid"  : "#708090",
        "soft" : "#B0C4DE",
        "light": "#F5F5F5",
    }
}

def changeTheme(theme_name: str):
    global _themes, THEME_NAME
    try:
        if theme_name in _themes:
            THEME_NAME = theme_name
        else:
            raise ValueError(f"Theme '{theme_name}' not found. Available themes: {list(_themes.keys())}")
    except ValueError as e:
        wx.MessageBox(str(e), "Theme Error", wx.OK | wx.ICON_ERROR)
    except Exception as e:
        wx.MessageBox(f"An unexpected error occurred: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

def _as_colour(code: str) -> wx.Colour:
    return wx.Colour(code)         

def getThemes() -> list:
    return list(_themes.keys())

def getColoursDict():
    global _themes, THEME_NAME
    return {
        "hard" : _as_colour(_themes[THEME_NAME]["hard"]),
        "mid"  : _as_colour(_themes[THEME_NAME]["mid"]),
        "soft" : _as_colour(_themes[THEME_NAME]["soft"]),
        "light": _as_colour(_themes[THEME_NAME]["light"]),
    }
