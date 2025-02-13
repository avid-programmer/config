# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
import subprocess

from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy

mod = "mod4"            # Super key
terminal = "urxvt"
youtube = "firefox youtube_url"

keys = [

    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),

    # Change size of the window
    Key([mod, "shift"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "shift"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "shift"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "shift"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod, "shift"], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Fullscreen
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
    Key([mod, "shift"], "f", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),

    # Open terminal
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "t", lazy.next_layout(), desc="Toggle between layouts"),

    # Kill focussed window
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
   
    # Change from normal to floating
    Key([mod], "Tab", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),

    # Reload configuration file
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),

    # Open gui applications
    Key([mod], "p", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Launch rofi
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc = "Spawn rofi"),

    # Launch youtube
    Key([], "XF86AudioPlay", lazy.spawn(youtube), desc = "Launch youtube"),

    # Audio configurations
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer set 'Master' 5%+"), desc = "Increase Volume"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer set 'Master' 5%-"), desc = "Decrease Volume"),
    Key([], "XF86AudioMute", lazy.spawn("amixer -D pulse set Master 1+ toggle"), desc = "Toggle Mute"),

    # Print Screen
    Key([], "Print", lazy.spawn("flameshot full --path '/home/rupesh/Pictures/Screenshots/'"), desc = "Quick screenshot"),
    Key([mod], "Print", lazy.spawn("flameshot full"), desc = "Full screenshot"),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

# List of X clients to open in floating mode
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="Galculator"),
        Match(wm_class="GParted"),
        Match(wm_class="Manjaro-hello"),
        Match(wm_class="Manjaro Settings Manager"),
        Match(wm_class="nitrogen"),
        Match(wm_class="octopi"),
        Match(wm_class="pamac-manager"),
        Match(wm_class="simple-scan"),
    ]
)

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call(home)

# Workspaces from 1 - 9
groups = [Group(i) for i in "123456789"]

# Assigning keys to switch to each workspace
for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key([mod], i.name, lazy.group[i.name].toscreen(), desc=f"Switch to group {i.name}",),

            # mod + shift + group number = switch to & move focused window to group
            Key( [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),

            # mod + Control + group number = move focused window to group
             Key([mod, "Control"], i.name, lazy.window.togroup(i.name),
                 desc="move focused window to group {}".format(i.name)),
        ]
    )


layouts = [
    
    layout.Columns(
                    border_focus = "#458a57",
                    border_width = 2,
                    margin = 8,
                    insert_position = 1,
                  ),

    layout.Max(),
    layout.TreeTab(),
    # layout.Floating(),
    
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font = "MesloLGS NF",
    fontsize = 12,
    padding = 3,
    background = "#161719",
)
extension_defaults = widget_defaults.copy()

# Colors
fg ='#C5C8C6'
gray = '#30343b'
red = '#cc6666'
magenta = '#b294bb'


screens = [
    Screen(
       bottom=bar.Bar(
            [
                # Left
                widget.Spacer(length = 10),
                widget.CurrentLayout(),
                widget.Spacer(length = 10),

                widget.GroupBox(disable_drag = True, fontsize = 14, highlight_method = 'border', 
                                highlight_color = "#161719", inactive = gray, active = fg, 
                                this_current_screen_border = magenta, urgent_alert_method = 'text', 
                                urgent_text = red),

                widget.Spacer(length = 30),

                # Center
                widget.Prompt(),
                widget.Spacer(length = 270),

                # Right
                widget.Wlan(format='{essid}  {percent:2.0%}', interface = 'wlp0s20f3', 
                            ethernet_interface = "enp43s0i", disconnected_message = "Down"),

                widget.Memory(format = ' {MemUsed: .1f} {mm}  ', measure_mem = 'M'),
                widget.CPU(format = 'CPU {load_percent}%  '),

                widget.Volume(font = "MesloLGS NF", fmt = "Volume: {}  ", mute_format = "  "),

                widget.ThermalSensor(format = '󰔏 {temp:.0f}{unit}  ', threshold = 85, foreground_alert = red),

                widget.Battery(format = '{char}  {percent:2.0%}  {hour:d}:{min:02d} ', 
                               full_char = '󰁹', charge_char = '󰂄', discharge_char = '󱟞', empty_char = '󰂃', 
                               not_charging_char = '󰚥', low_foreground = red, low_percentage = 0.2, 
                               notify_below = 20, show_short_text = False, update_interval = 10),

                widget.Clock(format=" %d %b %Y  %H:%M "),
                widget.QuickExit(countdown_format = "  {}   ", default_text = " Exit "),
                widget.Systray(),
                widget.Spacer(length = 100),
            ],
            35,
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
     ),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24


# groups.append(ScratchPad("scratchpad", 
#                           dropdowns = [
#
#                           # define a drop down terminal
#                            DropDown("term", "urxvt", 
#                                     x = 0.25, y = 0.3,
#                                     width = 0.5, height = 0.5,
#                                     opacity = 0.8,
#                                     on_focus_lost_hide = True),
#                             ]),
# )
#
# keys.extend([
#     Key([], 'F9', lazy.group['scratchpad'].dropdown_toggle('term')),
# ])

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
