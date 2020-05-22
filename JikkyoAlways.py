from tkinter import ttk
import tkinter
import tweepy
import configparser
from ctypes import windll
import sys


def move(i):
    global nowdatalist

    def x():
        labels[i].place(x=ww+lc[i], y=fontsize*(2*i-0.5))
        lc[i] -= v+len(nowdatalist[i].text)*acc
        if(ww+lc[i] < -labels[i].winfo_reqwidth()):  # 左端行った
            lefted[i] = True
        labels[i].after(1, move(i))
    return x


def reAuth(api):
    global results
    while(True):
        print("TwitterAPI could not authenticate your account.\nGet your ConsumerKey,ConsumerSecret,AccessToken,AccessTokenSecret!")
        print("Detail:https://developer.twitter.com/en/apply-for-access\n")
        CK = input("input your ConsumerKey:")
        CS = input("input your ConsumerSecret:")
        AT = input("input your AccessToken:")
        AS = input("input your AccessTokenSecret:")
        config = configparser.ConfigParser()
        section = "TwitterAPI"
        config.add_section(section)
        config.set(section, "CK", CK)
        config.set(section, "CS", CS)
        config.set(section, "AT", AT)
        config.set(section, "AS", AS)
        auth = tweepy.OAuthHandler(CK, CS)
        auth.set_access_token(AT, AS)
        api = tweepy.API(auth)
        try:
            results = api.search(q=word, count=num_comment)
            print("Authentication　Successful!")
            with open("config.ini", "w")as f:
                config.write(f)
            print("Wrote your CK,CS,AT,AS to config.ini")
            select = input("Restart to erase prompt?(y/n):")
            if select == "y":
                sys.exit()
            else:
                print("Setting finished!")
                break
        except Exception as e:
            print(e)
            print(CK)
            print(CS)
            print(AT)
            print(AS)
            print("Authentication failed…Please retry.")
    return api


def longtxt(r):
    if len(r.text) > max_length:
        return True
    else:
        return False


def exURL(r):
    if withoutURL and (r.entities["urls"] != [] or ("media" or "is_quote_status") in r.entities):
        return False  # URLが含まれる
    else:
        return True


# favでred,RTでgreen,両方でblue.
def lclick(i):
    if(enable_fav):
        global nowdatalist

        def y(self):
            labels[i].place_forget()
            if (str(labels[i].cget("background")) == "red"):
                print("unlike:"+str(nowdatalist[i].text))
                api.destroy_favorite(nowdatalist[i].id)
                labels[i] = (ttk.Label(master=root, text=nowdatalist[i].text, font=(
                    "メイリオ", fontsize), foreground=colour, background="grey"))
            elif (str(labels[i].cget("background")) == "blue"):
                print("unlike:"+str(nowdatalist[i].text))
                api.destroy_favorite(nowdatalist[i].id)
                labels[i] = (ttk.Label(master=root, text=nowdatalist[i].text, font=(
                    "メイリオ", fontsize), foreground=colour, background="green"))
            elif (str(labels[i].cget("background")) == "green"):
                print("like:"+str(nowdatalist[i].text))
                api.create_favorite(nowdatalist[i].id)
                labels[i] = (ttk.Label(master=root, text=nowdatalist[i].text, font=(
                    "メイリオ", fontsize), foreground=colour, background="blue"))
            else:
                print("like:"+str(nowdatalist[i].text)+str(nowdatalist[i].id))
                api.create_favorite(nowdatalist[i].id)
                labels[i] = (ttk.Label(master=root, text=nowdatalist[i].text, font=(
                    "メイリオ", fontsize), foreground=colour, background="red"))
            labels[i].bind("<1>", lclick(i))
            labels[i].bind("<3>", rclick(i))
        return y


def rclick(i):
    if(enable_rt):
        global nowdatalist

        def z(self):
            labels[i].place_forget()
            if (str(labels[i].cget("background")) == "green"):
                print("unRT:"+str(nowdatalist[i].text))
                api.unretweet(nowdatalist[i].id)
                labels[i] = (ttk.Label(master=root, text=nowdatalist[i].text, font=(
                    "メイリオ", fontsize), foreground=colour, background="grey"))
            elif (str(labels[i].cget("background")) == "blue"):
                print("unRT:"+str(nowdatalist[i].text))
                api.unretweet(nowdatalist[i].id)
                labels[i] = (ttk.Label(master=root, text=nowdatalist[i].text, font=(
                    "メイリオ", fontsize), foreground=colour, background="red"))
            elif (str(labels[i].cget("background")) == "red"):
                print("RT:"+str(nowdatalist[i].text))
                api.retweet(nowdatalist[i].id)
                labels[i] = (ttk.Label(master=root, text=nowdatalist[i].text, font=(
                    "メイリオ", fontsize), foreground=colour, background="blue"))
            else:
                print(labels[i].cget("background"))
                print("RT:"+str(nowdatalist[i].text))
                api.retweet(nowdatalist[i].id)
                labels[i] = (ttk.Label(master=root, text=nowdatalist[i].text, font=(
                    "メイリオ", fontsize), foreground=colour, background="green"))
            labels[i].bind("<1>", lclick(i))
            labels[i].bind("<3>", rclick(i))
        return z


def get_newcomment():
    global j
    global results
    global latestid
    global realtime
    j = 0
    if(lefted.count(True) > 0):  # 流れ切ったコメがある
        if (len(results) > 0):  # resultsがあればlatestid更新.ない場合は前のまま
            latestid = results[0].id
        if(realtime):
            results = api.search(
                q=word, count=lefted.count(True), since_id=latestid)
        else:
            results = api.search(q=word, count=lefted.count(True))
        labels[0].after(5050, get_newcomment)
    else:  # 流れ切ったのがないからnmsごとにleftedがあるか見直す
        labels[0].after(100, get_newcomment)


def update_comment():  # resultsを元にコメを書き換え
    global j
    global results
    global nowdatalist
    global colour
    k = 0
    for i in range(num_comment):
        if(k != 0 and k % 2 == 0):
            k += 1
            break
        if(lefted[i] == True):  # went left.So update comment
            while(j < len(results)):
                if (exURL(results[j]) and (not longtxt(results[j]))):
                    nowdatalist[i].text = results[j].text.replace("\n", " ")
                    nowdatalist[i].id = results[j].id
                    labels[i].place_forget()
                    try:  # colourに例外が来た時のため
                        labels[i] = (ttk.Label(master=root, text=nowdatalist[i].text, font=(
                            "メイリオ", fontsize), foreground=colour, background="grey"))
                    except Exception as e:
                        print(e)
                        colour = "white"  # 強制初期化
                        labels[i] = (ttk.Label(master=root, text=nowdatalist[i].text, font=(
                            "メイリオ", fontsize), foreground=colour, background="grey"))
                    labels[i].bind("<1>", lclick(i))
                    labels[i].bind("<3>", rclick(i))
                    lc[i] = 0
                    lefted[i] = False
                    j += 1
                    k += 1
                    break
                else:
                    j += 1
    labels[0].after(1000, update_comment)


def Change_word(f):
    def x(self):
        subf = tkinter.Tk()
        subf.wm_attributes("-topmost", True)
        subf.geometry("300x500")
        subf.title("Settings")

        label1 = tkinter.Label(subf, text="Search Word")
        label1.pack()
        txt1 = tkinter.Entry(subf, width=30)
        txt1.insert(tkinter.END, word.replace("-filter:retweets", ""))
        txt1.pack()

        bl1 = tkinter.BooleanVar(subf)
        bl1.set(withoutURL)
        CheckBox1 = tkinter.Checkbutton(subf, text="withoutURL", variable=bl1)
        CheckBox1.pack()

        bl2 = tkinter.BooleanVar(subf)
        bl2.set(withoutRT)
        CheckBox2 = tkinter.Checkbutton(subf, text="withoutRT", variable=bl2)
        CheckBox2.pack()

        bl3 = tkinter.BooleanVar(subf)
        bl3.set(enable_fav)
        CheckBox3 = tkinter.Checkbutton(subf, text="enable fav", variable=bl3)
        CheckBox3.pack()

        bl4 = tkinter.BooleanVar(subf)
        bl4.set(enable_rt)
        CheckBox4 = tkinter.Checkbutton(subf, text="enable RT", variable=bl4)
        CheckBox4.pack()

        bl5 = tkinter.BooleanVar(subf)
        bl5.set(realtime)
        CheckBox5 = tkinter.Checkbutton(
            subf, text="realtime mode", variable=bl5)
        CheckBox5.pack()

        label2 = tkinter.Label(subf, text="num of comments(reccomend:10~25)")
        label2.pack()
        txt2 = tkinter.Entry(subf, width=30)
        txt2.insert(tkinter.END, num_comment)
        txt2.pack()

        label3 = tkinter.Label(subf, text="fontsize(reccomend:rec)")
        label3.pack()
        txt3 = tkinter.Entry(subf, width=30)
        txt3.insert(tkinter.END, fontsize)
        txt3.pack()

        label4 = tkinter.Label(
            subf, text="maximum length of comment(reccomend:100)")
        label4.pack()
        txt4 = tkinter.Entry(subf, width=30)
        txt4.insert(tkinter.END, max_length)
        txt4.pack()

        label5 = tkinter.Label(subf, text="velocity(reccomend:1)")
        label5.pack()
        txt5 = tkinter.Entry(subf, width=30)
        txt5.insert(tkinter.END, v)
        txt5.pack()

        label6 = tkinter.Label(subf, text="acceleration(reccomend:0.05)")
        label6.pack()
        txt6 = tkinter.Entry(subf, width=30)
        txt6.insert(tkinter.END, acc)
        txt6.pack()

        label7 = tkinter.Label(
            subf, text="colour(colour name(pink)or 8 bit RGB(#FFC0CB))")
        label7.pack()
        txt7 = tkinter.Entry(subf, width=30)
        txt7.insert(tkinter.END, colour)
        txt7.pack()

        button = tkinter.Button(subf, text="Apply")
        button.pack(side="right")
        button.bind("<1>", lambda word: get_word(f, txt1, bl1, bl2,
                                                 bl3, bl4, bl5, txt2, txt3, txt4, txt5, txt6, txt7))

        button = tkinter.Button(subf, text="Default")
        button.pack(side="left")
        button.bind("<1>", lambda word: get_default(f, txt1, bl1, bl2,
                                                    bl3, bl4, bl5, txt2, txt3, txt4, txt5, txt6, txt7))

        subf.mainloop()
    return x


def tweetframe(word):
    def x(self):
        twf = tkinter.Tk()
        twf.wm_attributes("-topmost", True)
        twf.title("Tweet from @"+me)

        twtxt1 = tkinter.Text(twf, width=40, height=10)
        twtxt1.pack()

        twbl1 = tkinter.BooleanVar(twf)
        twbl1.set(True)
        twf.bind("<Control-Return>", lambda word: tweet(twtxt1, twbl1))
        twCheckBox1 = tkinter.Checkbutton(
            twf, text="append "+word.replace("-filter:retweets", ""), variable=twbl1)
        twCheckBox1.pack(side='left')

        twbtn = tkinter.Button(twf, text="Tweet", bg='#1DA1F2')
        twbtn.pack(side='right')
        twbtn.bind("<1>", lambda word: tweet(twtxt1, twbl1))

        twf.mainloop()
    return x


def tweet(twtxt1, twbl1):
    text = twtxt1.get('1.0', 'end -1c')
    if(twbl1.get()):
        text += "\n"+word.replace("-filter:retweets", "")
    try:
        api.update_status(text)
        twtxt1.delete('1.0', 'end')
        print('Tweet successful!'+str(text))
    except Exception as e:
        twtxt1.delete('1.0', 'end')
        twtxt1.insert(tkinter.END, 'Failed to tweet...\n'+str(e))
        print(e)


def get_default(f, txt1, bl1, bl2, bl3, bl4, bl5, txt2, txt3, txt4, txt5, txt6, txt7):

    txt1.delete(0, tkinter.END)
    txt1.insert(tkinter.END, "Change here")
    bl1.set(True)
    bl2.set(True)
    bl3.set(False)
    bl4.set(False)
    bl5.set(False)
    txt2.delete(0, tkinter.END)
    txt2.insert(tkinter.END, "25")
    txt3.delete(0, tkinter.END)
    txt3.insert(tkinter.END, int((400*f.winfo_height()/1080)/num_comment))
    txt4.delete(0, tkinter.END)
    txt4.insert(tkinter.END, 100)
    txt5.delete(0, tkinter.END)
    txt5.insert(tkinter.END, 1)
    txt6.delete(0, tkinter.END)
    txt6.insert(tkinter.END, 0.05)
    txt7.delete(0, tkinter.END)
    txt7.insert(tkinter.END, "white")


def get_word(f, txt1, bl1, bl2, bl3, bl4, bl5, txt2, txt3, txt4, txt5, txt6, txt7):
    global word, withoutURL, withoutRT, enable_fav, enable_rt, realtime, num_comment, fontsize, max_length, v, acc, colour

    withoutURL = bl1.get()
    withoutRT = bl2.get()
    word = txt1.get()
    if withoutRT:
        word += " -filter:retweets"
    enable_fav = bl3.get()
    enable_rt = bl4.get()
    realtime = bl5.get()
    num_comment = int(txt2.get())
    if(txt3.get() == "rec"):
        i = 1
        while (True):
            labeltemp = ttk.Label(master=root, text='Changed settings!', font=(
                "メイリオ", i), foreground='red', background='blue')
            labeltemp.place(x=0, y=0)
            reqheightemp = labeltemp.winfo_reqheight()
            labeltemp.place_forget()
            if(reqheightemp*num_comment > f.winfo_height()):
                fontsize = i
                break
            else:
                i += 1
    else:
        fontsize = int(txt3.get())
    max_length = int(txt4.get())
    v = int(txt5.get())
    acc = float(txt6.get())

    if(str(txt7.get()) == "grey"):
        colour = str("light grey")
    else:
        colour = str(txt7.get())

    print("word:"+str(word))
    print("withoutURL:"+str(withoutURL))
    print("wiothoutRT:"+str(withoutRT))
    print("enable_fav:"+str(enable_fav))
    print("enable_rt:"+str(enable_rt))
    print("realtime mode:"+str(realtime))
    print("num_comment:"+str(num_comment))
    print("fontsize:"+str(fontsize))
    print("max_length:"+str(max_length))
    print("v:"+str(v))
    print("acc:"+str(acc))
    print("colour="+colour)


if __name__ == '__main__':
    num_comment = 25
    fontsize = int(400/num_comment)
    v = 1
    acc = 0.05
    withoutURL = True
    withoutRT = True
    max_length = 100
    enable_fav = False
    enable_rt = False
    realtime = False
    colour = "white"

    lefted = []
    config = configparser.ConfigParser()
    config.read("config.ini")
    section = "TwitterAPI"
    try:
        CK = config.get(section, "ck")
        CS = config.get(section, "cs")
        AT = config.get(section, "at")
        AS = config.get(section, "as")
    except:
        CK, CS, AT, AS = "", "", "", ""

    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    api = tweepy.API(auth)
    me = api.me().screen_name
    word = input("検索ワード:")
    if withoutRT:
        word += " -filter:retweets"
    print(word)

    try:
        results = api.search(q=word, count=num_comment)
        latestid = results[0].id
        print("Authentication　Successful!")
    except Exception as e:
        print(e)
        api = reAuth(api)

    ww = windll.user32.GetSystemMetrics(0)
    wh = windll.user32.GetSystemMetrics(1)
    root = tkinter.Tk()
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-transparentcolor", "grey")
    # root.wm_attributes("-fullscreen",True)#閉じられなくなるから処理が必要
    ttk.Style().configure("TP.TFrame", background="grey")
    root.title("JikkyoAlways")
    f = ttk.Frame(master=root, style="TP.TFrame", width=ww, height=wh)
    root.bind("<Control-Key-s>", Change_word(f))
    root.bind("<Control-Key-t>", tweetframe(word))
    f.pack()

    j = 0
    lc = []
    nowdatalist = results
    for i in range(num_comment):
        lc.append(0)
        lefted.append(False)

    labels = []
    for i in range(num_comment):
        if(i < len(nowdatalist)):
            if exURL(nowdatalist[i]) and (not longtxt(nowdatalist[i])):
                nowdatalist[i].text.replace("\n", "")
            else:
                nowdatalist[i].text = ""
                lefted[i] = True
            labels.append(ttk.Label(master=root, text=nowdatalist[i].text.replace(
                "\n", " "), font=("メイリオ", fontsize), foreground=colour, background="grey"))
        else:
            nowdatalist.append(nowdatalist[0])  # padding(改良の余地あり)
            nowdatalist[-1].text = ""  # padding
            labels.append(ttk.Label(master=root, text=nowdatalist[i].text, font=(
                "メイリオ", fontsize), foreground=colour, background="grey"))

    for i in range(num_comment):
        labels[i].bind("<1>", lclick(i))
        labels[i].bind("<3>", rclick(i))
        labels[i].after(1, move(i))

    get_newcomment()
    update_comment()

    root.mainloop()
