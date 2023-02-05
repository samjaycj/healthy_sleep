from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.uix.list import TwoLineIconListItem, IconLeftWidgetWithoutTouch
from kivymd.uix.pickers import MDTimePicker
from datetime import datetime,timedelta
from kivy.properties import ObjectProperty
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivy.uix.settings import SettingsWithSidebar
from jsonsettings import settings_json

class Content(MDBoxLayout):
    pass

class MainApp(MDApp):
    icon_list_s = []
    icon_list_w = []
    timetosleep=0
    tf="%H:%M:%S"
    dtf="%Y-%m-%d %H:%M:%S"

    def build(self):
        #self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = False
        self.timetosleep = int(self.config.get('HealthySleep', 'timetosleep'))
        timeformat=self.config.get('HealthySleep', 'timeformat')
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepOrange"
        if timeformat=='24H': 
            self.tf="%H:%M:%S"
            self.dtf="%Y-%m-%d %H:%M:%S"
        else:
            self.tf="%I:%M %p"
            self.dtf="%Y-%m-%d %I:%M %p"

    def build_config(self, config):
        config.setdefaults('HealthySleep', {
            'timetosleep': 15,
            'timeformat': '24H'})

    def build_settings(self, settings):
        settings.add_json_panel('Settings',
                                self.config,
                                data=settings_json)

    def on_config_change(self, config, section,
                         key, value):
        self.timetosleep = int(self.config.get('HealthySleep', 'timetosleep'))
        timeformat=self.config.get('HealthySleep', 'timeformat')
        if timeformat=='24H': 
            self.tf="%H:%M:%S"
            self.dtf="%Y-%m-%d %H:%M:%S"
        else:
            self.tf="%I:%M %p"
            self.dtf="%Y-%m-%d %I:%M %p"

    def on_start(self):
        self.root.ids.box.add_widget(
            MDExpansionPanel(
                icon="emoticon-happy-outline",
                content=Content(),
                panel_cls=MDExpansionPanelOneLine(
                    text="I'm Happy about the app",
                )
            )
        )
        self.root.ids.box.add_widget(
            MDExpansionPanel(
                icon="emoticon-neutral-outline",
                content=Content(),
                panel_cls=MDExpansionPanelOneLine(
                    text="Nothing bad or good to say",
                )
            )
        )
        self.root.ids.box.add_widget(
            MDExpansionPanel(
                icon="emoticon-sad-outline",
                content=Content(),
                panel_cls=MDExpansionPanelOneLine(
                    text="I'm Unsatisfied about the app",
                )
            )
        )


    def disp_alarm_sleep(self):
        sdt=self.root.ids.stime.text
        if (sdt!=""):
            Current_date = datetime.now()
            dt = datetime.strptime(sdt, self.tf)
            dtadded=dt+timedelta(minutes=self.timetosleep)
            t1=dtadded.time()
            t2 = Current_date.time()
            if t1>t2: 
                d=Current_date.date()
            else:
                d=Current_date.date()+timedelta(1)
            self.root.ids.alarm_list_w.clear_widgets()
            dt_calc=datetime.combine(d,t1)
            self.icon_list_w.clear()
            for i in range(7):
                stime=dt_calc+timedelta(hours=1.5*(i+1))
                strstime=stime.strftime(self.dtf)
                icons=IconLeftWidgetWithoutTouch(icon="bell-outline")
                listitem=TwoLineIconListItem(text=str(strstime),secondary_text="Cycle "+str(i+1)+" Alarm")
                self.icon_list_w.append(icons)
                listitem.add_widget(icons)
                listitem.bind(on_release=self.change_icon)
                self.root.ids.alarm_list_w.add_widget(listitem, index=i)


    def change_icon(self,listdata):
        sindex = self.root.ids.alarm_list_w.children.index(listdata)
        if self.icon_list_w[sindex].icon == "bell":
            self.icon_list_w[sindex].icon = "bell-outline"
        else:
            self.icon_list_w[sindex].icon ="bell"

    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(on_save=self.get_time)
        time_dialog.open()

       
    def get_time(self, instance, time):            
        self.root.ids.stime.text=time.strftime(self.tf)
        self.disp_alarm_sleep()

    def disp_alarm_wake(self):
        wdt=self.root.ids.wtime.text
        if (wdt!=""):
            Current_date = datetime.now()
            dt = datetime.strptime(wdt, self.tf)
            dtadded=dt-timedelta(minutes=self.timetosleep)
            t1=dtadded.time()
            t2 = Current_date.time()
            if t1>t2: 
                d=Current_date.date()
            else:
                d=Current_date.date()+timedelta(1)
            self.root.ids.alarm_list_s.clear_widgets()
            dt_calc=datetime.combine(d,t1)
            self.icon_list_s.clear()
            for i in range(7):
                stime=dt_calc-timedelta(hours=1.5*(i+1))
                strstime=stime.strftime(self.dtf)
                icons=IconLeftWidgetWithoutTouch(icon="bell-outline")
                listitem=TwoLineIconListItem(text=str(strstime),secondary_text="Cycle "+str(i+1)+" Alarm")
                self.icon_list_s.append(icons)
                listitem.add_widget(icons)
                listitem.bind(on_release=self.change_icon2)
                self.root.ids.alarm_list_s.add_widget(listitem, index=i)


    def change_icon2(self,listdata):
        sindex = self.root.ids.alarm_list_s.children.index(listdata)
        if self.icon_list_s[sindex].icon == "bell":
            self.icon_list_s[sindex].icon = "bell-outline"
        else:
            self.icon_list_s[sindex].icon ="bell"

    def show_time_picker_s(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(on_save=self.get_time_s)
        time_dialog.open()

       
    def get_time_s(self, instance, time):            
        self.root.ids.wtime.text=time.strftime(self.tf)
        self.disp_alarm_wake()

    def pick_time_format(self):
        self.menu_list = [
            {
                "viewclass": "OneLineListItem",
                "text": "24H",
                "on_release": lambda x="24H": self.drop_option(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "12H",
                "on_release": lambda x="12H": self.drop_option(x)
            }
        ]
        self.dropdown=MDDropdownMenu(
            caller=self.root.ids.ftimedrop,
            items = self.menu_list,
            width_mult=4
        )
        self.dropdown.open()

    def drop_option(self, option_text):
        self.root.ids.ftime.text=option_text
        self.dropdown.dismiss()

class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


MainApp().run()



