from wtforms import Form, validators, SubmitField, URLField


class NewUrl(Form):
    long_url = URLField('Long url', validators=[
        validators.input_required(),
        validators.url()
    ])
    
    def reset(self):
        blankData = dict([ ('csrf', self.reset_csrf() ) ])
        self.process(blankData)
        