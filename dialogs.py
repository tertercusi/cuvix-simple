from ttkbootstrap import *
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame


class ProfileView(Toplevel):
    def __init__(self, master, profile_name):
        super().__init__(master)
        self.title(f'Profile - {profile_name}')
        self.rowconfigure(1, weight=1)
        self.geometry('650x400')

        self.profile_lbl = Label(self, text=profile_name, font=('', 16), justify=LEFT)
        self.profile_lbl.pack(side=TOP, fill=X)

        self.feed = ScrolledFrame(self)
        self.feed.pack(side=TOP, expand=True, fill=BOTH)

        self.fill_feed(profile_name)

    def fill_feed(self, profile_name):
        from models import Post
        for p in Post.select().where(Post.posted_by == profile_name).order_by(Post.created_at.desc()):
            post = PostFrame(self.feed, username=p.posted_by, date=p.created_at, content=p.content)
            post.pack(side=TOP, fill=X)


class PostFrame(Labelframe):
    def __init__(self, master, username, date, content):
        super().__init__(master, text=date, bootstyle=PRIMARY)

        self.username = username

        self.username_link = Button(self, text=username, bootstyle=(LINK, INFO), command=self.show_profile)
        self.username_link.pack(side=TOP, padx=3, pady=3)

        self.message = Label(self, text=content)
        self.message.pack(side=TOP, padx=3, pady=3, fill=X)

    def show_profile(self):
        ProfileView(self, self.username)


class NewPostDialog(Toplevel):
    def __init__(self, poster):
        super().__init__(title='New Post')
        self.poster = poster

        self.geometry('300x200')
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.lbl = Label(self, text='Create a post')
        self.lbl.grid(row=0, column=0)

        self.fld = Text(self)
        self.fld.grid(row=1, column=0, columnspan=2, sticky=(N, W, E, S))

        self.post_btn = Button(self, text='Post', command=self.commit)
        self.post_btn.grid(row=2, column=1, sticky=E)

    def commit(self):
        from models import Post
        post = Post(content=self.fld.get('1.0', END), created_at=datetime.now(), posted_by=self.poster)
        post.save()
        self.destroy()
