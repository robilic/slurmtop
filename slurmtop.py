
from re import I
from textual.app import App, ComposeResult, RenderResult
from textual.widgets import Static, DataTable, Label, TextArea
from textual.containers import Container, Vertical
from textual import events
from textual.message import Message
from textual import log

import slurmtopUtils as stu
   
class JobTable(Container):
  jobtable = DataTable()
  
  def __init__(self, title: str) -> None:
    super().__init__()
    self._title = title
  
  def on_mount(self) -> None:
    table = self.query_one(DataTable)
    table.cursor_type = "row"
    table.styles.overflow_x = "hidden"
    self.styles.border = ("heavy", "white")
  
  def _test_dt(self) -> DataTable:
    l = stu.get_joblist("ub01556")
    #self.jobtable.clear()
    self.jobtable.add_columns("JOB", "PARTITION", "NAME", "USER", "STATE", "TIME", "NODES", "NODELIST(REASON)")
    for x in l.splitlines():
      r = x.split()
      self.jobtable.add_row(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7])
    return self.jobtable
  
  def compose(self) -> ComposeResult:
    yield self._test_dt()
  
  class Selected(Message):
    def __init__(self, job_name: str) -> None:
      self.job_name = job_name
      super().__init__()
  
  def on_data_table_row_selected(self, message: DataTable.RowSelected) -> None:
    log("Row = ", self.jobtable.get_cell_at((message.cursor_row, 0)))
    super().post_message(self.Selected(self.jobtable.get_cell_at((message.cursor_row, 0))))

class JobDetailTable(Container):
  job_name = ''
  dt = DataTable()
  
#  class Selected(Message):
#    def __init__(self, overlay_file_name: str) -> None:
#      self.overlay_file_name = overlay_file_name
#      log("OverlayDetailTable.Selected() overlay_file_name = ", overlay_file_name)
#      super().__init__()
  
  def __init__(self, title: str) -> None:
    super().__init__()
    self._title = title

  def on_mount(self) -> None:
    # what is table, vs dt?
    table = self.query_one(DataTable)
    table.cursor_type = "row"
    self.styles.border = ("heavy", "white")
    self.dt.add_columns("JOBID", "UID", "CPUS", "NODES")
  
  def _test_dt(self) -> DataTable:
    self.dt.clear()
    if self.job_name != '':
      l = stu.get_jobinfo(self.job_name)
      for x in l.splitlines():
        r = x.split()
        self.dt.add_row(r[0], r[1], r[2], r[3])
    
    return self.dt

#  def on_data_table_row_selected(self, message: DataTable.RowSelected) -> None:
#    log("OverlayDetailTable() selected ", self.dt.get_cell_at((message.cursor_row, 4)))
#    super().post_message(self.Selected(self.dt.get_cell_at((message.cursor_row, 4))))

  def compose(self) -> ComposeResult:
    #yield Label(self._title)
    yield self._test_dt()

class NodesTable(Container):
  job_name = ''
  dt = DataTable()

#  class Selected(Message):
#    def __init__(self, overlay_file_name: str) -> None:
#      self.overlay_file_name = overlay_file_name
#      log("OverlayDetailTable.Selected() overlay_file_name = ", overlay_file_name)
#      super().__init__()

  def __init__(self, title: str) -> None:
    super().__init__()
    self._title = title

  def on_mount(self) -> None:
    # what is table, vs dt?
    table = self.query_one(DataTable)
    table.cursor_type = "row"
    self.styles.border = ("heavy", "white")
    self.dt.add_columns("NODENAME", "CPU", "MEM")

  def _test_dt(self) -> DataTable:
    #this will be all the node related info
    self.dt.clear()
    if self.job_name != '':
      nodes = stu.get_nodelist(self.job_name)
      #l = stu.get_jobinfo(self.job_name)
      for x in nodes.splitlines():
        r = x.split()
        nodeusage = stu.get_nodeusage(r[0], "ub01556")
        nr = nodeusage.split()
        self.dt.add_row(r[0], nr[0], nr[1])

    return self.dt

#  def on_data_table_row_selected(self, message: DataTable.RowSelected) -> None:
#    log("OverlayDetailTable() selected ", self.dt.get_cell_at((message.cursor_row, 4)))
#    super().post_message(self.Selected(self.dt.get_cell_at((message.cursor_row, 4))))

  def compose(self) -> ComposeResult:
    #yield Label(self._title)
    yield self._test_dt()

class MyApp(App):
  #CSS_PATH = "wwdive.tcss"
  #ODT = OverlayDetailTable("Overlay Detail")
  JT = JobTable("Job Table")
  JDT = JobDetailTable("Job Detail Table")
  NT = NodesTable("Nodes Table")

  def compose(self) -> ComposeResult:
    #yield OverlayTable("Overlays")
    yield self.JT
    yield self.JDT
    yield self.NT
    #yield Static("Two", classes="box")
    #yield self.FV

  def on_job_table_selected(self, message: JobTable.Selected) -> None:
    self.JDT.job_name = message.job_name
    self.JDT._test_dt()
    self.NT.job_name = message.job_name
    self.NT._test_dt()
  
#  def on_overlay_detail_table_selected(self, message: OverlayDetailTable.Selected) -> None:
#    self.FV.overlay_name = self.ODT.overlay_name
#    self.FV.file_to_show = message.overlay_file_name
#    self.FV.load_file()

#  def on_key(self, event: events.Key) -> None:
#    if event.key.isdecimal():
#      self.screen.styles.background = self.COLORS[int(event.key)]

if __name__ == "__main__":
  app = MyApp()
  app.run()


