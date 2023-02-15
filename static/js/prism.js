/* global tinymce */

tinymce.init({
  selector: 'textarea',
  plugins: 'emoticons wordcount lists',
  menubar: false,
  statusbar: true,
  branding: true,
  elementpath: false,
  toolbar: 'wordcount | emoticons | blocks fontsize | hr | bold italic underline strikethrough | backcolor | alignleft aligncenter alignright alignjustify | indent outdent | numlist bullist| removeformat',
  content_css: "{% static 'css/tinymce.css' %}", // resolved to http://domain.mine/mysite/mycontent.css
});
