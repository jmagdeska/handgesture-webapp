// function readURL(input) {
//         if (input.files && input.files[0]) {
//             var reader = new FileReader();
            
//             reader.onload = function (e) {
//                 $('#image').attr('src', e.target.result);
//             }
            
//             reader.readAsDataURL(input.files[0]);
//         }
//     }
    
//     $("#id_docfile").change(function(){
//         readURL(this);
//     });

function previewFile() {
  var preview = document.querySelector('img');
  var file    = document.querySelector('input[type=file]').files[0];
  var reader  = new FileReader();

  reader.addEventListener("load", function () {
    preview.src = reader.result;
	preview.hidden = false;
  }, false);

  if (file) {
    reader.readAsDataURL(file);
  }
}