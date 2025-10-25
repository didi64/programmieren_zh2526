import re
from ipywidgets import VBox, HBox, Text, Checkbox, BoundedIntText
from nbf import helpers


class PatternCollector:
    def __init__(self):
        self.state = {}
        self.all_pats = []
        self.any_pats = []
        self.checkbox_re = Checkbox(indent=False, layout={'width': '100px'})
        self.checkbox_ic = Checkbox(value=True, indent=False, layout={'width': '100px'})
        self.textbox1 = Text(value='',
                             placeholder='Stichworte (z.B. Funktion Variable)',
                             continuous_update=False,
                             )
        self.textbox2 = Text(value='',
                             placeholder='Stichworte (z.B. dict list)',
                             continuous_update=False,
                             )
        self.int_text = BoundedIntText(value=5, min=1, layout={'width': '150px'})
        self.widgets = [self.textbox1, self.textbox2, self.checkbox_re, self.checkbox_ic, self.int_text] 
        self.descriptions = ['Alle:', 'Manche:', 'Regex', 'Case egal', 'Resultate:']
        for w, descr in zip(self.widgets, self.descriptions):
            w.description = descr

        self.hbox = HBox(children=[self.checkbox_re, self.checkbox_ic, self.int_text]) 
        self.widget = VBox(children=[self.textbox1, self.textbox2, self.hbox])

    def update_state(self):
        # fpat = r'(^|[ @,;:\(\[{{=<>\n])({})([ ,;:\)\]}}\n]|$)'
        for w in self.widgets:
            self.state[w.description] = w.value

        flags = re.IGNORECASE if self.state['Case egal'] else 0
        self.max_res = self.state['Resultate:']

        if self.state['Regex']:
            self.all_pats = [re.compile(self.state['Alle:'], flags=flags)]
            self.any_pats = [re.compile(self.state['Manche:'], flags=flags)]
        else:
            self.all_pats = [re.compile(helpers.wrap_pattern(p), flags=flags)
                             for p in helpers.mysplit(self.state['Alle:']) if p]
            self.any_pats = [re.compile(helpers.wrap_pattern(p), flags=flags)
                             for p in helpers.mysplit(self.state['Manche:']) if p]

        # print('all:', self.all_pats)
        # print('any:', self.any_pats)

    def __repr__(self):
        return 'PatternCollector()'

    def _ipython_display_(self):
        display(self.widget)