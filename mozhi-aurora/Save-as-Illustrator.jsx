#target illustrator
(function () {
    var folder = File($.fileName).parent;
    var source = File(folder.fsName + "/MOZHI-aurora-420x148mm.svg");
    if (!source.exists) { alert("Place this script next to MOZHI-aurora-420x148mm.svg."); return; }
    var target = File(folder.fsName + "/MOZHI-aurora-420x148mm.ai");
    if (target.exists && !confirm("Replace existing AI file?")) return;
    var doc = app.open(source);
    var options = new IllustratorSaveOptions();
    options.pdfCompatible = true;
    options.compressed = true;
    doc.saveAs(target, options);
    alert("Saved: " + target.fsName);
})();
