#!/usr/bin/python


import pygtk
pygtk.require("2.0")
import gtk, gtk.glade, gobject
import gdata, gdata.media, gdata.geo, gdata.youtube, gdata.youtube.service
from xml.etree import ElementTree


class UpYou(object):

    def __init__(self):
    
        self.user = 'username'
        self.password = ''
        gladefile = 'UpYou.glade'
        windowname = "main_window" 
        self.mainTree = gtk.glade.XML(gladefile,windowname)
        self.fileTree = gtk.glade.XML(gladefile,'file_window')
        self.loginTree = gtk.glade.XML(gladefile, 'login_window')


        self.main_window = self.mainTree.get_widget(windowname)
        self.main_window.show()

        self.file_win = self.fileTree.get_widget('file_window')
        self.login_win = self.loginTree.get_widget('login_window');

        dic = { "on_pub_btn_toggled"  : self.rad_btn_group_change,
                "on_pick_btn_clicked" : self.show_file_chooser,
                "on_go_btn_clicked"   : self.do_upload,
                "on_fc_cancel_btn_clicked" : self.cancel_file,
                "on_fc_choose_btn_clicked" : self.choose_file,
                "on_login_menu_activate"   : self.open_login_window,
                "on_cancel_login_btn_clicked" : self.cancel_login,
                "on_get_login_btn_clicked" : self.do_login,
                "gtk_main_quit"       : gtk.main_quit,
              }
    
        self.mainTree.signal_autoconnect(dic)
        self.fileTree.signal_autoconnect(dic)
        self.loginTree.signal_autoconnect(dic)

        self.pub = True;
        self.video = {}
        self.doing_upload = False;
        self.mainTree.get_widget('category_drop').set_active(10)
    
        self.dev_key = 'AI39si5ttJIOXSj5zfTFFgntMnEWUZaqZxu_1Wqae22G35XmVR7ZkIrNN2aorkl7m5ZKdSdMYiZChO7ZzBZxkE6lNjb7kopQWA'
  


    def rad_btn_group_change(self, *args):
        self.pub = not self.pub
        print 'Public Video: ', self.pub

    def show_file_chooser(self, *args):
        self.file_win.show()

    def choose_file(self, *args):
        file_name = self.file_win.get_filename()
        self.mainTree.get_widget('name_txt').set_text(file_name)
        self.file_win.hide()

    def cancel_file(self, *args):
        print 'File Choser Cancel'
        self.file_win.hide()

    def open_login_window(self, *args):
        self.login_win.show()
        self.loginTree.get_widget('username_txt').set_text(self.user)
        self.loginTree.get_widget('password_txt').set_text(self.password)

    def do_login(self, *args):
        self.user = self.loginTree.get_widget('username_txt').get_text()
        self.password = self.loginTree.get_widget('password_txt').get_text()
        self.login_win.hide()

    def cancel_login(self, *args):
        self.user = 'username'
        self.password = ''
        self.loginTree.get_widget('username_txt').set_text(self.user)
        self.loginTree.get_widget('password_txt').set_text(self.password)
        self.login_win.hide()



    def __pulse(self):
        wid = self.mainTree.get_widget('prog_bar')
        wid.pulse()
        if self.doing_upload:
            gobject.timeout_add(50, self.__pulse)




        


    def do_upload(self, *args):
        self.__pulse()
        video_name = self.mainTree.get_widget('name_txt').get_text()
        cat_txt = self.mainTree.get_widget('category_drop').get_active_text()
        cat_txt = 'People'
        tags = self.mainTree.get_widget('tag_txt').get_text()
        desc = self.mainTree.get_widget('desc_txt').get_text()
        file_path = self.mainTree.get_widget('file_txt').get_text()
        print file_path
        cat = self.mainTree.get_widget('category_drop').get_active()

        print 'Uploading: ', video_name 
        print 'Category of :', cat_txt, ', #:', cat
        print 'Desc: ', desc
        print 'Tags: ', tags
        print 'File: ', file_path
        print 'Public: ', self.pub

        media_group = self.prepare_meta_data(video_name, desc, tags, cat_txt)
#        where = gdata.geo.Where()
#        where.set_location((37.0, -122.0))

        video_entry = gdata.youtube.YouTubeVideoEntry(media=media_group, geo=None)

        video_file = open(file_path);
        yt_service = gdata.youtube.service.YouTubeService()
        yt_service.email = self.user
        yt_service.password = self.password
        yt_service.source = 'LinVidUU'
        yt_service.developer_key = self.dev_key
        yt_service.client_id = 'LinVidUU'
        yt_service.ProgrammaticLogin()

        self.doing_upload = True
        new_entry = yt_service.InsertVideoEntry(video_entry, video_file)        
        self.doing_upload = False
        print type(new_entry)

    def prepare_meta_data(self, title, desc, tags, cat):
        title=gdata.media.Title(text=title)
        desc=gdata.media.Description(description_type='plain',
                                              text=desc)
        keywords=gdata.media.Keywords(text=tags)

        if not self.pub:
            private = gdata.media.Private()
        else:
            private = None
        
        category=gdata.media.Category(
              text=cat,
              scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
              label=cat)
        player=None
        
        media_group = gdata.media.Group(title, desc, keywords, category, player, private)
        return media_group

if __name__=='__main__':
    UpYou()
    gtk.main()
