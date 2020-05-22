# JikkyoAlways
某動画サイト風にTwitterの検索結果が流れます.  
Youtubeで動画を再生しながら公式Live上映会推奨ハッシュタグのついたコメントが流れるので,楽しくなります.  
![live.gif](https://github.com/T3aHat/JikkyoAlways/blob/master/image/live.gif)  
LTなどで任意の推奨ハッシュタグを作成し,発表資料上に参加者のコメントをオーバーレイすると盛り上がる(荒れる)かもしれません.  
tkinterのtransparentcolorがかなり環境依存なため,Windows環境以外では動かない仕様になっています.  

# 推奨環境  
Win10-64bit  
(JIkkyoAlways.py編集はPython3.7)  
  

# 利用方法  
* https://developer.twitter.com から`consumer_key`,`consumer_secret`,`access_token`,`access_secret`を取得.  
* Windows環境でJikkyoAlways.exeをダウンロード.なお,信頼できないサイトからDLしたexeファイルを実行する際は"十分"注意してください.  
* Frameを開いた状態で`Ctrl+s`を押すとGUIによる各種変数の変更可能.  
* Frameを開いた状態で`Ctrl+t`を押すとツイート可能.  
  
# 機能及び変数紹介  
## `ctrl+s`  
![Change.png](https://github.com/T3aHat/JikkyoAlways/blob/master/image/Change.png)  
* `Search Word`  
Twitterで検索するワードを入力.  
* `withoutURL`  
URL(メディア,引用RT)を含むツイートを非表示にする.  
* `withoutRT`  
RTを検索から除外する.  
* `enable fav`  
流れるコメントを左クリックすると,いいねできるようにする.いいねでコメントが赤くハイライトされ,再度クリックすると,いいねを取り消す.  
* `enable RT`  
流れるコメントを右クリックすると,RTできるようになる.RTでコメントが緑にハイライトされ,再度クリックすると,RTを取り消す.  
いいねとRTをすると青にハイライトされる.  
* `realtime mode`  
リアルタイムモード.通常はsince_idにより検索に漏れがないように取得するので,該当ツイートが多い場合は実行中だんだんと遅延が生じます.  
`realtime mode`を指定すると,since_idを指定しないので,常に最新のn件のツイートを取得します.  
* `num of comments`  
一度に流れるコメント数.  
* `fontsize`  
フォントサイズ.`rec`とすると,画面に合うフォントサイズになる(仕様は`JikkyoAlways.py`を参照)  
* `maximum length of comment` 
コメントの長さ.n文字よりも長いツイートを流れないようにする.  
* `velocity`  
コメントの流れる速度.  
* `acceleration`  
コメントの加速度.長いコメントを速く流せる.  
コメントの速さ=`velocity+len(コメント)*acceleration`  
* `colour`  
コメントのフォントカラー. http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter にある`COLORS`で定義されたcolour name,もしくは`#`に続けて8bitでRGB指定できます.(ex.`red`は`#FF0000`に同じ)  
* Default  
各種変数をデフォルトに戻す.
* Apply  
変数の変更を適用.なお,`fontsize`に"hoge"など型エラーを起こすものを入れるとエラーになる.  
そこら辺のデバッグはしていないので,察して使用してください...  
  
## `Ctrl+t`  
![tweet.png](https://github.com/T3aHat/JikkyoAlways/blob/master/image/tweet.png)   
テキストボックスにツイートしたいテキストを入力して`Tweet`ボタンを押すと，API認証しているアカウントからツイートします.また，TweetDeck同様`ctrl+Enter`でもツイートできます．    
正常にツイートできるとテキストボックスの文字が消えます.失敗した場合はエラーコードがテキストボックスに表示されます.  
* `append Search Word`  
オンにすると,テキストボックス内のテキストの次に改行(`\n`)し,検索ワードを追加してツイートします．ハッシュタグを追っているときに便利.  
 

# 備忘録
色々書いてみました.  
[某動画サイト風にTwitter検索結果を流す【python】](https://qiita.com/teahat/items/1b0b5b51fbd7bb6e3d58)  
[tkinterで背景が透過するFrameを作る【Python】](https://qiita.com/teahat/items/050b572aad0d1686370b)  
[tweepyでURLを含むツイートを除外する【Python】](https://qiita.com/teahat/items/3417c91cc111e4f16ef3)  
[tkinterで作った透過Frameのpyinstallerでの挙動の違い【Python】](https://qiita.com/teahat/items/4aa4611fee3e9ea10bdc)  
[tkinterでLabelを動かす【Python】](https://qiita.com/teahat/items/a1e70621a62ab3a42ad8)  
  
  
# 田所あずさの純真Alwaysはいいぞ
https://www.youtube.com/watch?v=sBy76SY6zoQ
