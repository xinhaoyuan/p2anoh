$(function() {
	$("#page-container")
	.annotator()
	.annotator("addPlugin", "Unsupported")
	.annotator("addPlugin", "Filter")
	.annotator("addPlugin", "Tags")
	.annotator("addPlugin", "Offline");
});