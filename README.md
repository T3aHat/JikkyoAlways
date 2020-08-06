# JikkyoAlways

某動画サイト風に Twitter の検索結果が流れます.  
Youtube で動画を再生しながら公式 Live 上映会推奨ハッシュタグのついたコメントが流れるので,楽しくなります.  
![live.gif](https://github.com/T3aHat/JikkyoAlways/blob/master/image/live.gif)  
LT などで任意の推奨ハッシュタグを作成し,発表資料上に参加者のコメントをオーバーレイすると盛り上がる(荒れる)かもしれません.  
tkinter の transparentcolor がかなり環境依存なため,Windows 環境以外では動かない仕様になっています.

# 推奨環境

Windows10-64bit  
(JIkkyoAlways.py 編集は Python3.7)

# Download

releases:[here](https://github.com/T3aHat/JikkyoAlways/releases).  
latest exe file:[here](https://github.com/T3aHat/JikkyoAlways/raw/master/JikkyoAlways.exe).

# 利用方法

- https://developer.twitter.com から`consumer_key`,`consumer_secret`,`access_token`,`access_secret`を取得.
- Windows 環境で[JikkyoAlways.exe](https://github.com/T3aHat/JikkyoAlways/raw/master/JikkyoAlways.exe)をダウンロード.なお,信頼できないサイトから DL した exe ファイルを実行する際は"十分"注意してください.
- Frame を開いた状態で`Ctrl+s`を押すと GUI による各種変数の変更可能.
- Frame を開いた状態で`Ctrl+t`を押すとツイート可能.

# 機能及び変数紹介

## `ctrl+s`

![Change.png](https://github.com/T3aHat/JikkyoAlways/blob/master/image/Change.png)

- `Search Word`  
  Twitter で検索するワードを入力.
- `bold`  
  コメントを太字にする.
- `withoutURL`  
  URL(メディア,引用 RT)を含むツイートを非表示にする.
- `withoutRT`  
  RT を検索から除外する.
- `enable fav`  
  流れるコメントを左クリックすると,いいねできるようにする.いいねでコメントが赤くハイライトされ,再度クリックすると,いいねを取り消す.
- `enable RT`  
  流れるコメントを右クリックすると,RT できるようになる.RT でコメントが緑にハイライトされ,再度クリックすると,RT を取り消す.  
  いいねと RT をすると青にハイライトされる.
- `realtime mode`  
  リアルタイムモード.since_id を指定しないので,常に最新の n 件のツイートを取得.  
  通常(オフ時)は since_id により検索に漏れがないように取得するので,該当ツイートが多い場合は実行中だんだんと遅延が生じる.  
  有効化することでこれは解決できますが,表示すべき行数よりも新しいツイート数が少ない場合は,前に取得したツイートと同じツイートのコメントが流れてしまうので,トレンド入りしているようなワードでの検索時以外はオフを推奨.
- `remove Search word`  
  検索ワードをコメントに流れないようにする.ハッシュタグを非表示にすることを想定.
- `num of comments`  
  一度に流れるコメント数.
- `fontsize`  
  フォントサイズ.`rec`とすると,画面に合うフォントサイズになる(仕様は`JikkyoAlways.py`を参照)
- `maximum length of comment`
  コメントの長さ.n 文字よりも長いツイートを流れないようにする.
- `velocity`  
  コメントの流れる速度.
- `acceleration`  
  コメントの加速度.長いコメントを速く流せる.  
  コメントの速さ=`velocity+len(コメント)*acceleration`
- `colour`  
  コメントのフォントカラー. http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter にある`COLORS`で定義された colour name,もしくは`#`に続けて 8bit で RGB 指定可能.(ex.`red`は`#FF0000`に同じ)
* `transparency`  
  コメントの透明度．ウィンドウが見えなくならないよう透明度の下限を 0.1(10)とした．
- Default  
  各種変数をデフォルトに戻す.
- Apply  
  変数の変更を適用.なお,`fontsize`に"hoge"など型エラーを起こすものを入れるとエラーになる.  
  そこら辺のデバッグはしていないので,察して使用してください...

## `Ctrl+t`

![tweet.png](https://github.com/T3aHat/JikkyoAlways/blob/master/image/tweet.png)  
テキストボックスにツイートしたいテキストを入力して`Tweet`ボタンを押すと，API 認証しているアカウントからツイート.また，TweetDeck 同様`ctrl+Enter`でもツイートできます．  
正常にツイートできるとテキストボックスの文字が消えます.  
失敗した場合はエラーコードがテキストボックスに表示されます.

- `append Search Word`  
  オンにすると,テキストボックス内のテキストの末尾に改行(`\n`)と検索ワードを追加してツイート．ハッシュタグを追っているときに便利.

## `Ctrl+f`

フルスクリーンにする.フルスクリーン時は,フルスクリーンを解除する.

# 田所あずさの純真 Always はいいぞ

https://www.youtube.com/watch?v=sBy76SY6zoQ
