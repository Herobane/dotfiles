from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, DropDown, Group, Key, Match, ScratchPad, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook
from libqtile import qtile

import os
import subprocess
import psutil
import iwlib

@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])

mod = "mod4"
terminal = "kitty"

widget_defaults = dict(
    font="FiraCode Nerd Font",
    fontsize=14,
    padding=10,
)

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "Tab", lazy.prev_layout(), desc="Toggle between layouts"),
    Key([mod, "control"], "Tab", lazy.window.toggle_floating(), desc="Toggle floating mode"),
    Key([mod, "shift"], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod, "shift"], "q", lazy.spawn("xscreensaver-command --lock"), desc="Locks Qtile"),
    Key([mod], "q", lazy.spawn("rofi-powerv2"), desc="Calls rofi power menu"),
    Key([mod], "s", lazy.spawn("rofi-search"), desc="Calls rofi search menu"),
    Key([mod, "shift"], "c", lazy.spawn("rofi-config"), desc="Calls rofi config menu"),
    Key([mod], "c", lazy.spawn("conkytoggle"), desc="Calls conky"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "d", lazy.spawn('rofi -show drun -icon-theme "Tela-circle-dark" -show-icons -font "FontAwesome 15"')),
    Key([mod], "e", lazy.spawn('kitty mc --nosubshell')),
    Key([mod], "m", lazy.spawn("emacsclient -c -a 'emacs'")),
    Key([mod], "t", lazy.spawn('kitty htop')),
    Key([mod], "f", lazy.spawn('firefox')),
]

groups = [Group(i) for i in "123456789"]

#groups.append(ScratchPad("scratchpad", [
#    DropDown("kitty", "kitty", opacity=0.8),
#]))
#groups.append(Group("a"))


for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

groups.append(ScratchPad("quick_apps", [
    DropDown("term", "kitty", width=0.6, height=0.6, x=0.2, y=0.15),
    DropDown("file_manager", "kitty mc --nosubshell", width=0.6, height=0.6, x=0.2, y=0.15),
    DropDown("wifi", "kitty nmtui", width=0.6, height=0.6, x=0.2, y=0.15),
    DropDown("htop", "kitty btop", width=0.6, height=0.6, x=0.2, y=0.15),
]))

keys.append(Key([mod], "F1", lazy.group['quick_apps'].dropdown_toggle("term")))
keys.append(Key([mod], "F2", lazy.group['quick_apps'].dropdown_toggle("file_manager")))
keys.append(Key([mod], "F3", lazy.group['quick_apps'].dropdown_toggle("htop")))
keys.append(Key([mod], "F4", lazy.group['quick_apps'].dropdown_toggle("wifi")))

layouts = [
    layout.Columns(border_focus="#aaaaaa", border_width=0, margin=10, margin_on_single=[10, 10, 10, 10]),
    layout.Max(),
    layout.Floating(),
    layout.Stack(num_stacks=2, border_width=0, margin=10),
    layout.Bsp(border_focus="#aaaaaa", border_width=0, margin=10, margin_on_single=10),
    layout.Matrix(border_focus="#aaaaaa", border_width=0, margin=10, margin_on_single=[5, 10, 10, 10], columns=2),
    layout.MonadTall(border_width=0, margin=10),
    layout.MonadWide(border_focus="#aaaaaa", border_width=0, margin=10, single_margin=10),
    layout.RatioTile(border_width=0, margin=10),
    layout.Tile(border_width=0, margin=10),
    #layout.TreeTab(panel_width=200),
    layout.VerticalTile(border_focus="#aaaaaa", border_normal="#000000", border_width=0, margin=10, margin_on_single=[5, 10, 10, 10]),
    layout.Zoomy(margin=10, columnwidth=300),
    layout.Spiral(clockwise=False, main_pane="left", ratio=0.5, border_width=0, margin=10, ratio_increment=0),
]

screens = [
    Screen(bottom=bar.Gap(10),left=bar.Gap(10),right=bar.Gap(10),top=bar.Bar([
        widget.CurrentLayoutIcon(
            scale=0.6,
            padding=3
        ),
        widget.GroupBox(
            padding=9,
            highlight_method='block',
            hide_unused=True,
            inactive="ffffff",
            #this_current_screen_border="484848",
            #this_current_screen_border="202029",
            this_current_screen_border="a314a0",
        ),
#                widget.Sep(linewidth=0, padding=16),
        widget.Prompt(prompt="  "),
        widget.TaskList(txt_minimized="   ", txt_maximized="🗖   ", txt_floating="🗗   ", borderwidth=0, icon_size=20, fontsize=9, padding=5, highlight_method='block', border="202029"),
        widget.CheckUpdates(distro="Arch", colour_have_updates="ffcc88", display_format=" {updates}", mouse_callbacks={"Button1": lazy.spawn("kitty yay")}),
        widget.WidgetBox(text_closed="  ", text_open="  ", close_button_location="right", widgets=[
            widget.Systray(icon_size=20),
        ]),
        #widget.Sep(size_percent=60),
        widget.WidgetBox(background="#a314a0", text_closed="  ",text_open="  ", close_button_location="right", widgets=[
            widget.Sep(foreground="#a314a0" ,size_percent=100, linewidth=2),
            widget.CPU(
                format=" {load_percent}%",
                mouse_callbacks={"Button1": lazy.spawn('kitty htop')},

            ),
            #widget.Sep(size_percent=60),
            widget.Memory(
                format=" {MemPercent:.0f}%",
                mouse_callbacks={"Button1": lazy.spawn('kitty htop')}
            ),
            #widget.Sep(size_percent=60),
            widget.DF(
                visible_on_warn=False,
                format=" {r:.0f}%",
                mouse_callbacks={"Button1": lazy.spawn("kitty mc")}
                #format=" Disk : {r:.0f}%",
                #background="#208040"
            ),
        ]),
        widget.Wttr(location={'Ecrouves': 'Ecrouves'}),
        #widget.Sep(size_percent=60),
        widget.WidgetBox(text_closed="  ",text_open="  ", close_button_location="right", background="#a314a0" ,widgets=[
            widget.Sep(foreground="#a314a0" ,size_percent=100, linewidth=2),
            widget.Wlan(interface="wlp4s0", format=" {percent:2.0%} @ {essid}", disconnected_message="<span foreground='#ff0252'></span>", mouse_callbacks={"Button1": lazy.spawn("kitty nmtui")}),
            widget.Net(),
        ]),
        #widget.Sep(size_percent=60),
        widget.PulseVolume(fmt=" {}", volume_app="pulseaudio", mouse_callbacks={"Button1": lazy.spawn('kitty pulsemixer')}),
        #widget.Bluetooth(),
        widget.Backlight(change_command="brightnessctl s {0}%", fmt=" {}", backlight_name="amdgpu_bl0"),
        widget.Battery(
            format="{char} {percent:2.0%}",
            charge_char="",
            discharge_char="",
            empty_char="",
            unknown_char=""
        ),
        #widget.Sep(size_percent=60),
        widget.TextBox(background="a314a0", text="", mouse_callbacks={"Button1": lazy.spawn("conkytoggle")}),
        widget.Clock(
            font="FontAwesome",
            format="  %a %d %b      %H:%M",
        ),
        #widget.Image(filename="~/Pictures/qtile.png", mouse_callbacks={"Button1": lazy.spawn("kitty nvim /home/flavien/.config/qtile/config.py")}),
        #widget.QuickExit(),
        ],
        29,
        background="#151520",
        #background="#151520bb",
        margin=[0, 0, 10, 0],
        #background="#31313A",
        # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
        # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
    )),
    Screen(top=bar.Bar([
        widget.CurrentLayoutIcon(
            scale=0.6,
            padding=3
        ),
        widget.GroupBox(
            padding=9,
            highlight_method='block',
            hide_unused=True,
            inactive="ffffff",
            #this_current_screen_border="484848",
            this_current_screen_border="292930",
        ),
#                widget.Sep(linewidth=0, padding=16),
        widget.Prompt(prompt="  "),
        widget.TaskList(txt_minimized="   ", txt_maximized="🗖   ", txt_floating="🗗   ", borderwidth=0, icon_size=20, fontsize=9, padding=5, highlight_method='block', border="292930"),
        widget.Sep(size_percent=60),
        widget.Clock(
            font="FontAwesome",
            format="%a %d %b, %H:%M",
        ),
        #widget.Image(filename="~/Pictures/qtile.png", mouse_callbacks={"Button1": lazy.spawn("kitty nvim /home/flavien/.config/qtile/config.py")}),
        #widget.QuickExit(),
        ],
        29,
        #background="#31313Ae6",
        background="#151520bb",
        margin=[5, 8, 5, 8],
        #background="#31313A",
        # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
        # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
    )),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

floating_layout = layout.Floating(
    border_width=0,
    fullscreen_border_width=0,
    max_border_width=0,
    border_focus="#a314a0",
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(title="conky"),
    ]
)

extension_defaults = widget_defaults.copy()


# Drag floating layouts.

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
