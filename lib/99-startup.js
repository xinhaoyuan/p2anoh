$(function() {
	$("#page-container")
	.annotator()
	.annotator("addPlugin", "Unsupported")
	.annotator("addPlugin", "Filter")
	.annotator("addPlugin", "Tags")
	.annotator("addPlugin", "Offline");
	
	lsSave = $("<div id='local-storage-save'>Save</div>").click(function() {
		var content = "data:text/json;charset=utf-8," + JSON.stringify(localStorage);
		var encodedUri = encodeURI(content);
		var link = document.createElement("a");
		link.setAttribute("href", encodedUri);
		link.setAttribute("download", "annotations.json");
		document.body.appendChild(link);
		link.click();
	});
	lsImportInput = $("<input id='local-storage-import-input' type='file' id='file-input' />").on("change", function(e) {
		var file = e.target.files[0];
		if (!file) return;
		var reader = new FileReader();
		reader.onload = function(e) {
			var contents = e.target.result;
			var data = JSON.parse(contents);
			localStorage.clear();
			for (var key in data) {
				localStorage.setItem(key, data[key]);
			}
			window.location.reload();
		};
		reader.readAsText(file);
	});
	lsLoad = $("<div id='local-storage-load'>Load</div>").click(function() {
		lsImportInput.click();
	});
	lsSync = $("<div class='local-storage-sync'/>").append(lsSave).append(lsLoad).append(lsImportInput);
	$("body").append(lsSync);
});