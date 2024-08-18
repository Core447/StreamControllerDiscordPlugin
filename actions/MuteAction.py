from gi.repository import Gtk, Adw

from plugins.StreamControllerDiscordPlugin.DiscordActionBase import DiscordActionBase


class MuteAction(DiscordActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mode: str = None

    def on_ready(self):
        self.load_config()

    def load_config(self):
        settings = self.get_settings()
        self.mode = settings.get('mode')
        if not self.mode:
            self.mode = 'Mute'

    def get_config_rows(self):
        super_rows = super().get_config_rows()
        self.action_model = Gtk.StringList()
        self.mode_row = Adw.ComboRow(
            model=self.action_model, title=self.plugin_base.lm.get("actions.mute.choice.title"))

        index = 0
        found = 0
        for k in ['Mute', 'Unmute', 'Toggle']:
            self.action_model.append(k)
            if self.mode == k:
                print('Setting to {0}:{1}', k, index)
                found = index
            index += 1
        self.mode_row.set_selected(found)

        self.mode_row.connect("notify::selected", self.on_change_mode)
        super_rows.append(self.mode_row)
        return super_rows

    def on_change_mode(self, *_):
        settings = self.get_settings()
        selected_index = self.mode_row.get_selected()
        settings['mode'] = self.action_model[selected_index].get_string()
        self.mode = settings['mode']
        self.set_settings(settings)

    def on_key_down(self):
        match self.mode:
            case "Mute":
                self.plugin_base.backend.set_mute(True)
            case "Unmute":
                self.plugin_base.backend.set_mute(False)
            case "Toggle":
                status = self.get_current_mute()
                self.plugin_base.backend.set_mute(not status)

    def get_current_mute(self):
        resp = self.plugin_base.backend.get_voice_settings()
        print(resp)
        return False
