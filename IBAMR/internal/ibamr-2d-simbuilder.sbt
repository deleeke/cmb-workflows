<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeSystem Version="2">

  <!-- Category & Analysis specifications -->

  <!-- Attribute definitions -->
  <Includes>
    <File>templates/grid-2d.sbt</File>
    <File>templates/velocity-2d.sbt</File>
    <File>templates/solver.sbt</File>
    <File>templates/parameters.sbt</File>
    <File>templates/output.sbt</File>
    <File>templates/controls.sbt</File>
    <File>templates/toplevel.sbt</File>
  </Includes>

  <!-- View specifications -->
  <Views>
    <View Type="Group" Title="SimBuilder" TopLevel="true"
      FilterByAdvanceLevel="false" FilterByCategory="false">
      <Views>
        <View Title="Top Level" />
        <View Title="Grid"/>
        <View Title="BC"/>
        <View Title="Solver" />
        <View Title="Parameters" />
        <View Title="Output" />
        <View Title="Controls" />
      </Views>
    </View>

    <View Type="Instanced" Title="Grid">
      <InstancedAttributes>
        <Att Name="Geometry" Type="geometry" />
        <Att Name="Grid" Type="grid" />
      </InstancedAttributes>
    </View>

    <View Type="Group" Title="BC" Style="tiled">
      <Views>
        <View Title="Lower X" />
        <View Title="Upper X" />
        <View Title="Lower Y" />
        <View Title="Upper Y" />
      </Views>
    </View>
    <View Type="Instanced" Title="Lower X">
      <InstancedAttributes>
        <Att Name="velocity0" Type="velocity" />
      </InstancedAttributes>
    </View>
    <View Type="Instanced" Title="Upper X">
      <InstancedAttributes>
        <Att Name="velocity1" Type="velocity" />
      </InstancedAttributes>
    </View>
    <View Type="Instanced" Title="Lower Y">
      <InstancedAttributes>
        <Att Name="velocity2" Type="velocity" />
      </InstancedAttributes>
    </View>
    <View Type="Instanced" Title="Upper Y">
      <InstancedAttributes>
        <Att Name="velocity3" Type="velocity" />
      </InstancedAttributes>
    </View>

    <View Type="Instanced" Title="Solver">
      <InstancedAttributes>
        <Att Name="solver" Type="solver" />
      </InstancedAttributes>
    </View>

    <View Type="Instanced" Title="Parameters">
      <InstancedAttributes>
        <Att Name="parameters" Type="parameters" />
      </InstancedAttributes>
    </View>

    <View Type="Instanced" Title="Output">
      <InstancedAttributes>
        <Att Name="output" Type="output" />
      </InstancedAttributes>
    </View>

    <View Type="Instanced" Title="Controls">
      <InstancedAttributes>
        <Att Name="controls" Type="controls" />
      </InstancedAttributes>
    </View>
   
    <View Type="Instanced" Title="Top Level">
      <InstancedAttributes>
        <Att Name="toplevel" Type="toplevel" />
      </InstancedAttributes>
    </View>

  </Views>
</SMTK_AttributeSystem>
