# Marlin_Memo  


Marlin Website  

[https://marlinfw.org/](https://marlinfw.org/)  

gcode documents  

[https://marlinfw.org/meta/gcode/](https://marlinfw.org/meta/gcode/)  


```gcode
E[vlaue] ; 吐出量
F[vlaue] ; 速度

G0 ; 直線移動（最高速度）
G1 ; 直線移動（設定速度）
G4 ; 一時停止
G21 ; 単位をミリメートルに指定する
G90 ; 絶対的な位置を設定する
G91 ; 相対的な位置を設定する
G92 ; 位置を指定する(Set Position)

M82 ; E Absolute
M84 ; stepper off (???)
M104 ; Set Hotend Temperature
M106 ; Set Fan Speed
M107 ; Fan Off
M109 ; Wait for Hotend Temperature
M140 ; Set Bed Temperature
M190 ; Wait for Bed Temperature
M204 ; Set Starting Acceleration
M205 ; Set Advanced Settings
```


