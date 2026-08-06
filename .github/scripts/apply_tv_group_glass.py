from pathlib import Path

widgets = Path('1080i/Includes_Widgets.xml')
text = widgets.read_text(encoding='utf-8')

expression = '''
    <!-- Detect folder items exposed by Kodi's TV channel-group root. -->
    <expression name="HomeWidgetIsPVRChannelGroup">ListItem.IsFolder + [String.StartsWith(ListItem.Path,pvr://channels/tv/) | String.StartsWith(ListItem.FolderPath,pvr://channels/tv/) | String.StartsWith(ListItem.FileNameAndPath,pvr://channels/tv/)]</expression>
'''
if 'name="HomeWidgetIsPVRChannelGroup"' not in text:
    text = text.replace('<includes>\n', '<includes>\n' + expression, 1)

landscape_old = '''        <control type="group">
            <height>$PARAM[height]</height>
            <top>$PARAM[top]</top>
            <control type="image">
                <left>10</left>
                <top>10</top>
                <right>10</right>
                <bottom>10</bottom>
                <aspectratio scalediffuse="false">scale</aspectratio>
                <texture flipy="true" diffuse="diffuse/listposter-ref-widgets.png" background="true">$VAR[LandscapeImage]</texture>
                <visible>$PARAM[reflections]</visible>
            </control>
        </control>
        <control type="group">
            <height>$PARAM[height]</height>
            <include content="def_widgetlandscape">
                <param name="indicatorbackground" value="$PARAM[indicatorbackground]" />
                <param name="small" value="$PARAM[small]"/>
                <param name="poster" value="$PARAM[poster]"/>
            </include>
            <include content="def_widgetfocus" condition="$PARAM[focused]">
                <param name="id" value="$PARAM[id]"/>
            </include>
        </control>'''

landscape_new = '''        <control type="group">
            <height>$PARAM[height]</height>
            <top>$PARAM[top]</top>
            <control type="image">
                <left>10</left>
                <top>10</top>
                <right>10</right>
                <bottom>10</bottom>
                <aspectratio scalediffuse="false">scale</aspectratio>
                <texture flipy="true" diffuse="diffuse/listposter-ref-widgets.png" background="true">$VAR[LandscapeImage]</texture>
                <visible>$PARAM[reflections]</visible>
                <visible>!$EXP[HomeWidgetIsPVRChannelGroup]</visible>
            </control>
        </control>
        <control type="group">
            <height>$PARAM[height]</height>
            <include content="def_widgetlandscape" condition="!$EXP[HomeWidgetIsPVRChannelGroup]">
                <param name="indicatorbackground" value="$PARAM[indicatorbackground]" />
                <param name="small" value="$PARAM[small]"/>
                <param name="poster" value="$PARAM[poster]"/>
            </include>
            <include content="def_widgetpvrchannelgroup" condition="$EXP[HomeWidgetIsPVRChannelGroup]">
                <param name="id" value="$PARAM[id]"/>
                <param name="focused" value="$PARAM[focused]"/>
            </include>
            <include content="def_widgetfocus" condition="$PARAM[focused] + !$EXP[HomeWidgetIsPVRChannelGroup]">
                <param name="id" value="$PARAM[id]"/>
            </include>
        </control>'''

if landscape_old not in text:
    raise SystemExit('Landscape include block not found or already changed unexpectedly')
text = text.replace(landscape_old, landscape_new, 1)

card_include = '''
    <!-- Compact glass card used only for PVR TV channel-group folder widgets. -->
    <include name="def_widgetpvrchannelgroup">
        <param name="focused" default="false"/>
        <definition>
        <control type="group">
            <left>10</left>
            <right>10</right>
            <top>38</top>
            <bottom>48</bottom>
            <animation effect="zoom" start="100" end="103" center="auto" time="150" reversible="true" condition="$PARAM[focused] + Control.HasFocus($PARAM[id])">Conditional</animation>
            <control type="image">
                <left>-8</left>
                <top>-8</top>
                <right>-8</right>
                <bottom>-8</bottom>
                <texture colordiffuse="88000000" border="18">common/rounded-shadow8.png</texture>
            </control>
            <control type="image">
                <texture colordiffuse="B2070B10" border="18" background="true">common/box.png</texture>
            </control>
            <control type="image">
                <left>1</left>
                <top>1</top>
                <right>1</right>
                <bottom>1</bottom>
                <texture colordiffuse="22FFFFFF" border="18" background="true" infill="false">common/box21.png</texture>
            </control>
            <control type="image">
                <left>24</left>
                <top>20</top>
                <right>24</right>
                <bottom>58</bottom>
                <aspectratio align="center" aligny="center" scalediffuse="false">keep</aspectratio>
                <texture background="true">$VAR[LandscapeImage]</texture>
            </control>
            <control type="image">
                <left>12</left>
                <right>12</right>
                <bottom>10</bottom>
                <height>48</height>
                <texture colordiffuse="66000000" border="12" background="true">common/box.png</texture>
            </control>
            <control type="label">
                <left>24</left>
                <right>24</right>
                <bottom>12</bottom>
                <height>42</height>
                <align>center</align>
                <aligny>center</aligny>
                <scroll>true</scroll>
                <font>SmallBold</font>
                <textcolor>PanelWhite100</textcolor>
                <selectedcolor>PanelWhite100</selectedcolor>
                <shadowcolor>CC000000</shadowcolor>
                <label>$INFO[ListItem.Label]</label>
            </control>
            <control type="image">
                <left>3</left>
                <top>3</top>
                <right>3</right>
                <bottom>3</bottom>
                <texture colordiffuse="$VAR[ColorHighlight]" border="20">common/selectbox.png</texture>
                <visible>$PARAM[focused] + Control.HasFocus($PARAM[id])</visible>
                <include>Animation.SelectBoxHome</include>
            </control>
            <control type="image">
                <left>3</left>
                <top>3</top>
                <right>3</right>
                <bottom>3</bottom>
                <texture colordiffuse="$VAR[ColorGradient]" border="20">common/gradient-selectbox.png</texture>
                <visible>$PARAM[focused] + Control.HasFocus($PARAM[id])</visible>
                <include>Animation.SelectBoxHome</include>
            </control>
        </control>
        </definition>
    </include>

'''
marker = '    <include name="def_widgetlandscape">'
if 'name="def_widgetpvrchannelgroup"' not in text:
    if marker not in text:
        raise SystemExit('def_widgetlandscape marker not found')
    text = text.replace(marker, card_include + marker, 1)
widgets.write_text(text, encoding='utf-8')

changelog = Path('CHANGELOG.md')
c = changelog.read_text(encoding='utf-8')
old = 'Aucune modification en attente : `develop` est alignée sur la dernière version stable.'
new = '''- nouveau rendu vitré et compact pour les widgets de groupes de chaînes TV ;
- fond sombre transparent, logos conservés sans étirement et nom du groupe intégré à la carte ;
- carte visuellement moins haute afin de laisser davantage apparaître l’arrière-plan ;
- focus cyan conservé, avec un léger agrandissement de la carte sélectionnée ;
- détection limitée aux dossiers `pvr://channels/tv/` afin de ne pas modifier les autres widgets paysage.'''
if old not in c:
    raise SystemExit('Unreleased changelog marker not found')
changelog.write_text(c.replace(old, new, 1), encoding='utf-8')

readme = Path('README.md')
r = readme.read_text(encoding='utf-8')
bullet = '- cartes vitrées compactes pour les groupes de chaînes TV sur `develop` ;\n'
anchor = '- navigation retravaillée entre le menu et les listes de widgets ;\n'
if bullet not in r:
    if anchor not in r:
        raise SystemExit('README insertion anchor not found')
    r = r.replace(anchor, anchor + bullet, 1)
readme.write_text(r, encoding='utf-8')

docs = Path('docs/THERAND_CUSTOMIZATIONS.md')
d = docs.read_text(encoding='utf-8')
d = d.replace('- Version stable restaurée et vérifiée : `3.19.11+25widgets.10`.', '- Version stable vérifiée : `3.19.11+25widgets.13`.')
d = d.replace('### Sous-menus — `develop`', '### Sous-menus')
d = d.replace('### Titres de sous-menu — `develop`', '### Titres de sous-menu')
tv_section = '''### Groupes de chaînes TV — `develop`

Les dossiers du widget `pvr://channels/tv/` utilisent une carte dédiée : fond vitré sombre et transparent, miniature conservée en proportions naturelles, nom du groupe intégré en bas et hauteur visuelle réduite. Le focus reprend volontairement la couleur d’accent actuelle du skin et applique un léger agrandissement. Les widgets paysage ordinaires et les chaînes individuelles ne sont pas modifiés.

'''
anchor = '### Titres par section\n'
if '### Groupes de chaînes TV — `develop`' not in d:
    if anchor not in d:
        raise SystemExit('Documentation insertion anchor not found')
    d = d.replace(anchor, tv_section + anchor, 1)
docs.write_text(d, encoding='utf-8')
