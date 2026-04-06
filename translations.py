# -*- coding: utf-8 -*-
from qgis.core import QgsApplication

_strings_en = {
    "&Instant TPS": "&Magic Canopy Model Generator - UAV",
    "Magic Canopy Model Generator - UAV": "Magic Canopy Model Generator - UAV",
    "Capa MDS:": "DSM Layer:",
    "Marcar Puntos de Suelo Desnudo": "Mark Bare Soil Points",
    "↩ Deshacer Último": "↩ Undo Last",
    "Eliminar Seleccionado": "Delete Selected",
    "ID": "ID",
    "X": "X",
    "Y": "Y",
    "Z (Cota)": "Z (Elevation)",
    "💣 Eliminar Todos los Puntos": "💣 Clear All Points",
    "▶ Ejecutar Interpolación TPS": "▶ Run TPS Interpolation",
    "Listo.": "Ready.",
    "💾 Guardar productos (opcional — sin guardar quedan como capas temporales):": "💾 Save products (optional — will stay as temporary layers if unsaved):",
    "💾 MDT (Suelo)": "💾 DTM (Soil)",
    "💾 MAC (Altura)": "💾 CHM (Height)",
    "💾 MVC (Volumen)": "💾 CVM (Volume)",
    "Compresión (reduce el tamaño sin modificar datos):": "Compression (reduces file size without modifying data):",
    "DEFLATE (Muy alta compresión)": "DEFLATE (Very high compression)",
    "LZW (Compresión alta)": "LZW (High compression)",
    "Sin compresión": "No compression",
    "Magic Canopy Model Generator - UAV — Ayuda": "Magic Canopy Model Generator - UAV — Help",
    "Atención": "Attention",
    "Seleccioná una capa MDS primero.": "Please select a DSM layer first.",
    "📌 Clavando puntos en: {layer}": "📌 Marking points on: {layer}",
    "Error": "Error",
    "Primero ejecutá la interpolación.": "Run interpolation first.",
    "Guardar {name}": "Save {name}",
    "💾 Guardado: {name}": "💾 Saved: {name}",
    "La capa temporal fue eliminada de QGIS y no se pudo guardar.": "The temporary layer was removed from QGIS and could not be saved.",
    "Error Interno de QGIS": "Internal QGIS Error",
    "Falló la exportación nativa al disco (Código {}). ¿El archivo ya existe y está bloqueado o abieto?": "Native export to disk failed (Code {}). Does the file already exist and is locked or open?",
    "Error Crítico": "Critical Error",
    "Excepción durante el guardado: {}": "Exception during saving: {}",
    "scipy no está disponible.": "scipy is not available.",
    "Faltan puntos": "Not enough points",
    "Necesitás al menos 3 puntos.": "You need at least 3 points.",
    "Preparando interpolación...": "Preparing interpolation...",
    "Buscando suavizado óptimo (LOOCV)...": "Searching for optimal smoothing (LOOCV)...",
    "Interpolando TPS (λ={best_smooth})...": "Interpolating TPS (λ={best_smooth})...",
    "Interpolando filas {start}-{end}/{total}...": "Interpolating rows {start}-{end}/{total}...",
    "Calculando MAC y MVC...": "Calculating CHM and CVM...",
    "Cargando capas temporales...": "Loading temporary layers...",
    "✅ ¡Listo! 3 capas temporales generadas.": "✅ Done! 3 temporary layers generated.",
    "Error Fatal": "Fatal Error",

    """<html>
<h3 style="margin-top:0">📖 ¿Cómo funciona?</h3>

<p><b>1. Marcás puntos de suelo desnudo</b><br/>
Hacé clic en zonas donde el suelo es visible 
(caminos, bordes, entre-surcos). Cada clic 
registra la coordenada (X, Y) y la cota Z 
del pixel.</p>

<p><b>2. Se interpola el MDT</b><br/>
Se utiliza el algoritmo <b>Thin Plate Spline (TPS)</b> para interpolar los puntos de suelo marcados. El plugin optimiza automáticamente el parámetro de suavizado mediante <b>validación cruzada (LOOCV)</b> para asegurar que el modelo del terreno sea lo más preciso posible, incluso debajo de las plantas.</p>

<p><b>3. Se calcula el MAC</b><br/>
<b>MAC = MDS − MDT</b><br/>
(Modelo de Altura de Canopeo)<br/>
Al restar el suelo interpolado (MDT) del 
raster original (MDS), queda la <b>altura 
de todos los objetos</b> sobre el suelo 
(plantas, árboles, etc.). Valores negativos 
se fuerzan a 0.</p>

<p><b>4. Se calcula el MVC</b><br/>
<b>MVC = MAC × Área del pixel</b><br/>
(Modelo de Volumen de Canopeo)<br/>
Multiplica la altura de cada pixel por su 
resolución espacial (ej: 0.05m × 0.05m). 
Da el volumen de biomasa en m³ por pixel.</p>

<hr/>
<table border="1" cellpadding="3" cellspacing="0" style="font-size:10px">
<tr><th>Sigla</th><th>Español</th><th>English</th></tr>
<tr><td>MDS</td><td>Modelo Digital de Superficie</td><td>DSM</td></tr>
<tr><td>MDT</td><td>Modelo Digital de Terreno</td><td>DTM</td></tr>
<tr><td>MAC</td><td>Mod. Altura de Canopeo</td><td>CHM</td></tr>
<tr><td>MVC</td><td>Mod. Volumen de Canopeo</td><td>CVM</td></tr>
</table>
<p style="font-size:11px">Autor: <a href="mailto:menes.josefernando@inta.gob.ar">José Fernando Menes</a></p>
</html>""": """<html>
<h3 style="margin-top:0">📖 How it works</h3>

<p><b>1. Mark bare soil points</b><br/>
Click on areas where bare soil is visible 
(paths, borders, inter-rows). Each click 
records the (X, Y) coordinate and Z elevation.</p>

<p><b>2. DTM Interpolation</b><br/>
The <b>Thin Plate Spline (TPS)</b> algorithm is used to interpolate the marked soil points. The plugin automatically optimizes the smoothing parameter via <b>Leave-One-Out Cross-Validation (LOOCV)</b> to ensure the most accurate terrain model, even under plant cover.</p>

<p><b>3. CHM Calculation</b><br/>
<b>CHM = DSM − DTM</b><br/>
(Canopy Height Model)<br/>
By subtracting the interpolated soil (DTM) from 
the original raster (DSM), we get the <b>height 
of all objects</b> above ground (plants, trees, etc.). 
Negative values are forced to 0.</p>

<p><b>4. CVM Calculation</b><br/>
<b>CVM = CHM × Pixel area</b><br/>
(Canopy Volume Model)<br/>
Multiplies the height of each pixel by its 
spatial resolution. Yields biomass volume 
in m³ per pixel.</p>

<hr/>
<table border="1" cellpadding="3" cellspacing="0" style="font-size:10px">
<tr><th>Abbr</th><th>Español</th><th>English</th></tr>
<tr><td>DSM</td><td>Modelo Digital de Superficie</td><td>Digital Surface Model</td></tr>
<tr><td>DTM</td><td>Modelo Digital de Terreno</td><td>Digital Terrain Model</td></tr>
<tr><td>CHM</td><td>Mod. Altura de Canopeo</td><td>Canopy Height Model</td></tr>
<tr><td>CVM</td><td>Mod. Volumen de Canopeo</td><td>Canopy Volume Model</td></tr>
</table>
<p style="font-size:11px">Author: <a href="mailto:menes.josefernando@inta.gob.ar">José Fernando Menes</a></p>
</html>"""
}

_strings_pt = {
    "&Instant TPS": "&Magic Canopy Model Generator - UAV",
    "Magic Canopy Model Generator - UAV": "Magic Canopy Model Generator - UAV",
    "Capa MDS:": "Camada MDS:",
    "Marcar Puntos de Suelo Desnudo": "Marcar Pontos de Solo Exposto",
    "↩ Deshacer Último": "↩ Desfazer Último",
    "Eliminar Seleccionado": "Excluir Selecionado",
    "ID": "ID",
    "X": "X",
    "Y": "Y",
    "Z (Cota)": "Z (Elevação)",
    "💣 Eliminar Todos los Puntos": "💣 Limpar Todos os Pontos",
    "▶ Ejecutar Interpolación TPS": "▶ Executar Interpolação TPS",
    "Listo.": "Pronto.",
    "💾 Guardar productos (opcional — sin guardar quedan como capas temporales):": "💾 Salvar produtos (opcional — ficarão como temporárias se não salvos):",
    "💾 MDT (Suelo)": "💾 MDT (Solo)",
    "💾 MAC (Altura)": "💾 MAC (Altura)",
    "💾 MVC (Volumen)": "💾 MVC (Volume)",
    "Compresión (reduce el tamaño sin modificar datos):": "Compressão (reduz o tamanho sem modificar dados):",
    "DEFLATE (Muy alta compresión)": "DEFLATE (Compressão muito alta)",
    "LZW (Compresión alta)": "LZW (Compressão alta)",
    "Sin compresión": "Sem compressão",
    "Magic Canopy Model Generator - UAV — Ayuda": "Magic Canopy Model Generator - UAV — Ajuda",
    "Atención": "Atenção",
    "Seleccioná una capa MDS primero.": "Selecione uma camada MDS primeiro.",
    "📌 Clavando puntos en: {layer}": "📌 Marcando pontos na camada: {layer}",
    "Error": "Erro",
    "Primero ejecutá la interpolación.": "Execute a interpolação primeiro.",
    "Guardar {name}": "Salvar {name}",
    "💾 Guardado: {name}": "💾 Salvo: {name}",
    "La capa temporal fue eliminada de QGIS y no se pudo guardar.": "A camada temporária foi removida do QGIS e não pôde ser salva.",
    "Error Interno de QGIS": "Erro Interno do QGIS",
    "Falló la exportación nativa al disco (Código {}). ¿El archivo ya existe y está bloqueado o abieto?": "Falha na exportação nativa para o disco (Código {}). O arquivo já existe e está bloqueado ou aberto?",
    "Error Crítico": "Erro Crítico",
    "Excepción durante el guardado: {}": "Exceção ao salvar: {}",
    "scipy no está disponible.": "SciPy não está disponível.",
    "Faltan puntos": "Faltam pontos",
    "Necesitás al menos 3 puntos.": "Você precisa de pelo menos 3 pontos.",
    "Preparando interpolación...": "Preparando interpolação...",
    "Buscando suavizado óptimo (LOOCV)...": "Buscando suavização ideal (LOOCV)...",
    "Interpolando TPS (λ={best_smooth})...": "Interpolando TPS (λ={best_smooth})...",
    "Interpolando filas {start}-{end}/{total}...": "Interpolando linhas {start}-{end}/{total}...",
    "Calculando MAC y MVC...": "Calculando MAC e MVC...",
    "Cargando capas temporales...": "Carregando camadas temporárias...",
    "✅ ¡Listo! 3 capas temporales generadas.": "✅ Pronto! 3 camadas temporárias geradas.",
    "Error Fatal": "Erro Fatal",

    """<html>
<h3 style="margin-top:0">📖 ¿Cómo funciona?</h3>

<p><b>1. Marcás puntos de suelo desnudo</b><br/>
Hacé clic en zonas donde el suelo es visible 
(caminos, bordes, entre-surcos). Cada clic 
registra la coordenada (X, Y) y la cota Z 
del pixel.</p>

<p><b>2. Se interpola el MDT</b><br/>
Se utiliza el algoritmo <b>Thin Plate Spline (TPS)</b> para interpolar los puntos de suelo marcados. El plugin optimiza automáticamente el parámetro de suavizado mediante <b>validación cruzada (LOOCV)</b> para asegurar que el modelo del terreno sea lo más preciso posible, incluso debajo de las plantas.</p>

<p><b>3. Se calcula el MAC</b><br/>
<b>MAC = MDS − MDT</b><br/>
(Modelo de Altura de Canopeo)<br/>
Al restar el suelo interpolado (MDT) del 
raster original (MDS), queda la <b>altura 
de todos los objetos</b> sobre el suelo 
(plantas, árboles, etc.). Valores negativos 
se fuerzan a 0.</p>

<p><b>4. Se calcula el MVC</b><br/>
<b>MVC = MAC × Área del pixel</b><br/>
(Modelo de Volumen de Canopeo)<br/>
Multiplica la altura de cada pixel por su 
resolución espacial (ej: 0.05m × 0.05m). 
Da el volumen de biomasa en m³ por pixel.</p>

<hr/>
<table border="1" cellpadding="3" cellspacing="0" style="font-size:10px">
<tr><th>Sigla</th><th>Español</th><th>English</th></tr>
<tr><td>MDS</td><td>Modelo Digital de Superficie</td><td>DSM</td></tr>
<tr><td>MDT</td><td>Modelo Digital de Terreno</td><td>DTM</td></tr>
<tr><td>MAC</td><td>Mod. Altura de Canopeo</td><td>CHM</td></tr>
<tr><td>MVC</td><td>Mod. Volumen de Canopeo</td><td>CVM</td></tr>
</table>
<p style="font-size:11px">Autor: <a href="mailto:menes.josefernando@inta.gob.ar">José Fernando Menes</a></p>
</html>""": """<html>
<h3 style="margin-top:0">📖 Como funciona?</h3>

<p><b>1. Marcar pontos de solo exposto</b><br/>
Clique nas áreas onde o solo é visível 
(caminhos, bordas, entre-linhas). Cada clique 
registra a coordenada (X, Y) e a elevação Z.</p>

<p><b>2. Interpolação do MDT</b><br/>
O algoritmo <b>Thin Plate Spline (TPS)</b> é utilizado para interpolar os pontos de solo marcados. O plugin otimiza automaticamente o parâmetro de suavização via <b>validação cruzada (LOOCV)</b> para garantir que o modelo do terreno seja o mais preciso possível, mesmo sob as plantas.</p>

<p><b>3. Cálculo do MAC</b><br/>
<b>MAC = MDS − MDT</b><br/>
(Modelo de Altura do Dossel)<br/>
Subtraindo o solo interpolado (MDT) do 
raster original (MDS), obtemos a <b>altura 
de todos os objetos</b> acima do solo 
(plantas, árvores, etc.). Valores negativos 
são forçados a 0.</p>

<p><b>4. Cálculo do MVC</b><br/>
<b>MVC = MAC × Área do pixel</b><br/>
(Modelo de Volume do Dossel)<br/>
Multiplica a altura de cada pixel pela 
sua resolução espacial. Produz o volume 
de biomassa em m³ por pixel.</p>

<hr/>
<table border="1" cellpadding="3" cellspacing="0" style="font-size:10px">
<tr><th>Abrev</th><th>Español</th><th>Português</th></tr>
<tr><td>MDS</td><td>Modelo Digital de Superficie</td><td>Modelo Digital de Superfície</td></tr>
<tr><td>MDT</td><td>Modelo Digital de Terreno</td><td>Modelo Digital de Terreno</td></tr>
<tr><td>MAC</td><td>Mod. Altura de Canopeo</td><td>Modelo de Altura do Dossel</td></tr>
<tr><td>MVC</td><td>Mod. Volumen de Canopeo</td><td>Modelo de Volume do Dossel</td></tr>
</table>
<p style="font-size:11px">Autor: <a href="mailto:menes.josefernando@inta.gob.ar">José Fernando Menes</a></p>
</html>"""
}

_strings_zh = {
    "&Instant TPS": "&Magic Canopy Model Generator - UAV",
    "Magic Canopy Model Generator - UAV": "Magic Canopy Model Generator - UAV",
    "Capa MDS:": "DSM 图层:",
    "Marcar Puntos de Suelo Desnudo": "标记裸露地面点",
    "↩ Deshacer Último": "↩ 撤销上一步",
    "Eliminar Seleccionado": "删除已选",
    "ID": "ID",
    "X": "X",
    "Y": "Y",
    "Z (Cota)": "Z (高程)",
    "💣 Eliminar Todos los Puntos": "💣 清除所有点",
    "▶ Ejecutar Interpolación TPS": "▶ 运行 TPS 插值",
    "Listo.": "准备就绪。",
    "💾 Guardar productos (opcional — sin guardar quedan como capas temporales):": "💾 保存产品（可选 — 如果不保存将作为临时图层）:",
    "💾 MDT (Suelo)": "💾 MDT (土壤)",
    "💾 MAC (Altura)": "💾 MAC (高度)",
    "💾 MVC (Volumen)": "💾 MVC (体积)",
    "Compresión (reduce el tamaño sin modificar datos):": "压缩 (减小文件但不修改数据):",
    "DEFLATE (Muy alta compresión)": "DEFLATE (极高压缩率)",
    "LZW (Compresión alta)": "LZW (高压缩率)",
    "Sin compresión": "无压缩",
    "Magic Canopy Model Generator - UAV — Ayuda": "Magic Canopy Model Generator - UAV — 帮助",
    "Atención": "注意",
    "Seleccioná una capa MDS primero.": "请先选择一个 DSM 图层。",
    "📌 Clavando puntos en: {layer}": "📌 正在标记点: {layer}",
    "Error": "错误",
    "Primero ejecutá la interpolación.": "请先运行插值。",
    "Guardar {name}": "保存 {name}",
    "💾 Guardado: {name}": "💾 已保存: {name}",
    "La capa temporal fue eliminada de QGIS y no se pudo guardar.": "临时图层已从 QGIS 移除，无法保存。",
    "Error Interno de QGIS": "QGIS 内部错误",
    "Falló la exportación nativa al disco (Código {}). ¿El archivo ya existe y está bloqueado o abieto?": "导出失败 (代码 {})。文件是否已存在并且被锁定？",
    "Error Crítico": "严重错误",
    "Excepción durante el guardado: {}": "保存期间出现异常: {}",
    "scipy no está disponible.": "SciPy 不可用。",
    "Faltan puntos": "点数不足",
    "Necesitás al menos 3 puntos.": "您至少需要 3 个点。",
    "Preparando interpolación...": "正在准备插值...",
    "Buscando suavizado óptimo (LOOCV)...": "寻找最佳平滑参数 (LOOCV)...",
    "Interpolando TPS (λ={best_smooth})...": "正在进行 TPS 插值 (λ={best_smooth})...",
    "Interpolando filas {start}-{end}/{total}...": "正在插值行 {start}-{end}/{total}...",
    "Calculando MAC y MVC...": "正在计算 MAC 和 MVC...",
    "Cargando capas temporales...": "正在加载临时图层...",
    "✅ ¡Listo! 3 capas temporales generadas.": "✅ 完成！生成了 3 个临时图层。",
    "Error Fatal": "致命错误",

    """<html>
<h3 style="margin-top:0">📖 ¿Cómo funciona?</h3>

<p><b>1. Marcás puntos de suelo desnudo</b><br/>
Hacé clic en zonas donde el suelo es visible 
(caminos, bordes, entre-surcos). Cada clic 
registra la coordenada (X, Y) y la cota Z 
del pixel.</p>

<p><b>2. Se interpola el MDT</b><br/>
Se utiliza el algoritmo <b>Thin Plate Spline (TPS)</b> para interpolar los puntos de suelo marcados. El plugin optimiza automáticamente el parámetro de suavizado mediante <b>validación cruzada (LOOCV)</b> para asegurar que el modelo del terreno sea lo más preciso posible, incluso debajo de las plantas.</p>

<p><b>3. Se calcula el MAC</b><br/>
<b>MAC = MDS − MDT</b><br/>
(Modelo de Altura de Canopeo)<br/>
Al restar el suelo interpolado (MDT) del 
raster original (MDS), queda la <b>altura 
de todos los objetos</b> sobre el suelo 
(plantas, árboles, etc.). Valores negativos 
se fuerzan a 0.</p>

<p><b>4. Se calcula el MVC</b><br/>
<b>MVC = MAC × Área del pixel</b><br/>
(Modelo de Volumen de Canopeo)<br/>
Multiplica la altura de cada pixel por su 
resolución espacial (ej: 0.05m × 0.05m). 
Da el volumen de biomasa en m³ por pixel.</p>

<hr/>
<table border="1" cellpadding="3" cellspacing="0" style="font-size:10px">
<tr><th>Sigla</th><th>Español</th><th>English</th></tr>
<tr><td>MDS</td><td>Modelo Digital de Superficie</td><td>DSM</td></tr>
<tr><td>MDT</td><td>Modelo Digital de Terreno</td><td>DTM</td></tr>
<tr><td>MAC</td><td>Mod. Altura de Canopeo</td><td>CHM</td></tr>
<tr><td>MVC</td><td>Mod. Volumen de Canopeo</td><td>CVM</td></tr>
</table>
<p style="font-size:11px">Autor: <a href="mailto:menes.josefernando@inta.gob.ar">José Fernando Menes</a></p>
</html>""": """<html>
<h3 style="margin-top:0">📖 工作原理</h3>

<p><b>1. 标记裸露地面点</b><br/>
在可见地面的区域（路径、边缘、行间）单击。
每次单击都会记录该像素的 (X, Y) 坐标和 Z 高程。</p>

<p><b>2. DTM 插值</b><br/>
使用 <b>薄板样条插值 (TPS)</b> 算法对标记的地表点进行插值。插件通过 <b>留一法交叉验证 (LOOCV)</b> 自动优化平滑参数，以确保地形模型在植被覆盖下也能保持最高精度。</p>

<p><b>3. CHM 计算</b><br/>
<b>CHM = DSM − DTM</b><br/>
(冠层高度模型)<br/>
通过从原始栅格中减去插值地面，
我们得到了地面上方<b>所有物体的高度</b>。负值强制设为 0。</p>

<p><b>4. CVM 计算</b><br/>
<b>CVM = CHM × 像素面积</b><br/>
(冠层体积模型)<br/>
将高度乘以其空间分辨率。计算生物量体积 (m³)。</p>

<hr/>
<table border="1" cellpadding="3" cellspacing="0" style="font-size:10px">
<tr><th>缩写</th><th>Español</th><th>中文</th></tr>
<tr><td>DSM</td><td>Modelo Digital de Superficie</td><td>数字地表模型</td></tr>
<tr><td>DTM</td><td>Modelo Digital de Terreno</td><td>数字地形模型</td></tr>
<tr><td>CHM</td><td>Mod. Altura de Canopeo</td><td>冠层高度模型</td></tr>
<tr><td>CVM</td><td>Mod. Volumen de Canopeo</td><td>冠层体积模型</td></tr>
</table>
<p style="font-size:11px">作者: <a href="mailto:menes.josefernando@inta.gob.ar">José Fernando Menes</a></p>
</html>"""
}

def tr(text):
    try:
        from qgis.PyQt.QtCore import QSettings
        locale_str = QSettings().value('locale/userLocale', 'en').lower()
        if locale_str.startswith('pt'):
            return _strings_pt.get(text, text)
        elif locale_str.startswith('zh'):
            return _strings_zh.get(text, text)
        elif not locale_str.startswith('es'):
            return _strings_en.get(text, text)
    except:
        pass
    return text
