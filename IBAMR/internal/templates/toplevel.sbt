<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeSystem Version="2">
  <!-- Attribute Definitions-->
  <Definitions>
    <AttDef Type="toplevel" Label="Top Level" BaseType="" Version="0">
      <ItemDefinitions>
        <!-- Next 4 value originally from bottom of geometry-->
        <Double Name="mfac" Label="MFAC" Optional="true" IsEnabledByDefault="false">
          <BriefDescription>ratio of structural mesh width to Cartesian mesh width</BriefDescription>
          <DefaultValue>2.0</DefaultValue>
          <RangeInfo>
            <Min Inclusive="false">0.0</Min>
          </RangeInfo>
        </Double>
        <String Name="element-type" Label="Element Type">
          <DiscreteInfo DefaultIndex="1">
            <Value>TRI3</Value>
            <Value>TRI6</Value>
            <Value>QUAD4</Value>
            <Value>QUAD8</Value>
            <Value>QUAD9</Value>
          </DiscreteInfo>
        </String>
        <Int Name="pk1-dev-quad-order" Label="Quadrature Rule Order for Deviatoric Stress">
          <DefaultValue>5</DefaultValue>
          <RangeInfo>
            <Min Inclusive="true">0</Min>
            <Max Inclusive="true">43</Max>
          </RangeInfo>
        </Int>
        <Int Name="pk1-dil-quad-order" Label="Quadrature Rule Order for Dilational Stress">
          <DefaultValue>3</DefaultValue>
          <RangeInfo>
            <Min Inclusive="true">0</Min>
            <Max Inclusive="true">43</Max>
          </RangeInfo>
        </Int>
      </ItemDefinitions>
    </AttDef>
  </Definitions>
</SMTK_AttributeSystem>
