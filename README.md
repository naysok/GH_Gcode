# GH_Gcode  
 

ポリラインを、gcode(S) に変換するライブラリ。  

汎用のファームウェアでは、XYZ と同じ様に、材料の吐出はモータの回転量（E）で制御されるが、EB の機械は、スピンドルの回転数（S）で制御する。  


### index  

- gh // Grasshopper Files   
  - dev // WIP。ghPython コンポーネントから、モジュールのコードを呼び出す。実装中のあれこれはこっちで。  
  - release // 安定版。ghPython コンポーネントに全て書き込み済み。とりあえず動く。  


- gh_gcode // Python モジュール  
  - operate_attribute.py // 各点に重みづけ処理を行う。  
  - operate_big_gcode.py // gcode(S) の文字列処理他。  
  - operate_curve.py // ジオメトリ処理系。  
  - operate_marlin_gcode.py // Marlin 向けの gcode(E) の文字列処理他。  
  - transform.py // 数値計算系。  
  - util.py // ユーティリティ。  
  - util_eb.py // EB 向けのカスタムユーティリティ（継承）。  
  - viewer_big.py // gcode(S) のビューワー。  
  - viewer_marlin.py // gcode(E) のビューワー。汎用 gcode 向け。  


### To Do  

- Atrribute Mode // 吐出量を細かな単位でいじるため  


### Attribute Mode  

各点のレベルで吐出量などをいじる機能を便宜的に Attribute Mode と呼んでいる。これには各点に重み付けを行う必要がある。  

重みづけを、ポリライン作成と同じ工程でハンドルしてもよいが、その場合は、データ構造等を深く考える必要があると思う。  

簡単なのはおそらく、ポリラインからポイントに変換した後に、ポイントを領域指定でまとめて重み付けを行う方法だと思う。この場合は、データ構造を考慮せずに、重みづけしたいポイントを Brep で囲んだら良い。  

デメリットとしては、重みづけしたいポイントをきちんと内包する Brep を作る必要があることくらいか。  

モコモコのテクスチャなど作りたい場合は、データ構造をハンドルしながら作る方がたぶん楽。  


### Marlin_Firmware  

- [Marlin_Memo.md](https://github.com/naysok/GH_Gcode/blob/master/Marlin_Memo.md)  


### F社_Firmware  

- [F_Memo.md](https://github.com/naysok/GH_Gcode/blob/master/F_Memo.md)  
  


### Ref  

- [ＮＣプログラム基礎知識](https://nc-program.s-projects.net/g-code.html)  

- [G-code (Rep Rap wiki)](https://reprap.org/wiki/G-code)  

- [Marlin - gcode documents](https://marlinfw.org/meta/gcode/)
