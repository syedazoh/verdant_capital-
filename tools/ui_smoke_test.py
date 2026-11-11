"""Offline component smoke runner when Streamlit is not installed.

Not a substitute for launching Streamlit on the target machine. Exercises view
code and Plotly chart generation against real fictional demo results.
"""
from __future__ import annotations
import runpy
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FakeStreamlit(types.ModuleType):
    def __init__(self, run_button=False, mode="demo"):
        super().__init__("streamlit")
        self.sidebar = self
        self.session_state = {}
        self.plot_count=0
        self.render_count=0
        self.run_button=run_button
        self.mode=mode
        self.errors=[]

    def __enter__(self): return self
    def __exit__(self, *args): return False
    def set_page_config(self, **kw): pass
    def markdown(self, *a, **kw): self.render_count+=1
    def caption(self, *a, **kw): pass
    def divider(self): pass
    def radio(self, label, options, **kw): return options[1] if self.mode=="market" else options[kw.get("index",0)]
    def number_input(self, label, **kw): return kw["value"]
    def selectbox(self, label, options, **kw): return options[kw.get("index",0)]
    def toggle(self,label,**kw): return kw.get("value",False)
    def multiselect(self, label, options, **kw): return kw.get("default",options)
    def text_area(self, label, **kw): return kw.get("value","")
    def button(self, *a, **kw): return self.run_button
    def columns(self, n, **kw): return [self]* (len(n) if isinstance(n,(list,tuple)) else n)
    def tabs(self, values): return [self]*len(values)
    def expander(self, *a, **kw): return self
    def spinner(self,*a,**kw): return self
    def plotly_chart(self, fig, **kw):
        assert fig is not None
        self.plot_count+=1
    def info(self,*a,**kw): pass
    def warning(self,*a,**kw): pass
    def success(self,*a,**kw): pass
    def error(self,msg,*a,**kw): self.errors.append(msg)
    def json(self,*a,**kw): pass
    def dataframe(self,*a,**kw): pass
    def metric(self,*a,**kw): pass
    def write(self,*a,**kw): pass
    def download_button(self,*a,**kw): pass
    def code(self,*a,**kw): pass


def main():
    sys.path.insert(0,str(ROOT))
    total_charts=0
    for mode, press in [("demo",False),("demo",True),("market",False)]:
        fake=FakeStreamlit(run_button=press,mode=mode)
        sys.modules["streamlit"]=fake
        runpy.run_path(str(ROOT/"app.py"),run_name="__main__")
        assert not fake.errors, fake.errors
        minimum=4 if mode=="demo" else 3
        assert fake.plot_count >= minimum, f"Expected visualizations in {mode}, got {fake.plot_count}"
        assert fake.render_count >= 20
        total_charts+=fake.plot_count
    print(f"Offline UI smoke passed: preview, Run action and missing-market-data modes; {total_charts} total Plotly charts; zero view errors.")


if __name__=="__main__":
    main()
