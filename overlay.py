#!/usr/bin/env python

import gtk

from base import Base


class Shortest(Base):
    
    def query(self):
        query = str()
        query += "%s AND %s " % (self.motif(self.type, 'a', 'b', 'c', 'd'), " AND ".join("%s.nome = '%s'" % (k, v[0]) for k, v in self.motif1.items()))
        query += "MATCH (p)-[:TSCP]->(a) WHERE %s "  % " AND ".join("(%s)<-[:TSCP{valor:%s}]-(p)" % (k, v[1]) for k, v in self.motif1.items())
        query += "AND (d)<-[:TSCP{valor:%s}]-(p) " % self.extra
        #query += "WHERE a.tnbc is NOT NULL AND b.tnbc is NOT NULL AND c.tnbc is NOT NULL AND d.tnbc is NOT NULL "
        query += "RETURN DISTINCT p.nome as paciente, d.nome as proteina"

        print query
        
        #return
        
        result = self.session.run(query)

        self.text.set_buffer(gtk.TextBuffer())
        for record in result:     
            buff = self.text.get_buffer()
            buff.insert_at_cursor("%s - %s\n" % (record['paciente'], record['proteina']))
    
    def setup(self):
        self.window.set_title("Sobreposicao de Motifs")
        self.window.resize(200, 150)
        
        self.type = 0;
        self.extra = None
        
        self.motif1 = {'a':[None,None], 'b':[None,None], 'c':[None,None]}
        self.motif1 = {'a':['RPL6',0], 'b':['RPL37A',0], 'c':['M6PR',0]}

        self.container.add(self.combo(None, self.types, self.on_motif_changed))        
        
        for k in sorted(self.motif1):                     
            hbox = self.entry(" %s " % k.upper(), self.on_entry_changed, k)
            hbox.add(self.combo(None, self.tscp, self.on_combo_changed, k))        
            self.container.add(hbox)

        hbox = self.entry(" D ", self.on_entry_changed, k)
        item = hbox.get_children()
        item[1].set_sensitive(False)
        hbox.add(self.combo(None, self.tscp, self.on_extra_changed, k))        
        self.container.add(hbox)
        
        self.container.add(self.entry('Amostra: ', self.on_entry_changed, 1, 'a'))
        
        button = gtk.Button()
        button.set_label('Procurar')
        button.connect("clicked", self.run)
        button.show()
        self.container.add(button)
        
        self.text = gtk.TextView()
        self.text.set_size_request(-1, 300)
        self.text.show()
        self.container.add(self.text)

    def on_motif_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            self.type = model[tree_iter][0]
        
    def on_entry_changed(self, entry, name):
        self.motif1[name][0] = entry.get_text()
        
    def on_combo_changed(self, combo, name):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            self.motif1[name][1] = model[tree_iter][0]
        
    def on_extra_changed(self, combo, name):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            self.extra = model[tree_iter][0]
        
if __name__ == "__main__":
    base = Shortest()
    base.main()