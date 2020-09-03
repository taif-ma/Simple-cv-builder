var tinymceInit = function() {
  tinymce.init({
    selector: 'textarea',
    height: 300,
    width: 400,
    menubar: false,
    plugins: [
        'advlist lists' ],
    toolbar: 'undo redo | bold italic underline | bullist numlist | removeformat ',
    content_css: [
      '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
      '//www.tinymce.com/css/codepen.min.css']
  });
};
