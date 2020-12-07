from datetime import datetime
import gtk
from neo4j.v1 import GraphDatabase, basic_auth
import pygtk


pygtk.require('2.0')

class Base:
    
    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget=None, data=None):
        self.session.close()
        gtk.main_quit()
        
    def setup(self):
        print "Please override it"
        
    def query(self):
        print "Please override it"
        
    def motif(self, i, *args):
        if i == 1:
            return "MATCH ({0})-[:LINK]->({1})-[:LINK]->({2})-[:LINK]->({3}) WHERE {0} <> {2} AND {0} <> {3} AND {1} <> {3}".format(*args)
        elif i == 2:
            return "MATCH ({0})-[:LINK]->({1})-[:LINK]->({2}), ({1})-[:LINK]->({3}) WHERE {0} <> {2} AND {0} <> {3} AND {1} <> {3}".format(*args)
        elif i == 3:
            return "MATCH ({0})-[:LINK]->({1})-[:LINK]->({2})-[:LINK]->({3}) WHERE {0} <> {2} AND {0} <> {3} AND {1} <> {3} AND ({1})-[:LINK]-({3})".format(*args)
        elif i == 4:
            return "MATCH ({0})-[:LINK]->({1})-[:LINK]->({2})-[:LINK]->({3}) WHERE {0} <> {2} AND {0} <> {3} AND {1} <> {3} AND ({0})-[:LINK]-({3})".format(*args)
        elif i == 5:
            return "MATCH ({0})-[:LINK]->({1})-[:LINK]->({2})-[:LINK]->({3}) WHERE {0} <> {2} AND {0} <> {3} AND {1} <> {3} AND ({0})-[:LINK]-({2}) AND ({0})-[:LINK]-({3})".format(*args)
        elif i == 6:
            return "MATCH ({0})-[:LINK]->({1})-[:LINK]->({2})-[:LINK]->({3}) WHERE {0} <> {2} AND {0} <> {3} AND {1} <> {3} AND ({0})-[:LINK]-({2}) AND ({0})-[:LINK]-({3}) AND ({1})-[:LINK]-({3})".format(*args)                
        
    def entry(self, text, *changed):
        hbox = gtk.HBox()
            
        label = gtk.Label()
        label.set_text(text)
        label.show()
        hbox.add(label)

        entry = gtk.Entry()
        entry.connect("changed", *changed)
        entry.show()
        hbox.add(entry)

        hbox.show()
        return hbox

    def combo(self, text, store, *changed):
        hbox = gtk.HBox()
            
        if text is not None:
            label = gtk.Label()
            label.set_text(text)
            label.show()
            hbox.add(label)

        combo = gtk.ComboBox(store)
        combo.connect("changed", *changed)
        renderer = gtk.CellRendererText()
        combo.pack_start(renderer, True)
        combo.add_attribute(renderer, "text", 1)
        combo.show()
        hbox.add(combo)

        hbox.show()
        return hbox
    
    def run(self, *args):
        start = datetime.now()
        self.query()
        #self.status.remove_all()
        self.status.push(0, "Tempo total %sus" % (datetime.now() - start))

    def __init__(self):
        self.types = gtk.ListStore(int, str)
        self.types.append([1, "Linear"])
        self.types.append([2, "Estrela"])
        self.types.append([3, "Pipa"])
        self.types.append([4, "Quadrangular"])
        self.types.append([5, "Diag"])
        self.types.append([6, "K4"])
        
        self.tscp = gtk.ListStore(int, str)
        self.tscp.append([1, "O"])
        self.tscp.append([0, "N"])
        self.tscp.append([-1, "S"])
        
        self.driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "admin"))
        try:
            self.session = self.driver.session()
        except Exception as e:
            md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE, e.message)
            md.run()
            exit()
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)
        
        self.container = gtk.VBox()
        self.container.show()
        self.window.add(self.container)
        
        self.setup()
        
        self.status = gtk.Statusbar()
        self.status.show()
        self.container.add(self.status)
        
        self.window.show()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    base = Base()
    base.main()