<!DOCTYPE html> <!-- html5 -->
<html>
<head>
<META charset="UTF-8">
<title>Cologne PD Sample</title>
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
 width:600px;
 overflow:auto;
 /*padding-top:5px;*/
}
</style>

</head>
<body>
<div id="wrapper">
<H3 style="text-align:center">Sample for 
 <span style="text-decoration: underline;">
  An Encyclopedic Dictionary of Sanskrit on Historical Principles
 </span>
</H3>
<div id="basictxt">
<?php
include "pd-sample1.php";
echo $pd_akza;
?>
</div>
<div id="basicimg">
<!--
<img src="ap-sample.jpg" width="900" height="1200"/>
 -->
<img src="pd-sample-extract.png"/>
</div>
</div> <!-- wrapper-->
</body>
</html>
