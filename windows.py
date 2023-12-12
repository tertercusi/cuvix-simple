from ttkbootstrap import *
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs.dialogs import Messagebox

class NewsFeed(Window):
    def __init__(self):
        super().__init__(title='Cuvix', themename='superhero')
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.geometry('850x400')

        self.current_user = StringVar(value=None)
        self.status = StringVar(value='Ready.')

        self.new_post_btn = Button(self)
        self.new_post_btn.config(text='New Post...', command=self.new_post)
        self.new_post_btn.grid(column=0, row=0, sticky=(N, W, E), pady=(1, 20))

        self.show_profile_btn = Button(self)
        self.show_profile_btn.config(text='Show Profile...', bootstyle=SECONDARY, command=self.show_profile)
        self.show_profile_btn.grid(column=0, row=1, sticky=(N, W, E))

        self.add_user_btn = Button(self)
        self.add_user_btn.config(text='Add User...', bootstyle=SECONDARY, command=self.add_new_user)
        self.add_user_btn.grid(column=0, row=2, sticky=(N, W, E))

        self.refresh_btn = Button(self)
        self.refresh_btn.config(text='Refresh Posts', bootstyle=SECONDARY, command=self.refresh_feed)
        self.refresh_btn.grid(column=0, row=3, sticky=(N, W, E))

        self.current_usr_btn = Button(self)
        self.current_usr_btn.config(textvariable=self.current_user, bootstyle=(LINK,PRIMARY), command=self.show_own_profile)
        self.current_usr_btn.grid(column=0, row=4, sticky=EW)

        self.switch_user_btn = Button(self)
        self.switch_user_btn.config(text='Switch User...', bootstyle=(LINK), command=self.switch_usr)
        self.switch_user_btn.grid(column=1, row=4, sticky=W)

        self.feed = ScrolledFrame(self)
        self.feed.grid(column=1, row=0, rowspan=4, columnspan=2, padx=(10, 0), pady=1, sticky=(N, W, E, S))

        self.switch_usr()
        self.refresh_feed()

    def refresh_feed(self, *args):
        for child in self.feed.winfo_children():
            child.destroy()

        from models import Post
        from dialogs import PostFrame
        for post in Post.select().order_by(Post.created_at.desc()):
            frame = PostFrame(self.feed, username=post.posted_by, content=post.content, date=post.created_at, post_id=str(post))
            frame.pack(side=TOP, fill=X, padx=(5,20))

    def new_post(self):
        if not self.current_user.get():
            Messagebox.show_error('Must be logged in.')
            return

        from dialogs import NewPostDialog
        d = NewPostDialog(self.current_user.get())
        d.bind('<Destroy>', self.refresh_feed, add=True)

    def add_new_user(self):
        from dialogs import AddUserDialog
        d = AddUserDialog()

    def switch_usr(self):
        from dialogs import SwitchUserDialog
        d = SwitchUserDialog(self.current_user)

    def show_profile(self):
        from dialogs import SearchProfileDialog
        SearchProfileDialog()

    def show_own_profile(self):
        from dialogs import ProfileView
        ProfileView(self, self.current_user.get())


if __name__ == '__main__':
    NewsFeed().mainloop()
