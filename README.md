# GH_Gcode  
 

### gcode Memo

```
E[vlaue] : 吐出量
F[vlaue] : 速度
G28 : リファレンス点に復帰
G49 : 
G54 - G59 : ワーク座標系を選択
G80 : 
G90 : アブソリュート指令、ワーク原点より算出
G91 : インクレメンタル指令、現在位置より算出
M3 : スピンドル回転開始（時計回り）
M4 : スピンドル回転開始（反時計回り）
M5 : スピンドル回転終了
M07 : クーラント２
M30 : プログラム終了
M55 : 位置１への工具の直線シフト
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

### gcode の始まり  

```gcode
( == gcode start == )
%
G91
G28 Z0.000
G28 X0.000 Y0.000
G49
G80
G90
G5
( == gcode start == )
```


### ヘッドの起動？  

```gcode
( === head1 start ===)
M55
M3 S0 P1
M7
( === head1 start ===)
```


### gcode の終わり  

```gcode
( == gcode end == )
S0
M5
G91
G28 Z0
G28 X0 Y0
M30
%
( == gcode end == )
```


---  

---  


### Ref  

- [ＮＣプログラム基礎知識](https://nc-program.s-projects.net/g-code.html)  

- [G-code (Rep Rap wiki)](https://reprap.org/wiki/G-code)  

