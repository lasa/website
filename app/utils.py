from app import app
from app.models import Page
from flask import render_template
import os

def render_with_navbar(template, **kwargs):
    pages = {'calendars': Page.query.filter_by(category='calendars').order_by(Page.index.asc()),
                'about': Page.query.filter_by(category='about').order_by(Page.index.asc()),
                'academics': Page.query.filter_by(category='academics').order_by(Page.index.asc()),
                'students': Page.query.filter_by(category='students').order_by(Page.index.asc()),
                'parents': Page.query.filter_by(category='parents').order_by(Page.index.asc()),
                'admissions': Page.query.filter_by(category='admissions').order_by(Page.index.asc())}
    return render_template(template, pages=pages, **kwargs)

#custom widget for rendering a TinyMCE input
def TinyMCE(field):
    uploads = os.listdir(os.path.join('app', app.config['UPLOAD_FOLDER']))
    uploads.remove(".gitignore")
    image_list = link_list = "["
    image_extensions = ["png", "jpg", "jpeg", "gif", "bmp"]

    for upload in uploads:
        if '.' in upload and upload.rsplit('.', 1)[1].lower() in image_extensions:
            image_list += "{title: '" + upload + "', value: '/uploads/" + upload + "'},"
        else:
            link_list += "{title: '" + upload + "', value: '/uploads/" + upload + "'},"

    image_list = image_list[:-1] + '],'
    link_list = link_list[:-1] + ']'

    return """  <script src="//cdn.tinymce.com/4/tinymce.min.js"></script>
         <script>
            function customInit() {
                setTimeout(function(){
                    window.scrollTo(0, 0);
                    $('form *:input[type!=hidden]:first').focus();
                },0);
            }
            tinymce.init({ 
            oninit: customInit(),
            selector:'#editor', 
            theme: 'modern',
            height: 800,
            convert_urls: false,
            fontsize_formats: '8pt 10pt 11pt 12pt 14pt 18pt 24pt 36pt',
            setup: function(ed) {
                     ed.on('init', function(ed) {
                       ed.target.editorCommands.execCommand("fontSize", false, "11pt");
                     });
                   },
			plugins: [
            'advlist autolink link image lists charmap preview hr anchor',
            'wordcount visualblocks visualchars code nonbreaking',
            'table contextmenu paste textcolor'
            ],
            table_default_attributes: {
            class: 'table-condensed'
            },
            content_css: '/static/css/tinymce.css',
            toolbar: 'styleselect | fontsizeselect | bold italic underline | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | forecolor backcolor',
            plugin_preview_height: 600,
            plugin_preview_width: 925,
            link_context_toolbar: true,
            link_title: false,
            image_advtab: true,
            image_title: true,
            image_description: false,
            image_list: """ + image_list + """
            link_list: """ + link_list + """
         });
         </script>
         <textarea id='editor'> %s </textarea>""" % field._value()


