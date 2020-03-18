$(function() {
	var cvs = $('#canvas')[0],
	ctx = cvs.getContext('2d'),
	im1 = new Image();
    im2 = new Image();
    im3 = new Image();
    im4 = new Image();
	$('#file1').change(function(ev) {
		var files = ev.target.files;
		$.each(files, function(index, item) {
			var reader = new FileReader();
			reader.onload = function(file1) {
				var dataUrl = file1.target.result;
				im1.src = dataUrl;
				im1.onload = function() {
					ctx.drawImage(im1, 0, 0, 320*240);
                };
            };
                reader.readAsDataURL(item);
        });
    });
	$('#file2').change(function(ev) {
		var files = ev.target.files;
		$.each(files, function(index, item) {
			var reader = new FileReader();
			reader.onload = function(file2) {
				var dataUrl = file2.target.result;
				im2.src = dataUrl;
				im2.onload = function() {
					ctx.drawImage(im2, 320, 0, 320*240);
                };
            };
                reader.readAsDataURL(item);
        });
    });
	$('#file3').change(function(ev) {
		var files = ev.target.files;
		$.each(files, function(index, item) {
			var reader = new FileReader();
			reader.onload = function(file3) {
				var dataUrl = file3.target.result;
				im3.src = dataUrl;
				im3.onload = function() {
					ctx.drawImage(im3, 0, 180, 320*240);
                };
            };
                reader.readAsDataURL(item);
        });
    });
	$('#file4').change(function(ev) {
		var files = ev.target.files;
		$.each(files, function(index, item) {
			var reader = new FileReader();
			reader.onload = function(file4) {
				var dataUrl = file4.target.result;
				im4.src = dataUrl;
				im4.onload = function() {
					ctx.drawImage(im4, 320,180, 320*240);
                };
            };
                reader.readAsDataURL(item);
        });
    });
});
