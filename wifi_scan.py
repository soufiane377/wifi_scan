#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import os
import commands
import re
import time
class Base:

    def popup(self, widget):
        label = gtk.Label("Nice label")
        dialog = gtk.Dialog("My dialog",
            None,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
            gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        dialog.vbox.pack_start(label)
        label.show()
        checkbox = gtk.CheckButton("Useless checkbox")
        dialog.action_area.pack_end(checkbox)
        checkbox.show()
        response = dialog.run()
        dialog.destroy()
        

    def destroy(self, widget, data=None):
        gtk.main_quit()
    def mystart(self, widget):
        ip2 = self.ip.get_text()
        mask2 = self.mask.get_text()
        stop=0
        tmp=0
        taymu=60*int(self.minutes.get_text())
        while(stop==0):
            ret = commands.getoutput("nmap -sn "+ip2+"/"+mask2)
            number = re.search('addresses ((.*?) hosts up)', ret).group(1)
            if number is None:
            	continue
            num = number[1:-9]
            real = int(num)-1
            if real==tmp:
                print "in loop "+str(real)+"connected devices"
            elif real > tmp:
                '''
                d = gtk.Dialog()
                label = gtk.Label(" "+str(real - tmp)+' devices connected')
                label.show()
                d.vbox.pack_start(label)
                d.run()
                time.sleep(10)
                d.destroy()
                '''
                ret1 = commands.getoutput("notify-send \" [+] "+str(real - tmp)+" devices connected."+" \"")
                tmp=real
                #print in terminal as a history
                print("+ 1")
            else:
                ret2 = commands.getoutput("notify-send \" [-] "+str(tmp - real)+" devices has disconnected."+" \"")
                tmp=real
                #print in terminal as a history
                print("- 1")
            time.sleep(taymu) #int(self.minutes.get_text())*60)
                
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_size_request(500,100)
        self.window.set_title("scan your wifi every x min")
        self.button1 = gtk.Button("Start")
        self.button1.connect("clicked",self.mystart)
        self.button1.set_size_request(50, 40)
        color = gtk.gdk.color_parse('#2ECC71')
        self.button1.modify_bg(gtk.STATE_NORMAL, color)
        self.button2 = gtk.Button("Stop")
        self.button2.connect("clicked",self.popup)
        self.button2.set_size_request(50, 40)        
        self.label1 = gtk.Label("ip:")
        self.label1.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFFFFF'))
        self.ip = gtk.Entry()
        self.ip.set_text("192.168.1.0")
        self.ip.set_size_request(100, 33)        
        self.label2 = gtk.Label("/ mask:")
        self.label3 = gtk.Label("   scan very ")
        self.label4 = gtk.Label("min")
        self.mask = gtk.Entry()
        self.mask.set_text("24")
        self.mask.set_size_request(33, 33)
        self.minutes = gtk.Entry()
        self.minutes.set_text("5")
        self.minutes.set_size_request(33, 33)
        self.box1 = gtk.HBox()
        self.box2 = gtk.HBox(False, 0)
        self.box2.set_size_request(400, 50)
        self.box3 = gtk.VBox()
        self.label2.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFFFFF'))
        self.label3.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFFFFF'))
        self.label4.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFFFFF'))
        self.box1.pack_start(self.label1)
        self.box1.pack_start(self.ip)
        self.box1.pack_start(self.label2)
        self.box1.pack_start(self.mask)
        self.box1.pack_start(self.label3)
        self.box1.pack_start(self.minutes)
        self.box1.pack_start(self.label4)
        self.box1.pack_end(self.button1)
        #self.box1.pack_end(self.button2)
        #self.box2.pack_start(self.button2)
        #self.box3.pack_start(self.box1) 
        #self.box3.pack_end(self.box2) 
        #self.box3.pack_start(self.button1)
  
        self.window.add(self.box1)
        color = gtk.gdk.color_parse('#22313F')
        self.window.modify_bg(gtk.STATE_NORMAL, color)
        self.window.show_all()
        self.window.connect("destroy",self.destroy)

    def main(self):
        gtk.main()

if __name__ == "__main__":
    base = Base()
    base.main()
