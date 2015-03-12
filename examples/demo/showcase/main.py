#!/usr/bin/kivy
'''
Showcase of Kivy Features
=========================

This showcases many features of Kivy. You should see a
menu bar across the top with a demonstration area below. The
first demonstration is the accordion layout. You can see, but not
edit, the kv language code for any screen by pressing the bug or
'show source' icon. Scroll through the demonstrations using the
left and right icons in the top right or selecting from the menu
bar. This showcases dozens of features.

The file showcase.kv describes the main container, while each demonstration
pane is described in a separate .kv file in the data/screens directory.
The image data/background.png provides the gradient background while the
icons in data/icon directory are used in the control bar. The file
data/faust_github.jpg is used in the Scatter pane. The icons are
from `http://www.gentleface.com/free_icon_set.html` and licensed as
Creative Commons - Attribution and Non-commercial Use Only; they
sell a commercial license.

The file android.txt is used to package the application for use with the
Kivy Launcher Android application. For Android devices, you can
copy/paste this directory into /sdcard/kivy/showcase on your Android device.

'''

from time import time
from kivy.app import App
from os.path import dirname, join
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
from kivy.logger import Logger


class ShowcaseScreen(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(ShowcaseScreen, self).add_widget(*args)


class ShowcaseApp(App):

    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    show_sourcecode = BooleanProperty(False)
    sourcecode = StringProperty()
    screen_names = ListProperty([])
    hierarchy = ListProperty([])

    def build(self):
        self.title = 'hello world'
        Clock.schedule_interval(self._update_clock, 1 / 60.)
        self.screens = {}
        self.available_screens = sorted([
            'Buttons', 'ToggleButton', 'Sliders', 'ProgressBar', 'Switches',
            'CheckBoxes', 'TextInputs', 'Accordions', 'FileChoosers',
            'Carousel', 'Bubbles', 'CodeInput', 'DropDown', 'Spinner',
            'Scatter', 'Splitter', 'TabbedPanel + Layouts', 'RstDocument',
            'Popups', 'ScreenManager'])
        self.screen_names = self.available_screens
        curdir = dirname(__file__)
        self.available_screens = [join(curdir, 'data', 'screens',
            '{}.kv'.format(fn)) for fn in self.available_screens]
        self.go_next_screen()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def on_current_title(self, instance, value):
        self.root.ids.spnr.text = value

    def go_previous_screen(self):
        self.index = (self.index - 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='right')
        self.current_title = screen.name
        self.update_sourcecode()

    def go_next_screen(self):
        self.index = (self.index + 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='left')
        self.current_title = screen.name
        self.update_sourcecode()

    def go_screen(self, idx):
        self.index = idx
        self.root.ids.sm.switch_to(self.load_screen(idx), direction='left')
        self.update_sourcecode()

    def go_hierarchy_previous(self):
        ahr = self.hierarchy
        if len(ahr) == 1:
            return
        if ahr:
            ahr.pop()
        if ahr:
            idx = ahr.pop()
            self.go_screen(idx)

    def load_screen(self, index):
        if index in self.screens:
            return self.screens[index]

        name_to_map = {
            "accordions.kv": """
ShowcaseScreen:
    name: 'Accordions'

    fullscreen: True

    BoxLayout:
        size_hint_y: None
        height: '48dp'

        ToggleButton:
            id: tbh
            text: 'Horizontal'
            group: 'accordion'
            state: 'down'

        ToggleButton:
            text: 'Vertical'
            group: 'accordion'

    Accordion:

        orientation: 'horizontal' if tbh.state == 'down' else 'vertical'

        AccordionItem:
            title: 'Panel 1'
            Label:
                text: 'This is a label fit to the content view'
                text_size: self.width, None

        AccordionItem:
            title: 'Panel 2'
            Button:
                text: 'A button, what else?'

        AccordionItem:
            title: 'Panel 3'
            Label:
                text: 'This is a label fit to the content view'
                text_size: self.width, None

            """,
            "bubbles.kv": """
ShowcaseScreen:
    name: 'Bubbles'

    Bubble:
        size_hint_y: None
        height: '48dp'

        BubbleButton:
            text: 'Cut'
        BubbleButton:
            text: 'Copy'
        BubbleButton:
            text: 'Paste'

    Widget:
        size_hint_y: None
        height: '48dp'

    BoxLayout:
        size_hint_y: None
        height: '48dp'
        Label:
            text: 'Hello'

        Bubble:
            arrow_pos: 'left_mid'
            Label:
                text: 'World'

            """,
            "buttons.kv": """
ShowcaseScreen:
    name: 'Buttons'

    Button:
        size_hint_y: None
        height: '48dp'
        text: 'Button normal'

    Button:
        size_hint_y: None
        height: '48dp'
        text: 'Button down'
        state: 'down'

    Button:
        size_hint_y: None
        height: '48dp'
        text: 'Button disabled'
        disabled: True

    Button:
        size_hint_y: None
        height: '48dp'
        text: 'Button down disabled'
        state: 'down'
        disabled: True

            """,
            "carousel.kv": """
<ColoredLabel@Label>:
    font_size: '48sp'
    color: (.6, .6, .6, 1)
    canvas.before:
        Color:
            rgb: (.9, .9, .9)
        Rectangle:
            pos: self.x + sp(2), self.y + sp(2)
            size: self.width - sp(4), self.height - sp(4)

ShowcaseScreen:
    name: 'Carousel'
    fullscreen: True

    BoxLayout:
        size_hint_y: None
        height: '48dp'

        ToggleButton:
            text: 'Loop'
            id: btnloop

        Label:
            size_hint_x: None
            width: self.height
            text: '{}'.format(carousel.index)

        Button:
            size_hint_x: None
            width: self.height
            text: 'Prev'
            on_release: carousel.load_previous()

        Button:
            size_hint_x: None
            width: self.height
            text: 'Next'
            on_release: carousel.load_next()

    Carousel:
        id: carousel
        loop: btnloop.state == 'down'

        ColoredLabel:
            text: 'Slide 0'

        ColoredLabel:
            text: 'Slide 1'

        ColoredLabel:
            text: 'Slide 2'

            """,
            "checkboxes.kv": """
ShowcaseScreen:
    name: 'CheckBoxes'

    GridLayout:

        cols: 3
        spacing: '8dp'
        size_hint: .5, None
        height: self.minimum_height

        Label:
            text: 'Checkbox'

        CheckBox:
            size_hint_y: None
            height: '48dp'

        CheckBox:
            size_hint_y: None
            height: '48dp'

        Label:
            text: 'CheckBox with group'

        CheckBox:
            size_hint_y: None
            height: '48dp'
            group: 'g2'

        CheckBox:
            size_hint_y: None
            height: '48dp'
            group: 'g2'

            """,
            "codeinput.kv": """
ShowcaseScreen:

        fullscreen: True
        name: 'CodeInput'

        CodeInput:
                padding: '4dp'
                text: 'class Hello(object):\\tpass\\n\\nprint "Hello world"'
                focus: True if root.parent else False
            """,
            "dropdown.kv": """
ShowcaseScreen:
    fullscreen: True
    name: 'DropDown'

    # trick to not lost the Dropdown instance
    # Dropdown itself is not really made to be used in kv.
    __safe_id: [dropdown.__self__]

    Button:
        id: btn
        text: '-'
        on_release: dropdown.open(self)
        size_hint_y: None
        height: '48dp'

    Widget

    DropDown:

        id: dropdown
        on_parent: self.dismiss()
        on_select: btn.text = 'Selected value: {}'.format(args[1])

        Button:
            text: 'Value A'
            size_hint_y: None
            height: '48dp'
            on_release: dropdown.select('A')

        Button:
            text: 'Value B'
            size_hint_y: None
            height: '48dp'
            on_release: dropdown.select('B')

        Button:
            text: 'Value C'
            size_hint_y: None
            height: '48dp'
            on_release: dropdown.select('C')

            """,
            "filechoosers.kv": """
ShowcaseScreen:
    name: 'FileChoosers'
    fullscreen: True

    BoxLayout:
        size_hint_y: None
        height: '48dp'

        ToggleButton:
            text: 'Icon'
            state: 'down'
            group: 'filechooser'
            on_release: filechooser.view_mode = 'icon'

        ToggleButton:
            text: 'List'
            group: 'filechooser'
            on_release: filechooser.view_mode = 'list'

    FileChooser:
        id: filechooser
        
        FileChooserIconLayout
        FileChooserListLayout
            """,
            "popups.kv": """
ShowcaseScreen:
    popup: popup
    fullscreen: True
    name: 'Popups'
    BoxLayout:
        id: bl
        Popup:
            id: popup
            title: "Hello World"
            on_parent:
                if self.parent == bl: self.parent.remove_widget(self)
            Button:
                text: 'press to dismiss'
                on_release: popup.dismiss()
        Button:
            text: 'press to show Popup'
            on_release: root.popup.open()

            """,
            "progressbar.kv": """
ShowcaseScreen:
    name: 'ProgressBar'

    Label:
        text: 'Progression: {}%'.format(int(pb.value))
        size_hint_y: None
        height: '48dp'

    ProgressBar:
        id: pb
        size_hint_x: .5
        size_hint_y: None
        height: '48dp'
        value: (app.time * 20) % 100.

""",
            "rstdocument.kv": """
ShowcaseScreen:
    name: 'RstDocument'
    fullscreen: True
    on_parent: if not args[1]: textinput.focus = False

    GridLayout:
        cols: 2 if root.width > root.height else 1
        spacing: '8dp'

        TextInput:
            id: textinput
            text:
                ('.. _top:\\n'
                '\\n'
                'Hello world\\n'
                '===========\\n'
                '\\n'
                'This is an **emphased text**, *italic text*, ``interpreted text``.\\n'
                'And this is a reference to top_::\\n'
                '\\n'
                '   $ print("Hello world")\\n')

        RstDocument:
            text: textinput.text
""",
            "scatter.kv": """
ShowcaseScreen:
    name: 'Scatter'

    Widget:

        Scatter:
            id: scatter
            size_hint: None, None
            size: image.size

            Image:
                id: image
                source: 'data/faust_github.jpg'
                size: self.texture_size
""",   
            "screenmanager.kv": """
#:import Factory kivy.factory.Factory

ShowcaseScreen:
    name: 'ScreenManager'
    fullscreen: True

    BoxLayout:
        size_hint_y: None
        height: '48dp'

        Spinner:
            text: 'Default transition'
            values: ('SlideTransition', 'SwapTransition', 'FadeTransition', 'WipeTransition')
            on_text: sm.transition = Factory.get(self.text)()

    ScreenManager:
        id: sm

        Screen:
            name: 'screen1'
            canvas.before:
                Color:
                    rgb: .8, .2, .2
                Rectangle:
                    size: self.size
                
            AnchorLayout:
                Button:
                    size_hint: None, None
                    size: '150dp', '48dp'
                    text: 'Go to screen 2'
                    on_release: sm.current = 'screen2'

        Screen:
            name: 'screen2'
            canvas.before:
                Color:
                    rgb: .2, .8, .2
                Rectangle:
                    size: self.size
            AnchorLayout:
                Button:
                    size_hint: None, None
                    size: '150dp', '48dp'
                    text: 'Go to screen 1'
                    on_release: sm.current = 'screen1'
""",   
            "sliders.kv": """
ShowcaseScreen:
    name: 'Sliders'

    BoxLayout:
        size_hint_y: None
        height: '48dp'

        Label:
            text: 'Default'

        Slider:
            id: s1

        Label:
            text: '{}'.format(s1.value)


    BoxLayout:
        size_hint_y: None
        height: '48dp'

        Label:
            text: 'Stepped'

        Slider:
            id: s2
            step: 20

        Label:
            text: '{}'.format(s2.value)

    AnchorLayout:
        size_hint_y: None
        height: '100dp'

        GridLayout:
            cols: 2
            spacing: '8dp'
            size_hint_x: None
            width: self.minimum_width

            Slider:
                size_hint_x: None
                width: '48dp'
                orientation: 'vertical'
                value: s1.value
                on_value: s1.value = self.value

            Slider:
                size_hint_x: None
                width: '48dp'
                orientation: 'vertical'
                step: 20
                value: s2.value
                on_value: s2.value = self.value
""",   
            "spinner.kv": """
ShowcaseScreen:
    name: 'Spinner'
    fullscreen: True

    Spinner:
        text: 'Home'
        values: ('Home', 'Work', 'Other', 'Not defined')
        size_hint_y: None
        height: '48dp'

    Widget
""",   
            "splitter.kv": """
ShowcaseScreen:
    name: 'Splitter'
    fullscreen: True

    RelativeLayout:
        id: rl

        Splitter:
            sizable_from: 'right'
            min_size: 10
            max_size: rl.width
            Button:
                text: 'Panel'
""",   
            "switches.kv": """
ShowcaseScreen:
    name: 'Switches'

    BoxLayout:
        size_hint_y: None
        height: '48dp'

        Label:
            text: 'Switch normal'
        Switch:

    BoxLayout:
        size_hint_y: None
        height: '48dp'

        Label:
            text: 'Switch active'
        Switch:
            active: True

    BoxLayout:
        size_hint_y: None
        height: '48dp'

        Label:
            text: 'Switch off & disabled'
        Switch:
            disabled: True
            active: False

    BoxLayout:
        size_hint_y: None
        height: '48dp'

        Label:
            text: 'Switch on & disabled'
        Switch:
            disabled: True
            active: True
""",   
            "textinputs.kv": """
ShowcaseScreen:
    name: 'TextInputs'
    focused: ti_default
    on_parent:
        if not args[1] and self.focused: self.focused.focus = False
        if args[1]: ti_default.focus = True

    CTextInput
        size_hint_y: None
        height: '32dp'
        multiline: False
        text: 'Monoline textinput'

    CTextInput:
        id: ti_default
        size_hint_y: None
        height: '32dp'
        text: 'Focused textinput'
        focus: True

    CTextInput:
        size_hint_y: None
        height: '32dp'
        text: 'Password'
        password: True

    CTextInput:
        size_hint_y: None
        height: '32dp'
        text: 'Readonly textinput'
        readonly: True

    CTextInput:
        size_hint_y: None
        height: '48dp'
        text: 'Multiline textinput\\nSecond line'
        multiline: True

    CTextInput:
        size_hint_y: None
        height: '32dp'
        disabled: True
        text: 'Disabled textinput'

<CTextInput@TextInput>
    on_focus:
        screen = self.parent.parent.parent.parent
        if screen.parent: screen.focused = self
""",   
            "togglebutton.kv": """
ShowcaseScreen:
    name: 'ToggleButton'

    GridLayout:

        cols: 3
        spacing: '8dp'
        size_hint_y: None
        height: self.minimum_height

        Label:
            text: 'Choice 1'

        ToggleButton:
            size_hint_y: None
            height: '48dp'
            text: 'A'
            group: 'g1'

        ToggleButton:
            size_hint_y: None
            height: '48dp'
            text: 'B'
            group: 'g1'

        Label:
            text: 'Choice 2'

        ToggleButton:
            size_hint_y: None
            height: '48dp'
            text: 'A'
            group: 'g2'

        ToggleButton:
            size_hint_y: None
            height: '48dp'
            text: 'B'
            group: 'g2'
""",
            "tabbedpanel + layouts.kv": """
#:import random random.random

ShowcaseScreen:
    name: 'TabbedPanel + Layouts'
    fullscreen: True
    on_parent: if args[1] and tp.current_tab == tab_fl: app.showcase_floatlayout(fl)

    TabbedPanel:
        id: tp
        do_default_tab: False

        TabbedPanelItem:
            id: tab_fl
            text: 'FloatLayout'
            on_release: app.showcase_floatlayout(fl)
            FloatLayout:
                CFloatLayout:
                    id: fl
        TabbedPanelItem:
            text: 'BoxLayout'
            on_release: app.showcase_boxlayout(box)
            FloatLayout
                CBoxLayout:
                    id: box
        TabbedPanelItem:
            text: 'GridLayout'
            on_release: app.showcase_gridlayout(grid)
            FloatLayout
                CGridLayout:
                    id: grid
                    rows: 3
        TabbedPanelItem:
            on_release: app.showcase_stacklayout(stack)
            text: 'StackLayout'
            FloatLayout
                CStackLayout:
                    id: stack
        TabbedPanelItem:
            text: 'AnchorLayout'
            on_release: app.showcase_anchorlayout(anchor)
            FloatLayout
                CAnchorLayout:
                    id: anchor
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint: .4, .5
                        Button
                        Button
                            text: 'anchor_x: {}'.format(anchor.anchor_x)
                        Button
                            text: 'anchor_y: {}'.format(anchor.anchor_y)
                        Button

<CFloatLayout@FloatLayout+BackgroundColor>
<CBoxLayout@BoxLayout+BackgroundColor>
<CGridLayout@GridLayout+BackgroundColor>
<CStackLayout@StackLayout+BackgroundColor>
<CAnchorLayout@AnchorLayout+BackgroundColor>


<BackgroundColor@Widget>
    pos_hint: {'center_x': .5, 'center_y': .5}
    size_hint: .9, .9
    canvas.before:
        Color:
            rgba: .2, .3, .4, 1
        Rectangle:
            size: self.size
            pos: self.pos
"""
        }
        screen_str = name_to_map[self.available_screens[index].lower().split("/")[-1]]
        screen = Builder.load_string(screen_str)
        self.screens[index] = screen
        return screen

    def read_sourcecode(self):
        fn = self.available_screens[self.index].lower()
        with open(fn) as fd:
            return fd.read()

    def toggle_source_code(self):
        self.show_sourcecode = not self.show_sourcecode
        if self.show_sourcecode:
            height = self.root.height * .3
        else:
            height = 0

        Animation(height=height, d=.3, t='out_quart').start(
                self.root.ids.sv)

        self.update_sourcecode()

    def update_sourcecode(self):
        if not self.show_sourcecode:
            self.root.ids.sourcecode.focus = False
            return
        self.root.ids.sourcecode.text = self.read_sourcecode()
        self.root.ids.sv.scroll_y = 1

    def showcase_floatlayout(self, layout):

        def add_button(*t):
            if not layout.get_parent_window():
                return
            if len(layout.children) > 5:
                layout.clear_widgets()
            layout.add_widget(Builder.load_string('''
#:import random random.random
Button:
    size_hint: random(), random()
    pos_hint: {'x': random(), 'y': random()}
    text:
        'size_hint x: {} y: {}\\n pos_hint x: {} y: {}'.format(\
            self.size_hint_x, self.size_hint_y, self.pos_hint['x'],\
            self.pos_hint['y'])
'''))
            Clock.schedule_once(add_button, 1)
        Clock.schedule_once(add_button)

    def showcase_boxlayout(self, layout):

        def add_button(*t):
            if not layout.get_parent_window():
                return
            if len(layout.children) > 5:
                layout.orientation = 'vertical'\
                    if layout.orientation == 'horizontal' else 'horizontal'
                layout.clear_widgets()
            layout.add_widget(Builder.load_string('''
Button:
    text: self.parent.orientation if self.parent else ''
'''))
            Clock.schedule_once(add_button, 1)
        Clock.schedule_once(add_button)

    def showcase_gridlayout(self, layout):

        def add_button(*t):
            if not layout.get_parent_window():
                return
            if len(layout.children) > 15:
                layout.rows = 3 if layout.rows is None else None
                layout.cols = None if layout.rows == 3 else 3
                layout.clear_widgets()
            layout.add_widget(Builder.load_string('''
Button:
    text:
        'rows: {}\\ncols: {}'.format(self.parent.rows, self.parent.cols)\
        if self.parent else ''
'''))
            Clock.schedule_once(add_button, 1)
        Clock.schedule_once(add_button)

    def showcase_stacklayout(self, layout):
        orientations = ('lr-tb', 'tb-lr',
                        'rl-tb', 'tb-rl',
                        'lr-bt', 'bt-lr',
                        'rl-bt', 'bt-rl')

        def add_button(*t):
            if not layout.get_parent_window():
                return
            if len(layout.children) > 11:
                layout.clear_widgets()
                cur_orientation = orientations.index(layout.orientation)
                layout.orientation = orientations[cur_orientation - 1]
            layout.add_widget(Builder.load_string('''
Button:
    text: self.parent.orientation if self.parent else ''
    size_hint: .2, .2
'''))
            Clock.schedule_once(add_button, 1)
        Clock.schedule_once(add_button)

    def showcase_anchorlayout(self, layout):

        def change_anchor(self, *l):
            if not layout.get_parent_window():
                return
            anchor_x = ('left', 'center', 'right')
            anchor_y = ('top', 'center', 'bottom')
            if layout.anchor_x == 'left':
                layout.anchor_y = anchor_y[anchor_y.index(layout.anchor_y) - 1]
            layout.anchor_x = anchor_x[anchor_x.index(layout.anchor_x) - 1]

            Clock.schedule_once(change_anchor, 1)
        Clock.schedule_once(change_anchor, 1)

    def _update_clock(self, dt):
        self.time = time()

def list_files(startpath):
    file_list = ""
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        file_list = file_list + "\n" + ('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            file_list = file_list + "\n" + ('{}{}'.format(subindent, f))
    return file_list

if __name__ == '__main__':
    ShowcaseApp().run()
