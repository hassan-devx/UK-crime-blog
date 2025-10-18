import markdown
import bleach


 
def markdown_filter(text):
    html = markdown.markdown(text)
    return bleach.clean(html)

# Register the filter globally
def register_filters(app):
    app.jinja_env.filters['markdown'] = markdown_filter