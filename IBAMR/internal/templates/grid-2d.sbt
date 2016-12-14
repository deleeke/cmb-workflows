<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeSystem Version="2">
  <!-- Attribute Definitions-->
  <Definitions>
    <AttDef Type="geometry" Label="Geometry" BaseType="" Version="0">
      <ItemDefinitions>
        <Double Name="origin" Label="Lower Left Corner" Version="0" NumberOfRequiredValues="2">
          <BriefDescription>physical location of the lower left corner</BriefDescription>
          <ComponentLabels>
            <Label>x:</Label>
            <Label>y:</Label>
          </ComponentLabels>
          <DefaultValue>0.0</DefaultValue>
        </Double>
        <Double Name="length" Label="Physical Length" Version="0" NumberOfRequiredValues="2">
          <BriefDescription>physical size of the geometry domain</BriefDescription>
          <ComponentLabels>
            <Label>x:</Label>
            <Label>y:</Label>
          </ComponentLabels>
          <DefaultValue>1.0</DefaultValue>
          <RangeInfo>
            <Min Inclusive="false">0.0</Min>
          </RangeInfo>
        </Double>
        <Int Name="periodic" Label="Periodic?" NumberOfRequiredValues="2">
          <ComponentLabels>
            <Label>x:</Label>
            <Label>y:</Label>
          </ComponentLabels>
          <DiscreteInfo DefaultIndex="0">
            <Value Enum="No">0</Value>
            <Value Enum="Yes">1</Value>
          </DiscreteInfo>
        </Int>
      </ItemDefinitions>
    </AttDef>
    <AttDef Type="grid" Label="Grid" BaseType="" Version="0">
      <ItemDefinitions>
        <Int Name="base-grid-size" Label="Base Grid Size" Version="0" NumberOfRequiredValues="2">
          <BriefDescription>number of grid cells at the base/coarsest refinement level</BriefDescription>
          <ComponentLabels>
            <Label>x:</Label>
            <Label>y:</Label>
          </ComponentLabels>
          <DefaultValue>64</DefaultValue>
          <RangeInfo>
            <Min Inclusive="true">1</Min>
          </RangeInfo>
        </Int>
        <Int Name="max-levels" Label="Maximum Levels" Version="0">
          <DefaultValue>1</DefaultValue>
          <RangeInfo>
            <Min Inclusive="true">1</Min>
          </RangeInfo>
        </Int>
        <!-- Define refinement ratio as string, to indicate whether itis specified as a single value ("fixed") or table of values
        -->
        <String Name="refinement-ratio" Label="Refinement Ratio">
          <ChildrenDefinitions>
            <Int Name="fixed" Label="Fixed Refinement Ratio">
              <BriefDescription>Recommended values of 2 or 4 (effective for every level)</BriefDescription>
              <DefaultValue>2</DefaultValue>
              <RangeInfo>
                <Min Inclusive="true">1</Min>
              </RangeInfo>
            </Int>
            <Group Name="table" Label="General Refinement Ratio" Extensible="true" NumberOfRequiredGroups="1">
              <ItemDefinitions>
                <Int Name="row" Label="Refinement Ratio" NumberOfRequiredValues="2">
                  <ComponentLabels>
                    <Label>x:</Label>
                    <Label>y:</Label>
                  </ComponentLabels>
                  <DefaultValue>2</DefaultValue>
                  <RangeInfo>
                    <Min Inclusive="true">1</Min>
                  </RangeInfo>
                </Int>
              </ItemDefinitions>
            </Group>
          </ChildrenDefinitions>
          <DiscreteInfo DefaultIndex="0">
            <Structure>
              <Value Enum="Fixed Value">fixed</Value>
              <Items>
                <Item>fixed</Item>
              </Items>
            </Structure>
            <Structure>
              <Value Enum="General">table</Value>
              <Items>
                <Item>table</Item>
              </Items>
            </Structure>
          </DiscreteInfo>
        </String>
        <!-- largest-patch-size follows *exact* same patten as refinement ratio-->
        <String Name="largest-patch-size" Label="Largest Patch Size">
          <ChildrenDefinitions>
            <Int Name="fixed" Label="Fixed Value">
              <DefaultValue>2</DefaultValue>
              <RangeInfo>
                <Min Inclusive="true">1</Min>
              </RangeInfo>
            </Int>
            <Group Name="table" Label="Table" Extensible="true" NumberOfRequiredGroups="1">
              <ItemDefinitions>
                <Int Name="row" Label="Largest Patch Size" NumberOfRequiredValues="2">
                  <ComponentLabels>
                    <Label>x:</Label>
                    <Label>y:</Label>
                  </ComponentLabels>
                  <DefaultValue>2</DefaultValue>
                  <RangeInfo>
                    <Min Inclusive="true">1</Min>
                  </RangeInfo>
                </Int>
              </ItemDefinitions>
            </Group>
          </ChildrenDefinitions>
          <DiscreteInfo DefaultIndex="0">
            <Structure>
              <Value Enum="Fixed Value">fixed</Value>
              <Items>
                <Item>fixed</Item>
              </Items>
            </Structure>
            <Structure>
              <Value Enum="General">table</Value>
              <Items>
                <Item>table</Item>
              </Items>
            </Structure>
          </DiscreteInfo>
        </String>
        <!-- smallest-patch-size follows *exact* same patten as refinement ratio-->
        <String Name="smallest-patch-size" Label="Smallest Patch Size">
          <ChildrenDefinitions>
            <Int Name="fixed" Label="Fixed Value">
              <DefaultValue>2</DefaultValue>
              <RangeInfo>
                <Min Inclusive="true">1</Min>
              </RangeInfo>
            </Int>
            <Group Name="table" Label="Table" Extensible="true" NumberOfRequiredGroups="1">
              <ItemDefinitions>
                <Int Name="row" Label="Smallest Patch Size" NumberOfRequiredValues="2">
                  <ComponentLabels>
                    <Label>x:</Label>
                    <Label>y:</Label>
                  </ComponentLabels>
                  <DefaultValue>2</DefaultValue>
                  <RangeInfo>
                    <Min Inclusive="true">1</Min>
                  </RangeInfo>
                </Int>
              </ItemDefinitions>
            </Group>
          </ChildrenDefinitions>
          <DiscreteInfo DefaultIndex="0">
            <Structure>
              <Value Enum="Fixed Value">fixed</Value>
              <Items>
                <Item>fixed</Item>
              </Items>
            </Structure>
            <Structure>
              <Value Enum="General">table</Value>
              <Items>
                <Item>table</Item>
              </Items>
            </Structure>
          </DiscreteInfo>
        </String>
        <!-- Next 4 values not currently used-->
        <!--        <Double Name="mfac" Label="MFAC" Optional="true" IsEnabledByDefault="false">
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
        </Int> -->
        <Double Name="efficiency-tolerance" Label="Efficiency Tolerance">
          <BriefDescription>min % of tag cells in new patch level</BriefDescription>
          <DefaultValue>0.85</DefaultValue>
          <RangeInfo>
            <Min Inclusive="true">0.0</Min>
            <Max Inclusive="true">1.0</Max>
          </RangeInfo>
        </Double>
        <Double Name="combine-efficiency" Label="Combine Efficiency">
          <BriefDescription>chop box is sum of volumes of smaller boxes &lt; efficiency * vol of large box</BriefDescription>
          <DefaultValue>0.85</DefaultValue>
          <RangeInfo>
            <Min Inclusive="true">0.0</Min>
            <Max Inclusive="true">1.0</Max>
          </RangeInfo>
        </Double>
      </ItemDefinitions>
    </AttDef>
  </Definitions>
</SMTK_AttributeSystem>
