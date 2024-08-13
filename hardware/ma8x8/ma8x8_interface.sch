<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="6.6.0">
<drawing>
<settings>
<setting alwaysvectorfont="no"/>
<setting verticaltext="up"/>
</settings>
<grid distance="0.1" unitdist="inch" unit="inch" style="lines" multiple="1" display="no" altdistance="0.01" altunitdist="inch" altunit="inch"/>
<layers>
<layer number="1" name="Top" color="4" fill="1" visible="no" active="no"/>
<layer number="2" name="Route2" color="1" fill="3" visible="no" active="no"/>
<layer number="3" name="Route3" color="4" fill="3" visible="no" active="no"/>
<layer number="4" name="Route4" color="1" fill="4" visible="no" active="no"/>
<layer number="5" name="Route5" color="4" fill="4" visible="no" active="no"/>
<layer number="6" name="Route6" color="1" fill="8" visible="no" active="no"/>
<layer number="7" name="Route7" color="4" fill="8" visible="no" active="no"/>
<layer number="8" name="Route8" color="1" fill="2" visible="no" active="no"/>
<layer number="9" name="Route9" color="4" fill="2" visible="no" active="no"/>
<layer number="10" name="Route10" color="1" fill="7" visible="no" active="no"/>
<layer number="11" name="Route11" color="4" fill="7" visible="no" active="no"/>
<layer number="12" name="Route12" color="1" fill="5" visible="no" active="no"/>
<layer number="13" name="Route13" color="4" fill="5" visible="no" active="no"/>
<layer number="14" name="Route14" color="1" fill="6" visible="no" active="no"/>
<layer number="15" name="Route15" color="4" fill="6" visible="no" active="no"/>
<layer number="16" name="Bottom" color="1" fill="1" visible="no" active="no"/>
<layer number="17" name="Pads" color="2" fill="1" visible="no" active="no"/>
<layer number="18" name="Vias" color="2" fill="1" visible="no" active="no"/>
<layer number="19" name="Unrouted" color="6" fill="1" visible="no" active="no"/>
<layer number="20" name="Dimension" color="15" fill="1" visible="no" active="no"/>
<layer number="21" name="tPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="22" name="bPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="23" name="tOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="24" name="bOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="25" name="tNames" color="7" fill="1" visible="no" active="no"/>
<layer number="26" name="bNames" color="7" fill="1" visible="no" active="no"/>
<layer number="27" name="tValues" color="7" fill="1" visible="no" active="no"/>
<layer number="28" name="bValues" color="7" fill="1" visible="no" active="no"/>
<layer number="29" name="tStop" color="7" fill="3" visible="no" active="no"/>
<layer number="30" name="bStop" color="7" fill="6" visible="no" active="no"/>
<layer number="31" name="tCream" color="7" fill="4" visible="no" active="no"/>
<layer number="32" name="bCream" color="7" fill="5" visible="no" active="no"/>
<layer number="33" name="tFinish" color="6" fill="3" visible="no" active="no"/>
<layer number="34" name="bFinish" color="6" fill="6" visible="no" active="no"/>
<layer number="35" name="tGlue" color="7" fill="4" visible="no" active="no"/>
<layer number="36" name="bGlue" color="7" fill="5" visible="no" active="no"/>
<layer number="37" name="tTest" color="7" fill="1" visible="no" active="no"/>
<layer number="38" name="bTest" color="7" fill="1" visible="no" active="no"/>
<layer number="39" name="tKeepout" color="4" fill="11" visible="no" active="no"/>
<layer number="40" name="bKeepout" color="1" fill="11" visible="no" active="no"/>
<layer number="41" name="tRestrict" color="4" fill="10" visible="no" active="no"/>
<layer number="42" name="bRestrict" color="1" fill="10" visible="no" active="no"/>
<layer number="43" name="vRestrict" color="2" fill="10" visible="no" active="no"/>
<layer number="44" name="Drills" color="7" fill="1" visible="no" active="no"/>
<layer number="45" name="Holes" color="7" fill="1" visible="no" active="no"/>
<layer number="46" name="Milling" color="3" fill="1" visible="no" active="no"/>
<layer number="47" name="Measures" color="7" fill="1" visible="no" active="no"/>
<layer number="48" name="Document" color="7" fill="1" visible="no" active="no"/>
<layer number="49" name="Reference" color="7" fill="1" visible="no" active="no"/>
<layer number="51" name="tDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="52" name="bDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes"/>
<layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes"/>
<layer number="93" name="Pins" color="2" fill="1" visible="no" active="yes"/>
<layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes"/>
<layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes"/>
<layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes"/>
<layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes"/>
<layer number="98" name="Guide" color="6" fill="1" visible="yes" active="yes"/>
</layers>
<schematic xreflabel="%F%N/%S.%C%R" xrefpart="/%S.%C%R">
<libraries>
<library name="frames">
<description>&lt;b&gt;Frames for Sheet and Layout&lt;/b&gt;</description>
<packages>
</packages>
<symbols>
<symbol name="A4-35SC">
<wire x1="63.5" y1="256.54" x2="63.5" y2="264.16" width="0.254" layer="94"/>
<wire x1="185.42" y1="256.54" x2="119.38" y2="256.54" width="0.254" layer="94"/>
<wire x1="185.42" y1="260.35" x2="166.37" y2="260.35" width="0.254" layer="94"/>
<wire x1="119.38" y1="264.16" x2="119.38" y2="260.35" width="0.254" layer="94"/>
<wire x1="119.38" y1="260.35" x2="119.38" y2="256.54" width="0.254" layer="94"/>
<wire x1="119.38" y1="256.54" x2="63.5" y2="256.54" width="0.254" layer="94"/>
<wire x1="166.37" y1="260.35" x2="166.37" y2="264.16" width="0.254" layer="94"/>
<wire x1="166.37" y1="260.35" x2="119.38" y2="260.35" width="0.254" layer="94"/>
<wire x1="0" y1="256.54" x2="63.5" y2="256.54" width="0.254" layer="94"/>
<text x="66.04" y="259.08" size="2.54" layer="94" ratio="10">NAME:</text>
<text x="120.65" y="261.493" size="1.524" layer="94" ratio="10">DATE:</text>
<text x="120.65" y="257.81" size="1.524" layer="94" ratio="10">Devices</text>
<text x="167.64" y="261.493" size="1.524" layer="94" ratio="10">SHEET:</text>
<text x="77.47" y="259.08" size="2.54" layer="94">&gt;DRAWING_NAME</text>
<text x="175.895" y="261.493" size="1.524" layer="94" ratio="10">&gt;SHEET</text>
<text x="128.905" y="261.493" size="1.524" layer="94" ratio="12">&gt;Last_Date_Time</text>
<frame x1="0" y1="0" x2="185.42" y2="264.16" columns="8" rows="5" layer="94" border-left="no" border-top="no" border-right="no" border-bottom="no"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="A4-35SC" prefix="FRAME" uservalue="yes">
<description>&lt;b&gt;FRAME&lt;/b&gt;&lt;p&gt;
DIN A4, 185 x 264 mm</description>
<gates>
<gate name="G$1" symbol="A4-35SC" x="0" y="0"/>
</gates>
<devices>
<device name="">
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="pv-measurement-array">
<packages>
<package name="8X8-POGO">
<wire x1="-9.8" y1="14" x2="-9.8" y2="15.4" width="0.127" layer="21"/>
<wire x1="-7" y1="15.4" x2="-7" y2="14" width="0.127" layer="21"/>
<wire x1="-4.2" y1="15.4" x2="-4.2" y2="14" width="0.127" layer="21"/>
<wire x1="-1.4" y1="15.4" x2="-1.4" y2="14" width="0.127" layer="21"/>
<wire x1="1.4" y1="15.4" x2="1.4" y2="14" width="0.127" layer="21"/>
<wire x1="4.2" y1="15.4" x2="4.2" y2="14" width="0.127" layer="21"/>
<wire x1="7" y1="15.4" x2="7" y2="14" width="0.127" layer="21"/>
<wire x1="9.8" y1="15.4" x2="9.8" y2="14" width="0.127" layer="21"/>
<wire x1="-14" y1="9.8" x2="-15.4" y2="9.8" width="0.127" layer="21"/>
<wire x1="-14" y1="7" x2="-15.4" y2="7" width="0.127" layer="21"/>
<wire x1="-14" y1="4.2" x2="-15.4" y2="4.2" width="0.127" layer="21"/>
<wire x1="-14" y1="1.4" x2="-15.4" y2="1.4" width="0.127" layer="21"/>
<wire x1="-14" y1="-1.4" x2="-15.4" y2="-1.4" width="0.127" layer="21"/>
<wire x1="-14" y1="-4.2" x2="-15.4" y2="-4.2" width="0.127" layer="21"/>
<wire x1="-14" y1="-7" x2="-15.4" y2="-7" width="0.127" layer="21"/>
<wire x1="-14" y1="-9.8" x2="-15.4" y2="-9.8" width="0.127" layer="21"/>
<wire x1="14" y1="9.8" x2="15.4" y2="9.8" width="0.127" layer="21"/>
<wire x1="14" y1="7" x2="15.4" y2="7" width="0.127" layer="21"/>
<wire x1="14" y1="4.2" x2="15.4" y2="4.2" width="0.127" layer="21"/>
<wire x1="14" y1="1.4" x2="15.4" y2="1.4" width="0.127" layer="21"/>
<wire x1="14" y1="-1.4" x2="15.4" y2="-1.4" width="0.127" layer="21"/>
<wire x1="14" y1="-4.2" x2="15.4" y2="-4.2" width="0.127" layer="21"/>
<wire x1="14" y1="-7" x2="15.4" y2="-7" width="0.127" layer="21"/>
<wire x1="14" y1="-9.8" x2="15.4" y2="-9.8" width="0.127" layer="21"/>
<wire x1="9.8" y1="-14" x2="9.8" y2="-15.4" width="0.127" layer="21"/>
<wire x1="7" y1="-14" x2="7" y2="-15.4" width="0.127" layer="21"/>
<wire x1="4.2" y1="-14" x2="4.2" y2="-15.4" width="0.127" layer="21"/>
<wire x1="1.4" y1="-14" x2="1.4" y2="-15.4" width="0.127" layer="21"/>
<wire x1="-1.4" y1="-14" x2="-1.4" y2="-15.4" width="0.127" layer="21"/>
<wire x1="-4.2" y1="-14" x2="-4.2" y2="-15.4" width="0.127" layer="21"/>
<wire x1="-7" y1="-14" x2="-7" y2="-15.4" width="0.127" layer="21"/>
<wire x1="-9.8" y1="-14" x2="-9.8" y2="-15.4" width="0.127" layer="21"/>
<text x="-9.8" y="16.2" size="1.27" layer="21" align="bottom-center">1</text>
<text x="-16.8" y="9.8" size="1.27" layer="21" align="center">1</text>
<text x="-7" y="16.2" size="1.27" layer="21" align="bottom-center">2</text>
<text x="-4.2" y="16.2" size="1.27" layer="21" align="bottom-center">3</text>
<text x="-1.4" y="16.2" size="1.27" layer="21" align="bottom-center">4</text>
<text x="1.4" y="16.2" size="1.27" layer="21" align="bottom-center">5</text>
<text x="4.2" y="16.2" size="1.27" layer="21" align="bottom-center">6</text>
<text x="7" y="16.2" size="1.27" layer="21" align="bottom-center">7</text>
<text x="9.8" y="16.2" size="1.27" layer="21" align="bottom-center">8</text>
<text x="-16.8" y="-9.8" size="1.27" layer="21" align="center">8</text>
<text x="-16.8" y="-7" size="1.27" layer="21" align="center">7</text>
<text x="-16.8" y="-4.2" size="1.27" layer="21" align="center">6</text>
<text x="-16.8" y="-1.4" size="1.27" layer="21" align="center">5</text>
<text x="-16.8" y="1.4" size="1.27" layer="21" align="center">4</text>
<text x="-16.8" y="4.2" size="1.27" layer="21" align="center">3</text>
<text x="-16.8" y="7" size="1.27" layer="21" align="center">2</text>
<pad name="81" x="-9.8" y="-9.8" drill="1.1"/>
<pad name="82" x="-7" y="-9.8" drill="1.1"/>
<pad name="83" x="-4.2" y="-9.8" drill="1.1"/>
<pad name="84" x="-1.4" y="-9.8" drill="1.1"/>
<pad name="85" x="1.4" y="-9.8" drill="1.1"/>
<pad name="86" x="4.2" y="-9.8" drill="1.1"/>
<pad name="87" x="7" y="-9.8" drill="1.1"/>
<pad name="88" x="9.8" y="-9.8" drill="1.1"/>
<pad name="78" x="9.8" y="-7" drill="1.1"/>
<pad name="77" x="7" y="-7" drill="1.1"/>
<pad name="76" x="4.2" y="-7" drill="1.1"/>
<pad name="75" x="1.4" y="-7" drill="1.1"/>
<pad name="74" x="-1.4" y="-7" drill="1.1"/>
<pad name="73" x="-4.2" y="-7" drill="1.1"/>
<pad name="72" x="-7" y="-7" drill="1.1"/>
<pad name="71" x="-9.8" y="-7" drill="1.1"/>
<pad name="61" x="-9.8" y="-4.2" drill="1.1"/>
<pad name="62" x="-7" y="-4.2" drill="1.1"/>
<pad name="63" x="-4.2" y="-4.2" drill="1.1"/>
<pad name="64" x="-1.4" y="-4.2" drill="1.1"/>
<pad name="65" x="1.4" y="-4.2" drill="1.1"/>
<pad name="66" x="4.2" y="-4.2" drill="1.1"/>
<pad name="67" x="7" y="-4.2" drill="1.1"/>
<pad name="68" x="9.8" y="-4.2" drill="1.1"/>
<pad name="58" x="9.8" y="-1.4" drill="1.1"/>
<pad name="57" x="7" y="-1.4" drill="1.1"/>
<pad name="56" x="4.2" y="-1.4" drill="1.1"/>
<pad name="55" x="1.4" y="-1.4" drill="1.1"/>
<pad name="54" x="-1.4" y="-1.4" drill="1.1"/>
<pad name="53" x="-4.2" y="-1.4" drill="1.1"/>
<pad name="52" x="-7" y="-1.4" drill="1.1"/>
<pad name="51" x="-9.8" y="-1.4" drill="1.1"/>
<pad name="41" x="-9.8" y="1.4" drill="1.1"/>
<pad name="42" x="-7" y="1.4" drill="1.1"/>
<pad name="43" x="-4.2" y="1.4" drill="1.1"/>
<pad name="44" x="-1.4" y="1.4" drill="1.1"/>
<pad name="45" x="1.4" y="1.4" drill="1.1"/>
<pad name="46" x="4.2" y="1.4" drill="1.1"/>
<pad name="47" x="7" y="1.4" drill="1.1"/>
<pad name="48" x="9.8" y="1.4" drill="1.1"/>
<pad name="38" x="9.8" y="4.2" drill="1.1"/>
<pad name="37" x="7" y="4.2" drill="1.1"/>
<pad name="36" x="4.2" y="4.2" drill="1.1"/>
<pad name="35" x="1.4" y="4.2" drill="1.1"/>
<pad name="34" x="-1.4" y="4.2" drill="1.1"/>
<pad name="33" x="-4.2" y="4.2" drill="1.1"/>
<pad name="32" x="-7" y="4.2" drill="1.1"/>
<pad name="31" x="-9.8" y="4.2" drill="1.1"/>
<pad name="21" x="-9.8" y="7" drill="1.1"/>
<pad name="22" x="-7" y="7" drill="1.1"/>
<pad name="23" x="-4.2" y="7" drill="1.1"/>
<pad name="24" x="-1.4" y="7" drill="1.1"/>
<pad name="25" x="1.4" y="7" drill="1.1"/>
<pad name="26" x="4.2" y="7" drill="1.1"/>
<pad name="27" x="7" y="7" drill="1.1"/>
<pad name="28" x="9.8" y="7" drill="1.1"/>
<pad name="18" x="9.8" y="9.8" drill="1.1"/>
<pad name="17" x="7" y="9.8" drill="1.1"/>
<pad name="16" x="4.2" y="9.8" drill="1.1"/>
<pad name="15" x="1.4" y="9.8" drill="1.1"/>
<pad name="14" x="-1.4" y="9.8" drill="1.1"/>
<pad name="13" x="-4.2" y="9.8" drill="1.1"/>
<pad name="12" x="-7" y="9.8" drill="1.1"/>
<pad name="11" x="-9.8" y="9.8" drill="1.1"/>
<wire x1="-12.5" y1="12.5" x2="-12.5" y2="-12.5" width="0.127" layer="21"/>
<wire x1="-12.5" y1="-12.5" x2="12.5" y2="-12.5" width="0.127" layer="21"/>
<wire x1="12.5" y1="-12.5" x2="12.5" y2="12.5" width="0.127" layer="21"/>
<wire x1="12.5" y1="12.5" x2="-12.5" y2="12.5" width="0.127" layer="21"/>
<pad name="B1" x="-12" y="12" drill="1.1"/>
<pad name="B3" x="12" y="12" drill="1.1"/>
<pad name="B7" x="-12" y="-12" drill="1.1"/>
<pad name="B5" x="12" y="-12" drill="1.1"/>
<pad name="B4" x="12" y="0" drill="1.1"/>
<pad name="B8" x="-12" y="0" drill="1.1"/>
<pad name="B6" x="0" y="-12" drill="1.1"/>
<pad name="B2" x="0" y="12" drill="1.1"/>
<text x="-18" y="12" size="1.27" layer="21">M3</text>
<text x="15.9" y="12" size="1.27" layer="21">M3</text>
<text x="-18" y="-18" size="1.27" layer="21">M3</text>
<text x="15.9" y="-18" size="1.27" layer="21">M3</text>
<hole x="-15" y="15" drill="3.2"/>
<hole x="15" y="15" drill="3.2"/>
<hole x="15" y="-15" drill="3.2"/>
<hole x="-15" y="-15" drill="3.2"/>
</package>
</packages>
<symbols>
<symbol name="8X8-PIN">
<pin name="11" x="0" y="53.34" visible="off" length="point"/>
<pin name="21" x="0" y="45.72" visible="off" length="point"/>
<pin name="31" x="0" y="38.1" visible="off" length="point"/>
<pin name="41" x="0" y="30.48" visible="off" length="point"/>
<pin name="51" x="0" y="22.86" visible="off" length="point"/>
<pin name="61" x="0" y="15.24" visible="off" length="point"/>
<pin name="71" x="0" y="7.62" visible="off" length="point"/>
<pin name="81" x="0" y="0" visible="off" length="point"/>
<pin name="12" x="7.62" y="53.34" visible="off" length="point"/>
<pin name="22" x="7.62" y="45.72" visible="off" length="point"/>
<pin name="32" x="7.62" y="38.1" visible="off" length="point"/>
<pin name="42" x="7.62" y="30.48" visible="off" length="point"/>
<pin name="52" x="7.62" y="22.86" visible="off" length="point"/>
<pin name="62" x="7.62" y="15.24" visible="off" length="point"/>
<pin name="72" x="7.62" y="7.62" visible="off" length="point"/>
<pin name="82" x="7.62" y="0" visible="off" length="point"/>
<pin name="13" x="15.24" y="53.34" visible="off" length="point"/>
<pin name="23" x="15.24" y="45.72" visible="off" length="point"/>
<pin name="33" x="15.24" y="38.1" visible="off" length="point"/>
<pin name="43" x="15.24" y="30.48" visible="off" length="point"/>
<pin name="53" x="15.24" y="22.86" visible="off" length="point"/>
<pin name="63" x="15.24" y="15.24" visible="off" length="point"/>
<pin name="73" x="15.24" y="7.62" visible="off" length="point"/>
<pin name="83" x="15.24" y="0" visible="off" length="point"/>
<pin name="14" x="22.86" y="53.34" visible="off" length="point"/>
<pin name="24" x="22.86" y="45.72" visible="off" length="point"/>
<pin name="34" x="22.86" y="38.1" visible="off" length="point"/>
<pin name="44" x="22.86" y="30.48" visible="off" length="point"/>
<pin name="54" x="22.86" y="22.86" visible="off" length="point"/>
<pin name="64" x="22.86" y="15.24" visible="off" length="point"/>
<pin name="74" x="22.86" y="7.62" visible="off" length="point"/>
<pin name="84" x="22.86" y="0" visible="off" length="point"/>
<pin name="15" x="30.48" y="53.34" visible="off" length="point"/>
<pin name="25" x="30.48" y="45.72" visible="off" length="point"/>
<pin name="35" x="30.48" y="38.1" visible="off" length="point"/>
<pin name="45" x="30.48" y="30.48" visible="off" length="point"/>
<pin name="55" x="30.48" y="22.86" visible="off" length="point"/>
<pin name="65" x="30.48" y="15.24" visible="off" length="point"/>
<pin name="75" x="30.48" y="7.62" visible="off" length="point"/>
<pin name="85" x="30.48" y="0" visible="off" length="point"/>
<pin name="16" x="38.1" y="53.34" visible="off" length="point"/>
<pin name="26" x="38.1" y="45.72" visible="off" length="point"/>
<pin name="36" x="38.1" y="38.1" visible="off" length="point"/>
<pin name="46" x="38.1" y="30.48" visible="off" length="point"/>
<pin name="56" x="38.1" y="22.86" visible="off" length="point"/>
<pin name="66" x="38.1" y="15.24" visible="off" length="point"/>
<pin name="76" x="38.1" y="7.62" visible="off" length="point"/>
<pin name="86" x="38.1" y="0" visible="off" length="point"/>
<pin name="17" x="45.72" y="53.34" visible="off" length="point"/>
<pin name="27" x="45.72" y="45.72" visible="off" length="point"/>
<pin name="37" x="45.72" y="38.1" visible="off" length="point"/>
<pin name="47" x="45.72" y="30.48" visible="off" length="point"/>
<pin name="57" x="45.72" y="22.86" visible="off" length="point"/>
<pin name="67" x="45.72" y="15.24" visible="off" length="point"/>
<pin name="77" x="45.72" y="7.62" visible="off" length="point"/>
<pin name="87" x="45.72" y="0" visible="off" length="point"/>
<pin name="18" x="53.34" y="53.34" visible="off" length="point"/>
<pin name="28" x="53.34" y="45.72" visible="off" length="point"/>
<pin name="38" x="53.34" y="38.1" visible="off" length="point"/>
<pin name="48" x="53.34" y="30.48" visible="off" length="point"/>
<pin name="58" x="53.34" y="22.86" visible="off" length="point"/>
<pin name="68" x="53.34" y="15.24" visible="off" length="point"/>
<pin name="78" x="53.34" y="7.62" visible="off" length="point"/>
<pin name="88" x="53.34" y="0" visible="off" length="point"/>
<text x="-5.08" y="61.468" size="1.27" layer="95">&gt;NAME</text>
<wire x1="-5.08" y1="58.42" x2="58.42" y2="58.42" width="0.254" layer="94"/>
<wire x1="58.42" y1="58.42" x2="58.42" y2="-5.08" width="0.254" layer="94"/>
<wire x1="58.42" y1="-5.08" x2="-5.08" y2="-5.08" width="0.254" layer="94"/>
<wire x1="-5.08" y1="-5.08" x2="-5.08" y2="58.42" width="0.254" layer="94"/>
<pin name="B" x="-5.08" y="-5.08" visible="off" length="point"/>
<circle x="0" y="53.34" radius="0.71841875" width="0" layer="94"/>
<circle x="7.62" y="53.34" radius="0.71841875" width="0" layer="94"/>
<circle x="15.24" y="53.34" radius="0.71841875" width="0" layer="94"/>
<circle x="22.86" y="53.34" radius="0.71841875" width="0" layer="94"/>
<circle x="30.48" y="53.34" radius="0.71841875" width="0" layer="94"/>
<circle x="38.1" y="53.34" radius="0.71841875" width="0" layer="94"/>
<circle x="45.72" y="53.34" radius="0.71841875" width="0" layer="94"/>
<circle x="53.34" y="53.34" radius="0.71841875" width="0" layer="94"/>
<circle x="0" y="53.34" radius="0.71841875" width="0" layer="94"/>
<circle x="0" y="45.72" radius="0.71841875" width="0" layer="94"/>
<circle x="7.62" y="45.72" radius="0.71841875" width="0" layer="94"/>
<circle x="15.24" y="45.72" radius="0.71841875" width="0" layer="94"/>
<circle x="22.86" y="45.72" radius="0.71841875" width="0" layer="94"/>
<circle x="30.48" y="45.72" radius="0.71841875" width="0" layer="94"/>
<circle x="38.1" y="45.72" radius="0.71841875" width="0" layer="94"/>
<circle x="45.72" y="45.72" radius="0.71841875" width="0" layer="94"/>
<circle x="53.34" y="45.72" radius="0.71841875" width="0" layer="94"/>
<circle x="0" y="38.1" radius="0.71841875" width="0" layer="94"/>
<circle x="0" y="30.48" radius="0.71841875" width="0" layer="94"/>
<circle x="0" y="22.86" radius="0.71841875" width="0" layer="94"/>
<circle x="0" y="15.24" radius="0.71841875" width="0" layer="94"/>
<circle x="0" y="7.62" radius="0.71841875" width="0" layer="94"/>
<circle x="0" y="0" radius="0.71841875" width="0" layer="94"/>
<circle x="7.62" y="0" radius="0.71841875" width="0" layer="94"/>
<circle x="7.62" y="7.62" radius="0.71841875" width="0" layer="94"/>
<circle x="7.62" y="15.24" radius="0.71841875" width="0" layer="94"/>
<circle x="7.62" y="22.86" radius="0.71841875" width="0" layer="94"/>
<circle x="7.62" y="30.48" radius="0.71841875" width="0" layer="94"/>
<circle x="7.62" y="38.1" radius="0.71841875" width="0" layer="94"/>
<circle x="15.24" y="38.1" radius="0.71841875" width="0" layer="94"/>
<circle x="15.24" y="30.48" radius="0.71841875" width="0" layer="94"/>
<circle x="15.24" y="22.86" radius="0.71841875" width="0" layer="94"/>
<circle x="15.24" y="15.24" radius="0.71841875" width="0" layer="94"/>
<circle x="15.24" y="7.62" radius="0.71841875" width="0" layer="94"/>
<circle x="15.24" y="0" radius="0.71841875" width="0" layer="94"/>
<circle x="22.86" y="0" radius="0.71841875" width="0" layer="94"/>
<circle x="22.86" y="7.62" radius="0.71841875" width="0" layer="94"/>
<circle x="22.86" y="15.24" radius="0.71841875" width="0" layer="94"/>
<circle x="22.86" y="22.86" radius="0.71841875" width="0" layer="94"/>
<circle x="22.86" y="30.48" radius="0.71841875" width="0" layer="94"/>
<circle x="22.86" y="38.1" radius="0.71841875" width="0" layer="94"/>
<circle x="30.48" y="38.1" radius="0.71841875" width="0" layer="94"/>
<circle x="30.48" y="30.48" radius="0.71841875" width="0" layer="94"/>
<circle x="30.48" y="22.86" radius="0.71841875" width="0" layer="94"/>
<circle x="30.48" y="15.24" radius="0.71841875" width="0" layer="94"/>
<circle x="30.48" y="7.62" radius="0.71841875" width="0" layer="94"/>
<circle x="30.48" y="0" radius="0.71841875" width="0" layer="94"/>
<circle x="38.1" y="0" radius="0.71841875" width="0" layer="94"/>
<circle x="38.1" y="7.62" radius="0.71841875" width="0" layer="94"/>
<circle x="38.1" y="15.24" radius="0.71841875" width="0" layer="94"/>
<circle x="38.1" y="22.86" radius="0.71841875" width="0" layer="94"/>
<circle x="38.1" y="30.48" radius="0.71841875" width="0" layer="94"/>
<circle x="38.1" y="38.1" radius="0.71841875" width="0" layer="94"/>
<circle x="45.72" y="38.1" radius="0.71841875" width="0" layer="94"/>
<circle x="45.72" y="30.48" radius="0.71841875" width="0" layer="94"/>
<circle x="45.72" y="22.86" radius="0.71841875" width="0" layer="94"/>
<circle x="45.72" y="15.24" radius="0.71841875" width="0" layer="94"/>
<circle x="45.72" y="7.62" radius="0.71841875" width="0" layer="94"/>
<circle x="45.72" y="0" radius="0.71841875" width="0" layer="94"/>
<circle x="53.34" y="0" radius="0.71841875" width="0" layer="94"/>
<circle x="53.34" y="7.62" radius="0.71841875" width="0" layer="94"/>
<circle x="53.34" y="15.24" radius="0.71841875" width="0" layer="94"/>
<circle x="53.34" y="22.86" radius="0.71841875" width="0" layer="94"/>
<circle x="53.34" y="30.48" radius="0.71841875" width="0" layer="94"/>
<circle x="53.34" y="38.1" radius="0.71841875" width="0" layer="94"/>
<rectangle x1="-6.35" y1="-6.35" x2="-3.81" y2="-3.81" layer="94"/>
<text x="-2.54" y="50.8" size="1.27" layer="97">11</text>
<text x="5.08" y="50.8" size="1.27" layer="97">12</text>
<text x="12.7" y="50.8" size="1.27" layer="97">13</text>
<text x="20.32" y="50.8" size="1.27" layer="97">14</text>
<text x="27.94" y="50.8" size="1.27" layer="97">15</text>
<text x="35.56" y="50.8" size="1.27" layer="97">16</text>
<text x="43.18" y="50.8" size="1.27" layer="97">17</text>
<text x="50.8" y="50.8" size="1.27" layer="97">18</text>
<text x="50.8" y="43.18" size="1.27" layer="97">28</text>
<text x="43.18" y="43.18" size="1.27" layer="97">27</text>
<text x="35.56" y="43.18" size="1.27" layer="97">26</text>
<text x="27.94" y="43.18" size="1.27" layer="97">25</text>
<text x="20.32" y="43.18" size="1.27" layer="97">24</text>
<text x="12.7" y="43.18" size="1.27" layer="97">23</text>
<text x="5.08" y="43.18" size="1.27" layer="97">22</text>
<text x="-2.54" y="43.18" size="1.27" layer="97">21</text>
<text x="-2.54" y="35.56" size="1.27" layer="97">31</text>
<text x="5.08" y="35.56" size="1.27" layer="97">32</text>
<text x="12.7" y="35.56" size="1.27" layer="97">33</text>
<text x="20.32" y="35.56" size="1.27" layer="97">34</text>
<text x="27.94" y="35.56" size="1.27" layer="97">35</text>
<text x="35.56" y="35.56" size="1.27" layer="97">36</text>
<text x="43.18" y="35.56" size="1.27" layer="97">37</text>
<text x="50.8" y="35.56" size="1.27" layer="97">38</text>
<text x="50.8" y="27.94" size="1.27" layer="97">48</text>
<text x="43.18" y="27.94" size="1.27" layer="97">47</text>
<text x="35.56" y="27.94" size="1.27" layer="97">46</text>
<text x="27.94" y="27.94" size="1.27" layer="97">45</text>
<text x="20.32" y="27.94" size="1.27" layer="97">44</text>
<text x="12.7" y="27.94" size="1.27" layer="97">43</text>
<text x="5.08" y="27.94" size="1.27" layer="97">42</text>
<text x="-2.54" y="27.94" size="1.27" layer="97">41</text>
<text x="-2.54" y="20.32" size="1.27" layer="97">51</text>
<text x="5.08" y="20.32" size="1.27" layer="97">52</text>
<text x="12.7" y="20.32" size="1.27" layer="97">53</text>
<text x="20.32" y="20.32" size="1.27" layer="97">54</text>
<text x="27.94" y="20.32" size="1.27" layer="97">55</text>
<text x="35.56" y="20.32" size="1.27" layer="97">56</text>
<text x="43.18" y="20.32" size="1.27" layer="97">57</text>
<text x="50.8" y="20.32" size="1.27" layer="97">58</text>
<text x="50.8" y="12.7" size="1.27" layer="97">68</text>
<text x="43.18" y="12.7" size="1.27" layer="97">67</text>
<text x="35.56" y="12.7" size="1.27" layer="97">66</text>
<text x="27.94" y="12.7" size="1.27" layer="97">65</text>
<text x="20.32" y="12.7" size="1.27" layer="97">64</text>
<text x="12.7" y="12.7" size="1.27" layer="97">63</text>
<text x="5.08" y="12.7" size="1.27" layer="97">62</text>
<text x="-2.54" y="12.7" size="1.27" layer="97">61</text>
<text x="-2.54" y="5.08" size="1.27" layer="97">71</text>
<text x="5.08" y="5.08" size="1.27" layer="97">72</text>
<text x="12.7" y="5.08" size="1.27" layer="97">73</text>
<text x="20.32" y="5.08" size="1.27" layer="97">74</text>
<text x="27.94" y="5.08" size="1.27" layer="97">75</text>
<text x="35.56" y="5.08" size="1.27" layer="97">76</text>
<text x="43.18" y="5.08" size="1.27" layer="97">77</text>
<text x="50.8" y="5.08" size="1.27" layer="97">78</text>
<text x="50.8" y="-2.54" size="1.27" layer="97">88</text>
<text x="43.18" y="-2.54" size="1.27" layer="97">87</text>
<text x="35.56" y="-2.54" size="1.27" layer="97">86</text>
<text x="27.94" y="-2.54" size="1.27" layer="97">85</text>
<text x="20.32" y="-2.54" size="1.27" layer="97">84</text>
<text x="12.7" y="-2.54" size="1.27" layer="97">83</text>
<text x="5.08" y="-2.54" size="1.27" layer="97">82</text>
<text x="-2.54" y="-2.54" size="1.27" layer="97">81</text>
<text x="-7.62" y="-8.128" size="1.27" layer="97">BC</text>
</symbol>
</symbols>
<devicesets>
<deviceset name="8X8-POGO" prefix="8X8">
<gates>
<gate name="G$1" symbol="8X8-PIN" x="2.54" y="2.54"/>
</gates>
<devices>
<device name="" package="8X8-POGO">
<connects>
<connect gate="G$1" pin="11" pad="11"/>
<connect gate="G$1" pin="12" pad="12"/>
<connect gate="G$1" pin="13" pad="13"/>
<connect gate="G$1" pin="14" pad="14"/>
<connect gate="G$1" pin="15" pad="15"/>
<connect gate="G$1" pin="16" pad="16"/>
<connect gate="G$1" pin="17" pad="17"/>
<connect gate="G$1" pin="18" pad="18"/>
<connect gate="G$1" pin="21" pad="21"/>
<connect gate="G$1" pin="22" pad="22"/>
<connect gate="G$1" pin="23" pad="23"/>
<connect gate="G$1" pin="24" pad="24"/>
<connect gate="G$1" pin="25" pad="25"/>
<connect gate="G$1" pin="26" pad="26"/>
<connect gate="G$1" pin="27" pad="27"/>
<connect gate="G$1" pin="28" pad="28"/>
<connect gate="G$1" pin="31" pad="31"/>
<connect gate="G$1" pin="32" pad="32"/>
<connect gate="G$1" pin="33" pad="33"/>
<connect gate="G$1" pin="34" pad="34"/>
<connect gate="G$1" pin="35" pad="35"/>
<connect gate="G$1" pin="36" pad="36"/>
<connect gate="G$1" pin="37" pad="37"/>
<connect gate="G$1" pin="38" pad="38"/>
<connect gate="G$1" pin="41" pad="41"/>
<connect gate="G$1" pin="42" pad="42"/>
<connect gate="G$1" pin="43" pad="43"/>
<connect gate="G$1" pin="44" pad="44"/>
<connect gate="G$1" pin="45" pad="45"/>
<connect gate="G$1" pin="46" pad="46"/>
<connect gate="G$1" pin="47" pad="47"/>
<connect gate="G$1" pin="48" pad="48"/>
<connect gate="G$1" pin="51" pad="51"/>
<connect gate="G$1" pin="52" pad="52"/>
<connect gate="G$1" pin="53" pad="53"/>
<connect gate="G$1" pin="54" pad="54"/>
<connect gate="G$1" pin="55" pad="55"/>
<connect gate="G$1" pin="56" pad="56"/>
<connect gate="G$1" pin="57" pad="57"/>
<connect gate="G$1" pin="58" pad="58"/>
<connect gate="G$1" pin="61" pad="61"/>
<connect gate="G$1" pin="62" pad="62"/>
<connect gate="G$1" pin="63" pad="63"/>
<connect gate="G$1" pin="64" pad="64"/>
<connect gate="G$1" pin="65" pad="65"/>
<connect gate="G$1" pin="66" pad="66"/>
<connect gate="G$1" pin="67" pad="67"/>
<connect gate="G$1" pin="68" pad="68"/>
<connect gate="G$1" pin="71" pad="71"/>
<connect gate="G$1" pin="72" pad="72"/>
<connect gate="G$1" pin="73" pad="73"/>
<connect gate="G$1" pin="74" pad="74"/>
<connect gate="G$1" pin="75" pad="75"/>
<connect gate="G$1" pin="76" pad="76"/>
<connect gate="G$1" pin="77" pad="77"/>
<connect gate="G$1" pin="78" pad="78"/>
<connect gate="G$1" pin="81" pad="81"/>
<connect gate="G$1" pin="82" pad="82"/>
<connect gate="G$1" pin="83" pad="83"/>
<connect gate="G$1" pin="84" pad="84"/>
<connect gate="G$1" pin="85" pad="85"/>
<connect gate="G$1" pin="86" pad="86"/>
<connect gate="G$1" pin="87" pad="87"/>
<connect gate="G$1" pin="88" pad="88"/>
<connect gate="G$1" pin="B" pad="B1 B2 B3 B4 B5 B6 B7 B8"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="con-headers-harvin">
<packages>
<package name="D01-9923246">
<wire x1="-1.27" y1="1.016" x2="-1.016" y2="1.27" width="0.127" layer="21"/>
<wire x1="1.016" y1="1.27" x2="1.27" y2="1.016" width="0.127" layer="21"/>
<wire x1="1.27" y1="1.016" x2="1.27" y2="-1.016" width="0.127" layer="21"/>
<wire x1="1.27" y1="-1.016" x2="1.016" y2="-1.27" width="0.127" layer="21"/>
<wire x1="1.016" y1="-1.27" x2="-1.016" y2="-1.27" width="0.127" layer="21"/>
<wire x1="-1.016" y1="-1.27" x2="-1.27" y2="-1.016" width="0.127" layer="21"/>
<wire x1="-1.27" y1="-1.016" x2="-1.27" y2="1.016" width="0.127" layer="21"/>
<pad name="1" x="0" y="0" drill="0.8"/>
<wire x1="-1.27" y1="3.556" x2="-1.016" y2="3.81" width="0.127" layer="21"/>
<wire x1="1.016" y1="3.81" x2="1.27" y2="3.556" width="0.127" layer="21"/>
<wire x1="1.27" y1="3.556" x2="1.27" y2="1.524" width="0.127" layer="21"/>
<wire x1="1.27" y1="1.524" x2="1.016" y2="1.27" width="0.127" layer="21"/>
<wire x1="1.016" y1="1.27" x2="-1.016" y2="1.27" width="0.127" layer="21"/>
<wire x1="-1.016" y1="1.27" x2="-1.27" y2="1.524" width="0.127" layer="21"/>
<wire x1="-1.27" y1="1.524" x2="-1.27" y2="3.556" width="0.127" layer="21"/>
<pad name="2" x="0" y="2.54" drill="0.8"/>
<wire x1="-1.27" y1="6.096" x2="-1.016" y2="6.35" width="0.127" layer="21"/>
<wire x1="1.016" y1="6.35" x2="1.27" y2="6.096" width="0.127" layer="21"/>
<wire x1="1.27" y1="6.096" x2="1.27" y2="4.064" width="0.127" layer="21"/>
<wire x1="1.27" y1="4.064" x2="1.016" y2="3.81" width="0.127" layer="21"/>
<wire x1="1.016" y1="3.81" x2="-1.016" y2="3.81" width="0.127" layer="21"/>
<wire x1="-1.016" y1="3.81" x2="-1.27" y2="4.064" width="0.127" layer="21"/>
<wire x1="-1.27" y1="4.064" x2="-1.27" y2="6.096" width="0.127" layer="21"/>
<pad name="3" x="0" y="5.08" drill="0.8"/>
<wire x1="-1.27" y1="8.636" x2="-1.016" y2="8.89" width="0.127" layer="21"/>
<wire x1="1.016" y1="8.89" x2="1.27" y2="8.636" width="0.127" layer="21"/>
<wire x1="1.27" y1="8.636" x2="1.27" y2="6.604" width="0.127" layer="21"/>
<wire x1="1.27" y1="6.604" x2="1.016" y2="6.35" width="0.127" layer="21"/>
<wire x1="1.016" y1="6.35" x2="-1.016" y2="6.35" width="0.127" layer="21"/>
<wire x1="-1.016" y1="6.35" x2="-1.27" y2="6.604" width="0.127" layer="21"/>
<wire x1="-1.27" y1="6.604" x2="-1.27" y2="8.636" width="0.127" layer="21"/>
<pad name="4" x="0" y="7.62" drill="0.8"/>
<wire x1="-1.27" y1="11.176" x2="-1.016" y2="11.43" width="0.127" layer="21"/>
<wire x1="1.016" y1="11.43" x2="1.27" y2="11.176" width="0.127" layer="21"/>
<wire x1="1.27" y1="11.176" x2="1.27" y2="9.144" width="0.127" layer="21"/>
<wire x1="1.27" y1="9.144" x2="1.016" y2="8.89" width="0.127" layer="21"/>
<wire x1="1.016" y1="8.89" x2="-1.016" y2="8.89" width="0.127" layer="21"/>
<wire x1="-1.016" y1="8.89" x2="-1.27" y2="9.144" width="0.127" layer="21"/>
<wire x1="-1.27" y1="9.144" x2="-1.27" y2="11.176" width="0.127" layer="21"/>
<pad name="5" x="0" y="10.16" drill="0.8"/>
<wire x1="-1.27" y1="13.716" x2="-1.016" y2="13.97" width="0.127" layer="21"/>
<wire x1="1.016" y1="13.97" x2="1.27" y2="13.716" width="0.127" layer="21"/>
<wire x1="1.27" y1="13.716" x2="1.27" y2="11.684" width="0.127" layer="21"/>
<wire x1="1.27" y1="11.684" x2="1.016" y2="11.43" width="0.127" layer="21"/>
<wire x1="1.016" y1="11.43" x2="-1.016" y2="11.43" width="0.127" layer="21"/>
<wire x1="-1.016" y1="11.43" x2="-1.27" y2="11.684" width="0.127" layer="21"/>
<wire x1="-1.27" y1="11.684" x2="-1.27" y2="13.716" width="0.127" layer="21"/>
<pad name="6" x="0" y="12.7" drill="0.8"/>
<wire x1="-1.27" y1="16.256" x2="-1.016" y2="16.51" width="0.127" layer="21"/>
<wire x1="1.016" y1="16.51" x2="1.27" y2="16.256" width="0.127" layer="21"/>
<wire x1="1.27" y1="16.256" x2="1.27" y2="14.224" width="0.127" layer="21"/>
<wire x1="1.27" y1="14.224" x2="1.016" y2="13.97" width="0.127" layer="21"/>
<wire x1="1.016" y1="13.97" x2="-1.016" y2="13.97" width="0.127" layer="21"/>
<wire x1="-1.016" y1="13.97" x2="-1.27" y2="14.224" width="0.127" layer="21"/>
<wire x1="-1.27" y1="14.224" x2="-1.27" y2="16.256" width="0.127" layer="21"/>
<pad name="7" x="0" y="15.24" drill="0.8"/>
<wire x1="-1.27" y1="18.796" x2="-1.016" y2="19.05" width="0.127" layer="21"/>
<wire x1="1.016" y1="19.05" x2="1.27" y2="18.796" width="0.127" layer="21"/>
<wire x1="1.27" y1="18.796" x2="1.27" y2="16.764" width="0.127" layer="21"/>
<wire x1="1.27" y1="16.764" x2="1.016" y2="16.51" width="0.127" layer="21"/>
<wire x1="1.016" y1="16.51" x2="-1.016" y2="16.51" width="0.127" layer="21"/>
<wire x1="-1.016" y1="16.51" x2="-1.27" y2="16.764" width="0.127" layer="21"/>
<wire x1="-1.27" y1="16.764" x2="-1.27" y2="18.796" width="0.127" layer="21"/>
<pad name="8" x="0" y="17.78" drill="0.8"/>
<wire x1="-1.27" y1="21.336" x2="-1.016" y2="21.59" width="0.127" layer="21"/>
<wire x1="1.016" y1="21.59" x2="1.27" y2="21.336" width="0.127" layer="21"/>
<wire x1="1.27" y1="21.336" x2="1.27" y2="19.304" width="0.127" layer="21"/>
<wire x1="1.27" y1="19.304" x2="1.016" y2="19.05" width="0.127" layer="21"/>
<wire x1="1.016" y1="19.05" x2="-1.016" y2="19.05" width="0.127" layer="21"/>
<wire x1="-1.016" y1="19.05" x2="-1.27" y2="19.304" width="0.127" layer="21"/>
<wire x1="-1.27" y1="19.304" x2="-1.27" y2="21.336" width="0.127" layer="21"/>
<pad name="9" x="0" y="20.32" drill="0.8"/>
<wire x1="-1.27" y1="23.876" x2="-1.016" y2="24.13" width="0.127" layer="21"/>
<wire x1="1.016" y1="24.13" x2="1.27" y2="23.876" width="0.127" layer="21"/>
<wire x1="1.27" y1="23.876" x2="1.27" y2="21.844" width="0.127" layer="21"/>
<wire x1="1.27" y1="21.844" x2="1.016" y2="21.59" width="0.127" layer="21"/>
<wire x1="1.016" y1="21.59" x2="-1.016" y2="21.59" width="0.127" layer="21"/>
<wire x1="-1.016" y1="21.59" x2="-1.27" y2="21.844" width="0.127" layer="21"/>
<wire x1="-1.27" y1="21.844" x2="-1.27" y2="23.876" width="0.127" layer="21"/>
<pad name="10" x="0" y="22.86" drill="0.8"/>
<wire x1="-1.27" y1="26.416" x2="-1.016" y2="26.67" width="0.127" layer="21"/>
<wire x1="1.016" y1="26.67" x2="1.27" y2="26.416" width="0.127" layer="21"/>
<wire x1="1.27" y1="26.416" x2="1.27" y2="24.384" width="0.127" layer="21"/>
<wire x1="1.27" y1="24.384" x2="1.016" y2="24.13" width="0.127" layer="21"/>
<wire x1="1.016" y1="24.13" x2="-1.016" y2="24.13" width="0.127" layer="21"/>
<wire x1="-1.016" y1="24.13" x2="-1.27" y2="24.384" width="0.127" layer="21"/>
<wire x1="-1.27" y1="24.384" x2="-1.27" y2="26.416" width="0.127" layer="21"/>
<pad name="11" x="0" y="25.4" drill="0.8"/>
<wire x1="-1.27" y1="28.956" x2="-1.016" y2="29.21" width="0.127" layer="21"/>
<wire x1="1.016" y1="29.21" x2="1.27" y2="28.956" width="0.127" layer="21"/>
<wire x1="1.27" y1="28.956" x2="1.27" y2="26.924" width="0.127" layer="21"/>
<wire x1="1.27" y1="26.924" x2="1.016" y2="26.67" width="0.127" layer="21"/>
<wire x1="1.016" y1="26.67" x2="-1.016" y2="26.67" width="0.127" layer="21"/>
<wire x1="-1.016" y1="26.67" x2="-1.27" y2="26.924" width="0.127" layer="21"/>
<wire x1="-1.27" y1="26.924" x2="-1.27" y2="28.956" width="0.127" layer="21"/>
<pad name="12" x="0" y="27.94" drill="0.8"/>
<wire x1="-1.27" y1="31.496" x2="-1.016" y2="31.75" width="0.127" layer="21"/>
<wire x1="1.016" y1="31.75" x2="1.27" y2="31.496" width="0.127" layer="21"/>
<wire x1="1.27" y1="31.496" x2="1.27" y2="29.464" width="0.127" layer="21"/>
<wire x1="1.27" y1="29.464" x2="1.016" y2="29.21" width="0.127" layer="21"/>
<wire x1="1.016" y1="29.21" x2="-1.016" y2="29.21" width="0.127" layer="21"/>
<wire x1="-1.016" y1="29.21" x2="-1.27" y2="29.464" width="0.127" layer="21"/>
<wire x1="-1.27" y1="29.464" x2="-1.27" y2="31.496" width="0.127" layer="21"/>
<pad name="13" x="0" y="30.48" drill="0.8"/>
<wire x1="-1.27" y1="34.036" x2="-1.016" y2="34.29" width="0.127" layer="21"/>
<wire x1="1.016" y1="34.29" x2="1.27" y2="34.036" width="0.127" layer="21"/>
<wire x1="1.27" y1="34.036" x2="1.27" y2="32.004" width="0.127" layer="21"/>
<wire x1="1.27" y1="32.004" x2="1.016" y2="31.75" width="0.127" layer="21"/>
<wire x1="1.016" y1="31.75" x2="-1.016" y2="31.75" width="0.127" layer="21"/>
<wire x1="-1.016" y1="31.75" x2="-1.27" y2="32.004" width="0.127" layer="21"/>
<wire x1="-1.27" y1="32.004" x2="-1.27" y2="34.036" width="0.127" layer="21"/>
<pad name="14" x="0" y="33.02" drill="0.8"/>
<wire x1="-1.27" y1="36.576" x2="-1.016" y2="36.83" width="0.127" layer="21"/>
<wire x1="1.016" y1="36.83" x2="1.27" y2="36.576" width="0.127" layer="21"/>
<wire x1="1.27" y1="36.576" x2="1.27" y2="34.544" width="0.127" layer="21"/>
<wire x1="1.27" y1="34.544" x2="1.016" y2="34.29" width="0.127" layer="21"/>
<wire x1="1.016" y1="34.29" x2="-1.016" y2="34.29" width="0.127" layer="21"/>
<wire x1="-1.016" y1="34.29" x2="-1.27" y2="34.544" width="0.127" layer="21"/>
<wire x1="-1.27" y1="34.544" x2="-1.27" y2="36.576" width="0.127" layer="21"/>
<pad name="15" x="0" y="35.56" drill="0.8"/>
<wire x1="-1.27" y1="39.116" x2="-1.016" y2="39.37" width="0.127" layer="21"/>
<wire x1="1.016" y1="39.37" x2="1.27" y2="39.116" width="0.127" layer="21"/>
<wire x1="1.27" y1="39.116" x2="1.27" y2="37.084" width="0.127" layer="21"/>
<wire x1="1.27" y1="37.084" x2="1.016" y2="36.83" width="0.127" layer="21"/>
<wire x1="1.016" y1="36.83" x2="-1.016" y2="36.83" width="0.127" layer="21"/>
<wire x1="-1.016" y1="36.83" x2="-1.27" y2="37.084" width="0.127" layer="21"/>
<wire x1="-1.27" y1="37.084" x2="-1.27" y2="39.116" width="0.127" layer="21"/>
<pad name="16" x="0" y="38.1" drill="0.8"/>
<wire x1="-1.27" y1="41.656" x2="-1.016" y2="41.91" width="0.127" layer="21"/>
<wire x1="1.016" y1="41.91" x2="1.27" y2="41.656" width="0.127" layer="21"/>
<wire x1="1.27" y1="41.656" x2="1.27" y2="39.624" width="0.127" layer="21"/>
<wire x1="1.27" y1="39.624" x2="1.016" y2="39.37" width="0.127" layer="21"/>
<wire x1="1.016" y1="39.37" x2="-1.016" y2="39.37" width="0.127" layer="21"/>
<wire x1="-1.016" y1="39.37" x2="-1.27" y2="39.624" width="0.127" layer="21"/>
<wire x1="-1.27" y1="39.624" x2="-1.27" y2="41.656" width="0.127" layer="21"/>
<pad name="17" x="0" y="40.64" drill="0.8"/>
<wire x1="-1.27" y1="44.196" x2="-1.016" y2="44.45" width="0.127" layer="21"/>
<wire x1="1.016" y1="44.45" x2="1.27" y2="44.196" width="0.127" layer="21"/>
<wire x1="1.27" y1="44.196" x2="1.27" y2="42.164" width="0.127" layer="21"/>
<wire x1="1.27" y1="42.164" x2="1.016" y2="41.91" width="0.127" layer="21"/>
<wire x1="1.016" y1="41.91" x2="-1.016" y2="41.91" width="0.127" layer="21"/>
<wire x1="-1.016" y1="41.91" x2="-1.27" y2="42.164" width="0.127" layer="21"/>
<wire x1="-1.27" y1="42.164" x2="-1.27" y2="44.196" width="0.127" layer="21"/>
<pad name="18" x="0" y="43.18" drill="0.8"/>
<wire x1="-1.27" y1="46.736" x2="-1.016" y2="46.99" width="0.127" layer="21"/>
<wire x1="1.016" y1="46.99" x2="1.27" y2="46.736" width="0.127" layer="21"/>
<wire x1="1.27" y1="46.736" x2="1.27" y2="44.704" width="0.127" layer="21"/>
<wire x1="1.27" y1="44.704" x2="1.016" y2="44.45" width="0.127" layer="21"/>
<wire x1="1.016" y1="44.45" x2="-1.016" y2="44.45" width="0.127" layer="21"/>
<wire x1="-1.016" y1="44.45" x2="-1.27" y2="44.704" width="0.127" layer="21"/>
<wire x1="-1.27" y1="44.704" x2="-1.27" y2="46.736" width="0.127" layer="21"/>
<pad name="19" x="0" y="45.72" drill="0.8"/>
<wire x1="-1.27" y1="49.276" x2="-1.016" y2="49.53" width="0.127" layer="21"/>
<wire x1="1.016" y1="49.53" x2="1.27" y2="49.276" width="0.127" layer="21"/>
<wire x1="1.27" y1="49.276" x2="1.27" y2="47.244" width="0.127" layer="21"/>
<wire x1="1.27" y1="47.244" x2="1.016" y2="46.99" width="0.127" layer="21"/>
<wire x1="1.016" y1="46.99" x2="-1.016" y2="46.99" width="0.127" layer="21"/>
<wire x1="-1.016" y1="46.99" x2="-1.27" y2="47.244" width="0.127" layer="21"/>
<wire x1="-1.27" y1="47.244" x2="-1.27" y2="49.276" width="0.127" layer="21"/>
<pad name="20" x="0" y="48.26" drill="0.8"/>
<wire x1="-1.27" y1="51.816" x2="-1.016" y2="52.07" width="0.127" layer="21"/>
<wire x1="1.016" y1="52.07" x2="1.27" y2="51.816" width="0.127" layer="21"/>
<wire x1="1.27" y1="51.816" x2="1.27" y2="49.784" width="0.127" layer="21"/>
<wire x1="1.27" y1="49.784" x2="1.016" y2="49.53" width="0.127" layer="21"/>
<wire x1="1.016" y1="49.53" x2="-1.016" y2="49.53" width="0.127" layer="21"/>
<wire x1="-1.016" y1="49.53" x2="-1.27" y2="49.784" width="0.127" layer="21"/>
<wire x1="-1.27" y1="49.784" x2="-1.27" y2="51.816" width="0.127" layer="21"/>
<pad name="21" x="0" y="50.8" drill="0.8"/>
<wire x1="-1.27" y1="54.356" x2="-1.016" y2="54.61" width="0.127" layer="21"/>
<wire x1="1.016" y1="54.61" x2="1.27" y2="54.356" width="0.127" layer="21"/>
<wire x1="1.27" y1="54.356" x2="1.27" y2="52.324" width="0.127" layer="21"/>
<wire x1="1.27" y1="52.324" x2="1.016" y2="52.07" width="0.127" layer="21"/>
<wire x1="1.016" y1="52.07" x2="-1.016" y2="52.07" width="0.127" layer="21"/>
<wire x1="-1.016" y1="52.07" x2="-1.27" y2="52.324" width="0.127" layer="21"/>
<wire x1="-1.27" y1="52.324" x2="-1.27" y2="54.356" width="0.127" layer="21"/>
<pad name="22" x="0" y="53.34" drill="0.8"/>
<wire x1="-1.27" y1="56.896" x2="-1.016" y2="57.15" width="0.127" layer="21"/>
<wire x1="1.016" y1="57.15" x2="1.27" y2="56.896" width="0.127" layer="21"/>
<wire x1="1.27" y1="56.896" x2="1.27" y2="54.864" width="0.127" layer="21"/>
<wire x1="1.27" y1="54.864" x2="1.016" y2="54.61" width="0.127" layer="21"/>
<wire x1="1.016" y1="54.61" x2="-1.016" y2="54.61" width="0.127" layer="21"/>
<wire x1="-1.016" y1="54.61" x2="-1.27" y2="54.864" width="0.127" layer="21"/>
<wire x1="-1.27" y1="54.864" x2="-1.27" y2="56.896" width="0.127" layer="21"/>
<pad name="23" x="0" y="55.88" drill="0.8"/>
<wire x1="-1.27" y1="59.436" x2="-1.016" y2="59.69" width="0.127" layer="21"/>
<wire x1="1.016" y1="59.69" x2="1.27" y2="59.436" width="0.127" layer="21"/>
<wire x1="1.27" y1="59.436" x2="1.27" y2="57.404" width="0.127" layer="21"/>
<wire x1="1.27" y1="57.404" x2="1.016" y2="57.15" width="0.127" layer="21"/>
<wire x1="1.016" y1="57.15" x2="-1.016" y2="57.15" width="0.127" layer="21"/>
<wire x1="-1.016" y1="57.15" x2="-1.27" y2="57.404" width="0.127" layer="21"/>
<wire x1="-1.27" y1="57.404" x2="-1.27" y2="59.436" width="0.127" layer="21"/>
<pad name="24" x="0" y="58.42" drill="0.8"/>
<wire x1="-1.27" y1="61.976" x2="-1.016" y2="62.23" width="0.127" layer="21"/>
<wire x1="1.016" y1="62.23" x2="1.27" y2="61.976" width="0.127" layer="21"/>
<wire x1="1.27" y1="61.976" x2="1.27" y2="59.944" width="0.127" layer="21"/>
<wire x1="1.27" y1="59.944" x2="1.016" y2="59.69" width="0.127" layer="21"/>
<wire x1="1.016" y1="59.69" x2="-1.016" y2="59.69" width="0.127" layer="21"/>
<wire x1="-1.016" y1="59.69" x2="-1.27" y2="59.944" width="0.127" layer="21"/>
<wire x1="-1.27" y1="59.944" x2="-1.27" y2="61.976" width="0.127" layer="21"/>
<pad name="25" x="0" y="60.96" drill="0.8"/>
<wire x1="-1.27" y1="64.516" x2="-1.016" y2="64.77" width="0.127" layer="21"/>
<wire x1="1.016" y1="64.77" x2="1.27" y2="64.516" width="0.127" layer="21"/>
<wire x1="1.27" y1="64.516" x2="1.27" y2="62.484" width="0.127" layer="21"/>
<wire x1="1.27" y1="62.484" x2="1.016" y2="62.23" width="0.127" layer="21"/>
<wire x1="1.016" y1="62.23" x2="-1.016" y2="62.23" width="0.127" layer="21"/>
<wire x1="-1.016" y1="62.23" x2="-1.27" y2="62.484" width="0.127" layer="21"/>
<wire x1="-1.27" y1="62.484" x2="-1.27" y2="64.516" width="0.127" layer="21"/>
<pad name="26" x="0" y="63.5" drill="0.8"/>
<wire x1="-1.27" y1="67.056" x2="-1.016" y2="67.31" width="0.127" layer="21"/>
<wire x1="1.016" y1="67.31" x2="1.27" y2="67.056" width="0.127" layer="21"/>
<wire x1="1.27" y1="67.056" x2="1.27" y2="65.024" width="0.127" layer="21"/>
<wire x1="1.27" y1="65.024" x2="1.016" y2="64.77" width="0.127" layer="21"/>
<wire x1="1.016" y1="64.77" x2="-1.016" y2="64.77" width="0.127" layer="21"/>
<wire x1="-1.016" y1="64.77" x2="-1.27" y2="65.024" width="0.127" layer="21"/>
<wire x1="-1.27" y1="65.024" x2="-1.27" y2="67.056" width="0.127" layer="21"/>
<pad name="27" x="0" y="66.04" drill="0.8"/>
<wire x1="-1.27" y1="69.596" x2="-1.016" y2="69.85" width="0.127" layer="21"/>
<wire x1="1.016" y1="69.85" x2="1.27" y2="69.596" width="0.127" layer="21"/>
<wire x1="1.27" y1="69.596" x2="1.27" y2="67.564" width="0.127" layer="21"/>
<wire x1="1.27" y1="67.564" x2="1.016" y2="67.31" width="0.127" layer="21"/>
<wire x1="1.016" y1="67.31" x2="-1.016" y2="67.31" width="0.127" layer="21"/>
<wire x1="-1.016" y1="67.31" x2="-1.27" y2="67.564" width="0.127" layer="21"/>
<wire x1="-1.27" y1="67.564" x2="-1.27" y2="69.596" width="0.127" layer="21"/>
<pad name="28" x="0" y="68.58" drill="0.8"/>
<wire x1="-1.27" y1="72.136" x2="-1.016" y2="72.39" width="0.127" layer="21"/>
<wire x1="1.016" y1="72.39" x2="1.27" y2="72.136" width="0.127" layer="21"/>
<wire x1="1.27" y1="72.136" x2="1.27" y2="70.104" width="0.127" layer="21"/>
<wire x1="1.27" y1="70.104" x2="1.016" y2="69.85" width="0.127" layer="21"/>
<wire x1="1.016" y1="69.85" x2="-1.016" y2="69.85" width="0.127" layer="21"/>
<wire x1="-1.016" y1="69.85" x2="-1.27" y2="70.104" width="0.127" layer="21"/>
<wire x1="-1.27" y1="70.104" x2="-1.27" y2="72.136" width="0.127" layer="21"/>
<pad name="29" x="0" y="71.12" drill="0.8"/>
<wire x1="-1.27" y1="74.676" x2="-1.016" y2="74.93" width="0.127" layer="21"/>
<wire x1="1.016" y1="74.93" x2="1.27" y2="74.676" width="0.127" layer="21"/>
<wire x1="1.27" y1="74.676" x2="1.27" y2="72.644" width="0.127" layer="21"/>
<wire x1="1.27" y1="72.644" x2="1.016" y2="72.39" width="0.127" layer="21"/>
<wire x1="1.016" y1="72.39" x2="-1.016" y2="72.39" width="0.127" layer="21"/>
<wire x1="-1.016" y1="72.39" x2="-1.27" y2="72.644" width="0.127" layer="21"/>
<wire x1="-1.27" y1="72.644" x2="-1.27" y2="74.676" width="0.127" layer="21"/>
<pad name="30" x="0" y="73.66" drill="0.8"/>
<wire x1="-1.27" y1="77.216" x2="-1.016" y2="77.47" width="0.127" layer="21"/>
<wire x1="1.016" y1="77.47" x2="1.27" y2="77.216" width="0.127" layer="21"/>
<wire x1="1.27" y1="77.216" x2="1.27" y2="75.184" width="0.127" layer="21"/>
<wire x1="1.27" y1="75.184" x2="1.016" y2="74.93" width="0.127" layer="21"/>
<wire x1="1.016" y1="74.93" x2="-1.016" y2="74.93" width="0.127" layer="21"/>
<wire x1="-1.016" y1="74.93" x2="-1.27" y2="75.184" width="0.127" layer="21"/>
<wire x1="-1.27" y1="75.184" x2="-1.27" y2="77.216" width="0.127" layer="21"/>
<pad name="31" x="0" y="76.2" drill="0.8"/>
<wire x1="-1.27" y1="79.756" x2="-1.016" y2="80.01" width="0.127" layer="21"/>
<wire x1="1.016" y1="80.01" x2="1.27" y2="79.756" width="0.127" layer="21"/>
<wire x1="1.27" y1="79.756" x2="1.27" y2="77.724" width="0.127" layer="21"/>
<wire x1="1.27" y1="77.724" x2="1.016" y2="77.47" width="0.127" layer="21"/>
<wire x1="1.016" y1="77.47" x2="-1.016" y2="77.47" width="0.127" layer="21"/>
<wire x1="-1.016" y1="77.47" x2="-1.27" y2="77.724" width="0.127" layer="21"/>
<wire x1="-1.27" y1="77.724" x2="-1.27" y2="79.756" width="0.127" layer="21"/>
<wire x1="1.016" y1="80.01" x2="-1.016" y2="80.01" width="0.127" layer="21"/>
<pad name="32" x="0" y="78.74" drill="0.8"/>
<text x="-1.27" y="-1.27" size="1.27" layer="21">1</text>
<text x="-1.27" y="78.74" size="1.27" layer="21">32</text>
</package>
<package name="D01-9920146">
<pad name="1" x="0" y="0" drill="0.8"/>
<wire x1="1.016" y1="1.27" x2="1.27" y2="1.016" width="0.127" layer="21"/>
<wire x1="1.27" y1="1.016" x2="1.27" y2="-1.016" width="0.127" layer="21"/>
<wire x1="1.27" y1="-1.016" x2="1.016" y2="-1.27" width="0.127" layer="21"/>
<wire x1="1.016" y1="-1.27" x2="-1.016" y2="-1.27" width="0.127" layer="21"/>
<wire x1="-1.016" y1="-1.27" x2="-1.27" y2="-1.016" width="0.127" layer="21"/>
<wire x1="-1.27" y1="-1.016" x2="-1.27" y2="1.016" width="0.127" layer="21"/>
<wire x1="-1.27" y1="1.016" x2="-1.016" y2="1.27" width="0.127" layer="21"/>
<wire x1="-1.016" y1="1.27" x2="1.016" y2="1.27" width="0.127" layer="21"/>
</package>
</packages>
<symbols>
<symbol name="D01-9923246">
<pin name="1" x="0" y="0" visible="pin" length="short"/>
<pin name="2" x="0" y="2.54" visible="pin" length="short"/>
<pin name="3" x="0" y="5.08" visible="pin" length="short"/>
<pin name="4" x="0" y="7.62" visible="pin" length="short"/>
<pin name="5" x="0" y="10.16" visible="pin" length="short"/>
<pin name="6" x="0" y="12.7" visible="pin" length="short"/>
<pin name="7" x="0" y="15.24" visible="pin" length="short"/>
<pin name="8" x="0" y="17.78" visible="pin" length="short"/>
<pin name="9" x="0" y="20.32" visible="pin" length="short"/>
<pin name="10" x="0" y="22.86" visible="pin" length="short"/>
<pin name="11" x="0" y="25.4" visible="pin" length="short"/>
<pin name="12" x="0" y="27.94" visible="pin" length="short"/>
<pin name="13" x="0" y="30.48" visible="pin" length="short"/>
<pin name="14" x="0" y="33.02" visible="pin" length="short"/>
<pin name="15" x="0" y="35.56" visible="pin" length="short"/>
<pin name="16" x="0" y="38.1" visible="pin" length="short"/>
<pin name="17" x="0" y="40.64" visible="pin" length="short"/>
<pin name="18" x="0" y="43.18" visible="pin" length="short"/>
<pin name="19" x="0" y="45.72" visible="pin" length="short"/>
<pin name="20" x="0" y="48.26" visible="pin" length="short"/>
<pin name="21" x="0" y="50.8" visible="pin" length="short"/>
<pin name="22" x="0" y="53.34" visible="pin" length="short"/>
<pin name="23" x="0" y="55.88" visible="pin" length="short"/>
<pin name="24" x="0" y="58.42" visible="pin" length="short"/>
<pin name="25" x="0" y="60.96" visible="pin" length="short"/>
<pin name="26" x="0" y="63.5" visible="pin" length="short"/>
<pin name="27" x="0" y="66.04" visible="pin" length="short"/>
<pin name="28" x="0" y="68.58" visible="pin" length="short"/>
<pin name="29" x="0" y="71.12" visible="pin" length="short"/>
<pin name="30" x="0" y="73.66" visible="pin" length="short"/>
<pin name="31" x="0" y="76.2" visible="pin" length="short"/>
<pin name="32" x="0" y="78.74" visible="pin" length="short"/>
<wire x1="2.54" y1="0" x2="2.54" y2="78.74" width="0.254" layer="94"/>
<text x="0" y="81.28" size="1.778" layer="95">&gt;NAME</text>
</symbol>
<symbol name="D01-9920146">
<pin name="1" x="0" y="0" visible="pin" length="short"/>
<text x="0" y="2.54" size="1.778" layer="95">&gt;NAME</text>
</symbol>
</symbols>
<devicesets>
<deviceset name="D01-9923246" prefix="H32.">
<gates>
<gate name="G$1" symbol="D01-9923246" x="0" y="0"/>
</gates>
<devices>
<device name="" package="D01-9923246">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="10" pad="10"/>
<connect gate="G$1" pin="11" pad="11"/>
<connect gate="G$1" pin="12" pad="12"/>
<connect gate="G$1" pin="13" pad="13"/>
<connect gate="G$1" pin="14" pad="14"/>
<connect gate="G$1" pin="15" pad="15"/>
<connect gate="G$1" pin="16" pad="16"/>
<connect gate="G$1" pin="17" pad="17"/>
<connect gate="G$1" pin="18" pad="18"/>
<connect gate="G$1" pin="19" pad="19"/>
<connect gate="G$1" pin="2" pad="2"/>
<connect gate="G$1" pin="20" pad="20"/>
<connect gate="G$1" pin="21" pad="21"/>
<connect gate="G$1" pin="22" pad="22"/>
<connect gate="G$1" pin="23" pad="23"/>
<connect gate="G$1" pin="24" pad="24"/>
<connect gate="G$1" pin="25" pad="25"/>
<connect gate="G$1" pin="26" pad="26"/>
<connect gate="G$1" pin="27" pad="27"/>
<connect gate="G$1" pin="28" pad="28"/>
<connect gate="G$1" pin="29" pad="29"/>
<connect gate="G$1" pin="3" pad="3"/>
<connect gate="G$1" pin="30" pad="30"/>
<connect gate="G$1" pin="31" pad="31"/>
<connect gate="G$1" pin="32" pad="32"/>
<connect gate="G$1" pin="4" pad="4"/>
<connect gate="G$1" pin="5" pad="5"/>
<connect gate="G$1" pin="6" pad="6"/>
<connect gate="G$1" pin="7" pad="7"/>
<connect gate="G$1" pin="8" pad="8"/>
<connect gate="G$1" pin="9" pad="9"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="D01-9920146" prefix="H1.">
<gates>
<gate name="G$1" symbol="D01-9920146" x="0" y="0"/>
</gates>
<devices>
<device name="" package="D01-9920146">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
</libraries>
<attributes>
</attributes>
<variantdefs>
</variantdefs>
<classes>
<class number="0" name="default" width="0" drill="0">
</class>
</classes>
<parts>
<part name="FRAME1" library="frames" deviceset="A4-35SC" device=""/>
<part name="H1" library="con-headers-harvin" deviceset="D01-9923246" device=""/>
<part name="H2" library="con-headers-harvin" deviceset="D01-9923246" device=""/>
<part name="BC" library="con-headers-harvin" deviceset="D01-9920146" device=""/>
<part name="8X1" library="pv-measurement-array" deviceset="8X8-POGO" device=""/>
</parts>
<sheets>
<sheet>
<plain>
</plain>
<instances>
<instance part="FRAME1" gate="G$1" x="0" y="0"/>
<instance part="H1" gate="G$1" x="35.56" y="233.68" smashed="yes" rot="R180">
<attribute name="NAME" x="33.02" y="236.22" size="1.778" layer="95"/>
</instance>
<instance part="H2" gate="G$1" x="149.86" y="203.2" smashed="yes" rot="MR180">
<attribute name="NAME" x="152.4" y="205.74" size="1.778" layer="95" rot="MR0"/>
</instance>
<instance part="BC" gate="G$1" x="35.56" y="147.32" smashed="yes" rot="R180">
<attribute name="NAME" x="33.02" y="149.86" size="1.778" layer="95"/>
</instance>
<instance part="8X1" gate="G$1" x="66.04" y="177.8"/>
</instances>
<busses>
<bus name="P[11..18]">
<segment>
<wire x1="40.64" y1="233.68" x2="40.64" y2="215.9" width="0.762" layer="92"/>
<wire x1="40.64" y1="233.68" x2="119.38" y2="233.68" width="0.762" layer="92"/>
</segment>
</bus>
<bus name="P[21..28]">
<segment>
<wire x1="45.72" y1="226.06" x2="45.72" y2="195.58" width="0.762" layer="92"/>
<wire x1="45.72" y1="226.06" x2="119.38" y2="226.06" width="0.762" layer="92"/>
</segment>
</bus>
<bus name="P[31..38]">
<segment>
<wire x1="50.8" y1="175.26" x2="50.8" y2="218.44" width="0.762" layer="92"/>
<wire x1="50.8" y1="218.44" x2="119.38" y2="218.44" width="0.762" layer="92"/>
</segment>
</bus>
<bus name="P[41..48]">
<segment>
<wire x1="55.88" y1="154.94" x2="55.88" y2="210.82" width="0.762" layer="92"/>
<wire x1="55.88" y1="210.82" x2="119.38" y2="210.82" width="0.762" layer="92"/>
</segment>
</bus>
<bus name="P[51..58]">
<segment>
<wire x1="144.78" y1="203.2" x2="144.78" y2="185.42" width="0.762" layer="92"/>
<wire x1="144.78" y1="203.2" x2="66.04" y2="203.2" width="0.762" layer="92"/>
</segment>
</bus>
<bus name="P[61..68]">
<segment>
<wire x1="139.7" y1="195.58" x2="139.7" y2="165.1" width="0.762" layer="92"/>
<wire x1="139.7" y1="195.58" x2="66.04" y2="195.58" width="0.762" layer="92"/>
</segment>
</bus>
<bus name="P[71..78]">
<segment>
<wire x1="134.62" y1="144.78" x2="134.62" y2="187.96" width="0.762" layer="92"/>
<wire x1="134.62" y1="187.96" x2="66.04" y2="187.96" width="0.762" layer="92"/>
</segment>
</bus>
<bus name="P[81..88]">
<segment>
<wire x1="129.54" y1="124.46" x2="129.54" y2="180.34" width="0.762" layer="92"/>
<wire x1="129.54" y1="180.34" x2="66.04" y2="180.34" width="0.762" layer="92"/>
</segment>
</bus>
</busses>
<nets>
<net name="P11" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="1"/>
<wire x1="35.56" y1="233.68" x2="40.64" y2="233.68" width="0.1524" layer="91"/>
<label x="35.56" y="233.68" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="11"/>
<wire x1="66.04" y1="233.68" x2="66.04" y2="231.14" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P12" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="2"/>
<wire x1="35.56" y1="231.14" x2="40.64" y2="231.14" width="0.1524" layer="91"/>
<label x="35.56" y="231.14" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="12"/>
<wire x1="73.66" y1="233.68" x2="73.66" y2="231.14" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P13" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="3"/>
<wire x1="35.56" y1="228.6" x2="40.64" y2="228.6" width="0.1524" layer="91"/>
<label x="35.56" y="228.6" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="13"/>
<wire x1="81.28" y1="233.68" x2="81.28" y2="231.14" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P14" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="4"/>
<wire x1="35.56" y1="226.06" x2="40.64" y2="226.06" width="0.1524" layer="91"/>
<label x="35.56" y="226.06" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="14"/>
<wire x1="88.9" y1="233.68" x2="88.9" y2="231.14" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P15" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="5"/>
<wire x1="35.56" y1="223.52" x2="40.64" y2="223.52" width="0.1524" layer="91"/>
<label x="35.56" y="223.52" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="15"/>
<wire x1="96.52" y1="233.68" x2="96.52" y2="231.14" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P16" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="6"/>
<wire x1="35.56" y1="220.98" x2="40.64" y2="220.98" width="0.1524" layer="91"/>
<label x="35.56" y="220.98" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="16"/>
<wire x1="104.14" y1="233.68" x2="104.14" y2="231.14" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P17" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="7"/>
<wire x1="35.56" y1="218.44" x2="40.64" y2="218.44" width="0.1524" layer="91"/>
<label x="35.56" y="218.44" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="17"/>
<wire x1="111.76" y1="233.68" x2="111.76" y2="231.14" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P18" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="8"/>
<wire x1="35.56" y1="215.9" x2="40.64" y2="215.9" width="0.1524" layer="91"/>
<label x="35.56" y="215.9" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="18"/>
<wire x1="119.38" y1="233.68" x2="119.38" y2="231.14" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P21" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="9"/>
<wire x1="35.56" y1="213.36" x2="45.72" y2="213.36" width="0.1524" layer="91"/>
<label x="35.56" y="213.36" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="21"/>
<wire x1="66.04" y1="226.06" x2="66.04" y2="223.52" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P22" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="10"/>
<wire x1="35.56" y1="210.82" x2="45.72" y2="210.82" width="0.1524" layer="91"/>
<label x="35.56" y="210.82" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="22"/>
<wire x1="73.66" y1="226.06" x2="73.66" y2="223.52" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P23" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="11"/>
<wire x1="35.56" y1="208.28" x2="45.72" y2="208.28" width="0.1524" layer="91"/>
<label x="35.56" y="208.28" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="23"/>
<wire x1="81.28" y1="226.06" x2="81.28" y2="223.52" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P24" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="12"/>
<wire x1="35.56" y1="205.74" x2="45.72" y2="205.74" width="0.1524" layer="91"/>
<label x="35.56" y="205.74" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="24"/>
<wire x1="88.9" y1="226.06" x2="88.9" y2="223.52" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P25" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="13"/>
<wire x1="35.56" y1="203.2" x2="45.72" y2="203.2" width="0.1524" layer="91"/>
<label x="35.56" y="203.2" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="25"/>
<wire x1="96.52" y1="226.06" x2="96.52" y2="223.52" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P26" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="14"/>
<wire x1="35.56" y1="200.66" x2="45.72" y2="200.66" width="0.1524" layer="91"/>
<label x="35.56" y="200.66" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="26"/>
<wire x1="104.14" y1="226.06" x2="104.14" y2="223.52" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P27" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="15"/>
<wire x1="35.56" y1="198.12" x2="45.72" y2="198.12" width="0.1524" layer="91"/>
<label x="35.56" y="198.12" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="27"/>
<wire x1="111.76" y1="226.06" x2="111.76" y2="223.52" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P28" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="16"/>
<wire x1="35.56" y1="195.58" x2="45.72" y2="195.58" width="0.1524" layer="91"/>
<label x="35.56" y="195.58" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="28"/>
<wire x1="119.38" y1="226.06" x2="119.38" y2="223.52" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P31" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="17"/>
<wire x1="35.56" y1="193.04" x2="50.8" y2="193.04" width="0.1524" layer="91"/>
<label x="35.56" y="193.04" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="31"/>
<wire x1="66.04" y1="218.44" x2="66.04" y2="215.9" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P32" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="18"/>
<wire x1="35.56" y1="190.5" x2="50.8" y2="190.5" width="0.1524" layer="91"/>
<label x="35.56" y="190.5" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="32"/>
<wire x1="73.66" y1="218.44" x2="73.66" y2="215.9" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P33" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="19"/>
<wire x1="35.56" y1="187.96" x2="50.8" y2="187.96" width="0.1524" layer="91"/>
<label x="35.56" y="187.96" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="33"/>
<wire x1="81.28" y1="218.44" x2="81.28" y2="215.9" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P34" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="20"/>
<wire x1="35.56" y1="185.42" x2="50.8" y2="185.42" width="0.1524" layer="91"/>
<label x="35.56" y="185.42" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="34"/>
<wire x1="88.9" y1="218.44" x2="88.9" y2="215.9" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P35" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="21"/>
<wire x1="35.56" y1="182.88" x2="50.8" y2="182.88" width="0.1524" layer="91"/>
<label x="35.56" y="182.88" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="35"/>
<wire x1="96.52" y1="218.44" x2="96.52" y2="215.9" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P36" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="22"/>
<wire x1="35.56" y1="180.34" x2="50.8" y2="180.34" width="0.1524" layer="91"/>
<label x="35.56" y="180.34" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="36"/>
<wire x1="104.14" y1="218.44" x2="104.14" y2="215.9" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P37" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="23"/>
<wire x1="35.56" y1="177.8" x2="50.8" y2="177.8" width="0.1524" layer="91"/>
<label x="35.56" y="177.8" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="37"/>
<wire x1="111.76" y1="218.44" x2="111.76" y2="215.9" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P38" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="24"/>
<wire x1="35.56" y1="175.26" x2="50.8" y2="175.26" width="0.1524" layer="91"/>
<label x="35.56" y="175.26" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="38"/>
<wire x1="119.38" y1="218.44" x2="119.38" y2="215.9" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P41" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="25"/>
<wire x1="35.56" y1="172.72" x2="55.88" y2="172.72" width="0.1524" layer="91"/>
<label x="35.56" y="172.72" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="41"/>
<wire x1="66.04" y1="210.82" x2="66.04" y2="208.28" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P42" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="26"/>
<wire x1="35.56" y1="170.18" x2="55.88" y2="170.18" width="0.1524" layer="91"/>
<label x="35.56" y="170.18" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="42"/>
<wire x1="73.66" y1="210.82" x2="73.66" y2="208.28" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P43" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="27"/>
<wire x1="35.56" y1="167.64" x2="55.88" y2="167.64" width="0.1524" layer="91"/>
<label x="35.56" y="167.64" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="43"/>
<wire x1="81.28" y1="210.82" x2="81.28" y2="208.28" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P44" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="28"/>
<wire x1="35.56" y1="165.1" x2="55.88" y2="165.1" width="0.1524" layer="91"/>
<label x="35.56" y="165.1" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="44"/>
<wire x1="88.9" y1="210.82" x2="88.9" y2="208.28" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P45" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="29"/>
<wire x1="35.56" y1="162.56" x2="55.88" y2="162.56" width="0.1524" layer="91"/>
<label x="35.56" y="162.56" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="45"/>
<wire x1="96.52" y1="210.82" x2="96.52" y2="208.28" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P46" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="30"/>
<wire x1="35.56" y1="160.02" x2="55.88" y2="160.02" width="0.1524" layer="91"/>
<label x="35.56" y="160.02" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="46"/>
<wire x1="104.14" y1="210.82" x2="104.14" y2="208.28" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P47" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="31"/>
<wire x1="35.56" y1="157.48" x2="55.88" y2="157.48" width="0.1524" layer="91"/>
<label x="35.56" y="157.48" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="47"/>
<wire x1="111.76" y1="210.82" x2="111.76" y2="208.28" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P48" class="0">
<segment>
<pinref part="H1" gate="G$1" pin="32"/>
<wire x1="35.56" y1="154.94" x2="55.88" y2="154.94" width="0.1524" layer="91"/>
<label x="35.56" y="154.94" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="48"/>
<wire x1="119.38" y1="210.82" x2="119.38" y2="208.28" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P51" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="1"/>
<wire x1="149.86" y1="203.2" x2="144.78" y2="203.2" width="0.1524" layer="91"/>
<label x="144.78" y="203.2" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="51"/>
<wire x1="66.04" y1="203.2" x2="66.04" y2="200.66" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P52" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="2"/>
<wire x1="149.86" y1="200.66" x2="144.78" y2="200.66" width="0.1524" layer="91"/>
<label x="144.78" y="200.66" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="52"/>
<wire x1="73.66" y1="203.2" x2="73.66" y2="200.66" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P53" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="3"/>
<wire x1="149.86" y1="198.12" x2="144.78" y2="198.12" width="0.1524" layer="91"/>
<label x="144.78" y="198.12" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="53"/>
<wire x1="81.28" y1="203.2" x2="81.28" y2="200.66" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P54" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="4"/>
<wire x1="149.86" y1="195.58" x2="144.78" y2="195.58" width="0.1524" layer="91"/>
<label x="144.78" y="195.58" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="54"/>
<wire x1="88.9" y1="203.2" x2="88.9" y2="200.66" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P55" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="5"/>
<wire x1="149.86" y1="193.04" x2="144.78" y2="193.04" width="0.1524" layer="91"/>
<label x="144.78" y="193.04" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="55"/>
<wire x1="96.52" y1="203.2" x2="96.52" y2="200.66" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P56" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="6"/>
<wire x1="149.86" y1="190.5" x2="144.78" y2="190.5" width="0.1524" layer="91"/>
<label x="144.78" y="190.5" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="56"/>
<wire x1="104.14" y1="203.2" x2="104.14" y2="200.66" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P57" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="7"/>
<wire x1="149.86" y1="187.96" x2="144.78" y2="187.96" width="0.1524" layer="91"/>
<label x="144.78" y="187.96" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="57"/>
<wire x1="111.76" y1="203.2" x2="111.76" y2="200.66" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P58" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="8"/>
<wire x1="149.86" y1="185.42" x2="144.78" y2="185.42" width="0.1524" layer="91"/>
<label x="144.78" y="185.42" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="58"/>
<wire x1="119.38" y1="203.2" x2="119.38" y2="200.66" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P61" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="9"/>
<wire x1="149.86" y1="182.88" x2="139.7" y2="182.88" width="0.1524" layer="91"/>
<label x="144.78" y="182.88" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="61"/>
<wire x1="66.04" y1="195.58" x2="66.04" y2="193.04" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P62" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="10"/>
<wire x1="149.86" y1="180.34" x2="139.7" y2="180.34" width="0.1524" layer="91"/>
<label x="144.78" y="180.34" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="62"/>
<wire x1="73.66" y1="195.58" x2="73.66" y2="193.04" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P63" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="11"/>
<wire x1="149.86" y1="177.8" x2="139.7" y2="177.8" width="0.1524" layer="91"/>
<label x="144.78" y="177.8" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="63"/>
<wire x1="81.28" y1="195.58" x2="81.28" y2="193.04" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P64" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="12"/>
<wire x1="149.86" y1="175.26" x2="139.7" y2="175.26" width="0.1524" layer="91"/>
<label x="144.78" y="175.26" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="64"/>
<wire x1="88.9" y1="195.58" x2="88.9" y2="193.04" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P65" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="13"/>
<wire x1="149.86" y1="172.72" x2="139.7" y2="172.72" width="0.1524" layer="91"/>
<label x="144.78" y="172.72" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="65"/>
<wire x1="96.52" y1="195.58" x2="96.52" y2="193.04" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P66" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="14"/>
<wire x1="149.86" y1="170.18" x2="139.7" y2="170.18" width="0.1524" layer="91"/>
<label x="144.78" y="170.18" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="66"/>
<wire x1="104.14" y1="195.58" x2="104.14" y2="193.04" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P67" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="15"/>
<wire x1="149.86" y1="167.64" x2="139.7" y2="167.64" width="0.1524" layer="91"/>
<label x="144.78" y="167.64" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="67"/>
<wire x1="111.76" y1="195.58" x2="111.76" y2="193.04" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P68" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="16"/>
<wire x1="149.86" y1="165.1" x2="139.7" y2="165.1" width="0.1524" layer="91"/>
<label x="144.78" y="165.1" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="68"/>
<wire x1="119.38" y1="195.58" x2="119.38" y2="193.04" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P71" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="17"/>
<wire x1="149.86" y1="162.56" x2="134.62" y2="162.56" width="0.1524" layer="91"/>
<label x="144.78" y="162.56" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="71"/>
<wire x1="66.04" y1="187.96" x2="66.04" y2="185.42" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P72" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="18"/>
<wire x1="149.86" y1="160.02" x2="134.62" y2="160.02" width="0.1524" layer="91"/>
<label x="144.78" y="160.02" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="72"/>
<wire x1="73.66" y1="187.96" x2="73.66" y2="185.42" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P73" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="19"/>
<wire x1="149.86" y1="157.48" x2="134.62" y2="157.48" width="0.1524" layer="91"/>
<label x="144.78" y="157.48" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="73"/>
<wire x1="81.28" y1="187.96" x2="81.28" y2="185.42" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P74" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="20"/>
<wire x1="149.86" y1="154.94" x2="134.62" y2="154.94" width="0.1524" layer="91"/>
<label x="144.78" y="154.94" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="74"/>
<wire x1="88.9" y1="187.96" x2="88.9" y2="185.42" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P75" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="21"/>
<wire x1="149.86" y1="152.4" x2="134.62" y2="152.4" width="0.1524" layer="91"/>
<label x="144.78" y="152.4" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="75"/>
<wire x1="96.52" y1="187.96" x2="96.52" y2="185.42" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P76" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="22"/>
<wire x1="149.86" y1="149.86" x2="134.62" y2="149.86" width="0.1524" layer="91"/>
<label x="144.78" y="149.86" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="76"/>
<wire x1="104.14" y1="187.96" x2="104.14" y2="185.42" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P77" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="23"/>
<wire x1="149.86" y1="147.32" x2="134.62" y2="147.32" width="0.1524" layer="91"/>
<label x="144.78" y="147.32" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="77"/>
<wire x1="111.76" y1="187.96" x2="111.76" y2="185.42" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P78" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="24"/>
<wire x1="149.86" y1="144.78" x2="134.62" y2="144.78" width="0.1524" layer="91"/>
<label x="144.78" y="144.78" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="78"/>
<wire x1="119.38" y1="187.96" x2="119.38" y2="185.42" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P81" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="25"/>
<wire x1="149.86" y1="142.24" x2="129.54" y2="142.24" width="0.1524" layer="91"/>
<label x="144.78" y="142.24" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="81"/>
<wire x1="66.04" y1="180.34" x2="66.04" y2="177.8" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P82" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="26"/>
<wire x1="149.86" y1="139.7" x2="129.54" y2="139.7" width="0.1524" layer="91"/>
<label x="144.78" y="139.7" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="82"/>
<wire x1="73.66" y1="180.34" x2="73.66" y2="177.8" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P83" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="27"/>
<wire x1="149.86" y1="137.16" x2="129.54" y2="137.16" width="0.1524" layer="91"/>
<label x="144.78" y="137.16" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="83"/>
<wire x1="81.28" y1="180.34" x2="81.28" y2="177.8" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P84" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="28"/>
<wire x1="149.86" y1="134.62" x2="129.54" y2="134.62" width="0.1524" layer="91"/>
<label x="144.78" y="134.62" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="84"/>
<wire x1="88.9" y1="180.34" x2="88.9" y2="177.8" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P85" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="29"/>
<wire x1="149.86" y1="132.08" x2="129.54" y2="132.08" width="0.1524" layer="91"/>
<label x="144.78" y="132.08" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="85"/>
<wire x1="96.52" y1="180.34" x2="96.52" y2="177.8" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P86" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="30"/>
<wire x1="149.86" y1="129.54" x2="129.54" y2="129.54" width="0.1524" layer="91"/>
<label x="144.78" y="129.54" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="86"/>
<wire x1="104.14" y1="180.34" x2="104.14" y2="177.8" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P87" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="31"/>
<wire x1="149.86" y1="127" x2="129.54" y2="127" width="0.1524" layer="91"/>
<label x="144.78" y="127" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="87"/>
<wire x1="111.76" y1="180.34" x2="111.76" y2="177.8" width="0.1524" layer="91"/>
</segment>
</net>
<net name="P88" class="0">
<segment>
<pinref part="H2" gate="G$1" pin="32"/>
<wire x1="149.86" y1="124.46" x2="129.54" y2="124.46" width="0.1524" layer="91"/>
<label x="144.78" y="124.46" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="8X1" gate="G$1" pin="88"/>
<wire x1="119.38" y1="180.34" x2="119.38" y2="177.8" width="0.1524" layer="91"/>
</segment>
</net>
<net name="BC" class="0">
<segment>
<pinref part="BC" gate="G$1" pin="1"/>
<pinref part="8X1" gate="G$1" pin="B"/>
<wire x1="35.56" y1="147.32" x2="60.96" y2="147.32" width="0.1524" layer="91"/>
<wire x1="60.96" y1="147.32" x2="60.96" y2="172.72" width="0.1524" layer="91"/>
</segment>
</net>
</nets>
</sheet>
</sheets>
<errors>
<approved hash="113,1,92.606,131.976,FRAME1,,,,,"/>
</errors>
</schematic>
</drawing>
</eagle>
