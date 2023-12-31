from ttkbootstrap import *
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs.dialogs import Messagebox

from encryption import encrypt, decrypt

class ProfileView(Toplevel):
    def __init__(self, master, profile_name):
        super().__init__(master, topmost=True)
        self.title(f'Profile - {profile_name}')
        self.rowconfigure(1, weight=1)
        self.geometry('650x400')

        self.profile_lbl = Label(self, text=profile_name, font=('', 16), justify=LEFT)
        self.profile_lbl.pack(side=TOP, fill=X, padx=(5, 20))

        from models import User
        user = User.get(User.username == profile_name)
        date_joined = Label(self, text=f'Joined at {user.created_at}', font=('', 10), foreground='gray', justify=LEFT)
        date_joined.pack(side=TOP, fill=X, padx=(5,0))

        self.feed = ScrolledFrame(self)
        self.feed.pack(side=TOP, expand=True, fill=BOTH)

        self.fill_feed(profile_name)

    def fill_feed(self, profile_name):
        from models import Post
        for p in Post.select().where(Post.posted_by == profile_name).order_by(Post.created_at.desc()):
            post = PostFrame(self.feed, username=p.posted_by, date=p.created_at, content=p.content, post_id=str(p))
            post.pack(side=TOP, fill=X, padx=(5, 20))


class PostFrame(Labelframe):
    def __init__(self, master, username, date, content, post_id=None):
        super().__init__(master, bootstyle=PRIMARY, text='')

        self.username = username
        self.post_id = post_id

        head_frm = Frame(self)

        username_link = Button(head_frm, text=f'@{username}', bootstyle=(LINK, INFO), command=self.show_profile)
        username_link.pack(side=LEFT, anchor=W)

        timestamp = Label(head_frm, text=f'at {date}', foreground='gray')
        timestamp.pack(side=LEFT, anchor=W, padx=(0,10))

        edit_btn = Button(head_frm, text='Edit', bootstyle=(LINK, INFO), command=self.edit)
        edit_btn.pack(side=LEFT, anchor=W, padx=(0,10))

        delete_btn = Button(head_frm, text='Delete', bootstyle=(LINK, DANGER), command=self.delete)
        delete_btn.pack(side=LEFT, anchor=W, padx=(0,10))

        head_frm.pack(side=TOP, anchor=W)

        self.content = StringVar(value=content)
        message = Label(self, textvariable=self.content)
        message.pack(side=BOTTOM, padx=10, pady=3, fill=X)

    def show_profile(self):
        ProfileView(self, self.username)

    def delete(self):
        from models import Post
        Post.delete_by_id(self.post_id)
        self.destroy()

    def edit(self):
        d = EditPostDialog(self.post_id)
        d.bind('<Destroy>', self.update, add=True)

    def update(self, *args):
        from models import Post
        post = Post.get_by_id(self.post_id)
        self.content.set(post.content)


class NewPostDialog(Toplevel):
    def __init__(self, poster):
        super().__init__(title='New Post', topmost=True)
        self.poster = poster

        self.geometry('300x200')
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.lbl = Label(self, text='Create a post')
        self.lbl.grid(row=0, column=0, sticky=W)

        self.fld = Text(self)
        self.fld.grid(row=1, column=0, columnspan=2, sticky=(N, W, E, S))

        self.post_btn = Button(self, text='Post', command=self.commit)
        self.post_btn.grid(row=2, column=1, sticky=E)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def commit(self):
        from models import Post
        post = Post(content=self.fld.get('1.0', END), created_at=datetime.now(), posted_by=self.poster)
        post.save()
        self.destroy()

class EditPostDialog(Toplevel):
    def __init__(self, post_id):
        super().__init__(title='Edit Post', topmost=True)
        
        from models import Post
        self.post = Post.select().where(Post.id == post_id).get()

        self.geometry('300x200')
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.lbl = Label(self, text='Edit post:')
        self.lbl.grid(row=0, column=0, sticky=W)

        self.fld = Text(self)
        self.fld.grid(row=1, column=0, columnspan=2, sticky=(N, W, E, S))
        self.fld.insert('1.0', self.post.content)

        self.post_btn = Button(self, text='Save', command=self.commit)
        self.post_btn.grid(row=2, column=1, sticky=E)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def commit(self):
        self.post.content = self.fld.get('1.0', END)
        self.post.save()
        self.destroy()

class AddUserDialog(Toplevel):
    def __init__(self):
        super().__init__(topmost=True)
        self.title('Sign Up')
        self.resizable(width=False, height=False)

        self.usr_lbl = Label(self, text='Username')
        self.usr_lbl.grid(row=0, column=0)

        self.username = StringVar()
        self.usr_fld = Entry(self, textvariable=self.username)
        self.usr_fld.grid(row=0, column=1)

        self.pass_lbl = Label(self, text='Password')
        self.pass_lbl.grid(row=1, column=0)

        self.password = StringVar()
        self.pass_fld = Entry(self, textvariable=self.password, show='*')
        self.pass_fld.grid(row=1, column=1)

        self.signup_btn = Button(self, text='Sign Up', command=self.signup)
        self.signup_btn.grid(row=2, column=0, columnspan=2, sticky=EW)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def signup(self):
        from models import User
        try:
            raw_password = self.password.get()
            user = User(username=self.username.get(), password=encrypt(raw_password), created_at=datetime.now())
            user.save(force_insert=True)
            self.destroy()
        except:
            Messagebox.show_error('User already exists!')

class SwitchUserDialog(Toplevel):
    def __init__(self, user_var):
        super().__init__(topmost=True)
        self.title('Login')
        self.resizable(width=False,height=False)
        
        self.user_var = user_var

        self.user_fld = StringVar()
        user_lbl = Label(self, text='Username:')
        user_lbl.grid(row=0, column=0)
        
        user_ent = Entry(self, textvariable=self.user_fld)
        user_ent.grid(row=0, column=1)

        self.pass_fld = StringVar()
        pass_lbl = Label(self, text='Password:')
        pass_lbl.grid(row=1, column=0)
        
        pass_ent = Entry(self, textvariable=self.pass_fld, show='*')
        pass_ent.grid(row=1, column=1)

        login_btn = Button(self, text='Login', command=self.login)
        login_btn.grid(row=2, column=0, columnspan=2, sticky=EW)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def login(self):
        username = self.user_fld.get()
        password = self.pass_fld.get()

        from models import User
        
        try:
            user = User.get(User.username == username)
            if not decrypt(user.password) == password:
                raise Exception
            else:
                self.user_var.set(username)
                self.destroy()
        except:
            Messagebox.show_error('Wrong credentials!')


class SearchProfileDialog(Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Search Profile')

        Label(self, text='Profile:').pack(side=LEFT)

        self.profile = StringVar()
        Entry(self, textvariable=self.profile).pack(side=LEFT)

        Button(self, text='Search', bootstyle=PRIMARY, command=self.search).pack(side=LEFT)

        for child in self.winfo_children():
            child.pack_configure(padx=5, pady=5)
        
    def search(self):
        from models import User

        username = self.profile.get()
        try:
            User.get(User.username == username)
            ProfileView(self, profile_name=username)
            self.destroy()
        except:
            Messagebox.show_error('User not found.')

    
