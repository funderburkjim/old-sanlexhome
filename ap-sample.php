<!DOCTYPE html> <!-- html5 -->
<html>
<head>
<META charset="UTF-8">
<title>Cologne AP Sample</title>
<style>

#basictxt {
 position:absolute;
 top: 50px;
 width:400px;
 height:460px;
 overflow:auto;
 border: 1px solid black;
 padding-left: 5px;
 padding-bottom:5px;
}
#basicimg {
 position: absolute;
 top:50px;
 left:430px;
 width:500px;
 overflow:auto;
 /*padding-top:5px;*/
}
</style>

</head>
<body>
<div id="wrapper">
<H3 style="text-align:center">Sample for 
 <span style="text-decoration: underline;">
  Practical Sanskrit-English Dictionary, revised edition
 </span>
</H3>
<div id="basictxt">
<?php
include "ap-sample1.php";
echo $ap_akza;
?>
</div>
<div id="basicimg">
<!--
<img src="ap-sample.jpg" width="900" height="1200"/>
 -->
<img src="ap-sample-extract.png"/>
</div>
</div> <!-- wrapper-->
</body>
</html>
