# GH_Gcode  
 

### gcode Memo

```
E[vlaue] : 吐出量
F[vlaue] : 速度

G0 : 直線移動（最高速度）
G1 : 直線移動（設定速度）
G28 : リファレンス点に復帰
G49 : 
G54 - G59 : ワーク座標系を選択
G80 : 
G90 : アブソリュート指令、ワーク原点より算出
G91 : インクレメンタル指令、現在位置より算出

M3 : スピンドル回転開始（時計回り）
M4 : スピンドル回転開始（反時計回り）
M5 : スピンドル回転終了
M7 : クーラント1 オン
M8 : クーラント2 オン
M9 : クーラントオフ
M13 : 
M30 : プログラム終了
M55 : ヘッド1 下降
M56 : ヘッド1 上昇
M57 : ヘッド2 下降
M58 : ヘッド2 上昇

P[vlaue] : ツール番号
S[vlaue] : スピンドル回転速度（今回は材料の吐出）  
```


### F_Firmware Memo

```
() : コメントアウト
% : 開始と終了？、コメントアウト関係なく効く
```


---  

---  


# 材料の吐出について  

### 材料の出力  
```gcode
M3 S100 P1 // 材料の出力
```

### 材料の出力停止  

(1) 材料の停止（止めるだけ）  

```gcode
M3 S0 P1 // 順回転の回転停止
```

(2) 材料の停止（逆回し、ダマ防止）  

```gcode
M4 S100 P1 // 逆回転の回転始め
G4 X0.4 // 待機
M3 S0 // 順回転に設定し、回転はしない
```


---  

---  


# 実装メモ  

（200529 - Optimiser の実装より確認）  

ヘッドの起動・終了は、フィラメントを止めるとき、出し始めるときにそれぞれ必要っぽい。  

2つのエクストルーダで出力する際には、各レイヤーでエクストルーダの切り替えのたびに起動・終了を必ず挟む。  

# gcode の始まり  

```gcode
( == gcode start == )
% // 開始
G91 // 原点復帰
G28 Z0.000 // 原点復帰
G28 X0.000 Y0.000 // 原点復帰
G49 // 工具長補正（一応）
G80 // 固定サイクルキャンセル（一応）
G90 // （絶対）
G54 // ワーク座標系を選択
( == gcode start == )
```


### ヘッドの起動    

```gcode
( === START HEAD1 ===)
M55 // ヘッド1 下降
M3 S0 P1 // ツール1 順回転
M7 // クーラント1 オン
( === START HEAD1 ===)
```

```gcode
( === START HEAD2 ===)
M57 // ヘッド2 下降
M13 S0 P2
M8 // クーラント2 オン
( === START HEAD2 ===)
```

※ M13 怪しい


### ヘッドの終了  

```gcode
( === END HEAD1 ===)
M5 // スピンドル回転終了
M9 // クーラントオフ
M56 // ヘッド1 上昇
( === END HEAD1 ===)
```

```gcode
( === END HEAD2 ===)
M5 // スピンドル回転終了
M9 // クーラントオフ
M58 // ヘッド2 上昇
( === END HEAD2 ===)
```

### gcode の終わり  

```gcode
( == gcode end == )
S0 // 回転数を 0 に
M5 // スピンドル回転終了
G91 // 原点復帰
G28 Z0 // 原点復帰
G28 X0 Y0 // 原点復帰
M30 // プログラム終了
% // 終了
( == gcode end == )
```


---  

---  


### Ref  

- [ＮＣプログラム基礎知識](https://nc-program.s-projects.net/g-code.html)  

- [G-code (Rep Rap wiki)](https://reprap.org/wiki/G-code)  

