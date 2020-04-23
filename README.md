# GH_Gcode  
 

### gcode Memo

```
E[vlaue] : 吐出量
F[vlaue] : 速度
M3 : スピンドル回転開始（時計回り）
M4 : スピンドル回転開始（反時計回り）
M5 : スピンドル回転終了
M30 : プログラム終了
P[vlaue] : ツール番号
S[vlaue] : スピンドル回転速度（今回は材料の吐出）  
```


### F_Firmware Memo

```
() : コメントアウト
% : 開始と終了？、コメントアウト関係なく効く
```

材料の出力
```
M3 S100 P1 : 材料の出力
```

材料の出力停止
```
M3 S0 P1 : 材料の停止（止めるだけ）
M4 S100 P1 : 材料の停止（逆回し、ダマ防止）
```


---  


### Ref  

- [ＮＣプログラム基礎知識](https://nc-program.s-projects.net/g-code.html)  

- [G-code (Rep Rap wiki)](https://reprap.org/wiki/G-code)  

