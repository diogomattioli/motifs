#!/usr/bin/env python

import gtk

from base import Base


class Shortest(Base):
    
    def query(self):
        query = str()
        query += "%s AND %s " % (self.motif(self.type1, 'a', 'b', 'c', 'd'), " AND ".join("%s.nome = '%s'" % (k, v[0]) for k, v in self.motif1.items()))
        query += "MATCH %s "  % ", ".join("(%s)<-[:TSCP{valor:%s}]-(p)" % (k, v[1]) for k, v in self.motif1.items())
        query += "%s AND %s " % (self.motif(self.type2, 'e', 'f', 'g', 'h'), " AND ".join("%s.nome = '%s'" % (k, v[0]) for k, v in self.motif2.items()))
        query += "MATCH %s WITH a, b, c, d, e, f, g, h, p LIMIT 1 "  % ", ".join("(%s)<-[:TSCP{valor:%s}]-(p)" % (k, v[1]) for k, v in self.motif2.items())
        query += "MATCH sp = allShortestPaths((x)-[*]->(y)) WHERE x IN [a, b, c, d] AND y IN [e, f, g, h] "
        #query += "AND all(z in nodes(sp) WHERE z.tnbc IS NOT NULL) "
        #query += "AND all(z in rels(sp) WHERE z.pontuacao_combinada >= %s AND z.pontuacao_combinada <= %s) " % (scorea, scoreb) 
        query += "RETURN p.nome as paciente, extract(z in nodes(sp) | ID(z)) as ids, extract(z in nodes(sp) | z.nome) as nomes, extract(z in rels(sp) | z.pontuacao_combinada) as pontuacao, length(sp) as comprimentos ORDER BY comprimentos"

        print(query)
        
        return

        result = self.session.run(query)

        self.text.set_buffer(gtk.TextBuffer())
        for record in result:     
            buff = self.text.get_buffer()
            buff.insert_at_cursor("%s %s %s %s\n" % (record["comprimentos"], record["paciente"], record["nomes"], record["pontuacao"]))
    
    def setup(self):
        self.window.set_title("Caminho mais curto entre dois motifs")
        self.window.resize(300, 150)
        
        self.type1 = 0;
        self.type2 = 0;
        
        self.motif1 = {'a':[None,None], 'b':[None,None], 'c':[None,None], 'd':[None,None]}
        self.motif2 = {'e':[None,None], 'f':[None,None], 'g':[None,None], 'h':[None,None]}
                        
        self.motif1 = {'a':['RPL6',0], 'b':['RPL37A',0], 'c':['M6PR',0], 'd':['RPS28',0]}
        self.motif2 = {'e':['ARF5',0], 'f':['PNMAL2',0], 'g':['RPS15',0], 'h':['RAD23A',0]}
                        
        hobox = gtk.HBox()

        for i in range(1,3): 

            vbox = gtk.VBox()
            
            if i == 1:
                names = self.motif1
            else:
                names = self.motif2
        
            vbox.add(self.combo(None, self.types, self.on_motif_changed, i))        
        
            for k in sorted(names):                     
                hbox = self.entry(" %s " % k.upper(), self.on_entry_changed, i, k)
                hbox.add(self.combo(None, self.tscp, self.on_combo_changed, i, k))        
                vbox.add(hbox)
                
            hobox.add(vbox)
            vbox.show()        
        
        self.container.add(hobox)
        hobox.show()
        
        self.container.add(self.entry('Amostra: ', self.on_entry_changed, 1, 'a'))
        self.container.add(self.entry('Pontuacao Maxima: ', self.on_entry_changed, 1, 'a'))
        self.container.add(self.entry('Pontuacao Minima: ', self.on_entry_changed, 1, 'a'))
        self.container.add(self.entry('Comprimento: ', self.on_entry_changed, 1, 'a'))
                
        button = gtk.Button()
        button.set_label('Procurar')
        button.connect("clicked", self.run)
        button.show()
        self.container.add(button)
        
        self.text = gtk.TextView()
        self.text.set_size_request(-1, 300)
        self.text.show()
        self.container.add(self.text)

    def on_motif_changed(self, combo, motif):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            if motif == 1:
                self.type1 = model[tree_iter][0]
            else:
                self.type2 = model[tree_iter][0]
        print("%s %s" % (self.type1, self.type2))
        
    def on_entry_changed(self, entry, motif, name):
        if motif == 1:
            self.motif1[name][0] = entry.get_text()
        else:
            self.motif2[name][0] = entry.get_text()
        print("%s %s" % (self.motif1, self.motif2))
        
    def on_combo_changed(self, combo, motif, name):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            if motif == 1:
                self.motif1[name][1] = model[tree_iter][0]
            else:
                self.motif2[name][1] = model[tree_iter][0]
        print("%s %s" % (self.motif1, self.motif2))
        
if __name__ == "__main__":
    base = Shortest()
    base.main()
