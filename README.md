# GH_Gcode  
 

ポリラインを、gcode に変換するライブラリ。  

一般的な 3D プリンタでは、Marlin 等の汎用のファームウェアにより gcode を解釈し、XYZE の可動軸が制御される。  


### Index  

- gh // Grasshopper Files   
  - dev // WIP。ghPython コンポーネントから、モジュールのコードを呼び出す。実装中のあれこれはこっちで。  
    - カンバス左上の Add Module に、ライブラリのパスを書き、 True にしてパスを追加する。初回はライノも含め再起動必要（？）  
  - release // 安定版。ghPython コンポーネントに全て書き込み済み。とりあえず動く。  


- gh_gcode // Python モジュール  
  - operate_attribute.py // 各点に重みづけ処理を行う。  
  - operate_curve.py // ジオメトリ処理系。  
  - operate_marlin_gcode.py // Marlin 向けの gcode の文字列処理他。  
  - transform.py // 数値計算系。  
  - util.py // ユーティリティ。  
  - viewer_marlin.py // gcode のビューワー関係。


### To Do  

- Atrribute Mode // 吐出量を細かな単位でいじるため  


### Attribute Mode  

各点のレベルで吐出量などをいじる機能を便宜的に Attribute Mode と呼んでいる。これには各点に重み付けを行う必要がある。  

重みづけを、ポリライン作成と同じ工程でハンドルしてもよいが、その場合は、データ構造等を深く考える必要があると思う。  

簡単なのはおそらく、ポリラインからポイントに変換した後に、ポイントを領域指定でまとめて重み付けを行う方法だと思う。この場合は、データ構造を考慮せずに、重みづけしたいポイントを Brep で囲んだら良い。  

デメリットとしては、重みづけしたいポイントをきちんと内包する Brep を作る必要があることくらいか。  

モコモコのテクスチャなど作りたい場合は、データ構造をハンドルしながら作る方がたぶん楽。  


### Marlin_Firmware Memo  

- [Marlin_Memo.md](https://github.com/naysok/GH_Gcode/blob/master/Marlin_Memo.md)  


### Ref  

- [ＮＣプログラム基礎知識](https://nc-program.s-projects.net/g-code.html)  

- [G-code (Rep Rap wiki)](https://reprap.org/wiki/G-code)  

- [Marlin - gcode documents](https://marlinfw.org/meta/gcode/)  

- [piac/list_to_tree.py, tree_to_list.py (GitHub Gist)](https://gist.github.com/piac/ef91ac83cb5ee92a1294)  